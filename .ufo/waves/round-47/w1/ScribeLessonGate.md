# ScribeLessonGate — round 47 lesson-gate check (S136)

Seat: scribe (freshness). Read-only evidence; no lane writes beyond this report,
no mutating jj/git, no network, no installs. Report path is the only artifact
written. Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

## Behavior

Read `corpus/lessons/round-47.md:61-79` (`## Gate`), `corpus/SOURCES.md:144`
(S136 row), `.ufo/waves/round-47/sources/{S136.txt,receipts.log}`, the S136
knowledge entry, the r47 verifier spot-check at HEAD, and the committed wave
spec. Ran read-only `sha256sum`, `wc`, `grep`, `nl`, `git show`, and a whitespace-
normalized quote match. Did not re-fetch the URL and did not rerun the lane
counters; no evidence below depends on an unrun command.

## Acceptance checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | S136 URL + access date | **pass** | Gate 63-64 gives `git-scm.com/docs/gitrevisions` + `2026-10-24T06:31:20Z`; full `https://` URL in `corpus/SOURCES.md:144`; `receipts.log` line 1 records the same URL and time; `S136.txt` mtime `2026-10-24 03:31:20 -0300` = `06:31:20Z` (host TZ -03). Note: the Gate heading itself omits the scheme; the receipt carries it. |
| 2 | Located quote ≤25 words | **pass** | Gate 68-69 quote; after whitespace collapse it is a verbatim substring of `S136.txt` (`q1 present: True`), source lines 2179-2180. Count `len(q.split()) == 18`. Gate's own "18 words" is exact. Second quote (Gate 73-75) is also verbatim (`q2 present: True`), source 2181-2183, 25 words. |
| 3 | Candidate / admit / reject counts | **pass with wording note** | Gate 78: "Identified 1, screened 1, included 1 (S136), excluded 0"; admit count is carried by `included 1` / `ADMITTED` (69), not a literal `admit=1`. Reject count is `excluded 0` + `Rejections this round: none` (77). Registry diff adds exactly one row, status `mined` (`git diff cd42e3c -- corpus/SOURCES.md` = +S136, 0 deletions). |
| 4 | No-rejection honesty | **round-local pass / universal claim fail** | `Rejections this round: none` (77) is true: only S136 was added; no existing status/recheck/used-by cell changed. But Gate 79's reason "there is no rejected source candidate to sample" is unqualified and false at the same commit: `corpus/SOURCES.md` holds **22 rows with status `rejected`** (`git show 59146c9:corpus/SOURCES.md | grep -c '\| rejected \|'` → 22), e.g. S134 tier C `rejected` at `SOURCES.md:142`. One commit later the closure sampled S134 as the reject leg and agreed (see below). |
| 5 | Explicitly owed non-author admit+reject spot-check | **pass on disclosure; stale at HEAD** | Gate 79 explicitly says "Independent admit+reject spot-check remains owed to closure." That disclosure is present. At HEAD `766f461` (commit "round-47 verifier spot-check (integrator, hyaku): non-author admit/reject") the owed check exists in `corpus/lessons/round-47-verifier-spotcheck.md:58-62`: S136 ADMIT → "agree"; S134 REJECTED → "agree"; plus a row recording the in-round reject leg as not exercisable. So the obligation is disclosed and now discharged; the Gate's "remains owed" is stale relative to HEAD (round-47.md last changed at `59146c9`; `git diff --stat 59146c9 766f461 -- corpus/lessons/round-47.md` is empty; `766f461` adds only the spot-check file). Separately, the prepared 32-seat `w47-spec.json` contains no seat tasked with an admit+reject spot-check: its only S136 seats are `ScoutS136Quote` (quote/receipt/scope) and `ScribeLessonGate` (this check); `"admit"` appears in no item.

## Findings (material)

**F1 — fail: the Gate's S136 digest elision is not a truncation of the actual digest.**
`round-47.md:65` and `SOURCES.md:144` print `` `33a99ba2…2d2da8c` ``. The file's
sha256 is `33a99ba212228d6968e7721a87197558b0e88a450ecfc303eaa34d8321d2da8c`
(`sha256sum .ufo/waves/round-47/sources/S136.txt`); `endswith('2d2da8c')` is
`False` and `'2d2da8c' in digest` is `False`. The true suffix is tail-7
`1d2da8c` (or tail-5 `2da8c`); note the established row convention e.g. S135
`73b3b4a8…ec18d` = true tail-5. No gate covers it: `scripts/citation_lint.py:157`
skips an ellipsis digest when `len(token) != 40`, so this class is unchecked.
The same invalid elision is repeated by the non-author spot-check
(`corpus/lessons/round-47-verifier-spotcheck.md:60`, "same sha256,
`33a99ba2…2d2da8c`") and by the peer w1 report
`.ufo/waves/round-47/w1/ScoutS136Quote.md:67,71` ("`sha256sum` →
`33a99ba2…2d2da8c`"). The full digest is correct and the 74,526-byte count
matches; the defect is the receipt-identity string, on this round's own
citation-hygiene axis.

**F2 — fail: "there is no rejected source candidate to sample" is contradicted
by the registry and by the closure's own sample.**
Gate 79. `corpus/SOURCES.md` has 22 status-`rejected` rows at both `59146c9`
and HEAD; S134 is one. `round-47-verifier-spotcheck.md:62` re-opened S134 as
"nearest-dated rejected row" and scored it "agree". The round-scoped reading
("no reject *this round*") is true and already captured by line 77; the
unqualified sentence at 79 is false as written and is the stated excuse for
the unexercised reject leg.

## Advisory findings (outside the enumerated predicate, same artifact)

**F3 — SOURCES S136 `teaches` cell overreaches the retained text.**
`SOURCES.md:144` ends the teaching with "…and is what git rev-parse --verify
tests". `grep -ci verify .ufo/waves/round-47/sources/S136.txt` → 2, both
`verify-pack` links; there is no `--verify` text in the retained `gitrevisions`
body. The knowledge entry's `recheck:` (`corpus/knowledge/commit-citation-hygiene.md:3`)
uses `git rev-parse -q --verify` as the lane's method, which is fine, but the
row's anchor paragraph does not support the `--verify` clause.

**F4 — "grounds … the R4 corrections" is a conceptual link, not a citation.**
`grep -n S136 corpus/quality/citation-adjudications.md` returns nothing; the
`## Round-47 corrections` block does not cite S136. S136 is cited by
`commit-citation-hygiene.md` (lines 1, 19, 27). The `## Registry changes` bullet
"the C2 … claim rests on S136" is also broader than the evidence: C2's R3/R5/R6
repairs (population count, full hashes, unreceipted verdict) do not read S136.

**F5 — quote line number in the closure spot-check is off by one.**
The spot-check says the quote is "present verbatim at retained-text line 2180";
the sentence starts at 2179 and ends at 2180 (`grep -n 'The full SHA-1 object
name'` → 2179). The Gate itself does not assert a line number, so this does not
affect the Gate check.

## Conflicts for the canonical judge (verbatim)

- Closure spot-check (`766f461`, `round-47-verifier-spotcheck.md:60`): "same
  sha256, `33a99ba2…2d2da8c`" — conflicts with
  `sha256sum` = `33a99ba212228d6968e7721a87197558b0e88a450ecfc303eaa34d8321d2da8c`.
- Peer `ScoutS136Quote.md:71`: "`sha256sum` → `33a99ba2…2d2da8c` — **byte-identical
  to the committed retained text today**" — same invalid suffix; its byte
  identity claim is compatible with the full digest but not with the printed
  elision.
- Closure spot-check line 62 samples S134 and agrees, while `round-47.md:79`
  says "there is no rejected source candidate to sample".

## Not run / out of scope

- No live re-fetch: the `HTTP_STATUS=200 BYTES=74526 exit=0` receipt is
  self-recorded; I verified the retained file's size/hash and mtime, not the
  network event. The closure's live re-fetch claim was not reproduced here.
- No rerun of `c47_registry_count.py` / `c47_routed_count.py` (not needed for
  this checklist; C1/C2 seats cover them).
- Did not audit R3-R6 gate content, the wave-spec validator, or sibling repos;
  did not inspect or modify `.jj`, refs, `.ufo/state/`, or `.ufo/watchdog.log`.
- No tools installed or updated; no scratch files created.

## Touched surfaces

Read-only: `corpus/lessons/round-47.md`, `corpus/SOURCES.md`,
`corpus/knowledge/commit-citation-hygiene.md`,
`corpus/quality/citation-adjudications.md`,
`corpus/lessons/round-47-verifier-spotcheck.md`,
`.ufo/waves/round-47/sources/*`, `.ufo/waves/round-47/w1/*` (peer reports,
read only), `.ufo/waves/round-47/w47-spec.json`, `scripts/citation_lint.py:157`.
Written: this report only.

## Artifacts cited

- `corpus/lessons/round-47.md:61-79`
- `corpus/SOURCES.md:144` (S136), `:142` (S134)
- `.ufo/waves/round-47/sources/S136.txt:2179-2183`, `receipts.log`
- `corpus/lessons/round-47-verifier-spotcheck.md:58-62` (committed `766f461`)
- `corpus/knowledge/commit-citation-hygiene.md:1-29`
- `.ufo/waves/round-47/w47-spec.json` (32 items; roles executor 4, scribe 4,
  scout 2, reviewer 10, critic 4, mutation-tester 6, connector 1, sentinel 1)
