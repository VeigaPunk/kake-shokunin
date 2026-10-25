# SentinelBounds — round 49 wave 1

Axes: operability (write bound), freshness (bound pinned to the scored tip, not a stale base).

Seat: SentinelBounds. Leaf: no subagent dispatch. This seat's only write is the report named below.

## Absolute path this seat writes

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-49/w1/SentinelBounds.md`

That path resolves inside the lane (`readlink -f` of the parent is `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-49/w1`; no symlink on that directory). Before this write the path was absent.

## Confirmation: this seat did not write outside its report

Observed, not inferred from the prompt:

- Lane toplevel: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/kake-shokunin`.
- Scored tip: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD` → `1c846ed2d67b1692ea966be064f0fc04542763c6` (the wave's measured revision, not base `090ce8f1cfbae2dfb8bfa65dedd2c72861c48166`).
- First command of this seat: `2026-10-24T21:37:51-03:00`. At that instant `SentinelBounds.md` was absent. A second check immediately before this write was still `ABSENT`.
- This seat issued no redirect, no `git add`, no `git commit`, no editor write, and no counter run. The Write that created this file is the only mutation.

Other files already in `.ufo/waves/round-49/w1/` at the pre-write listing are peer seats, not this seat. That listing included `CriticOpenedDate.md`, `ExecAncestor.md`, `ExecCensusLane.md`, `ExecQuoteBlob.md`, `ExecRerunC1.md`, `ExecRerunC2.md`, `MutWorktreeOpen.md`, `ReviewMirrorScope.md`, `ScoutOllamaProvince.md`, `ScoutQuarantineSlice.md`, `ScoutReopenS273.md`, `ScoutReopenS274.md`, `ScribeConsider.md`, `ScribeGateQuotes.md`, `ScribeRejects.md`, `ScribeRowShape.md`, and `swarm-registry.json` (mode `0600`, mtime `2026-10-24 21:36:01 -0300`). This seat did not open those files for write.

## No-jj bound

This seat did not invoke `jj`. The binary is on PATH at `/home/vgpnk/.local/bin/jj`; it was not executed. Lane jj state was only `stat`'d:

- `.jj/working_copy/tree_state` mtime `2026-10-24 21:34:41.878932604 -0300`
- `.jj/working_copy/checkout` mtime `2026-10-24 21:34:43.612933466 -0300`

Both predate this seat. Re-stat after the read-only commands left those mtimes unchanged. No jj operation, no working-copy snapshot, no `refs/jj/keep` write from this seat. A `jj log` / `jj st` in this checkout would snapshot the dirty wave directory (round-47 sentinel observed that); that command was not run.

## No-fleet bound

This seat did not create, edit, or delete any path under `/home/vgpnk/Projects/shokunin` except this report under the kake lane. It did not open a sibling lane, did not write `/home/vgpnk/Projects/shokuknow/merge/kake/`, and did not run a campaign tool. It did not touch `considerthese/`, `.ufo/waves/round-46/residual/`, or the round-48 validate copies.

Fleet identity was read once: `git -C /home/vgpnk/Projects/shokunin rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin`, distinct from the lane. Two help invocations (`git show -h`, `git show --help`) ran with the session cwd at that fleet root. They printed help only. Fleet `.git/index` mtime stayed `2026-10-24 21:36:37.268025232 -0300`, before this seat. Lane `.git/index` mtime stayed `2026-10-24 21:34:59.847942363 -0300`. No fleet file was opened or written.

## Attack: the counters do not enforce this bound

Severity: low on the frozen argv (not reached). The scored commands stay inside the bound. The counter source does not. Not executed: exercising either hole writes outside this report.

Frozen argv (wave context), both with `python3 -B`, lane `--root`, and revision `1c846ed2d67b1692ea966be064f0fc04542763c6`, and neither passing `--json`:

- `python3 -B …/c49_order.py --root …/kake-shokunin --revision 1c846ed2d67b1692ea966be064f0fc04542763c6`
- `python3 -B …/c49_quote_truth.py --root …/kake-shokunin --revision 1c846ed2d67b1692ea966be064f0fc04542763c6`

`contract.json` counting commands match that shape (`--root . --revision <commit>`, no `--json`).

### F1 — `--json` truncates an arbitrary path

Exploit path: a caller adds `--json <path>`. Both counters then `open(path, "w")` with no confinement to the lane, the report dir, or even an existing parent check beyond what `open` does.

Evidence: `c49_order.py:204-206` and `c49_quote_truth.py:211-213`. The docstring claim is about reads (`git show` only). The write is a separate path. Because C1 and C2 score committed blobs, this write can truncate `corpus/SOURCES.md`, a fleet ledger, or a sibling file and still leave `met` unchanged.

Impact: "score held" is not "bound held". The frozen commands do not pass `--json`, so the scored run does not hit this. This seat did not pass it.

Smallest remediation: drop `--json`, or reject any path that is not a relative file under a declared output directory inside the lane. Do not apply that from this seat.

### F2 — CLI revision is interpolated into `git show` with no end-of-options guard

Exploit path: `--revision` beginning with `-` becomes one argv token `f"{revision}:{rel}"`. Git 2.56.0 documents `git show --output=<file>` ("Output to a specific file instead of stdout"). A revision `--output=/tmp/escaped` composes to `--output=/tmp/escaped:<rel>`, which git parses as an option. Round-47 observed that composition create a file outside the tree. This seat did not re-run it: the successful case writes outside this report.

Evidence: `c49_order.py:80-83` and `c49_quote_truth.py:76-79` build `["git", "-C", root, "show", f"{revision}:{rel}"]`. Neither checks the CLI revision. `c49_order.py:133-135` does reject a `pre_rev` that is not 40 lowercase hex before that value is passed to git. The measured revision from argv has no such check. Help quote, this host, no file written:

```
git version 2.56.0
--output=<file>
    Output to a specific file instead of stdout.
```

Impact: the frozen revision is 40 hex, so the scored run is not injected. The counter will still run a dashed revision if a later caller supplies one, and that can write outside `--root`. Same low reachability as F1: argv-only, not ledger-fed.

Smallest remediation: reject a revision that does not match `^[0-9a-f]{40}$`, or resolve it with `git rev-parse --verify --end-of-options` and pass only the object id. Do not apply that from this seat.

### F3 — `--root` is an unconfined `git -C`

Info. `git -C root` accepts the fleet root or a sibling. Combined with F2 that is a write outside the lane; alone it is a read outside the lane. The frozen commands pin `/home/vgpnk/Projects/shokunin/kake-shokunin`. This seat did not point `--root` elsewhere and did not run the counters, so no `__pycache__` was written beside them either (`python3 -B` is what the frozen commands use; this seat did not import the modules).

## Checks not run

- No counter execution, no `--json` probe, no dashed-revision probe, no sandbox clone.
- No `jj`, no `git status`, no `git add`, no `git commit`, no push.
- No read of sibling repos, fleet ledgers, `.ufo/state/`, or `.ufo/watchdog.log`.

Report: .ufo/waves/round-49/w1/SentinelBounds.md
