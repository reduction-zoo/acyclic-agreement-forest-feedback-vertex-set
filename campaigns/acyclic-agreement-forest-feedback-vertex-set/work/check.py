"""Definition-based exact oracles; no imports from candidate implementations."""
import argparse
import itertools
import json
from pathlib import Path
import subprocess
import sys

import z3

WORK = Path(__file__).resolve().parent
SOURCE_LEAF_CAP = 7
TARGET_OUTPUT_CAP = 128


def acyclic(vertices, arcs):
    remaining = set(vertices)
    while remaining:
        incoming = {v for u, v in arcs if u in remaining and v in remaining}
        roots = remaining - incoming
        if not roots:
            return False
        remaining -= roots
    return True


def parse_source(source):
    if not isinstance(source, dict) or source.get('problem') != 'maaforest':
        raise ValueError('expected maaforest instance')
    labels = source.get('labels')
    rho = source.get('root_label')
    if (not isinstance(labels, list) or not labels
            or any(not isinstance(x, str) or not x for x in labels)
            or len(set(labels)) != len(labels)
            or not isinstance(rho, str) or not rho or rho in labels):
        raise ValueError('invalid leaf/root labels')
    trees = []
    for key in ('t1', 't2'):
        raw = source.get(key)
        if not isinstance(raw, dict) or not isinstance(raw.get('nodes'), list):
            raise ValueError('expected tree nodes')
        nodes = {}
        for node in raw['nodes']:
            if (not isinstance(node, dict) or not isinstance(node.get('id'), str)
                    or not node['id'] or node['id'] in nodes):
                raise ValueError('invalid or duplicate node id')
            kids = node.get('children')
            if (not isinstance(kids, list) or len(kids) not in (0, 2)
                    or any(not isinstance(x, str) for x in kids)
                    or len(set(kids)) != len(kids)):
                raise ValueError('tree must be binary')
            if (kids and node.get('label') is not None) or (
                    not kids and node.get('label') not in labels):
                raise ValueError('invalid node label')
            nodes[node['id']] = node
        root = raw.get('root')
        if not isinstance(root, str) or root not in nodes:
            raise ValueError('invalid root')
        parent = {}
        for v, node in nodes.items():
            for child in node['children']:
                if child not in nodes or child in parent:
                    raise ValueError('unknown child or multiple parents')
                parent[child] = v
        if set(parent) != set(nodes) - {root}:
            raise ValueError('invalid tree parents')
        seen, todo = set(), [root]
        while todo:
            v = todo.pop()
            if v in seen:
                raise ValueError('tree cycle')
            seen.add(v)
            todo.extend(nodes[v]['children'])
        if seen != set(nodes):
            raise ValueError('disconnected tree')
        found = [v['label'] for v in nodes.values() if not v['children']]
        if sorted(found) != sorted(labels):
            raise ValueError('leaf labels do not match')
        # Integer indices and fresh indices prevent collisions with user ids.
        ids = {v: i for i, v in enumerate(nodes)}
        children = {ids[v]: tuple(ids[c] for c in node['children'])
                    for v, node in nodes.items()}
        label_of = {ids[v]: node['label'] for v, node in nodes.items()
                    if not node['children']}
        above, extra = len(nodes), len(nodes) + 1
        children[above] = (ids[root], extra)
        children[extra] = ()
        label_of[extra] = rho
        ancestors = {}
        def walk(v, chain):
            ancestors[v] = chain
            for c in children[v]:
                walk(c, chain + (v,))
        walk(above, ())
        trees.append((children, label_of, ancestors))
    return tuple(sorted(labels + [rho])), trees


def restriction(tree, block):
    children, label_of, ancestors = tree
    leaves = [v for v, label in label_of.items() if label in block]
    paths = [ancestors[v] + (v,) for v in leaves]
    root = next(v for v in reversed(paths[0]) if all(v in p for p in paths))
    vertices = frozenset(v for p in paths for v in p[p.index(root):])
    def shape(v):
        if v in label_of:
            return ('leaf', label_of[v])
        branches = [shape(c) for c in children[v] if c in vertices]
        return branches[0] if len(branches) == 1 else ('fork', *sorted(branches))
    return root, vertices, shape(root)


def block_data(source):
    labels, trees = parse_source(source)
    data = {}
    for k in range(1, len(labels) + 1):
        for block in itertools.combinations(labels, k):
            pair = tuple(restriction(tree, block) for tree in trees)
            if pair[0][2] == pair[1][2]:
                data[block] = pair
    return labels, trees, data


def feasible_partition(blocks, labels, trees, data):
    if sorted(x for b in blocks for x in b) != list(labels):
        return False
    if any(b not in data for b in blocks):
        return False
    arcs = set()
    for t, tree in enumerate(trees):
        seen = set()
        for b in blocks:
            vertices = data[b][t][1]
            if seen & vertices:
                return False
            seen.update(vertices)
        for i, b in enumerate(blocks):
            for j, c in enumerate(blocks):
                if i != j and data[b][t][0] in tree[2][data[c][t][0]]:
                    arcs.add((i, j))
    return acyclic(range(len(blocks)), arcs)


def validate_source_output(source, output, optimum=None):
    if not isinstance(output, dict) or output.get('problem') != 'maaforest':
        return False
    blocks = output.get('components')
    if (not isinstance(blocks, list) or not blocks
            or any(not isinstance(b, list) or not b or
                   any(not isinstance(x, str) for x in b) for b in blocks)
            or type(output.get('num_components')) is not int
            or output['num_components'] != len(blocks)):
        return False
    labels, trees, data = block_data(source)
    blocks = tuple(tuple(sorted(b)) for b in blocks)
    return (feasible_partition(blocks, labels, trees, data)
            and (optimum is None or len(blocks) == optimum))


def solve_source(source):
    """All minimum forests on the explicit finite source domain."""
    if len(source['labels']) > SOURCE_LEAF_CAP:
        raise ValueError('source oracle domain exceeded')
    labels, trees, data = block_data(source)
    blocks = list(data)
    chosen = [z3.Bool(f'b{i}') for i in range(len(blocks))]
    ranks = [z3.Int(f'r{i}') for i in range(len(blocks))]
    solver = z3.Solver()
    for label in labels:
        solver.add(z3.PbEq([(chosen[i], 1) for i, b in enumerate(blocks)
                           if label in b], 1))
    for i, b in enumerate(blocks):
        for j in range(i + 1, len(blocks)):
            c = blocks[j]
            if any(data[b][t][1] & data[c][t][1] for t in (0, 1)):
                solver.add(z3.Or(z3.Not(chosen[i]), z3.Not(chosen[j])))
        for j, c in enumerate(blocks):
            if i != j and any(data[b][t][0] in trees[t][2][data[c][t][0]]
                              for t in (0, 1)):
                solver.add(z3.Implies(z3.And(chosen[i], chosen[j]), ranks[i] < ranks[j]))
    objective = [(v, 1) for v in chosen]
    for k in range(1, len(labels) + 1):
        solver.push()
        solver.add(z3.PbEq(objective, k))
        result = solver.check()
        if result == z3.unknown:
            raise RuntimeError('source oracle unknown: ' + solver.reason_unknown())
        if result == z3.sat:
            break
        solver.pop()
    else:
        raise AssertionError('singleton forest must exist')
    solutions = set()
    while result == z3.sat:
        model = solver.model()
        indices = [i for i, v in enumerate(chosen) if z3.is_true(model.eval(v))]
        partition = tuple(sorted(blocks[i] for i in indices))
        if not feasible_partition(partition, labels, trees, data):
            raise AssertionError('invalid source oracle witness')
        solutions.add(partition)
        solver.add(z3.Or([z3.Not(chosen[i]) for i in indices]))
        result = solver.check()
    if result != z3.unsat:
        raise RuntimeError('source optimum enumeration unknown')
    return k, solutions


def parse_target(target):
    if not isinstance(target, dict) or target.get('problem') != 'dfvs':
        raise ValueError('expected dfvs instance')
    vertices, arcs = target.get('vertices'), target.get('arcs')
    if (not isinstance(vertices, list)
            or any(not isinstance(v, str) or not v for v in vertices)
            or len(set(vertices)) != len(vertices) or not isinstance(arcs, list)):
        raise ValueError('invalid digraph')
    vset = set(vertices)
    for edge in arcs:
        if (not isinstance(edge, list) or len(edge) != 2
                or any(not isinstance(v, str) or v not in vset for v in edge)):
            raise ValueError('invalid arc')
    return vertices, set(map(tuple, arcs))


def valid_dfvs(vertices, arcs, chosen):
    return (isinstance(chosen, list) and all(isinstance(v, str) for v in chosen)
            and len(set(chosen)) == len(chosen) and set(chosen) <= set(vertices)
            and acyclic(set(vertices) - set(chosen), arcs))


def solve_bidirected(vertices, arcs, cap):
    """Independent minimum vertex-cover model for a bidirected input graph.

    Every edge is a directed 2-cycle, so hitting these edges is necessary and
    sufficient. No graph naming convention or candidate metadata is read.
    """
    from ortools.sat.python import cp_model
    model = cp_model.CpModel()
    chosen = {v: model.new_bool_var(f'x{i}') for i,v in enumerate(vertices)}
    for u,v in arcs:
        if u <= v:
            model.add_bool_or([chosen[u], chosen[v]])
    total = sum(chosen.values())
    model.minimize(total)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    result = solver.solve(model)
    if result != cp_model.OPTIMAL:
        raise RuntimeError('CP-SAT did not certify global optimality: '+solver.status_name(result))
    optimum = sum(solver.value(x) for x in chosen.values())
    model.clear_objective()
    model.add(total == optimum)
    class Outputs(cp_model.CpSolverSolutionCallback):
        def __init__(self):
            super().__init__()
            self.outputs = set()
        def on_solution_callback(self):
            output = tuple(sorted(v for v,x in chosen.items() if self.value(x)))
            if not valid_dfvs(vertices, arcs, list(output)) or len(output) != optimum:
                raise AssertionError('invalid CP-SAT witness')
            self.outputs.add(output)
            if len(self.outputs) > cap:
                self.stop_search()
    callback = Outputs()
    solver.parameters.enumerate_all_solutions = True
    result = solver.solve(model, callback)
    if result not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError('CP-SAT witness enumeration failed: '+solver.status_name(result))
    outputs = callback.outputs
    complete = len(outputs) <= cap and result == cp_model.OPTIMAL
    return optimum, set(sorted(outputs)[:cap]), complete


def solve_target(target, cap=TARGET_OUTPUT_CAP):
    vertices, arcs = parse_target(target)
    if not vertices:
        return 0, {()}, True
    if all((v,u) in arcs for u,v in arcs):
        return solve_bidirected(vertices, arcs, cap)
    deleted = {v: z3.Bool(f'd{i}') for i, v in enumerate(vertices)}
    ranks = {v: z3.Int(f'p{i}') for i, v in enumerate(vertices)}
    solver = z3.Solver()
    for u, v in arcs:
        solver.add(z3.Or(deleted[u], deleted[v], ranks[u] < ranks[v]))
    terms = [(v, 1) for v in deleted.values()]
    # Binary search uses only conclusive SAT/UNSAT, with no time limit.
    low, high = 0, len(vertices)
    while low < high:
        mid = (low + high) // 2
        solver.push()
        solver.add(z3.PbLe(terms, mid))
        result = solver.check()
        solver.pop()
        if result == z3.sat:
            high = mid
        elif result == z3.unsat:
            low = mid + 1
        else:
            raise RuntimeError('target optimum unknown')
    solver.add(z3.PbEq(terms, low))
    solutions = set()
    while len(solutions) < cap:
        result = solver.check()
        if result == z3.unsat:
            return low, solutions, True
        if result != z3.sat:
            raise RuntimeError('target enumeration unknown')
        model = solver.model()
        chosen = tuple(sorted(v for v in vertices if z3.is_true(model.eval(deleted[v]))))
        if len(chosen) != low or not valid_dfvs(vertices, arcs, list(chosen)):
            raise AssertionError('invalid target oracle witness')
        solutions.add(chosen)
        solver.add(z3.Or([z3.Not(deleted[v]) for v in chosen]))
    result = solver.check()
    if result == z3.unknown:
        raise RuntimeError('target enumeration completeness unknown')
    return low, solutions, result == z3.unsat


def run_map(path, payload, extract=False):
    command = [sys.executable, str(path)] + (['--extract'] if extract else [])
    result = subprocess.run(command, input=json.dumps(payload), text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f'candidate exit {result.returncode}: {result.stderr}')
    return json.loads(result.stdout)


def check_candidate(path, cases, evidence_dir):
    recoveries = capped = 0
    for i, case in enumerate(cases, 1):
        source = case['source']
        optimum, _ = solve_source(source)
        if optimum != case['source_opt_components']:
            raise AssertionError('stored source ground truth mismatch')
        target = run_map(path, source)
        target_opt, witnesses, complete = solve_target(target)
        if not witnesses:
            raise AssertionError('missing minimum target output')
        for chosen in witnesses:
            recovered = run_map(path, {'source': source, 'target_solution': {
                'problem': 'dfvs', 'feedback_vertex_set': list(chosen)}}, True)
            if not validate_source_output(source, recovered, optimum):
                evidence = evidence_dir / 'recovery-failure.json'
                evidence.write_text(json.dumps(dict(source=source, target=target,
                    target_solution=list(chosen), recovered=recovered,
                    expected_source_optimum=optimum), ensure_ascii=False, indent=2)+'\n')
                raise AssertionError(f'{case["name"]}: invalid/suboptimal recovery; {evidence}')
            recoveries += 1
        capped += not complete
        print(f'{i}/{len(cases)} {case["name"]}: target_opt={target_opt} '
              f'outputs={len(witnesses)} all_optima={complete}', flush=True)
    print(f'candidate: instances={len(cases)} recoveries={recoveries} capped_instances={capped}')


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--self-test', action='store_true')
    group.add_argument('--candidate', type=Path)
    args = parser.parse_args()
    if args.self_test:
        from prepare import self_test
        self_test()
    else:
        check_candidate(args.candidate.resolve(),
                        json.loads((WORK / 'cases.json').read_text())['cases'],
                        WORK / 'evidence')


if __name__ == '__main__':
    main()
