"""Independent graph optimization and exhaustive optimum-rank projections.

Run with .venv/bin/python -B; candidate is executed only as a subprocess.
The unchanged exhaustive source reference is reused, not the candidate oracle.
"""
import itertools
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parents[2] / 'work'
sys.path.insert(0, str(WORK))
from source_reference import solve
from ortools.sat.python import cp_model
import networkx as nx


def invoke(value, extract=False):
    command = [sys.executable, '-B', str(WORK / 'algorithm.py')]
    if extract:
        command.append('--extract')
    result = subprocess.run(command, input=json.dumps(value), text=True,
                            capture_output=True, check=True)
    return json.loads(result.stdout)


def tree(shape, prefix):
    nodes = []
    def visit(part):
        name = prefix + str(len(nodes))
        node = dict(id=name, children=[], label=None)
        nodes.append(node)
        if isinstance(part, str):
            node['label'] = part
        else:
            node['children'] = [visit(p) for p in reversed(part)]
        return name
    root = visit(shape)
    return dict(root=root, nodes=list(reversed(nodes)))


def check(left, right, labels):
    source = dict(problem='maaforest', labels=labels, root_label='rho',
                  t1=tree(left, 'left:'), t2=tree(right, 'right:'))
    optimum, forests = solve(source)
    graph = invoke(source)
    assert graph == invoke(source)
    vertices = graph['vertices']
    arcs = set(map(tuple, graph['arcs']))
    assert len(vertices) == len(set(vertices))
    assert all(u in vertices and v in vertices and (v,u) in arcs for u,v in arcs)
    model = cp_model.CpModel()
    deleted = {v: model.new_bool_var(str(i)) for i,v in enumerate(vertices)}
    # Constraints are derived solely from actual graph edges. On a bidirected
    # graph, covering every edge is exactly directed feedback vertex deletion.
    for u,v in arcs:
        model.add_bool_or(deleted[u], deleted[v])
    undirected = nx.Graph()
    undirected.add_nodes_from(vertices)
    undirected.add_edges_from(arcs)
    for clique in nx.find_cliques(undirected):
        model.add(sum(deleted[v] for v in clique) >= len(clique)-1)
    model.minimize(sum(deleted.values()))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    assert solver.solve(model) == cp_model.OPTIMAL
    target_optimum = sum(solver.value(v) for v in deleted.values())
    model.clear_objective()
    model.add(sum(deleted.values()) == target_optimum)

    def recover():
        chosen = [v for v in vertices if solver.value(deleted[v])]
        assert len(chosen) == target_optimum
        chosen_set = set(chosen)
        assert all(u in chosen_set or v in chosen_set for u,v in arcs)
        output = invoke(dict(source=source, target_solution=dict(
            problem='dfvs', feedback_vertex_set=list(reversed(chosen)))), True)
        partition = tuple(sorted(tuple(sorted(b)) for b in output['components']))
        assert output['problem'] == 'maaforest'
        assert output['num_components'] == optimum and partition in forests
        return partition

    # Fully enumerate the distinct optimum-threshold leaf-bit projections,
    # rather than spend a cap on clause-gadget choices with identical ranks.
    width = (optimum-1).bit_length()
    projection = [deleted[f'{optimum}:v:{2+i}:1']
                  for i in range((len(labels)+1)*width)]
    projected = model.clone()
    count = 0
    recovered = set()
    while True:
        status = solver.solve(projected)
        if status == cp_model.INFEASIBLE:
            break
        assert status == cp_model.OPTIMAL
        recovered.add(recover())
        count += 1
        projected.add_bool_or(v.Not() if solver.value(v) else v for v in projection)

    # On the quartet, k=2 is infeasible. Force every binary leaf-rank pattern
    # there while retaining a globally minimum target solution.
    adversarial = 0
    if optimum == 3:
        for bits in itertools.product((0,1), repeat=len(labels)+1):
            forced = model.clone()
            for i,bit in enumerate(bits):
                forced.add(deleted[f'2:v:{2+i}:1'] == bit)
            assert solver.solve(forced) == cp_model.OPTIMAL
            recover()
            adversarial += 1
    print(json.dumps(dict(leaves=len(labels), source_optimum=optimum,
        source_optima=len(forests), vertices=len(vertices), arcs=len(arcs),
        target_optimum=target_optimum, exhaustive_optimum_rank_projections=count,
        recovered_source_optima=len(recovered), forced_infeasible_rank_patterns=adversarial)), flush=True)


check((('a','b'),'c'), (('a','c'),'b'), ['c','a','b'])
check((('a','b'),('c','d')), (('a','c'),('b','d')), ['d','c','b','a'])
print('PASS: all projected target ties and all forced infeasible rank patterns recovered exact source optima.')
