# ReviewerC2Counter

Reviewed artifact: the **contract-pinned committed version** of `.ufo/waves/round-59/c59_resolver_cases.py`
(blob at contract commit `45a92b6`, 350 lines, sha256 `ca2e85c685dbb9479ac96906296b7c8eaf460457a2184cac81e12927350fea33`
== `contract.json` `claims.C2.counterSha256v1`), plus `derive_c59_resolver_cases.py`.
Drift note: while I reviewed, the lane worktree copy of the counter became 768 lines (sha `90c431b…`, `git status`
` M`) — a sibling seat's in-flight 13-control selftest port. Findings below are stated against the committed v1 and
each says whether it also holds for the in-flight file. I did **not** run the in-flight port.

## FINDINGS:

**H1 HIGH — every gate fixture lane is distinguishable by a constant URL marker, so a fixture-keyed tool scores
21/21 while all seven routes stay open on a real lane.** `row()` (v1 line 65–66; in-flight line 75) emits
`fixture — https://example.invalid/<id>` into the first data row of *every* K/P fixture registry; P4's knowledge
file repeats the marker (in-flight line 264). The real lane's `corpus/SOURCES.md` and `corpus/knowledge/**` contain
zero occurrences of `example.invalid` (verified `grep -c`, 164-row registry). I built a candidate detector tool =
the honest fix, gated so the K8–K14 semantics apply only when the registry text contains `example.invalid`:
- counter result: `C2 resolver-cases 21/21 met=True … EXIT=0` (seed 7, revision `dfac0d5`), all 21 PASS incl. P6 `('66','66')`;
- same tool on a real-lane-shaped fixture (registry row `https://example.org/S001` + a row inside a multi-line
  HTML comment, knowledge cites `S001` and `S777`): `ids_cited=2 ids_resolved=2 dangling=0`, exit 0 — i.e. the
  c01 false green survives — while the honest fix on the same bytes printed `ids_cited=2 ids_resolved=1 dangling=1`, exit 1.
The round-58 v2 mitigation only randomized *case directory names* and the drawn ids; the fixture row URL stayed constant,
and the in-flight 13-control selftest does not add a fixture-content-keyed control (grep for `marker`/`fixture_keyed`
in the 768-line file: none). Fix: draw the fixture host per run from `--seed` (as `fixture_ids` already draws ids), or
drop URLs from fixture rows, **and** add a marker-keyed control to the gate selftest (a tool that closes the routes only
where the marker is present must score 20/21, not 21/21).

**M2 MEDIUM (v1 only; being fixed in-flight) — the committed counter's `--selftest` is a stub returning exit 2.**
`selftest()` v1 lines 298–300 prints `version 1 stub (not yet ported); exit 2`. Consequences: (a) the counter cannot
self-verify, so H1 is undetectable from inside the gate; (b) exit 2 is the counter's own documented *unevaluable* code
(contract.md C2 "Kill rule"), so a harness cannot distinguish "stub" from a genuine unevaluable run.
`derive_c59_resolver_cases.py:68-70` causes this: it slices `body[:sel]` at `# ---- selftest (wave-1 hardening)` and
`body[main_at:]` from `def main()`, discarding c58 lines 221–539 (CONST_STUB, MINI_STUB, `_stub`, `_control`,
`_fixture_lane`, `_base_tool`, the 7-control scorer). The source is intact at `1c0aa211` (resolvable in-lane).
The in-flight 768-line file already carries a 13-control port; the action is to land it, keep `BASE_REV = fd6303c`,
and add the H1 control.

**M3 MEDIUM — `P6_FLOOR = 66` silently requires the *fixed tool* to grow its own selftest suite from 59 to ≥66 cases.**
Base tool at `fd6303c` has 59 `_cases()` entries; P6 (v1 lines 271–276) demands a `selftest: N/N` tally with N ≥ 66.
Measured: an independent reference fix that closes **all seven routes** but adds no tool-selftest cases scores
`20/21 met=False`, the only failure being `P6_tool_selftest exit=0 ('59','59')`. So the fix must add exactly one
tool-selftest case per route. This is precedented (round 58: floor 55 against a 49-case base) and the contract does
disclose the base failure ("P6 fails (59 < 66)"), but the C2 claim sentence — "closes seven disclosed false-green /
robustness routes" — does not state it. Recommend recording "the fixed tool's own selftest grows by ≥7 cases" in the
contract text, or lowering the floor to the base count so P6 tests only self-consistency.

**L4 LOW — K14 admits one remedy only (exit 2), not the observable ("never green").** `check()` (v1 line 158) requires
`rc == want_rc` exactly; K14 wants 2. A fix that instead measured the subtree named by `--root` would correctly report
`DANGLING d14` at exit 1 and be scored FAIL (mechanism not exercised: [INFERENCE]). Contract.md routes K14 to F6, which
prescribes exit 2, so this is contract-consistent — recorded for the integrator, not a blocker.

**L5 LOW — K12/K14 assert no positive text** (`want_re = []`, forbids only the green summary, v1 lines 221 and 244):
any exit-2 cause passes (e.g. "exit 2 whenever the lane contains any symlink"), and no case covers an *in-lane*
registry symlink, so a fix that refuses every symlinked registry passes. Conservative, acceptable, but it is a
coverage gap; one positive case (`registry absent`/`registry outside` in stderr) would pin the reason.

**L6 LOW — the forbid regexes are format-locked.** `^ids_cited=\d+ ids_resolved=\d+ dangling=0\b` (v1 lines 221, 244)
matches only the tool's exact field order and single-space spacing; a reordered or re-spaced summary evades the forbid.
Low risk because the same cases' `want_re` summary assertions use that same format.

**L7 LOW — the derive script rewrites the frozen counter in place.** `derive_c59_resolver_cases.py:193` writes
`os.path.join(HERE, "c59_resolver_cases.py")`, i.e. into the lane's `.ufo/waves/round-59/`. Re-running it after the
in-flight selftest port would silently revert that port to the stub. Content risk today is nil: I re-ran the derive in
scratch and its output is **byte-identical** to the committed counter (reproducible from `1c0aa211`).

## CHECKLIST (each item the assignment named, verified)

1. **K13 bytes path is really non-UTF-8 in the committed tree — CONFIRMED.** The fixture commit's `git ls-tree -r -z`
   carries the raw byte `…626164ff2e6d64` = `corpus/knowledge/bad\xff.md`, mode `100644`; the non-`-z` listing C-quotes
   it `"corpus/knowledge/bad\377.md"`. Base tool decodes `-z` paths with `errors="replace"` → `bad\ufffd.md` →
   `git show` path miss → exit 2, exactly the observed `K13 FAIL exit=2 cannot read corpus/knowledge/bad?.md`.
2. **K14's ancestor really holds a green lane at its root — CONFIRMED.** Ancestor `corpus/SOURCES.md` registers
   `ok_id` **and** `d14`; ancestor `corpus/knowledge/ok.md` cites both → green at the ancestor root. The named lane
   `anc/lane` registers only `ok_id` while its knowledge cites `ok_id`+`d14`, so `d14` should dangle. Base tool with
   `--root anc/lane --revision head` reads repo-root-relative paths (`show head:corpus/SOURCES.md`, `ls-tree -r` →
   `corpus/knowledge/ok.md`), i.e. the ancestor, and prints `ids_cited=2 ids_resolved=2 dangling=0` exit 0 — the false green.
3. **K11's dangling link is committed as mode 120000 — CONFIRMED** for both entries: `120000 blob … corpus/knowledge/linked.md`
   (target `../notes.md` → `corpus/notes.md`, present in the tree) and `120000 blob … corpus/knowledge/odd.md`
   (target `S1244-target.md`, absent → dangling). K11 correctly rejects the weaker remedy: a "skip 120000" variant scores
   `19/21` with K11 `exit=0 ids_cited=1` — skipping still hides the `d11` citation, so the false green survives.
   F2's wording offers "skipping `120000` (or resolving it inside the tree)"; only the second closes the route, and the
   counter enforces that. Worth stating so the implementer does not take F2's first option.
4. **K12's outside registry is outside both the lane and the fleet dir — CONFIRMED.** Symlink target
   `<scratch>/outside/SOURCES.md`; fleet dir `<scratch>/fleet`; `os.path.commonpath([fleet, target]) == <scratch>`.
   Base reads it through `open()` → `ids_cited=2 ids_resolved=2 dangling=0` exit 0 (F5 false green).
5. **The toplevel check in `main()` — present and correct** (v1 lines 323–326, before revision resolution):
   `git -C a.root rev-parse --show-toplevel`, `realpath`-compared, exit 2 on mismatch, `run()` strips `GIT_*`.
   Verified: the lane root passes; a subdirectory root exits 2. It guards the *counter's* `--root` only, independent of K14.
6. **A correct fix can pass all 21 — CONFIRMED, no contradiction between cases.** An independent reference fix
   (registry HTML-comment stripping; setext H2 ends the section; registry realpath containment; `ls-tree -r -z` with
   mode+sha and in-tree symlink resolution via `cat-file blob`; revision-mode toplevel guard; in-lane symlink-dir
   following) scores `21/21 met=True` with `P6 ('66','66')`, `EXIT=0`. So the 21 expectations are jointly satisfiable.
7. **Base control reproduces exactly:** `13/21 met=False EXIT=1` at `--revision fd6303c`, failing
   `K8,K9,K10,K11,K12,K13,K14,P6` — identical set at `--seed 59` (as `controls/base-c2-resolver-cases.txt`) and
   `--seed 7`; the four structural preconditions above are stable across seeds.
8. **The 21 cases alone reject the six round-58 cheat classes** (measured with the c58 mini-stub controls):
   `const_green 1/21`, `blanket_dangling 0/21`, `fence_drop 11/21`, `always_exit_one 10/21`, `tally 54/54 → 13/21`,
   `tally 66/66 → 14/21`. Only the **fixture-content-keyed** class (H1) passes.
9. **C2↔C3 separability for P7 holds:** the real lane's `corpus/SOURCES.md` has no `<!--`, no bare `---`/`===` line, and
   `find corpus -type l` is empty, so the seven fixes cannot move the real-lane measurement (108/108 green at base and
   with the fixed tool).

## RESIDUAL RISK / GAPS

- P6 reads a printed tally (disclosed since round 58): a tool may print `selftest: 66/66`. The 21 behavioural cases are
  the real defence; the in-flight 13 controls are the intended guard against a canned tally.
- H1 means the frozen predicate is *not* a proof against a tool that behaves correctly only inside gate fixtures. Until
  the marker is randomized, an evaluator must not read `21/21` as "the real lane is fixed".
- In-flight drift: the 768-line file changes the selftest substrate (controls are patched variants of the base tool).
  Re-run the counter against the *committed* revision once that port lands; I did not run it.
- Reproduction recipe (all read-only on the lane; scratch under `/fast/scratch/hyaku/kake-r59/ReviewerC2Counter`,
  deleted after use): base control = `python3 -B .ufo/waves/round-59/c59_resolver_cases.py --root <lane>
  --revision fd6303ce5c14b3f892dec586297a942ab6e4193b --work <scratch> --seed 59`; H1 = the same command with a
  candidate tool whose seven route fixes are gated on `example.invalid` in the registry text.
- Tooling: no installs or upgrades were needed; no package manager was run.

VERDICT: the committed v1 C2 counter is faithful to its four fixtures, its base control reproduces 13/21 and a correct fix reaches 21/21, but it is defeated by a fixture-keyed tool — randomize the `example.invalid` row marker and add that control to the gate selftest (H1) before any C2 claim is measured.
