# ScribeMistakeMine — round 33 mistake mined: a repair counter that accepts a faked repair

Seat: KakeR33.ScribeMistakeMine (scribe, leaf). Milestone r33-build. Axes: operability, freshness.
Base of my clone: `bc6c4a8d435473f3c30903210be30d9d6e3ef750`.
Deliverable: `/fast/scratch/hyaku/kake-r33/w1/ScribeMistakeMine/mistake.md` (row draft, criterion draft,
check command, failing output).

## What I built

Chosen candidate: the round-32 C2 counter frozen with seven defects (`w1/ReviewC2CounterCode.md`,
`w1/CriticC2Scope.md`), over the m3g under-count (`w1/MutM3Variants.md`) — the C2 gap is a gate that was
never required, not a list that was short: wave-1 seats measured the looseness in-round and the closure
still had to re-measure by hand ("Wave 1 reproduced seven defects in that counter, so the three conditions
were re-measured without it", `corpus/lessons/round-32-verifier-spotcheck.md`, C2).

Reproduced, in my own sandbox: the frozen counter `.ufo/waves/round-32/c2_retained_count.py`
(sha256 `48126fc5b42db1e210bcc2c24c7cb699207ee79b0683bf47cb0c8f94c3f3e22c`, matches the round-32
spot-check) gives `met 3` on the landed round-32 repair `e9283ec` **and** `met 3` on a hollow commit
`6ffa03ea9c1b094f04ddcf65da46903b7cd16c82` whose repair is faked at every condition, while the
before-revision `a0b0dff` gives `met 0`.

Hollow commit (built in `/fast/scratch/hyaku/kake-r33/w1/ScribeMistakeMine/w32`, from `a0b0dff`):
- the two ds4cc blobs at `scripts/fixtures/unrelated/a.txt` / `b.txt` (`git hash-object` reproduces
  `d17ab7e5…` and `ee0b6381…`), i.e. not under the declared `sources/ds4cc-1fbdb8ed/` path;
- fabricated registry row `| S099 | ds4cc-marketplace 1fbdb8ed | x | x | x | x | x | x | 2026-10-22 | x | x |`
  under `## Registry`;
- one unrelated mention `S099 is unrelated to this entry.` in the entry.

## Commands and outcomes (exit codes)

- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone`; `git -C clone checkout -q bc6c4a8d…` → 0;
  `rev-parse HEAD` = `bc6c4a8d…`. Second clone `w32` checked out at `a0b0dffcd95b2215f638a5ff7591dd4fde325d27` → 0.
  `TMPDIR=/fast/scratch/hyaku/kake-r33/w1/ScribeMistakeMine/tmp` exported for every run.
- `python3 -B clone/.ufo/waves/round-32/c2_retained_count.py --rev a0b0dff --repo clone` → 0, `met 0`.
- same `--rev e9283ec` → 0, `met 3`, `c2RowIds ["S062"]`.
- same `--rev HEAD --repo w32` (hollow) → 0, `met 3`, `c2RowIds ["S099"]`, `c1BlobPaths` pointing at
  `scripts/fixtures/unrelated/{a,b}.txt` → `/fast/scratch/hyaku/kake-r33/w1/ScribeMistakeMine/hollow-count.json`.
- **Criterion check, failing direction:** `python3 -B check_counter_control.py --counter clone/.ufo/waves/round-32/c2_retained_count.py --repo clone --before a0b0dff --after e9283ec --hollow 6ffa03ea`
  → **exit 1**, `before=0 after=3 hollow=3`, `FAIL: hollow commit scores the declared after-value 3`
  (`check-round32.txt`).
- **Criterion check, passing direction:** same check against a sandbox-only strict counter
  (`strict_c2_pin_count.py`: pins path `100644`, row id `S062`, and an `S062` line containing
  `retained|byte-identical`) → **exit 0**, `before=0 after=3 hollow=0` (`check-pass-strict.txt`).

Notable: the round-32 counter exits 0 on every input, printing only `met`, so a hollow commit scoring the after-value is invisible without a negative control.

## Drafted row (for `corpus/lessons/round-33.md` `## Mistakes`; the file has no such section at `bc6c4a8`)

Class: *a repair counter accepts a faked repair at its declared after-value*.
Captured-by: **partly** — `w1/MutC2Conditions.md` (M4–M8 survive at `met 3`), `w1/ReviewC2CounterCode.md`
(F1–F7) and `w1/CriticC2Scope.md` (hollow commit `ea1050dd` → `met 3`) observed it in-round, but no
criterion or declaration check required a control on the counter before `met` was read as the claim's
evidence; `corpus/QUALITY.md:307` only asks a counter to reject a *constant* gate.
Fix: `corpus/QUALITY.md` criterion appended this round (text in `mistake.md`), with the check shown able
to fail and to pass above.

## Touched surfaces

- Lane: this report only. Lane repo read with `git show` / `git ls-tree` only.
- Sandbox: `clone/`, `w32/` (hollow commit `6ffa03ea`), `check_counter_control.py`,
  `strict_c2_pin_count.py`, `hollow-count.json`, `check-round32.txt`, `check-pass-strict.txt`, `mistake.md`.
- No jj command ran anywhere. No network request; no owned property contacted. No tool installed.

## Findings for the L1 (advisory)

1. The criterion is non-duplicate against `QUALITY.md:307` (reject a constant), `:362` (reason code) and
   `:461` (compare every expectation field): none pins the identity of the artifact a counter grades.
2. If the criterion lands, `check_counter_control.py` must land with it (e.g. under `.ufo/waves/round-33/`),
   or the check sentence cannot be run by a reviewer; the draft in my sandbox is the reference.
3. The same shape applies to round 33's own C1/C2 counters: C1 grades runner variants and C2 grades a pin;
   a reviewer reading `met 4` should ask what a hollow variant scores. I did not run that on either
   round-33 counter — out of my slice.

## Not verified

- Did not verify the ds4cc upstream bytes against the lane's retained copies (sibling surface).
- Did not test one-condition-at-a-time hollow commits; the drafted limit says one per condition group.
- Did not replay the round-32 bespoke receipts; I ran the counter myself at the same revisions.
- Did not edit `corpus/lessons/round-33.md` or `corpus/QUALITY.md` (leaf bounds); the row and criterion
  text are drafts only.
