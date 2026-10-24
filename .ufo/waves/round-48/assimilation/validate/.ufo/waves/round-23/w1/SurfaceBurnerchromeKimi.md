## Verdict

**C2 operability:** the live root page is reachable and reproducibly audited, but it fails the frozen canonical policy: the served head has no canonical link (`canonical_missing`, `failed-policy`, exit 1). My pre-run, by-eye prediction matched the post-candidate validator exactly. **Local policy judgment:** `https://burnerchrome.kimi.page/` is the appropriate expected canonical for now: the property map records no other primary for this Kimi surface, and the page declares no alternate canonical. The policy is appropriate but not implemented by the live page.

**C1 freshness:** the property-map row's public URL is live; its listed local source directory is absent, and the row's specific Kimi chat binding cannot be verified from a public read-only surface.

## Findings

- **P2 — canonical policy fails on the live root page (operability).** Exact fetch command: `curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D /tmp/kake-r23-SurfaceBurnerchromeKimi-k7LS/h -o /tmp/kake-r23-SurfaceBurnerchromeKimi-k7LS/b https://burnerchrome.kimi.page/`. Observed response: `HTTP/2 200`; `content-type: text/html`; 11,976-byte body; SHA-256 `44dc3491fbc6cdc517c1d3821cae43c5988fd4d4f951203f15be8de36829addb`. One response-header block and no `Location` header were captured, so the final URL was the requested `https://burnerchrome.kimi.page/` (no redirect observed). By-eye head result before audit: zero `rel=canonical` links; no canonical occurrence anywhere in the body. Exact audit command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-SurfaceBurnerchromeKimi-k7LS/manifest.json --json`. Exact stdout: `{"findings":[{"id":"canonical_missing","page":"https://burnerchrome.kimi.page/"}],"pagesChecked":1,"verdict":"failed-policy"}`; exit `1`. **Smallest upstream fix (documented only, not applied):** add `<link rel="canonical" href="https://burnerchrome.kimi.page/">` inside the root page's `<head>` in the site's upstream source, then republish through its Kimi publishing path. The listed source directory is currently absent locally (see below).
- **P3 — property-map source path is no longer present (freshness).** The row anchors `~/Projects/ds4cc-marketplace/burnerchrome` as its source directory. Exact checks: `test -e /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome` and `test -e /home/vgpnk/Projects/ds4cc-marketplace`; exact observed output: `source_dir_test_e=1` and `parent_dir_test_e=1`. **Smallest fix:** when the property map is next maintained, mark this source path as historical/absent unless the source is restored; do not treat it as an executable local source path.

## Checked and held

- Frozen C2 population entry: `burnerchrome-kimi`, URL and expected canonical both `https://burnerchrome.kimi.page/`, policy basis `no primary on record: self-canonical`.
- Frozen round-22 policy: exactly one canonical link in the explicit head, resolving against the first head base URL or document URL, must match `expectedCanonical` after HTTP(S) normalization. The head has no `<base>`, no canonical, and no body canonical. It contains regular head metadata/assets and a Kimi SDK script; its one `<svg>` is after `</head>` in the body.
- Lane HEAD observed as `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`; both `b5d599e19bead54b96f589444e9ec64cdf67c28a` (base) and `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc` (candidate) are ancestors. On the exact same snapshot, the lane validator returned `{"findings":[{"id":"canonical_missing","page":"https://burnerchrome.kimi.page/"}],"pagesChecked":1,"verdict":"failed-policy"}` (exit 1), matching my prior prediction. Running the base revision's validator returned `{"findings":[{"id":"html_unsupported","page":"https://burnerchrome.kimi.page/"}],"pagesChecked":1,"verdict":"could-not-evaluate"}` (exit 2), due to the post-head SVG shape. This distinguishes the frozen base from the candidate/current validator behavior.
- Policy judgment: the SKILL.md property map lists this as a Kimi surface and gives no other primary or mirror target for it. The served page title is `burnerchrome — Musketeer family`; its visible site navigation is self-contained through relative page links, and the page itself declares no canonical target. Thus self-canonical is the consistent local publisher policy given current records, even though the live page presently omits the required declaration. The head's `https://www.kimi.com/sdk-seed.js` script has `data-kimi-website-env="published"` and website id `1a0ada92-7532-8d00-8000-00003dc97818`, evidence for Kimi-published status but not proof of the chat id in the map.
- The following receipt contains four C1 claim rows anchored to exact SKILL.md property-map row text as present at the frozen base. The chat-binding row is UNVERIFIABLE because this read-only task cannot send into a Kimi chat, and the public page exposes a website id rather than the map's chat id.

```json
{
  "unit": "property-map",
  "path": "SKILL.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "| burnerchrome kimi | `https://burnerchrome.kimi.page/`",
      "claim": "The property map's burnerchrome Kimi surface URL is live.",
      "surface": "https://burnerchrome.kimi.page/",
      "method": "GET",
      "observation": "curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D /tmp/kake-r23-SurfaceBurnerchromeKimi-k7LS/h -o /tmp/kake-r23-SurfaceBurnerchromeKimi-k7LS/b https://burnerchrome.kimi.page/ → HTTP/2 200; content-type: text/html; final URL https://burnerchrome.kimi.page/ (single response block; no Location); 11976 bytes; sha256 44dc3491fbc6cdc517c1d3821cae43c5988fd4d4f951203f15be8de36829addb",
      "verdict": "HOLD"
    },
    {
      "id": "c2",
      "anchor": "`https://burnerchrome.kimi.page/` | `~/Projects/ds4cc-marketplace/burnerchrome`",
      "claim": "The map's listed source directory is present as a current local source path.",
      "surface": "/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome",
      "method": "test -e",
      "observation": "test -e /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome → exit 1; test -e /home/vgpnk/Projects/ds4cc-marketplace → exit 1",
      "verdict": "STALE",
      "correction": "2026-10-21: ~/Projects/ds4cc-marketplace/burnerchrome and its parent ~/Projects/ds4cc-marketplace are absent on this workstation; the listed source path is historical unless restored."
    },
    {
      "id": "c3",
      "anchor": "Kimi surface, chat `1a0ada42-28e2…`",
      "claim": "The live surface is Kimi-published, as the map's Kimi-surface designation implies.",
      "surface": "https://burnerchrome.kimi.page/ (served HTML head)",
      "method": "read",
      "observation": "Head includes https://www.kimi.com/sdk-seed.js with data-kimi-website-env=\"published\" and data-kimi-website-id=\"1a0ada92-7532-8d00-8000-00003dc97818\".",
      "verdict": "HOLD"
    },
    {
      "id": "c4",
      "anchor": "Kimi surface, chat `1a0ada42-28e2…`",
      "claim": "The specific owning Kimi chat is 1a0ada42-28e2…",
      "surface": "Public page and read-only Kimi surface only; chat interaction prohibited",
      "method": "read",
      "observation": "The served page exposes website id 1a0ada92-7532-8d00-8000-00003dc97818, not the SKILL.md chat id; no chat interaction was performed.",
      "verdict": "UNVERIFIABLE",
      "reason": "The public page does not expose its owning chat id, and verifying that binding would require Kimi chat/account access or sending into a Kimi chat, which is outside the read-only bounds."
    }
  ]
}
```

## Limits

- This is one GET snapshot of the root URL only. No subpage, response-body canonical in another route, redirect target beyond this response, search-engine selection, or publisher state was independently tested.
- The page's missing canonical is a static HTML observation; no claim is made about search-engine behavior.
- The Kimi chat binding remains unverifiable without prohibited chat/account interaction. No upstream changes or publishing were performed; no tools were installed or updated.
