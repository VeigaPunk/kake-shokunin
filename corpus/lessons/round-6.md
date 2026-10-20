# Lesson — round 6 (2026-09-28)

Cites: LOG.md round-6 entry; `corpus/knowledge/ghp-subpath-spotcheck.md`;
evidence = live baseline audit (2 352 paths, ~16:45Z) +
`~/Projects/webzites/src/reconcile.mjs` source + per-repo git lead/lag. <!-- r18 re-census 2026-10-14: ~/Projects/webzites/src/reconcile.mjs absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
Commit `round-6`. Zero publishes, zero metered ops.

## The gap closed

README's residual gap: "GHP subpath rot beyond `index.html` is still
invisible — no spotcheck tooling exists yet." Closed with a procedure +
first baseline, not new code: a ~30-line script pattern (walk sourceDir,
GET live, sha-compare) plus a classification rule that turned out to be
the entire point.

## What the audit actually found

- **0 true rot** across 2 352 paths (ds4cc 1 874, plazir15 35, charter 443).
- **126 non-clean results, all explained by git state, not deploy rot**:
  ds4cc was 20 commits ahead of `origin/main` (120 diffs incl. live-404
  `robots.txt`/`sitemap.xml`/`404.html`/`infinizoom/main.js` — unpushed
  additions), plazir15 5 ahead (5 diffs), charter 2 behind (1 diff).
- **`reconcile` covers ONE `index.html`, not "index.html"** — source read
  proved it scores candidates (depth ≤2) and compares a single file.
  SKILL.md's "subpaths beyond index" blind spot was understated: even
  second `index.html` files (`magga/v2/index.html` etc.) are invisible.
- **`in-sync` on GHP masks real byte drift** — title+marker parity is a
  kimi affordance misapplied to a verbatim-bytes surface. charter-ghp
  logged `in-sync` while index differed 8.6 KB vs 50.9 KB (source lag).
  Keeper precedent (09-21 log) already knew: resolve with `git pull`,
  re-reconcile to `match`.
- **GHP serves dir indexes** (`/dir` 301→`/dir/`→index.html) — kimi
  doesn't; the mirror pitfall is now live-verified, and `.md` files are
  servable raw so they're fair game for spotchecks.

## Learned

- **The classification table is the tool.** "live ≠ source" decomposes
  into local-ahead (resolves on push), local-behind (`git pull`), and
  true rot — the only actionable class. Comparing against `origin/main`
  instead of the working tree collapses ~95% of raw diffs into noise.
- **`expect` tripwires can't watch what isn't the row URL.** probe covers
  one URL, reconcile covers one file; subpaths have no tripwire slot at
  all. Spotcheck is the only coverage for the other ~1 900 paths.
- **A baseline of zero findings is still the payload** — it establishes
  that the current fleet has no subpath rot and defines the diff
  signature for when it appears (live ≠ origin/main, not live ≠ HEAD).

## Gate

**Retrospective round-21 reconstruction, not the original round-6 admission.** Round 6 carried no Gate section (the round-6 `LOG.md` entry records none). This section was written 2026-10-20 by round-21 lane Lesson12 from the lesson text above and existing corpus records only. No live domain state was re-read; nothing here upgrades an observation to a live result.

Sources: original sections "The gap closed" (lines 8-14), "What the audit actually found" (lines 16-34), and "Learned" (lines 36-47); `LOG.md` round-6 entry (line 8); `corpus/knowledge/ghp-subpath-spotcheck.md` (round-6 evidence line 7). Round-21 reference: `corpus/lessons/round-21.md` is not present at write time, so the round-21 contract is cited by its wave artifact `.ufo/waves/round-21/wave1-spec.json` (Lesson12 item; `context` `# Contract`). Metadata contract: S019 (`corpus/CORPUS.md`, pending L1 registration; file absent at write time). S019 is metadata authority, not platform authority.

Candidates and historically supported outcomes:

| # | Candidate (original section) | Outcome | Basis |
|---|---|---|---|
| C1 | Gap closed by procedure plus first baseline, not new code (The gap closed) | Admitted with qualification | `LOG.md` round-6 entry records the same closure. Only a "~30-line script pattern" is described; no script artifact is cited. |
| C2 | 0 true rot across 2 352 paths: ds4cc 1 874, plazir15 35, charter 443 (What the audit found) | Admitted with qualification | Same counts in `LOG.md` round-6 entry; per-repo figures sum to 2 352. Single snapshot ~16:45Z 2026-09-28; webzites revision not recorded. |
| C3 | 126 non-clean results explained by git state: ds4cc 120 diffs (20 ahead), plazir15 5 (5 ahead), charter 1 (2 behind) | Admitted with qualification | Per-repo figures sum to 126; same breakdown in `LOG.md` round-6 entry. The "git state, not deploy rot" reading rests on that round's git reads, not re-read here. |
| C4 | `reconcile` covers one scored `index.html` (depth <=2), not all `index.html` files | Admitted with qualification (source-based) | Based on the round-6 read of `~/Projects/webzites/src/reconcile.mjs`. Source absent since the 2026-10-12 prune (r18 re-census 2026-10-14, line 5), so it cannot be re-read now. |
| C5 | `in-sync` on GHP masks byte drift (charter index 8.6 KB vs live 50.9 KB) | Admitted with qualification | Figures recorded in `LOG.md` round-6 entry. Later `LOG.md` round-13 entry records the charter gap as pull/deploy lag (human pushed `b74190e` and four others 2026-09-28 18:32-20:43Z); this is consistent with the lag reading, not a separate verification of the round-6 cause. |
| C6 | GHP serves directory indexes (`/dir` 301 to `/dir/` to index.html); `.md` served raw | Unverified (frontier) | Lesson says "live-verified" at round 6. `corpus/lessons/round-20.md` gate (lines 191-193) explicitly did not admit `round-6.md:33-34` and treats it as frontier pending a live read or further source. Kimi-mirror dir-index behavior in `LOG.md` round-8 and round-13 entries is a different surface and does not verify the GHP claim. |
| C7 | Classification table (local-ahead / local-behind / true rot) against `origin/main`, not the working tree (Learned) | Method admitted; "~95%" figure unverified | The method underlies the C2/C3 counts. The "collapses ~95% of raw diffs into noise" figure has no recorded denominator in the lesson or `LOG.md`. |
| C8 | `expect` tripwires cover only the row URL; subpaths have no tripwire slot (Learned) | Admitted with qualification | Structural claim consistent with the probe and reconcile scope the lesson describes. "The other ~1 900 paths" does not reconcile to 2 352 minus the row-level targets (about 2 349); the denominator is unverified. |
| C9 | A zero-finding baseline defines the diff signature: live vs `origin/main`, not live vs HEAD (Learned) | Admitted | Method statement, consistent with `LOG.md` round-6 entry. Later `corpus/lessons/round-7.md` lines 23-25 cite the round-6 origin/main walk as covering the deleted-file direction, modulo push-to-deploy lag. |
| C10 | Commit `round-6`; zero publishes, zero metered ops (header) | Unverified (historical record only) | Same claim is recorded in `LOG.md` round-6 entry. No commit or operation log was re-read for this reconstruction. |

Rejected candidates: not recorded. Neither the round-6 lesson, the round-6 `LOG.md` entry, nor `ghp-subpath-spotcheck.md` documents a rejected candidate; none is invented here.

Outside spot-check: not recorded. No independent non-author verifier (reviewer, critic, connector, or labrat replication) is named for round 6 in the round-6 `LOG.md` entry or the lesson. Later independent replications in `LOG.md` rounds 13-14 cover later probe rows, not the round-6 2 352-path baseline, and are not counted here.

Limits: all round-6 figures are historical snapshots (2026-09-28); none is a current domain claim. The lesson's provenance header carries only `Cites:` and `Commit` lines, without `verified-at:` or `recheck:`; that prefix is outside this section and was left unedited.
