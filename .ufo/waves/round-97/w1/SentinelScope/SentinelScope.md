# Round 97 — SentinelScope (confinement and scope attacks on both frozen counters)

Seat: SentinelScope-35. Lane tip read first: `git -C LANE rev-parse master` = `9e27ce0b2a8d168e032ab79ea11471b36eaceedf`.
Frozen digests verified before attack (`w1/SentinelScope/instrument-digests-verified.txt`): c97_index.py `8535150e…`, c97_reval.py `f3895a32…`, frozen/neg-lookup-table.py `898df9a2…`. All three match the freeze.
Tooling: none installed or upgraded. No pacman, no sysctl, nothing in ~/.local/bin.

## Summary

| item | result | command / receipt |
|---|---|---|
| (1) PATH shadow, both counters | **marker absent** (0 bytes) for both | `w1/SentinelScope/shadow-marker.txt`, `git-call-log.txt` |
| (2) `git replace` of README blob | **both counters ignore it** (met=true on the forged clone) | `w1/SentinelScope/replace-substitution.txt` |
| (3) C2 sandbox probes | 10 refused, several effectful/observational escapes admitted | `w1/SentinelScope/c2-sandbox-probes-b.txt`, `probe-*.py`, `probe-*.receipt.txt` |
| (4) LANE mutation during run | **none**: `git status --porcelain` identical before/after both counters | `lane-status-diff.txt` (`lane-status-unchanged`) |
| (5) misroot in fleet untracked | **0** | `misroot-scan.txt` |

Verdict line: `SENTINEL refused=10 escaped=in-tree-write,stdout-fd-shadow,listdir-stat-metadata,usr-prefix-read,kill0-ppid,symlink-create-in-tree misroots=0`

## (1) PATH shadow — marker absent

Wrapper: `w1/SentinelScope/orbit-driver.py` drove both counters with `PATH=<scratch>/shadow:$PATH`, where `shadow/git` appends `sentinel-git-marker` to a log before `exec /usr/bin/git`.

- C1 (`c97_index.py --revision 9e27ce0b…`) rc=0, `C1v97 … mismatches=0 met=true`. Log bytes = 0.
- C2 (`c97_reval.py --revision 9e27ce0b…`) rc=0, `C2v97 … met=true`. Log bytes = 0.

Positive control (the wrapper is live): `PATH=<shadow>:$PATH python3 -c "subprocess.run(['git','--version'])"` wrote 19 bytes to the log. `PATH=<shadow>:/usr/bin:/bin /usr/bin/git --version` wrote 0 bytes (absolute path bypasses the shadow, as it should).

Why the counters are safe: both build their own environment and pass `PATH=/usr/bin:/bin` (`c97_index.py` line 72, `c97_reval.py` line 332 and the scoring subprocess at line 353), and they call `GIT = "/usr/bin/git"`. A by-name `GIT = "git"` copy under the same shadow PATH also logged 0 bytes, because the counter's own env drops the shadow. Confirmed.

## (2) `git replace` substitution — both ignore it

Scratch clone `fx` (`git clone --shared`, toplevel asserted equal to the clone dir). Replace created for the README blob at the scored revision:

- original blob `5b0fc5eb5c9056ca9579dfddb1d8e656568c3d4d` (lane README)
- forged blob `973b9968fe69e770b9446e485b3cebf1c13e30e2` (rows naming `revalidation-exchange.md` with garbage prose, and an invented `yokawa-sitemaps.md` row) via `refs/replace/5b0fc5eb…`.

Mechanism is live: `git -C fx show 9e27ce0b…:corpus/README.md` returns the forged bytes (sha256 `e3096ae2…`), while `git -C fx --no-replace-objects …` and the lane return real bytes (`b2372d08…`). Note: plain `git show` in the clone follows the replace; the counters do not.

Result with the replace ref active, counters called as shipped (no env override):

- `c97_index.py --root fx --revision 9e27ce0b…`: `C1v97 … entries=84 indexed=84 unindexed=0 dangling=0 mismatches=0 met=true`, rc=0. A forged README would produce unindexed rows; the counter read the real bytes.
- `c97_reval.py --root fx --revision 9e27ce0b…`: `C2v97 … candidate=present hand=37/37 generated=104/104 heldout=56/56 forgeries_refused=7/7 positive=admitted mutants=14/14 survivors=none anti_table=ok population=ok seed=97 met=true`, rc=0.

Both counters pin `GIT_NO_REPLACE_OBJECTS=1` in their own env and do not trust ambient git config. Confirmed as stated in the freeze.

## (3) C2 sandbox — refused vs admitted

The sandbox is the `SANDBOX` string in `c97_reval.py`, extracted byte-for-byte (`sandbox-extracted.py`, sha256 `f4374ac4…`). Its semantics: audit hook; `open` is allowed only under the subject's root (`dirname(subject)`, which the counter sets to `work/tree/`) or under `sys.prefix`/`os` install prefix (`/usr`); `import` only for a fixed allowlist; `os.system`, `Popen`, `os.spawn*`, `os.posix_spawn`, `os.exec*`, `os.fork` denied.

Real layout (subject `tree/`, sandbox.py beside it), fresh receipts in `c2-sandbox-probes-b.txt`:

| probe | subject does | outcome |
|---|---|---|
| K_execv | `os.execv` into fresh python | **REFUSED** `process creation denied: os.exec` |
| L_fork | `os.fork` | **REFUSED** `process creation denied: os.fork` |
| A_outside_write | writes a marker outside `tree/` (sibling of tree) | **REFUSED** `open outside the subject tree` |
| O_sibling_write | writes a marker in `layout/` (sibling dir) | **REFUSED** `open outside the subject tree` |
| C_tmp_write | writes `/tmp/…` | **REFUSED** `open outside the subject tree` |
| I_os_open_outside | `os.open(O_CREAT)` outside tree | **REFUSED** `open outside the subject tree` |
| J_symlink_open_outside | symlink in tree → outside target, then open | **REFUSED** on open (`open outside`) — the symlink itself was created |
| H_import_posixsubprocess | `import _posixsubprocess` | **REFUSED** `import denied` |
| M_counter_read | `open(c97_reval.py)` to read the reference | **REFUSED** (`READ-REFUSED`) |
| N_etc_read | `open(/etc/hosts)` | **REFUSED** (`READ-REFUSED`) |

Refused distinct subjects: **10** (K, L, A, O, C, I, J, H, M, N). Earlier scratch probes agree (`os.exec`/`os.fork`/counter-file/`/etc/hosts`/sibling refusals repeat the same classes).

Admitted (the escape list):

1. **in-tree-write (effectful shadow, R96-4 carried gap, measured).** B_inside_write writes `tree/marker-inside`; rc=0; the file exists after the run. A candidate can therefore leave effectful side effects inside its own tree. The counter wipes `tree/` after each score, so this is not persistent, but it is admitted. Demonstrated verdict-neutral end to end: a candidate that writes `in-tree-marker-via-cand` into its tree and otherwise answers correctly scored `C2v97 … met=true` (rc 0) on probe commit `40af5788` (`probe-intree-candidate.receipt.txt`). The counter does not detect it.
2. **stdout-fd-shadow.** A subject writing `SHADOW-FD-MARKER` to stdout before its JSON was admitted (rc 0 from the sandbox). It corrupts the candidate's own output (the counter would reject non-JSON stdout), so it is self-defeating for a verdict but still an unconstrained output channel (`probe-fd-stdout.receipt.txt`).
3. **listdir-stat-metadata.** D_listdir_fleet lists `/home/vgpnk/Projects/shokunin` (58 entries) and E_stat_counter stats the counter file (size 29759) — both rc=0. Metadata disclosure of the lane and fleet roots; the counter file's bytes are still unreadable.
4. **usr-prefix-read.** G_usr_read reads `/usr/lib/python3.14/os.py` (41958 bytes) — admitted because `sys.prefix` is `/usr`, so the prefix rule admits every file under `/usr`. The rule is broader than the install dir it was meant to protect; on a layout where `sys.prefix` is `/` it would admit the whole filesystem. Not verdict-relevant here.
5. **kill0-ppid.** F_kill_ppid calls `os.kill(os.getppid(), 0)` — rc=0 (liveness probe to the counter's pid; no signal delivered, but not audited).
6. **symlink-create-in-tree.** J creates `tree/linkmarker → outside`; the symlink is created (symlink creation is not audited), only the open through it is refused.

Not run (named, not claimed): reads via `runpy`/`spec_from_file_location` of the counter file (expected to hit the `open` audit event; inference, not measured).

Effectful-shadow is the R96-4 carried gap. It was measured, not fixed (as instructed). The seat's own rule is unchanged: the sandbox has no effectful-shadow defense for in-tree writes or the stdout channel.

## (4) LANE not mutated during runs

`git -C LANE status --porcelain` before and after each counter run (C1 shadow run, C2 shadow run, final re-run): identical. Recorded in `lane-status-diff.txt` (`lane-status-unchanged`) and the pre/post files in scratch (deleted; the diff result is the receipt). Pre-existing dirty state at tip (not mine): `M SKILL.md`, untracked round-97 controls, dispatch files, `w1/`.

## (5) Misroot check

`git -C /home/vgpnk/Projects/shokunin status --porcelain` (read-only):

```
 M .scratch/run15-kernel.py
 M .scratch/run15-state.json
 M .ufo/l0-questions.md
?? w4lines.txt
```

Untracked: `w4lines.txt` only (content: numeric line markers; `kake=0 r97=0 round-97=0`). **misroots=0.** Observation (tracked, not misroots, out of scope): `.scratch/run15-state.json` names `KakeR97` as an orchestrator label and `.ufo/l0-questions.md` has 35 kake mentions — both are the orchestrator's own tracked state, not untracked misroots.

## Incident (disclosed)

ConnectorScope-23 ran `rm -rf /fast/scratch/hyaku/kake-r97` at ~18:14Z, which deleted this seat's scratch tree mid-run (and sibling seat trees). I recreated the scratch tree and a fresh clone, re-derived every receipt from frozen bytes, and reran the counters. Nothing frozen, no LANE tree byte, no sysctl and no MANIFEST was touched by that incident. ConnectorScope-23 acknowledged the misread (their rm reached the shared round parent, not their seat dir). Pre-wipe scratch probes that I re-ran are noted above; the receipts in this directory are the post-recreate runs.

Also discarded: a first real-layout probe batch with a glob bug (`c2-sandbox-probes.txt`, "no subject file" lines) was deleted as superseded by `c2-sandbox-probes-b.txt`.

## Route to L1

- R96-4 (effectful-shadow) remains open: in-tree writes and stdout-fd writes are admitted by the C2 sandbox; the C1 counter has no sandbox at all (it runs git in-process only, so the shadow analysis above is its whole surface).
- Routed defect candidate (new): the C2 sandbox prefix rule admits every file under `sys.prefix` (`/usr`), wider than the stdlib it names.
- Routed defect candidate (new): metadata disclosure (`listdir`, `stat`, `kill 0`) on outside paths is not gated.
- No frozen instrument was patched. No repair was made.

## Verdict

SENTINEL refused=10 escaped=in-tree-write,stdout-fd-shadow,listdir-stat-metadata,usr-prefix-read,kill0-ppid,symlink-create-in-tree misroots=0
