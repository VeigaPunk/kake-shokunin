# ReviewPinnedSelftest — round 38 wave 2 (falsify)

Seat: `KakeR38.ReviewPinnedSelftest` (leaf). Target: `.ufo/waves/round-38/pinned_selftest.py`
(sha256 `7f5fd17b7d55a1287972901d75979d6e1ccd3b5ae734847a5d349c7f1fa556d0` at `adab4c7`),
`verification/harm/*.json`, `verification/postfix/r37-postfix-selftest-pinned.json` (QUALITY (l),
corpus/QUALITY.md:932-944). Sandbox `/fast/scratch/hyaku/kake-r38w2/ReviewPinnedSelftest/`; clone
at `adab4c7`. Unset GIT_*; TMPDIR sandbox. No tools installed.

## What I attacked
(l) pin honesty: every receipt's `toolSha256`/`selftestSha256`/object-id re-derived from the repo,
plus attempts to make the runner record a wrong pin.

## V1 — receipt pins re-derive (PASS, all)
`git cat-file -p <toolRevision>:<toolPath> | sha256sum` and `git rev-parse --verify <rev>:<path>`
vs receipt fields, for all 5 pinned receipts (`harm/recheck-hardening-at-145a6468.json`,
`harm/recheck-selftest-at-145a6468.json`, `harm/robots-selftest137-at-3ed8e15c.json`,
`harm/robots-selftest194-at-145a6468.json`, `postfix/r37-postfix-selftest-pinned.json`): tool and
selftest sha + object id all MATCH (e.g. postfix tool `944d2f51…d3e5` @ `af43a50f`, oid
`55637e6b…`; robots137 tool `f4d057c4…baace` @ `3ed8e15c`). Counter receipts (no rev fields):
`harm/r37-counter-on-3ed8e15c-tool.json` toolSha256 `f4d057c4…` == sha(`3ed8e15c:scripts/robots_audit.py`);
`harm/r36-counter-on-145a6468-tool.json` `6629d800…` == sha(`145a6468:scripts/source_recheck.py`);
their `counterSha256` (`2ebb39b5…`, `88ec5914…`) == sha of `.ufo/waves/round-37/sealed_count.py`,
`.ufo/waves/round-36/sealed_count.py` at those revs. All pins honest.

## V2 — postfix receipt reproduced (PASS)
`python3 -B .ufo/waves/round-38/pinned_selftest.py --root . --revision af43a50fa399881eead9381d835b78a015e277a6 --tool scripts/robots_audit.py --selftest scripts/robots_audit_selftest.py --out <sb>/repro-postfix.json --exit-file <sb>/repro-postfix.exit`
exit 0; all fields equal the committed receipt (cases 137, passed 137, verdict clean, pins equal);
exit file `0`. `from` `selftestStdoutBytes` (373 vs 373 not compared; 328 only for the 3ed8e15c run).

## V3 — attempts to record a wrong pin
- **Forged summary** (clone `scripts/fake_selftest.py`, sha `43b71736…`, prints `passed:999`, `toolSha256:"0"*64`, `runner:"not-pinned_selftest"`, exit 1): run exit 1, exit file `1`; receipt `toolSha256`/`selftestSha256` = real hashes, `selftestExit` 1, `toolPath`/`tool` = args. Pins are NOT forgeable. BUT the summary DOES overwrite the receipt's `runner` (receipt: `"runner": "not-pinned_selftest"`) and passes through `met`/`predicate`/`passed` — the runner-identity field is spoofable by the measured program. Finding (low): `pinned_selftest.py:240-243` final pin block re-sets pins but not `runner`.
- **PATH-injected fake git** (`<sb>/fakegit/git`, sha `d34945af…`, replies deadbeef… for rev-parse, junk blob / python fake-selftest blob for cat-file):
  `env PATH=<sb>/fakegit:$PATH python3 -B … --root . --revision adab4c7… --tool scripts/robots_audit.py --selftest scripts/fake_selftest.py --out <sb>/pathforged.json --exit-file <sb>/pathforged.exit`
  → exit 0, receipt `passed: 999`, `toolRevision`/`toolObjectId` = `deadbeef…`, `toolSha256` `ee4f8ada…` ≠ real repo sha `f4d057c4…`. A wrong pin IS recordable under environment control: the runner drops `GIT_*` vars but trusts whatever `git` PATH resolves (`GitStore.git`, `pinned_selftest.py:86-99`). Residual risk, not an intrinsic bug; the prescribed verification (V1, real git) catches it.
- Negative inputs (abs path, `a:b`, `--timeout 0`, bad `--root`, `scripts/../` component): all exit 2, error receipt, no pins; `--revision -x` fails in argparse before main → exit 2 but NO receipt written (stale file left; contradicts docstring "in every one of those cases the receipt is still written", line ~35).
- Distinct `--tool-revision 3ed8e15c` on base `af43a50f`: receipt records `toolRevision 3ed8e15c` + `f4d057c4…`, `revision af43a50f` — correct.

## Verdicts
- (l) runner writes `toolRevision`/`toolSha256`/`selftestSha256`, re-derivable: **holds** (V1, V2).
- Postfix pinned re-run 137/137 on `944d2f51…d3e5`: **holds** (V2).
- "Every post-measurement receipt names the tool's sha256": **holds**; caveat: the two counter harm receipts name sha + `/tmp/b.py|/tmp/s.py` only, no revision in-receipt (re-derivable only via filename/scorecard).
- "Cannot record a wrong pin": **overstated as stated** — pins cannot be forged via summary, but (a) the `runner` field is summary-forgeable, (b) a fake `git` on PATH makes the runner record a fully fictitious pin (passed 999/999, deadbeef revision, junk sha) with exit 0. Both reproducible; (b) requires PATH control and is caught by V1-style verification.

## Residual risk / gaps
- Pins bind to bytes handed to the selftest, not to git's word about them; a PATH-controlled or compromised `git` defeats the revision binding. Mitigation: verify with the canonical `git` (done here); consider resolving/echoing `git`'s path or object-id recheck.
- `runner` and summary pass-through fields are unauthenticated; consumers should key off pin fields and the pinned selftest sha only.
- Not run: full re-run of 194/194 and 9/9 harm receipts (pins verified; rerun is `ReviewQualityProvince`'s lane), C2 sealed-counter receipts (not this target).

Evidence: receipts `repro-postfix.json c35b8b8b…`, `forged.json 0d346794…`, `dotdot.json 87d4cb40…`, `distinct.json dab0dea1…`, `timeout.json 1c1a578d…`, `neg.json e59627c2…`, `norev.json c5fe7de5…`, `pathforged.json 0395a0da…` in sandbox.
