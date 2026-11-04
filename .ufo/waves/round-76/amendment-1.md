# Round 76 — Amendment 1 (terms-only, recorded before any after-state)

Frozen contract: `contract.md` at `b758cb04` (`4d5c1c25…` blob). This amendment changes no predicate, no
finding id, no exit code and no target; it corrects an input count the L1 measured after the freeze and
before any after-state receipt existed.

## A1 — the real-input population is 8 retained served pages, not 12

§C2 says the audit "runs end-to-end on the 12 retained real surfaces". Measured at the base revision
(`ls .ufo/waves/round-23/live/`): 12 named surface directories, of which **8** retain `page.html` +
`manifest.json`; the other four (`charter-kimi`, `lucario-kimi`, `plazir15-kimi`, `plazir27-kimi`) retain
only `audit.json` + `fetch.json` — those are the round-23 "not-served" outcomes, so there are no bytes to
audit.

The C2 real-input target is therefore: **all 8 retained pages are read, each page's `page.html` sha256 is
verified against its retained `fetch.json` sha256, and the audit's output is recorded**. The four
not-served surfaces are reported as `not-served (no retained bytes)`, never counted as clean or as an error.

Everything else in §C2 stands unchanged.
