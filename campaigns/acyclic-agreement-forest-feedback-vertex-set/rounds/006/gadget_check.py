"""Finite graph-oracle and unit-gap checks; no source encoding is reimplemented."""
import itertools
from pathlib import Path
import sys

WORK = Path(__file__).resolve().parents[2] / 'work'
sys.path.insert(0, str(WORK))
import algorithm
import verify

graphs = 0
for n in range(4):
    vertices = [str(i) for i in range(n)]
    pairs = list(itertools.combinations_with_replacement(vertices, 2))
    for mask in range(1 << len(pairs)):
        edges = [e for i, e in enumerate(pairs) if mask >> i & 1]
        graph = dict(problem='dfvs', vertices=vertices,
                     arcs=list({(u, v) for a, b in edges for u, v in ((a, b), (b, a))}))
        for size in range(n + 1):
            expected = {frozenset(s) for s in itertools.combinations(vertices, size)
                        if all(u in s or v in s for u, v in edges)}
            if expected:
                break
        optimum, outputs = verify.target_optima(graph)
        assert optimum == size and {frozenset(s) for s in outputs} == expected
        graphs += 1
print(f'PASS independent CP-SAT oracle: {graphs} bidirected graphs, all optima')

clauses = [(2,), (-2,), (3,), (-3,), (2, 3), (2, -3), (-2, 3), (-2, -3)]
for mask in range(1 << len(clauses)):
    selected = [c for i, c in enumerate(clauses) if mask >> i & 1]
    satisfiable = any(all(any(bits[abs(lit)-2] == (lit > 0) for lit in c)
                         for c in selected) for bits in itertools.product((False, True), repeat=2))
    cnf = algorithm.CNF()
    cnf.size = 4
    cnf.clauses = [c + (4,) for c in [(1,)] + selected] + [(-4,)]
    vertices, edges = algorithm.cover_graph(cnf, 'test')
    graph = dict(problem='dfvs', vertices=vertices,
                 arcs=[e for u, v in edges for e in ((u, v), (v, u))])
    lower = cnf.size + sum(len(c)-1 for c in cnf.clauses)
    optimum, outputs = verify.target_optima(graph, cap=1)
    assert outputs and optimum == lower + (not satisfiable), (mask, optimum, lower)
print('PASS unit-gap cover: all 256 subsets of the eight nonempty two-variable clauses')
