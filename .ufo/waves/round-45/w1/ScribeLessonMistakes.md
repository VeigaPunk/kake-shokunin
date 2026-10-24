# ScribeLessonMistakes — round-45 wave 1 (draft lesson content: receipt-trust mistake + Gate skeleton)

Axes: **operability** (the gate's decision procedure) and **freshness** (the provenance of every
cited byte). No round judgment, claim admission, or score is made here; the canonical Rust judge
owns that. Draft only — the L1 lands `corpus/lessons/round-45.md`.

## What I did

1. Re-read the assigned evidence: `.ufo/waves/round-44/w2/ReviewCounterContract.md` (defects
   1a/1b/1c) and the frozen round-45 C1/C2 declarations in `SCORECARD.md`.
2. **Re-derived the three HIGH receipt-trust defects on today's frozen bytes** with a scratch
   probe that loads `.ufo/waves/round-44/c44_audit.py` by path (no copy, no edit) and drives its
   own `semantic_witness` / `expectation_ok` on the row shapes `score()` emits. All three
   reproduce.
3. **Ran an able-to-fail comparison** of the frozen v1 driver and the round-45 v2 driver over the
   three landed invalid fixture classes, entirely in scratch.
4. **Re-derived the C2(c) witness split** from both committed round-44 receipts and found the
   frozen `22/1/4` tuple belongs to the *earlier* 23-witness receipt, not to the receipt the
   frozen sentence names.
5. Opened the primary source for the C1 knowledge entry independently
   (`https://docs.python.org/3/library/subprocess.html`), located the `returncode` passages, and
   opened one non-primary candidate on the same topic.
6. Drafted the `## Mistakes` rows and the `## Gate` table skeleton into
   `.ufo/waves/round-45/drafts/mistakes.md`.
7. Coordinated with `kake-r45.ScribeSourcesGate` (it owns the S133/S134 source decisions and the
   single reject decision for this round; I labeled my row as candidate-only and pointed at its
   draft).

## Named attack — pass/fail

The item names the receipt-trust mistake class and its evidence/defect/fix/able-to-fail skeleton.
The decisive question is whether the frozen v1 driver really does credit receipts it never bound
to its own run, and whether v2 closes it.

| Named attack | Verdict | Decisive fact |
|---|---|---|
| v1 credits an exit-2 (counter-error) receipt as a witness | **FAIL — defect present in the frozen bytes** | probe A: `semantic_witness: True`, `expect witnessed (build 3/3 met): True` |
| v1 credits a `note: "tool absent"` receipt as a witness | **FAIL — defect present** | probe B: `semantic_witness: True`, `expect witnessed (build 3/3 met): True` |
| v1 credits a receipt written outside the run (crash-killed counter, `-9`) | **FAIL — defect present** | probe C: `semantic_witness: True`, `expect witnessed (build 3/3 met): True` |
| the frozen predicates read exit / note / mtime / counter-sha | **FAIL — none of the four is read** | probe D: `expectation_ok mentions exit False`, `… note False`, `… st_mtime False`, `… counterSha False`; same for `semantic_witness`; module mentions `st_mtime False`, `getmtime False`, `time.time() False` |
| v1 accepts the three invalid fixture classes end-to-end | **FAIL — 3/3 accepted** | scratch run: each class `ok=True`, exit 0, the row's `exit` recorded as 2 / 1 / -9 |
| v2 refuses all three invalid fixture classes | **PASS — 0/3 accepted, each named** | scratch run: `ok=False`, exit 1, row `error=counter_error` / `error=tool_absent` / `error=counter_error` |
| v2 still certifies an honest receipt (junk control) | **PASS** | honest fixture under the real frozen counter: `witnessed=1/1 notMet=1 build_met=0/0 ok=True`, exit 0 |
| the C1 count `22/1/4` re-derives from the receipt the frozen sentence names | **FAIL — it does not** | `after-final/after-v5.json` → `{"witnessed":27,"split":{"class_only":26,"mixed":1,"met":0,"other":0}}`; `22/1/4` comes from the earlier `after-v5.json` (`witnessed:23`) |
| the frozen matrix stages exist / have been run | **UNRUN — placeholder** | `python3 -B .ufo/waves/round-45/c45_matrix.py --stage before\|after` not run by this seat; no `verification/matrix/` receipt existed at this seat's read |
| the honest 27-control cohort under v2 (`honest_witnessed=27`, `honest_build_met=3`) | **UNRUN — not claimed** | `ExecRegressionHonest` reported the driver absent at its run; the committed receipt `.ufo/waves/round-45/verification/honest-regression/after-v5-v2.json` did not exist at this seat's read |

**Lesson-side answer:** the mistake class named by the item is real, present in the frozen bytes,
re-derivable today, and closed by the landed v2 driver on all three invalid classes. The
able-to-fail line in the drafted row therefore names the frozen counting command and marks the
matrix receipt as a placeholder, with the scratch before/after table as the interim evidence.

## Decisive commands and verbatim output

All commands were run from the lane root `/home/vgpnk/Projects/shokunin/kake-shokunin` (scratch
files under `/fast/scratch/hyaku/kake-r45/ScribeLessonMistakes/`). No counter run, no audit
scoring run over the 27-control cohort, no matrix stage, no build, no test, no formatter, no
git/jj write, no commit, no push, no install.

### 1. Frozen hashes re-measured

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && sha256sum .ufo/waves/round-44/c44_audit.py .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-45/c45_audit.py .ufo/waves/round-45/c45_matrix.py .ufo/waves/round-44/w2/ReviewCounterContract.md
```

```text
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
5a342e29c7e872d992cfedc26de849c010d197bb82162e007a61a55d915c7051  .ufo/waves/round-45/c45_audit.py
cdddee5a62b0f03bb39a1801ea9fce039e8af8b405add620cdb156143a4694cd  .ufo/waves/round-45/c45_matrix.py
e85060b72c3c0495affe4a842d7e420b8d7f60ed27537c1b9d79b196b68933a4  .ufo/waves/round-44/w2/ReviewCounterContract.md
```

### 2. The three HIGH defects, re-derived on today's frozen bytes

```sh
cd /fast/scratch/hyaku/kake-r45/ScribeLessonMistakes && python3 -B probe_receipt_trust.py
```

Exit 0. Verbatim output:

```text
FROZEN_PATH /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/c44_audit.py
A_MODULE /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/c44_audit.py
== A. counter error (exit 2) after a class divergence ==
semantic_witness: True
expect witnessed (build 3/3 met): True
== B. 'tool absent' receipt (exit 1, note='tool absent') ==
semantic_witness: True
expect witnessed (build 3/3 met): True
== C. crash-killed counter (-9) with a planted receipt ==
semantic_witness: True
expect witnessed (build 3/3 met): True
== D. predicate source reads ==
expectation_ok mentions exit         False
semantic_witness mentions exit         False
expectation_ok mentions note         False
semantic_witness mentions note         False
expectation_ok mentions mtime        False
semantic_witness mentions mtime        False
expectation_ok mentions st_mtime     False
semantic_witness mentions st_mtime     False
expectation_ok mentions counterSha   False
semantic_witness mentions counterSha   False
expectation_ok mentions toolSha      False
semantic_witness mentions toolSha      False
expectation_ok mentions receipt      False
semantic_witness mentions receipt      False
module mentions st_mtime       False
module mentions getmtime       False
module mentions time.time()    False
module mentions counterSha256  True
module mentions toolSha256     True
```

Reading: the frozen predicates read neither `exit`, nor `note`, nor any timestamp, nor any
counter-byte pin; the module mentions `counterSha256`/`toolSha256` only as summary fields it
writes, never as a gate it checks.

### 3. Able-to-fail: v1 vs v2 over the three invalid fixture classes (scratch only)

```sh
cd /fast/scratch/hyaku/kake-r45/ScribeLessonMistakes && bash able_to_fail.sh
```

Each leg: `--controls <fixture>/controls.tsv --counter <fixture>/fake_counter.py --classes v5
--expect witnessed --build-rev 020bc457 --build-runs 3 --workers 1`, output into scratch; the v1
stale-planted leg is pre-seeded with the fixture's committed receipts, the v2 legs start from an
empty cohort (v2 refuses a non-empty output directory, `c45_audit.py:200-203`).

```text
CLASS=counter-error DRIVER=v1 EXIT=0
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=15363b71eaa0
  ctl1                 G5         met=False caught=G5,G7
  witnessed-by-class ctl1 caughtBy=G5,G7
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
  summary ok=True witnessed=1 build_met=None
  row name=ctl1 exit=2 met=False caughtBy=['G5', 'G7'] error=None

CLASS=counter-error DRIVER=v2 EXIT=1
AUDIT kake-r45 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=0/0 notMet=0 build_met=0/3 ok=False counter=15363b71eaa0
  ctl1                 G5         met=False caught=G5,G7                  counter_error
  build#1 met=True equal=21/21 stale_receipt
  build#2 met=True equal=21/21 stale_receipt
  build#3 met=True equal=21/21 stale_receipt
  summary ok=False witnessed=0 build_met=None
  row name=ctl1 exit=2 met=False caughtBy=['G5', 'G7'] error=counter_error

CLASS=tool-absent DRIVER=v1 EXIT=0
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=c697435a11e7
  ctl1                 G5         met=False caught=A,B,C,D,E,F,G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,T1,T2,T3,T4,T5
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
  summary ok=True witnessed=1 build_met=None
  row name=ctl1 exit=1 met=False caughtBy=['A','B','C','D','E','F','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','T1','T2','T3','T4','T5'] error=None

CLASS=tool-absent DRIVER=v2 EXIT=1
AUDIT kake-r45 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=0/0 notMet=0 build_met=0/3 ok=False counter=c697435a11e7
  ctl1                 G5         met=False caught=A,B,C,D,E,F,G1,...,T5 tool_absent
  build#1 met=True equal=21/21 stale_receipt
  build#2 met=True equal=21/21 stale_receipt
  build#3 met=True equal=21/21 stale_receipt
  summary ok=False witnessed=0 build_met=None
  row name=ctl1 exit=1 met=False caughtBy=['A','B','C','D','E','F','G1',…,'T5'] error=tool_absent

CLASS=stale-planted DRIVER=v1 EXIT=0
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=18e3bcfda602
  ctl1                 G5         met=False caught=G2,G4,G9
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
  summary ok=True witnessed=1 build_met=None
  row name=ctl1 exit=-9 met=False caughtBy=['G2', 'G4', 'G9'] error=None

CLASS=stale-planted DRIVER=v2 EXIT=1
AUDIT kake-r45 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=0/0 notMet=0 build_met=0/3 ok=False counter=18e3bcfda602
  ctl1                 G5         met=None  caught=-                      counter_error
  build#1 met=None equal=None counter_error
  build#2 met=None equal=None counter_error
  build#3 met=None equal=None counter_error
  summary ok=False witnessed=0 build_met=None
  row name=ctl1 exit=-9 met=None caughtBy=[] error=counter_error
```

(The `caught=A,B,C,D,E,F,G1,…,T5` and `caught=G1,…,T5` spans above are elided for width; the
unabridged stdout is in the scratch directory `able-to-fail/*.log.stdout`.)

**Reading:** v1 certifies all three invalid classes (`ok=True`, exit 0) while recording the very
exit codes that should have refused credit (2, 1, -9). v2 refuses all three (`ok=False`, exit 1)
and names a class per rejected row. Note the shape of the v2 rejections: the *control* rows give
`counter_error` (counter-error fixture), `tool_absent` (tool-absent fixture) and `counter_error`
again (stale-planted fixture, exit `-9` ∉ `{0,1}`), while the third distinct name
`stale_receipt` arrives on the fixture **build** rows, whose receipts carry the real counter's
`counterSha256` while the invoked counter is the fixture's fake one. The mtime-window branch of the
gate is therefore not exercised by the landed stale-planted fixture — only by the driver's own
selftest assertion (`c45_audit.py:162`). This is recorded in the draft as a residual risk and as a
finding for the L1; it does not change the three-class verdict.

### 4. Honest control under v2 (junk control)

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && timeout 280 python3 -B .ufo/waves/round-45/c45_audit.py --root . --controls .ufo/waves/round-45/fixtures/honest/controls.tsv --counter .ufo/waves/round-44/c44_count_v5.py --classes v5 --expect not-met --workers 1 --out /fast/scratch/hyaku/kake-r45/ScribeLessonMistakes/honest-v2/summary.json
```

```text
AUDIT kake-r45 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=0/0 ok=True counter=5cedaa3b9f91
  ctl1                 G5         met=False caught=G5,G7
  witnessed-by-class ctl1 caughtBy=G5,G7
EXIT=0
```

### 5. C2(c) witness split re-derived from both committed receipts

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && for f in .ufo/waves/round-44/verification/claim/after-v5.json .ufo/waves/round-44/verification/claim/after-final/after-v5.json; do jq -c '{witnessed:.witnessed, split:(.rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length, mixed: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length, met: map(select(.met==true))|length, other: map(select(.met==false and (.classCaught|length)==0))|length})}' "$f"; done
```

```text
{"witnessed":23,"split":{"class_only":22,"mixed":1,"met":4,"other":0}}
{"witnessed":27,"split":{"class_only":26,"mixed":1,"met":0,"other":0}}
```

Receipt digests:

```text
2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902  .ufo/waves/round-44/verification/claim/after-v5.json
9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1  .ufo/waves/round-44/verification/claim/after-final/after-v5.json
```

Reading: the frozen C2(c) tuple `22 class-only + 1 mixed + 4 met` belongs to the **earlier**
23-witness receipt; the receipt the frozen sentence names (`after-final/after-v5.json`, witnessed 27)
carries `26/1/0`. Independent wave-1 agreement: `ExecWitnessSplit.md:7`, `ScoutRoutedLedger.md:6`,
`CriticC2Scope.md:9`.

### 6. Primary source for S133, opened independently

```sh
cd /fast/scratch/hyaku/kake-r45/ScribeLessonMistakes && curl -sS -D pyhdr.txt -o subprocess.html -w "HTTP=%{http_code} bytes=%{size_download}\n" https://docs.python.org/3/library/subprocess.html && sha256sum subprocess.html subprocess2.html && date -u +"FETCHED_AT=%Y-%m-%dT%H:%M:%SZ"
```

```text
HTTP=200 bytes=208624
HTTP/2 200
last-modified: Sat, 24 Oct 2026 00:16:18 GMT
etag: "6adbf8d2-32ef0"
content-length: 208624
eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd  subprocess.html
eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd  subprocess2.html
FETCHED_AT=2026-10-24T03:15:19Z
```

Two independent fetches are byte-equal. Located quotes (markup stripped), verified as substrings
of the retained bytes:

```text
§Using the subprocess Module → CompletedProcess.returncode, paragraph 1 (17 words):
"Exit status of the child process. Typically, an exit status of 0 indicates that it ran successfully."
§Popen Objects → Popen.returncode, paragraph 3 (15 words):
"A negative value -N indicates that the child was terminated by signal N (POSIX only)."
```

This byte-identity also matches `kake-r45.ScribeSourcesGate`'s independent fetch of the same URL
(sha256 `eceda6f6…e5bdf0dd`, 208,624 bytes), confirmed over IRC.

### 7. Non-primary candidate opened by this seat (candidate only — no decision)

```sh
cd /fast/scratch/hyaku/kake-r45/ScribeLessonMistakes && curl -sS --compressed -o ans-5631624.json "https://api.stackexchange.com/2.3/questions/5631624/answers?site=stackoverflow&filter=withbody&order=desc&sort=votes"
```

```text
ANSWER_ID 5631819 score 363 accepted True
CREATION 1302593363 UPDATED 1785246737
LINK https://stackoverflow.com/a/5631819
BODY: Popen.communicate will set the returncode attribute when it's done(*). …
  The child return code, set by poll() and wait() (and indirectly by communicate()).
  A None value indicates that the process hasn't terminated yet.
  A negative value -N indicates that the child was terminated by signal N (Unix only).
```

A plain HTML GET of `stackoverflow.com` returns **HTTP 403** to this host (both for the question
page and for the answer page); the Stack Exchange API returns HTTP 200. This candidate restates
the same documentation passage S133 carries (with the older "Unix only" wording), so it adds no
authority; `kake-r45.ScribeSourcesGate` carries the round's single reject decision (S134, its own
candidate) and my row is labeled **candidate only, no decision** in the drafted Gate table.

### 8. SOURCES.md census (for the L1's row ids)

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md; awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print "malformed="n+0}' corpus/SOURCES.md; awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | tail -3
```

```text
132
malformed=0
S130
S131
S132
```

132 rows, 0 malformed, last id S132 — S133 and S134 are the next free ids.

### 9. Driver v2's gate, read at the cited lines

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && grep -n "def receipt_validity\|def row_valid\|def valid_rows\|def not_met_rows\|def build_met\|MTIME_EPS_NS\|run-manifest\|output directory must be empty" .ufo/waves/round-45/c45_audit.py
```

```text
15:MTIME_EPS_NS = 1_000_000_000
68:def receipt_validity(receipt, exit_code, mtime_bounds, counter_sha):
96:def row_valid(row):
100:def valid_rows(rows):
104:def not_met_rows(rows):
108:def build_met(build, build_runs):
203:        ap.error("output directory must be empty: %s" % outdir)
227:        with open(os.path.join(outdir, "run-manifest.json"), "x") as fh:
243:            rec, code, (mtime_ns, started_ns - MTIME_EPS_NS, finish_ns + MTIME_EPS_NS), counter_sha)
273:            rec, code, (mtime_ns, started_ns - MTIME_EPS_NS, finish_ns + MTIME_EPS_NS), counter_sha)
```

And the shipped selftest (the C2(a) leg's own instrument):

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B .ufo/waves/round-45/c45_audit.py --selftest; echo "EXIT=$?"
```

```text
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, and build-count gates
EXIT=0
```

## Findings for the L1 (beyond the drafted rows)

1. **The C2(c) tuple does not belong to the receipt the frozen sentence names.** `22/1/4` is the
   earlier 23-witness receipt's split; the named final 27-witness receipt carries `26/1/0`
   (§5 above). Three wave-1 seats agree. The frozen declaration is the authority — this is
   reported, not resolved here.
2. **The landed `stale-planted` fixture does not exercise the mtime-window branch of v2's gate.**
   The matrix plants the pre-existing receipts only in the *before* stage
   (`.ufo/waves/round-45/c45_matrix.py:235`), and v2 refuses a non-empty output directory
   (`c45_audit.py:200-203`), so under v2 the stale-planted class is rejected as `counter_error`
   (exit `-9`), and the third distinct rejection name `stale_receipt` arrives on the fixture
   *build* rows via the counter-sha mismatch. The mtime branch is exercised only by the driver's
   selftest assertion (`c45_audit.py:162`). Rejecting the stale-planted case therefore does not by
   itself demonstrate the run-window or sha binding doing the claimed work
   (`CriticC1Predicate.md:38-40` reached the same conclusion from the other side).
3. **The Stack Exchange API response is not byte-reproducible.** Three successive fetches of the
   same answer endpoint gave three different file digests, because the response embeds a live
   `quota_remaining` counter (290, 289, 288). The quoted `body` is byte-stable
   (`sha256 51b11fc5f8de927fd96cfa59761a7adc…`). `kake-r45.ScribeSourcesGate`'s recorded digest
   `702954fd…716ffcd1` is exactly my bytes with `quota_remaining` patched to 295 — verified:
   patching my file to 295 reproduces the sibling digest exactly. [INFERENCE] Any Gate row or
   SOURCES row that cites a whole-file digest of a Stack Exchange API response should either
   retain the file and cite the digest of the retained bytes, or cite the stable `body` digest, or
   pin the query and note the counter field; a re-fetcher will not reproduce the digest.
   The primary source is unaffected: two independent fetches of the Python docs page are
   byte-equal.
4. **`corpus/lessons/round-45.md` already exists** with the `## Gate` and `## Mistakes` section
   headings and placeholder text only (11 lines). The drafted rows above are ready to be landed
   into those two sections; no numbering conflict exists yet (the file has no numbered rows), and
   the lane counter continues at 14.
5. **`ExecRegressionHonest` and `ExecV4ReceiptV6` are blocked at their prerequisites** as of their
   reports: `c45_audit.py` / `c45_count.py` were absent at their first inspection. `c45_audit.py`
   and `c45_count.py` now exist (I measured their digests in §1), so those two items should be
   re-run; I did not run them (not my item).

## Files written by this seat

1. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/drafts/mistakes.md` — the
   drafted `## Mistakes` rows (14, and candidate row 15) and the `## Gate` table skeleton.
2. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w1/ScribeLessonMistakes.md` —
   this report.
3. `/fast/scratch/hyaku/kake-r45/ScribeLessonMistakes/` — scratch only: `subprocess.html`,
   `subprocess2.html`, `pyhdr.txt`, `ans-5631624.json`, `q5631624.json`, `search.json`,
   `so-24139389.json`, `so-rep-1.json`, `so-rep-2.json`, `v-*.json`, `so.html`, `ans.html`,
   `probe_receipt_trust.py`, `able_to_fail.sh`, `honest-v2.stdout`, `honest-v2.stderr`, and the
   `able-to-fail/`, `plantv2/`, `honest-v2/` run directories.

No frozen artifact, corpus file, `SCORECARD.md`, `corpus/SOURCES.md`, receipt, manifest, state
file, fleet file, or sibling-lane file was edited. No `git`/`jj` write, no commit, no push, no
publish, no deploy. No tool was installed or updated (none was needed — `python3` and `curl` were
already present; pacman is paused host-wide, so no pacman transaction was attempted). No subagent
dispatched. No other runtime invoked.

## Bounds and coordination

- Read-only over the fleet repo and sibling lanes; the only lane paths written are my two named
  outputs (`drafts/mistakes.md`, `w1/ScribeLessonMistakes.md`).
- `kake-r45.ScribeSourcesGate` was messaged before drafting and answered: it keeps the single
  reject decision (its S134 candidate) and asked that my row be labeled candidate-only with the
  decision deferred to its draft — done.
- **Unrun by this seat and therefore not claimed:** `c45_matrix.py --stage before|after` (no matrix
  receipt exists); the honest 27-control / 3-build regression under v2; `c45_freshness.py` (the
  frozen C2 counting command, absent at my read); the round-44 27-control v1 audit re-run; any
  `git`/`jj` write.
- No blocker for the draft. The only open dependency for the L1 is the matrix receipt that would
  turn the drafted "able to fail" placeholder into committed evidence.

Report: `.ufo/waves/round-45/w1/ScribeLessonMistakes.md`
