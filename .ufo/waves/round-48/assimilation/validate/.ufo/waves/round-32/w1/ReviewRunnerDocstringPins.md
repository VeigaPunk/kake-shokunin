ReviewRunnerDocstringPins — C1 consistency, runner docstring probe statements
Lane rev reviewed: 285abcad632e3c1c57bb402232e7d218054db383 (files read via `git show`; working tree identical for both scripts).

Commands run (all read-only, lane repo):
- `git show 285abcad:scripts/citing_set_selftest.py` lines 1-140 — exit 0
- `git show 285abcad:scripts/citing_set_hostile_selftest.py` lines 1-130, 210-232 — exit 0
- `ls scripts/fixtures/citing-set-hostile/` + parsed every `hostile.json` — exit 0;
  six specs: P1(N1), P2(N2), P3(N3, tmpdir_in_victim), P4(N5), P5(N6), P6(gap "m3",
  tmpdir_in_victim, case_json setup=[git_commit, git_init], reason_contains "needs an earlier 'git_init'")
- `grep` in runner: load-time guard at scripts/citing_set_selftest.py:362-363
  (`if step["op"] == "git_commit" and not initialized: raise ValueError("... needs an earlier 'git_init'")`),
  apply-time re-check at :488-490 (`RuntimeError("git_commit needs the repository created by git_init")`)
- selftest reason check: scripts/citing_set_hostile_selftest.py:218-222 — substring match on the
  runner's per-case failure `reason`; docstring claim ("must contain it") is accurate.

FINDINGS (stale or newly-wrong sentences in scripts/citing_set_selftest.py docstring)

1. Line 83 — WRONG. "The hostile specs probe five routed shapes (N1, N2, N3, N5, N6)."
   After P6 there are six specs and six probed shapes; m3 is itself a round-31 routed item
   (routed item 2), so even "five routed" undercounts the routed set.
   Suggested: "The hostile specs probe six shapes: the five round-31 routed gaps (N1, N2, N3,
   N5, N6) plus the round-32 m3 guard (P6: a ``git_commit`` step listed before ``git_init``,
   pinned to the load-time refusal by ``reason_contains``)."

2. Lines 84-86 — borderline stale, still literally true. "...are not separately probed: a
   runner without them still passes the hostile selftest and the round-31 C1 counter."
   The claim survives P6 (P6's refusal fires when case.json is loaded, before any Git command,
   so pins remain unexercised), but the sentence names only the superseded round-31 counter;
   the operative round-32 counter `.ufo/waves/round-32/c1_m3_probe.py` exists and is likewise
   pin-agnostic.
   Suggested: "...are not probed even by P6 (its refusal happens at case.json load, before any
   Git command): a runner without them still passes the hostile selftest and the round-32 C1
   counter (``.ufo/waves/round-32/c1_m3_probe.py``)."

3. Lines 90-91 — now an understatement, not false. "``scripts/citing_set_hostile_selftest.py``
   checks these refusals against the hostile specs..." Since P6 the selftest also checks which
   layer refuses (``reason_contains``), not merely that it refuses; the runner docstring nowhere
   mentions the two-layer guard (load-time :362 vs apply-time :489) that this key distinguishes.
   Suggested: append "; a spec may additionally pin the reported failure reason via
   ``reason_contains`` (P6 pins the load-time guard, distinguishing it from the apply-time
   re-check)."

VERIFIED NOT STALE
- Line 74 containment bullet "a ``git_commit`` step with no earlier ``git_init``" covers both
  P3 (no git_init at all) and P6 (git_init listed later). Correct.
- Lines 57-62 git_commit op doc; lines 86-88 os.pathsep/--tmpdir sentence. Unaffected by P6.
- Hostile selftest docstring is consistent: reason_contains documented at :38-43 and in the
  pass criteria at :52-55; implementation (:218-222) matches "must contain it" (substring, not
  equality). Nits only: header still says "(round 31)" though the file now implements a
  round-32 key, and the spec example shows `"gap": "N1"` while P6 uses `"gap": "m3"` — both
  illustrative, defensible.

NOT VERIFIED: did not execute the selftest or counters (review-only seat); staleness of
counter behavior claims (finding 2) is by code reading, not a run.
No tools installed. No lane files mutated except this report.
