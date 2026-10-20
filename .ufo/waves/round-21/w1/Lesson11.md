# Lesson11 — round-5 lesson Gate (round 21, w1)

## Behavior
- Target: `corpus/lessons/round-5.md`. Read in full before editing.
- No `## Gate` heading existed, so a historical Gate section was appended at EOF. No gate-completeness review was needed for an existing gate.
- The appended section is a retrospective round-21 reconstruction, labelled as such. It is not the original round-5 admission. Round 5 recorded no Gate, candidate list, or admit/reject ledger.

## File changes
- `corpus/lessons/round-5.md`: old line count **67**; appended Gate is pure EOF addition after line 67, no prior byte changed. Line count after the first append was 150; the follow-up provenance fix (below) replaced the outside spot-check block with a longer block.
- No other corpus file was edited. No commits. No SCORECARD, LOG, QUALITY, SOURCES, README, SKILL, or CORPUS changes. No credential or auth file was read.

## Follow-up fix (TrendDiscernment critic, via IRC)
- The "Outside spot-check" block cited `round-10.md` and `keeper-timer-inert.md` as independent evidence. Both are author-side: `round-10.md` lines 3-5 say the evidence was delegated read-only L2 probes plus L1 self-runs by the same lane, and `keeper-timer-inert.md` is a later in-lane round (r12).
- Fix applied in `corpus/lessons/round-5.md` (block replaced, EOF-only, no pre-existing line touched): outside spot-check now lists only `round-5-aggregator-audit.md` and `round-6-aggregator-audit.md`, followed by "Admit/reject spot-check: not recorded". `round-10.md` and `keeper-timer-inert.md` moved to a separate "Later in-lane corroboration (author-side, not outside)" paragraph.
- The critic's cited line range (138-140) was approximate; the block sat at lines 134-141 of the pre-fix file.
- The critic cited `LEARNING.md:45-46` for the rule "A subagent the lane dispatched is still the lane." LEARNING.md:45-46 confirmed at /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md. The author-side classification above rests on `round-10.md` and that rule.

## Gate contents
- Candidates: the original "The gap closed", "Evidence mined", and "Learned" claims, each with a historically supported outcome (admitted with qualification, refuted, or unverified).
- Rejected: **not recorded**. None were invented.
- Outside spot-check: `round-5-aggregator-audit.md` and `round-6-aggregator-audit.md` only; cited and not newly run. Admit/reject spot-check: not recorded.
- Later in-lane corroboration: `round-10.md` and `keeper-timer-inert.md`, labelled author-side.
- Cites the original sections of round-5.md.

## Evidence basis and limits
- Evidence used: corpus files named above. No live-state re-verification, no probes, no `systemctl`/`journalctl` calls, no webzites tree reads (the lesson's own r18 note records that tree as absent).
- **Round-21 lesson** (`corpus/lessons/round-21.md`): not present in `corpus/lessons/` at edit time. Not cited as evidence.
- **S019 metadata/gate contract**: referenced by `.ufo/waves/round-21/wave1-spec.json` as the metadata authority (L1 to register in CORPUS.md). No S019 entry was found in `corpus/SOURCES.md`, `corpus/QUALITY.md`, or `corpus/README.md`, and no `CORPUS.md` exists under `corpus/`. The gate follows the round-20 `## Gate` shape instead.
- Not checked: whether `corpus/knowledge/freshness-pins.json` (which lists `corpus/lessons/round-5.md`) hashes this file's bytes. Flagged for the main agent.
- Unverified items: the charter-ghp window, repos-r1..r8 primary evidence (absent from the tree), the speedrun-pipeline claim, the keeper-bot "undocumented" claim, and the probe-latest-age and flat-frontier learnings.

## Tooling
- No tools installed or updated. No pacman transactions.

## Checks for main agent
- Confirm `corpus/lessons/round-5.md` first 67 lines are unchanged against `.ufo/waves/round-21/frozen/before/corpus/lessons/round-5.md`, and that the file ends with the "Sources for this gate" paragraph.
- Decide whether `freshness-pins.json` needs a pin update for the appended file.
- L1: register S019 in CORPUS.md; confirm whether `corpus/lessons/round-21.md` should be cited once it exists.
- LEARNING.md:45-46 confirmed at /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/LEARNING.md. No further action needed on that citation.
