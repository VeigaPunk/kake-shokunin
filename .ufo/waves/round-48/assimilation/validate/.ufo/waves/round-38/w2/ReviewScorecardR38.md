# ReviewScorecardR38 — round-38 falsification

Scope: `SCORECARD.md` round-38 sections and the two earlier capability rows changed by this diff. Axes: operability; freshness/publishing only where the scorecard makes a boundary claim. Findings below assess statements, not round admission.

## Findings

1. **P2 — C2 pre-score classification is not evidenced.** `SCORECARD.md:2243-2251` says the control classes were named before v3 scores were read and classifies four 20/20 wrapper files as builds, not controls. The same SHA-256s have C1 control receipts and C2 v3 receipts (`verification/control-CtlBaseWrapper-care.json:7-11`, `verification/v3/CtlBaseWrapper-care.json:7-11`; likewise delegate ceiling and rulepatch tools). `w1/CriticControlReceipts.md:27` records the first v3 receipt at 01:28:03 and `SCORECARD.md` mtime at 01:28:53, with the four 20s already present. The v3 measurements are also explicitly said to precede this declaration (`SCORECARD.md:2237`). **Verdict: overstated/unsubstantiated ordering**; the repository does not establish a pre-score C2 class freeze. This does not negate that these wrappers implement the listed behavior.

2. **P3 — v2 mutation total is wrong in the table and withdrawal paragraph.** `SCORECARD.md:2194,2199` says 28/42 meet. Counting all 42 `verification/mutref/M*.json` receipts gives scores 16×5, 18×8, 19×16, 20×13, hence **29** meet the v2 `>=19` predicate. The later correction at `SCORECARD.md:2282-2283` is accurate (13 at 20, 16 at 19), but leaves the earlier 28s stale. **Verdict: 28 is wrong; correction to 29 holds.**

3. **P3 — “Every tool a seat named was scored” is too broad.** `SCORECARD.md:2178` is contradicted for `MutCounterV2`: its dummy-key fixture tools are listed at `ctl/MutCounterV2.md:48-57`, and `w1/CriticControlReceipts.md:37` records 8 fixture tools and 10 counter mutants without receipts. Those are counter probes, not robots-audit controls; the narrower claim that every robots-audit control named was scored holds. **Verdict: overbroad as written, immaterial to the robots-audit control table.**

4. **P3 — C1 predicate-string equivalence is false.** `SCORECARD.md:2101-2104` says the `met: ...` sentence is the `PREDICATE` and every receipt field. The v2 constant is `sealed_count.py:56` (`passed >= 19...`, no `met: `); `verification/c1-at-af43a50f.json:3` likewise omits the prefix. `SCORECARD.md:2207` discloses this later, and C1 was withdrawn. **Verdict: C1 wording wrong; later disclosure accurate; no live C2 effect.**

## Attacked statements / verdicts

- Round-37 closure control: 28/28 receipt holds (`round-37/verification/control-CtlC1Shortcut-followup.json:8-11`); commit `ccc3b2b9` at 00:29:45-03 precedes build `9dbc88bb` at 00:39:37-03. **Holds.**
- C1 base 8/20 and C1 pre-separation scores (reference 20, base 8, round-37 controls 7/5/1/1/0/0, eight ablations 16–18): **holds** in `verification/c1-at-af43a50f.json`, `verification/pre/*.json`; hashes match pins (v2 counter `52daff55a2b897ba814eed134cd6bfe0de28305bf4ab82e87a5c6d1ae7096e7b`, C1 key `8b3fac55864195602fa2f4c1608e900c6ab708aef4f9cc0fbaa27ef2e5992941`).
- C1 control table except mutant total: **holds** in 12 v2 control receipts; seven `.ctl/*.md` reports are present. C1 after-score at the later C2 build file also passes v2 20/20 (rerun below), though no C1 build seat was dispatched.
- C2 base 8/20, build 20/20, reveal refusal exit 2: **holds** in receipts and reruns. Tool SHA-256 `f4d057c4afac885b998de404da8c19f2d5d0a4d754a9d539e49b07d3f36baace`; v3 counter `28b120a5a38061825094c17f0e978d7e6a5ec3fb131094e2cdfd59360f38f9e4`; key pin/reveal `749ef6a65de67f09abffad33fa6d7efcb1e7f1515b1d2fa51a93ff9977b63aa6`. V3 controls, 42 mutants (16–19), eight ablations (16–18), `CtlExampleK` 19/20, and harm receipts match their stated scores. The 43 distinct excluded-ASCII-character checks are present; every one of 22 case runs states `checksEvaluated`.
- Before-build order: **holds**. `b0ab7f6` (C1) < `2dab7f3` (withdrawal/C2 declaration, 04:28:54Z) < wave-1 dispatch (`w1-dispatched-at.txt`: 04:29:52Z) < `3ed8e15c` build (04:38:59Z) < `99357694` reveal (04:39:18Z). Build commit changes only `scripts/robots_audit.py`.
- Earlier-line rewrite: diff is 223 insertions and 2 deletions; only existing `SCORECARD.md:198,2010` rows changed, each appending the round-37 “not admitted” status/closure pointer. No other prior lines were rewritten. **Holds; additions match the closure correction.**

## Commands and exits

- `git diff --unified=0 af43a50fa399881eead9381d835b78a015e277a6 adab4c7e9ec2178657395f49346f18800ff4796f -- SCORECARD.md` → **0**; 223 insertions, 2 deletions.
- `git log --format='%H %cI %s' --reverse af43a50fa399881eead9381d835b78a015e277a6..adab4c7e9ec2178657395f49346f18800ff4796f` → **0**; chronology above.
- `git show -s --format='%H %cI %s' ccc3b2b9c16dc2278bca5009792d5c12ec569b74; git show -s --format='%H %cI %s' 9dbc88bb` → **0**; round-37 control 00:29:45-03 precedes build 00:39:37-03.
- `git diff-tree --no-commit-id --name-only -r 3ed8e15c2707ac4cec88f48fc9be48b35be4f2b0` → **0**; only `scripts/robots_audit.py`.
- From the sandbox clone with `TMPDIR=/fast/scratch/hyaku/kake-r38w2/ReviewScorecardR38/tmp`, `timeout 60 python3 -B .ufo/waves/round-38/sealed_count.py --root . --revision af43a50fa399881eead9381d835b78a015e277a6 --key-revision 99357694f68886d3175fc6c386979c350be789bc` → **1**, 8/20; same command at revision `3ed8e15c2707ac4cec88f48fc9be48b35be4f2b0` → **0**, 20/20.
- `timeout 60 python3 -B .ufo/waves/round-38/sealed_count_v3.py --root . --revision af43a50fa399881eead9381d835b78a015e277a6 --key-revision 99357694f68886d3175fc6c386979c350be789bc` → **1**, 8/20.
- Same command with `--revision 3ed8e15c2707ac4cec88f48fc9be48b35be4f2b0` → **0**, 20/20; with `--revision 99357694f68886d3175fc6c386979c350be789bc` → **2**, key visible.
- `timeout 10 python3 -c 'import glob,json,collections; files=glob.glob(".ufo/waves/round-38/verification/mutref/M*.json"); counts=collections.Counter(json.load(open(p))["passed"] for p in files); assert len(files)==42 and counts=={18:8,16:5,19:16,20:13}; print("files=42 score_counts=",sorted(counts.items()),"met_ge_19=",sum(v for k,v in counts.items() if k>=19))'` → **0**, 29 met.

## Residual risk / verification gaps

I inspected the committed harm/selftest receipts and W1 reports but did not rerun those selftests or the 64-MiB performance probe. The scorecard itself marks the independent implementation’s C2 score as pending (`SCORECARD.md:2280-2281`); it is not a passed C2 measurement.