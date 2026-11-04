# SentinelScope — round 75 / w1 — scope, disclosure, scratch and failure-mode audit

Seat: sentinel (leaf, no dispatch). Read-only on the lane. Measured 2026-11-03 21:01–21:23 -03:00.
Lane HEAD at open of this audit: `ab939c46`; at close: `4e3fc159` (21:15:56) — the L1 landed the
after-state during the audit (`f1fc5d0a` instruments, rows, receipt; `4e3fc159` receipt carrier).
Base revision `c9c5e484`; `SKILL.md` blob `4b3d31cc` is identical at base, freeze, wave and
amendments 1–3, so none of the C1/C2 measured bytes changed under the amendments.

Receipts: `w1/SentinelScope/receipts.txt` (commands and verbatim output, scratch/lane roots
normalised to `<scratch>` / `<lane>` when copied; §16 holds the landed-tip runs). Nothing was
written outside that directory and `/fast/scratch/hyaku/kake-r75/SentinelScope/`; the scratch tree
was deleted before this report was yielded (§6).

**Verdict in one paragraph.** No credential, token, session body or secret is present in the round's
committed or uncommitted wave artifacts. The disclosure that exists is host-absolute paths — at the
landed tip `4e3fc159`, **66** `/home/<user>` occurrences and **44** `/fast/` occurrences across 16
committed files under `round-75/` — plus three committed `TMPDIR=/fast/…` value assignments
(`w1/ScoutRegistry.receipts.txt:17,20,26`) and a `/tmp` token list that is quoted lane history and
remains uncommitted. No wave seat wrote outside `.ufo/waves/round-75/`; the production-file writes
are the L1's landing. The C2 receipt itself is clean (repo-relative paths, digests, byte counts, host
class). At the landed tip both instruments re-derive their targets when I run them independently:
C1 `mismatches=0 met=true` (exit 0) and C2 `population=18 bound=18 met=true` (exit 0), and the
landed counter re-checks out `--revision` in a reused `--work` (the v0 stale-tree defect is fixed).
What remains is evidence-chain identity, not the claims: the base control was produced by the
pre-landing counter (`43538343`), so its line lacks the amendment-1 `missing_frozen` field; the
receipt binds the population but not the checker; and the committed control receipts carry scratch
paths and `cwd=` banners (§4, §5).

---

## 1. Disclosure audit — round artifacts under `.ufo/waves/round-75/`

Scope measured: every file tracked at HEAD under `.ufo/waves/round-75/` (`git grep` over the tree at
`ab939c46` and again at the landed tip `4e3fc159`) plus every uncommitted/untracked file in that
tree at 21:14. Patterns: `ghp_[A-Za-z0-9]{20,}`,
`github_pat_`, `AKIA[0-9A-Z]{16}`, `sk-[A-Za-z0-9]{20,}`, `-----BEGIN … PRIVATE KEY`,
`Bearer <token>`, `password[=:]`, plus manual reads of the dispatch/spec/registry, the controls, the
C2 receipt and its surrounding receipts.

**Zero hits for credential values, tokens, keys, cookies, session bodies, or agent transcripts.**

| # | Class | Where | Observed | Severity / disposition |
|---|---|---|---|---|
| 1 | Host-absolute user paths | At `4e3fc159`: `w1-dispatch.json`, `w1-spec.json`, `w1/swarm-registry.json`, `contract.md`, `w1/ScoutSources.md`, `w1/ScribeKnowledge.md`, `w1/ConnectorOverlap.md`, `w1/ScoutSources/fetch-intoto.txt`, `w1/ScoutRegistry.receipts.txt`, the seven committed `w1/ExecC2Receipts/*` receipts — **66 `/home/<user>` and 44 `/fast/` occurrences in 16 files** (58 `/home` in the three dispatch files alone) | Committed by the L1's landing. All are the lane path `/home/<user>/Projects/shokunin/kake-shokunin`, the fleet root, or the scratch root `/fast/scratch/hyaku/kake-r75/…` | **Low** — pre-existing lane convention: 5,939 tracked files in the repo already carry `/home/<user>`; these are new instances, not a new class. Note for the L1: the dispatch trio is the bulk; the seven C2 controls each carry a `(tool sha256=…; cwd=/fast/…)` banner. |
| 2 | Environment **values** serialised | **Committed:** `w1/ScoutRegistry.receipts.txt:17,20,26` — `TMPDIR=/fast/scratch/hyaku/kake-r75/ScoutRegistry/tmp …`. **Uncommitted:** `w1/ExecC2Receipts/receipt.sha256.txt:4` — `TMPDIR=/fast/…/work/tmp HOME=/fast/…/work/home` inside a copied `$ (cd …) …` line | The commitment happened with the L1's landing; the `receipt.sha256.txt` pair is still only in the worktree | **Low–medium** — the values are scratch-scoped, not the operator's HOME, so no secret leaks, but the committed `TMPDIR=` value is the exact pattern this item asks to flag. Fix: write `TMPDIR=<scratch>/tmp` (symbolic) in receipts. |
| 3 | `/tmp` paths captured as evidence | `w1/ExecHarm/append-absent-home-token-c70.txt:6–12` | `/tmp/kake-r18`, `/tmp/kake-r17`, `/tmp/kake-r15`, `/tmp/kake-r14`, `/tmp/kake-r13`, `/tmp/kake-r12`, `/tmp/kake-r11`, `/tmp/kake-r10` | **Informational** — the tokens are quoted *lane history* that the c70 pointer audit annotated (the capture is the finding, not the seat's scratch). No live `/tmp` capture: `git grep '/tmp/'` over committed round-75 blobs = 0 hits, and no wave artifact records a seat scratch path under `/tmp`. |
| 4 | Scratch path cited as a comparison target that will not exist | `w1/ScoutSources/fetch-intoto.txt:9` | `cbe684a1…  /fast/scratch/hyaku/kake-r75/ScoutSources-6/refetch.md` — the seat deleted that tree; the retained bytes are `w1/ScoutSources/intoto-statement.md` | **Low** — cite the in-report path; the digest (`cbe684a1…`, 2,492 B) is independently correct (I re-hashed the retained file and HEAD's `l1` copy: identical). |
| 5 | Absolute command lines in receipts | `w1/ScoutSources/verify-output.txt:1–2`, `w1/ScoutSources/integrity.txt:1` (`lane=/home/…`), `w1/ScribeKnowledge.md:3,396`, `w1/ConnectorOverlap.md:29,56` | The lane path, the scratch root, and the fleet root `/home/<user>/Projects/shokunin/` ("twenty sibling checkouts") | **Low** — same class as #1. `ConnectorOverlap.md:56` cites a sibling lane relatively (`tameshi-shokunin/corpus/knowledge/…:1`); the lane name/filename is the only sibling-lane content exposed. |
| 6 | Internal process text in committed evidence | `w1-dispatch.json` (`context`, `taskCall`, `note`), `w1-spec.json` (`context`), `w1/swarm-registry.json` | The full seat briefs and the host-guard text are embedded and committed | **Informational / operator call** — prompts, not transcripts; no session body. If the repo is public these directives become public process text. |

Not found, and worth stating because the item names them: no `.netrc`, no `Authorization:` header, no
cookie, no SSH material, no environment *dump*, no `os.environ` serialisation (the only `environ`
reference is the counter's own `env={**os.environ, …}` at `c75_row_truth.py:111`, code not output),
and no agent conversation history.

## 2. Scope audit — who wrote what

### 2.1 Lane working tree (`git status --porcelain`, read-only)

Two snapshots matter, because the L1 landed the after-state mid-audit.

**At 21:14** (`7348d37e`), status had 50 entries:

- **Wave-dir only, seat output (expected):** `w1/*.md`, `w1/*/` (ScoutSources, ExecHarm,
  ExecC2Receipts, ExecC2Tool, ExecC1Counter, ReviewerC1-heldout, ReviewerC2, ScribeKnowledge,
  SentinelScope) and `w1.ready.dispatched` (L1 dispatcher marker, 21:01, untracked).
- **Wave-dir deliverable edits after the L1's snapshot commit:** `M` on
  `w1/ExecC1Counter/c75_row_truth.py`, `w1/ExecC2Tool/instrument_receipts.py` and six
  `w1/ExecC2Receipts/*` receipts — seats revising their own files, in scope.
- **Production files, outside every seat's scope:** `M PROVINCE.md`, `M corpus/QUALITY.md`,
  `M corpus/README.md`, `M corpus/SOURCES.md`, `?? corpus/knowledge/instrument-receipts.md`
  (all 21:10). These are the L1's after-state landing; no wave seat's item claims them. Attribution
  is `[INFERENCE]` from the role rule that the L1 is the only lane writer — git cannot prove
  authorship from a worktree.
- **Ignored in-lane writes, predating the round:** `.ufo/waves/round-66/__pycache__/c66_gate_status_hostportable.cpython-314.pyc` (19:42) and
  `.ufo/waves/round-72/__pycache__/c72_tmp_v2.cpython-314.pyc` (19:40). Bytecode from an *import*
  (not `--main`) run without `-B`, i.e. an in-lane write outside `round-75/` before the round opened.
  Not committed, not evidence. Recommend the L1 remove those two directories.
- No world-writable or setuid file under `round-75/` (`find -perm -o+w -o -perm -4000` → none).

**At 21:22** (`4e3fc159`) the after-state has landed (`f1fc5d0a`: counter, binder, superseding rows,
knowledge entry, criterion, sources; `4e3fc159`: the receipt at the instrument revision). Status is
82 entries: 69 untracked, 10 modified, 3 deleted, all under the wave dir except the L1's in-flight
landing (`M LOG.md`, `M SCORECARD.md`, `M SKILL.md`, `?? corpus/lessons/round-75.md`, and the two
pending `controls/after-*` receipts). Seats were still editing their own `w1/ExecC2Receipts/*`
controls (`M`/`D` against HEAD) when I closed.

**No file outside `.ufo/waves/round-75/` was written by a wave seat.** (The production files above
are L1 writes; the pycache is older than the round.)

### 2.2 The revision moved under the seats

Reflog- and log-verified HEAD sequence during the wave:
`c9c5e484` (base) → `88f2e05f` (freeze 20:58:33) → `ab939c46` (wave 21:00:41) → `9a9c4a6f`
(amendment 1, 21:03:41) → `d599c8be` (amendment 2) → `7348d37e` (amendment 3) → `f1fc5d0a`
(after-state instruments/rows/entry) → `4e3fc159` (after-state receipt, 21:15:56). Each is an
`export from jj` by `kake-shokunin <kake@shokunin.local>`. `SKILL.md` is byte-identical from base
through amendment 3 (`4b3d31cc…`); it changes only at `f1fc5d0a`, where the Round 75 rows land. A
seat using the default `--revision master` before the landing measured different commit ids at
different times; every receipt must pin the sha it measured (the landed after receipts do).

Also during the wave the lane's **git object store changed**: 772 loose objects newer than round
open (sampled 355 blobs / 45 trees, no seat-authored commits) and both pack files re-written at
21:02:20; `.jj/repo/op_store` and `op_links` changed 21:00–21:03. This is consistent with the L1's
jj working-copy export (`[INFERENCE]`), not with any read-only git command a seat was permitted to
run. It matters because `.git` is not read-only even when the worktree is.

**Self-report:** the lane's `.git/index` mtime is 21:03:43, which coincides with (and may have been
caused by) my read-only `git status --porcelain`; jj's export writes the index too, so I do not claim
exclusive attribution. No tracked content changed, nothing staged; the untracked set is unchanged by
me.

### 2.3 Scratch (`/fast/scratch/hyaku/kake-r75/`, read-only listing)

Total 21,409 MB in 9 trees at 21:13 (`du -sm`): `CriticPredicates` 7.5 GB, `l1` 4.8 GB,
`ScribeRows` 2.5 GB, `SentinelScope` 2.5 GB (mine), `ExecHarm` 1.9 GB, `ExecC2Receipts` 0.9 GB,
`MutationTesterC2` 0.7 GB, `ExecC1Counter` 0.3 GB, `ExecC2Tool` 0.3 GB. At 21:26, after several seats
finished, the root held **6 trees / 20,703 MB** (`l1` 8.0 GB, `SentinelScope` 3.8 GB mine,
`ExecC1Counter` 3.4 GB, `ExecC2Receipts` 2.5 GB, `CriticPredicates2` 1.6 GB, `MutationTesterC2`
1.4 GB) — cleanup is in flight, and each running seat must finish it. `/fast` is not `/tmp`, so
the 50 MB `/tmp` rule is not engaged. `ScoutSources-6` was verified removed at 21:05;
`ScribeKnowledge`, `ConnectorOverlap`, `ScoutRegistry`, `ScribeRows`, `ExecHarm`, `ExecC2Tool` and
`ReviewerC2` trees are gone from the root by 21:26. My tree is deleted (§6).

Fixture repos: every `.git/config` under the scratch root (full-depth scan, 20 configs) points at the
kake lane or at a scratch-internal clone. **Zero configs name another lane or the fleet root**, and
no fixture repo's `core.worktree`/symlink escapes its own tree (symlink scan: none). One deviation
from the scratch rule: `l1/lane-clone` is a **full clone** from
`https://github.com/VeigaPunk/kake-shokunin.git` (34.7 MB pack, no `objects/info/alternates`, a `.jj`
directory inside) rather than `clone --shared`/`worktree`/`archive`. L1-side, low severity, not used
as wave evidence.

Fleet root (`git -C /home/<user>/Projects/shokunin status`, read-only): `M .scratch/*`, `?? after`,
`?? .scratch/run15-kernel.py` — fleet-run state, outside this lane's seats and not touched.

## 3. The C2 receipt — does it leak build context?

`w1/ExecC2Receipts/instrument-receipts.json` (the delivered, pre-landing copy) is 3,397 B, sha256
`b37d1b09415e2e63816c701324cf53d86b5e8dcc150130609583dcc836d81a69`. I re-derived it independently
at `c9c5e484` with the wave writer (latest run: tool sha `162dd685…`; earlier runs with the 21:07
build produced the same bytes): **byte-identical** (same sha, same length), which is a real
cross-check of the writer, not a copy.

The **landed** receipt at `4e3fc159` (`corpus/knowledge/instrument-receipts.json`, blob 98ffca2a) is
3,793 B, sha256 `f3128628d928ae1977b79e9a1005d74a6e4cf97d8730399e4c3aa44a9b8ecc9b`, 18 files, declared
`revision=f1fc5d0a` (the instrument commit), `host=linux-x86_64`. It contains **zero** `/home`,
`/fast`, `/tmp` or hostname strings (grep = 0).

Fields, complete (both copies): `schema` (`instrument-receipts/v1`), `revision` (40-hex commit),
`date`, `host` (`linux-x86_64`), `files[N]` each `{path, sha256, bytes, selftest_mode}` (N=16 at
base, 18 at the tip). The paths are all repo-relative; the host is a **class**
(`sys.platform`-`platform.machine()`, no hostname, no kernel build, no distro); there is no absolute
path, no `/tmp`, no environment value, no username, no network endpoint, no tool digest and no build
metadata. **Verdict: the receipt itself discloses nothing beyond repo state and a two-token host
class.**

The leaks are *around* it, and they are mechanical:
- `receipt.sha256.txt:4` — `TMPDIR=`/`HOME=` values (§1 #2) and the absolute tool path.
- Every control receipt opens with `$ (cd /fast/scratch/…) TMPDIR=… HOME=…` and a
  `(tool sha256=…; cwd=/fast/scratch/…)` banner (`after-c2-receipts.txt:2`,
  `check-at-freeze.txt:2`, `committed-edit.txt:2`, `worktree-uncommitted-edit.txt:2`,
  `controls/ctl-uncommitted-strict.txt:2`, …).
- The C2 tool's `--selftest` prints the absolute fixture directory
  (`selftest: fixtures under /fast/scratch/hyaku/kake-r75/<seat>/est3/fx-17la6a4q`). Any committed
  capability receipt that copies the run output will carry the seat name and host layout. Fix in the
  tool: print it relative to `--work`.

**Provenance of the receipt (more important than its content).** Four tool sha256s are in play:

| Where | sha256 | State |
|---|---|---|
| `HEAD:.ufo/waves/round-75/w1/ExecC2Tool/instrument_receipts.py` | `169e2136…` | pre-amendment: prefers the worktree receipt, `--require-committed` opt-in |
| `w1/ExecC2Tool/instrument_receipts.py` (worktree, 21:10–21:12) | `a2005c6a…` | amendment-3-conformant: committed-only receipt read, declared-revision validation, no worktree fallback |
| same path (worktree, 21:21, the latest I measured) | `162dd685…` | same behaviour, re-confirmed (§4.3); the file is still being edited |
| cited by the seat's receipts (`receipt.sha256.txt:1`, `after-c2-receipts.txt:2`, `controls/*.txt:2`) | `62b795ea…` | the seat's scratch "canonical" copy; not delivered, not committed |

The L1 landed `162dd685…` at `scripts/instrument_receipts.py` (48,868 B at `4e3fc159`) and the new
`controls/after-c2-receipts.txt` records `tool_sha256=162dd685… bytes=48868`,
`receipt_sha256=f3128628… bytes=3793`, `source=committed`, `bound=18`, `met=true`, exit 0 — so the
*evidence* now pins the checker even though the receipt schema itself does not. The superseded
`w1/ExecC2Receipts/after-c2-receipts.txt` (untracked at my close, produced by `62b795ea` before
amendment 3) still shows `committed=absent`, `met=true` and must not be landed; its `receipt.sha256.txt`
companion remains the only file with `HOME=` values (§1 #2).

## 4. Counter failure modes — measured, not assumed

Every row below is a command I ran (receipts §1–§16). "Required" is the seat item's requirement.

### 4.1 Pre-landing C1 counter, blob `43538343…` (the counter that produced `controls/base-c1-row-truth.txt`; the path now holds the hardened counter `0699a672…` at `HEAD`)

| Test | Observed | Required | Verdict |
|---|---|---|---|
| missing `--work` | `64 usage: --work <dir> is required`, exit **64** | 64 | pass |
| unresolvable revision (`deadbeef`) | `2 unevaluable: cannot resolve revision…`, exit **2** | 2 | pass |
| revision resolves but `SKILL.md` absent | stderr `2 unevaluable: cannot read SKILL.md…`, **exit 1**, no verdict line | 2 | **fail** — `raise SystemExit(f'2 unevaluable: …')` (`c75_row_truth.py:53`) exits 1: a git read failure is indistinguishable from "claim not met" |
| unreadable `--base` | same: stderr says unevaluable, **exit 1** | 2 | **fail** (same line) |
| `--work` reused across revisions | output line claims `revision=ab939c46`, but `work/tree` stayed at `c9c5e484` and every self-test ran base bytes | stale tree detected or refused | **fail** — `if not os.path.isdir(tree/.git)` skips the checkout (`:229`) and never compares the tree's HEAD to `--revision` |
| empty registry, no `--base` | `rows=0 files=0 mismatches=0 append_only=true met=true`, exit **0** | not met | **fail (vacuous)** — `append_only` defaults true when `--base` is omitted (`:222` + `:363` in the hardened copy), so an empty `SKILL.md` is "met" |
| read-only `--root` | correct verdict, exit 1, **zero writes** (`find -newer` empty) | no writes | pass |
| recorded-command timeout | none (`subprocess.run` without `timeout`) | — | risk: a hanging registry cell hangs the measurement |

### 4.2 Hardened C1 counter delivered this wave (`w1/ExecC1Counter/c75_row_truth.py`, `90a4cdd5…` then `d982cc5d…`)

| Test | Observed | Verdict |
|---|---|---|
| missing `--work` | exit 64 | pass |
| unresolvable revision | exit **2** | pass |
| `SKILL.md` absent at a valid revision | exit **2** | pass — the `SystemExit(str)` defect is fixed |
| empty registry | `met=false missing_frozen=16`, exit 1 | pass — amendment-1 floor enforced |
| read-only `--root` | correct verdict, zero writes | pass |
| `--selftest` | 19/19 at `90a4cdd5`; **26/26** at `d982cc5d`, exit 0 | pass |
| base control reproduced | `rows=28 live=16 files=16 mismatches=2 classes=E1 E3 append_only=true met=false missing_frozen=0`, exit 1 | pass, semantically identical to `controls/base-c1-row-truth.txt` (the control line has no `missing_frozen`, see §5 #4) |
| `--base` still optional | `append_only=true` printed when omitted | **residual** — recommend 64 or `append_only=unchecked`; the frozen command always passes it |

### 4.3 C2 tool

| Test | Tool sha | Observed | Verdict |
|---|---|---|---|
| `--write` without `--date` | 8fbbb23b | exit 64 | pass |
| `--selftest` without `--work` | a2005c6a | exit 64 | pass |
| unresolvable revision | a2005c6a | exit 2 | pass |
| non-git root / repo subdirectory as root | a2005c6a, 162dd685 | exit 2 with an explicit reason | pass |
| `--check` on `chmod -R a-w` root | a2005c6a, 162dd685 | exit 1, zero writes | pass — read-only as required |
| receipt present only in the working tree | 8fbbb23b (pre-amendment) | `met=true`, exit 0, `receipt: worktree committed=absent` | **fail**, closed by amendment 3; a2005c6a: `bound=0 mismatches=16 met=false`; 162dd685: `source=uncommitted worktree=only-worktree`, red |
| good worktree receipt masking a fabricated **committed** receipt | 8fbbb23b | `met=true`, exit 0, `committed=differs` | **fail** (the sharp form of the same defect); a2005c6a and 162dd685 read committed bytes only and stay red (`bound=0`, `source=committed`) |
| declared revision that does not resolve | a2005c6a | `declared_valid=false`, 16× `receipt_revision_invalid`, `met=false`, exit 1 | pass (amendment 3 A7 implemented) |
| `--selftest` | a2005c6a, 162dd685 | 17/17, exit 0; prints the absolute fixture dir | pass, with the disclosure nit in §3 |

The pre-amendment exploit is worth stating precisely because it was live: with a fabricated receipt
committed at R3 and the correct one written over it in the worktree, `--check` reported
`bound=16 mismatches=0 met=true`, exit 0. The current tool's `source=committed` line and red verdict
on the same state close it. **Amendment 3 is the remediation; the evidence generated before it
(`after-c2-receipts.txt` under tool `62b795ea`, the seat's controls) predates it and is superseded
by the L1's `controls/after-*` receipts.**

### 4.4 Landed tip `4e3fc159` — the instruments measured independently

| Command | Result |
|---|---|
| `python3 -B .ufo/waves/round-75/c75_row_truth.py --root . --revision 4e3fc159 --base c9c5e484 --work <scratch>/tipwork` (counter sha `0699a672`, verified from `git show HEAD:`) | `C1v1 revision=4e3fc159 rows=32 live=20 files=18 mismatches=0 classes=- append_only=true met=true missing_frozen=0`, **exit 0**, 30.4 s |
| same `--work`, `--revision c9c5e484` | `rows=28 live=16 files=16 mismatches=2 … met=false`, exit 1; `work/tree` HEAD moved `4e3fc159 → c9c5e484` — **the stale-work defect is fixed** (unconditional checkout) |
| `python3 -B scripts/instrument_receipts.py --root . --revision 4e3fc159 --check` (tool sha `162dd685`, 48,868 B) | `population=18 bound=18 mismatches=0 met=true`; `receipt: source=committed worktree=identical declared=f1fc5d0a declared_match=false declared_valid=true`; **exit 0** |
| same tool, `--revision f1fc5d0a` (the receipt's declared revision) | `source=uncommitted worktree=only-worktree`, `bound=0 met=false`, exit 1 — the receipt lands at `4e3fc159`, one commit after the instruments; accepted by A7 (ancestor) but worth one sentence in the closure |

These numbers match the L1's own pending receipts (`controls/after-c1-row-truth.txt`,
`controls/after-c2-receipts.txt`) line for line, including `counter_sha256=0699a672…` and
`tool_sha256=162dd685… bytes=48868`. The claims' targets are met at the landed tip as measured by
me; whether they are *admissible* is the reviewer/critic call, not this seat's.

## 5. Residual risk this round's instruments accept

**(a) Instrument identity is now pinned by the landing, but not by the receipt.** `HEAD` carries one
counter (`0699a672…`) and one binder (`162dd685…`), and the after receipt records the binder's sha
and byte count. The receipt *schema* still has no `tool_sha256`, so a third party re-checking the
receipt alone cannot tell which checker admitted it; and the seat's pre-amendment controls
(`62b795ea`) remain in the tree unless the L1 removes them. **(b) The measured revision is
caller-supplied and the tip moved seven times**; the landed after receipts pin `4e3fc159`, but the base
control was produced by the pre-landing counter, so the two lines differ by one field
(`missing_frozen`, added by amendment 1) and a naive line diff will not match even when the verdict
reproduces (I reproduced it semantically, twice). **(c) The C1 counter executes shell commands
recorded in the measured `SKILL.md` with the caller's environment and no sandbox or network
isolation** (the pre-landing counter also had no timeout; the landed one adds a per-command timeout);
nothing leaks by default because only the literal command is retained, but the instrument's blast
radius is the registry's, not zero. **(d) Two of the three C1 controls are not re-derivable from
committed bytes** — `ctl-cheapcontent.txt` (sandbox `83a9bc27`) and `ctl-deletion.txt`
(`afc73a87`) name no retained fixture; I reproduced the do-nothing control twice, and only that one.
**(e) Scratch peaked at ~21 GB** on `/fast`, and `l1/lane-clone` is a full network clone. **(f)
Disclosure is inherited and now partly committed**: at `4e3fc159` the wave tree carries 66
host-absolute paths and 44 `/fast/` occurrences in 16 files, three committed `TMPDIR=/fast/…`
values, and the internal seat briefs; the pre-amendment `receipt.sha256.txt` still holds `HOME=`/`TMPDIR=`
values but is not committed, and the C2 selftest still prints its absolute fixture dir.

**Lane vs operator.** Lane-internal and cheap: remove the two superseded control sets
(`w1/ExecC2Receipts/*` produced under `62b795ea`, including `receipt.sha256.txt`'s `HOME=` line) or
mark them superseded; require `--base` (or print `append_only=unchecked`); remove the two
round-66/72 `__pycache__` directories; print the C2 selftest fixture directory relative to `--work`;
symbolise `TMPDIR=`/`HOME=` in receipts; and note in the closure that the receipt is declared at
`f1fc5d0a` while the carrier is `4e3fc159` (A7 permits it, a reader may not expect it). Operator
(L0) decisions: whether host-absolute paths and the host-guard/seat-brief text may be committed to
this repository at all (it is public-facing); whether ~21 GB of scratch on `/fast` and one full
network clone are acceptable operating cost; and whether the corpus wants receipt→checker binding
(a `tool_sha256` field) — that changes the receipt schema for every lane, so it is not kake's call.
One consistency item belongs to the L1's closure rather than to L0: amendment 1 says "the counter
therefore prints `missing_frozen`", which was untrue at `9a9c4a6f` (only the pre-landing counter was
committed there, and it has zero `missing_frozen` hits and rejects `--population` with exit 2); it
became true when the hardened counter landed (`f1fc5d0a`). The contract's printed output line was not
amended to match, so code, amendment and contract carry the same line in two shapes — the A5 class.

## 6. Method, limits, cleanup

Commands were read-only git (`show`, `rev-parse`, `status`, `ls-tree`, `cat-file`, `log`, `grep`,
`diff`), `sha256sum`, `find`, `du`, and the counters/tools run with `--work` inside
`/fast/scratch/hyaku/kake-r75/SentinelScope/` (clones made with `git clone --shared`, fixture repos
`git init` with `rev-parse --show-toplevel` asserted before every commit). No mutating git/jj command
ran in the lane; my only lane writes are this report and `w1/SentinelScope/receipts.txt`.

Limits: seats were still writing while I measured, so §2.1 and the tool shas are a snapshot at
21:14–21:20 and will drift; the two 21:10 receipts I call invalid under A6 were produced before
amendment 3 and may be regenerated by their owner after this report. I did not re-run the full
16-self-test measurement on the *successor* tool versions after `d982cc5d`/`a2005c6a`; §4.2's base
reproduction and §4.3's C2 rows were run on the shas named, and the `--population`/`missing_frozen`
and committed-read behaviours were re-run after each change I detected.

Cleanup: `rm -rf /fast/scratch/hyaku/kake-r75/SentinelScope` executed before yield; no tree, clone or
fixture of mine remains under the scratch root (verified by re-listing the root).
