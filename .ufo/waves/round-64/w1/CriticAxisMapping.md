# CriticAxisMapping — round 64

Scope: axis mapping of C1/C2/C3 at measured T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`; receipts commit `cc8add1fa740b920ea5179a71152680ab220c70c`. This is a critic's finding/recommendation, not admission, integration, or canonical judgment.

## Findings per claim

| Claim | Actual surface | Scoped verdict |
|---|---|---|
| C1 calibration | Integrity and auditability of the S432 disagreement-resolution record: genuine retained bytes, recipe output, class and location; lesson prose acknowledging an outside disagreement. | Calibration-relevant target, but the measured green does **not** establish improved self-assessment quality. Strongest counterexample below shows the claimed actual-outside-verdict binding is absent. Do not equate instrument integrity with new independent agreement. |
| C2 operability | Stub rejection and revision-local verification of an existing quote-class tool's four-case selftest. | Correct axis. The C2-specific round-63 hardening conditions are visibly implemented. However, the claim that the quote-class **capability row re-entered** is not borne out at T0: only a counter row was added. Eligibility to re-enter is not actual registry entry. |
| C3 freshness | Recovery of the standing offline paths drift detector from could-not-evaluate to evaluating. | Correct, bounded freshness mapping: detection is demonstrably restored, not just an error suppressed. No whole-corpus/current-world freshness verdict follows; armed/history checks remain skipped. |

Scores are not evidence of these moves: `SCORECARD.md` is byte-unchanged base→T0. A HOLD-10 axis can have a bounded capability restoration without a scalar increase. Conversely, selecting the lowest score does not make instrument work calibration automatically.

## C1: strongest counterexample — false actual-verdict binding

Absolute source references:

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:193-198` reads the spot-check only to count lines containing `S432` and `Disagree`.
- Same file `:253-259` checks `SPOT_VERDICT_SPAN` against the lesson Gate, not against the actual reason in the spot-check file.
- Same file `:267-270` derives `unresolved` by subtracting one when that lesson presence gate passes. This is not an independently observed resolution verdict.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-61-verifier-spotcheck.md:33` holds the actual original reason.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/base-c1.txt:1-3` already records pins=1, recipe_rederive=1, class_match=1, located=6150-6154, quote_correction=1, criterion=1, source_row=1 at base. Only lesson_gate=0/unresolved=1 distinguishes that base from after. This is re-entry of old correction evidence under a new instrument, not a newly observed correction or agreement.

Attack fixture was made from `git -C /home/vgpnk/Projects/shokunin/kake-shokunin archive --format=tar 4c8295fa5e3b628f1fdf3840299ae415c01849fb`, extracted beneath `/fast/scratch/hyaku/kake-r64/CriticAxisMapping-2/`. No lane files were changed. Fixture repo top-level printed `/fast/scratch/hyaku/kake-r64/CriticAxisMapping-2/spot-attack` before its first commit. Fixture revisions below are scratch-local, not lane revisions.

Mutation A changed only the outside reason's text, preserving its S432 row and Disagree verdict:

```
is only a generic lead-in, not substantive evidence for a response-header expectation.
→ is a well-formed sentence with no defect worth recording.
```

The exact mutation operation was `s.replace(old, 'is a well-formed sentence with no defect worth recording.')`, with `assert s.count(old)==1`, on `corpus/lessons/round-61-verifier-spotcheck.md`. Neither the frozen counter nor lesson nor pinned blobs were changed.

Command, run from that scratch fixture:

```
TMPDIR=/fast/scratch/hyaku/kake-r64/CriticAxisMapping-2/tmp python3 -B .ufo/waves/round-64/c64_calibration.py --root . --revision 1fcb5c98088956f267fc0dd95a084ff8cf11213e
```

Exact output and exit:

```
revision=1fcb5c98088956f267fc0dd95a084ff8cf11213e disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

Negative comparator B restored the original reason and changed the one `| Disagree |` cell to `| Agree |`:

```
TMPDIR=/fast/scratch/hyaku/kake-r64/CriticAxisMapping-2/tmp python3 -B .ufo/waves/round-64/c64_calibration.py --root . --revision b22c4a5e5d8421fed455c0f170325c8177a722fa
revision=b22c4a5e5d8421fed455c0f170325c8177a722fa disagreements=0 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
```

Tool call exited 1. Thus the row's disagreement token is enforced, but its actual reason is not. This is a provenance-binding counterexample, not a demonstration that the real S432 sentence is false, nor a marker-only/digest-fabrication kill-rule reproduction. Do not extend it to those stronger claims.

The real substantive outside evidence exists separately: `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-63-verifier-spotcheck.md`, §Discernment spot-check, explicitly agrees with the field-purpose span and says the round-61 disagreement is resolved. That supports the calibration relevance of the target; it predates this round and is not consumed by the new counter. No new self-assessment agreement rate was measured here.

**Impacted axes:** calibration; operability of its evidence-binding instrument. **Smallest safe correction for a future frozen instrument:** bind the actual S432 row/reason from the non-author spot-check (or pin that authoritative artifact), require the lesson to quote that same row's reason, and reject the rewritten-reason control. Keep byte-presence/classification evidence distinct from substantive-support agreement. A stronger semantic claim needs an outside adjudication, not a second lane-authored authority. Do not repair this round's frozen counter or relabel its receipts after scoring.

## C2: proper axis, but re-entry claim overstates the registry state

`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-63.md:129-139` conditions future re-entry on the named repairs. The C2-specific conditions are implemented in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py`, function `evaluate`: reject sha mismatch before execution; materialize tool and fixtures from revision blobs; execute the materialized selftest; guarded JSON parsing; counter-side class re-derivation. This is bounded operability work. The tool itself is unchanged and already exists at base; the stub differential, not tool introduction, is the meaningful before/after.

Existing receipts (read, not independently re-executed by this seat):

- `.../.ufo/waves/round-64/controls/stub-c63-defect.txt:1-3`: old counter on stub prints `present=1 selftest=4/4 frozen_cases=ok met=true`, exit 0.
- `.../.ufo/waves/round-64/controls/stub-c64.txt:1-3`: new counter prints `tool_sha=mismatch ... met=false`, exit 1.
- `.../.ufo/waves/round-64/controls/after-c2.txt:1-3`: T0 prints `tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true`, exit 0.

Exact inspected command:

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- SKILL.md
```

It adds exactly two registry rows, at `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:1363-1364`: `calibration-counter` and `quote-tool-counter`, both **gate** entries. There is no `scripts/quote_class.py` entry command for users. Searching that script path at T0 returned only the older `c50_quote_class.py` substring match and the new calibration row's explicit statement that it never gates on `scripts/quote_class.py`. Neither is a tool capability row. SCORECARD also has no diff.

**Impacted axes:** operability and capability-record accuracy. **Smallest safe correction:** describe the landed item as a stub-proof gate, not an already re-entered tool row. If a tool capability row is wanted, enter the real tool's command, exit contract, write scope and bounded four-case proof through the authorized integration process. Do not infer that a future permission has already been exercised. The C1 provenance defect above also means the complete combined repair recipe should not be represented as conclusively satisfied merely because C2's specific repairs landed. Canonical judgment owns the admission consequence.

## C3: restoration is real, bounded freshness work

Exact inspected diff command:

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- corpus/knowledge/freshness-sidecar.json
```

Output changes only seven `line` values by +1. All seven lineSha256 values remain unchanged: the content moved, not the annotated facts. The contract's permitted line/lineSha256-pair scope therefore includes the actual narrower change. Thirty sidecar entries exist; all ten SKILL.md entries were checked against SHA-256 of their current line bytes and printed OK.

Read-only archive runs (not lane-root writes):

```
cd /fast/scratch/hyaku/kake-r64/CriticAxisMapping-2/tree-base
TMPDIR=/fast/scratch/hyaku/kake-r64/CriticAxisMapping-2/tmp node scripts/freshness-sweep.mjs --offline
```

Base archive exits 2. Captured first line: `freshness-sweep: Error: paths sidecar binding invalid: SKILL.md:364`.

On T0 archive, same command from `.../tree` exits 0. Relevant exact output:

```
§paths  172 files · 679 occurrences · 106 unique tokens
  resolve 31 · declaredAbsent 65 · drift 0 · unresolved 10
  set-delta miss: no new miss
VERDICT: OK (exit 0, partial: offline)
```

The 65 missing paths already occur in `freshness-pins.json`'s `pins.pathsMissSet`; comparing them to an old round-20 count of 55 would use the wrong baseline. The 56-entry pinned file set is informationally stale relative to 172 current scanned files; the sweep nevertheless scans those files and applies the miss-set gate.

Strongest counterargument tested: perhaps re-pinning merely suppresses errors and leaves detection dead. It does not. On the same T0 archive, with an empty scratch HOME:

```
HOME=/fast/scratch/hyaku/kake-r64/CriticAxisMapping-2/fakehome TMPDIR=/fast/scratch/hyaku/kake-r64/CriticAxisMapping-2/tmp node scripts/freshness-sweep.mjs --offline --section=paths
```

Relevant output:

```
§paths  172 files · 679 occurrences · 106 unique tokens
  resolve 1 · declaredAbsent 74 · drift 21 · unresolved 10
VERDICT: DRIFT — §paths: 21 unannotated miss · 30 NOT in pins.pathsMissSet (exit 1, partial: offline)
```

Captured sweep process exit was 1. The fake-HOME selftest also printed `selftest: 36/36 passed`; that command was piped through `tail`, so its shell pipeline exit 0 is not an independently captured Node exit. The printed selftest total is the evidence.

**Impacted axis:** freshness, specifically local path-citation drift detection. The re-pin mechanism is bookkeeping, but the restored observable detection is not merely bookkeeping. **Smallest safe correction:** retain the narrow label "offline §paths detection restored" and the explicit skipped sections. The round-64 QUALITY criterion requiring a sweep when a sidecar-pinned file is edited is a relevant recurrence guard; no new content-addressed framework is needed to justify this bounded restoration. Do not call this a fresh whole-corpus verdict.

## Provenance, limits, cleanup

Frozen instrument SHA-256s independently read with `sha256sum` matched the assignment: C1 `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf`; C2 `96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b`; tool `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14`.

No tools installed or updated. Node reported v24.21.0. All temporary archives, fake HOME and fixture repo were beneath the seat's scratch tree and removed before yielding. No lane counters, receipts, lesson, contract or tracked source files edited; this report is the only retained write. Fixture commits are local scratch evidence, not lane commits or published artifacts. The attempted sidecar-only/base follow-on run did not execute after the base failure; no result for that extra experiment is claimed.

Self-evaluation: accuracy 4/5 (claims distinguish re-executed attacks from read receipts; no independent replay of C2 differential); completeness 4/5 (all three mappings covered, no general adversarial audit claimed); clarity 4/5 (separates mapping from admission, long evidence section); actionability 4/5 (names minimal binding/registry corrections, not a redesigned system); conciseness 4/5 (exact receipts retained at some length). Overall 4.0/5. Main improvement would be a separately frozen C1 actual-reason binding control; it must not be retrofitted into this round. User should agree that these are scoped review findings, not canonical verdicts.
