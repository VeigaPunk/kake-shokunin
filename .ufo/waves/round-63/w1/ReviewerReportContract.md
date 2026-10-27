# ReviewerReportContract — marker-rule checklist for the round-63 kake report

Scope: pre-compute the checklist a marker-rule judge applies to the round-63
report at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-63/kake.md`
(prompt §4 `kake-round-63.md:99-129`), with the current evidence pointers a
grader can re-check now. Source of truth: the committed round-63 prompt,
contract `.ufo/waves/round-63/contract.md`, and the r61/r62 report skeletons
(which the prompt keeps identical). Author-side review; no verdict here
admits anything.

## A. The marker rule itself (verdict logic)

Prompt `.ufo/prompts/kake-round-63.md:121-129`: a contentless report —
placeholder text, missing required sections **other than** Sources &
frontier and Trend verdicts, or no evidence pointers — counts the round
**failed** (driver relaunches). A report naming real committed work that
skips Sources & frontier / Trend verdicts is `ok` + a minimum-content
conformance defect. So the judge's first gate is binary:

1. All six required headings present **in this order** (r61/r62 filed
   skeleton): `## Work performed` → `## Landed changes` →
   `## Before → after measurements` → `## Sources & frontier` →
   `## Trend verdicts` → `## SHONEN`. Title line above them (r62 used
   `# Kake — round 62`; r61 `# kake round 61 — report`).
2. Report names real committed work (claims C1/C2 + landed paths) and every
   bullet carries a resolvable evidence pointer (`path:line`, command
   output, or commit hash) — `kake-round-63.md:104-106`.
3. `grep -c '^## SHONEN' <report>` must print `1`, followed by one
   `[x]`/`[~]`/`[ ]` line per SHONEN.md box — pre-commit gate,
   `kake-round-63.md:472-473`.

## B. Required-content checklist (what each section must contain to pass)

| # | Check | Must contain (contract cite) | Current evidence pointer / status |
|---|---|---|---|
| 1 | Claims named up front | Work performed opens by naming the declared claims (1–3) and target axes (§4:104). Expect exactly two: **C1 calibration** (lowest owned axis 2/10 — repair falsified counter family; S432 disagreement resolved as `collapsed-only`) and **C2 operability** (HOLD 10 — `scripts/quote_class.py` runs at measured revision). | `corpus/lessons/round-63.md:7-16`; contract `.ufo/waves/round-63/contract.md` §C1/§C2. Both landed in `6d8c52a6`. |
| 2 | Frozen predicates + counter hashes | Frozen predicate sentences quoted/named identically to contract; counter sha256 `bcd16f68…3fc91` (c63_calibration) and `9fcbfad0…f01e` (c63_quote_tool); tool sha `431e75e8…1f14`; ledger sha `5f48e26b…c42d`; base `13d4519818db28cd0aa912e49020659140d7b9fa`; measured `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`. | Verified now: `sha256sum` on all four files matches the contract exactly. |
| 3 | Landed changes tied to LOG entry + commit hash | Every change bullet cites a `LOG.md` entry and the carrying commit; cite only the helper's `landed <hash>` line (§6:413-467). Round commits so far: `6d8c52a6` (freeze+counters+tool+correction), `05b0d7f4` (tool cwd fix + freeze-note), `7f77d12b` (after receipts), `15eb965c` (w1 spec/dispatch). Integration + wave evidence + report commits still pending. | `git log --oneline` at tip `15eb965c1d0f23ce2a522c651e9306a0952da7d3`; LOG.md has **no Round-63 entry yet** (tail ends at Round-62) — L1 must land it before the report cites it. |
| 4 | Before→after, per claim | One block per claim: counting command + measured commit + before/after outputs verbatim (§4:109-110). | C1: `python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision <rev>`; before at base `13d45198`: `disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false` exit 1 (`controls/base-c1.txt`); after at `05b0d7f4`: `…derived=collapsed-only class_match=1 … unresolved=0 met=true` exit 0 (`controls/after-c1.txt`). C2: `python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision <rev>`; before `present=0 selftest=unevaluable met=false` exit 1 (`base-c2.txt`); after `present=1 selftest=4/4 frozen_cases=ok met=true` exit 0 (`after-c2.txt`). |
| 5 | Controls + kill-rule honesty | Report must record the controls: `control-marker-fixture.txt` (old c62 → `met=true` defect on fixture rev `7833be88…`; new c63 → `met=false`), `control-junk-fixture.txt` (`met=false`), and the round-62 defect receipt `.ufo/waves/round-62/controls/counter-false-green-l1.txt`. If any wave attack reproduces a marker-only green on c63, C1 verdict must be `unprovable`, not `met`. | Receipts committed at `6d8c52a6`; no falsifying wave result observed yet (wave settling). |
| 6 | Wave/shape accounting | Round shape named (one v2 wave under `ufo-wave-policy-v2.json`), seat count, role mix, attack share ≥25%, dead seats w/ last error, residual call, round total; L1 holds the planner seat (validator rejects `planner`) (§3:80-97, §6:304-358). | `w1-dispatch.json`: **64 seats, one batch** — executor 15, reviewer 15, scout 10, scribe 8, critic 6, mutation-tester 5, connector 2, sentinel 1, simplifier 1, revenger 1; attack roles 26/64 (40.6%). `w1-results.json` not yet present; 26 seat reports in `w1/` at read time. Dead-seat list must come from the results handoff, never invented. |
| 7 | Sources & frontier | `SOURCES.md` rows before→after, rows added by tier, rows touched old→new, frontier rows advanced; **both census outputs pasted with exit codes** (§2b:54-66); assimilation line (`Assimilation: none` per `round-63.md:49-51`); considerthese disposition (proposal 2 rejected, `round-63.md:43-48`). Sourced-claim evidence: S432 re-open record (URL, 2026-10-27 access date, ≤25-word located quote) — `round-63.md:53-59`. | Start census: 171 rows, 16 W04, exit 0 (`round-63.md:67-69`). End census must be pasted fresh — registry still 171 (`git show 6d8c52a6` touched no `corpus/SOURCES.md`; no-harm forbids row edits). Expect 171→171, none/none/none, exit 0. |
| 8 | Trend verdicts | Exactly three verdicts — `expansion`, `quality`, `discernment` — each one of improved/harmed/unchanged/unprovable-but-better, with evidence, no scalar (§4:116-117). | Honest precompute: expansion `unchanged` (no new knowledge entry/capability beyond the tool; registry flat) or `improved` only if a capability row for `quote_class.py` is argued; quality `improved` (S432 dispute resolved with blob-derived class + new criterion `QUALITY.md:1414-1416`); discernment `improved` (outside Disagree learned and resolved). A `harmed`/`unprovable` must be reported if wave attacks land. |
| 9 | SHONEN — one line per box | 4 lines matching `SHONEN.md:5-8`; `[x]` only with a named non-author verifier — **none is bound this round** (all 64 seats are lane-dispatched, author-side), so any `[x]` is an over-claim defect. `[~]` needs a resolvable pointer; `[ ]` if untouched. | `SHONEN.md` itself unmodified (not in `6d8c52a6`/`05b0d7f4`/`15eb965c` diffs). Likely honest marks: box1 `[ ]`, box2 `[~]` at most (tool+selftest is arguably not an end-to-end domain task — r62 filed all `[ ]`), box3 `[ ]`, box4 `[ ]`. |
| 10 | Stale-lane line | A line beginning `Stale-lane:` — respawn-per-round driver; no other lane mission open (§6 item 6:481-482). r62 form: launch/progress timestamps + "No other kake mission is open." | Required; trivially satisfiable. |
| 11 | Tool installs | Line recording installs/updates (tool, version, channel, reason) or `none` (§6:483-485; RULES.md). Pacman paused host-wide — any pacman transaction in the round is a defect. | Expected `no tools installed; no pacman` — consistent with nothing under `.ufo/waves/round-63/` recording one. |
| 12 | Frontier duties | Mined-mistake pointer (`corpus/lessons/round-63.md` §Mistakes: false-green class row exists, :18-22); inherited-state naming (earlier attempts — `.ufo/watchdog.log` `lane-dead-no-report kake round=63` check); misroot-sweep note (`git -C /home/vgpnk/Projects/shokunin status --porcelain` before report). | `## Mistakes` row present in lesson. Untracked wave files `w1.ready*`/`w1/` await the wave-evidence commit — Landed changes must name it. |
| 13 | SCORECARD/LOG rows | §2:22-23 — per claim in SCORECARD: score delta, evidence pointer, counting command, measured commit; motivating evidence appended to LOG.md. Report's Landed changes cites both. | **Not yet landed** — `SCORECARD.md` has no round-63 section and `LOG.md` tail is Round-62 at tip `15eb965c`. Blocking gap; the report cannot pass item 3/13 until integrated. |
| 14 | Pre-report gates evidence | `git ls-remote origin refs/heads/master` printed the final lane hash before the report commit (§6:468-471); report commits via `fleet-commit.sh --as kake`, landing last and citing the pushed lane hash. | Judge re-checks by comparing the cited hash to lane tip. |
| 15 | Separability + no-harm statements | One line each: C1 never gates on `scripts/quote_class.py`, C2 never reads C1's ledger (contract §Separability); append-only edits, S432 row cells untouched, r62 held block preserved verbatim, c62 counter/receipts retained (contract §No-harm). | `git show 6d8c52a6 --stat`: 19 files, all additions; `response-header-expectations.md:218-220` r62 block preserved above `:222` r63 block; `SOURCES.md` not in diff. |

## C. Current verdict-relevant facts (re-derivable now)

- All four frozen sha256s match the contract (checked 2026-10-27):
  `c63_calibration.py` `bcd16f68…`, `c63_quote_tool.py` `9fcbfad0…`,
  `quote-classes.json` `5f48e26b…`, `quote_class.py` `431e75e8…`.
- Both commits resolve: base `13d45198`, measured `05b0d7f4` (lane tip
  `15eb965c`; report-integration commit still pending).
- Receipts exist and match the frozen predicates byte-for-byte on their
  key fields (`after-c1.txt` `met=true` exit 0; `after-c2.txt`
  `selftest=4/4 met=true` exit 0; both bases exit 1; both fixtures exit 1
  under c63).
- Not yet landed at read time (must exist before the report can pass):
  `w1-results.json` + dead-seat accounting, end-census paste, SCORECARD
  round-63 row, LOG.md Round-63 entry, wave-evidence commit, the report
  itself, and the final `landed <hash>` citation.

## D. Judgment binding

This seat judged on **calibration**. The checklist above is
conformance-only: sections 7 and 8 are conformance items, not marker
predicates (prompt :114-125); sections 1–6, 9 are the marker rule's
contentless conditions.

Seat bounds honored: read-only against fleet root and lane; wrote only this
file. No commits, no git/jj mutations, no subagent dispatch, no tool
installs, no scratch fixtures.
