# FidelityHandTokenizer — w2a3 falsification of CtlHandTokenizer

Lane bounds: leaf, no subagents. Key-blindness kept: no l1priv/sealed paths, no cases.json/key builders, counter never run. Verdict: **faithful shortcut** (not secretly correct, not mis-materialized).

## Shape — holds
Imports are only `json`, `os`, `sys`, `from urllib.parse import urlsplit` (CtlHandTokenizer.py:3–6). Tokenization is literal `text.split("<")` (:167), `chunk.split(">")` (:152), `partition`; tag stack hand-maintained (:219–262); entity unescape via `split("&")` (:70). `grep -nE 'import|re\.|xml|html|ElementTree|minidom|expat|sax|lxml'` → only the 4 imports plus an `xml_char()` helper and an `xmlns` literal string. `grep -nE 'eval|exec|__import__|subprocess|ctypes|importlib|compile\('` → 0 real hits (matches were `could-not-evaluate` string literals). No hidden parser.

## Skipped work — holds (genuinely skipped, not implemented)
Namespace handling is literal-prefix equality: `literal_name()` (:284), `child_prefix != prefix` skip (:379, :396), root-only `xmlns` attr check (:371–372), child `Node` attrs discarded (`attrs if not stack else None`, :251). No in-scope binding map, no unbound-prefix check, no descendant rebind. DOCTYPE: any `<!DOCTYPE` token raises `DoctypePresent` (:186–187) — full internal-subset grammar skipped. Everything else (encoding, lastmod calendar/leap math :301–334, priority decimal :337–350, loc scope :288–298, 50MB/50k limits, manifest+check validation, output shape, exit codes) is implemented.

## Materialization — holds
`sha256sum` of lane file and w1 sandbox `control.py` both = `edf2ed363f2afd46ff4184eee2b466910dc1e98b938422f0ec3e75b206945322`, matching the seat report's declared hash (report line 18); `diff -q` → IDENTICAL (byte-for-byte). No `l1-materialized.diff` exists for this seat (fresh build, not a tweak: `dead-w1/` lists no CtlHandTokenizer base; diffs exist only for CtlGuessTweak/CtlRegexTweak/CtlXsdTweak under `a3-controls/w1a3-materialized/` and the named path `/fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/l1-materialized.diff` is absent).

## Disagreement probes (contract-derived, run on the lane bytes)
Sandbox `/fast/scratch/hyaku/kake-r39a3w2/FidelityHandTokenizer/t/`, `sitemapUrl=https://example.com/maps/s.xml`. Command: `timeout 30 prlimit --as=4000000000 /usr/bin/python3 -B …/w1a3/CtlHandTokenizer.py --manifest manifest.json` → exit 1, stderr empty.

| probe | contract-correct (sentences) | control output |
|---|---|---|
| p1 `<url xmlns="urn:foreign">` rebind | `no_entries` (s.11–14: foreign subtree ignored, zero NS entries) | clean — literal `url` counted as entry |
| p2 `<q:url>` w/ `xmlns:q`=sitemap URI, unprefixed root | clean (s.10–11: prefix binds same URI) | `no_entries` — prefix `q` != `""` dropped |
| p3 undeclared `<u:extra/>` in entry | `xml_malformed` (s.8: unbound prefix ill-formed) | clean — skipped as foreign child |

All three reproduce the seat's own declared gaps (report :40–42 rebound/alias/undeclared), independently re-derived from the contract.

## Per attacked statement
- "str-split tokenizer, no re/xml/html": **holds**.
- "skips namespace resolution + full DOCTYPE parsing": **holds** — probes prove the work is absent.
- "L1 materialized seat text byte-for-byte": **holds** — sha256 + diff identity; no tweak diff expected.

## Residual
Local probes only; sealed-key discrimination unknown. No installs. No persistent processes.
