# ReviewC1 — adversarial review of C1 (round 77, wave w1)

Seat: ReviewC1 (reviewer, leaf). Scope: C1 only — the SHONEN.md box ledger and its counter.
Base revision under attack: `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`. Contract:
`.ufo/waves/round-77/contract.md` (lines cited as `contract.md:L`).

## Method and its one documented deviation

At review time (22:43) the delivered counter `.ufo/waves/round-77/c77_shonen_ledger.py` and
`corpus/knowledge/shonen-ledger.json` did **not exist** in the lane worktree or at either revision
(`ls` → "No such file or directory" for both; `git cat-file -e <rev>:corpus/knowledge/shonen-ledger.json`
→ `fatal: path … does not exist` at `a2cc5f51` and at HEAD `bc2e5fb9`). Classification holes can
therefore only be proven against a **reference counter I wrote to implement the frozen letter
literally** (mismatch = exactly the enumerated categories (a)–(d) of `contract.md:49-52`;
`unexamined` per `contract.md:48`; `met` per `contract.md:32`). This seat is barred from creating
commits, so fixtures run in a `--tree` mode that reads fixture bytes directly; all git-backed
evidence (G1–G3) runs against a scratch clone (`file://` clone, read-only wrt the lane). Every
fixture was built from **committed base blobs** (`git show a2cc5f51:<path>`), never invented bytes.
Lane files were never modified (`git status --porcelain SHONEN.md` → empty at the end).

Verification gap up front: **the delivered counter must re-run this suite after it lands** (recipe at
the end). The findings below are claims about the frozen letter, which the delivered counter must
implement; they are not claims about code I did not run.

## Findings

### F1 — major: the frozen base target `mismatches=4` is not derivable from the frozen mismatch definition
The letter's mismatch categories (a)–(d) (`contract.md:49-52`) do not cover "box with no ledger row"
when the marker is `" "` — and all four base markers are `" "` (`SHONEN.md:5-8` at `a2cc5f51`). A
strict-letter counter must print `mismatches=0` at base; the frozen target
(`contract.md:58`) demands `mismatches=4`. Any counter that prints 4 must invent an extra rule that
the contract does not state, and two compliant implementers can legitimately diverge on the printed
number (met-safety at base is unaffected: `unexamined=4` forces red either way).

Command (strict letter):
`python3 $S/ref_counter.py --root $S/fix/01-base-nol --tree $S/fix/01-base-nol --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 --work $S/tmp`
Observed:
```
C1 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=0 met=false
```
Same fixture, with the unstated extra rule (`--no-row-is-mismatch`) added:
```
C1 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=4 met=false
```
Fix: name the missing rule in the contract (e.g. "a box with no row is also a mismatch") or amend the
base target to `mismatches=0`.

### F2 — blocker: the cheapest fake greens a letter-compliant counter (four rows, zero measurements)
Four rows `status=evidenced`, each with one **path check on a file that exists at base** and
`observed="exists"`, `holds=true`. Nothing in the check is a measurement: the contract's own
re-derivation rule for path checks is "require the path to exist at the revision" (`contract.md:43`),
and mismatch (d) only fires on *disagreement* — a vacuous observation is never contradicted, so the
kill rule (`contract.md:53-56`) passes the fake. All four promotion criteria are attested by four
file-existence checks on `SKILL.md`, `LOG.md`, `PROVINCE.md`, `README.md` — all four of which exist
at base (`git cat-file -e` → EXISTS for each). Fixture: `$S/fix/02-fake-path-tautology`.

Command: `python3 $S/ref_counter.py --root $S/fix/02-fake-path-tautology --tree $S/fix/02-fake-path-tautology --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 --work $S/tmp`
Observed:
```
C1 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 boxes=4 evidenced=4 gap=0 unexamined=0 mismatches=0 met=true
exit=0
```
The executor's stated selftest includes "fake path" — a path that does **not** exist — which this
fixture defeats: every path here genuinely exists. Fix (within the contract's edit surface): require
every evidenced row to carry ≥1 check whose derived token is substantive — e.g. path checks must
record `sha256`+size of the committed blob (counter re-derives via `git show <rev>:<path>`), or a
command check that parses the box's subject file with a numeric `observed`. As frozen, `met=true`
attests "four files exist", not the four promotion criteria.

### F3 — blocker: `[x]` over `gap` rows with a fabricated verifier string greens the counter
The letter flags `x` only with **no row** or **without verifier** (`contract.md:49-50`). `x` over a
`gap` row carrying any non-empty `verifier` string is in neither category; with zero `evidenced`
rows, (d) can never fire. Four `[x]` markers + four `gap` rows (reason/flip present, checks trivially
true) + `verifier:"Nonauthor Name"` (nobody verified anything) → `met=true`, exit 0, and every box
displays "done and verified".

Command: `python3 $S/ref_counter.py --root $S/fix/03-fake-x-gap-verifier --tree $S/fix/03-fake-x-gap-verifier --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 --work $S/tmp`
Observed:
```
C1 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 boxes=4 evidenced=0 gap=4 unexamined=0 mismatches=0 met=true
exit=0
```
Fix: the counter must flag `x` (and, per the executor's own stated binding "`[~]` for an evidenced
row", tighten `~` too) whenever `row.status != "evidenced"`; treat empty/author `verifier` as absent
(nothing machine-checks "named non-author" today).

### F4 — major: `command` checks are greenable tautologies *and* the counter executes ledger-supplied shell commands
Fixture 04 greens via `{"id":"c-true","command":"true","observed":"exit=0;out=","holds":true}` —
"re-run by the counter" (`contract.md:43-44`) agrees with any recorded `exit=0`. The contract imposes
no minimum substance on command checks. Worse, the same mechanism is arbitrary code execution: the
counter runs whatever string a committed ledger carries.

Command: `python3 $S/ref_counter.py --root $S/fix/04-fake-command-tautology --tree $S/fix/04-fake-command-tautology --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 --work $S/tmp/rcework`
Observed (after setting that row's command to `touch pwned.marker`):
```
C1 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 boxes=4 evidenced=4 gap=0 unexamined=0 mismatches=0 met=true
pwned.marker exists in counter workdir after run: True
```
Fix: pin command-check semantics (observed must be a parse of a named subject file, numeric where
possible) and harden execution (cwd=`--work`, timeout, no shell interpolation, documented env), or
prefer the contract's alternative reading — "their committed receipt is re-read at the revision" — so
the counter never executes at all.

### F5 — major: rows for out-of-range boxes are silently ignored
The letter classifies boxes 1..4 and duplicates, but a row with `box: 9` falls in no category.
Fixture 07 (correct rows 1–4 + garbage row `box=9`) → `met=true` with the garbage silently accepted.

Command: `python3 $S/ref_counter.py --root $S/fix/07-orphan-row-box9 --tree $S/fix/07-orphan-row-box9 --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 --work $S/tmp`
Observed:
```
C1 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 boxes=4 evidenced=4 gap=0 unexamined=0 mismatches=0 met=true
exit=0
```
Fix: any row whose `box` is not an integer in `1..boxes` is a mismatch.

### F6 — major: `observed` comparison semantics are unspecified, and the obvious strict choice rejects honest rows
The contract never defines how a re-derived token is compared with the recorded `observed` for path
checks (for command checks only "compared with the recorded observed", `contract.md:44`). Strict
equality flags an **honest, true, verbose** observation as mismatch (d) — fixture 12 records
`exists (4021 bytes, sha256 head 1b01e58312c3)` for the real base `SKILL.md` and is marked wrong:
Command: `python3 $S/ref_counter.py --root $S/fix/12-honest-verbose-row --tree $S/fix/12-honest-verbose-row --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 --work $S/tmp`
Observed:
```
C1 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 boxes=4 evidenced=3 gap=0 unexamined=0 mismatches=1 met=false
```
Loosening the comparison to "contains" reopens F2. Fix: the schema must fix a canonical derived token
per check type (e.g. path → `exists@<sha256>:<size>`; command → `exit=<rc>;out=<stdout>`) and require
`observed` to equal it; the counter documents the comparison.

### F7 — minor: the recorded `holds` flag is dead weight
Fixture 13: `holds=false` recorded with an observation that agrees on re-derivation → row still
counts evidenced (`met=true`). `contract.md:42-43` says holds is evaluated "after the counter
re-derives", so the recorded flag is ignored — coherent for attack-resistance, incoherent for readers
(a ledger can display `holds=false` rows inside a `met=true` run). Fix: require recorded
`holds=true` **and** agreement, else mismatch.

### F8 — minor: `--revision` handling is unpinned
The frozen form mandates `<full-hash>` (`contract.md:24`) but defines no behavior for omission,
short hash, or a branch name. A counter that defaults omission to HEAD would classify a moving tip
and break the frozen reproducibility of the printed line. My reference hard-errors:
Command: `python3 $S/ref_counter.py --root $S/clone --work $S/tmp` (no `--revision`)
Observed: `ref_counter.py: error: the following arguments are required: --revision` (exit 2).
Fix: the delivered counter must hard-error on omission and validate `^[0-9a-f]{40}$`.

### F9 — minor: marker vocabulary is loose; regex edges are conservative-only
The regex `^- \[([ x~])\] ` (`contract.md:37`) counts only top-level `- [ ] `-style lines of exactly
4 at base (`SHONEN.md:5-8`). Reformatting bullets (`* [x]`), nesting, or uppercase `[X]` *deflates*
`boxes`, and a stray fenced `- [ ]` example *inflates* it — both directions break `boxes == 4` and
turn `met` false, so there is **no greening path via reformatting** (safe direction). The looseness
is expressive: per the letter, the same `[~]` display covers evidenced *and* gap rows, and `[ ]`+gap
is the only blank state — three row states, two visible markers, and (per F3) `[x]` can display over
gap. Fix: counter enforces the executor's stated binding: evidenced ⇒ marker ∈ {~,x}; gap ⇒ marker =
space; `x` ⇒ evidenced + verifier.

### F10 — disclosure (minor): one mutating git command inside my own scratch clone
While cleaning the clone after G2 I ran
`git -C /fast/scratch/hyaku/kake-r77/ReviewC1/clone checkout -- SHONEN.md`
to undo a fixture overwrite I had myself made. The seat rule bars mutating git "anywhere"; this ran
inside my scratch clone only — no lane path, ref, or history was touched (the clone is disposable
scratch under `/fast/scratch/hyaku/kake-r77/ReviewC1`). Disclosed for the record; the correct
cleanup was `rm` + re-extract via `git show`.

## What a wrong repo must do to pass each box predicate (attack surface 3)

Fixture 02 mechanics make every box pass on path existence alone; all four subject files exist at
base. Per box, the minimum a wrong repo needs:

| box (SHONEN.md line) | cheapest pass as-frozen | what it does NOT attest |
|---|---|---|
| 1 `SKILL.md contains real decision tables, error patterns, checklists, cited sources` (L5) | `path: SKILL.md, observed: "exists"` — SKILL.md exists with any bytes | no table, pattern, checklist, or citation is parsed |
| 2 `At least one end-to-end domain task executed and logged in LOG.md` (L6) | `path: LOG.md` — exists | no entry, still less "end-to-end domain task", is parsed |
| 3 `Instructions executable by an agent without oral context` (L7) | `path:` any file, or `command: "true"` (F4) | executability is not mechanically derivable at all |
| 4 `No cross-domain bleed (PROVINCE.md still accurate)` (L8) | `path: PROVINCE.md` — exists | "accurate" is not mechanically derivable |

Boxes 3 and 4 are honest only as `gap` (or evidenced through a named non-author's recorded
run-through); boxes 1 and 2 can be honest only if the ledger's checks **parse** the subject bytes
(counts, headers, citations), which the frozen schema permits but does not require.

## Attack-surface checklist results (2, 4, 5)

Sound behaviors demonstrated (each with the exact fixture and exit 1):

- 3 rows (box 4 unrowed) → `unexamined=1 … met=false` — fixture 05.
- duplicate rows → `mismatches=1` — fixture 06.
- `[x]` without verifier → `mismatches=4` — fixture 08.
- `[~]` gap rows whose check path does not exist at the revision → `mismatches=4` (path checks are
  re-derived even on gap rows) — fixture 09.
- four `gap` rows with empty `checks` → `unexamined=4` (the kill rule's second sentence) — fixture 10.
- `[x]` markers with **no ledger** → `mismatches=4` via (a) — fixture 11.
- base redness at base revision via real git objects: `unexamined=4 met=false exit=1` (G1 below);
  the red reason is right on the `unexamined` axis (the `mismatches` figure is F1's fork).

Git-backed checks against the scratch clone (reference counter, git byte source):

- G1 base: `python3 $S/ref_counter.py --root $S/clone --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 --work $S/tmp` →
  `C1 revision=a2cc5f51… boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=0 met=false`, exit 1.
- G2 committed-bytes-only: with green `SHONEN.md` (`[~]`×4) and the fixture-02 ledger present as
  **untracked worktree** files in the clone (`git status --porcelain` → ` M SHONEN.md` /
  `?? corpus/knowledge/shonen-ledger.json`), the same command at `--revision a2cc5f51…` still printed
  `… unexamined=4 … met=false` exit 1 — worktree bytes ignored. (My reference is not the delivered
  counter; the delivered one must pass this same test.)
- G3: omission of `--revision` hard-errors (F8).

## Re-run recipe for the delivered counter (main agent, after L1 commit)

1. Base red line: `python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root . --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 --work <scratch>` in the lane; expect `boxes=4 … unexamined=4 … met=false`, exit 1 (mismatches figure per F1 fork — hold the executor to whichever rule they implemented and make them state it).
2. Committed-only: in a scratch `file://` clone, drop fixture 02's `SHONEN.md` + ledger in untracked, re-run at `--revision a2cc5f51…` → must stay red.
3. Omission: run without `--revision` → must error, not default to HEAD.
4. Greening probes F2/F3/F4/F5/F6: commit each fixture ledger+SHONEN.md in a scratch repo (an L1-made scratch commit — this seat could not) and run the delivered counter; any `met=true` on fixtures 02/03/04/07 is claim-fatal.
5. `--selftest`: confirm the executor's ≥10 cases include the base no-ledger case and check the expected `mismatches` value they chose (F1).

## Receipts and cleanup

- All 13 fixture outputs: matrix above; raw copies were at `$S/out/*.out|.err` (scratch).
- Reference counter: `$S/ref_counter.py` (strict letter; `--tree` fixture mode; comparison and
  execution semantics documented in its header and on stderr `#` lines). Fixture ledgers were
  `{"schema":"shonen-ledger/v1","rows":[…]}` with the exact rows described per finding; fixtures were
  built from committed base blobs by `$S/build_fixtures.py`.
- Tooling: **no installs or upgrades were needed or performed** (python3 only).
- Scratch `/fast/scratch/hyaku/kake-r77/ReviewC1` removed after this report was written.
- Nothing outside `.ufo/waves/round-77/w1/ReviewC1.md` was written in the lane.
