# Round-21 w1 Lesson02 — corpus/lessons/round-10.md Gate

## Behavior

- Target: `corpus/lessons/round-10.md` (kake-shokunin).
- Before: 62 lines, no `## Gate` heading (exact-heading check: none present). The file ended with a single newline after line 62.
- Action: appended one blank line plus `## Gate — round-21 retrospective reconstruction` and its sections at EOF (`PUT >62`). Lines 1-62 unchanged; the edit response showed lines 1-62 intact.
- After: 93 lines (31 appended, lines 63-93). Tag changed `#6FC8` → `#6853`.
- Label: "retrospective round-21 reconstruction, not the original round-10 admission". No round-10 gate or candidate ledger existed before this section.

## Gate content

- Candidates reconstructed from the lesson's own sections (lines 10-62): probe-delta detector (admitted with qualification); running-universe rule (admitted with qualification); r5 veigapunk-page correction (admitted as correction); 33/33 commands and 60/60 paths (admitted for the round-10 measurement only; later superseded by r15); two undocumented CLI behaviours (admitted with qualification); citation-drift fixes (admitted with qualification); xsnapshot constancy narrowing (admitted with qualification); 11-row bookkeeping quirk (admitted as observation); cross-lane connector check (admitted as reported by one lane); CDP-9222 lease (unverified, open).
- Rejected, documented reasons only: naive consecutive-row diff (42 events / 40 phantom); r5 transition window (identical `violated[]` sets); "60/60" standing claim (later rejected in r15).
- Admit/reject spot-check: **not recorded.** Other non-author evidence is `corpus/lessons/round-6-aggregator-audit.md` (aggregator L1 non-author review, scout lane, 2026-09-28, round-10 HEAD `dd4eabf`). It flagged the 11/76 identity mismatch (acknowledged in round 10, uncorrected at audit time) and the `/tmp/kake-r10/*` evidence-pointer failure (open at audit time). It did not spot-check the detector, the 33/33/60/60 measurements, or CLI claims. No round-21 non-author spot-check of round-10 admissions is recorded.
- Known limits stated in the section: retrospective; original ledger not recorded; no live-state re-verification or domain recheck; `probe-latest` / `probe-history` not read; S019 is format authority only.

## Evidence basis

- Original lesson sections: `corpus/lessons/round-10.md` lines 1-62 (read complete before edit).
- Contract: `corpus/SOURCES.md:27` (S019 row, `own-work`, grade A; metadata authority only; "Knowledge entries open with source, verified-at and recheck; round lessons record candidates, admissions, rejections and spot-check state"; registration target `corpus/lessons/round-21.md`).
- Gate convention precedent: `corpus/lessons/round-20.md:41-60` (`## Gate` with candidates, admitted/rejected, outside spot-check) and `:182-196` (`## Gate — round-20 resume`).
- Round-10 corroboration cited: `LOG.md:15`, `SCORECARD.md` rows 10-11, `SKILL.md:203-206,224`, `README.md:72-75`, `corpus/knowledge/probe-delta-alerting.md` (lines 3-6, 37-38, 45-47, 88-91), `corpus/knowledge/ops-automation.md` (lines 43-47, 115-119), `corpus/knowledge/freshness-sweep.md:32-34`.
- Later repo artifacts cited as recorded-only: `.ufo/round-20/resume/paths-before.txt:55` (indirect declared-absent cite at `round-10.md:41`).
- Non-author evidence: `corpus/lessons/round-6-aggregator-audit.md` lines 3-4, 17-22, 76-80, 94-97, 129-130.

## Changed files

- `corpus/lessons/round-10.md` — appended `## Gate — round-21 retrospective reconstruction` at EOF (pure addition; no prior byte altered).
- `.ufo/waves/round-21/w1/Lesson02.md` — this report (new).

No other file was edited. No commits. No subagents dispatched.

## Out-of-scope observations

- `corpus/lessons/round-21.md` did not exist when read, so the S019 registration target named in `SOURCES.md:27` is pending. The new gate cites it only by name.
- Source conflict, reported verbatim: `SOURCES.md:27` says the canonical CORPUS.md input is `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md`. Several knowledge entries say `corpus/CORPUS.md (pending L1 registration)` (e.g., `probe-delta-alerting.md` line 2, `ops-automation.md` line 1). The gate follows `SOURCES.md:27`.
- `/tmp/kake-r10/` does not exist at read time (one read-only `ls`). It is not used as a basis, and the gate states the lane reports were not opened.

## Tools installed or updated

None.

## Verification

Not run, per assignment. The edit response showed lines 1-62 intact and the new section at lines 63-93. Main agent should check: the `## Gate` heading is exact, and the diff against HEAD shows zero deletions in `corpus/lessons/round-10.md`.

## Limitations

- Reconstruction only. The gate does not claim any round-10 admission was made or reviewed at the time.
- Admit/reject spot-check not recorded; the only other non-author evidence is one round-6 aggregator audit. No independent round-10 spot-check was found.
- No live-state re-verification or domain recheck was performed.
