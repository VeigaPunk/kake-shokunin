# ResidHarmRerun — harm rerun at tip b9bf1a39 (Kake R41 residual)

All commands run from sandbox /fast/scratch/hyaku/kake-r41resid/ResidHarmRerun/ on copies; the lane repo
was only read (git show/log/diff/cat-file), plus this report file. No installs were needed (python3 3.14.8,
jq→jaq 3.1.1, git 2.56.0 preinstalled).

Tool bytes reviewed (sha256):
- final `scripts/sitemap_audit.py` at tip: `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`
- base tool (git 8eb121c8): `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e`
- first-build tool (git eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6): `0b485431d96268d46c8dc9052eec92520248a03989896bd83f4521f15f13edbf`
- `scripts/sitemap_audit_selftest.py` at tip: `18752057c8b0f7cb1b8567e8fff01be79faae0235b78201f344e7ec5c6e01bf8` (= SCORECARD's `18752057…01bf8`)

## Checked statements — commands and exit codes

1. Selftest, final tool: `python3 -B sitemap_audit_selftest.py --tool tools/final_tool.py` (under
   `prlimit --as=4000000000 timeout 600`) → `PASS 225/225`, EXIT:0. **Holds** (expected PASS 225/225).
2. Selftest, base tool `4de35f8c…`: same command → `PASS 196/225`, EXIT:1; 29 FAIL lines, 0 of them
   non-`r41_`; my FAIL-name list is byte-identical to the lane record
   `.ufo/waves/round-41/verification/build3/selftest-final-on-base-8eb121c8.txt` (diff clean).
   **Holds** (expected 196/225, only `r41_*` red).
3. Selftest, first-build tool `0b485431…`: same command → `PASS 219/225`, EXIT:1; the only failures are
   `r41_{loc,manifest_url}_ipv6_literal_{tab,lf,cr}` (exactly 6). **Holds** (expected 219/225).
4. Real run from sandbox copy of `.ufo/waves/round-41/realrun/` (sha256sum -c SHA256SUMS → all OK):
   `<tool> --manifest in/manifest.json > out-*.raw` → final EXIT:1, base EXIT:1 (expect findings exit;
   lane `build3/realrun-build3.exit` = `exit=1`); `jq -S . out-final.raw | sha256sum` = 
   `fd985a41867ed31b02ab03797562a1f01969aa3fc01c293eda145c2a7a4bc8a5`, base identical. **Holds**
   (expected `fd985a41…8a5`). Bonus: `cmp out-final.raw build3/realrun-build3.json` → byte-identical;
   `cmp out-final.raw out-base.raw` → byte-identical (wave-2 "real run byte-equal" reconfirmed on base
   vs final, not only vs the round-40 record).
5. Harm scope: `git diff --stat 8eb121c8 b9bf1a39362ec7c7fe06d80cc4162aa8ca3bca8f -- . ':!.ufo'` → 8 files
   changed, 562 insertions(+), 2 deletions(-): LOG.md, SCORECARD.md, SKILL.md, corpus/QUALITY.md,
   corpus/SOURCES.md, corpus/lessons/round-41.md, scripts/sitemap_audit.py,
   scripts/sitemap_audit_selftest.py. No file outside the round's declared set. **Holds.**
6. Deleted-line counts `git diff 8eb121c8 b9bf1a39… -- <f> | grep -c '^-[^-]'`: SCORECARD.md 0,
   LOG.md 0, corpus/SOURCES.md 0. **Holds** (append-only claim).

## Findings

- None at the reviewed tip. No defect found in the six statements above.

## Residual risk / verification gaps

- First-build tool bytes were recovered from git blob at commit `eae5ae2c7dc5…` (sha-verified
  `0b485431…`), not from a retained byte copy; if `eae5ae2c` were not the wave-2-attacked change the
  219/225 result would attach to different bytes — commit id matches SCORECARD/lesson, risk low.
- `jq` on this host is jaq 3.1.1; the recomputed hash equals the recorded `fd985a41…`, so the
  normalization is reproducible on the current host binary.
- The two-deletion count in the diff-stat is `scripts/sitemap_audit.py` line churn, not a record-file
  deletion (all three record files: 0 deleted lines).
