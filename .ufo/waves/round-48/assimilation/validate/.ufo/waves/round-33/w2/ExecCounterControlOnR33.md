# Round 33 C2 counter-control probe

Axis: freshness. Result: the current C2 counter passes the hollow-commit criterion.

## Hollow revision

Built in sandbox clone `/fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/clone` (at `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`) using detached worktree `/fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/hollow` based on `bc6c4a8d435473f3c30903210be30d9d6e3ef750`. Hollow commit: `3b3cb7e382ce64a48d241f2576d461cfde0e9381`.

The commit copies the four retained files from `0a0acfb1` under the unrelated `scripts/fixtures/unrelated/c2-ds4cc/` path: `sitemap.xml`, `magga/frostbite/index.html`, `magga/frostbite/classic/index.html`, and `magga/frostbite/remastered/index.html`. It adds a fabricated S099 row (not S065) at hollow `corpus/SOURCES.md:74` and an unrelated S099 mention at hollow `corpus/knowledge/sitemap-orphan-audit.md:184`; it does not add the exact round-33 evidence heading.

## Commands and observed results

- `mkdir -p /fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/tmp && export TMPDIR=/fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/tmp && unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/clone && git -C /fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/clone checkout -q 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0` — exit 0, no output.
- `git -C /fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/clone worktree add -q --detach /fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/hollow bc6c4a8d435473f3c30903210be30d9d6e3ef750` — exit 0, no output.
- Python `subprocess.run(['git', '-C', '/fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/clone', 'archive', '0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0', '.ufo/waves/round-33/sources/ds4cc-7fc6aa2f'], stdout=<temporary archive file>)` — exit 0; the four listed files were extracted and moved to the unrelated path.
- `git -C /fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/hollow add corpus/SOURCES.md corpus/knowledge/sitemap-orphan-audit.md scripts/fixtures/unrelated/c2-ds4cc` — exit 0.
- `git -C /fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/hollow -c user.name='Kake R33 Counter Control' -c user.email=kake-r33-counter-control@example.invalid commit -m 'Add hollow C2 counter-control fixture'` — exit 0; `[detached HEAD 3b3cb7e]`, 6 files changed, 803 insertions.
- `git -C /fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/hollow rev-parse HEAD` — exit 0; `3b3cb7e382ce64a48d241f2576d461cfde0e9381`.
- `export TMPDIR=/fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/tmp && unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && python3 -B .ufo/waves/round-33/criteria/counter_control_check.py --counter /fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/clone/.ufo/waves/round-33/c2_pin_count.py --repo /fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/clone --before 5777d5af --after 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0 --hollow 3b3cb7e382ce64a48d241f2576d461cfde0e9381` — exit 0:

```text
before 5777d5af -> met=0 exit=0
after  0a0acfb1b2e7 -> met=4 exit=0
hollow 3b3cb7e382ce -> met=0 exit=0
after=4 before=0 hollow=0
PASS: hollow scores below the after-value; the counter pins identity
```

## Evidence, risks, blockers

- Counter identity checks: `.ufo/waves/round-33/c2_pin_count.py:98-110` (retained path/mode/blob), `:112-129` (exact S065 row), `:131-136` (exact cited heading and identifiers); criterion decision: `.ufo/waves/round-33/criteria/counter_control_check.py:47-54`.
- Hollow commit evidence and copied bytes remain in `/fast/scratch/hyaku/kake-r33/w2/ExecCounterControlOnR33/` only. The only lane file written is this report.
- No build, lint, or broader test was run. This is a local synthetic revision check only; it does not establish current upstream or live-site state. No blockers; no tools installed.