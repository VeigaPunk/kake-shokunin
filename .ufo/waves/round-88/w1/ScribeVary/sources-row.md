# SOURCES registry row candidate — S463

Drafted for LANE/.ufo/waves/round-88/w1/ScribeVary/vary-matching.md. L1
integrates; this seat does not edit `corpus/`.

## The row

One row, eleven cells, in the schema of `LANE/corpus/SOURCES.md`
(`id | source | kind | tier | scope | anchor | teaches | status | opened |
recheck | used-by`):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S463 | RFC 9111 — HTTP Caching, §4.1 Calculating Cache Keys with the Vary Header Field — https://httpwg.org/specs/rfc9111.html#caching.negotiated.responses | spec | A | The Vary match rule for two requests: the transformations that make nominated header fields match, the absent-field rule and the always-fails wildcard; not cache-key construction, storage, revalidation, freshness, serving or browser behaviour | RFC 9111 June 2022 section 4.1 paragraphs 1 to 5, retained HTML line 269; opened 2026-11-04, GET-only, HTTP 200, 178573 bytes, sha256 999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64; retained .ufo/waves/round-88/w1/ScribeVary/rfc9111.html | Two requests match when the first can be transformed into the second by whitespace removal, field-line combination or known-semantic normalization; a field absent from both requests matches; a member `*` always fails to match | mined | 2026-11-04 | 180d | corpus/knowledge/vary-matching.md |

## Column count

The row above has **11 columns** — the eleven the lane schema declares:
`id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `status`,
`opened`, `recheck`, `used-by`. Counted by splitting the row on the pipe
characters that delimit it: 12 pipe characters bound 11 cells.

Two rows are drafted in this file and both are reported:

| Row | Where | Columns | Pipes |
|---|---|---|---|
| S463 | the registry row above | 11 | 12 |
| header row | the schema header immediately above it | 11 | 12 |

No cell in the registry row contains a literal pipe character. The `teaches`
cell spells the wildcard member as `*`, and the `scope` cell contains no
pipe; the only pipes in the row are the twelve that delimit the eleven
cells.

## Id and collision check

**The next free id in `LANE/corpus/SOURCES.md` is S463**, so the row takes
S463 as specified.

- `LANE/corpus/SOURCES.md` currently ends at **S462** (the RFC 9111
  §4.2.3 age-arithmetic row). The registry holds the contiguous range
  S001–S462.
- **No S463 row exists in the lane registry.** `grep -n 'S463'
  corpus/SOURCES.md` returns nothing.
- **No duplicate id.** `S463` appears nowhere else in
  `LANE/corpus/SOURCES.md`; the census validator's `E03` (duplicate id)
  cannot fire on this row.
- **The `merge/kake` package does not claim S463.** Its staged
  `SOURCES.append.md` holds 129 rows in the range S287–S415; `S463` is
  absent from it. The eight ids the merge package does collide with the
  lane registry are **S312, S329, S367, S372, S373, S374, S390, S409** —
  re-derived here by intersecting the two id sets, and consistent with the
  contract's statement that the round reports `Assimilation: none`. None of
  the eight is S463.
- Other lanes in the fleet each have their own S463 (`mado-shokunin`,
  `revenger-shokunin`), but those are separate registries; ids are
  lane-local.

## Schema conformance of the drafted row

Checked against `scripts/sources-census.sh` (SOURCES-CONTRACT-v1), whose
validator emits `E01`–`E12` for errors and `W01`–`W04` for warnings:

- `E01` malformed row: the row has 11 cells, so its awk field count is 13,
  which is what the contract requires (11 columns => NF=13). Not fired.
- `E02` id shape: `S463` matches `S[0-9]{3,}`. Not fired.
- `E03` duplicate id: S463 is unused in this registry. Not fired.
- `E04` duplicate URL+scope: the URL `httpwg.org/specs/rfc9111.html` is
  already used by S461 and S462, so the census's `W04` (same URL across
  scopes) will fire for this row, exactly as it already does for S461 and
  S462. `E04` fires only when the same URL appears with the *same* scope
  and the row is not `rejected` and does not say `supersedes S<digits>`.
  This row's scope text is distinct from S461's and S462's scopes (S461:
  *Response Cache-Control first-match lifetime and duplicate-value
  first-occurrence option…*; S462: *Conservative current-age arithmetic on
  supplied timestamps only…*), so `E04` does not fire. The census URL
  normalizer strips the fragment, so the `#caching.negotiated.responses`
  anchor does not create a distinct URL key.
- `E05` kind: `spec` is in the enum. `E06` tier: `A` is in the enum.
  `E07` status: `mined` is in the enum. `E08` opened: `2026-11-04` is a
  valid ISO date, not in the future relative to the round date. `E09`
  recheck: `180d` matches the `^[0-9]+d$` cadence form. `E10`: tier A is
  not `community`. None fired.
- `E11` used-by path missing on disk: `corpus/knowledge/vary-matching.md`
  does not exist yet in the lane, because this seat's candidate lives at
  `.ufo/waves/round-88/w1/ScribeVary/vary-matching.md` and L1 integrates it.
  **`E11` will fire against the lane registry until L1 lands the entry at
  `corpus/knowledge/vary-matching.md`.** The `used-by` cell is written for
  the landed path, which is what the other mined rows name; the row is
  intended to land together with the entry.
- `W01` tier-C mined row: not applicable, the tier is A. `W02` rejected
  row: not applicable, the status is `mined`. `W03` mined but unused: not
  applicable, `used-by` is a path, not `—`.

## Scope and supersession

The row's scope is limited to the §4.1 match rule. It does not restate
S461's Cache-Control lifetime scope or S462's age-arithmetic scope, so it
neither enlarges nor supersedes either. The `teaches` cell says `supersedes`
nothing, and nothing in the row needs it to.

## Evidence for the row's anchor cell

- GET `https://httpwg.org/specs/rfc9111.html`, 2026-11-04, HTTP 200,
  178573 bytes, sha256
  `999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64`.
  Response headers retained at
  `.ufo/waves/round-88/w1/ScribeVary/rfc9111.headers`; body retained at
  `.ufo/waves/round-88/w1/ScribeVary/rfc9111.html`, byte-identical to the
  round-86 and round-87 retained copies of the same URL.
- Section 4.1 is at retained HTML line 269; the paragraphs this row cites
  are `rfc.section.4.1.p.1` (the MUST NOT condition), `.p.2` and `.p.3`
  (the definition and the three permitted transformations), `.p.4` (the
  absent-field rule) and `.p.5` (the wildcard rule).
- The anchor `#caching.negotiated.responses` is the section element's own
  id in the retained body; the paragraph ids `rfc.section.4.1.p.N` are
  present for N = 1..8.
