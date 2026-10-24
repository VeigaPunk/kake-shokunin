# W2 ReviewEntryExamples — the C2 entry's S084/S085 ("two live files") sentences

Seat: KakeR35.ReviewEntryExamples (falsify). Attacked: every sentence in
`corpus/knowledge/security-txt-publishing.md` section "The two live files" (and the
header's S084/S085 hashes), checked against the retained bodies
`.ufo/waves/round-35/sources/S084.txt|S085.txt|S084.html.gz|S085.html.gz`, receipts.json,
wave-1 reports `w1/ScoutGithubExpiresDynamic.md` and `w1/ScoutSecurityTxtCensus.md`, and
one fresh GET per file today (2026-10-22 ~23:00Z). Lane untouched except this report.
No tools installed or updated.

## Verdict: entry HOLDS on every checked sentence — falsifier not triggered

Retained-body sentences (entry vs `sources/S084.txt` / `S085.txt`, sha-verified):

| # | Entry sentence (abbrev.) | Verdict | Evidence |
|---|---|---|---|
| G1 | one `Contact` (`https://hackerone.com/github`) | HOLDS | S084.txt:1 — exactly one Contact line |
| G2 | `Acknowledgments`, `Preferred-Languages: en`, `Canonical`, `Policy`, `Hiring` | HOLDS | S084.txt:1, all five present, `en` exact |
| G3 | `Expires: 2026-11-21T22:02:20z` ~1 month out at 2026-10-22, inside year [INFERENCE] | HOLDS | S084.txt:1 stamp exact; 30 days; receipts.json:87 `accessedUtc 2026-10-22T22:02:20Z` + 2,592,000 s = the stamp |
| G4 | GitHub has no `Encryption` | HOLDS | S084.txt:1, absent (269 B, 7 fields) |
| K1 | two `Contact`, `https://` first, `mailto:` second | HOLDS | S085.txt:1 (g.co/vulnz, then mailto:security@google.com) |
| K2 | `Encryption`, `Acknowledgments`, `Policy`, `Hiring` | HOLDS | S085.txt:1, all present |
| K3 | `Expires: 2030-04-01T00:00:00z` | HOLDS | S085.txt:1 exact |
| K4 | first line preferred (S078) | HOLDS | order as claimed; attribution to RFC, body matches |
| K5 | ~3.5 years out, past recommendation [INFERENCE] | HOLDS | 1256 d = 3.44 y > 365 d RECOMMENDED (matches census +1256.1 d) |
| K6 | no `Canonical`, no `Preferred-Languages` | HOLDS | S085.txt:1, both absent |
| S1 | neither opens with PGP header; both begin `Contact:` | HOLDS | both raw bodies start `Contact:` |

Header hash claims: `sha256sum` S084.txt = `35cf4b7ba43d9e84afaf5b56e145de6fe10758a82f794d46ac75ab9be043af58`,
S085.txt = `c7a10ffa520a9d5d344f18464348815482ed0db8f4fb54ebcc5b8c0410e71813` — both equal
the entry's "text sha256" values. Labeled as text, not raw body; correct (receipts.json:89/101
carry the raw-body sha `b5839608…`/`a6a8aa9a…`).

## Fresh GETs today (one each, GET only, no owned host, no bot handling)

Commands (exit 0 each): `mkdir -p …/w2/ReviewEntryExamples/tmp` (first attempt without the
dir failed: cwd missing, retried with absolute path, ok); `bash fetch.sh` (curl `-sS
--http1.1 --max-time 30 -D <h> -o <b>`, timestamps via `date -u`).

- github.com/.well-known/security.txt — 2026-10-22T23:00:11Z, HTTP 200,
  `text/plain; charset=utf-8`, 269 B, sha256 `fb607612607bbff92cbe3c6291a70686137086033c1f705ccee683063e95d707`.
- www.google.com/.well-known/security.txt — 2026-10-22T23:00:13Z, HTTP 200,
  `text/plain`, 275 B, sha256 `a6a8aa9a16b530dc6a0c3b6f18ac69c39e76026b71eb8db7aaeb660d356b6021`
  — **byte-identical to the wave-1 receipt bodySha256** (receipts.json:101) and to
  `gzip -cd S085.html.gz` (`cmp` exit 0, "GOOGLE-BYTE-IDENTICAL"). Every S085 sentence holds unchanged.
- GitHub vs retained raw: `diff` → exit 1, `7c7` only:
  `Expires: 2026-11-21T22:02:20z` → `Expires: 2026-11-21T23:00:11z`. All six other lines identical,
  so G1/G2/G4/S1 hold on the live body too. Response `Date: Thu, 22 Oct 2026 23:00:11 GMT`;
  body Expires = Date + exactly 30 days — confirms w1/ScoutGithubExpiresDynamic's mechanism
  (regenerated per ~10–11 s generation, offset 2 592 000 s constant).

Is the entry still true live? Yes. The quoted stamp is scoped to "GitHub's retained body", and
the live characterization "about a month out at 2026-10-22, inside the year" reproduces on the
fresh fetch (same calendar date 2026-11-21, since today+30d = 2026-11-21). Google is static and
byte-stable. The entry's own falsifier ("a fresh fetch that contradicts a sentence below")
does not fire.

## Findings (advisory; no defect rises to wrong/overstated/harmful)

1. LOW (robustness, not falsehood): the entry quotes GitHub's `Expires` seconds without noting
   they are per-generation (wave-1 report proves it; the entry cites S084 only). Any fresh fetch
   shows a different time-of-day, and from 2026-10-23 the calendar date drifts off the quoted
   `2026-11-21`. Because the sentence is "retained body"-scoped and hedged as "about a month",
   nothing becomes false; a one-clause "(served stamp is per-request, date+30d)" would make the
   entry survive contact with a live body. The recheck trigger "90d" will never see byte-stability
   on S084 — expected, not a defect.
2. INFO: `S084.txt`/`S085.txt` are single-line whitespace-normalized views (newlines→spaces, same
   byte counts 269/275); the byte-faithful artifacts are `S084.html.gz`/`S085.html.gz`. Entry
   header says "retained text", so its labels are honest. Anyone re-diffing against the `.txt`
   must normalize the same way (wave-1 seats did).
3. INFO: Google's HTTP-level `Expires:` header (goog.headers) equals `Date` — cache directive,
   unrelated to the body field, same as wave-1 observed; the entry never conflates them. Good.

## Commands and exit codes (all observed)

1. `mkdir -p /fast/scratch/hyaku/kake-r35/w2/ReviewEntryExamples/tmp` → 0 (earlier attempt with
   `cwd` set to the not-yet-existing dir errored; no side effect).
2. `sha256sum S084.txt S085.txt` + `file`/`gzip -t` + `gzip -cd | head -c 400` in
   `.ufo/waves/round-35/sources` → 0; hashes above; gzip integrity ok.
3. `bash fetch.sh` (two `curl` GETs + `date -u` + `sha256sum` + `wc -c`) → curl exits 0, HTTP 200 both.
4. `diff retained-gh.body gh.body` → 1 (one line, Expires); `cmp retained-goog.body goog.body` → 0.
5. `wc -l S084.txt S085.txt` → 1/1 lines, 269/275 bytes.

## Saved artifacts (sandbox, absolute paths)

- /fast/scratch/hyaku/kake-r35/w2/ReviewEntryExamples/gh.body (github, 2026-10-22T23:00:11Z)
- /fast/scratch/hyaku/kake-r35/w2/ReviewEntryExamples/goog.body (google, 2026-10-22T23:00:13Z)
- same dir: gh.headers, goog.headers, times.txt (start/gh_at/goog_at/end UTC), sha.txt,
  fetch.sh, retained-gh.body, retained-goog.body (decompressed retained raw bodies).

## Not verified / residual risk

- One fetch per host, one vantage point, ~1 h after the wave-1 window; Google stability rests on
  that single GET plus the wave-1 samples. GitHub's field set beyond this one body rests on the
  byte-identical-except-Expires diff, not on independent field enumeration (the diff implies it).
- I did not re-verify S078/S079 RFC claims, the sealed counter, or SOURCES-row prose (other seats);
  rows S084/S085 in SOURCES.md were read only to confirm the entry's scope lines ("live file,
  one ordinary GET" datasets) are consistent — S084 row's "14 words" phrasing was not audited.
- Did not test the root copies (github.com/security.txt, google.com/security.txt); the entry makes
  no claim about them for these hosts.
