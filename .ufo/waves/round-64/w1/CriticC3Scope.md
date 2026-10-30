# CriticC3Scope — honesty ruling on C3 (round 64)

Seat: `CriticC3Scope` (leaf, no subagents). Lane repo read-only; all mutations ran in a private clone under `/fast/scratch/hyaku/kake-r64/CriticC3Scope/clone` (toplevel asserted before every mutation). Scratch deleted before yield.

## Ruling

**The instrument does not overclaim. The claim wording partly does.**

1. **Instrument output is honest.** The `--offline` run prints `VERDICT: OK (exit 0, partial: offline)`, then `skipped(offline): §armed … · §history (probe-history source absent — pin-declared) — complete=false, never counted as pass`. `--json` carries `"complete": false` and the `skipped` list. The exit-0 verdict is computed only from sections that actually ran (`verdictOf`, `scripts/freshness-sweep.mjs:1058`). The SKILL registry row (`SKILL.md:212`) states: "`0=clean` for evaluated checks only … Offline/skipped/suspended sections are never proof of a complete publishing check." The governing QUALITY row (`corpus/QUALITY.md:10`) names "a partial/offline run presented as a complete publishing check" as a failure. Nothing in round 64 claims completeness.

2. **Contract §C3 (`.ufo/waves/round-64/contract.md:96`, predicate at `:104-106`) stays inside what the instrument proves, but only under its own title.** The title scopes the claim to "the standing §paths gate evaluates again", and the kill rule is §paths-specific ("the §paths drift count is non-zero"). The bare predicate quotes `VERDICT: OK` and drops the `partial: offline` qualifier that the same printed line carries. Ruling: acceptable as written; the predicate should quote the full line so the qualifier travels with the token.

3. **Lesson §Mistakes / Gate overclaims scope. This is the defect to fix.** `corpus/lessons/round-64.md:23` says "`scripts/freshness-sweep.mjs --offline` returns to evaluating (exit 2 → exit 0)". Row 30's Fix column says the re-pin "returns the sweep to exit 0". Read plainly, that restores the whole instrument. It does not. At T0 §history is SUSPENDED (pin `probeHistoryAbsent`, in place since round 18) and §armed is skipped offline. Neither the lesson nor the contract mentions the §history suspension anywhere (grep of `round-64.md`, `contract.md`, `QUALITY.md` round-64 text: no hit). Only §paths evaluates. Suggested wording: "§paths evaluates again (`--offline` exit 2 → 0); §history remains SUSPENDED by pin and §armed is skipped offline, so this is not a complete freshness check."

4. **The committed after-receipt cannot show the §paths leg of the claim.** `.ufo/waves/round-64/controls/sweep-after.txt` is 6 lines: a `$ node … --offline (measured tree T0, contract §C3)` header, a `§armed` block, the skipped line, `VERDICT: OK (exit 0, partial: offline)`, `exit=0`. It contains no §paths block (no resolve/declaredAbsent/drift/newMissing counts) and no §history line, though the real command prints both (my T0 run: `t0-plain.txt` lines 5 and 78). The kill rule names "the §paths drift count", and the receipt does not record it. The count (drift 0, newMissing 0) holds on my re-run, so the claim survives, but the receipt is an excerpt presented as a command transcript. Recommend replacing it with the raw stdout and exit. This is an evidence defect, not a kill: the rule triggers on a non-zero count, and the receipt shows exit 0. That reading is my judgment.

5. **§paths OK has limits the VERDICT line does not show.** The body prints them, but the one-word verdict hides them: `relative-form cites … not resolve-checked: 2677` (2678 under E3); `unresolved 10` (globs/placeholders); `declaredAbsent 65` is exit-neutral by design. Known limit already documented at `corpus/knowledge/freshness-sweep.md:132`. §paths OK therefore proves: every `~/` and `/home/vgpnk/` token resolves, or sits within ±2 lines of absence vocabulary. It does not prove relative-form citations.

6. **Doc drift (pre-existing, not round-64).** `corpus/knowledge/freshness-sweep.md:21` says `--offline` is "§paths + §history only". At T0 it evaluates §paths only, because §history is pin-suspended. The doc was not updated.

7. **Minor instrument wording (pre-existing, unchanged base→T0; `pins`/script diff empty).** (a) Zero-check runs print `VERDICT: OK (exit 0)`: `--offline --section=history` and `--offline --section=armed` each evaluate nothing and exit 0 (E4a/E4b). The default offline command is not vacuous because §paths always runs, so the contract command is unaffected. (b) `skipped … never counted as pass` sits beside a headline `OK`. (c) Exit 2 prints `VERDICT: DRIFT` (E6), since `ok = code === 0`.

8. **Contract prose error on the re-pin.** Contract §C3 says the re-pin "changes only `line` and `lineSha256`". The field-level comparison shows only `line` changed (7 entries); every `lineSha256` is unchanged from base. The lesson re-pin map labels the unchanged sha as "new lineSha256". Neither breaks the kill rule, which permits but does not require a sha change. Correct both to "changes only `line`".

## Kill-rule check (C3, as I read it)

- after receipt exit: 0 → not triggered.
- §paths drift count: 0 on re-run (receipt silent; see 4) → not triggered.
- sidecar cells other than the seven line/lineSha256 pairs: none changed → not triggered.

C3 is not killed. The proposition "§paths evaluates again" is re-observed. The wording and receipt defects above need correction before the claim stays inside what it proves.

## Evidence (exact commands and outputs)

Clone setup and toplevel assertion:
```
git clone --shared /home/vgpnk/Projects/shokunin/kake-shokunin clone
git -C …/clone rev-parse --show-toplevel  -> /fast/scratch/hyaku/kake-r64/CriticC3Scope/clone
```
(One early base checkout hit a transient `index.lock` in my own clone; re-run with HEAD asserted.)

Base `1a481315` — `node scripts/freshness-sweep.mjs --offline`:
```
freshness-sweep: Error: paths sidecar binding invalid: SKILL.md:364   (exit 2)
```

Measured T0 `4c8295fa` and receipts commit `cc8add1f` (diff of sweep, SKILL, corpus/knowledge, lesson, QUALITY between them: empty), `node scripts/freshness-sweep.mjs --offline`, exit 0:
```
§paths  172 files · 679 occurrences · 106 unique tokens
  resolve 31 · declaredAbsent 65 · drift 0 · unresolved 10
  relative-form cites (outside PATH_RE, not resolve-checked): 2677
  citation base: 106 targets · missSet 65 · files 172
  set-delta miss: no new miss
§history  SUSPENDED — probe-history source absent by declaration (pins.probeHistoryAbsent): /home/vgpnk/Projects/webzites/state/probe-history.jsonl …
§armed
  all remote checks skipped(offline) — NOT counted as pass (complete=false)
skipped(offline): §armed (all remote checks) · §history (probe-history source absent — pin-declared) — complete=false, never counted as pass
VERDICT: OK (exit 0, partial: offline)
```
`--offline --json`: `{"ok":true,"code":0,"complete":false,"skipped":["§armed (all remote checks)","§history (probe-history source absent — pin-declared)"],"reasons":[],"paths":{"resolve":31,"declaredAbsent":65,"declaredAbsentIndirect":4,"drift":0,"unresolved":10,"newDrift":0,"newMissing":0},"hist":{"suspended":true,"ok":true}}`

Boundary experiments (all sequential, clean tree asserted before and after each; one early attempt ran in parallel and raced with my own pins edit, so its output was discarded and every result below is from the sequential re-run):

- E1 `node scripts/freshness-sweep.mjs --section=paths` (no `--offline`): `VERDICT: OK (exit 0)`, no partial marker, no skipped line.
- E4a `--offline --section=history`: `§history SUSPENDED …`, `VERDICT: OK (exit 0, partial: offline)`, exit 0, zero history checks evaluated.
- E4b `--offline --section=armed`: `all remote checks skipped(offline)`, `VERDICT: OK (exit 0, partial: offline)`, exit 0, zero armed checks evaluated.
- E2 appended `~/Projects/nonexistent-r64-probe/file.json` (unannotated) to SKILL.md: `set-delta miss: !! NEW MISS ~/Projects/nonexistent-r64-probe/file.json`, `VERDICT: DRIFT — §paths: 0 unannotated miss · 1 NOT in pins.pathsMissSet (exit 1, partial: offline)`, exit 1. Sensitivity confirmed.
- E3 appended `fleet/nonexistent-r64-relative.json`: `relative-form cites … not resolve-checked: 2678`, `VERDICT: OK (exit 0, partial: offline)`, exit 0. A missing relative-form cite passes.
- E6 removed `probeHistoryAbsent` from `corpus/knowledge/freshness-pins.json`: `§history !! ERROR cannot read /home/vgpnk/Projects/webzites/state/probe-history.jsonl`, `VERDICT: DRIFT — … (exit 2, partial: offline)`, exit 2. Suspension is pin-dependent and fails closed.
- All mutations reverted with `git checkout -- <file>`; `git status --porcelain` empty after each.

Sidecar comparison, base `1a481315` vs T0 `4c8295fa` (`JSON.parse` both, per entry, 30 entries):
```
entries changed=7 fields changed=line
SKILL.md 364 -> 365 line ~/Projects/ds4cc-marketplace        (also 445->446, 448->449, 449->450, 450->451)
SKILL.md 423 -> 424 line ~/Projects/ds4cc-marketplace/burnerchrome   (431->432)
```
No `lineSha256` value changed.

Receipt inspection:
```
$ wc -l controls/sweep-after.txt  -> 6
$ grep -n "§paths|resolve |declaredAbsent|VERDICT|exit=" controls/sweep-after.txt
5:VERDICT: OK (exit 0, partial: offline)
6:exit=0
```

Wording locations (lane repo, absolute):
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/contract.md:96` (C3 title), `:104-106` (predicate)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-64.md:23` ("returns to evaluating"), `:30` (Mistakes row, Fix column "returns the sweep to exit 0")
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md:10` (governing row), `:1426` (round-64 criterion, scoped to §paths)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:212` (freshness-sweep registry row)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/freshness-sweep.md:21` (stale "§paths + §history" for --offline), `:132` (relative-cite limit)
- `/fast/scratch/hyaku/kake-r64/CriticC3Scope/clone/scripts/freshness-sweep.mjs:139` (SECTIONS), `:1058` (verdictOf), `:1129` (VERDICT print)

## Suggested corrections (not applied; lane frozen)

1. Lesson `:23` and `:30`: replace "returns to evaluating" / "returns the sweep to exit 0" with the §paths-scoped wording in item 3.
2. Contract predicate: quote the full printed line `VERDICT: OK (exit 0, partial: offline)`.
3. Receipt: replace `controls/sweep-after.txt` with the raw full stdout and exit of the command.
4. Contract and lesson re-pin map: "changes only `line`"; drop the "new lineSha256" column or mark it unchanged.
5. `freshness-sweep.md:21`: drop "§history" from the `--offline` description while the pin suspends it.

## Tooling

No tools installed or upgraded. Used pre-existing `node v24.21.0` and `git`. pacman untouched. Nothing written to `~/.local/bin` or any PATH directory, and no fleet-root tracked file touched.

## Host notes

The lane's untracked files changed during this run (`w1.ready.partial` replaced by `w1.ready.dispatched`), which is orchestrator activity. I wrote nothing outside this report and my scratch tree.
