# ReviewerSelftallyCode

Code review of `.ufo/waves/round-56/c56_selftally.py` (round-56 C1 counter) before claim measurement.
Evidence run: `--selftest` → `20/20`, exit 0. Full measurement at BASE_REV e48354b7 → `tally_mismatches=7 rows_checked=10`, exit 1 (7 stale documented claims vs live script tallies — that output is the counter doing its job, not a defect).

FINDINGS:

- HIGH — L61-62 (POP yahoo-robots-quote-truth-counter claim regex `(\d+) (?:sandbox-repo )?(?:fixtures|checks)`) + L192-193: the regex undercaptures the declared claim. The real cell reads "(47 sandbox-repo fixtures … plus 3 unit-rule checks" — "3 unit-rule checks" does not match (`unit-rule` is not in the prefix alternation), so `claim=47` where the cell declares 50. Failing input: live cell → `re.findall` → `['47']` (confirmed by running; live measurement shows `claim=47 observed=54/54`). Even the faithful sum (50) ≠ observed 54, so the row is stale anyway — but the counter must sum all declared integers. Fix: `r"(\d+) (?:sandbox-repo |unit-rule )?(?:fixtures|checks)"` → captures ['47','3'] (confirmed).

- MED — L113-116 `documented_command`: on `shlex.split` ValueError the function `return None` instead of continuing to later spans/cells, and diverges from `selftest_cell` (which still returns the first matching cell). Failing input: `["x", "`python3 -B t/a_selftest.py '`", "ok", "ok", "`python3 -B t/a_selftest.py` (1 fixtures)"]` → `documented_command` = None → `command_missing` although a valid documented command exists (confirmed by running). Fix: `except ValueError: continue` (return None only after all spans exhausted).

- MED — L103-104 `_is_selftest_span`: the `script in words` membership test runs on raw whitespace words before bracket-stripping/shlex, so the pinned script is invisible when documented quoted or `./`-prefixed. Failing inputs (confirmed by running): `` `python3 -B ./t/a_selftest.py` `` → None; `` `python3 -B "t/a_selftest.py"` `` → None → `command_missing` for a working command. Fix: strip brackets and `shlex.split` first, then test `script in words` and the selftest predicate on parsed words.

- MED — L112 `re.sub(r"\[[^\]]*\]", "", span)`: the non-nested pattern corrupts nested optionals and deletes legitimate bracket content. Failing input (confirmed by running): `[--tool [PATH]]` → argv `['python3','-B','t/a_selftest.py',']']` — a stray `]` arg passed to the script (usage-error path → `selftest_failed` or `tally_unparsable` on a healthy claim). `PIN=[1] python3 …` or `glob[0-9]` args would be silently rewritten the same way [INFERENCE]. Fix: strip only innermost `[...]` groups (loop until stable) or reject spans with residual `[`/`]` in parsed words.

- MED — L136-138 `parse_tally`: the `pass|selftest` substring filter accepts any `a/b` on a matching line as the tally. Confirmed inputs: `"selftest ran on 2026/10/25"` → `(2026,10)`; `"selftest: missing fixture 12/20"` → `(12,20)` — a death/diagnostic line masquerades as a tally (mismatch-1 instead of unevaluable-2; `a==b` on such a line would even fake a pass). Also the last `a/b` *on a line* wins: `"selftest: 2/3 passed (target 3/3)"` → `(3,3)`, masking a failure if exit is 0. Fix: anchor the tally (e.g. `(?:selftest|pass)[^\d]*(\d+)/(\d+)` near line end, or require the line's last numeric token to be the tally); optionally ignore `FAIL`-prefixed lines.

- MED — L92-95 `table_rows`: `line.strip().strip("|").split("|")` splits on escaped `\|`, fragmenting the cell. Failing input (confirmed by running): selftest cell `` `python3 -B t/alpha_selftest.py --stage before\|after` `` → `documented_command`=None → `command_missing`. Live SKILL.md unaffected today (its only `\|` sits in a later cell of the redirect row), but latent for the first named pipe inside a selftest cell. Fix: split on `(?<!\\)\|` or treat backtick spans atomically.

- LOW — L142-150 `clone_at`: `mkdtemp` dir leaks when clone or checkout raises (clone itself leaves a non-empty dir; on checkout failure the full clone is orphaned — `measure`'s `finally` never sees it because `clone` was never assigned). Confirmed by running: `clone_at(src, "0"*40)` raised and left `/tmp/c56-tally-30p4g0dl`. Fix: `try/except → shutil.rmtree(d, ignore_errors=True); raise`.

- LOW — L252-261 `_sandbox.commit`: `git add -A` only stages files written this round; a file committed at base but absent from the tip dict survives at tip. Confirmed by running: tip tree still contains `t/leftover.py`. Consequence: the selftest builder can never express "pinned script deleted at the measured revision" (silent coverage gap). Fix: delete tracked paths not in `files` before `add -A`.

- LOW — L163-164 `run_command`: the `argv[0]` allowlist turns any non-`python3|python|node` documented command (e.g. `env PIN=1 python3 …`, `python3.11`, `/usr/bin/python3`) into `RuntimeError`, which `measure` converts to a whole-run exit 2 discarding all previously measured rows (env-only command `["FOO=1"]` → `RuntimeError []`, confirmed by running). Spec permits exit 2 for "command could not run", so this is conforming but all-or-nothing; [INFERENCE] consider scoping the failure to the row or extending the allowlist.

- LOW — L165 `run_command`: no `stdin=subprocess.DEVNULL`; a selftest that reads stdin inherits the caller's terminal/pipe → blocks to the 300 s timeout → exit 2. [INFERENCE]

- INFO — L198: `blob(root, rev, script)` is called twice per row (the `is None` guard then the comparison) — one extra subprocess per row; harmless [INFERENCE: hoist into a local].

Context on the live base measurement (not counter defects): observed totals exceed stale claims for source-recheck 106≠101, robots 204≠137, sitemap 235≠150 (cell says "150 fixtures"), citation_lint 9≠8, readme_index 44≠35 (cell says 35), yahoo-robots 54≠47; and `quote-truth-counter` prints `17/18` at base — confirmed by running `c52_quote_truth.py --selftest` in a clean clone: its `pass` fixture fails C5_quote_truth (S374 quote not a raw substring) and C8_mirror_bytes. The counter correctly reports `selftest_failed`.

NO-DEFECT CHECKS:

- `run_command` env-prefix split (L157-162): `K=V` collected into env only while `argv` is empty; trailing `K=V` stays an arg — matches the documented "leading VAR=value words are part of the documented command". Verified live: `env_pin_removed` selftest case and all 10 rows execute.
- `run_command` cwd=clone, `PYTHONDONTWRITEBYTECODE=1`, stderr merged into stdout: all three tally shapes parsed in the live run — `passedOverTotal` JSON (base_path 45/45, source_recheck 106/106, robots 204/204), `PASS N/N` (sitemap 235/235), `selftest: N/N` lines (redirect 23/23, citation 9/9, c52/c55 counters).
- `parse_tally` JSON branch precedence: `"passedOverTotal"` line `continue`s, so digits elsewhere on the JSON line can't overwrite; later pass/selftest lines still win per the stated "last … line wins" rule.
- `_is_selftest_span` positive path: distinguishes `scripts/redirect_audit.py --manifest PATH` usage from `--selftest` (basename lacks `selftest`, needs the flag) — live redirect row resolved correctly.
- Flat bracket strip: `[--tool PATH]` → `['python3','-B','scripts/robots_audit_selftest.py']` — unit-checked and confirmed live (robots ran with built-in `--tool` default, 204/204).
- `clone_at`: `git clone --no-checkout` of a local path + detached `checkout <rev>` reads committed bytes only, safe with hardlinks, leaves no lane writes — verified by the live run and an independent manual clone.
- `measure` early returns: unreadable SKILL.md → 2; timeout → 2 + partial rows; unparsable tally → 2 + partial rows; `RuntimeError`/`OSError` → 2; `finally` rmtrees the clone — all per the docstring contract; `rows_checked` counts skipped rows (`row_missing`/`command_missing` append before `continue`), verified `rows_checked=10`.
- Blob-vs-BASE_REV (L198): at base all 10 rows show no `tool_changed`; missing blob also maps to `tool_changed` per docstring.
- Exit map: 0 met / 1 not met / 2 unevaluable / 64 usage — observed: measurement EXIT=1, selftest EXIT=0, no `--revision` path returns 64 (L348-350), unresolvable revision returns 2 before `measure` (L351-354).
- `render`/`--json`: row lines, `tally_mismatches`, `rows_checked`, `met`, `EXIT=` all consistent between the two output paths.
- `--selftest`: 20/20 passing (13 cases + 7 unit checks), covers claim_missing, command_missing, selftest_failed, claim_ne_observed, tool_changed, tally_unparsable, row_missing, env prefix, bracket strip, entry-vs-selftest disambiguation.

VERDICT: counter logic is mostly sound — 1 HIGH (yahoo claim regex undercapture) + 5 MED (shlex abort, raw-word script match, nested-bracket strip, permissive tally filter, escaped-pipe split) + minor lows; the 7 base mismatches are stale documented claims, not counter bugs.
