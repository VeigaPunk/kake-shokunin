# MutCounterV6Spec — mutation attack on the counter-v6 spec

Axes: **freshness** (judged) and operability (harm guard).
Named attack: four v6-spec mutants — (1) `PREDICATE_V5` string changed, (2) `classRuns` populated in
v4 mode, (3) runs list mutated in v4 (a G-run inserted), (4) docstring header left claiming the wrong
provenance — each with a named detector (grep / diff-audit / receipt-fields) that must kill it.

**Result: 4/4 mutants KILLED by the named detectors. Two detectors also fire on the PRISTINE shipped
`.ufo/waves/round-45/c45_count.py` (sha256 `ce8bf235…`) — see Finding F1 (surviving mutant of the
spec's own header requirement) and Finding F2 (excerpt fidelity).**

---

## 0. Dependency status — v6 EXISTS (no dependency recorded)

`c45_count.py` did **not** exist when this seat started (00:13Z). It landed at 00:14:27Z from
`ExecCounterV6` while I was building the mutant lab. **Every detector was therefore run against the
REAL shipped bytes**, not against a spec-only reconstruction. Dependency: **none outstanding** for the
four named mutants. The v4 receipt `.ufo/waves/round-45/verification/v6v4/counter-v4.json` does **not**
yet exist (`ExecV4ReceiptV6` item) — but I produced an equivalent real receipt myself in scratch
(§4), so D2/D5/D6 have real runtime evidence independent of that seat.

---

## 1. The four mutant specs and their kill methods

| # | Mutant | One-byte-level change | Detector that must kill it | Kill evidence |
|---|---|---|---|---|
| **M1** | `PREDICATE_V5` string changed → v5 receipts no longer comparable | alter one character of the `PREDICATE_V5` literal (e.g. `class runs` → `class runs.`) | **D1 grep/byte-compare** (constant-level `ast.literal_eval` of `PREDICATE_V5` vs the frozen `PREDICATE`), corroborated by **D6 receipt-fields** (v5-mode receipt predicate ≠ frozen predicate) | KILLED by D1 **and** D6 |
| **M2** | `classRuns` populated in v4 mode | `"classRuns": [key for key, _ in CLASS_MODULES] if a.classes == "v5" else []` → `"classRuns": [key for key, _ in CLASS_MODULES],` | **D2 receipt-fields** (v4 receipt `classRuns` must be `[]`) + **D3 diff-audit** (the changed line is a receipt field, an OTHER class) | KILLED by D2 **and** D3 |
| **M3** | runs list mutated in v4 (a G-run inserted) | `classes = load_classes(root) if a.classes == "v5" else {}` → `classes = load_classes(root)` (so `runs += [(key, None) for key, _ in CLASS_MODULES if key in classes]` inserts G1–G10 in v4 mode) | **D2 receipt-fields** (v4 receipt `runs` must contain **no** `G*` key and must be exactly the eleven v4 runs) + **D3 diff-audit** (the changed line is the class loader line, an OTHER class) | KILLED by D2 **and** D3 |
| **M4** | docstring header left claiming the wrong provenance | `Round-42 version 3 header follows for provenance:` → `Round-43 version 4 header follows for provenance:` (the claim then names a header that does **not** follow) | **D4 docstring-provenance** (the claim must name the header that actually follows) | KILLED by D4 |

### Detector suite (7 detectors, all offline, all cheap)

- **D1 grep/byte-compare** — `ast.literal_eval` of `PREDICATE_V5` in the candidate vs `PREDICATE` in
  the frozen `c44_count_v5.py`. Byte equality, not substring.
- **D2 receipt-fields** — run the counter under test in `--classes v4`, assert `classesMode == "v4"`,
  `classRuns == []`, `runs` keys == exactly `A,B,C,D,E,F,T1,T2,T3,T4,T5`, and **no** key starting `G`.
- **D3 diff-audit** — per-**changed-line** classification of `diff(v5, v6)`. A changed line is allowed
  only if it lies inside the module docstring span or inside a `PREDICATE*` constant span, or matches
  `PREDICATE|predicate`. Everything else (run list, class loader, scoring, CLI, other receipt fields)
  is a FAIL. *(My first D3 was a whole-hunk keyword classifier and produced a **false kill** on the
  legitimate reference — it flagged the `PREDICATE_V4` literal's continuation lines. It was rewritten
  to the line-span classifier above before any verdict was recorded; the false kill is reported here
  rather than hidden.)*
- **D4 docstring-provenance** — the `… header follows for provenance:` claim must name the header that
  actually follows it.
- **D4b docstring self-identification** *(added by this seat)* — a v6 counter must not carry the v5
  module banner (`Round-44 C1 counter, version 5`); it must self-identify as version 6.
- **D5 receipt-predicate v4** — the v4-mode receipt's predicate must name only the eleven v4 runs
  (no `class runs` phrase) and must equal the `PREDICATE_V4` constant.
- **D6 receipt-predicate v5** — the **v5-mode** receipt's predicate must be byte-identical to the
  frozen v5 predicate carried by the committed round-44 receipts.

---

## 2. Harness — how the receipt-level detectors observe a receipt in 15 s instead of a full bwrap run

`harness.py` loads the counter under test as a module and stubs **only** `Sandbox.run` (returning
`("0", b"", 0.01)`). Case generation, run-list construction, the class loader, the timing-ratio
computation and the `met` decision all run unmodified; only the sandboxed tool execution is replaced.
**Fidelity check against the real committed bytes** — the harness run of the *frozen* v5 counter in v4
mode reproduces the committed receipt `.ufo/waves/round-44/verification/freeze/tools/portlen-v1.json`
field-for-field:

```sh
python3 harness.py .ufo/waves/round-44/c44_count_v5.py v4 /tmp/frozen_v4.json .
```

```text
{"label": "", "revision": null, "toolSha256": "914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021", "equalRuns": "11/11", "ratios": {"T1": 1.0, "T2": 1.0, "T3": 1.0, "T4": 1.0, "T5": 1.0}, "met": true, "note": null}

real	0m5.194s
```

```sh
jq '{predicate,classesMode,classRuns,runs_keys:(.runs|keys),equalRuns,met,note}' /tmp/frozen_v4.json
```

```json
{
  "predicate": "met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's",
  "classesMode": "v4",
  "classRuns": [],
  "runs_keys": ["A","B","C","D","E","F","T1","T2","T3","T4","T5"],
  "equalRuns": "11/11",
  "met": true,
  "note": null
}
```

The committed receipt gives the same `predicate` / `classesMode` / `classRuns` / `runs` keys /
`equalRuns` / `met`. The harness is therefore sound for the receipt-*construction* fields the
detectors read. It is **not** a substitute for the real counter run — §4 carries the real run.

---

## 3. Mutants built from the REAL shipped v6, and the decisive detector output

Mutants were derived from the real bytes
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45_count.py`
(sha256 `ce8bf2353d4f008a987f6fb3b6d3677d2dbed98aaae274126c68f0a3cf622556`) into scratch copies.
The lane file was never modified.

### M1 — `PREDICATE_V5` string changed

```sh
cd /fast/scratch/hyaku/kake-r45/MutCounterV6Spec && python3 detectors.py \
  --candidate real_mutants/M1_predicate_v5_changed.py
```

```text
KILL  D1  grep/byte-compare PREDICATE_V5     PREDICATE_V5 != frozen PREDICATE
      frozen: "met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's"
      v6    : "met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs.), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's"
KILL  D6  receipt-predicate v5 comparability v5 receipt predicate != frozen v5 predicate (v5 receipts not comparable)
verdict: KILLED (3/7 detectors failed)
```

**M1 KILLED.** Note D2 and D5 both **survive** M1: the defect is invisible in v4 mode. Only the
byte-compare (D1) and the v5-mode receipt (D6) see it — which is exactly why the v5 receipt's
comparability needs its own detector and cannot be folded into the v4 check.

### M2 — `classRuns` populated in v4 mode

```sh
cd /fast/scratch/hyaku/kake-r45/MutCounterV6Spec && python3 detectors.py \
  --candidate real_mutants/M2_classruns_in_v4.py
```

```text
KILL  D2  receipt-fields classRuns/runs      classRuns=['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10'] (must be [])
KILL  D3  diff-audit changed-line classes    non-allowed changed lines (run list / loader / scoring / CLI / other receipt fields):
      line -1001: "classRuns": [key for key, _ in CLASS_MODULES] if a.classes == "v5" else [],
      line 1002: "classRuns": [key for key, _ in CLASS_MODULES],
verdict: KILLED (3/7 detectors failed)
```

**M2 KILLED** by both the receipt-fields detector and the diff-audit.

### M3 — runs list mutated in v4 (a G-run inserted)

```sh
cd /fast/scratch/hyaku/kake-r45/MutCounterV6Spec && python3 detectors.py \
  --candidate real_mutants/M3_grun_in_v4.py
```

```text
KILL  D2  receipt-fields classRuns/runs      v4 runs contain class keys ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10']; v4 runs keys ['A', 'B', 'C', 'D', 'E', 'F', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'T1', 'T2', 'T3', 'T4', 'T5'] != the eleven v4 runs
KILL  D3  diff-audit changed-line classes    non-allowed changed lines (run list / loader / scoring / CLI / other receipt fields):
      line -1046: classes = load_classes(root) if a.classes == "v5" else {}
      line 1047: classes = load_classes(root)
verdict: KILLED (3/7 detectors failed)
```

**M3 KILLED** by both. This is the most dangerous of the four: M3 makes the v4 receipt *claim* eleven
runs while *executing* twenty-one, which is the exact class of defect that made the v4-mode receipt
predicate lie in round 44.

### M4 — docstring header left claiming the wrong provenance

```sh
cd /fast/scratch/hyaku/kake-r45/MutCounterV6Spec && python3 detectors.py \
  --candidate real_mutants/M4_wrong_provenance.py
```

```text
KILL  D4  docstring provenance claim         header claims 'Round-43 version 4' but the header that follows is 'Round-42 C1 counter, version 3 (pre-freeze redesign of version 2, sha2'
verdict: KILLED (2/7 detectors failed)
```

**M4 KILLED.**

### Control — the legitimate reference must SURVIVE (baseline sanity)

A detector suite that kills everything is worthless. `ref_strict.py` (v5 → v6, predicate split,
provenance label corrected **and** the banner updated to version 6) is the conformant shape:

```text
=== candidate: ref_strict.py ===
PASS  D1  grep/byte-compare PREDICATE_V5     PREDICATE_V5 byte-identical to frozen v5 PREDICATE
PASS  D2  receipt-fields classRuns/runs      v4 receipt classRuns=[] runs=A,B,C,D,E,F,T1,T2,T3,T4,T5
PASS  D3  diff-audit changed-line classes    every changed line is predicate-text or module-docstring
PASS  D4  docstring provenance claim         provenance claim 'Round-42 C1 counter, version 3' matches the following header
PASS  D4b docstring self-identification      module banner self-identifies as version 6 ('Round-45 C1 counter, version 6 (built from the round-44 counter v5, sh')
PASS  D5  receipt-predicate v4 wording       v4 receipt predicate names only the eleven v4 runs
PASS  D6  receipt-predicate v5 comparability v5 receipt predicate byte-identical to the frozen v5 predicate
verdict: SURVIVED (0/7 detectors failed)
```

**PASS against the item's named attack: the suite discriminates. 4/4 mutants killed, 1/1 conformant
reference survives.**

---

## 4. The real v6 against the suite — and two findings that fire on the pristine bytes

### The real counter run (not the harness)

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && time python3 -B .ufo/waves/round-45/c45_count.py \
  --root . --classes v4 --tool-file scripts/sitemap_audit.py \
  --out /fast/scratch/hyaku/kake-r45/MutCounterV6Spec/real_v4_receipt.json
```

```text
{"label": "", "revision": null, "toolSha256": "914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021", "equalRuns": "11/11", "ratios": {"T1": 1.016, "T2": 1.19, "T3": 1.343, "T4": 1.261, "T5": 1.165}, "met": true, "note": null}

real	0m20.389s
```

```sh
jq '{predicate, classesMode, classRuns, runs_keys:(.runs|keys), counterSha256, seed, equalRuns, met}' real_v4_receipt.json
```

```json
{
  "predicate": "met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's",
  "classesMode": "v4",
  "classRuns": [],
  "runs_keys": ["A","B","C","D","E","F","T1","T2","T3","T4","T5"],
  "counterSha256": "ce8bf2353d4f008a987f6fb3b6d3677d2dbed98aaae274126c68f0a3cf622556",
  "seed": 83655839885459,
  "equalRuns": "11/11",
  "met": true
}
```

The v4 receipt is **clean**: the predicate names only the eleven v4 runs (no "class runs" phrase),
`classRuns` is `[]`, and there is no `G*` run key. The C2(b) fix works at runtime.

### Suite against the PRISTINE shipped v6

```sh
cd /fast/scratch/hyaku/kake-r45/MutCounterV6Spec && python3 detectors.py \
  --candidate /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45_count.py
```

```text
=== candidate: /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45_count.py ===
PASS  D1  grep/byte-compare PREDICATE_V5     PREDICATE_V5 byte-identical to frozen v5 PREDICATE
PASS  D2  receipt-fields classRuns/runs      v4 receipt classRuns=[] runs=A,B,C,D,E,F,T1,T2,T3,T4,T5
PASS  D3  diff-audit changed-line classes    every changed line is predicate-text or module-docstring
PASS  D4  docstring provenance claim         provenance claim 'Round-42 version 3' matches the following header
KILL  D4b docstring self-identification      stale module banner: 'Round-44 C1 counter, version 5 (frozen before any control is scored; built from the round-' — a v6 counter must self-identify as version 6
PASS  D5  receipt-predicate v4 wording       v4 receipt predicate names only the eleven v4 runs
PASS  D6  receipt-predicate v5 comparability v5 receipt predicate byte-identical to the frozen v5 predicate
verdict: KILLED (1/7 detectors failed)
```

### FINDING F1 (freshness, HIGH) — the v6 module banner still claims to be the round-44 version-5 counter

`c45_count.py` lines 2–3 read:

```text
"""Round-44 C1 counter, version 5 (frozen before any control is scored; built from the round-43
counter v4, sha256 1c3b9661..., by .ufo/waves/round-44/build_v5.py). Version 5 keeps the v4
```

The file is round-45's counter **v6**; its own `counterSha256` in the receipt is
`ce8bf235…`, not `5cedaa3b…` (the frozen v5). `grep` for the v6 identity finds **nothing**:

```sh
grep -n "version 6\|Round-45\|c45_count" .ufo/waves/round-45/c45_count.py | head
```

```text
(no output)
```

The spec (`ExecCounterV6`) named only the *following-header label* correction
(`Round-43 version 4 header follows` → `Round-42 version 3 header follows`) and said "Nothing else
changes". **The banner was left claiming v5 provenance**, so the file says it *is* the round-44 v5
counter that was "frozen before any control is scored" — which is false for a v6 that is being
introduced in round 45 to score controls that have already been scored. **This is a surviving mutant
of the spec's own header requirement**: D4b kills it.

Smallest correction (docstring-header class only — no receipt, run-list, loader, scoring or CLI
change): replace the banner's first two lines with a v6 self-identification, e.g.

```text
"""Round-45 C1 counter, version 6 (built from the round-44 counter v5, sha256
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc). Version 6 keeps the v5
```

That exact text is the `ref_strict.py` reference, which **survives all seven detectors**. Note the
frozen v5's own banner is retained verbatim below the corrected label, so the provenance chain is
preserved.

**Ownership / status.** `ExecCounterV6` (the owning seat, which wrote `c45_count.py`) confirmed to
this seat that it observed the unchanged Round-44/v5 opening banner and **deliberately left it
unchanged to honour the ticket's exact requested edits** (the predicate behaviour and the
following-header provenance line), and that it is **flagging the banner to L1 as an additional
documentation risk**. This seat did not edit `c45_count.py` and does not dispute that scoping
decision — the ticket text for `ExecCounterV6` named only the following-header label. The finding
here is that the *freshness* axis the item is judged on still has this defect open; the disposition
(banner edit vs. explicit L1 waiver) belongs to the L1. Neither the runtime run in §4 nor any other
verification in this report was performed by `ExecCounterV6`; those are this seat's own runs.

### FINDING F2 (freshness, MEDIUM) — the "Round-42 v3 header" excerpt is not the round-42 v3 header

The label now says the following excerpt *is* the round-42 version-3 header. It is not — it is the v3
header **as inherited with v4 edits**. The load-bearing factual sentence differs from the original:

```sh
python3 d4c_probe.py
```

```text
round-42 c42_count_v3.py equality-run count : Five
round-45 c45_count.py retained excerpt count : Six
excerpt claims the same equality-run count as the original v3 header: NO
original v3 usage names : .ufo/waves/round-42/c42_count_v3.py
retained excerpt names  : .ufo/waves/round-42/c42_count_v3.py
D4c: FAIL — the excerpt is NOT the round-42 v3 header it claims to be
```

The original `.ufo/waves/round-42/c42_count_v3.py:16` says **Five** equality runs; the retained
excerpt in `c45_count.py:27` says **Six** (it adds run F and explicitly distinguishes version 3's five
runs). The label therefore over-claims. This is inherited text, not a v6 hunk, and it is **not** a
reason to rewrite the retained history. Smallest correction (docstring-header class only):
`Round-42 version 3 header, as inherited with v4 edits, follows for provenance:`.
`CriticV6Minimal` reached the same precision limit independently and proposed the same wording; this
seat adds the executable probe. **I did not edit the file** — the fix belongs to the L1 / the owning
seat.

---

## 5. One-liner kill script for a human to re-run against the real v6

`kill_commands.sh` re-implements all six checks as plain shell + `jq` + `python3`, with **no**
dependency on my harness. It exits 1 if any check fails.

```sh
cd /fast/scratch/hyaku/kake-r45/MutCounterV6Spec && sh kill_commands.sh; echo "EXIT=$?"
```

```text
== D1 grep/byte-compare: PREDICATE_V5 == frozen PREDICATE ==
frozen: "met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's"
v6    : "met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's"
D1: PASS

== D2/D5/D6 receipt-fields: run the REAL counter in v4 mode ==
{
  "predicate": "met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's",
  "classesMode": "v4",
  "classRuns": [],
  "runs_keys": ["A","B","C","D","E","F","T1","T2","T3","T4","T5"]
}
D2: PASS
D5: PASS
D6: PASS (v5-mode receipt predicate identical to frozen)

== D3 diff-audit: only predicate-text and docstring hunks ==
D3: PASS

== D4/D4b docstring provenance ==
D4: PASS | claim='Round-42 version 3' following='Round-42 C1 counter, version 3 (pre-freeze redesign of versi'
D4b: FAIL | banner='Round-44 C1 counter, version 5 (frozen before any control is scored; b'

OVERALL: FAIL
EXIT=1
```

`OVERALL: FAIL` is **Finding F1** (the stale v5 banner), not a failure of M1–M4.

---

## 6. Verdict against the item's named attack

| Named attack | Required detector | Verdict on the real bytes |
|---|---|---|
| (1) `PREDICATE_V5` string changed | grep/byte-compare | **PASS** — the real `PREDICATE_V5` is byte-identical to the frozen v5 `PREDICATE`; the mutant is KILLED by D1 and D6 |
| (2) `classRuns` populated in v4 mode | receipt-fields | **PASS** — the real v4 receipt has `classRuns: []`; the mutant is KILLED by D2 and D3 |
| (3) runs list mutated in v4 (a G-run inserted) | receipt-fields + diff-audit | **PASS** — the real v4 receipt runs are exactly the eleven v4 runs, no `G*`; the mutant is KILLED by D2 and D3 |
| (4) docstring header left claiming the wrong provenance | diff-audit / docstring-provenance | **PARTIAL** — the *following-header label* is corrected and the M4 mutant is KILLED by D4, **but the module banner still self-identifies as the round-44 version-5 counter (Finding F1) and the retained excerpt is not the v3 header it claims (Finding F2)** |

**Overall: 4/4 mutants killed; 1/1 conformant reference survived; 2 findings against the pristine
shipped bytes (F1 stale v5 banner, F2 excerpt fidelity).**

---

## 7. Files written by this seat

**Lane report (the only lane file I wrote):**
1. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w1/MutCounterV6Spec.md` — this report.

**Scratch (`/fast/scratch/hyaku/kake-r45/MutCounterV6Spec/`), created by this seat:**

| File | sha256 | Purpose |
|---|---|---|
| `detectors.py` | `1ccbe7d480eaec1ed620f2b6293de877e6553cb81a274c749057ff7f5c99bbc0` | the 7-detector suite |
| `harness.py` | `5b67eb97cdf59163619ca0482266490c4e5f237f792ddcdc57fb0520845c9d54` | sandbox-stubbed receipt harness |
| `gen.py` | `807f139f8a19c13cc3de18f1a9f0882d0c5df0e771470784e3f98b2625392394` | builds reference + 4 spec mutants |
| `kill_commands.sh` | `8f3e93b1557fb157c3a358b41aee0e1d30942972efe49a5bcb9ebce8351b5050` | shell one-liner kill script |
| `d4c_probe.py` | `4380d5a7760a572d32a196f37245d8a8a88f454c6129bd6c7cdaab6eb2c86de8` | provenance-excerpt fidelity probe (F2) |
| `ref_spec.py` | `425427f08ce86ad0ee62450f898b4ff5a1800c1f6ebf05b659a64aec888c173e` | reference: spec-literal v6 (kills **only** D4b) |
| `ref_strict.py` | `9a2aa6793fa8fa2be9a8af061db34e146b7b38a408c382c91b3afcd96e7520c4` | reference: spec + v6 banner (**survives all 7**) |
| `m1_predicate_v5_changed.py` | `e0322034ad82d2ce263b8dd5aa460dadfaa1eedc49c26c77395a7eeb035bd017` | spec-level M1 |
| `m2_classruns_in_v4.py` | `1394be01a749568afdc6d61652b8e2c627f7906c53fb3c7d5ba227c9b9e013c8` | spec-level M2 |
| `m3_grun_in_v4.py` | `0cb16c17f69088079fc0c90748de802f1a65f64cb79da4fafb294a80197d5119` | spec-level M3 |
| `m4_wrong_provenance.py` | `39a798dcdc896e2b8c95b8d9a04c38010ffd379986ba2f46ec2d142c07b92ac5` | spec-level M4 |
| `m4b_stale_version_header.py` | `425427f08ce86ad0ee62450f898b4ff5a1800c1f6ebf05b659a64aec888c173e` | spec-level M4b (identical bytes to `ref_spec.py`) |
| `real_mutants/M1_predicate_v5_changed.py` | `90f8a908355c753d1c8b17d68f6a072f978c83ce6ae4c360054974761fc11920` | M1 derived from the **real** v6 |
| `real_mutants/M2_classruns_in_v4.py` | `402fe6f76020bf3d51c3deb6e3b10650d7cfdf7fdca7166472348fd982d5e9d2` | M2 derived from the **real** v6 |
| `real_mutants/M3_grun_in_v4.py` | `852c8dc22f73237a380790ce7f32fd3a693c03c2f34528c00957c717eac03184` | M3 derived from the **real** v6 |
| `real_mutants/M4_wrong_provenance.py` | `79e06ce74d0186caffd7edeabaf5977144db5ecda5bf977aaad46d56abd0c126` | M4 derived from the **real** v6 |
| `real_v4_receipt.json` | (receipt) | the real counter's own v4-mode receipt (§4) |
| `shell_out.txt` | (log) | captured `kill_commands.sh` output |

**No lane source, frozen file, receipt, ledger or history was edited by this seat.** All mutations
were written to scratch copies; the lane's `c45_count.py` was only read.

---

## 8. Restoration evidence

The frozen counter and the shipped v6 are byte-identical before and after this seat's work:

```sh
sha256sum .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-45/c45_count.py
```

```text
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
ce8bf2353d4f008a987f6fb3b6d3677d2dbed98aaae274126c68f0a3cf622556  .ufo/waves/round-45/c45_count.py
```

`5cedaa3b…` is the frozen v5 hash recorded in the round-44 receipts
(`counterSha256` in `.ufo/waves/round-44/verification/freeze/tools/portlen-v1.json`) and in
`CriticHarmGuard.md`; it is unchanged. `ce8bf235…` matches the snapshot hash `CriticV6Minimal`
independently reviewed and is unchanged. `git status --porcelain` lists `c45_count.py` only as an
untracked new file (written by `ExecCounterV6`); the frozen `c44_count_v5.py` does not appear — it was
never modified.

---

## 9. Unrun checks, blockers, tooling

- **Unrun:** no full bwrap counter run of the *mutants* (the mutants were observed through the
  sandbox-stubbed harness, whose receipt-construction fidelity is proven in §2 against committed
  bytes; the pristine real v6 *was* run for real in §4). No `c45_audit.py` / `c45_matrix.py` /
  `c45_freshness.py` execution — those are other seats' items and out of this seat's scope. No
  `ledger_latest_check.py` run. No build, lint or formatter.
- **Blockers:** none. The `verification/v6v4/counter-v4.json` receipt (`ExecV4ReceiptV6`) did not exist
  when I ran; I produced an equivalent receipt in scratch instead of waiting or polling.
- **Tool installs / updates:** none. No `pacman`, `uv tool install`, `npm -g` or binary download was
  performed. Everything used (`python3`, `jq`, `sha256sum`, `diff`, `grep`, `git`) was already present.
- **Sibling coordination:** `ExecCounterV6` and `CriticV6Minimal` both reviewed the same bytes and
  reached compatible conclusions (three allowed hunks; `CriticV6Minimal` independently flagged the
  excerpt-fidelity limit now formalised as Finding F2). Neither flagged the stale v5 **banner**
  (Finding F1); that is this seat's net-new contribution. `ExecCounterV6` owns `c45_count.py`; **this
  seat did not edit it** — F1 and F2 are reported for the L1 to route.

## 10. Godspeed axes

- **Freshness (judged axis):** the v6 predicate split is byte-faithful to the frozen v5 predicate
  (D1, D6 PASS on the real bytes) and the v4-mode receipt now names only the eleven v4 runs
  (D5 PASS, real receipt in §4). Two freshness defects remain open on the pristine bytes: the stale
  v5 banner (F1) and the over-claimed v3 excerpt (F2).
- **Operability (harm guard):** the four mutants that would have altered the run list, the class
  loader, the receipt schema or the scoring are all killed by D2/D3. The v6 diff against the frozen
  v5 has exactly three hunks (docstring + two predicate-text), all in the allowed classes.
- **Cheap iteration, parallel fronts:** the four mutants were built and evaluated as one batch against
  one detector suite; the harness stub made receipt-level detection cost ~15 s per candidate instead
  of a full bwrap counter run, which is what made a 4-mutant × 7-detector matrix affordable inside the
  15-minute box.
