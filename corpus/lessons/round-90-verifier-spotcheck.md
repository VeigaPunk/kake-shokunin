author: hyaku closure (non-author integrator, @m_zfl)
round: kake 90
date: 2026-11-04
report: .ufo/reports/round-90/kake.md
lane_base: 209027f49959e2e2f0e16867a90a7bb38bbcd3f4
lane_head: 7134ef6b2d8cf171c4570672d8e58ba2e4b9e3a8

# Round 90 verifier spot-check — kake (hyaku closure, non-author)

I did not author this round and edited no lane-authored file. I re-ran the
measurements below on committed bytes with plain `git`/`grep`/`awk`/AST counts.
The lane-owned counters (`c90_defects.py`, `c90_gate.py`) and the shipped gate
(`scripts/cache_key_conformance.py`) were **not executed**: their committed
receipts were read and the revision each one measures was checked
(`PROTOCOL.md` §Gate standard, Closure consequence).

## Conformance results

- Report commit `f7a937bed61d57adf03ab93b463b7d89b41fd315`, author
  `kake-shokunin <kake@shokunin.local>` (author date `19:39:05 -0300`,
  committer date `19:42:50 -0300`). It is an ancestor of `origin/master`, and it
  lands before the driver's completion line `19:43:08`. ✓
- Driver digest (copied from the closure prompt; `.ufo/watchdog.log` re-read
  and equal): `2026-11-04T18:55:22-03:00 launch kake round=90 pgid=1707444
  driver=hyaku-inline attempt=1`; `2026-11-04T19:43:08-03:00 complete kake
  round=90; hyaku-inline attempt=1`. One attempt; the report discloses that no
  `lane-dead-no-report` line exists. ✓
- The `## SHONEN` heading appears once, followed by exactly four box lines
  (three `[~]`, one `[ ]`, no `[x]`). `git diff 209027f4 7134ef6b -- SHONEN.md`
  is empty. ✓
- Every cited lane hash resolves and is an ancestor of `master`
  (`git merge-base --is-ancestor <full> master`): `4ee62b18`, `7f6c68f1`,
  `e50c9566`, `79e1aac2`, `a4814f58`, `f6915632`, `7134ef6b`, plus the two
  reference revisions `f62e7954` and `209027f4` — 9/9 ok. ✓
- `jj-lane.sh state` → `branch=master local=7134ef6b remote=7134ef6b ahead=0
  behind=0 tracked=0 untracked=0`; `git status --porcelain` prints nothing.
  `ls-remote origin refs/heads/master` → `7134ef6b…`. No uncommitted round
  work; pushed. ✓
- Prompt `.ufo/prompts/kake-round-90.md`: `diff` against
  `templates/round-prompt.md` lines 1–140 shows only `{{LANE}}`/`{{ROUND}}`/
  `{{FLEET_ROOT}}`/`{{AXES}}` substitutions — the round-level contract (mission
  binding, L2 floor, commit-then-push, push scope, L0 channel) and all five
  child-lane items (report path, commit-before-report, `SHONEN` heading,
  hash-citation rule, lane write scope) are carried verbatim. The hyaku
  addendum §6 and the scratch-discipline §7 follow. ✓
- Wave: `w1-spec.json` `maxLanes=13`, 13 items; `w1-results.json` `seats=13`;
  13 non-empty seat reports under `w1/`. Roles: scout 2, executor 4,
  mutation-tester 2, reviewer 2, critic 1, scribe 1, connector 1 → attack
  seats 5/13 = 38 %, above the 25 % floor; one wave, no residual call. ✓
- **Route-map note (status-neutral, integrator-side).** `MISSION.md` carries
  role *classes* only ("route through the operator's global host model table"),
  which the template §3 repeats. The addendum's last amendment (Amendment 9,
  "all 18 roles → `@m_mim`") does not match the live
  `task.agentModelOverrides` at closure (`reviewer` `@m_zfl`, 17 roles
  `@m_flash`). No claim depends on it: `w1-results.json` records roles, not
  models, and the lane's report states per-seat models were not recorded.

## Per-claim re-check

Base `209027f4`, carriers `7f6c68f1` (C2) and `e50c9566` (C1), tip `7134ef6b`
(`f6915632` + receipts). Freeze digests at `4ee62b18` and at the tip are equal:
`c90_defects.py` `462224f630d4369138af1bf38783b16695b712b85bb46b7b9d2d3c35f05d519b`,
`c90_gate.py` `703b00580391d8546ce238099d8fdba46358797af307cad02169c3828d70ccfa`,
`frozen/c2-population.sha256`
`a57f8985e69ac01bb0d9f0d21f95a2007dad5396421c7cf46d0b0f57c614850c` — the three
values `freeze.md` names. Only `4ee62b18` ever touched the two counters.

| Claim | Reported | Re-check (mine) | Mode |
|---|---|---|---|
| C1 calibration — the three routed round-89 defects close | `open=3 closed=0 met=false` (exit 1) at base → `open=0 closed=3 met=true` (exit 0) at `e50c9566` and `f6915632` | Receipts match line for line: `controls/base-c1.txt` (`revision=209027f4… open=3 closed=0 met=false`, `exit=1`), `controls/after-c1-carrier.txt` (`revision=e50c9566… open=0 closed=3 met=true`, `exit=0`), `controls/final2-c1-at-tip.txt` (`revision=f6915632… met=true`, `exit=0`). Underlying facts re-derived independently (below). | evidence-verified + re-measured |
| C2 operability — behavioural conformance gate | `gate=absent … met=false` (exit 1) at base → `positives=4/4 negatives_refused=57/57 false_admits=0 errors=0 anti_table=ok population=ok met=true` (exit 0) at `7f6c68f1` and `f6915632` | Receipts match: `controls/base-c2.txt`, `controls/after-c2-carrier.txt`, `controls/final2-c2-at-tip.txt`. Gate is behavioural, not a table: 92 clause-tagged hand cases at the tip (70 at the carrier), 120 seeded generated cases decided by its own reference, an install-time-bound audit-hook sandbox. Population pins are 61 subjects = 4 conforming + 57 non-conforming, and all 61 files exist at the tip with matching sha256 (0 missing, 0 drift). | evidence-verified + re-measured |
| Census / knowledge counts | rows 202→205 (A 177→180), knowledge `.md` 77→78, census exit 0, 26→29 × W04 | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 202, 205. Tier-A `awk` filter → 177, 180. `git ls-tree -r --name-only <rev> -- corpus/knowledge \| grep -c '\.md$'` → 77, 78. `sources-census.sh validate --root … kake` → exit 0, `kake ok`, 29 × W04 (`controls/census-before.txt`: exit 0, 26 × W04). | re-measured, matches |

**C1, re-derived without the counter.** The counter is lane-owned and was not
run; its three predicates were checked directly on committed bytes.

- D89-1 (scratch at the lane root): `git ls-tree 7134ef6b --name-only | grep
  baseclean` prints nothing; `.ufo/waves/round-90/inherited/baseclean.out` is
  tracked from `e50c9566` on, sha256
  `4046c204384ccf255f4e8b77fa4aba4ffb9c2167b7794f128fc4497db890f00f` (the value
  the `c90 defects` registry row pins); `ls baseclean.out` → "No such file".
- D89-2 (unreceipted statement): `SCORECARD.md:5554` and `LOG.md:3088` carry the
  appended D89-2 correction naming `f62e7954` and
  `controls/r89-c1-at-f62e7954.txt`, whose line 1 reads
  `C1v1 revision=f62e7954… items=6 open=5 closed=1 met=false`, `exit=1` — and
  the tail corrects the item list ("only item E is closed") that the round-89
  row had contradicted.
- D89-3 (scope column): `S467`'s `teaches` opens `supersedes S463 —`; the S463
  row is byte-identical base→tip (`diff` of the two extracted rows is empty),
  so the filed scope cell was not rewritten (CORPUS.md rule 2).

**C2, re-derived without the gate.** AST count of `hand_cases()` at the tip: 86
`add(` call sites, one of them the `WORKED` loop over 7 examples → 85 + 7 = 92,
equal to the `hand=92/92` line; at the carrier 64 call sites → 63 + 7 = 70,
equal to `hand=0/70`. `frozen/c2-population.sha256` holds 61 entries; the four
conforming subjects (`scripts/cache_key.py`, round-89 `w1/L1/cache_key.py`,
`M33`, `M36`) are the 4 the counter reports admitted, and the other 57 are the
refused population. Carrier receipt line for `M37-absent-name-not-escaped.py`
reads `met=false`, which is the case that falsifies the round-89 "M37 is
equivalent" claim.

**Held-out evidence (not a frozen target, read as reported):**
`integration/heldout-tip.txt` shows 8/8 positives admitted and 57/58 negatives
refused; the single admit is `S09-value-nul-refused.py`, which refuses NUL — a
point the contract leaves undecided. At the carrier the same file class was
admitted wholesale (14/23 ExecStubs, 6/20 ExecSandbox, 7/7 CriticClaims
probes). The hardening that closes those classes landed after the carrier
measurement (`a4814f58`) and was not re-mutated.

## No-harm check

`git diff --numstat 209027f4 7134ef6b` totals 1155 files, 93 218 added,
**0 deleted**. Outside `.ufo/`: 11 files, 918 added, 0 deleted (`LOG.md`,
`PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`,
`corpus/README.md`, `corpus/SOURCES.md`, two knowledge entries, the round
lesson, `scripts/cache_key_conformance.py`). No axis row changed score:
operability 10, freshness 10, calibration 2, all still HOLD, and the SCORECARD
change only appends the round-90 sections. No file was deleted; `SHONEN.md` is
untouched. No owned axis is harmed.

## Spot-check (`corpus/lessons/round-90.md` `## Gate`; 3 admits, 3 rejects)

The three retained RFC bodies were re-opened at the tip. Each digest equals the
row's anchor and the lesson table: `rfc9110.txt` 502 941 B
`21c1cdce…ff47232a`, `rfc9111.txt` 84 477 B `aeb52adb…5302cf3e`,
`rfc8259.txt` 28 360 B `61a5378f…9b4cd2d7`.

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| RFC 9110 §5.5 field values (S466) | admit, A, scope-limited | `rfc9110.txt` line 1579 heading "5.5.  Field Values"; lines 1606–1607 "Field values containing CR, LF, or NUL characters are invalid and dangerous" | agree | Quote is verbatim at the cited lines, 12 words, and the section's MUST ("reject the message or replace each … with SP") supports the gate's CR/LF refusal clause and the advisory NUL case. |
| RFC 9111 §2 + §4.1 construction ground (S467, supersedes S463) | admit, A, scope-limited | `rfc9111.txt` lines 252–253 "and is composed from, at a minimum, the request method and target URI"; lines 258–259 "Caches differentiate these responses by incorporating some of the original request's header fields into the cache key as well"; §4.1 title at line 526 | agree | Both quotes are verbatim (13 and 19 words); §2 composes the key from method + URI + Vary fields and §4.1 names the calculation. S463's match-profile scope is genuinely narrower, so a superseding row (not a rewrite) is the right instrument. |
| RFC 8259 §7 + §8.1 (S468) | admit, A, advisory-only scope | `rfc8259.txt` lines 429–431 "the characters that MUST be escaped: quotation mark, reverse solidus, and the control characters (U+0000 through U+001F)"; lines 485–486 "MUST be encoded using UTF-8" | agree | Verbatim at the cited lines (17 and 18 words); the lesson keeps them on the unscored advisory line, which is the honest reading of a contract that is silent on encoding. |
| "the round-89 contract's byte layout is what RFC 9111 specifies" | reject (proposition) | `rfc9111.txt` §2 lines 251–262; `c2-contract.md` "Canonical key form" | agree | §2 names ingredients only — no separators, escaping or absent marker — and the contract's ingredient list omits the request method §2 requires at minimum. Layout stays an adapter convention. |
| "M37 is equivalent because names are tokens and cannot contain `%`" | reject (proposition) | `rfc9110.txt` lines 1735–1737, `tchar = "!" / "#" / "$" / "%" / …` | agree | `%` is a `tchar`, so `vary: "A%1F"` with the field absent distinguishes M37 from the contract (`a%251f` vs `a%1f`). The carrier receipt records M37 `met=false`, so the rejection is demonstrated, not asserted. |
| "add NUL to the contract's refusal list this round" | reject (row candidate) | `rfc9110.txt` lines 1606–1612 | agree | The RFC allows *either* rejecting or replacing NUL with SP, so the choice changes the contract rather than reading it; routing it (R90-2) is correct. |

New `corpus/SOURCES.md` rows re-opened: S466, S467, S468. Every `anchor` cell
resolves at the stated plain-text line numbers, every `teaches` quote is
≤25 words (12; 13 and 19; 17 and 18), all three rows are `status=mined` with
`used-by` naming the new knowledge entry, and all three are tier A `spec` — no
tier inflation, no `community` row graded A. `S463` stays `mined` with its
filed scope cell intact.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
exited 0 with `kake ok …/corpus/SOURCES.md` and 29 × W04. The three new W04 are
the plain-text RFC URLs shared with earlier rows across scopes; the base had 26.

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| calibration (C1, lowest owned non-retired axis) | improved | All three routed round-89 defects close on committed bytes, re-derived above without the lane's counter: the scratch file is relocated and tracked, both correction tails name a receipted revision, and the construction ground is superseded by a new row with S463 byte-identical. The score stays 2 HOLD, and the frozen counter that measures it is forgeable (author-disclosed; ReviewC1 F1–F4, MutC1, CriticClaims) — routed, not admitted as a sound instrument. |
| operability (C2, capability acquisition) | improved | A behavioural gate exists and runs (`scripts/cache_key_conformance.py`, 581 lines at the tip), with 92 clause-tagged hand cases, 120 generated cases, an install-time-bound sandbox, and a pinned 61-subject population whose digests all still resolve at the tip. The carrier instrument was falsified by the round's own held-out stubs and hardened after the measurement; the tip refuses 57/58 held-out negatives and admits 8/8 positives. The capability row is in SCORECARD and the registry rows are in `SKILL.md` (the lane's registry home). |
| freshness (not claimed this round) | unchanged | No drift claim was made and no freshness receipt was superseded; the three new rows carry `recheck 180d` and the knowledge entry carries a dated `recheck`. No score moved, and no stale entry was left unmarked. |

## Trend verdicts

- **expansion: improved.** `corpus/knowledge/` 77 → 78 (`.md` count command
  above) with `cache-key-conformance-gate.md` on ground the coverage map did not
  hold (`corpus/README.md` gains the r90 "Cache-key conformance" row), and it
  cites S466, S467 and S468 — all `mined`, all tier A, all opened this round.
  Registry 202 → 205 (A 177 → 180); census clean at both ends.
- **quality: improved.** A weaker scope (S463 "not cache-key construction") is
  superseded by a stronger row (S467) with the filed bytes untouched; both
  round-89 ledger statements are corrected by appended tails naming a receipted
  revision; the round-89 M37 equivalence claim is falsified with a gate case
  that fails it; and `corpus/QUALITY.md` gains a grounded criterion
  ("a counter earns a `met` only after it has been shown able to say no") citing
  the round-89 spot-check and this round's Mistakes rows 3 and 5. The whole
  diff has 0 deleted lines, so no admitted entry failed a re-check by
  rewriting.
- **discernment: improved.** The outside spot-check agrees on all six sampled
  gate decisions (3 admits, 3 rejects) and on the three new rows' quotes and
  anchors, and the item the round-89 spot-check routed into a QUALITY criterion
  landed as a criterion with lesson grounding. Offset, stated for the record:
  both frozen counters again admitted forgeries and the shipped carrier gate
  was falsified by held-out stubs — the lane found this with its own attack
  seats, mined it (Mistakes rows 3 and 5), hardened the gate and routed the
  successor requirements, so the disagreement is learned rather than left
  standing.

## Routed defects (lane fixes next round)

- R90-A: both frozen round-90 counters admit forgeries (C1: ignored/staged file,
  any receipted revision, case-variant scope; C2: pin-reading or allowlist
  gate). Successor requirements are already written in SCORECARD "Planned —
  after round 90"; land the successor counters.
- R90-B: the tip gate was never re-mutated — MutGate attacked the carrier bytes
  only, so the hardening (`a4814f58`) has no mutation score.
- R90-C: `controls/run_controls.sh` no longer replays at the tip: it copies the
  lane-root `baseclean.out`, which this round relocated. Re-point it at
  `.ufo/waves/round-90/inherited/baseclean.out`.
- R90-D: the held-out admit `S09-value-nul-refused.py` stays undecided until the
  contract rules on NUL (R90-2).
- R90-E: carried from the lane's own routing — R90-1 (input encoding), R90-3
  (example 5 raw-vs-escaped), R90-4 (method missing from the key), R90-5
  (duplicate JSON members).

Operator note (promotion is operator-owned): `SHONEN` boxes 1, 3 and 4 carry
resolvable pointers a non-author can check; box 2 stays `[ ]` on the round-47
receipt gap, so the checklist is not fully checkable yet.
