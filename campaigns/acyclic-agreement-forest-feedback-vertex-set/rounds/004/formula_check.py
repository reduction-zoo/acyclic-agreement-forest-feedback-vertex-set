"""Local diagnostic of emitted formulas; not actual-target verification."""
import importlib.util
import json
from pathlib import Path
import sys
import z3

WORK=Path(__file__).resolve().parents[2]/'work'
sys.path.insert(0,str(WORK))
import source_reference
spec=importlib.util.spec_from_file_location('candidate',WORK/'algorithm.py')
candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
cases=json.loads((WORK/'cases.json').read_text())['cases']
thresholds=assignments=0
for index,case in enumerate(cases,1):
    cnf,member,count=candidate.formula(case['source'])
    variables={i:z3.Bool(f'q{i}') for i in range(1,cnf.size+1)}
    lit=lambda x:variables[x] if x>0 else z3.Not(variables[-x])
    solver=z3.Solver()
    solver.add([z3.Or([lit(x) for x in clause]) for clause in cnf.clauses])
    for k in range(1,len(count)):
        solver.push()
        if k+1<len(count):solver.add(z3.Not(lit(count[k+1])))
        result=solver.check();thresholds+=1
        assert result in (z3.sat,z3.unsat)
        assert (result==z3.sat)==(k>=case['source_opt_components']), (case['name'],k,result)
        solver.pop()
    k=case['source_opt_components']
    if k+1<len(count):solver.add(z3.Not(lit(count[k+1])))
    valid=source_reference.forests(case['source'])
    labels=sorted(case['source']['labels']+[case['source']['root_label']])
    for _ in range(4):
        result=solver.check()
        if result==z3.unsat:break
        assert result==z3.sat
        model=solver.model()
        selected=[(leaf,s) for (leaf,s),var in member.items() if z3.is_true(model.eval(variables[var]))]
        blocks=tuple(sorted(tuple(labels[l] for l,s in selected if s==slot)
                            for slot in range(len(labels)) if any(s==slot for l,s in selected)))
        assert blocks in valid and len(blocks)==k,(case['name'],blocks)
        solver.add(z3.Or([z3.Not(variables[member[key]]) for key in selected]))
        assignments+=1
    if index%25==0: print(f'formulas={index} thresholds={thresholds} recovered_partitions={assignments}',flush=True)
print(f'PASS formulas={len(cases)} thresholds={thresholds} recovered_partitions={assignments}')
