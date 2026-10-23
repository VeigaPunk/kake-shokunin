# MutSelftestStructure — r41-falsify
Axes: operability (fixture discrimination, measured); freshness (not assessed; offline only).
Checked eight isolated structural mutants against the same unchanged 198 fixtures. Result: five killed, three survived, zero inconclusive; one survivor is guarded downstream rather than a demonstrated behavioral defect.
Sandbox/cwd: `/fast/scratch/hyaku/kake-r41w2/MutSelftestStructure` (called `$S` below). Lane build bytes matched the assigned SHA before copying; no lane source/index/state changed.
Expected detector: pristine/restored `PASS 198/198`, exit 0; a detected behavioral regression gives fixture FAIL lines, fewer passes, exit 1. A printed PASS count alone is not suite success.

## Survivors first; actual mutated outputs
Line references below are to `scripts/sitemap_audit.py`; every change existed only in its named sandbox copy.
| Verdict | Copy ID; change | Actual selftest line | Exit | Mutant SHA-256 (before = after detector) |
|---|---|---|---|---|
| SURVIVED | m01_pct_one_hex; :75 percent digits `{2}` → `{1}` | `PASS 198/198` | 0 | `941222b35d0497e3e676cb29bfea97522ca1ed3092463adc8ebe398adf4c9bdb` |
| SURVIVED | m05_query_hash; :84 query `[/?]` → `[/?#]` | `PASS 198/198` | 0 | `12a0f3e6bb4c7f7da39c4763504ef93eb7c359d7d5abb0e456e3f0fc77add550` |
| SURVIVED | m03_empty_reg_name; :81 reg-name `+` → `*` | `PASS 198/198` | 0 | `b4bc842a1fc89217e47a7a25d77121be828fac34f171a3de5cbc136c5ada364b` |
| KILLED | m02_no_end_anchor; :85 remove URI regex end anchor `\Z` | `PASS 176/198` | 1 | `458b5e179e4ce0f2781d32d005c1f5020a3d2d632a91c5561bfccc6c6efc1902` |
| KILLED | m04_userinfo_at; :79 add `@` to userinfo repertoire | `PASS 197/198` | 1 | `5c53909535d8423aa1f72fc37ec969c41c236294303ccf65f313f2e4b5c17ce6` |
| KILLED | m06_strip_before_regex; :92 match `value.strip()` instead of `value` | `PASS 196/198` | 1 | `55a2f7b62d351696e4a3bc023a5e0381aceb01c52927ec6956004b8eaad724d4` |
| KILLED | m07_skip_sitemapUrl; :89/:92 optional grammar guard, disabled only at :382 | `PASS 188/198` | 1 | `735905f33b748ec623ae63a9e80075d017bbc7f5f81f8b6e41c175aade4116ae` |
| KILLED | m08_skip_loc; :89/:92 optional grammar guard, disabled only at :308 | `PASS 182/198` | 1 | `4eb9d035860842e56055d0b5893a7dd5803405413d60df826637e1a820f54c0d` |

## Findings and checked statements
- **Medium — percent-triplet regression detection: wrong.** `scripts/sitemap_audit_selftest.py:919-941` misses the one-hex mutant. Supplementary CLI witness `http://example.com/a%2`: pristine/restored exit 1, `failed-policy`, `loc_not_absolute`; mutated exit 0, `clean`, empty findings. These witness cases did not alter or count toward the 198-fixture detector.
- **Medium — query-delimiter regression detection: wrong.** `scripts/sitemap_audit_selftest.py:909-913` catches a second hash in a fragment without a query, but not this mutant. Witness `http://example.com/a?x#y#z`: pristine/restored exit 1, `failed-policy`, `loc_not_absolute`; mutated exit 0, `clean`, empty findings.
- **Info — empty-host rejection on the checked witness: holds.** `scripts/sitemap_audit.py:99-101` still rejects `http:///a` in all three stages (exit 1, `loc_not_absolute`). [INFERENCE] M03 is behaviorally equivalent because the unchanged downstream host guard rejects the newly admitted empty reg-name; its survival is not a demonstrated coverage defect.
- **Detection of the other five requested changes: holds.** M02 has 22 failing fixtures; M04 fails `r41_loc_userinfo_second_at`; M06 fails `r40_u_sitemapurl_leading_space` and `r40_u_sitemapurl_more_leading_unit_separator`; M07 has 10 failures including `r41_manifest_url_c0_interior`; M08 has 16 including `r41_loc_bad_percent_triplet`.
- **Build fixture-pass harm statement: holds.** Every one of the eight pristine runs and eight restored runs returned exit 0, exactly `PASS 198/198`, no FAIL lines, empty stderr. No baseline failure was counted as a kill. This probe makes no general C1 or round verdict and changes no contract.

## Commands, receipts, restoration
Exact outer commands (all exit 0; the mutated harness records expected detector exits 0/1 separately above):
```sh
timeout -k 5s 30s prlimit --as=4000000000 -- python3 -B /fast/scratch/hyaku/kake-r41w2/MutSelftestStructure/probe_runner.py init
timeout -k 5s 900s prlimit --as=4000000000 -- python3 -B /fast/scratch/hyaku/kake-r41w2/MutSelftestStructure/probe_runner.py pristine
timeout -k 5s 900s prlimit --as=4000000000 -- python3 -B /fast/scratch/hyaku/kake-r41w2/MutSelftestStructure/probe_runner.py mutated
timeout -k 5s 900s prlimit --as=4000000000 -- python3 -B /fast/scratch/hyaku/kake-r41w2/MutSelftestStructure/probe_runner.py restored
```
For each ID and each phase the exact detector was `timeout -k 2s 240s prlimit --as=4000000000 -- /usr/bin/python3 -B $S/sitemap_audit_selftest.py --tool $S/<ID>.py`; cwd `$S`, `TMPDIR=$S/tmp/<phase>/<ID>`, `PYTHONDONTWRITEBYTECODE=1`. Fully expanded commands, individual exits, failures and before/after hashes are retained in `$S/{pristine,mutated,restored}.json`; actual stdout/stderr in `$S/<phase>-<ID>.{stdout,stderr}.log`. Exact source deltas: `$S/mutations.patch`.
Supplementary commands: `timeout -k 2s 60s prlimit --as=4000000000 -- python3 -B $S/witness_probe.py <phase>` for `pristine`, `mutated`, `restored` (each outer exit 0); child commands/output/individual exits retained in `$S/witness-<phase>.json`.
Restoration executed `timeout 15s prlimit --as=4000000000 -- cp -- pristine.py <ID>.py` for all eight IDs, joined by `&&` in numeric order, cwd `$S` (exit 0), before the restored detector runs.
Pristine SHA-256 and every restored copy's before/after-detector SHA-256: `0b485431d96268d46c8dc9052eec92520248a03989896bd83f4521f15f13edbf`. All eight mutated hashes differed; exact original bytes were restored in all eight copies.
Unchanged suite SHA-256: `d8d2ba6cf3d8721e558cac42f44784101aaaddab8571a5364b8808cd4977c16d`. Runtime: Python 3.14.8. No tool installations/updates; no network requests.
Bounds/cleanup: two concurrent suite workers; 4,000,000,000-byte AS caps; 64 MiB per-file cap in fixture runner; temporary fixture roots confined to sandbox and removed per case. Child process groups are killed in `finally` and waited; all launched runs completed, no retained services/process trees.
