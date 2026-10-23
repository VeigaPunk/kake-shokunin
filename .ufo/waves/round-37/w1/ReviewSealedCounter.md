# ReviewSealedCounter — round-37 C1 counter review (no key)
I did not touch /fast/scratch/hyaku/kake-r37/ or anything under it, and did not run the C1 counter with the real key. No installs.
Target: `.ufo/waves/round-37/sealed_count.py` sha256 `2ebb39b5…f0e3` (matches SCORECARD), diffed against `.ufo/waves/round-36/sealed_count.py` sha256 `88ec5914…ff8e`.
Sandbox `/fast/scratch/hyaku/kake-r37w1/ReviewSealedCounter/`: `counter.py` (9ef6f722…6cd2) is the target with only KEY_SHA256, CASES=7 and TARGET=7 changed by `make_key.py` (59576c19…73bb). Dummy key `dummy_key.json` (967895e8…194f) has 7 cases, K1–K7. `tools/mini.py` (e02f5d54…fdf) is a small contract tool. `tools/probe.py` (8e6b1291…0f58) dumps what the jail exposes. `logwrap.py` (8cbafe0c…6288) saves each jailed run's stdout. `measure.py` (a3250077…f38f) records exit code, wall time and peak memory.
Shared prefix for the commands below: `cd $S && TMPDIR=$S/tmp`. Each command is `timeout 300 python3 -B counter.py --tool-file tools/<T>.py --key-file dummy_key.json`, or `python3 measure.py <T>`.

## Findings by severity
**M1 Medium — files with the same base name collide; this is a regression from round 36.** At lines 106-115, `names` is keyed by the base name (`base = rel.rsplit("/",1)[-1]`, line 110). Round 36 keyed it by the full relative path (r36:117-125). If a case ships both `robots.txt` and `../robots.txt`, the last file written wins. Both checks are then rewritten to the same fresh name (probe run02: `"robots": "9407…"` and `"../9407…"`). The inside check now points at a file that does not exist.
Reproducer: case K2 with `mini` gives `K2-collide False`. `mini` run directly on the original layout (`direct/k2/w/m.json`) gives exactly the sealed expectation (exit 2, `[b check_invalid]`). Fix: key `names` by `rel`, as round 36 did, and rewrite on an exact `robots == rel` match.
**M2 Medium — subdirectories are never created, but the docstring at lines 12-13 says the directory part is kept.** Lines 111-114 always write the file flat into `work/<fresh>` or `work.parent/<fresh>`. Lines 129-133 rewrite `sub/robots.txt` to `sub/<fresh>`, so a valid check under a subdirectory always resolves to a missing file.
Reproducer: case K3 gives `K3-subdir False` (probe run03 shows `"robots": "sub/e3ec…"`). `mini` on `direct/k3/w/m.json` gives the sealed expectation (exit 1, `[b exposed]`).
[INFERENCE] M1 and M2 are latent with the current key, because the private reference scores 28 of 28. Any future key edit that hits either one makes the case unpassable for every tool, and the counter does not say why.
**M3 Medium — a case with zero runs passes for any present tool.** At lines 215-234, `ok = tool_path is not None` holds when `case["runs"] == []`. Reproducer: `tools/junk.py` (prints `not a report`) scores 1 of 7, and that one is `K6-empty-runs True`.
Fix: refuse the key with exit 2 when any case has no runs, or when the number of cases is not CASES. I did not verify that the sealed key has no empty-run case (no key).
**M4 Medium — the declared coverage is overstated for rules the materializer cannot express.** `materialize` (lines 104-138) only writes regular files and one regular manifest. It cannot create symlinks, directories, unreadable files or a non-regular manifest path.
- In (g), "manifest path that is not a regular file" and "unreadable" cannot be in any case.
- In (f), "after resolving symlinks" cannot be in any case.
This contradicts SCORECARD's "Every case of a bullet carries one check per listed rule of that bullet". It matches MutRefPass, where the "symlink and prefix containment" mutants survive (ctl/MutRefPass.md).
**L1 Low/Medium — the jail is writable and shared across runs.** At line 167, `--bind scratch scratch` is read-write, and at line 168 `HOME` is set to scratch. A tool can keep state across every run and case and can rewrite its own file. Probe run06 found 5 earlier manifests that it had copied into `$HOME/.loot`.
The contract's "no writes" is not enforced. The docstring at lines 161-164 ("sees … the current run, the tool file") is overstated. The prefix `kake-r37-c1-` (line 209) also lets a tool detect that it is running under the counter.
I found no key leak: the jail shows no /home, its pid 1 command line is bwrap's own argv with no key path, and the environment is clean. Fix: bind scratch read-only, bind only the current `case_dir` read-write, and set `HOME=/tmp`.
**L2 Low/Medium — a tool can crash the counter, and every crash exits 1, which is the "not met" code.** Reproducer: `python3 measure.py chmod`, where the tool runs `chmod $HOME 0o500`. The next `case_dir.mkdir()` (line 221) raises `PermissionError`, giving exit 1 with no JSON receipt. Likewise `--tool-file /nonexistent` gives `FileNotFoundError` and exit 1. The docstring (lines 31-32) promises exit 2 for "cannot evaluate". Fix: the read-only bind from L1, plus a top-level `except Exception` that prints the error JSON and exits 2.
**L3 Low — stdout is captured with no size limit.** At lines 226-229 there is no cap. `measure.py huge` printed 2 GiB in 2.1 s, and the counter peaked at 4122 MiB of memory (bytes plus the decoded string). At that rate, 20 s is roughly 40 GB, enough to kill the counter by running out of memory. This cannot produce a false pass. Fix: stream into a file and fail the run above a cap such as 64 MiB.
**L4 Low — the fresh-name and fresh-id guarantee is partial** (SCORECARD: "replaces every check id and robots file name"). A `robots` value whose file name is not in `files` keeps the author's literal name: probe run06 saw `"SECRET-LABEL-expect-invalid.txt"`. `raw` runs (lines 117-120) keep the original ids and names. Fix: replace unmatched file names with fresh names too.
**L5 Low — the key-visibility check looks only at the path** (line 191). I committed the key at `scripts/cases_copy.json` in sandbox repo `$S/repo`. Running `counter.py --root repo --revision HEAD --key-file dummy_key.json` measured it (exit 1, passed 5), whereas `KEY_PATH` gives exit 2. The docstring at lines 17-18 ("nothing measured can be a copy of the key") is stronger than this check. Fix: compare every blob id from `git ls-tree -r` with `git hash-object` of the key.
**Info.**
- Line 219: `proc, idmap = None, {}` is dead code, since both are reassigned at lines 224-232.
- Line 100: `str(reason)` treats null and `"None"` as the same reason.
- Lines 226-228: stdin is inherited and there is no `--new-session`. TIOCSTI injection is blocked on this host (`dev.tty.legacy_tiocsti = 0`), but not on a host where it is 1.

## Checked and correct (observed)
- Repeated ids keep one fresh id through `setdefault` (line 128): `K4-repeat True`.
- A case passes only if every run passes, and stops at the first failing run (lines 215-233): `K5-multi True` with `mini`; with `junk` it fails at run 1 and only 1 jailed run happens.
- A tool missing at the revision scores 0, including the empty-run case: `toolPresent False`, `passed 0`, exit 1.
- With the key at `KEY_PATH` at the revision, the counter refuses with exit 2.
- Projection on (check, reason) matches the contract. These cases neither crash nor pass:
  - unhashable check ids `[1]` and `{"a":1}`, through `repr` at lines 96-99 (`tools/unhash.py`);
  - non-object findings (`unhash`);
  - non-list findings at lines 152-153 (`tools/nonlist.py`);
  - nesting at depths 500, 990, 2000 and 100000 (`tools/deep*.py`).
- An in-process bisect showed `json.loads` raises RecursionError (caught at line 147) at depth 52189, and `project` never failed below that depth.
- Timeout (`counter1.py`, single-case key `dummy_key1.json`, `tools/hang.py`, which ignores SIGTERM and forks a `setsid` grandchild): the run returned at 20.09 s and failed, with no jailed process left.
- `$S/tmp` was empty after every run, including the chmod crash.

## Not verified
- Anything about the sealed key's content, including whether M1, M2, M3 or M4 actually affect the current 28 cases.
- Behaviour under a key larger than about 85 MiB.
- Other Python versions than 3.14.8 (bwrap 0.13.1).
- No other verification gaps. The 7-case `python3 measure.py hang` run completed in the background: exit 1, 120.1 s (6 jailed runs × 20 s), passed 1 of 7 (only `K6-empty-runs`, the M3 case), counter peak RSS 21 MiB. Afterwards `pgrep -af ReviewSealedCounter` found no process left.
