"""Rank-encoding diagnostic. No result here substitutes for target verification."""
import importlib.util
import json
from pathlib import Path
import sys
import z3
WORK=Path(__file__).resolve().parents[2]/'work';sys.path.insert(0,str(WORK))
import source_reference
spec=importlib.util.spec_from_file_location('candidate',WORK/'algorithm.py')
candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
cases=json.loads((WORK/'cases.json').read_text())['cases']
thresholds=assignments=0
sizes=[]
for index,case in enumerate(cases,1):
    labels=sorted(case['source']['labels']+[case['source']['root_label']])
    valid=source_reference.forests(case['source'])
    vertices=arcs=0
    for k in range(1,len(labels)+1):
        cnf,ranks=candidate.formula(case['source'],k)
        variables={i:z3.Bool(f'q{i}') for i in range(1,cnf.size+1)}
        lit=lambda x:variables[x] if x>0 else z3.Not(variables[-x])
        solver=z3.Solver();solver.add([z3.Or([lit(x) for x in clause]) for clause in cnf.clauses])
        result=solver.check();thresholds+=1
        assert result in (z3.sat,z3.unsat)
        assert (result==z3.sat)==(k>=case['source_opt_components']),(case['name'],k,result)
        if k==case['source_opt_components']:
            for _ in range(4):
                result=solver.check()
                if result==z3.unsat:break
                assert result==z3.sat
                model=solver.model();groups={};assignment=[]
                for leaf,bits in enumerate(ranks):
                    rank=0
                    for bit in bits:
                        value=z3.is_true(model.eval(variables[bit],model_completion=True))
                        rank=2*rank+value;assignment.append(variables[bit]!=value)
                    groups.setdefault(rank,[]).append(labels[leaf])
                blocks=tuple(sorted(tuple(b) for b in groups.values()))
                assert blocks in valid and len(blocks)==k,(case['name'],blocks)
                solver.add(z3.Or(assignment));assignments+=1
        vs,es=candidate.cover_graph(cnf,str(k));vertices+=len(vs);arcs+=2*len(es)
    sizes.append(dict(name=case['name'],leaves=len(labels)-1,vertices=vertices,arcs=arcs))
    if index%25==0:print(f'formulas={index} thresholds={thresholds} decoded={assignments}',flush=True)
print(f'PASS instances={len(cases)} thresholds={thresholds} decoded={assignments}')
Path(__file__).with_name('sizes.json').write_text(json.dumps(sizes,indent=2)+'\n')
