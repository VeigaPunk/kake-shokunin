# ScoutC1Table

Read-only scout, report only (none of these are round-59 targets). Base `fd6303ce5c14b3f892dec586297a942ab6e4193b`
(SCORECARD.md and SHONEN.md are byte-identical at base and at lane tip `cb68527`; checked by diff). Capability checks ran in a
`git clone --shared` detached at the base under my scratch dir. Observed = ran or read; [INFERENCE] marked.

## LAST-CHANGE:
Axis table rows (SCORECARD.md lines 17-19), compared with `git log -L<line>,<line>:SCORECARD.md` and the Move log / round sections.
- calibration, `58`: CORRECT. Row first appeared round 54 (score 0->1, `8e408e0`), stayed 1 through rounds 55-57 (sections at lines
  4306, 4334, 4361 say "stays 1/10"), moved 1->2 in round 58 (line 4384 "score 1->2"; row last edited `1b009b7`). Evidence prose matches
  line 4394 (19 undisclosed events -> 0).
- operability, `round 12`: CORRECT as the last NUMERIC move (`a642f93` "operability 9->10", 2026-09-28; row not edited since). But the cell
  is stale as an evidence pointer: it cites only r11/r12 live-run work, while operability claims were HELD at 10 in rounds 20-58 (e.g.
  line 266 r21, 404 r24, 4289 r54, 4362 r57, 4395 r58 "6/14 -> 14/14"). Whether "Last change" means "last score move" or "last claim that
  worked this axis" is unstated in the table (no AXES.md in the lane; `AXES.md` exists only at the fleet root, not read here).
- freshness, `17`: INCONSISTENT with the git history. Numeric move 9->10 is round 16 (`ab87a48` "freshness 9->10"); round 17 (`72eb112`) was
  "HOLD 10" (a text edit, no score change). So `17` is the last row edit, not the last score move (that is 16). Freshness claims were held
  at 10 later in rounds 21, 24, 44, 45, 53, 55-58 without touching the row.
- Format drift: cells read `round 12` / `17` / `58` (mixed label styles).
- Sub-observation: the operability and freshness rows are the first cell of a pointer-style essay (1,090 and 1,244 characters) and the
  rows' text mentions "r17 HOLD 10" as the freshness lead while the Evidence column for both stops at 2026-09-28/29 data.
- Net: 0 hard false cells for calibration; 1 definitional ambiguity (operability); 1 factual off-by-one if "last change" = last score move (freshness 17 vs 16).

## CAPABILITY ROWS:
Capability tables are split: main table lines 193-204 (+ round-44 row at 223); later rows live inside round sections
(51: line 4209; 55: 4316-4319; 56: 4343-4347; 57: 4374-4377). The header at line 213 says rows enter "only through a round that
demonstrates the capability"; the later tables are not merged into the line-193 table.
Evidence-path existence at base (every `scripts/`, `.ufo/` pointer in all 25 capability rows): all resolve. Shorthand relative paths
(`verification/...`, `controls/...`, `resid/...`, `w1/...`) resolve under the round named in the row, 13/13 checked with `git cat-file -e`.
Sampled commands, run at the base in the scratch clone (all exit 0 unless noted):
| Row (first-working round) | command | observed | row's stated figure |
|---|---|---|---|
| canonical preflight (22) | `canonical_audit.py --selftest`; `.ufo/waves/round-22/measure.py --revision b539cc17` | selftest 82/82 cases pass (82 counted by script); measure `accepted: 32` | row says "selftest 62/62" and 32/32: 32 OK; 62 is historical (82 now; line 350 already records 82/82) |
| base-path audit (29) | `base_path_selftest.py`; `c2_matrix_count.py --revision d8cd2e45` | 45/45 fixtures; `C2 30/30` | 45/45 and 30/30: MATCH |
| link-preview (34/35) | `link_preview_selftest.py` | 46/46 | rows say 29/29 (r34) and 45/45 (r35, at `b1cbbc39`): HISTORICAL, drift +1 since |
| source re-check (36) | `source_recheck_selftest.py` | 106/106 | row says 101/101 "at 4d5b3d55": historical, drift +5 |
| robots audit (37) | `robots_audit_selftest.py`; `--help` | 204/204; `--help` exits 64 | row names only the sealed 28/28 counter (not rerun) |
| sitemap audit (39) | `sitemap_audit_selftest.py --tool scripts/sitemap_audit.py`; `sitemap_audit.py --help` | PASS 235/235; `--help` exit 64, 0 bytes of output | row says 150/150 "at 565ef4c9": historical, drift +85. Bare selftest without `--tool` exits 64 (usage), `--help` does not print help |
| quote-class ledger (50) | `c50_quote_class.py --revision ff3f6ecf` / `9619af67` / base | `C1 classed 3/3 met=True` exit 0 / `0/3 met=False` exit 1 / `3/3` exit 0 | MATCH, including the do-nothing control |
| source-id resolver (57) | `id_resolver.py --selftest` | 59/59 | row cites round-57 files (49/49 at that time): historical; line 4395 already says 59/59 |
| landed check (56) | `landed_check.py --selftest` | 14/14 | no tally stated in row |
| wave-evidence ledger (51), witness gate (44), selftally (56) | `--help` only | exit 0 | `c44_audit.py` full run NOT run (heavy) |
Not run: `live_snapshot.py` network/--reaudit, `c44_audit.py` full counter, `c56_selftally.py`, `source_recheck`/`robots` sealed counters,
the round-34/36/37/39 counters. Row figures that quote a tally without "at <sha>" and now differ (canonical 62, link-preview 29) read as
current claims but are historical: 2 rows. [INFERENCE] a reader would need the row's revision qualifier to avoid a false mismatch.
No row's command failed to run; 0 dead evidence paths.

## SHONEN:
- `SHONEN.md` at base (and tip): 4 boxes, all `[ ]`; file last touched in the seed commit `1126144` ("seed: kake shonen"). It has no `[~]` state.
- Round-58 report (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-58/kake.md:58-63`, `## SHONEN`): box 1 `[~]`, box 2 `[ ]` ("untouched this
  round"), box 3 `[~]`, box 4 `[~]`. Round-57 report (lines 79-84): all `[ ]`. Round-58 lesson (`corpus/lessons/round-58.md:137`) says "D4 SHONEN: untouched
  (operator-owned promotion)"; spot-check lesson section 7 says nothing was written to SHONEN.md.
- Mismatch: SHONEN.md (4x `[ ]`) vs round-58 report (3x `[~]`, 1x `[ ]`) — 3 of 4 boxes differ in glyph. It is a reporting-convention mismatch (the report invents
  `[~]` for "asserted by author"), not a promotion claim: the report text carries no claim that SHONEN.md changed. Box wording also differs slightly (report
  drops "real" and "by an agent"; SHONEN.md box 1 says "real decision tables ... cited sources", box 3 "by an agent").
- Report evidence pointers resolve at base: `corpus/QUALITY.md` "## Round-58 criteria" (line 1260), `PROVINCE.md` "## Round-58 crawler identity" (line 449), S378 rejection text
  present in the registry grep, `r1/ReviewerEntryUnblocking.md` exists.
- Round-58 spot-check says boxes 1, 3, 4 "look mechanically checkable by a non-author"; none carries a named non-author `[x]`.

## Scratch
Clone and scratch dir removed at the end; no lane state touched. No installs.

VERDICT: calibration row's Last change (58) correct; freshness `17` is the last edit but the last score move was round 16, operability `round 12` is right only on the score-move reading; 25 capability rows resolve with 9 sampled commands running (4 historical tally drifts: 62->82, 29/45->46, 101->106, 150->235), and SHONEN.md (4x `[ ]`) differs from round-58's reported `[~]`,`[ ]`,`[~]`,`[~]` by glyph only.
