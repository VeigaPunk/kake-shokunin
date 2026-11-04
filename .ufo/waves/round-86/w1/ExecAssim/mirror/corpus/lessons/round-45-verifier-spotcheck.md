# Round 45 — verifier spot-check (closure)

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-24
lane repo: /home/vgpnk/Projects/shokunin/kake-shokunin @ dc7f03e7c8ba45878e0f4eb1ea87543c9466d67b
base: 35b35f41ba8782872bec42a4df77407c76e7926e · report: .ufo/reports/round-45/kake.md (fleet commit 1a5b2d8, author `kake-shokunin`)
dispatch digest (from .ufo/watchdog.log, copied per duty): `2026-10-23T23:51:35-03:00 launch kake round=45 pgid=4072003 driver=hyaku-inline attempt=1`; `2026-10-24T01:27:07-03:00 complete kake round=45; hyaku-inline attempt=1`

## Step-1 conformance

| Check | Command | Result |
|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-45/kake.md` | `kake-shokunin 1a5b2d8a73a853ba0c3ae257f8081139789ae264` — pass |
| SHONEN heading, one line per box | read | 4 boxes, `[ ]`/`[~]` lines with pointers — pass |
| Cited commits exist + ancestor of `master` | `git merge-base --is-ancestor <hash> master` for 3b4c430a, 7ed93784, 4c538444, 290b570d, 74c9b3cf, dc7f03e7 | all ancestors — pass; **defect: report cites `e5455253` (wave-2 registry) which does not resolve — the commit is `e54552553eaff4d7…`; a dead short-hash citation, status-neutral** |
| Lane clean + pushed | `scripts/hyaku/jj-lane.sh state` | `ahead=0 behind=0 tracked=0 untracked=0`, tip = dc7f03e7 — pass |
| Prompt carries template contract | read of .ufo/prompts/kake-round-45.md | sections 1–6 + hyaku addendum; five child-lane items present (report path, commit-before-report, SHONEN heading, hash-citation rule, write scope) — pass |
| Marker test | report content | real claims, evidence pointers, landed hashes — not a marker |

## Per-claim re-check (my own measurements over committed bytes at dc7f03e7)

**C1 — operability, witness-gate driver v2.** Reported: before invalid_accepted=3; after 0, rejections_named=3, honest 27/27 + build 3/3; verdict NOT MET as declared (causal clause "over the invoked counter bytes" unfalsifiable by mtime + self-reported sha).

- `jq -c '{invalid_accepted, rejections_named, honest_witnessed, honest_build_met}' verification/matrix/before.json` → `{"invalid_accepted":3,"rejections_named":0,"honest_witnessed":27,"honest_build_met":3}` — matches.
- Same on `after.json` → `{"invalid_accepted":0,"rejections_named":3,"honest_witnessed":27,"honest_build_met":3,"honest_exit":0}` — matches; per-fixture classes counter_error / tool_absent / stale_receipt named in the receipt.
- `sha256sum` on both drivers: v1 `8ee2c8bf…` (frozen bytes, matches report), v2 `9b824d95…` (matches report).
- Root-cause code read: `c44_audit.py` returns/stores `p.returncode` (:61, :176) but no refusal path consumes it; `c45_audit.py` `receipt_validity()` (:77-88) returns the three named classes. Matches the declared mechanism.
- Disposition evidence present and consistent: `w1/CriticC1Predicate.md`, `w2/AttackC1Sentence.md`, `w2/AttackKnowledgeEntry.md` F1, correction appended to lesson entry 14, L0 question filed (fleet commit 03a0f94c, lane identity). The NOT-MET-as-declared ruling is sound: the frozen sentence's causal clause is indeed not falsifiable by mtime + a self-reported sha field — the verifier agrees with the lane and the disposition is routed, not hidden.
- **Bounded repair: verified.** Re-measured by me from committed receipts (above); the frozen counting command itself re-run by me on a sandbox clone checked out at dc7f03e7 (lane untouched): `--stage before` exit 0 re-derived `invalid_accepted=3` live; `--stage after` exit 0 (223.8s wall) re-derived `{"invalid_accepted":0,"rejections_named":3,"honest_witnessed":27,"honest_build_met":3}` live.

**C2 — freshness, standing-claim re-verification.** Reported: (a) selftest 2/4 → 4/4; (b) v4 receipt names class runs true → false; (c) named claim receipt re-derives 26/1/0, not the frozen 22/1/4 → falsified as declared.

- (a) committed selftest logs: before m2/m4 `SELFTEST_EXIT=0` (survive), m1/m3 `=1`; after all four `EXIT=1` → 2/4 → 4/4 — matches.
- (b) `jq -r '.predicate' .ufo/waves/round-44/verification/claim/v4-final/v4.json` names "the eleven v4 runs **and the ten class runs**" (true); fresh `verification/v6v4/counter-v4.json` names only "the eleven v4 runs" (false) — matches.
- (c) my own derivation from the named receipt's committed bytes (`after-final/after-v5.json`, sha256 verified `9dead4d7…`): per-row `caughtBy`/`legacyCaught` counts → class_only=26, mixed=1, met=0, witnessed_total=27 — exactly the reported falsification. The frozen 22/1/4 re-derives only from the earlier `after-v5.json` (sha `2383efae…`, 23 witnessed, met_no_witness=4) — the lane's claim-identity finding is confirmed by my own jq.
- Correction filed append-only in SCORECARD + lesson entry 15 with both receipt sha256s — not narrowed, not rewritten.

**Exploratory claims:** none declared (zero exploratory this round) — nothing to rule on.

## Per-axis verdicts

- **operability: improved** — C1's bounded repair re-measured true (3/3 invalid classes refused with named classes; honest cohort re-certified 27/27 + 3/3, exit 0); the unfalsifiable causal clause is named, not papered over. No harm: SCORECARD diff is append-only (234 added, 0 removed lines).
- **freshness: improved** — C2(a)/(b) verify; C2(c) falsified-as-declared with a confirmed, filed correction; the witness-split figure now binds to the receipt it names (path + sha256).

No owned axis harmed: committed no-harm evidence `w2/ReRunLedgerGate.md` (ledger gate 3 figures, 0 mismatches + selftest) verified as committed evidence per the gate standard (not executed by me); census exit 0 (below); `git diff base..tip -- SCORECARD.md` append-only.

## Discernment spot-check (LEARNING.md — outside check)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S133 (subprocess docs) | admit | live `curl` re-open HTTP 200, 208,624 bytes (matches row) + retained `.ufo/waves/round-45/sources/subprocess.html` (sha256 prefix eceda6f6 matches row) | **agree** | Located quote "A negative value -N indicates that the child was terminated by signal N (POSIX only)." present verbatim in the retained text modulo one HTML line-wrap; 15 words ≤ 25; a tier-A primary and the correct grounds for a receipt-gate exit-status rule |
| S134 (SO 24139389, tier C) | reject | retained `so-answer.json` via the Stack Exchange API (HTTP-403 note on direct HTML confirmed by the row) | **agree** | Quote "A negative return code usually means that the process was terminated by a signal." found verbatim (14 words); the durable point is a restatement of the tier-A primary S133, and the row carries an actionable flip — a sound reject satisfying the round-44 closure requirement |
| candidate-only row (SO a/5631819) | no decision | retained `so-a5631819.json` exists | agree | screened, adds no authority beyond S133; correctly left undecided |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → **exit 0** (12 pre-existing W04 duplicate-url warnings, no E-class rows) — matches the report's after-state. SOURCES rows 132 → 134 confirmed by row read (`| S133`, `| S134` at lines 141-142).

## Trend verdicts (closure assessment)

- **expansion: improved** — 2 net new rows (one admit tier A, one logged reject), new `corpus/knowledge/receipt-integrity.md` on uncovered receipt-integrity ground citing S133 (sourced-claim requirement met), two Mistakes rows, new instruments (driver v2, counter v6, matrix, freshness runner). Agree with the report.
- **quality: improved** — three HIGH latent gate defects closed with named-class refusals and an unchanged honest-cohort verdict; v4 receipts mode-accurate (b leg); the witness-split figure now re-derives from the receipt it names. Found-false standing claims were marked, not left unmarked. Agree with the report.
- **discernment: improved** — my outside spot-check agrees with both gate decisions; the lane falsified its own frozen claims twice and reported them as falsified; both falsifications became grounded Mistakes rows (14, 15) with captured-by and able-to-fail fixes. Agree with the report.

## Admission and routed items

Both declared claims are **NOT MET as declared** (C1 causal clause unfalsifiable as declared — bounded repair verified, disposition routed; C2(c) falsified — correction filed, legs (a)/(b) verified). Per the round contract ("every claim verifies — … Report all verdicts and let the operator rule") and the closure rule (`admitted` only if every claim verifies), admission is **false** with verdict **rejected-honest-stop**: the lane stopped honestly, filed corrections append-only, harmed nothing, and routed the disposition (C1 trust boundary) to the operator via the L0 channel. The bounded repairs are real, re-measured progress and are recorded in the trend verdicts; they do not convert the round's declared claims into met ones.

Routed defects the lane must fix next round:
1. **Dead short-hash citation** — report/Landed-changes cites `e5455253`; the wave-2 registry commit is `e54552553eaff4d7033dc2df299300fc056f4a0d`. Cite unambiguous prefixes or full hashes.
2. **C1 trust boundary** — operator ruling pending on the L0 question; round 46 must reflect the ruling in SCORECARD/QUALITY (bounded trusted-local-counter reading vs counter-side causal provenance).
3. **Receipt-identity binding** — per Mistake 15's own fix, any future filed count against a receipt must cite path + sha256; verify this becomes a QUALITY.md criterion in round 46.
4. Minor: the `--stage after` matrix re-run on a full clone exceeds 4 minutes of wall clock (honest-cohort re-certification); not a defect, but size round-46 re-run budgets accordingly.

Tool installs this closure: none (git, jq, curl, python3 pre-existing; no pacman transaction).
