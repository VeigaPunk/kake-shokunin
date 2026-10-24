# ReviewBuildWitnesses — build vs wave-2 witnesses (residual review)

Verdict: PASS — `scripts/sitemap_audit.py` at lane tip `d8a20a99` reproduces the
contract-decided reference output on all 18 inputs: 18/18 match (stdout JSON
deep-equal AND exit code; stderr empty for every run). No actionable finding.

Axes: operability (clean run from each witness dir, zero stderr, exits 0/1 per
contract s34); freshness (rebuild today 2026-10-23 at tip d8a20a99).

Method: for each input, `timeout 60 prlimit --as=4000000000 python3 -B
scripts/sitemap_audit.py --manifest manifest.json`, cwd = witness dir. Expected =
reference output stated in each `w2a3/Verify*.md` (e.g. VerifyUrlAuthorityM10.md:17,
VerifyNamespaceBindingM11.md:18, VerifyEntryNumberingM02.md:12, VerifyUrlAuthorityM03.md:12,
VerifyUrlAuthorityM05.md:10, VerifyNamespaceBindingM08.md:15, VerifyNamespaceBindingM10.md:6,
VerifyNamespaceBindingM03.md:12). Witness dirs:
`/fast/scratch/hyaku/kake-r39a3w1/<Family>/witnesses/<M>/`; raw outputs at
`/fast/scratch/hyaku/kake-r39a3res/ReviewBuildWitnesses/outs/<label>.{out,err}`.

| # | witness (label) | expected (ref) | build | match |
|----|------------------|-----------------|-------|-------|
| 1 | StdlibSubstitution M09 (SSL-M09) | failed-policy loc_out_of_scope@1, exit1 | identical | yes |
| 2 | NamespaceBinding M02 (NS-M02) | failed-policy root_invalid, exit1 | identical | yes |
| 3 | NamespaceBinding M03 (NS-M03) | failed-policy root_invalid, exit1 | identical | yes |
| 4 | NamespaceBinding M04 (NS-M04) | clean, exit0 | identical | yes |
| 5 | NamespaceBinding M07 (NS-M07) | failed-policy no_entries, exit1 | identical | yes |
| 6 | NamespaceBinding M08 (NS-M08) | clean, exit0 | identical | yes |
| 7 | NamespaceBinding M09 (NS-M09) | clean, exit0 | identical | yes |
| 8 | NamespaceBinding M10 (NS-M10) | clean, exit0 | identical | yes |
| 9 | NamespaceBinding M11 (NS-M11) | failed-policy element_unexpected@1, exit1 | identical | yes |
|10 | UrlAuthority M03 (UA-M03) | clean, exit0 | identical | yes |
|11 | UrlAuthority M04 (UA-M04) | clean, exit0 | identical | yes |
|12 | UrlAuthority M05 (UA-M05) | clean, exit0 | identical | yes |
|13 | UrlAuthority M09 (UA-M09) | clean, exit0 | identical | yes |
|14 | UrlAuthority M10 (UA-M10) | failed-policy loc_out_of_scope@1, exit1 | identical | yes |
|15 | EntryNumbering M02 (EN-M02) | failed-policy loc_missing@1, exit1 | identical | yes |
|16 | Regex control (a) unquoted attr | failed-policy xml_malformed, exit1 | identical | yes |
|17 | Regex control (b) attr on close tag | failed-policy xml_malformed, exit1 | identical | yes |
|18 | Regex control (c) duplicate xmlns:x | failed-policy xml_malformed, exit1 | identical | yes |

**Count: 18/18 matches.**

Commands/evidence:
- `git -C kake-shokunin rev-parse master` -> d8a20a99b7816d3a61cd21a58d6b72bbf465087d (tip).
- 15 witness exit codes: SSL-M09=1 NS-M02=1 NS-M03=1 NS-M04=0 NS-M07=1 NS-M08=0
  NS-M09=0 NS-M10=0 NS-M11=1 UA-M03=0 UA-M04=0 UA-M05=0 UA-M09=0 UA-M10=1 EN-M02=1.
- Regex-control exit codes: RC-a=1 RC-b=1 RC-c=1; stderr total 0 bytes across all 18 runs.
- Regex-control fixtures materialized under `.../regexcontrols/{a,b,c}/` per
  FidelityRegexTweak.md (manifest id "t"; map.xml = unquoted attr / attr on close tag /
  duplicate xmlns:x); expected from contract s8 (xml_malformed -> failed-policy/1).

Residual risk/gaps: build verified only on these 18 inputs; no claim about the sealed
24-case key (not run here). No lsp device in this leaf session; verdict rests on the
executed runs above (18/18), not on grep. No tools installed (pacman untouched);
no lane mutation besides this report.

Report: .ufo/waves/round-39/resid/ReviewBuildWitnesses.md
