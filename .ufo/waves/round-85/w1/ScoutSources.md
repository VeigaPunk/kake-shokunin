# ScoutSources — round 85, wave 1

Author-side source grounding and bounded planning data-walk; not independent closure. Production unchanged. Assimilation: none.

## Axes and operative inputs

Axes: source fidelity, scope containment, reproducible provenance, dependency clarity. Read frozen contract and count.py before source analysis; read operative binding receipt before analysis: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/bindings-read.md` records all 18 roles @m_zfl, no model argument, configuration sha256 2014653da3c365e9091c902bdc2c605052b0c5b7514882b6de8b6824147cd5c6, pacman paused and no installs. This is an observation of the receipt, not an independent configuration audit.

## Retained source

URL and final URL: https://w3c.github.io/webappsec-referrer-policy/ . GET at 2026-11-04T14:51:09.473548+00:00, HTTP 200, 246577 raw bytes, sha256 339bdd20be241c9eca2f47a18d35368af460edfc708288d90c51e094393743a6. Source observation date: 2026-11-04. Document labels itself Editor’s Draft, 20 March 2026; its status warns it is work in progress, not endorsed W3C final text.

Assets are under `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ScoutSources/`: `source.html` (unmodified fetched bytes), `body.txt` (body-only stripped text, script/style omitted, whitespace normalized), `receipt.json` (URL/status/time/bytes/digests/response headers). Text: 34966 UTF-8 bytes, sha256 f1ea4ce688c9cec1f88561968e867ed0ecdd7fa2c51a998965ebb1e9f630cca8.

## Located findings

Observed, high confidence: §8.1 `#parse-referrer-policy-from-header`, raw HTML lines 1596–1621, body.txt lines 480–494. Steps extract header list values, initialize policy to empty, assign each recognized nonempty token in sequence, then return policy. Located quote (23 whitespace-separated words), body.txt 488–490:

> For each token in policy-tokens, if token is a referrer policy and token is not the empty string, then set policy to token.

Observed, high confidence: §3, body.txt 148–166, defines the empty string plus eight nonempty tokens: `no-referrer`, `no-referrer-when-downgrade`, `same-origin`, `origin`, `strict-origin`, `origin-when-cross-origin`, `strict-origin-when-cross-origin`, `unsafe-url`. §8.1 deliberately excludes the empty token from assignment. No recognized token therefore returns empty; do not substitute the browser default `strict-origin-when-cross-origin` into this parser’s result.

Observed, high confidence: §11.1 `#unknown-policy-values`, body.txt 633–651, says unknown values are ignored and the latest recognized value is used; multiple field lines and comma-separated values are equivalent **with sequence preserved**. §4.1, body.txt 383–396, uses list syntax and says values should not be quoted. This is not permission to reorder members.

Case: the frozen decoder contract explicitly requires case-sensitive matching. [INFERENCE, high confidence] §3’s exact strings and §8.1’s membership test support that reading: the algorithm contains no lowercase conversion or case-insensitive comparison. Thus `NO-REFERRER` is unrecognized while `no-referrer` is recognized. Caveat: §4.1’s ABNF literal grammar by itself is not proof of case-sensitive semantic matching; distinguish grammar acceptance from §8.1’s policy selection. The retained page does not explicitly say “case-sensitive.”

Whitespace: surrounding token whitespace is stripped under the frozen local interface; internal whitespace is not removed, and quoted tokens are not unquoted. §8.1 delegates extraction to Fetch (`https://fetch.spec.whatwg.org/#extract-header-list-values`, raw HTML 1604–1605), while §4.1 supplies comma-list grammar and §11.1 supplies comma-list examples. The named URL was the only external source fetched: Fetch’s detailed whitespace character set was not opened. Therefore broad Python/Unicode stripping is a **local contract choice**, not established by this retained page alone. Ordinary surrounding spaces are expressly exercised by frozen CASES[9]; tabs, Unicode whitespace, quoted commas and arbitrary malformed HTTP bytes are not measured by those ten cases. Do not claim full Fetch conformance from C2.

## Lesson Gate candidates: reason and flip

- **ADMIT S458**, spec/tier A for the scoped header-token algorithm, opened 2026-11-04 at the URL above. Located quote: the 23-word §8.1 sentence above. Reason: repeated assignment proves last-recognized-nonempty selection and preserves field/member sequence. Flip to reject or revise if a later retained draft changes that loop, its token vocabulary, or its extraction contract; reopen source before asserting later behavior.
- **REJECT blanket-reorder equivalence**, not the source. Same URL/date and same located §8.1 quote. Reason: `no-referrer, strict-origin` selects `strict-origin`; reversing it selects `no-referrer`. Sorting or set-comparing tokens destroys this semantic difference. Flip only for a narrower, proven transformation that leaves the last recognized token unchanged (for example, reordering ignored tokens without moving recognized tokens), or a future source revision explicitly making selection order-independent. Neither licenses arbitrary-header equivalence or publication approval.

## Bounded planning data-walk

1. Operative binding receipt + frozen contract + count.py → fixed ownership, two claims, exact populations and oracle. No seat may integrate production; L1 integrates after WAVE-DONE.
2. C1 branch: three missing eight-cell instrument rows → executor registry proposals → reviewer predicate/scope review → L1 integration → frozen C1 count. No semantic-upgrade inference for the experimental general classifier.
3. C2 branch: independent GET receipt → §3 vocabulary + §8.1 loop + §11.1 ordering → this S458 row proposal → scribe knowledge/lesson proposals and executor offline decoder proposal. These drafting nodes can proceed concurrently once the contract/source semantics are fixed.
4. Join: source-grounded decoder and corpus proposals + review/attack findings → WAVE-DONE → L1-only integration → ten-case C2 count. Frozen cases 0/1 force opposite effective values; case 6 exercises uppercase rejection indirectly, case 9 surrounding spaces; neither constitutes comprehensive syntax coverage.
5. Separate evidence nodes: unchanged-base controls, prose-only C1 control and constant-output C2 control; decoder selftest/exit checks; retained round-84 control-pair trial; before/after census. These remain integrator/assigned-seat work, not executed here. Trial values do not enter the ten-case numerator. D84-2/3 substantive debts remain open; no full D84 closure, rank or publishing claim.

## Candidate registry row

Exact proposed eleven-cell row is retained in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ScoutSources/S458.row.md`. It follows the currently observed SOURCES table columns and mined/180d convention. `used-by` is the required `corpus/knowledge/referrer-policy-effective.md`. Registration has not occurred; ID/URL collision checking remains the connector’s assignment.

## Commands, exits, limits

- Source acquisition: Python stdlib `urllib.request.Request(url, method='GET')` + `urlopen(..., timeout=60)` inside eval; completed without exception, recorded exit 0, HTTP 200. A separate read-tool GET opened the same permitted public URL for reading before retained acquisition. No other remote URL was fetched.
- Extraction/receipt: stdlib HTMLParser + hashlib.sha256 + JSON, completed in the same successful eval. No external tools installed or updated; no shell commands or VCS commands run.
- Targeted reads/searches located contract, counter, binding receipt, registry examples and retained source anchors. `xd://` inventory had no lsp device; semantic source-code navigation unavailable. Counter observations are literal reads, not LSP proof, and no exported code contract was changed.
- No checks/tests/counters/builds were run: none assigned to this seat. No candidate decoder or real retained-pair effective values are claimed measured here.
- No scratch directory was created or used; source bytes went directly to the allowed deliverable directory. Hence no scratch artifacts remain to delete. No production, sibling, fleet, PATH or VCS mutation.

Report: .ufo/waves/round-85/w1/ScoutSources.md
