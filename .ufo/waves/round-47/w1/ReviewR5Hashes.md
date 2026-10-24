# ReviewR5Hashes — round 47 w1

Scope: C2 freshness leg R5 (round-46 LOG landing-hash citation) plus resolution of the
round-46 build/verdict/wave-spec hashes. Read-only; no lane file written except this report.

Lane tip `refs/heads/master` = `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` (= HEAD); frozen base
`cd42e3c310ba442e89dde638ba6401adaefaf3e8`. `git status --short LOG.md SCORECARD.md SKILL.md`
is empty, so all line citations below are committed bytes, not worktree drift.

## Verdict

No falsifying defect in the R5 slice. All three cited hashes resolve as commits, are ancestors of
the lane tip (and of the frozen base), and a same-line correction naming both landing hashes exists
in the round-46 section. One Low predicate-coverage gap and two informational notes follow.

## Evidence

### 1. Hash resolution (`git cat-file -t`, full 40-hex inputs)

| Hash | `cat-file -t` | `rev-parse` round-trip |
|---|---|---|
| `ee43e66367bf23e386ff29029b9ea60515efd9d1` (build) | `commit` | exact |
| `861113eb0eea4d51bd0614c542aa6ecb7cc9a843` (verdict) | `commit` | exact |
| `ded938d2f23aba265d1acf1fdd4b3ab028020037` (wave spec) | `commit` | exact |
| `cd42e3c310ba442e89dde638ba6401adaefaf3e8` (base) | `commit` | exact |

`git rev-parse --is-shallow-repository` → `false`; `git replace -l | wc -l` → `0`.

### 2. Ancestry

- `git merge-base --is-ancestor <h> 766f4610…` → exit 0 for all three hashes.
- Same against `refs/heads/master` → exit 0 for all three; against the base `cd42e3c…` → exit 0
  for all three (so all are inherited, not re-introduced this round).
- `git rev-list --first-parent refs/heads/master | grep -qx <h>` → exit 0 for all three.
- Parent chain is consecutive and matches the labels:
  `ded938d^` = `bd86ee80…`; `ee43e66^` = `ded938d`; `861113e^` = `ee43e66`;
  `cd42e3c^` = `861113e`.

### 3. Role attribution

- `ee43e66`: subject `round-46: C1 redirect/rewrite audit + C2 citation-hygiene gate (tools,
  sealed matrix, fixtures, ledger, S135)`; tree contains `scripts/redirect_audit.py` and
  `scripts/citation_lint.py` — build commit.
- `861113e`: subject `round-46: after measurements (…), verdict hashes, residual wave spec`; its
  `SCORECARD.md` carries `## Round 46 — measured verdicts (2026-10-24, attempt 1 resumed)` —
  verdict commit.
- `ded938d`: subject `round-46: v2 wave spec + validated dispatch (64 seats, 28 attack)`; its
  `w46-spec.json` reads `wave=kake-r46-w1`, `items=64` — wave-spec commit.
- Ordering: `ded938d` 01:50:16 → `ee43e66` 03:03:40 → `861113e` 03:04:17 → `cd42e3c` 03:22:36
  (-0300), consistent with wave-spec → build → verdict → spot-check.

### 4. R5 same-line correction

- Exactly one line in `LOG.md` contains both full landing hashes: **`LOG.md:1813`** —
  `- [r47-correction R5 identity] Full hashes of the round-46 build and verdict commits are
  `ee43e663…` and `861113eb…`.` (both literals on one physical line; `cat -A` shows `$` only
  after the final period).
- That line sits inside `## Round 46 (attempt 1, frozen 2026-10-24)` (heading `LOG.md:1757`), so
  the "entry cites" scope holds.
- It is present byte-identically at `846138c:LOG.md:1813`, `714e707:LOG.md:1813`, and
  `HEAD:LOG.md:1813` — it was not appended after the C2_MET measurement.
- The labeled correction `LOG.md:1798-1804` names all three hashes (`1800` build, `1801` verdict,
  `1802` wave-spec) but wraps them across three lines, so it alone cannot satisfy a same-line
  predicate.
- Append-only shape: `git diff --numstat cd42e3c..766f461 -- LOG.md` → `101	0	LOG.md`;
  removed-line count `0`.

### 5. Counter reproducibility and receipt identity

- `python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision cd42e3c…` →
  `outstanding=4/4 C2_NOT_MET`, exit 1; per-defect `{R3:false,R4:false,R5:false,R6:false}`.
- Same at `714e707…` → `outstanding=0/4 C2_MET`, exit 0, all four true.
- Same at HEAD `766f461…` → `outstanding=0/4 C2_MET`, exit 0.
- `--json -` output is byte-identical to the committed `verification/c2-before-cd42e3c.json` and
  `verification/c2-after-714e707.json` (`diff -q` empty for both).
- Retained failed measurement `verification/c2-after-846138c.json` shows only `R6:false`,
  matching `LOG.md:1858-1863`.
- Receipt sha256 match the LOG claims: `866b91be…` (before), `141ede64…` (after), `b86bc459…`
  (r47 rerun).

## Findings

**F1 — Low (instrument coverage; not a claim falsifier).** The R5 predicate enforces two of the
three hashes the R5 correction declares. `c47_routed_count.py:47-50` defines `R5_HASHES` as only
the build + verdict literals, and `:135` is `r5_fixed = any(all(h in line for h in R5_HASHES) for
line in log_lines)`. The frozen predicate `SCORECARD.md:3951-3953` names the same two literals;
`LOG.md:1802`'s wave-spec hash `ded938d2…` appears in neither. Consequence: a corrupted or absent
wave-spec hash leaves `R5:true` and `C2_MET` green. I verified that third hash by hand today
(commit, ancestor of base and master, first-parent, correct subject and 64-item spec), so the
claim is true as written; the gap is that the instrument cannot test it. This does not falsify C2,
whose declared predicate names only the two landing hashes.

**F2 — Informational.** The same-line contract is carried only by the duplicate bullet
`LOG.md:1813`, not by the labeled R5 correction `LOG.md:1798-1804`. The duplication is benign
(append-only, identical literals, no contradiction), but it is the predicate's actual carrier,
and it is why F1 exists: the sole satisfying line names two hashes, so the third stays outside
any line-level check. Two copies of the same fact must be kept in sync.

**F3 — Observation, not a defect.** `LOG.md:1888` claims `w1/swarm-registry.json` sha256
`bce58d7f93f64cdec17e3ebe68678c8382bc4b0e262bc2786237d11051635582`; the committed blob at HEAD
hashes exactly that. The working tree currently hashes `e5b5ee10c874…` with `M` status, and
`w1/` holds untracked seat reports. In read-only scope the committed claim is intact; the drift
is runtime seat state, not C1/C2 evidence. The integrator should compare committed bytes, not
worktree bytes.

## Residual risk

- The ancestry sentence `LOG.md:1803-1804` is prose with no committed `git merge-base` output. I
  re-ran it (all exit 0), but no receipt binds it, and C2 does not check ancestry.
- `R5` is literal-existence only: a line quoting both hashes in a negated context would also pass.
  At HEAD exactly one line matches and it is affirmative, so no present defect.
- `cat-file -t` proves object existence and type, not role. Role attribution here rests on commit
  subjects, tree contents, and ordering — all consistent, but not a cryptographic binding.

## Verification gaps

- Did not run `git fsck` or verify pack integrity.
- Did not run the C1 counter or any R1/R2 check (other seats).
- Did not re-run the round-46 verdict-time freshness sweep (withdrawn by R6; out of this slice).
- Counter runs used `--json -` (stdout) only; no lane receipt was rewritten, and no sandbox clone
  or mutating git/jj command was used.
- No tool installed or updated by this seat.
