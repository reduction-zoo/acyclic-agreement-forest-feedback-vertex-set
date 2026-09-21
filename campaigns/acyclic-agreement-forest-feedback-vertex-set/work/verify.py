"""Independent target-side verification for the current candidate.

The target instances produced by the candidate are bidirected clone graphs.
This verifier solves them as generic minimum vertex-cover instances after
grouping nonadjacent vertices with identical neighbourhoods.  It imports only
the standalone source reference oracle, never the candidate or prepared
checker.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict

import z3

from evidence.agreement_forest_reference import Tree, acyclic, agreement_forest_size


ROOT = "\u03c1"


def run_candidate(path, payload, extract=False):
    command = [sys.executable, path]
    if extract:
        command.append("--extract")
    proc = subprocess.run(command, input=json.dumps(payload),
                          capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr[-400:])
    return json.loads(proc.stdout)


def target_solutions(target, cap=16):
    vertices = target["vertices"]
    arcs = {(u, v) for u, v in target["arcs"]}
    if any(u == v or (v, u) not in arcs for u, v in arcs):
        raise ValueError("verification scope expects a simple bidirected target")
    adjacency = {v: set() for v in vertices}
    for u, v in arcs:
        adjacency[u].add(v)
    by_neighbours = defaultdict(list)
    for vertex in vertices:
        by_neighbours[frozenset(adjacency[vertex])].append(vertex)
    groups = list(by_neighbours.values())
    group_of = {vertex: i for i, group in enumerate(groups)
                for vertex in group}
    edges = set()
    for u, v in arcs:
        left, right = group_of[u], group_of[v]
        if left != right:
            edges.add(tuple(sorted((left, right))))
    chosen = [z3.Bool(f"cover_{i}") for i in range(len(groups))]
    constraints = [z3.Or(chosen[left], chosen[right]) for left, right in edges]
    objective = z3.Sum([z3.If(chosen[i], len(group), 0)
                        for i, group in enumerate(groups)])
    optimizer = z3.Optimize()
    optimizer.add(constraints)
    optimizer.minimize(objective)
    if optimizer.check() != z3.sat:
        raise RuntimeError("independent target solver did not find a cover")
    model = optimizer.model()
    optimum = sum(len(groups[i]) for i, variable in enumerate(chosen)
                  if z3.is_true(model.eval(variable, model_completion=True)))

    selected_groups = {i for i, variable in enumerate(chosen)
                       if z3.is_true(model.eval(variable, model_completion=True))}
    first = [vertex for i in selected_groups for vertex in groups[i]]
    if cap == 1:
        return [first], optimum, len(groups)

    solver = z3.Solver()
    solver.add(constraints)
    solver.add(z3.PbEq([(variable, len(groups[i]))
                        for i, variable in enumerate(chosen)], optimum))
    out = []
    while len(out) < cap and solver.check() == z3.sat:
        model = solver.model()
        selected_groups = {i for i, variable in enumerate(chosen)
                           if z3.is_true(model.eval(variable,
                                                    model_completion=True))}
        selected = [vertex for i in selected_groups for vertex in groups[i]]
        out.append(selected)
        solver.add(z3.Or([variable != (i in selected_groups)
                          for i, variable in enumerate(chosen)]))
    return out, optimum, len(groups)


def ref_id(value, tree):
    if value == ROOT:
        return ("label", ROOT)
    above = next(v for v in tree.nodes if v[0] == "above")
    if value == f"__above__{above[1]}":
        return above
    return ("node", value)


def plain_id(value):
    if value[0] == "above":
        return f"__above__{value[1]}"
    return value[1]


def validate_source_output(source, output):
    if output.get("problem") != "maaforest":
        return False, "wrong source problem"
    entries = output.get("components")
    if not isinstance(entries, list) or not entries:
        return False, "missing components"
    labels = set(source["labels"]) | {ROOT}
    blocks = [tuple(sorted(entry.get("labels", []))) for entry in entries]
    if set(x for block in blocks for x in block) != labels:
        return False, "component labels do not cover the source labels"
    if len(set(blocks)) != len(blocks):
        return False, "repeated component label set"
    if output.get("num_components") != len(entries):
        return False, "wrong component count"

    trees = (Tree(source["t1"]), Tree(source["t2"]))
    rendered = []
    for tree_index, tree in enumerate(trees):
        tag = f"t{tree_index + 1}"
        raw_cuts = output.get("cuts", {}).get(tag)
        if not isinstance(raw_cuts, list):
            return False, f"missing {tag} cuts"
        cuts = set()
        for edge in raw_cuts:
            if not isinstance(edge, list) or len(edge) != 2:
                return False, "malformed cut"
            cuts.add((ref_id(edge[0], tree), ref_id(edge[1], tree)))
        if not cuts <= set(tree.edges):
            return False, f"unknown {tag} cut"
        parts = tree.parts(cuts)
        by_block = {}
        for part, kept in parts:
            component = tree.component(part, kept)
            if component is None:
                return False, f"{tag} has a label-free or malformed part"
            block = tuple(sorted(component["labels"]))
            by_block[block] = (part, component)
        if set(by_block) != set(blocks):
            return False, f"{tag} parts do not match component blocks"
        for entry in entries:
            block = tuple(sorted(entry["labels"]))
            part, component = by_block[block]
            actual_vertices = set(entry[f"{tag}_vertices"])
            expected_vertices = {plain_id(v) for v in part}
            if actual_vertices != expected_vertices:
                return False, f"{tag} raw part mismatch for {block}"
            actual_arcs = {tuple(edge) for edge in entry[f"{tag}_edges"]}
            expected_arcs = {(plain_id(u), plain_id(v))
                             for u, v in component["arcs"]}
            if actual_arcs != expected_arcs:
                return False, f"{tag} component arcs mismatch for {block}"
            rendered.append((block, tree_index, component))

    by_block_key = defaultdict(dict)
    union = set()
    for block, tree_index, component in rendered:
        by_block_key[block][tree_index] = component["key"]
        union.update(component["arcs"])
    if any(values[0] != values[1] for values in by_block_key.values()):
        return False, "component restrictions disagree"
    if not acyclic(union):
        return False, "component-ancestry union is cyclic"
    return True, "ok"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--max-leaves", type=int, default=4)
    parser.add_argument("--target-cap", type=int, default=16)
    args = parser.parse_args(argv)
    path = os.path.abspath(args.candidate)
    cases_path = os.path.join(os.path.dirname(__file__), "cases.json")
    with open(cases_path, encoding="utf-8") as stream:
        cases = json.load(stream)["cases"]
    checks = 0
    failures = []
    pending = []
    for case in cases:
        if len(case["source"]["labels"]) > args.max_leaves:
            pending.append(case["name"])
            continue
        source = case["source"]
        target = run_candidate(path, source)
        solutions, target_opt, group_count = target_solutions(target, args.target_cap)
        source_opt, _ = agreement_forest_size(source)
        for selected in solutions:
            checks += 1
            payload = {"source": source,
                       "target_solution": {
                           "problem": "dfvs",
                           "feedback_vertex_set": selected}}
            recovered = run_candidate(path, payload, extract=True)
            valid, why = validate_source_output(source, recovered)
            if not valid or recovered["num_components"] != source_opt:
                failures.append((case["name"], why,
                                 recovered.get("num_components"), source_opt))
        print(f"{case['name']}: target_opt={target_opt} groups={group_count} "
              f"alternate_targets={len(solutions)} source_opt={source_opt}")
    print(f"verification: {checks} target outputs checked, "
          f"{len(failures)} failures, pending={pending}")
    for failure in failures:
        print("FAIL", failure)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
