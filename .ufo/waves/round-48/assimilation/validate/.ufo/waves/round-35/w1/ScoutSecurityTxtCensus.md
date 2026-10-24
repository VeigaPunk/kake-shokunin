# Round 35 W1 — ScoutSecurityTxtCensus

Built a ten-host public census of `/.well-known/security.txt` (GET only, redirects followed, no bot-challenge handling, no owned hosts touched). All artifacts and scripts are in `/fast/scratch/hyaku/kake-r35/w1/ScoutSecurityTxtCensus/`; nothing in the lane was modified except this report.

## Artifacts
- `census/<host>.body`, `census/<host>.hdr`, `census/.raw` (status/effective URL/Content-Type), `census/.request_ts`, `census/.hosts`
- `census.json` — 10 rows + summary, sha256 `29e887b0d92102daa05ac710622051a03f9e22153692060ca1c4fb0b7c2ed1fa`
- `fetch.sh` (`523f1db5…`), `build_census.py` (`72b9491e…`), `summarize.py` (`567dfb74…`), `summary.txt`, `probes/` (github re-fetch probes)

## Commands (exact, with exit codes)
1. `bash fetch.sh` — EXIT=0. Request window 2026-10-22T22:25:07Z→22:25:08Z, UA `Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0`, `xargs -P4`, `curl -sS -L --max-time 30 --max-redirs 5`.
2. `python3 -B build_census.py` — EXIT=0, wrote `census.json` rows 10; counts `{"expires_more_than_365_days_ahead": 3, "serving": 8, "signed_pgp": 1}`.
3. `python3 -B summarize.py` — EXIT=0, `OK: row fields and summary counts reproduce from saved bodies + .raw statuses`.
4. Bodies-only recount (no `.raw`, no `census.json`), pasted verbatim below — same 8 / 3 / 1.

```
cd /fast/scratch/hyaku/kake-r35/w1/ScoutSecurityTxtCensus && served=$(grep -lai '^Contact:' census/*.body | wc -l); signed=$(grep -lai -- '-----BEGIN PGP SIGNED MESSAGE-----' census/*.body | wc -l); req=$(date -d "$(cat census/.request_ts)" +%s); gt=0; for f in $(grep -lai '^Expires:' census/*.body); do e=$(grep -ai '^Expires:' "$f" | tr -d '\r' | sed 's/^Expires:[[:space:]]*//' | tr 'z' 'Z'); es=$(date -d "$e" +%s); d=$(( (es-req)/86400 )); [ "$d" -gt 365 ] && gt=$((gt+1)); done; echo "serving=$served gt365=$gt signed=$signed"
```
Output: `serving=8  gt365=3  signed=1`.

## Census table (distances from request time 2026-10-22T22:25:07Z)
| host | status | final URL | Content-Type | fields | Expires | days | Signed | Canonical |
|---|---|---|---|---|---|---|---|---|
| github.com | 200 | same | text/plain; charset=utf-8 | Contact, Expires, Canonical, Policy, Hiring, Acknowledgments, Preferred-Languages | 2026-11-21T22:25:07z | +30.0 | no | yes |
| gitlab.com | 200 | same | text/plain; charset=utf-8 | 2×Contact, Policy, 2×Acknowledgments, Canonical, Preferred-Languages, Hiring, Expires | 2027-01-31T05:00:00.000Z | +100.3 | **yes (cleartext PGP, CRLF)** | yes |
| www.apple.com | 200 | same | text/plain | Contact, 2×Acknowledgments, Policy, Expires | 2027-10-19T01:00:00.000Z | +361.1 | no | no |
| www.cloudflare.com | 200 | same | text/plain; charset=utf-8 | 2×Contact, Policy, Hiring, Preferred-Languages, Canonical — **no Expires** | — | n/a | no | yes |
| www.facebook.com | **400** | same | text/html | none (error page, 1542 B) | — | n/a | no | no |
| www.google.com | 200 | same | text/plain | 2×Contact, Encryption, Acknowledgments, Policy, Hiring, Expires | 2030-04-01T00:00:00z | **+1256.1** | no | no |
| www.microsoft.com | 200 | same | text/plain; charset=utf-8 | Acknowledgements, Canonical, Contact, Encryption, Expires, 3×Policy, CSAF, Preferred-Languages | 2026-09-23T16:00:00.000Z | **−29.3 (expired)** | no | yes |
| www.mozilla.org | 200 | same | text/plain | Contact, Expires, Policy, Preferred-Languages, Canonical | 2037-09-19T00:00:00.000Z | **+3984.1** | no | yes |
| www.python.org | **404** | same | text/html | none (404 page, 32590 B) | — | n/a | no | no |
| www.wikipedia.org | 200 | **https://en.wikipedia.org/…** (301) | text/plain | Contact, Expires, Acknowledgments, Preferred-Languages, Policy | 2029-03-31T09:00:00.000Z | **+890.4** | no | no |

**Summary counts:** serve it **8/10** (both `www.` and apex probed for the two misses); Expires **>365 days ahead 3/8** (google, mozilla, wikipedia; apple at 361.1 d is the boundary case and is *not* counted); PGP signed **1/8** (gitlab). Also: 1/8 omits Expires entirely (cloudflare, a `MUST` per RFC 9116 §2.5.5), 1/8 is already stale (microsoft, −29.3 d), 5/8 carry Canonical, 7/8 have every field RFC 9116 marks mandatory.

## Falsifiers I ran against my own numbers
- **github's `Expires` is generated per response, not stored.** Three independent fetches: `Expires: 2026-11-21T22:25:07z` at 22:25:07Z, `…22:25:05z` at 22:25:05Z, `…22:25:21z` at 22:25:21Z — exactly request time + 30 days each, lowercase `z`. So "days ahead" for github describes a rolling 30-day horizon and must not be read as a static timestamp.
- **The two misses are path-specific, not agent blocks.** Same UA on `https://www.facebook.com/robots.txt` → 200 `text/plain`; `https://www.python.org/robots.txt` → 200 `text/plain`. Apex `https://facebook.com/.well-known/security.txt` → 400; `https://python.org/.well-known/security.txt` → 404 (redirects to `www.`). Legacy root `https://www.python.org/security.txt` → 200 but the body is the HTML blog index (`/blogs/`), i.e. a soft-404 and **not** counted as served; `https://www.facebook.com/security.txt` → 400.
- **Field parsing cross-checked two ways.** `grep -aic '^Contact:'` over every saved body and the independent `summarize.py` parser agree line-for-line (e.g. gitlab 2, cloudflare 2, google 2, apple 1; Expires strings identical after CRLF strip). `gitlab.com` body is CRLF with a cleartext PGP signature block that must be skipped before parsing.

## Grounding for C2 (advisory, not written by me)
Retained S078 (RFC 9116) states: `Expires` **MUST always be present**, value per RFC 3339, and "It is RECOMMENDED that the value of this field be less than a year into the future to avoid staleness" (§2.5.5); signing is **RECOMMENDED**, not required (§2.3, OpenPGP cleartext, with `Canonical` likewise recommended when signed). The census is a live witness that (a) the "less than a year" recommendation is widely ignored — mozilla 3984 d, google 1256 d, wikipedia 890 d; (b) omitting `Expires` happens in production (cloudflare); (c) a stale file can sit unrefreshed for a month (microsoft). A C2 entry on GitHub Pages publishing can point to S078 for those rules, S082/S083 for the well-known URI registry, and existing row S006 for Jekyll's default exclusion of `.`-prefixed paths (the practical reason `.well-known/` needs opt-in), but I did not write or grade that entry.

## Not verified / limits
- No `whois`/CDN attribution, so "large public hosts" rests on the listed names only; single fetch batch, no repeat to test diurnal variation except the github probes.
- HTTP status is curl's; I did not verify TLS chain details or whether 400 on facebook is a WAF policy versus a route miss (headers show `text/html` error page only).
- Wikipedia's row is a 301 to `en.wikipedia.org`, so the served file's origin host differs from the requested one; I recorded the redirect but did not test whether `Canonical` absence matters there (the file is unsigned).
