# ExecGuardTool

Claim C2 primary implementation: `scripts/append_guard.py` candidate, delivered at
`.ufo/waves/round-60/w1/ExecGuardTool.files/append_guard.py` (stdlib only, python3 >= 3.10,
671 lines). Contract § Claim C2 implemented literally.

## DESIGN:

- **CLI / plumbing.** `--root/--base/--revision [--scope glob ...] [--json] [--selftest]`;
  custom `ArgumentParser.error` maps every usage failure to exit 64 (K21 verified). Git access
  is committed-bytes only: `rev-parse --show-toplevel`, `rev-parse --verify --quiet
  --end-of-options <rev>^{commit}`, `merge-base --is-ancestor --`, `ls-tree -r`, `cat-file
  blob`. The worktree is never opened; every child env is rebuilt without inherited `GIT_*`
  (X12 selftest: `GIT_DIR=/nonexistent` still exits 0). Exit order: root must be the repo
  toplevel (realpath compared; subdir root → 2, X10) → base/revision resolve →
  `merge-base --is-ancestor` (K20 → 2; equal base=rev is allowed, X11) → trees.
- **Population.** Every base-tree entry that is a regular blob (`100644`/`100755`) whose path
  matches scope. Scope globs translate `**/` to zero-or-more directories, so the default
  `corpus/knowledge/**/*.md` matches nested files (K22) and still requires the
  `corpus/knowledge/` prefix (K17 `SKILL.md` untouched → clean). Missing-at-revision or
  non-blob-at-revision (symlink K18, gitlink, tree) → `deleted P`; renames show as `deleted`
  on the old path (K7); revision-new paths are unchecked (K11).
- **Line model.** `content.split(b"\n")`, drop one trailing `b""`. Raw bytes, no decode, no
  normalisation — so K4/K12/K13 (byte change, swap, trailing space) and K14 (CRLF) all leave
  B not a subsequence of R → `changed`. K19 (`\xff\xfe` appended after final newline) is one
  new trailing line → EOF append → clean.
- **changed vs untagged.** Greedy leftmost subsequence match decides `changed`; only if B is
  a subsequence does the tag rule run.
- **Tag visibility.** `\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]` searched as bytes.
  Per line a visibility mask hides (a) `<!--` .. `-->` regions — comment state is carried
  across lines, so an unclosed `<!--` hides to EOF (K9 and X9 both fail); (b) backtick code
  spans — a run of N backticks opens a span closed only by an equal-length run on the same
  line, span masks delimiters and interior; an unclosed run is literal text (K10 fails).
  A tag is visible iff some regex match starts on an unmasked character (K2 `**[r60-…]**`
  visible; X14 bad year shape invisible).
- **untagged_insertion — existential rule.** `untagged_insertion P:<line>` is emitted iff
  *no* alignment of B into R leaves every non-EOF inserted run starting with a tagged line.
  Implemented as a DP over states `(i, in_run)` consuming R left-to-right: match needs
  `r == B[i]`; an insertion extends a run freely (`in_run`), starts an EOF-append run once
  `i == m`, or starts a mid-file run only when `r` is tagged. Runs are "non-EOF" when they
  start at or before the last matched base line, so prepends are checked too (X2 tagged→0,
  X3 untagged→1). Complexity O(n·m) states worst case, each O(1); typical runs are tiny.
  `<line>` is the 1-based revision line of the first bad run under the leftmost alignment
  (any clean alignment existing ⟹ every alignment's bad runs are impossible; the reported
  line is then from the canonical leftmost one).
- **Output.** One `kind path[:line]` per line, sorted by path then kind, then
  `files=<n> findings=<k>` (`files` = in-scope base blobs evaluated). Also printed on the
  exit-2 path (stdout summary, error on stderr) so the last line is always the summary;
  `--json` emits `{schema, findings[], files, findings_count, exit, error?}` (X15).
- **Existential cases exercised.** K15 `a,""/b`→`a,TAG,""/"",b` style: leftmost alignment
  leaves untagged `""` mid-file, the alternate alignment makes the run `TAG,""` → 0. K16
  untagged duplicate `b`: no alignment rescues → 1. X13: leftmost leaves a lone untagged `x`
  run, DP finds the clean alignment → 0.

## SELFTEST:

`--selftest` builds a `git init` fixture repo per case under `$TMPDIR` (identity
`selftest <selftest@local>`; asserts `rev-parse --show-toplevel` == fixture dir before and
after commits), runs the tool **as a subprocess**, and asserts both exit code and every
expected `kind path` token on stdout. **38/38 cases pass** (all 22 contract K-cases incl.
R-side equivalents verified separately, plus 16 supplementary: empty-base fill, tagged/
untagged prepends, mid-file+EOF combo, indented bold tag, second-tagged-line rescue
rejection, mode-only change 100644→100755 → 0, narrowed `--scope`, subdir root → 2,
base==rev → 0, `GIT_DIR` scrub, malformed-year tag → 1, `--json` parse). Runtime ~1.8 s.

## REAL LANE:

Both required invocations (outputs verbatim):

    $ python3 -B append_guard.py --root /home/vgpnk/Projects/shokunin/kake-shokunin \
        --base fd6303ce5c14b3f892dec586297a942ab6e4193b \
        --revision 97cdc122379711c2b02a8970752c8782da3ac81d
    files=53 findings=0          (exit 0)

    $ python3 -B append_guard.py --root /home/vgpnk/Projects/shokunin/kake-shokunin \
        --base 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 \
        --revision 97cdc122379711c2b02a8970752c8782da3ac81d
    files=46 findings=0          (exit 0)

The r59 correction block in `corpus/knowledge/crawler-identity.md` (16 inserted lines mid-file,
first line `  **[r59-correction 2026-10-27]** …`) is accepted as a tagged run — the R1 fixture
the byte-prefix port failed. Mutation probe on a `git clone --shared` of the lane detached at
`97cdc12`, one byte of a base line changed + one untagged mid-file line committed by the
selftest identity, produced:

    untagged_insertion corpus/knowledge/baidu-friendly-crawl-guidance.md:6
    changed corpus/knowledge/crawler-identity.md
    files=55 findings=2          (exit 1)

matching R2's expected `changed corpus/knowledge/crawler-identity.md` and confirming both
finding kinds on real lane bytes. `--root <lane>/corpus` exits 2 (not a toplevel).

## LIMITS:

- "Backtick code span" is enforced per line only; fenced code blocks (``` fences) are *not*
  masked — a tag inside a fenced block counts as visible. Contract wording names code spans,
  not fences; flag for w2 review.
- HTML-comment state is tracked across lines but the opener/closer search is a plain byte
  scan — `<!--` inside a code span on the same line is ignored, yet one inside a fenced block
  or inside an unterminated earlier code span could mis-set comment state (rare in lane md).
- `files=` counts in-scope regular blobs evaluated at base (deleted included), not files with
  findings; `findings=` counts emitted lines (max one per file).
- An empty base file treats all of R as an EOF append (byte-prefix `startswith(b"")` special
  case): fills with no tag → 0. Chosen deliberately; the literal reading is ambiguous here.
- `untagged_insertion` line number is the first bad run of the leftmost alignment — a stable
  convention, not existentially quantified; contract requires only kind+path.
- Only `ls-tree -r` default format parsed; non-UTF-8 paths surface via `os.fsdecode`
  surrogates. No repo lock/network; runtime on lane < 3 s.

VERDICT: append_guard.py delivered — 38/38 selftest cases pass and both real-lane runs exit 0 with `findings=0`; ready for L1 integration at `scripts/append_guard.py`.
