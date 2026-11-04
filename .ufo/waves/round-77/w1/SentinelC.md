# SentinelC — round 77, wave w1 (security review of the new code paths)

Seat: leaf sentinel, kake lane round 77 w1 attempt 1. Lane checkout read-only; every experiment ran in
`S=/fast/scratch/hyaku/kake-r77/SentinelC` with `TMPDIR=$S/tmp`, every child under `RLIMIT_AS` (600 MB default,
700–900 MB for the 52 MB fixtures) and `RLIMIT_CPU` 60 s, and every `--work` an explicit path under `$S`. No
tool was installed or upgraded. No model was named. No network was used. No file outside `$S` was written
except this report.

**Closing instant: 2026-11-03 22:57 -0300.** The wave was in flight throughout: `scripts/sitemap_audit.py`
was rewritten six times, the ledger three, the matrix three — and one build was declared final, replaced, and
replaced again within nine minutes. Every number below is tied to the sha256 it was measured on. **If the
closing hash of any surface differs from the table, the receipt must be re-cut against the new bytes; nothing
here transfers to another hash.**

## 0. Bytes reviewed (sha256), and what moved

| Surface | closing sha256 (bytes) | mtime | state at close |
|---|---|---|---|
| `scripts/sitemap_audit.py` | `f767af770652437d7af18c693dff7cafd64d7f79c38cec36a20e6c4e0bbe9176` (32,325) | 22:56:28 | **closing**; third "final" of the round (superseded `16ea784f…` and `742c2ab1…`) |
| `scripts/sitemap_audit_selftest.py` | `f22e0a67d777ce80ce2d1099520f50f98016c28901e77b7cb5e4b73c386b9c89` (81,651) | 22:56:42 | closing; `PASS 271/271`, exit 0, empty stderr |
| `.ufo/waves/round-77/c77_sitemap_matrix.py` | `5c6eacba266068845144ba59c8e7099cc22fee10ca95c0ab78019ba33d21afce` (29,677) | 22:49:41 | stable since 22:49; `selftest 14/14`; 20/20 correct on the closing tool |
| `.ufo/waves/round-77/c77_shonen_ledger.py` | `00cb4fb2dccc01268a21666ff58d94c636ff49313870c52d798a1bb74c63bd50` (48,225) | 22:56:50 | **closing** (v2); `selftest 26/26` |
| `.ufo/waves/round-77/amendment-1.md`, `amendment-2.md` | — | 22:44 | the terms under which the ids and the C1 check vocabulary changed (§5) |

Builds measured on the way: `914ebdee…` base, `dc97e2d6…`, `f4fbdcb9…`, `29e2f2fa…`, `16ea784f…`, `742c2ab1…`,
`f767af77…` closing; ledger `a9eef8bd…` → `9612baac…` → `00cb4fb2…`. Every finding below states the build it
was reproduced on and the build where it closed, because four of them did close inside the wave.

---

## 1. Findings

### F1 — **High — closed** (live at `a9eef8bd…`, closed at `9612baac…`; still closed at `00cb4fb2…`) — a ledger row's `argv` was executed verbatim

- **Exploit path (build `a9eef8bd…`, 22:46:28).** `corpus/knowledge/shonen-ledger.json` is the object C1
  measures. A row of kind `command` carried an `argv` list; the counter substituted `{root}/{rev}/{work}` into
  each element and ran `subprocess.run(argv, cwd=root, ...)`. No shell (good), but nothing constrained the
  program: a committer of the ledger got arbitrary code execution as the user running the frozen C1 command,
  with `cwd` = `--root` (the lane) and the environment inherited except `GIT_*`; only `HOME`/`TMPDIR` were
  redirected. The counter printed its normal line and exited 0 — the execution was silent.
- **The pin was decorative.** When `program` was present the counter checked that the worktree file's sha256
  equalled the committed blob's, then ran `argv`, not `program`. `argv: ["/bin/sh","-c",…]` with a valid
  `program` still ran `/bin/sh`.
- **Evidence** (git-plumbing fixtures under `$S`, counter run with `--git-dir <fixture>/repo.git --revision <tree>`):
  ```
  a9eef8bd, unpinned row:  exit 0 | C1 revision=4962cba0… boxes=4 evidenced=0 gap=4 unexamined=0 mismatches=0 met=true
                           CANARY EXISTS: True 'executed'
  a9eef8bd, pinned row:    exit 0 | C1 revision=b8c26b5a… boxes=4 evidenced=0 gap=4 unexamined=0 mismatches=0 met=true
                           CANARY EXISTS: True 'pinned-bypass'
  ```
- **Impact while open.** Code execution from audited bytes, in the verifier, at L1 privileges; a relative-path
  write landed in the lane (`cwd=root`); env-borne secrets were readable by the payload. Amendment 2 A2 says
  "checks are declarations, never executable" and A5 requires a `command` fixture to stay red — that build was
  both executing and reporting `met=true` on my fixture, a violation of the amendment it was written under.
- **Closure verified.** `9612baac…` rejected `kind == "command"` in the schema
  (`… is an executable check; the counter runs no ledger-supplied command`); `00cb4fb2…` (v2) instead reports
  `check '<id>' kind 'command' is outside the frozen vocabulary`. Same two fixtures on the closing bytes:
  ```
  exit 1 | C1 revision=… boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=0 met=false
  CANARY EXISTS: False        (both fixtures; stderr names each rejected check)
  ```
  `--selftest` 26/26 passed on `00cb4fb2…`; the closing file has **no** `_run_command` and no ledger-supplied
  argv path — the only `subprocess` calls are git plumbing and its own fixtures
  (`c77_shonen_ledger.py:109,159-160,693-711,1050`).
- **Residual (small).** Keep it that way: a schema gate is what holds the line now, so a future widening of
  the vocabulary re-opens execution unless a test blocks it. The 26-case selftest is that test.

### F2 — **Medium — closed at `f767af77…`** (open through `742c2ab1…`) — manifest containment was lexical: a symlink escaped it, and the finding set was a file oracle

- **Exploit path (builds to `742c2ab1…`).** `_file_value_invalid` rejected a leading `/` and any `..` segment,
  and the audit path was `os.path.join(base_dir, file_value)` with no resolution. A manifest directory
  containing `escape.xml -> ../outside/target.xml` was read as the named file.
- **Evidence** (`742c2ab1…`): manifest `{"file":"escape.xml"}` → exit 0 `clean` for a document outside the
  manifest directory; pointing it at a 5-line out-of-tree file → exit 1 with five `text_line_not_url`
  findings, entries 1–5 — one finding per line of a file outside the tree, i.e. a line-structure oracle
  (line count and line shape, never the bytes), bounded at 52,428,801 B per file.
- **Impact while open.** A hostile tree fed to the verifier made it read any file the process could read and
  exposed structural facts about it. No content exfiltration, no write.
- **Closure verified** (`f767af77…`): `_resolves_inside` (`sitemap_audit.py:789-798`) compares
  `os.path.realpath` of the target against `os.path.realpath(base_dir) + os.sep`, and `_evaluate_check`
  rejects a non-contained target as `check_invalid` (`:825`):
  ```
  fx/escape-out.xml      -> ../outside2/target.xml   exit 2  check_invalid
  fx/read-out-lines.txt  -> ../outside2/lines.txt    exit 2  check_invalid
  ```
  (A symlink whose target is *inside* the manifest directory is still followed, by design — my earlier
  "escape" fixture pointed at `fx/outside/…`, inside the tree, and correctly stayed clean; the honest
  out-of-tree fixtures above are the discriminating ones.)
- **Residual.** `realpath`-then-open is TOCTOU-racy in principle (an attacker with write access to the tree
  could swap between check and open); for a single-user offline audit that is acceptable, and `O_NOFOLLOW`
  on the final component would close it if the lane wants it.

### F3 — **Medium — closed at `f767af77…`** (open through `742c2ab1…`) — a FIFO or device named by a manifest blocked the audit indefinitely

- **Exploit path (builds to `742c2ab1…`).** `_load_payload` used plain `open(path, "rb")`; `open()` on a FIFO
  with no writer blocks forever, and a symlink made any FIFO or device reachable under a permitted name.
- **Evidence** (`742c2ab1…`): `mkfifo fx/fifo.xml`, manifest names it → `timeout 5 …` returns rc 124 with zero
  bytes of output, zero stderr; the runner records `TIMEOUT`. The matrix and the C1 counter cap a child at
  300 s, so the instrument-level observable was a five-minute stall per case.
- **Closure verified** (`f767af77…`): `_open_regular` (`sitemap_audit.py:441-459`) opens with
  `O_RDONLY | O_NONBLOCK`, requires `S_ISREG(os.fstat(...).st_mode)`, closes and returns `None` otherwise; both
  `_load_payload` (`:469`) and `_load_manifest` (`:748`) go through it.
  ```
  m_fifo            -> exit 2  file_unreadable   (0.021 s, 15.2 MB)
  m_manifest_huge    -> exit 2  input_invalid    (see F4)
  ```
  The device case is closed by the same `S_ISREG` test.

### F4 — **Low — closed at `f767af77…`** (open through `742c2ab1…`, inherited from round 39) — the manifest was read without a size bound

- **Evidence while open** (`742c2ab1…`): a 62,914,661-byte manifest with one valid check → exit 0, `clean`,
  peak RSS 195.2 MB. Previously reported in round 45 (`w1/SentinelFrozen.md`, "Additional local finding —
  Low: unbounded sitemap manifest read").
- **Closure verified** (`f767af77…`): `MAX_MANIFEST_BYTES = 4 * 1024 * 1024` (`:47`),
  `handle.read(MAX_MANIFEST_BYTES + 1)` (`:753`) and an over-size reject (`:756`). Same 60 MB manifest now:
  **exit 2, `input_invalid`, 19.5 MB**. A legitimate matrix manifest is a few hundred bytes, so 4 MiB is
  ample.

### F5 — **Medium — open** — the frozen one-line output can be forged through `--revision`

- **Exploit path.** `frozen_line` interpolates the revision verbatim (`c77_sitemap_matrix.py:286-302`) and
  `--revision` is unvalidated (`:680`). A revision containing `\n` makes the counter print **additional**
  lines indistinguishable in shape from the frozen line, including `met=true`.
- **Evidence** (matrix `5c6eacba…`, closing tool, rc 0):
  ```
  $ python3 -B c77_sitemap_matrix.py --root … --tool scripts/sitemap_audit.py \
      --revision "x
  C2 revision=0000000000000000000000000000000000000000 cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4 met=true
  C2 revision=y" --cases … --consts … --work $S/mwC
  C2 revision=x$
  C2 revision=0000000000000000000000000000000000000000 cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4 met=true$
  C2 revision=y cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4 met=true$
  ```
  The middle line is entirely attacker-chosen.
- **Impact.** The claim's only artifact is this line; a `grep '^C2 '` consumer sees three, one of which can say
  `met=true` over a red run. The caller can print anything anyway, so this is not privilege escalation — it is
  a laundering path for a *seat that proposes a command line* the L1 pastes and runs, which is how this lane
  moves counters.
- **Smallest remediation.** Validate the token before printing (`\A[0-9a-f]{40}\z`, or at minimum `\A\S+\z`) and
  exit 64 otherwise; print the resolved full hash, not the argument.

### F6 — **Low — open** — `--tool-revision` reaches git's option parser; the arbitrary-path write is attempted and fails closed

- **Exploit path.** `c77_sitemap_matrix.py:705-712` builds
  `["git","-C",root,"show", "%s:scripts/sitemap_audit.py" % rev]` with no `--` guard and no validation of
  `rev`; a revision beginning with `-` is parsed as a git option, and `--output=<path>` writes git's output
  there. The derived filename `os.path.join(work, "tool-%s.py" % rev[:16])` is likewise unvalidated.
- **Evidence** (matrix `5c6eacba…`). The space-separated form is rejected by argparse (`expected one argument`);
  the `=` form reaches git:
  ```
  $ … --tool-revision=--output=$S/matrix3-canary --revision deadbeef … --work $S/mwB
  c77_sitemap_matrix: cannot evaluate: git show --output=/fast/…/matrix3-canary:scripts/sitemap_audit.py failed:
    fatal: could not open '…/matrix3-canary:scripts/sitemap_audit.py' for writing: No such file or directory
  $ ls /fast/…/matrix3-canary*   -> no such file
  ```
  The fixed `:scripts/sitemap_audit.py` suffix makes git refuse the path (`git show --output=$S/g1:scripts/…`
  → rc 128; `--output=$S/g2` → rc 0, file written). **No file was written.** I record the mechanism, not a
  successful write.
- **Impact.** Bounded: fail-closed exit 2, no write. A hygiene defect in an instrument the lane treats as
  confining its writes to `--work`.
- **Smallest remediation.** Reject `--tool-revision` unless it matches `\A[0-9a-f]{40}\z`, and pass `--` before
  the revision.

### F7 — **Low — open** — text-path memory amplification, and one recursion class is mislabelled

- **Amplification** (`f767af77…`). A 52,428,800-byte text sitemap that is **one** URL line costs **314.9 MB**
  peak RSS; a 40 MB line costs 255.7 MB; a 52 MB file of 50,000 lines costs 168.3 MB, against a ~15 MB
  baseline. `_audit_text` (`sitemap_audit.py:652`) + `strip()` + `_parse_url` copy the line several times.
  Bounded by `MAX_BYTES`, so the ceiling is ~315 MB per check — but the manifest can name many files (time
  amplification, ~0.15 s each at the cap).
- **Recursion.** `_value_text` (`:338`) recurses over a `<loc>`'s children; 50,000 nested `<loc>` elements
  exhaust the stack: exit 2,
  `{"verdict":"could-not-evaluate","error":"input_invalid","checks":[]}`, 38.2 MB, stderr empty. Fail-closed,
  but an internal fault is labelled *invalid input*.
- **Smallest remediation.** Iterate `_value_text` with an explicit stack (or cap element depth); in `main`,
  give an internal exception its own error code so a crash is not presented as a bad input.

### F8 — **Info — open** — trailing bytes after a valid gzip member are reported `gzip_invalid`

- **Evidence** (`f767af77…`): a valid member followed by 1 KB of non-gzip bytes → exit 2, `gzip_invalid`; a
  member with a wrong CRC → `gzip_invalid`. RFC 1952 does not forbid trailing data and some producers pad, so a
  legitimate file is refused.
- **Impact.** Fail-closed and safe; classification only. C2 freezes "truncated → input fault (2)" and names no
  id, so this is a C2 question; recorded, not graded above info.

### Accepted behaviour (checked, not findings)

- **Any doctype → `doctype_present` (exit 1), before the root gate.** Amendment 1 A9 states this explicitly
  ("an HTML document with a doctype would decide `doctype_present` instead of `format_unsupported`"), and `d01`
  is built without a doctype.
- **Invalid UTF-8 in the body → `encoding_invalid` (exit 1).** Deliberate retention of round-39 behaviour
  (executor, 22:47). Container corruption is exit 2; body decode keeps the frozen id. Nothing becomes clean.
- **An in-tree symlink is followed.** The containment guard is containment, not "no symlinks"; a target inside
  the manifest directory stays readable, which is what the guard is for.

---

## 2. What held on the closing bytes (`f767af77…`)

**Gzip bound (G1/G2) — the core of the claim — holds, and is applied during the read.**
`_load_payload` reads `stream.read(MAX_BYTES + 1)` (`:479`) before deciding (`:503-506`), then reads one more
byte only when under the cap to verify CRC/ISIZE. Peak RSS is flat in the decompressed size — the operational
meaning of "while reading, not after":

| fixture (compressed → decompressed) | exit | finding | peak RSS |
|---|---|---|---|
| `bomb60.gz` (61,181 B → 60 MiB) | 1 | `too_large` | **114.5 MB** |
| `bomb400.gz` (407,706 B → 400 MiB) | 1 | `too_large` | **115.7 MB** |
| `bomb-padded.gz` (407,837 B → 400 MiB, valid urlset first) | 1 | `too_large` | **115.6 MB** |
| `multi-member.gz` (107,999 B → 100 MiB in 100 concatenated members) | 1 | `too_large` | 66.1 MB |

400 MiB and 60 MiB decompressed cost the same ~115 MB: the bomb is never buffered whole. A concatenated-member
bomb is caught **cumulatively** — the limit is on the body, not per member.

**The boundary is exact and on the decompressed size.**

| fixture | size | exit | finding |
|---|---|---|---|
| `exact-limit.txt` (50,000 lines, exactly the limit) | 52,428,800 | 0 | clean |
| `over-limit.txt` | 52,428,801 | 1 | `too_large` |
| `exact-limit.txt.gz` (decompressed = limit) | 291,292 B gz | 0 | clean |
| `over-limit.txt.gz` (decompressed = limit + 1) | 291,295 B gz | 1 | `too_large` |
| `stored-exact.gz` (deflate level 0: **compressed 52,432,841 B > limit**, decompressed exactly 52,428,800) | 52,432,841 | 0 | clean |

The last row is the discriminating one: if the limit were applied to the container, this file would be refused.
It is accepted.

**Container faults are input faults, never clean.** `trunc.gz`, `magic-garbage.gz`, `bad-crc.gz`,
`trailing-garbage.gz`, `header-weird.gz` → exit 2, `gzip_invalid`, 0 findings, empty stderr, 15.3–17.6 MB. A
`.gz` name over a plain body is read as plain (G2).

**XML entities / DOCTYPE.** Every DOCTYPE-bearing document returns a finding **before**
`ElementTree.fromstring` (`:518-529`), and the expat probe runs with `XML_PARAM_ENTITY_PARSING_NEVER` and no
external-entity handler:

| probe | result | peak RSS / wall |
|---|---|---|
| billion laughs (8 levels, `&h;` in a `<loc>`) | exit 1, `doctype_present` | 15.2 MB / 0.060 s |
| XXE `SYSTEM "file://<scratch canary>"` | exit 1, `doctype_present`; canary never appears | 14.9 MB |
| external DTD `SYSTEM "file://<FIFO>"` | exit 1, `doctype_present`, **0.020 s** | 15.2 MB |

The FIFO is the proof of no fetch: if expat opened the external DTD it would block on the FIFO forever. It does
not. (Cross-checked with `/usr/bin/time -v`: `Maximum resident set size (kbytes): 14804` for the entity
document — peak-RSS figures here are `wait4`/`time -v` values, **not** in-process `getrusage`, which in this
shell environment reported an impossible 6,761 MB for a 479-byte parse; recorded so nobody repeats the error.)

**UTF-8 and malformed input.** invalid UTF-8 → `encoding_invalid` (1); UTF-16 with BOM → `encoding_invalid`
(1); overlong `\xc0\xaf` → `encoding_invalid` (1); U+0000 → `xml_malformed` (1); 200k-deep element nesting →
findings (1), 84.3 MB, no crash.

**Exit-code contract.** Every probe case that terminated produced an exit in {0, 1, 2, 64}; every non-64 run
printed exactly one JSON document on stdout; stderr was empty in every run. No input produced
`verdict: clean` together with an error, and no internal exception produced a clean verdict:

| probe | exit | output |
|---|---|---|
| no args / bad flag | 64 | nothing |
| absent manifest, invalid JSON, invalid UTF-8 manifest, 100k-deep JSON | 2 | `"error":"input_invalid"` |
| directory, missing file, FIFO | 2 | per-check `file_unreadable` |
| `MemoryError` (400 MiB bomb under an 80 MB `RLIMIT_AS`, measured on `16ea784f…`) | 2 | `{"verdict":"could-not-evaluate","error":"input_invalid","checks":[]}`, stderr empty |
| `RecursionError` (50k nested `<loc>`) | 2 | same generic document |

**No writes, no shell, no network, in all four files.** `grep -nE "shell=True|os.system|os.popen|socket|http.client|urlopen"`
over the four files → the only hit is `from urllib.parse import urlsplit` (parse-only). No write mode exists in
`scripts/sitemap_audit.py`. The matrix writes only under `--work` (`shutil.rmtree(<work>/selftest)`, fixture
writes, `tool-*.py`) and to `--json-out` (operator-chosen). The ledger's own scratch is `<work>`-scoped.

**Matrix subprocesses.** `observe` (`c77_sitemap_matrix.py:136-160`) runs
`[sys.executable,"-B",tool,"--manifest",manifest]` with `shell` unset, `cwd=work`, `C2_REAL_TOOL` stripped,
`PYTHONDONTWRITEBYTECODE=1`, `timeout`. Ledger git calls are argv lists; `rev-parse` uses `--end-of-options`,
and `evaluate` receives the revision already resolved to a full object id, so `git show`/`cat-file` never see
an argument starting with `-`.

**Cross-file state at close.** Matrix `5c6eacba…` on tool `f767af77…`, frozen case population:
```
C2 revision=f767af770652437d7af18c693dff7cafd64d7f79c38cec36a20e6c4e0bbe9176 cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4 met=true
```
rc 0.

---

## 3. The 52 MB fixture: where it lives, and that it is removed

- **In the lane:** `cases/g02/sitemap.xml.gz` is **51,139 B** — a compressed member whose decompressed body is
  52,428,801 B. The 52 MB body is never a file: the tool materialises at most `MAX_BYTES+1` **in memory**
  (`sitemap_audit.py:479`), and the case builder writes only compressed members (`cases/build_cases.py:204-236`,
  `gzip_bytes` with `mtime=0`). No file under `.ufo/waves/round-77/` exceeds 1,450,029 B
  (`cases/t05/sitemap.txt`).
- **In the selftest:** the two oversized fixtures are real 52 MB files, created under `$TMPDIR`
  (`tempfile.mkdtemp`, `sitemap_audit_selftest.py:1437`) and removed in `finally` (`:1447`). On the closing
  selftest `f22e0a67…`, watched at 20 ms with `TMPDIR=$S/tmp`:
  ```
  PASS 271/271, exit 0, stderr empty
  observed >40 MB during run:
    52428801 …/lim_too_large/a.xml
    52428810 …/r77_text_too_large/s.txt
  leftover entries in TMPDIR after run: 0
  ```
- **In scratch:** at 22:41 two 52,428,800 / 52,428,801-byte files existed under
  `/fast/scratch/hyaku/kake-r77/ScoutSurface/tmp/` (another seat's scratch); both were gone by 22:50 — under
  scratch either way, outside my ownership. My own 52 MB fixtures are under `$S/fx` and are removed at the end
  of this seat (§6).

---

## 4. Measurement table (closing tool `f767af77…`, one row per probe case, `run/finalf7.json`)

| case | exit | peak RSS MB | verdict | codes |
|---|---|---|---|---|
| `ok.xml` | 0 | 14.9 | clean | — |
| `gz-small` | 0 | 15.4 | clean | — |
| `bomb60` / `bomb400` / `bomb-padded` | 1 | 114.5 / 115.7 / 115.6 | failed-policy | `too_large` |
| `multi-member` (100 MiB) | 1 | 66.1 | failed-policy | `too_large` |
| `exact-limit` / `exact-limit.gz` / `stored-exact` | 0 | 168.3 / 168.1 / 168.7 | clean | — |
| `over-limit` / `over-limit.gz` | 1 | 64.7 / 100.0 | failed-policy | `too_large` |
| `trunc` / `magic-garbage` / `bad-crc` / `trailing-garbage` / `header-weird` | 2 | 15.3–17.6 | could-not-evaluate | `gzip_invalid` |
| billion laughs / xxe-local / xxe-dtd / xxe-fifo | 1 | 14.9–15.5 | failed-policy | `doctype_present` |
| `invalid-utf8` / `utf16-bom` / `overlong` | 1 | 15.2–15.5 | failed-policy | `encoding_invalid` |
| `nul-byte` | 1 | 14.9 | failed-policy | `xml_malformed` |
| 200k-deep elements | 1 | 84.3 | failed-policy | `element_unexpected`,`no_entries` |
| 50k nested `<loc>` | 2 | 38.2 | could-not-evaluate | `input_invalid` (generic) |
| symlink to `../outside2/target.xml`, `../outside2/lines.txt` | 2 | — | could-not-evaluate | `check_invalid` (F2 closed) |
| in-tree symlink (`fx/outside/…`) | 0 | 15.5 | clean | by design |
| `../outside/target.xml`, `sub/../../…`, absolute path | 2 | 14.9–15.6 | could-not-evaluate | `check_invalid` |
| directory / missing file / FIFO | 2 | 14.6–15.2 | could-not-evaluate | `file_unreadable` (F3 closed) |
| 60 MB manifest | 2 | 19.5 | could-not-evaluate | `input_invalid` (F4 closed) |
| 40 MB single line / 52 MB single line | 0 | 255.7 / 314.9 | clean | — (F7) |
| 50,000 URLs on one line | 1 | 22.2 | failed-policy | `text_url_not_absolute` |
| no args / bad flag | 64 | 15.1 / 14.9 | — | — |
| absent manifest | 2 | 14.9 | could-not-evaluate | `input_invalid` |

Commands: `$S/run_matrix.py <tool> <label>` drives
`$S/wrapper.py <cap> <summary> <out> <err> -- python3 -B <tool> --manifest <case>` (`os.wait4` rusage per child,
`RLIMIT_AS` per case). Fixtures: `$S/build_fixtures.py`, `$S/build_fixtures2.py`; the out-of-tree containment
fixtures are created inline in §1 F2.

---

## 5. Provenance observations (not SentinelC findings; for the L1 and the C2 reviewers)

1. **Three "final" hashes in nine minutes.** `16ea784f…` was declared final at 22:47, superseded by
   `742c2ab1…` at 22:51:36 (amendment 1 A5/A6/A9), superseded by `f767af77…` at 22:56:28 (the F2/F3/F4 fixes).
   All three were honest; the lesson is procedural — a "final" claim without a hash cannot anchor a receipt,
   and a hash can be invalidated minutes later. This report measures `f767af77…` and says so everywhere.
2. **The contract table and amendment 1 disagree on two ids.** The frozen table says g02 → `sitemap_too_large`
   and names no id for g03; amendment 1 A5/A6 (22:44, "recorded before any after-state") says `too_large` and
   `gzip_invalid`, and the closing case files and tool match the amendment. At 22:50, with the pre-amendment
   case bytes, the matrix printed `correct=18 wrong=2 met=false`; with both sides aligned on the closing bytes it
   prints 20/20 `met=true` (§2). The base receipt `controls/base-c2-matrix.txt` (22:50) exists and states that
   no after-state was run at that point. Whether the amended base re-measurement the amendment promises was cut
   is the C2 reviewers' question; the ids the report must quote are the amended ones.
3. **The C1 amendment that closed F1 was written before the delivered counter** (amendment 2 A2, 22:44) and the
   counter delivered at 22:46 nevertheless executed `argv`; by 22:53 it refused, and the closing v2 counter
   rejects the kind at the schema. Freezing the C1 receipt to `00cb4fb2…` (not `a9eef8bd…`) is load-bearing.

---

## 6. Residual risk, what I did not review, cleanup

- **Threat model.** The manifest, the case tree and the ledger are treated as *untrusted records* (the item's
  framing) and the tool/counters as trusted. Under that model the only finding that ever crossed into code
  execution is F1, closed; F7 is resource amplification bounded by the byte cap; F5/F6 are instrument-integrity
  classes.
- **Not reviewed:** the URL grammar (`_uri_ok`, `:226`-region; `_parse_url`) beyond its role as a copy
  amplifier; the round-39 rule semantics; the C1 predicate; the C2 case contents except for provenance (§5);
  the four `consts/*` tools (inert printers, run only by the matrix); `git` plumbing correctness in the ledger
  beyond the option-injection surface.
- **No `--work` escape found** in the matrix or the ledger other than F1's executed program (closed) and F6's
  blocked attempt.
- **Cleanup.** `rm -rf /fast/scratch/hyaku/kake-r77/SentinelC` after this file is written; every number above
  is copied here first. Drivers (`build_fixtures.py`, `build_fixtures2.py`, `run_matrix.py`, `wrapper.py`,
  `ledger_probe.py`) lived only in that scratch dir by design; their behaviour is described inline.
