# ExecTallySitemap

Claim C1 (calibration), row `sitemap-file-audit` (SKILL.md line 1128 at base
`e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`). All work in scratch clones; no lane write except this
report. Clone `D=/tmp/tmp.7G1KuAANCq` (`git clone -q --no-checkout` + `checkout -q e48354b7…`;
`git -C $D rev-parse --show-toplevel` = `$D`, HEAD = `e48354b7…`). Scripts at base:
`scripts/sitemap_audit_selftest.py` sha256 `bebd834bc43d6839…bcda22`,
`scripts/sitemap_audit.py` sha256 `914ebdee7bcb25e8…2cd021`.

## RUNS:

Command (from clone root, exactly as the row documents it):
`python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py`.
No env pin: the selftest documents none and contains no `os.environ` / `getenv` / env-var mention;
imports are stdlib only (`json, os, shutil, subprocess, sys, tempfile`). Outputs went to a private
dir `/tmp/ExecTallySitemap.X6OF6G/` (stdout is a single line, so "last 3 lines" = that one line).

| run | exit | wall | stdout (all of it) | stderr |
|---|---|---|---|---|
| 1 | 0 | 9241 ms | `PASS 235/235` | 0 bytes |
| 2 | 0 | 7759 ms | `PASS 235/235` | 0 bytes |

`diff r1.out r2.out` → identical; sha256 of both = `661d11d13d6efe30…daffdb`.

Corroboration and counter result:

- `python3 -B scripts/sitemap_audit_selftest.py --map` → `case count: 235`, `sentence coverage: 34/34`,
  34 `sentence` lines, 11 `rule` lines, exit 0.
- Frozen counter, this row only (`c56_selftally.measure(..., pop=[sitemap row], expected=1)`):
  `sitemap-file-audit: claim=150 observed=235/235 MISMATCH claim_ne_observed`, `EXIT=1`,
  `tally_mismatches=1 rows_checked=1`.
- Isolated copy (only the two scripts, no `.git`, no `corpus/`, no `SKILL.md`, no `.ufo/`) with a
  private `TMPDIR`: `PASS 235/235`, exit 0, 8531 ms, 0 leftover temp dirs.

## WHAT N COUNTS:

`N = len(build_cases())` = the number of **cases**, and `run_suite` prints `passed/total` with
`total = len(cases)`. Each case is one **fixture directory** materialized under
`tempfile.mkdtemp(prefix="sitemap-audit-case-")` (a manifest plus the files it names) and one
subprocess invocation of the tool under test. Measured decomposition of the 235:

- 235 cases / 235 distinct case names / 235 tool subprocess runs (1 per case).
- 217 fixture payload files across all cases; 231 manifests written; 4 cases have `manifest = None`
  (usage/exit-64 cases); 8 cases override `argv`.
- Not checks, not mutants, not unit checks. `--fault-injection` (not part of the documented command)
  would add 2 × 235 = 470 further runs against a silent tool and a constant-clean tool; the default
  documented run does none. `coverage()` gates sentences 1–34 and both polarities of rules (a)–(k)
  before the run but contributes no count of its own.

Comparison with the row's Self-test cell (`(150 fixtures, all 34 sentences)`): the stated integer
**150 ≠ 235**. History shows why it is stale — the row line was last written by `b56433b` (round-39
C1 verdict) while the suite grew: `56d57ee` "selftest 150 -> 179" (round-40), `133257d` 225
(round-41), `020bc45` 235 (round-42). The prose "all 34 sentences" is still true (`--map`: 34/34,
`missing=[]`, `gaps=[]`).

## HEAD DEPENDENCE:

Files the selftest reads from the clone's HEAD or working tree beyond its own script and its
generated fixtures: **none**.

- Grep over the script for `rev-parse`, `git show`, `HEAD`, `environ`, `__file__`: zero hits. No
  `git` call, no network import.
- All `open(` sites are write-mode: fixture writers `wb` (≈96, ≈103), `materialize` `wb` (≈1102,
  ≈1114), fault-injection tool writer `w` (1309), plus one inside the `CONSTANT_CLEAN_TOOL` string
  literal (1059 — generated source, not this process).
- The only path it consumes is the `--tool` argument (`os.path.abspath`), executed as
  `[sys.executable, "-B", tool] + argv` with `cwd=` the per-case fixture dir; the tool reads only
  the manifest and the files that manifest names inside that dir.
- Byte-proven, not inferred: the isolated copy run above (two scripts only, no repo files at all)
  prints the same `PASS 235/235`, exit 0.

Extra-commit rerun (`D2=/tmp/tmp.TwT02fqSRU`, clone of the lane at base, toplevel verified, one extra
commit `8be3744` made with `git -C "$D2" -c user.name=selftest -c user.email=selftest@local commit`)
touching exactly the named paths: `corpus/SOURCES.md` (+2 lines), `corpus/README.md` (+2 lines),
`corpus/knowledge/probe-selftally.md` (new), `SKILL.md` (+1 extra registry row
`sitemap-file-audit-probe` carrying its own `(999 fixtures)` claim), and `.ufo/waves/round-56/probe.json`
(new — that directory does not exist at base: 0 tracked files). Result: `PASS 235/235`, exit 0,
9965 ms, output byte-identical to the base run.

So a later commit changing `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/`, `SKILL.md`,
or adding files under `.ufo/waves/round-56/` neither changes the tally nor fails the selftest. Two
caveats that are not HEAD reads: (i) the frozen counter's `tool_changed` problem compares the pinned
script's blob at `<rev>` against `BASE_REV`, so a commit that rewrites
`scripts/sitemap_audit_selftest.py` flips this row to a mismatch even at an unchanged tally; (ii) if
the case count changes, the cell integer must be re-derived from the new run.

## REPLACEMENT CELL:

Self-test cell (5th cell of the line 1128 row), exact replacement text — documented command kept
first in backticks, other prose kept, tally stated as the counter reads it:

```
`python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` (235 fixtures, all 34 sentences)
```

Checked in-process against the frozen counter's own functions on the base SKILL.md row:

- `documented_command(cells, "scripts/sitemap_audit_selftest.py")` →
  `['python3','-B','scripts/sitemap_audit_selftest.py','--tool','scripts/sitemap_audit.py']`
  (unchanged; `_is_selftest_span` True via "selftest" in the basename).
- `selftest_cell(...)` returns the whole cell; row regex `\((\d+) fixtures` yields exactly one hit,
  `['235']`; claim sum = **235**; `parse_tally("PASS 235/235")` = `(235, 235)`; claim == observed B →
  `claim_ne_observed` cleared. (The counter's own unit test `parse_pass_line` pins the same literal.)
- No second `(<N> fixtures` occurrence is introduced (those are summed by the counter); "all 34
  sentences" is untouched prose.

## RISKS:

1. 235 is a moving figure (150→179→225→235 across rounds 40–42). Any future case addition re-stales
   the cell with no tolerance in the counter; the cell is a claim about the script's bytes, not
   about HEAD.
2. `tool_changed` fires on any later rewrite of `scripts/sitemap_audit_selftest.py`, independent of
   the cell text — this fix is only valid at the revision whose blob equals `BASE_REV`'s.
3. One case (`_oversized`) materializes a 52,428,800-byte sparse file (`seek(52428800)` + 1 byte).
   Disk-backed TMPDIR is fine; a RAM-backed TMPDIR costs 50 MiB resident. Observed run times 7.8–11.2 s
   on this loaded host against the counter's `TIMEOUT=300`.
4. Shared `/tmp` filenames are unsafe in this fleet: another seat overwrote `/tmp/run1.out` mid-flight
   (a `c55 readme-index selftest: 44/44` line appeared in it after my run). All numbers above come
   from the private dir `/tmp/ExecTallySitemap.X6OF6G/` and from reruns after that collision.
5. Unrun, and reported as unrun: `--fault-injection` (not in the documented command) and the full
   ten-row counter sweep (only this row was measured, via `measure(pop=[row])`).
6. No tool install or upgrade was needed or performed; `pacman` was never invoked (host-wide pause
   respected).

VERDICT: Row claim 150 ≠ observed `PASS 235/235` (exit 0, ~7.8–9.2 s, two identical runs); N counts 235 cases/fixture dirs, the selftest reads nothing from HEAD (proven by an extra-commit clone and a two-script isolated copy), and the replacement cell `(235 fixtures, all 34 sentences)` clears the counter's `\((\d+) fixtures` claim against observed 235.
