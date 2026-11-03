# Round 71 · w1 · CriticClaims (critic, reviewer route) — attack on C1 and C2

Base cc6b4e0b8c35e72dfb02c6184b847f68c1262153. Read-only on the lane (git show/log/cat-file only; `clone --shared` into scratch; scratch removed at exit). Installed nothing.

## Verdicts

| # | Point | Verdict |
|---|---|---|
| 1 | C1 is a calibration move on the lowest owned axis | **weakened**: placement survives; the attack_share conjunct is **falsified** as a mismatch; stale_planned is not calibration under S132 |
| 2 | C2 is a freshness move; do-nothing reachability; annotation-only green | do-nothing **survives** (red); annotation-only green **falsified** as a measure of the contract's kill rule; placement **weakened** |
| 3 | Axis harm (operability 10, freshness 10, calibration 2) | **weakened**: harms named below, none exercised; one is a new false statement written by the C1 repair |
| 4 | S132 meets CORPUS.md rule 1 for the claim | **weakened** |
| 5 | labrat→executor (amendment-1) | wording change **survives**; the "controls byte-identical" statement is **falsified** by undefined J3 |

## 1. C1 (calibration, score 2)

- Placement survives. AXES.md:33-34 requires one claim on the lowest non-retired axis. SCORECARD.md:19 gives calibration 2; operability and freshness are 10. Grep of `^| saturation`/`^| retired` found no calibration retirement (the `## Retired` heading at line 103 was not expanded).
- **attack_share is falsified as a mismatch.** `.ufo/waves/round-70/amendment-0-note.md:11-16` (pre-dispatch, round 70) says labrat was refused by the validator and "a sentinel seat joins the attack set", and records "Attack share 4/14". `w1-results.json` has reviewer, critic, mutation-tester and sentinel (SentinelAdoption) = 4 of 14. The round-71 counter's STRICT_ROLES (`c71_calibration.py`, reviewer/critic/mutation-tester/labrat) applies the superseded round-70 contract list (`.ufo/waves/round-70/contract.md:131-133`, "4/13 … 1 labrat … 1 revenger"). The stated 4/14 is correct under the definition in force for that wave. Base receipt's attack_mismatch=1 is an artifact.
- The round-70 diagnosis is also wrong: `corpus/lessons/round-70-verifier-spotcheck.md:99-101` says 4/14 counts the **revenger**; the record says sentinel. The frozen repair text "the revenger seat is not an attack role" names the wrong seat, and the repaired value 3/14 would write a false count and a false cause into SCORECARD.
- Also: the strict list names labrat, which `~/.agents/skills/swarm/SKILL.md:122-125` excludes as a swarm role, so no swarm wave can satisfy that list through labrat. Under it, round 70 (3/14 = 21.4 %) is below the binding ≥25 % rule (`scripts/hyaku/lane-addendum.md:3,5`). The correction line does not disclose that.
- stale_planned is weakly sourced. S132 (kama `corpus/knowledge/self-assessment-at-writing.md:7`) defines the error as "a calibration error present when the statement was written". `## Planned` naming round 21, written in round 21, was accurate then. Its justification is age, which is freshness-type.
- Gaming input (scratch, in-memory, base bytes except the stated edits): repairs 2+3+4 only → `stale_planned=1 mismatches=1 met=False` (exit 1). Add the line `**Round 72** — plan re-stamped in place` under line 21 → `stale_planned=0 guard=ok mismatches=0 met=True` (exit 0). The frozen repair 1 (heading → Superseded) is not enforced: the guard fires only on removed lines (`c71_calibration.py` guard loop). "The counter checks the rule" is not true for repair 1.
- Junk J1 (delete both planned headings) → guard=fail, exit 1: confirmed. Heading-only rename of line 3990 to `## Planned — round 72` → guard=fail, exit 1: confirmed.

## 2. C2 (freshness, score 10)

- Do-nothing: base → `tokens_total=7 unannotated_tokens=7 met=False`, exit 1. Not reachable by do-nothing.
- Annotation-only green (input G1, in memory): append ` (historical record, not an executable instruction)` to the seven `/tmp` lines of SKILL.md at base (27, 95, 227, 356, 359, 463, 464) → `unannotated_tokens=0 removed=7 added=7 guard=ok met=True`, exit 0. No `test -e`, no exact target, no recipe repoint. This includes line 95, an imperative recipe. The contract's kill rule (round-71 contract.md, C2 kill rule; QUALITY criterion 14) makes that annotation `unprovable`. The counter does not implement its own kill rule.
- Freshness definition (AXES.md:14): "stale items flagged or fixed"; "re-verified against live surfaces". A phrase flags. Nothing re-verifies. `freshness-sweep.mjs:136` (PATH_RE = `~` and `/home/vgpnk` only) never scans `/tmp`, so the instrument behind the freshness row cannot see this move.
- Token coverage is complete: `grep -n '/tmp' SKILL.md` at base hits exactly the seven lines.

## 3. Axis harm (what the repairs touch; none exercised)

- **Operability 10.** C2 repoints SKILL.md:95, a runnable recipe (`cp … /tmp/probe-latest.backup.json → run → cp back`), to `$(mktemp -d)`. A restore step in a separate shell cannot find a fresh path. The counter never runs the recipe. C1 adds `## Planned — next round` with no claims, against the SCORECARD `planned` field (AXES.md:81, "1–3 claims"). No parser for `## Planned` found (grep of kake `scripts/` and fleet `scripts/` empty).
- **Freshness 10.** Sweep base is pre-existing red: `controls/sweep-offline-base.txt` → §paths DRIFT 1 (`~/projects`, corpus lessons only), `skipped(offline)`, exit 1. The sweep does not read SCORECARD, so C1 cannot move it. None of the seven SKILL.md lines is bound in `corpus/knowledge/freshness-sidecar.json` (25 SKILL entries, none at 27/95/227/356/359/463/464). Phrase annotations could mask neighbouring `~/` cites through the sweep's ±2-line absence window; base has no unannotated SKILL.md cite, so none is masked today. No tip run.
- **Calibration 2.** The C1 repair writes a new miscalibrated statement (3/14 plus revenger cause, see 1). Line 4770 keeps "4/14" in place; the correction line is appended at file tail, and the counter excludes correction lines from the stated population, so the contradicted statement stays uncorrected in place. Round-58 receipt chain (c58) not checked.

## 4. S132 and CORPUS.md rule 1

- Row exists: `corpus/SOURCES.md:140`, added in commit 297aa62d (round 44, 2026-10-23), status mined, used-by round-44 and SCORECARD.md. Rule 1's Gate duty applies to new rows; none is written in round 71.
- Teaching matches the source. Verbatim quote, kama line 7, 18 words: "not just against the current tip". Location: first paragraph under the heading.
- Not met yet: no round-71 lesson Gate exists (`corpus/lessons/round-71*` absent), so URL, access date 2026-11-03 and quote are not recorded. ScoutCalib's re-open is not landed (`w1/` holds only swarm-registry.json).
- Fit fails: S132's method is writing-revision checking, which C1 does not run (the counter reads `--revision` = tip only). Under S132, stale_planned is not an error (see 1). Tier A for a sibling lane's prose about its own counter is arguable. The kama file uses the same ID S132 for an unrelated llama.cpp row; cite the path, not the ID alone.

## 5. Amendment-1 (labrat → executor)

- Role change is grounded: `~/.agents/skills/swarm/SKILL.md:122-125` lists labrat as a frozen-topology seat, not a swarm role. Predicate sentence unchanged; `sha256` of contract.md and both counters equals freeze 04557e17 (checked with `git show 04557e17:…`).
- Falsified part: amendment-1 says controls are "byte-identical to the freeze commit", yet cites "J1-J3". Contract and amendment define two junk controls (delete planned headings; delete `/tmp` lines). J3 appears nowhere else in round-71 and is "a named residual probe, not a pass": undefined. Its result cannot be checked.
- Independence weakened: junk controls move from an adversarial labrat seat to an executor (same routing as the repair writers). Cosmetic for the predicates; real for the claim that controls are attacked before scoring.

## Recommendations (for the integrator; not applied)

1. Re-derive the attack-share conjunct under the round-70 amendment-0 definition (4/14, mismatch 0) or get an operator ruling. Drop the revenger cause and the 3/14 correction until ruled.
2. Require C1 repair 1 to be checked by the counter (heading must be Superseded) or drop the in-place rewrite for an appended correction, as round 29 did (SCORECARD round-29 corrections).
3. Add the `test -e` exit and an imperative-line check to C2, or make C2 `unprovable` on line 95.
4. Define J3 or strike it, and restate "controls byte-identical" accurately.

Commands and exits (all exercised in scratch, base bytes): `c71_calibration.py` base → exit 1 (matches `controls/c1-base.txt`); `c71_tmp.py` base → exit 1 (matches `controls/c2-base.txt`); harness F0–F4 and G0–G3 via `importlib` with `sys.dont_write_bytecode` (exit 0; per-fixture codes as above).
