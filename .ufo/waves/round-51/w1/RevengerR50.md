# RevengerR50 — the four round-50 routed defects against round-51 committed bytes

Seat: `L1Kake51.RevengerR50-2` (revenger). Judged axis: **operability**. Read-only seat.

- Lane root: `/home/vgpnk/Projects/shokunin/kake-shokunin`
- Measured revision: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (= lane `master`, = `HEAD`)
- Base (do-nothing): `007d66e4e8360a5f88d29a93eeedd8066dad4434`
- Everything below is scored against **committed bytes at the measured revision**, never the
  worktree. Where I used the worktree (to read a file that is not committed) I say so.

## Verdict table

| id | round-50 defect (short) | round-51 committed state | verdict |
|---|---|---|---|
| r50-1 | report states 26 seat reports; bytes hold 25 | L1 count condition committed; correction figure in committed lesson; no round-51 report exists; L1 not exercisable (no settlement) | **partly addressed** |
| r50-2 | route-failure HTTP statuses live only in report prose | L2 condition committed; route map + probe receipts exist but are **untracked**; the one failing receipt is a synthetic probe | **partly addressed** — open on the evidence the defect names |
| r50-3 | no aggregate overrun figure re-derivable from committed bytes | L3 condition + measure + counting command committed; **no figure committed anywhere**; LOG names none | **partly addressed** — figure open |
| r50-4 | keep the ten inherited paths untouched | all ten untracked; no round-51 commit touches them | **addressed** (upheld) |

## 0. Where the four defects are defined (and a correction to the ids)

The labels `r50-1`…`r50-4` appear in **no round-50 committed artifact**. A read-only grep of
`/home/vgpnk/Projects/shokunin` returns them only in
`.ufo/waves/round-51/{contract.json,w51-spec.json,w51-taskcall.json}` and the round-51 seat
registry. The defect *text* they name is the numbered list under
`corpus/lessons/round-50-verifier-spotcheck.md` § "Routed defects (the lane must fix these next
round)" (lines 240–268). The 1:1 mapping of `r50-N` to list item *N* is my inference (ordinal
position; the round-51 contract's four `routedDefectsAddressed` entries line up with it exactly).

Quoted verbatim, the defect text I relied on:

> **1. Report overstatement on the wave report count.** The report says 26 seat reports were present
> when it was written; committed bytes and the working tree both hold 25 (`reports_written 25`,
> `ls-tree` 25). Correct the figure in the next round's report — append-only, never a rewrite of
> the filed bytes (`PROTOCOL.md` §Evidence standard).

> **2. Route-failure detail is prose-only.** The fallback is recorded in committed evidence
> (`.ufo/waves/round-50/route-map.json`: `connector`/`sentinel`/`executor`/`mutation-tester` →
> `devin/swe-2-max`, "own bucket unreachable on this substrate"), but the HTTP status codes that
> caused it — the `xai-oauth/grok-4.7-fast` **403** (out of credits) and the
> `commandcode/deepseek/…` **402**/unconfigured bucket — appear only in the lane report's prose,
> never in a committed artifact. Commit the probe receipts (status code + body excerpt) next time
> a route is substituted, so the deviation is re-derivable without the report.

> **3. No aggregate round-overrun figure is named in committed evidence.** […] Name the overrun
> measure and its counting command in the next round's report and `LOG.md`, so the ledger carries a
> figure a reader can re-derive.

> **4. Keep the ten inherited paths untouched.** The eight `round-46/residual/` reports and the nine
> `>1MiB` `round-48/assimilation/validate/` copies are orchestrator/large-file artifacts, named as
> deliberately untouched in `LOG.md` and in the r48/r49 spot-checks. Do not force-add them to
> silence a `git status` warning; a >1 MiB add is skipped by jj's snapshot limit anyway.

The filed report's offending sentence still stands at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-50/kake.md:219`:
"Report files: 25 at settlement, 26 present when this report was written (one seat's file landed
after the settlement snapshot)."

## 1. Committed-bytes inventory at `9d13768c`

`git ls-tree -r --name-only 9d13768c .ufo/waves/round-51/` contains: `contract.json`,
`c51_wave_ledger.py`, `c51_quote_truth.py`, `controls/` (4 files), `assimilation/` (guard,
collisions, quarantine slice, slices, the pre-append mirror and its census receipts), and
`sources/` (`S262.html`, `S263.html`, `receipts.json`).

It does **not** contain any of:

```
settlement.json   wave-timing.json   round-time-accounting.json
route-map.json    route-probes/      wave-grant.txt   wave-start-utc.txt
w1/               build_wave_evidence.py   w51-spec.json   w51-taskcall.json
```

`git status --porcelain` in the lane lists every one of those as `??` (untracked). Consequence:
**no wave evidence for round 51 is committed at the measured revision**, which is exactly why the
frozen C1 counter reads 0 of 3 (§5).

## 2. r50-1 — seat-report count

### What round 51 committed that bears on it

`c51_wave_ledger.py:check_l1` (committed at `19a99bd`) enforces, from committed bytes only:

- `payload_spawn == len(tasks)` and `settlement.spawn == len(tasks)`;
- `settled_count + dead_count == len(settled) + len(dead)`;
- `settlement.reports_written == <count of committed .md files under .ufo/waves/round-51/w1/>`;
- the set of seat names marked `report: true` equals the set of committed report file names
  (missing and extra both fail).

The class fix the defect asks for is therefore real and, on the round-50 numbers, would have
caught it: run L1 today against round 50's own receipt and the disagreement is named
(`controls/c1-junk-wave.txt`: "settlement reports_written 40 != committed report files 25" plus
fifteen named seats with no file).

The correction figure is also in committed prose, `corpus/lessons/round-51.md`:

> **class:** a wave's seat-report count stated in prose and not re-derivable. **evidence:**
> `corpus/lessons/round-50-verifier-spotcheck.md` routed defect 1 — the round-50 report
> claimed 26 seat reports while the committed tree holds 25.

I re-derived the figure independently:
`git ls-tree -r --name-only 1c7f0769 .ufo/waves/round-50/w1/ | grep -c '\.md$'` → **25**
(and → 25 at `9d13768c` as well). The verifier's 25 is right; the report's 26 is wrong.

### What is missing

1. The literal ask — "Correct the figure in the next round's report" — has not happened.
   `.ufo/reports/round-51/` in the fleet repo holds `kotoba.md`, `kotodama.md`, `kumitate.md` and
   **no `kake.md`**; `git log -- .ufo/reports/round-50/kake.md` shows only `47e235a5` and
   `f546bfc0`, i.e. no append-only correction of the filed 26.
2. L1 is not exercised at the measured revision: no `settlement.json` exists, so
   `python3 -B .ufo/waves/round-51/c51_wave_ledger.py --revision 9d13768c…` prints
   `L1 FAIL — settlement receipt absent at the measured revision`.

### Attack

L1 never reads a report. It makes the *number* derive-able from the settlement; it would not catch
a future report that restates a count wrongly. The defect's own wording ("stated in prose and not
re-derivable") is addressed at the root, not at the sentence.

**Verdict: partly addressed.** Committed: the condition, the corrected figure in the lesson, the
contract's mapping. Open: the round-51 report does not exist, and L1 cannot be run end to end until
the settlement is committed. Confidence: high.

## 3. r50-2 — route-failure receipts

### What round 51 committed

`check_l2` (committed) requires a committed JSON receipt per **used** route carrying an integer
`httpStatus`; for any `ok: false` receipt it requires a non-blank `bodyExcerpt`, forbids the route
being bound to a role, and requires the alias string to appear in the route map's deviation text.

I tested whether the *design* works by building a throwaway repo under
`/tmp/r51probe` containing only the worktree `route-map.json` and the two receipt JSONs, committed,
and calling `check_l2` directly:

```
L2 ok= True
notes= []
facts= {'roles': 10, 'receipts': 2}
```

So the receipt schema satisfies the committed condition. The receipts themselves are substantive:
`route-probes/xai-oauth_grok-4.7-fast.json` carries `"httpStatus": 403`, `"ok": false`, and a real
body excerpt (`provider.auth_error: 403 "You have run out of credits or need a Grok subscription…"`).

### What is missing

At `9d13768c` **nothing about routes is committed**: `route-map.json` and the whole
`route-probes/` directory are `??`. The committed counter says so:

```
L2 FAIL
  - route map absent at the measured revision
```

So a reader of committed bytes still cannot re-derive the 403 — the exact gap the defect
describes, only now the prose is in an untracked file instead of the report.

### Attacks (the stronger part)

1. **There was no real substitution to record.** The failing receipt carries
   `"note": "probed to exercise the failing-receipt path; no role is bound to this route this wave"`
   and `"endpoint": "provider route via kimi CLI (not used by this wave)"`. The wave map binds all
   ten roles to one alias (`commandcode/deepseek/deepseek-v4.1-flash`). The receipt is a deliberate
   exercise of the failure path, not evidence of the fallback the defect was about. [INFERENCE
   from the receipt's own note; the note is explicit.]
2. **The map records no reason for the change it did make.** Round 50 ran `devin/swe-2-max` for
   scout/critic and `zai-coding-plan/glm-5.3-flash` for reviewer/revenger/simplifier/scribe; the
   round-51 map moves every role to `@m_flash` and says nothing about why the round-50 routes were
   dropped. The only deviation it names is the 403 on a route it says it does not use.
3. **The passing receipt is an edge probe, not a completion probe.** It is
   `"leg": "http-edge"`, `"endpoint": "https://api.commandcode.ai/"`, body
   `{"success":true,"message":"Command Code API"…}`. The actual completion leg ("answered PONG") is
   prose in the receipt's `detail` and in the map's `probe` string. L2 checks neither `leg` nor a
   completion, so an API-root 200 satisfies it.
4. **Nothing binds the receipt to what ran.** All 48 objects in `w51-taskcall.json` `taskCall.tasks`
   carry `name`, `agent`, `task` — **zero have a `model` field**. L2's `used` set is built from the
   map's own `kimiModel` values, so the receipt certifies the map's declaration, not the dispatch.

**Verdict: partly addressed.** The instrument and the receipt schema are committed and work; the
receipts, the map and any real deviation are not. Confidence: high on (1)–(4) (all read from
committed/worktree bytes); medium on the judgement that a synthetic failure does not discharge the
defect.

## 4. r50-3 — aggregate overrun figure

### What round 51 committed

`check_l3` (committed) re-derives `aggregate_seat_seconds` (sum of per-seat `seconds` in the
settlement), `dead_seat_seconds`, and `wall_clock_seconds` (from `wave-timing.json`'s
`startedAt`/`settledAt`), requires `round-time-accounting.json` to carry the same three figures,
requires `str(wall) in LOG.md`, and requires a grant line.

The **measure and the counting command are committed**: the contract's L3 sentence names aggregate
seat seconds, dead-seat seconds and wall clock; the counting command
`python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision <commit>` is in the contract
and in `LOG.md`.

### What is missing

No figure. `settlement.json`, `wave-timing.json`, `round-time-accounting.json` and even
`settled-utc.txt` do not exist (`ls` fails on all four); `LOG.md` at `9d13768c` contains no round-51
wall-clock, aggregate or dead-seat figure (grepped for `wall`, `417`, `6.95`, `overrun`,
`seat-seconds` — the only hits are from earlier rounds). The counter prints:

```
L3 FAIL
  - settlement receipt absent at the measured revision
```

Committed prose already speaks as if the artifact exists. `corpus/lessons/round-51.md`:

> **fix:** the round-51 settlement carries the wave's start and end stamps,
> `.ufo/waves/round-51/round-time-accounting.json` carries the three figures, and
> `c51_wave_ledger.py` condition L3 re-derives them from the committed bytes and requires the
> lane's `LOG.md` to name the wall-clock figure.

### Attacks

1. **L3's dead-seat clause does not implement the contract's sentence.** The contract says "every
   dead seat's duration matches its recorded reason". The code only checks reasons that start with
   `timeout-` or `exit-`. The (untracked) `build_wave_evidence.py` emits every report-less seat as
   `{"exit": -1, "seconds": wall, "reason": "no-report"}` — a reason that matches neither branch, so
   the recorded duration is never checked against anything. L3 can pass while a dead seat is
   charged the whole wave wall clock under a reason the contract requires to be checked.
2. **The LOG clause is a digit-substring test.** `if wall > 0 and str(wall) not in log_text`.
   Measured: `417` — the round-50 verifier's own wave wall-clock figure — occurs once in `LOG.md` at
   `9d13768c`, inside the commit hash on line 947
   (`6cb08a40d72d657628f9a0334417901cdc97c732`, the `…334417…` run). `48` occurs 40 times. A hash
   digit-run or a seat count satisfies "`LOG.md` names the wall-clock figure" with no figure named.
3. **The per-seat seconds are not committed-byte-derived.** The builder takes each seat's `seconds`
   from `os.path.getmtime()` of its report file — mutable filesystem metadata, absent from the
   commit. L3 then "re-derives" the aggregate by summing the settlement's own numbers, so the
   arithmetic is verifiable but the inputs are not. The contract's phrase "re-derivable from the
   committed settlement and wave-timing bytes" is satisfied literally and circularly.
   [INFERENCE: read from the untracked builder; the committed counter cannot detect it.]

**Verdict: partly addressed.** Instrument, measure, command and the LOG obligation are committed;
the figure, the timing bytes and the accounting artifact are not, and the three clauses above are
the ways L3 could pass without the defect actually being fixed. Confidence: high on (1) and (2)
(code read; (2) measured), high on (3) as a provenance limitation.

## 5. The contract's own present-tense claims, checked

`contract.json:56–59` (committed at `19a99bd`) states, in the present tense:

| claim | text | true at `9d13768c`? |
|---|---|---|
| r50-1 | "the seat-report count is now a committed, re-derivable ledger condition (L1) instead of prose" | **true** (L1 is committed and reads committed bytes) |
| r50-2 | "the route substitutions now carry committed probe receipts with an HTTP status and a body excerpt (L2)" | **false** — receipts and route map untracked; L2 reports "route map absent" |
| r50-3 | "the aggregate round-overrun figure is now derived from committed bytes and named in LOG.md (L3)" | **false** — no figure, no timing, no accounting; LOG names none |
| r50-4 | "the ten inherited paths stay untouched and uncommitted" | **true** |

The r50-2 and r50-3 sentences are the r50-1 defect class — a present-tense figure claim with no
re-derivable artifact behind it — reproduced inside the round that claims to fix that class. This is
the single most useful finding for the L1: the contract's `routedDefectsAddressed` block reads as a
completion statement when two of its four entries are targets.

## 6. Claim state I reproduced (context; not my axis)

- C1: `C1 ledger 0/3 met=False`, exit 1, L1/L2/L3 each FAIL on an absent artifact. No run of mine
  produced anything else, and no seat could have: the artifacts are untracked.
- C2: `C2 quote-truth 8/8 met=True`, exit 0, all eight conditions pass at `9d13768c`.
- Frontier step: `corpus/SOURCES.md` at `9d13768c` holds **145** rows; S262 is line 152, S263 line
  153, both `status mined`, `opened 2026-10-24`, `recheck 180d`, last cell exactly the one admitted
  entry (`corpus/knowledge/canonical-selection.md`, `corpus/knowledge/crawler-identity.md`); both
  entries are present at the measured revision. The frontier step is landed.

## 7. The "able to fail" controls are transcripts, not evidence

`controls/c1-junk-wave.txt` cites revision `d969fa2819f1f2050c10637531cba2e12f92a557`;
`controls/c2-junk-entries.txt` cites `cc57cb80b2060f8c754a896235e323f67a5a91da`. Neither object
exists in the lane: `git cat-file -e <rev>^{commit}` fails for both, so both are **not in lane**.
The transcript cannot be reproduced by running the committed counter in the lane root — the reader
must reconstruct a synthetic repo. (The base controls *are* reproducible: I re-ran the base revision
and got `0/3 met=False` exit 1 for C1, which matches `controls/c1-before-base.txt`.)

This bears on r50-2 and r50-3: the demonstration that L2/L3 "can fail" is an artifact whose revision
a reader cannot open.

## 8. r50-4 — the ten inherited paths

Checked one path at a time with `git ls-files --error-unmatch <path>`: all ten fail (untracked).
`git diff --name-only 007d66e4…9d13768c | grep -E 'round-46/residual|round-48/assimilation/validate'`
prints **NONE**. `git log 9d13768c -- .ufo/waves/round-46/residual/` is empty; the only history on
the validate tree is `af7b217` (round 48, before this cycle). mtimes also predate this wave: residual
dir `2026-10-24 03:35`, validate copies `2026-10-20` / `2026-10-23`, wave start
`2026-10-25T06:32:17Z` (`.ufo/waves/round-51/wave-start-utc.txt`). They appear in
`git status --porcelain` only as `??`.

**Verdict: addressed (upheld).** Nothing was force-added, renamed or swept; the count is not
laundered. Confidence: high.

## 9. Bounds and tooling

- Read-only throughout. The only write is this file. No `git add/commit/stash/checkout/switch/
  reset/pull/push`, no mutating `jj`, no edit of `considerthese/`, `round-46/residual/`, the
  `>1MiB` round-48 copies, or the shokuknow tree.
- Scratch: `/tmp/r51probe` (throwaway git repo holding copies of the untracked route map and two
  receipts, used only to evaluate `check_l2`). Nothing under the lane or fleet repo was touched by
  it.
- Tool installs/upgrades: **none**. No pacman transaction was attempted (host-wide pause respected).
- Observation, not a defect claim: the worktree is diverged from the measured revision —
  `PROVINCE.md` (+15), `SCORECARD.md` (+33), and both admitted entries edited with a "round-51
  correction" section — all uncommitted. Every verdict above is against `9d13768c`, not the
  worktree; the C2 8/8 result I quote is the measured revision's, not the worktree's.

## 10. Confidence

| finding | confidence | basis |
|---|---|---|
| no round-51 wave evidence committed | high | `git ls-tree`, `git status --porcelain`, C1 run |
| r50-1 corrected figure is 25, not 26 | high | `git ls-tree … \| grep -c '\.md$'` = 25 |
| r50-1 literal correction absent | high | `.ufo/reports/round-51/` has no `kake.md` |
| L2 design accepts the committed receipts | high | `/tmp/r51probe` run: `L2 ok=True` |
| L2/L3 certificates bind to the map, not the dispatch | high | 48/48 payload seats carry no `model` |
| the failing receipt is a synthetic probe | high on the note, medium on the judgement | receipt `note` field |
| L3 dead-seat clause skips `no-report` | high | code read + builder read |
| L3 LOG clause can pass on a hash substring | high on mechanic, value-dependent | `417` found in a hash at LOG:947 |
| per-seat seconds come from mtimes | high (builder read) | untracked `build_wave_evidence.py` |
| r50-4 upheld | high | per-path `ls-files` + base→tip diff filtered |

Net: of the four routed defects, **one is addressed**, **three are partly addressed**; the two
that the contract describes in the present tense (r50-2, r50-3) are not yet true of committed bytes.
The wave's own C1 counter agrees: `0 of 3`.
