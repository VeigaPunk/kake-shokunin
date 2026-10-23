SURVIVED: 1 of 6 single-member scheme mutants (M5, default https port 443->80) passes counter v4 at 11/11 met=true while changing stdout on a legal manifest; the other 5 are KILLED. Survivor is a counter-coverage finding, not counter unsoundness and not a verdict on C1.

# MutBuildScheme — round 43 w1, build scheme handling (odd case / odd schemes / schemeless)

Baseline: `git -C <lane> show 020bc4574729ed674299f6cab02faac1582d9464:scripts/sitemap_audit.py` (read-only) -> `/fast/scratch/hyaku/kake-r43/MutBuildScheme/build.py`, sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` (matches tasking; re-hashed unchanged after scoring).
Reference: ref41 rev 1ef7a0e9 -> `ref41.py` sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` (matches counter REF41_SHA).
Each mutant = one exact one-occurrence substitution of build.py (assert count == 1), scored once with:
`timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-43/c43_count_v4.py --root <lane> --tool-file <mutant> --label MutBuildScheme-<M> --out <receipt>` (no --seed). exit 1 = not met / 0 = met.

# Per mutant (receipt = /fast/scratch/hyaku/kake-r43/MutBuildScheme/receipts/<name>.json)
| mutant | sha256 | one-member change | equalRuns | met | verdict |
|---|---|---|---|---|---|
| M1_scheme_add_ftp | 8bcb429aa16798cbe9354ae7598f2bfc5e016013003f0ee491ff0d872c9a4ac5 | build.py:295 `("http","https")` -> `("http","https","ftp")` (class member) | 9/11, failed A,D | false | KILLED |
| M2_scheme_drop_https | 48d7c4b9182b5e65d0815c01feb0bd5fd66e1c3d8178fac38a56230d592a9ec9 | build.py:295 -> `("http",)` (class member) | 0/11 | false | KILLED |
| M3_scheme_drop_http | 3d272250b705a7b0269b289605cbfe132f048733ddbce853c29ee8131da08df2 | build.py:295 -> `("https",)` (class member) | 1/11, failed all but T2 | false | KILLED |
| M4_head_boundary_lower | 286c81af822268b3a5c5d3725ff0ac2e7f956be14e2ad0f8452d72a380f3c31b | build.py:221 drop `0x61 <= head <= 0x7A` from the scheme-head range (boundary) | 0/11 | false | KILLED |
| M5_default_port_https80 | 0fc6091351c1e080b90df1f96ef2558d9f5ada2dce473109d0fe805d07fe5889 | build.py:304 `else 443` -> `else 80` (branch/default value) | 11/11 | **true** | **SURVIVED** |
| M6_scheme_prefix | 33b8f2206e64ac69254fc2beef95774da852b78f20ee862e791efaacddeca8a1 | build.py:295 `not in ("http","https")` -> `not scheme.startswith("http")` (branch condition) | 9/11, failed A,D | false | KILLED |
M5 ratios T1..T5 = 1.042/1.179/1.274/1.254/1.221 (<= 2.0); seeds recorded in receipts (M5 seed 262137913446005; M1 228965333964004; M6 64916933881399).

# Survivor witness (M5) — reproduced under the counter's own invocation shape
`witness/m.json` = `{"version":1,"checks":[{"id":"w1","file":"s.xml","sitemapUrl":"https://h.example:443/sitemap.xml"}]}`, `s.xml` holds one loc `https://h.example/a`.
ref41.py exit 0 clean; build.py exit 0 clean (so build == ref41 here); M5 exit 1 `{"code":"loc_out_of_scope","entry":1}`.
Counter gap (why it survives): layout_cases derives a group's sitemapUrl from its first value (`c43_count_v4.py:725`, same explicit port) or from a random different host; sitemapUrl units point at one shared file whose only loc has a different host (`c43_count_v4.py:549,705`). layout_f likewise pairs long-port sitemapUrls with a shared clean loc of another host (`c43_count_v4.py:535,549`). No generated run pairs an explicit-default-port sitemapUrl (:443 or :80) with a portless loc on the same host, so default-port normalization is never exercised.

# Findings
- Holds: counter v4 kills scheme-set, scheme-case and scheme-prefix defects (M1-M4, M6; 0-9 of 11 runs unequal). Odd schemes are generated only in `make_url` at `c43_count_v4.py:173` (ODD_SCHEMES `:101`), hence M1/M6 fail only runs A and D — the "run F" repetition classes add no odd-scheme coverage. This is consistent with the frozen counter text; it is not an overstatement of it.
- Holds: build's default-port normalization is behavior-bearing: ref41 treats explicit `:443` equal to the https default (witness above, ref clean), so build.py:304 encodes a real contract term. Coverage of that term by c43_count_v4.py: absent (M5 met).
- Holds: reference pins agree (ref41 sha == REF41_SHA; base40 untouched); counter exit 2 never occurred; all 6 receipts parse and carry toolSha256 of the scored bytes.
- Not claimed: no soundness defect (do-nothing/junk) and no pre-freeze score evidence was examined in this probe.

# Mutants vs ref41 (local differential, non-sandbox pre-check)
All 6 differ from ref41 on the crafted manifest (`box/m.json`): M1 ftp->loc_out_of_scope (ref loc_not_absolute); M2/M4 check_invalid exit 2 (ref clean); M3 check_invalid (ref clean on http); M5 loc_out_of_scope (ref clean); M6 loc_out_of_scope (ref loc_not_absolute).

# Restoration / scope evidence
No lane file modified; only this report written inside the lane. All mutant/scoring bytes live under /fast/scratch/hyaku/kake-r43/MutBuildScheme/ (build.py unchanged sha256 914ebdee...cd021). All spawned processes exited (no bwrap from this seat remains). No tools installed or upgraded.
