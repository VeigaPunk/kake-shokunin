# ExecReceiptPin — round-38 w1 (defect 5: post-measurement receipts must pin the tool)

Built `pinned_selftest.py` and the pinned re-run of round-37's postfix selftest. Nothing under
`/fast/scratch/hyaku/kake-r38/` or `kake-r38ctl/` was listed, read, stat'ed or opened; no round-38
counter was run. No network, no tool installs or upgrades.

## Deliverables (sandbox; L1 copies after review)

| Path | sha256 | size |
|---|---|---|
| `/fast/scratch/hyaku/kake-r38w1/ExecReceiptPin/pinned_selftest.py` (to land as `.ufo/waves/round-38/pinned_selftest.py`) | `7f5fd17b7d55a1287972901d75979d6e1ccd3b5ae734847a5d349c7f1fa556d0` | 337 lines |
| `/fast/scratch/hyaku/kake-r38w1/ExecReceiptPin/r37-postfix-selftest-pinned.json` | `97b377bc603c3658dbc7384e411197291239618f661db712aeb90245e5709fb3` | 1 receipt |
| `/fast/scratch/hyaku/kake-r38w1/ExecReceiptPin/r37-postfix-selftest-pinned.exit` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | contains `0` |

## What the runner does

`pinned_selftest.py --root R --revision REV --tool PATH --selftest PATH --out FILE` resolves `REV`
via `git rev-parse --verify --end-of-options REV^{commit}`, reads tool and selftest with
`git cat-file blob REV:PATH` (blobs only, never the working tree; all `GIT_*` env dropped, system
and global config ignored, hooks off — the `receipt_replay.py` Git pattern), writes both to a
private temp dir, runs `python3 -B <selftest> --tool <copy>` with `TMPDIR` inside that dir, and
writes the receipt = the selftest's stdout JSON summary at top level (its `tool` member re-pointed
to `toolPath`; temp paths stay in `command`) plus `toolPath`, `toolRevision`, `toolObjectId`,
`toolSha256`, `selftestPath`, `selftestRevision`, `selftestObjectId`, `selftestSha256`, `revision`,
`revisionRequested`, `selftestExit`, `timedOut`, `command`, `root`, `time` (UTC). Pin fields are
written after the summary, so a summary cannot forge them. Exit = selftest exit; 2 on usage error,
unreadable revision/blob, timeout (process group killed), a signal-killed selftest, an unreadable
summary (never reported as a pass) and internal errors — every one still writes a receipt.

Two additions beyond the named signature, both optional: `--tool-revision` / `--selftest-revision`
(default: `--revision`) and `--exit-file` (lane `.exit` convention). Deliberate deviation: a
selftest that prints no JSON summary gives exit 2, not its own 0.

## Pinned receipt for round 37's postfix tool
Command, exit 0 (3 s):
`timeout 900 prlimit --as=4000000000 python3 -B pinned_selftest.py --root clone --revision af43a50fa399881eead9381d835b78a015e277a6 --tool scripts/robots_audit.py --selftest scripts/robots_audit_selftest.py --out r37-postfix-selftest-pinned.json --exit-file r37-postfix-selftest-pinned.exit`

Receipt: `cases 137, passed 137, failed 0, verdict clean, selftestExit 0`,
`toolPath scripts/robots_audit.py`, `toolRevision af43a50fa399881eead9381d835b78a015e277a6`,
`toolObjectId 55637e6bfc91cd95098757d914b7c5f2677b1bd0`,
`toolSha256 944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`,
`selftestRevision af43a50f…`, `selftestObjectId 78dd2fe5828a29daf30b61acdad416f0af4c72e0`,
`selftestSha256 01c61297987f043f3bdc80612e50f744ac6f84605c43963c63fc87e1e6151df4`,
`time 2026-10-23T04:36:40Z`, `perContract` identical to round-37's receipt.

Equality to the round-37 tip tool named in the closure (defect 5's ask):
- `git cat-file -p 8319cb76:scripts/robots_audit.py | sha256sum` → `944d2f51f396…d3e5`; base
  `af43a50f` and the lane working tree (`…/kake-shokunin/scripts/robots_audit.py`, read-only,
  04:35Z) hash the same. `8319cb76` is an ancestor of `af43a50f` (exit 0).
- The unpinned round-37 receipt (`8319cb76:.ufo/waves/round-37/verification/postfix/robots-selftest-137-on-postfix-tool.json`)
  carries `tool: "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/robots_audit.py"` and has
  `toolSha256`, `toolRevision`, `revision`, `selftestSha256` all absent; its 8 measurement fields
  (`cases`, `passed`, `failed`, `passedOverTotal`, `perContract`, `failures`, `selftest`,
  `verdict`) equal the pinned receipt's.

## Falsifiers run (all in the sandbox clone)

| Test | Command shape | Observed |
|---|---|---|
| Working-tree independence | junk tool written over `clone/scripts/robots_audit.py` (tree sha `afaf6e72…`), pinned at `af43a50f` | exit 0, receipt `toolSha256 944d2f51…`, 137/137 — the tree copy was not read |
| Exit propagation 1 | 137 selftest at `af43a50f` on `retained/controls/CtlTrivial-constant_clean.py` at `2dab7f31` (`--tool-revision`) | exit 1, `passed 2/137`, `verdict failed`, `.exit` = `1`, sha `d1a777c9…` |
| Timeout | `--timeout 1` | exit 2, `timedOut true`, `error "selftest exceeded 1 s and was killed"`, `selftestExit null`; `$TMPDIR` left 0 entries (child temp dir is inside the removed work dir) |
| Bad revision / tree path / missing blob | `--revision deadbeefdeadbeef`; `--tool scripts`; tool at `621fb528` | exit 2 each, receipt carries `error` |
| Unreadable summary | sandbox-only commit `8781e7de…` whose selftest prints `not json at all` | exit 2, `summary null`, `summaryError`, `selftestStdoutHead "not json at all"`, `selftestExit 0` recorded |
| GIT env contamination | `GIT_DIR=/nonexistent GIT_WORK_TREE=/tmp GIT_INDEX_FILE=/nonexistent` exported | exit 0, 137/137, same sha |
| Rerun determinism | same production command twice | exit 0 both; non-volatile field differences `{}` |

No temp dirs or processes of mine remain; `pgrep` for my paths is empty.

## Not verified / limits

- Not run at a round-38 build commit (none landed while this seat ran): the runner is a tool, and
  the pinned receipt above is for `af43a50f` only.
- The round-37 counter (key `424aa248`) and both round-38 counters were not run: not this item, and
  I hold no round-38 key.
- `selftestStdoutBytes` varies with TMPDIR path length; informational only, not a pin.
- The runner would need `scripts/robots_audit_selftest.py` to keep printing its summary on stdout;
  a selftest that changes that fails closed (exit 2) rather than silently green.
- No installs to record: no package manager, `uv`, `npm` or binary download was used.
