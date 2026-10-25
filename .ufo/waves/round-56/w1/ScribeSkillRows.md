# ScribeSkillRows

Round-56 W1, SKILL.md gate-registry draft: one new section with two eight-cell rows and the
Self-test cell replacement for each of the ten rows the C1 counter (`c56_selftally.py::POP`) pins.
Base `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`, contract commit `2d308e808bfd`, round date 2026-10-25.
No lane file was edited: the draft was applied and measured only in a `/tmp` clone.

## NEW SECTION:

Append at the end of `SKILL.md` (after line 1242, the round-55 withdrawal-rule paragraph), verbatim:

```markdown
### Round 56 gate registry additions

Round 56 ships two counters whose predicates are frozen in `.ufo/waves/round-56/contract.json`
before any data; both are offline and read committed bytes only. C1 calibrates the ten self-test
tallies in the registry above (the round-55 routed defect) and C2 is the freshness claim for three
Yahoo! JAPAN crawl-handling entries. Receipts: `.ufo/waves/round-56/controls/`.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| selftest-tally-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision <commit>` | `0=met` (`tally_mismatches == 0 AND rows_checked == 10`); `1=not met` (any row_missing, command_missing, claim_missing, tool_changed, selftest_failed or claim_ne_observed); `2=could-not-evaluate` (revision unresolved, clone or command failure, unparsable tally, timeout); `64=usage` | `python3 -B .ufo/waves/round-56/c56_selftally.py --selftest` (20/20, generated sandbox repos; observed at contract commit `2d308e80`) | `contract.json` `claims.C1.predicate`; base control `.ufo/waves/round-56/controls/base-c1-selftally.txt` (`tally_mismatches=7 rows_checked=10`, exit 1 at `e48354b7c26b`); population is `POP` in the counter | none (reads `git show` / `git rev-parse`; selftest writes only `mktemp -d` sandboxes and removes them) | kake |
| yahoo-crawl-handling-quote-truth-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision <commit>` | `0=met` (`conditions_passed == 8 of 8`); `1=not met` (any C1–C8 sub-condition fails); `2=could-not-evaluate` (malformed receipt or mirror-pin JSON, an exception); usage errors also exit 2 (`ap.error`) | `python3 -B .ufo/waves/round-56/c56_quote_truth.py --selftest` (stub: exits 2 until the round-56 fixtures are integrated) | `contract.json` `claims.C2`; base control `.ufo/waves/round-56/controls/base-c2-quote-truth.txt` (`0/8`, exit 1); retained bodies `.ufo/waves/round-56/sources/` (`S367`, `S419`, `S420`) with `receipts.json`; pre-append mirror pin `.ufo/waves/round-56/assimilation/mirror-pin.json` | none (reads `git show` / `git log` only; selftest writes only `mktemp -d` sandboxes) | kake |

The C1 counter runs each row's documented self-test command — a leading `VAR=value` word in the
backticked span is part of the command — in a `git clone` of the measured revision, and compares the
sum of the claim integers in that row's Self-test cell with the printed tally. A rewritten selftest is
a different claim: the pinned script's blob must equal its blob at `e48354b7c26b`. Round 56 rewrites
the seven cells whose claim disagreed with the observed tally and leaves the three that already
agreed. Withdrawal rule: a row goes when its counter leaves the tree.
```

Both rows carry all eight cells (`Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner`), confirmed by parsing the drafted file with the counter's own `table_rows`: 8 cells each. The Self-test cell of `selftest-tally-counter` states `python3 -B .ufo/waves/round-56/c56_selftally.py --selftest` with the **20/20** the counter prints at `2d308e80`; the C2 row's cell states the stub honestly (`exits 2 until the round-56 fixtures are integrated`).

## CELL REPLACEMENTS:

Only the Self-test cell (cell index 4) of the seven changed rows differs; every other cell is byte-identical. `line` = line number at the base revision (SKILL.md is identical at base and at `2d308e808bfd`). Claim-regex = the row's regex in `c56_selftally.py::POP` applied to the new cell; the captured integers are summed and compared to the observed tally.

| row | line | old cell | new cell | claim-regex match |
|---|---|---|---|---|
| base-path-audit | 726 | `python3 -B scripts/base_path_selftest.py` over `scripts/fixtures/base-path/` (30 matrix fixtures plus 15 round-29 regression fixtures `X01`–`X15`), comparing exit, verdict and reason tuples | unchanged — identical to the old cell | yes — ['30', '15'] (sum 45) |
| source-recheck-audit | 1067 | `python3 -B scripts/source_recheck_selftest.py` (101 fixtures) | `python3 -B scripts/source_recheck_selftest.py` (106 fixtures) | yes — ['106'] (sum 106) |
| robots-expectation-audit | 1093 | `python3 -B scripts/robots_audit_selftest.py [--tool PATH]` (137 fixtures) | `python3 -B scripts/robots_audit_selftest.py [--tool PATH]` (204 fixtures) | yes — ['204'] (sum 204) |
| sitemap-file-audit | 1128 | `python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` (150 fixtures, all 34 sentences) | `python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` (235 fixtures, all 34 sentences) | yes — ['235'] (sum 235) |
| redirect-expectation-audit | 1198 | `python3 -B scripts/redirect_audit.py --selftest` (23/23; receipt `.ufo/waves/round-47/verification/selftest-redirect-audit.txt` names tool path + sha256 + tally) | unchanged — identical to the old cell | yes — ['23'] (sum 23) |
| commit-citation-lint | 1199 | `python3 -B scripts/citation_lint.py --selftest` (8/8; receipt `.ufo/waves/round-47/verification/selftest-citation-lint.txt` names tool path + sha256 + tally) | `python3 -B scripts/citation_lint.py --selftest` (9/9; receipt `.ufo/waves/round-47/verification/selftest-citation-lint.txt` names the round-47 tool sha256 `3c78a0a8…` and its then-tally 8/8; the current selftest prints 9/9) | yes — ['9'] (sum 9) |
| wave-evidence-ledger | 1215 | `python3 -B .ufo/waves/round-52/c52_wave_ledger.py --selftest` (19 fixtures, sandbox repos; receipt `.ufo/waves/round-52/control/c1-ledger-selftest.txt`) | unchanged — identical to the old cell | yes — ['19'] (sum 19) |
| quote-truth-counter | 1216 | `python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` (18 fixtures, sandbox repos; receipt `.ufo/waves/round-52/control/c2-quote-selftest.txt`) | `KAKE_R52_SELFTEST_REV=1ae8de5d4dee python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` (18 fixtures, sandbox repos; the leading pin fixes the fixture revision — without it the fixtures rebuild from `HEAD` and the pass case fails; receipt `.ufo/waves/round-52/control/c2-quote-selftest.txt`) | yes — ['18'] (sum 18) |
| readme-index-counter | 1233 | `python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest` (35 fixtures, generated sandbox repos; receipt `.ufo/waves/round-55/controls/c1-selftest-v2.txt`) | `python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest` (44 fixtures, generated sandbox repos; receipt `.ufo/waves/round-55/controls/c1-selftest-v2.txt`) | yes — ['44'] (sum 44) |
| yahoo-robots-quote-truth-counter | 1234 | `python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` (47 sandbox-repo fixtures built from the committed round-55 evidence at `HEAD` or `KAKE_R55_SELFTEST_REV`, plus 3 unit-rule checks; receipt `.ufo/waves/round-55/controls/c2-selftest.txt`) | `KAKE_R55_SELFTEST_REV=64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` (54 sandbox-repo fixtures built from the committed round-55 evidence at the pinned revision, plus 3 unit-rule checks; receipt `.ufo/waves/round-55/controls/c2-selftest.txt`) | yes — ['54'] (sum 54) |

Three rows (`base-path-audit`, `redirect-expectation-audit`, `wave-evidence-ledger`) already agreed with the observed tally and are left untouched. The other seven move only the tally token: 101→106, 137→204, 150→235, 8/8→9/9, 35→44, 47→54; the two `VAR=value` pins are added to the `quote-truth-counter` and `yahoo-robots-quote-truth-counter` commands.

## VERIFIED RUNS:

Scratch clone: `D=$(mktemp -d)`; `git clone -q --no-checkout <lane> $D`; `git -C $D checkout -q 2d308e808bfd`; `git -C $D rev-parse --show-toplevel` == `$D`; HEAD `2d308e808bfdabced268294ff823fb6acce9e02e`.

At `2d308e808bfd` (contract commit):
- `python3 -B .ufo/waves/round-56/c56_selftally.py --selftest` → `c56 selftally selftest: 20/20`, exit 0 (0.7 s). This is the number in the new row's Self-test cell.
- `python3 -B .ufo/waves/round-56/c56_quote_truth.py --selftest` → `c56 quote-truth selftest: not yet supplied (version 1 ships without fixtures; wave 1 adds them)`, exit 2. Stub confirmed by running it, not inferred from the contract.

Extra commit on top: `git -C $D -c user.name=selftest -c user.email=selftest@local commit -q --allow-empty -m 'extra on top'` → `233c772ee511e25bb89ce0779156ed7b0b4119f3`.

At `233c772` (extra commit, so `HEAD` is not the fixture revision):
- `python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` **without** the pin → `17/18`, exit 1 (`FAIL pass: … C5_quote_truth: S374 … not a raw substring of the retained body`, `C8_mirror_bytes: registry rows 156 != mirror rows 145 + 3`).
- `KAKE_R52_SELFTEST_REV=1ae8de5d4dee python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` → `18/18 (fixture revision 1ae8de5d4dee)`, exit 0. The pin is load-bearing and is written into the cell.
- `python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` without the pin → `54/54`, exit 0; with `KAKE_R55_SELFTEST_REV=64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6` → `54/54 (fixture revision 64c0ce12ffe3)`, exit 0.

The eight other documented commands at `233c772`, each run exactly as its row spells it, all exit 0 with A == B: `scripts/base_path_selftest.py` 45/45 (`45/45 fixtures passed` on stderr), `scripts/source_recheck_selftest.py` 106/106, `scripts/robots_audit_selftest.py` 204/204, `scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` 235/235, `scripts/redirect_audit.py --selftest` 23/23, `scripts/citation_lint.py --selftest` 9/9, `.ufo/waves/round-52/c52_wave_ledger.py --selftest` 19/19, `.ufo/waves/round-55/c55_readme_index.py --selftest` 44/44.

End-to-end: the seven cell edits plus the appended section were written into the clone's `SKILL.md` and committed (`f81df6420c289187f7133d0b5ee60c571697f68e`); `python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision f81df6420c289187f7133d0b5ee60c571697f68e` → `C1 selftest-tally tally_mismatches=0 rows_checked=10 met=True`, `EXIT=0` (54 s), every row `claim == observed` (45, 106, 204, 235, 23, 9, 19, 18, 44, 54). Diff scope `git diff --unified=0 2d308e808bfd f81df64 -- SKILL.md`: 7 one-line hunks (1067, 1093, 1128, 1199, 1216, 1233, 1234) + 19 appended lines, nothing else.

Pinned-script blobs: `git diff --stat e48354b7 HEAD` over the ten pinned scripts is empty, so the counter's `tool_changed` check holds for every row at the contract revision.

## RISKS:

- **The C2 counter is moving under this draft.** The lane working tree carries an uncommitted `M .ufo/waves/round-56/c56_quote_truth.py` (+317 lines; docstring line 4 reads: version 1.1 replaces the `--selftest` stub with the ported selftest). The row's Self-test cell is true at the frozen contract commit only; when v1.1 lands, that cell must be restated with its printed N/N and its receipt path. I inspected only the docstring and the diff size of the uncommitted body; I did not run it.
- No counter pins the C2 row's Self-test text: `c56_quote_truth` is outside `POP`, so C1 would not catch a stale stub sentence.
- `c55_quote_truth.py --selftest` passes 54/54 with **and** without `KAKE_R55_SELFTEST_REV` at `233c772`; the pin anchors the fixture revision but is not a repair at this revision. Only `c52_quote_truth.py` needs its pin to pass (17/18 → 18/18). The cell states the pin without claiming it changes the count.
- The round-47 receipt `.ufo/waves/round-47/verification/selftest-citation-lint.txt` records `selftest: 8/8 passed` for tool sha256 `3c78a0a8…`; `scripts/citation_lint.py` is now `0beba647…` (changed in `af7b217`, round 48) and prints 9/9. The new cell keeps the receipt pointer and states both numbers; a fresh receipt is outside this seat's write scope.
- `c56_selftally.py::table_rows` splits on every `|`, so `redirect-expectation-audit` reads as 9 cells (escaped `\|` in its Pinned-values cell). Harmless for the Self-test cell (index 4) and the row is unchanged, but the eight-cell schema is not enforced by this counter for that row.
- The 44/44 and 54/54 receipts already matched the observed tallies; only the registry integers were stale. Nothing under `corpus/` or any tool was touched, and no tool install was needed (no pacman/uv/npx run).
- All measurement happened in a `mktemp -d` clone; lane jj/git state and the Git index are untouched, and this report is the only lane path written.

VERDICT: Drafted and end-to-end verified — the C1 counter reads `met=True, tally_mismatches=0, rows_checked=10` on the drafted SKILL.md (7 cell edits, 2 new eight-cell rows, 20/20 tally, C2 selftest confirmed exit 2 at the contract commit).
