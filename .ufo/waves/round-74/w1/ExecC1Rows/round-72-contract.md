# Round 72 — frozen contract (kake, attempt 1)

Frozen before any wave seat ran and before any after-state was measured. Base revision (lane
`master` at round open): `3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1`.
Round-71 base for the C2 counter (fixed frozen constant in `c72_tmp_v2.py`): `cc6b4e0b8c35e72dfb02c6184b847f68c1262153`.

Disclosure (pre-freeze diagnosis): before this contract was written, the L1 ran the frozen gate family at the
base revision to locate the lane's red gates (c66 gate-status, c56, c57, c58, c59, id_resolver) and prototyped an
in-scratch repair of the adopted CrUX entry. Those diagnostic receipts are NOT the claims' base receipts; they
informed the choice of claims. The prototype repair was discarded (append-only guard and id rule block it). This
is recorded in the report as a conformance caveat for the non-author closure.

Scores at base (SCORECARD): operability 10, freshness 10, calibration 2. Lowest non-retired axis: calibration.

## C1 — calibration (lowest-scoring axis; HOLD 2)

Claim: the gate-status counter's self-assessment agreement rises by exactly one member, from 24 to 25 of 28, by
re-adjudicating the `selftest-tally-counter` row (c56) in SKILL.md from `live` to `historical`, on the basis of a green
run at its round-56 measured revision and a red run at the lane tip.

Predicate (one sentence, the same in the plan, the receipt label and the counter's reading): C1 is met iff, over the
frozen counter `.ufo/waves/round-66/c66_gate_status_hostportable.py` run at the measured tip, `agreement == 25`,
`evaluated == 28`, and the only member whose per-member label agreement changed from base to tip is
`c56_selftally.py`, which moves from disagreement to agreement.

Counting commands:
- base (receipt `controls/c1-base.txt`): `python3 -B .ufo/waves/round-66/c66_gate_status_hostportable.py --root . --revision 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1 --jobs 6` → `agreement=24 mismatches=4`
- tip: the same command with `--revision <tip>`
- pin proof (receipt `controls/c56-pin-linux.txt`): `python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision 4cb225fb032b04166fb0232bc98a7bcce72675ec` → exit 0, tally 10/10
- tip proof (receipt `controls/c56-tip-linux.txt`): the same script at base `3c68645a` → exit 1, `tally_mismatches=6`

Kill rule: if the tip `agreement` is not 25, or any member other than `c56_selftally.py` changes its agreement, or the
pin run is not green, C1 is unprovable and reported as such. A relabel the counter does not accept is not landed.

Non-goals (named, not claimed): c57, c58, c59 remain live and red on this host (their P7 real-lane legs cite three
staged ids, S303 S304 S352, that no kake registry row holds, inside the adopted entry
`corpus/knowledge/crux-bigquery-origin-membership.md`). That cause is routed to the operator (L0) and not repaired in
this round: the append-only guard forbids rewriting that entry, and the id rule forbids registering staged ids as
lane ids. No claim is made that the lane's gate family is green.

## C2 — operability (HOLD 10)

Claim: the round-72 C2 counter `.ufo/waves/round-72/c72_tmp_v2.py` rejects a phrase-only annotation on a
command-bearing `/tmp` line that the round-71 counter `.ufo/waves/round-71/c71_tmp.py` accepts, while still accepting
the lane's own repaired `mktemp` recipes and dated-absence prose annotations.

Predicate (one sentence): C2 is met iff `c72_tmp_v2.py --selftest` exits 0 with `11/11`, `c71_tmp.py` exits 0 and
`c72_tmp_v2.py` exits 1 on the J3 control commit that `.ufo/waves/round-72/controls/j3-control.sh` builds (a scratch clone
of base tip `3c68645a` with line 27 replaced by a command-form `cp` line carrying the phrase; the commit hash differs per
run and is printed by the script; the script is the frozen artifact), the counter exits 1 at the round-71 base
`cc6b4e0b8c35e72dfb02c6184b847f68c1262153` (red-before), and exits 0 at the measured tip.

Counting commands:
- `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --selftest` (receipt `controls/c2-selftest.txt`) → `11/11`, exit 0
- `sh .ufo/waves/round-72/controls/j3-control.sh` (receipt `controls/c2-j3-control.txt`) → `c71_exit=0` and `c72_exit=1`
- `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --revision cc6b4e0b8c35e72dfb02c6184b847f68c1262153` (receipt `controls/c2-base-red.txt`) → exit 1
- `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --revision <tip>` → exit 0 (receipt `controls/c2-base-head.txt` at base `3c68645a`)

Kill rule: if the J3 control is not rejected, or the selftest is not 11/11, or the red-before is not red, or the tip is
not green, C2 is unprovable. A constant stub that always exits 0 or always exits 1 cannot satisfy all four legs at once.

Source: the `--end-of-options` mitigation for revision arguments (round-71 M7) rests on S439
(`corpus/SOURCES.md`, git-scm gitcli, opened 2026-11-03, located quote in `.ufo/waves/round-72/sources/gitcli.html`).

## Frontier step

- `corpus/SOURCES.md` gains exactly one row, S439 (gitcli), opened this round; census exit 0 before and after is required.
- Mistakes mined into `corpus/lessons/round-72.md` `## Mistakes`: (M1) the r70 adoption cited three staged ids no
  registry row holds (id resolver red at base, `dangling=3`); (M2) the round-71 counter accepted the J3 control;
  (M3) pre-freeze diagnosis (the freeze follows diagnostic runs, disclosed above).

## Acceptance (round end)

- Census `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exit 0.
- `scripts/hyaku/jj-lane.sh state` shows `ahead=0` after landing; `git ls-remote origin refs/heads/master` equals the final lane hash.
- Report `.ufo/reports/round-72/kake.md` committed via `fleet-commit.sh --as kake` only after WAVE-DONE.
