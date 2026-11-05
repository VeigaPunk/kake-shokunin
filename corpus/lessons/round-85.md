# Round 85 — registry discoverability and field-specific policy decoding

Author-side draft for L1 integration only; not an after receipt or independent closure. Base: `bdabc6bc8f762a16c6c19c524c4ac84528eb4bf7`. Authority: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/contract.md`, assigned freeze `2f042c370b5f11b84d4f8c9e5d066517aef646b8`; the freeze identifier comes from the assignment, not a new ancestry check. One v1 wave; L1 alone integrates after WAVE-DONE. The uncommitted, undispatched pre-freeze broad planning draft was discarded without scoring; its wider scope is not this contract.

## Axes and exact claim boundaries

- **C1 — calibration, lowest owned score 2, HOLD.** Three round-84 verdict instruments acquire complete discoverable registry rows: `c84_defect_queue.py`, `c84_policy_values.py`, `policy_value_class.py`. Target complete=0/3 → 3/3, missing=0. Frozen count.py requires exactly one eight-cell row per instrument, all cells nonempty, filename in entry command, `0=`/`1=` verdict mapping, `--selftest`, persisted `.ufo/waves/` proof path, and owner `kake`. This measures registry discoverability, not full semantic or gate conformance. The general classifier stays experimental; a selftest never authorizes publication.
- **C2 — freshness, 10, HOLD; bounded capability acquisition.** A separate offline `scripts/referrer_policy_effective.py` reads a stdin JSON list of string field values in response field order. It splits comma-separated tokens in order, strips surrounding whitespace, compares case-sensitively, and emits exactly one JSON object `{"effective": <last recognized nonempty policy token, or empty string>}`. Recognized tokens: `no-referrer`, `no-referrer-when-downgrade`, `same-origin`, `origin`, `strict-origin`, `origin-when-cross-origin`, `strict-origin-when-cross-origin`, `unsafe-url`. Normal exits: 0 decoded data, 1 invalid data, 64 usage; unsupported input fails nonzero. `--selftest` must use isolated fixtures and exit-code assertions. Target: frozen ten CASES absent=0/10 → 10/10, without narrowing or retrofitting the oracle.
- **Operability — preservation constraint, not a third acquisition claim.** No production edits by seats, no arbitrary response-field equivalence, no publishing authorization, no score or rank/SHONEN promotion. Keep improvements only when no owned axis is harmed; this draft cannot decide that verdict.

The frozen cases expect, in index order: `strict-origin`, `no-referrer`, `same-origin`, `unsafe-url`, empty string, empty string, `origin`, `strict-origin`, `origin`, `strict-origin`. Cases 0/1 reverse two recognized tokens and must disagree. C2 also requires a separate retained-r84-control-pair trial reporting both decoded values; it is not part of the ten-case numerator. Neither that trial nor an after measurement was performed by this seat.

## Gate — admit a parser algorithm, reject blanket equivalence

**Admit — S458, W3C Referrer Policy §8.1, bounded parser semantics.** Source: [Parse a referrer policy from a Referrer-Policy header](https://www.w3.org/TR/referrer-policy/#parse-referrer-policy-from-header), opened GET-only by this seat on **2026-11-04**. Curl returned HTTP 200, 128,023 bytes; SHA-256 `4e60be213bbe74353fd4be29e519c9dd046f3dc6f012cc1149a7d50234a81e81`. Retained source: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ScribeLesson/referrer-policy.html`. S458 is the frozen contract's designated new source row; this seat does not assert that another seat's registry candidate has landed.

Located admission quote, **23 words**, §8.1 step 3, retained HTML lines 706–707:

> For each token in policy-tokens, if token is a referrer policy and token is not the empty string, then set policy to token.

Step 2 initializes the empty string (line 704); step 4 returns the policy (line 711). Thus the accumulator is overwritten by each recognized token in sequence, not sorted or compared as a multiset. This admits a field-specific effective-token decoder only. The JSON interface, exit-code convention and ten-case oracle are the lane contract, not claims that W3C specifies this Python CLI.

**Reject — blanket response-policy reorder equivalence.** Same source URL/date; supporting located quote, **22 words**, §11.1, retained HTML lines 881–882:

> policy values will be ignored, and when multiple sources specify a referrer policy, the value of the latest one will be used.

This is a located clause, not the whole sentence: line 880 begins the context about unknown policy values. Quote evidence and normalization are retained in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/w1/ScribeLesson/source-receipt.json`. Both quotations match rendered source text after HTML data concatenation and whitespace collapse; neither is falsely described as contiguous raw HTML.

Reason for rejection: `no-referrer, strict-origin` selects `strict-origin`, whereas `strict-origin, no-referrer` selects `no-referrer`. Identical token multisets do not imply identical effective policy. A field-agnostic `reordered` label is syntax evidence only. Flip condition: an expressly scoped, source-grounded rule for a particular field plus independent order/duplicate witnesses could support equivalence for that field; this source does not establish it for arbitrary response headers. Do not retroactively relabel r84's failed semantic claim as a successful narrower claim.

Source-reader limit: the initial reader open returned W3C metadata rather than algorithm text. The subsequent direct public GET retained the actual document. This draft uses that body, not metadata-only content, for the Gate.

Registry-URL evidence for S458: https://w3c.github.io/webappsec-referrer-policy/,
opened 2026-11-04 by ScoutSources; §8.1 step 3, retained
`w1/ScoutSources/source.html` lines 1612–1614 contains the same rendered
23-word admission quote printed above. This Editor's Draft rendering, rather
than the independently opened TR rendering, is the registry row's URL.

## Mistakes — semantic scope, captured-by, and a falsifiable repair

**Class: blanket-reorder semantic overreach.** Evidence: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/w1/ReviewC2.md` lines 14–19 identifies the frozen opposite-order Referrer-Policy pair. The retained `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-84/controls/tool-ctl-equivalent.txt` reports `class=reordered` and `verdict=policy-rewritten-equivalent`. These are actual r84 syntactic outputs, not semantic preservation.

**Captured-by:** the round-84 non-author closure spotcheck, `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-84-verifier-spotcheck.md` §C2, lines 51–53, independently identifies the reversed retained fields and confirms that green syntax tallies cannot establish the declared semantics. Its routed D84-3 preserves the failing witness and publication prohibition. The earlier reviewer discovery and later non-author confirmation are distinct provenance, not a claim that this author-side seat independently closed r85.

**Fix direction:** acquire a separately named field-specific decoder with a frozen, implementation-independent oracle. Red-before evidence is retained in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/controls/base-c2.txt`: revision `bdabc6bc8f762a16c6c19c524c4ac84528eb4bf7`, all ten cases `matches=0`, `C2 cases=0/10 met=false`, `counter_exit=1`. Frozen count.py lines 39–43 mark a missing decoder red. Reversal witnesses are cases 0/1: the two token orders demand different outputs. A sorter, first-token decoder, absent decoder or constant-output shortcut cannot satisfy both. These receipts establish a red baseline and a discriminating oracle, not an observed green repair. This seat did not execute a mutant or an after gate.

C1's analogous retained base receipt reads `complete=0/3 missing=3 met=false`, `counter_exit=1`. Registering complete rows is the intended response to D84-1, but row completeness cannot certify the classifier's semantics.

## Historical gates versus current gates — proposal 5 considered

`/home/vgpnk/Projects/shokunin/kake-shokunin/considerthese/2026-10-26.md` proposal 5 asks for a historical-gate list so a gate pinned to an earlier tree is not mistaken for a current regression. Apply that distinction without laundering a flawed historical oracle:

| Instrument / evidence | Frozen or historical scope | Current teaching / limits |
|---|---|---|
| r84 `c84_defect_queue.py` | D1–D4 round-83 routed repairs, historical receipts and frozen census comparison | Preserve v1 receipts. r84 lesson lines 172–180 and non-author spotcheck lines 93–106 disclose missing conjuncts/permissive parsing. A later census change can reopen a historical equality; that alone is not proof the original repair regressed. Nor does historical status excuse known false accepts. |
| r84 `c84_defect_queue_v2.py` | Separately named diagnostic fixing only two prose conjuncts | Its 10/10 selftest is not substitution for v1 and does not discharge D84-2's remaining defects. |
| r84 `c84_policy_values.py` | Frozen policy-value table and retained pairs, including opposite-order “equivalent” case | Historical green output is evidence of that predicate, not of semantic equivalence. r84 C2 remains unprovable; do not alter expectations after scoring or award retrospective capability credit. |
| r84 `policy_value_class.py` | Experimental general syntactic classifier | Registry discovery and selftest success confer no publishing approval and no field-specific semantic correctness. |
| r85 `count.py` C1 | Current bounded row-completeness predicate over exactly three instruments | A complete row need not be a sound gate. D84-1 is intended addressed only within this explicit discoverability boundary. |
| r85 `count.py` C2 | Current ten frozen decoder cases; separate retained-pair trial | New field-specific capability, not repair/approval of every general-classifier behavior. Preserve red base and shortcut controls; no after result is asserted here. |

This is scoped teaching grounded in existing r84 bytes, not a census or rerun of every historical gate and not a new global historical-gate mechanism. A changed contract requires a separately named/authorized current gate; it must not overwrite the historical verdict.

## Routed debt and procedural limits

- **D84-1:** intended addressed by C1's three complete discoverable rows; no after-row measurement or independent closure is claimed by this draft.
- **D84-2:** remains open. General defect-instrument soundness debts include exact prose/line/output/exit-token checks and the later disclosed empty-equal-census issue. Registry rows do not fix these.
- **D84-3:** remains open as substantive general-classifier debt: field-specific order/duplicate coverage, independent changed-row/input-dependence oracle, canned-output weakness, imported-table enforcement and repeated-run/newline handling. C2 attacks the concrete Referrer-Policy decoding gap without claiming general closure.
- **D84-4:** read-before-dispatch and single-integration-owner mitigations are explicit in the frozen r85 contract; `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-85/bindings-read.md` records all 18 roles `@m_zfl` read before dispatch. These are documented procedural mitigations, not this seat's independent dispatch audit. Planner disagreement remains open: the local validator forbids planner, L1 holds canonical planner, and ScoutSources carries bounded planning data-walk; the outside integrator's literal L2-planner requirement is not silently settled. A single writer reduces overlap but is not evidence of separate-worktree isolation.

No full D84-queue closure claim. **Assimilation: none.** No bulk staged-source assimilation, promotion, publication, live property request, score change or independent admission decision.

## Measurement handoff — not executed by this seat

After WAVE-DONE and integration, L1 owns frozen before/after and unchanged/shortcut controls, ten-case C2 measurement, isolated invalid-input/usage/selftest exit checks, the separate r84 retained-control trial, census and independent closure. A nonzero after measurement is unprovable. If an unchanged control meets its target, the relevant claim is unprovable. Do not narrow the population or revise expected outputs after scoring. This draft ends before those receipts exist; its lesson is not a proxy for them.

## Integration after WAVE-DONE

The orchestrator delivered WAVE-DONE for all ten seats before any production
integration. L1 alone copied candidate code and corpus drafts and appended the
registry rows. The earlier draft language above records the seats' observation
time; this section supersedes its pending measurement statements.

Worktree integration receipts: `controls/integrated-c1.txt` prints
`C1 complete=3/3 missing=0 met=true`, exit 0; `controls/integrated-c2.txt`
prints `C2 cases=10/10 met=true`, exit 0. `controls/decoder-selftest.txt`
prints `selftest: 32/32 passed`, exit 0. Revision-pinned after receipts are
recorded separately after the carrier commit; the worktree receipts do not
pretend to name a committed revision.

The real retained-property audit is `controls/integrated-trial.json`: the six
r81/r82 captures (three surfaces each) have no Referrer-Policy field, so each
decodes to an empty token. This does not infer browser defaults. The separate
synthetic r84 equivalent pair yields strict-origin versus no-referrer. These
are intentionally different populations: synthetic fields never become live
property observations. Handoff: inspect any actual deployment's field order
before treating a reorder as inert; do not publish based on these receipts.

### S458 Gate supplement — exact registry URL

The registry row uses https://w3c.github.io/webappsec-referrer-policy/, opened
2026-11-04 by ScoutSources (HTTP 200, 246577 bytes, sha256
339bdd20be241c9eca2f47a18d35368af460edfc708288d90c51e094393743a6),
not the separately opened TR rendering quoted in the draft above. The same
23-word rendered quote is at retained `w1/ScoutSources/source.html` lines
1612–1614, §8.1 step 3: “For each token in policy-tokens, if token is a referrer
policy and token is not the empty string, then set policy to token.”
This grounds token iteration only. No pre-existing registry row's status,
recheck or used-by changed; S458 is new, tier A, mined, used-by
`corpus/knowledge/referrer-policy-effective.md`. The source is an Editor's
Draft, not a W3C endorsement or a complete HTTP extraction specification.

### Mistakes supplement

- **Late control capture** · `controls/late-shortcut-c1.txt` and
  `late-shortcut-c2.txt` were captured after the ready-file handoff, despite the
  contract's control-recording sequence · captured-by: L1 integration · fix:
  preserve the timestamps/late label, never call them pre-freeze; the actual
  unchanged-base controls were committed before dispatch and are red. This is
  a disclosed procedural defect, not a retroactive change to predicate/target.
- **Finite-counter shortcut** · `w1/CriticClaims.md` shows bogus complete rows
  and a canned discriminator can meet the finite counters · captured-by:
  critic and reviewer · fix: keep the frozen predicates and disclose this
  limit; truthful registry mappings were independently source-audited
  (`w1/ExecRegistry.md`), the candidate is a genuine sequential token walk,
  and the separate selftest/trial supplies evidence beyond the numerator.
  No universal counter-soundness or full gate-conformance claim is made.
- **Local whitespace profile** · `w1/ScoutSources.md` notes that Python Unicode
  stripping is not sourced by §8.1 itself · captured-by: scout · fix: keep it
  explicitly local to the JSON adapter, not browser/Fetch extraction.

`controls/census-before.txt` and `controls/census-after.txt` both exit 0, with
22 W04 warnings and 195→196 rows. One tier-A mined row added, no existing
mutable cells changed. Generic policy semantics remain frontier; only this
separate decoder enters the bounded capability repertoire.

Fleet misroot sweep `controls/fleet-misroot-sweep.txt` found orchestrator
scratch files and an unrelated root `after` file containing only a SCORECARD
diff heading; none identifies kake/r85 seat work. No fleet file was moved or
deleted. No installations or upgrades; pacman untouched.

### Author self-evaluation

Accuracy 4 (finite-cases versus universal semantics explicitly separated);
completeness 3 (late shortcut receipts remain a disclosed sequence defect);
clarity 4 (draft and integration instants explicitly distinguished);
actionability 4 (commands, sources and retained trial resolve);
conciseness 3 (historical draft plus supplement is longer than ideal).
Overall 3.6/5. Highest-impact improvement applied: report the bounded claims
only, never claim the whole D84 queue closed. Operator/non-author closure
still owns admission and independent admit/reject agreement.

## Gate

Round-93 C1 E1 repair (2026-11-04): this lesson's own Gate decisions are recorded
above in `## Gate — admit a parser algorithm, reject blanket equivalence` (retained
unchanged); this section adds the canonical `## Gate` heading the round-93 C1
predicate requires and restates those decisions from the lesson's own evidence.
No source work was opened for this section; every line below cites the round-85
receipts and quotes already in this lesson. The lesson records source work (the
2026-11-04 GETs below), so the flip conditions are stated per row.

Admits:

- **S458 — W3C Referrer Policy §8.1 (parser semantics), admitted.** Source: the
  W3C Referrer-Policy TR page,
  https://www.w3.org/TR/referrer-policy/#parse-referrer-policy-from-header,
  opened GET-only on 2026-11-04, HTTP 200, 128,023 bytes, sha256 recorded in
  `.ufo/waves/round-85/w1/ScribeLesson/source-receipt.json`; retained body
  `.ufo/waves/round-85/w1/ScribeLesson/referrer-policy.html`. Located admission
  quote, 23 words, §8.1 step 3, retained HTML lines 706–707:

  > For each token in policy-tokens, if token is a referrer policy and token is
  > not the empty string, then set policy to token.

  Reason: step 2 initializes the empty string and step 4 returns the policy, so
  the accumulator is overwritten by each recognized token in sequence — the
  source grounds a field-specific effective-token decoder only; the JSON
  interface, exit-code convention and ten-case oracle are the lane contract, not
  W3C's.
- **Registry-URL evidence for the same row (admitted).** The S458 registry row
  uses the Editor's Draft URL, https://w3c.github.io/webappsec-referrer-policy/
  (HTTP 200, 246,577 bytes, sha256
  `339bdd20be241c9eca2f47a18d35368af460edfc708288d90c51e094393743a6`, receipt
  `.ufo/waves/round-85/sources/prefreeze-receipt.json`); the same 23-word quote
  stands at retained `w1/ScoutSources/source.html` lines 1612–1614. Reason: it
  grounds token iteration only; an Editor's Draft is not a W3C endorsement.

Rejects:

- **Blanket response-policy reorder equivalence, rejected.** Source: the same TR
  page, §11.1, retained HTML lines 881–882, 22 words:

  > policy values will be ignored, and when multiple sources specify a referrer
  > policy, the value of the latest one will be used.

  Reason: `no-referrer, strict-origin` selects `strict-origin` while
  `strict-origin, no-referrer` selects `no-referrer`; identical token multisets
  do not imply identical effective policy, so a field-agnostic `reordered` label
  is syntax evidence only.

Flips:

- Reject flip: an expressly scoped, source-grounded rule for a particular field
  plus independent order/duplicate witnesses could support equivalence for that
  field; this source does not establish it for arbitrary response headers.
- Admit flip: the admit covers token iteration for the field only; it flips on a
  source that specifies a general extraction, ordering or browser-default rule
  for the field. No such source is cited in this lesson.
- Registry flip: the row's URL is the Editor's Draft rendering; it flips if the
  row is re-pinned to the TR rendering or the draft moves.

### Author self-evaluation (round-93 E1 section)

Accuracy: this section restates, and does not extend, the decisions above;
completeness: the digests live in the retained receipts cited here; clarity: the
suffixed Gate heading above remains this lesson's own Gate prose.
