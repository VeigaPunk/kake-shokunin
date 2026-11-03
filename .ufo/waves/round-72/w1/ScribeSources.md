row_cells=11 census_file_exit=1 census_root_exit=0 new_errors=0 new_warnings=0

# ScribeSources — S439 registry row, census proof (round-72 w1)

## Commands and exit codes
- census --file scratch mod copy: exit 1 ; base copy (3c68645a corpus): exit 1
- census --root $S/fleet kake (conf-backed, clone of lane at base 3c68645a + mod SOURCES + stub lesson): exit 0 ; same with base SOURCES: exit 0
- census --root $S/tree kake (literal form): exit 2, 'ERROR: config not found: .../tree/shokunin.conf' (lane tree carries no shokunin.conf; see notes)

## Census validate --root (lane-name form, mod)
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	W04	S416 duplicate url ziyuan.baidu.com/college/courseinfo?id=1399 across scopes
kake	W04	S417 duplicate url ziyuan.baidu.com/college/courseinfo?id=267&page=15 across scopes
kake	W04	S427 duplicate url developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers across scopes
kake	W04	S433 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	ok	/fast/scratch/hyaku/kake-r72/ScribeSources/fleet/kake-shokunin/corpus/SOURCES.md

## Census validate --root (lane-name form, base) diff vs mod: empty

## Census validate --file (mod) full output
file	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
file	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
file	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
file	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
file	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
file	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
file	W04	S110 duplicate url www.w3.org/TR/xml across scopes
file	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
file	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
file	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
file	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
file	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
file	W04	S416 duplicate url ziyuan.baidu.com/college/courseinfo?id=1399 across scopes
file	W04	S417 duplicate url ziyuan.baidu.com/college/courseinfo?id=267&page=15 across scopes
file	W04	S427 duplicate url developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers across scopes
file	W04	S433 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
file	E11	S088 missing used-by scripts/source_recheck.py
file	E11	S089 missing used-by scripts/source_recheck.py
file	E11	S090 missing used-by scripts/source_recheck.py
file	E11	S091 missing used-by scripts/source_recheck.py
file	E11	S092 missing used-by scripts/source_recheck.py
file	E11	S117 missing used-by SCORECARD.md
file	E11	S118 missing used-by .ufo/waves/round-41/c1_count.py
file	E11	S118 missing used-by SCORECARD.md
file	E11	S119 missing used-by .ufo/waves/round-41/oracle_crosscheck.py
file	E11	S119 missing used-by SCORECARD.md
file	E11	S120 missing used-by SCORECARD.md
file	E11	S121 missing used-by SCORECARD.md
file	E11	S122 missing used-by SCORECARD.md
file	E11	S124 missing used-by SKILL.md
file	E11	S129 missing used-by SCORECARD.md
file	E11	S131 missing used-by SCORECARD.md
file	E11	S132 missing used-by SCORECARD.md

## Census validate --file (base) diff vs mod: empty
(identical)

## Census counts (root form)
base rows=176 tier.A=153 status.mined=146; mod rows=177 tier.A=154 status.mined=147 (delta: one row, tier A, mined)

## Notes (read with the verdict)
1. census_file_exit=1 is NOT a new error. `--file` resolves used-by paths against the parent of corpus/ in the scratch copy, which holds only corpus/. The same 21 E11 lines (SCORECARD.md, SKILL.md, scripts/source_recheck.py, .ufo/waves/round-41/*) fire at base and mod; the base and mod --file outputs are byte-identical (diff exit 0). The census_root leg resolves those paths against the full tree and exits 0 with 0 E and 16 W, matching base.
2. Pipe count: the seat text says "11 cells between 13 pipes". 11 cells require 12 pipes; census NF==13 after -F'|' is the same 12-pipe shape. The row was built with 11 cells and 12 pipes (awk -F'|' gives NF=13). No pipe appears inside any cell.
3. Literal `--root $S/tree kake` exits 2 ("config not found: .../tree/shokunin.conf"): the lane tree does not track shokunin.conf. The lane-name form was therefore run through $S/fleet (shokunin.conf holding the kake line copied from the fleet conf, repo kake-shokunin -> symlink to the clone). This is the conf-backed equivalent; no other change.
4. Anchor check: retained body $LANE/.ufo/waves/round-72/sources/gitcli.html sha256 4e1ea3a5951e10f5c31157d1b03e0938d9b09130c5db099aa5baec6a02714a1e, 51306 bytes (matches the row). The quoted paragraph "Because -- disambiguates revisions and paths in some commands" and the --end-of-options text are both present in the body.
5. Duplicate check: no existing registry row carries the git-scm gitcli URL (E04 clean); used-by corpus/lessons/round-72.md exists in the scratch copy as an empty stub (not in lane committed bytes at 3c68645a).
6. Lane untouched: scratch clone only; no lane file written except this report and S439-row.txt. Working-tree lane files (gate-status-ledger.md modified, corpus/lessons/round-72.md untracked) were not read or changed.
7. Tooling: none installed. pacman not run.
