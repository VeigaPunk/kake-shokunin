# RerunBase — counter v1 and v2 at base 8eb121c8 (two random seeds each)

Checked statement (SCORECARD.md:2793): "Base scores vary with the seed (1028–1078 measured)" and
(SCORECARD.md:2719-2720) base `8eb121c8` "1049/1434, not met". **Holds.**

## Runs (2026-10-23, `/home/vgpnk/Projects/shokunin/kake-shokunin`)

Prereqs verified: `git rev-parse --verify 8eb121c8^{commit}` → `8eb121c81ffebada064eefcabcd94dd2303d646f`
(exit 0); `command -v bwrap` → `/usr/bin/bwrap`; counter sha256 `2acc443a…67b4` (matches frozen value at
SCORECARD.md:2698); oracle wheel `cdcac127…0917`; Python 3.14.8.

Command per run (4 in parallel, `prlimit --as=4000000000 timeout 900`, receipts in
`/fast/scratch/hyaku/kake-r41w2/RerunBase/`):
`python3 -B <counter> --root . --revision 8eb121c8 --label <label> --out <receipt>` (no `--seed` → counter
draws a random seed from `os.urandom`, recorded in each receipt).

| Receipt | Counter | Seed | passed | cases | met | toolExit | Exit |
|---|---|---|---|---|---|---|---|
| v1-r1.json | c1_count.py | 176967491963390 | 1060 | 1434 | false | 2 | 1 |
| v1-r2.json | c1_count.py | 32856794585998 | 1057 | 1434 | false | 2 | 1 |
| v2-r1.json | c1_count_v2.py | 101806599678861 | 1083 | 1434 | false | 2 | 1 |
| v2-r2.json | c1_count_v2.py | 127578863574466 | 1076 | 1434 | false | 2 | 1 |

All four: `revision` resolved to `8eb121c81ffebada…646f`, `toolSha256` = `4de35f8c…1460e` (round-40 base
bytes, SCORECARD.md:2719), `oracleInvalid` 604–629 of 1434, `note` null (real tool run under bwrap).

byField — v1-r1 loc 516/630 sitemapUrl 544/804; v1-r2 loc 516/630 sitemapUrl 541/804; v2-r1 loc 523/630
sitemapUrl 560/804; v2-r2 loc 522/630 sitemapUrl 554/804.
byComponent (of 239 each) — v1: port 238/238, host 166–168, userinfo 162–168, path 160–162, query
159–165, fragment 164–167. v2: port 238/238, host 171–174, userinfo 165–173, path 165–170, query
164–167, fragment 165–169.

## Findings

- **Statement holds.** Base does not meet on either counter version at two independent random seeds each
  (exit 1 every run). Both v1 scores (1057, 1060) fall inside the recorded 1028–1078 range; v2 scores
  (1076, 1083) are comparable — v2-r1 lands 5 above the stated range, consistent with v2 generating
  end-position insertions and empty components the v1 measurements did not cover (the range documents v1
  only; not a defect).
- No anomalies: counter/ oracle sha256s match the frozen values; the tool ran inside the bwrap sandbox
  (toolExit 2 = the tool's own nonzero exit over generated inputs, `note` null, not a harness failure).
- No installs performed; no tools added. No repo mutation — all git access was read-only.
