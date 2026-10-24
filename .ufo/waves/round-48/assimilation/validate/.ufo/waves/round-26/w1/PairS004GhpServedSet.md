# PairS004GhpServedSet: round 26 freshness recheck

**Pair:** `corpus/knowledge/ghp-served-set.md` × S004 (GitHub Docs: Using custom workflows with GitHub Pages)
**Milestone:** r26-recheck-build · **Axis:** freshness · **Judged against:** `fetched/text/S004-1.txt` (fetchIndex 1)

## Bytes judged
- Manifest and population: index 1, status 200, final URL equals requested URL, `fetchedAt` 2026-10-21T15:09:34Z, content-length 141818 (`fetched/manifest.json:97-115`, `population.json:95-118`).
- The manifest `sha256` `5c15ef2d…` equals the SHA-256 of the **decompressed** HTML (141,818 bytes). It does not hash `fetched/S004-1.raw.gz` (20,935 bytes, sha256 `d57f60c3…`). Checked this session.
- Text view `fetched/text/S004-1.txt`: 6,053 bytes, one line, sha256 `f24e4f82…`.
- The raw HTML has two `<ol>` elements, both navigation (breadcrumb and sidebar). The article body has no numbered steps. The page carries no revision date; its only date is the footer "GitHub Inc. © 2026 Terms Privacy Status Pricing".
- No 2026-10-19 S004 bytes are retained, so change between 10-19 and 10-21 cannot be shown either way. Verdicts rest on today's bytes.
- No new GET was made.

## Statements in ghp-served-set.md that cite or rely on S004

| # | file:line | Statement | Verdict | Verbatim quote (S004-1.txt) | anchorObserved | Flags and notes |
|---|---|---|---|---|---|---|
| 1 | :1 | Header `source:` lists S004 among its sources | HOLD | "The GitHub Pages artifact should be a compressed gzip archive containing a single tar file." | "Configuring the upload-pages-artifact action" (the SOURCES.md:12 anchor, present) | None for S004. The `§Archive artifact` anchor and commit 7b1f4a7 point to S001 (action.yml) and are not judged here. |
| 2 | :2 | `verified-at: 2026-10-19 (v4.0.0 commit 7b1f4a7; current action commit 5f327015)` | HOLD | "To use the action in your current workflow place this snippet under jobs. - name: Upload GitHub Pages artifact uses: actions/upload-pages-artifact@v4" | Docs pin `actions/upload-pages-artifact@v4`, consistent with the entry's v4 line | **Date superseded for S004.** The S004 bytes were re-fetched 2026-10-21, so 2026-10-19 is no longer the latest S004 check. The historical date remains true. `current action commit 5f327015` is not decidable from S004 (S001 pair). |
| 3 | :29-30 | `S004 steps 4-5 upload static files and deploy the artifact.` | HOLD (content) | "- name: Upload artifact uses: actions/upload-pages-artifact@v4 # Deployment job deploy: environment: name: github-pages" | "Linking separate build and deploy jobs" example: step 4 `Upload artifact` (upload-pages-artifact@v4) and step 5 `Deploy to GitHub Pages` (deploy-pages@v4), counted across the build and deploy jobs **[INFERENCE]** | **Anchor unlabeled, not superseded.** "Steps 4-5" resolves only through that cross-job count. The single-job example gives upload=3 and deploy=4. Prose support: "The upload-pages-artifact actions enables you to package and upload artifacts." (Configuring the upload-pages-artifact action) and "The deploy-pages action handles the necessary setup for deploying artifacts." (Deploying GitHub Pages artifacts). |
| 4 | :67 | `platform docs, and GNU tar manual are cited at their scoped sources` (S004 component only) | HOLD | "The deploy-pages action handles the necessary setup for deploying artifacts." | "Deploying GitHub Pages artifacts" | The S003 and S006 components belong to their own pairs. SOURCES.md:12 names only the upload section as the S004 anchor. The deploy half of row 3 falls within the row scope ("Artifact shape and deployment requirements") but outside that named anchor. This is a row-anchor gap for L1, not a defect in line 67. |

## Row-level check (not an entry statement)
- SOURCES.md:12 teaches: **HOLD.** "The tar file must be under 10GB in size and should not contain any symbolic or hard links." The page says "a single tar file", which the one-line teaches omits. The entry does not use that constraint, and nothing changed.
- SOURCES.md:12 `fetched 2026-10-19` is superseded by the 2026-10-21 fetch. L1 logs it in the allowed recheck cell. The row is not rewritten.
- The sibling row receipt `w1/RowS004.md` (HOLD) agrees with this row check and with row 3.

## Excluded after checking (no S004 citation or reliance)
- :3 recheck command (action.yml greps).
- :7-12 Claim (S001/S002 behaviour). The `path: .` shape appears in S004's single-job example, but the entry does not cite it.
- :14-18 r20-correction, which cites publish-channels.md.
- :20-27 and :31-36 S001, S002, S006, S008 clauses; :28 S003 clause.
- :38-54 rechecks and the local tar repro.
- :56-58 named debt; :60-62 CNAME prediction (S005 is the adjacent row).
- :71-79 r20 tail: S008 version erratum only.
- Whole-file grep: "S004" occurs only at :1 and :29.

## Verdict totals
Statements 4 · hold 4 · stale 0 · unverifiable 0. Row 2 (superseded date) and row 3 (unlabeled anchor) are flagged. Neither is STALE. No S004 content changed in the re-fetched bytes, and no prior bytes exist to show drift.

```json
{"pair":"S004xghp-served-set","statements":4,"hold":4,"stale":0,"corrections":[]}
```

## Hand-off (no corpus edits made)
- Nothing to append to `ghp-served-set.md`; `corrections` is empty.
- Optional and not counted: name the sections instead of "steps 4-5" ("Configuring the upload-pages-artifact action" for upload; "Deploying GitHub Pages artifacts" for deploy).
- Route to the S001 pair: whether `current action commit 5f327015` is still current. S004 pins `@v4` and cannot decide it.

## Checks exercised
- Hashes, gzip decompression, exact-substring counts of every quoted string in `S004-1.txt` (each found; some headings appear twice because of the table of contents), and an `<ol>` and step census of the raw HTML. Run in the eval kernel with the Python standard library only.
- `grep` over `ghp-served-set.md` for S004, platform, workflow, upload, deploy, steps, verified, and recheck.
- `glob` for other retained S004 copies: none beyond the round-26 pair.
- Not run: `measure.py`, builds, tests, linters.

## Tooling
No tools installed or updated.
