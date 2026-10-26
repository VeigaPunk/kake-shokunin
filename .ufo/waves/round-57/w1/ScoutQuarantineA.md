# ScoutQuarantineA

Rows: S142, S143, S148 (quarantine slice, class `payload-absent`). Fetched 2026-10-25 UTC, one GET per cited URL (`curl -sS -L --compressed -A kake-shokunin-round57-scout`). Bodies saved in `ScoutQuarantineA.files/`.

## ROWS:

| id | URL | HTTP | verdict | located quote + location |
|---|---|---|---|---|
| S142 | https://www.kimi.com/help/websites/websites-faq | 200 | VERIFIED (claim located; registered quote is a stale/truncated rendering, not a raw substring) | `"网站链接将始终有效，除非手动点击「取消发布」"` (22 units/chars), `<h2>` "网站链接有效期是多久？会过期吗？", first `<p>` under it. Full page sentence: `如果用户点击「发布」将网站公开部署，产生的网站链接将始终有效，除非手动点击「取消发布」将网站设为私密，或者内容不适触发举报。` |
| S143 | https://developer.chrome.com/docs/crux/methodology/tools | 200 | VERIFIED (claim located as a table row; registered quote is a flattened rendering, not a raw substring) | Page "CrUX Tools", comparison table (cols Tool / Frequency / Metrics / Dimensions / Historical Data / Origin / Page-level), last row `CrUX on BigQuery`. Raw-substring quote: `"(except LCP resource types and subparts)"` (6 units, 40 chars), in the Metrics cell. Sibling cells in the same `<tr>`: `Monthly`, `All dimensions`, `Since 2017`, `Origin`. |
| S148 | https://arxiv.org/abs/2308.06409 | 200 | ABSENT on the cited page (and on the companion PDF); exists only as commented-out LaTeX in the e-print source | No quote located on the abs page or in the published PDF. See NOTES. |

## NOTES:

Register and row provenance (observed):
- The three ids are NOT in `corpus/SOURCES.md` (grep for S142/S143/S148 returns nothing there; the only hits in `corpus/` are round-48..56 lessons naming them as quarantined). The authoritative rows are the register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` lines 83-85 (lane `kake`, round1; the same ids also appear under `kumitate`, `tabi`, `tameshi` with other sources — not mine). Hence no `anchor`/`teaches`/`used-by` cells exist in kake; the register's quote cell is the only claim on record. No `corpus/knowledge` entry cites these ids.
- Upstream numbering: round-48 staging renumbered the shokuknow scout rows by +6 (ScoutKake.md S136 kimi -> kake S142; S137 CrUX Tools -> S143; S142 arXiv tier-B -> S148). Upstream scout text: S136 "tier A for Kimi's own publishing surface (publish/unpublish durability)"; S137 "compares all access surfaces on cadence, dimensions, history depth and origin-vs-page granularity in one table"; arXiv row = tier B, "full LaTeX source retrieved and quoted".

S142 detail:
- The register quote ends `...将网站设为私密。`; the live page continues `...将网站设为私密，或者内容不适触发举报。` (a trailing clause). The 40-unit-class quote stem (up to `私密`) is present; the closing `。` is the mismatch. So the round-48 `absent` was a quote-drift/truncation defect, not fabrication: the claim (published-site link stays valid until manual 取消发布) is genuinely on the page. The same sentence also occurs in the page's embedded markdown/RSC payload (`\n## 网站链接有效期是多久？会过期吗？\n\n如果用户点击...`), so it is in the server-rendered HTML, not client-only.
- Body hash changed vs round-48 receipt (round-48 sha256 1d342beca626…, 565250 bytes; now 8823b1232bf4…, 516026 decoded bytes). The page was evidently re-served/edited; the extra clause may be a post-round-48 edit [INFERENCE — no archive checked].
- Full candidate quote (41 units) exceeds 25; use the 22-unit stem above.

S143 detail:
- The registered quote joins table cells with ` — `, which is not on the page; every cell text is present and in one `<tr>`: `CrUX on BigQuery | Monthly <sup>1</sup> | All metrics (except LCP resource types and subparts) | All dimensions | Since 2017 <sup>5</sup> | Origin`. Footnote markers (1, 5) sit inside the cells, so even the cell-joined text is not contiguous in the raw HTML. Footnote 1: "Monthly data is released on the second Tuesday after each monthly collection period."; footnote 5: "Not all metrics are available in all monthly tables".
- Round-48 `absent` was therefore a quote-form defect (flattened table), not fabrication.

S148 detail:
- Registered quotes: `ratio of total to distinct`, `The ratio of total to distinct number of data entries describes the average dimension values the metrics can be segmente`.
- Searched: abs page (HTML, 43052 bytes) — 0 hits for "distinct", "total to"; only the abstract is present. Companion `https://arxiv.org/pdf/2308.06409` (HTTP 200, `pdftotext`, ~69 KB text) — no "ratio of total to distinct"; "distinct" appears only as an adjective ("distinct lead", "distinct origins"). Companion `https://arxiv.org/e-print/2308.06409` (HTTP 200, gzip tarball) — the exact sentence is in `sections/analysis.tex` line 11, but on a line beginning with `%` (commented-out draft text, adjacent to a commented table header `ratio of total to distinct` and the draft marker `\texthl{[check this and add the more recent dataset information]}`). Saved: `S148-analysis.tex` (copy of that file). Companion fetches are extra to the one-GET rule; recorded for transparency.
- Conclusion: the quoted sentence is not content of the published paper or the cited abstract page; it survives only in commented-out source. It cannot back a claim about the paper. Verdict ABSENT for the cited URL. Keep refused; if the data fact were ever needed it would have to come from a published table, not this comment. Not fabrication in the invented-text sense (the words exist in the author's draft), but not citable.

Unrun / not done: no live check for a Wayback copy of the kimi page; the S142 clause-edit timing is unverified. No register or campaign file was edited. No tools installed.

Files: `ScoutQuarantineA.files/{S142.html,S143.html,S148.html,S148-pdf.txt,S148-analysis.tex}` (sha256 S142.html 8823b123…, S143.html 28f1c338…, S148.html 2d148a78…).

VERDICT: S142 VERIFIED (claim on page; registered quote truncated/stale at its tail), S143 VERIFIED (table row present; quote was a flattened join), S148 ABSENT (not on abs page or PDF; only in a commented-out LaTeX draft line).
