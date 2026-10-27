# ExecCountingCommands — round-63 w1

Seat: `ExecCountingCommands`. Item: produce the paste-able before/after command set
for both frozen claims (one before-at-base command and one after-at-measured-commit
command per claim, each with its expected output line and exit), run them all, and
paste the outputs.

Scope: read-only against the fleet repo. No commits, no push, no mutation of the
fleet repo, `.ufo/state`, `scripts/`, templates, sibling repos, `corpus/SOURCES.md`,
`considerthese/`, or `MANIFEST.json`. Only this report file was written to the
fleet repo. Scratch fixture repos were created under
`/fast/scratch/hyaku/kake-r63/ExecCountingCommands/` and deleted afterwards.
No tools were installed (none needed).

Revs used throughout:

- base (round-62 tip) = `13d4519818db28cd0aa912e49020659140d7b9fa`
- measured commit      = `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`
- lane root            = `/home/vgpnk/Projects/shokunin/kake-shokunin`

---

## 1. The paste-able command set

All four commands are run from the lane root. `--root .` is the lane root; the
counters read committed bytes via `git -C <root> show <rev>:<path>`, so the
worktree content is not the subject of measurement (see §4 for the one exception).

### C1 — calibration (`c63_calibration.py`)

**Before (base) — expect `met=false`, exit 1**

```bash
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
```

**After (measured commit) — expect `met=true`, exit 0**

```bash
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
```

### C2 — operability (`c63_quote_tool.py`)

**Before (base) — expect `present=0 selftest=unevaluable met=false`, exit 1**

```bash
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
```

**After (measured commit) — expect `present=1 selftest=4/4 frozen_cases=ok met=true`, exit 0**

```bash
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
```

Exit-code contract (both counters, from their module docstrings and
`.ufo/waves/round-63/contract.md`): `0` = met, `1` = not met, `2` =
could-not-evaluate (git unreadable).

---

## 2. Measured outputs (all four commands actually run)

Command block run verbatim from the lane root:

```
--- C1 before (base) ---
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
--- C1 after (measured) ---
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
--- C2 before (base) ---
revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
exit=1
--- C2 after (measured) ---
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

### Byte-exact match against the committed receipts

Each live line was diffed against the corresponding committed receipt in
`.ufo/waves/round-63/controls/` (receipt lines are the `$`-command line plus the
output line plus `exit=N`; the leading `#` comment lines were excluded):

```
base-c1.txt: EXACT MATCH (exit=1)
after-c1.txt: EXACT MATCH (exit=0)
base-c2.txt: EXACT MATCH (exit=1)
after-c2.txt: EXACT MATCH (exit=0)
```

Receipt files:

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/controls/base-c1.txt`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/controls/after-c1.txt`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/controls/base-c2.txt`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/controls/after-c2.txt`

The receipts are therefore reproducible from the committed tree, not hand-written.

### Frozen-shas re-verified at the measured commit

`git show <measured>:<path> | sha256sum` against the contract's frozen values:

```
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
```

All four match the contract's frozen sha256 values. The working-tree copies at
the lane root are also byte-identical to those blobs.

### Portability of the command set

The commands are cwd-independent as long as `--root` points at the repo. Run from
`/home/vgpnk/Projects/shokunin` (the fleet root, one level above the lane) with
absolute `--root`:

```
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

Worktree cleanliness after all runs (`git status --porcelain` at the lane root):
only the pre-existing untracked wave artifacts
`.ufo/waves/round-63/w1.ready`, `.ufo/waves/round-63/w1.ready.dispatched`,
`.ufo/waves/round-63/w1/` — nothing written by these counters.

---

## 3. Independent clean-checkout reproduction

To confirm the receipts do not depend on the lane root's working tree, a fresh
clone was made in scratch (`/fast/scratch/hyaku/kake-r63/ExecCountingCommands/full`,
`toplevel` verified) and the full four-command matrix was run against it with the
worktree checked out at each rev in turn:

```
### worktree=05b0d7f revision=13d45198
C2  revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
C2 exit=1
C1  revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
C1 exit=1
### worktree=05b0d7f revision=05b0d7f4
C2  revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
C2 exit=0
C1  revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
C1 exit=0
### worktree=13d4519 revision=13d45198
C2  revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
C2 exit=1
C1  revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
C1 exit=1
### worktree=13d4519 revision=05b0d7f4
C2  revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=failed met=false
C2 exit=1
C1  revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
C1 exit=0
```

Reading of this matrix:

- **C1 is revision-pure.** Its output is identical in all four cells for a given
  `--revision`; it depends only on committed bytes (`git show <rev>:<path>`),
  never on the worktree. The after-value is a property of the measured commit.
- **C2 is worktree-sensitive** — see §4. The last cell (`worktree=base`,
  `revision=measured`) prints `selftest=failed met=false` / exit 1.

---

## 4. Finding — C2's after-value depends on the worktree, not only on the revision

This is a real, load-bearing caveat on the paste-able C2 command, and it is the
only defect-class observation this seat produced.

**Mechanism.** `c63_quote_tool.py` copies the tool blob out of the revision into a
temp dir and executes it with `cwd=root`:

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_quote_tool.py:57-64`

```python
    with tempfile.TemporaryDirectory() as tmp:
        tool = Path(tmp) / "quote_class.py"
        tool.write_bytes(tool_blob)
        proc = subprocess.run(
            [sys.executable, "-B", str(tool), "--selftest", "--json"],
            cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=False)
```

The tool then resolves every fixture against `Path.cwd()` (i.e. the worktree at
`--root`), not against the revision:

`/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py:26-28`

```python
LANE_ROOT = Path.cwd()
FIXTURES = Path("scripts/fixtures/quote-class")
```

and `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py:85-88`
(inside `run_selftest`) reads `LANE_ROOT / case["raw"]` and
`LANE_ROOT / case["text"]`.

So only the **tool code** is revision-bound; the **six fixture inputs** are
worktree-bound:

- `scripts/fixtures/quote-class/inline.raw.html`
- `scripts/fixtures/quote-class/inline.txt`
- `scripts/fixtures/quote-class/markup.raw.html`
- `scripts/fixtures/quote-class/markup.txt`
- `.ufo/waves/round-61/sources/S432.html`
- `.ufo/waves/round-63/quote-class/S432.txt`

This is deliberate and disclosed in the contract's C2 freeze note ("the frozen
tool binds fixture resolution to the invoking cwd (the lane root)") — it was the
reason the tool's sha changed `40655dd8…` → `431e75e8…`. The contract states the
predicate as *"at the measured revision, `c63_quote_tool.py` prints `present=1
selftest=4/4 frozen_cases=ok met=true`"*, and the receipt was taken with the lane
root's worktree checked out at/near the measured commit, where all six files are
present and byte-identical to the measured-commit blobs.

**Confirmed empirically.** I verified all six worktree files are byte-identical to
their measured-commit blobs at the lane root (`sha256sum` of the worktree file vs
`git show <measured>:<path> | sha256sum`), so the committed after-receipt is
faithful — the receipt does not depend on any dirty worktree content. And in the
clean clone at the measured commit, C2 prints `met=true` / exit 0.

**But the contamination channel is reachable.** Two scratch experiments, both
non-mutating to the fleet repo:

1. *Worktree supplies files the revision does not contain.* I built a scratch repo
   at the measured commit, removed `scripts/fixtures/quote-class/` and
   `.ufo/waves/round-63/quote-class/S432.txt` from the **commit** (revision
   `2891657ec091c722c1bac58ba4acfd9622ea820f` — `git ls-tree` for those paths is
   empty), then restored them into the **worktree only** as untracked files. Result:

   ```
   revision=2891657ec091c722c1bac58ba4acfd9622ea820f present=1 selftest=4/4 frozen_cases=ok met=true
   exit=0
   ```

   The counter prints `met=true` at a revision that does not contain the fixture
   files, because the worktree supplied them.

2. *Worktree removal flips the after-value red.* Deleting
   `.ufo/waves/round-63/quote-class/S432.txt` from the worktree only (revision
   untouched) turns the after-command red:

   ```
   revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=failed met=false
   exit=1
   ```

   Restoring it returns `selftest=4/4 frozen_cases=ok met=true` / exit 0.

**Risk assessment.** This is not a falsification of the committed receipts —
they are correct and reproducible, and the after-receipt was taken with a
worktree matching the measured commit. It is a *robustness* gap in the C2
predicate as written: the after-value is a joint property of (revision, worktree),
not of the revision alone. Consequences for anyone pasting the command set:

- The C2 after-command must be run with the worktree at `--root` containing the
  six fixture paths. At the lane root today they are all present and byte-equal
  to the measured commit, so the pasted command gives the contracted output.
- If the lane root's worktree is later moved to another rev (e.g. round-64 work)
  the C2 after-command may print `selftest=failed met=false` even though the
  measured revision is unchanged and correct. That is a false *red*, not a false
  green — it cannot inflate a claim, it can only deflate it.
- The false-green direction (experiment 1) requires a tree whose revision lacks
  the fixtures while the worktree supplies them — an unusual state, and it did
  not occur at the measured commit (all six files are committed there).

**Suggested remediation (not applied — this seat is read-only on the frozen
artifacts):** either (a) have `c63_quote_tool.py` materialize the six fixture
files from the revision (not the worktree) into the temp dir before invoking the
tool, or (b) state the C2 predicate explicitly as a joint
`(revision, worktree-state)` measurement and require the receipt to record a
clean `git status` for the worktree it was taken in. Option (a) makes C2 match
C1's already-revision-pure property; option (b) is cheaper and honest. Note this
would change a frozen counter's sha, which the contract forbids mid-wave, so it
belongs in a future round, not round 63.

---

## 5. Control commands re-verified (paste-able)

The contract's two C1 controls were rebuilt from scratch to confirm the control
commands in the report are paste-able and behave as the receipts state.

**Marker-only false-green control** (round-62 routed-defect fixture; corpus
copied byte-exact from
`.ufo/waves/round-62/controls/false-green-fixture/corpus/`, scratch repo
toplevel verified, rev `09ddadfa48b360ad7264401b80cd8dd834ef0d75`):

```
=== old c62 counter on marker fixture ===
revision=09ddadfa48b360ad7264401b80cd8dd834ef0d75 disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
exit=0
=== new c63 counter on marker fixture ===
revision=09ddadfa48b360ad7264401b80cd8dd834ef0d75 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

Matches the committed receipt
`.ufo/waves/round-63/controls/control-marker-fixture.txt` (old family `met=true`
/ exit 0; repaired family `met=false` / exit 1). The round-62 defect receipt
`.ufo/waves/round-62/controls/counter-false-green-l1.txt` remains the defect
history. The old `c62_calibration.py` run against the live lane root at the
measured commit prints `met=false` / exit 1 — the family defect does not fire on
the real tree.

**Junk-marker control** (adversarial markers planted, no retained blobs, no
ledger; scratch repo toplevel verified, rev
`dcc736163953d04ac37d22ae9a27fdb9e10e108b`):

```
revision=dcc736163953d04ac37d22ae9a27fdb9e10e108b disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

Matches `.ufo/waves/round-63/controls/control-junk-fixture.txt` (`met=false`,
exit 1).

**C2 stub-tool control** (tool replaced by a stub returning `ok=true` but only one
of the four frozen case ids; scratch repo toplevel verified, rev
`79d731ce2d657b56f564734cb2e73df4f5fa06e5`):

```
revision=79d731ce2d657b56f564734cb2e73df4f5fa06e5 present=1 selftest=1/1 frozen_cases=missing met=false
exit=1
```

The frozen-case-set check rejects the stub as the contract requires.

---

## 6. Edge cases measured (for the report's readers)

| Input | Command | Output | Exit |
|---|---|---|---|
| unreadable rev, C1 | `--revision deadbeef…` | `could-not-evaluate: verifier spot-check absent` | 2 |
| unreadable rev, C2 | `--revision deadbeef…` | `revision=deadbeef… present=0 selftest=unevaluable met=false` | 1 |
| non-repo root, C1 | `--root /tmp` | `could-not-evaluate: revision 05b0d7f4… unreadable` | 2 |
| non-repo root, C2 | `--root /tmp` | `could-not-evaluate: revision 05b0d7f4… unreadable` | 2 |

Note: `git rev-parse --verify <40-hex-nonexistent>` exits **0** (it echoes the
hex back without resolving it), so C2's revision probe does not catch a
nonexistent-but-well-formed SHA — it falls through to the `present=0` path and
exits 1 rather than the documented exit 2. C1 catches it by a different route
(`git show` fails → the spot-check blob reads as absent → exit 2). This is a
cosmetic inconsistency in the exit-code contract, not a claim-affecting one: an
unreadable revision yields a red, never a green, under both counters.

---

## 7. Files changed

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ExecCountingCommands.md`
  — this report (the only file written in the fleet repo).

Nothing else in the fleet repo was created, modified or deleted. Scratch fixture
repos under `/fast/scratch/hyaku/kake-r63/ExecCountingCommands/` were removed
after the measurements.

## 8. Blockers

None for the assigned item: all four commands were run and their outputs pasted
above, all four byte-match the committed receipts, the frozen shas were
re-verified at the measured commit, and the clean-checkout reproduction passed.

The one carried-forward caveat is §4: the C2 after-value is a joint
(revision, worktree) measurement, while the contract states it as a
revision-only measurement. The committed receipts are correct; the predicate's
wording is what is loose.

## 9. Tooling installs

None. No packages, binaries or PATH entries were installed or modified in this
seat; `python3` from the host was sufficient for every measurement.
