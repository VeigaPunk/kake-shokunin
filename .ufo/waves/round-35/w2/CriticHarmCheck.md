# KakeR35.CriticHarmCheck — attacks the round-35 no-harm claim (16a6b8b8 → 7deacc46), both axes

Verdict: two real changes that the round's own text does not record, both on the freshness or routing side. They come from the C2 entry (`95abec21`), not the C1 tool. Every deletion is explained. No lane gate and none of the 12 earlier counters regresses in its exit code or score.

## Commands (lane: read-only git; everything else in /fast/scratch/hyaku/kake-r35/w2/CriticHarmCheck/{clone,wt-16a6b8b8,wt-7deacc46}, TMPDIR=…/tmp)
- `git diff --numstat|--shortstat|--name-status 16a6b8b8 7deacc46` → exit 0. 273 files, +13909/−22. The only non-additions are 10 modified files. Lines are deleted in exactly 3 files: `corpus/SOURCES.md` 15/1, `scripts/fixtures/link-preview/input_policy_suppressed_on_input/expected.json` 1/1, `scripts/link_preview_audit.py` 58/20. The other 7 modified files (LOG, PROVINCE, SCORECARD, SKILL, QUALITY, README, link_preview_selftest.py) only insert lines. All of those insertions are appended at the end of the file, except SCORECARD:196 (a new capability row) and selftest:99 (opt-in `pagesChecked`/`findingIds` checks that only run when the expected file names them). No file under `.ufo/waves/round-{0..34}` changed. `git diff --quiet b1cbbc39 7deacc46 -- scripts` → identical.
- A Python field-by-field comparison of every SOURCES row at both revisions: 77 → 87 rows, none removed, S078–S087 added. The only changed old row is S006, and only column 10 (used-by) changed, by one appended path. The claim holds.
- 12 existing script blobs are identical at both revisions (canonical_audit, base_path_audit/selftest, citing_set/selftest/hostile_selftest, corpus-contract, freshness-sweep, live_snapshot, receipt_replay, accessibility_packet, probe-delta).

## Harm table (base exit / tip exit; outputs compared with paths and hashes masked)
| Check | Base | Tip | Same? |
|---|---|---|---|
| `canonical_audit.py --selftest` | 0, 82/82 | 0, 82/82 | byte-identical (sha 03072497781f) |
| `base_path_selftest.py` | 0, 45/45 | 0, 45/45 | yes (paths only) |
| `citing_set_selftest.py --root . --tmpdir <sandbox>` | 0 | 0 | yes |
| `citing_set_hostile_selftest.py --root . --tmpdir <sandbox>` | 0, passed | 0, passed | yes |
| `link_preview_selftest.py` | 0, 35/35 | 0, 45/45 | +10 new fixtures, as declared |
| `node corpus-contract.mjs --json --root .` | 0, 0 findings | 0, 0 findings | knowledge 28→29, lessons 29→30 |
| `node freshness-sweep.mjs --json --offline --repo .` | 1 | 1 | only additions: 2 files scanned, cites 1384→1423 |
| **`citing_set.py --revision <rev> --population r26 --ledger r27 --json`** | **1, 4 findings** | **1, 7 findings** | **NO: see finding 1** |
| 11 earlier counters (r29 c1_quote_truth, c2_matrix_count; r30 c2_quote_truth; r31 c2_quote_truth, c2_strict_checks; r32 c2_retained_count; r33 c2_pin_count, c1_code_probe, c1_strict_supplement; r34 c1_matrix_count, c2_source_census) | all 0 | all 0 | identical except r34 c1_matrix `toolSha256` (repaired tool); `C1 28/28` at both |
| r27 `c2_count.py` | 0 | 0 | not diffed field by field |
| r34 `real_input_run.py --census r34 c2-at-9ef758c.json` (offline, retained archive) | 0, agrees | 0, agrees | identical |
| Cross-run: tip tool on base fixtures | — | 1, 34/35 | the only failure is the one changed fixture |
| Cross-run: base tool on tip fixtures | — | 1, 36/45 | the new contract cases fail, as expected |

## Deletions, explained
- SOURCES.md −1: the S006 row rewritten with one used-by path appended (declared, `corpus/lessons/round-35.md:66`).
- Fixture expected.json −1: old expectation `[page_unreadable]` only. New: the page_unreadable finding plus the readable page's 3 `og_required_missing` findings. This is declared contract bullet c, recorded at `SKILL.md:1047-1054` (tip). The stale round-34 row at `SKILL.md:1010` ("Exit 2 reports input findings only") stays as landed, with an appended correction. Intended; not harm.
- Tool −20: docstring sentences rewritten for the new contract, `if input_findings:` at old line 215, and the `handle_startendtag` override removed. The default HTMLParser handler now also calls `handle_endtag` for self-closing tags. The 34 unchanged base fixtures and the r34 matrix (28/28) show no change for `<meta/>`/`<link/>`, and the `svg_self_closing_guard` fixture covers `<svg/>`.

## Finding 1: the citing-set gate gains 3 findings (freshness and operability)
Counterexample: at `16a6b8b8` and `b1cbbc39` the gate reports `unadjudicated_citing_pair` for S003, S005, S007 and S018. From `95abec21` (and at tip) it also reports S001, S002 and S006 in `corpus/knowledge/security-txt-publishing.md`. These are new knowledge-file citations of r26-population rows with no ledger adjudication. Round 34's no-harm rested on "same 4 findings, no new finding" (`.ufo/waves/round-34/w2/CriticHarmCheck.md:38-42`). Nothing in round 35 (SCORECARD round-35 sections, lesson, LOG) mentions it. Evidence: `out/csrev-{16a6b8b8,b1cbbc39,95abec21,7deacc46}.json`.
Is it fixable or a tradeoff? A fixable recording defect. The gate is a "Round27 unadmitted candidate" (`SKILL.md:594`) with a frozen r26 population, so it is not a regression of an admitted measure. Smallest correction: append a note (lesson "Carried open" or SCORECARD) that the gate's finding count went 4 → 7 at `95abec21`, or adjudicate the 3 pairs in a dated ledger addendum.

## Finding 2: the S001 and S002 used-by cells are stale (freshness, false routing)
The entry cites S001 ×6 and S002 ×6 (header line 1, body lines 88-94 and 124). Its own recheck line names an upload-pages-artifact change (S001, S002) as a trigger. Yet neither row's used-by lists the entry. Only S006 was updated, and so was every new mined row. Per `SKILL.md:598` (tip), used-by is the routing information, so a recheck routed from S001 or S002 will miss this entry. Precedent: round 26 repaired stale S024/S025 used-by cells as a defect (`LOG.md:1036-1038`). The wave-1 drafter disclosed the S001/S002 cites (`w1/ScribeEntryDraft.md:41`); the rows seat updated S006 only (`w1/ScribeSourcesRows.md:25`). The claim "no earlier row changed except S006's used-by" is literally true; the harm is the change that was left out. Smallest correction: append `corpus/knowledge/security-txt-publishing.md` to the S001 and S002 used-by cells (append-only, as done for S006) and log it.

## Not verified / limits
- I did not judge the truth of the entry's prose, the counters, or the sealed keys. I did not diff the r27 `c2_count` output field by field.
- Bounds slip: my first no-argument `citing_set_selftest.py` runs used that script's fixed scratch parent under `/fast/scratch/hyaku/kake-r27` (documented at `SKILL.md:616`). The runner removed both temp directories itself (checked with `ls`: absent). I then reran it contained in my sandbox.
- The lane working copy shows an uncommitted `M SKILL.md` and untracked w2 files that are not mine. All my citations are against the tip commit (`git show 7deacc46:SKILL.md`).
- No tools installed or updated. No network requests.
- Sandbox outputs: /fast/scratch/hyaku/kake-r35/w2/CriticHarmCheck/out/ (selftests `wt-*-*.txt`, `cc-*`, `cs-*`, `csrev-*`, `fs-*`, `realinput-*`, `x-*`, `prior/*`).
