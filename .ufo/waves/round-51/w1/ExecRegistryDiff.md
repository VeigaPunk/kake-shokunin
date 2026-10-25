# ExecRegistryDiff — is `corpus/SOURCES.md` append-only from base to tip?

Seat: `L1Kake51.ExecRegistryDiff-2` (leaf). Assigned question only: diff the base registry against the tip
registry at the **row** level, report added ids, removed ids and changed pre-existing rows. Judged axis:
freshness. Read-only; the only file written by this seat is this report.

## Verdict on the assigned question

**The registry append is append-only. Zero pre-existing rows changed.**

| measure | value |
|---|---|
| added row ids | **S262, S263** |
| removed row ids | **none** |
| changed pre-existing rows | **0** |
| base rows / tip rows | 143 / 145 (143 + 2 = 145) |
| base lines / tip lines | 256 / 258 |
| `git diff --numstat BASE TIP -- corpus/SOURCES.md` | `2	0	corpus/SOURCES.md` |

Because there are no changed pre-existing rows, **no id is named as a registry defect** — the defect-naming
clause of the assignment is vacuously satisfied. A separate, non-registry defect was found in the C2
evidence chain and is reported below under *Attack finding*, because it is the one thing that could make
the 2-row append look unproven to a reader who trusts the mirror.

## Revisions and identity

| object | blob | sha256 |
|---|---|---|
| `007d66e…:corpus/SOURCES.md` (base) | `cd448eaf06bbccefbd2e672be03355c79dd6d851` | `cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117` |
| `9d13768…:corpus/SOURCES.md` (tip) | `9e2a22175ef95a23252b349d8743cf0e5b5480fc` | `4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3` |
| `19a99bd:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` (mirror) | `9e2a22175ef95a23252b349d8743cf0e5b5480fc` | `4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3` |

Worktree `corpus/SOURCES.md` is 258 lines and `git rev-parse HEAD` = `9d13768…`, so the tip bytes are the
bytes under review (no uncommitted drift in the registry).

## Method (row level, not line level)

Rows were keyed on the `id` in field 1 and compared on the **whole raw line**, not on selected columns, so a
change to any cell, ordering, spacing or trailing whitespace in a pre-existing row would surface as
`changed`. Four independent checks were run; all agree.

1. **Keyed map diff.** Parse both revisions' rows (`^| S`), build `id -> raw line`.
   - `ADDED: ['S262', 'S263']`
   - `REMOVED: []`
   - `CHANGED pre-existing: []`
2. **Duplicate-id check.** `base dup ids []`, `tip dup ids []` — no new row shadows or duplicates an existing id.
3. **Ordering / move check.** The base id sequence is an ordered subsequence of the tip id sequence
   (`base seq is ordered subsequence of tip: True`), so no pre-existing row was reordered or moved.
4. **Byte reconstruction.** Deleting only the two new lines from the tip yields bytes equal to the base:
   `tip minus the 2 new rows == base, byte-for-byte: True` (133 780 bytes both sides).

Corroborating multiset check: `only in base: []`, `only in tip:` exactly the two new row lines
(`| S262 | Google Sear…`, `| S263 | Google Sear…`).

## Placement and shape of the two new rows

- The table region in the base is lines 9–151 (all 143 rows, verified `all(l.startswith("| S") …) = True`);
  base line 152 is blank, then the notes block.
- The new rows land at **1-based tip lines 152 and 153** — i.e. appended at the end of the row region, with
  the 114 non-row lines (header, separator, blank, notes) **byte-identical** between the two revisions
  (`non-row equal: True`). The append does not touch the notes block.
- Id order at the tail is therefore `…, S274, S286, S262, S263`. This is the pre-existing convention
  (S274/S286 already trailed S0xx–S127); appending S262/S263 after S286 is correct append-only behaviour and
  is **not** a reorder of any pre-existing row.
- Guard against the indented-row trap that `assimilation/guard/guard-registry.md` models: neither revision
  contains any indented `|` row and no line containing `| S` sits off column 0, so a column-zero parser
  (the one used here) sees the whole registry in both revisions.
- Row shape of both new rows (raw `|`-split → **11 cells** each, no literal/escaped pipe):

```
S262 | docs | A | status=mined | opened=2026-10-24 | recheck=180d | used-by=corpus/knowledge/canonical-selection.md
S263 | docs | A | status=mined | opened=2026-10-24 | recheck=180d | used-by=corpus/knowledge/crawler-identity.md
```

`used-by` names exactly one entry per row path and matches the counter's `ADOPTED` map
(`S262 -> corpus/knowledge/canonical-selection.md`, `S263 -> corpus/knowledge/crawler-identity.md`).

## Freshness spot-check on the two added rows (judged axis)

Both row URLs were probed live on 2026-10-25:

```
https://developers.google.com/search/docs/crawling-indexing/canonicalization -> 200
https://developers.google.com/search/docs/crawling-indexing/googlebot          -> 200
```

Both rows carry `opened 2026-10-24` and `recheck 180d`, so the next recheck falls inside round 51's
180-day window; the anchors record doc revisions `2026-08-20 UTC` and `2026-02-03 UTC` respectively. The
S263 anchor's `2026-02-03` revision is ~8.7 months older than the row date — that is the page's own stated
revision, not a stale row, but it is the weaker of the two freshness claims and worth a reviewer's eye.

## Attack finding — the "pre-append mirror" is the post-append registry (defect, not in the registry)

This does not change the append-only result above; it changes what the C2 counter's C8 is allowed to claim.

- The mirror path is `.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md`. It was added in
  `19a99bd` (round-51: declare the two claims, freeze both counters and commit the pre-append mirror) and
  touched by no other commit.
- Its blob at that commit is `9e2a221…`, **identical to the tip registry blob**, and its content is
  258 lines / 145 rows with `S262` and `S263` already present
  (`git show 19a99bd:.ufo/…/pre-append/corpus/SOURCES.md | grep -c '^| S262 '` → `1`).
- The lane's own `corpus/SOURCES.md` at `19a99bd` is still 256 lines / 143 rows with no `S262` — so the
  append commit `5591557` is genuine, but the snapshot taken *before* it was taken from an
  already-appended tree. The artifact named "pre-append" contains the append.
- `c51_quote_truth.py` does not read the mirror bytes for C8. Line 47 defines
  `REGISTRY = "corpus/SOURCES.md"`, line 51 defines `MIRROR = ".ufo/…/pre-append/corpus/SOURCES.md"`, and
  line 277 reads `mirror_registry = show(root, mirror_commit, REGISTRY)` — the lane registry *at* the mirror
  commit, never the mirror file.
- Consequence, evaluated by hand against the declared C8 ("the mirror's registry carries none of the adopted
  ids"): the mirror carries both, so the correct notes are
  `['S262: the mirror already carries the row', 'S263: the mirror already carries the row']` → **C8 FAIL**.
  The counter's `C8_append_after_mirror True []` is an artifact of reading the wrong path at `19a99bd`
  (where `corpus/SOURCES.md` is still the 256-line base).

Recorded counter output at the tip, for contrast:

```
python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768… --json
passed 8 True
C1_entries_exist True []          C2_entry_cites_id True []      C3_row_shape True []
C4_used_by True []                C5_gate_quote_truth True []    C6_receipt_pins True []
C7_validate_before_append True [] C8_append_after_mirror True []
```

So: **C2's `8/8` is not a valid proof of C8 as declared; evaluated against the declared bytes the condition
count is 7/8, met=False.** C1–C7 are unaffected by this path bug. Two further notes on the same evidence:

- C7's census receipt (`census-argv.txt`, `census-exit.txt` = `0`, `census-stdout.txt` = 12 `W04` duplicate-URL
  warnings + `ok <mirror path>`, no `E03`/`E04`) passes **as written**, but the file it validated is the
  post-append blob. A "validate before the append" receipt whose subject already contains the appended rows
  proves nothing about the pre-append state, even though the textual predicate is satisfied.
- The declared C8 also requires "the pre-append mirror commit is a strict ancestor of the measured revision";
  `19a99bd` *is* a strict ancestor of `9d13768`, so that clause holds. Only the "carries none of the adopted
  ids" clause fails.

## Risks

1. **Highest:** C8 is mis-scoped (line 277 / line 47 vs line 51). Any reader who trusts `8/8` inherits a false
   pre-append claim. Fixing it means either reading `MIRROR` at `mirror_commit` (which fails today) or
   committing a real pre-append snapshot and re-scoring — a scoring change, so it is the L1's call, not this
   seat's.
2. C7's receipt shares the same contaminated subject; it can stay textual-passing while proving nothing.
3. The registry itself is clean, so any wave-level "append-only" assertion can be made from base↔tip alone and
   should not be made by comparing the registry to the mirror — that comparison is currently vacuous.
4. `S263`'s anchor revision (`2026-02-03`) is the older of the two freshness anchors; a reviewer should confirm
   the page has not been superseded rather than assume 180 d still fits.

## Blockers

None. No file was unreadable; no command failed. Tool installs/upgrades: **none** (no pacman, no `uv`,
no network installs); every command used was `git show` / `git diff` / `git log` / `git rev-parse` /
`grep` / `sha256sum` / `curl -o /dev/null` / `python3 -B` reading committed bytes only. No mutating git or
`jj` command was run; scratch stayed in-memory.

## Reproduction

```
git -C <lane> show 007d66e4e8360a5f88d29a93eeedd8066dad4434:corpus/SOURCES.md > /tmp/base.md
git -C <lane> show 9d13768c4fdd0e9a2688d2ecf1616b539cf57658:corpus/SOURCES.md > /tmp/tip.md
git -C <lane> diff --numstat 007d66e4e8360a5f88d29a93eeedd8066dad4434 9d13768c4fdd0e9a2688d2ecf1616b539cf57658 -- corpus/SOURCES.md
git -C <lane> show 19a99bd:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md | grep -c '^| S262 '
git -C <lane> rev-parse 9d13768c4fdd0e9a2688d2ecf1616b539cf57658:corpus/SOURCES.md \
                        19a99bd:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md
```

## Addendum — measured state of the attempt-2 mirror repair (worktree, uncommitted, 2026-10-25)

Another seat has since rewritten the pre-append mirror **in the worktree only** (no commit; `git status`
shows `M .ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md`, plus untracked
`census-correction.txt` and `superseded/`). This seat did not perform or edit that repair; it is recorded
here because it changes what the C2 receipts would score if committed.

Measured on the repaired worktree bytes:

| item | measured value |
|---|---|
| mirror `sha256` | `cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117` = **the base registry** |
| mirror shape | 256 lines, 143 rows, `^| S262 ` count = **0** |
| `census-exit.txt` | `exit=0\n` (7 bytes) — **breaks C7**: line 260 requires `exit_text.strip() == "0"` |
| superseded `census-exit.txt` | `0\n` (2 bytes) — the shape C7 accepts |
| `census-argv.txt` / `census-stdout.txt` / `census-stderr.txt` | `cmp` **identical** to `superseded/` copies |

Three consequences that matter to the claim, none of which the registry diff itself changes:

1. **The repair is invisible to the counter until committed.** `show()` (counter lines 69–71) reads
   `git show <rev>:<path>`, i.e. committed bytes. At HEAD `9d13768` C7 still passes on the *contaminated*
   mirror; if the worktree repair is committed as-is, C7 flips to FAIL on the `exit=0` shape.
2. **A sha256 pin in the receipt is now truthful but does not bind chronology.** The census receipt was
   re-run over bytes that do hash to `cd9ee4cf…`, so pinning that digest is consistent (it would not have
   been before the rewrite, when the file hashed to `4ea81a5a…`). It proves *which bytes were validated*,
   not that those bytes existed before the append — the mirror can be rewritten at any later commit.
3. **C8 stays false even after the repair, and the repair cannot fix it.** C8 locates the mirror via
   `log --diff-filter=A … -- MIRROR`, which pins the **add** commit `19a99bd`; a new commit that modifies
   the mirror does not change that lookup, and `19a99bd`'s mirror blob is still `9e2a221…`. Making C8 bind
   requires the counter to change which commit it reads (a rule change) or history to be rewritten — not an
   evidence repair. The correction doc's sentence "C8 reads the live registry at the mirror commit, so both
   scored exactly as declared" is exactly the mis-scope documented above: C8 scores as declared only because
   its subject is the wrong file.

### Which C8 formulation actually binds, tested three ways

A peer (ReviewC2Conditions) proposed reading `MIRROR` at the *measured revision* and comparing it to
`corpus/SOURCES.md` at the mirror-add commit. Measured, that check does pass on the repaired worktree — but
it is satisfiable by the repair itself, so it certifies a reconstruction rather than a snapshot:

| formulation | at `9d13768` | on repaired worktree | binds order? |
|---|---|---|---|
| as implemented: `REGISTRY@mirror_add` (rows) | pass (vacuous) | pass (vacuous) | no — reads the wrong file |
| proposed: `MIRROR@rev` == `REGISTRY@mirror_add` | FAIL | **PASS** | no — `MIRROR@rev` is rewriteable after the append |
| honest: `MIRROR@mirror_add` == `REGISTRY@mirror_add` | **FAIL** | FAIL unless history rewritten | **yes** — both sides at one immutable commit |

Measured values behind the table: `MIRROR@19a99bd` = `9e2a221…`, `REGISTRY@19a99bd` = `cd448eaf…`, so the
honest formulation fails (they differ); `19a99bd` *is* a strict ancestor of the append commit `5591557`
(its parent), so the ancestry half already holds.

The proposed formulation is not equivalent to an ordering proof: `MIRROR@rev` is whatever the mirror says at
the measured revision, and the in-flight repair is precisely a post-append rewrite of it. Committing that
rewrite makes the proposed check pass while the only commit that ever *added* the mirror still carries the
post-append blob `9e2a221…`. Any seat can copy `REGISTRY@mirror_add` into the mirror after the append and turn
the FAIL into a PASS, so the check measures "the mirror now equals the pre-append bytes", not "it did before
the append". The honest formulation cannot be satisfied that way, because both operands are read at the same
immutable commit; it also needs ancestry measured against **the append commit**, not merely against `rev`,
or a mirror added after the append would satisfy the equality trivially.

Consequence for the claim: on this history C8 as declared is not satisfiable without rewriting history.
Either C2 scores **7/8, met=False**, or C8 is amended to the honest formulation and scores its measured FAIL.

Two mechanics for any such amendment, both measured:

- **Commit selection.** `git log` is newest-first in this lane (`corpus/SOURCES.md` returns `5591557`, then
  `ff3f6ec`, then `1c846ed`), so the counter's `mirror_commits[-1]` picks the **oldest** add. That is latent
  today — the mirror path has exactly one add event (`git log --diff-filter=DA` → `19a99bd` only; the
  in-flight repair is a workspace modification, not an add), so `[-1] == [0]`. It misjudges only after a
  delete-and-re-add re-landing, and the newest add `[0]` is the one the equality half must read.
- **The check must stay a conjunction, not the equality alone.** Equality is satisfiable *after* the append:
  a delete-and-re-add of the mirror at HEAD would give `MIRROR@add == REGISTRY@add` at 145 rows, both carrying
  S262/S263. The binding form is (a) the selected add commit is a strict ancestor of the **append** commit,
  (b) `MIRROR@add == REGISTRY@add`, (c) `MIRROR@add` carries none of the adopted ids. (a)+(b) defeats the
  post-hoc copy; (c) defeats a post-append re-add under `[0]`. On today's history (b) and (c) both fail at
  `19a99bd`: `9e2a221…` ≠ `cd448eaf…`, with S262 and S263 present.

Reachability is real but constrained: a fresh landing that re-adds the mirror while the registry is still at
143 rows, followed by a separate append, satisfies (a)–(c) with no history rewrite. The re-add must precede
the append in history — a re-landing of the wave, not a patch on top of `5591557` (registry already 145 rows).
That is why the current worktree repair cannot reach it.

Worktree state at the time of writing: `census-exit.txt` has been restored to the bare `0\n`, so the C7 shape
risk above is currently cleared (uncommitted); a new untracked `census-count-argv/stdout/stderr/exit` receipt
set (its exit file is likewise bare `0\n`) reports `file rows 143`, tier A 120 / B 6 / C 17 — a genuine content
discriminator (the contaminated mirror reports 145 rows), though still a byte-level, not ordering, binding.
`HEAD` was still `9d13768` and `corpus/SOURCES.md` clean (145 rows) at the last check, so every measurement above
remains pinned to the tip that was scored.
