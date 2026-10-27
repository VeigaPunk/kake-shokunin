# Round 63 — lessons (kake)

Round opened 2026-10-27; base `13d4519818db28cd0aa912e49020659140d7b9fa`
(round-62 tip). Two claims, frozen in `.ufo/waves/round-63/contract.md`
before any after-state measurement:

- **C1 calibration (lowest owned axis, 2/10).** Repair the falsified
  calibration counter family: `.ufo/waves/round-63/c63_calibration.py`
  re-derives every `resolved` component from committed bytes (retained-blob
  digests, tool-re-derived match class, located proposition, outside verdict).
  The round-61 S432 disagreement is resolved by admitting the §3.6
  field-purpose span as `collapsed-only` under the round-50 quote-class rule,
  grounding `corpus/knowledge/response-header-expectations.md` append-only.
- **C2 operability (HOLD 10).** Land `scripts/quote_class.py` — the committed
  quote-class derivation tool (selftest 4/4, one real corpus case) that the C1
  counter consumes; counted by `.ufo/waves/round-63/c63_quote_tool.py`.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| false-green (marker-only counter predicate) | `.ufo/waves/round-62/controls/counter-false-green-l1.txt`: the frozen c62 counter printed `met=true` on a marker-only fixture (`disagreements=1`, no retained source body); the same attack is in round-62 w1 `ReviewerCounterControls`. The round-61 spot-check had already ruled C1 unprovable, so no false admission landed — but the counter family stayed able to green a marker-only tree. | none — the lane's freeze rule (round-60) pinned the counter's sha and receipts but never required `resolved` to bind semantics; the substantive-support criterion (round 62) judges entries, not counters. The non-author verifier caught it (round-62 routed defect 1). | New frozen counter binds every component to committed bytes (blob digests + tool-re-derived class + located proposition + outside verdict); committed QUALITY round-63 criterion; red-before/green-after and do-nothing/junk controls in `.ufo/waves/round-63/controls/`. |

## Gate

Candidates considered this round: (a) the S432 field-purpose span, classed
from its retained blobs; (b) the two round-62 rejected spans (fragment ending
before its object; generic lead-in), re-examined as grounding; (c)
`considerthese/2026-10-26.md` proposal 2 (a daily git-log receipt-rewrite
watch); (d) the `merge/kake/` assimilation package.

- **Admit (a):** the span “The `X-Content-Type-Options` response header can
  be used to require checking of a response’s `Content-Type` header against
  the destination of a request.” is derived `collapsed-only` from its two
  blobs (retained HTML sha256 `63b0a018…911b`; flat text sha256
  `8b90d096…2a69`; recipe `extract_text.py`). It substantively states the
  proposition the `xcto_nosniff_value` section attributes to S432. The class
  ledger, both digests and the recipe are committed; the lane tool re-derives
  the class (selftest case `s432_real`).
- **Reject (b), kept rejected:** the fragment and the lead-in still ground
  nothing; the round-62 reasoning stands (they end before the object / are a
  section lead-in). Flip: none — superseded by (a).
- **Reject (c), not implemented:** `considerthese/2026-10-26.md:26` proposal 2
  is aggregate bookkeeping; the semantic class it watches (receipt rewrites)
  is already countered by `c58_receipt_rewrites.py`, and a git-log watch adds
  a second ledger without adjudicating anything. Flip: repeated verifier/gate
  comparisons showing the semantic counter misses a receipt-rewrite class the
  log watch would catch.
- **Assimilation: none.** No `merge/kake/` entry was adopted this round; the
  round's calibration work admits nothing from the package. The package stays
  staged and unread-by-adoption for a later round.

**S432 re-open record (rule 1):** https://fetch.spec.whatwg.org/ opened
2026-10-27, one GET, HTTP 200, 1,854,393 bytes; sha256 byte-identical to the
round-61 retained body (`63b0a018…911b`), so the retained body is current.
Located quote (raw lines 6150–6154, ≤25 words): "response header can be used
to require checking of a response’s Content-Type header against the
destination of a request". No registry row added or changed; S432 stays
`mined`.

**Outside verdict:** the round-61 non-author spot-check `Disagree` on the S432
admission (`corpus/lessons/round-61-verifier-spotcheck.md:33`) is the outside
verdict this gate records; it is resolved by this round's correction. This
round's own gate decisions (admits/rejects above) are lane self-assessment,
author-side; the non-author closure of round 63 decides agreement.

## Sources census

Round-start census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → 171 rows, 16 W04 cross-scope duplicate-URL warnings, exit 0 (recorded 2026-10-27 before any registry edit). No `corpus/SOURCES.md` row was added or changed this round. The round-end census output is pasted in the round report.
