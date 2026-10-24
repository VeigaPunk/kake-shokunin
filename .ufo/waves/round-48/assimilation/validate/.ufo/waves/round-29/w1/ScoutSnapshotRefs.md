# ScoutSnapshotRefs — C2 real-world shape: URL-bearing attributes in round-23 snapshots

Lane revision read: `9e541a1d138158cd957c0e7b1a32050478c02dd0` (working tree; `.ufo/waves/round-23/live/` unchanged by me).
Frozen contract used as the reference set: `.ufo/waves/round-29/c2-matrix.json` `interface` (sha256 `75c08f64…acb2e84a`).
`scripts/base_path_audit.py` does **not** exist at this revision (`ls` exit 2), so every verdict below is my independent
implementation of the interface text, not tool output. Nothing was probed live; no tool installed.

## Commands (all run from the sandbox; TMPDIR inside it)

1. `python3 -B scan_refs.py --live <lane>/.ufo/waves/round-23/live --out refs_flat.json` → **exit 0** (base `/` for all, i.e. what round-23 manifests imply).
2. `python3 -B scan_refs.py --live <lane>/.ufo/waves/round-23/live --bases '{"charter-ghp":"/charter-ufo-fsd/","lucario-ghp":"/lucario/","plazir15-ghp":"/plazir-15-site/"}' --out refs_true.json` → **exit 0**.
3. provenance: sha256/size of each `page.html` vs its `fetch.json` → **exit 0**, 8/8 identical sha256 and byte count, `truncated:false`, `redirects:[]`.
4. absence greps over the 8 retained bodies (`grep -ci 'http-equiv'`, `'<base'`, `'srcset'`, `poster=|action=|data-src|data-bg|formaction`, `(href|src)="//'`) → all counts **0**; the only non-zero exit (2) came from the 4 directories that have no `page.html`, not from a match.
5. `cd`-free read of `.ufo/waves/round-23/live/*/manifest.json|audit.json|fetch.json` (12 dirs enumerated).

Sandbox deliverables: `/fast/scratch/hyaku/kake-r29/w1/ScoutSnapshotRefs/{scan_refs.py,refs.json,refs_flat.json,refs_true.json}`.

## Per-snapshot census (in-scope reference instances, all attributes incl. srcset candidates)

The interface's reference set: `a|area|link[href]`, `img|script|iframe|source|audio|video|track|embed[src]`,
`img|source[srcset]` (per candidate), `video[poster]`, `form[action]`; `base[href]` sets the document base.

| snapshot | body | basePath used | relative | root-rel | same-origin-abs | proto-rel | other-origin | non-http | total | outside-base findings |
|---|---|---|---|---|---|---|---|---|---|---|
| burnerchrome-kimi | yes | `/` | 25 | 0 | 0 | 0 | 6 | 0 | 31 | 0 |
| charter-ghp | yes | `/charter-ufo-fsd/` | 15 | 0 | 7 | 0 | 45 | 0 | 67 | **3** |
| charter-kimi | **no** (404) | — | — | — | — | — | — | — | — | n/a |
| ds4cc-kimi | yes | `/` | 36 | 2 | 0 | 0 | 45 | 0 | 83 | 0 |
| ds4cc-primary | yes | `/` | 38 | 0 | 2 | 0 | 43 | 0 | 83 | 0 |
| lucario-ghp | yes | `/lucario/` | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 |
| lucario-kimi | **no** (404) | — | — | — | — | — | — | — | — | n/a |
| plazir15-ghp | yes | `/plazir-15-site/` | 38 | 0 | 2 | 0 | 6 | 0 | 46 | **1** |
| plazir15-kimi | **no** (404) | — | — | — | — | — | — | — | — | n/a |
| plazir27-kimi | **no** (404) | — | — | — | — | — | — | — | — | n/a |
| ufo-fsd-kimi-pro | yes | `/` | 0 | 2 | 0 | 0 | 1 | 0 | 3 | 0 |
| vault-index-kimi | yes | `/` | 0 | 0 | 0 | 0 | 4 | 1 | 5 | 0 |
| **total (8 bodies)** | | | **152** | **4** | **11** | **0** | **151** | **1** | **319** | **4** |

Attribute mix across 319 in-scope instances: `a.href` 279, `link.href` 22, `script.src` 13, `img.src` 5.
Never observed: `area`, `iframe`, `source`, `audio`, `video`, `track`, `embed`, `srcset`, `poster`, `action`, `base`.
Relative composition (152): fragment-only 67, path-relative 53, `./`-relative 32, parent-relative 0.
Entity decoding is exercised: 8 in-scope values contain `&`, encoded `&amp;` in source (e.g. `charter-ghp/page.html` invite URLs), and all 8 are other-origin, so decoding changes no in-scope finding. No whitespace-padded or uppercase element/attribute names.

## Findings for the L1 (advisory)

- **F1 — the target premise overcounts.** 12 live directories, only **8** retain `page.html`. The four `*-kimi` dirs are HTTP 404
  (`fetch.json status:404`, 13409 bytes, all sha256 `93ddca9a0216…8fca966`, `audit.json verdict "not-served"`) with **no retained body**.
  A 12-snapshot census is an 8-body census.
- **F2 — round-23 data cannot express the project base.** Manifests are `{version:1, pages:[{expectedCanonical,file,url}]}`; no `basePath`.
  Under the implied `/`, all 8 bodies project clean. The frontier defect is invisible in the old data — supports treating the C2
  `basePath` field as new capability, not a behavior change.
- **F3 — real project sites trip the anchor rule.** Under the true bases the projection yields exactly 4 findings and **all four are
  `<a href>` to a sibling project on the shared `veigapunk.github.io` origin**: charter-ghp → `/horizon-halo-comma-design/` (×2) and
  `/plazir-15-site/`; plazir15-ghp → `/xbrd-spark/highlights.html`. **0 subresource findings.** Because the interface tests `a/area/link[href]`
  with the same outside-base rule as `img/script[src]`, a working project site that links its siblings exits 1 `failed-policy`.
  The matrix has no case for this; the intended verdict is a design decision for you, not for me.
- **F4 — matrix classes with zero real instances:** srcset (D3), protocol-relative (D5), poster/form action (D10), `<base>` (D7),
  uppercase names (D12), whitespace-wrapped values (D13), case-sensitivity (D9), segment-prefix (D8). The corpus exercises only
  relative, root-relative, same-origin absolute, other origin and non-http. Synthetic coverage for D3/D5/D7/D9/D10/D12/D13 is uncorroborated
  by real data and cannot be validated against it.
- **F5 — the one real migration hazard.** `ufo-fsd-kimi-pro` is a Vite build with root-relative `/assets/index-Bw9NLFv4.js` and
  `/assets/index-B-Hzbnm3.css`; at `https://ufo-fsd.kimi.pro/` that is inside `/` and clean. [INFERENCE] the same `dist/` on a project
  URL would leave `/<repo>/` — the exact frontier defect, and the only snapshot where a project-site move breaks subresources.
- **F6 — forms are JS-driven.** Two `<form>` elements (`lucario-ghp#f`, `plazir15-ghp#charter-ballot`) have **no** `action`; both are
  intercepted by inline JS `preventDefault`. `form[action]` is unexercised and the tool cannot see their real submit target.
- **F7 — invisible URL sources, state them in the tool contract.** `lucario-ghp` fetches its core asset with `fetch('engine.py')` in
  inline JS (relative, works under a base, but invisible). `vault-index-kimi` renders its link set from a literal array of 10 absolute
  URLs inside inline JS. `ds4cc-kimi`/`ds4cc-primary` build `…/tree/main/…` hrefs from an absolute `REPO` constant. `plazir15-ghp`'s
  inline block is `application/ld+json` (metadata, not a reference). A `clean` verdict on these pages says nothing about their effective
  reference set; the frozen interface text is silent on JS, so the limit is currently unstated anywhere.

## Out-of-scope kinds the interface ignores — presence in this corpus

| kind | observed | detail |
|---|---|---|
| meta refresh | **0**/8 | `http-equiv` absent everywhere |
| CSS `url()` in `style=""` | **0**/8 | — |
| CSS `url()` in `<style>` | **10** | ds4cc-kimi 5 + ds4cc-primary 5, all relative `assets/fonts/*.woff2`; vault-index and lucario `<style>` blocks hold 0 |
| JS-built URLs | **4**/8 pages | lucario `fetch('engine.py')`; vault-index 10-entry URL array → anchors; ds4cc-kimi/primary `REPO` templates; plazir15 JSON-LD only |
| `data-*` carrying URL text | **2**/8 | ds4cc-kimi, ds4cc-primary `button.data-copy` (bare `https://app.ds4cc.com/mcp` and shell commands containing URLs); not references |
| other `data-*` | 6/8 | i18n keys, category ids, host names, flags, a `data-cfemail` hash — no URLs |
| lazy-load attrs | **0**/8 | no `data-src`/`data-bg`/`data-lazy` anywhere |
| edge-injected root-relative | 1/8 | ds4cc-kimi Cloudflare `/cdn-cgi/l/email-protection` and `/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js` (in scope; inside `/` only because that page sits at the origin root) |

## Not verified

- No case was run against `scripts/base_path_audit.py` (absent at `9e541a1d`); the exit/verdict column is a projection from the interface
  text by my own scanner, so it neither confirms nor refutes the tool's conformance.
- The 4 sibling-project targets behind F3 were not fetched (no live probes); their existence is inferred from repo links on the same pages
  (`github.com/VeigaPunk/plazir-15-site`, `…/xbrd-spark`), and the page paths `/horizon-halo-comma-design/`, `/xbrd-spark/highlights.html`
  are unchecked. Whether flagging them is wanted is unanswered by the matrix.
- Same-origin external bundles (`main.js`, `assets/app.js`, `./rinnegan/*.js`, `/assets/index-*.js`) were not retained, so any URLs they
  construct are unknown. The 4 404 dirs have no body, so nothing beyond status and hash was enumerable.
