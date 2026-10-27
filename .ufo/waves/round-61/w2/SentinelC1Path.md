# SentinelC1Path

Security review of claim C1's committed instruments at lane HEAD `f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f`
(jj working copy `67c538f7c3ac`): `scripts/receipt_lineage.py` (1040 lines, committed) and its counter
`.ufo/waves/round-61/c61_lineage_cases.py`. Contract + amendments A1–A5 read end-to-end first; predicates
unchanged; no lane file, jj/index or git state was mutated. All probes are benign, built under
`/fast/scratch/hyaku/kake-r61/SentinelC1Path/` (`git init` per fixture, toplevel asserted, selftest identity
only), and the scratch tree is deleted on exit. No tool installed.

Axes attacked: (1) contract fidelity of the "committed bytes only" guarantee, (2) argument/path/environment
injection, (3) resource bounds on hostile history, (4) evasion of the watch's own event classes.

---

## F1 — CRITICAL — committed-only guarantee is broken for the disclosures registry; all findings are forgeable by uncommitted state

**Exploit path.** A seat, CI step or any process with worktree write access creates or edits the *untracked*
file `.ufo/waves/round-61/../.ufo/receipt-disclosures.json` (default `DEFAULT_DISCLOSURES`) without committing.
`load_disclosures` (`scripts/receipt_lineage.py:378-398`) first tries `git cat-file blob <rev>:<path>`; when that
fails it silently falls through to `open(os.path.join(root, given))` — the **worktree**. Every receipt event is
then matched against that unaudited file and reported `disclosed`.

**Evidence (probes A/B, base run).**
- Fixture: one receipt, undisclosed `revision:` rewrite, then an *uncommitted* worktree registry naming
  (path, commit). `git status` shows `?? .ufo/receipt-disclosures.json`. Tool with no arguments:
  `receipts=1 events=1 undisclosed=0 met=True`, **exit 0** (expected per contract/A3: 1 finding, exit 1).
- Fixture B: registry committed *after* the measured commit; measuring the rewrite commit still reports
  `undisclosed=0 met=True`, exit 0 — `git cat-file blob <measured>:<reg>` returns 128 (absent), so the later
  commit's bytes are read from the worktree. A result at revision R is therefore a function of today's
  worktree, not of R.
- Real lane, measured at base `9f07731a` (registry genuinely absent there — `git cat-file -e` says "exists on
  disk, but not in 9f07731a"):
  - default path → `receipts=95 events=12 undisclosed=0 met=True`, exit **0**
  - `--disclosures <empty committed-equivalent registry>` → the 12 events as
    `undisclosed_rewrite`/`undisclosed_pending_filled`, `undisclosed=12 met=False`, exit **1**
  A1 states the base run must print `undisclosed=12`, exit 1. The implementation prints `met=True`, exit 0.
- `strace -f -e trace=openat` on a fixture: the tool opens
  `<root>/.ufo/receipt-disclosures.json` (worktree) and **never** opens the worktree control file — the
  carve-out is exactly one file.
- Positive control: when the registry *is* committed at the measured revision, the worktree copy is not opened
  and a worktree sabotage (`{"entries":[]}` uncommitted) is ignored. The defect is the fallback only.

**Impact.** The claim's own property ("undisclosed receipt rewrites become detectable in-lane") is neutralised
without a commit, without a receipt and without leaving tracked state; the base negative control (A1) collapses
to the after-state (`met=True` at both ends); results are non-reproducible across machines/checkouts; a
counter that asserts `undisclosed==0` cannot distinguish honest disclosure from an untracked forgery. This is a
provenance defect, not only a hardening nit.

**Smallest remediation.** Delete the filesystem fallback (`scripts/receipt_lineage.py:386-396`): committed
`<rev>:<path>` or nothing; missing default → zero entries, missing explicitly named path → exit 2 (the latter
already works: `--disclosures /nonexistent/x.json` → exit 2).

## F2 — HIGH — the C1 counter does not exist; the 18-case predicate and the frozen 144-member population are unenforced

**Evidence.**
- `.ufo/waves/round-61/c61_lineage_cases.py` is absent from the worktree, the index, `HEAD`, and every ref
  (`git cat-file -e HEAD:…` → "does not exist in 'HEAD'"; `git log --all -- <path>` → empty; `find` over the
  fleet tree → empty). The contract names it once (`contract.md`, Claim C1) and describes 16 fixture cases plus
  R1/R2, `member_changed`, `extra_member`, `member_missing` as implemented behaviour. Nothing implements them.
- The w1 seat that owned it says so: `w1/ExecC1Counter.md` — "Not run. The counter implementation is
  incomplete and must not be used or frozen … Do not treat the current file as a passing deliverable." No
  `ExecC1Counter.files/` evidence directory exists.
- The tool re-derives the population dynamically and cannot enforce the frozen list: at HEAD it reports
  `population=146`, frozen list is 144; the two extras are
  `.ufo/waves/round-61/controls/census-before.txt` and `.ufo/waves/round-61/controls/population-144.txt`
  (A2 excludes round-61 apparatus from `extra_member`, but no code carries that bound). At base the tool
  reports `population=144`. `member_missing` has no implementation anywhere, which is what makes F3's
  delete-at-revision evasion silent.
- Manual run of the tool at HEAD does match A1's pinned shape: `receipts=95 events=12 undisclosed=0 met=True`,
  exit 0, 12 disclosed events, 0 findings, 0 skipped. `--selftest` passes 68/68 in 1.6 s. So the tool's own
  claims hold; the **scored** `cases_passed == 18 of 18` claim has no instrument.

**Impact.** Any w2 or L1 line reporting C1 `met` (18/18) is unsupported; `R2` is reproducible by hand but not
scored, `R1`/do-nothing is broken by F1, and the population-freeze terms have no enforcement. This is fabricated
readiness at the contract level.

**Smallest remediation.** L1 writes and commits the counter to the frozen contract text (or records C1 as
unevaluable for this round); before any counter run, F1 must be fixed or the counter's base control will pass
for the wrong reason.

## F3 — MEDIUM — deletions are not events (A3 violated); a receipt can be removed or replaced wholesale with zero findings

**Evidence.** `segments_of`/`path_events` (`:313-332`, `:411-434`) only compare versions inside a present
segment; a `D` closes the segment and emits nothing. A3 binds "a path absent in a later tree is a deletion
event with empty result span".
- `git rm` of a receipt in the measured commit: `receipts=0 events=0 undisclosed=0 met=True`, exit 0 — the path
  is gone from the revision, so the tool's dynamic population no longer contains it.
- Clean receipt → delete → re-add with wholly different results (`met=True`→`met=False`, `EXIT=0`→`EXIT=1`,
  `findings=9`): `receipts=1 events=0 undisclosed=0 met=True`, exit 0.

**Impact.** A receipt can be replaced by delete+re-add, or removed at the measured revision, with the watch
silent; only the missing counter's `member_missing` would see the second case. The tool's own L20 test asserts
this behaviour as correct, so it is a design reading, not an accident — but it contradicts the binding A3 text.

**Smallest remediation.** Emit `rewrite` (or a named `deleted`) event at the deleting commit when the prior
span is non-empty; keep re-add as a fresh segment.

## F4 — MEDIUM — giant blobs: unbounded memory, all history versions held at once

**Evidence.** `read_blobs` (`:267-296`) sends every changed blob sha to one `git cat-file --batch`, buffers the
whole stdout, and keeps every version in one dict; `walk_changes` buffers all of `git log --raw`. No size cap,
no streaming, no per-commit release. Measured on fixtures via `getrusage(RUSAGE_CHILDREN).ru_maxrss`:
- one 64 MiB receipt body → 215 MB RSS;
- three ~64 MiB versions → 466 MB RSS (all versions concurrently, ~2.4× total bytes).

**Impact.** A committed multi-hundred-MB control file (or a corrupted capture fixture) makes the counter OOM or
thrash; because the counter is meant to run inside gate-built fixture repos in CI, the failure is a DoS on the
measurement, not on the lane. No cap or named skip exists.

**Smallest remediation.** Stream `cat-file --batch` and drop each blob after its comparison; optionally skip
(and name) blobs above a fixed size.

## F5 — LOW — disclosures path resolution escapes the repository root and follows symlinks

**Evidence.** The explicit-path branch (`:386-396`) does `os.path.join(root, given)` with no containment check
and no `O_NOFOLLOW`:
- `--disclosures ../outside-disclosures.json` (a file in the scratch parent) is accepted and suppresses the
  event: exit 0, `undisclosed=0`.
- the default path can be a worktree symlink to a file outside the root: exit 0, `undisclosed=0`.
- absolute paths are accepted by design (same as above, no escape needed).

**Impact.** Read of an arbitrary local JSON file as the disclosure registry, and honouring it; caller-controlled,
same-user, read-only. Combined with F1 it widens the trust boundary from "committed at `<rev>`" to "any readable
file". Also: a `{"entries":[]}` registry with no `schema` key is accepted (schema is optional, `:355-357`),
while the contract names the schema.

**Smallest remediation.** F1's removal eliminates this surface; if the fallback is kept, `realpath` containment
plus `O_NOFOLLOW` and a required `schema`.

## F6 — LOW — output-line injection through committed filenames

**Evidence.** Plain output is `f"{kind} {path} {commit}"` with no escaping (`render`, `:504-512`). A committed
population path containing a newline (`.ufo/waves/round-50/controls/a\nb.txt`, valid on Linux and in git) yields
stdout:

```
undisclosed_rewrite .ufo/waves/round-50/controls/a\nb.txt 221c8e88…\nreceipts=1 events=1 undisclosed=1 met=False
```

i.e. one event prints as two output lines. The summary is appended last, so a counter that takes the **last**
`receipts=` line is safe; one that counts `undisclosed_` lines, or unions lines across runs, can be steered.
`--json` is safe (`json.dumps` escapes).

**Smallest remediation.** Git-style quote paths in plain output, or refuse/flag control characters in a
population path as a named finding.

## F7 — LOW — internal failures map to exit 1 (not met) instead of exit 2 (unevaluable)

**Evidence.** `git()` (`:131-135`) lets `subprocess.TimeoutExpired`/`OSError`/`ValueError` escape;
`population`, `walk_changes`, `read_blobs` wrap only the non-zero-rc case. A git wrapper that returns a
malformed `cat-file --batch` header gives:

```
size = int(header[2])
ValueError: invalid literal for int() with base 10: 'notanumber'   (exit 1)
```

A 300 s git timeout behaves the same way by inspection. The kill rule reserves 2 for "could not evaluate"; a
crash reads as "findings / not met" and a `cases_passed` measurement would score it as a legitimate failure.

**Smallest remediation.** Wrap `evaluate` in `except (OSError, subprocess.SubprocessError, ValueError,
RecursionError)` → exit 2.

## F8 — LOW — `phantom_disclosure` scope is wider than A3

**Evidence.** Every unmatched registry entry becomes a finding, with no population-membership test
(`:478-482`). A registry entry for `.ufo/waves/round-5/capture/response.json` (outside the population) gives
`phantom_disclosure … ` and exit 1 while `met=True`. A3 bounds phantoms to entries naming a frozen population
path. Practical effect: a legitimate disclosure for a non-population artefact would fail the run.

**Impact.** Contract deviation in the fail direction (false positive), not a bypass.

**Smallest remediation.** Restrict phantom reporting to paths in the revision's population (or the frozen list,
once F2 exists).

---

## Verified clean (no finding)

- **Subprocess usage**: every call is argv-list form (`:132`, `:526`, `:537`, `:565`); no `shell=True`, no
  `os.system`/`eval`/`pickle`/network imports anywhere in the file.
- **Argument injection**: `--revision` rejects empty and leading-dash values and passes
  `--end-of-options` (`:151-158`); `--literal-pathspecs` is global (`:132`); `--revision` values
  `--output=/tmp/…`, `-x`, `HEAD;touch …`, `HEAD$(…)`, `:.ufo` all exit 64 or 2, no side effect (no marker
  file written).
- **Environment**: inherited `GIT_*` are scrubbed (`:123-129`). A PATH wrapper recorded every `GIT_*` git saw
  under poisoning (`GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_COUNT/KEY_0/VALUE_0`): only
  `GIT_OPTIONAL_LOCKS=0` and `GIT_TERMINAL_PROMPT=0`. Residual: `PATH` itself can select a different `git`
  binary, and `HOME`/global gitconfig remain readable — neither drives these plumbing commands.
- **Symlinks / submodules in the population**: `ls-tree` mode gate (`:100`, `:196`) skips mode 120000/160000
  with a named stderr note; a committed symlink yields `receipts=0` plus
  `note: non-blob population path (mode 120000) …`.
- **Committed-only for population/history**: `ls-tree`/`log --raw`/`cat-file` only; `strace` shows no worktree
  control file is opened, and an uncommitted edit to a receipt does not change the result.
- **No writes**: fixture tree snapshot before/after a run is identical; `-B` avoids `__pycache__`.
- **Failure mapping when git itself fails**: a wrapper failing `git log` gives exit 2 with
  `receipt_lineage: the first-parent history could not be walked` (only the timeout/parse paths in F7 escape).
- **Real-lane shape**: at HEAD `population=146 receipts=95 events=12 undisclosed=0 met=True`, exit 0, findings 0,
  skipped 0 — matches A1's pin; `--selftest` 68/68.

## Overlap note for the integrator

F3 (deletion) is also in `CriticC1Deletion`'s scope and F2 in `ReviewerC1Counter`'s; this report's F1 (worktree
disclosures), F4 (memory), F5 (path/symlink), F6 (line injection), F7 (exit mapping) and F8 (phantom scope) are
the sentinel-only surfaces, and F1 is the reason the base control cannot be scored as written.

VERDICT: C1 is not safely frozen — the tool's disclosed/undisclosed result is controlled by uncommitted worktree bytes (base `9f07731a` prints `met=True`, exit 0 instead of A1's `undisclosed=12`, exit 1), the frozen counter `.ufo/waves/round-61/c61_lineage_cases.py` does not exist in any ref so `cases_passed == 18 of 18` is unsupported, and deletions plus giant blobs are unhandled; argument, shell and environment hygiene are otherwise clean.
