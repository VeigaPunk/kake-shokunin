# `## Mistakes` — draft for `corpus/lessons/round-98.md` (kake round 98)

Seat: ScribeLesson (scribe, leaf member — no subagent dispatch). Draft only; the L1 integrates.
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Round base `e51328b63690c8aaa78c9c8f3b87d8735c0ccbf7`;
instruments `2db768356cd081092c3abc60f76b25487ec4c535`; freeze `c3eace8b5c70453faff872c89d8443753e5d21b6`;
C1 repair `4446ce219b4f0c9f5f4fc81f7f772e3a7f24c95a`; lane tip at this seat's start
`7838981e4e40280176085e8aa1f6827eb7133a69` (`git -C LANE rev-parse master`).

Table shape follows `corpus/lessons/round-97.md` `## Mistakes`: `# | Class | Evidence | Captured-by | Fix`.
Every evidence pointer is `path:line` into committed bytes; every command and rc is in the
receipt files beside this draft (`receipt-*.txt`, all in this directory).

Frozen digests verified before use (`sha256sum` against
`.ufo/waves/round-98/controls/instrument-sha256.txt`): `c98_captable.py` `efd59857…7cf3`,
`c98_stale.py` `e0331e56…a9f3` — both match. No frozen byte was touched by this seat.

**Overlap with the L1's landed lesson (read at `corpus/lessons/round-98.md:59` while this draft was
being written).** The L1's `## Mistakes` already carries an M1 (the Capabilities drift) and an M2
(the R98-D1 meta-text leak), and its `## Quality criteria added this round` already carries an
R98-B for `considerthese/2026-11-05.md` proposal 2. Rows 1 and 2 below are this seat's independent
mining of the same two required items — they agree with the L1's M1/M2 on the evidence and on the
fix, and they add the `path:line` pointers and the two round-review receipts. Rows 3, 4 and 5 are
**new**: `grep -n 'landed-tip\|improved-bounded\|attack share' corpus/lessons/round-98.md` returns
no hit, so the three routes below are not in the landed lesson. The L1 may adopt rows 3–5 verbatim,
reword them, or record them as not-mined under R98-Y4; this seat does not decide.

---

## Mistakes

| # | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| 1 | Self-assessment drift: the `SCORECARD.md` `## Capabilities` table stopped receiving rows after round 82, so the lane's own repertoire no longer matched the capabilities its own closures had admitted. Eight admitted capabilities (rounds 83, 85, 87, 88, 90, 93, 97 ×2) were demonstrated and recorded in per-round `### Demonstrated repertoire` subsections but never entered the `## Capabilities` table; six table rows were unbacked — five named capabilities whose closures were never admitted (rounds 34, 35, 37, 61, 64) and one named an admitted capability (round 20) under a wording the closure record does not use | `.ufo/waves/round-98/controls/base-c1.txt:2` — `entries=48 rows=14 matched=8 unlisted=40 unbacked=6 mismatches=46 met=false`, `exit=1` at `e51328b6`; the base table's own last row is round 82 (`SCORECARD.md:208` at base), and the round-83/85/87/88/90/93/97 rows live only in per-round `### Demonstrated repertoire` subsections (`SCORECARD.md:5284` at base), never in the `## Capabilities` table at `SCORECARD.md:191` | **a rule, never a gate**: `AXES.md` §Capabilities states the row-entry rule ("Rows enter only through a round that demonstrates the capability running"), but it constrains only the *entry* of a row — no lane criterion or live instrument checked the reverse direction (that every admitted capability has a row) until round 98's `c98_captable.py` (`SKILL.md:223` registers it). The drift is a coverage failure the AXES rule does not reach, so the rule as written did not capture it | the C1 repair at `4446ce2` (`git log --format=%s` → "round-98: C1 repair — Capabilities table matches admitted closures (39 rows added, 1 renamed, 5 moved to history)") re-derives to `entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true`, `exit=0` — re-run read-only by this seat, `receipt-c1-repair-reproduce.txt` (`rc=0`), against the base `receipt-c1-base-reproduce.txt` (`rc=1`). The row-review conjunct (`w1/ReviewCapA/verdicts.tsv` + `w1/ReviewCapB/verdicts.tsv`) is the L1's to record; this seat asserts neither reviewer verdict. |
| 2 | Corpus form defect: seat handoff meta-text was copied into an admitted knowledge entry as a malformed duplicate heading with an unbalanced backtick — a drafting receipt that reached the corpus verbatim | `corpus/knowledge/revalidation-exchange.md:130` at `7838981e` — "## Errata sweep (round 97)`; body is 103 words (word-count receipt in quotes-verified.txt, rc 0, count 103). Drafted by ScoutErrata; the L1 integrates it (this seat makes no knowledge-entry edit)." — sitting 2 lines above the real `## Errata sweep (round 97)` heading at `corpus/knowledge/revalidation-exchange.md:132` | **the round-97 closure, not a lane rule**: `corpus/lessons/round-97-verifier-spotcheck.md:42` (defect D-a) and `:236` (route R98-D1). No lane criterion covered seat meta-text in `corpus/knowledge/` — `grep -rn 'Drafted by\|this seat makes\|word-count receipt' corpus/knowledge/` returns exactly this one line | routed as R98-D1 in the round-98 freeze (delete the line; add a gate that fails on seat meta-text under `corpus/knowledge/`). The round-98 work is the seat `ExecMetaLint` instrument `scripts/knowledge_metatext_lint.py` (selftest 13/13 in `.ufo/waves/round-98/w1/ExecMetaLint/selftest.txt`) — this seat neither wrote nor ran that instrument and claims no verdict on it; the deletion itself is the L1's to land. |
| 3 | Unexmined closure route: the round-94 closure routed "landed-tip receipts uncommitted" (evidence must resolve at closure without the report's own prose) and no later lane lesson ever mined it | `corpus/lessons/round-94-verifier-spotcheck.md:118` — "**Landed-tip receipts uncommitted.** The report's \"final run at `99a88dea`\" C1/C2 outputs have no committed receipt"; `git grep -n 'revision=99a88dea' 99a88dea -- .ufo/` → no match (rc 1), and `grep -rn 'landed-tip\|99a88dea' corpus/lessons/` returns only that spot-check line — no `## Mistakes` row in round-95, -96 or -97 carries it | **none**: the route was named by the round-94 closure and then dropped from the lane's own mined corpus; rounds 95–97 each landed a tip receipt afterwards (`controls/after-c1-final.txt` @ `1fca1ad7`, `controls/after-c1-successor.txt` @ `1098dccd`, `controls/after-c1.txt` @ `d687cd6a`), so the practice was adopted but the lesson was never written | mined here as row 3; the standing rule it implies — a landed-run receipt that the round's own report cites must exist as a committed file under `.ufo/waves/round-<N>/controls/`, and a closure route that the lane does not mine must be recorded as not-mined — is proposed for `corpus/QUALITY.md` (see `quality-criterion.md`, §Round 98). The route itself is closed in practice; this entry mines it, it does not re-open it. |
| 4 | Measurement misstatement carried by a published report and its LOG line: the round-96 wave share counts the sentinel seat as an attack seat, the same defect class the round-80 closure routed (R80-4) and the round-81 accounting artifact pinned — and no closure or lesson since has checked it | the published claim is "attack share 5/12 ≈ 42%" at fleet `.ufo/reports/round-96/kake.md:73` and at lane `LOG.md:3274`; the run-15 attack-role set is pinned at `.ufo/waves/round-81/w1-accounting.json:2` — "attack_role_source": "run-15 addendum role list; sentinel is not an attack role (round-80 closure R80-4)" — and the round-96 spec carries exactly four attack-role seats (`ReviewC1`, `ReviewReval`, `CriticClaims`, `MutReval`), so the strict share is 4/12 = 0.3333; the fifth seat in the numerator is `SentinelScope`. Measured at `receipt-attack-share-instance-r96.txt`. Round 97 published the strict figure correctly (6/13 = 46 %) at fleet `.ufo/reports/round-97/kake.md:169`, so round 96 is the outlier | **none**: `grep -rn 'attack share\|5/12' corpus/lessons/round-9[4-7]*.md corpus/lessons/round-96-verifier-spotcheck.md corpus/lessons/round-97-verifier-spotcheck.md` returns no hit — the round-96 closure's §1 conformance list does not include the wave share, and no lesson carries the recurrence | mined here as row 4. The share is a count like any other and must name its role set and its denominator on the same line as the number; that rule is the criterion proposed in `quality-criterion.md` (Round 98). The published round-96 line is filed bytes in the fleet repo and is not rewritten by this seat; the lane's `LOG.md:3274` line is filed bytes in the lane and is likewise not rewritten here — the correction belongs to the L1 or to the fleet closure, not to a reporter. |
| 5 | Unmined closure route (second instance): the round-95 closure routed a status-neutral vocabulary defect (a trend label outside the protocol vocabulary) and no lane lesson mined it either | `corpus/lessons/round-95-verifier-spotcheck.md:77` — "the report's trend labels read `improved-bounded`, which is not in the protocol vocabulary (`improved \| harmed \| unchanged \| unprovable-but-better`)"; `grep -rn 'improved-bounded' corpus/lessons/round-9[5-8].md` → no hit, and `LOG.md:3264` still carries "expansion improved-bounded" for round 95 | **none**: the route was named by the round-95 closure; the round-96 and round-97 lessons have no row for it, so the lane's own mined corpus does not record the vocabulary rule it received | mined here as row 5. The fix is a vocabulary rule stated once in `corpus/QUALITY.md` (a trend label is one of the four protocol words; a bound goes in the evidence prose) rather than a per-round correction; the historical `LOG.md:3264` line is filed bytes and is not rewritten by this seat. |

### Not mined, and why (so the next round does not re-open them)

- `.ufo/waves/round-94/controls/` holds only `base-c1.txt`, `base-c2-v1.txt`, `base-c2-v2.txt`,
  `ctl-c1-selftest.txt`, `ctl-c2-selftest.txt`, `instrument-sha256.txt` — the round-94 landed-tip
  receipts are absent (row 3's evidence).
- The round-94 closure route 3 (`--skip-battery` returning `met=true` while bypassing the battery
  and the predecessor clauses, `corpus/lessons/round-94-verifier-spotcheck.md:119`) is closed in the
  successor: the round-95 instrument's own docstring states "no `--skip-battery` met=true"
  (`.ufo/waves/round-95/c95_selfassess.py:9`) and the round-96 successor is registered in
  `SKILL.md:219` as battery-covered. It is therefore not re-opened here; it is named so the sweep is
  auditable.
- The round-96 closure count-accuracy note (216 wave-time registry ids vs 217 at the tip,
  `corpus/lessons/round-96-verifier-spotcheck.md:185`) is addressed in the round-96 lesson's own
  Gate (`corpus/lessons/round-96.md:75` cites `w1/ExecReceipts/assimilation/…` with the tip figure);
  it is not a lane mistake and is not mined.
- The round-97 closure's other routed defect (R98-D2, a dead review seat) is handled as round work
  by the round-98 freeze (two full-coverage reviewers), not as a lesson mistake.

### Scope note

This seat mined; it repaired nothing. No corpus file, counter, contract, ledger or registry was
edited by this seat, no verdict is asserted for C1 or C2, and no commit, push, publish or deploy was
performed. The two corrections referenced in rows 1–2 belong to the L1 and to seat `ExecMetaLint`.
