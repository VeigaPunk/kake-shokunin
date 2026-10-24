# VerifyNamespaceBindingM08 — M08_foreign_entry_url

**Verdict: valid control** — mutant breaks contract sentence 14 (sentence 11 unchanged by the diff); reference matches the contract on the witness.

## Diff (exactly one change, confirmed)
`diff -u shared/reference.py mutants/M08_foreign_entry_url.py` (exit 1) — single line at reference.py:154:
```
-            if ns != NS:
+            if ns != NS and loc != "url":
```
sha256: reference `663e051e…69f8`, mutant `35c41a83…232c6` — both match the sha256 recorded in mutants.json (reference "before"/"after" and mutant entry).

## Runs on the seat's witness (`witnesses/M08/manifest.json` → `sitemap.xml`)
Sitemap: `<urlset xmlns=…0.9><url><loc>https://example.test/</loc><x:url xmlns:x="urn:foreign"/></url></urlset>`
- `timeout 60 python3 -B shared/reference.py --manifest …/manifest.json` → exit 0:
  `{"version": 1, "verdict": "clean", "checks": [{"id": "witness", "status": "clean", "error": null, "findings": []}]}`
- `timeout 60 python3 -B mutants/M08_foreign_entry_url.py --manifest …/manifest.json` → exit 1:
  `{"version": 1, "verdict": "failed-policy", "checks": [{"id": "witness", "status": "findings", "error": null, "findings": [{"code": "element_unexpected", "entry": 1}]}]}`

## Contract reasoning
- Sentence 14: "Elements in any other namespace, at any level, are ignored." The witness's `<x:url>` child of `<url>` is a foreign-namespace entry child, so it must be ignored — no `element_unexpected`.
- Sentence 17 restricts `element_unexpected` to "any other child of an entry in the sitemap namespace"; foreign-ns `url` does not qualify. Sentence 11 (entries = root children in the sitemap namespace) is about root-level enumeration, which the diff does not touch — the manifest's own record cites sentence 14; the claimed "11" is imprecise but the defect is real.
- The mutant's `and loc != "url"` lets a foreign-ns child named `url` past the namespace guard into the `allowed` check, yielding `element_unexpected` — exactly a violation of sentence 14. The contract fully decides this witness; the reference obeys, the mutant does not.

## Per-claim assessment
- Claim "breaks sentence 14": **holds**.
- Claim "breaks sentence 11": **overstated** — the diff doesn't touch root-level entry enumeration; sentence 17 is the companion rule.
- Receipt `w1a3-MutNamespaceBinding__M08_foreign_entry_url.json`: label, passed=24/24, met=true, toolSha256 matches the mutant bytes — consistent with kill rule (1) firing correctly.

No tool installs. Bounds respected: no l1priv/sealed paths, no cases.json/counter, read-only repo access.
