# S479 — drafted SOURCES row (contract v1 schema, 11 cells)

Drafted by ScoutErrata (kake round 95, w1). Not appended: the L1 integrates it through the round gate.
Insert position: after the S478 row (`corpus/SOURCES.md` line 224 at freeze `8f638b591e739e1863f5fa22334d5e15178189ed`), which is the last row of `## Registry`.

| S479 | RFC Editor errata search for RFC 9110 HTTP Semantics — https://www.rfc-editor.org/errata_search.php?rfc=9110 | dataset | A | errata status of RFC 9110 sections 5.6/8.8/13.1 | errata search page for RFC 9110 fetched 2026-11-05T16:32:51Z by one GET answered 302 to https://errata.rfc-editor.org/search/?rfc_number=9110 and then HTTP 200, 97741 bytes, sha256 e6ddebb240b522f36acf0ccc9b6a52030a35ff77d17203dbd1fcf6d1339c0911; retained body .ufo/waves/round-95/w1/ScoutErrata/errata-9110.html; status headings Verified (6) line 108, Reported (2) line 689, Rejected (6) line 904; EID 9164 record lines 803-903 with the quoted note at line 863 | No verified or reported RFC 9110 erratum targets sections 5.6.1.2, 5.6.3, 8.8.3 or 13.1.x at fetch, and the one reported erratum naming 5.6.1 and 8.8.3 rules (EID 9164, Appendix A) says "Each is semantically equivalent ABNF, so no interoperability question arises: the collected grammar and the body define the same language throughout." | mined | 2026-11-05 | 90d | .ufo/waves/round-95/freeze.md |

## Cell check

- Cells: 11. Command: `python3` — `len(row.split('|')[1:-1]) == 11` → True; `'\\|' in row` → False. Every pipe in the row line is a column delimiter; no cell holds a literal or escaped pipe.
- kind `dataset` (census enum: spec, docs, paper, code, tool, dataset, talk, book, community, own-work); tier `A`, scoped to errata status only (the RFC Editor publishes the errata record of its own RFCs); status `mined`; opened `2026-11-05`; recheck `90d` (two of the page's 14 entries are Reported, i.e. not yet resolved, so the status can move).
- used-by: `.ufo/waves/round-95/freeze.md`. Its "Sourced-claim requirement" paragraph names this source, and the file exists at the freeze commit, so E11 is clean today. When the C2 knowledge entry and `corpus/lessons/round-95.md` land, the L1 appends both paths (comma-separated) to used-by.
- The anchor's retained-body path (`errata-9110.html` in this seat directory) has to be committed together with the row. It is not in used-by, so the census does not check it.

## Located quote (inside the teaches cell)

21 words. It is an exact substring of the raw fetched body at raw HTML line 863, inside the EID 9164 record (lines 803-903):

> Each is semantically equivalent ABNF, so no interoperability question arises: the collected grammar and the body define the same language throughout.

Check: `python3` — `q in open("errata-9110.html", encoding="utf-8").read()` → True (count 1); `q in row` → True. The quote contains no HTML entity, so the raw bytes and the rendered text agree.

Grounding of the teaches clause: the page lists 14 records under three status headings, Verified (6), Reported (2) and Rejected (6). No "Held for Document Update" heading is present. Their "Section N says:" lines name 12.5.1, 14.1.1, 8.3.2, B.1, 15.4.9, B.2 (Verified); 5.2, Appendix A (Reported); 6.5.1, 6.4.1, 8.6, 15.4, 15, 15.5.2 (Rejected). None of them is 5.6.1.2, 5.6.3, 8.8.3 or 13.1.x. EID 9164 quotes "list rules are expanded per Section 5.6.1" (raw lines 855/859) and lists `weak §8.8.3 %s"W/" — Appendix A %x57.2F` (raw line 876, entity-encoded). That makes it the one record that names rules from those sections.

## Census receipts

Scratch mirror: `git -C <lane> archive 8f638b591e739e1863f5fa22334d5e15178189ed | tar -x -C <mirror>`. The mirror's `corpus/SOURCES.md` is `cmp`-identical to the lane worktree's. The row was inserted after line 224.

- Control: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-11-05 <mirror>` → rc 0, `mirror ok` (`census-validate-control.txt`).
- With S479: same command → rc 0, `mirror ok`, no finding that names S479: no E01-E12 and no W03 for this row (`census-validate-with-s479.txt`).
- `sources-census.sh census <mirror>` with S479 → rows 216 (215 at the freeze), tier.A 191, status.mined 186 (`census-withrow.txt`).
- The two validate outputs are identical apart from the mirror path they name: the added row raises no finding; the W04 "duplicate url across scopes" lines are pre-existing lane warnings, none of them S479 (its URL is new).

VERDICT: S479-DRAFT admit-ready (scope-limited: errata status only; it supplies no RFC-text grounding for any contract clause).
