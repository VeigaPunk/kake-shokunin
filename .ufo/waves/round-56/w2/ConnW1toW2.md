# ConnW1toW2

Cross-wave connection pass synthesizing 11 W1 reports across contract, critic, mutation, reviewer, and cheat seats.

## FINDING DISPOSITION TABLE:

| ID | Seat | What it attacks | Disposition | Evidence / Resolution |
|---|---|---|---|---|
| A1 | CriticC1Contract | `c56_selftally.py:101` (fake print in span) | Acted on | Commit 3691e96 `c56_selftally.py:164-171` (`command_problem` strict argv) |
| A2 | CriticC1Contract | `c56_selftally.py:107` (qualifying span shadows) | Acted on | Commit 3691e96 `c56_selftally.py:150-156` (bound to `Self-test` cell) |
| A3/A3c | CriticC1Contract | `c56_selftally.py:89` (duplicate row / section escape) | Acted on | Commit 3691e96 `c56_selftally.py:126,243` (`duplicate_row` & table header check) |
| A4 | CriticC1Contract | `c56_selftally.py:189` (helper module inflation) | Acted on / Disclosed | Commit d5afc48 `c56_selftally.py:205`; `contract.md:100` (outside dir unpinned) |
| A5 | CriticC1Contract | `c56_selftally.py:196` (two junk claims sum to tally) | Acted on | Commit 3691e96 `c56_selftally.py:61,260` (`nclaims` integer match) |
| A6 | CriticC1Contract | `c56_selftally.py:156` (host env leak via `os.environ`) | Acted on | Commit d5afc48 `c56_selftally.py:192-203` (fixed environment scrub) |
| A7 | CriticC1Contract | `c56_selftally.py:51` (11th registry row invisible) | Disclosed limit | `contract.md:36`, `ReviewerSkillRegistry.md:107` (population closed at 10) |
| A8 | CriticC1Contract | `c56_selftally.py:163` (host path in span outside clone) | Acted on | Commit 3691e96 `c56_selftally.py:169` (strict argv matching) |
| A9 | CriticC1Contract | `c56_selftally.py:222` (`rows_checked` vacuous) | Acted on | Commit d5afc48 `c56_selftally.py:246,288` (`checked = sum(r["checked"])`) |
| A10 | CriticC1Contract | `c56_selftally.py:348` (caller-chosen revision) | Disclosed limit | `contract.md:85-88` (provenance recorded in contract & settlement) |
| W1 | CriticC1Contract | `c56_selftally.py:158` (`env` prefix command rejected) | Acted on | Commit d5afc48 `c56_selftally.py:166,197` (`PIN_RX` allowlist) |
| W2 | CriticC1Contract | `c56_selftally.py:rx` (breakdown summed to 90) | Acted on | Commit 3691e96 `c56_selftally.py:63` (`nclaims=2` for `base-path-audit`) |
| W3 | CriticC1Contract | `c56_selftally.py:129` (multi A/B output, last wins) | Acted on | Commit d5afc48 `c56_selftally.py:75,174` (anchored `TALLY_RES`) |
| W4 | CriticC1Contract | `c56_selftally.py:189` (tool_changed blocks repair) | Acted on | Commit d5afc48 `SKILL.md:1216` (env pin in row prose bypasses script edit) |
| W5 | CriticC1Contract | `c56_selftally.py:parse_tally` (prose tally unparsable) | Disclosed limit | `contract.md:91` (standard tally regexes required) |
| W6 | CriticC1Contract | `c56_selftally.py:163` (missing python3 prefix) | Acted on | Commit 3691e96 `contract.md:91`, `c56_selftally.py:169` (`python3 -B` contract) |
| A1 | CriticC2Contract | `c56_quote_truth.py:C6` (self-referential body pin) | Acted on | Commit d5afc48 `c56_quote_truth.py:91,339` (`HELD_BODY_SHA256` pin) |
| A2 | CriticC2Contract | `c56_quote_truth.py:C1-C6` (12-line junk entry accepted) | Disclosed limit | `contract.md:111-113` (substring truth, not semantic support) |
| A3 | CriticC2Contract | `c56_quote_truth.py:249` (false verified-at date) | Acted on | Commit d5afc48 `c56_quote_truth.py:270` (`verified-at == ROUND_DATE`) |
| A4 | CriticC2Contract | `c56_quote_truth.py:334` (page-unique sibling-only) | Acted on | Commit d5afc48 `c56_quote_truth.py:349` (checked vs all retained bodies) |
| A5 | CriticC2Contract | `c56_quote_truth.py:377` (1-token quote skipped) | Acted on | Commit d5afc48 `c56_quote_truth.py:408` (`len >= 12` substring checked) |
| A6 | CriticC2Contract | `c56_quote_truth.py:376` (raw `"` splits quote check) | Disclosed limit | `contract.md:115`, `settlement.md:12` (entries avoid raw `"`) |
| A7 | CriticC2Contract | `c56_quote_truth.py:C1` (staged filename survives) | Acted on | Commit d5afc48 `c56_quote_truth.py:87,247` (`STAGED_ABSENT` check) |
| A8 | CriticC2Contract | `c56_quote_truth.py:89` (punctuation 0 units / 44 chars) | Acted on | Commit d5afc48 `c56_quote_truth.py:86,396` (`CHAR_CEILING = 40`) |
| A9 | CriticC2Contract | `c56_quote_truth.py:259` (empty row metadata fields) | Acted on | Commit d5afc48 `c56_quote_truth.py:92,298` (`kind/tier/scope/teaches` checks) |
| A10 | CriticC2Contract | `c56_quote_truth.py:276` (junk recheck regex) | Acted on | Commit d5afc48 `c56_quote_truth.py:307` (strict `recheck` regex) |
| A11 | CriticC2Contract | `c56_quote_truth.py:326` (S367 second section only) | Acted on | Commit d5afc48 `corpus/knowledge/yahoo-japan-link-target-...:15` |
| A12 | CriticC2Contract | `c56_quote_truth.py:C7` (census receipts self-authored) | Disclosed limit | `contract.md:114`, `settlement.md:13` (receipt check only) |
| WR-1 | CriticC2Contract | `c56_quote_truth.py:319` (S367 title punctuation reject) | Acted on | Commit d5afc48 `c56_quote_truth.py:91,339` (sha256 body pin) |
| WR-2 | CriticC2Contract | `c56_quote_truth.py:376` (raw `"` quote unverifiable) | Disclosed limit | `contract.md:115` (entries avoid raw `"`) |
| WR-3 | CriticC2Contract | `c56_quote_truth.py:356` (multiline spans split) | Disclosed limit | `contract.md:115` (per-line span evaluation) |
| F1 | CriticControls | `c56_selftally.py:222` (`rows_checked` constant len) | Acted on | Commit d5afc48 `c56_selftally.py:246,288` (`checked = sum(r["checked"])`) |
| F2 | CriticControls | `c56_selftally.py:101` (`--case D1-root` junk pass) | Acted on | Commit 3691e96 `c56_selftally.py:169` (strict command equality) |
| F3 | CriticControls | `contract.md:52` (census validate base-satisfied) | Acted on | Commit 3691e96 `contract.md:107` (dropped from predicate) |
| F4 | CriticControls | `c56_quote_truth.py:395` (Gate quotes not unique in body) | Acted on | Commit 3691e96 `c56_quote_truth.py:401` (`text.count(q) == 1`) |
| F5 | CriticControls | `AXES.md:15` (C1 surface not SCORECARD calibration) | Disclosed limit | `contract.md:118` (axis note; SCORECARD held at 1) |
| F6 | CriticControls | `contract.md:C2` (lacked "What counter does not test") | Acted on | Commit 3691e96 `contract.md:111` (limits section added) |
| F7 | CriticControls | repo (uncommitted working tree counters) | Acted on | Commit 3691e96 `contract.md:84` (counters committed and declared) |
| F8 | CriticControls | `contract.md:21` (quote-truth "disagree" wording) | Acted on | Commit 3691e96 `contract.md:98` (clarified unpinned failure) |
| F1-4 | CriticAxisClaim | `contract.md:13-15` (C1 operability, C2 coverage) | Disclosed limit | `contract.md:118` (axis note records both views) |
| H1 | CriticAxisClaim | `c56_selftally.py:51` (new tools outside POP) | Acted on | Commit a450e43 `SKILL.md:1243` (additions section appended) |
| H2 | CriticAxisClaim | `c56_selftally.py:197` (tool_changed blocks edits) | Acted on | Commit d5afc48 `SKILL.md:1067-1234` (SKILL-only fixes) |
| H3 | CriticAxisClaim | `corpus/SOURCES.md:157` (S367 re-verify unrecorded) | Disclosed limit | `contract.md:80` (re-verification in receipts.json) |
| H4-5 | CriticAxisClaim | axis governance (premature saturation/ownership) | Disclosed limit | `contract.md:118` (operator ruling required) |
| H6 | CriticAxisClaim | `c55_readme_index.py` (cross-round gate regression) | Acted on | Commit d5afc48 `corpus/README.md:66` (coverage map updated) |
| M03 | MutC1Counter | `c56_selftally.py:196` (first claim only `nums[0]`) | Acted on | Commit 3691e96 `c56_selftally.py:387` (fixture `sum_row_with_two_claims`) |
| M07 | MutC1Counter | `c56_selftally.py:129` (first tally match returned) | Acted on | Commit 3691e96 `c56_selftally.py:408` (fixture `last_tally_line_wins`) |
| M09 | MutC1Counter | `c56_selftally.py:89` (last table row wins) | Acted on | Commit 3691e96 `c56_selftally.py:378` (fixture `duplicate_row_earlier`) |
| M12 | MutC1Counter | `c56_selftally.py:270` (TimeoutExpired swallowed) | Acted on | Commit 3691e96 `c56_selftally.py:410` (fixture `timeout_is_unevaluable`) |
| M13 | MutC1Counter | `c56_selftally.py:142` (clone_at skipped) | Acted on | Commit 3691e96 `c56_selftally.py:415` (fixture `measures_checked_out_rev`) |
| M16 | MutC1Counter | `c56_selftally.py:90` (row regex space tolerance) | Acted on | Commit 3691e96 `c56_selftally.py:419` (fixture `indented_table_rows`) |
| HIGH | ReviewerSelftallyCode | `c56_selftally.py:61` (yahoo claim undercapture) | Acted on | Commit d5afc48 `SKILL.md:1234` (reworded to 54 fixtures) |
| MED 1 | ReviewerSelftallyCode | `c56_selftally.py:113` (shlex ValueError abort) | Acted on | Commit d5afc48 `c56_selftally.py:138` (ValueError caught, continue) |
| MED 2 | ReviewerSelftallyCode | `c56_selftally.py:103` (_is_selftest_span before shlex) | Acted on | Commit d5afc48 `c56_selftally.py:157` (shlex before word test) |
| MED 3 | ReviewerSelftallyCode | `c56_selftally.py:112` (nested brackets `[--tool [PATH]]`) | Acted on | Commit d5afc48 `c56_selftally.py:130,444` (recursive bracket strip) |
| MED 4 | ReviewerSelftallyCode | `c56_selftally.py:136` (permissive tally regex) | Acted on | Commit d5afc48 `c56_selftally.py:75,438` (strict `TALLY_RES`) |
| MED 5 | ReviewerSelftallyCode | `c56_selftally.py:92` (escaped pipe `\|` in cell) | Acted on | Commit d5afc48 `c56_selftally.py:118` (`(?<!\\)\|` split) |
| LOW 1 | ReviewerSelftallyCode | `c56_selftally.py:142` (clone_at dir leak) | Acted on | Commit d5afc48 `c56_selftally.py:192` (cleanup in `except BaseException`) |
| LOW 2 | ReviewerSelftallyCode | `c56_selftally.py:252` (_sandbox.commit add -A) | Acted on | Commit d5afc48 `c56_selftally.py:324` (`text is None` file removal) |
| LOW 3 | ReviewerSelftallyCode | `c56_selftally.py:163` (argv[0] whole run abort) | Acted on | Commit d5afc48 `c56_selftally.py:164,250` (`command_problem` check) |
| LOW 4 | ReviewerSelftallyCode | `c56_selftally.py:165` (run_command stdin unclosed) | Acted on | Commit d5afc48 `c56_selftally.py:201` (`stdin=subprocess.DEVNULL`) |
| INFO | ReviewerSelftallyCode | `c56_selftally.py:211` (double blob() call) | Unaddressed | `c56_selftally.py:211` redundant subprocess call |
| Audit | ReviewerSkillRegistry | `SKILL.md` (population sound; link-preview excluded) | Acted on | `contract.md:28,36` confirmed sound |
| Limit | ReviewerSkillRegistry | `SKILL.md` (8 unmeasured prose tallies, 3 stale) | Disclosed limit | `contract.md:36` (scope limited to self-test cells) |
| g1 | ReviewerPlan | `corpus/SOURCES.md:159` (S420 used-by rename) | Acted on | Commit d5afc48 `corpus/SOURCES.md:159` (pointed at nonexistent-url) |
| g2 | ReviewerPlan | `corpus/lessons/round-56.md` (Gate-block assembly) | Acted on | Commit d5afc48 `corpus/lessons/round-56.md:12-45` |
| g3 | ReviewerPlan | `assimilation/guard-proof/` (wave evidence) | Acted on | Commit d5afc48 `.ufo/waves/round-56/w1/ExecIdGuard.files/` |
| g4 | ReviewerPlan | EntryLinkTarget (staged cross-reference exclusion) | Acted on | Commit d5afc48 `corpus/knowledge/yahoo-japan-link-target-...` |
| S367 | ReviewerStaged | staged S367 (per-link, attribution, motive) | Acted on | Commit d5afc48 `yahoo-japan-link-target-...` trimmed & grounded |
| S419 | ReviewerStaged | staged S419 (46u quote, dropped hedge, trigger) | Acted on | Commit d5afc48 `yahoo-japan-deleted-url-...` 23u quote, hedge restored |
| S420 | ReviewerStaged | staged S420 (29u quote, causes list, aphorism) | Acted on | Commit d5afc48 `yahoo-japan-nonexistent-url-...` 25u quote, aphorism trimmed |
| Cheat 1 | CritCheatC1 | `c56_selftally.py:89` (duplicate row cheat) | Acted on | Commit d5afc48 `c56_selftally.py:243` (`duplicate_row` check) |
| Cheat 2 | CritCheatC1 | `c56_selftally.py:196` (padded claims in cell cheat) | Acted on | Commit d5afc48 `c56_selftally.py:260` (`claim_ambiguous` check) |
| Cheat 3 | CritCheatC1 | `c56_selftally.py:107` (command in earlier column cheat) | Acted on | Commit 3691e96 `c56_selftally.py:150` (`Self-test` column binding) |
| Coupling | CritCheatC1 | `c56_selftally.py:205` (`helpers_changed` over-broad) | Unaddressed | Directory-wide `*.py` check couples unrelated rows |
| Hygiene | CritCheatC1 | counter workflow (uncommitted counter drift) | Acted on | Commit 3691e96 `contract.md:84` committed & amended |
| Var A | CritCheatC2 | `c56_quote_truth.py:C1-C8` (junk tree passes 8/8) | Partially acted on / Disclosed | Commit d5afc48 metadata checks; `contract.md:111` disclosed |
| Var B | CritCheatC2 | `c56_quote_truth.py:C8` (mirror written same commit) | Acted on / Confirmed | C8 rejects same-commit mirror |
| Var C | CritCheatC2 | `c56_quote_truth.py:465` (mirror delete/re-add passes C8) | Unaddressed | `c56_quote_truth.py:465` takes oldest commit `commits[-1]` |
| Var D | CritCheatC2 | `c56_quote_truth.py:C5` (quotes in HTML comments) | Unaddressed / Disclosed | Substring-only window; comments unstripped |
| Var E | CritCheatC2 | `c56_quote_truth.py:319` (honest body fails on punctuation) | Acted on | Commit d5afc48 `c56_quote_truth.py:91,339` (`HELD_BODY_SHA256` pin) |

## CROSS-SEAT PATTERNS:

1. **Receipt agreement is not proof of execution**: Hit independently by `CriticC2Contract` (A12), `CriticControls` (F3/F6), and `CritCheatC2` (Var A). In C6 and C7, receipts are self-authored text artifacts; `sources-census.sh validate` never actually executed during C7 verification in junk fixtures. Acted on by disclosing in `contract.md:114` and `settlement.md:13` that C7 is an agreement receipt, requiring W2 executors to independently execute the real command.
2. **Counter-induced honest rejection**: Hit by `CriticC1Contract` (W4), `CriticC2Contract` (WR-1), `CritCheatC1` (E1), and `CritCheatC2` (Var E). Strict syntactic rules in frozen v1 counters rejected truthful implementations (fullwidth punctuation differences in S367 rejected honest retained bodies; `tool_changed` forbade legitimate fixture bug fixes) while admitting synthetic junk. Resolved by adding the `KAKE_R52_SELFTEST_REV` env pin to SKILL.md and replacing title substring matching with `HELD_BODY_SHA256` pin.
3. **Syntactic parsing shortcuts admit injection / shadowing**: Hit by `CriticC1Contract` (A1, A2, A3, A5), `CritCheatC1` (Cheats 1-3), `ReviewerSelftallyCode` (MED 1, 3, 4, 5), and `CriticC2Contract` (A5, A6, A8). Unanchored regexes, naive string splitting (`split("|")`), and first-match loops permitted span shadowing, nested bracket corruption, and multi-integer claim inflation. Resolved in C1 v2 via column binding (`Self-test`), `(?<!\\)\|` splitting, recursive bracket stripping, and strict `nclaims` cardinality.
4. **Shared across claims (C1 and C2)**:
   - *Closed-world assumption*: Both counters enforce manually curated lists (`POP` with 10 rows in C1; `ADOPTED` with 3 rows in C2) and cannot discover or check unlisted rows (8 prose tallies unmeasured in SKILL.md; non-adopted rows unmeasured in SOURCES.md).
   - *External invariant pinning*: Both v1 counters lacked external bounds and required v2 amendments to check sibling tree state (`helpers_changed` in C1; `HELD_BODY_SHA256` and `others` in C2).
   - *Axis displacement*: Both claims were declared on primary axes (C1 Calibration, C2 Freshness) but actually operate on secondary surfaces (C1 Operability tooling checks; C2 Coverage/Expansion new-entry admissions), leaving core observables (SCORECARD ratings; freshness drift) unmeasured.

## UNADDRESSED:

1. `c56_quote_truth.py:465` (CritCheatC2 Variant C): C8 takes `commits[-1]` from `git log --diff-filter=A`, inspecting only the oldest commit that added the mirror; deleting and recreating the mirror in subsequent commits still passes C8.
   - *Proposed disposition*: Amend C8 in future rounds to verify the mirror commit is an ancestor of the commit introducing the new rows (`git log -S`), or record as a disclosed invariant in contract.
2. `c56_selftally.py:205-212` (CritCheatC1 / CriticC1Contract A4): `helpers_changed` pins all `*.py` files in the script directory at base revision; editing any unrelated script under `scripts/` marks 6 unrelated gate registry rows `tool_changed`.
   - *Proposed disposition*: Hold as disclosed limitation for round-56 (`contract.md:100`); in future counter versions, scope helper checks to an explicit module import graph (`ast.parse`) or stem matching.
3. `c56_quote_truth.py:377` (CritCheatC2 Variant D): C5 searches raw substrings in a byte window without HTML DOM parsing; quotes inside HTML comments `<!-- ... -->` or tag attributes pass counter verification.
   - *Proposed disposition*: Disclose as an accepted limit of regex counters; rely on non-author reviewer quote audits (`ReviewerStaged`, W2 recounts) for rendering context.
4. `c56_selftally.py:211` (ReviewerSelftallyCode INFO): Redundant `blob()` call per row in `helpers_changed` (checks existence via rev-parse then compares).
   - *Proposed disposition*: Hoist into local variable during next tooling pass; harmless minor subprocess overhead.
5. `SCORECARD.md` calibration pointer (CriticControls F5, CriticAxisClaim F2): Self-assessment calibration row still points to round-54 evidence `.ufo/waves/round-54/c54_s374_calib.py`.
   - *Proposed disposition*: Retain calibration at 1/10 per `contract.md:118-120` pending operator ruling on whether tooling gate registry rows fall under calibration or operability.

VERDICT: All high-severity W1 findings were acted on in commits d5afc48 and 3691e96 or disclosed in contract.md §Counter versions; five residual architectural limitations (C8 oldest add, directory-wide helper coupling, comment-blind quotes, redundant blob call, SCORECARD pointer) are documented above with proposed dispositions.
