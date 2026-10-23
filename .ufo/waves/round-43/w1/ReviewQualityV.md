DEFECT: registry_count_check.py's census() is not the CORPUS.md contract-v1 census it claims to re-derive, and revision identity is never verified — 4 of 5 probe classes bypass it (exit 0) and canonically-honest claims false-positive.

Tool: .ufo/waves/round-43/registry_count_check.py sha256 35ca6d40f91215ab59b79ee9ccbf6e920bfc4067c3caf87173a86a6a87c535db (python3 -B, timeout 60, sandbox /fast/scratch/hyaku/kake-r43/ReviewQualityV/, probe git repo with commits A/E/D/T/F).
Canonical census: .ufo/round-20/resume/sources-census.txt (anchored `^\|[[:space:]]*S[0-9]{3,}`, NF!=13 defect counter, status vocabulary check). Checker's census() (lines 28-39) diverges on all three.

Receipts reproduce (command: `python3 -B .ufo/waves/round-43/registry_count_check.py --root <lane> --claims <claims>`):
- r42 claims: exit 1, output byte-identical to freeze/registry-count-r42-check.txt — holds.
- r43 claims: exit 0, byte-identical to registry-count-r43-check.txt — holds.

Probes (each exit observed, output in sandbox out-*.txt):
- p1-swap (base/tip revs swapped, counts matching stated revs, deltas negated): exit 0 — BYPASS. Checker never verifies revisions are the intended or even distinct commits; "119 -> 128" passes equally as "128 -> 119".
- p1-samerev (base_rev == tip_rev, deltas 0): exit 0 — BYPASS. A zero-change claim greens.
- p2a leading-space row `   | S003 ...` (commit 9804597a):
  - honest canonical claims (tip rows 2): exit 1 ("tip.rows: stated 2, re-derived 3") — caught, but the checker's derived count contradicts the census (S003 invisible to `^\|`; checker counts it because split+strip discards the anchor).
  - checker-consistent claims (rows 3, mined +1): exit 0 — BYPASS. A row the census never sees can be claimed as a mined row.
- p2b extra trailing empty cell (commit 95a45ccc):
  - honest canonical claims (tip rows 3, queued 1; census counts the NF=14 row and flags it as a defect): exit 1 ("tip.queued: stated 1, re-derived 0") — caught.
  - checker-consistent claims (tip rows 2, deltas 0): exit 0 — BYPASS. `len(cells)==13` silently drops a row the census counts; claims asserting the row never existed green.
- p3 status typo `mend` (commit 4ec80c6d):
  - claims matching post-typo numbers (rows 3, mined 1): exit 0 — BYPASS. Status vocabulary (queued|mined|rejected) is never validated; a defect the canonical census prints ("status S005 mend") is invisible.
  - claims with pre-typo mined 2: exit 1 — only caught because the claims are also wrong; blamed on the count, never on the typo.
- p5 two-digit ID `S12` (commit 0e95c592): claims rows 3, mined 2: exit 0 — BYPASS. `isdigit()` accepts S12; `S[0-9]{3,}` does not (census: rows 2).
- p4 nonexistent base_rev: exit 1 via unhandled CalledProcessError traceback (line 26->23). Exit 1 is indistinguishable from a clean mismatch and no mismatch is named, contrary to the docstring; malformed claims likewise KeyError-crash.

Soundness verdict: the checker validates only four integers per side plus deltas against its own divergent derivation. Exit 0 does not certify the census contract holds (defective registries and wrong/equal revisions pass); exit 1 does not certify stated counts are wrong (canonically-correct claims fail on probe-2a/2b shapes). For the r43 repair specifically the red/green receipts are real — actual SOURCES.md at 1ef7a0e9 and 5949e66f has no malformed rows — but as a reusable able-to-fail gate it is overclaimed: it can bless swaps, no-ops, unseen rows, dropped rows, non-rows and invalid statuses.

No installs needed. All probe processes exited; probe repo lives in /fast/scratch/hyaku/kake-r43/ReviewQualityV/probe-repo.
