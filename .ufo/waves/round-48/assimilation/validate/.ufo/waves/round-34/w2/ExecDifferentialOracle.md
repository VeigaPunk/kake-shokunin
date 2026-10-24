# R34 W2 — ExecDifferentialOracle

Axis: operability (landed auditor versus the wave-1 independent lxml implementation).

## Result

Compared the landed source at `24a16474ee73e20453f3e1be9d2f33573c5196d9` with the copied wave-1 oracle. The deterministic corpus was 512 seeded generated pages plus all 102 retained ds4cc HTML pages (614 total). The harness checked the 102 archive paths and Git blob ids against `tree.txt`; all matched. All pages were UTF-8 readable.

Generated coverage included absent, `name=`, empty, ASCII-space/tab/newline/form-feed values, non-empty values, duplicate `og:type`, duplicate `og:url`, relative/absolute/protocol-relative URLs, zero/one/two canonical links, uppercase tags and attributes, entities, self-closing meta tags, and head/body placement. Counts are in the retained result.

Both actual CLI runs returned exit 1 / `failed-policy`, with 614 pages checked. The exit and verdict agreed; the projected reason/property finding multisets did not. Landed emitted 1,725 findings; independent emitted 1,915. Page-level CLI comparison found 171 generated-page disagreements and zero retained ds4cc-page disagreements. No other disagreement class appeared in this seed/corpus.

### Disagreement classes and minimal reproductions

1. **Vertical-tab trimming — 156 pages (11 overlap the multiple-URL class).** Independent treated U+000B as whitespace; landed did not. Of these, 145 had only this cause. Across all pages the net finding delta was independent-only `og_required_missing`: `og:image` 80, `og:title` 84, `og:url` 11; landed-only `og_url_not_absolute` on `og:url` 11. Minimal page URL `https://oracle.example/page/4`; HTML: `<meta property="og:title" content=" \v ">`. The observed CLI page projection is in `differential-results.json:54-67`; minimized HTML and delta are at `2763-2780`.

   **Interface winner: under-specified.** The matrix says “ASCII whitespace” but does not list code points (`c1-matrix.json:10-12`). Under the HTML-defined ASCII-whitespace set (HT, LF, FF, CR, space; not VT), landed is correct. If the contract means the broader ASCII set including VT, independent is correct. Recommend making the set explicit before treating these as definite defects.

2. **Multiple `og:url` values — 26 pages (11 overlap vertical-tab cases; 15 URL-only).** Independent added 26 `og_url_not_canonical` findings. Minimal URL `https://oracle.example/page/5`; HTML: `<meta property="og:url" content="https://oracle.example/page/5"><meta property="og:url" content="https://other.example/second/5"><link rel="alternate canonical" href="https://other.example/canonical/5" />`. Landed reports one mismatch (first URL only); independent reports both. The minimized case and delta are at `differential-results.json:2789-2807`.

   **Interface winner: independent (stronger reading).** The interface says an absolute `og:url` that differs from the canonical href is a finding, and says *first* only for canonical links; it gives no first-`og:url` rule. Landed explicitly selects `og_urls[0]` (`scripts/link_preview_audit.py:207-225`); independent evaluates every collected URL (`wave-1 clone/scripts/link_preview_audit.py:116-120`). If first-URL-only behavior was intended, it must be stated in the interface.

The 171 unique-page total is 145 vertical-tab-only plus 26 multiple-URL pages, with 11 pages in both causes. Result counts: `differential-results.json:2665-2668`; actual CLI aggregate comparison and reason/property deltas: `8-50`. Coverage counts: `2670-2718`. Retained corpus mismatch count: 0.

## Commands and evidence

- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && mkdir -p /fast/scratch/hyaku/kake-r34/w2/ExecDifferentialOracle/tmp /fast/scratch/hyaku/kake-r34/w2/ExecDifferentialOracle/oracles && export TMPDIR=/fast/scratch/hyaku/kake-r34/w2/ExecDifferentialOracle/tmp && git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 24a16474ee73e20453f3e1be9d2f33573c5196d9:scripts/link_preview_audit.py > /fast/scratch/hyaku/kake-r34/w2/ExecDifferentialOracle/oracles/landed.py && cp /fast/scratch/hyaku/kake-r34/w1/ExecIndependentOracle/clone/scripts/link_preview_audit.py /fast/scratch/hyaku/kake-r34/w2/ExecDifferentialOracle/oracles/independent.py` — exit 0.
- `python3 -B -c 'import lxml; print("lxml", lxml.__version__)'` — exit 0, `lxml 6.1.3`; Python `3.14.8`. No packages installed.
- `python3 -B /fast/scratch/hyaku/kake-r34/w2/ExecDifferentialOracle/run_differential.py --seed 34022026 --generated 512` — exit 0; output: 512 generated + 102 retained, 614 total, 171 page disagreements, 156 vertical-tab affected pages, 26 multiple-URL pages, 11 overlaps, 0 retained-page differences. Full retained output: `/fast/scratch/hyaku/kake-r34/w2/ExecDifferentialOracle/differential-results.json`.
- Captured child command `/usr/bin/python3 -B /fast/scratch/hyaku/kake-r34/w2/ExecDifferentialOracle/oracles/landed.py --manifest /fast/scratch/hyaku/kake-r34/w2/ExecDifferentialOracle/runs/readable-corpus/landed/manifest.json` — exit 1, `failed-policy`, 614 pages, 1,725 findings.
- Captured child command `/usr/bin/python3 -B /fast/scratch/hyaku/kake-r34/w2/ExecDifferentialOracle/oracles/independent.py --manifest /fast/scratch/hyaku/kake-r34/w2/ExecDifferentialOracle/runs/readable-corpus/independent/manifest.json` — exit 1, `failed-policy`, 614 pages, 1,915 findings.

SHA-256: landed copy `8dd0018248e04d4e7dd7d901acd846b687a420b559125695b7f2cf5a3c91d875`; independent copy `7a988883cad4d4f040e14bb6cb249eb2ebc15fbc61ccef3a59be512bfa2511ad`; harness `/fast/scratch/hyaku/kake-r34/w2/ExecDifferentialOracle/run_differential.py` `f5d888e8b507017c94cf67c11dec8274f3c00170db4c5936eef046437d0394fa`; results JSON `a3052a19708f5bfdd438e471b1b39584304b896cd048a9ccc59e245cb1acf113`.

No lane implementation files were changed; no network was used. No remaining blocker. Main-owned build/test gates were not run.
