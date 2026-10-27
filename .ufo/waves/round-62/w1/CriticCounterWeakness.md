# Counter false-green review — CriticCounterWeakness

Axes reviewed: token-presence false greens, path omission, revision substitution, and stale-text acceptance. Advisory only; no lane claim, counter, criterion, or score was changed.

## Evidence

- Frozen counter `.ufo/waves/round-62/c62_calibration.py` lines 8–16 fixes base revision and five queried paths. Lines 19–24 run `git show <rev>:<path>` against the supplied root and return empty text on any failed blob lookup; lines 26–43 evaluate only blobs at the supplied revision.
- Lines 31–38 are substring checks, not semantic validation: a single line containing both `S432` and `Disagree` counts; the correction checks for the exact quote fragment plus `S432 §3.6` and `Round-62 correction`; QUALITY checks literal `substantive located quote` and lesson filename; lesson gate checks only presence of `## Gate`, `S432`, `Agree`, and `Reject`; source row checks `| S432 |` anywhere.
- Retained verifier spot-check `.ufo/waves/round-61-verifier-spotcheck.md` lines 32–36 says S432 was admitted but its generic lead-in was rejected, leaving an admitted row without quote grounding. Retained S432 source body lines 6151–6154 contains the substantive §3.6 passage about X-Content-Type-Options requiring checking response Content-Type against request destination.
- Exact integrity command: `sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/c62_calibration.py` → `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d` (matches frozen hash).

## Counterexample / finding

Strongest false-green is adversarial committed text: once all four gates are enabled, the measured revision can retain the original S432 disagreement yet pass by placing every required phrase in unrelated prose. In particular, an unrelated correction paragraph can contain the checked quote, citation, and label without actually correcting the knowledge entry; unrelated QUALITY prose can contain the two checked tokens; a lesson gate can contain all four words without codifying the dispute. A source row token anywhere similarly does not prove the row remains valid. This is a real token-presence limitation, but no scratch run was made and no observed false-green output is claimed.

Path omission is partially handled: missing required blobs yield empty strings and their corresponding checks fail. The spot blob alone has an explicit missing diagnostic (return 2); missing other blobs silently behave as failed checks (normally exit 1). Revision substitution is structurally permitted by `--revision` (lines 45–50), so output is only meaningful for the intended committed revision; the counter does not enforce that revision equals base or the integration commit. It does correctly use committed Git blobs, avoiding uncommitted working-tree text. It counts any matching line, so duplicating the matching row could inflate disagreements, but does not produce a false green while gates remain absent.

## Impact and smallest safe correction

Impacted axis: calibration-counter validity (token-presence / provenance); potential false-green undermines evidence that the disagreement was actually learned. Do not change the frozen predicate after score. For a future counter version only, anchor checks to the intended sections/rows and require the correction/criterion text to occur in their designated section, and record/check the expected measured revision externally; validate lesson gate fields as structured content rather than independent tokens. Current round's intended success must therefore be corroborated by manual committed-diff inspection, not inferred solely from `met=true`.
