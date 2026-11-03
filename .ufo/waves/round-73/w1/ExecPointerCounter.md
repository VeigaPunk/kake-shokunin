# ExecPointerCounter — round 73 w1 (C1 counter)

Seat: executor, leaf. Scope: build the C1 counter and measure it; no lane file,
contract, corpus, control or frozen counter was edited. Committed bytes were read
with `git show --end-of-options <rev>:<path>`; the lane checkout was never mutated.

## Deliverables

| Path (absolute under the lane) | sha256 | Size |
|---|---|---|
| `.ufo/waves/round-73/w1/ExecPointerCounter/c73_wave_pointers.py` | `37025eff891635bccd03ab3a2ab6deec39f103e7d3c31759faedf7703b702e6b` | 621 lines |
| `.ufo/waves/round-73/w1/ExecPointerCounter.md` | this report | — |

The contract's counting path is `.ufo/waves/round-73/c73_wave_pointers.py`; the
integrator promotes this w1 file there before the after-state run. The counter is
standalone (stdlib only), `python3 -B`-safe, and executable.

## Predicate implemented

Identical to frozen contract C1, not restated as a new rule: C1 is met iff
`unannotated == 0`, `dead >= 2`, and every base line of `LOG.md` and
`SCORECARD.md` survives as a line-prefix of the same file at the measured
revision. Output first line:

```
C1v1 revision=<rev> pointers=<n> dead=<d> annotated=<a> unannotated=<u> append_only=<true|false> met=<bool>
```

Exit 0 met, 1 not met, 2 unevaluable, 64 usage. Detail lines follow for each dead
token and each file that failed the append-only conjunct.

## Population and the exact "names a corrected path" rule

Population at the revision: the `LOG.md` section starting at the first line
beginning `## Round 72 ` (up to, excluding, the next line beginning `## `), plus
every `SCORECARD.md` line matching `^\| 72 \|` over the whole file. Tokens are
distinct matches of `(controls|sources|w1)/[A-Za-z0-9._/-]+`, first-occurrence
order. A token is dead iff `git cat-file -e <rev>:.ufo/waves/round-72/<token>`
does not exit 0. Tokens are deduplicated; `pointers=9` at base.

Let `T` be a dead token and `F` a file that cites `T` (LOG.md and/or
SCORECARD.md). `tail(F)` is the lines of `F` at the revision whose 1-based
number is greater than the number of lines of `F` at the pinned base
`c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`. `T` is **annotated** iff one line
`L` of some `tail(F)` satisfies both:

1. **`L` names `T` exactly.** `T` occurs with the character before it not in
   `[A-Za-z0-9._-]` and the character after it not in `[A-Za-z0-9._/-]`, or at a
   line boundary. A preceding `/` is allowed, so a full
   `.ufo/waves/round-72/.../T` spelling also names `T`; `controls/x.txt.bak` and
   `xcontrols/x.txt` do not.
2. **The same line `L` names a correcting repo path `C` that resolves.**
   Candidates are every match of `\.ufo/waves/round-72/[A-Za-z0-9._/-]+` (full
   repo path) and every match of the token regex (wave-relative path). A
   candidate is tried as written and, if it ends in `.`, with exactly one
   trailing period removed (sentence punctuation). It is normalized with
   `posixpath.normpath`, must remain strictly below `.ufo/waves/round-72/` (no
   `..` escape and not the wave directory itself), must differ from `T`, and
   `git cat-file -e <rev>:C` must exit 0. Per the frozen `cat-file -e` wording,
   any resolved object (blob or tree) counts.

No other pairing is inferred: a bare errata line naming `T` with no resolving
path fails; a resolving path on a different line fails; a path outside the
round-72 wave directory fails; a dead candidate path fails. The correction must
be in the tail of a file that cites `T`. There is no `--base` override: the base
is a constant, so the frozen command cannot be shifted to an earlier base.

## Evidence (commands run from `/fast/scratch/hyaku/kake-r73/ExecPointerCounter`)

### (a) Counter selftest — exit 0

```
TMPDIR=/fast/scratch/hyaku/kake-r73/ExecPointerCounter/work \
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecPointerCounter/c73_wave_pointers.py \
  --selftest --work /fast/scratch/hyaku/kake-r73/ExecPointerCounter/work
```

Exit 0; last line `selftest 6/6`. Cases (function-level, scratch repos built by
`git init` in a `mktemp` dir with `--work`, each fixture verified with
`git rev-parse --show-toplevel`; commits use `kake-scratch`):

```
case no_dead ok: expect=annotation-met dead=0 annotated=0 unannotated=0 append_only=true annotation=met met=false
case dead_no_tail ok: expect=annotation-not-met dead=1 annotated=0 unannotated=1 append_only=true annotation=not-met met=false
case dead_bare_errata ok: expect=annotation-not-met dead=1 annotated=0 unannotated=1 append_only=true annotation=not-met met=false
case dead_correct_tail ok: expect=annotation-met dead=1 annotated=1 unannotated=0 append_only=true annotation=met met=false
case base_line_edited ok: expect=append-only-false dead=1 annotated=1 unannotated=0 append_only=false annotation=met met=false
case dead_two_annotated ok: expect=met dead=2 annotated=2 unannotated=0 append_only=true annotation=met met=true
```

The `no_dead` / `dead_correct_tail` fixtures grade the annotation conjunct, as
the seat list's "(met)" labels do; the frozen predicate also requires
`dead >= 2`, which those fixtures cannot satisfy by construction, so
`dead_two_annotated` exercises the full predicate and the exit-0 mapping. This
is a function-level reading of the fixture list, not a predicate change: the lane
run below prints `met=false` whenever `dead < 2`.

TMPDIR-only run (no `--work`):

```
TMPDIR=/fast/scratch/hyaku/kake-r73/ExecPointerCounter/tmpdir-only \
python3 -B .../c73_wave_pointers.py --selftest
```

Exit 0, `selftest 6/6`; `find "$TMPDIR" -mindepth 1 -maxdepth 1 | wc -l` → `0`
(fixtures removed).

### (b) Counter at the frozen base — dead=2, unannotated=2, exit 1

```
TMPDIR=/fast/scratch/hyaku/kake-r73/ExecPointerCounter/work \
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ExecPointerCounter/c73_wave_pointers.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision c1f3d8d4ed9470ecbaaf3353952a374b079e68cc
```

Exit `1`; output exactly:

```
C1v1 revision=c1f3d8d4ed9470ecbaaf3353952a374b079e68cc pointers=9 dead=2 annotated=0 unannotated=2 append_only=true met=false
dead unannotated citations=LOG.md:2505,SCORECARD.md:4818 token=controls/c1-tip.txt
dead unannotated citations=LOG.md:2505,SCORECARD.md:4819 token=controls/c2-tip.txt
```

The nine tokens (first occurrence): `controls/c1-base.txt`,
`controls/c2-base-red.txt`, `controls/c2-selftest.txt`,
`controls/c2-j3-control.txt`, `controls/c56-tip-linux.txt`,
`controls/j3-control.sh`, `controls/c2-j3-control-r3.txt`,
`controls/c1-tip.txt` (dead), `controls/c2-tip.txt` (dead). Seven resolve under
`.ufo/waves/round-72/`; the two `*-tip.txt` names do not (the committed names are
`controls/c1-tip-final.txt` and `controls/c2-tip-final.txt`).

Same run at lane master `4c7c53bc563a66ae0676b468966781f023ae0110` (read-only,
`git -C ... rev-parse master`): identical counts and tokens, exit 1.

### (c) c70 on the same revision — exit 0; the two tokens are invisible to it

The committed c70 was extracted from base bytes to scratch and run:

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show --end-of-options \
  c1f3d8d4ed9470ecbaaf3353952a374b079e68cc:.ufo/waves/round-70/c70_pointer_audit.py > c70_base.py
sha256sum c70_base.py   # c75444bde1d1cfdf2fabc03ef9858ae0dfddffdced765398749fda0884c99f66
python3 -B c70_base.py --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision c1f3d8d4ed9470ecbaaf3353952a374b079e68cc --work "$PWD/work"
```

Exit `0`; first line `pointers=359 dangling=17 annotated=17 unannotated=0 met=true`.
`grep -c 'controls/c1-tip\.txt\|controls/c2-tip\.txt' c70_out.txt` → `0`
(grep exit 1): c70 never sees either token. The same tokens are present on the
round-72 SCORECARD rows:

```
git -C ... show --end-of-options c1f3...:SCORECARD.md | sed -n '4818,4819p' | grep -o 'controls/[A-Za-z0-9._/-]*'
controls/c1-base.txt
controls/c1-tip.txt
controls/c2-tip.txt
controls/c2-j3-control-r3.txt
```

Blind-spot mechanism from the committed c70 source: its `repo` grammar requires
a prefix `.ufo|corpus|scripts|handoffs|considerthese/` (docstring line 14), so
`controls/...` is outside the token class; and `read_scorecard()` reads only
`SCORECARD.md` (line 80), so the LOG citations are outside its population too.

### Extra: red→green rehearsal in a scratch clone (not a round claim)

Base clone under scratch (`git clone --shared`, checkout `c1f3d8d4`), then one
commit appending to `LOG.md`:

```
- `controls/c1-tip.txt` superseded by `controls/c1-tip-final.txt` at this revision.
- `controls/c2-tip.txt` superseded by `controls/c2-tip-final.txt` at this revision.
```

Run at tip `fa7c29ead1424f802e2e87c67256a7f9771244e2`:

```
C1v1 revision=fa7c29ead1424f802e2e87c67256a7f9771244e2 pointers=9 dead=2 annotated=2 unannotated=0 append_only=true met=true
dead annotated file=LOG.md line=2511 token=controls/c1-tip.txt corrected=.ufo/waves/round-72/controls/c1-tip-final.txt
dead annotated file=LOG.md line=2512 token=controls/c2-tip.txt corrected=.ufo/waves/round-72/controls/c2-tip-final.txt
```

Exit `0`. The lane was not used for this; all edits are in the scratch clone.

### Extra: rule probes (module functions against the lane's committed base)

`corrected_paths(lane, base, line, 'controls/c1-tip.txt')`:
same-line wave-relative correction → `['.../controls/c1-tip-final.txt']`;
full repo-path correction → the same; path outside the wave dir (`corpus/SOURCES.md`)
→ `[]`; dead candidate (`controls/no-such-file.txt`) → `[]`.
`names_token`: full-path occurrence → `true`; `controls/c1-tip.txt.bak` → `false`;
`xcontrols/c1-tip.txt` → `false`.
Split lines (token on one appended line, resolving path on the next) →
`dead=1 annotated=0 unannotated=1 append_only=true met=false`, proving the
same-line requirement end to end.

### Extra: exit contracts

Bad revision `000...0` → `error: revision does not resolve to a commit: ...`,
exit `2`. Missing `--root/--revision` → usage line and
`error: --root and --revision are required`, exit `64`. `--selftest --root ...` →
`error: --selftest does not take --root/--revision`, exit `64`.

### Lane state

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --stat   # no output, exit 0
git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain .ufo/waves/round-73/w1/ExecPointerCounter/
?? .ufo/waves/round-73/w1/ExecPointerCounter/
```

No tracked lane file was modified; the deliverable path is the only new entry in
scope. No `git add/commit/checkout/reset/stash/pull/push` and no `jj` command was
run in the lane.

## Risks, limits and notes

- **Selftest labels.** The seat fixture list calls `no_dead` and
  `dead_correct_tail` "(met)"; the frozen predicate also requires `dead >= 2`, so
  those fixtures are graded on the annotation conjunct and the full-predicate
  case is `dead_two_annotated`. The counter's lane output and `met` formula are
  unchanged from the frozen predicate.
- **Base pinned.** `c1f3d8d4...` is a constant; there is no CLI base override, so
  the append-only conjunct and the tail boundary cannot be moved by a command
  variant.
- **Resolution semantics.** A corrected path is accepted iff `git cat-file -e`
  exits 0, so a tree path resolves as well as a blob path. This follows the
  frozen wording literally.
- **No semantic pairing.** A tail line naming `T` plus any resolving round-72
  path counts, even if the path is not the intended replacement for `T`; the
  frozen rule only requires both names on one appended line. The counter does not
  judge correction prose beyond resolution.
- **Population breadth.** All `^\| 72 \|` SCORECARD rows at the revision are in
  the population, including appended rows; a new round-72 row that cites a dead
  token can add to `dead`. This is the frozen procedure.
- **Reads committed bytes.** Both `LOG.md` and `SCORECARD.md` come from
  `git show`; the lane working tree and index are not consulted. A missing file
  or missing `## Round 72 ` section is exit 2 (unevaluable), not a silent zero.

## Tooling

Nothing was installed or upgraded. `pacman` was not run (host-wide pause);
`uv`/`npx` were not needed. Instruments used: git `2.56.0`, Python `3.14.8`.

## Scratch

Scratch root `/fast/scratch/hyaku/kake-r73/ExecPointerCounter/` was used for the
selftest work dir, the c70 extraction and the rehearsal clone. It was removed
before yield; `test ! -e /fast/scratch/hyaku/kake-r73/ExecPointerCounter`
returned exit 0.

## Blockers

None.
