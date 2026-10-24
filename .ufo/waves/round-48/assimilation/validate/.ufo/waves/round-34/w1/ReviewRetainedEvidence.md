# ReviewRetainedEvidence — round 34 wave 1 (r33 routed item 2: verify retained evidence)

Seat: reviewer, axes operability + freshness. Advisory input for the L1; no verdict on the round.
Sandbox: `/fast/scratch/hyaku/kake-r34/w1/ReviewRetainedEvidence/` (clone of lane at `a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f`, TMPDIR `tmp/`). No tools installed or updated. No lane mutation; this report is the only file written in the lane.

## 1. Bundle verify + list-heads (run against the lane repo)

- `cd kake-shokunin && git bundle verify .ufo/waves/round-34/retained/r33-c1-counterexample-489714be.bundle` → exit 0:
  "is okay"; contains `489714be413c936a6d98188a80fce016c0b52ef7 refs/tags/r33-c1-counterexample`;
  requires `bc6c4a8d435473f3c30903210be30d9d6e3ef750`; hash algorithm sha1.
- `git bundle list-heads <bundle>` → exit 0: `489714be413c936a6d98188a80fce016c0b52ef7 refs/tags/r33-c1-counterexample`.
- Requirement satisfied by lane: `git merge-base --is-ancestor bc6c4a8d4354… master` → 0. Bundle sha256 `6ff6c403c4df5b2afa532556fcf13f9d4f6db55905442a77daa0955ab7877c00`.

## 2. Unbundled commit: parent and content

- `git -C <clone> fetch <bundle> 'refs/tags/*:refs/tags/*'` → exit 0 (`[new tag] r33-c1-counterexample`).
- `git -C <clone> cat-file -p 489714be…` → `parent bc6c4a8d435473f3c30903210be30d9d6e3ef750`; `rev-parse 489714be^` agrees. Matches `corpus/lessons/round-33-verifier-spotcheck.md:70-72`.
- `git -C <clone> show 489714be` → 2 files, +2/−2:
  - `scripts/citing_set_selftest.py:366` raise becomes `raise ValueError("setup_commit_before_init" ": %s setup op 'git_commit' needs an earlier 'git_init'" % CASE_SETUP_FILE)` (code literal inside message text).
  - `P6-commit-before-init/hostile.json:23` `reason_contains` → `"setup_commit_before_init"` (no `reason_code` key added).
  - Exactly what SCORECARD.md:1144-1146 and the closure describe; consistent with `verification/c1-strict-at-critic-489714b.json` (met 1/4: `s3_message` true — the message carries the literal — `s1_spec` false because the key stays `reason_contains`).
- Author/committer `critic <critic@sandbox>`, message "sandbox counterexample: code literal inside message text, P6 keeps reason_contains". Honest labeling, not presented as landed work.

## 3. Patch hashes + apply checks

`sha256sum` in `.ufo/waves/round-34/retained/`:
- `r33-option-table-dedup-patch.diff` → `28fd9adf5f302eaaa1e8046dd4ce4be4a884afaa7064c542339361baa1b47d6e` — equals expected `28fd9adf…d6e` (w2/CriticOptionTableRejection.md) and the executor's own recorded hash (w1/ExecDuplicatedOptionTables.md:13). 82 lines.
- `r33-option-table-alt-patch.diff` → `daeaa738525e424521e368826dccdcd03a44880f799002770d58d11c9b80ce6e` — equals expected `daeaa738…ce6e`. 142 lines.

Read-only apply checks in the sandbox clone:
- `git apply --stat` dedup → `scripts/citing_set_selftest.py` +28/−11 (one file); matches the critic's reported stat for sandbox commit `b209bcb`.
- `git apply --check` dedup @ `bc6c4a8` → exit 0; @ `0a0acfb` → exit 1 (`patch failed: scripts/citing_set_selftest.py:127`), reproducing the critic's apply failure at the lane tip.
- `git apply --stat` alt → `scripts/citing_set_selftest.py` +35/−15 (one file); matches reported stat for `21da23cf`; `--check` @ `0a0acfb` → exit 0.
- Retained dedup line 44 is `from citing_set import build_parser` — the line the closure's reject spot-check cited (`round-33-verifier-spotcheck.md:160`, "lines 43–44").

## 4. Sandbox-only pointers and their lane resolution

| Lane pointer | Artifact named | Resolves from committed bytes? |
|---|---|---|
| `SCORECARD.md:1146` "sandbox commit `489714be`" | counterexample commit | YES — `retained/r33-c1-counterexample-489714be.bundle`, tracked at `a2fe31b` |
| `verification/c1-strict-at-critic-489714b.json` `rev` field | same commit | YES — same bundle |
| `round-33-verifier-spotcheck.md:71` `git -C /fast/scratch/…/CriticC1RepairScope/clone show 489714be` | same commit via dead-path command | YES — bundle fetches the identical sha; original scratch clone also still exists on this host |
| `round-33-verifier-spotcheck.md:160,194` "sandbox `patch.diff`" | ExecDuplicatedOptionTables patch | YES — `retained/r33-option-table-dedup-patch.diff`, sha256 `28fd9adf…` equal to the recorded hash |
| `w2/CriticOptionTableRejection.md` "sandbox …/alt-patch.diff sha256 daeaa738…ce6e" | alternative patch | YES — `retained/r33-option-table-alt-patch.diff`, sha256 equal; applies at `0a0acfb` |

Routed item 2 named only the counterexample commit and `patch.diff`; the alt-patch was retained too, so the critic report's own evidence pointer also resolves. Retention precedent `.ufo/waves/round-33/verification/hollow-r32-c2-6ffa03e.bundle` is still tracked — same pattern.

Not retained (not routed; pointers remain sandbox-only): critic evidence files `CriticC1RepairScope/{probe-bc6c4a8.json,probe-cx.json,c1_code_probe.py}` (the probe's sha256 `74bf1f80…` is recorded in-lane and equals committed `.ufo/waves/round-33/c1_code_probe.py`); sandbox commits `b209bcb`/`21da23cf` (recoverable — dedup applies cleanly at `bc6c4a8`, alt at `0a0acfb`); w1/w2 seat evidence dirs under `/fast/scratch/hyaku/kake-r33/`; the `ds4cc-upstream` scratch clone. Round-33 dispatch/spec files also name every seat's `Sandbox:` dir as boilerplate; those are working-directory grants, not evidence pointers.

## Defects found

None. Bundle verifies against the lane, parent and diff match the SCORECARD/closure descriptions byte-for-byte, both patch hashes equal the declared values, and every pointer the routed item named now resolves from tracked lane bytes.

## Not verified

- Probe/strict-supplement scores on `489714be` were read from receipts, not re-run (item scoped to evidence verification).
- Bundle import into a repo already carrying tag `r33-c1-counterexample` (would need a namespaced ref or `--force`).
- Whether sandbox scratch under `/fast/scratch/hyaku/kake-r33/` persists — irrelevant now that pointers resolve in-lane.
