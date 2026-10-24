# Round 29 wave 2 - HeldOutCases (C2 tool on cases the author never saw)

Item attacked: `scripts/base_path_audit.py` at lane commit `7697990cbca20291f3b0367b8ff4220e93b38b03`,
sha256 `e32646159b652710be4053bbdb001c3d11929ef63b055b7f57545231ac6965aa`, read through the frozen
matrix interface text `.ufo/waves/round-29/c2-matrix.json` (sha256 `75c08f64...dbac2e84a`). Every
expected outcome below was written from the interface text before the tool was run; the same bytes
were then run and compared with the counter's own judge (`c2_matrix_count.judge`). P = the 8 wave-1
probes reused verbatim, Q and X = mine.
## Commands (TMPDIR inside the seat sandbox `/fast/scratch/hyaku/kake-r29/w2/HeldOutCases`)
- `git clone -q <lane> clone && git -C clone checkout -q 7697990` -> 0.
- `git -C <lane> show 7697990:scripts/base_path_audit.py > work/base_path_audit.py` -> 0.
- `python3 -B probes_heldout.py work/base_path_audit.py` -> 1; SUMMARY 17/21 agree.
- `python3 -B <w1>/CriticC2CounterGameable/probes.py <lane>/c2_matrix_count.py work/base_path_audit.py` -> 0; 7/8 probes, P3 detail `exit 1 != 0`.
- `python3 -B <lane>/.ufo/waves/round-29/c2_matrix_count.py --root <lane> --revision 7697990` -> 0; 30/30, constant gates 7/0/7 rejected, toolSha256 `e3264615`.
- `python3 -B mutate.py work/base_path_audit.py work probes_heldout.py` -> 0.
## Predicted versus observed
| probe | predicted | observed | agree |
|---|---|---|---|
| P1 div[href] | exit 0 clean | exit 0 clean | yes |
| P2 a[src] | exit 0 clean | exit 0 clean | yes |
| P3 http same host | exit 0 clean | exit 1 failed-policy, a[href]="http://o.github.io/other/" | NO |
| P4 other port :8443 | exit 0 clean | exit 0 clean | yes |
| P5 entity `&#47;x` | exit 1, a[href]="/x" | exit 1, a[href]="/x" | yes |
| P6 single quotes | exit 1, a[href]="/x" | exit 1, a[href]="/x" | yes |
| P7 unquoted | exit 1, a[href]="/x" | exit 1, a[href]="/x" | yes |
| P8 base without href | exit 0 clean | exit 0 clean | yes |
| Q1 form[action] absolute | exit 1, form[action] | exit 1, form[action] | yes |
| Q2 embed[src] | exit 1, embed[src]="/e.swf" | same | yes |
| Q3 srcset first candidate outside | exit 1, img[srcset]="/a.png" | same | yes |
| Q4 nested basePath without final slash | exit 0 clean | exit 0 clean | yes |
| Q5 whitespace-only src | exit 0 clean | exit 0 clean | yes |
| Q6 data: url src | exit 0 clean | exit 0 clean | yes |
| Q7 cross-scheme same host | exit 0 clean | exit 1 failed-policy, a[href]="http://o.github.io/other/" | NO |
| Q8 base href + "../up" | exit 1, a[href]="../up" | exit 0 clean | NO (my error) |
| Q8b base href + "../../up" | exit 1, a[href]="../../up" | exit 1, a[href]="../../up" | yes |
| Q9 padded src value | exit 1, img[src]=" /x.png " | same | yes |
| Q10 "/repo/subx" prefix | exit 1, a[href]="/repo/subx" | same | yes |
| X1 template content (bonus) | exit 1, a[href]="/x" | exit 0 clean, referencesChecked 0 | NO |
| X2 default port :443 (bonus) | exit 1, a[href]="https://o.github.io:443/x" | same | yes |
## Disagreements
1. Cross-scheme same host (P3, Q7): the interface text says other origins are compared by (scheme, host, port) and are ignored, so `http://o.github.io/other/` on an `https` page should be ignored. The tool reports `outside_base_path`, because `_site_key` drops the scheme (`scripts/base_path_audit.py:345-350`, used at `:581` and `:700`) and its module docstring says http and https on one host are the same site (`:36-37`). No matrix case and no committed selftest fixture contains an `http://` reference, so the declared 30/30 cannot see it. Effect on the round-23 snapshot run: none (no `http://` in the six files under `.ufo/waves/round-29/real-input/sites/`), so the 4 reported findings are unaffected.
2. Q8 was my own prediction error: `../up` against base `/repo/sub/` resolves to `/repo/up`, inside base path `/repo/`, so exit 0 clean is right. The corrected variant Q8b (`../../up` -> `/up`) agrees.
3. X1 template content: the interface text lists `a[href]` as a reference and says nothing about template content; the tool deliberately skips template content (docstring `:26-28`). The interface is silent, so this is a gap in the interface text, not a proven defect. Bonus probe, outside the required set.
## Verdict
- Holds on 17 of 21 held-out probes, including every quoting, entity, attribute-mismatch, port and base-path rule the interface text states.
- Breaks one stated interface rule: a cross-scheme, same-host reference is treated as same-origin. On the interface text the claim is broken; in the tool's own docstring it is intended behaviour. The L1 must choose which text is the contract. The frozen 30-case matrix has zero power here.
- Q8 is my error, not the tool's.
## Mutation probe (sandbox copies only; lane bytes never modified)
- M1 `M1-cross-scheme-is-other-origin`: one line of `_site_key` made the scheme part of the site key (mutant sha256 `26bfd1150fe5865a6943bd7656a32069ebbe2f15adb430685248335e412e415e`). Frozen matrix 30/30, survived. Held-out set 19/21 against pristine 17/21, so the held-out probes detect what the frozen matrix cannot.
- M2 `M2-template-content-is-scanned`: the template skip in `handle_starttag` disabled (mutant sha256 `61bea60db523cb805317e049f6cb5dadf5962ccf380d12800865af9ea1f6aa0b`). Frozen matrix 30/30, survived. Held-out set 18/21.
- Restoration: pristine sha256 `e3264615...` identical before and after; commit bytes at 7697990 still `e3264615...`; both mutant files deleted after their run. The lane working-tree copy was edited by another seat during my run (sha256 `f923564a...`, usage text only, no behaviour change); I attacked the commit bytes and did not touch the lane file.
- Also measured: the wave-1 fake tool `f4_wrong_generic.py` passes the frozen matrix 30/30 but only 12/21 of the held-out probes.
## Not verified
- No reference implementation exists, so every expectation is my reading of the interface text.
- No live site was probed; only the six saved snapshot files were read. The other 30 matrix cases were not re-derived by hand; the counter run reproduced 30/30.
## Tooling
No installs or upgrades were needed. System `python3` 3.14.8 and `git` only; every write went to `/fast/scratch/hyaku/kake-r29/w2/HeldOutCases` (`probes_heldout.py`, `mutate.py`, `runs_heldout.jsonl`, `runs_w1_probes.jsonl`, `runs_mutation.json`, `runs_counter_7697990.json`).
