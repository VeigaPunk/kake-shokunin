# ScoutQuarantineD

Rows: S154, S178, S184 (class "the cited source could not be fetched, so no quote was checked"). Fetch date 2026-10-25 UTC. Bodies saved in `ScoutQuarantineD.files/` (`crux-post.body/.hdr`, `psi-get.body/.hdr`).

## ROWS:

| id | URL | status code | verdict | located quote + location |
|---|---|---|---|---|
| S154 (shokuknow register: lane `kake`, round2) | https://chromeuxreport.googleapis.com/v1/records:queryRecord | 403 (POST, body `{"origin":"https://example.com"}`); round-48 GET was 404 | VERIFIED | "doesn't allow unregistered callers" in the JSON response body, field `error.message`; same body has `"status": "PERMISSION_DENIED"` (`error.status`), `error.code` 403 |
| S178 (register: `kake`, round4) | https://www.googleapis.com/pagespeedonline/v5/runPagespeed | 429 (GET, `url=https://ds4cc.com&category=performance`) | VERIFIED | "Quota exceeded for quota metric" in the response body, field `error.message` (full text: `... 'Queries' and limit 'Queries per day' of service 'pagespeedonline.googleapis.com'`); `error.status` = `"RESOURCE_EXHAUSTED"` |
| S184 (register: `kake`, round5) | https://chromeuxreport.googleapis.com/v1/records:queryRecord | 403 (same POST as S154; one probe serves both rows, same URL) | VERIFIED | same as S154: "doesn't allow unregistered callers", `error.status` `"PERMISSION_DENIED"` (`error.message`, `error.status`) |

Each quote is <= 25 units and <= 40 characters (34, 31, 34 chars). I checked with `grep -cF` against the saved bodies: each returned >= 1, and `"status": "PERMISSION_DENIED"` and `"status": "RESOURCE_EXHAUSTED"` each returned 1.

## NOTES:

- **The three ids are not in this lane's `corpus/SOURCES.md`.** `grep` finds no `S154`, `S178` or `S184` in `corpus/SOURCES.md` or `corpus/knowledge`, so no kake entry cites them under these ids. They exist only in the read-only shokuknow register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, in a table whose ids carry a stray trailing backtick (lines 319-321). They are not adopted.
- **Mapping to the lane's own proposals.** The register ids are round-local staging ids. The matching rows in `/home/vgpnk/Projects/shokuknow/lanes/kake/` are `own-work` probes:
  - round2 `S304` (`round2/SOURCES-PROPOSED.md`). Its Gate block quotes the response body: "Method doesn't allow unregistered callers (callers without established identity)."
  - round4 `S328` (`round4/SOURCES-PROPOSED.md`). Its entry quotes "Quota exceeded for quota metric 'Queries' and limit 'Queries per day' of service 'pagespeedonline.googleapis.com'".
  - round5 `S334` (`round5/SOURCES-PROPOSED.md`). It is the same POST probe as S304, rechecked.
  - The `ID-REMAP.md` table maps round2 S267->S304, round4 S291->S328 and round5 S297->S334. That is a different numbering from the register's S154/S178/S184, so this pairing is **[INFERENCE]**. It rests on the URL, the round and the probe content, not on an explicit id map.
- **Why they were "unreachable" in round 48.** The register class is "could not be fetched". Round 48's check used a plain GET and got S154/S184 HTTP 404 and S178 HTTP 429. These are not documentation pages but API endpoints, and the claim is the API's own error response. The CrUX endpoint is POST-only; **[INFERENCE]** a bare GET returns 404 for that reason (I did not run the GET). A POST with a JSON `origin` body, as the row's own `recheck` command specifies, returns the cited 403 body. The 404 was a method mismatch, not an absent claim.
- **Not fabrication.** Both claims reproduce from a plain HTTP call today, so none of the three rows is fabrication class.
- **S178 is time-sensitive.** The 429 is the shared keyless daily quota. The body today shows `quota_limit_value` `"0"`, `quota_limit` `defaultPerDayPerProject`, consumer `projects/583797351490`. That is a zero default per-project quota, not a transient exhaustion. The lane's S328 text calls it a "shared daily quota", which is still compatible but understates it. The quote is re-checkable only while Google keeps this behaviour (live API, no revision marker).
- **Probes run:** one POST to the CrUX endpoint, one GET to the PSI endpoint, no key or credential involved, user agent `kake-shokunin-round57-scout`. The CrUX Vis page (`cruxvis.withgoogle.com`), named in the S328/S334 claims, was **not** fetched: it is not one of the three cited URLs (those claims say it serves a client-rendered shell). That part of the claims is unrun.
- No register or campaign file was edited. No tool installed.

VERDICT: S154 VERIFIED, S178 VERIFIED, S184 VERIFIED (403 PERMISSION_DENIED and 429 RESOURCE_EXHAUSTED bodies reproduced on 2026-10-25); the old 404 was a GET against a POST-only endpoint; none are fabrication; none are in corpus/SOURCES.md.
