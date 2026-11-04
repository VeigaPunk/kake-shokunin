# MutationTesterGates — round 76, wave w1 (kake lane)

Seat: mutation tester for the two new gates (C1 quote-truth counter, C2 hreflang audit). Leaf seat: no
subagent dispatch, no network, no commit, lane checkout read-only. Every executed byte lived in
`/fast/scratch/hyaku/kake-r76/MutationTesterGates` (`git clone --shared` of the lane at
`b758cb04`); mutants, harnesses and receipts are copied under `MutationTesterGates/` here. No tool was
installed or upgraded for this seat.

## 0. Bytes scored

|Role|File|sha256|bytes|Measured|
|---|---|---|---|---|
|C1 counter, **final scored**|`w1/ExecQuoteCounter/doc_quote_truth.py`|`e7f86d3aa0554f61330179f803fcc7624504b2ee63ea2d3e1a9ee5e3427f59ae`|49077|final bytes of this wave|
|C1 counter, v0 (frozen with contract)|`.ufo/waves/round-76/c76_quote_truth.py`|`c931178067bfb53f3d54e59ae10b24fd62550f80403f34244ac10a652da068e3`|18130|earlier in this wave|
|C1 counter, abort build (A5 D5 cites it)|`w1/ExecQuoteCounter/doc_quote_truth.py`|`63af0ede46919b213c6dad414b26b9eef5cd23078d741afe0bdb940f44a966c8`|—|earlier in this wave|
|C2 tool, **final scored**|`w1/ExecAuditTool/hreflang_audit.py`|`0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac`|59734|final bytes of this wave|
|C2 matrix, **final scored**|`w1/ExecAuditMatrix/c76_hreflang_matrix.py`|`4958ede07559d15cfb95af57b99dcaee98883420a071847f78f02db248ad7756`|—|final bytes of this wave|
|C2 cases|`w1/ExecAuditMatrix/cases/`|71 files, 69 decided, 2 undecided|—|final bytes of this wave|

The C1 file was revised by its owner four times during this wave (distinct shas: `63af0ede`, `33162b61`,
`302bcb9b`, `e7f86d3a`). The ledger below is measured on `e7f86d3a`; the same 9 mutations were also run on
`63af0ede` (reported in §3, because amendment 5 D5 cites its defect) and on `33162b61`/`302bcb9b` with
identical verdicts except where stated. Re-running the harness against newer bytes takes ~60 s.

## 1. Detectors (bounded, local, re-runnable)

|Detector|Invocation|Pristine expectation|
|---|---|---|
|`ST`|`python3 -B <counter> --selftest --work <dir>`|exit 0 and every case executed (A5 D5)|
|`BEFORE`|`python3 -B <counter> --root <clone> --revision a0491fcd --base a0491fcd --rounds 75,76`|`findings=7 met=false`, exit 1 (A7 F2)|
|`HEAD`|same, `--revision b758cb04`|red until the repair rows land (A5 D4)|
|`P_ARTIFACT`|fixture whose absent span lives only in `round-76/w1/w1-results.json`|red|
|`P_CASE`|fixture: span `MET=TRUE`, receipt `met=true`|red|
|`P_SEATREE`|fixture: span only in `round-75/w1/SomeSeat/receipts/notes.txt`, measuring round 75|red (75 is the newest measured round there, A7 F1)|
|`P_DIAG`|fixture: span only on a line `  T1 SCORECARD.md:1 <span>`|red (A5 D2 strips it)|
|`P_DATAEXT`|fixture: span only in `round-74/notes.txt`, outside every receipt directory|red (A5 D1)|

Each probe fixture is its own `git init` repo under the scratch work dir. A mutant is **killed** when any
detector leaves the pristine shape (selftest rc, before/head exit + finding count, or any probe verdict);
`survived` means every detector was unchanged.

Final-build baseline (`e7f86d3a`):

```
ST      selftest: 63/63 passed (exit 0)
BEFORE  C1v2 revision=a0491fcd rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false   (rc 1)
HEAD    C1v2 revision=b758cb04 rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false   (rc 1)
probes  P_ARTIFACT rc=1  P_CASE rc=1  P_SEATREE rc=1  P_DIAG rc=1  P_DATAEXT rc=1
```

`HEAD` red with `corrections=0` is the behaviour A4/A5 D4 demand: committing this round's controls no longer
turns the counter green.

## 2. C1 mutant ledger — final build `e7f86d3a` (authoritative)

One-line changes, each applied alone to a fresh copy of the pristine bytes
(`mutants/c1final/`, receipt `receipts/c1final/<id>.json`).

|#|Mutant|Exact one-line change|Observed|Verdict|Killed by|
|---|---|---|---|---|---|
|M1|drop the append-only conjunct|`"met": len(findings) == 0 and append_only,` → `"met": len(findings) == 0,`|`met` identical on every tree; `append_only=false` still printed|**survived**|— (see §2.1)|
|M2|make `met` ignore findings|`…` → `"met": append_only,`|`met=true` with 7 findings, rc 0|killed|`ST 34/63`; `BEFORE 0/7`; `HEAD 0/7`; all 5 probes rc 0|
|M3|every span contiguous|`frags = […split(span)…] if ELIDE_RE.search(span) else [span]` → `frags = [span]`|elided spans tested as one literal|killed|`ST 61/63`|
|M4|case-insensitive spans|`all(f in body for f in frags)` → `all(f.lower() in body.lower() for f in frags)`|`MET=TRUE` accepted against `met=true`|killed|`P_CASE rc 0` (**ST still 63/63** — see F2)|
|M5|`*-results.json` is a receipt|`if any(fnmatch…ARTIFACT_GLOBS):` → `if False and any(…)`|`receipt_files 7923→7933`; dispatcher dump admitted|killed|`ST 62/63`|
|M6|elision needs only one fragment|`all(f in body …)` → `any(f in body …)`|one surviving fragment passes|killed|`ST 62/63`|
|M7|skip the T4 check|`findings.append({"id": "T4", …` → `(lambda *a, **k: None)({"id": "T4", …`|no T4 emitted|killed|`ST 59/63`|
|M8|correction presence exempts|`if span in defects and any(span in c["spans"] for c in validated):` → `if validated:`|any validated correction exempts every defective span|killed|`ST 62/63`|
|M9|exit 0 unconditionally|`return 0 if res["met"] else 1` → `return 0`|rc 0 with 7 findings|killed|`ST 32/63`; `BEFORE 0/7`; `HEAD 0/7`; all 5 probes rc 0|

**Tally, C1 final: `mutants=9 killed=8 survived=1`.**

### 2.1 The one survivor, with its reason

**M1 — dropping `and append_only` is an *unreachable redundancy*, not a live defect.**
`evaluate()` appends an `A1` finding for every row present at `--base` and gone at the measured revision
(and skips the span loop for it), so `findings` can never be empty when `append_only` is false;
`len(findings) == 0` already implies `append_only`. Proven, not inferred: a fixture deleting one claim row
between `--base` and `HEAD` was scored by pristine and M1; the full JSON is identical, `append_only:false`
and the `A1` finding included — `receipts/c1v0/eq_v0_M1.json` and `receipts/c1v0/eq_v2_M1.json`:

```
v0_M1 identical= True pristine= {'rc': 1, 'append_only': False, 'met': False,
                                 'findings': [('A1', 'SCORECARD.md')], 'rows': 3}
                        mutant   = {'rc': 1, 'append_only': False, 'met': False,
                                    'findings': [('A1', 'SCORECARD.md')], 'rows': 3}
v2_M1 identical= True  (same shape on doc_quote_truth.py)
```

No tree can kill it: `append_only` false with empty findings is unreachable while `A1` is emitted there. The
residual risk is that the append-only guarantee is carried *only* by that emission — a future edit that stops
emitting `A1` for some deletion class would silently leave `met=true`, and no case in the delivered selftest
(63 cases) would notice. Terms-neutral options: delete the conjunct (it is unobservable), or add a case that
asserts `met == (findings == []) and append_only` on a shape where `A1` is suppressed by construction.

## 3. C1 mutant ledger — abort build `63af0ede` (the build A5 D5 cites)

On those bytes `--selftest` **aborted before executing any case**, so `ST` contributed nothing:

```
RuntimeError: git -C …/green_commit_citation -c user.name=t … commit -q --no-verify -m fixture 2 failed:
```

Cause, reproduced (`receipts/c1v2/proof_stdout.txt`, `proof_rc.txt`): the selftest calls `_fixture(...)` for
`green_commit_citation` twice in a row with a byte-identical first payload (lines 557–560 then 561–568); the
second `git commit` has nothing to stage and returns 1 with **empty stderr**, and `_fixture` raises on any
nonzero git exit:

```
second_commit_rc=1
stdout='On branch main\nnothing to commit, working tree clean\n'
stderr=''
```

With `ST` dead, only `BEFORE`/`HEAD`/probes could kill anything:

|Mutant|Observed on `63af0ede`|Verdict|
|---|---|---|
|M1 append-only conjunct|no detector moves|survived (same redundancy as §2.1)|
|M3 every span contiguous|no detector moves — only the dead selftest tested `ok_elision`|**survived**|
|M6 one fragment suffices|no detector moves|**survived**|
|M7 T4 skipped|no detector moves — the measured corpus carries no correction rows at base|**survived**|
|M8b presence-exempts (`if correction_lines(rows):`)|no detector moves|**survived**|
|M2 `met` ignores findings|`BEFORE`/`HEAD` `met=true` with 8 findings; probes green|killed|
|M4 case-insensitive spans|`P_CASE` green|killed|
|M5 `*-results.json` as receipt|`BEFORE` finding count changed; `P_ARTIFACT` green|killed|
|M9 exit 0 always|`BEFORE`/`HEAD` rc 0; probes green|killed|

**Tally, `63af0ede`: `mutants=9 killed=4 survived=5`** — every survivor is traceable to the aborted
selftest. The final build repeals this (`ST 63/63`, and M3/M5/M6/M7/M8 are killed again). The v0 counter
`c9311780` behaved like the final build on the mutations it could run: `ST 13/13`, `mutants=9 killed=8
survived=1` (same M1), receipts in `receipts/c1v0/`.

## 4. C1 measurements worth the L1's attention

**F1 — the base count is a function of the seat-tree rule, and amendment 7 F2 now matches the build.**
Measured base counts on the same frozen base `a0491fcd`: `eae3ce48 → findings=9`, `33162b61 → findings=8`,
`302bcb9b → findings=7`, `e7f86d3a → findings=7`. The two swings are exactly amendment 7's subject: the
64-char digest `cbe684a1…` at `corpus/lessons/round-75.md:56` and `source=uncommitted` at line 103. At the
base revision `git grep -l` finds the digest in 12 files, none of them under a receipt directory of the
A5 D1 sense; the only carriers that can legitimately count are the closed round-75 seat-tree data files.
I verified the final rule at import level against the frozen base (read-only, in scratch):

```
is_receipt('.ufo/waves/round-75/w1/ScoutSources/fetch-intoto.txt', [75,76])  -> True
is_receipt('.ufo/waves/round-75/w1/ScoutSources/verify-output.txt',[75,76])  -> True
is_receipt('.ufo/waves/round-75/w1/SentinelScope/receipts.txt',   [75,76])  -> True
is_receipt('.ufo/waves/round-75/w1-results.json',                 [75,76])  -> False
is_receipt('.ufo/waves/round-75/w1/ScribeKnowledge.md',           [75,76])  -> False
```

i.e. the newest measured round's seat tree is excluded, a closed round's seat-tree *data* files count, its
prose and scripts do not — F1 as written. No defect; recorded because earlier in the wave the count moved
and a reader of the intermediate receipts would otherwise think the counter or the amendment was wrong.

**F2 — the delivered selftest does not test case sensitivity.** M4 leaves `ST` at **63/63 green** on the
final build; only my external `P_CASE` probe kills it. One case would close it: a span that differs from a
pristine receipt token only by ASCII case, expecting `T1`.

**F3 — the laundering this seat first measured is closed in the final build.** On the pre-amendment builds
(`c9311780` and the A3+A4 ones) `--revision b758cb04 --base a0491fcd` printed `findings=0 met=true` with
`corrections=0`, because `.ufo/waves/round-76/controls/*.txt` are receipt-directory files whose diagnostic
lines end with the absent spans:

```
grep -rlF 'files=18 mismatches=0 append_only=true met=true' .ufo/waves/round-76/
  .ufo/waves/round-76/controls/base-c1-quote-truth.txt
  .ufo/waves/round-76/controls/ctl-{deletion,do-nothing,junk-correction,launder}.txt
```

Adopted as amendments 4 and 5; the final build prints `findings=7 met=false` at `b758cb04` (same seven as
base), so the do-nothing tree is red again and the after-state cannot be reached without repair rows.

## 5. C2 mutant ledger — tool `0762452f`, matrix `4958ede0`

Baseline of those bytes (same harness invocation, matrix run against the tool):

```
tool --selftest           59/59 passed (rc 0)
matrix                     cases=71 decided=69 correct=69 wrong=0 undecided=2  constants_failed=4/4  met=true (rc 0)
constants                  const_noop.py          failed 69/69  passes_all=no
                           const_report_all.py    failed 69/69  passes_all=no
                           const_always_clean.py  failed 53/69  passes_all=no
                           const_empty_list.py    failed 47/69  passes_all=no
undecided residue          undecided-svg-template-crossing, undecided-unreadable-undecodable (A8 G3, excluded)
```

Each mutation was applied alone to a fresh copy of the tool (`mutants/c2/`); the matrix was then run over
the frozen cases with that copy as `--tool`, and every failure below is the matrix's own verdict line
(`receipts/c2/c2_<id>.json` carries the full wrong-case list).

|#|Mutant|Exact one-line change (`hreflang_audit.py`)|Killing case(s)|Matrix|Tool selftest|
|---|---|---|---|---|---|
|M1|skip the self-reference rule|`if not any(normalize_url(alt["href"]) == page["url_norm"] for alt in tagged_abs):` → prefixed `False and …`|`self-missing-pair` (exit1 `[self_missing]` → exit0 `[]`), `multi-self-missing-and-nonreciprocal`|2 wrong|57/59|
|M2|accept relative hrefs|`if not absolute_with_host(alt["href"]):` → `if False and …`|`relative-href-path`, `-fragment`, `-mailto`, `-protocol-relative`|4 wrong|55/59|
|M3|ignore x-default multiplicity|`if len(xdefault) > 1:` → `if len(xdefault) > 10 ** 9:`|`multiple-xdefault-pair` (expects four `hreflang_multiple_xdefault`, got none)|1 wrong|57/59|
|M4|every external target reciprocal|external `_add(...)` neutralised with `(lambda *a, **k: None)(`|`external-target-single`, `-mixed`, `-trailing-slash` (info finding dropped)|3 wrong|57/59|
|M5|skip the canonical rule|`if normalize_url(canonical["href"]) != page["url_norm"]:` → `if False and …`|`canonical-not-self`, `canonical-first-wins`, `canonical-with-hreflang`|3 wrong|58/59|
|M6|accept `_` in tags|`lowered = ascii_lower(tag)` → `ascii_lower(tag).replace("_", "-")`|`invalid-tag-underscore` (+ `structure-noscript`, `multi-missing-value-and-invalid-tag`, `input-policy-and-fault`, …)|7 wrong|56/59|
|M7|return no policy findings|`alts = page["alternates"]` → `alts = page["alternates"][:0]`|43 cases, first `canonical-not-self`|43 wrong|36/59|
|M8|exit 0 always|`return run_audit(…)` → `return run_audit(…) and EXIT_CLEAN`|50 cases; shape check fires too (`report exit=1 but process exit=0`), first `canonical-not-self`|50 wrong|27/59|
|M9|granularity collapsed (A2 probe)|`_sorted_findings`: `return sorted(findings, …)` → dedupe by `(id,page)` before sorting|`duplicate-pair-two-pairs` (2→1), `multiple-xdefault-pair` (4→2)|2 wrong|55/59|

**Tally, C2: `mutants=9 killed=9 survived=0`** (M9 is an extra mutant beyond the eight required, added because
A2 granulation only bites under a multiset comparison; the current matrix is multiset-aware, so it dies).

Two matrix-level probes, for completeness:

* `c2_bare_json.json` — a tool printing `{"findings": []}` and exiting 0 (no `version`/`pages`/`counts`): the
  matrix fails it on **69/69** cases (A16 shape check), never scoring it as `{exit:0, ids:[]}`.
* The four committed constants are the contract's cheap controls and each fails at least one decided case
  (§5 baseline), so a constant that passed everything is not present.

## 6. Tally

```
C1 final build e7f86d3a   mutants=9 killed=8 survived=1   (survivor M1: unreachable redundancy, §2.1)
C1 abort build 63af0ede   mutants=9 killed=4 survived=5   (all 5 surviving because the selftest aborted; §3)
C1 v0 build  c9311780     mutants=9 killed=8 survived=1   (same M1)
C2 tool 0762452f / matrix 4958ede0   mutants=9 killed=9 survived=0   constants 4/4 fail >=1 case
combined (final builds)   mutants=18 killed=17 survived=1
```

No surviving mutant is a wildcard: the single survivor is reachable-by-no-input redundancy in the delivered
instrument, with the residual risk named in §2.1. Every other mutation of every assigned behaviour is caught
by the delivered detectors (selftest, before/head state, or a case in the matrix).

## 7. Reproduction and file map

```sh
S=/fast/scratch/hyaku/kake-r76/MutationTesterGates
git clone --shared /home/vgpnk/Projects/shokunin/kake-shokunin "$S/clone"   # tip b758cb04, base a0491fcd
python3 -B "$S/harness_c1_final.py" \
  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-76/w1/ExecQuoteCounter/doc_quote_truth.py \
  "$S/out_final4"                     # ST/BEFORE/HEAD + 5 probes, 9 mutants, ~60 s
python3 -B "$S/harness_c2.py"         # tool selftest + matrix per mutant, ~110 s
python3 -B "$S/equiv_m1.py"           # the M1 equivalence proof
```

`MutationTesterGates/harness/` — `harness_c1_final.py` (amended-contract C1 matrix), `harness_c1.py`
(v0/v1 harness used for the `63af0ede` ledger), `harness_c2.py`, `equiv_m1.py`, `multiset_probe.py`.
`MutationTesterGates/mutants/c1final|c1v0|c1v2|c2/` — the exact mutant files.
`MutationTesterGates/receipts/c1final|c1v0|c1v2|c2/` — every JSON verdict, the before/head transcripts, and
the `git commit` proof for the D5 abort. The scratch tree was removed after the copy.
