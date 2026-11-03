# Round 74 — adversarial review of the frozen contract (CriticClaims)

Seat: `CriticClaims` · lane `/home/vgpnk/Projects/shokunin/kake-shokunin` · base
`ced2878a1e77f57afb4ee3baebf1021e5130399b` · freeze commit `b35dd4d7` · measured at the base
revision only (no after-state exists). Every number below is from a command I ran in this seat;
scratch tree `/fast/scratch/hyaku/kake-r74/CriticClaims/`, deleted before yielding.

Scope: attack the approach, not the owner. Findings are limited to defects that can change a
verdict, plus the smallest correction that closes each one. No production byte was touched.

---

## 0. Base facts I established (so the critiques below are grounded)

| Fact | Command | Result |
|---|---|---|
| all 8 population paths resolve | `git cat-file -e <rev>:<path>` ×8 | exit 0 ×8 |
| independent registry scan | row = line whose `lstrip()` starts `\|` | rows=0 for 7 counters; `c73_tmp_v3.py` rows=1 (line 1404); `c72_tmp_v2.py` appears in **prose** line 1400 only |
| population completeness | per-round `git ls-tree` top-level `c*.py` | r69=2, r70=1, r71=2, r72=1, r73=2 → exactly the 8 named (wave copies under `w1/` are duplicates, not extra claims) |
| sidecar shape | `json.load` | 174 entries, no `history` key anywhere; absent=148, restored=26 |
| host probe | `os.stat` vs `os.path.exists` over all 174 tokens | agree on **174/174**; 144 absent→present, 4 absent→absent, 26 restored→present, **0 unevaluable** |
| genuine absences | distinct absent tokens that do not stat | 3 tokens / 4 entries: `~/Projects/plazir-15-site`×2, `~/Projects/webzites/bin/webzites.mjs`, `~/Projects/webzites/scripts/kimi-surface.mjs` |
| max pinned `SKILL.md` line | sidecar entries with `file=="SKILL.md"` | 25 entries, min 16, **max 935** |

The `controls/base-c1-registry.txt` and `controls/base-c2-sidecar.txt` receipts reproduce exactly
against these checks. The control receipts are honest. The defects are in the *predicates*, not in
the pre-freeze measurement.

---

## 1. Claim C1 — calibration

### 1.1 Population: correct. No change.

Rounds 69–73 name exactly the eight counters in the table, each under its own round directory:
r69 §C1/§C2 → `c69_recorded_counts.py`, `c69_tmp_honour.py`; r70 §C1 → `c70_pointer_audit.py`;
r71 §C1/§C2 → `c71_calibration.py`, `c71_tmp.py`; r72 §C2 → `c72_tmp_v2.py`; r73 §C1/§C2 →
`c73_wave_pointers.py`, `c73_tmp_v3.py`. Round-72's contract also *references* `c56_selftally.py`,
`c66_gate_status_hostportable.py` and `c71_tmp.py`; round-73 references `c72_tmp_v2.py`. The
"each under its own round directory" qualifier correctly excludes the referenced (not owned)
counters, and the 8-row enumeration is what the predicate freezes. Two wave copies exist
(`round-69/w1/ExecC1Counter/c69_recorded_counts.py`, `round-73/w1/ExecC2Counter/c73_tmp_v3.py`, …);
the population is an explicit table, so they are not silently doubled. **Keep as written.**

### 1.2 Counterexample A — "any cell" is a false-positive test, proven at base

The frozen rule is: "a table row whose cells contain its exact filename … a row naming the counter
in any cell counts". The registry already contains a row where that rule fires falsely:

- `SKILL.md:1198` (round-47 section) gates `scripts/redirect_audit.py` — its **Name** cell is
  `redirect-expectation-audit`, its **Entry command** cell runs `scripts/redirect_audit.py`.
- Its **cell 5** ("Pinned values / frozen proof") contains
  `python3 -B .ufo/waves/round-46/c46_matrix.py --root . --revision <rev> --stage before|after`.
- `c46_matrix.py` appears in **no other row** (column scan: one occurrence, column 5, line 1198).

So under the literal rule `c46_matrix.py` is "registered" by a row that does not gate it. This is
not hypothetical — it is the registry's own style: cell 5 routinely cites *other* counters as
witnesses (`c58_receipt_rewrites` at line 1396, `c57_idresolver_gate` at 1356). Applied to the
round-74 population, the same shape lets the round be met by a provenance sentence.
`controls/base-c1-registry.txt` is clean only because none of the 8 happens to appear in a notes
cell at base; the rule, not the data, is what an executor inherits.

### 1.3 Counterexample B — one dump row satisfies all eight conjuncts 1

Nothing in conjunct 1 requires one row per counter, or that the row's **Entry command** runs the
counters it names. A single row of the form

`| c69_recorded_counts.py c69_tmp_honour.py … c73_wave_pointers.py | gate | python3 -B .ufo/waves/round-73/c73_tmp_v3.py --revision <rev> | … |`

satisfies "at least one row whose cells contain its exact filename" for all eight. Conjunct 2 then
becomes ill-defined: it is written in the singular ("the counter path named by each such row"), and
a row naming eight counters has no single path. Either reading is bad — under the population-path
reading conjunct 2 is inert (see 1.4); under the command-cell reading it is undefined.

### 1.4 Does conjunct 2 add anything? No, as worded — and when bound, it checks the wrong property

- **As population-path check:** inert. All 8 paths resolve at base (`git cat-file -e` = 0 ×8); the
  check can never fail for a counter that is present in its frozen table.
- **As command-cell check:** it still only proves the *path string* resolves. It cannot catch a row
  whose command is not operable, and the population's flag surfaces are heterogeneous:

| counter | plausible row command | exit at base |
|---|---|---|
| `c69_recorded_counts.py` | `--root . --revision <rev>` | **2** (`--pairs is required`) |
| `c69_tmp_honour.py` | `--root . --revision <rev>` | **2** (`--work` required) |
| `c71_calibration.py` | `--lane . --revision <rev>` | **2** (`C1 unevaluable: stated attack-share population is 2, frozen population is 1`) |
| `c71_tmp.py` | `--revision <rev>` | **1** (`guard=fail met=False`) |
| `c72_tmp_v2.py` | `--lane . --revision <rev>` | 0 (`findings=[]`) |
| `c72_tmp_v2.py` | `--root . --revision <rev>` | **64** (usage) |
| `c70_pointer_audit.py`, `c73_wave_pointers.py`, `c73_tmp_v3.py` | `--root . --revision <rev>` / `--revision <rev>` | 0 |

Five of the seven unregistered counters are **not green at base** under their own natural flags.
A registry row that labels them `gate (live)` would be exactly the miscalibration C1 claims to
repair, and the predicate cannot see it. This is a known failure mode in this very registry: c66 at
base reports `mismatches=3`, including two `MISMATCH live_not_green`
(`c58_resolver_cases.py`, `c59_resolver_cases.py`), while still exiting 0. Registering more `live`
labels without an exit check repeats that defect by construction.

### 1.5 C1 and C2 are **not** separable as frozen — measured

C1 edits `SKILL.md`; C2's sidecar pins 25 `SKILL.md` lines (`line` + `lineSha256`) and the sweep
rejects any drift with `paths sidecar binding invalid`. Measured on scratch copies of the base tree:

- insert one registry row at line 512 → `node scripts/freshness-sweep.mjs --offline` →
  `Error: paths sidecar binding invalid: SKILL.md:512`, **exit 2**;
- append the same 17 lines after EOF (new line count 1420) → same `VERDICT: DRIFT …` **exit 1**,
  `--selftest` **36/36 exit 0**.

Max pinned `SKILL.md` line is 935. So C1 is separable **only if** every `SKILL.md` addition lands
above 935, or is re-pinned in the same commit. The contract states this discipline nowhere for
round 74 (round-73's prose recorded it for its own section, but round 74 does not inherit it by
reference). An executor who registers `c69_recorded_counts.py` inside the round-69 section — the
most natural placement — kills C2 outright.

### 1.6 Receipt / reproducibility defect

`controls/base-c1-registry.txt` prints `C1v1 revision=… population=8`, per-counter
`<name> rows=N file_exit=0`, and `unregistered=7 met=false`. It has **no `own_row` line**, while the
predicate and kill rule require `own_row`. A counter that must report `own_row=false` cannot
reproduce the receipt "exactly" (byte-identical stdout). The meaning of `file_exit` is also
undefined anywhere in the contract. "Reproduce exactly" is therefore unsatisfiable as literally
worded, independent of the counter's correctness.

### C1 verdict: **amend-before-data**

Impacted axis: calibration (and freshness through 1.5). Smallest corrections, in order:

- **A1 (registration test).** Credit a row only when the filename appears in the **Name**, **Entry
  command**, or **Self-test** cell. A filename appearing *only* in Kind/Verdict/Pinned/Write-scope/
  Owner does not count. This keeps frozen fixture f2 ("a row naming a counter in a non-first cell
  must count" — entry-command and self-test cells are non-first) and kills the `c46_matrix.py`
  false positive.
- **A2 (one counter per row).** A row credits exactly one population counter, and conjunct 2 binds
  to the path in **that row's** entry-command cell: `git cat-file -e <rev>:<path-from-cell-2>`
  exits 0. This fixes the singular/plural ambiguity and the one-dump-row exploit, and makes f4
  meaningful.
- **A3 (`own_row` bound).** Define the round-74 section as the rows between the first
  `### Round 74` heading and EOF; `own_row=true` iff a row in that block names
  `c74_registry_gap.py`. Otherwise any row anywhere in 1 400 lines satisfies it.
- **A4 (label honesty).** Each new row's Kind label must agree with the counter's exit at the
  measured revision: `live` only for exit 0; otherwise `historical`/`never met` with its pinned
  revision (the registry already uses both labels). Without this, C1 can be "met" while its own
  axis is harmed by five new false claims (evidence in 1.4).
- **A5 (placement).** All `SKILL.md` additions append after line 935, or the sidecar is re-pinned in
  the same commit. Evidence in 1.5.
- **A6 (reproduction).** Define `file_exit`, and read "reproduce exactly" as the receipt's named
  fields (plus the per-counter rows), not byte-identical stdout — the receipt predates `own_row`.

---

## 2. Claim C2 — freshness

### 2.1 `kind=restored` + `history`: honest representation — keep, with one vocabulary hole

Two facts settle the laundering question:

- The lane's own 26 existing `restored` entries already use this vocabulary for present-state
  re-observation: *"2026-10-21: ~/Projects/ds4cc-marketplace present (test -e exit 0; checkout
  1fbdb8ed); prior local-state annotations at SKILL.md:16 are historical."* `restored` here means
  "prior absence annotation superseded", not "the object vanished and returned".
- The after-state **improves** on that precedent: conjunct 2 preserves the prior note byte-for-byte,
  which the 26 existing entries do not do (`history` count over all 174 entries: **0**). The new
  note is dated, host-classed and states `stat ok`, so it is a dated present-tense observation, not
  an unbounded claim.

But conjunct 3's banned vocabulary is **too narrow**, and I measured the hole. The sweep's regex is
`/absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing/i`. On a
scratch copy of the flipped tree I rewrote one restored note to
*"… present (stat ok …); the directory was **removed** and later **reappeared**; prior annotation
preserved under history."* Result: `--selftest` 36/36, `--offline` exit 1, **no binding error** —
the false historical claim ("it disappeared and came back") passes both the frozen predicate and
the standing instrument. `removed`, `deleted`, `purged`, `returned`, `reappeared`, `came back`,
`recreated` are exactly the words that launder an erroneous prior note into a fabricated event.

### 2.2 Is `unevaluable==0` achievable? Yes on this host, but the kill rule mislabels the failure

Measured over the frozen population on this host: `os.stat` → 0 unevaluable; `os.path.exists` →
also 0; the two probes agree on 174/174 entries, so the `exists` vs `stat` substitution cannot change
the count **on this population** (it can only diverge on EACCES/ELOOP, of which there are none here).
So the predicate is achievable and the base receipt is reproducible by a stat-based counter.

The defect is severity, not feasibility: the counter spec assigns `2=unevaluable`, and frozen
fixture g3 requires exit 2 for an unevaluable probe — yet the kill rule says "C2 fails if …
`unevaluable > 0`". A measurement failure is not a failed claim. The same collision exists in C1:
the kill rule says "C1 fails if … any population row's counter path does not resolve", while f5
requires a missing counter to be `unevaluable`. In both claims a 2 will be scored as a kill, which
is the exact instrument-defect-as-falsification pattern already filed as an L0 by `revenger` for
round 69 (`.ufo/l0-questions.md:160`).

### 2.3 Does C2 depend on the open L0 `kake | round-69` case? Only pedantically — clarify

`.ufo/l0-questions.md:260` is the open case (lowercase `~/projects`; three possible rulings:
annotate+pin, restore the path, or accept host-bound debt). I tested the two cheap rulings:

- add `~/projects` to `pins.pathsMissSet` → `--offline` still **exit 1**, verdict line becomes
  `1 unannotated miss · 0 NOT in pins.pathsMissSet` — drift class unchanged, so conjunct 4 still
  passes;
- annotate the six unannotated citations (the other obvious ruling) → drift disappears → **exit 0**,
  which conjunct 4 also allows;
- creating the lowercase directory → token resolves → **exit 0**, also allowed.

So no likely L0 ruling blocks C2. The residual risk is purely textual: conjunct 4 demands "the same
single named drift class", which has no referent once the drift is fixed. State that zero drift is
a pass.

### 2.4 Is the target reachable by a do-nothing round? No

The base sidecar with no edits still has 148 `absent`, 144 of which resolve → `contradictions=144`,
exit 1. Flipping requires a sidecar rewrite; token existence is host state and cannot flip `kind`.
The base receipt is therefore a real do-nothing control, and the target is not reachable by
inaction.

### 2.5 Reachability of the target itself — verified end to end

I built the base tree with `git archive`, flipped the 144 contradicted entries exactly as the
contract specifies (kind→restored, date `2026-11-03`, note with date + host class + `stat ok`,
prior `{date,kind,note}` pushed to `history`), and ran the standing instrument:

- `node scripts/freshness-sweep.mjs --selftest` → `36/36 passed`, **exit 0**;
- `node scripts/freshness-sweep.mjs --offline` → `VERDICT: DRIFT — §paths: 1 unannotated miss ·
  1 NOT in pins.pathsMissSet`, **exit 1**, no `Error:` line, no `paths sidecar binding invalid`.

The 4 genuinely absent entries stay `absent`; the 26 restored entries are untouched. The sweep's
`resolve 32 / declaredAbsent 64 / drift 1` counts are unchanged by the flip, because the flipped
tokens were already resolving. **No hidden regression from the flip itself.**

### 2.6 Missing input for conjunct 2's byte-for-byte check

Conjunct 2 and the kill rule require that "any history entry differs from the base note bytes" be
detectable. The counter is specified with `--revision <rev>` and `--root` only. At the tip, the base
note exists only inside `history`; a counter that trusts `history` cannot detect self-consistent
laundering. Either the base revision must be pinned in the counter (per-entry note sha256), or a
`--base <rev>` argument must be added. As frozen, the check is unexecutable from the stated inputs.

### 2.7 Receipt / field-name inconsistency

`controls/base-c2-sidecar.txt` prints `absent_present=144 … restored_absent=0`, while the predicate
requires the counter to print `absent_notes_resolving=0 restored_notes_absent=0 unevaluable=0
met=true`. Same quantities, different names. "MUST reproduce it exactly" and "prints <X>" cannot both
be literal unless the counter prints both field sets — say which.

### C2 verdict: **amend-before-data**

Impacted axis: freshness. Smallest corrections:

- **B1 (severity).** Kill rules read: *not met* for 1-conditions; *unevaluable* (exit 2, not a kill)
  for probe/permission/revision failures. Applies to C1's f5 vs "path does not resolve" collision
  too.
- **B2 (vocabulary).** Extend the banned restored-note vocabulary with
  `removed|deleted|purged|returned|reappeared|came back|recreated`. Measured: the current list lets
  "removed … reappeared" through the sweep and would let it through the counter.
- **B3 (base bytes).** Add `--base <rev>` or hardcode the base sidecar's per-entry note sha256, so
  conjunct 2 is checkable from the tip.
- **B4 (L0 wording).** Conjunct 4 accepts *zero* drift as a pass; only a **new** drift class,
  exit 2, or an `Error:` line fails.
- **B5 (field names).** One field-name set for both the base receipt and the predicate output, or
  require the counter to print both.

---

## 3. Controls

| Control | Verdict | Evidence |
|---|---|---|
| `base-c1-registry.txt` | **scores the do-nothing control only by identity** | "no rows added" at base *is* the do-nothing outcome, and the receipt's `unregistered=7 met=false` matches an independent row scan. But the receipt was produced by a pre-freeze probe, the counter does not exist at base, `file_exit` is undefined, and the receipt omits `own_row` (see 1.6). Reproduction must be defined as named fields. |
| `base-c2-sidecar.txt` | **reproduced exactly; probe choice cannot change the count** | my stat probe gives 144/4/0, 26/0/0, 3 genuine tokens — identical. `os.stat` and `os.path.exists` agree on 174/174 tokens. Divergence is possible only on EACCES/ELOOP, absent here. Keep, with the field-name amendment (2.7). |
| `base-c2-sweep.txt` | **reproduced exactly** | `--selftest` 36/36 exit 0; `--offline` exit 1, `VERDICT: DRIFT — §paths: 1 unannotated miss … 1 NOT in pins.pathsMissSet`, and the 144 contradictions are nowhere in the output — the standing instrument is blind to them, exactly as claimed. |

---

## 4. Harm battery at base — nothing listed is red, but three lines are mis-specified

Measured at `ced2878a`:

| Check | Exit | Verdict |
|---|---|---|
| `node scripts/freshness-sweep.mjs --selftest` | 0 | 36/36 |
| `node scripts/freshness-sweep.mjs --offline` | 1 | same single `~/projects` drift, no `Error:` |
| `c66_gate_status_hostportable.py --root . --revision <rev> --work <scratch>` | 0 | `members=28 evaluated=28 mismatches=3 structural=0 agreement=25 scores_held=3/3 met=True` |
| `c70_pointer_audit.py --root . --revision <rev>` | 0 | annotated dead lines only |
| `c72_tmp_v2.py --lane . --revision <rev>` | 0 | `findings=[]` |
| `c73_wave_pointers.py --root . --revision <rev>` | 0 | `pointers=9 dead=2 annotated=2 unannotated=0 met=true` |
| `c73_tmp_v3.py --selftest` | 0 | `41/41` |
| `c73_tmp_v3.py --revision <rev>` | 0 | `findings=[] met=True` |
| `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` | **127 from the lane root**; **0 from the fleet root** | `kake ok`; the script lives only at `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` |

Defects in the battery text:

1. **Census path.** `scripts/sources-census.sh` does not exist in the lane (`bash scripts/…` from
   `/home/vgpnk/Projects/shokunin/kake-shokunin` → `No such file or directory`, exit 127). Name the
   absolute fleet path or the fleet cwd; otherwise the check is unverifiable as printed.
2. **`c72_tmp_v2.py` flag.** The battery gives no command; the counter accepts `--lane`, not
   `--root` (`--root` → 64). Same for `c73_tmp_v3.py` (`--lane`). Print the command.
3. **c66 base numbers unpinned.** "agreement unchanged from base" has no base value in the
   contract; measured 25. Pin `members=28 evaluated=28 mismatches=3 structural=0 agreement=25
   scores_held=3/3` so "unchanged" is decidable.
4. **The `/tmp` clause is unenforced and unscoped.** It says "no `/tmp` code literal in any new or
   edited file (`c73_tmp_v3.py` stays green over `SKILL.md`)". `c73_tmp_v3.py` reads **only
   `SKILL.md`** (`PATH = "SKILL.md"`), so the round's three new files — `scripts/sidecar_reobserve.py`,
   `.ufo/waves/round-74/c74_sidecar_reobserve.py`, `.ufo/waves/round-74/c74_registry_gap.py` — are
   never scanned. And the contract file itself already contains `/tmp` twice (lines 104, 135), so
   "any new or edited file" has no defined scope. Replace with: grep `git diff --name-only
   <base>..<tip>` over the three new/edited paths for the literal, or state that the clause covers
   only `SKILL.md`.
5. `git diff <base>..<tip> -- corpus/SOURCES.md` cannot be red at base (tip == base); it is a
   post-state check, not a base control. Fine, but it should not be counted as "scored" before data.

---

## 5. Verdict per claim

| Claim | Verdict | Reason (one line) |
|---|---|---|
| **C1** | **amend-before-data** (A1–A6) | The population is right and the receipts reproduce, but "any cell" is a proven false-positive rule (`c46_matrix.py`), one row can satisfy all eight, conjunct 2 is inert-or-ambiguous and never tests operability, `own_row` has no section bound, five of the seven counters are not green at base, and a natural mid-file placement kills C2 with a measured exit 2. |
| **C2** | **amend-before-data** (B1–B5) | `restored`+`history` is the lane's established vocabulary and the flip is reachable and regression-free (measured), but the banned vocabulary misses removal/reappearance verbs, unevaluable is mis-scored as a kill, conjunct 2's byte check has no base input, the L0 wording needs a "zero drift is a pass" clause, and the receipt's field names differ from the predicate's. |

No claim is killed: both have a real defect behind them (measured at base), both are reachable, and
both repairs are local. No axis is harmed by the corrections; A4 would additionally stop C1 from
scoring "met" while adding five false `live` labels.

## 6. Impacted axes

- **calibration** — A1/A2/A4 (the registry can be satisfied without gating or without truth).
- **freshness** — A5 (C1's placement can break the sidecar binding), B2 (false historical claims),
  B1 (kill-by-instrument-defect).
- **separability** — C1 and C2 share `SKILL.md`; the contract freezes no placement rule. This is the
  only finding that can turn a green C2 into exit 2 through an unrelated claim's edit.

---

## 7. Commands run (exact, with exits)

All read-only; scratch under `/fast/scratch/hyaku/kake-r74/CriticClaims/`, removed on exit. No git
mutation in the lane; fixture trees were `git archive` extractions.

```
git -C <lane> rev-parse --show-toplevel                 -> /home/vgpnk/Projects/shokunin/kake-shokunin (0)
git -C <lane> rev-parse HEAD                            -> b35dd4d7… (0)
git cat-file -e <base>:<8 paths>                        -> 0 ×8
independent row scan over SKILL.md@base                 -> rows 0×7, c73_tmp_v3 rows=1@1404, c72_tmp_v2 prose@1400
git ls-tree .ufo/waves/round-{69..73}                   -> 8 owned counters, no extra claim
python3 stat-vs-exists probe over 174 tokens            -> 174/174 agree; 144/4/0 + 26/0/0; 0 unevaluable
c69_recorded_counts.py --root . --revision <base>       -> 2  (--pairs required)
c69_tmp_honour.py --root . --revision <base>            -> 2  (--work required)
c70_pointer_audit.py --root . --revision <base>         -> 0
c71_calibration.py --lane . --revision <base>           -> 2  (stated population 2, frozen 1)
c71_tmp.py --revision <base>                            -> 1  (guard=fail met=False)
c72_tmp_v2.py --lane . --revision <base>                -> 0  (findings=[])
c72_tmp_v2.py --root . --revision <base>                -> 64 (usage)
c73_wave_pointers.py --root . --revision <base>         -> 0  (met=true)
c73_tmp_v3.py --revision <base>                         -> 0  (findings=[])
c73_tmp_v3.py --root . --revision <base>                -> 64 (usage)
c73_tmp_v3.py --selftest                                -> 0  (41/41)
node scripts/freshness-sweep.mjs --selftest             -> 0  (36/36)
node scripts/freshness-sweep.mjs --offline              -> 1  (DRIFT ~/projects, no Error:)
c66_gate_status_hostportable.py --root . --revision <base> --work <scratch>
                                                        -> 0  (28/28, agreement=25, met=True, 83 s)
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root … kake
                                                        -> 0  (kake ok; 127 when invoked as scripts/ from the lane)
git archive <base> | tar -x -C <scratch>                -> 0
flip 144 absent→restored with history, then inspect     -> 144 flipped, 4 kept absent
  node scripts/freshness-sweep.mjs --selftest           -> 0  (36/36)
  node scripts/freshness-sweep.mjs --offline            -> 1  (same verdict, no binding error)
restored note "removed … reappeared", re-run            -> 36/36, exit 1, NOT caught  (vocabulary hole)
insert one registry row at SKILL.md:512, re-run         -> 2  (Error: paths sidecar binding invalid: SKILL.md:512)
append 17 registry lines at EOF (1420 lines), re-run    -> 1 + 36/36  (safe path)
add ~/projects to pins.pathsMissSet, re-run             -> 1  (0 NOT in pins.pathsMissSet, drift class unchanged)
```

Tooling: no installs, no upgrades, no pacman transactions. Scratch tree removed before yield.
