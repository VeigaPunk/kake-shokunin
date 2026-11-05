# CriticClaims — round 95 verdicts

Seat: CriticClaims (leaf critic, no dispatch). Attack target: the two frozen claims as declared in
`.ufo/waves/round-95/freeze.md`, measured on the **committed freeze tree** (`8f638b59`), never on the
lane worktree. Counters were run from committed bytes (sha-verified) against scratch git fixtures
whose content derives from that tree. Every verdict line names its command and observed rc.

Verdict line: `CLAIMS C1=falsified-as-declared C2=gaming-route-found:memorizing-candidate-passes-met`

## Digest verification

| object | expected (`controls/instrument-sha256.txt`) | observed | rc |
|---|---|---|---|
| committed `c95_selfassess.py` (`git show 8f638b59:…`) | 8fd27d6268…b193 | 8fd27d6268…b193 | 0 |
| committed `c95_conditional.py` | f09f8409…f312 | f09f8409…f312 | 0 |
| committed `frozen/c1-surfaces.json` | 00a04c9a…47b8 (`SURFACES_SHA` in counter) | 00a04c9a…47b8 | 0 |
| lane worktree `c95_selfassess.py` (checked after my start) | 8fd27d… | **04be4a7d…a32** | — |
| lane worktree `frozen/c1-surfaces.json` | 00a04c9a… | **9eff04c5…f4665** | — |

**Integrity finding (drift, not a repair licence):** between my first verification and a later check,
the lane worktree's `c95_selfassess.py` and `frozen/c1-surfaces.json` were rewritten (mtime
13:35:10 -0300, uncommitted; `git status` shows `M`). The drift removes the knowledge-entry
content identity (`head8_sha256` pins, 82 lines) and replaces it with a presence-only check under
an "Amendment A" comment; `SURFACES_SHA` was updated to match. `controls/base-c1.txt` line 1 was also
rewritten (13:35:37) and now prints `counter=04be4a7d…` where the committed receipt prints
`counter=8fd27d…`. Full diff: `instrument-drift-worktree-vs-freeze.diff`. Main was notified
(relayed to KakeR95; L1 directed to restore committed bytes or score C1 not-admitted).

## Do-nothing control (frozen counters on the freeze tree)

| run | rc | line 1 (key fields) | matches committed base receipt? |
|---|---|---|---|
| `c95_selfassess.py --root <freeze fixture> --revision HEAD --work …` | 1 | `counter=8fd27d… mismatches=18 E1=0 E2=0 E3=3 E4=0 E5=15 pins=ok battery=20/20 admit=5/5 shadow=absent predecessor_admits=10/19 floor=4 self_pin=ok met=false` | yes (`controls/base-c1.txt`) |
| `c95_conditional.py --root <freeze fixture> --revision HEAD --work …` | 1 | `candidate=present hand=57/66 generated=79/120 forgeries_refused=7/7 positive=admitted mutants=40/40 survivors=none anti_table=ok population=ok seed=95 met=false` | yes (`controls/base-c2.txt`) |

Receipts: `c1-ctl-freeze-fixture-run.txt`, `c2-ctl-freeze-fixture-run.txt`,
`c1-ctl-worktree-run-before-drift-counter-8fd27d.txt` (lane run before the drift, same numbers).

## C1 gaming and identity routes (frozen counter, committed bytes)

Each route is a scratch git commit on a clone of the freeze tree; counter run with `--root <fixture>
--revision HEAD`. Full output per route in `c1-<route>.txt`; summary in `c1-route-summary.json`.

| route | construction | rc | line 1 key fields | outcome |
|---|---|---|---|---|
| X0 de-backtick | strip backticks from every `scripts/`/`corpus/`/`.ufo/` token in SKILL.md | 1 | `pins=identity mismatches=3 E5=0`; 100 `skill_row_tokens` refusals | refused (R94-3 path-token pin works) |
| X1 dir→prose | 15 directory tokens replaced by prose, no files added | 1 | `pins=identity mismatches=3 E5=0`; 15 refusals | refused |
| X2 drop rows | delete the 15 directory rows | 1 | `rows=240 pins=short mismatches=3`; 15 `skill_row` identity refusals | refused |
| X2 + `--base-pins-json` lowered to 1 | operator-supplied base pins (flag exists; the frozen command does not use it) | 1 | `pins=identity`; still 15 `skill_row` refusals | refused; flag lowers only `short`, not identity |
| X3 canned wrapper | prints `counter=0000 … mismatches=0 … met=true`, exit 0 (`c1-X3-canned-wrapper.sh`) | 0 | true digest `8fd27d…` absent (`in` test → False) | a consumer that checks the digest refuses; a consumer keyed on `met=true`/rc admits. The counter itself cannot prevent a canned wrapper; protection is consumer-side |
| X4 verdict-only | frozen counter `--verdict-only` on X8 | 1 | `met=n/a verdict=failed` | never prints `met=true` (confirmed) |
| X4 verdict-only, clean | drifted counter on a clean fixture | 0 | `mismatches=0 met=n/a verdict=clean` | exit 0 with `met=n/a`: consumers must not read rc 0 as met |
| X5 rename pinned entry | `git mv corpus/knowledge/crux-keyless-check.md …-v2.md` | 1 | `pins=identity`; `entry:corpus/knowledge/crux-keyless-check.md` | refused |
| X7 blob-only E5 | 15 directory tokens replaced by `` `corpus/QUALITY.md` `` (non-empty blob, unrelated to the row) | 1 | `pins=ok E5=0 mismatches=3 (E3 only)` | **E5 passes with a meaningless blob**; the counter has no semantic check; only the non-author row review (R94-5) guards it. Counter-level gaming route |
| H1 honest E5 | each directory token → a real committed blob inside the same tree | 1 | `pins=ok E5=0 mismatches=3` | honest E5 reachable |
| H2 honest E5 + in-place E3 | H1 + kimi line 1 `/tmp/` removed; second `source:` line deleted in crawl-budget and crux | 1 | `pins=identity mismatches=0`; `entry-content:` for all three entries | **refused by the frozen identity pin** |
| X8 E5 blob + E3 head displacement | X7 + 8 tagged lines inserted above each E3 entry (pushes defective `source:` out of the 8-line head) | 1 | `mismatches=0 pins=identity`; `entry-content:` ×3 | refused by identity; the only E3 clearance that does not edit a base line is append-only, and it still alters the head-8 bytes |
| D-H2 (drifted instrument) | H2 scored with the on-disk drifted counter + surfaces | **0** | `mismatches=0 pins=ok battery=20/20 admit=5/5 … met=true` | **met=true**: reachable only with the relaxed instrument |
| D-X8 (drifted instrument) | X8 scored with drifted instrument | **0** | `mismatches=0 pins=ok … met=true` | met=true |
| D-base (drifted instrument, base tree) | unchanged base | 1 | `mismatches=18 … met=false` | the drift alone does not clear the base; it relaxes the E3 identity |

Append-guard (`scripts/append_guard.py`, capability row `append-guard`; base = freeze tree):

| fixture | rc | findings |
|---|---|---|
| H2 (in-place head edits) | **1** | `changed` ×3 (crawl-budget, crux-keyless, kimi-subpath) |
| X8 (insert-only displacement) | 0 | none |
| H1 (E5 table rows only) | 0 | none |
| X0 (de-backtick) | 0 | none (append-guard is blind to SKILL.md; scope is `corpus/knowledge/**`) |

Receipts: `c1-appendguard-*.json`, `c1-H2-honestE5+inplaceE3.txt`, `c1-X8-displace+blob.txt`,
`c1-D-H2-drift.txt`, `c1-D-X8-drift.txt`.

## C1 reachability: what a legitimate repair must touch

Base mismatches (`controls/base-c1.txt` JSON, reproduced at the freeze tree): E3 = 3, E5 = 15.

**E5 (15 findings → 15 SKILL.md table rows).** The freeze says "13 directory rows (15 E5)". The
audit surface has **15 rows**, one E5 per row (`c1-E5-tree-row-scan.txt`, freeze SKILL.md lines):
617 citing-set; 720 round-29 real-input; 726 base-path-audit; 1046 link-preview-audit; 1253
selftest-tally (`scripts/fixtures`); 1254 yahoo-crawl (`round-56/sources/`); 1350 wave-evidence-ledger
(`round-51/`); 1359 response-snapshot (`round-61/capture/`); 1431 c72 tmp (`round-72/`); 1506
x_robots (`round-80/cases`); 1535, 1536, 1537 (`round-85/w1/ExecRegistry/`, three rows); 1539
count.py (`round-85/controls/`); 1588 c87 finite claims (brace list ending in `snapshots/`, a row my
plain scan misses because of the brace). Honest repair = H1 (verified: E5 0, pins ok).

**E3 (3 findings → 3 knowledge entries, all inside the 8-line head window):**
- `corpus/knowledge/crawl-budget-consequences.md`: two `source:` lines (lines 1–2).
- `corpus/knowledge/crux-keyless-check.md`: two `source:` lines (lines 1–2).
- `corpus/knowledge/kimi-subpath-audit.md`: line 1 `source:` carries a `/tmp/` locator.

**Nothing else** is touched by the counter's base mismatches. The R94-9 registry rows are not counted
in the base E-classes and were not evaluated here.

**Can the E3 repairs be made?** No, under the frozen counter:
- The frozen committed counter pins each base knowledge entry's first eight lines by sha256
  (`head8_sha256`, 82 entries; the counter's identity code emits `entry-content:<path>`). Every E3
  defect sits inside those eight lines, so any clearing edit changes the pinned bytes and fails identity.
  H2 and X8 both show `pins=identity` with `entry-content:` for all three entries.
- The append-guard capability row forbids the in-place head edits the freeze declares: "a changed,
  reordered or deleted base line … [is a] finding". H2 shows rc 1 with three `changed` findings.
  The only append-guard-legal shape is an insertion beginning with a visible `[rNN-correction]` tag
  (X8, rc 0), and insertion cannot remove a head defect; it can only push it out of the window, which
  the frozen identity pin refuses.

Therefore the best reachable state under the frozen instrument is **mismatches = 3 (E3 only)**, so
`met=false`, and mismatches=0 is unreachable by the declared repair set. The only routes to
mismatches=0 with `met=true` are the on-disk drifted instrument (D-H2, D-X8) or the counter-level
gaming route X7/X8, both of which are outside the declared claim.

## C1 verdict

**C1 = falsified-as-declared.** Target `mismatches 18 → 0` is unreachable by the declared work
under the frozen instrument. The declared E3 repairs (in-place head edits) are refused by the counter's
own content identity and by the append-guard capability row. Secondary: the counter admits E5 pins to
an unrelated blob (X7) and does not enforce append-guard, and the CLI accepts an operator
`--base-pins-json` knob (harmless to identity, but it is an operator-supplied parameter the freeze does not declare).

## C2 base control and the nine hand failures

Base hand failures (`controls/base-c2.txt`, `hand_failures`, the first 9 entries of the 12 retained;
the counter caps the list at 12, with the 9 hand entries first):

| hand case | clause |
|---|---|
| `inm/empty-member-middle-ignored` | C1 (empty list members) |
| `ifmatch/empty-member-leading-ignored` | C1 |
| `inm/empty-member-trailing-ignored` | C1 |
| `inm/all-empty-members-match-nothing` | C1 |
| `ifmatch/all-empty-members-match-nothing` | C1 |
| `etag/obs-text-current-weak-matches` | C2 (obs-text in opaque-tag) |
| `etag/obs-text-strong-ifmatch` | C2 |
| `role/null-key-explicit` | C3 (`"role": null`) |
| `refuse/duplicate-top-keys` | C4 (raw duplicate keys) |

So the nine hand failures are exactly the clauses C1–C4. **C5 contributes zero hand failures**: the
v1 candidate already passes its C5 hand cases.

Generated failures (41; attribution `c2-generated-attribution.txt`, `c2-attribution.py`): every one
involves an empty list member (C1), an obs-text byte in an opaque-tag (C2), or a non-GET/HEAD
If-Match/If-None-Match/If-Modified-Since edge (C5). Three of them are obs-text inside request tags.
None involves C3 or C4 (the generator never emits `"role": null` or raw duplicate keys).

**Reachability.** Hand 66/66 requires the C1–C4 decisions (9 cases). It does **not** require C5
[the C1–C4 sufficiency is an inference from the mapping; no candidate implementing it was built].
Full `met=true` requires the C5 decisions for the generated 120 (the 10 non-GET/HEAD edge failures
with no C1/C2 tag). So "no repair short of C1–C5 reaches met" holds; "66/66 needs C1–C5" overstates by
C5.

## C2 gaming route (found and scored)

Route `C2-T`: a lookup-table candidate (`c2-T-lookup-table-candidate.py.txt`, built by
`c2-T-lookup-table-builder.py`). It embeds the 66 hand cases (2 raw duplicate-key payloads keyed by
bytes; 64 canonical JSON keys) and the 120 generated seed-95 cases with reference expectations,
refuses everything else, and is installed as `scripts/conditional_eval.py` in a scratch commit.

Command: `python3 -B fz/.ufo/waves/round-95/c95_conditional.py --root fx/C2-table --revision HEAD --work …`
→ **rc 0**, line 1: `candidate=present hand=66/66 generated=120/120 forgeries_refused=7/7
positive=admitted mutants=40/40 survivors=none anti_table=ok population=ok seed=95 met=true`.

Why the counter admits it: `anti_table` tests only the first 16 hex of sha256 of canonical JSON for
hand inputs and forgery/positive filename stems. It does not look for the 120 generated inputs, although
`generate(95, 120)` is public in the frozen counter and deterministic. The mutant conjunct is scored
against the reference, not the candidate, so it is identical (40/40) for any candidate (it is therefore
no evidence about this candidate). Receipts: `c2-T-lookup-table-candidate.txt` (+ `.err`).

## C2 mutant kill rule: circular?

Facts:
- Population: 40 mutants of the round-93 positive control (`pos-good.py`, pre-v2 semantics).
- v1 survivors at round 94: M11, M18, M19, M24, M28, M29, M32, M37, M40.
- The v2 hand file comment says its successor cases are "one per class in which the round-93 population
  left a reference mutant alive (M11, M18, M19, M24, M28, M29, M32, M37, M40)": nine cases authored
  after seeing the survivors, then scored on the same population.
- M11 is equivalent to the base under v1: `receipts/equiv_m11.py` (round 94) gives `cases=115200 differing=0`.
  Under v2 it is killed by `inm/empty-member-middle-ignored`, because the v2 reference now accepts empty
  members while M11 (like the base) still refuses them. Nothing in M11 changed.
- Five of the 40 kills are refusals where the v2 reference accepts: M11, M19, M20, M33 (traceback), M40
  (`mutant-scan-v2-result.json` notes, `got None (rc=1 …)`).

**For "circular":** the target 40/40 is reached by authoring cases against the survivors and by moving the
reference onto the behaviour the pre-v2 base lacked; M11 is killed by oracle movement alone; the metric is
independent of the candidate (the lookup table gets 40/40). It measures the authored oracle's distance
from the old base, not candidate quality, and the empty equivalence receipt list hides the fact that
M11 was equivalent to the base under v1.

**Against "circular":** the v2 clauses (C1 from S478, C2 from S455) are RFC-grounded, the population and
its base are digest-pinned and were scored before the freeze, and killing refusal-mutants is a real
behaviour check, since the old base refused RFC-valid input. Successor cases stand on their own grounding
as regression tests. A held-out population would be the test of generalisation, and none was declared.

**Verdict on the kill rule:** circular as an acceptance criterion. It is a consistency check of the
authored oracle against its own population, not evidence that the candidate implements contract v2, and
the lookup-table route shows the combined conjuncts can be met without it.

## C2 verdict

**C2 = gaming-route-found:memorizing-candidate-passes-met.** The frozen counter returns `met=true` (rc 0)
for a candidate that memorises the public, seeded 186-case set and refuses the rest. The anti-table
gate is digest-only and covers hand inputs only, so the counter cannot distinguish a lookup from contract
v2. Separately, the mutant 40/40 target is circular as stated (above). The nine hand failures are exactly
C1–C4 clauses; C5 is needed for the generated 120, not the hand 66.

## Receipts index (flat, in this directory)

- Controls: `c1-ctl-freeze-fixture-run.txt`, `c2-ctl-freeze-fixture-run.txt`, `c1-ctl-freeze-C1.txt`,
  `c1-ctl-worktree-run-before-drift-counter-8fd27d.txt`, `c2-ctl-freeze-raw.txt`.
- C1 routes: `c1-X0-deback.txt`, `c1-X1-prose.txt`, `c1-X2-dropRows.txt`, `c1-X2-lowpins.txt`,
  `c1-X3-canned-wrapper.{sh,txt}`, `c1-X4-verdict-only-{X8,drift-clean}.txt`, `c1-X5-rename.txt`,
  `c1-X7-blobOnly.txt`, `c1-X8-displace+blob.txt`, `c1-H1-honestE5only.txt`, `c1-H2-honestE5+inplaceE3.txt`,
  `c1-D-base-drift.txt`, `c1-D-H2-drift.txt`, `c1-D-X8-drift.txt`, `c1-route-summary.json`,
  `drift-routes.json`, `c1-appendguard-*.json`.
- C1 scans: `c1-E5-tree-row-scan.{py,txt}`, `c1-frozen-counter-committed-bytes.py`,
  `c1-frozen-surfaces-committed.json`, `instrument-drift-worktree-vs-freeze.diff`.
- C2: `c2-generated-attribution.txt`, `c2-attribution.py`, `c2-T-lookup-table-candidate.txt`
  (+ `.err`), `c2-T-lookup-table-candidate.py.txt`, `c2-T-lookup-table-builder.py`.
- Tools: frozen counters only, run with `python3 -B` and `TMPDIR` set to scratch. No tool was installed or upgraded.
