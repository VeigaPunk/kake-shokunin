Verdict: valid control — mutant breaks contract sentence 17 on the witness; reference matches the contract.

Target: `w1a3-MutNamespaceBinding__M11_entry_nested_url` (receipt: passed 24/24, met=true, toolSha256 b98696a3…).
Seat's manifest claims sentence 17 (target text said "11/14"; actual broken sentence is 17).

## Diff vs `/fast/scratch/hyaku/kake-r39a3w1/shared/reference.py`
Exactly one changed line (reference:156):
```
-            if loc not in allowed:
+            if loc not in allowed and loc != "url":
```
In the entry-children loop this exempts a sitemap-namespace `url` child from `element_unexpected`.
reference.py sha256 `663e051e…d69f8` (matches manifest); mutant sha256 `b98696a3…b2c8` (matches manifest + receipt).

## Runs (timeout 60 python3 -B <tool> --manifest witnesses/M11/manifest.json)
Witness: `<urlset …0.9><url><loc>https://example.test/</loc><url/></url></urlset>`; sitemapUrl `https://example.test/sitemap.xml`.

reference, exit 1:
`{"version": 1, "verdict": "failed-policy", "checks": [{"id": "witness", "status": "findings", "error": null, "findings": [{"code": "element_unexpected", "entry": 1}]}]}`

mutant, exit 0:
`{"version": 1, "verdict": "clean", "checks": [{"id": "witness", "status": "clean", "error": null, "findings": []}]}`

Both match the seat's recorded outputs byte-for-byte; stderr empty.

## Contract reasoning
- Sentence 17: "Any other child of an entry in the sitemap namespace … gives `element_unexpected` (entry-level)." The nested `<url/>` is in the sitemap namespace, is a child of the entry, and is not one of the permitted fields (loc/lastmod/changefreq/priority per sentences 15–16) — so the contract requires `element_unexpected` at entry 1.
- Sentence 14 ("elements in any other namespace … are ignored") does not apply: `url` here is in the sitemap namespace, not another namespace.
- Sentence 34 maps a non-error findings check to `failed-policy`, exit 1 — exactly the reference output. The contract fully determines the witness; mutant's `clean`/exit 0 violates it.

Per attacked statement: sentence 17 — mutant breaks it, reference holds. Sentences 11/14 (named in the target) — not what the defect touches; the manifest's own claim of 17 is correct.
Evidence for kill rule (1): the mutant diverges from the contract on an observable output → valid control.

Commands: `diff -u reference.py M11_entry_nested_url.py` exit 1 (one hunk); both `timeout 60 python3 -B …` exits above. No installs.
Report: .ufo/waves/round-39/w2a3/VerifyNamespaceBindingM11.md
