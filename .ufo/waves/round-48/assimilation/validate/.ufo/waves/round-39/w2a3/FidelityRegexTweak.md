Fidelity check: CtlRegexTweak (control shape "regex reader, no XML parser (24 of 24)").

Target: .ufo/waves/round-39/a3-controls/w1a3/CtlRegexTweak.py sha256 2d941dab16fbd28fba438c0fcf172c696c627503ff7faf57c9b4fcc892db2af3
Base:   .ufo/waves/round-39/a3-controls/dead-w1/CtlRegexOnly.py sha256 b7667eaf223caf1045f2e5298f8759205dc5703f7a8bfea1cf66930b93d21871
Report: .ufo/waves/round-39/w1a3/CtlRegexTweak.md sha256 acd0f94eb9877b2da18f845eaf2a0941f91d6eae240ad1d7a6bb038a328cea3f
L1 diff: /fast/scratch/hyaku/kake-r39a3w1/CtlRegexTweak/l1-materialized.diff sha256 28f6f65a7ed36b1c84fd06469dd0818b677c9183721e5ac5ca2c2806ea970a98

1. Shape — holds. Imports (file lines 15-21) are only json, os, re, sys, datetime.date, decimal, urllib.parse.
   `grep -nE 'xml\.etree|xml\.dom|xml\.sax|expat|lxml|ElementTree|minidom|defusedxml|bs4|html\.parser'` -> no matches.
   Structure recovery is TOKEN_RE regex scanning (lines 27-35, 73-131). Tweak adds namespace-prefix bookkeeping
   (line 110-115) and entity decoding (lines 63-69) via re.findall/re.sub only — still regex, no parser.
   Skipped work it claims to skip: full XML 1.0 well-formedness — confirmed by adversarial runs below.
   Changed lines vs base: 15 removed / 26 added (materialized diff), 430 -> 441 lines. Small tweak, not a rewrite.

2. Materialization — faithful, byte-for-byte. Fenced ```diff block extracted from the seat report (2638 bytes)
   equals l1-materialized.diff byte-for-byte. Applying that diff to dead-w1/CtlRegexOnly.py via
   `patch -p0 control.py < l1.diff` produces sha256 2d941dab… = the on-disk target. No drift.

3. Disagreement inputs (all three files verified malformed by xml.etree.ElementTree.parse; contract s8 ->
   xml_malformed, verdict failed-policy, exit 1). Manifest: {"version":1,"checks":[{"id":"t","file":"map.xml",
   "sitemapUrl":"https://example.test/sitemap.xml"}]}; command `python3 CtlRegexTweak.py --manifest <d>/manifest.json`:
   (a) map.xml = <urlset xmlns="…0.9" foo=bar><url><loc>https://example.test/a</loc></url></urlset>   (unquoted attr)
       control output: {"version": 1, "verdict": "clean", ... "findings": []} exit=0   [WRONG vs contract: clean/0]
   (b) map.xml = <urlset xmlns="…0.9"><url><loc>https://example.test/a</loc></url foo></urlset>        (attr on close tag)
       control output: clean, exit=0   [WRONG vs contract]
   (c) map.xml = <urlset xmlns="…0.9" xmlns:x="urn:a" xmlns:x="urn:b"><x:meta/>…</urlset>              (duplicate attr)
       control output: clean, exit=0   [WRONG vs contract; last binding wins in its dict]
   All three divergences are the regex shape's declared gap (no real well-formedness check), i.e. expected controls.

Per-statement verdicts:
- "regex reader, no XML parser": HOLDS — no XML parser imported or invoked anywhere.
- Materialized by L1 = seat's text: HOLDS — diff blocks byte-identical; patched base sha256 equals target sha256.
- Skips the work its shape says it skips: HOLDS — emits clean/0 on 3 inputs any XML-1.0-correct tool must
  flag xml_malformed/failed-policy/1 (unquoted attribute, attribute on close tag, duplicate attribute).
- Overstates anything: none found; docstring honestly lists remaining approximations (lines 9-13).

Verdict: faithful shortcut (and correctly materialized). Operability: runs offline on own fixtures, exits 0/1/2
per contract, no crash observed. Freshness: not measured. No tools installed (pacman paused; nothing needed).
Residual risk: unquoted-attr/close-tag-attr/dup-attr acceptance shown; other XML 1.0 lexical gaps (e.g. invalid
name start chars like <1x>) very likely also accepted but unverified here — same shape-consistent class.
