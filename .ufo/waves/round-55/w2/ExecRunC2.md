# ExecRunC2
ATTACKS: the C2 measurement — `.ufo/waves/round-55/c55_quote_truth.py` (predicate `met: conditions_passed == 8 of 8`) run against revision `a7a548e102b71bd16b0a6ddafa469393a2c98b69`, its determinism, its base control at `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`, and an independent recount of the same claim from committed bytes only. No lane mutation; the only file written is this report.

## COMMANDS:
All commands run with cwd `/home/vgpnk/Projects/shokunin/kake-shokunin` unless stated. Tooling: `python3 --version` → `Python 3.14.8`; `git --version` → `git version 2.56.0`. No installs were needed.

1. `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision a7a548e102b71bd16b0a6ddafa469393a2c98b69` (twice) → `rc=0`, `rc2=0`; `sha256sum` of both captures `1d67f74d783905875c7f09ce338c51812268894608029a3b4374db105f11d38e`; `cmp` → `IDENTICAL`; 11 output lines: `C2 quote-truth 8/8 met=True`, eight `PASS` lines (`C1_entries_exist … C8_mirror_bytes`), `revision: a7a548e1…`, `EXIT=0`.
2. Same plus `--json` → `rc=0`; body parsed after stripping the trailing `EXIT=0` line: `schema=kake-r55-c2-quote-truth-v1`, `predicate=met: conditions_passed == 8 of 8`, `conditions_passed=8`, `met=true`, every check `state=pass, passed=true, notes=[]`; facts `C1 entries=3`, `C3 rows=156 base_rows=155`, `C6 receipts=3`, `C8 registry_rows=156`; `adopted` = S372→`yahoo-japan-robots-txt-refusal-rules.md`, S373→`yahoo-japan-robots-pattern-syntax.md`, S418→`yahoo-japan-robots-txt-basics.md`.
3. `KAKE_R55_SELFTEST_REV=a7a548e102b71bd16b0a6ddafa469393a2c98b69 python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` (run from the lane root) → `rc=0`, `c55 quote-truth selftest: 50/50 (fixture revision a7a548e102b7)`; no `FAIL` lines. Fixtures are built under `tempfile.mkdtemp(prefix="c55-qt-")` and each is `shutil.rmtree`d.
4. `python3 -B … --revision fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d` → `rc=1`, `C2 quote-truth 0/8 met=False`, `EXIT=1`; `diff -u .ufo/waves/round-55/controls/base-c2-quote-truth-v2.txt <capture>` → empty (`BASE-CONTROL-IDENTICAL`); both files `sha256 8c0899ec2ccb60321d8f8043c08a5c6e0857445764ba8bbcba7aa1fc34db61e5`.
5. Row census: `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → base `155`, build `156`. Same count scoped to the `## Registry` section (awk section gate) → `155` / `156` (identical, so no matching row lives outside `## Registry`).
6. Counter bytes pinned: `sha256sum .ufo/waves/round-55/c55_quote_truth.py` → `300fb426f9d4cfcde93b7c18d50adef66a65fe33908f039582db1f0ce8813ce5`; `git show a7a548e…:.ufo/waves/round-55/c55_quote_truth.py | sha256sum` → same digest. The measured code is the committed code.
7. Write-site audit: `grep -n "open(\|Path(\|os.listdir\|glob(" .ufo/waves/round-55/c55_quote_truth.py` → single hit, line 561 `with open(tgt, "w", …)` inside `_build` (selftest fixture only). `run_checks` reads exclusively through `git show`/`git log`/`git merge-base`.
8. Kill-rule probes: no `--revision` → `rc=2`, stderr `error: --revision is required unless --selftest is used`; `--revision deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` → `rc=1`, `0/8 met=False`; `--root /nonexistent-lane` → `rc=1`, `0/8 met=False`.
9. `find .ufo/waves/round-55 -name '__pycache__' -o -name '*.pyc'` → empty; `ls -d /tmp/c55-qt-*` → `0`.

## DETERMINISM:
- Two build-revision runs are byte-identical (`sha256 1d67f74d…`, `cmp` clean). A third run launched from `/tmp` with the same absolute `--root` produced the same bytes (`CWD-INDEPENDENT-IDENTICAL`).
- `--json` is stable across `--root <abs>` and `--root .`: both captures `sha256 0e8791331487abc65b2cbd1f058f61ee6d3df15125755b314168bcf56e08b480`.
- The selftest is stable across two runs: `sha256 55413c04c157883598aa6ceb247dae5b66d2e39e583f6e07a4b0ad238f2ae5f9` both times, `50/50` both times, zero leftover fixture directories.
- Measurement is revision-pinned, not worktree-pinned: every evidence read is `git show <rev>:<path>`. Independently, the worktree is not drifted here — `git diff --stat a7a548e… -- corpus/SOURCES.md corpus/knowledge .ufo/waves/round-55/sources .ufo/waves/round-55/assimilation` is empty, and `sha256sum corpus/SOURCES.md` = `git show a7a548e…:corpus/SOURCES.md | sha256sum` = `cc402e4b559528170fe71ba09b6ad3be663a8f9d5ce9f36caeaed5ea45e6c50e`.
- The counter is silent on `stdout`/`stderr` apart from its report and the trailing `EXIT=` line; no timestamps or paths derived from `time`, cwd or environment enter the output (the only env input is `KAKE_R55_SELFTEST_REV`, selftest only).

## INDEPENDENT RECOUNT:
Recount done without importing or calling the counter: committed bytes read via `git show`, parsed with `re`/`split("|")`.

| item | counter says | my recount | agree |
|---|---|---|---|
| registry rows, build vs base | C3 `rows=156`, `base_rows=155` | grep 156 / 155 (whole file and `## Registry`-scoped); id set diff = added `['S418']`, removed `[]` | yes |
| S372 row | C3 row shape ok, C4 used-by extended | 11 cells at both revs; cells 0–9 identical; only cell[10] differs, base `…rel-nofollow-semantics.md` → build `…rel-nofollow-semantics.md, …robots-txt-refusal-rules.md` | yes |
| S373 row | same | 11 cells both revs; cells 0–9 identical; only cell[10] differs, base `…rel-nofollow-semantics.md, …baidu-friendly-crawl-guidance.md` → build adds `…robots-pattern-syntax.md` | yes |
| S418 new row | C3 new-row branch passes; C4 used-by = own entry | absent at base (token `S418` count 0); present exactly once at build; 11 cells, 12 `|`, no `\|`; cells: `S418`, `Yahoo!検索 インフォセンター — robots.txtとは？ — https://info-search.yahoo.co.jp/archives/002885.php`, `docs`, `A`, descriptive, location, summary, `mined`, `2026-10-25`, `180d`, `corpus/knowledge/yahoo-japan-robots-txt-basics.md` | yes |
| duplicate source URLs | C7 requires no E04 in the census stdout | each URL occurs in exactly one registry row: 002849→S372, 002850→S373, 002885→S418 (1 row-hit and 1 total line-hit each) | yes |
| three entries + header trio | C1 pass, C2 pass | all three absent at base, present at build (9630 / 7471 / 5292 bytes); first 8 lines carry filled `source:`, `verified-at: 2026-10-25`, `recheck: 180d — …`; each `source:` line names its own sid; sid also cited below the header (13 / 11 / 11 lines) | yes |
| base control | `controls/base-c2-quote-truth-v2.txt` = do-nothing 0/8 exit 1 | byte-equal, `rc=1` | yes |

Selftest scope confirmed from source: 46 `@case(...)` decorators + the inline `pass` case = 47 fixture cases, plus 3 unit-rule assertions = 50 checks, matching the observed `50/50`. `pass` case expects 0; 42 `@case` failures expect 1; `fail_bad_receipts` expects 2.

## DISAGREEMENTS:
- **None between the recount and the counter.** `conditions_passed=8`, `met=True`, exit 0 reproduce from independent byte-level recomputation; no check passes on evidence I could not re-derive.
- Non-predicate defects found by the probes above (they do not flip the predicate; recorded because they affect how a future C2 reading would be interpreted):
  1. **Usage exit code violates the frozen kill rule.** Contract: "exit 0 iff met; 1 not met; 2 unevaluable; 64 usage." Observed with no `--revision`: `rc=2` (argparse's own error exit), so a usage error is indistinguishable from `unevaluable` by exit code alone.
  2. **An unreadable revision or root reports `not met`, not `unevaluable`.** `--revision deadbeef…` and `--root /nonexistent-lane` both exit 1 with `0/8 met=False` — a broken measurement prints the same verdict as a genuinely failing claim. Only the in-exception path and a non-JSON `receipts.json` reach exit 2.
  3. **`--json` is not a pure JSON stream.** The object is followed by a bare `EXIT=0` line; `json.load` fails with `Extra data: line 72 column 1`. Any consumer must strip the last line before parsing. (No contract text mandates pure JSON, so this is a consumer hazard, not a contract breach.)
  4. **Contract fixture count is understated.** Contract says "Junk controls (selftest, 30 fixtures)"; the counter carries 47 cases (+3 unit checks). Higher than declared, so the control surface is not weaker than frozen; [INFERENCE] the contract line is stale wording from version 1.
  5. **S418 `recheck:` line records a command but no observed result.** S372/S373 end `-> 1`; S418 ends at the `grep -F -c '…'` command with no count. `C2_entry_provenance` only requires a filled `recheck:` line, so the counter passes; the evidence is weaker than its siblings'. Not a predicate disagreement — an evidence-strength observation for the reviewer.

VERDICT: C2 measurement reproduces exactly (8/8, met=True, exit 0, byte-identical twice, base control byte-equal, selftest 50/50) and my counter-free recount of rows, cell diffs, S418 shape, URL uniqueness and the entry header trio agrees with every check fact; residual defects are exit-code/JSON-shape/contract-wording issues that do not move the predicate.
