# ReviewerResolverOther

C2 breadth: registry/knowledge parse gaps beyond D1 (fences) and F1 (quoted paths) that let
`scripts/id_resolver.py` print exit 0 / dangling=0 over a lane whose markdown cites an unregistered id.

Method: snapshot of the lane tool at HEAD `cc8da1674d6e590ae2d05e1f48944ac7939e9ecd`, blob
`878da27c49a3ae7617e8b207fa45e2abee588ff2` (file clean at HEAD when snapshotted; blob unchanged at
last re-check after all runs). 13 worktree fixtures + 2 committed `--revision HEAD` fixtures; each is
a minimal lane (`corpus/SOURCES.md` with a `## Registry` section holding S001; `corpus/knowledge/a.md`
cites S001 + S900, S900 unregistered unless a vector hides its registration). Run:
`python3 -B <snapshot> --root <lane> --fleet <case>`. Expected-correct outcome for every case:
exit 1 flagging S900. Harness and raw run transcript copied to `w1/ReviewerResolverOther.files/`;
scratch dir deleted after the copy.

CASES:

- c01 multiline HTML comment hides the row — FALSE GREEN
  input: inside `## Registry`, after the S001 row: `<!--` newline `| S900 | https://e.example/9 |`
  newline `-->`. result: exit 0, `ids_cited=2 ids_resolved=2 dangling=0`.
  class: false green. Markdown renders nothing (commented out); `parse_registry` only knows the ATX
  heading and `^ {0,3}\|...` rows, so the raw row line resolves S900. Same observable defect class the
  round froze for K2/K3 (invisible-in-markdown registry rows resolving an id).

- r01 c01 replayed at `--revision HEAD` (fixture committed with selftest identity, toplevel asserted)
  result: exit 0, dangling=0, identical. The false green is not a worktree artifact; `git show`
  returns the same bytes.

- c02 single-line comment `<!-- | S900 | https://e.example/9 | -->` inside the section — correct
  result: exit 1, DANGLING S900. class: correct (no false green): the line does not start with `|`,
  so it is never a row.

- c03 row inside a blockquote `> | S900 | https://e.example/9 |` — correct
  result: exit 1, DANGLING S900. class: correct (no false green). Loud-direction note: markdown
  renders a blockquoted table row, so a lane registering an id only inside a quote would get a false
  DANGLING (exit 1), not a green.

- c04 citation inside a blockquote in knowledge (`> Cites S900.`) — correct
  result: exit 1, DANGLING S900. class: correct; ID_RE scans raw text, quotes still count as citations.

- c05 setext heading `Registry` + `---` AS the registry heading — correct
  input: no `## Registry` ATX anywhere; rows for S001 and S900 under the setext heading.
  result: exit 1, `ids_resolved=0 dangling=2` (S001, S900). class: correct (no false green): the
  heading regex needs `## `, so the whole registry is invisible and every id is flagged — fails loud.

- c06 setext heading INSIDE the Registry section — FALSE GREEN
  input: after the S001 row: `Subsection` newline `---` newline `| S900 | https://e.example/9 |`.
  result: exit 0, `dangling=0`. class: false green. In markdown `Subsection\n---` is an H2 and ends
  the `## Registry` section, so the S900 row is outside the registry; `SECTION_END_RE` (`^#{1,2}\s`)
  only stops at ATX H1/H2, so the row still resolves S900. No fence is involved, so this is a
  different mechanism from K1–K3; that the D1 fix as scoped (fence tracking) does not close it is
  [INFERENCE] from the frozen case list.

- c07a citation reachable only through a symlinked directory — FALSE GREEN
  input: `lane/notes_store/hidden.md` cites S900; `corpus/knowledge/linked` -> `../../notes_store`
  (target inside the lane). result: exit 0, `ids_cited=1 dangling=0`.
  class: false green. `os.walk` defaults to `followlinks=False`, so `linked` is never descended, even
  though the tool's own `inside()` guard would accept the in-lane realpath — the citation is silently
  dropped, not quarantined. The out-of-lane symlink variant is the stated w2/SentinelRound F3 choice
  (selftest `case_symlink_out_of_the_lane_is_not_a_citation`); the in-lane target is the defect here.

- c07b citation through a symlinked FILE (in-lane target) — correct
  result: exit 1, DANGLING S900. class: correct; the walk visits the symlink file and `open()` follows
  it. The gap is directory-following only.

- c08 `.markdown` / `.MD` extensions — false green (surface ambiguity)
  input: `b.markdown` cites S900, `c.MD` cites S901. result: exit 0, `ids_cited=1 dangling=0`.
  class: false green by the seat's literal criterion (markdown cites an unregistered id, tool prints
  green); contract-ambiguous in that the frozen surface names `corpus/knowledge/**/*.md`, and the
  census is equally `.md`-blind, so the lane gate would miss it too.

- c09 UTF-8 BOM before the `# Sources` title — correct
  result: exit 1, DANGLING S900. class: correct; the BOM only corrupts line 1, `## Registry` still
  matches. No false green in the real lane shape.

- c09b UTF-8 BOM directly before `## Registry` (file starts with the section) — correct
  input: BOM + `## Registry` + rows S001 and S900. result: exit 1, `ids_resolved=0 dangling=2`.
  class: correct (fails loud): heading unrecognized, everything dangling. No BOM route to a false green.

- c10 citation id split by a zero-width space — contract-ambiguous (leans false green)
  input: `a.md` = `Cites S<U+200B>900.` result: exit 0, `dangling=0`.
  class: the rendered text reads "S900", but `ID_RE` requires contiguous `S\d{3,}`; no contract
  sentence makes ZWSP-split ids citations [INFERENCE: the id grammar is contiguous-token only].
  Tool prints green over a human-visible citation; grammar says it is not an id.

- c11 citation in markdown outside corpus/knowledge (`docs/notes.md` cites S900) — contract-ambiguous
  result: exit 0, `dangling=0`. class: ambiguous: the frozen surface is the lane's own
  knowledge/registry; a citation in a non-knowledge markdown file is out of that surface by
  construction.

TOP RISKS:

1. c01 + c06 (registry parse): two routes where an unregistered id resolves — a raw row line inside a
   multiline HTML comment, and rows after a setext sub-heading. Same observable as the frozen D1 class
   (markdown-invisible registry text resolving an id) but outside K1–K3's fence mechanism; the frozen
   counter can stay 12/12 while the tool still greens over them.
2. c07a (knowledge walk): a symlinked directory inside the lane silently drops citations; the summary
   line then shrinks (`ids_cited`) instead of flagging, so nothing in the output looks wrong.
   Distinct from the stated out-of-lane F3 quarantine.
3. Coverage asymmetry: all three false greens manifest as absent DANGLING/ids_resolved counts, so a
   "real lane green" check (P7-style) cannot distinguish them; only adversarial fixtures like these do.
4. Loud-direction gaps (not false greens, robustness only): blockquote-registered rows (c03) and a
   setext-headed or BOM'd registry (c05, c09b) make real registrations invisible -> exit 1 with
   `ids_resolved=0`; safe direction for the gate, but they fail closed on ordinary markdown lanes.
5. c08/c10/c11 are graded contract-ambiguous deliberately: they print green over citations a human
   reader sees, but the frozen surface (`.md`, contiguous `S\d{3,}`, corpus/knowledge) does not clearly
   claim them; widening the surface is a next-round decision, reported as a limit, not pursued.

All 15 runs exercised; nothing inferred except the two [INFERENCE] tags above. No lane or fleet file
mutated beyond this report and its `.files/` receipts; fixtures lived under
`/fast/scratch/hyaku/kake-r58/ReviewerResolverOther` and were removed after receipts were copied.
The two committed revision fixtures asserted `git rev-parse --show-toplevel` equals the fixture dir
before committing with the selftest identity, inside scratch only.

VERDICT: 3 new false-green routes confirmed beyond D1/F1 (HTML-comment registry row c01/r01, setext section-end c06, in-lane symlinked-dir citation drop c07a); c02–c05, c07b, c09, c09b hold loud; c08, c10, c11 contract-ambiguous — reported limits for round 58, not new targets.
