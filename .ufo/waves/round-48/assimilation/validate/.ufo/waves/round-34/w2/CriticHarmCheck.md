# CriticHarmCheck — round 34 harm check, 1e54c89 to 24a1647

Verdict: no harm found. Range 1e54c89515b0b1f7c9d7d10e6232d15e43320713 to
24a16474ee73e20453f3e1be9d2f33573c5196d9 has 187 files changed, 7363 insertions and 0 deletions.
Axes: operability, freshness. Sandbox: /fast/scratch/hyaku/kake-r34/w2/CriticHarmCheck/
(clone/, wt-base/, wt-head/ detached worktrees, out/ receipts). No tools installed or updated.

## Findings

1. History not rewritten. `git merge-base --is-ancestor 1e54c89 24a1647` gives exit 0. `git rev-list --parents`
   shows a linear chain d08d8de, a2fe31b, 5613071, 9ef758c, 24a1647, each with one parent.
2. Zero deleted lines, both across the range and inside every commit. `git diff --name-status` shows 180 A
   and 7 M, with no D, R or T. `git diff --numstat` gives 0 deletions on all 7 M files: LOG.md +35,
   PROVINCE.md +43, SCORECARD.md +94, SKILL.md +33, corpus/QUALITY.md +71, corpus/README.md +15,
   corpus/SOURCES.md +11. A `git show --numstat` loop over each commit finds no non-zero deletion count.
   The 15 binary rows (`-`/`-`) are all A (bundles, .html.gz, html.tar.xz). There is no deletion to judge.
3. All M edits are appends at end of file except two inserts. One inserts a table row
   (`git diff -U0` hunks): SCORECARD.md @@ -194,0 +195 adds the "Offline link-preview (Open Graph) audit"
   row to `## Capabilities`. It has 6 pipe fields, like rows 189-194. The other inserts S067-S077 after S066
   in corpus/SOURCES.md (@@ -74,0 +75,11). No existing row was edited.
4. No source row status changed. No SOURCES.md line was deleted (finding 2), and no ID is duplicated
   (`awk ... | sort | uniq -d` prints nothing). New rows: S067-S070 and S073 mined, S071, S072, S074 and S075
   rejected with flips, S076 and S077 queued.
   The source receipts frozen at declaration were not rewritten. In `.ufo/waves/round-34/sources/receipts.json`
   at d08d8de vs 24a1647, the S067-S072 entries are equal object for object. S073-S077 are added keys
   (+60 lines, 0 deletions). The stated fetch times fit the commit times: sources at 20:57Z vs d08d8de at
   21:00:16Z, and S073-S077 at 21:08-21:09Z vs 9ef758c at 21:13:49Z (`git show -s --format=%cI`).
5. No axis score lowered. The only score text added is SCORECARD "Axis ratings unchanged (10 → 10,
   saturation line)" and the declaration's "Both owned axes sit at the 10/10 saturation line".
   Nothing was removed (finding 2).
6. No behaviour change in existing scripts. No base script appears in the diff: every scripts/ entry is A
   (link_preview_audit.py, link_preview_selftest.py, scripts/fixtures/link-preview/**). The base scripts
   and fixtures are byte-identical. I re-ran the input-dependent checks, which read corpus directories this
   round added files to, at both revisions:
   - `node scripts/corpus-contract.mjs --json --root .` gives exit 0 at base and at head with findings [].
     knowledgeChecked goes 27 to 28 and lessonsChecked 28 to 29 (link-preview-metadata.md and round-34.md
     both pass the trio and Gate rules). Output: out/cc-{base,head}.json.
   - `python3 -B scripts/citing_set.py --root . --population .ufo/waves/round-26/population.json --ledger
     .ufo/waves/round-27/complete-ledger.json --json` gives exit 1 at both revisions. The same 4
     unadjudicated_citing_pair findings (S003, S005, S007, S018) existed before this round. Only corpusFiles
     (30 to 31) and outsidePopulation (46 to 53, the new S067+ ids sit outside the r26 population) change.
     No new finding. Output: out/cs-{base,head}.json.
   - `node scripts/freshness-sweep.mjs --json --offline --repo .` gives exit 1 at both revisions. Compared as
     sets: unresolved stays 10, newMissing stays the same 2 pre-existing paths (round-29 FieldsAndCounts.md,
     round-33 ScoutPinsFlagAccuracy.md), and drift stays 2. Additions are 2 scanned files and 1 new cited path
     (~/Projects/shokunin/.ufo/reports/round-33/kake.md, from QUALITY.md:649 and round-34.md:67), which
     resolves. The history and armed sections are identical. Output: out/fs-{base,head}.json.
7. Earlier rounds' counters are not regressed. I ran each at `--revision`/`--rev` base and head against
   the sandbox clone, with TMPDIR set to the sandbox. All exit 0 at both revisions, and stdout is identical
   once 40-character and short hashes are masked:
   round-29 c1_quote_truth and c2_matrix_count; round-30 c2_quote_truth; round-31 c2_quote_truth and
   c2_strict_checks; round-32 c2_retained_count; round-33 c2_pin_count, c1_code_probe and
   c1_strict_supplement (out/prior/*). The first round-32/33 attempt with `--root/--revision` was a usage
   error (exit 2) at both revisions. It was rerun with `--rev/--repo`, which gave exit 0.
8. Round-32 declared-time criterion (QUALITY.md:548-553): `declared_time_check.py --rev 24a1647 --section
   "Round 34 — declared claims (before implementation lands)"` prints "no stated time" with exit 2, the same as
   the round-33 section. The rule is conditional ("A declaration that states the time it was declared"),
   so this is not a violation. The tool does not read the prose "Sources were opened at 20:57Z", which I
   checked by hand in finding 4.
9. Tradeoff, not harm: the range adds 2,628,590 blob bytes, about 3x the whole round-33 tree
   (882,968). The largest are S074.txt, a full Telegram Bot API page kept for a rejected row (494,103 bytes),
   and ds4cc-7fc6aa2f/html.tar.xz (498,180 bytes, the C2 census input). Retaining S074 bytes is what makes
   the rejection checkable. Smallest correction, if the L1 wants it: none required. The L1 may note retained
   size per rejected source as a future cap.

## Not verified
- I did not run round-30 c1_reason_count.py, because it writes to fixed /fast/scratch/hyaku/kake-r30 outside
  my sandbox. I did not run round-31 c1_sandbox_probes.py or the existing script selftests (scripts and
  fixtures are byte-identical, and the citing-set selftest writes under kake-r27 scratch). I did not run
  the freshness-sweep live sections (owned-site ban).
- I did not judge the truth of the new prose, the C1 and C2 counters, or the wave-1 reports. Those are
  other seats.

## Commands (all exit 0 unless stated)
`git log --oneline`, `git diff --name-status|--numstat|-U0|-U1|--stat`, `git merge-base --is-ancestor`,
`git rev-list --parents`, `git show --numstat` per commit, `git show -s --format=%cI`, `git ls-tree -r -l`
(lane, read-only); `git clone -q` and `git worktree add --detach` (sandbox only). corpus-contract exit 0/0,
citing_set exit 1/1, freshness-sweep --offline exit 1/1, nine earlier-round counters exit 0/0,
declared_time_check exit 2 (no stated time).
