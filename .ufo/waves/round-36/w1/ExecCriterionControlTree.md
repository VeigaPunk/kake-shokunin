# ExecCriterionControlTree — round-36 wave 1, routed defect 4 (control key-blindness)

Built the criterion check that makes a control report record the tree it was built from and fails
when that tree holds a key; ran it both ways. No path under `/fast/scratch/hyaku/kake-r36/` was
listed, statted, searched or opened here; it appears only as text in the patterns.

## Deliverable (two byte-identical copies)
- `/fast/scratch/hyaku/kake-r36w1/ExecCriterionControlTree/control_tree_check.py`
- `.ufo/waves/round-36/criteria/control_tree_check.py` (landed, mode 755)

sha256 `be52b331552772f4e1c229ccb02cd0197215f8df3bbc472d3578fc0a746f2867`, 267 lines, stdlib
only, reads only the reports given, writes nothing, no network. `--report` and `--pattern`, both
repeatable; exit 1 for no listing or a key path in it, 0 otherwise, 2 for bad input. Listing lines
are `ls -l` entries (`control_tree_check.py:51`) and `git ls-tree` entries (`:53`), `ls` names
joined onto the directory the nearest quoted `ls` command names (`:57`). Matching (`:88`): `/`-
terminated pattern = that directory or anything inside, else a literal last-component prefix; a
container (an `ls` root or `git ls-tree` tree entry, `:156`) also matches when the key is under it.

## Round-35 case — exit 1 (the check fails it)
Build tree = parent tree from the retained bundle in a sandbox clone (`git bundle verify` ok;
`0b7779dc` = `refs/heads/suff/B-topic-cite`).

```
$ git -C <clone> rev-parse 0b7779dc^   -> 7deacc4629c1d05a34fb919d8095e99efc7b712f
$ git -C <clone> ls-tree -r 0b7779dc^ | grep sealed/
100644 blob 4ac1d3fd…  .ufo/waves/round-35/sealed/c1-cases.json
100644 blob 4c704a40…  .ufo/waves/round-35/sealed/c2-probes.json
100644 blob 77dd6416…  .ufo/waves/round-35/sealed/l1-reference-patch-not-landed.diff
$ git -C <clone> ls-tree -r 0b7779dc | grep sealed/   -> (none: the commit deleted sealed/)
```

A — that listing embedded as a control report (`r35-control-tree-report.md`):

```
$ python3 -B control_tree_check.py --report r35-control-tree-report.md \
    --pattern '.ufo/waves/round-35/sealed/' --pattern '.ufo/waves/round-36/sealed/'
FAIL: … lists a key path '.ufo/waves/round-35/sealed/c1-cases.json' (plain) matching pattern '.ufo/waves/round-35/sealed/'.
FAIL: … lists a key path '.ufo/waves/round-35/sealed/c2-probes.json' (plain) matching pattern '.ufo/waves/round-35/sealed/'.
FAIL: … lists a key path '.ufo/waves/round-35/sealed/l1-reference-patch-not-landed.diff' (plain) matching pattern '.ufo/waves/round-35/sealed/'.
exit=1
```

B — the round-35 report as written (`.ufo/waves/round-35/w2/CriticC2Sufficiency.md`) has no listing:
`FAIL: … records no tree listing`, `exit=1`.

## Round-36 control reports — all five pass (exit 0)
```
$ python3 -B control_tree_check.py --report .ufo/waves/round-36/ctl/<NAME>.md \
    --pattern '/fast/scratch/hyaku/kake-r36/.k' --pattern '.ufo/waves/round-36/sealed/'
PASS CtlAllFalse.md / CtlConstantClean.md / CtlNaiveReader.md / CtlNoReader.md / CtlShortcut.md
     "records a tree listing (ls; 3 listed paths) and shows no key path."      exit=0 (each)
```

Each lists only `/fast/scratch/hyaku/kake-r36/controls/<NAME>/` (`.`, `..`, `source_recheck.py`),
which is neither a key path nor an ancestor of the `.k` pattern.

## Falsifiers of the check (selftest.sh: 16 rows, failures=0, exit 0)
F1 `.key` under the key root → 1; F2 no listing → 1; F3 the control's own commit tree → 0; F4 sealed
files listed → 1; F5 sealed dir as tree entry → 1; F6 `git ls-tree` of `.ufo/waves/round-36` → 1; F7
`sealed_count.py`/`_v2` → 0 (the directory rule spares the public counter); F8 missing report → 2; F9
absolute `ls` of the lane's sealed `c2-probes.json` → 1; several reports in one run all get checked.

## Attacks on the criterion (for the L1)
1. **Wrong tree still passes (F3).** The check cannot tell the build tree from the control's own
   commit tree, so a control whose commit deletes the key — exactly 0b7779dc — passes if its report
   lists that commit tree. Remedy outside the check: require `git ls-tree -r <control>^` or the build
   directory's `ls -la` in the report template.
2. **Any unrelated listing satisfies "has a listing"** (F2 vs C); same remedy, and the assigned
   contract cannot close it, so I did not widen it.
3. **Patterns are literal:** `/fast/scratch/hyaku/kake-r36/.k` catches `.k`, `.key`, `.keys/…`.

## Not verified / tooling
No key name confirmed (that tree untouched), so `.k` is used as given. No sealed case, no counter
run, no jj/git write, no tracked lane file touched, no post-integration gate. No installs or upgrades;
pacman not invoked; pre-existing python 3.14.8 and git 2.56.0; every run `timeout`-capped (≤250 s),
nothing left running. Evidence: `…/ExecCriterionControlTree/evidence.log` (75 lines; sections at
`:4`, `:22`, `:29`, `:34`, `:51`, `:71`), `selftest.sh` sha256 `5cb995e3…be3cad`.

Report: .ufo/waves/round-36/w1/ExecCriterionControlTree.md
