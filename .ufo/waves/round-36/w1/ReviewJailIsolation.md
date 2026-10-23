# Round 36 W1 — ReviewJailIsolation: what the jail lets a jailed tool see

Defensive check of the measurement. I imported `jail()` unmodified from the public counter
(`.ufo/waves/round-36/sealed_count.py`, sha256 `88ec5914…342ff8e`) and ran a harmless read-only
probe inside it, in my sandbox — never the counter, never the sealed tree
(`/fast/scratch/hyaku/kake-r36/` untouched; its in-jail path probed only and returned `exists: false`).

## Method
- Runner mirrors `main()` exactly: `subprocess.run(jail(scratch, work) + ["/usr/bin/python3", "-B", probe], cwd=work, capture_output=True, timeout=60, env={})`, one shared scratch, simulated earlier-case leftovers in it (work dir + manifest + escaping body + tool file), fresh uuid names.
- Probe: existence/readability/listing of the assigned paths, `/proc` pid set, `/proc/1/cmdline`, parent-ppid, `connect(("127.0.0.1", 9))` with 1 s socket timeout. Read-only; no writes, no fetches.
- Commands (both exit 0, two independent runs, identical verdicts):
  `python3 probe/runner.py` → `EXIT: 0`; rerun captured to `probe-run2.txt` → `EXIT=0`.
- Sandbox evidence: `/fast/scratch/hyaku/kake-r36w1/ReviewJailIsolation/`
  `probe/probe_in_jail.py` sha256 `f4d0306…9ea7897`, `probe/runner.py` sha256 `8e7e5f0…d6a03ce`,
  full output `probe-run2.txt` sha256 `99c95bc…dcee9ad6`.
- No tool installs (bwrap 0.13.1 preinstalled; nothing added per operator directive).

## Visibility table (from inside the jail, pasted from probe-run2.txt)
| Path | Exists | Readable | Note |
|---|---|---|---|
| /home | no | — | not mounted at all |
| /fast | yes (chain only) | yes | contains exactly 1 entry per level (`scratch`→`hyaku`→…→scratch); pure bwrap mount chain to the bound scratch; siblings absent; `/fast/scratch/hyaku/kake-r36` → `exists: false` |
| /etc | no | — | absent |
| /usr | yes | yes | ro-bind, 9 entries |
| /tmp | yes | yes | empty tmpfs, 0 entries |
| scratch dir (=$HOME, =cwd parent) | yes | yes | rw-bind at host-identical absolute path |
| scratch dir's siblings | no | — | parent `…/tmp` lists exactly 1 entry (the scratch itself) |
| /proc/self | yes | yes | full self proc; own cmdline = `python3 -B <probe path>` |
| parent process cmdline | no (counter) | pid1 = bwrap | `/proc/1/cmdline` = bwrap argv (scratch/work/tool paths only); `PPid: 0`, `NSpid: 1`, `/proc` pids = `[1, 2]` — counter process invisible |
| network 127.0.0.1:9 | — | — | `ConnectionRefusedError: [Errno 111]` in <1 s; nothing connected in either run |
| key path `…/sealed/cases.json` | no | — | `exists: false` |
| lane repo `/home/vgpnk/Projects/shokunin/kake-shokunin` | no | — | `exists: false` |
| env | — | — | exactly `PATH=/usr/bin, HOME=<scratch>, LC_ALL, PYTHONDONTWRITEBYTECODE` (+PWD by python); no GIT_*, no key info |

## Verdicts on the three hidden items
1. **Key path: HIDDEN — verdict holds.** `/home` absent; direct probe `exists: false`. The key path/revision live only on the counter's argv, which sits outside the unshared pid namespace.
2. **Lane repository: HIDDEN — verdict holds.** `/home/vgpnk/...` and any `/fast` sibling invisible; only `/usr` + the scratch are mounted.
3. **Counter's command line: HIDDEN — verdict holds.** Pid namespace unshared: inside, `/proc` shows only bwrap (pid 1, PPid 0) and the tool (pid 2). `/proc/1/cmdline` is readable and names the scratch/work/tool/manifest paths — paths the tool already knows from its own argv — but never the key path, key revision, or counter flags. `/proc/1/environ` is readable but empty (counter launches bwrap with `env={}`).

## Cross-case visibility (same scratch dir): YES — earlier cases are visible
The counter runs all 28 cases sequentially against ONE `TemporaryDirectory` scratch and never
cleans between cases (`work.mkdir()` only; no rmtree). Observed inside the jail for case N+1
after case N: `earlier_case_d2f8a95d/earlier_manifest.json` listed and read
(`{"marker":"earlier-case-input"}`), `earlier_escape_01918f08` read (`earlier escaping body`),
`tool_file_sim.py` read. The scratch is rw-bound, so a tool can also WRITE notes a later case
reads ($HOME is the scratch). Impact: materialized *inputs* (bodies, id-rotated manifests) of
earlier cases leak to later cases, enabling case-order fingerprinting and within-run state
carry-over. The sealed `expect` data stays outside, ids/names are fresh per run, so this does
not hand the tool its expected findings — but "each case runs blind and fresh" is only true
per run, not per case. Cheap hardening if wanted: fresh scratch per case, or per-case tmpfs
subdir binding only `work`.

## Residual risk / not verified
- Jailed `/proc/1/cmdline` does reveal the host scratch path prefix (harmless, known via cwd).
- Network tested only as a 127.0.0.1:9 connect (assigned probe); no external egress attempted, so DNS/full-stack egress untested — though `--unshare-all` unshares net and the loopback connect fails.
- Exit code 2 of my first attempt (probe path outside the bind) reproduces by design why the counter must copy the tool into the scratch — measurement-affecting only if a future jail change drops that copy.
- No other seats' files touched; report file is the only lane write.
