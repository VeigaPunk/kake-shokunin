# Round 33 — structured refusal codes for the citing-set runner; ds4cc source pin advanced to 7fc6aa2f

## Claims

Declared before implementation in `SCORECARD.md` section "Round 33 — declared
claims" (commit `bc6c4a8d435473f3c30903210be30d9d6e3ef750`, which also carries
both counters; the declaration states no clock time of its own). Base
`5777d5af79cac1ebf9144b348a9d274099e77338`.

- C1 (operability, round-32 routed items 2 and 3): the runner
  `scripts/citing_set_selftest.py` reports a structured `code` next to the
  human `reason` for setup refusals (`setup_commit_before_init`,
  `setup_commit_without_repo`, `setup_failed`), the hostile selftest gains a
  spec key `reason_code`, and P6 keys on it instead of `reason_contains`.
  Counter `.ufo/waves/round-33/c1_code_probe.py` (four runner variants; a kill
  counts only with `guard_ok`; a timeout is a recorded verdict): met 2/4 at
  base, 4/4 at `b1752a2`.
- C2 (freshness, sourced claim on S065): the corpus' ds4cc-marketplace pin
  advances from `1fbdb8ed` to upstream `7fc6aa2f`; four files retained by
  path, mode and blob id; section `## Round-33 ds4cc source pin 7fc6aa2f` in
  `corpus/knowledge/sitemap-orphan-audit.md` states the sitemap loc count and
  three canonical verdicts that the counter re-derives. Counter
  `.ufo/waves/round-33/c2_pin_count.py`: met 0/4 at base, 4/4 at `b1752a2`.

## Gate

### Source openings

| id | source | opened | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S065 | https://github.com/VeigaPunk/ds4cc-marketplace/commit/7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 (read through a sandbox clone at `/fast/scratch/hyaku/kake-r33/ds4cc-upstream`, `git clone` of the public repository, clone made 2026-10-22T19:49:58Z per wave-1 `CriticDeclarationOrder`) | 2026-10-22 | “`<link rel="canonical" href="https://ds4cc.com/magga/frostbite/">`” (magga/frostbite/index.html line 9; 3 words); “`<url><loc>https://ds4cc.com/magga/frostbite/</loc></url>`” (sitemap.xml line 15; 1 word) | admit, tier A for the files' own content at that commit, status `mined` |
| S066 | https://api.github.com/repos/VeigaPunk/ds4cc-marketplace/actions/runs?head_sha=7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 and https://api.github.com/repos/VeigaPunk/ds4cc-marketplace/actions/workflows/apps-sdk.yml/runs?branch=main&per_page=6 (`gh api`, L1, 2026-10-22T20:05:11Z and 20:06:32Z; both responses retained under `.ufo/waves/round-33/sources/`) | 2026-10-22 | “"name":"Deploy marketplace to GitHub Pages" … "status":"completed","conclusion":"success"” (run 39644779773 object; 6 words) | admit, tier A for GitHub's own run record, kind `dataset`, status `mined`; first written with kind `api`, which the census refused (`E05 S066 kind=api`), changed to `dataset` before commit |

Row changes logged old→new: S065 new (`—` → `mined`, opened `2026-10-22`,
recheck `90d`, used-by `corpus/knowledge/sitemap-orphan-audit.md`). No other
row's status, recheck or used-by cell changed. S066 new (`—` → `mined`, opened `2026-10-22`, recheck `90d`, used-by `corpus/knowledge/sitemap-orphan-audit.md`).
