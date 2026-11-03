# Round 71 W1 — ReviewRepair (reviewer): attack the repair rules, not the counters

Base cc6b4e0b8c35e72dfb02c6184b847f68c1262153. Counters from freeze 04557e17, sha256 identical to the lane working tree
(c71_calibration ae317667…fd51, c71_tmp 9037746b…d32a). Scratch /fast/scratch/hyaku/kake-r71/ReviewRepair (clone at base;
every test a `-c user.name=kake-seat` commit built from the base blob), removed before yield — cited revs are scratch-only.
No tools installed; lane tracked bytes untouched. Base controls reproduced first: C1 `mismatches=3 met=False` exit 1, C2
`unannotated_tokens=7 met=False` exit 1, both matching controls/c1-base.txt and c2-base.txt. Attack = a change that turns
the counter green while a stale or unsupported fact survives; each verdict asks whether the rule TEXT forbids it.

## C1 items 1–2 — planned heading → exact superseded string — verdict: holds
- A1 rename L21 `## Planned`→`## Historical plan`, no superseded note (items 2–4 exact): rev c51bb730b402, exit 1,
  `stale_planned=0 attack_mismatch=0 guard=fail` — guard catches replace-without-superseded; the exact-string rule text forbids it too. HOLDS.
- A2 rename both headings to `## Planned — round 99` + orphan `## Superseded plan — round 21`/`— round 48` (correction +
  item 4 exact): rev 62191f3cfcc3, **exit 0 met=True guard=ok**. Both stale plan sections stay active under a false round
  label (bodies still carry `**Round 21**`/round-48 text); the guard's superseded check is `any()` over the whole tip, not
  positional, and the stale scan only sees `## Planned` headings. Rule text forbids (items 1–2 pin exact strings). HOLDS
  as text; counter green-wrong. Severity MEDIUM (review-detected only).

## C1 item 3 — correction line — verdict: holds (text); counter and kill rule both blind to a wrong-wave claim
- B wrong-wave correction `the round-69 wave W1 attack share 3/14 …` (numbers right, items 1–2/4 exact): rev 7760820dfb7d,
  **exit 0 met=True**. L4770's 4/14 stands uncorrected and a false round-69 claim is added; the kill rule "a correction
  whose number differs from the recomputed value" cannot fire (3/14 matches). Only the exact-content rule forbids. Severity MEDIUM.

## C1 scope gap — `.ufo/waves/round-70/w1-results.json` unguarded — verdict: under-specified. Severity HIGH
- R no correction line; results tampered connector→reviewer so the strict recount is 4/14 = stated: rev 6cbb807d996f,
  **exit 0 met=True** (`attack_stated=4/14 attack_strict=4/14`). Round-70 history is laundered; the exact fact C1 exists to
  correct becomes "supported". The guard diffs SCORECARD.md only; repair items 1–4 never mention results.json; the counter
  reads results at the tip revision; the kill rule is inapplicable (no correction). Nothing automated prevents it.

## C1 item 4 — `## Planned — next round`, no declared claims — verdict: holds (text); counter has zero enforcement
- E1b item 4 skipped (results clean): rev aa4341ca738a, exit 0 met=True (strict 3/14, corrected via item 3). E2b item 4
  heading plus declared-claim body `**Round 72** …`: rev 3817828edc98, exit 0 met=True — `## Planned — next round` never
  matches PLANNED_RE, so declared claims under it are invisible. Rule text forbids both. Severity LOW (skip leaves no
  false fact; the claims variant leaves unsupported forward claims).

## C2 repair rule — verdict: under-specified (prescribed repoint demonstrated harmful); annotation half holds
- C phrase-only annotation on all seven lines incl. imperative L95, `/tmp/probe-latest.backup.json` token intact: rev
  b4b54c9a9fc5, **exit 0 met=True guard=ok** — same verdict as ExecControls J3 (rev 5b37014e0479, exit 0). The added-line
  test is phrase-or-mktemp, so the counter cannot encode the kill rule "annotation on an imperative command"; rule text
  forbids (L95 must be repointed). HOLDS as text; backstop is review-only. Severity MEDIUM.
- D2 repoint exactly as prescribed — L95 becomes `state/probe-latest.json $(mktemp -d)` → run → `cp` back;: rev
  4c3006e86218, exit 0 met=True — but the prescribed replacement breaks the recipe. Exercised fixture: the original
  named-path round-trip restores (`restored: 18-rows`); the repaired form `cp file $(mktemp -d)` exits 0 yet the backup
  lands in an anonymous dir, and both restore attempts exit 1 (`cp: cannot stat …/probe-latest.json`; `cp: -r not
  specified; omitting directory`). Any inline mktemp is unreachable by the later "`cp` back" step; a working repoint
  needs a captured path the rule neither prescribes nor authorizes. UNDER-SPECIFIED. Severity MEDIUM.
- D1 `$(mktemp)` variant: rev e673dd40b046, exit 0 — deviates from the prescribed string (forbidden by text); same round-trip anonymity. Severity LOW.
- Phrase-only on the six historical lines (dropping exact path + dated `test -e` exit) is also green; the QUALITY bar
  (target + dated event + non-executable wording) is text-enforced only. `test -e` recorded for all six targets, exit 1
  (absent): L27/227/359 `/tmp/kake-r12/live/`, L356 `/tmp/kake-r11/`, L463/464 `/tmp/kake-r23-SurfacePlazir15Kimi-bnbU/SKILL-base.md`.
  Residual: L463/464 carry `Surface: git … > /tmp/...` command syntax; if judged imperative, their annotation fires the kill
  rule — contract classifies only L95 runnable. Severity LOW.

Verdict summary — C1-1 holds · C1-2 holds · C1-3 holds (counter+kill blind to wrong-wave, MEDIUM) · C1-4 holds (unenforced,
LOW) · C1-scope results.json UNDER-SPECIFIED (HIGH) · C2-repoint UNDER-SPECIFIED, literal prescription harmful (MEDIUM) ·
C2-annotation holds, kill-rule backstop review-only (MEDIUM).

Honesty: every exit above was exercised against a committed scratch revision (revs inline); no check reported unrun; counter bytes verified against the lane working tree by sha256; scratch removed before yield; no lane tracked file edited.

Report: .ufo/waves/round-71/w1/ReviewRepair.md
