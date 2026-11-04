Verdict: C1 **narrow**, C2 **stands locally**, C3 **fails the current integration state**; capability is new and in province, but no final-carrier admission is supported by this review.

## Latest C3 addendum — supersedes historical open-defect wording below

Read committed amendments 3 (`715795eb`) and 4 (`e409f6c1`). Amendment 3 resolves the count to **36** and g27 to `["indexifembedded","noindex"]`; amendment 4 corrects finding-case exits. Earlier 36/34 and g27 objections are therefore **closed in terms**, not current contract defects.

Latest inspected matrix SHA256: `7dc7cc9253895c653f88d523d2e3aaf787197c5cd26dfe5d78a8e8cf0a6c35f2`; current tool at handoff: `c0b6e579e93fe1c72da9df0341699466a583d230c86f85b0813fe6fabef28d73`. Command: `sha256sum .ufo/waves/round-78/c78_meta_robots_matrix.py scripts/meta_robots_audit.py`. The replacement tool was not rerun in this addendum; earlier 84/84 evidence does not transfer to this digest.

**Isolation repair credited:** revised `audit_case` (lines 248–271 at inspected snapshot) stages only page payload and an expectation-free manifest into a randomly named scratch input directory, passes that directory rather than the oracle directory, and removes it afterward. IDs/URLs are anonymized and the returned ID is compared against the rewritten one. This closes the direct sibling-label lookup below by source inspection. It is input separation, not an OS sandbox. A sibling-echo negative control and the final committed end-to-end receipt were not exercised in this addendum.

**Open residual — g26 has conflicting authorities.** Amendment 3 C2:24–32 says `max-snippet:0` becomes `nosnippet`, participates in rule 3, and suppresses every `max-video-preview` token. C4:82 nevertheless requires g26 (`max-snippet:0, max-video-preview:-1`) to emit `max-video-preview:-1,nosnippet`. Amendment 4 changes exits only. The L1 explicitly retained this inconsistency after scoring, rather than retargeting the case.

Impacted axes: operability and calibration. A receipt can truthfully establish compliance with the **explicit C4 table**, but cannot establish simultaneous compliance with C2 steps 3/5. Under the combined contract, the broader semantics are **unprovable from that green**: no single g26 output satisfies both authorities. This is a fixable contract defect, not grounds to fabricate a tool failure. Preserve the frozen expectation after data; label the measured guarantee as table-specific and route the contradiction to closure. Admission belongs to the canonical judge, not this critic.

For a future pre-data contract, the smallest semantic correction is g26 effective `["nosnippet"]`, preserving C2's collapse rule, or an explicit sourced exception to C2. Neither should be silently applied to the already-scored population.

**Concurrent report notice:** this addendum preserves a replacement report that appeared between my read and edit. Its additional C1/C2 experiments are not newly attested by this C3 addendum. My contribution here is the source/interface critique, the isolated old-matrix measurement, the reviewed isolation repair and the unresolved g26 authority conflict.

---

# Axes and scope

Calibration=C1; freshness=C2; operability/capability=C3. Review is point-in-time, not canonical judgment. Read the complete original contract and amendments 1–4; all eight top-level w1 reports present at the final report census (ExecC1Population, ExecC2Annotate, ExecReceipts, ReviewC1, ReviewC23, ScoutCites, ScoutSources, ScribeProvince); all six original control receipts plus base-instrument-receipts and the landed after/quote receipts. Producers were changing files during review. Latest instrument snapshot: 2026-11-04T02:48:45Z.

# 1. C1 — narrow: actual declarations are plausible, predicate does not bind population identity

The no-edit base is red (`controls/base-c1-population.txt`: rows_with_population=0, exit 1). The note-only control is also red. But **a declaration-only repo can pass without declaring the population actually measured**.

Independent scratch experiments used the base tree, fixture-local git repositories, and the lane's unmodified C1 counter:

| experiment | fixture revision | observed result |
|---|---|---|
| Entire base tree; add `{"kind":"file","path":"SKILL.md","count":1}` to ALL four ledger rows; no observation/check/SHONEN edits | `71a972baf35a7edb2f22613f107db0addfc0ce17` | `rows=4 rows_with_population=4 undeclared=0 stale_populations=0 exact_mismatches=0 floor_violations=0 growth_tolerated=2 met=true`, exit 0 |
| Same, then delete SHONEN.md | `19ab7f7943c287a41466bff0c1a0da8c43385610` | c78 `met=true`, exit 0; c77 `boxes=0 ... mismatches=0 met=false`, exit 1 |
| Committed full-tree fixture has REAL c77; replace ONLY its uncommitted worktree c77 by `print(json.dumps({'findings': [], 'met': False, 'boxes': 0}))`; measure committed revision | `299f11bc34f476037ac225a08294af66077192ac` | c78 `growth_tolerated=0 met=true`, exit 0; fixture status explicitly showed modified c77 |

Exact measurement argv (L is `/home/vgpnk/Projects/shokunin/kake-shokunin`; F is the named fixture under `/fast/scratch/hyaku/kake-r78/CriticC/`):

`python3 -B $L/.ufo/waves/round-78/c78_shonen_population.py --root $F --revision <full revision above>`.

**Mechanism:** `c78_shonen_population.py:57-73` accepts arbitrary file/files population specifications; `:76-94` runs the *worktree* c77 and checks only that its JSON carries `findings`; `:124-155` uses that list without requiring the authority to have examined four checklist boxes. A missing SHONEN produces no c77 findings, so c78 mistakes absence of examination for absence of error. An overall c77 red must NOT simply be rejected: its two count-growth reds are intentionally regraded by C1. Instead require the structural examination fields (four boxes, no unexamined) and classify its findings.

The delivered ledger's SKILL/LOG/SKILL/knowledge declarations do correspond to its checks' primary input paths; the on-disk knowledge count reached 65 once the C3 entry landed. Thus this is not evidence that those particular declarations are false. It is evidence that the predicate cannot establish their identity. ExecC1Population §5.2 and ReviewC1 F4 already route the population-identity/worktree-authority limitations; the missing-SHONEN green above strengthens that objection.

**Smallest safe corrections:** bind each population specification to its check surface; extract c77 from the measured revision; require structural examination rather than merely `findings=[]`. Preserve the frozen floor regrading. These are fixable counter defects, not grounds to reject the domain task. Until fixed, narrow the claimed guarantee to review-asserted population identity and explicitly disclose the missing-checklist false green.

`controls/after-c1-population.txt` is NOT a lane-carrier receipt: revision `1729712e4ee5c2960bcad1c3d55fe8babbf9f1b7` does not exist in the lane object store (`git cat-file -t`, exit 128). ExecC1Population honestly labels it a projected fixture with a placeholder C3 document. Re-cut it at the real integration revision.

# 2. C2 — stands locally; no observed gate loosening

Independent base archive sweep:

`node scripts/freshness-sweep.mjs --offline --json --repo /fast/scratch/hyaku/kake-r78/CriticC/fx3`

Exit 1: `resolve=32 declaredAbsent=64 drift=1 unresolved=10 newDrift=1 newMissing=1 paths.ok=false`. The drifting token is exactly `~/projects`, resolving to missing `/home/vgpnk/projects`. My `test -e /home/vgpnk/projects` returned 1.

Independent repaired lane worktree run:

`node /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs --offline --json`

Exit 0: `resolve=32 declaredAbsent=65 drift=0 unresolved=10 newDrift=0 newMissing=0 paths.ok=true`; armed checks skipped and history suspended, NOT passed. The 10 unresolved entries are placeholders/globs, unchanged from base, not ten newly silenced missing files.

Inspected pin diff: only the new `~/projects` miss plus dated metadata. Inspected sidecar entries: exactly 16 new line/hash-bound absence records, dated 2026-11-03, preserving lesson bytes. Sweep source is unchanged. Pin-only control remains red (`controls/ctl-c2-pin-only.txt`: exit 1, drift=1 newMissing=0); ScoutCites §7 and ReviewC23 pin-only.json independently reproduce it. A pin changes newMissing, not the per-citation drift predicate. Their post-repair same-token plant also stays red (drift=1 newMissing=0), so pinning does not immunize later citations.

Cheapest skipped-work attempt is pin-only; rejected. A purely fabricated annotation is not semantically proven by the sweep, but these 16 annotations cite historical narratives and the absent lowercase directory, not live executable instructions. QUALITY's existing sidecar mechanism is the compliant repair, not a new bypass. The historical W6 event is retained-corpus evidence, not established merely by today's existence test.

My crude deletion probe removed 57 lines containing the token and returned **exit 2**, `paths sidecar binding invalid: SKILL.md:365`. It did NOT demonstrate a successful deletion cheat; do not count it as one.

C2 counter was tightened during review: it now archives both measured and control revisions and includes sidecar/sweep bytes in tree identity (digest below). That repairs, rather than loosens, the original mutable-worktree problem identified by ReviewC23. Existing after-C2 receipt explicitly measures an uncommitted worktree; fixture counter receipt also identifies its distinct input identity. Re-cut against the final committed carrier.

# 3. C3 — genuinely new ground; current deliverables do not yet agree

## Novelty and province

Base `scripts/robots_audit.py` is an RFC9309 robots.txt URL/rule expectation instrument, not a page-meta instrument (its first 35 lines define that scope; no noindex/nofollow/max-snippet/meta processing). Existing link-preview metadata parsing is shared substrate, not robots directive interpretation. Existing Yahoo refusal entry mentions a meta-tag substitute but explicitly says the source supplies neither tag value nor substitute scope (`corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md:104-114`). No same-capability lane instrument was found.

Searched sibling scripts/corpora and broader retained material for meta-robots/noimageindex/max-snippet/unavailable_after. Hits in tabi/chousa/kengaku were retained pages, header evidence, or adjacency reports, not an existing page-directive decision instrument. `tabi/scripts/check-aria-metadata.mjs` is ARIA, not robots. This is acquisition of directive semantics, not repair of robots_audit.

Boundary: `PROVINCE.md:38-39`: **“tabi drives browsers and owns client-side crawler discipline; kake owns publisher-side placement (robots/sitemap at the host it serves).”** Local publisher HTML declarations are kake; actual crawler obedience, rendering, ranking/indexing outcomes and browser behavior are not. chousa owns research method, not this publisher audit. A duplicate parser substrate is not duplicate domain authority.

## Two different instrument states were exercised — do not conflate their receipts

The initial matrix revision, before amendment-2 cutover, was run against an exact scratch commit of delivered tool bytes:

`python3 -B $L/.ufo/waves/round-78/c78_meta_robots_matrix.py --root /fast/scratch/hyaku/kake-r78/CriticC/mxrepo --tool-revision ac7bceaf4ac7bd993bbbe8ffcb8ab9e0e8f58197 --cases $L/.ufo/waves/round-78/cases --consts $L/.ufo/waves/round-78/consts --work /fast/scratch/hyaku/kake-r78/CriticC/mxrun/real`

Exit 0: `cases=34 decided=34 correct=34 wrong=0 constants_failed=4/4 met=true`; tool SHA256 `d32fb5808c1de8f9abdb10248247acc7ff779937ba51c09dabf82c1f8611acf4`, 62,459 bytes; cases digest `ec15f5ec6da0213058db2455ade7cb132d82beda794c21b91b7822bd188fa59a`. Constants failed 9/34 (clean), 9/34 (empty findings/real exits), 17/34 (substring), 34/34 (every id). Tool selftest independently exited 0, **`selftest 84/84 passed`**. Matrix selftest with explicit `--work` exited 0, 14/14.

That green is **obsolete** under amendments 2–4. At 02:48:45Z:

- Matrix SHA256 `d6a4ad6740d9eb698523bfe7173136d0cece327960692ffeadc9ff81ce637284` freezes 36 underscore ids but retains `DECLARED_CASE_COUNT = 34` (`:58-80`, predicate `:373-378`). Amendment 3 explicitly corrected the count to 36. Its tally counts every record (`:338-342`), so this mismatch cannot produce the amended predicate's green.
- Cases on disk were still 34 hyphen-named dirs, with manifest `expect` and expect.json containing only exit/findings. New matrix requires underscore ids, no manifest expectation, effective comparison, and exit-2 error cases. The run returned `cases=36 decided=0 ... met=false`, exit 1, listing missing frozen ids.
- Tool `d32fb580...` still consumes expectations and emits `meta_robots_expected_mismatch`; g20 actual output demonstrates it. It prints `selftest 84/84 passed` without the colon now required by matrix `SELFTEST_RE`. The new protocol requires `{"version":1,"checks":[...]}` or fault `error`, and removes expected_mismatch entirely. Thus 84/84 alone does not establish amendment-2 interface compliance.
- Amendment 3 itself conflicts internally on g26: §C2 rules 3/5 remove video limits when max-snippet:0 renders nosnippet, but C4's g26 row retains max-video-preview:-1. Amendment 4 explicitly changes exit columns only. Resolve the effective-set contradiction before a producer selects an answer.

These are fixable clean-cutover defects. Reconcile tool, all cases, constants, selftest footer, count, and docs to one amended contract, then measure the exact carrier. No partial alias/shim is needed.

## Cheapest oracle cheat remains reachable in the harness

Amendment 2 removes expectations from the manifest, but explicitly leaves expect.json beside it. Matrix `audit_case():251-255` still supplies **the original case directory as --root**. A tool can read `$root/expect.json` and echo its exit/effective/findings without opening HTML. The four frozen constants are not this oracle reader.

I built a scratch oracle tool that opens only expect.json. Invoked with the matrix's actual argv for old g20 and g11, it returned exactly the expected finding-id set and exit 1 for each, without reading page.html. Full current-matrix green was NOT demonstrated: the simultaneous 36/34 case mismatch and its selftest requirement made that run red. Oracle reachability is directly demonstrated; complete harness acceptance after repairing those unrelated blockers remains [INFERENCE]. Smallest correction: hand the tool a clean staged input directory containing only manifest and page inputs; keep the oracle elsewhere. Under a malicious-program threat model, ordinary directory staging is not an OS sandbox, so do not claim arbitrary-code secrecy from staging alone.

# 4. Evidence claims and unresolved pointers

1. PROVINCE's round-78 behavior paragraph and README's coverage paragraph still restate the original pre-amendment grammar (outside-head ignored, noarchive effective, tool-side expectation matching, g01–g24 population). ScribeProvince §3 explicitly says so. They contradict the amendments, the initial g19/g23 cases, and the new matrix. Replace/supersede with the final contract; do not merely update case counts.
2. New entry `meta-robots-directives.md:104-114` still says noarchive enters the effective set and indexifembedded/nocache are unknown; amendment 1 A3 and subsequent cases say the opposite. This is substantive stale knowledge, not a missing source. Earlier body/default grammar must be reconciled too.
3. Amendment-1 source pointers were wrong, but amendment 2 §“Pointer corrections” explicitly supersedes them. Do not re-open them as uncorrected findings. Both retained Google captures contain the five amended source statements; different raw captures (208,191 bytes SHA bf8adcc7... versus 208,195 SHA d9fdfe42...) are dated and separately identified, not proof of conflicting semantics.
4. My early suspicion of missing S449/S450 rows was a race: SOURCES.md now carries S449/S450 and rejected-404 S451. The final entry cites existing S032 for RFC3339. ScoutSources §7 is explicitly a draft using S451 for RFC3339, not the final allocation; retain that distinction. Registry census ran: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`, exit 0, with W04 duplicate-URL warnings (including S450's separately scoped WHATWG URL).
5. Entry quotation checks must use the named source: its WHATWG pointers refer to ScoutSources/whatwg-semantics.txt, NOT the Google text. My exploratory checks using guessed phrases/wrong source were invalid and establish no quotation defect. The exact quote text read in the entry resolves at the inspected Google ranges (e.g. 912–913 actual meta example, 1083 numeric rule, 1217 unused-rules introduction). No fabricated quote failure is asserted here.
6. `controls/doc-quote-truth-r78.txt` is honestly green at freeze revision 78711a62 **with missing round-78 lesson and zero round-78 contribution**. It cannot prove the final round's claims. ExecReceipts explicitly requires a re-cut. At final inspection `corpus/lessons/round-78.md` did not exist. Consequently lesson-based routed corrections were not yet evidenced.
7. ReviewC23 explicitly withheld C3 because artifacts were then absent; that report is not C3 approval. ExecC1Population's placeholder green and ExecC2Annotate's fixture green are explicitly qualified, not missing receipts masquerading as carrier runs. ScribeProvince removed moving C3 digests rather than retaining its intermediate SHA as carrier evidence.
8. Inherited instrument_receipts remains red for doc_quote_truth/hreflang rows at base/freeze (ExecReceipts, controls/base-instrument-receipts.txt). Not new harm, but do not call it green or assume new instruments are automatically in its registry population.

# 5. What L1 must fix before landing

- Complete one C3 amended-contract cutover (36 ids/count, no labels in manifest, output shape/effective comparison, selftest footer, error cases, g26 precedence); stop treating the initial 34-case pass as final evidence.
- Remove oracle exposure from the supplied case root; state the actual harness threat model.
- Correct PROVINCE/README/new knowledge-entry semantics to match that same contract, with dated supersession where required.
- Explicitly narrow or fix C1's population identity, missing-checklist acceptance and mutable authority. No silent assurance that its counter proves more than tested.
- Land lesson/routed corrections and re-cut C1/C2/C3/doc_quote_truth on the exact committed carrier; bind new instruments if claiming the registry gate. Preserve the existing box-2 gap and offline disclaimers.

No change here to score, admission, canonical judgment, or shipping authority. No source/runtime installations. Only this report is a permanent write; scratch fixtures and probes were under `/fast/scratch/hyaku/kake-r78/CriticC` and removed before yield. Fixture commits never touched lane history.

Self-evaluation: accuracy 4 (race-sensitive snapshots explicitly separated; invalid probes disclosed); completeness 4 (all five assigned questions addressed, no final-carrier evidence yet available); clarity 4 (three verdicts plus exact blockers, but long report); actionability 4 (small concrete corrections); conciseness 3 (multiple instrument generations require detail). Overall 3.8/5. Highest-value next action is a single exact-carrier re-cut after the cutover, not reinterpretation of old greens.
