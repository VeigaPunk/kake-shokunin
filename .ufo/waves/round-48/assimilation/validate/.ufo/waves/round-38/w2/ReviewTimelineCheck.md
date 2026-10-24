# W2 ReviewTimelineCheck — timeline_check.py and the "58 s before dispatch" claim

Axes: operability (does the check re-run and discriminate), freshness/authenticity (are the
timestamps it compares real and attributable). Scope: tip adab4c7e; sandbox clone
/fast/scratch/hyaku/kake-r38w2/KakeR38.ReviewTimelineCheck/clone @ adab4c7e (lane untouched;
no tool installs needed — python3/git only).

## Verdicts

1. **"Control receipts landed 58 s before wave-1 dispatch" (LOG.md:1540,
   corpus/lessons/round-38.md:69-70) — holds (reproduced), with an authentication caveat (3).**
   Re-run, exit 0, three distinct receipt paths, all identical:
   `python3 -B .ufo/waves/round-38/criteria/timeline_check.py $C $C/.ufo/waves/round-38
   .ufo/waves/round-38/verification/control-{base-af43a50f,CtlStdlibV2,CtlTrivial-junk}.json`
   → `receipt_added_at=2026-10-23T01:28:54-03:00`, `w1_dispatched_at=...T04:29:52+00:00`,
   `dispatch_minus_receipt_seconds=58`, `PASS`, exit 0 each. All 12
   `verification/control-*.json` have add-commit cd=ad=04:28:54Z (2dab7f3) — verified per-file
   with `git log --diff-filter=A -1 --format='cd=%cI ad=%aI'`; result is path-independent.

2. **What time the check reads: committer time, not author time — confirmed by probe.**
   timeline_check.py:31 uses `--format=%cI`. Probe in sandbox: file committed with
   GIT_AUTHOR_DATE=2020-01-01, GIT_COMMITTER_DATE=2021-01-01 → check printed
   `receipt_added_at=2021-01-01T00:00:00+00:00`. For the green case this is moot: 2dab7f3 has
   ad=cd=01:28:54-03:00, so the verdict survives either reading. Note the lane does rewrite
   history (b0ab7f6 ad=01:04:40 cd=01:14:15; r37 dispatch file 528a6d0 ad=00:29:45 cd=00:36:51),
   so %cI-vs-%aI is a live distinction here — the landed green case is insensitive to it.

3. **"w1-dispatched-at.txt authenticated?" — no; self-attested, committed after the fact.
   Claim precision is overstated to the second, substance corroborated.**
   - Content `2026-10-23T04:29:52Z` (sha256 54c2d11c…cdb1), unsigned; added to git only at
     145a646 (cd=04:40:21Z), 10.5 min AFTER the dispatch it attests, by the same party making
     the ordering claim. The checker (`read_text` → fromisoformat) cannot authenticate it; a
     backdated file passes silently. Same pattern in r37 (528a6d0, 14 min late).
   - Corroboration (working-tree mtimes, unchanged files retain creation mtime through later
     jj snapshots): w1-dispatched-at.txt mtime 04:29:52.376Z — matches content to the second;
     w1-dispatch.json + w1/swarm-registry.json mtime 04:29:36Z; earliest wave-1 seat artifact
     w1/ScoutPythonJson.md mtime 04:31:55Z. Subagent outputs cannot precede dispatch, so
     dispatch is pinned to (04:28:54, 04:31:55] independently of the file's own text. The
     exact "58 s" figure rests on the unauthenticated file; "receipts before dispatch" does not.

4. **QUALITY (m) red/green statements (corpus/QUALITY.md:955-958) — hold.**
   - Red: `... timeline_check.py $C $C/.ufo/waves/round-37
     .ufo/waves/round-37/verification/control-CtlC1Shortcut-followup.json` →
     `receipt_added_at=00:29:45-03:00`, `-435`, FAIL, exit 1 — reproduces timeline-r37.txt.
     Honest scope note: this is 1 of 7 r37 control receipts; the other 6 were added at
     00:21:56 (34 s early; e.g. control-CtlC1Junk.json → PASS exit 0, +34). The red case is
     the worst case; QUALITY (m) cites it as a single receipt ("exit 1, 435 s late"), and
     lessons/round-37-verifier-spotcheck.md:38 tells the same story — no misrepresentation.
   - Green: exit 0, 58 s, "three control receipts" — reproduced (see 1); any control-* path
     yields the same because all 12 share one add commit.

5. **The check discriminates and fails closed on bad input — holds.**
   Post-dispatch receipt: `.ufo/waves/round-38/verification/c2-at-3ed8e15c.json` (added
   01:39:18) vs w1 dispatch → `-566`, FAIL, exit 1 (not always-PASS). Naive timestamp
   (no offset) → `timeline-check error: timestamp must include a UTC offset`, exit 2.
   Missing wave dir → exit 2; unknown receipt → exit 2 ("no add commit"). `-1
   --diff-filter=A` takes the LATEST add of the path — conservative direction. Aware-datetime
   arithmetic across -03:00/+00:00 is correct.

## Defects (minor, no verdict flipped)

- D1 receipts/provenance: timeline-r38.txt (sha256 2622ae13…2476) records three PASS runs but
  no repo, commit, wave dir or receipt paths, so the checked invocation is not reconstructible
  from the receipt alone. Harmless here (path-independence, verdict 1) but it is what let my
  first r37 attempt silently mix r37 receipts with r38's dispatch file (exit 0, +4076 s) —
  a wrong invocation still produces a plausible-looking receipt.
- D2 the instrument receipt itself (timeline-r38.txt) landed at 145a646, after the dispatch —
  fine for an instrument, but nothing pins that the receipt predates the round's admission.

## Residual risk / gaps

- mtimes and GIT_COMMITTER_DATE are both forgeable; the 58 s precision is only as strong as
  the dispatcher's honesty plus jj's snapshot behavior (not cryptographic). I did not verify
  jj op-log timestamps (no jj commands allowed in the lane).
- I checked add-commits for control-*.json and dispatch files only; other claim files
  (SCORECARD/LOG edits) were added at tip (01:43:03), after both — consistent, not re-timed.
- Sandbox clone left at /fast/scratch/hyaku/kake-r38w2/KakeR38.ReviewTimelineCheck/clone with
  two probe commits on top of adab4c7e; no lane file other than this report was written.

Statements attacked: (1) 58 s ordering — holds; (2) commit-vs-author time reading — holds
(committer time, green case insensitive); (3) dispatch-file authentication — overstated as
precision, substance corroborated; (4) QUALITY (m) red/green — hold; (5) fail-closed behavior —
holds. LSP/diagnostics not applicable (no language server for this throwaway criteria script;
checks were execution-based, not text-grep-based).
