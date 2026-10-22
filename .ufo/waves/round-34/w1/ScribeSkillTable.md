# ScribeSkillTable — SKILL.md decision table draft, round 34

Seat: leaf scribe. Draft only; the L1 owns the SKILL.md edit. No live request made; no
counter run by this seat. Insertion point in `SKILL.md` (991 lines at lane head
`a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f`): after the round-33 table, line 946, immediately
before `## Citing-set runner — round 33` (line 948). Shape copied from
`## Upstream source moved after a pin — round 33` (`SKILL.md:930-946`): Situation | Action |
Evidence command, with the grounding phrase folded into the last column so each row carries
its own source.

## Link-preview metadata — round 34

Grounded in S067 (ogp.me), S068 (Facebook sharing guide), S069 (Slack robots), S070
(Mastodon PreviewCard), and the tool contract in `.ufo/waves/round-34/c1-matrix.json`
(key `interface`, 28 frozen cases). Phrases are quoted verbatim from the retained visible
text (`.ufo/waves/round-34/sources/S0xx.txt`, one line per file; offsets are byte offsets)
or from the interface text. Counts are dated measurements (r16 rule, `SKILL.md:201`).

| Situation | What to check / action | Evidence command (round-34 result) | Grounding phrase |
|---|---|---|---|
| A page change could alter how a shared URL previews | Run the offline audit before and after the change; manifest is version 1, each page has `file` relative to the manifest directory and an absolute `url`; no network is involved | `python3 -B scripts/link_preview_audit.py --manifest <dir>/manifest.json` (`invocation`, c1-matrix.json) | interface: `manifest v1: {version:1, pages:[{file: relative path inside the manifest directory, url: absolute http(s) page URL}]}` |
| Someone wants to claim the tool meets its whole contract | Run the frozen counter at the landed commit; it reads the tool from `git show <rev>:scripts/link_preview_audit.py`, never the working tree, and four constant gates must each fail a case | `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root <repo> --revision <commit>` (at `d08d8de`: 0/28, `toolPresent:false`, `byKind` 0/6 control, 0/13 defect, 0/7 input, 0/2 usage; `constantGatesAllRejected:true`; `verification/c1-at-d08d8de.json`) | counter docstring: `each must fail at least one case, so a counter that a constant could satisfy is reported as broken` |
| Exit 1, `og_required_missing`, `property` names one of the four | Add that one property to the page source; `name=` does not count, and content that is only ASCII whitespace counts as empty | re-run the audit; the finding clears only for the named property (D1–D6, D7 exit 1 `og_required_missing og:image`; K6 exit 0) | S067.txt@955 `The four required properties for every page are:`; interface `name= attributes do not count` |
| A page carries the other three but no `og:image` | Treat it as the census's dominant defect, not a per-page accident: 101 of the retained 102 ds4cc pages lack a non-empty `og:image` property, and only 1 has all four | census line, not the tool; see the census rows below | S067.txt@955 (same four-property sentence); S068.txt@6801 `Images are cached based on the URL and won’t be updated unless the URL changes` |
| Exit 1, `og_type_multiple` | Keep exactly one `og:type`; repeated `og:image` is not a finding, so do not generalise the check to every property | re-run the audit (D10 `og_type_multiple og:type`; K2 repeated `og:image` exit 0 clean) | S068.txt@3896 `Each URL should be a single object, so multiple og:type values are not possible.` |
| Exit 1, `og_url_not_absolute` | Rewrite `og:url` as an absolute `http`/`https` URL with a host; a relative value never passes | re-run the audit (D9 `og_url_not_absolute og:url`) | interface `og_url_not_absolute (og:url value is not an absolute http or https URL with a host)`; S067.txt@1303 `og:url - The canonical URL of your object that will be used as its permanent ID` |
| Exit 1, `og_url_not_canonical` | Compare `og:url` with the first `<link rel=canonical href>`, resolved against the page `url`; exact string match after stripping ASCII whitespace, so a scheme-only difference still fails, while a relative canonical that resolves equal passes | re-run the audit (D8 and D12 fail; K3 relative canonical resolved equal exit 0; K4 no canonical link exit 0) | interface `first canonical link wins; exact string comparison after stripping ASCII whitespace`; S068.txt@2626 `og:url The canonical URL for your page. This should be the undecorated URL` |
| Exit 2, `could-not-evaluate` | Fix the input, never the page: `input_invalid` (bad JSON, version other than 1, empty pages, non-http page url, `file` escaping the manifest directory) or `page_unreadable` (not UTF-8). Exit 2 reports input findings only | re-run the audit (I1–I7: 6 `input_invalid`, 1 `page_unreadable`) | interface `exit 2 verdict could-not-evaluate (any input finding; then only input findings are reported, reasons input_invalid or page_unreadable)` |
| Exit 64 | Fix the argv (missing `--manifest`, unknown argument); no JSON is produced, so nothing is known about any page | re-run the audit (U1, U2) | interface `exit 64 usage (missing --manifest, unknown argument)` |
| Reading the census line | Read `ds4cc-7fc6aa2f-og-census: pages=102 og:title=87 og:type=87 og:image=1 og:url=87 all-four=1 og-url-equals-canonical=87` as a recount of retained HTML at `7fc6aa2f`; `og:X` counts pages with a `<meta property="og:X">` whose stripped content is non-empty; the canonical side is resolved against `https://ds4cc.com/<path>` with a trailing `index.html` removed, which is the census's own base, not the manifest's page URL | `python3 -B .ufo/waves/round-34/c2_source_census.py --root <repo> --revision <commit>` (met 0/5 at `d08d8de`, census block still derived: `verification/c2-at-d08d8de.json` `census.derived`) | c2_source_census.py docstring condition (e): `og:X = pages with a <meta property="og:X"> whose content is non-empty after stripping ASCII whitespace` |
| Quoting those numbers as a preview verdict | Do not: the census says what the retained bytes contain, not what any crawler fetches or renders, and it covers only the four properties, only `.html`, only that commit | restate the commit and the dated-measurement status beside the number | S069.txt@685 `we are looking for oEmbed and Twitter Card / Open Graph tags`; S070.txt@3020 `Represents a rich preview card that is generated using OpenGraph tags from a URL` |
| A card looked wrong live, or a fixed page still previews the old title/image | Prepare the source change and the exact URL, then ask the operator: a re-scrape is a live request to an owned property, and image caches key on the image URL, not the page | operator action (Sharing Debugger); do not fire from a seat | S068.txt@4546 `The debugger also triggers a scrape of your page`; S069.txt@974 `Responses to these requests are cached globally across the service for around 30 minutes` |
| Someone wants to widen the source set to X or GitHub card docs | Do not: S071 is a generic developer-docs index with no card markup URL, and S072 documents a repository Settings image upload, not page-level Open Graph tags. Keep S067–S070 | read the retained text, not the intended target | S071.txt@0 `X Developer Platform - X Documentation Index`; S072.txt@0 `Customizing your repository's social media preview` |

## Per-row grounding, condensed

1 manifest v1 — interface; 2 constant gates — counter docstring; 3 four required/name= —
S067@955 + interface; 4 og:image floor — S067@955 + S068@6801 (101/102 arithmetically from
census `og:image=1` of `pages=102`); 5 single object — S068@3896; 6 absolute — interface +
S067@1303; 7 canonical compare — interface + S068@2626; 8 exit 2 — interface; 9 exit 64 —
interface; 10 census definition — c2 docstring (e) + `census.derived`; 11 census limit —
S069@685 + S070@3020; 12 re-scrape gate — S068@4546 + S069@974; 13 rejected sources —
S071@0 + S072@0.

## Commands run and observed output

- `python3 -c "…json.load('.ufo/waves/round-34/c1-matrix.json')['interface']"` — exit 0:
  six interface clauses quoted above; `cases` = 28, exits `{0:6, 1:13, 2:7, 64:2}`, reasons
  `og_required_missing` ×12 (title 3, type 3, image 4, url 2), `og_url_not_canonical` ×2,
  `og_url_not_absolute` ×1, `og_type_multiple` ×1, `input_invalid` ×6, `page_unreadable` ×1.
- same file, `invocation` — exit 0: `python3 -B scripts/link_preview_audit.py --manifest
  <dir>/manifest.json   (cases with argv run that argv instead; cwd is the case directory)`.
- `python3 -c "…c2-at-*.json['census']['derived']"` — exit 0:
  `{'pages': 102, 'og:title': 87, 'og:type': 87, 'og:image': 1, 'og:url': 87,
  'all-four': 1, 'og-url-equals-canonical': 87}`; both c2 receipts `met: 0`.
- `git cat-file -e a2fe31b2:{scripts/link_preview_audit.py,corpus/knowledge/link-preview-metadata.md,corpus/lessons/round-34.md}`
  — exit 1 for all three: absent at lane head, so every "run the tool" row is a forward
  instruction, not a demonstrated run.
- phrase locator (`str.find` over the retained `.txt` files) — exit 0: offsets reported in
  the table; `S0xx.txt` are one line each, so a citation is `S067.txt:1` plus the byte offset.
- `sed -n '944,949p' SKILL.md` — exit 0: confirms the insertion point before line 948.

## Limits

- I did not run `c1_matrix_count.py`, `c2_source_census.py`, or the not-yet-written tool; the
  tallies above are read from retained receipts and matrix text.
- No live request was made; the Sharing Debugger row is a gate description, not an attempt.
- Offsets are byte offsets into UTF-8 text and shift if a source is re-fetched; the sha256
  pin in `receipts.json` is the authority, not the offset.
- Phrase word count and table width follow the round-33 shape; the L1 may trim, but rows 3–7
  and 10–12 are the operability core and row 10 is the one the tool must not be read as
  exceeding.
