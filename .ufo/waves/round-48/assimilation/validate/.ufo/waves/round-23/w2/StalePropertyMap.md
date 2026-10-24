# Round 23 wave 2 — falsifier: property-map STALE claims (c2, c8, c10, c31, c36, c39, c47, c48)

Seat: KakeR22Recovery.StalePropertyMap-2 · Date: 2026-10-21 · Frozen revision verified: lane HEAD = `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd`; `git show <rev>:SKILL.md | diff - SKILL.md` → identical; `git show <rev>:.ufo/waves/round-23/receipts/property-map.json | diff -` → identical. All checks below ran against the frozen content. Scratch: `/tmp/kake-r23w2-StalePropertyMap-nXnt`. Read-only throughout; no tool installs needed.

## Verdict

Counterexample found — one defective correction.

- All eight STALE verdicts are correct: every re-run live check reproduces the receipt (4+ filesystem paths absent; plazir27.kimi.page byte-identical generic 404).
- **c10's correction is materially wrong as maintenance guidance (P1):** it concludes "the listed source path is historical unless restored", but a live, content-matching local source for the same surface exists at `/home/vgpnk/Projects/burnerchrome` (repo `VeigaPunk/burnerchrome`, last commit 2026-08-21, working tree dated 2026-10-03 — i.e. present *before* the round-23 checks). Its `index.html` holds the exact `<title>burnerchrome — Musketeer family</title>` and h1 `Four adapters. One permanent burner Chrome.` that the live `https://burnerchrome.kimi.page/` body (sha256 `44dc3491…`, byte-identical to receipt c9) serves. The source was not "gone"; it lives at a sibling path the correction never mentions.

## Findings

### P1 — c10 correction overclaims "historical unless restored" while the current source exists one directory up

- Impacted claim: `property-map:c10` (anchor `https://burnerchrome.kimi.page/` | `~/Projects/ds4cc-marketplace/burnerchrome`), correction in both the receipt JSON and SKILL.md round-23 section.
- Evidence — mapped paths really are absent (verdict STALE stands):
  `test -e /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome` → ABSENT; `test -e /home/vgpnk/Projects/ds4cc-marketplace` → ABSENT (2026-10-21).
- Evidence — a current candidate source exists and was omitted:
  - `git -C /home/vgpnk/Projects/burnerchrome remote -v` → `origin https://github.com/VeigaPunk/burnerchrome.git`; `log -1` → `ee83492 2026-08-21 12:29:57 -0300 Point the Musketeer family site at kimi.ai for the Kimi adapter.`; working-tree files dated 2026-10-03 (`.git` mtime 2026-10-20) — pre-dates the 2026-10-21 receipt checks.
  - Local `/home/vgpnk/Projects/burnerchrome/index.html`: h1 `Four adapters. One permanent burner Chrome.`, `<title>burnerchrome — Musketeer family</title>`, 0 occurrences of `sdk-seed` (raw source, no Kimi wrapper).
  - Live GET `https://burnerchrome.kimi.page/` → HTTP 200, 11976 bytes, sha256 `44dc3491fbc6cdc517c1d3821cae43c5988fd4d4f951203f15be8de36829addb` (byte-identical to receipt c9), body contains that exact h1 (grep count 1) and title; served wrapper carries `data-kimi-website-id="1a0ada92-7532-8d00-8000-00003dc97818"` (receipt c11) — consistent with repo = content source, Kimi = publisher.
  - Full-depth scan `find /home/vgpnk/Projects \( -type d (‑iname plazir-15-site ‑o lucario ‑o ds4cc-marketplace ‑o webzites ‑o burnerchrome ‑o origin-work) ‑o ‑type f ‑iname grokbots.json \) -not -path '*/.git/*'` → only hit: `/home/vgpnk/Projects/burnerchrome`.
- Why the verdict still holds: the correction's atomic assertions ("both mapped paths absent") are true, so STALE on the *listed path* is right; what is wrong is the actionable conclusion.
- Smallest fix: rewrite the correction to scope the claim to the path and name the survivor, e.g. "2026-10-21: `~/Projects/ds4cc-marketplace/burnerchrome` and its parent are absent; do **not** mark the surface source historical — a content-matching checkout exists at `~/Projects/burnerchrome` (repo `VeigaPunk/burnerchrome`, commit `ee83492`); verify it as the replacement source path before any annotation." Apply the same text in the SKILL.md round-23 bullet and the receipt JSON.

### P3 — c2 correction incomplete: omits the existing burnerchrome candidate and the unannotated active `app.ds4cc.com` row

- Impacted claim: `property-map:c2`.
- The correction's four paths are all verified absent and the sentence-2 cross-reference checks out against the map (r18 `historical record` comments sit on the ds4cc.com, charter-GHP and ds4cc-kimi-mirror rows; the r20 bracket note on the plazir15.kimi.page dead-slot row says "historical record, not an executable instruction"). True and not overclaiming as far as it goes.
- Gaps: (1) for burnerchrome it says "need a verified replacement" without noting a candidate already on disk (see P1); (2) the "active plazir front, burnerchrome, and lucario" enumeration skips `app.ds4cc.com`, whose source `ds4cc-marketplace/apps-sdk` resolves under the absent root (verified ABSENT) while its row carries no absence annotation — no receipt claim tests that path either.
- Smallest fix: extend c2's correction with the burnerchrome candidate pointer and add an apps-sdk row annotation (or a c-claim) covering `~/Projects/ds4cc-marketplace/apps-sdk`.

## Checked and held

| Claim | Re-run (2026-10-21) | Result | Verdict on STALE | Correction |
|---|---|---|---|---|
| c2 | `test -e` on plazir-15-site, ds4cc-marketplace/burnerchrome, lucario, lucario/site | all ABSENT | correct (rows unannotated in map) | true/complete for its scope; P3 gaps above |
| c8 | `test -e /home/vgpnk/Projects/webzites/fleet/grokbots.json`; whole `~/Projects/webzites` tree; alt root `~/Projects/fleet/grokbots.json`; full-depth Projects file scan | all ABSENT / no `grokbots.json` anywhere under Projects | correct | true; "mark unavailable/historical or replace" apt — no current path exists to cite (map itself already annotates sibling `fleet.config.json` historical) |
| c10 | see P1 | mapped path + parent ABSENT | correct | **defective (P1)** |
| c31 | `test -e` on `~/Projects/lucario`, `…/site`, `…/src/lucario/engine.py`; home-wide scan (maxdepth 4, caches pruned) | all ABSENT; no `lucario` dir anywhere scanned | correct | true and properly hedged ("at the checked paths", "only after identifying the current checkout") |
| c36 | `test -e /home/vgpnk/Projects/lucario/site` | ABSENT | correct | true, correctly scoped ("on this host", "stale here") |
| c39 | `test -e /home/vgpnk/Projects/plazir-15-site`; Projects full-depth + home maxdepth-4 scans | ABSENT; no copy anywhere scanned | correct | true; "absent on this workstation" supported within scanned scope |
| c47 | `curl -sS -L https://plazir27.kimi.page/` | HTTP 404, final URL unchanged, body sha256 `93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966` — byte-identical to receipt and to the plazir15/charter/lucario dead-slot bodies | correct | true (generic Kimi 404 body, sha as quoted) |
| c48 | same fetch + browser-UA re-fetch | 404 stable across user agents; `<title>404</title>` at body line 6; grep `rel="canonical"`/`rel=canonical`/`<base ` → 0 hits | correct | true ("no canonical link, neither 09-18 content nor 09-28 canonical present") |

Cross-checks that held: SKILL.md round-23 bullets for all eight claims match the receipt JSON corrections verbatim (c2 tail confirmed by literal grep); lane worktree is byte-identical to the frozen integration revision for both SKILL.md and the receipt; map rows re-read from SKILL.md lines 10–40 confirm c2's sentence-2 annotation cross-reference.

## Limits

- The repo→live binding for `~/Projects/burnerchrome` is content-identity evidence (exact h1/title match, repo/surface name, family titles incl. "DS4CC marketplace"), not proof of the Kimi publish path — establishing that binding would require Kimi chat access, which is out of bounds. Strong enough to falsify "historical unless restored", not to declare the replacement verified.
- "On this workstation" scans covered `/home/vgpnk/Projects` full-depth (pruning `.git`) and `/home/vgpnk` to depth 4 with `.cache/.cargo/.rustup/.local/node_modules` pruned; deeper non-Projects nesting was not enumerated.
- Did not run `measure_c1.py`/`measure_c2.py` (kept the lane strictly read-only; direct re-verification above is the freshness evidence for this unit). No Kimi chat, MCP call, or write of any kind was performed; single scratch dir under `/tmp` only.
