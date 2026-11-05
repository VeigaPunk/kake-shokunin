# SentinelScope — round-98 execution-boundary review

Full register: `vectors.md` (15 vectors, one blocking). Receipts are flat files in this directory.
Report path: the seat spec names `.ufo/waves/round-98/w1/SentinelScope.md`; the hard bounds place reports
inside `w1/SentinelScope/`, so the report lives here. Findings are identical.

## Findings

1. **SV-8 — BLOCKING for C2 (scored-revision selection / seed grind).** The C2 seed is
   `int(sha256(commit id)[:8],16)`. The author picks the commit id. A flawed candidate (lenient
   `shared: null`, passes all 60 hand cases, fails the default-seed population `239/240`) returns
   `met=true` on 3 of 10 fixture commits that differ only in commit message (the candidate commit
   itself among them). A correct candidate (`pos-oracle`) returns `met=true` on 4 of 4. The freeze's
   "unknown until the scored commit exists" premise does not hold when the candidate's author chooses
   the scored commit. Route to L1: pin the seed in the frozen contract before any candidate exists (or
   enumerate, or require pass across K pinned seeds), and record the number of revisions scored.
   Receipts: `receipt-grind.txt`, `poc-p7-flaw-shared-null.py.txt`.

2. **Candidate-run sandbox (SV-1..SV-7, SV-15) — carried under R97-5.** Demonstrated, all non-destructive:
   - reads the oracle and HAND expectations from the lane and scores `met=true` (SV-1);
   - rewrites its own executed file so cases 2–300 run different bytes than the printed sha (SV-2);
   - persists cross-case and cross-run state via absolute paths (SV-3);
   - writes outside its cwd; same-uid write access to `freeze.md`, `SCORECARD.md`, `.git/HEAD`, `.git/config` (probed, not written) (SV-4);
   - spawns a `setsid` grandchild that survives the per-case timeout and the counter (SV-5);
   - opens loopback connections on every case (SV-6, external egress not exercised);
   - reads 35 parent-environment names including `PI_TOOL_BRIDGE_TOKEN` (names only) (SV-7).
   The declared R97-5 limit covers these in kind; SV-2 and SV-4 mean the printed `sha256=` line and
   the "no frozen byte changes" rule are not enforced by the counter. L1 control: re-verify
   `controls/instrument-sha256.txt` and the scored revision after each scoring run.

3. **Git reads (SV-9..SV-14) — none.** Both counters read committed bytes only (`show <rev>:path`,
   `cat-file -e <rev>:path`, `rev` a commit id from `rev-parse --verify <x>^{commit}`). Option or ref
   injection through `--revision` / `--fleet-revision` was rejected by `rev-parse --verify` in every probed
   form (including `--revision=` and `--opt=value`). Textconv and replace refs had no effect. One
   conditional item (SV-13): `GENV` inherits `GIT_DIR`, which redirected a read to a fixture repo; the frozen
   verdict is clean only if the L1 scores from an environment with no `GIT_*` variables (record it). Hygiene
   fix: allowlist `GENV`.

## Verdict inputs

- Counters checked: `c98_captable.py` (C1), `c98_stale.py` (C2). Frozen digests match committed and worktree
  bytes (`receipt-instrument-digests.txt`). No instrument was patched or re-stamped.
- Scratch: `/fast/scratch/hyaku/kake-r98/SentinelScope/` (own seat directory); removed at seat end, after receipts were copied here.
- Tools: none installed or upgraded. System `python3` 3.14.8, `/usr/bin/git` 2.56.0.
- Not exercised: external egress; memory and CPU exhaustion; grafts, shallow and partial-clone fetch; any mutating git on LANE.

SENTINEL vectors=15 blocking=1
