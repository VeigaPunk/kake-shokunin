# ScoutGoogleImplicit — does Google's parser or spec normalize the path before the implicit /robots.txt allow? (`%2E`, query, case)

Round-38 W1 question: whether S096 `google/robotstxt` (`robots.cc`) or S095 normalizes the path before
the implicit `/robots.txt` allow, and how each treats `%2E`, query and case there. Judged against
round-38 (k) (`SCORECARD.md:2158-2163`, clarifications `:2255-2257`).
Sources: `robots.cc`, `robots_test.cc`, `robots.h`, `README.md` at commit
`22b355ff855419e6a3ff8ff09c0ad7fdb17116f9` (GitHub API date 2026-04-01T12:46:47Z; the anchor commit
of `corpus/SOURCES.md:204`); S095 fetched (Search Central URL 301 -> https://developers.google.com/
crawling/docs/robots-txt/robots-txt-spec, HTTP 200, 99414 B).

## Observed facts

1. **No implicit allow in the parser.** `robots.cc` has no `/robots.txt` code path (only a comment at
   `robots.cc:23`); `AllowedByRobots` is `ParseRobotsTxt(...); return !disallow();`
   (`robots.cc:537-546`); `robots.h`/`README.md` likewise — no implicit allow (`Disallow: /` -> `false`).
2. **The parser does not normalize the URL path.** `robots.cc:540-542`: "The url is not normalized
   (escaped, percent encoded) here because the user is asked to provide it in escaped form already."
   `robots_test.cc:396-397`: "It's up to the caller to percent encode a URL". `GetPathParamsQuery`
   (`robots.cc:127-157`) only strips scheme/authority and fragment.
3. **`%2E`/`%72` are never decoded; rule hex is uppercased, URL hex is not.** `MaybeEscapePattern`
   (`robots.cc:161-207`, rule values only) uppercases `%xx`, percent-encodes non-ASCII, never decodes.
   `robots_test.cc:432-444`: rule `/foo/bar/%62%61%7A` does not match `/foo/bar/baz` ("illegal
   according to RFC3986 … should not be relied on"); `robots_test.cc:1011-1016`: `%aa` -> `%AA` only.
4. **Query is in the compared path; fragment is dropped.** `robots_test.cc:997-1009`:
   `http://www.example.com/a/b?c=d&e=f#fragment` -> `/a/b?c=d&e=f`. S095 table (`spec.txt:560`):
   `/fish.php?id=anything` is matched by `/fish`; a bare trailing `?` is kept (`/robots.txt?`).
5. **Byte-exact matching, no case folding.** `Matches` compares `path[pos[i]] == *pat` (`robots.cc:80-119`);
   S095: "the matching is case-sensitive" (`spec.txt:553`); robots.txt URL case-sensitive (`spec.txt:101`).
6. **S095 on percent-encoding** (`spec.txt:523-527`): "As defined in RFC 9309 Section 2.2.2, Google's
   crawlers compare rules against URLs using their percent-encoded forms, and automatically
   canonicalize raw UTF-8 rule paths into percent-encoded forms" (`ツ` == `%E3%83%84`). Nothing on
   decoding unreserved escapes; the text never mentions an implicit allow (`/robots.txt` appears
   only in the file-location section, `spec.txt:100-175`).

Harness `/fast/scratch/hyaku/kake-r38w1/ScoutGoogleImplicit/harness.cc` (sha256 `a857b41a…e64f4e`)
transcribes `Matches`, `GetPathParamsQuery`, `MaybeEscapePattern` verbatim (`absl::string_view`->
`std::string_view`, `FixedArray`->`vector`); `g++ -std=c++17 -O0` exit 0, run exit 0. Observed:
`path …/robots%2Etxt -> [/robots%2Etxt]`; `…/%72obots.txt -> [/%72obots.txt]`; `…/robots.txt? ->
[/robots.txt?]`; `…/ROBOTS.TXT -> [/ROBOTS.TXT]`; `escape /robots%2etxt -> [/robots%2Etxt]`;
`pattern[/robots.txt] vs path[/robots%2Etxt], [%72obots.txt], [/ROBOTS.TXT], [/robots%2Ftxt] => false`;
`pattern[/robots%2Etxt] vs path[/robots%2etxt] => false`; `pattern[/robots.txt$] vs [/robots.txt?] =>
false`.

## Agree / differ / silent per (k) sentence

- "a URL whose path to match, normalized by rule (e), is exactly `/robots.txt` is allowed (so
  `/robots%2Etxt` and `/%72obots.txt` are allowed)" — **SILENT on the allow (parser and spec);
  DIFFER on the normalization premise.** Neither source states an implicit allow and `robots.cc`
  implements none, so the examples are ungrounded there; keyed on Google's path string both are not
  `/robots.txt` (fact 3), so Google lets the rules decide them — opposite to (k) under `Disallow: /`.
  [INFERENCE, high] Googlebot's fetch layer (outside the repo) may still refuse a block on its own
  robots.txt; S096/S095 do not show it. (e)'s URL-side hex uppercasing also differs (`/robots%2Etxt`
  rule vs `/robots%2etxt` URL: no match).
- "A path to match with a query (`/robots.txt?x=1`) … decided by the rules" — **AGREE**: the query is
  inside `path_`, so it is not equal to `/robots.txt`. Caveat: bare `/robots.txt?` is `/robots.txt?`
  in robots.cc where (k)'s clarification makes it `/robots.txt` — that **differs**, visible in
  `$`-anchored rules (`/robots.txt$` does not match `/robots.txt?`).
- "another case (`/ROBOTS.TXT`) … decided by the rules" — **AGREE**: byte-exact match, no folding.
- "or a kept reserved escape (`/robots%2Ftxt`) … decided by the rules" — **AGREE**: nothing decoded,
  `%2F` only matches a rule spelled `%2F`.
- "The fragment is never part of the path" — **AGREE** (fact 4).

Net: (k)'s query/case/reserved/fragment clauses match Google's parser and spec; its two allow examples
and the `/robots.txt?` clarification do not — they need unreserved-escape decoding, which `robots.cc`
omits and S095 does not state. Only support: RFC 9309 §2.2.2 (S011), cited by S095 for percent-encoding only.

## Commands (exit codes) and retained digests

`git clone -q` + `git checkout -q 2dab7f31…` exit 0; GitHub API lookup exit 0 (`22b355ff…`);
`curl robots.cc` HTTP 200 24644 B; `robots_test.cc`/`robots.h`/`README.md` HTTP 200 each;
`curl -sSL …/robots_txt` 301 then HTTP 200 99414 B; `g++` exit 0; `./harness` exit 0; all curls exit
0. Retained: `spec.txt` `2ca1d55c…e453`, `spec.html` `19f4b2bb…1ec25`, `robots.cc` `d05a7fa7…ed473`,
`robots_test.cc` `9868caef…d670`, `robots.h` `912f3a5c…0bd5`, `README.md` `3bc73ffb…11050`, `harness`
`6b8adca4…da58`.

Limits: RFC 9309 not opened (not named in my item); its text enters only via (k). Real library not
compiled (abseil) — behavior from verbatim transcriptions plus the repo's tests, not the shipped
binary. No live Googlebot observation; crawler-layer statements are [INFERENCE]. S095 line numbers
refer to tag-stripped `spec.txt`.
