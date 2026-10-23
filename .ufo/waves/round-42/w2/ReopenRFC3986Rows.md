HOLDS — live RFC 3986 matches S117, S120 and the Gate pin; S117 equals `9e3c31d2` except `used-by`; S120 `teaches` opens `supersedes S117 —`. The restored S117 `teaches` is still overstated, and its Appendix A span is still wrong; S120 corrects both.

Fetch: `curl -sS -D /fast/scratch/hyaku/kake-r42w2/ReopenRFC3986Rows/rfc3986.headers -o /fast/scratch/hyaku/kake-r42w2/ReopenRFC3986Rows/rfc3986.txt -w 'http_code=%{http_code} size=%{size_download}\n' --max-time 60 https://www.rfc-editor.org/rfc/rfc3986.txt` → exit 0, HTTP/2 200, Date Fri, 23 Oct 2026 12:13:23 GMT, 141811 bytes, sha256 `3102dae4b68cebe40337730312fcb612297b8928547267e8b3d1ee6002b2d683`. Newline lines 3419 (`wc -l`). The file has 61 form feeds; Python `splitlines()` would mis-number line 867 as 882.

sha256 equal to both rows: yes (full digest in each `anchor`). `cmp` exit 0 against `.ufo/waves/round-42/sources/www.rfc-editor.org_rfc_rfc3986.txt` (SHA256SUMS records the same digest) and `.ufo/waves/round-41/sources/rfc3986.txt`. S098's recorded digest is the same string. Gate `3102dae4…d683` and `141,811` (round-42.md:16): holds. No separate round-42 wave-1 scout file for this URL was under `/fast/scratch/hyaku/kake-r42w1/`; the retained body equals the round-41 copy and this fetch.

Quotes (newline line numbers):
- Gate round-42.md:16 `"URI         = scheme ":" hier-part [ "?" query ] [ "#" fragment ]"`: verbatim yes, line 867 (nine spaces before `=`).
- Rows' backtick `` `URI = scheme ":" hier-part [ "?" query ] [ "#" fragment ]` ``: verbatim no (spaces collapsed). Same tokens at line 867 and at Appendix A line 2697 (`URI           = …`, eleven spaces). The cited line 867: holds.
- `` `port = *DIGIT` ``: verbatim no. `port        = *DIGIT` at line 1189 (§3.2.3, header line 1183); `port          = *DIGIT` at line 2720. Prose 1195–1196 allows an empty port (`*DIGIT` is zero or more).
- `absolute-URI`: rule `absolute-URI  = scheme ":" hier-part [ "?" query ]` at line 1470 (§4.3, header 1463) and line 2706. Prose 1465–1468: absolute form without a fragment. holds.
- Percent triplet: lines 640–641 and `pct-encoded = "%" HEXDIG HEXDIG` at line 647. holds.
- Appendix A heading line 2695; last production line 2788 (`sub-delims` continuation); blank 2789; Appendix B line 2790. Line 2690 is the page-48 banner; line 2691 is a form feed.

S117 (`corpus/SOURCES.md:125`). scope: supported (URI components in §3 / Appendix A; distinct from S098 §§2.1–2.3, S029 §3, S089 §5.2). teaches: overstated — the grammar paraphrase holds, but "a value `urlsplit` accepts can still fail this grammar" is not in the RFC. anchor span 2690–2760: wrong (starts on the page banner; 2760 is mid-`path`, `/ path-absolute`; the grammar continues through 2788).

S120 (`corpus/SOURCES.md:128`). Opens `supersedes S117 —` (U+2014 EM DASH): yes. scope: supported. teaches: supported (the urlsplit clause is marked as the lane's observation, not the RFC's). anchor span 2695–2788: supported.

Cells vs `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 9e3c31d2:corpus/SOURCES.md` (exit 0): S117 equal on id, source, kind, tier, scope, anchor, teaches, status, opened, recheck. Only `used-by` differs (raw index 1077): now `SCORECARD.md, corpus/lessons/round-41.md`; at `9e3c31d2` `SCORECARD.md "Round 41", corpus/lessons/round-41.md`. Lesson round-42.md:26-28 and :78-79: holds for S117. No tool installed.
