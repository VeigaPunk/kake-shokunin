# ScribeRecord — round 81 drafts

**Verdict:** five drafts are written and every base-state number in them is quoted from a committed
receipt with `file:line`; after-state values are left as explicit `⟨FILL …⟩` markers because no
after-state existed when this seat ran — nothing here is a claim that C1 or C2 met.

## Findings

1. **F1 — the frozen C1 counter reproduced the round-80 defect; already corrected mid-wave, before
   any after-state.** `c81_defect_queue.py`'s `p_r80_4` selected *every* results row as settled
   (frozen form: `settled = [r.get("name") for r in (results.get("results") or []) if isinstance(r, dict)]`),
   while contract §C1 and `make_accounting.py:36-38` count only non-empty output. Any empty-output
   seat therefore made the accounting record and the counter disagree (`settled_total`,
   `settled_attack`, `share`), so R80-4 would open on honest bytes — and could print a green share the
   contract calls red when the two populations straddle 0.25. The wave's `ScribeLesson` seat found it
   first; amendment 1 A1
   (`.ufo/waves/round-81/amendments/amendment-1.md`) landed at `0a27045e4b1b18ae521c9be508429262fdf993ca`
   before any after-state. Verified in the current bytes: `c81_defect_queue.py:197-199` now filters
   `(r.get("output") or "").strip()`, and the selftest gained `r80-4-empty-seat-excluded` and
   `r80-4-empty-seat-counted-opens` (`controls/c81-selftest-c1.txt:11-12`), tally `15/15` at `:17-18`.
   The three re-cut receipts are disclosed; base and junk verdict lines are unchanged
   (`controls/base-c81-defect-queue.txt:8-9`, `controls/ctl-c81-junk-queue.txt:8-9`, both byte-identical
   per the amendment). Reported here as closed-by-amendment, not as an open defect — this seat reached
   the same conclusion independently from `make_accounting.py:36-38` vs the frozen counter.
2. **F2 (open, low) — the C2 fetch-time floor is lexical, not temporal.**
   `c81_capture_audit.py:87` compares `fetched < ROUND_FIRST_DAY` as strings after an RFC 3339 shape
   check (`:33`). Offsets are therefore ordered by digit, not by instant: `2026-11-03T20:00:00-05:00`
   (instant 2026-11-04T01:00Z) is rejected as predating the round, and `2026-11-04T00:30:00+09:00`
   (instant 2026-11-03T15:30Z) is accepted. A `Z`-form capture (what the seat is told to write) is
   unaffected; the counter cannot tell a valid offset form from an early one.
3. **F3 (open, low; wording) — "byte-for-byte" is implemented as line-normalised equality.** Contract
   §C2 says the audit's stdout "equals the committed audit receipt byte-for-byte"; `evaluate` compares
   `normalise(stdout) == normalise(receipt)` (`c81_capture_audit.py:155`, `normalise` at `:55-56`
   strips trailing whitespace and drops blank lines). The implemented predicate is strictly weaker than
   the sentence the round will quote.
4. **F4 (open, medium; evidence scope) — `capture-expectations.json` is never read by the C2 counter.**
   `grep -n capture-expectations c81_capture_audit.py` → no reference. `surfaces` is
   `len(manifest["checks"])` and the allowlist is `manifest["allowlist"]`, both written by the capture
   seat: a manifest declaring one surface, or a different surface set, still meets `surfaces >= 1` as
   long as its own receipts verify, and the frozen expectations file cannot open the item. The
   contract's predicate is worded exactly this way, so this is a *stated-claim vs evidence* gap
   (the README/province drafts therefore describe what the counter re-derives, not an equality with
   the expectations file) — the manifest-versus-expectations join is `ReviewC2`'s question 5, not
   something this counter decides.
5. **F5 (open, low; naming) — two names for the after receipts.** The contract, this seat's spec and
   the verification block name `controls/after-c1.txt` / `controls/after-c2.txt`; the round-81
   lesson's settlement paragraph names `controls/after-c81-defect-queue.txt` /
   `controls/after-c81-capture-audit.txt` (`corpus/lessons/round-81.md:225`). No receipt exists under
   either name yet, so nothing is inconsistent on disk — but the L1 should pick one pair and make the
   lesson, the contract's control list and the report agree, because the C1/C2 evidence pointer is
   exactly what the closure will read. The drafts use the contract's pair and the log draft's routed
   bullet records the divergence.
6. **Observation — no sentinel seat this wave, and the carrier must commit the instruments.**
   `w1-spec.json` roles: executor 4, reviewer 4, scout 2, scribe 2, critic 1, mutation-tester 1,
   connector 1 (15 seats; requested attack 6/15 = 40.0 %). No sentinel; the round touches no external
   state (capture is GET-only, nothing published), so the contract does not require one. Integration
   note that follows from `materialise` (`c81_defect_queue.py:87-101`): the after-state is only green
   at a revision that *commits* `w1-spec.json`, `w1-results.json`, `w1-accounting.json`,
   `seat-failures.json`, `corpus/lessons/round-81.md`, `junk-tree.json`, `junk_tree_build.py`,
   `capture/manifest.json` and `controls/after-c2-audit.txt` — `git show` failures are skipped
   silently, so a missing file reads as that item's open message, not as an export error.

## Independent checks this seat ran (read-only)

| Check | Command | Result |
|---|---|---|
| Registry arithmetic behind R80-1/R80-3 | `git show HEAD:corpus/SOURCES.md \| python3 -c '<row parse>'` | `rows 191`; `rfc9110.txt 3 ['S028','S033','S453']`; `rfc9110.html 3 ['S010','S088','S433']`; `S453 line 200` — matches the base receipt's `rows=3` / `rows=3` (`controls/base-c81-defect-queue.txt:2,4`) |
| Constants arithmetic behind R80-2 | `cat .ufo/waves/round-80/controls/ctl-c80-constants.txt` | `12+12+11+12 = 47` failures over `4 × 12 = 48` slots; `const_echo 11/12`; `constants_failed=4/4` — matches `:3` |
| Audit tool untouched since base | `git diff --stat 2e119255..HEAD -- scripts/header_audit.py` | empty output, rc 0 |
| Amendment 1 landed before after-state | `git log --oneline -3` at lane HEAD `bec3ecf7` | `bec3ecf7 round-81: disclose the one receipt rewrite from amendment 1`; `0a27045e round-81: amendment 1`; `a77b8a19 round-81: freeze contract…` |
| C1 selftest receipt current | `cat -n .ufo/waves/round-81/controls/c81-selftest-c1.txt` | `15/15` at `:17`, `exit=0` at `:18` |
| C2 expectations file unchanged by A2 | `python3 -c '…capture-expectations.json…'` | `grounding.status` still reads `§15.5.4/§15.5.5`; the amendment states the bytes stay frozen and carries the correction |
| Lesson correction rows carry the tokens R80-1/2/3 require | read `corpus/lessons/round-81.md:72,74,76` | `:72` names `corpus/SOURCES.md:200 for S453` (line 201 is blank, `## Paths` at 202); `:74` carries `constants_failed=4/4, 47/48, 11/12`; `:76` carries `rfc9110.txt rows=3` and `rfc9110.html rows=3` — the same strings the base receipt's open lines print (`controls/base-c81-defect-queue.txt:2-4`) |

No network call, no git mutation, no scratch tree: every check was a read or a pipe, so there is
nothing under `$HYAKU_SCRATCH/kake-r81/ScribeRecord/` to delete. No production file, counter, receipt
or contract was touched; both control receipts I quote are the current committed bytes.

## Drafts (under `.ufo/waves/round-81/w1/ScribeRecord/`)

| File | Shape matched | What is complete | What the L1 must fill |
|---|---|---|---|
| `scorecard-block.md` | `## Round 81 — measured claims (author-side; closure owns admission)`, 5-column claim table, 5-column move log, `### Capabilities acquired in round 81` (4 columns), stated-limits paragraph | contract + amendment commits, base standing, wave shape (15 seats, requested 6/15 = 40.0 %), base C1/C2 receipt lines, selftest tallies with line pointers, junk-control line, capability row text, amendment-qualified limits | carrier revision; `controls/after-c1.txt:8` and its `exit=`; `controls/after-c2.txt`; settled share from `w1-accounting.json`; the round's own freshness-sweep receipt if one was run; registry/`W04` after-counts |
| `log-entry.md` | `## Round 81 — 2026-11-04 (hyaku run 15; attempt 1; Linux host; claims frozen before any seat ran)` with the round-79/80 bullet set | frozen contract + amendment 1, motivating evidence (R80-1…R80-6 restated with their measured deltas), wave shape, C1 mechanism and base receipt, C2 mechanism and base receipt, S454/S433 Gate facts (access times, bytes, sha256, quote spans, recheck/used-by changes, rejected §15.5.4 anchor, S088 overlap, `merge/kake` collision), the three mined mistakes with lesson line pointers, routed items, "not done" | carrier; after receipts; per-surface audit outcome; registry 191 → N and the `W04` after-count; the receipt-name choice (F5); any further routed wave finding |
| `readme-rows.md` | `| Area | Entry | Coverage |` rows | the C2 instrument row (paths, what re-derives, what it refuses) and the S454 status-semantics row naming `corpus/knowledge/response-header-expectations.md` | nothing numeric beyond the paths; insert at the end of §Coverage map (or a `## Coverage — round 81` table, per the file's convention) |
| `province-append.md` | `## Round 81 …` short section (round-29-onward style) | the chain as a Core instrument (base control `surfaces=0 met=false`, selftest 12/12, five mutants), S454 as the verdict boundary with A2's anchors | nothing numeric; keep after the existing `[r80-correction]` paragraph |
| `quality-criterion.md` | `## Round 81 criterion — …` plus one bolded bullet (the file's post-75 convention; also renders as one row of the main table) | admit/reject text (committed capture tree, digest/length/status/fetch-time/allowlist re-derivation, audit-output equality, S454 absence handling), grounding to this round's lesson, counters and the R80-5/R80-6 class it closes | nothing; the `corpus/lessons/round-81.md §Mistakes/§Gate` pointers resolve once that lesson exists |

Draft convention: every after-state slot is `⟨FILL <receipt:line>⟩` with the predicate the line must
satisfy, so integrating means copying receipt bytes, never transcribing this draft.

## Stated limits of this report

- No after-state existed at 08:5xZ (no `capture/`, no `w1-results.json`, no S454 registry row, no
  `controls/after-c1.txt`/`after-c2.txt`), so no C1/C2 verdict is asserted anywhere in the drafts.
  `corpus/lessons/round-81.md` appeared while this seat ran (untracked at `bec3ecf7`); its Correction,
  Gate, Mistakes and Limits sections are used as committed-prose sources with line pointers, and the
  drafts keep every counter value as `⟨FILL⟩` because the lesson's own settlement paragraph says the
  carrier measurements are appended by the L1. F2–F4 are code-level readings of the frozen counters,
  not measurements of the round's data.
- The drafts quote `.ufo/waves/round-81/controls/` bytes as they stood at this seat's run; the
  amendment re-cut one receipt (the C1 selftest) and this report uses the re-cut version. If the L1
  re-cuts any further receipt, the `file:line` pointers in the drafts must be re-checked at
  integration.
- `S454`'s admission, quote and registry line are the `ScoutSources`/`ScribeLesson` seats' evidence;
  this report only corrects the anchor prose the drafts would otherwise have copied from the contract.
