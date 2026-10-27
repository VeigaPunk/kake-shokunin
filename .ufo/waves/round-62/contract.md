# Kake round 62 contract

Base: `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13` (master, remote verified). Freeze before swarm scoring.

## C1 — calibration (lowest owned non-retired axis; score 2)

Claim: learn the round-61 non-author S432 admission disagreement into the corpus quality gate and correct the knowledge entry's S432 citation. Frozen predicate: `met: unresolved_round61_spotcheck_disagreements == 0 AND substantive_quote_correction == 1 AND criterion_present == 1` at the measured committed revision. Before counter: the unique S432 `Disagree` row is present in `corpus/lessons/round-61-verifier-spotcheck.md`, and the knowledge entry's quoted span is a generic lead-in; a do-nothing control must report `unresolved=1`, `quote_correction=0`, `criterion=0`, `met=False`, exit 1. After: append a correction to `corpus/knowledge/response-header-expectations.md` with a substantive quote in S432 §3.6 and explain its support; append a QUALITY.md criterion that located quotes must substantively support their associated claims, citing the verifier finding. Preserve the old knowledge prose, source row, and verifier record; append only. The counter re-derives all states from committed blobs, verifies old-row preservation and criterion/lesson/source pointers, and rejects the base control. Do not claim to resolve every corpus disagreement or raise calibration above its ceiling.

Source grounding: S432 is reopened this round at https://fetch.spec.whatwg.org/ (HTTP 200 from the web reader on 2026-10-27). The retained committed round-61 body `.ufo/waves/round-61/sources/S432.html`, §3.6 lines 6151–6154, contains the substantive sentence: “response header can be used to require checking of a response’s Content-Type header against the destination of a request.” The new correction locates this text and distinguishes it from the generic verifier-rejected lead-in. The entry's policy remains bounded to the Fetch-defined `X-Content-Type-Options` field; it makes no claim about a property's live headers.

No post-freeze predicate changes. No second claim is frozen; any extra axis work is reported separately and cannot be promoted as a claim.

## Frontier / lesson duties

Census before was run: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → `kake\tok\t/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`, exit 0 (16 W04 duplicate-URL warnings, including S433, are recorded; no row edits justified by those cross-scope warnings). Contract-v1 census counted 171 rows. Keep assimilation none unless a qualifying source package is actually opened. Record the round mistake and its criterion in `corpus/lessons/round-62.md`.

## Frozen controls and evidence

`python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision <rev>` is the only C1 counter. Record its committed base-control output before the wave; after-state output is measured only after integration. Scratch/fixtures live under `/fast/scratch/hyaku/kake-r62/<seat>/`, cleaned on exit. No writes to fleet, siblings, upstream property trees, lane Git/jj state by seats. No pacman transactions. Every wave prompt must carry the tooling authorization and pacman guard text from the round prompt.
