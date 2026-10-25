# CriticC1Contract

Attack of claim C1 (`met: tally_mismatches == 0 AND rows_checked == 10`) before any build. Read
`contract.md`, `contract.json` (C1 object), `c56_selftally.py` (367 lines), the committed base control
`controls/base-c1-selftally.txt`, and the ten pinned scripts' output lines at base. Every attack/wrong-reject below was
executed against the counter's own `measure()` in `mktemp`-initialised git sandboxes (the module's `_sandbox`), or in a
throwaway clone of `e48354b7c26b`; results are the printed exit codes, not predictions, except where marked
`[INFERENCE]`. Line refs are `c56_selftally.py`.

## ATTACKS:

**A1 — fake printer named in the SKILL.md span (script blob untouched).** Input: self-test cell
`` `python3 -c "print('selftest: 106/106 passed')" scripts/base_path_selftest.py` (106 fixtures) ``. Predicted/observed
**exit 0**. Root: `_is_selftest_span` (l.101-105) only needs the script path to be one *word* of the span, and
`run_command` (l.163) only needs `argv[0] in {python3,python,node}`. The pin at l.189-190 guards the script blob, never
the command. Covered by the 20-check selftest: **no** (`tool_replaced_by_fake_print` edits the script, not the span).
Note the span text is executed with inherited env and the caller's privileges — SKILL.md becomes executable content.

**A2 — honest command present but shadowed by an earlier qualifying span.** Input: cell =
`` `python3 -c "print('selftest: 6/6 passed')" t/alpha_selftest.py` `python3 -B t/alpha_selftest.py` (6 fixtures) ``
with the real selftest printing 4/4. `documented_command` returns the **first** qualifying span (l.107-119), so the fake
wins. Observed **exit 0** while the honest command contradicts the claim. Covered: **no** (unit
`entry_command_not_selftest` tests the opposite order — a non-qualifying span first).

**A3 — duplicate row earlier in the file.** `table_rows` (l.89-98) is file-global, first-occurrence-wins, no `##`
scoping. Input: insert `| base-path-audit | <command> (106 fixtures) |` in any earlier table, leave the gate-registry
row stale. Observed **exit 0**. Covered: **no** (`row_deleted` only tests absence).

**A3c — row moved out of the gate registry.** Delete the registry row, re-add the same name under `## Notes` with a
corrected claim. Observed **exit 0**; the registry loses the row it is supposed to calibrate. Covered: **no**.

**A4 — helper module inflation.** Only the named script's blob is compared (l.189-190). Input: edit a module the pinned
selftest imports so its printed total equals the stale claim (or the claim equals the inflated total). Observed **exit
0**. Covered: **no** (`tool_replaced_by_fake_print` replaces the named script itself).

**A5 — two junk claims whose sum equals the tally.** `claim = sum(nums)` (l.196-198). Input: cell
`(2 fixtures) (2 fixtures)` against observed 4/4 — the doc never states the tally 4. Observed **exit 0**. Covered:
**no** (`two_claims_sum_wrong` only tests a *wrong* sum).

**A6 — host environment leak (live on the real population).** `run_command` uses `dict(os.environ, …)` (l.156). The real
`quote-truth-counter` row runs `.ufo/waves/round-52/c52_quote_truth.py --selftest`, whose fixture revision is
`os.environ.get("KAKE_R52_SELFTEST_REV")` or HEAD. At base that command prints `17/18`, exit 1 (base control; re-verified
in a clone). With `KAKE_R52_SELFTEST_REV=1ae8de5d4dee` exported it prints `18/18`, **exit 0** (verified). So: fix the
other six claims in SKILL.md, export one shell variable, and the predicate is met with the stale round-52 fixture
untouched and no repo repair at all. Covered: **no** (no case scrubs or sets `os.environ` beyond a leading `PIN=1` span).

**A7 — the eleventh registry row is invisible (population is a choice).** Input: add
`| link-preview-audit | … (999 fixture directories) |`. Observed **exit 0**; the excluded row's cell is never read, so
the exclusion is unguarded in both directions (a wrong `46` there would also pass). Covered: **no**
(`population_one_short` tests a shortened pop, not an extra row).

**A8 — span points the selftest at host state outside the clone.** Input: `python3 -B scripts/x_selftest.py --root
/home/vgpnk/Projects/shokunin/kake-shokunin`. The observed tally comes from the mutable working tree, not the measured
revision. Observed **exit 0** with a host-file-driven tally. Covered: **no**.

**A9 — `rows_checked` is vacuous.** `results` gets one entry per `POP` row even when the row is missing (l.184-188), and
`met` uses `len(results) == expected` (l.222). With the real ten-row `POP` and a SKILL.md containing **none** of the ten
rows, the counter prints `rows_checked=10` (mismatches 10, exit 1 — observed). So the frozen predicate's second conjunct
can never be why `met=False`, and `rows_checked=10` is not evidence that ten rows were found. Covered: **no**.

**A10 — caller-chosen revision.** `main` validates only that `--revision` resolves (l.348-356); nothing binds it to the
wave tip or pins the counter's own blob (`contract.json`'s C1 object carries predicate/counter/baseControl/kill and **no
sha256**). "C1 met at rev X" is self-reported provenance. Covered: **no**.

## WRONG-REJECT:

**W1 — `env VAR=value python3 …` pin.** `run_command` lifts only *leading* `VAR=value` words and rejects any other
`argv[0]` (l.158-164). A row documenting `env KAKE_X=1 python3 -B scripts/x_selftest.py` yields **exit 2**
(observed: `unevaluable: unsupported command word ['env']`), though `contract.md` promises "any `VAR=value` pin the row
names" counts.

**W2 — honest total + breakdown on `base-path-audit`.** rx `(\d+) (?:matrix |round-29 regression )?fixtures`; the
corrected cell "(45 fixtures: 30 matrix fixtures plus 15 round-29 regression fixtures …)" sums to **90** vs observed 45
→ `claim_ne_observed`, **exit 1** (arithmetic verified: `['45','30','15']`). That row is already correct at base, so any
clarification of it becomes a mismatch.

**W3 — multi A/B output, last line wins.** `parse_tally` (l.129-139) keeps the last matching line. A selftest printing
`selftest: 4/4 passed` then `selftest: coverage 3/4 lines` yields observed `(3,4)` → `selftest_failed`, **exit 1**
(observed). Related hole: for rows whose success line prints `passed/passed` (`redirect_audit.py:570`) the `A == B` half
is a tautology, leaving exit code as the only guard.

**W4 — the natural repair is rejected.** Any edit to a pinned script trips `tool_changed` (l.189-190) even when the row
then states the truth and the selftest passes (observed: **exit 1**, `tool_changed` + `claim_ne_observed`). Live case:
`quote-truth-counter`'s documented command prints `17/18`, exit 1 at base; its failures are C5 (S374 quote) and C8
(`registry rows 156 != mirror rows 145 + 3`). C8 cannot be cleared without rewriting the frozen round-52 mirror/pin, and
the honest fix — repairing the fixture in `c52_quote_truth.py` — is exactly what `tool_changed` rejects. For that row the
predicate is satisfiable only via A1/A2/A6. This is the central inversion: the counter forbids the real repair and admits
the fake one.

**W5 — prose tally.** `selftest: 4 cases, 4 passed` → `tally_unparsable`, **exit 2** (observed), even when the row is
exactly right. A wording change in a selftest is unevaluable, never a pass.

**W6 — command not prefixed by `python3`/`node`.** `./scripts/x_selftest.py` → `command_missing`, **exit 1** (observed).
`[INFERENCE]` Same for `python3 -m …` and for a cell that only mentions the script path in backticks (→ exit 2).

## RECOMMENDED COUNTER CHANGES:

Before data, in `c56_selftally.py`:

1. **Pin the command, not just the script** (l.101-119, l.154-168). After `shlex`, require `argv[0] in {python3,python}`,
   `argv[1] == "-B"`, `argv[2] == script`, and a whitelist of flags; reject `-c`, `-m`, extra positional words and
   absolute paths. Kills A1, A2, A8; makes W6 a stated contract instead of a silent reject.
2. **Scrub the environment** (l.156): pass a fixed env (PATH, LANG, PYTHONDONTWRITEBYTECODE) instead of inheriting
   `os.environ`, and record the env keys in the receipt. Kills A6 and makes the measurement reproducible from bytes.
3. **Scope and de-duplicate the table** (l.89-98): parse only the gate-registry section and report a duplicate first cell
   as a mismatch instead of first-wins. Kills A3/A3c.
4. **Pin imported helpers** (l.189-190): compare the blob of every module the pinned script imports at `rev` vs
   `BASE_REV`. Kills A4.
5. **One stated tally per cell** (l.196-198): accept >1 match only when the row marks a sum explicitly, or subtract a
   stated breakdown from a stated total. Kills A5 and W2.
6. **First A/B line, or require agreement** (l.129-139): any disagreement between A/B lines is unevaluable. Kills W3's
   false reject and the last-wins hole.
7. **Accept `env VAR=value …`** as a documented pin, and reject pins not named in the row's prose (l.158-164). Kills W1.
8. **Bind `rows_checked` to rows *found*** (l.184-188, l.222) and bind `--revision` to the lane tip of the round
   (l.348-356); add the counter's own sha256 to `contract.json`'s C1 object. Kills A9/A10.
9. **Give `tool_changed` an honest exit** for a fixture repair (new receipt field pinning the new blob), or rewrite the
   `quote-truth-counter` row to invoke with `KAKE_R52_SELFTEST_REV=<base>` *in the row* — and say so in the contract's
   After. Otherwise W4 leaves one of the ten rows satisfiable only by a fake.
10. **Selftest**: add cases for A1, A2, A3, A3c, A4, A5, A6, A7, A8, A9, W1, W5. The committed 20 checks (13 cases +
    7 unit) kill none of them; in particular there is no case where a qualifying-but-fake span shadows the honest one, no
    case with an extra registry row, and no case asserting that `rows_checked` reflects rows found.

Scope note for the L1: the C1 axis sits outside the prompt's declared operability/freshness axes (contract.md says so
itself); that ownership question is the operator's, not mine. Nothing above disputes C2.

VERDICT: C1 is not attack-proof — nine do-nothing/junk inputs reach `met` (A1, A2, A3/A3c, A4, A5, A6, A7, A8) with zero
coverage by the committed 20-check selftest, and the predicate wrongly rejects five honest states (W1, W2, W3, W4, W5);
A6 is live on the real population (one exported `KAKE_R52_SELFTEST_REV` clears the only failing row), and A9 makes
`rows_checked == 10` structurally vacuous. Fix l.89-98, 101-119, 129-139, 154-168, 184-190, 196-198, 222 before data.
