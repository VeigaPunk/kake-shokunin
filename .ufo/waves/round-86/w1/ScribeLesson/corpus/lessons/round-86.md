# Round 86 — routed-disposition closure and the bounded Cache-Control effective reader

Author-side skeleton drafted by seat ScribeLesson for L1 integration only; not an after
receipt and not independent closure. Lane base `376ac5dcdf86457ef1f8dd490dada735dad81f68`;
authority `.ufo/waves/round-86/contract.md` (frozen at blob
`efc2ad654f1ee56a86ecb57b3b709c18cd1323b5`). This seat wrote no production file; quotes are
taken only from landed round receipts and carry file + line; remaining unfilled spots carry
`TODO-L1` naming the receipt that must land before the lesson is final — no quote is
invented or paraphrased here. Paths are lane-relative unless marked fleet-absolute.

## Axes and exact claim boundaries

- **C1 — calibration (lowest owned score 2, HOLD).** The round-85 non-author closure routed
  five defects; this round records dispositions for four (R1–R4) over committed bytes,
  `open=4 → open=0` measured by `python3 -B .ufo/waves/round-86/count.py --claim c1`. The
  fifth (operator template wording) is operator-owned and only named. Textual conjuncts are
  disclosed as such: a records-only tree with the right sentences opens nothing;
  transcription is the non-author closure's catch.
- **C2 — freshness (10, HOLD).** Bounded value-level Cache-Control reader
  `scripts/cache_control_effective.py`: target `cases=0/15 → 15/15`, `selftest_ok=1`,
  `tool_offline=1` at the carrier. A separate field-specific reader; no upgrade or rewrite
  of the r84 experimental general classifier, no arbitrary-header equivalence, no publishing
  authorization, no live property request, no browser cache model (Vary, Age, Pragma,
  must-understand store-permission stay out of scope, disclosed). Discriminating pairs:
  cases 5/15 (`max-age=200, max-age=100` → 200, the RFC-9111-vs-RFC-7234 order witness),
  2/3 (shared vs non-shared s-maxage), and the no-store order-independent pair.
- **Assimilation (§10, one theme).** Adopt `crux-keyless-check.md` re-grounded on this
  round's re-opened sources — staged S303 renormalized (escaped-`\|` recheck cell rewritten)
  into new lane id S459 — plus a lane own-work probe row S460 from the re-run keyless probe;
  ≥1 reject from the assimilation set recorded below (`crux-eligibility-route.md`). The §10
  id-guard proof (indented-collision fixture → nonempty collisions) and the scratch-mirror
  census gate must both pass before any append. Staged package bytes are not bumped;
  adoption lands only inside the lane repo.

## Gate

One row per candidate. Quotes are ≤25-word located spans from the named receipt; every
`TODO-L1` placeholder must be replaced by that receipt's exact located words before this
lesson is final — never invented, never filled from memory.

| Candidate | Decision | URL | Accessed | Located quote (≤25 words) | Receipt |
|---|---|---|---|---|---|
| S457 re-open (held, tier A) — used-by old→new: `corpus/knowledge/policy-value-classes.md` → that plus `corpus/knowledge/cache-control-effective.md` | re-open | https://httpwg.org/specs/rfc9111.html | 2026-11-04 | §4.2.1 (L270): "evaluating the following rules and using the first match"; duplicates §4.2.1 (L270): "either the first occurrence should be used or the response should be considered stale" | `.ufo/waves/round-86/w1/ScoutCache/` (s457.fetch.meta: 200, 178573 B, sha256 `999f4013…` — byte-identical to the registered r84 digest) |
| S456 support re-open (held, tier A) | re-open | https://www.rfc-editor.org/rfc/rfc9111.txt | 2026-11-04 | n/a — digest-only verification, no new quote asserted | `.ufo/waves/round-86/w1/ScoutCache/` (s456.fetch.meta: 200, 84477 B, sha256 `aeb52adb…` — matches the registered recheck expectation) |
| S459 (new row) — CrUX Vis docs, ground of the adopted entry | admit (assimilation; staged S303 renormalized) | https://developer.chrome.com/docs/crux/vis | 2026-11-04 | no-data case (docs.html L2932): "If your origin is not included in the CrUX dataset, there will be no data to display"; false-negative causes (docs.html L2934, rendered): "Some common issues with origins are providing the wrong protocol, for example http:// instead of https://, and omitting the subdomain when needed" — same paragraph records the redirect→canonical rule | `.ufo/waves/round-86/w1/ScribeAssim/receipts.md` (docs GET 200, 2026-11-04, body sha256 `ea17c956…`); ScoutAssim cross-check TODO-L1 |
| S460 (new row) — lane own-work keyless probe (tier B) | admit (own-work) | https://chromeuxreport.googleapis.com/v1/records:queryRecord — the one authorized keyless POST probe | 2026-11-04 | observed refusal (probe.json): HTTP 403, `error.status=PERMISSION_DENIED` — "Method doesn't allow unregistered callers (callers without established identity)" | `.ufo/waves/round-86/w1/ScribeAssim/receipts.md` + `probe.json`/`probe.headers` (POST re-run 2026-11-04, body sha256 `da4b1ce0…`) |
| `crux-keyless-check.md` | ADMIT (assimilation, re-grounded) | sources = S459 + S460 | 2026-11-04 | quotes ride the S459/S460 rows above | `.ufo/waves/round-86/w1/ScribeAssim/crux-keyless-check.md` (draft; integrated copy TODO-L1) |
| `crux-eligibility-route.md` | REJECT (assimilation) | duplicate route ground; held eligibility ground: `corpus/knowledge/field-performance-cwv.md` (S038, S039) | 2026-11-04 (precedent r51) | n/a — a reject records reason + flip, not a new quote | this round's record `.ufo/waves/round-86/w1/ScribeAssim/lesson-gate.md` (landed); precedent `corpus/lessons/round-51.md` |

Row notes:

- **S457 binding receipt.** The registered rendering and anchors are the httpwg HTML, and
  ScoutCache's fresh GET reproduced the registered digest exactly:
  `.ufo/waves/round-86/w1/ScoutCache/s457.fetch.meta` records
  `final_url=https://httpwg.org/specs/rfc9111.html`, HTTP 200, 178573 bytes, sha256
  `999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64`, fetched
  2026-11-04T15:37:19Z — byte-identical to the round-84 retained copy the S457 anchors name.
  Quotes above were located by this seat in the retained `s457.body.html` (line numbers
  cited): the §4.2.1 spans and the §5.2 sentence are contiguous rendered text; the
  §5.2.2.10 override sentence renders `Expires` through a link, so any quote of it is
  rendered-text, not raw HTML. Supporting corroboration committed pre-dispatch:
  `.ufo/waves/round-86/sources/receipt-l1-rfc9111.txt`
  (`url=https://www.rfc-editor.org/rfc/rfc9111.html`, status 200, 232630 bytes, sha256
  `ce91ee9848d2b9ac46386b0f0cbd4bfd9c0cd1948ebc363834cadc7e0997f3d7`, 2026-11-04) with
  located §4.2.1/§5.2/§5.2.2.x/§1.2.2 spans and the Appendix B note that RFC 9111 replaces
  RFC 7234's most-restrictive duplicate rule — a different serialization; it supports, not
  substitutes.
- **used-by semantics.** The S457 row's used-by cell gains
  `corpus/knowledge/cache-control-effective.md` alongside the existing
  `corpus/knowledge/policy-value-classes.md`; the old entry is not rewritten or superseded.
- **S459/S460 renormalization.** Staged rows live at
  `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` (`| S303 |` CrUX Vis docs,
  `| S304 |` unregistered-caller probe, 2026-10-23). Adoption renormalizes them into lane
  ids S459/S460 with this round's receipts; the staged recheck cell's escaped-`\|` wording is
  rewritten, not the staged bytes themselves. Both ids verified free in the lane registry at
  the worktree (rows end at `| S458 |`; no `developer.chrome.com/docs/crux/vis` or
  `records:queryRecord` URL row present). Landed receipts: ScribeAssim re-opened the docs
  (HTTP 200, 2026-11-04, body sha256 `ea17c956…`, page rev. last updated 2025-05-06 UTC) and
  re-ran the one authorized keyless POST (HTTP 403, `PERMISSION_DENIED`, body sha256
  `da4b1ce0…`); commands, statuses and digests are in
  `.ufo/waves/round-86/w1/ScribeAssim/receipts.md`. ScribeAssim executed no guard/census
  gate and appended no rows — those stay L1 integration prerequisites.
- **Reject — `crux-eligibility-route.md`.** This round's recorded reason
  (`.ufo/waves/round-86/w1/ScribeAssim/lesson-gate.md`, landed): duplicate CrUX-route ground
  already covered by the adopted keyless-route entry, and its historical PageSpeed quota and
  browser-shell observations were not re-run this round, so they must not become fresh lane
  evidence. Flip (this round's restatement): adopt if the keyless-route entry proves thin or
  the route map gains a route it lacks, re-grounding any new route claims before adoption.
  Precedent: `corpus/lessons/round-51.md` refused the same staged file as covered ground —
  the lane's `corpus/knowledge/field-performance-cwv.md` holds the eligibility question
  (§ "CrUX eligibility (S038)", § "The CrUX API (S039)"); supersede in place, never a
  parallel second row for the same ground.

## Mistakes

Rows are `class · evidence pointer · captured-by · fix`; a fix that cannot fail is not a
fix, so each names the check that can turn the row red. Mine only real round events: a row
needs an evidence pointer to bytes that exist, the seat that captured it, and a fix naming a
check that can fail. If the round yields no real event, record the sweep that found none —
naming where it looked (committed controls, `w1/*` receipts, census warnings) — instead of a
synthetic row.

- candidate row — L1 confirms or drops at integration, never edits the frozen receipt ·
  `receipt-shape` · `.ufo/waves/round-86/controls/base-c1.txt` R1 line reads
  `base_met_false=false` while the contract asserts both base controls exist and read
  `met=false` at the freeze revision (base-c2.txt's line does record `met=false`) ·
  captured-by: ScribeLesson, read of committed control bytes, 2026-11-04 · fix:
  ReviewCounter's item 2 — the byte-wise re-run of both base receipts at the exact recorded
  revisions — is the designed catch; the integrated lesson keeps whichever reading the
  re-run prints and discloses the delta rather than repairing the receipt in place.

### R1–R4 disposition mapping (exact evidence paths)

| Item | Closes | Evidence (exact paths) | State at base receipt | Observed 2026-11-04 by this seat |
|---|---|---|---|---|
| R1 late-controls sequence | control ordering provable from bytes, not timestamps | `.ufo/waves/round-86/controls/base-c1.txt` and `.ufo/waves/round-86/controls/base-c2.txt` committed at the freeze (both must read `met=false`); after receipts `.ufo/waves/round-86/controls/after-c1-carrier.txt` and `.ufo/waves/round-86/controls/after-c2-carrier.txt` read `met=true` at the carrier; no `after-c*` file exists at the freeze | base-c1.txt: `items=4 closed=0 open=4 met=false`, `c1_base_exit=1`; base-c2.txt: `cases=0/15 selftest_ok=0 tool_offline=0 tool_absent=1 met=false`, `c2_base_exit=1`; `controls/` holds no `after-c*` file | unchanged; after receipts TODO-L1 (L1 commits them at the carrier) |
| R2 D84-4 operator routing | route-around recorded, never a silent settlement | fleet-absolute `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`, the `kake | round-86 |` line (line 294) routing the literal-L2-planner vs validator-prohibition conflict to the operator | base receipt R2 line: `ok=false l0_absent` | the routing line verified present by this seat (grep of the fleet file, 2026-11-04) |
| R3 counterexample preservation | round-85 counterexamples still resolve and are referenced | `.ufo/waves/round-85/w1/CriticClaims.md` (bogus complete rows / canned discriminator disclosure) and `.ufo/waves/round-85/controls/late-shortcut-c1.txt` still resolve at the carrier; this lesson references the preserved path `round-85/w1/CriticClaims.md` (counter conjunct `lesson_ref`) | base receipt R3 line: `critic=yes late=yes lesson_ref=no` | both files verified present (2026-11-04); `lesson_ref` is satisfied by this mapping once integrated |
| R4 retained-open debt row | D84-2/D84-3 recorded as open debt with flip conditions | `corpus/README.md` "Open instrument debt (round 86)" block naming `D84-2` and `D84-3` with a `flip:` re-open condition, citing `corpus/lessons/round-85.md` (draft also cites `corpus/lessons/round-85-verifier-spotcheck.md`) | base receipt R4 line: `d84_2=no d84_3=no flip=no lesson_cite=no`; the worktree README carries no D84 row yet | block drafted by ExecQueue under `.ufo/waves/round-86/w1/ExecQueue/`; lands at L1 integration — TODO-L1 |

**Retained-open statement.** D84-2 and D84-3 remain open exactly as recorded in
`corpus/lessons/round-85.md` (§ Routed debt and procedural limits): D84-2 general
defect-instrument soundness debts; D84-3 substantive general-classifier debt. This round's
C1 records dispositions of the round-85 routed queue (R1–R4) over committed bytes;
retention is the routed instruction, not closure of the debts, and no full D84-queue closure
is claimed.

**L0 routing line (D84-4).** The literal-L2-planner vs validator-prohibition conflict is
routed to the operator at fleet-absolute
`/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`, line `kake | round-86 |` (line 294).
Round 86 proceeds with the recorded mitigation (L1 holds the canonical planner; ScoutCache
carries the bounded planning data-walk) and this routing; no answer blocks it and nothing
here settles the conflict.

## Measurement handoff — not executed by this seat

After WAVE-DONE and integration, L1 owns the frozen measurements:

```
python3 -B .ufo/waves/round-86/count.py --root . --claim c1 \
  --freeze <freeze-rev> --revision <rev> --work /fast/scratch/hyaku/kake-r86/L1-count
python3 -B .ufo/waves/round-86/count.py --root . --claim c2 \
  --revision <rev> --work /fast/scratch/hyaku/kake-r86/L1-count
```

Committed pre-dispatch controls stand: `controls/ctl-c2-constant.txt`,
`controls/ctl-c2-minmost.txt`, `controls/ctl-c2-sharedalways.txt` (shortcut decoders fail
the frozen cases), `controls/c86-selftest-c1.txt` (`selftest: 10/10 passed`,
`selftest_exit=0`), `controls/census-before.txt` (`census_exit=0`, 22 standing W04 warnings;
196 rows per contract). Kill rule: if any unchanged/shortcut control meets its target, that
claim is unprovable — fix before data, never after. Never narrow the 15-case population or
retrofit expectations after a seat scores. A nonzero after measurement is unprovable. New
discovered defects are disclosed, never hidden by green counts. Census after: `196 → N`
rows, TODO-L1.

## Fill ledger — every TODO-L1 that must land before this lesson is final

Filled from landed receipts while this seat worked: S457/S456 re-open receipts and quotes
(ScoutCache fetch metas + retained bodies), S459/S460 receipts and quotes and the adopted
draft + REJECT record (ScribeAssim `receipts.md`, `crux-keyless-check.md`, `lesson-gate.md`).

Remaining:

1. ScoutAssim's independent CrUX Vis receipt and quotes (its directory was still empty at
   this seat's last read) — cross-check for the S459 row; reconcile any drift into the row
   rather than duplicating quotes.
2. ExecQueue's `corpus/README.md` debt block at integration (draft exists at
   `w1/ExecQueue/corpus-README-debt-block.md`) → R4 evidence.
3. `controls/after-c1-carrier.txt` + `controls/after-c2-carrier.txt` at the carrier with
   `met=true` → R1 completion.
4. `controls/census-after.txt` (`196 → N`) → census closure.
5. ScribeKnowledge's `corpus/knowledge/cache-control-effective.md` draft → the new S457
   used-by entry (provenance trio per the r85 house style; the old
   `policy-value-classes.md` entry stays).
6. ExecAssim's id-guard proof (indented-collision fixture → nonempty collisions) and
   scratch-mirror census gate receipts — both prerequisites before any registry append.
7. The integrated copy of the adopted entry landing at
   `corpus/knowledge/crux-keyless-check.md` (draft at
   `w1/ScribeAssim/crux-keyless-check.md`).

### Author self-evaluation

Accuracy 4 (only bytes read this seat are cited; every quote slot is an explicit
placeholder); completeness 3 (skeleton by design — the fill ledger enumerates exactly what
is missing); clarity 4; actionability 4 (each TODO names its landing path); conciseness 4.
Overall 3.8/5. Highest-impact improvement applied: no quote anywhere in the skeleton, so
nothing can be mistaken for sourced text before the receipts land.
