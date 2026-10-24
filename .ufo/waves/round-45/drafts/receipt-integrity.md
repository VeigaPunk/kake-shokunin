source: S133 (Python 3.15.1 documentation, `subprocess` — `CompletedProcess.returncode`) and `.ufo/waves/round-44/w2/ReviewCounterContract.md` (round-44 counter-contract review, defects 1(a)–(c)); lane bytes `.ufo/waves/round-44/c44_audit.py` (sha256 `8ee2c8bf9333…2d0c75`) and `.ufo/waves/round-44/c44_count_v5.py` (sha256 `5cedaa3b9f91…7672bc`)
verified-at: 2026-10-24 (kake round 45) — the three v1 defect sites re-read at the frozen hashes; the v2 gate read at `.ufo/waves/round-45/c45_audit.py` (round-45 build artifact, uncommitted at writing); the round-44 probe outputs are quoted from the review, not re-run by this entry
recheck: `python3 -B .ufo/waves/round-45/c45_matrix.py --stage before` and `--stage after` — rerun on any counter, driver or receipt-format change; a cohort that certifies a witness or not-met row whose receipt fails the validity gate is a regression of this entry

# Receipt integrity — bind a receipt to the run that wrote it

A verification driver reads receipts by path. If it never binds the file to the invocation it just
made, the gate certifies whatever bytes sit at that path: a receipt from a counter that errored, a
receipt written when the tool was missing, or a receipt planted by an earlier run. The file is then
evidence of *some* run, not of *this* one, and "witnessed" becomes a statement about a directory.

## Three defect classes, each reachable in the round-44 instrument

All three were found by reading the frozen v1 driver against the frozen counter, and each was
demonstrated on row shapes the driver itself produces (`.ufo/waves/round-44/w2/ReviewCounterContract.md`,
2026-10-23). Class count: **3** — `grep -cE '^\*\*\([abc]\) ' .ufo/waves/round-44/w2/ReviewCounterContract.md`
prints `3` (2026-10-24).

1. **Counter-error receipt (exit 2).** The counter writes a receipt and then exits 2 on
   `CannotEvaluate` (`.ufo/waves/round-44/c44_count_v5.py:1114-1119`, `finish(2)`), and that path is
   reachable *after* the class-run entries are recorded (`:1108`), so the receipt can carry a real
   class divergence. The v1 driver records the exit (`c44_audit.py:157`, `exit=code`) and never
   reads it: `semantic_witness` (`:63-66`) and `expectation_ok` (`:69-83`) consult only `met` and
   `caughtBy`. Evidence pointer: `ReviewCounterContract.md:41-55` — probe A prints
   `semantic_witness: True` / `expect witnessed (build 3/3 met): True` on an exit-2 row.
2. **Tool-absent receipt (exit 1, `note: "tool absent"`).** When the counter cannot read the tool it
   sets `cand = None` (`c44_count_v5.py:1031-1034`), marks every run `equal: False` with
   `candExit: "tool absent"` (`:1078-1080`), records `note = "tool absent"` (`:1113`) and exits 1
   (`:1120`). Every class key then appears in the derived `caughtBy`, so the control is "witnessed"
   although nothing ran. The v1 driver never propagates `note` (`c44_audit.py:157-160`). Evidence
   pointer: `ReviewCounterContract.md:57-71` — probe B prints the same two `True` lines on an
   exit-1 `note='tool absent'` row.
3. **Stale planted receipt (no write at all).** `run_counter` opens the receipt path whenever it
   parses, regardless of `p.returncode` (`c44_audit.py:54-61`). A counter killed by a signal writes
   nothing, and receipts planted beforehand are certified. Evidence pointer:
   `ReviewCounterContract.md:73-96` — end-to-end run with a SIGKILL-ing fake counter and planted
   `tools/ctl1.json` + `build-{1,2,3}.json` reports `ok=True`, exit 0, while the summary *records*
   `"exit": -9` on the row and all three build rows.

Why the exit code is the right field to gate: `subprocess` documents `returncode` as "Exit status of
the child process", with "A negative value `-N` indicates that the child was terminated by signal `N`
(POSIX only)" (`CompletedProcess.returncode`, https://docs.python.org/3/library/subprocess.html,
opened 2026-10-24). A signal death (`-9`, `-15`) is therefore distinguishable from the counter's own
contract of 0 (met) / 1 (not met) / 2 (cannot evaluate), which is what makes `exit in {0, 1}` a
meaningful gate rather than a guess.

## The binding rule (driver v2)

A receipt earns witness or not-met credit only if it is bound to the invocation that produced it.
Implemented in `.ufo/waves/round-45/c45_audit.py` as one `receipt_validity()` predicate (`:68-86`),
fed by a manifest written **before** any counter is spawned (`run-manifest.json`
`{started_ns, counter_sha256, nonce}`, `:223-227`; v2 creates the cohort directory itself and
refuses a non-empty one):

- **exit gate** — counter exit in `{0, 1}`; anything else is class `counter_error`;
- **note gate** — `receipt["note"] != "tool absent"`; else class `tool_absent`;
- **counter binding** — `receipt["counterSha256"] == sha256(invoked counter)`; else `stale_receipt`;
- **run window** — receipt `st_mtime_ns` inside `[started_ns - 1 s, finish_ns + 1 s]`
  (`MTIME_EPS_NS = 1_000_000_000`); else `stale_receipt`;
- **seed recorded** — a receipt without a `seed` is `stale_receipt`.

An invalid row joins `errors[]` under its named class; `expectation_ok` fails if any control row or
any build row is invalid (`:115`); `--expect not-met` counts only valid `met is False` rows (`:105`).
The v1 CLI, row fields, summary fields and exit codes are unchanged, so the honest cohort's
certification does not move.

## Do-nothing reachability

The cheapest control that skips the claimed work is exactly these three receipt shapes: never run the
tool (tool absent), die after the interesting run (counter error), or reuse an earlier run's receipt
(stale planted). Under v1 each reaches the declared after-state — `ok=True` with a "witnessed"
control — without the counter doing the work, so a v1-style instrument is do-nothing-reachable and
its certification says nothing about the tool. Under the binding rule none reaches it: each is refused
with its named class, so the after-state (`invalid_accepted=0`, three distinct rejection classes)
cannot be reached by skipping the work — it is reachable only by running the counter and gating what
it wrote. The instrument's own do-nothing lookalike (v2 with a gate removed) must also fail the after
predicate; the driver's `--selftest` carries one invalid-receipt assertion per class so that removal
is caught locally.

*Opinion (marked as opinion):* the run window is the load-bearing clause. Exit, note and counter-sha
are cheap corroboration that a receipt is well-formed and from the right code, but only the window
makes it evidence of *this* invocation; a gate with exit+note+sha alone still accepts a byte-valid
receipt left over from a previous run.

## Counts

- 27 controls in the round-44 claim cohort —
  `ls .ufo/waves/round-44/verification/claim/after-final/tools/ | wc -l` → `27` (2026-10-24).
- 3 invalid fixture classes plus 1 honest control — `ls .ufo/waves/round-45/fixtures` →
  `counter-error  honest  stale-planted  tool-absent` (2026-10-24).
- Round-44 claim receipt witness split, re-derived with
  `python3 -c "import json;d=json.load(open(P));rows=d['rows'];print(sum(1 for r in rows if r['met'] is False and r['classCaught'] and not r['legacyCaught']), sum(1 for r in rows if r['met'] is False and r['classCaught'] and r['legacyCaught']), sum(1 for r in rows if r['met'] is True))"`
  over each file:
  - `P=.ufo/waves/round-44/verification/claim/after-v5.json` → `22 1 4` (witnessed 23/27, `ok=False`)
  - `P=.ufo/waves/round-44/verification/claim/after-final/after-v5.json` → `26 1 0`
    (witnessed 27/27, build 3/3, `ok=True`)

  The frozen C2(c) sentence ("22 class-only + 1 mixed + 4 met") re-derives from the first file; the
  second, later receipt re-derives 26/1/0. Two files named `after-v5.json` exist under
  `verification/claim/`; a citation of "the round-44 claim receipt" must name which one.

## Registry status (dependency, at writing)

`source:` cites S133, which is not yet in this lane's registry: the round-45 wave lands that row.
Check at writing: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `132`;
the last row id is `| S132`; `grep -c 'S133' corpus/SOURCES.md` → `0` (2026-10-24). The L1 lands the
S133 row (Python subprocess docs, kind `docs`, tier A for child-process exit-status semantics) with
this entry; until then this `source:` line names an id the registry does not carry.
