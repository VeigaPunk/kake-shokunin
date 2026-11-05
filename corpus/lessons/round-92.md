# Round 92 — kake: the round-91 instrument defects, and a heuristic freshness decision

Author: kake L1 (`KakeR92`). Base `e143faff1b86aad172dd87696da900c70347b8b2`; freeze
`a5640ca02c20f94a0fa03af41b977b46ae99808e` (`.ufo/waves/round-92/freeze.md`); carrier
`2a4447c1a4696cbfb40b17014e47fc6af716c06d`. Outside closure owns admission and the
non-author spot-check of this Gate.

## Gate

Source opened this round (CORPUS.md rule 1), by `w1/ScoutSources` with a live GET:

| URL | HTTP | bytes | sha256 | opened |
|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 200 | 84 477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 2026-11-05T00:30:13Z (2026-11-04 local) |

`cmp` against the retained `L1/src/rfc9111.txt` is identical (exit 0), so the retained
body and the fresh fetch agree byte for byte. This also settles the round-91 routed
provenance question (K91-7): the row below rests on a fetch of this round.

Admits:

- **S470 admit, A, §4.2.2 line 689–690** — "a cache MAY assign a heuristic expiration
  time when an explicit time is not specified" (15 words). Grounds the permission clause.
- **§4.2.2 lines 695–696** — "A cache MUST NOT use heuristics to determine freshness when
  an explicit expiration time is present in the stored response." (20 words). Grounds the
  `explicit` decision taking precedence.
- **§4.2.2 lines 697–699 and 700–701** — "heuristics can only be used on responses
  without explicit freshness whose status codes are defined as "heuristically cacheable""
  (18 words) and "on responses without explicit freshness that have been marked as
  explicitly cacheable (e.g., with a public response directive)." (18 words). Grounds the
  cacheability gate and the `public` override.
- **§4.2.2 lines 707–708 and 709** — "caches are encouraged to use a heuristic expiration
  value that is no more than some fraction of the interval since that time." (22 words)
  and "A typical setting of this fraction might be 10%." (9 words). Grounds the 10 %
  fraction as a *typical* setting, not a requirement.

Rejects:

- **Reject (proposition): "the 86400-second cap is RFC 9111's".** §4.2.2 imposes "worst-case
  constraints on their results" but names no value; the cap is the lane's adapter
  convention and the contract and entry say so. Flip: a section that names a bound.
- **Reject (row candidate): a second row for the heuristically-cacheable status set.**
  §4.2.2 defers to "Section 15.1 of [HTTP]" and does not list the codes; a row would have
  to cite RFC 9110 §15.1, not this one. Flip: a row whose anchor is the RFC 9110 §15.1
  text itself.
- **Reject (row candidate): a row for the RFC-Editor errata page.** Four records exist
  (9004, 9185, 9166, 7695) and none names §4.2.x, so it grounds nothing about this
  ground. Flip: an erratum touching §4.2.2.

## Registry

- Row added: S470 (tier A, kind spec, status mined, recheck 180d), `used-by`
  `corpus/knowledge/heuristic-freshness.md`. 206 → 207 rows.
- Rows touched: none.
- Census `validate --root … kake`: exit 0 before (`.ufo/waves/round-92/assimilation/census-before.txt`)
  and exit 0 after; W04 advisories 30 → 31 (S470 is a fourth scope on the same RFC text).

## Mistakes

| # | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| 1 | A control resolved its carrier from a ref the clone did not carry | the known-good fixture's replay read `carrier-open=2` and `self=hit`: `git clone` of a detached-HEAD repo produced a clone with no local `master`, so the harness's `${CARRIER:-$(git rev-parse master)}` fell back to the base | the pre-freeze known-good run `controls/ctl-c1-known-good.txt`, before the freeze commit | `clone_at()` now pins `refs/heads/master` to the root's master (`update-ref`) after every clone; FA then read its exact set `{A}` instead of `{A,C}` |
| 2 | A sandbox denied a mechanism the runner itself needs | the known-good C2 subject scored `hand=5/28`: the audit hook refused the builtin `exec` event, which `runpy` raises while loading the subject | the pre-freeze C2 positive control `controls/ctl-c2-positive.txt` | the hook now denies only process creation (`os.system`, `subprocess.Popen`, `os.spawn*`); the same subject reads `28/28 120/120` |
| 3 | A declared label was the label of a different mode | the harness printed `base-open=2` where the freeze declared `base-open=3`: the replay runs the counter with `--skip-replay`, which leaves item C out of the open set | the replay's own label assertion (item C) | the declared set is `base-open=2`; the positive fixture now reads the exact nine labels |
| 4 | A refusal fired for the wrong reason, so the fixture proved nothing about its class | the canned-runner fixture FB was refused as "observed ≠ log" instead of "base and mutant do not differ", because the log comparison ran first | the battery's declared reason substring for FB | the "do not differ" check now precedes the log comparison; FB's reason names the canned class |

| 5 | A round committed its work and then ended without a report | attempt 1 landed `a5640ca0`…`9f15115b` and ended at 21:58:46 with no `.ufo/reports/round-92/kake.md`; `.ufo/watchdog.log:2603` reads `lane-dead-no-report kake round=92` | the driver's `report_of` content gate — it fired on this very round and relaunched attempt 2 (`watchdog.log:2604`) | none beyond that gate; attempt 2 re-ran both frozen counters at the base and at the carrier (`controls/attempt2-reverify.txt`) before filing, and changed no counter, case, predicate or label |

Disclosure: mistakes 1–4 were found and fixed before the freeze commit; no counter, case,
predicate or label was changed after it. Every instrument defect the wave found is routed
below, not patched. Mistake 5 is a close-order defect of attempt 1, recorded by attempt 2.

## Attempt 2 — inherited state

Attempt 1 (21:13–21:58) committed the freeze, the wave-1 spec and dispatch, the wave-1 evidence,
the instruments, the registrations and the SCORECARD/LOG/lesson sections; it ended before the
report. Attempt 2 re-verified rather than re-did: both frozen counters reproduce their carrier
readings exactly (`open=0 closed=3 … met=true`, `hand=28/28 120/120 5/5 … met=true`, both exit 0)
and their base readings exactly (`open=3 … met=false`, `candidate=absent … met=false`, both exit
1) — receipt `controls/attempt2-reverify.txt`; the lane tree was clean at the tip, so nothing
inherited was discarded. No claim, counter, case, predicate, label, receipt or wave artifact was
changed by attempt 2; the only additions are that receipt and this note.

## Wave review (w1, 14 seats) — what the attack seats found

Thirteen seats returned reports or receipts; `SentinelQuote` settled with no file in its
directory (dead seat, named in the report).

- **ReviewC1 falsified the frozen C1 counter three ways**, each reaching `met=true` in a
  fixture clone: a runner that mutates nothing and prints canned per-target verdicts, a
  control harness that echoes the nine frozen labels, and a counter blob edited with its
  self-pin rewritten in the same commit (`w1/ReviewC1/Attack.md`, classes 3, 5c, 6).
- **CriticClaims built three more**: a receipt whose log and runner execute a *different*
  gate than the digest names (F1 `333230ce`), a registry row naming a counter that refuses
  every revision (F2 `605a0026`), and a harness whose labels are constants (F3). It also
  confirmed C1/C2 separability in both directions and measured the do-nothing control at
  the freeze (`open=3`, `candidate=absent`, both `met=false`).
- **ExecMutation** landed item A's artifacts (N=30, K=20, S=10, digest equal to the gate
  blob) and found that only one mutant line is ever executed, so a forged unsampled line
  is admitted.
- **ExecStubs** scored 14 held-out subjects: both contract-faithful ones read `met=true`,
  seven clause-violating ones are refused, **five are admitted** (clauses 2, 3, 4, 6, 8
  uncovered), and the counter's own reference accepts a quoted delta-seconds argument,
  which contract clause 4 refuses.
- **MutHeuristic**: 13 of 24 single-clause tool mutants survive the frozen counter, and 9
  hand-built clause-violating subjects read `met=true`; the sandbox, the forgery battery
  and the population pins hold (4 of 16 counter mutants are killed by a frozen subject).
- **ReviewC2** computed 97 cases from the contract alone and measured the delivered tool at
  93/97 with **0 tool defects**; all four disagreements resolve to three contract
  ambiguities it named before running.
- **ExecTrial** decided the twelve recorded round-61 surfaces and the r81/r82 captures
  through the new instrument and tabulated the headers each decision rests on.
- **ScribeEntry/ScribeRegistry** landed the knowledge entry (480 lines), the SKILL.md
  registry rows, the README frontier section and the S470 draft; **ConnectorScope** found
  no sibling lane holds §4.2.2 ground and confirmed S470 is not a within-scope duplicate;
  **ScoutSources** fetched the RFC, checked four errata and quoted §4.2.2;
  **ScoutGround** mapped the insertion points and the `heuristic-undecided` seam in
  `scripts/stored_reuse.py`.

## Routed

Carrier `2a4447c1`: both counters read `met=true` on their frozen predicates
(`controls/after-c1-carrier.txt`, `controls/after-c2-carrier.txt`). The wave falsified
what those predicates *mean*; nothing was repaired after scoring.

- **R92-1 (C1 item A, unbound execution).** The runner is invoked with no gate argument,
  so it may execute any subject; only one mutant line is ever re-executed. A successor
  must pass the gate path and the mutant id to the runner, re-execute a *sample chosen
  after* the receipt is read, and bind each log line to the mutant's own source digest at
  the measured revision. Evidence: `w1/CriticClaims/C1.md` F1, `w1/ReviewC1/Attack.md`
  class 3, `w1/ExecMutation.md`.
- **R92-2 (C1 item C, labels not derived).** Item C asserts the nine label values but not
  that they were produced by runs; a constant printer passes. A successor must make the
  harness emit a nonce per run and bind each label to an artifact the counter can re-derive
  (a counter output line and its digest). Evidence: `w1/CriticClaims/C1.md` F3,
  `w1/ReviewC1/Attack.md` class 5c.
- **R92-3 (C1 item B, text-only).** A registry row is a text predicate: a row naming a
  counter that refuses every revision satisfies it. The claim should say "registered", not
  "registered and correct", or the successor must resolve the row's command and run it.
  Evidence: `w1/CriticClaims/C1.md` F2.
- **R92-4 (C2 population coverage).** The frozen population leaves clauses 2, 3, 4, 6 and 8
  unexercised: 13 of 24 tool mutants survive and 9 violating subjects are admitted. A
  successor needs one case per clause and per refusal class, and a type-mismatch case for
  clause 3. Evidence: `w1/ExecStubs.md`, `w1/MutHeuristic/Mutations.md`.
- **R92-5 (C2 reference drift).** `c92_heuristic.py`'s reference accepts `max-age="5"`
  where contract clause 4 requires a refusal; the delivered tool refuses it, so the
  counter is *weaker* than the subject it scored. A successor's reference must be checked
  against the contract by an independent reader before the freeze. Evidence:
  `w1/ExecStubs.md` F6, this round's direct probe.
- **R92-6 (dead seat).** `SentinelQuote` settled with no file in
  `.ufo/waves/round-92/w1/SentinelQuote/`; its quote and scope checks were not performed
  and the entry's quotes are verified only by ScribeEntry and ScoutSources.
- **R92-7 (carried).** Round-91 items K91-3, K91-6, K91-8, K91-9, K91-10 stay open; K91-7
  is answered by this round's live GET (`Gate` above).
