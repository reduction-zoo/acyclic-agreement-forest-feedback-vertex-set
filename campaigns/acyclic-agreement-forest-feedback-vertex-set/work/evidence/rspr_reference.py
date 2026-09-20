"""Scratch reference: exact rSPR distance and agreement-forest sizes.

A tree is either a label (str) or a frozenset of exactly two children.
This is a throwaway cross-check for the oracle; the reusable oracle lives in
check.py.
"""
from itertools import combinations
import sys


def leaf_of_label(labels):
    return {l: l for l in labels}


def canon(t):
    if isinstance(t, str):
        return t
    return "(" + ",".join(sorted(canon(c) for c in t)) + ")"


def all_nodes(t):
    if isinstance(t, str):
        return [t]
    out = [t]
    for c in t:
        out += all_nodes(c)
    return out


def all_edges(t):
    if isinstance(t, str):
        return []
    out = []
    for c in t:
        out.append((c, t))
        out += all_edges(c)
    return out


def replace(t, target, new):
    if t is target:
        return new
    if isinstance(t, str):
        return t
    return frozenset(replace(c, target, new) for c in t)


def spr_neighbours(t):
    out = set()
    for (u, p) in all_edges(t):
        if not isinstance(p, frozenset) or len(p) != 2:
            continue
        rest = [x for x in p if x is not u][0]
        t2 = replace(t, p, rest)
        # regraft u under a fresh parent placed on any edge of t2
        for (v, q) in all_edges(t2):
            if not isinstance(q, frozenset) or len(q) != 2:
                continue
            new_parent = frozenset([v, u])
            t3 = replace(t2, q, frozenset([x for x in q if x is not v] + [new_parent]))
            if canon(t3).count("(") >= 1:
                out.add(canon(t3))
    return out


def rsp_distance(a, b, max_depth=5):
    """BFS over tree objects; canonical strings are only used as keys."""
    ka, kb = canon(a), canon(b)
    if ka == kb:
        return 0
    seen = {ka}
    frontier = [a]
    for d in range(1, max_depth + 1):
        nxt = []
        for t in frontier:
            for k2 in spr_neighbours(t):
                if k2 in seen:
                    continue
                seen.add(k2)
                if k2 == kb:
                    return d
                nxt.append(parse(k2))
        frontier = nxt
        if not frontier:
            return None
    return None


def parse(k):
    if not k.startswith("("):
        return k
    inner = k[1:-1]
    parts, depth, cur = [], 0, ""
    for ch in inner:
        if ch == "(":
            depth += 1
        if ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return frozenset(parse(p) for p in parts)


def T(s):
    if isinstance(s, str):
        return s
    return frozenset([T(s[0]), T(s[1])])


if __name__ == "__main__":
    cases = [
        ("quartet swap", (("a", "b"), ("c", "d")), (("a", "c"), ("b", "d"))),
        ("quartet other", (("a", "b"), ("c", "d")), (("a", "d"), ("b", "c"))),
        ("n3 rSPR1", (("a", "b"), "c"), (("a", "c"), "b")),
        ("identical4", (("a", "b"), ("c", "d")), (("a", "b"), ("c", "d"))),
        ("n5 example", ((("a", "b"), ("c", "d")), "e"), ((("a", "b"), ("d", "e")), "c")),
    ]
    for name, s1, s2 in cases:
        a, b = T(s1), T(s2)
        d = rsp_distance(a, b)
        print(f"{name:16s} rSPR distance = {d}   ({canon(a)} -> {canon(b)})")
