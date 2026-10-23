Verdict: valid control — the mutant breaks contract sentence 14, which the reference obeys; the contract fully determines the witness output. (Evidence that kill claim (1) was sound; note the sealed key scored it 24/24, i.e. the key holds no distinguishing case.)

Commands (all run 2026-10-23, cwd = witness dir for tool runs):
- `diff -u shared/reference.py mutants/M10_foreign_priority.py` → exit 1, exactly one hunk: reference.py:154 `if ns != NS:` → `if ns != NS and loc != "priority":`. Matches mutants.json `single_point_change` (line 154, changed_lines 1). Confirmed: one change only.
- `sha256sum`: mutant `4fe2e38d9179cbea995a89d405d3220b0db2302b7ee1fd0e5c669a42685df393` (= receipt `toolSha256`, = mutants.json); reference `663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8`; manifest `7896a372bde566ce3d0053cac13b025b74ef42b05b68ce85f21c4f514401d8e7`; sitemap `fa89eeff7ab7aa5ec72cd165f89388b51e72da2cf6d7c9d0f276946922ee547e`. All match recorded values.
- `timeout 60 python3 -B /fast/scratch/hyaku/kake-r39a3w1/shared/reference.py --manifest manifest.json` → exit 0:
  `{"version": 1, "verdict": "clean", "checks": [{"id": "witness", "status": "clean", "error": null, "findings": []}]}`
- `timeout 60 python3 -B /fast/scratch/hyaku/kake-r39a3w1/MutNamespaceBinding/mutants/M10_foreign_priority.py --manifest manifest.json` → exit 1:
  `{"version": 1, "verdict": "failed-policy", "checks": [{"id": "witness", "status": "findings", "error": null, "findings": [{"code": "priority_invalid", "entry": 1}]}]}`

Witness: urlset entry `<url>` contains `<x:priority xmlns:x="urn:foreign">2</x:priority>` — a foreign-namespace child whose local name is `priority`, value `2`.

Sentence text (c1-contract.md):
- S14: "Elements in any other namespace, at any level, are ignored." (rule (d); contract.md:46-48)
- S17: "Any other child of an entry in the sitemap namespace … gives `element_unexpected` (entry-level)." (contract.md:53-55)

Reasoning: `x:priority` is in `urn:foreign`, not the sitemap namespace. S14 commands that it be ignored; S17 never triggers because it covers only sitemap-namespace children, and rules (e)/(k) apply only to sitemap-namespace `priority` children. The reference `continue`s on `ns != NS` → no findings → clean/0: the contract-determined output. The mutant lets a foreign `priority` through; `priority` is in `allowed`, so it is value-checked under (k): "2" fails 0.0–1.0 → `priority_invalid`/1. Divergence is real and contract-decidable, so not equivalent, not contract-silent. mutants.json claims sentence 14 only; the assignment's "14/17" is unsupported for 17 — the mutant emits no `element_unexpected` for the element and 17's trigger never applies.

Per attacked statement: S14 — holds (mutant breaks it; reference obeys). S17 — wrong (named in assignment but absent from mutants.json; not actually violated).

Notes: receipt w1a3-MutNamespaceBinding__M10_foreign_priority.json shows `passed: 24, met: true` — the sealed 24-case key did not discriminate this mutant, consistent with a genuine-but-uncovered defect class. No tools installed; no sealed/key paths touched; reference read-only.
