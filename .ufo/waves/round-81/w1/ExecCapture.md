# ExecCapture — kake round 81, wave w1, seat report

Verdict: **C2 live half done end-to-end; frozen counter (amendment 2) reports `met=true`, exit 0** — 3 declared surfaces captured once (all HTTP 200), audited offline with `header_audit.py` exit 1 (4 findings), audit receipt byte-exact, chain re-derived from committed bytes with `failures=0`.

## What ran (verbatim commands + exit codes)

1. Population: wrote `.ufo/waves/round-81/population/{ds4cc-primary,ds4cc-robots,ds4cc-sitemap}/fetch.json`, each `{"id": "<dir>", "url": "<declared url>"}`.
2. Capture (exactly one run):
   `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/response_snapshot.py --population /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-81/population --out /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-81/capture` → **exit 0**, stdout JSON summary of 3 captures, no per-surface error, no redirects. Full stdout: `.ufo/waves/round-81/w1/ExecCapture/capture-run.txt` (sha256 `9494fb550665912650d284062c42ce284f01184b2c633833e056612cd8dec74e`); stderr empty (`capture-stderr.txt`).
3. Manifest `.ufo/waves/round-81/capture/manifest.json` (sha256 `b9d46c3311b2c18f60ce7abaf60ba8ac3d65b94b325ef8bbea19e24b208addcb`): version 1, `allowlist` copied verbatim from `capture-expectations.json` (`["ds4cc.com", "www.ds4cc.com"]`), three checks in declared order, each with `id`, `url`, `expect` copied verbatim, `"https": true`, and `"source": ".ufo/waves/round-81/capture/<id>/response.json"`. Nothing else in checks.
4. Audit: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/header_audit.py --manifest .../.ufo/waves/round-81/capture/manifest.json --root .../kake-shokunin > .../.ufo/waves/round-81/controls/after-c2-audit.txt` → **exit 1** (findings exist; accepted range 0–1). stdout byte-exact in `controls/after-c2-audit.txt` (sha256 `cc2fad1f5e4fa5c312fbf17eb251c0c18809b368fe5c786d55d796caeaa937ef`); run record `.ufo/waves/round-81/w1/ExecCapture/audit-run.txt` (sha256 `fcbddfe0a21f296eca4fcf72578ed4c279d50a2927041ee700cb20500d3a2e5c`); stderr empty.
5. Counter: `python3 -B .ufo/waves/round-81/c81_capture_audit.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --work $HYAKU_SCRATCH/kake-r81/ExecCapture/work` (cwd = lane root) → **exit 0**; receipt `controls/after-c2.txt` (sha256 `709331e1d34a020e2a1274977d0ce807906a83b8cadf9b35a3f83a51998b35f1`); stdout copy `w1/ExecCapture/counter-run.txt` (sha256 `c5641dd4ce6223018084a5676c9e5d27fbcd13502c3128ec97fcc93fd5b4bcce`); stderr empty.

## Per-surface result (all fetched 2026-11-04T12:05:06Z, GET, finalUrl = declared url, not truncated)

| id | status | content-type | headerCount | body sha256 (retained `body.bin`) | bytes |
|---|---|---|---|---|---|
| ds4cc-primary | 200 | text/html; charset=utf-8 | 22 | `f2c5d2b3ab34e8e1dd6d08566147664e4dc7d21a5b01acd7943fd719e8342e93` | 78897 |
| ds4cc-robots | 200 | text/plain; charset=utf-8 | 22 | `70f9ea2885def1b2d2117946b6e6256e666f970f018189d8f5414b1ad0264c05` | 62 |
| ds4cc-sitemap | 200 | application/xml | 23 | `55cb947fa2d07f4a39f709b102f0133c94eb351501ec0b6d2263746f487006ef` | 7810 |

Receipt sha256s: primary `ca981d24cd2f06d4ac2361a134ae71b9039911a3266e9ec6254c4aef13ac0576`, robots `7c69a42c3fa4868958a35a338c69bd110f63cae544b6268e48a6a6658e530e5f`, sitemap `897afea4af5f389f6f8c3f4e5033f0ca8414f0f5a05d495eba1fdcbb8b6dfa67`. Each body.bin sha256 equals the `sha256` recorded in its receipt.

## Findings by expectation class (the audit's output, not a pass claim)

- S430 (HSTS): `hsts_present missing` on **all three** surfaces — none sends `Strict-Transport-Security`.
- S431 (CSP): `csp_present missing` on **ds4cc-primary** (declared `csp_present: true`, none sent). robots/sitemap declare `false`; none sent → no finding.
- S432 (XCTO): `xcto_nosniff_value` produced **no finding** on any surface; the header is absent on all three (the class is a value rule, the tool reports nothing for absence).
- S433 (content-type sender rule): satisfied — `content_type_present` holds on all three, no finding.
- S454 (status semantics): all three answered **200**; no absent-resource case occurred, so no non-2xx absence is recorded and none is needed.

Audit stdout (committed byte-exactly to `controls/after-c2-audit.txt`):

```
ds4cc-primary hsts_present missing
ds4cc-primary csp_present missing
ds4cc-robots hsts_present missing
ds4cc-sitemap hsts_present missing
checks=3 findings=4
```

## Counter verdict line

```
C2v1 revision=worktree declared=3 surfaces=3 failures=0 audit_rc=1 met=true
exit=0
```

Amendment 2 (`eccd0f9c`, disclosed `e93d26b7`) was verified present in the worktree before I built anything (git log, counter grep, base control now `declared=0 surfaces=0 met=false`, selftest control `18/18`); the manifest was built to the amended strict-equality rules and the counter accepted it on the first run with zero failures. Kill rules untouched: `controls/base-c81-capture-audit.txt` was not read-modified (it still reads `met=false`); the counter, expectations file and base controls were never edited by this seat.

## Notes for the L1

- No tools were installed or upgraded this seat (none needed); no pacman transaction attempted.
- Network use: exactly three GETs, one per declared URL, no cookies/credentials/body. No other URL contacted.
- Scratch `$HYAKU_SCRATCH/kake-r81/ExecCapture` was copied into `.ufo/waves/round-81/w1/ExecCapture/` and then deleted; verified absent before this report (no scratch residue defect).
- Write scope held: population/, capture/, controls/after-c2-audit.txt, controls/after-c2.txt, w1/ExecCapture/ (+ this report). No git mutation of any kind was run.
