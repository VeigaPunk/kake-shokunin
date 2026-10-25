# ReviewQualityCriterion — round-46 residual attack

- wave: `kake-r46-residual` (seat `ReviewQualityCriterion`, role reviewer) · lane: `kake-shokunin`
- base `7cdbaefd3ecbbc8814eca1f013fcee101a6157b0` · build `ee43e66367bf23e386ff29029b9ea60515efd9d1` · lane tip `861113eb0eea4d51bd0614c542aa6ecb7cc9a843`
- claim under attack: **C2 criterion-leg correction** — frozen broad grep 2→3 vs the "sealed" narrow 0→1
- method: read-only over the lane — committed bytes via `git show <rev>:<path>`, the committed gate `scripts/citation_lint.py` run against committed revisions, and read-only file greps. No lane mutation (jj/git index, `.ufo/state`, `.ufo/watchdog.log` untouched), no sibling lanes touched, no installs. Scratch: `/fast/scratch/hyaku/kake-r46-residual/ReviewQualityCriterion/repro.txt`.

## Assigned checks — result

| Check | Result | Evidence |
|---|---|---|
| Narrow counter fails at base | **PASS** | `grep -c '^- \*\*Receipt identity for filed counts' corpus/QUALITY.md` → base `0`, build `1`, tip `1` (bytes via `git show`). The only matching line is the round-46 bullet added in `ee43e66` (`corpus/QUALITY.md:1071`). |
| A do-nothing round cannot satisfy the narrow counter | **PASS** | A round that changes nothing leaves the count at `0`; the base state is a real red state. |
| Frozen broad leg re-derives | **PASS** | `grep -c '^- .*receipt.*\(path\|sha256\)' corpus/QUALITY.md` → base `2`, build `3`, tip `3`, matching `verification/quality-broad-base.txt` (`2`) and `-tip.txt` (`3`). |
| Falsified frozen leg reported NOT MET | **PASS at leg level** | `LOG.md:1781` "C2 criterion leg NOT MET as declared"; team report (fleet) `.ufo/reports/round-46/kake.md:30` "**falsified as declared**, reported NOT MET"; `corpus/lessons/round-46.md:5-21` Mistake 1. |
| Not silently re-pinned | **PASS for the frozen text** | The declaration block at the tip still names the broad grep (`SCORECARD.md:3885-3892`); `git diff bd86ee8 861113e -- SCORECARD.md LOG.md` has no content deletions; the correction is disclosed in the verdict row, LOG, lesson and closure. Two labels overstate the correction — F1, F2. |

The specific attack fails in the good direction: the lane did not launder the falsified leg, and the narrow red state is genuine. The findings below are qualification defects around an honestly disclosed falsification, not a fabricated red state.

## Findings

### F1 — Medium — claim-level `PARTLY MET as declared` contradicts the lane's own conjunctive rule

`SCORECARD.md:3907` labels C2 "**PARTLY MET as declared**: gate legs MET; the criterion's frozen counting command falsified (base 2, not 0)". The frozen C2 sentence (`SCORECARD.md:3885-3892`) is one conjunctive predicate with three clauses: the gate resolves/reports; the gate exits 1 at base and 0 at the tip with every base violation repaired or adjudicated; and `corpus/QUALITY.md` carries the criterion, counting the broad grep `0 → 1`. The third clause is false at both ends (2 at base, 3 at tip).

The lane's own precedent for exactly this shape is `SCORECARD.md:3767`: "**Verdict: NOT MET as declared** (conjunctive MET fails on leg (c)); legs (a) and (b) verify", and `SCORECARD.md:3771`: "**Round verdict.** Both claims NOT MET as declared". `PARTLY MET` is a new category — it occurs once in `SCORECARD.md` (line 3907) and nowhere in `LOG.md`, the lessons, or the prior rounds. The frozen declaration never defined partial credit, and `SCORECARD.md:3742` records the lane's own rule "No post-hoc narrowing".

This is not score inflation — freshness is scored 10→10 (HOLD), and the report/LOG/lesson are more honest than the SCORECARD row, splitting the claim and labelling the criterion leg NOT MET. It is a verdict-label defect: under the lane's stated rule, C2 is **NOT MET as declared**. Fix: append-only relabel of the C2 verdict cell, or define partial-verdict semantics in a future freeze before any use.

### F2 — Low — the "sealed" narrow counter is not sealed in the lane's established sense

The freeze commit `bd86ee8` (2026-10-24T01:46:07-03:00) contains no narrow counter string: the frozen sentence names only the broad grep. The narrow command first appears in the build commit `ee43e66` (03:03:40) as a wave-1 artifact — `.ufo/waves/round-46/drafts/quality-criterion.md:10`, `.ufo/waves/round-46/w1/ExecQualityCriterion.md:16`, then `LOG.md:1783`, `SCORECARD.md:3907`, `corpus/lessons/round-46.md:16`. The seat that authored it had already measured the base and rejected the broad expression: `w1/ExecQualityCriterion.md` records `corpus_marker=0`, `broad_corpus=2`, "**FAIL** for the broad expression's claimed current 0 → 1 shape", and `w1/ReviewLessonQuality.md:139-160` recommends either "`2 → 3` for one appended criterion row, or the unique label the sibling draft chose".

Two things are true and one is not:
- The narrow red state was **pre-measured before integration** by an attack seat (`corpus_marker=0`), so it is not a counter chosen after the after-value was known — it is pre-registration by draft, and the closure re-derived it.
- It is **not sealed** in the lane's established sense. The lane's sealed counters are committed artifacts with pinned digests/key revisions (e.g. `c46_matrix.py`, sha256 `7335b001…b102164` pinned inside the C1 receipts; `sealed_count.py` with `key-revision`). The narrow counter has no committed counter file, no pinned sha256, and no receipt under `verification/`; its only filed evidence is prose in `SCORECARD.md`/`LOG.md`/the lesson plus the closure's re-run (`corpus/lessons/round-46-verifier-spotcheck.md:40`).
- The lesson's supporting sentence is misaligned: "every round-46 counter was measured at base before any after-claim (c1-before/c2-before receipts in `verification/`)" does not cover the narrow counter (its base has no receipt; the base measurement lives in the wave-1 draft), and "the fix is shown able to fail — the frozen broad command still reads 2 → 3" shows the *falsified* command persisting, not the narrow counter failing. The narrow counter's failure at base is real (0), but that sentence does not show it.

Accurate label: "pre-registered narrow counter (wave-1 draft, base 0 measured pre-integration)", not "sealed". The numbers stand; the adjective borrows a freeze-time authority the counter never had.

### F3 — Medium — the C2 do-nothing control the frozen declaration requires was never built or scored, and the verdict does not disclose it

Frozen requirement: `SCORECARD.md:3892` "Do-nothing control: gate absent / always-exit-0 stub must be scored and rejected." Evidence of non-execution:

- No `always0.py` exists at any revision: `git ls-tree -r --name-only 861113e | grep -i always0` → absent; `.ufo/waves/round-46/controls/` contains only the C1 `placebo.py` (the C1 do-nothing control); the C1 fixtures carry `fixtures/controls/{do_nothing,constant_clean,junk_accept}.py`, the C2 claim has no counterpart.
- The C2 receipts have no controls section: `jq keys .ufo/waves/round-46/verification/c2-after-ee43e66.json` → `adjudicated, adjudications, population, revision, verdict, version, violations` (the C1 receipt by contrast has a `controls` object with `do_nothing`, `constant`, `junk`, each `accepted:false`).
- The seat tasked to re-score it (`ReviewAlways0Control`, `.ufo/waves/round-46/w46-spec.json`: "Independently re-score the C2 always-0 control: at base bytes it must be shown unable to reach the after-state…") returned no report: `w1/` holds 12 `.md` reports, none for it, and `w1/swarm-registry.json` lists it with `agentId: null`.

The base leg (exit 1 with 28 named violations at `7cdbaefd`) would reject an always-exit-0 stub **if it were scored** — so the semantics are indirectly covered and the oracle is not blind to a constant-clean gate. But the declaration requires the control to be scored and rejected, no such score exists, and `PARTLY MET` / "gate legs MET" does not record the omission. Fix: land and score `controls/always0.py` at the base stage, or append a disclosure that the declared control was not exercised and the base leg is being used as its substitute.

### F4 — Medium — the round's filed verdicts violate the receipt-identity criterion the round itself adds

`corpus/QUALITY.md:1071` (added at `ee43e66`): "**Receipt identity for filed counts (round 46).** Any filed count or verdict against a receipt cites that receipt's path + sha256; a receipt citation without sha256 violates this criterion." The round-46 verdict rows cite receipts by path only:

- `SCORECARD.md:3906` (C1) cites `verification/c1-before-7cdbaefd.json`, `verification/c1-after-ee43e66.json` — no sha256 in the citation.
- `SCORECARD.md:3907` (C2) cites `verification/c2-before-7cdbaefd.json`, `verification/c2-after-ee43e66.json`, and `verification/quality-broad-{base,tip}.txt` — no sha256 in the citation.
- The round-46 SCORECARD section contains **no sha256 value at all**; the three matching lines are the criterion description and the two frozen sentences (`grep -n sha256` over `## Round 46`).
- The C2 receipts carry no sha256 field (keys above), unlike the C1 receipts which pin `tool.sha256` and `counter.sha256`; `quality-broad-base.txt`/`-tip.txt` contain only `2`/`3`, with no revision or hash binding.

So the correction's own evidence cannot satisfy the criterion the correction introduces, and the C2 gate's measured bytes are not pinned by sha256 in the filed evidence (revision-bound only, `ee43e66`). The criterion's plain reading binds this round's filed verdicts; if a future-only scope was intended, the bullet does not say so. Hashes an append would need (my derivation, from committed bytes):

```
c1-before  5f438e14ba72fa00e51cd6deb84cedf76a110b903a6b82ba2ea7f10df2d05b8c
c1-after   8c8d9521b3ddc45f9719ddb13ffdb1468e6662c94c59b246d5dcf2b75a7c90c0
c2-before  bdb88eca0a293eefd9c3343aeb9e5914b80eefb8b9840e9c53bee363bfe4b4f7
c2-after   1d9a5a23f1ffa1ded728f3e6867e6964570251890b136a2906a5592873c085f9
broad-base 53c234e5e8472b6ac51c1ae1cab3fe06fad053beb8ebfd8977b010655bfdd3c3
broad-tip  1121cfccd5913f0a63fec40a6ffd44ea64f9dc135c66634ba001d10bcf4302a2
```

Overlap note: peer `ReviewReceiptIdentity` owns the broad receipt-identity attack; this is its criterion-leg instance (the correction's own `quality-broad-*` evidence and the C2 receipts).

### F5 — Low — the after gate receipt is bound to the build commit, not the tip the frozen predicate names

The frozen predicate says the gate "exits 0 at the round-46 tip". The filed after receipt names revision `ee43e66…` (the build), while the lane tip is `861113eb…`. I ran the committed gate at the tip: `exit 0`, `0` violations, `30` adjudicated — identical to the build run. The clause is therefore true; the receipt identity is not bound to the tip. The closure did not execute the gate at the tip ("closure verified the committed receipts instead of executing the lane's gate", `corpus/lessons/round-46-verifier-spotcheck.md`), so the tip leg rests on this re-run. Fix: re-file the after receipt at `861113eb…` (or cite the reproducible tip run) under the criterion the round adds (F4).

### F6 — Informational — the narrow counter is a literal-presence check

`grep -c '^- \*\*Receipt identity for filed counts' corpus/QUALITY.md` counts the exact heading. It fails at base (0) and cannot be satisfied by a round that changes nothing — what the assignment asks — but it also cannot distinguish a substantive criterion entry from a cosmetic line with the same heading, and it cannot fail at tip short of deleting the deliverable. Enforcement of what the bullet says (receipt citations actually carrying sha256) is untested, and F4 shows the round's own filings would fail it. This is inherent to documentation counters; record as residual risk, not as a pass.

## Reproduced measurements

| Measurement | Command | Output |
|---|---|---|
| Frozen broad, base | `git show 7cdbaefd:corpus/QUALITY.md \| grep -c '^- .*receipt.*\(path\|sha256\)'` | `2` |
| Frozen broad, build | same at `ee43e66` | `3` |
| Frozen broad, tip | same at `861113e` | `3` |
| Narrow, base | `git show 7cdbaefd:corpus/QUALITY.md \| grep -c '^- \*\*Receipt identity for filed counts'` | `0` |
| Narrow, build | same at `ee43e66` | `1` |
| Narrow, tip | same at `861113e` | `1` |
| QUALITY.md sha256, base | `sha256sum` over the shown bytes | `0efca0973073cae58e130f7ea52bafd101914319f0727f1261a656ad04863504` |
| QUALITY.md sha256, build/tip | idem | `7d4d580188f51d45a625c6802fe3d81d4d04e48ab2f7257110df7273de1e6f4e` |
| Gate, base | `python3 -B scripts/citation_lint.py --root . --revision 7cdbaefd…` | exit `1`; `failed-policy`; 28 violations / 17 unique tokens / 0 adjudicated |
| Gate, build | same at `ee43e66…` | exit `0`; `clean`; 0 violations / 30 adjudicated |
| Gate, tip | same at `861113eb…` | exit `0`; `clean`; 0 violations / 30 adjudicated |
| Freeze commit | `git show --stat bd86ee8` | LOG + SCORECARD + lesson skeleton only; no narrow string |
| Freeze→tip diff | `git diff bd86ee8 861113e -- SCORECARD.md LOG.md` | no content deletions; frozen C2 sentence still names the broad grep |

## Residual risk and verification gaps

- The lane's selftests (`redirect_audit.py` 23/23, `citation_lint.py` 8/8) exist only as prose; I did not re-run them (verifier routed R2). Out of scope for this seat.
- The C2 adjudication ledger is described as "12 rows" in `SCORECARD.md:3912`; the ledger has 20 data rows at the tip (`grep -c '^| `'` over `git show 861113e:corpus/quality/citation-adjudications.md` = 20). Adjacent to F4 (a filed count that is wrong); already routed as defect R3 by the closure, and the working tree's round-47 correction block in `LOG.md` records the 20-row population. Not re-filed here.
- Neither C2 nor C1 has a gate-registry row in `SKILL.md` (closure R1). Out of scope.
- The C2 always-0 control cannot be verified because no artifact exists (F3).
- The narrow counter has no committed receipt; my numbers are re-derived from `git show <rev>:corpus/QUALITY.md` + `grep` and reproduce the closure's re-run.
- The lane working tree is concurrently edited by the round-47 wave (at review time `jj diff --stat` showed `LOG.md`, `SKILL.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/quality/citation-adjudications.md` modified against `cd42e3c`). Every authoritative count above is from committed round-46 bytes (`git show <rev>`); the working-tree cross-check of the two counters also read 1/3 at review time. I did not touch those files. The lane's jj state, git index, `.ufo/state`, `.ufo/watchdog.log`, and sibling lanes were not touched. No tools were installed or updated; no pacman. Only files written: this report and the scratch repro.

## Evidence index

- `SCORECARD.md:3885-3892` frozen C2 sentence + do-nothing control requirement
- `SCORECARD.md:3906-3907` round-46 C1/C2 verdict rows ("PARTLY MET")
- `SCORECARD.md:3767,3771,3742` lane's r45 conjunctive rule / round verdict / no-post-hoc-narrowing rule
- `LOG.md:1781-1784` round-46 C2 criterion-leg NOT MET entry
- `corpus/lessons/round-46.md:5-21` Mistake 1 (frozen-counter base never measured; narrow correction)
- `corpus/lessons/round-46-verifier-spotcheck.md:40` closure re-derivation of both legs
- `corpus/QUALITY.md:1071` receipt-identity criterion added this round
- `corpus/quality/citation-adjudications.md` ledger (20 data rows)
- `.ufo/waves/round-46/verification/c2-before-7cdbaefd.json`, `c2-after-ee43e66.json`, `quality-broad-base.txt`, `quality-broad-tip.txt`
- `.ufo/waves/round-46/drafts/quality-criterion.md:10` narrow counter, first committed occurrence
- `.ufo/waves/round-46/w1/ExecQualityCriterion.md` `broad_corpus=2`, "FAIL for the broad expression's claimed current 0 → 1 shape"
- `.ufo/waves/round-46/w1/ReviewLessonQuality.md:139-160` recommendation of `2 → 3` or the unique label
- `.ufo/waves/round-46/w46-spec.json` `ReviewAlways0Control` (no report; registry `agentId: null`)
- `.ufo/waves/round-46/controls/placebo.py` only control artifact present (C1)
- Team report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-46/kake.md:28-30` (fleet repo)
- Scratch repro: `/fast/scratch/hyaku/kake-r46-residual/ReviewQualityCriterion/repro.txt`
