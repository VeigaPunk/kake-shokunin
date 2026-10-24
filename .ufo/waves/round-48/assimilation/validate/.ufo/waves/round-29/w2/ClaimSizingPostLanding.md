# Round 29 wave 2 — ClaimSizingPostLanding (critic, leaf)

Item attacked: the round-29 claims C1 and C2 as landed at 7697990cbca20291f3b0367b8ff4220e93b38b03, checked against the Claim sizing, Learning claim and Drift sentinel rules in /home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md:145-176 (read only) and against wave-1 `w1/CriticClaimSizing.md`. Advisory only; the L1 and the closure decide.

## Verdict per rule

| Rule | Verdict |
|---|---|
| Never narrow a target after landing | holds |
| One value, one command over committed bytes | holds (C1 4/4, C2 30/30 reproduced) |
| No universal wording the counter does not enumerate | limit: one new unenumerated universal sentence in SKILL.md, with counterexamples |
| Learning claim: capability shown running and entered in the Capabilities table | broken at 7697990: shown running, not entered |
| Learning claim: admitted knowledge on uncovered ground | holds conditionally (the ground was uncovered; admission is the closure's call) |
| Drift: same axis and surface 3 rounds running | holds for round 29 (risk for freshness in round 30) |
| Drift: same routed defect class 3 rounds running | limit: counter-granularity gaps from wave 1 persist unchanged |
| Drift: run-together tokens in round-29 prose | holds for the pattern scanned |

## Evidence

1. **No narrowing.** The counter blobs are the same at d18bbf3, 9e541a1 and 7697990: `c1_quote_truth.py` 139ede1e…, `c2_matrix_count.py` 58dde062…, `c2-matrix.json` 0687433e…. `git diff --exit-code d18bbf3 7697990 -- <three counter files>` exits 0. The only SCORECARD change after the declaration is the 9e541a1 notes (SCORECARD.md:639-648). They were committed at 07:36:48 -0300, before the first build commit f8675e5 at 07:46:29. The notes add criteria and change no target. The lesson repeats 4/4 and 30/30 unchanged (corpus/lessons/round-29.md:9-18). Its "round-28 routed defect 3" attribution for C2 reason codes is correct, because that defect names both reason codes and quote truth (corpus/lessons/round-28-verifier-spotcheck.md, routed item 3).
2. **Reproduced values** (sandbox clone at 7697990, Python 3.14.8, TMPDIR in the sandbox):
   - `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision 7697990…` printed "C1 4/4 at 7697990…" and exited 0.
   - `python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision 7697990…` printed "C2 30/30 at 7697990…" and exited 0.
   - `python3 -B scripts/base_path_selftest.py` printed "30/30 fixtures passed" and exited 0.
   - Outputs are in the sandbox: c1-7697990.json, c2-7697990.json and selftest.out.
3. **Universal wording added after the declaration:**
   - These "all" statements are enumerated and hold:
     - "all 4 findings … were such sibling links" (SKILL.md:718 and the entry's "Reading a finding" section). summary.json totals 4 findings. All four are `a[href]` links to other veigapunk.github.io projects (real-input/out/charter-ghp.json:15-38, plazir15-ghp.json:15-20).
     - "all three constant gates" is enumerated by the counter.
     - "all four opened" is backed by receipts.json.
     - "all 29 committed fixtures assert only the exit code" (corpus/QUALITY.md:355): there are 29 fixture directories, and 0 of them contain "reason".
   - Not enumerated, and contradicted: SKILL.md:705-707 says "Every root-relative reference in the built HTML therefore points outside the project site unless the build or the template adds the base path." Two counterexamples:
     - A hand-written `/repo/style.css` with basePath `/repo/` is root-relative, yet the lane's own audit returns `clean` with exit 0 (sandbox probe2).
     - A project site on a custom domain is served at the root (S041 "unless a custom domain is specified"; S043 base '/'). The table row at SKILL.md:716 says this itself.
     - Smallest fix: "A reference written for the origin root (such as `/style.css`) points outside a project site served at its repository subpath, unless the build or template adds the base path."
   - Capability wording beyond the counted set: the entry and the tool help claim `audio[src]` and `embed[src]`. No matrix case and no committed fixture contains `<audio` or `<embed`; `git grep` found no matches, and the words appear only in the matrix `interface` text at c2-matrix.json:10. My sandbox probe shows both elements flagged as `outside_base_path`, with exit 1. So the behaviour runs, but it is outside the 30 counted cases. State this as a limit; it is not a defect.
   - Status wording: corpus/README.md (round-29 section) says the ground is "leaving the open list". PROVINCE.md:26-30 keeps it under Frontier. The README states the outcome before the closure has admitted it.
4. **Learning claim, capability path: broken at the attacked commit.**
   - The Capabilities table (SCORECARD.md:187-193) still has three rows: the registry, canonical preflight, and snapshot replay.
   - `base_path` appears in SCORECARD.md only at :626 (the declaration) and :641. Line :641 is the note committing that "C2 enters a SCORECARD Capabilities row in this round."
   - The capability is shown running (item 2, plus the real-input run over 3 sites with 114 references), but the condition also needs the row to be entered.
   - Smallest safe correction: add one Capabilities row, or a "Capabilities acquired in round 29" subsection like round 25's at SCORECARD.md:466. It would name `scripts/base_path_audit.py`, the C2 counter command, 30/30 at the landed commit, and first-working round 29. This adds the declared row and narrows nothing.
5. **Learning claim, knowledge path.**
   - The ground was uncovered: PROVINCE at d18bbf3 listed "Jekyll/base-path build tooling" as open Frontier. At fe1805c, `git grep` for baseurl, base path, basePath and relative_url found no knowledge entry on it. The only subpath material, ghp-subpath-spotcheck.md, covers served-path rot, not base-path authoring.
   - The landed entry has real content: each of the four distinct Gate quotes reappears in the entry body.
   - The counter is unchanged, so wave 1's hollow 4/4 counterexample (sandbox ea8a94e) still applies. Admission therefore rests on the closure reading the body, as the 9e541a1 note asks.
6. **Drift.**
   - Operability moved from scripts/citing_set.py (rounds 27 and 28) to scripts/base_path_audit.py, which breaks the run.
   - Freshness used the "new entry from four sources with Gate quotes" shape in rounds 28 and 29. A third round of that shape would trip the sentinel.
   - Both counters are byte-identical to the declaration, so the granularity gaps from wave 1 remain: C2 does not compare `pagesChecked`, `referencesChecked` or `resolved`, and C1 cannot tell a hollow entry from a real one. If the closure routes counter granularity again, that is three rounds running, and round 30 must work a different frontier area.
   - Run-together scan: `rg -o '\b(round|rounds|review|remains|stays|seats|after|before)[0-9][0-9/]*\b'` over the round-29 added lines found no match (exit 1).

## Commands (exit codes)

- `git clone -q … clone && git -C clone checkout -q 7697990…`: 0.
- c1 counter: 0. c2 counter: 0. selftest: 0.
- Probe 1 (`audio`/`embed`, `--manifest manifest.json`): 1, failed-policy, 2 findings. An earlier attempt with `--json` exited 64 because the flag does not exist.
- Probe 2 (hand-written `/repo/style.css`): 0, clean.
- `git diff --exit-code` on the counter files: 0. The git grep, rg and log reads ran in the lane read-only.

## Not verified

- I did not reopen any source, and I made no network fetch.
- I did not rerun the counters at f8675e5 or 98dbab2.
- I did not read the other wave-1 reports, or every entry sentence against its quote.
- I did not check the report-depth, dead-seat or rejection-streak sentinels; those are closure and L0 metrics.

No installs. The only file written in the lane is this report. Sandbox: /fast/scratch/hyaku/kake-r29/w2/ClaimSizingPostLanding/.
