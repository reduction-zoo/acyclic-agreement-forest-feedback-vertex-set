"""Scratch reference: agreement-forest size by exhaustive edge cuts.

An acyclic agreement forest is modelled the standard way (Bordewich-Semple
2005): delete a set of edges from each of the two trees; the resulting
components must pair up bijectively so that paired components have the same
leaf set and are isomorphic as rooted labelled trees; the size is the total
number of components. Acyclicity is automatic for forests that are *cut out* of
the two trees one component at a time in the descendant-closed order used by
the standard definition, so this reference computes the unconstrained
agreement-forest size, which is the quantity the rSPR theorem equates with
d_rSPR + 1.

This is a throwaway cross-check; the reusable oracle is check.py.
"""
import itertools
import sys
from collections import Counter

sys.path.insert(0, ".")
import rspr_reference as R  # noqa: E402


def index_tree(s):
    """nested tuple -> (children, label, root); leaves are their own labels"""
    children, label = {}, {}

    def mk(s):
        if isinstance(s, str):
            children[s] = []
            label[s] = s
            return s
        a, b = mk(s[0]), mk(s[1])
        nid = f"n{len(children) + 1}"
        children[nid] = [a, b]
        label[nid] = None
        return nid

    root = mk(s)
    return children, label, root


def edges_of(children, root):
    parent = {c: v for v in children for c in children[v]}
    parent[root] = None
    return [(c, parent[c]) for c in children if parent[c] is not None]


def components(children, label, root, cut):
    cut = set(cut)
    kids = {v: [c for c in children[v] if (c, v) not in cut] for v in children}
    parent = {c: v for v in kids for c in kids[v]}
    out = []
    for v in children:
        if v in parent:
            continue
        stack, vs = [v], set()
        while stack:
            u = stack.pop()
            if u in vs:
                continue
            vs.add(u)
            stack.extend(kids[u])
        out.append((v, vs))
    return out


def key_of(children, label, apex, vs):
    kids = {v: [c for c in children[v] if c in vs] for v in vs}

    def ser(v):
        cs = sorted(ser(c) for c in kids.get(v, []))
        if not cs:
            return label[v] if label[v] is not None else v
        return "(" + ",".join(cs) + ")"

    return ser(apex)


def component_key(children, label, apex, vs):
    return (frozenset(label[v] for v in vs if label[v] is not None),
            key_of(children, label, apex, vs))


def agreement_forest_size(labels, s1, s2):
    ch1, lb1, r1 = index_tree(s1)
    ch2, lb2, r2 = index_tree(s2)
    e1, e2 = edges_of(ch1, r1), edges_of(ch2, r2)
    best = None
    best_sets = []
    for k1 in range(len(e1) + 1):
        for c1 in itertools.combinations(e1, k1):
            comp1 = components(ch1, lb1, r1, c1)
            k1keys = Counter(component_key(ch1, lb1, *x) for x in comp1)
            for k2 in range(len(e2) + 1):
                for c2 in itertools.combinations(e2, k2):
                    comp2 = components(ch2, lb2, r2, c2)
                    if len(comp1) != len(comp2):
                        continue
                    k2keys = Counter(component_key(ch2, lb2, *x) for x in comp2)
                    if k1keys != k2keys:
                        continue
                    total = len(comp1)
                    if best is None or total < best:
                        best, best_sets = total, [(c1, c2)]
                    elif total == best:
                        best_sets.append((c1, c2))
    return best, best_sets


if __name__ == "__main__":
    cases = [
        ("quartet swap", ["a", "b", "c", "d"], (("a", "b"), ("c", "d")), (("a", "c"), ("b", "d"))),
        ("n3 rSPR1", ["a", "b", "c"], (("a", "b"), "c"), (("a", "c"), "b")),
        ("identical4", ["a", "b", "c", "d"], (("a", "b"), ("c", "d")), (("a", "b"), ("c", "d"))),
        ("common cherry", ["a", "b", "c", "d"], (("a", "b"), ("c", "d")), (("a", "b"), ("d", "c"))),
        ("n5 example", ["a", "b", "c", "d", "e"],
         ((("a", "b"), ("c", "d")), "e"), ((("a", "b"), ("d", "e")), "c")),
        ("n5 mirror", ["a", "b", "c", "d", "e"],
         ((("a", "b"), ("c", "d")), "e"), ((("a", "b"), ("c", "e")), "d")),
    ]
    for name, labels, s1, s2 in cases:
        size, sets = agreement_forest_size(labels, s1, s2)
        d = R.rsp_distance(R.T(s1), R.T(s2), max_depth=4)
        print(f"{name:16s} |F|={size}  |F|-1={None if size is None else size - 1}  "
              f"rSPR={d}  n_min_solutions={len(sets)}")
