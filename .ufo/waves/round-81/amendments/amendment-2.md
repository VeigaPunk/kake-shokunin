# Round-81 amendment 2 — C2's instrument measures what its sentence says

Written 2026-11-04, after amendment 1 and **before any C2 after-state existed**:
`.ufo/waves/round-81/capture/` does not exist at this moment (no manifest, no receipts,
no audit receipt) and `w1-results.json` does not exist. The claim's predicate, populations,
kill rules and targets are unchanged; this amendment corrects the instrument and fills a
control the contract named but the freeze did not ship.

Found by the wave's `CriticClaims` seat, from bytes at `bec3ecf7`, before any after-state:
`w1/CriticClaims.md` findings 1 and 2.

## A1 — the manifest must equal the frozen declared expectations, not assert its own

Contract §C2 declares "three real surfaces" and the frozen
`.ufo/waves/round-81/capture-expectations.json` is the declaration. The counter read the
manifest only, so a manifest that declared its own `expect` objects could make a surface
look clean. Now `evaluate()` loads the expectations file from the measured tree and
requires: the manifest's `allowlist` equals the declared `allowlist`; every manifest check
id is a declared surface id; each check's `url` and `expect` equal the declared ones
exactly; every declared surface appears exactly once (a dropped surface is a failure, not
a smaller population); and `https` is `true`.

## A2 — `--revision`, so "committed bytes" is measurable at a revision

Contract §C2's counter line names `[--revision <rev>]`; the freeze shipped no such flag,
so the verb "re-derives" was worktree-only. `--revision` now exports
`capture-expectations.json`, `capture/**`, `controls/after-c2-audit.txt` and
`scripts/header_audit.py` from the revision into `--work` and evaluates that tree.

## A3 — audit equality is a byte comparison, not line-normalised

The freeze compared normalised lines (trailing whitespace stripped, blank lines dropped).
Now `strip_one_newline(stdout) == strip_one_newline(receipt)` — the receipt must carry the
tool's bytes, not a re-wrapped equivalent.

## A4 — receipt URL identity and final-URL safety

The freeze read the host from the receipt's own `url`. Now the receipt's `url` must equal
the declared surface `url` verbatim, and `finalUrl` must be `https://` on an allowlisted
host. A receipt that redirects the identity elsewhere fails.

## A5 — the named tampered-capture control

Contract §C2's controls name `controls/ctl-c81-tampered-capture.txt`; the freeze shipped
the counter and its tampered selftest fixture but not that receipt file. It is produced
from the **real** capture as soon as the capture lands: copy the capture tree into scratch,
flip one byte of `body.bin` for one surface, run the counter with `--root` on the copy, and
commit `$ <command>`, stdout, `exit=<n>`. The command and the flip are mechanical, not
tailored to any verdict, and the receipt is committed before the measured carrier.

## Selftest after this amendment

`selftest: 18/18 passed` — the ten earlier cases plus `manifest-url-drift-opens`,
`manifest-expect-drift-opens`, `missing-declared-surface-opens` and their audit runs.
Base control re-cut: `C2v1 revision=2e119255… declared=0 surfaces=0 failures=1 met=false`,
exit 1 (the expectations file does not exist at the base).
