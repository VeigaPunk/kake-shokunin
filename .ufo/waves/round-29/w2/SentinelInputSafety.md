# C2 hostile-input probe: `scripts/base_path_audit.py`

- Axes: operability (judged); freshness (not exercised).
- Target: commit `7697990cbca20291f3b0367b8ff4220e93b38b03`; source SHA-256 `e32646159b652710be4053bbdb001c3d11929ef63b055b7f57545231ac6965aa`.
- Verdict: **holds** for the hostile inputs listed below. Severity: none observed. No remediation indicated.

Command run (runner exit 0):

```text
TMPDIR=/fast/scratch/hyaku/kake-r29/w2/SentinelInputSafety/tmp python3 -B /fast/scratch/hyaku/kake-r29/w2/SentinelInputSafety/run_hostile_inputs.py
```

Each case ran the target with exit 2 using this command pattern (the case name selected its separate manifest):

```text
strace -f -qq -e 'trace=%network,%file,write,pwrite64,writev,ftruncate,fallocate' -o /fast/scratch/hyaku/kake-r29/w2/SentinelInputSafety/traces/<case>.strace timeout --kill-after=1s 6s python3 -B /fast/scratch/hyaku/kake-r29/w2/SentinelInputSafety/clone/scripts/base_path_audit.py --manifest /fast/scratch/hyaku/kake-r29/w2/SentinelInputSafety/cases/<case>/manifest.json
```

| Input | Exit | Reason | Time |
|---|---:|---|---:|
| Symlinked page file | 2 | `input_invalid` | 0.064 s |
| Symlinked parent directory | 2 | `input_invalid` | 0.067 s |
| FIFO page | 2 | `input_invalid` | 0.063 s |
| `/dev/zero` as absolute page path | 2 | `input_invalid` | 0.059 s |
| `../victim.html` traversal path | 2 | `input_invalid` | 0.062 s |
| `/etc/passwd` absolute page path | 2 | `input_invalid` | 0.079 s |
| 2 MiB + 1 byte page | 2 | `input_invalid` | 0.062 s |
| 1 MiB + 1 byte manifest | 2 | `input_invalid` | 0.064 s |
| Non-UTF-8 page | 2 | `input_invalid` | 0.061 s |
| Directory used as page | 2 | `input_invalid` | 0.063 s |

All stdout results were JSON with `verdict=could-not-evaluate`, zero pages/references checked, and an `input_invalid` finding; stderr was empty. No timeout or traceback. Across all 10 traces: zero network syscalls, zero write-mode file opens, zero non-stdout writes, and zero filesystem mutation syscalls. FIFO trace confirms it was opened `O_NONBLOCK` and the child exited 2 (`traces/fifo-page.strace:602-607`).

Evidence: bounded limits and reads at `scripts/base_path_audit.py:55-58,228-239,242-275`; relative-path, no-follow, nonblocking, and regular-file checks at `:278-317`; strict UTF-8 page decode and rejection at `:677-694`; input result and exit handling at `:653-663,687-694,742-752`. Run records: `/fast/scratch/hyaku/kake-r29/w2/SentinelInputSafety/results.json`, SHA-256 `637942f0767ddcd4d979681c52065d625836fc527a22a2d6c7d27a303315cfe1`.

Limit: the device case supplied `/dev/zero` as an absolute manifest path (rejected before opening); no special device node was created inside the sandbox. No tool was installed or updated.
