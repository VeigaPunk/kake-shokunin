# ReviewC1 — round 83 wave w1

Attack surface: the frozen C1 counter `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-83/c83_defect_queue.py`
(sha256 `9fdfe84fc80c2218754ef486c4a9b5ee7f8621da7c9bc1ade9f13d8e1e3a985a`) and the six item
conditions in `.../round-83/contract.md` (sha256 `652eec765bf41df45f1b02beb7bba9ecde8231a55fbfce81e91613835a83052a`).
I wrote no production file, edited no frozen file, and wrote nothing in the fleet repo or a sibling.
Receipts: `.ufo/waves/round-83/w1/ReviewC1/` — `runs/` holds 32 counter invocations plus 3 notes,
`attack.py` is the fixture driver, `frozen-sha256.txt`, `all-cheapest-inventory.txt`, `fleet-diff.txt`.
Scratch root `/fast/scratch/hyaku/kake-r83/ReviewC1` was deleted after the receipts were copied.

Method: every probe is a tree assembled from scratch and measured with
`python3 -B /home/vgpnk/…/c83_defect_queue.py --root <tree> --fleet <fleet>` (worktree mode) or
`--root <repo> --revision <sha> --work <abs>` (after-state mode). Synthetic fleets are real git
repos under the scratch root, created with `git -C <dir> init -q`, toplevel asserted equal to the
fixture dir before the first commit, commits made with a throwaway `-c user.name/user.email`
identity. No network, no installs.

## Controls reproduced first (harness trust)

- Base after-state: counter over `--revision 826b0061f233ce1dffb9bd6874abc1342a864247` → exit 1,
  six `open` lines and `C1v1 … open=6 closed=0 met=false`; `diff` against the counter section of
  `controls/base-c83-defect-queue.txt` is identical. Receipt `runs/../base-run.txt`.
- Junk control: `junk_tree_build.py --root <scratch>/junk` → exit 0 (6 prose claims, no state);
  counter over it → exit 1, `open=6`; six lines identical to `controls/ctl-c83-junk-queue.txt`
  (`diff` clean). Receipt `runs/junk-control-repro.txt`.
- `--selftest` with `TMPDIR` under scratch → exit 0, `selftest: 9/9 passed`; identical to
  `controls/c83-selftest-c1.txt`. Receipt `selftest-run.txt`.

So the counter behaves as its controls claim; the findings below are about what the conjuncts
measure, not about a broken control.

## 1. Cheapest tree per item (no work done)

Each tree was built in scratch, run, and left `open=5` with exactly the named item closed —
the six do not interfere, so the union is a single tree of 7 files / 2,604 bytes.

| Item | Cheapest artifact that satisfies the condition | Run | open | Item closed |
|---|---|---|---|---|
| D1 | `w1-spec.json` 8 items (reviewer, critic, 6 executor); `w1-results.json` 8 rows each `output:"x"` (1 byte); `w1-accounting.json` echoing `settled=8`, `settled_attack=2`, `settled_share=0.25`, eight `output_bytes:1` seats; one lesson line with `0/7` and `settled_attack=` | `d1-only` | 5 | D1 (`settled=8 settled_attack=2 settled_share=0.25`) |
| D2 | spec 1 item; results `{"results": []}`; accounting `bytes_basis:"utf-8"`, `settled:0`, `[]`, `0`, `0.0`, `seats:[]`; one lesson line | `d2-only` | 5 | D2 (`mismatched=[]`) |
| D3 | one fabricated line `C2v1 revision=<40 lowercase hex> population=30 bound=30 mismatches=0 met=true` at the receipt path; one lesson line | `d3-only` | 5 | D3 |
| D4 | one lesson quoting 4 of the 5 lines `git diff cb02b705 7678247a` removed, plus `7678247a` and `erratum` on the D4 line — copy-paste only, no analysis of the four lines | `d4-only` | 5 | D4 (`quoted=4`) |
| D5 | a 6-line runner printing five `killed` rows and `distinguished=5/5`, exit 0; no fixture, no fixture path, nothing read; one lesson line | `d5-only` | 5 | D5 (`rc=0 rows=yes`) |
| D6 | one appended `corpus/QUALITY.md` line containing `corpus/lessons/round-82.md`, `Gate`, `round-83`; one lesson line | `d6-only` | 5 | D6 (`criterion=yes`) |
| all six | union of the above: 7 files, 2,604 bytes, **no seat report, no `w1/` directory** | `all-cheapest` | **0** | all six, `met=true`, exit 0 |

After-state mode confirms it: a git repo with the same 7 files (commit `a62c36ce…`), measured with
`--revision a62c36ce… --work /fast/…/work-rev-abs` → `open=0 closed=6 met=true`, exit 0
(`runs/all-cheapest-revision-abs.txt`). The union tree's D4 quotes are copied from the real fleet
diff; everything else in the tree is fabricated bytes.

## 2. The three requested falsifications

**(a) Accounting right, results rows empty — D2 reads closed.** Three variants, all `D2 closed
mismatched=[] log=yes`: `results:[]` with accounting 0/[]/0/0.0 (`a-empty-results`); eight rows all
`output:""` with accounting 0/[]/0/0.0 and eight `output_bytes:0` seats
(`a-rows-empty-right-zero`); eight empty rows with accounting claiming `settled:8` over zero-byte
seats (`a-rows-empty-echo`, D1 catches the settled mismatch but D2 still closes). Cause:
`item_d2` line 177 filters `row["output_bytes"] > 0` over the derived seats; with zero settled
seats `mismatched` is empty and the item passes. D2 never reads `settled`/`settled_names`, so a
tree that delivered nothing has "correct" byte accounting.

**(b) Killer prints `distinguished=5/5` without running anything — D5 reads closed.**
`b-killer-print-only` (five bare `print('C1-m3 killed')` … plus `print('distinguished=5/5')`, exit 0)
→ `D5 closed rc=0 tail='distinguished=5/5' rows=yes`. `b-killer-equivalent-no-guard` (five
`equivalent` rows, no guarding source line printed) also closes D5; line 233 only requires the name
and the word `killed`/`equivalent` anywhere on a line, so the contract's "killed on its named
fixture or `equivalent` with the guarding source line printed" is not enforced, and no fixture
existence is checked.

**(c) Erratum quoting four lines from a different report — D4 stays open.** `c-erratum-other-report`
quotes four long lines from `/home/vgpnk/Projects/shokunin/.ufo/reports/round-82/kake.md` under a D4
line carrying `7678247a` → `D4 open removed=5 quoted=0 log=yes`. The quote test compares against
the fleet diff's `-` lines, so a wrong-report quote contributes nothing; the probe also confirms a
lesson token alone does not close D4.

## 3. D4 derivation: amendment or later commit?

Code (lines 209–219) takes `commits[0]` (newest commit touching `.ufo/reports/round-81/kake.md`)
as `after`, `commits[1]` as `before`, diffs them, counts `-` lines longer than 41 raw characters,
and requires the D4 lesson line to contain `after[:8]` and `erratum`. It never names `7678247a`.

- **Real fleet today**: `git -C /home/vgpnk/Projects/shokunin log --format=%H -- .ufo/reports/round-81/kake.md`
  returns exactly `7678247a3c13b1dc03ed1cb8f80d2dba603ee0ca` then
  `cb02b70551f14ac3dea7eadebac22cb2cdc45c10`. So `after` **is** the amendment — by position, not
  by pin. `d4-only` reads `removed=5 quoted=4 amendment=7678247a`.
- **Any commit pair satisfies it**: a synthetic two-commit fleet whose amendment is `c371ad52…`
  reads `D4 closed removed=5 quoted=4 amendment=c371ad52 log=yes` (`fleet-two`). The frozen hash
  is not required by the code.
- **A later append-only touch re-opens a compliant tree**: `fleet-later-append` (filed → amended →
  append-only later touch) reads `removed=0 quoted=0 amendment=742eb9c4`. With the contract's
  `7678247a` token the row reads `log=no` (the counter demands `after[:8]`), and with the later
  token `log=yes` but still `quoted=0`. A contract-compliant erratum cannot close D4 once any
  later commit touches the report.
- **A later commit can retarget the content**: `fleet-later-remove` (filed → amended → an unrelated
  later rewrite that removes four other long lines) reads `D4 closed removed=4 quoted=4
  amendment=ab2fd357 log=yes`. The four quoted lines were removed by the later commit, not by
  `7678247a`; the state conjunct is satisfiable by content the frozen amendment never removed.
  Contract requires `7678247a`; the counter requires whichever commit is newest — the two diverge
  in both directions.
- **No history**: report absent or untouched → `D4 open fleet history for .ufo/reports/round-81/kake.md has 0 commit(s)`;
  one commit → `has 1 commit(s)`; a non-git directory at the same path → `has 0 commit(s)` (git
  failure is reported as a count). All exit 1; there is no crash/unevaluable path. `--fleet`
  defaults to the hard-coded `/home/vgpnk/Projects/shokunin`, so off-host the item is unevaluable
  unless `--fleet` is passed.

Also unenforced: the contract says "each quoted line absent from the amended blob"; line 217 only
tests `line in lesson`. `fleet-moved` swaps two four-line blocks in one commit — git reports the
four moved lines as `-` lines that are re-added in the same commit — and the counter reads
`D4 closed removed=4 quoted=4 amendment=8331c2b5`, while `git show HEAD:<report>` still contains
all four quoted lines (my absence check printed `[]`). The real amendment is a true replacement
(0 of its 5 removed lines is present in `7678247a:…/kake.md`), so today's verdict is unaffected,
but the clause is not implemented.

## 4. D1 arithmetic: what the frozen rule measures

As implemented (lines 130–136, 155):

- **settled** = a results row whose `output` is a `str` with `len(output.encode("utf-8")) > 0`.
  Any non-empty byte counts: `"x"` (1 byte), `" "` (1 byte). Empty string does not.
- **share** = `round(len(settled_attack) / len(settled), 4)` — over **settled rows only**, never
  over requested seats. Attack roles are exactly `{reviewer, critic, mutation-tester, labrat}`;
  a row whose name is absent from the spec has role `""` and counts as non-attack, diluting.
- **gate** = `settled_attack >= 2 and settled_share >= 0.25`, plus a record echo of `settled`,
  sorted `settled_names`, `settled_attack`, `settled_share`.

Evidence: `d1-share-025` — eight 1-byte `x` outputs, two attack roles → `settled=8
settled_attack=2 settled_share=0.25`, D1 closed. `d1-share-below` — one attack of four → share
0.25 but `settled_attack=1`, open; the absolute floor of two is the binding constraint.
`d1-dead-seats-free` — 12 requested seats, four attack seats dead with empty output, 8 settled
with 2 attack → D1 closed at 0.25; dead attack seats cost the share nothing because the
denominator excludes them.

So yes: the share is computed over settled rows only, and a 1-byte output counts as a settled
seat. The frozen rule measures "at least two attack-role rows emitted at least one byte, and those
rows are at least 25 % of all rows that emitted at least one byte" — not substantive work, not
report size, not requested shape.

## Findings (severity order)

**F1 — High — C1 can read `met=true` on a records-only tree with zero seat reports.** The 7-file,
2,604-byte union (`all-cheapest`) closes all six items in worktree mode and in after-state mode
(`--revision`, absolute `--work`): `open=0 closed=6 met=true`, exit 0. Every state conjunct is a
self-attested artifact in the same tree: D1/D2 arithmetic over a hand-written spec/results/
accounting triple; D3 a text receipt never produced by the instrument; D4 four lines copied from
the fleet diff; D5 a print-only script; D6 one appended QUALITY line. This confirms and completes
the limit the round-82 spot-check recorded ("a records-only tree with correct arithmetic could
reach `open=0`"): the counter establishes artifact shape and internal arithmetic, not that any
round-83 work happened. `met=true` must therefore never be reported as evidence of work on its
own; it must be paired with the seat reports, which the counter does not read.

**F2 — Medium-High — D4 is positional, not pinned; a later commit re-opens or retargets it.**
See §3. A compliant tree is re-opened by an append-only later touch (`removed=0`), and an
unrelated later commit that removes four long lines closes D4 with its own hash. The frozen
`7678247a` identity is enforced nowhere. Since the fleet report history is shared, a fleet-side
commit can change C1's verdict after the lane commit; today the two-commit history happens to land
on the amendment.

**F3 — Medium — D4's "absent from the amended blob" clause is not implemented.** `fleet-moved`
closes D4 on four quoted lines that remain in the amended blob. Not exploited by the current fleet
history (verified 0 of 5 removed lines present in the amended blob), but a block-move commit is
ordinary git history and would pass.

**F4 — Medium — D3 accepts any text with five tokens, and the first line wins.** `d3-only` closes
on one fabricated line. `d3-revision-short` closes with `revision=abc` and a 40-hex token elsewhere
on the line, contrary to the contract's `revision=<40 hex>`. `d3-first-red` (red `mismatches=2`
first, green rerun second) reads open with the red line's fields — a receipt that transcripts a
failed then passing run is false-open. `HEX40` is lowercase-only, so an uppercase revision reads
`no C2v1 revision line` (`d3-upper-hex`). No check ties `population` to the instrument's derivation
or the file to `scripts/instrument_receipts.py`; the counter only reads the file.

**F5 — Medium — D5 is a print check.** `b-killer-print-only` and
`b-killer-equivalent-no-guard` close D5 with no fixture executed, and a single `print('<name> killed')`
per row suffices. The runner's stderr is captured and discarded (`stderr=PIPE`, never read), and
`subprocess.run` has no timeout, so a hanging runner hangs the counter.

**F6 — Medium — relative `--work` + `--revision` silently false-opens D5.** `main()` resolves
`--root` and `--fleet` but not `--work` (line 471); `export()` returns `work/"export"` (line 76);
D5 runs the runner with `cwd=tree.root` and the root-relative runner path (line 228). With
`--work work-rev` the path doubles under the new cwd → Python `rc=2`, empty stdout, `D5 open
rc=2 tail='' rows=no` (receipt `all-cheapest-revision.txt`); the same tree with an absolute
`--work` reads `D5 closed` and `met=true` (`all-cheapest-revision-abs.txt`). A valid after-state
can therefore never close C1 when the caller uses a relative work dir, and the dropped stderr
hides why. This is a false-negative, not a false-positive, but it converts an instrumentation
fault into a measured defect with no diagnostic.

**F7 — Medium — D2 is vacuous when nothing settled.** See §2(a). `mismatched` only inspects
derived rows with `output_bytes > 0`; zero settled seats pass, and the item never reads
`settled`/`settled_names`. D1's floor prevents the pair from closing on nothing, but D2 alone is
not evidence that any byte count was taken.

**F8 — Low — D4 off-by-one against the contract.** Contract: removed lines "≥ 40 chars"; code:
`len(line) > 41` on the `-`-prefixed raw line (line 216), i.e. content ≥ 41. `fleet-len40` removes
four exactly-40-char lines plus one longer line and quotes all five; the counter reads
`removed=1 quoted=1` and D4 stays open. Four contract-qualifying lines are silently excluded from
the candidate set.

**F9 — Low — D1's `0/7` row token is an unanchored substring.** `d1-row-token-loose` closes D1
with a lesson line reading `10/70` (`log=yes`): `line_with` anchors the tag (`\bD1\b`) but not the
number.

**F10 — Low — `record=ok` in the D1 detail means "accounting.json exists", not "record matched".**
`a-rows-empty-echo` prints `settled=0 … record=ok` while the record claims `settled:8`, because the
detail is `'ok' if record else 'no'` over the parsed dict. A receipt reader can over-read the token.

## Residual risk

- The frozen predicate `met <=> open == 0` is satisfied by F1, so C1's `met=true` is an
  artifact-shape claim. The round's calibration row should say that, or cite the seat reports and
  real receipts alongside the counter output.
- D4 depends on mutable fleet history (F2). If anyone commits to
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-81/kake.md` after the lane commit, the
  reported C1 receipt may no longer reproduce; the report should cite the fleet commit pair it
  used (`7678247a`, `cb02b705`) and note the positional dependency.
- D5 has no timeout and discards stderr; a crashing or hanging runner is not distinguished from a
  measured red.
- D3's hex regex is lowercase-only, and the receipt is not bound to the instrument that produced it.

## Verification gaps

- The real lane after-state did not exist while I reviewed (`w1-results.json`, `w1-accounting.json`
  absent; wave running). My verdict is about the counter predicate, not about whether the eventual
  round-83 artifacts are honest.
- No `lsp` device is mounted in this session, so all code reading was text-based; I record that
  unavailability rather than presenting grep output as semantic proof. Citations are to the frozen
  file at the sha256 above.
- I did not run a hanging-runner test (it would hang the counter) or a Windows/macOS path test.
  The `--root` with `--revision` on a non-git tree path (`fault (tree)`, exit 2) was read in code,
  not exercised.

## Verdict

**C1: admissible only as a shape/arithmetic claim, with limits disclosed — recommendation, not an
admission.** The counter is reproducible (base `open=6`, junk `open=6`, selftest 9/9, all matching
the committed controls) and its selftest is green, so the property is passable. But the cheapest
satisfying tree is 7 fabricated files / 2,604 bytes with no seat report (`open=0 met=true`, exit 0,
worktree and `--revision`), D4 is not pinned to `7678247a` and is retargetable by a later commit,
D3 and D5 are token/print checks, and D2 is vacuous at zero settled seats. A round-83 report that
prints `open=0 closed=6 met=true` is accurate about the counter and silent about the work; it
should pair that line with the seat reports and the real receipts, and re-derive D4 by hand against
`7678247a` (`removed=5`, 0 of them present in the amended blob) because the counter does not.
