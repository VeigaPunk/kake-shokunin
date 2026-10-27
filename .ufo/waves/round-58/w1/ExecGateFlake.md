# ExecGateFlake

Seat: C2 stability (flake gate). Claim C2, predicate `met: cases_passed == 12 of 12`. Counter measured:
`.ufo/waves/round-58/c58_resolver_cases.py` sha256 `60c814aac4c20fd4ef2a30968a5d8f56dbb019db46435e739d4a68b1034837c5`
— byte-identical at base `04404…`, contract commit `fff3eea…`, HEAD `cc8da16…` and the worktree, so this measurement is on frozen counter version 1 and no sibling edit is in play.
Host: 32 cores, load avg ~16 during the window; every run is a single `python3 -B … --root <lane> --revision 044048597d62f3199494b63b36e90dd57825e350 --work /fast/scratch/hyaku/kake-r58/ExecGateFlake/w`.

## RUNS:

Five consecutive runs, same `--work` dir, wall time from `date +%s.%N` around each invocation:

| run | tally (first line) | EXIT | wall |
|---|---|---|---|
| 1 | `C2 resolver-cases 7/12 met=False  (met: cases_passed == 12 of 12)` | 1 | 0.68 s |
| 2 | same | 1 | 0.66 s |
| 3 | same | 1 | 0.66 s |
| 4 | same | 1 | 0.64 s |
| 5 | same | 1 | 0.72 s |

- Tally is 7/12 in all five runs (the frozen base expectation from the do-nothing control, not the after-target 12/12 — the lane tool at base still carries D1/F1).
- Failing set is identical in all five: `K1_fenced_heading_before_registry`, `K2_backtick_fence_inside_registry`, `K3_tilde_fence_inside_registry`, `K4_non_ascii_path_at_revision`, `K5_git_quoted_path_at_revision`; passing set identical: `P1`–`P7`, including `P6_tool_selftest 49/49` and `P7_real_lane_green ids_cited=106 ids_resolved=106 dangling=0`.
- Determinism check: after normalising only the two run-varying paths (`c58-rc-<tmp>` mkdtemp suffix and the `--work` prefix, both appearing solely in P5's `unevaluable: fleet root …` note) all five outputs hash to the same value (`sha256[:12] = c7d04bfd356d`). Raw file hashes differ only through those temp names.
- Cross-check against the committed control: `controls/base-c2-resolver-cases.txt` at `fff3eea` is line-for-line identical to my run apart from its own `/fast/scratch/hyaku/kake-r58/l1/<tmp>` work path. Receipt vs. re-run agreement, 1 of 1.
- Extra flake channels (each exit 1, 7/12, byte-identical after normalisation): hostile `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` pointing at the lane (0.68 s — the counter's `env()` strips every `GIT_*` key); `HOME` redirected to an empty dir + `GIT_CONFIG_GLOBAL=/dev/null` (0.66 s — host git config not a factor); `cwd=/` (0.66 s — no cwd dependence); `TMPDIR`-only, no `--work` (0.65 s); two simultaneous runs sharing one `--work` dir (`par-a`/`par-b`, both 7/12 — `mkdtemp` keeps fixture trees disjoint).

## LOCALE:

- `LC_ALL=C LANG=C` → 7/12, EXIT=1, 0.74 s.
- `LC_ALL=C.UTF-8 LANG=C.UTF-8` → 7/12, EXIT=1, 0.76 s.
- `LC_ALL=ja_JP.UTF-8 LANG=ja_JP.UTF-8` → 7/12, EXIT=1, 0.69 s.
- All three outputs are byte-identical to the default-env run after path normalisation (same `c7d04bfd356d` hash), including the K4/K5 lines: `K4 … FAIL exit=0 ids_cited=1 …`, `K5 … FAIL exit=0 ids_cited=1 …`. Neither the tally nor any case note changes with locale.
- Caveat on the ja run: **`ja_JP.UTF-8` is not generated on this host** (`locale -a` lists 4 locales, no `ja*`); `locale.setlocale(LC_ALL,'')` raises `unsupported locale setting`, so glibc stays in the C locale. Python still reports `fsenc=utf-8 utf8_mode=1` under that env (auto UTF-8 mode for a failed/C locale), so the run exercises "unsupported locale" rather than a live Japanese locale. A host with a real ja_JP.UTF-8 would behave the same way for the reasons below.
- Why K4 is locale-stable, measured: the counter builds its child env in `env()` as `{all os.environ except GIT_*} + LC_ALL=C.UTF-8 + PYTHONDONTWRITEBYTECODE=1`, so every `git` and every `id_resolver.py` child gets C.UTF-8 regardless of the parent locale; all `git` output is decoded explicitly `.decode("utf-8","replace")`. Parent-locale influence is thus limited to the counter's own filesystem encoding, measured `utf-8` in all three locales (`LC_ALL=C` also forces Python's UTF-8 mode, `PYTHONCOERCECLOCALE=0` included). `core.quotepath` is unset (git default true) and is locale-independent.
- Fixture-level probe (labrat, counter imported as a library in scratch, both locales): the K4 fixture commits a real `corpus/knowledge/中文.md` and `git ls-tree -r --name-only HEAD` prints the quoted form `"corpus/knowledge/\344\270\255\346\226\207.md"` in *both* `LC_ALL=C` and `LC_ALL=ja_JP.UTF-8`, with `status --porcelain` empty and `rev-parse --show-toplevel` equal to the fixture dir; K5 likewise commits `a"b.md`, quoted as `"corpus/knowledge/a\"b.md"`. The non-ASCII/git-quoted fixtures are materialised identically, so the K4/K5 inputs are not locale-dependent — only the tool's path handling decides their verdict.
- Residual channel (measured, latent, not a present flake): `env()` forwards `PYTHONIOENCODING` unchanged to children (verified: child env `PYTHONIOENCODING='ascii'`, `LC_ALL='C.UTF-8'`, `PYTHONUTF8` unset), and a child under that env dies with `UnicodeEncodeError: 'ascii' codec can't encode characters` when it prints CJK. A full `PYTHONIOENCODING=ascii` run still yields identical 7/12 because the base tool never prints a CJK path; once a fixed tool prints `cited-by=corpus/knowledge/中文.md`, an ASCII-IO caller would flip K4 rather than fail it cleanly. Worth one line in the counter's hardening note.

## EVIDENCE:

Receipts (18 files, 76 KB) at `.ufo/waves/round-58/w1/ExecGateFlake.files/`: `run{1..5}.out`, `loc-{c,ce,ja}.out`,
`env-{hostile_gitdir,empty_home,cwd_root,tmpdir_only,ioenc_ascii}.out`, `par-{a,b}.out`, `probe-{c,ja}.out` (fixture-identity probe JSON +
its source `k4probe.py`), `base-control.txt` (committed control extracted read-only for the diff). No lane mutation: read-only `git show/log/rev-parse/status`
only, no `git add/commit/stash/checkout/reset/pull/push`, no jj action. Scratch `/fast/scratch/hyaku/kake-r58/ExecGateFlake` deleted after copying receipts.
Files changed by me: this report and `ExecGateFlake.files/` only.

## RISKS:

- K4's *pass* path is unmeasured: at base K4 fails for a non-locale reason (the tool drops the path, `ids_cited=1`), so locale-independence is evidenced on the failing path plus the forced-child-env mechanism and the fixture probe. Re-running the same locale sweep against the fixed tip is the one gap the L1 should close after C2 lands. [INFERENCE] it will hold, since both the counter and its children are pinned to UTF-8 encodings.
- Wall times are single-shot on a load-16 host; treat 0.63–0.76 s as the observed band, not a benchmark.
- `LC_ALL=C.UTF-8` is hard-coded in `env()`; on a host without a generated `C.UTF-8` (musl/Alpine) that falls back to C and the guarantees above rest on Python's UTF-8 mode instead. Not exercised here.
- The counter's fixtures inherit host git configuration beyond `commit.gpgsign=false`; the empty-HOME run showed no dependence today, but a global `core.hooksPath` would still run hooks inside fixtures. [INFERENCE], untested since this host has none.

VERDICT: C2 counter is stable — 5/5 runs at exactly 7/12 (exit 1, 0.64–0.72 s) with byte-identical per-case output, reproduced against the committed base control, and unchanged under LC_ALL=C, LC_ALL=C.UTF-8 and LANG=ja_JP.UTF-8; K4's non-ASCII fixture is locale-independent, with the fixed-tool pass path left as the one follow-up.
