## Verdict

C1 `ghp-subpath-spotcheck` recheck is mixed: 4 HOLD, 1 UNVERIFIABLE, 2 STALE. The current public route checks are reproducible, but the `webzites` implementation claims remain unverified because their source and CLI are absent. This is an author-side freshness receipt, not an independent admission.

## Findings

- **P2 — UNVERIFIABLE implementation behavior (freshness).** The unit's root-only `probe`, one-file `reconcile`, and title/marker-only `in-sync` rules cannot be checked against the current implementation. Read-only checks returned `absent /home/vgpnk/Projects/webzites/src/probe.mjs` and `absent /home/vgpnk/Projects/webzites/src/reconcile.mjs`; `command -v webzites` returned no path. Smallest correction: restore the referenced source/CLI for re-verification, or retire/update these behavior claims from a current implementation source.
- **P3 — STALE missing-page title (freshness).** Exact command: `curl -sS --max-time 25 -o /dev/null -w 'GET status=%{http_code} effective=%{url_effective} redirect=%{redirect_url} type=%{content_type}\n' 'https://veigapunk.github.io/plazir-15-site/__r23-nonexistent-20261021__'`. Exact output: `https://veigapunk.github.io/plazir-15-site/__r23-nonexistent-20261021__ GET status=404 effective=https://veigapunk.github.io/plazir-15-site/__r23-nonexistent-20261021__ redirect= type=text/html; charset=utf-8`. `curl` SHA-256 of that body and `/404.html` was `f02b656cb925f54b069dbe82e78bd58daea8556428615b0020fa7a6955810f11`; raw `/404.html` has `<title>Not found — Plazir-15</title>` (though its body still says “Page not found”). Smallest correction: replace the old title claim with the current title while retaining the observed HTTP 404 behavior.
- **P2 — STALE unresolved `/CNAME` prediction (freshness).** Exact command: `curl -sS --max-time 25 -o /dev/null -w 'GET status=%{http_code} effective=%{url_effective} type=%{content_type}\n' 'https://ds4cc.com/CNAME'`. Exact output: `https://ds4cc.com/CNAME GET status=200 effective=https://ds4cc.com/CNAME type=application/octet-stream`; raw GET body: `ds4cc.com`. Smallest correction: record that the current `ds4cc.com` deployment exposes `/CNAME`, while explicitly not inferring which workflow supplied the bytes.

## Checked and held

The anchors below are copied from the unit at frozen base `b5d599e19bead54b96f589444e9ec64cdf67c28a`. `observedAt` is 2026-10-21.

```json
{
  "unit": "ghp-subpath-spotcheck",
  "path": "corpus/knowledge/ghp-subpath-spotcheck.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "~/Projects/webzites/src/reconcile.mjs:55-107 (absent since the 2026-10-12 prune)",
      "claim": "The cited local reconcile source path is absent at this recheck.",
      "surface": "/home/vgpnk/Projects/webzites/src/reconcile.mjs",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/webzites/src/reconcile.mjs",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "`in-sync` needs only `titleEqual` + marker parity.",
      "claim": "The current webzites behavior is as documented: probe checks only the row root URL, reconcile selects one shallow index.html, and in-sync can accept title/marker parity without byte equality, masking GHP byte drift.",
      "surface": "command -v webzites; /home/vgpnk/Projects/webzites/src/probe.mjs; /home/vgpnk/Projects/webzites/src/reconcile.mjs",
      "method": "run",
      "observation": "source paths absent; command -v webzites produced no path",
      "verdict": "UNVERIFIABLE",
      "reason": "The cited implementation files and webzites executable are absent locally; no current implementation surface can decide these behaviors. The historical 2026-09-28 byte example also has no reproducible audit-file path."
    },
    {
      "id": "c1",
      "anchor": "`/dir` → 301 → `/dir/` → serves `dir/index.html`.",
      "claim": "Current GHP slashless /snake and /magga paths redirect to slash URLs, whose response bytes match their explicit index.html paths.",
      "surface": "https://veigapunk.github.io/plazir-15-site/snake; https://ds4cc.com/magga; both slash and index.html forms",
      "method": "GET",
      "observation": "GET /snake status=301 redirect=https://veigapunk.github.io/plazir-15-site/snake/; followed GET status=200, redirects=1. GET /magga status=301 redirect=https://ds4cc.com/magga/; followed GET status=200, redirects=1. SHA-256 /snake/ and /snake/index.html both d42e5247cf52456efc8c86768ae16c331fd8f06d3914767ff64d00fb12509826; /magga/ and /magga/index.html both 63ba970082ccf115af0c763aa8350f26e35e249058406bdae14cf13bd94642cc.",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "`404.html` at root is honored as the custom 404 body",
      "claim": "The Plazir Pages site serves its root 404.html bytes for missing routes; ds4cc.com does not expose a 404.html file and currently returns the stock GitHub Pages 404 body.",
      "surface": "https://veigapunk.github.io/plazir-15-site/404.html; https://veigapunk.github.io/plazir-15-site/__r23-nonexistent-20261021__; https://ds4cc.com/404.html; https://ds4cc.com/__r23-nonexistent-20261021__",
      "method": "GET",
      "observation": "Plazir /404.html status=200; missing path status=404; both body SHA-256 f02b656cb925f54b069dbe82e78bd58daea8556428615b0020fa7a6955810f11. ds4cc /404.html status=404; missing path status=404; both body SHA-256 b620507312c5e97566a3c6cfaf99144fefc18a0da7d941401dfa0f5f58fb0368; body includes `<title>Page not found &middot; GitHub Pages</title>` and `File not found`.",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "title \"Page not found\"",
      "claim": "The current Plazir GHP missing-page document title is `Page not found`.",
      "surface": "GET https://veigapunk.github.io/plazir-15-site/__r23-nonexistent-20261021__; raw GET https://veigapunk.github.io/plazir-15-site/404.html",
      "method": "GET",
      "observation": "Missing-path GET status=404; its body hash equals /404.html; raw HTML title is `<title>Not found — Plazir-15</title>`.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, the missing path returns HTTP 404 with bytes identical to /404.html, whose HTML title is `Not found — Plazir-15`; the body still contains the words `Page not found`."
    },
    {
      "id": "c1",
      "anchor": "whether Actions serves /CNAME is an unverified prediction requiring an operator-authorized free read",
      "claim": "The note's unresolved `/CNAME` availability question is still open for the current ds4cc.com deployment.",
      "surface": "https://ds4cc.com/CNAME",
      "method": "GET",
      "observation": "GET status=200, Content-Type=application/octet-stream; raw response body `ds4cc.com`.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, GET https://ds4cc.com/CNAME returns HTTP 200 with raw body `ds4cc.com`, so the current ds4cc.com deployment exposes `/CNAME`; this does not establish which publishing workflow supplied it."
    },
    {
      "id": "c1",
      "anchor": "kimi has no directory indexes",
      "claim": "The current ds4cc Kimi mirror reproduces the directory-index contrast on its linked omarchy-usage path: the directory URL is 404 while explicit index.html is 200.",
      "surface": "https://ds4cc.kimi.page/omarchy-usage/; https://ds4cc.kimi.page/omarchy-usage/index.html",
      "method": "GET",
      "observation": "GET /omarchy-usage/ status=404; GET /omarchy-usage/index.html status=200.",
      "verdict": "HOLD"
    }
  ]
}
```

Other checked public responses: `GET https://ds4cc.com/robots.txt` returned 200, `text/plain; charset=utf-8`; `GET https://ds4cc.com/sitemap.xml` returned 200, `application/xml`. The live sitemap responses were read successfully. The pinned `actions/upload-pages-artifact` action source excludes `.git`, `.github`, and hidden dotfiles by default, not literal `CNAME`; GitHub's current custom-domain guide says an Actions-published site ignores a CNAME for domain configuration. Neither source identifies the provenance of the current ds4cc `/CNAME` bytes.

## Limits

Skipped claims and reasons:

- The 2026-09-28 `/tmp` census counts (2,352 paths, 2,614 ds4cc files/~1,874 text files), the exact historical zero-rot result, and the `origin/main` ahead/behind / working-tree-diff counts: the baseline is named only as an unspecified `/tmp` audit, the source repositories are absent, and a current probe cannot reproduce those past facts.
- The combined `.md`, `.json`, `.txt`, `.xml`, `.webmanifest` “all served raw” claim: only the current `.txt` and `.xml` examples above were located and checked; the unit supplies no exact live `.md`, `.json`, or `.webmanifest` paths. A public GitHub API tree request to locate a Markdown source failed with HTTP 403, so no extra route was inferred.
- The `kimi-surface.mjs sync-check` implementation and its per-path title/marker behavior: the local executable and source were absent; the one Kimi directory-index route above does not verify the sync-check implementation.
- The unit's unenumerated binary-asset hash coverage and complete live-only/orphan-path census were not re-run; the checks above are targeted samples, not a whole-site sweep.

`read xd://lsp` returned `No such tool: xd://lsp`; no LSP status/references/definition/diagnostics were available. The literal `S001|S005` text search only located the source registry rows and was not treated as semantic proof. No builds, tests, or installs/updates were run.
