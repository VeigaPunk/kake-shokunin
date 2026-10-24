# Wave-2 ReviewCriteriaChecks — criteria checks and receipts falsified

Attacks the three round-35 criteria checks (`.ufo/waves/round-35/criteria/{registry_row_check,control_description_check,prebuild_leak_check}.py`) and their receipts (`.ufo/waves/round-35/verification/criterion-*.txt`): reproduction at `7deacc4`, then false-pass attempts with an irrelevant quoted line, a task-table-only row, and a receipt holding values in an array. All three checks accept bad input they should reject (4 confirmed false passes); reproduction itself is 6/6 exact.

## 1. Reproduction of the six receipts

Sandbox clone `/fast/scratch/hyaku/kake-r35/w2/ReviewCriteriaChecks/clone`, `git checkout 7deacc4629c1d05a34fb919d8095e99efc7b712f` (rev-parse verified; GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset; TMPDIR=/fast/scratch/hyaku/kake-r35/w2/ReviewCriteriaChecks/tmp). Bundle used from the clone's own copy, sha256 `6486b9abc3cb32c5403bc4ddeb7331bc8e6aace6dd775c04fd3733ab1cab2b7e`, byte-identical to the lane copy. The criteria scripts are byte-identical at `7deacc4` and the current lane tip `0d52173` (blob shas `c57c76ca…`, `b2f5b648…`, `37bc51b1…`), so all runs below used exactly the landed scripts.

| Receipt | Command (from clone root) | Receipt says | Rerun observed | Match |
|---|---|---|---|---|
| criterion-registry-row-at-fd0d53b2.txt | `python3 -B .ufo/waves/round-35/criteria/registry_row_check.py --repo . --rev fd0d53b2` | revision line, 7 scripts, `missing tools: none`, exit=0 | identical, exit=0 | yes |
| criterion-registry-row-at-318561ef.txt | same, `--rev 318561ef` | missing `scripts/link_preview_audit.py`, exit=1 | identical, exit=1 | yes |
| criterion-control-description-r35-correction.txt | reconstructed, see §4 | PASS quotes line 15 (45 chars), exit=0 | identical, exit=0 | yes |
| criterion-control-description-r34-row4.txt | `… control_description_check.py --repo . --bundle .ufo/waves/round-34/retained/r34-c1-lookup-dcef39b5.bundle --revision dcef39b5 --path scripts/link_preview_audit.py --doc corpus/lessons/round-34.md --doc-rev fd0d53b2 --anchor dcef39b5` | FAIL no whole ≥20-char line + line number, exit=1 | identical, exit=1 | yes |
| criterion-prebuild-leak-r34-c1-at-a2fe31b.txt | `… prebuild_leak_check.py --repo . --receipt-rev a2fe31b --receipt .ufo/waves/round-34/verification/c1-at-d08d8de.json --entry-rev ce72dd1b --entry corpus/knowledge/link-preview-metadata.md --line-regex '^ds4cc-7fc6aa2f-og-census:'` | 7 matched values, PASS, exit=0 | identical, exit=0 | yes |
| criterion-prebuild-leak-r34-c2-at-a2fe31b.txt | same with `c2-at-d08d8de.json` | 7 matched values, FAIL published, exit=1 | identical, exit=1 | yes |

Reproduction is clean: the receipts are honest at `7deacc4`. `dcef39b5` exists only inside the bundle (not lane history); the control check's private bundle fetch resolves it in a TMPDIR clone — that part works as designed.

## 2. Confirmed false passes (attack commit `2bac6f931c77aa97ebf6c9dc13bfdf412ad03501` = `318561ef` + 12 added lines; sandbox clone, branch `attack`)

**A. registry_row_check passes on a row that only exists in a task table — exit 0.** Appended to SKILL.md (nothing else changed, `git diff --stat 318561ef 2bac6f9`: SKILL.md +6): a section `## Wave-2 task table (work items, not a gate registry)` with header `| Name | Entry command | Owner |` and one row `| audit-new-pages | python3 scripts/link_preview_audit.py --manifest /abs/manifest.json | wave-2 executor |`. Run `registry_row_check.py --repo . --rev 2bac6f9` → `scripts scanned: 7 / missing tools: none`, exit=0. Root cause: `row_covers_tool` (`.ufo/waves/round-35/criteria/registry_row_check.py:148-170`) scans *every* markdown table in SKILL.md whose header row has cells `name` and `entry command`, anywhere in the file, and never anchors to the gate-registry section; a row whose command cell merely mentions the script path counts as registry coverage. At the unchanged `318561ef` the same run exits 1 (row 2 of the table above), so the table alone flips the verdict.

**A2. registry_row_check ignores a tool that visibly has an exit contract — exit 0.** Commit `ee2b219e2d6339cbca2ac3a02345f02dddef1cb9` adds `scripts/ghost_audit.py` (5 lines, `sys.exit(2)` on bad usage, `sys.exit(0)` on success, no docstring, no `EXIT_`-prefixed names). Run at that rev → `scripts scanned: 8 / missing tools: none`, exit=0. Root cause: `has_exit_contract` (`registry_row_check.py:88-107`) detects a contract only via an `EXIT_*` assignment or the docstring regex `EXIT_DOC_RE`; a tool that keeps both silent needs no registry row at all. The check audits declaration strings, not behavior.

**B. control_description_check passes on an irrelevant 20+ character quoted line inside a factually wrong description — exit 0.** `attack-b.md` (committed in `2bac6f9`) contains one paragraph: `Correction of `dcef39b5`: the retained control recomputes its verdict live from the page DOM on every run, and line 1 of its source is `import hashlib, json, os, sys`, which confirms the tool performs a general metadata audit of arbitrary pages.` Run `control_description_check.py --repo . --bundle .ufo/waves/round-34/retained/r34-c1-lookup-dcef39b5.bundle --revision dcef39b5 --path scripts/link_preview_audit.py --doc attack-b.md --doc-rev 2bac6f9 --anchor 'Correction of `dcef39b5`'` → `PASS: paragraph for anchor 'Correction of `dcef39b5`' quotes source line 1 verbatim (29 characters).`, exit=0. The quoted line is pure boilerplate and the sentence around it asserts the opposite of what the `dcef39b5` tool does (it is a sha256 lookup table: `T.get(key(...))` at lines 14-15 of the bundled source), yet the check passes it. Root cause: `_names_line_number` (`control_description_check.py:143-151`) plus `_quoted_source_line` (`:153-168`) require only that the block names *some* line number N and backticks source line N verbatim with length ≥ 20; relevance and truth are unchecked, so any import/shebang line satisfies the criterion.

**C2. prebuild_leak_check passes on a receipt holding 6 of 7 census values in an array — exit 0.** `attack-c2-partial-array.json` (in `2bac6f9`): `{"note": "six of seven census values published before the build; pages total withheld", "census": ["87", "87", "1", "87", "1", "87"]}`. Run with `--receipt-rev 2bac6f9 --receipt attack-c2-partial-array.json` (entry args as in the receipts) → `PASS: not every matched value appears as a value in the receipt JSON; absent: pages=102`, exit=0. A pre-build receipt that publishes og:title, og:type, og:image, og:url, all-four and og-url-equals-canonical is blessed as leak-free. Root cause: the PASS predicate is "not *every* matched value appears" (`prebuild_leak_check.py:83-95`); only total disclosure fails.

**C3. prebuild_leak_check passes on a receipt publishing every value as a JSON key — exit 0.** `attack-c3-values-as-keys.json`: `{"note": …, "102": "pages total", "87": "published count …", "1": "og:image floor and all-four"}` → PASS, all seven values listed absent, exit=0. Root cause: `scalar_strings` (`prebuild_leak_check.py:37-45`) walks dict *values* only; keys are invisible, so a receipt can publish the full census as key names and pass.

**C1 (negative result, confirmed strength).** `attack-c1-full-array.json` with all seven values in one plain array → `FAIL: every matched value appears as a value in the receipt JSON (pre-build target published)`, exit=1. Values stored in arrays are scanned (`scalar_strings` recurses lists), so the assigned "values in an array" input is *detected*, not passed; the false passes are the partial-array (C2) and keys (C3) variants.

## 3. Severity (advisory)

- **High — A/A2:** the registry-row criterion proves a row exists in *a* two-column table, not in the gate registry, and only for tools that advertise their contract; both the table-locality and the silent-tool holes are reachable by accident (task tables are common in SKILL.md-style docs) and by a tool author who simply never writes `EXIT_`/docstring text. The `fd0d53b2` PASS receipt is genuine but the check would also have passed without the real registry (demonstrated at `2bac6f9`).
- **High — C2:** "not every value" is the wrong predicate for a leak criterion; 6/7 pre-published values pass. Suggested shape: fail when *any* `key=value` from the sealed target appears in the receipt, or at least require a declared margin.
- **Medium — C3:** JSON keys as a value channel evade `scalar_strings`; walk keys too, or hash-scan the raw receipt bytes for each value.
- **Medium — B:** the control-description criterion is satisfiable by any ≥20-char source line plus its number; it cannot tell the real correction from boilerplate-plus-false-claim. Bounded claim needed: the check establishes quoting form only, not description correctness.

## 4. Receipt completeness gap

`criterion-control-description-r35-correction.txt:1` records the command with a literal `...` — `--repo`, `--bundle`, `--revision`, `--path` are elided, so the receipt alone does not permit exact reproduction. I reconstructed `--repo . --bundle .ufo/waves/round-34/retained/r34-c1-lookup-dcef39b5.bundle --revision dcef39b5 --path scripts/link_preview_audit.py` and got the exact recorded output ("quotes source line 15 verbatim (45 characters)"), but the recorded command should be complete. The other five receipts record full commands.

## 5. Residual risk / not verified

- Did not test InputError/exit=2 paths of the three checks (unreadable revisions, multi-block anchors); only the exit 0/1 contracts and the two exit-2 file-not-found runs during setup.
- Did not audit whether the real `fd0d53b2` gate registry table itself satisfies any additional implicit convention (my finding is that nothing in the check distinguishes it from any other table).
- Did not re-run the receipts at revisions other than `7deacc4`/attack commits, and did not touch the sealed counters (out of scope, held items).
- No tools installed or updated (nothing needed beyond python3/git already present); no pacman use.

Sandbox artifacts (deletable): `/fast/scratch/hyaku/kake-r35/w2/ReviewCriteriaChecks/clone` (branch `attack` at `2bac6f9`, `ee2b219`; attack files `attack-b.md`, `attack-c1-full-array.json`, `attack-c2-partial-array.json`, `attack-c3-values-as-keys.json`, `scripts/ghost_audit.py`), `/fast/scratch/hyaku/kake-r35/w2/ReviewCriteriaChecks/tmp`.
