# ExecSweepFull — full freshness sweep (all sections), round-43 wave 1

Seat: `kake-r43-w1-ExecSweepFull` (leaf). Axis: freshness. Target: the FULL sweep, not just `--section=paths`.
Frozen tip under test: `b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee`.

## Verdict

**CONFORMANT** — the C2 claim as frozen holds (its `--section=paths` predicate is exactly met and reproducible),
but the FULL sweep is **RED** at `§armed`, and the frozen `sweep-after.txt` receipt does **not** reproduce
byte-identically at the frozen commit. Two findings below (F1 §armed red, F2 receipt drift) bound the round's
freshness claim and must be reported, not fixed.

## Commands and exits (all with `timeout` + `prlimit --as=8000000000`)

| command (cwd = lane repo) | exit | verdict line |
|---|---|---|
| `node scripts/freshness-sweep.mjs` (no `--section`) | **1** | `VERDICT: DRIFT — §armed: PQ-2 GATE-OPENED, sitemap LISTED-LIVE, plazir-gate-anomaly (exit 1)` |
| `node scripts/freshness-sweep.mjs --section=paths` | 0 | `VERDICT: OK (exit 0)` |
| `node scripts/freshness-sweep.mjs --section=history` | 0 | `VERDICT: OK (exit 0)` — §history `SUSPENDED` (pin-declared absent) |
| `node scripts/freshness-sweep.mjs --section=armed` | **1** | `VERDICT: DRIFT — §armed: PQ-2 GATE-OPENED, sitemap LISTED-LIVE, plazir-gate-anomaly (exit 1)` |
| `node scripts/freshness-sweep.mjs --section=plazir` | **1** | `VERDICT: DRIFT — §armed: plazir-gate-anomaly (exit 1)` |
| `node scripts/freshness-sweep.mjs --offline` (all sections, remote skipped) | 0 | `VERDICT: OK (exit 0, partial: offline)` |
| `node scripts/freshness-sweep.mjs --json` (all sections) | 1 | `ok=false code=1 complete=true reasons=["§armed: PQ-2 GATE-OPENED, sitemap LISTED-LIVE, plazir-gate-anomaly"]` |

Full-sweep red is **stable**: two further consecutive bare runs both exited 1 with the identical verdict string.

## Per-section verdicts (from `--json`, `sweep-full.json`)

- **§paths** `ok=true` — `resolve 26 · declaredAbsent 65 · drift 0 · unresolved 10`; `missSet 65`, `newMissing 0`,
  `newDrift 0`, `set-delta miss: no new miss`. Same as the frozen `sweep-after.txt` numbers except counts (F2).
- **§history** `ok=true`, but `historySuspended=true` — `probe-history source absent by declaration
  (pins.probeHistoryAbsent)`. Listed under `skipped(...)`, "complete=false, never counted as pass". **Not evaluated**,
  so §history is not evidence of anything this round.
- **§armed** `ok=false`, `driftVerdicts=["PQ-2 GATE-OPENED","sitemap LISTED-LIVE","plazir-gate-anomaly"]`:
  - PQ-12 charter-ghp `EDIT-LANDED` (steady-state set; sha `7c243a1d…` matches pin; r15 snapshot absent → warning)
  - PQ-5 kimi dead slot `PENDING` (404/13409 B/93ddca9a… — body matches pin)
  - PQ-2 `GATE-OPENED`: remote `7fc6aa2f…` vs pin `e6bd0718…`; unpushed 0 vs pin 20
  - ds4cc sitemap `LISTED-LIVE`: status **200**/7810 B vs pin 404 (pin `corpus/knowledge/freshness-pins.json:36`)
  - PQ-14 plazir `ANOMALY` · sitemap `NOT-EVALUATED`: live 7 locs (pin 8), source `skipped(no-source-file)`
    (dir `/home/vgpnk/Projects/plazir-15-site` absent), `plazir-gate-anomaly` from the git error at
    `scripts/freshness-sweep.mjs:756`.

## F1 — the full sweep is RED at §armed; C2's frozen scope covers only §paths

`SCORECARD.md:3250-3260` declares C2 as "`node scripts/freshness-sweep.mjs --section=paths` (exit code + verdict
line)" — a §paths-only predicate, which is met (exit 0, `VERDICT: OK`). The full sweep is red at §armed, and the
**same three drift verdicts already stood at the round-43 base `61046fcf…`** (bare full sweep there: exit 1,
identical `§armed: PQ-2 GATE-OPENED, sitemap LISTED-LIVE, plazir-gate-anomaly`). So F1 is **pre-existing standing
debt, not introduced by the freeze**. The lane already knows and deliberately did not re-pin it:
`SKILL.md:946` ("`pq2Remote` `e6bd0718`, `sitemapStatus` 404 flagged, not re-pinned this round"),
`corpus/knowledge/sitemap-orphan-audit.md:246`, and `corpus/knowledge/freshness-sweep.md:92-100` ("Exit 1 is
currently the EXPECTED verdict"). **Bounds the round's freshness claim** (the lane's standing instrument is not
green overall), but does not falsify C2 as declared. Not fixed here, per instruction.

## F2 — the frozen `sweep-after.txt` receipt does not reproduce at the frozen commit

`sweep-after.txt` (2026-10-23T19:38:16Z) reports `§paths 100 files · 620 occurrences · 98 unique tokens`,
`resolve 23`, `citation base: 98 targets · files 100`. Re-running `--section=paths` **at the frozen commit
`b49cba9…`** gives `102 files · 623 occurrences · 101 unique tokens`, `resolve 26`, `citation base: 101 targets ·
files 102` — same `drift 0`, `declaredAbsent 65`, `missSet 65`, `set-delta miss: no new miss`, `VERDICT: OK (exit 0)`.
Cause, isolated by checkout: the receipt was captured **before** the freeze commit added
`corpus/lessons/round-43.md` and `corpus/knowledge/claim-count-derivation.md` (files 100→102) and before the
`corpus/SOURCES.md` S129/S130 rows added 3 sibling-repo tokens (occurrences 620→623, tokens 98→101,
resolve 23→26). Receipt mtimes: `sweep-after.txt` 16:38:16 vs `SOURCES.md` 16:41:51, `claim-count-derivation.md`
16:42:09, `round-43.md` 16:42:41 — the receipt predates the commit's own corpus bytes (commit 16:44:33).
**Consequence: the receipt's file/occurrence/token counts are stale with respect to the tree it is filed under**;
the *verdict* (exit 0 / OK / drift 0) does reproduce. This is the same class as the round's own Mistake 7
(counts that fail re-derivation from committed bytes) — the receipt is evidence of the claim, and its numbers
cannot be re-derived from `b49cba9…`.

## F3 — the movement census pointer shift is off by one (defect in the frozen C2 fix)

`SCORECARD.md:3258-3259` and the two dated EOF notes claim the shift
`.ufo/waves/round-30/w2/CriticC1Scope.md` `round-29.md:118-122` → `:119-123` and
`.ufo/waves/round-34/w1/CriticFrontierNovelty.md` `round-29.md:124-132` → `:125-133` — a **+1** shift for a
**2-line** insertion (annotation row + blank line). Measured against the committed bytes:
`git show 61046fcf:corpus/lessons/round-29.md | sed -n '118,122p'` == `git show b49cba9:… | sed -n '120,124p'`
(md5 `8766f47b03bc2e022b4ff1289ea112a0`) and `…124,132p` == `…126,134p` (md5 `abba07ec8025b7b55dca7a397c38e604`).
The correct pointers are **:120-124** and **:126-134**; the frozen text names ranges that are off by one and do not
contain the cited content — the named range `b49cba9…:119-123` md5 `8fc3067c9389d02d343144a9a7856cfc` ≠ base
`118-122` md5 `8766f47b03bc2e022b4ff1289ea112a0` (it starts on a blank line and drops the last cited line,
"and the missing `O_NOCTTY`."). The EOF notes' own wording ("gained one annotation row (line 104)") is right about the
row but misses the added blank line that moves the downstream pointers by 2. Both notes are append-only dated
corrections, so the fix is another appended correction, not an in-place edit.

## Per-checked-statement holds / overstated / wrong

| statement (source) | verdict |
|---|---|
| C2 counting command `--section=paths` → exit 0, `VERDICT: OK` (`SCORECARD.md:3252`, `:3261`) | **holds** — reproduced at `b49cba9…` (exit 0) and at HEAD |
| C2 before-state: `--section=paths` exit 1, "2 unannotated miss · 2 NOT in pins.pathsMissSet" (`sweep-before.txt`) | **holds** — re-run at base `61046fcf…` is byte-identical to `sweep-before.txt` except the `generated` timestamp |
| the two named tokens are the round-29/round-33 misroot fleet paths | **holds** — both are in `pathsMissSet` (65) and are the only §paths drift at base |
| pins `pathsMissSet` 63 → 65 (`SCORECARD.md:3257`) | **holds** — base pins 63, freeze pins 65; diff is exactly the two tokens |
| annotation rows at `corpus/lessons/round-29.md:104` and `corpus/lessons/round-33.md:45` | **holds** — both rows present at those lines |
| movement census `:118-122 → :119-123`, `:124-132 → :125-133` (`SCORECARD.md:3259` + both EOF notes) | **wrong** — actual shift is +2: `:120-124`, `:126-134` (F3) |
| `sweep-after.txt` counts (100 files / 620 occ / 98 tokens / resolve 23) as the freeze-commit state | **overstated** — at `b49cba9…` the same command yields 102 / 623 / 101 / resolve 26 (F2); the verdict line reproduces |
| full sweep green | **wrong** — full sweep exits 1 at §armed (F1), pre-existing at base, deliberately un-re-pinned per `SKILL.md:946` |

## Digests and artifacts

- `scripts/freshness-sweep.mjs` sha256 `a1aa79d114093cc5b663e811e86a20a57bf37357dd8a3598c9e02084770d8d8b`
  (identical at `b49cba9…` and HEAD); `corpus/knowledge/freshness-pins.json` sha256
  `4539b8e2659832229f609fbbb2df38f4dc08e4f18ebd67e8f5ec331a82e7f660` (identical at both).
- Receipts: `/fast/scratch/hyaku/kake-r43/kake-r43-w1-ExecSweepFull/` — `sweep-full.txt`/`.json`/`.exit`,
  `sec-{paths,history,armed,plazir}.txt`, `offline-full.txt`, `paths-at-freeze.txt`, `paths-at-base.txt`,
  `paths-freeze-minus2.txt`, `paths-freeze-nosources.txt`, `json-{base,freeze-full}.json`.
- No repo file was modified by this seat (only this report); scratch clones under `/fast/scratch/.../` were removed.
  No tool installed or upgraded (node v24.21.0 already present).

## Limits

- §armed reaches the operator's live properties (`veigapunk.github.io`, `ds4cc.com`, `*.kimi.page`) and the
  `ds4cc-marketplace` git remote — read-only GET/`ls-remote`, as the standing instrument does; the C2 scope
  itself is `--section=paths`, which touches no network.
- §history could not be evaluated at all (pin-declared absent source), so nothing in this report speaks to the
  history-shape claims (H2/H3/H4).
- F1/F3 are reported only; per the item, red sections outside `paths` are bounded, not fixed.
