# ExecC1Perf

Claim C1 performance and determinism. Counter `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root <lane> --revision 044048597d62f3199494b63b36e90dd57825e350`, lane `/home/vgpnk/Projects/shokunin/kake-shokunin` (HEAD `cc8da1674d6e590ae2d05e1f48944ac7939e9ecd` throughout), scratch `/fast/scratch/hyaku/kake-r58/ExecC1Perf`. Host: 32 cores, load average 13.76 / 13.31 / 12.64 at start, Python 3.14.8. Every run is read-only against the lane; every fixture is a `git clone -q --shared` under scratch; no lane, fleet-repo or sibling-lane path was written. Measurement tools already present (hyperfine, strace) — no installs, no pacman.

Method: output captured to files and compared by sha256 (never by eye); timings by `hyperfine` (3-run blocks for the mandated shape, 7-run blocks for medians); syscall-level cost and filesystem reach by `strace -f -e trace=execve` and `-e trace=openat,newfstatat`; attribution by `-m cProfile -s tottime`.

## TIMINGS:

Mandated 3-run blocks, base revision, plain and `--json`, stdout captured each run:

| shape | per-run wall (ms) | mean | peak RSS | exit |
|---|---|---|---|---|
| plain | 122.7 / 120.5 / 117.4 | 120.2 ± 2.7 | 25.6 MiB | 1 |
| `--json` | 123.3 / 124.8 / 117.2 | 121.8 ± 4.0 | 25.9 MiB | 1 |

7-run medians (same host load): base plain 122.6 ms (min 119.2, max 128.6); base `--json` 123.1 ms (min 121.3, max 126.9); tip `cc8da16` plain 121.1 ms (min 118.9, max 122.6, n=5); base through the `--no-checkout` shared clone 129.2 ms (min 124.5, max 134.5, n=5 — the ~7 ms delta is a separate object store on `/fast/scratch`, not worktree state). Runtime spread is ±4 %, consistent with the host load.

Cost structure (strace, base run): **61 git spawns** — 39 `ls-tree`, 20 `rev-parse`, 1 `log`, 1 `show`; plus 671 failing `execve` PATH probes (11 per spawn before `/usr/bin/git`, ~0 measured time). Single-call costs: full-history `log --name-status` 16.2 ms, every other git call 0.7–0.9 ms; interpreter floor (`python3 -B -c pass`) 6.8 ms. cProfile: `clean_env()` is called once per spawn and re-iterates + re-encodes a 264-variable environment each time (cumtime 33 ms, ~0.4 ms per call); `select.poll` waiting on children ~50 ms; `events()` is the only long function (cumtime 148 ms under the profiler).

After-state scale, measured on a scratch fixture (clone of the lane at base + one selftest-identity commit carrying a 19-entry ledger built from the 19 real base events): **119 git spawns, median 192.2 ms** (min 185.6, max 195.7, n=7) — ~+3.7 ms and ~+3 spawns per ledger entry. [INFERENCE] the real after-state run lands in the same 190–200 ms band, because spawn count and not text volume drives the cost; the fixture's placeholder kinds and absent-pointer notes change the counters (`wrong_kind=13`, `unpointed=19`) but not the spawn count.

Headroom measured, **not applied** (scratch copy only, lane counter untouched): memoizing `clean_env()` in a module-level cache gives median 112.0 ms (min 107.7, max 116.8, n=7), −8.6 %, with byte-identical stdout. Full diff and numbers in `…files/headroom-variant.txt` + `…files/variant-env-memoized.py`. The larger lever for the after-state is the per-entry/per-event spawn pattern (`rev-parse --verify` + two `ls-tree` per event, `cat-file` per note pointer); batching those is [INFERENCE] worth ~40–80 ms at 19 entries, unmeasured — I did not build a batched variant.

## DETERMINISM:

- Base plain stdout sha256 `8ac03b117dfecd75f7a371068a9e7be5d3d00a41b9bf61e6479bd457cb40ba70`, identical in all 3 captured runs; base `--json` sha256 `56518e5a42999cbbf3bc2f63b6cce7e4d6eeed6645c98e9fc759a2d083eb0e0b`, identical in all 3 captured runs and in 20 further sequential `--json` runs (1 unique hash). stderr is empty (0 bytes) in every run. Exit is 1 in every base and tip run: at both revisions the ledger is absent, so the counter reports `events=19 undisclosed=19 … met=False` — that is the contract's before-state, observed, not a judgement.
- One byte stream (`8ac03b11…`) survives every interface/environment probe I ran: `LC_ALL=C LANG=C TZ=UTC`; `LC_ALL=en_US.UTF-8 TZ=Asia/Tokyo`; abbreviated revision `0440485`; cwd `/` with `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`GIT_OBJECT_DIRECTORY` pointed at `/nonexistent`; a hostile global git config via a fake `HOME` (`log.showSignature=true`, `log.decorate=full`, `core.abbrev=7`, `column.ui=always`, `diff.noprefix`, `diff.external=/bin/false`, `i18n.logOutputEncoding=ISO-8859-1`); `PYTHONHASHSEED` 0/1/2/12345/random; `--root` as a relative path from `/`; `--root` as the `.git` directory itself.
- Why it holds, from the code and the traces: stdout carries no timestamp, no path and no absolute path (only the resolved 40-hex tip), event order comes from `git log --reverse`, `_new_receipts` is sorted, `GIT_*` is stripped by `clean_env()` and `core.quotePath=false` is pinned on every call — which is exactly why the hostile-config probe is a no-op. At the tip the same invariance holds: sha256 `3931a48683c06aa01a7a0b7cc3048dbd08c2210278767f7e329ea22a646b8c3e` across all three roots tested.

## WORKTREE INDEPENDENCE:

- Syscall audit (`strace -f -e trace=openat,newfstatat`): the only lane paths touched outside `.git/` are directory stats during repo discovery (`…/kake-shokunin` 183×, `…/kake-shokunin/.git` 122×) and the counter script itself (2 stats, 3 opens). **Zero** opens or stats of any worktree receipt, ledger, source body or tree file. Raw counts in `…files/fs-audit.txt`.
- stdout identity at base across five worktree shapes, all `exit 1`, stderr empty, sha256 `8ac03b11…`: the lane worktree itself; `git clone -q --shared --no-checkout` (no working files exist at all); `git clone -q --shared --bare` (no worktree concept); a checkout clone deliberately dirtied (a receipt overwritten with `PENDING-JUNK`, a receipt deleted, an untracked `.ufo/waves/round-58/controls/TAMPERED.txt` and an untracked `stray.py` added — `git status` confirms `M`/`D`/`??` entries); and the lane run from cwd `/`.
- At the tip, identity across lane worktree, `--no-checkout` clone and the dirty clone: `3931a486…`. A dirty worktree therefore cannot change a C1 verdict; only a different revision can. That matches the contract's `--revision` interface — an uncommitted ledger edit is invisible by construction.

## Unrun / limits

Cold-page-cache timing (would need a host-wide cache drop: out of bounds), timing with the object store on a filesystem other than `/fast/scratch`, and a real after-state receipt run: the ledger and the two C2/C3 after-receipts are absent from lane history at `cc8da16`, so the after-state figure is the fixture estimate above, marked [INFERENCE] where it extrapolates. Suites were not run for me — I ran the counter itself only, with `--root`/`--revision`, never `--selftest` (that writes temp fixtures; other seats hold the selftest cases).

## Evidence

`.ufo/waves/round-58/w1/ExecC1Perf.files/`: `base-plain.txt`, `base-json.txt`, `tip-plain.txt`, `ledger19-fixture.txt`, `ledger-fixture-19entries.json`, `hashes.txt` (every sha256 and invariance label), `timings.txt` (all hyperfine blocks), `git-spawns.txt`, `fs-audit.txt`, `headroom-variant.txt`, `variant-env-memoized.py`. Scratch `/fast/scratch/hyaku/kake-r58/ExecC1Perf` deleted after copying these.

VERDICT: C1 counter at base is deterministic (one stdout hash over 26 runs and 16 environment/root/worktree probes), worktree-independent (zero worktree reads; identical bytes on no-checkout, bare and deliberately dirtied clones) and costs 122.6 ms median / 61 git spawns, rising to ~192 ms at 19 ledger entries; no lane file was modified.
