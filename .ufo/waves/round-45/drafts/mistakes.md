# Round 45 — lesson draft: the receipt-trust mistake class + Gate skeleton

Seat: `kake-r45.ScribeLessonMistakes` (wave 1, scribe). **Draft only.** The L1 lands
`corpus/lessons/round-45.md`; this seat wrote no corpus file, no `SCORECARD.md`, no
`corpus/SOURCES.md`, and made no git/jj commit, push, publish or deploy. Files written by this
seat are exactly: this draft, `.ufo/waves/round-45/w1/ScribeLessonMistakes.md`, and scratch files
under `/fast/scratch/hyaku/kake-r45/ScribeLessonMistakes/`.

Axes: **operability** (the gate's decision procedure) and **freshness** (the provenance of every
cited byte). No round judgment, claim admission, or score is made here; the canonical Rust judge
owns that.

---

## 1. Proposed `## Mistakes` section for `corpus/lessons/round-45.md`

Numbering continues the lane counter: `corpus/lessons/round-42.md` ends at 6, `round-43.md` at 11
(`corpus/lessons/round-43.md:94`), `round-44.md` at 13 (`corpus/lessons/round-44.md:53`), so the next
entry is **14**. The class label keeps the lane's prose style used in entries 12–13; a
vocabulary-tagged variant is offered in §3 for the L1's choice.

### 14. Instrument trusted receipts without binding them to the run

**Class:** instrument trusted receipts without binding them to the run — the witness gate
certified whatever bytes sat at a receipt path, never checking that *this* invocation wrote
*these* bytes, so "witnessed" was a statement about a directory rather than about a measurement.

**Evidence.** The frozen v1 driver `.ufo/waves/round-44/c44_audit.py` (sha256
`8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75`) recorded the counter's exit
code on every row and never read it: `run_counter` returns `p.returncode` (`:54-61`), `score()`
stores it as `exit=code` (`:157`), and neither `semantic_witness` (`:63-66`) nor `expectation_ok`
(`:69-83`) consults `exit`, `note`, the receipt's mtime, or its `counterSha256`. Three HIGH
defects with that one root cause were found by the round-44 wave-2 reviewer and are preserved
verbatim at `.ufo/waves/round-44/w2/ReviewCounterContract.md` defects **1a** (`:41-55`), **1b**
(`:57-71`) and **1c** (`:73-96`):

- **1a** — a counter-error (exit 2) receipt that already recorded a class divergence is a witness
  (`semantic_witness: True`; `expect witnessed (build 3/3 met): True`);
- **1b** — a `note: "tool absent"` receipt (exit 1, every run `equal: false`) is a witness on every
  class key although nothing ran (the same two `True` lines);
- **1c** — a receipt already on disk is loaded even when the invocation wrote none: a
  SIGKILL-ing counter plus pre-planted `tools/ctl1.json` and `build-{1,2,3}.json` certified
  `ok=true`, exit 0, while the summary *records* `"exit": -9` on the row and on all three build
  rows.

Re-derived independently on today's bytes by this seat (command and verbatim output in
`.ufo/waves/round-45/w1/ScribeLessonMistakes.md`, §"Decisive commands"): all three reproduce on the
frozen driver — exit-2 row → `semantic_witness: True`, `expect witnessed: True`; `note='tool absent'`
row → `True`/`True`; exit `-9` row → `True`/`True`. The frozen predicates read neither `exit`, nor
`note`, nor any timestamp, nor any counter-byte pin.

**Captured-by.** Kill rule (2) required receipts to re-derive **at their recorded seeds** but said
nothing about binding a receipt to the run that produced it, so it certified seed-binding while
leaving run-binding unchecked — the round-44 C1 kill rules as frozen (`SCORECARD.md:3459-3462`:
"(2) Any witness that is a timing-only failure, a v4-corpus divergence, or a counter error → not a
witness") and the capability row's "per-row receipts re-derive at their recorded seeds"
(`SCORECARD.md:218`) both admit a receipt whose bytes came from some other run at some other seed.
Kill rule (2) should have required **run-binding**, not just seed-binding: a receipt counts only if
the invocation that just ran produced it. [INFERENCE] The round-45 C1 kill rule (2) (`SCORECARD.md:3662`,
"every receipt cited re-derives from committed bytes at its recorded inputs") is the same class of
rule and is still not a run-binding rule: it constrains what a receipt may be *cited* for, not
which invocation wrote it.

**Fix.** Driver v2 `.ufo/waves/round-45/c45_audit.py` (sha256
`5a342e29c7e872d992cfedc26de849c010d197bb82162e007a61a55d915c7051` at this seat's read) applies one
receipt-validity gate, `receipt_validity(receipt, exit_code, mtime_bounds, counter_sha)`
(`:68-86`), before any witness or not-met credit: counter exit in `{0, 1}` else class
`counter_error`; `note != "tool absent"` else class `tool_absent`;
`receipt["counterSha256"] == sha256(invoked counter)` else class `stale_receipt`; a seed present
else `stale_receipt`; and the receipt's `st_mtime_ns` inside the driver's own run window
`[started_ns − 1 s, finish_ns + 1 s]` else `stale_receipt`. The driver creates its cohort
directory itself and refuses a non-empty one (`:200-203`), and writes `run-manifest.json`
(`{started_ns, counter_sha256, nonce}`) before any counter is spawned (`:223-227`). Invalid rows
earn neither witness nor not-met credit (`row_valid` / `valid_rows` / `not_met_rows`,
`:96-105`), and the requested build count is pinned (`:108-111`).

**Able to fail.** The frozen counting command is
`python3 -B .ufo/waves/round-45/c45_matrix.py --stage before|after`; the *before* stage must record
`invalid_accepted=3` and the *after* stage `invalid_accepted=0`, `rejections_named=3`,
`honest_witnessed=27`, `honest_build_met=3` (`SCORECARD.md:3653-3658`). **The matrix stages have
not been run by this seat and no matrix receipt exists yet, so this row's able-to-fail evidence is
a placeholder.** What this seat did run, in scratch only, is the same comparison directly over the
three committed invalid fixture classes (`.ufo/waves/round-45/fixtures/{counter-error,tool-absent,stale-planted}/`):

| fixture class | frozen v1 (`c44_audit.py`) | driver v2 (`c45_audit.py`) |
|---|---|---|
| `counter-error` | `ok=True`, exit 0, row `exit=2` credited as witness | `ok=False`, exit 1, row `error=counter_error` |
| `tool-absent` | `ok=True`, exit 0, row `exit=1` credited as witness on all 21 keys | `ok=False`, exit 1, row `error=tool_absent` |
| `stale-planted` | `ok=True`, exit 0, row `exit=-9` credited as witness | `ok=False`, exit 1, row `error=counter_error` |
| honest control (real counter, one row) | — | `ok=True`, exit 0, `witnessed=1/1` |

Verbatim outputs are in the seat report. **Not yet demonstrated by this seat:** the honest
27-control cohort under v2 (`honest_witnessed=27`, `honest_build_met=3`) — the heavy run is
`ExecRegressionHonest`'s and the committed receipt
`.ufo/waves/round-45/verification/honest-regression/after-v5-v2.json` did not exist at this seat's
read; the v1 baseline it must equal is `.ufo/waves/round-44/verification/claim/after-final/after-v5.json`
(`witnessed 27`, three build rows `met: true`).

**Residual risk / limits (for the L1).** Two limits are visible in the artifacts and are recorded
here rather than resolved:

1. The landed `stale-planted` fixture does **not** exercise the run-window (mtime) branch of the v2
   gate. The fixture's counter is SIGKILLed before writing anything and the matrix plants the
   pre-existing receipts only in the *before* stage
   (`.ufo/waves/round-45/c45_matrix.py:235`, `if args.stage == "before" and fixture_name ==
   "stale-planted"`), so under v2 there is no receipt at all and the row is rejected as
   `counter_error` (exit `-9` ∉ `{0,1}`), not as `stale_receipt`. The mtime-window branch is
   exercised only by the driver's own selftest assertion
   (`c45_audit.py:162`, `receipt_validity(receipt, 1, (111, 90, 110), "counter-sha") == (False,
   "stale_receipt")`). [INFERENCE] The three *named* rejection classes in the after stage therefore
   come from two sources, not three: the control rows give `counter_error` (counter-error fixture),
   `tool_absent` (tool-absent fixture) and `counter_error` again (stale-planted fixture), and the
   third distinct name `stale_receipt` comes from the fixture **build** rows, whose receipts carry
   the real counter's `counterSha256` while the invoked counter is the fixture's fake one.
   Rejecting the stale-planted case does not by itself show that the mtime or sha binding does the
   claimed work (`CriticC1Predicate.md:38-40`).
2. The v1 driver resolves its per-control receipts and build receipts from `dirname(--out)`
   (`c44_audit.py:130-132,174-175`), so every leg sharing an output parent overwrites the previous
   leg's receipts — the contamination recorded as round-44 lesson entry 13
   (`corpus/lessons/round-44.md:53-68`). Driver v2 removes the footgun for its own legs (it
   creates the cohort directory and refuses a non-empty one), but the round-44 **receipts already
   committed** under `verification/claim/after-final/` were produced by v1 and must be read with
   that history in mind.

---

### 15. (candidate row, for the L1's decision) The same class, recurring in-round: a claim leg bound to a receipt's numbers but not to the receipt

**Class:** instrument trusted receipts without binding them to the run — recurrence, this round, in
the freshness claim rather than the audit gate.

**Evidence.** The frozen C2(c) leg states that "the round-44 claim receipt's 27 witnessed controls
re-derive as 22 class-only + 1 mixed + 4 met" (`SCORECARD.md:3681-3689`) and fixes the MET tuple as
`after=(4/4, false, 22/1/4)` (`SCORECARD.md:3697-3701`). The receipt the claim names is the final
round-44 claim receipt `.ufo/waves/round-44/verification/claim/after-final/after-v5.json`
(`SCORECARD.md:3602-3611`), sha256
`9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1`, `witnessed: 27`. Re-derived by
this seat from the committed bytes:

```text
after-final/after-v5.json  → {"witnessed":27,"split":{"class_only":26,"mixed":1,"met":0,"other":0}}
after-v5.json (earlier)    → {"witnessed":23,"split":{"class_only":22,"mixed":1,"met":4,"other":0}}
```

So `22/1/4` re-derives from the **earlier** 23-witness receipt
`.ufo/waves/round-44/verification/claim/after-v5.json` (sha256
`2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902`) and not from the receipt the
sentence names. Independently reported by three wave-1 seats: `ExecWitnessSplit.md:7` ("The
measured split is 26 class-only, 1 mixed, 0 met, and 0 other … **Fail against the item's expected
22/1/4 split**"), `ScoutRoutedLedger.md:6` ("**FAIL** on frozen C2(c) arithmetic"), and
`CriticC2Scope.md:9` (the counterexample is "already committed": substituting the earlier receipt
satisfies the numeric split while making the stated final-receipt leg false).

**Captured-by.** The same kill rule (2) gap as entry 14: a receipt's *numbers* were checked without
checking that they came from the receipt the sentence names. A leg that says "the round-44 claim
receipt" must bind the tuple to that receipt's identity (path + revision + digest), not merely to
values that some round-44 receipt happens to carry.

**Fix.** Any repaired C2(c) must name the receipt (path, revision, sha256) it re-derives from and
require the split that receipt actually carries — for the final receipt that is `26/1/0` with
`other=0` — and the runner must derive the split from that identity rather than accept a cached
value (`CriticC2Scope.md:104-108`).

**Able to fail.** The two committed receipts are the red state: the jq above is red against the
stated tuple on the receipt the claim names and green on the receipt it does not name. This seat ran
that comparison; it did **not** run `python3 -B .ufo/waves/round-45/c45_freshness.py` (the frozen
counting command, absent at this seat's read), so no after-state is claimed here.

*This row is a candidate only: the item assigned this seat one mistake row (entry 14). Entries 14
and 15 are the same class and may be landed as one row by the L1; entry 15 is separable because its
evidence and its fix are in the freshness claim, not the audit gate.*

---

## 2. Proposed `## Gate` section for `corpus/lessons/round-45.md` (skeleton)

The round-45 lesson skeleton already states the required shape: "one row per opened/rejected
source, labeled per new row, with URL or repo path, access date, and a ≤25-word located quote. At
least one reject decision is required this round — round-44 closure observation." The decisions
themselves are carried by `kake-r45.ScribeSourcesGate`'s draft
`.ufo/waves/round-45/drafts/sources-gate.md`; this section is the table skeleton and the row
labels, and it does not restate that draft's decisions as this seat's own.

Table header uses `ID` and `Decision` so a reject spot-check can find the decision column.

| ID | URL | Accessed | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S133 | https://docs.python.org/3/library/subprocess.html | accessed 2026-10-24, HTTP 200, 208,624 bytes, sha256 `eceda6f6…e5bdf0dd` | "A negative value -N indicates that the child was terminated by signal N (POSIX only)." (§Popen Objects → `Popen.returncode`, paragraph 3; 15 words) | **admit** — grounds the receipt-gate exit-status reading (kind `docs`, tier A, status `queued`); decision text in `drafts/sources-gate.md` |
| S134 | https://stackoverflow.com/questions/24139389/unable-to-find-out-what-return-code-of-11-means (read via the Stack Exchange API) | accessed 2026-10-24, API read HTTP 200, 723-byte JSON (a plain HTML GET of the same URL answers HTTP 403) | "A negative return code usually means that the process was terminated by a signal." (accepted answer by `sth`, first paragraph; 14 words) | **reject** — the durable point is already carried by the tier-A primary S133, and its `-11 is SIGSEGV` claim is a signal-number mapping the opened primary does not make; flip: a tier-A POSIX or Python `signal` source naming signal 11 as SIGSEGV is opened, and the answer becomes an illustrative example; decision text in `drafts/sources-gate.md` |
| — (candidate only, no id) | https://stackoverflow.com/a/5631819 | accessed 2026-10-24 via the Stack Exchange API (answer id 5631819, score 363, accepted; the HTML page answers HTTP 403) | "A negative value -N indicates that the child was terminated by signal N (Unix only)." (13 words) | **candidate only, no decision** — a second non-primary source on the same topic, opened by this seat while cross-checking S133/S134. It adds no authority beyond S133 (it restates the same documentation passage, with the older "Unix only" wording instead of the current "POSIX only"), so it is not proposed as a Gate decision; `kake-r45.ScribeSourcesGate` carries the single reject decision for this round |

**Wave-1 rejections reported by seats, and where each belongs.** No wave-1 seat reported a *source*
rejection other than the one above. The wave-1 rejections that exist are of two other kinds, and
this draft places them accordingly rather than inside the Gate table:

- **claim-level rejection (belongs in `## Mistakes`, entry 15 above):** the frozen C2(c) tuple
  `22/1/4` does not re-derive from the receipt the claim names — `ExecWitnessSplit.md:7`,
  `ScoutRoutedLedger.md:6`, `CriticC2Scope.md:9`.
- **instrument-level rejections (belong in the SCORECARD measurement append, not in a lesson Gate):**
  the routed-defect ledger's non-C1 items (`ScoutRoutedLedger.md:28-33`: the `--expect blind`
  universal-v4-blindness reading, the unpinned build count, the input-error exit code, the
  `witnessedByClass` nit, the duplicate-TSV-name nit) are defects of the frozen v1 driver that
  driver v2 does not claim to fix, except where noted. They are not source decisions and must not
  be logged as Gate rejects.

**Gate row count for the round.** 1 admit (S133) + 1 reject (S134) + 1 labeled candidate-only row
that carries no decision. The round-44 closure observation (at least one screened reject with its
reason) is satisfied by S134.

**Registry note for the L1.** `corpus/SOURCES.md` currently ends at S132 (132 rows, 0 malformed
under the CORPUS.md census: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`
→ `132`; `awk -F'|' '… NF!=13 {n++} END{print n+0}'` → `0`), so S133 is the next unused id and S134
is free. If the L1 prefers not to give the rejected candidate a registry id, drop the S134 registry
row and keep only its Gate row — the decision is what the Gate must carry. A rejected row's
`status` is `rejected` and its `teaches` cell must read `REJECTED: <reason>; flip: <what would
change the verdict>`.

---

## 3. Two drafting choices left to the L1

1. **Class label.** Entry 14 uses the lane's prose class ("instrument trusted receipts without
   binding them to the run"), matching the style of `corpus/lessons/round-44.md` entries 12–13. The
   fleet vocabulary suggested in `kaika-w1/mistakes.md` §5 is `vacuous`, `survivor`,
   `stale-premise`, `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`,
   `provider`; the nearest fit for entry 14 is `vacuous` (the gate's credit was vacuous with
   respect to the receipt's provenance) and for entry 15 `attribution` (a tuple attributed to a
   receipt that does not carry it). [INFERENCE] Prior rounds mixed the two forms; the round-43
   reviewer recorded the vocabulary gap as a style nit, not a missing component
   (`corpus/lessons/round-43.md`, `ReviewLesson43.md`).
2. **Entry count.** Land entry 14 alone, or 14 and 15 as two rows of the same class. Entry 15's
   evidence is committed bytes and three independent wave-1 reports, so it does not depend on any
   round-45 instrument; entry 14's "able to fail" line, by contrast, still points at a matrix
   receipt that does not exist yet.

---

## 4. Files this seat wrote

1. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/drafts/mistakes.md` — this draft.
2. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w1/ScribeLessonMistakes.md` —
   the seat report (exact commands, verbatim decisive output, pass/fail against the named attack).
3. `/fast/scratch/hyaku/kake-r45/ScribeLessonMistakes/` — scratch only: `subprocess.html`,
   `subprocess2.html`, `so-24139389.json`, `so-rep-1.json`, `so-rep-2.json`, `ans-5631624.json`,
   `q5631624.json`, `search.json`, `probe_receipt_trust.py`, `able_to_fail.sh`, and the
   `able-to-fail/` and `plantv2/` run directories.

No frozen artifact, corpus file, receipt, manifest, SCORECARD entry, state file, fleet file, or
sibling-lane file was edited. No `git`/`jj` write, no commit, no push, no install or update of any
tool (none was needed: `python3` and `curl` were already present; pacman is paused host-wide). No
subagent dispatched.
