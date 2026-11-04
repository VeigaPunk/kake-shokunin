# Correction — `c2_survivors.*` (secondary self-written reference sweep)

`receipts/c2_survivors.txt` / `.json` were produced by `probe_survivors.py` comparing a
**v2-order** self-written reference (`ref_vary_match.py`) and its mutants against the module
that was then loaded from `c88_vary.py` — which by that moment was the **v3** counter.

Consequently the section printed as

```
m19 guard-removal differential over 40000 random inputs: 5 splits
```

is an artefact of that cross-version comparison, not a property of the mutant. All five
"split" payloads carry `vary: '*'` with a malformed request map: the v3 module labels them
`invalid`, the v2-order reference returns `mismatch`.

Re-measured correctly, in process, against the mutant's **own** base over 100,000 inputs
(100k `reference()` comparisons, same adversarial value pool):

```
m19-vs-own-base splits over 100000: 0
```

→ `m19_empty_member_guard_removed` is an **equivalent mutant**. The guard
`if not members or any(m == '' for m in members)` is redundant with `is_token('')`, so removing
it cannot change a verdict.

Everything else in `c2_survivors.*` stands: the five population class counts are v3 counts
(the module loaded was v3 at probe time), and the four witness divergences (m08, m11, m16, m17)
are adversarial value comparisons that do not touch the star rule. The same four classes also
appear as survivors of ExecReader's candidate in `exec_survivors.json`, which is the primary
dataset for this seat.

Related, same cause: `ref_vary_match.py` is a v2-order implementation and therefore scores
`20/20 + 197/200` under the **v3** counter (failing `r53`, `r150`, `r193`), and `20/20 + 200/200`
under **v2**. Its sweep in `c2_sweep.*` ran while the live counter was still v2, so that
baseline was green and those kill counts are valid for the v2 instrument.
