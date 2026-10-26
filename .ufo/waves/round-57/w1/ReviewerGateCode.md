# ReviewerGateCode

## FINDINGS:

1. **HIGH — Line 167 / 169 (`evaluate` G4 `RED_REV` run): `--root` is passed as `root`, which need not be named `kake-shokunin`, so the tool does not exclude `kake-shokunin` from sibling owners when evaluated from a scratch clone (`confirmed by running`)**
   - **Line:** 167–170 (`rc, out = run_tool(clone, "--root", root, "--revision", RED_REV, "--fleet", fleet_real)` and `all(RED_OWNER in v[1].split(",") for v in dang.values())`).
   - **Failing input:** Run `c57_idresolver_gate.py --root $D --revision <rev> --fleet /home/vgpnk/Projects/shokunin` where `$D` is a scratch clone `/tmp/test-gate-stub-...` and `scripts/id_resolver.py` implements the contract's sibling-exclusion rule (`every <fleet>/*-shokunin/ other than the lane` by realpath). Because `--root` is `/tmp/test-gate-stub-...` (realpath != `/home/vgpnk/Projects/shokunin/kake-shokunin`), the resolver treats `/home/vgpnk/Projects/shokunin/kake-shokunin` as a sibling, reads its live `HEAD:corpus/SOURCES.md` (which since round 53 contains `S367`, `S372`, `S373`, `S390`, `S409`), and outputs `owners=kake-shokunin,kotodama-shokunin`. Conversely, if G4 checked exact equality `v[1] == RED_OWNER` as the docstring line 34 ("each owned by `kotodama-shokunin`") states, any scratch-clone gate run would wrongly reject a genuine tool; and because line 169 uses `RED_OWNER in v[1].split(",")`, a broken tool that fails to exclude the lane itself (or lists `kake-shokunin,kotodama-shokunin,fake-lane` with `cited-by=fake.md`, `url-match=fake`, `summ=(0, 0, 5, 0, 99)`) passes G4 (`confirmed by running`).
   - **Fix:** Either exclude any sibling directory whose basename matches the target lane name (`kake-shokunin`) when `--root` is a clone of it, or in G4 check `set(v[1].split(",")) <= {RED_OWNER, "kake-shokunin"} and RED_OWNER in v[1].split(",") and v[2] == "-" and summ == (99, 94, 5, 5, 0)`.

2. **MEDIUM — Lines 85–94 (`parse`): Unmatched lines, duplicate `DANGLING` ids, and non-final or multiple `SUMMARY` lines are silently ignored (`confirmed by running`)**
   - **Line:** 85–94 (`for ln in lines: ... dang[m.group(1)] = ... summ = ...`).
   - **Failing input:** A tool that outputs `DANGLING S101 cited-by=wrong owners=wrong url-match=wrong` followed by `DANGLING S101 cited-by=corpus/knowledge/sub/bad.md owners=alpha-shokunin url-match=alpha-shokunin`, arbitrary unrecognized stdout lines (`GARBAGE LINE NOT REJECTED`), two summary lines (`ids_cited=999 ...` then `ids_cited=6 ...`), and a trailing line after the summary (`EXTRA LINE AFTER SUMMARY`). `parse()` overwrites `dang["S101"]` and `summ`, ignores non-matching lines, and does not require the summary line to be `lines[-1]` as required by docstring line 21 ("and a last line `ids_cited=...`"). Tested in a scratch clone: the gate reported `G3_fixture PASS` and `5/5 met=True` (`confirmed by running`).
   - **Fix:** Require `lines` to be non-empty, the last line `lines[-1]` to match `SUMMARY` (and no earlier line to match `SUMMARY`), every preceding line `lines[:-1]` to match `DANGLE` with no duplicate `m.group(1)` keys (returning `({}, None)` on any violation).

3. **MEDIUM — Line 163 (`evaluate` G3 clean-fixture second run): Only `s2[2] == 0` is checked on the clean fixture summary, ignoring `ids_cited=2` and `ids_resolved=2` (`confirmed by running`)**
   - **Line:** 161–164 (`ok = rc2 == 0 and not d2 and s2 is not None and s2[2] == 0`).
   - **Failing input:** A tool that on the clean fixture outputs `ids_cited=0 ids_resolved=0 dangling=0 owned_elsewhere=0 unowned=0` (or `ids_cited=0 ids_resolved=99 dangling=0 owned_elsewhere=5 unowned=5`) and exits 0. Even though `clean/demo-shokunin/corpus/knowledge/good.md` cites `S001` and `S002` (both resolved in `clean/demo-shokunin/corpus/SOURCES.md`), G3 passes with `clean exit=0 summary=(0, 0, 0, 0, 0)` (`confirmed by running`).
   - **Fix:** Replace `s2 is not None and s2[2] == 0` on line 163 with `s2 == (2, 2, 0, 0, 0)`.

4. **MEDIUM — Line 175 (`evaluate` G5 green check): Arithmetic consistency of `summ` is not checked (`confirmed by running`)**
   - **Line:** 175 (`ok = rc == 0 and not dang and summ is not None and summ[2] == 0 and summ[0] >= MIN_CITED`).
   - **Failing input:** A tool that outputs `ids_cited=100 ids_resolved=0 dangling=0 owned_elsewhere=99 unowned=99` (exit 0) for G5. Line 175 checks only `summ[0] >= 100` and `summ[2] == 0`, ignoring `summ[1] == summ[0]`, `summ[3] == 0`, and `summ[4] == 0`. Tested in a scratch clone: `G5_green PASS` with `summary=(100, 0, 0, 99, 99)` (`confirmed by running`).
   - **Fix:** Require `summ[1] == summ[0] and summ[2] == 0 and summ[3] == 0 and summ[4] == 0` (and in general for any `summ`, `summ[0] == summ[1] + summ[2]` and `summ[2] == summ[3] + summ[4]`).

5. **LOW — Lines 167, 173 (`evaluate` G4 and G5): Tool is invoked with `--root <root>` instead of `--root <clone>`**
   - **Line:** 167 (`run_tool(clone, "--root", root, "--revision", RED_REV, "--fleet", fleet_real)`) and 173 (`run_tool(clone, "--root", root, "--revision", rev, "--fleet", fleet_real)`).
   - **Failing input:** A broken tool that ignores `--revision` in G5 and reads `<root>`'s working tree when `<root>` is checked out at `BASE_REV` (or `rev`). Because `BASE_REV`'s working tree already has 0 dangling ids and 104 cited ids (`>= 100`), G5 passes even if the tool reads the working tree on `--revision <rev>` whenever `<rev> != RED_REV`. Conversely, `clone` is a `--no-checkout` clone checked out only at `rev`, and could be mutated or stripped of working-tree `corpus/` files to prove `--revision` uses `git show`.
   - **Fix:** Pass `clone` (after removing `os.path.join(clone, "corpus")` from the working tree once `TOOL` is loaded, or verifying against a bare repo) so `--revision` cannot fall back to working-tree files.

6. **LOW — Line 151 (`evaluate` G2 selftest check): String comparison `m.group(1) == m.group(2)` instead of integer equality (`confirmed by running`)**
   - **Line:** 150–151 (`m = re.fullmatch(r"selftest: (\d+)/(\d+)", out[-1])`, `m.group(1) == m.group(2)`).
   - **Failing input:** `selftest: 016/16` (exit 0). `int(m.group(1)) == int(m.group(2)) == 16`, but `m.group(1) == m.group(2)` is `False`, causing `G2_selftest FAIL` (`confirmed by running`). Also, G2 only inspects `out[-1]` and does not reject non-zero stderr or failure lines before `out[-1]`.
   - **Fix:** Use `int(m.group(1)) == int(m.group(2)) >= MIN_SELFTEST`.

7. **LOW — Lines 146, 177–183 (`evaluate` temp-dir cleanup) and Lines 192–195 (`main` `--help` exit code)**
   - **Line:** 146–183 and 192–195.
   - **Failing input:** (a) If `KeyboardInterrupt` or an unhandled exception (e.g. `UnicodeDecodeError` inside `subprocess.run(..., text=True)` if the tool emits invalid UTF-8 bytes) is raised inside `try`, `tmp` directories (`c57-gate-*`, `c57-fixture-*`, `c57-fixture-clean-*`) are leaked because cleanup is duplicated in `except (RuntimeError, subprocess.TimeoutExpired, OSError):` and post-`try` instead of a `finally:` block, and `sandbox_clone` (line 146) runs outside `try`. (b) Running `c57_idresolver_gate.py --help` raises `SystemExit(0)` inside `ap.parse_args()`, which `except SystemExit: return 64` turns into exit code `64` instead of `0` (`confirmed by running`).
   - **Fix:** Wrap `try ... finally:` around `tmp` cleanup, pass `errors="replace"` to `subprocess.run` in `run_tool`, and in `main()` catch `except SystemExit as e: return 0 if e.code == 0 else 64`.

## FIXTURE ARITHMETIC:

Recount of `build_fixture()` (lines 97–126) vs `EXPECT_FIXTURE` (lines 129–134) and `EXPECT_SUMMARY` (line 135) — **consistent** (`confirmed by running`):
- **Lane registry (`demo-shokunin/corpus/SOURCES.md`, lines 109–111):**
  - `| S001 | t — https://e.example/1 | ...` (0 leading spaces) -> resolves `S001`.
  - `  | S002 | t — https://e.example/2 | ...` (2 leading spaces, within 0..3 rule) -> resolves `S002`.
  - Total lane registry ids: `2` (`S001`, `S002`).
- **Sibling registries (lines 112–113):**
  - `alpha-shokunin/corpus/SOURCES.md` (0 leading spaces): `S101` (`https://a.example/101`), `S200` (`https://a.example/200`), `S0300` (`https://a.example/300`).
  - `beta-shokunin/corpus/SOURCES.md` (3 leading spaces, within 0..3 rule): `S200` (`https://b.example/200`).
- **Knowledge citations (`demo-shokunin/corpus/knowledge/**/*.md`, lines 115–120):**
  - `corpus/knowledge/good.md`: cites `S001` (twice) and `S002` (once) -> distinct cited in `good.md`: `{S001, S002}`.
  - `corpus/knowledge/sub/bad.md`: cites `S101` (twice, and quotes `https://a.example/101`), `S200` (once), `S777` (once), `S0300` (once). Decoys in `bad.md`: `S12` (only 2 digits, fails `\bS\d{3,}\b`), `AS500` (leading `A`, fails word boundary), `S500x` (trailing `x`, fails word boundary), `s101` (lowercase `s`, fails case-sensitive `S`).
- **Totals (`EXPECT_SUMMARY = (6, 2, 4, 3, 1)`):**
  - `ids_cited`: `6` (`S001`, `S002`, `S101`, `S200`, `S0300`, `S777`).
  - `ids_resolved`: `2` (`S001`, `S002`).
  - `dangling`: `4` (`S0300`, `S101`, `S200`, `S777`).
  - `owned_elsewhere`: `3`:
    - `S101`: cited-by `corpus/knowledge/sub/bad.md`, owners `alpha-shokunin`, url-match `alpha-shokunin` (`https://a.example/101` is in `bad.md`).
    - `S200`: cited-by `corpus/knowledge/sub/bad.md`, owners `alpha-shokunin,beta-shokunin`, url-match `-` (neither `https://a.example/200` nor `https://b.example/200` is in `bad.md`).
    - `S0300`: cited-by `corpus/knowledge/sub/bad.md`, owners `alpha-shokunin`, url-match `-` (`https://a.example/300` is not in `bad.md`).
  - `unowned`: `1`:
    - `S777`: cited-by `corpus/knowledge/sub/bad.md`, owners `-`, url-match `-`.
- **Clean fixture (`clean`, lines 121–126):**
  - Copies `alpha-shokunin`, `beta-shokunin`, and `demo-shokunin` into `clean`, then removes `clean/demo-shokunin/corpus/knowledge/sub/bad.md`.
  - Remaining knowledge file `good.md` cites only `S001` and `S002` (both resolved): `ids_cited=2 ids_resolved=2 dangling=0 owned_elsewhere=0 unowned=0`, exit `0`.

## NO-DEFECT CHECKS:

- `sandbox_clone` (lines 68–75): Clones `--no-checkout` into a `c57-gate-*` temp dir and runs detached `checkout -q <rev>`; cleans up `d` and raises `RuntimeError` if either `git` call fails (`confirmed by running`).
- `run_tool` (lines 78–82): Executes `[sys.executable, "-B", os.path.join(clone, TOOL), *args]` with `cwd=clone`, `timeout=300`, minimal `env={"PATH": ..., "HOME": ..., "LC_ALL": "C.UTF-8"}`, and parses `p.stdout` only (`confirmed by running`).
- `DANGLE` and `SUMMARY` regexes (lines 60–61): Match the exact contract line formats (`DANGLING S\d{3,} cited-by=\S+ owners=\S+ url-match=\S+` and `ids_cited=\d+ ids_resolved=\d+ dangling=\d+ owned_elsewhere=\d+ unowned=\d+`).
- `RED_REV` and `RED_IDS` (lines 54–56): `3994101dba28896830604fd0b08c7f00faca8ed6` is the round-52 verifier spot-check commit; at that revision `corpus/SOURCES.md` has 148 rows, `corpus/knowledge/**/*.md` cites 99 distinct ids, 94 resolve, and the 5 dangling ids are `['S367', 'S372', 'S373', 'S390', 'S409']`, each held by `kotodama-shokunin` (`confirmed by running`).
- `G5` threshold `MIN_CITED = 100` (line 59): At `BASE_REV` (`28fa0b23e699...`), `corpus/knowledge/**/*.md` cites 104 distinct ids (all 104 resolved in the 158-row registry), and after C3 adds `S421`/`S422` it will cite 106 >= 100 (`confirmed by running`).
- Exit codes and `--fleet` option (lines 187–215): Missing `--revision` or bad args return `64`; unresolved `--revision` or `RuntimeError`/`TimeoutExpired`/`OSError` returns `2`; `--fleet` defaults to `os.path.dirname(root)` and overrides `fleet_real` when passed (`confirmed by running`).

VERDICT: Fixture arithmetic (6 cited, 2 resolved, 4 dangling, 3 owned elsewhere, 1 unowned) and base/stub runs confirmed; 7 logic/validation findings in `c57_idresolver_gate.py` (G4 `--root` sibling self-inclusion in scratch clones, permissive `parse()`, unchecked clean-fixture and G5 summary invariants, G4/G5 `--root` vs `clone`, G2 string equality, and `finally`/`--help` handling).
