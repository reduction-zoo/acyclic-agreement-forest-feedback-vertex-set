"""Exact MAAF -> DFVS construction.

The forward map encodes a forest by assigning every augmented-tree vertex to a
connected component slot.  The CNF is converted to weighted vertex cover by
the standard variable-edge and clause-clique construction, then weights are
expanded into clone groups.  Bidirected edges make the result an unweighted
DFVS instance.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict

ROOT = "\u03c1"


def key_name(key):
    return tuple(key)


def freeze(value):
    if isinstance(value, list):
        return tuple(freeze(item) for item in value)
    return value


class CNF:
    def __init__(self):
        self.vars = []
        self.seen_vars = set()
        self.clauses = []
        self.seen_clauses = set()
        self.aux_counter = 0

    def var(self, key):
        key = key_name(key)
        if key not in self.seen_vars:
            self.seen_vars.add(key)
            self.vars.append(key)
        return key

    def aux(self, prefix):
        self.aux_counter += 1
        return self.var(("aux", prefix, self.aux_counter))

    def clause(self, literals):
        clean = {}
        for var, positive in literals:
            var = self.var(var)
            if var in clean and clean[var] != positive:
                return
            clean[var] = positive
        if not clean:
            raise ValueError("the source encoding produced an empty clause")
        item = tuple(sorted(clean.items(), key=repr))
        if item not in self.seen_clauses:
            self.seen_clauses.add(item)
            self.clauses.append(item)

    def exactly_one(self, keys):
        keys = [self.var(k) for k in keys]
        self.clause([(k, True) for k in keys])
        for i, left in enumerate(keys):
            for right in keys[i + 1:]:
                self.clause([(left, False), (right, False)])


class Tree:
    def __init__(self, obj):
        self.root = obj["root"]
        self.children = {node["id"]: list(node["children"])
                         for node in obj["nodes"]}
        self.label_of = {node["id"]: node.get("label")
                         for node in obj["nodes"]}
        self.virtual_root = f"__above__{self.root}"
        self.children[self.virtual_root] = [ROOT, self.root]
        self.children[ROOT] = []
        self.label_of[self.virtual_root] = None
        self.label_of[ROOT] = ROOT
        self.parent = {self.virtual_root: None}
        for parent, children in self.children.items():
            for child in children:
                self.parent[child] = parent
        self.ids = list(self.children)
        self.edges = [(child, parent) for parent in self.ids
                      for child in self.children[parent]]
        self.depth = {}
        stack = [(self.virtual_root, 0)]
        while stack:
            node, depth = stack.pop()
            self.depth[node] = depth
            stack.extend((child, depth + 1) for child in self.children[node])
        self.leaf_of = {self.label_of[node]: node for node in self.ids
                        if self.label_of[node] is not None}

    def lca(self, left, right):
        ancestors = set()
        while left is not None:
            ancestors.add(left)
            left = self.parent[left]
        while right not in ancestors:
            right = self.parent[right]
        return right

    def rooted_triple(self, labels):
        a, b, c = labels
        pairs = [((a, b), self.lca(self.leaf_of[a], self.leaf_of[b])),
                 ((a, c), self.lca(self.leaf_of[a], self.leaf_of[c])),
                 ((b, c), self.lca(self.leaf_of[b], self.leaf_of[c]))]
        pair, node = max(pairs, key=lambda item: self.depth[item[1]])
        return tuple(sorted(pair))


def parse_source(source):
    if source.get("problem") != "maaforest":
        raise ValueError("expected a maaforest source")
    if source.get("root_label") != ROOT:
        raise ValueError("the campaign uses the fixed root label rho")
    t1 = Tree(source["t1"])
    t2 = Tree(source["t2"])
    labels = sorted(list(source["labels"]) + [ROOT])
    if set(t1.ids) != set(t2.ids):
        raise ValueError("the trees must share node ids")
    return labels, t1, t2


def zvar(tree_index, node, slot):
    return ("z", tree_index, node, slot)


def build_cnf(source):
    labels, t1, t2 = parse_source(source)
    trees = (t1, t2)
    slots = range(len(labels))
    cnf = CNF()
    use = [cnf.var(("use", s)) for s in slots]

    def z(tree_index, node, slot):
        return cnf.var(zvar(tree_index, node, slot))

    # Every tree vertex belongs to exactly one slot.  A slot is used exactly
    # when it contains at least one labelled leaf.
    for tree_index, tree in enumerate(trees):
        for node in tree.ids:
            cnf.exactly_one([z(tree_index, node, s) for s in slots])
            for s in slots:
                cnf.clause([(z(tree_index, node, s), False), (use[s], True)])
    for s in slots:
        cnf.clause([(use[s], False)] +
                   [(z(0, tree.leaf_of[label], s), True)
                    for label in labels])

    # The two trees assign every common label to the same slot.
    for label in labels:
        for s in slots:
            left = z(0, t1.leaf_of[label], s)
            right = z(1, t2.leaf_of[label], s)
            cnf.clause([(left, False), (right, True)])
            cnf.clause([(right, False), (left, True)])

    # A slot's vertices form one connected part in each tree.  `top` marks
    # the unique vertex of that part whose parent is outside the part.
    for tree_index, tree in enumerate(trees):
        tops = {s: [] for s in slots}
        for node in tree.ids:
            parent = tree.parent[node]
            for s in slots:
                top = cnf.var(("top", tree_index, node, s))
                tops[s].append(top)
                cnf.clause([(top, False), (z(tree_index, node, s), True)])
                if parent is None:
                    cnf.clause([(z(tree_index, node, s), False), (top, True)])
                else:
                    parent_z = z(tree_index, parent, s)
                    cnf.clause([(top, False), (parent_z, False)])
                    cnf.clause([(z(tree_index, node, s), False),
                                (parent_z, True), (top, True)])
        for s in slots:
            for i, left in enumerate(tops[s]):
                for right in tops[s][i + 1:]:
                    cnf.clause([(left, False), (right, False)])

    # Agreement of rooted binary component restrictions is characterized by
    # rooted triples.  Only triples assigned to one block need checking.
    for i, first in enumerate(labels):
        for j in range(i + 1, len(labels)):
            second = labels[j]
            for k in range(j + 1, len(labels)):
                triple = (first, second, labels[k])
                if t1.rooted_triple(triple) == t2.rooted_triple(triple):
                    continue
                for s in slots:
                    cnf.clause([(z(0, t1.leaf_of[label], s), False)
                                for label in triple])

    # `keep` is true exactly for a tree edge retained in a rendered
    # component.  The renderer suppresses an unlabelled apex with one child.
    keeps = []
    for tree_index, tree in enumerate(trees):
        for child, parent in tree.edges:
            other = next(x for x in tree.children[parent] if x != child)
            parent_parent = tree.parent[parent]
            for s in slots:
                child_z = z(tree_index, child, s)
                parent_z = z(tree_index, parent, s)
                keep = cnf.var(("keep", tree_index, child, parent, s))
                keeps.append((child, parent, s, keep))
                cnf.clause([(keep, False), (child_z, True)])
                cnf.clause([(keep, False), (parent_z, True)])
                if parent_parent is None:
                    cnf.clause([(keep, False),
                                (z(tree_index, other, s), True)])
                    cnf.clause([(child_z, False), (parent_z, False),
                                (z(tree_index, other, s), False),
                                (keep, True)])
                else:
                    parent_parent_z = z(tree_index, parent_parent, s)
                    cnf.clause([(keep, False), (parent_parent_z, True),
                                (z(tree_index, other, s), True)])
                    cnf.clause([(child_z, False), (parent_z, False),
                                (parent_parent_z, False), (keep, True)])
                    cnf.clause([(child_z, False), (parent_z, False),
                                (z(tree_index, other, s), False),
                                (keep, True)])

    # A strict total order on the common node ids witnesses acyclicity of the
    # union of retained component arcs.
    nodes = sorted(set(t1.ids) | set(t2.ids))
    lt = {}

    def order(left, right):
        key = ("lt", left, right)
        return cnf.var(key)

    for i, left in enumerate(nodes):
        for right in nodes[i + 1:]:
            lr = order(left, right)
            rl = order(right, left)
            cnf.clause([(lr, True), (rl, True)])
            cnf.clause([(lr, False), (rl, False)])
    for left in nodes:
        for middle in nodes:
            if middle == left:
                continue
            for right in nodes:
                if right == left or right == middle:
                    continue
                cnf.clause([(order(left, middle), False),
                            (order(middle, right), False),
                            (order(left, right), True)])
    for child, parent, s, keep in keeps:
        cnf.clause([(keep, False), (order(child, parent), True)])

    return labels, (t1, t2), slots, cnf, use


def group_id(kind, *parts):
    return (kind,) + tuple(parts)


def vertex_id(group, clone):
    return json.dumps(["clone", list(group), clone], separators=(",", ":"))


def make_target(source):
    labels, trees, slots, cnf, use = build_cnf(source)
    base = len(labels) + 1
    use_keys = set(use)
    weights = {}
    groups = {}
    for var in cnf.vars:
        for bit in (False, True):
            weight = base + (1 if var in use_keys and bit else 0)
            group = group_id("x", var, bit)
            groups[var, bit] = group
            weights[group] = weight

    clause_groups = []
    for index, clause in enumerate(cnf.clauses):
        row = []
        for position, (var, positive) in enumerate(clause):
            group = group_id("c", index, position)
            weights[group] = base
            row.append(group)
        clause_groups.append(row)

    cover_edges = set()
    for var in cnf.vars:
        cover_edges.add((groups[var, False], groups[var, True]))
    for index, clause in enumerate(cnf.clauses):
        row = clause_groups[index]
        for i, left in enumerate(row):
            for right in row[i + 1:]:
                cover_edges.add((left, right))
        for position, (var, positive) in enumerate(clause):
            cover_edges.add((row[position], groups[var, positive]))

    vertices = []
    clones = {}
    for group, weight in weights.items():
        clones[group] = [vertex_id(group, i) for i in range(weight)]
        vertices.extend(clones[group])
    arcs = set()
    for left, right in cover_edges:
        for u in clones[left]:
            for v in clones[right]:
                arcs.add((u, v))
                arcs.add((v, u))
    return {"problem": "dfvs", "vertices": vertices,
            "arcs": [list(edge) for edge in sorted(arcs)]}


def decode_target(source, target_solution):
    labels, trees, slots, cnf, use = build_cnf(source)
    chosen = set(target_solution["feedback_vertex_set"])
    selected = defaultdict(set)
    for raw in chosen:
        item = json.loads(raw)
        if item[0] != "clone":
            raise ValueError("unknown target vertex encoding")
        group = freeze(item[1])
        clone = item[2]
        selected[group].add(clone)

    base = len(labels) + 1
    truth = {}
    for var in cnf.vars:
        bits = []
        for bit in (False, True):
            group = group_id("x", var, bit)
            expected = base + (1 if var in set(use) and bit else 0)
            count = len(selected[group])
            if count not in (0, expected):
                raise ValueError("a minimum target set split a clone group")
            if count == expected:
                bits.append(bit)
        if len(bits) != 1:
            raise ValueError("a minimum target set did not choose one variable value")
        truth[var] = bits[0]

    def value(var):
        return truth[var]

    slot_of_label = {}
    for label in labels:
        matches = [s for s in slots if value(zvar(0, trees[0].leaf_of[label], s))]
        if len(matches) != 1:
            raise ValueError("decoded label has no unique component slot")
        slot_of_label[label] = matches[0]

    def slot_of(tree_index, node):
        matches = [s for s in slots
                   if value(zvar(tree_index, node, s))]
        if len(matches) != 1:
            raise ValueError("decoded tree vertex has no unique component slot")
        return matches[0]

    def kept(tree_index, tree, child, parent, slot):
        if slot_of(tree_index, child) != slot or slot_of(tree_index, parent) != slot:
            return False
        if tree.parent[parent] is None:
            return slot_of(tree_index, next(x for x in tree.children[parent]
                                            if x != child)) == slot
        if slot_of(tree_index, tree.parent[parent]) == slot:
            return True
        return slot_of(tree_index, next(x for x in tree.children[parent]
                                        if x != child)) == slot

    components = []
    for s in slots:
        block = sorted(label for label in labels if slot_of_label[label] == s)
        if not block:
            continue
        entry = {"labels": block}
        for tree_index, tree in enumerate(trees):
            part = {node for node in tree.ids if slot_of(tree_index, node) == s}
            arcs = []
            for child, parent in tree.edges:
                if kept(tree_index, tree, child, parent, s):
                    arcs.append([child, parent])
            tag = f"t{tree_index + 1}"
            entry[f"{tag}_vertices"] = sorted(part)
            entry[f"{tag}_edges"] = sorted(arcs)
        components.append(entry)

    cuts = {}
    for tree_index, tree in enumerate(trees):
        cuts[f"t{tree_index + 1}"] = sorted(
            [[child, parent] for child, parent in tree.edges
             if slot_of(tree_index, child) != slot_of(tree_index, parent)])
    return {"problem": "maaforest", "cuts": cuts,
            "components": components, "num_components": len(components)}


def main():
    payload = json.load(sys.stdin)
    if "target_solution" in payload:
        out = decode_target(payload["source"], payload["target_solution"])
    else:
        out = make_target(payload)
    json.dump(out, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
