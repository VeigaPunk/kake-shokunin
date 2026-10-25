# RowPagesBasePath

Claim C1 (coverage-map calibration), round 55, lane `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Target file: `corpus/knowledge/pages-base-path.md` (60 lines, read whole).
Format source: `corpus/README.md` header (lines 1-16) and `## Coverage map` (line 15, table lines 17-45, 27 existing rows). File not edited.

ROW:
```markdown
| Project-site base paths | `knowledge/pages-base-path.md` (S040–S043) | Publisher-side ground that a project site is published under a base path: two site kinds (S040), Liquid `relative_url`/`absolute_url` filters (S042), Vite's `base` option (S043), an offline audit over a frozen 30-case matrix; root-relative breakage is inference, no property measured. |
```

EVIDENCE:
- `knowledge/pages-base-path.md:1` — "source: S040, S041, S042, S043 (corpus/SOURCES.md)" (6 units) → the four ids in the Entry cell, written as the range `(S040–S043)` in the style of existing rows (`(S036–S039)`).
- `knowledge/pages-base-path.md:7-9` — "Coverage-map ground: project-site base paths (previously Frontier)." (7 words) and "owns publisher-side knowledge of the base path; it owns no live property" (12 words, line 8; the sentence continues onto line 9) → Area phrase, "Publisher-side ground", and "no property measured". The file's own H1 (line 6, `# Project-site base paths on GitHub Pages`) supplies the Area wording and the shared word "project".
- `knowledge/pages-base-path.md:11-12` and `:19` — "A GitHub Pages *project* site is published under a" (10 words, line 11) … "base path" (line 12; one sentence across the break) and "There are two types of GitHub Pages sites." (8 words) → "is published under a base path" and "two site kinds (S040)".
- `knowledge/pages-base-path.md:25`, `:39-40`, `:53-55` — "Root-relative references: [INFERENCE] under ordinary URL resolution `/style.css` resolves against the origin, not the base path" (16 words); "Set the correct base in vite.config.js ." (7 words) with "then set base to '/<REPO>/' ." (6 words); "the frozen 30-case matrix is `.ufo/waves/round-29/c2-matrix.json`" (6 words) with "Cannot: the audit reads local files only." (7 words) → "root-relative breakage is inference", "Vite's `base` option", "an offline audit over a frozen 30-case matrix".

Quote and cell checks actually run (python, read-only): every passage above is a raw substring of the retained file (`in` → True), each ≤ 16 whitespace tokens; the Coverage cell is 39 words, contains no `|`, does not start with `TBD`, and shares the 5+-letter words `publisher`, `ground`, `project`, `published`, `under`, `liquid`, `filters`, `absolute`, `option`, `property` with the H1 plus the first 1500 characters.

RISKS:
- **Duplicate description.** `corpus/README.md:257`, in the per-round section `## Round-29 base-path frontier step` (not `## Coverage map`), already carries a 3-cell row for the same file: Area "Project-site base paths (r29)", Entry "`knowledge/pages-base-path.md` (S040–S043) + `scripts/base_path_audit.py`", with a much longer Coverage. A new main-map row means two cells describe one file and can diverge; the main-map Entry format has no slot for the audit script, so my Coverage mentions it instead.
- **No round tag in the file's own header.** The H1 carries no `r29`/round marker (the only round evidence is the `.ufo/waves/round-29/` paths and README prose), so the Area cell stays untagged. The existing round-29 row does tag it; a reader of the main map alone cannot date this entry.
- **Inference classes the row must not assert.** Lines 26-27 and 49 mark escapes above the base path, `<base href>`, and rebuild-on-base-change as `[INFERENCE]`; line 25 likewise marks root-relative resolution as inference and says "none of S040–S043 states this". The cell therefore says "breakage is inference" rather than stating breakage as sourced fact.
- **Stated limits the 39-word cell cannot carry.** Line 21: S041 covers branch or `docs`-folder publishing and "says nothing about Actions publishing". Line 55: the audit "cannot show what a server returns, confirm the base path a deployed site is served under". Line 56: "Not established here: the base path, domain or build mode of any owned property". A reader taking the cell as complete coverage would overreach past these.
- **Freshness / consistency.** File header `verified-at: 2026-10-22`, `recheck: 90d` — inside window on round date 2026-10-25. Referenced artifacts exist and the stated count matches: `scripts/base_path_audit.py` (29 312 bytes) and `.ufo/waves/round-29/c2-matrix.json` whose `cases` list has length 30 (read-only check this round). No inaccuracy found in the file's own counts. Outside the file: `corpus/README.md:107` still lists "Jekyll/base-path tooling" under open ground while line 259 says that ground moved to held Frontier — a README inconsistency, not a defect of this file, and the row claims no Core/Frontier status.
- **Scope compliance.** Only this report file was written. No `git add/commit/stash/checkout/reset/pull/push`, no jj mutation, no pacman (host transactions paused), no tool installs needed, no subagent dispatch.

VERDICT: One coverage-map row drafted for `knowledge/pages-base-path.md` with 4 evidence anchors, 39-word traceable Coverage; duplicate round-29 row, untagged header and the file's inference/limit classes flagged as overreach risks.
