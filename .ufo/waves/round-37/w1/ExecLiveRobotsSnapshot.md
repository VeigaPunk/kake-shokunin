# ExecLiveRobotsSnapshot — live robots.txt input for C1 (round 37, wave 1)

Built the served `/robots.txt` of the 12 assigned hosts and a 55-check C1-shaped manifest whose
every `expect` is grounded in a verbatim line of the recorded file. Only lane write: this report.

## Deliverables (all under `/fast/scratch/hyaku/kake-r37w1/ExecLiveRobotsSnapshot/`; sha256[:16])

`robots/receipts.json` `72d17eddee90b574` · `robots/manifest.json` (55 checks, 71 quoted lines)
`f184b0b9ad328282` · `robots/manifest.strict.json` (same checks, no evidence key) `d2cafee9176b714f`
· `fetch_robots.py` `f7c061f88fe43a53` · `build_manifest.py` `303fe494a3e162ea` ·
`validate_manifest.py` `0f9b777cffd80456` · `check_receipts.py` `b1fb3659d71094b5` ·
`receipts_check.json` `65391fe540da30a2`. Bodies: `robots/*.txt` (12 files).

## Commands (sandbox, TMPDIR set) and results

1. `timeout 600 python3 -B fetch_robots.py` → exit 0. 12 GETs, one per host, 1.1 s apart, UA
   `kake-shokunin-round37/1.0 (robots.txt snapshot; +https://github.com/veigapunk)`,
   `--max-time 30 --max-redirs 5`, no retries; 2026-10-23T03:23:15Z–03:23:31Z, 0 redirects, all 200.
2. `python3 -B build_manifest.py` → exit 0; asserts every quote against the recorded line, 55
   checks (4–7 per host, 38 allow / 17 disallow).
3. `python3 -B validate_manifest.py robots/manifest.json --evidence` → exit 0, `faults: []`,
   stats `checks 55, allow 38, disallow 17, quotes 71`. The validator implements only the
   contract's fault list (bullets (f)/(g)): object, unique non-empty id, product-token user agent,
   status in 200-299/400-499/500-599, absolute http(s) URL with host, expect one of two strings,
   `robots` a contained regular file. It parses no rule and decides no access.
4. `python3 -B validate_manifest.py robots/manifest.strict.json` → exit 0, `faults: []`.
5. `python3 -B check_receipts.py > receipts_check.json` → exit 0, `faults: []`; 12/12 hosts, bytes
   and sha256 re-derived from disk, per-host URL/host/status agreement checked.

## Receipts (full record in `robots/receipts.json`)

| host | st | bytes | sha256[:12] | UTC | host | st | bytes | sha256[:12] | UTC |
|---|---|---|---|---|---|---|---|---|---|
| www.rfc-editor.org | 200 | 135 | df052cf39044 | 03:23:15 | developers.google.com | 200 | 93 | 2d1ba1920a0a | 03:23:16 |
| github.com | 200 | 14540 | b622e2dd9b60 | 03:23:18 | docs.github.com | 200 | 13 | d9066d29c1df | 03:23:19 |
| www.sitemaps.org | 200 | 45 | 19edcf7d91ea | 03:23:20 | developer.mozilla.org | 200 | 119 | 8f2712e11105 | 03:23:22 |
| en.wikipedia.org | 200 | 28275 | 48b98d80c844 | 03:23:23 | www.robotstxt.org | 200 | 24 | e5c4b84484ee | 03:23:25 |
| html.spec.whatwg.org | 200 | 69 | 6d81a8c02087 | 03:23:26 | pages.github.com | 200 | 46 | e87ca891cd14 | 03:23:28 |
| ds4cc.com (owned, GET only) | 200 | 62 | 70f9ea2885de | 03:23:29 | veigapunk.github.io (owned) | 200 | 72 | cdeee3065f3c | 03:23:31 |

## Manifest shape

`{"version":1,"checks":[…]}`; each check has `id`, `robotsStatus` (JSON int 200), `userAgent`
`Googlebot` (product token; GitHub and Wikipedia have no Googlebot group — only AdsBot-Google and
Mediapartners-Google* — so the `*` fallback decides there), `url` on the receipt's host, `expect`,
`robots` (relative file in the manifest's directory), plus `evidence` (`sourceUrl, finalUrl,
fetchedUtc, bodySha256, quotes[{line,text}], why`). Contract (f) is an exhaustive fault list that
does not mention unknown keys; `manifest.strict.json` is the minimal projection if a reader
disagrees.

## What the live files give C1 (all in the manifest)

- (b) en.wikipedia.org starts with EF BB BF; four bodies end without a final newline (rfc-editor,
  docs.github, sitemaps.org, wikipedia) — the last record must still count.
- (c) sitemaps.org and pages.github.com serve no `user-agent` record (only a Sitemap, which must
  not open a group); docs.github.com is 13 bytes of `User-agent: *` with no rule; MDN's `Sitemap:`
  (line 2) sits inside the `*` group above rules at lines 4–6.
- (d) www.robotstxt.org's only rule is `Disallow:` with an empty value; GitHub's `*` group holds
  165 rule records; longest-match allow wins twice live — GitHub line 361
  `Allow: /*?tab=achievements&achievement=*` (33 octets) over line 522 `Disallow: /*?tab=*` (8),
  and Wikipedia line 149 `Allow: /w/api.php?action=mobileview&` (29) over line 153 `Disallow: /w/` (3).
- (e) Wikipedia has 224 rule lines with `%XX`, one raw-non-ASCII rule (line 171
  `Disallow: /wiki/Wikipedia:Löschkandidaten/`, encoded twin line 170); the encoded-URL check
  proves the escape is preserved, not decoded.
- (a) limit: every host answered 200 first try, so the live set exercises only the 2xx branch; no
  live 4xx/5xx evidence exists here.

## Not done / not verified

No `scripts/robots_audit.py`, `urllib.robotparser` or any robots matcher ran — no machine computed
a decision, so each `expect` is my hand reading of the quoted line and the quotes are the review
surface. No counter, no key; the sealed tree was never listed or opened. No network beyond the 12
GETs; nothing installed.

## Risks
Live files drift; UTC times and body hashes are the only anchor. The 38/17 allow split is what the
files say, not a designed balance. `developers.google.com/youtube/partner` (allow) is the one
judgement call — it rests on the rule's trailing slash, not on a fetched page. Bodies and manifest
must stay in one directory or the `robots` paths break.
