# KakeR34.CriticSeparability — can C1 and C2 each verify with the other unlanded?

Verdict: yes, separable at the file and score level (tested both ways). Not fully separable in quality: C2 condition (e) is the C1 rule set re-implemented in the C2 counter and applied to real ds4cc pages. Advisory only; no admission or verdict.

Sandbox: /fast/scratch/hyaku/kake-r34/w1/CriticSeparability/ (clone at a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f; TMPDIR set to the sandbox's tmp/). Counters are tracked at a2fe31b and byte-equal to the lane copies: c1_matrix_count.py fc72d855…c51e, c1-matrix.json 246a6a3b…14f7 (equal to the pinned MATRIX_SHA256), c2_source_census.py ee7461b9…f892.

## Findings

1. **Read sets are disjoint.** C1 reads `git show <rev>:scripts/link_preview_audit.py` (c1_matrix_count.py:33,46-49,142), the matrix from the counter's own directory on disk rather than from `<rev>` (:30-31,132, sha-pinned at :32,134), and its own bytes for counterSha256 (:165). C2 reads only `<rev>` blobs: corpus/SOURCES.md, corpus/knowledge/link-preview-metadata.md, corpus/lessons/round-34.md, sources/receipts.json, sources/S067-S070.txt, ds4cc-7fc6aa2f/tree.txt and html.tar.xz (c2_source_census.py:63-69,199-202,224,233), plus its own bytes (:240). No path is in both sets. Only `git rev-parse` on the same `--root` is shared.
2. **Tested in both directions, on four sandbox commits:**
   - a2fe31b2 (base): C1 0/28 (exit 1), C2 0/5 (exit 1).
   - d391d95f (base plus a 28/28 probe tool at scripts/link_preview_audit.py, sha 24b15f31…62b2): C1 28/28 (exit 0, all constant gates rejected), C2 0/5 (exit 1). Landing C1 left C2 unchanged.
   - 4a84b5af (base plus only a link-preview-metadata.md that cites S067-S070 and holds the census line): C1 0/28 (exit 1, "tool absent"), C2 1/5 (exit 1). Census condition (e) passed; every id has b=true and a, c, d false. Landing C2 left C1 unchanged.
   - 2ba77dff (merge of both): C1 28/28 (exit 0), C2 1/5 (exit 1). Each score equals its single-claim score, so neither interacts with the other.
   - Outputs: sandbox out-<counter>-<rev>.json and err-<counter>-<rev>.txt.
3. **C2 condition (e) is C1's semantics measured twice.** I ran the probe tool (28/28 on the frozen matrix) over the retained ds4cc pages, with a manifest using page URL https://ds4cc.com/<path> and a trailing index.html removed (the same base as c2:182). It exited 1 (failed-policy) with 146 findings: og_required_missing for og:image 101, og:title 15, og:type 15, og:url 15; no other reasons.
   - Complements give pages=102, og:title=87, og:type=87, og:image=1, og:url=87, all-four=1. That is identical to the counter's census.derived in verification/c2-at-d08d8de.json.
   - The seventh number, og-url-equals-canonical=87, equals og:url-present minus og_url_not_canonical (0 such findings; every og:url page has a canonical link).
   - The definitions match line for line: the c2 Head parser (c2:127-141, 177, 183-184) against c1-matrix.json "interface" items 4 and 5 (exact property attribute, non-empty content after stripping ASCII whitespace, name= ignored, first canonical wins, urljoin against the page URL, exact comparison).
   - So one quality, "does this HTML carry correct required Open Graph tags", is scored on operability (synthetic cases) and on freshness (real-page counts). The sources part of C2, conditions a-d (4 of 5 points), is independent of C1.
4. **Condition (e) is already saturated by a published receipt.** Commit 4a84b5af passed (e) by copying census.derived from verification/c2-at-d08d8de.json into the entry. That needed no tool, no ds4cc reading and no C1 work. Condition (e) proves transcription, not an independent census. Impacted axis: freshness (premature saturation). Smallest correction: the L1 declares (e) a transcription check, or C2's after-value does not credit (e) as separate learning.
5. **Latent divergences between the C2 counter and the C1 contract.** None occurs on the 102 retained pages.
   - Non-UTF-8 page: C2 decodes with "replace" and counts the page (c2:175). C1 requires page_unreadable and exit 2 (interface item 3). The probe found every retained page valid UTF-8.
   - A first `<link rel=canonical>` with no href: C2 skips it and lets the next canonical link win (c2:137-139). The C1 contract says only "first canonical link wins", and no matrix case pins this.
   - Risk: if the census is later stated from tool output on other pages, either of these could make an honest census fail (e). Smallest correction: one matrix case or interface sentence for each, or a scope note that (e) applies only to the pinned 7fc6aa2f tree.
6. **C1's source citations are verified only through C2.** C1 cites S067 and S068, but its counter checks no source (c1:1-17). Any provenance for C1 rides on C2 conditions a-d for S067 and S068.
   - Supported by retained text: S067.txt offset ~964, "The four required properties for every page are: og:title …"; S068.txt offset ~3944, "multiple og:type values are not possible".
   - Not supported: og_url_not_canonical (comparing against `<link rel=canonical>`) is cited to S067 and S068, but rel=canonical and `<link` occur 0 times in S067, S068, S069 and S070. Those sources only say og:url is "the canonical URL". [INFERENCE] The canonical-link-element rule is a lane design choice, not a quoted source fact.
   - Impacted axes: freshness (provenance) and operability (claim wording). Smallest correction: drop the S067/S068 tag from the canonical rule in the C1 wording, or retain a source that names rel=canonical.
7. **Shared blind spot: Open Graph tags placed in `<body>`.** Neither definition requires the tags to be inside `<head>`, although S067 says "place additional <meta> tags in the <head> of your web page". A synthetic page with all four tags in `<body>` makes the probe tool exit 0 (clean), and the C2 counter counts it the same way. Both claims inherit this, so it cannot appear as a cross-claim disagreement. On the 102 retained pages I found none: four pages have no explicit `<head>` tag, so their tags sit in the implied head, which is not a defect.
8. **Constraint on shared code.** The C1 counter copies only the single tool blob into scratch (c1:146-148) and runs it with cwd set to the case directory. A tool that imports a helper shared with any C2-side script would fail all 28 cases. The claims can only share code by duplication, which keeps them separable but makes finding 5 (drift between two parsers) structural.

## Commands (all run in the sandbox; exit codes observed)
- `git clone -q <lane> clone && git checkout -q a2fe31b…` exit 0. Sandbox-only commits d391d95f, 4a84b5af and 2ba77dff were made on sandbox branches c1only, c2only and both.
- `python3 -B .ufo/waves/round-34/{c1_matrix_count,c2_source_census}.py --root <clone> --revision R` for the four revisions: exit codes as in finding 2.
- `python3 -B probe_tool.py --manifest ds4cc/manifest.json`: exit 1, 146 findings. The synthetic body-placement page: exit 0.

Not verified: S069 and S070 quote checks (no gate lines written); C1 and C2 behaviour at any L1 integration commit; the real executors' tool. probe_tool.py is a sandbox falsifier, not a deliverable. No tools were installed or updated.
