# Round 21 — Trend: expansion (TrendExpansion seat)

Scope: corpus README coverage map and SCORECARD capabilities/trend lines, read against the planned round-21 claims C1 (knowledge provenance trio) and C2 (lesson `## Gate` sections). Read-only. Only this report was written. No other files, commits, or network reads. No tools installed or upgraded.

## Verdict

**Expansion: unchanged (delta 0).** C1 and C2, as specified, add no domain ground:

- 0 new knowledge entries (21 before, 21 after).
- 0 new coverage-map rows (23 before, 23 after).
- 0 new SCORECARD capability rows (1 before, 1 after).
- 0 frontier items closed.

C1 adds provenance metadata to existing entries. C2 adds retrospective decision sections to existing lessons. Both re-describe ground the lane already holds. Neither moves the frontier.

## Measured ground boundary

| Measure | Value | Evidence |
|---|---|---|
| Knowledge entries (`*.md`, excl. `freshness-pins.json`) | 21 | `corpus/knowledge/` glob |
| Coverage-map rows | 23 | `corpus/README.md:17-41` |
| Entries with a coverage row | 20 of 21 | `vault-properties.md` appears only in Known-gaps prose (`corpus/README.md:53`, `:65`), not in the table |
| Entries with provenance trio in first 8 lines | 4 of 21 | `crawl-scope-per-host.md`, `ghp-custom-domain.md`, `ghp-etag-anatomy.md`, `ghp-served-set.md`, lines 1-3 each, all from round-20 resume |
| Lessons with `^## Gate` | 1 file (2 headings) | `corpus/lessons/round-20.md:41` and `:182` |
| Lane-authored round lessons | 15 | non-aggregator `round-*.md` (16) minus `round-20-verifier-spotcheck.md` |
| Capabilities | 1 (curated source registry) | `SCORECARD.md:189-191` |

## Trend history (trend boundary)

- Round 20 attempt: "expansion unchanged (same domain ground, no new knowledge frontier admitted)" (`SCORECARD.md:132-133`).
- Round 20 resume, as first written: "expansion improved (4 knowledge entries on coverage-map ground new to the lane)" (`SCORECARD.md:180-182`).
- Round 20 post-review ruling, which supersedes the above: "Expansion is the registry capability and crawl-scope-per-host frontier entry only; the other three new entries supersede covered ground" (`SCORECARD.md:221-224`).
- Verifier spot-check agrees on the narrow reading: "expansion improved (narrow: capability + one entry on new ground; three entries supersede covered ground)" (`corpus/lessons/round-20-verifier-spotcheck.md:17`).

So the counted expansion ledger is: one registry capability plus one new-ground entry (`crawl-scope-per-host.md`). The three GHP entries (`ghp-custom-domain`, `ghp-etag-anatomy`, `ghp-served-set`) are corrections of covered ground. They must not be counted as expansion.

Saturation rule (`SCORECARD.md:206-211`): round 21 is not waived by the stagnation nudge, because a capability entered in round 20. If round 21 adds no capability, round 22 should be a frontier or capability move. C1 and C2 add no capability, so the rule fires for round 22.

## Per-claim analysis

**C1 — provenance trio, prefix additions to 17 entries.**
- Expansion delta: 0.
- Honesty constraint: `verified-at` must carry the date of each entry's own evidence, not `2026-10-19`. The four round-20 entries carry that date because their sources were fetched that day. For example, `fleet-registry.md` says "Verified 2026-09-28" (line 5). Its trio must reflect 2026-09-28, or be marked unverified. Using today's date would be a backdated claim.
- `recheck:` lines contain commands. Writing them is not a network read. Running them is out of scope for this round.

**C2 — historical `## Gate` sections, EOF additions to 14 lessons.**
- Expansion delta: 0.
- Contract constraint: a historical gate cannot be contemporaneous. Each must say it is retrospective and that no gate existed at the time. Otherwise it fabricates admissions, which the contract forbids. Any admit/reject a gate records is a discernment claim, not expansion.
- Count command defect: `ls corpus/lessons/round-*.md | grep -v aggregator | xargs grep -l '^## Gate' | wc -l` does not exclude `round-20-verifier-spotcheck.md`. That file is integrator-authored (its lines 2-3) and is protected by "no altering verifier lessons". After landing, the command prints 15 (round-20.md plus 14). Its denominator is 16 unless `grep -v verifier` is added. The SCORECARD baseline "1/15" implies the verifier file was excluded, so the command and the baseline disagree.

## Risks

1. **Mislabeling.** C1 and C2 could be reported as expansion. They belong to freshness, operability, and discernment, and should be ledgered that way.
2. **Honest-date risk.** Stamping `verified-at: 2026-10-19` on entries not re-read that day backdates their evidence.
3. **Gate backfill risk.** Retrospective gates written as contemporaneous "Admitted" would fabricate admissions.
4. **Frontier untouched.** Open ground in `corpus/README.md:88-106` and `PROVINCE.md §Frontier` (canonical signals and JS-rendered canonicals, CWV/CrUX, WCAG 2.2, Jekyll/base-path tooling, Render deploys) remains open. The non-author spot-check remains owed.

## Proposed move

No expansion move is proposed in this seat. Report round-21 expansion as unchanged, and flag round 22 as a frontier or capability move under the stagnation rule above. Separately, flag to L1 (which owns README) that `vault-properties.md` lacks a coverage-map row. This seat did not edit README.

## Checks for main agent (after landing; not run by this seat)

- Trio: the SCORECARD command (first 8 lines, three keys) should read 21/21 for each key.
- Gate count: add `grep -v verifier` to the command, then expect 15 lane-authored gated lessons.
- Unchanged: 21 knowledge `.md` files, 23 coverage-map rows, 18 SOURCES rows, and one capability row.
- Spot-check that every `verified-at` in C1 matches the date of the entry's own evidence.

## Limitations

- Read via grep for headers and the trio, not full-file reads of all 21 knowledge entries or all 15 lessons.
- `round-19-recensus.md` is counted as lane-authored without reading its header.
- `LOG.md`, `PROVINCE.md`, and `SOURCES.md` were not read beyond the cited SCORECARD and README references.
- No `recheck:` command was executed.
