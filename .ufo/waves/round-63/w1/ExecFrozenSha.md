# ExecFrozenSha — round-63 frozen sha256 re-derivation at the measured commit

Seat scope (assigned item): recompute sha256 of `c63_calibration.py`, `c63_quote_tool.py`,
`quote-classes.json` and `scripts/quote_class.py` at the measured commit with
`git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:<path> | sha256sum` and compare to the
contract's frozen values; report any mismatch.

Verdict: **PASS — all four frozen sha256 values match exactly. Zero mismatches.**
One additional finding (not a mismatch): the C2 counter is **not revision-pure for the
selftest fixtures**, and a hardcoded-output stub tool satisfies it. Details in §4.

No tools installed. No fleet-repo, `.ufo/state`, `scripts/`, `templates/`, sibling-repo or
corpus/`SOURCES.md` writes. The only file written by this seat is this report.
Scratch fixtures were created under `/fast/scratch/hyaku/kake-r63/ExecFrozenSha/`, each
verified with `git -C "$D" rev-parse --show-toplevel` before its first commit, and the whole
directory was deleted afterwards (`scratch_cleanup=clean`).

Fleet root: `/home/vgpnk/Projects/shokunin/kake-shokunin` (all relative paths below are
relative to it).

## 1. Frozen sha256 re-derivation at the measured commit — the assigned item

Command (exactly the assigned recipe, one path per loop iteration):

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin && for p in \
  .ufo/waves/round-63/c63_calibration.py \
  .ufo/waves/round-63/c63_quote_tool.py \
  .ufo/waves/round-63/quote-class/quote-classes.json \
  scripts/quote_class.py; do \
  printf '%s  ' "$(git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:$p | sha256sum | cut -d' ' -f1)"; \
  echo "$p"; done
```

Output:

```
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
```

Comparison against the contract (`.ufo/waves/round-63/contract.md`):

| Path | Contract frozen sha256 | Recomputed | Result |
|---|---|---|---|
| `.ufo/waves/round-63/c63_calibration.py` | `bcd16f68…ea3fc91` (contract.md:29) | `bcd16f68…ea3fc91` | **MATCH** |
| `.ufo/waves/round-63/c63_quote_tool.py` | `9fcbfad0…eaa7f01e` (contract.md:66) | `9fcbfad0…eaa7f01e` | **MATCH** |
| `.ufo/waves/round-63/quote-class/quote-classes.json` | `5f48e26b…010c42d` (contract.md:41) | `5f48e26b…010c42d` | **MATCH** |
| `scripts/quote_class.py` | `431e75e8…841f14` (contract.md:56) | `431e75e8…841f14` | **MATCH** |

**No mismatch in any of the four.**

Cross-check by exact blob bytes (`git cat-file blob`, bypassing the `git show` pipeline):

```
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  7369 bytes  8a4c3288578c8b583d4bf599151b927cfe905311
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  3230 bytes  db04d6727434315be2ae81dc8e5e27beb58f51d9
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  1039 bytes  7b2a907b290bd215f22109bc824ea38a80d88dc9
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  4914 bytes  66b55109efe902091058554ab1b1c85933e886cf
```

All four are worktree-clean as well — the checked-out copies are byte-identical to the
committed blobs, so a counter run against the worktree executes the frozen bytes:

```
.ufo/waves/round-63/c63_calibration.py                       IDENTICAL
.ufo/waves/round-63/c63_quote_tool.py                         IDENTICAL
.ufo/waves/round-63/quote-class/quote-classes.json            IDENTICAL
scripts/quote_class.py                                        IDENTICAL
```

### 1a. Every 64-hex literal in the contract is accounted for

`contract.md` contains exactly five 64-hex values. Mapping each to the file it names at the
measured commit (full-tree `git ls-tree -r` + `git show … | sha256sum` sweep):

```
40655dd87ab026fad29648bb784493d010b922b8a93dcf792f618186f2ef88a1 -> <no file at measured commit (prior-version value)>
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14 -> scripts/quote_class.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d -> .ufo/waves/round-63/quote-class/quote-classes.json
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e -> .ufo/waves/round-63/c63_quote_tool.py
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91 -> .ufo/waves/round-63/c63_calibration.py
```

The one non-file value is the contract's **prior-version** tool sha, quoted in the freeze
note at contract.md:61. It is not a live claim; §2 verifies it independently.

## 2. The contract's freeze-note sha change is honest

contract.md:58-64 states the tool sha changed `40655dd8…` → `431e75e8…` "for this reason
only; the selftest case set and expectations are unchanged". Both halves verified.

**(a) The prior sha is real.** `scripts/quote_class.py` exists in the round-63 freeze commit
`6d8c52a6b232b306cd5bda9be9339d036f120c61` (parent = the declared base `13d45198…`), with
sha256 exactly `40655dd8…f88a1`:

```
$ git log --oneline --all -- scripts/quote_class.py
05b0d7f4 round-63: bind quote-class tool fixtures to cwd; contract freeze-note (pre-wave)
d990b442
06cfd360
6d8c52a6 round-63: freeze contract; semantics-binding calibration counter; quote-class tool; S432 collapsed-only correction
c5459a38
e92ef6f6
```

```
$ git show 6d8c52a6:scripts/quote_class.py | sha256sum
40655dd87ab026fad29648bb784493d010b922b8a93dcf792f618186f2ef88a1  -
```

Note: the tool does **not** exist at the declared base `13d45198…` — `git show
13d45198…:scripts/quote_class.py` fails with `fatal: path 'scripts/quote_class.py' exists on
disk, but not in '13d45198…'`. That is consistent with `base-c2.txt` (`present=0 met=false`)
and with C2's base half of the predicate; the tool was introduced in the round-63 freeze
commit, one commit after the base.

**(b) The change is exactly one line, and the selftest case set/expectations are unchanged.**
`git diff 6d8c52a6 05b0d7f4 -- scripts/quote_class.py` is a single hunk:

```diff
-LANE_ROOT = Path(__file__).resolve().parent.parent
+LANE_ROOT = Path.cwd()
```

The full change set of that commit is exactly two paths:

```
M	.ufo/waves/round-63/contract.md
M	scripts/quote_class.py
```

`FIXTURE_CASES` (the four ids `inline_raw_substring`, `markup_collapsed_only`,
`absent_everywhere`, `s432_real`) and their `expected` values are byte-for-byte untouched
between the two versions. The freeze-note claim is **confirmed**.

## 3. Receipts reproduce from the frozen bytes

Counting commands from contract.md:35 and contract.md:72, run in the fleet root:

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0

$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
exit=1
```

All four lines match the committed receipts `.ufo/waves/round-63/controls/after-c1.txt`,
`after-c2.txt`, `base-c1.txt`, `base-c2.txt` character-for-character, including exit codes.

Reproduced again in a **pristine checkout** of the measured commit (fresh `git init` +
`git fetch origin 05b0d7f4` + `git checkout 05b0d7f4`, run with `cwd` = that clean tree),
confirming the greens are not an artifact of the fleet worktree's state:

```
=== C2 in PRISTINE checkout at measured commit (cwd=clean tree) ===
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit= 0

=== C1 in PRISTINE checkout at measured commit ===
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit= 0
```

### 3a. C1 marker-fixture control reproduces, and the routed defect is genuinely repaired

Built the marker-only fixture by copying the committed
`.ufo/waves/round-62/controls/false-green-fixture/corpus/` byte-exact into a scratch repo
(`git init -q`, top-level verified equal to `$D` before the first commit, throwaway identity
inside the fixture only). The five copied files' sha256s match those recorded in the round-62
defect receipt `.ufo/waves/round-62/controls/counter-false-green-l1.txt` exactly:

```
635089aadf398ea2b17799494c5a0e209af3f87a4459234e71892d29351ba6b6  .../knowledge/response-header-expectations.md
0a9a034861b19ba9f0c2b49adb9e9c394b406816a63dc458b1b8ee62668405c3  .../lessons/round-61-verifier-spotcheck.md
d7033c6dc40448844e9c652900fb54298de8af539c8e45819e29d377bb1a8923  .../lessons/round-62.md
373b9d254dff8668f9ae273e3f24ec87ff9b52f2c862ebabd158d76ad64d0457  .../QUALITY.md
a27f4338e565e5231b48adb49c24f759612f8827927cd80cf838462ff4dd8d2b  .../SOURCES.md
```

Old c62 vs new c63 on that same fixture (`revision=e2dd3de045547f767eb3f93b3019721802620dc7`):

```
--- OLD c62 on marker fixture ---
revision=e2dd3de045547f767eb3f93b3019721802620dc7 disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
exit= 0

--- NEW c63 on marker fixture ---
revision=e2dd3de045547f767eb3f93b3019721802620dc7 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit= 1
```

The round-62 routed defect (marker-only green) is dead under c63: the marker fixture now
prints `met=false` (exit 1) while the old family member still prints `met=true` (exit 0).
This independently reproduces `controls/control-marker-fixture.txt`.

**C1 is revision-pure** (it reads every input through `git_show`, never the worktree). Probe:
a scratch repo whose only commit is the marker-only corpus, with the *full correct* corpus,
ledger and retained blobs planted untracked in the worktree — the counter still reads the
revision and refuses:

```
C1 at marker-only revision, worktree polluted with full correct corpus:
revision=833105d7fd30537058012bd9170daf7dbf3d7f2e disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit= 1
```

### 3b. The class ledger is independently re-derivable (not merely asserted)

Re-running the committed recipe `.ufo/waves/round-63/quote-class/extract_text.py` on the
retained HTML blob reproduces the committed flat-text rendering **byte-identically**:

```
$ python3 -B .ufo/waves/round-63/quote-class/extract_text.py --raw .ufo/waves/round-61/sources/S432.html --out <scratch>/S432.derived.txt
extracted 1854393 bytes -> 286933 chars
derived sha256 : 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
committed sha256: 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
BYTE-IDENTICAL: True
```

And the class derivation from the two retained blobs:

```
raw contains span as raw substring?  False
text contains span as substring?   True
=> class: collapsed-only
```

The ledger's declared `rawSha256` / `textSha256` match the actual blobs, and the ledger
`quote` is byte-identical to the counter's `FROZEN_QUOTE`. The ledger is self-consistent
and re-derivable, so C1's `blobs_match=1 / derived=collapsed-only / class_match=1` reflects
a real derivation, not an asserted constant.

## 4. Findings beyond the assigned sha comparison

These are **not** sha mismatches and do not contradict the contract's frozen values. They are
robustness observations about the C2 counter, surfaced because the sha verification is the
gate that makes the tool's identity checkable and any weakness in it is worth recording.

### 4a. The C2 counter's selftest fixtures come from the **worktree**, not the revision

`c63_quote_tool.py` reads the *tool* from the revision (`git_show(root, rev, TOOL_REL)`,
line 56) but executes it with `cwd=root` (line 66). The frozen tool then resolves its
fixtures via `LANE_ROOT = Path.cwd()` (scripts/quote_class.py:24) — i.e. the **worktree**,
not the revision. So the counter's selftest evidence is not revision-bound, even though the
tool bytes are.

Probe A — a revision containing **only** the tool and no fixtures at all, with the fixture
files present untracked in the worktree:

```
=== D1: worktree HAS fixtures, revision A does NOT ===
revision=b955790af1f56e20612592b84389ba4798df22b2 present=1 selftest=4/4 frozen_cases=ok met=true
exit= 0

=== D3: worktree CLEAN, revision A does NOT ===
revision=b955790af1f56e20612592b84389ba4798df22b2 present=1 selftest=failed met=false
exit= 1

  revision A contains scripts/fixtures/quote-class/inline.raw.html? NO
  revision A contains scripts/fixtures/quote-class/inline.txt? NO
  revision A contains scripts/fixtures/quote-class/markup.raw.html? NO
  revision A contains scripts/fixtures/quote-class/markup.txt? NO
  revision A contains .ufo/waves/round-61/sources/S432.html? NO
  revision A contains .ufo/waves/round-63/quote-class/S432.txt? NO
```

Probe B — the decisive form: a revision whose **own** `S432.txt` is corrupt (so the
`s432_real` case genuinely cannot pass at that revision), with the correct file supplied
only through the worktree:

```
revB S432.txt sha256: f6a9525b15638d67838ab9b96c0e16ae75eb715b8df85541648ec0f06ec89761   (revision's own bytes)
worktree S432.txt sha256: 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69   (correct bytes)
real   S432.txt sha256: 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69

=== C2 counter at revB (revision's own S432.txt is CORRUPT) ===
revision=d5deac9531a0e514685235aedc4529e91b7b3cce present=1 selftest=4/4 frozen_cases=ok met=true
exit= 0

=== C2 counter at same revB, worktree reset to corrupt revision state ===
revision=d5deac9531a0e514685235aedc4529e91b7b3cce present=1 selftest=failed met=false
exit= 1
```

The counter reports `selftest=4/4 frozen_cases=ok met=true` for a revision whose own
retained blob is corrupt — the green is supplied by the worktree. It also fails *closed* in
the other direction (deleting `scripts/fixtures/quote-class/markup.txt` from a pristine
measured-commit checkout flips it to `selftest=failed met=false`, exit 1).

**Scope of this finding.** At the *measured* commit the worktree copies of all six fixture
files are byte-identical to the revision's (verified: `SAME` for
`scripts/fixtures/quote-class/{inline.raw.html,inline.txt,markup.raw.html,markup.txt}`,
`.ufo/waves/round-61/sources/S432.html`, `.ufo/waves/round-63/quote-class/S432.txt`), and
the green reproduces in a pristine checkout (§3). So the committed `after-c2.txt` receipt is
**not falsified** — the counter's green is correct at the measured commit. The finding is that
the counter does not *prove* revision-binding: it would have accepted a green on a tree
whose revision does not support it. C1 does not have this weakness (§3a). Under C2's kill
rule ("if the after receipt does not print `met=true`, or a stub tool passes, C2 is
`unprovable`") this is a *counter-strength* concern, not a trigger: the after receipt does
print `met=true`, and the measured commit's tool is the real, sha-pinned tool.

### 4b. The counter accepts a stub that hardcodes the expected answers

The contract's stated control is that "the counter's frozen-case-set check rejects a stub
selftest missing the four frozen case ids". That control works as stated — and it also
rejects a stub whose `derived` disagrees with `expected`:

```
A) stub MISSING frozen case ids (contract's stated control):
    revision=19efef51cf5a257df67d27661f53d6c1c5b99f58 present=1 selftest=failed met=false  exit= 1
B) stub WITH all 4 ids but derived != expected:
    revision=b712fc90e385038a396928dabc8d6eebeb4986f3 present=1 selftest=4/4 frozen_cases=missing met=false  exit= 1
```

But a stub that prints the four frozen ids with `derived == expected` **hardcoded**, reading
no blob and performing no derivation, is accepted:

```
C') VALID hardcoded stub (all 4 ids, derived==expected, reads no blobs):
    revision=3667a0275b383484bdb4cb38712f25202d58419f present=1 selftest=4/4 frozen_cases=ok met=true
    exit= 0
```

This is a genuine limitation of the counter's construction: it validates the *shape* of the
tool's self-report, not that the tool derived anything. The contract's own kill rule names
"a stub tool passes" as an `unprovable` trigger — the check as written does not detect a
fully-hardcoded stub. What *does* rule the stub out at the measured commit is the sha256
pinning verified in §1: `scripts/quote_class.py` at `05b0d7f4` hashes to
`431e75e8…841f14`, and that byte-for-byte file is the genuine classifier (it reads the
blobs and implements `classify()`). **The sha256 freeze is the load-bearing control for C2**,
not the counter's stub check. Had the tool's bytes not been pinned, §4b would have been
directly exploitable.

### 4c. The counters do not self-pin their own sha256

Neither counter contains any 64-hex constant (only the base revision literal
`BASE = "13d4519818db28cd0aa912e49020659140d7b9fa"` in each, at `c63_calibration.py:40` and
`c63_quote_tool.py:23`), and `scripts/quote_class.py` contains none. The counters also do
not verify the sha256 of the artifacts they consume (the ledger's `5f48e26b…` is not
checked against a literal — the ledger's *blob* hashes are re-derived instead, which is
strictly stronger for the retained blobs, but the ledger file's own sha256 is not pinned by
the counter). The frozen sha256 values in contract.md are therefore enforced only by
out-of-band verification — which is exactly what this seat performed in §1.

## 5. No-harm checks

```
$ git diff --name-status 13d45198 05b0d7f4
A	.ufo/waves/round-63/c63_calibration.py
A	.ufo/waves/round-63/c63_quote_tool.py
A	.ufo/waves/round-63/contract.md
A	.ufo/waves/round-63/controls/base-c1.txt
A	.ufo/waves/round-63/controls/base-c2.txt
A	.ufo/waves/round-63/controls/control-junk-fixture.txt
A	.ufo/waves/round-63/controls/control-marker-fixture.txt
A	.ufo/waves/round-63/quote-class/S432.txt
A	.ufo/waves/round-63/quote-class/extract_text.py
A	.ufo/waves/round-63/quote-class/quote-classes.json
A	.ufo/waves/round-63/sources/S432.live.html
M	corpus/QUALITY.md
M	corpus/knowledge/response-header-expectations.md
A	corpus/lessons/round-63.md
A	scripts/fixtures/quote-class/inline.raw.html
A	scripts/fixtures/quote-class/inline.txt
A	scripts/fixtures/quote-class/markup.raw.html
A	scripts/fixtures/quote-class/markup.txt
A	scripts/quote_class.py
```

All changes are additions or appends; `corpus/SOURCES.md` is **not** in the change set, and
the S432 registry row is byte-identical between base and the measured commit:

```
$ diff <(git show 13d45198:corpus/SOURCES.md | grep -n "S432") \
       <(git show 05b0d7f4:corpus/SOURCES.md | grep -n "S432")
S432 row IDENTICAL base vs measured
```

The measured commit is an ancestor of `HEAD` (`15eb965c`), and the after-receipts are a
separate later commit (`7f77d12b`), consistent with the contract's "all receipts below commit
before any after-state measurement" ordering in structure — the receipts were committed
*after* the measured commit they attest, and neither the measured commit nor the receipts
modify any frozen artifact (all four frozen paths are `UNCHANGED` between `05b0d7f4` and
`HEAD`).

## 6. Scope discipline

- No writes outside this report. No commits, no push, no mutating git/jj anywhere. The
  fleet repo's only git operations were read-only (`show`, `ls-tree`, `cat-file`, `log`,
  `rev-parse`, `merge-base`, `diff`, `status`).
- No fixture was created inside the fleet repo, `.ufo/state`, `scripts/`, `templates/`, a
  sibling repo, or this lane's corpus/`SOURCES.md`.
- `considerthese/` untouched; `MANIFEST.json` untouched.
- No pacman transaction was run; no tool was installed (nothing in this task needed one).
- Scratch fixtures lived only under `/fast/scratch/hyaku/kake-r63/ExecFrozenSha/` and were
  deleted (`scratch_cleanup=clean`). Each was `git init -q`'d with `git -C "$D" rev-parse
  --show-toplevel` asserted equal to `$D` before its first commit, and used a throwaway
  identity (`t@t.invalid` / `throwaway`) configured inside that scratch repo only.

## 7. Summary

| Check | Result |
|---|---|
| `c63_calibration.py` sha256 at `05b0d7f4` vs contract | **MATCH** (`bcd16f68…ea3fc91`) |
| `c63_quote_tool.py` sha256 at `05b0d7f4` vs contract | **MATCH** (`9fcbfad0…eaa7f01e`) |
| `quote-classes.json` sha256 at `05b0d7f4` vs contract | **MATCH** (`5f48e26b…010c42d`) |
| `scripts/quote_class.py` sha256 at `05b0d7f4` vs contract | **MATCH** (`431e75e8…841f14`) |
| **Mismatches reported** | **NONE** |
| Contract's prior-version sha `40655dd8…` | verified real at `6d8c52a6`; change is exactly the one `LANE_ROOT` line; selftest cases/expectations unchanged |
| All four receipts reproduce | yes, including exit codes, and in a pristine checkout |
| C1 marker-fixture control | reproduced (old c62 `met=true` / new c63 `met=false`) |
| Ledger re-derivation | `extract_text.py` reproduces `S432.txt` byte-identically; class derives `collapsed-only` |
| C2 counter weakness (§4a, §4b) | fixtures resolved from worktree not revision; a hardcoded-answer stub passes the counter. Receipts at the measured commit are unaffected (fixtures byte-identical to the revision there, and the tool is sha-pinned). |
