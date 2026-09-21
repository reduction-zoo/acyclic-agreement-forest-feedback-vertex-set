"""Independent finite source oracle for the campaign fixtures.

This implementation uses its own augmented-tree representation and derives a
component signature from the minimal subtree spanning a block. It does not
import the reusable checker or the rSPR cross-check.
"""

import itertools
import json
import os
from collections import defaultdict


ROOT = "ρ"


class Tree:
    def __init__(self, obj):
        self.children = {}
        self.label = {}
        self.parent = {}
        nodes = {node["id"]: node for node in obj["nodes"]}
        for nid, node in nodes.items():
            v = ("node", nid)
            self.children[v] = [("node", child) for child in node["children"]]
            self.label[v] = node["label"]
        root = ("node", obj["root"])
        rho = ("label", ROOT)
        above = ("above", obj["root"])
        self.children[rho] = []
        self.label[rho] = ROOT
        self.children[above] = [rho, root]
        self.label[above] = None
        self.nodes = list(self.children)
        for v, children in self.children.items():
            for child in children:
                self.parent[child] = v
        self.parent[above] = None
        self.by_label = {self.label[v]: v for v in self.nodes if self.label[v] is not None}
        self.edges = [(child, v) for v in self.nodes for child in self.children[v]]

    def parts(self, cut):
        cut = set(cut)
        kept = {v: [c for c in self.children[v] if (c, v) not in cut]
                for v in self.nodes}
        child_parent = {c: v for v in kept for c in kept[v]}
        out = []
        for start in self.nodes:
            if start in child_parent:
                continue
            stack, part = [start], set()
            while stack:
                v = stack.pop()
                if v in part:
                    continue
                part.add(v)
                stack.extend(kept[v])
            out.append((part, kept))
        return out

    def component(self, part, kept):
        alive = set(part)
        children = {v: [c for c in kept[v] if c in alive] for v in alive}
        while alive:
            roots = [v for v in alive if self.parent[v] not in alive]
            if not roots:
                return None
            root = roots[0]
            if self.label[root] is None and len(children[root]) < 2:
                alive.remove(root)
                del children[root]
                continue
            break
        if not alive:
            return None
        labels = frozenset(self.label[v] for v in alive if self.label[v] is not None)
        if not labels:
            return None
        roots = [v for v in alive if self.parent[v] not in alive]
        with_root_label = [v for v in roots if self._contains_label(v, ROOT, children)]
        root = with_root_label[0] if len(with_root_label) == 1 else roots[0]
        reached = {root}
        stack = [root]
        while stack:
            v = stack.pop()
            for child in children[v]:
                reached.add(child)
                stack.append(child)
        if reached != alive:
            return None
        arcs = frozenset((child, v) for v in alive for child in children[v])
        return {"labels": labels, "key": self.restriction_key(labels), "arcs": arcs}

    def _contains_label(self, start, wanted, children):
        stack = [start]
        while stack:
            v = stack.pop()
            if self.label[v] == wanted:
                return True
            stack.extend(children[v])
        return False

    def restriction_key(self, labels):
        targets = [self.by_label[label] for label in labels]
        chains = []
        for v in targets:
            chain = []
            while v is not None:
                chain.append(v)
                v = self.parent[v]
            chains.append(chain)
        common = set(chains[0]).intersection(*chains[1:])
        depth = {v: len(chains[0]) - chains[0].index(v) for v in common}
        root = max(common, key=depth.get)
        selected = set()
        for chain in chains:
            selected.update(chain[:chain.index(root) + 1])
        children = {v: [c for c in self.children[v] if c in selected] for v in selected}

        def render(v):
            if self.label[v] is not None:
                return self.label[v]
            rendered = sorted(render(c) for c in children[v])
            if len(rendered) == 1:
                return rendered[0]
            return "(" + ",".join(rendered) + ")"

        return render(root)

    def signature(self, cut):
        components = []
        for part, kept in self.parts(cut):
            component = self.component(part, kept)
            if component is None:
                return None
            components.append(component)
        return tuple(sorted((tuple(sorted(c["labels"])), c["key"]) for c in components))

    def components_for(self, cut):
        components = []
        for part, kept in self.parts(cut):
            component = self.component(part, kept)
            if component is None:
                return None
            components.append(component)
        return components


def acyclic(arcs):
    children = defaultdict(list)
    indegree = defaultdict(int)
    for child, parent in arcs:
        children[child].append(parent)
        indegree[parent] += 1
        indegree.setdefault(child, 0)
    stack = [v for v, degree in indegree.items() if degree == 0]
    seen = 0
    while stack:
        v = stack.pop()
        seen += 1
        for parent in children[v]:
            indegree[parent] -= 1
            if indegree[parent] == 0:
                stack.append(parent)
    return seen == len(indegree)


def agreement_forest_size(source):
    t1, t2 = Tree(source["t1"]), Tree(source["t2"])
    first = defaultdict(list)
    second = defaultdict(list)
    for size in range(len(t1.edges) + 1):
        for cut in itertools.combinations(t1.edges, size):
            signature = t1.signature(cut)
            if signature is not None:
                first[signature].append(cut)
    for size in range(len(t2.edges) + 1):
        for cut in itertools.combinations(t2.edges, size):
            signature = t2.signature(cut)
            if signature is not None:
                second[signature].append(cut)
    best = None
    count = 0
    for signature, cuts1 in first.items():
        for cut1 in cuts1:
            components1 = t1.components_for(cut1)
            for cut2 in second.get(signature, []):
                components2 = t2.components_for(cut2)
                arcs = set()
                for component in components1 + components2:
                    arcs.update(component["arcs"])
                if not acyclic(arcs):
                    continue
                size = len(signature)
                if best is None or size < best:
                    best, count = size, 1
                elif size == best:
                    count += 1
    return best, count


def main():
    path = os.path.join(os.path.dirname(__file__), "..", "cases.json")
    with open(path, encoding="utf-8") as stream:
        cases = json.load(stream)["cases"]
    for case in cases:
        best, count = agreement_forest_size(case["source"])
        print(f"{case['name']:24s} |F|={best}  n_min_cut_pairs={count}")


if __name__ == "__main__":
    main()
