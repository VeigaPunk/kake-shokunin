# w2/ReviewRetainedControls — retained round-34 control bundles and receipts

Axes: operability (do the retained controls actually run under the declared counters) and
freshness (do the receipts reflect the landed artifacts byte-for-byte). Result: both controls
reproduce exactly; receipts match my re-runs; no new defects in scope. The underlying
counter-insufficiency (lookup table scores 28/28, hollow entry scores 5/5) is already disclosed
by the L1 in SCORECARD "Round 34 — measured results" and the lesson's mistake row 4; not re-reported.

Sandbox: /fast/scratch/hyaku/kake-r34/w2/ReviewRetainedControls/ (clone at
24a16474ee73e20453f3e1be9d2f33573c5196d9; TMPDIR=…/tmp; GIT_* unset). Rerun artifacts:
c1-crit-rerun.txt, c2-rerun.json, c1-receipt-line1.txt in the sandbox root.
Tools installed: none (system git + python3 sufficed).

## Bundle integrity (read-only on lane files)
- `sha256sum` in .ufo/waves/round-34/retained/:
  r34-c1-lookup-dcef39b5.bundle = 6486b9abc3cb32c5403bc4ddeb7331bc8e6aace6dd775c04fd3733ab1cab2b7e
  r34-c2-hollow-0cce15f0.bundle = cf17a18e52669c236f203177c4a0c3329eee435ac43cff39ce03f2c439060843
- `git bundle list-heads`: c1 bundle → dcef39b5f4e8373970eb74858d2c6175524cdfd0 refs/heads/lookup-c1;
  c2 bundle → 0cce15f0719a4fc23e0e1e7a20bf680f5974e1ba refs/heads/hollow-c2.
- `git -C clone bundle verify <bundle>`: "is okay" for both; each requires a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f (present).
- Fetched into sandbox refs/retained/c1-lookup and refs/retained/c2-hollow; `cat-file -t` = commit.

## Commit inspection
- dcef39b5: parent a2fe31b (the pre-tool "before receipts" commit; `git log -1` → "round-34: before
  receipts at base and declaration…"), author "critic", 2026-10-22 18:07:54 -0300, subject
  "sandbox: lookup C1". Diff: 18-line new file scripts/link_preview_audit.py — a lookup table of
  exactly 28 unique 64-hex sha256 keys (one per frozen matrix case) mapping hashed argv+file-tree
  keys to canned {exit, verdict, findings}; default fallback is clean/0. `merge-base
  --is-ancestor dcef39b5 24a1647` → exit 1 (not on master; bundle-only, correct).
- 0cce15f0: parent a2fe31b, author "critic", 18:07:36, subject "sandbox: hollow C2". Diff adds
  junk SOURCES rows S067–S070 (status cell `mined`, opened `2026-10-22`), a 10-line
  corpus/knowledge/link-preview-metadata.md ("# junk", filler, ids on line 9, census line 10), and
  corpus/lessons/round-34.md with the four gate quotes. `merge-base --is-ancestor 0cce15f0 24a1647`
  → exit 1 (bundle-only, correct).

## Counter re-runs vs receipts
Counter bytes used (my clone at 24a1647): c1_matrix_count.py sha256 fc72d855cde3656fe74ab8372ae57dca39ff2d7cebc5e5e4aced6e483b71c51e
(matches the JSON's own counterSha256 field); c2_source_census.py sha256 ee7461b9e3a33949174591c527ccbf2854ca178c41638f71b5128cbd57e5f892
(matches c2 receipt counterSha256); c1-matrix.json sha256 246a6a3b…14f7 = MATRIX_SHA256 constant pinned in the counter.

- C1: `cd clone/.ufo/waves/round-34 && python3 -B c1_matrix_count.py --root <clone> --revision dcef39b5…` → exit 0, JSON passed 28/28, byKind 6/6+13/13+7/7+2/2, all four constant gates rejected (6/28, 0/28, 6/28, 1/28), toolSha256 a2e274c0…30ec = sha256 of `git show dcef39b5:scripts/link_preview_audit.py`.
- C1 receipt: `python3 -B criteria/lookup_control_check.py --counter c1_matrix_count.py --repo <clone> --control dcef39b5…` → exit 1, prints
  `{"counter": "c1_matrix_count.py", "control": "dcef39b5f4e8373970eb74858d2c6175524cdfd0", "score": 28, "total": 28, "counterExit": 0, "verdict": "FAIL: control reaches the full score"}`.
  `diff` vs line 1 of verification/criterion-lookup-control-c1-dcef39b.txt → identical; line 2 is `exit=1` (wrapper's own exit, matches).
- C2: `python3 -B c2_source_census.py --root <clone> --revision 0cce15f0…` → exit 0, met 5/5, controlBroken false, all a–d checks true, census stated == derived (pages=102 og:title=87 og:type=87 og:image=1 og:url=87 all-four=1 og-url-equals-canonical=87).
  `diff` of stdout vs verification/c2-at-critic-hollow-0cce15f.json → identical (1559 bytes both).

## Findings
- No discrepancy: both receipts are byte-exact re-runs of the landed counters on the retained bundles; bundles verify, controls are correctly isolated from master, and the criterion verdict ("FAIL: control reaches the full score") is faithfully recorded.
- Observation (not new): controls parent a2fe31b, where scripts/link_preview_audit.py and the corpus entry did not yet exist — the counter accepts whatever `<rev>:<path>` carries, which is exactly the disclosed necessary-not-sufficient gap.
- Verification gap: none in scope; I did not re-run the matrix cases' semantic correctness, only the counter outputs. No LSP server/device applies to these artifacts; checks were git/python/diff only.
