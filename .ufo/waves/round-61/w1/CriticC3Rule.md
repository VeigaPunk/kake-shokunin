# CriticC3Rule

Scope: attack C3's pin rule and its counter conditions as frozen in
`.ufo/waves/round-61/contract.md` § Claim C3 (conditions C1-C6, counter
`.ufo/waves/round-61/c61_recheck_pins.py`). Evidence read: contract.md/contract.json,
`corpus/SOURCES.md` rows S001-S018, S129-S132, `corpus/lessons/round-60.md` (§ Gate format),
`corpus/lessons/round-27.md` (S001 anchor clarification), `.ufo/waves/round-61/make_spec_w1.py`
(C3 seat block), `.ufo/waves/round-61/recheck/` (10 retained bodies + receipts.json, all HTTP 200,
one URL per row). Base `9f07731a`.

## ATTACKS:

**A1. opened+90d for on-release/on-use is arbitrary and erases the event semantic.**
The pin rule converts S001/S002's event-driven cadence into a calendar date equal to the 90d
rows' pins: all of S001-S007 land on 2027-01-17, so after pinning the registry cannot
distinguish an on-release row from a 90d row. No justification is given for 90 days versus
30/180. Consequence (honesty, not counter-failure): a new release of upload-pages-artifact on
2026-11-01 leaves S001 stale while its cell shows a future date; conversely 2027-01-17 forces a
re-fetch even if nothing shipped. The contract quotes "the pin is opened + 90d" as if derived;
it is a frozen choice. C2 hardcodes `= opened + 90d` for the two rows, so the counter cannot
fail on this — it is a tradeoff the reviewer must record, not a fixable scoring defect.

**A2. The C2 bound is looser than the pin rule it checks.**
C2 requires "for each pinned row the recheck cell is a concrete ISO date" with
`opened < pinned <= opened + cadence`. The pin rule prescribes exactly `opened + cadence`.
So C2 admits pins the pin rule forbids (e.g. opened+1d on a 365d row) — undefined-behaviour
slop in scoring; harmless in practice (no lane gains by pinning early) but the window adds no
checked value. On the assigned edge: `pinned == opened+cadence` exactly is not merely allowed
by `<=`, it is the prescribed value, so equality MUST stay allowed; the defect is the rest of
the window. Fixable defect: tighten C2 to equality.

**A3. Tie-break by lowest id permanently starves S011-S016.**
At base, 16 non-rejected rows carry opened 2026-10-19 (verified by re-derivation: S001-S016
minus rejected S017/S018). The id-order cut excludes S011 (RFC 9309), S012 (sitemaps.org),
S013 (Google sitemap docs), S014 (own-work freshness-sweep), S015 (GitHub Pages limits,
status `queued`), S016 (pages.github.com versions, `queued`). Consequence: `opened` never
changes, so every future "oldest opened" sweep re-selects S001-S010 and can never reach the
excluded six — a permanent underclass, including two rows that were never live-verified at all.
The stake is real: the tie-break has no freshness rationale, and it shields exactly the rows
whose status (`queued`) argues for verification, not exemption.

**A4. Ten-row width is a sizing choice, but width x tie-break makes the skip static.**
10/167 rows ≈ 6% coverage; the contract itself records the width as reviewer-checked sizing,
which is fair. The attack is the interaction with A3: of the 16-row equally-old cohort, width 10
plus lowest-id ordering skips a fixed 37.5% every round, and no other rule ever enforces the
cadence text of the other ~94% of the registry. Nothing operational turns a `90d` cell into a
due date; cadences are aspiration unless a row enters a frozen due set.

**A5. The no-pin-on-quote-missing carry is unevidenced — a zero-work after-state passes 6/6.**
Conditions C3/C4 bind retained bodies, receipts and located quotes to *pinned* rows only; C5
requires just "an unpinned due row has a Gate note naming the observed state". The do-nothing
control (base -> C2 fails) shows the intended C2 reading is pins-or-carries per due row. Under
that reading: a lane performs zero fetches, writes ten Gate notes of the form "S00N —
quote-missing", changes no cells -> C1 passes (due-set rule unchanged), C2-C4 pass vacuously
(quantification over zero pinned rows), C5 passes (notes name the state), C6 passes (no
changes). Predicate `conditions_passed == 6 of 6` holds with no live verification — the claim
verb "re-verified live" is satisfied by prose. Nothing bounds consecutive carries, requires a
retained body/receipt for a carried row, or lets the counter re-check quote-absence from
committed bytes (the same search machinery as C3, inverted, would close this). This is the one
attack a canonical judge should reject as-is; it is fixable in w2 as a tightening, not fatal
to the frozen predicate text.

**A6. "Row's URL" is singular in the rule; S001/S002 carry two URLs each — and the wave is
already inside the ambiguity.**
S001's source cell lists two action.yml URLs (v4.0.0 tag 7b1f4e7…, main 5f32701…); its anchor
cell reads "inputs.include-hidden-files lines 17-20 and Archive artifact steps lines 37-39",
and the round-27 lesson pins those line coordinates to the **main** commit file while noting
the v4.0.0 archive command sits at lines 29-36. The wave's own receipts.json shows only the
v4.0.0 URL was fetched for S001 (and only the v4.0.0 release page for S002). Consequence: a
lane can fetch the v4.0.0 file only, honestly fail to find the main-pin anchor, and carry S001
as "quote-missing" — while the never-fetched main URL still carries the quote. C4's "receipt
URL = row URL" cannot even be stated literally for a two-URL cell. The carry decision is
URL-selection-dependent, which is A5's hole made concrete.

**A7. (minor) Due rows' non-recheck cells are unconstrained.**
C6 byte-identity covers only rows NOT in the due set. A lane could edit a due row's teaches,
anchor or status cells mid-recheck (e.g. quietly weaken an overclaim while touching the row)
and stay green. The contract's procedure allows recheck-cell changes only; the counter does
not test the restriction.

## TIGHTENINGS:

- **T1 (A5, judge-reject):** new counter condition: every due row is pinned XOR evidenced-carried.
  A carried row must have (i) a retained body + receipt (status, sha256, bytes, fetchedAt on
  the access date, userAgent `round61`) or a named fetch-error class; (ii) a Gate note carrying
  id, URL, access date and the observed state; (iii) for quote-missing, the counter re-runs the
  quote search on the retained body and confirms absence. Add an escalation rule: two
  consecutive carries -> the row must be re-anchored or rejected in the lesson; no third carry.
- **T2 (A2):** C2 bound -> `pinned == opened + cadence` (Nd rows) and `== opened + 90d`
  (S001/S002); keep the strict `opened <` lower side. Equality at the cadence end stays allowed
  and becomes the only accepted value.
- **T3 (A1):** contract states the 90d figure is a fallback floor ("recheck no later than"),
  not a cadence conversion; the S001/S002 Gate lines must name the trigger event class; add a
  post-pin lifecycle rule: at the pin date, if no release/use was observed, revert to
  on-release/on-use or re-pin with a lesson note.
- **T4 (A3/A4):** due-set rule -> "oldest `opened` among rows whose recheck cell is still a
  cadence (or due on/before the access date)", so pinned rows leave the pool and S011-S016
  enter the next sweep; alternatively sweep the full tie cohort (all 16) when ties exist.
- **T5 (A6):** pin rule names which URL(s) of a multi-URL row are fetched; require receipts for
  every URL in the source cell, or explicitly bind the anchor quote to one named URL and fetch
  that one. For S001 this wave: fetch the main-commit URL the anchor coordinates belong to.
- **T6 (A7):** add C7: each due row is byte-identical to its base form outside the recheck cell.

## VERDICT:

Pins are scored honestly, but the carry path is unevidenced (a zero-fetch, ten-note after-state
passes 6/6 — the one defect the canonical judge must reject), the C2 window is looser than the
pin rule it checks, the +90d on-release default is an unstated floor that erases the event
semantic, and lowest-id tie-breaking permanently starves S011-S016 — all w2-tightenable, none
fatal to the frozen predicate as written.
