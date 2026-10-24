# CtlSkipE — partial repair that skips class E (r40 w1 control)

**Result: does NOT meet the predicate. Best skip-E tool = 25/30 (E 4/9, U 13/13, R 8/8), selftest 150/150, `met: false`. Caught by E1–E5 only (exit 0 instead of 1). The counter has full power to reject this skip; no legal skip-E variant reached 30.**

## Tools (sandbox `/fast/scratch/hyaku/kake-r40w1/CtlSkipE/`)

| tool | sha256 | what it is / declared work skipped |
|---|---|---|
| `base.py` | `6d86c8cef78e36d372f7277096ec163cc8f1e919fa66702ad24e5e32f9a240ec` | base `f043c72:scripts/sitemap_audit.py` (no repair; equals SCORECARD's listed base `6d86c8ce…`) |
| `v1_skipE.py` | `c61e5811dd4c339cfc84c0f6d1f579150dec774eea03064819a34ed5c5cd6e3b` | **the control**: base + U hunk (`_parse_url` guard) + R hunk (duplicate before type-check), E path untouched. Skips the whole class-E repair — caught by **E1–E5** |
| `v2_proxy.py` | `344cb63f12c2fe5f48e79d4f745c68da06adf77ff0eefc8d3d781b673f3f5bc9` | v1 + pre-decode raw `b"\x00"` sniff (a SCORECARD-named proxy). Skips the declared decode→U+0000 reading — caught by **E8, E9** |
| `v3_declonly.py` | `f832870b7ec5aaa8f875fc0ff5ff2da5cfcf1a54bacb33b8436ac87bb8b2c021` | v1 with the E check gated on "declaration present" (SCORECARD sub-shape). Behaviourally = v1 — caught by **E1–E5** |
| `ref_fix.py` (read-only, /fast/scratch/hyaku/kake-r40/shared) | `03a8fba4930ad7628a569e7aa30b3ece728fbb6eb3fa4ac7c9a78dfbeb07b22b` | reference (matches SCORECARD's listed reference sha); scored as environment check |

`diff -u v1_skipE.py ref_fix.py` = exactly the 2-line E hunk (`ref_fix.py:189-190`). U/R hunks are byte-identical to the reference (`ref_fix.py:70-71`, `:337-343`).

## Counter receipts (`/fast/scratch/hyaku/kake-r40w1/CtlSkipE/`)

| receipt | label | seed | passed | byClass | selftest | met | exit |
|---|---|---|---|---|---|---|---|
| `receipt-base.json` | CtlSkipE-base | 4242 | 10 | E 4/9, U 3/13, R 3/8 | PASS 150/150 | false | 1 |
| `receipt-v1-s4242.json` | CtlSkipE | 4242 | 25 | E 4/9, U 13/13, R 8/8 | PASS 150/150 | false | 1 |
| `receipt-v1-s777.json` | CtlSkipE | 777 | 25 | E 4/9, U 13/13, R 8/8 | PASS 150/150 | false | 1 |
| `receipt-v1-s40001.json` | CtlSkipE-s40001 | 40001 | 25 | E 4/9, U 13/13, R 8/8 | PASS 150/150 | false | 1 |
| `receipt-v2-s4242.json` | CtlSkipE-proxy | 4242 | 28 | E 7/9, U 13/13, R 8/8 | PASS 150/150 | false | 1 |
| `receipt-v3-s4242.json` | CtlSkipE-declonly | 4242 | 25 | E 4/9, U 13/13, R 8/8 | PASS 150/150 | false | 1 |
| `receipt-ref-s4242.json` | CtlSkipE-ref | 4242 | 30 | E 9/9, U 13/13, R 8/8 | PASS 150/150 | **true** | 0 |

## Exact commands (all exit codes as shown above)

```
timeout 1200 prlimit --as=4000000000 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-40/c1_count.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file <tool> --label <L> --seed <N> --out <receipt>
```
V1 built by exact string replacement from `base.py`; env: Python 3.14.8, counter sha256 `6d73b8f498a29a5a86c9a7f1ce5d87cd135c40f1b634d869d14659cc10bee8d8` (= SCORECARD).

## Findings

1. **E1–E5 fail because pyexpat 3.14.8 silently drops U+0000**, not because the base "decodes UTF-16 as UTF-8 and then reports". Measured: `ElementTree.fromstring` on E1's decoded text yields a valid `urlset` whose loc text is `http://whost.example/dd/pabcd` with the NULs gone; base `:182` decode → `:187` declared → `:193` parse → clean. Every E1–E5 failure is `exit 0 != 1`, i.e. the tool says *clean* for a UTF-16 document. Nothing in the tool observes U+0000 except the reference's `"\x00" in text` check (`ref_fix.py:189-190`), so class E is unreachable by any non-E work.
2. **The declaration-present sub-shape is not expressible on decoded text** (v3): the XML declaration itself is NUL-interleaved (`<\x00?\x00x\x00m\x00l\x00`), so `_declared_encoding` returns None on E1–E5 and the gated check never fires; v3 scores exactly like v1.
3. **E8/E9 are the witnesses that separate the proxy from the declared reading**: a pre-decode `b"\x00"` sniff (v2) turns E8/E9 into `xml_malformed` where the contract keeps `encoding_invalid` ("with a BOM the bytes are not UTF-8"), scoring 28/30. A post-decode U+0000 check passes 30/30.
4. **The regression half has no class-E power**: `sitemap_audit_selftest.py@f171c58` passes 150/150 for base (10/30) and for every skip-E variant. Only the 30 witnesses gate E.
5. Counter reproducibility: base 10/30 and V1 25/30 at seeds 4242/777/40001; base byClass matches SCORECARD's pre-run receipt (10, E 4/9, U 3/13, R 3/8).

## Attacked statements

- "The counter rejects a tool that skips class E" — **holds**: 25/30 on three seeds, 5 witnesses margin, `met: false`.
- "A control that skips E could still meet by proxy" — **wrong for the pre-decode sniff** (E8/E9 catch it at 28/30); the SCORECARD's proxy class is genuinely separated.
- "The base fails E because the decoded text carries U+0000 which is not an XML Char, so sentence 8 gives `xml_malformed`" — **holds as a contract reading, overstated as a mechanism**: the shipped parser does not enforce it (finding 1); the repair must be explicit. No change to the expected outcome.
- "U and R repairs are independent of E" — **holds**: U 13/13 and R 8/8 across all three seeds with the E path untouched.

No installs or upgrades; no lane files touched; only the sandbox and this report were written.
