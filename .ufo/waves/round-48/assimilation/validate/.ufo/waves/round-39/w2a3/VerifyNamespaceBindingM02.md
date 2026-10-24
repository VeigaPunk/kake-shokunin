# VerifyNamespaceBindingM02 — w1a3-MutNamespaceBinding__M02_root_trailing_slash

Verdict: **valid control** — the mutant breaks contract sentence 10 on a constructible witness; the reference obeys the sentence.

Checked (axes: operability = every command ran clean and reproducible; freshness = bytes/hashes re-verified today):
- `diff -u shared/reference.py mutants/M02_root_trailing_slash.py` → exit 1, exactly one changed line (137): `if rns != NS or ...` → `if rns.rstrip("/") != NS or ...`. Single-point change confirmed.
- sha256: mutant `e58a3d3a…ba77b` == receipt `toolSha256` == mutants.json entry (the scored tool is the mutant); reference `663e051e…d69f8` == mutants.json pristine before/after.
- Receipt (read only `label`/`passed`/`met`/`toolSha256`): `passed 24, met true`.
- Witness hashes match mutants.json: manifest `7896a372…`, sitemap `882b8308…`; sitemap bytes: `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9/"/>` — namespace URI ends in a slash.

Runs (`timeout 60 prlimit --as=4000000000 python3 -B <tool> --manifest .../witnesses/M02/manifest.json`; manifest sitemapUrl `https://example.test/sitemap.xml`):
- reference.py → `{"version": 1, "verdict": "failed-policy", "checks": [{"id": "witness", "status": "findings", "error": null, "findings": [{"code": "root_invalid", "entry": null}]}]}` — exit 1, stderr empty.
- M02_root_trailing_slash.py → `{"version": 1, "verdict": "failed-policy", "checks": [{"id": "witness", "status": "findings", "error": null, "findings": [{"code": "no_entries", "entry": null}]}]}` — exit 1, stderr empty.

Sentence 10 (c1-contract.md): "The root element must be `urlset` or `sitemapindex` in the namespace `http://www.sitemaps.org/schemas/sitemap/0.9`, whatever prefix binds it; otherwise `root_invalid` (file-level) and no other finding (S102; S103)."

Reasoning: XML namespace names compare exactly; the contract names the exact URI (no trailing slash) and licenses no normalization anywhere (sentence 26's "as written" shows the contract's no-normalization posture). The witness root is in `…/0.9/` — a different namespace — so sentence 10 plus sentences 33–34 fully determine the output: findings exactly `[{root_invalid, null}]`, `failed-policy`, exit 1. The reference matches; the mutant instead accepts the non-conforming root and reports `no_entries`, a finding sentence 10's "no other finding" clause forbids. Not `equivalent` (this witness distinguishes them), not `contract-silent` (sentence 10 decides).

Residual: the frozen counter scored these same bytes 24/24 (`met: true`) — the sealed key contains no case with a trailing-slash root namespace, so sealed-key coverage misses this sentence-10 edge. mutants.json itself scopes its `killed` verdict to "supplied local witness, not the sealed key" — honest. No installs; no persistent writes outside sandbox/report; transient /tmp stderr captures removed in-command.
