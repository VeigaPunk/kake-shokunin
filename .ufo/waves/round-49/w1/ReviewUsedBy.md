# ReviewUsedBy — S273/S274 used-by and body citations

**Seat:** reviewer. Leaf. No subagent. No other file written.
**Axes:** operability, freshness.
**Milestone:** Round 49 v1 wave: attack the frozen order proof and crawl-budget quote truth.
**Lane:** `/home/vgpnk/Projects/shokunin/kake-shokunin`.
**When:** 2026-10-25T00:38:35Z.
**HEAD:** `1c846ed2d67b1692ea966be064f0fc04542763c6`.

Asked check: used-by on S273 and S274 is exactly `corpus/knowledge/crawl-budget-consequences.md`, and that entry cites both ids below line 8.

## Verdict

Both conjuncts hold on the committed blobs and on the worktree. The worktree does not diverge from `HEAD` for these files, so a dirty tree is not moving this score.

No production edit. No `jj`. No fleet write.

## Used-by cells

`git status --porcelain -- corpus/SOURCES.md corpus/knowledge/crawl-budget-consequences.md corpus/lessons/round-49.md` printed nothing (exit 0). `git diff --exit-code -- corpus/SOURCES.md corpus/knowledge/crawl-budget-consequences.md` exit 0. `cmp` of the knowledge entry against `git show HEAD:corpus/knowledge/crawl-budget-consequences.md` exit 0.

Blobs at `HEAD`: `corpus/SOURCES.md` `a4528808626743ea6084d22915f66bbe78c6ccdf`; `corpus/knowledge/crawl-budget-consequences.md` `5255cb01331734078ff79a10f279593dd7ec78d5`.

Live registry (same cells at `HEAD`):

```
awk -F'|' '/^\|[[:space:]]*S273[[:space:]]*\|/ || /^\|[[:space:]]*S274[[:space:]]*\|/ {print NR, $2, NF, $12}' corpus/SOURCES.md
149  S273  13  corpus/knowledge/crawl-budget-consequences.md
150  S274  13  corpus/knowledge/crawl-budget-consequences.md
```

`NF=13` is the census 11-column shape (`CORPUS.md` malformed-row note). No cell contains a pipe, so the used-by field is not shifted. Split repr of field 11 is `' corpus/knowledge/crawl-budget-consequences.md '` for both rows: one leading space and one trailing space, the same table padding as every other row. After the trim `sources-census.sh` `trim_cell` applies, each cell is exactly `corpus/knowledge/crawl-budget-consequences.md`. No comma, no second path, no `—`.

Those are the only Registry rows whose used-by names that path. Status on both is `mined`. `test -e corpus/knowledge/crawl-budget-consequences.md` → exists (1243 bytes), so this cell would not be E11.

## Citations below line 8

The entry is 17 lines. Line 8 is the heading `# Robots blocking does not free crawl budget` and names neither id. Word-boundary hits (`\bS273\b` / `\bS274\b`):

| line | below line 8 | tokens |
|---|---|---|
| 1 `source: S273 — https://developers.google.com/crawling/docs/crawl-budget` | no | S273 |
| 2 `source: S274 — https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate` | no | S274 |
| 11 `…crawl capacity limit (S273).` | yes | S273 |
| 13 `…whole hostname (S274). The checked S274 quote does not itself name the status codes…` | yes | S274, S274 |

The `source:` lines are above line 8. They do not satisfy the second conjunct. The body does: S273 once on line 11, S274 twice on line 13 (`(S274)` and `The checked S274 quote`). Same four hit-lines in `git show HEAD:` of the entry.

The pre-append mirror entry is byte-identical to the live entry (1243=1243), so those line numbers are not a worktree-only reading. The mirror registry has the same trimmed used-by on its own lines 150 and 151. Those line numbers are not the live rows. This seat did not score the mirror as the registry.

## Attacks that do not falsify the check

**Padding as "not exactly".** A byte compare of the raw field against the path with no spaces fails. That is table padding, not a second path. The census trims before E11. Treating the pad as a miss would "fix" every row and harm the registry. Rejected.

**Lesson also names both ids.** `corpus/lessons/round-49.md` lines 9–10 record the Gate quotes for S273 and S274. Line 12 logs used-by as that knowledge path "and only that path." `CORPUS.md` defines used-by as repo-relative paths of knowledge entries or lessons citing the row; `mined` needs ≥1 such path. `SKILL.md:598` says used-by is routing, never the reviewed denominator. The census does not warn when a lesson names an id that is absent from the cell. Round 48 has the same shape: S137 used-by is only `corpus/knowledge/js-rendering-queue.md` while `corpus/lessons/round-48.md` names S137 (8 hits). Expanding used-by to include the lesson would falsify the logged "only that path" cell. Not a defect against this check.

**Other mentions are outside the used-by contract.** Live counts outside `corpus/knowledge/` and `corpus/lessons/`: `PROVINCE.md` S273=2 S274=2, `LOG.md` S273=2 S274=1, `SCORECARD.md` S273=1 S274=1. Those files are not knowledge entries or lessons. They do not belong in the cell.

**Header-only pass.** A checker that stops at `source:` lines 1–2 would report both ids cited and would still be wrong about "below line 8". The body lines above are what make the conjunct true.

## Axis read

- **Operability:** an operator reading the trimmed used-by cell lands on one existing file, and that file's body names both ids below line 8. Column count is 13. The path is not missing.
- **Freshness:** the cells and the citation lines are the `HEAD` blobs (`1c846ed2`), not an uncommitted overlay. `verified-at` on the entry is `2026-10-24`. This seat did not re-fetch the two URLs; quote-substring truth is not this check.

Report: .ufo/waves/round-49/w1/ReviewUsedBy.md
