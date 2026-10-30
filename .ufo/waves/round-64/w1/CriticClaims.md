# CriticClaims — round-64 w1 skip-work controls

## Finding and scope

**C3's executable target is reachable without any re-pin:** delete exactly the seven stale SKILL.md entries from the *base* sidecar, retaining the other 23 entries unchanged. Both the base archive and measured archive then print `VERDICT: OK (exit 0, partial: offline)`, with paths drift=0 and newMissing=0. No seven-entry re-pin is performed. This reaches the assigned skip-work target. C1 and C2 did not admit the assigned controls.

This is a discriminator defect, not an allegation that the actual measured sidecar was deleted. The deletion alternative violates the frozen contract's separate permitted-diff condition. Therefore the result falsifies **exit-0 as sufficient evidence of the claimed re-pin**, but does not establish that the actual measured tree violates that permitted-diff condition. Final claim disposition belongs to the canonical judge; this report neither admits nor ships anything.

Attacked axes: calibration (C1), operability (C2), freshness/provenance of repair (C3). Strongest counterexample: seven-entry deletion on the untouched round-63 base archive, so no round-64 lesson, counters, or other build work can explain its green.

## Identity and environment

Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Base: `1a48131577ba82c967650561be34e8dba909432a`.
Measured T0: `4c8295fa5e3b628f1fdf3840299ae415c01849fb`.
Receipts commit observed in lane log: `cc8add1fa740b920ea5179a71152680ab220c70c`.
Scratch root: `/fast/scratch/hyaku/kake-r64/CriticClaims`.

SHA-256 of instruments actually executed, read without modifying the lane:

- `.ufo/waves/round-64/c64_calibration.py`: `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf`.
- `.ufo/waves/round-64/c64_quote_tool.py`: `96fd64e9a915468a32596e1560de4a71af5ba26fd7a6cc583d279add6327ee2b`.
- `.ufo/waves/round-64/fixtures/stub_tool.py`: `7c78a05df78703044f8fe8fa02793a63b580f6353f58e8ebcee836038762edde`.

No tools installed or upgraded by this seat. Initial shell versions: Python 3.14.8, Node v24.21.0. The preserved exact-seven human sweep receipt identifies its actual subprocess Node as **v26.12.0**; do not substitute the initial shell version for that receipt's runtime.

## C1 — calibration controls denied

Counter path, in every command below:
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py`.
Commands were invoked with `TMPDIR=/fast/scratch/hyaku/kake-r64/CriticClaims/tmp` and `python3 -B`.

### Base, no round-64 work

Exact command:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 1a48131577ba82c967650561be34e8dba909432a
```

Output, exit 1:

```text
revision=1a48131577ba82c967650561be34e8dba909432a disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
```

Also exported the complete base tree with read-only `git -C /home/vgpnk/Projects/shokunin/kake-shokunin archive 1a48131577ba82c967650561be34e8dba909432a | tar -x -C /fast/scratch/hyaku/kake-r64/CriticClaims/fx/e1b-base-archive`, then made that directory an independent fixture repo. It contains no round-64 directory. Command:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/CriticClaims/fx/e1b-base-archive --revision e993c0506dafe1737c2567835a6033fc765bc5aa
```

Same metrics as above with fixture revision `e993c0506dafe1737c2567835a6033fc765bc5aa`: lesson_gate=0, unresolved=1, met=false, exit 1.

### Copied lesson, no blobs

An independent fixture containing **only** the exact measured `corpus/lessons/round-64.md` did not green:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/CriticClaims/fx/e1d-lesson-only --revision HEAD
```

The driver resolved HEAD before invoking the counter; the equivalent command above uses that fixture's HEAD. Observed exit **2**, stderr:

```text
could-not-evaluate: round-61 verifier spot-check absent
```

This is an intentional input denial, **not** `met=false` exit 1 and not a traceback. A literal lesson-only tree therefore does not meet an expectation of exit 1, although it cannot earn credit.

Stronger evaluable control: copied all five real measured prose files, but none of the four pinned blobs:

- `corpus/knowledge/response-header-expectations.md`
- `corpus/QUALITY.md`
- `corpus/lessons/round-64.md`
- `corpus/SOURCES.md`
- `corpus/lessons/round-61-verifier-spotcheck.md`

Exact command:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/CriticClaims/fx/e1e-prose-no-blobs --revision 5d3b1e63f2c55b419e23402029c911cad4cca961
```

Output, exit 1:

```text
revision=5d3b1e63f2c55b419e23402029c911cad4cca961 disagreements=1 pins=0 pin_drift=absent:raw,text,ledger,recipe recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
```

This isolates the blob requirement even when copied prose satisfies every prose component and unresolved=0. Full measured archive fixture `a06fbe920648847775e2d171970fe0b8649c5086` was the positive control: pins=1, recipe_rederive=1, lesson_gate=1, met=true, exit 0. An empty fixture also denied with the same spot-check-absent exit 2.

Evidence anchors: absolute file `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:193-198` intentionally denies absent spot-check; `:206-208` requires every pinned blob; `:267-270` includes pins independently of unresolved. Verdict for assigned C1 skip-work attack: **no false green found**.

## C2 — both stubs rejected by SHA before execution

### Exact committed stub fixture

Commands:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py --root /fast/scratch/hyaku/kake-r64/l1/fixtures/stub-repo --revision 14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_quote_tool.py --root /fast/scratch/hyaku/kake-r64/l1/fixtures/stub-repo --revision 14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3
```

Outputs respectively:

```text
revision=14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3 present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false
exit=1
revision=14fe2eab9b08cca0923b3ca5f6801f1a6418b3d3 present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

The named contract fixture was read only; no writes to l1's directory.

### Independently built lying JSON stub

Fixture `/fast/scratch/hyaku/kake-r64/CriticClaims/fx/lying-json-stub`, revision `6af6ebdc84d3a6798b53103e2731671d0088c24b`. Tool SHA-256: `ed911010d7c2095a2551c551ff8bc3c0d6ee0b0600006841a041b29ff8c3ef3a`.

Tool writes `/fast/scratch/hyaku/kake-r64/CriticClaims/lying-tool-executed` if executed, then emits a JSON object with all four frozen case IDs, each claiming passed=true, derived="absent", expected="collapsed-only"; totals=4/4, ok=true, checked_retained_bytes=true. No input bytes are inspected.

Exact new-counter command:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py --root /fast/scratch/hyaku/kake-r64/CriticClaims/fx/lying-json-stub --revision 6af6ebdc84d3a6798b53103e2731671d0088c24b
```

Output, exit 1:

```text
revision=6af6ebdc84d3a6798b53103e2731671d0088c24b present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false
```

Execution marker after c64: **False**. Running the same fixture through c63 subsequently created the marker (**True**), but c63 rejected this contradictory JSON (frozen_cases=missing, met=false, exit 1). Thus do not conflate this independent lying variant with the contract's canned all-success stub, which c63 did accept.

Evidence: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_quote_tool.py:153-157` hashes and rejects before any materialization or tool execution. Verdict for assigned C2 attack: **no false green; SHA gate discriminates both controls**.

## C3 — partial sidecar deletion reaches target without re-pin

### Controls and exact outcomes

Each command ran from `/fast/scratch/hyaku/kake-r64/CriticClaims/archive-meas`, an export of measured T0, using `node scripts/freshness-sweep.mjs --offline --json`:

| Scratch change | Exit | paths drift | newMissing | Result |
|---|---:|---:|---:|---|
| Exact measured sidecar | 0 | 0 | 0 | ok=true |
| Restore base sidecar, no re-pin | 2 | unevaluated | unevaluated | binding invalid: SKILL.md:364 |
| Base sidecar + remove pathsMissSet, pathsCitedSet, pathsFiles, pathsAbsenceStrictSameLine from pins | 2 | unevaluated | unevaluated | same SKILL.md:364 error |
| Empty sidecar `{schema:"kake-paths-sidecar-v1",entries:[]}` | 1 | 3 | 0 | ok=false |
| Delete entire sidecar | 1 | 3 | 0 | ok=false |
| Delete all SKILL.md entries from base sidecar (10 entries, retain 20) | 0 | 0 | 0 | ok=true |
| Delete **only seven changed entries**, retain other 23 | **0** | **0** | **0** | **ok=true** |

For empty/deleted sidecar, reason was exactly `§paths: 3 unannotated miss · 0 NOT in pins.pathsMissSet`. Thus deletion of the **whole** sidecar is not a false green; selective deletion is the stronger control. The first broad filter removed ten SKILL entries, not seven; this was noticed and tightened to exactly the seven differing entries before drawing the finding.

### Reproduction of strongest control

Archives were exported with these read-only commands, into fresh scratch directories:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin archive 1a48131577ba82c967650561be34e8dba909432a | tar -x -C /fast/scratch/hyaku/kake-r64/CriticClaims/archive-base
git -C /home/vgpnk/Projects/shokunin/kake-shokunin archive 4c8295fa5e3b628f1fdf3840299ae415c01849fb | tar -x -C /fast/scratch/hyaku/kake-r64/CriticClaims/archive-meas
```

Exact transformation run in Python (B/T are base/measured sidecar JSON loaded with read-only `git -C <lane> show <rev>:corpus/knowledge/freshness-sidecar.json`):

```python
changed = [i for i, (a, z) in enumerate(zip(B['entries'], T['entries'])) if a != z]
assert changed == [6, 7, 8, 9, 10, 21, 22]
attack = dict(B, entries=[e for i, e in enumerate(B['entries']) if i not in changed])
assert len(attack['entries']) == 23
# Write attack, not T, to each archive's corpus/knowledge/freshness-sidecar.json.
```

The removed old line numbers were `[364,445,448,449,450,423,431]`. No retained entry was re-pinned or otherwise edited. This uses **base** values for everything retained.

Then, exact commands executed by `subprocess.run` with cwd set to each archive and TMPDIR set to the seat's tmp directory:

```sh
node scripts/freshness-sweep.mjs --offline
node scripts/freshness-sweep.mjs --offline --json
```

Base archive human output excerpt, exit 0:

```text
§paths  171 files · 677 occurrences · 106 unique tokens
  resolve 31 · declaredAbsent 65 · drift 0 · unresolved 10
VERDICT: OK (exit 0, partial: offline)
```

Measured archive human output excerpt, exit 0:

```text
§paths  172 files · 679 occurrences · 106 unique tokens
VERDICT: OK (exit 0, partial: offline)
```

Both JSON runs, exit 0, reported:

```json
{"resolve":31,"declaredAbsent":65,"declaredAbsentIndirect":4,"drift":0,"unresolved":10,"newDrift":0,"newMissing":0}
```

### Mechanism and smallest safe correction

Absolute source anchors:

- `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs:359-364`: absent file becomes empty Map; entries are validated only if present. No mandatory roster prevents dropping an individual binding.
- Same file `:376-389`: retained entries' line bindings are validated, but missing entries have no expected identity against which to fail.
- Same file `:469-476`: only `kind=absent` injects citation annotation. The seven deleted entries were `kind=restored`.
- Same file `:504-505`: existing targets resolve independently of those restored sidecar entries.
- Same file `:575`: path verdict requires drift=0/newMissing=0, not preservation of the sidecar binding roster.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/contract.md:104-118`: combines the executable exit-0 outcome with a separate seven-pair-only diff condition. The latter is not enforced by the sweep command.

Smallest safe correction: retain the real seven-entry re-pin, but require a frozen sidecar roster/identity check (or round-specific exact expected sidecar digest) **in addition to** the sweep verdict. An independent permitted-diff check should reject removal of any of the original 30 entries and changes outside the seven allowed line/lineSha256 fields. Do not convert missing entries to pass or weaken the paths drift test. No implementation change was made in this review.

## Evidence limits, protocol, cleanup

C1/C2 fixture revisions are ephemeral local evidence, not shipped commits. Fixture creation used `git init/config/add/commit` only inside this seat's scratch directories, verifying each repo toplevel before commit, following the explicit fixture-construction paragraph. **The assignment also contains an absolute 'never commit anywhere' sentence; under that stricter reading this is a protocol deviation.** No lane/fleet git mutation, push, or integration was performed. The decisive C3 attack needs no fixture repo or commits: only read-only archives and scratch JSON edits, so its evidence does not depend on that interpretation.

Two initial Eval cells hit their default 30-second deadline (one during size accounting, one during C1 execution). They were not treated as test results. The completed C1 driver ran to completion with a longer explicit deadline; only its completed outputs are reported above.

Temporary archives, fixtures, scripts, raw sweep outputs and tool marker are removed from the seat scratch tree before yielding; the necessary commands and outputs are retained here. No installed tools to hand off. This report is the only intended durable lane write.

Self-evaluation: accuracy 4/5 (literal lesson-only exit 2 and alternate-repair-vs-actual-diff distinction explicitly retained); completeness 4/5 (all assigned controls exercised; C3 pins variant is removal of gate pins, not every imaginable pins mutation); clarity 4/5 (separate target bypass from actual-tree allegation); actionability 4/5 (exact seven-entry recipe and correction supplied, no fix applied in critic role); conciseness 3/5 (full reproduction evidence makes this report long). Overall 3.8/5. Highest-priority improvement is a sidecar-roster discriminator, not broader unrelated auditing.
