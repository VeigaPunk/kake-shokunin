# ExecNoHarmGates — no-harm gate re-run at the committed round-47 lane tip

**Seat:** executor; leaf (no delegation, no background jobs, no `agent://all`).
**Lane:** `/home/vgpnk/Projects/shokunin/kake-shokunin`.
**Evidence revision:** `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` (`git rev-parse HEAD`; 5 commits
after the frozen base `cd42e3c310ba442e89dde638ba6401adaefaf3e8`, which `git cat-file -t` confirms
is a commit).
**Evidence window:** 2026-10-24T07:40:29Z–07:42Z. `node v24.21.0` (from the sweep's own header);
`python3` 3.14 (`/usr/lib/python3.14` in the traceback of one deliberate bad-input control).

**Result of the assigned triple: all three re-run green at the tip, matching the committed receipts.**
`node scripts/freshness-sweep.mjs --selftest` → `selftest: 35/35 passed`, exit `0`.
`python3 -B scripts/citation_lint.py --selftest` → `selftest: 8/8 passed`, exit `0`, byte-identical
to the committed receipt stdout.
`python3 -B scripts/citation_lint.py --root .` → one JSON line, `"verdict":"clean"`,
`"violations":[]`, `30` adjudicated occurrences, exit `0`.

No difference from a committed receipt falsifies any C1/C2 clause. Findings N1–N4 below are
receipt-identity and operability hazards, not claim falsifiers; N1 is the one with wave-level blast
radius.

## 0. Byte provenance of what I actually ran

The working tree carries peer edits (`.ufo/waves/round-47/w1/swarm-registry.json` modified,
`.ufo/waves/round-46/residual/` and `.ufo/waves/round-47/w1/MutationC1Receipt.md` untracked), none of
which is in the gate population or the tool set. I verified byte equality to `git show HEAD:` before
trusting the runs:

| Path | worktree sha256 | equals `git show HEAD:<path>` |
|---|---|---|
| `scripts/freshness-sweep.mjs` | `a1aa79d114093cc5b663e811e86a20a57bf37357dd8a3598c9e02084770d8d8b` | yes |
| `scripts/citation_lint.py` | `3c78a0a82f70b166776f7f7626dc7afbf9f9916a4399ae879287e4bf9662987f` | yes |
| `scripts/redirect_audit.py` | `1e1dff18030c9028d833ab108bff140102343f4c5198c35984e7838e54bb748a` | yes |
| `SCORECARD.md` | `8bd2ffe95ecafdfc12d477256452a27dfb9e26c25f5c21e631fe2c52a0038e02` | yes |
| `LOG.md` | `16d1085b91ff1153fff6eaccedf94e8d67c85a64d8d9b8d6c721cf0a06a9999c` | yes |
| `corpus/quality/citation-adjudications.md` | `e75bc3a746539d86651f4b31f578480702fc325cbe1e1555cd76aa38d5058669` | yes |

`git diff --stat HEAD -- scripts/ SCORECARD.md LOG.md corpus/quality/citation-adjudications.md`
is empty (`rc=0`). So every run below is at committed tip bytes, not a peer's half-finished state.

## 1. Assigned reruns — exact commands and outputs

### 1.1 `node scripts/freshness-sweep.mjs --selftest`

`cwd` = lane root; **no** `HOME` or `KAKE_SELFTEST_DIR` override (the bare form, as assigned).
Exit **`0`**. 108 stdout lines, `35 PASS`, `0 FAIL`; stderr empty.

```text
freshness-sweep --selftest
fixtures: /tmp/kake-r16/selftest (hermetic; re-runnable)
  PASS  a annotated-missing -> declaredAbsent, exit-neutral
        expect: exit 0 · declaredAbsent contains selftest-missing.md · drift [] · resolve contains selftest-present.md
        got:    exit 0 · declaredAbsent ["~/Projects/webzites/selftest-missing.md"] · drift [] · resolve ["~/.kake-freshness-selftest-102911/selftest-present.md"]
  ...
  PASS  recovered list is exact and informational
        expect: exit 0, recovered [~/.kake-freshness-selftest-102911/selftest-present.md]
        got:    exit 0 · ["~/.kake-freshness-selftest-102911/selftest-present.md"]
selftest: 35/35 passed
```

### 1.2 `python3 -B scripts/citation_lint.py --selftest`

Exit **`0`**. Full stdout (9 lines), verbatim:

```text
citation_lint --selftest
  PASS  planted dead citations flagged (2/2)
  PASS  resolving commit not flagged
  PASS  no false positives on the exclusion classes
  PASS  mutant F (no resolution) false-green on dead token (diverges)
  PASS  mutant G (no context filter) overreaches on plain hex (diverges)
  PASS  mutant H (no digest exclusion) flags the sha256 token (diverges)
  PASS  mutant E (no ellipsis rule) overreaches on digest prefixes (diverges)
  PASS  adjudication ledger suppresses named token/file only
selftest: 8/8 passed
```

### 1.3 `python3 -B scripts/citation_lint.py --root .`

Exit **`0`**. One compact JSON line (2 667 bytes; scratch `cl_root.out`), fields:

```json
{"adjudicated":[ …30 entries… ],"adjudications":"corpus/quality/citation-adjudications.md",
 "population":["SCORECARD.md","LOG.md"],"revision":null,"verdict":"clean",
 "version":1,"violations":[]}
```

Adjudication composition measured from that line: **30 occurrences**
(`SCORECARD.md` 16, `LOG.md` 14), **20 unique (file, token) pairs** (`LOG.md` 12,
`SCORECARD.md` 8), classes `sandbox-control commit` 15, `external-repo commit` 12,
`quoted-dead-token` 2, `external-repo pin` 1. `revision` is `null` because I ran the form exactly
as assigned, without `--revision`.

## 2. Difference from committed receipts

| Command | Committed artifact | Claimed | Reproduced | Difference |
|---|---|---|---|---|
| `freshness-sweep.mjs --selftest` | `.ufo/waves/round-46/verification/no-harm-baseline.md:99-141` (added by `ee43e66`); no round-47 receipt exists | `selftest: 35/35 passed`, `EXIT_CODE=0` | `35/35 passed`, exit 0 | **2 of 108 lines differ**, both dynamic: output line 26 (`"generatedAt": "2026-10-24T07:40:30Z"` vs `…04:59:10Z`) and lines 106–107 (`~/.kake-freshness-selftest-102911/…` vs `…-2656727/…`). Other 106 lines byte-identical (`diff -u`, after normalizing the pid suffix and dropping the trailer). See N2. |
| `citation_lint.py --selftest` | `.ufo/waves/round-47/verification/selftest-citation-lint.txt` (`tool_sha256: 3c78a0a8…2987f`, `run_at_utc 06:46:10Z`) | `selftest: 8/8 passed`, `exit=0` | identical | **None.** `diff -u` of the receipt's `stdout:` block against my stdout → **rc 0**. Tool sha256 equals the receipt's field. |
| `citation_lint.py --root .` | `.ufo/waves/round-46/verification/c2-after-ee43e66.json` (`861113e`) | `clean`, 0 violations, 30 adjudicated, population `{SCORECARD.md, LOG.md}` | `clean`, 0 violations, 30 adjudicated, same population + same `adjudications` path | Only `revision`: committed `ee43e663…`, mine `null` (no `--revision`, as assigned). `adjudicated` lists are **equal as arrays**; `verdict`, `violations`, `population` equal. |

Extra control, same gate with the tip revision (this is the frozen C2 command form):
`python3 -B scripts/citation_lint.py --root . --revision 766f4610b64f35a0f402b37eb1d8be2d4d634c0f`
→ exit `0`, `"verdict":"clean"`, 30 adjudicated, 0 violations. So the gate is clean **at the tip**,
not only at the r46 build revisions.

## 3. Independent deciders re-run (extra, read-only)

Assigned target is the triple above; the following are the cheapest deciders of the two claims and
were run through committed bytes only (`git show` / `ls-tree`).

| Command | Output | Exit |
|---|---|---|
| `python3 -B scripts/redirect_audit.py --selftest` | `selftest: 23/23 passed`; stdout byte-identical to `.ufo/waves/round-47/verification/selftest-redirect-audit.txt` (`diff` rc 0); tool sha256 `1e1d1ff1…748a` equals the receipt's `tool_sha256` | 0 |
| `python3 -B .ufo/waves/round-47/c47_registry_count.py --root . --revision 766f4610…` | `registry_rows=2/2 receipts=2/2 C1_MET` | 0 |
| same counter at `714e7074…` (the filed after-receipt's revision) | `registry_rows=2/2 receipts=2/2 C1_MET` | 0 |
| same counter at base `cd42e3c3…` | `registry_rows=0/2 receipts=0/2 C1_NOT_MET` | 1 |
| same counter at an unreadable 40-hex revision (my own mistyped hash) | `could-not-evaluate: no SKILL.md at 766f461b…` (stderr) — negative control for the exit-2 path | 2 |
| `python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision 766f4610…` | `outstanding=0/4 C2_MET` | 0 |
| `python3 -B scripts/citation_lint.py --root . --adjudications /nonexistent/adj.md` | `verdict:"failed-policy"`, **30** violations (all 30 adjudicated occurrences), one human line each | 1 |
| `python3 -B scripts/citation_lint.py --root /nonexistent-root` | `citation_lint.py: cannot read SCORECARD.md: [Errno 2] …` | 2 |
| `python3 -B scripts/citation_lint.py` (no args) | usage error | 64 |

Registry rows the C1 counter reads are `SKILL.md:1197` (`redirect-expectation-audit`) and
`SKILL.md:1198` (`commit-citation-lint`); both name the round-47 receipt paths and their tallies.

## 4. Findings

### N1 — MEDIUM (operability, inherited): `--selftest` is not concurrency-safe under its default fixture path

`scripts/freshness-sweep.mjs:1183` resolves the fixture dir as
`process.env.KAKE_SELFTEST_DIR || '/tmp/kake-r16/selftest'` — a **fixed** path. Fixtures are then
written unconditionally under it (the `SELFTEST-WRITES` region ending at `:1270`), and the cleanup
region (`:1628-1630`) removes **only** the per-pid `$HOME` dir, never the shared tree. The header
still prints `fixtures: <dir> (hermetic; re-runnable)` (`:1634`).

Measured, 4-way concurrency, same code branch (shared scratch dir — I deliberately did **not** point
the experiment at `/tmp/kake-r16/selftest` to avoid corrupting peers' in-flight evidence):

| Run | Fixture dir | Result | Exit |
|---|---|---|---|
| 4 concurrent | one shared dir | `22/35`, `24/35`, `21/35`, `25/35` | 1, 1, 1, 1 |
| 4 concurrent (control) | four distinct dirs | `35/35`, `35/35`, `35/35`, `35/35` | 0, 0, 0, 0 |

Cross-run provenance is visible in the failure text: one run expected
`recovered [~/.kake-freshness-selftest-138564/selftest-present.md]` and got
`["~/.kake-freshness-selftest-138563/selftest-present.md"]` — a sibling process's `note.md` under
the shared dir. Sidecar cases additionally flip (`sidecar malformed JSON` expect exit 2, got 1).

Blast radius in this wave: the wave carries 32 seats and at least one peer was executing a base
archive self-test while this seat ran (roster entry `ReviewNoHarmC1`). Any two seats invoking the
documented bare command
concurrently can produce a **false red** on correct bytes and route a defect against an unchanged
gate. This hazard is inherited (the default path dates to `ab87a48`, round 16) and is already
acknowledged one level up — `SKILL.md:212` says the caller must isolate `HOME` and
`KAKE_SELFTEST_DIR` — but `SCORECARD.md:3980` states the no-harm result using the bare form with no
isolation, and `.ufo/waves/round-46/verification/no-harm-baseline.md` records a single unisolated
run. Suggested runbook fix for the integrator: `KAKE_SELFTEST_DIR=$(mktemp -d)` on every invocation
(or make the default per-process). I am not proposing a code patch here.

### N2 — LOW (freshness / receipt reproducibility): the sweep selftest's stdout is not byte-reproducible by design

`scripts/freshness-sweep.mjs:1215` embeds `process.pid` in the `$HOME` fixture path, and case `c`
echoes a child's `generatedAt` timestamp. Consequently no two runs are byte-identical, and the r46
receipt cannot be reproduced byte-for-byte (my diff: 2/108 lines, quoted in §2). The correct claim
for this gate is *semantic* reproduction (same 35 PASS ids, same exits), which holds; a byte-identity
check would be a false red. Normalizing `\.kake-freshness-selftest-[0-9]+` and `"generatedAt": "…"`
before comparison makes the receipt replayable.

### N3 — LOW (freshness / receipt identity): the round-47 no-harm tally has no receipt file

`SCORECARD.md:3980` asserts this exact triple (`35/35`, `8/8`, `--root .` exit 0) plus the ledger
check, without naming a receipt path. No file under `.ufo/waves/round-47/verification/` records
`freshness-sweep.mjs --selftest` (the only sweep artifact there is
`offline-sweep-r47-rerun.txt`, which is the `--offline` run); the sole selftest receipt is the r46
`verification/no-harm-baseline.md:99-141`. The lane's own rule is explicit —
`c47_registry_count.py:17-19`: "Prose tallies in LOG.md/SCORECARD.md are never receipts." My rerun
substantiates the numbers, so the line is **true but unreceipted** by that standard. This does not
falsify C1 (whose predicate only requires receipts for the two r46 gates) or C2; it is a gap the
next round should not inherit as a precedent.

### N4 — LOW (freshness / receipt identity): the after-receipts are revision-stale and each pins only half of QUALITY (l)

`SCORECARD.md:3975-3976` files `verification/c1-after-714e707.json` and
`verification/c2-after-714e707.json`, both measured at `714e7074…`. The tip is `766f4610…`, three
commits later, and `SKILL.md` gained 5 lines after the measurement
(`git diff 714e707..766f461 -- SKILL.md` → `1196,3 +1196,8`, the "Round-46 residual scope note").
I re-ran both frozen counters at the tip (§3): `C1_MET` and `C2_MET`. **The predicates are true at
the tip; the receipts are not tip-bound.** Field-level: the two counter receipts carry `revision`
but no `tool_sha256`/`selftest_sha256`, while the two selftest receipts carry `tool_path` +
`tool_sha256` + tally + `exit=0` but no `toolRevision`. `corpus/QUALITY.md:951-953` criterion (l)
asks for "revision and sha256, re-derivable from the revision" on a post-measurement receipt, so no
single r47 receipt satisfies that pair of fields on its own. Re-derivable today (I did it), but not
self-pinned.

### Positives worth retaining

- `citation_lint.py` and `redirect_audit.py` selftest receipts are the strongest artifacts in the
  round: tool sha256 matches the file on disk byte-for-byte, and the recorded stdout reproduces
  exactly (`diff` rc 0 for both). My independent 8/8 and 23/23 are those receipts, re-earned.
- The C2 gate's own output corroborates the R3 correction arithmetically: 20 unique
  (file, token) adjudications = 12 `LOG.md` + 8 `SCORECARD.md`, exactly the ledger's 20 data rows
  (`grep` of `^| .* | LOG.md |` = 12, `^| .* | SCORECARD.md |` = 8); the 30 figure is occurrences,
  not rows.
- Every bad-input path I exercised fails closed: missing ledger → 30 violations/exit 1 (a missing
  ledger cannot make the gate green); unreadable revision → exit 2; unreadable root → exit 2;
  no args → exit 64.

## 5. Write scope

- **Lane:** this report is the only file I wrote under
  `/home/vgpnk/Projects/shokunin/kake-shokunin`. No production file, `.jj`, git index, ref/bookmark,
  `.ufo/state/`, watchdog log, or sibling repo was touched; no mutating `git`/`jj` command was run
  (all git usage was `rev-parse`/`cat-file`/`show`/`ls-tree`/`diff`/`log`).
  `git status --porcelain` on entry: ` M .ufo/waves/round-47/w1/swarm-registry.json`,
  `?? .ufo/waves/round-46/residual/`. On exit it additionally lists peers' wave reports under
  `.ufo/waves/round-47/w1/` and this report — nothing of mine outside this report. One write-path
  slip, disclosed: the relative report path first resolved against the session CWD and the file was
  created at `<fleet-root>/.ufo/waves/round-47/w1/ExecNoHarmGates.md`; I moved it here and removed
  that stray. No other fleet-root file was read, moved, or modified.
- **Outside the lane:** scratch only under
  `/fast/scratch/hyaku/kake-r47/ExecNoHarmGates/` (captured stdout, diffs, four distinct fixture
  dirs, one shared fixture dir). The gate itself created and removed
  `~/.kake-freshness-selftest-102911/` (verified: `ls -d ~/.kake-freshness-selftest-*` → 0 entries
  after the run, including after the four failed concurrent runs) and refreshed the pre-existing
  shared `/tmp/kake-r16/selftest` tree at 2026-10-24T07:40:29Z, which the tool never cleans up.
- **Tooling:** no installs or updates; pacman not invoked (host pause respected).

## 6. Not run / limits

- I did not run the concurrency experiment against the live `/tmp/kake-r16/selftest` path, to avoid
  perturbing peers mid-wave; the shared-scratch dir exercises the identical branch and only the path
  string differs. A reproduction at the real path is a two-line experiment for the integrator.
- I did not run `node scripts/freshness-sweep.mjs --offline` (it can write lane history state); R6's
  rerun receipt and `c47_routed_count.py` were the read-only evidence I used instead.
- I did not judge, re-score, patch, commit, or push anything; no subagents or background jobs.
