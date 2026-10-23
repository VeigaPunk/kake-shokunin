# VerifyNamespaceBindingM04 — M04_entry_local_default_binding

Verdict: **valid control** — the mutant breaks contract sentence 11 on the supplied witness; the reference obeys it.

## Diff (one change confirmed)
`diff -u shared/reference.py mutants/M04_entry_local_default_binding.py` (exit 1): exactly one changed line, at line 90:
- before: `if ns == NS:`
- after:  `if ns == NS and not (local == ("url" if rloc == "urlset" else "sitemap") and re.search(rb"\sxmlns\s*=", p.GetInputContext().split(b">", 1)[0])):`

sha256: reference `663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8`; mutant `f99b81ef1f00e127985199ee0d5d4c31b1cedfcb2dc5a155965aa18669aa2299` (matches mutants.json and the receipt's toolSha256). Witness hashes match mutants.json (manifest `7896a372…`, sitemap `4b7a8439…`).

## Runs (cd witnesses/M04; `timeout 60 python3 -B <tool> --manifest manifest.json`)
Witness sitemap.xml: `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><loc>https://example.test/</loc></url></urlset>`; manifest names `sitemapUrl: https://example.test/sitemap.xml`.

- reference, exit 0:
  `{"version": 1, "verdict": "clean", "checks": [{"id": "witness", "status": "clean", "error": null, "findings": []}]}`
- mutant, exit 1:
  `{"version": 1, "verdict": "failed-policy", "checks": [{"id": "witness", "status": "findings", "error": null, "findings": [{"code": "no_entries", "entry": null}]}]}`

Both outputs match the mutants.json `expected_detector` predictions byte-for-byte.

## Contract reasoning
Sentence 11: "The entries are the root's child elements in the sitemap namespace named `url` (in a `urlset`) or `sitemap` (in a `sitemapindex`)." Sentence 10 requires only that the root be `urlset`/`sitemapindex` in the sitemap namespace "whatever prefix binds it".

The witness `<url>` re-declares `xmlns="…/sitemap/0.9"` on itself; its expanded name is still `{http://www.sitemaps.org/schemas/sitemap/0.9}url`, so by sentence 11 it is unambiguously an entry. Namespace membership is a property of the expanded name, not of where the binding is declared — re-declaring a default namespace to the same URI is legal XML Namespaces and changes nothing. The `loc` value `https://example.test/` satisfies rules (g) and (h): absolute https URL, same scheme/host/port as `sitemapUrl`, and path `/` starts with the sitemapUrl directory `/`. No other rule fires. Expected output is therefore `clean`, which the reference produces.

The mutant's extra clause suppresses any `url`/`sitemap` child whose raw start-tag text contains ` xmlns=` — i.e. it treats a redundant default-namespace declaration as disqualifying the entry. On the witness it drops the only entry and emits `no_entries` (sentence 12's file-level finding for zero entries), which is wrong: the file has one valid entry. Divergence is not confined to this witness: any `<url xmlns="NS">` (or any entry tag redundantly binding the default prefix to the sitemap URI) is skipped, which also misnumbers the 1-based `entry` positions of later entries and can suppress `element_unexpected` classification paths.

## Note on receipt
Receipt `w1a3-MutNamespaceBinding__M04_entry_local_default_binding.json`: `passed 24/24`, `met: true`, toolSha256 matches the mutant bytes. That means no sealed case contains an entry element carrying a literal default-`xmlns` declaration (or a sibling tag whose start-tag text matches `\sxmlns\s*=`); the mutation is real but outside the sealed key's coverage. Verdict `valid control` stands on the contract text and the reproduced divergence, independent of the sealed score.

Per attacked statement (sentence 11): **holds** — the claimed defect is real and contract-decidable; the mutant is not equivalent and the contract is not silent on the witness.
