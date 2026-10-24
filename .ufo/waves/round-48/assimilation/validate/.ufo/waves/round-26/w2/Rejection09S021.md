# Rejection09S021: falsify attempt on L1's rejection of the S021 verified-at finding

Target: the L1 disposition for S021 row 2, `w1/PairS021StaticCanonicalPrefl.md` (Correction A). The seat marked `verified-at: 2026-10-20 (S020-S027)` STALE because the date was "superseded". L1 rejected that: `statements.json` S021 pair, l1Disposition `"row 2 date stamp only; ..."`, with `seatStale 3` and `stale 1`.

Axis: freshness. Verdict: **AGREE** with the rejection. I could not show that the statement is wrong at its stated scope, and no staleness is hidden.

## Axes tested

1. Truth at scope: did an S021 reading actually happen on 2026-10-20, in the round that line 2 names ("documentation opened this round")?
2. Version continuity: did the 2026-10-20 reading see the same document version as the 2026-10-21 bytes?
3. Rule fit: does `QUALITY.md` "Recheck adjudication — round 26" classify a superseded verified-at date as STALE or as a note?
4. Hidden staleness: does rejecting the row drop any later reading that the entry fails to record?

## Evidence

**1. The line was written on 2026-10-20 at the round-22 opening.** `git log -L2,2` on the entry at 97404de:
- c0fd6d5 `2026-10-20 18:30:55 -0300` "round-22: offline canonical publishing preflight" created the line as `verified-at: 2026-10-20, documentation opened this round`. That is 21:30 UTC, still 2026-10-20.
- b539cc1 `2026-10-21 03:16:39 -0300` narrowed it to `2026-10-20 (S020-S027) and 2026-10-21 (S028-S029)`. S021 falls inside S020-S027.
- At 97404de, `.ufo/waves/round-22/w1/GoogleCanonical.md` (added by c0fd6d5) records `**Access date:** 2026-10-20`, the same URL, and `page states "Last updated 2026-07-10 UTC"`.
- At 97404de, the round-22 Case14, Case16 and Case17 files say "Observed 2026-10-20" and "accessed 2026-10-20". `SOURCES.md:29` (the S021 row) reads `updated 2026-07-10, opened 2026-10-20`.

**2. Same document version.** `fetched/manifest.json` row S021: status 200, finalUrl equal to the url, `last-modified: Fri, 10 Jul 2026 10:12:15 GMT`, sha256 `4edda778…c7e5c5`. I counted each verbatim quote from the round-22 scout in `fetched/text/S021-1.txt`; each one occurs exactly once:
- `The rel="canonical" link element is only accepted if it appears in the <head> section of the HTML`
- `Use absolute paths rather than relative paths with the rel="canonical" link element.`
- `Even though relative paths are supported by Google, they can cause problems in the long run`
- `As with the rel="canonical" link element, use absolute URLs in the rel="canonical" HTTP header.`
- `Do include a rel="canonical" link on the canonical page itself (also known as a self-referential canonical).`
- `Don't specify a URL fragment as canonical, as Google generally doesn't support URL fragments.`
- `Last updated 2026-07-10 UTC`

So nothing that the 2026-10-20 reading relied on has drifted. The date is not a false claim of currency over changed bytes.

**3. The rule points to a note, not STALE.** `corpus/QUALITY.md:216-220` says: "STALE means the statement is wrong or unsupported at its own stated scope. A historical verified-at date, a pointer explicitly scoped to a base revision, or a patch-version label in the same documented family is not a stale claim; record it as a note." The ledger rule in `statements.json` says the same: "Historical dates and base-scoped pointers are not stale." The seat's own reason is "superseded by 2026-10-21 observations", which is a currency argument, not falsity. The round-21 rule (`QUALITY.md:46-49`) also says "A provenance header records the original evidence date/revision… installing a header is never live re-verification." Line 2 is that kind of header and makes no claim of being the latest check.

**4. Nothing is hidden.**
- At base, the entry already records the later reading. Line 96 is the heading `## Round 23: body markup, live snapshots, corrections (2026-10-21)`, and the [r23-correction] at lines 140-142 cites S021.
- The candidate e28312b adds the required note under `## Round-26 source recheck`: "Older verified-at/reopened dates in this entry remain the historical record of the earlier reading; they are not rewritten." The same paragraph lists S021 among the rows re-fetched and judged HOLD.
- The round-26 SOURCES summary also logs the 2026-10-21 re-fetch.

The newer observation is therefore on record, and the rejection loses no freshness signal.

## Strongest counterexample tried, and why it fails

A reader of line 2 alone might take 2026-10-20 as the latest S021 verification. That reading is outside the line's stated scope, which is "documentation opened this round" (round 22). The round-21 rule makes headers historical by construction. A STALE marker here would also break append-only discipline, because it labels a true historical fact as wrong. The fix the seat wanted, surfacing the newer date, is already delivered by the round-26 note.

## Residual observations (no verdict change)

- The seat applied the wrong rule: it marked row 2 STALE against `QUALITY.md:216-220`. L1 corrected that. This is a seat defect, not a ledger defect.
- The l1Disposition text "date stamp only" names no rule. Citing "QUALITY.md round-26: historical verified-at date" there would make the rejection self-explaining. This is cosmetic.
- I did not do a live GET. The retained bytes and the base-revision history were enough.

## Verification exercised

These were all read-only: `git log -L2,2` and `git show`/`git grep` at 97404de, `git diff 97404de e28312b` on the entry and on SOURCES.md, a stdlib Python quote count over `fetched/text/S021-1.txt`, and a manifest row read. I wrote nothing except this report. I installed and updated no tools.

```json
{"target":"S021 row 2 L1 rejection (verified-at 2026-10-20 date stamp)","verdict":"AGREE","severity":"none"}
```
