## Verdict

The single read-only GET returned HTTP 404 at `https://lucario.kimi.page/` (final URL unchanged), `text/html; charset=utf-8`, body SHA-256 `93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966`. Before invoking the audit, I inspected the snapshot head: it is explicitly closed and has no canonical link. Under the frozen round-22 policy, my pre-run prediction was `failed-policy` with `canonical_missing` (exit 1). The audit returned exactly that.

The expected URL, `https://veigapunk.github.io/lucario/`, is the right canonical *target for a published mirror*: the property map labels the GHP surface canonical. It is not the right model of this Kimi slot's current serving state: the map says the slot was never published / expected not served, and the fetched page is a generic 404 that declares no canonical. Thus `canonical_missing` describes this snapshot; it does not establish that the expected target URL is wrong. The current C2 entry conflates an intended future mirror's canonical policy with an unserved slot.

Documented upstream fix, not applied: the property map says Lucario has no bound Kimi chat and zero consumed fires, and its recovery rule is `dead slot + empty chat → recreate`. Recreate the upstream slot; if it is intended to become a mirror, publish it with one canonical link to the GHP primary. Until then, represent it as unserved rather than as a currently published canonical page.

## Findings

### P2 — `lucario-kimi` is modeled as a published canonical page although the map says it is unserved

**Axis:** operability and freshness. **Impacted claim:** C2 `lucario-kimi`.

Exact read-only fetch command (the only GET made): `tmp="$(mktemp -d /tmp/kake-r23-SurfaceLucarioKimi-XXXX)" && curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D "$tmp/h" -o "$tmp/b" -w 'status=%{http_code}\nfinal_url=%{url_effective}\ncontent_type=%{content_type}\n' 'https://lucario.kimi.page/' && sha256sum "$tmp/b" && printf 'TMP=%s\n' "$tmp" && cat "$tmp/h"`

Exact requested result fields:

- `status=404`
- `final_url=https://lucario.kimi.page/`
- `content_type=text/html; charset=utf-8`
- `93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966  /tmp/kake-r23-SurfaceLucarioKimi-Nsld/b`
- Response status line: `HTTP/2 404 `

By-eye head check before the audit: the downloaded body has `<head>` at line 3 and `</head>` at line 114, with metadata, `<title>404</title>`, and style content, but no `<link rel="canonical">`. The page body also identifies itself as `404 Page Not Found`. The C2 population row was read as `id=lucario-kimi`, URL `https://lucario.kimi.page/`, expected canonical `https://veigapunk.github.io/lucario/`, policy basis `mirror declares its primary (map: never published, expected not served)`.

Predicted result, made before the audit: one explicit, supported head and no canonical signal implies `failed-policy` / `canonical_missing`, not `canonical_mismatch` or `html_unsupported`.

Exact audit command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-SurfaceLucarioKimi-Nsld/manifest.json --json`

Exact output:

`{"findings":[{"id":"canonical_missing","page":"https://lucario.kimi.page/"}],"pagesChecked":1,"verdict":"failed-policy"}`

`EXIT_CODE=1`

**Smallest fix:** keep the GHP URL as the canonical target for any published mirror, but do not treat this currently unserved slot as a served canonical page; defer it from canonical-page preflight or model its expected-unserved state separately until upstream publication.

### P2 — The property-map source checkout path is absent at its recorded local path

**Axis:** freshness. **Impacted claim:** the `~/Projects/lucario/site` source path in the Kimi property-map row.

Exact commands and observed output: `test -e /home/vgpnk/Projects/lucario/site exit=1`; `test -e /home/vgpnk/Projects/lucario/site/README.md exit=1`.

**Smallest fix:** re-establish the checkout or verify its replacement location before updating the map; no replacement path was inferred or written.

## Checked and held

- Frozen policy at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/contract.json` requires exactly one canonical link in an explicit head and compares its normalized HTTP(S) URL to `expectedCanonical`. It explicitly does not claim to fetch pages, evaluate JavaScript, or establish HTTP state or search-engine canonical selection.
- The fresh body and the audit agree: no head canonical, `canonical_missing`, exit 1. The audit operated offline on the saved response body; it did not make a request.
- The map's GHP row names `https://veigapunk.github.io/lucario/` canonical, so that is a consistent target for a future published mirror. I did not make a second GET to reverify the map's historical `live 200, verified 09-28` statement.
- The source directory and its referenced README are absent at the mapped local paths. The README's current publish-gate state is therefore not verified.
- No production file, upstream Kimi state, publish/deploy state, git index, or jj state was modified. The audit manifest is only at `/tmp/kake-r23-SurfaceLucarioKimi-Nsld/manifest.json`.

C1 property-map receipt:

```json
{
  "unit": "property-map",
  "path": "/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "| lucario kimi slot | `https://lucario.kimi.page/` — 404",
      "claim": "The mapped Kimi slot currently responds HTTP 404.",
      "surface": "https://lucario.kimi.page/",
      "method": "GET",
      "observation": "status=404\nfinal_url=https://lucario.kimi.page/\ncontent_type=text/html; charset=utf-8",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "| `https://lucario.kimi.page/` — 404, **never published**",
      "claim": "The historical assertion that this slot was never published is not established by a single current 404.",
      "surface": "https://lucario.kimi.page/",
      "method": "GET",
      "observation": "status=404; final_url=https://lucario.kimi.page/",
      "verdict": "UNVERIFIABLE",
      "reason": "A current 404 cannot establish that the URL has never been published historically; no Kimi publication history was available in the checked sources."
    },
    {
      "id": "c1",
      "anchor": "| `~/Projects/lucario/site` |",
      "claim": "The property-map source directory is present at its recorded local path.",
      "surface": "/home/vgpnk/Projects/lucario/site",
      "method": "test -e",
      "observation": "test -e /home/vgpnk/Projects/lucario/site exit=1",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, `/home/vgpnk/Projects/lucario/site` is absent on this host, so the property-map source path is stale here."
    },
    {
      "id": "c1",
      "anchor": "Kimi surface pending first publish (README: \"pending — gated\").",
      "claim": "The referenced README still documents a pending, gated first publish.",
      "surface": "/home/vgpnk/Projects/lucario/site/README.md",
      "method": "test -e",
      "observation": "test -e /home/vgpnk/Projects/lucario/site/README.md exit=1",
      "verdict": "UNVERIFIABLE",
      "reason": "The mapped source directory and README are absent at this host, and the live 404 cannot determine whether the upstream README's publish gate remains pending."
    }
  ]
}
```

## Limits

- The one GET was limited to `https://lucario.kimi.page/`; the GHP target's current live status was not rechecked.
- The live 404 establishes the current response, not the historical claim "never published." The local Lucario source checkout is absent, preventing inspection of its README or local publish artifacts.
- `canonical_audit.py` is the frozen offline static policy checker; the result does not test server status, redirect behavior, or publishing readiness.
- I attempted to read `xd://lsp`; the tool returned `No such tool: xd://lsp` and listed no LSP device. No LSP semantic definition/reference query was available; the behavioral result is grounded in the actual CLI run and the frozen policy/source read, not grep output.
