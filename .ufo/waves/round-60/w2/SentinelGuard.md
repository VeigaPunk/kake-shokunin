# SentinelGuard

ATTACKS: `scripts/append_guard.py` at B1 `8b33fd24` — scope-escape (`..`, absolute, glob, empty),
option injection through `--base`/`--revision`, tree/tag/abbrev revisions, hostile file names
(non-ASCII, quote, backslash, tab, newline, git quoting), ambient git config, symlinked `--root`,
`GIT_*` env, blob size (DP time/memory), worktree independence, and whether the real-lane R1 pass is
load-bearing. Everything below was run; fixtures are under
`/fast/scratch/hyaku/kake-r60/SentinelGuard/` (deleted at exit); the rerunnable driver is
`SentinelGuard.files/repro.sh` (writes only its own scratch, asserts fixture toplevel before any commit).

## ATTACKS RUN (exact commands, observed output)

Tool under test is the *committed* blob at B1, read from a `git clone -q --shared` of the lane detached
at `8b33fd24` (`$S/lane/scripts/append_guard.py`); `--root` values are my fixtures or that clone.

1. **Quoted path names (the one that breaks the rule).**
   fixture base: `corpus/knowledge/keep.md`, `corpus/knowledge/naïve.md`; revision rewrites `naïve.md`.
   ```
   $ git -C "$D" ls-tree -r "$B"
   100644 blob 97b4b8df…	corpus/knowledge/keep.md
   100644 blob 587be6b4…	"corpus/knowledge/na\303\257ve.md"
   $ python3 -B scripts/append_guard.py --root "$D" --base "$B" --revision "$R"
   files=1 findings=0            rc=0        <-- false clean; the rewrite is invisible
   $ HOME=<dir with .gitconfig core.quotePath=false> python3 -B … (same argv, same commits)
   changed corpus/knowledge/naïve.md
   files=2 findings=1            rc=1        <-- same input, opposite verdict
   ```
   Deletion of the same file: `files=1 findings=0 rc=0` (no `deleted`). Same for names with `"`, `\`,
   tab, newline: base tree shows `"corpus/knowledge/quo\"te.md"`, `"corpus/knowledge/back\\slash.md"`,
   `"corpus/knowledge/tab\tname.md"`, `"corpus/knowledge/we\nird.md"`; all three rewrites →
   `files=2 findings=0 rc=0` while 5 in-scope `.md` blobs exist at base.
2. **Scope escapes.** `--scope ''`, `'/etc/passwd'`, `'../**/*.md'`, `'../../../../**'`,
   `'corpus/knowledge/[a-'`, `'-x'` → all `files=0 findings=0 rc=0`. Traversal itself is *not* possible
   (git tree paths cannot leave the tree; `--scope '**'` reads only repo objects) — the defect is the
   silent zero-coverage success. `--scope '[[:alpha:]]*'` additionally emits
   `FutureWarning: Possible nested set at position 5` but still exits 0.
3. **Option injection.** `--revision=--output=pwn`, `--base=--help`, `--revision=--upload-pack=x`,
   `--revision=--all`, `--base=--all` → `append_guard: unevaluable: … does not resolve to a commit`,
   `rc=2`, no file created (`ls "$D/pwn"` → No such file); `--scope=-x` parses as a value, not an option.
4. **Revision shapes.** `$R^{tree}` → `rc=2` "does not resolve to a commit"; annotated tag → `rc=0`
   (files=2); 7-char abbrev `--base` → `rc=0`; `--root` a file / a subdirectory / `""` → `rc=2`/`rc=2`/`rc=64`.
5. **Symlinked `--root`**: `link -> repo` → `rc=0`; `link2 -> repo/corpus` → `rc=2`.
6. **`GIT_*`**: `GIT_DIR/GIT_WORK_TREE/GIT_OBJECT_DIRECTORY/GIT_ALTERNATE_OBJECT_DIRECTORIES/GIT_INDEX_FILE/
   GIT_COMMON_DIR=/nonexistent` → `rc=0`; `GIT_DIR=<another real repo>/.git GIT_WORK_TREE=…` → `rc=0`
   (scrubbed, no cross-repo read). Ambient `HOME/.gitconfig` is *not* isolated (see finding 1).
7. **Subprocess audit** (PATH shim logging argv), real-lane window `fd6303ce..8b33fd24`: 112 git calls —
   106 `cat-file` for 54 distinct oids, 2 `ls-tree`, 1 `merge-base`, 3 `rev-parse`; zero
   `show/diff/status/ls-files/checkout/grep/--work-tree`. Dirtying `corpus/knowledge/crawler-identity.md`
   in a clone's worktree while `--base == --revision` still gives `files=57 findings=0 rc=0` → the
   "committed bytes only" claim holds.
8. **Blob size.** 60 MB dup-heavy in-scope blob: `exit=0 wall=1.44s peak_rss=513 MiB` (~8.5× the blob).
   DP probe (tags interleaved so the state set widens): n=500/1000/2000/4000 lines →
   0.011/0.042/0.182/0.808 s (quadratic); largest real file `corpus/knowledge/free-read-verbs.md` is
   503 lines / 438 distinct, so no live impact.
9. **Is R1 vacuous?** In `fd6303ce..B1` only *one* in-scope `corpus/knowledge/*.md` is modified
   (`crawler-identity.md`); `googlebot-verification.md`, `robots-txt-limits.md`,
   `google-user-triggered-fetchers.md`, `crawler-identity-signals.md` are *added* (skipped by rule;
   `googlebot-verification.md` is absent at `fd6303ce`, present at the round base `97cdc12`). Removing
   the `[r59-correction 2026-10-27]` token from the one real inserted run in a scratch clone →
   `untagged_insertion corpus/knowledge/crawler-identity.md:35 rc=1`; unchanged → `files=53 findings=0
   rc=0`. The tag is load-bearing: R1 is a genuine tagged-mid-file case.
10. **Frozen counters at B1** (allowed): `c60_guard_cases.py --root . --revision 8b33fd24` → all
    K1–K22, R1, R2 `PASS`, `EXIT=0`, seed 2493026749 (24/24). `append_guard.py --selftest` → `38/38`.

## FINDINGS

| severity | target | issue | evidence | fix |
|---|---|---|---|---|
| high | `scripts/append_guard.py:93` (+`:103`) | `git ls-tree -r` output is parsed as a line-per-path format, but git *quotes* names containing non-ASCII/high bytes, `"`, `\`, tab or newline (`core.quotePath`, default true). The quoted token (`"corpus/knowledge/na\303\257ve.md"`) no longer starts with `corpus/knowledge/`, so `in_scope` rejects it: no `changed`, no `deleted`, `files=` undercounts, **exit 0** — the rule "every path P in scope that is a regular blob at base" is violated silently. Latent at B1 (0 of 57 in-scope paths non-ASCII), permanent for any name like `日本語.md`. Also non-hermetic: an ambient `.gitconfig core.quotePath=false` flips the verdict on identical commits. | `repro.sh` §F1 (above): `files=1 findings=0 rc=0` vs `changed … files=2 findings=1 rc=1` for the same argv; tree shows `"…na\303\257ve.md"` | `git(root, "-c", "core.quotePath=false", "ls-tree", "-r", "-z", rev)` and split on `b"\0"` — the round's own counter already does exactly this (`c60_guard_cases.py:403,493`), the tool does not |
| medium | `c60_guard_cases.py:48` (`ALL_IDS`) / append_guard `--selftest` | No case in the 24-case suite or in the 38-case selftest uses a name git quotes (`LC_ALL=C grep -c '[^ -~]'` on every fixture path = 0; ids are `amber-orbit-basalt.md`-style ASCII), so `met: cases_passed == 24 of 24` certifies the rule but not the path model. 24/24 is true and still does not exclude finding 1. | `python3 -B .ufo/waves/round-60/c60_guard_cases.py --root . --revision 8b33fd24` → `EXIT=0`; the fixture in finding 1 fails the same tool | add `K23` (base `corpus/knowledge/naïve.md` rewritten → 1 `changed`) to the selftest and, in a v2 counter (a tightening, permitted), to the case table |
| medium | `scripts/append_guard.py:649`,`:307` | An effective scope that matches nothing is reported as success: `--scope ''`, `--scope '/etc/passwd'`, `--scope '../**/*.md'`, `--scope 'corpus/knowledge/[a-'` → `files=0 findings=0 rc=0`. A CI caller reading only the exit code (the contract's kill rule) takes zero coverage for "clean". | `repro.sh` §F3 | `files == 0` → `exit 2` with `"scope matched no blob at base"` (a narrowing, consistent with "2 could-not-evaluate") |
| low | `scripts/append_guard.py:340` | Every in-scope blob is fetched twice even when unchanged: content is compared *after* two `cat-file` calls, although `ls-tree` already hands back both oids. 106 `cat-file` calls for 54 distinct oids per real-lane run; cost scales with corpus size, not with the size of the change. | PATH shim audit (`SentinelGuard.files/e2-git-calls.log`): `cat-file=106 distinct_oids=54` | `if base_tree[path][1] == ent[1]: continue` before `blob_bytes` |
| low | `scripts/append_guard.py:338-344` | No input bound: both blobs are read fully through pipes and split into one `bytes` object per line — 60 MB in-scope blob → 513 MiB peak RSS, and `--scope` is user-widenable to any committed blob. | `repro.sh` §F5 | skip (or stream) blobs above a cap, e.g. 8 MiB, with a `files=`/exit-2 note |
| low | `scripts/append_guard.py:349`,`:351` | The expensive existential DP runs before the cheap sufficient test: `any_clean_alignment` is called first and `first_untagged_run(leftmost)` (O(n), and exactly the "leftmost is clean" case that holds for realistic files) only afterwards. With tags present the state set widens and the DP is quadratic (0.011→0.808 s from n=500→4000). No live impact: real files ≤503 lines. | `repro.sh` §F6 | test `first_untagged_run` first, return clean if `None`, else run the DP |
| low | `scripts/append_guard.py:315-330` | `toplevel()` realpaths its answer and compares it to `realpath(root)`, but every later git call receives the *original* `root` string, so a `--root` symlink re-pointed between validation and use would be evaluated against a different repository than the one validated. [INFERENCE] — not demonstrated (would need a mid-run swap); the symlinked-root acceptance itself is verified (`rc=0`). | code read + attack 5 | replace `root` with the validated `t` for all subsequent calls (`git(t, …)`), or open the repo once and pass the resolved path |

Attacks that held (no finding): option injection through `--base`/`--revision` (`--end-of-options` plus
the `^{commit}` peel defeats `--output=`, `--help`, `--all`, `--upload-pack=`; `rc=2`, no side effect);
tree/blob ids as revisions (`rc=2`); tags and abbreviations (resolve as documented); `GIT_*` scrubbing;
`--root` must be a toplevel; committed-bytes-only (zero worktree-reading subprocesses; dirty worktree
ignored); stdout framing (quoted/odd names can never inject a second finding or summary line, so the
counter's exact-set rule cannot be fooled into a false pass); the tag rule itself (K1–K22 + the R1
mutation behave exactly as the contract states, including tag-in-comment, tag-in-code-span,
tag-on-second-line, duplicate-line parking).

No tool was installed or upgraded during this seat (system `python3` 3.14.8, `git` from base). Fleet repo,
sibling lanes and the lane's git/jj state untouched: writes were confined to this report,
`SentinelGuard.files/`, and `/fast/scratch/hyaku/kake-r60/SentinelGuard/` (removed).

VERDICT: C2's frozen counter is honest (24/24 at B1) but the tool it certifies has one high-severity
false-clean class — every git-quoted path (`naïve.md`, `we"ird.md`, `we\nird.md`) is silently out of
scope, exit 0 — with three low-severity robustness debts; fix the `ls-tree -z`/`quotePath` parse and add
the missing case.
