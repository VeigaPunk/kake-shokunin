# ReviewerCrossClaims

## Claim surface map

| Claim | Primary writes | Counter reads | Cross-claim contact |
|---|---|---|---|
| C1 | `scripts/receipt_lineage.py`, `.ufo/receipt-disclosures.json`; historical population list is frozen under `controls/` | No C1 counter is present in the committed round-61 tree: `git ls-tree -r HEAD` lists only `c61_header_cases.py` and `c61_recheck_pins.py`. `w1/ExecC1Counter.md` says implementation incomplete/not run. | No executable frozen C1 counter available to establish its declared `SCORECARD.md`/`SKILL.md` dependencies. |
| C2 | `scripts/response_snapshot.py`, `scripts/header_audit.py`, capture receipts/manifest; intended S430–S433 appends and Gate citations | `c61_header_cases.py` reads the committed C2 tool and round-61 capture tree/manifest. Search of implementation found no reads of `SOURCES.md`, lesson, recheck, disclosures, scorecard or C1 controls. | C2 registry append shares `corpus/SOURCES.md` with C3's due-cell edits; C2 capture data is separate. |
| C3 | S001–S010 recheck cells, `.ufo/waves/round-61/recheck/` evidence, `corpus/lessons/round-61.md` Gate records | `c61_recheck_pins.py` declares and reads `corpus/SOURCES.md`, the round-61 lesson and recheck bodies/receipts. It does not read C2 capture or C1 disclosure/control surfaces. | Its registry parser sees appended rows, but C6 compares only base-row IDs; implementation lines 650–671 permit added IDs. Its Gate lookup is keyed to the due-row ID, so unrelated C2 Gate lines do not satisfy or replace a C3 Gate line. |

## Separability result

The shared registry file is a real shared mutation surface, but the mutation regions and counter invariants are explicitly separable: C2 adds rows with new IDs, while C3 checks all base rows, permits added IDs, and limits each changed due row to its recheck cell (C3 counter lines 650–671). The contract's shorthand that C3 reads only the due cells is not literally exhaustive: the counter parses the registry and reports appended rows, and its due-set calculation uses registry rows. However, C2's new rows have later opened dates per the contract and do not enter the frozen oldest-ten due set; C6 explicitly allows appends. This is a bounded, declared observational dependency, not a causal failure of C3's predicate.

The lesson is also a common write target, but `gate_line(lesson, sid)` selects a bullet/table row by exact due ID (lines 260–268), so C2 S430–S433 rows cannot stand in for or disrupt a C3 S001–S010 Gate record absent unrelated Markdown restructuring. C1, C2, and C3 tools are distinct scripts; the C2 counter's source search is capture-scoped and the C3 counter's source search is registry/lesson/recheck-scoped. No counter-to-counter call or C1 disclosure dependency was found in those two committed counters.

There is an independent integration gap relevant to interpreting this audit: at HEAD `f5a9b8a`, `corpus/SOURCES.md` and `corpus/lessons/round-61.md` are not committed changes (the latter exists only untracked); the worktree has modified `SOURCES.md` and untracked `recheck/S010.html`, `sources/S432.html`, and `sources/S433.html`. Thus this is not yet an audit of an integrated measured after-state. The lack of the C1 counter also prevents an end-to-end C1 dependency test. I did not treat these as proof of a cross-claim coupling.

## Residual risk and verification gaps

- The contract's strong C1 isolation claim cannot be empirically validated until the specified C1 counter is integrated; the w1 report explicitly records it as incomplete.
- C2/C3 and their shared-file integration cannot be assessed at a final measured revision because registry/lesson edits and the noted evidence files are not committed at current HEAD. The C3 counter's allowed-append implementation does, however, avoid an inherent C6 collision.
- The worktree's untracked/modified artifacts are not attributed to a particular writer here; no lane files were changed by this audit except this report.

VERDICT: No demonstrated predicate-breaking cross-claim dependency in the committed C2/C3 counters; shared SOURCES.md and lesson writes are structurally ID/append separated, but final integration and C1 separability remain unverified (C1 counter absent).