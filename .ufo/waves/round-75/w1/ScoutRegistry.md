# ScoutRegistry — C1 population recon (round 75, w1)

Read-only recon of the round-75 C1 population. Base revision
`c9c5e484c533aa65f4374b841a3edcf572ed19a9`; frozen contract `.ufo/waves/round-75/contract.md` §C1.

**Method.** `SKILL.md` read from committed bytes (`git -C <lane> show <rev>:SKILL.md`); rows parsed
with the contract's header regex `^### Round (\d+) gate registry additions`. Every recorded
`--selftest` command ran inside a `git clone --shared` at `<scratch>/tree` (clone toplevel verified
with `git rev-parse --show-toplevel`), with `HOME` and `TMPDIR` under the scratch root, the scratch
root outside the clone, `PATH=/usr/local/bin:/usr/bin:/bin`, `LANG=C.UTF-8`, cwd = the clone.
Host linux-x86_64, `python3` 3.14.8, `/usr/bin/python` → `python3`. No tool installs this seat.
No production file was written in the lane — only this report and `ScoutRegistry.receipts.txt` under
`.ufo/waves/round-75/w1/`; the scratch tree was removed before yield.

## 1. Registry row census (observed)

Ten sections match the header regex: `SKILL.md:1188` (47), `1206` (52), `1224` (55), `1243` (56),
`1263` (57), `1283` (58), `1297` (59), `1379` (67), `1398` (73), `1406` (74).
They carry **28 table rows, 16 live, 12 historical** — exactly the contract's expected counts.

| section round | rows | live |
|---|---|---|
| 47 | 2 | 2 |
| 52 | 2 | 1 |
| 55 | 2 | 0 |
| 56 | 2 | 0 |
| 57 | 4 | 2 |
| 58 | 3 | 2 |
| 59 | 3 | 2 |
| 67 | 1 | 1 |
| 73 | 1 | 1 |
| 74 | 8 | 5 |

Full row list (`Kind family` = the first word of the Kind cell; `historical` = the word appears in
the Kind cell):

| line | round | Name | Kind family | historical |
|---|---|---|---|---|
| 1198 | 47 | `redirect-expectation-audit` | gate | no |
| 1199 | 47 | `commit-citation-lint` | gate | no |
| 1215 | 52 | `wave-evidence-ledger` | gate | no |
| 1216 | 52 | `quote-truth-counter` | gate | yes |
| 1233 | 55 | `readme-index-counter` | gate | yes |
| 1234 | 55 | `yahoo-robots-quote-truth-counter` | gate | yes |
| 1253 | 56 | `selftest-tally-counter` | gate | yes |
| 1254 | 56 | `yahoo-crawl-handling-quote-truth-counter` | gate | yes |
| 1273 | 57 | `receipt-pin-counter` | gate | yes |
| 1274 | 57 | `id-resolver-gate` | gate | no |
| 1275 | 57 | `baidu-dead-link-quote-truth-counter` | gate | yes |
| 1276 | 57 | `source-id-resolver` | tool | no |
| 1293 | 58 | `receipt-rewrite-counter` | gate | no |
| 1294 | 58 | `resolver-cases-counter` | gate | no |
| 1295 | 58 | `baidu-crawler-identification-quote-truth-counter` | gate | yes |
| 1307 | 59 | `axis-evidence-counter` | gate | no |
| 1308 | 59 | `disclosed-route-resolver-cases-counter` | gate | no |
| 1309 | 59 | `crawler-identity-quote-truth-counter` | gate | yes |
| 1396 | 67 | `gate-status-counter-v2-hostportable` | gate | no |
| 1404 | 73 | `c73_tmp_v3.py` | gate | no |
| 1425 | 74 | `c69_recorded_counts.py` | gate | no |
| 1426 | 74 | `c69_tmp_honour.py` | gate | no |
| 1427 | 74 | `c70_pointer_audit.py` | instrument | yes |
| 1428 | 74 | `c71_calibration.py` | instrument | yes |
| 1429 | 74 | `c71_tmp.py` | instrument | yes |
| 1430 | 74 | `c72_tmp_v2.py` | gate | no |
| 1431 | 74 | `c73_wave_pointers.py` | gate | no |
| 1432 | 74 | `c74_registry_gap.py` | gate | no |

Note on the count's sensitivity: `### Round 60 gate-status ledger and registry additions`
(`SKILL.md:1311`, ends before `SKILL.md:1379`) carries 22 further registry-shaped table rows that
this header string excludes, so "28" is header-string-dependent, not "all tables that look like the
registry". Those 22 rows are outside the frozen population and were not measured.

## 2. Instrument derivation (observed, code-level)

Rule as implemented by `.ufo/waves/round-75/c75_row_truth.py` at the freeze commit `88f2e05`
(lines 39–44, 80–91): `FILE_RE = ((?:scripts|\.ufo)/[\w./-]+\.(?:py|mjs))`; the Name cell must
`fullmatch` it; else the first match in the Entry-command cell (index 2); else the first match in the
Self-test cell (index 4); else the first match in the joined cells.

Two consequences worth recording:

- **The Name-cell branch never fires at base.** Six live Name cells are bare basenames
  (`c73_tmp_v3.py` L1404, `c69_recorded_counts.py` L1425, `c69_tmp_honour.py` L1426,
  `c72_tmp_v2.py` L1430, `c73_wave_pointers.py` L1431, `c74_registry_gap.py` L1432). A bare
  basename cannot satisfy a `scripts/`/`.ufo/` prefix, so all six derive through their Entry command.
  The contract prose ("the Name cell when it is itself a `.py`/`.mjs` path") is therefore only
  reachable for prefixed Name cells, of which there are none.
- **No basename resolution is needed** under the frozen regex; deriving `c73_wave_pointers.py` by
  unique basename would have been ambiguous (two copies exist, one under `w1/ExecPointerCounter/`).

The 16 derived files, each with the row line and the cell that yielded it:

| population file | effective row line | source cell |
|---|---|---|
| `.ufo/waves/round-52/c52_wave_ledger.py` | 1215 | entry |
| `.ufo/waves/round-57/c57_idresolver_gate.py` | 1274 | entry |
| `.ufo/waves/round-58/c58_receipt_rewrites.py` | 1293 | entry |
| `.ufo/waves/round-58/c58_resolver_cases.py` | 1294 | entry |
| `.ufo/waves/round-59/c59_axis_evidence.py` | 1307 | entry |
| `.ufo/waves/round-59/c59_resolver_cases.py` | 1308 | entry |
| `.ufo/waves/round-66/c66_gate_status_hostportable.py` | 1396 | entry |
| `.ufo/waves/round-69/c69_recorded_counts.py` | 1425 | entry |
| `.ufo/waves/round-69/c69_tmp_honour.py` | 1426 | entry |
| `.ufo/waves/round-72/c72_tmp_v2.py` | 1430 | entry |
| `.ufo/waves/round-73/c73_tmp_v3.py` | 1404 | entry |
| `.ufo/waves/round-73/c73_wave_pointers.py` | 1431 | entry |
| `.ufo/waves/round-74/c74_registry_gap.py` | 1432 | entry |
| `scripts/citation_lint.py` | 1199 | entry |
| `scripts/id_resolver.py` | 1276 | entry |
| `scripts/redirect_audit.py` | 1198 | entry |

Cross-check: the counter's own `--json` result list is set-equal to these 16 and to the contract's
frozen list (verified in Python; 16 == 16, no extras, no misses).

**The two files a naive any-token scan adds, and the cells that mention them** (same
`scripts/`/`.ufo/` token notion, applied to *every* cell instead of Name → Entry → Self-test):

1. `.ufo/waves/round-46/c46_matrix.py` — `SKILL.md:1198` **Pinned values / frozen proof** cell of the
   round-47 `redirect-expectation-audit` row: `python3 -B .ufo/waves/round-46/c46_matrix.py --root .
   --revision <rev> --stage before|after`. The row's own instrument is `scripts/redirect_audit.py`.
2. `scripts/freshness-sweep.mjs` — `SKILL.md:1426` **Write scope** cell of the round-74
   `c69_tmp_honour.py` row: "… tree with `git archive` under `--work`; runs
   `node scripts/freshness-sweep.mjs` in that tree". The row's own instrument is
   `.ufo/waves/round-69/c69_tmp_honour.py`.

A scan that also resolves bare basenames adds a third: `c51_wave_ledger.py` in the
`SKILL.md:1215` Pinned cell (round-52 `wave-evidence-ledger`) → `.ufo/waves/round-51/c51_wave_ledger.py`.
Under the frozen regex that token is not a path token, so it is not one of the two.

## 3. Execution of the recorded self-tests (observed)

`<scratch>` below is the scratch root; `--work` targets are fresh directories under it. Two of the 16
rows record no self-test command, so 14 commands ran; all 14 exited 0.

| population file | row | command run | exit | observed tally | cell claim | claim re-derives |
|---|---|---|---|---|---|---|
| `scripts/redirect_audit.py` | 1198 | `python3 -B scripts/redirect_audit.py --selftest` | 0 | `selftest: 23/23 passed` | 23/23 | yes |
| `scripts/citation_lint.py` | 1199 | `python3 -B scripts/citation_lint.py --selftest` | 0 | `selftest: 9/9 passed` | 9/9 (cell also discloses the round-47 receipt's then-tally 8/8) | yes |
| `.ufo/waves/round-52/c52_wave_ledger.py` | 1215 | `python3 -B .ufo/waves/round-52/c52_wave_ledger.py --selftest` | 0 | `c52 ledger selftest: 19/19` | "19 fixtures, sandbox repos" | yes |
| `.ufo/waves/round-57/c57_idresolver_gate.py` | 1274 | — none recorded | — | — | "the gate has no selftest of its own"; Kind declares `differential` | E1 substitute satisfied (no E1 finding) |
| `scripts/id_resolver.py` | 1276 | `python3 -B scripts/id_resolver.py --selftest` | 0 | `selftest: 72/72` | "72 checks" | yes |
| `.ufo/waves/round-58/c58_receipt_rewrites.py` | 1293 | `TMPDIR=<scratch>/tmp python3 -B …/c58_receipt_rewrites.py --selftest` | 0 | `c58 receipt-rewrites selftest: 45/45` | "45 checks" | yes |
| `.ufo/waves/round-58/c58_resolver_cases.py` | 1294 | `TMPDIR=<scratch>/tmp python3 -B …/c58_resolver_cases.py --selftest` | 0 | `selftest: ok (7 controls; P7 satisfied on a fixture lane)` | "7 scored control tools" | yes |
| `.ufo/waves/round-59/c59_axis_evidence.py` | 1307 | `python3 -B …/c59_axis_evidence.py --selftest` | 0 | `c59 axis-evidence selftest: 24/24` | "24 checks" | yes |
| `.ufo/waves/round-59/c59_resolver_cases.py` | 1308 | `TMPDIR=<scratch>/tmp python3 -B …/c59_resolver_cases.py --selftest` | 0 | `selftest: ok (13 controls scored; P7 satisfied on a fixture lane) exit 0` | "13 scored control tools over the 21 cases" | yes |
| `.ufo/waves/round-66/c66_gate_status_hostportable.py` | 1396 | `python -B …/c66_gate_status_hostportable.py --selftest` | 0 | `selftest 86/86 passed` | "86 checks" | yes (interpreter caveat below) |
| `.ufo/waves/round-73/c73_tmp_v3.py` | 1404 | `python3 -B …/c73_tmp_v3.py --selftest` | 0 | `C2v3 revision=selftest attack_accepted=0/0 legit_rejected=0/0 selftest=41/41 findings=[] met=True` | no numeric claim (Kind verdict map: "`--selftest` full count") | n/a — nothing to compare |
| `.ufo/waves/round-69/c69_recorded_counts.py` | 1425 | `python3 -B …/c69_recorded_counts.py --selftest --work <scratch>/kake/rc` | 0 | `selftest 6/6` | `selftest 6/6`, exit 0 | yes |
| `.ufo/waves/round-69/c69_tmp_honour.py` | 1426 | — none recorded (`none (no self-test mode; --selftest is an argparse error, exit 2 …)`) | — | `--selftest` run separately: exit 2, `error: the following arguments are required: --root, --revision, --work` | "no self-test mode, exit 2" | the cell's own claim re-derives; the row's **Kind** claim does not → E1 |
| `.ufo/waves/round-72/c72_tmp_v2.py` | 1430 | `python3 -B …/c72_tmp_v2.py --selftest` | 0 | `C2v2 selftest 11/11` | `C2v2 selftest 11/11`, exit 0 | yes |
| `.ufo/waves/round-73/c73_wave_pointers.py` | 1431 | `python3 -B …/c73_wave_pointers.py --selftest --work <scratch>/kake/wp` | 0 | `selftest 6/6` | `selftest 6/6`, exit 0 | yes |
| `.ufo/waves/round-74/c74_registry_gap.py` | 1432 | `python3 -B …/c74_registry_gap.py --selftest` | 0 | `selftest 8/8` | "five frozen fixtures: f1 … f5" | **no** — cell enumerates 5 ids, counter runs 8 (E3) |

**Base counter, re-run** (copy of the freeze-commit file, `--root <lane>`):

```
C1v1 revision=c9c5e484c533aa65f4374b841a3edcf572ed19a9 rows=28 live=16 files=16 mismatches=2 classes=E1 E3 append_only=true met=false
  finding: E1 .ufo/waves/round-69/c69_tmp_honour.py: Kind is gate without a self-test mode or a declared differential
  finding: E3 .ufo/waves/round-74/c74_registry_gap.py: cell enumerates 5 fixture ids, observed total 8
exit=1
```

That **confirms** the contract's base finding `mismatches=2 classes=E1 E3`, and matches
`.ufo/waves/round-75/controls/base-c1-row-truth.txt` modulo that receipt's abbreviated revision
(`c9c5e484`). E3 has code evidence beyond the cell: `.ufo/waves/round-74/c74_registry_gap.py:491`
defines `FIXTURES = (("f1", …), … ("f8", …))` (len 8, verified by import) while its `--selftest`
help string and the registry cell still say "f1-f5".

**Rows whose recorded command is not literally runnable** (measured, not inferred):

| row | cell text | literal result | exact reason |
|---|---|---|---|
| 1426 `c69_tmp_honour.py` | `none (no self-test mode; --selftest is an argparse error, exit 2 …)` | `--selftest` → exit 2 | no self-test branch; argparse requires `--root --revision --work` |
| 1274 `c57_idresolver_gate.py` | "the gate has no selftest of its own; …" | not run (no command) | the row's *Entry* carries `[--fleet <fleet root>]`, a placeholder the counter does not substitute (it substitutes only `<lane>`, `<scratch>`, `--work <dir>` / `[--work <dir>]`); Entry is never executed by E1–E4, so this is inert to the verdict |
| 1293 `c58_receipt_rewrites.py` | `TMPDIR=<scratch> python3 …` | exit 1: `bash: line 1: scratch: No such file or directory` | `<scratch>` in a leading assignment is parsed as an input redirect, not a value |
| 1294 `c58_resolver_cases.py` | `TMPDIR=<scratch> python3 …` | exit 1, same message | same |
| 1308 `c59_resolver_cases.py` | `TMPDIR=<scratch> python3 …` | exit 1, same message | same |
| 1425 `c69_recorded_counts.py` | `… --selftest --work <dir>` | exit 2: `bash: -c: line 1: syntax error near unexpected token 'newline'` | `<dir>` opens a redirect |
| 1431 `c73_wave_pointers.py` | `… --selftest [--work <dir>]` | exit 1: `bash: line 1: dir: No such file or directory` | optional-bracket form plus redirect |
| 1396 `c66_gate_status_hostportable.py` | `python -B …` | exit 0 | runs only because `/usr/bin/python` is a symlink to `python3` (3.14.8) on this host; a host without that alias gets ENOENT. This is the one row not naming `python3`, and its Kind claims Windows-host portability |

**Two implementation notes** (observed in the freeze-commit counter; neither changes the base count):

- E4 prose says "every `.py`/`.mjs` path token in the row's cells resolves"; `measure()` checks only
  the derived instrument path (`cat-file -e <rev>:<file>`). Implementing the prose literally adds no
  finding at base: the 18 distinct `scripts/`/`.ufo/` tokens across the 16 live rows all resolve at
  `c9c5e484`.
- The prose's "effective row" is "the last registry row naming it"; `effective()` takes the last
  **live** row. The two readings agree at base because the 12 historical rows resolve to 12 distinct
  files that do not intersect the population (empty intersection, verified).

Wall time: independent sweep 28.9 s for the 14 commands; counter at base 29.6 s.

## 4. The 12 historical rows (outside the population; no verdict rendered)

| line | row (round) | Kind qualifier | why re-deriving needs its own bounded pass |
|---|---|---|---|
| 1216 | `quote-truth-counter` (52) | green at `1ae8de5d` only; red later "by design" — mirror pins the 148-row registry | needs the registry tree and the 148-row mirror at that past revision |
| 1233 | `readme-index-counter` (55) | green at `64c0ce12` and on the round-58 tree; red from round 59 — `head_changed` needs every round-55-base knowledge file as a byte prefix | needs the round-55 base tree materialised and a byte-prefix comparison across rounds |
| 1234 | `yahoo-robots-quote-truth-counter` (55) | green at `64c0ce12` only; mirror pins 156 rows | needs that revision plus its 156-row mirror |
| 1253 | `selftest-tally-counter` (56) | green at `4cb225fb`; red at this tip only because the audited `scripts/fixtures` tree gained four `quote-class` files after the pin | needs the fixture tree restored to the pin, or a re-derivation of the pin receipt's context |
| 1254 | `yahoo-crawl-handling-quote-truth-counter` (56) | green at `4cb225fb` only; mirror pins 158 rows | needs that revision plus its 158-row mirror |
| 1273 | `receipt-pin-counter` (57) | green from `20217f23` (third after-receipt); red at its own measured revision `32754df7` | whole-ancestry history walk over round-57 receipts |
| 1275 | `baidu-dead-link-quote-truth-counter` (57) | green at `32754df7`; red once a later round appends a registry row — mirror pins 158 rows + the 2 adopted | needs the pre-append registry state and its mirror |
| 1295 | `baidu-crawler-identification-quote-truth-counter` (58) | green at `8d340c15`; C7 pins the round-58 validate scratch, C8 the 160-row mirror, and round 59 grows the registry to 164 | needs the round-58 validate scratch and the 160-row mirror |
| 1309 | `crawler-identity-quote-truth-counter` (59) | green at `b322ccab`; C8 requires the registry minus S425/S426 to equal the 162-row pre-append mirror | needs the pre-append mirror plus the S425/S426 subtraction |
| 1427 | `c70_pointer_audit.py` (74) | `instrument (historical; the round-70 append-only baseline e5f6fd9e is red at the round-74 base; without --base it exits 0 …)` | needs a fixed revision pair (baseline + measured) before the append-only conjunct means anything |
| 1428 | `c71_calibration.py` (74) | `instrument (historical; unevaluable at the round-74 base — stated attack-share population 2, frozen population 1 …)` | needs the round-70 `w1-results.json` plus a decision on which population is authoritative; as landed it exits 2 |
| 1429 | `c71_tmp.py` (74) | `instrument (historical; never met after round 71 — the equal-count guard cannot survive later SKILL.md additions; superseded by c73_tmp_v3.py …)` | needs a frozen `SKILL.md` snapshot at the round-71 measurement, which the superseding v3 counter now covers differently |

## 5. Residual unknowns

- The c66 row's 86 checks are an aggregate only; no per-check enumeration exists in the cell, so the
  internal split was not re-derived.
- c74's f6–f8 are not named in the registry cell; only the `FIXTURES` label list (f1–f8) was read,
  not what each of the three extra fixtures asserts.
- Rows 1294 and 1308 end their output on a fixture score pair (`6/14`, `20/21`), not a check tally.
  E2 does not bind today because neither cell records an `a/b` claim; a future cell that adds one
  would bind to a fixture score rather than a check total.
- Only aggregate verdicts were observed; no per-row timeout behaviour was exercised (all runs were
  well inside the 1800 s the registry allows).
