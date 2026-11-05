# Round 92 — RFC 9111 §4.2.2 source open (ScoutSources)

Opened this round by ScoutSources (CORPUS.md rule 1). Lane root: `kake-shokunin`.
Receipts beside this file: `rfc9111-fetched.txt`, `errata9111.html`, `datatracker9111.html`.

## 1. Receipt table

| # | URL | HTTP | bytes | sha256 | UTC access (observed) |
|---|---|---|---|---|---|
| R1 | https://www.rfc-editor.org/rfc/rfc9111.txt | 200 | 84477 | aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e | 2026-11-05T00:30:13Z |
| R2 | https://www.rfc-editor.org/errata/rfc9111 (no redirect follow) | 302 | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty body) | 2026-11-05T00:30:21Z |
| R2b | redirect target of R2: https://errata.rfc-editor.org/search/?rfc_number=9111&presentation=records (followed with `curl -L`, 3 redirects) | 200 | 40383 | 1df394f9c04e33e74bf69360e3b7d3bbdeccbe80e27caaa18fdace216ccb54a4 | 2026-11-05T00:30:27Z |
| R3 | https://datatracker.ietf.org/doc/rfc9111/ | 200 | 120322 | 8340f51a9856a9a58fb2feec11e0afb108a97914a6c370ed993eb92d9b126132 | 2026-11-05T00:30:31Z |

- The UTC access times are what the host clock reported. They fall on 2026-11-05 UTC, which is
  2026-11-04 local evening (UTC−03:00). The round is dated 2026-11-04; the date is recorded as observed.
- R2 was fetched twice: once without redirect-following (302, empty body), then with `-L` to the
  redirect target R2b, a host the seat item did not name. Disclosed as a deviation from "once each".
- Receipts in this directory: `rfc9111-fetched.txt` (= R1 body), `errata9111.html` (= R2b body),
  `datatracker9111.html` (= R3 body). The 302 body was empty and is not kept.

### Byte-for-byte comparison with the frozen copy

`cmp .ufo/waves/round-92/L1/src/rfc9111.txt .ufo/waves/round-92/w1/ScoutSources/rfc9111-fetched.txt`
→ no output, exit 0. **Identical.** Both sha256 = `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`.

## 2. Quotes (plain-text line numbers of `rfc9111-fetched.txt`; each verified as a raw substring of the cited lines joined by one space)

Line numbers are the line numbers of the fetched body, not RFC section page numbers.

**(a) Permission to assign a heuristic expiration time — lines 689–690 (15 words)**
> a cache MAY assign a heuristic expiration time when an explicit time is not specified

**(b) Prohibition when an explicit expiration time is present — lines 695–696 (20 words)**
> A cache MUST NOT use heuristics to determine freshness when an explicit expiration time is present in the stored response.

**(c) Which responses may use heuristics — two quotes, split to stay within 25 words**

- (c1) lines 697–699 (18 words):
  > heuristics can only be used on responses without explicit freshness whose status codes are defined as "heuristically cacheable"
- (c2) lines 700–701 (18 words):
  > on responses without explicit freshness that have been marked as explicitly cacheable (e.g., with a public response directive).

The status-code set itself is not in §4.2.2; §4.2.2 cites "Section 15.1 of [HTTP]". See §4 below.

**(d) Fraction of the interval since Last-Modified, and the 10 % figure — lines 707–708 (22 words) and 709 (9 words)**
> caches are encouraged to use a heuristic expiration value that is no more than some fraction of the interval since that time.

> A typical setting of this fraction might be 10%.

## 3. Errata and obsoletion (checked once each; see R2/R2b and R3)

- **Errata (R2b).** Four records exist for RFC 9111. None names §4.2.x:

  | Errata-ID | Status | Section cited | Touches §4.2.2? |
  |---|---|---|---|
  | 9004 | Reported | 3.5 | No |
  | 9185 | Reported | 4.3.4 | No |
  | 9166 | Held for Document Update | 5.2.3 | No |
  | 7695 | Rejected | 4.3.2 | No |

  Adjacent, not touching §4.2.2: 9004 (§3.5, shared-cache authorization) and 9166 (§5.2.3, extension directives) sit beside the Section 3 requirements that §4.2.2 cites ("Because of the requirements in Section 3"). Both are unverified or held; neither changes normative text in force.
- **Obsoletion (R3).** The page states "This document obsoletes RFC 7234" and carries status "Internet Standard (June 2022)". The page text contains no "Obsoleted by" or "Updated by" relationship field. This is a text search of the saved HTML (`grep -ci` for those strings), not a rendered-view check; the only "updated by" text found is inside the document body (§4.3.3).

**Conclusion on §4.2.2:** no erratum or obsoletion touches §4.2.2 as of the access times above.

## 4. Which contract conventions the RFC text supports

The contract (`c2-contract.md`, clause 12) names two lane conventions: the 10 % fraction and the 86400-second cap.

- **10 % fraction — supported as an example, not as a rule.** Quote (d2), line 709: "A typical setting of this fraction might be 10%." The RFC gives 10 % as a *typical* value, hedged with "might". The contract's labelling it a lane convention is accurate.
- **86400-second cap — not supported by the RFC text.** The RFC names no cap value. Searches of `rfc9111-fetched.txt`:
  - `grep -c 86400` → `0`
  - `grep -ciE "24 hours|one day"` → `0`
  - The only constraint language is lines 692–693: "This specification does not provide specific algorithms, but it does impose worst-case constraints on their results." The constraints are not quantified.
  The cap is correctly labelled as a lane convention in the contract.

**Items the contract does not label as conventions but the RFC does not settle:**

1. **Upper endpoint of the interval (clause 12, `Date - Last-Modified`).** The RFC says "the interval since that time" (line 708) and does not name the upper endpoint (response Date, generation time, or current time). The contract uses `Date`. That is an unlabelled choice. The contract's sentence "Everything else is a direct reading of the section" overstates.
2. **Last-Modified absent or after Date → `heuristic-undecided` (clause 13).** The RFC permits heuristics "employing algorithms that use other field values" (lines 690–691) without Last-Modified, and says nothing about a Last-Modified later than Date. The undecided outcome is a lane choice, unlabelled.
3. **Status-code set (clause 11).** The 12-code set `{200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501}` matches the list in RFC 9110 §15.1 in the lane's retained copy `.ufo/waves/round-81/w1/ScoutSources/rfc9110.txt` (12 "is heuristically cacheable" sentences, lines 6953–7876). This was **not** re-fetched this round; it is a lane-retained copy, cited as such.
4. **`now` input (clause 3 and the input schema).** The contract requires `now` to be a non-negative int, and the frozen counter validates it (`c92_heuristic.py` line 137–139). No decision clause (9–13) reads `now`; the reference decision (`c92_heuristic.py` line 186) computes from `Date` and `Last-Modified` only. The input is validated and unused — a contract defect for the round's routed list.

## 5. Limits

- Only the RFC 9111 body was fetched and quoted this round. RFC 9110 §15.1 was not fetched; the status set rests on the retained copy named in §4, item 3.
- The datatracker and errata checks were text searches of saved HTML. No rendered view was inspected.
- Line numbers refer to the plain-text body `rfc9111-fetched.txt` (sha256 `aeb52adb…cf3e`), not to RFC section page numbers.
