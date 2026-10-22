# KakeR35.ScribeGateLines — round-35 lesson `## Gate` source-opening lines (wave 1)

Axes: freshness (Gate provenance for the C2 sources) and operability (the L1 can re-run every
check). I did not touch `/fast/scratch/hyaku/kake-r35/sealed/`; I made no network request (all
nine texts were read from the round-35 retained sources); I installed no tool; I wrote nothing
in the lane except this report.

## Built

`/fast/scratch/hyaku/kake-r35/w1/ScribeGateLines/gate.md` — nine lines, one per source in
assignment order S078-S085 plus the S006 re-open, in the shape of `corpus/lessons/round-34.md:34-44`:
`- S0NN — URL — accessed <UTC>, HTTP <status> — <decision>, tier <T>, kind <K>, status <S>: <reason>;
quote “…” (<location>; <N> words).` All nine HTTP statuses are 200. sha256
`6b82bcd6b52d275c66b7b2d5b8f5d03a03cf4fadec0ccab734968f8a6e7075b1`.

Decisions: admit/mined S078 (spec A), S080 (docs A), S082 (spec A), S083 (dataset A), S084
(dataset A), S085 (dataset A), S006 (docs A, re-open, status unchanged); admit/mined S079
(docs B, restates the RFC rather than norming it); reject/rejected S081 (community C, located
at its File format section).

## Commands, exit codes, observed output

1. `cd /fast/scratch/hyaku/kake-r35/w1/ScribeGateLines && export TMPDIR=$PWD/tmp && python3 -B verify_quotes.py`
   → **exit 0**. Nine lines of `S0NN exact=True words=N index=I textSha256=…`, e.g.
   `S078 exact=True words=13 index=16094`, `S081 exact=True words=22 index=3037`,
   `S083 exact=True words=6 index=9100`, each followed by the matched context; no `MISSING`,
   no word-count warning. First run of this command was **exit 1** on S078 (`exact=False`); see
   finding 1. Output saved to `gate-check.txt`.
2. `python3 -B check_gate.py` → **exit 0**. It parses `gate.md` against
   `.ufo/waves/round-35/sources/receipts.json` and prints `gate lines: 9` then `S0NN OK` for all
   nine, with `quoteWords == stated` for each; the checks are sid, url, accessed time, HTTP
   status, decision, tier, kind, row status, `quote_exact`, 6<=words<=25, non-empty location,
   reason >=4 words. Last line: `S081 decision reject: True | located reason: True`.
3. Hash check of every retained text against the receipt (`python3 -c` over `receipts.json`,
   full `textSha256` comparison) → all nine `text_sha_match=True`, e.g. S078 `4954ddcd…`,
   S081 `1af8954e…`, S084 `35cf4b7b…`.
4. `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 318561ef:corpus/SOURCES.md | grep -c -E '^\| S0(7[89]|8[0-9]) '`
   → **exit 1**, count `0`: no S078-S089 row exists at the base revision, so the nine lines add
   eight rows and only S006 re-opens an existing row. `git rev-parse --short=12 master` → `318561efa672`.

## Findings for the L1 and the C2 entry

1. S078's retained text keeps the RFC's line-wrap hyphenation: it reads `.well- known` across the
   break. My first quote, which spelled `.well-known/security.txt`, failed `quote in text`
   (`exact=False`); the kept quote stops at `...path`. A C2 quote that crosses that wrap fails
   the same way.
2. S081's rejection is located, not asserted: its whole File format section is two sentences
   (`S081.txt` index 3016-3268) and the 979-word page has 0 occurrences of `Expires`, 0 of
   `Jekyll`, 0 of `Canonical`, and 1 of `GitHub` (the adopter list in History). Its location
   sentence also omits the RFC's rule that the `/.well-known/` copy wins.
3. S084's `Expires: 2026-11-21T22:02:20z` is the receipt access time 2026-10-22T22:02:20Z plus
   exactly 30 days, same seconds. [INFERENCE] GitHub mints the value per request; one
   observation cannot separate a per-request value from a coincidentally fresh static one, so
   the Gate line does not claim it.
4. S085's `Expires: 2030-04-01T00:00:00z` is over three years out, while RFC 9116 §2.5.5 only
   RECOMMENDS under one year (verified in S078's retained text). The C2 entry should not equate
   "valid" with "meets the recommendation".
5. The status words are proposals for the registry seat: no C2 entry exists at 318561ef, so a
   `mined` cell only holds if `used-by` cites it in the landed commit. S006 is re-opened, not
   re-tiered: its existing row stays `docs | A | mined | 90d`.
6. Kind choices to reconcile: S084/S085 are `dataset` (raw served response bodies, as S066 was
   for an API capture), S083 is `dataset` (registry table), S079 `docs`/B.

## Not verified / out of scope

- I did not run either sealed counter and did not read under `/fast/scratch/hyaku/kake-r35/sealed/`.
- I did not write or inspect a C2 entry and make no statement about the 9-of-12 probe target.
- SOURCES.md row cells (scope, anchor, teaches) are the registry seat's text; my lines fix only
  URL, access time, HTTP status, decision, tier, kind, status word, reason and quote.

## Artifacts (sandbox)

- `/fast/scratch/hyaku/kake-r35/w1/ScribeGateLines/gate.md` — sha256 `6b82bcd6…075b1`
- `/fast/scratch/hyaku/kake-r35/w1/ScribeGateLines/verify_quotes.py`, `check_gate.py`
- `/fast/scratch/hyaku/kake-r35/w1/ScribeGateLines/gate-check.txt` — sha256 `15ae49d9…58e2`
