# ExecCountersTmpScan

Prompt §7.4 scratch-discipline scan of the committed lane tools/counters. Read-only against the
lane (git show / read; no git or jj mutation). Lane HEAD `cb685273cc9e331b51f45485793d5d1c91184b3a`;
base `fd6303ce5c14b3f892dec586297a942ab6e4193b` (`git merge-base --is-ancestor` = true).

Scope actually scanned (`git ls-files`, 150 committed files):
`scripts/*.py`+`scripts/*.mjs` = 27, `.ufo/waves/round-5*/**/*.py` = 123 (round-50..round-59,
incl. the `.files/` and `assimilation/` copies). Pattern per the assignment,
`grep -nE "(/tmp|mkdtemp\(dir=.?/tmp)"`, plus the neighbouring constructors the same rule covers
(`mkdtemp(`, `TemporaryDirectory(`, `gettempdir`, `TMPDIR`, `mos.tmpdir()`).

Semantics used for "honours TMPDIR" (measured on this host, not assumed):
- Python `tempfile.gettempdir()` returns `$TMPDIR` **only when it names an existing writable
  directory**; if `TMPDIR` is unset *or points at a non-existent dir* it silently falls back to
  `/tmp` (`TMPDIR=<missing> python3 -c 'print(tempfile.gettempdir())'` → `/tmp`).
- Node `os.tmpdir()` returns `$TMPDIR` verbatim with **no existence check**; `mkdtempSync` then
  throws `ENOENT` rather than writing to `/tmp` (`TMPDIR=<missing> node -e 'fs.mkdtempSync(...)'`
  → `THREW ENOENT`).
- An explicit `dir=` argument taken from `os.environ.get("TMPDIR")` is honoured literally (no
  existence check), so it either writes where told or fails loudly.

## HITS:

Hardcoded `/tmp` write, TMPDIR and `--work` both ignored:

| site | code | TMPDIR honoured | scratch arg | cleanup | evidence |
|---|---|---|---|---|---|
| `scripts/freshness-sweep.mjs:1193` | `const dir = process.env.KAKE_SELFTEST_DIR \|\| '/tmp/kake-r16/selftest';` | **NO** — only `KAKE_SELFTEST_DIR` overrides; `TMPDIR` is never read for this path | no (`--repo/--json/--offline/--section/--selftest/--help` only, `parseArgs` :147-169) | **none** — the tree is never removed; only the `$HOME` fixture is (`:1226`, `:1658`) | run with `TMPDIR=<scratch>/t HOME=<scratch>/home`: wrote **18 files** under `/tmp/kake-r16/selftest` (`annotated-only/`, `unannotated/`, `loose-window/`, `strict-window/`, `cross-citation-leak/`, `sidecar/`, `pins*.json`, `bad-history.jsonl`, `bad-pins.json`); scratch `TMPDIR` stayed empty; `selftest: 36/36 passed`. Removed the residue myself afterwards. |
| `scripts/freshness-sweep.mjs:1225-1227` | `path.join(os.homedir(), '.kake-freshness-selftest-<pid>')` + `mkdirSync`/`writeFileSync` | **NO** — `$HOME`, not `TMPDIR` | no | yes (`:1658`, verified empty `$HOME` after my run) | same run; second scratch escape in the same function. |

Hardcoded absolute scratch root (not `/tmp`, same defect class — TMPDIR ignored by default):

| site | code | TMPDIR honoured | scratch arg |
|---|---|---|---|
| `scripts/citing_set_selftest.py:158` + `:824-825` | `DEFAULT_TMPDIR = "/fast/scratch/hyaku/kake-r27"`; `Path(DEFAULT_TMPDIR).mkdir(...)`; `tempfile.mkdtemp(prefix=..., dir=DEFAULT_TMPDIR)` | **NO by default** — constant, not env-derived (`DEFAULT_TMPDIR != $TMPDIR`, checked by importing the module) | yes — `--tmpdir` (`:191`); parent dir left in place by design (`:824`) |

Soft hit (writes under `/tmp` only when the env var is absent):

| site | code | behaviour |
|---|---|---|
| `.ufo/waves/round-57/w2/ExecResolverDiff.files/gen_and_diff.py:36` | `"HOME": os.environ.get("HOME", "/tmp")` | child `git` runs get `HOME=/tmp` when `HOME` is unset → any HOME-scoped git write lands in `/tmp` regardless of `TMPDIR`. Committed w2 seat artifact, not a lane counter. |

Conditional `/tmp` fallback (bare `mkdtemp()` — honours `TMPDIR` only while `TMPDIR` exists):

| site | code | behaviour |
|---|---|---|
| `scripts/id_resolver.py:365` | `tempfile.mkdtemp(prefix=SELFTEST_PREFIX)` | measured: `TMPDIR=<existing>` → `<TMPDIR>/idresolver-selftest-*`; `TMPDIR=<missing>` → **`/tmp/idresolver-selftest-wvtjaa3x`** (silent fallback). Ctxmgr `rmtree`s it (`:363-370`), so no residue, but the write escaped the scratch root. No `--work`/`--tmpdir` flag. |
| 34 further committed round-5x `.py` files (of 45 that create temp dirs; the other 11 pass `dir=`) + 11 `scripts/*.{py,mjs}` files (13 sites) | bare `mkdtemp(` / `TemporaryDirectory(` with no `dir=` | same silent `/tmp` fallback when `TMPDIR` is unset or stale. Sites: `scripts/{canonical_audit.py:944, citation_lint.py:196, landed_check.py:233, receipt_replay.py:502,853, redirect_audit.py:475, robots_audit_selftest.py:1347, sitemap_audit_selftest.py:1204,1305, source_recheck_hardening_selftest.py:500,501, source_recheck_selftest.py:923}`; round-5x: `c55_quote_truth.py:566`, `c55_readme_index.py:235`, `c56_quote_truth.py:587`, `c56_selftally.py:202,347,511`, `c57_idresolver_gate.py:107,248,319`, `c57_quote_truth.py:737`, `c57_receipt_pins.py:421`, `c58_quote_truth.py:731`, `derive_c58_quote_truth.py:204`, the six `.ufo/waves/round-4x/c1_count.py:336` copies, and the `w1/`/`w2/` `.files/` copies of each. |

Read-only `/tmp` dependency (records no write, listed because the grep matches it):

| site | code | note |
|---|---|---|
| `scripts/freshness-sweep.mjs:108` (`:879`) | `R15_SNAPSHOT_DEFAULT = '/tmp/kake-r15/charter-live.html'`; `fs.existsSync`/`readFileSync` | read of a hardcoded, already-reaped `/tmp` path (`/tmp/kake-r15` absent on this host). Overridable (`KAKE_R15_SNAPSHOT`); the code itself degrades to `skipped`. Not a write. |

`/tmp` literal that is **not** a host write: `.ufo/waves/round-5*/assimilation/../.ufo/waves/round-41/c1_count.py:245`
(`"--tmpfs", "/tmp"`) is a bubblewrap argument — a tmpfs mounted *inside* the `--unshare-all`
sandbox; the tool's own scratch there is `TemporaryDirectory()` (`:336`), i.e. the bare-mkdtemp class.

## CLEAN:

Honours `TMPDIR` **and** an explicit scratch argument, removes what it creates:

| site | resolution | cleanup | run evidence |
|---|---|---|---|
| `.ufo/waves/round-59/c59_resolver_cases.py:332,334` | `parent = a.work or os.environ.get("TMPDIR") or tempfile.gettempdir()`; `os.makedirs`; `mkdtemp(prefix="c59-rc-", dir=parent)` | `finally shutil.rmtree` (`:338`) | 3 configs at base `fd6303c`: (a) `TMPDIR=<scratch>/t --work <scratch>/w` → `/tmp` count 1206→1206, `w`+`t` empty; (b) `TMPDIR` unset, `--work` given → work removed; (c) `TMPDIR` unset, no `--work` → work removed, no `/tmp/c59-*`. `13/21` at base. |
| `.ufo/waves/round-58/c58_resolver_cases.py:504,505,564,566` (+ its `w1/ExecC2GateSelftest.files` copy) | same `a.work or TMPDIR or gettempdir()` shape | `finally` | static |
| `.ufo/waves/round-58/c58_receipt_rewrites.py:290,310` (+ `w1/ExecC1Perf`, `w1/ExecC1SelftestHarden`, `SimplifierCounters` copies) | `scratch = os.environ.get("TMPDIR") or gettempdir()`; `mkdtemp(dir=scratch)` | `finally` | `TMPDIR=<missing>` → `FileNotFoundError` (fails loud; does **not** fall back to `/tmp`) |

Creates no temp dir and writes nothing:

| file | note |
|---|---|
| `.ufo/waves/round-59/c59_axis_evidence.py` | zero `tempfile`/`mkdtemp`/`/tmp`-write constructs, zero write calls; pure `git show` reader. Ran at base: `mismatches=16 … met=False`, exit 1, no filesystem change. |
| `.ufo/waves/round-59/c59_quote_truth.py:60` | `import tempfile` is **dead** (no call anywhere in the file) — same finding as round 58 for `c58_quote_truth.py`. No writes; ran at base: exit 1, no filesystem change. |
| `.ufo/waves/round-59/span_tools.py` | read-only (`open(..., encoding=...)` on retained bodies). |
| `.ufo/waves/round-59/fetch_sources.py:11,19,22` | writes only into `sys.argv[1]` (caller-chosen directory), refuses to overwrite an existing `receipts.json`. No `/tmp`, no `TMPDIR`. |
| `.ufo/waves/round-59/derive_c59_{quote_truth,resolver_cases}.py` | write only `os.path.join(HERE, "c59_*.py")` — beside themselves in the lane tree. No `/tmp`. |
| `scripts/probe-delta.mjs` | no `fs` write API at all (read-only differ). |
| 13 of 27 `scripts/*.{py,mjs}` | `accessibility_packet`, `base_path_audit`, `base_path_selftest`, `citing_set`, `ledger_latest_check`, `link_preview_audit`, `link_preview_selftest`, `live_snapshot`, `probe-delta.mjs`, `robots_audit`, `sitemap_audit`, `source_recheck`, `source_snapshot` — no temp/`/tmp` construct. |
| 78 of 123 committed round-5x `.py` | no `mkdtemp`/`TemporaryDirectory`/`/tmp` construct. |
| `scripts/citing_set_hostile_selftest.py` | `--tmpdir` is `required=True` (`:240`); no default. |
| `scripts/corpus-contract.mjs:406` | `fs.mkdtempSync(path.join(os.tmpdir(), 'kake-corpus-contract-'))` → honours `TMPDIR`; `TMPDIR=<missing>` throws `ENOENT` (no `/tmp` write); `fs.rmSync` at `:588`; verified `TMPDIR=<scratch>` → 7/7 pass, scratch empty. |

## VERDICT:

Two committed writers ignore both `TMPDIR` and any scratch argument — `scripts/freshness-sweep.mjs`
(`--selftest` fixture root `/tmp/kake-r16/selftest` at :1193, 18 files on a run with `TMPDIR` set,
never removed; plus a `$HOME` fixture at :1225) and `scripts/citing_set_selftest.py` (default
`/fast/scratch/hyaku/kake-r27` at :158, `--tmpdir`-overridable); both are routed defects to record,
not fixed here. The round-59 counters themselves are clean: `c59_axis_evidence.py` writes nothing,
`c59_quote_truth.py` carries only a dead `import tempfile`, and `c59_resolver_cases.py` honours
`--work`→`TMPDIR` and leaves zero `/tmp` residue across the three configurations I ran at base
(`13/21`, exit 1). The remaining 47 temp-creating sites use bare `mkdtemp()`/`TemporaryDirectory()`,
which honours `TMPDIR` only while that directory exists and otherwise falls back to `/tmp` silently —
a latent defect class, evidenced on `scripts/id_resolver.py:365` (`TMPDIR=<missing>` → wrote
`/tmp/idresolver-selftest-…`, cleaned up by its own ctxmgr).
