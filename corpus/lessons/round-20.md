# Round 20 attempt — citation-local absence evidence

Date: 2026-10-15. One interactive L1, lowest LIVE axis tie resolved to
freshness. Status: **blocked / unadmitted**; zero new verified-round credit.
The preceding headless launch counter 16 is not a completed-round count.
Round-19 history through `20d13115323fba21bb3d63204cce13425feaf399` is preserved.
See the appended round-20 reconciliation in `LOG.md` and
`plans/wwkd-round-20-citation-locality.md`.

## Trigger → action → outcome

Round 19's re-census lesson names stale publishing-tool instructions. The
inherited scanner patch addresses the cause: target-wide OR allowed a
historical note to hide an unannotated citation of the same deleted target.
The interactive L1 retained the per-citation evidence sets, simplified the
new diagnostic, and removed an incidental first-evidence ordering assertion
from the inherited regression case. Path grammar, local annotation windows,
strict mode, pins, history and publishing gates are unchanged.

The actual CLI was run against isolated publishing fixtures on both the
committed baseline and candidate. Full argv/stdout/stderr/exit records:
`.ufo/round-20/baseline-proof.json` and
`.ufo/round-20/candidate-proof.json`. Input bytes, digests and expected
findings: `.ufo/round-20/frozen/citation-locality/expected.json`.

| Case | Baseline exit | Candidate exit | Observable |
|---|---:|---:|---|
| Mixed annotation, already-pinned miss | 0 | 1 | Only `SKILL.md:3` is unannotated; no new miss-set member. |
| All occurrences annotated | 0 | 0 | Declared absence remains exit-neutral. |
| Existing target, mixed prose | 0 | 0 | Target resolves; annotation does not override existence. |
| Distant occurrences in one file | 0 | 1 | The unannotated location is `SKILL.md:9`. |
| Home-alias spellings | 0 | 1 | One canonical target, exact unannotated location. |
| Brace-expanded targets | 0 | 1 | Both expanded targets retain their unannotated originating location. |
| Strict local annotation mode | 0 | 1 | Direct historical evidence elsewhere cannot hide the unannotated occurrence. |

Human CLI smoke also reported `1 of 2 cites unannotated: SKILL.md:3` and
`VERDICT: DRIFT — §paths: 1 unannotated miss · 0 NOT in pins.pathsMissSet (exit 1, gates inert)`.
The fixture intentionally pins only the checks under study; the inert-pin
warning is retained, not removed from the evidence.

## Gate

Candidates considered:

- **Locally admitted implementation fact:** missing-target annotation
  coverage must hold at every citation location. Both controls stayed clean;
  exact finding locations are observed in the CLI evidence.
- **Locally admitted quality criterion:** a pinned missing target is not an
  exemption for a newly unannotated instruction. Added to `corpus/QUALITY.md`.
- **Rejected:** restore green by re-pinning old misses, borrowing absence
  evidence across occurrences, or declaring deleted tools executable.
  These do not address the reproduced false-green.
- **Rejected:** treat canonical plan/render success as a dispatched wave or
  native judgment. `.ufo/round-20/wave/validation.json` records 32 distinct
  scopes, 32 leading Godspeed invocations, zero native task calls, and no
  registry persistence. No route mutation or substitute dispatch occurred.

Outside spot-check: **unavailable**. No independent non-author verifier has
reviewed an admit and reject. No promotion box or discernment improvement is
claimed. The local code evidence is not full round admission.

## Named debt and unblock

- **Dispatch / host owner:** bind existing content roles to `@m_composer`,
  audit roles to `@m_grok`, connector to `@m_antigravity` with `@m_zfl`
  fallback, outside this lane's write authority. Effective observations and
  exact mismatches: `.ufo/round-20/routing-blocker.json`. Then a fresh session
  may dispatch the saved complete canonical wave; never a shortened wave.
- **Corpus / kake:** use P1's unannotated-location diagnostics to qualify or
  repair the stale recipes without blanket markers or miss-pin suppression.
  The retained local annotation heuristic still permits unrelated words
  within its ±2-line window; this round does not claim semantic freshness.
- **Publishing-source / operator:** restore or explicitly retire the deleted
  PQ-2/PQ-14 source watches. **History / operator:** restore a surviving
  history source or explicitly end the old probe-timer era. No current live
  HTTP state was measured under this local-only dispatch.
- **Static self-source proof / kake:** round-19's independent audit already
  reports a confinement-assertion weakness. It was not re-probed or repaired
  here; a passing selftest is not a complete write-free proof.
- **Receipt / integrator:** a Sighting run/session identity is known, but no
  applicable queue task/expected receipt binding has been supplied by this
  interactive dispatch. Do not invent one or call Sighting `complete`.

## Local acceptance measured after integration

`node .ufo/round-20/replay-proof.mjs` verifies every frozen input digest
before comparing the real baseline and candidate CLIs:
`CITATION_LOCALITY_PROOF: PASS (cases=7, failures=0)`, exit 0.
The isolated-HOME `--selftest` returned `selftest: 14/14 passed`, exit 0.
Full commands, complete outputs and exits: `.ufo/round-20/acceptance.json`.

The baseline program was also run against the **same candidate corpus**
(not presented as a historical corpus snapshot): exit 0, drift 0,
declaredAbsent 55. Candidate path gate: exit 1, drift 7 targets containing
26 locally unannotated locations, declaredAbsent 48, newMissing 0.
`same-surface-baseline.json`, `citation-debt.json`, and
`measured-corpus-inputs.json` under `.ufo/round-20/` carry the comparison,
actionable locations and hashes of the 43 measured markdown inputs.
These hashes describe the acceptance input surface before this bookkeeping
append, not a later unmeasured commit.

```text
VERDICT: DRIFT — §paths: 7 unannotated miss · 0 NOT in pins.pathsMissSet (exit 1)
VERDICT: DRIFT — §paths: 7 unannotated miss · 0 NOT in pins.pathsMissSet (exit 1, partial: offline)
```

Both commands exited 1. Offline explicitly suspended history and skipped
all remote armed checks; neither skip is a passed check. The red gate is
the exposed annotation debt, not a repaired source or a new miss-pin member.
The 26 heuristic locations are not asserted to equal round 19's manual
live-claim population: the scanner measures a different, explicit contract.

Receipt metadata was checked read-only in the selected Sighting manifest
row and its nested dispatch object: run/session identities exist, but no
task key, expected bag or receipt/result paths. The dispatch object has only
`argv` and `kind`; argv contents were not inspected. Evidence:
`.ufo/round-20/receipt-binding.json`. No mint or `complete` call was made.

Local axis verdicts: freshness improved, operability unchanged. Learning:
expansion unchanged, quality improved locally, discernment unchanged.
All remain provisional because no compliant wave or independent non-author
spot-check ran; this attempt is blocked, not a completed training round.
