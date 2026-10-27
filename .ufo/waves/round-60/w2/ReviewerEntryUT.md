# ReviewerEntryUT

ATTACKS: Sentence-level source fidelity and quote compliance for `corpus/knowledge/google-user-triggered-fetchers.md` at B1 (`8b33fd248d126b48d838af5c38bc175850f41a09`), against retained S428.

SENTENCES:

| Sentence / location | Verdict | Span / evidence |
|---|---|---|
| Lines 8–13: title, printed revision, nine sections and robots sentence's intro position | Supported | HTML title line 51; `<h1>`/intro and nine `<h2>`s in article. Footer update at HTML 1461. |
| Quote line 17 and example line 21 | Supported | S428 article lines 1082–1085. Both quoted spans are verbatim and 6–25 tokens; example phrase is a substring of the paragraph text node. |
| Lines 23–26: RSS continuation and technical properties/range pointers | Supported, explicitly lane's reading for split link sentence | Article lines 1085–1089; page mentions both properties and range objects. |
| Quote line 30; lines 32–34: generally, no named exception, full robots discussion is intro-only | Supported | S428 lines 1086–1087 and per-fetcher section scan; quote is 10 tokens, page-unique. No exception is specified. |
| Lines 38–43: three range object names | Supported | S428 lines 1092–1096. Quote line 40 (10 tokens) ends at “in the”; filenames are properly rendered as backticks, not quotes. |
| Quote line 47 and hostname mapping lines 49–50 | Supported | S428 lines 1097–1099; quote is page-unique and within token/character bounds. Mapping uses “or … respectively,” matching listed ordering. |
| Quote line 53 and Google-Agent range object | Supported | S428 article Google-Agent entry; quote is 22 tokens and under 160 characters. |
| Lines 55–59: both supplied identifiers are address-based; UA is not an identifier; caution aside says it can be spoofed | Partly unsupported / over-inference | Source supports IP ranges, reverse DNS masks and the caution that UA can be spoofed (HTML 1107–1109). It does not say those are the only identifiers or state that UA is not an identifier. The “does not make … an identifier” assertion is not marked as the lane's reading, unlike the aside statement. |
| Lines 63–76: dated comparison with verification page, and wording differences | Not established by S428 alone; correctly attributes earlier-page wording to a separate file and explicitly declines to decide governing wording | S428 supports the newer phrase and date; comparison's prior quote is out of S428's scope. This is a cross-source claim, not an S428-supported sentence. The parenthetical correctly explains why that text is in backticks. |
| Lines 80–83: no exception set and no per-fetcher robots clause | Supported | Article intro lines 1086–1087 and nine subsequent sections. |
| Lines 84–85: page links to verification page and Web Bot Auth, but omits verification procedure | Supported | S428 links to verification page (1109) and Web Bot Auth (1247–1249); no reverse-DNS-then-forward-DNS test is spelled out in this article. |
| Lines 86–87: no claim verification page is wrong/retracted; divergence is dated and attributed | Supported as a description of this entry's treatment, not a claim made by S428 | Entry's own text and cited two-page comparison. |
| Lines 88–92: non-exhaustive statement | Supported | Article lines 1103–1105; quote line 90 is 9 tokens, page-unique. |
| Line 93: nothing about other vendors | Supported as a bounded statement about this page; not a claim about the world | S428 describes Google fetchers only. |

FINDINGS:

| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| medium | `corpus/knowledge/google-user-triggered-fetchers.md:55-56` | “it does not make the user-agent string an identifier” overstates the source: listing address-based indicators does not establish their exclusivity or rule out UA as an identifier. Mark as explicit lane inference/qualify to “the page identifies these fetchers here by…” | `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 8b33fd248d126b48d838af5c38bc175850f41a09:corpus/knowledge/google-user-triggered-fetchers.md`; `grep` evidence: S428 article 1092–1099 and caution 1107–1109 | Qualify the claim to the page's described methods and avoid asserting exclusivity. |
| ~~low~~ | `corpus/knowledge/google-user-triggered-fetchers.md:84-85` | No finding: both links are present in S428 and the page itself does not spell out the test. | `grep -nE 'verify-google-requests|Web Bot Auth' /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-60/sources/S428.html` -> verification link 1109; Web Bot Auth links 1247–1249 | None. |

Quote rule check: each displayed double-quoted passage is verbatim from S428 article text, within the 6–25 whitespace-token and 160-character limits, and page-unique to the extent checked against the cited article passages. No credentials or private URLs included.

VERDICT: One medium unsupported identification inference remains; other reviewed assertions and quoted spans are supported.
