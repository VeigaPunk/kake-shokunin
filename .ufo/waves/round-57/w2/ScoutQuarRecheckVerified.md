# ScoutQuarRecheckVerified

Re-checked 2026-10-25 UTC (server `date:` header read 2026-10-26 00:27 GMT), lane HEAD read 51921b97124616d8526160231aec5c5708c74f3d (only wave-1 reports and the register read; no build artifact attacked). One GET per URL, UA `kake-shokunin-round57-recheck`, no API key, no POST. Bodies were kept in a mktemp dir and removed afterwards. Wave-1 reports read: ScoutQuarantineA/B/D. Register: absent-defect-register.md lines 83, 84, 86 (S142/S143/S156, quotes) and line 320 (S178, no quote cell).

PER ROW:
- S142 https://www.kimi.com/help/websites/websites-faq
  - Command: `curl -sS -L --compressed -A <ua> -o s142.html -w '%{http_code}'` -> 200 (confirmed by running). sha256 8823b123... = identical to wave 1's body.
  - Located: `<h2>` "网站链接有效期是多久？会过期吗？", the next `<p>`: `如果用户点击「发布」将网站公开部署，产生的网站链接将始终有效，除非手动点击「取消发布」将网站设为私密，或者内容不适触发举报。`
  - Register quote (`...设为私密。`) occurs 0 times as a substring. Stem `网站链接将始终有效，除非手动点击「取消发布」` occurs 3 times (first `<p>`, plus the embedded RSC/markdown payload copies). The page continues `，或者内容不适触发举报` where the register has `。`.
  - Claim "link stays valid until unpublished": true as the page states it, but there are two exits: manual 取消发布, or content that triggers a report. A summary saying "valid until unpublished" without the report clause overstates it. Confirmed by running.
- S143 https://developer.chrome.com/docs/crux/methodology/tools
  - Command: same curl -> 200. sha256 0f6a18a8... differs from wave 1 (28f1c338...), so the page was re-served. The row is still present.
  - Located, same `<tr>`, the last row of the tools comparison table: `<td><a href="#tool-bigquery">CrUX on BigQuery</a></td> <td>Monthly <a href="#footnote-1"><sup>1</sup></a></td> <td>All metrics (except LCP resource types and subparts)</td> <td>All dimensions</td> <td>Since 2017 <a href="#footnote-5"><sup>5</sup></a></td> <td>Origin</td>`.
  - `(except LCP resource types and subparts)` occurs exactly once (6 units, 40 chars, raw substring). The register's ` — `-joined line is not a raw substring; every cell is present. Confirmed by running.
- S156 https://kimi.page/
  - Command: `curl -sS -D s156a.hdr -o s156a.html https://kimi.page/`, then `sleep 3`, then the same into s156b (no `-L`, no compression). Both 200, HTTP/2.
  - Header in both: `cache-control: private, no-cache, no-store, max-age=0, must-revalidate`. It is the exact register string, byte-identical across the two requests, and the wave-1 value. Also `cf-cache-status: DYNAMIC`, `server: cloudflare`, `x-powered-by: Next.js`.
  - Non-volatile headers (everything except date/x-*/etag/content-length/cf-ray/set-cookie) diff-identical across the two. Body sha256 differs between my two requests (8429328b... vs 38cb36d2...), so the HTML is per-request dynamic. `cache-control` occurs 0 times in the body (confirmed by running).
- S178 https://www.googleapis.com/pagespeedonline/v5/runPagespeed
  - Command: `curl -sS -D s178.hdr -o s178.body 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://ds4cc.com&category=performance'` -> 429.
  - Body `error.message`: `Quota exceeded for quota metric 'Queries' and limit 'Queries per day' of service 'pagespeedonline.googleapis.com' for consumer 'project_number:583797351490'.` `error.status` = `RESOURCE_EXHAUSTED`, reason `rateLimitExceeded`; ErrorInfo metadata `quota_limit` `defaultPerDayPerProject`, `quota_limit_value` `"0"`, consumer `projects/583797351490`. This is the same body wave 1 recorded. Confirmed by running.

VERDICTS:
- S142: claim VERIFIED with a qualifier. The register quote is NOT verbatim (ends `。` where the page has `，或者内容不适触发举报。`). The claim as written ("until unpublished") omits the report-takedown clause. A citable quote needs the page's real wording, e.g. the 22-unit stem `网站链接将始终有效，除非手动点击「取消发布」`. Wave-1's VERIFIED stands for the claim, not for the register quote.
- S143: VERIFIED (table row present, with the `<tr>` context). The register quote is not a raw substring. Use `(except LCP resource types and subparts)` plus the row cells as separate quotes.
- S156: VERIFIED. The header value is stable across two requests and equals wave 1's and the register's value. It is a header, not body text, and a point-in-time measurement of a dynamic Next.js page.
- S178: VERIFIED. The 429 body still says what wave 1 claimed.

NOTES:
- The register line 320 for S178 has no quote cell (class "could not be fetched"). "Quota exceeded for quota metric" is wave 1's chosen claim, not the register's. VERIFIED therefore means "the endpoint fetch works and the body is as wave 1 described", not "register quote located".
- The S178 429 comes from `quota_limit_value` "0" on a shared keyless project, so it is a standing refusal rather than transient load. It could change if Google changes the default quota. There is no revision marker. [INFERENCE] on the shared-project reading; the body fields are observed.
- S143's page hash changed between waves while the row survived, so any pin on whole-page hash will drift. Pin on the row/quote.
- Not run: no Wayback check for S142 (clause edit timing unknown); no HEAD request (`-D` on GET used instead); no re-run of the CrUX POST (not my rows).
- No tools installed.

VERDICT: S142 claim VERIFIED but register quote not verbatim (report-takedown clause omitted), S143 VERIFIED (row present, quote form flattened), S156 VERIFIED (header stable across 2 requests), S178 VERIFIED (429 body unchanged; register has no quote cell).
