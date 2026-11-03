# ExecC1Counter — C1 recorded-counts counter (round 69, W1 + Amendment 1)

Base `4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4`; contract `.ufo/waves/round-69/contract.md` incl. §"Amendment 1" and `w1/L1-amendment-message.md`. Writer clone `/fast/scratch/hyaku/kake-r69/ExecC1Counter/clone`; no lane file edited. Delivered into `.ufo/waves/round-69/w1/ExecC1Counter/`.

## Delivered (Amendment 1)

| File | sha256 | What |
|---|---|---|
| `c69_recorded_counts.py` | `e0c3fb74…a50c94ea` | the counter (new file, 460 lines, mode 100644) |
| `patch.diff` | `d438914d…fbafd7d5` | `git add -N` + `git diff --src-prefix=a/ --dst-prefix=b/`; `git -C <lane> apply --check` exit 0; applying it reproduces the counter byte-for-byte |
| `selftest.txt` | — | 6-fixture selftest: `selftest 6/6`, exit 0 |
| `base-run.txt` | — | base do-nothing control on the FROZEN pairs: `unrelabelled=1 met=false`, exit 1 |
| `attacks.txt` | — | 29 named attacks with verdicts (all exercised) |
| `relabel-demo.txt` | — | exact-row relabel + wrong-integer / substring / absent controls |
| `pairs-frozen.json` | `4e787bcb…a9e9be` | byte copy of `.ufo/waves/round-69/c1/pairs.json` used by the base run and the semantic attacks |
| `attack-*.json`, `pairs-scout-*.json`, `empty.json` | — | attack / demonstration inputs |

## Behaviour (contract §C1 with Amendment 1 terms)

`--root <repo> --revision <rev> --pairs <json>`: each pair's `command` runs with `cwd=<root>` via `subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)`; the first stdout line must be an ASCII integer (else the pair is an error). `mismatch = observed != recorded_value`. `relabelled = mismatch AND correction_locus at --revision is a regular-file blob AND some line of it matches `^\|\s*<correction_id>\s*\|\s*<observed integer>\s*\|` (Amendment 1: exact id token, equal re-derived integer; substring/prefix ids and other integers relabel nothing; regex has no end anchor, so a trailing cell is allowed). `unrelabelled = (mismatches - relabelled) + errors`. Prints `pairs=N mismatches=M relabelled=R unrelabelled=U met=true|false`, then per pair `pair <id> recorded=<n> observed=<n|err> status=<ok|relabelled|unrelabelled|error>`. Exit 0 iff `unrelabelled==0`; 1 otherwise; 2 on usage/IO faults. Temp dirs only via `tempfile.mkdtemp(dir=<--work>)`; zero `/tmp` literal; the pairs file is never written (sha unchanged across runs); no network.

## Evidence (all exercised, exact commands in the receipts)

- `selftest 6/6`, exit 0, 0 entries left under `--work`: (a) match → met/0; (b) no locus → unrelabelled=1/1; (c) exact `| C1-SELFTEST | 2 |` row → relabelled=1 unrelabelled=0 met/0; (d) locus absent → 1/1; (e) id row with wrong integer (`| C1-SELFTEST | 7 |`) → unrelabelled=1/1; (f) id only as substring of `C1-SELFTEST-X` → unrelabelled=1/1.
- Base run with the FROZEN `c1/pairs.json` (sha `4e787bcb…`), predicate shape from the clone: `pairs=20 mismatches=1 relabelled=0 unrelabelled=1 met=false`, exit 1; only `C1-02` (recorded 1, observed 2 at `4b03efe1`) red, 19 rows re-derive. Same with `--root` = the lane. Matches Amendment 1's expected base (exit 1) → mirror kill rule not triggered.
- Relabel demo on scratch tips carrying `corpus/lessons/round-69.md` variants: exact row `| C1-02 | 2 |` → relabelled=1 unrelabelled=0 met=true exit 0; row `| C1-02 | 5 |` → red 1; row `| C1-02X | 2 |` → red 1; correction file absent (base `4d188f94`) → red 1.
- Attacks (all as expected; `attacks.txt`): A1 unicode digits error; A2/A2b 75 s sleep killed at 60 s (`wall=60.08s`); A3 int on line 2 error; A4 blank first line error; A5 undecodable bytes error; A6 `grep -c` 0 with exit 1 is the value 0; A7 pairs-file `observed_value`/`match` ignored; A8 CRLF parses; A9 `+7` parses; A10 negative matches; A11 wrong correction id stays red; A12 directory locus stays red; A13 `../etc/passwd` → fault/2; A14 missing command error; A15 relabel clause on a match never counts; A16 error raises unrelabelled but not mismatches; A17 mixed `(2-1)+1=2`; A18 duplicate ids counted independently; A19 id substring of another id → red (new exact-token rule); A20 unresolvable revision → fault/2; A21 empty array met=true (vacuous); A22 5000-digit line error, no crash; A23 id row naming another integer → red; A24 integer prefix (12 for 2) → red; A25 `|C1-02|2|` relabels; A26 exact row + trailing cell relabels; A27 indented row (not column 0) does not relabel; A28 exact row at the demo tip relabels; A29 frozen pairs at base → red 1.
- Patch replay: fresh clone at base + `git apply patch.diff` → byte-identical counter; `selftest 6/6` exit 0; base run red 1.

## Risks / handoff notes

1. **Row must start at column 0.** Amendment 1's regex is `^\|…`; an indented correction row (A27) relabels nothing. The L1's §Corrections table must be unindented.
2. **Trailing cells are permitted** (A26) because the contract regex has no end anchor; the row must still carry the exact id and the re-derived integer in its first two cells.
3. **Empty pairs array passes vacuously** by the contract formula; the base control is the guard against a wrong pair set.
4. Nonzero command exit with parsable stdout is accepted (A6): required, since `grep -c` exits 1 on a count of 0. Only stdout decides.
5. Relabel is section-agnostic: any unindented line in `corpus/lessons/round-69.md` matching the pattern relabels, not only lines under §Corrections (the amendment bounds it by line shape, not heading).
6. `rev`/`path` in the pairs file are carried for the record only; the command names its revision and `--revision` is used solely for the correction lookup.

Tooling: none installed or upgraded (no pacman, no uv/npx/cargo). Python 3.14.8, git 2.56.0. Scratch `/fast/scratch/hyaku/kake-r69/ExecC1Counter` deleted on exit.
