## Verdict

RFC 9110's grammar accepts `TEXT/HTML ; charset=utf-8` and `text/html;`. A leading space is not part of the `media-type` grammar: it is removed when it is HTTP field-line OWS, before the field value is evaluated. `text/html, text/plain` is not a valid `Content-Type` media type; Content-Type is a singleton, not a list. The round-23 `served()` helper recognizes the first three samples as HTML, but treats the comma-combined malformed value as merely not served; its call on a non-string content type raises an exception. These are source-level/helper observations, not a full replay run.

## Findings

### P2 — C2 / operability: Content-Type recognition is not full media-type validation

- **RFC source:** RFC 9110, §§5.5, 5.6.2, 5.6.6, 8.3, and 8.3.1. Source identity and located quotes are recorded below.
- **Exact inspection:** read `.ufo/waves/round-23/measure_c2.py:36-39` and `:71-78`; evaluated only the AST-extracted `served` function from that file, with HTTP status 200, `error=None`, and `truncated=False` for each string.
- **Exact observed output:**
  ```text
  'TEXT/HTML ; charset=utf-8' => served=True
  'text/html;' => served=True
  ' text/html' => served=True
  'text/html, text/plain' => served=False
  17 => AttributeError: 'int' object has no attribute 'split'
  ```
- **Impacted claim/axis:** C2 / operability.
- **Finding:** the source uses `ctype.split(";")[0].strip().lower() == "text/html"`; the caller sends every `False` result through its `not-served` path. Thus the helper does not distinguish an invalid comma-combined singleton value from a valid non-HTML type. From the caller's code, a matching `not-served` receipt and absent page could pass that branch even with a 200 response and malformed comma-combined `contentType` (**inference from source; I did not run a full synthetic receipt replay**). A non-string truthy `contentType` raises `AttributeError` instead of yielding a replay rejection.
- **Smallest fix:** check that `contentType` is a string and validate the entire value against the Content-Type media-type grammar before classifying it as served or not served; treat parse failure as a receipt problem, not as an ordinary non-HTML response.

### Parse decisions for the four requested values

| Input | RFC 9110 parse judgment | Notes |
|---|---|---|
| `TEXT/HTML ; charset=utf-8` | **Valid media type.** | Type/subtype are case-insensitive. OWS is permitted before the parameter semicolon; the `charset` parameter name is case-insensitive. |
| `text/html;` | **Valid under the written ABNF.** | The `parameters` repetition permits a semicolon with its `[ parameter ]` omitted. It contributes no parameter. Do not use this as a malformed-receipt case. |
| ` text/html` | **Invalid if matched literally as a `media-type`; valid after HTTP field-line OWS extraction.** | RFC 9110 §5.5 says field values exclude leading/trailing whitespace and a parser MUST exclude allowed such whitespace before evaluation. HTTP/1.1's RFC 9112 §5.1 confirms field-line OWS is stripped during extraction. A stored, already-extracted field value should therefore be `text/html`, not a value whose first character is SP. |
| `text/html, text/plain` | **Invalid as a Content-Type value.** | The media-type production has no list/comma alternative. Content-Type is a singleton; RFC 9110 warns that incorrectly combined duplicate values create apparent lists and that “last valid member” handling can cause interoperability and security problems. Treat the whole value as malformed rather than selecting a member. |

### RFC 9110 source, access, and located quotes

- **URL:** <https://www.rfc-editor.org/rfc/rfc9110.txt>
- **Access:** GET returned HTTP 200 at `2026-10-21T11:45:19Z`; effective URL was the URL above.
- **Bytes:** 502,941 downloaded bytes.
- **SHA-256:** `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`
- **Exact retrieval output:** `http_code=200 effective_url=https://www.rfc-editor.org/rfc/rfc9110.txt size_download=502941 content_type=text/plain;charset=utf-8`; `sha256sum` output: `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a  /tmp/kake-r24-SourceRFC9110MediaType-Lkjf/rfc9110.txt`.
- **Document identity:** the fetched text identifies RFC 9110 as STD 97, Standards Track, June 2022; RFC Editor info page identifies it as an Internet Standard.
- The following are exact excerpts from the fetched text; each excerpt is no more than 25 words. Line numbers refer to the downloaded RFC text.

| Location | Quote |
|---|---|
| §8.3, lines 2930–2932 | “The "Content-Type" header field indicates the media type of the associated representation” |
| §8.3.1, line 2980 | `media-type = type "/" subtype parameters` |
| §8.3.1, lines 2981–2984 | `type = token` / `subtype = token` / “The type and subtype tokens are case-insensitive.” |
| §8.3.1, lines 2986–2988 | “The type/subtype MAY be followed by semicolon-delimited parameters (Section 5.6.6) in the form of name/value pairs.” |
| §5.6.2, lines 1730–1733 | “Tokens are short textual identifiers that do not include whitespace or delimiters.”; `token = 1*tchar` |
| §5.6.6, lines 1818–1821 | `parameters = *( OWS ";" OWS [ parameter ] )`<br>`parameter = parameter-name "=" parameter-value`<br>`parameter-name = token`<br>`parameter-value = ( token / quoted-string )` |
| §5.6.6, lines 1823–1825 | “Parameter names are case-insensitive. Parameter values might or might not be case-sensitive, depending on the semantics of the parameter name.” |
| §5.5, lines 1591–1594 | “A field value does not include leading or trailing whitespace.” / “a field parsing implementation MUST exclude such whitespace prior to evaluating the field value.” |
| §8.3, lines 2964–2970 | “Although Content-Type is defined as a singleton field, it is sometimes incorrectly generated multiple times” / “resulting in a combined field value that appears to be a list.” |
| §8.3.1, lines 2995–2996 | “the "charset" parameter value is defined as being case-insensitive in [RFC2046], Section 4.1.2” |

- **Supplemental field-line context:** <https://www.rfc-editor.org/rfc/rfc9112.txt>, §5.1, lines 722–729, says field-line OWS before/after the field value is excluded by parsers extracting the field line value. This supports the distinction above; the requested media-type and field-value rules are from RFC 9110.

## Checked and held

- Read-only GET of the RFC text and RFC Editor info/errata pages; no target/source tree was changed by the investigation.
- The narrow probe ran the AST-extracted round-23 `served()` helper only. It did **not** run `measure_c2.py` or mutate a receipt.
- No tool was installed or updated.
- Report written only to `.ufo/waves/round-24/w1/SourceRFC9110MediaType.md`.

## Limits

- The exact helper outcomes are observed; the consequence for a synthetic full receipt is explicitly an inference from the caller branch, not a replay result.
- The RFC conclusions are syntactic. They do not authenticate a receipt's originating network observation or prescribe a complete application policy for malformed Content-Type values.