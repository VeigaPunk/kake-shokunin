# Sentinel — round 74, wave w1: security and receipt-integrity review (pre-after-state)

Reviewer: `Sentinel` (read-only seat). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Base revision reviewed: `ced2878a1e77f57afb4ee3baebf1021e5130399b`; freeze commit
`b35dd4d7d6a0a633d7c950bf641d3f948e680448` (HEAD at review). Contract:
`.ufo/waves/round-74/contract.md` (sha256 `940e7450fa4d89a865a843a30fa545e7d8aa4ec0550f93bbc4b768cfe1da164e`).
Wave spec: `.ufo/waves/round-74/w1-spec.json` (14 seats). Scratch:
`/fast/scratch/hyaku/kake-r74/Sentinel` (deleted before yield).

Method: read the frozen contract and every seat item, then attack the delivered writers and the
base receipts with read-only probes in a `git clone --shared` of the lane at base. The lane working
tree was never written; the production sidecar was byte-identical to base before and after every
test (sha256 `9ecfdf2b3a1772198ebdf47f521ad28c4f7176c30469a17063da95a035dfba9f`).
No tool was installed or upgraded during this seat.

**Verdict: PASS for execution safety (no seat is asked to write outside its scope and no seat item
runs a mutating git/jj command), with 8 findings (F8 informational). Three of them (F2, F3, F5) can
make a C2 after-state score wrong against the frozen kill rule or the sweep binding; F4 is a
frozen-control-integrity defect; F1, F6 and F7 are guards/hygiene the design must add before the L1
runs `--write`.**

---

## Findings (severity, exploit path, evidence, impact, smallest remediation)

### F1 — HIGH (design / write scope): the repair tool's write target is caller-chosen and can be the lane; no seat item forbids `--root <lane> --write`

The delivered tool writes exactly one path, `Path(root).resolve()/corpus/knowledge/freshness-sidecar.json`
(constant, lines 96-99, 132-135), and it refuses to create a missing sidecar (verified: exit 2, zero
new entries — see T5). But `--root` defaults to `.` and has no lane/fleet denylist. Pointed at the
lane, `--write` will rewrite a production file mid-wave, which is a lane write by a seat and would
invalidate every revision-bound measurement. [INFERENCE from the code path: no denylist, containment
only — this seat did not execute `--write` against the lane, by design.] The failure is procedural only.

- Evidence: `.ufo/waves/round-74/w1/ExecC2Tool/sidecar_reobserve.py` sha256
  `1284bd17d0f0e8c41ac37d27598d8cc623e39ee89866b950ad5a5f1f4e8d0c28`; `--root` default at line 236
  (`parser.add_argument('--root', default='.')`), containment check line 98, write line 132.
  The seat item (ExecC2Tool) constrains *what the tool writes relative to `--root`* but never says
  the seat may only run `--write` against a scratch clone.
- Mitigating fact: the host guard fixes the process cwd to the fleet root, where
  `corpus/knowledge/freshness-sidecar.json` does not exist (checked: `ls` exit 2), so an accidental
  default-invocation `--write` exits 2 and creates nothing (T5). The exploit needs an explicit
  `--root /home/vgpnk/Projects/shokunin/kake-shokunin`.
- Impact: one mistaken `--write --root <lane>` destroys the base sidecar bytes and with them the
  wholly pre-after-state receipt chain (the lane is git-backed, so recoverable, but then no longer
  the measured bytes).
- Smallest remediation: (a) make `--root` required when `--write` is given (default only for
  `--check`); (b) add to the ExecC2Tool item: "run `--write` only against a scratch clone; record
  the absolute root, the pre/post sha256 and `git -C <clone> status --porcelain`"; (c) L1 records
  `sha256sum corpus/knowledge/freshness-sidecar.json` == `9ecfdf2b…` before and after the wave and
  greps seat reports for `--write` against the lane path.

### F2 — MEDIUM (receipt integrity / detector gap): the C2 counter's exit code ignores `annotation_findings`, so the frozen history-preservation kill rule has no instrument

`measure_entries` computes `met`/`exit_code` from stat counts only (lines 89-90). `measure()` adds
`annotation_findings` (lines 94-114, 120-121), but `main` prints `summary(result)` (which excludes
them) and returns `result['exit_code']` (lines 199, 129). The sweep's `loadPathSidecar` never
inspects `history` either (review of `scripts/freshness-sweep.mjs:359-394`).
Therefore an entry flipped to `restored` with a missing or altered `history` — with the token
present — yields `met=true`, exit 0, and passes the sweep binding. The contract's kill rule says C2
fails if "any history entry differs from the base note bytes" (contract:112). Only the counter's
function-level selftest g5 notices, and g5 passes because it calls `annotation_findings` directly.

- Evidence (observed end to end): in scratch clone `$S/probe2` at base, the delivered tool's
  `--write` flipped 144 entries (4 genuinely absent stayed absent); I deleted `history` from one
  flipped entry and committed (`6110458541d48be0d1270e0ba681813c4e144f22`). The counter prints
  `entries=174 absent=4 restored=170 … contradictions=0 met=true` and **exit 0**, while `--json`
  reports `annotation_findings=[{'index': 30, 'issue': 'prior-history'}]`. The sweep binds the same
  bytes without error (exit 1, only the standing `~/projects` drift). The kill-rule violation is
  invisible to both verdicts.
  Supporting: `--selftest` → `selftest 6/6`, exit 0; `--root <clone> --revision <base>` → 144
  contradiction line, exit 1. Code lines as above (counter sha256
  `62b3d9e8188ce88bfecd30dbd2076a5b3f3edb6396f6187023bb964c8b7df285`).
- Impact: an after-state can claim C2 met while violating a named kill rule; a reviewer who runs the
  counter as specified cannot detect it.
- Smallest remediation: fold findings into the verdict — `met = stat_clean and not annotation_findings`,
  exit 1 when findings, and add one file-level selftest case (a flipped entry with `history` deleted)
  that exercises `main`, not `annotation_findings` directly. (Route to MutC2 as the M5 mutant: it
  should currently survive.)

### F3 — MEDIUM (receipt integrity): the C2 control receipt is not byte-reproducible and the frozen predicate uses a third field vocabulary

Three different strings describe the same measurement:

1. Contract predicate (contract:79): `python3 -B … --root . --revision <rev>` must print
   `absent_notes_resolving=0 restored_notes_absent=0 unevaluable=0 met=true` and exit 0.
2. Contract reproduction clause (contract:97): the counter's run at base MUST reproduce
   `controls/base-c2-sidecar.txt` exactly, named as
   `entries=174 absent=148 restored=26 absent_present=144 absent_absent=4 restored_absent=0 contradictions=144 met=false`.
3. The delivered counter prints one line with `absent_present/absent_absent/absent_unevaluable/restored_present/restored_absent/restored_unevaluable/contradictions` — none of the predicate's
   `absent_notes_resolving` / `restored_notes_absent` / `unevaluable` tokens.

The control file itself is 14 lines: 4 summary lines plus 10 lines (`sample (...)` ×6,
`genuinely_absent_tokens= 3`, `absent_token …` ×3) that no specified counter emits. Observed:
counter stdout is 1 line; `diff` against the control is 13 removed lines (`diff` exit 1); the numeric
values match exactly.

- Evidence: `diff -u .ufo/waves/round-74/controls/base-c2-sidecar.txt <counter stdout>`; control
  sha256 `1d4fb00e184b1c27bdcd22c649083f368ef1c19fba4320c434bc0352fa283935`, 14 lines; counter 1 line.
- Impact: "reproduce exactly" is literally unachievable by the specified counter; a strict reviewer
  can fail a correct counter, and the predicate's own token names cannot be satisfied by any artifact
  in the round.
- Smallest remediation (pre-data, no seat has scored): L1 records a one-paragraph clarification that
  "reproduce exactly" means the summary tuple plus exit, that the sample/token lines are informational
  L1-probe output, and that the predicate's three tokens map to `absent_present`,
  `restored_absent`, `absent_unevaluable+restored_unevaluable`. For future rounds, put `rev=`, `cmd=`
  and `exit=` headers in every receipt.

### F4 — MEDIUM (frozen-control integrity): four harm receipts were added to `controls/` after the freeze commit and after the wave opened, untracked and unattributed

At review, `.ufo/waves/round-74/controls/` contains the three frozen receipts (committed in
`b35dd4d7`) **plus** `base-harm-c70.txt`, `base-harm-c72.txt`, `base-harm-c73p.txt`,
`base-harm-c73tmp.txt`, all mode 644, mtime `2026-11-03 20:15:45` — after the freeze commit
(`git show --stat b35dd4d7` lists only contract.md + 3 controls + 4 sources) and after the wave
directory was opened (20:14). All four are untracked (`git status --porcelain -- .ufo/waves/round-74/controls/`
prints `??` for each). No seat item authorises a write to `controls/` (spec scan below), so either a
seat wrote outside its scope or the L1 wrote after declaring controls frozen (contract:5: "Frozen
before any seat ran: … controls … are fixed").

The receipts themselves have no `cmd=` line; `base-harm-c70.txt` has no `revision=` line; exits are
encoded as bare `c70=0` / `c72=0` / `c73p=0` / `c73tmp=0` (consistent, but not labelled as exits).
Their values do corroborate the contract's harm battery (c70 `unannotated=0 met=true`; c72
`findings=[] removed=8 added=16 met=True`; c73p `met=true`; c73tmp `selftest=41/41 findings=[] met=True`).

- Evidence: `ls -la --time-style=full-iso .ufo/waves/round-74/controls/`; `git status --porcelain -- .ufo/waves/round-74/controls/`;
  `git show --stat --oneline b35dd4d7`.
- Impact: the control set that the contract calls frozen is not the set on disk; the four receipts
  cannot be bound to a revision, so they cannot be cited as "before" evidence.
- Smallest remediation: L1 discloses authorship, and either (a) commits the four receipts at a named
  revision (a separate freeze commit, disclosed in the report) or (b) moves them under
  `.ufo/waves/round-74/w1/` and re-runs them from a base clone; add `rev=`/`cmd=`/`exit=` lines.

### F5 — LOW-MEDIUM (writer accepts input the reader rejects): `validate()` is weaker than the sweep's `loadPathSidecar`, so `--write` can emit a sidecar that breaks the sweep binding while the counter still reports met

The tool validates schema/kind/line/lineSha256/date/history (`validate()`, line 37) but not the
reader's rules for `file` (`SKILL.md` or `corpus/**/*.md`, no `.`/`..`/empty components) or `token`
canonical spelling (`canonHome(token) === token`; `scripts/freshness-sweep.mjs:366-371`). Tested: an entry with
`file='../../../../etc/hostname'` and a present token was flipped, written, exit 0 (T6). `strace`
confirms the traversal string is never opened (0 hits) — `entry.file` is used only inside the note
string — but the resulting sidecar throws `paths sidecar invalid entry` / `paths sidecar binding
invalid` in the sweep while the counter reports met. Observed: with one `file` set to
`../../../../etc/hostname` and committed (`e609939e341636a33aeb7742cac47d4437f36418`), the counter
prints `met=true` and exits 0; the sweep exits 2 with `freshness-sweep: Error: paths sidecar invalid entry`.

- Evidence: T6 below; sweep rule lines `scripts/freshness-sweep.mjs:366-371`; the two instrument runs
  over the same commit (`e609939…`).
- Impact: a hand-edited or hostile sidecar turns the C2 harm check red (`--offline` exit 2) with no
  counter-side signal; the two instruments disagree about the same claim.
- Smallest remediation: mirror the reader's `file` and token-canonical checks in `validate()` and
  refuse (exit 2) before any note is composed; add a selftest fixture with a traversal-shaped `file`.

### F6 — LOW (durability): the sidecar rewrite is not atomic

The write is `os.open(..., O_WRONLY|O_TRUNC|O_NOFOLLOW)` then `json.dump` in place (lines 132-136),
with no temp file, no `os.replace`, no `fsync`. A crash, SIGKILL or ENOSPC between truncate and the
end of the dump leaves a truncated sidecar — in a scratch clone that is the only copy of the fixture
state. The contract asks for determinism, not atomicity, but receipt integrity implies the last good
bytes survive a failed write.

- Smallest remediation: write to a temp file created with `tempfile.mkstemp(dir=sidecar.parent)`, then
  `os.replace(tmp, sidecar)`; keep `O_NOFOLLOW` semantics by rejecting a symlinked sidecar before the
  replace (already done, line 98).

### F7 — LOW (write-scope hygiene): `freshness-sweep.mjs --selftest` writes outside the seat scratch and leaves residue

The sweep's normal path is read-only (verified), but `--selftest` builds fixtures under
`process.env.KAKE_SELFTEST_DIR || path.join(os.tmpdir(),'kake-r16','selftest')` and cleans only
`homeFixtureDir` (`scripts/freshness-sweep.mjs:1208, 1241, 1673`). Observed: 37 residue entries left
under `<TMPDIR>/kake-r16/selftest`. ReviewerC2 item (4) and the contract's harm battery ask for this
command without pinning `KAKE_SELFTEST_DIR`; with an inherited `TMPDIR=/tmp` that is a write outside
the two allowed roots (and the wave rule forbids relying on an inherited TMPDIR).

- Evidence: run below (selftest exit 0, `36/36 passed`, `residue_count=37`).
- Smallest remediation: require `KAKE_SELFTEST_DIR=<scratch>/sweep-selftest TMPDIR=<scratch>` in the
  item and in the harm battery; the L1 should assert no residue in `/tmp`.

### F8 — INFORMATIONAL (residual, no action this round)

- TOCTOU: the realpath/`is_symlink` check (line 98) and `os.open` (line 132) are separate operations;
  a parent-directory symlink swapped between them would redirect the write. `O_NOFOLLOW` protects only
  the final component. Not reachable within a seat's declared write scope; note for the next tool revision.
- Existence oracle: both instruments `os.stat` the token, and the tool's `validate` accepts absolute
  tokens (e.g. `/etc/hostname`); no file contents are read (verified with `strace`), but the sidecar can
  be used to probe host path existence. Acceptable while the sidecar is trusted committed bytes.

---

## (1) Write scope — PASS, with F1 and F7 as the only gates to close

All 14 seat items were parsed and every absolute path/write verb extracted. Each seat's write targets
are exactly:

| Seat | Declared write targets | Inside scope |
|---|---|---|
| ScoutSources | `w1/ScoutSources.md`, `w1/ScoutSources/{python-os-path,python-os-stat}.{html,txt}`, `strip-tags.py` | yes |
| ScoutSidecar | `w1/ScoutSidecar.md` | yes |
| ExecC1Counter | `w1/ExecC1Counter.md`, `w1/ExecC1Counter/c74_registry_gap.py` | yes |
| ExecC1Rows | `w1/ExecC1Rows.md`, `w1/ExecC1Rows/*` (evidence + copied contracts) | yes |
| ExecC2Tool | `w1/ExecC2Tool.md`, `w1/ExecC2Tool/sidecar_reobserve.py` | yes |
| ExecC2Counter | `w1/ExecC2Counter.md`, `w1/ExecC2Counter/c74_sidecar_reobserve.py` | yes |
| ScribeRows | `w1/ScribeRows.md` | yes |
| ScribeKnowledge | `w1/ScribeKnowledge.md` | yes |
| ReviewerC1 | `w1/ReviewerC1.md`, `w1/ReviewerC1-heldout/*` | yes |
| ReviewerC2 | `w1/ReviewerC2.md`, `w1/ReviewerC2-heldout/*` | yes |
| CriticClaims | `w1/CriticClaims.md` | yes |
| MutC2 | `w1/MutC2.md` (+ mutants in scratch) | yes |
| ConnOverlap | `w1/ConnOverlap.md` | yes |
| Sentinel | `w1/Sentinel.md` | yes |

- Outside paths named by items are reads only: `sources/`, `controls/`, `contract.md`,
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, `scripts/freshness-sweep.mjs`,
  `scripts/id_resolver.py`, round-69..73 contracts and counters. `sources-census.sh validate` emits to
  stdout unless `-o` is passed and the items pass no `-o` (`emit()` at `scripts/sources-census.sh:94`);
  `--offline` never writes (verified in section (4)).
- Forbidden-token scan over all 14 items for `.ufo/state`, `MANIFEST.json`, `watchdog.log`, `.scratch/`,
  `templates/`, `SCORECARD.md`, `LOG.md`: 0 hits.
- Observed lane state: `git -C … status --porcelain` shows only untracked `.ufo/waves/round-74/w1*`
  harness files, seat outputs under `w1/`, and the four F4 control files. No tracked file modified;
  sidecar sha equals base.
- Scope gaps: F1 (tool can be pointed at the lane), F7 (`--selftest` residue), F4 (controls written
  after freeze — outside every seat's item).

## (2) Re-observation tool: path traversal, symlink writes, and `--check`

Design answer to the seat question — **`--root` plus `entry.file` cannot escape the lane for a write**,
in the delivered bytes:

- The write path is the constant `root/corpus/knowledge/freshness-sidecar.json`; `entry['file']` is
  interpolated only into the note string (`new_note`, lines 83-91) and is never opened (confirmed by
  `strace` with `file='../../../../etc/hostname'`: 0 `openat` hits, T6). The sweep reader constrains
  `file` to `SKILL.md|corpus/**/*.md` with no `.`/`..` parts (`freshness-sweep.mjs:366-371`), so a
  traversal-shaped `file` cannot be a read path there either — but the tool does not enforce that rule
  and will emit a sidecar the reader rejects (F5).
- Symlink writes are blocked three ways: `Path(root).resolve()` (line 96), realpath containment plus
  `is_symlink()` (line 98), and `O_NOFOLLOW` on the final component (line 132). Verified with both a
  symlinked `corpus/knowledge` directory and a symlinked sidecar file: exit 2, target bytes unchanged
  (T3, T4). Residual parent-dir TOCTOU: F8.
- `--check` cannot write: the write branch is gated by `if write:` (line 122) and notes are composed
  before any mutation (line 125); the check run exits 0 with `wrote=false`, sha unchanged, and `strace`
  shows zero `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC` opens (T1).
- Fail-closed properties confirmed: missing sidecar → exit 2, no directory or file created (T5);
  unevaluable token → exit 2, sidecar byte-unchanged, nothing partially applied (T9); hostile `--host`
  containing absence vocabulary with a live candidate → exit 2, byte-unchanged (T7b); invalid calendar
  date → exit 2 (T8); second `--write` on an already-flipped file → byte-identical, `flipped=0` (T2b);
  two independent runs from identical input → identical sha256 (T-det); `--selftest` 8/8, exit 0, no
  residue when `--work` points into scratch.

**What a reviewer must test** (all against a scratch clone or fixture root; never `--root <lane> --write`):

1. `--check` no-write: `strace -f -e trace=openat,open,unlink,rename,renameat,renameat2 -o log python3 -B tool --root <clone> --check`;
   assert zero `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC` in `log` and unchanged sha256.
2. Parent symlink escape: `mkdir -p R/corpus; ln -s <outside> R/corpus/knowledge; tool --root R --write --date 2026-11-03`;
   expect exit 2 and outside target unchanged.
3. Final-component symlink: `ln -s <outside-file> R/corpus/knowledge/freshness-sidecar.json`; expect exit 2,
   outside file unchanged.
4. Absent sidecar (fleet-root mimic): empty root, `--write`; expect exit 2 and `find R -mindepth 1` empty.
5. Hostile `entry.file`: `../../../../etc/hostname` plus a present token; expect (after F5) exit 2;
   today exit 0 — assert via `strace` that the string is never opened and that the note still carries it
   verbatim, then run the sweep binding over the result and record `paths sidecar binding invalid`.
6. Hostile `--host` (`linux missing`) with at least one live candidate: expect exit 2, no write; also
   test a newline-bearing host to confirm the note is a single JSON string.
7. Unevaluable token: expect exit 2, sha unchanged, and no entry mutated (compare full JSON, not just kind).
8. Idempotence/determinism: two `--write` runs on the same input → identical sha256; second run `flipped=0`.
9. Atomicity: inspect for `os.replace` (currently absent, F6); if testing, SIGKILL mid-write on a large
   fixture and assert the file is one of exactly {pre-sha, post-sha}.
10. Lane integrity at wave end: `sha256sum corpus/knowledge/freshness-sidecar.json` == `9ecfdf2b…` and
    `git status --porcelain` unchanged except `w1/`.

## (3) Secrets — PASS, none found

Scan of the retained sources (16,596 lines across the two HTML and two tag-stripped text files), the
contract, all controls, the wave spec, and every file under `w1/` (including the artifacts delivered
during this review):

```
grep -rIlE 'AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[abprs]-[A-Za-z0-9-]{10,}|sk-[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}' .ufo/waves/round-74/
# exit 1 (no match), files_with_hits=0
grep -rInE '(AWS_SECRET_ACCESS_KEY|GITHUB_TOKEN|GH_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY|ELEVENLABS_API_KEY|CLOUDFLARE_API_TOKEN)[[:space:]]*[=:]' .ufo/waves/round-74/
# exit 1, assign_hits=0
grep -cE 'Set-Cookie|Authorization:' sources/*.html   # 0 and 0, exit 1
grep -rl 'BEGIN .*PRIVATE KEY' .ufo/waves/round-74/   # no files, exit 1
```

No credential-shaped string, PEM block, session token, auth header or cookie in the retained bytes.
The only long hex strings are the corpus sha256 digests, which are content hashes, not secrets.

## (4) Receipt integrity — findings F3, F4; per-file result

| Control | Revision in file | Command recorded | Exit recorded | Replay result |
|---|---|---|---|---|
| `base-c1-registry.txt` | yes (`ced2878a…`) | no | no (contract asserts 1) | Independent row census reproduced `rows=0` ×7 and `c73_tmp_v3.py` `rows=1` at `SKILL.md:1404`; `unregistered=7` |
| `base-c2-sidecar.txt` | yes | no | no (contract asserts 1) | Delivered counter reproduces the 4 summary lines' values exactly (`entries=174 absent=148 restored=26 absent_present=144 absent_absent=4 restored_absent=0 contradictions=144 met=false`, exit 1); 10 sample/token lines are not emitted — F3 |
| `base-c2-sweep.txt` | **no rev of the probe clone** | no | yes (`SWEEP_EXIT=1`) | My base clone replay: `§paths 193 files · 712 occurrences · 107 unique tokens`, `DRIFT 1 … ~/projects`, `VERDICT: DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet (exit 1, partial: offline)`, exit 1 — identical key lines; `--selftest` 36/36 exit 0 |
| `base-harm-c70/c72/c73p/c73tmp.txt` | c70 no; others yes | no | bare `cXX=0` | Values corroborate the harm battery; all four are **untracked and post-freeze** — F4 |

Also: `--offline` replay in the base clone changed no file (`find` before/after identical,
`git status --porcelain` empty) — the sweep's normal path is read-only as documented
(`freshness-sweep.mjs:21`).

Instrument dry run (evidence for F2/F5; this is not an acceptance verdict on C2): in scratch clone
`$S/probe2` at base, the delivered tool's `--write` flipped 144 entries, left the 4 genuinely absent
entries at `kind=absent`, preserved all 143 still-present prior notes byte-identically
(`history_exact=143 history_mismatch=0`), and exited 0. The sweep over the rewritten sidecar exited 1
with only the standing `~/projects` drift — no `paths sidecar binding invalid`, no `Error:` line.
The two synthetic violations reported in F2 and F5 were then injected into that same clone
(commits `6110458…` and `e609939…`); in both, the counter stayed `met=true` / exit 0.

## (5) Mutating git/jj — PASS, none

Regex scan of all 14 items for `git (add|commit|push|stash|checkout|switch|reset|pull|merge|rebase|clean|rm|mv)`
and `jj (commit|describe|new|edit|abandon|rebase|squash|bookmark|git push|op restore)`: **0 hits**.
Items that create repositories say "scratch clone" / "fixture under your scratch", and the wave
context requires `git rev-parse --show-toplevel` == fixture dir before the first commit.
Delivered artifacts use git read-only: `git -C <root> show --end-of-options <rev>:<path>`
(counter:41) and `git -C <lane> show <rev>:…` (ReviewerC2 fixture); no `add/commit/push/checkout/jj`
in any artifact. My own probes are confined to a `git clone --shared` in scratch and left it clean.

## (6) Verdict

**PASS for the wave as designed**, with the following routes:

- Route to L1 before the after-state: F2 (counter must fail on history/vocabulary findings), F3
  (clarify "reproduce exactly" and the predicate field names, pre-data), F4 (attribute/commit or move
  the four post-freeze receipts), F1c (record lane sidecar sha before/after).
- Route to the ExecC2Tool seat/owner: F1a+b (`--root` required for `--write`; item forbids `--root <lane>`),
  F5 (mirror the reader's `file`/token validation), F6 (atomic replace), F7 (pin `KAKE_SELFTEST_DIR`).
- F8 is recorded, no action this round.

## Appendix — exact commands and exit codes (scratch `/fast/scratch/hyaku/kake-r74/Sentinel`)

```
git clone --shared -q <lane> $S/probe            # exit 0
git -C $S/probe checkout -q ced2878a…            # exit 0; rev-parse --show-toplevel = $S/probe
node scripts/freshness-sweep.mjs --offline       # exit 1; VERDICT line identical to control
node scripts/freshness-sweep.mjs --selftest      # exit 0; "selftest: 36/36 passed"
                                                 # residue under $TMPDIR/kake-r16/selftest: 37 entries (F7)
python3 -B .ufo/waves/round-74/w1/ExecC2Counter/c74_sidecar_reobserve.py --selftest
                                                 # exit 0; selftest 6/6
python3 -B …/c74_sidecar_reobserve.py --root $S/probe --revision ced2878a…
                                                 # exit 1; entries=174 … contradictions=144 met=false
diff -u controls/base-c2-sidecar.txt <counter stdout>            # exit 1; 13 lines only in control (F3)
awk '/^\| / && index($0,"c73_tmp_v3.py")' SKILL.md(base bytes)   # line 1404, rows=1
# tool probes (fixture roots, never the lane):
tool --root R --check --json                     # exit 0, wrote=false, sha unchanged, 0 write flags (T1)
tool --root R --write --date 2026-11-03 …        # exit 0, flipped=1, history appended, idempotent (T2/T2b)
tool --root R3 --write …  (corpus/knowledge symlink)  # exit 2 "sidecar must be a regular path under root" (T3)
tool --root R4 --write …  (sidecar symlink)           # exit 2, outside file unchanged (T4)
tool --root R5 --write …  (no sidecar)                # exit 2, 0 entries created under root (T5)
tool --root R6 --write …  (file=../../../../etc/hostname)  # exit 0, wrote=true, 0 outside opens (F5/T6)
tool --root R7 --write --host "linux missing" …       # exit 2, unchanged (T7b)
tool --root R8 --write --date 2026-13-45              # exit 2 (T8)
tool --root R9 --write …  (unevaluable token)         # exit 2, unchanged (T9)
tool --selftest --work $T                             # exit 0, 8/8, residue 0
sha256sum corpus/knowledge/freshness-sidecar.json     # 9ecfdf2b… == base, before and after all tests
# instrument dry run in scratch clone $S/probe2 (never the lane):
tool --root $S/probe2 --write --date 2026-11-03       # exit 0; flipped=144, absent=4
# one history removed, committed: 6110458541d48be0d1270e0ba681813c4e144f22
counter --root $S/probe2 --revision 6110458…          # met=true, exit 0; findings=[{index:30, issue:prior-history}]
node scripts/freshness-sweep.mjs --offline            # exit 1; no binding error
# one file field set to ../../../../etc/hostname, committed: e609939e341636a33aeb7742cac47d4437f36418
counter --root $S/probe2 --revision e609939…          # met=true, exit 0
node scripts/freshness-sweep.mjs --offline            # exit 2; Error: paths sidecar invalid entry
```
