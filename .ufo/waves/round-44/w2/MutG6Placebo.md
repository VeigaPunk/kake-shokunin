# MutG6Placebo — G6 placebo mutation probe (case-memo witnesses)

Axis: operability. Freshness untouched. Role: mutation-tester. One mutation probe, one verdict.

## Verdict

**PASS against the item's named attack.** The mutant (a G6 that delegates to the counter's
`cases_f` generator) **survives** — it is **killed** by the detector in the sense that the
item's hypothesis is **refuted**: the placebo G6 does **not** witness the casememo controls
on **any** seed. No seed exits 1, so **there is no lucky seed** for the G6 seat to check, and
the witnessing of the four casememo controls cannot be attributed to the harness or to luck in
the shared run-F corpus. It is attributable to G6's own fold-pair shapes.

The mutant is **not** a vacuous pass: the identical detector **does** fire (probe exit 1) on
the same four controls when the class module carries G6's real shapes, so the zero result is a
property of the mutant, not of the detector.

- Mutant: `classes/g6_fold_pairs.py` `cases()` replaced by `return h.cases_f(rng)`.
- Expected detector: `c44_probe.py --class G6 --tool-file <casememo control> --seed N` exits 1 (witness) for a control whose memo the class's shapes can trigger; exits 0 (equal, no witness) otherwise.
- Output: 80/80 rows exit 0 on seeds 1..20 (all four casememo controls); 800/800 rows exit 0 on seeds 1..200.
- Verdict: **mutant survived** (no witness on any seed) → the named attack **fails**.
- Restoration: scratch bytes restored to `f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d`; lane repo never written by this seat.

## What the attack was, precisely

The hypothesis in the item is *falsified*, not confirmed: "a placebo G6 delegating to
`cases_f` would still witness casememo controls on some seeds by luck — proving G6 is not what
does the witnessing." The probe found the opposite: the placebo G6 witnesses **nothing**, on
any seed tried. So the witness, once G6 is fixed, rests on G6's own shapes and cannot be
explained by luck in the shared corpus.

The mutant is byte-equivalent to the frozen placebo class, so this is a measurement of the
shipped placebo's own behaviour:

```
$ python3 -c "import re; a=open('repo/.ufo/waves/round-44/classes/g6_fold_pairs.py').read(); \
b=open('/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/classes-placebo/g6_fold_pairs.py').read(); \
ga=re.search(r'def cases.*',a,re.S).group(0).strip(); gb=re.search(r'def cases.*',b,re.S).group(0).strip(); \
print('mutant cases() == frozen placebo cases():', ga==gb); print(' ',repr(ga))"
mutant cases() == frozen placebo cases(): True
  'def cases(rng, h):\n    return h.cases_f(rng)'
```

Mutant bytes (scratch only): `7926c8d271d07a2ad431c491583091d630f7713094793036f62ce1afd4486007`
Frozen placebo bytes: `b827ec1cd2b5e2144aa6c14ae3590b7ae6ff17488e9e93a9173b4bb63aea5f54`

## Setup (scratch only; lane repo never written)

Scratch root `/fast/scratch/hyaku/kake-r44/MutG6Placebo/`. A `git clone --no-checkout --shared`
of the lane repo gives the probe a git root so `c44_count_v5.py`'s `git show` of the pinned
round-41 revision works (`REF41_REV 1ef7a0e9…`, sha256 `50287ac6de5600ab…` == `REF41_SHA`).
The frozen `classes/`, `controls-r43/`, `c44_probe.py`, `c44_count_v5.py` and `c44_placebo.py`
were copied into it unchanged; the class dir was the only thing mutated.

```sh
git clone --no-checkout --shared /home/vgpnk/Projects/shokunin/kake-shokunin repo
cp -a $L/.ufo/waves/round-44/classes        $R/.ufo/waves/round-44/classes
cp -a $L/.ufo/waves/round-44/controls-r43   $R/.ufo/waves/round-44/controls-r43
cp -a $L/.ufo/waves/round-44/c44_probe.py $L/.ufo/waves/round-44/c44_count_v5.py \
      $L/.ufo/waves/round-44/c44_placebo.py $R/.ufo/waves/round-44/
```

## The mutation

Applied to the scratch copy's `classes/g6_fold_pairs.py` only:

```python
"""MUTANT (scratch copy only): G6 delegates to the counter's run-F generator cases_f,
so the run carries none of G6's own fold-pair shapes. Same unit kinds as cases_f
(value/foldpair/prefixpair/pairfile), so layout_f still applies."""


def cases(rng, h):
    return h.cases_f(rng)
```

The mutant is faithful to the real class-run path: the counter calls
`classes[key].cases(rng, sys.modules[__name__])` and then `layout_f(rng, units, cd)`
(`c44_count_v5.py:1063-1065`), and `c44_probe.py` does the same. Verified that the mutant's
unit stream is exactly the counter's run-F stream:

```
mutant G6 units == counter run-F units for seeds 1..20: True
```

## DECISIVE OUTPUT

### 1. The named attack: mutant G6, per-seed probe exit codes, seeds 1..20

```sh
cd /fast/scratch/hyaku/kake-r44/MutG6Placebo/repo
for c in casememo-v3-validity-lower casememo-v4-validity-lower-short \
         casememo-v7-value-lower-nonascii casememo-v8-value-casefold-nonascii; do
  line=""; for s in $(seq 1 20); do
    python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 \
      --tool-file .ufo/waves/round-44/controls-r43/$c.py --seed $s >/dev/null 2>&1
    line="$line $?"; done
  echo "$c exit-by-seed(1..20):$line"; done
```

```
casememo-v3-validity-lower exit-by-seed(1..20): 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
casememo-v4-validity-lower-short exit-by-seed(1..20): 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
casememo-v7-value-lower-nonascii exit-by-seed(1..20): 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
casememo-v8-value-casefold-nonascii exit-by-seed(1..20): 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**No seed exits 1. There is no lucky seed to name.** The G6 seat's witnesses need no luck check
over these seeds.

Extended sweep, seeds 1..200, all four controls (800 rows):

```
$ python3 -B sweep.py repo mutant 200
SWEEP mutant: seeds=1..200 controls=4 rows=800  witnessExit1=0  probeErrorExit2=0  cleanExit0=800
```

### 2. Detector power: the same detector fires when the class carries G6's real shapes

A witness-capable G6 class (scratch `repo2`, built from the frozen control sources and the
independent derivation in `w2/ReviewG6Semantics.md`) makes the *same* detector report
witnesses on all four controls, seeds 1..20:

```
SUMMARY positive: rows=80 witnessExit1=80 probeErrorExit2=0 cleanExit0=0
  ('casememo-v3', 1) -> 20 rows
  ('casememo-v4', 1) -> 20 rows
  ('casememo-v7', 1) -> 20 rows
  ('casememo-v8', 1) -> 20 rows
```

Single control, single seed, verbatim probe JSON:

```
casememo-v3-validity-lower exit=1 equal= False units= 40
casememo-v4-validity-lower-short exit=1 equal= False units= 40
casememo-v7-value-lower-nonascii exit=1 equal= False units= 40
casememo-v8-value-casefold-nonascii exit=1 equal= False units= 40
```

So the mutant's 80/80 zeros are the mutant's property, not a broken harness.

### 3. Pristine (unmutated) lane G6 — the pre-fix baseline

```
SUMMARY pristine: rows=80 witnessExit1=0 probeErrorExit2=0 cleanExit0=80
```

The lane's G6 at `f4f13a76…` (unchanged during this seat's whole run; a 10-minute poll on the
file hash found no landing) witnesses 0/4 — consistent with `claim/after-v5.txt`
(`casememo-v3 G6 met=True caught=-`) and with `w1/ExecG6Fold.md`. The mutant and the pristine
baseline are **indistinguishable** on this detector, which is itself the point: the shared
run-F corpus carries no casememo witness at all.

### 4. Why the mutant cannot witness — structural, not statistical

The four controls differ from the round-41 reference only through a case-folded memo:

| control | memo key | when consulted |
|---|---|---|
| v3 `casememo-v3-validity-lower` | `value.lower()` | every value |
| v4 `casememo-v4-validity-lower-short` | `value.lower()` | only values ≤ 64 code points |
| v7 `casememo-v7-value-lower-nonascii` | `value.lower()` | only values carrying a non-ASCII character |
| v8 `casememo-v8-value-casefold-nonascii` | `value.casefold()` | only values carrying a non-ASCII character |

A witness needs a value whose memoized answer differs from its as-written scan answer.
`cases_f` builds its corpus exclusively from the counter's ASCII tables — `FILL`, `LOWER`,
`ALNUM`, `HEX`, `UNRESERVED`, `SUB_DELIMS`, `TLDS`, `COMMON_HOSTS`, all verified ASCII-only —
so the mutant's corpus carries **no non-ASCII value at all**:

```
$ python3 -B ...  # cases_f over seeds 1..500
cases_f over seeds 1..500: units=610000 string values=1300000  NON-ASCII values=0

cases_f source mentions NON_ASCII: False
cases_f source mentions U+212A / \u212a: False
cases_f source mentions casefold: False
```

Consequences, each confirmed against the frozen control modules:

- **v7 / v8**: their memos are consulted *only* for non-ASCII values. With an all-ASCII corpus
  the memo is never consulted for the deciding value, so the memoized answer equals the
  as-written answer and the control agrees with ref41. Confirmed on a run-F fold pair (which
  *does* put the case difference in the first path segment, so ref41 flags member b
  `loc_out_of_scope`):

  ```
  member b IS out of scope for ref41 (first segment case differs from smu).
  v7 memo gate is non-ASCII-only; both members ASCII:
    v7._parse_url(b)      = ('https', 'qg6yq.com', 443, '/jqbjllyhp/j7izhy')
    v7._parse_url_scan(b) = ('https', 'qg6yq.com', 443, '/jqbjllyhp/j7izhy')
    -> identical tuple, memo MISS => v7 reports the SAME out_of_scope as ref41. No divergence.
  ```

- **v3 / v4**: their memo keys on `value.lower()`, and run-F's `fold_pair` members *do* collide
  under `lower()` (`a.lower() == b.lower()` is `True`) — but both members are valid ASCII URLs,
  so the cached verdict equals the fresh verdict and the memo hit is harmless:

  ```
  a.lower()==b.lower(): True
  v3 scan a: True scan b: True -> identical verdict, memo hit harmless
  v4 scan a: True scan b: True
  ```

A faithful replay of each control's own memoized entry point against each control's own
as-written scan, over the laid-out value stream, confirms the counts and confirms the
simulation is sensitive (it fires on the witness-capable class):

```
=== A) POSITIVE CONTROL (witness-capable G6) ===
class=g6_fold_pairs.py seeds 1..10 : values=800  non-ASCII=400
  v3 memo-divergence hits: 2 [('http://[::1%25K]/seg/tail')]
  v4 memo-divergence hits: 1 [('http://[::1%25K]/seg/tail')]
  v7 memo-divergence hits: 3 [('http://[::1%25K]/seg/tail')]
  v8 memo-divergence hits: 4 [('http://[::1%25K]/seg/tail')]

=== B) MUTANT (cases_f delegator) ===
class=mut_class.py seeds 1..10 : values=16600  non-ASCII=0
  v3 memo-divergence hits: 0
  v4 memo-divergence hits: 0
  v7 memo-divergence hits: 0
  v8 memo-divergence hits: 0

=== C) PRISTINE lane G6 (pre-fix) ===
class=g6_fold_pairs.py seeds 1..10 : values=2000  non-ASCII=1000
  v3 memo-divergence hits: 0
  v4 memo-divergence hits: 0
  v7 memo-divergence hits: 4 [('hTtp://5usx.test/jqmv1h/Kayflcx38yc1')]
  v8 memo-divergence hits: 5 [('hTtp://5usx.test/jqmv1h/Kayflcx38yc1')]
```

Read this carefully — it is the substantive finding for the G6 seat:

- **B (mutant)**: zero memo divergence on every control. The mutant is *structurally incapable*
  of witnessing, at any seed. The zero is not a sampling accident.
- **A (witness-capable)**: the simulation fires on all four controls. Sensitive.
- **C (pristine lane G6)**: v3/v4 fire **zero** times even though the corpus is half non-ASCII.
  The pre-fix G6 puts its markers in the **second** path segment, where the grammar admits
  non-ASCII, so the fold collision is benign; and its v7/v8 divergence at the URL level does not
  reach a *finding* because the scope prefix is unaffected. This independently reproduces
  `w2/ReviewG6Semantics.md`'s diagnosis from a different direction and confirms the wave-1
  `ExecG6Fold.md` failure is a shape error, not a harness error.

## Implication for the G6 seat (falsification deliverable)

When the fixed G6 lands and witnesses the four casememo controls, that witnessing **cannot** be
attributed to the shared corpus, to the harness, or to seed luck:

1. The placebo G6 (the shipped `classes-placebo` behaviour) witnesses **0/4** on seeds 1..20 and
   0/800 rows on seeds 1..200 — so no seed is "lucky" for the placebo.
2. A class carrying G6's real shapes witnesses **4/4** on seeds 1..20 — so the detector is live.
3. The mutant's inability is structural (zero non-ASCII values ⇒ v7/v8's memos are never
   consulted; v3/v4's collisions are verdict-neutral), not statistical.

The G6 seat therefore need not check its witnesses for luck over seeds 1..20 (or 1..200) against
the placebo: the placebo witnesses nothing there. The witnesses that matter are the ones G6's
own fold-pair shapes produce.

**Coverage finding (not a contract change):** the memo divergence for v3/v4 requires a
non-ASCII code point in a position the round-41 grammar *rejects* — the IP-literal zone id
`[ ]` is the only such slot (`_TABLE_IP_LITERAL` is built `non_ascii=False`). A first-segment
case swap alone cannot witness v3/v4; only v7/v8. This is a shape constraint on G6, recorded
here as information for the fix seat, not a change to any contract.

## Files written

Lane repo (one file, this report):
- `.ufo/waves/round-44/w2/MutG6Placebo.md`

Scratch only (`/fast/scratch/hyaku/kake-r44/MutG6Placebo/`), never in the lane:
- `repo/` — clone with `classes/`, `controls-r43/`, `c44_probe.py`, `c44_count_v5.py`, `c44_placebo.py` (class dir mutated and restored)
- `repo2/` — second clone carrying the witness-capable positive-control `classes/g6_fold_pairs.py`
- `classes-pristine/` — copy of the lane `classes/` dir as found
- `g6_pristine_snapshot.py` — pristine lane G6 bytes (`f4f13a76…`)
- `g6_positive_control.py`, `g6_positive_control2.py` — positive-control class modules
- `matrix.py`, `sweep.py` — the bounded detector drivers
- `memo_sim.py`, `memo_sim_class.py`, `memo_faithful.py` — memo-precondition simulations
- `ref41_tool.py` — `git show 1ef7a0e9…:scripts/sitemap_audit.py` (the pinned reference)
- `matrix-pristine.json`, `matrix-mutant.json`, `matrix-positive.json`, `sweep-mutant.json` — row records

The lane repo was **not** written by this seat except for this report:
`git status --porcelain` in the lane shows only `LOG.md`, `SCORECARD.md`, `corpus/SOURCES.md`
and untracked round-44 artefacts, all pre-existing or owned by other seats; `classes/g6_fold_pairs.py`
still hashes `f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d`, the value it
had when this seat started.

## Restoration evidence

```
$ cp /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/classes/g6_fold_pairs.py \
     repo/.ufo/waves/round-44/classes/g6_fold_pairs.py
$ sha256sum repo/.ufo/waves/round-44/classes/g6_fold_pairs.py \
            /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/classes/g6_fold_pairs.py \
            g6_pristine_snapshot.py
f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d  repo/.ufo/waves/round-44/classes/g6_fold_pairs.py
f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/classes/g6_fold_pairs.py
f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d  g6_pristine_snapshot.py
RESTORED: bytes identical to start
```

## Blockers / dead ends

- **No tool installs.** None needed; `python3`, `git` and `/usr/bin/bwrap` (0.13.1) were present.
- The lane's `classes/g6_fold_pairs.py` was **not** rewritten by this seat (the fix seat
  `ExecG6FoldFix` owns that file). A 10-minute hash poll on the lane file found no landing
  during this seat's run; the pre-fix bytes `f4f13a76…` were therefore the baseline throughout.
  The mutant and the positive control were both built in scratch, so this seat never blocked or
  raced the fix seat.
- Dead end recorded: my first positive control used a literal ASCII `K` inside the brackets
  instead of U+212A and produced no witness (probe exit 0) — the zone-id rejection needs the
  real U+212A. Fixed; the corrected control fires on all four controls.
- Dead end recorded: a first memo-precondition simulation modelled v7/v8 as
  consult-and-store-only-if-non-ASCII, missing that the controls' ASCII path *stores* into the
  memo. Replaced by `memo_faithful.py`, which calls each control's own memoized entry point
  (`_uri_ok` / `_parse_url`) and compares against its own as-written scan; that version is
  sensitive on the positive control and reports zero for the mutant.
- Unrun check: the full `c44_audit.py --classes v5` claim run was **not** executed by this seat
  (out of scope for a single mutation probe, and the fix seat's file is in flight). The claim's
  own receipts were read only.

Report: .ufo/waves/round-44/w2/MutG6Placebo.md
