# RerunC1Strict — C1 strict supplement re-run (wave 2, falsify)

Sandbox: /fast/scratch/hyaku/kake-r33/w2/RerunC1Strict/ (clone of lane at
0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0; TMPDIR=sandbox/tmp; no tool installs;
w1 clone touched read-only via rev-parse/ls-tree/show and the script's
`git archive`). Script identity: `.ufo/waves/round-33/c1_strict_supplement.py`
is byte-identical at e490381..0a0acfb (empty `git diff --stat`, no commits touch it).

## Runs (exit codes as observed)

Command form: `python3 -B clone/.ufo/waves/round-33/c1_strict_supplement.py --repo <repo> --rev <rev>`

| rev | repo | result | exit |
|---|---|---|---|
| 5777d5af79cac1ebf9144b348a9d274099e77338 | lane clone | met 0/4 (all false) | 0 |
| b1752a2480aa86fc27536dd6e7d27a91b52bed12 | lane clone | met 4/4 | 0 |
| e4903817669aa411e424006bb342b345e143ab20 | lane clone | met 4/4 | 0 |
| 1cf452eafb028785ce9fa154887178864e22ab71 | lane clone | met 4/4 | 0 |
| 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0 | lane clone | met 4/4 | 0 |
| 489714be413c936a6d98188a80fce016c0b52ef7 | w1 CriticC1RepairScope clone | met 1/4 (s3 only) | 0 |

- My five revs reproduce the L1 receipts in
  `.ufo/waves/round-33/verification/c1-strict-at-{5777d5a,b1752a2,e490381,1cf452e,critic-489714b}.json`
  exactly, checks dicts included. **No receipt exists for tip 0a0acfb** (receipts
  stop at 1cf452e); my run fills it: 4/4.
- First 5777d5a attempt used a typo'd hash (`5777d5a79cac1…`, missing the `f`)
  → "unknown revision", exit 2. My error; correct hash runs clean.
- 489714be exists **only in the w1 clone** (my lane clone: not an object; w1 tree
  111e6c548efe9b4a076f98e7d8fd390195ccf4e1). `c1-strict-at-critic-489714b.json`
  is therefore not reproducible from the lane repo alone.

## Per check — can it fail for the reason it names?

All four: **yes**, each with an observed demo. Mechanism first: the supplement
exports `<rev>` via `git archive` (committed bytes only), requires the guard
pattern (`if step["op"] == "git_commit" and not initialized:` + one `raise` line)
to match exactly once (else exit 2), then s1 reads the exported P6 spec; s2/s3/s4
run the hostile selftest (exit 0 = pass) against pristine / message-reworded /
guard-deleted runner variants and read `detail.codes`/`detail.reasons`
(populated by scripts/citing_set_hostile_selftest.py:220-229 from runner failure
entries). The spec `gap` key is display-only (hostile selftest:205) — no hidden
mutant injection; s4's m3 is built by the supplement itself.

- **s1_spec — YES, as named.** Demo: at 5777d5af the h6 case carries
  `reason_contains: "needs an earlier 'git_init'"` and no `reason_code`
  (`git show 5777d5af:scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json`
  line 23) → s1 false. Pure JSON field predicate (equal to
  "setup_commit_before_init", no `reason_contains` key, exactly one h6); nothing
  else can flip it, so no false-pass path. Nit: scoped to h6 only, by design
  (`reason_contains` stays legal for other cases per CASE_KEYS:89-90).
- **s2_field — YES, as named, both clauses.** (a) No structured code: at
  5777d5af and 489714be the pristine h6 failure has `code: null` (old runner
  raised plain ValueError) → false. (b) Code leaked into message: demo D1
  (sandbox demo_strict.py, tip bytes, message arg prefixed with the code
  literal): hostile selftest still passes (exit 0, p6 passed True), h6 code
  still "setup_commit_before_init", but reason text contains the code → s2
  predicate False. D1 also re-demonstrates the round-32 hole independently:
  pass/fail of the selftest alone tolerates a runner that embeds the code in
  the message — the exact failure the frozen counter cannot see.
- **s3_message — YES, as named, with one observed limit.** Demo: at 5777d5af
  the reworded guard raises `ValueError("refused")`; hostile exits 1 with
  failing=["P6-commit-before-init"] (base spec keys on
  `reason_contains "needs an earlier 'git_init'"`) → s3 false for exactly the
  named reason: the selftest is keyed on message text. At tip s3 passes (exit 0,
  no failing case): tip keys h6 on `reason_code` only. Limit (observed at
  489714be): the old guard was `raise ValueError("setup_commit_before_init" ": %s …'git_init'" % CASE_SETUP_FILE)`
  (w1 clone, citing_set_selftest.py:365-366) — two adjacent literals; the
  mutation replaces only the message literal, leaving
  `"setup_commit_before_init" "refused"`, whose concatenation still contains the
  old key → s3 true even though that selftest is message-keyed. So s3 alone does
  not prove non-message-keying whenever code and message share the raise line's
  literal pool; s1's ban plus s2 carry that proof, and at tip the code is a
  separate first argument (`CaseRefusal("setup_commit_before_init", "%s setup op …")`,
  citing_set_selftest.py:402), so the limitation is latent, not active.
  Conservative false-fail: if MESSAGE_ARG matches 0 times (raise reshaped), s3
  is set false for a shape reason, not the named one (tip: messageArgMatches=1).
- **s4_layer — YES, as named, both failure shapes.** (a) Layer never existed:
  at 5777d5af and 489714be, m3 h6 code is null → false. (b) Layer removed:
  demo D2 (tip bytes, apply-time `SetupRefusal("setup_commit_without_repo", …)`
  replaced by `pass`, then load guard deleted): the case proceeds, git fails,
  h6 reports code "setup_failed" ≠ "setup_commit_without_repo" → s4 predicate
  False. False-pass bound: requires exit 1 AND code == L2 AND p6 failed; a
  double removal that lets the commit succeed cannot occur (commit without a
  repo fails), and a misnaming (either layer reusing the other's code) flips
  the equality. Conservative false-fail: GUARD's `[^\n]*\n` cuts a multi-line
  raise mid-call → deletion would mangle syntax and fail s4 for the wrong
  reason; tip's raise is single-line (line 402), so not triggered.

## Other observations (advisory)

1. Fail-visible, not fail-open: unlocatable/ambiguous guard, unknown rev, or
   archive failure abort with exit 2 and no `met` — the instrument cannot be
   silently fooled by refactoring the guard shape, but it can be silenced
   (aborted) by one; that is within the declared two-line shape contract.
2. SCORECARD.md "Round 33 — measured results" (:1122-1133) cites only the
   frozen counter c1_code_probe receipts; the c1-strict-*.json receipts are not
   referenced there. The strict results (which survive the wave-1 counter
   objection) exist and reproduce; the non-author closure may want them cited.
   Advisory only.
3. s3 requires `failing == []` across all cases, so an unrelated case breaking
   under the reworded runner also fails s3 — conservative, not exploitable.

## Not verified

- e490381/1cf452e were run beyond assignment only to match receipts; no other
  revs were attempted. The 489714be tree was inspected only through the w1
  clone; I did not confirm how that commit relates to lane history (not an
  ancestor visible to my clone).
- No check of c1_code_probe.py itself (outside scope; covered by other seats).

Report artifact in sandbox: /fast/scratch/hyaku/kake-r33/w2/RerunC1Strict/demo_strict.py
(D1/D2 harness; exit 0), raw run JSONs reproducible via the commands above.
