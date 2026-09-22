"""Independent actual-target checks; imports neither check.py nor algorithm.py."""
import argparse
import itertools
import json
from pathlib import Path
import subprocess
import sys

import networkx as nx
from ortools.sat.python import cp_model
from source_reference import solve as source_optima


def invoke(path, value, extract=False):
    command=[sys.executable,str(path)] + (['--extract'] if extract else [])
    result=subprocess.run(command,input=json.dumps(value),capture_output=True,text=True)
    if result.returncode: raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


def connected_optima(target, cap=4):
    vertices=target['vertices'];arcs={tuple(e) for e in target['arcs']}
    assert target['problem']=='dfvs' and len(vertices)==len(set(vertices))
    assert all(u in vertices and v in vertices and (v,u) in arcs for u,v in arcs)
    graph=nx.Graph();graph.add_nodes_from(vertices);graph.add_edges_from(arcs)
    model=cp_model.CpModel();kept={v:model.new_bool_var(f'keep{i}') for i,v in enumerate(vertices)}
    for v in vertices:
        if (v,v) in arcs:model.add(kept[v]==0)
    for clique in nx.find_cliques(graph):
        model.add_at_most_one(kept[v] for v in clique)
    # Certificate upper bound for the independent set, using disjoint cliques.
    unavailable={v for v in vertices if (v,v) in arcs}; bound=0
    packing=[([v],0) for v in unavailable]
    for clique in nx.find_cliques(graph):
        if len(clique)>=3 and not unavailable.intersection(clique):
            unavailable.update(clique); bound+=1; packing.append((clique,1))
    position={v:i for i,v in enumerate(vertices)}
    for v in vertices:
        if v in unavailable: continue
        partners=[u for u in graph[v] if u not in unavailable]
        if partners:
            u=min(partners,key=position.get); unavailable.update((u,v)); bound+=1; packing.append(([u,v],1))
    packing.extend(([v],1) for v in set(vertices)-unavailable)
    bound+=len(set(vertices)-unavailable)
    model.add(sum(kept.values())<=bound)
    model.maximize(sum(kept.values()))
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    status=solver.solve(model)
    assert status==cp_model.OPTIMAL,solver.status_name(status)
    size=sum(solver.value(x) for x in kept.values())
    model.clear_objective();model.add(sum(kept.values())==size)
    if size==bound:
        for group,limit in packing:model.add(sum(kept[v] for v in group)==limit)
    outputs=[]
    for _ in range(cap):
        status=solver.solve(model)
        if status==cp_model.INFEASIBLE:break
        assert status==cp_model.OPTIMAL,solver.status_name(status)
        selected=[v for v in vertices if not solver.value(kept[v])]
        deleted=set(selected)
        assert len(selected)==len(vertices)-size
        assert all(u in deleted or v in deleted for u,v in arcs)
        outputs.append(selected)
        model.add_bool_or(kept[v] for v in selected)
    return len(vertices)-size,outputs


def target_optima(target, cap=4):
    graph=nx.Graph();graph.add_nodes_from(target['vertices']);graph.add_edges_from(target['arcs'])
    pieces=sorted(nx.connected_components(graph),key=lambda c:(-len(c),min(c)))
    total=0;combined=[[]]
    for nodes in pieces:
        local=dict(problem='dfvs',vertices=[v for v in target['vertices'] if v in nodes],
                   arcs=[e for e in target['arcs'] if e[0] in nodes])
        size,outputs=connected_optima(local,max(1,(cap+len(combined)-1)//len(combined)))
        total+=size;combined=[a+b for a in combined for b in outputs][:cap]
    return total,combined


def encode(shape, prefix):
    nodes=[]
    def visit(t):
        index=prefix+str(len(nodes));node=dict(id=index,children=[],label=None);nodes.append(node)
        if isinstance(t,str):node['label']=t
        else:node['children']=[visit(c) for c in t]
        return index
    root=visit(shape)
    return dict(root=root,nodes=list(reversed(nodes)))


def caterpillar(labels):
    result=labels[-1]
    for leaf in reversed(labels[:-1]):result=(leaf,result)
    return result


def cases():
    for n in range(1,5):
        labels=['α','b,()','leaf:2','ρ'][:n]
        for offset in range(n):
            a=caterpillar(labels)
            b=caterpillar(labels[offset:]+labels[:offset])
            yield dict(problem='maaforest',labels=list(reversed(labels)),root_label='root:extra',
                       t1=encode(a,'first:'),t2=encode(b,'unrelated:'))
    labels=['a','b','c','d','e']
    for offset in (1,2):
        yield dict(problem='maaforest',labels=labels,root_label='ρ',
                   t1=encode(caterpillar(labels),'left'),
                   t2=encode(caterpillar(labels[offset:]+labels[:offset]),'right'))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--candidate',type=Path,required=True)
    args=parser.parse_args();count=recoveries=0
    # Tiny exact graph ground truth, including every deletion tie and a self-loop.
    tiny=[dict(problem='dfvs',vertices=['u','v'],arcs=[['u','v'],['v','u']]),
          dict(problem='dfvs',vertices=['u'],arcs=[['u','u']]),
          dict(problem='dfvs',vertices=['u','v'],arcs=[])]
    for graph,expected in zip(tiny,(1,1,0)):
        actual,outputs=target_optima(graph);assert actual==expected and outputs
    for count,source in enumerate(cases(),1):
        optimum,partitions=source_optima(source)
        graph=invoke(args.candidate,source)
        target_size,outputs=target_optima(graph)
        assert outputs
        for output in outputs:
            recovered=invoke(args.candidate,dict(source=source,target_solution=dict(
                problem='dfvs',feedback_vertex_set=output)),True)
            partition=tuple(sorted(tuple(sorted(b)) for b in recovered['components']))
            if (recovered.get('problem')!='maaforest' or type(recovered.get('num_components')) is not int
                    or recovered['num_components']!=optimum or partition not in partitions):
                path=Path(__file__).with_name('evidence')/'verify-failure.json'
                path.write_text(json.dumps(dict(source=source,target_solution=output,
                    recovered=recovered,expected_optimum=optimum),ensure_ascii=False,indent=2))
                raise AssertionError(str(path))
            recoveries+=1
        print(f'verify {count}: leaves={len(source["labels"])} vertices={len(graph["vertices"])} '
              f'target_opt={target_size} outputs={len(outputs)} source_opt={optimum}',flush=True)
    print(f'PASS independent instances={count} target_recoveries={recoveries}')


if __name__=='__main__':main()
