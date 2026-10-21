## Verdict

C2 operability: **HOLD / clean**. Before running `canonical_audit.py`, the fetched head showed one explicit-head canonical link equal to the configured `expectedCanonical`; the frozen round-22 policy therefore predicted `verdict=clean` and no finding ID. The audit matched. The configured self-canonical is correct for this GHP front. C1 freshness: the mapped public URL is live and self-canonical, but the listed local checkout is absent and the listed deployment mechanism cannot be reverified from the page.

## Findings

- **P2 — Property-map source locator is stale as a present local checkout (freshness).** Exact check: `for p in /home/vgpnk/Projects/plazir-15-site /home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml /home/vgpnk/Projects/plazir-15-site/index.html; do if test -e "$p"; then printf 'present %s\\n' "$p"; else printf 'absent %s\\n' "$p"; fi; done`. Exact output: `absent /home/vgpnk/Projects/plazir-15-site`; `absent /home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml`; `absent /home/vgpnk/Projects/plazir-15-site/index.html`. Smallest fix: correct the property-map entry to mark this local checkout unavailable (or restore the intended checkout before relying on it); no production or map file was changed.
- **No C2 canonical-policy finding.** The one captured page was `200`, stayed at the requested URL, and the static audit returned `clean` with no finding IDs (exact command/output below). No canonical correction is warranted.

### Exact live fetch

Command (the scratch directory was created by this command; one GET only):

```sh
d=$(mktemp -d /tmp/kake-r23-SurfacePlazir15Ghp-XXXX) && printf 'scratch=%s\\n' "$d" && curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D "$d/h" -o "$d/b" -w 'status=%{http_code}\\nfinal_url=%{url_effective}\\ncontent_type=%{content_type}\\n' 'https://veigapunk.github.io/plazir-15-site/' && printf 'sha256=' && sha256sum "$d/b" | cut -d ' ' -f 1
```

Exact output:

```text
scratch=/tmp/kake-r23-SurfacePlazir15Ghp-9HKE
status=200
final_url=https://veigapunk.github.io/plazir-15-site/
content_type=text/html; charset=utf-8
sha256=d82af77aee401d2270c719c6e818256298cc8aad7a71c3e7c4d65bd41f6af18e
```

### Audit and policy comparison

The captured body was read by eye before the audit: lines 3–36 are an explicit `<head>`; line 10 is `<link rel="canonical" href="https://veigapunk.github.io/plazir-15-site/" />`. That is one visible canonical, equal to `expectedCanonical`. Pre-run prediction: `clean`; finding ID: none.

Exact audit command and output:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-SurfacePlazir15Ghp-9HKE/manifest.json --json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
```

The manifest used the captured body as `file: "b"`, URL `https://veigapunk.github.io/plazir-15-site/`, and the same URL as `expectedCanonical`. This matches the prediction. The round-23 population calls this surface `GHP front self-canonical`; the SKILL.md property-map row names this same GHP front URL. The page’s declared canonical independently confirms the local policy is right for this front page. SKILL.md separately describes the *speedrun subpath* as a frozen copy whose canonical points to ds4cc.com; that distinct subpath does not change the front-page policy. This is only the frozen local publisher policy, not a claim about search-engine canonical selection.

## C1 property-map receipt

The anchors below were checked against `SKILL.md` at base `b5d599e19bead54b96f589444e9ec64cdf67c28a`. Three operational claims are included: live front URL/canonical, mapped local checkout, and publishing mechanism.

```json
{
  "unit": "property-map",
  "path": "SKILL.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "| plazir15 GHP front | `https://veigapunk.github.io/plazir-15-site/`",
      "claim": "The property-map GHP front URL is live and its page declares one self-canonical in the head.",
      "surface": "https://veigapunk.github.io/plazir-15-site/",
      "method": "GET",
      "observation": "status=200; final_url=https://veigapunk.github.io/plazir-15-site/; content_type=text/html; charset=utf-8; sha256=d82af77aee401d2270c719c6e818256298cc8aad7a71c3e7c4d65bd41f6af18e; body head line 10: <link rel=\"canonical\" href=\"https://veigapunk.github.io/plazir-15-site/\" />; audit output: {\"findings\":[],\"pagesChecked\":1,\"verdict\":\"clean\"}",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "| plazir15 GHP front | `https://veigapunk.github.io/plazir-15-site/` | `~/Projects/plazir-15-site`",
      "claim": "A local source checkout is present at the property-map path `~/Projects/plazir-15-site`.",
      "surface": "/home/vgpnk/Projects/plazir-15-site",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/plazir-15-site",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, the mapped local source checkout `/home/vgpnk/Projects/plazir-15-site` is absent on this workstation."
    },
    {
      "id": "c1",
      "anchor": "`~/Projects/plazir-15-site` | GH Actions on push to `main`",
      "claim": "The front is currently published by GitHub Actions on pushes to `main`.",
      "surface": "/home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml; absent /home/vgpnk/Projects/plazir-15-site",
      "verdict": "UNVERIFIABLE",
      "reason": "The mapped checkout and workflow are absent locally; the one public page GET confirms served HTML but cannot establish the current GitHub Actions or Pages deployment configuration."
    }
  ]
}
```

## Checked and held

- Read the frozen round-22 canonical policy and round-23 C2 entry. The relevant policy is exactly one canonical link in the explicit head resolving to the expected URL; the policy lists `canonical_missing`, `canonical_multiple`, `canonical_outside_head`, `canonical_href_missing`, `canonical_url_invalid`, `canonical_fragment`, `canonical_mismatch`, and other input findings. None was emitted.
- Read the head by eye and recorded the pre-run prediction before invoking the validator; then ran the requested snapshot audit once.
- Documented-only upstream fix: **none needed for the canonical link**; it already equals the expected URL. If a future snapshot reports a canonical mismatch, the source-level correction would be to set the upstream front-page HTML’s `<link rel="canonical">` to `https://veigapunk.github.io/plazir-15-site/` and publish via the repository’s actual configured channel. No source change or publish was performed. The local source checkout and workflow are unavailable, so their current upstream location/channel is not asserted.

## Limits

One public GET snapshot only; no auth, cookies, writes, publishing, or additional network calls. The audit is static HTML policy checking and does not prove JS-rendered behavior, redirects beyond this fetch, search-engine choice, or deployment provenance. The local checkout and workflow are absent; only those property-map claims remain stale/unverifiable. No tools were installed; no builds, lint, formatters, or broad tests were run.
