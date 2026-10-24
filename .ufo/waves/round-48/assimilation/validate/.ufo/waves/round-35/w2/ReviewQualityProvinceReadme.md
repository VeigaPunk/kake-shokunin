# ReviewQualityProvinceReadme — findings

Seat: KakeR35.ReviewQualityProvinceReadme. Attacks the round-35 sections of
QUALITY.md ("Round-35 criteria"), PROVINCE.md and corpus/README.md, at lane HEAD
7deacc4629c1d05a34fb919d8095e99efc7b712f. Work in sandbox clone
/fast/scratch/hyaku/kake-r35/w2/ReviewQualityProvinceReadme/clone (checked out
at 7deacc46; retained bundles fetched from the lane). No tools installed.

## 1. QUALITY (a) numbers vs receipts — all match
Every number quoted in corpus/QUALITY.md:703-739 matches
.ufo/waves/round-35/verification/control-v2-*.json + matching .exit:
- C1 constant clean passed 7/24 (target 22, exit 1), lookup (dcef39b5) 7,
  base-tool (16a6b8b8) 14, declaration (81d9fd74) 14. ✓
- C2 junk 0/12, keyword 3, transcript 8 (target 9, exit 1), transcript
  copiedShare 0.9951; critic zwsp-hiddenrows 8, dilute-comment 8, reworded 6. ✓
- Counter sha256 named at declaration (c4d58dae…) = sha256 of sealed_count.py at
  81d9fd74 (checked via `git show 81d9fd74:.ufo/waves/round-35/sealed_count.py | sha256sum`).
- Sealed key files' sha256 at reveal commit 4c6be2bd match C1_KEY_SHA256
  (a861dccd…) and C2_KEY_SHA256 (111bceea…) pins. ✓

## 2. Commands named in QUALITY run as written at 7deacc46 (with bundles)
- `python3 -B .ufo/waves/round-35/criteria/registry_row_check.py --repo . --rev 318561ef`
  → exit 1 listing scripts/link_preview_audit.py (receipt
  criterion-registry-row-at-318561ef.txt identical); `--rev fd0d53b2` → exit 0. ✓
- `prebuild_leak_check.py` c2 pair → exit 1 ("pre-build target published");
  c1 pair → exit 0 (receipts identical). ✓
- `control_description_check.py` r34 row4 → exit 1; r35 correction
  (--doc-rev bc0304de, anchor 'Correction of `dcef39b5`') → exit 0. ✓
- `git merge-base --is-ancestor 81d9fd74… 318561ef…` → 0; with first build
  commit b1cbbc39 → 0 (b1cbbc39 is the first build commit after the controls;
  git log 318561ef..HEAD shows bd14096a, b1cbbc39, 95abec21, 4c6be2bd…). ✓
- `sealed_count.py c1 --revision 5f767534… --key-revision 4c6be2bd` → exit 1,
  passed 7/24; `c2 --revision ae9fb361…` → exit 1, 8/12 probes, copiedShare
  0.9951 — reproduce the quoted "Observed from the committed receipts". ✓
- Limitation: these control revisions are NOT reachable from HEAD alone; the
  commands exit 2 "revision does not resolve" until the retained
  r35-control-*.bundle files are fetched (QUALITY:720 documents this
  prerequisite but names no fetch command). With the bundles fetched, all
  reruns match receipts.
- Seal behavior: `sealed_count.py c1 --revision 4c6be2bd --key-revision
  4c6be2bd` → exit 2 "key visible at the measured revision", zero mutation. ✓

## 3. Entry vs docs statements (freshness) — consistent, with two nits
Re-ran `sealed_count.py c2 --revision 95abec21 --key-revision 4c6be2bd`:
met true, 12/12 probes, 1388 words, copiedShare 0.0, goodCites 8
(S078-S080, S082-S086) — matches the context's C2 claim.
PROVINCE.md:202-295 and corpus/README.md:329-360 statements check out:
S078-S085 opened 22:00:48Z-22:02:20Z with one GET each (receipts.json timestamps
match; S006 22:02:19Z, S081/S084/S085 22:02:20Z); S081 rejected secondary;
S084/S085 body-text-only with no headers/TLS/redirect chain recorded (receipts
hold status/finalUrl/body/text sha256 only); S006 re-open used-by change landed
(SOURCES.md:14); SOURCES round-35 bounded question counts 11 identified/11
screened, 10 new rows (S078-S087: 8 mined, 2 rejected) ✓; report-35 census
claims match w1/ScoutDs4ccWellKnown.md (no .well-known, no security.txt, no
_config.yml, root .nojekyll, single pages.yml pinned upload-pages-artifact@v3
with include-hidden-files unset) ✓; ten-host census claim matches
w1/ScoutSecurityTxtCensus.md ✓.
Nits (low):
- corpus/knowledge/security-txt-publishing.md:8 "counter:" line still documents
  C2 v1 size condition ("≤ 1500 words"); the landed counter is v2
  (sealed_count.py:21-31: "at most 2200 words, counted as [a-z0-9]+ runs").
  Stale contract in the entry header; entry passes either way (1388 words).
- PROVINCE.md:208-215 and corpus/README.md:333-343 grounding lists omit S086,
  which the landed entry uses for the .nojekyll claim (entry lines 83-85, 92;
  SOURCES S086 used-by contains the entry). Incomplete, not false (no "only"
  wording). Also "one public GET each" is technically off for S083: receipt url
  = …well-known-uris.xhtml vs finalUrl = …well-known-uris, so that one fetch
  followed a redirect (urllib follows redirects); all other rows single-GET.

## 4. Cross-domain bleed — none found
Round-35 sections of all three docs keep vulnerability handling (report intake,
triage, remediation, disclosure, bounty, policy) out; no owned-site action is
instructed (writing/editing/deploying security.txt explicitly operator-owned);
entry header states "no request to an operator-owned host" and grep found no
owned-host URL (ds4cc.com/veigapunk.github.io/kimi.*/onrender) in the entry,
QUALITY round-35 criteria, or round-35 sections of PROVINCE/README. Open items
listed in PROVINCE are questions, not directives.

## Residual risk / not verified
- Did not byte-compare w1/ScribeProvinceReadme.md draft vs landed prose (out of
  scope). Did not re-run c1/c2 measured-run receipts (c1-at-*.json etc.) beyond
  the control/entry runs above; those belong to other seats.
- The QUALITY check block's placeholder commands (<first build commit>,
  <reveal commit>) were instantiated with the L1's actual values (b1cbbc39,
  4c6be2bd); the literal placeholders cannot run as printed.
