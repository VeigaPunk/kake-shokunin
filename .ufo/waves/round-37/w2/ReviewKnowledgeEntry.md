# ReviewKnowledgeEntry — corpus/knowledge/robots-txt-rules.md vs S011/S095/S096 (r37 wave 2)

Seat KakeR37.ReviewKnowledgeEntry, leaf. Target `git show 79d3c780:corpus/knowledge/robots-txt-rules.md` (83 lines). Sandbox `/fast/scratch/hyaku/kake-r37w2/ReviewKnowledgeEntry/`. No tools installed.
## Commands (exit codes)
- `sha256sum sources/S0{11,95,96}.txt` + `zcat *.html.gz | sha256sum`/`wc -c`/`wc -w` → 0; all six text/body sha256, byte and word counts equal `sources/receipts.json` (S011 8e632e48…/bbaa2806…, S095 a9094853…/c8c1f204…, S096 d17aa81d…/fe4b5e3a…).
- `curl raw.githubusercontent.com/google/robotstxt/master/{robots.cc,robots.h}` → 200/200, master `22b355ff`; sha256 `d05a7fa7…d473`, `912f3a5c…b0bd5` = wave-1 ScoutReopenS096 artifacts.
- Sandbox clone at 79d3c780: `node scripts/corpus-contract.mjs --root .` → exit 0, 0 findings (header trio present).
- Probe `python3 -B scripts/robots_audit.py --manifest probe/m.json` (tool sha 5eb767ec…; m.json 9d919099…) → exit 1, findings `row2-raw-uri: exposed`, `robots-503: blocked`; rows 1, 5, encoded row 2 and `/robots.txt`@200 clean. `--manifest probe/noid.json` (08f3dbdc…) → exit 2, `check_invalid`.
## Findings by severity
- **M1 (overstated, L63) "This follows Figure 4".** S011 Fig. 4 row 2: path `/foo/bar?baz=https://foo.bar` → path to match `https%3A%2F%2Ffoo.bar` (S011.txt, §2.2.2 table). The lane reading ("reserved characters are never decoded or encoded", SCORECARD.md:1844-1845) leaves `:`/`/` raw. Reproduced: `Disallow: /foo/bar?baz=https%3A` vs raw URL → tool allows (`exposed`), Figure 4 disallows. The reading follows rows 1 and 5 only. Wave 1 never examined row 2 (ScoutReopenS011.md:24-30 cite rows 1 and 5 only).
- **M2 (overstated, L57) RFC condition invented.** S011 §2.2.2: "The /robots.txt URI is implicitly allowed." (no condition). "when a robots file's rules decide access" is contract (e) (SCORECARD.md:1840) plus (a) 5xx "including /robots.txt" (1815). Reproduced: 503 + `/robots.txt` → `blocked`. Belongs under a Lane reading marker that says it departs from the RFC sentence, as L63 does for D1.
- **M3 (operability, L67) usage omits required inputs.** It lists URL, token, expectation and status but not `id` (required, unique), the `{"version":1,"checks":[…]}` wrapper, the absolute http(s) URL rule, or the command `python3 scripts/robots_audit.py --manifest PATH` (SCORECARD.md:1797-1809). A check built from L67 alone → `check_invalid`, exit 2 (noid.json probe).
- **M4 (freshness/traceability, L63 + header L1-3).** L63 cites `robots.cc`/`robots.h`, but the header names only README "Quickstart"/"Notes". The S096 SOURCES row anchors are README sections only (SOURCES.md:104). No code file is retained or listed in receipts.json, so the L3 recheck ("compare the retained source receipts") cannot cover the code claim. The claim holds at master 22b355ff (robots.cc:184,194-199 uppercase-only; robots.h:153 "'url' must be %-encoded according to RFC3986").
- **L1 (overstated, L37).** S095 "Syntax" lists `sitemap` as supported, but S095 "Grouping of lines and rules" says rules other than allow/disallow/user-agent "are ignored by the robots.txt parser" and the sitemap line does not split a group. That is the lane behavior. The "unlike" contrast holds only for sitemap discovery, not parsing. S095 is not "parser documentation".
- **L2 (overstated, L81) "does not apply crawler-specific extensions".** L31 adopts the BOM drop. robots.cc:435 calls it a "Google-specific optimization", and S095 "File format" documents it. S011 has no BOM text, yet L31 cites only S011 §§2.2, 2.3, 2.5.
- **L3 (overstated, L49).** RFC: "If an 'allow' rule and a 'disallow' rule are equivalent". The entry says "equally specific". Equal length is the lane/Google reading (S095 "Order of precedence for rules"), not RFC text.
- **L4 (citation gap, L33).** "Field names are case-insensitive": not stated in S011 §§2.2.1-2.2.4. It is inferable only from ABNF literal case-insensitivity (RFC 5234, not retained). S095 "Syntax" states it but is not cited there. Also "rules" wrongly includes `user-agent` (S011 §2.1 defines Rule as allow/disallow).
- **L5 (wording, L21).** "undefined file remains unavailable" conflates RFC terms: "unavailable" = 4xx (§2.3.1.3). §2.3.1.4 says "undefined for a reasonably long period".
- **L6 (metadata).** The header cites S095 "Syntax" and "opening", which are not in the S095 SOURCES row anchors (SOURCES.md:103). The S011 SOURCES row still shows verified 2026-10-19/365d, while the header claims 2026-10-23 (the receipt confirms 02:50:49Z), so the row was not refreshed. "Limits" and "Frozen predicate" (L11, L77, L83) are claim bullets (SCORECARD.md:1770,1791), not "C1 contract" items. L11's S011 §2.3.1 cite does not bear on its sentence.
## Sentence table (L = entry line; S = supported, O = overstated, U = unsupported)
| L | Location | Verdict |
|---|---|---|
| 1-3 | receipts.json; SOURCES.md:19,103-104; corpus-contract exit 0 | trio present, hashes reproduce; M4, L6 |
| 9 | S011 §1 "not a form of access authorization"; §3 | S |
| 11 | SCORECARD.md:1791-1793, 1797-1802 | S (S011 §2.3.1 cite irrelevant) |
| 15 | S011 §2.3 "/robots.txt (all lowercase) in the top-level path"; S095 "apply only to the host, protocol, and port" | S |
| 17 | S095 "folder/robots.txt Not a valid robots.txt file"; not-valid-for examples | S |
| 19 | S011 §2.3.1.1, §2.3.1.3 "MAY access any resources", §2.3.1.4 "MUST assume complete disallow" | S |
| 21 | S011 §2.3.1.4 | S, wording L5 |
| 23 LR | SCORECARD.md:1813-1815 (a) | matches contract |
| 25 | S095 "except 429"; 5xx 12 h / 30 days / cached copy | S |
| 29 | S011 §2.3 UTF-8 text/plain; §2.3.1.5; §2.5 "at least 500 kibibytes" | S |
| 31 LR | SCORECARD.md:1816-1824 (b) | matches contract; BOM provenance L2 |
| 33 | S011 §2.2.4 "MUST NOT interfere"; case-insensitivity not in S011 | S/O (L4) |
| 35 LR | SCORECARD.md:1822-1824; S011 §2.2.2 SHOULD ignore, §2.2.4 | matches contract |
| 37 | S095 "Syntax" vs "Grouping of lines and rules" | O (L1) |
| 39 | S011 §2.2.1 "case-insensitive matching", "MUST be combined", "*" fallback | S |
| 41 LR | SCORECARD.md:1806, 1825-1830 (c) | matches contract |
| 43 LR | SCORECARD.md:1825-1827 | matches contract |
| 45 | S095 "Only one group is valid"; "specific … and global groups (*) are not combined" | S |
| 49 | S011 §2.2.2 "first octet", "most octets", "equivalent … SHOULD" | O (L3) |
| 51 | S011 §2.2.3 Figure 5 | S |
| 53 LR | SCORECARD.md:1831-1834 (d); case-sensitivity implied by (d)/(e) octet compare, not stated | matches (implied) |
| 55 LR | SCORECARD.md:1835-1837 | matches contract |
| 57 | S011 §2.2.2 unconditional sentence | O (M2) |
| 59 LR | SCORECARD.md:1838-1840 (e) | matches contract |
| 61 | S011 §2.2.2 both MUST sentences; Fig. 4 rows 1, 5 | S |
| 63 LR | SCORECARD.md:1840-1845 matches; "follows Figure 4" vs row 2; robots.cc:184,194-199, robots.h:153 | contract match; O (M1); code claim S but unretained (M4) |
| 67 | SCORECARD.md:1803-1809 | S but incomplete (M3) |
| 69 LC | SCORECARD.md:1810-1812 | matches contract |
| 71 LC | SCORECARD.md:1846-1857 (f)(g) Verdict | matches contract |
| 73 | S096 README Quickstart "test a local robots.txt against a user-agent and URL"; Notes "will not perform full normalization" | S |
| 77 LR | SCORECARD.md:1801-1802, 1791-1792 | matches contract |
| 79 | S011 §3 "makes the paths discoverable", "security measure relevant to the application layer" | S |
| 81 | S095 "describes Google's interpretation"; S096 Notes | O (L2) |
| 83 | SCORECARD.md:1770, 1791 | S |
Lane reading/contract markers: all 14 match the contract text. The markers are used for every contract rule, not only for the SHOULD/MAY choices that SCORECARD.md:1792-1793 restricts "lane reading" to (benign). L57 lacks a marker it needs (M2).
## Residual risk / gaps
- RFC 9309 errata page not checked (it is not a named source). robots.cc was read, not compiled, and the M1/L2 Google-side behavior was not executed. The C1 counter was not run (not my item). Probe processes exited; nothing of mine is left running.
