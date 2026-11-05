# SentinelScope — round 95 adversarial scope and hygiene audit

Seat: SentinelScope (leaf, no subagent dispatch). Scratch: `/fast/scratch/hyaku/kake-r95/SentinelScope/` (deleted before yield; receipts copied to `receipts/` beside this file). Lane HEAD observed at audit: `d9be693f` (freeze `8f638b59` is an ancestor).

Verdict line: `SCOPE shadows-refused=5 sandbox-escapes=[symlink-read-outside-subject, os.execv-unaudited] writes-clean=yes`

Headline findings (ranked):
1. **C1 instrument was changed after the declared freeze** (commit `d9be693f`, 13:36:06, seven minutes after the freeze commit `8f638b59` at 13:29:12). The counter's identity surface was relaxed. The frozen digest pins in `freeze.md` and `controls/instrument-sha256.txt` no longer match the lane's counter at the freeze revision (see F1 below).
2. **C2 counter has no effectful-shadow defense** (R94-2 not closed for C2). Five of ten shadow runs executed a planted `subprocess.py`.
3. **C2 sandbox is escapable**: a symlink inside the subject tree reads any file (including the counter source); `os.execv` runs `/bin/sh` unconstrained. The symlink escape was confirmed end-to-end through the real `c95_conditional.py` pipeline (candidate read 39148 bytes = the counter's full source).
4. **C1 sanitization does not cover PYTHONPATH shadows** from a directory other than the script dir (mode D).
5. Documentation defect: the freeze command is `python3 -B`, but the C1 counter header says "the frozen command also runs python3 -I". False.

## Method and commands (all rc observed)

- Digest check, C2: `sha256sum c95_conditional.py` = `f09f84090fdda405992d7b51191be8838549e3df402b0898eb2ca00c4c3ff312` (matches pin). PASS.
- Digest check, C1: first check (~13:33, before `d9be693f`) = `8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193` (matches pin). Later checks (after `d9be693f`) = `04be4a7dc32adee08e386936e2af8257a191421bd2005c97b40af49933a24a32`. **MISMATCH with the frozen pin; a finding, not a repair license.** I did not repair anything.
- Fixture: `git clone --no-hardlinks` of the lane to scratch, toplevel asserted equal to the fixture dir before every commit. Lane was never mutated by me.

### (1) Effectful shadows (R94-2)

Planted `subprocess.py` (writes `MARK` into its own directory, then `sys.exit(7)`) beside copies of each counter. Runs use `env -i PATH=/usr/bin:/bin HOME=… TMPDIR=…` with `--root <fixture> --revision 8f638b59… --work <scratch>`.

| run | invocation | C1 `c95_selfassess.py` | C2 `c95_conditional.py` |
|---|---|---|---|
| A | shadow in script dir, `python3 -B` | marker absent, rc=1, own `C1v95` line → refused | marker **present**, rc=7, no verdict → EFFECT |
| B | script dir + `PYTHONPATH=<shadow dir>`, `python3 -B` | absent, rc=1, own line → refused | **present**, rc=7 → EFFECT |
| C | as B under `python3 -I` | absent, rc=1, own line → refused | absent, rc=1, own `C2v95` line → refused |
| D | counter in own dir; shadow only via `PYTHONPATH` from a separate dir | **present**, rc=7 → EFFECT | **present**, rc=7 → EFFECT |
| E | `python3 -B -c` wrapper, shadow reached via `sys.path.insert(0,'.')` | absent, rc=1, own line → refused | **present**, rc=7 → EFFECT |

- shadows-refused = 5 of 10 (C1: A, B, C, E; C2: C). Effects observed in 5 of 10 (C1-D; C2-A, B, D, E).
- Mechanism: C1 (`c95_selfassess.py` lines 100-111) removes the script directory from `sys.path` before `import subprocess`, so the script-dir shadow cannot load, but it does not remove other `PYTHONPATH` entries (mode D). C2 (`c95_conditional.py` line 74) has no sanitization at all. `-I` is the only protection for C2.
- Harness note (not a counter defect): my first C1 pass copied only the counter file, so C1 stopped at `unevaluable=missing frozen/c1-surfaces.json` (rc=2). The table above is from the rerun that copied `frozen/` too. Raw receipts: `receipts/shadow1/`, `receipts/shadow2/`, `receipts/shadow-summary.txt`.

### (2) C2 sandbox escapes

Extracted the `SANDBOX` string verbatim from `c95_conditional.py` (`receipts/c2-sandbox-extracted.py`, sha256 `64cffb79649b3ea844019eefe0c924b5ae7152035c1dae7eb801cd1dc61e2db3`). Subjects run as `python3 -B sandbox.py <subject>`, cwd=work, minimal env, exactly as the counter's `run_subject` does.

| subject | probe | rc | observed |
|---|---|---|---|
| b00_ok | happy path | 0 | works (stdout not shown: harness quirk, rc is authoritative) |
| p01 | `open('/etc/hostname')` | 1 | denied: `PermissionError: sandbox: open outside the subject tree` |
| p02 | `import shutil` | 1 | denied: `import denied: shutil` |
| p03 | `os.system('true')` | 1 | denied: `process creation denied: os.system` |
| p04 | `import subprocess; subprocess.Popen` | 1 | denied at **import** (`import denied: subprocess`), not at the Popen audit event |
| p05 | read the counter file itself | 1 | denied: `open outside the subject tree: …/c95_conditional.py` |
| x01 | `os.symlink('/etc/hostname', root/lnk1)`, then read `root/lnk1` | 0 | **ESCAPE**: read `/etc/hostname` contents |
| x02 | `os.symlink(<counter path>, root/lnk2)`, then read | 0 | **ESCAPE**: read the counter source |
| x03 | `os.execv('/bin/sh', …)` writing a marker outside the subject tree | 0 | **ESCAPE**: `exec_marker` created outside the subject tree (`os.exec*` is not a denied audit event) |
| x04 | `os.open(…, O_CREAT|O_WRONLY)` outside the tree | 1 | denied (audit `open` covers `os.open`) |
| x05-x07 | `importlib.util.spec_from_file_location` loading stdlib / `_posixsubprocess` | 1 | denied at transitive `import fnmatch` / `import glob`. Not a bypass for these; a leaf non-allowlisted module was **not** tested |

Cause: the open hook uses `os.path.abspath`, not `realpath`, so any symlink created inside the subject tree is trusted. Symlink creation itself is not audited. `os.exec*` is not in the denied event list.

End-to-end confirmation (scratch fixture commit `847fc677`/`c29f8aed`-series, candidate `scripts/conditional_eval.py` that symlinks the counter and returns the bytes it read in its `decision`): the real `c95_conditional.py --root <fixture> --revision <leak-rev> --work <scratch>` ran the candidate and the output (`receipts/e2e-leak/out.txt`) contains `LEAKOK bytes=39148 head=b'#!/usr/bin/env python3\n…` — the complete counter source, read through the sandbox. rc=1 (candidate correctly refused, `hand=0/66`, which is irrelevant to the leak). Impact: a candidate can read the counter's reference and pins. [INFERENCE] that a candidate could also use the read to tune against the reference; not tested.

### (3) Scope and writes

- Lane runs: `python3 -B c95_selfassess.py --root <lane> --revision 8f638b59… --work <scratch>` → rc=1, `C1v95 … mismatches=18 E1=0 E2=0 E3=3 E4=0 E5=15 pins=ok battery=20/20 admit=5/5 shadow=absent predecessor_admits=10/19 floor=4 self_pin=ok met=false` (receipts `lanerun/c1-*`). `python3 -B c95_conditional.py --root <lane> --revision 8f638b59… --work <scratch>` → rc=1, `C2v95 … candidate=present hand=57/66 generated=79/120 forgeries_refused=7/7 positive=admitted mutants=40/40 survivors=none anti_table=ok population=ok seed=95 met=false` (receipts `lanerun/c2-*`). Both measured the **on-disk** counters, i.e. the post-amendment C1 counter (see F1).
- Lane `git status --porcelain` before/after my runs: the only differences were new untracked entries from other seats (`w1/ExecC1Repair/`, `w1/ScoutErrata.md`). My counters created nothing in the lane (`--work` honored; C2 removes its tree on exit per its docstring).
- Unattributed write: `.ufo/waves/round-95/__pycache__/c95_conditional.cpython-314.pyc` mtime 13:38:01, inside my window. All my invocations used `-B` and executed the counter as a script (never imported), so I did not create it. Attribution not established; flagged for the L1.
- `w1-spec.json` write-path keys: only `/reportDir → .ufo/waves/round-95/w1` (inside w1). No other absolute write path found in `w1-spec.json` or `w1-dispatch.json`.
- pacman: `/var/log/pacman.log` has 0 lines dated 2026-11-05 (readable, `grep -c` rc=0 count 0). No `pacman -S/-U/-R/-Sy` string in the round-95 tree. Evidence limited to the log and tree; seat transcripts were not inspected.
- Credential-shape scan (PCRE: `sk-…`, `ghp_…`, `op://`, `PRIVATE KEY`, mixed-case base64 ≥40): hits only in `w1-spec.json:55`, `w1-dispatch.json:84,159`, `w1/swarm-registry.json:66`, all the prohibition sentence "no file … matches a credential shape (sk-, ghp_, op://, BEGIN PRIVATE KEY, long base64 tokens)". No secrets. The counters themselves matched nothing.
- Sysctl `user.max_user_namespaces`: before = 122865 (16:33:29Z), after = 122865. Unchanged. No sysctl was modified.

## F1 — C1 instrument modified after freeze (Amendment A), measured

Freeze commit `8f638b59` (instruments `43cdd9fc`) versus HEAD `d9be693f` (`kake-shokunin`, 13:36:06, "amendment A pre-scoring"):

| item | at freeze `8f638b59` | at HEAD `d9be693f` |
|---|---|---|
| `c95_selfassess.py` blob | `f1836665…` | `985e39bb…` |
| `c95_selfassess.py` sha256 | `8fd27d62…` (pinned) | `04be4a7d…` |
| `frozen/c1-surfaces.json` sha256 | `00a04c9a…` (pinned) | `9eff04c5…` (82 lines removed) |
| identity rule | entry head-8-line content digest | entry presence only |
| `freeze.md` | as declared | +30 lines "## Amendment A" |
| `controls/base-c1.txt` | counter `8fd27d…` | re-stamped to `04be4a…`; counts unchanged |

Measured effect (`receipts/amend/`): a one-line head edit to `corpus/knowledge/accessibility-review-packet.md` committed to a scratch fixture (`REV3`-series), scored by both counters at that revision:
- frozen counter (`8fd27d…`, from `8f638b59`): `pins=identity`
- amended counter (`04be4a…`, HEAD): `pins=ok`
Both `met=false` (E3=3, E5=15, mismatches=18 unchanged). So the amendment removes an identity refusal that the freeze's kill rule ("an identity or cardinality pin" fails the claim) would have raised. The amendment's own text says "no predicate, target or kill rule changed," but the identity pin is a kill-relevant surface and was relaxed after freeze, in the same commit that re-stamped the base control. The amendment landed while seats were already running (the first digest check at ~13:33 still showed the frozen value).

Under the frozen declaration, the C1 instrument's digest check fails. Per the assignment, that is a finding. I did not revert or repair anything. The L1 must decide whether Amendment A is an authorized instrument change (it contradicts "frozen before data") and whether C1's `met=true` claim is evaluated against `8fd27d` or `04be4a`.

## Recommended smallest remediations (not applied)

1. Revert the C1 instrument to the freeze blob and digests, or re-freeze explicitly with a new declared digest set before any scoring. Do not re-stamp base receipts under a new digest.
2. C2: add the same `sys.path` sanitization as C1 before `import subprocess`, and run the frozen command with `python3 -I`. Fix the C1 header claim about `-I`.
3. Sandbox: in the audit hook, `os.path.realpath` the path before the root-prefix check (or deny `os.symlink` / `os.readlink` writes inside the subject tree). Deny `os.exec*` events (add `os.exec` to the denied set). Consider a leaf-module import bypass test (e.g. `colorsys` via `spec_from_file_location`), not run here.

## Receipts (`receipts/`)

- `shadow-summary.txt`, `shadow1/` (first pass, C1 rc=2 harness artifact), `shadow2/` (C1 rerun with frozen/), `drive_shadow.sh`
- `sandbox-summary.txt`, `probe_sandbox.sh`, `c2-sandbox-extracted.py`, `sbx-*.err`, subject sources `p*.py x*.py b00_ok.py`
- `lanerun/` (c1, c2 rc/out/err), `e2e-leak/` (rc/out/err), `amend/` (pre/post rc/out/err and the two counter versions), `base-c1-amendment-diff.txt`
- `lane-status-before.txt`, `lane-status-after.txt`

Checks the main agent should run: `sha256sum .ufo/waves/round-95/c95_selfassess.py` (expect `8fd27d…` if Amendment A is reverted, else the amended `04be4a…` plus a recorded instrument decision), and the freeze-digest comparison in `controls/instrument-sha256.txt`.

Tools: no installs or upgrades. Only `python3`, `git`, `sysctl`, `grep`, `sha256sum`, `find`, coreutils used. No pacman, no sysctl writes.
