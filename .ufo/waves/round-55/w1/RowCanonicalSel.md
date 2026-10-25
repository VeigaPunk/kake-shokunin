# RowCanonicalSel

Claim C1 (coverage-map calibration). Read in full: `corpus/knowledge/canonical-selection.md`
(96 lines) and `corpus/README.md:1-63` (`## Coverage map` header at :15, format row at :17,
existing rows :19-45). No file edited; no git/jj mutation; no tool installed (no pacman run).

## ROW:

```markdown
| Canonical selection vs declaration | `knowledge/canonical-selection.md` (S262) | Google's selection mechanism: a declared canonical is a hint, weighed against HTTPS, redirects and sitemap inclusion; four recognised variant classes; quotation rendering classes and the round-51 correction. |
```

Insertion point if adopted: after `corpus/README.md:45` (last existing row, "Field performance
(r28)"). Format matches :17 and the precedent at :45 (`knowledge/field-performance-cwv.md`
(S036–S039)) for a source-id suffix.

Constraint checks, measured (`python3`, `in` / `split()`):
- Coverage = 27 words (10-45); 0 `|` characters; does not start with `TBD`.
- Row parses to exactly 3 cells.
- Shares 5+-letter words with H1 (:6): `declared`, `canonical`; with the first 1500 chars:
  `selection`, `Google`, `mechanism`, `redirects`, `sitemap`.
- Area = 4 words ("Canonical selection vs declaration"), <= 8; carries no round tag because the
  file's header (:1-4) carries none — see RISKS 1.
- Entry id `S262` copied from the file's own `source:` line (:1).

## EVIDENCE:

Every passage below was verified as a raw substring of the cited line (`python3` `in`), ASCII
double quotes, all <= 25 words. Passages are slices of the knowledge file itself; the source-body
checks in RISKS are against the retained body `.ufo/waves/round-51/sources/S262.html` (the file's
own `source:` id; that body is not among the round-55 retained set S372/S373/S418).

1. `corpus/knowledge/canonical-selection.md:6` — "A declared canonical is a hint; Google selects"
   (8 words). Rests the Area noun phrase and the "a declared canonical is a hint" half of Coverage.
2. `corpus/knowledge/canonical-selection.md:17` — "The page then states what the hint is weighed
   against" (10 words), with `:21` — "served over HTTP or HTTPS, redirects, presence of the URL in
   a sitemap, and" (14 words). Rests "weighed against HTTPS, redirects and sitemap inclusion".
3. `corpus/knowledge/canonical-selection.md:37` — "The page lists the variant classes it
   recognises" (8 words), with `:91` — "of those four bullets were labelled" (6 words). Rests
   "four recognised variant classes" (the file states the count "four" itself at :91).
4. `corpus/knowledge/canonical-selection.md:81` — "## Quote classes (round-51 correction)"
   (5 words), with `:83` — "Every quotation in this entry is a **rendering**" (8 words). Rests
   "quotation rendering classes and the round-51 correction".

## RISKS:

1. **No round tag available in the header.** `:1-4` are `source:`/`verified-at:`/`recheck:`/
   `ground:` only; the only round marker is body-level ("round-51 correction" at :39, :81, :88,
   :94). The Area therefore carries none. If the planner wants one, it is `r51`, sourced from the
   body, not the header.
2. **Row omits two sections to keep one cited line per claim.** The fourth steering signal
   (":61" — "inclusion and the canonical element") and the publisher-side consequences section
   (`:54` — "## Publisher-side consequences") are in the file but not in the row; adding them
   needs two more evidence lines, which exceeds the 2-4 reference budget.
3. **Counts in the file are cross-entry, not this file's.** `:94-96` reports "15 body quotations
   across both admitted entries, 3 are raw substrings, 2 survive collapse only and 10 need markup
   removal". The row states no counts, because those figures cover two entries.
4. **Internal overreach at :83.** ":83" — "Every quotation in this entry is a **rendering**" —
   "not a byte slice of it" is contradicted by the entry's own `:15` — "indicating a canonical
   preference is a hint, not a rule." — which **is** a raw substring of the retained body
   (measured True). The exception is disclosed immediately after (`:84-86`), so the universal
   sentence is the defect, not the claim. Recomputed digest of the retained body:
   `792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b`, matching the truncated
   `79222433…` at :86.
5. **Stated rendering rule does not match the entry's renderings.** `:83` states the rule as
   "inline markup is removed and whitespace collapsed". Measured: all six body quotations
   reproduce only when markup is replaced by a **space** (tags→space + collapse), not removed —
   the outcome quote at `:26-28` renders "(or signals )" from the body's
   `(or <em>signals</em>)`, and the variant bullets at `:41-46` render " : " from
   `<b>Device variants</b>: for example". Under pure removal the outcome quote and both variant
   bullets fail to match. So the entry's rendering convention is tags→space, unstated.
6. **The round-51 label correction is incomplete.** `:88` — "Corrections landed this round, both
   to this entry's own labels" — fixed two of the four variant bullets (`:44`, `:46`). Three other
   quotations still carry "(collapsed-only quote)" and are **not** recovered by collapse alone:
   `:17` (factors), `:24` (outcome), `:30` (preference) all need markup replacement. Measured
   collapse-only result per label: `:17` False, `:24` False, `:30` False, `:44` False, `:46`
   False, `:49` True — only the mobile quote at `:49-51` is genuinely collapse-only, which sits
   awkwardly against the "2 survive collapse only" figure at `:95`.
7. **Staleness: none found as of 2026-10-25.** `verified-at: 2026-10-24` with `recheck: 180d`
   (next due ~2027-04-22). The `source:` line's section and revision were confirmed present in
   the retained body: "What is URL canonicalization" and "Last updated 2026-08-20 UTC".
   `S262` is registered in `corpus/SOURCES.md:152` (mined 2026-10-24, 180d, consuming this file).
8. **Cross-file claims the row cannot assert, checked anyway.** `:4` says the held preflight
   "explicitly disclaims" selection; confirmed at `corpus/knowledge/static-canonical-preflight.md:8`
   — "not browser crawling or search-engine" (continuing "canonical selection." on :9). The
   S021/S022 claim at `:64-66` is consistent with `corpus/SOURCES.md:29-30`. Neither belongs in
   the row.
9. **Unrun:** no README edit or table render check (out of bounds), no link/HTTP check, no
   re-fetch of the Google page, no verification of Baidu's account mentioned at `:70-71`.

VERDICT: One 3-cell coverage-map row drafted and constraint-checked (27 words, no pipe, one `|`-free Coverage cell, S262 id from the file's `source:` line); six measured defects logged against the file itself, chiefly a stated rendering rule that its own renderings do not follow and three stale "collapsed-only" labels left by the round-51 correction.
