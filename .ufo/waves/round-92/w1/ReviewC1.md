author: ReviewC1 (attack seat, reviewer, leaf)
round: kake 92
date: 2026-11-04
report: .ufo/waves/round-92/w1/ReviewC1.md
deliverable: .ufo/waves/round-92/w1/ReviewC1/Attack.md
fixtures: .ufo/waves/round-92/w1/ReviewC1/fixtures/
freeze: a5640ca02c20f94a0fa03af41b977b46ae99808e

# ReviewC1 — execution-side attack on the frozen C1 counter

VERDICT: C1 falsified — the frozen counter reads `met=true` (exit 0) on three
fixture classes that do none of the work the claim measures: a runner that
mutates nothing but prints per-target canned verdicts (class 3), a control
harness that echoes the nine frozen labels without running anything (class 5c),
and a counter blob edited after the pin with the pin re-written in the same
commit (class 6). Classes 1, 2, 4, 5a and 5b are refused, each by a shallow
form check.

## Scope and method

Work ran only in scratch fixtures cloned from the lane at the freeze revision
`a5640ca02c20f94a0fa03af41b977b46ae99808e` (`git clone -q --shared`, one clone,
`master` pinned to the lane master, `git rev-parse --show-toplevel` asserted
before every commit; fixture identity
`ReviewC1 fixture <reviewc1@fixture.invalid>`; no mutating git command ever
touched the lane). Scratch root `/fast/scratch/hyaku/kake-r92/ReviewC1/`, passed
as `--work` and `TMPDIR` on every counter run; the scratch directory was deleted
after the receipts were copied under
`.ufo/waves/round-92/w1/ReviewC1/fixtures/`. The measurement command for every
class is the frozen one:

    TMPDIR=$S/tmp python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-92/c92_defects.py \
        --root $S/clone --revision <fixture-rev> --work $S/w-<class>

Baseline at the freeze revision: `open=3 closed=0 battery=hit differential=fail
self=ok met=false`, exit 1 (`fixtures/base/counter-stdout.txt`), matching
`controls/base-c1.txt` in shape. The eight fixture rows, their revisions,
counter lines and exits are in `Attack.md` (table reproduced in
`fixtures/summary.tsv`).

## Falsifications (each is a `met=true` the work does not back)

**F1 — class 3, rev `a92bcede206c74c4696ee9e12f0355ab5b769360`, exit 0.** The
committed runner (`fixtures/c3/files/.ufo_waves_round-92_integration_mutate-tip.py`)
reads `--mutant`, prints `verdict=survived rc=0` for `base` and
`verdict=killed rc=1` for every mutant id, and never touches the gate. Item A
executes exactly two targets (`base` and `sorted(verdicts)[0]` = `M01`),
requires base to survive, the sampled verdict to equal the log line, and the two
to differ — all three hold for canned output. The detail shows the counter
executed the forgery and accepted it:
`"A_observed": {"M01": ["killed", 1], "base": ["survived", 0]}`. The K91-1
repair ("bind the receipt to an execution log") binds the log to ONE sampled
execution and that execution to nothing real: 19 of 20 log lines are never
checked against any run, and the checked run is itself forged. This is the
round-91 canned-runner class surviving its supposed closure.

**F2 — class 5c, rev `417f6583f9753602266bc43b4f3aaee452cd9df1`, exit 0.** The
committed control harness (`fixtures/c5c/files/.ufo_waves_round-92_controls_run_controls.sh`)
is nine `echo` lines and `exit 0`; item C closes because the replay's stdout
label set equals the frozen nine labels and the exit is 0. Two aggravations:

- The nine labels are public constants of the counter (`LABELS` in
  `c92_defects.py`), so echoing them requires no knowledge and no work.
- Mid-wave the honest labels are unproducible: the frozen harness replayed at
  the base reads LANE master, and my baseline run printed
  `carrier-open=2 carrier-met=false carrier-exit=1` (master `f0b2dc63` does not
  carry the artifacts yet). Item C therefore cannot close honestly before the
  carrier lands — every pre-landing `met=true` necessarily contains an unearned
  `carrier-met=true`. The K91-5 repair asserts the label SET, not that the
  replay ran the counters it claims to have run.

**F3 — class 6, rev `d7befad5c1daf1ffa2d7ea6100525515784d11b6`, exit 0.** Here
everything else is real: the runner (`fixtures/c6/files/mutate-tip-source.py`)
applies 20 distinct source mutations to the gate blob and really runs the mutated
gate (`--seed 92 --generated 10`); base survives, all 20 mutants are observed
killed (M01–M17 rc=2 `self_check` failures, M18–M20 rc=1 judge failures —
`fixtures/validation-transcript.txt`), and the receipt/log carry the observed
numbers with the correct gate digest `d7bca38e…64b65e`. The only forgeries are
the counter blob (a ~70-line successor that verifies nothing and always prints
`met=true` in normal mode) and `frozen/c1-self.sha256` re-written to the forged
blob's digest **in the same commit**. Both defects this exposes are in the
frozen instrument:

- *The self conjunct pins nothing.* The counter reads pin and blob both from
  `--revision` (`show(root, rev, SELF_PIN)`, `show(root, rev, SELF_PATH)`), so
  `self=ok` only certifies internal consistency of a commit the attacker fully
  controls. The executing canonical counter is never compared to the revision
  blob, and the pin is not anchored at the freeze revision.
- *The battery grades the successor by its own self-reports.* The battery runs
  `show(root, rev, SELF_PATH)` — the forged blob — against the five fixtures; a
  liar that recomputes the planted brokenness from the fixture bytes prints the
  declared exact open sets and `battery=exact` follows. The c6 detail is
  unambiguous: fixture FA's reason reads `"receipt digest 000000000000 != gate
  blob ffffffffffff"` — the forger's own string — where the canonical counter's
  reason for the same brokenness reads `gate blob d7bca38ec146`
  (`fixtures/c6/counter-stdout.txt` vs `fixtures/base/counter-stdout.txt`). The
  K91-4 "exact open set and reason substring" repair constrains what a lying
  successor must print; it does not make it measure.

## Refused classes (the counter's real discriminative power, and its shallowness)

- **Class 1** (fabricated receipt, correct digest `d7bca38e…`, `mutants=20
  killed=20 survivors=0 met=true`, no log): refused — `"execution log absent"`
  (`fixtures/c1/counter-stdout.txt`). The receipt alone no longer passes; the
  K91-1 first-line fix works only against receipts with no log at all.
- **Class 2** (20-line log, runner prints one identical canned line for base and
  mutant): refused — `"base and mutant runs do not differ (canned output)"`. The
  differ check is one bit on one sampled mutant; the argv-switch of class 3
  defeats it.
- **Class 4** (registry row naming the counter without `--revision`/`met`):
  refused — `"no registry row names c92_defects.py with its --revision command
  and met predicate"`. Note the check is a substring scan of one line: a row
  that adds the two tokens without a runnable command would pass (a wording
  row, not a behaviour row) — untested beyond class 4, reported as a limit.
- **Class 5a** (nine labels, wrong values, exit 0): refused — `"label set
  differs"`. **Class 5b** (correct labels, exit 7): refused — `"replay exit=7"`.
  Between them they leave exactly the class-5c hole: correct labels + exit 0 +
  no work.

## Routed defects (lane fixes; frozen bytes untouched by this seat)

- **R92-C1-a.** Item A's execution binding samples one mutant (`sorted first`)
  and verifies no mutation occurred. Route: bind the log to the runner by digest,
  require the runner to re-emit every id's observed verdict for comparison, and
  tie the verdict to a blob that provably differs from the gate (e.g. print the
  mutated blob's digest per id and have the counter re-derive it for the sample).
- **R92-C1-b.** Item C grades a printed label set. Route: have the counter
  re-derive base/carrier readings itself and compare them to the harness's
  labels, or grade the harness's own intermediate outputs; as frozen, item C
  cannot close honestly before the carrier lands, which every pre-landing
  `met=true` exploits.
- **R92-C1-c.** The self conjunct is commit-local and bypassable by any
  committer (pin rewritten beside the blob). Route: anchor the pin at the freeze
  revision (the counter already hardcodes `BASE`) or compare the revision blob
  to the executing counter's own digest.
- **R92-C1-d.** The battery executes the revision's counter blob, so a forged
  successor self-grades `battery=exact`. Route: grade the battery with the
  canonical counter while still requiring the successor to agree with it, or
  cross-check the successor's battery-mode and normal-mode outputs on identical
  bytes; as frozen, "battery=exact" is attainable by a ~70-line liar (shipped in
  `fixtures/c6/files/counter-liar-source.py`).
- **R92-C1-e (claim wording).** `freeze.md`'s C1 predicate says "the counter
  blob at `<REV>` equals its pinned digest", which reads as tamper-evidence; the
  implementation is revision-local self-consistency. The kill rule should say
  the pin travels with the blob, or the instrument should make it not travel.

## Honest limits

- Only the six assigned classes plus 5c were attempted; index-level forgeries
  (`git replace`, alternates tricks) were not attempted and are unknown.
- Class 4's refusal was not probed with a token-only row (row containing
  `--revision` and `met` but no runnable command); the substring scan suggests
  it would pass, but that is inference, not a measurement.
- The carrier labels are environment-dependent (they read the lane master at run
  time); my baseline numbers (`carrier-open=2`) hold for master `f0b2dc63`.
- All fixture work ran in the scratch clone; the lane received only this report,
  `Attack.md` and `fixtures/`. No tool was installed or upgraded (pacman
  untouched); scratch root deleted after the copy.

Evidence index: `Attack.md` (per-class table), `fixtures/<class>/` (counter
stdout+stderr, full fixture diff, commit metadata, extracted artifact bytes),
`fixtures/summary.tsv`, `fixtures/validation-transcript.txt`,
`fixtures/base/`.
