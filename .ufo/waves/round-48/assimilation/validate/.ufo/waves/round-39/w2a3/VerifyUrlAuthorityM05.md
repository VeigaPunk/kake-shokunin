VERDICT: valid control — the mutant breaks contract sentence 22 on the witness; the reference obeys it.

Diff vs `/fast/scratch/hyaku/kake-r39a3w1/shared/reference.py` (sha256 663e051e…f8): exactly one changed line, line 170:
`-            if a is None:` → `+            if a is None or ":" in a[1]:`
`a[1]` is the lowercased parsed hostname; the mutant rejects any `loc` whose host contains `:`, i.e. every IPv6-literal host. Mutant sha256 560fb760…10a matches `mutants.json` and the receipt `toolSha256`.

Witness (`mutants.json` → `/fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/witnesses/M05/`): manifest sha256 4047689e…f34, sitemap sha256 3d53f4dd…32e; `sitemapUrl` and `loc` both `https://[2001:db8::1]/…`.

Commands run (cwd = witness dir):
`timeout 60 python3 -B /fast/scratch/hyaku/kake-r39a3w1/shared/reference.py --manifest manifest.json` → exit 0:
`{"version": 1, "verdict": "clean", "checks": [{"id": "w", "status": "clean", "error": null, "findings": []}]}`
`timeout 60 python3 -B /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M05.py --manifest manifest.json` → exit 1:
`{"version": 1, "verdict": "failed-policy", "checks": [{"id": "w", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 1}]}]}`
Both reproduce `reference_output`/`mutant_output` in mutants.json byte-for-byte.

Sentence 22: "A `loc` must be an absolute URL whose scheme is `http` or `https` (case-insensitive) and whose host is non-empty; otherwise `loc_not_absolute`, and rule (h) is skipped for that entry."
Reasoning: `https://[2001:db8::1]/a` is an absolute https URL; under the ordinary URL grammar the contract presupposes (sentence 4's "absolute http/https URL with a host" applies the same notion to `sitemapUrl`, which here is also bracketed IPv6), `[2001:db8::1]` is a non-empty host — RFC 3986 `IP-literal`. Nothing in sentences 1–34 forbids IPv6 hosts or narrows "host" to exclude them, and no other sentence attaches a finding to this file (scheme/host/port equal under sentence 24; path scope satisfied under 25). The contract therefore decides the witness as `clean`; the reference produces that, the mutant emits `loc_not_absolute`. Attacked statement (sentence 22): holds.

Sealed receipt `verification/a3/w1a3-MutUrlAuthority__M05.json`: met=true, passed 24/24, toolSha256 matches — the key did not expose this defect, so the mutation survives the counter while still being a real contract break (kill-rule (1) evidence stands; the counter's met flag is a control property, not a kill verdict).

Residual risk: I did not probe other inputs (e.g. `userinfo` hosts, where `:` never lands in `hostname` anyway; port-bearing IPv6 adds a `:port` outside `hostname`), so "exactly one behavioral divergence = IPv6-literal hosts" is supported by the one-line diff, not by an exhaustive sweep. No tools installed; pacman untouched.
