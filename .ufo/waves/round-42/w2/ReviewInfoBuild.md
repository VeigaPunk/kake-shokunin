# ReviewInfoBuild — wave-2 review of the L1's build choice and Python 3.10 evidence (round 42)

VERDICT: the attacked L1 choice (ExecBuildIndependent over ExecBuildRegex) and the Python 3.10 evidence hold; no actionable defect found.

## What I checked

1. Python interpreters: `~/.local/share/uv/python/cpython-3.10.22-linux-x86_64-gnu/bin/python3.10` (3.10.22), `.../cpython-3.11.17-linux-x86_64-gnu/bin/python3.11` (3.11.17), `.../cpython-3.12.15-linux-x86_64-gnu/bin/python3.12` (3.12.15), host `python3` (3.14.8).
2. Tools (sha256): regex build `/fast/scratch/hyaku/kake-r42w1/ExecBuildRegex/sitemap_audit.py` = `8a30432dc69a671b9aa53e05c6356dc4ca8c0afb3906aa971e78318232ecbc13`; regex selftest `sitemap_audit_selftest.py` = `57c382b5e0c8baf11ae3bcd7de734a91743747ca043fc4d94ad731da57070f7d`; independent build `/fast/scratch/hyaku/kake-r42w1/ExecBuildIndependent/sitemap_audit_fast.py` = `438afaf0a445e07f3eeb551da18912818e0f9553caa436b941e64e14591c6e8b`; landed tool `scripts/sitemap_audit.py` = `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`; lane selftest `scripts/sitemap_audit_selftest.py` = `bebd834bc43d683950a2891676c5fc1c300395a524ca919f02f290f5dabcda22`.

## Selftest runs (each: `timeout 600 prlimit --as=8000000000 -- <py> -B <selftest> --tool <tool> > sandbox/<run>.log 2>&1`)

| run | python | result | exit |
|---|---|---|---|
| regex build, own selftest | 3.10.22 | PASS 0/235 (tool fails at `re.compile`, sitemap_audit.py:106) | 1 |
| regex build, own selftest | 3.11.17 | PASS 235/235 | 0 |
| regex build, own selftest | 3.12.15 | PASS 235/235 | 0 |
| regex build, own selftest | 3.14.8 | PASS 235/235 | 0 |
| independent build, lane selftest | 3.10.22 | PASS 235/235 | 0 |
| independent build, lane selftest | 3.11.17 | PASS 235/235 | 0 |
| landed tool, lane selftest | 3.10.22 | PASS 235/235 | 0 |
| landed tool, lane selftest | 3.11.17 | PASS 235/235 | 0 |

Direct 3.10 run of regex tool (`python3.10 -B .../sitemap_audit.py`): `re.error: multiple repeat at position 26` — possessive quantifiers `*+` unsupported below 3.11; tool dies at import, exit 1.

## Per checked statement

- SCORECARD.md:3087-3088 "ExecBuildRegex PASS 0/225 under Python 3.10.22 (possessive quantifiers need Python 3.11)" — HOLDS (measured 0/235; fixture count was 225 before the 10 `r42_*` guards were added; same cause, `re.error: multiple repeat`).
- SCORECARD.md:3087-3088 "round-41 tool PASS 225/225, ExecBuildIndependent PASS 225/225 under 3.10.22" — HOLDS (independent build measured 235/235 under 3.10.22 and 3.11.17; L1 receipts `verification/harm/selftest-tip41-py310.txt` / `selftest-build-py310.txt` both PASS 235/235, exit=0).
- "Regex build fails only below 3.11" — HOLDS as tested (fails 3.10.22; passes 3.11.17, 3.12.15, 3.14.8). Unrun: 3.8/3.9 — not needed for the 3.11 boundary.
- `verification/build/info-execbuildregex.json` read: `met: true`, `equalRuns 10/10`, `equalValues 10229`, `toolSha256 8a30432d…` (matches regex tool), `counterSha256 ce2d5a0c…` (matches v3), `ref41Sha256 50287ac6…` (matches tip41), ratios T1 0.937 / T2 1.237 / T3 1.043 / T4 1.073 / T5 1.203 — matches SCORECARD.md:3100-3101 "also met (T1 0.937 … T5 1.203) but fails H5". HOLDS.
- Choice recorded before scoring (commit order) — HOLDS. Commit `1e1da69` (2026-10-23T09:05:44) contains SCORECARD.md:3084 "The build, chosen before it is scored…" and :3091 H5 "added now, stricter, before the build is scored" and contains **zero** `verification/build/` files; commit `721310b` (2026-10-23T09:07:28) adds SCORECARD.md:3095 "Round 42 — build scored" and exactly the four build JSONs (`c1-v3-020bc457-{1,2,3}.json`, `info-execbuildregex.json`). Choice precedes scoring by ~1m44s commit time.

## Findings

None actionable. No defect found in the choice, the 3.10 evidence, or the info-only scoring.

## Gaps / unrun

- I did not run the counter on either build (out of scope; the L1's `c1-v3-020bc457-*.json` and `info-execbuildregex.json` were read, not re-run). Counter receipts on the *chosen* build were not independently verified by me.
- The "fails only below 3.11" boundary was checked on 3.10.22 vs 3.11.17(+3.12/3.14); not on 3.8/3.9.
