## Verdict

- **Operability:** `plazir27.kimi.page` returned HTTP 404 and the static audit failed with `canonical_missing` (exit 1). The fetched response is not the charter mirror.
- **Freshness / policy:** `https://veigapunk.github.io/charter-ufo-fsd/` is the right *local expectedCanonical* for this Kimi charter variant: the property map says all Kimi variants use the charter GHP canonical. The live 404 response itself declares no canonical, so it does not demonstrate that a published mirror currently follows that policy.
- Before invoking `canonical_audit.py`, I read the downloaded explicit head: it has `<title>404</title>` and no canonical link. Under the frozen round-22 policy (exactly one canonical in the explicit head, equal to expectedCanonical), my prediction was `failed-policy`, finding `canonical_missing`, exit 1. The audit matched it.

## Findings

### P1 — The named Kimi mirror is not currently served (operability; property-map freshness)

**Single read-only GET command:**

```sh
tmp=$(mktemp -d /tmp/kake-r23-SurfacePlazir27Kimi-XXXX) && curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D "$tmp/h" -o "$tmp/b" -w 'status=%{http_code}\nfinal_url=%{url_effective}\ncontent_type=%{content_type}\n' 'https://plazir27.kimi.page/' && sha256sum "$tmp/b" && printf 'snapshot=%s\nheaders=%s\n' "$tmp/b" "$tmp/h"
```

Exact observed output:

```text
status=404
final_url=https://plazir27.kimi.page/
content_type=text/html; charset=utf-8
93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966  /tmp/kake-r23-SurfacePlazir27Kimi-iBfG/b
snapshot=/tmp/kake-r23-SurfacePlazir27Kimi-iBfG/b
headers=/tmp/kake-r23-SurfacePlazir27Kimi-iBfG/h
```

By-eye head evidence from that snapshot: `<!DOCTYPE html>`, `<html lang="en">`, explicit `<head>`, `<title>404</title>`, then `</head>`; there is no `<link rel="canonical">` in the head. This is the 404 response, not an observed 09-18 mirror document.

The snapshot manifest used `url=https://plazir27.kimi.page/`, `file=b`, and `expectedCanonical=https://veigapunk.github.io/charter-ufo-fsd/`.

**Pre-run prediction:** `failed-policy` / `canonical_missing` / exit 1, because the explicit head contains zero canonical links. This was derived before running the audit.

Exact audit command:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-SurfacePlazir27Kimi-iBfG/manifest.json --json
```

Exact observed stdout and exit:

```text
{"findings":[{"id":"canonical_missing","page":"https://plazir27.kimi.page/"}],"pagesChecked":1,"verdict":"failed-policy"}
Command exited with code 1
```

The expected canonical is right as a *local policy* because `SKILL.md`'s charter GHP property-map row says “canonical doc, all kimi variants `rel=canonical` here.” The page itself declares no alternative; it serves a 404 page with no canonical. Thus the expected target is supported by the property map, while the live declaration is absent and fails that local policy. The offline audit evaluates the saved HTML against the manifest; it does not prove Google-selected canonical, HTTP redirect/header canonical, or publication readiness.

**Smallest documented upstream fix (not applied):** PQ-3 in `corpus/knowledge/publish-queue.md` names refreshing `plazir27-kimi-page` from the charter source via its metered-fire + human-publish path; it sequences to PQ-12 for beat-marker re-pin after publish. That queue preflight is historical and must be revalidated against this newly observed 404 before any operator action. No chat, fire, publish, source edit, or policy change was performed.

#### C1 property-map receipt

```json
{
  "unit": "property-map",
  "path": "/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "canonical doc, all kimi variants `rel=canonical` here",
      "claim": "The property map designates the charter GHP URL as canonical for all Kimi variants, so it is the correct local expectedCanonical for plazir27.kimi.page.",
      "surface": "git -C /home/vgpnk/Projects/shokunin/kake-shokunin show b5d599e19bead54b96f589444e9ec64cdf67c28a:SKILL.md",
      "method": "git",
      "observation": "The charter GHP row says: `| charter GHP front | `https://veigapunk.github.io/charter-ufo-fsd/` | `~/Projects/origin-work/charter-ufo-fsd` | Pages deploy from branch (no workflow file); canonical doc, all kimi variants `rel=canonical` here |`. The C2 manifest target is that exact URL.",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "plazir27.kimi.page | `https://plazir27.kimi.page/` | charter repo | canonical kimi charter mirror",
      "claim": "The property map's plazir27 Kimi URL is presently serving the described charter mirror.",
      "surface": "GET https://plazir27.kimi.page/",
      "method": "GET",
      "observation": "status=404; final_url=https://plazir27.kimi.page/; content_type=text/html; charset=utf-8; body sha256=93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966; head title is 404.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, the listed URL returns HTTP 404 with the generic Kimi 404 body (sha256 93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966), so it is not serving a live charter mirror."
    },
    {
      "id": "c1",
      "anchor": "(stale: serves 09-18 beat, canonical 09-28)",
      "claim": "The current Kimi response serves the 09-18 charter beat with a 09-28 canonical.",
      "surface": "GET https://plazir27.kimi.page/",
      "method": "GET",
      "observation": "status=404; final_url=https://plazir27.kimi.page/; content_type=text/html; charset=utf-8; body sha256=93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966; the explicit head has `<title>404</title>` and zero canonical links.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, the listed URL returns a 404 page whose explicit head has no canonical link, so neither the stated 09-18 content nor its 09-28 canonical is present in the live response."
    }
  ]
}
```

## Checked and held

- Read the frozen round-22 canonical policy, round-23 C2 surface record, round-23 C1 unit population, the property-map rows in `SKILL.md`, and the documented PQ-3/PQ-12 rows.
- Performed exactly one GET for `https://plazir27.kimi.page/`; audit ran only on its saved local snapshot.
- Held the map's charter-GHP canonical policy; stale is the map's assertion that this URL currently serves the described mirror/vintage.
- Named PQ-3/PQ-12 only; did not apply the fix.

## Limits

Only the requested surface was fetched. The expected charter GHP URL was not fetched independently, and this result cannot establish its current availability or Google canonical selection. No Kimi account, browser, publishing, deploy, or source-tree operation was used.
