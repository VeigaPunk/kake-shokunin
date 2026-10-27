# MutResolverSelftest

Seat: mutation tester of the lane tool's own `--selftest` (`scripts/id_resolver.py`, lane HEAD
`cb68527`, blob sha256 `2c1b4970a652023a883a414620c07cf393f7c4b28b87053564a45302428e663a`).

Method: each mutant is a single-point text edit applied to a **copy** of the tool; the detector is
that copy's own `--selftest` (59 checks). A mutant still printing `selftest: 59/59` and exiting 0
is a **survivor**. Every survivor was re-run on a purpose-built fixture against the pristine tool
to separate a real behavioural difference from an inert mutant (`probe.py`, `probe2.py`,
`final.py`), and a candidate case was checked to PASS on the pristine tool and FAIL on its mutant
(`candidates.py`, `cand_m39.py`). All of it ran in `/fast/scratch/hyaku/kake-r59/MutResolverSelftest/`
(deleted on exit); the lane file was never opened for writing.

Detector control: pristine copy `--selftest` → `selftest: 59/59`, exit 0, re-run before every
batch. Round-counter control: `c59_resolver_cases.py --root <lane> --revision fd6303c` →
`13/21 met=False`, exit 1 — matching the contract's base control, so the measured revision was the
contracted one.

**40 mutants, 22 killed, 18 survived.** Killed per area: parse_registry 4, fence machine 1,
knowledge walk 3, revision path parse 3, sibling registry 3, evaluate 5, render 2, parse_cited 1.
Survived per area: parse_registry 3, fence machine 4, knowledge walk 4, revision path parse 3,
sibling registry 1, evaluate 2, render 1.

## MUTANTS:

Full ledger with per-mutant sha256, tally and first failing case names:
`MutResolverSelftest.files/mutants.json`; harness `MutResolverSelftest.files/mutate.py`.
`K 58/59 (04)` = killed, 58 of 59 checks passed, first failing selftest case 04.

**parse_registry** — M01 `ROW_RE` accepts 4 leading spaces (4-space code row registered) K 58/59 (04);
M02 `ID_CELL_RE` accepts 2 digits (registry cell `S12` registers) SURVIVED; M03 `SECTION_END_RE`
accepts level 1–6 headings SURVIVED; M08 registry URL keeps its trailing punctuation K 58/59 (46);
M09 URLs read from every cell of the row, not only the source cell SURVIVED; M29 registry row must
start at column 0 (indented rows dropped) K 56/59 (02, 03); M38 3-space indented registry row
ignored K 57/59 (03, 25).

**fence machine** — M04 `FENCE_OPEN_RE` opener may be indented 4 spaces SURVIVED; M05 closing run
must be exactly the opener length K 58/59 (54); M06 closing run may use the other fence character
SURVIVED; M07 backtick fence may carry a backtick in its info string SURVIVED; M35 closing run may
not carry trailing whitespace SURVIVED.

**knowledge walk** — M10 per-file lane guard dropped (symlinked file outside the lane read) K 58/59
(49); M11 `.markdown` knowledge files are walked SURVIVED; M12 cited path relative to the knowledge
dir, not the lane root K 54/59 (22, 23); M13 knowledge-dir lane guard dropped (`inside(base)`
unchecked) SURVIVED; M31 revision mode accepts an empty knowledge set SURVIVED; M39 the knowledge
walk follows symlinked directories SURVIVED; M40 compound: follows symlinked dirs **and** drops the
per-file lane guard K 58/59 (49).

**revision path parse** — M14 revision paths decoded with `surrogateescape` SURVIVED; M15 NUL split
replaced by newline split K 53/59 (15, 20); M16 `ls-tree` drops `--name-only` (raw tree format) K
53/59 (15, 20); M17 revision resolves to a tree, not a commit SURVIVED; M18 inherited `GIT_*` env
passed on to git K 58/59 (48); M33 knowledge prefix matched without the path separator SURVIVED.

**sibling registry** — M19 sibling repo without a committed registry falls back to its worktree
file K 58/59 (40); M20 lane excluded from siblings by path string, not by realpath K 58/59 (15);
M21 sibling directory need not carry the `-shokunin` suffix K 58/59 (38); M34 a linked git
worktree (`.git` a file) read from its worktree file SURVIVED.

**evaluate** — M22 default fleet root is the **grandparent** of `--root` SURVIVED; M23 a missing
fleet directory is not unevaluable K 58/59 (43); M24 `owned_elsewhere` counts url-match owners,
not registry owners K 57/59 (13, 25); M25 url-match looks only at the first citing file K 58/59
(45); M28 dangling ids are not sorted (set order kept) SURVIVED (flaky, below); M30 revision mode
reads the working-tree registry, not the revision blob K 57/59 (15, 20); M36 `ids_resolved` counts
the registry size, not resolved citations K 43/59 (07, 08).

**render** — M26 empty owners print as an empty field instead of `-` K 58/59 (24); M27 summary-line
field order swapped K 58/59 (24); M37 `unowned` printed as the dangling count SURVIVED.

**parse_cited** — M32 cited id needs no left word boundary K 56/59 (09, 25).

M39 combined with a dropped per-file guard is exactly M40 (killed by the existing case 49), so that
fence holds; M39's blind spot is that *no* case pins symlinked-directory behaviour either way.

## SURVIVORS:

18 survivors, each re-checked on a fixture against the pristine tool. **DIFFERENT** = the mutant
changes the tool's output (a real blind spot); **SAME** = behaviourally inert at the contract
surface (equivalent mutant — a reasoning gap, not a behavioural one). Observed pristine → mutant:

1. **M14 — revision paths decoded with `surrogateescape` not `replace`.** DIFFERENT. Pristine
   `exit=2 unevaluable: cannot read corpus/knowledge/bad?.md at <rev>` → mutant `exit=1 DANGLING
   S777 cited-by=corpus/knowledge/bad?.md`. This is the **K13 route**: the pristine tool cannot read
   a non-UTF-8 file name at a revision — it exits 2 where the counter demands exit 1 with the id
   resolved. The counter catches it (K13 FAILS at base, PASSES on the mutant); the tool's own
   selftest cannot see it — no non-UTF-8 path fixture among the 59.
2. **M39 — `os.walk(base, followlinks=True)`.** DIFFERENT on the K10 fixture: pristine `ids_cited=1`
   (in-lane symlinked knowledge dir not walked) → mutant `ids_cited=2 dangling=1` (walked). The
   **K10 route**; pristine fails K10 at the counter too. The selftest has a symlinked *file* case
   (49) but no symlinked *directory* case.
3. **M33 — `rel.startswith(KNOWLEDGE_REL)` without the `/`.** DIFFERENT: pristine `ids_cited=1` →
   mutant `ids_cited=2 DANGLING S777 cited-by=corpus/knowledge-notes/b.md`.
   `corpus/knowledge-notes/` is not under `corpus/knowledge/`; no case distinguishes them.
4. **M11 — `.markdown` files are walked.** DIFFERENT: pristine `exit=2 … corpus/knowledge/**/*.md
   empty` → mutant `exit=1 DANGLING S777 cited-by=corpus/knowledge/a.markdown`. The docstring scopes
   citations to `**/*.md`; the contract lists `.markdown` as counter-ambiguous; the selftest pins
   neither.
5. **M03 — any level-1–6 heading ends the Registry section.** DIFFERENT: pristine `ids_resolved=2`
   (a `### Sub` heading does not end it) → mutant `ids_resolved=1 DANGLING S002`. Only `##` as a
   section end is covered (case 33).
6. **M04 — opener may be indented 4 spaces.** DIFFERENT: pristine `ids_resolved=2` → mutant
   `ids_resolved=1 DANGLING S002`. CommonMark: a 4-space indented fence is code, not a fence. A
   3-space opener is covered (case 53); the 4-space boundary is not.
7. **M06 — closing run may use the other fence character.** DIFFERENT: pristine `ids_resolved=1` (a
   backtick run does not close a tilde fence) → mutant `ids_resolved=2 DANGLING S002`. Backtick and
   tilde fences are covered separately (cases 51, 52); a mixed pair never is.
8. **M07 — backtick fence may carry a backtick in its info string.** DIFFERENT: pristine
   `ids_resolved=2` (a backtick-bearing info string is not a fence) → mutant `ids_resolved=1 DANGLING
   S002`. The CommonMark rule the tool documents is untested.
9. **M35 — closing run may not carry trailing whitespace.** DIFFERENT: pristine `ids_resolved=2` (a
   run with trailing spaces closes the fence) → mutant `ids_resolved=1 DANGLING S002,S003`.
10. **M09 — URLs read from every cell of the row.** DIFFERENT: pristine `owners=alpha-shokunin
    url-match=-` → mutant `url-match=alpha-shokunin` — a URL in the `used-by` cell of a *sibling's*
    row becomes a source URL. The docstring says "source cell"; unpinned.
11. **M22 — default fleet root is the grandparent of `--root`.** DIFFERENT: pristine
    `owners=alpha-shokunin` (default = parent of `--root`, as documented) → mutant `owners=-`. All
    59 cases pass `--fleet` explicitly, so the documented default is untested.
12. **M31 — revision mode accepts an empty knowledge set.** DIFFERENT: pristine `exit=2 … no
    knowledge file at <rev>` → mutant `exit=0 ids_cited=0 dangling=0` — a false green. The
    worktree path has the matching case (19); the revision path does not.
13. **M17 — the revision resolves to a tree, not a commit.** DIFFERENT: pristine `exit=2
    unevaluable: revision '<sha>' unresolved` → mutant `exit=0 ids_resolved=1`. A tree-ish revision
    is accepted and measured. Case 17 covers an *unresolved* revision, never a wrong-type one.
14. **M34 — a linked git worktree (`.git` a file) is read from its worktree file.** DIFFERENT:
    pristine `owners=alpha-shokunin,beta-shokunin` (linked worktree read at HEAD) → mutant
    `owners=alpha-shokunin` (its dirty file trusted). Case 39 pins the dirty-worktree rule for a
    `.git` *directory* only.
15. **M37 — `unowned` printed as the dangling count.** DIFFERENT: pristine `owned_elsewhere=1
    unowned=1` → mutant `unowned=2`. The exact-line case (24) only ever has `owned_elsewhere=0`,
    where the two are equal.
16. **M13 — knowledge-dir lane guard dropped.** DIFFERENT in the message only: pristine `exit=2 …
    no knowledge file: corpus/knowledge absent` → mutant `exit=2 … no knowledge file:
    corpus/knowledge/**/*.md empty`. Same exit code and same refusal — inert at the contract
    surface, but the message is unpinned.
17. **M02 — a 2-digit registry cell registers.** SAME (inert): a `S12` row can never be cited (the
    cited-id regex needs 3+ digits), so no output differs.
18. **M28 — dangling ids are not sorted.** SURVIVED in the harness run but is a **flaky kill**: over
    40 fixed `PYTHONHASHSEED` values it fails 38 times (56/59 or 57/59) and survives twice, because
    the exposed set-iteration order sometimes coincides with sorted order for that fixture. Pristine
    is 59/59 at all 40 seeds. The unsorted-order case (47) therefore depends on hash luck and
    cannot be relied on as a detector.

Cross-check against the round's own counter (`crosscheck2.py`; discriminating cases K1–K7, P1–P5,
P7 — the ones that pass on the pristine tool): of the 18 survivors the counter catches **none**. Its
kills on the mutant set came only from K8–K14 and P6, which already fail on the pristine tool at
base and so discriminate nothing. The C2 counter and the tool's own 59-case selftest are blind to
the same 18 behaviours.

## CASES TO ADD:

The C2 fix should add cases to `scripts/id_resolver.py`'s own `--selftest`. Each is written and
verified: PASS on the pristine tool, FAIL on its mutant (`candidates.py`, `cand_m39.py`); the route
cases that must be RED on the current tool are marked (verified by `kcand.py`, which reproduces the
counter's K-cases against the pristine tool). Adding them also lifts the selftest count past the
counter's P6 floor of 66 (59 today).

Route cases the fix must add (RED on the current tool):
1. **HTML-comment registry row is not registered** (K8) — a `<!-- … -->` block around a row must not
   register the id; expected `(2 cited, 1 dangling)`. Currently `ids_resolved=2` — RED.
2. **A setext H2 ends the Registry section** (K9) — expected `(2 cited, 1 dangling)`. Currently
   `ids_resolved=2` — RED.
3. **An in-lane symlinked knowledge directory is read** (K10) — `corpus/knowledge/linked →
   ../notes_store` inside the lane must contribute its citations; expected `(2 cited, 1 dangling)`.
   Currently `ids_cited=1` — RED. Kills M39.
4. **A committed symlink at a revision is resolved inside the tree** (K11).
5. **A registry symlinked out of the lane is unevaluable** (K12) — expected `exit=2`, never a clean
   `ids_cited=…`. Currently `exit=0` — RED.
6. **A non-UTF-8 knowledge file name at a revision is read, not fatal** (K13) — expected `exit=1`
   with the id cited; pristine gives `exit=2 cannot read corpus/knowledge/bad?.md`. Kills M14 and
   pins the decode choice (`surrogateescape` vs `replace`).
7. **A `--root` below a repository toplevel is unevaluable** (K14) — expected `exit=2`. Currently
   `exit=0` — RED.

Blind-spot cases the fix should add (GREEN on the pristine tool; each kills one survivor):
8. A level-3 heading does not end the Registry section — kills M03. 9. A 4-space indented fence is
   code, not a fence — kills M04. 10. A backtick run does not close a tilde fence — kills M06.
   11. A backtick in the info string means the line is not a fence — kills M07. 12. A closing run
   may carry trailing whitespace — kills M35. 13. `url-match` uses the source cell only; a URL in a
   later cell of a sibling's row is not a source URL — kills M09. 14. Only `.md` files under
   `corpus/knowledge/` are knowledge files — kills M11. 15. Without `--fleet` the fleet root is the
   parent of `--root` and the sibling is found — kills M22. 16. A revision with no knowledge file is
   unevaluable, never a clean `ids_cited=0` — kills M31. 17. A revision that is not a commit (a
   tree) is unevaluable — kills M17. 18. `corpus/knowledge-notes/` is not under `corpus/knowledge/`
   — kills M33. 19. A sibling that is a linked git worktree is read at HEAD, not at its dirty file
   — kills M34. 20. The summary prints `unowned = dangling - owned_elsewhere`, in a case with
   `owned_elsewhere >= 1` — kills M37. 21. The dangling-id-order case must not depend on
   set-iteration luck: build it so the set order differs from sorted order under every
   `PYTHONHASHSEED` — the current case 47 is a flaky detector (fails 38/40 seeds against M28) —
   closes M28. 22. The knowledge-dir refusal message is pinned (`corpus/knowledge absent` vs
   `**.md empty`) — closes M13 (message level only). 23. The registry-cell digit rule is pinned
   explicitly (a `S12` row is not a registry id) so M02 cannot recur silently — closes M02 (inert
   today; the rule is currently implied only by the cited-id regex).

## VERIFICATION:

- Pristine detector control: `selftest: 59/59`, exit 0, re-run before every batch.
- Base counter control: `13/21 met=False`, exit 1 at `fd6303c` — matches the contract's base
  control, so the measured revision was the contracted one.
- No tool installed or upgraded for this seat (none needed; the harness is plain `python3`).
- Lane untouched: `git status --porcelain scripts/id_resolver.py` empty; blob sha256 unchanged at
  `2c1b4970a652023a883a414620c07cf393f7c4b28b87053564a45302428e663a` after the run; `git log -1`
  still `cb68527`. No `git add/commit/stash/checkout/reset/pull/push`, no `jj` mutation. All 40
  mutants, fixtures and fixture repos lived under the seat scratch dir, now deleted.
- Receipts: `MutResolverSelftest.files/mutants.json` (per-mutant sha256, tally, failing case
  names), `crosscheck2.json` (counter cross-check), and the eight harness/probe scripts.

VERDICT: The tool's 59-case selftest survives 18 of 40 single-point mutants (four on the fence
machine, four on the knowledge walk, three each on the registry parser and the revision path
parse), and the round's C2 counter catches none of those 18 — the same 18 behaviours stay
unverified by both detectors, so the C2 fix must add the seven K-route cases (K8–K14, all RED on
the current tool) plus the sixteen blind-spot cases listed above, every one of which was verified
to pass on the pristine tool and fail on the mutant it was written for.
