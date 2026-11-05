# ReviewC1 — round-96 C1 counter attack (c96_selfassess.py, a282da65…)

Verdict line: **REVIEW-C1 refused=8 false-greens=RX01-decisions-only-in-html-comment,RX02-decisions-only-in-fenced-code,RX03b-entire-gate-inside-fence,RX09-subdir-roundno-hijack**

Digest duty (receipt `receipts/runs/_digests.txt`): `c96_selfassess.py`
`a282da65…` OK, `c95_selfassess.py` (frozen predecessor) `8fd27d62…` OK,
`c96_reval.py` `ec40aec1…` OK, c1-surfaces `c1caa585…` OK, c95 surfaces
`00a04c9a…` OK. All attacks ran against the frozen lane bytes; nothing
repaired, nothing re-stamped.

Method: ONE fixture repo in scratch (`/fast/scratch/hyaku/kake-r96/ReviewC1/fx`)
holding the full base tree (`bde9869144f69c5a…`, 367 MB archive extract);
each route = restore-all-touched-paths → apply one defect overlay → commit
(`git rev-parse --show-toplevel` asserted == fixture before every commit) →
score the defect rev with the FROZEN counters via CLI (`--root <fixture>
--revision <rev> --verdict-only`), then the same rev under the frozen
round-95 counter for predecessor liveness. Full-mode base reproductions first
(`receipts/runs/_repro-succ-full-base.txt`, `_repro-pred-full-base.txt`):
line-1 field-identical to the committed controls
(`controls/c1-successor-at-base.txt`, `controls/base-c1-predecessor.txt`)
modulo the `revision=` sha (fixture commit sha vs lane sha — different repos,
same tree; every other field equal: lessons=90 entries=83 rows=260
criteria=40, battery=23/23 admit=5/5 predecessor_admits=6/22 ng_pred_admits=3/3
met=true for the successor; mismatches=0 pins=identity met=false
predecessor_admits=10/19 for the predecessor).

## Refused (8) — NG closures are real

| route | c96 observation (rc) | named finding | c95 predecessor |
|---|---|---|---|
| NG01r-heading-over-junk-body | rc=1 verdict=failed | E1 "no whole-word admit decision line in the body (routes NG01/NG08/NG11)" | mismatches=0 (admits — false-green live) |
| NG08r-heading-decision-summary | rc=1 verdict=failed | same E1 | mismatches=0 (admits — live) |
| NG11a-substring-admittta-rejectable | rc=1 verdict=failed | same E1 | mismatches=0 (admits — live) |
| NG11b-substring-admin-rejector | rc=1 verdict=failed | same E1 | mismatches=1 E1 "no admit decision line" (predecessor already refuses this family; no predecessor false-green existed to close) |
| NG11c-substring-codespan-no-wholeword (`admits_more`/`auto_rejected` in code spans, no whole word) | rc=1 verdict=failed | same E1 | mismatches=0 (admits — live) |
| RX03a-phantom-gate-heading-in-fence (`## Gate — admit…` inside a fenced block, junk body) | rc=1 verdict=failed | same E1 (heading tokens never count, even from a fence) | mismatches=0 (admits — live) |
| RX04-entry-deleted-after-base | rc=1 verdict=failed pins=short+identity | identity `entry:corpus/knowledge/conditional-list-membership.md` — the PRESENCE pin fires on deletion | refuses (identity) |
| RX07-tokens-only-in-mistakes-section | rc=1 verdict=failed | E1 (vocabulary is Gate-body-scoped; Mistakes rows do not count) | E1 refuse (R01) |

Routed-trio liveness duty met: c95 shows mismatches=0 on NG01r, NG08r and
NG11a (`receipts/runs/*__pred.txt`), matching the freeze's differential
requirement.

## False-greens (4) — c96 prints verdict=clean (rc=0) on defective input

1. **RX09-subdir-roundno-hijack — successor REGRESSION vs predecessor
   (strongest finding).** A round-96 lesson filed one level deep at
   `corpus/lessons/round-95/round-96.md` with a junk gate is certified clean
   (`receipts/runs/RX09-subdir-roundno-hijack.txt`: mismatches=0 pins=ok
   verdict=clean rc=0) because both counters derive `round_no` from the FIRST
   `round-(\d+)` in the path (→ 95), and c96's vocabulary rule is guarded by
   `round_no >= 96`. The frozen predecessor on the SAME rev REFUSES with E1
   (`__pred.txt`: "vacuous Gate: no admit decision line (route R01)", its
   guard is `>= 95`). The R95-5 class rule is thereby strictly weaker than
   what it replaced on misfiled paths. Fixture bytes:
   `_fixture-rx09-lesson-at-rev.txt`.
2. **RX01-decisions-only-in-html-comment** — `<!-- decisions recorded here:
   admit X, reject Y -->` over a no-decisions prose line satisfies the
   whole-word body rule (DECISION_RE scans comment text); verdict=clean rc=0.
   Predecessor admits too (not a regression; the carrier channel was simply
   never closed).
3. **RX02-decisions-only-in-fenced-code** — decision tokens as fenced code
   sample lines certify a decision-free gate; verdict=clean rc=0. Same
   carrier-channel class as RX01.
4. **RX03b-entire-gate-inside-fence** — the gate_sections regex is
   fence-unaware: a lesson whose ONLY `## Gate` heading is a quoted example
   inside a ``` fence is treated as a real Gate, and the fence's example
   admit/reject lines are read as its body → verdict=clean rc=0 on a lesson
   with no actual Gate section. Predecessor admits too.

## R95-1 differential confirmed (RX05 — must NOT fire, and it did not)

`corpus/knowledge/conditional-list-membership.md` head repaired in file with a
`[r96-correction 2026-11-05]` tag (`_fixture` overlay in driver): c96 →
pins=ok, mismatches=0, identity empty, verdict=clean rc=0
(`RX05-entry-head-correction-must-not-fire.txt`) — the declared repair route
is reachable. Same rev under c95 → `entry-content` identity pins (predecessor
still uncertifiable). Presence-pinning is real, live, and does exactly what
R95-1 routed.

## Process attacks (`receipts/runs/P*.txt`)

- P1 PYTHONPATH shadow (effectful `subprocess.py` on PYTHONPATH, non-script
  dir): marker NOT written, verdict normal (rc=0). `__pycache__` aside, the
  scrub holds.
- P2 cwd shadow: marker NOT written, rc=0.
- P3 effectful `subprocess.py` beside a counter COPY (copy sha-verified ==
  frozen bytes before and after): marker NOT written, rc=0, copy unmodified.
- P4 `--surfaces-file`: refused, exit 2.
- P5 `--verdict-only` on a clean state: prints `met=n/a verdict=clean`, and
  `met=true` appears nowhere in stdout.
- P6 `--self-pin 000…0` → rc=2, line "self_pin=mismatch met=false" with
  expected/actual JSON; correct pin → rc=0 normal verdict. PASS.
- P7 `--base-pins-json` zeroed floors: on the RX04 deletion rev the identity
  pin still fires (rc=1 verdict=failed pins=identity, entry pin present) — no
  cardinality backdoor; on the clean base rev the flag is inert (rc=0 clean).
- P8 git shim on PATH serving clean bytes for the defective lesson →
  verdict=clean rc=0 on the RX01-defective rev. Environment-trust residual:
  the counter audited clean bytes as served by a lying `git`; the defective
  tree was never seen. Same trust family as F1e/R94-2 (module shadows) which
  the counter defends, but PATH-shim shadows of the `git` binary are
  undefended. NOT counted in the false-green tally (the counter's own view
  was clean); routed as a successor hardening note.

## Honesty / verification status

- Every verdict line above names its command (in the receipt header) and its
  observed rc; nothing is claimed from an unrun check.
- Two driver iterations occurred: the first run built an empty fixture and
  produced only rc=2 unevaluable outputs; those receipts were destroyed
  unfixed-nothing was integrated from them. The committed receipts all come
  from the fixed run.
- Route scoring used `--verdict-only` (audit leg). Full-mode `met=true` on a
  defective lane was not exercised per-route; the met predicate is a
  conjunction whose remaining legs (battery/selftest/predecessor diff) are
  revision-independent of the defect and were reproduced at base
  (`_repro-*-full-base.txt`).
- No tools were installed or upgraded (pacman paused host-wide; python3/git
  already present were sufficient). No lane file outside
  `.ufo/waves/round-96/w1/ReviewC1*` was written; no mutating git/jj command
  touched anything but the scratch fixture.

Per-run receipts: `receipts/runs/` (routes `*.txt` + predecessor `*__pred.txt`,
harness `_harness-*`, reproductions `_repro-*`, digests `_digests.txt`,
process `P1–P8`, summaries `_summary_routes.json`/`_summary_process.json`,
driver code `_driver.py`/`_pattacks.py`, fixture evidence `_fixture-*.txt`).
Full analysis: `../../ReviewC1.md` (seat report).
