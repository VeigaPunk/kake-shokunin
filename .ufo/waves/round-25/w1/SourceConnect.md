# SourceConnect — S035 conformance section vs packet `not-assessed`

Seat: `KakeR25.SourceConnect` (connector, read-only). Axes: operability, freshness. No website, browser, account or live-site action; the only network read was one GET of the pinned W3C Recommendation document.

## Evidence

- Source S035: `https://www.w3.org/TR/2024/REC-WCAG22-20241212/`, fetched 2026-10-21 13:21:54 UTC (HTTP 200, `last-modified: Thu, 12 Dec 2024 10:36:22 GMT`, 512457 bytes).
- SHA-256 `6e3c5fe397257cae509a2fb4752b73062cf8cbeb92c2cec618989b17e4cf7057`. This **equals** `sourceSha256` in `.ufo/waves/round-25/population.json` (`opened: 2026-10-21`), so the pinned population is still fresh against the live REC bytes.
- Section located: `#conformance-reqs` (5.2 Conformance Requirements), with subsections `#cc1` (5.2.1 Conformance Level), `#cc2` (5.2.2 Full pages), `#cc3` (5.2.3 Complete processes), `#cc4` (5.2.4 Only Accessibility-Supported Ways of Using Technologies), `#cc5` (5.2.5 Non-Interference). It ends at `#conformance-claims` (5.3 Conformance Claims (Optional)).
- Population count is consistent with the source: 31 Level A + 24 Level AA = 55. `#parsing` is headed "Success Criterion 4.1.1 Parsing (Obsolete and removed)", and the population correctly omits 4.1.1 (only `4.1.2` and `4.1.3` are present).

Each quote below was checked verbatim against the whitespace-normalized text of `#conformance-reqs`. Word counts are shown in brackets, and all are 25 words or fewer.

| Requirement | Location | Quote |
|---|---|---|
| Level AA | `#cc1` | "the web page satisfies all the Level A and Level AA success criteria, or a Level AA conforming alternate version is provided." [22] |
| Full pages | `#cc2` | "Conformance (and conformance level) is for full web page(s) only, and cannot be achieved if part of a web page is excluded." [22] |
| Complete processes | `#cc3` | "Conformance is not possible at a particular level if any page in the process does not conform at that level or better." [22] |
| Accessibility-supported | `#cc4` | "Only accessibility-supported ways of using technologies are relied upon to satisfy the success criteria." [14] |
| Non-interference | `#cc5` | "they do not block the ability of users to access the rest of the page." [15] |
| Non-interference scope | `#cc5` | "the following success criteria apply to all content on the page, including content that is not otherwise relied upon to meet conformance" [22] |

## How `status: not-assessed` differs from each requirement

`not-assessed` is a property of a **review card**: a criterion prompt that has not been applied to any page. Conformance, by contrast, is a property of a **web page or a process**, established only when every requirement in 5.2 holds ("all of the following conformance requirements must be satisfied"). The packet cannot produce conformance, for these reasons:

1. **Level AA (`#cc1`).** Level AA requires a page to satisfy all 55 A and AA criteria, or to provide a conforming alternate version. A card that is `not-assessed` makes no statement about any page. Even 55/55 cards accepted (`verdict: clean`) only means the packet's structure is ready. It is not 55 satisfied criteria, and the "conforming alternate version" route is not modelled at all.
2. **Full pages (`#cc2`).** Conformance is decided per whole page, including every responsive variation. Cards are organised per criterion, so they never combine into a page-level result.
3. **Complete processes (`#cc3`).** Conformance of a page in a process depends on every other page in the sequence, for example a checkout from start to finish. Even a fully reviewed single page could not claim conformance without the rest of its process. The packet has no concept of pages or processes.
4. **Accessibility-supported technologies (`#cc4`).** Success counts only through technology uses that are accessibility supported. Accessibility support is defined relative to users' assistive technologies and user agents (`#dfn-accessibility-supported`), which is outside the source text and outside the repository. A publisher-side card cannot establish it. This belongs in card `limitation` text, never in a status.
5. **Non-interference (`#cc5`).** Content that is not relied upon, or that does not conform, must still not block access to the rest of the page. The page must also keep conforming when such technologies are turned on, turned off, or unsupported. 1.4.2, 2.1.2, 2.3.1 and 2.2.2 apply to *all* content, including content not relied upon. Their cards therefore have a wider review scope than the other 51. Sibling reports `SC142.md`, `SC212.md`, `SC222.md` and `SC231.md` already mention this scope.

Contradiction stated plainly: `verdict: clean` together with `accepted: 55` looks like a pass/fail result shaped like Level AA. Per `#cc1` to `#cc5`, it is not one. The only page-level value the packet may ever emit is `websiteConformance: not-assessed`.

## Proposed move (single, bounded)

**Make `websiteConformance: "not-assessed"` an invariant that holds in every exit path, and cross-check it with the two existing verifiers. Do not change the schema.**

- `scripts/accessibility_packet.py` emits `websiteConformance: "not-assessed"` as a constant on exit 0, 1 and 2 (whenever JSON is emitted). It never derives this value from `verdict` or `accepted`.
- `.ufo/waves/round-25/measure.py` (seat `KakeR25.PacketCounter`) adds one cross-check: the returned object has `websiteConformance == "not-assessed"`. Any other value, or a missing field, is treated as an inconsistent tool result. This sits beside the existing row/total/exit cross-checks.
- `.ufo/waves/round-25/packet_selftest.py` (seat `KakeR25.PacketTests`) asserts the same field in the **pristine55** case (exit 0, `verdict: clean`). That is exactly the case where a reader would be most likely to read the result as Level AA.

This is a synthesis of the shared interface (which already fixes the field) and the conformance section, not a new feature: no new field, no new error ID, no card-schema change.

## Affected axes

- **Operability (improves):** the CLI's success output can no longer be read as a conformance level. The claim's "no website conformity claim" (contract `claim.after`) is then enforced by two independent checkers rather than documented once.
- **Freshness (neutral to positive):** no new source dependency. This report also records that the population hash still matches the live REC bytes on 2026-10-21, and that the 4.1.1 removal is reflected (55 = 31 + 24).
- **No harm:** adds no network access, no writes and no fields. The measurement counter and pass threshold are unchanged.

## Risks

- If the tool emits no JSON on exit 2 or 64, the measure cross-check must apply only when a JSON object is present. Otherwise it would turn a legitimate "input unavailable" result into a spurious failure.
- Peer seats own `measure.py` and `packet_selftest.py`. This seat edits neither. Main or the owners must decide whether to adopt the move.
- This move does not try to put 5.2.2 to 5.2.5 into card fields. Keeping card prose narrow is the scouts' job; widening the schema would break the exact-field interface.

## Verification (for main, after all seats land)

- `python3 -B scripts/accessibility_packet.py --root . --json` on the pristine 55 cards should give exit 0, `verdict: "clean"` and `websiteConformance: "not-assessed"`.
- Run the same with one card mutated (for example, `status: "passed"`). This should give exit 1, still with `websiteConformance: "not-assessed"`.
- `python3 -B .ufo/waves/round-25/packet_selftest.py --root .` should include the pristine55 assertion on this field.
- `python3 -B .ufo/waves/round-25/measure.py --root . --revision <commit>` should exit 0, and should fail if the tool output's `websiteConformance` is altered in an isolated copy.

## Tooling

No tools installed or updated. Used the existing `curl`, `python3`, `sha256sum` and `rg`. The fetched copy is at `/tmp/wcag22-rec-20241212.html`, outside the lane.
