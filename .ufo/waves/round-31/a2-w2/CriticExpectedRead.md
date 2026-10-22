# CriticExpectedRead — round 31 attempt 2, wave 2 (falsify), C1 N5 guarded expected.json read

Seat: KakeR31a2.CriticExpectedRead (critic, leaf). Axis judged: operability. Attack target: `read_expected` in
`scripts/citing_set_selftest.py` at fde133ab48086bb9a06911b4ab045e2ad9086347 (lines 384-407; caller `run_case` lines 528-532).

## Result

I could not falsify N5. All 11 requested and extra inputs, plus one simulated race, are refused or accepted
as claimed. Every refusal message names `expected.json`, nothing blocks, and no descriptor leaks. I found
one wording defect only: refusals for "missing" and "no read permission" are labelled "(symlinks are refused)".

## Setup and commands (all in sandbox /fast/scratch/hyaku/kake-r31/a2-w2/CriticExpectedRead/, TMPDIR=<sandbox>/tmp)

1. `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin <sandbox>/clone && git -C <sandbox>/clone checkout -q fde133ab48086bb9a06911b4ab045e2ad9086347` gave exit 0 and HEAD fde133ab48086bb9a06911b4ab045e2ad9086347.
2. `python3 -B <sandbox>/probe_read_expected.py <sandbox>/clone <sandbox>/run1` gave exit 0 and `{"summary": "all HOLDS"}`.
   Raw output: <sandbox>/probe-fde133a.jsonl. Python 3.14.8, run as uid 1000 (not root, so mode 000 really denies the read).
3. `sha256sum` of the runner was 5371530d93ecb218b4607fb37de810fe7b7b2db869c65c8b65988b2f04c0ce6c at both fde133a and the lane tip
   92235a0578b04458c5eb96c966f82fa03593130e (`git show 92235a0:scripts/citing_set_selftest.py | sha256sum`), so the result also holds at the tip.

Probe method: the probe imports the runner module and builds each input as `<case>/expected.json`. It calls `read_expected` under a 5 s
SIGALRM, so a blocking open raises instead of hanging. It counts `/proc/self/fd` before, after one call, after 500 more
calls and after `run_case(case_dir, None, None, None, parent)`. For refusals `run_case` returns before it needs the gate, so the
probe also checks that `row["reason"]` equals the `read_expected` error and that `passed` is false.

## Table

| input | result (read_expected, then run_case reason) | verdict |
|---|---|---|
| regular file, exactly 1048576 bytes (valid JSON padded with spaces) | returned 1048576 chars; `expectation_entries` parses it | HOLDS (accepted at the limit) |
| regular file, exactly 1048577 bytes | `expected.json must be at most 1048576 bytes` | HOLDS |
| empty file | returns "" (not refused by `read_expected`); `run_case`: `expected.json is not valid JSON: Expecting value: line 1 column 1 (char 0)` | HOLDS (refused one layer up) |
| invalid UTF-8 (byte 0xff) | `expected.json is not UTF-8: 'utf-8' codec can't decode byte 0xff in position 26` (UnicodeDecodeError is a ValueError, so run_case catches it) | HOLDS |
| directory named expected.json | `expected.json must be a regular file` (O_RDONLY open on a directory succeeds, then the fstat type check refuses it) | HOLDS |
| FIFO, no writer | `expected.json must be a regular file`, returned at once with no block (O_NONBLOCK) | HOLDS |
| symlink to regular file | `expected.json unreadable (symlinks are refused): [Errno 40] Too many levels of symbolic links` | HOLDS |
| dangling symlink (extra) | same ELOOP refusal | HOLDS |
| symlink to FIFO (extra) | same ELOOP refusal, no block | HOLDS |
| missing file | `expected.json unreadable (symlinks are refused): [Errno 2] No such file or directory` | HOLDS, wording defect W1 |
| file mode 000 (no read permission) | `expected.json unreadable (symlinks are refused): [Errno 13] Permission denied` | HOLDS, wording defect W1 |
| 1048577-byte file with `os.fstat` patched to report size 0 (simulates growth between fstat and read) | the post-read cap fires: `expected.json must be at most 1048576 bytes` | HOLDS (second guard, lines 399 and 402-403, is live) |

Descriptor count was 6 at all four points for every row, and also before and after the patched-fstat row: no leak on any success
or error path, including 500 repeated calls per input. The `finally: os.close(descriptor)` at line 400-401 covers the
type and size raises, and `os.fdopen(..., closefd=False)` prevents a double close.

## Findings

- W1 (wording, operability, minor): line 391 attaches "(symlinks are refused)" to every `OSError` from `os.open`.
  So ENOENT and EACCES tell the operator a symlink was refused when none exists. The errno text that follows is
  correct, which keeps the error diagnosable. Smallest correction: say "symlinks are refused" only on ELOOP, e.g.
  `"expected.json unreadable: %s" % exc` plus a symlink note when `exc.errno == errno.ELOOP`. This is not a containment defect.
- The empty file is not refused by `read_expected` itself but by `json.loads` in `run_case` (lines 533-537), so the claim holds at the
  runner level. A caller that used `read_expected` alone would get "" back.
- The docstring (lines 74-76) matches the observed behaviour.

## Not verified

- Base runner f1ffb81: it has no `read_expected` (its `run_case` used `expected_file.read_text`, base line 423), so the probe
  fails on import there (`AttributeError: ... EXPECTED_MAX_BYTES`, exit 1, <sandbox>/probe-f1ffb81.err). I did not build a
  base-shaped probe, so this report gives no independent evidence that the base was weak on these inputs.
- Character or block device nodes (they need mknod or root), a real concurrent writer race (only simulated via patched fstat), and
  TOCTOU between `case_dir.is_symlink()` (line 521) and the open of the parent path component.
- I did not run the full `main()` or the gate end to end for the accepted 1048576-byte case. That row checks `read_expected` and parsing only.
- I did not re-run the C1 counter, the hostile selftest or the P4 spec (other seats own these).

## Deliverables (sandbox)

- /fast/scratch/hyaku/kake-r31/a2-w2/CriticExpectedRead/probe_read_expected.py (probe)
- /fast/scratch/hyaku/kake-r31/a2-w2/CriticExpectedRead/probe-fde133a.jsonl (raw output)

Installs: none. Lane writes: this report only.
