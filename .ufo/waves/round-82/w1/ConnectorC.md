# ConnectorC — round 82 wave w1

Seat: connector (leaf; no dispatch, no labrat). Scope: cross-lane, cross-source and
proposal-overlap scan. **Wrote no production file** — this report plus
`.ufo/waves/round-82/w1/ConnectorC/` only. I did not edit `corpus/SOURCES.md`, `corpus/QUALITY.md`,
`corpus/lessons/round-82.md`, `corpus/knowledge/capture-drift-validators.md`, the counters or
`scripts/capture_delta.py`; all are owned by other seats.

Lane base: `419866015b1f58e01f061cde9a77d490653d3c76`. Read first:
`.ufo/waves/round-82/contract.md`, `PROVINCE.md` §Core / §Frontier / §Adjacent,
`corpus/lessons/round-81-verifier-spotcheck.md` §7, `considerthese/2026-10-26.md` Part 2.

**Measurement hazard, disclosed.** Sibling seats were writing this tree while I measured.
`git -C <lane> status --porcelain` showed ` M corpus/SOURCES.md` (D1), ` M corpus/QUALITY.md`
(D6), ` M corpus/lessons/round-80.md` (D8), `?? corpus/knowledge/capture-drift-validators.md`.
An intermediate read of the working tree gave 193 registry rows; that number is an artifact of
the in-flight D1 edit. **Every count below is re-derived from the base blob** —
`git -C <lane> show 41986601…:corpus/SOURCES.md`, sha256
`1ffc61f1e9cb03df5caa1b6d52801fb3b3ed372bc1e20ba4305d771cca28435f` — so it is stable and
re-derivable by any reader.

## Commands run

Exit codes as observed; `read` calls are reads, not commands.

1. `read` — PROVINCE.md, round-82/contract.md, considerthese/2026-10-26.md,
   round-81-verifier-spotcheck.md, capture-A receipts, ghp-etag-anatomy.md,
   scripts/capture_delta.py, scripts/response_snapshot.py, and the mori / kumitate / kama /
   kasegi / tabi / kaidoku / tameshi files cited below. (no exit code)
2. `git -C <lane> show 41986601…:corpus/SOURCES.md > $S/SOURCES.base.md` → **0**
3. `python3 -B $S/evidence.py > …/w1/ConnectorC/evidence.txt` → **0** (twice, byte-identical)
4. `bash $S/sibling_scan.sh > …/w1/ConnectorC/sibling-scan.txt` → **0**
5. `git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %ad %s' -- merge/kake/SOURCES.append.md`
   → **0**
6. `grep -nE 'EXCLUDE|exclude|SKIP|skip_|IGNORE_|VOLATILE' scripts/capture_delta.py` → **1**
   (no match ⇒ the tool has no header skip list; every recorded field is compared)
7. `grep -rn 'agreed=|disagreed=' --include=*.md --include=*.py .` over the lane, wave dirs
   excluded → **1** (no match ⇒ no committed agreement tally exists)

Scratch `$S = /fast/scratch/hyaku/kake-r82/ConnectorC/` (removed before yield). Receipts copied
to `.ufo/waves/round-82/w1/ConnectorC/{evidence.txt,evidence.py,sibling-scan.txt,sibling_scan.sh}`.
`evidence.py` is re-runnable: `CONNECTORC_BASE=<exported base blob> python3 -B evidence.py`.

## 1. Sibling overlap

No sibling lane under `/home/vgpnk/Projects/shokunin/*-shokunin/` holds a capture-to-capture drift
gate, and no sibling claims an owned ds4cc surface. Ownership splits as follows (all lines from
`ConnectorC/sibling-scan.txt`):

| Primitive | Owner | Committed evidence |
|---|---|---|
| two dated captures of one URL, compared for drift | **kake** | no `capture_delta` outside kake (grep, no match); the only "capture-to-capture" prose elsewhere is kasegi's r31/r32 scout finding (`…/round-31/wave2/ScoutLiveDrift.md:22`, "capture-to-capture sha256 is NOT equal") and audio's r77 phase-offset finding — findings, not gates |
| capture **idempotence** (same artifact twice, byte-identical) | tabi | `tabi-shokunin/SKILL.md:371` "sha256-identical artifact, plus a re-capture proving the capture operation idempotent"; `corpus/knowledge/live-dynamic-capture.md:110` "is idempotent on a quiescent page" |
| custody-receipt re-capture reproducibility | kaidoku | `kaidoku-shokunin/SKILL.md:759-761` |
| SOURCES row → committed capture bytes (one capture, `sha256`+`bytes`+`captured`) | kumitate | `kumitate-shokunin/scripts/source-capture.mjs` (header, rules) |
| pinned capture + quote-exactly-once recheck; manifest/row/provenance binding | kasegi | `corpus/instruments/source-recheck.py`, `capture-binding-check.py` |
| verdict receipt → certified revision | tameshi | `tools/receipt-revision-gate.py` (`RECEIPT_REV_MISMATCH` / `…_CONTENT_DRIFT`) |
| receipt-ledger / append-only disclosure (Markdown + source registry) | kama, plus kake's own for its `control(s)/` tree | `kama-shokunin/SKILL.md:1577`; kake `SKILL.md:1293` (receipt-rewrite-counter), `:1493` (c79 standing ledger), `:1509` (ledger-append-guard) |
| entity-tag / validator identity semantics (held ground) | **kake** | `corpus/knowledge/ghp-etag-anatomy.md` (S009/S010); `corpus/QUALITY.md` criterion "Validator is not identity" |
| RFC 9111 §4.1 Vary / representation selection | **mori** | `mori-shokunin/corpus/SOURCES.md:375` (S594) + `corpus/knowledge/ua-serving-normative-r79.md` K2/K4 |
| RFC 9111 §4.2.3 Age / receipt age on a compare path | **kumitate** | `kumitate-shokunin/corpus/SOURCES.md:191` (S237) + `corpus/knowledge/receipt-age-on-the-compare-path.md` (verified 2026-11-04) |
| `ds4cc.com` surfaces | **kake** | `kasegi-shokunin/.ufo/waves/round-23/build/OverlapWeb.md:20`: "PROVINCE.md (kasegi) refuses live-target testing and names kake as adjacent web properties." |

On the three named tokens: (a) **`capture_delta`** — kake only. (b) **ETag / `8.8.3` / validator
semantics** — no sibling holds this as ground: the 13 tabi files matching `8.8.3` resolve to a
*draft CSRF* section (`corpus/knowledge/csrf-defense-shape-boundary.md:39`, "draft §8.8.3"), and the
chousa/mori/kumitate/revenger hits are retained RFC bodies or unrelated section numbers.
(c) **receipt-ledger gate** — kama does hold one, and kama's own round-51 connector already names
kake's `.ufo/waves/round-58/c58_receipt_rewrites.py` as its "sibling design twin"
(`kama-shokunin/.ufo/waves/round-51/a2w1/out/N1Overlap.md:90`). That is a recorded adjacency, not a
collision: kama governs *its* registry/Markdown append-only; kake's gates govern kake's own
`.ufo/waves/round-*/control(s)/` tree.

**Verdict on province.** C2 stays inside kake's province: the surfaces are kake's, the drift
question is kake's, no sibling runs a competing gate, and kasegi explicitly refuses live-target
testing. Two *adjacent* facts, however, are unrecorded and bear directly on how C2's record may be
read — see §4.

## 2. merge/kake package re-derivation

Source of truth: base blob above vs
`/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md`
(sha256 `5f0cd4c4debc647f3d1e2a85519d4ae2b000d91dad49765514871fa502e9f0cc`), last touched by
`ba6779f0160d12dd7373627e00291d6d5e3ba7ee` 2026-10-24 10:50 -0300 — 11 days stale against the
round-82 base. Both files parse cleanly as 11-column GFM: lane `{11: 192}` (0 escaped pipes),
package `{11: 129}` (113 escaped `\|`, which a naive `split('|')` mis-reads as cell breaks).

**Ids.** Lane 192 unique (`S001..S454`, no duplicates; 162 `mined`, 8 `queued`, 22 `rejected`).
Package 129 unique (`S287..S415`, no duplicates; **129/129 `mined`** — the package stages admits
only, unlike the lane's own mix).

**Id collisions — 8.** Every one is the *same id carrying the same source cell* in both files, i.e.
a row the lane has already adopted, not an id assigned to two different sources:

    S312  S329  S367  S372  S373  S374  S390  S409

**Staged URLs already held — 27 rows.** Unit: host+path with the query sorted and one trailing
slash dropped, so `http`/`https`, `www.` and fragment differences collapse. Of those, 8 are the
same-id rows above; the other **19** are staged rows whose source the lane already holds under a
*different* id — evidence the package predates the lane's own adoption of those sources:

    S287→S137  S288→S138  S289→S139  S296→S080  S299→S262  S300→S263  S310→S273  S311→S274
    S323→S286  S352→S438  S375→S419  S376→S420  S380→S418  S395→S423  S398→S425,S427
    S399→S249  S403→S421  S408→S422  S415→S429

102 staged rows match no held URL; they are candidate new ground, not screened by this seat.
The package is also internally consistent with the lane's own duplicate-URL practice: at the base
the lane holds 18 duplicate-URL groups on exact strings and 22 on the normalized unit
(`ConnectorC/evidence.txt` §D) — the package adds no new duplicate beyond the 8 same-id rows.

**`Assimilation: none` is re-derivable iff it states these three numbers.** The re-derivation is
the two paragraphs above: 8 same-id rows already adopted, 19 further rows whose source is already
held under another id, and 102 unscreened rows in a package last touched 2026-10-24. "None" is
therefore *supported*, but only as "nothing in the package is both unheld and screened" — not as
"the package is empty". A lesson sentence that says only "the package is stale" would not be
re-derivable; one that says `8 / 19 / 102` at the base blob's sha256 is.

## 3. considerthese mining (one proposal)

- **#2 receipt-rewrite watch — implemented.** `SKILL.md:1293` registers `receipt-rewrite-counter`
   over `.ufo/waves/round-58/c58_receipt_rewrites.py` (ledger `receipt-rewrites.json`); `SKILL.md:1493`
   adds the standing `c79_receipt_ledger.py` gate; `SKILL.md:1509` adds
   `scripts/ledger_append_guard.py`. The daily read the proposal asked for is now three gates.
- **#4 gate-agreement ledger — NOT implemented.** The lane holds 59 `corpus/lessons/round-*-verifier-spotcheck.md`
   files, each carrying its own per-claim sections, and per-round admission prose in the lessons —
   but nothing aggregates verifier agree/disagree across rounds: `grep 'agreed=|disagreed='` over
   the lane returns no match (command 7, exit 1). The `agreement` token at `SKILL.md:1396` is the
   *gate-status counter's* host-evaluability agreement and is explicitly "REPORTED, never gating";
   it is not admission agreement.
- **#5 historical-gate list — implemented.** `corpus/knowledge/gate-status-ledger.md` says of
  itself: "Adopted from `considerthese/2026-10-26.md` proposal 5 ("Historical-gate list")", and
  `corpus/QUALITY.md:1488-1500` makes the `live`/`historical` label enforceable at registry entry.

**Recommended: #4 only.** It is the one proposal still unimplemented *and* the one that fits this
round's claims: C1's contract §Limits states that the non-author closure "is what catches a
transcription", so the closure is load-bearing for C1 and nothing in the lane counts whether it has
ever disagreed. Exact row it should land as — a **QUALITY criterion**, appended (never inserted)
after the round-75 criterion, with this shape:

    ## Round-82 criterion — closure agreement is counted per round (append-only)

    Admit: a round's lesson Gate block carries one tally line
      `closure agreement: claims=<n> agreed=<a> disagreed=<d> reason-only=<r>`,
    where <n> equals the round's settled-claim count, <a>+<d>+<r> = <n> with no unclassified
    claim, and each claim's outcome is re-derived from the named
    `corpus/lessons/round-<N>-verifier-spotcheck.md` per-claim section — never copied from
    that file's prose.
    Reject: a tally whose <n> differs from the round's claim count; a tally asserted from a
    spot-check that did not read the claim; `reason-only` used to hide an outcome disagreement.
    Grounding: `considerthese/2026-10-26.md` Part 2 proposal 4;
    `corpus/lessons/round-81-verifier-spotcheck.md` §2, §3, §9 (first subject);
    `corpus/lessons/round-82.md` §Gate (first tally). Able-to-fail: a fixture spot-check that
    disagrees on one claim must move `disagreed` from 0 to 1.

Not a lesson row and not a SOURCES row: no external source grounds it, and the round-82 lesson's
Gate block is the criterion's *subject*, not its home. **Do not land it in round 82** — the contract
froze two claims and a new criterion mid-round is scope drift. Route it to round 83 with the row
text above; round 82's own closure then becomes its first data point.

## 4. Cross-domain evidence that belongs to another lane

Two sibling lanes already hold, as grounded entries, the two facts that decide how a
capture-to-capture record may be read. Neither is in `PROVINCE.md` §Adjacent (which names only
tabi, chousa, kagi, kama), so this is an unrecorded edge, not an absorbed one:

1. **mori — a byte difference at one URL need not be content drift.** S594 (RFC 9111 §4.1) and
   `ua-serving-normative-r79.md` K2/K4: if a response nominates a request field in `Vary`,
   changing it selects a different representation; the reader rule is "compare variant to variant,
   or pin per client". Ground belongs to mori; kake must cite it, not re-derive it.
2. **kumitate — a receipt's own age is a separate, consumer-declared gate.** S237 (RFC 9111
   §4.2.3, opened 2026-11-04) and `receipt-age-on-the-compare-path.md`, which lands on kumitate's
   own round-82 compare path. Age answers "when was this written", never "was this true"; a 304
   updates the stored response, so `Age` counts from the later event. Ground belongs to kumitate.
   kake's C2 must not claim receipt-age ground; `order_ok`/`floor_ok` are order/floor conjuncts, not
   an age gate.

Reported, not absorbed. Also reported: `corpus/knowledge/capture-drift-validators.md` was being
written by another seat during this seat's read; its §2 already carries the RFC 9110
validator-vs-bytes reading and its §5 already carries "`verdict=changed` … a reader who takes
`verdict=changed` as 'content changed' is wrong". This report does not restate it as new.

## 5. Connector move — one, bounded

**Evidence (all from committed bytes; no capture B needed).**

- Capture A's three receipts were all fetched at `2026-11-04T12:05:06Z`. At that one instant,
  `x-github-request-id` reads `…:6AEB18EA` (primary) but `…:6AEB1F72` (robots *and* sitemap), and
  `x-timer` reads `S1793793906…` vs `S1793793907…` — the value tracks the *request instant*, not
  the resource. `x-fastly-request-id`, `x-served-by`, `x-cache` and `expires` likewise differ
  across surfaces fetched in the same second (`ConnectorC/evidence.txt` §E).
- `scripts/capture_delta.py` (sha256 `4b0dc252…9680`, 457 lines) counts a surface `identical` only
  when status, body sha256, body length **and the whole header mapping** match, and has no header
  skip list (command 6, exit 1).
- Therefore the round-82 record's `identical=` is structurally 0 for all three surfaces: two
  distinct requests cannot share those per-request fields. `changed=3` is not a finding, and
  `body=` is the only content token.
- Capture A's ETags decode exactly as `%xT-%xO` — `6addaff5` = hex of the shared `Last-Modified`
  (`2026-10-25T07:29:57Z`, one deploy), and `13431`/`3e`/`1e82` = hex of each surface's
  `Content-Length`. That is `corpus/knowledge/ghp-etag-anatomy.md`'s own rule, so
  `field=etag change=changed` is redundant with `last-modified` + `content-length`.
- The one *substantive* gap: `response_snapshot.py` pins the client (`USER_AGENT = "round61"`,
  line 78; recorded per receipt at line 175) and all three surfaces answer `Vary:
  Accept-Encoding`. `capture_delta.py` verifies each receipt's own `method == "GET"` but **never
  compares `userAgent` between the two trees**. A UA bump between rounds would compare two
  different clients' representations and print `body=changed`, which under mori's K2 is exactly the
  case that is not content drift.

**Proposed move (cheapest form, no predicate change).** Land one limits line, this round, on the
record's reading rule — in the round-82 lesson's Gate/Limits block (owner: the lesson scribe) or in
`capture-drift-validators.md` §5 (owner: the C2 entry seat), not in both:

> `[r82-note]` The delta's `identical`/`changed` verdict is a *header-mapping* verdict: on this
> property `x-github-request-id`, `x-fastly-request-id`, `x-timer`, `x-served-by`, `x-cache` and
> `expires` are per-request (proved by the three same-instant capture-A receipts disagreeing on
> them), so `identical=0 changed=3` is expected and is not drift; read `body=` and `status=` only.
> `field=etag` is redundant: the ETag decodes as `%xT-%xO` over the shared `Last-Modified` and each
> `Content-Length` (`ghp-etag-anatomy.md`). And both trees must have been fetched by the same
> client: `response_snapshot.py` records `userAgent` per receipt, but `capture_delta.py` does not
> compare it across trees, so a UA change between rounds is invisible in the verdict.

Round-83 follow-on (not this round, because it changes the committed record's bytes): have
`capture_delta.py` fault on a per-surface `userAgent` mismatch, `per` mori S594 K4 ("pin per
client"). That is one added check in the verifier it already runs over both trees.

**Axes.** Improves `freshness` (C2's record stops being readable as drift it cannot contain) and
`calibration` (the round's lowest axis: the claim's evidence is now bounded by a derived property
of the frozen instrument rather than by prose). Harms neither — no predicate, target, kill rule,
control or tool byte moves.

**Risks.** (i) The note must not read as a verdict on any surface — it says what the record cannot
say, not that the property is clean. (ii) It presumes the round-82 capture uses the same instrument
and UA as capture A; verify by reading `userAgent` in the round-82 `response.json` before landing
the sentence. (iii) Two owners are named for one slot; if both land it, the schedule's append-only
rule turns a duplicate into a false correction — land it in exactly one.

**Verification.** (a) The theorem is falsifiable today: if the committed
`.ufo/waves/round-82/controls/after-c2-delta.txt` shows `identical>0`, either the tool excludes
header fields (it does not: command 6 returned no match) or the capture step normalizes
`response.json` — either would be worth knowing, and this prediction would be wrong. (b) Re-derive
§E/§F with `python3 -B evidence.py`; it is deterministic (two runs, identical md5
`d1a55ea8…f9b6`). (c) After the round-83 change, the selftest should gain one fixture: two trees
with differing `userAgent` and identical bodies must fault, not print `identical`.

## Verdict

C2 stays inside kake's province — no sibling lane holds a capture-to-capture drift gate, the ETag /
§8.8.3 ground is kake's own, and no sibling claims a ds4cc surface — but two unrecorded adjacencies
(mori's `Vary` rule, kumitate's receipt-age rule) must be cited rather than absorbed. The merge/kake
package re-derives at **8 id collisions** (all same-id, same-source), **27 staged rows with an
already-held URL** (8 same-id + 19 under another lane id) and **102 unscreened rows** against a
2026-10-24 package, so `Assimilation: none` is re-derivable only if it names those three numbers.
Of the three candidates, **#4 (gate-agreement ledger)** is the single unimplemented proposal and the
one that fits C1's dependence on the non-author closure; recommend it as a QUALITY criterion in
round 83, with the row text above, not in this round.

Route: `Assimilation: none` numbers and the `[r82-note]` text to the round-82 lesson owner
(C1 rows) and the C2 entry owner — one slot, one owner. No production file was written by this
seat; nothing here is a claim that any surface is correct, current, or drifted.
