# ReviewQualityProvince — QUALITY round-37 (a)-(i), PROVINCE r37, README r37 vs evidence
Seat: KakeR37.ReviewQualityProvince. Clone `/fast/scratch/hyaku/kake-r37w2/ReviewQualityProvince/clone` @ `79d3c780`; TMPDIR in sandbox. No installs. No process left running. Lane HEAD is `a5ae028` (wave-1 reports, 12 s after the measured tip).

## Receipts rerun (in clone)
Copies of `criteria/receipts/run_{bare_id,control_tree,polarity}.sh` with `L=<clone>` and `C=<clone>/.ufo/waves/round-37/criteria/*.py`. `B` (fixtures) stays the wave-1 sandbox, read-only, snapshot + sha256 in `<sandbox>/fixtures-snapshot`, `fixtures.sha256`. Copies are in `<sandbox>/rerun/`.
- `timeout 600 bash run_bare_id.sh`: 0. Inner exits `0 1 0 0` = receipt.
- `run_control_tree.sh`: 0. Inner exits `0 1 1 1 1 1 1 0 0 0 0` = receipt.
- `run_polarity.sh`: 0. Inner exits `0 0 1 0 1 0` = receipt.
- `diff` of the outputs against the committed `criterion-*.txt`, after normalizing paths: 0 lines for all three (`rerun/diff_*.txt`). The committed check scripts have the same sha256 as the scripts that produced the receipts: `8b8fe47d`, `b592270e`, `7ebc5d67`.
- **Reproducibility defect (operability):** the receipt scripts hardcode `B=/fast/scratch/hyaku/kake-r37w1/ExecCriteriaRepairs` and `cd` into the live lane (`L=/home/…/kake-shokunin`), not a clone. The 9 fixtures they use are uncommitted (`git ls-files | rg <fixture names>` → exit 1). From the committed tree alone, the RED/GREEN-on-constructed-input runs cannot be reproduced once that sandbox is gone. The script headers also use different criterion letters than QUALITY: `run_bare_id.sh` says "(a)" for QUALITY (g), `run_control_tree.sh` says "(d) v2" for (f), and `run_polarity.sh` says "(f)" for (e).

## Per criterion
- **(a) holds.** `round-36-verifier-spotcheck.md:155-157` is routed defect 2. `round-36.md:80` is the row about two seats writing under `criteria/`. "No check yet" is honest; there is no receipt to run.
- **(b) wrong citation, otherwise holds.** `corpus/lessons/round-36.md:61-65` is S089 urljoin plus the "Real-input run" heading, not the key-v2 casefold loosening. That text is at `:141-142` (`CriticKeyV2Change` 24→26). `spotcheck:161-163` (defect 4) and `:73` (counter v1 + key v1 = 28/28) hold, and `verification/c1-counter-v1-keyv1-at-4d5b3d55.json` exists.
- **(c) grounding holds; the cited wording is overstated.** `spotcheck:158-160`, `round-36.md:134-143` (9/32 tool mutants, 5/6 new reference mutants), `SCORECARD.md:1780-1784` and `MutRefPass.md:3` (met 28/42) hold. The table runs M01 at `:11` to M42 at `:52`. Re-read of `verification/ablations/`: 34 ablations, 16 (c_star) to 24, and the reference scores 28. But `SCORECARD.md:1930` says "25 of 28 certifies the listed rules", and QUALITY (c) paraphrases it as "limits the claim to those listed rules". `MutRefPass.md` contradicts this:
  - M20 breaks the listed (d) tie rule ("allow wins equal-length ties") and still meets 25, at 26/28, although ablation `d_tie` scores 24.
  - M01/M02 break the (b) 512000 limit and score 28 (`b_limit` = 24).
  - M08 breaks (b) key case and scores 28 (`b_keycase` = 24).

  What 25/28 excludes is the 34 listed ablations, not the listed rules.
- **(d) holds.** `git cat-file -e <h>^{commit}` succeeds for 4d5b3d55, 3555f63f, 621fb528, 9dbc88bb, 424aa248, 202d625a, 4b089da6, ccc3b2b9, 528a6d02. bf9b2089 is missing from lane objects, and `git bundle list-heads .ufo/waves/round-36/retained/r36-l1-postfix-remeasure.bundle` → `bf9b2089… refs/heads/postfix`, so the bundle-only citation is correctly attributed. `hash_resolve_check.py` and `criterion-hash-resolve-r36-decl-at-3555f63f.txt` exist. `spotcheck:153-154` and `:23` hold.
- **(e) receipt reproduces; "replaces no check yet" is overstated.** `timeout 60 python3 -B .ufo/waves/round-37/criteria/polarity_check.py --key .ufo/waves/round-37/sealed/cases.json` → `ERROR: case 'c1' has no expect object`, exit 2. The check cannot read the round-37 key schema (`runs[].expect`), so the round-37 per-case promise has no receipt, although (e) itself says it "need[s] explicit evidence too". Label independence also has no receipt; the only evidence is the counter's id/file-name randomization (`SCORECARD.md:1785`). Ad-hoc count (not a receipt, script inline in this seat's log): every one of the 28 round-37 cases has at least one finding check and at least one hold check. f2/f4 pass only through the first `dupid`: 8 checks, 7 findings. So the promise is true in fact but has no committed check.
- **(f) receipt reproduces; the criterion is not met by v2 (overstated).** (f) rejects "a detached listing". v2 passes one:
  - A constructed `adv/report-detached.md` (an `ls -la` of `.` with no root) gets `WARN … names no root, so it cannot vouch for tree identity` and then `PASS … that name their trees`, exit 0. The PASS line contradicts the WARN.
  - The receipt's GREEN "key-free work dirs" set includes `ctl/MutRefPass.md` with the same WARN. That seat scored with `--key-file /fast/scratch/hyaku/kake-r37/private/cases.json` (`MutRefPass.md:7`), and `--pattern private/` still exits 0.
  - Every round-37 ctl GREEN lists only the seat's own work dir, under `/fast/scratch/hyaku/kake-r37/ctl/`, which sits beside `private/` (e.g. `CtlC1AllFalse.md:19,29`). That is the weak-reason pass already named in `round-36/w2/ReviewCriteriaChecks.md:40-44`.

  So "proves the control was built from the listed, key-free tree" is not shown for round 37. Grounding citations `spotcheck:170-171`, `ReviewCriteriaChecks.md:40-49` and `make_w1_spec.py:81-83` hold.
- **(g) holds for the stated receipts.** Residual weakness: the check is lexical. `adv/padonly.md` ("See S095 and S096 and also more words here to pad.") gets PASS, exit 0: any word of two or more letters counts as claim text, and one block credits every id in it. `oneword.md` and `bracket.md` → exit 1, as expected.
- **(h) holds.** `jq .met retained/controls/c2/c2-snapshot.json` → true. `ctl/CtlC2FixtureSets.md:12` shows snapshot killed 32, met true. The SCORECARD "Round 37 — control call" section is at `:1900`.
- **(i) unverifiable at the measured tip; holds at `a5ae028`.** `.ufo/waves/round-37/w1/` does not exist at `79d3c780` (`ls` of the round-37 dir shows no w1). `ReviewRoutedDisposition.md` first appears at `a5ae028`, where `:17` and `:61` state G2 (control sandboxes were siblings of the key). The statement about moving to `kake-r37w1` matches the `ExecCriteriaRepairs` sandbox path. The lesson row at `corpus/lessons/round-37.md:158` has the same dangling pointer at the tip.

## PROVINCE "Round-37 robots.txt frontier step" (`PROVINCE.md:297-305`)
1. Frontier move and per-check comparison (S011; S095; contract) — **holds**: `SCORECARD.md:1797-1812`.
2. "reads only the manifest and named robots files, writes nothing, uses no network" — **holds**: contract `:1800-1802`. Tool imports json/os/re/stat/sys/urlsplit only, and `os.open` is `O_RDONLY` at `scripts/robots_audit.py:341,365`.
3. blocked/exposed and the verdict order — **holds**: `:1810-1812`, `:1856-1857`.
4. Unknown records ignored; sitemap and extensions open (Lines; S012–S013) — **holds**: contract (b) `:1822-1823`. S012/S013 are the sitemap rows (`SOURCES.md:20-21`).
5. No live fetch, redirect, caching or crawler behavior (Limits) — **holds**: `:1791-1793`.
6. Boundary with tabi (Adjacent) — **holds**: `PROVINCE.md:34-35`.
7. The knowledge entry cites S011, S095, S096 with lane readings marked — **holds**: entry `:1` and "Lane reading" at `:23,31,35,41,43`. `bare_id_check` passes 3 ids.

## corpus/README "Coverage — round 37" (`corpus/README.md:362-370`)
- Table row — **overstated (minor)**: "compares the expected decision with RFC 9309 access rules". The contract fixes lane readings wherever RFC 9309 says SHOULD/MAY (`SCORECARD.md:1792-1793`) and treats every 3xx as `check_invalid` (`:1846-1849`). The PROVINCE wording "C1 contract" is accurate; the README row should say "the C1 contract's reading of RFC 9309".
- "reads local inputs only … cases are synthetic" — **holds**: Limits `:1791`. The sealed cases use example.com URLs.
- Open items and ignored records — **holds** (as in PROVINCE 4–5).
- tabi boundary — **holds**: `PROVINCE.md:34-35`.
- Knowledge entry pointer — **holds**: the file exists.

## Residual risk and verification gaps
- Not run: the receipts against the committed lane path. My rerun used a clone, plus fixtures read from the wave-1 sandbox. Fixture integrity rests on my sha256 snapshot, not on a committed pin.
- The (e) per-case count is a seat-local script, not a landed check. The (f) detached-listing result is one constructed report.
- Not reviewed: the measured-results and capability-row wording against (c), beyond the cited `SCORECARD.md:1924-1932` text.
