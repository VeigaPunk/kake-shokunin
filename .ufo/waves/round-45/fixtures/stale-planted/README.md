# stale-planted fixture

`ctl1.py` is a byte copy of `.ufo/waves/round-44/controls-r43/headtail-V1-prefix-cache64.py`; `controls.tsv` carries the committed source SHA-256 and one G5 row. The fake counter calls `os.kill(os.getpid(), signal.SIGKILL)` for every invocation and writes nothing.

Before the driver run, `.ufo/waves/round-45/verification/hardening/before/stale-planted/out-v1/` is seeded with the following byte-exact committed receipts (the same fixture copies are retained here):

- `tools/ctl1.json` comes from `.ufo/waves/round-44/verification/claim/after-final/tools/buildport-m6.json`.
- `build-1.json`, `build-2.json`, and `build-3.json` each come from `.ufo/waves/round-44/verification/claim/after-final/build-1.json`.

Every top-level and nested field in each planted JSON receipt is unchanged from its cited real frozen-counter receipt, including `seed`, `met`, all `runs`, and all ratio/note fields. There is no raw `caughtBy` field; the audit derives it from false `runs[*].equal` values and v5 class keys. This setup tests whether the driver accepts pre-window bytes after the counter is killed.
