## Verdict

P1 — Operability: the one GET returned HTTP 404, and the frozen static canonical policy correctly predicts `failed-policy` / `canonical_missing` / exit 1. The supplied `expectedCanonical` matches the property map's Plazir15 GHP front and is appropriate as the intended target for a recreated mirror; it is not a declaration observed on today's Kimi 404 page. The property map calls this a dead slot and a `RECREATE` path. Upstream remediation is to restore/recreate and publish the mirror with one head canonical to the GHP front; no fix or publication was applied.

## Findings

### P1 — C2 operability: dead slot has no canonical

Exact request used (one GET; headers and body saved under `/tmp/kake-r23-SurfacePlazir15Kimi-bnbU`): `curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D "$tmp/h" -o "$tmp/b" -w 'http_status=%{http_code}\nfinal_url=%{url_effective}\ncontent_type=%{content_type}\n' 'https://plazir15.kimi.page/'`, where `tmp=/tmp/kake-r23-SurfacePlazir15Kimi-bnbU`.

Exact curl/sha256 output:

> `http_status=404`  
> `final_url=https://plazir15.kimi.page/`  
> `content_type=text/html; charset=utf-8`  
> `snapshot_dir=/tmp/kake-r23-SurfacePlazir15Kimi-bnbU`  
> `93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966  /tmp/kake-r23-SurfacePlazir15Kimi-bnbU/b`

The saved response headers begin `HTTP/2 404` and `content-type: text/html; charset=utf-8`. Before running `canonical_audit.py`, I read the captured head by eye: it opens at `<head>`, contains `<title>404</title>`, closes at `</head>`, and has no `<link rel="canonical">`. The body says `404 Page Not Found`. Under the round-22 contract's rule “Exactly one canonical link in explicit head per page ... compare ... to expectedCanonical,” the predicted result was one `canonical_missing` finding and a `failed-policy` verdict (exit 1).

Actual command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-SurfacePlazir15Kimi-bnbU/manifest.json --json`

Exact stdout: `{"findings":[{"id":"canonical_missing","page":"https://plazir15.kimi.page/"}],"pagesChecked":1,"verdict":"failed-policy"}`; exact process status: `process_exit=1`. The observed result matches the pre-run prediction. This offline auditor evaluated the saved HTML only; the GET is the independent evidence of the live 404.

**Policy judgment:** The `expectedCanonical` value `https://veigapunk.github.io/plazir-15-site/` matches the property-map row naming that URL as `plazir15 GHP front`. Thus it is a sound intended target for a *recreated mirror*. The current page is not mirror content and does not declare any canonical, so its own declaration cannot confirm that relationship; for the present 404 response the canonical relationship is unverifiable. Treating the given target as a required value for a future published mirror is reasonable, but the current surface is not an operable published mirror.

**Smallest upstream fix (documented only; not applied):** follow the map's `RECREATE path` for `plazir15.kimi.page`, restore/recreate and publish the mirror, and ensure its explicit head contains exactly one canonical link to `https://veigapunk.github.io/plazir-15-site/`. The mapped source directory `/home/vgpnk/Projects/plazir-15-site` was absent on this host (`test -d` output: `source_dir=absent`), so recovery/recreation is upstream work; adding a tag to the provider's generic 404 page would not restore the mirror.

### P2 — C1 freshness: property-map receipt

The `property-map` unit and `SKILL.md` path match `.ufo/waves/round-23/c1-population.json`. Anchors below are exact substrings of `SKILL.md` at base `b5d599e19bead54b96f589444e9ec64cdf67c28a`. The receipt distinguishes the source-map entries from what the live 404 can establish.

```json
{
  "unit": "property-map",
  "path": "SKILL.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1-primary",
      "anchor": "| plazir15 GHP front | `https://veigapunk.github.io/plazir-15-site/` | `~/Projects/plazir-15-site` | GH Actions on push to `main` |",
      "claim": "The property map designates https://veigapunk.github.io/plazir-15-site/ as the plazir15 GHP front and records GH Actions on push to main.",
      "surface": "git -C /home/vgpnk/Projects/shokunin/kake-shokunin show b5d599e19bead54b96f589444e9ec64cdf67c28a:SKILL.md > /tmp/kake-r23-SurfacePlazir15Kimi-bnbU/SKILL-base.md",
      "method": "git",
      "observation": "| plazir15 GHP front | `https://veigapunk.github.io/plazir-15-site/` | `~/Projects/plazir-15-site` | GH Actions on push to `main` |",
      "verdict": "HOLD"
    },
    {
      "id": "c1-slot-map",
      "anchor": "| plazir15.kimi.page | 404 dead slot | `~/Projects/plazir-15-site` | RECREATE path — no bound chat;",
      "claim": "The property map records plazir15.kimi.page as a 404 dead slot with a RECREATE path and no bound chat.",
      "surface": "git -C /home/vgpnk/Projects/shokunin/kake-shokunin show b5d599e19bead54b96f589444e9ec64cdf67c28a:SKILL.md > /tmp/kake-r23-SurfacePlazir15Kimi-bnbU/SKILL-base.md",
      "method": "git",
      "observation": "| plazir15.kimi.page | 404 dead slot | `~/Projects/plazir-15-site` | RECREATE path — no bound chat; vessel `1a0c2186-fa12` is empty",
      "verdict": "HOLD"
    },
    {
      "id": "c1-live-status",
      "anchor": "| plazir15.kimi.page | 404 dead slot |",
      "claim": "The mapped public Kimi URL still returns a 404, matching the map's dead-slot status.",
      "surface": "https://plazir15.kimi.page/",
      "method": "GET",
      "observation": "http_status=404; final_url=https://plazir15.kimi.page/; content_type=text/html; charset=utf-8; SHA-256 93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966",
      "verdict": "HOLD"
    },
    {
      "id": "c1-source-path",
      "anchor": "`~/Projects/plazir-15-site` | RECREATE path — no bound chat;",
      "claim": "The source directory mapped to this Kimi surface is absent on this host, consistent with the row's historical absence note.",
      "surface": "test -d /home/vgpnk/Projects/plazir-15-site",
      "method": "run",
      "observation": "source_dir=absent",
      "verdict": "HOLD"
    },
    {
      "id": "c1-intended-canonical",
      "anchor": "| plazir15.kimi.page | 404 dead slot |",
      "claim": "[INFERENCE] For a recreated mirror, the GHP front is the intended canonical target; no current Kimi mirror declaration is established.",
      "surface": "https://plazir15.kimi.page/",
      "method": "GET",
      "observation": "HTTP/2 404; head contains <title>404</title> and </head>, with no <link rel=canonical>.",
      "verdict": "UNVERIFIABLE",
      "reason": "The URL serves the provider's 404 page rather than mirror content, so no live mirror declaration exists to verify the intended canonical relationship."
    }
  ]
}
```

## Checked and held

- The base-commit property-map rows were read from `git show ...:SKILL.md`; the C1 population names `property-map` at `SKILL.md`.
- One public GET only, with no cookies/authentication; no Kimi chat interaction, publish, deploy, or source modification.
- The manifest used for the audit is `/tmp/kake-r23-SurfacePlazir15Kimi-bnbU/manifest.json`; it points at the saved response body, not a refetch.
- No build, lint, formatter, or test suite was run.

## Limits

- The GHP front URL was not fetched; this assignment used one GET against the Kimi surface. Its designation as the primary is verified as a property-map statement, not by a live response.
- No LSP device/route was exposed in the available tools, so the Markdown property-map rows were checked by literal search and direct file reads; no semantic code-reference claim is made.
- The canonical audit's round-22 policy explicitly does not evaluate HTTP status, publishing readiness, JavaScript, or search-engine canonical selection. The 404 and the audit result are therefore reported as separate observations.
