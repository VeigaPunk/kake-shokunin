# ExecC1Counter

## DESIGN:

- Frozen predicate constant: `PREDICATE` at line 82. The 28 path/blob pairs are hardcoded at lines 103–134; path-regex discovery for unexpected members is at lines 208–211. `measure` enforces identity, flags missing/changed/extra paths, counts unchanged frozen members, and evaluates the gate at lines 522–566.
- Rendered Markdown masking/table and arbitrary-row duplicate scan: lines 215–300. Registry-row matching, exact eight nonempty cells, `0=`/`1=` verdict-map rule, ASCII-word label detection, pin/ancestor/member-at-pin checks, and exit predicates: lines 407–490.
- Command A2/A3 handling: bracket segment filtering and shlex parse at lines 302–321; shape, permitted env, revision-placeholder, root/selftest, and metacharacter checks at lines 324–346; placeholder rendering at lines 348–380. Fresh shared detached clones, fixed four-variable runtime environment, timeout-to-124, and cleanup at lines 383–405. The report includes the member command (and pin command when applicable) via lines 570–580.
- SCORECARD exact-one-axis-table, exact-one-row-per-axis, formatting-stripped digit-exact score logic: lines 493–519. `--root` toplevel/revision resolution, usage exit 64, `--json`, and main output are at lines 1097–1159.
- Selftest fixtures and checks are at lines 716–1094. Retained selftest evidence: `selftest 76/76 passed` (2026-10-27), including row masks/duplicate/junk cases, each label and mismatch family, placeholder/env checks, 27/29 member counts, missing/changed/extra identities, score mutant and score-table variants, and CLI cases.

## SELFTEST:

Verbatim tally: `selftest 76/76 passed`.

## BASE RUN:

Verbatim stdout from the requested base-revision run (the shell wrapper's final `EXIT=0` is the `cat` status; the counter itself returned 1, consistent with `met=False`):

```text
.ufo/waves/round-48/c48_lint_count.py label=- e_T=- MISMATCH unregistered
.ufo/waves/round-48/c48_quote_truth.py label=- e_T=- MISMATCH unregistered
.ufo/waves/round-49/c49_order.py label=- e_T=- MISMATCH unregistered
.ufo/waves/round-49/c49_quote_truth.py label=- e_T=- MISMATCH unregistered
.ufo/waves/round-50/c50_durable.py label=- e_T=- MISMATCH unregistered
.ufo/waves/round-50/c50_quote_class.py label=- e_T=- MISMATCH unregistered
.ufo/waves/round-51/c51_quote_truth.py label=- e_T=- MISMATCH unregistered
.ufo/waves/round-51/c51_wave_ledger.py label=- e_T=- MISMATCH unregistered
.ufo/waves/round-52/c52_gate_registry.py label=- e_T=- MISMATCH unregistered
.ufo/waves/round-52/c52_mutation_ladder.py label=- e_T=- MISMATCH unregistered
.ufo/waves/round-52/c52_quote_truth.py label=historical e_T=1 e_P=0 ok
    argv=python3 -B .ufo/waves/round-52/c52_quote_truth.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d
    argv@pin=python3 -B .ufo/waves/round-52/c52_quote_truth.py --root . --revision 1ae8de5d4dee8300624b0db2a94497ff905942c5
.ufo/waves/round-52/c52_wave_ledger.py label=live e_T=0 ok
    argv=python3 -B .ufo/waves/round-52/c52_wave_ledger.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d
.ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py label=live e_T=1 MISMATCH live_not_green
    argv=python3 -B .ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py --revision 97cdc122379711c2b02a8970752c8782da3ac81d
.ufo/waves/round-54/c54_ops_debt.py label=- e_T=- MISMATCH unregistered
.ufo/waves/round-54/c54_s374_calib.py label=- e_T=- MISMATCH unregistered
.ufo/waves/round-55/c55_quote_truth.py label=historical e_T=1 e_P=0 ok
    argv=python3 -B .ufo/waves/round-55/c55_quote_truth.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d
    argv@pin=python3 -B .ufo/waves/round-55/c55_quote_truth.py --root . --revision 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6
.ufo/waves/round-55/c55_readme_index.py label=historical e_T=1 e_P=0 ok
    argv=python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d
    argv@pin=python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6
.ufo/waves/round-56/c56_quote_truth.py label=historical e_T=1 e_P=0 ok
    argv=python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d
    argv@pin=python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision 4cb225fb032b04166fb0232bc98a7bcce72675ec
.ufo/waves/round-56/c56_selftally.py label=live e_T=0 ok
    argv=python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d
.ufo/waves/round-57/c57_idresolver_gate.py label=live e_T=0 ok
    argv=python3 -B .ufo/waves/round-57/c57_idresolver_gate.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d --fleet /home/vgpnk/Projects/shokunin
.ufo/waves/round-57/c57_quote_truth.py label=historical e_T=1 e_P=0 ok
    argv=python3 -B .ufo/waves/round-57/c57_quote_truth.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d
    argv@pin=python3 -B .ufo/waves/round-57/c57_quote_truth.py --root . --revision 32754df75774dd38e8a96fcda375fc93adf97f1e
.ufo/waves/round-57/c57_receipt_pins.py label=historical e_T=1 e_P=1 MISMATCH historical_not_green_at_pin
    argv=python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d
    argv@pin=python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root . --revision 32754df75774dd38e8a96fcda375fc93adf97f1e
.ufo/waves/round-58/c58_quote_truth.py label=historical e_T=1 e_P=0 ok
    argv=python3 -B .ufo/waves/round-58/c58_quote_truth.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d
    argv@pin=python3 -B .ufo/waves/round-58/c58_quote_truth.py --root . --revision 8d340c15200959190ba3e894399cdc931976331f
.ufo/waves/round-58/c58_receipt_rewrites.py label=live e_T=0 ok
    argv=python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d
.ufo/waves/round-58/c58_resolver_cases.py label=live e_T=0 ok
    argv=python3 -B .ufo/waves/round-58/c58_resolver_cases.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d --work <scratch>
.ufo/waves/round-59/c59_axis_evidence.py label=live e_T=0 ok
    argv=python3 -B .ufo/waves/round-59/c59_axis_evidence.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d
.ufo/waves/round-59/c59_quote_truth.py label=live e_T=0 ok
    argv=python3 -B .ufo/waves/round-59/c59_quote_truth.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d
.ufo/waves/round-59/c59_resolver_cases.py label=live e_T=0 ok
    argv=TMPDIR=<scratch> python3 -B .ufo/waves/round-59/c59_resolver_cases.py --root . --revision 97cdc122379711c2b02a8970752c8782da3ac81d --work <scratch>
C1 gate-status members=28 mismatches=14 scores_held=3/3 met=False
EXIT=0
```

## CONTRACT AMBIGUITIES:

- L1 A2 resolved the bracket rule: only bracket segments containing one or more `<scratch>` / `<fleet root>` placeholders are kept; revision-placeholder and placeholder-free segments are dropped.
- A5 requires historical exits `(e_T=1,e_P=0)` and never-met `(1,1)` but names no classes for other nonzero statuses. The implementation assigns `historical_bad_exit` / `never_met_bad_exit` to exit codes outside `{0,1}`; zero remains the named `*_but_green` class. This classification is an interpretation, not a contract-provided name.
- The recorded base output prints `<scratch>` symbolically in argv summaries; the actual per-run scratch paths are unique temporary directories and were removed after each observation. The counter return was 1; `EXIT=0` at the final wrapper line is only the `cat` command's status.

VERDICT: Counter implemented in the assigned .files path; amended base evaluation recorded 28 frozen members, 14 mismatches, scores held 3/3 (not met); selftest 76/76 passed.
