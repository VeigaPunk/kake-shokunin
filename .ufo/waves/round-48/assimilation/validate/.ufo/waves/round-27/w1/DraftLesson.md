# DraftLesson — r27 draft lesson (Claims / Gate / Mistakes) + QUALITY criterion for the omitted grouped S001–S006

Seat `KakeR27.DraftLesson` (scribe, leaf, no dispatch). Axis judged: **freshness** (secondary context: operability). Scope:
**report-only** — no production file edited (no `corpus/lessons/round-27.md`, `corpus/QUALITY.md`, `corpus/knowledge/*`,
`scripts/*`), no git/jj mutation, no commit, no build/lint/test/selftest run, no tool installed (none needed; pacman is
host-paused). Path: `.ufo/waves/round-27/w1/DraftLesson.md`.

## 1. Axes

- **freshness** — make the citing set enumerable and give the six omitted grouped pairs `(S001…S006,
  corpus/knowledge/static-canonical-preflight.md)` plus every other enumerated pair a durable, source-grounded adjudication.
  Must not: re-open r26, re-adjudicate r26 verdicts, or treat a green counter as completion.
- **operability** — state the fail-closed requirement (an enumerated, unadjudicated citing pair ⇒ non-zero exit). Must not:
  implement the gate (owned by `KakeR27.BuildGate`/`BuildSelftest`) or pre-judge their exit codes.
- **both** — keep the denominator monotone and the oracle frozen: no weakening of `c2-oracle.json`, no narrowing of the
  16-pair oracle to the grouped six, no rewriting of `expected.json` to candidate output.

## 2. Baseline facts actually observed (not planned)

Frozen revisions: base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations
`be375d90afc6fc7aca369ab3cf5247bf460aeed2` (both `git cat-file -t` → `commit`; `git log --oneline -2` = `be375d9 round-27:
freeze full citing-set claims and independent oracles`, `83528f7 round-26 verifier spot-check (integrator, hyaku): non-author
admit/reject`).

**2.1 Baseline 41/57 + 16 omissions.** `.ufo/waves/round-27/c1-before.json` (sha256 `af55d0a4bb1aa9b…`) at base:
`population 32`, `citingPairs 57`, `decided 41`, `r26CarriedPairs 41`, `newDecided 0`, `missing` = 16 pairs, `findings []`.
An independent read-only recomputation at the same revision (Python over `git show` blobs, same literal/range rules, nothing
written) reproduced **57 citing / 41 decided / 16 missing** and the same 16-pair list. Ranges present in `corpus/knowledge/`:
`publish-channels.md` `S001-S007`; `sitemap-orphan-audit.md` `S001-S006`; `static-canonical-preflight.md` `S020-S027`,
`S028-S029` (hyphen-minus) and **`S001–S006` (en dash U+2013)** at `static-canonical-preflight.md:54`, whose text reads
"Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed checkout served set"
(20 words; line continues `… (S001–S006, `ghp-served-set.md`).`).
All six grouped pairs are **present in the citing set and absent from the r26 ledger** (no `S003`/`S004` pair for
`static-canonical-preflight.md` exists in `statements.json` at base) — they are **6 of the 16**; the other **10** are
`S003|sitemap-orphan-audit.md`, `S004|publish-channels.md`, `S005|sitemap-orphan-audit.md`, `S006|publish-channels.md`,
`S008|` × 4 (`crawl-scope-per-host.md`, `ghp-custom-domain.md`, `ghp-etag-anatomy.md`, `static-canonical-preflight.md`),
`S022|static-canonical-preflight.md`, `S023|static-canonical-preflight.md`.
`.ufo/waves/round-27/c2-oracle.json` (sha256 `1d038205473180c7…`) freezes exactly those **16** pairs, `expectedExit 1`,
`expectedFinding unadjudicated_citing_pair`, `expectedCount 16`, `falsePositives 0`.

**2.2 r26 exit 0 on the same bytes (fail-open).** `.ufo/waves/round-27/r26-fail-open-before.json` (sha256
`40fbeb3f6e197ef6…`): `python3 -B .ufo/waves/round-26/measure.py --root . --revision 83528f7c…` → **exit 0**, `decided 32`,
`expected 32`, `findings []`, `hold 32`, `populationSha256 16330e1effd5ee52665f8f31738e9423c6ec387e5d4a1404c5bcc35f69d01b03`.
The r26 counter is green on the revision that still leaves **16 citing pairs unadjudicated**.

**2.3 r26 ledger size; 313 is not retroactively enlarged.** `statements.json` at base (blob sha256 `c2026376832ad4e4…`):
**41** pairs; totals `statements 313`, `stale 7`, `reclassified 4`, `seatUnverifiable 6`. `skillTails` is a separate object
(`statements 11`, `hold 7`, `staleAlreadyCorrected 4`) — outside the 313.

**2.4 r26 non-author verdict (retained).** `corpus/lessons/round-26-verifier-spotcheck.md` (sha256 `94c43088b995f30a…`):
`:9` "Status ok (real report); admitted false; rejected-honest-stop." (9 words) · `:11` "the grouped **S001–S006** claim at
`corpus/knowledge/static-canonical-preflight.md:53–54` remains outside the final ledger and has no recorded final adjudication"
(23 words) · `:13` "It does not establish that the grouped recommendation is false. It establishes an unproved part of the frozen
full citing-set clause." (23 words) · `:119` "Do not retrofit this review into the author's 313 units or treat it as author
completion." (15 words) · `:120` "Keep the two-executor W1 floor failure disclosed; future build waves meet the required minimum
before dispatch" (17 words) · `:121` "Gate counts do not prove semantic correctness, perpetual HOLD, authenticity or live-site
conformance." (13 words) · `:123` "Open L0: prior **round-24 policy-stop disposition** remains unresolved."

**2.5 The omission was already named in r26 seats (not a new standard).** `w1/ClaimCritic.md:53` "the range citation `S001–S006`
at `static-canonical-preflight.md:54`" · `w2/CounterCritic.md:147` "Add pairs and seats for the unjudged citing set" … "plus the
`S001–S006` range at `static-canonical-preflight.md:54`" · `w1/PairS001GhpServedSet.md:75` "S001 is also cited (plain ID search,
not judged) in …" (usedBy-vs-actual-citers gap).

**2.6 W1 executor floor (historical debt).** `.ufo/reports/round-26/kake.md:25` "W1 has two executor seats, below the prompt's
three-executor minimum." (11 words) and "no padding or retrospective relabelling is claimed"; verifier `:120` carries it as a
required next-round defect. r27 `contract.json` requires **3 explicit executor writers, each with a real separate worktree,
unique branch/path, observed base `be375d90afc6fc7aca369ab3cf5247bf460aeed2`**.

**2.7 Sources opened this round for S001–S006.** `.ufo/waves/round-27/fetched/manifest.json` (sha256 `d3b0b1ca215bfa6d…`):
**8** payloads, all gzip bytes present and sha256-matched to the manifest — `S001-1` `4524ed61c2fb…`, `S001-2` `e8ce828a4f2e…`,
`S002-1` `43d5e22d3d02…`, `S002-2` `bc5d74856acf…`, `S003-1` `f42d48b59277…`, `S004-1` `9ee0766a2fb7…`, `S005-1` `6f3d1ad215c9…`,
`S006-1` `f0318abe7e63…`. This seat verified presence and digests only; it did **not** adjudicate against them.

**2.8 C2 pre-state.** `.ufo/waves/round-27/c2-before.json` (sha256 `853a6b07d28d845a…`): at `be375d90…` the oracle run exits
**1** with `finding: gate_absent` (`scripts/citing_set.py` does not exist at that revision). No exit code is predicted here.

**2.9 Observation about the frozen scripts (not mine, not a verdict).** `git status` shows the working-tree copies of
`.ufo/waves/round-27/count_c1.py` and `c2_count.py` **modified** relative to the freeze (a monotone-baseline rule plus
`--selftest` dispatch; committed digests `a1e46d19b438fc25…` / `93f39b0f7187fa08…` vs working-tree
`7ebb3f366f72f53…` / `e5b6fa7f2e850225…`). My §2.1 recomputation used the **committed** (frozen) semantics and reproduces
`c1-before.json` exactly. Which copy the L1 freezes is an integration decision, not a scribe call.

## 3. Draft lesson text (report-only; L1 lands it or not)

### Claims
**C1 — freshness (r27).** The reviewed citing set is the set of `(source row, citing file)` pairs the corpus *implies*: every
literal `S###` in a knowledge file plus every row of a grouped/range citation `S###–S###`, each against the containing file.
At frozen base `83528f7c…` that set is **57 pairs over 32 inherited rows**; the r26 ledger carries **41**; **16 are
unadjudicated**, six of them the grouped `S001–S006` range at `corpus/knowledge/static-canonical-preflight.md:54`. The r27
obligation: every one of the 57 — plus any pair newly discovered and added monotonically to `discovered-pairs.json` — has a
durable **HOLD / STALE / UNVERIFIABLE** adjudication in a ledger row, `UNVERIFIABLE` explicit and never counted decided. A
grouped recommendation may be local synthesis: each source's contribution and each inferential step must be labelled, and no
individual source may be pretended to entail the group alone. **Adjudicating a pair is not proof that every statement in that
file is true** — it is a located, scoped judgment about that pair at its stated scope.
**C2 — operability (r27).** A range-aware citing-set completeness gate detects exactly the **16** frozen missing pairs with
**0** false positives and exits non-zero (`unadjudicated_citing_pair`) on the inherited r26 set, while exiting 0 on a complete
positive fixture. The r26 counter's green result on the incomplete set is preserved as the captured fail-open witness; C2 is
measured against the **unchanged r26 ledger**, so it stays independent of the C1 adjudications.

### Gate
1. **Enumerate** the citing set from `corpus/knowledge/*` at a measured revision: literal `S###` tokens plus range-expanded `S###–S###` (hyphen/en-dash/em-dash/`..`/`to`/`through`), intersected with the inherited 32-row population; historical metadata and r26 EOF prose included. Result at base: 57 pairs.
2. **Adjudicate each enumerated pair** with a ledger row: verdict, reason, located support (source: fetch index, ≤25-word quote, anchor; artifact: repo evidence path + contained substring). `STALE` additionally requires `[r27-recheck S0NN STALE]` appended in the citing file.
3. **Count independently**: `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision <commit>`; decided = r26 pairs carried explicitly + r27 additions; `UNVERIFIABLE` never enters the decided count; the denominator may only grow.
4. **Fail closed on completeness**: `python3 -B .ufo/waves/round-27/c2_count.py --root . --revision <candidate>` against the frozen oracle (16 pairs, exit 1, 0 false positives); altered pinned bytes ⇒ `snapshot_tampered`, exit 2.
5. **Report gaps as gaps**: UNVERIFIABLE and unadjudicated pairs print as findings, never rounded into "clean".

### Mistakes (r26 → r27)
| Class | Evidence | Captured by | Fix / fail-capable witness |
|---|---|---|---|
| fail-open | r26 exit 0 with 16 citing pairs unadjudicated (`r26-fail-open-before.json`) | r27 pre-state capture | citing-set gate exits non-zero on the frozen 16; oracle pins count 16, exit 1, false positives 0 |
| range-blindness | grouped `S001–S006` at `static-canonical-preflight.md:54` never enumerated; all six pairs absent from `statements.json` | r26 `ClaimCritic.md:53`, `CounterCritic.md:147`, verifier `:11` | range/group expansion; each enumerated pair gets its own ledger row |
| registry-cell scope | ledger followed `usedBy` cells only, so plain-ID citers outside the cell went unjudged | r26 `PairS001GhpServedSet.md:75`; r26 lesson "coverage" row | citing set derived from corpus text, not registry cells (extends QUALITY 231–233) |
| over-claim of completion | a green structural counter existed while the frozen full citing-set clause was unproved | verifier `:121` | verdict language names the unproved clause; no PASS from plan or shape |
| scope drift (r26, retained) | r26 seat scratch deviations (`/tmp`, `/dev/shm`), prose-offset errata, manual completeness limits | r26 report; verifier `:121` | r27 scratch is `/fast/scratch/hyaku/kake-r27/<seat>/`; deviations stay disclosed |
| conformance (r26, retained) | r26 W1 had 2 executor seats vs 3 required | r26 report `:25`; verifier `:120` | r27 dispatches 3 executor writers with separate worktrees; no padding/relabelling of the r26 defect |

### Measurement
The numbers in §2 are measured at `83528f7c…`: **41 decided / 57 citing pairs / 16 missing**; r26 exit **0**. The r27 "after"
numbers are **not** asserted here: they must come from `count_c1.py` and `c2_count.py` runs at an integrated revision, executed by
L1 after integration.

## 4. Draft QUALITY criterion (for `corpus/QUALITY.md`, round-27 section — L1 to land; not applied here)

Basis, verbatim `corpus/QUALITY.md:231-233` (sha256 `fd5065a1da106949…`): "A recheck covers every corpus statement that cites a
rechecked row, not only files listed in `usedBy`; derived locators (offsets, digests) are re-derived after any extractor change."
Draft criterion to append:

> - The reviewed citing set is **corpus-implied, not registry-implied**. A knowledge file containing `S###` cites that row; a
>   grouped or ranged citation `S###–S###` cites **every** row in the range, in that file. Each implied `(row, file)` pair needs
>   its own durable adjudication — HOLD, STALE, or explicit UNVERIFIABLE — in a ledger row. A verdict covers its pair at its
>   stated scope only; it is not proof that every statement in that file is true, and UNVERIFIABLE is never counted as decided.
> - A recheck count that enumerates only registry `usedBy` cells (or only row receipts) does **not** satisfy this clause. The
>   citing-set completeness check must **fail closed**: an enumerated but unadjudicated pair is a finding and the run exits
>   non-zero. Green row counters and green fixtures do not substitute for it.
> - Extending round 26's rule (QUALITY 231–233): range/group expansion adds citing obligations and may only enlarge the
>   denominator; a later round may not quietly shrink it, and r26's frozen 313-unit ledger is carried forward as 313, not
>   re-counted or retroactively enlarged.

The criterion is fail-capable by construction: §2.2 is the pre-state (r26 exit 0 with 16 missing pairs); `c2-oracle.json` pins
the post-state (16 detected, exit 1, 0 false positives).

## 5. Retained rejections and non-retroactive constraints

- **r26 stays rejected-as-admitted-false** (verifier `:9` "Status ok (real report); admitted false; rejected-honest-stop."). r27 does not re-open, re-adjudicate or admit r26; it answers r26 next-round defect 1 (`:119`) with new r27 adjudications.
- **r26's 14 rejected seat proposals stay rejected** (r26 lesson "Statement-level admissions and rejections": anchor drift in pointers explicitly scoped "at base cb807bc", verification-date stamps, Python 3.15.0→3.15.1 labels, S021 fragment wording). r27 converts no rejection into a HOLD or a STALE.
- **313 units stay 313.** r27 adjudications are new rows in `.ufo/waves/round-27/pairs.json`; r26's `statements.json` is carried explicitly and never relabelled as a fresh r27 source observation (contract `C1.ledger`; verifier `:119`). The SKILL-tail review (11 units, outside the 313) is untouched.
- **The oracle is frozen.** `c2-oracle.json` (16 pairs) and `frozen/expected.json` (sha256-pinned snapshot) are inputs, not outputs; if the gate cannot satisfy them, the outcome is disclosed as UNPROVABLE, not by editing `expected.json`.
- **r24 L0 stays unresolved and untouched** — no r24 probe/counter read, retried, rephrased or rerouted. **The r26 W1 executor-floor defect stays disclosed as historical debt**, not repaired by padding or relabelling.

## 6. Uncertainties; what this seat does not claim

- **No adjudication verdicts are produced here.** The six grouped pairs are enumerated and sourced, not judged; HOLD / STALE / UNVERIFIABLE is for the C1 adjudication seats and L1, on the 8 payloads in `fetched/manifest.json`, with quote/anchor recorded.
- **No PASS is asserted for C1 or C2** — both are unimplemented/unrun at the revision observed (`c2-before.json` → `gate_absent`); r27 "after" numbers are unknown to this seat.
- **16 vs 6**: the oracle covers all 16 missing pairs; the grouped `S001–S006` are 6 of them. Narrowing the oracle to the grouped six would weaken scope and is not proposed. **Discovered pairs are not enumerated by this seat**; `discovered-pairs.json` did not exist at `be375d90…`. If a seat finds another valid citing form the denominator grows and the oracle count must be revisited honestly, not silently dropped.
- **The r27 executor count was not audited** here (the roster snapshot shows `KakeR27.BuildGate` and `KakeR27.BuildSelftest` as executor seats; whether the wave dispatched exactly three, each with a separate worktree, is an L1/registry fact).
- **General qualifier** (verifier `:121`): gate counts do not prove semantic correctness, perpetual HOLD, authenticity or live-site conformance. A HOLD on a pair is dated and scoped.
- **No production edit, no test run, no tool install, no git/jj/fleet mutation.** Only this report was written.

## 7. Evidence index

| Item | Path / ref | Digest or locator |
|---|---|---|
| Frozen contract | `.ufo/waves/round-27/contract.json` | `C1`/`C2`/`gateInterface`/`r26Record`/`originalTargetRule` |
| C1 counter (frozen / worktree) | `.ufo/waves/round-27/count_c1.py` | `a1e46d19b438fc25…` / `7ebb3f366f72f53…` (§2.9) |
| C1 pre-state | `.ufo/waves/round-27/c1-before.json` | `af55d0a4bb1aa9b21bc2ce026035beaf21e523458661252f8a520008f2ec6e3c` |
| C2 oracle | `.ufo/waves/round-27/c2-oracle.json` | `1d038205473180c7cb57895c2d480a8b52debe3bf08ab0a2f58ca7b1f67bc7dd` |
| C2 counter (frozen / worktree) | `.ufo/waves/round-27/c2_count.py` | `93f39b0f7187fa08…` / `e5b6fa7f2e850225…` (§2.9) |
| C2 pre-state | `.ufo/waves/round-27/c2-before.json` | `853a6b07d28d845ab44d230aa5c64d33645bddf0755424a0504b4c6527e1f4ba` |
| r26 fail-open witness | `.ufo/waves/round-27/r26-fail-open-before.json` | `40fbeb3f6e197ef6c5cea021d980c1d4cf9853e24a7fe5d8400f5abb0091eec7`; exit 0 |
| r26 ledger | `.ufo/waves/round-26/statements.json` @ `83528f7c…` | blob `c2026376832ad4e4114d1bc19abeec4fcbdbd0fea3dbb102ab8a5c2eb18c95ce`; 41 pairs / 313 / 7 / 4 / 6 |
| r26 non-author verdict | `corpus/lessons/round-26-verifier-spotcheck.md` | `94c43088b995f30a6128014f42d97e6145bfac3191442aa9026f2d1c5c2e5bda`; lines 9, 11, 13, 119–121, 123 |
| QUALITY bar | `corpus/QUALITY.md:231-233` | `fd5065a1da1069494ce4faf9e912728487e3fc766bd000a1a81cb071a4a1d2e8` |
| Grouped claim | `corpus/knowledge/static-canonical-preflight.md:53-54` | `833b28f26fa7309f7e31398275bae2f704969d8e6f095bc5bb96250da5c531bc` |
| r26 report (executor floor, 313) | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-26/kake.md:11,25` | line 25 quote above |
| Sources opened this round | `.ufo/waves/round-27/fetched/manifest.json` | `d3b0b1ca215bfa6d89edf639b2b87475d668fdf73cbf0ddf089c87e11d043781`; 8 payloads, digests matched |

**Report trailer — Report: `.ufo/waves/round-27/w1/DraftLesson.md`**
