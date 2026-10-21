# C1 re-verification — publish-channels

Observed 2026-10-21 against the frozen base `b5d599e19bead54b96f589444e9ec64cdf67c28a`. This is scoped author-side evidence for the `freshness` axis only; it is not an independent admission. Eight load-bearing claims were selected. No production file, source checkout, or Kimi session was modified or invoked.

## Verdict

**Recommendation: HOLD for C1 freshness.** The sampled claims include two stale statements, one Kimi operation claim that remains unverifiable, and five current observations held at the time checked. In particular, the CNAME statement conflicts with its later round-20 correction, and the setup-script description omits that invoking it again runs another `git push`.

## Findings

### P2 — STALE: the repository CNAME does not configure an Actions-published Pages domain

**Impacted claim/axis:** `publish-channels.md:13`; C1 freshness. **Smallest fix:** replace “CNAME file pins `ds4cc.com`” with a version that says the file contains that value but does not configure an Actions-published site's domain; identify Pages settings/API as the configuration source.

**Exact checks/outputs:** GET `https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/CNAME` returned `status=200 content_type=text/plain; charset=utf-8 bytes=9`; its body was `ds4cc.com`. GET the GitHub custom-domain documentation returned `status=200 content_type=text/html; charset=utf-8 bytes=240398`; the observed text says: “If you are publishing your site from a custom GitHub Actions workflow, no `CNAME` file is created, and any existing `CNAME` file is ignored and is not required.”

```json
{
  "unit": "publish-channels",
  "path": "corpus/knowledge/publish-channels.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "CNAME file pins `ds4cc.com`.",
      "claim": "The repository CNAME file configures/pins the custom domain for the current Actions-published Pages site.",
      "surface": "GET https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/CNAME; GET https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site",
      "method": "GET",
      "observation": "CNAME GET: status=200 content_type=text/plain; charset=utf-8 bytes=9; body: ds4cc.com. GitHub Docs GET: status=200 content_type=text/html; charset=utf-8 bytes=240398; exact text: `If you are publishing your site from a custom GitHub Actions workflow, no CNAME file is created, and any existing CNAME file is ignored and is not required.`",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, the repository CNAME file contains `ds4cc.com`, but an Actions-published Pages site ignores it for domain configuration; configure that domain in Pages settings or through the Pages API.",
      "reason": ""
    }
  ]
}
```

### P2 — STALE: the setup helper does not enforce a single push

**Impacted claim/axis:** `publish-channels.md:16–18`; C1 freshness and publishing safety. **Smallest fix:** describe the push as occurring on each invocation; retain that the Pages workflow, not this helper, deploys the artifact.

**Exact check/output:** GET `https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/deploy-github-pages.sh` returned `status=200 content_type=text/plain; charset=utf-8 bytes=814`. The current file contains `git remote add origin "git@github.com:${GITHUB_REPO}.git" || true` followed by unconditional `git push -u origin main`; it also prints `Pages deploys via .github/workflows/pages.yml (Source = GitHub Actions).` No script was run.

```json
{
  "unit": "publish-channels",
  "path": "corpus/knowledge/publish-channels.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "adds origin, pushes once, prints the DNS records (apex A/AAAA, www CNAME).",
      "claim": "The current setup helper performs one push only and has a run-once guard.",
      "surface": "GET https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/deploy-github-pages.sh",
      "method": "GET",
      "observation": "GET returned status=200 content_type=text/plain; charset=utf-8 bytes=814. Exact lines: `git remote add origin \"git@github.com:${GITHUB_REPO}.git\" || true`; `git push -u origin main`; `echo \"Pages deploys via .github/workflows/pages.yml (Source = GitHub Actions).\"`.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, the script has no run-once guard and executes `git push -u origin main` on every invocation, so the unit should describe the push as per-invocation rather than ‘once’.",
      "reason": ""
    }
  ]
}
```

### P2 — UNVERIFIABLE: current Kimi publish/metering behavior

**Impacted claim/axis:** the Kimi CLI verb, metering, human publish gate, and post-click claims in `publish-channels.md:32–54`; C1 freshness. **Smallest fix:** re-derive these details from a restored, current source and an allowed current observation, or retire them; do not treat the 2026-09/2026-10 observations as live confirmation.

**Exact checks/outputs:** `test -e /home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs` → `ABSENT /home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs`; `test -e /home/vgpnk/Projects/webzites/fleet/kimi-surface-ops.md` → `ABSENT /home/vgpnk/Projects/webzites/fleet/kimi-surface-ops.md`; `command -v kimi-webbridge` → `ABSENT: kimi-webbridge is not in PATH`; unauthenticated GET `https://www.kimi.ai/apiv2/` → body `404 page not found`, then `status=404 content_type=text/plain; charset=utf-8 bytes=19`. No authenticated UI, Kimi chat, or stateful API operation was accessed.

```json
{
  "unit": "publish-channels",
  "path": "corpus/knowledge/publish-channels.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "| `update <id> --chat=<uuidv8>` | chat bound to live URL | `--fire --confirm=<id>` = 1 fire |",
      "claim": "The Kimi script still enforces the listed update precondition and one-fire confirmation gate, with the documented human publish and post-click verification sequence.",
      "surface": "test -e /home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs; test -e /home/vgpnk/Projects/webzites/fleet/kimi-surface-ops.md; command -v kimi-webbridge; unauthenticated GET https://www.kimi.ai/apiv2/",
      "method": "run",
      "observation": "The two local source paths returned ABSENT; `command -v kimi-webbridge` returned `ABSENT: kimi-webbridge is not in PATH`. The public unauthenticated GET returned `404 page not found` and `status=404 content_type=text/plain; charset=utf-8 bytes=19`.",
      "verdict": "UNVERIFIABLE",
      "correction": "",
      "reason": "The cited CLI and operations sources are absent, and the host's missing `kimi-webbridge` command does not establish the absence or behavior of every possible channel. An unauthenticated GET of the API root does not determine whether cookie-authenticated methods or the human-gated UI flow exist; those flows were not accessed under the no-auth/no-chat boundary."
    }
  ]
}
```

## Checked and held

### C1 HOLD — the historical local source trees are absent at their recorded paths

**Exact check/output:** `for p in /home/vgpnk/Projects/ds4cc-marketplace /home/vgpnk/Projects/plazir-15-site /home/vgpnk/Projects/webzites /home/vgpnk/Projects/ephemeral/wz1/ds4cc; do if test -e "$p"; then printf 'EXISTS %s\n' "$p"; else printf 'ABSENT %s\n' "$p"; fi; done` produced four `ABSENT` lines for those exact paths. This is a host-local observation, not evidence that corresponding public repositories are gone.

```json
{
  "unit": "publish-channels",
  "path": "corpus/knowledge/publish-channels.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "the external source trees are absent after the 2026-10-12 prune.",
      "claim": "The named historical project/workspace trees remain absent at their recorded local paths on this host.",
      "surface": "for p in /home/vgpnk/Projects/ds4cc-marketplace /home/vgpnk/Projects/plazir-15-site /home/vgpnk/Projects/webzites /home/vgpnk/Projects/ephemeral/wz1/ds4cc; do if test -e \"$p\"; then printf 'EXISTS %s\\n' \"$p\"; else printf 'ABSENT %s\\n' \"$p\"; fi; done",
      "method": "test -e",
      "observation": "ABSENT /home/vgpnk/Projects/ds4cc-marketplace; ABSENT /home/vgpnk/Projects/plazir-15-site; ABSENT /home/vgpnk/Projects/webzites; ABSENT /home/vgpnk/Projects/ephemeral/wz1/ds4cc.",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    }
  ]
}
```

### C1 HOLD — ds4cc Pages workflow and public surface

**Exact checks/outputs:** GET `https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/.github/workflows/pages.yml` returned `status=200 content_type=text/plain; charset=utf-8 bytes=1789`. The live YAML has `branches: [main]`, the listed JS validation, Kimi archive unittest/build, and `cargo test`, then `uses: actions/upload-pages-artifact@v3` with `path: ./ds4cc-marketplace`, followed by `actions/deploy-pages@v4`. GET `https://ds4cc.com/` returned `status=200 content_type=text/html; charset=utf-8 bytes=76159`; GET `https://ds4cc.com/sitemap.xml` returned `status=200 content_type=application/xml bytes=7565`; the page's extracted canonical is `https://ds4cc.com/` and title is `DS4CC — ship-ready agent software, distributed plainly`.

```json
{
  "unit": "publish-channels",
  "path": "corpus/knowledge/publish-channels.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "- `ds4cc-marketplace/.github/workflows/pages.yml`: on push to main → validate",
      "claim": "The ds4cc Pages workflow still triggers on main, performs the listed checks/build/test, uploads the checked-out project tree, and deploys it; its documented public domain currently serves the site and sitemap.",
      "surface": "GET https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/.github/workflows/pages.yml; GET https://ds4cc.com/; GET https://ds4cc.com/sitemap.xml",
      "method": "GET",
      "observation": "Workflow GET: status=200 content_type=text/plain; charset=utf-8 bytes=1789; observed `branches: [main]`, the listed validation/build/tests, `uses: actions/upload-pages-artifact@v3` with `path: ./ds4cc-marketplace`, and `uses: actions/deploy-pages@v4`. Site GET: `url=https://ds4cc.com/ status=200 content_type=text/html; charset=utf-8 bytes=76159`; sitemap GET: `url=https://ds4cc.com/sitemap.xml status=200 content_type=application/xml bytes=7565`.",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    }
  ]
}
```

### C1 HOLD — Plazir Pages workflow and public project URL

**Exact checks/outputs:** GET `https://raw.githubusercontent.com/VeigaPunk/plazir-15-site/main/.github/workflows/pages.yml` returned `status=200 content_type=text/plain; charset=utf-8 bytes=565`; current YAML triggers on `branches: [main]`, uploads `path: .` with `actions/upload-pages-artifact@v3`, and deploys with `actions/deploy-pages@v4`. GET `https://veigapunk.github.io/plazir-15-site/` returned `status=200 content_type=text/html; charset=utf-8 bytes=38337`, with extracted canonical `https://veigapunk.github.io/plazir-15-site/` and title `Plazir-15 — Domed Paradise of the Outer Rim | Fan Codex`; GET its sitemap returned `status=200 content_type=application/xml bytes=1144`.

```json
{
  "unit": "publish-channels",
  "path": "corpus/knowledge/publish-channels.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "- `plazir-15-site/.github/workflows/pages.yml`: same shape, uploads `.` whole,",
      "claim": "The Plazir Pages workflow still triggers on main, uploads the project root (`.`), and its documented GitHub Pages URL currently serves the expected site and sitemap.",
      "surface": "GET https://raw.githubusercontent.com/VeigaPunk/plazir-15-site/main/.github/workflows/pages.yml; GET https://veigapunk.github.io/plazir-15-site/; GET https://veigapunk.github.io/plazir-15-site/sitemap.xml",
      "method": "GET",
      "observation": "Workflow GET: status=200 content_type=text/plain; charset=utf-8 bytes=565; observed `branches: [main]`, `uses: actions/upload-pages-artifact@v3` with `path: .`, and `uses: actions/deploy-pages@v4`. Site GET: `url=https://veigapunk.github.io/plazir-15-site/ status=200 content_type=text/html; charset=utf-8 bytes=38337`; extracted canonical matches that URL. Sitemap GET: `url=https://veigapunk.github.io/plazir-15-site/sitemap.xml status=200 content_type=application/xml bytes=1144`.",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    }
  ]
}
```

### C1 HOLD — Render configuration and live health endpoint

**Exact checks/outputs:** GET `https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/render.yaml` returned `status=200 content_type=text/plain; charset=utf-8 bytes=565`; current file has `name: ds4cc-marketplace-app`, `runtime: docker`, `dockerfilePath: ./apps-sdk/Dockerfile`, `healthCheckPath: /health`, `APP_ORIGIN: https://app.ds4cc.com`, and `ALLOWED_ORIGINS: https://chatgpt.com`. GET `https://app.ds4cc.com/health` returned `status=200 content_type=application/json; charset=utf-8 bytes=63`; body: `{"status":"ok","service":"ds4cc-marketplace","version":"1.0.0"}`.

```json
{
  "unit": "publish-channels",
  "path": "corpus/knowledge/publish-channels.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "`ds4cc-marketplace/render.yaml`: Docker web service `ds4cc-marketplace-app`,",
      "claim": "The Render configuration still names the Docker web service, Dockerfile, health path, APP_ORIGIN, and ALLOWED_ORIGINS as stated, and the public health endpoint currently reports healthy.",
      "surface": "GET https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/render.yaml; GET https://app.ds4cc.com/health",
      "method": "GET",
      "observation": "render.yaml GET: status=200 content_type=text/plain; charset=utf-8 bytes=565; observed `name: ds4cc-marketplace-app`, `runtime: docker`, `dockerfilePath: ./apps-sdk/Dockerfile`, `healthCheckPath: /health`, `APP_ORIGIN` = `https://app.ds4cc.com`, `ALLOWED_ORIGINS` = `https://chatgpt.com`. Health GET: `status=200 content_type=application/json; charset=utf-8 bytes=63`; body: `{\"status\":\"ok\",\"service\":\"ds4cc-marketplace\",\"version\":\"1.0.0\"}`.",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    }
  ]
}
```

### C1 HOLD — versioned upload-artifact correction

**Exact checks/outputs:** the pinned upload action v4 source GET returned `status=200 content_type=text/plain; charset=utf-8 bytes=2529` and includes exclusions `--exclude=.git`, `--exclude=.github`, and `--exclude=".[^/]*"`. The v5 source GET returned `status=200 content_type=text/plain; charset=utf-8 bytes=2895`, defines `include-hidden-files` with default `false`, and keeps `.git`/`.github` excluded. The live ds4cc workflow above uses `upload-pages-artifact@v3`; its v3 source GET returned `status=200 content_type=text/plain; charset=utf-8 bytes=2389` and shows `.git`/`.github` exclusions without the v4 hidden-path exclusion or v5 input. Thus the v4/v5 correction is held as version-specific, not as a statement of the current ds4cc workflow's action version.

```json
{
  "unit": "publish-channels",
  "path": "corpus/knowledge/publish-channels.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "the uploaded artifact is not the full checkout; .git/.github are excluded and v4 excludes hidden paths by default",
      "claim": "The version-qualified action correction is current: v4 excludes hidden paths by default in addition to `.git`/`.github`, and v5 adds an `include-hidden-files` option defaulting to false while always excluding `.git`/`.github`.",
      "surface": "GET https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml; GET https://raw.githubusercontent.com/actions/upload-pages-artifact/fc324d3547104276b827a68afc52ff2a11cc49c9/action.yml; GET https://raw.githubusercontent.com/actions/upload-pages-artifact/v3/action.yml; GET https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/.github/workflows/pages.yml",
      "method": "GET",
      "observation": "v4 source: status=200, 2529 bytes; includes `--exclude=.[^/]*` with `.git`/`.github` exclusions. v5 source: status=200, 2895 bytes; input description says hidden files are excluded by default, `include-hidden-files` defaults to `false`, and `.git`/`.github` remain excluded. Current ds4cc workflow source uses `actions/upload-pages-artifact@v3`; v3 source status=200, 2389 bytes and has `.git`/`.github` exclusions but no hidden-file exclusion/input.",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    }
  ]
}
```

## Limits

- **Skipped as separate claims:** Plazir's assertion that no custom domain is configured. The workflow and live canonical URL were checked, but current Pages settings/API state is not visible from those public GETs and I did not access an authenticated GitHub account.
- **Skipped as separate Kimi claims:** exact `sync-check`/`kimi-map` semantics; update/recreate/rebuild preconditions and fire metering; whether the Publish / Share→Update click is human; the `AppService/PublishApp` and `OKCService/PublishDeployment` methods; the assertion that `DuplicateApp` is never called; and the post-click `GetWebsiteByChatID`/`PUBLISHED`/marker sequence. The source files are absent, `kimi-webbridge` is not in PATH, and verifying the remainder would require the prohibited authenticated Kimi UI/session or API interaction. The unauthenticated API-root 404 is not evidence that authenticated methods are absent.
- **Skipped historical patch protocol:** `git format-patch` plus `publish/APPLY.md` and `git am --check` on a fresh clone. `/home/vgpnk/Projects/ephemeral/wz1/ds4cc` is absent; the public current path `https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/main/publish/APPLY.md` returned `status=404 content_type=text/plain; charset=utf-8 bytes=14`. I did not create a clone or run the historical procedure.
- Public GET observations are snapshots, not guarantees. Pages workflow/settings claims are not inferred from successful site responses alone; CNAME behavior is supported by current GitHub documentation. Kimi observations remain historical/unverifiable. No builds, linters, formatters, tests, publishing commands, or stateful operations were run; no tool was installed or updated.
