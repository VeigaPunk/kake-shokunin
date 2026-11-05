# S480 — finalized SOURCES row (contract v1 schema, 11 cells)

Finalized by ScribeEntry (kake round 96, w1), from ScoutRFC's opened-source draft
(`.ufo/waves/round-96/w1/ScoutRFC/s480-row.md` and `fetch.txt`). **Not appended**: the
L1 integrates it through the round gate. This file is a draft and a receipt; it
changes nothing in the lane.

Insert position: after the S479 row (`corpus/SOURCES.md` line 225 at base
`bde9869144f69c5a459c0d2c93f5135922fe3a8d`, the last row of `## Registry`), so the new
row lands at line 226.

## The row

```
| S480 | RFC 9111: HTTP Caching, section 4.3.1 Sending a Validation Request and section 4.3.3 Handling a Validation Response - https://www.rfc-editor.org/rfc/rfc9111.txt | spec | A | How a cache constructs a conditional validation request for a stored response and how it handles the response it receives: that it must send the stored entity tags, should send the stored Last-Modified value, that both validators are usually generated together, that a 304 updates and reuses the stored response, that a full response replaces it, and that a 5xx leaves the cache free to forward or reuse a stored response; not the lane's supplied-values convention, not any live cache's behaviour, not storage, freshness lifetime, cache keys, serving or the merged header field set of a 304; distinct section and scope from S476's 4.3.2 origin-side reading, S470's heuristic-freshness reading and S456's broader storage-and-freshness reading | Section 4.3.1 heading plain-text line 812, MUST entity-tag bullet lines 848-850, SHOULD Last-Modified bullet lines 852-854, both-validators sentence lines 861-864; Section 4.3.3 heading plain-text line 930, 304 bullet lines 935-936, full-response bullet lines 938-942, 5xx bullet lines 944-949; June 2022; fetched 2026-11-05T18:17:11Z HTTP 200, 84477 bytes, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e; retained body .ufo/waves/round-93/L1/src/rfc9111.txt (cmp identical to the fetched body); fetch receipt .ufo/waves/round-96/w1/ScoutRFC/fetch.txt | A cache builds a validation request from the stored response's own validators and then reads the response status to decide reuse: the entity tags MUST be sent, the Last-Modified value SHOULD be sent, both validators are usually generated together ("In most cases, both validators are generated"), a 304 updates and reuses the stored response, a full response replaces it, and a 5xx lets the cache forward the error or reuse a stored response | queued | 2026-11-05 | 180d | corpus/knowledge/revalidation-exchange.md, corpus/lessons/round-96.md |
```

## Cell check

- **Cells: 11.** `python3` — `len(row.split('|')[1:-1]) == 11` → True. Every pipe in
  the row line is a column delimiter; no cell holds a literal or escaped pipe
  (`'\\|' in row` → False; no `|` occurs inside any cell's text). The `i.e.,` inside
  the RFC fragment of the contract's clause C5 carries a comma, not a pipe, and no
  cell needed a comma to be split on.
- **kind** `spec` (census enum: spec, docs, paper, code, tool, dataset, talk, book,
  community, own-work). **tier** `A`, scoped to RFC 9111 §4.3.1/§4.3.3 only — the RFC
  Editor's own publication of the cache-validation clauses is primary for that scope.
- **scope** is distinct from every other scope already carried under the same URL
  (`www.rfc-editor.org/rfc/rfc9111.txt` at S456, S467, S469, S470, S476), so the
  census's E04 duplicate-URL-within-scope rule cannot fire on this row. The scope
  states what the row teaches and, following the lane's row convention, what it does
  not teach (the supplied-values convention, live-cache behaviour, storage,
  freshness lifetime, cache keys, serving, and the merged header field set of a 304).
- **The `teaches` cell carries a verbatim quote** — "In most cases, both validators
  are generated" (7 words, under the 25-unit bound in `corpus/QUALITY.md`). `python3`
  — `q in body.read()` → True; `q in body_lines[860]` → True (the raw single line, so
  the fragment sits at plain-text line **861** of the body, byte-identical to the
  fetched body); `q in row` → True. The fragment grounds the both-validators half of
  `teaches`; it is a raw substring of the retained body, not a reconstruction.
- **status** `queued`. The freeze's Sourced-claim requirement reserves the `mined`
  decision for the L1; this seat does not flip it.
- **opened** `2026-11-05`, **recheck** `180d` (the retained body is byte-identical to
  the round's fetch and to the freeze's expected digest; RFC 9111 is a published
  specification with a fixed revision, so the cadence is a re-read cadence, not a
  "the content may have moved" cadence).
- **used-by** `corpus/knowledge/revalidation-exchange.md, corpus/lessons/round-96.md`
  — the C2 knowledge entry the freeze's *Sourced-claim requirement* names, and the
  round-96 lesson the freeze's non-claim work creates
  (`corpus/lessons/round-96.md` `## Mistakes`). **Caveat for the L1:** the census's
  E11 check runs only on `mined` rows, so neither not-yet-existing path fires today;
  if the row is flipped to `mined` before both the knowledge entry and the round-96
  lesson are committed, E11 fires. Flip the status only after both land.

## Source and quote grounding

- One GET, `https://www.rfc-editor.org/rfc/rfc9111.txt`, HTTP **200**, **84 477
  bytes**, sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`,
  accessed `2026-11-05T18:17:11Z` (ScoutRFC's receipt:
  `.ufo/waves/round-96/w1/ScoutRFC/fetch.txt`). The digest equals the freeze's
  expected digest **and** the sha256 of the retained round-93 body
  `.ufo/waves/round-93/L1/src/rfc9111.txt`.
- This seat re-derived the body identity rather than taking it on trust:
  `sha256sum` of both bodies → the same digest; `wc -c` → 84 477 each;
  `cmp .ufo/waves/round-93/L1/src/rfc9111.txt
  .ufo/waves/round-96/w1/ScoutRFC/rfc9111.txt` → **rc 0**, no output. Receipt:
  `quotes-verified.txt` (the body-identity lines) and the seat report.
- The six clause quotes the contract v1 names are located on those bytes with
  `grep -n -F` (each an exact substring of the line it is named at):

| expected line | fragment | found line | words |
|---|---|---|---|
| 848 | MUST send the relevant entity tags | 848 | 6 |
| 852 | SHOULD send the Last-Modified value | 852 | 5 |
| 861 | In most cases, both validators are generated | 861 | 7 |
| 935 | A 304 (Not Modified) response status code indicates | 935 | 8 |
| 938 | A full response (i.e., one containing content) indicates | 938 | 8 |
| 944 | However, if a cache receives a 5xx (Server Error) response | 944 | 10 |

  **6/6 located**, at the named lines. Because the fetched body is byte-identical to
  the retained round-93 body, these line numbers are also the retained body's line
  numbers — which is what the contract's §4.3.1/§4.3.3 clauses cite.
- Section headings on the same body: line 801 `4.3.  Validation`, line 812
  `4.3.1.  Sending a Validation Request`, line 866 `4.3.2.  Handling a Received
  Validation Request`, line 930 `4.3.3.  Handling a Validation Response`, line 951
  `4.3.4.  Freshening Stored Responses upon Validation`. The anchor cites §4.3.1 and
  §4.3.3 only; §4.3.4 (the merged field set of a 304) is the contract's named
  exclusion and is not in this row's scope.
- **Gate quote for the round lesson's `## Gate` record** (contract v1 rule 1 wants a
  ≤25-word quote with its location, grounding `teaches`): the line-861 fragment
  **"In most cases, both validators are generated"** (7 words) — an exact
  single-line raw substring of the retained body at plain-text line 861, and the
  sentence that carries the both-validators half of the row's `teaches`. The L1 picks
  one and records the location; this seat does not write the lesson.

## Census receipts

A lane-shaped scratch mirror of `corpus/SOURCES.md` plus the used-by paths the census
checks, so that E11 measures the row rather than a missing mirror. The mirror's
`corpus/SOURCES.md` is `cmp`-identical to the lane worktree's before the insert, and
the row is inserted at line 226 (after S479). Receipts are in
`census-with-s480.txt` and `census-control-mirror.txt`.

- Control (mirror, no S480): `scripts/sources-census.sh validate --today
  2026-11-05 <mirror>` → **rc 0**, `mirror ok`, zero E-findings.
- With S480 (same command, row inserted): → **rc 0**, `mirror ok`, zero E-findings.
- The only difference between the two outputs is one added line: a `W04` duplicate-URL
  warning for `www.rfc-editor.org/rfc/rfc9111.txt` across scopes — the pre-existing
  warning class that S456, S467, S469, S470 and S476 already carry for the same URL at
  different scopes. It is a warning, not an E-finding; the exit stays 0.
- `scripts/sources-census.sh census --today 2026-11-05 <mirror>` with S480 → rows
  **217** (216 at the lane base), tier.A 192 (191), status.queued 9 (8),
  status.mined 186, status.rejected 22, FLEET.missing 0. The lane's own census at
  base reads rows 216 / tier.A 191 / queued 8 / mined 186, matching.

## Findings for the L1

1. **The `used-by` paths do not exist yet.** `corpus/knowledge/revalidation-exchange.md`
   is this seat's draft (`knowledge-entry.md`, to be landed by the L1) and
   `corpus/lessons/round-96.md` is the round's lesson, which no seat has written.
   While the row stays `queued`, E11 does not look at it. Flipping the row to `mined`
   before both land produces an E11 finding.
2. **The draft's `source:` line names S480 itself.** The knowledge entry's provenance
   trio cites `S480`, so the entry and this row must land together; the entry is
   otherwise a dangling row reference under the C1 counter's E3 audit (an unresolved
   row id in a `source:` line is an E3 finding).
3. **No instrument was amended.** The C2 counter `.ufo/waves/round-96/c96_reval.py`
   still hashes to the freeze's pinned digest
   `ec40aec19d0b4563ad21d79b398c7aaa65a99806984dbca55086c099571eebb9`, and the frozen
   round-95 counter still hashes to `8fd27d62…` — both re-verified by this seat
   (`sha256sum`, no change).

**VERDICT: S480-FINAL admit-ready** (scope-limited: RFC 9111 §4.3.1 and §4.3.3 only),
status `queued` pending the L1's `mined` decision.
