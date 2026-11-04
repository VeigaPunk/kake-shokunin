# DRAFT — corpus/README.md round-89 rows (ScribeLedger, wave 1)

Landing note for L1: the frontier-map row landed in commit `28532540` (inside the `Frontier ground map`
table, after the round-77 sitemap row) and is correct; keep it, with its Rows cell `S464 S465` and its
"instrument not admitted" wording. The two blocks below are the round-89 additions in the house form of
rounds 85–88: a `## Coverage — round 89` table, and a `## Round-89 frontier step` paragraph at the end of
the file.

## Coverage — round 89

| Area | Entry | Bounded held ground |
|---|---|---|
| Canonical Vary-nominated stored-response key (construction only) | `knowledge/cache-key-construction.md` (S464, S465); `scripts/cache_key.py` | Declared key form for a presented request under a `Vary` value: sorted lowercased members, byte-exact trimmed values, escaped separators, absent distinct from present-empty, `*` and malformed input refused; held but not admitted, because the instrument accepts non-conforming candidates |

## Round-89 frontier step — cache-key construction

`corpus/knowledge/cache-key-construction.md` (S464, RFC 9111 §4.1; S465, RFC 9110 §5.6.2 and §5.6.1.2)
moves the *construction* half of Vary-selected storage from the frontier into held ground: given a URI,
a request header map and a `Vary` value, the entry fixes the key a request maps to, with
`scripts/cache_key.py` as its offline reader. The construction form, the escaping and the refusal list
are adapter conventions the RFC does not require, and the entry says so. The instrument does not yet
establish conformance to the declared form (the round-89 lesson §Wave review), so the ground is held,
not admitted. The entry claims nothing about storage, storability, revalidation, freshness, serving or
browser behaviour.

Remaining frontier here: storage and storability of a keyed response; revalidation and freshness under
a key; serving from a key; browser `Vary` and `Pragma` behaviour; the contract's undecided points (the
combination of duplicate `Vary` header lines, the fourth separator U+001D, duplicate JSON keys and CTL
bytes in non-nominated values); and an instrument that asserts the key string and the uncovered clauses.
Sibling note: `mori-shokunin` holds an RFC 9111 §4.1 Vary rule and an observability entry that disclaims
key construction (see `.ufo/waves/round-89/w1/ConnectorScope.md`); reported as adjacency, not absorbed.
