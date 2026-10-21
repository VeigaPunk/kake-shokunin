## Verdict

**C2 / operability: FAIL.** The single read-only GET returned `200` at the expected URL, but the captured explicit `<head>` has no canonical link. Before running the validator, the frozen round-22 rule (exactly one canonical link in the explicit head) and that observed head implied `failed-policy` / `canonical_missing`; the audit matched.

The expected canonical `https://ufo-fsd.kimi.pro/` is the right **local policy expectation**: the frozen C2 row and SKILL.md property map identify that exact root as this surface, and record no primary URL. It is not a canonical declared by the page or a search-engine canonical assertion. The page declares `<title>DS4CC</title>` and Kimi `data-kimi-website-id="1a0acf59-c082-8794-8000-0000eaa74687"` / `data-kimi-website-env="published"`, but no canonical. The property map warns that this website ID is shared with `ufo-fsd.kimi.page`, so it cannot establish which host is primary.

This is a scoped surface observation only; it makes no independent admission claim.

## Findings

### P2 — `canonical_missing` (C2 operability)

- **Exact command (one curl invocation):** `tmp=$(mktemp -d /tmp/kake-r23-SurfaceUfoFsdKimiPro-XXXX) && printf 'tmp=%s\n' "$tmp" && curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D "$tmp/h" -o "$tmp/b" -w 'status=%{http_code}\nfinal_url=%{url_effective}\ncontent_type=%{content_type}\n' https://ufo-fsd.kimi.pro/ && sha256sum "$tmp/b"`
- **Exact observed output:**
  ```text
  tmp=/tmp/kake-r23-SurfaceUfoFsdKimiPro-vdJv
  status=200
  final_url=https://ufo-fsd.kimi.pro/
  content_type=text/html; charset=utf-8
  1df92e30ba5a76e69a863a729326949871d3d83e290935d596f6cd9b7d65ab8c  /tmp/kake-r23-SurfaceUfoFsdKimiPro-vdJv/b
  ```
  Captured head by eye: title, module script, stylesheet, and Kimi seed script; no `<link rel="canonical">`.
- **Expected before audit:** one canonical in explicit head is required; the head contains none, so expected finding `canonical_missing` and verdict `failed-policy`.
- **Exact audit command:** `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-SurfaceUfoFsdKimiPro-vdJv/manifest.json --json`
- **Exact output:** `{"findings":[{"id":"canonical_missing","page":"https://ufo-fsd.kimi.pro/"}],"pagesChecked":1,"verdict":"failed-policy"}`; exit code `1`.
- **Impacted claim/axis:** C2 surface `ufo-fsd-kimi-pro`; operability. The live response does not satisfy the frozen head-only canonical preflight.
- **Smallest upstream fix (documented only; not applied):** publish exactly one `<link rel="canonical" href="https://ufo-fsd.kimi.pro/">` inside the served document's explicit `<head>` at the upstream page source. Do not change the local validator or infer a publish target from the shared website ID.

### P3 — Source-directory and chat-binding claims are not live-verifiable here (C1 freshness)

- **Exact command:** the one GET command above; no second request was made.
- **Exact observed output relevant to this limit:** `wc -c /tmp/kake-r23-SurfaceUfoFsdKimiPro-vdJv/b` returned `612 /tmp/kake-r23-SurfaceUfoFsdKimiPro-vdJv/b`. The body contains `<script type="module" crossorigin src="/assets/index-Bw9NLFv4.js"></script>` and `<div id="root"></div>`. Its head declares `data-kimi-website-id="1a0acf59-c082-8794-8000-0000eaa74687"`, not the mapped chat ID.
- **Impacted claim/axis:** the property-map row's `none (Vite shell)` source-directory status and `chat 1a0acd51-4122…` binding; freshness. The 612-byte SPA-shell description and URL are held by this GET; the local source and chat binding are UNVERIFIABLE from this public HTML.
- **Smallest fix:** obtain a read-only authoritative source inventory and chat-to-published-URL record. The page's website ID alone is insufficient, as SKILL.md warns that IDs are not host-unique.

## Checked and held

- Frozen C2 population row: `id=ufo-fsd-kimi-pro`, URL and expected canonical both `https://ufo-fsd.kimi.pro/`, policy basis `no primary on record: self-canonical`.
- Frozen round-22 policy: exactly one canonical link in the explicit head; findings include `canonical_missing`; the audit is a local policy comparison, not a Google/search-engine canonical check.
- The response body is exactly 612 bytes. Its visible HTML mounts `#root` and loads a module asset; the property map's SPA-shell size remains current.
- C1 property-map receipt (anchors are exact substrings of the frozen base `SKILL.md` property-map row):

```json
{
  "unit": "property-map",
  "path": "SKILL.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "| ufo-fsd.kimi.pro | `https://ufo-fsd.kimi.pro/` |",
      "claim": "The mapped live URL remains reachable at the listed root URL.",
      "surface": "https://ufo-fsd.kimi.pro/",
      "method": "GET",
      "observation": "status=200; final_url=https://ufo-fsd.kimi.pro/; content_type=text/html; charset=utf-8; sha256=1df92e30ba5a76e69a863a729326949871d3d83e290935d596f6cd9b7d65ab8c",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "| ufo-fsd.kimi.pro | `https://ufo-fsd.kimi.pro/` |",
      "claim": "The mapped 612B SPA-shell description still matches the public response.",
      "surface": "https://ufo-fsd.kimi.pro/",
      "method": "GET",
      "observation": "612 /tmp/kake-r23-SurfaceUfoFsdKimiPro-vdJv/b; `<script type=\"module\" crossorigin src=\"/assets/index-Bw9NLFv4.js\"></script>`; `<div id=\"root\"></div>`",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "| ufo-fsd.kimi.pro | `https://ufo-fsd.kimi.pro/` |",
      "claim": "The map's source-directory field remains `none` for this surface.",
      "surface": "https://ufo-fsd.kimi.pro/",
      "method": "GET",
      "observation": "The public GET returned the 612-byte HTML shell; it contains no local source-directory path or inventory.",
      "verdict": "UNVERIFIABLE",
      "reason": "A public page response cannot establish whether a local source directory exists; the map provides no path to test, and no local source inventory was checked."
    },
    {
      "id": "c1",
      "anchor": "| ufo-fsd.kimi.pro | `https://ufo-fsd.kimi.pro/` |",
      "claim": "The surface remains bound to the property-map chat ID `1a0acd51-4122…`.",
      "surface": "https://ufo-fsd.kimi.pro/",
      "method": "GET",
      "observation": "The captured head declares `data-kimi-website-id=\"1a0acf59-c082-8794-8000-0000eaa74687\"` and `data-kimi-website-env=\"published\"`; it does not declare the mapped chat ID.",
      "verdict": "UNVERIFIABLE",
      "reason": "The page exposes a Kimi website ID, not a chat-to-published-URL binding; the property map says website IDs are not host-unique, and no permitted public response here proves that binding."
    }
  ]
}
```

## Limits

The only network request was the requested read-only GET (one curl invocation); local evidence steps also included read-only `git show` of the frozen base `SKILL.md` to a temporary file, `wc -c`, and the canonical-audit command. No other host was fetched; no JavaScript or search-engine behavior was exercised; no Kimi chat, account, publish, or deploy action was taken. The report documents the upstream fix only. No tools were installed or updated.
