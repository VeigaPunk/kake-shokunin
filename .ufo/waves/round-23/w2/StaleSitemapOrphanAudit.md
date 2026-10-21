## Verdict

Counterexample found: one P3 wording ambiguity in c6. The marker correction is substantively right, but its shortened negative literal can be read more broadly than the evidence supports. No P1 wrong-correction finding.

## Findings

### P3 — c6 correction should name the marker it negates

**Evidence / exact checks**

```sh
curl -sS -o /tmp/kake-r23w2-StaleSitemapOrphanAudit-fK3b/charter-home.html -w 'code=%{http_code} bytes=%{size_download} redirect=%{redirect_url} url=%{url_effective}\n' https://veigapunk.github.io/charter-ufo-fsd/
```

```text
code=200 bytes=53660 redirect= url=https://veigapunk.github.io/charter-ufo-fsd/
```

The marker-specific checks returned:

```text
marker-2026-09-30: 1
marker-2026-09-28: 0
other-2026-09-28: 1
```

The extra `2026-09-28` occurs in an unrelated historical entry (`<span class="ldate">2026-09-28</span>`, homepage markup around line 578 of the captured response); the `data-i18n="s3.scribeBeat"` marker is 2026-09-30. The correction in `corpus/knowledge/sitemap-orphan-audit.md:138` says “not the `2026-09-28` literal,” which is accurate when read as shorthand for the scribe-beat marker, but can imply that the date literal is absent from the entire homepage. This is a scope ambiguity, not a false result about the marker.

**Impacted claim/axis:** `sitemap-orphan-audit:c6`, freshness. The stale marker claim is corrected, but the correction sentence's negation is broader/less explicit than its evidence.

**Smallest fix:** say “not the `2026-09-28 scribe beat` marker” (or “not the `s3.scribeBeat` value `2026-09-28 ...`”).

## Checked and held

- **c1 — genuinely stale; correction true and appropriately scoped.** Exact GET command:
  ```sh
  curl -sS -o /tmp/kake-r23w2-StaleSitemapOrphanAudit-fK3b/plazir-sitemap.xml -w 'code=%{http_code} bytes=%{size_download} redirect=%{redirect_url} url=%{url_effective}\n' https://veigapunk.github.io/plazir-15-site/sitemap.xml
  ```
  Output: `code=200 bytes=1144 redirect= url=https://veigapunk.github.io/plazir-15-site/sitemap.xml`; `<loc>` count: `7`. The captured XML has seven entries, so “7 <loc> entries, not 8” is complete for the count claim and does not assert sitemap completeness. Separately, the c5 route probe returned `tetris code=200 bytes=1650 redirect=`; `/tetris/` is not one of those seven locs. This does not make c1's count correction false, but the count is not a claim that every live route is listed.

- **c3 — genuinely stale; correction true and complete for the endpoint-status/count claim.** Exact GET command:
  ```sh
  curl -sS -o /tmp/kake-r23w2-StaleSitemapOrphanAudit-fK3b/ds4cc-sitemap.xml -w 'code=%{http_code} bytes=%{size_download} redirect=%{redirect_url} url=%{url_effective}\n' https://ds4cc.com/sitemap.xml
  ```
  Output: `code=200 bytes=7565 redirect= url=https://ds4cc.com/sitemap.xml`; `<loc>` count: `96`. The 96 locs are distinct and all use `https://ds4cc.com/`. This reproduces the receipt and supports the correction replacing the 404 claim.

- **c4 — stale as a current-path presence claim; correction accurately limits itself to that path.** Exact check:
  ```sh
  test -e /home/vgpnk/Projects/ds4cc-marketplace/sitemap.xml && echo PRESENT || echo ABSENT; test -d /home/vgpnk/Projects/ds4cc-marketplace && echo DIR-PRESENT || echo DIR-ABSENT
  ```
  Output: `ABSENT` and `DIR-ABSENT`. A Git HEAD check could not be run because the cited checkout is absent:
  ```sh
  git -C /home/vgpnk/Projects/ds4cc-marketplace rev-parse --verify HEAD
  ```
  Output: `fatal: cannot change to '/home/vgpnk/Projects/ds4cc-marketplace': No such file or directory` (exit 128). The correction's “absent ... at that path” wording is true and not an assertion about some other checkout; the underlying Git-tree content of a local HEAD is not established by the unavailable checkout.

- **c6 — stale marker claim reproduced; apart from the P3 wording ambiguity above, correction is substantively accurate.** The `s3.scribeBeat` value is 2026-09-30 with `(the-scribe via local-fallback)`; the exact 2026-09-28 scribe-beat marker is absent. The unrelated historical date occurrence means the correction should not be read as claiming that the token `2026-09-28` occurs nowhere on the page.

- **c7 — genuinely stale; correction true and complete for the three-row 404 claim.** Exact GET probes and outputs:
  ```sh
  curl -sS -o /dev/null -w 'plazir15.kimi.page code=%{http_code} bytes=%{size_download} redirect=%{redirect_url}\n' https://plazir15.kimi.page/
  curl -sS -o /dev/null -w 'charter-ufo-fsd.kimi.page code=%{http_code} bytes=%{size_download} redirect=%{redirect_url}\n' https://charter-ufo-fsd.kimi.page/
  curl -sS -o /tmp/kake-r23w2-StaleSitemapOrphanAudit-fK3b/lucario-home.html -w 'lucario code=%{http_code} bytes=%{size_download} redirect=%{redirect_url}\n' https://veigapunk.github.io/lucario/
  ```
  Outputs: `plazir15.kimi.page code=404 bytes=13409 redirect=`; `charter-ufo-fsd.kimi.page code=404 bytes=13409 redirect=`; `lucario code=200 bytes=3435 redirect=`. The 200 body has `<title>lucario</title>` and `engine.py` references, supporting that this is the Lucario page rather than an unrelated success response. Thus the two Kimi rows remain 404 while Lucario is not in the dead-404 set.

## Limits

All web probes were read-only direct GETs with no redirects reported; all five receipt observations reproduced on 2026-10-21. The c4 checkout itself is missing, so only the cited filesystem path's absence was verified, not the contents of a Git HEAD object. No tools were installed.