# ExecLedgerMutation — round-63 C1 ledger single-field mutation attack

Seat scope (dispatch item, `.ufo/waves/round-63/w1-dispatch.json` → `ExecLedgerMutation`):
apply five single-field mutations to a copy of `.ufo/waves/round-63/quote-class/quote-classes.json`
in a scratch repo and run `c63_calibration.py` on each mutated tree; each must fail with
`met=false` and the expected component at 0.

**Verdict: 4 of the 5 assigned mutations are killed with the expected component at 0.
M5 (`locatedRawLines` → `6150-6156`) SURVIVES (`met=true`, exit 0) — the counter never
reads that field. The survival does not trip the contract's C1 kill rule as written (it is
not a marker-only green), but it fails this item's literal acceptance criterion, so it is
reported as a measured deviation, not a pass.**

Two further measured findings are reported in §4–§5:
(a) a **self-consistent fabricated-body tree** (both retained blobs replaced by fabricated
bytes, both ledger digests updated coherently) is **green under both C1 and C2** — the
counter compares the ledger's digests against the *revision's* blobs and never against the
contract-frozen ledger digest `5f48e26…`; and (b) the C2 counter's `s432_real` fixture is
resolved from the **worktree**, not the measured revision (corroborating sibling
`ExecToolSelftest.md` Finding A).

No tools installed. No fleet-root, `.ufo/state`, `scripts/`, or template file was written.
The only file written is this report.

---

## 1. Vehicles and their provenance

### 1.1 The frozen artifacts used

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:.ufo/waves/round-63/c63_calibration.py | sha256sum
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  -
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:.ufo/waves/round-63/quote-class/quote-classes.json | sha256sum
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  -
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:.ufo/waves/round-63/quote-class/S432.txt | sha256sum
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  -
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:.ufo/waves/round-61/sources/S432.html | sha256sum
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  -
```

All four equal the contract-frozen digests
(`.ufo/waves/round-63/contract.md:20-27`, `:35-39`).

The counter used for every run below was a **byte-identical copy** of the frozen counter:

```
$ cp /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_calibration.py \
     /fast/scratch/hyaku/kake-r63/ExecLedgerMutation/c63_calibration.py
$ sha256sum /fast/scratch/hyaku/kake-r63/ExecLedgerMutation/c63_calibration.py
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  /fast/scratch/hyaku/kake-r63/ExecLedgerMutation/c63_calibration.py
```

### 1.2 Scratch repo construction (host guard satisfied)

Driver script: `/fast/scratch/hyaku/kake-r63/ExecLedgerMutation/final_pass.py`
(all file bytes transferred in binary mode; every path verified byte-identical to the
fleet's committed blob before the first mutation commit).

```
$ git -C /fast/scratch/hyaku/kake-r63/ExecLedgerMutation/final rev-parse --show-toplevel
/fast/scratch/hyaku/kake-r63/ExecLedgerMutation/final
baseline commit=9e173a1d033a56f522fc2811a54e5ab0c5b74379
byte-fidelity of the scratch tree vs the fleet's committed blobs:
  MATCH corpus/lessons/round-61-verifier-spotcheck.md b4faa46bb618399b02d8dc52e14a7f785bb87c17697737f5a92c92621203d013
  MATCH corpus/knowledge/response-header-expectations.md a4f0f228ca145fccee03e70e994e2670c7275dafebf0df752dffdf32888531cb
  MATCH corpus/QUALITY.md cec4e6b7b578151baa6cc65caea3b50fc3fe820ad0704e38fae312322eaa1e0f
  MATCH corpus/lessons/round-63.md 1e0e444546c0d41623d06f5dda2f7736560dc1d560f02b00f7c224169dda0f81
  MATCH corpus/SOURCES.md 63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2
  MATCH .ufo/waves/round-61/sources/S432.html 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b
  MATCH .ufo/waves/round-63/quote-class/S432.txt 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
  MATCH .ufo/waves/round-63/quote-class/quote-classes.json 5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d
```

The scratch repo was created with `git init -q` at
`/fast/scratch/hyaku/kake-r63/ExecLedgerMutation/final`, `git rev-parse --show-toplevel`
asserted equal to that directory **before the first commit**, and the throwaway identity is
scoped to the scratch repo only (`user.name kake-r63 fixture`,
`user.email fixture@kake-r63.local`). The fleet repo was never mutated, cloned, or
committed to.

### 1.3 Baseline on the scratch tree (green, as required)

```
$ python3 -B c63_calibration.py --root /fast/scratch/hyaku/kake-r63/ExecLedgerMutation/final --revision 9e173a1d033a56f522fc2811a54e5ab0c5b74379
revision=9e173a1d033a56f522fc2811a54e5ab0c5b74379 disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

Identical in shape to the committed after-receipt
`.ufo/waves/round-63/controls/after-c1.txt` (which prints the same field values at
`05b0d7f4…`, exit 0).

For reference, the counter's own read of the fleet repo (read-only) reproduces both ends of
the contract predicate:

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

---

## 2. The five assigned mutations

Each mutation rewrites exactly **one** field of the `S432` row, then commits; the pristine
ledger bytes are restored from the baseline commit before the next mutation. The mutated
ledger blob digest is shown so each run is independently identifiable.

| # | Field mutated | Mutation | Mutated-commit sha | Mutated ledger sha256 | Counter verdict | Expected component at 0 | Result |
|---|---|---|---|---|---|---|---|
| M1 | `textSha256` | last hex char `9`→`a` | `7b82ae96e0d2bd7a8d70d2db9889df3cde3a6da9` | `2118d1f3df2b38b047bd8e58d002b5c13e2b3453c463ab7eaa2f25caa9aed6ba` | `met=false` exit 1 | `blobs_match=0` | **KILLED** |
| M2 | `rawSha256` | last hex char `b`→`c` | `27dc694ec8b8e7b99b0c485ec1d511f1e2d97689` | `0c45fdf50da4f34ac645064d23bda02f1c8dd8b71288f41901161380b1c4e54b` | `met=false` exit 1 | `blobs_match=0` | **KILLED** |
| M3 | `matchClass` | `collapsed-only`→`raw-substring` | `cef4cc2f88fb59978ea1faed5adb99a590150461` | `98de5bf4ef087f8de640417357b176b5c68691f94a9889550ba58b414c454228` | `met=false` exit 1 | `class_match=0` | **KILLED** |
| M4 | `quote` | U+2019 `’`→U+0027 `'` | `8891d417d88f8525090367ca92d824e187384a6f` | `803b80c486bec45339d267971d2bc89f1095015c0f7d88c79e14769796852224` | `met=false` exit 1 | `blobs_match=0` | **KILLED** |
| M5 | `locatedRawLines` | `"6150-6154"`→`"6150-6156"` | `3d1b5b977508f8a5d1dc96f5401fd247e9dedf07` | `57e681d7d176c5d6628fff5c2d5eb19acb24b67b05db8603727efd6f3ad01f39` | **`met=true` exit 0** | **none — all components 1** | **SURVIVED** |

### 2.1 M1 — wrong `textSha256` (KILLED)

```
--- M1_wrong_textSha256 (textSha256 last hex char 9 -> a) ---
commit=7b82ae96e0d2bd7a8d70d2db9889df3cde3a6da9
ledger_sha256=2118d1f3df2b38b047bd8e58d002b5c13e2b3453c463ab7eaa2f25caa9aed6ba
revision=7b82ae96e0d2bd7a8d70d2db9889df3cde3a6da9 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

Killed at `blobs_match=0` — the ledger's `textSha256` no longer equals
`sha256(S432.txt)`, so `c63_calibration.py:135` fails and the class is never even derived
(`derived=unevaluable`). `quote_correction=0` at `:145`; `unresolved=1` at `:165`.

### 2.2 M2 — wrong `rawSha256` (KILLED)

```
--- M2_wrong_rawSha256 (rawSha256 last hex char b -> c) ---
commit=27dc694ec8b8e7b99b0c485ec1d511f1e2d97689
ledger_sha256=0c45fdf50da4f34ac645064d23bda02f1c8dd8b71288f41901161380b1c4e54b
revision=27dc694ec8b8e7b99b0c485ec1d511f1e2d97689 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

Killed at `blobs_match=0` via `c63_calibration.py:134`.

### 2.3 M3 — `matchClass` swapped to `raw-substring` (KILLED)

```
--- M3_matchClass_swapped_to_raw-substring (matchClass collapsed-only -> raw-substring) ---
commit=cef4cc2f88fb59978ea1faed5adb99a590150461
ledger_sha256=98de5bf4ef087f8de640417357b176b5c68691f94a9889550ba58b414c454228
revision=cef4cc2f88fb59978ea1faed5adb99a590150461 disagreements=1 quote_correction=0 blobs_match=1 derived=collapsed-only class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

Killed at `class_match=0`: the digests still match (`blobs_match=1`), the class is still
re-derived inline as `collapsed-only` from the two blobs, and the ledger's *recorded*
class disagrees with the derivation (`c63_calibration.py:142-143`). This is the strongest
of the five kills: the class is not asserted, it is derived and compared.

### 2.4 M4 — quote with a straight apostrophe (KILLED)

```
--- M4_quote_straight_apostrophe (quote U+2019 -> U+0027) ---
commit=8891d417d88f8525090367ca92d824e187384a6f
ledger_sha256=803b80c486bec45339d267971d2bc89f1095015c0f7d88c79e14769796852224
revision=8891d417d88f8525090367ca92d824e187384a6f disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

Killed at `blobs_match=0` via `c63_calibration.py:136`
(`row.get("quote") == FROZEN_QUOTE`): the ledger's quote must be byte-identical to the
counter's `FROZEN_QUOTE` (`c63_calibration.py:51-55`), whose apostrophe is U+2019.

### 2.5 M5 — `locatedRawLines` changed to `6150-6156` (SURVIVED)

```
--- M5_locatedRawLines_6150-6156 (locatedRawLines "6150-6154" -> "6150-6156") ---
commit=3d1b5b977508f8a5d1dc96f5401fd247e9dedf07
ledger_sha256=57e681d7d176c5d6628fff5c2d5eb19acb24b67b05db8603727efd6f3ad01f39
revision=3d1b5b977508f8a5d1dc96f5401fd247e9dedf07 disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

**Every component stays at 1 and `met=true`.** Root cause, read directly from the frozen
counter — the ledger row is read at only five places, and `locatedRawLines` is not one of
them:

```
$ grep -n 'row.get\|ledger.get\|QUOTE_REL =\|TEXT_REL =\|LEDGER_REL =' .ufo/waves/round-63/c63_calibration.py
41:QUOTE_REL = ".ufo/waves/round-61/sources/S432.html"
42:TEXT_REL = ".ufo/waves/round-63/quote-class/S432.txt"
43:LEDGER_REL = ".ufo/waves/round-63/quote-class/quote-classes.json"
131:        row = ledger.get("S432")
134:                row.get("rawSha256") == hashlib.sha256(raw_blob).hexdigest()
135:                and row.get("textSha256") == hashlib.sha256(text_blob).hexdigest()
136:                and row.get("quote") == FROZEN_QUOTE
143:                                  == row.get("matchClass"))
```

```
$ grep -c 'locatedRawLines' .ufo/waves/round-63/c63_calibration.py
0
```

The counter also hardcodes the two blob paths (`QUOTE_REL`/`TEXT_REL`, `:41-42`) and never
consults the ledger's own `textPath`/`rawPath`.

**Scope of the M5 survival.** It is a *coverage* gap on a field the counter's frozen
semantics do not mention — the contract's C1 component list requires the ledger to record
the span and the shas to re-derive and the class to re-derive inline
(`.ufo/waves/round-63/contract.md:29-40`); it does not require `locatedRawLines` to be
re-derived. The same field is ungated for sibling `MutLedger` (M4, "locatedRawLines field
removed entirely") and `RevengerC62Defect` (J, forged to `"1-1"`), so this is a
**reproduced, independent** finding, not a new one.

**M5 is also not, on these bytes, a semantic falsification.** The sentence-bearing raw span
is verified from committed bytes — collapsing raw lines `6150-6156` with the committed
recipe still yields the frozen quote verbatim:

```
$ (python3 - <<'PY'
import importlib.util, subprocess
spec=importlib.util.spec_from_file_location("et",
  "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/extract_text.py")
et=importlib.util.module_from_spec(spec); spec.loader.exec_module(et)
R="/fast/scratch/hyaku/kake-r63/ExecLedgerMutation/final"
raw=subprocess.run(["git","-C",R,"show","9e173a1d033a56f522fc2811a54e5ab0c5b74379:.ufo/waves/round-61/sources/S432.html"],
                   stdout=subprocess.PIPE,check=True).stdout
lines=raw.decode().split("\n")
Q=("The `X-Content-Type-Options` response header can be used to require checking of a "
   "response\u2019s `Content-Type` header against the destination of a request.")
for a,b in ((6150,6154),(6150,6156),(6149,6156)):
    flat=et.extract(("\n".join(lines[a-1:b])+"\n").encode())
    print(f"raw lines {a}-{b}: collapsed contains FROZEN_QUOTE = {Q in flat}")
PY
)
raw lines 6150-6154: collapsed contains FROZEN_QUOTE = True
raw lines 6150-6156: collapsed contains FROZEN_QUOTE = True
raw lines 6149-6156: collapsed contains FROZEN_QUOTE = True
```

So `"6150-6156"` is a truthful superset range for the sentence, and the round-62 held
citation in the corpus already uses that range
(`corpus/knowledge/response-header-expectations.md:220`,
`corpus/lessons/round-62-verifier-spotcheck.md:39-40`,
`corpus/lessons/round-62.md:15`) while the round-63 block and the ledger use `6150–6154`
(`corpus/knowledge/response-header-expectations.md:226`,
`.ufo/waves/round-63/quote-class/quote-classes.json:14`). The counter's silence is thus
benign on these bytes — but the mutation does leave the ledger's own `note` (which still
says "raw lines 6150-6154") inconsistent with the mutated `locatedRawLines` field, and
nothing detects that.

---

## 3. Supplementary single-field probes (same vehicle)

Run with the same baseline and the same byte-identical counter. All are single-field
mutations of the `S432` row unless stated.

| # | Mutation | Counter result | Verdict |
|---|---|---|---|
| P1 | `textPath` → `.ufo/waves/round-63/quote-class/WRONG.txt` | `blobs_match=1 derived=collapsed-only class_match=1 … met=true` exit 0 | survived |
| P2 | `rawPath` → `.ufo/waves/round-61/sources/WRONG.html` | `blobs_match=1 … met=true` exit 0 | survived |
| P3 | `note` rewritten to a false claim ("raw lines 1-2 carry it") | `blobs_match=1 … met=true` exit 0 | survived |
| P4 | extra row `{id:"S999", …}` appended to `classes` | `blobs_match=1 … met=true` exit 0 | survived |
| P5 | `id` renamed `S432`→`S432x` | `quote_correction=0 blobs_match=0 derived=unevaluable … met=false` exit 1 | killed |
| P6 | `matchClass` → `absent` | `blobs_match=1 derived=collapsed-only class_match=0 … met=false` exit 1 | killed |
| P7 | top-level `schema` → `bogus-v9` | `blobs_match=1 … met=true` exit 0 | survived |
| P8 | `locatedRawLines` → `"1-1"` | `blobs_match=1 … met=true` exit 0 | survived |
| P9 | `locatedRawLines` → `""` | `blobs_match=1 … met=true` exit 0 | survived |
| D1 | duplicate `S432` rows, corrupt first / pristine last | `blobs_match=1 … met=true` exit 0 | survived |
| D2 | duplicate `S432` rows, pristine first / corrupt last | `blobs_match=0 derived=unevaluable … met=false` exit 1 | killed |

Exact D-series output (dict materialisation order matters):

```
--- D1_duplicate_S432_corrupt_first_good_last ---
revision=a1efb0aff3c1f4be3a16998a85736855a1e88104 disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
--- D2_duplicate_S432_good_first_corrupt_last ---
revision=b6208e51b8a756faed389f13fb3c26d6115e0c5c disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

D1 vs D2 confirms the materialisation is `{row["id"]: row for row in classes}`
(`c63_calibration.py:117-119`) — last duplicate wins. P4/P7/D1 are the same class of
finding as sibling `MutLedger` M5 (extra id row survived).

### 3.1 Blob-level probes (self-consistent re-derivation)

These mutate the *blobs* and keep the ledger coherent, to test whether the counter's
"re-derive from the retained blobs" is anchored to anything.

| # | Tree mutation | Counter result | Verdict |
|---|---|---|---|
| B1 | `S432.txt` appended with a line; ledger `textSha256` **not** updated | `blobs_match=0 … met=false` exit 1 | killed |
| A1 | `S432.txt` with the quote removed; ledger `textSha256` **updated** | `blobs_match=1 derived=absent class_match=0 … met=false` exit 1 | killed |
| S1 | `S432.html` with the quote appended; ledger `rawSha256` **updated** and `matchClass`→`raw-substring` | `blobs_match=1 derived=raw-substring class_match=0 … met=false` exit 1 | killed |
| F1 | `S432.txt` replaced by a one-line fabricated rendering containing the quote; ledger `textSha256` **updated** | `blobs_match=1 derived=collapsed-only class_match=1 … met=true` exit 0 | **survived** |
| G1/H1 | **both** blobs replaced by fabricated bytes (raw = unrelated HTML, text = one-line quote); both ledger digests **updated** | `blobs_match=1 derived=collapsed-only class_match=1 … met=true` exit 0 | **survived** |

```
--- S1_selfconsistent_raw_substring_forgery ---
commit=e526e669cec19be2590739d2eded2143fbd44cb4
revision=e526e669cec19be2590739d2eded2143fbd44cb4 disagreements=1 quote_correction=0 blobs_match=1 derived=raw-substring class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
--- H1_fabricated_bodies_C1_and_C2 ---
commit=9597fa0cef8589dff0b6acc43164aabe0fe8a9e9
ledger_sha256=918e0b59e75031205049d39e5e8403a228a5bbdc4c0829aba750d97d8e0f1c61  (contract frozen 5f48e26be279…  match=False)
  C1: revision=9597fa0cef8589dff0b6acc43164aabe0fe8a9e9 disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true exit=0
  C2: revision=9597fa0cef8589dff0b6acc43164aabe0fe8a9e9 present=1 selftest=4/4 frozen_cases=ok met=true exit=0
```

**This is the material finding.** The counter's re-derivation is *internally* sound
(S1/A1 are killed) but it is anchored to the **revision's own blobs**, not to the
contract-frozen ledger digest `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d`
or to the frozen blob digests `63b0a018…`/`8b90d096…`:

```
$ grep -c '5f48e26b\|63b0a018\|8b90d096' .ufo/waves/round-63/c63_calibration.py
0
```

A tree whose retained "source body" is 45 bytes of unrelated HTML plus a one-line text file
containing the quote is green under **both** C1 and C2. The ledger digest in that tree is
`918e0b59…`, i.e. **not** the contract-frozen `5f48e26…`, and the counter does not notice.
This reproduces, independently of sibling `RevengerC62Defect` §5 ("the decisive miss:
self-consistent fabrication", variant C), the same shape; the sibling's fabricated bundle was
built from scratch, mine was built by mutating the real tree.

---

## 4. Marker-only fixture control re-run (independent of the committed receipt)

The committed receipt `.ufo/waves/round-63/controls/control-marker-fixture.txt` claims the
round-62 marker-only fixture is `met=true` under the old `c62` counter and `met=false`
under `c63`. Re-run here from the **committed** fixture corpus
(`.ufo/waves/round-62/controls/false-green-fixture/corpus/`), copied byte-exact into a
fresh scratch repo at `/fast/scratch/hyaku/kake-r63/ExecLedgerMutation/marker-fix`
(`git init -q`, top-level asserted before the first commit):

```
$ git -C /fast/scratch/hyaku/kake-r63/ExecLedgerMutation/marker-fix rev-parse --show-toplevel
/fast/scratch/hyaku/kake-r63/ExecLedgerMutation/marker-fix
fixture rev=90b3b621fba0f691d2e3f757c578e5f645a8c4e5

$ python3 -B .ufo/waves/round-63/c63_calibration.py --root <marker-fix> --revision 90b3b621fba0f691d2e3f757c578e5f645a8c4e5
revision=90b3b621fba0f691d2e3f757c578e5f645a8c4e5 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1

$ python3 -B .ufo/waves/round-62/c62_calibration.py --root <marker-fix> --revision 90b3b621fba0f691d2e3f757c578e5f645a8c4e5
revision=90b3b621fba0f691d2e3f757c578e5f645a8c4e5 disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
exit=0
```

The round-62 defect family is dead under `c63` on the committed fixture: the old counter
greens, the repaired counter reds with `quote_correction=0 blobs_match=0`. **The
marker-only green is not reproduced.** (The fixture rev differs from the receipt's
`7833be88…` because the corpus was re-committed here in scratch; the counter output matches
the receipt's field-for-field.)

---

## 5. C2 counter: the `s432_real` fixture is resolved from the worktree, not the revision

The C2 counter extracts the tool from the revision but runs it with `cwd=root`
(`c63_quote_tool.py:80-83`), and the frozen tool binds its fixtures to `Path.cwd()`
(`scripts/quote_class.py:24-25,30`). Measured:

**A5 — the same revision flips verdict on an uncommitted worktree edit.**

```
$ git -C /fast/scratch/hyaku/kake-r63/ExecLedgerMutation/c2split rev-parse --show-toplevel
/fast/scratch/hyaku/kake-r63/ExecLedgerMutation/c2split
rev=8b0debce4a464fc5072aef441a9a57f5fb2cb5b4
--- C2 at baseline (worktree == revision) ---
revision=8b0debce4a464fc5072aef441a9a57f5fb2cb5b4 present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
--- now tamper the WORKTREE blobs (not committed) so s432_real case would fail if read from worktree ---
 M .ufo/waves/round-63/quote-class/S432.txt
revision=8b0debce4a464fc5072aef441a9a57f5fb2cb5b4 present=1 selftest=failed met=false
exit=1
```

**A6 — a green at a revision whose committed blobs are fabricated, with a good worktree.**

```
$ git -C /fast/scratch/hyaku/kake-r63/ExecLedgerMutation/c2split2 rev-parse --show-toplevel
/fast/scratch/hyaku/kake-r63/ExecLedgerMutation/c2split2
worktree status:
M  .ufo/waves/round-61/sources/S432.html
M  .ufo/waves/round-63/quote-class/S432.txt
--- C2 at the FABRICATED revision (b3977d761f5028f829774a5c69b0437467ffba82) while the worktree holds the good blobs ---
revision=b3977d761f5028f829774a5c69b0437467ffba82 present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

This corroborates sibling `ExecToolSelftest.md` Finding A / `ExecC2CounterAttack.md` §"the
counter resolves the tool from the revision but runs it with cwd=root". It is outside my
C1 ledger-mutation scope; I record it because it was measured while running the mutation
trees through both counters, and because the C2 leg of the H1 fabricated-body probe depends
on it.

For the record, the C2 leg is **not** affected in the actual measurement: the six input
paths are byte-identical between the measured commit and the worktree —

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ sha256sum .ufo/waves/round-61/sources/S432.html .ufo/waves/round-63/quote-class/S432.txt .ufo/waves/round-63/quote-class/quote-classes.json
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .ufo/waves/round-63/quote-class/S432.txt
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

---

## 6. Answer to the item's question, and what the main agent should weigh

**Item answer.** Of the five assigned mutations: **M1, M2, M3, M4 fail as required**
(`met=false`, exit 1, with `blobs_match=0` / `class_match=0` / `blobs_match=0` /
`blobs_match=0` respectively at the expected component). **M5 does not fail**: `met=true`,
exit 0, every component at 1. The literal acceptance criterion ("each must fail with
met=false and the expected component at 0") is therefore **not met for M5**.

**Why it does not by itself trip the C1 kill rule.** The contract's kill rule
(`.ufo/waves/round-63/contract.md:41-46`) reads: *"if the after receipt does not print
`met=true`, or either control prints `met=true`, or any wave attack reproduces a
marker-only green, C1 is `unprovable` (honest stop), no calibration credit."* M5 is not a
marker-only green: the tree keeps the genuine retained blobs, the digests still re-derive,
and the class is still genuinely derived as `collapsed-only`. §4 shows the marker-only green
is in fact dead. The after-receipt also still prints `met=true` at the measured commit
(§1.3), and both controls red. So **on the contract's literal wording the M5 survival is a
coverage finding, not a kill-rule trip** — but it is a deviation from this seat's item and
from the ledger's role as a *located* proposition record, so the L1 should decide whether
the frozen C1 predicate is meant to cover `locatedRawLines`.

**The finding the L1 should weigh more.** §3.1 / H1: a tree whose two retained blobs are
fabricated and whose ledger digests are updated coherently is green under **both** C1 and
C2, with a ledger digest (`918e0b59…`) that differs from the contract-frozen
`5f48e26…`. The counter anchors re-derivation to the *revision's* blobs but to no constant
at all (`grep -c '5f48e26b\|63b0a018\|8b90d096' .ufo/waves/round-63/c63_calibration.py` → 0).
Under the predicate-literal reading (the contract names one marker-only fixture, and `c63`
is red on it) the control passes; under the semantic reading ("no genuine committed source
body survives, yet the counter is green") the false-green class has moved rather than
disappeared — as sibling `RevengerC62Defect` §5 argues. Whether that trips the kill rule is
the L1's call, not mine; I am reporting the measurement with an independent reproduction.

**Files changed by this seat:** this report only.
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ExecLedgerMutation.md`

**Fleet repo untouched** (verified after all runs):

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && git log --oneline -1 && git status --porcelain
76812537 round-63: wave settlement; honest-stop verdicts; QUALITY addendum; SCORECARD/LOG round-63
?? .ufo/waves/round-63/w1.ready
?? .ufo/waves/round-63/w1.ready.dispatched
?? .ufo/waves/round-63/w1/
```

(`w1/` is this wave's report directory — every seat's report, including this one — and the
two `.ready*` files were present before this seat ran. No tracked file was modified; no
commit, push, or git/jj mutation was performed in the fleet repo, `.ufo/state`, `scripts/`,
or `templates/`.)

**Note on HEAD movement during this seat.** The fleet HEAD was `15eb965c` when this seat
started and had advanced to the wave-settlement commit `76812537` (touched `LOG.md`,
`SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-63.md`) by the wave owner while
this seat was running — not by this seat, which performs no git mutation. All five frozen
artifacts are byte-identical at the new HEAD, and both counters still read green there, so
none of the measurements above is affected:

```
$ git show 76812537:.ufo/waves/round-63/c63_calibration.py | sha256sum
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  -
$ git show 76812537:.ufo/waves/round-63/quote-class/quote-classes.json | sha256sum
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  -
$ git show 76812537:scripts/quote_class.py | sha256sum
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  -
$ git show 76812537:.ufo/waves/round-61/sources/S432.html | sha256sum
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  -
$ git show 76812537:.ufo/waves/round-63/quote-class/S432.txt | sha256sum
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  -

$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 76812537c633b6e0776745e789125d51a1315b3c
revision=76812537c633b6e0776745e789125d51a1315b3c disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 76812537c633b6e0776745e789125d51a1315b3c
revision=76812537c633b6e0776745e789125d51a1315b3c present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

**Scratch cleanup.** All scratch repos under
`/fast/scratch/hyaku/kake-r63/ExecLedgerMutation/` (`repo/`, `final/`, `marker-fix/`,
`c2split/`, `c2split2/`) are deleted after the runs above; every commit hash quoted in this
report is recorded verbatim so the measurements are reproducible without the scratch trees.
