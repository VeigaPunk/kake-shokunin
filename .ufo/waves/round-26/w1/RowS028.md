# Row S028 — freshness recheck (round 26)

```json
{"id":"S028","verdict":"HOLD","fetchIndex":1,"quote":"with an empty host identifier. A recipient that processes such a URI reference MUST reject it as invalid","anchorObserved":"§4.2.1 http URI Scheme body, raw-text lines 1106-1108 (text view line 1); identical sentence repeats in §4.2.2 https URI Scheme at raw lines 1135-1137","reason":"Raw bytes re-fetched 2026-10-21T15:10:49Z (status 200, 502941 bytes) hash to sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a, exactly the row's pinned 21c1cdce…7232a, so the immutable June 2022 STD 97 text is unchanged. Sections 4.2.1 and 4.2.2 still hold sender MUST NOT and recipient MUST reject for an empty host identifier, and S010 remains scoped to §8.8 validators, so scope and anchor stand.","correction":null}
```

## Caveats

- Byte test is decisive: RFC 9110 plain text is frozen; the pinned digest match means no content drift is possible, only availability was re-tested.
- Only one fetch index exists for this row; status 200, final URL identical to the row URL, no redirect or error in manifest.json.
- Quote is scheme-neutral and occurs exactly twice in the text view (once at each anchor section), covering both http and https as the teaches states.
- Section headings are present twice in raw text (TOC lines 97-98, body lines 1090/1113); body occurrences used as anchor.
- Used-by statements still agree: knowledge line 83-84 renders the same reject requirement, lessons/round-22 line 183 quotes the identical sentence.
- No tools installed or upgraded; no network access beyond reading the retained fetch.
