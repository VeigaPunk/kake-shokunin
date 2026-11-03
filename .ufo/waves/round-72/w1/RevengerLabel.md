# RevengerLabel — c66 gate-status counter: `historical` label semantics (read-only)

## Verdict

- **false_historical_possible = no** — a `historical` row whose tip run is green (`e_T == 0`) is
  unconditionally classed `historical_but_green` (lines 586–587) and is therefore excluded from
  `agreement` (679). The counter never counts a false historical as agreement.
  (Caveat: the class is an *observation* class, so it does not turn the round verdict red — see (4).)
- **pin_ancestor_required = yes** — a `historical` row whose 40-hex pin is not an ancestor of the
  tested revision is classed `pin_not_ancestor` (549–552), never runs the pin observation (562–570),
  and cannot reach zero classes.
- Third fact needed to read C1: these two are *observation* mismatches, not structural; only
  `STRUCTURAL_CLASSES` (107–110) gates `met` (682–683).

## Provenance of the bytes read

- Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin` (read-only; no mutating git/jj run).
- Source: `git show 3c68645a:.ufo/waves/round-66/c66_gate_status_hostportable.py` (RC 0).
- sha256 `9beef91f77a644c7697366084b5f26dcbbac2a22b943fd20c8e284ec761a9051`; blob
  `a3c845983771b539f160dc3ac15edfab37840da5` — identical at base `3c68645a` and at freeze
  `a19d38ea` (C1 untouched by freeze).
- Demonstration method: the frozen file was copied byte-identically to scratch and imported; the
  fixture calls the counter's own `measure(root, revid, work, jobs, frozen=...)`, the same override
  hook its own selftest uses (953, 1246). The label algebra under test (`eval_member`, 505–599) is
  not reached through any other path. Fixture gates are toy counters with controlled exits.

## (1) `historical` label with a red pinned run (`e_P != 0`)

Line 590–591:

```
590        if e_P is not None and e_P != 0:
591            res["classes"].append("historical_not_green_at_pin")
```

- **Observation mismatch, not structural.** `historical_not_green_at_pin` is absent from
  `STRUCTURAL_CLASSES` (107–110); `structural` counts only that set (680–681) and `met` requires
  `structural == 0` (682–683). It is in `CLASS_ORDER` (97–101) only for print ranking.
- Effect: it adds to `mismatches` (676), removes the member from `agreement` (679), and prints
  `MISMATCH historical_not_green_at_pin` (708). It does not rewrite the label, does not reject the
  row, does not make the member unevaluable when `e_P` is a family verdict (574–575), and does not
  by itself change the exit code.
- It fires for *any* non-zero `e_P`, not only the red exit 1: `e_P = 2` produces the same class
  (probe1 row `c55_a` below). It does **not** fire when no pin run happened (`pin_not_ancestor`
  leaves `e_P = None`, 549–552).
- The two historical predicates are independent, so a row can carry both classes: `e_T = 0,
  e_P = 1` → `['historical_but_green', 'historical_not_green_at_pin']` (probe1 `c59_a`).

Real-lane corroboration (wave receipt, not my observation): `.ufo/waves/round-72/controls/c1-base.txt`
line 69 reads `members=28 evaluated=28 mismatches=4 structural=0 agreement=24 scores_held=3/3
met=True` with `exit=0` — four observation mismatches, verdict still met. The same receipt line 45
shows the C1 target row at base: `c56_selftally.py label=live e_T=1 eval=ok MISMATCH live_not_green`.

## (2) A `historical` pin that is not an ancestor of the tip

Cannot count as agreement. Lines 542–552:

```
542    if label in ("historical", "never-met"):
543        m = HEX40.search(kind)
544        if m is None:
545            res["classes"].append("unpinned")
546        else:
547            cand = m.group(0)
548            strict = label == "never-met"
549            if is_ancestor(root, cand, revid, strict=strict):
550                pin = cand
551            else:
552                res["classes"].append("pin_not_ancestor")
```

`is_ancestor` is `git merge-base --is-ancestor cand revid` (190–194). A non-ancestor pin
(549 fails) is a **structural** class (109), `pin` stays `None`, so `pin_run` is false (562) and no
pin observation exists (568–570). Both a side-branch pin and a fabricated 40-hex give
`pin_not_ancestor`, not `unpinned` (probe1 `c52_c`, `c55_b`).

Strictness asymmetry: `strict` is true only for `never-met` (548), so a `historical` pin equal to
the tested revision would be accepted as an ancestor. That hole is unreachable for agreement: with
`pin == revid`, `e_P == e_T`, and zero classes require `e_T == 1` together with `e_P == 0` — a
contradiction; either branch would fire (586–591). No committed row can contain the hash of the
commit that contains it in any case.

## (3) What `agreement` counts, and a green tip on a historical row

`agreement` is **not** literally "zero label mismatches". Line 679:

```
679    agreement = sum(1 for r in results if not r["classes"])
```

It counts members with an empty `classes` list, so structural exclusions count too: in probe1,
`c52_c` and `c55_b` have no label observation at all (`e_P = None`) yet are excluded from
agreement, which came out `agreement=2` of 8. The docstring wording at 39–41 ("members carrying
zero v1-class label mismatches") is narrower than the code; the code's set is a strict subset.
`mismatches` (676) and `structural` (680) are separate sums over the same list.

Yes, a `historical` row with a green tip is a disagreement: `historical_but_green` (586–587) empties
the list (679). Probe2: 28 members, all historical, tip red except `c59_b` (green tip) →
`agreement=26`, and the clean set is exactly the 26 red-tip rows.

## (4) Does the counter accept a `historical` label on a green-tip member?

No, in the agreement sense, and the behaviour is unconditional:

```
585    elif label == "historical":
586        if e_T == 0:
587            res["classes"].append("historical_but_green")
588        elif e_T != 1:
589            res["classes"].append("historical_bad_exit")
```

`e_T == 0` fires regardless of the pin, of `e_P`, and of the pin's validity. So a false historical
can never be silently counted. The counter's own selftest asserts this (`964`:
`.ufo/waves/round-52/c52_a.py: "historical_but_green"`, with the scenario comment at 891).

Two boundaries, both demonstrated:

- The class is observation-only, so the round verdict does not police a false historical. Probe2
  (28 members, `historical_but_green` on `c59_b`, `historical_not_green_at_pin` on `c59_a`):
  `MEASURE {'evaluated': 28, 'agreement': 26, 'structural': 0, 'mismatches': 2}`, `exit=0` — i.e.
  `met=True` while two labels are false. The counter reports, it does not gate.
- Label derivation is keyword presence, not a parse: `has_hist = "historical" in words_lc` (533).
  Probe1 `c59_b` with Kind ``gate (not historical: green at `<pin>` only)`` is labeled
  `historical` and reaches zero classes (`agreement=2`, `c59_b` clean). This is a *different*
  falsehood (an explicit negation), outside the (4) definition, but it is the nearest thing to a
  false-historical acceptance the code allows.

## Evidence (commands, outputs, exit codes)

1. `git show 3c68645a:.ufo/waves/round-66/c66_gate_status_hostportable.py` → RC 0; sha256
   `9beef91f…9051`; blob `a3c8459…` at both `3c68645a` and `a19d38ea`.
2. `git merge-base --is-ancestor 4cb225fb032b04166fb0232bc98a7bcce72675ec 3c68645a…` → RC 0
   (the C1 pin is an ancestor of base; the pin gate at 549 would accept it).
3. `TMPDIR=<scratch> python3 -B probe.py` → RC 0 (fixture `members=8 held=3 exit=1`):
   ```
   c52_a.py  label=historical e_T=0 e_P=0 eval=ok classes=['historical_but_green']
   c52_b.py  label=historical e_T=1 e_P=0 eval=ok classes=[]
   c52_c.py  label=historical e_T=1 e_P=None eval=ok classes=['pin_not_ancestor']
   c52_d.py  label=historical e_T=1 e_P=1 eval=ok classes=['historical_not_green_at_pin']
   c55_a.py  label=historical e_T=1 e_P=2 eval=ok classes=['historical_not_green_at_pin']
   c55_b.py  label=historical e_T=1 e_P=None eval=ok classes=['pin_not_ancestor']
   c59_a.py  label=historical e_T=0 e_P=1 eval=ok classes=['historical_but_green', 'historical_not_green_at_pin']
   c59_b.py  label=historical e_T=1 e_P=0 eval=ok classes=[]
   MEASURE {'evaluated': 8, 'agreement': 2, 'structural': 2, 'mismatches': 6}
   ANCHEK self_pin_strict_false=True self_pin_strict_true=False side_vs_tip=False
   ```
   (`c59_b`'s Kind is the negated form from the caveat above.)
4. `TMPDIR=<scratch> python3 -B probe2.py` → RC 0 (fixture `members=28 held=3 exit=0`):
   ```
   MEASURE {'evaluated': 28, 'agreement': 26, 'structural': 0, 'mismatches': 2}
   ROW .ufo/waves/round-59/c59_a.py label=historical e_T=1 e_P=1 classes=['historical_not_green_at_pin']
   ROW .ufo/waves/round-59/c59_b.py label=historical e_T=0 e_P=0 classes=['historical_but_green']
   ```
5. Receipts read for corroboration only: `controls/c1-base.txt` lines 45, 69 (above);
   `controls/c56-pin-linux.txt` tail `revision: 4cb225fb…` `EXIT=0` (pin run green);
   `c1-base.txt` also carries a real accepted historical row,
   `.ufo/waves/round-59/c59_quote_truth.py label=historical e_T=1 e_P=0 eval=ok ok`.

No tool was installed; python3 3.14.8 and git 2.56.0 as shipped. No pacman transaction was run.

## Divergences found inside the frozen counter

- **D1 (code vs docstring):** `agreement` documented as "zero v1-class label mismatches" (39–41),
  implemented as "zero classes of any kind" (679); structural exclusions also subtract from it.
- **D2 (predicate string vs code):** `PREDICATE` (78) prints `members == 28 AND evaluated == 28 AND
  scores_held == 3`, omitting the `structural == 0` term enforced at 682–683 (Amendment 1 rationale
  at 41–45). The JSON `predicate` field (1333) therefore under-describes `met`.
- **D3 (label parsing):** presence of the word `historical` (533), no negation handling; `historical`
  and `never-met` together are `label_invalid` (536–538) but `not historical` is `historical`.
- **D4 (class independence):** both historical classes can fire on one row (586–591; probe1 `c59_a`).
- **D5 (strictness asymmetry):** `strict` applies only to `never-met` (548); `historical` accepts
  `pin == revid` as an ancestor, harmless for agreement by the argument in (2).
- **D6 [INFERENCE from reading]:** `e_P` outside `FAMILY_VERDICTS` clears `evaluated` (574–575) while
  the `historical_not_green_at_pin` class is still recorded, so `met` fails on the evaluated term,
  not on the label term.

## Confidence

High for (1)–(4): each is a direct line citation plus an executed fixture on the frozen code path;
(4)'s negative is corroborated by the counter's own selftest assertion (964) and by the real-lane
receipt (45, 69). The only reading-only item is D6, marked as inference.

Scratch tree `/fast/scratch/hyaku/kake-r72/RevengerLabel/` (copies, fixtures, outputs) was removed
before yield; no lane tree file other than this report was touched.
