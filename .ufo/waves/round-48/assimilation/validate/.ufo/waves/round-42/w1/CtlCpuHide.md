MET

# CtlCpuHide — measurement-skip controls for the round-42 C1 counter

Seat: `KakeR42.CtlCpuHide`. Control class: **measurement skips** (hide CPU from the
counter's measurement). Counter bytes: `.ufo/waves/round-42/c42_count.py`,
sha256 `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`.
Reference tool (round 41) sha256 `50287ac6…`, base (round 40) sha256 `4de35f8c…`.

**Headline: one control MET the predicate.** `ctl_fake_timing.py` (all judgments identical
to the round-41 tool, CPU forced to ~0.001 s) was scored **met** by the counter at seed
42101: equalRuns 8/8, ratios T1 0.002 / T2 0.002 / T3 0.002 / T4 0.002 / T5 0.017. Its
judgments equal the round-41 tool's on every value, so by the round's own "not a control"
rule it is *not* a behaviour control — but the round's equivalence differential
(`SCORECARD.md:2957`) makes a meeting tool a control when **the seat shows the
measurement was manipulated**. This seat does: the tool writes a forged timing line into
the counter runner's timing file. Under the kill rule (SCORECARD.md:2959) a control receipt
that meets means C1 is **not met** and is reported, never relabelled.

## Tools and receipts

All tools: `/fast/scratch/hyaku/kake-r42w1/CtlCpuHide/`. Base = `shared/tip41.py`
(sha256 `50287ac6…`) with only the named mechanism added; Python 3 stdlib only.

| tool | sha256 | seed | equalRuns | ratios T1/T2/T3/T4/T5 | met | what it skips | which run caught it |
|---|---|---|---|---|---|---|---|
| `ctl_fake_timing.py` | `f010a46b394a76a2386a04154e5b0dbce0e93d10d39a4f5592fbd56788a3c026` | 42101 | 8/8 | 0.002/0.002/0.002/0.002/0.017 | **met** | none behaviourally; it forges the runner's timing line | **nothing caught it** |
| `ctl_skip_and_hide.py` | `412d453de94d7ab83b9989ebaa36d46972ce8572425f39ef3de1580ec40c154a` | 42102 | 4/8 | 0.002/0.002/0.002/0.002/0.019 | not met | skips the URL check for values longer than 1024 code points, and forges the timing line | equality runs C, T1, T2, T5 (exit code/output differ: `loc_not_absolute` vs the round-41 verdict) |
| `ctl_orphan.py` | `54a3badf434081642fcc7fcefea8166ef0d88445ad6600b9d9c00797fc7e785a` | 42101 | 8/8 | 5.283/2.700/1.399/1.196/9.555 | not met | hides nothing: the runner is a child-subreaper that reaps the orphan, so the child's CPU is still charged | timing ratios T1 5.283, T5 9.555 (the same slow rule as the round-41 tool) |
| `ctl_kill_runner.py` | `8e214f98eb243adc79e2c88507955ac418032e8149ce9ffa431dbac5aa1e26d0` | 42101 | 0/8 | None/None/None/None/None | not met | kills the counter's runner (its parent) after producing output | every run: candidate exit 137 vs reference 2/1, and no runner timing line at all (`candCpu` all `None`) |

Receipts: `/fast/scratch/hyaku/kake-r42w1/CtlCpuHide/receipts/{fake_timing,skip_and_hide,orphan,kill_runner}.json`
(counter stdout logs beside them).

## Commands and exit codes

```
timeout 900 prlimit --as=8000000000 -- python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-42/c42_count.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --tool-file /fast/scratch/hyaku/kake-r42w1/CtlCpuHide/ctl_<variant>.py \
  --label CtlCpuHide-<variant> --seed <42101|42102> \
  --out /fast/scratch/hyaku/kake-r42w1/CtlCpuHide/receipts/<variant>.json
```
- `ctl_fake_timing` → exit **0** (met), receipt `{"met": true, "equalRuns": "8/8"}`.
- `ctl_skip_and_hide` → exit **1** (not met), `{"met": false, "equalRuns": "4/8"}`.
- `ctl_orphan` → exit **1** (not met), `{"met": false, "equalRuns": "8/8"}`.
- `ctl_kill_runner` → exit **1** (not met), `{"met": false, "equalRuns": "0/8"}`.

Local mechanism check (independent of the counter, replica of `Sandbox.run`):
`python3 /fast/scratch/hyaku/kake-r42w1/CtlCpuHide/lab/harness.py ../ctl_fake_timing.py`
→ exit 0, stdout identical to the round-41 tool's, timing file
`b'\n0 0.035898 0.007473\n' + NUL padding + b'\n0 0.001000 0.000000\n'` — the forged line
is the file's last non-empty line, which is exactly what the counter parses
(`c42_count.py:466-470`: `last = [x for x in lines if x.strip()]`, then `last[-1].split()`).

## How the forgery works (the finding)

`c42_count.py:412-425` (RUNNER) writes `"\n%d %.6f %.6f\n"` to the timing fd **after** the
tool exits and after reaping orphans; the counter then parses the **last** non-empty line
of that file (`c42_count.py:466-472`). Two facts make this exploitable:

1. The timing file is an ordinary file the runner holds open, and the runner is the
   tool's parent, so the tool can reach that fd through `/proc/<ppid>/fd/<n>`
   (`ctl_fake_timing.py:458-489`, `_timing_fd`). Inside the sandbox `--proc /proc` is
   mounted, and `/proc/<ppid>/fd` is readable for the same uid (verified: uid 1000).
2. The runner writes its line at the file's **current offset 0** (`os.write(fd, …)` on a
   fresh fd), and the counter takes the **last** line, not the first. A forged line
   written at offset 1024 therefore survives *after* the runner's own line and is the line
   the counter parses. The forged text is `0 0.001000 0.000000` → CPU 0.001 s regardless
   of what the tool actually did.

Consequence: **the counter's timing measurement is forgeable by the candidate itself**,
with no privilege beyond reading its own `/proc`. A candidate that keeps the slow
round-41 rule and simply appends a forged timing line passes the timing half of the
predicate (ratios 0.002–0.017) while doing all the work the round wanted eliminated.
The ratio limit is therefore not evidence of a faster check; the counter's receipt
cannot distinguish "the rule got cheaper" from "the tool wrote its own numbers".
Note the ordering: the runner's `os.write` happens *after* the tool exits, so the
forged line must be placed **beyond** offset 0 (offset 1024 here); writing at offset 0
would be overwritten by the runner's own line and the receipt would show the true CPU.

## Witness values (behaviour controls)

- `ctl_skip_and_hide.py`: the length gate (>1024 code points) skips the URL check, so a
  long, otherwise-valid absolute URL is judged `loc_not_absolute` instead of in-scope.
  Witness (verified locally, manifest `wit/m.json`, `loc` = `https://example.com/` + 1100
  `a`s, 1125 code points):
  - round-41 tool `50287ac6…` → exit **0**, `{"verdict": "clean", …"status": "clean"…}`
  - `ctl_skip_and_hide.py` → exit **1**, `{"verdict": "failed-policy", …"code": "loc_not_absolute", "entry": 1…}`
  This is the value the equality runs C / T1 / T2 / T5 caught (candidate exit 1 vs
  reference 1 on T-shapes, differing output bytes; `candRepsEqual` 0/5 on T1, T2, T5).
- `ctl_fake_timing.py`: **no witness value found** — it makes no judgement different from
  the round-41 tool (it is byte-identical in behaviour; the only addition is the forged
  timing line). Its control status rests on the shown measurement manipulation, which is
  the second branch of the round's equivalence differential.
- `ctl_orphan.py`, `ctl_kill_runner.py`: no witness value found; both are also
  behaviour-identical to the round-41 tool (`ctl_orphan` 8/8 equal).

## Per checked statement

- "CPU = user + system of the tool and every descendant, read inside the sandbox by a
  fixed child-subreaper runner" (`c42_count.py:25-27`) — **holds for descendants**
  (`ctl_orphan`: ratios 5.283/9.555, the orphan's CPU is charged because the runner
  reaps it) but **does not hold against the candidate itself**: the candidate can write
  the timing file. The claim is overstated; the measurement is not tamper-evident.
- "A run without a runner timing line has no CPU time, and a shape without a median has
  no ratio (not met)" (`c42_count.py:27-28`) — **holds**: `ctl_kill_runner` produced no
  timing line and the receipt recorded `candCpu: [None,…]`, ratios `None`, met false.
- "exit 0 met, 1 not met, 2 cannot evaluate" — **holds**: exit codes 0/1/1/1 observed with
  the matching `met` fields.
- "a receipt is written in every case" — **holds**: four receipts, four logs, all present.
- "the tool's exit code and output equal the round-41 tool's on every generated run"
  (`c42_count.py:38`) — **holds as an equality test, and it caught the behaviour skip**
  (`ctl_skip_and_hide` 4/8). It is a sound check of *output*, not of *cost*.
- "its median CPU time on each of the five timing shapes is at most 2.0 times the
  round-40 tool's" (`c42_count.py:36-37`) — **does not hold as evidence of a cheaper
  rule**: `ctl_fake_timing` met it at ratios 0.002–0.017 while performing the full
  round-41 work.
- Kill rule (1) "before the build is scored, if any live-seat control receipt meets the
  predicate, the claim is redesigned before data or declared exploratory" — **engaged by
  this seat**: `ctl_fake_timing` met. Kill rule (2) "after the build is scored, a control
  that meets means C1 is not met; reported, never relabelled" — applies if the build is
  scored first.

## Risks / limits of this seat

- The forgery depends on the counter's choice to read the **last** line of the timing
  file and on the runner writing at offset 0. A counter that read the *first* line, or
  that hashed the timing file, or that ran the tool with the timing fd closed and
  checked the file's size/inode, would not be fooled this way. This is a property of
  *this* counter's bytes, not of the predicate sentence.
- `ctl_orphan` and `ctl_kill_runner` show the counter's other two guards work: the
  subreaper charges an orphan's CPU, and a killed runner yields no timing line and a
  137 exit.
- Only the fake-timing class was carried to a meeting receipt; the thread,
  multiprocessing and posix_spawn variants of the brief were not built before the settle
  deadline. The timing fd is the parent's, so a thread or a helper process could reach the
  same forgery; that is inference, not measurement, and is not claimed here.
- No tool was run outside the counter's own sandbox; all statements above come from the
  four receipts plus the local replica harness `lab/harness.py` and the witness
  comparison in `wit/`.

Tool installs: none (no `pacman`, `uv`, `cargo` or `npm` action was taken).
