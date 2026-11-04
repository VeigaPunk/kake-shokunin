# ScribeRegistry — round 87 single v1 wave

## Behavior and axes

Draft-only deliverable completed. Axes: calibration (lowest owned axis, 2 HOLD)
and freshness (10 HOLD). No score change, counter success, CLI success or outside
admission is claimed by this seat. L1 alone integrates independent candidates.
Canonical base: 86ca7803fd964db7ae2a628c7e9048741c78a45f;
freeze: 58fee726102aa89ad2c1fa9f697869de3a212510 (contract inputs, not
re-measured repository-state claims).

## Artifacts / touched surfaces

All writes are new seat-owned draft/evidence files, plus this report:

- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeRegistry/SKILL.append.md
- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeRegistry/README.append.md
- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeRegistry/PROVINCE.append.md
- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeRegistry/SOURCES.append.md
- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeRegistry/source-access.md
- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeRegistry.md

Append the first three blocks at EOF of their named canonical surfaces; the
SOURCES block is a single eleven-cell registry row to add after S461 within the
existing registry table. No canonical bytes were changed by this seat.

SKILL draft names cache_current_age as a probe, owner kake, exit 0
clean/calculated and exit 1 failed/invalid_input, diagnostic on stderr, exact
--selftest spelling and frozen .ufo/waves/round-87/age-cases.json oracle.
Normal operation is stdin/stdout only, apart from stderr diagnostics. Coverage
and province drafts advance Age arithmetic only, not storage/reuse approval,
HTTP extraction, browser/runtime observation or publishing.

## Source provenance and identifier finding

Independently opened https://httpwg.org/specs/rfc9111.html#age.calculations on
2026-11-04 before writing S462. Located §4.2.3 quote (8 words):
“The corrected_age_value MAY be used as the corrected_initial_age.”
Reader excerpt showed all six equations, absent Age default zero, the MAY path
and conservative max alternative. source-access.md retains the excerpt and
access limitations. Source kind spec, tier A, scope only age arithmetic;
used-by is exactly corpus/knowledge/cache-current-age.md. Existing S456/S457/S461
scopes were read; S461 is not broadened or replaced.

The source-id search returned no canonical S462 row at observation time:
functions.grep(pattern="\\| S462 \\|",
path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md",
gitignore=false). This is not a concurrent reservation. The broader capability
search found round-87 planning references, not an existing row in the inspected
production registry. No formal source census was run.

## Commands, outcomes and gates

Shell commands actually executed, cwd /home/vgpnk/Projects/shokunin:

1. `mkdir -p /fast/scratch/hyaku/kake-r87/ScribeRegistry /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeRegistry`
   — success, exit 0, no output.
2. `rmdir /fast/scratch/hyaku/kake-r87/ScribeRegistry`
   — success, exit 0, no output. Scratch was empty and is removed; no clone made.

Other operations were functions.read/glob/grep/write/edit, not shell commands;
no process exit status applies. Read contract.md and count.py first; opened
RULES.md; read Godspeed and completion self-evaluation skills. Public source
reader operation returned content (text/html, Method native); status code,
raw response size and raw digest were not exposed and are not invented.
Bounded follow-on source read: artifact://108390:295-375.

No builds, lints, counters, probe runs or selftests executed by this scribe.
Registry CLI/selftest strings describe the frozen intended interface, not observed
implementation behavior. L1's integrated counter/probe/selftest checks remain
necessary execution evidence; no receipt is fabricated here. No installs,
services, restarts, provider probes, browser, credentials, delegation, git/jj
mutation, commit, push, publish or deployment occurred.

## Findings, defects and limits

- Conservative max is an allowed profile, not the RFC's sole algorithm.
- Integer epoch JSON inputs and arbitrary precision are local adapter choices.
- Missing Date remains unsupported; calculated age proves neither freshness nor reuse.
- Fixed seventeen-case coverage does not establish universal correctness.
- No source-fetch HTTP status/digest claim or candidate execution claim is made.
- Existing general-classifier semantic debt, independent changed-row oracle,
  D84-2/3/4 and outside admission remain untouched.
- Draft quote length was initially mislabeled 9; corrected to 8 before handoff.
  First corrective edit was rejected because a source line was truncated;
  reread both affected locations, then the surgical correction succeeded.
- No product defect was established by this bounded documentation seat.

## Self-evaluation (not a gate)

Accuracy 4: source equations observed; candidate runtime not exercised.
Completeness 4: four requested append surfaces delivered; integration belongs to L1.
Clarity 4: distinct append files and explicit limitations; paths are necessarily long.
Actionability 4: EOF/table placement specified; executable evidence remains external.
Conciseness 4: detailed command/provenance accounting repeats some scope boundaries.
Overall 4.0. Improvements for integration: bind actual CLI evidence; preserve the
narrow frontier wording; retain source-access limitations. User agreement is not
observed; this is self-assessment only.
