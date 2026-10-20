# Round 21 w1 — TrendQuality: evidence bar for historical metadata repair

Lane: kake-shokunin. Base: `5009ecaa1cce10b895617a585ddd3f7c7c923a84`. Snapshot: working tree at about 2026-10-20 05:56Z, while sibling scribes are still writing. Every count below is a snapshot, not a final state. No verdict: integration owns it.

Scope: define what evidence would show "quality improved" for the knowledge-entry provenance-trio repair (C1), without a domain-live recheck. Nothing was edited. No network reads. No sweep, build or test run. No installs.

## 1. Inputs read

- `corpus/QUALITY.md` rows 9–20 (admission criteria, including the r20-resume rows) and the post-review append-only ruling at lines 31–41.
- `corpus/lessons/round-20-verifier-spotcheck.md`: the spot-check table, and the line-17 per-axis form ("improved-bounded", with the bounds named).
- Supporting: `SCORECARD.md` lines 19–30 (planned claim 1 and its count command); `corpus/SOURCES.md` rows S001–S019; `scripts/freshness-sweep.mjs` (`ABSENT_RE` L122, `PATH_RE` L125, ±2 window L300–330); `corpus/knowledge/freshness-sweep.md` tail (citation-local rule); external format contract `~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` L18–20 and L162–165 (trio rule; S### citation for external sources).

## 2. Definition: evidence sufficient for "quality improved"

The round-20 verifier separates presence from verification. Presence alone is what the SCORECARD count proves: `source:`/`verified-at:`/`recheck:` in the first 8 lines. That is necessary, not sufficient. Quality may be claimed only when every check below passes for all 21 entries, or each exception is named with an owner.

| ID | Requirement | Local observable (no domain read) | Grounding |
|---|---|---|---|
| Q1 | Trio occupies lines 1–3, blank line 4. Count is 21/21 for each key. | SCORECARD count command. Necessary, not sufficient. | SCORECARD L22–25 |
| Q2 | Pure prefix. Every base line survives in order and byte-identical. | `git diff -U0 5009eca -- F \| grep '^-[^-]'` empty for each knowledge file, and `diff <(git show 5009eca:F) <(tail -n +5 F)` empty. | QUALITY L31–39 |
| Q3 | `verified-at:` is the date of the evidence capture the body relies on, not the repair date. Each date in it appears in the entry body or in its SOURCES row. Text never implies a live re-read this round. | grep each `YYYY-MM-DD` in the trio against the body and `corpus/SOURCES.md`. | QUALITY row 2 (old result never presented as current) |
| Q4 | Each `source:` token is either an S### row whose `used-by` includes the file, or a path/command/URL the body already names. No invented S-id. S019 is format authority only and never the first or only evidence. | Check tokens against SOURCES `used-by`. | QUALITY row 4 (admission authority); CORPUS.md L162–165 |
| Q5 | Every `~/` path in the trio that fails a local `test -e` carries, in its own ±2 window, the exact missing target and its dated absence event, and says the cited recipe is historical. Word-only absence matches do not count. | Local `test -e` per token, then check the window text. | QUALITY row 14 (rejects "absence word inside the window" and "annotation beside a still-imperative command") |
| Q6 | No recheck argv is executed by the repair. Any argv against an absent or domain target is labelled historical or operator-authorized-not-run. | Command log of the repair: local-only. | QUALITY rows 2 and 14 |
| Q7 | Each absent substrate has a named owner and a restore-or-retire action, in the entry. | Read each trio. | QUALITY row 3 |
| Q8 | The trio cannot raise a claim's tier. Platform-mechanism claims keep their existing tier; a trio citing S019 does not license platform claims. | Compare trio sources with body claims in publish-channels, publish-queue, speedrun-pipeline, sitemap-orphan-audit, ghp-subpath-spotcheck. | QUALITY row 6 (platform mechanism); SOURCES S019 scope |
| Q9 | Anchor continuity. Every `file:line` pointer into the 17 repaired files is censused old→new (+4 for lines at or below the insert, 0 above). Current pointers get errata; append-only files (LOG, lessons, SOURCES) get tails, never edits. | Census over `corpus/`, `SKILL.md`, `README.md`, `SCORECARD.md`, `LOG.md`, `scripts/`. Snapshot population: 229 raw tokens (freshness-sweep.md 65, publish-channels.md 27, ops-automation.md 20, probe-delta-alerting.md 17, free-read-verbs.md 17, publish-queue.md 15, sitemap-orphan-audit.md 14, fire-journal-codes.md 14, kimi-subpath-audit.md 11, others ≤8). | r20 precedent: `.ufo/round-20/post-review-anchors.json`, `post-review-restoration.txt` |
| Q10 | Append-only: no base byte changes in `corpus/lessons/*` or `corpus/SOURCES.md`. | Same as Q2 on those files. | QUALITY L33–39 |

Trend rule. "Quality improved" requires Q2–Q6 and Q9–Q10 to pass, and Q7–Q8 to pass or name their exceptions. If Q1 passes but Q3 or Q5 fails, the honest claim is freshness presence only. If any of Q2, Q6 or Q10 fails, the claim does not stand as improvement. The round-20 form ("improved-bounded", bounds listed) applies if exceptions remain.

Replayable claim (QUALITY row 2): the integration report must name base `5009eca`, each argv run, and each outcome count.

## 3. Snapshot observations (local, in flight)

- Diff against base, knowledge: 17 files each +4 lines, 0 deletions. The 4 round-20 entries (crawl-scope-per-host, ghp-custom-domain, ghp-etag-anatomy, ghp-served-set) are already committed with trios and are unchanged.
- SOURCES: +1 line (S019 row).
- Lessons: `round-16.md` +105 −1; `round-19-recensus.md` +39; `round-4.md` +24; `round-8.md` +28; `round-21.md` new (out of my scope; not checked beyond the deletion count).
- Count (SCORECARD command, this snapshot): source 21/21, verified-at 21/21, recheck 21/21.
- Local absence probe over trio `~/` tokens: present `~/Projects` (bare). Absent, among others: `~/Projects/webzites/*` (bin/webzites.mjs, scripts/kimi-surface.mjs, src/cli.mjs, src/fleet.mjs, src/probe.mjs, src/reconcile.mjs, src/speedrun.mjs, state/probe-latest.json, state/probe-history.jsonl, fleet/fleet.config.json, fleet/fleet.dedupe-report.md, fleet/kimi-surface-ops.md, repos, reports/keepers/repos-r1.md, docs/SPEEDRUN-PROTOCOL.md, the whole tree), `~/Projects/plazir-15-site`, `~/Projects/ufofsdbeta`, `~/Projects/ds4cc-marketplace/{speedrun,render.yaml}`, `~/.config/systemd/user/webzites-{probe,keeper}.{timer,service}`. Consistent with the r18 re-census (2026-10-14) annotations already in the bodies.
- Date convention split: the 4 round-20 entries use the SOURCES fetch date (2026-10-19). The 17 use original capture dates (2026-09-20 to 2026-09-29), with later re-reads named. Both are capture dates, so both conform to Q3 once the convention is stated; the bar should state it explicitly.
- Working-tree state: the trio prefixes are in place, but no Gate or audit artifact exists yet for Q3, Q5 or Q9.

## 4. Findings (by severity)

**F1 — High. S019 anchor is broken and one trio claims a registration that does not exist.**
- `scripts/corpus-contract.mjs` (the S019 own-work anchor) is absent. `corpus/CORPUS.md` is absent.
- `publish-queue.md` line 1 says "corpus/CORPUS.md registered by L1 this round". At this snapshot that is false.
- The external canonical file `~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` is present and does state the trio rule (L18–20, L162–165). So the format authority exists; the repo-side anchor does not.
- Fix (owner: SOURCES/L1, not this lane): repoint the S019 anchor to the external CORPUS.md sections, or mark the anchor unresolved. Trios should say "format per S019 (external CORPUS.md), not a registered corpus file". Blocks Q4.

**F2 — High. Append-only breach in `corpus/lessons/round-16.md` (Q2/Q10).**
- Base last line `  internal-consistency count). L1 adjudicated each before landing.` has no trailing newline. The appended block adds `\n` to it, so that line's bytes change. Text is identical; bytes are not.
- No byte-identical way to append after an unterminated final line exists. Either the integrator records a named exception (base blob digest, the `\ No newline` evidence, reason), or the append is re-shaped. This is a decision for the integrator. I have not recommended a verdict on it.
- Same check passes for every other file in the set, since the base of the 17 has trailing newlines.

**F3 — Medium. Some absence annotations pass the sweep but fail Q5.**
- `fire-journal-codes.md` trio: verified-at says "script absent per the r20 correction below", and recheck says "script vanished in W7". No dated absence event is named on the trio, and the target appears only on line 1.
- `drift-detection.md` trio: "absent on this host at round-21 audit" names no dated absence event (2026-10-12 `~/Projects` prune, per the r18 census).
- The sweep's word-based window accepts both. QUALITY row 14 rejects them.

**F4 — Medium. Recheck argv is imperative against absent targets (Q5/Q6).**
- Example: `fire-journal-codes.md` recheck line is `test -e ~/Projects/webzites/scripts/kimi-surface.mjs && echo present || echo absent; grep -lE ... ~/Projects/webzites/state/recreate-plazir15-*.json`.
- QUALITY row 14 rejects "an annotation beside a still-imperative command". Each absent-target recheck needs "historical argv; substrate absent since <date>; not executable as a current check", or a "recheck unavailable" form that keeps the field.
- Several drafts already carry this wording in the trailing clause. The argv itself is still imperative.

**F5 — Medium. Source-first ordering (Q4/Q8).**
- `mirror-pitfalls.md` trio line 1: "source: S019 metadata contract (...) — entry evidence: ...". `publish-queue.md` line 1 begins with "S019 (metadata contract only...)".
- S019 is format authority, not evidence. Evidence should come first in `source:`, and S019 goes in a parenthetical.

**F6 — Medium. Anchor census not started (Q9).**
- 229 raw tokens. freshness-sweep.md self-points 65 times, so those move too.
- Brace-form trio tokens such as `~/Projects/webzites/{bin/webzites.mjs,` (drift-detection, free-read-verbs) include `{`, `}` and `,`. They do not match any `pathsMissSet` entry exactly. The `PATH_RE` class admits them, so they may classify as unresolved or as a new miss. That would move the set-equality pin `missSet 55`.
- Integration must run `--section=paths` once after the repair and compare `pathsMissSet`, `unresolved` and occurrence deltas. I have not run it.

**F7 — Low. `drift-detection.md` trio claims "round 21 re-verified no domain or source tree".**
- The claim matches the local probe above. It is still a claim of a check, and no check log exists in the entry or the round artifacts. Q6 requires the local argv to be logged.

**F8 — Low. SOURCES `used-by` does not match the round-20 correction tails (L1-owned, not edited).**
- `publish-channels.md` tails cite S001, S002, S004 and S005. The registry `used-by` for S001 and S002 lists only `ghp-served-set.md`, and for S005 only `ghp-custom-domain.md`. `ghp-subpath-spotcheck.md` tails cite S001 and S005 with the same gap.
- Q4 tests `used-by`, so this will fail for those cites until L1 updates it.

**F9 — Info. Date-text hygiene.**
- `ops-automation.md` and `vault-properties.md` trios mention 2026-10-20 only as a negative ("not a 2026-10-20 domain recheck"). Acceptable. Keep 2026-10-20 out of every `verified-at:` value.

## 5. Verification gaps and limits

- Working tree is still moving. Counts and deltas above are a snapshot at about 05:56Z.
- I read trio lines and diffs, not full bodies of the 17 entries; sibling scribes own those reads.
- `LEARNING.md` and `PROTOCOL-APPENDIX.md` (cited by the external contract) are not in the repo and were not read.
- Local FS probe covers trio `~/` tokens only, not body cites. Body citations are for the paths sweep.
- No network. No domain or fleet read. No sweep, build, test or lint run (main agent's job).
- Installs: none.

## 6. Checks for final integration (main agent; not run here)

1. Q2 and Q10: `git diff -U0 5009eca -- corpus/knowledge corpus/lessons corpus/SOURCES.md | grep '^-[^-]'`, plus per-file `diff <(git show 5009eca:F) <(tail -n +5 F)` for knowledge files. Expect empty, except the round-16 EOF exception if the integrator accepts it.
2. Q1: the SCORECARD count command.
3. Q3: each `verified-at` date found in its body or SOURCES.
4. Q4: each `source:` S### against SOURCES `used-by`; each `source:` path against the body.
5. Q5: local `test -e` per trio `~/` token, annotation text checked by hand.
6. Q9: anchor census script with old→new table; errata tails for LOG/lessons pointers.
7. One `freshness-sweep.mjs --section=paths` run after integration, comparing `pathsMissSet`, `unresolved` and occurrence deltas to the pins.

## 7. Verdict

None. This is the evidence definition and snapshot only. F1 and F2 are blocking decisions for integration. F3 through F6 are repairs owned by the scribes and the integrator. F7 through F9 are notes.

Report path: `.ufo/waves/round-21/w1/TrendQuality.md`
