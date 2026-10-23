Verdict: **valid control** — M03 breaks contract sentence 10; the reference obeys it. Kill rule (1) fired correctly.

## What was checked
- Mutant: `/fast/scratch/hyaku/kake-r39a3w1/MutNamespaceBinding/mutants/M03_root_uri_casefold.py` sha256 `69700da7b25e9d4710e5a213b02ec4910596ec5cd8617da72e73e524b6444178` (matches receipt `toolSha256` and mutants.json entry).
- Reference: `/fast/scratch/hyaku/kake-r39a3w1/shared/reference.py` sha256 `663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8`.
- `diff -u` reference vs mutant, exit 1: exactly one changed line — `if rns != NS or rloc ...` → `if rns.lower() != NS or rloc ...` at line 137 (matches recorded single_point_change).
- Witness files hash-verified: manifest `7896a372...`, sitemap `81d99e2f...` (contents: `<urlset xmlns="http://www.SITEMAPS.org/schemas/sitemap/0.9"/>` — root ns URI differs only in case).

## Commands and outputs
`timeout 60 python3 -B <tool> --manifest /fast/scratch/hyaku/kake-r39a3w1/MutNamespaceBinding/witnesses/M03/manifest.json`

- reference.py, exit 1:
  `{"version": 1, "verdict": "failed-policy", "checks": [{"id": "witness", "status": "findings", "error": null, "findings": [{"code": "root_invalid", "entry": null}]}]}`
- M03 mutant, exit 1:
  `{"version": 1, "verdict": "failed-policy", "checks": [{"id": "witness", "status": "findings", "error": null, "findings": [{"code": "no_entries", "entry": null}]}]}`

Both match the recorded reference_output/mutant_output in mutants.json byte-for-byte.

## Attacked sentence
10. "The root element must be `urlset` or `sitemapindex` in the namespace `http://www.sitemaps.org/schemas/sitemap/0.9`, whatever prefix binds it; otherwise `root_invalid` (file-level) and no other finding (S102; S103)."

## Reasoning
- Namespace identity is literal URI equality; sentence 10 names the URI as a fixed literal. Wherever the contract wants case-insensitivity it says so (sentence 7 encoding, 22 scheme, 24 scheme/host) — it does not for the namespace URI, so `SITEMAPS` ≠ `sitemaps`. The contract decides the witness: `root_invalid`, and "no other finding".
- Reference emits exactly `root_invalid` → obeys. Mutant casefolds the ns, accepts the root, then (root empty) emits `no_entries` → deviates.
- No crash path: `parse` sets `rns` to `""` for an unnamespaced root (line 84), never `None`, so `.lower()` is safe. Divergence is confined to ns-URI-case inputs, where the mutant is always wrong (children are still compared with `ns == NS` exactly).
- Per attacked statement: sentence 10 — **holds** (reference obeys; mutant breaks it).
- Tool installs: none.
