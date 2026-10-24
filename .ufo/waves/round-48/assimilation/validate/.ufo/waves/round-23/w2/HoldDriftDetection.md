## Verdict

**Counterexample found.** None of the assigned HOLD claims (c1, c2, c3, c5, c6) is falsified by the fresh read-only checks; each verdict still holds. However, the selection skips the more load-bearing r16 `plazir15-ghp` live-vs-source evidence in `corpus/knowledge/drift-detection.md:71-91`. Its live-side values have since changed on surfaces that are still publicly probeable. The c5 receipt also records an incorrect exact h1 literal, although its underlying “page still serves” HOLD is true.

There are no UNVERIFIABLE rows in this unit's receipt: it contains c1/c2/c3/c5/c6 as HOLD and c4 as STALE. Thus no requested UNVERIFIABLE claim remains to assess for a live-decidable surface.

## Findings

### P2 — Receipt selection skips a more load-bearing, live-decidable r16 finding

**Affected axis:** freshness / claim selection. `corpus/knowledge/drift-detection.md:71-91` calls the r16 quantified sweep out as the source of the plazir15-ghp drift finding and says it corrected the cross-file `sitemap-orphan-audit.md` arithmetic. This is materially more load-bearing than the selected status checks: it identifies sitemap-vs-source divergence and feeds the 103-vs-102 baseline correction. The dated 2026-09-29 observations remain historical evidence; this finding does not claim they were false at that time. It identifies their changed live state and the lack of a current round-23 update.

Exact current probe:

```text
$ cd /tmp/kake-r23w2-HoldDriftDetection-4uOH && curl -sS --max-time 30 -o plazir15-sitemap.xml -w 'code=%{http_code} size=%{size_download} type=%{content_type} url=%{url_effective}\n' https://veigapunk.github.io/plazir-15-site/sitemap.xml
code=200 size=1144 type=application/xml url=https://veigapunk.github.io/plazir-15-site/sitemap.xml
```

The fetched XML has 7 `<loc>` entries and no `/tetris/` entry (the seven URLs are `/`, `/snake/`, `/1337b/`, `/siduri/`, `/speedrun/`, `/512qa/`, and `/iqrunway/`). The r16 table at line 79 recorded 8 entries including `/tetris/`; lines 87-90 carry the resulting 103-vs-102 arithmetic. Direct live probes show this is sitemap membership drift, not route death: `/tetris/` still returns HTTP 200 and 1,650 bytes.

Two other live-side values in that same table have also changed. Exact probe outputs:

```text
$ cd /tmp/kake-r23w2-HoldDriftDetection-4uOH && for p in tetris snake speedrun 1337b siduri 512qa iqrunway; do curl -sS --max-time 20 -o "sub-$p.out" -w "$p code=%{http_code} size=%{size_download} url=%{url_effective}\n" "https://veigapunk.github.io/plazir-15-site/$p/"; done; curl -sS --max-time 20 -o snake.html -w 'snake.html code=%{http_code} size=%{size_download}\n' https://veigapunk.github.io/plazir-15-site/snake/index.html; curl -sS --max-time 20 -o speedrun.html -w 'speedrun.html code=%{http_code} size=%{size_download}\n' https://veigapunk.github.io/plazir-15-site/speedrun/
tetris code=200 size=1650 url=https://veigapunk.github.io/plazir-15-site/tetris/
snake code=200 size=8013 url=https://veigapunk.github.io/plazir-15-site/snake/
speedrun code=200 size=5048 url=https://veigapunk.github.io/plazir-15-site/speedrun/
1337b code=200 size=14751 url=https://veigapunk.github.io/plazir-15-site/1337b/
siduri code=200 size=11484 url=https://veigapunk.github.io/plazir-15-site/siduri/
512qa code=200 size=55510 url=https://veigapunk.github.io/plazir-15-site/512qa/
iqrunway code=200 size=6454 url=https://veigapunk.github.io/plazir-15-site/iqrunway/
snake.html code=200 size=8013
speedrun.html code=200 size=5048
```

The fetched `snake/index.html` now contains `<meta property="og:url" content="https://veigapunk.github.io/plazir-15-site/snake/" />` (r16 recorded 0 live hits); `speedrun/` now contains `<link rel="canonical" href="https://ds4cc.com/speedrun/" />` (r16 recorded the plazir self-canonical as live). The current local source tree is absent, so these live GETs cannot establish source-to-live synchronization or a new unpushed-commit count.

**Smallest fix:** add a round-23 live-side claim/correction for the currently served sitemap count and changed live metadata, while explicitly retaining the 2026-09-29 results as dated history. Re-label the 103-vs-102 arithmetic as historical; do not assert a current cross-source total or source comparison without restored source evidence. The current `sitemap-orphan-audit` receipt independently marks its 8-loc claim STALE, but that does not update this unit's skipped r16 observation.

### P3 — c5 observation overstates the exact h1 literal

**Affected claim:** drift-detection:c5 observation (the page-serving HOLD itself still holds). The receipt says the body includes literal `<h1>lucario</h1>`. Fresh response has `<h1>lucario<span>.</span></h1>` instead, so the exact literal cited in the observation is absent.

Exact request output:

```text
$ cd /tmp/kake-r23w2-HoldDriftDetection-4uOH && curl -sS --max-time 30 -o lucario.html -w 'code=%{http_code} size=%{size_download} type=%{content_type} url=%{url_effective}\n' https://veigapunk.github.io/lucario/ && sha256sum lucario.html
code=200 size=3435 type=text/html; charset=utf-8 url=https://veigapunk.github.io/lucario/
bee2d9f5b5777768e69a5b9aaa9c28dfcc4107f57a4dfb6ec8726d9685c46cff  lucario.html
```

Exact body literals: `<title>lucario</title>` and `<h1>lucario<span>.</span></h1>`.

**Smallest fix:** correct the observation to the literal h1 actually served, or omit that marker. Do not change c5's HOLD verdict.

## Checked and held

- **c1:** Re-ran `test -e` on both exact paths. Output: `webzites test -e rc=1`; `plazir-15-site test -e rc=1`. Both paths are absent. The `~/Projects` directory listing and a bounded name sweep found no migrated `webzites` or `plazir-15-site` tree. HOLD stands.
- **c2:** `curl -sS --max-time 30 -o ufofsd.html -w 'code=%{http_code} size=%{size_download} type=%{content_type} url=%{url_effective}\n' https://ufo-fsd.kimi.pro && sha256sum ufofsd.html` returned `code=200 size=612 type=text/html; charset=utf-8 url=https://ufo-fsd.kimi.pro/` and SHA-256 `1df92e30ba5a76e69a863a729326949871d3d83e290935d596f6cd9b7d65ab8`. The fetched body contains `<title>DS4CC</title>`, `/assets/index-Bw9NLFv4.js`, and `<div id="root"></div>`. HOLD stands.
- **c3:** `curl -sS -I --max-time 30 https://ufo-fsd.kimi.pro` returned `HTTP/2 403` and `content-type: application/json; charset=utf-8` (HEAD request exited 0 as a completed curl request). HOLD stands.
- **c5:** the same fresh GET returned HTTP 200 / 3,435 bytes and the `lucario` title; the page is served. HOLD stands, subject to the P3 exact-observation correction above.
- **c6:** `curl -sSL --max-time 30 ... https://plazir15.kimi.page` returned `plazir15 code=404 size=13409 type=text/html; charset=utf-8 url=https://plazir15.kimi.page/ redirects=0`; the same request for `https://charter-ufo-fsd.kimi.page` returned `charterufsd code=404 size=13409 type=text/html; charset=utf-8 url=https://charter-ufo-fsd.kimi.page/ redirects=0`. Both HOLDs stand.
- The working tree HEAD was `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd`; `git --no-optional-locks diff --stat 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd -- corpus/knowledge/drift-detection.md .ufo/waves/round-23/receipts/drift-detection.json` produced no diff, so these reads targeted the frozen candidate.

## Limits

Only unauthenticated public GET/HEAD and read-only local path checks were used. The absent source trees prevent a fresh local source-vs-live comparison; no inference about their present content or publishing state is made. The `measure_c1.py` unit checker validates receipt fields, base-revision anchors, appended-section citations/corrections, and presence of at least one HOLD/STALE; it does not assess relative claim importance or verify that the receipt selected the most load-bearing live-decidable claims, so it cannot catch the P2 selection gap.