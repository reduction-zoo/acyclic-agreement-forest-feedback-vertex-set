"""Compare both actual forward maps on the same prepared input records."""
import json
from pathlib import Path
import statistics
import subprocess
import sys
import time
import types
WORK=Path(__file__).resolve().parents[2]/'work';ROOT=WORK.parents[2]
sys.path.insert(0,str(WORK));import algorithm
old=types.ModuleType('threshold_baseline')
code=subprocess.run(['git','show','43f36e3:campaigns/acyclic-agreement-forest-feedback-vertex-set/work/algorithm.py'],cwd=ROOT,check=True,capture_output=True,text=True).stdout
exec(compile(code,'baseline.py','exec'),old.__dict__)
values={}
for case in json.loads((WORK/'cases.json').read_text())['cases']:
    n=len(case['source']['labels']); row=[]
    for function in (old.forward,algorithm.forward):
        start=time.perf_counter();graph=function(case['source']);elapsed=time.perf_counter()-start
        row.extend([len(graph['vertices']),len(graph['arcs']),len(json.dumps(graph,separators=(',',':'),ensure_ascii=False).encode()),elapsed])
    values.setdefault(n,[]).append(row)
print('leaves records baseline_vertices_median rank_vertices_median baseline_arcs_median rank_arcs_median rank_vertices_max rank_arcs_max rank_json_bytes_max rank_forward_seconds_median')
for n,rows in sorted(values.items()):
    med=lambda j:statistics.median(row[j] for row in rows)
    print(n,len(rows),med(0),med(4),med(1),med(5),max(r[4] for r in rows),max(r[5] for r in rows),max(r[6] for r in rows),round(med(7),6))
print('Both algorithms build the full explicit graph; timings are single runs, not a calibrated benchmark.')
