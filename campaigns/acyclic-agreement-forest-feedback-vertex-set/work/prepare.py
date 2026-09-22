"""Deterministic dataset generation and definition-level oracle tests."""
import argparse
from copy import deepcopy
from functools import lru_cache
import itertools
import json
from pathlib import Path
import random
import tempfile

import check
import source_reference as reference

WORK = Path(__file__).resolve().parent
SEED = 20260922


@lru_cache(None)
def trees(labels):
    if len(labels) == 1:
        return (labels[0],)
    out = []
    for k in range(len(labels)):
        for subset in itertools.combinations(labels[1:], k):
            left = (labels[0],) + subset
            right = tuple(x for x in labels if x not in left)
            if right:
                out.extend((a, b) for a in trees(left) for b in trees(right))
    return tuple(out)


def encode_tree(shape, prefix):
    nodes = []
    def visit(value):
        node = {'id': prefix + str(len(nodes)), 'children': [], 'label': None}
        nodes.append(node)
        if isinstance(value, str):
            node['label'] = value
        else:
            node['children'] = [visit(v) for v in value]
        return node['id']
    root = visit(shape)
    return {'root': root, 'nodes': nodes}


def source(a, b):
    t1, t2 = encode_tree(a, 'left:'), encode_tree(b, 'right:')
    labels = sorted(n['label'] for n in t1['nodes'] if n['label'] is not None)
    return {'problem': 'maaforest', 'labels': labels, 'root_label': 'ρ', 't1': t1, 't2': t2}


def renamed(instance):
    out = deepcopy(instance)
    for tag in ('t1', 't2'):
        tree = out[tag]
        names = {n['id']: tag + ':renamed:' + str(len(tree['nodes'])-i)
                 for i, n in enumerate(tree['nodes'])}
        tree['root'] = names[tree['root']]
        for node in tree['nodes']:
            node['id'] = names[node['id']]
            node['children'] = [names[v] for v in reversed(node['children'])]
        tree['nodes'].reverse()
    return out


def dataset():
    for n in range(1, 5):
        family = trees(tuple('abcdefg'[:n]))
        assert len(family) == (1, 1, 3, 15)[n-1]
        for i, a in enumerate(family):
            for j, b in enumerate(family):
                yield f'exhaustive_{n}_{i}_{j}', source(a, b)
    rng = random.Random(SEED)
    for n, count in ((5, 32), (6, 32), (7, 16)):
        family = trees(tuple('abcdefg'[:n]))
        pairs = rng.sample(range(len(family)**2), count)
        for k, code in enumerate(pairs):
            i, j = divmod(code, len(family))
            yield f'seeded_{n}_{k}', source(family[i], family[j])
    legacy = json.loads((WORK/'evidence/prepare-restart/legacy-source-cases.json').read_text())
    for case in legacy:
        yield 'legacy_' + case['name'], case['source']
    yield 'internal_renaming', json.loads((WORK/'evidence/prepare-restart/internal-renaming.json').read_text())
    yield 'ancestor_cycle', source(('a', ('b', ('c', 'd'))), ('c', ('d', ('a', 'b'))))


def generate():
    cases = []
    for name, instance in dataset():
        opt, solutions = reference.solve(instance)
        actual, found = check.solve_source(instance)
        assert (actual, found) == (opt, solutions), name
        cases.append(dict(name=name, source=instance, source_opt_components=opt,
                          source_opt_solution_count=len(solutions)))
        if len(cases) % 25 == 0:
            print(f'ground truth established: {len(cases)}', flush=True)
    text = '{"seed":' + str(SEED) + ',"cases":[\n'
    text += ',\n'.join(json.dumps(c, ensure_ascii=False, separators=(',', ':')) for c in cases)
    (WORK/'cases.json').write_text(text+'\n]}\n')
    print(f'generated: {len(cases)} source instances, all minimum partition sets cross-checked')


def brute_target(target):
    vertices, arcs = target['vertices'], target['arcs']
    # Independent Floyd-Warshall detects cycles, including self-loops.
    for k in range(len(vertices)+1):
        solutions = set()
        for chosen in itertools.combinations(vertices, k):
            kept = [v for v in vertices if v not in chosen]
            reach = {(u, v) for u, v in arcs if u in kept and v in kept}
            for mid in kept:
                reach |= {(u, v) for u in kept for v in kept
                          if (u, mid) in reach and (mid, v) in reach}
            if not any((v, v) in reach for v in kept):
                solutions.add(tuple(chosen))
        if solutions:
            return k, solutions
    raise AssertionError('deleting all vertices must work')


def self_test():
    cases = json.loads((WORK/'cases.json').read_text())['cases']
    partition_count = optima = 0
    for i, case in enumerate(cases, 1):
        instance = case['source']
        valid = reference.forests(instance)
        optimum = min(map(len, valid))
        expected = {p for p in valid if len(p) == optimum}
        actual, found = check.solve_source(instance)
        assert actual == optimum == case['source_opt_components'], case['name']
        assert found == expected and len(found) == case['source_opt_solution_count'], case['name']
        labels, ts, data = check.block_data(instance)
        for partition in reference.partitions(labels):
            partition_count += 1
            assert check.feasible_partition(partition, labels, ts, data) == (
                tuple(sorted(partition)) in valid), (case['name'], partition)
        for partition in found:
            output = dict(problem='maaforest', components=[list(b) for b in partition], num_components=optimum)
            assert check.validate_source_output(instance, output, optimum)
            assert check.validate_source_output(renamed(instance), output, optimum)
        optima += len(found)
        singles = dict(problem='maaforest', components=[[x] for x in labels], num_components=len(labels))
        assert check.validate_source_output(instance, singles)
        assert check.validate_source_output(instance, singles, optimum) == (len(labels) == optimum)
        for output in (None, {}, {'problem':'maaforest','components':[],'num_components':0},
                       dict(problem='maaforest', components=[[labels[0]]], num_components=1),
                       dict(problem='maaforest', components=[list(labels)], num_components=True)):
            assert not check.validate_source_output(instance, output, optimum)
        if i % 25 == 0:
            print(f'source checked: {i}/{len(cases)}', flush=True)
    by_name = {c['name']: c for c in cases}
    assert by_name['internal_renaming']['source_opt_components'] == 1
    assert by_name['legacy_one_leaf']['source_opt_components'] == 1
    assert by_name['legacy_rSPR1_3']['source_opt_components'] == 2
    assert by_name['legacy_rSPR1_3']['source_opt_solution_count'] == 3
    cycle = next(c['source'] for c in cases if c['name'] == 'ancestor_cycle')
    cyclic = dict(problem='maaforest', components=[['a','b'],['c','d'],['ρ']], num_components=3)
    assert tuple(sorted(map(tuple, cyclic['components']))) in reference.forests(cycle, False)
    assert not check.validate_source_output(cycle, cyclic)
    graphs = 0
    target_outputs = 0
    for n in range(4):
        vertices = [str(i) for i in range(n)]
        edges = list(itertools.product(vertices, repeat=2))
        for mask in range(1 << len(edges)):
            target = dict(problem='dfvs', vertices=vertices,
                          arcs=[list(e) for i,e in enumerate(edges) if mask >> i & 1])
            opt, sets = brute_target(target)
            actual, found, complete = check.solve_target(target)
            assert (actual, found, complete) == (opt, sets, True), target
            graphs += 1
            target_outputs += len(found)
    rng = random.Random(SEED)
    for n in range(4, 9):
        vertices = [str(i) for i in range(n)]
        for _ in range(20):
            target = dict(problem='dfvs', vertices=vertices,
                          arcs=[[u,v] for u in vertices for v in vertices if rng.random() < .25])
            opt, sets = brute_target(target)
            actual, found, complete = check.solve_target(target)
            assert (actual, found, complete) == (opt, sets, True), target
            graphs += 1
            target_outputs += len(found)
    assert check.solve_target(dict(problem='dfvs',vertices=['a','b'],arcs=[['a','b'],['b','a']]), 1)[2] is False
    assert not check.valid_dfvs(['a'], [('a','a')], [])
    assert not check.valid_dfvs(['a'], [], ['a','a'])
    assert not check.valid_dfvs(['a'], [], ['unknown'])
    malformed = deepcopy(cases[0]['source'])
    malformed['t1']['nodes'][0]['children'] = ['missing', 'missing2']
    try:
        check.parse_source(malformed)
    except ValueError:
        pass
    else:
        raise AssertionError('malformed tree accepted')
    # Run the real F/target-oracle/G harness on controlled correct and faulty maps.
    fixture = by_name['legacy_one_leaf']
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        fake = folder/'candidate.py'
        program = """import json,sys
value=json.load(sys.stdin)
if '--extract' not in sys.argv:
 print(json.dumps(dict(problem='dfvs',vertices=['u','v'],arcs=[['u','v'],['v','u']])))
else:
 s=value['source']; blocks=[s['labels']+[s['root_label']]]
 if BAD and value['target_solution']['feedback_vertex_set']==['v']:
  blocks=[[x] for x in s['labels']+[s['root_label']]]
 print(json.dumps(dict(problem='maaforest',components=blocks,num_components=len(blocks))))
"""
        fake.write_text(program.replace('BAD', 'False'))
        check.check_candidate(fake, [fixture], folder)
        fake.write_text(program.replace('BAD', 'True'))
        try:
            check.check_candidate(fake, [fixture], folder)
        except AssertionError as error:
            assert 'invalid/suboptimal recovery' in str(error)
            assert (folder/'recovery-failure.json').exists()
        else:
            raise AssertionError('bad recovery on alternate optimum was accepted')
        for text in ('raise RuntimeError("deliberate failure")', 'print("not JSON")'):
            fake.write_text(text)
            try:
                check.run_map(fake, fixture['source'])
            except (RuntimeError, ValueError):
                pass
            else:
                raise AssertionError('candidate execution failure accepted')
    print(f'PASS source_instances={len(cases)} partitions={partition_count} '
          f'source_optima={optima} target_instances={graphs} target_optima={target_outputs}; '
          'all optima enumerated; rename, cycle, suboptimal and malformed checks passed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true', required=True)
    parser.parse_args()
    generate()
