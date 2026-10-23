# ScoutContractVsGoogle — C1 (a)–(e) against S095 and google/robotstxt robots.cc

Seat KakeR37.ScoutContractVsGoogle (leaf). Base 621fb528; declarations read at 4b089da6 from SCORECARD.md. Lane read-only.
Evidence inputs: S011/S095/S096 text and receipts.json from `.ufo/waves/round-37/sources/` (accessed 2026-10-23T02:50:49–51Z);
`robots.cc` and `robots.h` fetched from github.com/google/robotstxt (S096) at commit **50a0dace76c54a0f25c0d1fa6ac53ec7c657c57c** (file-path HEAD, committer date 2026-02-27):
`robots.cc` sha256 `d05a7fa74c0e8b9fc440d15f4c3ae9a80873c0d950e569de2926303fd75ed473` (705 lines), `robots.h` sha256 `912f3a5c6821f8a9a97269f9598b7f29ac1edf1ee20e173f1dd2d9ca48fb0bd5`. Sandbox copies at `/fast/scratch/hyaku/kake-r37w1/ScoutContractVsGoogle/`.
Method: no LSP server covers a C++ file fetched outside a project, so this is source reading (semantic by construction: the cited lines are the logic), not grep inference. S095.txt is one collapsed line; my sentence-split copy is `S095.sent.txt:<n>` in the sandbox, and quotes below name the S095 section instead.
Legend: `=` agrees · `≠` differs · `–` silent. "OK?" = the contract's fixed reading is justified by at least one named source and contradicted by none that governs the tool.

| id | contract sentence (abridged) | S011 RFC 9309 | S095 Google spec | robots.cc @50a0dace | OK? |
|---|---|---|---|---|---|
| a1 | 2xx: file parsed and decides | = §2.3.1.1 "crawler MUST follow the parseable rules" | = "2xx … process the robots.txt file as provided" | – by design: S096 "do not handle implementation logic … outside of parsing and matching" | yes |
| a2 | 400–499 allowed, whatever file says | ~ §2.3.1.3 "crawler MAY access any resources" (fixed to allow) | ≠429: "treat all 4xx errors, except 429, as if a valid robots.txt file didn't exist" | – | yes, 429 caveat |
| a3 | 500–599 disallowed incl. /robots.txt | = §2.3.1.5 "MUST assume complete disallow" | ≠ "If there's no cached version available, Google assumes there's no crawl restrictions" | – | yes (RFC); S095 differs |
| b1 | first 512000 bytes only, exact | ~ §2.5 "parsing limit MUST be at least 500 kibibytes" | = "size limit of 500 kibibytes … content after … is ignored" | – no file cap; per-line cap 16664 at 413–419 | yes |
| b2 | leading EF BB BF dropped | – | = "including the Unicode Byte Order Mark (BOM) at the beginning" | = 411, 438–441 (skips only a leading BOM) | yes |
| b3 | invalid bytes become U+FFFD | – (only "MUST be UTF-8") | ≠ "may ignore characters that are not part of the UTF-8 range" | ≠ 187–203 escapes the raw high byte as %XX, no decode | no — invented reading |
| b4 | lines end CR, LF or CRLF | ~ ABNF "EOL = *WS [comment] NL" | = "lines must be separated by CR, CR/LF, or LF" | = 441–457 | yes |
| b5 | from first '#' is comment | = Fig. 5 "# Designates a line comment" | = only the example at S095 sentence 10 (no inline-comment rule) | = 305 `strchr(line,'#')` | yes |
| b6 | line without ':' ignored | = ABNF `rule = *WS ("allow"/"disallow") *WS ":"` | = "a valid robots.txt line consists of a field, a colon, and a value" | ≠ 323–345 accepts whitespace as separator if exactly two tokens | yes (robots.cc lenient) |
| b7 | key = text before first ':', SP/HTAB-trimmed, ASCII ci | = ABNF literals are case-insensitive (RFC 5234) | = "Field names are case-insensitive" | ≠ 217–260 `StartsWithIgnoreCase` + typos, 296 strips all ASCII WS | yes |
| b8 | value trimmed of spaces and tabs | = ABNF `*WS` = SP/HTAB | – | ≠ 296 also strips \v \f | yes |
| b9 | UA/allow/disallow are records; other keys do not end a group | = §2.2.4 "a 'Sitemaps' record MUST NOT terminate a group" | = sitemap-between-UAs "treated as one group" | = 700–703 empty handlers; only 641/674 set separator | yes |
| b10 | allow/disallow before first UA ignored | ~ ABNF group ordering (§2.1); contract cites §2.2.2, which does not state it | – | = 640, 673 `if (!seen_any_agent()) return;` | yes |
| c1 | UA line starts a group unless previous record was UA | = ABNF `startgroupline *(startgroupline / emptyline)` | = "e" and "f" form one group; a/b four groups | = 617–621 reset only via `seen_separator_` | yes |
| c2 | UA matches a name by ASCII-ci equality (no prefix, no version) | = "MUST use case-insensitive matching to find the group that matches the product token" | = "both the user-agent field name and its value are case-insensitive" | ≠ 602–614, 629–634 + robots.h:197–198 "'Googlebot/2.1' becomes 'Googlebot'" | yes (RFC) |
| c3 | rules of every matching group combined | = "matching groups' rules MUST be combined into one group" | = "all the rules … are combined internally" | = 557–568, 643–652 (max priority across groups) | yes |
| c4 | no match → every group named '*' combined | = "MUST obey the group with … '*' value, if present" | = specific and global "are not combined" | = 560–565, 625–627 | yes |
| c5 | no '*' → no rules, all allowed | = "no rules apply" | = quxbot "unrestricted access" | = 556–570 returns false | yes |
| d1 | empty rule never matches | – (ABNF `empty-pattern` only) | – | = Matches("") true at priority 0, and 557–558 require `> 0` | yes (behaviour) |
| d2 | '*' matches any sequence incl. none | = "0 or more instances of any character" | = "0 or more instances of any valid character" | = 96–103 | yes |
| d3 | trailing '$' anchors; any other '$' literal | = "$ designates the end of the match pattern" (mid-$ unstated) | = "$ designates the end of the URL" | = 74–75, 96, 100 | yes |
| d4 | prefix match from the first character | = "matching MUST start with the first octet of the path" | = "/fish Matches any path that starts with /fish" | = 74–115 | yes |
| d5 | longest normalized value in octets, '*' and '$' counted | = "most specific match … most octets" | = "length of the rule path"; /*.htm beats /page | = 470–471, 692/697 `pattern.length()` | yes |
| d6 | allow wins ties | ~ "the 'allow' rule SHOULD be used" | = "Google uses the least restrictive rule" (its tie example) | = 558 strict `>` | yes |
| d7 | no matching rule → allowed | = "the URI is allowed" | = (precedence section) | = 556–570 | yes |
| e1 | path, '/' when empty, plus '?' and non-empty query | = Fig. table row "/foo/bar?baz=quz" | = "/fish.php?id=anything" matches /fish | = 127–152 `GetPathParamsQuery` | yes |
| e2 | fragment never part of the path | – | – | = 139–141 drops at '#' | yes (robots.cc) |
| e3 | /robots.txt always allowed when (a) says the file decides | = "The /robots.txt URI is implicitly allowed" | – (0 hits for "implicit") | – no special case; `Disallow: /` would block it | yes (RFC) |
| e4 | normalize both rule value and path before compare | = "MUST be percent-encoded … prior to comparison" | = "compare rules against URLs using their percent-encoded forms" | ≠ 399–403 escapes values only; 540–543 "url is not normalized"; robots.h:153–154 "must be %-encoded" | yes (RFC, S095) |
| e5 | non-ASCII → UTF-8 octets, uppercase hex | = "outside … ASCII … MUST be percent-encoded" | = "canonicalize raw UTF-8 rule paths into percent-encoded forms" | = 187–203 | yes |
| e6 | %XX of an unreserved character decoded | = "MUST be unencoded … unless … reserved … or outside the unreserved range" | – | ≠ 167–212 never decodes, only uppercases | yes (RFC); robots.cc differs |
| e7 | other %XX kept, hex uppercased | – | – | = 172–181, 193–197 | yes (robots.cc) |
| e8 | reserved never decoded/encoded, so %2F ≠ / | = "unless it is a reserved character in the URI" | – | = (never decodes anything) | yes |

## Findings

1. **No (a)–(e) sentence contradicts S011.** Every rule robots.cc is silent on is covered by RFC 9309 or Google's prose; every "lane reading" label in the contract corresponds to a real SHOULD/MAY/floor: (d6) SHOULD, (a2) MAY, (b1) "at least". The contract does not overstate its grounds except in item 2.
2. **b3 (invalid UTF-8 → U+FFFD) is the only invented sentence.** S011 is silent, S095 says Google "may ignore" such characters, robots.cc escapes the raw byte (one octet → 3 chars `%XX`, not U+FFFD's `%EF%BF%BD`). Observable: a rule containing one invalid byte has priority 9 under the contract and 3 under robots.cc, so a longest-match tie can flip. It is also in the L1's own survivor list ("non-UTF-8 replacement" survives 25/28), so the sealed cases do not pin it — low risk to C1, but the build is free to differ and the public text should not be read as sourced here.
3. **robots.cc is more lenient than the contract in six places**, all in the "allow more" direction, so the tool never claims access that Googlebot would deny: e6 unreserved `%XX` decode, e4 path normalization (robots.h:153–154 pushes it to the caller), b7 prefix/typo keys (robots.h:105), b6 whitespace separator, c2 `Googlebot/2.1` → `Googlebot`, plus the undocumented `index.htm`→`/$` allow-rewrite (655–672) and `/robots.txt` (e3). The index.htm rewrite is the one case where the audit can report `blocked` for a URL Googlebot allows (`Disallow: /` + `Allow: /index.htm`, path `/`); it is not in RFC 9309 or S095, so it is a documented limit, not a contract error.
4. **HTTP statuses: two documented Google divergences, both correctly resolved toward the RFC.** (a2) Google exempts 429 from "as if no file exists"; the contract follows §2.3.1.3 and allows it. (a3) Google allows when a 5xx arrives with no cached copy, and reuses a cached copy for 30 days; the contract's blanket disallow follows §2.3.1.5's MUST and does not model caching. (e3) and (a3) are in tension in the RFC itself (implicit allow vs complete disallow) and the contract resolves it explicitly ("including /robots.txt") — defensible, and the only reading that keeps /robots.txt fetched under 5xx from being reported as allowed. 3xx is a check fault, so a publisher serving a redirect gets `could-not-evaluate` rather than Google's "follow ≥5 then treat as 404" — honest, but it is a modelling gap (S011 §2.3.1.2 SHOULD).
5. **One citation slip, no rule impact:** b10 cites §2.2.2 for "rule before the first user-agent line is ignored"; the dumped §2.2.2 does not say it — it follows from §2.1's group definition and the ABNF. Cosmetic in a frozen public text; worth a correction note in the L1's closure, not a case change.
6. **c2 "most specific user agent" (S095) is not modelled.** Under pure equality there is nothing to rank, and S095's own examples (googlebot-news vs googlebot) are exact-name matches, so no observable conflict; only a file that relies on robots.cc's truncation of a versioned name lands differently.

## Not verified / not done
- I did not build or execute robots.cc (no bazel/absl build); all robots.cc statements are source reads at the pinned commit, not run output.
- No LSP: the file is outside any project; text reading is the only available method (recorded, not presented as semantic proof beyond the quoted lines).
- I did not read, stat or search the sealed cases and did not run the C1 counter (no key); `/fast/scratch/hyaku/kake-r37/` untouched.
- No tools installed; no lane file other than this report written. Read-only git only (`git show`).
