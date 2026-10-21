## Verdict

- **C2 operability: failed policy (P2).** The single read-only GET returned HTTP 200 at the expected URL, but its explicit `<head>` contains no canonical link. Before running the audit, the observed head plus the frozen round-22 rule implied `failed-policy` / `canonical_missing` / exit 1; the local audit matched that prediction.
- **Expected canonical: correct local policy.** The frozen property map labels this GHP surface canonical, and the round-23 population sets the same URL as `expectedCanonical`. The page itself declares no canonical URL, rather than declaring a conflicting one: this is a missing published signal, not evidence to change the expected target.
- **C1 freshness:** the canonical role and HTTP 200 status are held; the mapped local source path is stale; the Pages-branch-on-push publishing mechanism is unverified.

## Findings

### P2 — Published page is missing its canonical link

**Impacted claim/axis:** `lucario-ghp`, C2 operability; the frozen local policy requires exactly one canonical link in the explicit head and equality with `expectedCanonical`.

**GET command:**

```text
curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D /tmp/kake-r23-SurfaceLucarioGhp-ONOv/h -o /tmp/kake-r23-SurfaceLucarioGhp-ONOv/b -w 'status=%{http_code}\nfinal_url=%{url_effective}\ncontent_type=%{content_type}\n' 'https://veigapunk.github.io/lucario/'
```

**Exact observed output:**

```text
status=200
final_url=https://veigapunk.github.io/lucario/
content_type=text/html; charset=utf-8
bee2d9f5b5777768e69a5b9aaa9c28dfcc4107f57a4dfb6ec8726d9685c46cff  /tmp/kake-r23-SurfaceLucarioGhp-ONOv/b
```

I read the saved response head before invoking the audit: it opens at line 3 (`<head>`), contains the charset, viewport, title and style through line 28, and closes at line 29 (`</head>`); no `<link rel="canonical">` occurs in that head. The round-22 contract says “Exactly one canonical link in explicit head per page.” This implies `canonical_missing`, hence `failed-policy` and exit 1. The script's `evaluate_page` returns `canonical_missing` when no head canonical is present; `audit_manifest` maps any finding to `failed-policy` and exit 1.

**Snapshot audit command:**

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-SurfaceLucarioGhp-ONOv/manifest.json --json
```

The manifest used was `{"version":1,"pages":[{"url":"https://veigapunk.github.io/lucario/","file":"b","expectedCanonical":"https://veigapunk.github.io/lucario/"}]}`.

**Exact audit output:**

```text
{"findings":[{"id":"canonical_missing","page":"https://veigapunk.github.io/lucario/"}],"pagesChecked":1,"verdict":"failed-policy"}
audit_exit=1
```

**Smallest upstream fix (documented only; not applied):** add `<link rel="canonical" href="https://veigapunk.github.io/lucario/">` to the Lucario homepage source's explicit `<head>`, then publish through the Pages branch. The property map names `site/` as part of the source tree, but the mapped local checkout is absent, so the exact source filename is not verified.

### P2 — Mapped local source path is stale

**Impacted claim/axis:** property-map source location; C1 freshness and the ability to locate the upstream file for the fix above.

**Exact command:** `for path in /home/vgpnk/Projects/lucario /home/vgpnk/Projects/lucario/site /home/vgpnk/Projects/lucario/src/lucario/engine.py; do if test -e "$path"; then printf 'test -e %s: true\n' "$path"; else printf 'test -e %s: false\n' "$path"; fi; done`

**Exact observed output:**

```text
test -e /home/vgpnk/Projects/lucario: false
test -e /home/vgpnk/Projects/lucario/site: false
test -e /home/vgpnk/Projects/lucario/src/lucario/engine.py: false
```

**Smallest fix:** update the property-map source location only after identifying the current checkout, or mark the source unavailable; do not infer a replacement path.

### P3 — Pages branch deployment trigger is not reverified

**Impacted claim/axis:** property-map publishing path; C1 freshness. The GET establishes the current response, not which branch or trigger publishes it.

**Exact command:** the read-only GET above.

**Exact observed output:** `status=200`, `final_url=https://veigapunk.github.io/lucario/`, `content_type=text/html; charset=utf-8`, body SHA-256 `bee2d9f5b5777768e69a5b9aaa9c28dfcc4107f57a4dfb6ec8726d9685c46cff`.

**Smallest fix:** verify the current upstream Pages branch or deployment configuration and refresh the map's publishing-path statement. The mapped local source checkout was absent, so this mechanism remains unverified here.

## Checked and held

- Frozen policy: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/contract.json` requires exactly one canonical link in the explicit head and compares its normalized URL to `expectedCanonical`; it does not claim search-engine selection or fetch URLs itself.
- Frozen C2 population: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/c2-population.json` identifies `lucario-ghp`, gives the GHP URL as both `url` and `expectedCanonical`, and cites the property map as the policy basis.
- The C1 anchors below were checked against `SKILL.md` at frozen base `b5d599e19bead54b96f589444e9ec64cdf67c28a` using read-only `git show`; each anchor is a substring of that property's map row.

### C1 property-map receipt

```json
{
  "unit": "property-map",
  "path": "/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "lucario GHP (canonical) | `https://veigapunk.github.io/lucario/`",
      "claim": "The property map designates the Lucario GHP URL as the canonical surface; this is the correct local expectedCanonical for this surface.",
      "surface": "/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md",
      "method": "read",
      "observation": "| lucario GHP (canonical) | `https://veigapunk.github.io/lucario/` | `~/Projects/lucario` (`site/` + `src/lucario/engine.py`) | Pages branch deploy on push — live 200, verified 09-28 |",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "`~/Projects/lucario` (`site/` + `src/lucario/engine.py`)",
      "claim": "The property map names a local Lucario source checkout with `site/` and `src/lucario/engine.py`.",
      "surface": "/home/vgpnk/Projects/lucario",
      "method": "test -e",
      "observation": "test -e /home/vgpnk/Projects/lucario: false\ntest -e /home/vgpnk/Projects/lucario/site: false\ntest -e /home/vgpnk/Projects/lucario/src/lucario/engine.py: false",
      "verdict": "STALE",
      "correction": "The mapped checkout, its site directory, and its engine file were absent at the checked paths on 2026-10-21; update the source location only after identifying the current checkout."
    },
    {
      "id": "c1",
      "anchor": "Pages branch deploy on push",
      "claim": "The map states that pushes to a Pages branch deploy this surface.",
      "surface": "https://veigapunk.github.io/lucario/",
      "method": "GET",
      "observation": "status=200\nfinal_url=https://veigapunk.github.io/lucario/\ncontent_type=text/html; charset=utf-8\nsha256=bee2d9f5b5777768e69a5b9aaa9c28dfcc4107f57a4dfb6ec8726d9685c46cff",
      "verdict": "UNVERIFIABLE",
      "reason": "The public page response establishes that the URL currently serves content but cannot identify its publishing branch or push trigger, and the mapped local checkout is absent."
    },
    {
      "id": "c1",
      "anchor": "live 200, verified 09-28",
      "claim": "The mapped live-200 status remains true at re-verification.",
      "surface": "https://veigapunk.github.io/lucario/",
      "method": "GET",
      "observation": "status=200\nfinal_url=https://veigapunk.github.io/lucario/\ncontent_type=text/html; charset=utf-8\nsha256=bee2d9f5b5777768e69a5b9aaa9c28dfcc4107f57a4dfb6ec8726d9685c46cff",
      "verdict": "HOLD"
    }
  ]
}
```

## Limits

- The HTTP observation is one response only; it does not establish crawler behavior, search-engine canonical selection, deployment configuration, or future availability.
- The source checkout `/home/vgpnk/Projects/lucario` was absent; therefore the exact upstream source filename and Pages publishing configuration were not inspectable. The upstream fix above is a documented smallest source change, not an applied change.
- No LSP device/server was exposed in the available tool inventory. `grep` was used only to locate relevant text; the findings rely on the subsequently read source sections, frozen policy rows, the saved response, and the exercised audit output rather than treating grep as semantic proof.
- No lane production file was changed; only the requested report was written. The response snapshot, manifest, and frozen map copy are under `/tmp/kake-r23-SurfaceLucarioGhp-ONOv/`.
