# stale-backdate fixture

A fake counter that writes a fully valid-shaped receipt (own sha, seed, note None,
met False — the reachable exit shape for a not-met counter, `finish(0 if met else 1)`)
but BACKDATES its mtime 5 seconds, then exits 1. Only the mtime is synthetic.

Under the frozen v1 driver this receipt certifies (ok=True) — the round-44 review's
defect 1c reachability class (a stale receipt accepted). Under driver v2 the receipt
fails the run-window mtime check and is refused with the named class `stale_receipt`;
with a fresh mtime (the `AttackStaleBackdate` w2 variant) v2 credits it, proving the
fixture carries the refusal. Unlike the stale-planted fixture (SIGKILL + pre-planted
bytes, exit -9), this variant keeps the counter exit inside {0,1} so the mtime
branch — not the exit branch — refuses it.

Correction landed from `w2/AttackFixtureShapes.md`: the fixture originally exited 0
with met False, an unreachable schema/exit combination; it now exits 1 with met False.
