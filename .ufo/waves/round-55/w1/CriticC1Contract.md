# CriticC1Contract

Pre-build attack on claim C1 (calibration: README coverage map vs knowledge tree), round 55 W1.
Read: `contract.md` (full), `contract.json`, `c55_readme_index.py` (all 238 lines), `controls/base-c1-readme-index.txt`.

## Method (every run named; nothing claimed unrun)

- Read-only lane git only: `rev-parse`, `ls-tree`, `show` at `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`.
- Base control reproduced: `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision fcaf4b85…`
  → `index_mismatches=21 knowledge_files=46 unindexed=21 thin=0 dangling=0 coverage_rows=27 EXIT=1`,
  byte-for-byte the committed receipt. **Base control reproduces.**
- Committed selftest: `--selftest` → `10/10`, exit 0.
- Predicate identity: `grep -o` over contract.md, counter, contract.json (`claims.C1.predicate`) and the
  receipt label → same sentence in all four, no drift.
- Each attack/wrong-reject below was **executed**: fixture repo `mktemp -d` + `git -C "$D" init -q`,
  toplevel asserted `== $D`, commit with per-command `-c user.name=critic -c user.email=critic@local`,
  counter run `python3 -B <lane>/.ufo/waves/round-55/c55_readme_index.py --root "$D" --revision <D-HEAD> --json`.
  Fixtures carry the **real 46 base knowledge bodies** (`git show`), so results are on real text. Scratch
  dirs deleted; lane repo, lane index and jj state never written.

Mechanism facts driving every finding: `thin` compares the cell against the entry's own `H1 + body[:1500]`;
`know` filters `"/" not in path[len("corpus/knowledge/"):]`; rows are `startswith("|")` lines of the
**first** `## Coverage map` section, `[2:]`; `dangling` scans backticked tokens, 6 extensions, 4 bases;
`coverage_rows` is reported but is **not** in the predicate.

## ATTACKS:

A1 **Constant boilerplate cell.** All 46 rows identical:
`` | a | `corpus/knowledge/<f>` | source knowledge note filler text | ``. Word cover over the real 46 heads:
`source` alone covers 44 files; `source`+`knowledge` covers 46/46.
Predicted 0 → **observed EXIT=0, mismatches=0, know=46**. Selftest: **no** (`fail_thin_short` is 1 token `TBD`).
A2 **Population swap.** Delete 10 real entries, add 10 stubs `# Stub\n\nsource: none\n`, index all 46 with A1's
cell. Predicted 0 → **observed EXIT=0, know=46**. Selftest: **no** (`fail_deleted_population` deletes without
replacement, so the floor being met by growth is untested).
A3 **One mega-row (minimal do-nothing).** Entire map = `` | all | `` + 46 backticked `corpus/knowledge/*`
paths + `` | source knowledge note filler text | ``. Predicted 0 → **observed EXIT=0, coverage_rows=1**.
Selftest: **no**. Headline: the predicate is satisfiable by one row stating nothing.
A4 **Cross-reference as index.** Drop B's row; A's cell = `` source knowledge note filler text; details in `knowledge/B.md` ``.
Predicted 0 → **observed EXIT=0, coverage_rows=45**. Selftest: **no**. A file can be "named" by a mention in
another entry's cell and never receive a statement of its own.
A5 **Entry edited to fit a junk cell (false provenance).** Cell `totally unrelated gardening notes here`;
prepend those words to the entry's own body head. Predicted 0 → **observed EXIT=0**. Selftest: **no** —
`fail_thin_offtopic` holds only because that fixture never edits the entry. A receipt "cell is descriptive"
can be earned by editing the entry, so the counter cannot say which side moved.
A6 **Nested knowledge file invisible.** Add unindexed `corpus/knowledge/archive/stale.md`. Predicted 0 →
**observed EXIT=0, know=46**. Selftest: **no**. "Every knowledge file" is counted top-level only.
A7 **Dangling to an unlisted shape.** Cell adds `` `knowledge/missing.csv` `` and `` `knowledge/nodir/` ``.
Predicted 0 → **observed EXIT=0**. Selftest: **no** (`fail_dangling` uses `.md`). `EXTS` = md py mjs json sh txt.
A8 **Duplicate `## Coverage map` sections.** First = A1's passing map; second (the real one) contains
`` `knowledge/ghost-entry.md` ``. Predicted 0 → **observed EXIT=0**. Selftest: **no**. Two authorities, first wins.
A9 **One word repeated.** Cell `source source source source source`. Predicted 1 only for the 2 JSON entries →
**observed EXIT=1, thin={freshness-pins.json, freshness-sidecar.json}**; the other 44 pass. Selftest: **no**.
A10 **Non-knowledge row inflates the row count.** Add `` | X | `scripts/robots_audit.py` | robots audit script cited as a knowledge entry | ``.
Predicted 0 → **observed EXIT=0, coverage_rows=47**. Selftest: **no**.

## WRONG-REJECT:

Real improvements the frozen predicate rejects (each observed EXIT=1 on an otherwise complete 46-row map):
WR1 **Basename-only rows.** `` `accessibility-review-cards.json` `` etc. without the `knowledge/` prefix →
**46 unindexed**. `unindexed` requires the literal `knowledge/<basename>`.
WR2 **Subject mention `robots.txt`.** Honest row
`` | Robots | `corpus/knowledge/robots-txt-rules.md` | `robots.txt` refusal rules and pattern syntax, operator policy | ``
→ **dangling=1**. No `robots.txt` exists under `corpus/` or the lane root (`ls-tree | grep -i robots`), so the
entry's *subject* is counted as a dead pointer. That knowledge file is one of the 21 unindexed base files.
WR3 **Subject mention `security.txt`.** Same shape for `corpus/knowledge/security-txt-publishing.md` (also one of
the 21) → **dangling=1**.
WR4 **CJK-only entry unsatisfiable.** Entry `# ヤフージャパン クロール規則 / 出典: S418 / …` with cell
`ヤフージャパン の クロール 拒否 規則 と パターン 構文` (8 units, honest) → **thin**. `words()` is
`[a-z][a-z0-9-]{4,}` on lowercased text, so a Japanese-only head gives an empty word set and `shared` is
always empty: no cell can pass. Today's 4 CJK-bearing files still carry ASCII words, so not yet fatal — but
this is a Japanese-web-properties corpus and C2's theme is Yahoo! JAPAN.
WR5 **Coverage column not last.** `| Area | Entry | Coverage | Source |` with honest coverage in column 3 and
`S418` in column 4 → **46 thin**. Adding provenance to the map is rejected by `cov = cells[-1]`.
WR6 **Brace-set naming.** `` | pair | `knowledge/{a.md,b.md}` | source knowledge note filler text | `` →
**both unindexed, dangling=0**. `expand()` runs on the negative clause only: the same token proves the
pointers resolve while failing to index the files.

## RECOMMENDED CONTRACT/COUNTER CHANGES (before any data)

None changes the frozen sentence; each makes one of its terms countable. Land with a re-run of the base
control at `fcaf4b85…` and an updated selftest count.
1. `boilerplate` term (A1, A3, A9): a cell whose normalized text appears on >1 row, or whose only shared word
   has document frequency > 50% across `corpus/knowledge/`, is a mismatch. `shared` words must have df < 50%
   and cell text must be unique per row.
2. `deleted` term (A2): pin `BASE_REV` in the counter (not a CLI arg), require `base_know - rev_know == empty`,
   and require any added file to carry a `source:`/citation line.
3. Structural naming (A4, WR1, WR6): a file is indexed only when its path is in the **Entry column** of a row
   whose last cell describes it; run `expand()` on the naming test too; accept a bare basename when unique
   under `corpus/knowledge/`.
4. Row shape in the predicate: `coverage_rows >= knowledge_files` and at most one knowledge file per row.
   Without this A3 is a legal pass.
5. Drop `"/" not in remainder` from `know` (A6), or report `nested` and add it to `index_mismatches`.
6. Pointer scope (WR2, WR3, A7): count `dangling` only for Entry-column tokens and an explicitly marked
   pointers area — the considerthese "Frontier ground map" needs its own marker for this reason — and exempt
   protocol filenames (`robots.txt`, `security.txt`, `sitemap.xml`, `humans.txt`). Separately extend `EXTS` and
   treat a trailing-`/` token as a directory prefix; the negative clause is backed for 6 extensions only.
7. Reject duplicate `## Coverage map` sections with exit 2 (A8): one authority per surface.
8. `thin` fallback (WR4, A5): `shared = words∩ or >=2 shared CJK bigrams`, and take the shared words from the
   entry's **H1 only** — not `body[:1500]` — so header keys like `source:` cannot carry 44 rows and an entry
   edit cannot retro-fit a junk cell.
9. Locate the coverage cell by header name (`Coverage`), last cell as fallback (WR5).
10. Drop `coverage_rows` from the receipt facts if it stays out of the predicate: it reads as a coverage claim
    (A10) while carrying none.

## Clause backing audit

| Contract clause | Counter | Backed? |
|---|---|---|
| every knowledge file named by a coverage-map row | `unindexed` | **Partially** — top-level only (A6), literal `knowledge/<basename>` only (WR1, WR6), satisfied by a cross-reference (A4) |
| coverage cell descriptive (>=5 tokens, shares a 5+-letter word with H1/head) | `thin` | **As written, yes** — but a constant cell satisfies it (A1, A3), only the first naming row is tested, and the entry can be edited to fit (A5) |
| no coverage-map pointer dangles | `dangling` | **Partially** — 6 extensions, backticked, first section only (A7, A8); fires on subject mentions (WR2, WR3) |
| file count not below 46 | `FLOOR` | **Yes**, but no base-retention term, so a swap passes (A2) |
| Before: 46 files, 21 unindexed | base receipt | **Yes** — reproduced at `fcaf4b85…` |
| predicate sentence identical in contract / counter / receipts | `grep -o` | **Yes** — 4 occurrences, no drift |

On the record: C1 sits on the `SCORECARD.md` calibration sub-axis, which is not in the prompt-declared axis
list (operability + freshness). The contract says so; the operator owns that ruling. Not closable from here.

## Smallest safe correction

If only one change lands before build: items 1 and 4 (uniqueness + row shape). A3 is otherwise a legitimate
exit 0 and this round could report `met: index_mismatches == 0` with zero calibration movement.

VERDICT: C1 is gameable to exit 0 by a single constant-cell row (A3) and by a population swap (A2) — neither killed by the 10/10 selftest — and falsely rejects the round's own robots/security coverage rows plus basename, CJK, brace-set and extra-column maps; base control and predicate identity check out, but the universal clause needs row-shape, uniqueness and base-retention terms before any build edit.
