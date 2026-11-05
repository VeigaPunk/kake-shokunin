# MutC1 — mutation test of the frozen C1 counter (kake round-95 w1, seat MutC1)

Date 2026-11-05. Target: the frozen C1 counter `.ufo/waves/round-95/c95_selfassess.py`
sha256 `8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193` with its
digest-pinned identity surface `frozen/c1-surfaces.json`
sha256 `00a04c9a68f00de1561d70822a8ff3cab718583de4cd2cbf6ebd06e87b5d47b8`
(the counter's embedded `SURFACES_SHA` equals `00a04c9a…`, so the frozen pair is
internally consistent). The probe measures the round base `fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3`
over committed bytes, exactly as `controls/base-c1.txt` was frozen. This is the
R94-7 evidence test: the round claims its battery now covers its own rule classes.

## Verdict

```
MUT-C1 mutants=16 killed=15 battery_killed=15
```

- Claim floor (>= 2/3 of mutants killed by the counter's own battery+selftest): **met** — 15/16 = 93.75 %.
- Battery kill rate 15/16, against 4/12 for the round-94 instrument
  (`corpus/lessons/round-94.md`, MutC1 row). At the level of this 16-mutant
  population the R94-7 routed defect tests **green**.
- No mutant reached `met=true`; no false-green route exists on these 16 defense points.
- One survivor, M03 (E1-vocabulary, heading-half), plus one supplementary probe of
  the sibling alternative (M03b, body-half) that also survived — a coverage finding,
  not a contract change (analysis below).
- Baseline green: the pristine full run reproduces the frozen receipt
  `controls/base-c1.txt` line 1 **field-for-field**, including `counter=8fd27d62…`,
  and the pristine selftest tail byte-matches `controls/ctl-c1-selftest.txt`
  (`selftest 13/13 planted findings, exit 1 on planted, exit 0 on repaired,
  battery 20/20 admit 5/5 shadow ok, predecessor_admits 10/19, --surfaces-file refused`).

## Method

Scratch root `/fast/scratch/hyaku/kake-r95/MutC1/` (deleted before this report was
finalized; verification line at the end). The pristine counter, surfaces and the
round-94 predecessor (`.ufo/waves/round-94/c94_selfassess.py`, sha `58028584…`,
byte-identical to the lane copy) were copied into a lane-shaped side tree
`env-r95/.ufo/waves/round-95/…` so that `load_surfaces()` and
`predecessor_clean()` resolve exactly as in the lane. Each mutant was staged the
same way under `env-mut/<id>/…`. The audit always reads the **lane's committed
bytes** through read-only git (`git -C <lane> show/cat-file/ls-tree/rev-parse`);
all fixture repos the counter's battery creates live under the scratch `--work`
dirs (the commits are counter-internal, identity `battery@example.invalid`, inside
fresh `git init` fixture dirs). This seat ran no mutating git/jj command itself.

Per mutant `M` (id, class, find, replace), the driver asserted
`pristine.count(find) == 1` (all 16 found exactly once; receipts carry the unified
diffs), then ran, with observed rc recorded per receipt:

1. `python3 -B env-mut/<id>/.ufo/waves/round-95/c95_selfassess.py --selftest` → rc
   (baseline rc 0);
2. `python3 -B env-mut/<id>/.ufo/waves/round-95/c95_selfassess.py --root <lane>
   --revision fdd5fdbe… --work <scratch>/work/<id>` → rc + line 1
   (baseline rc 1; line 1 quoted under Baseline).

Kill rule (as tasked): killed iff selftest rc != 0 OR the baseline line-1 field of
the guarded rule class changes OR the battery verdict fields
(`battery=`/`admit=`/`shadow=`/`predecessor_admits=`/`met=`) change. `revision=`
and `counter=` are normalized before comparison (every mutant necessarily carries
its own `counter=` digest).

Baseline commands (pristine bytes, rc observed):

- `python3 -B env-r95/.ufo/waves/round-95/c95_selfassess.py --root <lane> --revision fdd5fdbe… --work <scratch>/work/baseline` → **rc 1**
- `python3 -B env-r95/.ufo/waves/round-95/c95_selfassess.py --selftest` → **rc 0**

## Baseline (pristine) line 1 at fdd5fdbe

```
C1v95 revision=fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3 counter=8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193 lessons=89 entries=82 rows=255 criteria=39 mismatches=18 E1=0 E2=0 E3=3 E4=0 E5=15 pins=ok battery=20/20 admit=5/5 shadow=absent predecessor_admits=10/19 floor=4 self_pin=ok met=false
```

Identical to `controls/base-c1.txt` line 1 in every field, so the probe's
differential readings are anchored to the frozen receipt, not to a re-derived
baseline. `predecessor_admits=10/19 >= floor 4` confirms the defect routes are
live against the frozen round-94 counter (not blanket refusals).

## The 16 rule-targeted mutants

One mutant per tasked class; each is a single `str.replace` whose find-string
occurs exactly once in the pristine bytes. Full diffs: `MutC1/receipts/M*.diff`;
per-mutant selftest/base/battery receipts: `M*.selftest.txt`, `M*.base.txt`,
`M*.battery.txt`; aggregate: `MutC1/receipts/mutants.json`.

| id | class | single str.replace (find → replace) | selftest rc | line-1 delta vs baseline @ fdd5fdbe (observed) | verdict (channels) |
|---|---|---|---|---|---|
| M01 | E1-heading | `(?m)^## Gate\b…` → `(?m)^## Gats\b…` | 1 | E1 0→89, mismatches 18→107, battery 18/20, admit 0/5 | killed (selftest + battery + baseline-rule E1) |
| M02 | E1-vacuity | `len(nonempty) < 2` → `< 3` | 1 | battery 19/20, admit 0/5 (base audit fields unchanged) | killed (selftest + battery) |
| M03 | E1-vocabulary | `re.search(r"admit", head_line, re.I)` → `"adopt"` | 0 | none — line 1 identical except own `counter=`; battery 20/20, admit 5/5 | **survived** |
| M04 | E2-scope | `CRIT_RE.match(head)` → `CRIT_RE.fullmatch(head)` | 1 | pins ok→short (criteria 39→0), battery 19/20, admit 0/5 | killed (selftest + battery + baseline-rule pins) |
| M05 | E2-blob | E2 branch `!= "blob" or meta[1] <= 0` → `and …` | 1 | battery 19/20 (B18 empty-blob route unrefused) | killed (battery) |
| M06 | E3-rowid | ROW_ID_RE `S[0-9]{3,}` → `{4,}` | 1 | E3 3→80, mismatches 18→95, battery 20/20, admit 0/5 | killed (selftest + battery + baseline-rule E3) |
| M07 | E3-locator | `if TMP_LOCATOR_RE.search(line):` → `if False and …` | 1 | E3 3→2, battery 19/20 | killed (selftest + battery + baseline-rule E3) |
| M08 | E3-multi-source | `len(source_lines) > 1` → `> 2` | 1 | E3 3→1, battery 19/20 | killed (selftest + battery + baseline-rule E3) |
| M09 | E4-indent | `^[ \t]+\|` → `^\t+\|` in the Mistakes row check | 1 | battery 19/20 | killed (selftest + battery) |
| M10 | E4-deletion | `and not mistakes:` → `and mistakes is None:` | 1 | battery 19/20 (B13 deletion route unrefused) | killed (selftest + battery) |
| M11 | E5-suffix-strip | anchor strip `#([^#]*)$` → `#KEEP([^#]*)$` | 1 | admit 5/5→4/5 (C02 anchor-existing no longer admitted) | killed (selftest + battery) |
| M12 | E5-absence-open | ABSENCE_OPEN_RE `[r\d{2,}-absence` → `{3,}` | 1 | battery 19/20 (B12 unrefused) | killed (selftest + battery) |
| M13 | E5-symlink | `meta[2] == "120000"` → `"120001"` | 1 | battery 19/20 (B10 unrefused) | killed (selftest + battery) |
| M14 | identity-path-tokens | `row_tokens.get(cell, 0) < item["path_tokens"]` → `>` | 1 | battery 19/20 (B15 unrefused) | killed (selftest + battery) |
| M15 | identity-content | lesson digest compare `!= item["sha256"]` → `==` | 1 | pins ok→identity, battery 20/20, admit 0/5 | killed (selftest + battery + baseline-rule pins) |
| M16 | cardinality-short | `if pins[k] < v]` → `<= v]` | 1 | pins ok→short, battery 20/20, admit 0/5 | killed (selftest + battery + baseline-rule pins) |

Base-revision sensitivity corroborates the live detections: M07 shows the base's
three E3 findings include one `/tmp`-locator finding (3→2) and M08 shows two
dual-`source:` findings (3→1) — both rule halves catch real findings on the
frozen bytes, not only on synthetic fixtures.

## Survivor M03 + supplementary M03b — coverage finding (E1-vocabulary)

The vocabulary guard is a disjunction:
`if not (re.search(r"admit", head_line, re.I) or re.search(r"admit", body, re.I)): fire`
(and the same shape for `reject`). Observed:

- **M03 (heading-half → `"adopt"`)**: selftest rc 0; full run at `fdd5fdbe…`
  identical to baseline in every field except its own `counter=` digest
  (`battery=20/20 admit=5/5 … met=false`). Receipt `M03.base.txt`.
- **M03b (body-half → `"adopt"`**, supplementary probe outside the required 16,
  `M03b.*` receipts**)**: selftest rc 0; full run likewise identical to baseline
  except `counter=953c664d…`, `battery=20/20 admit=5/5`.

Why neither channel sees either mutant:

1. The base control cannot contribute: `git cat-file -t
   fdd5fdbe…:corpus/lessons/round-95.md` → fatal, exit 128. No lesson of rounds
   >= 95 exists at the measured revision, and the vocabulary rule applies only to
   those — the predicate has zero surface in the base population.
2. Every battery/selftest fixture satisfies BOTH alternatives at once: the junk
   fixtures (B02, selftest r96) carry "admit"/"reject" in neither heading nor
   body (so both mutants still flag them — `refused_ok: true` in both battery
   receipts), and the repaired selftest fixture carries the words in BOTH heading
   and body (`## Gate — admit the fix, reject the junk` + `admit: … / reject: …`),
   so breaking one alternative leaves the other to satisfy the predicate and the
   repaired assertion still reads clean (rc 0).

Reading: the E1-vocabulary **class** is refused by the battery only conjunctively
— each OR-alternative is individually untestable by the counter's own
battery+selftest at the measured revision. Two clean-shape routes would close
this: a >= 95 Gate whose heading carries the decision words over a junk body
(isolates the heading alternative) and a >= 95 Gate with a bare `## Gate` heading
over a decision-worded body (isolates the body alternative). This is a coverage
finding for the lane to consider in a successor battery; the freeze gives this
seat no repair license, and none was taken.

## Instrument provenance observed during the probe (informational)

- At probe start the working tree matched the tasking pins and the instruments
  commit `43cdd9fc…` (= freeze commit `8f638b59…` bytes): counter `8fd27d62…`,
  surfaces `00a04c9a…`.
- Mid-probe the lane briefly carried the "amendment A pre-scoring" pair
  (commit `d9be693f…`, 2026-11-05 13:36:06 -03): counter `04be4a7d…`, surfaces
  `9eff04c5…`, with `controls/base-c1.txt` regenerated to a `counter=04be4a7d…`
  receipt. One scratch staging copy captured those transient bytes.
- HEAD then moved to `4f443b3f…` ("round-95: integrity ruling option (b) - restore
  frozen instrument bytes and controls; amendment A withdrawn from scoring",
  13:47:02 -03) and the tree returned to the frozen pair. The probe ran entirely
  against the frozen `8fd27d62…` bytes; the committed instrument sequence
  (43cdd9fc → 8f638b59 → d9be693f → 4f443b3f) is recorded here because the
  tasking's digest pins name the freeze-time instrument, and the scored
  instrument today is that same restored pair.

## Scope compliance and integrity

Lane bytes this seat reads were never written by this seat. Before/after hashes
(identical):

| file | before = after sha256 |
|---|---|
| `.ufo/waves/round-95/c95_selfassess.py` | `8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193` |
| `.ufo/waves/round-95/frozen/c1-surfaces.json` | `00a04c9a68f00de1561d70822a8ff3cab718583de4cd2cbf6ebd06e87b5d47b8` |
| `.ufo/waves/round-95/c95_conditional.py` | `f09f84090fdda405992d7b51191be8838549e3df402b0898eb2ca00c4c3ff312` |
| `.ufo/waves/round-94/c94_selfassess.py` | `58028584f1aab19a294d24147854f56a703b2442f5af2d32fed69a5a87a8306a` |

`git status --porcelain` over the two instrument paths, `c95_conditional.py`,
`controls/instrument-sha256.txt` and `controls/base-c1.txt` is empty (rc 0) after
the probe. Writes were confined to `w1/MutC1.md`, `w1/MutC1/receipts/` (73 files:
16 diffs, 17 selftest, 17 base, 17 battery receipts, baseline.base,
baseline.selftest, mutants.json, driver.py, m03b.py) and the scratch tree. No
tools were installed (python3/git preexisting); pacman untouched; no sysctl was
read or changed; `/tmp` unused (all temp under scratch `--work`/`TMPDIR`).

## Self-defects recorded

1. Driver v1 staged mutants without the `frozen/` surfaces sibling, so run 1's
   full-report channel was invalid for all 16 mutants (every line 1 was an
   `unevaluable` output; the uniform missing-field pattern exposed it). Fixed by
   per-mutant lane-shaped side trees; run 2 is authoritative. Run 1's selftest
   channel was unaffected and matches run 2 exactly (cross-check).
2. Receipt files echo line 1 twice (the writer prints line 1, then full stdout
   which begins with the same line). Cosmetic only.

## Cleanup statement

Scratch tree `/fast/scratch/hyaku/kake-r95/MutC1/` deleted, and `test ! -e`
verified absent, before this report was finalized. Receipts were copied out
first (73 files under `w1/MutC1/receipts/`).

Report: `.ufo/waves/round-95/w1/MutC1.md`
