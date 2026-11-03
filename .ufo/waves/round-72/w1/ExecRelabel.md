relabel_numstat=1 agreement_base=24 agreement_tip=25 mismatches_base=4 mismatches_tip=3 changed_members=c56_selftally.py pin_exit=0 c72_exit=0 census_exit=0

# ExecRelabel — C1 relabel build/verify (round 72, w1)

C1 verdict: **met** under the frozen contract predicate. The gate-status counter agrees 25/28 at the
relabel tip (base 24/28); the only member whose per-member label agreement changes between base and
tip is `c56_selftally.py` (disagreement -> agreement). Scratch clone only; the lane tree was not
mutated (only this report plus the receipts/patch below were written under
`.ufo/waves/round-72/w1/`). Scratch commit RL = `84b5ecff97548bc8b731f1b3003bc9ec5e7c24c6`.

## Evidence (commands, exit codes)

Setup — clone of base, verified root before any write:

```
S=/fast/scratch/hyaku/kake-r72/ExecRelabel
git clone --shared -q /home/vgpnk/Projects/shokunin/kake-shokunin $S/clone           # exit 0
git -C $S/clone checkout -q 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1               # exit 0
git -C $S/clone rev-parse --show-toplevel   -> $S/clone
git -C $S/clone status --porcelain | wc -l  -> 0
```

Relabel (single row, second cell only). Row located at SKILL.md:1253; first cell exactly
`selftest-tally-counter`; Kind cell replaced with the seat-spec text (503 chars, byte-equal to the
spec string, verified char-by-char).

```
git -C $S/clone diff --numstat            -> 1	1	SKILL.md          # exactly one line, exit 0
git -C $S/clone diff --numstat | wc -l    -> 1
git -C $S/clone -c user.name=kake-scratch -c user.email=kake@scratch.local \
    commit -q -am 'docs(skill): re-adjudicate selftest-tally-counter as historical'   # exit 0
git -C $S/clone rev-parse HEAD            -> 84b5ecff97548bc8b731f1b3003bc9ec5e7c24c6
git -C $S/clone format-patch -1 --stdout > <lane>/.ufo/waves/round-72/w1/c56-relabel.patch
wc -l c56-relabel.patch                   -> 26; stat 1 file changed, 1 insertion(+), 1 deletion(-)
```

Cell-structure check (Python, analysis only): base and tip rows both split to 10 pipe-delimited
fields; differing field indices = `[2]` (the second cell, Kind); fields 0,1 and 3-9 byte-identical;
SKILL.md line count 1396 at both revisions; no other line differs (numstat 1/1).

Patch applicability check against an independent fresh clone at base:

```
git clone --shared -q <lane> $S/check/clone; git -C $S/check/clone checkout -q 3c68645a   # exit 0
git -C $S/check/clone apply --check <patch>   -> exit 0
git -C $S/check/clone apply <patch>; git -C $S/check/clone diff --numstat -> 1	1	SKILL.md
```

c66 gate-status at the relabel tip (run from the lane dir; TMPDIR=$S). Full output:
`.ufo/waves/round-72/w1/c1-relabel-tip.txt` (70 lines).

```
python3 -B .ufo/waves/round-66/c66_gate_status_hostportable.py \
  --root $S/clone --revision 84b5ecff97548bc8b731f1b3003bc9ec5e7c24c6 --jobs 6
exit=0
C1 gate-status members=28 evaluated=28 mismatches=3 structural=0 agreement=25 scores_held=3/3 met=True
  .ufo/waves/round-56/c56_selftally.py label=historical e_T=1 e_P=0 eval=ok ok
```

c66 gate-status at base 3c68645a (same root/clone). Full output:
`.ufo/waves/round-72/w1/c1-base-recheck.txt` (69 lines).

```
python3 -B .ufo/waves/round-66/c66_gate_status_hostportable.py \
  --root $S/clone --revision 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1 --jobs 6
exit=0
C1 gate-status members=28 evaluated=28 mismatches=4 structural=0 agreement=24 scores_held=3/3 met=True
  .ufo/waves/round-56/c56_selftally.py label=live e_T=1 eval=ok MISMATCH live_not_green
```

Matches the contract's base receipt `controls/c1-base.txt` verbatim on the summary line (24/4/28).

Member-level diff base vs tip (normalized `path|label ... status`, sorted):

```
diff <(base members) <(tip members)   -> exit 1, exactly one changed line, 19c19
< .ufo/waves/round-56/c56_selftally.py|label=live e_T=1 eval=ok MISMATCH live_not_green
> .ufo/waves/round-56/c56_selftally.py|label=historical e_T=1 e_P=0 eval=ok ok
```

All other 27 members identical, including the three residual tip mismatches `c57_idresolver_gate`,
`c58_resolver_cases`, `c59_resolver_cases` (label=live, live_not_green), present in both runs.
`changed_members=c56_selftally.py` only.

Pin proof (run in $S/clone). Full output `.ufo/waves/round-72/w1/c56-pin-run.txt`:

```
python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision 4cb225fb032b04166fb0232bc98a7bcce72675ec
exit=0
C1 selftest-tally tally_mismatches=0 rows_checked=10 met=True
```

Tip-side cited receipt `controls/c56-tip-linux.txt` backs the cell's red claim:
`tally_mismatches=6 rows_checked=10 met=False`, six `MISMATCH tool_changed` rows
(base-path-audit, source-recheck-audit, robots-expectation-audit, sitemap-file-audit,
redirect-expectation-audit, commit-citation-lint), `EXIT=1` — observed equals claim in every row.

C2 unchanged-tree check (frozen round-72 counter at RL). Full output
`.ufo/waves/round-72/w1/c72-run.txt`:

```
python3 -B .ufo/waves/round-72/c72_tmp_v2.py --lane $S/clone --revision 84b5ecff97548bc8b731f1b3003bc9ec5e7c24c6
exit=0
C2v2 revision=84b5ecff... brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=8 added=8 guard=ok met=True
```

Census gate. The literal seat command is not root-shaped and exits 2, so it was adapted by
supplying a scratch fleet root that carries the real kake conf row and a lane symlink to the clone:

```
scripts/sources-census.sh validate --root $S/clone kake
  exit=2  ERROR: config not found: $S/clone/shokunin.conf
          ERROR: unknown lane (not a dir, not in conf or root): kake

mkdir -p $S/censusroot
grep -E '^[[:space:]]*kake[[:space:]]*\|' /home/vgpnk/Projects/shokunin/shokunin.conf \
  > $S/censusroot/shokunin.conf          # one row: kake|kake-shokunin|operability + freshness (...)
ln -sfn $S/clone $S/censusroot/kake-shokunin
scripts/sources-census.sh validate --root $S/censusroot kake
  exit=0  (16 W04 duplicate-URL warnings, no E findings)
  kake	ok	/fast/scratch/hyaku/kake-r72/ExecRelabel/censusroot/kake-shokunin/corpus/SOURCES.md
```

Full output: `.ufo/waves/round-72/w1/census-run.txt`.

## Counterexample

None found. Every leg of the C1 predicate holds; no member other than `c56_selftally.py` changes
agreement; the pin run is green; the tip is green for the relabeled member. No kill-rule condition
triggered. `census_literal_exit=2` is a root-binding mismatch of the seat's literal command, not a
census finding: the same registry validates clean once bound to a fleet root (exit 0).

## Caveats / risks

- `--root $S/clone` cannot host `sources-census.sh` (the script requires `<root>/shokunin.conf` and
  resolves lanes as `<root>/<repo>`); the mandated exit-0 run used the adapted scratch root above.
- Base recheck used `--root $S/clone` per the seat step, not the lane path used in the contract's
  base receipt; the counter reads committed bytes and the summary line is identical (24/4/28).
- The census here validates the relabel clone's `corpus/SOURCES.md` (unchanged by this relabel); the
  frontier-step S439 row's own census obligation is outside this seat's scope.
- Tooling: no installs or upgrades performed (no pacman transactions).
- Scratch tree `/fast/scratch/hyaku/kake-r72/ExecRelabel` removed before yield; nothing written
  outside this `w1/` directory, the scratch clone, and the two `/tmp` normalize files
  (`/tmp/execrelabel-c1-*.norm`, <1 KB, removable).
