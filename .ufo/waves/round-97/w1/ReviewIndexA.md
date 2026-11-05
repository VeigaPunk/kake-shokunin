# ReviewIndexA — C1 row-review conjunct, round 97 (hyaku run 15, w1)

Seat: ReviewIndexA. Target: the 19 round-97 calibration-repair index rows
assigned to this seat, in `## Coverage index — round 97 (calibration repair)`
(`corpus/README.md:794` at commit `9e27ce0b2a8d168e032ab79ea11471b36eaceedf`),
each judged against its `corpus/knowledge/<entry>` at the same commit.

## Verdict

**All 19 rows: agree. agree=19/19 disagree=0.**

Deliverables:

- `.ufo/waves/round-97/w1/ReviewIndexA/verdicts.tsv` — 19 lines,
  `<entry>\t<agree|disagree>\t<reason>`, tab-separated, no header.
- `.ufo/waves/round-97/w1/ReviewIndexA/review.md` — per-row notes, judgment
  calls, commands with observed results.

## What was checked, per row (predicate conjuncts a/b/c)

- (a) id-set equality, bidirectional: every id in the row appears in the
  entry's `source:` line and the row omits none of them. Verified
  mechanically (python set comparison over committed bytes) — `ALL_EQUAL`
  across all 19; see review.md for the four special cases (S463 named inside
  the cache-key-conformance-gate source line's supersession parenthetical;
  claim-count-derivation's append-only S130→S132 correction leaves the
  `source:` line at S130; the two own-work rows whose source lines carry no
  S-id and whose cells say "own-work; no SOURCES row").
- (b) factual truth of Area and Coverage cells against the entry's own text
  at `9e27ce0b`, including corrected rows that reuse older cell text (the
  freeze's declared limit admits scope-text reuse as accurate index claims;
  each reused cell was re-checked against the entry as it stands now).
- (c) no overclaim of live-property/crawler/cache behaviour the entry
  disclaims (cache-control-effective, conditional-request-evaluation,
  ghp-served-set, ghp-custom-domain were read with this lens specifically).

## Fresh-start reads and instrument integrity

Read in dispatch order before judging: `freeze.md`; controls `instrument-sha256.txt`,
`base-c1.txt`, `ctl-c1-selftest.txt`, `ctl-c1-forgery-shuffle.txt`;
`corpus/lessons/round-96.md` (## Mistakes, ## Routed to round 97);
`corpus/lessons/round-96-verifier-spotcheck.md` (§6: R97-D1 = the missing
`revalidation-exchange.md` row — that row is in the section but outside this
seat's 19; R96-3/R96-4 are counter-shape defects, not row-prose defects).

Frozen digests verified before use, all rc=0, all three equal
`controls/instrument-sha256.txt`: c97_index.py `8535150e…aa008`,
c97_reval.py `f3895a32…39266`, frozen/neg-lookup-table.py `898df9a2…60cc`.
`git -C LANE rev-parse master` → `9e27ce0b…` (matches the dispatch's repair
tip). No mismatch found, so no digest finding.

All bytes reviewed were materialized from the frozen commit via
`git -C LANE show 9e27ce0b…:<path>`; no worktree reads.

## Findings

No defect in the reviewed rows; 19 × agree. Two routed observations
(status-neutral, recorded in review.md):

1. The frozen counter's shape check (c97_index.py docstring item b) is
   one-directional (every source id appears in the row); a row with an extra
   junk id would pass the counter and only fail this human conjunct. No such
   row exists in this seat's 19. Recommendation for a future counter
   successor: make the id check bidirectional. Routed as an observation; not
   a repair (instruments are frozen).
2. Rows summarizing the historical webzites-derived entries (drift-detection,
   fire-journal-codes, fleet-registry, free-read-verbs) describe content the
   entries themselves mark historical/stale-in-part (r23 re-verification
   sections). The cells describe what the entries hold, not current live
   state — no overclaim — but future row edits should keep that framing.

## Seat hygiene and incident note

- Scratch root `/fast/scratch/hyaku/kake-r97/ReviewIndexA/` was deleted
  **by a sibling seat's overbroad cleanup** (`ConnectorScope-23` ran
  `rm -rf /fast/scratch/hyaku/kake-r97`, the round parent, ~18:14Z; disclosed
  to all seats via agent message; that seat reports it as its own defect).
  Impact on this seat: none — the scratch held only read-only git-show
  extracts whose analysis was already complete; both deliverables had been
  written into the lane tree before the deletion. Scratch verified absent at
  yield (satisfies the delete-before-yield rule); not recreated. Nothing
  frozen was touched (host sysctls, LANE tree, MANIFEST, digests all intact
  from this seat's own reads).
- No git/jj mutation in LANE or the fleet repo; no fixture clone needed
  (single-revision reads went through `git show`, which is read-only).
- No tools installed or upgraded; pacman untouched.
- Writes confined to `.ufo/waves/round-97/w1/ReviewIndexA/verdicts.tsv`,
  `.ufo/waves/round-97/w1/ReviewIndexA/review.md`, and this Report file.

REVIEW-INDEX agree=19/19 disagree=0
