members_found=28 duplicates=0 c56_only_live_selftally=yes pin_ancestor_exit=0

# ScoutGateRows — Recon of SKILL.md Gate Registry at Base 3c68645a

Verdict line:
`members_found=28 duplicates=0 c56_only_live_selftally=yes pin_ancestor_exit=0`

## Summary of Findings

1. **Registry Population (28 members)**: Exactly 28 members are defined in `FROZEN` in `.ufo/waves/round-66/c66_gate_status_hostportable.py`. All 28 members are present in SKILL.md table rows at base revision `3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1`. There are 0 missing rows and 0 duplicate rows among table data rows.
2. **Table Schema and Member Mapping**: SKILL.md registry tables define columns `| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |`. The first cell (`Name`) contains the gate slug identifier (e.g., `citation-lint-existence-counter`, `selftest-tally-counter`), except for member `.ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py` where the first cell is `c53_gate_truth.py`. In all 28 rows, the member script path is referenced in the `Entry command` cell (cell 3), and both cell 1 and cell 3 establish a 1-to-1 bijection with the 28 FROZEN keys.
3. **c56 Selftest Tally Counter (`c56_selftally`)**: Row at line 1253 (`selftest-tally-counter`) is the only row whose base command is `python3 -B .ufo/waves/round-56/c56_selftally.py`. Its Kind cell contains neither `historical` nor `never met`, defaulting under the c66 label grammar to `live`. No other row in SKILL.md references `c56_selftally.py` or has this base command.
4. **c66 Historical Label Rule & Ancestor Pin**: Under `c66_gate_status_hostportable.py`, a row is `historical` iff its Kind cell contains the word `historical` (tokenized by `\b[A-Za-z0-9_-]+\b`). A historical label requires a 40-hex SHA pin that must be an ancestor of the tested revision (`git merge-base --is-ancestor <pin> <rev>`). The proposed round-56 pin `4cb225fb032b04166fb0232bc98a7bcce72675ec` was verified against base revision `3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1` and exits 0.

## 28 Registry Rows (Base 3c68645a)

| # | First Cell (Name) | FROZEN Member Path | Kind Cell Verbatim (first 200 chars) |
|---|---|---|---|
| 1 | `citation-lint-existence-counter` | `.ufo/waves/round-48/c48_lint_count.py` | gate (live; operability: the round-48 citation-lint repair — a token resolves by object existence, not `git rev-parse --verify`; green at round-60 base `97cdc122`) |
| 2 | `client-rendering-quote-truth-counter` | `.ufo/waves/round-48/c48_quote_truth.py` | gate (live; freshness: round-48 S137/S138/S139/S249 row-entry-quote-receipt truth, R4 matched per id against the retained text beside the receipt; the pre-fix counter blob exits 1 at its own measured  |
| 3 | `pre-append-order-counter` | `.ufo/waves/round-49/c49_order.py` | gate (live; operability: round-49 order proof — `pre_rev` strict ancestor, adopted ids absent before and present after, `--file`-only census exit 0, sibling counter reads committed bytes; green at rou |
| 4 | `crawl-budget-quote-truth-counter` | `.ufo/waves/round-49/c49_quote_truth.py` | gate (live; freshness: round-49 S273/S274 row-entry-quote-receipt truth over committed bytes only — R4 is `git show <rev>:.ufo/waves/round-49/sources/<textPath>`; green at round-60 base `97cdc122`) |
| 5 | `wave-grant-durability-counter` | `.ufo/waves/round-50/c50_durable.py` | gate (live; offline, committed bytes only, `git show` and `git merge-base --is-ancestor` only) |
| 6 | `quote-class-counter` | `.ufo/waves/round-50/c50_quote_class.py` | gate (live; offline, committed bytes only, `git show` only) |
| 7 | `canonical-crawler-identity-quote-truth-counter` | `.ufo/waves/round-51/c51_quote_truth.py` | gate (live; offline, committed bytes only, `git show`, `git log` and `git ls-tree` only) |
| 8 | `wave-evidence-ledger-v1` | `.ufo/waves/round-51/c51_wave_ledger.py` | gate (live; offline, committed bytes only, `git show` and `git ls-tree` only; v1 of the round-52 `wave-evidence-ledger` gate) |
| 9 | `gate-registry-completeness-counter` | `.ufo/waves/round-52/c52_gate_registry.py` | gate (historical: green at its round-52 measured revision `1ae8de5d4dee8300624b0db2a94497ff905942c5` (also green at `a4a890c` and tip `a1d83ec`); red on later trees by design — `frozen_baselines` hash |
| 10 | `ledger-mutation-ladder` | `.ufo/waves/round-52/c52_mutation_ladder.py` | gate (live; differential red-before ladder — runs the round-51 and hardened round-52 ledger scripts over the selftest fixture family harvested from committed round-51 evidence; green at `97cdc12237971 |
| 11 | `quote-truth-counter` | `.ufo/waves/round-52/c52_quote_truth.py` | gate (historical: green at its round-52 measured revision `1ae8de5d4dee8300624b0db2a94497ff905942c5` only; red on every later tree by design — its mirror pins the 148-row registry; offline, committed  |
| 12 | `wave-evidence-ledger` | `.ufo/waves/round-52/c52_wave_ledger.py` | gate (offline, committed bytes only; no network) |
| 13 | `c53_gate_truth.py` | `.ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py` | gate (never met: red at its round-53 measured revision `fd91527a286086c1f4e6d4f44f715a907f041b5d` (exit 1) and at every committed revision run since, the round-60 base included: the S312/S329 locator  |
| 14 | `ops-debt-counter` | `.ufo/waves/round-54/c54_ops_debt.py` | gate (historical from round 60: green at its round-54 measured revision `a631cc0246b97f2a949d61186c7466468faf94d6` and on every tree up to the round-60 base; red from round 60 on by design — its regis |
| 15 | `s374-calibration-counter` | `.ufo/waves/round-54/c54_s374_calib.py` | gate (live; green at the round-60 base 97cdc122 and at its round-54 measured revision a631cc0246b97f2a949d61186c7466468faf94d6; red 1 at the round-54 base 68228b2d, mismatches=1; the bound `[r54-corre |
| 16 | `yahoo-robots-quote-truth-counter` | `.ufo/waves/round-55/c55_quote_truth.py` | gate (historical: green at its round-55 measured revision `64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6` only; red on later trees by design — mirror pins 156 rows; offline, committed bytes only) |
| 17 | `readme-index-counter` | `.ufo/waves/round-55/c55_readme_index.py` | gate (historical from round 59: green at its round-55 measured revision `64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6` and on the round-58 tree; red from round 59 on by design — its `head_changed` term re |
| 18 | `yahoo-crawl-handling-quote-truth-counter` | `.ufo/waves/round-56/c56_quote_truth.py` | gate (historical: green at its round-56 measured revision `4cb225fb032b04166fb0232bc98a7bcce72675ec` only; red on later trees by design — mirror pins 158 rows; offline, committed bytes only) |
| 19 | `selftest-tally-counter` | `.ufo/waves/round-56/c56_selftally.py` | gate (offline, committed bytes only; runs the ten documented selftests in a clone of the revision) |
| 20 | `id-resolver-gate` | `.ufo/waves/round-57/c57_idresolver_gate.py` | gate (differential: a reference implementation inside the gate against the tool, over randomised fixtures and the real revisions; reads sibling registries) |
| 21 | `baidu-dead-link-quote-truth-counter` | `.ufo/waves/round-57/c57_quote_truth.py` | gate (historical from round 58: green at its round-57 measured revision `32754df75774dd38e8a96fcda375fc93adf97f1e`; red once a later round appends a registry row — mirror pins 158 rows + the 2 adopted |
| 22 | `receipt-pin-counter` | `.ufo/waves/round-57/c57_receipt_pins.py` | gate (historical from round 58: green from `20217f23eca15862febe14545523832e21584106`, the commit that landed the third round-57 after-receipt — red at the round-57 measured revision `32754df7` itself |
| 23 | `baidu-crawler-identification-quote-truth-counter` | `.ufo/waves/round-58/c58_quote_truth.py` | gate (historical from round 59: green at its round-58 measured revision `8d340c15200959190ba3e894399cdc931976331f`; red on later trees by design — C7 pins the round-58 validate scratch and C8 the 160- |
| 24 | `receipt-rewrite-counter` | `.ufo/waves/round-58/c58_receipt_rewrites.py` | gate (offline; first-parent history walk over every file at any depth under every round's `control(s)/`, against the round-58 ledger) |
| 25 | `resolver-cases-counter` | `.ufo/waves/round-58/c58_resolver_cases.py` | gate (the tool at the revision against gate-built fixture lanes with per-run fixture ids; every fixture repo is `git init` in its own dir) |
| 26 | `axis-evidence-counter` | `.ufo/waves/round-59/c59_axis_evidence.py` | gate (offline; calibration: the SCORECARD axis-table evidence cells against committed blobs at the measured revision; base pinned at `fd6303ce`) |
| 27 | `crawler-identity-quote-truth-counter` | `.ufo/waves/round-59/c59_quote_truth.py` | gate (historical from round 60: green at its round-59 measured revision `b322ccabe1628fc0cfe80c2dddca03ed154d1349`; red from round 60 on by design — C8 requires the registry minus S425/S426 to equal t |
| 28 | `disclosed-route-resolver-cases-counter` | `.ufo/waves/round-59/c59_resolver_cases.py` | gate (the tool at the revision against gate-built fixture lanes with per-run fixture ids; every fixture repo is `git init` in its own dir; `--root` must be a repository toplevel) |

## Evidence Commands and Exit Codes

1. `git -C /home/vgpnk/Projects/shokunin/kake-shokunin merge-base --is-ancestor 4cb225fb032b04166fb0232bc98a7bcce72675ec 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1`
   - Exit code: `0`
   - Confirms pin `4cb225fb032b04166fb0232bc98a7bcce72675ec` is a strict ancestor of base revision `3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1`.

2. Independent awk/grep census over `git show 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1:SKILL.md`:
   - Command:
     ```bash
     git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1:SKILL.md | \
     awk -F'|' 'BEGIN { split(".ufo/waves/round-48/c48_lint_count.py .ufo/waves/round-48/c48_quote_truth.py .ufo/waves/round-49/c49_order.py .ufo/waves/round-49/c49_quote_truth.py .ufo/waves/round-50/c50_durable.py .ufo/waves/round-50/c50_quote_class.py .ufo/waves/round-51/c51_quote_truth.py .ufo/waves/round-51/c51_wave_ledger.py .ufo/waves/round-52/c52_gate_registry.py .ufo/waves/round-52/c52_mutation_ladder.py .ufo/waves/round-52/c52_quote_truth.py .ufo/waves/round-52/c52_wave_ledger.py .ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py .ufo/waves/round-54/c54_ops_debt.py .ufo/waves/round-54/c54_s374_calib.py .ufo/waves/round-55/c55_quote_truth.py .ufo/waves/round-55/c55_readme_index.py .ufo/waves/round-56/c56_quote_truth.py .ufo/waves/round-56/c56_selftally.py .ufo/waves/round-57/c57_idresolver_gate.py .ufo/waves/round-57/c57_quote_truth.py .ufo/waves/round-57/c57_receipt_pins.py .ufo/waves/round-58/c58_quote_truth.py .ufo/waves/round-58/c58_receipt_rewrites.py .ufo/waves/round-58/c58_resolver_cases.py .ufo/waves/round-59/c59_axis_evidence.py .ufo/waves/round-59/c59_quote_truth.py .ufo/waves/round-59/c59_resolver_cases.py", members, " "); for (i in members) m[members[i]]=1 } /^ *\|/ { name=$2; kind=$3; entry=$4; gsub(/^ +| +$/, "", name); gsub(/^ +| +$/, "", kind); gsub(/^ +| +$/, "", entry); for (k in m) if (index(entry, k)>0 || index(name, k)>0) { seen[k]++; printf "%s | %s\n", name, substr(kind,1,200) } } END { print length(seen) }'
     ```
   - Exit code: `0`
   - Count: `28` unique members matched across all table rows.

3. Census of `c56_selftally.py` rows in `SKILL.md`:
   - Command:
     ```bash
     git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1:SKILL.md | grep -n "c56_selftally"
     ```
   - Exit code: `0`
   - Output: exactly 1 match at line 1253 (`selftest-tally-counter`), with base command `python3 -B .ufo/waves/round-56/c56_selftally.py`.

4. Extraction of FROZEN keys from `c66_gate_status_hostportable.py`:
   - Command:
     ```bash
     git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1:.ufo/waves/round-66/c66_gate_status_hostportable.py | grep -E "^\s*\"\.ufo/waves/round-[0-9]+" | wc -l
     ```
   - Exit code: `0`
   - Count: `28` keys in dictionary `FROZEN`.

## Counterexamples and Edge Cases Checked

- **Duplicate Path Mentions Outside Tables**: `.ufo/waves/round-52/c52_gate_registry.py` appears in prose at line 1218 (`The completeness counter is .ufo/waves/round-52/c52_gate_registry.py`), but only appears in one table data row (line 1352). Neither `c66` table-cell parser nor markdown table parsing treats line 1218 as a table row.
- **First Cell Naming Asymmetry**: Member `c53_gate_truth.py` is the only row where the first cell (`Name`) is the filename rather than a descriptive kebab-case gate name. However, both name-based and entry-command-based lookups locate all 28 rows with zero ambiguity.
- **No Extra or Missing Members**: No member from `FROZEN` is missing, and none appears in more than one table row.
