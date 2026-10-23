# CriticSourcesDecisions — retained-source attack
Axes: freshness (attribution and scope); operability (downstream interpretation, not measured behavior).
Checked: SOURCES.md rows S106–S115; ReopenS111–S114; retained Python, namespace, datatype, protocol and Yandex HTML; SHA256SUMS.
Commands run: none; exit codes: N/A. Critic used read/glob/grep only. No tests, runtime probes, live requests, digest recomputation or tool installations.
Paths below are lane-relative; `src/` means `.ufo/waves/round-40/sources/`, and `w1/` means `.ufo/waves/round-40/w1/`.

## S115 supersedes S111 — holds as a source-provenance correction
- Evidence: `src/py-urllib-parse.html:400–402` explicitly strips leading C0/space and removes TAB/CR/LF anywhere; `:419–420` says “urlsplit() does not perform validation.” Version notes at `:439–445` distinguish the old stripping changes from 3.15's new parameter.
- Counterexample to S111's inference: stripping a character is not an instruction to reject its input. The source expressly leaves validation outside this function. The leading-TAB/contract-strip counterexample is recorded at `w1/ReopenS111.md:19`; it was not executed or independently contract-checked here.
- `corpus/SOURCES.md:123` now attributes rejection to the lane, after sentence 21's strip, rather than to Python. This repairs the false provenance in `:119`; the retained source supports the correction, not a universal rejection rule.
- Smallest safe correction to the decision: none. The lane-contract interpretation itself is outside this retained-source check.

## Rejection of ReopenS114's “overstated” finding — holds for sitemap page URLs
- Direct located text: `src/yandex-sitemap.html:223`: “Specify only page links of the domain where the file will be located.” `:224` separately requires file/site co-location. Thus the restriction is not merely about file placement, contrary to `w1/ReopenS114.md:32`.
- “Page links” versus “URLs” does not defeat that paraphrase: `:91` shows the page URL in `loc`; `:153` explicitly says “page URLs”; `:229` says to define canonical URLs for included pages.
- Strongest retained counterexample: `:214` mentions localized pages/images; `:326` allows subdomains in the glossary's definition of an internal link. Neither states an exception allowing cross-domain page `loc` entries. They do prevent deriving an exact-host/subdomain ban or a rule for every extension URL from this page.
- Smallest safe clarification, if desired: “same-domain page URLs only”; do not silently strengthen “domain” to exact hostname. The assigned rejection need not be reversed.

## S112 corrects S106 — holds
- Evidence: `src/xml-names.html:206–211` defines expanded names as namespace/local-name pairs; `:288–301` specifies identical character strings, case-sensitive, with no percent-escaping done or undone; `:503–508` makes prefixes placeholders. Defaulting applies to unprefixed elements within scope, not directly to attributes (`:654–666`).
- Counterexample to the old authority claim: `src/sitemaps-protocol.html:1321–1349` permits an extension namespace and demonstrates its element; it supplies no instruction to ignore it. Searches for `ignor` found no occurrence in either retained namespace/protocol file. XML's reserved-prefix nonfatal-error rule (`xml-names.html:459–467`) is not a foreign-element ignore rule.
- `corpus/SOURCES.md:120` correctly separates namespace membership from sitemap requirements and retracts `:114`'s “comes from S102” attribution. Smallest safe correction: none; keep ignore behavior explicitly lane-owned.

## S113 corrects S107 — holds
- Static counterexample to `corpus/SOURCES.md:115`: `2026-10-23` has no seconds yet matches date production [18] (`src/xmlschema11-2.html:3348–3350`); date expressly requires hour/minute/second absent (`:3304–3308`). No runtime validation was performed.
- DateTime production [16] requires seconds or end-of-day (`:3081–3084`); its regex contains `24:00:00` (`:3151`), while date's does not (`:3368`). Both productions allow an absent timezone; the shared offset grammar stops at ±14:00 (`:10984–10987`). These support the corrected distinction in `corpus/SOURCES.md:121` and `w1/ReopenS113.md:19–27`.
- Smallest safe correction: none. The inherited comparisons to lane sentences 28–32 were not independently rechecked against the out-of-scope contract.

## Fixable residual: S115 scope separation is overstated
- `corpus/SOURCES.md:123` adds “and that it does not validate” but retains “not S027's ‘parsing is not validation’ scope.” Its own wording excludes the very topic it now includes; `src/py-urllib-parse.html:419` is explicitly a nonvalidation warning.
- Smallest safe correction: delete that stale S027-scope exclusion from S115, retaining the WHATWG/RFC conformance exclusion. This is an attribution/clarity defect on freshness, not evidence of an operability regression or a reason to reverse the source correction.

Freshness limit: manifest entries `src/SHA256SUMS:1,4–6` agree textually with the relevant registry digests; unchanged recorded hashes support interpretive corrections, not a claim of revised specifications. Live freshness and byte/digest integrity were not independently verified. No round verdict is issued.
