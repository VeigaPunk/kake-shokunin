# ExecCountersTmpScan

Scope: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/*.py` (7 files) and
`/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/*.py` (31 files), grepped for `/tmp`,
`mkdtemp(`, `tempfile.gettempdir`, `TemporaryDirectory(`. Static read only for `scripts/`;
the three round-58 counters were also executed. No file in the lane was modified.

## SCAN:

Semantics used: `tempfile.mkdtemp()` / `TemporaryDirectory()` **without `dir=`** resolve through
`tempfile.gettempdir()`, which consults `TMPDIR` first — so `TMPDIR` IS honoured, but the tool
accepts no explicit scratch argument. `dir=<path derived from TMPDIR>` honours it explicitly.

Round-58 wave files (executable temp usage):

| site | pattern | TMPDIR honoured | explicit scratch arg | cleanup |
|---|---|---|---|---|
| `.ufo/waves/round-58/c58_receipt_rewrites.py:246` | `mkdtemp(prefix="c58-rr-", dir=scratch)` | yes — `scratch = os.environ.get("TMPDIR") or tempfile.gettempdir()` (:266) | **NO** (no `--work`/`--tmpdir`; only `--root --revision --selftest --json --list`) | selftest `finally` rmtree |
| `.ufo/waves/round-58/c58_resolver_cases.py:215` | `mkdtemp(prefix="c58-rc-", dir=parent)` | yes — `parent = a.work or os.environ.get("TMPDIR") or tempfile.gettempdir()` (:213) | yes — `--work` (:200) | `finally shutil.rmtree` |
| `.ufo/waves/round-58/c58_quote_truth.py:56` | `import tempfile` — **unused, no tempfile call anywhere** | n/a (creates no scratch) | n/a | n/a |

No other temp usage in `c58_quote_truth.py`, `derive_c58_quote_truth.py`, `fetch_sources.py`,
`span_tools.py`. `make_spec_w1.py:33,290-293` contain the literal strings `/tmp` and the pattern
names only as seat-spec instruction text (generated job cards), not as executable paths.

`scripts/` hits (all call sites are selftest/self-check scratch):

| site | pattern | TMPDIR honoured | explicit scratch arg | cleanup |
|---|---|---|---|---|
| `scripts/canonical_audit.py:944` | `TemporaryDirectory(prefix="canonical-audit-selftest-")` | yes (implicit; no `dir=`) | no | context manager |
| `scripts/citation_lint.py:196` | `TemporaryDirectory(prefix="kake-r46-citelint-")` | yes (implicit) | no | context manager |
| `scripts/citing_set_selftest.py:825` | `mkdtemp(prefix="citing-set-selftest-", dir=DEFAULT_TMPDIR)` | **NO by default** — `DEFAULT_TMPDIR = "/fast/scratch/hyaku/kake-r27"` (:158), hardcoded; `TMPDIR` env ignored | yes — `--tmpdir` (:191) | rmtree in `finally` |
| `scripts/citing_set_selftest.py:824` | `Path(DEFAULT_TMPDIR).mkdir(...)` | no (same hardcoded root) | as above | left in place by design |
| `scripts/id_resolver.py:330` | `mkdtemp(prefix=SELFTEST_PREFIX)` (`SELFTEST_PREFIX="idresolver-selftest-"`, :47) | yes (implicit; no `dir=`) | no (`--root --revision --fleet --selftest` only) | `_tmpdir` ctxmgr rmtree (:333) |
| `scripts/landed_check.py:233` | `mkdtemp(prefix="landed-check-")` | yes (implicit) | no | rmtree at :426 |
| `scripts/receipt_replay.py:502` | `TemporaryDirectory(prefix="receipt-replay-c2-")` | yes (implicit) | no | context manager |
| `scripts/receipt_replay.py:853` | `TemporaryDirectory(prefix="receipt-replay-selftest-")` | yes (implicit) | no | context manager |
| `scripts/redirect_audit.py:475` | `TemporaryDirectory(prefix="kake-r46-redirect-")` | yes (implicit) | no | context manager |
| `scripts/robots_audit_selftest.py:1347` | `Path(mkdtemp(prefix="kake-r37-robots-selftest-"))` | yes (implicit) | no | `cleanup(work)` in `finally` |
| `scripts/sitemap_audit_selftest.py:1204` | `mkdtemp(prefix="sitemap-audit-case-")` | yes (implicit) | no | rmtree unless `keep_root` |
| `scripts/sitemap_audit_selftest.py:1305` | `TemporaryDirectory(prefix="sitemap-audit-faults-")` | yes (implicit) | no | context manager |
| `scripts/source_recheck_hardening_selftest.py:500` | `Path(mkdtemp(prefix="kake-r37-hardening-"))` | yes (implicit) | no | rmtree in `finally` |
| `scripts/source_recheck_hardening_selftest.py:501` | `Path(mkdtemp(prefix="kake-r37-hardening-traces-"))` | yes (implicit) | no | rmtree in `finally` |
| `scripts/source_recheck_selftest.py:923` | `Path(mkdtemp(prefix="kake-r36-selftest-"))` | yes (implicit) | no | rmtree in `finally` |

Counts: 10 `mkdtemp(` sites (3 with `dir=`: both round-58 counters + citing_set), 6
`TemporaryDirectory(` sites (0 with `dir=`), 2 explicit `gettempdir()` call sites (both round-58
counters, both as a fallback after `TMPDIR`). No executable hardcoded `/tmp` literal anywhere.

Empirical probe of the C1 counter's real fixture creator under `TMPDIR` (imported module, spied on
`tempfile.mkdtemp`, one `_repo()` call, dir removed):
```
RESOLVED_SCRATCH /fast/scratch/hyaku/kake-r58/ExecCountersTmpScan/t
CREATED /fast/scratch/hyaku/kake-r58/ExecCountersTmpScan/t/c58-rr-llwm16p_
MKDTEMP_ARGS () {'prefix': 'c58-rr-', 'dir': '/fast/scratch/hyaku/kake-r58/ExecCountersTmpScan/t'}
CLEANED True
```

## RUNS:

All three counters run once each at base `044048597d62f3199494b63b36e90dd57825e350`
(`--root .` inside the lane, `git merge-base --is-ancestor <base> HEAD` = true; lane HEAD `cc8da16`),
`TMPDIR=/fast/scratch/hyaku/kake-r58/ExecCountersTmpScan/t`. Raw output: `ExecCountersTmpScan.files/c1.out|c2.out|c3.out`.

1. `c58_receipt_rewrites.py --root . --revision 0440485…` → **EXIT=1**
   `C1 receipt-rewrites events=19 undisclosed=19 phantom=0 malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=0 met=False`
   `ledger: .ufo/waves/round-58/receipt-rewrites.json absent (0 entries)` → base 19 undisclosed reproduced.
   (Main/measure mode creates no temp dirs; only `--selftest` does.)
2. `c58_resolver_cases.py --root . --revision 0440485…` → **EXIT=1**
   `C2 resolver-cases 7/12 met=False`; FAIL K1_fenced_heading_before_registry, K2_backtick_fence_inside_registry,
   K3_tilde_fence_inside_registry, K4_non_ascii_path_at_revision, K5_git_quoted_path_at_revision (all `exit=0`
   false greens); PASS P1–P7. Its work dir materialised at
   `/fast/scratch/hyaku/kake-r58/ExecCountersTmpScan/t/c58-rc-tyhyda82/…` (visible in the P5 line) → `TMPDIR`
   honoured; base 7/12 reproduced.
3. `c58_quote_truth.py --root . --revision 0440485…` → **EXIT=1**
   C1_entries_exist, C2_entry_provenance, C3_row_shape, C4_used_by, C5_quote_truth, C6_receipt_pins,
   C7_validate_before_append, C8_mirror_bytes all FAIL (S423/S424 entry, row, retained body, receipt and
   pre-append mirror absent at base) → base 0/8 reproduced.

## LEFTOVERS:

- Before: `ls -1 /tmp | wc -l` = **930**; `find /tmp -maxdepth 1 \( -name 'c58-*' -o -name 'idresolver-*' \)` = **0**.
- After: `ls -1 /tmp | wc -l` = **932**; same prefix find = **0**.
  The +2 drift is unrelated concurrent seats' names (`claude-tool-count-sess_…`, `ecc-metrics-sess_…`,
  `nw-gate2.err`, `gate-frozen-old.json`, `tmpucdh0lry`, all by mtime within the run window); no
  `c58-*` or `idresolver-*` entry ever appeared.
- `/fast/scratch/hyaku/kake-r58/ExecCountersTmpScan/t` after all three runs: `.` and `..` only → every
  counter removed its work dir (`c58-rc-*` via `finally shutil.rmtree`, `c58-rr-*` probe removed; C3 creates none).
- Scratch dir deleted at seat end (receipts copied into `ExecCountersTmpScan.files/`). Lane `git status`
  unchanged apart from the orchestrator's untracked `w1/`, `w1.ready`, `w1.ready.partial`; no lane
  file other than this report and `.files/` written, no git/jj mutation.

Risks / unrun:
- §7.4 gap, advisory only: the C1 counter (`c58_receipt_rewrites.py`) honours `TMPDIR` but accepts **no**
  explicit scratch argument, unlike C2's `--work`. With `TMPDIR` unset it would fall to the system default
  (`/tmp` on this host) — not observed here because `TMPDIR` was set.
- `scripts/citing_set_selftest.py` ignores `TMPDIR` by default (hardcoded `/fast/scratch/hyaku/kake-r27`);
  `--tmpdir` is the only override. Pre-existing, outside round-58 counter scope.
- `c58_quote_truth.py` carries an unused `import tempfile` (dead weight, no behaviour).
- `scripts/*` findings are static-read only — none of those selftests was executed in this seat (not requested).

VERDICT: Both round-58 counters honour TMPDIR with zero /tmp residue (C1 additionally lacks a scratch argument; citing_set_selftest ignores TMPDIR by default), and the three counters reproduce the base readings 19 undisclosed / 7-of-12 / 0-of-8.
