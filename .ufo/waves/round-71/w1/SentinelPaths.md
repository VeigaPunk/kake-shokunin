# SentinelPaths — round 71 w1 (read-only security/path scan)

Scope: `c71_calibration.py`, `c71_tmp.py`, `contract.md` at freeze commit `04557e17` (sha256 identical to the working-tree bytes: `ae3176…`, `903774…`, `3c31e0…`). Base `cc6b4e0b8c35e72dfb02c6184b847f68c1262153`. No tools installed (preinstalled git 2.56.0, python3 3.14.8, strace). Read-only: no lane file edited, no git mutation in the lane; every probe ran in `/fast/scratch/hyaku/kake-r71/SentinelPaths` (scratch clone at base).

## (a) Literal scratch path under the system temp root in code — PASS (no literal)
`grep -n '/tmp' c71_calibration.py c71_tmp.py contract.md` → exit 0; hits only in `c71_tmp.py` L2, 6, 9, 10 (module docstring — excluded by the check) and `contract.md` L48, 50, 56, 61, 97, 103 (prose describing the predicate). `c71_calibration.py`: 0 hits.
AST literal dump (docstrings excluded): the only code-level temp reference is `c71_tmp.py:26 TMP_ROOT = "/" + "tmp" + "/"` — assembled at runtime, so the file text carries no `/tmp` literal; it is used once in `TOKEN_RE` (L27) as a text-matching prefix and is never opened as a path. No `/tmp/…` scratch-path literal in code. Observation, not a finding: the split-literal deliberately evades a naive `grep /tmp`; the value built is the temp root itself, used only for regex matching.

## (b) Credential material / token / cookie / key / `op://` — PASS (none)
`grep -nEi 'op://|-----BEGIN|api[_-]?key|secret|password|bearer |cookie:|authorization:|ghp_|sk-[A-Za-z0-9]{16}'` over the three files → exit 1, 0 hits; same scan over every blob of `.ufo/waves/round-71/` at `04557e17` → exit 1, 0 hits. The only `token` word matches are the counters' own metrics (`unannotated_tokens`, `tokens_total`) and "path token".

## (c) Git/jj write command or network call — PASS with one exploitable caveat (F1)
`grep -nE 'subprocess|urlopen|requests|socket|urllib|http|jj '` → only `import subprocess` and two call sites, `c71_calibration.py:39` / `c71_tmp.py:31`: `subprocess.run(["git","-C",lane,"show",f"{rev}:{path}"], capture_output=True, text=True)`. `grep -nE '\bjj\b'` → exit 1, 0 hits. `strace -f -qq -e trace=network` over a full C1 run → 387 B, SIGCHLD only, no socket/connect/bind. No mutating git verb, no `jj`, no network. Caveat: `rev` is interpolated unvalidated into the git argv (F1).

## (d) Filesystem writes by the counters — PASS in normal operation; FAILS under a hostile `--revision`
`strace -f -qq -e trace=file,write` on both counters at base (both exit 1; receipts byte-identical to `controls/c1-base.txt` / `c2-base.txt`): C1 → 0 × `O_CREAT|O_WRONLY`, 55 × `write(1,…)`; C2 → 0 × `O_CREAT|O_WRONLY`, 26 × `write(1,…)`; only `/dev/null` opened `O_RDWR` (subprocess stdin). `grep -nE 'open\(|Path\(|os\.makedirs|mkdir|mkstemp|NamedTemporaryFile|TemporaryDirectory|tempfile|shutil|unlink|rmtree'` → 0 hits (only the word "removed" in counter names). The counters write nothing themselves. Lane tree after all my runs: `git -C <lane> status --porcelain` → only pre-existing untracked wave files.

## (e) TMPDIR honour — NOT APPLICABLE (counters create no temp files)
`grep -nEi 'TMPDIR|tempfile|getenv|environ'` → no `tempfile`/`TMPDIR`/`environ` use (only "temp" in the docstring and `TMP_ROOT`). `grep -cE '"/tmp|TMPDIR'` on both straces → 0 and 0. Neither counter creates, opens or deletes a temp file, so TMPDIR cannot affect them and they need not honour it.

## F1 (finding) — git argv injection through `--revision` ⇒ arbitrary file write
Severity medium (local; needs a hostile/careless `--revision`; no remote path, no privilege gain). Exploit path: `show()` builds the git argument as `f"{rev}:{path}"` with no `--end-of-options` and no rev validation, so a `--revision` starting with `-` is parsed by git as an option; `git show --output=<file>` writes there and the counter's `:<path>` suffix is absorbed into the file name. Relative paths resolve against the `git -C <lane>` directory → a write lands inside the lane tree.
Evidence (scratch only): `--revision "--output=$S/inj1.out"` → counter exit 2, file `$S/inj1.out:SCORECARD.md` (10146 B, content = `git show HEAD` of the lane) created; C2 `--output=$S/injC2.out` → exit 1, file `injC2.out:SKILL.md`; `--output=../outside/escaped.txt` → `$S/outside/escaped.txt:SCORECARD.md`; `--output=STRAY_FILE:SCORECARD.md` → file created in the `git -C` dir (`git status --porcelain`: `?? STRAY_FILE:SCORECARD.md:SCORECARD.md`); pre-existing 39 B `$S/trunc.txt:SKILL.md` replaced by 10146 B (overwrite). Not reachable via `--lane` (`--lane "--output=/tmp/laneinj"` → exit 128, no file; the lane value is the separate `-C` argument); `--exec` → `fatal: unrecognized argument`, no marker. No false green: injected runs exit 2 (C1) / 1 (C2), the write happens regardless.
Impact: violates the counters' "reads committed bytes only" claim and this seat's "must write nothing"; a hostile revision can plant/truncate files (repo-derived content) under any writable directory, including the lane working tree, silently.
Smallest remediation — NOT applied (counters are frozen; the kill rule makes any counter edit after the first seat scored ⇒ C1/C2 `unprovable`): in `show()`, insert `--end-of-options` before the rev, or reject any `rev` not matching `^[0-9a-f]{7,40}$|^HEAD$`. Proven: `git show --end-of-options "--output=$S/mit.txt:SCORECARD.md"` → exit 128, no file; `git show --end-of-options <base>:SCORECARD.md` sha256 `fdbbe0196e53b9d0cacafe1b210720cef94cabf9c225ee8f19b2bdd6d926e502` == plain `git show` bytes.

## Attacks run and verdicts
| # | Attack | Verdict |
|---|---|---|
| 1 | grep literal `/tmp` in code (not docstrings) | no literal — PASS |
| 2 | AST literal sweep for temp/scratch paths in code | only runtime-assembled `"/"+"tmp"+"/"`, never an I/O path — PASS |
| 3 | credential / `op://` / key / cookie / token grep (3 files + whole wave dir) | no hits — PASS |
| 4 | grep git / `jj` / network / subprocess call sites | only `git show`, no `jj`, no net — PASS |
| 5 | strace network syscalls over a full C1 run | no socket calls — PASS |
| 6 | strace file+write on C1 and C2 at base (lane cwd) | 0 creates, stdout-only writes — PASS |
| 7 | strace temp-path / TMPDIR probe | 0 hits; no temp files created — N/A (no TMPDIR need) |
| 8 | `--revision "--output=<path>"` → file write | file created — FAIL (F1) |
| 9 | `--revision "--output=../x"` → traversal write | file created outside the lane dir — FAIL (F1) |
| 10 | `--revision "--output=rel"` → write into lane dir | file created in the `git -C` dir — FAIL (F1) |
| 11 | `--revision "--output=<existing>"` → overwrite | 39 B file replaced by 10146 B — FAIL (F1) |
| 12 | `--lane "--output=/tmp/x"` → option injection via lane arg | exit 128, no file — PASS |
| 13 | `--revision "--exec=touch <marker>"` → command exec | `fatal: unrecognized argument`, no marker — PASS |
| 14 | `--revision "--ext-diff"` / `"--textconv"` → filter exec | exit 128 (glued `:path` breaks the flag) — PASS |
| 15 | `--revision "HEAD:/etc/passwd"` / `"HEAD:../../../etc/passwd"` → path escape | `exists on disk, but not in 'HEAD'` / `is outside repository` — PASS |
| 16 | newline in `--revision` → receipt-line forgery | one argv element; git show exit 128, counter exit 2 — PASS |
| 17 | ambient `GIT_EXTERNAL_DIFF` → external command | no marker; blob form runs no diff — PASS |
| 18 | mitigation `--end-of-options` | blocks the write (exit 128, no file), byte-identical for a legit rev — PASS |

## Limits (named, not verified)
`jj` is absent from the host, so the `jj` result is grep-level only; the git option surface beyond those probed is not exhaustively enumerated; `--output` content is repo-derived (`git show HEAD`), and I did not test whether a crafted `rev` makes `git show` emit attacker-chosen bytes; the counters' trust in the supplied revision (a fabricated tip could report `met=True`) is inherent to the frozen design, not a path defect.
