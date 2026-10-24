# CriticQualityCriteria — round 31, wave 2 (attempt 2): QUALITY "Round-31 criteria"

Seat `KakeR31a2.CriticQualityCriteria`, critic. Target: `corpus/QUALITY.md:488-515` at `92235a0` (blob sha256 `71622b54…`; `git diff --stat fde133a 92235a0 -- corpus scripts` is empty). Sandbox: `/fast/scratch/hyaku/kake-r31/a2-w2/CriticQualityCriteria/` (clone and clone2 at the lane, TMPDIR inside it). Outputs are in `<sandbox>/out/`. No network, no installs, no lane mutation; the only lane write is this file.

## Verdict table

| Criterion | Grounded | Runnable | Would catch the round-30 defect | Output |
|---|---|---|---|---|
| 1. Containment repair backed by one hostile probe per shape | yes: `round-30-verifier-spotcheck.md:250-262` is routed defect 1 (N1-N6); lesson Mistakes row 1 | yes | yes, but only as a sensitivity check. It does not test the criterion's own "one probe per shape" | pre-repair runner: exit 1, 5/5 specs fail. Repaired runner: exit 0, 5/5 pass. **A tree with only P1 also exits 1** |
| 2. Closure command run once before declaring, and names files | yes: `:283-286` is routed defect 6; Mistakes row 2 | yes | **no**: the round-30 directory command passes both steps of the check (exit 0, exit 1) | R30: step 1 exit 0, step 2 exit 1. R31: step 1 exit 0, declared range exit 0, step 2 exit 1 |
| 3. Every seat's end state recorded | yes: `:280-282` is routed defect 5; Mistakes row 3 | partly: the status vocabulary does not fit the committed file | yes at round 30: 15 returned, 20 reports, none listed partial | **R31 w1 fails as written: 13 `returned` against 14 reports not listed as partial** |
| 4. Unmarked narrowing qualifier is marked | yes: `:271-276` is routed defect 3. No Mistakes row in `round-31.md` | partly: "such word" is not enumerated | yes: "lowercase" has 0 hits in S051 and "only" has 0 hits in S049 at `91b60bd` | R31 entry: 24 words flagged. Real gaps: line 39 "must" (0 hits); words that match unrelated text pass; line 67 has no qualifier word to search |

## Commands run (sandbox; exit codes)

- `git clone -q <lane> clone && git -C clone checkout -q 92235a0…` → 0.
- `git -C clone show f80bd8f:scripts/citing_set_selftest.py > runner-f80bd8f.py` → sha256 `9f2d1ecb…`. This equals the runner blob at `f1ffb81` and at `91b60bd`, so the "pre-repair runner" is the round-30 defect runner.
- `python3 -B clone/scripts/citing_set_hostile_selftest.py --root clone --tmpdir h1 --runner runner-f80bd8f.py` → **exit 1**.
  - P1: canary written. P2 and P3: victim repository changed. P4: timed out. P5: runner exit 0.
  - Output: `out/c1-prerepair.json`.
- The same command with no `--runner` (repaired runner `5371530d…`) → **exit 0**, P1-P5 all pass (`out/c1-repaired.json`).
- An exported tree with the P2-P5 specs deleted (`onlyP1/`), run with `--runner runner-f80bd8f.py` → **exit 1** (`out/c1-onlyP1-prerepair.json`).
- `git -C clone2 diff --quiet …` (full transcript `out/c2-closure.txt`):
  - Round-30 command `4580c78 4580c78 -- …round-30/sources/ …fetch_sources.py` → 0.
  - Any path, including `no/such/path/`, compared against the same revision → 0. Step 1 is vacuous: `git diff X X` always exits 0.
  - Round-30 command `4580c78 91b60bd` → 1. This is the real round-30 defect.
  - Round-30 command against a sandbox commit that appends to `S049.txt` → 1. Step 2 passes.
  - Round-30 command against a sandbox commit that adds `sources/screened/x.txt` → 1. Only this probe exposes the defect, and the QUALITY check does not include it.
  - Round-31 command (`SCORECARD.md:886`), `a16602a a16602a` → 0.
  - Round-31 command, `a16602a 92235a0` → 0.
  - Round-31 command against a sandbox commit changing `S057.txt` → 1.
  - Round-31 command against a sandbox commit adding `screened/x.txt` → 0.
- Seat count, Python over `.ufo/waves/round-31/w1/seat-status.json` (sha `e6acc874…`) → 0 (`out/c3-seats.txt`).
  - Counts: dead-at-spawn 18, returned 13, refused 1, returned-after-safety-filter 1.
  - 14 member reports, and 14 `.md` files on disk. No report starts with `PARTIAL:` and no partial list exists for round 31.
  - Round-30 wave 2: `partial-reports.json` lists 15 complete and 5 partial for 20 reports, so the check holds after the fix.
  - At `91b60bd`, `git ls-tree` shows no `seat-status.json` or `partial-reports.json`.
  - The round-30 `swarm-registry.json` has no `status` field on any of its 34 members, so "15 returned" exists only in the L1's prose.
- `python3 -B qualifier_scan.py clone corpus/knowledge/render-web-services.md` → 0 (`out/c4-r31-scan.txt`; script at `<sandbox>/qualifier_scan.py`). The scan strips curly-quoted spans, `[INFERENCE]` text and backticks. It then counts each of 17 narrowing words in the retained text of the sources cited on that line.
- Context reads: `grep -oiE` on S057, S058 and S060, plus `git -C ~/Projects/ds4cc-marketplace show 1fbdb8ed:render.yaml` and `:.dockerignore` → 0 (`out/c4-context.txt`, `out/c4-line67.txt`).
- Round 30: `git show 91b60bd:…/S049.txt` and `S051.txt` give 0 hits for "lowercase" and 0 for "only" (`out/c4-r30.txt`).
- One no-op: my first attempt to run both selftests in parallel ran the second subshell in the session cwd. Its redirect to `/home/vgpnk/Projects/shokunin/out/` failed, so nothing ran, and `ls` confirmed no directory was created. I reran it inside the sandbox.

## Findings

**F1, criterion 1 (medium): the check does not test what the criterion asks.**
- The check is "exit 1 against the pre-repair runner". With 4 of the 5 specs deleted it still exits 1, so a repair that names five shapes but ships one spec passes the check.
- The check also never runs the selftest against the repaired runner.
- Smallest correction:
  - Require `passed: false` per spec on the pre-repair runner.
  - Require exit 0 on the claimed runner.
  - Require the spec count to equal the shapes named in the commit (here 5: P1 to P5 for N1, N2, N3, N5, N6).
- The harm list in the criterion ("code ran, repository changed, hung") omits the N6 harm, a vanished case. The selftest covers it anyway: P5 fails when the symlinked case is not a failure.

**F2, criterion 2 (high): the check cannot fail on the defect it was written for.**
- Step 1 (both revisions equal) is a tautology for `git diff --quiet`.
- Step 2 (change a named file, expect exit 1) passes for the round-30 directory command too.
- The round-30 failure was a legitimate addition under a pinned directory. Only "names files, not a directory" in the criterion's prose catches it, and the check never probes that.
- The L1's own `verification/closure-command-check.txt` lines 4-5 contain the right probe: add a file under the pinned parent and expect exit 0. QUALITY does not require it.
- Smallest correction: replace step 1 with "add an unrelated file beside the named paths in a sandbox commit: exit 0 expected", and add "no path argument names a directory".

**F3, criterion 3 (medium): the round's own wave 1 fails the check as written.**
- `seat-status.json` uses a fifth status, `returned-after-safety-filter` (CriticSandboxThreatModel), which is outside the criterion's four statuses. 13 ≠ 14.
- The criterion says partial reports are "listed". The lesson (`round-31.md:70`) says they start with `PARTIAL:`. Those are two mechanisms, and the check reads only the first.
- Count equality can also hide a swap: a dead seat with a report offsets a returned seat without one.
- The attempt-1 wave 2 (`w2-spec.json`, `w2-dispatch.json`, never dispatched) has no `seat-status.json`. [INFERENCE] This is acceptable only if "each wave" means dispatched waves; the criterion does not say so.
- Smallest correction:
  - Name the status set, including the safety-filter case or mapping it to `returned` with a note.
  - Accept either a partial list or a `PARTIAL:` first line.
  - Compare the set of returned seats' report files to the set of reports not marked partial, not the counts.

**F4, criterion 4 (low to medium): a word search over the whole retained text gives false passes and misses universals.**
- It would catch both round-30 cases, since both words have 0 hits.
- On the round-31 entry, "must" on line 39 has 0 hits in S060 and is unmarked. The sentence is "a Host header the app must accept", which adds an app obligation the source does not state.
- "only" on line 64 ("Its value lives only in Render") and "many" on line 45 pass on unrelated hits. S057 has 35 hits for "only", and its one "many" is "many popular IDEs". The check passes them without reading context.
- Line 67 is a universal claim with no qualifier word: `domains`, `plan`, `region`, `autoDeployTrigger` and `renderSubdomainPolicy` "keep their current values (S057, quoted above)".
  - S057 states retention for `plan`, `autoDeployTrigger` and `renderSubdomainPolicy`.
  - For `region` it says "You can't modify this value after creation" and gives the default `oregon`.
  - For `domains` the retained text states no omission rule (`out/c4-line67.txt`). That part of the claim is unmarked and unsupported.
- Smallest correction: search within the cited quote's sentence rather than the whole page, enumerate the words (only, always, never, every, all, must, lowercase, each), and extend the rule to claims made over a list of keys.

**F5, grounding (low).** The section header cites `round-31.md` "Mistakes" as ground for all four criteria. Criterion 4 has no Mistakes row, and the Mistakes row "dead route not planned for" (`round-31.md:71`) has no criterion. All four routed-defect line ranges are exact.

## Not verified

- I did not run `c1_sandbox_probes.py`, the C2 counters, the gate selftest or any live fetch.
- I did not judge the entry's other sentences beyond the qualifier scan, which other seats own. Line 61's `.dockerignore` wording was read but not adjudicated.
- I did not check whether S057 says anything about `domains` omission outside the retained visible text.
- No tool was installed or updated.
