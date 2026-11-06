# SentinelScope — round 99 seat report (execution-boundary review)

Seat target: execution boundaries of `c99_registry.py` `run_span()` (C1) and `c99_fresh304.py`
`run_candidate()` (C2). Full vector detail with mechanisms, PoC cells, observed output and fix
recipes: `w1/SentinelScope/vectors.md`. PoC receipts (fixture SKILLs, tool sources, counter
outputs, cheat candidate, rev list) alongside it in the same directory.

## Provenance verified first
- `sha256sum -c controls/instrument-sha256.txt` → all OK, rc=0.
- `git show 2345e309:<counter>` digests equal the frozen digest file for both counters — reviewed
  bytes are the committed instruments.
- Freeze commit `ab35eace` present; freeze.md at that commit is byte-identical to the worktree
  (`git diff --stat ab35eace -- counters+freeze.md` empty). Repair section present at `9d341d1b`
  (SKILL.md:1700). No mismatch anywhere → no repair license taken.
- Instrument sanity: `c99_registry.py --selftest` = `selftest 20/20` rc=0;
  `c99_fresh304.py --selftest` = `selftest 2/2` rc=0 (both in seat scratch).

## Findings (11 vectors; full table in vectors.md)

**C1 — registry counter (`run_span`):**
1. **V1 HIGH, verdict-affecting:** lone `&` is not in FORBIDDEN (only `&&`); `bash -c '<selftest> & true'`
   forces exit 0 for a genuinely failing tool. Demonstrated on one fixture repo: honest row →
   `met=false` rc=1 (rev `5a234ae`); payload row → `met=true` rc=0 (rev `6139baa`), identical
   `broken.py`. Compensation: C1's two-reviewer conjunct sees the row bytes; counter alone is
   forgeable.
2. **V2 HIGH, verdict-affecting:** `PLACEHOLDER` masking runs before the FORBIDDEN check, so
   `` `bash -c '<x>/abs/path … & true'` `` hides both redirect operators (`<x>path` = stdin+stdout
   redirects in bash) → `met=true` rc=0 (rev `4a58890`) **and** an arbitrary file created outside
   `--work` and the extracted tree at a path chosen by the SKILL.md cell.
3. **V3 MEDIUM:** `argv[0]` unrestricted, PATH inherited, network open — any binary/interpreter
   reachable from a cell; sanctioned-shape PoC `scripts/net.py` performed a socket connect during
   scoring (evidence receipt). Excess beyond the instrument's design (repo-tool execution itself is
   the design).
4. **V4 LOW (inert):** `ASSIGN` strips `VAR=$(…)` values before the denylist; post-shlex drop makes
   it non-executing today — a doc/code promise mismatch, not a live exploit.
5. **V5 LOW:** 240 s per distinct span — timing lever on scoring; span cache bounds repeats.
6. **V6 INFO (checked-OK):** tar `filter="data"` blocks path/symlink escapes; env carries no caller
   secrets; entry-command cells never execute; `$'…'` ANSI-C payloads do not survive shlex
   (observed rc=127) — accidental, not a control.

**C2 — fresh304 counter (`run_candidate`):**

7. **W1 CRITICAL, verdict-affecting, BLOCKING:** a candidate that implements zero contract logic
   recovered the counter's oracle via `/proc/<ppid>/{cwd,cmdline}` → `import c99_fresh304` →
   answered with `ref_or_refusal()`. Observed: `candidate=present sha256=2088ed03… hand=50/50
   generated=240/240 refusals=50/50 seed=99099 met=true` rc=0. The frozen predicate cannot
   distinguish capability from oracle theft (`frozen/pos-oracle.py` equally readable). Instruments
   are frozen → route to L1: record as a declared instrument limit in the closure (mirroring C1's
   junk-prose limit); future rounds need pid/fs namespace isolation of the candidate.
8. **W2 HIGH:** candidate wrote 290/290 case receipts to the *caller's* cwd (procfs parent-cwd
   primitive) — writes outside case dir and work; same primitives are lane-tree writes when L1
   scores from the lane, i.e. cross-claim tamper potential against the C1 review conjunct's input
   files. PoC confined to seat scratch.
9. **W3 MEDIUM:** state persists across all 290 cases via the shared work dir (`dirname(argv[0])`;
   PoC counter reached exactly 290) — phase detection/coordination possible; does not outlive the
   counter run.
10. **W4 MEDIUM:** raw sockets during scoring (proven `connect_ex` each case) — exfil/beacon
    possible; per-case timeout bounds duration only.
11. **W5 INFO:** `-I -B` + minimal env correctly neutralized PYTHONPATH/user-site/script-dir import
    paths — the theft required procfs, confirming in-process isolation is the wrong layer.

Blocking count: 1 (W1 — closure must carry the limit; no in-round instrument change proposed).
Verdict-affecting: 4 (V1, V2, W1, W2).

## Bound compliance
Writes only to `w1/SentinelScope*` (vectors.md, this report, PoC receipts) and seat scratch
`/fast/scratch/hyaku/kake-r99/SentinelScope/`; lane untouched (read-only git only: rev-parse, show,
ls-tree, cat-file, diff); fixture commits made in scratch with `git init`, toplevel asserted,
identity `sentinelscope@example.invalid` via `-c` flags; one fixture repo, no live clone of the
lane; no pacman, no sysctls, no tool installs; seat scratch tree deleted before yield (receipts
copied first).

SENTINEL vectors=11 verdict_affecting=4 blocking=1
