# RevengerControls — round-44 wave-1 (r44-build, operability)

Reverse-engineered three round-43 controls from their committed bytes, reconstructed each
author's blind-spot claim, and judged the planned G-class shape against the shape that
actually defeats the control. sha256 of each file equals `controls-27.tsv` (no drift):
`headtail-V2…` `012527ff…c10bf`, `portvalue-memo-digits.py` `d09ad5fe…b00d`,
`repeat-ctl_defpos_memo_band.py` `b9c7eda6…55c0e`. All three are the same round-42 byte
scanner (`_uri_ok`/`_scan` grammar identical) with one injected cache; the diff per control
is the injected block only. ref41 tool re-extracted
(`git show 1ef7a0e9…:scripts/sitemap_audit.py`, sha256 `50287ac6…dde7d` matches the
counter's pin). Evidence harness + fixtures under
`/fast/scratch/hyaku/kake-r44/RevengerControls/` (`diffcheck.py`, `ref41.py`, `caseA/`,
`caseB/`). No tools installed; no lane files written but this report.

---

## 1. `headtail-V2-headtail-key48.py` → class G5 — verdict: **class covers it**

**Injected block** (lines 287-306): process-global `_HEADTAIL_CACHE` consulted in
`_parse_url`; `_parse_url_scan` holds the honest path (grammar + urlsplit + port default).

**Cache key** (lines 296-299):
```
key = value[:48] + "\x00" + value[-48:]   if len(value) > 96
key = value                              otherwise
```
Code points, not bytes; **length is not part of the key** — two values of different
lengths collide when their first 48 and last 48 code points match.

**Author's blind-spot claim** (the control's own comment, lines 287-290):
> "a process-global parse cache keyed on a HEAD+TAIL window (first 48 and last 48 code
> points). The middle of every later value that shares that window with an earlier value
> is never judged."
The seat report (`round-43/w1/CtlHeadTail.md`) adds the corpus claim: counter v4's
"keyed-window detection boundary is exactly 44 code points" — `cut = rng.randint(36, 44)`
in `c43_count_v4.py:450` — and no generated pair ever shared both a 48-cp head and a 48-cp
tail. Reconstruction agrees: the only shared-prefix generator capped at 44, and no
generator emitted same-head+same-tail pairs, so the window could never collide.

**Defeating shape** (named): two values **> 96 code points with identical first-48 and
last-48 code points, differing only inside the middle** — one carrying a grammar defect
there (`v2 = head + "b"*15 + " " + "b"*14 + tail` vs clean `v1 = head + "b"*30 + tail`).
Observed (`diffcheck.py`): equal keys, `v2` honest scan `None`, cached `_parse_url(v2)`
returns `v1`'s tuple.

**Class G5** (`classes/g5_prefix_cut_45plus.py`, present): its second unit kind is exactly
this shape — 40 head+tail-48 `prefixpair`s (`head` 48 cp, defect inside `mid`, shared
47+1-cp tail), order randomized; cut-pairs with `cut` in 64/65/80 and short tails also
collide on the window. Probe vs this control, run twice:

`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file .ufo/waves/round-44/controls-r43/headtail-V2-headtail-key48.py --seed 101` → exit 1,
`"equal": false`, ref41 tail `loc_not_absolute entry 2` vs cand tail `clean` (out sha
`b17870cb…` vs `cd747e64…`); seed 202 → exit 1, same direction (`19b68061…` vs
`f0aedb01…`). **headtail-V2 will not meet v5 once G5 runs.**

Disagreements: none — the comment states the skip precisely; the seat's 44-cp boundary
claim is about v4 and held.

## 2. `portvalue-memo-digits.py` → class G9 — verdict: **class misses it** (planned shape a cannot witness; pairfile shape required)

**Injected block** (lines 287, 290-301, 323-331): process-global `_PORT_MEMO` keyed on the
**port digit string alone** — `_port_digits(netloc)` strips userinfo (`rpartition("@")`)
and IP-literal brackets, then takes the text after the last `:` of the hostinfo. Consulted
only when `digits is not None` and only stores **successful** parses (the grammar/urlsplit
gate runs first, so the cache substitutes one valid parse for another — host, path, scheme,
port — never a `None`).

**Author's blind-spot claim** (comment, line 287):
> "CONTROL: parse results memoised on the port digits only"
plus seat report `CtlPortValue.md`: "the counter cannot see the port-digits-keyed parse
cache … no generator hands two different hosts one port string inside a manifest where the
answer would flip", and the measured subtlety: a wrong-host cache hit "still leaves
`parsed[:3] != sitemap_url[:3]`, so `loc_out_of_scope` is emitted by both tools" — the
counter "compares findings bytes, not parses".

**Defeating shape** (named, and it is narrower than "same port, different hosts"): two
locs **in one urlset under one check** (`pairfile`/same-file vehicle), same explicit
in-range port digits, **member 2's host ≠ member 1's host** with member 1 anchoring the
`segment_smu` sitemapUrl. The cached parse makes member 2 in-scope under the control while
ref41 flags it. Observed end-to-end (fixtures `caseB/`, run in their dirs):

```
ref41:   {"verdict": "failed-policy", … "loc_out_of_scope", "entry": 2}   exit=1
control: {"verdict": "clean", … "findings": []}                           exit=0
```

**Critical correction to the planned G9 shape (a)** — the spec's two-separate-`value`-unit
shape (`https://a…:8443/x` then `https://b…:8443/y`, different hosts) **produces no
divergence**: `_parse_url` memoises `sitemapUrl` parses too, and `derived_smu(v)` copies
v's port digits verbatim, so check 2's sitemapUrl hits the *same* poisoned slot and the
[:3] comparison stays self-consistent. Observed (`caseA/`, both tools exit 0, both
`clean`). The author's own claim is misread if applied cross-check: a port-digits cache
hit can **never** flip the host comparison inside one check when the sitemapUrl carries
the same digits — it only flips when the sitemapUrl is anchored on a *different* value
(member 1 of the same file). G9 must express shape (a) as a `pairfile` (member 1
`http://H1:PORT/d/x`, member 2 `http://H2:PORT/d/y`); as planned it misses.
(`portvalue-memo-digits-67` identical modulo the 6-7-digit gate; `prefixpair` also works
only if hosts differ within the shared 36-44-cp head — pairfile is the clean vehicle.)

## 3. `repeat-ctl_defpos_memo_band.py` → class G7 — verdict: **class covers it**

**Injected block** (lines 212-234): process-global `_DEFPOS_MEMO` wrapped around
`_uri_ok`; honest scan renamed `_uri_ok_slow`.
```
guard:  value.find('%') >= 1000 and len(value) <= 1799
key:    (len(value), value.find('%'))
```
Only the **grammar verdict** is memoised — a cache hit makes a defective value pass
`_uri_ok` and reach urlsplit, which accepts the defect (e.g. space or `%4G` inside the
path is fine for urlsplit), so the finding flips from `loc_not_absolute` to a scope
verdict.

**Author's blind-spot claim** (comment, lines 213-217):
> "defect-position memo for a first '%' at index >= 1000 and <= 1799 code points
> … The key does not determine the verdict, so a later value with that key can be judged
> differently from the round-41 tool."
Seat report `CtlRepeat.md` gives the corpus claim: the band is "corpus-absent" —
`active=0` on replay — because every generated short value is far under 1000 cp while
`long_tail_value`/`shape_t2` emit 2000-2047 cp, above the 1799 ceiling. Reconstruction
agrees with the mechanism.

**Disagreement inside the comment itself**: it says "a first '%' at index >= 1000 **and <=
1799**" — the 1799 bound is on `len(value)`, not on the '%' index. A 2000-cp value whose
first '%' sits at 1200 is *not* memoised (length gate), though the comment's phrasing
implies it is. The blind spot is the two-dimensional band `first-'%' ≥ 1000 ∧ len ≤ 1799`.

**Defeating shape** (named): two values, **same length L ≤ 1799, first '%' at the same
index i ≥ 1000**, different URI-grammar verdicts — clean member first
(`…c*1079 + "%41" + d*97`, L=1200, i=1100) then defective member (`…"%4G"…`, same L, same
i). Observed (`diffcheck.py`): `_uri_ok(u1)=True` cached; `_uri_ok_slow(u2)=False`;
`_uri_ok(u2)=True` via memo. Order matters only for the direction of the lie — bad-first
also diverges (clean member inherits `False`), so clean-first is the tidy witness.

**Class G7** (spec `g7_band_memos.py`, file not yet present): planned shape is exactly
this — "pairs of `value` units in FIRST-SEEN order — the clean member first, then a member
with the SAME key … (same (length, percent index)) carrying one grammar defect". `value`/
`loc` units are the right vehicle: the memo lives on `_uri_ok`, hit by both locs and
sitemapUrls, so cross-check first-seen ordering flips the second check's grammar verdict.
**repeat-ctl_defpos_memo_band will not meet v5 once G7 lands.**

---

## Verdict table

| control | class | verdict | defeating shape (named) |
|---|---|---|---|
| headtail-V2-headtail-key48 | G5 | **class covers it** (probe exit 1, seeds 101+202) | >96-cp pair, identical first-48 + last-48 cp, defect mid-value |
| portvalue-memo-digits | G9 | **class misses it** as planned — shape (a) cross-check is self-consistent (observed: both clean); pairfile same-check pair required | two locs, one urlset, same port digits, host₂≠host₁, sitemapUrl anchored on member 1 |
| repeat-ctl_defpos_memo_band | G7 | **class covers it** (spec shape == defeating shape) | two values, same len ≤ 1799, same first-'%' index ≥ 1000, clean-then-defective |

## Commands run (verbatim, decisive output trimmed)

- `sha256sum` of the three controls — all equal the TSV pins (above).
- `python3 -B /fast/scratch/hyaku/kake-r44/RevengerControls/diffcheck.py` — output quoted
  per control above (cache collision wrong-parses on all three).
- `python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file
  .ufo/waves/round-44/controls-r43/headtail-V2-headtail-key48.py --seed 101` →
  `"equal": false`, exit 1 (`loc_not_absolute` vs `clean`); `--seed 202` → same, exit 1.
- ref41 + control on hand fixtures `/fast/scratch/hyaku/kake-r44/RevengerControls/caseA`
  (two checks, same port digits, different hosts): **both exit 0, both clean — no
  divergence**; `caseB` (one check, two locs): ref41 exit 1 `loc_out_of_scope entry 2` vs
  control exit 0 `clean`.

## Hand-off note for ExecG9PortDigits

Shape (a) as specified (two `value` units) was tested and cannot witness: the second
check's `sitemapUrl` poisons/hits the same port-digits slot, keeping `parsed[:3] ==
sitemap_url[:3]` under the cache. Emit it as `pairfile` with `segment_smu(member1)` —
verified witness above (`caseB`). No blocker for G5/G7: G5 already witnesses V2 on two
seeds; G7's planned shape is the defeating shape for the defpos band.
