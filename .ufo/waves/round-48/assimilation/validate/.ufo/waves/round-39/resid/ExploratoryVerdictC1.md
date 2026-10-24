VERDICT: unprovable-but-better
Reviewer (non-author): KakeR39A3.ExploratoryVerdictC1 — I did not author the build or the sealed key; author seat was BuildSitemapAudit (L1 KakeR39A3).
Axes: operability (does the tool run and decide correctly offline), freshness (does it cover ground the lane previously lacked).

WHY UNPROVABLE
- Frozen kill rule (1) fired pre-build: 15 single-sentence mutants and a parser-free regex reader met the sealed 24-case predicate (.ufo/waves/round-39/sealed/cases.json — `cases` len 24). A counter that both contract-true and contract-false readers pass cannot decide C1; no counter decides an exploratory claim.

WHY BETTER (evidence, independent of the counter)
- Novelty: `git -C kake-shokunin ls-tree -r --name-only 2909f1dc -- scripts/ | grep -c sitemap_audit` → 0 (exit 0). Base had `robots_audit.py`, which ignores `Sitemap` records (PROVINCE.md:302) and lists "sitemaps" as Still open (PROVINCE.md:322, PROVINCE.md:23). No offline sitemap-file auditor existed before round 39.
- Selftest: `timeout 600 python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` → `PASS 150/150`, exit 0 (3.3 s; includes fault-injected silent/constant tools, per scripts/sitemap_audit_selftest.py "Fault-injection tools").
- Fresh adversarial inputs (5 files + 2 manifests under /fast/scratch/hyaku/kake-r39a3res/KakeR39A3.ExploratoryVerdictC1/), all outputs match the contract on my independent reading; the first two rules are absent from the sealed 24 (`HTTP://`, `2001`, `user:` — no matches in cases.json):
  1. Namespace-URI case variant `xmlns="HTTP://WWW.SITEMAPS.ORG/..."` → `root_invalid` (file-level, no other findings). Matches c1-contract.md sentence 10 (exact lowercase namespace); a case-folding reader would wrongly accept.
  2. IPv6 + userinfo locs → `[2001:db8::1]:8443` entry 1 `loc_out_of_scope`; `http://user:secret@example.com/dir/page2.html` entry 2 clean. Matches sentences 22/24/25 (absolute http(s), non-empty host; userinfo not prohibited or compared); no crash on the bracketed host.
  3. Repeated loc + repeated priority → `{"field_repeated",1},{"loc_repeated",1}` only — (g)–(h) and the priority value rule correctly skipped (sentences 15–16); out-of-scope second loc and invalid `2.0` produce no extra findings.
  4. Sitemapindex scope/lastmod → `{"loc_out_of_scope",1},{"lastmod_invalid",3}`: https-vs-http scheme flagged (sentence 27), `:80` = default port accepted and `/deep/nested.xml` path NOT scope-checked (27), `2023-02-29` rejected, `2024-02-29T23:59:59.1+05:30` accepted (28–29).
  5. Stray SM-namespace root child + comment → `{"element_unexpected",null},{"no_entries",null}` (sentences 12–13; comments ignored).
- Error paths: no args → exit 64, stdout empty (sentence 2); `checks: []` → exact sentence-3 document `{"version":1,"verdict":"could-not-evaluate","error":"input_invalid","checks":[]}`, exit 2. Both observed.
- Manifest runs: manifest_a exit 1 failed-policy, manifest_b exit 1 failed-policy, one JSON document each, nothing else written (sentences 1, 33–34).

Commands (exit codes): selftest 0; build A 1; build B 1; usage 64; empty-checks 2; base ls-tree count 0.

RESIDUAL RISK / GAPS
- No `lsp` device in this seat's tool inventory (only xd://ast_edit, xd://debug); caller/definition/diagnostics checks fell back to read/grep — semantic claims above rest on code reading of scripts/sitemap_audit.py:60-124 (_parse_url/_directory_of), :127-158 (value rules), :161-206 (encoding/doctype/parse order), :208-272 (tree/entry/loc rules), :276-330 (manifest), :340-377 (main/verdict), not on an LSP answer.
- Two contract-quiet spots, not defects: doctype+malformed precedence (build checks doctype first, scripts/sitemap_audit.py:195-198) and a ≥2048-char non-absolute loc emits both loc_too_long and loc_not_absolute (scripts/sitemap_audit.py:260-266; sentence 23 imposes no skip). Both are lane-reading gaps in the contract, not observed misbehavior.
- Not exercised by me directly (selftest covers): 50 MB / 50,000-entry limits; gzip and live fetch out of contract scope by design.
- Entry numbering with interleaved foreign-namespace root children (numbering counts SM-namespace entries only, sentence 11) not directly probed.
- Verdict is a recommendation; C1 remains exploratory and admits no proof beyond the reasons named here.
