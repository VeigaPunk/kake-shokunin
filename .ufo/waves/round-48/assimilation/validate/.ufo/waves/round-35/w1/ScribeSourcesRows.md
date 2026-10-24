# ScribeSourcesRows — round 35 source rows (S078-S085 + S006 re-open)

Built: draft rows file `/fast/scratch/hyaku/kake-r35/w1/ScribeSourcesRows/rows.md` (sha256 96776bd4…122aaf, 25 lines), containing 8 table rows (S078-S085) with 11 cells each, plus the S006 append-only used-by change with the retained-text quote.

## Behavior

- Row shape copied from S067-S077 of `kake-shokunin/corpus/SOURCES.md:75-85`; contract checked in `/home/vgpnk/Projects/shokunin/CORPUS.md` section "SOURCES.md — where a shokunin learns" (11 cells, kinds, tiers, statuses, append-only rule 2).
- Proposed statuses: S078, S079, S080, S082, S083, S084, S085 `mined`, used-by `corpus/knowledge/security-txt-publishing.md`; S081 `rejected`, used-by `—`.
- Tier rationale carried in each row's `scope` cell: S078 RFC 9116 spec (A); S079 the RFC authors' own project site, page credits EdOverflow and Yakov Shafranovich, so a maintainer statement (A, scoped to its own guidance); S080 Jekyll's own configuration reference (A, expressly not the Pages-pinned build); S082 RFC 8615 Standards Track (A); S083 IANA registry (A, dataset, registry header + security.txt row only); S084/S085 live operator-published files read by one ordinary GET (A, dataset, scoped to the served bytes); S081 community (C) and rejected.
- Anchors: each names a section/heading or the whole served file, and carries fetch time, HTTP status and retained-text sha256 prefix taken from `.ufo/waves/round-35/sources/receipts.json`.

## Commands and observed output

- `grep -n "^| S06[7-9]|^| S07[0-7]" corpus/SOURCES.md` — exit 0, rows at lines 75-85.
- `wc -c -w S0*.txt` in `.ufo/waves/round-35/sources` — exit 0; S078-S085 = 5590/842/1515/979/3505/1424/14/14 words.
- python extraction over S006/S078-S085 against keywords (Contact, Expires, Canonical, include/exclude, /.well-known/, security.txt row) — exit 0.
- Quote-grounding check: 18 exact substrings searched in the retained texts; 17 hit first pass, the miss was my paraphrase of S082's example sentence, fixed to the exact text (anchors now quote `"/.well-known/example" is a well-known URI, whereas "/foo/.well-known/example" is not`).
- Shape check `python3` splitting rows on `|` — exit 0: `rows 8 bad []` (each 11 cells, anchor has `sha256` + sha prefix).
- Final `sha256sum rows.md` after the two anchor wording edits: recomputed value not captured; deliverable path + line numbers below.

## Evidence pointers

- Deliverable: `/fast/scratch/hyaku/kake-r35/w1/ScribeSourcesRows/rows.md`; table rows at lines 7-14, S006 change at lines 16-25.
- Receipts: `kake-shokunin/.ufo/waves/round-35/sources/receipts.json` — S078 4954ddcd…e50e44, S079 66722966…31fa67, S080 24054b1a…85edf4, S081 1af8954e…176b55, S082 0746e9da…e20dc3, S083 aceda87b…3f9840, S084 35cf4b7b…43af58, S085 c7a10ffa…e71813, S006 9ddf8eb2…dd3447 (all HTTP 200).
- S006 old used-by (`corpus/SOURCES.md:14`) → new used-by adds `corpus/knowledge/security-txt-publishing.md`; no other cell changes. Taught fact re-confirmed verbatim: "By default, Jekyll doesn't build files or folders that: ... Start with _ , . , or # ..." and "If you want Jekyll to process any of these files, you can use the include setting in your configuration file." (location: Configuring Jekyll in your GitHub Pages site).

## Findings for the L1

1. Status conflict: marking S078-S085 `mined` is only truthful once `corpus/knowledge/security-txt-publishing.md` exists; the contract defines mined as cited by >=1 used-by path. The draft carries a note saying they are queued until C2 lands, so if C2 slips these rows must land `queued`, not `mined`.
2. S006 + S078 + S080 are the load-bearing chain: a `.well-known/` path starts with a dot, Jekyll excludes dot paths by default (S006) and needs `include` (S080), while RFC 9116 requires the file at `/.well-known/security.txt` (S078). S080 states Jekyll 3 replaces versus Jekyll 4 extends the exclude list; neither S006 nor S080 establishes the Jekyll version GitHub Pages builds, so any instruction naming `include` must not assume one semantics without separate Pages evidence.
3. S084/GitHub (Expires 2026-11-21, Canonical equal to the URL) and S085/Google (Expires 2030-04-01, two Contact lines) are live counterexamples: presence of Expires does not mean freshness; S085 is more than a year out against S078's recommendation.
4. No conflicting receipts observations were found; S083's requested `.xhtml` URL resolved to the directory URL, recorded in the row's source cell.

## Not verified / out of scope

- Did not re-fetch any URL; rows rest on the round's retained texts and receipts only. No network requests were made; the sealed key directory `/fast/scratch/hyaku/kake-r35/sealed/` was never read, listed or stat'ed.
- Did not test Jekyll or GitHub Pages build behavior; the rows are source claims.
- No lane files were written except this report; no git/jj mutation. No tooling installed or updated.
