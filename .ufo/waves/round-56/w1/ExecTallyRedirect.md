# ExecTallyRedirect

Claim C1 (calibration) — SKILL.md gate-registry row `redirect-expectation-audit`, line 1198 at base
`e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`. The row line is byte-identical at the lane worktree HEAD
`6b3df99d694f59d44504604da1a55a9fe1e9be75` (`git diff --stat e48354b7… HEAD -- SKILL.md` empty), and
`git rev-parse e48354b7…:scripts/redirect_audit.py` = `git rev-parse HEAD:scripts/redirect_audit.py` =
`8699e5d8ab3093dfc6ca9e49031ff3c7c7736422`, so the counter's `tool_changed` cannot fire for this row at
either revision. The replacement below applies at both.

## RUNS:

Scratch clone `D=$(mktemp -d)` = `/tmp/tmp.plywD30FVw`; `git clone -q --no-checkout <lane> "$D"` then
`git -C "$D" checkout -q e48354b7…`; `git -C "$D" rev-parse HEAD` → `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`;
`git -C "$D" rev-parse --show-toplevel` → `/tmp/tmp.plywD30FVw` (equals `$D`). Interpreter `Python 3.14.8`.

Command exactly as the row documents it, `cwd=$D`, `-B` kept, no env pin added — the script reads no
environment variable at all (grep for `environ`/`getenv`/`PYTHONHASHSEED`: no hit) and documents none:

```
python3 -B scripts/redirect_audit.py --selftest
```

| run | exit | wall (real) | last 3 lines |
|---|---|---|---|
| 1 | 0 | 0.221 s | `  PASS  cli negative control (exit 0, clean)` / `  PASS  cli bad input (exit 2)` / `selftest: 23/23 passed` |
| 2 | 0 | 0.210 s | `  PASS  cli negative control (exit 0, clean)` / `  PASS  cli bad input (exit 2)` / `selftest: 23/23 passed` |

Run 2 output saved to `/tmp/ra_run2.txt` (25 lines); a third run (0.236 s, exit 0, `user 0.499 / sys 0.218`
on the loaded host) diffed **identical** to run 2 — deterministic, 23 PASS lines each. No `__pycache__`, no
`*.pyc`, no files created in the lane or in the clone's worktree (all writes go to
`tempfile.TemporaryDirectory(prefix="kake-r46-redirect-")`).

Cross-check against the receipt the cell names: `git show HEAD:.ufo/waves/round-47/verification/selftest-redirect-audit.txt`
records `tool_sha256: 1e1dff18030c9028d833ab108bff140102343f4c5198c35984e7838e54bb748a` (= `sha256sum
scripts/redirect_audit.py` at base, exact) and `selftest: 23/23 passed` / `exit=0` — current, not stale.

## WHAT N COUNTS:

N is **assertion/PASS lines**, not fixtures. `selftest()` appends one entry per check to `passed` and
prints `selftest: {len(passed)}/{len(passed)+len(failures)} passed` (lines 570–572). At base the 23 PASS
lines decompose as (counted from the output, matching the code paths):

- 11 flag witnesses — `w1_shadowed_redirect`, `w2_first_match_shadow`, `w3_redirect_vs_rewrite`,
  `w4_splat_destination`, `w5_status_mismatch`, `w7_placeholders`, `w8_unmatched_none`,
  `w9_no_resource_precedence`, `w10_default_status`, `w11_malformed_rule`, `w12_malformed_status`
  (`_witnesses()`, kind `"flag"`). Note the numbering gap: there is **no W6**.
- 3 clean cases — `c6_encoded_path`, `c7_placeholders_correct`, `c8_first_match_correct` (kind `"clean"`).
- 6 in-memory mutants — `drop_status_check`, `drop_first_match`, `drop_resource_precedence`,
  `accept_malformed_rules`, `always_clean`, `skip_url_decoding` (`_mutants()`, one kill assertion each).
- 3 end-to-end CLI controls — positive (`exit 1`, one finding), negative (`exit 0`, clean), bad input
  (`exit 2`), each a real `subprocess.run` of the tool.

So 14 witness/clean fixtures + 6 mutants + 3 CLI controls = 23 assertions, each fixture yielding exactly
one. The denominator is not a fixed constant: a failure prints `22/23` (measured by feeding
`selftest: 22/23 passed` to the counter's `parse_tally` → `(22, 23)`), so printed B is a total.

The row's Self-test cell states `(23/23; …)` — numerator 23, denominator 23 — equal to both observed
numbers. The counter's POP regex for this row, `\((\d+)/\d+;`, captures the **numerator only** (`[23]`,
sum 23) and compares it to the observed **denominator** B = 23 → no `claim_ne_observed`. Because A == B in
a passing run that comparison is safe here; it is not if anyone writes an `A/B` pair with A != B.

## HEAD DEPENDENCE:

Grep over `scripts/redirect_audit.py` (607 lines) for `rev-parse`, `HEAD`, `git `, `git show`, `environ`,
`getenv`: **no hit**. The only `corpus/` mention is docstring line 8 (`grounded in
corpus/knowledge/redirect-rewrite-rules.md`) — prose, not a read. Files read beyond its own script:

- `scripts/redirect_audit.py` itself, re-spawned as a child process by absolute path derived from
  `os.path.dirname(os.path.abspath(__file__))` (line 521) — the **working tree beside the script**, not
  HEAD, not the CWD. Verified CWD-independent: running `python3 -B /tmp/tmp.plywD30FVw/scripts/redirect_audit.py
  --selftest` from `/tmp` also gives `23/23`, exit 0, 0.191 s.
- Two temp manifests it writes then the child reads: `$TMP/m.json` (`run_cli`, lines 526–531) and
  `$TMP/bad.json` (lines 553–556). `load_manifest`'s `open()` (line 212) runs only inside that child, on
  those temp paths; `--json`'s `open()` (line 598) is not reached. `sys.executable` is not a repo file.

Nothing under `corpus/`, `SKILL.md`, or `.ufo/` is read, so neither the tally nor the exit code can move
when those change.

Extra-commit proof — second scratch clone `D2=$(mktemp -d)` = `/tmp/tmp.sZOhw34VmC`, `git -C "$D2"
rev-parse --show-toplevel` → `/tmp/tmp.sZOhw34VmC` (equals `$D2`), base `e48354b7…`, then one commit
`35e4d76de20004162c73bd3bb8ad2a32c99d233f` made with `git -C "$D2" -c user.name=selftest -c
user.email=selftest@local commit`:

`git show --stat` of that commit: `.ufo/waves/round-56/zz-probe.md` +3 (round-56/ did not exist at base),
`SKILL.md` +1 (extra registry row `redirect-expectation-audit-probe`, 23/23), `corpus/README.md` +2,
`corpus/SOURCES.md` +1, `corpus/knowledge/zz-probe-redirect.md` +3.

Rerun of the documented command at `35e4d76` (tip): exit 0, `selftest: 23/23 passed`, 0.141 s. Rerun at
`e48354b7` (base) in the same clone: exit 0, `selftest: 23/23 passed`, 0.134 s. The counter's own
`parse_tally` on all three outputs (`/tmp/ra_run2.txt`, `/tmp/d2_tip.txt`, `/tmp/d2_base.txt`) returns
`(23, 23)`.

Answer: **no** later commit touching `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/`,
`SKILL.md`, or adding files under `.ufo/waves/round-56/` changes the tally or fails the selftest — proven
above. The tally moves only with `scripts/redirect_audit.py` itself (witness/mutant/CLI tables in that one
file), and — because the working tree beside the script is what executes — an *uncommitted* edit to that
script also moves it while HEAD is unchanged.

## REPLACEMENT CELL:

Exact Self-test cell text (command first in backticks, receipt prose unchanged, the tally stated as what
it counts; `23/23;` form retained because the POP regex `\((\d+)/\d+;` requires it):

```
`python3 -B scripts/redirect_audit.py --selftest` (23/23; 23 = 11 flag witnesses + 3 clean cases + 6 in-memory mutants + 3 end-to-end CLI controls, one PASS line each; receipt `.ufo/waves/round-47/verification/selftest-redirect-audit.txt` names tool path + sha256 + tally)
```

Whole-row line to land (line 1198), same cell substituted, all other cells untouched:

```
| redirect-expectation-audit | gate (offline; no network) | `python3 -B scripts/redirect_audit.py --manifest PATH` (manifest v1: `rules`, `resources`, `checks`; `resourcePrecedence` and `defaultStatus` host fields) | `0=clean`; `1=failed-policy` (a check's decided outcome differs from its expectation); `2=could-not-evaluate` (input); `64=usage` | `python3 -B scripts/redirect_audit.py --selftest` (23/23; 23 = 11 flag witnesses + 3 clean cases + 6 in-memory mutants + 3 end-to-end CLI controls, one PASS line each; receipt `.ufo/waves/round-47/verification/selftest-redirect-audit.txt` names tool path + sha256 + tally) | `python3 -B .ufo/waves/round-46/c46_matrix.py --root . --revision <rev> --stage before\|after` — 11/11 witnesses caught, 0 clean false positives, 3/3 controls rejected, wall <120 s; contract `corpus/knowledge/redirect-rewrite-rules.md` (S050, S135) | reads the manifest; writes only an optional `--json` report path | kake |
```

Checked with the counter's own functions (`.ufo/waves/round-56/c56_selftally.py` loaded read-only via
`importlib`, `-B`, no counter run and no other row touched):

- `documented_command` → `['python3', '-B', 'scripts/redirect_audit.py', '--selftest']`; `selftest_cell`
  → this cell (the Entry-command cell is not selected: `_is_selftest_span` needs `--selftest` in the words
  and `redirect_audit.py` has no `selftest` in its basename).
- POP regex `\((\d+)/\d+;` on the proposed cell → `[23]`, sum **23** = observed total B → no
  `claim_ne_observed`, no `claim_missing`.
- Control: the same cell rewritten as `(23 fixtures; …)` → `[]` → `claim_missing`. **The `(N fixtures)`
  shape does not work for this row**; the `N/M;` shape is mandatory here.

## RISKS:

- The row cannot adopt the sibling rows' `(N fixtures)` idiom: this row's POP regex is `\((\d+)/\d+;`, so a
  fixtures-worded cell would turn the row into `claim_missing`. A uniform registry vocabulary needs a
  counter POP change, not a doc change.
- The claim is a numerator, the observation a denominator. They coincide only while A == B; if a future
  edit states e.g. `(22/23; …)` the counter reports `claim_ne_observed` even though the run is clean.
  (A genuine failure already trips `selftest_failed` on the same row, so the failure mode is loud, not silent.)
- `parse_tally` keeps the **last** line containing `pass|selftest` that holds a `\bN/M\b`: measured,
  `"selftest: 23/23 passed\n  PASS  note 5/9 subcases\n"` → `(5, 9)`, so any future PASS/warning line with
  a fraction printed after the tally would silently replace the observed value (none exists today).
- `table_rows` keeps the **first** row per first cell (measured: a duplicated
  `redirect-expectation-audit` row yields the first). A later commit that prepends a same-named row would
  shadow line 1198 for the counter without any diff to line 1198.
- The tally is a count of PASS lines over a fixture table living in the same file as the decision logic it
  grades; adding one witness or mutant moves B (and must move the cell). It is a bounded count, not an
  oracle — the row's round-46 residual note records surviving mutants and a basename-matcher control gap,
  so 23/23 certifies the listed assertions only.
- `tool_changed` compares the script blob at the measured revision to BASE_REV. The blob is unchanged
  today, but any round that edits `scripts/redirect_audit.py` while keeping the cell at `23/23` will be
  marked `tool_changed` regardless of the tally — a cell edit alone cannot clear that row.
- Timing headroom is large (0.13–0.24 s vs the counter's `TIMEOUT = 300`) even on the loaded host.
- Scope: all runs in `/tmp` scratch clones; lane worktree, lane jj state and lane Git index untouched; only
  this report written; no installs, no pacman.

VERDICT: redirect-expectation-audit observes 23/23 (exit 0, twice, 0.221 s / 0.210 s; third run identical) — N counts 23 PASS assertions (11 flag witnesses + 3 clean cases + 6 mutants + 3 CLI controls), matching the row's stated 23/23 and the counter's captured numerator 23; the selftest reads only its own script plus its temp manifests (no HEAD/env/corpus/SKILL/.ufo read), proven by an extra-commit rerun still at 23/23; replacement cell keeps the required `(23/23; …)` shape (a `(23 fixtures)` rewrite would be claim_missing) and yields claim 23 under the POP regex.
