# Round 38 W1 — SentinelManifestDoS

Axis: operability. Base snapshot: `af43a50fa399881eead9381d835b78a015e277a6`.

## Base run

Command (runner exit 0): `export TMPDIR=/fast/scratch/hyaku/kake-r38w1/SentinelManifestDoS/tmp && prlimit --as=4000000000 timeout 600 /fast/scratch/hyaku/kake-r38w1/SentinelManifestDoS/run.sh /fast/scratch/hyaku/kake-r38w1/SentinelManifestDoS/clone/scripts/robots_audit.py`. Runner applies `prlimit --as=4000000000 timeout 60s python3 "$tool" --manifest "$input"` separately to every fixture. Times are elapsed ms from the runner.

| Input | Size / stress | Exit / time | Observed output |
|---|---:|---:|---|
| `deep-nesting.json` | 6,036 B; 3,000 nested arrays | 0 / 16 ms | `clean` |
| `digits-64m.json` | 67,108,899 B; exactly 64 MiB digits plus JSON wrapper | 2 / 15 ms | `input_invalid` |
| `huge-exponent.json` | 100,037 B; 100,000-digit exponent | 0 / 31 ms | `clean` |
| `long-status-integer.json` | 5,126 B; 5,000-digit status | 2 / 15 ms | `input_invalid` for whole manifest |
| `many-checks-long-urls.json` | 16,979,992 B; 2,048 checks, each URL 8,213 chars | 0 / 38 ms | `clean`, 2,048 evaluated |
| `many-long-numbers.json` | 14,340,132 B; 4,096 integers × 3,500 digits | 0 / 164 ms | `clean` |
| `nonjson-number-literals.json` | 59 B; NaN, Infinity, -Infinity in unused field | 0 / 15 ms | `clean` |
| `unused-long-integer.json` | 5,035 B; unused 5,000-digit integer | 2 / 16 ms | `input_invalid` for whole manifest |
| `url-ascii-pipe.json` | 148 B; `|` in URL path | 0 / 16 ms | `clean`, one check evaluated |

All invocations completed; no timeout, crash, traceback, or memory error was observed. Exit 2 outputs were JSON `could-not-evaluate`/`input_invalid`, not process failures. The 64 MiB digit file is 35 bytes above the 64 MiB manifest cap and is rejected. The two 5,000-digit integer documents are below the file cap but both reject at manifest parse, including the unused integer.

## Findings

- **Moderate — h validation/correctness.** An untrusted manifest containing non-JSON numeric constants in an ignored field returns `clean`, not `input_invalid`. A 5,000-digit unused integer instead rejects the entire manifest; a 5,000-digit `robotsStatus` also rejects globally rather than identifying that check as invalid. Evidence: outputs above; base `load_manifest` size gate and `json.loads`/ValueError handling at `clone/scripts/robots_audit.py:367-408` (SHA-256 `944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`). Likely cause for long integers is the runtime's decimal int conversion limit. Smallest remediation: reject constants with `parse_constant`, and use an integer parser that accepts long tokens so range checking can classify an out-of-range status while leaving unused values inert.
- **Moderate — i URL validation.** An ASCII `|` in a check URL is accepted and produces `clean`; `urlsplit`/hostname validation alone does not enforce the RFC 3986 ASCII character set. Evidence: `url-ascii-pipe.json`, with base URL handling at `clone/scripts/robots_audit.py:439-455` (same source hash). Smallest remediation: reject disallowed ASCII URL characters before URL splitting.
- **Low — resource stress.** The 64 MiB-plus file was rejected quickly; 4,096 3,500-digit values parsed in 164 ms and 2,048 long-URL checks in 38 ms. The 3,000-level ignored value and 100,000-digit exponent also completed without resource failure. No performance failure reproduced at these sizes.

## Artifacts

All input files and runner are in `/fast/scratch/hyaku/kake-r38w1/SentinelManifestDoS/`. Runner SHA-256: `b80d23e77e89794310602b68e7dbf973e4fa11c00d08bcf8fbf447d177836e4f`.

| File | SHA-256 |
|---|---|
| `inputs/deep-nesting.json` | `edd03feaeef9965bdeb9ae26f12510b06f03f76c18a36e0aae2ae031021cf398` |
| `inputs/digits-64m.json` | `4dcf7dba36eb4b1ada7e42911fd045cf1b359e144c245ff4fc2b0d3d7a2ed081` |
| `inputs/huge-exponent.json` | `fff094ce9e7ebb70ca208c0bc106f084187c3cce560d58421b0641bb09e92869` |
| `inputs/long-status-integer.json` | `8e89c52b8afb9fba0c354f62224fa11a6417578a548d98d8825a5ccf4eb828c9` |
| `inputs/many-checks-long-urls.json` | `26077f711f8826bf6193b64e0189bc63477e1221fdc36ed78dc5bc59c90cd2ce` |
| `inputs/many-long-numbers.json` | `bb81587a6bea82bc606781f9775f37de7989c608100aca8a598ca5f8feb8da01` |
| `inputs/nonjson-number-literals.json` | `c0757233c49bc385f7430186cbacf1eed0b59ca00acd8ee0d233e62669f81626` |
| `inputs/unused-long-integer.json` | `e972994748ed6e2aac6a7837e17d5e3053064d903526736186a62b986bd0f84c` |
| `inputs/url-ascii-pipe.json` | `83cff1355514af97e50f2eb7c054d61d29a1cfc4dcb7af6bbfd6782b49fd26e5` |

Not run: build revision, sealed round-38 counters, and `robots_audit_selftest.py`. No tools installed.