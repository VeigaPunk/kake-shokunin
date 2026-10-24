# KakeR32.CriticC2Scope — does C2 fit its routed item and the freshness axis?

Verdict: the C2 build is real and matches routed item 5's literal wording. Two things are overstated:
the "3/3" framing and the "freshness" label. The entry's disclosure also misses part of the gap, which
is a fixable defect. Retaining the two blobs is a provenance and re-checkability repair (the after
state is real), but it is not drift detection, and the counter cannot tell it apart from a hollow
commit. Advisory only; no admission or verdict on the round.

## What I read
- Declaration: SCORECARD.md:1009-1038 at 285abcad. Axes: /home/vgpnk/Projects/shokunin/AXES.md:14.
  Freshness is defined as "skill claims re-verified against live surfaces; stale items flagged or fixed".
- Routed item 5: corpus/lessons/round-31-verifier-spotcheck.md:175-176 says "retain or pin it so a
  fresh session can re-check". The same closure (line 96-97) frames the gap as "render.yaml facts".
- Entry at 285abcad: corpus/knowledge/render-web-services.md:50-90. S062 row: corpus/SOURCES.md:70.

## Finding 1 — the claim matches item 5, but the entry's disclosure undercounts the remaining gap (fixable)
- Item 5 names only render.yaml. C2 retains render.yaml and the Dockerfile, which is more than asked.
  Pinning by blob id already existed at base (entry line 53 named d17ab7e5), so the new part is retention.
- The entry's new closing note (lines 88-90) names one remaining external dependency: "the sentence
  about the server's allow list". The render.yaml section actually rests on two unretained files in six places:
  - `apps-sdk/src/server.ts` (blob 649726df…): line 62 (health check, `server.ts:193`), line 65
    (port and host 0.0.0.0, `server.ts:14`, `:272`), line 66 (allow list), and line 72 (the
    correction that says the server binds 10000, `server.ts:14`). That is 4 sentences, not 1.
  - `.dockerignore` (blob d650445a…): line 61 ("starts with `*` and re-admits only `apps-sdk/` …
    `marketplace/`") and line 74 (correction, "starts with `*`"). This file is not retained and not disclosed.
- Count over the ds4cc-dependent bullets (lines 58-67 and 72-74, 13 in all): 7 can now be fully
  re-checked from lane bytes (lines 58, 59, 60, 63, 64, 67, 73); 6 still need the external clone.
  The honest after state for item 5's outcome ("a fresh session can re-check") is 7/13, not "done".
- I checked the cited facts against `git show 1fbdb8ed:` and they hold: server.ts:14 reads PORT with fallback
  3000, :193 is GET /health, :272 listens on 0.0.0.0; `.dockerignore` line 1 is `*` with `!apps-sdk/…`
  and `!marketplace/…` re-includes; render.yaml lines 2-20 match the cited line numbers. So the gap is
  re-checkability, not wrong content.
- Smallest correction: retain server.ts (649726df) and .dockerignore (d650445a) under the same directory and
  add them to S062. Or amend lines 88-90 to list all 6 dependent sentences. The second option is narrower.

## Finding 2 — "freshness" fit is weak; this is provenance, not drift detection (tradeoff for the judge)
- AXES.md:14 asks for claims re-verified against live surfaces. The live surface here is the operator's
  ds4cc-marketplace repo. C2 copies a frozen snapshot, and the S062 scope cell says it is "not a statement about
  … any later commit". Nothing in the claim, the entry or the counter compares 1fbdb8ed with the current head.
- I ran that comparison (read-only, `git show`): ds4cc HEAD and the local origin/main are both 1fbdb8ed2dfe2…
  (2026-10-21), and render.yaml, Dockerfile, server.ts and .dockerignore have the same blob at HEAD and at
  1fbdb8ed. So nothing is stale today. But that re-verification, which is the actual freshness step, is not in the claim.
- The drift hook got weaker during the round. At 2f2f12d, the S062 recheck cell was "on ds4cc-marketplace render.yaml
  or Dockerfile change". At 285abcad it is "90d", changed to satisfy census E09 (scripts/sources-census.sh:28
  accepts an ISO date, NNd or a symbolic cadence). The entry's own `recheck:` header (line 3) covers only the Render
  Docs pages. So no artifact now ties a recheck to a ds4cc change.
- Precedent cuts both ways. Kake has scored sourcing claims as freshness before (round 28 C2, round 30 C2,
  round 31 C2: new rows opened this round). The condition "opened 2026-10-22" follows that convention. But
  those rounds opened new external sources. S062 re-registers bytes the entry already read in round 31.
- Smallest correction: put the drift step into the claim. Record one before-to-after on "ds4cc HEAD equals the
  retained blobs, checked on date D". Then restore an event trigger (for example in the entry's recheck header). Otherwise
  the judge should file C2 under calibration or operability (re-checkability) rather than freshness.

## Finding 3 — "0/3 to 3/3" overstates; the counter scores a hollow commit 3/3 (tradeoff, disclose)
- The three conditions are facets of one act (copy, register, cite), and condition 3 depends on condition 2's
  row id. The before value of 0 holds by construction: the paths and the row cannot exist before the repair. The ratio
  presents one yes-or-no repair as a three-step gain.
- Counterexample (sandbox, base a0b0dff plus one commit): the two blobs copied to unrelated paths
  `scripts/fixtures/unrelated/{a,b}.txt`, a row
  `| S099 | ds4cc-marketplace 1fbdb8ed | x | x | x | x | x | x | 2026-10-22 | x | x |`, and the entry gets the line
  "S099 is unrelated to this entry." The counter returns met 3. Condition 1 is path-agnostic, condition 2 checks only
  two substrings and a date, and condition 3 accepts any token match.
  - Commit `ea1050dda6c86eb81e24642dcda79eec37753c24` in /fast/scratch/hyaku/kake-r32/w1/CriticC2Scope/clone
  - Output: /fast/scratch/hyaku/kake-r32/w1/CriticC2Scope/hollow-count.json
- In fairness, condition 1's byte identity by blob id is strong, and the landed commit is not hollow: the paths
  sit under the declared directory, the row and anchor are real, and the entry cites S062 twice in the retention note.
- The declaration's "Truth step (routed item 4): byte identity is checked by blob id" redefines item 4.
  Item 4 asks for truth-sampling of entry sentences against their source. Blob identity proves the copy is
  faithful, not that the sentences are true. Nothing in C2 sampled sentence truth (I spot-checked lines 58-66
  and 72-74 above; the facts hold).
- Smallest correction: report C2 as one repair (retained and cited: yes) with the disclosed 7/13 re-checkable
  coverage, or pin condition 1 to the declared path and condition 3 to a sentence in the render.yaml section.

## Commands run (exit codes)
- `git show 285abcad:corpus/knowledge/render-web-services.md | grep -n -iE 'ds4cc|server\.ts|S062|…'` → 0
- `git ls-tree -r 285abcad -- .ufo/waves/round-32/`; `git show 285abcad:.ufo/waves/round-32/c2_retained_count.py` → 0
- `git diff --stat a0b0dff 285abcad`; `git diff 2f2f12d 285abcad -- corpus/SOURCES.md` → 0 (diff is the S062 recheck cell only)
- S062 cells parsed at 2f2f12d and 285abcad (11 cells each; cell 9 changed) → 0
- In ~/Projects/ds4cc-marketplace: `git show -s HEAD|1fbdb8ed|origin/main`, `git show <rev>:<path> | git hash-object --stdin`
  for 4 paths, `git show 1fbdb8ed:{.dockerignore,apps-sdk/src/server.ts,apps-sdk/Dockerfile,render.yaml}` → 0
- `grep -n E09 scripts/sources-census.sh` (fleet repo, read only) → 0
- Sandbox clone at a0b0dff, hollow commit, then `python3 -B …/c2_retained_count.py --rev ea1050dd --repo <clone>` → 0, met 3
- `python3 -B .ufo/waves/round-32/c2_retained_count.py --rev 285abcad` → 0, met 3.
  Counter sha256 48126fc5b42db1e210bcc2c24c7cb699207ee79b0683bf47cb0c8f94c3f3e22c.

## Not verified
- I did not rerun the counter at a0b0dff or 2f2f12d. I read the committed receipts instead (met 0 and met 3).
- I did not check the ds4cc remote. origin/main is the local tracking ref, not fetched, by bound.
- I did not run the sources census on 285abcad. I did not check the Render Docs (S057-S060) sentences.
- No tools installed or updated. No network requests. No lane file written except this report.
