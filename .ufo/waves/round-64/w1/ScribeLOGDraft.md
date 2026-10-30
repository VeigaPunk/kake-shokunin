# ScribeLOGDraft — round-64 LOG entry draft and pointer verification

Seat: `ScribeLOGDraft` (scribe, leaf, no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Basis: base `1a48131577ba82c967650561be34e8dba909432a` (round-63 tip), measured T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`, receipts commit `cc8add1fa740b920ea5179a71152680ab220c70c`.
Scope: draft the round-64 LOG entry in this report only. `LOG.md` was not written. Verify every cited pointer at `cc8add1f`.

## 0. Bottom line

- The LOG entry is drafted in §2. Its verdicts are **not final**: the wave is unsettled and two claims carry open kill-rule questions.
- **C1** is measured green at T0, but wave reports reproduce green from planted prose and from an altered spot verdict. That matches the contract's named kill-rule classes. Verdict left OPEN for the adjudicator (§3.1).
- **C2** is measured green, the stub differential reproduces, and no attack passed a stub. Verdict: met pending settlement.
- **C3** is measured `VERDICT: OK` exit 0, but the T0 after-receipt contains no `§paths` section, and the contract's "line and lineSha256" wording is wrong: only `line` cells changed.
- Wave pointers do not exist at `cc8add1f`. `w1-results.json` is not written, and `w1/` is untracked (37 of 65 reports present at 11:13Z, mine among the 28 missing). The LOG must not cite a results file until it is committed.
- Several claims in the round-64 lesson have no pointer at `cc8add1f` (§4). They must be fixed or dropped before landing.

## 1. Verification method

All checks were read-only against the lane. No mutating git or jj command was run; no file in the lane was written.

Commands used (exact):

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse --show-toplevel        -> /home/vgpnk/Projects/shokunin/kake-shokunin
git -C .../kake-shokunin log --oneline -8                                           -> cc8add1f top; 4c8295fa; 1a481315 ...
git -C .../kake-shokunin status --short                                             -> ?? .ufo/waves/round-64/{sources/S432.live.html,w1-dispatch.json,w1-spec.json,w1.ready,w1.ready.dispatched,w1/}
git cat-file -e cc8add1f:<path>                                                     -> per-pointer existence (§1.1)
git diff --stat 1a481315 cc8add1f                                                   -> 35 files, +1857 -7
git diff -U0 1a481315 cc8add1f -- corpus/knowledge/freshness-sidecar.json           -> 7 hunks, each a single `line` cell
git diff --quiet 1a481315 cc8add1f -- corpus/SOURCES.md  (also SCORECARD.md, LOG.md) -> identical (exit 0) for all three
git show cc8add1f:<path> | sha256sum                                                -> frozen instrument shas (§1.2)
git show cc8add1f:SKILL.md > /fast/scratch/hyaku/kake-r64/ScribeLOGDraft/SKILL.at-cc8add1f.md
  + python3 check: each sidecar entry's lineSha256 vs sha256 of SKILL.md line `line` at cc8add1f
```

### 1.1 Pointer existence at `cc8add1f`

| Pointer | At cc8add1f | Note |
|---|---|---|
| `.ufo/waves/round-64/contract.md` | OK | |
| `.ufo/waves/round-64/c64_calibration.py` | OK | sha256 `5489eb2f…088adf` verified (§1.2) |
| `.ufo/waves/round-64/c64_quote_tool.py` | OK | sha256 `96fd64e9…27d6` (full `96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b`) verified |
| `.ufo/waves/round-64/fixtures/build_fixtures.py` | OK | sha256 `7fbd8cbc…71d3` verified |
| `.ufo/waves/round-64/fixtures/stub_tool.py` | OK | sha256 `7c78a05d…edde` verified |
| `controls/base-c1.txt` | OK | `met=false` exit 1 at base |
| `controls/after-c1.txt` | OK | `met=true` exit 0 at T0 |
| `controls/after-c2.txt` | OK | `met=true` exit 0 at T0 |
| `controls/control-marker.txt` | OK | `met=false` exit 1 (rev `4c666e76`) |
| `controls/control-fabrication.txt` | OK | `met=false` exit 1 (rev `f924538e`) |
| `controls/control-junk.txt` | OK | `met=false` exit 1 (rev `82dcba0d`) |
| `controls/control-ledger-mut.txt` | OK | `met=false` exit 1 (rev `5b981bd0`); **not in `fixture-builds.txt`** (§4 D2) |
| `controls/selftest-c1.txt` | OK | `selftest 26/26`, `c1=0` |
| `controls/selftest-c2.txt` | OK | `selftest 11/11`, `c2=0` |
| `controls/stub-c63-defect.txt` | OK | `c63 met=true` exit 0 on stub `14fe2eab` |
| `controls/stub-c64.txt` | OK | `tool_sha=mismatch met=false` exit 1 |
| `controls/sweep-before.txt` | OK | single exception trace, `sweep-before-exit=2` (§4 D4) |
| `controls/sweep-after.txt` | OK | `VERDICT: OK (exit 0, partial: offline)`; **no `§paths` section** (§3.3) |
| `controls/sidecar-repin-map.txt` | OK | 7 rows, `line` old→new |
| `controls/census-before.txt` / `census-after.txt` | OK | 171 rows, 16 W04, exit 0 both |
| `controls/fixture-builds.txt` | OK | 4 lines; no ledger-mut-repo |
| `controls/no-harm/sweep.txt` | OK | `§paths … drift 0`; generated `2026-10-30T10:59:21Z` |
| `controls/no-harm/{append-guard-63tip,c58,c59-axis,c61-pins,c63-cal-base,c63-tool-base,idres}.txt` | OK | present |
| `sources/receipts.json` | OK | contains sha `63b0a018…` (2 hits) |
| `corpus/lessons/round-64.md` | OK | Mistakes row L30, Gate L~70–100 |
| `corpus/knowledge/freshness-sidecar.json` | OK | 30 entries; 7 `line` cells changed |
| `corpus/knowledge/response-header-expectations.md` | OK | `[r63-correction]` block at L224 |
| `corpus/QUALITY.md` | OK | `## Round-64 criteria` at L1424 |
| `SKILL.md` | OK | 2 gate rows at L1363 (`calibration-counter`), L1364 (`quote-tool-counter`) |
| `corpus/SOURCES.md` | OK | 171 rows; byte-identical to base |
| `corpus/lessons/round-61-verifier-spotcheck.md` | OK | S432 row at **L33**, reason text present |
| `corpus/lessons/round-63.md` | OK | §Outside verdict L61–65 |
| `.ufo/waves/round-63/quote-class/quote-classes.json` | OK | contains sha `63b0a018…` |
| `.ufo/waves/round-63/quote-class/extract_text.py` | OK | |
| `.ufo/waves/round-61/sources/S432.html` | OK | retained raw body |
| `.ufo/waves/round-63/sources/S432.live.html` | OK | |
| `.ufo/waves/round-64/sources/S432.live.html` | **MISSING** | untracked in lane; receipts.json cites its sha (§4 D8) |
| `.ufo/waves/round-64/w1/` | **MISSING** | untracked; 37/65 reports at 11:13Z |
| `.ufo/waves/round-64/w1-spec.json`, `w1-results.json` | **MISSING** (spec untracked; results not written) | §3.5 |
| `scripts/quote_class.py` | OK | sha256 `431e75e8…1f14` verified (frozen tool) |
| `scripts/freshness-sweep.mjs` | OK | |
| `scripts/id_resolver.py` | OK | |
| `scripts/sources-census.sh` (lane) | **MISSING** | exists only at fleet root `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, which the lesson cites as an absolute path |
| `merge/kake/` (assimilation package) | **MISSING** | absent at cc8add1f, in the lane, and at fleet root `merge*` (§4 D6) |
| `.ufo/waves/round-50/quote-classes.json` | OK | round-50 ledger (SCORECARD L204 row) |

Commit hashes cited in the lesson all exist: `9f671056`, `d2da25de`, `1a481315`, `3d07733b`, `f8438a28`, `4cb225fb`, `4c8295fa`, `cc8add1f`, `05b0d7f4`, `0b06a9c4`, `de7d96e7`, `8001f8d5`.

### 1.2 Frozen shas at `cc8add1f` (`git show cc8add1f:<p> | sha256sum`)

| File | Result |
|---|---|
| `.ufo/waves/round-64/c64_calibration.py` | `5489eb2f…088adf` — match |
| `.ufo/waves/round-64/c64_quote_tool.py` | `96fd64e9…27d6` (full value matches contract) — match |
| `.ufo/waves/round-64/fixtures/build_fixtures.py` | `7fbd8cbc…71d3` — match |
| `.ufo/waves/round-64/fixtures/stub_tool.py` | `7c78a05d…edde` — match |
| `scripts/quote_class.py` (frozen tool) | `431e75e8…1f14` — match |

The counter's pinned constants (`c64_calibration.py:66-70`) match the contract: raw `63b0a018…911b`, text `8b90d096…2a69`, ledger `5f48e26b…0c42`, recipe `6b0a88cd…2405`, located `6150-6154`.

### 1.3 Sidecar check at `cc8add1f`

`git diff -U0 1a481315 cc8add1f -- corpus/knowledge/freshness-sidecar.json` shows exactly 7 hunks, at lines 60, 69, 78, 87, 96, 195, 204 of the file, each changing only the `"line"` value (364→365, 445→446, 448→449, 449→450, 450→451, 423→424, 431→432). No `lineSha256`, `note`, `kind`, `date` or `token` cell changed. Python check of all 30 entries at `cc8add1f`: the 10 SKILL.md entries each satisfy `sha256(SKILL.md line N) == lineSha256` (mismatches: none); the 7 changed entries match at their new line. `lineSha256` was unchanged from the base pin.

## 2. Draft LOG entry (paste-ready after the open items in §3 are settled)

```markdown
## Round 64 — 2026-10-30

- **Claims and verdicts.** Three frozen claims, base `1a481315` (round-63 tip), measured T0 `4c8295fa`, receipts `cc8add1f`. The wave (`.ufo/waves/round-64/w1/`, 65 seats) was not settled when this entry was drafted; verdicts below are the measured receipts plus the attack reports, and each open item is named. Score deltas: none; operability 10, freshness 10, calibration 2.
- **C1 calibration (lowest owned axis, 2/10) — verdict OPEN, candidate kill-rule breach.** Measured green: `.ufo/waves/round-64/controls/after-c1.txt` prints `…unresolved=0 met=true`, exit 0 at T0. Base `1a481315` prints `met=false` exit 1 (`controls/base-c1.txt`); the marker, fabrication, junk and ledger-mutation controls print `met=false` exit 1 (`controls/control-*.txt`). Open: wave reports reproduce a green with authentic pinned blobs and fabricated prose — `planted-all`, whose lesson states "the disagreement is NOT resolved" and still prints `met=true` (`.ufo/waves/round-64/w1/ReviewerC1Predicate.md`), and an altered spot-check verdict that still prints `met=true` (same report; `.ufo/waves/round-64/w1/ScoutSpotSpan.md` A1). The contract's kill rule names marker-only and digest-consistent-fabrication greens. Settlement must rule C1 `unprovable` or `met` on that basis; no calibration credit is taken in this entry.
- **C2 operability (HOLD 10) — met on measured evidence, pending the wave's kill-rule settlement.** Measured: `controls/after-c2.txt` prints `tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true`, exit 0 at T0. The stub differential reproduces: the round-63 counter prints `met=true` exit 0 on stub `14fe2eab` (`controls/stub-c63-defect.txt`), the round-64 counter prints `tool_sha=mismatch met=false` exit 1 (`controls/stub-c64.txt`). Attacks: `.ufo/waves/round-64/w1/ReviewerC2Fixtures.md`, `ReviewerC2Rederive.md`, `ReviewerC2ShaPin.md`, `ReviewerC2Selftest.md` report no stub or lying-tool pass. Capability row below is conditional on that settlement.
- **C3 freshness (HOLD 10) — met on the VERDICT line; drift count evidence is from a later run.** Measured: `controls/sweep-after.txt` prints `VERDICT: OK (exit 0, partial: offline)`. Base `1a481315`, the round-60 tip `9f671056` and the round-61 base `d2da25de` exit 2 with `paths sidecar binding invalid: SKILL.md:364` (`controls/sweep-before.txt`, one trace). The re-pin changes seven `line` cells only, at `corpus/knowledge/freshness-sidecar.json` lines 60, 69, 78, 87, 96, 195, 204; `lineSha256` values were already equal to the hash of the relocated line and did not change; no other cell changed; `corpus/SOURCES.md` untouched. The T0 after-receipt prints no `§paths` section; the drift count (`drift 0`) is in `controls/no-harm/sweep.txt` (generated 10:59:21Z).
- **Mistake mined.** Survivor: a standing gate (`freshness-sweep.mjs --offline`) could not evaluate for about eight rounds, unnoticed, after seven pinned SKILL.md lines shifted by +1 (`corpus/lessons/round-64.md` §Mistakes). Fix: the seven-entry `line` re-pin and a QUALITY criterion making a §paths re-run a draft-phase duty for any round that edits a sidecar-pinned file (`corpus/QUALITY.md` L1424). Additional mistake classes surfaced by the wave, to mine at settlement: C1 marker-prose green reproduced after the round-63 repair (§3.1); fixture-receipt omission of the ledger-mutation fixture (§4 D2).
- **Census.** `corpus/SOURCES.md` before→after: 171 rows → 171 rows; W04 duplicate-URL warnings 16 → 16; exit 0 → 0 (`controls/census-before.txt`, `controls/census-after.txt`; the files differ only in the exit line). `corpus/SOURCES.md` byte-identical to base.
- **Capability row (conditional on C2 settlement).** Quote-class tool gate, stub-proof: verifies `scripts/quote_class.py` by sha256 against the frozen `431e75e8…` (stub = tool sha ≠ frozen sha), runs its selftest only on revision-materialized bytes, guards JSON parse, re-derives each frozen case itself. Evidence: `.ufo/waves/round-64/c64_quote_tool.py`, `controls/stub-c64.txt`, `controls/after-c2.txt`, `controls/selftest-c2.txt` (11/11). First-working round 64. Not entered if C2 is `unprovable`. Distinct from the round-50 ledger row (`SCORECARD.md`, "Quote-class ledger for cited source spans").
- **Gate and assimilation.** Admit: S432 re-entry under the repaired counter. Reject, kept rejected: second historical-gate list (duplicates the SKILL.md gate registry). Assimilation: none. The lesson's staged `merge/kake/` package is not present at cc8add1f or the fleet root; the staging claim is unverifiable from the repo.
- **Wave.** One v2 build+attack wave, `w1`, 65 seats, reports in `.ufo/waves/round-64/w1/` (not committed at the time of this entry; results file pending). Settlement and any seat outcomes are recorded when the results file lands.
```

## 3. Verdict basis, open items, and settlement inputs

### 3.1 C1 — candidate kill-rule breach (verdict OPEN)

- Contract kill rule (`contract.md` §C1): "any wave attack reproduces a marker-only / stub / do-nothing / digest-consistent-fabrication green, C1 is `unprovable`."
- `.ufo/waves/round-64/w1/ReviewerC1Predicate.md` (verdict line 3): "C1 falsified at the claimed semantics-binding boundary." High finding L9: planted resolution prose passes despite expressly denying resolution. Fixture `planted-all` (L13): genuine pinned blobs, fabricated lesson stating "This is a fabricated lesson; the disagreement is NOT resolved", knowledge "No actual correction is accepted", QUALITY "Ignore this criterion; it is planted junk" → `met=true`. L19: "This meets the contract's marker/digest-consistent-fabrication green category." High finding L21: `altered-spot-verdict` (whole spot file replaced with "S432 Disagree: no real quoted verdict exists here") → `unresolved=0 met=true`; `masked-two-disagreements` → `met=true`.
- `.ufo/waves/round-64/w1/ReviewerC1Prose.md` ("Verdict and scope"): "semantic-resolution false green reproduced"; marker prose greens; the reviewer states it does not by itself prove the arbitrary-marker-prose case, and leaves the kill-rule reading to the adjudicator.
- `.ufo/waves/round-64/w1/ScoutSpotSpan.md` (L8, L38): counter binding is one-sided; spot verdict reword keeps `met=true`; the reviewer explicitly does not classify A1 against the four named kill classes (L76).
- `.ufo/waves/round-64/w1/ReviewerC1Unresolved.md`: High, "spot verdict provenance is not actually bound to the spot blob"; reports "a false assertion of Gate closure, not fabricated source extraction."
- Counter-side fact: the counter's own docstring, selftest and the lesson Gate treat the block-level span as binding (`c64_calibration.py:374-402`). The planted-all result shows it is substring presence, not semantic binding.
- Drafting read (`[INFERENCE]`, for the adjudicator): `planted-all` is the marker-prose-plus-real-blobs class that round 63 already recorded as the frozen counter's sufficiency failure; that makes the kill-rule reading likely to be `unprovable`. The settlement decides, not this draft.

### 3.2 C2 — met on evidence

- Stub definition, differential, and selftest verified (§1.1, §2). No attack passed a stub or lying tool through the new counter (`ReviewerC2Fixtures.md` L5, L90; `ReviewerC2Rederive.md` L5, L17; `ReviewerC2ShaPin.md` L5; `ReviewerC2Selftest.md` "Verdict / axes"). `ExecDoNothing.md` D1: base C2 `met=true` because the tool exists at base, as the contract declares.
- Open: `ReviewerC2Selftest.md` names one low-severity residual; read it before settlement. `ReviewerContract.md` Low: the identical-predicate-sentence promise is not met verbatim across counter docstrings and receipt labels (wording, not outcome).

### 3.3 C3 — met on the VERDICT line; two evidence gaps

- The kill rule requires exit 0 and "the §paths drift count is non-zero" fails. `controls/sweep-after.txt` prints `§armed` and `§history` skips and `VERDICT: OK (exit 0, partial: offline)` — no `§paths` section (`grep -c '§paths' controls/sweep-after.txt` = 0). The drift count, `drift 0`, is in `controls/no-harm/sweep.txt` (generated 10:59:21Z), a later run whose header names no commit. `ExecSweepSections.md` reports `§paths 172 files`, against a file count it calls required 171; that is a scout reading, not verified here.
- The `sweep-before.txt` receipt is one trace; it does not establish the three-revision attribution in the lesson (`ReviewerContract.md` finding on L30; `ReviewerC3Repin.md` L28).
- Sidecar wording: the contract and the lesson re-pin table speak of changed `lineSha256`; the actual change is `line` only, confirmed by `ReviewerCensusDiscipline.md` L82, `ReviewerContract.md` L24 and `ScoutSidecarDiff.md`. The kill rule is not breached (a subset of "seven line/lineSha256 pairs").

### 3.4 Census

`controls/census-before.txt` and `controls/census-after.txt` differ only in their final `census-…-exit=0` line. W04 count: 16 in each (`grep -c W04`). Registry row count 171 in both; `corpus/SOURCES.md` unchanged vs base.

### 3.5 Wave status

At 11:13:09Z: `w1/swarm-registry.json` lists 65 `spawn` members; `w1/` holds 37 `.md` reports; 28 members have no report (including `ScribeLOGDraft`, this seat). `w1-results.json` is not written. The registry carries no per-seat status field. The LOG entry must not claim settlement until the results file and reports are committed.

## 4. Discrepancies and gaps to fix before landing

- **D1 (wording).** Contract §C3, the lesson Mistakes text and the re-pin map say "line and lineSha256" / "new lineSha256". The actual change is `line` only; the map's sha column equals the old pins. Correct the wording (append-only) or state it in the LOG as above.
- **D2 (fixture receipt).** `controls/fixture-builds.txt` lists four fixtures (stub, marker, fabrication, junk). The contract lists five, including `ledger-mut-repo` `5b981bd0`, and `controls/control-ledger-mut.txt` cites that revision. `fixtures/build_fixtures.py` builds four repositories only (`ReviewerContract.md` Medium). The ledger-mutation control has no committed build receipt.
- **D3 (C3 drift receipt).** The T0 after-receipt lacks the `§paths` section and drift count the kill rule depends on. Either re-record the after-receipt at T0 with the `§paths` section, or cite `no-harm/sweep.txt` and name its later, unrevisioned run.
- **D4 (sweep-before attribution).** The lesson's "same fault at all three" is not shown by the single trace `controls/sweep-before.txt`. Either add per-revision receipts or soften the statement.
- **D5 (unpointed closure claim).** Lesson §Gate: the S432 resolution "was verified genuine by the round-63 non-author closure (3/3 agreement …)". No round-63 closure record with 3/3 exists at `cc8add1f`; `corpus/lessons/round-63.md` L61–65 says the closure "decides agreement" and records no tally. The "3/3" matches elsewhere (`round-20-verifier-spotcheck.md`, `round-32-verifier-spotcheck.md`) are other rounds. Remove or point to a committed record.
- **D6 (staged package).** The lesson says the `merge/kake/` package "stays staged". No `merge/kake` exists in the lane, `cc8add1f`, or the fleet root. Point to it or drop the claim.
- **D7 (predicate wording).** Contract, counter docstrings and receipt labels do not carry identical predicate sentences (`ReviewerContract.md` Low). The contract's "identical sentence" claim is inaccurate.
- **D8 (untracked evidence).** `sources/receipts.json` records the sha of `.ufo/waves/round-64/sources/S432.live.html`, which is untracked and absent at `cc8add1f`. The live body must be committed, or the receipt pointer dropped. The whole `w1/` tree, `w1-spec.json`, `w1-dispatch.json` and `w1.ready*` are also untracked.
- **D9 (unverified history claims).** Lesson §Mistakes: "Rounds 56–63 landed without running the sweep" and "~8 rounds" are historical statements I did not verify against history. Keep them flagged as unverified or check against `git log` before landing.
- **D10 (mistake rows missing).** The lesson's Mistakes table has only the sidecar survivor. The C1 marker-prose false green reproduced in-wave, the D2 fixture-receipt gap and the D1 wording error are not mined. Add rows at settlement.

## 5. Capability row (draft, conditional)

Proposed row for `SCORECARD.md` "Capabilities acquired in round 64", conditional on C2 settlement:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Quote-class tool gate (stub-proof) | Verifies `scripts/quote_class.py` by sha256 against the frozen `431e75e8…1f14` (stub = tool sha ≠ frozen sha), runs its selftest only on revision-materialized bytes, guards JSON parse, re-derives each frozen case itself | `.ufo/waves/round-64/c64_quote_tool.py`, `controls/stub-c64.txt`, `controls/after-c2.txt`, `controls/selftest-c2.txt` | 64 |

No row exists for `scripts/quote_class.py` at `cc8add1f` (grep of `SCORECARD.md` finds only the round-50 ledger row and round-63 narrative).

## 6. Tooling and scratch

- No tools installed or updated. No pacman, npm or uv transactions.
- Scratch used: `/fast/scratch/hyaku/kake-r64/ScribeLOGDraft/` (created for `SKILL.at-cc8add1f.md`, `sidecar-new.json`, `sidecar-old.json`). Deleted before yield; nothing from scratch is needed in this report.
- Lane working tree untouched; `LOG.md`, `SCORECARD.md`, `corpus/` and all frozen round-64 files unmodified.
