# ScribeRejects — lesson refuses restated

Seat: scribe. Axes: operability, freshness. Read `corpus/lessons/round-49.md:14-17` at `1c846ed2d67b1692ea966be064f0fc04542763c6` on 2026-10-24T21:38:24-03:00. Worktree lesson matched that blob (`git status --porcelain` empty for the lesson). Refuse bullets: 2. No row added.

## Restatement

S259 reason: staged `corpus/knowledge/jekyll-url-baseurl-options.md` is refused because `https://jekyllrb.com/docs/configuration/options/` is already mined as S080, and a second row would be an E04 duplicate URL in scope.
S259 flip: supersede S080 in place so the url/baseurl aspect is on the held row, with no second row for that URL.
S321 reason: staged `corpus/knowledge/ollama-openapi-contract.md` is refused because local model-serving API contracts are kama's province (`PROVINCE.md` Adjacent; staged `source:` is `raw.githubusercontent.com/ollama/ollama/.../docs/openapi.yaml`).
S321 flip: the operator amends kake's province, or kama releases the surface.

## Freshness of those lines

- S080 still holds that URL, status `mined`, scope `docs`: `git show 1c846ed2d67b1692ea966be064f0fc04542763c6:corpus/SOURCES.md` cell `S080 | Jekyll: Configuration Options — https://jekyllrb.com/docs/configuration/options/` (`corpus/SOURCES.md:88`).
- Same commit's registry has zero `S259` and zero `S321` hits (`grep -cE 'S259|S321'` → 0).
- Staged S259 URL cell is the same URL (`/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md:16`, read-only). E04 is duplicate URL+scope with no `supersedes` (`scripts/sources-census.sh:25`, emit at `:649`).
- Adjacent still says kama owns local model-serving endpoints (`PROVINCE.md:41`). Staged source line is `https://raw.githubusercontent.com/ollama/ollama/efe43c5561047d8baf8c862730b2151249d51fd5/docs/openapi.yaml` (`ollama-openapi-contract.md:2`). The lesson's `...` abbreviation matches that path.
- Quarantine ids in the next Gate paragraph have no reason/flip pair. They were not restated and were not added as rows.

## Not done

No `corpus/SOURCES.md` row appended. Neither flip was performed. This seat wrote only this file.

Report: .ufo/waves/round-49/w1/ScribeRejects.md
