Verdict: valid control — M09 breaks contract sentence 24; the reference obeys it, so kill rule (1) fired correctly.

Mutant: /fast/scratch/hyaku/kake-r39a3w1/MutStdlibSubstitution/mutants/M09.py
sha256 2e78066920f6bb2889cb65bb6e01ab6d2b6402584878f68df80d0035e0907785 — matches mutants.json and receipt toolSha256.
Reference: /fast/scratch/hyaku/kake-r39a3w1/shared/reference.py sha256 663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8.

Diff: exactly one line (reference.py:36). Old: `return sch, p.hostname.lower(), port, (p.path or "/")` — where `port` was computed as `p.port`, defaulted to 80/443 only when `port is None`. New: `return sch, p.hostname.lower(), (p.port or (80 if sch == "http" else 443)), (p.path or "/")`. The `or` truthy fallback conflates an explicit port 0 with a missing port.

Commands (exit codes):
`prlimit --as=4000000000 timeout 60 python3 -B reference.py --manifest witnesses/M09/manifest.json` → exit 1
stdout: {"version": 1, "verdict": "failed-policy", "checks": [{"id": "M09", "status": "findings", "error": null, "findings": [{"code": "loc_out_of_scope", "entry": 1}]}]}
`prlimit --as=4000000000 timeout 60 python3 -B mutants/M09.py --manifest witnesses/M09/manifest.json` → exit 0
stdout: {"version": 1, "verdict": "clean", "checks": [{"id": "M09", "status": "clean", "error": null, "findings": []}]}

Witness: sitemapUrl `http://e.test:0/s.xml` (explicit port 0); loc `http://e.test/` (no port → default 80).

Contract sentence 24: "Scheme and host are compared case-insensitively; a missing port equals the scheme's default (80 for `http`, 443 for `https`)." Sentence 25: a loc "whose scheme, host or port differs from the `sitemapUrl`'s" gives `loc_out_of_scope`.

Reasoning: port 0 is present in the sitemapUrl, not missing, so sentence 24's default does not apply; the sitemap port is 0 while the loc's effective port is 80. Under sentence 25 the ports differ → `loc_out_of_scope`. The contract decides the witness and the reference matches it. The mutant silently rewrites the explicit 0 to 80, reports clean — the exact sentence-24 violation claimed. Holds as stated.
