# Focused follow-up

**Decision: ADVANCE remains.** At HEAD `5f3a30b`, the paragraph in
`work/proof.md:191–196` correctly accounts for O(m^2) per pair-LCA query,
O(m^4) for pair queries and O(m^5) for triple queries per threshold, and
O(m) thresholds. The overall O(m^6 polylog(m)) bound is unchanged. This
resolves the original review's sole nonblocking accounting finding.

Comparison against reviewed HEAD `83664d0` confirms that this paragraph is
the only proof change and `work/algorithm.py` is unchanged. Correctness,
all-optima recovery, graph bounds, and the limited novelty/significance
judgments are unaffected. Existing evidence is reused; no suite was rerun.
The original `review.md` is preserved as history.

## Reproducible source provenance

The successful shell download during the original review used the following
exact command, from the repository root
`/Users/xiweipan/Codes/reduction-zoo/acyclic-agreement-forest-feedback-vertex-set`:

```sh
curl -L --fail 'https://upcommons.upc.edu/server/api/core/bitstreams/3abb2a26-48f8-4405-951b-d8397d69c7fe/content' -o campaigns/acyclic-agreement-forest-feedback-vertex-set/reviews/rank-threshold/sat-paper.pdf
```

It completed with exit code 0. The web-tool request to that URL had returned
403; the shell download succeeded. Text extraction also completed with exit
code 0, using:

```sh
pdftotext -layout campaigns/acyclic-agreement-forest-feedback-vertex-set/reviews/rank-threshold/sat-paper.pdf campaigns/acyclic-agreement-forest-feedback-vertex-set/reviews/rank-threshold/sat-paper.txt
```

The PDF identifies *Efficiently Calculating Evolutionary Tree Measures Using
SAT*, by Maria Luisa Bonet and Katherine St. John. Sections 3–4, printed
pages 6–8, support the original review's encoding comparison. Publication
year and venue are left unspecified here: neither was verified as publication
metadata in this primary paper copy. Years and venues in its bibliography
do not establish its own publication details. The author-hosted copy read
through the web tool was `https://stjohn.github.io/research/sat6.pdf`; it was
not the URL used to create the local downloaded file.

The local PDF and extracted text can be excluded from Git as reproducible
source copies while retaining these commands and the review citations. This
follow-up neither deletes those files nor changes Git ignore rules. No fresh
download or extraction was needed.

Isolation and route are unchanged: Codex with the supplied GPT-6-based
identity; exact backend identifier is not visible. Filesystem access remains
unrestricted, so confinement to the assigned directory is instruction-based,
not sandbox-enforced. No agents were spawned; only this follow-up was written.
