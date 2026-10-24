# CriticD1Reject — source-only adversarial review

Axes: **operability** (assigned); freshness unchanged. No canonical scoring, admission, or round verdict.
Scoped assessment: **rejection holds** for D1's version-only examples.

## Strongest case that D1 is a deviation
- `.ufo/waves/round-39/c1-contract.md:38-39`, sentence 8: “The file must be well-formed XML 1.0 with namespaces; otherwise `xml_malformed`”. That names a document requirement, not merely successful parsing.
- `.ufo/waves/round-39/resid/ReviewBuildContract.md:7-8` reports `1.1`, `1.5`, `1.9`, `1.10` producing clean and calls the expected result `xml_malformed` because the “contract names XML 1.0”. This is retained report evidence, not a run by this seat.
- `.ufo/waves/round-40/sources/xml-1.0.html:492-494` says an XML declaration “specifies the version of XML being used”; §1.1 at :191-196 identifies the specification as supplying information to “understand XML Version 1.0”. A strict reading could distinguish a document declaring 1.1 from a 1.0 document.
- The strongest attack on the Gate's reasoning is therefore that processor compatibility does not itself establish document identity or well-formedness. A Note describing acceptance cannot, by itself, erase a contradictory normative grammar or well-formedness constraint.

## Dispositive contrary evidence
All XML quotations below are from the retained `.ufo/waves/round-40/sources/xml-1.0.html` (markup stripped).
- :269-273 defines well-formedness through matching the `document` production, meeting “all the well-formedness constraints given in this specification”, and well-formed referenced parsed entities.
- §2.8 :509-513 supplies these productions:
  `[24] VersionInfo ::= S 'version' Eq ("'" VersionNum "'" | '"' VersionNum '"')`
  `[25] Eq ::= S? '=' S?`
  `[26] VersionNum ::= '1.' [0-9]+`
- Thus all four D1 version strings match the XML 1.0 grammar. Neither [24] nor [25] imposes an additional version-equals-1.0 condition.
- Crucially, :516-517 says “XML 1.0 documents SHOULD NOT specify a version number other than '1.0'.” This is not a MUST, a different grammar production, or a well-formedness constraint. It expressly discusses XML 1.0 documents carrying other matching version numbers.
- The Note at :517-520 then confirms the reading: “When an XML 1.0 processor encounters a document that specifies a 1.x version number other than '1.0', it will process it as a 1.0 document.” Its essential qualifier is: “provided they do not use any non-1.0 features.”
- §1's identification of the specification as Version 1.0 does not override its explicit version grammar. The status text at :68-78 also distinguishes edition from version: “This fifth edition is not a new version of XML”; an older edition's restrictions cannot silently replace the retained text.

## Counterexample and impact
- Source-derived counterexample to a strict D1 fix: UTF-8 `<?xml version="1.1"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.invalid/a</loc></url></urlset>` with a valid manifest check and `sitemapUrl` of `https://example.invalid/sitemap.xml`.
- [INFERENCE] This has the same XML 1.0 grammar and namespace compliance as its `version="1.0"` counterpart; changing the version alone supplies no sentence-8 violation. A mandatory version-equality gate would introduce a false `xml_malformed`, harming operability by adding policy not present in sentence 8.
- This is a paper counterexample, not an executed tool result. It does not establish acceptance of XML-1.1-only features, arbitrary major versions, or every malformed 1.x document.

## Per-statement disposition and smallest safe correction
- `corpus/lessons/round-40.md:26-29`, rejection of D1: **holds**, specifically for “`version="1.1"` with 1.0 content”. The qualifier prevents a blanket XML 1.1-support claim.
- `SCORECARD.md:2571-2574`, “D1 is not a deviation”: **holds** for the version-only D1 observations at `ReviewBuildContract.md:7-8`; not a finding that every possible XML-version behavior is correct.
- `ReviewBuildContract.md:7-8`, expected `xml_malformed` solely because the contract names XML 1.0: **wrong** under the retained Fifth Edition grammar.
- The claimed existing `version="2.0"` runtime result was not independently checked. It is unnecessary to this conclusion; [26] excludes `2.0` as a grammar matter. `.ufo/waves/round-40/l1-probe.py:16-17` defines v11/v20 inputs, not retained stdout proving their results.
- Smallest safe correction: **no tool change for D1**. Strengthen both rejection rationales by citing [26], the preceding SHOULD NOT paragraph, and the Note's non-1.0-feature qualifier; do not rely on processor acceptance alone. This is a fixable explanatory weakness, not a reason to accept a stricter version gate.

## Execution accounting
Read-only inspection via `read`/`grep`; only this report was written. Shell/runtime commands: none; exit codes: not applicable.
Tools built/scored: none; tool paths/SHA256 and counter passed/byClass/selftest/met: not applicable. No check is represented as run or passed.
No network requests, installations, subprocesses, lane code edits, or shared-artifact edits.
Report: .ufo/waves/round-40/w1/CriticD1Reject.md
