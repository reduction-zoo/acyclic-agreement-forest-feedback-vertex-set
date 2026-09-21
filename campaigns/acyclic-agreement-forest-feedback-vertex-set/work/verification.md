# Independent verification of the current candidate

The tested candidate is commit `81e6d3a`, with forward and extraction maps in
`algorithm.py`. `verify.py` executes the candidate as a subprocess and uses a
separate target solver. Because the candidate's target graph is bidirected, the
solver reduces the actual target instance to minimum vertex cover; it groups
nonadjacent vertices with identical neighbourhoods, assigns each group its
cardinality as weight, and solves that weighted cover instance with Z3. It does
not import `algorithm.py` or `check.py`. The source output validator and source
optimum come from the standalone `agreement_forest_reference.py` implementation.

The finite run

```text
python3 -u verify.py --candidate algorithm.py --max-leaves 3 --target-cap 1
```

checked one independently obtained minimum target output for four cases,
including `rSPR1_3`, and all four recovered forests were valid and globally
minimum. The raw output is retained in
`evidence/verify-small-output.txt`. The run covers one target optimum per case;
the general candidate proof handles all clone-group optimum ties, while full
enumeration of target ties remains outside this verification run.

The follow-up with `--max-leaves 4` completed `identical_4` and was manually
interrupted during the next expanded target optimization. That execution
failure is retained in `evidence/verify-large-interruption.txt`; it does not
establish a mathematical counterexample. The prepared harness's positional
DFVS run has the same baseline-size limitation.
