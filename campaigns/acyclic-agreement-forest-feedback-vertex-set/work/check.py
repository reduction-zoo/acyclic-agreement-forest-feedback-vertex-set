"""Independent test oracles and validators for the fixed campaign question.

Source problem  Pi_A = Maximum Acyclic Agreement Forest (MAAF) on two rooted
binary phylogenetic trees with an additional root label.
Target problem  Pi_B = Minimum Directed Feedback Vertex Set (min-DFVS).

SOURCE MODEL.  The declared root is viewed as a vertex rho adjoined to it by a
pendant edge, and rho belongs to the label set, exactly as in the references:

  * a cut set S of T splits T into connected parts; the components of the forest
    are those parts after deleting unlabelled vertices and suppressing degree-2
    vertices, and a component is rooted at the apex of its part (or at rho when
    it carries the root label);
  * an agreement forest is a pair of cut sets (S1, S2) whose components pair up
    bijectively with identical label sets and isomorphic component trees;
  * its size is the number of components and a maximum agreement forest
    minimises it.

Sources read on 2026-09-21 through the harness:
  * Kelk, Linz, Meuwese, arXiv:2202.09904, Section 2 (definition and the
    identity d_rSPR(T,T') = |F| - 1 of Theorem 2.1);
  * Bordewich, Semple, Annals of Combinatorics 8(4):409-423, 2005.

`evidence/rspr_reference.py` computes the rSPR distance by an independent BFS
over rSPR moves; `evidence/agreement_forest_reference.py` reproduces the source
optima by a second, independent enumeration. The four conditions stated in the
campaign question are checked on every recovered forest by
`validate_source_output`.

Nothing here imports, executes or inspects a candidate reduction or an LLM, and
there is no randomness and no wall-clock, solver or subprocess timeout.

Usage:
    python3 check.py --self-test
    python3 check.py --candidate PATH
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import subprocess
import sys
from collections import defaultdict

ROOT = "\u03c1"
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
CASES_PATH = os.path.join(WORK_DIR, "cases.json")

EXHAUSTIVE_DFVS_VERTEX_CAP = 18
SOURCE_ORACLE_LEAF_CAP = 7
OPTIMAL_DFVS_ENUM_CAP = 128


# ==========================================================================
# Source side
# ==========================================================================


def labels_below(label_of, kids, u):
    out = set()
    stack = [u]
    while stack:
        v = stack.pop()
        lab = label_of.get(v)
        if lab is not None:
            out.add(lab)
        stack.extend(kids.get(v, []))
    return out


class Tree:
    """A rooted binary phylogenetic tree with the root label as a pendant leaf."""

    def __init__(self, ids, children, label_of, declared_root):
        self.declared_ids = list(ids)
        self.declared_root = declared_root
        self.virtual_root = f"__above__{declared_root}"
        children = {k: list(v) for k, v in children.items()}
        label_of = dict(label_of)
        children[self.virtual_root] = [ROOT, declared_root]
        children[ROOT] = []
        label_of[self.virtual_root] = None
        label_of[ROOT] = ROOT
        self.children = children
        self.label_of = label_of
        self.ids = list(children)
        self.parent = {}
        for v, kids in children.items():
            for k in kids:
                self.parent[k] = v
        self.parent[self.virtual_root] = None
        # cuttable edges: every edge of the working tree
        self.edges = [(c, v) for v in self.ids for c in self.children[v]]

    @staticmethod
    def from_json(obj, key):
        if not isinstance(obj, dict):
            raise ValueError(f"{key}: not a JSON object")
        nodes = obj.get("nodes")
        root = obj.get("root")
        if not isinstance(nodes, list):
            raise ValueError(f"{key}.nodes: not a JSON array")
        ids, children, label_of = [], {}, {}
        for node in nodes:
            if not isinstance(node, dict):
                raise ValueError(f"{key}.nodes: element is not an object")
            nid = node.get("id")
            if not isinstance(nid, str) or not nid:
                raise ValueError(f"{key}.nodes: bad id {nid!r}")
            if nid in children:
                raise ValueError(f"{key}: duplicate node id {nid!r}")
            kids = node.get("children")
            if not isinstance(kids, list) or any(not isinstance(k, str) for k in kids):
                raise ValueError(f"{key}.{nid}.children: not a list of ids")
            claim = node.get("label")
            if claim is not None and (not isinstance(claim, str) or not claim):
                raise ValueError(f"{key}.{nid}.label: not a nonempty string or null")
            ids.append(nid)
            children[nid] = list(kids)
            label_of[nid] = claim
        if root not in children:
            raise ValueError(f"{key}.root {root!r} is not a declared node id")
        return Tree(ids, children, label_of, root)

    # -- legality ---------------------------------------------------------

    def legality_problems(self, labels):
        problems = []
        declared_parent = {}
        for v in self.declared_ids:
            kids = self.children[v]
            if not kids:
                if self.label_of[v] is None:
                    problems.append(f"leaf {v!r} carries no label")
                elif self.label_of[v] not in labels:
                    problems.append(f"leaf {v!r} label {self.label_of[v]!r} not in labels")
            elif len(kids) == 2:
                if self.label_of[v] is not None:
                    problems.append(f"internal node {v!r} carries label {self.label_of[v]!r}")
                if kids[0] == kids[1]:
                    problems.append(f"internal node {v!r} repeats a child")
            else:
                problems.append(f"node {v!r} has {len(kids)} children (0 or 2 required)")
            for k in kids:
                if k not in self.children or k == ROOT:
                    problems.append(f"{v!r} has undeclared child {k!r}")
                elif k in declared_parent:
                    problems.append(f"node {k!r} has more than one parent")
                else:
                    declared_parent[k] = v
        for v in self.declared_ids:
            if v != self.declared_root and v not in declared_parent:
                problems.append(f"node {v!r} is not the root but has no parent")
        labels_found = sorted(self.label_of[v] for v in self.declared_ids
                              if not self.children[v])
        if labels_found != sorted(labels):
            problems.append(f"leaf labels {labels_found} != declared labels {sorted(labels)}")
        seen, stack = set(), [self.declared_root]
        while stack:
            v = stack.pop()
            if v in seen:
                problems.append(f"node {v!r} reachable twice from the root")
                continue
            seen.add(v)
            stack.extend(self.children[v])
        if seen != set(self.declared_ids):
            problems.append("some nodes are unreachable from the root")
        return problems

    # -- components -------------------------------------------------------

    def minimal_component_key(self, labels):
        """Canonical tree key for the minimal subtree spanning `labels`."""
        targets = [v for v in self.ids if self.label_of[v] in labels]
        if len(targets) != len(labels):
            return None
        chains = []
        for v in targets:
            chain = []
            while v is not None:
                chain.append(v)
                v = self.parent[v]
            chains.append(chain)
        common = set(chains[0]).intersection(*chains[1:])
        root = max(common, key=lambda v: len(chains[0]) - chains[0].index(v))
        alive = set()
        for chain in chains:
            alive.update(chain[:chain.index(root) + 1])
        kids = {v: [c for c in self.children[v] if c in alive] for v in alive}
        while True:
            victim = next((v for v in alive
                           if self.label_of[v] is None and len(kids[v]) == 1), None)
            if victim is None:
                break
            child = kids[victim][0]
            if victim == root:
                root = child
            else:
                parent = next(p for p in alive if victim in kids[p])
                kids[parent] = [child if c == victim else c for c in kids[parent]]
            alive.remove(victim)
            del kids[victim]

        def ser(v):
            cs = sorted(ser(c) for c in kids[v])
            return self.label_of[v] if not cs else "(" + ",".join(cs) + ")"

        return ser(root)

    def component_of_part(self, part):
        """Render one connected part of a cut as a rooted component tree.

        `part` is a closed set of vertices of T - cut. Unlabelled leaves are
        deleted and non-root vertices with a single child are suppressed; the
        apex of the part is the root of the rendered tree, except that a part
        carrying the label rho is rooted there. A part whose rendered form is not
        a single rooted tree, or which carries no label, is not a component.
        """
        alive = set(part)
        kids = {v: [c for c in self.children[v] if c in alive] for v in alive}
        while True:
            victim = None
            for v in alive:
                if v == ROOT or self.parent[v] in alive:
                    continue
                # the apex of a part is suppressed exactly when it is an
                # unlabelled vertex of degree 2 (one child in the part), which
                # lifts that child; an unlabelled childless apex is deleted. A
                # vertex that is not an apex is never touched.
                if self.label_of[v] is None and len(kids[v]) < 2:
                    victim = v
                    break
            if victim is None:
                break
            if len(kids[victim]) == 1 and self.label_of[kids[victim][0]] is not None:
                child = kids[victim][0]
                for w in alive:
                    if w == victim:
                        continue
                    kids[w] = [child if x == victim else x for x in kids[w] if x != victim]
            else:
                for w in alive:
                    if w == victim:
                        continue
                    kids[w] = [x for x in kids[w] if x != victim]
            alive.discard(victim)
            del kids[victim]
        labels = frozenset(self.label_of[v] for v in alive
                           if self.label_of[v] is not None)
        if not labels:
            return None
        roots = [v for v in alive if self.parent[v] not in alive]
        with_rho = [v for v in roots if ROOT in labels_below(self.label_of, kids, v)]
        if len(with_rho) == 1:
            root = with_rho[0]
        elif len(roots) >= 1:
            root = roots[0]
            with_rho = roots
        else:
            return None
        reach = {root}
        stack = [root]
        while stack:
            u = stack.pop()
            for c in kids.get(u, []):
                reach.add(c)
                stack.append(c)
        if reach != alive:
            return None

        def ser(v):
            cs = sorted(ser(c) for c in kids.get(v, []))
            if not cs:
                return self.label_of[v] if self.label_of[v] is not None else v
            return "(" + ",".join(cs) + ")"

        return {"labels": labels, "root": root,
                "key": self.minimal_component_key(labels),
                "vertices": set(alive),
                "arcs": frozenset((c, v) for v in alive for c in kids[v])}

    def raw_part_of(self, cut, start):
        """Vertices of the part of T - cut containing `start`."""
        cut = set(cut)
        stack, part = [start], set()
        while stack:
            u = stack.pop()
            if u in part:
                continue
            part.add(u)
            for c in self.children[u]:
                if (c, u) not in cut:
                    stack.append(c)
        return part

    def component_vertices(self, block):
        """Vertex set of the component with label set `block`.

        A vertex belongs to the component of a block exactly when every label in
        its subtree lies in that block; the block's own labels always qualify.
        Because the blocks partition the labels, these parts partition the vertex
        set of T -- the disjointness condition, derived rather than assumed.
        """
        members = set(block)
        for x in members:
            if x not in self.children:
                raise ValueError(f"block member {x!r} is not a label of the tree")
        mine = frozenset(members)
        cache = {}

        def below(v):
            if v in cache:
                return cache[v]
            lab = self.label_of.get(v)
            if lab is not None:
                res = frozenset([lab])
            else:
                res = frozenset()
                for c in self.children[v]:
                    res = res | below(c)
            cache[v] = res
            return res

        out = set()
        for v in self.ids:
            if v in members:
                out.add(v)
                continue
            b = below(v)
            if b and b <= mine:
                out.add(v)
        return out

    def cut_components(self, cut):
        """Components of T - cut. Returns None when a component has no label."""
        cut = set(cut)
        kids = {v: [c for c in self.children[v] if (c, v) not in cut] for v in self.ids}
        parent_in = {c: v for v in kids for c in kids[v]}
        comps = []
        for v in self.ids:
            if v in parent_in:
                continue
            stack, part = [v], set()
            while stack:
                u = stack.pop()
                if u in part:
                    continue
                part.add(u)
                stack.extend(kids[u])
            comp = self.component_of_part(part)
            if comp is None:
                return None
            comp["part"] = part
            comps.append(comp)
        return comps

    def cut_partition(self, cut):
        """Raw parts of T - cut, each with its rendered component."""
        cut = set(cut)
        kids = {v: [c for c in self.children[v] if (c, v) not in cut] for v in self.ids}
        parent_in = {c: v for v in kids for c in kids[v]}
        out = []
        for v in self.ids:
            if v in parent_in:
                continue
            stack, part = [v], set()
            while stack:
                u = stack.pop()
                if u in part:
                    continue
                part.add(u)
                stack.extend(kids[u])
            comp = self.component_of_part(part)
            out.append((part, comp))
        if set().union(*[p for p, _c in out]) != set(self.ids):
            raise AssertionError("cutting did not cover every vertex")
        return out


def parse_source(obj):
    if not isinstance(obj, dict):
        raise ValueError("source instance is not a JSON object")
    if obj.get("problem") != "maaforest":
        raise ValueError(f"source.problem is {obj.get('problem')!r}, expected 'maaforest'")
    labels = obj.get("labels")
    if not isinstance(labels, list) or any(not isinstance(x, str) or not x for x in labels):
        raise ValueError("source.labels must be a list of nonempty strings")
    if len(set(labels)) != len(labels):
        raise ValueError("source.labels contains duplicates")
    rl = obj.get("root_label")
    if not isinstance(rl, str) or not rl:
        raise ValueError("source.root_label must be a nonempty string")
    if rl in labels:
        raise ValueError("source.root_label collides with a leaf label")
    if rl != ROOT:
        raise ValueError(f"source.root_label must be the fixed constant {ROOT!r}")
    t1 = Tree.from_json(obj.get("t1"), "t1")
    t2 = Tree.from_json(obj.get("t2"), "t2")
    problems = [f"t1: {p}" for p in t1.legality_problems(labels)]
    problems += [f"t2: {p}" for p in t2.legality_problems(labels)]
    if set(t1.declared_ids) != set(t2.declared_ids):
        problems.append("t1 and t2 must share one node id set (contract section 1.2)")
    if t1.declared_root != t2.declared_root:
        problems.append("t1.root and t2.root must agree (contract section 1.2)")
    if problems:
        raise ValueError("illegal source instance: " + "; ".join(problems))
    return list(labels), t1, t2


def is_acyclic_arc_set(arcs):
    adj = defaultdict(list)
    indeg = defaultdict(int)
    for u, v in arcs:
        adj[u].append(v)
        indeg[v] += 1
        indeg.setdefault(u, 0)
    stack = [v for v in indeg if indeg[v] == 0]
    seen = 0
    while stack:
        u = stack.pop()
        seen += 1
        for w in adj[u]:
            indeg[w] -= 1
            if indeg[w] == 0:
                stack.append(w)
    return seen == len(indeg)


def forest_signature(tree, cut):
    """Sorted tuple of (label set, component key) of a cut."""
    comps = tree.cut_components(cut)
    if comps is None:
        return None
    return tuple(sorted((tuple(sorted(c["labels"])), c["key"]) for c in comps))


def source_oracle(obj, leaf_cap=SOURCE_ORACLE_LEAF_CAP):
    """(opt_size, solutions, status) for the MAAF instance.

    A solution is the pair of cut sets (S1, S2) producing the forest. The search
    family is the set of all cut subsets of both trees; `leaf_cap` enforces the
    finite bound declared in advance.
    """
    labels, t1, t2 = parse_source(obj)
    if len(labels) > leaf_cap:
        return None, [], "pending"
    e1, e2 = list(t1.edges), list(t2.edges)
    by_sig1 = defaultdict(list)
    for k in range(len(e1) + 1):
        for cut in itertools.combinations(e1, k):
            sig = forest_signature(t1, cut)
            if sig is not None:
                by_sig1[sig].append(cut)
    by_sig2 = defaultdict(list)
    for k in range(len(e2) + 1):
        for cut in itertools.combinations(e2, k):
            sig = forest_signature(t2, cut)
            if sig is not None:
                by_sig2[sig].append(cut)
    best, sols = None, []
    for sig, cuts1 in by_sig1.items():
        if sig not in by_sig2:
            continue
        size = len(sig)
        if best is not None and size > best:
            continue
        for c1 in cuts1:
            for c2 in by_sig2[sig]:
                comps1 = t1.cut_components(c1)
                comps2 = t2.cut_components(c2)
                union = set()
                for comp in comps1 + comps2:
                    union |= set(comp["arcs"])
                if not is_acyclic_arc_set(union):
                    continue
                if best is None or size < best:
                    best, sols = size, [(c1, c2)]
                elif size == best:
                    sols.append((c1, c2))
    if best is None:
        return None, [], "pending"
    return best, sols, "ok"


def matched_components(cut1, cut2, t1, t2):
    c1 = t1.cut_components(cut1)
    c2 = t2.cut_components(cut2)
    if c1 is None or c2 is None:
        raise ValueError("a cut set produced a label-free component")
    m2 = {c["labels"]: c for c in c2}
    if set(m2) != {c["labels"] for c in c1}:
        raise ValueError("the two cut sets do not have matching label sets")
    return [(c, m2[c["labels"]])
            for c in sorted(c1, key=lambda c: sorted(c["labels"]))]


def forest_to_output(cut1, cut2, t1, t2):
    """Encode an agreement forest by its two cut sets and its components.

    Each component carries the label set of its cut part and, for each tree, the
    full vertex set of that part together with the arcs induced on it.
    """
    pairs = matched_components(cut1, cut2, t1, t2)
    components = []
    for c1, c2 in pairs:
        entry = {"labels": sorted(c1["labels"])}
        for tag, comp in (("t1", c1), ("t2", c2)):
            entry[f"{tag}_vertices"] = sorted(comp["part"])
            entry[f"{tag}_edges"] = sorted(
                [u, v] for u, v in comp["arcs"])
        components.append(entry)
    return {
        "problem": "maaforest",
        "cuts": {"t1": sorted([u, v] for u, v in cut1),
                 "t2": sorted([u, v] for u, v in cut2)},
        "components": components,
        "num_components": len(components),
    }


def decode_source_output(out):
    if not isinstance(out, dict):
        raise ValueError("source output is not a JSON object")
    if out.get("problem") != "maaforest":
        raise ValueError("source output problem must be 'maaforest'")
    comps = out.get("components")
    if not isinstance(comps, list) or not comps:
        raise ValueError("source output components must be a nonempty list")
    parsed = []
    for comp in comps:
        if not isinstance(comp, dict):
            raise ValueError("component is not an object")
        labels = comp.get("labels")
        if not isinstance(labels, list) or any(not isinstance(x, str) for x in labels):
            raise ValueError("component.labels must be a list of strings")
        entry = {"labels": list(labels)}
        for tag in ("t1", "t2"):
            vs = comp.get(f"{tag}_vertices")
            if not isinstance(vs, list) or any(not isinstance(x, str) for x in vs):
                raise ValueError(f"component.{tag}_vertices must be a list of node ids")
            edges = comp.get(f"{tag}_edges")
            if not isinstance(edges, list):
                raise ValueError(f"component.{tag}_edges must be a list")
            arcs = []
            for e in edges:
                if (not isinstance(e, list) or len(e) != 2
                        or any(not isinstance(x, str) for x in e)):
                    raise ValueError(f"component.{tag}_edges entry is not a pair of node ids")
                arcs.append((e[0], e[1]))
            entry[f"{tag}_vertices"] = list(vs)
            entry[f"{tag}_edges"] = arcs
        parsed.append(entry)
    return parsed


def component_key_of_part(tree, vertices):
    """Canonical component tree of an explicitly given cut part."""
    comp = tree.component_of_part(set(vertices))
    if comp is None:
        return None
    return comp["key"]


def validate_source_output(out, source_obj):
    """Independent validator for a source output.

    Accepted only when it describes a genuine agreement forest of the source
    instance: the components are vertex-disjoint and cover both trees, their
    label sets partition the labels plus the root label, the two component trees
    of each pair are isomorphic, and the union of the two component-ancestry
    relations is acyclic.
    """
    labels, t1, t2 = parse_source(source_obj)
    try:
        parsed = decode_source_output(out)
    except ValueError as exc:
        return False, str(exc)
    if out.get("num_components") != len(parsed):
        return False, "num_components does not equal len(components)"
    flat = [x for e in parsed for x in e["labels"]]
    if sorted(flat) != sorted(set(labels) | {ROOT}):
        return False, "the decoded label sets do not partition labels plus root_label"
    keys = [tuple(sorted(e["labels"])) for e in parsed]
    if len(set(keys)) != len(keys):
        return False, "two components have the same label set"
    for tree, tag in ((t1, "t1"), (t2, "t2")):
        seen = set()
        for entry in parsed:
            block = entry["labels"]
            vs = entry[f"{tag}_vertices"]
            arcs = entry[f"{tag}_edges"]
            if any(v not in tree.ids for v in vs):
                return False, f"component {sorted(block)}: {tag}_vertices has an unknown node"
            if len(set(vs)) != len(vs):
                return False, f"component {sorted(block)}: {tag}_vertices repeats a node"
            vsset = set(vs)
            if seen & vsset:
                return False, f"component {sorted(block)} overlaps another in {tag}"
            seen |= vsset
            rendered = tree.component_of_part(vsset)
            if rendered is None:
                return False, (
                    f"component {sorted(block)}: {tag}_vertices is not a component "
                    f"of T - cut"
                )
            if rendered["labels"] != frozenset(block):
                return False, (
                    f"component {sorted(block)}: the labels of its part in {tag} are "
                    f"{sorted(rendered['labels'])}"
                )
            if set(arcs) != set(rendered["arcs"]):
                return False, (
                    f"component {sorted(block)}: {tag}_edges is not the component "
                    f"tree of its part"
                )
        if seen != set(tree.ids):
            return False, "the components do not cover every vertex of the tree"
    for entry in parsed:
        block = entry["labels"]
        k1 = component_key_of_part(t1, entry["t1_vertices"])
        k2 = component_key_of_part(t2, entry["t2_vertices"])
        if k1 is None or k2 is None:
            return False, f"component {sorted(block)} is not a rooted labelled tree"
        if k1 != k2:
            return False, f"component {sorted(block)} disagrees: {k1} vs {k2}"
    union = set()
    for entry in parsed:
        union |= set(entry["t1_edges"]) | set(entry["t2_edges"])
    if not is_acyclic_arc_set(union):
        return False, "the union of the two component-ancestry relations has a cycle"
    return True, "ok"


# ==========================================================================
# Target side
# ==========================================================================


def parse_target(obj):
    if not isinstance(obj, dict):
        raise ValueError("target instance is not a JSON object")
    if obj.get("problem") != "dfvs":
        raise ValueError(f"target.problem is {obj.get('problem')!r}, expected 'dfvs'")
    vs = obj.get("vertices")
    if not isinstance(vs, list) or any(not isinstance(x, str) or not x for x in vs):
        raise ValueError("target.vertices must be a list of nonempty strings")
    if len(set(vs)) != len(vs):
        raise ValueError("target.vertices contains duplicates")
    arcs_in = obj.get("arcs")
    if not isinstance(arcs_in, list):
        raise ValueError("target.arcs must be a list")
    vset = set(vs)
    arcs = []
    for pair in arcs_in:
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError("target.arcs entry is not a pair")
        u, v = pair
        if u not in vset or v not in vset:
            raise ValueError(f"arc {(u, v)!r} uses an undeclared vertex")
        arcs.append((u, v))
    return list(vs), arcs


def is_valid_dfvs(vertices, arcs, chosen):
    vs = set(vertices)
    chosen = list(chosen)
    if any(v not in vs for v in chosen):
        return False, "the set contains a vertex that is not in the instance"
    if len(set(chosen)) != len(chosen):
        return False, "the set contains a repeated vertex"
    kept = vs - set(chosen)
    remaining = [(u, v) for u, v in arcs if u in kept and v in kept]
    if not is_acyclic_arc_set(remaining):
        return False, "deleting the set leaves a directed cycle"
    return True, "ok"


def _dfvs_exhaustive(vertices, arcs):
    n = len(vertices)
    if n > EXHAUSTIVE_DFVS_VERTEX_CAP:
        return None
    for k in range(0, n + 1):
        for combo in itertools.combinations(vertices, k):
            ok, _ = is_valid_dfvs(vertices, arcs, combo)
            if ok:
                return k
    return None


def _dfvs_smt(vertices, arcs):
    """Z3 decision oracle with a positional acyclicity encoding."""
    import z3

    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    in_s = [z3.Bool(f"s_{i}") for i in range(n)]
    level = [z3.Int(f"l_{i}") for i in range(n)]
    solver = z3.Solver()
    for i in range(n):
        solver.add(level[i] >= 0, level[i] <= n)
    for u, v in arcs:
        i, j = idx[u], idx[v]
        solver.add(z3.Or(in_s[i], level[i] < level[j]))
    for k in range(0, n + 1):
        solver.push()
        solver.add(z3.PbLe([(in_s[i], 1) for i in range(n)], k))
        res = solver.check()
        solver.pop()
        if res == z3.sat:
            return k
        if res == z3.unknown:
            raise RuntimeError("Z3 returned unknown, which is not a decision")
    return n


def _dfvs_solutions_smt(vertices, arcs, k, cap):
    import z3

    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    in_s = [z3.Bool(f"s_{i}") for i in range(n)]
    level = [z3.Int(f"l_{i}") for i in range(n)]
    solver = z3.Solver()
    for i in range(n):
        solver.add(level[i] >= 0, level[i] <= n)
    for u, v in arcs:
        i, j = idx[u], idx[v]
        solver.add(z3.Or(in_s[i], level[i] < level[j]))
    solver.add(z3.PbLe([(in_s[i], 1) for i in range(n)], k))
    found = []
    while len(found) < cap:
        if solver.check() != z3.sat:
            break
        model = solver.model()
        vals = [z3.is_true(model.eval(in_s[i], model_completion=True)) for i in range(n)]
        chosen = tuple(vertices[i] for i in range(n) if vals[i])
        if chosen not in found:
            found.append(chosen)
        solver.add(z3.Or([in_s[i] != vals[i] for i in range(n)]))
    return found


def target_oracle(vertices, arcs):
    if len(vertices) <= EXHAUSTIVE_DFVS_VERTEX_CAP:
        return _dfvs_exhaustive(vertices, arcs), "exhaustive subsets of vertices"
    return _dfvs_smt(vertices, arcs), "z3 positional acyclicity"


def optimal_dfvs_sets(vertices, arcs, opt, cap=OPTIMAL_DFVS_ENUM_CAP):
    out = []
    if len(vertices) <= EXHAUSTIVE_DFVS_VERTEX_CAP:
        for combo in itertools.combinations(vertices, opt):
            ok, _ = is_valid_dfvs(vertices, arcs, combo)
            if ok:
                out.append(tuple(combo))
            if len(out) >= cap:
                break
        return out
    for chosen in _dfvs_solutions_smt(vertices, arcs, opt, cap):
        ok, _ = is_valid_dfvs(vertices, arcs, chosen)
        if ok and len(chosen) == opt and chosen not in out:
            out.append(chosen)
    return out


def parse_target_output(out):
    if not isinstance(out, dict):
        raise ValueError("target output is not a JSON object")
    if out.get("problem") != "dfvs":
        raise ValueError("target output problem must be 'dfvs'")
    s = out.get("feedback_vertex_set")
    if not isinstance(s, list) or any(not isinstance(x, str) for x in s):
        raise ValueError("target output feedback_vertex_set must be a list of strings")
    return list(s)


# ==========================================================================
# Cases, self-test and candidate check
# ==========================================================================


def load_cases(path=None):
    path = path or CASES_PATH
    with open(path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    seen = set()
    for case in doc["cases"]:
        if case["name"] in seen:
            raise ValueError(f"duplicate case name {case['name']!r}")
        seen.add(case["name"])
        parse_source(case["source"])
    return doc


def _run_self_test():
    failures = []
    checks = 0

    def check(name, condition, detail=""):
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(f"{name}: {detail}")

    doc = load_cases()
    by_name = {c["name"]: c for c in doc["cases"]}

    # 1. stored ground truth recomputed by the source oracle
    for case in doc["cases"]:
        stored = case.get("source_opt_components")
        if stored is None:
            print(f"PENDING case {case['name']}: {case.get('pending_reason', 'no ground truth')}")
            continue
        opt, sols, status = source_oracle(case["source"])
        check(f"case {case['name']}: oracle computed", status == "ok", status)
        if status != "ok":
            continue
        check(f"case {case['name']}: optimum matches stored ground truth",
              opt == stored, f"oracle {opt} vs stored {stored}")
        if case.get("source_opt_solution_count") is not None:
            check(f"case {case['name']}: number of optima matches stored ground truth",
                  len(sols) == case["source_opt_solution_count"],
                  f"oracle {len(sols)} vs stored {case['source_opt_solution_count']}")
        _l, t1, t2 = parse_source(case["source"])
        for c1, c2 in sols[:12]:
            out = forest_to_output(c1, c2, t1, t2)
            ok, why = validate_source_output(out, case["source"])
            check(f"case {case['name']}: optimum satisfies the conditions", ok, why)
            blocks = [e["labels"] for e in out["components"]]
            check(f"case {case['name']}: exactly one component carries the root label",
                  sum(1 for b in blocks if ROOT in b) == 1, str(blocks))

    # 2. hand-verified degenerate values
    check("one leaf is one component",
          by_name["one_leaf"].get("source_opt_components") == 1)
    check("two-leaf identical trees are one component",
          by_name["two_leaves_identical"].get("source_opt_components") == 1)
    check("identical four-leaf trees are one component",
          by_name["identical_4"].get("source_opt_components") == 1)

    # 3. round-trip of the source output encoding
    for case in doc["cases"]:
        opt, sols, status = source_oracle(case["source"])
        if status != "ok":
            continue
        _l, t1, t2 = parse_source(case["source"])
        for c1, c2 in sols[:8]:
            out = forest_to_output(c1, c2, t1, t2)
            ok, why = validate_source_output(out, case["source"])
            check(f"case {case['name']}: encoded optimum validates", ok, why)

    # 4. deliberately incorrect source outputs are rejected
    for case in doc["cases"]:
        for bad in case.get("wrong_source_outputs", []):
            ok, why = validate_source_output(bad["output"], case["source"])
            check(f"case {case['name']}: rejects fixture {bad['why']!r}", not ok,
                  f"wrongly accepted: {why}")

    # 5. target validity predicate
    for case in doc["cases"]:
        for good in case.get("target_valid_sets", []):
            vertices, arcs = parse_target(good["instance"])
            ok, why = is_valid_dfvs(vertices, arcs, good["set"])
            check(f"case {case['name']}: accepts valid target set", ok, why)
        for bad in case.get("target_invalid_sets", []):
            vertices, arcs = parse_target(bad["instance"])
            ok, why = is_valid_dfvs(vertices, arcs, bad["set"])
            check(f"case {case['name']}: rejects invalid target set {bad['why']!r}",
                  not ok, f"wrongly accepted: {why}")

    # 6. min-DFVS oracle cross-check on a fixed finite family
    import random as _random
    rng = _random.Random(20260921)
    for trial in range(30):
        n = rng.randint(1, 6)
        vertices = [f"v{i}" for i in range(n)]
        arcs = [(u, v) for u in vertices for v in vertices
                if u != v and rng.random() < 0.35]
        inst = {"problem": "dfvs", "vertices": vertices,
                "arcs": [[u, v] for u, v in arcs]}
        vs, ar = parse_target(inst)
        brute = _dfvs_exhaustive(vs, ar)
        smt = _dfvs_smt(vs, ar)
        check(f"dfvs oracle agreement trial {trial}", brute == smt,
              f"exhaustive {brute} vs smt {smt}")
        sets = optimal_dfvs_sets(vs, ar, brute, cap=8)
        check(f"dfvs oracle returns a minimum set trial {trial}", len(sets) >= 1)
        if sets:
            check(f"dfvs oracle set is minimum trial {trial}", len(sets[0]) == brute,
                  f"{len(sets[0])} vs {brute}")

    print(f"self-test: {checks} checks, {len(failures)} failures")
    for f in failures:
        print("  FAIL", f)
    return len(failures)


def _run_map(path, payload, mode):
    cmd = [sys.executable, path]
    if mode == "extract":
        cmd.append("--extract")
    proc = subprocess.run(cmd, input=json.dumps(payload), capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"candidate {mode} exited with status {proc.returncode}; "
            f"stderr tail: {proc.stderr.strip()[-400:]}"
        )
    return proc.stdout


def _run_candidate(path):
    doc = load_cases()
    failures = []
    checks = 0
    recovered = 0

    def check(name, condition, detail=""):
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(f"{name}: {detail}")

    for case in doc["cases"]:
        name = case["name"]
        source = case["source"]
        opt_a, _sols, status = source_oracle(source)
        check(f"{name}: source oracle available", status == "ok", status)
        if status != "ok":
            continue
        try:
            target = json.loads(_run_map(path, source, "forward"))
        except (RuntimeError, ValueError) as exc:
            check(f"{name}: forward map produces JSON", False, str(exc))
            continue
        try:
            vertices, arcs = parse_target(target)
        except ValueError as exc:
            check(f"{name}: forward output is a legal target instance", False, str(exc))
            continue
        opt_b, how = target_oracle(vertices, arcs)
        check(f"{name}: target oracle decided", opt_b is not None, how)
        if opt_b is None:
            continue
        sets = optimal_dfvs_sets(vertices, arcs, opt_b)
        check(f"{name}: at least one minimum target set", len(sets) >= 1)
        for chosen in sets:
            payload = {"source": source,
                       "target_solution": {"problem": "dfvs",
                                           "feedback_vertex_set": list(chosen)}}
            try:
                out = json.loads(_run_map(path, payload, "extract"))
            except (RuntimeError, ValueError) as exc:
                check(f"{name}: extract runs on {chosen}", False, str(exc))
                continue
            ok, why = validate_source_output(out, source)
            check(f"{name}: recovered forest is valid for {chosen}", ok, why)
            if not ok:
                continue
            check(f"{name}: recovered forest is optimal for {chosen}",
                  out.get("num_components") == opt_a,
                  f"recovered {out.get('num_components')} vs source optimum {opt_a}")
            recovered += 1
    print(f"candidate check: {checks} checks, {len(failures)} failures, "
          f"{recovered} minimum target sets passed through --extract")
    for f in failures:
        print("  FAIL", f)
    return len(failures)


def main(argv=None):
    parser = argparse.ArgumentParser(description="independent oracles for the campaign")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--candidate", metavar="PATH")
    args = parser.parse_args(argv)
    if args.self_test:
        return 1 if _run_self_test() else 0
    if not os.path.exists(args.candidate):
        print(f"candidate {args.candidate!r} does not exist", file=sys.stderr)
        return 2
    return 1 if _run_candidate(args.candidate) else 0


if __name__ == "__main__":
    sys.exit(main())
