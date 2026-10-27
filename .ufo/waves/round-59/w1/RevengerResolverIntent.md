# RevengerResolverIntent

Scope: reverse-engineer the intended contract of `scripts/id_resolver.py` at lane base `fd6303c` from its round-57/58
history, both contracts, the SKILL row and the tool's own docstring/selftest, then judge the round-59 K8–K14 cases
(K10/K11/K12/K14 named in the assignment). Read-only on the lane; no claim scored; no after-state measured. Scratch
`/fast/scratch/hyaku/kake-r59/RevengerResolverIntent` (fixtures F08, F09, F10, F10b, F11, F12, F12r, F13, F14; removed at end).

## INTENT

Documented contract, `scripts/id_resolver.py` at base:

1. **Surface** — "every word-bounded `S` + 3 or more digits in each `corpus/knowledge/**/*.md` file" (`:11`); a registry
   id is "first cell of each table row … under the exact heading `## Registry`" (`:15-16`). Round-57 contract C2 states
   the same surface verbatim (`round-57/contract.md:46-48`).
2. **Two sources, one measurement** — worktree mode reads files; `--revision` takes paths from `git ls-tree -r -z` and
   blobs from `git show`, "never the working tree", registry "at the same revision, for the same reason" (`:12-14`).
   Nothing in the docstring, the r57 contract or the r58 contract disclaims semantic parity: the promise is *same
   verdict, different source*. r57's junk control makes the revision the authoritative object ("a tool that reads the
   working tree instead of the revision fails G4", `round-57/contract.md:56-58`).
3. **Both modes are gated** — r57 gate calls `tool_vs_reference` with `rev=None` for G3 (`c57_idresolver_gate.py:340,343`)
   and with a revision for G4/G5 (`:359,363`), so parity is part of what C2's gate buys, not an extra.
4. **Symlinks** — one stated rule, worktree-only: "a symlink must not carry a citation in from outside the lane"
   (`:196`), pinned by selftest `case_symlink_out_of_the_lane_is_not_a_citation` (`:819-825`). It is the round-57
   post-freeze fix for `w2/SentinelRound F3` (`round-57/w2/SentinelRound.md:49-60`, landed at `32754df`), whose text says
   revision mode is "immune". **In-lane symlinks were never excluded**: the same branch accepts an in-lane symlinked
   knowledge *root* (`:200`) and follows in-lane file symlinks (`:213`) — both observed (F10b: `corpus/knowledge ->
   ../store` gives `DANGLING S920 cited-by=corpus/knowledge/hidden.md`, exit 1). Directory descent is missing only
   because `os.walk` defaults to `followlinks=False` (`:203`) — an implementation artifact, not a documented choice.
   r58 reviewer c07b certified the in-lane file-symlink following as *correct* (`round-58/w1/ReviewerResolverOther.md:61-63`).
5. **Markdown semantics** — round 58 introduced rendering semantics for fences only: "a heading or a table row inside
   such a block counts for nothing here" (`:17-20`), with the census divergence stated. HTML comments and setext headings
   appear nowhere; `SECTION_END_RE` is ATX-only (`:48`), matching the parenthetical "(the section ends at the next `# ` or
   `## ` heading)" (`:16`).
6. **Exit classes** (`:25-26`): 2 = revision unresolved, `--fleet` not a directory, registry absent, no knowledge file; 64
   usage. No class exists for a root that is not a toplevel, nor for a symlinked registry.
7. **`--root <lane dir>`** (`:9`) — the lane is named by the root; the CLI path never asserts `rev-parse --show-toplevel ==
   root` (only the selftest does so for its own fixtures, `:348-350`).
8. **Scope discipline** — round 58's claim title bound that round to "closes its two disclosed false-green defects, nothing
   else moves" (`round-58/contract.md:45`); round 59 drops that phrase. Round-58's v1 frozen contract (`fff3eea`) names no
   HTML-comment / setext / symlink limit — that list was added only in the v2 amendment (`1c0aa21`) — so round-59's
   "disclosed after the round-58 freeze" is accurate.

## CASE ALIGNMENT

- **K10 — in-lane symlinked knowledge dir: FOLLOWS the intent (restoration).** It restores `:11`'s `**` glob and applies
  `:196`'s containment rule at its stated scope (outside only). Observed base: `ids_cited=1 ids_resolved=1 dangling=0`,
  exit 0 (F10) — false green. The fix must keep `:819`'s out-of-lane refusal (K10's mirror is not in the case list, and the
  selftest case is the only pin for it). **Unpinned gap:** at `--revision` the same committed tree is still green for the
  wrong reason — `ls-tree` lists `corpus/knowledge/linked` (no `.md`, `:183`) so the citation is never read; observed
  revision `ids_cited=1 dangling=0`. A worktree-only K10 fix leaves the gated mode blind: exactly the r58 F2 class.
- **K11 — revision-mode committed symlink: FOLLOWS on resolution, EXTENDS on dangling links.** In-tree resolution follows
  from c07b (in-lane following is correct) plus parity (2, 3). The dangling-link half is new: revision mode must ignore
  `odd.md` and still report `ids_cited=2`. Observed base on K11's tree — revision: `DANGLING S903
  cited-by=corpus/knowledge/odd.md` (the link's *target string* parsed as a body: forged citation) and S902 hidden, exit 1;
  worktree: exit 2 `cannot read corpus/knowledge/odd.md` (`:216`). So K11 requires revision mode to be *more tolerant* than
  worktree mode, and no r59 case pins worktree behavior on that tree: a candidate can pass 21/21 while worktree still exits
  2 where revision exits 1 — an undisclosed mode divergence.
- **K12 — registry symlinked out of lane: CHANGES the intent (new refusal class), direction defensible.** Reading "the
  lane's own `corpus/SOURCES.md`" (`:5,:22`) as an ownership rule is new — `:196`'s containment covers knowledge only —
  and the case adds an exit-2 class absent from `:25-26` and from the SKILL row (`SKILL.md:1276`). Observed: worktree exit 0
  (F12; the outside row resolves the citation, i.e. the frozen D1 false-green class), and revision on the same committed
  tree exit 1 with every id dangling (`git show` returns the target path string, so the registry parses empty). K12 pins one
  mode and leaves the other loud-but-different; parity would also require mode-120000 handling of the registry (unevaluable),
  which nothing tests.
- **K14 — non-toplevel `--root`: CHANGES the intent (new precondition), closes a real false green.** `:9` only says
  `<lane dir>`; the tool never promised to reject a subdirectory, and F6 itself says "Not a false green by itself"
  (`round-58/w1/SentinelCounters.md:95`). On its own fixture it *is* one: observed revision over `anc/lane` → green
  `ids_cited=2 dangling=0` (ancestor's registry), while worktree over the same root → exit 1 `DANGLING S914` (the lane's own
  registry). So K14 aligns revision mode with the worktree verdict (`:168` "registry absent") and with the r57-r58 sandbox
  discipline (`:348-350`); it must be written into `:9` and `:25-26`, not only implemented.
- **K8/K9 — comment row, setext H2: EXTENSIONS of an established principle.** The r58 fence rule already says non-rendered
  headings/rows register nothing (`:17-20`), and the docstring's nouns are "table row" and "heading" — so the expectations
  follow the words; but `:16`'s parenthetical and `:48` describe ATX syntax, so both need a docstring extension. Observed
  base: both exit 0 `dangling=0` (F08, F09) — false greens, and a different mechanism from K1–K3 (no fence involved).
- **K13 — non-UTF-8 name at a revision: FOLLOWS** `:12-13` ("a git-quoted or non-ASCII name is read as itself") — same
  identity class — and `:25-26` offers no exit-2 class for an exotic name. Observed base: revision exit 2
  `cannot read corpus/knowledge/bad<FF>.md at <rev>` (F13); one name denies the whole run. **Unpinned sibling route:** on the
  same tree worktree mode crashes printing the surrogate path (`UnicodeEncodeError` traceback, exit 1) — same class, no case
  covers it, so a fix confined to the revision branch leaves it. Note the name-identity promise is one round old (the r57
  docstring had no `ls-tree -z` clause), so K13 restores a round-58 promise, not a round-57 one.

[INFERENCE] The K14 "extension vs restoration" call is a judgment over `:9`; the K8/K9 reading ("the docstring's nouns are
rendering-level") is my reading of `:15-16`, not a statement in any contract; K11's dangling-link tolerance direction is
inferred from the asserted counts (`ids_cited=2`), not from prose. Directly observed, not inferred: F08, F09, F10, F10b,
F11 (both modes), F12 (worktree), F12r (revision), F13 (both modes), F14 (both modes).

## Verdict

VERDICT: K10 and K13 follow the original intent (the `**` glob under the stated in-lane-only containment rule; names "read as itself"), K11 follows it on in-tree resolution but extends it with dangling-link tolerance the worktree path contradicts today, while K12 (out-of-lane registry refusal) and K14 (toplevel precondition) are new hardening the tool never promised and must be stated as intent changes in the docstring and the SKILL exit-2 list; all seven are directionally right — every observed base behavior is a false green or a whole-run denial — but K10's revision counterpart, K11's worktree counterpart, K12's revision verdict and K13's worktree print crash are unpinned, so 21/21 will not prove worktree/`--revision` parity.
