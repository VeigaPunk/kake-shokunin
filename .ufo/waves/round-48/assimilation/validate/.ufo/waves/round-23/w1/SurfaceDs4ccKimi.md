## Verdict

C2 for `ds4cc-kimi` is `failed-policy` with `canonical_missing` (exit 1), exactly as predicted from the inspected head before running the audit. `https://ds4cc.com/` is the correct **local policy** target: the base `SKILL.md` property map names ds4cc.com as primary and this URL as its Kimi mirror. The live page declares `og:url="./"`, which resolves to the mirror URL, but that is Open Graph metadata—not a canonical link—and the page has no `<link rel="canonical">`. The expectation is right; the current page does not implement it. This is scoped evidence, not independent lane admission.

## Findings

- **P2 — C2 operability / canonical policy.** Exact fetch command: `curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D /tmp/kake-r23-SurfaceDs4ccKimi-V6Es/h -o /tmp/kake-r23-SurfaceDs4ccKimi-V6Es/b -w 'STATUS=%{http_code}\nFINAL_URL=%{url_effective}\nCONTENT_TYPE=%{content_type}\n' https://ds4cc.kimi.page/`. Exact output:
  ```text
  STATUS=200
  FINAL_URL=https://ds4cc.kimi.page/
  CONTENT_TYPE=text/html
  BODY_SHA256=d135c81ef2090220a4aa56f76cfa323767d5e83651ba7a88cd6933922e480c82  /tmp/kake-r23-SurfaceDs4ccKimi-V6Es/b
  ```
  Exact audit command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-SurfaceDs4ccKimi-V6Es/manifest.json --json`. Exact stdout: `{"findings":[{"id":"canonical_missing","page":"https://ds4cc.kimi.page/"}],"pagesChecked":1,"verdict":"failed-policy"}`; process exit: `1`.
  **Impacted claim/axis:** frozen C2 expected-canonical check / operability. **Smallest fix:** add exactly one `<link rel="canonical" href="https://ds4cc.com/">` in the authoritative DS4CC page head, then republish the Kimi mirror through its correct publishing slot. Documented only; no source edit or publish was attempted. The mapped source directory `/home/vgpnk/Projects/ds4cc-marketplace` is absent (`SOURCE_PATH=absent (test -e exit 1)`), so it is not presently available here for that edit.

## Checked and held

- Inspected the fetched HTML head through `</head>` at line 486 by eye before invoking `canonical_audit.py`. It contains `<meta property="og:url" content="./"/>`, a favicon link, and the Kimi SDK seed script; it contains no canonical link. The frozen round-22 policy requires exactly one canonical link in the explicit head. Pre-run prediction: `failed-policy`, `canonical_missing`, exit `1`. The audit result above matches that prediction.
- The expected target is supported as local publisher policy by the base `SKILL.md` property map: ds4cc.com is marked primary and `ds4cc.kimi.page` is marked its Kimi mirror. The live page's relative `og:url` is self-referential Open Graph metadata; it does not constitute a canonical declaration and does not change the local policy.
- The GET response identifies a published Kimi-hosted page (`data-kimi-website-env="published"`). No Kimi chat was opened or written to. The mapped source path check was read-only.
- Exact source-path check: `if test -e /home/vgpnk/Projects/ds4cc-marketplace; then printf 'SOURCE_PATH=present\n'; else printf 'SOURCE_PATH=absent (test -e exit 1)\n'; fi` → `SOURCE_PATH=absent (test -e exit 1)`.
- Lane HEAD observed: `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`. Receipt anchors below were checked against the required base object `b5d599e19bead54b96f589444e9ec64cdf67c28a:SKILL.md`.

C1 property-map receipt for this surface:
```json
{
  "unit": "property-map",
  "path": "SKILL.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "| ds4cc.com (primary) | `https://ds4cc.com/`",
      "claim": "The property map designates ds4cc.com as primary, supporting https://ds4cc.com/ as this mirror's local canonical target; this is a local policy designation, not independent search-engine validation.",
      "surface": "/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:16",
      "method": "read",
      "observation": "| ds4cc.com (primary) | `https://ds4cc.com/` | `~/Projects/ds4cc-marketplace` | GH Actions on push to `main` ...",
      "verdict": "HOLD"
    },
    {
      "id": "c2",
      "anchor": "| ds4cc kimi mirror | `https://ds4cc.kimi.page/`",
      "claim": "The mapped DS4CC Kimi mirror URL remains publicly reachable at its listed URL.",
      "surface": "https://ds4cc.kimi.page/",
      "method": "GET",
      "observation": "STATUS=200; FINAL_URL=https://ds4cc.kimi.page/; CONTENT_TYPE=text/html; BODY_SHA256=d135c81ef2090220a4aa56f76cfa323767d5e83651ba7a88cd6933922e480c82  /tmp/kake-r23-SurfaceDs4ccKimi-V6Es/b",
      "verdict": "HOLD"
    },
    {
      "id": "c3",
      "anchor": "~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record.",
      "claim": "The map's annotation that the listed source directory is absent remains true locally.",
      "surface": "/home/vgpnk/Projects/ds4cc-marketplace",
      "method": "test -e",
      "observation": "SOURCE_PATH=absent (test -e exit 1)",
      "verdict": "HOLD"
    },
    {
      "id": "c4",
      "anchor": "chat `1a073c43-bf42-874a-8000-0907bd80b9dc` — STALE (~Aug-29 vintage)",
      "claim": "The referenced Kimi chat is still at the approximately Aug-29 vintage recorded by the map.",
      "surface": "https://ds4cc.kimi.page/ (public page; chat not accessed)",
      "method": "GET",
      "observation": "The public GET returned the published page HTML, not the referenced Kimi chat's version history.",
      "verdict": "UNVERIFIABLE",
      "reason": "The public page does not expose the cited chat's content/version history. No Kimi chat was accessed or written to, so its current vintage cannot be established from this allowed surface."
    }
  ]
}
```

## Limits

One read-only GET was made to the assigned mirror URL. The result covers fetch-time HTML and the frozen static publisher policy only; it does not establish rendered JavaScript state, HTTP headers beyond the response metadata captured, search-engine canonical selection, the current Kimi chat vintage, or publishing readiness. No install, source edit, publish, or chat interaction occurred.
