# ExecRobotsSelftest — independent selftest for C1 (round 37, wave 1)

Seat: KakeR37.ExecRobotsSelftest (leaf). I did not list, read, stat or search
`/fast/scratch/hyaku/kake-r37/` and did not run the sealed C1 counter. I never opened or waited
for the builder's tool. All work ran in `/fast/scratch/hyaku/kake-r37w1/ExecRobotsSelftest/`
(TMPDIR there); the lane received this report only.

## Deliverables (absolute path + sha256; L1 copies after review)
- `/fast/scratch/hyaku/kake-r37w1/ExecRobotsSelftest/robots_audit_selftest.py` — `0c5b1131afd25dc6052205fd6952f6c39a9500d0a259a091ab6368a7fb25e80f` — to land as `scripts/robots_audit_selftest.py`
- `/fast/scratch/hyaku/kake-r37w1/ExecRobotsSelftest/independent_robots_audit.py` — `3400abd5054bea2ee267bf08fe9841feb46dc8132f6bc4458f65465c6059bdb8`
- `/fast/scratch/hyaku/kake-r37w1/ExecRobotsSelftest/toy_robotparser.py` — `65cc57435f2c1ddb3efebac9fb4ea4e03297c1747ddacb45fdc01dc05bf79628`
- `/fast/scratch/hyaku/kake-r37w1/ExecRobotsSelftest/run_mutants.py` — `dd165f9230bd4fc624f5c5d55c3b9a9960723e858fdc3c737d13a47d644e7df0`
- `/fast/scratch/hyaku/kake-r37w1/ExecRobotsSelftest/mutation-summary.json` — `6753fae65441094ebc6b829d3682102ce002de22a7f844f593ad1574d572f543`
- Retained evidence in the same directory: `final.indep.json`, `out.indep.json`, `out.toy.json`, `out.toy.err`, `out.mutants.log`, `sha256sums.txt`.

## What was built
`python3 scripts/robots_audit_selftest.py [--tool PATH] [--list]`; 131 fixtures built by
`build_fixtures()`, each carrying the quoted contract sentence it tests (`contract` field, shown
by `--list`). Each run materializes the case in a temp dir, snapshots the work tree before/after
(any tool write is a failure), and invokes `python3 -B <tool> --manifest PATH` (or the fixture's
argv) under a 120 s timeout. Judged on exit code, one-JSON-object stdout, `version == 1`,
`verdict`, the multiset of findings on (check, reason), and `checksEvaluated` where stated.
Exit 0 only when every fixture passes; prints `passedOverTotal`; under 60 fixtures or under 6 in
any bullet (a)–(g), verdict → `could-not-evaluate`, exit 2.

Coverage: a13 b18 c11 d16 e16 f27 g15 verdict8 usage7 = 131.

Edges from the mutant table, all covered: exact 512000 read limit on both sides (b01 keeps the
last permitted byte via an allow/disallow tie; b02 drops byte 512001, turning a terminal `$`
literal); SP/TAB-only key and value trim (b09, b10, b11); first `#` (b06); CR/LF/CRLF-only line
ends (b07, b08, b16 with U+2028, b17 with U+000B); ASCII-only folding (b18 key `diſallow`, c10
group `U+212A`); exact user-agent equality (c09); `*` matches empty (d03); prefix from the first
character (d08, d16); normalized-length specificity (e14); allow-wins ties (d10, d11); status
edges 300/399/599/200 (f06, f07, a05, a01) and float/boolean statuses (f09, f10); symlink outside,
symlink inside, sibling-prefix containment, directory and FIFO robots (f23, f24, f20, f21, f22);
exactly 64 MiB valid vs 64 MiB + 1 invalid (g05, g04); non-UTF-8 manifest (g06); report `version`
1 on every report fixture (the M42 analogue scores 7/131). FIFO manifest (g02) is separate.

## Evidence (exact commands, exit codes, observed outputs)
cwd `/fast/scratch/hyaku/kake-r37w1/ExecRobotsSelftest`, `TMPDIR=$PWD/tmp`:
1. `timeout 600 python3 -B robots_audit_selftest.py --tool independent_robots_audit.py` → **exit 0**
   `{"cases": 131, "failed": 0, "passed": 131, "passedOverTotal": "131/131", "verdict": "clean",
   "perContract": {"a":13,"b":18,"c":11,"d":16,"e":16,"f":27,"g":15,"usage":7,"verdict":8}}`
2. `timeout 600 python3 -B robots_audit_selftest.py --tool toy_robotparser.py` → **exit 1**,
   `88/131`, verdict `failed`, 43 named failures: b02 b03 b09 b10 c10 d07 d13 e03 e04 e07 f01 f02
   f03 f04 f05 f11 f12 f13 f14 f15 f16 f17 f19 f20 f22 f23 f26 f27 g02 g04 g09 g10 g11 g12 g13 g14
   u01 u02 u03 u04 u05 u06 u07 (reasons in `out.toy.json`/`out.toy.err`; the FIFO fixtures time it out twice, 245 s total).
3. `timeout 850 python3 -B run_mutants.py` → exit 0; **40 of 42** single-point mutants of my
   independent implementation are killed by the selftest (`mutation-summary.json`: M01–M22,
   M25–M42 all fail; per-mutant fixture named in `firstFailures`).

## Readings I chose (also in the implementation docstring)
1. `/robots.txt` exemption compares the un-normalized path-to-match (path + `?query`) to the
   literal `/robots.txt`; query, case or percent-encoding defeat it.
2. The 512000-byte limit applies to raw bytes before the BOM drop.
3. Containment = `realpath(manifest dir) + os.sep` after `realpath(robots join)`; `""` or a
   directory is not a regular file; the manifest directory is the real directory of the real path.
4. A repeated id counts an earlier check even when that check was invalid for another reason.
5. A missing manifest file is `input_invalid` (exit 2), not usage; usage is any argv other than
   exactly `["--manifest", PATH]`, including `--manifest=PATH` and `--help` (u04, u07 test this).
6. An unreadable (already validated) robots file at evaluation time becomes `check_invalid`.
7. ASCII case-insensitive = fold A–Z only, never Unicode casefold.
8. Absolute URL = parses, scheme http/https (ASCII-insensitive), non-empty host; `%XX` normalization runs over path + query, and reserved characters are never decoded or encoded.

## Risks, limits, not verified
- M23 (kept-escape hex lowercased) and M24 (UTF-8 escape hex lowercased) survive because my
  `normalize()` applies one shared pass to rule and path, so hex case is unobservable black-box
  (measured: M23 → `/%c3%a9` on both sides, M24 → `/%C3%A9` on both). e08/e16 test the sentence
  for tools whose rule and path normalizers differ; I did not invent a fixture that cannot
  separate. A builder tool that lowercases uniformly will pass these two edges by equivalence.
- The selftest judges `checksEvaluated` where stated (contract-explicit); the sealed counter does
  not compare it. The M41 analogue (increment 1→2) dies at 48/131.
- Runtime ~2.6 s on a conforming tool; up to ~4 min against a tool that opens a FIFO (two 120 s
  timeouts). `os.mkfifo` requires a POSIX host; the unreadable-manifest fixture (g15) is skipped
  when euid is 0 (here 1000).
- Not verified: the builder's tool (never run, by design), the sealed C1 counter, no build, lint,
  formatter or lane gate. No installs were made.

Report: .ufo/waves/round-37/w1/ExecRobotsSelftest.md
