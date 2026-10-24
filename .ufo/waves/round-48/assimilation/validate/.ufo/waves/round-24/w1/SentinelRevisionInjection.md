## Verdict

**P2 — operability / trust-boundary defects confirmed in the frozen round-23 runners.** An option-shaped `--revision` is accepted in `--revision=<value>` form and is concatenated into the `git show` argument before revision validation. Git parses the injected option: `--output` can truncate/write outside the clone when its destination path exists (or a suitable worktree symlink exists), and `-O` reads an external orderfile. Separately, C2 executes `scripts/canonical_audit.py` bytes from the selected revision as Python with the caller's privileges; its temporary directory protects only its inputs, not the process. Malformed child output can also traceback.

No lane production files or runner files were changed. The only lane write is this report.

## Findings

### P2 — Raw revision option injection reaches `git show` before validation (C1 and C2; operability)

**Evidence.** `show()` constructs one `git show` argument as `f"{revision}:{path}"` (`measure_c1.py:36-38`, `measure_c2.py:31-33`). Both `main()` functions call `rev-parse`, then call `show()` with the unvalidated `args.revision`, and only afterwards test the `rev-parse` return code (`measure_c1.py:103-110`; `measure_c2.py:113-120`). C1's first affected read is the population at line 105. C2's first affected reads are the population and validator at lines 115-116. The regular separate-argument form `--revision --output=...` is rejected by argparse, but `--revision=--output=...` is accepted and reaches `show()`.

Clone and baseline:

```text
Command: git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r24-SentinelRevisionInjection-clone
Observed initial clone HEAD: f7de3ab4e9f030a15a857a5a08631bd8e690f436
Observed base object type: commit

Command: python3 /tmp/kake-r24-SentinelRevisionInjection-clone/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-SentinelRevisionInjection-clone --revision HEAD
Observed: rc=0; accepted=17; total=17; failing=[]; stderr empty.

Command: python3 /tmp/kake-r24-SentinelRevisionInjection-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-SentinelRevisionInjection-clone --revision HEAD
Observed: rc=0; accepted=12; total=12; failing=[]; stderr empty.
```

**Write probe.** With the outside destination's parent directories absent:

```text
Command: git -C /tmp/kake-r24-SentinelRevisionInjection-clone show --output=/tmp/kake-r24-SentinelRevisionInjection-PHBs/pwn:.ufo/waves/round-23/c1-population.json
Observed: rc=128; stderr: fatal: could not open '/tmp/kake-r24-SentinelRevisionInjection-PHBs/pwn:.ufo/waves/round-23/c1-population.json' for writing: No such file or directory
strace: openat(AT_FDCWD, "/tmp/kake-r24-SentinelRevisionInjection-PHBs/pwn:.ufo/waves/round-23/c1-population.json", O_WRONLY|O_CREAT|O_TRUNC, 0666) = -1 ENOENT (No such file or directory)

Command: python3 /tmp/kake-r24-SentinelRevisionInjection-clone/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-SentinelRevisionInjection-clone --revision=--output=/tmp/kake-r24-SentinelRevisionInjection-PHBs/pwn
Observed: rc=2; stdout: {"error": "revision or frozen population unreadable", "revision": "--output=/tmp/kake-r24-SentinelRevisionInjection-PHBs/pwn"}; stderr empty.
```

I then created the matching `pwn:.ufo/waves/round-23` directory under scratch and put `PRECIOUS-A` in the population target. The same C1 command returned rc 2 with the same generic unreadable-revision JSON, but git replaced that file with a 23,626-byte `git show` patch: first line `commit f7de3ab4e9f030a15a857a5a08631bd8e690f436`; `contains PRECIOUS-A: False`. The corresponding C2 command (`.../measure_c2.py --root <clone> --revision=--output=<scratch>/pwn`) also returned rc 2 and wrote 23,626 bytes to each existing `pwn:.ufo/waves/round-23/c2-population.json` and `pwn:scripts/canonical_audit.py` target. Thus the failure status does not undo the output side effect.

I also committed two symlink fixtures **only in the sandbox clone**, at commit `0b842d71adb94d2cbe92b61e6770130fd38f20fb` (parent: the frozen base): `escape:.ufo -> /tmp/kake-r24-SentinelRevisionInjection-PHBs/external/ufo` and `escape:scripts -> /tmp/kake-r24-SentinelRevisionInjection-PHBs/external/scripts`. `git ls-tree -r --name-only 0b842d71adb94d2cbe92b61e6770130fd38f20fb -- escape:.ufo escape:scripts` returned both paths. With those fixture symlinks present:

```text
Command: python3 /tmp/kake-r24-SentinelRevisionInjection-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-SentinelRevisionInjection-clone --revision=--output=escape
Observed: rc=2; stdout: {"error": "revision, frozen population or validator unreadable", "revision": "--output=escape"}; stderr empty.
Outside target: /tmp/kake-r24-SentinelRevisionInjection-PHBs/external/scripts/canonical_audit.py
Observed: exists=True; size=624; first line: commit 0b842d71adb94d2cbe92b61e6770130fd38f20fb
```

The analogous C1 call wrote to `.../external/ufo/waves/round-23/c1-population.json` (624 bytes; same first line). These files were only in `/tmp`.

**Read probe.** `-O` also reaches Git's orderfile option. The real runner invocation with `--revision=-O/tmp/kake-r24-SentinelRevisionInjection-PHBs/rd` returned rc 2 and an unreadable-revision JSON, while `strace` showed the argument-derived orderfile opened read-only. For a direct trace including the bytes read:

```text
Command: strace -f -yy -s 128 -e trace=openat,read -o /tmp/kake-r24-SentinelRevisionInjection-PHBs/strace-order-read-detail.txt git -C /tmp/kake-r24-SentinelRevisionInjection-clone show -O/tmp/kake-r24-SentinelRevisionInjection-PHBs/rd:.ufo/waves/round-23/c1-population.json HEAD
Observed: rc=0; stdout_len=424; stderr empty.
Trace: openat(AT_FDCWD</tmp/kake-r24-SentinelRevisionInjection-clone>, "/tmp/kake-r24-SentinelRevisionInjection-PHBs/rd:.ufo/waves/round-23/c1-population.json", O_RDONLY) = 3</tmp/kake-r24-SentinelRevisionInjection-PHBs/rd:.ufo/waves/round-23/c1-population.json>
Trace: read(3</tmp/kake-r24-SentinelRevisionInjection-PHBs/rd:.ufo/waves/round-23/c1-population.json>, "README.md\n", 8192) = 10
```

This confirms Git reads outside-repository data as an option value. It does **not** demonstrate exfiltration of that content: the C1 runner consumes/captures Git output and the file bytes above only affect Git's orderfile handling. `git show --pathspec-from-file=...` and `git show --git-dir=...` were rejected in probes (`fatal: unrecognized argument: ...`).

**Impact / exploit path.** A caller that supplies an option-shaped revision using the equals form can make Git process options before the runner rejects the revision. A writable output target with the suffix Git appends is enough to truncate/write a file outside the repository; the sandbox symlink fixture demonstrates the same with paths present in a commit/worktree. This is conditional on the caller passing the crafted revision and the target directory/symlink being available. The write is Git's show/patch output, not attacker-chosen bytes. The runners' later rc 2 is not a safety control because `git show` has already performed the write/read.

**Smallest fix for `scripts/receipt_replay.py`.** Resolve first, fail before any `show()`, and then pass only the resolved object ID to every later `show()` call. Use rev-parse's option terminator and validate the result as a full SHA-1/SHA-256 object ID, e.g.:

```python
resolved = subprocess.run(
    ["git", "-C", root, "rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}"],
    capture_output=True, text=True, check=False,
)
object_id = resolved.stdout.strip()
if resolved.returncode != 0 or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", object_id):
    return input_error
# Only now: show(root, object_id, fixed_or_population_path)
```

Tested with Git 2.56.0: `git rev-parse --verify --end-of-options 'HEAD^{commit}'` returned the full commit ID; `git rev-parse --verify --end-of-options '--output=/tmp/kake-r24-SentinelRevisionInjection-PHBs/guarded^{commit}'` returned rc 128 and `fatal: Needed a single revision`, and `/tmp/.../guarded` was not created. Crucially, move all `show()` calls **after** that check; adding `--end-of-options` only to the later reads is not enough if an earlier raw-revision `show()` remains.

### P2 — C2 executes selected-revision Python; `TemporaryDirectory` is not a sandbox (C2; operability)

**Evidence.** At `measure_c2.py:83-98`, the runner writes the validator bytes read from the selected revision to a `TemporaryDirectory`, writes page/manifest inputs there, then invokes `[sys.executable, "-B", <temp>/canonical_audit.py, ...]` with `capture_output=True`, `text=True`, `timeout=60`, and `check=False`. The call specifies neither `cwd` nor `env`, so it inherits the caller's working directory and environment. The temporary directory is private and cleaned up, but the child process is not confined to it.

I changed only `scripts/canonical_audit.py` in the sandbox clone to a benign probe that wrote its cwd, argv, a synthetic non-secret environment variable, and the mode of its script directory to a marker in scratch, then printed JSON. I committed it at `eb51d0a8812944f0dd878ea87b52c289071ca74e` and ran:

```text
Command: python3 /tmp/kake-r24-SentinelRevisionInjection-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-SentinelRevisionInjection-clone --revision eb51d0a8812944f0dd878ea87b52c289071ca74e
Invocation cwd: /tmp/kake-r24-SentinelRevisionInjection-PHBs
Environment supplied: SENTINEL_PROBE=synthetic-nonsecret-marker
Observed: rc=1; accepted=4; total=12; stderr empty (the intentional probe result differed from committed receipts).
Marker: {"argv": ["/tmp/kake-r23-c2-g27vyy4l/canonical_audit.py", "--manifest", "/tmp/kake-r23-c2-g27vyy4l/s/manifest.json", "--json"], "cwd": "/tmp/kake-r24-SentinelRevisionInjection-PHBs", "script": "/tmp/kake-r23-c2-g27vyy4l/canonical_audit.py", "sentinel": "synthetic-nonsecret-marker", "tmpMode": "0o700"}
Observed after runner: validator tempdir exists=False.
```

The probe establishes both sides of the boundary: mode `0o700` and automatic cleanup protect the temporary input directory, while the child can write outside it and sees caller-provided environment/cwd. The base validator itself was inspected; the source grep found its `subprocess` matches in its self-test helper, not a network-fetch API. This does not make executing arbitrary selected-revision Python safe.

**Impact / exploit path.** Anyone able to cause the counter to measure an untrusted revision can put executable Python in that revision's validator. It runs as the counter's user, with inherited environment, filesystem access, and network capability; the tempdir only contains the materialized script and replay inputs. The test used only a synthetic marker and did not use or inspect live secrets.

**Smallest remediation.** Treat the measured validator as code, not receipt data: either enforce an explicit trusted/reviewed-revision boundary before execution, or run it under an actual OS sandbox/low-privilege identity with only the temporary inputs mounted, no sensitive environment, and network disabled if not required. Setting `cwd=tmp` and a minimal `env` are useful defense-in-depth but are **not** containment for malicious Python (absolute paths and network remain available). If `receipt_replay.py` preserves this re-run behavior, the same trust boundary applies.

### P2 — Malformed validator output causes uncaught tracebacks (C2; operability)

`measure_c2.py:99-105` catches `json.JSONDecodeError` but not text decoding errors, then assumes `actual["result"]` is a mapping containing `"verdict"`. I exercised both cases only in the sandbox clone:

```text
Invalid UTF-8 case command:
python3 /tmp/kake-r24-SentinelRevisionInjection-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-SentinelRevisionInjection-clone --revision 7ac8701ff96b44f08aa6bd2c9741495196c23e85
Observed: rc=1; traceback=True; stderr tail:
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte

Wrong-shape JSON case command:
python3 /tmp/kake-r24-SentinelRevisionInjection-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-SentinelRevisionInjection-clone --revision a31661eb84e32a84171cae4ac29d0159ccca26dd
Observed: rc=1; traceback=True; stderr tail:
  File "/tmp/kake-r24-SentinelRevisionInjection-clone/.ufo/waves/round-23/measure_c2.py", line 105, in check
    return problems, actual["result"]["verdict"]
TypeError: list indices must be integers or slices, not str
```

The first test validator wrote `b"\\xff\\n"`; the second printed the valid JSON value `[]`. These revisions were sandbox-only. This is a concrete way a broken or adversarial validator prevents a clean counter result.

**Smallest fix.** Capture validator stdout as bytes or use an explicit decode policy inside the handled block; turn decode/JSON failures into a normal rejected row/input result. Before indexing, require `actual` to be a dict, `actual["result"]` to be a dict, and `actual["result"].get("verdict")` to be an accepted string. Return exit 1/2 rather than allowing decoding, `TypeError`, or `KeyError` exceptions to escape.

## Checked and held

- Frozen base and clone baseline: initial clone HEAD matched `f7de3ab4e9f030a15a857a5a08631bd8e690f436`; C1 and C2 both accepted all base controls (17/17 and 12/12 respectively).
- Confirmed the option-like revision reaches Git in `--revision=<value>` form; direct `git show` `openat` was `O_WRONLY|O_CREAT|O_TRUNC`. Confirmed a pre-existing target was overwritten and a sandbox-only symlink path wrote outside the clone.
- Confirmed `-O` opens and reads an external file. Did not claim the orderfile bytes were exfiltrated. `--pathspec-from-file` and `--git-dir` probes were rejected by `git show`.
- Tested the suggested `rev-parse --end-of-options` form with both a valid revision and an injected option; valid revision resolved, injected value failed, no output file appeared.
- Confirmed C2's private tempdir mode and cleanup with the benign probe; exercised inherited cwd/environment and malformed subprocess output in clone-only revisions.
- Live lane walk found no colon-named entries or symlinks. All symlink/validator fixtures and commits remained in `/tmp/kake-r24-SentinelRevisionInjection-clone`; final clone HEAD after probes was `a31661eb84e32a84171cae4ac29d0159ccca26dd`. The round-23 scripts in the lane were not changed.
- Tool versions observed: Git 2.56.0; Python 3.14.8; `strace` was already installed. No tools were installed or updated. No builds, lint, formatters, or unrelated tests were run.
- `scripts/receipt_replay.py` was absent from the lane's `scripts/` listing at inspection, so this report specifies the guard without editing or anticipating the integration.

## Limits

- All mutation probes were confined to the no-hardlinks clone and `/tmp/kake-r24-SentinelRevisionInjection-PHBs`; no lane Git/jj/index state or domain source tree was mutated. No live secrets were supplied. No public pages were fetched.
- The `--output` write is conditional: the composed destination must be creatable (pre-existing parent path) or a worktree symlink must direct it to an existing writable destination. The demonstrated output was Git's patch text. The revision value is caller input; these probes do not establish that the normal production caller supplies untrusted strings.
- The validator probe demonstrates execution under the current user's inherited context, not behavior against actual live credentials. The actual base validator source was not found to expose a network-fetch API; the risk is from executing changed/untrusted validator code, not a claim that the frozen base validator is malicious.
- This is a sentinel review only: no admission or integration is claimed.