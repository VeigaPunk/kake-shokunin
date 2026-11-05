# ReviewIndexA — row-by-row review notes (round 97, seat ReviewIndexA)

Seat: review the 19 round-97 calibration-repair index rows assigned to this
seat against the entries as they stand at commit
`9e27ce0b2a8d168e032ab79ea11471b36eaceedf`. Deliverable: `verdicts.tsv`
(19 lines, `<entry>\t<agree|disagree>\t<reason>`, no header).

## Method

Reads were from committed bytes at the repair commit (fresh-start rule):
each artifact was materialized with `git -C <LANE> show 9e27ce0b…:<path>`
into this seat's scratch (`/fast/scratch/hyaku/kake-r97/ReviewIndexA/`) and
reviewed from those bytes. Nothing in the lane tree was written except the
files this seat spec names.

Commands and observed results (all rc=0 unless stated):

- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse master`
  → `9e27ce0b2a8d168e032ab79ea11471b36eaceedf` (matches the dispatch's lane
  tip / C1 repair commit).
- Instrument digest check against
  `.ufo/waves/round-97/controls/instrument-sha256.txt`:
  `sha256sum c97_index.py c97_reval.py frozen/neg-lookup-table.py` →
  `8535150e…aa008`, `f3895a32…39266`, `898df9a2…60cc` — all three equal the
  frozen digests. No mismatch, so no finding and no repair license.
- Fresh-start reads (dispatch order): `freeze.md`, `controls/` receipts
  (`base-c1.txt`, `ctl-c1-selftest.txt`, `ctl-c1-forgery-shuffle.txt`,
  `instrument-sha256.txt`), `corpus/lessons/round-96.md`,
  `corpus/lessons/round-96-verifier-spotcheck.md` (§6: R97-D1 is the missing
  `revalidation-exchange.md` row — outside this seat's 19; R96-3/R96-4 are
  counter-shape defects, not row-prose defects).
- Section located at `corpus/README.md:794` (`## Coverage index — round 97
  (calibration repair)`); the table has 38 rows, of which the first 19 (in
  dispatch order, cache-control-effective … ghp-subpath-spotcheck) are this
  seat's; the remaining 19 belong to ReviewIndexB.
- Mechanical id-set cross-check (conjunct a), run as a python set comparison
  over the extracted rows and entry `source:` lines: row id set == source-line
  id set for all 19 (output `ALL_EQUAL`). The frozen counter's docstring
  (c97_index.py lines 19-23) states its own one-directional check (every
  source id appears in the row); this review applied the stricter
  bidirectional equality the seat spec states — no extra or missing id on
  either side.

## Judgment standard applied

Agree iff (a) row ids == entry `source:`-line ids (bidirectional); (b) every
factual statement in Area/Coverage is true of the entry's own text at
`9e27ce0b`; (c) no overclaim of live-property/crawler/cache behaviour the
entry disclaims. Corrected rows reuse older Area/Coverage text by design
(freeze: "a row that quotes or reuses an entry's own scope text is an
accurate index claim and is admitted by design"), so reused cells were
checked against the entry as it stands now, not against the older entry.

## Judgment calls (documented, all resolved agree)

1. **cache-key-conformance-gate (S463).** The entry's `source:` line carries
   S466, S467, S468 and names S463 inside "(supersedes S463 for construction
   ground)". The token is in the source line (the counter's `S###` tokenizer
   counts it; the row must include it to satisfy the counter), and the entry
   body genuinely discusses the S463→S467 supersession, so the row's S463 is
   "cited by the source line" under both the mechanical and semantic reading.
2. **conditional-list-membership.** The Coverage cell's head phrase "What the
   RFCs decide for the evaluator's v2 clauses: … duplicate JSON member names
   …" could be misread as claiming the RFCs mandate duplicate-member refusal.
   The cell ends "… separated from lane conventions", and the entry's own
   scope sentence has exactly this two-part structure (RFC decisions vs "which
   of contract v2's clauses are lane conventions rather than RFC
   requirements" — C3/C4 are lane conventions; RFC 8259 §4 is quoted as
   SHOULD-unique). The cell is a compression of the entry's scope line, not a
   contradiction of it.
3. **ghp-served-set "what an Actions artifact or branch build actually
   serves".** The entry is careful that artifact membership "does not alone
   establish a live site's membership" and names the un-reopened workflows as
   debt. The cell is a mechanism-scope summary of documented content
   (.git/.github exclusions across versions, v4.0.0 dotpath default, Jekyll
   skip rules, tar depth repro — each individually true of the entry) and
   names no live lane property, so it does not overclaim property behaviour
   the entry disclaims. Non-blocking observation: a stricter paraphrase would
   be "what the documented publishing modes include/exclude".
4. **claim-count-derivation (S130 vs S132).** The entry's 2026-10-24
   correction says to read the source line's S130 as S132 going forward, but
   the correction is append-only and the `source:` line still declares S130 —
   which the entry itself records as the fixed routed defect. Conjunct (a) is
   against the source line as it stands: S130 only, row says S130. Agree.

## Non-blocking observations (routed here, no verdict impact)

- The counter's own shape check (b) is one-directional (source ids ⊆ row
  ids); a row with an extra junk id would pass the counter but fail this
  review's conjunct. No such row exists in this seat's 19 today; the stricter
  human conjunct is doing real work and should stay in the predicate.
- Rows for the historical webzites-derived entries (drift-detection,
  fire-journal-codes, fleet-registry, free-read-verbs) summarize content that
  the entries themselves mark historical/stale-in-part (r23 re-verification
  sections). The cells describe what the entries hold, not current live
  state, so no overclaim; this stays a standing caution for future rows.

## Tooling

No tools were installed or upgraded (pacman untouched; nothing added to
PATH directories). Scratch tree `/fast/scratch/hyaku/kake-r97/ReviewIndexA/`
is deleted before yield; no git/jj mutation was run in LANE or the fleet
repo; no fixture clone was needed.

## Verdict

REVIEW-INDEX agree=19/19 disagree=0
