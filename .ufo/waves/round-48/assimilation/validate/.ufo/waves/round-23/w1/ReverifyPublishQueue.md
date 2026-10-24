## Verdict

C1 `publish-queue` scoped re-verification: **3 HOLD, 3 STALE** across six selected claims. The anchors were checked against the frozen base; this is an author-side receipt, not independent admission or a whole-ledger pass.

## Findings

- **P2 — PQ-12 live marker is stale (freshness).** The source asserts `2026-09-29 scribe beat`, while the live GET body contains `2026-09-30 scribe beat`. Smallest fix: append the dated correction in the C1 round-23 section. Command: `d=$(mktemp -d /tmp/kake-r23-ReverifyPublishQueue-XXXX) && curl --connect-timeout 15 --max-time 45 -sSL -o "$d/charter-ghp.html" -w 'final_http=%{http_code} bytes=%{size_download} redirects=%{num_redirects} url=%{url_effective}\n' https://veigapunk.github.io/charter-ufo-fsd/ && sha256sum "$d/charter-ghp.html"`; observed `final_http=200 bytes=53660 redirects=0 url=https://veigapunk.github.io/charter-ufo-fsd/` and SHA-256 `7c243a1d81357cdee71520034a05d540bfe8f69c702a7a1c95f8a0bfa5237aba`. `grep` over the downloaded GET body matched line 317 beginning `2026-09-30 scribe beat (`.
- **P2 — PQ-12 config-pin presence is stale (freshness).** `/home/vgpnk/Projects/webzites/fleet/fleet.config.json` is absent, so the cited line-256 pin is not present at its claimed surface. Smallest fix: append the dated correction in the C1 round-23 section. The read-only `test -e` sweep output was `absent /home/vgpnk/Projects/webzites/fleet/fleet.config.json`.
- **P2 — PQ-2 canonical endpoint statuses are stale (freshness).** The unit says `ds4cc.com/sitemap.xml` and `/robots.txt` are live 404s; both now return HTTP 200. Smallest fix: append the dated correction in the C1 round-23 section. GET observations: sitemap `http=200 bytes=7565 redirects=0 redirect= url=https://ds4cc.com/sitemap.xml`; robots `http=200 bytes=62 redirects=0 redirect= url=https://ds4cc.com/robots.txt`.

The required receipt follows. Its anchors are byte-for-byte substrings of the unit at base `b5d599e19bead54b96f589444e9ec64cdf67c28a`.

```json
{
  "unit": "publish-queue",
  "path": "/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/publish-queue.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "sources absent after the 2026-10-12 prune.",
      "claim": "The cited historical webzites report, dedupe report, and scribe ledger remain absent on disk.",
      "surface": "/home/vgpnk/Projects/webzites/reports/r9-publish-queue.md; /home/vgpnk/Projects/webzites/fleet/fleet.dedupe-report.md; /home/vgpnk/Projects/origin-work/ufo-fsd-alpha/.ufo/charter-scribe/ledger.jsonl",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/webzites/reports/r9-publish-queue.md\nabsent /home/vgpnk/Projects/webzites/fleet/fleet.dedupe-report.md\nabsent /home/vgpnk/Projects/origin-work/ufo-fsd-alpha/.ufo/charter-scribe/ledger.jsonl",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "charter-ufo-fsd.kimi.page, plazir15.kimi.page → 404; plazir27.kimi.pro → preview-404",
      "claim": "The three named queue URLs still return two hard 404s and a redirect to Kimi's preview-404 page.",
      "surface": "https://charter-ufo-fsd.kimi.page/; https://plazir15.kimi.page/; https://plazir27.kimi.pro/",
      "method": "GET",
      "observation": "http=404 bytes=13409 redirects=0 redirect= url=https://charter-ufo-fsd.kimi.page/\nhttp=404 bytes=13409 redirects=0 redirect= url=https://plazir15.kimi.page/\nhttp=302 bytes=72 redirects=0 redirect=https://statics.kimi.ai/pages/preview-404-en.html url=https://plazir27.kimi.pro/",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "GET https://charter-ufo-fsd.kimi.page/` → HTTP **404**",
      "claim": "The charter-ufo-fsd Kimi slug root remains HTTP 404 with the watch's sentinel bytes and digest.",
      "surface": "https://charter-ufo-fsd.kimi.page/",
      "method": "GET",
      "observation": "final_http=404 bytes=13409 redirects=0 url=https://charter-ufo-fsd.kimi.page/\n93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966  /tmp/kake-r23-ReverifyPublishQueue-xbtM/pq5.html",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "live `2026-09-29 scribe beat (`",
      "claim": "The live charter-ghp page carries the 2026-09-29 scribe-beat marker.",
      "surface": "https://veigapunk.github.io/charter-ufo-fsd/",
      "method": "GET",
      "observation": "final_http=200 bytes=53660 redirects=0 url=https://veigapunk.github.io/charter-ufo-fsd/; SHA-256 7c243a1d81357cdee71520034a05d540bfe8f69c702a7a1c95f8a0bfa5237aba; downloaded GET body, line 317: `<p class=\"thread-note rv\" data-i18n=\"s3.scribeBeat\">2026-09-30 scribe beat (`.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, GET https://veigapunk.github.io/charter-ufo-fsd/ serves the literal `2026-09-30 scribe beat (`, not `2026-09-29 scribe beat (`."
    },
    {
      "id": "c1",
      "anchor": "pin `2026-09-26 scribe beat` (`fleet.config.json:256`,",
      "claim": "The config-of-record path contains the cited 2026-09-26 scribe-beat pin at line 256.",
      "surface": "/home/vgpnk/Projects/webzites/fleet/fleet.config.json",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/webzites/fleet/fleet.config.json",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, `/home/vgpnk/Projects/webzites/fleet/fleet.config.json` is absent, so the cited line-256 `2026-09-26 scribe beat` pin is not present at its claimed surface."
    },
    {
      "id": "c1",
      "anchor": "ds4cc.com/sitemap.xml` and\n  `/robots.txt` are **live 404** (9,379B GH-Pages 404)",
      "claim": "The canonical sitemap and robots endpoints are live HTTP 404s.",
      "surface": "https://ds4cc.com/sitemap.xml; https://ds4cc.com/robots.txt",
      "method": "GET",
      "observation": "http=200 bytes=7565 redirects=0 redirect= url=https://ds4cc.com/sitemap.xml\nhttp=200 bytes=62 redirects=0 redirect= url=https://ds4cc.com/robots.txt",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, GET https://ds4cc.com/sitemap.xml returned HTTP 200 (7,565 bytes) and GET https://ds4cc.com/robots.txt returned HTTP 200 (62 bytes), not HTTP 404."
    }
  ]
}
```

## Checked and held

- The local-source absence claim is held: the report, dedupe file, and ledger paths in receipt row 1 all returned `absent` from the read-only existence sweep.
- The three explicit dead-slot destinations in PQ-1 were fetched directly; the two 404s and the preview-404 redirect still match their listed states.
- PQ-5's slug root still returns HTTP 404, 13,409 bytes, SHA-256 `93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966`.
- Anchor basis check: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --quiet b5d599e19bead54b96f589444e9ec64cdf67c28a -- corpus/knowledge/publish-queue.md` printed `publish-queue.md matches base b5d599e19bead54b96f589444e9ec64cdf67c28a`.

## Limits

Skipped claims and why:

- **PQ-1 aggregate `3 of 10` and current PROPERTIES membership:** only the three specifically named target URLs were fetched; the full current 10-URL member set was not re-derived, so no aggregate count is claimed.
- **PQ-2 mirror coverage (19/93 served, 74/75 missing), per-URL transitions, mirror vintage, chat identity, and unpushed-commit count:** the source URL universe and `ds4cc-marketplace` checkout are not available here; the public sitemap/robots statuses alone cannot establish those counts or the source/live delta.
- **PQ-3, PQ-4, PQ-6:** chat binding, card/version state, and publish/fire history were not probed; no Kimi chat/API interaction or publishing action was used.
- **PQ-5 preview-card, `probe-latest.json`, vault membership/dead-link count, and fire-history assertions:** only the public slug URL was checked; the local fleet/history evidence is absent and no chat/browser session was accessed.
- **PQ-7:** the NXDOMAIN/DNS registration tripwire was not rechecked; it was outside the selected six claims.
- **PQ-8 and PQ-13:** these are a decision and a conditional canary check; no PQ-8 decision/action occurred, so no PQ-13 verification was triggered.
- **PQ-9 and PQ-10:** code/config behavior and mutation-count claims require the missing webzites source/config files; no source-code assertion was made.
- **PQ-11:** the source provenance and 63KB artifact claim require the unavailable source artifacts.
- **PQ-12 loop classifications, timer/sweep recency, remote HEAD, and scribe-ledger counts:** only the public beat literal and cited config path were checked; the config, clone, and ledger are absent.
- **PQ-14:** source branch divergence and per-path live/source comparisons require the absent `plazir-15-site` checkout; no current source tree was available to compare with its live page.

All public observations were unauthenticated GETs. No writes, publishing, deployment, DNS actions, tools installs, builds, linters, or tests were performed. This receipt rechecks six selected claims only; remaining ledger claims are not thereby refreshed.
