# SrcS036Thresholds — S036 web.dev "Web Vitals" source opening

Seat: KakeR28a3.SrcS036Thresholds (leaf scribe, C2 freshness).
Target: S036 https://web.dev/articles/vitals — CWV set, per-metric thresholds, percentile/device assessment.

## Fetch (GET)

Command:
```
date -u +"%Y-%m-%dT%H:%M:%SZ"; curl -sS -L --max-time 60 -D headers.txt -o vitals.html -w "http=%{http_code} size=%{size_download} time=%{time_total}\n" https://web.dev/articles/vitals
```
Observed output:
```
2026-10-22T09:29:10Z
http=200 size=143746 time=1.007234
curl_exit=0
```
Headers (HTTP/2): 200 OK; content-type: text/html; charset=utf-8; last-modified: Thu, 31 Oct 2024 07:00:00 GMT; server: Google Frontend; date: Thu, 22 Oct 2026 09:29:11 GMT.
Fetched-bytes SHA-256: dc42735f2413bdd7f04fb4b2149bbd733dc1d5790dad0b46a5de9721677b0c24
Scratch artifacts: /fast/scratch/hyaku/kake-r28a3/w1/SrcS036Thresholds/{vitals.html, headers.txt, vitals.txt}

## Verification method

HTML->text extraction (Python html.parser: block-tag newlines, space-run collapse). Every quote below was re-checked verbatim against that rendered stream, and, where it survives tag-stripping, against the raw bytes; contiguous raw-HTML matches are noted. Offsets are byte offsets in vitals.txt (rendered stream) / vitals.html (raw HTML). All quotes are at most 25 words.

## Statements — what this page itself says

Anchor: every quote below lies in the H2 "Core Web Vitals" section (text offsets 5479–7145; the "Lifecycle" H3 begins at 7145).

1. Set scope. (a) Core Web Vitals are a subset of Web Vitals that apply to every web page and should be measured by all site owners.
   (b) "Core Web Vitals are the subset of Web Vitals that apply to all web pages, should be measured by all site owners" (22 w; txt 5497; html 101624, contiguous).
   (c) Anchor: Core Web Vitals.
2. Set composition. (a) The current set covers loading, interactivity, and visual stability; the page enumerates those metrics as LCP, INP, and CLS (each in its own card, all three listed "Stable" in the Lifecycle section).
   (b) "The current set focuses on three aspects of the user experience—loading, interactivity, and visual stability—and includes the following metrics (and their respective thresholds):" (23 w; txt 5904; raw HTML split by inline tags).
   (c) Anchor: Core Web Vitals.
3. LCP threshold. (a) For a good user experience LCP should occur within 2.5 seconds of when the page first starts loading.
   (b) "To provide a good user experience, LCP should occur within 2.5 seconds of when the page first starts loading." (19 w; txt 6227; html 103198, inline <strong> splits the tag).
   (c) Anchor: Core Web Vitals.
4. INP threshold. (a) For a good user experience pages should have an INP of 200 milliseconds or less (page wording: "a INP").
   (b) "To provide a good user experience, pages should have a INP of 200 milliseconds or less." (16 w; txt 6395).
   (c) Anchor: Core Web Vitals.
5. CLS threshold. (a) For a good user experience pages should maintain a CLS of 0.1 or less.
   (b) "To provide a good user experience, pages should maintain a CLS of 0.1. or less." (15 w; txt 6542; the doubled period after 0.1 is verbatim).
   (c) Anchor: Core Web Vitals.
6. Percentile and device segmentation. (a) The measurement point for these targets is the 75th percentile of page loads, segmented across mobile and desktop devices.
   (b) "a good threshold to measure is the 75th percentile of page loads, segmented across mobile and desktop devices." (18 w; txt 6713; html 103877, inline <strong> splits).
   (c) Anchor: Core Web Vitals.
7. Pass criterion. (a) A page passes compliance if it meets the recommended targets at the 75th percentile for all three Core Web Vitals metrics.
   (b) "should consider a page passing if it meets the recommended targets at the 75th percentile for all three of the Core Web Vitals metrics." (24 w; txt 6870; html 104058, contiguous).
   (c) Anchor: Core Web Vitals.

## Not found on this page

- Good / needs-improvement / poor three-band thresholds: NOT present ("needs improvement" and "poor" have zero hits). The page gives a single recommended target per metric; "Defining the Core Web Vitals metrics thresholds" is a link to another page, not content.
- Origin-level assessment: the word "origin" does not appear; the assessment language is page-level only.
- Threshold statements do not carry lab-vs-field framing (lab/field appear only in the tooling sections, outside these claims).

## Last-updated

Page displays "Last updated: October 31, 2024" (txt 4524); JSON-LD dateModified "2024-10-31"; HTTP Last-Modified Thu, 31 Oct 2024 07:00:00 GMT. Published May 4, 2020.

## Proposed registry row (SOURCES.md shape)

| S036 | https://web.dev/articles/vitals (last updated 2024-10-31) | docs | A | Core Web Vitals set definition, per-metric recommended targets (LCP/INP/CLS), and the 75th-percentile mobile/desktop page-assessment rule as stated on this overview page | "Core Web Vitals" section, metric cards and follow-on paragraphs; fetched 2026-10-22 | CWV = LCP+INP+CLS subset applying to all web pages; recommended targets: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1; pages are assessed at the 75th percentile of page loads segmented across mobile and desktop devices for all three metrics; the page gives no good/needs-improvement/poor bands and no origin-level rule | mined | 2026-10-22 | 90d | corpus/knowledge/field-performance-cwv.md |

## Notes

- No tools installed or updated (none needed; no pacman). Scratch only under /fast/scratch/hyaku/kake-r28a3/w1/SrcS036Thresholds/ with TMPDIR set there.
- Network: single GET to S036; no API keys, no CrUX/PageSpeed calls, no other sites fetched or referenced.
- Nothing else was written or mutated in the lane repo; this report is the only file I wrote there.
- Not verified: I did not build the field-performance-cwv.md knowledge entry or run any counter; this report is advisory input for the L1.
