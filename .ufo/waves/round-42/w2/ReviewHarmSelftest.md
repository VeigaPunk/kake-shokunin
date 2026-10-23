H1/H5 HOLD (operability) — no actionable finding; fresh reruns and fixture comparisons pass.

## Findings
- None. H1's declared fixture behavior and H5's Python 3.10.22 requirement hold for the tested build `scripts/sitemap_audit.py` (sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`) and tip41 `/fast/scratch/hyaku/kake-r42/shared/tip41.py` (sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`). Selftest sha256: `bebd834bc43d683950a2891676c5fc1c300395a524ca919f02f290f5dabcda22`.

## Verification
Host `python3` = 3.14.8; the specified uv interpreter = Python 3.10.22. All commands used `timeout 900` and `prlimit --as=8000000000`.

- `timeout 900 prlimit --as=8000000000 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit_selftest.py --tool /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit.py` → exit 0, PASS 235/235.
- `timeout 900 prlimit --as=8000000000 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit_selftest.py --tool /fast/scratch/hyaku/kake-r42/shared/tip41.py` → exit 0, PASS 235/235.
- `timeout 900 prlimit --as=8000000000 -- ~/.local/share/uv/python/cpython-3.10.22-linux-x86_64-gnu/bin/python3.10 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit_selftest.py --tool /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit.py` → exit 0, PASS 235/235.
- `timeout 900 prlimit --as=8000000000 -- ~/.local/share/uv/python/cpython-3.10.22-linux-x86_64-gnu/bin/python3.10 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit_selftest.py --tool /fast/scratch/hyaku/kake-r42/shared/tip41.py` → exit 0, PASS 235/235.

- Per-fixture differential: compared build vs tip41 return code, stdout bytes, and stderr bytes for all 42 `r41_*` plus all 10 `r42_*` fixtures.
- `timeout 900 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r42w2/KakeR42.ReviewHarmSelftest/compare_fixtures.py /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit_selftest.py /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit.py /fast/scratch/hyaku/kake-r42/shared/tip41.py /fast/scratch/hyaku/kake-r42w2/KakeR42.ReviewHarmSelftest` → exit 0, 52 fixtures, 0 output differences, 0 expectation failures.
- `timeout 900 prlimit --as=8000000000 -- ~/.local/share/uv/python/cpython-3.10.22-linux-x86_64-gnu/bin/python3.10 -B /fast/scratch/hyaku/kake-r42w2/KakeR42.ReviewHarmSelftest/compare_fixtures.py /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit_selftest.py /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit.py /fast/scratch/hyaku/kake-r42/shared/tip41.py /fast/scratch/hyaku/kake-r42w2/KakeR42.ReviewHarmSelftest` → exit 0, 52 fixtures, 0 output differences, 0 expectation failures.
- Comparison helper sha256 `87b589ac8f5f347a71f951b245c22274ee22242c163b0c6a50c8df3830494484`.

The ten `r42_*` outcomes match on both tools and both runtimes (all pass their fixture expectations; zero per-fixture differences): `r42_loc_zone_id_eth0`, `r42_loc_zone_id_pct25_eth0` clean/0; `r42_loc_zone_id_non_ascii`, `r42_loc_zone_id_pipe` failed-policy/1; `r42_sitemapUrl_zone_id_eth0`, `r42_sitemapUrl_zone_id_pct25_eth0` clean/0; `r42_sitemapUrl_zone_id_non_ascii`, `r42_sitemapUrl_zone_id_pipe` check_invalid/2; `r42_loc_long_2047_trailing_percent` failed-policy/1; `r42_loc_long_2047_valid` clean/0. All 42 `r41_*` outputs/exits are unchanged between build and tip41 on both interpreters.

Existing target receipts `verification/harm/selftest-{build,tip41}-py310.txt` and `selftest-{build,tip41-235}-py314.txt` each state PASS 235/235, exit=0; fresh runs above reproduce them. Fixture declarations: `scripts/sitemap_audit_selftest.py:991-1036`; suite result assertions: `:1129-1197`. H1/H5 contract and L1 statements: `SCORECARD.md:2976-2982,3084-3107` — holds.

## Residual risk and verification gaps
- Residual risk: this validates the 235 fixture expectations and exact build-vs-tip41 equality for the 52 named `r41_*`/`r42_*` fixtures, not all possible URL values.
- LSP device unavailable (`read xd://lsp` returned “No such tool”; mounted devices were `ast_edit`, `debug`). No caller/definition/diagnostics checks were available; literal fixture/source references above are not semantic LSP proof.
- No tools installed or updated.
