# ReviewS066RowTruth — S066 row and lesson gate line verification

Rev: `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0` (clone at `/fast/scratch/hyaku/kake-r33/w2/ReviewS066RowTruth/clone`).
Row under test: `corpus/SOURCES.md:74` (S066); gate line `corpus/lessons/round-33.md:32`; consumer claim `corpus/knowledge/sitemap-orphan-audit.md:230-238`.

## Commands run (exit codes)

- `sha256sum .ufo/waves/round-33/sources/gh-actions-*.json` (exit 0): `92bd3b31…ce1c` and `f2056e8b…67e4` — both match the row's truncated digests exactly.
- `gh api 'repos/VeigaPunk/ds4cc-marketplace/actions/runs?head_sha=7fc6aa2fc12451dd451fed5a9ee7125f3a90e884'` (exit 0) at 2026-10-22T~20:16Z → `tmp/live-runs-7fc6aa2f.json`; `diff <(jq -S . retained) <(jq -S . live)` → **IDENTICAL**, every field.
- `gh api 'repos/VeigaPunk/ds4cc-marketplace/actions/workflows/apps-sdk.yml/runs?branch=main&per_page=6'` (exit 0) → `tmp/live-apps-sdk.json`; canonical diff → **IDENTICAL**, including `total_count: 988` (no new pushes since 20:06:32Z retention).
- `jq` extraction of ids/names/paths/conclusions/timestamps (exit 0) and a Python fragment check on the quoted run object (exit 0).

## Per-cell verdict

| Cell | Verdict | Evidence |
|---|---|---|
| Source cell (URL, gh api read 20:05:11Z, retention paths, sha256s) | correct | Digests match; lesson line 32 names the same two URLs, second with `per_page=6`; both fetches reproducibly identical now |
| kind `dataset` | correct (fit) | `api` is not in the kind enum (spec\|docs\|paper\|code\|tool\|dataset\|talk\|book\|community\|own-work, per round-28 census note and E05); `dataset` is the right enum member for a retained API response; the E05 refusal story in the gate line is internally consistent |
| tier `A` | correct (fit) | Scope is "GitHub's own record of which workflows ran for one pushed commit and how they concluded" — the row cites the platform's own run objects for a claim about GitHub Actions runs; matches QUALITY.md:15 platform-mechanism tier-A rule. Scope's exclusions (not ds4cc.com serving, not Render, not failure cause) are honoured by the consumer at sitemap-orphan-audit.md:232,238 |
| Anchor: `total_count 3`, run 39644779773 "Deploy marketplace to GitHub Pages" pages.yml success, started 17:32:59Z, updated 17:33:42Z; run 39644779805 "Test Apps SDK wrapper" apps-sdk.yml failure; run 39644779775 "Validate Plugin Manifests" success | correct | Retained JSON: all three ids, names, workflow paths, `status: completed`, conclusions and timestamps match verbatim; validate.yml run's `path` is `.github/workflows/validate.yml` (not named in row, no conflict) |
| Teaches: Pages deploy "completed successfully about 47 seconds after the push"; apps-sdk test failed on the same push | correct | Push (commit `7fc6aa2f`, 2026-10-21T17:32:55Z) → `updated_at` 17:33:42Z = 47s; run_started_at 17:32:59Z = 4s after push. `conclusion` field is what says success/failure; runs share head_sha `7fc6aa2f` |
| 6-run failure streak | correct | Retained + live apps-sdk list: the 6 returned main-branch runs — 39644779805 (`7fc6aa2f`), 39572438715 (`1fbdb8ed`), 39570367127 (`95dbeb69`), 39440278959 (`6e888784`), 38642441807 (`9ec6e919`), 38641094581 (`480dd05f`, 2026-10-14T21:32:49Z) — all `conclusion: failure`. sitemap-orphan-audit.md:234-236 claims exactly "the six most recent main-branch runs … all concluded failure"; verified. (The listing is the six most recent by GitHub ordering; whether run 7 back also fails is unexamined but not claimed.) |
| status `mined`, opened `2026-10-22`, recheck `90d`, used-by `corpus/knowledge/sitemap-orphan-audit.md` | correct | Lesson :36 logs the `—` → `mined` transition; the used-by file does cite S066 at :230 and :236 |
| Gate-line quote ≤25 words | correct, one nit | `"name":"Deploy marketplace to GitHub Pages" … "status":"completed","conclusion":"success"` — 7 whitespace tokens; fragments verified present in run 39644779773's JSON. Nits: (a) the compacted JSON (no space after `:`) differs cosmetically from the retained bytes (`"name": "Deploy…"`) — a documented compaction, not a misquote; (b) the parenthetical "(6 words)" undercounts by whichever convention counts `…`/`"name":` (7 tokens) — still within the ≤25 bound, so the gate is satisfied |

## Change since retention

None. Both `gh api` responses are byte-for-byte identical (canonical `jq -S` diff) to the retained files; `total_count` 3 and 988 unchanged. The row remains fresh ~14 minutes after retention; nothing contradicts the 90d recheck interval.

## Not verified / residuals

- Why the apps-sdk run failed (explicitly out of scope per the row's own scope cell).
- Whether the 7th-oldest apps-sdk run also failed — consumer claims only "six most recent", which is what `per_page=6` returned.
- The round-32-style question of whether a refusal-code check may trust this row — outside this item's scope (holds noted).

## Tooling

No installs. Used preinstalled `gh 2.102.0` and `jq`, `python3`, `diff`, `sha256sum`. All pacman transactions paused per directive; none needed.

Live JSON copies (sandbox, for reproducibility): `/fast/scratch/hyaku/kake-r33/w2/ReviewS066RowTruth/tmp/live-runs-7fc6aa2f.json`, `…/tmp/live-apps-sdk.json`.
