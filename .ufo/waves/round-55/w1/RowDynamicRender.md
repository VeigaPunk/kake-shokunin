# RowDynamicRender

Claim C1 — coverage-map calibration for one knowledge file. Drafted a single row; no file edited
(not the knowledge file, not `corpus/README.md`), no git/jj mutation, no subagent dispatch.

Provenance (read-only):
- File read in full: `corpus/knowledge/dynamic-rendering-workaround-limits.md` (51 lines).
- Map read: `corpus/README.md` lines 1–45 — header (lines 1–13) plus `## Coverage map` (line 15),
  table header `| Area | Entry | Coverage |` (line 17), rows 19–45, then `## Known gaps` (line 47).
- Lane HEAD `143e592` ("round-55: W1 spec and dispatch…"); base `fcaf4b85…` verified an ancestor
  (`git merge-base --is-ancestor` → yes). Knowledge file last touched by `af7b217` (round-48);
  `git diff` on the file and on `corpus/README.md` is empty (working tree matches HEAD).

## ROW:

```markdown
| Dynamic rendering workaround limits | `knowledge/dynamic-rendering-workaround-limits.md` (S249) | One engine's own account of dynamic rendering as a workaround, not a recommended solution: the cloaking boundary is a content condition, not a technique; error pages inherit the rendering-queue status-code rule; nothing was observed on a live crawl. |
```

Format conformance (all machine-checked, python `in` / `split` on the file and on the row text):
- Area = 4 words, noun phrase, no round tag (the file's own header carries none — see RISKS 1/6).
- Entry = backticked `knowledge/<file>` + ` (S249)` copied from the file's `source:` line 1; matches
  the convention of the existing row at README line 45 (`… (S036–S039)`).
- Coverage = 38 words (10–45 ✓); contains no `|` ✓; does not start with `TBD` ✓.
- Shared 5+-letter words with the H1 (line 6): `cloaking`, `content`, `rendering`, `technique`,
  `workaround`. Also shared with the first 1500 characters: `account`, `condition`, `crawl`,
  `dynamic`, `queue`, `recommended`, `solution`.
- Every Coverage statement is a restatement of the file's own text, with no `all`/`every`/`complete`.

## EVIDENCE:

1. Lines 15–16 (blockquote, § cited at line 13) — the workaround framing:
   "Dynamic rendering is a workaround and not a recommended solution" (10 units; raw substring of
   line 15; the sentence continues "…, because it creates additional complexities and resource
   requirements." on lines 15–16). Also present at line 3 inside the recheck `curl` command; the
   cited line is the prose blockquote.
2. Line 27 — the cloaking boundary is a content condition:
   "the cloaking boundary is a content condition, not a technique condition" (11 units; raw
   substring). The two source clauses it rests on are quoted at lines 30–31 and 33–34.
3. Lines 39–42 — error pages and the inherited status rule:
   "response may skip the rendering pass entirely." (7 units; raw substring of line 42). The
   antecedent is lines 39–41: error pages "are not treated as cloaking, but are treated as any other
   error page: they inherit the status code rule of `corpus/knowledge/js-rendering-queue.md`".
4. Lines 46–48 (`## Boundary`) — one engine's account, nothing measured:
   "crawl: no crawler was run, no owned property was fetched, and the page's" (13 units; raw
   substring of line 48; the sentence opens on line 47 with "Nothing here was observed on a live").
   Line 46 supplies "one engine's own account of a technique".

## RISKS:

1. **Section-title inconsistency inside the file (its own inaccuracy, not mine).** Header line 1
   cites `§ "Dynamic rendering is a workaround"`; body line 13 cites `§ "Dynamic rendering as a
   workaround"`. The row therefore names no section title, and no Coverage statement depends on one.
2. **No round tag in the file's header.** Header lines 1–4 are `source:` / `verified-at:` /
   `recheck:` / `ground:` only; no `(rNN)`. Round-48 provenance exists only in git (`af7b217`), so
   putting a tag in the Area cell would have been an overreach — the row omits it. Sibling rows
   carrying `(r20)`/`(r22)`/`(r28)`/`(r43)` tags are consistent with that reading (tag = stated in
   the entry, not inferred from history).
3. **What the row may not say.** It may not generalize to crawlers/engines at large: lines 49–51
   state "A different engine's rule on dynamic rendering is not held by the lane and is not implied
   by this entry." It may not call the technique recommended or a gate: line 46 says "it is not a
   recommendation and it is not a gate." It may not pin a page revision: line 1 records "no revision
   printed on the page — pinned by the quoted clauses and the access date".
4. **Coverage-map gap noticed while checking for duplicates.** The file's cross-reference
   `corpus/knowledge/js-rendering-queue.md` exists on disk (`ls corpus/knowledge/`) but has no row in
   the map: `grep -n 'js-rendering-queue' corpus/README.md` → no match. Not an inaccuracy in this
   file; a map gap for a future calibration pass.
5. **Placement, if the row is appended.** The map's last row is README line 45
   (`knowledge/field-performance-cwv.md`); the new row belongs after line 45 and before
   `## Known gaps` (line 47). I did not edit README.
6. **Freshness.** `verified-at: 2026-10-24` with `recheck: 180d` → due ≈2027-04-22; no staleness as
   of the round date 2026-10-25. The 180d recheck command on line 3 is a `curl | grep -F -c` against
   the vendor page and was **not** re-run by me (out of scope; no network check performed).
7. **Unrun checks, stated as unrun.** No README render/lint/table-format validator was run (none was
   named in the assignment); conformance was checked by the python/grep commands listed above only.

VERDICT: One conformant row drafted for `knowledge/dynamic-rendering-workaround-limits.md` (38-word traceable Coverage, S249, no section title, no round tag) with the file's own header/body section-title mismatch and the missing `js-rendering-queue.md` map row flagged; no files edited.
