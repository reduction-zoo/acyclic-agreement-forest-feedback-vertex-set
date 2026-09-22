"""A minimal end-to-end example using both documented subprocess modes."""
import json
from pathlib import Path
import subprocess
import sys

work = Path(__file__).resolve().parents[2] / 'work'
sys.path.insert(0, str(work))
from check import solve_target, validate_source_output

case = next(c for c in json.loads((work/'cases.json').read_text())['cases']
            if c['name'] == 'exhaustive_3_0_1')
command = [sys.executable, str(work/'algorithm.py')]
forward = subprocess.run(command, input=json.dumps(case['source']),
                         text=True, capture_output=True, check=True)
target = json.loads(forward.stdout)
minimum, outputs, complete = solve_target(target, cap=1)
solution = dict(problem='dfvs', feedback_vertex_set=list(next(iter(outputs))))
payload = dict(source=case['source'], target_solution=solution)
backward = subprocess.run(command+['--extract'], input=json.dumps(payload),
                          text=True, capture_output=True, check=True)
forest = json.loads(backward.stdout)
assert validate_source_output(case['source'], forest, case['source_opt_components'])
print(f'PASS {case["name"]}: vertices={len(target["vertices"])} arcs={len(target["arcs"])} '
      f'minimum_dfvs={minimum} recovered_components={forest["num_components"]}')
print('One independently minimum target witness; target enumeration complete:', complete)
print(json.dumps(forest, ensure_ascii=False))
