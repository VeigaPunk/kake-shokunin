# LostFindingTrace — r27 W1 (KakeR27.LostFindingTrace, 2026-10-21)

Seat: read-only trace. Inputs: r26 `w1/ClaimCritic.md`, `w1/PairS001GhpServedSet.md`,
`w2/CounterCritic.md`, final `round-26/statements.json`, final verifier
(`corpus/lessons/round-26-verifier-spotcheck.md` @83528f7, fleet `MANIFEST.json` kake
round-26 closure entry); grounding reads of `round-26/measure.py` (final), rechecks
S017/S018, `corpus/lessons/round-26.md`, SCORECARD.md, and the frozen r27 corpus
snapshot. No r24 reads/work. No edits, no installs, no builds/tests; read-only git
(`diff --stat`, `log`) only. Scratch: none (no files created outside this report).

## 1. The finding left unadjudicated (exact reconstruction)

**Finding:** the grouped range citation `S001–S006` at
`corpus/knowledge/static-canonical-preflight.md:54` — sentence "…manifest over actual
built/deployable HTML when that artifact exists, not over an assumed checkout served set
(S001–S006" — produced six citing pairs (S001…S006, static-canonical-preflight.md) that
received **no recorded adjudication anywhere in round 26**: absent from the final
`statements.json` ledger (41 pairs / 313 statement units), absent from every pair seat
and from the w2 falsify-wave additions.

**Chain across the three named anchors:**
- `w1/ClaimCritic.md:53` (item 8, "pair coverage is narrower than the citing set"):
  "the range citation `S001–S006` at `static-canonical-preflight.md:54`" — listed with
  the unjudged literal citing lines (:48–52), demanding a unit "N statements across the
  full citing set, list pinned" (:127) and correction blocks "in every citing file …
  not just usedBy" (:104).
- `w1/PairS001GhpServedSet.md:75` (Flags for L1): S001 "also cited (plain ID search,
  not judged) in SKILL.md:229; corpus/README.md:28,60; knowledge/ghp-subpath-spotcheck.md:1,95;
  knowledge/publish-channels.md:1,2,58,60; knowledge/sitemap-orphan-audit.md:1,2,120-127;
  knowledge/speedrun-pipeline.md:1,70; knowledge/static-canonical-preflight.md:54;
  lessons/round-7.md:57-65; lessons/round-20.md:203,261; lessons/round-21.md:45".
- `w2/CounterCritic.md:147` (correction item 1, "Data or claim (required for the claim
  as written)"): "Choose one: Add pairs and seats for the unjudged citing set … plus the
  `S001–S006` range at `static-canonical-preflight.md:54`. Or, minimally, rescope … and
  record ClaimCritic item 8's excluded citing lines as named, unjudged debt."

**What r26 did with it:** the falsify wave adjudicated the *literal* enumerated pairs —
14 new pairs / 37 units, all HOLD except S024 (2 STALE) (`statements.json`
w2Adjudication; w2/UncoveredS024S025.md, L1 KakeR26-2). It did **not** adjudicate the
grouped range. Final verifier (CloseKaidoku23, non-author): "The grouped **S001–S006**
claim at corpus/knowledge/static-canonical-preflight.md:53–54 remains outside the final
ledger and has no recorded final adjudication. … All six (S001…S006,
static-canonical-preflight.md) pairs are absent from final statements.json. The added 37
units fix the other named omissions, not this one" (round-26-verifier-spotcheck.md:11-13).
The verifier's independent sweep: 43 literal (source,file) pairs vs 41 listed; "its only
unlisted literal endpoints are S001 and S006 in the grouped citation"; expanding the
range exposes all six unlisted pairs (spotcheck "Independent before → after
measurements"). The author's closure response "confirmed that no durable final
adjudication exists" (spotcheck:15).

**Final disposition in r26:** verdict `rejected-honest-stop`, `admitted: false`; freshness
axis "unprovable" (the frozen contract clause "knowledge-entry claims citing the rows
rechecked" is unproved, not refuted — "It does not establish that the grouped
recommendation is false"). Required next-round defect #1: "Give the grouped S001–S006
citation a recorded, source-grounded judgment and expand grouped/range citations when
defining the reviewed citing set" (spotcheck "Required next-round defects"). Recorded in
fleet `MANIFEST.json` kake round-26 closure entry (verdict/finding/commit
kake-shokunin@83528f7c…, i.e. contract.json:32 "verifier83528f7,MANIFEST[430]") and
SCORECARD.md:533 ("r26 author-side verify claim above is superseded by non-author
rejected-honest-stop … 313 units are not retroactively completed"). r26
report/contract/ledger/receipts/waves unchanged; correction belongs to r27
(contract.json r26Record).

## 2. Composition of the 16 still-missing pairs at the frozen base (grounded)

count_c1.py at 83528f7 (c1-before.json): citingPairs 57, decided 41, missing 16. The 16
decompose exactly (all locations read in the frozen snapshot
`.ufo/waves/round-27/frozen/corpus/knowledge/`):

| pairs | grounding location | named in r26 reports? |
|---|---|---|
| S001–S006 × static-canonical-preflight.md (6) | :54 range "(S001–S006, `ghp-served-set.md`)" | Yes — the core finding (ClaimCritic:53, PairS001:75, CounterCritic:147, verifier) |
| S022, S023 × static-canonical-preflight.md (2) | :2 range "verified-at: 2026-10-20 (S020-S027)" | No r26 report named this range |
| S004, S006 × publish-channels.md (2) | :2 range "round-20 corrections 2026-10-19 (S001-S007 opened that day)" | No — r26 named only :58-61 literals (S001,S002,S003,S005,S007; w2-adjudicated) |
| S003, S005 × sitemap-orphan-audit.md (2) | :2 range "r20 S001-S006 quote corrections 2026-10-19" | No — r26 named :120-127 literals (S001,S002,S004,S006; w2-adjudicated) |
| S008 × static-canonical-preflight.md (1) | :184 r26 EOF prose "S008 via `manifest-retry.json`" | No |
| S008 × crawl-scope-per-host.md, ghp-custom-domain.md, ghp-etag-anatomy.md (3) | :57, :62, :60 r26 EOF recheck paragraphs, same "S008 via" prose | No |

So the r26 critics' enumeration covered 20 of 21 affected pairs by location (the 14
literal sets + the grouped range); the frozen r27 enumeration adds 10 pairs from three
metadata-line ranges and four S008 mentions inside r26's own appended recheck prose.
Denominator grows monotonically (57 ≥ any r26-local count); nothing was shrunk.
Verifier-scope note [INFERENCE on method]: the verifier's "43 literal" sweep is
consistent with a base-era byte set (pre-r26-append prose) — stated as recorded, not
re-derived by me; the frozen 57 includes ranges + r26 append prose by
count_c1.py's declared scope.

## 3. Other unresolved citing-set findings in the named reports, with current disposition

| # | Finding (report:anchor) | Current disposition |
|---|---|---|
| 1 | Citing-set completeness not machine-checked; ledger shape only (CounterCritic F1: no coverage/upper-bound/identity check — omission, under-report, duplicate, row∉population all pass; ClaimCritic item 8/9) | Live gap r26; data portion fixed by w2's 37 units; round-26.md:118 itself marks "completeness of the citing set is still not machine-checked (open)". Inherited by r27 as C2 (range-aware gate, frozen oracle 16/16, c2-before.json: `gate_absent`, 0/16 at be375d). NOT complete — in flight this round |
| 2 | Tag/correction linkage: marker accepted in any corpus/** file, tag counted anywhere in named file, no appended-region/base-prefix enforcement (ClaimCritic item 7; CounterCritic F4) | Partially resolved at r26 landing: `statement_tags_unaccounted` requires tags == stale + reclassified (round-26.md:117-118; selftest + mutant N6 killed); actual candidate bytes verified prefix-clean out-of-band (verification/no-harm-final.json; spotcheck "26 baseline knowledge-file byte strings remain prefixes"). Machine placement check: still absent |
| 3 | STALE tag possible without matching receipt / orphan tag on HOLD row (ClaimCritic item 7) | Resolved in data (each file has exactly stale+reclassified matching tags — spotcheck reproducer assert); receipt-level any-blob marker path latent (F4), unused today |
| 4 | Non-knowledge citing locations outside every ledger/denominator: SKILL.md:229; corpus/README.md:28,60; lessons/round-7.md:57-65; round-20.md:203,261; round-21.md:45; also S015–S018 citing file lessons/round-20.md (PairS001:75; ClaimCritic STALE-corrections section) | Still unjudged; outside r27 C1/C2 denominator (corpus/knowledge only at measured revision, count_c1.py). Named residual — open, not silently shrunk |
| 5 | Multi-fetch receipt grounding: one quote per receipt cannot ground multi-clause/multi-URL rows (S001 v4/v5 halves; S002 two clauses) (ClaimCritic item 2; CounterCritic F2) | Fetch-integrity half resolved at landing: all fetches now checked (`second_fetch_tampered` case, `fetch_sha_mismatch`; selftest 24/24, mutants 12/12). Receipt `quotes:[{clause,…}]` schema NOT adopted (RECEIPT_KEYS unchanged, measure.py:58); clause-level grounding remains single-quote + prose reason. Open by design |
| 6 | Rejected rows' flip conditions not decidable from own bytes: S017 needs S005-1; S018 needs tier-A Firefox (ClaimCritic item 6) | Resolved by disclosure in receipts: S017 reason quotes S005-1 verbatim ("no CNAME file is created, and any existing CNAME file is ignored and is not required."), flip not met (rechecks/S017.json); S018 reason records tier-A confirmation absent, tier-C conflict stands (rechecks/S018.json). `crossFetch` field not adopted — evidence lives in reason prose |
| 7 | Group {S010,S028,S033}: boilerplate/near-twin quotes pass inside group (ClaimCritic item 3; CounterCritic F3) | Resolved at landing: twin-containment check + group fixture case (measure.py:423-434, :593); verifier confirmed "its three quotes are distinct and neither contains another" |
| 8 | Line anchors unverifiable against single-line text views (ClaimCritic item 4) | Unresolved as machine check: `anchorObserved` is required prose (measure.py:373-376) but not parsed against raw lines; offsets measured on pre-amendment views recorded in `round-26/receipt-locator-errata.json`, "not yet fail-capable" (round-26.md:121) |
| 9 | Text-view dotfile mangling (`Excludes.git and.github`) vs "VERBATIM" seat wording (ClaimCritic item 5) | Resolved by convention: counter normalizes both sides; known transform documented (PairS001 "Checks and boundaries"; CounterCritic "binding is consistent") |
| 10 | Counter absent / paths disagree; rows[] never emitted (F6) (ClaimCritic item 9; CounterCritic F6) | Resolved: measure.py exists; `output["rows"] = rows` present (measure.py:557), selftest asserts 32 row records (:829), mutant N1 killed; r26-fail-open-before.json shows rows emitted at 83528f7 |
| 11 | Saturation risk: 32/32 HOLD vacuous, "no evidence of improved quality" (ClaimCritic item 10) | Resolved by honest framing: spotcheck "Status ok (real report); admitted false"; "This does not prove the omitted citing-set clause or admit C1"; quality "improved, bounded"; no numeric inflation (SCORECARD:533) |
| 12 | round-23 digest columns swapped trap (:60-61 vs register :206-212) (ClaimCritic item 11) | Resolved by rule (compare against appended register only); historical lines untouched (append-only); no mis-fire occurred in r26 receipts |

Out-of-scope residual noted, not citing-set: CounterCritic F5 (manifest url/finalUrl
never compared; extra entries unflagged) and the selftest-writes-in-lane operability
note — no adopted fix found in the final counter; latent, low.

## 4. r27-side current state (observed, no adjudication by this seat)

- Frozen base 83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba (= verifier landing); declared
  before implementation at be375d90afc6fc7aca369ab3cf5247bf460aeed2.
- C1 before (c1-before.json @83528f7): 41/57 decided, 16 missing (matches §2 exactly),
  0 findings — the inherited state.
- C2 before (c2-before.json @be375d): exit 1, `gate_absent`, expected 16, detected 0 —
  base fail-open reproduced pre-implementation (matches r26-fail-open-before.json:
  measure.py exits 0 at 83528f7 with 32/32 HOLD).
- Adjudication of the six grouped pairs and the remaining ten belongs to r27 C1/C2
  executors + L1; this seat records the trace only and renders no verdict on r27 work.

## 5. Hashes and identities

- r26 base 97404de4ff73d6c8a4f87385cf5fdf36dca7f006; candidate e28312b14b076584fedd696fae2a684e460bd11e
- measured implementation b44daedc9658d86374f1c3e3cdfc3a6951d0bdf6; author-final a2be0dc53845a4963f9af447d7c7c6644bfde6b3
- verifier/landing + r27 frozen base 83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba; r27 declarations be375d90afc6fc7aca369ab3cf5247bf460aeed2
- population sha256 16330e1effd5ee52665f8f31738e9423c6ec387e5d4a1404c5bcc35f69d01b03 (32 ids)

## 6. Uncertainties

- Which revision the verifier's "43 literal pairs" sweep ran against is not stated in
  the spotcheck text; the count reconciles with base-era bytes. Marked [INFERENCE]; not
  load-bearing for the finding (both 43-literal and 57-with-ranges ground the same six
  grouped pairs).
- MANIFEST[430] read as the kake round-26 closure entry (its fields match: verdict,
  finding naming all three anchors, commit 83528f7c); entry ordinal not independently
  recounted.
- Whether r27's final C1/C2 close items 1–2 above is future work; nothing here
  pre-judges it.

Report: .ufo/waves/round-27/w1/LostFindingTrace.md
