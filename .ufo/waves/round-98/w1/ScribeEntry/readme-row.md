# README Entry-table row for the C2 knowledge entry

Draft row for `corpus/README.md`, in the column shape the round-97 coverage-index
rows use (Area | Entry | Coverage). It is a draft for the integrating step to
apply; this file changes nothing in the lane.

## The row

```
| Stale-serving extensions decision (r98) | `knowledge/stale-extensions.md` (S482, S483, S480, S478) | Whether a stale stored response may be served on a request or on an error, and for how long, decided over supplied values under contract v1; no live cache, no storage, no revalidation scheduling |
```

## Where it goes

Two tables in `corpus/README.md` carry the header `Area | Entry | Coverage`:
the `## Coverage map` table at line 15, and the `## Coverage index — round 97
(calibration repair)` table at line 794 (both at master `7838981e`). The row
above is written to drop into either.

The round-97 table is titled "one row per knowledge entry whose earlier index
row was missing or omitted source ids" — it is the r97 repair, and it stays as
filed history. A round-98 entry is therefore either a new row in the
`## Coverage map` table, or a row in a round-98 section of the same shape that
the L1 adds. This matters for the counter, not for the prose: the coverage-index
counter admits an entry only when some row carries **every** source id of that
entry's `source:` line, and the `## Coverage map` table carries ids in some rows
and not in others. This row carries all four, so it satisfies the counter
wherever it lands.

## Column check

- **Area** — "Stale-serving extensions decision (r98)": the entry's title in
  the lane's own words, matching the naming of the r91/r92/r93 rows
  ("Stored-response reuse decision (r91)", "Heuristic freshness decision
  (r92)", "Conditional request evaluation (r93)").
- **Entry** — the backticked token `knowledge/stale-extensions.md`, which is
  what the coverage-index counter's `TOKEN` pattern
  (`` `(?:corpus/)?knowledge/([^`/\s]+\.md)` ``) resolves the entry by, plus
  the four source ids of the entry's own `source:` line in parentheses, which
  is where the round-97 rows carry theirs.
- **Coverage** — the coverage sentence, drawn from the entry's `scope:` line
  and its "What this entry does not decide" list: one decision per supplied
  value, under contract v1, and the three things the entry does not claim.
- **Source ids** — `S482` (RFC 5861), `S483` (the RFC 5861 errata record),
  `S480` (RFC 9111) and `S478` (RFC 9110 §5.6), the four ids the entry's
  `source:` line names. No other id appears in the row.

## Coverage-index counter check

The row was checked against the coverage-index counter's own rules
(`.ufo/waves/round-97/c97_index.py`, `audit()`): the Entry cell carries the
backticked token; every id in the entry's `source:` line appears in the row
line; the row's other cells hold at least 8 words, of which at least 2
distinct words of at least 6 letters also occur as words in the entry's own
text. The check and its observed output are in `readme-row-check.txt`.
