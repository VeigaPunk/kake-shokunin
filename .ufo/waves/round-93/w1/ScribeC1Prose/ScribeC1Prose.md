# ScribeC1Prose — kake round 93, wave 1 — C1 classes E1, E2, E4

VERDICT: E1, E2 and E4 hold at the worktree — all three classes read 0 in an exact replica of the frozen c1 predicate and in the frozen counter itself run at a scratch fixture commit carrying the repairs; one E3 mismatch remains (C2 seat's scope). One required integration step is handed to the L1: a 3-entry freshness-sidecar re-pin (this seat's appends shift three line-bound sidecar pins; without it the §paths sweep crashes exit 2).

Seat: ScribeC1Prose (leaf scribe; owns C1 classes E1, E2 and E4 only).
Lane root: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Freeze `bb8012fee38c0e497cdaf36337072737bca0b3cd`; base `10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5`. During this seat's run the L1 committed `5272c727` ("preserve in-flight work … not a landed round"), which landed the sibling E3/E5 seat's repairs and the C2 knowledge entry — so master moved from `191ef8dd` to `5272c727` mid-flight; all readings below state which tree they measured.

## 1. Required frozen-counter paste (committed bytes at master)

Command: `python3 -B .ufo/waves/round-93/c93_selfassess.py --root . --revision master` (run 2026-11-04, after the L1's `5272c727` preservation commit). Exit 1, line 1 exact:

```
C1v93 revision=5272c727a3b438bb386c698dc110f44ba6384312 lessons=88 entries=81 rows=255 criteria=39 mismatches=14 E1=1 E2=8 E3=1 E4=4 E5=0 pins=ok met=false
```

My repairs are worktree-only (this seat never commits in LANE), so this reading shows the before-values for my three classes (E1=1, E2=8, E4=4) and the sibling seat's after-values (E3=0 … wait — E3=1: see §6). Full output: receipt `counter-at-master.txt`.

## 2. Authoritative repaired-tree reading (scratch fixture commit)

Per the git-fixture rules I created one scratch clone (`/fast/scratch/hyaku/kake-r93/ScribeC1Prose/clone`, `--shared`, detached at `bb8012fe`, `refs/heads/master` updated to LANE master, `--show-toplevel` verified), copied my six edited files in, and committed there with a fixture identity (`436678a4a9fe014902dcc305eec143eb6a20da1d` — "ScribeC1Prose scratch fixture … not a landed commit"). Frozen counter at that revision:

```
C1v93 revision=436678a4a9fe014902dcc305eec143eb6a20da1d lessons=88 entries=81 rows=255 criteria=39 mismatches=1 E1=0 E2=0 E3=1 E4=0 E5=0 pins=ok met=false
```

**E1=0, E2=0, E4=0** — all three of my classes clear the frozen predicate on committed bytes. Receipt: `counter-scratch-fixture.txt`. The one remaining mismatch (E3) is `corpus/knowledge/conditional-request-evaluation.md` — "unresolved S471, S472, S473, S474, S475, S476" — the C2 freshness entry's source ids are not in `corpus/SOURCES.md`; that entry and its ids belong to the C2/knowledge seat, not this seat (§6).

A worktree replica of the same predicate logic (identical regex/findall code, worktree files) reads identically: E1=0 E2=0 E4=0.

## 3. Required grep pastes

`grep -c '^## Gate' corpus/lessons/round-85.md` → **2**
(the original suffixed heading `## Gate — admit a parser algorithm, reject blanket equivalence` also starts with `## Gate`; the exact-match count `grep -c '^## Gate$'` is **1** — my appended heading.)

`grep -n 'corpus/lessons/' corpus/QUALITY.md | tail -20` → shows the tail of the file's lesson citations including my appended Round-76 grounding line at 1541; the eight appended E2 lines are at 546, 569, 694, 862, 1024, 1053, 1084 and 1541 (visible via `grep -n 'Grounding lesson (round-93' corpus/QUALITY.md`). Full paste: receipt `grep-pastes.txt`.

## 4. L1's awk check (requested paste)

```
corpus/lessons/round-29.md: blank_between_pipes=0
corpus/lessons/round-33.md: blank_between_pipes=0
corpus/lessons/round-54.md: blank_between_pipes=0
corpus/lessons/round-92.md: blank_between_pipes=0
```
Receipt: `awk-blank-between-pipes.txt`.

**Note on the awk vs the predicate:** the L1's awk counts every blank line whose *previous* line starts with `|`, which is stricter than the frozen predicate (a `|`-blank-`|` sandwich). The original files read 2/2/2/2 under the awk; the applied repair reads 0/0/0/0. I verified that the L1's literal two-part layout (marker prose *after* the blank) leaves the awk at 2 — because the retained historical row and the new tagged copy each precede a blank — so I placed each marker prose *before* the blank it guards, which satisfies both the frozen predicate and the awk. Every historical byte is retained unchanged.

## 5. What was changed (87 insertions, 0 deletions — pure append; `repairs.diff`)

**E1 — `corpus/lessons/round-85.md`** (+66 at EOF): appended a `## Gate` section whose heading line is exactly `## Gate`. The lesson's own Gate decisions sit above in `## Gate — admit a parser algorithm, reject blanket equivalence` (retained byte-identical); the appended section restates, from the lesson's own evidence: admits (S458 §8.1 step 3, 23-word quote — grounding a field-specific effective-token decoder only; plus the registry-URL Editor's-Draft evidence with its receipt-backed digest `339bdd20…`), rejects (blanket response-policy reorder equivalence, §11.1 22-word quote — identical token multisets do not imply identical effective policy), and the flips (the §11.1 flip condition; the admit's token-iteration-only scope; the registry URL flip). It states that the lesson records source work (the 2026-11-04 GETs) and that no source work was opened for the section itself. The TR-source sha256 is cited by its retained receipt path (`.ufo/waves/round-85/w1/ScribeLesson/source-receipt.json`) rather than re-pasted as a backticked 64-hex span, so the new title-exact Gate section introduces no unbacked claim-bearing span for a future `doc_quote_truth --rounds 85` scan. The located quotes are blockquoted (not spans).

**E2 — `corpus/QUALITY.md`** (+8, one line appended at the END of each flagged section): each names the lesson file that produced the criterion and, where the section quotes a receipt, the lesson row the receipt rests on:
- Round-31 wave-2 → `corpus/lessons/round-31.md`, §Mistakes row "doc claim wider than its probe" (the `hostile-selftest-fde133a-runner.json` receipt).
- Round-32 → `corpus/lessons/round-32.md`, sole §Mistakes row "unobserved timestamp written as fact" (receipt `declared-time-check.txt`).
- Round-34 wave-2 → `corpus/lessons/round-34.md`, §Wave-2 corrections (appended) bullet "Gate check repairs at 76fac3b" (receipt `criterion-gate-reject-fixtures-at-76fac3b.txt`); (c)/(d) on the same section's later entries.
- Round-35 wave-2 → `corpus/lessons/round-35.md`, §Wave-2 corrections (appended) C1-sufficiency entry (`ExecPartialRepairs`).
- Round-40 → `corpus/lessons/round-40.md`, §Mistakes rows 1 and 2.
- Round-41 → `corpus/lessons/round-41.md`, §Mistakes rows 1, 2, 3.
- Round-47 pointer correction — R6 → `corpus/lessons/round-47.md`, §Mistakes row 3 ("verdict filed without a committed receipt"), whose fix retains the exact rerun receipt + digest the section quotes.
- Round-76 criterion → `corpus/lessons/round-76.md`, §Mistakes row "A claim row quoted an interior slice of a receipt line (unmarked elision)" + §Routed dispositions row 6.
All eight cited lesson files verified to exist at master ✓. The Round-76 section is in `doc_quote_truth`'s scan scope (rounds 75,76) — my line there is a bullet whose only spans are `corpus/lessons/round-76.md` (PATHY-excluded, not claim-bearing) ✓, and it avoids `supersedes`/correction-tag syntax (T4-safe) ✓.

**E4 — four lessons** (tagged re-append inside the table + two marker prose lines; every historical byte unchanged):
- `round-29.md`: the round-43 "absent-path annotation" row (detached below the table by the round-43 append) is re-appended inside the table as its last row, tagged "— re-appended r93 (round-93 C1 E4 repair)"; a marker line before the historical blank and one after the retained row keep the layout machine-clean. Why the blank existed: the table originally ended at row 3 (misroot, line 102) with the blank at 103 closing it; round 43's re-census (`b49cba9c`, 2026-10-23) appended its annotation row *below* that blank instead of inside the table, splitting it.
- `round-33.md`: same shape and cause (row 43 misroot; blank 44 from `1cf452ea`; round-43 annotation row 45 from `b49cba9c`).
- `round-54.md`: TWO detached rows ("A lexical correction marker…" and "A settlement counter…", lines 30–31) re-appended inside the table as tagged copies; blank 29 from the round-54 initial commit `8e408e00`, rows 30–31 appended by `a631cc02`.
- `round-92.md`: mistake row 5 ("A round committed its work and then ended without a report", line 67) re-appended inside the table as row "5b"; blank 66 from attempt 1 (`9f15115b`), row 5 appended by attempt 2 (`027faf79`).

## 6. Findings for the L1 (route list)

1. **Sidecar re-pin REQUIRED (blocking the §paths sweep).** My appends shift three line-bound `corpus/knowledge/freshness-sidecar.json` pins: corpus/QUALITY.md 649→651, corpus/lessons/round-29.md 128→131 and 200→203 (lineSha256 unchanged — content moved, not modified). Measured: BEFORE re-pin the sweep throws `Error: paths sidecar binding invalid: corpus/lessons/round-29.md:200`, exit 2 (crash, no verdict); AFTER re-pin (verified in the scratch clone) it exits 1 with the same pre-existing drift it has at master ("1 unannotated miss", `~/projects` at round-90.md:82 — unrelated to this seat). I did not edit the sidecar (outside my named write scope). Exact spec + verification recipe: `sidecar-repin-for-L1.json` in my wave dir; also messaged to KakeR93. The three notes embed the old line numbers ("Citation corpus/QUALITY.md:649…"); the round-64 precedent updated the line field only — updating the note references is recommended, not sweep-validated.
2. **Pointer shifts caused by my appends (append-only discipline):** `corpus/lessons/round-76.md` §Mistakes row 3 and §Routed row 6 cite `corpus/QUALITY.md:1499` as a base-revision coordinate at base `a0491fcd` (historical, stays valid); tip-side, that content moves 1499→1506. `.ufo/waves/round-43/make_w1_spec.py:152` and `.ufo/waves/round-43/w1/ExecSweepFull.md:94` name `corpus/lessons/round-29.md:104 vs :102` and `round-33.md:45 vs :43` — closed-round artifacts; the live ±2 annotation window still holds (the re-appended copy at round-29.md:103 carries the absence wording within the cite's window). `.ufo/waves/round-54/w1/CriticCJKWords.md:32` cites `round-54.md:28` — unchanged (my insert is after 28). No live gate is affected; noted for the correction register.
3. **E1 predicate vs corpus-contract divergence:** the frozen c93 E1 check requires a line exactly `## Gate` (`^## Gate\s*$`) while the lane's standing `corpus-contract.mjs` gate explicitly accepts a `## Gate — …` suffix variant — round-85.md passed corpus-contract while failing c93. Both now pass.
4. **L1 awk vs predicate discrepancy:** the awk counts any blank line following a pipe row (a superset of the predicate's sandwich); the L1's literal two-part layout leaves the awk at 2 while the predicate is cleared. The applied layout clears both (0 and 0). Demonstrated empirically; readings in `awk-blank-between-pipes.txt`.
5. **Remaining E3 (not mine):** `corpus/knowledge/conditional-request-evaluation.md` (the C2 freshness entry, landed by the L1's preservation commit) cites S471–S476 which are not rows in `corpus/SOURCES.md` → E3=1 at both master and my scratch fixture. The C2/knowledge seat owns E3.

## 7. Gates re-run (no regression)

- `corpus-contract.mjs` (worktree): `0 findings · 81 knowledge entries · 88 lane lessons · 77 skipped · 0 errors — exit 0`. Receipt `corpus-contract.txt`.
- `doc_quote_truth.py --rounds 75,76 --base a0491fcd…` at the scratch fixture: `findings=0 met=true`, exit 0 — my Round-76 QUALITY bullet addition does not break the standing quote-truth gate. Receipt `doc-quote-truth.txt`.
- `freshness-sweep --offline --section=paths`: BEFORE re-pin exit 2 (sidecar crash — finding 1); AFTER re-pin exit 1 with the identical pre-existing drift. Receipt `sweep-sidecar-before-after.txt`.

## 8. Limits

- The frozen counter at `master` still reads 14 mismatches until the L1 lands my six files (it reads committed bytes; my edits are worktree-only). The scratch-fixture reading (§2) is the committed-bytes proof of the repair.
- The appended E2/E4/E1 content restates lesson evidence; it does not re-open sources or re-measure receipts (none were in my item).
- The sidecar re-pin values assume no other landed change shifts QUALITY.md or round-29.md lines above the pinned entries; the L1 should re-derive by sha256 match at integration (command in the spec receipt).
- doc_quote_truth would newly scan round-85.md's title-exact `## Gate` section only if a future round runs `--rounds` including 85; the section's spans are paths, receipt-backed digests, URLs and blockquotes (no unbacked claim-bearing spans), matching the lane's own round-92 Gate practice.

## 9. Receipts (all under `.ufo/waves/round-93/w1/ScribeC1Prose/`)

`counter-at-master.txt` · `counter-scratch-fixture.txt` · `awk-blank-between-pipes.txt` · `grep-pastes.txt` · `sweep-sidecar-before-after.txt` · `doc-quote-truth.txt` · `corpus-contract.txt` · `repairs.diff` (208 lines) · `sidecar-repin-for-L1.json` · `sidecar-repin-for-L1.md`

Scratch directory `/fast/scratch/hyaku/kake-r93/ScribeC1Prose/` deleted after receipts were copied. No LANE commits, no pushes, no frozen-file edits, no E3/E5 work, no C2 work.
