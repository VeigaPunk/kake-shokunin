# Round-38 C2 real-run: per-check justification lines

Oracle: `expectations.json` (declared from the public round-38 contract text; no sealed
case was read, listed or run). Every quote below was asserted verbatim at its line
against the retained round-37 body by `build_r38_manifest.py`, whose run also re-checked
each retained body's sha256 against the round-37 fetch receipts.

Main manifest: `manifest.json`, 91 checks (55 round-37 checks kept verbatim
plus the 36 below). Declared report: verdict `could-not-evaluate`, checksEvaluated 79, 12 findings (the 12 (i) check faults); exit 2.

Outcome vocabulary: `allow`/`disallow` are access results the tool must find no finding
for (the check's `expect` field says which); `check_invalid` is a check fault the tool
must report as `{"check": <id>, "reason": "check_invalid"}` and must not evaluate.

## www.rfc-editor.org — `robots/www_rfc-editor_org.txt`

- `r38-k-www_rfc-editor_org-pct2e` — `https://www.rfc-editor.org/robots%2Etxt` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L2 `Disallow: /rfc/authors/`; L3 `Disallow: /rfc/rerendered/`; L4 `Disallow: /rfc/v3test/`
  - why: Contract (k): %2E is an unreserved escape of '.', so the path to match normalizes to exactly /robots.txt; a URL whose normalized path is /robots.txt is allowed. The raw path /robots%2Etxt is not /robots.txt, so a raw-path comparison would fall through to these three Disallow rules (none of which matches it) instead of the implicit allow.
- `r38-i-www_rfc-editor_org-space` — `https://www.rfc-editor.org/rfc/rfc 9309.html` — user-agent `Googlebot` — declared **check_invalid**
  - deciding line(s): L2 `Disallow: /rfc/authors/`; L3 `Disallow: /rfc/rerendered/`; L4 `Disallow: /rfc/v3test/`
  - why: Contract (i): the space (U+0020) is ASCII outside the RFC 3986 character set, so the check is a check fault (check_invalid) and no access result is evaluated. Were it admitted, the path would be outside the three disallowed subtrees; the space cannot make any of them a prefix.
- `r38-e-www_rfc-editor_org-authors` — `https://www.rfc-editor.org/rfc/%61uthors/team` — user-agent `Googlebot` — declared **disallow**
  - deciding line(s): L2 `Disallow: /rfc/authors/`
  - why: Contract (e): %61 is an unreserved escape of 'a' and is decoded before matching, so the path to match is /rfc/authors/team, which begins with the disallowed /rfc/authors/ subtree.

## developers.google.com — `robots/developers_google_com.txt`

- `r38-k-developers_google_com-pct72` — `https://developers.google.com/%72obots.txt` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L2 `Disallow: /youtube/partner/`
  - why: Contract (k): %72 is an unreserved escape of 'r' and decodes, so the path to match is exactly /robots.txt and the URL is allowed. The file's only rule covers /youtube/partner/, so no rule matches either the raw path or the normalized one; (k) makes the allow independent of that.
- `r38-i-developers_google_com-quote` — `https://developers.google.com/search/docs/robots"txt` — user-agent `Googlebot` — declared **check_invalid**
  - deciding line(s): L2 `Disallow: /youtube/partner/`
  - why: Contract (i): the double quote is ASCII outside the RFC 3986 character set, so the check is a check fault (check_invalid); no allow or disallow is evaluated. The path is outside the only disallowed subtree either way.
- `r38-e-developers_google_com-partner` — `https://developers.google.com/youtube/%70artner/docs` — user-agent `Googlebot` — declared **disallow**
  - deciding line(s): L2 `Disallow: /youtube/partner/`
  - why: Contract (e): %70 is an unreserved escape of 'p', decoded before matching, so the path is /youtube/partner/docs and begins with the disallowed partner subtree.

## github.com — `robots/github_com.txt`

- `r38-k-github_com-pct2e` — `https://github.com/robots%2Etxt` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L360 `User-agent: *`
  - why: Contract (k): %2E decodes to '.', so the path to match is exactly /robots.txt and the URL is allowed. No Googlebot group exists, so the * group's 165 rules decide the raw path /robots%2Etxt; none of them matches /robots.txt (the closest shapes are anchored records such as Disallow: /search$), so the allow holds either way and (k) states it on the normalized path.
- `r38-i-github_com-caret` — `https://github.com/veigapunk^kake` — user-agent `Googlebot` — declared **check_invalid**
  - deciding line(s): L360 `User-agent: *`
  - why: Contract (i): '^' is ASCII outside the RFC 3986 character set, so the check is a check fault (check_invalid); no access result is evaluated. The path /veigapunk^kake matches none of the * group's rules.
- `r38-e-github_com-gist` — `https://github.com/gist/veigapunk/%61bc` — user-agent `Googlebot` — declared **disallow**
  - deciding line(s): L360 `User-agent: *`; L370 `Disallow: /gist/`
  - why: Contract (e): %61 is an unreserved escape of 'a', decoded before matching, so the path is /gist/veigapunk/abc, which begins with the disallowed /gist/ subtree.

## docs.github.com — `robots/docs_github_com.txt`

- `r38-k-docs_github_com-pct2e` — `https://docs.github.com/robots%2Etxt` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L1 `User-agent: *`
  - why: Contract (k): %2E decodes to '.', so the path to match is exactly /robots.txt and the URL is allowed. The 13-byte file holds one user-agent record and no rule record, so the raw path is unrestricted as well; (k) fixes the allow on the normalized path.
- `r38-i-docs_github_com-backslash` — `https://docs.github.com/en\pages` — user-agent `Googlebot` — declared **check_invalid**
  - deciding line(s): L1 `User-agent: *`
  - why: Contract (i): the backslash is ASCII outside the RFC 3986 character set, so the check is a check fault (check_invalid); no access result is evaluated. The file declares no rule record.
- `r38-e-docs_github_com-escslash` — `https://docs.github.com/en/pages%2Findex` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L1 `User-agent: *`
  - why: Contract (e): %2F is a reserved escape and is kept as %2F (uppercased), not decoded to '/', so the path is /en/pages%2Findex; the file holds no Allow or Disallow record, so it is allowed.

## ds4cc.com — `robots/ds4cc_com.txt`

- `r38-k-ds4cc_com-pct72` — `https://ds4cc.com/%72obots.txt` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L2 `Allow: /`
  - why: Contract (k): %72 decodes to 'r', so the path to match is exactly /robots.txt and the URL is allowed. The group's Allow: / would allow it in any case; (k) makes the allow independent of the rule.
- `r38-i-ds4cc_com-braceopen` — `https://ds4cc.com/posts/{2026` — user-agent `Googlebot` — declared **check_invalid**
  - deciding line(s): L2 `Allow: /`
  - why: Contract (i): '{' is ASCII outside the RFC 3986 character set, so the check is a check fault (check_invalid); no access result is evaluated. The Allow: / prefix would otherwise allow it.
- `r38-e-ds4cc_com-index` — `https://ds4cc.com/index%2Ehtml` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L2 `Allow: /`
  - why: Contract (e): %2E decodes to '.', so the path is /index.html; the group's Allow: / is a prefix rule covering every path on the host.

## en.wikipedia.org — `robots/en_wikipedia_org.txt`

- `r38-k-en_wikipedia_org-pct2e` — `https://en.wikipedia.org/robots%2Etxt` — user-agent `UbiCrawler` — declared **allow**
  - deciding line(s): L27 `User-agent: UbiCrawler`; L28 `Disallow: /`
  - why: Contract (k): UbiCrawler has its own group whose only rule is Disallow: /. The raw path /robots%2Etxt is not /robots.txt, so comparing before normalization applies that rule and disallows; %2E is an unreserved escape of '.', so the path to match normalizes to exactly /robots.txt and the URL is allowed.
- `r38-k-en_wikipedia_org-pct72` — `https://en.wikipedia.org/%72obots.txt` — user-agent `UbiCrawler` — declared **allow**
  - deciding line(s): L27 `User-agent: UbiCrawler`; L28 `Disallow: /`
  - why: Contract (k): %72 is an unreserved escape of 'r'; the path to match normalizes to exactly /robots.txt, which is allowed, while the raw path /%72obots.txt would be caught by the group's Disallow: /.
- `r38-i-en_wikipedia_org-pipe` — `https://en.wikipedia.org/wiki/A|B` — user-agent `Googlebot` — declared **check_invalid**
  - deciding line(s): L148 `User-agent: *`; L156 `Disallow: /wiki/Special:`
  - why: Contract (i): '|' is ASCII outside the RFC 3986 character set, so the check is a check fault (check_invalid); no access result is evaluated. No Googlebot group exists, the * group decides, and /wiki/A|B matches no rule of it (e.g. the Special: prefix does not apply).

## html.spec.whatwg.org — `robots/html_spec_whatwg_org.txt`

- `r38-k-html_spec_whatwg_org-pct2e` — `https://html.spec.whatwg.org/robots%2Etxt` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L2 `Disallow: /commit-snapshots/`; L3 `Disallow: /review-drafts/`
  - why: Contract (k): %2E decodes to '.', so the path to match is exactly /robots.txt and the URL is allowed. The two disallowed working-draft trees do not cover it either way; (k) fixes the allow on the normalized path.
- `r38-i-html_spec_whatwg_org-backtick` — `https://html.spec.whatwg.org/x`y` — user-agent `Googlebot` — declared **check_invalid**
  - deciding line(s): L2 `Disallow: /commit-snapshots/`; L3 `Disallow: /review-drafts/`
  - why: Contract (i): the backtick is ASCII outside the RFC 3986 character set, so the check is a check fault (check_invalid); no access result is evaluated. Neither disallowed tree covers the path.
- `r38-e-html_spec_whatwg_org-commit` — `https://html.spec.whatwg.org/commit-snapshots%2F1234` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L2 `Disallow: /commit-snapshots/`
  - why: Contract (e): %2F is a reserved escape and is kept, so the path is /commit-snapshots%2F1234, which does not begin with /commit-snapshots/ (the character after the name is '%', not '/'); the rule is a prefix rule and does not match.

## pages.github.com — `robots/pages_github_com.txt`

- `r38-k-pages_github_com-pct2e` — `https://pages.github.com/robots%2Etxt` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L1 `Sitemap: https://pages.github.com/sitemap.xml`
  - why: Contract (k): %2E decodes to '.', so the path to match is exactly /robots.txt and the URL is allowed. The only record is a Sitemap record, which opens no group, so the raw path is unrestricted as well.
- `r38-i-pages_github_com-braceclose` — `https://pages.github.com/a}b` — user-agent `Googlebot` — declared **check_invalid**
  - deciding line(s): L1 `Sitemap: https://pages.github.com/sitemap.xml`
  - why: Contract (i): '}' is ASCII outside the RFC 3986 character set, so the check is a check fault (check_invalid); no access result is evaluated. No group exists in the file.
- `r38-e-pages_github_com-project` — `https://pages.github.com/project%2Fpage` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L1 `Sitemap: https://pages.github.com/sitemap.xml`
  - why: Contract (e): %2F is a reserved escape and is kept as %2F, so the path is /project%2Fpage; the file holds no user-agent record, hence no rule, so the URL is allowed.

## veigapunk.github.io — `robots/veigapunk_github_io.txt`

- `r38-k-veigapunk_github_io-pct72` — `https://veigapunk.github.io/%72obots.txt` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L2 `Allow: /`
  - why: Contract (k): %72 decodes to 'r', so the path to match is exactly /robots.txt and the URL is allowed. The group's Allow: / covers it in any case; (k) fixes the allow on the normalized path.
- `r38-i-veigapunk_github_io-gt` — `https://veigapunk.github.io/a>b` — user-agent `Googlebot` — declared **check_invalid**
  - deciding line(s): L2 `Allow: /`
  - why: Contract (i): '>' is ASCII outside the RFC 3986 character set, so the check is a check fault (check_invalid); no access result is evaluated. Allow: / would otherwise allow it.
- `r38-e-veigapunk_github_io-index` — `https://veigapunk.github.io/index%2Ehtml` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L2 `Allow: /`
  - why: Contract (e): %2E decodes to '.', so the path is /index.html and the group's Allow: / prefix rule covers it.

## www.robotstxt.org — `robots/www_robotstxt_org.txt`

- `r38-k-www_robotstxt_org-pct2e` — `https://www.robotstxt.org/robots%2Etxt` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L2 `Disallow:`
  - why: Contract (k): %2E decodes to '.', so the path to match is exactly /robots.txt and the URL is allowed. The group's only rule has an empty value, which never matches, so the raw path is unrestricted as well.
- `r38-i-www_robotstxt_org-lt` — `https://www.robotstxt.org/a<b` — user-agent `Googlebot` — declared **check_invalid**
  - deciding line(s): L2 `Disallow:`
  - why: Contract (i): '<' is ASCII outside the RFC 3986 character set, so the check is a check fault (check_invalid); no access result is evaluated.
- `r38-e-www_robotstxt_org-tilde` — `https://www.robotstxt.org/%7Euser/page` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L2 `Disallow:`
  - why: Contract (e): %7E is an unreserved escape of '~' and is decoded, so the path is /~user/page; the group's only rule has an empty value, which never matches, so the URL is allowed.

## www.sitemaps.org — `robots/www_sitemaps_org.txt`

- `r38-k-www_sitemaps_org-pct72` — `https://www.sitemaps.org/%72obots.txt` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L1 `Sitemap: https://www.sitemaps.org/sitemap.xml`
  - why: Contract (k): %72 decodes to 'r', so the path to match is exactly /robots.txt and the URL is allowed. The only record is a Sitemap record, which opens no group.
- `r38-i-www_sitemaps_org-ctl` — `https://www.sitemaps.org/protocol.html` — user-agent `Googlebot` — declared **check_invalid**
  - deciding line(s): L1 `Sitemap: https://www.sitemaps.org/sitemap.xml`
  - why: Contract (i): U+0001 is a control character, ASCII outside the RFC 3986 character set, so the check is a check fault (check_invalid); no access result is evaluated.
- `r38-e-www_sitemaps_org-xml` — `https://www.sitemaps.org/sitemap%2Exml` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L1 `Sitemap: https://www.sitemaps.org/sitemap.xml`
  - why: Contract (e): %2E decodes to '.', so the path is /sitemap.xml; the file holds no rule record, so the URL is allowed.

## developer.mozilla.org — `robots/developer_mozilla_org.txt`

- `r38-k-developer_mozilla_org-pct2e` — `https://developer.mozilla.org/robots%2Etxt` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L4 `Disallow: /api/`; L5 `Disallow: /*/files/`; L6 `Disallow: /media`
  - why: Contract (k): %2E decodes to '.', so the path to match is exactly /robots.txt and the URL is allowed. The group's three rules (/api/, /*/files/, /media) do not cover it either way; (k) fixes the allow on the normalized path.
- `r38-i-developer_mozilla_org-del` — `https://developer.mozilla.org/en-US/docs/Web` — user-agent `Googlebot` — declared **check_invalid**
  - deciding line(s): L4 `Disallow: /api/`; L5 `Disallow: /*/files/`; L6 `Disallow: /media`
  - why: Contract (i): U+007F is a control character, ASCII outside the RFC 3986 character set, so the check is a check fault (check_invalid); no access result is evaluated. The path is outside all three disallowed rules.
- `r38-e-developer_mozilla_org-api` — `https://developer.mozilla.org/api%2Fv1` — user-agent `Googlebot` — declared **allow**
  - deciding line(s): L4 `Disallow: /api/`
  - why: Contract (e): %2F is a reserved escape and is kept, so the path is /api%2Fv1; the rule value /api/ ends in '/', which the path does not have at that position, so the prefix rule does not match and the URL is allowed.

## (h) fault manifests (same retained robots files)

### `manifest.h-float-status.json`

- declared: exit 2, verdict `could-not-evaluate`, checksEvaluated 1, findings `[{"check": "h-float-status-1e400", "reason": "check_invalid"}]`
- basis: (h) clarification: 1e400 is JSON but not an integer, so the status is a check fault for that check; the neighbour is evaluated and allowed.

### `manifest.h-infinity-status.json`

- declared: exit 2, verdict `could-not-evaluate`, checksEvaluated 0, findings `[{"check": null, "reason": "input_invalid"}]`
- basis: (h): Infinity outside a string is not JSON, so the manifest is input_invalid and nothing is evaluated.

### `manifest.h-long-status.json`

- declared: exit 2, verdict `could-not-evaluate`, checksEvaluated 1, findings `[{"check": "h-long-status-5000", "reason": "check_invalid"}]`
- basis: (h): a 5,000-digit out-of-range integer status is a check fault for that check only; the neighbour is evaluated and allowed.

### `manifest.h-nan-unused.json`

- declared: exit 2, verdict `could-not-evaluate`, checksEvaluated 0, findings `[{"check": null, "reason": "input_invalid"}]`
- basis: (h): NaN outside a string is not JSON, so the manifest is input_invalid and nothing is evaluated -- even though the NaN sits in a field no rule reads.

### `manifest.h-neginfinity-status.json`

- declared: exit 2, verdict `could-not-evaluate`, checksEvaluated 0, findings `[{"check": null, "reason": "input_invalid"}]`
- basis: (h): -Infinity outside a string is not JSON, so the manifest is input_invalid and nothing is evaluated.

### `manifest.h-unused-bigint.json`

- declared: exit 0, verdict `clean`, checksEvaluated 2, findings `[]`
- basis: (h): a 5,000-digit integer in a field the contract does not read changes nothing; both checks are evaluated and allowed.

