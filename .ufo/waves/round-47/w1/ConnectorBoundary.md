# ConnectorBoundary — S136 sibling overlap (round 47 wave 1)

Seat: ConnectorBoundary. Axes named: freshness (judged; C2) and operability (C1, must not be harmed). Read-only. No production edit, no sibling-repo read, no tool install.

## Verdict

S136 does not absorb another province's research method. It claims Git's repository-local abbreviated-object-name rule and the lane citation gate's use of that rule. The charter's research-method owner stays chousa.

Two attribution leaks inside that gate can be misread as a wider claim. They are not a method import. Fence them append-only; do not rewrite the mined row.

## Evidence

Files opened: PROVINCE.md, corpus/README.md, corpus/SOURCES.md, corpus/knowledge/commit-citation-hygiene.md. Reads and greps only. No shell command was run.

### Charter split (method stays next door)

PROVINCE.md:36-37:

> chousa owns research method and source hierarchy; kake keeps only domain findings and its own corpus/SOURCES.md rows.

PROVINCE.md:6 refuses absorbing cross-domain evidence. PROVINCE.md:17 lists the lane's own gates as scripts/freshness-sweep.mjs and scripts/probe-delta.mjs only. Grep of PROVINCE.md for S136, citation_lint, commit-citation, and research method hits only lines 36-37. The province file never admits the new gate and never hands research method to kake.

corpus/SOURCES.md:3 names the method and keeps it there:

> Claim admission stays in corpus/QUALITY.md; the research method remains chousa's (chousa-shokunin/SKILL.md: question, source hierarchy, citation chain, and claim-versus-source check).

chousa-shokunin/SKILL.md was not opened (sibling repo).

### What S136 itself claims

corpus/SOURCES.md:144 columns:

- scope: Git's own revision-token abbreviation and resolution semantics only; not a claim about any hosting platform
- anchor: Documentation/gitrevisions.txt, sha1 description-list entry, paragraph beginning "The full SHA-1 object name"; fetched 2026-10-24T06:31:20Z, HTTP 200, 74,526 bytes, retained sha256 33a99ba2…2d2da8c at .ufo/waves/round-47/sources/S136.txt
- teaches: An abbreviated object name is a leading substring that is unique within the repository; uniqueness, not length, is what makes a short hash resolve, and is what git rev-parse --verify tests
- status: mined; opened 2026-10-24; recheck 365d
- used-by: corpus/knowledge/commit-citation-hygiene.md, corpus/lessons/round-47.md

corpus/SOURCES.md:152 (Paths):

> Commit-citation resolution — S136: read Git's repository-local uniqueness rule, then run the lane citation gate; do not infer whether an external repository contains that object.

corpus/SOURCES.md:196 (search log) question is only what Git's documentation says makes an abbreviated object name resolvable within a repository, to ground the lane commit-citation gate. Stop rationale: the vendor-primary paragraph answers that narrow question; "no broader platform or hosting claim depends on Git's object-name syntax." Identified 1, screened 1, included 1 (S136, tier A), excluded 0.

corpus/README.md:38:

> repository-scoped object-name resolution, exclusions, ledger reason fidelity and committed receipt identity; S136 grounds Git revision semantics only

corpus/knowledge/commit-citation-hygiene.md grep for chousa, research method, source hierarchy, claim-versus-source, citation chain, S129, S130, S131, S132, kama, tameshi: no matches.

The entry's S136 sentences are the header quote (line 1) and lines 17-20 plus the "within the repository" application at line 27. Line 24 says dead-token verdicts are repository-scoped, never universal. Line 57 refuses the external-repo existence claim ("that an external-repo token names a real commit in its own repo"). That is the citation-gate consequence of the uniqueness rule, matching Paths line 152. It is not a research procedure.

### Contrast: rows that do import another method

Same registry, different shape. corpus/SOURCES.md:137-140 label S129/S131 as "tameshi round 33, adjacency import" of a "verification-fixture method", and S130/S132 as "kama round 29, adjacency import" of a "calibration method" (self-assessment counts re-derived from committed bytes at the writing revision). S136's scope cell does not use "adjacency import" and the knowledge entry does not cite those ids. Those rows were not re-opened in their sibling repos.

### Contradictions (not collapsed)

1. Fence aims at the wrong neighbor. Scope (SOURCES.md:144) and the search-log stop (line 196) disclaim a hosting-platform claim. The adjacent owner in PROVINCE.md:36-37 for a citation procedure is chousa, not a host. The positive text does not take chousa's four named parts. The disclaimer never mentions them. Absence of the right fence is not absorption; it is an unanswered boundary.

2. Teaches cell adds a tool fact the other three witnesses do not attribute to Git. SOURCES.md:144 teaches "and is what git rev-parse --verify tests". The search-log question (line 196) stops at Git's documentation. The knowledge entry (lines 15-16) says the gate runs git rev-parse -q --verify on the token and cites S136 only for "a leading substring that is unique within the repository" (lines 19-20). README line 38 says S136 grounds Git revision semantics only. The --verify clause is a lane-tool consequence glued onto the source's teaches cell. Flag also: the row says git rev-parse --verify; the entry's recheck line (commit-citation-hygiene.md:3) is git rev-parse -q --verify.

3. "The paragraphs above" over-reaches the Git rule. commit-citation-hygiene.md:65: "The paragraphs above state Git's repository-local abbreviation rule". Paragraphs above that note include Excluded classes (lines 38-42), Receipt identity (lines 46-52, QUALITY "Receipt identity for filed counts", round 46, routed R2), and reason fidelity (lines 56-61). Those are lane policy. They do not state Git's abbreviation rule. README line 38 already splits them from S136. Receipt identity's "re-derives from the named receipt's committed bytes" (lines 47-48) verbally neighbors S130/S132 and the r43 claim-count row (corpus/README.md:32) without citing either. The entry attributes that sentence to QUALITY, round 46, not to S136 and not to kama. QUALITY.md was not opened, so that attribution was not checked.

corpus/README.md:112 still owes a non-author S136 admit spot-check and records no rejection. This scan does not close that debt. corpus/lessons/round-47.md was not opened.

## Affected axes

- Freshness (improves): S136's mined wording can be read as certifying git rev-parse and as Git-grounding receipt identity / reason fidelity. An append that names the grounded lines removes that false certification without rewriting the 2026-10-24 row (C2: repairs append-only; r47 non-retroactive).
- Operability (unchanged): no change to scripts/citation_lint.py, SKILL.md registry rows, or committed selftest receipts. C1 is not touched.

## Proposed move

One append, no in-place edit of SOURCES.md:144 or of commit-citation-hygiene.md:65.

After commit-citation-hygiene.md:65, append a short boundary note:

- S136 grounds only the repository-local abbreviation sentences: the header quote and the Resolution semantics section, lines 17-20 and 27. Dead-token verdicts stay repository-scoped, never universal (lines 24 and 57).
- Excluded classes, receipt identity, and citation reason fidelity are lane gate / QUALITY policy. They are not S136, not chousa's research method (PROVINCE.md:36-37, SOURCES.md:3), and not an S129-S132 adjacency import.
- The teaches-cell clause "and is what git rev-parse --verify tests" (SOURCES.md:144) is a lane-gate consequence, not part of the Git claim, until a non-author compares it to the retained paragraph.

Do not retcon the mined teaches cell. A later append-only search-log note may record the split; replacing the cell would make the r47 row retroactive.

## Risks

- Leaving the teaches cell in place while the note contradicts it creates two live wordings until a non-author spot-check (already owed, README.md:112). That is the point of non-retroactivity; do not "fix" it by editing the row.
- If the retained gitrevisions paragraph actually names git rev-parse --verify, the note would under-claim. This scan did not decide that.
- Narrowing "paragraphs above" must not be read as withdrawing the residual-scope admission that the scanner misses full-40-hex dead tokens, case-sensitive Base, and the (token,file) ledger key (line 65). Those limits stay; only the Git-rule antecedent is named.
- Appending the note is a production edit for a later integrator. This seat did not apply it.

## Verification

Not run, by the four-file bound: no open of .ufo/waves/round-47/sources/S136.txt; no byte or word check of the gitrevisions quote; no open of corpus/lessons/round-47.md, corpus/QUALITY.md, or scripts/citation_lint.py; no citation_lint run; no sibling path (chousa-shokunin, tameshi-shokunin, kama-shokunin).

A later check, not this seat: diff should show only the appended note; SKILL.md registry rows and .ufo/waves/round-47/verification selftest receipts unchanged; teaches cell at SOURCES.md:144 still byte-identical.

## Tools

No install. Pacman is paused; nothing was required beyond read and grep.