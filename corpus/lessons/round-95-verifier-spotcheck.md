author: hyaku closure (non-author integrator, @m_zfl)

# Round 95 verifier spot-check — kake (hyaku run 15, attempt 1)

Closed 2026-11-05 by the hyaku closure judge (non-author; fresh session, did not author the
round). Lane base `fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3`; lane tip
`7bace5789077167614212d0a34d31f1bb448e668`. All commands below were run by the closure at the
lane repo unless noted. Per PROTOCOL §Gate standard the lane's gates were NOT executed by the
closure; gate claims were verified from committed evidence (receipts, self-test tallies, the
revision each verdict names) plus plain byte measurements.

## Conformance (step 1)

- Report committed in the fleet repo by the lane identity: `git log --format='%an %H' -- .ufo/reports/round-95/kake.md` → `kake-shokunin <kake@shokunin.local> 5d9c3109f08ea355a01896b22277baba83052bac`. PASS.
- `## SHONEN` heading present, one line per box: `grep -c '^## SHONEN'` → 1; `grep -cE '^- \[(x| |~)\]'` → 4 (boxes 1/3/4 `[~]`, box 2 `[ ]`). PASS.
- Every cited lane commit exists and is an ancestor of the branch ref (jj-colocated; tested against `master`, not `@{u}`): `git merge-base --is-ancestor <hash> master` → yes for `fdd5fdbe`, `43cdd9fc`, `8f638b59`, `4f443b3f`, `9cf92470`, `1fca1ad7`, `7bace578`, `d9be693f`. PASS. (The erratum's `191dd0ed` is cited as deliberately absent; `git cat-file -t` fatal is the erratum's own finding, not a conformance failure.)
- Lane clean and pushed: `scripts/hyaku/jj-lane.sh state <lane>` → `branch=master local=7bace578… remote=7bace578… ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` → empty; `git ls-remote origin refs/heads/master` → `7bace5789077167614212d0a34d31f1bb448e668`. PASS.
- Dispatch prompt carries the template contract: report path + filename, commit-before-report ordering ("The report lands last and cites the pushed lane hash"), SHONEN heading gate, commit-hash citation rule, write scope, L0 side channel, mission/axes binding, L2 ≥8 batched floor. PASS.
- Dispatch digest (copied from `.ufo/watchdog.log`, lines 2873/2889): `2026-11-05T12:45:45-03:00 launch kake round=95 pgid=3818161 driver=hyaku-inline attempt=1` / `2026-11-05T14:16:07-03:00 complete kake round=95; hyaku-inline attempt=1`. Matches the closure dispatch record.

## Claim re-checks (step 2)

Evidence-verified from committed bytes; no lane gate executed by the closure.

**C1 — calibration (HOLD 2), strict self-assessment conformance repaired. Re-measured: UNMET, honest stop.**
- Receipts at the tip (`git show master:.ufo/waves/round-95/controls/base-c1.txt` / `after-c1-final.txt`): base at `fdd5fdbe` reads `mismatches=18 E3=3 E5=15 pins=ok battery=20/20 admit=5/5 shadow=absent predecessor_admits=10/19 floor=4 met=false`; final at `1fca1ad7` reads `mismatches=0 … E5=0 pins=identity battery=20/20 admit=5/5 shadow=absent predecessor_admits=10/19 met=false`. Both match the report exactly.
- Frozen-counter identity held across both measurements: both receipts cite `counter=8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193`, equal to `controls/instrument-sha256.txt` line 1, and the tip blob hashes to the same digest (`git show master:.ufo/waves/round-95/c95_selfassess.py | sha256sum` → `8fd27d62…`). Byte-identity with the pre-amendment instruments commit: `git diff 43cdd9fc master -- .ufo/waves/round-95/c95_selfassess.py .ufo/waves/round-95/c95_conditional.py .ufo/waves/round-95/frozen/c1-surfaces.json` → empty. The Amendment A counter (`04be4a7d…`) produced no integrated receipt.
- Self-test tally committed (`controls/ctl-c1-selftest.txt`: 13/13 planted, exit 1 planted / 0 repaired, battery 20/20, admit 5/5, `--surfaces-file` refused); restoration receipts committed (`restore-verify-c1-selftest.txt` identical to the self-test tally; `restore-verify-c1-base.txt` line-1-identical to `base-c1.txt`).
- Ruling: the declared target (`met=true` exit 0 at the landed tip) is falsified by the frozen counter's own receipt; the zero-mismatch state is real but uncertifiable under the frozen predicate (`pins=identity` entry-content findings on exactly the three repaired entries). The round reported `met=false` with receipts rather than re-scoring on amended bytes — honest stop. Score stays 2.

**C2 — freshness (HOLD 10), capability acquisition: conditional_eval contract v2. Re-measured: MET.**
- Receipts: `controls/base-c2.txt` at the instruments commit `43cdd9fc` → `hand=57/66 generated=79/120 forgeries_refused=7/7 positive=admitted mutants=40/40 survivors=none met=false`; `controls/after-c2-final.txt` at `1fca1ad7` → `hand=66/66 generated=120/120 forgeries_refused=7/7 positive=admitted mutants=40/40 survivors=none met=true`. Both match the report.
- Landed candidate is the receipted candidate: `git show master:scripts/conditional_eval.py | sha256sum` → `957ddd4e361a6298beff806e30a8d53ac798dda4bc031eb2b0b1d943691212eb`, equal to `candidate_sha256` in `after-c2-final.txt`.
- Corroborating committed evidence: second independent implementation verdict `DRIVER VERDICT met=true` (`w1/ExecC2V2/scoring-v2.txt`); pre-freeze equivalence scan 40/40 killed with M11 included (`controls/mutant-scan-v2.txt`, `-result.json`); C2 self-test tally committed (`controls/ctl-c2-selftest.txt`: 8/8 fixtures, drifted-reference cases=5, M11 killed); gate-registry row for `c95_conditional.py` present in SKILL.md with entry command, verdict map, self-test spelling, pinned-value paths.
- The round's own caveats are carried in the report and routing (memorizing-candidate route R95-8, sandbox escapes R95-7, reference deviations R95-6, no C2 effectful-shadow defense); capability entered with caveats named. Score stays 10.

**Axis harm:** `git diff fdd5fdbe master -- SCORECARD.md` is append-only (round-95 section; no existing axis row modified). PROVINCE.md, SHONEN.md, corpus/README.md untouched; corpus/QUALITY.md append-only (52 insertions, 0 deletions); corpus/SOURCES.md +1 row; LOG.md append-only (+8). No owned axis harmed.

**R95-4 closure duty (row-by-row re-read of the 15 repaired SKILL.md rows) — discharged by this closure.** For each of the 15 rows in `w1/ExecC1Repair/repairs.md`: the named file is a committed non-empty regular blob at base (`git cat-file -t/-s` at `fdd5fdbe`: 34B–5747B, all `blob`), the token is present in SKILL.md at the tip, and first cells are unchanged (spot: row `citing-set` base L617 first cell == tip L622 first cell; row line numbers shifted by the five added registry rows). Recorded deviations (`registry-rows.mjson` absent at base → `c1-base.json`; row 1588 brace collapse) match the committed notes. The residual `scripts/fixtures/citing-set/` tree token at SKILL.md line 775 is narrative prose in the round-27 section body, not one of the 15 repaired gate-registry rows — no defect.

## Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration (HOLD 2) | unchanged | C1 unmet under the frozen rule (`after-c1-final.txt` `met=false`); real repairs receipted (mismatches 18→0) but uncertifiable by the frozen predicate; score stays 2; successor routed R95-1 |
| freshness (HOLD 10) | improved | C2 met on the frozen counter (`after-c2-final.txt` `met=true`, candidate sha matches the landed blob); capability row entered with caveats named; score stays 10 |
| operability / depth / coverage / adjacency (other owned rows) | unchanged | no re-scored rows in the SCORECARD diff; overlap evidence reported, not absorbed (`w1/ConnectorScope/overlaps.md`) |

## Discernment spot-check (step 3)

Sample from `corpus/lessons/round-95.md` `## Gate`: two admits and two rejects re-opened.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S479 row (RFC Editor errata for RFC 9110) | admit | live GET `https://www.rfc-editor.org/errata_search.php?rfc=9110` → 302→200, 97 741 bytes, sha256 `e6ddebb240b522f36acf0ccc9b6a52030a35ff77d17203dbd1fcf6d1339c0911` — byte-identical to the retained body; quote verified at retained-body line 863 (21 words, exact substring); `fetch.txt` receipt complete; status headings Verified(6)/Reported(2)/Rejected(6) at lines 108/689/904 as anchored | agree | source re-opens byte-identical at closure; the ≤25-word quote is located and grounded; the negative claim ("no verified or reported erratum targets 5.6.1.2/5.6.3/8.8.3/13.1.x") carries its sweep — the only `8.8.3` token in the body is inside the EID 9164 (Editorial, Appendix A) ABNF-diff note, not a Verified/Reported erratum targeting that section |
| Amendment A (post-freeze C1 instrument edit) | reject (integrity flag) | `git show d9be693f --stat` (edits `c95_selfassess.py`, `instrument-sha256.txt`, deletes `frozen/c1-surfaces.json` after freeze `8f638b59`); restore at `4f443b3f`; tip bytes hash to the frozen digests `8fd27d62…`/`00a04c9a…`; both C1 receipts cite the frozen counter; restore-verify base control line-1-identical | agree | a post-freeze instrument edit cannot score its own claim; the withdrawal was mechanical, receipted, and no amended receipt is integrated anywhere — the correct handling of the round's own seat-found defect |
| ExecC2V2 v2 candidate diff (landing) | reject (kept as corroboration) | landed `scripts/conditional_eval.py` at tip sha `957ddd4e…` = receipt `candidate_sha256`; seat's independent implementation verdict `DRIVER VERDICT met=true` retained as wave evidence | agree | one implementation lands; the independent second implementation still corroborates the population verdict — the reject is process-correct and loses no evidence |
| S479 first-drafted `used-by` (freeze.md only) | reject, corrected | tip `used-by` = `.ufo/waves/round-95/freeze.md, corpus/knowledge/conditional-list-membership.md, corpus/lessons/round-95.md`; all three paths exist | agree | `used-by` must name the row's real consumers; the corrected value keeps every path existing and names both real consumers |
| considerthese proposal 3 → QUALITY R95-D | admit | `corpus/QUALITY.md` R95-D present (frozen `met` line reported beside independent held-out replay; divergence flagged, never averaged away), grounded by the round-90 divergence record the proposal cites | agree | the criterion is grounded in a recorded historical divergence and was shown able to fail on it — not a vibe criterion |

New SOURCES row re-open: S479 (above) — agree, quote 21/25 words at the named location.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0 with the pre-existing W04 duplicate-URL warning class only (the report names it); rows 216 at tip vs 215 at base (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`), matching the report's 215 → 216.

## Trend verdicts (closure, protocol vocabulary)

- **expansion: improved** — one admitted knowledge entry (`corpus/knowledge/conditional-list-membership.md`, provenance trio first, cites mined rows S478 + S479) on ground the coverage map did not hold; registry 215 → 216 rows with census exit 0 at both ends; contract-v2 extension of the held conditional-request instrument. The report's `improved-bounded` label reads as improved with the recorded bound.
- **quality: improved** — 15 SKILL rows now name committed non-empty blobs (re-read 15/15 by this closure), three provenance-trio corrections tagged in place, tool deepened to contract v2 with committed self-test tally; no admitted entry failed a re-check; the calibration credit is honestly withheld (C1 unmet), which is reporting discipline, not a corpus regression.
- **discernment: improved** — the round's own attack seats caught the post-freeze instrument edit and the amendment was withdrawn rather than defended (verified above); every gate decision in `## Gate` carries reasons; the outside spot-check (this closure) agrees with all four sampled decisions. No disagreement left unlearned.

## Routed to round 96 (lane must fix)

1. **R95-1 (lane-routed, stands):** successor C1 counter pins knowledge entries by presence, freezes BEFORE dispatch, and re-declares the E3 repair route so the frozen predicate and pins agree.
2. **R95-2 (stands):** fleet kill-predicate decision owed (kumitate K43 vs tabi catalogue-time vs kake digest-pinned receipts) — `w1/ConnectorScope/overlaps.md` rows 4–5.
3. **R95-3 (stands):** cite chousa criterion 146 as prior art for the repair-naming rule; do not port.
4. **R95-5/R95-6/R95-7/R95-8 (stand):** successor-counter items — NG01/NG08/NG11 false-green shapes; C2 reference deviations R1/R2 under contract C5; symlink/`os.execv`/PYTHONPATH/docstring sandbox gaps; anti-table must digest generated inputs.
5. **New (this closure):** the report's trend labels read `improved-bounded`, which is not in the protocol vocabulary (`improved | harmed | unchanged | unprovable-but-better`). Status-neutral minimum-content defect; round 96's report uses the bare vocabulary and states any bound in the evidence prose.
6. **New (this closure):** `freeze.md` at the tip still carries Amendment A's "every post-amendment check must hash the values above" with the superseded digests (`04be4a7d…`/`9eff04c5…`). Filed bytes are never rewritten; round 96 records the supersession in its report/lesson (the ruling receipt set `4f443b3f` is authoritative) — a reader following freeze.md's stale instruction would mis-verify the instrument.
7. **Carried (operator-owned):** open L0 `kake | round-94` (two honest unmet claims) remains unanswered; round 95 added none. SHONEN box 2 stays `[ ]` (gap unchanged); boxes 1/3/4 are author-asserted `[~]` — none is promoted by this closure; promotion stays operator-owned.

## Closure verdict

C1 unmet (honest stop, receipted) + C2 met → not every claim verifies, no axis harmed.
`lanes: kake = ok` (real report, real landed work); `admitted: false`;
`verdict: rejected-honest-stop`. Trends: expansion improved, quality improved, discernment improved.
