"""Exhaustive label partitions and recursive pruning, independent of check.py.

Uses root-to-leaf bit paths rather than the SMT oracle's vertex/LCA encoding.
The caller supplies legal source instances. This module imports no project code.
"""
import itertools


def partitions(items):
    if not items:
        yield ()
        return
    head, *tail = items
    for rest in partitions(tail):
        yield ((head,),) + rest
        for i, block in enumerate(rest):
            yield rest[:i] + ((head,) + block,) + rest[i+1:]


def make_tree(raw, rho):
    nodes = {node['id']: node for node in raw['nodes']}
    def visit(v):
        node = nodes[v]
        if not node['children']:
            return node['label']
        return tuple(visit(c) for c in node['children'])
    return visit(raw['root']), rho


def subtree(tree, block, address=()):
    if isinstance(tree, str):
        return (tree, {address}, address) if tree in block else None
    left = subtree(tree[0], block, address + (0,))
    right = subtree(tree[1], block, address + (1,))
    if left is None:
        return right
    if right is None:
        return left
    shape = tuple(sorted((left[0], right[0]), key=repr))
    vertices = left[1] | right[1] | {address}
    for endpoint in (left[2], right[2]):
        vertices.update(endpoint[:k] for k in range(len(address)+1, len(endpoint)+1))
    return shape, vertices, address


def forests(source, require_acyclic=True):
    labels = tuple(sorted(source['labels'] + [source['root_label']]))
    trees = [make_tree(source[k], source['root_label']) for k in ('t1', 't2')]
    restrictions = {}
    for k in range(1, len(labels)+1):
        for block in itertools.combinations(labels, k):
            pair = [subtree(tree, block) for tree in trees]
            if pair[0][0] == pair[1][0]:
                restrictions[block] = pair
    accepted = set()
    for partition in partitions(labels):
        if any(b not in restrictions for b in partition):
            continue
        if any(restrictions[a][t][1] & restrictions[b][t][1]
               for a, b in itertools.combinations(partition, 2) for t in (0, 1)):
            continue
        n = len(partition)
        reach = [[False]*n for _ in range(n)]
        for i, a in enumerate(partition):
            for j, b in enumerate(partition):
                if i == j:
                    continue
                for t in (0, 1):
                    p, q = restrictions[a][t][2], restrictions[b][t][2]
                    if len(p) < len(q) and q[:len(p)] == p:
                        reach[i][j] = True
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    reach[i][j] |= reach[i][k] and reach[k][j]
        if not require_acyclic or not any(reach[i][i] for i in range(n)):
            accepted.add(tuple(sorted(partition)))
    return accepted


def solve(source):
    valid = forests(source)
    optimum = min(map(len, valid))
    return optimum, {p for p in valid if len(p) == optimum}
