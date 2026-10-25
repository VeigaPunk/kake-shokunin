# CriticClaimsAdmission

Read-only attack on the admission of C1 and C2 at the revision under attack `a450e43e696d032e3ac308383f6b3394e0c92860`
(lane tip `7ad7db5`; measured revision is a450e43). Every counter/selftest run below happened in its own
`D=$(mktemp -d)` clone of the lane; scratch probes ran in `mktemp -d` + `git init` or in a clone committed with
`-c user.name=selftest -c user.email=selftest@local`. No lane file was edited; this report is my only write.

Re-derived at a450e43 (my runs, not receipts): C1 `tally_mismatches=0 rows_checked=10 met=True` exit 0 (29.6 s);
C2 `8/8 met=True` exit 0. Base controls re-scored under the *final* counter versions: C1 `7/10 met=False` exit 1,
C2 `0/8 met=False` exit 1 — byte-identical to `controls/base-c1-selftally-v2.txt` and `controls/base-c2-quote-truth.txt`.
So the do-nothing control does not reach either target (prompt:426).

## VERSION HISTORY:

`git log --format='%h %s' -- .ufo/waves/round-56/c56_selftally.py .ufo/waves/round-56/c56_quote_truth.py`:

| commit | version | content | ordering |
|---|---|---|---|
| `2d308e8` | v1 | contract + both counters v1 + base controls + retained sources + mirror | before the build |
| `d5afc48` | v2 | C1: Self-test-column command pinning, fixed env, duplicates, helper pinning, anchored tally, nclaims; C2: S367 sha256 pin, 40-char ceiling, verified-at/recheck/cell checks | **the build commit** — three entries, S419/S420 rows, SKILL cells and counters v2 land together |
| `3691e96` | v2.1 | C2 Gate-quote uniqueness, kind/tier/scope/teaches, staged-name absence, page-uniqueness; C1 env/anchored-tally fixes | after the d5afc48 8/8 measurement (contract.md:107) and after every W1 seat scored the counters |
| `a450e43` | — | SKILL gate-registry cells, QUALITY criteria, W1 settlement | after v2.1 → rule precedes the measured after-state |

1. **Attacks `contract.md:5` ("committed together before any build edit").** True of v1 only: v2's implementation landed
   in `d5afc48`, the same commit as the after-state it measures, so the final *implementation* could be shaped against the
   data. The frozen *predicate sentences* did not move (`contract.md:31,55` == `PREDICATE` in both counters). This is the
   class round 55 already mined: `corpus/lessons/round-55.md:96` — "the contract's 'before any build edit' was wrong by
   commit graph (version 2 landed with the build, before any measurement)". Round 56 repeats it in the same sentence.
2. **Attacks the letter of prompt:431-433** ("a rule changed after any seat has scored is not the claim's rule"). W1 seats
   scored the counters under v1 (`w1/CritCheatC1.md` experiments 1-8, `w1/CriticC1Contract.md` A1-A9,
   `w1/CritCheatC2.md` A-D, `w1/CriticC2Contract.md`) and both counters changed twice afterwards. The contract's defence —
   no *claim* had been measured — is a narrower reading of "scored" than the prompt's words. Mitigations that are real:
   the predicate sentences are unchanged; v1's cheats are closed (`CritCheatC1` 5-8, `CritCheatC2` A-D); the base control
   re-scored under v2/v2.1 still fails (I reproduced both). Verdict: admissible under the contract's reading, not under the
   letter; the divergence must be stated, not glossed.

## SIZING:

- **C1** is one value from one command over committed bytes (`c56_selftally.py --root <clone> --revision <rev>`; it reads
  `SKILL.md` via `git show` and runs each command in a clone of the revision). Reproduced 0/10. The universal "every one of
  the ten rows" (`contract.md:28`) is over the enumerated `POP` of ten rows (`c56_selftally.py:63-73`), so §9's universal
  clause bar is met; the after-state's "exits 0 with A == B" clause *is* enforced (`code != 0` → `selftest_failed`,
  `c56_selftally.py:290-292`), not merely asserted.
- **C1 population narrowness.** `SKILL.md:1253-1254` are added by this round with tallies outside `POP`. Both are truthful
  today (I ran them: `c56_selftally.py --selftest` → `47/47`; `c56_quote_truth.py --selftest` under the row's pin
  `3691e9689a03` → `67/67`), so no false after-state — but the claim may only ever be read as "ten rows in population".
- **`link-preview-audit` exclusion is factually right**: 45 fixture directories at the row's pinned `b1cbbc39`, 46 at
  a450e43, selftest `46/46` — directories and cases still answer different questions.
- **C2** is one value from one command, offline, reproduced 8/8; base 0/8. Its after-state carries one clause met at base
  (census exit 0) — disclosed and removed from the predicate (`contract.md:109`).
- **Counter hole, C1 (attacks `c56_selftally.py:216-224`).** `helpers_changed` pins only `*.py` names that exist beside the
  pinned script *at base*; an **added** same-directory module is unpinned. Probe: a scratch repo where `scripts/foo.py` does
  `import json`, plus an added `scripts/json.py` printing `"passedOverTotal": "999/999"` and exiting 0 — the unchanged
  selftest is hijacked and the counter's `parse_tally`/exit check would accept 999. The landed tree adds only
  `scripts/landed_check.py` beside five pinned selftests and my run printed the real tallies, so the landed state is
  unaffected; the guard is incomplete for a junk tree. Smallest correction: also list `git ls-tree` at the revision and
  flag added `*.py` (`tool_added`), beside the already-disclosed "helper outside the pinned script's directory" limit.
- **Counter reachability, C2 (attacks the after-state's "quote-true spans" as provenance).** At the final v2.1 a fabricated
  body passes: in a clone at a450e43 I replaced `sources/S420.html` with a 2173-byte page shell (the entry's own 12 spans
  re-typed, `更新日`, the row's own-URL input, `個別リンクURL`, padding) and rewrote S420's sha256/bytes in `receipts.json`
  (commit `31a849d`) → `8/8 met=True`, exit 0. So the disclosed "substring truth, not support" limit holds at v2.1, not
  only at v1; 8/8 is not a fetch proof. The landed bodies are genuine (hashes below), so this does not falsify the claim —
  it bounds what the predicate may be cited for.

## HARM CHECK:

1. **Operability of the ten rows — not harmed.** `git diff --stat e48354b a450e43 -- scripts/` adds only
   `scripts/landed_check.py`; no selftest or helper was rewritten to match a tally. All ten documented commands run in a
   clone, exit 0, A == B; both pins resolve as commits (`1ae8de5d4dee`, `64c0ce12ffe3…`). Residue, pre-existing and
   disclosed: the two quote-truth **counter** rows exit 1 at the lane tip (`c55_quote_truth` C7/C8 `158 != 155 + 1`;
   `c52_quote_truth` C5 S374 + C8). `c55_quote_truth` passes 8/8 at its own `64c0ce12` (I ran it), so both are
   revision-scoped, not broken; but the rows do not say "at its measured revision", so a reader running them at the tip
   sees exit 1.
2. **Freshness of S367 re-opened — recorded outside the registry and outside the LOG.** The row's cells are unchanged
   (`C3` requires `row[:10] == base[:10]`), so "re-verified 2026-10-25, no drift" is visible only in
   `sources/receipts.json` (`fetchedAt 2026-10-25T22:02:40+00:00`, sha256 `0188de9d…` equal to the round-53 body) and
   `w1/ScoutFreshness.md`. `LOG.md` is untouched at a450e43 and at HEAD (last commit `955e3d7`, round 55;
   `git show HEAD:LOG.md | grep -c 'Round 56'` → 0), while `LEARNING.md`'s freshness observable is "each round LOG entry
   includes a re-verification result". Consequence: `corpus/lessons/round-56.md:59` — "recorded in LOG.md (seven Self-test
   cells)" — is **false on committed bytes** at the revision under attack.
3. **Round-55 coverage-map counter — not harmed.** `c55_readme_index.py --revision a450e43` →
   `index_mismatches=0 knowledge_files=52 coverage_rows=54 met=True`, exit 0. W1's harm risk 6 is closed.
4. **SCORECARD — the round's axis record is absent.** `grep -c 'Round 56' SCORECARD.md` → 0 at a450e43 and at HEAD, while
   round 55 carries `## Round 55 — declared and measured claims` (per-claim axis, before→after, command, verdict) and a
   capabilities table (`SCORECARD.md:4299-4319` at base). `AXES.md` requires "record before→after in SCORECARD.md", and
   `SCORECARD.md:9` still says its ratings are "legacy round-17/18 assessments, not a fresh proof". Neither claim has an
   axis record on committed bytes.
5. **Sourced-claim requirement (C2) — met.** `corpus/SOURCES.md:165` (S419) and `:166` (S420) are new rows, status `mined`,
   opened `2026-10-25`; S367 (`:157`) is the held row. Each entry's `source:` line names its id and each entry cites the id
   below the header (checked by `C2_entry_provenance`); `C3`/`C4` check row shape, opened date and `used-by`. Body hashes
   match receipts and the lesson: S367 `0188de9d…`, S419 `6172d5d1…`, S420 `a860d4f3…`; registry 158 rows vs 156 at base
   (independent `grep -cE '^\s{0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`).

## AXIS OBJECTION:

C1 is declared on **calibration** (`contract.md:13`) while the surface it changes is the `SKILL.md` gate registry. Tested
against the three authorities:

1. **Prompt §9 (`kake-round-56.md:422-423`)** requires a calibration claim to count mismatches between the lane's
   self-assessment "(SCORECARD/SHONEN)" and observed repo state. C1's population is ten `SKILL.md` rows; the counter never
   reads `SCORECARD.md` or `SHONEN.md`. Letter not met.
2. **`AXES.md:15`** names the calibration signal as "SHONEN.md/SCORECARD entries match observed repo state"; `AXES.md:13`
   names operability as "a checklist item can be run and produces the stated outcome" — and the contract's own after-state
   (`contract.md:28`) is exactly that sentence. `prompt:435` says name the axis by the surface changed.
3. **The lane's own round record disagrees with the contract**: `corpus/lessons/round-56.md:97` books C1 under
   **quality** ("the self-test tallies of ten gates now equal what their commands print (C1 counter)"), and `SCORECARD.md`
   books it nowhere. Three documents, three labels.

Strongest counter-argument, taken seriously: round 55 booked a third surface (`corpus/README.md` coverage map) as
calibration (`corpus/lessons/round-55-verifier-spotcheck.md:48`), and a registry tally *is* the lane's self-assessment of its
own tools, so the shape (mismatch count against observed state) matches calibration. Rebuttal: that precedent is precisely
the widening the r55 verifier left open — "Axis ownership for C1 stays with the operator" (`:79`) — and the operator has not
ruled; a lane cannot settle an ownership question by declaring the answer. Consequence either way: if C1 is operability
(10 → 10 HOLD), the lowest-axis obligation (calibration, score 1) is **unmet** and the label is wrong; if the operator rules
the widening, the claim is calibration but the artifact `AXES.md` names stays stale and uncounted (`SCORECARD.md:9` and its
`Planned` round-21 section). What the objection does **not** falsify: the measurement — 0/10 at a450e43 is real and
re-derived.

## ADMISSION VERDICT PER CLAIM: (author-side)

**C1 — measured after-state admissible, claim not admissible as declared.**
Show or fix: (a) the axis label — either relabel operability (10 → 10 HOLD, closing r55 routed defect 1) or obtain the
operator's ownership ruling and write the widening criterion into `corpus/QUALITY.md` before any score moves; (b) land the
`SCORECARD.md` before→after row and the `LOG.md` entry (`AXES.md`; `LEARNING.md`); (c) scope `contract.md:5` to v1 (round-55
lesson already mined the sentence); (d) close or disclose the added-`.py` guard hole beside the existing helper limit; (e)
state "ten rows in population", never "the registry is accurate" (`SKILL.md:1253-1254` are unchecked by C1, truthful today).

**C2 — measured after-state admissible, sourced requirement met, freshness label not admissible.**
Show or fix: (a) no condition in the final counter can fail for staleness (the eight are admission/self-consistency; S367 is
the only held row and its re-open lives in the receipts only) — relabel coverage/expansion and report
`freshness: unchanged (no drift found on S367)`, or add a drift condition and re-freeze; (b) land the `LOG.md`
re-verification entry (`LEARNING.md`), and correct `corpus/lessons/round-56.md:59`; (c) never present 8/8 as proof the pages
were fetched — a fabricated 2173-byte S420 body plus a matching receipt reaches 8/8 at v2.1 (measured here); admission as a
sourced claim rests on the reviewer terms the contract already names; (d) the round is not admissible as a round until the
`SCORECARD.md` record exists for both claims (`AXES.md`).

VERDICT: both after-states re-derive honestly at a450e43 (C1 0/10, C2 8/8; base controls 7/10 and 0/8, reproduced), but neither claim is admissible as declared — C1's calibration label fails §9/AXES.md and the lane's own lesson books it as quality, C2's freshness label fails the no-drift-condition test and its only re-verification record is missing from LOG, and no SCORECARD before→after exists for either claim at the measured revision.
