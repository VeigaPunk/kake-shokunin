# FidelityHtmlParserReader — CtlHtmlParserReader (a3-controls/w1a3) audit
**Verdict: faithful shortcut.** Keeps the html.parser-reader shape, genuinely skips XML
well-formedness / case identity / namespace resolution, is materialized byte-for-byte, and all
three seat-predicted counterexamples reproduce live. Python 3.14.8; every run under
`timeout` + `prlimit --as=4000000000`; only this report written to the lane.

## Materialization (byte-for-byte)
- `l1-materialized.diff` absent at `/fast/scratch/hyaku/kake-r39a3w1/CtlHtmlParserReader/`
  (dir contains only NOTE.md, control.py, t/); verified directly instead.
- `sha256sum`: lane `a3-controls/w1a3/CtlHtmlParserReader.py` =
  `bac9c7c4cd8dc3635b6dd17a7bb0fa03c4b439d257aa0d5580dc120123bdca91` (10,714 B) — identical to
  w1 artifact `control.py` AND to the decoded `exec()` string argument of fenced block 1 in
  `w1a3/CtlHtmlParserReader.md`, matching the seat-claimed sha. L1 materialized the decoded
  source, not the exec-wrapper (wrapper bytes differ, as the report itself flagged).
  Fenced block 2 is the selftest harness, not control source.
- Command: `timeout 60s python3 /fast/scratch/hyaku/kake-r39a3w2/FidelityHtmlParserReader/bytecmp.py` → exit 0.

## Shape kept / work skipped
- Imports (`CtlHtmlParserReader.py:3-10`): datetime, decimal, html.parser, json, pathlib, re,
  sys, urllib.parse only. grep `etree|ElementTree|minidom|xml\.sax|expat|lxml|defusedxml|
  parseString|xml\.dom|pulldom` → 0 matches. No xml.* import; named shape kept.
- Skips stated work: HTML-recovery `handle_endtag` (`:77-82`, "deliberately accepts unclosed
  and mismatched elements"); no nonempty-stack check after `reader.close()` (`:149-156`);
  root validated by literal `xmlns`/`xmlns:P` attribute string compare, not namespace
  resolution (`:161-165`); child entry/field matching by literal tag prefix (`:168-175`,
  `:186-189`); HTMLParser lowercases names (NOTE.md:4) so case identity is skipped.
- Rest of ruleset genuinely implemented (loc form/scope, lastmod, changefreq, priority,
  limits, manifest validation, output schema/verdict at `:234-288`).
- Tweak check: no `CtlHtmlParserReader*` base in `a3-controls/dead-w1/`; unified-diff vs
  nearest base `CtlXsdDelegate.py` = +254/-556 → fresh w1a3 control, not a tweak.

## Runs — `timeout 120s prlimit --as=4000000000 python3 -B <control> --manifest t/manifest.json`
exit 1, stdout: `{"version":1,"verdict":"failed-policy","checks":[{"id":"c0-valid","status":"clean",...},{"id":"c1-upper","status":"clean",...},{"id":"c2-unclosed","status":"clean",...},{"id":"c3-prefixed","status":"findings","error":null,"findings":[{"code":"no_entries","entry":null}]}]}`

- `t/upper.xml` sha `81a25516…`: uppercase `URLSET`/`URL`/`LOC` under sitemap xmlns → control
  **clean**; sentence 10 (XML names case-sensitive) requires `root_invalid`. Disagrees. ✔
- `t/unclosed.xml` sha `747747f5…`: no closing `</url></urlset>` → control **clean**;
  sentence 8 requires `xml_malformed`. Disagrees. ✔
- `t/prefixed.xml` sha `c0327a25…`: `xmlns:s` bound to the sitemap URI, `s:url`/`s:loc`
  children → control **`no_entries`**; sentences 11–14 (prefix binds the URI) require clean.
  Disagrees. ✔
- `t/valid.xml` sha `e06c2fff…` baseline → control **clean**: divergences are shape-specific,
  not brokenness. Fixture+manifest hashes recorded; manifest sha `49808b0e…`.

## Per attacked statement (w1a3 report [INFERENCE] predictions)
- "uppercase urlset → clean vs root_invalid" — **holds** (observed clean).
- "unclosed urlset → clean vs xml_malformed" — **holds** (observed clean).
- "s:-prefixed entries → no_entries vs clean" — **holds** (observed no_entries).
- Report's 4th prediction (xmlns rebound to urn:foreign → clean vs no_entries) unrun here;
  consistent with literal-marker code at :161-175.

## Residual risk
- `absolute_url` also rejects interior XML-whitespace in loc (`:93-94`), beyond sentence 22's
  scheme/host test — a possible extra false-finding on space-containing locs; not exercised.
- Divergences only matter if the sealed suite probes case/malformed/prefix-alias inputs.
- No installs; tools: system python3.14.8, coreutils. No lane mutation except this report.
