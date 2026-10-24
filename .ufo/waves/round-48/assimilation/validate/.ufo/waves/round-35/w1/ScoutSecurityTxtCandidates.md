# Round 35 w1 — security.txt candidate screening beyond S078–S085

Seat: KakeR35.ScoutSecurityTxtCandidates (leaf). 2026-10-22T22:25–22:28Z. No sealed-key path
touched; only this file written in the lane. Verdict: 4 screened (1 reject, 3 queue), 2 unopened.
Bodies: `/fast/scratch/hyaku/kake-r35/w1/ScoutSecurityTxtCandidates/sources/` (`*.txt` =
extracted-visible-text line numbers, `*.html` = raw GET body).

| id | source (kind, tier) | access UTC | status | proposal |
|---|---|---|---|---|
| C1 | github.com/securitytxt/security-txt (docs, B) | 22:25:45 | 200 | queue |
| C2 | OWASP Cheat Sheet: Vulnerability Disclosure (community, B) | 22:25:29 | 200 | queue |
| C3 | CISA BOD 20-01 VDP template (docs, C) | 22:25:29 | 200 | **reject** |
| C4 | RFC Editor errata for RFC 9116 (spec, A) | 22:25:29 | 200 | queue |
| C5 | GitHub Docs "adding a security policy" (—) | 22:25:29 | 404 | unopened |
| C6 | https://securitytxt.io/ (—) | 22:25:29 | conn fail | unopened |

## C1 — securitytxt/security-txt repo, branch master, page currentOid ec918fe449db24bffcd28f2002c5162c67be5321
Located `C1b.txt:230-231`: "The definitive reference on security.txt and how it is used can be
found in RFC 9116." (17 words). `C1b.txt:233-234` points extensions to an IANA registry and
`C1b.txt:238-240` names securitytxt.org; the 357-line body never says expires, deploy, Jekyll,
GitHub Pages, or validation.
Queue: corroborates the canonical reference and yields two unopened leads (IANA security.txt
extensions registry; securitytxt/securitytxt.org repo), but lacks publishing or hosting mechanics,
so it cannot support a "served from Pages" claim. First GET
`raw.githubusercontent.com/.../main/README.md` → 404; repo page reports `"defaultBranch":"master"`.

## C2 — OWASP Vulnerability Disclosure Cheat Sheet (B; community is never A)
Located `C2.txt:283-288` (Finding Contact Details): "A security.txt file on the website at
/.well-known/security.txt as per RFC 9116. At minimum include the required Contact and Expires
fields" (21 words); identical sentence repeats under Publishing Contact Details at `C2.txt:401-407`.
Queue: agrees with S078 on well-known location and the two required fields; adds no syntax,
hosting, or Pages detail, and the body carries no last-updated date.

## C3 — CISA VDP Template — REJECT
Located `C3.txt:118`: "Your policy must be published as a public web page in plain text or HTML at
the “/vulnerability-disclosure-policy” path of your agency's primary .gov website." (24 words).
Located absence: 0 occurrences of `security.txt`, `.well-known`, or `9116` in the 292-line body;
the page is a BOD 20-01 policy-content template plus a 35.93 KB DOCX.
Reject reason: it prescribes a different required path on .gov hosts and never names RFC 9116, so
it is evidence for neither side of serving `/.well-known/security.txt` from GitHub Pages.
Flip: a CISA page that names `/.well-known/security.txt` and its publication requirements.

## C4 — RFC 9116 erratum records (A for erratum state only)
`https://www.rfc-editor.org/errata/rfc9116` redirected 302 to
`https://errata.rfc-editor.org/search/?rfc_number=9116&presentation=records`.
- 6946, Verified, Editorial (2022-04-28): the ABNF comment's reference is "mistakenly given in
  ABNF comments as 'Section 3.5.3'" where Section 2.5.3 was meant (`C4.txt:105-109`).
- 7264, Reported, Technical (2022-12-10): "The ISO 8601 zulu indicator MUST be an upper case Z,
  not a lower case one." (18 words, `C4.txt:120-127`). 7743, Reported, Technical (2023-12-30):
  "Both CRLF and LF line separators can be used ... as long as the entire file uses the chosen
  line separator." (22 words, `C4.txt:130-140`).
Queue: authoritative on verified versus merely reported; only 6946 is Verified, so an entry must
not cite 7264/7743 as settled validity rules (S078 §2.2 already governs line separators).
Recheck 180d.

## Unopened
- C5 GitHub Docs security-policy page: 404 "Page not found." at three documented paths under
  `/code-security/security-advisories/…` and `/communities/setting-up-your-project-for-healthy-contributions/…`.
  No absence claimed.
- C6 https://securitytxt.io/: curl exit 7, "Failed to connect … after 232 ms". No body.

## Commands (exit 0 unless noted)
- `curl -sSL --max-time 30 --compressed -A "Mozilla/5.0 (compatible; kake-r35-scout/1.0; research)"
  -o … -w '%{http_code} %{url_effective} %{size_download}'` ×9 requests over 6 candidate URLs
  (3 retries); HTTP 200/404 exit 0, C6 exit 7. GET only; no owned property contacted.
- `python3 - <<EOF` tag-strip extraction — exit 0. `sha256sum` — exit 0:
  C1 `b0bb354a1a4e197aecb84b649787f0fdb0f7b1c6a774d1b5f55e9da57168e786` (292366 B);
  C2 `1351dcee2496031b8a0c3f9d2ea4c12503af53ea123bd466ca6931e1f4301b2b` (101356 B);
  C3 `88c56b86c96830aa81e84be80a94172267d694ded23403c86ae44f93028f28f4` (69054 B);
  C4 `76591a42ee973f4143bf86042d9f30edb6c0905ef0c2f5344bee4f73ccae01bf` (25394 B).

Receipts `/fast/scratch/hyaku/kake-r35/w1/ScoutSecurityTxtCandidates/receipts.json`; bodies
`sources/C1b.html`, `C2.html`, `C3.html`, `C4.html`, `C5c.html`. Tool installs: none.

## Not verified
- C2/C3 publication dates: no machine-readable last-updated date in either body, so freshness
  rests on the 2026-10-22 access alone.
- C1 currentOid is page-reported, not a git-verified head. Whether C5 exists at another GitHub
  Docs path, and C6's content, were not established.
