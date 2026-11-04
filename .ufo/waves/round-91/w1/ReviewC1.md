# ReviewC1 — attack on C1 (round-91 calibration claim)

VERDICT: C1 reproduces as measured (base `open=3 met=false`; tip `open=1 met=false`, only B open) but the frozen counter is forgeable: `met=true` is reached with one fabricated receipt file (a2), with a script that prints success (c), and with a junk successor counter (e2). The R90-C repair is guarded only by a regex that a one-token respelling evades (f). C1 as frozen does not measure calibration; a do-nothing lane that commits one fake file scores 3/3.

Scope: read-only on the lane (`git show`, `ls-tree`, `rev-parse`, `status --porcelain`, `show`); every fixture is `git clone -q --shared` of the lane into scratch, detached at tip `f4fff130`, with a `--show-toplevel` assertion before its first commit (identity `ReviewC1`). The frozen counter was run with `python3 -B`. No lane file, no commit, no install. Scratch deleted; receipts under `w1/ReviewC1/`.

Hashes (`w1/ReviewC1/hashes.txt`): `c91_defects.py` 5239c7f8… (= freeze); `c2-contract.md` faa91e09… (= freeze); tip gate blob d7bca38e… (`scripts/cache_key_conformance.py`); tip `run_controls.sh` 00e339b8… (= freeze's stated script sha, the re-pointed file); base `run_controls.sh` c893a72d….

## Item-by-item, re-derived without the counter's prose

**Base 5b20af16 (do-nothing).** `python3 -B .ufo/waves/round-91/c91_defects.py --root <LANE> --revision 5b20af16661040f383e9e84f85b838619857cb14 --work <S>/w-base` → exit 1, `C1v91 … open=3 closed=0 met=false`. Reasons: A "successor counter not tracked at the revision" (`git ls-tree` at base lists no `c91_defects.py`); B "mutation receipt absent" (no `integration/mutation-tip.txt` at base); C "line 49 still copies the lane-root baseclean.out". Hand check: `git show 5b20af16:…/run_controls.sh | sed -n 49p` → `mkdir -p "$D/.ufo/waves/round-90/inherited"; cp "$LANE/baseclean.out" "$D/.ufo/waves/round-90/inherited/"`, and the base script hardcodes `LANE=/home/vgpnk/Projects/shokunin/kake-shokunin` (no `${LANE:-…}`). Receipt: `w1/ReviewC1/fixtures/base-run.txt`. Matches freeze "Before (base)".

**Tip f4fff130 (pre-data).** Same command with `--revision f4fff130…` → exit 1, `open=1 closed=2 met=false`, `open_items=["B"]`, reason "mutation receipt absent". A: tracked; selftest rc 0 `selftest 6/6`; battery FA→[B], FB→[B], FC→[C], FD→[] rc 0 (matches the frozen expectations). C: replay `controls ok 9/9`. B: `git show HEAD:.ufo/waves/round-91/integration/mutation-tip.txt` → "does not exist in HEAD"; `integration/` is an empty directory. Receipt: `w1/ReviewC1/fixtures/tip-run.txt`. The orchestrator's `controls/freeze-state-c1.txt` shows the same reading.

So at the tip the only open item is B, and B is the only item that is calibration work (a mutation score for the gate). Items A and C are already closed by committed bytes before any data.

## Forgeries (each in a fixture clone at tip; the frozen counter reads committed bytes)

- **(a) stale digest, right numbers** — `forge.py a`: receipt `gate_sha256=2840f32e… mutants=21 killed=20 survivors=1 met=true` + 21 `M%02d` lines. Reading: **refused**, exit 1, B open, reason "receipt digest 2840f32e5331 != tip gate blob d7bca38ec146". Receipt `fixtures/forge-a.txt`.

- **(a2) correct digest, fabricated lines, no execution (tip + one commit)** — `forge.py a2`: receipt `gate_sha256=d7bca38e… mutants=21 killed=20 survivors=1 met=true` + 21 invented lines `M01 forged line 1` …. Reading: **FORGERY ACCEPTED**: exit 0, `open=0 closed=3 met=true`, `B_mutants_listed=21`. B checks only the first-line form, the digest against the gate blob, `N>=20`, `K>=18`, `S==N-K`, and that N distinct `^M\d{2} ` tokens exist. Nothing ties the lines to any execution (no run log, no mutant list digest, no harness re-run). This is the round-90 "receipt with no execution" class, not closed. Receipt `fixtures/forge-a2.txt`.

- **(b1) case-variant key `GATE_SHA256=`** — `forge.py b1`: **refused**, B open, "receipt first line not in the frozen form". `fixtures/forge-b1.txt`.

- **(b2) `Killed=20/20` token** — `forge.py b2`: **refused**, B open, same reason. `fixtures/forge-b2.txt`. Note: refusal here is strict-regex form matching only; any content with the exact form is accepted (see a2).

- **(c) script prints `controls ok 9/9`, exits 0, runs nothing** — `forge.py c`: fake `run_controls.sh` with `LANE=${LANE:-…}` and the relocated path on two comment lines, then `echo "controls ok 9/9"; exit 0`. Reading: **FORGERY ACCEPTED**, `open=0 closed=3 met=true`, `C_tail=controls ok 9/9`. C's static checks read raw text (comments count), and the replay trusts the summary line plus exit code. `fixtures/forge-c.txt`.

- **(d) genuinely broken script (prints `controls ok 4/9`, exits 1) with a receipt file claiming `exit=0`** — `forge.py d`: **refused**, C open, "replay exit=1". The `exit=0` claim file is read by no item of the counter, so that half of (d) is inert. `fixtures/forge-d.txt`.

- **(e1) empty `c91_defects.py` at the path** — `forge.py e1`: **refused**, A open, "successor counter selftest: rc=0 ''". `fixtures/forge-e1.txt`.

- **(e2) junk successor counter** (its `--selftest` prints `selftest 6/6` and exits 0; its normal mode keys on the fixture commit subject containing `FD`/`positive`, reports all three items open otherwise) — `forge.py e2`: **FORGERY ACCEPTED**, `open=0 closed=3 met=true`. The battery reads FA/FB/FC as "B/B/C open" and FD as "[]" and passes A. A's battery grades the successor by its own self-reports, not by an independent oracle. `fixtures/forge-e2.txt`.

- **(e3) control: always-open junk successor** — `forge.py e3`: A open, "positive fixture not met". So the battery does discriminate an always-open counter. `fixtures/forge-e3.txt`.

- **(f) regex evasion in a negative control** — `fx-f.py`: tip script with the D1a line (line 73) changed from `cp "$LANE/$INHERITED"` to `cp "${LANE}"/baseclean.out`. The frozen item-C regex `"\$LANE"/baseclean\.out|\$\{LANE\}/baseclean\.out|\$LANE/baseclean\.out` does not match it. Reading: **FORGERY ACCEPTED**, `open=0 closed=3 met=true`. Hand replay (`LANE=<fx> ONLY=c1 bash run_controls.sh`, `replay-f/`): exit 0, last line `controls ok 9/9`, zero `MISMATCH`, and stderr shows `cp: cannot stat '…/baseclean.out'` and `fatal: pathspec '.ufo/waves/round-90/inherited/baseclean.out' did not match`. The D1a control expects `met=false`, and a missing file also reads open, so the replay cannot see a broken copy in a negative control. Only the positive fixture's copy is guarded by the replay; the regex is the only guard for D1a. The frozen predicate says "never the bare lane-root copy", and this line is one. Receipts `fixtures/forge-f.txt`, `replay-f/*`.

## Battery isolation (item 3)

- **Membership, not exact set.** `item_a` checks `items[0] not in got` for FA/FB/FC, so a fixture passes if its item is open alongside any other item. The battery therefore cannot tell "refused on its own item" from "refused on several". e2 shows the consequence: a successor that opens everything but FD passes.
- **FC is refused for the wrong reason.** `battery-reasons.txt` (run by calling the frozen builder in-process from the lane file with `dont_write_bytecode`): `FA B=False (receipt digest 2840f32e5331 != tip gate blob d7bca38ec146) C=True`; `FB B=False (receipt first line not in the frozen form) C=True`; `FC B=True C=False (script copies the relocated file fewer than twice)`; `FD B=True C=True`. The FC fake body contains no reference to `inherited/baseclean.out`, so C is refused by the static line-count pre-check and **the replay never runs for FC**. Nothing in the battery shows the replay catching a script that prints success and exits 3.
- **FD is real only in part.** The positive fixture's receipt is written by `make_fixture` itself (`fixture mutant %d` lines, digest copied from the gate blob). FD therefore proves only that the counter accepts its own fabricated receipt, which is exactly a2. FD is real for C (the actual `run_controls.sh` is replayed) and for A (the counter's self-report only); it is not a real positive control for B.
- **Does FA/FB pass for wrong reasons?** They are refused for B and C is closed in both, so for these two fixtures the reading is B-specific. The B reason string is not recorded in the battery's output, so a counter that opens B for any reason passes FA and FB.

## Axis and sizing (item 4)

- The claim calls itself calibration, but its only calibration item is B, a mutation score for the tip gate. The predicate for B accepts any correctly formed file (a2). Items A and C are bookkeeping and repair: a successor counter file and a relocated path.
- **Do-nothing at base** scores 0/3 (`open=3`, exit 1), which is correct.
- **Do-nothing at tip (one commit)**: the tip already closes A and C, so committing the fabricated receipt of (a2) scores **3/3 `met=true`, exit 0**, with no mutation run and no change to the gate. The predicate would read "calibration closed" for a file of 21 invented lines.
- The SCORECARD calibration score (2, HOLD) is not moved by C1 (the freeze says so); the claim's own closure would still be credited as calibration evidence.

## Other defects in the round's instruments (routed, not repaired)

1. `selftest` denominator is a literal: `print("selftest %d/%d" % (6 - len(bad), 6))` (c91_defects.py line 276) while the function runs eight checks (six receipt tuples plus two `SUMMARY_RE` asserts). The printed `6/6` is a constant; A's gate string `selftest 6/6` is satisfied by a constant (e2). Receipt `w1/ReviewC1/selftest.txt`.
2. Item C's replay runs the round-90 counter `c90_defects.py`, which the round-90 lesson records as forgeable (R90-A). C certifies the script's readings, not their soundness.
3. Item C's replay counts checks it runs (`TOTAL`), so `K==N>=9` is satisfied by any nine checks; the counter does not assert the nine expected labels. Not exercised by a fixture here.

## Routed (for the round's list, not edits)

- B: bind the receipt to an execution artifact (a run log or mutant-list digest produced by a committed harness at the revision, re-run or re-hashed by the counter), not to the form of its first line.
- A: grade the successor by an oracle the successor cannot write (a committed expected-readings file pinned by digest), not by its own self-reports; derive the selftest denominator from its checks.
- C: make the replay assert the copies succeed (`set -e`, or check `cp`/`git add` exit), and widen the static check to any `LANE`-rooted reference to `baseclean.out` with or without quotes or braces.
- Battery: assert the exact open set and the reason strings for FA/FB/FC; let FC reach the replay; make FD's receipt from a real run (or drop FD's B dependency).

## Honest limits

- No mutation receipt exists at the tip, so B's real discriminating power was not measured; I did not run a mutation harness (none is committed at the revision for this purpose).
- Full battery run (A's inner fixtures) only for the tip, e2 and e3; a/a2/b1/b2/c/d/f ran with `--skip-battery` (A reads `skipped`), which is sufficient for the B/C targets.
- Forgery receipts and scripts are synthetic by design; I did not write any real-looking mutation evidence into the lane.
- `git status --porcelain` in the lane may refresh the index stat cache; no content changed. The lane has untracked files from other seats (`w1/ExecReuseTrial/`, `assimilation/`, `controls/freeze-state-c1.txt`, `corpus/lessons/round-91.md`) that I did not touch.
- C2 was not evaluated (not my seat). The freeze's "R90-A gate half is discharged by the C2 battery" was not checked here.
- Tools: none installed or upgraded.

## Receipts (under `.ufo/waves/round-91/w1/ReviewC1/`)

`fixtures/base-run.txt`, `fixtures/tip-run.txt`, `fixtures/forge-{a,a2,b1,b2,c,d,e1,e2,e3,f}.txt`, `fixtures/forge.py` (driver), `fixtures/fx-f.py`, `fixtures/battery-reasons.txt`, `replay-f/{out,err}.txt`, `replay-f/rc.txt`, `selftest.txt`, `hashes.txt`.
