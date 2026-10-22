# Scout — is GitHub's security.txt Expires per-request? (r35 w1)

Seat: KakeR35.ScoutGithubExpiresDynamic. Axes: operability + freshness. Method: live GET only, plain `curl 8.23.0`, one vantage point (edge region `brazilsouth`). No access to `/fast/scratch/hyaku/kake-r35/sealed/` at any point; no tool installed or updated. Bodies, headers, meta and `analyze.py` in `/fast/scratch/hyaku/kake-r35/w1/ScoutGithubExpiresDynamic/` (32 files).

## Verdict: HOLDS, with a measured refinement

`Expires` is the served representation's own `Date` plus exactly **30 days (2 592 000 s)**, **0 s spread over 9 distinct generations** from 22:02:20Z to 22:29:22Z (27 min). The anchor is the generation timestamp in `Date`, not the request-arrival second: the body is regenerated on a ~10–11 s cadence and reused inside that window, so a stamp can lag the client clock by 18 s. The interval never varied; the hypothesis is not refuted.

## Timed observations (UTC; offset = body `Expires` − response `Date`)

| # | request (local clock) | `Date` | body `Expires` | offset (s) | ETag |
|---|---|---|---|---|---|
| S084 | 22:02:20 (retained fetch, receipt `accessedUtc`) | — | `2026-11-21T22:02:20z` | **2 592 000** | — |
| obs1 | 22:25:04.986 | 22:25:05 | `2026-11-21T22:25:05z` | **2 592 000** | `12557be8…` |
| obs2 | 22:26:12.238 | 22:26:12 | `2026-11-21T22:26:12z` | **2 592 000** | `6b74a97b…` |
| obs3 | 22:27:17 | 22:27:17 | `2026-11-21T22:27:17z` | **2 592 000** | `207d7532…` |
| obs4 | 22:28:22 | 22:28:22 | `2026-11-21T22:28:22z` | **2 592 000** | `e3db9aeb…` |
| obs5a/5b | 22:28:22 (same second) | 22:28:22 | `2026-11-21T22:28:22z` | **2 592 000** | `e3db9aeb…` (identical) |
| g1 | 22:28:53 | 22:28:39 | `2026-11-21T22:28:39z` | **2 592 000** | `1b9676e7…` |
| lag1..5 | 22:29:11/16/21/27/32 | 22:28:53, 22:29:11×2, 22:29:22×2 | matches its `Date` | **2 592 000** | `66416fe1…`, `7cf5631d…`×2, `b371180b…`×2 |

`analyze.py` → `github offsets: [2592000 ×7] distinct=1 spread=0s`; `distinct github Expires values: 4 over 7 observations`. Every body is 269 B and differs from retained S084 in **one token**: token-`diff` → exit 1, `14c14`, the `Expires` value only.

## Mechanism, as far as the wire shows

- `ETag` = `W/"sha256(body)[0:32]"` on **10 of 10** bodies (`match=YES`): the validator moves exactly when the stamped body moves.
- Requests inside one second return byte-identical bodies; bodies cluster into ~10–11 s generations (22:29:11→`66416fe1`, 16 and 21→`7cf5631d`, 27 and 32→`b371180b`).
- Conditional GET with a superseded validator (`If-None-Match: W/"207d…"`) → `200` + fresh body (obs6); with the current one (`W/"e3db…"`) → `304`, no body (obs7), whose `Date` still read 22:28:22. Every response says `Cache-Control: max-age=0, private, must-revalidate`, so the reuse sits at or in front of the origin; I cannot separate them.

## Google contrast (one GET, 22:25:15Z, 200, 275 B)

Body `Expires: 2030-04-01T00:00:00z` is static: 108 524 085 s = **1 256.07 days** past its `Date` (3.4 years ahead, 2.5× the RFC's one-year recommendation); `Last-Modified: Tue, 01 Apr 2025 12:00:00 GMT`, no `ETag`. Its HTTP-level `Expires:` **header** equals `Date` — a cache directive, unrelated to the field, which lives only in the body. Token-`diff` vs retained S085 → 0; `cmp -l` → 6 positions, all space-vs-newline.

## Commands run (exit codes)

1. `mkdir -p /fast/scratch/hyaku/kake-r35/w1/ScoutGithubExpiresDynamic` → 0.
2. `curl -sS --http1.1 -D obs1.headers -o obs1.body -w 'http_code=%{http_code} …' https://github.com/.well-known/security.txt` → 0, 200; same on `https://www.google.com/.well-known/security.txt` → 0, 200.
3. Series at NOW+45/+110/+175 s plus two same-second GETs (`obs2`…`obs5b`) → 0, wall 175.29 s.
4. `python3 -B analyze.py` → 0 (figures above; script kept in the sandbox).
5. `diff <(tr ' ' '\n' < …/round-35/sources/S084.txt) <(tr ' ' '\n' < obs1.body)` → **1**, one token. Token `diff` of google body vs `S085.txt` → 0; `cmp -l S085.txt google.body` → 1, whitespace only.
6. `curl … -H 'If-None-Match: W/"207d…"'` → 200 (`obs6`); `… W/"e3db…"'` → **304** (`obs7`; `stat obs7.body` fails — a 304 carries no body, expected).
7. Five-sample lag loop, 5 s apart → curl work 0; shell exit **1** only from the trailing `[ $i -lt 5 ] && sleep 5` being false on the last iteration (no data effect).
8. ETag-vs-`sha256` loop over 10 saved bodies → 0, `match=YES` ×10; `python3` character windows over `S078.txt` (whitespace-collapsed to one line) → 0.

## RFC 9116 ground truth (S078) and the static-publisher consequence

- §2.5.5 @13266–13748: `Expires` is the instant after which the data "is considered stale and should not be used"; RFC 3339 format; "RECOMMENDED that the value ... be less than a year into the future"; "MUST always be present and MUST NOT appear more than once". The RFC's own examples write lowercase `z`, as GitHub and Google do.
- §3 @15937: organizations "MUST place" the file under `/.well-known/`. A static Pages build cannot stamp per request, so a publisher picks a fixed far-future value (Google's shape, past the <1-year RECOMMENDED — 1 256 d) or one refreshed per build/deploy (scheduled Actions build); only presence and single-use are MUSTs, so either shape is conformant.
- The dot-directory needs an override: S006 @2919 — Jekyll skips files or folders that "Start with `_`, `.`, or `#`", `include` being the escape hatch; S080 @2742 — `Include` "Force inclusion of directories and/or files ... .htaccess is a good example since dotfiles are excluded by default", and in Jekyll 4 user `include` entries override the default exclusions.

## Unknowns / not verified

- Origin memoization vs a shared edge cache (~10–11 s reuse) is indistinguishable from one client; `Cache-Control: private` argues against a conforming shared cache — [INFERENCE]. Whether the stamp is per request then reused, or once per generation, cannot be separated: both give a constant offset, and the anchor I can see is the generation second.
- One vantage point, no other regions, no HEAD, no authenticated or canary probes; Google sampled once live (its static nature also rests on S085). GitHub's implementation was not inspected — the 30-day constant is observed wire behavior, not an RFC 9116 requirement. Not scored by any counter here.
