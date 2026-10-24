source: S136 — https://git-scm.com/docs/gitrevisions, `Documentation/gitrevisions.txt` `<sha1>` entry ("a leading substring that is unique within the repository")
verified-at: 2026-10-24
recheck: `git rev-parse -q --verify <token>` for a lane-repository resolution; re-open gitrevisions when Git's revision syntax changes

# Commit-citation hygiene (round 47)

How the lane cites commits, how those citations are checked, and what the
check can and cannot prove. Gate: `scripts/citation_lint.py` (round-46 C2,
registry row `commit-citation-lint`); adjudication ledger:
`corpus/quality/citation-adjudications.md`.

## Resolution semantics

A commit citation is a hex token in a commit-bearing context (commit, base,
revision, tip, HEAD, landed, hash, ancestor, parent). The gate resolves each
token with `git rev-parse -q --verify <token>` in the lane repository. Git
accepts an abbreviated object name only while it is a leading substring
unique within the repository — uniqueness, not length, is the resolvability
test (S136, gitrevisions: "a leading substring that is unique within the
repository"). Consequences the lane relies on:

- A 7–8 character token that once resolved can go dead later if the prefix
  becomes ambiguous, and a token that is dead here may resolve in another
  repository. Dead-token verdicts are repository-scoped, never universal.
- `e5455253` (the round-45 quoted defect token) is dead in this lane repo
  while its true commit `e54552553eaff4d7…` resolves — same tree, different
  object stores, per S136's "within the repository" scope.
- Tokens naming an external repository (charter, ds4cc-marketplace,
  plazir-15-site, webzites) can never resolve here; the gate excludes lines
  naming the external repo, and the ledger's `external-repo commit` /
  `external-repo pin` / `sandbox-control commit` / `quoted-dead-token`
  classes record why a non-resolving token is not a violation. Those classes
  name what the citing line asserts — which is why a reason cell must name
  the same repository the citing line names (round-47 correction, R4).

## Excluded classes (never violations)

Content digests (sha256/sha/digest on the line), beat/marker pins, external
repositories named on the same line, tokens glued to alphanumerics or UUID
dashes, tokens without a–f letters. A 64-hex sha256 never matches the token
pattern; truncated digest cites (`8hex…8hex`) are excluded by the digest
vocabulary on their line.

## Receipt identity

Any filed count or verdict against a receipt cites the receipt's path +
sha256, and the count re-derives from the named receipt's committed bytes
(QUALITY "Receipt identity for filed counts", round 46). A selftest tally in
prose (LOG/SCORECARD) is not a receipt; the registry row is incomplete until
the selftest output is committed under `.ufo/waves/round-<N>/verification/`
with the tool path, tool sha256, tally and exit recorded (round-47 fix,
routed defect R2).

## What the gate cannot prove

That a resolving token is the intended commit (only that it is *a* commit
here), that an external-repo token names a real commit in its own repo, or
that a citing line's prose is faithful to its target. Class fidelity is
mechanical; reason fidelity is editorial and is kept by the round-47
QUALITY criterion "Citation reason fidelity" plus the lesson mined each time
a closure catches a drift.
