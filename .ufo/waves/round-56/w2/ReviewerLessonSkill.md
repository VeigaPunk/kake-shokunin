# ReviewerLessonSkill

W2 review of `corpus/lessons/round-56.md`, SKILL.md §Round 56 gate registry additions, and
`corpus/QUALITY.md` §Round-56 criteria. Verifications run read-only: `span_tools.py check`,
`git show`/`git diff`/`git ls-tree` against base `e48354b7` and tip `a450e43e`, both counters'
`--selftest` in my own `mktemp -d` clone at `a450e43e`, and direct unit measurement of the
shokuknow staged candidates (read-only).

## LESSON DEFECTS:

1. **Wrong unit count for the S389 reject (minor, number-drift class the round itself mines).**
   `round-56.md:39` says the staged `yahoo-japan-redirect-indexed-url.md` recheck string is
   "90 units" (copied from `w1/ScoutRejectRedirect.md:16`, same wrong figure). Measured under
   the counter's `units()`: the grep-quoted span `が設定されている場合、…判定します。` is
   **84 units** (92 for the whole backticked curl command). The reject decision is unaffected
   (>25 either way) but the printed number is false.
2. **Spot-check deferral leaves the `## Gate` section incomplete at writing (disclosed, minor).**
   `round-56.md:47` says the non-author spot-check "belongs to the closure; none is recorded
   here". LEARNING.md requires the record `agree`/`disagree` in the round's lesson and CORPUS.md
   wants the spot-check result inside `## Gate`; no `round-56-verifier-spotcheck.md` exists yet.
   Honestly disclosed, not masked — but the Gate contract is open until closure lands.
3. **`recorded in LOG.md (seven Self-test cells)` is not yet true (minor).**
   `round-56.md:59` points at LOG.md for the seven rewritten Self-test cells; LOG.md's tail
   (2175 lines) carries no round-56 entry at all (`grep round-56 LOG.md` → 0). The round is in
   flight, so this is a forward reference, not a false historical claim — but the pointer names
   a write that has not happened.

## SKILL DEFECTS:

1. **C1 row's `64=usage` is loose (minor).** `SKILL.md:1253` maps `64=usage` for
   `c56_selftally.py`; the script's own usage path exits 64 (no-args → 64 verified) but an
   `argparse` error (e.g. `--bogus-flag`) exits **2**, which the same map reads as
   could-not-evaluate. The C2 row documents `ap.error` → 2 explicitly; the C1 row does not.
   Every other verdict-map statement verified: `1=not met` enumerates exactly the ten problem
   codes the counter emits (docstring lines 19–28); the runtime-only `tally_unparsable` falls in
   the documented exit-2 bucket. Exit probes: bad-rev/bad-root → 2 as documented.

## QUALITY DEFECTS:

1. **No blocking defect.** Each of the six Round-56 criteria (`QUALITY.md:1188-1217`) cites a
   real lesson row or Gate/registry artifact and a falsifier that exists:
   c1 → §Mistakes `number-drift` + `c56_selftally.py` (its selftest junk list matches the 47/47
   cases); c2 → §Mistakes `stale-premise` + `ExecPinProof.md` and `env_pin_removed` selftest
   case; c3 → §Mistakes `vacuous` + `CriticC2Contract.md` WR-1/A1 + `HELD_BODY_SHA256`;
   c4 → `EntryDeletedUrl.md` §Quote classes + `CriticControls.md` (files exist); c5 →
   `ScoutClaimsAudit.md`/`ReviewerStaged.md`/`CritCheatC2.md` (all exist) + `STAGED_ABSENT`;
   c6 → `CriticC2Contract.md` A6/WR-2 (quote-regex splitting verified in code at line 698).
2. **Convention nit (not a defect):** only criterion 1 carries an explicit `Falsifier:` command
   line; criteria 2–6 name counter mechanisms (`selftest_failed`, C5 cases) instead. Same shape
   as the round-55 criteria (only c1/c4 name falsifier commands there), so in-convention.

## CLEAN CHECKS:

- **SOURCES rule 1 / CORPUS kaika rules:** every new row's Gate line carries URL + access date
  2026-10-25 + located quote. Unit-verified against retained bodies via `span_tools.py check`:
  S367 `インデックスへの登録を許可する` 15u/15c, S419 `クローラーは削除されたウェブページと認識できず、`
  23u/24c, S420 `クローラーはエラーページとみなさず、` 17u/18c — all ≤25u/40c, raw substrings,
  in the article block, count 1 in own page, absent from both sibling bodies. The S367 quote sits
  inside the `メタタグを使用する方法` section (offsets 2821 < 3018 < 3194) as its `§` locator
  claims; all named headings occur in their bodies (verified by count).
- **Registry facts:** `git show` counts 156 → 158 rows exactly as the lesson's command states;
  S367's base↔tip diff touches `used-by` only (cell-level diff, 11 cells both sides); S419/S420
  are 11-cell `mined` rows, opened 2026-10-25, recheck `180d`, single used-by each; S387/S388/S389
  absent from the registry; `quarantine-slice` = 12 rows; `claim-count-derivation.md` exists.
- **Prompt §2b:** census before/after receipts exist (`controls/census-before.txt`);
  `w1/ExecRowDryRun.md` records 158 rows, exit 0, E03/E01/E11 breaks caught — matches the
  lesson's citation; `## Mistakes` uses the `mistakes.md` vocabulary with class/evidence/
  captured-by/fix per row and red-before receipts (`controls/base-c1-selftally-v2.txt` exit 1);
  one sourced claim (C2) rests on S367/S419/S420 opened this round; candidates listed as
  admitted (3, each provenance-trio'd `source:`/`verified-at:`/`recheck:`) and refused (3,
  each with reason + flip); staged `soft-404` name correctly absent from the tree.
- **SKILL.md rows:** both new rows carry all eight cells. 47 tally verified by running
  `python3 -B c56_selftally.py --selftest` → `47/47`; 67 tally verified twice → `67/67`
  (unpinned and `KAKE_R56_SELFTEST_REV=3691e96…`; 63 fail cases + pass + 3 unit checks = 67,
  matching "64 fixtures + 3 unit checks"). The pin `3691e96` resolves, is an ancestor of
  `a450e43e`, and contains all round-56 evidence. "Seven Self-test cells … three that agreed":
  `git diff` shows exactly 7 Self-test-cell edits (source-recheck 101→106, robots 137→204,
  sitemap 150→235, citation-lint 8→9, quote-truth pin+18, readme-index 35→44,
  yahoo-robots 47→54) and 3 untouched agreeing rows (base-path 106, redirect 23,
  wave-evidence-ledger 19). C2 usage-error wording verified empirically (`ap.error` → 2).
- **Entry ceilings:** 21/15/12 quoted spans in the three adopted entries — none over 25u/40c;
  the S367 entry's spans ≤24u as the lesson claims. Staged numbers checked: S388 recheck 98u ✓,
  S375/S376 staged quotes 46u/29u ✓, S388 label 0 hits ✓, S388 absent from registry ✓.
- **Selftest pin mechanics (QUALITY c2):** `KAKE_R52_SELFTEST_REV=1ae8de5d4dee` and
  `KAKE_R55_SELFTEST_REV=64c0ce12…` both named in rows verbatim; the documented commands match
  the counter's command grammar.

VERDICT: Three minor lesson defects (S389 "90 units" is really 84; spot-check deferral disclosed
but leaves the Gate section open; LOG.md pointer precedes the write), one minor SKILL verdict-map
looseness (C1 `64=usage` vs argparse's 2), no QUALITY defects — everything else verified true.
