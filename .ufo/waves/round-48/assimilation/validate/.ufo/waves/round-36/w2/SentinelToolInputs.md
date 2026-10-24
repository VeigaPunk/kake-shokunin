# Wave-2 falsify — SentinelToolInputs: large and malformed inputs to `scripts/source_recheck.py`

Target: tool at `4d5b3d550748e5b52af31646b74c1aa435942bde` (wave-1 ExecToolBuild, unedited).
Sandbox clone at `f3a38bf`: `sha256(source_recheck.py)` = `577b2d7d028964e06152f5a7b792141e586045eaa8ec9262ee7f416ba5510d48`,
identical to `git show 4d5b3d5:scripts/source_recheck.py`. Every run: `timeout` ≤ 300 s, ≤ 4 children,
`TMPDIR` in sandbox, `git` vars unset, no host web property touched, no bot challenge attempted.
Fixtures, runners, raw JSON: `/fast/scratch/hyaku/kake-r36w2/SentinelToolInputs/`
(`gen_fixtures.py`, `run_bench{2..7}.py`, `results2..7.json`, `strace_*.txt`).

## Required table — `python3 -B scripts/source_recheck.py --manifest <case>`

| input | wall | exit | valid JSON | verdict / note |
|---|---|---|---|---|
| 20 MB HTML body | 0.20–0.25 s | 0 | yes | `clean`; peak RSS 108 MB |
| 1,000,000 unmatched `<script>` start tags | 0.064 s | 1 | yes | `quote_missing` (whole tail dropped, contract (c)) |
| 1,000,000 `<!--` with no `-->` | 0.057 s | 1 | yes | `quote_missing` (comment runs to EOF, contract (c)) |
| 50 000-hop redirect chain | 0.103 s | 1 | yes | `moved` target `https://example.com/hop49999` + `http_error` |
| body path symlink → outside manifest dir | 0.050 s | 0 | yes | **`clean` — out-of-directory read (F1)** |
| body path is a directory | 0.016 s | 2 | yes | `check_invalid` (correct) |
| body path is a FIFO | 0.016 s | 2 | yes | `check_invalid` (correct: `isfile` is false for FIFO) |
| deeply nested JSON, depth 100 000 | 0.019 s | 2 | yes | `input_invalid` (RecursionError caught) |
| manifest of 100 000 checks | 0.873 s | 0 | yes | `clean`, 100 000 evaluated, 127 MB RSS |
| manifest of 100 000 checks, 2 hops each | 0.589 s | 1 | yes | 200 000 findings, 13.2 MB stdout, 196 MB RSS |

No hang, crash or out-of-tree read in rows 1–4, 6–10. Row 5 is a real out-of-directory read.
All ten rows produced a parseable JSON report; none timed out.

## F1 (high, contract (g)) — symlink body escapes the manifest directory; content oracle
Contract line 1603 ("reads only the manifest and the body files it names") and bullet (g)
("a body path that … escapes the manifest directory … check_invalid"). `body_path` at
`source_recheck.py:393-405` checks `os.path.normpath` prefixes (lexical only) then
`os.path.isfile(candidate)`, which follows symlinks. A symlink *inside* the manifest dir passes
both checks and is read.
- `/fast/scratch/.../fixtures/c5_symlink_outside` — `body.txt` → `../outside_marker.txt`:
  exit 0, `clean`, quote `OUTSIDE_MARKER_9f3a2b` matched ⇒ file outside the directory was read.
- `fixtures5/t_oracle` — `body.txt` → `/etc/passwd`, quote `root:x:0:0`: exit 0, `clean`.
  Negative control (quote absent from `/etc/passwd`): exit 1, `quote_missing`. That is a
  one-bit-per-run content oracle over any file the audit user can read.
- `fixtures/c5b_symlink_dir` — `linkdir/b.txt` with `linkdir` a symlink out: also `clean`.
- `fixtures2/a_symlink_abs` — → `/etc/os-release`, quote `NAME="Arch Linux"`: `clean`.
- `fixtures/t_symlink` under strace: `openat(…/body.txt, O_RDONLY)` succeeds and the read
  returns the outside file's bytes (lot `/fast/scratch/hyaku/kake-r36w2/SentinelToolInputs/strace_passwd.txt:208`).
Impact: the tool's stated read boundary is unenforced; a manifest naming a symlink exfiltrates
any readable file one quote-at-a-time to stdout. The sealed key (revealed `fd1fb723`) has no
symlink case — `make_cases.py` bullet (g) uses `../outside.html` only — so 28/28 does not cover
this. **Smallest remediation:** resolve the real path before the prefix test, then open the
resolved path: `real_root = os.path.realpath(root)`, `real = os.path.realpath(candidate)`, reject
when `real` is not under `real_root`, and open `real` (not `candidate`). The lane has since
landed exactly this at `25f8487` (`source_recheck.py:404-407`); I re-ran the four escape fixtures
against that copy (`repaired_source_recheck.py`, sha256 `3e5457a9…`) and all four return exit 2
`check_invalid`. Note the repair still opens `candidate` after checking `real`, so a symlink
swapped between check and open (TOCTOU) remains possible; opening `real` would close it.

## F2 (medium, contract (g)/(usage)) — FIFO manifest blocks forever
`load_manifest` (`:535-539`) does a plain `open(path,"rb").read()`; a FIFO with no writer blocks
in `openat` indefinitely.
- `fixtures6/fifo/manifest.json` (a FIFO): 60.061 s → killed by harness, exit none, no stdout.
- strace: `openat(AT_FDCWD, "…/fifo/manifest.json", O_RDONLY|O_CLOEXEC) = ? ERESTARTSYS`
  (`strace_fifo.txt:81`), i.e. it is parked in the syscall.
Contract bullet (g) says an unreadable manifest is `input_invalid`; this never returns, so a
caller in a pipeline hangs. Same behaviour on the repaired copy at `25f8487`. Severity is bounded
because the manifest path is operator-supplied, unlike F1's manifest-controlled body path.
Remediation: `os.stat` first and reject non-regular manifests (reuse the `body_path` predicate),
or `open(..., O_NONBLOCK)`.

## F3 (medium, operability) — unbounded slurp: MemoryError traceback instead of a report
Manifest and body are both read whole: `load_manifest` `handle.read()` (`:539`) and
`evaluate_check` `handle.read()` (`:514`). No size cap, no `MAX_BODY` counterpart.
- `--manifest /dev/zero` → exit 1, **no stdout**, stderr ends `MemoryError`.
- 1 GB whitespace-padded manifest, 2 GB address-space cap → exit 1, no stdout, `MemoryError`
  (0.147 s). Uncapped it completes in 0.736 s at 2 062 MB RSS.
- 512 MB body → 0.771 s, 1 548 MB RSS (works, ~3× amplification).
- 8 GiB sparse body via symlink → `MemoryError` on the old tool; the repaired copy rejects it as
  `check_invalid` (realpath), but a large *regular* body inside the dir is still unbounded.
Impact: on a memory-limited runner the tool dies with a traceback and **no JSON on stdout**,
violating "prints one JSON report on stdout"; exit 1 also collides with `failed-policy`.
Remediation: cap manifest and body size (the recorder's own `MAX_BODY = 8 MiB` is the natural
bound), and map the overflow to `input_invalid` / `check_invalid`.

## Clean results (attacked, held)
- HTML parsing is linear, not quadratic: `<a`×N + one `>` and `<!--`×N + one `-->` and
  `<script`×N + one `</script>` are flat from 2 000 to 128 000 tags (0.047–0.053 s); closed-tag
  controls identical. `strip_tags` advances `index` past each `>`, so no rescan.
- Redirect resolution is linear: 1 000→50 000 relative hops 0.015→0.099 s, 200 000 hops 0.352 s,
  29.9 MB RSS. No recursion, no quadratic path growth.
- Per-check work is linear in `checks × body`: one 8 MiB body reused by 1/10/100/400 checks =
  0.11/0.62/5.8/23.3 s. Extrapolated 100 000 checks × 8 MiB ≈ 97 min; a manifest can multiply
  work 100 000× without the manifest itself being large (16 MB manifest). Advisory only — the
  recorder writes one body per check.
- Invalid manifests are handled: UTF-8 BOM, trailing garbage, duplicate `version`, `checks:null`,
  top-level array, `../` body path, absolute body path, NUL in body path, symlink loop, symlink
  to `/dev/null`, `/proc/kcore`, symlink to FIFO, body directory → exit 2 `input_invalid` /
  `check_invalid`. `/dev/stdin` (empty) → `input_invalid`.
- `NaN`/`Infinity` in the manifest are accepted (`r_nan`, `r_inf` → exit 0 `clean` with
  `checks: []`); Python's `json` default. Harmless here, but it means the manifest is not strict
  RFC 8259 JSON.
- No network and no writes: strace `trace=openat,connect,socket,write,unlink,rename,mkdir` on a
  benign run shows only libs, the manifest, the body and one `write(1, …)` of the report
  (`strace_benign.txt:81-83`); no `connect`.

## Not verified
- No adversarial test of the `25f8487` repaired tool beyond the four symlink fixtures and the
  FIFO/MemoryError re-checks; no TOCTOU demonstration (reasoned from code, not run).
- No run under bwrap as `sealed_count.py` does; all runs were direct.
- No test of 32-bit/other-Python behaviour; host Python 3.14.8.
- Tools installed: none (strace and coreutils already present).

Verdict for this surface: two defects worth blocking on at `4d5b3d5` — F1 (contract (g) escape,
content oracle; already repaired in-lane at `25f8487`, but the sealed key never tested it) and
F2/F3 (hang and unbounded slurp on operator-controlled paths, still present at `25f8487`). The
large-input and malformed-input paths themselves are linear and produce valid JSON.
