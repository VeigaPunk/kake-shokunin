# MutationTesterGates — round 76, wave w1 (kake lane)

Seat: mutation tester for the two new gates. Leaf seat: no subagent dispatch, no commit, no network, lane
checkout read-only; every executed byte lived in `/fast/scratch/hyaku/kake-r76/MutationTesterGates` and is
copied under `MutationTesterGates/mutants/` here.

## 0. What was scored (exact bytes)

|Gate|File scored|sha256|bytes|
|---|---|---|---|
|C1 counter, v0 (frozen with the contract)|`.ufo/waves/round-76/c76_quote_truth.py`|`c931178067bfb53f3d54e59ae10b24fd62550f80403f34244ac10a652da068e3`|18130|
|C1 counter, hardened chain|`w1/ExecQuoteCounter/doc_quote_truth.py` @ `63af0ede…`|`63af0ede46919b213c6dad414b26b9eef5cd23078d741afe0bdb940f44a966c8`|—|
|C1 counter, **final** (amendments 3+4+5 in force)|`w1/ExecQuoteCounter/doc_quote_truth.py` @ `33162b61…`|`33162b61fb2c9cfb4c0ae620ac54c206a620085cf439e22133bb6609ace77b61`|44966|
|C2 tool, **final**|`w1/ExecAuditTool/hreflang_audit.py` @ `0762452f…`|`0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac`|59734|
|C2 matrix|`w1/ExecAuditMatrix/c76_hreflang_matrix.py` @ `b8333969…`|`b83339693bf2c82ab4c6c1c454f212e42cff313d1c415a7a8c9b926500dc7c29`|—|

The two C1 builds `63af0ede` and `33162b61` carry the same mutant ledger *shape*; the 63af0ede run is
reported because amendment 5 D5 cites its defect, and the 33162b61 run is the authoritative one.

Fixture tree for before/after states: `git clone --shared` of the lane at
`b758cb040d53374b1b63b89702c7128f77212d23` (clone tip `b758cb04`, base `a0491fcd`), i.e. the lane's frozen
round tip, untouched.

## 1. Detectors (all bounded, all local, all re-runnable)

|Detector|Command shape|Pristine expectation|
|---|---|---|
|`ST`|`python3 -B <counter> --selftest --work <dir>`|exit 0, every case executed (A5 D5)|
|`BEFORE`|`python3 -B <counter> --root <clone> --revision a0491fcd --base a0491fcd --rounds 75,76`|per D4: `findings=7 met=false`, exit 1|
|`HEAD`|same with `--revision b758cb04`|red until the repair rows land (D4)|
|`P_ARTIFACT`|fixture: the absent span lives only in `round-76/w1/w1-results.json`|red (dispatcher artifacts are never receipts)|
|`P_CASE`|fixture: span `MET=TRUE`, receipt `met=true`|red (matching is exact, not case-folded)|
|`P_SEATREE`|fixture: span only in `round-75/w1/SomeSeat/receipts/notes.txt`|red (A5 D1: the measured round's seat tree is never a receipt)|
|`P_DIAG`|fixture: span only on a line `  T1 SCORECARD.md:1 <span>`|red (A5 D2: diagnostic lines are stripped)|
|`P_DATAEXT`|fixture: span only in `round-74/notes.txt` outside any receipt directory|red (A5 D1)|

Every probe fixture is its own `git init` repo under the scratch work dir; a mutant is **killed** when any
detector leaves the pristine shape (selftest rc, before/head exit+finding count, or any probe verdict).

## 2. C1 mutant ledger — final build `33162b61` (authoritative)

Baseline of that build: `ST 53/53 passed, exit 0`; `BEFORE findings=8 met=false rc=1`;
`HEAD findings=8 met=false rc=1`; all five probes red.
Reproduce: `python3 -B harness_c1_final.py <counter> <outdir>` (harness copied here as
`MutationTesterGates/harness_c1_final.py`; receipts in `MutationTesterGates/receipts/c1final/`).

|Mutant|One-line change (file: `doc_quote_truth.py`)|Observed|Killed by|
|---|---|---|---|
|M1|`"met": len(findings) == 0 and append_only,` → `"met": len(findings) == 0,`|`met` unchanged on every tree; `append_only=false` still printed|**survived**|
|M2|`"met": …,` → `"met": append_only,`|`met=true` with 8 findings; rc 0|ST 29/53; BEFORE 0/8; HEAD 0/8; all 5 probes green|
|M3|`frags = […] if ELIDE_RE.search(span) else [span]` → `frags = [span]`|elided spans become literal-string tests|ST 51/53|
|M4|`all(f in body …)` → `all(f.lower() in body.lower() …)`|case-variant span accepted|P_CASE rc 0 (ST still 53/53)|
|M5|`if any(fnmatch…ARTIFACT_GLOBS):` → `if False and any(…)`|`w1-results.json` becomes a receipt|ST 52/53|
|M6|`all(f in body …)` → `any(f in body …)`|one fragment suffices|ST 52/53|
|M7|`findings.append({"id": "T4", …` → `(lambda *a, **k: None)({"id": "T4", …`|no T4 finding|ST 50/53|
|M8|`if span in defects and any(span in c["spans"] for c in validated):` → `if validated:`|any validated correction exempts every defective span|ST 52/53|
|M9|`return 0 if res["met"] else 1` → `return 0`|rc 0 with findings|ST 27/53; BEFORE 0/8; HEAD 0/8; all 5 probes green|

**Tally (final build): mutants=9 killed=8 survived=1.**

### 2.1 The survivor, stated as a finding

**M1 — dropping the append-only conjunct is unobservable, because the conjunct is dead code.**
`evaluate()` appends an `A1` finding for every row present at `--base` and gone at the measured revision,
so `findings` can never be empty when `append_only` is false; `len(findings) == 0` already implies
`append_only`. Proof (not inference): a fixture with a claim row deleted between `--base` and `HEAD`
(`SCORECARD.md` row `| A | \`zz=9\` |`) was scored by the pristine counter and by M1; the full JSON is
identical, including `"append_only": false` and the `A1` finding —
`receipts/c1final/eq_v2_M1.json`, and the v0 counter shows the same identity in
`receipts/c1v0/eq_v0_M1.json`:

```
v0_M1 identical= True pristine= {'rc': 1, 'append_only': False, 'met': False,
                                 'findings': [('A1', 'SCORECARD.md')], 'rows': 3}
                        mutant   = {'rc': 1, 'append_only': False, 'met': False,
                                    'findings': [('A1', 'SCORECARD.md')], 'rows': 3}
```

Verdict: **unreachable redundancy**, not a live defect — no case can kill it and no tree distinguishes it.
The risk it hides is real though: the append-only guarantee is carried entirely by `A1` emission, so a
future edit that stops emitting `A1` for some deletion class would leave `met=true` and no test would
notice. Recommended repair (terms-neutral): either delete `and append_only` (it is unobservable) or add a
case where `append_only` is false with `A1` suppressed by construction — e.g. a base row whose text is
rewritten *and* which is then quoted by a validated correction, which the current emission order cannot
express. I did not change the contract.

## 3. C1 mutant ledger — hardened build `63af0ede` (the build amendment 5 D5 cites)

`--selftest` **aborted before executing any case** in this build, so `ST` contributed nothing:

```
RuntimeError: git -C …/green_commit_citation -c user.name=t … commit -q --no-verify -m fixture 2 failed:
```

Cause (reproduced, `receipts/c1v2/proof_stdout.txt`, `proof_rc.txt`): `selftest()` calls `_fixture(...)` for
`green_commit_citation` **twice** in a row (lines 557–560 and 561–568); the first call's two payloads are
byte-identical, so the second `git commit` has nothing to commit and returns 1 with **empty stderr**:

```
second_commit_rc=1
stdout='On branch main\nnothing to commit, working tree clean\n'
stderr=''
```

`_fixture` raises on any nonzero `git` return, so the whole selftest dies. Consequence measured on that
build with the surviving detectors (BEFORE/HEAD/probes):

|Mutant|Observed|Verdict|
|---|---|---|
|M1 append-only conjunct|no detector moves|survived (same redundancy as §2.1)|
|M3 every span contiguous|no detector moves (only the dead selftest tested `ok_elision`)|**survived**|
|M6 one fragment suffices|no detector moves|**survived**|
|M7 T4 check skipped|no detector moves (the corpus carries no correction rows)|**survived**|
|M8b presence-exempts (`if correction_lines(rows):`)|no detector moves|**survived**|
|M2 `met` ignores findings|BEFORE/HEAD `met=true` with 8 findings; probes green|killed|
|M4 case-insensitive spans|P_CASE green|killed|
|M5 `*-results.json` as receipt|BEFORE changed; P_ARTIFACT green|killed|
|M9 exit 0 always|BEFORE/HEAD rc 0; probes green|killed|

**Tally (63af0ede): mutants=9 killed=4 survived=5** — every survivor traceable to the aborted selftest.
The final build `33162b61` repairs this (ST 53/53) and kills M3, M5, M6, M7, M8 again; M1 remains the only
survivor of the chain, for the reason in §2.1.

## 4. C1 instrument findings (observed, not inferred)

**F1 — the base finding count under amendments 3+4+5 is 8, not the 7 asserted by D4.**
Measured on the final build at the frozen base:

```
C1v2 revision=a0491fcd rows=16 receipt_files=7753 spans=25 exempted=0 corrections=0 findings=8 met=false
  T1 SCORECARD.md:4892 files=18 mismatches=0 append_only=true met=true missing_frozen=0
  T1 SCORECARD.md:4892 mismatches=3 classes=E3 append_only=false missing_frozen=1
  T1 SCORECARD.md:4893 population=18 bound=18 mismatches=0 met=true missing_frozen=0
  T1 SCORECARD.md:4893 receipt: source=committed declared_valid=true
  T1 SCORECARD.md:4904 mismatches=0 met=true missing_frozen=0
  T1 corpus/QUALITY.md:1499 files=15 append_only=false met=false
  T1 corpus/lessons/round-75.md:56 cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea
  T1 corpus/lessons/round-75.md:82 files=15 append_only=false met=false
```

The eighth finding is new relative to the A3+A4 universe (that build printed 7 on the same base). Its only
carriers at `a0491fcd` are files that amendment 5 D1 excludes — `git grep` at the base revision:

```
a0491fcd:.ufo/waves/round-75/w1-results.json              (dispatcher artifact)
a0491fcd:.ufo/waves/round-75/contract.md                  (prose)
a0491fcd:.ufo/waves/round-75/w1/ConnectorOverlap.md       (seat tree)
a0491fcd:.ufo/waves/round-75/w1/ScoutSources/…            (seat tree)
a0491fcd:.ufo/waves/round-75/w1/ScribeKnowledge.md        (seat tree)
a0491fcd:.ufo/waves/round-75/w1/SentinelScope/receipts.txt (seat tree)
```

So the 8 is the D1-faithful count and D4's "stays findings=7" is the stale number (D1's exclusion necessarily
removes receipts, and a removal can only raise the base count). A build that printed 7 on the final receipts
universe would be ignoring D1 for that digest. Nothing here asks me to change the target; the L1 must
restate the base count or name the receipt that is supposed to keep the digest contiguous.

**F2 — the final selftest does not test case sensitivity.** M4 leaves `ST` at 53/53 green on the final build;
only my external `P_CASE` probe kills it. Cheapest fix: a case whose span is an upper-cased receipt token
with a non-matching receipt, expecting `T1`.

**F3 — the laundering this seat measured on the pre-amendment build is real and was adopted.** On
`c9311780` (v0) and on the A3+A4 builds, `--revision b758cb04 --base a0491fcd` printed
`findings=0 met=true` with `corrections=0`, because `.ufo/waves/round-76/controls/*.txt` are receipt-directory
files whose diagnostic lines end with the absent spans:

```
grep -rlF 'files=18 mismatches=0 append_only=true met=true' .ufo/waves/round-76/
  .ufo/waves/round-76/controls/base-c1-quote-truth.txt
  .ufo/waves/round-76/controls/ctl-{deletion,do-nothing,junk-correction,launder}.txt
```

Amendment 4 (name exclusion) and amendment 5 (D1 seat tree, D2 diagnostic lines) close it in the final build:
at `b758cb04` the final counter prints `findings=8 met=false` with `corrections=0`, i.e. still red without the
repair, as D4 requires.

## 5. C2 mutant ledger — final tool `0762452f`, matrix `b8333969`

Baseline of these bytes (matrix run on the same files):

```
PRISTINE tool_selftest 59/59 passed (rc 0)
         cases=69 decided=66 correct=66 wrong=0 undecided=3 constants_failed=4/4 met=true (rc 0)
```

All four committed constants fail at least one case (A16: `const_noop.py` and `const_report_all.py` fail all
66 decided cases; `const_always_clean.py` fails 50; `const_empty_list.py` fails 45).

<!-- C2_TABLE -->

## 6. Tallies

<!-- TALLIES -->

## 7. Reproduction

```sh
S=/fast/scratch/hyaku/kake-r76/MutationTesterGates
git clone --shared /home/vgpnk/Projects/shokunin/kake-shokunin "$S/clone"
# C1 (final build)
python3 -B "$S/harness_c1_final.py" \
  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-76/w1/ExecQuoteCounter/doc_quote_truth.py \
  "$S/out_final2"
# C2
python3 -B "$S/harness_c2.py"
```

Harnesses, mutant files and every JSON/text receipt cited above are copied into this wave directory
(`mutants/`, `receipts/`); the scratch directory was removed after the copy.
