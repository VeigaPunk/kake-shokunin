# RowS015 — round 26 freshness recheck

Seat: `KakeR25.RowS015-6`. Row: `corpus/SOURCES.md:23` (S015, tier A, kind docs, cadence 90d).
Source re-fetched this round: `#1 https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits` — HTTP 200, fetchedAt `2026-10-21T15:10:41Z`, body sha256 `e5e9c38f4d09a286ed2d06609c678097da8771c322025b875ea50f41dc2f5014` (88,733 B), text view `fetched/text/S015-1.txt` sha256 `64a9b04b9b5f79f3ee99876a0a01cff33f1bd6478ad71184100fb91e06845ff7` (4,037 B).

```json
{"id":"S015","verdict":"HOLD","fetchIndex":1,"quote":"Published GitHub Pages sites may be no larger than 1 GB.","anchorObserved":"\"Usage limits\" section heading, bullet list of usage limits (single-line text view line 1)","reason":"The re-fetched page still carries the 1 GB published-site cap in its Usage limits section, so the row's scope (published-site size and platform usage limits), anchor (Usage limits) and teaches all still hold; the neighbouring limits (10-minute deploy timeout, 100 GB/month soft bandwidth, 10 builds/hour) also persist.","correction":null}
```

Caveats (≤10 lines):

- Living docs URL, no commit/tag pin: this tests content drift plus availability, not an immutable artifact.
- Source wording "may be no larger than 1 GB" is semantically identical to the row's "limited to 1 GB"; no version/date pin is asserted by the row, so nothing became stale.
- `last-modified` and `etag` were absent in the fetch response; freshness rests on the 2026-10-21 body bytes and digest above.
- Row cells unchanged; no correction and no `[r26-recheck S015 STALE]` block required.
- No tools installed or updated; no builds/tests/linters run; only this report written.
