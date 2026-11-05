VERDICT: S477 and S478 appended after S476 (registry 213 -> 215); mirror gate exit 0; lane census `validate --root ... kake` exits 1 with exactly two E11 findings, both "missing used-by corpus/knowledge/http-list-and-method-grammar.md" (the scribe's file, not yet written). Exit 0 at the lane root is pending that file.

# ExecSourceRows — round 94, wave 1

Seat: executor ExecSourceRows. Scope: append exactly two rows to `corpus/SOURCES.md` Registry. Nothing else in that file was touched (`git -C kake-shokunin diff --numstat -- corpus/SOURCES.md` → `2 0`). No commit, stage or other mutating git/jj command was run. No tool was installed or upgraded (no tooling change to record). No labrat was dispatched.

## Source facts (RFC 9110, one GET plus the scout's receipt)

- The scout file `.ufo/waves/round-94/w1/ScoutRFC/quotes.json` was absent at my first check. I did the single fallback GET `https://www.rfc-editor.org/rfc/rfc9110.txt` myself. My command did not capture the HTTP status code; the observed result was `502941` bytes, sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, identical to the scout receipt and to S471's recorded digest. My UTC access time was not captured by the command (file mtime 2026-11-05 12:04 host-local). Body retained: `.ufo/waves/round-94/w1/ExecSourceRows/receipts/rfc9110.txt.retained`, digest in `receipts/rfc9110.sha256`.
- `quotes.json` then appeared (ScoutRFC). Its receipt: url `https://www.rfc-editor.org/rfc/rfc9110.txt`, accessed `2026-11-05T15:00:17Z`, HTTP 200, 502941 bytes, sha256 as above, `exact_substring: true` for both. Copy: `receipts/scout-quotes.json.copy`.
- I re-verified both quotes against the retained body (`receipts/verify.txt`, command: a Python whitespace-normalised substring test). Results: S477 True, S478 True. Line verification: S477 quote at plain-text lines 3748-3749, uppercase-convention sentence at 3750-3751, heading `9.1. Overview` line 3728. S478 subsection heading `5.6.1.2. Recipient Requirements` line 1693; "Empty elements do not contribute…" at lines 1695-1696; MUST-accept sentence and grammar at lines 1699-1702.

## Gate and append sequence

1. Baseline (pre-append, read-only): `validate --file corpus/SOURCES.md` exit 0 (only W04 warnings); `validate --root /home/vgpnk/Projects/shokunin kake` exit 0. Receipts: `receipts/baseline-validate.txt`, `receipts/baseline.txt`.
2. Collision guard before append: `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` on the lane SOURCES.md, filtered for S47[78]: no hits (grep exit 1). Row count `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` = 213 (receipts/baseline.txt line 68).
3. Mirror build and gate (scratch): full corpus copy, read-only symlinks to the other lane entries (a full 497 MB copy was rejected for the 50 MB scratch rule), two rows added, scratch-only placeholder `corpus/knowledge/http-list-and-method-grammar.md` (absent in lane). `validate --file <mirror>/corpus/SOURCES.md` → exit 0. Receipt: `mirror-validate.txt`.
4. Append to the lane after the gate: rows at lane lines 223-224. Lane and final-mirror rows are byte-identical (`receipts/lane-row-identity.txt`, `append-receipts.txt`).
5. Post-append census: `validate --root /home/vgpnk/Projects/shokunin kake` → exit 1 (`census-after.txt`). The only E-findings are:
   - `kake E11 S477 missing used-by corpus/knowledge/http-list-and-method-grammar.md`
   - `kake E11 S478 missing used-by corpus/knowledge/http-list-and-method-grammar.md`
   All other findings are W04 warnings. `corpus/lessons/round-94.md` (the other used-by target) exists. This is the case the seat spec names: the scribe's knowledge file does not exist yet. I did not create it. Required next step: after ScribeEntry lands the file, re-run `validate --root /home/vgpnk/Projects/shokunin kake` and expect exit 0.

## Counts and checks

- Registry rows: before 213, after 215 (`append-receipts.txt`; the 213 is receipts/baseline.txt line 68). The expected 213 -> 215 holds.
- Collision guard after append: S477 once, S478 once.
- Pipe check: each new row has NF=13 under `awk -F'|'` (11 cells).
- Non-empty cells: all 11 cells are non-empty in both rows; no escaped or literal pipe inside any cell.
- W04 duplicate-URL warnings: pre-append `--file` run has 37 W04. Final mirror run has 39 W04, the two extra being S477 and S478, which reuse `www.rfc-editor.org/rfc/rfc9110.txt` at a different scope (the same pattern as S453-S455, S465-S466, S471-S475). Warnings are non-blocking per the validator header.

## Row content (exact text: `rows.md`)

- S477: source `RFC 9110 HTTP Semantics, section 9.1 Overview of Methods — https://www.rfc-editor.org/rfc/rfc9110.txt`; kind `spec`; tier `A`; scope `method token case-sensitivity`; anchor `section 9.1, plain-text lines 3748-3751 (heading line 3728), RFC 9110 June 2022 revision of the fetched body (sha256 21c1cdce6ab0)`; status `mined`; opened `2026-11-05`; recheck `180d`; used-by `corpus/knowledge/http-list-and-method-grammar.md, corpus/lessons/round-94.md`.
- S478: source `RFC 9110 HTTP Semantics, section 5.6.1 List Syntax — https://www.rfc-editor.org/rfc/rfc9110.txt`; kind `spec`; tier `A`; scope `list member syntax and whitespace around list members`; anchor `section 5.6.1 List Syntax, subsection 5.6.1.2 Recipient Requirements (heading line 1693), plain-text lines 1695-1702, RFC 9110 June 2022 revision of the fetched body (sha256 21c1cdce6ab0)`; status `mined`; opened `2026-11-05`; recheck `180d`; used-by as S477.
- Teaches (S477, 22 words): "Method tokens are case-sensitive, so get and GET name different methods; standardized methods are all-uppercase by convention, so write them that way."
- Teaches (S478, 25 words): "A recipient MUST accept lists with empty elements and OWS around each comma, and empty elements do not count toward the number of elements present."

## Defects found in this seat (and their handling)

1. **S478 anchor did not cover its teaching (fixed before the final gate).** The first version cited plain-text lines 1699-1702 only. The clause "empty elements do not count…" is at lines 1695-1696, which the teaching cell cites. I corrected the anchor to 1695-1702 in the mirror and then in the lane (one line, rows 224), and re-ran the gate and census. Superseded receipts are kept: `mirror-validate-superseded-anchor-1699-1702.txt` (exit 0 at the old anchor) and `census-after-superseded-anchor-1699-1702.txt` (same two E11 findings). Both are for the record; the final files are `mirror-validate.txt` and `census-after.txt`.
2. **My first mirror was wrong, not the rows.** A corpus-only mirror gave exit 1 with five spurious E11 findings (SCORECARD.md, `.ufo/waves/round-73/contract.md`, `scripts/source_recheck.py`, `.ufo/waves/round-41/...`, `.ufo/waves/round-73/contract.md`) because `--file` resolves `used-by` against the registry's parent tree, and I had not copied those paths. The lane's own `--file` baseline was exit 0. I rebuilt the mirror with symlinks to the other lane entries; the gate then passed. Tool observation for the L1: `--file` has no root option, so a copy of only `corpus/` produces false E11 findings. This is a tool-usage trap, not a registry defect.
3. **Title/heading mismatches in the spec text (kept as specified; flagged).** The spec title for S477 is "section 9.1 Overview of Methods"; the RFC heading is `9.1. Overview`. The spec section for S478 is "5.6.1 List Syntax"; the RFC heading is `5.6.1. Lists (#rule ABNF Extension)`, and the quoted sentence sits in subsection 5.6.1.2. I used the spec's wording in the source cell and named both headings in the anchor. The L1 may want the source title to match the heading verbatim.

## Limits

- The E11 pending state (above) means the census is not yet exit 0 at the lane root; this seat did not hide it.
- I did not verify the `teaches` wording against the claims that cite these rows (the knowledge entry and the lesson are other seats' work). The rows ground only the quoted grammar and method-token facts.
- One fetch was the scout's; my own fallback GET's HTTP status and UTC time were not captured by the command. The byte count and sha256 are the same as the scout's receipt.
- Scratch `/fast/scratch/hyaku/kake-r94/ExecSourceRows/` was deleted after the receipts were copied to `.ufo/waves/round-94/w1/ExecSourceRows/` (the mirror was symlink-based, so the lane itself was not touched by the delete).

## Receipts (report-relative to the lane root)

- `.ufo/waves/round-94/w1/ExecSourceRows/rows.md` — exact two rows
- `.ufo/waves/round-94/w1/ExecSourceRows/mirror-validate.txt` — final gate, exit 0
- `.ufo/waves/round-94/w1/ExecSourceRows/mirror-validate-superseded-anchor-1699-1702.txt` — superseded gate
- `.ufo/waves/round-94/w1/ExecSourceRows/census-after.txt` — final post-append census, exit 1 (E11 pending scribe file)
- `.ufo/waves/round-94/w1/ExecSourceRows/census-after-superseded-anchor-1699-1702.txt` — superseded census
- `.ufo/waves/round-94/w1/ExecSourceRows/baseline-validate.txt` — pre-append lane validation, exit 0 both forms
- `.ufo/waves/round-94/w1/ExecSourceRows/append-receipts.txt` — counts, guard, identity, numstat, NF
- `.ufo/waves/round-94/w1/ExecSourceRows/receipts/` — verify.txt, anchor-check.txt, baseline.txt, baseline-validate.txt, rfc9110.txt.retained, rfc9110.sha256, scout-quotes.json.copy, lane-row-identity.txt, lane-rows-223-224.txt, mirror-SOURCES-final.md
