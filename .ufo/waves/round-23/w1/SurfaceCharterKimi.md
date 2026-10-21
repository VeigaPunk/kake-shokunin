## Verdict

`expectedCanonical` is the right **intended local policy target**: the SKILL.md property map calls the charter GitHub Pages front the canonical document and says Kimi charter variants use it. The single public GET returned the Kimi 404 dead-slot page, whose explicit `<head>` has no canonical link. The frozen round-22 rule therefore predicts `failed-policy` / `canonical_missing`; the snapshot audit returned exactly that. This is an operability failure for the current URL, not evidence that the expected target should be changed to the Kimi URL.

## Findings

### P2 — Current charter Kimi response fails the canonical preflight (operability)

Exact GET command: `curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D /tmp/kake-r23-SurfaceCharterKimi-jPIH/h -o /tmp/kake-r23-SurfaceCharterKimi-jPIH/b -w 'status=%{http_code}\nfinal_url=%{url_effective}\ncontent_type=%{content_type}\n' https://charter-ufo-fsd.kimi.page/`

Exact observed output:

- `status=404`
- `final_url=https://charter-ufo-fsd.kimi.page/`
- `content_type=text/html; charset=utf-8`
- `sha256=93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966  /tmp/kake-r23-SurfaceCharterKimi-jPIH/b`

The response header began `HTTP/2 404`; the body declares `<title>404</title>` and `404 Page Not Found`. Its head runs from `<head>` to `</head>` and contains charset, viewport, title, and style, with no canonical `<link>`.

Before invoking the audit, I recorded the prediction at `/tmp/kake-r23-SurfaceCharterKimi-jPIH/pre-audit-prediction.txt`: the explicit head has no canonical link, so the frozen policy implies `failed-policy`, exit 1, `canonical_missing`.

Exact audit command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-SurfaceCharterKimi-jPIH/manifest.json --json`

Exact observed output:

`{"findings":[{"id":"canonical_missing","page":"https://charter-ufo-fsd.kimi.page/"}],"pagesChecked":1,"verdict":"failed-policy"}`

`process_exit=1`

The prediction and observed result match. Smallest upstream fix: follow the documented `RECREATE` route for the charter Kimi slot, and have the resulting published charter page's head emit one canonical link to `https://veigapunk.github.io/charter-ufo-fsd/`. This is documented only; no source, chat, or publication action was taken. Do not change `expectedCanonical` to the dead Kimi URL.

## C1 property-map receipt

```json
{
  "unit": "property-map",
  "path": "SKILL.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "all kimi variants `rel=canonical` here",
      "claim": "The property map assigns charter Kimi variants to the charter GitHub Pages front as their canonical destination.",
      "surface": "/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md",
      "method": "read",
      "observation": "Row: | charter GHP front | `https://veigapunk.github.io/charter-ufo-fsd/` | `~/Projects/origin-work/charter-ufo-fsd` | Pages deploy from branch (no workflow file); canonical doc, all kimi variants `rel=canonical` here |",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "| charter-ufo-fsd.kimi.page | 404 dead slot |",
      "claim": "The property map identifies the charter Kimi URL as a 404 dead slot.",
      "surface": "https://charter-ufo-fsd.kimi.page/",
      "method": "GET",
      "observation": "status=404; final_url=https://charter-ufo-fsd.kimi.page/; content_type=text/html; charset=utf-8; body sha256=93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "RECREATE path — no bound chat exists",
      "claim": "The property map documents RECREATE as the route for this dead slot.",
      "surface": "/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md",
      "method": "read",
      "observation": "The charter Kimi row says `RECREATE path — no bound chat exists`.",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "RECREATE path — no bound chat exists",
      "claim": "No Kimi chat is bound to this charter slot.",
      "surface": "https://charter-ufo-fsd.kimi.page/",
      "method": "GET",
      "observation": "The public response is HTTP 404 with a generic `404 Page Not Found` body; it exposes no chat-binding state.",
      "verdict": "UNVERIFIABLE",
      "reason": "A public unauthenticated GET cannot determine private Kimi chat binding. No account/API or chat surface was accessed."
    }
  ]
}
```

## Checked and held

- The frozen round-22 contract requires exactly one canonical link in the explicit head and lists `canonical_missing` as a finding id. The input policy target was `https://veigapunk.github.io/charter-ufo-fsd/`.
- C2 population identifies this surface as `charter-kimi`, with the same `expectedCanonical` and policy basis `kimi charter variant (map: 404 dead slot)`.
- `git rev-parse HEAD` returned `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`; `git diff --quiet b5d599e19bead54b96f589444e9ec64cdf67c28a -- SKILL.md` succeeded (`skill_diff_from_c1_base=identical`), so the cited property-map anchors match the specified C1 base.
- `test -e /home/vgpnk/Projects/origin-work/charter-ufo-fsd` evaluated false (`charter_source_path=absent`). SKILL.md already records this source path as absent in its citation-local note; it is not currently available at that mapped location for a local recreate.
- The response's own HTML does **not** declare the expected canonical URL (or any canonical URL). Thus the expected target is map-correct for restored/published charter content, but it is not the current page's declared canonical. The audit only checks the local snapshot's static head; it does not determine HTTP status or Kimi publication state.

## Limits

- Exactly one unauthenticated public GET was made to the assigned Kimi URL. No GET/HEAD was made to the GHP target. No credentials, cookies, account APIs, chat, publish, deploy, or DNS operation was used.
- The local property map says `RECREATE path — no bound chat exists`; a separate dead-slots note in SKILL.md says an earlier charter rebuild produced version card `efc1830` and that the remaining gate was a human Publish + slug click. Those instructions do not agree about the current chat/workflow. I name the direct property-map `RECREATE` route above but cannot resolve that conflict through this public GET; no upstream change was applied.
- No tool was installed or updated.
