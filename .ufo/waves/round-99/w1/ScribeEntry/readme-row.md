# Coverage-map row draft for the round-99 C2 knowledge entry

The entry this row names is `corpus/knowledge/freshening-304.md`. The row
below is in the shape the existing `corpus/README.md` coverage-map table uses:
an area label with the round, the entry path with its source rows, and a
one-sentence coverage statement that names what the entry decides and what it
does not.

## The row

| Area | Entry | Coverage |
|---|---|---|
| 304 freshening decision (r99) | `knowledge/freshening-304.md` (S484, S485) | Which stored responses a 304 (Not Modified) identifies for update and which of their header fields it changes, decided over supplied values under contract v1; no initial-set computation, no live cache |

## Placement

Round 98 added its row under its own section at the end of the file, following
the shape of the section header and the paragraph above it. The equivalent
round-99 section would be appended after the round-98 block, in this form:

    ## Round-99 frontier step — 304 freshening

    New ground this round: RFC 9111 §4.3.4 and §3.2 (S484, opened 2026-11-05;
    erratum EID 9185 Reported, not Verified, S485), decided under contract v1
    (`.ufo/waves/round-99/fresh304-contract.md`). Still open: the initial-set
    computation (§4 reuse conditions, keys, Vary), HEAD freshening (§4.3.5),
    invalidation (§4.4), trailer fields, and any observation of a live cache.

    | Area | Entry | Coverage |
    |---|---|---|
    | 304 freshening decision (r99) | `knowledge/freshening-304.md` (S484, S485) | Which stored responses a 304 (Not Modified) identifies for update and which of their header fields it changes, decided over supplied values under contract v1; no initial-set computation, no live cache |

## Shape check

The row matches the existing table's three columns and its punctuation: the
area cell ends with the round in parentheses, the entry cell carries the
backticked `knowledge/` path followed by the source rows in parentheses, and
the coverage cell is one sentence naming the decision, the governing contract
version, and the limits. It follows the rows added at rounds 91, 96 and 98,
each of which names the decision first and the exclusions last.
