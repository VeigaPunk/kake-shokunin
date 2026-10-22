# ReviewMistakesRows — round-34 lesson `## Mistakes` rows verified

Sandbox: `/fast/scratch/hyaku/kake-r34/w2/ReviewMistakesRows/` (clone at
`24a16474ee73e20453f3e1be9d2f33573c5196d9`, TMPDIR=<sandbox>/tmp). No tools
installed. Only this report written in the lane; all mutations in the sandbox
clone (two `git fetch` of retained bundles, one failed bare clone into TMPDIR).

Method: each row's evidence pointers resolved against committed bytes; each
named check command re-run in the clone; output compared to the committed
receipt byte-for-byte or field-for-field.

## Row 1 — sandbox-only evidence pointers — PASS

- `c1-strict-at-critic-489714b.json` `"rev"` = `489714be413c…` (verified);
  `RerunC1Strict.md:28-30` "exists only in the w1 clone" (`:24-29` spans
  the receipts-stop sentence plus this — accurate). `git cat-file -e 489714be…`
  in the lane clone: exit 1 pre-fetch, object absent — confirmed.
- Captured-by: routed defect 2 = `round-33-verifier-spotcheck.md:192-196`
  ("Two evidence artifacts live only in sandbox scratch", both named) — accurate.
- Fix re-runs: `git cat-file -e d08d8de:<bundle>` → exit 128 "exists on disk,
  but not in 'd08d8de…'"; `a2fe31b2:<bundle>` → exit 0. Identical to receipt
  `criterion-retained-path-d08d8de-vs-a2fe31b.txt`.
- `git fetch <bundle> 'refs/tags/*:refs/tags/*'` → exit 0 `[new tag]
  r33-c1-counterexample`; `cat-file -p 489714be` shows `parent bc6c4a8d…`,
  `git show` 2 files +2/-2 (raise line + `reason_contains`). Fetch of a
  nonexistent path → exit 128; `git clone --bare <bundle>` → exit 128
  "Repository lacks these prerequisite commits: bc6c4a8d…". All row claims
  reproduced. sha256: bundle `6ff6c403…77c00`, dedup `28fd9adf…7d6e`,
  alt `daeaa738…ce6e` — all match.

## Row 2 — Gate with admits only — PASS

- `round-33.md` at `a2fe31b2`: Gate table rows at `:31` (S065) and `:32`
  (S066), both `admit`; `grep -cE '\| (admit|reject)'` over section = 2 — matches.
- Captured-by: routed defect 3 = `round-33-verifier-spotcheck.md:197-198`
  ("records no reject") — accurate; QUALITY (b) grounds item 3 — accurate.
- Re-runs: `gate_reject_check.py --rev 93359ff… --lesson corpus/lessons/round-33.md`
  → exit 1 `NO MATCH: ## Gate has no source decision beginning with reject and
  a non-empty reason` = receipt `criterion-gate-reject-r33-at-93359ff.txt`.
  `--rev a2fe31b2 --lesson corpus/lessons/round-29.md` → exit 0, MATCH line
  byte-identical to `criterion-gate-reject-r29-at-a2fe31b.txt`. Bonus:
  `--rev 24a1647 --lesson corpus/lessons/round-34.md` → exit 0 MATCH S071.

## Row 3 — run cited with no receipt — PASS

- Fleet `/.ufo/reports/round-33/kake.md:62` ends "`93359ff`: 4/4 (run, not
  committed)" — verified; file committed in fleet repo (`221c680`). Lane
  `round-33/verification/` `ls | grep -c 93359ff` = 0 — verified.
- Captured-by: routed defect 4 = `round-33-verifier-spotcheck.md:199-201`
  (quotes the same line) — accurate; QUALITY (c) grounds item 4 — accurate.
- Re-runs: `receipt_presence_check.py --report <fleet kake.md> --repo . --rev
  93359ff0924bf622acc51eb15c2afa3cd2743022 --round 33` → exit 1
  `unreceipted hashes: 93359ff` = receipt `criterion-receipt-presence-r33-report.txt`.
  Positive: same run on a TMPDIR copy with the `; \`93359ff\`: 4/4 (run, not
  committed)` clause removed → exit 0 `all measured hashes have committed receipts`.
- Nit (non-blocking): "holds receipts only for 5777d5a, bc6c4a8, b1752a2,
  e490381, 1cf452e, 3abfc44" omits `c1-strict-at-critic-489714b.json` (rev
  489714be — a sandbox commit, not a measured lane rev); and concurrency
  receipts at 3abfc44 exist. The operative claim (no receipt for 93359ff) holds.

## Row 4 — full score to a lookup-table control — PASS

- `c1_matrix_count.py:112` `materialize(case, scratch / tool_path.stem)` with
  `work = base / case["id"]` — the case-directory-name leak is real code.
- Evidence pointers: `w1/CriticDeclarationFit.md` (dcef39b5 28/28, 0cce15f0
  5/5, quotes confirmed); `w1/ReviewC1CounterDiff.md` (stub 83f53357 28/28);
  `retained/r34-c1-lookup-dcef39b5.bundle` + `r34-c2-hollow-0cce15f0.bundle`;
  `c2-at-critic-hollow-0cce15f.json` — all resolve in committed bytes.
- Captured-by: QUALITY round-33 bullet "hollow control scores below its
  after-value" (`corpus/QUALITY.md:590-604`) — accurate; lesson states the
  requirement existed but no control was run.
- Re-runs (bundles fetched via `refs/heads/*:refs/heads/*`; note row-1's
  `refs/tags/*` refspec does NOT fetch these branch-ref bundles — silent no-op,
  an under-specification in the row-4 replication path):
  `lookup_control_check.py --counter .ufo/waves/round-34/c1_matrix_count.py
  --repo . --control dcef39b5f4e8373970eb74858d2c6175524cdfd0` → exit 1,
  `{"score": 28, "total": 28, "verdict": "FAIL: control reaches the full score"}`
  = receipt `criterion-lookup-control-c1-dcef39b.txt` (modulo counter path).
  Same check vs `0cce15f0…` on `c2_source_census.py` → exit 1, score 5/5 —
  agrees with `c2-at-critic-hollow-0cce15f.json` (met 5/5).

## Verdict

All four rows: evidence resolves in committed bytes, captured-by accurate,
fix demonstrated able-to-fail by re-run matching the committed receipt. No
falsification found. Two nits above (row-3 receipt list slightly incomplete;
`refs/tags/*` vs `refs/heads/*` asymmetry between the two bundle formats).
Not verified: rerun of wave-1 receipt-generation commands themselves; the
`28fd9adf`/`daeaa738` patch contents beyond hash equality.
