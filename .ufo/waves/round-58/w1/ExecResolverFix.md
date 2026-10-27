# ExecResolverFix

C2 (operability) build seat. Candidate tool (never the lane file):
`.ufo/waves/round-58/w1/ExecResolverFix.files/id_resolver.py`. Lane `scripts/id_resolver.py` was not written
by me (no git/jj mutation in the lane either). Candidate base = the committed blob at
`044048597d62f3199494b63b36e90dd57825e350` = lane HEAD `cc8da1674d6e` blob (sha256
`25982446d2e6…461bee`; `git diff 0440485..HEAD -- scripts/id_resolver.py` empty). Note for the L1: at 20:57
one snapshot of the lane worktree file hashed differently (`git status` said ` M`); it re-hashed to the HEAD
blob minutes later and is clean now — another seat touched it, not me; every receipt here was regenerated
from `git show <rev>:scripts/id_resolver.py`. Gate clone: shared clone at the base revision, candidate
committed as `58976c081091d0c30223ebf181ad2abf7409755c` (selftest identity). python3 3.14.8, git 2.56.0; no
install or upgrade needed.

## DIFF:

`diff -u` vs the committed base blob (full 196-line diff, selftest hunks included, = `.files/candidate.diff`):

```
--- scripts/id_resolver.py        (0440485 = HEAD blob)
+++ .ufo/waves/round-58/w1/ExecResolverFix.files/id_resolver.py
@@ -10,9 +10,13 @@

   - cited ids: every word-bounded `S` + 3 or more digits in each `corpus/knowledge/**/*.md`
-    file; with `--revision` the blobs are read through `git show`, never the working tree
+    file; with `--revision` the paths come from `git ls-tree -r -z` (NUL split, so a git-quoted or
+    non-ASCII name is read as itself) and the blobs through `git show`, never the working tree
     (the lane registry is read at the same revision, for the same reason).
   - registry ids: first cell of each table row (a one-cell row counts) of `corpus/SOURCES.md` under the
     exact heading `## Registry` (the section ends at the next `# ` or `## ` heading), 0 to 3 leading spaces
-    before the pipe (the census parser's rule; 4 spaces is code).
+    before the pipe (the census parser's rule; 4 spaces is code). Fenced code blocks are CommonMark's:
+    a line of 0 to 3 spaces then 3 or more backticks or 3 or more tildes opens a block that only a line of
+    the same character, at least as long, with nothing but whitespace after it (0 to 3 spaces) or EOF closes;
+    a heading or a table row inside such a block counts for nothing here (the census still counts it — the stated divergence).
   - siblings: every `<fleet>/*-shokunin/` other than the lane (by realpath); a sibling's
@@ -43,4 +47,6 @@
 REGISTRY_HEADING_RE = re.compile(r"^##\s+Registry\s*$")
 SECTION_END_RE = re.compile(r"^#{1,2}\s")
+FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
+FENCE_CLOSE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")
 REGISTRY_REL = "corpus/SOURCES.md"
@@ -78,10 +84,39 @@


+def _nul_paths(data):
+    """Paths of a `git ls-tree -z` listing: NUL separated, never C-quoted."""
+    return [chunk.decode("utf-8", "replace") for chunk in data.split(b"\0") if chunk]
+
+
+def _fence(line):
+    """(char, length) when `line` opens a CommonMark fenced block, else None."""
+    m = FENCE_OPEN_RE.match(line)
+    if not m:
+        return None
+    run = m.group(1)
+    if run[0] == "`" and "`" in m.group(2):  # a backtick fence's info string may not hold a backtick
+        return None
+    return run[0], len(run)
+
+
+def _fence_closes(line, char, length):
+    m = FENCE_CLOSE_RE.match(line)
+    return bool(m) and m.group(1)[0] == char and len(m.group(1)) >= length
+
+
 def parse_registry(text):
-    """Map id -> [urls] for rows of the `## Registry` section (0-3 leading spaces)."""
+    """Map id -> [urls] for rows of the `## Registry` section (0-3 leading spaces, outside fenced code)."""
     rows = {}
     inside = False
+    fence = None
     for raw in text.splitlines():
         line = raw.rstrip("\r")
+        if fence is not None:  # a heading or a table row inside a fenced block counts for nothing
+            if _fence_closes(line, *fence):
+                fence = None
+            continue
+        fence = _fence(line)
+        if fence is not None:
+            continue
         if REGISTRY_HEADING_RE.match(line):
             inside = True
@@ -142,8 +177,8 @@
     """Map repo-relative path -> text, read from the revision blobs or the working tree."""
     if revision:
-        proc = _git(root, "ls-tree", "-r", "--name-only", revision)
+        proc = _git(root, "ls-tree", "-r", "-z", "--name-only", revision)
         if proc.returncode != 0:
             return None, f"cannot list {revision[:12]}: {_text(proc).strip()}"
-        rels = [rel for rel in _text(proc).splitlines()
+        rels = [rel for rel in _nul_paths(proc.stdout)
                 if rel.startswith(KNOWLEDGE_REL + "/") and rel.endswith(".md")]
         bodies = {}
```

Selftest hunks: helper `_fenced_row_case` + 10 cases (fenced heading+row before Registry; fenced row inside
Registry with ``` and with `~~~`; 3-space fence; longer closing run closes; row after a closed fence
resolves; shorter run does not close; unclosed fence swallows the rest; non-ASCII path at a revision;
`"`-bearing path at a revision) + their 10 `_cases()` entries.

## SELFTEST:

`python3 -B .files/id_resolver.py --selftest` -> `selftest: 59/59`, exit 0 (base 49/49; +10 cases, no
existing case edited). Tally at `.files/selftest.txt`.

## GATE RUN:

    python3 -B .ufo/waves/round-58/c58_resolver_cases.py --root <clone> --revision 58976c081091 --work <scratch>/work

```
C2 resolver-cases 12/12 met=True  (met: cases_passed == 12 of 12)
  K1_fenced_heading_before_registry PASS  exit=1 DANGLING S950 cited-by=corpus/knowledge/ok.md owners=- url-match=- | ids_cited=2 ids_resolved=1 dangling=1 owned_elsewhere=0 unowned=1
  K2_backtick_fence_inside_registry PASS  exit=1 DANGLING S951 cited-by=corpus/knowledge/ok.md owners=- url-match=- | ids_cited=2 ids_resolved=1 dangling=1 owned_elsewhere=0 unowned=1
  K3_tilde_fence_inside_registry PASS  exit=1 DANGLING S952 cited-by=corpus/knowledge/ok.md owners=- url-match=- | ids_cited=2 ids_resolved=1 dangling=1 owned_elsewhere=0 unowned=1
  K4_non_ascii_path_at_revision PASS  exit=1 DANGLING S900 cited-by=corpus/knowledge/中文.md owners=- url-match=- | ids_cited=2 ids_resolved=1 dangling=1 owned_elsewhere=0 unowned=1
  K5_git_quoted_path_at_revision PASS  exit=1 DANGLING S901 cited-by=corpus/knowledge/a"b.md owners=- url-match=- | ids_cited=2 ids_resolved=1 dangling=1 owned_elsewhere=0 unowned=1
  P1_three_space_row_resolves PASS  exit=0 ids_cited=1 ids_resolved=1 dangling=0 owned_elsewhere=0 unowned=0
  P2_row_after_closed_fence_resolves PASS  exit=0 ids_cited=2 ids_resolved=2 dangling=0 owned_elsewhere=0 unowned=0
  P3_four_space_line_is_code PASS  exit=1 DANGLING S003 cited-by=corpus/knowledge/ok.md owners=- url-match=- | ids_cited=2 ids_resolved=1 dangling=1 owned_elsewhere=0 unowned=1
  P4_committed_sibling_owns PASS  exit=1 DANGLING S004 cited-by=corpus/knowledge/ok.md owners=alpha-shokunin url-match=- | ids_cited=2 ids_resolved=1 dangling=1 owned_elsewhere=1 unowned=0
  P5_absent_fleet_is_unevaluable PASS  exit=2 id_resolver: unevaluable: fleet root /fast/scratch/hyaku/kake-r58/ExecResolverFix/work/c58-rc-51ixqivc/p5/no-such-fleet is not a directory
  P6_tool_selftest PASS  exit=0 ('59', '59')
  P7_real_lane_green PASS  exit=0 ids_cited=106 ids_resolved=106 dangling=0 
  revision: 58976c081091d0c30223ebf181ad2abf7409755c
EXIT=0
```

Do-nothing control, same counter at `0440485` (`.files/base-control.txt`): `7/12 met=False`, exit 1; K1–K5
FAIL as the contract states (`K1 exit=0 … dangling=0`; `K4/K5 ids_cited=1`), P1–P7 PASS, P6 `('49','49')`.
Verbatim capture: `.files/gate-run.txt`.

## BEHAVIOUR CHANGES:

1. `parse_registry` is shared by the lane registry (worktree and `--revision`) and every sibling registry,
   so a fenced row registers nowhere: an id whose only row sits in a fence loses owner/url-match (before
   `owned_elsewhere=1`, now `unowned=1`). The census still counts fenced rows — the contract's stated divergence.
2. Fence state is file-global and the section state survives inside a fence: a `## Paths`-looking heading
   inside an open fence no longer ends the Registry section; an unclosed fence suppresses every later
   heading and row to EOF (K1's false-green path); rows register again after the closing line (P2 holds).
3. CommonMark details enforced: a backtick fence whose info string holds a backtick opens nothing; a
   shorter run or the other fence character does not close; a closing line with trailing non-whitespace
   does not close; 0–3 leading spaces open, 4+ do not (P3 unchanged).
4. `--revision` listing: base dropped every path git C-quotes (non-ASCII, `"`, `\`, control chars) and
   split names on embedded newlines; now each path is read as itself. Measured probe
   (`.files/probe-f1.txt`): base `ids_cited=1 … dangling=0 exit=0`, candidate `ids_cited=3 … dangling=2 exit=1`
   naming both the newline-named and `back\slash.md` files. A newline in a path is printed raw inside
   `cited-by=`, so that record spans two lines (no escape; probe-only, the lane and fleet hold no such path).
5. Real data unmoved: (a) base vs candidate stdout on the real lane at `0440485`, `--fleet` = real root, is
   byte-identical — `ids_cited=106 ids_resolved=106 dangling=0 owned_elsewhere=0 unowned=0`
   (`.files/real-lane-{base,candidate}.out`); (b) `parse_registry` row-map parity over all 21 fleet
   registries at HEAD: `registries_differing=0` (kake 160, kotodama 808, mado 276 rows;
   `.files/registry-parse-parity.txt`). `game-dev-2d-shokunin` is the only sibling with fence lines (4, in
   `## Search log` after the Registry section ended at `## Paths`) and its 31-row map is unchanged.
6. Docstring contract lines updated to match both fixes (incl. the census divergence note).

Risks / unverified: [INFERENCE] a lane that wraps its whole registry table in a fence would register
nothing (every cited id dangles — loud, not a false green). [INFERENCE] a non-ASCII path argument to
`git show` depends on Python's filesystem encoding (UTF-8 under `LC_ALL=C` on 3.7+; K4 passed under the
gate's `C.UTF-8`). Not mine to test: the census tool, sibling ownership beyond P4, the counter's own
selftest (stub in version 1). Scratch `/fast/scratch/hyaku/kake-r58/ExecResolverFix` removed after
copying receipts; no credentials, tokens or private URLs in this report.

VERDICT: C2 candidate fixes D1 (fence-aware `parse_registry`, `selftest: 59/59`) and F1 (`ls-tree -r -z` NUL paths); gate 12/12 exit 0 vs base 7/12 exit 1; real-lane output byte-identical — ready to integrate.
