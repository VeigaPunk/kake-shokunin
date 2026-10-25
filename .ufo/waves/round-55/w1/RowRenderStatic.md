# RowRenderStatic

Claim C1 (coverage-map calibration), seat RowRenderStatic, round 55, base `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`.
Read in full: `corpus/knowledge/render-static-sites.md` (162 lines) and `corpus/README.md` header + `## Coverage map`
(lines 15–45, 26 existing rows). No file edited; no git or jj mutation; only this report written.

## ROW:

```
| Render static-site deploy semantics (r30) | `knowledge/render-static-sites.md` (S049–S052) | Render Docs reading of a static site: build details and dependency install, redirect/rewrite rule matching order, dashboard response headers, custom domains and TLS, and contrasts with the GitHub Pages entries already held; four retained pages, no owned property measured |
```

Format checks run (python, on the literal row above):
- 3 cells, `| Area | Entry | Coverage |` order; Entry cell is the backticked `knowledge/<file>` path followed by ` (S049–S052)` with the en dash U+2013 used by the existing `(S036–S039)` row (README line 45).
- Coverage = 39 words (limit 10–45); no `|`; does not start with `TBD`; no `all`/`every`/`complete`.
- Area = 5 tokens (limit 8).
- Coverage shares 16 five-plus-letter words with H1 line 10 / first 1500 chars, including `render`, `static`, `deploy`, `semantics`, `domains`.

## EVIDENCE:

- `render-static-sites.md:1` — "source: S049, S050, S051, S052" (5 words; `grep -F` = 1 hit).
  Rests on: the Entry cell's ids are copied only from this `source:` line, in its order.
- `render-static-sites.md:10` — "# Render static sites — deploy semantics" (7 words; raw substring).
  Rests on: the Area noun phrase and the shared five-letter words. The `(r30)` tag is grounded in header lines 2–3
  (`.ufo/waves/round-30/sources/`, `.ufo/waves/round-30/c2_quote_truth.py`) and in the creation commit
  `451e98f 2026-10-22 round-30: C2 Render static-site entry` (`git log` on the path, read-only).
- `render-static-sites.md:6` — "redirect and rewrite rule order, custom response headers, custom domains and TLS, and the contrast with GitHub Pages behaviour already held" (21 words; raw substring).
  Rests on: the Coverage list items. The phrase "publish directory and build" from the same header line is
  deliberately not used (see RISKS 1).
- `render-static-sites.md:5` — "the four retained Render Docs pages named above" (8 words) and
  `render-static-sites.md:15` — "it measures no owned property" (5 words); both raw substrings.
  Rests on: "four retained pages, no owned property measured". The word "reading" also appears at line 127
  ("every sentence above is a reading of four"), i.e. the entry describes itself as a reading of retained pages.

## RISKS:

1. **Header overstates the body on publish directory.** Line 6 (`coverage:`) says "publish directory and build", but
   line 25 says the retained page "names no publish-directory, root-directory or" output field, line 129 repeats the
   negative, and Round-31 corrections line 150 states "it still names no publish-directory field". Copying the header
   verbatim into a Coverage cell would assert what the body refuses to assert; the row therefore says "build details
   and dependency install" instead. The line-6 header text itself is the file's inaccuracy, not the row's.
2. **Citing set is wider than `source:`.** Round-31 corrections quote S061 three times (lines 158–160), and line 6's
   "publish directory" claim is also superseded by that section. The assignment restricts the Entry cell to ids from
   the `source:` line, so S061 does not appear in the row; a reader seeing only the row will under-count the entry's
   citing set. Fixing this is a file edit (widen `source:`), outside this seat.
3. **Counter not run.** Line 8 claims "4/4 declared ids expected at the landed commit" via
   `.ufo/waves/round-30/c2_quote_truth.py`. This seat did not execute it; that gate is reported unrun, not green.
   Likewise no fetch of any Render Docs page was attempted.
4. **Quote convention mismatch with this round's rule.** Line 5 declares curly-quoted spans as the entry's quote form,
   while round-55 retained-source work requires ASCII double quotes. The row contains no quotes, so it is unaffected,
   but re-deriving this entry under round-55 rules would need the quotes rewritten.
5. **Round tag choice is arguable.** The header has no literal `r30` token; only `round-30` paths (lines 2–3) and a
   `## Round-31 corrections` section (line 141). I used the creation round, matching the `(r28)` / `(r20)` convention
   in the existing rows; `(r31)` would be defensible if the tag is meant to mark the last amendment.
6. **Contrasts include inferences.** The `## How this differs…` section (line 68) carries several `[INFERENCE]`
   contrasts. The row says "contrasts with the GitHub Pages entries already held", which the file does hold, and it
   does not claim those contrasts are verified — but a reader could over-read "contrasts" as settled fact.
7. **Freshness is inside its window.** `verified-at` is 2026-10-22 against a round date of 2026-10-25 and a 90-day
   recheck, so no staleness flag is raised; the row makes no freshness claim either way.
8. Row placement (should it sit after the `Field performance (r28)` row, README line 45) was not decided or applied —
   this seat drafts one line only and does not edit `corpus/README.md`.

VERDICT: One coverage-map row drafted for `knowledge/render-static-sites.md` — 3 cells, 39-word Coverage, 4 verified in-file passages — with the file's own header-vs-body publish-directory conflict and its unlisted S061 citation flagged.
