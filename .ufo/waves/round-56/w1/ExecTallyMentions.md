# ExecTallyMentions

Mechanical inventory of `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md` (1241 lines, newline-terminated; read from the working tree at base revision e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6). No judgement: counts and lines only.

## COMMAND:

Pattern A — `[0-9]+ (sandbox-repo |generated |matrix |round-[0-9]+ regression )*(fixtures|cases|checks)`:

```
grep -nE '[0-9]+ (sandbox-repo |generated |matrix |round-[0-9]+ regression )*(fixtures|cases|checks)' SKILL.md
```

Pattern B — `[0-9]+/[0-9]+` next to the word selftest, read as same-line co-occurrence:

```
grep -nE '[0-9]+/[0-9]+.*selftest|selftest.*[0-9]+/[0-9]+' SKILL.md
```

Table-row count, `|`-leading lines carrying either selftest token:

```
grep -nE '^[[:space:]]*\|.*(--selftest|_selftest\.py)' SKILL.md
```

Executed as: the `grep` tool with those three patterns against `SKILL.md` (the line numbers below are its output), then one Python pass over the same file (`re` over the split lines) to emit exact first-120-character prefixes, because the grep tool elides long table rows (`... [col N]`). The Python pass re-ran both patterns independently and returned the same line sets. Pattern B was also re-run case-insensitively with `self[- ]?test` (covers "self-test"/"self test") and returned an identical line set, so the strict spelling loses nothing.

## MATCHES:

Pattern A — 20 matching lines. Prefix cut at 120 characters; inside cells every literal `|` is written `\|` so the table does not split; matched text lists every match on the line.

| line | first 120 chars | matched text |
|---|---|---|
| 504 |   (targeted loopback regression, 12 cases). | 12 cases |
| 593 | (`reclassified`). Self-test: 24 cases, fixtures under `TMPDIR`, never the lane. | 24 cases |
| 668 | **unprovable**. C2's exact16/16, real29-case fixtures, Git30 checks and mutant | 30 checks |
| 726 | \| base-path-audit \| gate (offline static project-site base-path policy) \| `python3 -B scripts/base_path_audit.py --manif | 30 matrix fixtures; 15 round-29 regression fixtures |
| 770 | over `scripts/fixtures/citing-set/` (41 cases). A case's `expected.json` lists | 41 cases |
| 1025 | Round-34 additions after wave 1: the committed selftest `python3 -B scripts/link_preview_selftest.py` (29 fixtures under | 29 fixtures |
| 1029 | `ReviewSkillTable34`). The selftest has 35 fixtures at `76fac3b`. The tool | 35 fixtures |
| 1046 | \| link-preview-audit \| gate (offline static Open Graph link-preview policy; no network) \| `python3 -B scripts/link_previ | 20 fixtures |
| 1067 | \| source-recheck-audit \| gate (offline source-quote re-check against recorded fetches; no network) \| `python3 -B scripts | 101 fixtures |
| 1093 | \| robots-expectation-audit \| gate (offline; no network) \| `python3 -B scripts/robots_audit.py --manifest PATH` \| `0=clea | 137 fixtures |
| 1110 | `scripts/robots_audit_selftest.py`, 194 fixtures. Frozen proof: `.ufo/waves/round-38/sealed_count_v3.py` | 194 fixtures |
| 1116 | The robots selftest now has 204 fixtures (round 39, routed defect 3): ten fixtures for the round-38 | 204 fixtures |
| 1128 | \| sitemap-file-audit \| gate (offline; no network) \| `python3 -B scripts/sitemap_audit.py --manifest PATH` (manifest v1: | 150 fixtures |
| 1141 | round-39 bytes and green now in the selftest (now 179 fixtures, `r40_*`): UTF-16 without a BOM gives | 179 fixtures |
| 1156 | extension element no longer makes a `loc` invalid. Selftest 183 fixtures. | 183 fixtures |
| 1184 | accepted (legacy laxity). Python 3.10 still runs it (selftest 235 fixtures, ten `r42_*` guards). | 235 fixtures |
| 1215 | \| wave-evidence-ledger \| gate (offline, committed bytes only; no network) \| `python3 -B .ufo/waves/round-52/c52_wave_led | 19 fixtures |
| 1216 | \| quote-truth-counter \| gate (offline, committed bytes only; no network) \| `python3 -B .ufo/waves/round-52/c52_quote_tru | 18 fixtures |
| 1233 | \| readme-index-counter \| gate (offline, committed bytes only; no network) \| `python3 -B .ufo/waves/round-55/c55_readme_i | 35 fixtures |
| 1234 | \| yahoo-robots-quote-truth-counter \| gate (offline, committed bytes only; no network) \| `python3 -B .ufo/waves/round-55/ | 47 sandbox-repo fixtures |

Note on whitespace: cells cannot show leading indentation. Lines 504 and 350 each begin with two ASCII spaces before the text shown. Prefixes that end mid-token are the 120-character cut (line 1128's cut leaves one trailing space).

Pattern B — 9 matching lines. Every `[0-9]+/[0-9]+` token on the line is listed, unfiltered.

| line | first 120 chars | ratio tokens on line |
|---|---|---|
| 212 | \| freshness-sweep \| gate \| `node scripts/freshness-sweep.mjs --offline` for this local-only dispatch; bare form requires | 15/15; 0/25; 25/25 |
| 350 |   instrument: §paths/§history/§armed, exit 0/1/2/64, `--selftest`, pinned | 0/1; 2/64 |
| 927 | score it 5/5; read the counter with the hostile selftest and the code review. | 5/5 |
| 1025 | Round-34 additions after wave 1: the committed selftest `python3 -B scripts/link_preview_selftest.py` (29 fixtures under | 28/28 |
| 1046 | \| link-preview-audit \| gate (offline static Open Graph link-preview policy; no network) \| `python3 -B scripts/link_previ | 28/28 |
| 1198 | \| redirect-expectation-audit \| gate (offline; no network) \| `python3 -B scripts/redirect_audit.py --manifest PATH` (mani | 23/23; 11/11; 3/3 |
| 1199 | \| commit-citation-lint \| gate (offline; no network) \| `python3 -B scripts/citation_lint.py --root . [--revision REV] [-- | 8/8 |
| 1203 | The round-46 `c46_matrix.py` figures above are observed fixture outcomes, not a semantic certificate or evidence of an i | 11/11; 3/3 |
| 1234 | \| yahoo-robots-quote-truth-counter \| gate (offline, committed bytes only; no network) \| `python3 -B .ufo/waves/round-55/ | 0/8 |

Table rows containing `--selftest` or `_selftest.py` — 24 rows, line numbers only: 212, 213, 388, 412, 483, 538, 539, 556, 569, 588, 617, 618, 619, 726, 1046, 1067, 1093, 1128, 1198, 1199, 1215, 1216, 1233, 1234.

## TOTALS:

- Pattern A matching lines: **20** (21 matches; line 726 carries two: `30 matrix fixtures` and `15 round-29 regression fixtures`).
- Pattern B matching lines (same-line ratio + selftest): **9**.
- Overlap of A and B: lines 1025, 1046, 1234 → **3**; union of both patterns: **26** distinct lines.
- `|`-leading (table) lines in the file: **175**; table rows containing `--selftest` or `_selftest.py`: **24**.
- All lines (table or prose) containing `--selftest` or `_selftest.py`: **41**; of those, **17** are not `|`-leading.

VERDICT: SKILL.md holds 20 lines matching the fixture/case/check count pattern (21 matches) and 9 lines pairing an `n/n` ratio with selftest; 24 of 175 table rows carry `--selftest`/`_selftest.py` (41 lines overall).
