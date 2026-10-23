# Round 40 — ScribeMistake

## Draft for `corpus/lessons/round-40.md` (`## Mistakes`)

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| A routed defect was not re-derived from its source: round-39 closure routed “fix D1,” which would reject a valid XML 1.0 document declaring `version="1.1"` with 1.0 features. | `corpus/lessons/round-39-verifier-spotcheck.md:173-174`; `.ufo/waves/round-40/l1-probe.py:16-17` (`v11`/`v20`); S110 §2.8 (`corpus/SOURCES.md:118`; retained `.ufo/waves/round-40/sources/xml-1.0.html:517-520`). S110 says XML 1.0 processors process a `1.x` declaration as 1.0, accepting it when it uses no non-1.0 features. | none | Add QUALITY (q): “A routed defect is re-derived from its source before a fix is built.” Check: the D1 source-rederivation check written by the D1 seat. |

The draft is one table row (three table lines including header/separator), under 25 lines.

## Round 38–39 sweep: commands and output

Read-only calls below use the exact paths passed to `read`/`grep`.

- `read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-38.md")` → Mistakes at 103–107; appended mistake at 144–148. Mistakes 1–3 map to (j)/(m)/(l); count 28→29 was corrected; Mistake 4 cites QUALITY (n), whose check is still “none yet” (`QUALITY.md:960-965`).
- `read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-38-verifier-spotcheck.md")` → routed defects at 166–185; control-consequence classification is reflected by the round-39 amendment to QUALITY (j); remaining carried items are listed there.
- `read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-39.md")` → Mistakes at 55–79 and Gate at 95–108. Two stale lesson statements remain: “5 false accepts in 15” at 102–104; “seven returned source or diffs” at 74–79.
- `read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-39-verifier-spotcheck.md")` → report defects at 160–166 and routed defects at 168–180. It corrects the false-accept denominator to 5 of 7 (145–146, 166) and the source/diff return count to six (64–70, 164–165); neither correction is reflected in the round-39 lesson.
- `read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md:960-989")` → (n) still has no check; (o), (p), and amended (j) address other round-38/39 mistakes. No existing criterion re-derives routed defects from their sources.
- `grep(pattern="^\\|.*\\|.*\\|.*\\|.*\\||false accepts|misreported|Check: none yet|Routed defects|Report defects", path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-38.md;/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-38-verifier-spotcheck.md;/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-39.md;/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-39-verifier-spotcheck.md", case=false)` → matches the round-38 Mistakes table, round-39 Mistakes and “5 false accepts in 15,” and the spot-check “Report defects” / “Routed defects” sections; see file/line results above.
- `read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md:118:raw")`; `grep(pattern="When an XML 1.0 processor encounters|1.x version number|process it as a 1.0 document", path="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-40/sources/xml-1.0.html", case=false)` → S110 row pins §2.8 and retained HTML contains the note at lines 517–520.

## Other sweep findings

- Round 38 QUALITY (n): criterion exists but has no check; control lists that include tools doing the claimed work therefore remain without an executable check.
- Round 39 lesson corrections above remain unmined into the lesson text: 5/15 should be 5/7, and seven source/diff returns should be six (two seats wrote files themselves; one was refused).

## Scope and limits

- Behavior: drafted one source-grounded D1 mistake entry; no lesson or product file edited.
- Gates: no counter, selftest, or D1 check run. The D1 check is owned by another seat and was not available in this sweep.
- Touched surface: this report only: `.ufo/waves/round-40/w1/ScribeMistake.md`.
- Out of scope: implementation, changing QUALITY/SCORECARD, and correcting historical lesson text.
- Provenance: lane source rows and lesson/spot-check files read from the lane; S110 retained HTML cited by its registry hash `f58a4b9e1e5b8bac13fb55c4e5c7c8c5e2c176aa45ee68e2f1ab2498511927ec`.
