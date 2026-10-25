# Residual settlement attack — round 51, measured revision `907790c`

Role: UFO-FSD critic (residual wave 2). Target: the settlement evidence itself, on the bytes committed at
`907790c78008819fc95c988431188f90b81f0d5f` (hereafter `907790c`). Read-only on the fleet repo; every
mutant ran in a scratch git repo under `/tmp/r51res` built by `git archive 907790c`, with the C1 counter
copied verbatim from `907790c:.ufo/waves/round-51/c51_wave_ledger.py`. Scratch-repo revisions named below
are fixture-local commits, not fleet commits.

## Verdict

The three consistency questions come out **true on these bytes**, and none of them is **enforced by the
instrument**. The measured wave is real evidence (48 distinct reports, 712,596 committed bytes, smallest
5,062 B); the C1 ledger at this revision still certifies a wave that produced nothing. Every wave-1
vacuity hole I re-ran — zero-seat wave, phantom seat, empty report body — **remains reachable on these
exact bytes**, and I found two more that wave 1 did not name: the grant's seat figure is never read, and
47-of-48 delivery certifies.

## 1. Does `settlement.json` name exactly the 48 payload seats?

**Yes, exactly — measured, not assumed.**

| set | count | source |
|---|---|---|
| `taskCall.tasks[].name` | 48 | `w51-taskcall.json` |
| `registry.members` keys | 48 | same file, same order as `tasks` (`tasks == registry order` → `True`) |
| `settlement.settled[].name` | 48 (dead 0) | `settlement.json` |
| `w1/*.md` basenames | 48 | `git ls-tree -r 907790c -- .ufo/waves/round-51/w1` |

Set equality holds in both directions (`payload − settled = ∅`, `settled − payload = ∅`); roles agree for
all 48 (`role mismatches: []`); `settlement.seats` matches `settled`; the per-seat `model` string equals
the route map's `kimiModel` for every role (`commandcode/deepseek/deepseek-v4.1-flash`, one route, all
roles). `w1/` also holds `swarm-registry.json` (49 files total, 48 `.md`) whose 48 member names are the
same set.

**But the ledger never compares settlement names to payload names.** L1 builds `reported` from
`settlement["settled"] + ["dead"]` and `committed` from `git ls-tree` `.md` names, and compares those two
to each other; `spawn == len(tasks)` is the only payload binding, and it is a *count*. Result: a
settlement can name 48 seats that were never in the dispatch payload and still score 3/3.

```
### M2 phantom 48 seats vs payload  rev=734e4d4a exit=0 met=True
   L1 pass
   L2 pass
   L3 pass
```

`settlement["seats"]` is not read by any of L1/L2/L3 at all (`grep 'seats'` shows only
`settled + dead`), so that third copy of the seat list can drift silently:

```
### M10 seats field drift rev=bb42cd53 exit=0 met=True     # settlement["seats"] renamed Unused00..47
```

## 2. Does `reports_written` equal the committed report count?

**Yes: 48 = 48.** The two counts come from independent code paths — `build_wave_evidence.py` counts
worktree file existence at build time; L1 counts `git ls-tree` blobs at the measured revision — which is
the one genuinely independent cross-check in L1, and it is satisfied.

It is a *count* only. Nothing in the chain opens a report: `list_paths` is name-only and `show` is never
called for a `w1/` path. So the count is blind to body, size and attribution:

```
### M3 48 zero-byte reports            rev=3bd7555c exit=0 met=True
### M6 report body = contract.json copy rev=a338d392 exit=0 met=True
### M4 48 seats 0 reports              rev=cc0146df exit=0 met=True
```

M4 is the "48 claimed / 0 reports" form: settlement `report:false` for all 48, `reports_written:0`,
`w1/` emptied → `0 == 0`, `[] == []`, `spawn 48 == len(tasks) 48` → 3/3. That is the contract's own L1
sentence ("every seat marked as having a report has exactly one committed report file") satisfied by a
wave in which no seat wrote the one report its dispatch ordered.

## 3. Is `spawn` consistent with the grant?

**Yes: 48 = 48.** `wave-grant.txt` = `granted lane=kake wave=r51-w1 seats=48 live=66 pending=0 cap=256`;
`settlement.spawn` = 48; `len(taskCall.tasks)` = 48; `policy.declaredMaxLanes` = 48; `hardCeiling` = 256
= grant `cap`. The settlement builder does **not** read the grant (`spawn` is copied from
`payload["counts"]["spawn"]`), and L3's only grant test is the substring `"granted lane=kake"`. The seat
figure in the grant is therefore decorative evidence:

```
### M8 grant seats=1 vs settlement spawn=48 rev=b7de8ad2 exit=0 met=True
```

`live=66` is unverifiable against this wave in either direction: 66 names lanes/agents alive at
grant time, 48 were dispatched, and no committed artifact enumerates either set.

## 4. Do wave-1's vacuity holes survive on these bytes?

The counter is byte-identical to its first commit (`git log --oneline 19a99bd..907790c --
.ufo/waves/round-51/c51_wave_ledger.py` is empty), which predicts wave 1's verdicts carry over. I re-ran
them rather than relying on that; every one still scores 3/3 at `907790c`'s counter bytes:

| hole | mutant | result |
|---|---|---|
| zero-seat wave | `spawn:0`, `tasks:[]`, `w1/` emptied, clock collapsed to 0 | **3/3, exit 0** (`8036287d`) |
| phantom seat | 48 settlement names + 48 renamed report files, payload untouched | **3/3, exit 0** (`734e4d4a`) |
| empty report body | all 48 reports truncated to 0 bytes | **3/3, exit 0** (`3bd7555c`) |
| 48 claimed / 0 reports | all `report:false`, `reports_written:0`, `w1/` emptied | **3/3, exit 0** (`cc0146df`) |
| multiset→set collapse (G2) | 49 settlement entries (one duplicated), 48 files, `reports_written:48` | **3/3, exit 0** (`e07c24be`) |
| LOG substring | the labelled sentence `wall clock **897 s**` deleted; `897` survives only inside `00:06:19.897Z` | **3/3, exit 0** (`51dff14f`) |
| time tautology | every seat `seconds:0`, accounting recomputed to 0, wall left at 897 | **3/3, exit 0** (`a4fa218c`) |
| unused field | `settlement["seats"]` renamed to `Unused00..47` | **3/3, exit 0** (`bb42cd53`) |
| **47-of-48 delivery** (new) | one seat moved to `dead` with `reason:"no-report"`, `exit:-1`, its report deleted, accounting resummed | **3/3, exit 0** (`8221d850`) |
| exit-code contract (new) | a settled entry with no `name` key | `KeyError: 'name'`, **exit 1**, not the documented 2 |

Two details worth keeping: G2 needs *exact* set equality — a duplicate name whose set difference is
non-empty does fire a note (my first M5 attempt did), so the collapse is narrow but real and passes at
scale (49 entries / 48 files). And M11 shows the dead-seat branch is not merely untested, it is a free
pass: L3's reason/duration rules only fire for reasons starting `timeout-`/`exit-`, so `no-report` dead
seats are admitted with any duration up to the wall clock.

## 5. What this evidence still cannot prove

1. **That 48 seats executed.** `agentId` is `null` for all 48 members in both `w51-taskcall.json` and
   `w1/swarm-registry.json`; `w51-validator.err` is 0 bytes; there is no committed dispatch transcript,
   no per-seat job record, no transcript digest. The settlement, the payload, the registry and the 48
   reports are all authored by the same lane, and the only cross-file bindings are counts and name
   strings.
2. **Per-seat `exit`.** `build_wave_evidence.py:58` hard-codes `"exit": 0` for every seat that has a
   file on disk. No exit status is recorded anywhere; settlement `exit` is a constant, not a
   measurement.
3. **Per-seat `seconds`.** Derived from the report file's *mtime* at build time. mtime is not committed,
   so `23554 s` aggregate and the `132..895 s` spread cannot be re-derived from the revision by any
   reader. L3 only re-sums the authored numbers.
4. **The wall clock.** `wave-start-utc.txt` (06:32:17Z) and `settled-utc.txt` (06:47:14Z) are two
   authored plain-text stamps; 897 s is arithmetic over them, not an observed interval.
5. **That a report body belongs to its seat.** 47 of 48 reports name their own seat; `ReviewC2Conditions`
   (23,496 B) does not. Nothing tests this either way, so the one miss is invisible and a wholesale
   substitution would be too (M6).
6. **That the grant authorised this wave.** Only the literal `granted lane=kake` is read; `seats=48`,
   `live=66`, `pending=0` and `cap=256` are unchecked (M8).
7. **That the route actually served the calls.** L2 checks receipt shape and `ok:true`, plus the route
   map's self-declared deviation; the receipt is authored by the same lane.

## 6. Smallest safe correction

Ordered by cost, each closes named mutants, none changes the frozen predicate arithmetic (all six hold on
the real `907790c` bytes, so the correction costs the claim nothing):

1. **Seat identity binding** — in L1, require `sorted(settled+dead names) == sorted(task names)`
   (multiplicity preserved) and `settlement["seats"] == [{"name": t["name"], "role": t["agent"]} for t in
   tasks]`; parse `seats=(\d+)` from `wave-grant.txt` and require it equals `spawn` and `len(tasks)`.
   *Closes M2, M5c, M8, M10.*
2. **Coverage floor** — require `spawn > 0`, `len(settled) == spawn`, `reports_written == len(settled)`,
   and `dead == []` unless the settlement carries a per-dead-seat dispatch receipt. *Closes M1, M4, M11.*
3. **Report pinning** — settlement carries `sha256` (and byte length) per report; L1 re-derives it from
   the blob, rejects an empty/whitespace body, rejects duplicate digests, and requires the seat name to
   appear in the body. *Closes M3, M6; makes the `ReviewC2Conditions` miss a visible, honest note.*
4. **Labelled LOG token** — match `wall clock[: ]+\*{0,2}897\*{0,2} s` or `wall_clock_seconds=897`, not
   `str(wall) in text`. *Closes M7.*
5. **Exit-code contract** — wrap each check in `try/except` and return 2 on unevaluable evidence; a
   missing `name` currently crashes to exit 1, the same code a genuine miss returns. *Closes M12.*

Not a correction, a constraint: L1's unknown-seat guard is strict in the other direction, so **any**
`.md` committed under `w1/` must be a settlement seat — residual and wave-2 reports belong under
`residual/`, never `w1/`, or C1 fails with `committed report files for unknown seats`.

## Command log (what printed)

```
$ git rev-parse HEAD                      -> 907790c78008819fc95c988431188f90b81f0d5f
$ python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 907790c...   -> C1 ledger 3/3 met=True, exit 0
$ python3 -B .ufo/waves/round-51/c51_quote_truth.py  --root . --revision 907790c...   -> C2 quote-truth 8/8 met=True, exit 0
$ ... --revision 007d66e4e8360a5f88d29a93eeedd8066dad4434                            -> C1 0/3 exit 1; C2 0/8 exit 1
$ git ls-tree -r --name-only 907790c -- .ufo/waves/round-51/w1 | grep -c '\.md$'     -> 48
$ md5sum .ufo/waves/round-51/w1/*.md | sort | uniq -d | wc -l                        -> 0
$ sha256 over blobs: 48 distinct, min 5062 B, max 41504 B, total 712596 B
$ settlement: spawn 48, settled 48, dead 0, reports_written 48, seats 48
$ wave-grant.txt: granted lane=kake wave=r51-w1 seats=48 live=66 pending=0 cap=256
$ wave-timing: 06:32:17Z -> 06:47:14Z = 897 s; aggregate 23554 s; dead 0; per-seat 132..895 s
$ scratch: git archive 907790c -> /tmp/r51res, counter copied from 907790c; baseline fixture -> 3/3 met
$ scratch mutants M1,M2,M3,M4,M5c,M6,M7,M8,M9,M10,M11 -> "3/3 met=True", exit 0 each; M12 -> exit 1 KeyError
$ fleet worktree at review time: dirty on 5 w1 reports + corpus/lessons/round-51.md (siblings);
  counters read committed bytes only, so verdicts are unaffected
```

No tool installs were required. No fleet, sibling, jj or index state was touched.
