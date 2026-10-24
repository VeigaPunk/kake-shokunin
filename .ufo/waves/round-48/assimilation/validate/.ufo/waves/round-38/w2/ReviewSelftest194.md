# Kake R38 W2 — ReviewSelftest194

Axis: **operability**. Attacked the 57 additions to `scripts/robots_audit_selftest.py` at `adab4c7e9ec2178657395f49346f18800ff4796f`.

## Findings

- **Medium — (h) performance bound is not exercised by this selftest.** The public contract says a manifest within the 64 MiB cap, however long its numbers, must finish within 20 s (`SCORECARD.md:2150-2151,2253-2254`). The added h fixtures use at most 6,000-digit literals (`scripts/robots_audit_selftest.py:787-859`); the harness has a 120 s per-case timeout (`:62,1116-1124`). Thus 194/194 does not establish that bound. This is a coverage gap, not a wrong expected result.
- **Per-clause verdicts:** h data semantics — holds (performance-bound gap above); i character validation — holds for the tested representatives; k normalized implicit allow — holds; c-exact group matching — holds; d-match wildcard/anchor/specificity — holds. No wrong expected outcomes among the 57 fixtures. Each expected exit, verdict, finding projection, and `checksEvaluated` agrees with its named sentence (`scripts/robots_audit_selftest.py:151-192,787-1022`; `SCORECARD.md:2149-2160,2252-2256`).
- **Tolerances:** no new fixture specifies an alternate accepted outcome. The harness treats findings as an order-insensitive multiset of `(check, reason)` and ignores extra finding fields (`scripts/robots_audit_selftest.py:1049-1059,1129-1192`); this is consistent with the report contract allowing extra fields. Every new fixture sets `evaluated`. The shortcut passes k01-k09, as expected: the existing shortcut already implements this implicit allow behavior; those fixtures still require the exact contract result.

## Runs

CWD for all commands: `/fast/scratch/hyaku/kake-r38w2/KakeR38.ReviewSelftest194/clone`.
Each exact command below ran with the stated `TMPDIR`; exit codes and observed summaries follow.

| Tool | Exact command | Exit | Observed |
|---|---|---:|---|
| Build | `export TMPDIR=/fast/scratch/hyaku/kake-r38w2/KakeR38.ReviewSelftest194/tmp; prlimit --as=4000000000 timeout 900 python3 -B scripts/robots_audit_selftest.py --tool scripts/robots_audit.py` | 0 | 194/194 |
| Base | `export TMPDIR=/fast/scratch/hyaku/kake-r38w2/KakeR38.ReviewSelftest194/tmp; prlimit --as=4000000000 timeout 900 python3 -B scripts/robots_audit_selftest.py --tool /fast/scratch/hyaku/kake-r38w2/KakeR38.ReviewSelftest194/base_robots_audit.py` | 1 | 149/194; precisely h01-h10, i01-i26, k01-k09 fail |
| Independent | `export TMPDIR=/fast/scratch/hyaku/kake-r38w2/KakeR38.ReviewSelftest194/tmp; prlimit --as=4000000000 timeout 900 python3 -B scripts/robots_audit_selftest.py --tool /fast/scratch/hyaku/kake-r38w1/ExecIndependent/independent_robots_audit.py` | 0 | 194/194 |
| Round-37 shortcut | `export TMPDIR=/fast/scratch/hyaku/kake-r38w2/KakeR38.ReviewSelftest194/tmp; prlimit --as=4000000000 timeout 900 python3 -B scripts/robots_audit_selftest.py --tool /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-37/retained/controls/CtlC1Shortcut-followup-robots_audit.py` | 1 | 150/194; 44 fail: h06-h10, i01-i26, c21, c25, d18-d21, plus b09, b10, c10, c12, d07, d13, d17; all k fixtures pass |

## Evidence / verification gaps

Selftest SHA-256 `bab98f444bdb6b10a375652977beb083c1d28adbed9b60b1857f36f0bec508c1`; build tool `f4d057c4afac885b998de404da8c19f2d5d0a4d754a9d539e49b07d3f36baace`; base tool `944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`; independent tool `ee78ba4656bed0638d1c7df06f267bad6d1f1b6711a4cef2b32e039bb30495b1`; shortcut `61724ead9831776ea70c72cdf6ae25221535b1b74e070665536a249bfebe6f7d`.

Build, base and test were run from a sandbox clone at tip; base bytes were extracted from `af43a50fa399881eead9381d835b78a015e277a6`. No tool installs or lane mutations other than this report. The 64 MiB / 20 s h bound remains unverified by these selftest runs.