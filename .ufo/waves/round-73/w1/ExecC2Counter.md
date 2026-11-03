# ExecC2Counter — C2 counter delivery (round 73, w1, kake)

Seat: `ExecC2Counter` (executor, leaf). Scope: contract section C2 only.
Base revision `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`; lane master tip read read-only at
measurement time: `4c7c53bc563a66ae0676b468966781f023ae0110`
(`git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse master`, exit 0).
Base and tip both carry SKILL.md blob `f6a7408d67ffab3ecd02d46e12ab1f64906387e6` (identical bytes).

## Deliverable

`.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py` — 491 lines, sha256
`9b4d2cd0d1a3ac5f834d6bac28966cd70f9ee9927f3e9a7753ff8b818eeb5027`, mode 0644.
The contract names the promoted path `.ufo/waves/round-73/c73_tmp_v3.py`; the integrator moves
and commits it (I wrote nothing outside `w1/ExecC2Counter/` and this report). The counter has no
dependency on its own path, so promotion is a byte copy.

Frozen corpus read only, never edited: `.ufo/waves/round-73/attack-corpus.txt`, sha256
`9da8778285b3e8c0dbdd85efcbcd55beae1771a9b82218201066f778579ed44b`
(11 `attack` lines at file lines 4–14, 4 `legit` lines at file lines 15–18).

## Behaviour

Reads committed bytes only: mode from `git -C <lane> ls-tree <rev> SKILL.md`; mode `100644`
reads `git -C <lane> show --end-of-options <rev>:SKILL.md`; mode `120000` is a finding (exit 1,
not an evaluation error); absent `SKILL.md` or any other mode is unevaluable (exit 2).
Inherited `GIT_DIR`/`GIT_WORK_TREE`/index/object pointers are scrubbed from every git subprocess
so `--lane` decides the repository.

Detection per scratch-root token (`/` + `tmp`, path tail; brace first, then command, then prose —
a token counts once):

- **H1 brace** — token inside a shell parameter default `${NAME<op>word}` (`:-`, `-`, `:=`, `=`;
  nested defaults handled) is a finding. `${TMPDIR:-/tmp}` and `${TMPDIR:-/tmp}/x` both count.
- **H2 command** — segments split on `&&`, `;`, `|` and backticks; leading `NAME=value`
  assignments and the `sudo`, `env`, `nohup`, `time`, `exec` prefixes are stripped (including
  their `-x` options), then the segment's first word (basename of a path) must be one of the
  35 frozen command words. The token is a command finding when its line carries such a segment;
  a phrase annotation never excuses it.
  Scope note (disclosed): the frozen corpus line
  ``run `cp` state/probe-latest.json /tmp/... (historical record, ...)`` puts the quoted command
  word in its own backtick segment and the token in the next segment; a token-segment-only
  reading would accept an attack line the corpus marks as a finding, so command detection is
  line-scoped over the line's shell segments. This is the corpus-required reading, not a
  weakening: no corpus `legit` line carries a command segment.
- **H3 symlink** — `SKILL.md` mode `120000` is reported and exits 1.
- **H4 phrase** — only the full phrase `not an executable instruction` annotates a prose token;
  truncated variants (`historical record`, `not an executable`) are prose findings. Asserted by
  two selftest cases.

Token boundary: a leading path-component boundary plus a trailing word boundary are required, so
`/var/tmp`, `a/tmp` and `/tmp2` are not tokens; `${TMPDIR:-/tmp}`, `TMPDIR=/tmp`, `"/tmp` and a
bare `/tmp` are. No literal scratch path exists in the source (`grep -c '/tmp'` = 0, exit 1).

Options: `--selftest`, `--lane`, `--revision`, `--corpus <file>`, `--work <dir>`; `--help`
exits 0; unknown options exit 64. `--corpus` alone classifies the corpus; adding `--lane` also
evaluates SKILL.md and both scopes must be clean. Output line:

```
C2v3 revision=<rev> attack_accepted=<n>/<A> legit_rejected=<n>/<L> selftest=<p>/<t> findings=[...] met=<bool>
```

Exit 0 met · 1 not met · 2 unevaluable · 64 usage. Scratch fixtures (the H3 repo) live under
`--work`, else `$TMPDIR`, and are removed in `finally`; both were measured residue-free.

## Measurements (all commands absolute, run from the fleet root)

### (a) selftest

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --selftest
```
exit **0**; 41 case lines `OK`; final line:
`C2v3 revision=selftest attack_accepted=0/0 legit_rejected=0/0 selftest=41/41 findings=[] met=True`

Inventory (41): H1 5 · H2 13 (rsync, rm, env-assignment, sudo, quoted command word, backticked
sudo, `cd && cp`, env+assignment, nohup, time, exec, plain, phrase-does-not-excuse) · legit/prose 4 ·
false-match 3 (`/tmp2`, `/var/tmp`, `a/tmp`) · bare root 2 · H4 3 (two truncations + full) ·
H3 mode 3 (`100644`→ok, `120000`→symlink, `100755`→unevaluable) · corpus parser 4 (valid,
malformed, inconsistent pairing, empty) · corpus counts 1 · H3 real repo 3 (regular→ok,
symlink→finding, absent→missing). The H3 repo fixture asserts
`git rev-parse --show-toplevel` equals the fixture before its first commit.

Additional exercised spot-checks (module imported by `importlib` from the delivered absolute path,
`line_findings` called directly; exit **0**):

```
sudo_option      (0, 1, 0)   sudo -E cp state/x <token>/kake-r12/live/y (phrase)
env_option       (0, 1, 0)   env -i TMPDIR=<token>/kake-r12 python3 -B tool.py (phrase)
time_option      (0, 1, 0)   time -p cp state/x <token>/kake-r12/live/y (phrase)
exec_option_arg  (0, 0, 0)   exec -a runner cp state/x <token>/kake-r12/live/y (phrase)  # disclosed residual
brace_short_op   (1, 0, 0)   BK=${X-<token>/kake-r12} then
brace_assign_op  (1, 0, 0)   BK=${X:=<token>/kake-r12} then
brace_equal_op   (1, 0, 0)   BK=${X=<token>/kake-r12} then
```

`python3 -B <deliverable> --help >/dev/null` exit **0**.

### (b) frozen corpus

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --corpus /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/attack-corpus.txt
```
exit **0**:
`C2v3 revision=corpus attack_accepted=0/11 legit_rejected=0/4 selftest=41/41 findings=[] met=True`

Contract-form combined command at base (clone at
`/fast/scratch/hyaku/kake-r73/ExecC2Counter/clone`, the prescribed `git clone --shared` +
detached checkout):

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --lane /fast/scratch/hyaku/kake-r73/ExecC2Counter/clone --revision c1f3d8d4ed9470ecbaaf3353952a374b079e68cc --corpus /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/attack-corpus.txt
```
exit **0**:
`C2v3 revision=c1f3d8d4ed9470ecbaaf3353952a374b079e68cc attack_accepted=0/11 legit_rejected=0/4 selftest=41/41 findings=[] met=True`

### (c) SKILL.md at base and tip (clone, read-only)

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --lane /fast/scratch/hyaku/kake-r73/ExecC2Counter/clone --revision c1f3d8d4ed9470ecbaaf3353952a374b079e68cc
```
exit **0**: `C2v3 revision=c1f3d8d4ed9470ecbaaf3353952a374b079e68cc attack_accepted=0/0 legit_rejected=0/0 selftest=41/41 findings=[] met=True`

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --lane /fast/scratch/hyaku/kake-r73/ExecC2Counter/clone --revision 4c7c53bc563a66ae0676b468966781f023ae0110
```
exit **0**: `C2v3 revision=4c7c53bc563a66ae0676b468966781f023ae0110 attack_accepted=0/0 legit_rejected=0/0 selftest=41/41 findings=[] met=True`

SKILL.md has exactly four token-bearing lines at base and tip (27, 227, 356, 359); each is a
prose annotation with the full phrase and no command segment, and each returns `(0, 0, 0)`.

### (d) do-nothing control — frozen c72 `line_findings`

Frozen c72 file untouched — its sha256 measured at run time is
`af2f0c9c6b7ba04facdf63397b1e2e66ca20dd464984745354409d91fcf6e6ca`; imported by
`importlib.util.spec_from_file_location` from its absolute path and called per corpus line
(`line_findings` only; no edit). Retained, re-runnable form (run from the fleet root):

```
python3 -B - <<'PY'
import importlib.util
C72 = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-72/c72_tmp_v2.py"
CORPUS = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/attack-corpus.txt"
spec = importlib.util.spec_from_file_location("c72_frozen", C72)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
acc = A = L = rej = 0
for line in open(CORPUS, encoding="utf-8"):
    t = line.rstrip("\n")
    if not t.strip() or t.startswith("#"):
        continue
    cls, exp, body = [p.strip() for p in t.split("|", 2)]
    b, c, p = m.line_findings(body)
    if cls == "attack":
        A += 1; acc += (b + c + p) == 0
    else:
        L += 1; rej += (b + c + p) > 0
print(f"c72_accepts={acc}/{A} c72_legit_rejected={rej}/{L}")
PY
```
exit **0**: `c72_accepts=9/11 c72_legit_rejected=0/4`

The nine accepted attack lines are file lines 4–12 (H1 fallbacks, rsync, rm, env-prefix python3,
backticked sudo, `cd && cp`, quoted `cp` with the token in the next segment, sudo-prefixed cp);
c72 rejects only the two plain `cp` command lines (13–14). This is the contract's `k ≥ 1`
control with `k = 9`.

### (e) deliberate break — counter fails red for the named reason

Corpus copy plus one attack line c73 accepts (a purely annotated prose line carrying a token):

```
cp /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/attack-corpus.txt /fast/scratch/hyaku/kake-r73/ExecC2Counter/red-attack.txt
printf '%s\n' 'attack | finding | the snapshot was under /tmp/kake-r12/live/ (historical record, not an executable instruction)' >> /fast/scratch/hyaku/kake-r73/ExecC2Counter/red-attack.txt
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --corpus /fast/scratch/hyaku/kake-r73/ExecC2Counter/red-attack.txt
```
exit **1**: `C2v3 revision=corpus attack_accepted=1/12 legit_rejected=0/4 selftest=41/41 findings=[('corpus', 19, 'attack', 'accepted', 0, 0, 0)] met=False`

Corpus copy plus one legit line the counter rejects (a command line):

```
cp /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/attack-corpus.txt /fast/scratch/hyaku/kake-r73/ExecC2Counter/red-legit.txt
printf '%s\n' 'legit | clean | cp state/probe-latest.json /tmp/kake-r12/live/backup.json' >> /fast/scratch/hyaku/kake-r73/ExecC2Counter/red-legit.txt
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --corpus /fast/scratch/hyaku/kake-r73/ExecC2Counter/red-legit.txt
```
exit **1**: `C2v3 revision=corpus attack_accepted=0/11 legit_rejected=1/5 selftest=41/41 findings=[('corpus', 19, 'legit', 'rejected', 0, 1, 0)] met=False`

### H3 and unevaluable evidence (from the same counter binary)

- Fixture repo (scratch `fix-skill`, built with `git init` + commit of a SKILL.md containing one
  clean line and four planted findings) — exact invocation:

  ```
  python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --lane /fast/scratch/hyaku/kake-r73/ExecC2Counter/fix-skill --revision HEAD
  ```
  exit **1**:
  `findings=[('skill',2,1,0,0),('skill',3,0,1,0),('skill',4,0,0,1),('skill',5,0,1,0)]` — the
  counter detects tokens in SKILL.md mode, not only in corpus mode.
- Fixture repo with a committed **symlink** SKILL.md (mode 120000):

  ```
  python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --lane /fast/scratch/hyaku/kake-r73/ExecC2Counter/fix-symlink --revision HEAD
  ```
  exit **1**:
  `findings=[('skill', 'symlink', 'SKILL.md mode 120000 (symlink) at revision HEAD')]` — a
  finding, not exit 2.
- Fixture repo without SKILL.md:

  ```
  python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --lane /fast/scratch/hyaku/kake-r73/ExecC2Counter/fix-missing --revision HEAD
  ```
  exit **2**: `findings=[('unevaluable', 'SKILL.md absent at revision HEAD')]` (stderr
  `C2v3 unevaluable: SKILL.md absent at revision HEAD`).
- Malformed corpus (`bad-corpus.txt` holding the single line `attack | finding`):

  ```
  python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --corpus /fast/scratch/hyaku/kake-r73/ExecC2Counter/bad-corpus.txt
  ```
  exit **2**:

  ```
  findings=[('unevaluable', "corpus line 1 is not `<class> | <expected> | <line>`: 'attack | finding'")]
  ```
- Unknown option:

  ```
  python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --bogus
  ```
  exit **64** (usage on stderr, empty stdout).

The same regular/symlink/absent assertions are built into `--selftest` (`h3_fixture_regular_ok`,
`h3_fixture_symlink_finding`, `h3_fixture_absent_unevaluable`), so they survive the scratch
deletion.

### Scratch, `TMPDIR`, `--work`

- ```
  TMPDIR=/fast/scratch/hyaku/kake-r73/ExecC2Counter/tmpd2 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --selftest
  ```
  exit **0**, final line `... selftest=41/41 ... met=True`;
  `find /fast/scratch/hyaku/kake-r73/ExecC2Counter/tmpd2 -mindepth 1 | wc -l` = **0**.
- ```
  python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py --selftest --work /fast/scratch/hyaku/kake-r73/ExecC2Counter/workd2
  ```
  exit **0**, 41/41; `find /fast/scratch/hyaku/kake-r73/ExecC2Counter/workd2 -mindepth 1 | wc -l`
  = **0**.
- The scratch tree (clone, fixture repos, red corpora, driver script, logs) was removed with
  `rm -rf -- /fast/scratch/hyaku/kake-r73/ExecC2Counter` (exit 0); the parent directory then held
  only other seats' trees (`CriticClaims`, `main`).

### Lane integrity

- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD` →
  `4c7c53bc563a66ae0676b468966781f023ae0110` (unchanged; exit 0).
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain` shows only the
  pre-existing untracked paths (`.ufo/waves/round-71/w1.ready*`,
  `.ufo/waves/round-73/w1-dispatch.json`, `w1.ready*`, `.ufo/waves/round-73/w1/`);
  `git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --stat` and `diff --cached --stat` are
  empty (exit 0). No `git add`/`commit`/`checkout`/`reset`/`jj` command was run in the lane; the
  only clone checkout was the prescribed detached checkout of the base in scratch.
- `git -C /fast/scratch/hyaku/kake-r73/ExecC2Counter/clone rev-parse HEAD` → `c1f3d8d4...`,
  `git -C /fast/scratch/hyaku/kake-r73/ExecC2Counter/clone status --porcelain` empty (exit 0).

## Risks / residuals (disclosed, none blocking)

1. **H2 scope** is line-scoped over shell segments (see above). Required by frozen corpus line 11;
   it is stricter than a token-segment-only reading, so it can only add findings, never accept an
   attack line. No `legit` corpus line is affected.
2. The command-word list is the frozen 35-word list; commands outside it (`echo`, `printf`, …) are
   not command words by design — a token line with only such a word and no annotation is still a
   prose finding.
3. `exec -a NAME cmd` (option argument) is not resolved: the argument would be read as the command
   word. Not in the corpus; `sudo -E`, `env -i`, `time -p` are handled.
4. The counter's selftest needs `git` on PATH (H3 fixture); on a host without git every run is red,
   which is honest for a git-reading counter rather than a silent pass.
5. The corpus is read from the filesystem (frozen sha recorded above), not from git.
6. H3 cannot be expressed as a corpus text line (it is a file mode), so it is covered by the real
   repo fixture instead; H1/H2/H4 are covered by corpus lines plus function fixtures.
7. The SKILL.md gate-registry row naming `c73_tmp_v3.py` is part of the contract predicate but not
   this seat's write scope; the integrator adds it after promotion.

## Tooling

No tool was installed or upgraded; no pacman transaction was run (host-wide pause respected), and
no file was written to `~/.local/bin` or any PATH directory. Host tools used: `python3 3.14.8`,
`git 2.56.0`.

## Files changed

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter/c73_tmp_v3.py` (new; deliverable, sha256 above)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecC2Counter.md` (this report)

No other file was written; scratch was deleted.
