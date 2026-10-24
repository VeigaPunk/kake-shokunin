# CriticOpenItemsCarried — round 31, attempt 2, wave 2 (falsify)

Seat KakeR31a2.CriticOpenItemsCarried. Target: round-30 routed defect 2 (open items still named).
Axis judged: operability. Read at lane tip `92235a0578b04458c5eb96c966f82fa03593130e` (content
identical to `fde133a`). Sandbox: `/fast/scratch/hyaku/kake-r31/a2-w2/CriticOpenItemsCarried/`
(clone at 92235a0, TMPDIR inside it). No installs. No network. This file is my only lane write.

## Verdict
Every routed open item is named in SKILL "Citing-set runner containment — round 31" (SKILL.md:863-871),
so no item is dropped from the lane. But the declared carrier set is not met: the round-31 lesson names
none of them, and the SCORECARD drops one. Two wave-1 findings are only partly carried, and one SKILL
sentence contradicts the runner.

## Item | named where | missing
| Item (spotcheck.md:263-270 or wave 1) | SKILL (833-871) | Lesson round-31.md | SCORECARD (920-957) | Missing / note |
|---|---|---|---|---|
| IDENTITY-PATHS | 864 | no | 944, only as "the round-27 families" | lesson; SCORECARD does not give the label |
| RETENTION-FRAGMENT | 864 | no | 944, as a group | same |
| RETENTION-TRUST-BOUNDARY | 864 | no | 944, as a group | same |
| C1-UNIT-OVERRIDE | 865 | no | 944, as a group | same |
| socket `document_unreadable` label | 865 | no | 944, "the socket label" | lesson; SCORECARD omits the code name |
| 12 of 25 reason codes unfixtured | 865-866 | no | 944-945 | lesson |
| deep corpus and `O_NOCTTY` (counter-only) | 866-867 | no | **absent** | lesson and **SCORECARD** (its scope list skips this item) |
| four strict-checker holes | 867 | no | 945 | lesson |
| runner mutants m2, m4, m5 | 867-868, "still surviving at `f1ffb81`" | no | 945-946 | lesson. The wording understates: the mutants also survive at the repaired runner (measured below) |
| fifo on `.gitattributes` (ConnectSiblingOverlap) | 868-871 | no | 941-943 | lesson. **`.gitignore` is dropped**: it was in the same proposed move (ConnectSiblingOverlap.md:36), and it reproduces at tip (below) |
| gate Git calls without timeout (ConnectSiblingOverlap) | 871 | no | 942-943 | lesson. A related point is not named: the runner's gate timeout kills only the gate, so a stuck git grandchild can survive (ConnectSiblingOverlap.md:40, `[INFERENCE]`, unverified by them and by me). The runner has no `start_new_session`/`killpg` (grep finds no match) |
| option values unrestricted (ReviewHostileContract F2) | 841-843 | no | 941 | lesson |
| dot-named fixture entries skipped (L1's own residual) | **contradicted**: 851 says "a symlink in the fixture directory (a failed case, never a skip)" | no | 943-944 | SKILL:851 is false for a dot-named symlink (below) |

Other round-31 text: LOG.md:1322-1323 points defect 2 to the SKILL section. PROVINCE.md:122-123 carries
only "the round-27 families". QUALITY.md (488+) names none of them. The round-30 lesson says "carried
by name" (spotcheck.md:263). The round-31 lesson (sections Claims, Gate, Mistakes; 71 lines) has no
carried-open section. `grep -n -i "open\|carried\|not repaired"` over it matches only "opened" and
"openings".

## Status at tip (are the named items still truly open?)
- Gate `scripts/citing_set.py` sha256 `dbfade45…7f02`, the same as base. Strict checker
  `.ufo/waves/round-30/c1_strict_checks.py` `96e7bbcd…500f`, also the same as base.
  `git diff --stat f1ffb81 92235a0 -- scripts/ .ufo/waves/round-30/ .ufo/waves/round-27/` (exit 0)
  shows only the runner, the hostile selftest and specs, and `partial-reports.json` changed. So the
  socket label, 12/25, deep corpus, `O_NOCTTY`, the strict holes and the round-27 families stay open
  by blob identity. Nothing named was falsely closed.
- Mutants at the repaired runner `5371530d…ce6c`: I copied ScoutOpenFamiliesLedger's
  `mutate_and_run.py` and changed two lines: the runner path and the `failedCases` key. Each
  anchor is unique in the tip runner (grep -c = 1 each).
  `python3 -B mutate_and_run_tip.py` gave **exit 0**. m2, m4 and m5 each pass all 45 committed fixtures with `failed: 0`.
  Separators are live for each: pristine exit 1 / failed 1, mutant exit 0 / failed 0.
  Output: `…/mut/result_tip.json` (sha256 `7ec836a6…eefd`).
- FIFO probes at the tip runner. Each fixture dir holds a copy of `01` plus case
  `[git_init, fifo <name>, git_commit]`, run with `--timeout 5`:
  - `.gitattributes`: rc 1 after 5.07 s, reason "setup command timed out: git --git-dir=…".
  - `.gitignore`: rc 1 after 5.07 s, same reason.
  No git processes were left (`pgrep`). Outputs: `…/probes/attr.json`, `…/probes/ignore.json`.
- Dot-named symlink probe: `ln -s <outside>/bad <fixtures>/.evil`, where `bad`'s
  `expected.json` is `{"exit": 99}`. The runner gave **rc 0 with `cases: 1`**: the symlinked case
  was skipped silently. Cause: `scripts/citing_set_selftest.py:681` filters
  `not path.name.startswith(".")` before the symlink refusal at `:521`. Output: `…/probes/dot.json`.
- Resolved silently (not a drop): ConnectSiblingOverlap's `GIT_CONFIG_NOSYSTEM` advisory is now in
  the runner's `GIT_IDENTITY` (:140). Its post-read length check is at :399-403. CriticRoutedDispositions'
  gate-ceiling residual is set at :694 and named at SKILL:847-848.

## Smallest safe corrections (L1 integrates)
1. Lesson `corpus/lessons/round-31.md`: append a "Carried open (round-30 routed defect 2)" paragraph.
   It should name each row above, or at least point to SKILL "Citing-set runner containment — round 31".
2. SCORECARD:943-946: add "deep corpus and `O_NOCTTY` guarded by round counters only". Name
   `document_unreadable` and the four family labels, or point to SKILL:863.
3. SKILL:851: change to "a symlink not named with a leading dot … (dot-named entries are still skipped,
   open)". SKILL:868-870: change "`.gitattributes`" to "`.gitattributes` or `.gitignore`". SKILL:868:
   change to "still surviving at `f1ffb81` and at the repaired runner `5371530d`".
4. Name the possible leaked git grandchild after a gate timeout as open and `[INFERENCE]`.

## Lower-severity extras (not in my item list)
- ReviewHostileContract F1 (`--r`, ambiguous between root and revision) is unnamed. SKILL:838-840's
  rule admits it, and gate argparse then exits 2. LOW, and no committed case uses it.
- The hold-only items N4, N7, N8 and N10-N12 (ReviewHostileContract.md:96-98) are not named in
  round-30 or round-31 text. They were never routed (grep of spotcheck.md finds none), so this is
  not a drop.

## Commands (exit codes)
- `git clone -q <lane> clone && git -C clone checkout -q 92235a0…`: 0.
- `grep -n` over SKILL/lesson/SCORECARD/LOG/PROVINCE/QUALITY for each item label: 0.
- `git diff --stat f1ffb81 HEAD -- scripts/ .ufo/waves/round-30/ .ufo/waves/round-27/`: 0.
- `sha256sum` over the gate, runner and strict checker: 0. The compound shell later exited 2 on a
  missing root `QUALITY.md`, which is harmless.
- `timeout 900 python3 -B mut/mutate_and_run_tip.py`: 0 (16 s).
- `timeout -k 2 120 python3 -B clone/scripts/citing_set_selftest.py --root clone --fixtures probes/<n> --tmpdir tmp/run-<n> --timeout 5`
  gave dot rc 0, attr rc 1 and ignore rc 1.

## Not verified
- Gate-grandchild survival after a runner timeout (not run). I did not build a gate-side FIFO stall.
- I did not run the C1, C2 or strict counters. Other seats own those.
- I checked whether the family labels are still open by blob identity of their scripts, not by
  re-running round-27 probes.
