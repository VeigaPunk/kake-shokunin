# ExecResolverFix

C2 primary implementation. Candidate: `.ufo/waves/round-59/w1/ExecResolverFix.files/id_resolver.py`, built from the lane tool at
base `fd6303ce5c14b3f892dec586297a942ab6e4193b` (contract commit `45a92b64`). Lane working tree, lane index, jj state and
siblings untouched; every run happened in a shared clone under `/fast/scratch/hyaku/kake-r59/ExecResolverFix/` (deleted).
No installs were needed (python3 3.14.8, git 2.56.0 already present); no pacman.

## DIFF:

Scored candidate commit in the clone: `290ac2e97015384e389b030bc9ffb81e3261f99b` (parent `45a92b64`, selftest identity).
`scripts/id_resolver.py | 410 +++++--- 1 file changed, 364 insertions(+), 46 deletions(-)`. Full unified diff:
`.files/id_resolver.diff`. Hunk map (old → new), each hunk named by the route it closes:

```
@@ -1,5   +1,7    docstring title: round-59 behaviours added
@@ -11,19 +13,27  docstring CLI contract: symlink/comment/setext/toplevel/escape rules
@@ -34,6  +44,7   +import posixpath
@@ -46,6  +57,10  +ATX_HEADING_RE +SETEXT_RE +THEMATIC_BREAK_RE +HTML_COMMENT_RE   (K8,K9)
@@ -83,9  +98,63  _nul_paths -> _ls_tree_entries(mode,type,id) + _blob_bytes + _resolve_tree_link  (K11,K13)
@@ -104,31 +173,67 _is_paragraph_line + parse_registry: HTML-comment state, setext section end (K8,K9)
@@ -157,15 +262,42 +repo_toplevel; lane_registry: tree modes, in-tree link, realpath containment (K12,K14)
@@ -173,47 +305,83 +_inside_lane + _walk_knowledge (in-lane symlinked dirs, cycle chain) + knowledge_bodies (K10,K11,K13)
@@ -253,14 +421,18 evaluate: one `ls-tree -r -z` listing passed to registry and knowledge reads
@@ -288,11 +460,16 +_show_path (visible `\xNN` escape) + render                                  (K13)
@@ -913,6  +1090,131 10 new selftest cases
@@ -974,6  +1276,16 case registration (59 kept + 10 new)
@@ -1013,6 +1325,12 main: revision-mode toplevel gate                                          (K14)
```

Load-bearing added lines (verbatim, elided where obvious):

```diff
+        if comment:  # an HTML block comment hides everything up to the line that holds -->
+            if "-->" in line:
+                comment = False
+        if HTML_COMMENT_RE.match(line):
+            comment = "-->" not in line
+        if prev_paragraph and SETEXT_RE.match(line):
+            inside = False  # a setext H1/H2 is a heading too: it ends the section like an ATX one
-        proc = _git(root, "ls-tree", "-r", "-z", "--name-only", revision)
+    proc = _git(root, "ls-tree", "-r", "-z", revision)
+        meta, _, path = chunk.partition(b"\t")
+        entries[path] = (fields[0], fields[1], fields[2])
+            if mode == b"120000":  # resolve the link inside the tree: its target string is not a body
+                object_id = _resolve_tree_link(root, entries, path)
+                if object_id is None:
+                    continue
+    real = os.path.realpath(path)
+    if real != root_real and not real.startswith(root_real + os.sep):
+        return None, f"registry outside the lane: {REGISTRY_REL} -> {real}"
+            rel = os.fsdecode(path)
+    return path.encode("utf-8", "surrogateescape").decode("utf-8", "backslashreplace")
+        toplevel = repo_toplevel(args.root)
+        if toplevel != os.path.realpath(args.root):
+            print(... "is not the toplevel of its repository" ..., file=sys.stderr)
+            return 2
```

## GATE RUNS:

Counter: `python3 -B .ufo/waves/round-59/c59_resolver_cases.py --root <clone> --revision HEAD --work <scratch>/w<N> --seed <N>`
against the candidate commit `290ac2e9`, receipts in `.files/c59_resolver_cases_seed*.txt`:

- seed 59: `C2 resolver-cases 21/21 met=True`, `EXIT=0` — K8…K14 all PASS, P6 `('69','69')`, P7 `ids_cited=108 … dangling=0`.
- seed 1: `21/21 met=True`, `EXIT=0`.
- seed 20261027: `21/21 met=True`, `EXIT=0`.

Do-nothing control (same counter, `--revision 45a92b64` = base tool, seed 59): `13/21 met=False`, `EXIT=1`
(`.files/c59_resolver_cases_base_seed59.txt`); the eight failures are exactly K8 K9 K10 K11 K12 K13 K14 and P6 (`59/59 < 66`),
i.e. the disclosed routes plus the tally floor, matching the frozen "before" line.

Observed per-route evidence in the candidate runs (seed 59): K8 `DANGLING S2676`, K9 `DANGLING S9644`,
K10 `DANGLING S5652 cited-by=corpus/knowledge/linked/hidden.md`, K11 `DANGLING S2990 cited-by=corpus/knowledge/linked.md`
(no `F11` id from the dangling link), K12 `exit=2 registry outside the lane: corpus/SOURCES.md -> …/outside/SOURCES.md`,
K13 `DANGLING S1757 cited-by=corpus/knowledge/bad\xff.md`, K14 `exit=2 root … is not the toplevel of its repository
(toplevel …/anc)`. Base on the same fixtures: K8/K9/K12/K14 exit 0 green, K10 `ids_cited=1`, K11 flags the link's target
string as an id, K13 `exit=2 cannot read corpus/knowledge/bad<U+FFFD>.md`.

## SELFTEST:

`python3 -B id_resolver.py --selftest` (TMPDIR in scratch): **69/69, rc 0** (`.files/id_resolver_selftest.txt`);
all 59 round-57/58 cases kept unchanged, 10 added (one per disclosed route plus a single-line-comment variant, a setext H1
variant and a symlink-cycle case): HTML comment hides a row; single-line comment is not a row; setext H2/H1 underline ends the
Registry section; in-lane symlinked knowledge dir is read; symlinked-dir cycle is finite; committed symlink resolved in the
tree; registry symlinked out of the lane is unevaluable; non-UTF-8 path read at a revision (with the visible escape asserted);
root below its repository toplevel is unevaluable.

## REAL LANE:

Shared clone of the lane at `45a92b64`, candidate committed at `290ac2e9` (`.files/real_lane_runs.txt`):

- `--root <clone> --revision 290ac2e9 --fleet <empty dir>` → `ids_cited=108 ids_resolved=108 dangling=0 owned_elsewhere=0 unowned=0`.
- baseline for the same command with the base tool at `--revision 45a92b64` → identical `ids_cited=108 … dangling=0`.
- worktree mode (no `--revision`) on the clone → identical `108/0`.

So C2's P7 surface is unchanged: `ids_cited` 108 = base, `dangling` 0. Grep of the candidate: no `c57_idresolver_gate`,
no `.ufo/`, no `reference(` (all 0); `py_compile` clean.

## DESIGN NOTES:

- **K8** `parse_registry` tracks CommonMark HTML block type 2: a line matching `^ {0,3}<!--` opens a block that ends on the
  line containing `-->` (same-line `<!-- … -->` is a one-line block). Everything inside counts for nothing — rows, headings,
  fences. Fenced code still wins (a `<!--` inside a fence is literal); probes: comment inside a fence leaves the row after it
  registering; an *unclosed* comment before `## Registry` hides the registry and the run fails loud (both ids dangling).
- **K9** section end now also accepts a setext underline: a line of only `=` (H1) or `-` (H2) that follows a *paragraph line*
  ends the Registry section, exactly like `# `/`## `. `_is_paragraph_line` excludes blank lines, ATX headings, table rows,
  setext underlines themselves, thematic breaks and comment openers. A bare `---` after a blank line stays a thematic break
  and does **not** end the section; table rows are deliberately not paragraph lines (a `---` after a row keeps the section
  open) — the counter only requires the `Text` + `---`/`===` case, and this choice never hides a row.
- **K10** worktree knowledge walk replaced `os.walk` with an explicit stack: a symlinked directory is descended iff its
  `realpath` stays inside the lane, and the tuple of realpaths on the current path travels with each entry, so a symlink cycle
  (`knowledge/self -> .`, or a link back to an ancestor) terminates. Out-of-lane symlinked dirs are skipped (probe: target
  outside the lane, no citation, rc 0); out-of-lane symlinked *files* stay skipped as in round 58; in-lane symlinked files are
  still read (probe: `cited-by=corpus/knowledge/ext.md`). Files that resolve to the lane registry itself are excluded so a
  link to a parent cannot turn the registry into a citation body.
- **K11/K13** `--revision` now reads one `git ls-tree -r -z <rev>` and keeps `(mode, type, object id)`; bodies come from
  `git cat-file blob <id>`, so no path ever becomes a git argv element (newline, quote and non-UTF-8 names all round-trip).
  A `120000` entry under `corpus/knowledge/` is resolved *inside the tree*: the link blob's target is joined to the link's
  directory, `normpath`'d, refused when it escapes the tree (`..`) or is absolute, then looked up in the same listing and
  followed at most 8 hops with a visited set. The target's **content** is the body, attributed to the link's own path; a link
  that points nowhere or leaves the tree contributes nothing (never its target string). A symlinked registry at a revision is
  resolved the same way; unresolvable → exit 2. Path bytes are decoded with `os.fsdecode` (surrogateescape) and rendered with
  a visible escape (`bad\xff.md`), so a non-UTF-8 name no longer makes the run unevaluable and cannot crash stdout.
- **K12** worktree registry: `os.path.realpath(root/corpus/SOURCES.md)` must be inside `realpath(root)` — a registry symlinked
  out of the lane exits 2 (`registry outside the lane`), a registry symlinked to a file *inside* the lane is accepted (probe),
  and the revision path applies the in-tree rule above. Gitlink/other non-blob entries are refused as unreadable.
- **K14** `main()` runs `git -C root rev-parse --show-toplevel` and exits 2 when it differs from `realpath(root)`, so a root
  that would resolve a revision through an ancestor repository is never measured. **Scoping decision:** the gate fires when a
  revision is requested, i.e. exactly where git resolves in the root's repository; in worktree mode the tool reads the named
  directory's own files and never consults an ancestor repository, and an unconditional gate would contradict the kept
  round-58 case `case_fleet_root_repo_does_not_own` (a lane inside a fleet-root repository must still evaluate).
- Sibling registries are parsed with the same registry grammar (stricter: rows after an HTML comment/setext heading in a
  sibling registry stop counting) — loud direction only (owners lost, never invented).
- Residual limits: `.markdown`/`.MD`, zero-width-split ids and markdown outside `corpus/knowledge` stay out of surface as the
  contract states; `splitlines()` still splits on more than `\n` (round-58 F3, unchanged); the printed selftest tally is still
  the only P6 signal; the K9 paragraph rule is a deliberate subset of CommonMark (see above).

VERDICT: candidate at `290ac2e9` closes K8–K14 — C2 counter 21/21 at seeds 59/1/20261027 (base 13/21 same seed), tool selftest 69/69, real lane `ids_cited=108 dangling=0` unchanged; no lane, fleet or external state mutated.
