source: corpus/knowledge/gate-agreement-ledger.json — lane path /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/gate-agreement-ledger.json; ledger sha256 ef58f9092c32179de6e680ab782cfb29900d9b5b34cfbfcb76b316a144c3d506; per-row provenance under .ufo/waves/round-87/snapshots/ (round-84/85/86 verifier spot-checks).
verified-at: 2026-11-04 — ledger bytes re-hashed from the frozen round-88 copy .ufo/waves/round-88/frozen/base-gate-agreement-ledger.json (sha256 ef58f9092c32179de6e680ab782cfb29900d9b5b34cfbfcb76b316a144c3d506) and from base f4479c14813037ad993a49a3dee4028763470f7a; the three per-row snapshot digests re-hashed from the snapshot files themselves; round-88 counter .ufo/waves/round-88/c88_defect_queue.py (item D1-ledger-companion).
recheck: 180d or whenever a verifier spot-check adds, re-decides or withdraws a row; re-hash the ledger and re-read the eight rows; any ledger byte change invalidates the digest quoted above and must be accompanied by a revision of this companion.

# Gate-agreement ledger — provenance companion

This entry is the companion to `corpus/knowledge/gate-agreement-ledger.json`.
It exists because a JSON file cannot open with the provenance trio — a filled
`source:` line, a filled `verified-at:` line and a filled `recheck:` line —
that every `corpus/knowledge/` entry is required to carry, and because a
ledger whose rows point at other ledger rows still needs one place that says
where the ledger came from, when it was last checked, and when it must be
checked again. The trio above is that place. The quoted sha256 binds this
companion to the exact ledger bytes: if the ledger changes, the digest above
stops matching and this entry is stale until it is revised with it.

## What the ledger holds

Eight rows, one per closure decision taken in rounds 84, 85 and 86, each with
the verdict the outside reviewer returned on that decision.

| Round | Item | Decision | Outside verdict |
|---|---|---|---|
| 84 | S457 response max-age semantics | admit | agree |
| 84 | §4.1 normalization as response-directive reorder proof | reject | agree |
| 84 | §5.2.2.2 as max-age anchor | reject | agree |
| 85 | S458 field-specific algorithm | admit | agree |
| 85 | Blanket response-policy reorder equivalence | reject | agree |
| 86 | S459 CrUX Vis docs | admit | agree |
| 86 | S461 RFC 9111 slice | admit | agree |
| 86 | RFC 7234 minimum-duplicate attribution | reject | agree |

Row order above is the ledger's own file order. Each row also carries the
`source` snapshot path and that snapshot's sha256; the three distinct snapshot
digests the eight rows cite are listed under "Ledger bytes are unchanged from
base" below.

## What kind of file this is

`corpus/knowledge/` is defined by `corpus/README.md` as the directory of
domain facts with citations. This file is not one of those facts. It is
evidence metadata: the ledger it accompanies records decisions that the
closure sessions of rounds 84–86 owned — whether a given candidate claim was
admitted to the corpus — together with the outside verdict recorded for each
decision. It is a record of who decided what and that the outside review
agreed. It asserts no domain claim about HTTP caching, no publisher property,
and no live surface, and it has no SOURCES row because it is not a sourced
claim: there is no external document here to open, quote and date. The
decisions belong to the closure sessions; this file only carries the metadata
that a JSON blob cannot carry for itself.

## Ledger bytes are unchanged from base

The ledger bytes at the round-88 base commit and at the frozen round-88 copy
are byte-identical to the bytes this companion describes:

    sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-88/frozen/base-gate-agreement-ledger.json
    ef58f9092c32179de6e680ab782cfb29900d9b5b34cfbfcb76b316a144c3d506  .../base-gate-agreement-ledger.json

    git show f4479c14813037ad993a49a3dee4028763470f7a:corpus/knowledge/gate-agreement-ledger.json | sha256sum
    ef58f9092c32179de6e680ab782cfb29900d9b5b34cfbfcb76b316a144c3d506  -

The three snapshot digests the rows cite re-hash to the values the ledger
records for them:

    sha256sum .ufo/waves/round-87/snapshots/round-84-verifier-spotcheck.md
    80f48887b1e5f2e9d7d54adcce19d8b935f77fc0b236620abac3335b730dfda9
    sha256sum .ufo/waves/round-87/snapshots/round-85-verifier-spotcheck.md
    948c316831d0c71927e6a29501f05037b3faa940a251984ed28ca8f0eee2ce71
    sha256sum .ufo/waves/round-87/snapshots/round-86-verifier-spotcheck.md
    47499686bc976564c43174fdeeae2219e0db2351c571678ba35caff0a34de42b

## Bound of this entry

This entry proves that the record exists, that its bytes are the ones quoted
above, and that each row points at a spot-check snapshot whose digest is the
one recorded. It does not prove that an assessment was performed: the ledger
says a decision was taken and the outside reviewer agreed, not that any
member of the closure re-derived the decision independently, and not that the
decision was correct. No decision accuracy is claimed and none improved by
this file. A reader who wants the substance of a row must open the cited
spot-check snapshot; the row's own `source` path is the authority for the
reasoning, and this companion only points at it.
