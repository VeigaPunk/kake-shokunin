# ScribeMistakeMine — round 37 mistake rows

## Findings
Axes: operability and freshness. Drafted four `## Mistakes` rows from the non-author round-37 closure disagreements: predicate-consequence override, dead-seat substitution, control/build ordering, and unpinned post-measurement tool identity. Full row text is in the sandbox draft; the first two and last rows name concrete checks that should reject the documented old state, but those checks were not implemented or run by this seat.

Provenance: `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-37-verifier-spotcheck.md` lines 31–43, 59–71, 113–115, 134–150; corroborating timeline `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-37/w2/ReviewTimeline.md` lines 21–24. Receipt data: `.ufo/waves/round-37/verification/control-CtlC1Shortcut-followup.json` lines 2–11 and `.ufo/waves/round-37/verification/postfix/robots-selftest-137-on-postfix-tool.json` line 1. QUALITY (j) says its check was “none yet” (`corpus/QUALITY.md:926-930`).

## Timeline check (executed)
The checker uses the receipt’s Git add-commit committer timestamp and the wave’s `w1-dispatched-at.txt` timestamp. Source corroboration command: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; timeout 15s git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --diff-filter=A --format='%cI %H' -- .ufo/waves/round-37/verification/control-CtlC1Shortcut-followup.json` → `2026-10-23T00:29:45-03:00 ccc3b2b9c16dc2278bca5009792d5c12ec569b74`; dispatch file → `2026-10-23T03:22:30Z`.

Red command (exit 1): `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r38w1/ScribeMistakeMine/tmp; prlimit --as=4000000000 timeout 20s python3 /fast/scratch/hyaku/kake-r38w1/ScribeMistakeMine/timeline_check.py /home/vgpnk/Projects/shokunin/kake-shokunin /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-37 .ufo/waves/round-37/verification/control-CtlC1Shortcut-followup.json`

Observed: `receipt_added_at=2026-10-23T00:29:45-03:00`; `w1_dispatched_at=2026-10-23T03:22:30+00:00`; `dispatch_minus_receipt_seconds=-435`; `FAIL: control receipt was committed after build dispatch`.

Green fixed-layout command (exit 0): `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r38w1/ScribeMistakeMine/tmp; prlimit --as=4000000000 timeout 20s python3 /fast/scratch/hyaku/kake-r38w1/ScribeMistakeMine/timeline_check.py /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r38w1/ScribeMistakeMine/fixed/round-37 .ufo/waves/round-37/verification/control-CtlC1Shortcut-followup.json`

Observed: `receipt_added_at=2026-10-23T00:29:45-03:00`; `w1_dispatched_at=2026-10-23T03:30:00+00:00`; `dispatch_minus_receipt_seconds=15`; `PASS: control receipt was committed before build dispatch`.

## Artifacts and bounds
- Draft rows: `/fast/scratch/hyaku/kake-r38w1/ScribeMistakeMine/mistakes.md` — SHA-256 `8c4f1027d2aa46b1bae7f279c27bef73e5b133aff5c53b70c2d8154d8ad5125a`.
- Timeline checker: `/fast/scratch/hyaku/kake-r38w1/ScribeMistakeMine/timeline_check.py` — SHA-256 `3ed428213a5f02c5ce48e8be3e3a12640be6098769074aa41b967e58b67e0814`.
- Fixed dispatch fixture: `/fast/scratch/hyaku/kake-r38w1/ScribeMistakeMine/fixed/round-37/w1-dispatched-at.txt` — SHA-256 `b2e645ecb830a8e7d5f7099b2e9b93a4d7947aeab0adfec894627cafe61721ca`.
- Touched surfaces: those three sandbox artifacts and this report only; no product code or lane state changed. No tools installed. No round-38 counter, build, tests, or other gate run. The timeline script tests one supplied receipt path; its green fixture is counterfactual, and the dispatch timestamp is not authenticated by the script.
- No access to either forbidden `/fast/scratch/hyaku/kake-r38/` tree. A lane round-38 directory listing incidentally displayed the `sealed/cases.json` entry; its contents were not opened/read/searched/stat’ed and no counter was run.
