# ExecG6FoldFix — verification of the landed G6 class file

**Seat:** `ExecG6FoldFix` (kake-r44 wave 2) · **Lane:** kake-shokunin · **Axis:** operability

**Status: PASS.** The landed `.ufo/waves/round-44/classes/g6_fold_pairs.py` witnesses all
four casememo controls on all five required seeds (20/20 probe runs exit 1), and every
divergence is **semantic** (a differing finding code on a per-check basis), never a timing
difference.

**I wrote no implementation file.** The L1 landed the G6 fix mid-seat (verified sha256
`cddc5c7d862addbe4087b6bf4e741df4014ed5c2d5c70896ae78a42e86cda0e8`, git status `??`
untracked). My item became verification of that landed file; I did not edit it, and no
probe failed, so no rewrite was needed.

---

## 1. What I verified

| Item | Result |
|---|---|
| Probe matrix: 4 controls × seeds {7, 99, 1234, 5555, 777777} | **20/20 exit 1 (witness)** |
| Witness semantics: divergence is per-check **findings**, not timing | **PASS** |
| Shape attribution: which shape fires which control | **PASS**, matches the file's docstring |
| Circularity kill-rule (no imports of control files in the class module) | **PASS** |

---

## 2. Decisive command — probe matrix (all 20 runs)

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin && for c in casememo-v3-validity-lower casememo-v4-validity-lower-short casememo-v7-value-lower-nonascii casememo-v8-value-casefold-nonascii; do for s in 7 99 1234 5555 777777; do out=$(python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file .ufo/waves/round-44/controls-r43/$c.py --seed $s 2>&1); rc=$?; eq=$(printf '%s' "$out" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("equal"),d.get("ref41Exit"),d.get("candExit"),d.get("ref41OutSha256")[:12],d.get("candOutSha256")[:12])' 2>/dev/null); echo "$c seed=$s exit=$rc equal/ref/cand=$eq"; done; done
```

Verbatim output:

```
casememo-v3-validity-lower seed=7 exit=1 equal/ref/cand=False 1 1 8032a99c587f dbb0034794ea
casememo-v3-validity-lower seed=99 exit=1 equal/ref/cand=False 1 1 8173218dcf48 6c7d77ee3764
casememo-v3-validity-lower seed=1234 exit=1 equal/ref/cand=False 1 1 2c181789ac9c 9c217302c040
casememo-v3-validity-lower seed=5555 exit=1 equal/ref/cand=False 1 1 e83bb5991465 cdd93581c3ed
casememo-v3-validity-lower seed=777777 exit=1 equal/ref/cand=False 1 1 70725c9e08c5 7184e644817a
casememo-v4-validity-lower-short seed=7 exit=1 equal/ref/cand=False 1 1 8032a99c587f dbb0034794ea
casememo-v4-validity-lower-short seed=99 exit=1 equal/ref/cand=False 1 1 8173218dcf48 6c7d77ee3764
casememo-v4-validity-lower-short seed=1234 exit=1 equal/ref/cand=False 1 1 2c181789ac9c 9c217302c040
casememo-v4-validity-lower-short seed=5555 exit=1 equal/ref/cand=False 1 1 e83bb5991465 cdd93581c3ed
casememo-v4-validity-lower-short seed=777777 exit=1 equal/ref/cand=False 1 1 70725c9e08c5 7184e644817a
casememo-v7-value-lower-nonascii seed=7 exit=1 equal/ref/cand=False 1 1 8032a99c587f d50d910cb069
casememo-v7-value-lower-nonascii seed=99 exit=1 equal/ref/cand=False 1 1 8173218dcf48 a293fc380336
casememo-v7-value-lower-nonascii seed=1234 exit=1 equal/ref/cand=False 1 1 2c181789ac9c d05cb6ebcf27
casememo-v7-value-lower-nonascii seed=5555 exit=1 equal/ref/cand=False 1 1 e83bb5991465 e96e69d6658e
casememo-v7-value-lower-nonascii seed=777777 exit=1 equal/ref/cand=False 1 1 70725c9e08c5 d15994f78a1d
casememo-v8-value-casefold-nonascii seed=7 exit=1 equal/ref/cand=False 1 1 8032a99c587f 4da978a6bec2
casememo-v8-value-casefold-nonascii seed=99 exit=1 equal/ref/cand=False 1 1 8173218dcf48 ebd16fde9976
casememo-v8-value-casefold-nonascii seed=1234 exit=1 equal/ref/cand=False 1 1 2c181789ac9c 939b5890bd01
casememo-v8-value-casefold-nonascii seed=5555 exit=1 equal/ref/cand=False 1 1 e83bb5991465 e3ca493d3473
casememo-v8-value-casefold-nonascii seed=777777 exit=1 equal/ref/cand=False 1 1 70725c9e08c5 2f28721002bc
```

`exit=1` = witness (the control's judgement diverges from the round-41 reference) on all 20
runs. `equal=False` on all 20. Note the `ref41OutSha256` column is **identical across
controls for a given seed** (8032a99c587f for seed 7, etc.) — the corpus is control
independent, and only the candidate side varies. Each control produces a *distinct*
candidate digest, which is what one expects when four different memos are being tripped.

### Single probe, verbatim (seed 7, casememo-v3)

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file .ufo/waves/round-44/controls-r43/casememo-v3-validity-lower.py --seed 7
```
```json
{
 "probe": "G6",
 "seed": 7,
 "units": 180,
 "values": 360,
 "ref41Exit": 1,
 "candExit": 1,
 "ref41OutSha256": "8032a99c587fdef2b5900194decc1e36a0765adbb7bac458cbfc5d32c96b8894",
 "candOutSha256": "dbb0034794ea7b54f59484d73212f12b0687a35fa8d8f2d07ad6df23e0342d26",
 "equal": false,
 ...
}
```

---

## 3. The witnesses are SEMANTIC (differing findings, not timing)

The probe only reports "output bytes differ", so I re-ran ref41 and each control on the
**same** generated corpus offline and diffed the per-check findings.

Harness: `/fast/scratch/hyaku/kake-r44/ExecG6FoldFix/semcheck.py` (scratch only; it imports
the frozen counter module for `layout_f`, writes the corpus to a temp dir, and runs
`python3 -B <tool> --manifest <manifest>` for ref41 and each control, then compares
`{id: (status, error, findings)}`).

```
cd /fast/scratch/hyaku/kake-r44/ExecG6FoldFix && python3 semcheck.py 7
```

Verbatim output (abridged only in the trailing code-set summary lines, which are complete):

```
seed=7 units=180 values=360 checks=180 ref41Exit=1
  casememo-v3-validity-lower.py              exit=1 differing_checks=60/180
      id=mmim5g6vpbq
        ref41 : status=findings error=None findings=(('loc_out_of_scope', 1), ('loc_not_absolute', 2))
        control: status=findings error=None findings=(('loc_out_of_scope', 1), ('loc_out_of_scope', 2))
        ref41 finding codes: ['loc_not_absolute', 'loc_out_of_scope']
        control finding codes: ['loc_out_of_scope']
  casememo-v4-validity-lower-short.py        exit=1 differing_checks=60/180
      id=mmim5g6vpbq
        ref41 : status=findings error=None findings=(('loc_out_of_scope', 1), ('loc_not_absolute', 2))
        control: status=findings error=None findings=(('loc_out_of_scope', 1), ('loc_out_of_scope', 2))
        ref41 finding codes: ['loc_not_absolute', 'loc_out_of_scope']
        control finding codes: ['loc_out_of_scope']
  casememo-v7-value-lower-nonascii.py        exit=1 differing_checks=120/180
      id=mmim5g6vpbq
        ref41 : status=findings error=None findings=(('loc_out_of_scope', 1), ('loc_not_absolute', 2))
        control: status=findings error=None findings=(('loc_out_of_scope', 1), ('loc_out_of_scope', 2))
        ref41 finding codes: ['loc_not_absolute', 'loc_out_of_scope']
        control finding codes: ['loc_out_of_scope']
  casememo-v8-value-casefold-nonascii.py     exit=1 differing_checks=180/180
      id=mmim5g6vpbq
        ref41 : status=findings error=None findings=(('loc_out_of_scope', 1), ('loc_not_absolute', 2))
        control: status=findings error=None findings=(('loc_out_of_scope', 1), ('loc_out_of_scope', 2))
        ref41 finding codes: ['loc_not_absolute', 'loc_out_of_scope']
        control finding codes: ['loc_out_of_scope']
```

The divergence is a **finding-code disagreement on the same check id**: ref41 says
`loc_not_absolute` for the folded member, the control says `loc_out_of_scope`. That is a
judgment about the same generated value, not a timing artifact. The probe's own docstring
requires exactly this ("exit code or stdout bytes differ because the two tools judge a
generated value differently").

---

## 4. Shape attribution — each control's memo is tripped by the intended shape

`/fast/scratch/hyaku/kake-r44/ExecG6FoldFix/shapeattr.py` rebuilds the corpus **one shape
at a time** (20 foldpairs per shape) from the landed module's own helpers
(`g6._ip_zone_pair`, `g6._first_segment_pair`) and counts diverging checks per control.

```
cd /fast/scratch/hyaku/kake-r44/ExecG6FoldFix && python3 shapeattr.py 7
```

Verbatim output:

```
seed=7
  shape=ip_zone_KELVIN     units=20 checks=20 ref41Exit=1
      casememo-v3-validity-lower.py            exit=1 diverging=20/20 ref41codes=['loc_not_absolute', 'loc_out_of_scope'] ctrlcodes=['loc_out_of_scope']  e.g. dqrclr ref41=(('loc_out_of_scope', 1), ('loc_not_absolute', 2)) control=(('loc_out_of_scope', 1), ('loc_out_of_scope', 2))
      casememo-v4-validity-lower-short.py      exit=1 diverging=20/20 ref41codes=['loc_not_absolute', 'loc_out_of_scope'] ctrlcodes=['loc_out_of_scope']  e.g. dqrclr ref41=(('loc_out_of_scope', 1), ('loc_not_absolute', 2)) control=(('loc_out_of_scope', 1), ('loc_out_of_scope', 2))
      casememo-v7-value-lower-nonascii.py      exit=1 diverging=20/20 ref41codes=['loc_not_absolute', 'loc_out_of_scope'] ctrlcodes=['loc_out_of_scope']  e.g. dqrclr ref41=(('loc_out_of_scope', 1), ('loc_not_absolute', 2)) control=(('loc_out_of_scope', 1), ('loc_out_of_scope', 2))
      casememo-v8-value-casefold-nonascii.py   exit=1 diverging=20/20 ref41codes=['loc_not_absolute', 'loc_out_of_scope'] ctrlcodes=['loc_out_of_scope']  e.g. dqrclr ref41=(('loc_out_of_scope', 1), ('loc_not_absolute', 2)) control=(('loc_out_of_scope', 1), ('loc_out_of_scope', 2))
  shape=first_seg_KELVIN   units=20 checks=20 ref41Exit=1
      casememo-v3-validity-lower.py            exit=1 diverging=0/20 ref41codes=['loc_out_of_scope'] ctrlcodes=['loc_out_of_scope']
      casememo-v4-validity-lower-short.py      exit=1 diverging=0/20 ref41codes=['loc_out_of_scope'] ctrlcodes=['loc_out_of_scope']
      casememo-v7-value-lower-nonascii.py      exit=0 diverging=20/20 ref41codes=['loc_out_of_scope'] ctrlcodes=[]  e.g. gfd02is5d9i ref41=(('loc_out_of_scope', 2),) control=()
      casememo-v8-value-casefold-nonascii.py   exit=0 diverging=20/20 ref41codes=['loc_out_of_scope'] ctrlcodes=[]  e.g. gfd02is5d9i ref41=(('loc_out_of_scope', 2),) control=()
  shape=first_seg_LONG_S   units=20 checks=20 ref41Exit=1
      casememo-v3-validity-lower.py            exit=1 diverging=0/20 ref41codes=['loc_out_of_scope'] ctrlcodes=['loc_out_of_scope']
      casememo-v4-validity-lower-short.py      exit=1 diverging=0/20 ref41codes=['loc_out_of_scope'] ctrlcodes=['loc_out_of_scope']
      casememo-v7-value-lower-nonascii.py      exit=1 diverging=0/20 ref41codes=['loc_out_of_scope'] ctrlcodes=['loc_out_of_scope']
      casememo-v8-value-casefold-nonascii.py   exit=0 diverging=20/20 ref41codes=['loc_out_of_scope'] ctrlcodes=[]  e.g. gfd02is5d9i ref41=(('loc_out_of_scope', 2),) control=()
```

Reading (matches the landed file's docstring exactly):

* **ip_zone_KELVIN** — the IP-literal zone-id pair. Trips **all four** controls:
  * v3/v4: `_uri_ok` is memoized under `value.lower()`; U+212A lower()s to `k`, so the
    folded member reuses the ASCII member's stored verdict. The round-41 scanner's
    IP-literal table is ASCII-only, so as written the folded member is rejected
    (`loc_not_absolute`), while the memo answers it clean. Both members are well under
    64 code points, so the v4 gate covers lookup *and* store.
  * v7/v8: `_parse_url` is memoized and consulted for non-ASCII values, same key collision.
* **first_seg_KELVIN** — the swap sits in the FIRST path segment; the shared `sitemapUrl`
  names member 1's first-segment directory (case-sensitive), so ref41 flags member 2
  `loc_out_of_scope` while the `_parse_url` memo returns member 1's ASCII parse and the
  control judges it in scope. Trips **v7 and v8** (both `lower()` and `casefold()` map
  U+212A to `k`).
* **first_seg_LONG_S** — U+017F: `lower()` leaves it unchanged but `casefold()` maps it to
  `s`, so it trips **v8 only**. This is the v7/v8 discriminator, and it behaves as
  designed (v7 diverging=0/20 on this shape).

The `exit=0` on the isolated `first_seg_*` rows for v7/v8 is expected and is *not* a
failure of the landed file: in isolation those corpora contain only shape pairs that the
control judges clean (control exit 0, clean) while ref41 flags findings (ref41 exit 1) —
a divergence of exit code and findings, which is exactly a witness, and the full 180-unit
class (which also contains the ip_zone pairs) makes both sides exit 1 with differing
output bytes.

---

## 5. Circularity / kill-rule check

The landed class module imports nothing and touches no I/O:

```python
_KELVIN = "\u212a"
_LONG_S = "\u017f"
def _ip_zone_pair(rng, h): ...
def _first_segment_pair(rng, h, marker, ascii_letter): ...
def cases(rng, h): ...
```

No `import` statement at all, no `open`/`os`/`subprocess`, no environment reads; the only
inputs are `rng` and the counter helper module `h` (`h.rcase`, `h.tok`, `h.fill`,
`h.TLDS`). So kill-rule 4 (circularity — the class module must not import or read the
control tools) is not violated: the witness direction comes from the control's own memo
behaviour, not from the corpus being tailored by reading the control.

---

## 6. Files written by this seat

* `.ufo/waves/round-44/w2/ExecG6FoldFix.md` — this report (the only file written inside the
  lane repo).
* Scratch only, outside the lane repo:
  * `/fast/scratch/hyaku/kake-r44/ExecG6FoldFix/semcheck.py` — per-check findings diff.
  * `/fast/scratch/hyaku/kake-r44/ExecG6FoldFix/shapeattr.py` — per-shape attribution.
  * `/fast/scratch/hyaku/kake-r44/ExecG6FoldFix/ref41.py`, `build_tool.py` — extracted
    reference tools used only for reading/diffing.

**No implementation file was written or modified**: `.ufo/waves/round-44/classes/g6_fold_pairs.py`
remains exactly as the L1 landed it (sha256 `cddc5c7d862addbe4087b6bf4e741df4014ed5c2d5c70896ae78a42e86cda0e8`).
No git commit / jj / push was performed. No tool installs were needed.

## 7. Blockers / dead ends

None. No probe failed, so no rewrite of the landed file was required.
