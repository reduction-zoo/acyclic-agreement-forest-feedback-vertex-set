"""Polynomial MAAF -> parallel threshold CNFs -> unweighted bidirected covers.

No solver, randomness, or import from the test oracles is used by either map.
"""
import itertools
import json
import sys


class Tree:
    def __init__(self, raw, labels, rho):
        nodes = {x['id']: x for x in raw['nodes']}
        self.children, self.leaf, self.parent = {}, {}, {}
        def visit(v, parent):
            index = len(self.children)
            self.children[index] = []
            self.parent[index] = parent
            node = nodes[v]
            if node['children']:
                self.children[index] = [visit(c, index) for c in node['children']]
            else:
                self.leaf[index] = labels.index(node['label'])
            return index
        self.children[0], self.parent[0] = [], None
        old = visit(raw['root'], 0)
        extra = len(self.children)
        self.children[extra], self.parent[extra] = [], 0
        self.leaf[extra] = labels.index(rho)
        self.children[0] = [old, extra]
        self.paths = {}
        self.desc = {}
        def walk(v, path):
            self.paths[v] = path + (v,)
            self.desc[v] = ({self.leaf[v]} if v in self.leaf else
                            set().union(*(walk(c, path + (v,)) for c in self.children[v])))
            return self.desc[v]
        walk(0, ())
        self.leaf_nodes = {label: v for v, label in self.leaf.items()}

    def lca(self, block):
        paths = [self.paths[self.leaf_nodes[x]] for x in block]
        return next(v for v in reversed(paths[0]) if all(v in p for p in paths))

    def restriction(self, block):
        root = self.lca(block)
        alive = set()
        for x in block:
            path = self.paths[self.leaf_nodes[x]]
            alive.update(path[path.index(root):])
        def shape(v):
            if v in self.leaf:
                return (0, self.leaf[v])
            parts = [shape(c) for c in self.children[v] if c in alive]
            return parts[0] if len(parts) == 1 else (1, *sorted(parts))
        return root, alive, shape(root)

    def triple(self, triple):
        return max(itertools.combinations(triple, 2),
                   key=lambda pair: len(self.paths[self.lca(pair)]))


def inputs(source):
    labels = sorted(source['labels'] + [source['root_label']])
    return labels, [Tree(source[tag], labels, source['root_label']) for tag in ('t1','t2')]


class CNF:
    def __init__(self):
        self.size = 1
        self.clauses = [(1,)]

    def variable(self):
        self.size += 1
        return self.size

    def add(self, *literals):
        values = set(literals)
        if 1 in values or any(-v in values for v in values):
            return
        values.discard(-1)
        self.clauses.append(tuple(sorted(values)) if values else (-1,))

    def either(self, literals):
        values = set(literals)
        if 1 in values or any(-v in values for v in values):
            return 1
        values.discard(-1)
        if not values:
            return -1
        if len(values) == 1:
            return next(iter(values))
        values = sorted(values)
        output = self.variable()
        for value in values:
            self.add(-value, output)
        self.add(-output, *values)
        return output

    def both(self, literals):
        return -self.either([-v for v in literals])


def formula(source):
    labels, trees = inputs(source)
    m = len(labels)
    cnf = CNF()
    member = {(leaf, slot): cnf.variable() for leaf in range(m) for slot in range(leaf+1)}
    def a(leaf, slot):
        return member.get((leaf, slot), -1)
    for leaf in range(m):
        row = [a(leaf, s) for s in range(leaf+1)]
        cnf.add(*row)
        for x,y in itertools.combinations(row, 2):
            cnf.add(-x,-y)
        for s in range(leaf):
            cnf.add(-a(leaf,s), a(s,s))
    order = {(s,t): cnf.variable() for s in range(m) for t in range(s+1,m)}
    def before(s,t):
        return order[s,t] if s<t else -order[t,s]
    for s,t,u in itertools.combinations(range(m),3):
        cnf.add(-before(s,t), -before(t,u), before(s,u))
        cnf.add(before(s,t), before(t,u), -before(s,u))
    for tree in trees:
        down, outside, occupied, above = {}, {}, {}, {}
        for v in reversed(list(tree.children)):
            for s in range(m):
                down[v,s] = (a(tree.leaf[v],s) if v in tree.leaf else
                             cnf.either(down[c,s] for c in tree.children[v]))
        for v in tree.children:
            for s in range(m):
                parent = tree.parent[v]
                if parent is None:
                    outside[v,s] = above[v,s] = -1
                else:
                    sibling = next(c for c in tree.children[parent] if c != v)
                    outside[v,s] = cnf.either([outside[parent,s],down[sibling,s]])
                    above[v,s] = cnf.either([above[parent,s],occupied[parent,s]])
                if v in tree.leaf:
                    occupied[v,s] = a(tree.leaf[v],s)
                else:
                    left,right = tree.children[v]
                    hits = [down[left,s],down[right,s],outside[v,s]]
                    occupied[v,s] = cnf.either(cnf.both(pair) for pair in itertools.combinations(hits,2))
            for s,t in itertools.combinations(range(m),2):
                cnf.add(-occupied[v,s],-occupied[v,t])
            for s in range(m):
                for t in range(m):
                    if s != t:
                        cnf.add(-above[v,s],-occupied[v,t],before(s,t))
    for triple in itertools.combinations(range(m),3):
        if trees[0].triple(triple) != trees[1].triple(triple):
            for s in range(min(triple)+1):
                cnf.add(*[-a(leaf,s) for leaf in triple])
    # Exact threshold circuit: count[j] iff at least j representatives are used.
    count = [1] + [-1]*m
    for s in range(m):
        count = [1] + [cnf.either([count[j],cnf.both([count[j-1],a(s,s)])])
                       for j in range(1,m+1)]
    return cnf, member, count


def cover_graph(cnf, threshold, prefix):
    clauses = cnf.clauses + ([] if threshold == -1 else [(-threshold,)])
    vertices, edges = [], []
    def endpoint(v, bit):
        return f'{prefix}:v:{v}:{bit}'
    for v in range(1,cnf.size+1):
        x,y = endpoint(v,0), endpoint(v,1)
        vertices.extend([x,y]); edges.append((x,y))
    for i,clause in enumerate(clauses):
        row = [f'{prefix}:c:{i}:{j}' for j in range(len(clause))]
        vertices.extend(row)
        edges.extend(itertools.combinations(row,2))
        for vertex,literal in zip(row,clause):
            edges.append((vertex,endpoint(abs(literal),int(literal>0))))
    return vertices, edges


def forward(source):
    cnf, _, count = formula(source)
    vertices, arcs = [], []
    for k in range(1,len(count)):
        vs,edges = cover_graph(cnf, count[k+1] if k+1<len(count) else -1, str(k))
        vertices.extend(vs)
        for u,v in edges:
            arcs.extend([[u,v],[v,u]])
    return dict(problem='dfvs',vertices=vertices,arcs=arcs)


def valid_partition(blocks, m, trees):
    if sorted(x for b in blocks for x in b) != list(range(m)):
        return False
    subtrees = [[tree.restriction(b) for b in blocks] for tree in trees]
    if any(a[2] != b[2] for a,b in zip(*subtrees)):
        return False
    arcs = set()
    for tree,parts in zip(trees,subtrees):
        seen = set()
        for _,vertices,_ in parts:
            if seen & vertices:
                return False
            seen.update(vertices)
        for i,(root,_,_) in enumerate(parts):
            for j,(other,_,_) in enumerate(parts):
                if i != j and root in tree.paths[other][:-1]:
                    arcs.add((i,j))
    remaining = set(range(len(blocks)))
    while remaining:
        roots = remaining - {v for u,v in arcs if u in remaining and v in remaining}
        if not roots:
            return False
        remaining -= roots
    return True


def extract(source, solution):
    labels, trees = inputs(source)
    m = len(labels)
    chosen = set(solution['feedback_vertex_set'])
    # Membership variables are allocated first in a fixed triangular order.
    member = {(leaf,s):2+leaf*(leaf+1)//2+s for leaf in range(m) for s in range(leaf+1)}
    best = None
    for k in range(1,m+1):
        blocks = [tuple(leaf for leaf in range(s,m)
                        if f'{k}:v:{member[leaf,s]}:1' in chosen) for s in range(m)]
        blocks = [b for b in blocks if b]
        if valid_partition(blocks,m,trees) and (best is None or len(blocks)<len(best)):
            best = blocks
    if best is None:
        raise ValueError('target output decodes to no valid source partition')
    return dict(problem='maaforest',components=[[labels[i] for i in b] for b in best],num_components=len(best))


if __name__ == '__main__':
    value = json.load(sys.stdin)
    if sys.argv[1:] == ['--extract']:
        result = extract(value['source'],value['target_solution'])
    elif not sys.argv[1:]:
        result = forward(value)
    else:
        raise ValueError('expected no option or --extract')
    json.dump(result,sys.stdout,separators=(',',':'),ensure_ascii=False)
    print()
