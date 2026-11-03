# ConnOverlap — round-74 w1: cross-claim and cross-file overlap scan

Seat: connector (read-only; no production file edited, no commit in the lane, no jj call).
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Measured base: `ced2878a1e77f57afb4ee3baebf1021e5130399b`
(`SKILL.md` = 1404 lines). Freeze commit `b35dd4d7` holds the contract and the base controls.
Scratch: `/fast/scratch/hyaku/kake-r74/ConnOverlap` (two `git clone --shared` copies of the lane
plus `git archive` trees; every commit was made only inside those scratch copies with
`-c user.name=ConnOverlap -c user.email=conn@scratch.invalid`, never pushed; toplevel asserted
with `git rev-parse --show-toplevel` before the first commit). Removed before yield (see §Scratch).
Tool installs: none (nothing installed or upgraded this seat).

Axes in play: **calibration** (C1, score 2), **freshness** (C2, score 10), **operability**
(score 10). Every finding below is attached to one of them.

---

## Headline: the drafted rows do not survive the delivered C1 counter

Landing the scribe's drafted section (`.ufo/waves/round-74/w1/ScribeRows.md`, the 31-line block
inside the ```` ````markdown ```` fence) **as drafted** leaves contract §C1 at `met=false`,
exit 1 — with `unregistered=0` and `own_row=true`. The cause is the delivered counter's path
conjunct, which reads the **first backticked `.py` token in a row**, not the Entry-command cell.
Two rows name their successor as a bare filename before their Entry cell:

| Row (line at the drafted tip) | first backticked `.py` token | resolves? |
|---|---|---|
| `c71_tmp.py` (1429) | `c73_tmp_v3.py` (Kind cell: "superseded for this class by `c73_tmp_v3.py`") | no |
| `c72_tmp_v2.py` (1430) | `c73_tmp_v3.py` (same phrasing) | no |

Measured, all on the same scratch history (`--root <scratch> --revision <rev>`):

| revision | tree content | `c74_registry_gap.py` exit | tail |
|---|---|---|---|
| `ced2878a` (base) | no section | 1 | `unregistered=7 met=false` (reproduces `controls/base-c1-registry.txt`) |
| `c9757cbd` | 40-line placeholder section (this seat's stand-in) | 0 | `unregistered=0 met=true`, `path_findings=0` |
| `f0f2d6c7` | **real drafted section**, counter not yet at registry path | 1 | `unregistered=0 own_row=true met=false`, 5 `path_unresolved` |
| `76b9ab3b` | real section + `c74_registry_gap.py` at `.ufo/waves/round-74/c74_registry_gap.py` | 1 | `met=false`, 4 `path_unresolved` (1429, 1430 ×2 counters each) |
| `bf305821` | + the two successor mentions spelled `.ufo/waves/round-73/c73_tmp_v3.py` | 0 | `unregistered=0 met=true`, `path_findings=0` |
| `64e362e2` | + drafted knowledge entry, drafted S441/S442 rows, retained sources | 0 | `unregistered=0 met=true` |

Two separable defects, both cheap to fix and both inside the round's own surfaces:

1. **Registry path.** The counter must be committed at `.ufo/waves/round-74/c74_registry_gap.py`
   (the path its own row's Entry cell names), not only under `w1/ExecC1Counter/`. At
   `f0f2d6c7` the own row is itself a `path_unresolved` finding.
2. **Successor spelling.** The two bare `c73_tmp_v3.py` mentions in Kind cells must resolve. The
   smallest repair that satisfies *both* readings of conjunct 2 (row-entry path only vs every
   path the row names) is to spell them as the full repo path
   `.ufo/waves/round-73/c73_tmp_v3.py`, which also reads better in the registry and changes no
   counter's population (measured at `bf305821`/`64e362e2`: sweep, c70, c73 tmp, wave pointers,
   id_resolver and census all unchanged — see §6 and §Harm).

Contradiction stated, not smoothed: under a narrow reading of §C1 conjunct 2 ("the counter path
named by each such row" = the row's Entry-command path) the counter is over-broad and the draft
is fine; under the counter's own implemented reading the draft fails. The proposed spelling
satisfies both, so the L1 does not have to adjudicate the reading to land a green C1. What the
counter's `--selftest` cannot do is decide it: fixtures f1–f5 (5/5, exit 0) include "entry-command
path not committed" (f4) but **no fixture where a row names a different counter's filename in a
non-Entry cell**, so the over-broad path claim is outside its kill set.

---

## (1) SKILL.md append point and the sweep's sidecar binding

Command (scratch clone at base):

```
python3 - <<'PY'   # over corpus/knowledge/freshness-sidecar.json
entries where file == "SKILL.md": 25   (absent 15 · restored 10)
largest .line: 935
PY
wc -l SKILL.md   → 1404
```

Append point 1405 (after 1404) is **beyond** the largest pinned line 935: 469 lines of headroom.
Confirmed byte-exactly: at the drafted tip `git diff --numstat ced2878a -- SKILL.md` = `32 0`
(32 additions, **0 deletions**) and `tip[:len(base_bytes)] == base_bytes` (prefix identity true,
194134 → 208878 bytes at `64e362e2`).

Simulations and the standing sweep (`node scripts/freshness-sweep.mjs --offline`, `TMPDIR` under
the seat scratch):

| tree | exit | VERDICT line | `paths sidecar binding invalid` | `Error:` |
|---|---|---|---|---|
| base `ced2878a` | 1 | `DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet` | no | no |
| 40-line placeholder at EOF | 1 | identical | no | no |
| real drafted section at EOF (`f0f2d6c7`) | 1 | identical | no | no |
| + counter, repair, knowledge, sources (`64e362e2`) | 1 | identical | no | no |
| **negative control**: the same 40 lines inserted at line 500 | **2** | — | `freshness-sweep: Error: paths sidecar binding invalid: SKILL.md:512` | yes |

`node scripts/freshness-sweep.mjs --selftest` = `selftest: 36/36 passed`, exit 0 (tip6).
So the append-at-EOF discipline is load-bearing and the instrument does see a mid-file pin
break; the drafted bytes keep it. The named drift is the open L0 `~/projects` case only
(`set-delta miss: !! NEW MISS ~/projects`), unchanged from base.

## (2) Scratch-root (`/tmp`) class over the appended rows

```
python3 -B .ufo/waves/round-73/c73_tmp_v3.py --lane <scratch> --revision <rev>
```

| revision | line | exit |
|---|---|---|
| base `ced2878a` | `C2v3 ... attack_accepted=0/0 legit_rejected=0/0 selftest=41/41 findings=[] met=True` | 0 |
| placeholder tip `c9757cbd` | same, `findings=[] met=True` | 0 |
| real section `f0f2d6c7` | same, `findings=[] met=True` | 0 |
| repaired tip `bf305821` | same, `findings=[] met=True` | 0 |
| full landed simulation `64e362e2` | same, `findings=[] met=True` | 0 |

Literal-string greps over the landing bytes (counts of `/tmp`):
`section-real.md` (drafted rows) **0**; drafted knowledge entry `knowledge-block-20.md` **0**;
drafted S441/S442 rows `knowledge-block-257.md` **0**; `ExecC2Tool/sidecar_reobserve.py` **0**;
`ExecC2Counter/c74_sidecar_reobserve.py` **0**; `ExecC1Counter/c74_registry_gap.py` **0**.
The single `/tmp` in `corpus/SOURCES.md` is the pre-existing round-73 S440 row (line 186); the
two new rows (187–188) carry none.

## (3) Pointer counters over a sample round-74 LOG tail

Sample tail appended to `LOG.md` in the scratch tree (round-74 section, 5 added lines):

```
- **Base receipts.** C1 and C2 base receipts at `.ufo/waves/round-74/controls/base-c1-registry.txt` and `.ufo/waves/round-74/controls/base-c2-sidecar.txt`, reproduced by the round-74 counters at `ced2878a`.
```

```
python3 -B .ufo/waves/round-73/c73_wave_pointers.py --root <scratch> --revision <rev>
python3 -B .ufo/waves/round-70/c70_pointer_audit.py  --root <scratch> --revision <rev> --base ced2878a
```

| counter | base | tip (LOG tail present) | round-74 token counted? | resolves? |
|---|---|---|---|---|
| `c73_wave_pointers.py` | `pointers=9 dead=2 annotated=2 unannotated=0 met=true` exit 0 | identical, exit 0 | **no** | n/a (never tested) |
| `c70_pointer_audit.py`, LOG tail only | `pointers=362 dangling=17 annotated=17 unannotated=0 met=true` exit 0 | identical (it never reads `LOG.md`) | **no** | n/a |
| `c70_pointer_audit.py`, same token in a **SCORECARD** row | — | `pointers=364 dangling=19 annotated=17 unannotated=2 met=false` exit 1 | **yes** | **no** at that revision |
| `c70_pointer_audit.py` after the controls are committed | — | `pointers=364 dangling=17 annotated=17 unannotated=0 met=true` exit 0 | yes | yes |

Why: `c73_wave_pointers` fixes its population to the LOG section that starts at `## Round 72 `
and to SCORECARD rows matching `^| 72 |` (`LOG_SECTION_PREFIX`, `SCORECARD_ROW` at lines 87–89
of the counter) — a round-74 tail is outside both, so its `met=true` says nothing about round-74
pointers (the round-73 lesson — `controls/c1-tip.txt` cited but never committed — would recur
here undetected). `c70_pointer_audit` reads `SCORECARD.md` **whole** (`read_scorecard` →
`extract_tokens`), so a `.ufo/...` token in any SCORECARD row is in its population, and its only
resolution test is `git cat-file -e <rev>:<token>`.

**Cross-file hazard for the L1:** if the after-state SCORECARD row cites a receipt that is not
committed at the measured revision (a tip receipt created after the measurement, or a path that
moves), `c70_pointer_audit` flips from exit 0 to exit 1 and the contract's harm battery fails
(`c70 exit 0`). The base receipts under `.ufo/waves/round-74/controls/` are safe: they are
committed at the freeze commit `b35dd4d7`, which is an ancestor of any landing tip — measured
`git cat-file -e <rev>:.ufo/waves/round-74/controls/base-c2-sidecar.txt` = MISSING at the
pre-controls tip, 0 at the controls tip and at HEAD.

## (4) SOURCES S441/S442 — id and URL collisions

`scripts/id_resolver.py --root <scratch> --revision <rev> --fleet /home/vgpnk/Projects/shokunin`:

| revision | exit | summary |
|---|---|---|
| base `ced2878a` | 1 | `ids_cited=121 ids_resolved=118 dangling=3 owned_elsewhere=3 unowned=0` |
| drafted rows + drafted knowledge entry `64e362e2` | 1 | `ids_cited=123 ids_resolved=120 dangling=3 owned_elsewhere=3 unowned=0` |

The three dangling ids are the pre-existing `S303`, `S304`, `S352`; the set does not change.
S441 and S442 are new (no row carried either id at base), each appears exactly once
(`S441 rows: [187]`, `S442 rows: [188]`), and both new URLs are unique in the registry
(`https://docs.python.org/3/library/os.path.html#os.path.exists`,
`https://docs.python.org/3/library/os.html#os.stat` — one occurrence each; the pre-existing
duplicate-URL population is the known `W04` class, unchanged). Fleet census
(`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate <dir>`, read-only):
base lane exit 0 (`rows 178`), drafted tip exit 0 (`rows 180`), warnings only (`W04`).

## (5) c66 gate-status population (rounds 48–59) is untouched

`c66_gate_status_hostportable.py` derives its population from the **tree**, not from SKILL.md:
`population_candidates` keeps paths matching
`^\.ufo/waves/round-(\d+)/(?:[a-z0-9-]+/)?c(\d+)_[a-z0-9_]+\.py$` with `round == counter` and
`48 <= round <= 59`. Reproduced with the module's own functions over both revisions:

| revision | tree entries | population | extra_member | per-frozen-member `rows_mentioning` |
|---|---|---|---|---|
| base `ced2878a` | 20031 | **28** | none | 28 rows, lines 1342+ |
| landed simulation `64e362e2` | 20044 | **28** | none | identical lists |

Direct regex over the new section (nine `|`-starting lines = header + 8 data rows):
`48-59 population hits in new rows: []` (every new
counter path is round 69–74; none satisfies `round == counter` inside 48–59). Non-vacuity
control: injecting a row that names `.ufo/waves/round-50/c50_durable.py` into the new section is
detected by `rows_mentioning` at line 1447 — the check is live, the drafted rows simply do not
trip it. New rows carry 9 pipes each (8 cells), so they parse as registry rows without breaking
`md_tables`.

Latent (not active): `c73_tmp_v3.py` is named in **4** table rows (1404, 1429, 1430, 1432) after
the successor repair. `c66`'s `duplicate_row` class fires on more than one counted row per
member; the class is inert today because 69–73 are out of the 48–59 band, but any future widening
of that band would flag these four rows. Successor mentions are the mechanism; keeping them as
resolving paths does not remove the duplication.

## (6) Does the C2 flip move any sidecar pin?

No. Structure: 174 entries, pinned files and largest pinned line —
`SKILL.md` 25 (max 935), `corpus/SOURCES.md` 9 (max 140), everything else ≤ 321 (max is
`corpus/knowledge/free-read-verbs.md:321`). The append starts at 1405 and the two SOURCES rows
are inserted at 187–188, both **after** every pin in the affected files, so nothing shifts.

Measured after running the delivered tool (`w1/ExecC2Tool/sidecar_reobserve.py --write --date
2026-11-03 --host linux-x86_64`, exit 0, `flipped=144`) on the landed simulation:

- sidecar keys unchanged (174 → 174); entries whose `line` **or** `lineSha256` changed: **0**;
- `kind` flips: 144; `restored=170 absent=4`; the 4 remaining absent are the 3 contract tokens
  (`~/Projects/plazir-15-site` ×2, `~/Projects/webzites/bin/webzites.mjs`,
  `~/Projects/webzites/scripts/kimi-surface.mjs`);
- `history[0].note` equals the prior note bytes for all 144 flips; no restored note matches the
  sweep's absence vocabulary (0);
- SKILL.md pin hashes re-checked directly at the landed tip: **25/25** match;
- `node scripts/freshness-sweep.mjs --offline` after the flip: exit 1, the same single drift,
  **no** `paths sidecar binding invalid`, **no** `Error:` (i.e. the loader validated all 174
  entries, SKILL.md pins included, after both the append and the flip);
- `python3 -B .ufo/waves/round-74/w1/ExecC2Counter/c74_sidecar_reobserve.py --root <scratch>
  --revision <rev>`: base exit 1 (`entries=174 absent=148 restored=26 absent_present=144
  absent_absent=4 restored_absent=0 contradictions=144 met=false`, exactly the contract's base
  numbers), flipped tip exit 0 (`absent=4 restored=170 ... contradictions=0 met=true`).

The 15 flipped SKILL.md entries all pin lines ≤ 935; the flip edits only `date`, `kind`, `note`
and adds `history`, never `line`/`lineSha256`.

---

## Harm check on the proposed landing shape (all measured at `64e362e2`)

| check | result |
|---|---|
| `freshness-sweep --offline` | exit 1, `DRIFT — §paths: 1 unannotated miss`, no binding error, no `Error:` |
| `freshness-sweep --selftest` | `36/36 passed`, exit 0 |
| `c70_pointer_audit --root . --revision HEAD --base ced2878a` | exit 0, `pointers=364 dangling=17 annotated=17 unannotated=0 append_only=true met=true` |
| `c73_wave_pointers --root . --revision HEAD` | exit 0, `pointers=9 dead=2 annotated=2 unannotated=0 met=true` |
| `c73_tmp_v3 --lane . --revision HEAD` | exit 0, `selftest=41/41 findings=[] met=True` |
| `c74_registry_gap --root . --revision HEAD` | exit 0, `unregistered=0 met=true`; `--selftest` `5/5` exit 0 |
| `id_resolver --revision HEAD` | exit 1 (base-consistent), `ids_cited=123 ids_resolved=120 dangling=3` |
| `sources-census.sh validate` | exit 0, `rows 180` |
| SKILL.md diff vs base | `32 0` additions-only, prefix byte-identical |

## Risks

1. **Calibration, high:** landing the drafted rows unedited (with the counter at the registry
   path) yields C1 `met=false` and exit 1 at the landing tip. This is a *kill-rule* failure, not
   a cosmetic one.
2. **Calibration, medium:** `c74_registry_gap --selftest` (5/5) cannot distinguish the
   successor-mention reading, so a green selftest is not evidence the landing is green. If the
   L1 prefers the narrow reading, the counter needs a sixth fixture (successor mention in a
   non-Entry cell) *and* a pre-data predicate note — outside a frozen round.
3. **Freshness, medium:** any SCORECARD row citing an uncommitted receipt flips `c70` to exit 1
   (measured); tip receipts must be committed no later than the measured tip.
4. **Calibration, low:** `c73_wave_pointers` is blind to round-73/74 LOG tails by construction, so
   the round's own pointer battery is vacuous for round-74 pointers.
5. **Latent:** the four rows naming `c73_tmp_v3.py` would be `duplicate_row` for `c66` if its
   band ever widens past round 59.

## Proposed move (one, bounded)

Land the section with two text substitutions and one commit ordering: (a) commit
`c74_registry_gap.py` at `.ufo/waves/round-74/c74_registry_gap.py`; (b) in the `c71_tmp.py` and
`c72_tmp_v2.py` rows, spell the successor as `.ufo/waves/round-73/c73_tmp_v3.py` instead of the
bare `c73_tmp_v3.py`; (c) append the rows at EOF as drafted. This improves **calibration**
(C1: `met=false`/exit 1 → `unregistered=0 met=true`/exit 0, measured at `bf305821` and
`64e362e2`) and, on the measured evidence, harms no other axis: freshness is unmoved (sweep
exit/verdict/binding identical before and after; C2 counter still exit 0 with 170 restored), and
operability is unmoved (`c70` exit 0, `c73_wave_pointers` exit 0, `c73_tmp_v3` `findings=[]`, census
exit 0). It also removes the ambiguity at its source: the row then names a path that a reader can
resolve, which is what conjunct 2 asks for under either reading.

## Scratch

`/fast/scratch/hyaku/kake-r74/ConnOverlap` (clones `lane`, `lane2`, archive trees `fixA`,
`fixB`, `fixB-mid`, `fixC`, `fixE`, `tmp/`) is deleted before yield; the receipts listed above
were copied to `.ufo/waves/round-74/w1/ConnOverlap/receipts/` first. If a later reader finds the
tree on disk, that is this seat's defect.

## Receipts

`.ufo/waves/round-74/w1/ConnOverlap/receipts/` (64 files): `sweep-base.out`, `sweep-tip1.out`,
`sweep-tip4real.out`, `sweep-tip6.out`, `sweep-tip7.out`, `sweep-mid.out`, `sweep-flip.out`,
`selftest-tip6.out`, `code-*` (recorded exit codes), `c74run-*` (per-revision counter runs),
`c74-tip*.json` (JSON diagnoses incl. `path_findings`), `ptr70-tip{1,2,3,6}.out`,
`waveptr-tip{1,3,6}.out`, `tmp-tip{4real,6}.out`, `idres-*.out`, `census-*.out`,
`reobserve-{check,write}.out`. Draft-extracted bytes used in the simulation are beside them as
`section-real.md`, `knowledge-block-20.md`, `knowledge-block-257.md`, and the stand-in
`section.md`.
