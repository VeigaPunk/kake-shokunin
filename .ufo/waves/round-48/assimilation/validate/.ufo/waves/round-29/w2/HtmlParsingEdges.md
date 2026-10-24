# HtmlParsingEdges: base_path_audit.py HTML tokenization edges

Repo kake-shokunin at 7697990cbca20291f3b0367b8ff4220e93b38b03, read from a sandbox clone. Axis: operability.
Sandbox artifacts: pages/ (46 fixtures), predictions.tsv, results.json, oracle/out.json, browser/results.json.

## Verdict
BROKEN: 8 pages exit 0 while a browser sees a same-site reference outside /repo/; 3 pages exit 1 on
references a browser never loads (docstring L6-7, L35-38 claim browser-like resolution).
HOLDS: exit codes and JSON contract. 46/46 pages exit 0 or 1 with one JSON object; 4000 fuzz snippets and
5 large inputs raised no uncaught exception; committed selftest 30/30 (rc 0).
Predicted before running (predictions.tsv, code path per row): observed matched on findings,
referencesChecked and exit code, 46/46. Truth (parse5 8.0.1 + WHATWG URL; Chromium, 16 file-only checks)
matched predictions 46/46.

## Silent passes (exit 0; browser sees a same-site reference outside /repo/)
- 20 `<svg><base href=evil>` replaces the document base for the whole page. Chromium keeps file: (B1); an HTML base switches it (B2).
- 22 `<image src>`: browsers parse it as img (B3). Docs list the set but not this mapping.
- 42, 43 CDATA outside SVG hides later markup (`<![CDATA[ > <a>`; unclosed). Chromium shows the anchor (B4, B5, B15).
- 12, 15, 16, 17 `///h/p`, `https:/h/p`, `https:///h/p`, `https:&sol;h/p`: dropped by resolve_url (L402-407) and
  _parse_absolute (L364-366). Chromium resolves all four to same-site URLs outside /repo/ (B6). Docs contradicted (B).

## False failures (exit 1; browser sees no reference)
- 32 `<script><!--<script></script>`: html.parser ends raw text at the first `</script` (B7).
- 33 `<script src=... />`: a self-closing script sets no raw-text mode (B9).
- 37 `<template/>`: opened and closed at once; the browser hides the rest (B8).
- 39 `<noscript>` link: documented (L30-31); with scripting on, Chromium shows no link (B14).

## Limits and silent gaps
- 19 late `<base>` after an earlier link: the tool applies the final base to all refs (L570). Browser timing not run [INFERENCE].
- 38 unclosed `<template>` silently skips the rest of the page (B16). Docs silent.
- 23 `<svg><image href>`: outside the documented set (L13-14).
- Correct but undocumented: comments (25-30), script text (31, 34), entities (9-11, 14), case (5, 36),
  duplicate href (7, 8), CDATA in SVG (40, 41), RCDATA/RAWTEXT (44, 45), bogus end tag (46), valueless attributes (4).

## Root causes (for the planner)
html.parser has no SVG/MathML model (20, 42, 43); its self-closing and raw-text rules differ from HTML (32, 33, 37);
resolve_url and _parse_absolute drop browser-valid forms (12, 15-17); image-to-img is a tree-construction rule (22).

## Per page: id name F/r truth docs verdict
F/r = observed findings/referencesChecked (pred = obs on all 46). Truth: c Chromium, p parse5 + WHATWG URL.
Docs: S stated, I implied, N silent, B contradicted, L limit. Verdict: ok, FN, FP, doc (documented), lim (limit).
```
01 unquoted-href     1/2 1p I  ok    |   02 single-quoted-hre 1/2 1p I  ok 
03 valueless-attr-be 1/2 1p I  ok    |   04 valueless-href    0/1 0p N  ok 
05 mixed-case-img    1/2 1p N  ok    |   06 unquoted-trailing 1/2 1p I  ok 
07 dup-href-first-in 0/2 0p N  ok    |   08 dup-href-first-ou 1/2 1p N  ok 
09 entity-decimal-sl 1/2 1c N  ok    |   10 entity-named-sol  1/2 1c N  ok 
11 entity-hex-protoc 1/2 1c N  ok    |   12 entity-triple-sla 0/2 1c B  FN 
13 entity-backslash- 1/2 1c S  ok    |   14 entity-srcset     1/2 1p N  ok 
15 scheme-single-sla 0/2 1c B  FN    |   16 scheme-triple-sla 0/2 1c B  FN 
17 entity-scheme-sin 0/2 1c B  FN    |   18 base-before-ancho 0/2 0p S  ok 
19 early-link-late-b 0/2 0p SL lim   |   20 svg-base-evil     0/2 1c N  FN 
21 base-href-empty   1/2 1p S  ok    |   22 html-image-elemen 0/1 1c N  FN 
23 svg-image-href    0/1 0p S  lim   |   24 svg-a-href        1/2 1p I  ok 
25 comment-anchor    0/1 0p N  ok    |   26 comment-dashdash- 0/1 0c N  ok 
27 comment-lookalike 1/2 1p N  ok    |   28 abrupt-empty-comm 1/2 1c N  ok 
29 bang-close-commen 1/2 1p N  ok    |   30 downlevel-reveale 1/2 1p N  ok 
31 script-string-anc 0/1 0p N  ok    |   32 script-double-esc 1/2 0c N  FP 
33 script-selfclosin 1/3 0c N  FP    |   34 script-uppercase- 0/1 0p N  ok 
35 template-anchor   0/1 0p S  ok    |   36 template-uppercas 0/1 0p S  ok 
37 template-selfclos 1/2 0c N  FP    |   38 template-unclosed 0/1 0c N  ok 
39 noscript-link     1/2 0c S  doc   |   40 svg-cdata-anchor  0/1 0p N  ok 
41 svg-cdata-single- 0/1 0p N  ok    |   42 html-cdata-gt-anc 0/1 1c N  FN 
43 html-cdata-unterm 0/1 1c N  FN    |   44 iframe-rawtext-an 0/1 0p N  ok 
45 textarea-rcdata-a 0/1 0c N  ok    |   46 bogus-end-tag-spa 0/1 0c N  ok 
```

## Commands and exit codes
git clone + checkout 7697990: rc 0. npm install --prefix oracle parse5: rc 0 (parse5 8.0.1).
46 x python3 -B clone/scripts/base_path_audit.py --manifest pages/ID/manifest.json: rc 0 x25, rc 1 x21, rc 2 x0.
python3 -B scripts/base_path_selftest.py: rc 0 (30/30). node oracle/run.mjs pages oracle/out.json: rc 0.
chromium --headless --dump-dom file://... x16 (B1-B16): rc 0 x16; proxy 127.0.0.1:9, DNS mapped to NOTFOUND.
evaluate_page fuzz (seed 29; 4000 snippets, 5 large inputs): no uncaught exception.
Installs: parse5 8.0.1 via npm, sandbox only (DOM oracle). Chromium pre-installed, used read-only. No pacman.
Not verified: 19 browser timing; Firefox and WebKit; subresource fetches (by design); formaction, object,
frame, use, imagesrcset (outside the set); performance (another reviewer's axis).
