# ScoutPriorSubpathKnowledge — round 29 wave 1 (scout, leaf)

Axes: operability, freshness. Lane HEAD `e58b66c203bed4e38f89afeaa9573d980344ab64`; `git status
--porcelain corpus/knowledge/` empty; `pages-base-path.md` absent here. Sandbox
`/fast/scratch/hyaku/kake-r29/w1/ScoutPriorSubpathKnowledge/`. No installs, no network, no lane file
changed except this report. Sources read from the committed retained bodies.

## Headline

No statement in the five named files contradicts S040–S043 on the core rule. The hazard is
vocabulary: `subpath` already means *a path inside a site* (spotcheck:15,17,91; kimi:1,5,14,20;
sitemap-orphan-audit:20), while this round's frontier uses it for the *mount point*. No entry defines
"site root"; the corpus's single use of "base path" is undefined (`sitemap-orphan-audit.md:50-51`).
An entry that does not define `site root = host + base path` will read as a duplicate of the existing
entries or be cross-linked wrongly.

## Commands (read-only; exit codes)

- `grep -rIcF` over `corpus/` (68 files) for `baseurl`, `relative_url`, `absolute_url`,
  `root-relative`, `root relative`: **0 hits each**, exit 0. `base path`: **1 hit**, exit 0.
- `grep -rIn 'baseurl' corpus/`: no match, exit 1. `grep -rIn 'base_url_invalid' corpus/ scripts/`:
  5 hits, all `canonical_audit` policy (preflight:81, round-22:96, script:99,655,830-831), exit 0.
- Per-file `grep -n` for `github.io|CNAME|custom domain|subpath|base|index.html`: exit 0 (statement
  set below). `wc -l`: 111 / 100 / 73 / 135 / 84 lines, exit 0.
- `python3 -c` read of `.ufo/waves/round-29/c2-matrix.json`: 30 cases, exit 0; D5 `//o.github.io/x/` → outside; no `///` case.

## Statements (path:line, verdict vs S040–S043)

Legend: **AGREE**; **REFINE** (copying the wording would be wrong or imprecise); **SUPERSEDED** (a later in-file correction overrides it); **N/A** (kimi-only).

| path:line | statement (tight paraphrase) | verdict |
|---|---|---|
| ghp-subpath-spotcheck.md:15-22 | probe compares only the row's `site.url`; reconcile one shallow `index.html`; blind spot "every subpath", rest of tree unobserved | AGREE; `site.url` already carries `/<repo>/`, so a root comparison cannot see a root-relative escape except via bytes |
| ghp-subpath-spotcheck.md:62-65 | unpushed `robots.txt`, `sitemap.xml`, `404.html` serve live-404 | AGREE (path-level) |
| ghp-subpath-spotcheck.md:69-73 | "`/dir` → 301 → `/dir/` → serves `dir/index.html`. `href=\"dir/\"` works." | REFINE: measured at `/plazir-15-site/snake` and `/magga`. The working link is relative; host-root-absolute `/dir/` leaves a project site. Do not generalize the leading-slash shorthand |
| ghp-subpath-spotcheck.md:74-76 | "`404.html` at root is honored as the custom 404 body" | REFINE: root = published site root = `/<repo>/`; r23 c4 proves it (`veigapunk.github.io/plazir-15-site/404.html`) |
| ghp-subpath-spotcheck.md:78-80 | missing path → real 404, `title "Page not found"` | SUPERSEDED by in-file :105 (title `Not found — Plazir-15`) |
| ghp-subpath-spotcheck.md:87-95 | "`.github/`, CNAME, workflow files — never servable"; `/CNAME` "unverified prediction" | SUPERSEDED by in-file :106: `GET https://ds4cc.com/CNAME` → 200, body `ds4cc.com`. Copying :89 asserts a live-observed falsehood about custom domains |
| ghp-subpath-spotcheck.md:101-107 | r23 c3-c7: slashless redirect, 404 bytes, title, `/CNAME` 200, kimi dir contrast | AGREE; these are the observation-backed forms to cite |
| kimi-subpath-audit.md:1,9,14-15,24-26 | kimi audit scope; bytes meaningless there; map `dir/` → `dir/index.html` | N/A; the new entry must scope itself to GitHub Pages |
| kimi-subpath-audit.md:49-55 | "GHP serves the same links fine (`/dir` → 301 → `/dir/`)" | REFINE, same as spotcheck:69: tested inside the repo subpath, not a host-root rule |
| ghp-custom-domain.md:7-11,18-24 | workflow publishing ignores a repo `CNAME`; domain is Pages config (`cname`, `build_type`); S005/S003 quotes | AGREE; supplies the carve-out the entry must keep |
| ghp-custom-domain.md:30-32 | falsifier: legacy mode → the repo `CNAME` is the mechanism | AGREE |
| ghp-custom-domain.md:34-37 | named debt: ds4cc `build_type` unknown | AGREE; forbids asserting ds4cc's publishing mode |
| ghp-served-set.md:7-10 | artifact membership ≠ live membership (`.git`/`.github`/dotfiles) | AGREE; membership and mount point are independent axes |
| ghp-served-set.md:28-32,83-87 | S003: source folder is repo root `/` or `/docs` (r26 exact quote adds "on the source branch") | REFINE: this "root" is the *source folder*, not the site root or base path |
| ghp-served-set.md:60-62 | `CNAME` not excluded; "public service at `/CNAME` remains unverified" | REFINE, see C2: where a packaged root file lands depends on the base path |
| publish-channels.md:9-13 | ds4cc uploads repo root; "`CNAME` file pins `ds4cc.com`" | SUPERSEDED by in-file :59/:61 and ghp-custom-domain:7-11 |
| publish-channels.md:14-15 | plazir uploads `.` whole, "no custom domain → `veigapunk.github.io/plazir-15-site/`" | AGREE with S040's default location; REFINE: the `/<repo>/` segment comes from the repository name, not the source folder |
| publish-channels.md:16-18 | setup script writes CNAME, prints apex A/AAAA + www CNAME | AGREE; DNS, not base path |
| publish-channels.md:58-61,70-71,84 | r20: artifact ≠ checkout, repo CNAME only under branch publishing; r23: both workflows upload project root and serve; r26: S005 "any existing CNAME file is ignored and is not required" | AGREE |

## Conflicts and refinements

- **C1 — custom domain removes the subpath.** Existing files document the domain *mechanism* only;
  none states the URL consequence S041/S043 give. Refinement: add "custom domain ⇒ base `/`" and keep
  "unless a custom domain is specified" on every `/<repo>/` sentence.
- **C2 — `/CNAME` is base-path-dependent.** served-set:60-62 and spotcheck:95/:106 measure
  `ds4cc.com/CNAME`, where the site root is the host root. [INFERENCE] With S040's project-site
  location plus S043's base rule, an artifact-root file without a custom domain would appear at
  `/<repo>/CNAME`, not `/CNAME`. The entry must name the host it was measured on.
- **C3 — three different "roots".** `root` means repository source folder (served-set:28-32,60),
  published site root (spotcheck:74), host root (crawl-scope:8-9, qualified), row URL root
  (spotcheck:15). Conflating them is the highest-risk wording failure.
- **C4 — base element.** Use S024's qualified form, "first base element with an href attribute" (a
  `base` with only `target` does not set the base), matching static-canonical-preflight.md:198-199.
  Copying "the first base in tree order wins" repeats a corrected error. The preflight's blanket
  rejection of a body `<base>` (:113-119) is local tool policy, not platform behavior.
- **C5 — empty-authority `//`.** preflight:80-88 rejects `///project/a.html` as
  `canonical_url_invalid`/`base_url_invalid`; the C2 matrix has no `///` case, so entry and tool may
  legitimately diverge there. Any `//` sentence must separate `//host/path` (network-path; D5:
  same-origin, outside `/repo/`) from `///path` (empty authority, invalid under S029/S028).
- **C6 — 404 title.** Cite spotcheck:105, not :78-80.

## Absences and adjacent bindings

- The base-path rule, `baseurl`, `relative_url`/`absolute_url` and `root-relative` are absent from
  the corpus (commands above). The entry is new ground and supersedes no claim; it should say so.
- Adjacent bindings: `crawl-scope-per-host.md:8-9` (only prior mount-point statement, plus :44-46
  host-root robots debt); `sitemap-orphan-audit.md:50-51` (undefined "base path"), :59-61 ("`/`
  resolves to `index.html`" notation hazard); `mirror-pitfalls.md:16-17` (relative `href="snake/"`
  labelled "GHP-style" — true only because relative); `fleet-registry.md:54-56`,
  `origin-repos.md:18-20`, `SKILL.md:17-18,26` (live `/<repo>/` URLs, matching S040).
- S040–S043 are not registry rows (`corpus/SOURCES.md`: 39 rows, S001–S039); DraftSourcesRowsLog owns
  them, so the citations stay unregistered until integration.

## Not verified

- No live property probed, no network; all observations are committed text. Coordinates are at
  `e58b66c` and can move with sibling writes.
- Did not run `scripts/base_path_audit.py` (absent at HEAD) or `c1_quote_truth.py`; quote admissibility is another seat's remit. Did not read `sources/receipts.json` beyond provenance.

## Evidence pointers

- Retained sources: `.ufo/waves/round-29/sources/S040.txt`–`S043.txt` (read as sandbox wraps from
  `fold -s -w 110`, exit 0). Matrix contract: `.ufo/waves/round-29/c2-matrix.json`.
- Peer overlap: `w1/ConnectorCorpusLinks.md` already proposes the S024 used-by change and the
  no-import rule; C4/C5 are the statement-level evidence for both.
