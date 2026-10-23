# S096 re-open — github.com/google/robotstxt (README, robots.cc, robots.h)

Seat KakeR37.ScoutReopenS096, leaf, independent live GET. No sealed-tree access; this file is my only lane write.
## Access (freshness)
- `GET https://github.com/google/robotstxt` at **2026-10-23T03:23:15Z**: status **200**, final URL
  **https://github.com/google/robotstxt** (0 redirects), 321354 B. Retained: 200, same final URL,
  321363 B at 02:50:50Z. **The page did not move.**
- Same page: visible text under the fetcher's own rule (`fetch_sources.py:visible_text`) is
  byte-identical to retained `S096.txt` — sha256 `d17aa81d51ba5fa3e030f24697a95bc50b864545bd90ba9db5228008a8615574`, 1274 words, 8703 B. Body sha differs only
  (`9ed0c743…b74a` vs `fe4b5e3a…5c1b`, 9 B) = GitHub per-response chrome, not content.
- Code: `raw.githubusercontent.com/google/robotstxt/master/{README.md,robots.cc,robots.h}`, all
  **200** — README 5282 B, robots.cc 24644 B, robots.h 11034 B; master commit
  `22b355ff855419e6a3ff8ff09c0ad7fdb17116f9`, committer date 2026-04-01T12:46:47Z.
## Passages grounding C1 contract rules (exact, ≤25 words)
1. **(b) BOM drop** — robots.cc:435–436, `RobotsTxtParser::Parse`: "Google-specific optimization:
   UTF-8 byte order marks should never appear in a robots.txt file, but they do nevertheless."
   Code skips the 3-byte EF BB BF prefix (438–441), as the contract fixes.
2. **(d) longest normalized value, octets** — robots.cc:470–471, above
   `LongestMatchRobotsMatchStrategy`: "The maximum number of characters matched by a pattern is
   returned as its match priority." Priority is `pattern.length()` (690–698) of the normalized value
   (escaping applied to allow/disallow only, 284–292), so `*`/`$` count — contract's wording.
3. **(d) empty rule never matches** — robots.cc:55–56: "match priority == 0: Match, but treat it as
   if matched an empty pattern." `disallow()` counts only priorities > 0 (557, 567).
4. **(c) new group after a rule; unknown keys don't end one** — robots.cc:618–621:
   "if (seen_separator_) { seen_specific_agent_ = seen_global_agent_ = seen_separator_ = false; }"
   `seen_separator_` is set only by allow/disallow (641, 674), grounding (b) "does not end a group".
5. **(b) comment strip** — robots.cc:305: "Remove comments from the current robots.txt line."
6. **(e) normalization direction** — robots.cc:161–163: "Canonicalize the allowed/disallowed paths.
   For example: /SanJoséSellers ==> /Sanjos%C3%A9Sellers %aa ==> %AA".
7. **(e) path/query, no fragment** — robots.cc:122–124, `GetPathParamsQuery`: "Removes scheme,
   authority, and fragment. Result always starts with '/'."
8. **(d) tie allows** — 558/568 use strict `>`: equal allow/disallow priority returns false
   (allowed). Matches the contract's "allow decides" (RFC 9309 §2.2.2 says only SHOULD).
## Contradictions with contract sentences (do not copy S096 here)
- **K1 (e) decode-unreserved.** Contract decodes `%XX` of unreserved chars; `MaybeEscapePattern`
  never decodes, only uppercases hex — robots.cc:184: "(c) Already escaped and escape-characters
  normalized (eg. %2f -> %2F)." `Disallow: /a%7Eb` + path `/a~b`: contract normalizes to `/a~b` →
  block; S096 → allow.
- **K2 (d) `/index.htm` rewrite.** robots.cc:655–656: "Google-specific optimization: 'index.htm'
  and 'index.html' are normalized to '/'." `Disallow: /a/` + `Allow: /a/index.htm` + path `/a/`:
  S096 allows (priority 4 vs 3); contract disallows — opposite verdict.
- **K3 (b)(c) exact key equality.** Contract compares keys exactly to `user-agent`/`allow`/
  `disallow`; robots.cc:44 "static bool kAllowFrequentTypos = true;" plus `StartsWithIgnoreCase`
  (217–260) accept `Disalow:`, `User agent:`, and any key starting `allow` (e.g. `Allowance:`).
  Contract ignores all three.
- **K4 (c) exact group name.** Contract compares the whole trimmed name. robots.cc:602–608
  truncates at the first char outside `[A-Za-z_-]` (robots.h:197 "Example: 'Googlebot/2.1' becomes
  'Googlebot'"), and robots.cc:623–624: "Google-specific optimization: a '*' followed by space and
  more characters in a user-agent record is still regarded a global rule." `User-agent: Foo/1.0`
  matches check UA `Foo` in S096 only; `User-agent: * x` is global in S096 only.
- **K5 (b) line truncation.** Contract has no per-line cap; robots.cc:413–417 "If so, we can ignore
  the chars on a line past that" with `kMaxLineLen = 2083*8` (16664 B) drops tails of long lines.
- **K6 (b) the 512000-byte limit.** Absent from robots.cc (no file-size cap in `Parse`; only the
  line buffer). S011 §2.5 says "The parsing limit MUST be at least 500 kibibytes", so "exactly this
  limit" is the lane's reading — not RFC text and not S096.
- **K7 (b) line without colon.** Contract ignores it; robots.cc:321–323: "Google-specific
  optimization: some people forget the colon, so we need to accept whitespace in its stead."
  `Disallow /x` is a rule in S096, ignored by the contract.
## Gaps — S096 is silent (do not cite it)
- **(a) access results.** No status logic in robots.cc/robots.h; README:128–130 says the library
  "do not handle implementation logic that a crawler might apply outside of parsing and matching".
  Contract (a) rests on S011 §2.3.1.3 (4xx: crawler MAY access; contract fixes allowed) and §2.3.1.4.
- **(e) `/robots.txt` implicitly allowed.** No special case in robots.cc; grounds are S011 §2.2.2
  ("The /robots.txt URI is implicitly allowed.").
- **Caller-side normalization.** README:125–126: "this library will not perform full normalization
  of those URI parameters." S096 cannot ground the tool's own path normalization.
## Freshness note
- Stale metadata in both snapshots: the GitHub repo description still says "(compliant to C++11)"
  while README.md:4 says C++14. Corpus rows should cite README, not the page blurb.
## Not verified
- robots.cc was not compiled or run; K1–K7 examples are code-reading inferences, not executed.
- Did not run the C1 counter (no key); did not read/stat/search the sealed tree; no tooling installed.
## Artifacts (sandbox)
`/fast/scratch/hyaku/kake-r37w1/ScoutReopenS096/raw/` — S096_live.html `9ed0c7435c6de22cace7f86ca4eb0c9fb717a0a092bf22c5813d3fa46f2db74a`; S096_live.txt `d17aa81d51ba5fa3e030f24697a95bc50b864545bd90ba9db5228008a8615574`; README.md `3bc73ffbf6ba2f79ba0a1b33d10a300c47bffc03ff901b0220447a0c71e11050`; robots.cc `d05a7fa74c0e8b9fc440d15f4c3ae9a80873c0d950e569de2926303fd75ed473`; robots.h `912f3a5c6821f8a9a97269f9598b7f29ac1edf1ee20e173f1dd2d9ca48fb0bd5`.
