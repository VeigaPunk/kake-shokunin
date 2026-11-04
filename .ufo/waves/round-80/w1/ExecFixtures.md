# ExecFixtures — R79-4 survivor fixtures (kake round-80 w1)

**Verdict: done — `.ufo/waves/round-80/c80_ledger_fixtures.py` isolates all three round-79 mutation survivors against the frozen round-79 receipt-ledger counter (`killed=3`, exit 0), and `controls/c80-cheap-note.txt` records the cheap-note fixture's verbatim run red through `undisclosed=1` (with `malformed=1`, the documented co-fire).**

## Deliverables (bytes on disk, this working tree)

| File | sha256 |
|---|---|
| `.ufo/waves/round-80/c80_ledger_fixtures.py` | `1456741c3649cc3ff3df29409379982370495ad3c541d4fb350118314d8eebfc` |
| `.ufo/waves/round-80/controls/c80-cheap-note.txt` | `a9649a7896edcf21eb6c317961ccb358e3d41daa0b5ae6902a89f265a6a8064d` |
| `.ufo/waves/round-80/w1/ExecFixtures/runs.txt` (retained evidence) | `be12942a77b8dcd44f511290bb4500bff6a58f744787cc2deef7c4a2fab141ff` |

Interface is exactly the one pinned by `c80_defect_queue.py::p_r79_4` (`--root <tree> --json` →
`{"schema": "kake-r80-ledger-fixtures-v1", "fixtures": {"wrong_kind", "cheap_note", "symlinks"}, "killed": n}`,
stdout pure JSON, exit 0 iff `killed == 3`). The counter is driven as a subprocess
(`--revision <fixture HEAD> --round 79`), never re-implemented.

## Per-fixture result (canonical run, cwd=/home/vgpnk/Projects/shokunin, rc=0)

| Fixture | Mechanism (recipe source) | Counter's exact line | exit |
|---|---|---|---|
| `wrong_kind` (k3) | rewrite `"a\n"→"b\n"` disclosed with true blobs but `kind="append"` for a byte-level `content` change (MutC probe S1) | `C1v2 revision=5ec3da12e81a60d12509ce48d67411105a96ebf4 events=1 undisclosed=0 phantom=0 malformed=0 wrong_kind=1 unpointed=0 symlinks=0 round_rewritten=0 met=false` | 1 |
| `cheap_note` (k4) | same rewrite disclosed with true blobs, true kind, **empty note** → entry malformed → never matches → rewrite undisclosed (round-79 battery recipe, `ctl_receipt_fixture.py:105-109`; MutC F2) | `C1v2 revision=e6e5f80bf76daa3945d39d65a2e5d03734014d50 events=1 undisclosed=1 phantom=0 malformed=1 wrong_kind=0 unpointed=0 symlinks=0 round_rewritten=0 met=false` | 1 |
| `symlinks` (k5) | receipt replaced by a symlink at the measured tip; swap disclosed with the true link blobs (MutC probe S3, minimal one-event form) | `C1v2 revision=c02c0d82fb8671774d17e62c79d31905f0af4fc2 events=1 undisclosed=0 phantom=0 malformed=0 wrong_kind=0 unpointed=0 symlinks=1 round_rewritten=0 met=false` | 1 |

`killed=3`. Isolation is exact for `wrong_kind` and `symlinks` (sole red field, all six others 0 —
killing k3/k5: zeroing their field flips these fixtures green). `cheap_note` reproduces the
round-79 battery mechanism exactly: `undisclosed=1` **with** `malformed=1`, the co-fire MutC
named ("cheap-note stays red only via `undisclosed=1`") — the harness's `killed` flag requires
that pair, so the receipt cannot be greenwashed into a drop-one fixture.

## Commands run (verbatim, all exit codes)

1. `python3 -B .ufo/waves/round-80/c80_ledger_fixtures.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --json` (from the fleet root, foreign cwd — the `p_r79_4` invocation shape) → `killed=3`, **exit 0**. Full stdout/stderr retained in `runs.txt` and `controls/c80-cheap-note.txt`.
2. Carrier simulation (the C1 counter's `--revision` export tree has no `.git` and no round-79 files): harness copied into a bare tree, run with `--root` pointing at it → counter falls back to the lane copy `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-79/c79_receipt_ledger.py`, `killed=3`, **exit 0** (`runs.txt` §Run 2). Without this fallback the harness would be unevaluable at the carrier — that was a design constraint, verified closed.
3. `TMPDIR=<scratch> python3 -B .ufo/waves/round-79/c79_receipt_ledger.py --selftest` → `selftest: 15/15 passed`, **exit 0**.
4. `git diff --stat 9998dc7a… HEAD -- .ufo/waves/round-79/c79_receipt_ledger.py .ufo/waves/round-58/c58_receipt_rewrites.py` → empty (**rc 0**); same for `f20163c1… HEAD` → empty (**rc 0**). sha256: c79 `98b7c137…eb0a195`, c58 `3f52040a…e926c2d`. The engine the harness drives is byte-identical at the round base, the freeze, and HEAD.

## Finding: HEAD already carries a foreign-run receipt of this same harness

Commit `12116017` (08:03:09, "append guard, survivor fixture harness, cheap-note receipt, …")
integrated my harness **byte-identically** (HEAD blob sha256 `1456741c…` == disk) together with a
`c80-cheap-note.txt` receipt produced by a run I did not execute (fixture revisions
`3f02632c…/2ff5d47b…/3936e373…`, scratch `run-4qj59exn`). Its field shapes are identical to mine
(`killed=3`, same seven-field values per fixture) — an independent reproduction, not a conflict.
My working tree overwrites that receipt with my own verbatim run per this seat's spec; both
versions satisfy `p_r79_4`'s receipt checks (`cheap-note`, `undisclosed=1`), so integration of
either keeps R79-4's receipt conjunct closed. The round has since settled (`63afc0ee`); the L1
owns the choice.

## Disclosed debugging history (not evidence)

- Run 0a **rc=2**: builders committed the ledger rewrite without first writing `"b\n"` (nothing
  staged) — fixed; both builders now rewrite before committing.
- Run 0b **rc=1, killed=2**: `cheap_note`'s killed predicate initially required `malformed=0`,
  which the mechanism co-fires at 1 — fixed to require the pair.
- One `edit` call reported "could not find a close enough match" yet the replacement landed on
  disk; the file was re-read in full and re-run green twice afterwards, so the shipped bytes are
  the verified ones.

## Risks / notes

- **Counter-engine fallback**: at a carrier export tree the harness measures with the
  *working-tree* round-79/58 counter bytes (verified identical to base/freeze/HEAD today). The
  round-79 files are read-only this round, so this is exact today; if a later round ever edits
  those standing-gate files, a re-measure of an old revision would use the newer engine. That is
  standing-gate semantics, named here rather than hidden.
- `cheap_note`'s `killed` bar is deliberately stricter than `p_r79_4`'s (requires `malformed=1`
  beside `undisclosed=1`) to pin the mechanism, not just the red.
- Fixture repos use round-78 receipt paths with `--round 79`, so `round_rewritten=0` on every
  fixture; note-pointer target `corpus/lessons/round-75.md` is seeded in each fixture (pointed).
- Git fixtures: `git init -q` only under `$HYAKU_SCRATCH/kake-r80/ExecFixtures/` (created by the
  harness), toplevel asserted equal to the fixture dir before any commit, per-invocation
  `-c user.name/-c user.email/-c commit.gpgsign=false` identity, never global config, never the
  lane repo. Harness run dirs are removed in `finally`; the seat scratch tree was deleted and
  its absence verified (`test -e` → not present) before this report.
- No tools installed (none needed); no labrat spawned; no mutating git commands; no files
  touched outside the three paths above.
