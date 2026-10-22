# ReopenSourcesOthers — re-open of S079, S080, S081, S084, S085, S006 (r35 w1)

Method: re-ran the round's own fetcher (byte-identical copy, sha256 c807eba010f476eadc78129c23de909878dcd30f99bfebdc646dcb84b4c30a3d,
equals the fetcherSha256 the retained receipts record for S006/S081/S084/S085) against the six live
URLs in my sandbox, then compared body sha256, text sha256 (same extraction rule) and diffed text.

Commands (exit codes):
- `mkdir -p /fast/scratch/hyaku/kake-r35/w1/ReopenSourcesOthers/{fetch,tmp}` → OK
- `cp .ufo/waves/round-35/fetch_sources.py <sandbox>/ && TMPDIR=<sandbox>/tmp python3 -B fetch_sources.py --only S079,S080,S081,S084,S085,S006` → EXIT=0; six lines all `200`:
  S079 31690 B 22:25:37Z, S080 40569 B, S006 138096 B, S081 107491 B, S084 269 B, S085 275 B (all 2026-10-22T22:25:37-38Z)
- Python compare of retained vs live receipts + bodies + text (outputs below).

## Six rows

| id | URL | status | match vs retained | difference |
|---|---|---|---|---|
| S079 | https://securitytxt.org/ | 200/200 | text MATCH (textSha 66722966…fa67 both); body bytes differ | 40 bytes differ (raw offsets 9431–9470): only the Cloudflare `data-cfemail` hex token; same length, invisible to text |
| S080 | https://jekyllrb.com/docs/configuration/options/ | 200/200 | EXACT — body bytes and text byte-identical | none |
| S081 | https://en.wikipedia.org/wiki/Security.txt | 200/200 | EXACT — body bytes and text byte-identical | none |
| S084 | https://github.com/.well-known/security.txt | 200/200 | text differs in Expires only | `Expires: 2026-11-21T22:02:20z` → `2026-11-21T22:25:38z`: +23 m 18 s, exactly the elapsed time between the two GETs; date/hour unchanged |
| S085 | https://www.google.com/.well-known/security.txt | 200/200 | EXACT — body bytes and text byte-identical | none |
| S006 | docs.github.com/en/pages/…/about-github-pages-and-jekyll | 200/200 | EXACT — body bytes and text byte-identical | none |

Quotes (located in retained `.ufo/waves/round-35/sources/<id>.txt`; each file is one line after
whitespace collapse, so location = character offset):
- S079, off 581 (18 words): "security.txt defines a standard to help organizations define the process for security researchers to disclose security vulnerabilities securely"
- S080, off 1075 (19 words): "Disable caching of content to disk in order to skip creating a .jekyll-cache or similar directory at the source"
- S081, off 1504 (13 words): "similar in syntax to robots.txt but intended to be machine and human readable"
- S084, off 239: "Expires: 2026-11-21T22:02:20z"
- S085, off 245: "Expires: 2030-04-01T00:00:00z"
- S006, off 2785 (18 words): "By default, Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor"

## Tier/kind check (rows S078–S085 not yet in corpus/SOURCES.md at report time — grep for `S07[89]|S08[0-5]` found nothing; recommendations for the scribes)

- S079 securitytxt.org: kind docs, tier A — official project site for its scope (maintainer statement).
- S080 jekyllrb.com options page: kind docs, tier A — official Jekyll docs; S006's registry row (corpus/SOURCES.md:14) is docs/A, opened 2026-10-19, recheck 90d → re-open 2026-10-22 is within cadence; teaching (default exclusions) confirmed still on the live page at off 2785.
- S081 Wikipedia: kind community — and the contract says community is never A; ceiling is C (lead only). Verdict below.
- S084/S085: kind dataset (served artifact), tier A only for the narrow scope "the live file this operator serves"; they witness how two major publishers run security.txt, not the RFC.

## S081 verdict — REJECT as secondary restatement (status rejected; kept as evidence of taste)

1. Its load-bearing content (purpose, `.well-known/security.txt` location, field syntax) restates RFC 9116 (S078) and the official site (S079), both retained tier-A primaries; nothing the C2 publishing entry needs must come from S081.
2. Its only non-redundant material is history/adoption trivia (Foudil draft Sept 2017, CISA directive, 2017–2020 press citations in References) — outside the serving/publishing scope, and press-cited, i.e. not reproducible detail.
3. kind=community can never be A; B requires an expert write-up with reproducible detail, which a crowd-edited wiki page does not meet here; so C is its ceiling, and a C lead that adds no needed premise is a rejection candidate under the SOURCES.md contract.
Caveat: judged on the full visible text (979 words) of the retained copy, which is byte-identical to today's live page.

## Findings that bear on the round's freshness axes

- S084's Expires is computed per request: served value = request time + 30 days, exact to the second (22:02:20→22:25:38 tracks the GET times). Consequence: github.com/.well-known/security.txt can NEVER be byte-stable across fetches; any counter, pin or check that demands a stable bodySha256 for S084 will fail forever, and the retained Expires line goes stale by definition. Google's S085 (static Expires 2030) was byte-identical — the contrast is real, not noise.
- S079 body bytes vary per fetch only in the 40-byte Cloudflare email-obfuscation hex; text is the right comparison invariant there too. So 4/6 pages are byte-stable (S080, S081, S085, S006); S079 and S084 are text-stable only.

## Gaps / not verified

- Did not re-open S078 (RFC 9116), S082, S083 — outside my assigned six.
- Did not run any sealed counter; no sealed directory touched.
- Tier/kind cells above are recommendations; the scribe seats own the SOURCES.md rows (none landed yet).
- Tooling: no packages installed or updated; used the repo's own python3 fetcher.
