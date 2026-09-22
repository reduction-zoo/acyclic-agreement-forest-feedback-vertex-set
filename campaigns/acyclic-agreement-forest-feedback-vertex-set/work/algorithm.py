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
        self.children[0], self.parent[0] = [], None
        pending = [(raw['root'], 0)]
        while pending:
            v, parent = pending.pop()
            index = len(self.children)
            self.children[index] = []
            self.parent[index] = parent
            self.children[parent].append(index)
            node = nodes[v]
            if node['children']:
                pending.extend((c, index) for c in reversed(node['children']))
            else:
                self.leaf[index] = labels.index(node['label'])
        extra = len(self.children)
        self.children[extra], self.parent[extra] = [], 0
        self.leaf[extra] = labels.index(rho)
        self.children[0].append(extra)
        self.paths = {0: (0,)}
        for v in self.children:
            if v:
                self.paths[v] = self.paths[self.parent[v]] + (v,)
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
        shapes = {}
        for v in reversed(self.children):
            if v not in alive:
                continue
            if v in self.leaf:
                shapes[v] = f'L{self.leaf[v]};'
            else:
                parts = [shapes[c] for c in self.children[v] if c in alive]
                shapes[v] = parts[0] if len(parts) == 1 else '(' + ''.join(sorted(parts)) + ')'
        return root, alive, shapes[root]

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

    def equivalent(self, a, b):
        if a == b: return 1
        if a == -b: return -1
        if abs(a) == 1: return b if a == 1 else -b
        if abs(b) == 1: return a if b == 1 else -a
        q = self.variable()
        self.add(-a,-b,q); self.add(a,b,q)
        self.add(-a,b,-q); self.add(a,-b,-q)
        return q

    def majority(self, values):
        a,b,c = values
        if a == b or a == c: return a
        if b == c: return b
        if a == -b: return c
        if a == -c: return b
        if b == -c: return a
        if 1 in values: return self.either(x for x in values if x != 1)
        if -1 in values: return self.both(x for x in values if x != -1)
        q = self.variable()
        for x,y in itertools.combinations(values,2):
            self.add(-x,-y,q); self.add(x,y,-q)
        return q


def formula(source, k):
    labels, trees = inputs(source)
    m, width = len(labels), (k-1).bit_length()
    cnf = CNF()
    ranks = [[cnf.variable() for _ in range(width)] for _ in range(m)]
    # Bit vectors use most-significant bit first.
    def equal(x,y):
        return cnf.both(cnf.equivalent(a,b) for a,b in zip(x,y))
    def leq(x,y):
        lower = 1
        for a,b in reversed(list(zip(x,y))):
            lower = cnf.majority([-a,b,lower])
        return lower
    limit = [1 if (k-1) >> bit & 1 else -1 for bit in reversed(range(width))]
    for rank in ranks:
        cnf.add(leq(rank,limit))
    same = {(a,b):equal(ranks[a],ranks[b]) for a,b in itertools.combinations(range(m),2)}
    for tree in trees:
        values = {v:(ranks[tree.leaf[v]] if v in tree.leaf else
                     [cnf.variable() for _ in range(width)]) for v in tree.children}
        for v in tree.children:
            for child in tree.children[v]:
                cnf.add(leq(values[v],values[child]))
        # One comparison per (ancestor, leaf) is shared across leaf pairs.
        agreements = {}
        for a,b in itertools.combinations(range(m),2):
            root = tree.lca((a,b))
            if (root,a) not in agreements:
                agreements[root,a] = leq(ranks[a],values[root])
            cnf.add(-same[a,b],agreements[root,a])
    for a,b,c in itertools.combinations(range(m),3):
        if trees[0].triple((a,b,c)) != trees[1].triple((a,b,c)):
            cnf.add(-same[a,b],-same[a,c])
    return cnf, ranks


def cover_graph(cnf, prefix):
    clauses = cnf.clauses
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
    labels, trees = inputs(source)
    whole = tuple(range(len(labels)))
    if trees[0].restriction(whole)[2] == trees[1].restriction(whole)[2]:
        return dict(problem='dfvs',vertices=[],arcs=[])
    blocks = [(leaf,) for leaf in whole]
    while True:
        for a,b in itertools.combinations(range(len(blocks)),2):
            merged = tuple(sorted(blocks[a]+blocks[b]))
            proposal = [block for i,block in enumerate(blocks) if i not in (a,b)] + [merged]
            proposal.sort()
            if valid_partition(proposal,len(labels),trees):
                blocks = proposal
                break
        else:
            break
    upper = len(blocks)
    vertices, arcs = [], []
    for k in range(2,upper+1):
        cnf, _ = formula(source,k)
        if k < upper:
            selector = cnf.variable()
            cnf.clauses = [clause+(selector,) for clause in cnf.clauses] + [(-selector,)]
        vs,edges = cover_graph(cnf,str(k))
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
    whole = tuple(range(m))
    if trees[0].restriction(whole)[2] == trees[1].restriction(whole)[2]:
        return dict(problem='maaforest',components=[labels],num_components=1)
    chosen = set(solution['feedback_vertex_set'])
    best = None
    for k in range(2,m):
        width = (k-1).bit_length()
        groups = {}
        for leaf in range(m):
            rank = 0
            for bit in range(width):
                variable = 2 + leaf*width + bit
                rank = 2*rank + (f'{k}:v:{variable}:1' in chosen)
            groups.setdefault(rank,[]).append(leaf)
        blocks = list(groups.values())
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
