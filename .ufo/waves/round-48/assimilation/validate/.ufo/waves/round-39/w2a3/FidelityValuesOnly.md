# FidelityValuesOnly — r39 w2 falsify-a3 review

Verdict: **faithful shortcut** (skips the named work, does not implement it).

## Materialization
- Lane `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-39/a3-controls/w1a3/CtlValuesOnly.py` sha256 `ff518efed54a96246e87754add88c137b5b5159df1bfbd7fe340df226c72ddf3` == seat report line 21 hash (`…/w1a3/CtlValuesOnly.md:21`) == w1 sandbox `…/CtlValuesOnly/control.py` hash (byte-for-byte identical content).
- No `l1-materialized.diff` exists for this seat: `/fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/l1-materialized.diff` missing, and `a3-controls/w1a3-materialized/` contains only CtlGuessTweak/CtlRegexTweak/CtlXsdTweak diffs; `dead-w1/` has no CtlValuesOnly base. Fresh control, not a tweak — diff check N/A.

## Shape / forbidden techniques
- Imports (tool.py:4-11) are stdlib only: datetime, decimal, json, os, re, sys, urllib.parse, xml.etree.ElementTree. No network, subprocess, lxml, or non-stdlib use.
- Audit logic (tool.py:72-127) implements value rules 21–32 on local names (`local_name`) of ancestors and descendants; does NOT implement rules 6,7 (encoding/declared-encoding), 8 (well-formedness except `ET.fromstring` parse failure → `xml_malformed`, an unavoidable parse prerequisite), 9 (doctype), 10 (root), 11-13 (entry structure/unexpected), 15-17 (entry children/cardinality/repeat), 19 (too_large), 20 (too_many_entries), nor 14 (extension-namespace exclusion). Manifest/output/verdict handling (rules 1-5, 33-34) retained; urlset-only applicability of changefreq/priority and index scope retained — matches report lines 4-5.
- Counterexample flow in report line 7 verified below; report assertions hold.

## Disagreement inputs (3, built from contract; correct-tool expectation = contract outcome)
Manifest `t/manifest.json` (checks: empty/noloc/extloc, sitemapUrl `http://example.com/sub/sitemap.xml`); command: `timeout 60 prlimit --as=4000000000 -- python3 -B tool.py --manifest t/manifest.json` → exit 1, stdout:
`{"version":1,"verdict":"failed-policy","checks":[{"id":"empty","status":"clean","error":null,"findings":[]},{"id":"noloc","status":"clean","error":null,"findings":[]},{"id":"extloc","status":"findings","error":null,"findings":[{"code":"loc_not_absolute","entry":1}]}]}`
1. `t/empty.xml` — `<urlset/>` with zero entries. Contract S12 → `no_entries` (file-level). Control: clean. Misses S12 work. ✔ disagreed.
2. `t/noloc.xml` — one `<url>` with only valid `<lastmod>2026-10-23</lastmod>`. Contract S15 → `loc_missing` entry 1 (no `{(mod_invalid` finding since S28 allows YYYY-MM-DD). Control: clean. Misses S15 work; correctly applies S28. ✔ disagreed.
3. `t/extloc.xml` — one `<url>` with sitemap-NS `<loc>http://example.com/sub/page</loc>` plus foreign-NS `<x:loc>not a url at all</x:loc>`. Contract S14 ignores foreign-NS elements → clean. Control: flags `loc_not_absolute` at entry 1 (false positive). Matches report line 9 claim. ✔ disagreed.

## Self-test
Seat self-test (report line 12, run from w1 sandbox): `timeout 90 /usr/bin/prlimit --as=4000000000 -- /usr/bin/python3 -B /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/selftest.py` → 5 manifest + 3 usage cases all `match: true`, failures []; exit 0.

## Bounds / hygiene
No lane file written by this seat (verified read-only scan; lane timestamps from siblings only). No counter run, sealed key, or forbidden path accessed. No tool installed. Sandbox writes <200 MB. Process trees terminated (all commands exited).

## Residual risk / verification gaps
- Independent proof of every edge case in rules 21–32 (zone-offset boundary, `+24:00` vs `+23:59`, exact `2,048` char boundary, priority `0.0`/`1.0`/`.5`/`-.5`, port-default equivalence) exercised only via aggregate bhand above and the seat's own fixtures; no per-edge independent probes run here.
- Rule-8 partial touch (xml_malformed) judged necessary parse plumbing, not implementation of the skipped rules group.
- Sealed coverage unknown by construction; anything the seal asks outside the named omitted rules rests on the unproven-above 21–32 edges.
