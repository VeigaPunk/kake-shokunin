# Round 37 W2 — `robots_audit.py` hostile inputs

**Axis:** operability. **Verdict:** one confirmed hang in wildcard matching; tested path, size, malformed-data, and 100k-check cases otherwise returned one report with the expected CLI exit.

## Target and method
- Audited commit `9dbc88bb3aaafba15569b54387737e4880191045` (`round-37: C1 build`); it matches measured tip `79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c`. Script SHA-256: `5eb767ec68a649145102619ed13754428bef489e432ed50eb20e9e50542cabae`.
- Ran in isolated clone `/fast/scratch/hyaku/kake-r37w2/SentinelRobotsInputs/clone`; fixtures/logs are under `/fast/scratch/hyaku/kake-r37w2/SentinelRobotsInputs/fixtures/`.
- `/usr/bin/time` was absent; used pre-existing GNU Time 1.9 at `/home/vgpnk/.local/bin/time`, with `-v`. Each invocation was `time -v -o fixtures/logs/<case>.time timeout --signal=TERM --kill-after=1s <limit>s /usr/bin/python3 -B <clone>/scripts/robots_audit.py --manifest <M>`; `M` is the literal relative path in the table, prefixed by the fixture root (or `/dev/zero`). All completed cases emitted exactly one JSON line and had empty stderr; exit is the observed process/time exit.

## Results
| Input (`M`; sizes where relevant) | Limit | Wall | Max RSS KiB | Exit; output/verdict |
|---|---:|---:|---:|---|
| `manifest_fifo/manifest.fifo` | 25s | 0.02s | 13,232 | 2; JSON, input_invalid |
| `/dev/zero` manifest | 25s | 0.02s | 13,464 | 2; JSON, input_invalid |
| `robots_fifo/manifest.json` | 25s | 0.01s | 12,980 | 2; JSON, check_invalid |
| `robots_devzero_link/manifest.json` | 25s | 0.02s | 13,464 | 2; JSON, check_invalid |
| `robots_devzero_abs/manifest.json` | 25s | 0.01s | 13,440 | 2; JSON, check_invalid |
| `manifest_64m_plus_1/manifest.json` (67,108,865 B) | 25s | 0.02s | 13,440 | 2; JSON, input_invalid |
| `robots_1gib/manifest.json` (1,073,741,824 B robots) | 25s | 0.02s | 14,704 | 0; JSON, clean |
| `manifest_symlink_loop/manifest.json` | 25s | 0.02s | 12,904 | 2; JSON, input_invalid |
| `robots_symlink_loop/manifest.json` | 25s | 0.02s | 13,440 | 2; JSON, check_invalid |
| `robots_symlink_escape/manifest.json` | 25s | 0.02s | 13,468 | 2; JSON, check_invalid |
| `deep_json/manifest.json` (2,000 nested arrays) | 25s | 0.02s | 13,716 | 2; JSON, check_invalid |
| `deep_json_100k/manifest.json` (100,000 nested arrays) | 25s | 0.02s | 24,692 | 2; JSON, input_invalid |
| `checks_100k/manifest.json` (9,988,914 B; 100,000 findings) | 120s | 0.32s | 82,736 | 1; JSON, failed-policy |
| `wildcard_backtracking/manifest.json` | 3s | 3.00s | 13,456 | 124 (timeout); **no JSON** |
| `wildcard_matchcontrol/manifest.json` | 25s | 0.13s | 13,272 | 0; JSON, clean |
| `manifest_nul/manifest.json` | 25s | 0.02s | 13,464 | 2; JSON, input_invalid |
| `url_nul/manifest.json` | 25s | 0.02s | 13,348 | 0; JSON, clean |
| `robots_nul/manifest.json` | 25s | 0.02s | 13,464 | 0; JSON, clean |
| `robots_path_nul/manifest.json` | 25s | 0.02s | 12,916 | 2; JSON, check_invalid |
| `manifest_invalid_utf8_url/manifest.json` | 25s | 0.02s | 12,908 | 2; JSON, input_invalid |
| `robots_invalid_utf8/manifest.json` | 25s | 0.02s | 13,464 | 0; JSON, clean |
| `url_surrogate/manifest.json` (escaped lone surrogate) | 25s | 0.01s | 13,464 | 0; JSON, clean |
| `robots_long_line/manifest.json` (4,194,330 B robots file; >4 MiB rule line) | 25s | 0.06s | 20,020 | 0; JSON, clean |

For the 1 GiB robots file, `timeout 30s strace -qq -f -yy -s 0 -e trace=read -o fixtures/logs/robots_1gib.strace /usr/bin/python3 -B <clone>/scripts/robots_audit.py --manifest <fixture-root>/robots_1gib/manifest.json` exited 0. Trace shows seven 65,536-byte reads plus one 53,248-byte read: **512,000 bytes total**, no more.

## Findings
- **High — confirmed wildcard backtracking DoS; verdict: wrong for operability.** The 191-byte manifest points at a 76-byte rule `Disallow: /` + `*a`×24 + `z$` and path `/` + `a`×48 + `x`. It consumed the full 3-second cap, exited 124 via `timeout`, emitted no JSON, and was killed. Same rule against the positive-match control ending in `z` completed in 0.13s (exit 0). Reproducer: `/home/vgpnk/.local/bin/time -v -o /fast/scratch/hyaku/kake-r37w2/SentinelRobotsInputs/fixtures/logs/wildcard_backtracking.time timeout --signal=TERM --kill-after=1s 3s /usr/bin/python3 -B /fast/scratch/hyaku/kake-r37w2/SentinelRobotsInputs/clone/scripts/robots_audit.py --manifest /fast/scratch/hyaku/kake-r37w2/SentinelRobotsInputs/fixtures/wildcard_backtracking/manifest.json`. Source constructs `.*` regexes then calls `fullmatch` at `scripts/robots_audit.py:275-288`. Impact: a caller auditing an untrusted robots file can be held indefinitely absent an external timeout. **Smallest remediation:** replace regex matching with a linear-time wildcard matcher preserving `*`, prefix, and `$` semantics. Fixture SHA-256: manifest `e632c976e2dd837a281c2ce5fc36444a99759ff5510a7f808eb091400951d015`; robots `b551a39ed0f6e877a971a65060a7179fb4372dc82dfc84941a547fa4d97d5e5d`.
- **Low — observed check-count memory amplification; verdict: 100k case holds, larger-scale impact unverified.** The valid 9.99 MB manifest processed 100,000 checks in 0.32s, returned the expected exit 1 and one JSON line (3,788,968 B), but max RSS was 82,736 KiB. **[INFERENCE]** Since `audit_manifest` retains findings for every check (`scripts/robots_audit.py:463-540`) and there is no check-count limit in the input validation (`:354-395`), larger allowed manifests can increase memory/output pressure; OOM was not tested. Smallest remediation if bounded-resource behavior is required: enforce an explicit check-count limit.
- **Holds on tested cases:** FIFO/device files, oversized manifest, symlink loop/escape, NUL, malformed UTF-8, 100k checks, long line, and 1 GiB file all returned the expected input/policy/clean exit and one JSON report when not timed out. Bounds are visible at `scripts/robots_audit.py:84-86,316-395,402-423`; invalid UTF-8 replacement is at `:167-172`.
