# ReviewGateAndRowLog — review of `## Gate` in corpus/lessons/round-34.md @ 24a1647

Verdict input: the Gate section meets the assigned contract. No defect found; two
nits below. Independent re-verification script and clone in
`/fast/scratch/hyaku/kake-r34/w2/ReviewGateAndRowLog/` (`verify_gate.py`, `clone/`).

## Assigned check (ran verbatim)

`python3 -B .ufo/waves/round-34/criteria/gate_reject_check.py --repo
/home/vgpnk/Projects/shokunin/kake-shokunin --rev
24a16474ee73e20453f3e1be9d2f33573c5196d9 --lesson corpus/lessons/round-34.md`
→ exit 0, `MATCH: corpus/lessons/round-34.md:38` (the S071 reject bullet, first
qualifying line). Note the check is shallow — it stops at the first matching
reject; coverage of all 11 lines came from my own parse (below).

## Per-Gate-line verification (11 bullets, S067–S077)

Parsed each bullet for URL / accessed / decision / status / quote / location,
then checked against committed bytes (clone @ 24a1647):

- Every quote is an exact substring of the retained text `.ufo/waves/round-34/sources/S0XX.txt`:
  S067 @byte955 (8 words), S068 @1382 (23), S069 @671 (13), S070 @3020 (14),
  S071 @45 (15), S072 @3016 (16), S073 @3061 (16), S074 @41784 (21),
  S075 @0 (2), S076 @14 (16), S077 @3736 (12). All ≤25 words; every printed
  count equals the recount.
- Every URL and `accessed` timestamp equals `sources/receipts.json` `url` /
  `accessedUtc` (S068 and S071 parenthetical finals equal `finalUrl`).
- Decision ↔ status ↔ SOURCES.md row status agree on all 11 rows
  (admit→mined ×5, reject→rejected ×4, queue→queued ×2).
- Location hints resolve: `Basic Metadata` (S067.txt), `Open Graph Markup`
  (S068), `Slackbot-LinkExpanding` (S069), `PreviewCard`/`link_preview_options`
  (S070/S074), `What it does` (S077); S075's "entire visible text" is literally
  the whole 15-byte file.
- Rejects carry located reasons, and the reasons are true in the bytes:
  S071.txt has 0 `og:` and 0 `meta` matches and exactly one `card` — inside
  "payment card and a match of the first auto-recharge"; S074.txt (494,103 B,
  receipt `textWords` 73,876 matching the Gate's "73,876-word") has 0 `og:`,
  0 `opengraph`, 0 `og[_%]`; S075.txt is 15 bytes "Post Inspector".

## Row-change log vs. the registry

`git diff 1e54c89..24a1647 -- corpus/SOURCES.md`: 11 added lines, **0 deleted**
→ all new rows; no existing row's status/recheck/used-by touched, matching the
lesson line. New rows S067–S077 all have Gate lines (none missing). Row tail
cells match the lesson's old→new log exactly: mined rows used-by
`corpus/knowledge/link-preview-metadata.md` (S073 is really cited there: 4
`S073` mentions in the entry), rejected/queued rows used-by `—`, opened
`2026-10-22`, recheck `90d`. Timing claim holds: S067–S072 receipts 20:57:39–42Z
precede declaration commit d08d8de (2026-10-22T18:00:16-03:00 = 21:00:16Z);
S073–S077 21:08–21:09Z land in 9ef758c (21:13:49Z). Screened-not-rowed claims
corroborated by `w1/ScoutMoreSourceLeads.md` (LinkedIn help 404s L19,
raw.githubusercontent README 404s L22, Discord resource pages folded L20) and
`w1/ScoutXCardsLocation.md` (docs.x.com cards paths 404, byte-identical S071
body rehash).

## Nits (not defects)

- S073's location label "Requirements list" is descriptive, not a literal
  heading: `Requirements` appears 0 times in S073.txt; the quote sits in the
  enumerated list under "How Discord Reads Your Page".
- `gate_reject_check.py` itself only proves ≥1 reasoned reject exists; the
  round-34 section's four rejects were each confirmed only by manual check.

## Not verified

Truth of the external pages themselves (no refetch — only retained bytes were
checked); quotes were verified against `S0XX.txt`, not re-derived from
`S0XX.html.gz`. Tools installed: none (stock `git`, `python3` sufficed).
