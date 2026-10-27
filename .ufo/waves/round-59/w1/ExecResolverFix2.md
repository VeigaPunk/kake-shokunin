# ExecResolverFix2

Claim C2, **second independent implementation** (no coordination with the primary seat, no inspection of its
candidate). Candidate: `.ufo/waves/round-59/w1/ExecResolverFix2.files/id_resolver.py` (1459 lines), written from
`scripts/id_resolver.py` as committed at contract commit `45a92b6` (base `fd6303ce`; the blob is identical at both).
Scored in a `git clone --shared` of the lane at `45a92b6` under `/fast/scratch/hyaku/kake-r59/ExecResolverFix2/`,
candidate committed there with the selftest identity as `c117475` then `2d8b8aa`. Scratch removed; receipts copied to
`ExecResolverFix2.files/`. Base blob `c1c47a4` verified byte-identical at `fd6303ce` and `45a92b6`
(`rev-parse fd6303ce:… 45a92b6:…` -> same object). Provenance: the only lane paths this seat wrote are this report and
`ExecResolverFix2.files/`; the lane worktree `M scripts/id_resolver.py` seen after the run is another seat's candidate
(436+/49-, applied after my base copy was taken at 1026 lines), not mine.

## DIFF:

`45a92b6:scripts/id_resolver.py` (1026 lines) -> candidate (1459): **+480 / -47**, 12 hunks.
Full unified diff: `ExecResolverFix2.files/id_resolver.diff`; production hunks only (no selftest cases):
`id_resolver.prod.diff`; `-U0` form: `id_resolver.u0.diff`.

| base hunk | candidate | change | route |
| --- | --- | --- | --- |
| `-1,29 +1,40` | docstring | html-comment/setext/symlink semantics, `cat-file` reads, `\xNN` rendering, exit-2 list | all |
| `-34,6 +45,7` | `import posixpath` | in-tree link normalisation | K11 |
| `-48,6 +60,11` | regexes | `HTML_COMMENT_OPEN/CLOSE`, `SETEXT_H1/H2`, `ATX_HEADING` | K8, K9 |
| `-83,9 +100,90` | `_nul_paths` out | `_tree_entries` (`ls-tree -r -z` **with modes**), `_blob_bytes` (`cat-file blob <oid>`), `_resolve_link_path`, `_link_dir_bodies` | K11, K13 |
| `-104,31 +202,71` | `parse_registry` | opaque HTML-block state; setext H1/H2 section end gated on the preceding paragraph line; `_is_paragraph_line` | K8, K9 |
| `-157,15 +295,33` | `lane_registry` | worktree registry realpath-contained (else exit 2); revision registry from the tree, symlink resolved in-tree | K12 |
| `-173,20 +329,81` | knowledge read | `_walk_knowledge` follows in-lane symlinked dirs with cycle protection; revision read resolves blobs, dirs and chains | K10, K11 |
| `-200,20 +417,10` | knowledge read | old `os.walk` body (no symlinked dirs, `git show rev:path`) removed | K10, K11 |
| `-250,17 +457,37` | `evaluate` | `_repo_toplevel`; revision mode requires `--root` == its repository toplevel (else exit 2); tree map threaded once | K14 |
| `-288,11 +515,23` | `render` | `_visible()` renders non-UTF-8 name bytes as `\xNN` | K13 |
| `-913,6 +1152,185` | selftest | 15 new cases | all |
| `-974,6 +1392,21` | `_cases()` | registration (59 -> 74) | all |

Core of the registry fix (K8/K9), verbatim from the candidate:

```
+        if html:  # an HTML comment block hides everything up to its `-->`
+            if HTML_COMMENT_CLOSE_RE.search(line):
+                html = False
+            prev_para = False
+            continue
...
+        if HTML_COMMENT_OPEN_RE.match(line):
+            html = not HTML_COMMENT_CLOSE_RE.search(line)
+            prev_para = False
+            continue
...
+        if inside and prev_para and (SETEXT_H1_RE.match(line) or SETEXT_H2_RE.match(line)):
+            inside = False  # a setext H1/H2 ends the section, like an ATX `# `/`## ` heading
```

## GATE RUNS:

Counter (frozen v1, `--root <clone> --revision HEAD --work <scratch>/w`), 6 seeds, all `EXIT=0`:

| seed | result |
| --- | --- |
| 5901 | `C2 resolver-cases 21/21 met=True`, `EXIT=0` (console only, not kept) |
| 5902, 5903 | `21/21 met=True`, `EXIT=0` (console only, not kept) |
| 5911, 5912, 5913 | `21/21 met=True`, `EXIT=0` — receipts `gate-seed5911.txt`, `-5912`, `-5913` (all `P6 ('74','74')`) |

Per-case output of `gate-seed5911.txt` (all 21 PASS, fixture ids drawn per seed): K1 S9404, K2 S6408, K3 S6208,
K4 S6473 (`cited-by=corpus/knowledge/中文.md`), K5 S1756 (`a"b.md`), K6 S6842, K7 S5318, K8 S7637, K9 S8547,
K10 S7277 (`cited-by=corpus/knowledge/linked/hidden.md`), K11 S7665 (`cited-by=corpus/knowledge/linked.md`, no forged
citation), K12 `exit=2 registry outside the lane`, K13 S9154 (`cited-by=corpus/knowledge/bad\xff.md`), K14 `exit=2
... is not the toplevel of its repository`, P1-P7 PASS (P7 `ids_cited=108 ids_resolved=108 dangling=0`).

Base control, same counter, `--revision 45a92b6`: `13/21 met=False EXIT=1`, failing exactly K8, K9, K10, K11, K12, K13,
K14, P6 (`59/59`) — reproduces the contract's before-state (`gate-base-45a92b6.txt`).

Own edge probes (transcript `probes.txt`, fixtures in a scratch dir removed afterwards; all as designed):
p1 in-lane symlinked registry is read (rc 0); p2 dangling registry symlink (rc 2); p3 unclosed `<!--` hides the rest
(rc 1, DANGLING); p4 same-line `<!-- note -->` then a row (row registers, rc 0); p5 3-space-indented setext underline
ends the section (rc 1, DANGLING); p6 `<!--` inside a fence is code, row after the fence registers (rc 0);
p7 worktree root that is a repository subdirectory evaluates its own files (rc 0, the documented scoping); p8 `--root`
given as a symlink to the toplevel works in revision mode (rc 0); p9 `--root` below its toplevel with `--revision`
(rc 2); p10 revision-mode registry symlink inside the tree (rc 0).

## SELFTEST:

`python3 -B <candidate> --selftest` -> **`selftest: 74/74`**, rc 0 (`selftest.txt`). Base: 59/59; all 59 kept, 15 added
(one per route plus the boundaries the probe established):

K8 row inside `<!-- -->`; K8b `## Registry` inside a comment opens nothing; K8c inline `<!-- -->` in a row keeps the row;
K9 setext H2 ends the section; K9b setext H1 ends it; K9c `---` after a blank line (thematic break) does not;
K9d `---` immediately after a table row (row is not a paragraph) does not; K10 in-lane symlinked knowledge dir is read;
K10b out-of-lane symlinked dir refused; K10c symlink cycle (`self -> .`, `up -> lane root`) terminates;
K11 committed file symlink resolved in-tree, dangling link target string never a body (`S999` not cited);
K11b committed symlinked knowledge **directory** read at a revision (parity with K10);
K12 registry symlinked out of the lane is unevaluable; K13 non-UTF-8 name at a revision read and rendered `bad\xff.md`;
K14 root below its repository toplevel is unevaluable.

## REAL LANE:

- Clone at my commits, `--revision <commit>`, empty fleet: `ids_cited=108 ids_resolved=108 dangling=0` (`c117475`,
  `2d8b8aa`), identical to the base tool at `45a92b6` (`108/108/0`) — `reallane.txt`.
- Real lane working tree (read-only): base tool and candidate both `ids_cited=110 ids_resolved=110 dangling=0`
  (the lane moved past the contract commit: 110 cited ids today, 108 at the measured revision; **no delta**).
- G2: `grep -n 'c57_idresolver_gate\|\.ufo/\|reference('` over the candidate -> no match.

## DESIGN NOTES:

1. **K8 — HTML blocks are opaque, never marker-stripped.** `^ {0,3}<!--` opens a block that ends on the line
   containing `-->`; every line inside (headings, rows, fences) counts for nothing, and the `-->` line itself is
   consumed. Inline `<!--` inside a table cell cannot open a block because the block rule is anchored at line start
   (probe p4). Fence state wins over HTML state when a fence is already open (p6).
2. **K9 — setext end is gated on the preceding paragraph line.** `---`/`===` (0-3 indent) end the section **iff** the
   immediately preceding line is a paragraph line (`_is_paragraph_line`: non-blank, not a row, not ATX, not a setext
   underline). So: `Subsection`+`---` ends it (K9); `---` after a blank line is a thematic break (K9c); `---`
   immediately after a table row is a thematic break too, since a table row is not a paragraph (K9d) — the boundary
   `w1/ProbeCommonMark.md` rendered in four engines. Nothing is keyed on "any dashes".
3. **K10 — in-lane symlinked knowledge directories.** The `os.walk` walker is replaced by a recursive walker that
   follows a symlinked directory only when its realpath is inside the lane **and** it is neither the knowledge tree
   itself nor one of its ancestors (that guard is what stops a `linked -> ..` jump from pulling `corpus/SOURCES.md`
   in as a citation); a `visited` set of directory realpaths is the cycle protection. Out-of-lane dirs and files stay
   refused (existing `case_symlink_out_of_the_lane_is_not_a_citation` still passes).
4. **K11 — revision mode never reads a link target string as a body.** `git ls-tree -r -z` is read **with** modes and
   oids, and bodies are read with `git cat-file blob <oid>` (no path in argv at all). A `120000` entry is resolved
   against the same tree map: target normalised from the link's directory, refused when absolute or escaping the tree,
   chains followed with a depth bound and a `seen` set; a blob target is read, a directory target has its `*.md`
   subtree read under the link path (K10 parity — the critic's "strongest untested gap"), anything else is skipped,
   so a dangling link (`odd.md -> S999-target.md`) contributes no citation.
5. **K12 — the worktree registry is realpath-contained.** `corpus/SOURCES.md` whose realpath leaves the lane is
   `exit 2` ("registry outside the lane"); an in-lane symlinked registry is still read (probe p1). In revision mode a
   committed symlinked registry is resolved inside the tree instead of being parsed as its target string.
6. **K13 — non-UTF-8 names.** Revision paths are `os.fsdecode`d (`surrogateescape`) and `_visible()` renders any
   surrogate byte back as `\xNN`, so a name like `bad\xff.md` neither aborts the run nor raises `UnicodeEncodeError`
   on a strict-UTF-8 stdout; valid UTF-8 (`中文.md`) and quote-char names are untouched (K4/K5 unchanged).
7. **K14 — root must be its repository's toplevel, scoped to the mode that measures a repository.** The check runs
   whenever a revision is resolved (root must be a git repo toplevel; a bare/non-repo/sub-tree root is `exit 2`).
   Worktree mode only reads files under `--root`, so an enclosing repository is never measured there; making it
   `exit 2` as well would break the counter's own non-repository fixture lanes (K1-K3, K6, K8-K9, P1-P5), which the
   contract requires to stay green. `p7` records the resulting behaviour explicitly.
8. Determinism kept: ids, citing paths, owners and url-match sorted; the tree map is iterated in sorted byte order;
   no `GIT_*` inheritance (`_spawn` unchanged).

VERDICT: Candidate closes K8-K14 by construction and measurement — 21/21 on six seeds (base 13/21), own selftest 74/74, real lane unchanged at 108/108/0 (`dangling=0`); scoping caveat: the toplevel rule is enforced where a repository is measured (revision mode), which is the only mode where an ancestor repository could be measured.
