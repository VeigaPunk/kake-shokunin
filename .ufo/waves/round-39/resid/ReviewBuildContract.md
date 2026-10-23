# ReviewBuildContract — sitemap_audit.py vs c1-contract.md s1–34

Verdict: 4 corner-case deviations + 1 contract-ambiguous precedence; ~160 probes (all exit/stderr
correct) confirm every sentence is implemented. Axes: operability/freshness (built & run today at tip
d8a20a99; py3.14.8). Deviations (all LOW-MED; none reach the 24-case key's covered ground):

D1 s8 (LOW): `<?xml version="1.1"/"1.5"/"1.9"/"1.10"?>` → clean (expected xml_malformed; contract
   names XML 1.0). Expat accepts any 1.x; no version gate (sitemap_audit.py:191).
D2 s6/s8 (MED): UTF-16LE/BE **without BOM** → clean. NUL-interleaved bytes decode as UTF-8
   (:180-183), then `ET.fromstring(str)` re-encodes and expat re-sniffs as UTF-16 (:193), so the
   "well-formed" check never sees the U+0000s the contract's byte model implies.
   Input: `doc.encode("utf-16-le")` → `{"verdict":"clean"}` exit 0.
D3 s8/s9 (LOW, contract-ambiguous): prescan (:189-190) reports `doctype_present` for a document that
   is ALSO malformed (`<!DOCTYPE urlset><urlset xmlns="…"><url><loc>x` truncated → doctype_present;
   `<!DOCTYPE urlset>` alone → doctype_present). s8 reads unconditionally "otherwise xml_malformed";
   s9 is the flagged lane reading — build seat declared this interpretation (w2a3/BuildSitemapAudit.md:57).
D4 s21+s22 (LOW): `urlsplit` strips interior \t\r\n, so `<loc>http://example.com/di\tr/a</loc>` and
   `<loc>…/di\nr/a</loc>` → clean (as-written not absolute → loc_not_absolute). Same for sitemapUrl
   under s4 (`http://example.com\t/dir/sitemap.xml` accepted). :72 vs strip(XML_WS) :100.
D5 s4 (LOW): a check repeating the `id` of an earlier check that was itself `check_invalid` is NOT
   flagged (seen_ids only registers valid checks, :341-343) — literal "repeats an earlier check's id".

Cosmetic (not counted): `http://h:` empty port accepted (RFC-lax hostport, s4/s22); `file:""` →
file_unreadable not check_invalid; `itertext()` concatenates loc text across child markup (s21
"element value" undefined for markup); manifest UTF-8 BOM accepted (contract silent); NaN/Inf rightly
rejected via parse_constant (:307). `--manifest=<path>` → exit 64, 0B stdout — implemented (:379).

Sentence map (all implemented, evidence = harness run under /fast/scratch/hyaku/kake-r39a3res/
ReviewBuildContract/t*,t2,t3):
s1 :378-416 emit :368 (stderr 0B every run) | s2 :379-381 (no-args/=/extra/--help → 64)
s3 :288-317,383-390 (13 invalid manifests → input_invalid exit 2) | s4 :326-348,320-323,67-84
s5 :174-177,391 (missing/dir→file_unreadable; subdir resolves) | s6 :180-185 (latin1 bytes→encoding_invalid)
s7 :55-60,142-152,186-187 (utf-16 decl incl. lowercase → encoding_invalid; uTf-8 ok; PI not decl)
s8 :191-194 (+D1,D2) | s9 :155-169,189-190 (+D3; unclosed DOCTYPE→xml_malformed; comment-DOCTYPE ok)
s10 :199-206 (wrong ns/local/no-ns → root_invalid; prefixed ok) | s11 :208-217 (prefixed entries counted)
s12 :218,222-223 (empty both kinds → no_entries) | s13 :212-216 | s14 :209-211,233 (other-/no-ns ignored)
s15 :243-249 (missing/repeated → skip g–h; lastmod still checked) | s16 :236-241,250-264 (dup lastmod/cf →
field_repeated, value skipped; index lastmod×2 same) | s17 :241-243 (cf/priority in index → element_unexpected)
s18 :227-264 (order not checked; permuted entry clean) | s19 :178-179 (52,428,804→too_large; ==52,428,800 clean)
s20 :219-220 (50,001→too_many_entries + entry findings; 50,000 clean) | s21 :99-100 (NBSP survives→loc_not_absolute)
s22 :67-84,275-281 (+D4; rel/ftp/no-host/bad-port → loc_not_absolute; upper scheme ok; `h:` trailcolon lax)
s23 :30,269-270 (2047 clean / 2048 + unicode codepoints → loc_too_long; coexists w/ loc_not_absolute)
s24 :71-84 (scheme/host case-insens; :80↔implicit match; https:443 ok) | s25 :273-281 (path prefix via
sitemapUrl dir; /di ≠ /dir/) | s26 :87-92 (case-sens, dot-seg, %61 literal) | s27 :273-281 (index: scheme/
host/port only — port 8080 & https → out_of_scope, path free)
s28-30 :46-51,103-121 (all 21 forms incl. frac/min-TZD/offsets/year(-month)/lowercase tz; index both ways)
s31 :39-41,124-125 (Daily/dailyy/empty → changefreq_invalid) | s32 :53,128-135 (±/.5/1./-0 ok; 1.1/1e-1/.→invalid)
s33 :326-361,368-370 (shape, order, id echo/null, dedup+file-level-first sort) | s34 :393-416
(could-not-evaluate→2 / failed-policy→1 / clean→0; mixed error wins)

Commands: `prlimit --as=4000000000 timeout 300 python3 harness.py|harness2.py` (scratch above) →
~160 runs, rc∈{0,1,2,64} as mapped, stderr 0B always; spot CLI runs exit 64/0B. Residual: key not
run (not this seat's job); nothing testable was left unexercised. No tools installed; no lane mutation.
Report: .ufo/waves/round-39/resid/ReviewBuildContract.md
