# ReviewC1 — round-96 seat report: attack on the frozen C1 counter

Seat: ReviewC1, kake round 96 (hyaku run 15, attempt 1), wave w1. Lane base
`bde9869144f69c5a459c0d2c93f5135922fe3a8d`. Target: the frozen
`.ufo/waves/round-96/c96_selfassess.py`, attacked with 13 distinct
synthetic-lane defect routes plus 8 process attacks. Deliverables:
`w1/ReviewC1/routes.md` (verdict line) and `w1/ReviewC1/receipts/runs/*`
(one receipt per run: command, rc, line 1, parsed findings). Scratch tree
deleted before this report was finalized (see Cleanup).

**Verdict line: `REVIEW-C1 refused=8
false-greens=RX01-decisions-only-in-html-comment,RX02-decisions-only-in-fenced-code,RX03b-entire-gate-inside-fence,RX09-subdir-roundno-hijack`**

## 1. Digest duty (done first; all verified, none amended)

`sha256sum` over the frozen instruments and both surfaces files
(`receipts/runs/_digests.txt`): c96_selfassess `a282da65…` = pin, c95_selfassess
`8fd27d62…` = frozen round-95 scoring instrument, c96_reval `ec40aec1…` = pin,
c96 surfaces `c1caa585…` = pin, c95 surfaces `00a04c9a…` = c95's embedded
`SURFACES_SHA`. Every attack below executed the lane's own frozen bytes; no
copy was patched, no control re-stamped.

## 2. Harness (fixture + control reproduction)

One fixture repo (`/fast/scratch/hyaku/kake-r96/ReviewC1/fx`) holding the full
base tree (`git archive bde98691…` extract, 367,636,480 bytes). Each route:
restore every previously touched path to base bytes → apply ONE defect overlay
→ assert `git rev-parse --show-toplevel` == the fixture → commit → score the
defect rev with both frozen counters via CLI
(`python3 -B <counter> --root <fixture> --revision <rev> --verdict-only`) and
with the frozen round-95 counter for predecessor liveness. Driver:
`receipts/runs/_driver.py`, `_pattacks.py`.

Control reproductions before any attack (reproduce, never re-stamp):

- `_repro-succ-full-base.txt`: c96 FULL mode at the fixture's base commit —
  line 1 field-identical to `controls/c1-successor-at-base.txt` except the
  `revision=` sha (fixture commit `6abf6e86…` vs lane base `bde98691…`; same
  tree, different repo). Equal fields include counter digest, lessons=90
  entries=83 rows=260 criteria=40, mismatches=0, pins=ok, battery=23/23,
  admit=5/5, shadow=absent, predecessor_admits=6/22, ng_pred_admits=3/3,
  met=true, rc=0.
- `_repro-pred-full-base.txt`: c95 FULL mode at the same commit —
  field-identical to `controls/base-c1-predecessor.txt` modulo `revision=`:
  mismatches=0, pins=identity, battery=20/20, admit=5/5,
  predecessor_admits=10/19, met=false, rc=1.

## 3. Findings by severity

### F1 — HIGH: subdir round-number hijack is a successor REGRESSION (false-green, route RX09)

A round-96 lesson filed one level deep at
`corpus/lessons/round-95/round-96.md` with a junk gate (two lorem lines, no
decision vocabulary) and a valid Mistakes table is **certified clean**:

- c96: `verdict=clean`, mismatches=0, pins=ok, rc=0
  (`receipts/runs/RX09-subdir-roundno-hijack.txt`).
- c95 on the SAME rev: **refuses**, E1 "vacuous Gate: no admit decision line
  (route R01)", rc=1 (`RX09-subdir-roundno-hijack__pred.txt`).

Root cause (read from the frozen bytes, unmodified): both counters derive
`round_no` from the FIRST `round-(\d+)` anywhere in the path; c95 guards its
decision check with `round_no >= 95`, c96's R95-5 class rule is guarded with
`round_no >= 96`. With the misfiled path the first match is `95`, so the
successor skips the check the predecessor performed. The lesson listing is
recursive (`git ls-tree -r`), so the subdir file is counted (lessons=91) and
audited — minus the rule. Fixture bytes at the rev:
`_fixture-rx09-lesson-at-rev.txt`. Route for a successor (not repaired here):
derive the round number from the basename (or the last match), or restrict
lessons to `corpus/lessons/*.md` at the top level.

### F2 — MEDIUM: decision tokens in non-prose carriers satisfy the E1 body rule (false-greens RX01, RX02, RX03b)

The R95-5 class rule requires whole-word admit/reject tokens in the Gate BODY;
it does not require that the body be decision prose, and `gate_sections`' regex
is fence-unaware. Three junk-gate shapes certify (`verdict=clean`, rc=0 each;
predecessor admits all three too, so these are open carrier channels, not
regressions):

- RX01: the only decision tokens live in an HTML comment
  (`<!-- decisions recorded here: admit X, reject Y -->`) — DECISION_RE reads
  comment text.
- RX02: the only decision tokens are fenced code sample lines inside the Gate
  body.
- RX03b: the lesson's ONLY `## Gate` heading is inside a quoted ``` fence;
  the regex treats the fence line as a real Gate heading and the fence's
  example admit/reject lines as its body — a lesson with no actual Gate
  section certifies. The mirrored refusal direction (RX03a: fence-carried
  heading + junk body) IS refused with the named E1 finding, so the
  heading-token rule itself holds even from a phantom fence heading.

### F3 — confirmed defenses (process attacks P1–P7, all PASS by receipt)

- PYTHONPATH shadow, cwd shadow, and effectful `subprocess.py` beside a
  counter COPY (copy digest-verified == frozen bytes before and after): the
  planted module never executed (no marker file), verdict normal (P1, P2, P3;
  R95-7's sys.path scrub + stdlib-origin check hold).
- `--surfaces-file` refused, exit 2 (P4, route R18).
- `--verdict-only` prints `met=n/a verdict=clean` and `met=true` appears
  nowhere in its output (P5; round-94 closure item honored).
- `--self-pin` wrong pin → rc=2 `self_pin=mismatch met=false` with
  expected/actual JSON; correct pin → rc=0 (P6).
- `--base-pins-json` with zeroed floors cannot green identity violations: the
  RX04 deletion rev still refuses with the entry presence pin under zeroed
  floors; the flag is inert on a clean state (P7). No cardinality backdoor on
  the real lane (identity pins are content/presence, independent of floors).

### F4 — residual (observed, not counted as a false-green): PATH git shim (P8)

A `git` shim earlier on PATH serving clean bytes for
`corpus/lessons/round-96.md` flips the RX01-defective rev to `verdict=clean`
rc=0. The counter never saw the defective bytes — it audited exactly the clean
content the shim served — so under the seat's definition this is not a
counter false-green, but it is the same trust family as F1e/R94-2 (module
shadow defense) where the analogous PATH-level shadow of the `git` binary is
undefended. Routed as a successor note; the frozen command's environment is
operator-trusted today.

### R95-5 liveness and R95-1 differential (the closures are real)

- The routed trio is live: c95 shows mismatches=0 on NG01r, NG08r and NG11a
  (its known false-greens) and refuses with the named E1 finding on all three
  under c96. My additional NG11 variants: NG11c (code-span substrings
  `admits_more`/`auto_rejected`, no whole word) refused by c96, predecessor
  admits; NG11b (`admin`/`rejector`) refused by BOTH counters — honestly
  recorded: that family never was a predecessor false-green (no "admit"
  substring anywhere), so there was nothing live to close there; c96's
  refusal is added strictness, not a regression.
- Presence pins (R95-1) do exactly what was routed: deletion fires the
  identity pin (`entry:<path>`, RX04, both counters refuse); an in-file head
  repair carrying `[r96-correction 2026-11-05]` does NOT fire under c96
  (RX05: pins=ok, identity empty, verdict=clean rc=0) while the same rev
  stays uncertifiable under c95 (`entry-content` identity pins). The declared
  E3 repair route is reachable under the frozen predicate; the round-95 trap
  (predicate forbidding its own repair) has not recurred.

## 4. Honesty block

- Every verdict above names its command and observed rc; every claim maps to a
  receipt file under `receipts/runs/`. An unrun check has not passed anywhere.
- Two driver iterations occurred: the first built an empty fixture (all runs
  rc=2 `unevaluable=missing-surface`); those receipts were destroyed and
  nothing from that run was integrated. All delivered receipts come from the
  fixed run (fixture populated with the full base tree).
- Route scoring used `--verdict-only` (the audit leg that decides
  clean/defective). Full-mode `met=true` on a defective lane was not exercised
  per route; the met predicate's other legs (battery 23/23, admit 5/5, shadow
  absent, predecessor floors) were reproduced at base and are defect-blind by
  construction (they run the counter's own synthetic fixtures).
- Findings F1–F2 are instrument observations routed to the successor per the
  freeze (attack the instruments, never patch them); no instrument byte was
  modified.

## 5. Scope, tooling, cleanup

- Writes: only `.ufo/waves/round-96/w1/ReviewC1{,.md,/}` in the lane plus
  `/fast/scratch/hyaku/kake-r96/ReviewC1/`. No mutating git/jj anywhere except
  the scratch fixture (toplevel asserted before every commit). No sysctls
  touched; none needed.
- Tooling: nothing installed or upgraded (pacman paused host-wide honored;
  system python3/git sufficient). One run-time note: the c95 full-mode
  reproduction loads its own round-94 predecessor module from the lane
  (predecessor_admits=10/19 reproduced, so the resolution worked unmodified).
- Cleanup: scratch tree `/fast/scratch/hyaku/kake-r96/ReviewC1/` deleted after
  receipts were copied into `w1/ReviewC1/receipts/runs/` (47 files: 13 route
  receipts + 13 predecessor receipts + harness/repro/digest/process/summary/
  driver/fixture evidence, including the exact driver scripts `_driver.py` /
  `_pattacks.py`). No scratch residue remains; if any is found, that is a
  defect of this seat and should be flagged against ReviewC1.
