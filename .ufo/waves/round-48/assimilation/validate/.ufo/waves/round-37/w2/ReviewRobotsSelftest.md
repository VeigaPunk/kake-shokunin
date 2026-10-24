# ReviewRobotsSelftest — r37 wave 2 (falsify), operability
Target: `scripts/robots_audit_selftest.py` at 79d3c780 (sha256 0c5b1131…; landed tool sha256 5eb767ec…, the SCORECARD.md:1987 hash). Sandbox `/fast/scratch/hyaku/kake-r37w2/ReviewRobotsSelftest/` (clone checked out at 79d3c780, TMPDIR=sandbox/tmp). No installs. No lsp server was used: the target is a standalone script, so I checked callers and definitions by reading it directly.

## Verdicts
- "Every fixture's expectation follows the contract sentence it quotes": **holds**. I derived all 131 expectations myself from SCORECARD.md:1796-1857; 131 agree and 0 disagree. All 11 quoted CONTRACT strings match SCORECARD verbatim apart from markup (backticks and quote style; the verdict quote capitalises "Any").
- "any tool write is a failure" (w1/ExecRobotsSelftest.md:20): **overstated**. Only *new paths under the selftest's temp dir* are detected (selftest:739-740, 789-804).
- "Judged on … `version == 1`" (w1 report:21): **overstated**. Python `==` accepts `true` and `1.0` (selftest:830, 862).
- ≥6-per-bullet gate (selftest:919-931): **holds**. It is a label count, not a count of rules tested.
- Run results in SCORECARD.md:1989-1993 and w1 report:41-47 (131/131 landed, 126/131 shortcut, 119/131 naive reader, toy 88/131 with 43 named failures): **hold**. All four reproduce exactly.

## Runs (cwd = sandbox; `timeout 900 python3 -B clone/scripts/robots_audit_selftest.py --tool T`)
| T | exit | result |
|---|---|---|
| landed `scripts/robots_audit.py` | 0 | 131/131 clean; perContract a13 b18 c11 d16 e16 f27 g15 verdict8 usage7 |
| `retained/independent/independent_robots_audit.py` | 0 | 131/131 clean |
| `retained/independent/toy_robotparser.py` | 1 | 88/131 failed; failure set identical to w1's list of 43 |
| `retained/controls/CtlC1NaiveReader-robots_audit.py` | 1 | 119/131; failure set equals receipt `verification/robots-selftest-on-CtlC1NaiveReader.json` |
| `retained/controls/CtlC1Shortcut-followup-robots_audit.py` | 1 | 126/131 (b09 b10 c10 d07 d13); equals receipt |

FIFO timing: the toy blocks in `open()` on f22 (robots FIFO) and on g02 (manifest FIFO). Each one ends as "tool could not run: … timed out after 120 seconds" (run-toy.json), and the toy run took 247.59 s in total (measured wall time, exit 1). This fails closed and matches w1's "245 s". Residual risk: a tool that hangs on every fixture would take 131 × 120 s, about 4.4 h, because the selftest has no overall deadline. A tool that opens the robots FIFO with O_NONBLOCK reads it as empty, gets "allow" and still fails f22, as it should. For g02 the same approach gives "not JSON", which matches the expected outcome anyway.

## Judge review, with mutation evidence (wrappers around the landed tool in sandbox `mut/`)
1. **Medium: the write check sees only creations.** It compares path sets under `work`, so in-place edits, deletions and writes outside `work` all pass. `m_writes.py` appends to each case's robots.txt and to `$TMPDIR/kake-r37w2-leak-marker` (121 lines written): exit 0, 131/131. `m_delete_robots.py` unlinks robots.txt after the run: exit 0, 131/131. The contract's "no writes" (SCORECARD.md:1802) is not enforced beyond file creation inside the temp tree.
2. **Low: version and count accept look-alike values.** `m_version_true.py` emits `"version": true`, and `checksEvaluated` as `true` or a float: exit 0, 131/131. The contract requires the integer 1 and an integer count.
3. **Low: crash on a malformed finding.** `m_reason_missing.py` adds `{"check": id}` with no `reason`. `project()` then calls `sorted()` on a mix of None and str and raises `TypeError` (selftest:732; only ValueError is caught at 846). Exit 1 with a traceback and an empty stdout: no JSON summary and no per-case failures. It fails closed, but the report is lost.
4. **Low: a missing `check` key counts as null.** `m_missing_check_key.py` drops the key from null-check findings: exit 0, 131/131. The contract's finding shape is `{"check": …, "reason": R}`.
5. **Info: dead code.** The `accept=`/`alt()` alternative-outcome path is used by none of the 131 fixtures (selftest:140, 165-167, 806-812).
6. Exit-first ordering, the verdict check, the multiset projection (`json.dumps(check)` keeps null distinct from "null"), the unknown-reason check and the exit-64 fixtures skipping stdout are all correct against the contract.

## Gate mutation (`gate_mut.py`; loads the selftest and edits FIXTURES before `main`)
| change | exit | result |
|---|---|---|
| c kept to 5 | 2 | "contract c has 5 fixtures; expected at least 6" |
| c kept to 6 | 0 | 126/126 |
| verdict kept to 5 | 2 | — |
| total cut to 59 | 2 | "only 59 fixtures" plus four bullet shortfalls |
| all usage fixtures removed | 0 | 124/124 (usage is not gated, and the docstring does not claim it is) |

The gate counts the `contract` label, so it cannot see which rule a fixture actually exercises. Mislabels I found: a13 and f25 test the Manifest sentence "Otherwise robots is ignored", and d15 tests (b)'s "text before the first `:`". Recounting by the rule actually tested, every bullet still has at least 6. The `manifest` and `findings` CONTRACT entries have no fixtures under their own labels.

## Fixture sensitivity (expectation correct, but the fixture does not discriminate)
- **b05 (low).** Contract (b) says invalid bytes become U+FFFD. Mutant `mutb/m_ignore.py` (one line: `decode("utf-8","replace")` → `"ignore"` at robots_audit.py:171) scores 131/131, exit 0. The cause: the rule `/bad` (byte dropped) still prefix-matches the URL `/bad%EF%BF%BD`. A fixture that would kill it: rule `disallow: /bad\xff`, URL `/bad`, expect allow, expected clean.
- Not covered at all: whether a BOM counts toward the 512000 bytes; manifest `version: 1.0`; manifest with no `checks` key.

## Per-fixture derivations (all 131; A = agree)
- (a) a01-a13 A. 2xx: the file decides. 4xx: allowed (a02, a03, a09 give exposed; a13 ignores a bogus robots path). 5xx: blocked, including /robots.txt (a04, a05, a08, a10, a11). Status edges 204, 250, 299 are in range.
- (b) b01 A: exactly 512000 bytes keeps the final `j`, so the allow/disallow tie goes to allow (a limit of 511999 would leave disallow longer and block). b02 A: byte 512001 `X` is cut, so `/exact$` is anchored and expect disallow is clean. b03 A: a leading BOM is dropped. b04 A: a BOM mid-file is not trimmed, so the key is not `disallow`. b05 A (weak, above). b06 A: everything from the first `#` is removed. b07, b08 A: CR and CRLF end lines. b09, b10 A: NBSP is not trimmed (the key is not user-agent; the value becomes `%C2%A0/x`). b11 A: space and tab are trimmed. b12 A: no colon, line ignored. b13 A: `sitemap` neither counts as a record nor ends the group, so `other` joins bot's group. b14 A: a rule before the first user-agent is ignored, and the `*` group is empty. b15 A: keys fold ASCII case. b16, b17 A: U+2028 and VT are not line ends, so the group name is `*…disallow: /x`, which matches nothing. b18 A: `ſ` is not ASCII-folded.
- (c) c01-c11 A. Names compare by ASCII-case-insensitive equality (c01; c09 is not a substring match; c10 Kelvin sign ≠ k). Fall back to `*` only when nothing matches (c02, c05, c07). No group, or no match and no `*`: allowed (c03, c04). Consecutive user-agent lines form one group (c06). Matching groups combine, so in c08 `/x`(2) beats `/`(1).
- (d) d01-d16 A. An empty value or one emptied by trimming never matches (d01, d02). `*` matches the empty string (d03, d14) and runs of characters (d04). A trailing `$` anchors (d05, d06); any other `$` is literal (d07). Matching is a prefix from the first character (d08, d16). The longest rule wins (d09). Ties go to allow (d10, d11). No match: allow (d12). `$` counts in length, 5 > 4 (d13). The value after the first `:` keeps later colons (d15).
- (e) e01-e16 A. An empty path is `/` (e01). A non-empty query is kept, an empty one dropped, and the fragment dropped (e02-e04). Unreserved escapes decode, %62%61%7A, %7E and %31 included (e05, e13, e15). Reserved escapes are kept and uppercased; %2F ≠ / (e06-e08). Non-ASCII is percent-encoded from UTF-8 octets on both sides (e09, e10, e16). The /robots.txt exemption is exact and case-sensitive (e11, e12). e14: both rules normalise to 7 octets, so allow wins the tie.
- (f) f01-f27 A. A non-object check or a missing, empty or non-string id gives a null check (f01-f04). Repeated id k1: the first is evaluated (404, allow, no finding), the second is check_invalid, evaluated=1 (f05). Statuses 300, 399, 600, 200.0 and true are invalid (f06-f10). User agents `bot7`, `bot!` and the empty string are not product tokens (f11-f13). `Allow` is not an expect value (f14). Relative, ftp and hostless URLs are invalid (f15-f17). Robots paths that are missing, absolute, in a sibling-prefix dir, a dir, a FIFO, a symlink outside, or not a string are invalid (f18-f23, f26). A symlink inside is valid (f24). robots is ignored for 5xx (f25). Other checks are still evaluated (f27).
- (g) g01-g15 A. Each gives input_invalid with a null check, evaluated 0: missing, FIFO, dir, >64 MiB, not UTF-8, not JSON, empty, `[]`, version 2, "1", true or absent, checks `{}`, unreadable (g15 is skipped when run as root). Exactly 64 MiB is valid, clean, evaluated 0 (g05).
- verdict v01-v08 A (precedence and exit codes, two findings, empty list clean, relative manifest path). usage u01-u07 A: anything other than exactly `--manifest PATH` exits 64, including `--manifest=P`, `--help` and two pairs.

Residual: network use is not checked by the selftest, and I did not test it. A second toy rerun was killed by me after 225 s (exit 143, empty output) and is not used; all my processes are stopped (`pgrep` finds none).
