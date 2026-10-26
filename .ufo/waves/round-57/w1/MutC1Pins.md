# MutC1Pins

Mutation probe of the C1 counter `.ufo/waves/round-57/c57_receipt_pins.py` and its `--selftest`.
Method: pristine copied to a `mktemp -d` scratch dir; 18 single-point mutants applied to the scratch copy only;
each mutant run as a fresh `python3 -B mut_<id>.py --selftest`. Detector = exit != 0 or any `FAIL ` line.
Baseline: pristine selftest **19/19 PASS, exit 0** (detector sound) — re-confirmed after all runs.
Lane file never written; sha256 `d0d0dc1f725a…c9c22e0f` identical before and after; scratch pristine likewise.
Tooling: python3 + git only, nothing installed. Bounds: writes were the scratch dir and this report only.

## MUTANTS:

| id | change | selftest result |
|----|--------|-----------------|
| M01 | `cur != prev` -> `cur == prev` (relabel guard inverted) | KILLED exit=1 (3 FAILs, incl. "old relabel undisclosed") |
| M02a | drop `not NEW_RE.match` conjunct, keep WAVE-prefix | SURVIVED (equivalent: every NEW_RE path already starts with `round-57/`; filter set identical for all inputs) |
| M02b | drop WAVE-prefix conjunct, keep only `not NEW_RE.match` | SURVIVED (exit 0, no FAIL) |
| M03 | `--first-parent` removed from history log | SURVIVED (all 19 scenarios are linear histories) |
| M04 | `is_ancestor` always True | KILLED exit=1 (2 FAILs: "not an ancestor of the receipts", "measured.json names another commit") |
| M05 | `measured_rev != intro` conjunct removed | SURVIVED (no fixture pins measured at the receipts' intro commit) |
| M06 | `len(revs) == 1` -> `>= 1` | KILLED-FLAKY (run A: 1/3, run B: 2/3 of selftest invocations; ~50%/run — kill depends on `next(iter(revs))` set order, i.e. PYTHONHASHSEED) |
| M07 | errata compare on 3 of 4 fields (`to` dropped) | KILLED exit=1 ("old relabel disclosed with matching errata" -> undisclosed=1) |
| M08 | phantom check removed (`phantom = []`) | KILLED exit=1 ("errata names nothing git shows" -> met=True) |
| M09 | deleted-receipt counter always 0 | KILLED exit=1 ("receipt deleted" -> met=True) |
| M10a | POP_RE rounds widened to `round-[0-9]+` | KILLED exit=1 ("round outside 52-57 is out of population" -> undisclosed=1) |
| M10b | POP_RE rounds narrowed to `5[6-7]` | SURVIVED (no scenario uses rounds 52-55) |
| M11 | REV_RE loses the `=` form (`[:=]` -> `:`) | KILLED exit=1 ("= form relabel detected" -> undisclosed=0) |
| M12 | `scorecard_pin` always 1 | KILLED exit=1 ("SCORECARD omits the pin" -> met=True) |
| M13 | `met()`: `new_receipts == 3` -> `>= 1` | KILLED exit=1 ("new receipt missing claim 3" -> met=True) |
| M14 | `reversed(commits)` dropped (newest-first version walk) | KILLED exit=1 (2 FAILs: "disclosed with matching errata", "pin line stripped later") |
| M15 | oldest-add selection `[-1]` -> `[0]` | SURVIVED (linear fixtures: exactly one A entry per path, so identical) |
| M16 | main() exit-code swap (`0 if met else 1` -> `1 if met else 0`) | SURVIVED (selftest returns before main(); exit mapping never exercised) |

Score: **11 killed (1 flaky), 7 survived, 0 not-applied.**

## SURVIVORS:

- **M02a** — *equivalent mutant*, no fixture can kill it: `NEW_RE` paths are a subset of the `startswith(f"{WAVE}/")` check, so the two filters accept exactly the same relabels for every input. Cleanup candidate only, not a coverage gap.
- **M02b** — a relabelled round-57 *non-claim* control receipt (e.g. `round-57/controls/tooling.txt`) would be double-counted: `undisclosed_relabels` AND `new_relabelled`. Current fixtures only relabel round-56 receipts and claim receipts.
- **M03** — every selftest history is linear, so `--first-parent` is a no-op there. Note: pristine `git log --first-parent` diffs merges against the first parent (`--diff-merges=first-parent` default), so merge-introduced relabels *are* seen; dropping the flag only changes *which commit* records them (side commit vs merge), which no fixture's errata distinguishes.
- **M05** — nothing pins `measured.json` at the receipts' own introducing commit; the strict-ancestor guard (`measured_rev != intro`) is untested.
- **M06** — a receipt with two revision lines, one equal to the measured revision, flips on `next(iter(revs))` set order; per process the outcome is a coin toss (observed: 6/6 killed in one process, 0/6 in another).
- **M10b** — rounds 52-55 receipts can silently leave the population; fixtures only use round-56.
- **M15** — with delete+re-add of a receipt path, `[0]` picks the re-adding commit instead of the true introduction; no fixture re-adds a receipt.
- **M16** — `--selftest` never reaches `main()`'s exit-code mapping; the 0/1/2/64 contract is untested by construction.

## PROPOSED FIXTURES:

All validated in the scratch lab: each scenario PASSES on pristine and FAILS on its mutant (actual outputs recorded). `F06` is probabilistic by nature.

```python
def f02b(sb):  # kills M02b — validated: pristine met=False,new_relabelled=1,undisclosed=0; mutant undisclosed=1
    O = ".ufo/waves/round-57/controls/tooling.txt"
    sb.commit({O: f"revision: {'a' * 40}\n"}, "other receipt")
    sb.commit({O: f"revision: {'b' * 40}\n"}, "relabel other")
    return honest(sb)
scenario("round-57 non-claim control relabelled", f02b, False, {"new_relabelled": 1, "undisclosed_relabels": 0})

def f03(sb):  # kills M03 — pristine met=True (errata names the merge commit); mutant records the relabel
    honest(sb) # at the side commit -> undisclosed=1, phantom=1
    r1 = git log --format=%H -- <OLD> | last     # oldest commit touching OLD
    git checkout -q -b side r1; sb.commit({OLD: f"revision: {'b' * 40}\nEXIT=0\n"}, "side relabel")
    git checkout -q -; git merge --no-ff -m "merge side" side; merge = git rev-parse HEAD
    return sb.commit({ERRATA: _json({"entries": [{"path": OLD, "from": "a" * 40, "to": "b" * 40, "commit": merge}]})},
                     "disclose merged relabel")
scenario("side-branch relabel disclosed at the merge commit", f03, True, {"undisclosed_relabels": 0, "phantom_errata": 0})

def f05(sb):  # kills M05 — pristine new_unpinned=3 (measured == intro); mutant unpinned=0
    tipr = honest(sb)
    return sb.commit({MEASURED: _json({"revision": tipr}),
                      "SCORECARD.md": f"# s\n## Round 57 — measured\nmeasured at {tipr}\n",
                      **{p: f"C{n} met=True\n  revision: {tipr}\nEXIT=0\n" for n, p in NEWP.items()}},
                     "re-pin everything at the receipts' introduction")
scenario("measured revision equals the receipts' introduction", f05, False, {"new_unpinned": 3})

def f06(sb):  # kills M06 with p=7/8 per invocation (vs p=1/2 for the existing single-pair scenario);
    sb.commit({OLD: f"revision: {'a' * 40}\nEXIT=0\n", "SCORECARD.md": "# s\n"}, "old receipt")
    base = sb.commit({f"{WAVE}/x": "x\n"}, "round 57 work")
    sb.commit({MEASURED: _json({"revision": base}),
               "SCORECARD.md": f"# s\n## Round 57 — measured\nmeasured at {base}\n"}, "pins")
    nr = {NEWP[n]: f"C{n} met=True\n  revision: {base}\n  revision: {chr(ord('c') + n - 1) * 40}\nEXIT=0\n"
          for n in (1, 2, 3)}              # distinct partners c/d/e*40 decouple the three set orders
    return sb.commit(nr, "receipts")
scenario("new receipts each carry a distinct second revision line", f06, False, {"new_unpinned": 3})

def f10b(sb):  # kills M10b — pristine undisclosed=1; narrowed regex misses round-54 -> met=True
    R54 = ".ufo/waves/round-54/controls/after-c1.txt"
    sb.commit({R54: f"revision: {'a' * 40}\n"}, "r54 receipt")
    sb.commit({R54: f"revision: {'b' * 40}\n"}, "r54 relabel")
    return honest(sb)
scenario("round-54 relabel undisclosed", f10b, False, {"undisclosed_relabels": 1})

def f15(sb):  # kills M15 — pristine intro=[-1]=t -> new_unpinned=3; mutant intro=[0]=re-add -> unpinned=0
    t = honest(sb)
    sb.commit({p: None for p in NEWP.values()}, "delete receipts")
    sb.commit({p: f"C{n} met=True\n  revision: {t}\nEXIT=0\n" for n, p in NEWP.items()}, "re-add receipts")
    return sb.commit({MEASURED: _json({"revision": t}),
                      "SCORECARD.md": f"# s\n## Round 57 — measured\nmeasured at {t}\n"}, "pin first intro")
scenario("receipts deleted and re-added; pin names the first introduction", f15, False,
         {"new_unpinned": 3, "deleted_receipts": 3})

def scenario_cli(name, build, want_exit):  # kills M16 — needs a CLI-level check, selftest cannot reach main()
    sb = Sandbox()
    try:
        tip = build(sb)
        p = subprocess.run([sys.executable, "-B", __file__, "--root", sb.d, "--revision", tip],
                           capture_output=True, text=True)
        results.append((f"{name}: exit={p.returncode}", p.returncode == want_exit))
    finally:
        sb.close()
scenario_cli("met repo exits 0", lambda sb: honest(sb), 0)                       # validated: pristine 0/1, M16 1/0
scenario_cli("unmet repo exits 1", lambda sb: honest(sb, old_relabel=True), 1)
```

M02a: no fixture exists or can exist (equivalent mutant) — recommend collapsing the filter to the single
WAVE-prefix test (or the NEW_RE test) so future readers don't assume two independent guards.

VERDICT: 18 mutants, 11 killed by `--selftest` (M06 only flakily, ~50%/run), 7 survived; killer fixtures for
6 of 7 survivors validated in the scratch lab (M02a is equivalent, unkillable) — selftest coverage gaps are
merge histories, non-claim round-57 controls, measured==intro pinning, rounds 52-55, receipt re-adds, and
main()'s exit codes.
