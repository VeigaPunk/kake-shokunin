VERDICT: 2 terms overlap (identity pins, mutant kill count; both principle-level only, zero same RFC clause or same instrument), 4 sibling lanes hold ground (kengaku, revenger, kaidoku, mori)

# ConnectorScope — round 94 cross-lane overlap (read-only)

Seat: ConnectorScope. Lane: /home/vgpnk/Projects/shokunin/kake-shokunin. No LANE file edited, no git mutation, no network, no campaign tool run, no scratch created.
- Siblings: all 20 `*-shokunin` lanes other than kake (audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi). All 20 hold `corpus/SOURCES.md`; 18 also carry `SKILL.md`, and every one with a `corpus/knowledge/` directory has at least one note.
## Scope and method

- Siblings: all 20 `*-shokunin` lanes other than kake (audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi). All 20 hold `corpus/SOURCES.md`; 19 also carry `SKILL.md` and a `corpus/knowledge/` directory.
- Searched: `corpus/SOURCES.md`, `corpus/knowledge/*.md`, `SKILL.md`, each sibling, case-insensitive, via the grep tool with `!**/kake-shokunin/**` excluded.
- Not a sibling lane: `/home/vgpnk/Projects/shokunin/kumitate-shokinin/` (typo directory; contains only a nested `kumitate-shokunin/` with no corpus). Not matched by the `*-shokunin` glob; not counted.
- Staged package: `/home/vgpnk/Projects/shokuknow/merge/kake/MERGE-REPORT.md` exists and was read (read-only; first 25 lines). Nothing else under shokuknow was read.
- Kake-side ground was read only to name what each term refers to (kake's own `corpus/SOURCES.md` S471-S476 and `corpus/knowledge/conditional-request-evaluation.md`).

## RFC 9110 registration check

Command: grep (case-insensitive) `rfc ?9110` over sibling `corpus/SOURCES.md`, plus a same-line co-occurrence check for `9.1`/`5.6.1` near `rfc9110`/`HTTP Semantics`/`STD 97` (result: No matches found), plus `§ ?9.1|section-9.1|§ ?5.6.1|section-5.6.1` (only sibling-internal section numbers, no RFC 9110 hits).

| Lane | SOURCES row | RFC 9110 clause registered | Relation to kake S471-S476 (§13.1.1-13.1.4, §13.2.2, §8.8.3.2) |
|---|---|---|---|
| chousa | S061 (line 71) | §15.5.5 404, §15.5.11 410 | none (different clauses) |
| mori | S042 (line 48) | §10.2.3 Retry-After | none |
| mori | S221 (line 227) | §15.4 3xx redirection | none |
| tabi | S107 (line 121) | §15.4, §10.2.3 | none |

- Sibling registrations of RFC 9110 §9.1 (method definition, method token case): **0**.
- Sibling registrations of RFC 9110 §5.6.1 (list syntax, `#rule`): **0**.
- Sibling registrations of any RFC 9110 §13 conditional-request clause: **0**.
- Adjacent RFC 9111 registrations (not the same clauses as kake S476 §4.3.2): kumitate `receipt-age-on-the-compare-path.md:37-41` and `self-describing-shape-receipt.md:34-37` cite §4.2.3 and §4.3.4; mori `ua-serving-normative-r79.md:3,22` cites §4.1 (Vary, S594).

## Per-term table

Hit counts are sibling-only (19 or 20 lanes, SOURCES + knowledge + SKILL). "Same ground" means the same RFC clause or the same instrument.

| # | Term | Sibling hits (exact) | Sibling lanes, same ground | Sibling mentions, near ground | Decision |
|---|---|---|---|---|---|
| 1 | conditional request evaluation | 0 | 0 | kumitate (RFC 9111 §4.2.3/§4.3.4 age after validation); mori (RFC 9111 §4.1 Vary); tabi (GitHub REST docs "Use conditional requests", S121, `SOURCES.md:136`) | report as adjacent; no absorb |
| 2 | If-None-Match | 0 | 0 | none | none; kake-only (S473) |
| 3 | If-Match | 0 | 0 | none | none; kake-only (S472) |
| 4 | method token case-sensitive | 0 | 0 | none (kaidoku SKILL hit is a "method … case" false positive, unrelated) | none; kake-only |
| 5 | list member syntax | 0 | 0 | lore `2026-10-12-lore-decision-table.md:213` ("malformed list member", lore's own dependency grammar; not RFC 9110 §5.6.1) | report as adjacent (no ground); no absorb |
| 6 | annotated absence | 0 | 0 | chousa S061 (`SOURCES.md:71`) and `corpus/knowledge/exempt-hop-audit-r32.md:3,16-19` (RFC 9110 §15.5.5/§15.5.11: what 404/410 say about origin availability; same RFC, different clauses) | report as adjacent; cite candidate only if kake cites §15.5 (it does not) |
| 7 | identity pins | 3 | 0 same clause; 1 principle-level | kengaku `fixture-honest-geometry.md:40-42` (pin mismatch reported, never silently re-pinned: principle-level, cite-able precedent); mado `walker-deep-r9.md:53` (heading only); mori `retention-reconciliation-r22.md:60` (phrase only) | cite kengaku as precedent for the pin-mismatch rule; no absorb |
| 8 | names a tree, not a blob | 0 | 0 | none (kake-only: `corpus/knowledge/receipt-provenance-r85.md:69`) | none; kake-only |
| 9 | mutant kill count | 1 exact (revenger `SKILL.md:64-67`: "A mutant kill counts only if the mutant run exits non-zero and its last output line ends with the registered phrase") | 3 lanes hold the named-case kill-attribution rule: revenger (SKILL.md:64-67); kaidoku (`2026-11-03-r69-packed-route-contract.md:43-44`, `2026-11-04-r74-probe-mutation-closure.md:52-54`, `2026-11-04-r79-mutation-and-pointers.md:41-44`, `2026-11-04-r85-mutant-kill-binding.md:11`); mori (`calibration-arming-r91.md:21-24`) | ~9 lanes use kill-count wording without an attribution rule (mado, kama, tameshi, kotoba, kumitate, tabi, plus those above) | cite (named-case attribution rule from revenger/kaidoku/mori); no absorb |

Totals: exact-term sibling hits = 4 across 9 terms (identity pins 3, mutant kill count 1); terms with at least one same-clause or same-instrument sibling = 0; terms with a principle-level sibling = 2; distinct sibling lanes holding principle-level ground = 4 (kengaku, revenger, kaidoku, mori).

## Findings and honest limits

1. Kake's conditional-request ground (S471-S476: RFC 9110 §13.1.1-13.1.4, §13.2.2, §8.8.3.2; RFC 9111 §4.3.2) and the round's RFC section terms (§9.1, §5.6.1) are unique in the fleet. No sibling holds the same clause. Overlap is not a reason to absorb or re-cite anything from siblings.
2. The `mutant kill count` overlap is the only one that matters for the round's C2 instrument. revenger and kaidoku state a named-case attribution rule that the kill counter should satisfy. I did not check whether `c94_conditional.py` implements that rule: `grep -n -i 'kill' .ufo/waves/round-94/c94_conditional.py` returns zero lines, so its kill verdict is not visible by the word "kill". This is a finding for the L1, not an edit.
3. Staged-package defect (read-only observation): `/home/vgpnk/Projects/shokuknow/merge/kake/MERGE-REPORT.md` says the lane registry "currently holds 145 rows; first staged id is S287". Kake's `corpus/SOURCES.md` now runs to S476, so the staged ids S287 onward collide with rows already in the lane. Do not merge that package unmodified. I did not run any campaign tool.
4. Kumitate's `S237` row labels the RFC 9111 quote "Section 5.1 (Age)" while the quote sits in §4.2.3 (kumitate's own note records this). Sibling registry label error; no effect on kake.
5. Search-tool limits: grep output in this seat was capped (around 20 matches per file, with truncated lines), so per-file counts above are lower bounds for the broad patterns (kill-count wording, RFC 9110 near-variants). The exact-term zeros (If-None-Match, If-Match, method token case-sensitive, list member syntax, annotated absence, names a tree, conditional request evaluation) came from unbounded output and are reliable at the exact-phrase level only.
6. The sibling glob `*-shokunin` skipped `kumitate-shokinin`. It is a typo directory with no corpus, so no overlap is lost.

## Decision summary

- absorb: 0 terms.
- cite: 2 (identity pins → kengaku precedent; mutant kill count → revenger SKILL.md:64-67 and kaidoku named-case rules, as candidates for C2's kill attribution).
- report as adjacent: 2 (conditional request evaluation; annotated absence), plus list member syntax (term match with no shared ground).
- none (kake-only): 4 (If-None-Match, If-Match, method token case-sensitive, names a tree, not a blob).

## Checks the main agent should run

None. Read-only overlap scan; no build, test or counter run was requested or performed.
