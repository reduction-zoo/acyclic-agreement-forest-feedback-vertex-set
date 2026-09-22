"""Legal flat-JSON trees must not inherit Python's call-stack depth limit."""
import json
from pathlib import Path
import subprocess
import sys

candidate = Path(__file__).resolve().parents[2] / 'work' / 'algorithm.py'
for n in (1, 2, 1200):
    labels = [f'x{i}' for i in range(n)]
    nodes = [dict(id=f'l{i}', children=[], label=labels[i]) for i in range(n)]
    for i in range(n-1):
        nodes.append(dict(id=f'b{i}', children=[f'l{i}',
            f'b{i+1}' if i < n-2 else f'l{n-1}'], label=None))
    root = 'b0' if n > 1 else 'l0'
    other = [dict(id='other:'+v['id'], label=v['label'],
                  children=['other:'+c for c in reversed(v['children'])])
             for v in reversed(nodes)]
    source = dict(problem='maaforest', labels=list(reversed(labels)), root_label='rho',
                  t1=dict(root=root, nodes=nodes), t2=dict(root='other:'+root, nodes=other))
    def run(value, *options):
        result = subprocess.run([sys.executable, str(candidate), *options],
            input=json.dumps(value), text=True, capture_output=True, check=True)
        return json.loads(result.stdout)
    assert run(source) == dict(problem='dfvs', vertices=[], arcs=[])
    recovered = run(dict(source=source,
        target_solution=dict(problem='dfvs', feedback_vertex_set=[])), '--extract')
    assert recovered == dict(problem='maaforest',
        components=[sorted(labels+['rho'])], num_components=1)
    print(f'PASS identical caterpillars: {n} leaves, independent ids and child/node reversal, F and G')
