# ScoutC1Shapes

Recon for C1 (`scripts/receipt_lineage.py`): classified all 144 frozen population paths at base
`9f07731a873585e655a6518233ea39f5d9fb8204` against the contract's receipt grammar, walked first-parent
history for every event, and flagged shapes the frozen rules may misread. Method: read-only git on a
`--shared` clone in scratch; evidence in `.ufo/waves/round-61/w1/ScoutC1Shapes.files/` (classify.json,
events.json, classify.py, analyze3.py). No tools installed (system git + python3 sufficed).

## CLASSES:

- Population: 144 files at base; all present, none empty (smallest 2 bytes), no non-ASCII paths.
- **Receipts: 84** — first committed version carries a grammar line. By round: r52 15, r54 6, r55 6,
  r56 7, r57 13, r58 9, r59 9, r60 19. Extensions: 83 `.txt` + 1 `.json`.
- **Non-receipts: 60** — 42 `.txt` + 18 `.json`. Kinds: census snapshots (`0`, `145`, `kake W04`
  lines), selftest logs, `argv:` env dumps, `Recorded resolution`, `# Round 59` markdown headers,
  `PASS` logs, r51 met-summary lines. Rule: these are never findings even when rewritten (L5
  analogue holds — 0 events on non-receipts).
- Classification by FIRST version per contract. First-version vs base-version classification is stable:
  0 files flip class between first add and base.
- **Grammar-reading sensitivity** (the decisive number): the contract writes `(?im)^\s*#\s*receipt\s*:`
  OR `EXIT=` OR `^VERDICT:`. Scope of `(?im)`:
  - Reading A (flags cover all alternatives): **95 receipts**
  - Reading B (`EXIT=` case-sensitive, `VERDICT:` ci+multiline): **84 receipts**
  - Reading C (`EXIT=` cs, `VERDICT:` cs, `^` = string start): **83**
  - Reading D (`EXIT=` cs, `VERDICT:` cs+multiline): **84** — no file flips B↔D.
- All 11 A-only files carry lowercase `exit=` in selftest/census/validate tails (e.g. `drift exit=1`,
  `- exit=0 summary=…`): census-before.txt (r52, r55), census-after.txt (r55, r57), c1-selftest-v1/v2,
  c2-selftest-v2, c3-selftest-v2 (r58), a2-selftests-rerun + c2-selftest-v2 (r59), validate-append (r60).
  They are intent-clearly non-receipts → the EXIT= case-sensitive reading matches intent; the span regex
  writes `(?im)` before its whole alternation, so a parallel-flags reading is plausible but wrong here.

## SHAPES:

Marker first-appearance by round (of each receipt's base-version tail):

| marker | rounds observed | count notes |
|---|---|---|
| `EXIT=` (uppercase) | r52–r60, all 84 | the universal marker; several files end `EXIT=0\nEXIT=0` (rerun appends) |
| `met=` | r52–r60 | summary lines like `C2 quote-truth 8/8 met=True` |
| `revision: <sha>` (or `revision=<sha>`) | r52–r60 | canonical indented `  revision: <sha>` tail since r55 |
| `VERDICT:` | r52 only | 2 drift receipts, e.g. `VERDICT: DRIFT — §armed: plazir-gate-anomaly (exit 1)` |
| `conditions_passed` | r52, r55–r60 | in `(met: conditions_passed == N of N)` lines |
| `cases_passed` | r58–r60 | resolver/guard cases |
| `scores_held` | r59–r60 | 3 r59 files carry the R59-D2 term |
| `members=` | r60 only | 4 files |
| `findings=` | r60 only | 3 files |
| `# receipt:` header | r60 only | 16 files (R60-D3 fix); never sole marker — all 16 also carry EXIT= |

Grammar-hit pattern (reading A): 76 EXIT=-only, 16 receipt_hdr+EXIT=, 3 EXIT=+VERDICT:. Neither
`# receipt:` nor `VERDICT:` ever matches alone; `EXIT=` is the only load-bearing grammar token below r60.
`EXIT=0\nEXIT=0` doubled and (r59) `EXIT=0\nEXIT_CODE=0` (`EXIT_CODE` does not match `EXIT=`).

## EDGE CASES:

1. **`.json` receipt — exactly one**: `.ufo/waves/round-52/control/c1-mutation-ladder.json` (4945 B).
   Grammar hits via `"new_tail": "EXIT=1"` inside JSON string values; 21 of 203 lines are span lines
   (`revision:`/EXIT inside quoted case tails). It has 3 rewrite events; every ladder-field edit with a
   quoted revision/EXIT tail counts. A JSON-aware implementation MUST still match string contents.
2. **Multi-line / span-saturated result spans** (span-line count/total at base): `after-c2-guard-cases-t1`
   21/28, `after-c2-guard-cases` 22/31, `c2-b1-tool-under-v2` 23/31 (r60), `c1-selftest-v2` 44/50 (r57),
   `base-c2-resolver-cases` 16/16 (r58 — every line is a span line), `final-verify` 8/71 (r52). On these
   files almost ANY edit is a rewrite event; fixture L4-style "non-result-line" edits barely exist.
3. **Nested-subdir population paths — 19, all non-receipts**:
   - `.ufo/waves/round-37/retained/controls/c2/*.json` ×8 (controls dir is under `retained/`, one level
     deeper still under `c2/`),
   - `.ufo/waves/round-40/controls/w1/CtlKeyFinder/selftest_table.json` (depth 2 under `controls/`),
   - `.ufo/waves/round-48/assimilation/validate/.ufo/waves/round-37/retained/controls/c2/*.json` ×8 and
     `…/validate/.ufo/waves/round-40/controls/w1/CtlKeyFinder/selftest_table.json` ×1 — paths EMBEDDING a
     full `.ufo/waves/round-N/…` subtree inside `round-48/assimilation/validate/`. An anchored regex
     `^\.ufo/waves/round-\d+/(control|controls)/[^/]*\.(txt|json)$` excludes all 19 (nested or
     prefix-shifted), while the frozen population includes them; an unanchored `/controls?/` match
     mis-attributes the embedded copies. `extra_member` needs a pinned path rule.
4. **Files whose first version predates round 40**: r37 ×8 + r40 ×1, first added 2026-10-23 — all
   non-receipts. They make the contract phrasing "FIRST committed version (base..revision …)" ambiguous:
   their first version lies BEFORE base; the walk rule ("after the commit that first added the file")
   requires full-history first-add lookup, not a base..revision restriction. Harmless only because they
   are non-receipts.
5. **Empty files**: none (minimum 2 bytes). UTF-8 paths: none. No symlinks/submodules seen in population
   (all are plain blobs — verify via ls-tree mode 120000/160000 in tool anyway; contract names the note).
6. **`pending` receipts**: only `round-57/controls/after-c1-receipt-pins.txt` had `pending` in its first
   version — but on its own line OUTSIDE the result span (first version = `pending` / `  revision:
   32754df7…` / `EXIT=0`; span = lines 2–3). The contract's rule ("first version's RESULT SPAN contains
   pending") does NOT fire → the routed r57 defect classifies as `rewrite`, never `pending_filled`.
   r52 `drift-before.txt`/`sweep-after.txt` still contain `pending` at base → no event.

## CONTRACT FIT:

- **Event census at base (walk reproduced)**: 12 events, ALL on receipts, ALL kind `rewrite`, all
  commits dated 2026-10-25 (rounds 52–57 era; nothing at the base commit itself). The disclosures JSON
  must carry (path, commit) for ALL 12 or R2's `undisclosed=0` fails:
  - r52: c1-ledger-real.txt @a4a890cf1381; c1-mutation-ladder.json @1ae8de5d4dee, @a4a890cf1381,
    @fd91527a2860; c2-quote-real.txt @a4a890cf1381
  - r54: c1-selftest.txt @8e408e00fbe1, @a631cc0246b9
  - r55: after-c1-readme-index.txt @955e3d7bd6d1; after-c2-quote-truth.txt @955e3d7bd6d1
  - r56: after-c1-selftally.txt @ad06cb8a17bd; **after-c2-quote-truth.txt @ad06cb8a17bd** (the routed
    r56 defect: `revision:` f8438a28→4cb225fb, verified diff: only that line changed)
  - r57: after-c1-receipt-pins.txt @20217f23eca1 (the routed r57 pending-fill — emitted as `rewrite`)
- **`receipts=144` discrepancy (headline)**: R2 expects `receipts=144` but the grammar counts 84 (B) or
  95 (A) population files. Either the summary's `receipts=` counts population paths walked (then a tool
  printing the grammar count fails R2), or the contract intends all 144 as "receipts" (contradicting the
  detection rule and L5's "non-receipt population file"). Builders: pin whether `receipts=` means
  walked-population (144) or grammar-detected (84); L16's `receipts=0` fits the population reading.
- **`(?im)` scope (see CLASSES)**: unpinned; changes the class count by 11 files. The result-span regex
  carries `(?im)` over the whole alternation — parallel construction suggests A, but A misclassifies
  11 selftest/census logs as receipts. Recommend the tool doc pin reading B (`EXIT=` uppercase literal;
  `^VERDICT:` at line start, any case) and the counter fixture add a lowercase-`exit=` control.
- **Rename rule vs reality**: all 12 events are same-path blob changes; no renames observed in
  population history (renames end history per contract — no evidence either direction at base).
- **r57 pending-fill vs pending_filled rule**: with `pending` outside the span, the kind is `rewrite`;
  if the disclosures entry carries `kind: pending_filled` the path/commit match still works (contract
  matches on path+commit only) but narrative kind will diverge from the tool's — name it in the note.
- Duplicated tail lines (`EXIT=0\nEXIT=0`) are normal rerun appends — span SET comparison handles them.
- Tool builders: the span regex `met\s*=` also matches `mismatches=`, `index_mismatches=`? No — `met\s*=`
  requires `met` then `=`; `mismatches=` contains `es=` not `met=`. BUT `met=` matches inside
  `commit=`? No (`mit=`). Verified: `revision=`/`revision:` both in span by design (`revision\s*[:=]`).

VERDICT: 84 receipts vs 60 non-receipts under the intent-matching case-sensitive `EXIT=` reading; 12 rewrite events at base all need disclosure entries; contract must pin the `(?im)` scope (84 vs 95) and the `receipts=` summary semantics (144 population vs 84 grammar hits).
