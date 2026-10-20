# PublisherVsBrowser — static canonical preflight

Seat: connector, read-only. Axis: operability. Milestone: offline-canonical-capability.
Lane base observed: `7c61c8cc791bde36dd5e3688bdfea2678d90146c` (contract `base`).
No install. No package transaction. `scripts/canonical_audit.py` is absent on this lane tree (contract before-state). This report does not run that tool and does not admit C1.

## Evidence

Province split, still in force:

- `PROVINCE.md:22-23` — crawl hygiene’s first entry is `corpus/knowledge/crawl-scope-per-host.md`; “canonical/JS rendering open.”
- `PROVINCE.md:30-36` — `tabi` drives browsers and owns client-side crawler discipline; kake owns publisher-side placement. The the-musketeer Chrome profile lease stays with the integrator.
- `corpus/README.md:101-103` — open ground still names “canonical signals and JS-rendered canonicals” after round 21. Round 21 “adds no new publishing-domain coverage” (`corpus/README.md:117-119`).

Existing publisher-vs-browser pattern already in the lane:

- `SKILL.md:139-140` — `kimi-map` (E5) is browser-gated and never gates the “published” verdict.
- `corpus/knowledge/vault-properties.md:6-10` — a surface that looked JS-rendered was checked from the serialized `PROPERTIES` literal, with no rendered DOM. That closed the vault-link gap on 2026-09-28. It did not close canonical/JS rendering; province and the corpus frontier still list that ground open.
- `SKILL.md:212` — freshness-sweep `0` covers evaluated checks only; “Offline/skipped/suspended sections are never proof of a complete publishing check.”
- `corpus/knowledge/crawl-scope-per-host.md:44-54` — host-root robots bytes stay named operator debt. The entry records shape and sources, and states that no live response was collected.

Contract C1 is the publisher side of that split, not the browser side (`/.ufo/waves/round-22/contract.json`):

- Before: no lane-owned runnable canonical-policy validator; 0 accepted cases in a frozen 32-case matrix.
- Limits: “Explicit-head serialized static HTML only; policy comparison, not search-engine selection, JS rendering, HTTP headers, redirects, network freshness or publishing readiness.”
- Policy ignore list: comments, raw script, and template descendants. `noscript` is not on that list.
- Finding ids include `canonical_multiple`. Exit `0` is clean; exit `1` is failed policy.
- Debts that stay outside this claim: paths gate red (three targets / four legacy locations, missSet 55); anchor-census 78 is not a gate; no SHONEN promotion.

Local parser fact, exercised 2026-10-20 on `/usr/lib/python3.14/html/parser.py` (Python 3.14.8), not on a canonical auditor:

- `CDATA_CONTENT_ELEMENTS` includes `script` and is parsed as RAWTEXT (`html/parser.py:133-134`). A `document.createElement("link")` sequence inside `<script>` produced no `link` start tag.
- `HTMLParser(scripting=False)` is the default. The docstring (`html/parser.py:143-145`) says false parses `noscript` content normally, and true returns that content unparsed. The flag is not a script executor.
- Probe feed of one explicit-head canonical plus a second `<link rel="canonical">` inside `<noscript>`: `scripting=False` emitted 2 `link` start tags (both hrefs); `scripting=True` emitted 1 (the noscript href was absent).

## Contradiction (do not collapse)

Round 9’s “no browser” method and C1’s “no JS rendering” limit agree that kake does not drive a browser. They do not agree that every browser-hidden element is out of policy. Default HTMLParser emits a `noscript` canonical; a scripting browser does not. Contract limits exclude JS rendering and omit `noscript` from the ignore list, so the serialized default-parser tree is the publisher observation. Matching the scripting browser would be the absorption.

`script_decoy` is a different control. RAWTEXT already hides tags and runtime DOM writes inside `script`. A future noscript case that expected the same “ignore” result would encode `scripting=True`.

## Pattern to reuse

Reuse the E5 non-gating rule together with the vault literal method and the freshness-sweep disclaimer:

1. Inspect the serialized publisher artifact (explicit-head HTML on disk).
2. Keep browser/CDP/lease observations in another evidence class. They never flip this verdict.
3. Label exit `0` as clean for this policy only, not as crawler-selected, JS-rendered, or publish-ready.

Construct `HTMLParser()` with the default `scripting=False`. Do not pass `scripting=True` to approximate Chrome or Googlebot. Count a canonical `link` the default parser emits from `noscript` in the explicit head as a real candidate.

## Boundary not to absorb

- `tabi` browser driving, client-side crawler discipline, and the contested Chrome lease (`PROVINCE.md:30-36`).
- JS-rendered canonicals. They remain open frontier (`PROVINCE.md:22-23`, `corpus/README.md:101-103`), not a C1 consequence.
- `HTMLParser(scripting=True)`. That switch drops `noscript` children and is the browser-scripting tree.
- Search-engine selection, HTTP `Link` headers, redirects, network freshness, publishing readiness (contract `limits`).
- Kimi served-body rewriting (`sdk-seed.js`, `corpus/knowledge/vault-properties.md:70-76`). That is a third observer (live bytes versus source) and belongs to freshness, not this falsifier.
- Round-21 paths red, anchor census, and reconstructed Gate chronology (contract `debts`). No relabel.
- The frozen 32-name denominator. This falsifier is not a 33rd matrix row in round 22.

## Proposed move

Keep C1 on default-parser explicit-head links. In the knowledge/lesson scope (L1, not this seat), state that a clean verdict does not assert DOM equality with a scripting browser. Leave the falsifier below outside `measure.py`’s `total` of 32.

Affected axis: operability. The move blocks a false clean on two serialized canonicals. It does not change freshness, the paths gate, or the frozen population.

## Future falsifier — PVB-NOSCRIPT

Not part of the frozen matrix. Do not add it to `cases.json` this round.

Fixture `pvb-noscript.html` (regular file, no symlink):

```html
<!DOCTYPE html>
<html><head>
<link rel="canonical" href="https://example.test/project/a.html">
<noscript><link rel="canonical" href="https://example.test/project/other.html"></noscript>
</head><body></body></html>
```

Manifest page: `url` and `expectedCanonical` both `https://example.test/project/a.html`, `file` `pvb-noscript.html`.

Publisher expectation, from the contract ignore list plus the local parser probe: exit `1`, verdict failed policy, finding id `canonical_multiple` on that page. Two canonical `link` start tags are in the explicit head under `scripting=False`.

Scripting-browser expectation (not a kake command, not a measure input): one canonical element; the noscript child is not in the DOM. That observation must not be required to match the static exit.

Falsified if a future `canonical_audit.py --manifest <this> --json` exits `0` or omits `canonical_multiple`. That result means `noscript` was skipped (`scripting=True` or an ignore list the contract does not give) and the browser tree was absorbed.

Minimum pair once the tool exists, still outside this round’s 32:

- Accept: frozen `absolute_match` (one head canonical, no noscript) exits `0`.
- Reject: PVB-NOSCRIPT exits `1` with `canonical_multiple`.

## Risks

- An implementer can read `scripting=True` as “match the client” and turn this fixture into a false clean without failing `script_decoy`.
- Folding PVB-NOSCRIPT into the frozen 32 changes the population the measure counter is defined on (`accepted` / `total` 32).
- Treating round 9’s closed vault gap as closing JS canonicals overclaims province frontier.
- A noscript-only canonical that matches `expectedCanonical` is one default-parser link (exit `0`) and zero scripting-browser links. This falsifier uses two serialized links so the static failure is `canonical_multiple`, not that inverse. Do not “fix” the inverse inside C1 by enabling scripting.
- Unclosed `<script>` is RAWTEXT-to-EOF in this parser and can swallow a later real link. That is parser support (`html_unsupported` / exit `2` territory), not PVB-NOSCRIPT.

## Verification for L1

Not run here: no auditor, no matrix, no measure.

- `cases.json` names stay the contract’s 32; `pvb-noscript` is absent; measure `total` stays 32 on the baseline-unavailable and candidate paths.
- Auditor source constructs `HTMLParser` without `scripting=True`.
- After the tool exists, the fixture above exits `1` with finding id `canonical_multiple`, and frozen `absolute_match` still exits `0`.
- Auditor source has no CDP, lease, browser binary, or network fetch.
- Knowledge text, if added, says exit `0` is explicit-head serialized policy under the default parser, and JS-rendered canonicals stay open.

## Sources

No public URL fetched. Parser behavior is the local stdlib file cited above. Platform canonical documents stay with the source seats; this seat does not upgrade the unopened Google troubleshooting lead in `corpus/SOURCES.md:62`.
