Verdict: valid control (mutant violates contract sentence 14 — and 11 — which the reference obeys).

Diff (exactly one line, mutant M07 line 90 vs shared/reference.py:90):
`-            if ns == NS:` → `+            if ns == NS or local == "url":`
sha256 reference 663e051e…69f8; mutant 3bdf80f0…dc15 (matches mutants.json:1147 and receipt toolSha256).

Runs (witness manifest witnesses/M07/manifest.json, sha 7896a372…d8e7; sitemap `<x:url xmlns:x="urn:foreign">` inside a default-NS urlset, sha c83584f4…d73b):
`prlimit --as=4000000000 timeout 60 python3 -B shared/reference.py --manifest …/manifest.json` → exit 1:
`{"version": 1, "verdict": "failed-policy", "checks": [{"id": "witness", "status": "findings", "error": null, "findings": [{"code": "no_entries", "entry": null}]}]}`
`prlimit --as=4000000000 timeout 60 python3 -B mutants/M07_foreign_root_url.py --manifest …/manifest.json` → exit 0:
`{"version": 1, "verdict": "clean", "checks": [{"id": "witness", "status": "clean", "error": null, "findings": []}]}`
Both byte-identical to mutants.json reference_output/mutant_output records.

Contract: S14 "Elements in any other namespace, at any level, are ignored." → `x:url` ignored → zero entries → S12 `no_entries` → S34 failed-policy/1. The contract fully decides the witness; reference matches, mutant treats `x:url` as a `url` entry (its default-NS `<loc>` validates) → clean/0, violating S14 and S11 ("entries … in the sitemap namespace"). Under a sitemapindex root the same line also mis-flags a foreign `url` as `element_unexpected` instead of ignoring it (still S14).

Claim text said sentences 10/14; mutants.json:1148 lists only 14. S10 (root element) is untouched — `out["root"]` set at line 87 before the mutated test. Claim "10/14": overstated for 10, holds for 14.

Note: receipt w1a3-MutNamespaceBinding__M07…json shows passed 24/24 as a *met* control — the sealed key exercises no input distinguishing this defect; local witness kills it.
No tools installed. Key-blindness respected: no l1priv/sealed/cases/key paths touched, counter not run.
