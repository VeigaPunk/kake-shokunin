# ReviewBuildRepairs — diff attack on C1 build (E/U/R), sentences 4/6/8/21/22

Reviewer: KakeR40.ReviewBuildRepairs (leaf seat). Base f171c58b, build 56d57ee4.
Scope: `git diff f171c58b 56d57ee4 -- scripts/sitemap_audit.py` (10+/4-, 3 hunks).
No tools installed.

## What I ran (all exit codes)
- `git diff f171c58b 56d57ee4 -- scripts/sitemap_audit.py` — exit 0; hunks: `_parse_url` guard,
  `_audit_file` NUL check, `_evaluate_check` duplicate reordering.
- `python3 -B probe.py` (99 cases, base vs build, JSON+exit compared) — exit 0; 47 AGREE, 52 DIFFER.
  Full table: /fast/scratch/hyaku/kake-r40res/ReviewBuildRepairs/cases/probe_result.json.
- `python3 -B scripts/sitemap_audit_selftest.py --tool <build>` — **PASS 179/179, exit 0**.
- `python3 -B scripts/sitemap_audit_selftest.py --tool <base>` — **PASS 156/179, exit 1**
  (23 red fixtures = E utf16-NBOM ×5, U tab/cr/lf/leading-C0 ×14, R repeat-after-invalid ×2
  + upper-id; matches lesson).
- expat micro-probes: `fromstring` on NUL strings — rejects NUL in most positions but TOLERATES
  interleaved NULs forming a well-formed document (utf16 NBOM ASCII parses clean).

## Probe table (summary; base → build)
E (utf16 NBOM ASCII, LE+BE): clean → xml_malformed [fix]. BOM variants: encoding_invalid both.
NUL in body/attr/comment: xml_malformed both. NUL + decl-encoding mismatch: encoding_invalid → xml_malformed.
U: sitemapUrl TAB/CR/LF anywhere or leading C0(00–1F)/space: clean → check_invalid [fix].
loc internal TAB/LF/CR: clean → loc_not_absolute [fix]. loc leading/trailing XML WS, %09, foreign-NS: clean both.
Internal C0 (01,0B,0C,0E,1F,00) in sitemapUrl host and leading DEL 7F, trailing space: AGREE (accepted or rejected identically).
R: dup after earlier check invalid only on file/url gate: second check clean → check_invalid [fix].
dup valid-first, empty id, int-vs-str, case, NFC/NFD: AGREE. Clean-path sentences (loc scope, lastmod, priority, https): AGREE.

## Findings (severity)
1. LOW — E repair holds and generalizes: base judged UTF-16-NBOM ASCII sitemaps CLEAN (expat swallows
   the NULs); build's post-decode `"\x00" in text` (build copy line 189-190) returns xml_malformed for
   every NUL position probed; no false positive found. With BOM, encoding_invalid preserved (sentence 6).
2. INFO — ordering change: NUL + declared-encoding mismatch now xml_malformed instead of encoding_invalid
   (build line 189 before 191-193). Both are error codes; contract sentences 7 vs 8 are unordered, so
   neither verdict is wrong; behavioral delta only.
3. MEDIUM — U residual gap (not a regression, both versions): internal C0 other than TAB/CR/LF
   (U+0000–0008,000B,000C,000E–001F) in a sitemapUrl host/path still passes `_parse_url`
   (build line 70 guard checks only first char ≤ space plus \t\r\n anywhere) and is judged absolute;
   trailing space also accepted. Outside the declared class (S111 strips only leading C0/space + TAB/CR/LF
   anywhere), but sentence 4 + S102 "RFC-3986" would exclude them — claim implements its class, not full
   URL validation.
4. LOW — R repair holds on both unsampled sub-shapes (earlier check failing only file gate / only url
   gate → repeat now check_invalid, build line 337-344); integer-vs-string ids stay distinct, case and
   NFC/NFD distinct (matches witness list).
5. None found — no repair breaks another sentence: all normal clean/out-of-scope/lastmod/priority probes
   byte-identical base vs build; selftest 179/179 green on build, red on base.

## Per attacked statement
- s4 (check_invalid): holds for TAB/CR/LF/leading-C0 sitemapUrl and for repeats after invalid earlier checks;
  overstated only in the RFC sense above (internal C0).
- s6 (encoding): holds, unchanged behavior verified.
- s8 (xml_malformed): holds, now uniform for ALL NUL placements.
- s21 (strip only XML WS): holds — only " \t\r\n" stripped; internal TAB kept then rejected.
- s22 (loc_not_absolute): holds for TAB/CR/LF-bearing locs; escapes/WS cases stay clean.

Verification gaps: no oracle beyond urllib.parse/S111 reading; loc C0 unreachable (XML parse rejects first);
counter scores not re-run (out of seat scope).
