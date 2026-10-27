# ExecutorCounterMutation1 — round 62

Seat: advisory leaf. Scope: probe whether deleting the criterion condition from a **copy** of the frozen counter false-greens base. No lane file, claim, counter, criterion, or score was altered.

## Verdict

**No — deleting the criterion condition does not false-green base.** The base control still reports `unresolved=1 quote_correction=0 criterion=0 met=false` with exit `1` under every criterion-deletion mutant, because base independently satisfies none of the four conjuncts (`correction=0`, `lesson_gate=0`). The criterion conjunct is therefore **not** what makes base red.

However, the same deletion **does** false-green a state where every other artifact landed but the QUALITY criterion did not. So the criterion conjunct is load-bearing for exactly the omission it guards, and the *base control alone cannot detect its removal*. Base is an insufficient mutant detector here; the discriminating control is a post-state fixture that carries the correction, lesson gate, and source row but lacks the criterion.

## What was probed

Frozen counter (unmodified, read from the lane):
`.ufo/waves/round-62/c62_calibration.py`, SHA-256 `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d` — matches the frozen value named in the round prompt.

Relevant counter source (`.ufo/waves/round-62/c62_calibration.py:33-40`):

```
correction = int(QUOTE in data["knowledge"] and "S432 §3.6" in data["knowledge"]
                 and "Round-62 correction" in data["knowledge"])
criterion = int(CRITERION in data["quality"] and "round-61-verifier-spotcheck.md" in data["quality"])
lesson_gate = int("## Gate" in data["lesson"] and "S432" in data["lesson"]
                  and "Agree" in data["lesson"] and "Reject" in data["lesson"])
source_row = int("| S432 |" in data["sources"])
resolved = correction == 1 and criterion == 1 and lesson_gate == 1 and source_row == 1
unresolved = disagreements if not resolved else 0
met = unresolved == 0 and resolved
```

`CRITERION = "substantive located quote"` (`.ufo/waves/round-62/c62_calibration.py:20`), matched case-sensitively.

### Mutants (scratch copies only, never in the lane)

| Mutant | Change vs frozen counter |
|---|---|
| `m1_no_criterion_conjunct.py` | `resolved = correction == 1 and lesson_gate == 1 and source_row == 1` — the `criterion == 1` conjunct deleted; the criterion *measurement* is still computed and printed |
| `m2_criterion_removed.py` | m1 plus `criterion = 0` — the criterion *measurement* removed as well |
| `m3_inverted_criterion.py` | `resolved = correction == 1 and criterion != 1 and …` — criterion polarity inverted (control for "condition present but pointing the wrong way") |

Diff for m1 (only line changed):

```
-    resolved = correction == 1 and criterion == 1 and lesson_gate == 1 and source_row == 1
+    resolved = correction == 1 and lesson_gate == 1 and source_row == 1
```

### Fixture states (scratch git repos, `corpus/` at repo root)

Built by exporting the real base blobs `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13:{corpus/lessons/round-61-verifier-spotcheck.md, corpus/knowledge/response-header-expectations.md, corpus/QUALITY.md, corpus/SOURCES.md}` and appending candidate text. `corpus/lessons/round-62.md` does not exist at base (`git show` → `fatal: path 'corpus/lessons/round-62.md' does not exist`), so it was created empty for F0–F4 and appended for the "after" shapes.

| State | Shape |
|---|---|
| `F0_base` | base blobs verbatim (no appends) — base replica |
| `F1_no_criterion` | + substantive S432 §3.6 quote & `Round-62 correction` in knowledge, + `## Gate` lesson; **no** QUALITY criterion |
| `F2_with_criterion` | F1 + QUALITY criterion with exact lowercase phrase **and** verifier pointer (full intended after-state) |
| `F3_criterion_only` | base + QUALITY criterion only (no knowledge correction, no lesson) |
| `F4_knowledge_only` | base + knowledge correction only |
| `G1_capital` | after-state but criterion phrase capitalised: `**Substantive located quote**` |
| `G2_nopointer` | after-state but criterion phrase present without `round-61-verifier-spotcheck.md` pointer |
| `G3_both` | after-state with exact lowercase phrase **and** pointer (duplicate of F2 shape, built in the second fixture pass) |

Fixture hygiene: each fixture repo's root was asserted with `git -C <dir> rev-parse --show-toplevel` (all five/eight roots printed their own path); fixture identities are local (`user.name=Kake R62 Fixture`, `user.email=fixture@example.invalid`) and confined to the fixture repos; no fixture operation touched the lane repo, the fleet repo, sibling repos, or any source tree.

## Measured output (exact)

Frozen base control against the **real lane**, read-only:

```
$ python3 -B ./c62_calibration.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

This matches the round-prompt base control exactly (`unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false exit 1`).

Same revision under the mutants (identical output, so base is **not** false-greened by criterion deletion):

```
m1_no_criterion_conjunct  disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false | exit=1
m2_criterion_removed      disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false | exit=1
m3_inverted_criterion     disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false | exit=1
```

Full fixture matrix (revision prefix stripped for width):

```
F0_base              c62_calibration              disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false | exit=1
F0_base              m1_no_criterion_conjunct     disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false | exit=1
F0_base              m2_criterion_removed         disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false | exit=1
F0_base              m3_inverted_criterion        disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false | exit=1
F1_no_criterion      c62_calibration              disagreements=1 unresolved=1 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=false | exit=1
F1_no_criterion      m1_no_criterion_conjunct     disagreements=1 unresolved=0 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=true  | exit=0
F1_no_criterion      m2_criterion_removed         disagreements=1 unresolved=0 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=true  | exit=0
F1_no_criterion      m3_inverted_criterion        disagreements=1 unresolved=0 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=true  | exit=0
F2_with_criterion    c62_calibration              disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true  | exit=0
F2_with_criterion    m1_no_criterion_conjunct     disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true  | exit=0
F2_with_criterion    m2_criterion_removed         disagreements=1 unresolved=0 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=true  | exit=0
F2_with_criterion    m3_inverted_criterion        disagreements=1 unresolved=1 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=false | exit=1
F3_criterion_only    c62_calibration              disagreements=1 unresolved=1 quote_correction=0 criterion=1 lesson_gate=0 source_row=1 met=false | exit=1
F3_criterion_only    m1_no_criterion_conjunct     disagreements=1 unresolved=1 quote_correction=0 criterion=1 lesson_gate=0 source_row=1 met=false | exit=1
F3_criterion_only    m2_criterion_removed         disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false | exit=1
F3_criterion_only    m3_inverted_criterion        disagreements=1 unresolved=1 quote_correction=0 criterion=1 lesson_gate=0 source_row=1 met=false | exit=1
F4_knowledge_only    c62_calibration              disagreements=1 unresolved=1 quote_correction=1 criterion=0 lesson_gate=0 source_row=1 met=false | exit=1
F4_knowledge_only    m1_no_criterion_conjunct     disagreements=1 unresolved=1 quote_correction=1 criterion=0 lesson_gate=0 source_row=1 met=false | exit=1
F4_knowledge_only    m2_criterion_removed         disagreements=1 unresolved=1 quote_correction=1 criterion=0 lesson_gate=0 source_row=1 met=false | exit=1
F4_knowledge_only    m3_inverted_criterion        disagreements=1 unresolved=1 quote_correction=1 criterion=0 lesson_gate=0 source_row=1 met=false | exit=1
G1_capital           c62_calibration              disagreements=1 unresolved=1 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=false | exit=1
G1_capital           m1_no_criterion_conjunct     disagreements=1 unresolved=0 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=true  | exit=0
G1_capital           m2_criterion_removed         disagreements=1 unresolved=0 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=true  | exit=0
G1_capital           m3_inverted_criterion        disagreements=1 unresolved=0 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=true  | exit=0
G2_nopointer         c62_calibration              disagreements=1 unresolved=1 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=false | exit=1
G2_nopointer         m1_no_criterion_conjunct     disagreements=1 unresolved=0 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=true  | exit=0
G2_nopointer         m2_criterion_removed         disagreements=1 unresolved=0 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=true  | exit=0
G2_nopointer         m3_inverted_criterion        disagreements=1 unresolved=0 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=true  | exit=0
G3_both              c62_calibration              disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true  | exit=0
G3_both              m1_no_criterion_conjunct     disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true  | exit=0
G3_both              m2_criterion_removed         disagreements=1 unresolved=0 quote_correction=1 criterion=0 lesson_gate=1 source_row=1 met=true  | exit=0
G3_both              m3_inverted_criterion        disagreements=1 unresolved=1 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=false | exit=1
```

## Reading of the matrix

1. **Base is not false-greened.** F0 and the real lane base produce identical verdicts under the frozen counter and all three mutants (`met=false`, exit 1). Deleting the criterion condition changes nothing at base, because base already has `correction=0` and `lesson_gate=0`. A criterion-deletion mutation is therefore **invisible to the base control**.
2. **The criterion conjunct is load-bearing for its own omission.** At F1 (everything present except the criterion) the frozen counter correctly refuses (`met=false`, exit 1), while m1/m2 flip to `met=true`, exit 0. So the criterion conjunct is the *only* thing standing between "round-62 landed" and "round-62 landed except the QUALITY criterion" — exactly the artifact the frozen claim names (`criterion_present == 1`).
3. **The mutation is verdict-equivalent to the removal.** m2 (criterion measurement removed as well) is indistinguishable from m1 across all eight states: deleting the conjunct and deleting the measurement have identical observable effects, because once the conjunct is gone the measurement only affects the printed field, never `resolved`.
4. **Inverted polarity is caught only by the after-state.** m3 flips to `met=false` at F2/G3 (the only states where the criterion is actually present), so it is killed by any post-state carrying the criterion but survives base.
5. **The criterion check is literal and case-sensitive.** G1 (`**Substantive located quote**`, capital S) → `criterion=0`; G2 (exact phrase, pointer `round-61-verifier-spotcheck.md` absent) → `criterion=0`; G3 (exact lowercase phrase **and** pointer) → `criterion=1`. Both the exact lowercase phrase `substantive located quote` and the path `round-61-verifier-spotcheck.md` are required, and no other casing/wording counts.

## Note on how `unresolved` is derived (advisory)

`disagreements` stays `1` in every fixture, including F2/G3, because the round-61 `S432 / Fetch … | Disagree |` row (`corpus/lessons/round-61-verifier-spotcheck.md:33`) is deliberately retained — the contract forbids marking it rejected. `unresolved` reaches `0` only because `resolved` short-circuits it (`c62_calibration.py:39`). So the counter's "unresolved" reading is a function of artifact presence, not of a disposition recorded in the verifier row. Consistent with the contract's explicit "keep the row" instruction and not a defect, but it means `unresolved=0` must not be read as "the disagreement row was adjudicated."

## Risks

- **Base control is a weak mutant detector for this counter.** Any future mutation that removes a conjunct other than `correction`/`lesson_gate` leaves base red and is only exposed by a post-state fixture. If the wave wants mutation evidence for the criterion clause specifically, the discriminating control is F1/G1/G2 (everything present, criterion absent), not base.
- **Brittle literal matching.** The criterion detection depends on one exact lowercase substring plus one exact path. A criterion that is semantically stronger but differently worded scores `criterion=0` (G1/G2). Conversely, a sentence containing the phrase and the path with no real criterion behind it scores `criterion=1`. The counter measures artifact presence, not criterion quality.
- **Fixture texts are my own constructions.** The quote, criterion, and lesson strings used here were written to exercise the counter's literals against the real base blobs; they are not the lane's intended wording, and the real after-state has not been committed yet. F2/G3 are therefore *shape* replicas, not the authoritative after-state.
- **Fixture repos carry throwaway identities** (`Kake R62 Fixture <fixture@example.invalid>`), local to the fixture repos only, removed with the scratch tree.

## Lane integrity

- Lane HEAD unchanged: `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`.
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain` → `?? .ufo/waves/round-62/` only (the pre-existing untracked wave directory; this seat's report file lives inside it). No tracked lane file modified; no index, branch, or Git state touched.
- Frozen counter SHA-256 re-verified as `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d` after all probes.
- No pacman transaction, no install, no network fetch. Tools used: `git`, `python3` (standard library only), `diff`, `sha256sum`, `grep`, `ls`, `sed`/`cat` via shell reads — all pre-installed.
- Scratch confined to `/fast/scratch/hyaku/kake-r62/ExecutorCounterMutation1/`, deleted before yield. No writes outside this seat's report path and that scratch tree.

## Evidence commands

```
cd /fast/scratch/hyaku/kake-r62/ExecutorCounterMutation1
cp /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/c62_calibration.py ./c62_calibration.py
sha256sum ./c62_calibration.py
python3 -B ./c62_calibration.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13; echo "exit=$?"
diff -u c62_calibration.py mutants/m1_no_criterion_conjunct.py
for st in F0_base F1_no_criterion F2_with_criterion F3_criterion_only F4_knowledge_only G1_capital G2_nopointer G3_both; do
  FX=$PWD/fx/$st; R=$(git -C $FX rev-parse HEAD)
  for c in c62_calibration.py mutants/m1_no_criterion_conjunct.py mutants/m2_criterion_removed.py mutants/m3_inverted_criterion.py; do
    python3 -B ./$c --root $FX --revision $R; echo "exit=$?"
  done
done
```

## Recommendation (advisory only — no claim, counter, criterion, or score altered)

Keep the frozen counter untouched; the criterion conjunct is doing real work and the base control alone does not prove it. If the wave wants a mutation record for this clause, cite F1/G1/G2 as the killing states (frozen `met=false`/exit 1 vs mutant `met=true`/exit 0) and state explicitly that base is non-discriminating for this mutation. Separately, whoever writes the QUALITY append must use the exact lowercase phrase `substantive located quote` and include the literal path `round-61-verifier-spotcheck.md`, or the frozen counter will score `criterion=0` for a semantically correct criterion.
