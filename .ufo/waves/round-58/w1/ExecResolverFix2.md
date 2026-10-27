# ExecResolverFix2

C2 second independent implementation of the fence-aware / quoted-path fix, written from the base tool
(`scripts/id_resolver.py` @ `044048597d62f3199494b63b36e90dd57825e350`) without reading any sibling seat's
candidate. Candidate file: `.ufo/waves/round-58/w1/ExecResolverFix2.files/id_resolver.py`
(46 042 B, 1030 lines); receipts beside it: `candidate.diff`, `selftest.txt`, `gate-run.txt`,
`battery.txt`, `base-control.txt`.

## DIFF:

Committed on a shared clone at the base revision — clone `/fast/scratch/hyaku/kake-r58/ExecResolverFix2/lane`
(`rev-parse --show-toplevel` == that dir; clone is `--shared`, the lane repo and its index/jj state untouched),
candidate stored as `scripts/id_resolver.py`, commit `99e6dbe6c60ded6620ad99ee2399d6063adef55b`
(`user.name=selftest`, `user.email=selftest@local`), one file changed: `1 file changed, 141 insertions(+), 5 deletions(-)`.

Six hunks, all inside `scripts/id_resolver.py`; no other path in the candidate commit:

1. Module docstring (lines 10-23 base): states that the `--revision` file list comes from `git ls-tree -r -z`
   and that fenced code blocks are code (CommonMark 4.5/4.6 rules spelled out: 0-3 spaces, 3+ of ` or ~,
   same character, closing length >= opening length, nothing but whitespace after, unclosed runs to EOF,
   fenced `## Registry` neither opens nor ends the section, fenced `| S### |` is not a row).
2. New constant `FENCE_RE = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")` next to `SECTION_END_RE`.
3. New `_fence_open(line)` / `_fence_closed(line, fence)` helpers; `parse_registry` rewritten as the
   line-state machine: `fence` state is checked first (only a valid close clears it, every fenced line is
   `continue`d), then a fence opener, then `## Registry`, then `not inside`, then section end, then the row
   regex — the registry row/URL logic is the base code, unchanged.
4. `knowledge_bodies` revision branch: `ls-tree -r --name-only` + `splitlines()` -> `ls-tree -r -z --name-only`
   + `split("\0")`, so git's path quoting (core.quotePath) can no longer drop a non-ASCII or
   special-character `corpus/knowledge/**/*.md` name. Working-tree branch, sibling logic, `render`,
   CLI/exit codes untouched.
5. Ten new selftest cases (`case_fenced_heading_before_registry`,
   `case_fence_inside_registry_hides_a_row`, `case_tilde_fence_inside_registry_hides_a_row`,
   `case_info_string_fence_hides_a_row`, `case_short_close_does_not_end_a_longer_fence`,
   `case_indented_fence_marker_is_not_a_fence`, `case_unclosed_fence_hides_the_rest`,
   `case_revision_reads_non_ascii_path`, `case_revision_reads_double_quote_path`,
   `case_revision_reads_newline_path`) plus a `_row_line`/`_registry_doc`/`_revision_path_case` helper trio;
   all 49 base cases kept verbatim.
6. `_cases()` gains those ten entries: 49 -> 59.

## GATE RUN:

Counter `.ufo/waves/round-58/c58_resolver_cases.py` (version 1, unmodified), run as
`python3 -B <lane>/.ufo/waves/round-58/c58_resolver_cases.py --root <clone> --revision 99e6dbe --work /fast/scratch/hyaku/kake-r58/ExecResolverFix2/w`;
receipt `ExecResolverFix2.files/gate-run.txt`.

- `C2 resolver-cases 12/12 met=True  (met: cases_passed == 12 of 12)`, `EXIT=0`.
- K1 PASS `exit=1 DANGLING S950 ... ids_cited=2 ids_resolved=1 dangling=1`; K2 PASS (S951);
  K3 PASS (S952); K4 PASS `exit=1 DANGLING S900 cited-by=corpus/knowledge/中文.md`;
  K5 PASS `exit=1 DANGLING S901 cited-by=corpus/knowledge/a"b.md`.
- P1 PASS `ids_cited=1 ids_resolved=1 dangling=0`; P2 PASS `ids_cited=2 ids_resolved=2 dangling=0`;
  P3 PASS `exit=1 DANGLING S003`; P4 PASS `owners=alpha-shokunin`;
  P5 PASS `exit=2 id_resolver: unevaluable: fleet root ... is not a directory`;
  P6 PASS `exit=0 ('59', '59')`; P7 PASS `exit=0 ids_cited=106 ids_resolved=106 dangling=0`.
- Independent red control on the same clone, `--revision 0440485...` (base tool, receipt
  `base-control.txt`): `7/12 met=False EXIT=1`, K1-K5 FAIL with `exit=0 ... dangling=0`, P1-P7 PASS —
  the same before-state the contract states, so the counter discriminates on this clone.
- Tool selftest (in the clone, cwd = clone): `selftest: 59/59`, exit 0 (`selftest.txt`).

## BATTERY:

`ExecResolverTests.files/battery.py` existed at finish time and was run against the candidate:
`battery: 13/13 cases passed`, exit 0, receipt `ExecResolverFix2.files/battery.txt`
(`battery: tool=.../ExecResolverFix2.files/id_resolver.py`).

Caveat, disclosed: `battery.py` hardcodes `SCRATCH = "/fast/scratch/hyaku/kake-r58/ExecResolverTests"`,
another seat's scratch root, and the battery `rmtree`s each case dir before building it, so two seats running
it concurrently would corrupt each other. I therefore ran a copy of the file at
`/fast/scratch/hyaku/kake-r58/ExecResolverFix2/battery.py` with that one `SCRATCH` line repointed inside my own
scratch; verified with `diff` that the copy differs from the original **only** in that line. Case semantics,
expectations and the `verdict` comparison are byte-identical to the author's file.

Per-case: 00 control `exit=0 dangling=0`; 01 four-backtick-not-closed-by-three `dangling=2`; 02 tilde-not-closed-
by-backticks `dangling=2`; 03 four-space-fence-line `dangling=0 exit=0`; 04 info-string fence `dangling=1`;
05 unclosed-to-EOF `dangling=2`; 06 heading-after-fenced-heading `dangling=1`; 07 three-space-row-after-fence
`dangling=1`; 08 CRLF-around-fence `dangling=1`; 09 tab-in-name `dangling=1` (S917); 10 newline-in-name
`dangling=1` (S918); 11 backslash-in-name `dangling=1` (S919); 12 non-ASCII subdir `dangling=1` (S920).

## DESIGN NOTES:

- Fence state is document-global, not section-local: it is advanced before the `## Registry` test, so a fence
  opened above the heading (gate K1) suppresses the heading and its rows, and an unclosed fence suppresses
  everything to EOF (battery 05). This is the CommonMark reading; a registry-local machine would print a green
  line for K1.
- The closing test reuses `FENCE_RE` and accepts any run of the *same* character with `len >= opening`, then
  requires the remainder to be spaces/tabs only, so a 4-backtick opening is not closed by a 3-backtick line
  (3 < 4, battery 01) and a `~~~` fence is not closed by a ` ``` ` line (character mismatch, battery 02).
  A backtick fence whose info string
  contains a backtick is not an opener (CommonMark), and a 4-space-indented marker is indented code, matched by
  `^ {0,3}` failing rather than by a special case (battery 03).
- A fence *inside* the section does not end the section: rows after the closing fence still count (gate P2,
  battery 07) — the section boundary is still only `#`/`##` headings, as in the base.
- `-z` was chosen over `-c core.quotePath=false`: `-z` is NUL-delimited, so a path with a newline survives
  (`split("\0")` instead of `splitlines()`, battery 10) and no name is ever unquoted-and-reparsed by hand.
  `git show <rev>:<path>` is then given the raw path, which git accepts literally.
- Deliberately unchanged (contract "nothing else moves"): knowledge-body id scanning is still raw text over
  the whole file, so a fenced id in a knowledge file still counts — that divergence is the contract's stated
  choice and no case targets it; sibling ownership/url-match, `render`, exit-code table, usage handling, and
  the census-facing 0-3-space row rule are untouched.

Risks / limits: [INFERENCE] a path whose bytes are not valid UTF-8 decodes with `errors="replace"` and could
fail the `.md` suffix test, identically to the base; no such case exists in the gate or the battery. The selftest
is now 59 cases, so any later gate asserting an exact count 49 rather than `>= 49` would need updating (P6 asserts
`>= 49`). Candidate is a candidate only: it lives in the wave-1 files dir and a scratch clone; nothing in the lane
was committed or mutated.

VERDICT: Both defects closed independently — C2 gate 12/12 (EXIT=0) vs 7/12 on the base control, battery 13/13, tool selftest 59/59; candidate committed only in the scratch clone 99e6dbe, lane untouched.
