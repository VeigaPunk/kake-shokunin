# CriticC — round 80, w1: falsification of C1 and C2

**Verdict:** both claims are currently honest, red-at-base and red-at-worktree, and no do-nothing
control reaches either target — but C1 **was not a claim at all at freeze** (its counter could never
close R79-1; repaired post-freeze by amendment-2), the contract's junk-control sentence is
**contradicted by its own committed receipt** (R79-5 closes on words alone), and C2's written target
is **broader than its measurable predicate** (single-space asctime and amendment A5 are unenforced by
any counter). Smallest safe corrections listed at the end. Nothing edited; findings only.

Axes: C1 targets **calibration** (lane score 2, lowest non-retired); C2 targets **operability** (10).
Per the contract both claims move **evidence, not scalars** — as declared, so no axis-honesty
violation in the claim headers themselves (§5 below for the residual).

## 1. Do-nothing premise

**C1 — controls reproduce, junk control half-succeeds.** I re-ran the frozen counter at the base
revision and reproduced the receipt byte-for-byte (`open=6 met=false`, exit 1; my run vs
`controls/base-c80-defect-queue.txt`: identical 8 lines). But the frozen junk control does NOT do
what the contract says: contract §C1 kill rule says a words-only junk tree "must still report every
item open" and §Controls says it "must still print `open=6`", yet the committed receipt
`controls/ctl-c80-junk-queue.txt` (both at freeze bytes f20163c1 and as regenerated in the worktree)
prints **`R79-5 closed … open=5 closed=1`**. A junk tree that only writes a withdrawal row naming
R79-5 and quoting the sentence into a lesson file closes R79-5 — the sentence-absence scan is
vacuously true in any tree that lacks self-assessment files. Confirmed against the real tree: at base
the withdrawn sentence occurs in exactly one file, `corpus/lessons/round-79-verifier-spotcheck.md:170`
(`git grep` at 9998dc7a, rc=0), which is deliberately outside the scanned set, so on the real tree
too R79-5's closure reduces to "write the row". **Conjunct doing no work: R79-5** (half of it — the
absence scan — is real only if some scannable file ever carried the sentence; none does). The junk
control does not reach `met=true`, so the claim survives formally; the contract prose is what is
false.

**C1 — at freeze the counter made the claim unsatisfiable (proven by experiment).** The frozen
counter read the `used-by` cell at index 11 while `row_shape` rejects any row that is not exactly 11
cells, so for every shape-valid row `row[11]` was empty and R79-1 could never read `closed`. I
extracted the frozen bytes (`git show f20163c1:…c80_defect_queue.py`, 12593 bytes) and ran both
counters on an identical synthetic tree carrying a shape-valid S453 row whose used-by resolves:

```
FROZEN f20163c1: rc=1 R79-1 -> R79-1 open S453 used-by resolves to no file that cites S453
WORKTREE fixed : rc=1 R79-1 -> R79-1 closed S453 = RFC 9110 row present, used-by resolves …
```

The base control could not catch this (at base the row is absent, so the earlier branch fires) —
exactly as `amendments/amendment-2.md` argues. Amendment-2's fix (index 10 + a `--selftest`) is the
minimal repair and I verified its receipt `controls/ctl-c80-queue-selftest.txt` (3/3, exit 0). The
repair is legitimate — it makes the counter implement the *written* condition instead of an
impossible one — but it must be flagged: **the C1 claim only became a claim when the counter was
amended after freeze**, and the amendment + counter + two regenerated receipts are still uncommitted
in the worktree (`git status`: `M c80_defect_queue.py`, `M base-c80-defect-queue.txt`,
`M ctl-c80-junk-queue.txt`, `?? amendments/amendment-2.md`).

**C2 — do-nothing control is the base receipt and it holds.** The round-79 tool unchanged scores
`a2 wrong=10 met=false` (reproduced at `--revision 9998dc7a`, exit 1, matching
`controls/base-c80-a2.txt` line-for-line, including the two `C2v1` lines — the first is the inner
matrix summary echoed inside the truncated `detail:` field, not a second counter). The counter's
premise holds at base. One inventory defect: the contract §Controls names `ctl-c80-consts.txt` as
committed; **no such file exists** (controls/ holds `ctl-c80-junk-queue.txt` and
`ctl-c80-queue-selftest.txt` only). The constants conjunct itself works — both runs print
`constants=4/4+4/4` over the 4 files in `.ufo/waves/round-79/consts/` — so this is a frozen
prose/inventory mismatch, not a predicate hole.

## 2. Universal-clause audit

- **C1 R79-5 "no lane self-assessment file repeats it":** the counting command enumerates the full
  named set (5 named files + `corpus/knowledge/**/*.md` via rglob, and the same set exported under
  `--revision`). Enumeration complete; the weakness is not coverage, it is that the set is empty of
  the sentence at base (see §1).
- **C1 R79-8 "every seat whose output was empty":** full enumeration over all 14 seats of
  `.ufo/waves/round-79/w1-results.json`; population premise verified — exactly 2 empty seats
  (`CriticC`, `ExecC2Tool`, both 0 bytes, sha `e3b0c442…`), so the item is closable.
- **C1 R79-3 "prints the identical line":** the counter compares only the **last** `selftest: …`
  line (`c80_defect_queue.py:163-167`). If the tool printed multiple such lines the universal
  ("identical") would be checked on one line only. Currently the tool prints one; residual only.
- **C2 "accepts the date shapes its own source names":** the counting command enumerates only the
  31 frozen cases + 12 new cases. A2 explicitly accepts asctime with a **single-space** day field
  ("a single space is also accepted"); the case set scores asctime only at width two
  (`c34 = Sun Nov  6 …`, `c43 = Sun Nov 16 …`; confirmed over all 12 manifests). The tool may reject
  single-space asctime and still print `met=true`. A3's "never `xrt_unknown_directive`" for failing
  comma-bearing values is covered (c37), and "every other comma keeps the round-79 rule" is covered
  by c38/c39/c41/c42/c43.
- **C2 "four degenerate constants each fail on either set":** enumerated — `consts/` holds exactly
  4 files, counter requires `cf==cn==4` per run. Complete.

## 3. Causally separable? Asymmetrically

Four cells I ran (all exit 1):

| cell | C1 (`c80_defect_queue.py`) | C2 (`c80_measure.py`) |
|---|---|---|
| base rev 9998dc7a | `open=6 met=false` | `frozen_wrong=0 a2_wrong=10 met=false` |
| current worktree | `open=6 met=false` | `frozen_wrong=0 a2_wrong=10 met=false` (tool already modified, sha `720ea8a7…`, 20578 bytes) |

From the code: C2 reads only the tool bytes + frozen round-79 set + this round's set + consts — no
C1 artifact can touch it, so **C2 is independent of C1**. C1's R79-3 re-runs the tool's `--selftest`
and requires the receipt line to match, so **C1 reads C2's output bytes**: demonstrated live, the
tool's selftest line moved `selftest: 26/26 passed` (base) → `selftest: 33/33 passed` (worktree,
ExecGrammar mid-landing). Any `c80-selftest.txt` written before the tool settles makes C1 red at the
carrier with all six work items done. The contract's "causally separable" sentence is therefore
true only in one direction and only under a landing order where the R79-3 receipt is regenerated at
the measured tool bytes. The counter design (re-derive at measurement) already forces this; the
contract prose overstates separability.

## 4. Axis honesty

- C1 moves **evidence on calibration** (six filed report/receipt-accuracy defects to zero open), not
  the score — the contract says so explicitly ("a claim moves evidence, not a scalar"). Honest.
  Two items (R79-2 guard, R79-4 fixtures) add new verification tooling, which is operability-flavored
  work justified by a calibration defect; no misattribution.
- C2 moves **operability directly** (the lane-owned round-79 tool accepts the shapes its source
  names) while A4 pins the no-regression conjunct. Honest.
- Harm to axes the lane does not own: none available. Write scope is the lane; `git status` shows
  only lane files touched; round-79 artifacts frozen and untouched; the fleet root, `MANIFEST.json`,
  `.ufo/state/` etc. are not in any seat's write scope. The only self-harm vector found is
  evidence-manufacturability (junk control closing R79-5; self-graded scripts, §5), which would make
  calibration *evidence* weaker while claiming to strengthen it — the axis the claim targets.

## 5. Kill-rule adequacy

- **C1, most likely pass-while-false:** the two self-graded scripts. R79-2 runs
  `ledger_append_guard.py --selftest` and trusts its printed words, then trusts its `--json`; R79-4
  runs `c80_ledger_fixtures.py` and trusts its `killed=3` JSON. A guard or harness whose output is
  canned passes both items while verifying nothing. The predicate does **not** exclude this — unlike
  R79-3/R79-8 (where the counter independently re-derives) there is no external re-derivation of the
  scripts' honesty. Second path: the R79-5 words-closure above (already demonstrated by the round's
  own junk receipt). **Predicate excludes: no.**
- **C2, most likely pass-while-false:** a shared misreading — oracle and tool agree because
  `make_cases.py` and ExecGrammar read the same amendment sentence the same wrong way. The counter
  measures tool-vs-oracle agreement, never tool-vs-source; the S452 grounding is real (retained
  bytes line 1733 carry `Wed, 03 Dec 2025 13:09:53 GMT`) but no counter step re-consults S452/S453.
  Additionally A5 (selftest grows with the amendment) is enforced by **no counter at all**: nothing
  compares the selftest count against round-79's 26 — a tool that skips A5 entirely still prints
  `met=true` on both claims. **Predicate excludes: no** (both paths open).

## Smallest safe corrections (proposed, not applied)

1. Contract prose, one sentence: correct the junk-control claim from "must still print `open=6`" to
   what its receipt shows (`open=5`, R79-5 closes on words), or add to R79-5's closure condition an
   evidence-bearing conjunct; today the written contract is falsified by its own committed control.
2. Commit amendment-2 + the fixed counter + the two regenerated receipts (they are the only thing
   standing between C1 and unsatisfiability) — integration item for L1, not a seat.
3. Restore or drop `controls/ctl-c80-consts.txt` from the contract's control inventory (counter
   already enforces the conjunct; the prose names a file that does not exist).
4. Either narrow A2's written sentence to the tested two-space padding or accept, explicitly, that
   single-space asctime is outside the measurable claim (the frozen case set cannot grow).
5. Make A5 enforceable in C2's summary line (e.g. selftest count > 26 re-derived by the matrix) or
   mark it residual; today it is claim text with no counter.
6. Landing order note for the carrier: regenerate `controls/c80-selftest.txt` at the settled tool
   bytes (R79-3) — otherwise C1 fails *because* C2 landed.

Both counters also declare exit `2 unevaluable` in the contract; neither has a code-2 path (grep:
no `return 2` in either file) — dead spec, one line to fix in prose or code.

Commands run (all under scratch `/fast/scratch/hyaku/kake-r80/CriticC`, tree removed before yield):
C1 at `--revision 9998dc7a` (exit 1), C1 on worktree (exit 1), C2 at `--revision 9998dc7a` (exit 1),
C2 on worktree `--tool scripts/x_robots_tag_audit.py` (exit 1), frozen-vs-fixed counter on a
synthetic green-S453 tree (open/closed as quoted), tool `--selftest` base vs worktree (26/26 vs
33/33), `git grep` for the withdrawn sentence at base and in the worktree, manifest/oracle/consts/
receipt reads. No tools installed; pacman untouched.
