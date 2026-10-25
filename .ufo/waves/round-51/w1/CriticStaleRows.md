# CriticStaleRows — round-51 wave 1 (seat `CriticStaleRows`, critic; axis: freshness)

Measured revision: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (= `HEAD`).
Host clock at seat start: `2026-10-25T03:34:02-03:00` (`America/Sao_Paulo`; `2026-10-25T06:34:02Z`).

Two rulings, one hole, one adjacent-evidence section. No lane file was modified; scratch lives
in `/tmp/c51-stale-2` (fixture commits cited as witnesses only — every counter output and
numstat quoted below is inlined, so this report stands if the scratch tree is swept).
No tool was installed or upgraded.

**Ruling 1 — `opened 2026-10-24` against a run dated 2026-10-25: not a defect under CORPUS.md
rule 1 as written.**
**Ruling 2 — the Gate access dates match the carrying commit's date in the commit's own
recorded offset; they differ only under a UTC normalization that no rule requires.**

---

## Rule text relied on

From `/home/vgpnk/Projects/shokunin/CORPUS.md` (the only readable copy of the rule text: the
lane's `corpus/SOURCES.md` has no `### Rules` section — `grep -n '### Rules' corpus/SOURCES.md`
prints nothing, exit 1).

Field definition, `CORPUS.md:105-106`, quoted verbatim:

````text
- `opened` — ISO date the row's author opened the source. `recheck` — ISO date or cadence
(`90d`, `180d`, `on-release`).
````

Rule 1, `CORPUS.md:112-115`, quoted verbatim:

````text
1. **A row is a claim.** Write it only after opening the source in the round that writes
   the row. The round lesson's `## Gate` records, for every new row, the URL, the access
   date, and a ≤25-word quote with its location grounding `teaches`. Non-author
   verification re-opens a sample.
````

Rule 2, `CORPUS.md:116-118`, quoted verbatim, bounds the repair available:

````text
2. **Append-only.** Only `status`, `recheck` and `used-by` change in place, and each change
   is logged old→new in the round lesson. A correction is a new row whose `teaches` opens
   `supersedes S0NN —`.
````

The rule as written names (a) the round that writes the row and (b) the access date. It does
**not** name the calendar day on which the wave/run happens, and it does **not** name a timezone.

## What this seat measured (every number below was re-derived here)

| check | command | output |
|---|---|---|
| C2 at tip | `python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768…` | `C2 quote-truth 8/8 met=True`, all C1–C8 pass, exit 0 |
| carrying commit | `git log -1 --format='%h %cI %aI %s' 5591557` | `5591557 2026-10-24T23:20:56-03:00 2026-10-24T23:20:56-03:00 round-51: append S262 and S263…` |
| which commits touch the lesson | `git log --format='%h %cI' -- corpus/lessons/round-51.md` | only `5591557 2026-10-24T23:20:56-03:00` |
| round-open commit | `git log -1 --format='%h %cI %aI' 19a99bd` | `19a99bd 2026-10-24T23:20:47-03:00 2026-10-24T23:02:31-03:00` |
| access receipt | `.ufo/waves/round-51/sources/receipts.json` | `"fetchedAt": "2026-10-24T23:16:49-03:00"` |
| wave start | `cat .ufo/waves/round-51/wave-start-utc.txt` | `2026-10-25T06:32:17Z` |
| registry cells | `awk -F'\|'` over the two rows | `opened=2026-10-24`; `recheck= 180d` (both) |
| entry metadata | `head -2` of both entries | `fetched 2026-10-24`; `verified-at: 2026-10-24` |

Instants, one frame each:

- fetch `2026-10-24T23:16:49-03:00` = `2026-10-25T02:16:49Z`
- carrying commit `2026-10-24T23:20:56-03:00` = `2026-10-25T02:20:56Z`
- round open `2026-10-24T23:02:31-03:00` = `2026-10-25T02:02:31Z`
- wave start `2026-10-25T06:32:17Z` = `2026-10-25T03:32:17-03:00`
- fetch → wave start `4:15:28`; commit → wave start `4:11:21`; fetch → commit `4:07`

## Ruling 1 — `opened 2026-10-24` while this run is 2026-10-25

**Not a defect under rule 1 as written.** Rule 1 asks two things, and both hold:

1. *"Write it only after opening the source in the round that writes the row."* The row was
   written in round 51. Round 51 opens at `19a99bd` (author time `2026-10-24T23:02:31-03:00`);
   the source was opened at `23:16:49` and the row landed at `23:20:56` — strictly inside the
   round, in the order round open < fetch < commit. The wave that runs on 2026-10-25 is round
   51's wave, not a new round.
2. *"The round lesson's `## Gate` records, for every new row, the URL, the access date, and a
   ≤25-word quote with its location."* Both Gate lines carry the URL, `accessed 2026-10-24`,
   and a quote under 25 words (`round-51.md:8-9`). The quote strings themselves are raw
   substrings — `grep -cF 'indicating a canonical preference is a hint, not a rule'` → 1 in
   `S262.html`; `grep -cF 'Googlebot is the generic name for two types of'` → 1 in `S263.html`.

The `opened` cell is defined as *"ISO date the row's author opened the source"*. The author's
own calendar day at the access instant is 2026-10-24 (`-03:00`, the offset the receipt itself
records). The run being on 2026-10-25 is a different fact about a different instant; the column
records the access, not the wave.

The "stale" reading does not survive either clock:

- author-local frame: access 2026-10-24, run 2026-10-25, gap 4h15m — the row was written four
  hours before the wave started, not carried over from an earlier round.
- UTC frame: the access is `2026-10-25T02:16:49Z` — the **same UTC day** as the run. No frame
  makes the row a prior-day artifact relative to the run's UTC date.

Registry census (my own derivation, 145 rows, introducing commit per row):

```
rows whose introducing commit straddles UTC midnight: 18
opened == commit local date: 138 / 145
opened == commit UTC date:   134 / 145
```

Of the 18 straddling rows, 11 record the `-03:00` date and 7 record the UTC date
(`S088`–`S094`, round 36, commit `4d5b3d5 2026-10-22T22:54:39-03:00`). The 11 local-date rows
are `S131`/`S132` (round 44, `297aa62`), `S137`–`S139` and `S249` (round 48, `af7b217c`),
`S273`/`S274` (round 49, `1c846ed`), `S286` (round 50, `ff3f6ec`), and `S262`/`S263` (round 51,
`5591557`). Every straddling append in rounds 48–51 is local-date; the UTC exceptions are all
one commit in round 36. S262/S263 follow the dominant and the recent precedent.

Counter consequence (fixture `/tmp/c51-stale-2`, evidence files copied from the lane, history
built so the mirror is an ancestor):

- pristine fixture, rows at `2026-10-24`: `C2 quote-truth 8/8 met=True`, exit 0 (fixture commit
  `1d9dcce`).
- one change off that commit, `git diff --numstat` = `2 2 corpus/SOURCES.md` and nothing else —
  the two `opened` cells set to `2026-10-25`: `C2 quote-truth 7/8 met=False`, exit 1 (fixture
  commit `256f47ae`), failing notes verbatim:
  `S262: registry opened is '2026-10-25', expected '2026-10-24'` and the same for S263.

So "correcting" the rows to the run day would falsify the frozen claim. The expected date was
frozen with the declaration commit `19a99bd` (`ROUND_DATE = "2026-10-24"`, line 46; authored
`2026-10-24T23:02:31-03:00`, committed `23:20:47`, nine seconds before the append commit) — it
was not fitted after the row landed. Independently, rule 2 forbids changing
`opened` in place; a "fix" would need a superseding row, which this evidence does not warrant.

**What would have made it a defect:** `opened` later than the carrying commit (forward-dated),
`opened` earlier than the round open (a prior round's access), or a Gate access date that no
retained receipt supports. None of the three holds.

## Ruling 2 — Gate access dates against the commit dates that carry them

**They match in the commit's recorded offset.** Both Gate lines say `accessed 2026-10-24`; the
only commit carrying them is `5591557`, whose `%aI` and `%cI` are both
`2026-10-24T23:20:56-03:00`, i.e. date `2026-10-24`. The access receipt
(`2026-10-24T23:16:49-03:00`) and the rows' `opened` cells are the same date; the entries'
`fetched` and `verified-at` fields are the same date. Five artifacts, one date, no internal
contradiction.

They do **not** match under a UTC normalization: the carrying commit and the fetch are both
`2026-10-25T02:1xZ`, so a UTC-normalized commit date is `2026-10-25` while the Gate says
`2026-10-24`. That is the only sense in which the dates disagree. Rule 1 says "the access date"
and names no zone; the only offset any artifact records is `-03:00` (the receipt's own
`fetchedAt`). The commit's own date string is `2026-10-24`. I therefore hold the comparison to
the recorded offset, where they match.

## Finding (mine, not the assigned ruling): C2 does not defend the Gate access date at all

No condition in `c51_quote_truth.py` reads the word `accessed`. C5 checks the quote only
(`c51_quote_truth.py:208-219`); C3 checks the row's `opened` against the hardcoded `ROUND_DATE`.
I falsified the Gate dates in the passing fixture — `accessed 2026-10-24` → `accessed
1999-01-01` on both Gate lines (exactly two replacements, asserted), a change whose
`git diff --numstat` against the pristine fixture commit is `2 2 corpus/lessons/round-51.md`
and nothing else — and the counter still printed:

```
C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)
no condition failed
exit 0        (fixture commit 8c9bd7a6)
```

So the committed C2 8/8 is compatible with any Gate access date. The committed dates are true,
so this is not a miss on C2 as frozen; it is a hole in what the claim proves for the freshness
axis. Smallest safe correction, for the next round, not retrofitted mid-round: one additional
condition requiring each Gate access date to equal the `receipts.json` `fetchedAt` date in that
file's own offset (and, for the row, `opened` to equal the same). That makes the date
re-derivable from committed bytes instead of resting on the lesson's prose.

## Adjacent evidence found while grounding the Gate (not the assigned ruling; no verdict claimed)

- **Gate locations are not headings.** S262 cites `§ "What is URL canonicalization"`; the
  retained body's only `h1` is `What is canonicalization` (`<h1 ... id="what-is-canonicalization"
  data-text="What is canonicalization">`), and the cited string occurs once as a
  `devsite-nav-title` (navigation label). S263 cites `§ "Googlebot is the generic name for two
  types of web crawlers used by Google Search"`; the body's `h1` is `Googlebot`, and that
  sentence is the opening paragraph, interrupted by an `<a>` around "web crawlers", so the
  cited string is not a raw substring (`grep -cF` → 0). Rule 1's "its location" clause is
  therefore only nominally satisfied; the counter never checks it.
- **A negative claim in the lesson is false.** `round-51.md:78-85` says the staged phrase
  "Google chooses the most complete and useful page as the canonical URL" is "not in the
  source" and "confirmed absent from the bodies this round fetched". The retained
  `S262.html` carries it once (offset 145222), inside
  `<div class="devsite-content-data-template">` as the page's content-data summary; the prose
  paragraph separately says "objectively the most complete and useful for search users". The
  absence claim needed its sweep and does not survive one.
- **Not a date issue, observed while checking ancestry:** at `9d13768` the committed mirror
  blob and the live registry are byte-identical
  (`sha256 4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3`, 145 rows each),
  so the "pre-append" mirror file at the measured revision already carries S262/S263. C8 reads
  the live registry at the mirror commit (`19a99bd`, 143 rows, neither id), so C8's substantive
  check is sound; C7 checks only the census receipt's shape. A corrected mirror
  (`sha256 cd9ee4cf…`, 143 rows) exists in the worktree but is uncommitted at this revision.
  Adjudication of that defect belongs to the seat that owns the mirror diff, not here.

## Trend verdicts

- Freshness, assigned question: **no defect**. The rows and the Gate record the true access
  date for the round that wrote them; the run date differs only by the calendar frame, and the
  source is 4h15m old at wave dispatch.
- Freshness, instrument: **one hole** — C2 verifies the quote but not the access date, so the
  freshness claim's 8/8 would survive a falsified Gate date. Recorded above with the smallest
  safe correction.
- Date convention: **latent ambiguity** — the registry mixes `-03:00` and UTC dates across the
  seven round-36 straddle rows. Not a defect in S262/S263, which follow the dominant recent
  precedent, but a candidate for a one-line convention note rather than a row edit.
