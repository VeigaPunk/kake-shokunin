# Round 64 — lessons (kake)

Round opened 2026-10-30; base `1a48131577ba82c967650561be34e8dba909432a`
(round-63 tip). Three claims, frozen in `.ufo/waves/round-64/contract.md`
before any after-state measurement:

- **C1 calibration (lowest owned axis, 2/10).** Implement the round-63
  repair recipe: `.ufo/waves/round-64/c64_calibration.py` pins the raw blob,
  flat text, ledger and recipe sha256s as constants, re-executes the
  committed extraction recipe against the retained raw blob inside the
  counter, re-derives the located raw-line range, gates `unresolved` without
  masking it, and binds the lesson Gate to the round-61 spot-check's actual
  verdict span. The round-63 S432 resolution re-enters as the calibration
  evidence this counter verifies.
- **C2 operability (HOLD 10).** `.ufo/waves/round-64/c64_quote_tool.py`
  hardens the round-63 counter: the stub definition is "tool sha ≠ frozen
  sha", the selftest runs entirely on revision-materialized bytes, and the
  counter re-derives each frozen case itself from those bytes. The
  quote-class capability row re-enters on this evidence (withheld in round
  63 by the frozen kill rule).
- **C3 freshness (HOLD 10).** Re-pin
  `corpus/knowledge/freshness-sidecar.json` to the current `SKILL.md` bytes;
  `scripts/freshness-sweep.mjs --offline` returns to evaluating
  (`paths sidecar binding invalid: SKILL.md:364`, exit 2 → exit 0).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| survivor (a standing gate could-not-evaluate for ~8 rounds, unnoticed) | `corpus/knowledge/freshness-sidecar.json` was last re-pinned at round-24 (`3d07733b`, 2026-10-21). SKILL.md growth after that (first post-pin edits `f8438a28`/`4cb225fb`, round 56, 2026-10-25) shifted seven pinned lines by +1; `scripts/freshness-sweep.mjs --offline` then failed `paths sidecar binding invalid: SKILL.md:364` at the round-60 tip `9f671056`, the round-61 base `d2da25de`, and the round-63 base `1a481315` — receipt `.ufo/waves/round-64/controls/sweep-before.txt` (exit 2, same fault at all three; resolver table `controls/sidecar-repin-map.txt`). Rounds 56–63 landed without running the sweep, so the lane's own drift instrument could not evaluate while real rounds landed. | none at break time; after round 59 the QUALITY criterion "A frozen claim never silently turns a standing gate red" existed but no build-phase duty applied it to SKILL.md-side line shifts, and rounds 60–63 did not run the sweep at all. | This round's re-pin (7 entries, old→new recorded below) returns the sweep to exit 0 (`.ufo/waves/round-64/controls/sweep-after.txt`), and the round-64 QUALITY criterion makes a draft-phase §paths re-run a build duty for any round that edits a sidecar-pinned file. |

Re-pin map (§2b discipline: every cell change logged old→new; file
`corpus/knowledge/freshness-sidecar.json`; 23 further entries re-verified
byte-identical at their pinned lines and unchanged):

| entry (SKILL.md) | old line | new line | new lineSha256 (first 12) |
|---|---|---|---|
| ds4cc-marketplace source row | 364 | 365 | `7070c25fb9ab` |
| property-map:c2 | 423 | 424 | `97576af9b60a` |
| property-map:c10 | 431 | 432 | `f2d75f797445` |
| property-map:c24 | 445 | 446 | `f08a35d9d8cb` |
| property-map:c27 | 448 | 449 | `6e1baa1fa1e9` |
| property-map:c28 | 449 | 450 | `cfb08909875e` |
| property-map:c29 | 450 | 451 | `c16c7a6a684c` |

## Gate

Candidates considered this round: (a) re-entry of the round-63 S432
resolution as calibration evidence under the repaired counter; (b)
`considerthese/2026-10-26.md` proposal 5 (a standing historical-gate list);
(c) the `merge/kake/` assimilation package.

- **Admit (a):** the S432 disagreement resolution re-verifies under
  `c64_calibration.py` with every component bound to committed bytes: the
  retained raw blob `63b0a018…911b` and flat text `8b90d096…2a69` shas
  pinned as constants; the committed recipe (`6b0a88cd…`) re-executed
  in-counter over the raw blob, its output byte-identical to the committed
  `S432.txt`; the class re-derived `collapsed-only` from the recipe output
  and raw blob (never gating on `scripts/quote_class.py`, keeping C1 and C2
  separable); the located raw-line range re-derived `6150-6154` from the raw
  bytes and required to equal the ledger's `locatedRawLines` and the pinned
  constant (killing the round-63 M5 survivor); `unresolved` gated without
  masking. The prose gates bind block-level: the round-64 lesson Gate must
  quote the spot-check's actual verdict span, the QUALITY round-62 criterion
  must name the located proposition, and the knowledge `[r63-correction]`
  block must quote the frozen span and cite the ledger. Controls (receipts
  under `.ufo/waves/round-64/controls/`): base `1a481315` (exit 1,
  `lesson_gate=0`), marker-only `4c666e76` (exit 1), digest-consistent
  fabrication `f924538e` (exit 1), junk `82dcba0d` (exit 1, pins=0 named),
  ledger-mutation `5b981bd0` (exit 1, `pin_drift=drift:ledger`).
- **Reject (b), kept rejected:** the standing historical-gate list already
  exists as the SKILL.md gate-registry `Kind` labels (`live` / `historical` /
  `never met`, each with its pin revision) and the round-60 gate-status
  counter (`c60_gate_status.py`, 28 frozen members, selftest 76 checks)
  re-derives those labels; a second lane-owned list would duplicate the
  registry without adjudicating anything new. Flip: a gate found red on a
  later tree whose registry row carries no `historical`/`never met` label —
  the exact failure the round-60 relabel pass closed for the 28 known
  members.
- **Assimilation: none.** No `merge/kake/` entry was adopted this round; the
  round's work is counter repair and sidecar maintenance on held ground, and
  the package stays staged for a later round.

**S432 re-open record (rule 1):** https://fetch.spec.whatwg.org/ opened
2026-10-30 (one GET, HTTP 200, 1,854,393 bytes; receipt
`.ufo/waves/round-64/sources/receipts.json`), sha256 `63b0a018…911b`
byte-identical to the round-61 retained body, so the retained body is
current. Located quote (raw lines 6150–6154, 19 words): "response header can
be used to require checking of a response's Content-Type header against the
destination of a request". No registry row added or changed; the S432 row
stays `mined`.

**Outside verdict:** the round-61 non-author spot-check `Disagree` on the
S432 admission (`corpus/lessons/round-61-verifier-spotcheck.md`, row
"S432 / Fetch" — its reason: "is only a generic lead-in, not substantive evidence for a response-header expectation")
is the outside verdict this
round's calibration evidence resolves; the resolution itself was verified
genuine by the round-63 non-author closure (3/3 agreement on the sampled
gate decisions, including this admission's `collapsed-only` class). This
round's own gate decisions (admits/rejects above) are author-side
self-assessment; the round-64 non-author closure decides agreement.

## Sources census

Round-start census:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
→ 171 rows, 16 W04 cross-scope duplicate-URL warnings, exit 0 (recorded
2026-10-30 before any registry edit; output pasted in the round report). No
`corpus/SOURCES.md` row was added or changed this round; the round-end
census output is pasted in the round report.

## Attempt-2 evidence corrections (append-only)

These corrections supersede the corresponding narrative above, not the frozen
contract, instruments, controls, or predicate. Attempt 2 inherited the build
`4c8295fa5e3b628f1fdf3840299ae415c01849fb`, receipt commit
`cc8add1fa740b920ea5179a71152680ab220c70c`, and already-dispatched w1;
it did not re-dispatch or change the claims.

- **Sidecar delta:** exactly seven `line` cells changed, not seven changed
  `lineSha256` cells or fourteen changed cells. Every digest in the table is
  the unchanged, re-verified digest of the same text at its new line.
  `w1/ScoutSidecarDiff.md` and `w1/ScribeRepinLog.md` re-derived this
  distinction. The other 23 entries are unchanged.
- **Sweep scope:** `VERDICT: OK (exit 0, partial: offline)` is the full
  verdict. It restores evaluated §paths checks only: remote §armed checks
  are skipped and §history suspended, `complete=false`. T0 has 172 files,
  not the 171 stated in one seat assignment; the registry separately has
  171 source rows. `w1/ExecSweepSections.md` records §paths drift 0 and
  unresolved 10 (placeholder/glob tokens, not newly missing concrete paths).
- **Census attribution:** the validation receipts print 16 W04 warnings and
  exit 0, not the row count. The row count 171 comes from
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`,
  reproduced at base and T0 in `w1/ScoutCensusState.md` and
  `w1/ExecCensusCommands.md`.
- **Source quote:** the short quotation above was normalized, not verbatim:
  ASCII apostrophe and removed inline-code delimiters make it `absent`
  under the quote-class rule. Superseding located quote (raw lines
  6150–6153; 18 whitespace units counted with `len(quote.split())`,
  `collapsed-only` against the retained raw/flat pair):
  “The `X-Content-Type-Options` response header can be used
  to require checking of a response’s `Content-Type` header against the
  destination”. The full class-bound proposition remains in the round-63
  correction and ledger. This supports field purpose, not the S432 row's
  separate exact-value rule; no registry row was written this round.
  Grounding: `w1/ScoutS432Reopen.md`, `w1/ScribeRule1Audit.md`.
- **Chronology limit:** `sweep-before.txt` proves the failure at three
  recorded revisions, not an uninterrupted failure throughout rounds 56–63,
  nor that nobody ran an unrecorded check. The broader historical wording
  in §Mistakes and QUALITY is an inference, not an observed eight-round run.
- **Control reproducibility:** `fixtures/build_fixtures.py` builds four
  controls; the separate ledger-mutation receipt has no committed builder.
  Its recorded output is evidence, not a reproducible fixture revision in
  the lane object database. `w1/CriticPredicateFreeze.md` F1 records this
  durability gap. The frozen builder is not silently amended.

### Additional mined mistakes

| Class | Evidence pointer | Captured-by | Fix / disposition |
|---|---|---|---|
| marker-only semantic admission | `w1/ReviewerC1Prose.md` minimal and contradictory fixtures; `w1/MutC1Prose.md` Q3x | Round-63 semantics-binding criterion | The frozen counter still greens token-bearing non-resolution and a hidden criterion. Preserve its bytes, apply its kill rule, withhold calibration credit; future counter work must reject these exact controls before freeze. |
| one-sided outside-verdict binding | `w1/ScoutSpotSpan.md`, `w1/ScoutPriorRecipe.md`, `w1/MutC1Counter.md` F1 | Round-63 routed recipe item 1 | Rewording the actual outside verdict leaves pins and `met=true` unchanged. Carry this as a counter-family defect, not a repaired external verdict; future binding must read and authenticate the outside verdict itself. |
| normalized quotation presented as verbatim | `w1/ScoutS432Reopen.md`, `w1/ScribeRule1Audit.md` | Round-50 quote-class rule | Superseding quote above retains the actual apostrophe and delimiters; the original short string is `absent`, not a source quote. No source-row rewrite or new admission is inferred. |

The additional counter failures are observations, not claims that a repair
has landed. The demonstrated red-before/green-after fix this round remains
the seven-line sidecar repair. Outside round-64 admit/reject verification
remains the non-author closure's responsibility.

## Wave settlement

WAVE-DONE received from Main after all 65 w1 seats settled; authoritative
handoff `.ufo/waves/round-64/w1-results.json`. One v2 wave, no residual:
scout 10, executor 15, reviewer 16, critic 6, mutation-tester 5, connector 2,
sentinel 1, simplifier 1, revenger 1, scribe 8. Attack share
27/65 (reviewer + critic + mutation-tester); L1 holds the planner seat.
62 scoped reports. CriticExploratory, MutC2Counter and ScribeMistakeClass
returned no scoped report and receive no falsification credit. The handoff
has no seat status/id/last-error fields; causes are unknown, not invented.
MutC2Counter's retained partial text names an eval deadline; this is not a
completed mutation matrix. No seats were replaced.

- **C1 unprovable:** `ReviewerC1Prose` minimal/contradictory prose and
  `MutC1Prose` Q3x (criterion in HTML comment) reproduce marker-only
  semantic greens with the real pins intact. This fires the contract's
  marker-only kill rule; no calibration credit. `RevengerC63Defect`
  independently confirms prose-provenance survivors. Recipe/class/location
  integrity is real, but does not cure the semantic counter weakness.
- **C2 measured met:** no settled attack passes a non-frozen tool; the
  frozen-sha gate rejects it before execution. JSON-helper unhashable-id
  failure is defense-in-depth debt, unreachable with the pinned real tool;
  do not advertise arbitrary hostile-JSON safety. The SCORECARD records
  bounded quote-classifier capability re-entry, not semantic admission.
- **C3 measured met:** actual delta preserves the sidecar roster and
  changes exactly seven line cells; sweep drift 0, exit 0 partial offline.
  `CriticClaims` deletes exactly seven stale entries and greens the
  standalone sweep, but that fixture violates the already-frozen
  permitted-diff condition. It is a detector coverage defect, not a
  permitted C3 repair. No predicate was tightened after data.
- **Carried no-harm uncertainty:** `ExecC63Regression` finds c60 gate-status
  mismatches=1 (c56 selftally live row red). No causal before/after result
  establishes round-64 harm; no clean standing-gate inventory is claimed.
  This remains a routed self-defect alongside the missing reproducible
  ledger-mut builder and missing handoff status/last-error fields.

All inherited build/receipt work and wave evidence is retained. No frozen
instrument, control receipt or predicate was discarded or rewritten.
Assimilation remains none; no tools were installed or upgraded.
