# Round 74 — lessons (kake, attempt 1)

Base `ced2878a1e77f57afb4ee3baebf1021e5130399b` (lane master at round open). Frozen contract
`.ufo/waves/round-74/contract.md` at `b35dd4d7d6a0a633d7c950bf641d3f948e680448`; Amendment 1 (terms
only, after the wave-1 attack seats and before any after-state) at
`312b531a1e319cb0cc14d9d2eac4ff1414d6ca75`. Wave `w1`: one v1 wave, 14 seats (scout 2, executor 4,
scribe 2, reviewer 2, critic 1, mutation-tester 1, connector 1, sentinel 1; attack share 4/14; the L1
held the planner seat). All 14 seats settled (`.ufo/waves/round-74/w1-results.json`).

Claims: C1 calibration (lowest owned axis, score 2), C2 freshness (score 10).

## Claims and verdicts

| Claim | Predicate (frozen, as amended) | Before (base `ced2878a`) | After (measured at `30c35842`) | Verdict |
|---|---|---|---|---|
| C1 registry completeness | `c74_registry_gap.py`: `unregistered==0`, every credited row's entry-command path (basename = counter) resolves, `own_row==true` over the 8 frozen counters | `unregistered=7 own_row=false met=false`, exit 1 (`controls/base-c1-registry.txt`) | `unregistered=0 own_row=true met=true`, exit 0 (`controls/after-c1-registry.txt`) | met on the amended predicate (calibration HOLD 2) |
| C2 sidecar re-observation | `c74_sidecar_reobserve.py`: `absent_present==0`, `restored_absent==0`, unevaluable 0, history matches the base bytes, restored notes outside the extended vocabulary; sweep 36/36 and exit <=1 with the same drift | `entries=174 absent=148 restored=26 absent_present=144 contradictions=144 met=false`, exit 1 (`controls/base-c2-sidecar.txt`) | `absent=4 restored=170 absent_present=0 contradictions=0 annotation_findings=0 met=true`, exit 0 (`controls/after-c2-sidecar.txt`) | met on the amended predicate (freshness HOLD 10) |

Both instruments reproduce their base controls (C1: 7/8 unregistered; C2: 144 contradictions). The
do-nothing control is the base receipt itself: no registry row and no sidecar rewrite leaves both
targets unmet, and the standing sweep stays blind to the 144 contradictions
(`controls/base-c2-sweep.txt`).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| M1 registration predicate was a false-positive test — "a row naming the counter in any cell" credits a row that cites the counter only as a witness, and one dump row could satisfy all eight. Measured at base: `SKILL.md:1198` cites `c46_matrix.py` in its Pinned-values cell while gating another counter | `w1/CriticClaims.md` §1.2–1.3; `w1/ReviewerC1.md` §2 | none at freeze — the round-70 "table row" rule was inherited without its cell semantics, and the fixture set had no witness-cell or dump-row case. Captured by the wave-1 critic, before any after-state | Amendment 1 A1 (credit only Name/Entry/Self-test cells) and A2 (one counter per row; the entry-command basename must equal the counter); selftest fixtures f7 (witness cell) and f8 (dump row) now kill the pre-amendment reading — the amended counter passes 8/8 |
| M2 verdict gap — the delivered C2 counter printed `met=true` and exit 0 while `annotation_findings` named a missing `history` or a forbidden restored note, so the frozen history/vocabulary kill rule had no instrument | `w1/ReviewerC2.md` High; `w1/Sentinel.md` F2; `w1/MutC2.md` M5 | the contract's kill rule named the conjuncts, but no fixture asserted the verdict (g4/g5 called the helper directly) | verdict gating in `apply_findings` plus g4/g5 verdict assertions and g8 (removal/reappearance note). Shown able to fail: a flipped entry with `history` dropped and a note containing `missing` both return exit 1, `met=false` |
| M3 host-relative absence notes — 144 of 148 `kind=absent` notes were written on another host (2026-10-31) and every token resolves here; no instrument compared a note against the host, so the contradiction was invisible | `controls/base-c2-sidecar.txt`; round-73 lesson M3; `w1/ScoutSidecar.md` | none — the sweep consults a note only in the citation-scan absent branch and never probes the token for the note's own sake | `scripts/sidecar_reobserve.py` + `c74_sidecar_reobserve.py`: base 144 → 0, history preserved, 4 genuinely absent entries untouched; shown able to fail by the base receipt and the g-fixtures |
| M4 frozen-control set integrity — four `base-harm-*.txt` receipts were produced by the L1 after the freeze commit and left untracked beside the three frozen claim controls | `w1/Sentinel.md` F4; `controls/PROVENANCE.md` | none — no rule bound the control directory's post-freeze state | `controls/PROVENANCE.md` names the author, time, revision and commands; the three claim controls stay the frozen set and the report discloses the four as supplementary |

No mistake sweep was needed: the wave produced the four entries above.

## Gate

- **Admit — Amendment 1 (A1–A7, B1–B5).** Each term closes a defect measured before the after-state
  (`w1/CriticClaims.md` §1.2–1.6, §2.1–2.7; `w1/ReviewerC1.md` H1/H2; `w1/ReviewerC2.md` High). The
  amendments change terms only; the claims, populations and targets are unchanged.
- **Admit — S441.** Python 3.15.2 documentation, `os.path.exists`
  (https://docs.python.org/3/library/os.path.html#os.path.exists), opened 2026-11-03, HTTP 200,
  90,223 bytes, sha256 `aa392ce9…e479a8`, retained at `.ufo/waves/round-74/sources/python-os-path.html`.
  Located quote (21 words, tag-stripped text lines 326-329): "may return False if permission is not
  granted to execute os.stat() on the requested file, even if the path physically exists". The
  boolean probe has a documented false-negative class; it cannot carry the absent/unevaluable split.
- **Admit — S442.** Python 3.15.2 documentation, `os.stat`
  (https://docs.python.org/3/library/os.html#os.stat), opened 2026-11-03, HTTP 200, 791,358 bytes,
  sha256 `4a8bb54c…3d287a`, retained at `.ufo/waves/round-74/sources/python-os-stat.html`. Located
  quote (21 words, tag-stripped text lines 237-239): "All functions in this module raise OSError (or
  subclasses thereof) in the case of invalid or inaccessible file names and paths". A second located
  quote (22 words, lines 3520-3521): "Get the status of a file or a file descriptor. Perform the
  equivalent of a stat() system call on the given path."
- **Admit — `corpus/knowledge/sidecar-reobservation.md`.** Provenance trio, both rows cited, the
  2026-11-03 census, the three-way probe and the limits; no live-property claim.
- **Admit — the two counters and the repair tool.** C1 selftest 8/8 and base reproduction; C2
  selftest 8/8 and base reproduction; the tool selftest 10/10, `--check` byte-preserving, `--write`
  atomic and refusing unevaluable input.
- **Reject — the delivered C1 counter's "first `.py` token anywhere in the row" path rule.** It makes
  a Kind-cell successor mention a path finding and hides the witness-cell false positive; replaced by
  A2's entry-command-cell rule with basename equality.
- **Reject — the "any cell" registration test.** It credits the `c46_matrix.py` witness citation and
  the one-dump-row exploit; replaced by A1/A2.
- **Reject — the ScribeRows draft's bare `c73_tmp_v3.py` successor mentions.** They are path findings
  under the delivered counter (measured by ConnOverlap); the landed rows spell
  `.ufo/waves/round-73/c73_tmp_v3.py`.
- **Reject — the draft's `gate (offline …)` Kind labels for five non-green counters.** A4 requires
  `gate (live` only for an exit-0 counter; the landed rows label `c70`, `c71_calibration` and
  `c71_tmp` `instrument (historical …)` with their measured state.
- **Reject — claiming the freshness gate "clean".** The sweep still exits 1 with the single
  `~/projects` drift; the round claims *evaluable with the same named drift*, not clean.

Spot-check: the non-author closure is owed. The L1 sample for it: 5 admits (Amendment 1, S441, S442,
the knowledge entry, the three instruments) and 5 rejects (the delivered counter's path rule, the
"any cell" test, the bare successor mentions, the draft Kind labels, the "clean" freshness reading).

## Sourced claims

- **C2 rests on S441 and S442** (both opened this round; quotes and retained bytes above).
- C1 rests on lane instruments and receipts, not web sources.

## Limits and routed items

- MutC2 survivors: M7 (working-tree instead of revision bytes) and M10 (non-deterministic write) are
  not killed by the two instruments' selftests; routed as next-round counter amendments.
- Sentinel F8: the tool's parent-directory TOCTOU window stays a named residual; F7: the sweep's
  `--selftest` residue is avoided this round by pinning `KAKE_SELFTEST_DIR`, not fixed.
- The four remaining `absent` entries are host-relative by nature; a future host change may need a
  new pass.
