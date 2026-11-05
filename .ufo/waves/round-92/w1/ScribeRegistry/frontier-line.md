# ScribeRegistry — round-92 frontier line draft (for the L1 to apply)

I do not edit `SCORECARD.md`; the L1 owns it. Two forms below: the corpus form
(already in place in `corpus/README.md`, appended at EOF) and the SCORECARD
"Planned — after round 92" form.

## Form A — the `corpus/README.md` frontier line (already in place)

Appended verbatim at `corpus/README.md` EOF under
`## Round-92 frontier step — heuristic freshness`:

> Frontier line: the heuristic freshness decision moves from open ground to held,
> bounded ground for supplied integer seconds only. Storage-key identity stays
> with r88/r89/r90, the age arithmetic with r87, the reuse decision with r91.
> Still open on this axis: the revalidation exchange (§4.3), storage (§4.1 key
> identity), serving stale without a client directive (§4.2.4's permission rather
> than a preference), field-specific header normalisation, and every live-cache or
> browser observation.

## Form B — the SCORECARD "Planned — after round 92" paragraph

House form is round 91's paragraph: `Outside closure owns admission.` + `Routed
from the wave:` + `Frontier:`. Draft:

> Outside closure owns admission. Routed from the wave: every counter and tool
> defect the wave found is routed in `corpus/lessons/round-92.md` §Routed, and
> the frozen round-92 counters are not repaired after scoring. Frontier: the
> heuristic freshness decision is held for supplied integers only; revalidation
> exchanges (§4.3), storage (§4.1 key identity), serving stale without a client
> directive, and browser behaviour stay open.

## Form C — the `PROVINCE.md` tail (the L1 owns `PROVINCE.md`; not written by me)

`PROVINCE.md` is outside my write scope, so this is a proposal only. Round 91
appended no `PROVINCE.md` section for the reuse decision, so the round-92
equivalence is the L1's call:

> ## Round-92 heuristic freshness frontier step
>
> RFC 9111 §4.2.2 heuristic freshness enters the lane's held Frontier ground as
> a decision over supplied integer seconds (`corpus/knowledge/heuristic-freshness.md`,
> S470; `scripts/heuristic_freshness.py`). It assigns or refuses a heuristic
> expiration time and its lifetime; it stores nothing, revalidates nothing and
> serves nothing. Revalidation exchanges (§4.3), storage (§4.1 key identity),
> serving stale without a client directive and browser behaviour remain open.

## What stays open, spelled out for the L1

| Open item | Where it lives now | Why it stays open |
|---|---|---|
| Revalidation exchanges (§4.3) | nowhere in the lane | The round's instrument decides a lifetime; it performs no exchange with an origin and reads no validator round-trip. |
| Storage (§4.1 key identity) | r88/r89/r90 (`cache_key.py`, `cache_key_conformance.py`) | A cache key is a construction; this round assigns a lifetime to a response, and never stores one. |
| Serving stale without a client directive (§4.2.4's permission rather than a preference) | r91 (`stored_reuse.py` decides `serve-stale` / `must-revalidate-fail`) | Whether a stale response may be served is a reuse decision; this round only reports the lifetime a heuristic would have produced. |
| Browser behaviour | tabi's province (adjacent, not absorbed) | No browser, no live cache, no live property was observed. |
| Field-specific header normalisation | r88's `vary_match.py` declined it (the third permitted transformation) | Not in this round's contract. |
