source: S443 — in-toto Attestation Framework, Statement v1 (https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md), opened 2026-11-03, HTTP 200, 2,492 bytes, sha256 cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea; row in `corpus/SOURCES.md`, bytes retained at `.ufo/waves/round-75/w1/ScoutSources/intoto-statement.md`
verified-at: 2026-11-03
recheck: 90d
ground: calibration and operability — whether a landed instrument's recorded capability is bound to the bytes that make the claim
scope: one receipt file and the lane's frozen instrument population; this entry says nothing about any deployed artifact, any other host, or the truth of a self-test's assertions

# Binding a claim to the bytes that make it

## What a digest-bound receipt is

A receipt is one committed record that names, for each file in a population, the identity of the
exact bytes that carry the capability. The lane's shape is `corpus/knowledge/instrument-receipts.json`,
schema `instrument-receipts/v1`:

```
{schema, revision, date, host, files[]}
files[] entry: {path, sha256, bytes, selftest_mode}
```

`sha256` and `bytes` are taken from the file's **committed blob at `revision`**, never from the
working tree; `selftest_mode` is true when that blob registers a `--selftest` argument (parsed from
the source, so a docstring or an argv list that merely mentions the flag does not count).
`--check` re-derives all three from the same revision and compares.

The receipt's job is narrow: it runs nothing. It answers one question per file — *is the thing that
claims a capability the same byte sequence the ruler was cut against?* — and leaves the capability's
meaning to another predicate. It is not a membership check either: it does not ask whether a digest
appears *somewhere* in the tree, only whether **this path's** committed blob is **this digest**.

## Why a tally without the artifact digest is not evidence

A tally names a run; a digest names bytes. Round 74 landed three instruments and reported
`selftest 8/8`, `selftest 8/8` and `tests=10 passed=true`; a non-author re-ran all three on the
landed bytes and they passed, yet **no committed receipt named those bytes**, and the delivered
files hashed differently from the landed ones — the numbers were true and unbound
(`corpus/lessons/round-74-verifier-spotcheck.md` R5). A later reader had no way to attach the tally
to a file, and a later edit to the file could not invalidate it.

The same rule is in the vocabulary this lane borrows. in-toto's Statement v1 defines `subject` as
an array of ResourceDescriptor objects — the artifacts the attestation applies to — and requires a
digest on each element: "Each element MUST have `digest` set." (S443, 6 words, raw line 37; the
full 22-word paragraph spans lines 36–37 and matches only after line-leading blockquote-marker
removal followed by whitespace collapse). That is why a name — or a tally written beside a name —
cannot stand in for one.

## The population rule

The lane's *live* instruments, and for the same reason the C1 predicate measures them. Each live
gate-registry table row in `SKILL.md` resolves to one instrument file:

1. the Name cell, when it is itself a repo-relative `.py`/`.mjs` path;
2. else the first `.py`/`.mjs` token of the Entry-command cell;
3. else of the Self-test cell;
4. else of the first cell that carries one.

Rows whose Kind cell carries `historical` are outside the population: their claims are pinned to a
past revision by their own cells, and re-deriving them is a separate bounded pass (a decision
recorded in the round-75 contract §C1, not an accident). A row may be superseded by a later appended
row but never deleted; the row *effective* for a file is the last one naming it.

The cell order matters: a naive any-`.py`-token scan finds two extra files, because
`scripts/freshness-sweep.mjs` is mentioned inside another row's prose and `.ufo/waves/round-46/c46_matrix.py`
is a witness citation, not a row's instrument (`.ufo/waves/round-75/controls/base-c2-receipts.txt`).

## Check semantics

`--check` reads the measured revision through git, never through the filesystem:

- byte length from the committed object (`git cat-file -s <rev>:<path>`);
- sha256 over the committed blob's bytes;
- `selftest_mode` from the same blob's source text;
- the population itself re-derived from `<rev>:SKILL.md`, so a new live row grows the population the
  same check measures (the frozen base list is a floor, never an equality — amendment 1).

Consequences worth stating because they are the point:

- a dirty working tree, an uncommitted receipt, or a receipt written against a path rather than a
  revision cannot pass;
- a receipt is true only at its `revision`; the next commit that touches a population file
  invalidates it by design — re-cutting the receipt is the acknowledgement, and the commit that does
  it is visible;
- a missing entry, or a missing receipt file, is a mismatch (`bound` 0, `mismatches` = population);
- an entry for a file outside the population is not counted toward `bound` and is reported
  separately;
- `met = (bound == population) and (mismatches == 0) and missing_frozen == 0`.

## Limits

- **Identity plus declared capability, never meaning.** `sha256` + `bytes` say *these are the
  bytes*; `selftest_mode` says *this blob registers the flag*. A file whose `--selftest` prints a
  constant and exits 0 binds perfectly. Whether the self-test asserts anything is a different
  predicate, measured by a different artifact (a tally receipt, or a counter that kills its
  fixtures).
- **The receipt re-runs nothing.** It converts "trust the prose" into "re-derive the identity at a
  named revision". It does not convert a vacuous check into a meaningful one.
- **A self-consistent forgery is out of reach by convention only.** Anyone who can commit can pair
  an empty instrument with a receipt whose digests re-derive; the digest cannot forbid that. What
  the receipt changes is the cost: from editing one line of prose to writing a commit that rewrites
  both the file and its receipt, in a history a non-author reads. That is a convention — an
  append-only log with an outside reader — not a cryptographic guarantee, and this entry must not be
  cited as the latter.
- **Snapshot, not a standing licence.** The receipt covers the population at its revision. A live row
  added later is uncovered until the receipt is re-cut, and `--check` reports it as a mismatch rather
  than silently widening `bound`.
- **Cross-lane adjacency, recorded once.** Sibling lanes hold working variants of the same
  primitive: tabi's measurement-binding gate (counter bytes + revision per claim), chousa's
  `digest-in-tree` (digest membership in the tree), souji's `TOOL_SHA256` (one run receipt),
  tameshi's receipt-revision gate (receipt → measured tree). This entry's distinct ground is the
  **registry-derived instrument inventory**: the population is the lane's own registry, derived
  twice and cross-checked. Evidence for the adjacency verdicts is the round-75 wave report
  `.ufo/waves/round-75/w1/ConnectorOverlap.md` §1.
