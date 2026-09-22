# Manuscript inspection

Date: 2026-09-22. Native Typst source uses the research-write manuscript and
report assets. The sci-brain technical-writing skill was read before drafting
and again for the final language pass, including its notation/figure rules and
checklist. Definitions, quantifiers, bounds and qualifications match the
independent advance review and focused follow-up. No author or affiliation is
invented. The bibliography retains the unverified year/venue limitation for
the author-hosted SAT manuscript.

From the repository root:

```sh
uv run --locked python campaigns/acyclic-agreement-forest-feedback-vertex-set/work/figures/draw_gadgets.py
typst compile campaigns/acyclic-agreement-forest-feedback-vertex-set/work/manuscript.typ campaigns/acyclic-agreement-forest-feedback-vertex-set/work/manuscript.pdf
pdftoppm -r 120 -png campaigns/acyclic-agreement-forest-feedback-vertex-set/work/manuscript.pdf campaigns/acyclic-agreement-forest-feedback-vertex-set/work/evidence/manuscript/rendered/page
```

Typst 0.15.1 compiled successfully, exit 0, with no diagnostics (`compile.txt`
is empty). The PDF has eight A4 pages. Rendered PNGs and extracted text are
reproducible bulk outputs and are explicitly ignored; the reviewed PDF and
native sources are retained. No random generation or external figure package
is used.

All eight pages were visually inspected. After correcting formula attachment
scope and appendix numbering/page breaks, affected pages 5–8 were recompiled,
rendered and reinspected; pages 1–4 were unchanged. A final reproduction edit selects Python 3.12.11
explicitly instead of attributing Python selection to the dependency lock;
`uv sync --locked --python 3.12.11` exited zero. Page 8 was recompiled,
rendered and reinspected after that edit.

| Page | Checked result |
|---|---|
| 1 | Title, abstract, theorem, references and definition opening legible; no clipping |
| 2 | Rank lemma, both proof directions and binary-width notation legible |
| 3 | Comparator implication, threshold interval and cover baseline correctly scoped |
| 4 | Exact nine-vertex gadget has every stated edge and five selected vertices; curved edge has the correct endpoints; schematic graph boxes explicitly omit internal edges |
| 5 | Recovery proof and bounds legible; the factor d_C times (d_C-1) is visibly multiplication, not part of a subscript |
| 6 | Limitations and primary-source references contained within margins |
| 7 | Appendix headings A.1/A.2, evidence counts and six-column graph-size table fit |
| 8 | Environment and both executable modes fit; source/extraction payload convention and finite limits are stated |

The figure generator asserts all endpoints, edge uniqueness, the displayed
five-vertex cover, and absence of a four-vertex cover by exhaustive subsets.
`figures.txt` records nine vertices, nine undirected edges (18 directed arcs),
baseline four and optimum five. The second figure is labelled schematic.

The final language/notation pass retained all quantifiers, defined symbols at
use, distinguished source and target objectives, checked the measured counts,
and kept campaign operations in the appendix. Figure captions explain their
proof role and all omissions. No mathematical or implementation change was
made in the writing stage. Presentation checks do not provide a formal proof
certificate or extend the bounded literature audit.
