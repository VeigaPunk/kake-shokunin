Axes: citation fidelity, fetch reproducibility, sentence-to-spec fit (10, 11, 14).

Checked Namespaces in XML 1.0 (Third Edition), https://www.w3.org/TR/xml-names/, against `.ufo/waves/round-39/c1-contract.md` sentences 10, 11 and 14. No tools installed.

Command (exit 0): `curl -sS -L --max-time 60 -o /fast/scratch/hyaku/kake-r39a3w1/ScoutXmlNamespaces/xml-names.html -w 'http_code=%{http_code} url_effective=%{url_effective} size=%{size_download} redirects=%{num_redirects}\n' https://www.w3.org/TR/xml-names/ && sha256sum /fast/scratch/hyaku/kake-r39a3w1/ScoutXmlNamespaces/xml-names.html && wc -c -l /fast/scratch/hyaku/kake-r39a3w1/ScoutXmlNamespaces/xml-names.html`

Observed: HTTP 200, final URL `https://www.w3.org/TR/xml-names/`, 0 redirects, 51390 bytes, 925 lines, sha256 `b4a649e5fdab9852d68eca21442481599164949bcdee5549f2ec7e38fb3cd3a8`. Access 2026-10-23T06:53:09Z (HTTP Date 2026-10-23T06:53:10 GMT). Last-Modified 2018-10-09. Title line 3 and h1 line 34: "Namespaces in XML 1.0 (Third Edition)". This version, lines 37–38: `https://www.w3.org/TR/2009/REC-xml-names-20091208/`. Line 35: W3C Recommendation 8 December 2009. The dated copy and the errata (line 49) were not fetched; the item named only this URL.

Deliverable: `/fast/scratch/hyaku/kake-r39a3w1/ScoutXmlNamespaces/xml-names.html` sha256 `b4a649e5fdab9852d68eca21442481599164949bcdee5549f2ec7e38fb3cd3a8`.

Quotes from that file (each ≤25 words):

- Line 301 (11 words): "The comparison is case-sensitive, and no %-escaping is done or undone."
- Lines 293–299: the two URIs "are treated as strings" and are identical "if and only if the strings are identical, that is, if they are the same sequence of characters."
- Lines 503–504 (13 words): "Note that the prefix functions only as a placeholder for a namespace name."
- Lines 662–663 (13 words): "A default namespace declaration applies to all unprefixed element names within its scope."
- Lines 221–223 (16 words): "For a name N that is not in a namespace, the namespace name has no value."

Findings:

- "whatever prefix binds it" (sentence 10; the same test in sentence 11) follows. An expanded name is the pair (namespace name, local name), lines 206–211. Lines 503–508: applications SHOULD use the namespace name, not the prefix. Lines 625–637: a prefixed name's namespace name is the URI that prefix is bound to, so two prefixes bound to one string are one name (lines 751–755, `n1` and `n2`). Lines 293–301: that string compare is exact and case-sensitive, with no percent-unescaping. The contract's sitemap URI matches only that character sequence.
- A default namespace is not a prefix. Sentence 10's words "whatever prefix" do not name `xmlns=`. Lines 655–678 still put an unprefixed element in the in-scope default namespace. Reading sentence 10 as "that namespace URI, prefix irrelevant, including the default" follows. Reading it as "only a prefixed binding counts" contradicts lines 662–678.
- "any other namespace … ignored" (sentence 14) does not follow. This Recommendation never says to ignore, skip or discard foreign elements. It only makes them a different expanded name. Sentence 14 already cites S102 "Extending the Sitemaps protocol", not this spec. Silence, not a contradiction of "ignored".
- Hole, not a contradiction: lines 221–223 and 677–678, a name in no namespace "has no value". That is not "any other namespace". Sentences 11 and 13 speak only of the sitemap namespace; sentence 14 only of other namespaces. An unprefixed element with no default namespace in scope is outside 11, 13 and 14 (preamble: uncovered inputs are outside the contract).
- Scope (lines 615–618 and 655–659) excludes inner redeclarations, so a descendant can enter or leave the sitemap namespace. Sentence 14's "at any level" matches that shape; the verb "ignored" still does not come from this spec.
- Sentences 10–11 cite S102 and S103; sentence 14 cites S102. The contract does not state case-sensitive namespace-URI comparison. §2.3 supplies it; the contract neither states nor contradicts it.

Draft SOURCES row (not appended; S104 is the last registry row at `corpus/SOURCES.md:112`; S105 is provisional):

| S105 | Namespaces in XML 1.0 (Third Edition) — https://www.w3.org/TR/xml-names/ | spec | A | Expanded-name identity, default-namespace scope, and case-sensitive namespace-name comparison; not a sitemap rule to ignore foreign elements | §2.3 Comparing URI References (lines 283-301), §4 placeholder prefix (lines 503-508), §6.1-6.2 scoping and defaulting (lines 614-678); W3C Recommendation 8 December 2009; fetched 2026-10-23T06:53:09Z, HTTP 200, retained HTML SHA256 b4a649e5fdab9852d68eca21442481599164949bcdee5549f2ec7e38fb3cd3a8 | The prefix is only a placeholder: a name is the namespace-name string plus the local name, compared case-sensitively, and a default namespace covers unprefixed elements | queued | 2026-10-23 | 365d | — |

Verdict: keep the row; it grounds sentences 10 and 11. Do not use it to ground sentence 14's "ignored".
