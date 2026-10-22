# KakeR33.CriticDeclarationCorrection — is the SCORECARD declaration-time correction complete?

Verdict (advisory): **incomplete, with specifics.** What the correction states is accurate. But it reports the
screening of C2 inputs as narrower than it was. Neither counter became easier to satisfy.

Target: 0a0acfb:SCORECARD.md:1137–1143 ("Declaration time" bullet under "Corrections and limits found by wave 1").

## Accurate parts (each checked)
- The committer time of bc6c4a8 is 19:52:44Z, and the author time 16:26:05 -03:00 is jj's change-creation time.
  The lane `jj --ignore-working-copy op log` shows op 6021563dc952 (16:26:05) and then no operation until
  3e322d241d4b (16:52:43.910). The commit op d66a8b570f9e ran at 16:52:44.006.
- Upstream clone at 19:49:58Z: the reflog entry in ds4cc-upstream/.git/logs/HEAD has epoch 1792698598, and
  `date -u -d @1792698598` gives 2026-10-22T19:49:58Z. The clone command started at 19:49:55Z (directory birth 16:49:55.20).
- At 19:52:01Z the L1 ran `scripts/canonical_audit.py` on two of the three pages, with verdict clean. W1 marked
  this as [INFERENCE]. The L1 transcript now proves it:
  ~/.omp/agent/sessions/-Projects-shokunin/2026-10-22T17-34-59-437Z_01a164ae-2f6d-7232-aa84-10d4c104a0ef/KakeR33.jsonl
  line 77 is the command (manifest with /magga/frostbite/ and /classic/). Line 79 is its output:
  `{"findings":[],"pagesChecked":2,"verdict":"clean"}`, exit=0.
- "No counter had run": confirmed. I extracted every L1 tool call before 19:52:47Z (sandbox copy
  l1-predecl-calls.txt). c1_code_probe.py was written at 19:51:50Z (line 74) and c2_pin_count.py at 19:52:28Z (line 80).
  Neither was invoked before the commit (line 83). The first runs are at 19:52:51Z (line 86). The L1 ran nothing for
  C1 before the freeze. It only read the round-32 probe and the runner's guard code (line 65). The C1 "reworded
  fails" before value was a known round-32 result, as w1 said.
- The declaration text is unchanged: `git diff bc6c4a8 0a0acfb -- SCORECARD.md` has no removed lines.
  The counters are unchanged: `git diff --stat bc6c4a8 0a0acfb -- <both counters>` is empty, exit 0.

## Incomplete: what the correction leaves out
1. At 19:50:57Z (transcript line 68; result at line 70), about 107 s before the freeze and before the auditor run, one L1
   command read every fact that C2's c1 and c4 conditions later count:
   - the four pinned blob ids (`git ls-tree`): 67d8c7a5, e0d9ee29, 12c58e2d, 4e6d70ae. These are the PINNED values
     at c2_pin_count.py:44–49.
   - the sitemap `<loc>` counts: 100 at 7fc6aa2f and 97 at 1fbdb8ed. 100 is the `sitemap-locs: 100` that c4 checks
     (corpus/knowledge/sitemap-orphan-audit.md:203).
   - the `<link rel="canonical">` of **all three** pages, including remastered. Each points to its own URL, which is
     what makes all three verdicts clean (sitemap-orphan-audit.md:204–206).
   The declaration's "sitemap.xml +3 locs" discloses only the change in the loc count. The correction lists only the
   clone and the auditor run, so it suggests the remastered page and the loc count were not looked at before the freeze.
2. The 19:52:01Z probe saved the bytes of all three pages under /fast/scratch/hyaku/kake-r33/probe/; its manifest
   names only two. Births are all 16:52:01.45 (`stat %w`). The remastered page is 16494 bytes, and its manifest
   (/fast/scratch/hyaku/kake-r33/m.json) was born at 16:58:41, after the freeze.
3. Minor: at 19:49:22Z (line 52) the L1 ran `git ls-remote origin HEAD` on the local ds4cc checkout's GitHub remote.
   This was the first look at the upstream drift, before the clone. It was a GitHub read, which was allowed.

## Did the screening make either counter easier to satisfy? No.
- c4 compares what the section states with what the counter observes, for any verdict and any loc count
  (c2_pin_count.py:150–172). `grep -n "clean\|\b100\b\|\b97\b" c2_pin_count.py` finds nothing (exit 1): the counter
  hard-codes no verdict and no count. The pinned ids are upstream facts. I re-read them with `git ls-tree 7fc6aa2f`, and all four match.
- Counterfactual (sandbox commit 9c262a75). I changed the retained remastered page's canonical to point at the wrong URL,
  stated `failed-policy` in the section, and set PINNED to the new blob 80dd79f7 in a sandbox copy of the counter.
  `python3 -B ../c2_cf.py --rev 9c262a75… --repo .` exit 0 gave **met 4 of 4**, remastered observed failed-policy and
  stated failed-policy. So met 4 is reachable whatever verdict the screening would have shown. The frozen counter on
  the same commit (exit 0) gave met 2: c1 and c4 fail on the changed bytes, as they should.
- C1 had no screening runs, so there is nothing that could have made its counter easier.
- What the screening did do: the L1 chose C2's scope (three pages and four paths) after seeing upstream. This is
  claim selection, not making the bar easier, and the declaration already discloses it in part.

## Smallest safe correction (append; leave the declaration text unchanged)
Add to the "Declaration time" bullet: "The screening also covered, at 19:50:57Z, the four pinned blob ids, the sitemap
loc counts (100 at 7fc6aa2f, 97 at 1fbdb8ed) and the canonical link of all three pages. The 19:52:01Z probe saved all
three pages' bytes. So every fact that C2's c1 and c4 count was known before the freeze. c4 compares stated with
observed values for any verdict (sandbox counterfactual), so this did not make met 4 easier."
Axes: freshness provenance (low severity), operability (none).

## Commands run (sandbox clone at 0a0acfb; TMPDIR set to my sandbox)
- `git clone -q` of the lane, then `checkout -q 0a0acfb…`, then `git log 5777d5a..HEAD`: exit 0
- `jj --ignore-working-copy op log` in the lane (read-only): exit 0
- `stat` of /fast/scratch/hyaku/kake-r33/* and probe/**: exit 0
- extraction of the L1 transcript tool calls (read-only python3 JSON parse): exit 0
- `git -C ds4cc-upstream show/ls-tree` (loc counts, canonical links, blob ids): exit 0
- `python3 -B .ufo/waves/round-33/c2_pin_count.py --rev 0a0acfb…`: exit 0, met 4 of 4; stated equals observed (100, clean ×3)
- counterfactual runs described above: exit 0, met 4 (sandbox counter copy) and met 2 (frozen counter)

## Not verified
The C1 implementation and the strict supplement. Whether any process outside the L1 transcript touched the inputs.
I did not stat the lane working tree; the counter mtimes come from w1 and the transcript write times.
No tools were installed. There was no network use.

Sandbox files: /fast/scratch/hyaku/kake-r33/w2/CriticDeclarationCorrection/{l1-predecl-calls.txt,
c2-at-0a0acfb.json, c2_cf.py, c2-cf.json, c2-cf-frozen.json}; clone branch cf-nonclean (commit 9c262a75a7289c6f9271281b1d55145c7befde84).
