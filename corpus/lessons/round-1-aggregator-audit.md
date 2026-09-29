# Round-1 aggregator corpus audit — kake

Auditor: aggregator L1 (m_qwen) + one independent L2 `reviewer` lane
(m_composer), 2026-09-28. Method: re-parsed `~/Projects/webzites/fleet/
fleet.config.json` and re-greped the cited sources. **No network probe, deploy,
or publish was performed** — the domain's operator-gated publish boundary was
respected by the audit itself. Scope: `corpus/` only.

Round evidence: `LOG.md` round-1 entry; commit `cd5b381`; lane report
`~/Projects/shokunin/.ufo/reports/round-1/web-properties-publishing.md`
(r17: this cite originally pointed at the lowercase `~/projects` twin, which
vanished between r16 ~2026-09-29T02:4xZ and r17 03:20Z — W6 of the
`~/Projects` prune regime; the canonical report sits at the uppercase path;
filename violates `PROTOCOL.md`'s `.ufo/reports/round-<N>/<lane>.md` — should
be `kake.md`; filed to the integrator).

## Verdict: NOT conformant — well-sourced, but core fleet counts are wrong

Layout (`README.md`, `knowledge/` ×4, `lessons/round-1.md`) satisfies
`CORPUS.md`; no dangling index paths; the lesson cites round, commit and report.
`knowledge/drift-detection.md` lacks a top-level `Source:` line (paths are
inline only) — minor conformance gap. The blocking problem is numeric: the
registry size and clone count are wrong in four places at once.

## Independently re-verified

| Claim | Command | Observed |
|---|---|---|
| registry schema + vintage | `grep schema\|updatedAt fleet.config.json` | `webzites-fleet-v1`, `updatedAt: 2026-09-26` ✓ |
| marker probe is a case-sensitive substring test | `grep marker ~/Projects/webzites/src/probe.mjs` | `probe.mjs:55` `html.includes(expect.marker)` ✓ |
| ds4cc CNAME | `cat ~/Projects/ds4cc-marketplace/CNAME` | `ds4cc.com` ✓ |
| Render service | `grep name\|APP_ORIGIN render.yaml` | `ds4cc-marketplace-app`, `APP_ORIGIN=https://app.ds4cc.com` ✓ |
| frozen speedrun copy | `grep 'rel=.canonical' plazir-15-site/speedrun/index.html` | 1 hit → `https://ds4cc.com/speedrun/` ✓ |
| `ufofsdbeta` is runtime, not a site | `test ! -e ufofsdbeta/.github; test -d ufofsdbeta/dist` | no workflow; `dist/` present ✓ |
| `ufofsdbeta-kimi-review` is a snapshot | `test ! -e …/.git` | not a git repo ✓ |
| weak markers killed by r2 set | `grep '12 cross-body' fleet.dedupe-report.md` | present ✓ |
| kimi-webbridge unsupported on Linux | `grep -i 'not supported on Linux' fleet/kimi-surface-ops.md` | present ✓ |
| preview-404 body size | `fleet/probe-reports/r01-census-l1.json` | plazir27 entry `bytes: 5995` ✓ |
| publish never automated | header of `scripts/kimi-surface.mjs` | "publish is never automated — no PublishApp/…" ✓ |
| kimi rows = 14 | count `.updatePath == "kimi-websites-surface"` | **14** ✓ (numerator exact) |
| commit exists | `git -C kake-shokunin log -1 --oneline` | `cd5b381 round-1` ✓ |

## Defects filed

1. **Registry row count wrong, and repeated.** Claim "20-row registry" appears
   in `corpus/README.md`, `knowledge/fleet-registry.md`, `LOG.md`, `SKILL.md`
   and the lane report. Observed: `len(json.load(fleet.config.json)["sites"])` =
   **21**. Breakdown: `status` live 12 / pruned 3 / broken 3 / queued 3;
   `class` kimi-surface 15 / repo-driven 3 / queued 3; `owner` webzites-kimi 16
   / webzites-repo 5. The "14 of 20" kimi fraction therefore has an exact
   numerator and a wrong denominator (14 of 21; or 14 of 18 non-pruned). Fix
   direction: pick one counting rule — *rows*, *active rows*, or *kimi rows* —
   and print the command beside every number.
2. **Clone count stale.** "~40 clones under `webzites/repos/`" (README +
   lesson); `ls -1 ~/Projects/webzites/repos | wc -l` = **50** (+25%).
3. **Misleading mechanism claim.** `knowledge/fleet-registry.md` says
   `status:"pruned"` is "inert in `probe.mjs`". `probe.mjs` contains **no**
   `pruned` handling at all: every row with `url` + `expect` is probed equally.
   The sentence implies a code path that does not exist; the useful fact is the
   opposite (pruning is a registry-level label, invisible to the prober).

## Gaps for the next round

- Reconcile every doc to 21 rows (or name the missing/extra id and explain the
  historical 20).
- `app.ds4cc.com` / Render row appears in `SKILL.md`'s property map but is
  absent from the `fleet-registry.md` inventory.
- One fresh `webzites probe` snapshot as a corpus entry, when the operator
  permits network: every "stale/broken" state in `drift-detection.md` is
  2026-09-26 report-sourced, not re-probed.
- Per-row `sourceDir` map covering all 50 `repos/` clones, not just the
  registry subset.
- `probe.mjs` content-level assertions (already filed by the lane): marker-inside
  rot stays invisible.
- **Cross-domain (reported, not absorbed):** the shared burner Chrome profile +
  CDP `127.0.0.1:9222` lease is also claimed by kagi (secrets & vault ops,
  `kagi-shokunin/corpus/knowledge/cdp-bridge-1password.md`). One owner must be
  ruled on by the integrator; `PROTOCOL.md` contested-scope invariant applies.
