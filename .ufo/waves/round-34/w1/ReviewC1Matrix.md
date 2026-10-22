# ReviewC1Matrix — grounding review of c1-matrix.json (r34 w1)

Scope: are the 28 expected outcomes grounded? Reviewed the frozen matrix
(sha256 246a6a3ba67a842c408f56b0240d2ad36969330c5a414b715f04b7e56fac14f7 ==
counter pin in c1_matrix_count.py:16), the interface text, retained sources
S067.txt / S068.txt, counter c1_matrix_count.py (sha256 fc72d855cde3656fe74a… ==
receipt c1-at-d08d8de.json counterSha256), and receipt c1-at-d08d8de.json.
No source contradicts any expectation. Findings are coverage gaps and ambiguities.

## Per-case grounding

| Case | Rule tested | Grounding |
|---|---|---|
| K1 | control: 4 required present, og:url == canonical | S067 "The four required properties for every page are: og:title … og:type … og:image … og:url"; S067 "og:url - The canonical URL of your object"; S068 "og:url The canonical URL for your page" |
| K2 | repeated og:image is an array, clean | S067 Arrays: "just put multiple versions of the same <meta> tag on your page" |
| K3 | relative canonical href resolved vs page URL, equal → clean | lane policy (resolution mechanics; sources silent on relative hrefs) |
| K4 | no rel=canonical → no comparison | lane policy (rule precondition; neither source mandates rel=canonical) |
| K5 | per-page evaluation over manifest pages | lane policy (manifest is lane-invented); S067 per-page required props |
| K6 | ASCII whitespace stripped from content values | lane policy |
| D1 | og_required_missing og:title | S067 "four required properties" |
| D2 | og_required_missing og:type | S067 (same) |
| D3 | og_required_missing og:image | S067 (same) |
| D4 | og_required_missing og:url | S067 (same) |
| D5 | all four missing → 4 findings | S067 (same) |
| D6 | content empty after strip = missing | lane policy (interface line 4; sources silent on empty values) |
| D7 | name= og:image does not count | lane policy, supported by S067 markup examples (all property=; RDFa basis); no normative sentence |
| D8 | og:url differs from canonical → og_url_not_canonical | S067/S068 concept ("canonical URL"), mechanism is lane policy (see finding 5) |
| D9 | relative og:url → og_url_not_absolute, no canonical comparison | lane policy (assignment's own example); S067 URL type grounds http/https-ness only |
| D10 | two og:type elements → og_type_multiple | S068 "Each URL should be a single object, so multiple og:type values are not possible" |
| D11 | defect isolated to second page | lane policy mechanics + S067 per-page requirement |
| D12 | scheme-exact comparison (http ≠ https) | lane policy (exact string comparison declared); consistent with distinct URLs |
| D13 | meta property=og:type without content → missing | lane policy (interface: content non-empty; absent = no value) |
| I1 | malformed manifest JSON → input_invalid | lane policy |
| I2 | version 2 → input_invalid | lane policy (manifest v1) |
| I3 | empty pages → input_invalid | lane policy ("non-empty pages") |
| I4 | missing listed file → page_unreadable, input-only findings | lane policy; suppression half not exercised (finding 4) |
| I5 | ftp:// page URL → input_invalid | lane policy ("url: absolute http(s) page URL") |
| I6 | file escaping manifest dir → input_invalid | lane policy (path safety; fixture coherent — target exists on disk, tool must refuse) |
| I7 | --manifest names absent file → exit 2 input_invalid | lane policy — pins one of two readings of the interface (finding 2) |
| U1 | no args → 64 | lane policy (sysexits usage) |
| U2 | unknown flag → 64 | lane policy |

28 cases verified: 6 control, 13 defect, 7 input, 2 usage (python3 count, exit 0).

## Defects, severity-ranked

1. MEDIUM — untested interface rule: "a listed file that cannot be read as UTF-8 is
   page_unreadable" has no case; I4 covers only the missing-file path (checked: no
   case fixture contains non-ASCII bytes). A tool that crashes or exits 0 on decode
   failure passes 28/28. Add one input case with invalid UTF-8 in a listed page.
2. MEDIUM — interface sentence with two readings: exit-64 clause "missing --manifest"
   vs I7 expecting exit 2 input_invalid for an --manifest that names an absent file.
   A builder reading "missing --manifest" as "the named manifest is missing" emits 64
   and fails only I7 (27/28). One clause sentence ("a --manifest that cannot be read
   is input_invalid") removes it.
3. MEDIUM-LOW — untested tie-breaks: "first canonical link wins" (no page has two
   rel=canonical links) and "og_url_not_absolute … with a host" (no protocol-relative
   "//host/p" or scheme-only "https:///p" case). Both are declared but unpinned.
4. MEDIUM-LOW — untested suppression: interface says on exit 2 "only input findings
   are reported", but I4's readable page is clean, so no case has a co-present policy
   finding to suppress. The sorted-multiset comparison would catch a violation if a
   case existed (observed extra reasons change the projected multiset).
5. LOW — grounding overstated in notes: neither S067 nor S068 normatively ties og:url
   to <link rel=canonical>; S067 names link-rel canonical only as an inspiration
   ("inspired by Dublin Core, link-rel canonical, Microformats, and RDFa"). D8/D12
   notes citing "S067/S068" are honest about the concept but the comparison rule is
   lane-policy operationalization. No contradiction with the sources.
6. LOW — declared-but-unvalidated fields: no expected finding carries id or page
   (checked), so finding→page attribution is never asserted — D11 would pass a tool
   attributing the defect to the first page. pagesChecked is declared in the report
   object and never compared (constants report 0 and pass their gates). Both are
   explicitly declared in interface lines 1/5, so this is coverage, not violation.
7. LOW — "property attribute equals the name exactly": case-sensitivity and attribute
   whitespace handling are pinned by no case; html.parser vs regex implementations
   can diverge. K6 pads content values but never hrefs or attribute values.
8. LOW — manifest structural sub-rules untested: pages key missing, pages not a list,
   url missing/non-string, file not a string — all presumably input_invalid under
   "manifest v1", no case pins them.
9. INFO — contract duplication: "policy findings are not reported with them" appears
   only in I4's note, not the interface; notes carrying contract risk drift from the
   interface text.

## Constant gates (analytic)

constant-clean fails D1; constant-failed-empty fails K1 (and every exit≠1 case);
constant-refuse fails K1; constant-all-missing passes only D5, fails K1. Each gate
fails ≥1 case, so "all constants rejected" is achievable. Receipt c1-at-d08d8de.json
confirms: 0/28, toolPresent false, gates 6/28, 0/28, 6/28, 1/28, all-rejected true.

## Not verified

Did not run the counter against any audit tool (none exists at d08d8de; builders are
landing theirs this wave). Did not fetch any URL (network bounds). Did not open
S069–S072 (not needed for C1 grounding). All commands read-only; lane untouched
except this report file.
