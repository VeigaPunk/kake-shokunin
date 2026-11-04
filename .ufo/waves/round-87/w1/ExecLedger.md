# ExecLedger — round 87 single v1

## Axes and result

Calibration: lowest axis 2 HOLD; candidate implements only the frozen eight-row agreement ledger. Freshness: 10 HOLD, untouched by this seat. No global score/admission judgment.

Candidate: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecLedger/gate-agreement-ledger.json`

SHA-256: `ef58f9092c32179de6e680ab782cfb29900d9b5b34cfbfcb76b316a144c3d506`.

I opened each historical snapshot's gate table independently. The retained probe separately parses those tables and constructs candidate rows from their cells, not from EXPECTED. Explicit normalizations: `admit/mined` and `admit (A)` → `admit`; `reject proposition` → `reject`; bold `**agree**` → `agree`. All eight complete normalized rows equal the frozen expectation. Counts: source rows 3/2/3; missing 0; row disagreements 0; extras 0; historical outside-disagree judgments 0.

| Round | Source lines | Row identities | Snapshot SHA-256 |
|---|---|---|---|
| 84 | 73–75 | S457 response max-age semantics; §4.1 normalization as response-directive reorder proof; §5.2.2.2 as max-age anchor | `80f48887b1e5f2e9d7d54adcce19d8b935f77fc0b236620abac3335b730dfda9` |
| 85 | 71–72 | S458 field-specific algorithm; Blanket response-policy reorder equivalence | `948c316831d0c71927e6a29501f05037b3faa940a251984ed28ca8f0eee2ce71` |
| 86 | 89–91 | S459 CrUX Vis docs; S461 RFC 9111 slice; RFC 7234 minimum-duplicate attribution | `47499686bc976564c43174fdeeae2219e0db2351c571678ba35caff0a34de42b` |

All source paths are under `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/snapshots/`, named `round-84-verifier-spotcheck.md`, `round-85-verifier-spotcheck.md`, and `round-86-verifier-spotcheck.md` respectively. Full original table lines, line numbers, normalized rows and digests are retained in receipts.

## Exact checks and receipts

Executed command, exit 0:

`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecLedger/probe.py`

Cwd: `/fast/scratch/hyaku/kake-r87/ExecLedger`.

The probe retained each subprocess's exact argv, cwd, exit, stdout and stderr at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecLedger/receipts.json`. Five read-only `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 58fee726102aa89ad2c1fa9f697869de3a212510:<path>` calls exited 0 and matched current bytes for count.py, expected-ledger.json and all three snapshots. Exact paths and complete returned bytes are in that receipt. No frozen input was changed.

Nested command, exit 0:

`/usr/bin/python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/count.py --selftest`

Output: `selftest 6/6: clean, empty, missing, altered, duplicate, tampered`.

The instrument was imported read-only with bytecode disabled. Independent mutations operated on deep-copied candidate rows, not frozen EXPECTED:

| Case | Instrument mismatches | Result |
|---|---:|---|
| Clean candidate | 0 | passes |
| Omit round-85 S458 row | 1 | fails |
| Change round-85 blanket-equivalence outside agree → disagree | 1 | fails |
| Wrong digest on round-86 S461 row | 1 | fails |
| Duplicate round-86 RFC7234 row | 2 | fails |
| Supply wrong actual source bytes through read callback | 8 | fails |

Mutation failure means `ledger_errors > 0`, the frozen C1 rejection condition; these are imported-function calls, not separate CLI processes with invented exits. No production revision gate, build, lint, formatter or unrelated test ran.

Scratch commands: `mkdir -p /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecLedger /fast/scratch/hyaku/kake-r87/ExecLedger`, exit 0; `rmdir /fast/scratch/hyaku/kake-r87/ExecLedger`, exit 0. No clone created. Scratch removed after retaining receipts. No installations, services, provider probes, credentials, network reads, commits, pushes or production writes. LSP is unavailable in this seat's mounted tool interface; no symbol refactor was needed.

## Limits and unsound-premise disclosure

The target is deliberately exposed, finite and self-assessment only. Exact reproduction measures transcription/consistency, not calibration across unseen decisions. A copied false table or curated all-agree sample can pass; source digests pin bytes, not truth, completeness of historical sampling, authenticity, or source semantics. This seat independently compared all snapshot gate tables, but did not re-open their primary URLs or certify their historical judgments. The zero missing/disagreement result is therefore not independent domain admission, not closure of D84-2/3/4, and not universal agreement evidence. A duplicate counts two mismatches under this instrument, not two independently false historical decisions.

The snapshot boundary and expected rows were frozen before this seat's work and remain unchanged. Candidate is not integrated: L1 alone owns production placement and post-integration revision measurement. No blocker within the assigned candidate scope.

## Retained files and handoff

Only this report and the following files were written:

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecLedger/gate-agreement-ledger.json`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecLedger/probe.py` — retained reproducible bounded probe, not production code.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecLedger/receipts.json`

After integrating, L1 should run the frozen C1 revision counter against its carrier; that production-revision result was not exercised here.

Self-evaluation (not admission): accuracy 4 (snapshot consistency only, no primary-source certification); completeness 4 (all requested candidate checks, integration reserved for L1); clarity 4 (full receipts intentionally verbose); actionability 4 (candidate ready, carrier check remains L1-owned); conciseness 4 (exact evidence adds length). Overall 4.0/5. Highest-impact safeguard: retain the finite-self-assessment label in production documentation.
