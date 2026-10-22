# KakeR29.RealInputReproduce — real-input capability run, wave 2 falsify

Item attacked: `.ufo/waves/round-29/real-input/` at lane commit 7697990cbca20291f3b0367b8ff4220e93b38b03.
All commands ran in my sandbox clone checked out at that commit:
`/fast/scratch/hyaku/kake-r29/w2/RealInputReproduce/clone` (TMPDIR under sandbox). No lane file
other than this report was written. Tool bytes at the commit:
`scripts/base_path_audit.py` sha256 e32646159b652710be4053bbdb001c3d11929ef63b055b7f57545231ac6965aa,
`real_input_run.py` sha256 324be40fd47e050f41cd2a65e7b4026ba3a52df8fc1ef8f131beffeeaa8d4bd0.

## 1. Snapshot identity: real-input page.html vs round-23 live page.html — EQUAL
- `git show 7697990:.ufo/waves/round-29/real-input/sites/<s>/page.html | sha256sum` vs the
  round-23 twin, then `cmp` on the checked-out pair (exit 0 all three):
  - charter-ghp 7c243a1d81357cdee71520034a05d540bfe8f69c702a7a1c95f8a0bfa5237aba
  - lucario-ghp bee2d9f5b5777768e69a5b9aaa9c28dfcc4107f57a4dfb6ec8726d9685c46cff
  - plazir15-ghp d82af77aee401d2270c719c6e818256298cc8aad7a71c3e7c4d65bd41f6af18e
- Verdict: byte-identical for all 3 sites.

## 2. fetch.json vs declared base path — CONSISTENT (recorded data only)
For each `.ufo/waves/round-23/live/<s>/fetch.json`: recorded `sha256` equals the stored
page.html hash, recorded `bytes` equals file size (53660 / 3435 / 38337), `status` 200,
`redirects` empty, and the `finalUrl` path equals the manifest `basePath` exactly:
`/charter-ufo-fsd/`, `/lucario/`, `/plazir-15-site/`
(`sites/<s>/manifest.json:4`, fetch.json `finalUrl`). No live probe was made — bounds
forbid probing owned properties, so this is internal consistency of the stored records.

## 3. Rerun with the landed tool — REPRODUCES
Command (exit 0):
`TMPDIR=<sandbox>/rerun/tmp python3 -B .ufo/waves/round-29/real-input/real_input_run.py --tool scripts/base_path_audit.py --sites .ufo/waves/round-29/real-input/sites --out ../rerun/out`
Printed table and totals match the committed out/summary.json exactly:
charter-ghp exit 1 failed-policy 1 page 67 refs 3 findings; lucario-ghp exit 0 clean
1 page 1 ref 0; plazir15-ghp exit 1 failed-policy 1 page 46 refs 1; totals sites=3
pagesChecked=3 referencesChecked=114 findings=4 failedSites=2 contractProblems=0.
Field-level compare of rerun vs committed `out/*.json` after normalizing the absolute
path prefix (author lane path vs sandbox path): `charter-ghp.json`, `lucario-ghp.json`,
`plazir15-ghp.json` IDENTICAL in every field (exit, stdout, stderr, result,
stdoutNotJson). `summary.json` differs only in the `outRoot` path echo (sandbox output
location), as expected.

## 4. Findings are real bytes, not canned output — CONFIRMED
- charter-ghp 3 `outside_base_path` findings are genuine `<a href>` cross-links present in
  the page bytes: horizon-halo-comma-design at physical lines 251 and 258, plazir-15-site
  at line 425. plazir15-ghp's single finding targets xbrd-spark/highlights.html at line 338.
- Finding ids (`page.html#21`, `#27`, `#54`, `#38`) are 1-based reference ordinals, not
  line numbers (`enumerate(references, start=1)` scripts/base_path_audit.py:577, id built
  at :586); each ≤ that site's referencesChecked (67/46) — internally consistent.
- lucario's referencesChecked=1 is its single `<script src>` to cdn.jsdelivr.net
  (cross-host, outside "ours"), so verdict clean. Matches `REFERENCE_ATTRIBUTES`
  (scripts/base_path_audit.py:76-92).

## Verdict
HOLDS. The committed real-input run reproduces exactly from committed bytes with the
committed tool: snapshots byte-identical to round-23 live, fetch records consistent with
declared base paths, and rerun outputs identical modulo path echoes. No defect found.

## Not verified
- Live availability/freshness of the three URLs today (no live probes of owned properties
  per bounds); freshness rests on the recorded fetchedAt 2026-10-21 and matching hashes.
- Authenticity of round-23 fetch.json against the real web at fetch time (same bound).
- Tool contract beyond these three pages (C2 seat scope); selftest battery not rerun here.

Tooling: no installs (system python3 only). No pacman use.
