# ReviewScopeBound — write-scope audit, round 45 wave 1

Axis: adjacency (operability/freshness lens). Reviewer only — no edits to instruments, no
commit, no judgment/admission of the wave. Lane repo: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Scratch: `/fast/scratch/hyaku/kake-r45/ReviewScopeBound/` (32 prompt dumps, no other artifacts).

## Named attack and verdict

**Attack:** *Every lane write path this wave's items name must be (a) inside the lane repo,
(b) not a frozen path, (c) not MANIFEST.json / fleet `scripts/` / `templates/` / `.ufo/state/`
/ a sibling repo. The corpus must be L1-write-only; scribes draft under `drafts/` only.
Report any out-of-scope write path with its item name.*

**Verdict: FAIL (one out-of-scope write materialized; all declared targets pass).**

- (a) PASS, (b) FAIL in effect, (c) PASS for every *declared* target.
- Every declared artifact (16 groups, table below) resolves under
  `.ufo/waves/round-45/` inside the lane repo; none is frozen; none touches
  `MANIFEST.json`, `templates/`, fleet scripts, `.ufo/state/`, or a sibling lane.
- One **unnamed, implicit** write landed in a frozen path during the wave: Python bytecode
  under `.ufo/waves/round-44/classes/__pycache__/` (see F1). No item names bytecode
  caches, so no item authorizes it; the write is a side effect of a wave execution.
- Corpus: PASS. No item names a write under `corpus/`; all four corpus-destined drafts
  land in `.ufo/waves/round-45/drafts/`; `git status --porcelain corpus/ SCORECARD.md LOG.md`
  is empty (L1 landed `corpus/lessons/round-45.md` + `SCORECARD.md` at 00:02, before
  dispatch at 00:13).

## Findings by severity

### F1 — HIGH: frozen-path write during the wave (bytecode cache), concretely verified
No item names it; it contradicts the frozen-set guarantee and it is the single drift the
sha guard records.

```
$ sha256sum -c .ufo/waves/round-45/verification/sha-guard/before.sha256 2>&1 | grep -v ': OK$'
.ufo/waves/round-44/classes/__pycache__/g3_empty_path.cpython-314.pyc: FAILED
sha256sum: WARNING: 1 computed checksum(s) did NOT match

$ sha256sum -c ... | awk -F': ' '{print $2}' | sort | uniq -c
      1 FAILED
    482 OK

$ find .ufo/waves/round-44 -name '*.pyc' | wc -l          # now
39
$ grep -c '__pycache__' .ufo/waves/round-45/verification/sha-guard/before.sha256
36
```

Baseline vs now (identical to SentinelFrozen's independent measurement):

| file | baseline (manifest) | now | mtime |
|---|---|---|---|
| `classes/__pycache__/g3_empty_path.cpython-314.pyc` | `25ba85808f19b6ab…` | `ff0cbbc8d23d7272…` | 00:15:52 |
| `classes/__pycache__/g9_port_digits.cpython-314.pyc` | absent | `bb3b9b590308a482…` | 00:15:52 |

Sweep of the whole lane repo for writes since dispatch:

```
$ find . -type f -newermt '2026-10-24 00:07:00' -not -path './.ufo/waves/round-45/*' \
    -not -path './.git/*' -not -path './.jj/*' -not -path './.ufo/interactive-sessions/*' -printf '%TH:%TM %p\n' | sort
00:19 ./.ufo/waves/round-44/classes/__pycache__/g3_empty_path.cpython-314.pyc
00:19 ./.ufo/waves/round-44/classes/__pycache__/g9_port_digits.cpython-314.pyc
```

The pair was written twice (00:15:52 and again 00:19); the second write reproduced identical
bytes (`ff0cbbc8…`, `bb3b9b59…`), so the path is live and idempotent: every unguarded import
of those two class modules re-touches the frozen tree. The original divergence is between the
baseline pyc (compiled by an earlier 3.14.x) and the host interpreter (3.14.8, `python3
--version` → `3.14.8 (main, Oct 2 2026)`), which is why the first rewrite changed content.
The drivers themselves are not the writer: v2 spawns counters as
`[sys.executable, "-B", counter, …]` (`c45_audit.py:41`), and all named wave commands pass
`-B`; the writer is therefore an ad-hoc `python3` invocation that imports
`round-44/classes/g3|g9` without `-B` — a write path no item names.

Mechanism (verified in the shipped bytes): `c45_count.py:137-152` (`load_classes`) imports
`.ufo/waves/round-44/classes/g*.py` via `importlib.util.spec_from_file_location` +
`spec.loader.exec_module`. `exec_module` writes a `__pycache__` entry unless the interpreter
runs with `-B`/`PYTHONDONTWRITEBYTECODE`; neither `c45_count.py`, `c44_count_v5.py`, nor
`c44_audit.py` sets `sys.dont_write_bytecode` (`grep -n "dont_write_bytecode" …` → no hits).
Every named command in the wave uses `python3 -B`, but an ad-hoc inspection command that
imports a class module without `-B` is enough to mutate the frozen tree; the two files above
carry exactly that signature.

Smallest remediation: raise the bytecode policy into the loader itself
(`sys.dont_write_bytecode = True` before `exec_module`, or `compile()` the source bytes and
`exec` without caching) so the instrument cannot mutate its frozen inputs regardless of
caller flags. This belongs in v6 (`c45_count.py`) and is inherited by frozen v5 at runtime
only (v5 bytes stay untouched). I did not attribute the writer to a seat: no live process
remained at inspection, and the item texts do not record ad-hoc runs. SentinelFrozen's
report (`.ufo/waves/round-45/w1/SentinelFrozen.md`) records the same drift; I reproduce it
independently rather than relying on that report.

### F2 — MEDIUM: the frozen guard measures ignored bytecode, not committed bytes
`before.sha256` has 483 entries, of which 36 are `__pycache__/*.pyc` (all ignored by
`.gitignore`: the file lists only 3 patterns, `__pycache__/` and `*.pyc` among them).
Non-pyc entries = 447 = 440 `git ls-files` under the guarded dirs + 5 named round-44 files
+ 2 scripts — i.e. the committed set is fully covered, and the one guard failure is entirely
in generated cache bytes.

```
$ python3 … group by prefix
{'scripts': 2, 'r43-verif': 68, 'other': 5, 'classes': 10, 'classes-placebo': 10,
 'pycache': 36, 'controls-r43': 27, 'r44-verif': 325}
$ git ls-files .ufo/waves/round-44/classes … .ufo/waves/round-44/verification | wc -l
440
```

Consequence: a kill-rule-1 "frozen drift" verdict is now ambiguous — the frozen instruments
and receipts are byte-intact (482/483 OK; the 447 committed entries all OK), while the
failing entry is generated bytecode. Recommendation for the L1: the guard should enumerate
`git ls-files` over the frozen prefixes (or exclude `__pycache__`), and the round claim's
"committed bytes" framing should be stated as such; F1 should still be fixed, because the
same mechanism could equally clobber a frozen *interpreter* path in a future round.

**F2b — the guard also under-covers the frozen set.** `build_v5.py`, named frozen by the wave
context, is not in the manifest at all:

```
$ grep -c 'build_v5.py' .ufo/waves/round-45/verification/sha-guard/before.sha256
0
$ ls -la .ufo/waves/round-44/build_v5.py
-rwxr-xr-x 1 vgpnk vgpnk 7381 Oct 23 19:34 .ufo/waves/round-44/build_v5.py
```

The five "other" manifest entries are exactly `c44_audit.py`, `c44_count_v5.py`,
`c44_placebo.py`, `controls-27.tsv`, `controls-canary.tsv` — the six named round-44 files
minus `build_v5.py`. So the guard is both wider (ignored bytecode) and narrower (one frozen
source unguarded) than the claim it is meant to enforce; the L1 should fix the file list
from the frozen declaration itself, not from the previous round's guard command.

### F3 — HIGH (adjacency): instrument-writer and instrument-runner seats raced; three named receipts are missing
Two seats returned dependency-blocked because the artifact they must exercise did not exist
when they looked, and the missing artifact landed seconds later:

- `ExecRegressionHonest` (report 00:13:56): `Path …/c45_audit.py not found`; C1 honest
  regression **unrun**. `c45_audit.py` was written at **00:17:32**, after that seat returned.
- `ExecV4ReceiptV6` (report 00:14:14): `c45_count.py` absent; C2(b) v4 receipt **unrun**.
  `c45_count.py` landed at **00:14:27 — 13 s after the seat returned**.

```
$ stat -c '%y %s %n' .ufo/waves/round-45/c45_audit.py .ufo/waves/round-45/c45_count.py .ufo/waves/round-45/c45_matrix.py
2026-10-24 00:17:32 15044 .ufo/waves/round-45/c45_audit.py
2026-10-24 00:14:27 52433 .ufo/waves/round-45/c45_count.py
2026-10-24 00:18:09 13335 .ufo/waves/round-45/c45_matrix.py
$ find .ufo/waves/round-45/verification -maxdepth 1 -type d
…/verification  …/ledger-gate  …/selftest-coverage  …/sha-guard  …/witness-split  …/hardening
$ test -f …/verification/v6v4/counter-v4.json && echo YES || echo NO       → NO
$ test -f …/verification/matrix/after.json && echo YES || echo NO          → NO
$ test -f …/verification/honest-regression/after-v5-v2.json && echo YES || echo NO → NO
$ find …/verification/selftest-coverage -type f
…/before/m1.txt …/before/m2.txt …/before/m3.txt …/before/m4.txt   (`after/` exists, empty)
```

Absent receipts in this wave: `verification/v6v4/` (C2(b) after), `verification/matrix/`
(C1 before/after counts), `verification/honest-regression/` (C1 27/27 + build 3/3),
`verification/selftest-coverage/after/` (C2(a) 4/4). Note `c45_matrix.py` post-dates the
`ExecMutantMatrix` report (00:15:11), and `c45_audit.py` post-dates `ExecMutantMatrix`'s
before-run window — so the before-state matrix is valid, but every after-state number in
this wave is still contingent on re-running the (now present) instruments. This is an
ordering defect in the wave plan, not a seat defect:
the plan has no write→run barrier and forbids polling, so a fast seat deterministically
returns on a slow sibling. Fix at plan level: schedule runner seats one wave after builder
seats, or make the L1 re-run idempotent and mandatory (as the blocked reports already say).

### F4 — MEDIUM: unanchored relative write paths in three item texts
These targets are stated without the `.ufo/waves/round-45/` prefix; resolved from the repo
root they would create lane-root `fixtures/`, `verification/`, `mutants/` beside `corpus/`:

| item | unanchored token | intended location |
|---|---|---|
| ExecInvalidFixtures | `fixtures/honest/` | `.ufo/waves/round-45/fixtures/honest/` |
| ExecMutantMatrix | `verification/selftest-coverage/after/mN.txt`, `mutants/m{1..4}_v2.py` | `.ufo/waves/round-45/…` |
| ExecMatrixRunner | `fixtures/{counter-error,tool-absent,stale-planted}` (no outdir named for the after cohorts) | `.ufo/waves/round-45/fixtures/…` |

No stray root dirs exist (`ls -d fixtures mutants verification drafts v6diff` → none), so the
defect is latent, not yet materialized. `ExecMatrixRunner` additionally never names the
after-stage cohort dir it asks v2 to create; v2 refuses a non-empty outdir, so the only safe
choice is a fresh `fixtures/<class>/out-v2/` — worth pinning in the re-run brief.
L1 action: normalize these to lane-absolute paths before wave 2 reissues them.

### F5 — MEDIUM: receipts cannot be attributed to the executing driver revision
`ExecDriverV2` specifies `run-manifest.json {started_ns, counter_sha256, nonce}` — counter
sha is bound, driver sha is not. Combined with F3 (driver written while siblings run it), a
receipt produced at minute N may come from a driver revision that no longer exists, and
nothing in the artifact records which bytes ran. Smallest fix: add `driver_sha256` (and
`driver_mtime_ns`) to the v2 manifest, then have the L1 re-run the runner seats against the
final bytes and diff the manifest's driver sha against the committed file.

### F6 — LOW: executor authors corpus-bound prose
`ExecWitnessSplit` (executor role) writes `.ufo/waves/round-45/drafts/witness-split-sentence.md`,
a SCORECARD sentence. Path is in-scope (drafts are the designated dropbox) but authorship
crosses the scribe/L1 boundary stated in the wave context; the L1 must treat that draft as
unreviewed input, not as integration-ready text.

### F7 — PASS: report trailers
All 32 task-call report trailers are unique and match
`\.ufo/waves/round-45/w1/[A-Za-z0-9]+\.md` — no traversal, no collisions, no path escaping
`w1/` (`duplicates: []`, 32/32 in-pattern). One report was already written per seat naming
itself; no seat overwrote another's report.

## Declared write-target matrix

| artifact group (owning item) | resolved path | (a) lane | (b) frozen | (c) forbidden |
|---|---|---|---|---|
| fixtures/{counter-error,tool-absent,stale-planted}/ (ExecInvalidFixtures) | `.ufo/waves/round-45/fixtures/*` | yes | no | no |
| verification/hardening/before/ (ExecInvalidFixtures) | `.ufo/waves/round-45/verification/hardening/before/*` | yes | no | no |
| c45_audit.py (ExecDriverV2) | `.ufo/waves/round-45/c45_audit.py` | yes | no | no |
| c45_count.py (ExecCounterV6) | `.ufo/waves/round-45/c45_count.py` | yes | no | no |
| v6diff/v5-v6.diff (ExecCounterV6) | `.ufo/waves/round-45/v6diff/v5-v6.diff` | yes | no | no |
| verification/v6v4/ (ExecV4ReceiptV6) | `.ufo/waves/round-45/verification/v6v4/*` | yes | no | no |
| mutants/m{1..4}.py, m{1..4}_v2.py (ExecMutantMatrix) | `.ufo/waves/round-45/mutants/*` | yes* | no | no |
| mutants/v2/m{1..6}.py (MutDriverV2Spec) | `.ufo/waves/round-45/mutants/v2/*` | yes | no | no |
| verification/selftest-coverage/{before,after}/ (ExecMutantMatrix) | `.ufo/waves/round-45/verification/selftest-coverage/*` | yes* | no | no |
| verification/witness-split/ + drafts/witness-split-sentence.md (ExecWitnessSplit) | `.ufo/waves/round-45/{verification/witness-split,drafts}/*` | yes | no | no |
| c45_matrix.py (ExecMatrixRunner) | `.ufo/waves/round-45/c45_matrix.py` | yes | no | no |
| verification/matrix/{before,after}.json (ExecMatrixRunner) | `.ufo/waves/round-45/verification/matrix/*` | yes | no | no |
| verification/honest-regression/after-v5-v2.json (ExecRegressionHonest) | `.ufo/waves/round-45/verification/honest-regression/*` | yes | no | no |
| verification/ledger-gate/before.txt (ExecLedgerGate) | `.ufo/waves/round-45/verification/ledger-gate/before.txt` | yes | no | no |
| verification/sha-guard/before.sha256 (SentinelFrozen) | `.ufo/waves/round-45/verification/sha-guard/before.sha256` | yes | no | no |
| drafts/{scorecard-measurement,sources-gate,receipt-integrity,mistakes}.md (4 scribes) | `.ufo/waves/round-45/drafts/*` | yes | no | no |

`*` = relative token in the item text, intended location as in F4.

## Corpus L1-write-only check

```
$ git status --porcelain=v1 corpus/ SCORECARD.md LOG.md
(empty)
$ git merge-base --is-ancestor 3b4c430 HEAD && echo YES
YES
$ git diff --stat 3b4c430 HEAD -- .ufo/waves/round-44 .ufo/waves/round-43 corpus/
(empty)
$ git diff --stat 3b4c430 HEAD
 …/round-45/{make_w1_spec.py,w1-plan.json,w1-plan.stderr,w1-run.stderr,w1-spec.json,
             w1-taskcall.json,w1/swarm-registry.json} | 7 files, 2139 insertions
```

`corpus/lessons/round-45.md` and `SCORECARD.md` carry mtimes 00:02 — L1's pre-dispatch commit,
not a seat write. No scribe prompt names a write under `corpus/`; each says "the L1 lands it;
you write the draft" and points at `drafts/`. The four scribe prompt write clauses were read
in full (`ScribeDeclarations`, `ScribeSourcesGate`, `ScribeKnowledge`, `ScribeLessonMistakes`);
`ScribeSourcesGate`'s draft is `drafts/sources-gate.md` only (its target text asks for a
SOURCES.md *row draft*, and the row is stated as draft content, not a file write).

`scripts/ledger_latest_check.py` is read-only: `grep -nE '"w"|write_text|write_bytes|mkdir|makedirs|unlink|replace\('`
has no matches; its only subprocess is `git` (`:73`). Both guarded scripts remain
byte-identical (482/483 OK includes them; `git diff 3b4c430 HEAD` clean on `scripts/`).

## Residual risk

- **Writer attribution for F1 is open.** I can prove *when* (00:15:52), *what*, and *which
  code path can do it*, not *which seat*. Any seat that ran an un-`-B` import of
  `round-44/classes/g3|g9` is consistent with the evidence; the wave's own commands all use
  `-B`, so the likely source is an ad-hoc inspection command. Without process accounting the
  claim "no seat wrote outside its scope" cannot be stronger than "no *declared* write
  escaped and exactly two ignored cache files changed".
- **Guard scope (F2)** means the current FAIL is simultaneously too loud (ignored bytecode)
  and too narrow (it cannot detect a frozen *source* touched only in mtime, since only
  content is hashed). A `git ls-files`-scoped guard plus a mtime-free content check is the
  honest instrument.
- **F3 receipts** are unproduced, so I cannot audit their paths retroactively; my matrix is
  over declared intent. When the L1 re-runs the blocked seats, re-check the actual landing
  paths against this table (F4 tokens are the ones most likely to drift).

## Verification gaps (unrun by design)

- I did not run any instrument (`c44_audit.py`, `c45_audit.py`, `c45_count.py`,
  `c45_matrix.py`) — correctness of v2/v6 is other seats' scope, and running them would
  itself risk F1.
- I did not run `scripts/ledger_latest_check.py` (leased to ExecLedgerGate); its read-only
  status is a static read, corroborated by the unchanged script hash.
- I did not inspect sibling lane repos beyond the fleet top-level mtime sweep
  (`find /home/vgpnk/Projects/shokunin -maxdepth 2 -newermt '2026-10-24 00:07'`): only other
  lanes' own `.git/`, `kotoba-shokunin/LOG.md`, and `.ufo/watchdog.log` changed — no kake
  seat wrote there. `.ufo/state/` changes (`mori.report-baseline` 00:02,
  `chousa.report-baseline` 00:03) predate dispatch and are not attributable to this lane.

## Files written

- `.ufo/waves/round-45/w1/ReviewScopeBound.md` (this report).
- `/fast/scratch/hyaku/kake-r45/ReviewScopeBound/<SeatName>.txt` — 32 prompt dumps, scratch only.
No tool installs or upgrades; nothing else written.
