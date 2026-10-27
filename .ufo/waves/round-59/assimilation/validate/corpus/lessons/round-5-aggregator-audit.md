# round-5 aggregator audit — kake-shokunin

- **Round:** aggregator round-5 (steered 16:47:37), 2026-09-28. Audited state:
  round-5 commit `18537e9` (16:15:02); index/credential/append-only checks also
  run against the current tree (rounds 6–8 landed since: `8755018`, `83d08e4`,
  `9544914`). Method: one read-only reviewer L2 (26 citations re-executed; zero
  probes fired, zero metered ops) + L1 re-run of the major.
- **Verdict (round-5 delta `18537e9`): NOT conformant** — 1 major, 3 minors.

## Major

1. **"Already running" ops layer claimed from unit-file configuration — the
   keeper timer never ran.** `SKILL.md:56-57`: "The fleet is already
   instrumented — … and `webzites-keeper.timer` runs `grokbot tick` daily"
   (framing shared by `corpus/knowledge/ops-automation.md`'s keeper section).
   Observed (L1 re-run + reviewer, 2026-09-28): `systemctl --user is-enabled
   webzites-keeper.timer` → **disabled**; `is-active` → **inactive**;
   `journalctl --user -u webzites-keeper.service -n 3` → **"-- No entries --"**
   (unit installed 09-20 22:33; it has never executed — so the claim was false
   at write time, not drifted); `grep -rn '## 2026-09-2[2-9]'
   ~/Projects/webzites/reports/keepers/grokbot-*.log.md | wc -l` → **0**.
   Contrast in the same commit: `webzites-probe.timer` **is** enabled+active
   with `probe-history.jsonl` growing live — the verification path was one
   `is-active` away. This is exactly PROTOCOL.md's evidence standard: "A status
   command printing configured values is not evidence of capability." The
   probe-timer half of the same sentence **is** verified-true; the defect is
   the keeper half shipping as running. Fix: correct SKILL.md + ops-automation.md
   to "unit installed, timer disabled, never executed" (owning lane, next
   round; P-b sweep across README/LOG/lesson mentions of the daily tick).

## Minors

2. **veigapunk-page flip window wrong** (`ops-automation.md:30-31`, repeated in
   round-5 report, `lessons/round-5.md`, `LOG.md`): claimed "left `violated[]`
   between 09-21T04:14 and 09-22T22:58"; observed from `probe-history.jsonl`
   rows 38/42/43: last violated run **09-21T03:32:06**, first clean run
   **09-21T04:14:50** — the flip predates the claimed window start. Four
   mentions owe one swept correction (P-b).
3. **xsnapshot-app constancy overstated** (`ops-automation.md:40`): "in
   `errors[]` every run since 09-21" — absent from `errors[]` in 7 fleet runs
   09-21T00:42→01:33; constant-E actually starts **09-21T01:34:20** and holds
   through the latest row (membership scan of `errors[]` per row).
4. **`total − ok = violated + errors` formula fails on early rows**
   (`ops-automation.md:25`): 11 of 66 fleet runs (09-20T23:47:43→09-21T01:33)
   carry one unaccounted row (e.g. row 5: 17−12=5 vs 4+0). The formula needs
   its validity window or the missing-state explanation.

## Verified reproducing (re-executed, not restated)

Round-4's README "20 rows" major **stayed fixed** at `18537e9` and HEAD;
README index 1:1 both directions at `18537e9` (8 rows ↔ 8 knowledge files) and
at current tree (11/11); `probe-history.jsonl` semantics + row count, charter-ghp
window, lucario registration-event reading all reproduce; credential sweep
clean (`grep -rn 'op://' corpus/` → 0; `speedrun-pipeline.md` denylist
documents redaction *classes* only — no values); append-only PASS
(`round-1-aggregator-audit.md` → `6b1cd07` only; `round-4-aggregator-audit.md`
→ `ac5ff82` only; `18537e9` touched neither); LOG round-5 entry complete with
resolving pointers. Fleet hygiene sweep adds one INFO: stray U+200B zero-width
space at `corpus/lessons/round-1.md:16` splitting "click/push" (cosmetic,
corrupts exact-match greps; lane-owned file, optional fix).

## Report-conformance note (round-5 report, filed with the integrator)

`.ufo/reports/round-5/kake.md` carries **no SHONEN section at all** (substance
required since round-1 text; the literal-heading rule landed at `c5abaac`
16:16:15, one minute *after* this lane's 16:15:02 commit — heading exempt,
substance not). The report therefore cannot serve as promotion evidence;
SHONEN.md itself is the untouched verbatim 4-box seed.

## Falsification

Major 1 re-checks with the four printed systemctl/journalctl/grep commands; it
flips to conformant-if-repaired when SKILL.md and ops-automation.md carry the
disabled/never-ran state in a committed round. Minors re-check by re-parsing
`~/Projects/webzites/state/probe-history.jsonl` (live file — pin row numbers, <!-- r18 re-census 2026-10-14: ~/Projects/webzites/state/probe-history.jsonl absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
not just timestamps, on re-run).
