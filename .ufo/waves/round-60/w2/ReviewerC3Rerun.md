# ReviewerC3Rerun

ATTACKS: C3 frozen quote-truth command and selftest at B1; live source reopens; Gate quote occurrence check.

RUNS:

- In a detached `--shared` scratch clone at B1, ran `python3 -B .ufo/waves/round-60/c60_quote_truth.py --root . --revision 8b33fd248d126b48d838af5c38bc175850f41a09` → exit 0, `C3 quote-truth 9/9 met=True`; C1–C9 all PASS.
- Ran `python3 -B .ufo/waves/round-60/c60_quote_truth.py --selftest` → `140/140 (baseline exit 0, 9/9 conditions; 129 fixtures, 125 red, 4 green)`.
- `corpus/lessons/round-60.md` § Gate presents two quoted spans each for S427, S428, S429. The counter's successful C5 run establishes its validated quote checks; I did not independently execute a substring-occurrence-count script. Exact once-per-quote occurrence is therefore **not independently verified** here.

LIVE:

- Re-opened S428 and S429 with `curl -sL --compressed`; returned bodies had SHA-256 `4ae6131cec75148391f57995d5c0286e8d21b58be96942f811d457627765209f` and `7414d25972719f51ae2bf6d1efe116ad004405ad229d49679c9aa9606832b2`, respectively. Retained receipts pin `0f296b...` (76197 bytes) and `423d99...` (178797 bytes), so the live byte bodies differ from retained snapshots. S427 was not fetched live: the command used its overview URL path incorrectly as `/googlebot`; therefore its live status/content was not checked. Hash command: `sha256sum S427.live S428.live S429.live` in `/fast/scratch/hyaku/kake-r60/ReviewerC3Rerun`.
- This is not itself evidence of quote falsity: dynamic page bytes may vary. No live DOM/text-node extraction or comparison against retained bodies was performed. [INFERENCE] The changed hashes make a direct live quote comparison necessary before asserting current-page quote persistence.

FINDINGS:

| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| low | `.ufo/waves/round-60/lessons.md:21-23` | Exact once-per-quote Gate occurrence was requested but not independently counted; frozen counter PASS was observed, not an occurrence-frequency audit. | `python3 -B .ufo/waves/round-60/c60_quote_truth.py --root . --revision 8b33fd248d126b48d838af5c38bc175850f41a09` → 9/9 PASS | Count each Gate quote occurrence within its corresponding retained body and report results. |

VERDICT: No actionable C3 counter/selftest defect found; live byte bodies differed from retained snapshots and S427 was not live-checked, leaving requested live text comparison incomplete.
