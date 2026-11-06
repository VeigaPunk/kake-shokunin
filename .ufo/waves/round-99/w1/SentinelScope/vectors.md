# SentinelScope — round 99 execution-boundary vectors (seat w1/SentinelScope)

Target: execution boundaries of `.ufo/waves/round-99/c99_registry.py` (`run_span()`, C1) and
`.ufo/waves/round-99/c99_fresh304.py` (`run_candidate()`, C2). All PoCs are harmless, confined to
`/fast/scratch/hyaku/kake-r99/SentinelScope/` (fixture repos created with `git init`, identity
`sentinelscope@example.invalid`, toplevel asserted before first commit). The lane was never mutated
(read-only git only). No repair was made to any instrument; findings are routed to L1.

## Provenance of the reviewed instruments (verified, not assumed)

- `controls/instrument-sha256.txt`: `sha256sum -c` rc=0, all 11 entries OK (worktree bytes).
- `git show 2345e30:.ufo/waves/round-99/c99_registry.py | sha256sum` = `0f39bbbc…` and
  `…c99_fresh304.py` = `d13bba5d…` — both equal the frozen digest file, so the bytes reviewed are
  the committed instruments.
- Freeze commit `ab35eace` exists; `git show ab35eace:.ufo/waves/round-99/freeze.md | sha256sum` =
  worktree freeze.md sha `7446de3c…`; `git diff --stat ab35eace -- <counters, freeze.md>` empty
  (rc=0). Repair section present at `9d341d1b` (SKILL.md line 1700, `## Round 99 — tool registry
  completion`).
- Instrument sanity in scratch: `c99_registry.py --selftest` → `selftest 20/20` rc=0;
  `c99_fresh304.py --selftest` → `hand=50/50 reference agrees; …` `selftest 2/2` rc=0.

---

## V1 — c99_registry `run_span()`: single `&` bypasses FORBIDDEN → forced exit 0 → C1 met=true flip
- **Severity: HIGH. Verdict-affecting (C1): demonstrated met=false → met=true on the same broken tool.**
- Mechanism: `FORBIDDEN = \| > < ; && $( \`` — a lone `&` is not blocked (only `&&` is). The span is
  executed via `subprocess.run(argv)` with **no shell**, so the filter is the only shell-semantics
  gate; but `argv[0]` is unrestricted, so `bash -c '<payload>'` hands the payload to a real shell,
  where `&` is a command separator. `cmd & true` ignores the tool's failure and exits 0.
- PoC (fixture revs in `poc-fx-revs.txt`, receipts `poc-reg-results.txt`):
  - baseline `5a234ae…` — honest row for `scripts/broken.py` whose `--selftest` exits 1 →
    `unlisted=1 … exec_fail=1 mismatches=1 met=false`, rc=1.
  - poc1 `6139baa…` — identical repo, self-test cell replaced by
    `` `bash -c 'python3 -B scripts/broken.py --selftest & true'` `` →
    `listed=2 unlisted=0 dangling=0 exec_fail=0 mismatches=0 met=true`, rc=0.
- Exploit path for this round: any SKILL.md row can pass R5 without the tool's selftest ever
  succeeding, flipping C1's `met=true`. Compensation in the frozen design: the two-reviewer conjunct
  sees the row bytes, and the kill rule turns a `disagree` into unmet — so the flip requires the
  reviewers to also miss the payload. The counter alone is forgeable.
- Smallest remediation: reject any `&` (and any of `; | < > $ \` `) in the raw span **before**
  placeholder masking; structurally, forbid code-eval flags (`-c`, `-e`, `-m`, `--eval`) in `argv`
  after shlex, or exec with `argv[0]` constrained to an interpreter allowlist plus a required
  argument that token-matches the population script.

## V2 — `PLACEHOLDER` masking hides bash redirect operators → arbitrary file write outside `--work`/tree
- **Severity: HIGH. Verdict-affecting (C1): same forced-rc-0 listing, plus out-of-sandbox write.**
- Mechanism: `FORBIDDEN.search(PLACEHOLDER.sub("PH", span))` masks every `<[^<>\s]+>` token **before**
  the denylist runs; shlex then passes the raw word through. In bash, `<x>path` is *two* redirects
  (stdin from `x`, stdout to `path`) — both operators live inside the masked region.
- PoC (poc2 `4a58890…`): self-test cell
  `` `bash -c '<x>/fast/scratch/hyaku/kake-r99/SentinelScope/poc-write-outside.txt python3 -B scripts/broken.py --selftest & true'` ``
  (repo commits a root file `x`) → counter prints `met=true` rc=0 **and** bash created
  `/fast/scratch/.../poc-write-outside.txt` — an absolute path outside `--work` and outside the
  extracted tree, chosen by the SKILL.md cell. When L1 scores with `--root .` from the lane cwd,
  the same primitive is a lane-tree write by SKILL.md text.
- Smallest remediation: same as V1 (raw-span denylist + argv-level structural check); additionally
  reject words that are not needed for the documented "simple command" grammar.

## V3 — unrestricted `argv[0]`, inherited PATH, no fs/network confinement
- **Severity: MEDIUM (design boundary; malicious-*tool* class, adjacent to the counter's declared limit).**
- `run_span()` builds `env` from scratch (good: no caller secrets — only `PATH`, `LANG`,
  `PYTHONDONTWRITEBYTECODE`; `HOME`/`TMPDIR`/`KAKE_SELFTEST_DIR` redirected into the exec base) but
  inherits `PATH` verbatim and never restricts `argv[0]`. Any installed binary is executable; any
  interpreter (`bash -c`, `python3 -c`, `perl -e`, `awk 'system(…)'`) receives code the text filter
  cannot inspect. Network is unrestricted.
- PoC (sanctioned-shape, no bypass): committed `scripts/net.py` selftest opened a socket during
  scoring — `socket connect_ex(("127.0.0.1", 9)) → rc=111` recorded in
  `poc-sanctioned-net.txt` (3 runs, one per counter invocation). Writes outside the tree by
  sanctioned repo code are equally possible (tool code runs as the scoring user).
- Note: executing committed repo tools is the instrument's design (R5 "that span EXECUTES"); this
  vector is the *excess* beyond the design (network + host fs + arbitrary non-repo binaries), not
  the execution itself.
- Smallest remediation: bwrap/landlock namespace per span (only extracted tree + scratch visible, no
  network), scrub `PATH` to a minimal set.

## V4 — `ASSIGN` stripping hides `$(…)` in leading assignment values (inert today)
- **Severity: LOW.** `ASSIGN.sub` runs before the FORBIDDEN check, so `VAR=$(…)` values are never
  seen by the denylist; the post-shlex loop then drops those words (no shell → no execution), so
  this is currently inert — but the docstring's "no `$(` after leading VAR=value words" is not what
  the code enforces, and future edits can turn the gap live. Observed benign: `X=$(touch …) cmd`
  tokenizes to `["X=$(touch", "/tmp/pwn)", "cmd"]` → dropped/garbage argv → rc=127, no execution.
- Smallest remediation: check the raw span including assignments; reject `$(` in assignment values.

## V5 — per-span 240 s budget, span cache
- **Severity: LOW.** Each distinct self-test span may consume 240 s (timeout → rc=124); a registry
  table is a timing lever on scoring. The per-span cache bounds repeats (one execution per distinct
  span). Remediation: global wall-clock budget for `score()`.

## V6 — checked-OK boundaries (no action)
- Tar extraction uses `filter="data"` on the host Python (3.14.8), so archive members with absolute
  paths or escaping symlinks are refused — the extracted tree is not an escape hatch via commit
  contents.
- `shlex`/bash quoting mismatch observed and **load-bearing in the safe direction**:
  `bash -c $'…\x3e…'` ANSI-C payloads do *not* survive `shlex.split` (`$` tokenizes separately from
  the quoted chunk → `bash -c "$" extra-args` → rc=127). This accidental protection must not be
  relied on as a control (see V1/V2 for real bypasses).
- Entry-command cells are never executed — only self-test spans run, cached per span. Surface is
  smaller than a full table-execution model.

---

## W1 — c99_fresh304 `run_candidate()`: candidate reads the counter's own oracle → perfect score with zero contract logic
- **Severity: CRITICAL. Verdict-affecting (C2): demonstrated — the frozen predicate `met=true` is attainable by a candidate that implements nothing.**
- Mechanism: `run_candidate()` scrubs env, uses `-I -B`, and gives a fresh cwd — but procfs is
  unmasked. The candidate reads `/proc/<ppid>/cwd` (→ caller cwd) and `/proc/<ppid>/cmdline` (→ the
  counter path), `sys.path.insert`s the counter's directory, `import c99_fresh304`, and answers
  every case with `ref_or_refusal()`. The `HAND` expectations and the generated-case `reference()`
  live in that one importable module; `frozen/pos-oracle.py` is equally readable.
- Observed (receipt `poc-c2-results-summary.txt`, candidate source `poc-c2-cheat-candidate.py`):
  `candidate=present sha256=2088ed03db3585aa8bd9cdd54e5f994141612d1da66aabeb22b5f12009ce6e2c hand=50/50 generated=240/240 refusals=50/50 seed=99099 met=true`, rc=0 — from a candidate with **no
  RFC 9111 logic at all**. All 290 cases ran and answered via the stolen oracle.
- Impact for this round: C2's frozen predicate ("candidate=present hand=50/50 generated=240/240
  met=true, exit 0") cannot, by itself, certify capability acquisition — it certifies behavior on
  cases whose answer key the candidate can read. There is no reviewer conjunct on C2 candidate
  provenance (unlike C1's row review).
- Smallest remediation (routed; instruments are frozen — no in-round change): record as a declared
  instrument limit in the closure, mirroring C1's junk-prose limit. For future rounds: execute the
  candidate in a namespace where the counter source and frozen oracles are absent/unreadable —
  pid namespace (kills `/proc/<ppid>` discovery) + bind-mounting only the case dir; or split
  expectation computation into a separate root-owned process and run candidates as an unprivileged
  user with no read access to instrument paths.

## W2 — candidate runs with unconfined filesystem → cross-claim tamper primitive
- **Severity: HIGH. Verdict-affecting for round integrity (could corrupt the C1 review conjunct's inputs).**
- Proven: the PoC candidate wrote **290/290** case receipts to the *caller's* cwd via
  `/proc/<ppid>/cwd` (file `c2-capability-proof.txt`, deduped in the receipt) — i.e. writes outside
  its case dir and outside `--work`, to a path it chose. The same two primitives (procfs parent
  discovery + arbitrary user-writable write) are lane-tree writes when L1 invokes the counter from
  the lane. During C2 scoring, repo-committed candidate code could therefore modify lane state —
  including `w1/<review seat>/verdicts.tsv` files that C1's frozen review conjunct reads.
- Exploit path requires the lane's own committed candidate to behave maliciously; likelihood low,
  impact cross-claim. PoC stayed inside the seat scratch.
- Smallest remediation: same isolation class as W1; interim: score C2 with cwd = scratch and ensure
  the lane tree is not writable by the scoring user during the run (not locally achievable → L1).

## W3 — state persists across cases via the shared work dir
- **Severity: MEDIUM.** `dirname(argv[0])` is the same work dir for all 290 cases (case dirs are
  fresh per case; the candidate file is written once). Proven: the PoC's `.sentinel-hits` counter in
  that shared dir reached exactly 290 during one counter run. A candidate can count invocations,
  detect the hand-vs-generated phase (hand cases run first), or coordinate per-case behavior. The
  work dir is deleted after the run, so persistence does not survive the counter process.
- Smallest remediation: copy the candidate bytes into each fresh case dir (candidate location
  per-case), or pass the candidate via stdin.

## W4 — raw sockets during scoring
- **Severity: MEDIUM.** Proven: candidate opened a socket (`connect_ex(("127.0.0.1", 9)) → 111`)
  in every case; outbound network (case exfiltration, beaconing) is unimpeded; the 10 s per-case
  timeout bounds duration only. Same remediation class (network namespace).

## W5 — what DID hold (boundary that worked)
- `sys.executable -I -B` + minimal env neutralized the easy import paths: no `PYTHONPATH`, no user
  site, script dir not prepended to `sys.path`. The oracle theft needed procfs. Confirms the
  in-process isolation is well-built but the wrong isolation layer for untrusted code — namespace
  isolation is the remediation class for W1/W2/W4.

---

## Tally

| # | Vector | Surface | Severity | Verdict-affecting |
|---|--------|---------|----------|-------------------|
| V1 | single-`&` forced exit 0 | registry `run_span` | HIGH | yes (C1) |
| V2 | placeholder-masked redirects, out-of-sandbox write | registry `run_span` | HIGH | yes (C1) |
| V3 | unrestricted argv[0]/PATH/network | registry `run_span` | MEDIUM | no (design-boundary excess) |
| V4 | ASSIGN hides `$(` in values (inert) | registry `run_span` | LOW | no |
| V5 | 240 s per-span timing lever | registry `run_span` | LOW | no |
| V6 | checked-OK: data filter, minimal env, entry cells never run, `$''` mismatch | registry | INFO | no |
| W1 | oracle theft via procfs → met=true with zero logic | fresh304 `run_candidate` | CRITICAL | yes (C2) |
| W2 | unconfined fs → cross-claim tamper primitive | fresh304 `run_candidate` | HIGH | yes (round integrity) |
| W3 | cross-case state in shared work dir | fresh304 `run_candidate` | MEDIUM | no |
| W4 | raw sockets during scoring | fresh304 `run_candidate` | MEDIUM | no |
| W5 | isolation that held (`-I -B`, minimal env) | fresh304 `run_candidate` | INFO | no |

Blocking (gates closure until L1 routes): **W1** — the C2 met=true verdict is not tamper-evident
against oracle-reading candidates; instruments are frozen, so the remediation inside this round is
to record the limit in the closure (as C1 already declares its junk-prose limit). V1/V2 are
compensated by C1's two-reviewer conjunct (rows are lane-authored, bytes reviewer-visible, kill rule
on `disagree`) — not blocking; W2/W3/W4 require a malicious candidate and are routed, not blocking.

Tooling: no tools installed or upgraded for this seat (none needed); pacman untouched; host sysctls
untouched. Scratch receipts copied to this directory; seat scratch tree deleted before yield.

SENTINEL vectors=11 verdict_affecting=4 blocking=1
