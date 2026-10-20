# Round 21 — Knowledge and author-lesson populations (Population seat)

Scope: read-only derivation. Base `5009ecaa1cce10b895617a585ddd3f7c7c923a84`. No corpus file edited. Only this report written.

## Result

| Population | Count | Rule |
|---|---|---|
| Knowledge entries (C1) | **21** | every `corpus/knowledge/*.md`; `freshness-pins.json` is not a `.md` entry and is out |
| Author lessons (C2) | **15** | `corpus/lessons/round-*.md` minus names matching `aggregator`, `verifier`, `spotcheck`; `round-19-recensus.md` is included |

Explicit lists:

Knowledge (21):
crawl-scope-per-host, drift-detection, fire-journal-codes, fleet-registry, free-read-verbs, freshness-sweep, ghp-custom-domain, ghp-etag-anatomy, ghp-served-set, ghp-subpath-spotcheck, keeper-timer-inert, kimi-subpath-audit, mirror-pitfalls, ops-automation, origin-repos, probe-delta-alerting, publish-channels, publish-queue, sitemap-orphan-audit, speedrun-pipeline, vault-properties (all `corpus/knowledge/<name>.md`).

Lessons (15):
round-1, round-3, round-4, round-5, round-6, round-7, round-8, round-9, round-10, round-12, round-16, round-17, round-18, round-19-recensus, round-20 (all `corpus/lessons/<name>.md`).

Excluded from `corpus/lessons/` (8 of 23): round-1-aggregator-audit, round-4-aggregator-audit, round-5-aggregator-audit, round-5-aggregator-mirror-pathless-cli-invocation, round-6-aggregator-audit, round-8-aggregator-box3-coldrun, round-9-aggregator-corpus-verdict, round-20-verifier-spotcheck.

## Agreement checks (all read-only)

- Directory counts: `corpus/knowledge/*.md` = 21; `corpus/lessons/round-*.md` = 23; no subdirectories, symlinks, or dotfiles in either tree.
- Base commit `5009ecaa…`: `git ls-tree` gives the same 23 lesson names and 21 knowledge `.md` names as the working tree.
- `.ufo/waves/round-21/initial.json` `knowledge` (21) and `lessons` (15) sets equal the derived sets exactly.
- `.ufo/waves/round-21/wave1-spec.json`: items Knowledge01–21 target the 21 knowledge names; Lesson01–15 target the 15 lesson names; sets equal the derived sets.
- Working tree vs base: no added or removed files. Four knowledge/corpus paths are modified (` M`): `corpus/SOURCES.md`, `corpus/knowledge/keeper-timer-inert.md`, `corpus/knowledge/ops-automation.md`, `corpus/knowledge/origin-repos.md`. These are in-flight edits by other seats; they do not change either population.

## Planned-command defects found

1. **SCORECARD lesson command (SCORECARD.md:30) includes an excluded file.**
   `ls corpus/lessons/round-*.md | grep -v aggregator | xargs grep -l '^## Gate' | wc -l`
   - Its input population is 16, not 15, because `round-20-verifier-spotcheck.md` matches `round-*.md` and does not contain `aggregator`.
   - It prints `1` today, which is numerically the same as the correct answer only by coincidence (round-20 is the sole gate file in both populations). The "Before 1/15" denominator in SCORECARD does not match the command's own 16.
   - Corrected command (run, output `15` and `1`, `corpus/lessons/round-20.md`):
     `ls corpus/lessons/round-*.md | grep -Ev 'aggregator|verifier|spotcheck' | xargs grep -l '^## Gate$' | wc -l`

2. **Naive `spotcheck` exclusion would drop a knowledge entry.** `corpus/knowledge/ghp-subpath-spotcheck.md` is a knowledge entry, not a verifier spotcheck. Filtering knowledge with `grep -Ev 'spotcheck'` yields 20 (wrong). The knowledge population has no exclusion rule and stays 21. The SCORECARD knowledge command (`Path.glob("*.md")`) yields 21 and is correct.

3. **Gate-heading pattern is a prefix match.** `^## Gate` (without `$`) also matches `## Gated steps …` in `corpus/lessons/round-8-aggregator-box3-coldrun.md:31`. That file is excluded, so no count changes, but `^## Gate$` (or `^## Gate( |$)`) is the safer heading test. Current heading state in the 15 lessons: only `round-20.md` has a gate heading (line 41 exact `## Gate`, line 182 `## Gate — round-20 resume`). The other 14 lack it, so the before-state is 1/15 under the corrected population.

4. **Knowledge command reads `round-19-recensus` as N/A.** Not applicable to knowledge; noted only so the lesson-side rule is not mis-applied to `round-19-recensus.md`, which is in scope and currently has no `## Gate` heading.

## Limitations

- Counts are from name and directory state at the time of the run, with other seats' edits in progress. Population is name-based; contents of excluded files were not read.
- No tools were installed or updated.
- No verification commands beyond the read-only population and heading checks above were run; no build, tests, or formatters.
