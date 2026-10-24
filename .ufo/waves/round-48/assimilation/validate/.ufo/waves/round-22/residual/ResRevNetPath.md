All probes resolved. Both versions' selftests pass; no regression. Compiling the verdict.

## Verdict
**No counterexample found.** The D1 fix (guard at `canonical_audit.py:441-443`: `raw.startswith("//") and not initial.netloc` → reject) holds against every spelling probed, including entity-encoded routes. No remaining false clean, no new false failure; the frozen `scheme_relative` case and all legit network-path forms still pass.

## Findings
None at P0–P2. Two P3 observations, no action required:
- **P3 — tab/newline-in-URL divergence (conservative, pre-existing).** `href="//&#9;project/target.html"` (and literal tab/newline): a WHATWG browser strips ASCII tab/newline from URLs and resolves `https://project/target.html`; the audit rejects as `canonical_url_invalid` (exit 1) in both versions. Page is flagged, never falsely passed — consistent with the documented "whitespace … rejected" subset. No fix needed for D1.
- **P3 — `//#` maps to `canonical_fragment` (exit 1), not `canonical_url_invalid`**, because the fragment check precedes the empty-authority guard. Both versions identical; page still flagged. Cosmetic id difference only.

## Checked and held
Probe harness `/tmp/kake-r22a2-netpath-JTCl/probe.py` (fresh manifests+page per case, public CLI `--manifest <tmp>/manifest.json --json`; pre-fix = `git show c0fd6d5:scripts/canonical_audit.py` snapshot, post-fix = working tree). Exit codes: 0=clean, 1=policy finding, 2=input problem.

| Input (canonical href unless `base:`) | pre-fix | post-fix |
|---|---|---|
| `///project/target.html` (expected=inherited) | **0 clean (false pass)** | 1 `canonical_url_invalid` |
| `//` (expected=document) | **0 clean (false pass)** | 1 `canonical_url_invalid` |
| `////example.test/...` | 1 `canonical_mismatch` | 1 `canonical_url_invalid` |
| `/////x` | 1 `canonical_mismatch` | 1 `canonical_url_invalid` |
| `//?x`, `//?` | 1 `canonical_mismatch` | 1 `canonical_url_invalid` |
| `&#47;&#47;&#47;project&#47;target.html`, `&#x2F;&#x2F;&#x2F;...` (numeric/hex charrefs) | **0 clean (false pass)** | 1 `canonical_url_invalid` |
| `&sol;&sol;&sol;x`, `&#47;&sol;&#47;x` (mixed named) | 1 `canonical_mismatch` | 1 `canonical_url_invalid` |
| `&sol;&sol;project&sol;target.html` → decodes to `//project/...` (netloc=`project`) | 1 `canonical_mismatch` | 1 `canonical_mismatch` (unchanged, correct) |
| base `///project/`, base `//` | **0 clean (false pass)** | 1 `base_url_invalid` |
| base `////evil.test/d/`, base `//?q` | 1 `canonical_mismatch` | 1 `base_url_invalid` |
| base `&#47;&#47;&#47;d/` | 1 `canonical_mismatch` | 1 `base_url_invalid` |
| `//:443/x`, `//:/x`, base `//:443/`, base `//:` | 1 `canonical_url_invalid`/`base_url_invalid` | same (empty-host check in `_host_and_port`, both versions) |
| `//@host/x`, base `//@h/` | 1 url/base invalid | same |
| `/\/`, `//\tx`, `//&#9;x`, `//\nx` | 1 `canonical_url_invalid` | same |
| `http:///x`, `https:/x`, `https:x`, `https://`, `HTTPS:///x`, `HTTPS://` | 1 `canonical_url_invalid` | same |
| `//#` | 1 `canonical_fragment` | 1 `canonical_fragment` |
| `//example.test/project/target.html` (frozen scheme_relative) | 0 clean | 0 clean |
| `//example.test`, base `//base.test/d/`, `//example.test:8443/...` | clean / clean / 0 clean | identical (no new false failure) |

Key mechanics verified: `urlsplit` yields a truthy `netloc` for scheme-less raw only when `raw` starts with `//` plus non-slash, so the `startswith("//")` guard covers exactly the empty-authority set; HTMLParser decodes both numeric charrefs and named `&sol;` in attribute values (verified: attrs parse to `///x` / `//x`), so entity-encoded forms reach the guard in decoded form and cannot bypass it; `URLProblem` is a `ValueError` and is caught per-page, so guard rejections surface as `canonical_url_invalid`/`base_url_invalid` (exit 1), not input errors. `--selftest`: passed=True, zero failed cases on **both** pre-fix and post-fix versions.

## Limits
- Did not exercise D2–D8 (other reviewers' slices). Browser-semantics claims (WHATWG tab-stripping, entity decoding) reasoned from spec/CPython behavior, not a live browser. The 6 pre-fix false-pass rows are evidence of the defect D1 fixed, not new findings. Lane untouched (read-only; `git show` only); probes confined to `/tmp/kake-r22a2-netpath-JTCl`. No tools installed.