# S480 — drafted SOURCES row (contract v1 schema, 11 cells)

Drafted by ScoutRFC (kake round 96, w1). **Not appended**: the L1 integrates it through
the round gate. This file is a draft and a receipt; it changes nothing in the lane.

Insert position: after the S479 row (`corpus/SOURCES.md` line 225 at base
`bde9869144f69c5a459c0d2c93f5135922fe3a8d`, the last row of `## Registry`), so the new
row lands at line 226.

## The row

```
| S480 | RFC 9111: HTTP Caching, section 4.3.1 Sending a Validation Request and section 4.3.3 Handling a Validation Response - https://www.rfc-editor.org/rfc/rfc9111.txt | spec | A | How a cache constructs a conditional validation request for a stored response and how it handles the response it receives: that it must send the stored entity tags, should send the stored Last-Modified value, that both validators are usually generated together, that a 304 updates and reuses the stored response, that a full response replaces it, and that a 5xx leaves the cache free to forward or reuse a stored response; not the lane's supplied-values convention, not any live cache's behaviour, not storage, freshness lifetime, cache keys, serving or the merged header field set of a 304; distinct section and scope from S476's 4.3.2 origin-side reading, S470's heuristic-freshness reading and S456's storage-and-freshness reading | Section 4.3.1 heading plain-text line 812, MUST entity-tag bullet lines 848-850, SHOULD Last-Modified bullet lines 852-855, both-validators sentence lines 861-864; Section 4.3.3 heading plain-text line 930, 304 bullet lines 935-936, full-response bullet lines 938-941, 5xx bullet lines 944-948; June 2022; fetched 2026-11-05T18:17:11Z HTTP 200, 84477 bytes, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e; retained body .ufo/waves/round-93/L1/src/rfc9111.txt (cmp identical to the fetched body) | A cache builds a validation request from the stored response's own validators and then reads the response status to decide reuse: the entity tags MUST be sent, the Last-Modified value SHOULD be sent, both validators are usually generated together ("In most cases, both validators are generated"), a 304 updates and reuses the stored response, a full response replaces it, and a 5xx lets the cache forward the error or reuse a stored response | queued | 2026-11-05 | 180d | corpus/knowledge/revalidation-exchange.md, .ufo/waves/round-96/w1/ScoutRFC/fetch.txt |
```

## Cell check

- **Cells: 11.** `python3` — `len(row.split('|')[1:-1]) == 11` → True; `'\\|' in row` →
  False. Every pipe in the row line is a column delimiter; no cell holds a literal or
  escaped pipe. The `i.e.,` inside the quoted RFC fragment of the freeze's clause C5
  carries a comma, not a pipe — no cell needed a comma to be split on.
- **kind** `spec` (census enum: spec, docs, paper, code, tool, dataset, talk, book,
  community, own-work). **tier** `A`, scoped to RFC 9111 §4.3.1/§4.3.3 only — the RFC
  Editor's own publication of the cache-validation clauses is primary for that scope.
- **The `teaches` cell carries a verbatim quote** — "In most cases, both validators are
  generated" (7 words, at or under the 25-unit bound in `corpus/QUALITY.md`).
  `python3` — `q in open("rfc9111.txt").read()` → True; `q in body_lines[860]` → True
  (the raw single line, i.e. the fragment sits at plain-text line **861** of the fetched
  body, which is byte-identical to the retained round-93 body); `q in row` → True.
  The fragment grounds the "both validators are usually generated together" clause of
  `teaches`; it is a raw substring of the retained body, not a reconstruction.
- **status** `queued`, **opened** `2026-11-05`, **recheck** `180d` (the retained body is
  byte-identical to the round-93 fetch and to the freeze's expected digest; RFC 9111 is a
  published specification with a fixed revision, so the cadence is a re-read cadence,
  not a "the content may have moved" cadence).
- **used-by** `corpus/knowledge/revalidation-exchange.md, .ufo/waves/round-96/w1/ScoutRFC/fetch.txt`
  — the C2 knowledge entry the freeze's *Sourced-claim requirement* names, and this
  seat's own fetch receipt (which exists on disk now). **Caveat for the L1:** the census's
  E11 check runs only on `mined` rows, so the not-yet-existing
  `corpus/knowledge/revalidation-exchange.md` does not fire today; if the row is flipped to
  `mined` before the C2 entry lands, E11 fires. Flip the status only after the knowledge
  entry is committed.

## Source and quote grounding

- One GET, `https://www.rfc-editor.org/rfc/rfc9111.txt`, HTTP **200**, **84477 bytes**,
  sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, accessed
  `2026-11-05T18:17:11Z`. The digest equals the freeze's expected digest
  `aeb52adb…` **and** the sha256 of the retained round-93 body
  `.ufo/waves/round-93/L1/src/rfc9111.txt`; `cmp` of the fetched bytes against the
  retained body → rc 0 (byte-identical). Full receipt: `fetch.txt` in this directory.
- The six clause quotes the contract v1 names, located on the fetched bytes with
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
  §4.3.3 only; §4.3.4 (the merged field set of a 304) is the contract's named exclusion
  and is not in this row's scope.
- **Gate quote for the round lesson's `## Gate` record** (contract v1 rule 1 wants a
  ≤25-word quote with its location, grounding `teaches`): a candidate is the line-861
  fragment **"In most cases, both validators are generated"** (7 words) — an exact
  single-line raw substring of the retained body at plain-text line 861, and the
  sentence that carries the both-validators half of the row's `teaches`. A longer
  alternative is the whitespace-collapsed 17-word span "A 304 (Not Modified) response
  status code indicates that the stored response can be updated and reused" (lines
  935-936 collapsed; it is not a single-line raw substring). The L1 picks one and
  records the location; this seat does not write the lesson.

## Census receipts

Mirror: a lane-shaped scratch copy of `corpus/SOURCES.md` plus the used-by paths the
census checks (`corpus/knowledge/`, `corpus/lessons/`, `SKILL.md`, `SCORECARD.md`,
`scripts/source_recheck.py`, `.ufo/waves/round-41/`, `.ufo/waves/round-73/`,
`.ufo/waves/round-95/freeze.md`, `.ufo/waves/round-96/w1/ScoutRFC/fetch.txt`) so that
E11 measures the row, not a missing mirror. The mirror's `corpus/SOURCES.md` is
`cmp`-identical to the lane worktree's before the insert.

- Control (mirror, no S480): `sources-census.sh validate --today 2026-11-05 <mirror>` →
  **rc 0**, `mirror ok`, zero E-findings (`census-validate-control-mirror.txt`).
- With S480 (same command, row inserted at line 226): → **rc 0**, `mirror ok`, zero
  E-findings (`census-validate-with-s480.txt`).
- The only difference between the two outputs is one added line:
  `W04 S480 duplicate url www.rfc-editor.org/rfc/rfc9111.txt across scopes` — the
  pre-existing duplicate-URL warning class that S456, S470 and S476 already carry for
  the same URL at different scopes. It is a warning, not an E-finding; exit stays 0.
- `sources-census.sh census --today 2026-11-05 <mirror>` with S480 → rows **217**
  (216 at the lane base), tier.A 192 (191), status.queued 9 (8), status.mined 186,
  status.rejected 22, FLEET.missing 0 (`census-with-s480.txt`). The lane's own census at
  base reads rows 216 / tier.A 191 / queued 8 / mined 186, matching.

**VERDICT: S480-DRAFT admit-ready** (scope-limited: RFC 9111 §4.3.1 and §4.3.3 only).
It is `queued`, not `mined`: the C2 knowledge entry that cites it does not exist yet.
