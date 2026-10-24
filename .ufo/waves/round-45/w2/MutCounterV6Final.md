# MutCounterV6Final — four v6 counter mutants rebuilt against the FINAL bytes

Axes: **freshness** (judged), operability (harm guard).
Named attack: rebuild the four v6 mutants (PREDICATE_V5 changed; `classRuns` populated in v4; a
G-run inserted into the v4 runs; provenance header wrong) **from the final committed
`.ufo/waves/round-45/c45_count.py`**, and show each is killed by its detector — byte-compare,
receipt-fields from a fresh `--classes v4` run, diff-audit, docstring check. Additionally verify
that the module-level `PREDICATE` alias cannot mask a `PREDICATE_V5` change.

**Result: 4/4 named mutants KILLED, each by its named detector. Baseline pristine bytes SURVIVE
all detectors (no vacuous kills). Alias-masking probe M1b proves the alias DOES mask a
post-binding `PREDICATE_V5` change: `PREDICATE == frozen` while the counter's own v5 receipt
carries the drifted text. The shipped driver `c45_audit.py:437` records `counter_mod.PREDICATE`
(the alias), not `PREDICATE_V5` — a freshness coverage finding (F3), not a contract change.**

---

## 0. Source identity — this is not the file w1 attacked

| | sha256 | bytes |
|---|---|---|
| bytes `w1/MutCounterV6Spec.md` attacked (cited there) | `ce8bf2353d4f008a987f6fb3b6d3677d2dbed98aaae274126c68f0a3cf622556` | — |
| **final committed bytes attacked here** | **`e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b`** | 52277 |

The banner moved between the two. w1 recorded a **surviving** defect (F1 there): the module still
identified as `Round-44 C1 counter, version 5`. At the final bytes that is fixed:

```text
PASS  D4b docstring self-identification
      banner: 'Round-45 C2(b) counter, version 6 (built from the round-44 counter v5, sha256'
```

So the re-run is not ceremony: w1's one surviving finding is **closed at the final bytes**, and all
four mutants had to be rebuilt against `e17b5dc8` rather than inheriting w1's `ce8bf235` evidence.

Source file mtime, read-only, unchanged by this seat: `2026-10-24 00:39:28 -0300`, 52277 bytes.

---

## 1. Mutants — built as scratch copies, one defect each

Builder: `/fast/scratch/hyaku/kake-r45/MutCounterV6Final/build.py`. Each file is a full copy of the
committed bytes with **exactly one** substitution (`assert count == 1` before every replace).
Isolated-diff proof — changed-line counts per mutant against `base.py` (byte-identical to the lane file):

```text
M1_predicate_v5_literal.py         2
M1b_predicate_v5_post_alias.py     1
M2_classruns_in_v4.py              2
M3_grun_in_v4.py                   2
M4_wrong_provenance.py             2
```

| # | Mutant file (sha256) | The single change |
|---|---|---|
| **M1** | `721fbce04c6262174600cfe60f27eeaabaf386e9e7c5b13f206f63cbe0d2a0a1` | one character added inside the `PREDICATE_V5` literal: `the ten class runs), and` → `the ten class runs.), and` |
| **M1b** | `35da0ba2ab5532daf3794f374686337985ea37612ce3452626c5ad95100bd7df` | one line inserted **after** `PREDICATE = PREDICATE_V5`: `PREDICATE_V5 = PREDICATE_V5.replace("the ten class runs)", "the ten class runs.)")` — alias-masking probe (extra) |
| **M2** | `95ff1767ae6dc0e21165771980bfc1dcef8fdabba855bff28cc36b066c9ce6d1` | `"classRuns": [...] if a.classes == "v5" else []` → `"classRuns": [...]` (populated in v4) |
| **M3** | `37f1ed15657644ef77bb6e96ac1d8c9f28632f165413ac57bbff1bd0c6d8e214` | `classes = load_classes(root) if a.classes == "v5" else {}` → `classes = load_classes(root)` (G-runs enter the v4 run list) |
| **M4** | `d47ce85966f112ac3542353d6d1d164d4183a6523a0183da5eaa187fa47682f1` | `Round-42 version 3 header (with round-43 v4 edits) follows for provenance:` → `Round-43 version 4 header follows for provenance:` |

Pristine scratch copy `base.py`: `e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b`
(= lane file, byte-for-byte).

## 2. Detectors — offline, 5 checks

`detectors.py`:

- **D1** — imports the candidate and compares **`mod.PREDICATE_V5`** (runtime value, so it sees
  post-binding drift too) to the `PREDICATE` literal extracted by AST from the frozen
  `.ufo/waves/round-44/c44_count_v5.py`. It also prints `mod.PREDICATE == frozen` **for contrast
  only** — the alias is never the compared value.
- **D2** — fields of a receipt produced by a **fresh real `--classes v4` run** (no stubs): must be
  `classesMode == "v4"`, `classRuns == []`, run keys exactly
  `A,B,C,D,E,F,T1,T2,T3,T4,T5`, no `G*` key, predicate names the eleven v4 runs and not class runs.
- **D3** — per-changed-line diff audit `c44_count_v5.py → candidate` (difflib, n=0). A changed line
  is allowed only inside the module docstring span, inside a top-level `PREDICATE*` assignment span
  (AST `lineno..end_lineno`, so multi-line implicit concatenation is covered), or if it mentions
  `PREDICATE|predicate`. Everything else — run list, class loader, scoring, CLI, other receipt
  fields — is a FAIL.
- **D4** — the `… follows for provenance:` claim must name the header that actually follows it
  (`Round-N` / `version M` pair equality).
- **D4b** — the module banner must self-identify as `Round-45` / `version 6` (w1's F1 made
  executable).

## 3. Baseline — pristine final bytes must survive

```sh
python3 -B detectors.py --candidate /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45_count.py \
  --receipt receipts/base.v4.json
```

```text
=== candidate: /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45_count.py ===
PASS  D1  PREDICATE_V5 byte-compare
      alias PREDICATE == frozen: True   (alias must not be the compared value)
PASS  D2  receipt-fields classRuns/runs/predicate (fresh v4 run)
      equalRuns=11/11 met=True keys=['A', 'B', 'C', 'D', 'E', 'F', 'T1', 'T2', 'T3', 'T4', 'T5']
PASS  D3  diff-audit changed-line classes (v5 -> candidate)
      every changed line is module-docstring or PREDICATE* text
PASS  D4  docstring provenance claim
      claim 'Round-42 version 3 header (with round-43 v4 edits)' vs following header 'Round-42 C1 counter, version 3 (pre-freeze redesign of versi'
PASS  D4b docstring self-identification
      banner: 'Round-45 C2(b) counter, version 6 (built from the round-44 counter v5, sha256'
verdict: SURVIVED (0 failed, 0 skipped)
```

The fresh v4 receipt behind D2 (real sandbox, seed 45002, `--classes v4`):

```text
{"label": "", "revision": null, "toolSha256": "914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021",
 "equalRuns": "11/11", "ratios": {"T1": 0.987, "T2": 1.147, "T3": 1.221, "T4": 1.234, "T5": 1.128}, "met": true, "note": null}
exit=0 wall=26s
```

So the suite discriminates: the reference survives, and every kill below is a delta against a
passing baseline on the same detectors.

## 4. The four named mutants, killed

### M1 — `PREDICATE_V5` changed (byte-compare)

```text
KILL  D1  PREDICATE_V5 byte-compare
      frozen PREDICATE: "...run (the eleven v4 runs and the ten class runs), and its median CPU..."
      candidate PREDICATE_V5: "...run (the eleven v4 runs and the ten class runs.), and its median CPU..."
      alias PREDICATE == frozen: False   (alias must not be the compared value)
verdict: KILLED (1 failed, 1 skipped)
```

D2 is skipped here by design: the v4 receipt's predicate is `PREDICATE_V4`, untouched by M1, so the
defect is invisible in v4 mode. D3 passes (the changed line is inside a `PREDICATE*` span, which
D3 allows). **Only the constant-level compare sees M1** — the detector assignment asks for exactly
that.

### M2 — `classRuns` populated in v4 mode (fresh v4 receipt + diff-audit)

```text
KILL  D2  receipt-fields classRuns/runs/predicate (fresh v4 run)
      equalRuns=11/11 met=True keys=['A', 'B', 'C', 'D', 'E', 'F', 'T1', 'T2', 'T3', 'T4', 'T5']
      classRuns=['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10']
KILL  D3  diff-audit changed-line classes (v5 -> candidate)
      non-allowed changed line v5:1001: "classRuns": [key for key, _ in CLASS_MODULES] if a.classes == "v5" else [],
      non-allowed changed line cand:1001: "classRuns": [key for key, _ in CLASS_MODULES],
verdict: KILLED (2 failed, 0 skipped)
```

The fresh-run receipt (seed 45002, wall 25s, exit 0) is the evidence — the receipt claims
**`classRuns: [G1..G10]` under `classesMode: "v4"` while the run keys prove only the eleven v4 runs
executed**. Note `met: true` and `equalRuns: "11/11"`: the receipt's own pass flag does not see the
lie. Only the field-level detector does (F2).

### M3 — a G-run inserted into the v4 runs (fresh v4 receipt + diff-audit)

```text
KILL  D2  receipt-fields classRuns/runs/predicate (fresh v4 run)
      equalRuns=21/21 met=True keys=['A', 'B', 'C', 'D', 'E', 'F', 'G1', 'G10', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'T1', 'T2', 'T3', 'T4', 'T5']
      runs keys [...] != the eleven v4 runs
      v4 runs contain class keys ['G1', 'G10', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9']
KILL  D3  diff-audit changed-line classes (v5 -> candidate)
      non-allowed changed line v5:1046: classes = load_classes(root) if a.classes == "v5" else {}
      non-allowed changed line cand:1046: classes = load_classes(root)
verdict: KILLED (2 failed, 0 skipped)
```

Fresh run (seed 45002, wall 27s, exit 0) produced `"equalRuns": "21/21"`, `met: true`. This is the
round-44 failure mode itself: **a v4 receipt that claims to be v4 while executing the ten class
runs**, and still reports success. D2 catches the shape; D3 catches the source line.

### M4 — provenance header wrong (docstring check)

```text
KILL  D4  docstring provenance claim
      claim 'Round-43 version 4 header' vs following header 'Round-42 C1 counter, version 3 (pre-freeze redesign of versi'
verdict: KILLED (1 failed, 1 skipped)
```

D3 passes M4 because the changed line is inside the module docstring span — **by construction D3
cannot police docstring content**. That is why D4 must exist as a separate detector (F3): the
provenance claim is only checkable against the header that actually follows.

## 5. Alias masking — the named trap, made executable

`PREDICATE = PREDICATE_V5` binds at import. A **literal** edit (M1) propagates to both names, so the
alias is not a hiding place there. The dangerous shape is a **rebind after the alias line** (M1b):
the alias keeps the frozen text while `PREDICATE_V5` — the name the counter actually writes into v5
receipts at `c45_count.py:996` — drifts.

```text
=== candidate: mutants/M1b_predicate_v5_post_alias.py ===
KILL  D1  PREDICATE_V5 byte-compare
      candidate PREDICATE_V5: "...run (the eleven v4 runs and the ten class runs.), and its median CPU..."
      alias PREDICATE == frozen: True   (alias must not be the compared value)
verdict: KILLED (1 failed, 1 skipped)
```

**The alias says the predicate is unchanged; the counter's own receipt says otherwise.** A v5-mode
run of M1b (real sandbox, seed 45002, wall 29s, exit 0, `equalRuns 21/21`, `met true`) wrote:

```text
driver line 437 value (counter_mod.PREDICATE) == frozen: True
counter line 996 source (PREDICATE_V5)          == frozen: False
v5 receipt predicate                            == frozen: False
v5 receipt predicate tail: the ten class runs.), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's
v5 receipt classRuns: ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10'] equalRuns: 21/21 met: True
```

**The detector in §2 compares `PREDICATE_V5` and kills M1b; a detector comparing the alias would
have SURVIVED it.** The check the assignment asked for holds on my side — but see F3 for the
shipped driver's read.

## 6. Verdicts

| Attack | Detector | Verdict |
|---|---|---|
| M1 `PREDICATE_V5` literal changed | D1 byte-compare of `PREDICATE_V5` | **KILLED** |
| M1b `PREDICATE_V5` rebound after the alias | D1 (alias would survive) | **KILLED** (alias-masking exposed) |
| M2 `classRuns` populated in v4 | D2 fresh v4 receipt + D3 diff-audit | **KILLED** (both) |
| M3 G-run inserted into v4 runs | D2 fresh v4 receipt + D3 diff-audit | **KILLED** (both) |
| M4 provenance header wrong | D4 docstring claim | **KILLED** |
| Baseline: pristine final bytes | all five | **SURVIVED** |

**Pass against the named attack: 4/4 named mutants killed, 1/1 pristine baseline survives, and the
alias-masking trap is real but does not blind a `PREDICATE_V5`-comparing detector.**

## 7. Findings

**F1 (freshness, CLOSED) — w1's surviving banner defect is fixed at the final bytes.** w1 reported
the module still said `Round-44 C1 counter, version 5` and killed it with its D4b (`ce8bf235…`).
Final bytes (`e17b5dc8…`) read `Round-45 C2(b) counter, version 6`; my D4b passes. The file was
rewritten at 00:39:28, after w1's evidence was taken — which is exactly why w1's kills could not be
inherited.

**F2 (freshness/operability, open coverage) — the receipt's own success flag is blind to both
receipt-shape mutants.** M2's v4 receipt says `met: true`, `equalRuns: 11/11` with `classRuns`
populated; M3's says `met: true`, `equalRuns: 21/21`. Any gate that trusts `met`/`equalRuns` alone
passes both. The named field-level detector (D2) is load-bearing for C2(b); this is a property of
the artefact, not a new contract demand.

**F3 (freshness, coverage gap in the shipped driver) — `c45_audit.py:437` records the alias, not
`PREDICATE_V5`.** The line is `"predicate": counter_mod.PREDICATE,` in the run summary. With the
current bytes that value is byte-identical to `PREDICATE_V5`, and the driver does **not compare**
the field anywhere (grep: single assignment, no comparison), so nothing is currently mis-certified.
But a post-alias rebind (M1b) leaves that summary field claiming the frozen predicate while every
v5 receipt carries the drifted one — demonstrated in §5. If a later check ever compares
`summary.predicate` for receipt comparability, it must read `counter_mod.PREDICATE_V5`, not the
alias. Recorded as a coverage finding; no driver edit made by this seat (read-only lane).

**F4 (detector-shape) — no one detector covers all four mutants.** M1 passes D3; M4 passes D3; M1b
passes D3 and D2-v4. The four named detector classes are each necessary; a single "diff is clean"
gate would have let three of the five probes through.

## 8. Restoration and harm evidence

The lane file was never written. Hashes and mtime before and after this seat's work:

```text
before: e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b  52277 bytes  00:39:28 -0300
after : e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b  52277 bytes  00:39:28 -0300
scratch base.py: e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b
```

All mutants and receipts live under `/fast/scratch/hyaku/kake-r45/MutCounterV6Final/`. No commit,
no `jj`, no push; no edit to `MANIFEST.json`, `scripts/`, `templates/`, route tables, `mcp.json`, or
`.ufo/state/`.

## 9. Files written

Lane (this report only):
- `.ufo/waves/round-45/w2/MutCounterV6Final.md`

Scratch (`/fast/scratch/hyaku/kake-r45/MutCounterV6Final/`):
- `build.py` (mutant builder), `detectors.py` (D1/D2/D3/D4/D4b), `base.py` (pristine copy)
- `mutants/M1_predicate_v5_literal.py`, `mutants/M1b_predicate_v5_post_alias.py`,
  `mutants/M2_classruns_in_v4.py`, `mutants/M3_grun_in_v4.py`, `mutants/M4_wrong_provenance.py`
- `receipts/base.v4.json` (`0e0b1422…`), `receipts/M2_classruns_in_v4.v4.json` (`039addda…`),
  `receipts/M3_grun_in_v4.v4.json` (`57f2352b…`), `receipts/M1b.v5.json`
- `final_suite.txt` (coherent full detector output)

## 10. Unrun / bounded

- Prompt-injection detector beyond *fresh receipt fields + line-class diff + claim string*: not
  attempted (out of the named attack).
- `c45_audit.py` end-to-end over the 27-control cohort with a mutated counter: **not run**
  (27 real sandboxed counter runs exceed the 15-minute box). F3 is therefore a static read of line
  437 plus the module-level and receipt-level demonstration in §5, not a driver-level certification.
- No tool installs or updates this seat (the only package-shaped need, `/usr/bin/time`, was absent;
  the run was timed with `$SECONDS` instead — no pacman/uv/npx transaction was attempted).
