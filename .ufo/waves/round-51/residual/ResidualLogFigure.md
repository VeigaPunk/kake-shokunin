# Residual — the LOG wall-clock figure (L3's LOG clause)

Seat: `L1Kake51.ResidualLogFigure`. Round 51, residual wave 2, dispatched after
`907790c78008819fc95c988431188f90b81f0d5f` (wave 1's landing commit). Read-only review of the
`897` clause in `LOG.md`; the only file written is this one.

Verdict: **the LOG figure is true and correctly attributed; the predicate clause that is
supposed to bind it does not bind it.**

---

## 1. `grep -n 897 LOG.md` — three matches, one of them the round-51 wall clock

```
265:  00:06:19.897Z `pushed:true`, none newer than `9c28d29`); PQ-5 `PENDING`
339:  newest 00:06:19.897Z `pushed:true`); and README's range gloss over missing
2088:  48 seats, 48 settled, 0 dead, 48 committed reports, wall clock **897 s**, aggregate seat seconds
```

- **2088 is the round-51 wall clock.** The sentence continues on 2089 (`**23 554**`, dead-seat
  seconds 0) and closes with `Sources: .ufo/waves/round-51/`. Same content at the commit:
  `git show 907790c:LOG.md` lines 2086–2091.
- **265 and 339 are incidental digit runs.** Both are the substring `.897` inside the timestamp
  `00:06:19.897Z` of the charter-scribe ledger's newest beat for remote `9c28d29` — r16/r17
  material, not round 51, not seconds of wall clock.

So the honest reading of the grep is: exactly one of the three matches is the figure under
review, and the other two are unrelated timestamps that happen to contain the same digits.

## 2. Does `wave-timing.json` re-derive 897 s? — yes, exactly

Committed bytes (`git show 907790c:.ufo/waves/round-51/wave-timing.json`):

```
startedAt 2026-10-25T06:32:17+00:00
settledAt 2026-10-25T06:47:14+00:00
wallClockSeconds 897
```

`06:47:14 − 06:32:17 = 14 min 57 s = 897 s`, computed as `897.0` s. No rounding slack: the pair
lands on the integer.

The pair is stamped in band, not back-filled. The two source files carry write mtimes that match
their own contents to the second (truncated):

| file | content | mtime (UTC) |
|---|---|---|
| `wave-start-utc.txt` | `2026-10-25T06:32:17Z` | `06:32:17.179854Z` |
| `settled-utc.txt` | `2026-10-25T06:47:14Z` | `06:47:14.241390Z` |

Both files are tracked, with byte-identical content, at `88aef0d` **and** at
`907790c` (`git cat-file -e` → present; `git show` → same strings). The stamps therefore existed
before the wave-evidence commit and were not retro-fitted by it.

Truncation direction is safe: `build_wave_evidence.py:45` uses `int(...total_seconds())`, which
truncates. Real elapsed between the two writes is 897.06 s and is reported as 897; the figure can
under-report by under a second and can never overstate.

## 3. Does `round-time-accounting.json` carry the same three figures as the settlement? — yes

| figure | `round-time-accounting.json` | settlement / re-derivation | LOG 2088–2089 |
|---|---|---|---|
| wall clock | `wall_clock_seconds: 897` | `wave-timing` delta `897.0` | `**897 s**` |
| aggregate seat seconds | `aggregate_seat_seconds: 23554` | Σ of the 48 `settled[].seconds` = `23554` | `**23 554**` |
| dead-seat seconds | `dead_seat_seconds: 0` | Σ of `dead[].seconds` = `0` (`dead_count: 0`) | `dead-seat seconds 0` |

Recomputed directly from `settlement.json`: `n=48`, `sum=23554`, `min=132`, `max=895`,
all `exit==0`, all `report==true`. The remaining LOG sentence figures also agree:
`spawn 48`, `settled_count 48`, `dead_count 0`, `reports_written 48`, and
`git ls-tree … .ufo/waves/round-51/w1 | grep -c '\.md$'` → `48`.
`max` seat 895 s at start +895 = 06:47:12, two seconds before the settled stamp — consistent with
a single batched dispatch, no seat claimed more time than the wave lasted.

`python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root … --revision 907790c…` → `L1 pass`,
`L2 pass`, `L3 pass`, `C1 ledger 3/3 met=True`, exit 0.

---

## Findings

### HIGH — L3's LOG clause is a bare substring test, so the two incidental matches would satisfy it even with the round-51 sentence deleted

`c51_wave_ledger.py:242`:

```python
if wall > 0 and str(wall) not in log_text:
```

`log_text` is the entire committed `LOG.md`. The test asks whether the three characters `897`
appear anywhere in 2 102 lines — and they do, at 265 and 339, for reasons that have nothing to do
with this round. I ran the check against the real revision with `show()` monkey-patched to serve a
mutated LOG (scratch script `/tmp/k51res/control_log_clause.py`; the repo was not touched):

```
[unmutated]            ok=True  wall=897 agg=23554 dead=0 notes=[]
[drop-L2088-2089]      ok=True  wall=897 agg=23554 dead=0 notes=[]
[wrong-figure-2088]    ok=True  wall=897 agg=23554 dead=0 notes=[]
[drop-all-897-lines]   ok=False wall=897 agg=23554 dead=0 notes=['LOG.md does not name the re-derived wall-clock figure 897']
```

Deleting the whole wall-clock sentence (2088–2089), or rewriting it to `wall clock **999 s**`,
leaves `L3 pass`. Only removing *every* line containing `897` fails. So:
the LOG's claim is true today — but the ledger does not certify that claim, it certifies the
presence of the digit string. Anything that reads `L3 pass` as "LOG names the round-51 wall clock"
is reading more than the check performs. The clause is **not vacuous** (a LOG with no `897`
anywhere fails), but it is satisfied by the incidental occurrence, which is exactly the failure
mode the sentence "LOG.md names the wall-clock figure" is meant to exclude.

Not repaired here: this seat is read-only. The repair is a scoped match (`wall clock **{wall} s**`,
or `f"wall clock **{wall:,} s**".replace(",", " ")`, plus a line-anchored window), not a new
check.

### LOW — the aggregate is verifiable as an internal sum, not as a fresh measurement from the commit

`build_wave_evidence.py:53` derives each seat's `seconds` from `os.path.getmtime(w1/<Seat>.md)`.
File mtimes are not versioned, so `aggregate_seat_seconds: 23554` cannot be re-measured from
`907790c`; it is checkable only as the sum of the numbers the settlement itself carries, which is
exactly what `c51_wave_ledger.py:215` does. That is a fair check of *internal consistency*, and it
passes. It is not independent corroboration of elapsed time. The ledger header's phrasing
("re-derivable from the committed settlement and wave-timing bytes",
`c51_wave_ledger.py:21-22`) is accurate for the check as written, but should not be read as
"independently remeasurable".

This is not hypothetical drift: five wave-1 reports are dirty in the working tree right now
(`CriticZeroControl`, `ExecRegistryDiff`, `ReviewAppendOnly`, `ReviewC2Conditions`,
`SentinelWriteScope`; mtimes 06:49:03–06:50:04 UTC), so re-running `build_wave_evidence.py` today
would print a different, larger aggregate (current max 1063 s vs. the committed 895 s). The
committed bytes are unchanged (`git hash-object` == the commit's blob for `settlement.json`,
`wave-timing.json`, `round-time-accounting.json`), but any future re-derivation of the aggregate
must be run against a pinned snapshot, not the live tree.

### INFO — no predicate binds `23 554`

The LOG names `23 554` at 2089 and the number is correct, but neither C1's L3 nor any other check
compares the LOG's aggregate against `round-time-accounting.json`; L3 only compares the accounting
file to the settlement sum (line 244). The agreement is real and I verified it independently, it
is simply not gated.

---

## Residual risk

1. `LOG.md:2088` remains true at `907790c` for the wall clock and every neighbouring figure. The
   risk is entirely in the predicate: `L3 pass` does not distinguish "LOG names 897 s as the
   round-51 wall clock" from "LOG contains the digits 897 twice in an unrelated timestamp".
2. If a later round's LOG happens to contain `897` for any reason and the round-51 sentence is
   rewritten or removed, C1 will keep scoring `3/3` with a false LOG claim. The mutation controls
   above are the direct demonstration.
3. The 897 s figure is trustworthy on its own merits: in-band stamps, tracked before the evidence
   commit, truncating arithmetic, and a seat-time maximum (895 s) that sits just inside it. Nothing
   about the wave's clock is inflated.

## Verification gaps

- No `lsp` server is applicable to this question: the objects under review are committed data
  files and a Python predicate run from the shell, not a code symbol graph. All caller/definition
  claims here are `grep`/`git show` plus direct executions, and are labelled as such; no semantic
  LSP evidence is claimed.
- I did not re-run `c51_quote_truth.py` (C2, 8 of 8) — out of scope for this seat. The sibling
  `L1Kake51.ResidualC1Rerun` owns the predicate re-run.
- I did not run `build_wave_evidence.py`, because running it against the live tree would overwrite
  committed artifacts and mutate the lane. The aggregate was verified by summation over the
  committed `settlement.json` bytes instead.
- The five dirty wave-1 reports were observed to be dirty; I did not read them, and their content
  is another seat's scope.

## Commands run (all read-only)

```
grep -n 897 LOG.md                                    # 265, 339, 2088
git show 907790c…:LOG.md | grep -n 897                # same three at the commit
git show 907790c…:.ufo/waves/round-51/{wave-start-utc,settled-utc}.txt   # stamps, unchanged from 88aef0d
git cat-file -e …                                     # both stamp files tracked at both revisions
stat + python getmtime                                # stamp files' own write times
python3 -c "sum(seconds) over settlement['settled']"  # 23554, n=48, min 132, max 895
python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root … --revision 907790c…   # 3/3 met=True, exit 0
python3 -B /tmp/k51res/control_log_clause.py          # four LOG mutations, results quoted above
git status --porcelain -- .ufo/waves/round-51/w1      # five dirty reports
```
