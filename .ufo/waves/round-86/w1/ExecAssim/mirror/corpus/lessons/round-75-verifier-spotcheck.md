author: hyaku closure (non-author integrator, @m_zfl)

# Round 75 — non-author verifier spot-check (kake)

Lane `kake`, round 75 (hyaku run 15, attempt 1). I did not author this round and did not improve it.
Base `c9c5e484c533aa65f4374b841a3edcf572ed19a9`; lane tip `0df52aed0b68d355ae3d73e5bc8f5bbda3c05ee6`;
report `.ufo/reports/round-75/kake.md` (fleet commit `2c862ffd`, author `kake-shokunin
<kake@shokunin.local>`). Every command below was run read-only over committed bytes (`git show
<rev>:<path>`); no lane gate was executed (PROTOCOL §Gate standard, *Closure consequence*), so each claim
is labelled **re-measured** (my own plain count/digest) or **evidence-verified** (the counter's committed
receipt, self-test tally and measured revision).

## 1. Step-1 conformance

| Check | Command | Observed | Ruling |
|---|---|---|---|
| Report identity | `git -C /home/vgpnk/Projects/shokunin log --format='%an %H %s' -- .ufo/reports/round-75/kake.md` | `kake-shokunin … 2c862ffd round-75: kake report (final lane tip)` (and `2fa1fa86` at 21:29:15, superseded) | conform — lane identity, not protocol/hyaku |
| Filing order | `git show -s --format=%cI` | report `2c862ffd` 21:29:33-03:00 > lane tip `0df52aed` 21:29:27-03:00 | conform (the earlier `2fa1fa86`, 12 s before the tip, was replaced in place) |
| `SHONEN` heading | read report §SHONEN | heading present; **4 box lines**, one per box, all `[~]` with resolvable pointers | conform |
| Cited commits | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> master` over all 15 lane hashes named (`88f2e05f ab939c46 9a9c4a6f d599c8be 7348d37e f1fc5d0a 4e3fc159 abfbfaac f87d14a9 6c10b433 ca1a2982 306fff49 3ae076ab 0df52aed c9c5e484`) | every hash `exists ancestor=yes` | conform — no dead or orphaned hash |
| Worktree / push | `jj-lane.sh state` (git-only) + `git status --porcelain` | `local=0df52aed remote=0df52aed ahead=0 behind=0 tracked=0 untracked=0 head=detached`; porcelain empty | conform |
| Prompt contract | `diff <(sed -n '3,140p' templates/round-prompt.md) <(sed -n '3,140p' .ufo/prompts/kake-round-75.md)` | diffs only where `{{FLEET_ROOT}}`/`{{AXES}}`/`{{ROUND}}`/`{{LANE}}` render; §6 hyaku addendum and §7 scratch discipline follow | conform — round-level + five child-lane items carried verbatim |
| Wave | `w1-results.json` | `seats=14`, `results=14`, empty outputs `[]`; roles executor 4, scout 2, scribe 2, reviewer 2, critic/mutation-tester/connector/sentinel 1 each; attack 4/14 = 28.6 % | conform — no undispatched wave, no dead seat |
| Marker test | real report, two checkable claims, six lane commits | — | not a marker → status `ok` |

Note (dispatch-time, not a lane defect): prompt §6 predates the addendum file's final routing amendment
(net map now reviewer-only `@m_zfl`); the lane's axes line reads "operability + freshness (web properties
and publishing)" against MISSION.md's `(web properties)` — the axes themselves match.

## 2. Claim re-checks

### C1 — calibration: every live registry row's claim re-derives (2 → 0 mismatches)

- **Population re-derived independently** by re-implementing the frozen row parse (`### Round <N> gate
  registry additions` sections; Kind cell without `historical`; Name cell, else Entry command, else
  Self-test, else any cell → first `.py`/`.mjs` token) over `git show <rev>:SKILL.md`:
  `c9c5e484 rows=28 live=16 files=16` / `0df52aed rows=32 live=20 files=18` — **exactly the reported
  values**, and the 18 effective files are the 18 receipt paths.
- **Base red, committed**: `controls/base-c1-row-truth-landed.txt` →
  `C1v1 revision=c9c5e484 rows=28 live=16 files=16 mismatches=2 classes=E1 E3 append_only=true met=false
  missing_frozen=0`, exit 1, findings `E1 .ufo/waves/round-69/c69_tmp_honour.py` and `E3
  .ufo/waves/round-74/c74_registry_gap.py: cell enumerates 5 fixture ids, observed total 8`.
  I re-opened the two named files: `c74_registry_gap.py` defines `def fx_f1`…`fx_f8` (8 functions,
  `FIXTURES` tuple, `selftest %d/%d` over `len(FIXTURES)`), and its docstring line 25 still says "five
  contract fixtures f1-f5" (the stale prose the lane routes itself).
- **After green, committed**: `controls/after-c1-row-truth.txt` →
  `C1v1 revision=f87d14a9 rows=32 live=20 files=18 mismatches=0 classes=- append_only=true met=true
  missing_frozen=0`, `counter_sha256=63e321b2…`, exit 0. `git show f87d14a9:…/c75_row_truth.py |
  sha256sum` and the tip blob both give `63e321b28e509781405f1b4209a66b99460bc2512c92a8615fec06f2423e944b`;
  `SKILL.md` and the counter are byte-identical from `f87d14a9` to the tip.
- **Sensitivity**: cheap content stays red (`… rows=30 live=18 files=16 mismatches=2 classes=E1 E3
  append_only=true met=false`, exit 1); deletion trips the floor (`… files=15 mismatches=3 classes=E3
  append_only=false met=false missing_frozen=1`, exit 1). Standing gates re-ran green in the tip battery
  (`c66` `members=28 … agreement=25 met=True`, `c72` `findings=[] met=True`, `c73_tmp_v3` `selftest=41/41`,
  `c73_wave_pointers`, `c74gap` `unregistered=0 own_row=true`, `c74side` `contradictions=0`) with the same
  values the round-74 spot-check recorded.
- **Evidence-verified**: the executed `mismatches` value, `append_only=true` and the self-test tally
  (`C1v1 selftest fixtures=29 passed=29 failed=0`, committed `w1/ExecC1Counter/selftest.txt`). **Re-measured**:
  populations, effective-file set, red/green control text, counter digest.

### C2 — operability: every live instrument bound to a committed receipt (0 → 18)

- **Receipt re-derived from committed bytes**: `git show 0df52aed:corpus/knowledge/instrument-receipts.json`
  → `schema=instrument-receipts/v1 revision=abfbfaac date=2026-11-03 host=linux-x86_64 files=18`; for each
  entry I recomputed `sha256sum` and the byte length of `git show 0df52aed:<path>`: **18/18 match, 0
  mismatches**. Its 18 paths equal the C1 effective-file set (frozen 16 floor + `c75_row_truth.py` +
  `instrument_receipts.py`).
- **Identity**: receipt blob `15768f81460bcbf991bacf9ffdf6a2145d32f4de7d952f52526589d8013e6613`, 3793 B —
  identical to `receipt_sha256=… receipt_bytes=3793` in `controls/after-c2-receipts.txt`; tool blob
  `162dd685…` identical in both the control line and the tip tree.
- **Base red / after green, committed**: `C2v1 revision=c9c5e484 population=16 bound=0 mismatches=16
  met=false`, exit 1 (receipt absent at base) → `C2v1 revision=f87d14a9 population=18 bound=18
  mismatches=0 met=true`, `population: derived=18 frozen=16 missing_frozen=0 beyond_frozen=2`,
  `receipt: source=committed worktree=identical declared=abfbfaac… declared_match=false declared_valid=true`,
  exit 0.
- **Static mode flags**: `selftest_mode` is `true` for 16 entries and `false` for exactly the two files whose
  rows/code register no self-test (`c57_idresolver_gate.py`, `c69_tmp_honour.py`); `--selftest` on
  `c69_tmp_honour.py` exits 2 with an argparse error, as its row states.
- **Evidence-verified**: executed `bound=18`/`mismatches=0`, the 17/17 tool self-test (committed transcript
  `w1/ExecC2Tool/selftest.txt`, sha256 `13016087…` as recorded) and the forgery reds. **Re-measured**: all
  18 digests/byte counts, the receipt digest and length, the population identity.

## 3. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | **improved** | two live registry rows that asserted false capabilities now re-derive (`mismatches` 2 → 0 over 18 files); the demotion and the eight-fixture supersession are appended rows, the reds are reproducible at the base |
| operability | **improved** | 18 live instruments carry a committed `{sha256, bytes, selftest_mode}` receipt that re-derives from committed bytes; the capability row enters SCORECARD with a working demonstration |
| depth | unchanged | no new decision table beyond the registry rows and one appended `QUALITY.md` criterion; nothing weakened |
| coverage | unchanged | frontier ground unchanged by the report's own account; `corpus/README.md` gains coverage rows, not ground |
| freshness | unchanged | the sweep still exits 1 on the same single `~/projects` drift; no stale entry was left unmarked |
| adjacency | unchanged | the connector re-read `merge/kake/` and adopted nothing; the four sibling digest-binding variants are reported in `PROVINCE.md` and `knowledge/instrument-receipts.md` §Limits, not absorbed |

No axis is harmed: `git diff --numstat c9c5e484 0df52aed` over `LOG.md SCORECARD.md corpus/QUALITY.md
corpus/SOURCES.md corpus/README.md PROVINCE.md` reports zero removed lines for every file (12/0, 31/0,
32/0, 1/0, 2/0, 16/0), and every standing gate in the tip battery is at least as green as at the round-74
spot-check.

## 4. Discernment spot-check (non-author, sampled from `## Gate`)

| Item | Decision | Source re-opened | Agree? | Reason |
|---|---|---|---|---|
| S443 in-toto Statement v1 | admit | `https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md` (live fetch) | **agree** | HTTP 200, 2,492 B, sha256 `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea` — byte-identical to the row and the report; the 6-word quote is a raw substring of line 37 (`> represents a single software artifact. Each element MUST have \`digest\` set.`), ≤25 words; the anchor names the line, so the blockquote prefix is not hidden |
| `c69_tmp_honour.py` Kind demoted `gate → instrument` | admit | `.ufo/waves/round-69/c69_tmp_honour.py`; SKILL rows at base and tip | **agree** | argparse registers only `--root/--revision/--work/--baseline`; `--selftest` exits 2; the row's own Self-test cell says "none"; PROTOCOL §Gate *Self-test* is not met, and `E1` would red it — the demotion is the honest label, and the old `gate (live …)` row is retained beside it |
| `c74_registry_gap.py` eight-fixture superseding row | admit | `.ufo/waves/round-74/c74_registry_gap.py` | **agree** | 8 fixture functions `fx_f1`–`fx_f8`, `FIXTURES` enumerates all eight, `selftest %d/%d` prints over `len(FIXTURES)`; the base row's "five" is false, so the appended row states the measured state |
| "add a `--selftest` to `c69_tmp_honour.py`" | reject | `.ufo/waves/round-69/controls/{c2-base,c2-after-t1}.txt` | **agree** | the instrument's three terms are already exercised by committed base and after controls (`tmp_literals=2 …` → `tmp_literals=0 … offline_unchanged=true`); a new suite would rewrite a frozen instrument's surface to serve a label fix |
| "delete the failing row" | reject | `controls/ctl-deletion.txt`; `.ufo/waves/round-73/c73_wave_pointers.py:311-312` | **agree** | deletion control prints `rows=27 live=15 files=15 mismatches=2 classes=E3 append_only=false met=false` with `base row 'c69_tmp_honour.py' is gone`; the standing gate computes `met = (not unannotated) and len(dead_tokens) >= 2 and append_only`, so deletion is structurally red, not repaired |
| `merge/kake/` assimilation as a whole | reject | four cited locators; kake `corpus/SOURCES.md` | **agree** | `.ufo/waves/round-14`, `/15`, `/16` and `.ufo/waves/corpus-expansion-1/audit-wave.py` are absent (`test -e` fails); S319/S371/S401/S407/S412 return 0 rows in kake's registry while the tip is S443, so adoption would cite unreachable paths and insert ids below the tip |

Six decisions re-opened, six agreements, no disagreement. Curation census: `scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin kake` → `kake ok` (181 rows), exit 0, the same 16 `W04`
duplicate-URL warnings the round reports as unchanged; `corpus/SOURCES.md` gained exactly one line
(`git diff --numstat` 1/0), so no pre-existing row's status/recheck/used-by cell moved.

## 5. Trend verdicts

- **expansion — improved.** One admitted `knowledge/` entry on ground the coverage map did not hold
  (`corpus/knowledge/instrument-receipts.md`: the registry-derived instrument inventory with its own
  precedence rule), with the provenance trio citing the `mined` S443 row, two new `corpus/README.md`
  coverage rows and one new tier-A source row (180 → 181). Qualified, as the lane states: the digest
  primitive itself is held in four sibling lanes and tameshi's S281 is the same spec (`tameshi-shokunin/
  corpus/SOURCES.md:156`), so the entry is scoped to the inventory, not to digest binding.
- **quality — improved.** Two registry claims that stated capabilities the instruments did not have now
  re-derive (base red → after green, re-run green in the tip battery); 18 instruments are digest-bound with
  a receipt I re-derived end to end; standing gates are unchanged or green. Two stale digests in the
  round's own `LOG.md` entry are a documentation defect routed below, not a false admitted entry.
- **discernment — improved.** The Gate records 3 admits and 3 rejects, each with a flip condition; this
  non-author spot-check agrees on all six. Two reviewer findings were adopted as amendments (argument-bound
  command programs, the committed-receipt and declared-revision clauses) instead of argued away, and the
  critic's "erasure is as cheap as the honest fix" finding is carried as a stated limit.

## 6. Routed defects (status-neutral; the lane fixes them next round)

1. **Stale counter digest in `LOG.md:2534`.** The round-75 entry names the hardened counter as `0699a672…`
   (the blob at `4e3fc159`); the tip blob is `63e321b2…`, the digest the report and both control receipts
   name. Append a correction naming the superseded digest (PROTOCOL §Evidence standard, *Corrections sweep
   every mention*).
2. **Stale receipt digest in `LOG.md:2535`.** It names the receipt as `18 entries, f3128628…, 3,793 B`
   (the cut at `4e3fc159`); the committed receipt at the tip hashes `15768f81…` (3,793 B, verified with
   `sha256sum` over `git show 0df52aed:corpus/knowledge/instrument-receipts.json`). Same correction row.
3. **Revision labels disagree with their own evidence.** The before→after table is headed "After (tip
   `6c10b433`)" while every after cell, and the receipt it cites, name `f87d14a9`; the tip paragraph calls
   `3ae076ab` "the measured revision"; `controls/after-harm-battery.txt` measures the tree at `306fff49`
   although it is committed at `3ae076ab`/`0df52aed`. State one measured revision per artifact.
4. **R5 is only partly closed.** R5 named three files; the C2 receipt binds one of them
   (`c74_registry_gap.py`). `c74_sidecar_reobserve.py` and `scripts/sidecar_reobserve.py` still have no
   committed sha256 receipt (and no registry row, so they are outside C2's population); the report's
   "R1, R2, R5 are closed" overstates R5. Either bind them in a later receipt or say they stay open.
5. **Round-74 R3 is left undispositioned.** R3 asked for the sweep line to be annotated with the phrase or
   for the count delta (193 → 195 files, 6 → 7 unannotated cites) to be recorded; the round records neither
   and the sweep still exits 1 on the same class. Record the delta in the next lesson.
6. **`QUALITY.md` able-to-fail quote is not a contiguous substring.** The round-75 criterion quotes the
   deletion control as `files=15 append_only=false met=false`; `controls/ctl-deletion.txt` reads
   `… rows=27 live=15 files=15 mismatches=2 classes=E3 append_only=false met=false`. Quote the landed line
   (`…-landed.txt`) whole, or mark the elision.
7. **C2 quotation scope.** The after-quote omits `declared_match=false` (receipt subject `abfbfaac` ≠
   carrier `f87d14a9`), and the reviewer's 16-forgery matrix was run on the predecessor tool blob
   `62b795ea…`, not on the landed `162dd685…`; the report cites that suite without the scope. Disclose the
   subject/carrier split and the snapshot scope.
8. **Superseded docstring** (the lane's own item 4): `c74_registry_gap.py:25` still says "five contract
   fixtures f1-f5". An appended docstring correction or a round-74 erratum closes it.

## 7. Status

`CLOSURE kake r75 status=ok admitted=true`. Both claims verify (C1 re-measured populations plus
evidence-verified executed verdicts; C2 re-measured digests plus evidence-verified executed verdicts), no
owned axis is harmed, and the three trends are `improved`. Routed defects 1–8 are documentation/evidence
hygiene and do not touch either claim's measurement.

Operator note: the four `SHONEN.md` boxes look fully checkable by a non-author from the repo (box 1:
`SKILL.md` round-75 registry section + the `QUALITY.md` criterion; box 2: `LOG.md` round-75 end-to-end;
box 3: both instruments' argv and self-tests; box 4: `PROVINCE.md` round-75 section). Promotion is
operator-owned and was not touched.
