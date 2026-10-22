# KakeR34.ReviewRealInputRun — review of `.ufo/waves/round-34/real_input_run.py` and its receipt

Seat: wave-2 reviewer, leaf. Sandbox: `/fast/scratch/hyaku/kake-r34/w2/ReviewRealInputRun/`
(clone at 24a1647; mutant commits live only there). Lane files touched: this report only.
No tools installed (builtin python3/git sufficed).

## Reproduction (assignment command)
- `python3 -B .ufo/waves/round-34/real_input_run.py --root <clone> --revision 5613071e0107544d825e37db1e98f0bfcfb61465 --census <clone>/.ufo/waves/round-34/verification/c2-at-d08d8de.json` → EXIT=0, `agrees: true`, toolExit 1, verdict failed-policy, pagesChecked 102, observed {og:image 101, og:title 15, og:type 15, og:url 15} == expectedFromCensus == landed receipt `verification/real-input-at-5613071.json`. Only textual delta: landed receipt says `"revision": "5613071e"` (short), mine the full sha I passed.
- Input integrity: tool blob identical at 5613071 and 24a1647 (`git rev-parse` → 93f3a2a7 both); archive `ds4cc-7fc6aa2f/html.tar.xz` byte-identical d08d8de↔5613071 (empty `git diff --stat`); census receipt `c2-at-d08d8de.json` `census.derived` = pages 102, og:title/type/url 87, og:image 1, all-four 1, og-url-equals-canonical 87, `derivedWhy: "ok"`. The receipt reproduces.

## Findings, severity-ranked

**F1 (Medium) — the run cannot reject a tool that drops the og:url-canonical rule; proven.**
Mutant A (sandbox commit `546cf4c0cba666a487052e790e4af879f1682ddc`): deleted the `elif parser.canonical_href is not None:` comparison block from `scripts/link_preview_audit.py`, leaving missing-property, og:type-multiple and og_url_not_absolute rules intact. Re-ran the runner against it:
`python3 -B .ufo/waves/round-34/real_input_run.py --root <clone> --revision 546cf4c0... --census <clone>/.ufo/waves/round-34/verification/c2-at-d08d8de.json` → EXIT=0, `agrees: true`.
Cause: the census covers only presence counts of the four properties plus og-url-equals-canonical. This corpus has og:url 87 = equals-canonical 87, so `expect` gains no `og_url_not_canonical` key; `set(by) == set(expect)` then requires the tool to emit none — which a canonical-blind tool also does. The landed run itself shows zero `og_url_not_canonical`, `og_url_not_absolute` and `og_type_multiple` findings on real input (my corpus run: `other findings: {}`), so the same blindness holds for the absolute-og:url and og:type-multiple rules (argued, not mutated). Consequence: real-input corroboration exercises only the four missing-property rules; the three extra policy rules get their coverage solely from the C1 matrix and the 29-fixture selftest.

**F2 (Medium) — aggregate-only comparison: right counts on wrong pages still agree; proven.**
Mutant B (sandbox commit `cfb8b9ad66e2b5722fa80df4e1d7525aba19303d`): og:title-missing fired on the first 15 pages in manifest order that HAVE og:title and lack og:image — 15 false positives; the 15 pages that truly lack og:title (e.g. `bloat.html`, `exa.html`, `burnerchrome/*`, verified via landed-tool page sets, symdiff og:title vs og:type missing = 0 files) got no og:title finding. Runner → EXIT=0, `agrees: true` (output saved `/fast/scratch/hyaku/kake-r34/w2/ReviewRealInputRun/mutantB.json`). The runner compares only `(reason, property)` counts; it never checks page identity, so per-page errors that cancel in aggregate are invisible. The docstring's "counts per property" discloses the granularity, but the run therefore cannot corroborate page-level correctness.

**F3 (Low) — census input is unbound.** The script reads `--census` from the working tree with no binding to `--revision` and no digest of the census file in its receipt; any JSON with `census.derived` is accepted — exactly the shape wave-1's hollow C2 (`0cce15f0`, "census copied from the published before-receipt") produced. Mitigated here: the pinned invocation reads the tracked `c2-at-d08d8de.json` whose `derived` is a counter recount (`derivedWhy: "ok"`), and my rerun reproduced the receipt. Suggest recording the census receipt's sha256 in the runner output/receipt.

**F4 (Low) — exit contract violated on malformed census and crashing tool.** Docstring: "2 on bad input". Observed: `--census .ufo/waves/round-34/verification/c1-at-5613071.json` (no `census` key) → unhandled `KeyError: 'census'`, EXIT=1, empty stdout (ran twice; second run without pipe to capture the code). A tool emitting non-JSON stdout, or exceeding `timeout=120`, would surface as `json.loads`/`TimeoutExpired` tracebacks the same way, not exit 2. Clean paths are fine: `--revision 1e54c89515b0b1f7c9d7d10e6232d15e43320713` (tool absent) → `{"error": "tool, archive or census missing"}`, EXIT=2. Landed invocation unaffected.

## SCORECARD "Round 34 — measured results" sentence
The sentence (SCORECARD.md ~1259-1268): "The landed tool is not that shape: it parses each page with `html.parser`, passes a 29-fixture selftest …, and over the 102 retained ds4cc pages reports exactly the missing counts the C2 recount implies (`verification/real-input-at-5613071.json`). These three checks were written after the finding and do not count toward C1; they are disclosed corroboration for the non-author read."
Verdict: **holds as written.** "Reports exactly the missing counts the C2 recount implies" is literally true (verified by rerun and mutant contrast) and the sentence claims nothing about the canonical/absolute/multiple rules. LOG.md:1434 ("matched by … the landed tool's real-input run") and the knowledge entry (`corpus/knowledge/link-preview-metadata.md` ~212, "the census above, seen through the tool") are likewise narrow. Residual gap: no landed document discloses F1 — a reader could take the real-input receipt as broader rule-level validation than it is. One disclosure clause (e.g. "the real-input run exercises only the four missing-property rules") would close it. Advisory only.

## Residual risk and verification gaps
- og_url_not_absolute and og_type_multiple blindness argued from corpus evidence (zero real-input findings; census has no counts), not proven by mutants.
- Did not test that a wrong census number flips `agrees` (code path `expect` ← `derived` makes it evident); did not audit `c2_source_census.py` itself (other seats hold that item).
- The receipt records the measured tool revision but no digest of the runner script; `real_input_run.py` first exists at 24a1647, so "at-5613071" names the measured revision — runner identity rests on the tracked bytes, which I exercised.
- `MetadataParser` accepts the FIRST canonical link and first og:url only; corpus never distinguishes alternatives, so that reading is unexercised by real input (covered by C1 matrix cases, not re-verified here).

## Sandbox evidence paths
- Clone with mutants: `/fast/scratch/hyaku/kake-r34/w2/ReviewRealInputRun/clone` (HEAD `cfb8b9ad`, parent `546cf4c0`, base 24a1647).
- `sets.py` (corpus extraction + per-property page sets): `/fast/scratch/hyaku/kake-r34/w2/ReviewRealInputRun/sets.py`; extracted corpus + manifest: `.../site/`; mutant B output: `.../mutantB.json`; TMPDIR `.../tmp` used throughout.
- Commands and exit codes are quoted above; every run executed inside the sandbox with GIT_* env cleared.
