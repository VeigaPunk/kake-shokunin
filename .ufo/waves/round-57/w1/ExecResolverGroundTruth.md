# ExecResolverGroundTruth

Claim C2 ground truth, built by hand over read-only git. No resolver was run, and that is also the
lane's state: `scripts/id_resolver.py` is absent from lane HEAD `f7c98ff` (`git ls-tree -r --name-only
HEAD scripts/` lists 489 files, none named `*resolver*`) and from the working tree (`ls` → ENOENT); only
this report and `.files/truth.py` were written.

SCRIPT: `.ufo/waves/round-57/w1/ExecResolverGroundTruth.files/truth.py` (python3 stdlib; only `git show|grep|log`; never imports `scripts/id_resolver.py`).
- `python3 -B truth.py history` → the 60-revision table plus repair attribution.
- `python3 -B truth.py owners [rev]` → dangling ids at `rev` (default `3994101`) plus sibling owners.
- `rows` = lines matching `^ {0,3}\|[ \t]*S[0-9]{3,} ` in `corpus/SOURCES.md`; `cited` = distinct
  word-bounded `S[0-9]{3,}` in `corpus/knowledge/*.md` via `git grep -w -o` (git's word class is
  `[A-Za-z0-9_]`, so CJK, brackets and punctuation terminate the token, and `S367a`/`XS367` do not
  count); `occ` = raw token occurrences; `dangling` = cited − rows.
- Cross-check: a second, independent implementation (per-file `git show` + Python
  `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`) reproduced rows/cited/occ/dangling exactly at
  `f8438a2`, `a4a890c`, `3994101`, `b99b667`, `f8675e5`, `f7c98ff`.

HISTORY TABLE: 60 revisions, newest first, exactly the assignment's
`git log --first-parent --format=%h -- corpus/SOURCES.md corpus/knowledge | head -60`.

| rev | date | rows | cited | occ | dangling | subject |
|---|---|---|---|---|---|---|
| f8438a2 | 2026-10-25 | 158 | 104 | 1094 | — | round-56: wave-2 repairs — entries, S419 row hedge, PROVINC… |
| d5afc48 | 2026-10-25 | 158 | 104 | 1065 | — | round-56: build — three Yahoo crawl-handling entries, S419/… |
| 64c0ce1 | 2026-10-25 | 156 | 102 | 995 | — | round-55: content revision — reviewer repairs, lesson cavea… |
| faf9abe | 2026-10-25 | 156 | 102 | 995 | — | round-55: wave-2 repairs — entries, README rows, lesson, co… |
| 2bda8e4 | 2026-10-25 | 156 | 102 | 984 | — | round-55: build — three Yahoo robots entries, S418 row, cov… |
| 8e408e0 | 2026-10-25 | 155 | 101 | 930 | — | round-54: repair S374 calibration and settle r53 ops debt |
| 7559149 | 2026-10-25 | 155 | 101 | 928 | — | round-53: clarify Baidu source locators |
| fd91527 | 2026-10-25 | 155 | 99 | 926 | — | round-53: re-ground crawl source citations |
| a4a890c | 2026-10-25 | 148 | 99 | 926 | S367,S372,S373,S390,S409 | round 52: measured receipts, drift reconciliation, scorecar… |
| 5422ff3 | 2026-10-25 | 148 | 99 | 926 | S367,S372,S373,S390,S409 | round 52: append three crawl-hygiene rows and entries; regi… |
| 907790c | 2026-10-25 | 145 | 91 | 895 | — | round-51: land the wave evidence, the ledger verdict and th… |
| 5591557 | 2026-10-24 | 145 | 91 | 893 | — | round-51: append S262 and S263 after the pre-append mirror … |
| ff3f6ec | 2026-10-24 | 143 | 89 | 875 | — | round-50: append the S286 row after the pre-append mirror a… |
| 1c846ed | 2026-10-24 | 142 | 88 | 871 | — | round-49: append crawl-budget rows after the pre-append mirror |
| af7b217 | 2026-10-24 | 140 | 86 | 866 | — | round-48: declare claims, land the client-rendering theme a… |
| 59146c9 | 2026-10-24 | 136 | 82 | 856 | — | round-47: scope inherited residual evidence |
| 846138c | 2026-10-24 | 136 | 82 | 856 | — | round-47: close r46 registry, receipt, and record defects |
| ee43e66 | 2026-10-24 | 135 | 81 | 853 | — | round-46: C1 redirect/rewrite audit + C2 citation-hygiene g… |
| dc7f03e | 2026-10-24 | 134 | 80 | 847 | — | round-45: final instruments, wave-2 corrections, measuremen… |
| 290b570 | 2026-10-24 | 134 | 80 | 847 | — | round-45: measurements, corpus (S133/S134, lesson, knowledg… |
| 297aa62 | 2026-10-23 | 132 | 78 | 837 | — | round-44: C1 witness-class gate capability (27/27 witnessed… |
| b49cba9 | 2026-10-23 | 130 | 78 | 837 | — | round-43: C1/C2 declared and frozen before any seat scores … |
| 6858665 | 2026-10-23 | 128 | 75 | 833 | — | round-42: wave-2 verdict — C1 NOT MET (kill rule 2, four wi… |
| b061585 | 2026-10-23 | 125 | 75 | 833 | — | round-42: SOURCES S117-S119 restored + S120-S125, lesson ro… |
| 0c5ad2f | 2026-10-23 | 119 | 75 | 833 | — | round-41: build revised after wave 2 — IP-literal branch ad… |
| 2653b62 | 2026-10-23 | 119 | 75 | 833 | — | round-41: build receipts, lesson, QUALITY (s)(t)(u), LOG, S… |
| 9e3c31d | 2026-10-23 | 119 | 75 | 833 | — | round-41: wave-1 control receipts; kill rule (1) fired on c… |
| d8d5578 | 2026-10-23 | 116 | 75 | 833 | — | round-40: build revised after residual attack (F1-F3 regres… |
| 6d5cd54 | 2026-10-23 | 115 | 75 | 833 | — | round-40: lesson (gate, mistakes, r39 corrections), QUALITY… |
| f043c72 | 2026-10-23 | 114 | 75 | 833 | — | round-40: C1 declared (frozen counter, witnesses, kill rule… |
| 4c080d3 | 2026-10-23 | 109 | 75 | 833 | — | round-39: wave-1 control receipts; kill rule (1) fired (six… |
| ceecb1b | 2026-10-23 | 104 | 75 | 833 | — | round-39: C1 declared (sitemap_audit capability; counter+co… |
| 729878e | 2026-10-23 | 101 | 75 | 833 | — | round-38: wave-2 reports and corrections; independent impl … |
| adab4c7 | 2026-10-23 | 101 | 75 | 833 | — | round-38: measured results, harm receipts, SOURCES S098-S10… |
| b99b667 | 2026-10-23 | 97 | 72 | 814 | S099 | round-37: wave-2 corrections; post-measurement repairs (lin… |
| 528a6d0 | 2026-10-23 | 97 | 72 | 812 | S099 | round-37: non-claim routed repairs (selftest fixtures kill … |
| 25f8487 | 2026-10-22 | 94 | 70 | 765 | S099 | round-36: wave-2 reports and corrections, real-run 2, post-… |
| e5a293b | 2026-10-22 | 94 | 70 | 765 | S099 | round-36: wave-1 reports and specs, criteria checks with re… |
| 4d5b3d5 | 2026-10-22 | 94 | 70 | 760 | S099 | round-36: C1 build — scripts/source_recheck.py (wave-1 Exec… |
| 662578e | 2026-10-22 | 87 | 70 | 760 | S099 | round-35: wave-2 corrections — reports and registry; entry,… |
| 95abec2 | 2026-10-22 | 87 | 70 | 754 | S099 | round-35: C2 build — security-txt-publishing entry (wave-1 … |
| 2ac06c5 | 2026-10-22 | 77 | 59 | 654 | — | round-34: wave-2 reports and registry, receipts at 24a1647 … |
| 76fac3b | 2026-10-22 | 77 | 59 | 649 | — | round-34: wave-2 repairs — link-preview tool (first-wins at… |
| 24a1647 | 2026-10-22 | 77 | 59 | 649 | — | round-34: wave-1 integration — selftest and fixtures, crite… |
| 9ef758c | 2026-10-22 | 77 | 58 | 644 | — | round-34: C2 build — link-preview-metadata entry, SOURCES S… |
| 3abfc44 | 2026-10-22 | 66 | 52 | 574 | — | round-33: wave-2 repairs (stray symlinks stay per-case refu… |
| e490381 | 2026-10-22 | 66 | 52 | 574 | — | round-33: runner repairs (per-run default scratch, read_exp… |
| b1752a2 | 2026-10-22 | 65 | 51 | 572 | — | round-33: C1 structured refusal codes + P6 reason_code; C2 … |
| 96d49d6 | 2026-10-22 | 64 | 50 | 568 | — | round-32: S062 source/scope cells widen to the four retaine… |
| d061f38 | 2026-10-22 | 64 | 50 | 568 | — | round-32: screened rejects S063 (Flue Blueprint restatement… |
| 4d13e68 | 2026-10-22 | 62 | 50 | 568 | — | round-32: wave-1 repairs — retain server.ts and .dockerigno… |
| 285abca | 2026-10-22 | 62 | 50 | 566 | — | round-32: S062 recheck 90d (census E09 fix), after receipts… |
| 2f2f12d | 2026-10-22 | 62 | 50 | 566 | — | round-32: C1 P6 commit-before-init spec with reason_contain… |
| 9a7f5be | 2026-10-22 | 61 | 49 | 564 | — | round-31: attempt-2 wave-2 repairs (dot-named symlinked cas… |
| fde133a | 2026-10-22 | 61 | 49 | 552 | — | round-31: C2 entry render-web-services.md, rows S057-S061, … |
| 1c7773e | 2026-10-22 | 56 | 44 | 493 | — | round-30: wave-2 repairs (runner pair ordering and guarded … |
| 451e98f | 2026-10-22 | 56 | 44 | 483 | — | round-30: C2 Render static-site entry, S049-S056 rows, less… |
| d8cd2e4 | 2026-10-22 | 48 | 40 | 403 | — | round-29: wave-2 repairs (entry, rows, SKILL, QUALITY, tool… |
| 7697990 | 2026-10-22 | 48 | 40 | 393 | — | round-29: integrate SKILL triage table, README/PROVINCE fro… |
| f8675e5 | 2026-10-22 | 48 | 40 | 393 | — | round-29: C1 base-path entry, S040-S048 rows, lesson gate, … |

DANGLING REVISIONS AND WHAT REPAIRED THEM — 9 of the 60 revisions, two episodes, nothing else.
1. `S099` — 7 consecutive revisions, rounds 35–37: `95abec2`, `662578e`, `4d5b3d5`, `e5a293b`,
   `25f8487`, `528a6d0`, `b99b667`. Repaired at `adab4c7` "round-38: measured results, harm receipts,
   SOURCES S098-S101, knowledge entry, QUALITY (j)-(n), PROVINCE/README/SKILL, lesson, LOG, wave-1
   reports" — row added (rows 97 → 101). Cause: at those seven revisions the only occurrence is `S099`
   as the upper bound of the range token `S078–S099` in the `counter:` frontmatter line of
   `corpus/knowledge/security-txt-publishing.md:8`, a range endpoint, not a document citation. The
   added row is RFC 9309 §§1–5, the *same URL* as existing row S011
   (https://www.rfc-editor.org/rfc/rfc9309.html) under a narrower scope; S099 becomes a real citation
   from round 38 on (`corpus/knowledge/robots-txt-rules.md:1,89,114` at HEAD).
2. `S367,S372,S373,S390,S409` — 2 revisions in the window, `5422ff3` (round-52 build: entries landed
   before their rows) and `a4a890c` (round-52 measured receipts); plus `3994101` itself, on the
   first-parent chain but outside the 60-revision path list because it changed only
   `corpus/lessons/round-52-verifier-spotcheck.md` (its registry/knowledge are identical to `a4a890c`:
   148 rows, 99 cited, 926 occurrences). Repaired at `fd91527` "round-53: re-ground crawl source
   citations" — all five rows added (rows 148 → 155).
Rows are monotone non-decreasing across the window (48 → 158, no deletions): every dangling id is a
citation that landed before its row, not a withdrawn row.

OWNER TABLE: dangling ids at `3994101` (`3994101dba28896830604fd0b08c7f00faca8ed6`; 148 rows, 99
cited, 926 occurrences); sibling registries read at their live HEAD. Only kotodama-shokunin
(`f7104cb`) holds any of the five ids.

| id | sibling holding the id | sibling row URL (source cell) | same document? |
|---|---|---|---|
| S367 | kotodama-shokunin | https://periodicos.ufpb.br/index.php/srh/article/view/13999/7921 | NO |
| S372 | kotodama-shokunin | https://museu.socgeografialisboa.pt/objectos/padrao-de-santo-agostinho/ | NO |
| S373 | kotodama-shokunin | https://eve.fcsh.unl.pt/en/places/rocks-ielala | NO |
| S390 | kotodama-shokunin | https://repository.up.ac.za/bitstreams/902842e3-d5eb-4688-bf3f-40b310b24959/download | NO |
| S409 | kotodama-shokunin | https://web.archive.org/web/20151110063110/http://www.metmuseum.org/exhibitions/listings/2015/kongo/blog/posts/kongo-textiles-renaissance-european-collections | NO |

- The documents these ids actually stand for are kake's own rows, added at `fd91527`: S367
  https://info-search.yahoo.co.jp/archives/002852.php, S372 …/002849.php, S373 …/002850.php, S390
  https://ziyuan.baidu.com/wiki/990, S409 https://ziyuan.baidu.com/wiki/1021. None of those six lane
  URLs appears in any sibling registry at HEAD under any id: no lane owns the document.
- The citing files name no URL *for* the dangling id: the cites sit in
  `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md:26-27` (S367, S372, S373) and
  `corpus/knowledge/baidu-friendly-crawl-guidance.md:40,50` plus
  `corpus/knowledge/baidu-mobile-matching-error-causes.md:35` (S373, S390, S409), in prose with no URL
  on the line or in the enclosing bullet; each file's only URL is its own frontmatter source row
  (`002851.php`, `college/courseinfo?id=1399`, `college/courseinfo?id=267&page=15`). "Same document" is
  therefore judged against the lane row that later supplies the id: NO for all five.

NOTES:
- The C2 contract's G4 premise is reproduced exactly (five dangling ids at `3994101`, each id-string
  held only by kotodama-shokunin), but the ownership is a namespace collision, not document identity:
  kotodama's S367 is a Brazilian history journal PDF, S372 a Museu da Sociedade de Geografia de Lisboa
  object record, S373 an EVE entry "Rocks Ielala", S390 a University of Pretoria repository PDF, S409 a
  Met exhibition blog post via Wayback — Kongo/Angola and Lisbon material, unrelated to Yahoo! JAPAN
  crawl pages or the Baidu platform. A resolver printing "owner = kotodama-shokunin" answers "who else
  uses this number", not "where does this citation come from"; what closed the gap was kake registering
  its own five rows (`fd91527`), not borrowing kotodama's.
- G5's threshold has room at HEAD `f7c98ff`: `cited` = 104 distinct ids (1094 occurrences), `dangling`
  = ∅, so `ids_cited >= 100` holds with four to spare. HEAD is 2 commits past base `28fa0b2`, and the
  registry plus knowledge tree is byte-identical between `f8438a2` and HEAD (`git diff --stat` empty).
- Row-regex sensitivity: the assignment's anchored pattern equals a loose `^\s*\|[ \t]*S\d{3,}[ \t]*\|`
  count at HEAD, `3994101`, `fd91527`, `f8675e5` (158 / 148 / 155 / 48); no duplicate ids at HEAD;
  ids run S001–S420.
- "Cited" counts `corpus/knowledge/*.md` only, per assignment: 49 of the 52 entries at HEAD; the three
  `.json` files are excluded, so ids appearing only there would not be counted.
- Unrun: the resolver, campaign tools, builds, lints and tests (wave in flight). Tool installs: none.

VERDICT: hand-built table over 60 revisions is self-consistent (two independent implementations agree);
9 revisions had dangling ids — S099 in rounds 35–37 (a range token, closed by adab4c7's RFC 9309 row,
duplicating S011's URL) and S367/S372/S373/S390/S409 in round 52 (closed by fd91527's five kake rows);
all five ids at 3994101 are held only by kotodama-shokunin as coincidental, different documents, and no
sibling holds kake's six documents.
