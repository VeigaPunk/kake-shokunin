# C1 sealed-key review — case expectations vs public contract (operability)

**Attack:** whether all 24 sealed expectations follow SCORECARD round-35 C1 (a–c) plus the round-34 interface. Primary axis: operability; freshness is out of scope.

**Findings:** case-05's `clean` expectation conflicts with the exact-name required-property rule. Cases 17 and 24 depend on the unresolved relative-URL/canonical comparison fork (quoted below). Case 19 follows the literal contract but shares the HTML-tree mismatch category described in the ambiguity note. The remaining expectations are supported by the public text.

| Case | Test; sealed expected result | Contract check / ambiguity dependency | Evidence |
|---|---|---|---|
| 01 | Template-contained `og:image`; exit 1, `og_required_missing(og:image)` | Yes: template contents count neither as OG property nor canonical. | `sealed/c1-cases.json:3-31` |
| 02 | SVG-contained canonical link; exit 0 clean | Yes: link inside open SVG is excluded; remaining metadata and canonical match. | `sealed/c1-cases.json:32-54` |
| 03 | Relative canonical resolves to OG URL; exit 0 clean | Yes: round-34 canonical URL resolution rule. | `sealed/c1-cases.json:55-77`; `round-34/c1-matrix.json:10-12` |
| 04 | Empty second `og:url`; exit 0 clean | Yes: empty value is not non-empty; round-34 strips ASCII whitespace. | `sealed/c1-cases.json:78-100`; matrix `:10-11` |
| 05 | `og:image:url` near-match; exit 0 clean | **No.** Exact property matching means no `og:image`; expected result should be exit 1 / `failed-policy` with `og_required_missing(og:image)`. | `sealed/c1-cases.json:101-123`; matrix `:10-11`; SCORECARD `:1388-1394` |
| 06 | Directory page unreadable, continue auditing other pages; exit 2 with `page_unreadable` and page-2 `og_type_multiple` | Yes: non-regular file is unreadable; readable-page policy finding is retained beside input finding. | `sealed/c1-cases.json:124-171`; SCORECARD `:1388-1393` |
| 07 | Latin-1 page beside readable page; exit 2, `page_unreadable` only | Yes: page must be UTF-8; other page is clean. | `sealed/c1-cases.json:172-207`; SCORECARD `:1388-1393` |
| 08 | One readable page missing `og:type`; exit 1, `og_required_missing(og:type)` | Yes: required-property rule applies per page. | `sealed/c1-cases.json:208-250`; matrix `:10-11` |
| 09 | Complete ordinary metadata/canonical page; exit 0 clean | Yes: round-34 rules. | `sealed/c1-cases.json:251-273`; matrix `:10-12` |
| 10 | Duplicate `og:type`; exit 1, `og_type_multiple` | Yes: round-34 counts multiple elements. | `sealed/c1-cases.json:274-302`; matrix `:11` |
| 11 | Canonical only inside template; exit 0 clean | Yes: template link is not canonical; absent outside canonical is not a mismatch. | `sealed/c1-cases.json:303-325`; SCORECARD `:1384-1387` |
| 12 | Two different non-empty `og:url` elements; exit 1, `og_url_multiple` | Yes: C1(a) counts elements; first URL matches canonical. | `sealed/c1-cases.json:326-354`; SCORECARD `:1380-1383` |
| 13 | `manifest.pages` has wrong shape; exit 2, `input_invalid` without page | Yes: round-34 requires non-empty pages array. | `sealed/c1-cases.json:355-377`; matrix `:8-9` |
| 14 | Template canonical followed by outside canonical; exit 1, `og_url_not_canonical` against outside link | Yes: template link counts neither; outside link is the first canonical. | `sealed/c1-cases.json:378-406`; SCORECARD `:1384-1387` |
| 15 | Latin-1 page plus readable page missing image; exit 2 with `page_unreadable` and `og_required_missing(og:image)` | Yes: (c) expressly retains readable-page policy findings. | `sealed/c1-cases.json:407-447`; SCORECARD `:1388-1393` |
| 16 | Relative canonical `/b/`; exit 1, `og_url_not_canonical` | Yes: resolve against page URL, then compare exact strings. | `sealed/c1-cases.json:448-476`; matrix `:11` |
| 17 | Relative sole `og:url` with absolute canonical; exit 1, only `og_url_not_absolute` | **Not settled.** Round-34 limits canonical comparison to absolute OG URLs; C1(a) says first non-empty URL gets the canonical comparison, which would add `og_url_not_canonical`. Depends on ambiguity-note item 3's fork. | `sealed/c1-cases.json:477-505`; SCORECARD `:1380-1383,1394`; ambiguity `:17` |
| 18 | Whitespace-only title; exit 1, `og_required_missing(og:title)` | Yes: ASCII-whitespace-only content is empty under round-34. | `sealed/c1-cases.json:506-534`; matrix `:10-11` |
| 19 | `og:type` meta directly inside MathML; exit 0 clean | Yes under the literal C1(b) wording. **HTML mismatch:** expected exclusion uses the same literal-vs-HTML-tree distinction noted in ambiguity item 6 (its example is `<math><mi>`, not this exact markup); this is not an undecided text reading. No parser comparison run here. | `sealed/c1-cases.json:535-557`; SCORECARD `:1384-1387`; ambiguity `:20` |
| 20 | `name=og:title` instead of `property`; exit 1, `og_required_missing(og:title)` | Yes: only the exact `property` attribute counts. | `sealed/c1-cases.json:558-586`; matrix `:10-11` |
| 21 | Missing `og:image`; exit 1, `og_required_missing(og:image)` | Yes: required-property rule. | `sealed/c1-cases.json:587-615`; matrix `:10-11` |
| 22 | FTP page URL in manifest; exit 2, `input_invalid` without page | Yes: manifest URL must be absolute HTTP(S). | `sealed/c1-cases.json:616-644`; matrix `:8-9` |
| 23 | Two identical non-empty `og:url` elements; exit 1, `og_url_multiple` | Yes: C1(a) says more than one element; ambiguity item 1 explicitly favors counting identical elements, not undecided. | `sealed/c1-cases.json:645-673`; SCORECARD `:1380-1383`; ambiguity `:15` |
| 24 | Relative first URL, absolute second URL equal to canonical; exit 1, `og_url_not_absolute` + `og_url_multiple` | **Not settled.** Literal C1(a) comparison would additionally produce `og_url_not_canonical`; unchanged round-34 conditional would not. Exact ambiguity-note item 3 scenario. | `sealed/c1-cases.json:674-707`; SCORECARD `:1380-1383,1394`; ambiguity `:17` |

## Findings and quoted ambiguity

1. **Confirmed expectation defect — case-05.** Its HTML has `property="og:image:url"`, not the exact required `og:image`, while the sealed key expects clean. Round-34 says the property attribute must equal the name exactly and lists `og:image` as required. This expected result is therefore not a valid public-contract oracle.
2. **Contract ambiguity affects cases 17 and 24.** The ambiguity note says: “The first og:url is relative, the second is absolute and equals the canonical link.” It contrasts both checks with the base `elif` and concludes: “Undecided: bullet (a) reads as A, and the "unchanged" clause reads as B.” Case 24 is that exact input shape; case 17 has the same relative-first/canonical-comparison conflict without a second URL. Their expected findings cannot be justified from the public text alone.
3. **HTML mismatch, not a text ambiguity — case-19.** C1(b) literally excludes tags inside open MathML; the ambiguity note identifies the opposing HTML-tree interpretation for MathML integration-point content. Case 19 is a direct MathML child rather than the note's `<math><mi>` example, so I classify this as the same mismatch category, not as a proved identical probe result.

## Evidence and verification

- Read SCORECARD C1 contract `:1379-1396`; round-34 interface `c1-matrix.json:6-14`; all sealed case records `c1-cases.json:3-707`; ambiguity note `:12-44`.
- SHA-256: sealed cases `a861dccdf63c21b2f731b5845ec016e216bee8bd7ad62df646d5e47e8bc1a391`; SCORECARD `f42056ee377c7d36025a8bfb5c607e92042ed0c57788b807a127b0f44f005803`; matrix `246a6a3ba67a842c408f56b0240d2ad36969330c5a414b715f04b7e56fac14f7`; ambiguity note `c03c58388ed8a4a8b7ffacd8368b1b948c485e5dc930fb72c277ec0cd0ffe4b3`.
- `mkdir -p /fast/scratch/hyaku/kake-r35/w2/ReviewSealedCasesVsContract/tmp && export TMPDIR=/fast/scratch/hyaku/kake-r35/w2/ReviewSealedCasesVsContract/tmp && unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r35/w2/ReviewSealedCasesVsContract/clone && git -C /fast/scratch/hyaku/kake-r35/w2/ReviewSealedCasesVsContract/clone checkout -q b1cbbc39 && git -C /fast/scratch/hyaku/kake-r35/w2/ReviewSealedCasesVsContract/clone rev-parse --short HEAD` (exit 0; `b1cbbc3`).
- In that clone: `export TMPDIR=/fast/scratch/hyaku/kake-r35/w2/ReviewSealedCasesVsContract/tmp && unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && cd /fast/scratch/hyaku/kake-r35/w2/ReviewSealedCasesVsContract/clone && timeout 120 python3 -B .ufo/waves/round-35/sealed_count.py c1 --root . --revision b1cbbc39 --key-revision 4c6be2bdec5630166c4013e53c226b1119ec63cc; echo "COUNTER_EXIT=$?"` (counter exit 0; shell exit 0; reported `cases:24`, `passed:24`, every case `passed:true`).
- `sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-35/sealed/c1-cases.json /home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/c1-matrix.json /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-35/w1/CriticC1ContractAmbiguity.md` (exit 0; hashes above).
- Counter result verifies only agreement with its sealed expectations; it does not validate those expectations against the contract. No separate per-case runtime or HTML5-parser comparison was run. No tools were installed.
