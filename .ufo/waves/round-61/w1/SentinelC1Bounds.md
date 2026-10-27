# SentinelC1Bounds

Scope: execution-safety review of the C1 design surface (`scripts/receipt_lineage.py`, the 144-path population,
`.ufo/receipt-disclosures.json`) **before freeze**. The tool does not exist yet — absent at base `9f07731` and at
tip `eaa9177`, and the sibling scratch dirs `ExecC1Tool`/`ExecC1Tool2`/`ExecC1Counter` were empty when checked — so
each finding is **measured against the lane or a fixture**, or marked `[INFERENCE]` (design-only, unrun). Nothing
here scores an after-state; the counters stay unmeasured by this seat.

Method: read `contract.md`, `population-144.txt`, the sibling registry `.ufo/receipt-disclosures.json`, and the
lane's precedent `c58_receipt_rewrites.py` (present at base); built throwaway fixtures with the toplevel asserted
before every commit; reimplemented the frozen rules once to test whether the contract's own real-lane expectation is
reachable. Every measured output is in `SentinelC1Bounds.files/evidence.txt`.

FINDINGS:

**S1 — CRITICAL — the frozen range `base..revision` makes the real-lane case either vacuous or 12-phantom.**
Measured: `base..tip` holds **1** commit and **0** population-path touches, so a range-bounded walk yields
`events=0 undisclosed=0` — clean by vacuity. Every one of the registry's **12** entries names a commit that is an
**ancestor of base**, so if the tool checks disclosures against in-range events it emits **12
`phantom_disclosure`** and exits 1. Meanwhile, the contract's own definition ("the commit that first added the file,
through the revision under test") over the full first-parent history yields exactly **12** events, which the
registry covers 12/12. The registry was built for the full-history reading; the contract text says
`base..revision`. **Fix (freeze before w2):** walk the full first-parent history of each path to the revision;
`--base` is the *population freeze point only* (`members`), never the walk start. Rewrite the Rules sentence and
R2 accordingly.

**S2 — CRITICAL — "the set of lines ... matching" is ambiguous, and the wrong reading blinds the tool to exactly
the r56/r57 class.** Measured on the same population and commits: whole-line extraction → **12** events (registry
12/12, 0 phantom); matched-substring extraction (`m.group(0)`) → **3** events, i.e. **9 phantom_disclosure** →
met=False. The substring reading cannot see `revision: A → B` (the matched keyword text is unchanged), `EXIT=0 →
EXIT=1`, or `met=False → met=True` — the very relabel that motivates C1, and the shape of fixtures **L2 and L6.**
**Fix:** freeze "the whole line containing a match" as the span, state it in the Rules sentence and in the
counter's docstring, and add two fixtures the current table lacks: **L2b** `EXIT=0 → EXIT=1` undisclosed → 1
`undisclosed_rewrite`; **L2c** `revision: <a> → <b>` with every other byte equal → 1 `undisclosed_rewrite`.

**S3 — HIGH — R2's expected numbers are factually wrong, so the predicate can only be met by a tool that
classifies nothing.** Measured over the 144 frozen paths: **95** carry the receipt grammar (49 are JSON controls),
**members=144** (all byte-identical base..tip), **events=12**. R2 as written expects `receipts=144 events=<k>
undisclosed=0`; a literal implementation prints `receipts=95`, and a tool that classifies zero receipts still
satisfies `undisclosed=0`. **Fix:** freeze R2 as `members==144 AND receipts==95 AND undisclosed==0` (all three now
measured) and add **L17**: a member added *before* the population freeze point whose result span is rewritten
afterwards, undisclosed → exactly 1 finding. Without L17 the only shape the real lane has (all 144 added pre-base)
is never exercised, and the pre-base-add rule is untested.

**S4 — CRITICAL — `extra_member` as written fires 480+ times at base and on the round's own controls.**
The contract's path rule is the lane's `POP_RE = ^\.ufo/waves/round-[0-9]+/(control|controls)/.+$` (c58 line 67).
Measured: it matches **607** files at base and **610** at tip against a **144**-line frozen list → 480 `extra_member`
findings before this round does anything, plus `census-before.txt` and `population-144.txt` from the round's own
controls directory. In the other direction, **17** frozen members do *not* match the anchored rule (nested
`round-37/retained/controls/…`, `round-48/assimilation/validate/…`). **Fix:** the frozen list *is* the membership
definition (`members` = frozen paths present with unchanged blob, measured 144/144); define `extra_member` as paths
added in the measured range that match the rule **and** are not under the declaring round's prefix
`.ufo/waves/round-61/` (c58's precedent: a round-scoped `NEW_RE`). State the exclusion; put L11's extra file under
a round ≠ 61.

**S5 — HIGH — disclosures read from the worktree defeat the claim; the registry is untracked as I checked.**
One uncommitted edit adding `{path, commit}` makes an undisclosed rewrite report clean, and a cwd-relative
`--disclosures` lets `cd lane && tool --root fixture` apply the lane's registry to a fixture. The lane's precedent
already reads the analogue ledger from committed bytes (`git show tip:LEDGER`, c58 line 191); the new registry is
currently an **untracked** worktree file, so a worktree read would be reading something the measured revision does
not contain. **Fix:** resolve disclosures as `<revision>:<path>` via `cat-file blob`; reject absolute paths and `..`
(exit 2); absent-at-revision → zero entries (distinct from malformed → exit 2); exact 40-hex `commit` equality (a
short SHA is malformed → 2, never silently `phantom_disclosure`). Counter consequence: fixtures L3/L8/L12/L13 must
**commit** their disclosures blob.

**S6 — HIGH — `GIT_DIR`/`GIT_WORK_TREE` injection passes the toplevel gate while resolving a foreign object
store.** Measured: with `GIT_DIR=<other>/.git`, `git -C <fixture> rev-parse --show-toplevel` still prints the
**fixture** — the gate the contract asks for passes — yet `rev-parse --verify <other-HEAD>^{commit}` succeeds, and
the same query with `GIT_DIR` unset fails. **Fix:** scrub every `GIT_*` (house idiom, c58 line 76) *and* assert
`rev-parse --absolute-git-dir == realpath(root)/.git` before walking.

**S7 — HIGH (evasion, no commit required) — `git replace` blinds the tool.** Measured: `git replace <v1blob>
<v2blob>` makes `cat-file blob <v1blob>` return the v2 body, so both sides of every comparison read identically and
no event is found; `--no-replace-objects` restores the true bytes. Replace refs are local, unpushed and invisible in
any tree check. **Fix:** pass `git --no-replace-objects <cmd>` on every invocation, and give the counter a real-lane
invariant: `git for-each-ref refs/replace` is empty. (c58 line 80 omits this; the new tool must not inherit it.)

**S8 — HIGH (provenance) — C1's motivation is false at base: the lane *does* own a committed check for this class.**
`contract.md` C1 says "the lane owns no committed check for the class" and "only the external verifier caught
either". At `9f07731`, `.ufo/waves/round-58/c58_receipt_rewrites.py` (v2, 592 lines) already walks every path ever
committed under `control(s)/` on the first-parent line, with a blob-pinned disclosure ledger
(`.ufo/waves/round-58/receipt-rewrites.json`), and `phantom`/`malformed`/`wrong_kind`/`symlinks`/`pending-fill`
classes; `SCORECARD.md` calibration cites its after receipt (`events=19, undisclosed=0`). Shipping a second
instrument with a weaker schema (no `fromBlob`/`toBlob`/`status`, no note-path check) leaves two divergent sources of
truth: a rewrite disclosed in one ledger and undisclosed in the other. **Fix:** generalise the round-58 ledger to
the repo-level path with a named migration (keeping its fields), or retire c58 in the same commit as the cutover;
correct the motivation sentence before freeze.

**S9 — MEDIUM — symlinked control files are blobs, so "a non-blob population path is skipped" does not cover them.**
Measured: a committed symlink is mode `120000` and `cat-file blob` returns the **link-target text** (no arbitrary
read — good), i.e. a symlink is silently treated as file content: a re-pointed link becomes a rewrite candidate.
**Fix:** gate on `git ls-tree <rev> -- <path>`: accept only `100644`/`100755`; skip `120000`/`160000` with a named
note; reword the contract clause to "non-regular-file mode".

**S10 — MEDIUM — gitlinks defeat size prechecks and are indistinguishable from absence.** Measured:
`cat-file blob HEAD:<gitlink>` → rc 128 `bad file`, while `cat-file -s HEAD:<gitlink>` → **rc 0** with the commit
object's size (154). A cap-then-read implementation passes the cap and then fails; and rc 128 is also what "does not
exist" returns, so a submodule degrades to `member_missing`. **Fix:** classify by `ls-tree` type first, then read;
never map rc≠0 straight to "missing".

**S11 — MEDIUM — traversal/absolute population lines cannot escape the repo, but they degrade to
`member_missing`.** Measured: `HEAD:…/../outside.txt` → rc 128 "does not exist in HEAD"; `HEAD:/etc/passwd` →
"exists on disk, but not in HEAD" (confined to the tree). No escape — but a malformed entry is byte-indistinguishable
from a deleted receipt. **Fix:** validate each line lexically (non-empty, no NUL, no leading `/`, no `..` component,
byte-identical to the frozen line); a violation is `population_path_invalid`, not `member_missing`.

**S12 — MEDIUM — no blob cap.** Measured: 64 MiB costs 0.03 s and lands **67,108,864 bytes in the parent heap**
(`capture_output`); the read side is unbounded by contract and by c58. **Fix:** after the type gate `cat-file -s`,
cap at 4 MiB; over-cap → exit 2 (could-not-evaluate) with a named line, never silently "no receipt".

**S13 — MEDIUM — empty `--root` silently evaluates the caller's cwd.** Measured: `git -C ''` exits 0 and reports
the cwd's repository (this seat's own fixture mishap demonstrates the consequence — see the incident note).
**Fix:** reject empty/whitespace `--root` before any git call; require exact `realpath(root) ==
realpath(show-toplevel)`; a subdirectory root exits 2 (measured: `--show-toplevel` prints the repo root for a
subdir, so this is checkable).

**S14 — MEDIUM — non-UTF-8 receipt bytes crash a naive reader.** Measured: `blob.decode()` raises
`UnicodeDecodeError` on `\xff\xfe`; `decode('utf-8','surrogateescape')` works. **Fix:** surrogateescape everywhere
(c58 line 83) and map any decode failure to exit 2, not a traceback.

**S15 — MEDIUM (counter harness) — run the tool as `python3 -I -B` from an empty directory.** Measured: `-B` alone
leaves both hijacks open — a `hashlib.py` on `PYTHONPATH` shadows stdlib, a `json.py` beside the extracted script
shadows via `sys.path[0]`; `-I` blocks both. Extract the tool by `cat-file blob` bytes with a mode gate (a checkout
turns a committed symlink into a live symlink the harness would execute by path). c60 standardises `python3 -B
<path>`; extend it to `-I`.

**S16 — LOW/MEDIUM — exit-code and stdout discipline.** `--selftest`, timeouts, git absent, `TimeoutExpired` and a
truncated walk must all be exit 2 and must **not** print the summary line; print `receipts=… events=… undisclosed=…
met=…` only after a completed walk, or a counter parsing stdout scores a partial walk as clean. `--json` stably
ordered by (path, commit).

**S17 — LOW — `PATH` is the one unscoped channel** (the scrub is prefix-based on `GIT_`): a hostile `PATH`
trojan-horses `git` itself. **Fix:** resolve git once via `shutil.which` and refuse a non-absolute result.

**S18 — LOW — selftest must carry the negative mutants** (`always-clean`, `always-exit-1`, `fixture-sniffing`) and
build fixtures only under `TMPDIR`; the sniffing control forces seeded ids, so no fixture path or commit message may
contain the case id (`L2`, `L7`, …).

Notes:
- `resume_continuity_v1` has no surface in this lane (absent from `contract.md`, `scripts/` and the round-61 tree),
  so that assigned check cannot be run here. Substituted: the plumbing the tool will use leaves **zero** mutation —
  `cat-file`, `log --first-parent` and `rev-list` all exit 0 against a `chmod -R a-w .git` clone with **0** lock
  files created, and the c58 precedent opens nothing for writing.
- Incident (disclosed, repaired): a first fixture attempt used `mktemp -d fx1` without `XXXXXX`; `$D` came back
  empty and one `git -C "" update-index --cacheinfo 160000,…` landed a stray `sub` gitlink in the **fleet** repo
  index. No commit, no worktree change; repaired with `git update-index --force-remove sub`; fleet `git status` is
  clean and HEAD is unchanged (`fe19085`). It is also the live proof of S13.
- Not tested (tool absent): real shell use, real network use, real write calls. `[INFERENCE]` from the contract text
  plus the c58 precedent — freeze three static invariants on the committed blob: no `shell=True`/`os.system`/
  `popen`, no `socket`/`urllib`/`http.client`, no `open(...,'w')`/`Path.write_*`/`tempfile` outside a
  `--selftest`-only branch.

VERDICT: Do not freeze C1 as written — four blocker-class defects are measured before any data exists (S1
`base..revision` makes the real case vacuous or 12-phantom, S2 substring-vs-line span silently blinds the tool to
relabels and breaks L2/L6, S3 R2's `receipts=144` is factually 95 and passes a zero-receipt tool, S4 `extra_member`
fires 480× at base and on the round's own controls), and S8 shows the claim's "no committed check" premise is false
at base; each is fixable by contract-level wording (full-history walk, whole-line span, `members=144 receipts=95
events=12`, round-scoped extra scan) plus committed-bytes disclosures, `--no-replace-objects` and a type/mode gate,
after which the execution surface itself is sound (no shell, no network, no writes, no path escape, read-only
plumbing verified).
