# KakeR29.DraftReadmeProvince — README coverage row and PROVINCE Frontier line

Seat: draft only; no tracked lane file was edited. Deliverables in my sandbox
(`/fast/scratch/hyaku/kake-r29/w1/DraftReadmeProvince/`): `readme-section.md`
(README section plus an optional top-Coverage-map row variant),
`province-frontier.md` (PROVINCE bullet replacement, notes, optional appended
round-29 PROVINCE section), `clone/` (lane clone with both drafts applied). The
Core rule sentence "Ground moves to Core only with source-backed entries and a
gate." is kept verbatim in the PROVINCE replacement; the Core section is not
touched.

## Draft 1 — README append-only section (verbatim)

    ## Round-29 base-path frontier step

    | Area | Entry | Coverage |
    |---|---|---|
    | Project-site base paths (r29) | `knowledge/pages-base-path.md` (S040–S043) + `scripts/base_path_audit.py` | A GitHub Pages project site is served under `https://<owner>.github.io/<repo>/`, so a root-relative reference such as `/style.css` leaves the site; the source-backed parts are the two site kinds and the project-site default location `http(s)://<owner>.github.io/<repositoryname>` (S040), the `username.github.io` repository-naming rule, project pages in a `gh-pages` branch or `docs` folder, and the local `jekyll serve --baseurl ""` override (S041), the Liquid `relative_url` and `absolute_url` filters that prepend the `baseurl` (S042), and the Vite `base` option, which defaults to `/` and must be `/<REPO>/` for a project site (S043). The gate part is an offline, manifest-driven audit of page references against a declared base path, with its 30-case frozen matrix and tool contract at `.ufo/waves/round-29/c2-matrix.json` (relative to the lane root); no live property was fetched, measured or repaired |

    This is the Jekyll/base-path build-tooling ground leaving the open list. The
    entry is grounded in four primary sources opened with one public GET each on
    2026-10-22 (HTTP 200); retained bodies, visible text and receipts are at
    `.ufo/waves/round-29/sources/` (lane root: `S040.txt` … `S043.txt`,
    `receipts.json`). The gate is offline by contract: it reads a local manifest
    and local HTML files and never contacts a property, so the round repaired
    nothing live and published nothing. Counters:
    `.ufo/waves/round-29/c1_quote_truth.py` (a quote must be an exact substring of
    the retained visible text, at most 25 words) and
    `.ufo/waves/round-29/c2_matrix_count.py` (the 30 frozen matrix cases, compared
    on exit, verdict and finding tuples).

    Still open: Jekyll and Liquid base-path handling on a real Pages build, Render
    deploy semantics, accessibility conformance, and the operator-authorized reads
    named in the Frontier above. The round-25 statement "the remaining
    field-performance, Jekyll and Render frontier is unchanged" is historical as
    of 2026-10-21 and now carries the base-path step above.

`readme-section.md` also holds a separated "Optional variant" block: one row to
insert into the top-level Coverage map table after the "Field performance (r28)"
row, mirroring round 28. That is a mid-file insertion, not a pure append, so I
did not apply it; the L1 should choose.

## Draft 2 — PROVINCE Frontier bullet replacement (verbatim)

Replacement for the bullet now at lane `PROVINCE.md:24-28`:

    - Field performance (Core Web Vitals, CrUX eligibility) — first entry
      `corpus/knowledge/field-performance-cwv.md` (round 28; knowledge only, no
      gate, no property measured); Jekyll/base-path build tooling — first entry
      `corpus/knowledge/pages-base-path.md` plus offline gate
      `scripts/base_path_audit.py` (round 29; no live property repaired);
      accessibility conformance (WCAG 2.2) and Render deploy semantics remain
      open. Ground moves to Core only with source-backed entries and a gate.

## Findings for the L1

- **Round-25 text becomes historical.** `PROVINCE.md:79` and the round-20-resume
  Frontier bullet at `corpus/README.md:105` still list "Jekyll/base-path tooling"
  as open; my README section says so explicitly. The PROVINCE bullet is the only
  PROVINCE edit I propose, so the round-25 paragraph stays a dated statement.
- **Promotion to Core is not claimed.** The item now has both a source-backed
  entry and a gate, the Core rule's condition, but stays in the Frontier because
  the round-29 gate is not independently closed; the L1 owns promotion.
- **Path convention.** `knowledge/...` is corpus-relative in `corpus/README.md`
  while `scripts/...` and `.ufo/...` are lane-root-relative (as in the "Freshness
  sweep (instrument)" row); my row follows that mixed convention.
- **Sources.** S040–S043 visible texts are at
  `.ufo/waves/round-29/sources/S04{0,1,2,3}.txt`, receipts at `receipts.json`
  (all HTTP 200, 2026-10-22T10:29:37Z); I read those retained texts and made no
  network call myself. S040's receipt records `finalUrl`
  …/what-is-github-pages while the claim names …/about-github-pages (a
  redirect); my quotes come from the retained S040.txt, so the row is unaffected,
  but the SOURCES.md anchor cell written by another seat should carry that URL.
  `province-frontier.md` also holds an optional appended round-29 PROVINCE
  section, matching the per-round appended pattern.

## Commands run (read-only, plus clone and apply in my sandbox)

| Command | Exit | Observed |
|---|---|---|
| `git clone -q <lane> <sandbox>/clone` | 0 | clone at lane HEAD `e58b66c` |
| `node scripts/corpus-contract.mjs --json` on the unmodified lane clone | 0 | ok true, code 0, 24 knowledge + 23 lessons checked, 0 findings |
| same on the clone with both drafts applied | 0 | ok true, code 0, 0 findings; `git diff --stat` = PROVINCE.md 8 lines, corpus/README.md +41 |
| python markdown table column check on the new README section | 0 | every `|` row has 3 cells |
| `git status --porcelain` and `git diff --stat` in the lane | 0 | no tracked file modified; only untracked wave files plus this report |

No git mutating command, no jj command, no write inside the lane; no tool was
installed or upgraded.

## Not verified

- `c1_quote_truth.py` and `c2_matrix_count.py` were not run: the entry
  `corpus/knowledge/pages-base-path.md` and the tool `scripts/base_path_audit.py`
  do not exist at lane HEAD `e58b66c` (both confirmed absent); my drafts name
  them as the round-29 targets. I did not check the entry's quotes against the
  retained texts, nor that the gate honours the matrix interface; those belong
  to the entry, audit and counter seats. No live property was probed.
