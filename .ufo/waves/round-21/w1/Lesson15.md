# Lesson15 — round-9 retrospective Gate (round-21 w1)

Seat: `KakeR21.Lesson15` (scribe, leaf). Shared base `5009ecaa1cce10b895617a585ddd3f7c7c923a84`.
Owned target: `corpus/lessons/round-9.md` only. No commits. No subagent dispatch.

## Target state

- Before: 66 lines, 4,173 bytes, sha256 `b613ce951eb78996c0ecd02ac2c3e21a9850aef48ff68985f7a62b21d39846e2`. No `## Gate` heading existed (grep `^## Gate` → 0 matches). Tag `#203C`.
- After: 198 lines, 12,670 bytes, sha256 `793cbb3df921ab965ae9971aecdec96532bb0493b69d4ee54f91e67330d66388`. Tag `#64AD`.
- Byte preservation: the first 4,173 bytes of the new file hash to the original `b613ce95…`, so the edit is a pure EOF append. Exactly one `## Gate` heading (line 68). File ends with a single newline.

## Change

One `PUT >66:` gap insert: one blank line, then `## Gate` (lines 67–198). Label: "retrospective round-21 reconstruction, not original admission."

## Gate contents and evidence basis

- **Original sections cited:** `Cites` (lines 3–7), `The gap closed`, `What the baseline found`, `Learned`; LOG.md:13 (round-9 entry).
- **Candidates a–m** (13 items): each marked admitted-with-qualification or unverified, with its evidence paths. Corroboration came from `corpus/knowledge/publish-queue.md` (PQ-1, PQ-2, PQ-4, PQ-5, PQ-6, PQ-10, PQ-12, PQ-14 addenda), `knowledge/ops-automation.md:30-33`, `knowledge/kimi-subpath-audit.md:39-41`, and `round-10.md:38` (the `:339`→`:342` maxBuffer pin correction).
- **Rejected candidates:** not recorded. None in the lesson or LOG.md round-9 entry; none inferred.
- **Outside spot-check:** not recorded. `round-9-aggregator-corpus-verdict.md` shares the "Round 9" label but is a different artifact (kake `a209441`, 2026-09-29, rule-10 verdict) and is explicitly not cited as a spot-check.
- **Evidence limits:** verified-at 2026-09-28; nothing re-verified live. Absent sources `r9-publish-queue.md` and `r9-stale-markers.md` are flagged (restore-or-retire). Recheck `ls -l` command given in the section, not run.
- **Contract:** S019 is not registered anywhere under `corpus/` (`SOURCES.md` ends at S018; no `corpus/CORPUS.md`), so it is not cited as satisfied. Round-21 lesson file absent; round-21 wave artifacts (`initial.json:41`, `wave1-spec.json` Lesson15 entry) cited instead.
- **Pre-edit identity:** the sha256 matches `.ufo/round-20/measured-corpus-inputs.json` (measured 2026-10-15).

## Commands run (local only)

- `wc -lc`, `sha256sum`, `dd … | sha256sum` (prefix check), `grep -c '^## Gate$'`, `grep -n '^## '`, `tail -c 1 | od -c`.
- Reads of the target, `LOG.md:13`, `corpus/knowledge/publish-queue.md:1-30`, `corpus/lessons/round-20.md` Gate sections (format reference), `corpus/lessons/round-9-aggregator-corpus-verdict.md:1-11`, and `.ufo/waves/round-21/` artifacts via grep/glob.
- No webzites reports, probes, network reads, or credential/auth files touched. No recheck command run.

## Tools installed or updated

None.

## Findings and open items

1. S019 metadata contract is referenced by the round-21 spec but unregistered in the corpus at this time. L1 must register it (or the reference must be retired) before the Gate's S019 line can be treated as satisfied.
2. Two cited report files are absent from the webzites tree per corpus annotations: `r9-publish-queue.md` and `r9-stale-markers.md`. Operator must restore or retire those citations. `dead-slot-recreate-readiness-r9.md` and `sentinel-sourceless-extract-r9.md` were not checked; their status is unknown.
3. No independent outside spot-check exists for round-9.md. Any future review of this lesson must be a separate, non-author pass.
4. Checks for the main agent to run after integration: `grep -c '^## Gate$' kake-shokunin/corpus/lessons/round-9.md` (expect 1) and the prefix hash check above (expect `b613ce95…` over the first 4,173 bytes).
