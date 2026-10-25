# ReviewL1Accounting — adversarial read of `check_l1`

Seat: leaf reviewer (no subagent dispatch). Scope: `check_l1` in
`.ufo/waves/round-51/c51_wave_ledger.py:97-143`, and the C1/L1 sentence it implements.
Read-only except this file. Scratch lived in `/tmp/r51attack`. No tool installed or upgraded
(no pacman/uv/npx/cargo transaction was run; the host-wide pacman pause was not tested).

## Verdict

**Yes — a settlement and report set that passes L1 while attesting a wave that never ran exists,
and the cheapest one needs no reports at all.** L1 is a *self-consistency* check over bytes the
same author writes; it never reads an execution trace (exit code, probe receipt, report body,
timing, transcript). Every number it compares comes from `settlement.json` or
`w51-taskcall.json`, both authored by the seat being checked.

Measured state at dispatch, reproduced:

```
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . \
    --revision 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
C1 ledger 0/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 FAIL
    - settlement receipt absent at the measured revision
EXIT=1
```

L1 fails today only because the settlement is absent. The absence of evidence and the evidence of
a never-run wave are the **same input** to this checker: commit the settlement below with an empty
`w1/` and L1 goes green.

## The construction that passes (executed, not just paper)

Three committed artifacts, one commit:

```jsonc
// .ufo/waves/round-51/settlement.json
{"spawn": 48,
 "settled": [{"name": "Seat00", "report": false, "exit": 0, "seconds": 60}, /* … x48 */],
 "dead": [], "settled_count": 48, "dead_count": 0,
 "reports_written": 0, "timeout_seconds": 900}

// .ufo/waves/round-51/w51-taskcall.json
{"counts": {"spawn": 48, "resume": 0, "total": 48},
 "taskCall": {"tasks": [{"name": "Seat00"}, /* … x48 */]}}

// .ufo/waves/round-51/w1/   -> empty; no committed .md at all
```

Every gate at `97-143` is quiet:

| gate | line | value |
|---|---|---|
| `payload_spawn != len(tasks)` | 124 | 48 == 48 |
| `spawn != len(tasks)` | 126 | 48 == 48 |
| `settled_count + dead_count != len(seats)` | 128 | 48 == 48 |
| `reports_written != len(committed)` | 130 | 0 == 0 |
| `reported != committed` | 135 | `[] == []` |

Executed against a scratch git repo:

```
CASE O2 (48 seats, all exit 0, reports_written 0, empty w1/)
passed= True
facts= payload_spawn 48, settlement_spawn 48, payload_seats 48, settlement_seats 48,
       settlement_reports_written 0, seats_marked_with_report 0, committed_report_files 0
notes= []
rev   = 942b666f664fe0bee84669640be3e9dbf06f18d6
```

That settlement asserts a 48-seat wave in which every seat exited 0 and no seat produced the one
report its dispatch ordered. L1 certifies it. It would certify the same document with `spawn`
unchanged and the wave never dispatched, because the dispatch payload is equally authored by the
same seat and only its *count* is compared.

Two further passing shapes are worth recording because they are cheaper still:

* **A (zero seats)** `{"spawn":0,"settled":[],"dead":[],"settled_count":0,"dead_count":0,
  "reports_written":0}` + `{"counts":{"spawn":0},"taskCall":{"tasks":[]}}` → `passed: true`
  (rev `b974cac5…`). No minimum-seat guard exists.
* **P2 (keys omitted)** `{"spawn":0,"reports_written":0}` → `passed: true` (rev
  `d2cd21ba…`). `.get(..., [])` makes missing `settled`/`dead` indistinguishable from empty.

## The missing guards, named precisely

Each is a distinct under-specification, each admitted a passing construction.

**G1 — no coverage floor.** `reports_written` is compared only to `len(committed)` (line 130).
It is never compared to `spawn` or `len(seats)`, and `len(reported)` is never required to equal
anything. *The ledger certifies seat accounting without requiring that any seat reported.* This is
the guard whose absence admits the never-run wave above. Exploits: O2, A, P2.

**G2 — multiset collapsed to set (a real bug, not just a contract gap).** Lines 135-141:

```python
if reported != committed:
    missing = sorted(set(reported) - set(committed))
    extra   = sorted(set(committed) - set(reported))
    if missing: notes.append(...)
    if extra:   notes.append(...)
```

`reported` and `committed` are **sorted lists**; the trigger is list inequality but the notes are
*set* differences. Any discrepancy that is a set-equality produces neither note, so the branch
enters and exits silently.

Exploit **N2** (rev `9347a090…`), `passed: true`, `notes: []`:

```jsonc
"settled": [{"name":"GhostA","report":true}, {"name":"GhostA","report":true},
            {"name":"GhostB","report":true}],
"settled_count": 3, "reports_written": 2
// w1/: GhostA.md, GhostB.md
// reported  = ['GhostA','GhostA','GhostB']   (3 seats marked)
// committed = ['GhostA','GhostB']            (2 files)
facts: seats_marked_with_report 3, committed_report_files 2
```

A seat marked as having a report has **no** committed file, and L1 passes — a direct contradiction
of the contract's own L1 sentence "every seat marked as having a report has exactly one committed
report file". The same collapse accepts duplicate seat names.

**G3 — no content or attribution binding.** No report body is ever read (`list_paths` is
name-only; `show` is never called for a report). Exploits:

* **B** (rev `4b592788…`), `passed: true`: `w1/GhostA.md` is **0 bytes**; `GhostB.md` and
  `GhostC.md` are byte-identical (`md5 eff5bc1ef8ec9d03e640fc4370f5eacd`, 3 bytes each).
* **M** (rev `b535e49ae…`), `passed: true`: both reports are a **verbatim copy of
  `contract.json`** — an unrelated committed document.
* **I2** (rev `cc664acd…`), `passed: true`: `"report": "no"` is truthy, so a seat that declares it
  has no report is counted as reported.
* **J** (rev `84ec5dbeb…`), `passed: true`: seat name `"sub/X"` satisfied by the nested path
  `w1/sub/X.md`; a report need not sit at `w1/<seat>.md`.

**G4 — no dispatch binding.** Lines 124-127 compare *counts* only; the payload's seat **names** are
never compared to the settlement's. Exploit **K** (rev `7fa81578…`), `passed: true`: payload
`Alice, Bob`; settlement `Solo, Duo` — two entirely different waves, one certification.

**G5 — no contract or grant binding.** L1 never reads `contract.json` (declares 48 seats) or
`wave-grant.txt` (`seats=48`). Exploit **L** (rev `0af85cf…`), `passed: true`: `spawn: 1`, one
seat, one report — while the committed grant says `seats=48`.

**G6 — report path not required to be a regular file.** `list_paths` (`git ls-tree -r
--name-only`) discards the mode, and `show` returns a symlink's *target string* as its body.
Exploit **R2** (rev `e327a254…`): `ln -s GhostA w1/GhostA.md`, committed as mode `120000`:

```
120000 blob 5135b60c... .ufo/waves/round-51/w1/GhostA.md
git show <rev>:.../GhostA.md  ->  GhostA
```

`passed: true`. The "report" is its own link target; no file exists.

**G7 — unguarded failure instead of the documented exit 2.** The docstring promises exit 2 when
"the evidence cannot be evaluated". `main()` (260-297) has no handler, so:

* **G** (rev `32b24214…`): settlement entry without `name` → `KeyError: 'name'` at line 109
  (direct `e["name"]`, not `.get`).
* **H** (rev `c05e0a84…`): `"settled_count": null` → `TypeError: unsupported operand type(s) for +:
  'NoneType' and 'int'` at line 128.

Both exit non-zero via traceback, so the predicate is not met — but the ledger reports a crash, not
a finding, and the documented code path is dead.

## What L1 does block (the guards that worked)

Fair credit; these were each defeated by construction and each held:

| case | attack | note printed |
|---|---|---|
| C (`8c20e62`) | seat marked report, no file | `reports_written 1 != committed 0`; `seats marked with a report but no committed file: ['X']` |
| D (`b6cacc2`) | extra file for an unknown seat | `committed report files for unknown seats: ['Stranger']` |
| E (`91698e9`) | `counts.spawn` lies about `len(tasks)` | `payload spawn 9 != payload seats 1` |
| F (`28e071f`) | `settled_count+dead_count` wrong | `settled_count + dead_count != settled + dead entries` |

The unknown-seat guard is also *strict in the other direction*, with a live consequence: **every**
`.md` committed under `w1/` must be a seat the settlement lists. This review file, once committed,
makes `ReviewL1Accounting` a mandatory settlement entry; otherwise C1 fails with
`committed report files for unknown seats: ['ReviewL1Accounting']`. Reviewer/scribe artifacts are
therefore seats by definition, not annotations.

## Frontier step (proposed, demonstrated in /tmp, **not applied**)

A nine-guard supplement (`/tmp/r51attack/augmented_l1.py`, wrapping the lane module read-only)
was run over every case:

| case | original L1 | augmented |
|---|---|---|
| A zero-seat | pass | fail (F1) |
| B empty/identical bodies | pass | fail (F8/F9) |
| K names unbound | pass | fail (F5) |
| I2 `report:"no"` | pass | fail (F4/F6) |
| L spawn 1 vs grant 48 | pass | fail (F5) |
| M contract copied (1-char names) | pass | **pass** (substring hit) |
| M2 contract copied (long names) | pass | fail (F9) |
| N2 duplicate hides missing report | pass | fail (F3/F4/F6) |
| O2 48 seats, 0 reports | pass | fail (F5) |
| P2 keys omitted | pass | fail (F1/F4) |
| R2 symlink body | pass | **pass** |

The guards, in the order they close the frontier:

1. **F1** `spawn` is a positive integer — closes the zero/empty fixed point (A, P2).
2. **F5** `{names of settled seats} == {reported names}` — that is the missing coverage guard; it
   is what closes O2 and is the one-line fix for G1.
3. **F3/F6** `reports_written == len(reported) == len(committed)` plus `Counter(reported) ==
   Counter(committed)` — closes G2 (N2). `Counter`, not `set`.
4. **F4** unique, non-empty seat names — closes the duplicate-name half of G2.
5. **F8/F9** non-empty body **and** a structural header naming the seat — closes G3 (B, M2, J).
   Substring containment is not enough: M passed with 1-char names because `"P"` occurs in any
   JSON; the match must be an exact header/first-line equality.
6. **F10** the report path must be a regular blob (`100644`/`100755`), not `120000`/`160000` —
   closes G6 (R2). Needs `git ls-tree -l` or a `git cat-file -p` type check, which the current
   `--name-only` call throws away.
7. **G4/G5** bind the payload's seat names to the settlement's, and `spawn` to the frozen
   contract/grant seat count — closes K and L. These belong in the *contract sentence*, not only
   the code: the frozen L1 text never says "every spawned seat must have a report", so the counter
   faithfully implements a contract that does not demand one.

What remains open even after F1-F10: **no chronology or provenance**. `check_l1` reads a single
revision, so a settlement committed in the *same commit* as all 48 reports (or a settlement
committed before the reports it describes) is indistinguishable from a real settlement. Closing
that needs a second revision — settle at N, score at N+1 with the settlement required to be
strict-ancestor of the measured revision — which is a contract change, not a guard.

## Root cause, stated once

The contract's L1 sentence is:

> the committed seat-report count under `.ufo/waves/round-51/w1/` equals the settlement's
> `reports_written`, the settlement's `spawn` equals the payload's seat count, and every seat
> marked as having a report has exactly one committed report file

All three clauses are relations among authored numbers. None is a relation to a trace of execution.
C1's predicate is therefore satisfiable by a well-formed settlement that reports nothing, which is
the one input that a wave that never ran and a wave that ran both produce. **The missing guard is
positive evidence: L1 must require that every spawned seat has exactly one non-empty, mode-regular,
seat-headed report whose basename multiset equals the marked-report name multiset — and must
require `spawn >= 1` between the grant, the payload and the settlement.**

## Reproduction

```
git init /tmp/r51attack && cd /tmp/r51attack
mkdir -p .ufo/waves/round-51/w1
# write the two JSON documents above, commit, then:
python3 -B <lane>/.ufo/waves/round-51/c51_wave_ledger.py \
    --root /tmp/r51attack --revision HEAD --json
```

Scratch revisions cited above (`git log --all` in `/tmp/r51attack`): A `b974cac5`, B `4b592788`,
C `8c20e62a`, D `b6cacc22`, E `91698e92`, F `28e071fb`, G `32b24214`, H `c05e0a84`, I `cd901b8e`,
I2 `cc664acd`, J `84ec5dbeb`, K `7fa81578`, L `0af85cf`, M `b535e49a`, N `161aa4a5`, N2
`9347a090`, O2 `942b666f`, P2 `d2cd21ba`, R2 `e327a254`, M2 `f36053e5`.

## Honesty

* Every `passed: true` / `passed: false` above is copied from a run I executed against
  `/tmp/r51attack`; the dispatch-state command was re-run in the lane and printed `0/3 met=False`,
  exit 1.
* The lane was not modified; no `git add/commit/stash/checkout/reset/pull/push`, no `jj` command,
  no pacman/uv/npx/cargo install ran. Only `/tmp/r51attack/*` and this file were written.
* The augmented checker is a `/tmp` wrapper that imports the lane module; it is a proposal with
  measured effect, not an applied fix, and its F9 weakness (substring match) is reported above
  rather than hidden.
* Files read: `contract.json`, `c51_wave_ledger.py` (all 297 lines), `w51-taskcall.json` (schema
  and first task), `wave-grant.txt`, `w1/swarm-registry.json` (head), `LOG.md` not read. No file
  was unreadable.
