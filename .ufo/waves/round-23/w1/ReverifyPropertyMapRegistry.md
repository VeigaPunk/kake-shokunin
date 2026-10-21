## Verdict

C1 `property-map` is **STALE** on local source pointers and the second registry path. The checked ds4cc/plazir Actions workflows, ds4cc CNAME content, charter branch-publish statement, and app Render descriptor are supported by current public repository content. The app endpoint answered one GET with HTTP 400. This is a scoped freshness recommendation, not independent admission.

## Findings

### P2 — Several mapped local source directories are absent

**Impacted claim/axis:** `SKILL.md:17,20,26-27`, C1 property-map source-directory claims / freshness.

**Exact command:**
```sh
for p in /home/vgpnk/Projects/ds4cc-marketplace /home/vgpnk/Projects/plazir-15-site /home/vgpnk/Projects/origin-work/charter-ufo-fsd /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome /home/vgpnk/Projects/lucario /home/vgpnk/Projects/lucario/site /home/vgpnk/Projects/ds4cc-marketplace/apps-sdk /home/vgpnk/Projects/ds4cc-marketplace/render.yaml /home/vgpnk/Projects/webzites/fleet/fleet.config.json /home/vgpnk/Projects/webzites/fleet/grokbots.json; do if test -e "$p"; then printf 'PRESENT %s\n' "$p"; else printf 'ABSENT %s\n' "$p"; fi; done
```

**Exact observed output:**
```text
ABSENT /home/vgpnk/Projects/ds4cc-marketplace
ABSENT /home/vgpnk/Projects/plazir-15-site
ABSENT /home/vgpnk/Projects/origin-work/charter-ufo-fsd
ABSENT /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome
ABSENT /home/vgpnk/Projects/lucario
ABSENT /home/vgpnk/Projects/lucario/site
ABSENT /home/vgpnk/Projects/ds4cc-marketplace/apps-sdk
ABSENT /home/vgpnk/Projects/ds4cc-marketplace/render.yaml
ABSENT /home/vgpnk/Projects/webzites/fleet/fleet.config.json
ABSENT /home/vgpnk/Projects/webzites/fleet/grokbots.json
```

The ds4cc and charter roots and the plazir dead-slot row have explicit missing-path annotations in the map. The active plazir-front row, burnerchrome row, and lucario rows still present local paths without an equivalent unavailable note. The remote ds4cc repo separately contains the app files cited by row 28 (see held evidence below); this local absence is not evidence that the public remote files are gone.

**Smallest fix:** mark the absent local source paths as unavailable/historical or replace them only with a verified current local path.

### P2 — The second registry path is not present at the implied location

**Impacted claim/axis:** `SKILL.md:34-36`, C1 registry-of-record path / freshness.

**Exact command:** the `test -e` loop above.

**Exact observed output:** `ABSENT /home/vgpnk/Projects/webzites/fleet/grokbots.json`.

The first registry path is explicitly annotated as a historical record after its disappearance; the second registry is still described as a 20-row registry without a corresponding missing-path note.

**Smallest fix:** mark the second-registry path unavailable/historical or replace it with a verified current absolute path.

## Checked and held

- The source text is unchanged from the stated base: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --no-ext-diff --unified=0 b5d599e19bead54b96f589444e9ec64cdf67c28a -- SKILL.md` produced no diff; the combined command then printed `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b` from `rev-parse HEAD`. Anchors below therefore match the base text.
- `GET https://raw.githubusercontent.com/veigapunk/ds4cc-marketplace/main/.github/workflows/pages.yml` returned the current workflow body containing `on:` / `push:` / `branches: [main]`. `GET https://raw.githubusercontent.com/veigapunk/ds4cc-marketplace/main/CNAME` returned exactly `ds4cc.com`.
- `GET https://raw.githubusercontent.com/veigapunk/plazir-15-site/main/.github/workflows/pages.yml` returned the current workflow body containing `on:` / `push:` / `branches: [main]`.
- The local publish-path `test -e` checks returned `ABSENT` for both repos' local `.github/workflows` directories and the local ds4cc `CNAME`; these local results are distinct from the public-remote content above.
- `GET https://github.com/VeigaPunk/charter-ufo-fsd` returned the public repository page on `main`; its README states `Pages: deploy from main / root`. `GET https://github.com/VeigaPunk/charter-ufo-fsd/tree/main/.github/workflows` returned HTTP 404, consistent with the checked no-workflow statement.
- `GET https://raw.githubusercontent.com/veigapunk/ds4cc-marketplace/main/render.yaml` returned a descriptor with `type: web`, `name: ds4cc-marketplace-app`, `runtime: docker`, and `dockerfilePath: ./apps-sdk/Dockerfile`; `GET https://raw.githubusercontent.com/veigapunk/ds4cc-marketplace/main/apps-sdk/Dockerfile` returned the Dockerfile. This supports the row's remote Render/source mapping.
- **Exact one-GET endpoint check:** `curl --silent --show-error --output /dev/null --write-out 'HTTP %{http_code}\n' --max-time 20 https://app.ds4cc.com/mcp` printed exactly `HTTP 400`. The endpoint returned an HTTP response; this is not evidence of successful MCP protocol behavior.
- Receipt (exactly one C1 JSON block):

```json
{
  "unit": "property-map",
  "path": "SKILL.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "GH Actions on push to `main` (`CNAME` = ds4cc.com)",
      "claim": "The public ds4cc and plazir-15 repositories currently have Pages workflows triggered on push to main, and the ds4cc root CNAME contains ds4cc.com; this verifies repository content, not the live Pages custom-domain setting.",
      "surface": "GET https://raw.githubusercontent.com/veigapunk/ds4cc-marketplace/main/.github/workflows/pages.yml; GET https://raw.githubusercontent.com/veigapunk/ds4cc-marketplace/main/CNAME; GET https://raw.githubusercontent.com/veigapunk/plazir-15-site/main/.github/workflows/pages.yml",
      "method": "GET",
      "observation": "Both pages.yml bodies contain `on:`, `push:`, `branches: [main]`; the CNAME response body is exactly `ds4cc.com`.",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    },
    {
      "id": "c1",
      "anchor": "| burnerchrome kimi | `https://burnerchrome.kimi.page/` | `~/Projects/ds4cc-marketplace/burnerchrome` | Kimi surface, chat `1a0ada42-28e2…` |",
      "claim": "The mapped local source directories for the active plazir front, burnerchrome, and lucario (including lucario/site) are absent; the explicit-path test output is recorded below. The missing ds4cc and charter roots and the plazir dead-slot path are separately annotated as historical/unavailable in the source map.",
      "surface": "test -e /home/vgpnk/Projects/plazir-15-site; test -e /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome; test -e /home/vgpnk/Projects/lucario; test -e /home/vgpnk/Projects/lucario/site",
      "method": "test -e",
      "observation": "ABSENT /home/vgpnk/Projects/plazir-15-site; ABSENT /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome; ABSENT /home/vgpnk/Projects/lucario; ABSENT /home/vgpnk/Projects/lucario/site.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, `/home/vgpnk/Projects/plazir-15-site`, `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome`, `/home/vgpnk/Projects/lucario`, and `/home/vgpnk/Projects/lucario/site` are absent, so these mapped local source paths need a verified replacement or an explicit unavailable/history annotation.",
      "reason": ""
    },
    {
      "id": "c1",
      "anchor": "| vault index | `https://veigapunk.kimi.page/` | none on disk | Kimi surface, chat `1a0c20ea-6372…` — NEVER fire into this chat, it hot-swaps the live vault |",
      "claim": "The pathless source declarations (`none on disk`, `none (Vite shell)`) and Kimi chat-binding/empty-vessel claims in the map cannot be decided by the required directory tests or a non-mutating public repository read; no Kimi interaction or MCP call was made, and page-serving status is left to sibling checks.",
      "surface": "SKILL.md rows 19-25; no specific local path for `test -e` and no read-only chat-binding surface used",
      "method": "read",
      "observation": "The rows provide no absolute source directory for the `none` entries; no live chat-binding observation was collected.",
      "verdict": "UNVERIFIABLE",
      "correction": "",
      "reason": "There is no named filesystem path for the pathless source declarations, and verifying Kimi chat bindings would require a separate read-only authority not used or exposed in this lane; chat writes and page-status rechecks are outside scope."
    },
    {
      "id": "c1",
      "anchor": "Pages deploy from branch (no workflow file)",
      "claim": "The charter repository's public README says GitHub Pages deploys from main/root, and its main-branch `.github/workflows` listing returns HTTP 404, consistent with branch deployment without a workflow file.",
      "surface": "GET https://github.com/VeigaPunk/charter-ufo-fsd; GET https://github.com/VeigaPunk/charter-ufo-fsd/tree/main/.github/workflows",
      "method": "GET",
      "observation": "Repository page is public on `main`; README says `Pages: deploy from main / root`; workflow-directory request returned HTTP 404.",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    },
    {
      "id": "c1",
      "anchor": "Pages branch deploy on push — live 200, verified 09-28",
      "claim": "The current lucario Pages deployment mode cannot be reverified from the local source or the guessed public repository URL.",
      "surface": "test -e /home/vgpnk/Projects/lucario; GET https://github.com/VeigaPunk/lucario",
      "method": "GET",
      "observation": "Local source directory is absent; the GitHub repository request returned HTTP 404.",
      "verdict": "UNVERIFIABLE",
      "correction": "",
      "reason": "The local checkout is absent and the public GitHub URL returned 404, which does not establish whether the repository is private, renamed, or removed; no live Pages settings authority was available."
    },
    {
      "id": "c1",
      "anchor": "| app.ds4cc.com | `https://app.ds4cc.com/mcp` | `ds4cc-marketplace/apps-sdk` + `render.yaml`",
      "claim": "The public Render descriptor points at a Docker web service and `./apps-sdk/Dockerfile`; the cited Dockerfile is present, and one GET to the MCP route receives an HTTP response.",
      "surface": "GET https://raw.githubusercontent.com/veigapunk/ds4cc-marketplace/main/render.yaml; GET https://raw.githubusercontent.com/veigapunk/ds4cc-marketplace/main/apps-sdk/Dockerfile; GET https://app.ds4cc.com/mcp",
      "method": "GET",
      "observation": "render.yaml: `type: web`, `name: ds4cc-marketplace-app`, `runtime: docker`, `dockerfilePath: ./apps-sdk/Dockerfile`; Dockerfile GET returned source; endpoint GET printed `HTTP 400`.",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    },
    {
      "id": "c1",
      "anchor": "Registry of record: `~/Projects/webzites/fleet/fleet.config.json`",
      "claim": "The first registry path is absent locally, and the map explicitly marks it as gone and retained only as a historical record.",
      "surface": "test -e /home/vgpnk/Projects/webzites/fleet/fleet.config.json",
      "method": "test -e",
      "observation": "ABSENT /home/vgpnk/Projects/webzites/fleet/fleet.config.json; SKILL.md line 30's adjacent r18 note calls it absent and historical.",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    },
    {
      "id": "c1",
      "anchor": "Second registry: `fleet/grokbots.json` (20 roster rows, mtime 2026-09-20)",
      "claim": "Interpreting the relative second-registry path under the same `~/Projects/webzites` root, the file is absent and the paragraph does not annotate that registry as historical.",
      "surface": "test -e /home/vgpnk/Projects/webzites/fleet/grokbots.json",
      "method": "test -e",
      "observation": "ABSENT /home/vgpnk/Projects/webzites/fleet/grokbots.json.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, `/home/vgpnk/Projects/webzites/fleet/grokbots.json` is absent, so mark this second-registry location unavailable/historical or replace it with a verified current absolute path.",
      "reason": ""
    }
  ]
}
```

## Limits

- I did not request the 12 property-map page URLs; sibling items own those checks. The only application URL request was the required single GET to `/mcp`.
- I did not query or write to Kimi chats. The pathless source labels and chat bindings remain unverifiable.
- GitHub contents API requests returned HTTP 403, so workflow/CNAME/Render checks used public GitHub pages and raw file URLs instead. The lucario public repository URL returned 404, so its publishing configuration remains unresolved.
- A Projects-wide glob for registry filenames timed out and explicitly reported an incomplete scan; this is not evidence of absence. The exact declared registry paths were tested directly.
- No LSP device was available in the mounted tool inventory; no semantic caller/reference claim is made. No tools were installed or updated.
