## Verdict

P3 — Recommend one documentation/receipt-scope clarification, not a validator or ownership change. Kake owns publisher policy and the audit of served response bytes; the current C2 pipeline does not inspect rendered DOM. The specific JS-rendered-canonical frontier is still open. Route any browser/DOM observation to tabi, while treating that route as future work rather than a capability already measured.

## Findings

### P3 — Keep C2's live-response audit distinct from rendered-DOM verification

**Impacted claims/axes:** C2 operability; freshness claims made from its dated snapshots. C2 establishes a reproducible, time-stamped policy result for fetched HTML bytes, not that every policy result is clean, that JavaScript leaves the canonical unchanged, or that Google selects it.

**Evidence:**

- `PROVINCE.md:22-23` leaves “canonical/JS rendering” in the Frontier; `PROVINCE.md:30-31` assigns browser/client-side crawler discipline to tabi and publisher-side placement to kake. The round-22 boundary is explicit at `PROVINCE.md:52-58`: the static validator/fixtures are not a live-site or Google-selection claim, and JS-rendered canonicals remain open.
- `corpus/knowledge/static-canonical-preflight.md:7-10` says the entry owns publisher-side static-file validation, not browser crawling. `SKILL.md:407` routes JS-state/browser work to tabi; `SKILL.md:411` registers only `canonical-audit` as the domain gate. `SKILL.md:413-416` says matrix/measurement/replay helpers are evidence tools, not extra domain gates. A search for `live_snapshot` in `SKILL.md` returned `No matches found`.
- The implementation is byte-level: `scripts/live_snapshot.py:50-81` builds a `GET`, reads at most `MAX_BODY + 1` response bytes, and considers only a complete 2xx `text/html` body served; `scripts/live_snapshot.py:84-91,121-128` passes the final response URL and those saved bytes to the validator and records its receipt. `scripts/canonical_audit.py:615-663` decodes the supplied bytes and feeds them to `CanonicalHTMLParser`; it does not execute JavaScript or inspect a browser DOM.
- The frozen scope agrees: `.ufo/waves/round-23/contract.json:21-26` defines C2 as a receipt for “live-served HTML,” describes the snapshot as served bytes, and excludes search-engine selection. `measure_c2.py:78-108` reproduces the audit result and sets each row's `pass` from whether the receipt has reproduction problems, not whether the validator verdict is `clean`. This is correct for an operability counter, but means a reproduced `failed-policy` or `could-not-evaluate` result must not be summarized as a clean canonical population.

**Concrete cached observation / counterexample:** The current round cache records a GET of `https://ufo-fsd.kimi.pro/` at `2026-10-21T06:33:12Z`: `.ufo/waves/round-23/live/ufo-fsd-kimi-pro/fetch.json:2-12` says `bytes: 612`, `status: 200`, `method: GET`, `contentType: text/html; charset=utf-8`, `truncated: false`, no redirects. Its `.ufo/waves/round-23/live/ufo-fsd-kimi-pro/audit.json:1-12` records `exit: 1`, `canonical_missing`, `verdict: failed-policy`. This is a counterexample to the broad assertion “C2 acceptance means every live surface has a clean canonical”: C2 is designed to count faithful/reproducible receipts, not only clean policy outcomes. I did not run `measure_c2.py` and do not claim an accepted count. The cache also records a useful positive counterexample to “live static preflight cannot evaluate any served page without a browser”: `charter-ghp/fetch.json:2-12` records a 53,660-byte HTTP 200 HTML GET and `charter-ghp/audit.json:1-8` records `exit: 0`, `pagesChecked: 1`, `verdict: clean`. Neither result says anything about later DOM mutation or Google selection.

These are cache observations, not requests made by this connector; `.ufo/waves/round-23/live/` was untracked at the observed HEAD. The property map itself labels the same `ufo-fsd.kimi.pro` surface a “612B SPA shell” (`SKILL.md:23`), so the static `canonical_missing` finding is evidence about the served shell only, not proof of what its browser-rendered DOM contains.

**Smallest move:** Add one sentence in the round-22 preflight section of `SKILL.md` or the C2 handoff: “Round-23 `live_snapshot.py` audits fetched response bytes at the final URL; it does not execute JavaScript or inspect rendered DOM, which remains an open tabi-routed frontier.” Keep C2's current receipt-reproduction predicate and do not register `live_snapshot.py` as a second canonical gate. This makes the operability result and freshness timestamp useful without claiming a rendered-DOM check or changing the frozen contract.

**Risk:** Calling C2 “clean” when it is only receipt-complete would hide real `canonical_missing` and `html_unsupported` observations. Conversely, requiring all C2 validator verdicts to be `clean` would conflate website policy health with the declared operability axis and would alter the frozen acceptance rule. A separate browser observation must not be inferred from the static snapshots.

**Verification (not run):** After integration, run the contract's exact counter command, `python3 .ufo/waves/round-23/measure_c2.py --root . --revision <integrated-commit>`, and confirm all twelve receipts reproduce; report policy verdicts separately from C2 receipt acceptance. Check that the scope note routes DOM/JS work to tabi and that no second domain gate is introduced. No browser observation is claimed here.

## Checked and held

- Read the requested `PROVINCE.md`, `corpus/README.md`, `corpus/knowledge/static-canonical-preflight.md`, `SKILL.md` (property map and canonical gate section), and round-23 `contract.json`, plus the C1/C2 populations, C2 counter, snapshotter, validator, and available round-23 snapshot records.
- C1 is specifically the sixteen historical knowledge units plus `SKILL.md` property map (`.ufo/waves/round-23/c1-population.json:4-73`); the new `static-canonical-preflight.md` is not one of those historical units. Its own metadata (`:2`) explicitly distinguishes recent source-document checks from live website verification.
- The observed lane HEAD was `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`, one commit after candidate `4d95d2e`; the round-23 snapshot directory and assigned report directory were untracked at that point. I wrote only this assigned report.
- No external request, browser action, publisher action, build, test, selftest, formatter, or counter was run by this connector; no tools were installed or updated.

## Limits

The cache is a point-in-time GET snapshot and was untracked, so it is not presented as a committed or independently admitted receipt. I did not inspect a live browser DOM, determine whether any page mutates its canonical at runtime, verify Google-selected canonicals, or independently execute the C2 counter. Ownership of an implemented rendered-DOM canonical gate is not evidenced: local sources say the frontier remains open and identify tabi as the browser/client-side discipline owner, so a future DOM check needs an explicit routed task.