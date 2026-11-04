# Round 76 — Amendment 2 (terms-only, recorded before any after-state)

Motivation: `w1/ScoutHreflangEdge.md` §3 enumerated **16 classes the frozen contract leaves undecidable**
(kill rule 1 would mark every case in them `undecided`, which would cost the matrix most of its cases and,
for A1 and A16, let the empty-list constant pass). This amendment **decides the undecided**; it changes no
verdict of any already-decided class. Every case whose verdict this amendment changes must be re-marked
`undecided` under the old terms and re-derived under these; a case cannot be scored under both.

Where a fetched source decides a line, the source and its location are named.

## A1 — informational findings
An informational finding (`hreflang_external_target`) appears in `findings` with `"severity": "info"` and
does not change the exit code: a run whose only findings are informational exits 0. Policy findings
(`severity: "policy"`) exit 1. Input faults exit 2. Sources for the id's existence: Google
`google-localized-versions.txt` "Missing return links : If page X links to page Y, page Y must link back to
page X."

## A2 — finding granularity
A policy finding is emitted **once per offending annotation** (one per `<link>` element), except
`hreflang_self_missing` and `hreflang_canonical_not_self`, which are emitted **once per page**, and input
faults, which are once per manifest entry.

## A3 — equality relations
Tag equality is ASCII case-insensitive. URL equality is exact string equality after RFC 3986 normalization
of both sides (scheme and host lowercased, default port removed, dot-segments removed, empty path → `/`); a
trailing `/` is significant. The id in each finding names the page it was found on.

## A4 — a non-absolute href is not resolved
A href that does not parse as absolute is reported as `hreflang_relative_href` and contributes to no other
finding (self-reference, reciprocity, canonical, external target).

## A5 — absent canonical
A page without a `rel=canonical` link has itself as its resolved canonical.

## A6 — multiple canonicals
The first `rel=canonical` link in document order is the page's canonical (the lane's round-35 precedent).

## A7 — canonical carrying hreflang
A `rel=canonical` link that also carries `hreflang` is still the page's canonical for this tool.

## A8 — input faults and policy findings together
When any input fault occurs the exit is 2; findings from pages that were read successfully are still
listed; a page that could not be read contributes no policy findings.

## A9 — link without href
A `link` element without an `href` attribute is not an alternate and is not reported.

## A10 — empty hreflang value
An empty `hreflang` attribute value is `hreflang_missing_value`, not `hreflang_invalid_tag`.

## A11 — x-default case
`x-default` is compared ASCII case-insensitively.

## A12 — absolute means scheme plus authority
`hreflang_relative_href` fires for any href that does not parse as an absolute URL with scheme and
authority under RFC 3986; the scheme need not be `http(s)`. Google, `google-localized-versions.txt`:
"Alternate URLs must be fully-qualified, including the transport method (http/https)".

## A13 — scanning rules
`rel` is a case-insensitive token set (`whatwg-links.html`, "Keywords are always ASCII case-insensitive");
a link whose `rel` tokens include `stylesheet` alongside `alternate` is not an alternate
(`whatwg-links.html`, "The `alternate` keyword does not create a link of its own"); `<template>`, `<svg>`
and `<math>` subtrees, comments, and `<script>`/`<style>` data are not scanned; an element self-closed as
`<svg/>` or `<math/>` opens nothing; entities are decoded before comparison; unquoted attribute values are
read as HTML reads them.

## A14 — noscript
Content inside `<noscript>` is scanned as markup (the scripting-off reading the lane recorded in round 35).

## A15 — manifest version and path policy
`version` ≠ 1 is exit 64. A `file` that escapes `--root`, is absolute, is a symlink, or is not a regular
file is `input_unreadable`. Two pages may not share a `file`.

## A16 — matrix comparison rule (counter-side, binds the C2 receipt)
A constant or tool that prints nothing must not be scored as `{exit: 0, ids: []}`. The matrix requires a
parseable JSON object carrying `version`, `pages` (count equal to the manifest's page count), `findings`,
`counts` and `exit`; a missing or unparseable object is a failed case. Finding ids are compared as a
**multiset** (the contract fixes no order). Each case declares its expected `{exit, ids}` multiset.

## A17 — the real-input run stays at 8 (Amendment 1)
Unchanged: the real-input population is the 8 retained served pages, four surfaces recorded `not-served`.
