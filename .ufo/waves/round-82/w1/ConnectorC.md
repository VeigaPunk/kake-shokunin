# ConnectorC — round 82 wave w1

Seat: connector (leaf; no dispatch). Scope: cross-lane, cross-source and proposal-overlap scan.
**Wrote no production file** — this report plus `.ufo/waves/round-82/w1/ConnectorC/` only. I did not
edit `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/lessons/round-82.md`,
`corpus/knowledge/capture-drift-validators.md`, the counters or `scripts/capture_delta.py`.
Lane base: `419866015b1f58e01f061cde9a77d490653d3c76`. Read first: `.ufo/waves/round-82/contract.md`,
`PROVINCE.md` §Core/§Frontier/§Adjacent, `corpus/lessons/round-81-verifier-spotcheck.md` §7,
`considerthese/2026-10-26.md` Part 2.

**Measurement hazard, disclosed.** Sibling seats were writing this tree while I measured:
`git -C <lane> status --porcelain` showed ` M corpus/SOURCES.md` (D1), ` M corpus/QUALITY.md` (D6),
` M corpus/lessons/round-80.md` (D8), `?? corpus/knowledge/capture-drift-validators.md`. An
intermediate working-tree read gave 193 registry rows; that is an artifact of the in-flight D1 edit.
**Every count below is re-derived from the base blob** — `git -C <lane> show
41986601…:corpus/SOURCES.md`, sha256 `1ffc61f1…435f` — so any reader can repeat it.

## Commands run

Exit codes as observed; `read` calls are reads, not commands.

1. `read` — PROVINCE.md, contract.md, considerthese/2026-10-26.md, round-81-verifier-spotcheck.md,
   capture-A receipts, ghp-etag-anatomy.md, scripts/{capture_delta,response_snapshot}.py,
   corpus/lessons/round-82.md, and the mori / kumitate / kama / kasegi / tabi / kaidoku / tameshi /
   chousa files cited below. (no exit code)
2. `git -C <lane> show 41986601…:corpus/SOURCES.md > $S/SOURCES.base.md` → **0**
3. `python3 -B $S/evidence.py > …/w1/ConnectorC/evidence.txt` → **0** twice, md5 `d1a55ea8…f9b6`
4. `bash $S/sibling_scan.sh > …/w1/ConnectorC/sibling-scan.txt` → **0**
5. `git -C /home/vgpnk/Projects/shokuknow log -1 --format='%H %ad %s' -- merge/kake/SOURCES.append.md` → **0**
6. `grep -nE 'EXCLUDE|exclude|SKIP|skip_|IGNORE_|VOLATILE' scripts/capture_delta.py` → **1** (no match
   ⇒ no header skip list; every recorded header field is compared)
7. `grep -rn 'agreed=|disagreed=' --include=*.md --include=*.py .` (wave dirs excluded) → **1** (no
   match ⇒ no committed agreement tally exists)
8. `grep -n -i 'assimilat|merge/kake|shokuknow' corpus/lessons/round-82.md` → **1** (no match ⇒ the
   lesson carries no `## Assimilation` section at all; §2)

Scratch `$S = /fast/scratch/hyaku/kake-r82/ConnectorC/` (removed before yield). Receipts:
`.ufo/waves/round-82/w1/ConnectorC/{evidence.txt,evidence.py,sibling-scan.txt,sibling_scan.sh}`;
`evidence.py` is re-runnable via `CONNECTORC_BASE=<exported base blob> python3 -B evidence.py`.

## 1. Sibling overlap

No sibling lane under `/home/vgpnk/Projects/shokunin/*-shokunin/` holds a capture-to-capture drift
gate, and none claims an owned ds4cc surface (all lines from `ConnectorC/sibling-scan.txt`):

| Primitive | Owner | Committed evidence |
|---|---|---|
| two dated captures of one URL, compared for drift | **kake** | no `capture_delta` outside kake (no match); the only "capture-to-capture" prose elsewhere is kasegi's r31/r32 scout finding (`…/round-31/wave2/ScoutLiveDrift.md:22`, "sha256 is NOT equal") and audio's r77 phase finding — findings, not gates |
| capture **idempotence** (same artifact twice, byte-identical) | tabi | `tabi-shokunin/SKILL.md:371` "plus a re-capture proving the capture operation idempotent"; `corpus/knowledge/live-dynamic-capture.md:110` |
| custody-receipt re-capture reproducibility | kaidoku | `kaidoku-shokunin/SKILL.md:759-761` |
| SOURCES row → committed capture bytes (one capture); pinned capture + quote-exactly-once | kumitate, kasegi | `kumitate-shokunin/scripts/source-capture.mjs` header/rules; `kasegi-shokunin/corpus/instruments/{source-recheck,capture-binding-check}.py` |
| verdict receipt → certified revision | tameshi | `tools/receipt-revision-gate.py` (`RECEIPT_REV_MISMATCH`, `…_CONTENT_DRIFT`) |
| receipt-ledger / append-only disclosure | kama, and kake's own for its `control(s)/` tree | `kama-shokunin/SKILL.md:1577`; kake `SKILL.md:1293` (receipt-rewrite-counter), `:1493` (c79 standing ledger), `:1509` (ledger-append-guard) |
| entity-tag / validator identity semantics (held ground) | **kake** | `corpus/knowledge/ghp-etag-anatomy.md` (S009/S010); `QUALITY.md` "Validator is not identity" |
| RFC 9111 §4.1 Vary / selection; §4.2.3 Age on a compare path | **mori**; **kumitate** | `mori-shokunin/corpus/SOURCES.md:375` (S594) + `ua-serving-normative-r79.md` K2/K4; `kumitate-shokunin/corpus/SOURCES.md:191` (S237) + `receipt-age-on-the-compare-path.md` |
| `ds4cc.com` surfaces | **kake** | `kasegi-shokunin/.ufo/waves/round-23/build/OverlapWeb.md:20`: "PROVINCE.md (kasegi) refuses live-target testing and names kake as adjacent web properties." |

On the three named tokens. **`capture_delta`** — kake only. **ETag / `8.8.3` / validator semantics** —
no sibling holds ground: the 13 tabi files matching `8.8.3` resolve to a *draft CSRF* section
(`corpus/knowledge/csrf-defense-shape-boundary.md:39`, "draft §8.8.3"), and the chousa/mori/kumitate/
revenger hits are retained RFC bodies or unrelated numbering. **receipt-ledger gate** — kama does hold
one, and kama's own round-51 connector already names kake's `.ufo/waves/round-58/c58_receipt_rewrites.py`
as its "sibling design twin" (`kama-shokunin/.ufo/waves/round-51/a2w1/out/N1Overlap.md:90`) — recorded
adjacency, not collision: kama governs *its* registry/Markdown append-only, kake's gates govern kake's
`control(s)/` tree.

**Verdict on province.** C2 stays inside kake's province: the surfaces and the drift question are
kake's, no sibling runs a competing gate, and kasegi explicitly refuses live-target testing. Two
*adjacent* facts are unrecorded and bear on how C2's record may be read — §4.

## 2. merge/kake package re-derivation

Base blob (above) vs `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` (sha256
`5f0cd4c4…f0cc`), last touched by `ba6779f0160d12dd7373627e00291d6d5e3ba7ee` 2026-10-24 10:50 -0300 —
11 days stale against the round-82 base. Both parse cleanly as 11-column GFM: lane `{11: 192}`, 0
escaped pipes; package `{11: 129}`, **113 escaped `\|`** that a naive `split('|')` mis-reads as cell
breaks (my own first pass did, producing a phantom "104 malformed rows" — discarded, not reported).

**Ids.** Lane 192 unique (`S001..S454`, no duplicates; 162 `mined`, 8 `queued`, 22 `rejected`).
Package 129 unique (`S287..S415`, no duplicates; **129/129 `mined`** — admits only, unlike the lane's
own mix). **Id collisions — 8**, every one the *same id carrying the same source cell* in both files: a
row the lane already adopted, not an id assigned to two different sources:

    S312  S329  S367  S372  S373  S374  S390  S409

**Staged URLs already held — 27 rows.** Unit: host+path, query sorted, one trailing slash dropped (so
`http`/`https`, `www.` and fragment differences collapse). 8 are the same-id rows above; the other
**19** stage a source the lane already holds under a *different* id — evidence the package predates
the lane's own adoption of those sources:

    S287→S137  S288→S138  S289→S139  S296→S080  S299→S262  S300→S263  S310→S273  S311→S274
    S323→S286  S352→S438  S375→S419  S376→S420  S380→S418  S395→S423  S398→S425,S427
    S399→S249  S403→S421  S408→S422  S415→S429

102 staged rows match no held URL; they are candidate new ground, not screened by this seat. The
package adds no duplicate the lane lacks: the base lane holds 18 duplicate-URL groups on exact strings
and 22 on the normalized unit (`evidence.txt` §D).

**`Assimilation` — routed finding, not repaired.** Command 8 returns no match:
`corpus/lessons/round-82.md` (207 lines, landed 09:59) has `Claims / Corrections / Gate / Mistakes /
Limits / Settlement` and **no `## Assimilation` section, and no mention of `merge/kake` or
`shokuknow`**; rounds 55–57 carried one. So `Assimilation: none` is not merely un-re-derivable this
round — it is absent. If it is to stay closed, the line must be added with the three numbers above:

> Assimilation: none. At base `41986601` the package holds 129 staged rows against the lane's 192:
> 8 ids collide and carry the identical source cell, 19 further staged rows stage a source the lane
> already holds under another id, and the remaining 102 are unscreened in a package last touched
> 2026-10-24 — so no staged row is both unheld and screened, and none was adopted.

"That the package is stale" alone would not be re-derivable; `8 / 19 / 102` at that blob's sha256 is.

## 3. considerthese mining (one proposal)

- **#2 receipt-rewrite watch — implemented.** `SKILL.md:1293` registers `receipt-rewrite-counter` over
  `.ufo/waves/round-58/c58_receipt_rewrites.py` (ledger `receipt-rewrites.json`); `:1493` adds the
  standing `c79_receipt_ledger.py` gate; `:1509` adds `scripts/ledger_append_guard.py`.
- **#4 gate-agreement ledger — NOT implemented.** The lane holds 59
  `corpus/lessons/round-*-verifier-spotcheck.md` files, each with its own per-claim sections, and
  per-round admission prose in the lessons, but nothing aggregates verifier agree/disagree across
  rounds (command 7, no match). The `agreement` token at `SKILL.md:1396` is the gate-status counter's
  *host-evaluability* agreement, "REPORTED, never gating"; it is not admission agreement.
- **#5 historical-gate list — implemented.** `corpus/knowledge/gate-status-ledger.md` says of itself:
  "Adopted from `considerthese/2026-10-26.md` proposal 5 ("Historical-gate list")", and
  `corpus/QUALITY.md:1488` onward makes the `live`/`historical` label enforceable at registry entry.

**Recommended: #4 only** — the one proposal still unimplemented *and* the one that fits this round:
C1's contract §Limits makes the non-author closure the thing that "catches a transcription", so the
closure is load-bearing for C1, and nothing in the lane counts whether it has ever disagreed. Exact
row it should land as — a **QUALITY criterion**, appended (never inserted) after the round-75 one:

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

Not a lesson row and not a SOURCES row: no external source grounds it, and the lesson's Gate block is
its *subject*, not its home. **Do not land it in round 82** — the contract froze two claims. Route to
round 83; round 82's own closure becomes its first data point.

## 4. Cross-domain evidence that belongs to another lane

Two sibling lanes already hold, as grounded entries, the facts that decide how a capture-to-capture
record may be read. Neither appears in `PROVINCE.md` §Adjacent (which names only tabi, chousa, kagi,
kama), so this is an unrecorded edge — reported, not absorbed:

1. **mori — a byte difference at one URL need not be content drift.** S594 (RFC 9111 §4.1) and
   `ua-serving-normative-r79.md` K2/K4: if a response nominates a request field in `Vary`, changing it
   selects a different representation; the reader rule is "compare variant to variant, or pin per
   client". kake must cite this, not re-derive it.
2. **kumitate — a receipt's own age is a separate, consumer-declared gate.** S237 (RFC 9111 §4.2.3,
   opened 2026-11-04) and `receipt-age-on-the-compare-path.md`, landing on kumitate's own round-82
   compare path. Age answers "when was this written", never "was this true"; a 304 updates the stored
   response, so `Age` counts from the later event. C2 must not claim receipt-age ground:
   `order_ok`/`floor_ok` are order/floor conjuncts, not an age gate.

Also reported: `corpus/knowledge/capture-drift-validators.md` (another seat's, written during this
read) already carries the RFC 9110 validator-vs-bytes reading and the warning that `verdict=changed`
is not "content changed". Not restated here as new.

## 5. Connector move — one, bounded

**Evidence (committed bytes only; capture B is not needed).**

- Capture A's three receipts were all fetched at `2026-11-04T12:05:06Z`, yet disagree on
  `x-github-request-id`, `x-fastly-request-id`, `x-timer`, `x-served-by`, `x-cache` and `expires`
  (`evidence.txt` §E) — six fields that are therefore not resource-stable. §6 refines *which* of them
  are per-request; the conclusion here needs only that they move while the bytes do not.
- `scripts/capture_delta.py` (sha256 `4b0dc252…9680`, 457 lines) calls a surface `identical` only when
  status, body sha256, body length **and the whole header mapping** match, and has no header skip list
  (command 6). `identical=0` is therefore structural for all three surfaces, `changed=3` is not a
  finding, and `body=` is the content token. The lesson's §Limits says the delta "reports
  identical/changed/added/removed **bytes** per surface" — that is the imprecision.
- Capture A's ETags decode exactly as `%xT-%xO`: `6addaff5` = hex of the shared `Last-Modified`
  (`2026-10-25T07:29:57Z`, one deploy) and `13431`/`3e`/`1e82` = hex of each surface's
  `Content-Length` — `ghp-etag-anatomy.md`'s own rule, so `field=etag` is redundant with
  `last-modified` + `content-length`.
- The substantive gap: `response_snapshot.py` pins the client (`USER_AGENT = "round61"`, line 78;
  per receipt line 175) and all three surfaces answer `Vary: Accept-Encoding`, yet `capture_delta.py`
  verifies only each receipt's own `method == "GET"` and **never compares `userAgent` between the two
  trees**. A UA bump between rounds would compare two clients' representations and print
  `body=changed` — under mori's K2, exactly the case that is not drift.

**Proposed move (cheapest form; no predicate change).** Correct and extend the existing §Limits bullet
in `corpus/lessons/round-82.md` (owner: the lesson scribe) — one edit, not a new section, and not
duplicated into the C2 entry:

> `[r82-note]` The delta's `identical`/`changed` verdict is a *header-mapping* verdict: on this
> property `x-github-request-id`, `x-fastly-request-id`, `x-timer`, `x-served-by`, `x-cache` and
> `expires` are per-request (proved by the three same-instant capture-A receipts disagreeing on
> them), so `identical=0 changed=3` is expected and is not drift; read `body=` and `status=` only.
> `field=etag` is redundant: the ETag decodes as `%xT-%xO` over the shared `Last-Modified` and each
> `Content-Length` (`ghp-etag-anatomy.md`). Both trees must also come from the same client:
> `response_snapshot.py` records `userAgent` per receipt but `capture_delta.py` never compares it
> across trees, so a UA change between rounds is invisible in the verdict.

Round-83 follow-on (not this round — it changes the committed record's bytes): have
`capture_delta.py` fault on a per-surface `userAgent` mismatch, per mori S594 K4 "pin per client". One
check added to the verifier it already runs over both trees.

**Axes.** Improves `freshness` (C2's record stops being readable as drift it cannot contain) and
`calibration` (the evidence becomes bounded by a derived property of the frozen instrument, not prose).
Harms neither: no predicate, target, kill rule, control or tool byte moves.

**Risks.** (i) It must not read as a verdict on a surface: it says what the record cannot say, not
that the property is clean. (ii) It presumes the round-82 capture uses capture A's instrument and UA —
read `userAgent` in the round-82 `response.json` first. (iii) Two owners share one slot; a double
landing turns a duplicate into a false correction under append-only — land it in exactly one.

**Verification.** (a) Falsifiable today: if the committed `controls/after-c2-delta.txt` shows
`identical>0`, either the tool excludes header fields (command 6 says it does not) or the capture step
normalizes `response.json` — either would be worth knowing. (b) Re-derive §E/§F with
`python3 -B evidence.py`; deterministic (command 3). (c) After the round-83 change, add one fixture:
two trees with differing `userAgent` and identical bodies must fault, not print `identical`.

## 6. Correction appended after capture B landed (2026-11-04T13:00Z)

Capture B and `controls/after-c2-delta.txt` existed by the time this seat closed, and they falsify part
of §5's field list. Recorded rather than smoothed.

**The record came out exactly as §5 predicted** — `surfaces=3 identical=0 changed=3 added=0 removed=0`
with `body=same` on all three, and the differing field set is `date`, `x-fastly-request-id`,
`x-served-by`, `x-timer`, plus `x-cache` on robots and sitemap. The theorem holds.

**But `x-github-request-id` and `expires` did *not* move A→B**, and decoding them explains why. The
trailing hex of `x-github-request-id` is a **unix epoch**, and `expires − thatEpoch = 600 s`
(`max-age`) on every surface in both trees:

| surface | fill epoch (from request-id) | A fetch | B fetch | `expires` | `x-cache` A→B |
|---|---|---|---|---|---|
| ds4cc-primary | `6AEB18EA` = 2026-11-04T11:37:14Z | 12:05:06Z | 13:00:27Z | 11:47:14Z (= fill+600) | HIT→HIT |
| ds4cc-robots | `6AEB1F72` = 2026-11-04T12:05:06Z | 12:05:06Z | 13:00:28Z | 12:15:06Z (= fill+600) | MISS→HIT |
| ds4cc-sitemap | `6AEB1F72` = 2026-11-04T12:05:06Z | 12:05:06Z | 13:00:28Z | 12:15:06Z (= fill+600) | MISS→HIT |

So `x-github-request-id` is the **cache-fill (origin-fetch) fingerprint**, replayed on every later
hit and revalidation; `expires` is that fill plus `max-age` and is likewise invariant. Both `Age: 0`
in B while `expires` was already 45–133 minutes in the past means the edge **revalidated** and reset
`Date`/`Age` without re-filling: B's `date` is B's revalidation instant, the object is not.

**Consequence for C2, which §5 did not state.** Capture B observed the **same stored objects** as
capture A — robots/sitemap as a HIT on the entry A's own MISS created, primary on an entry filled at
11:37:14Z, 28 minutes *before* A. B therefore caused no origin re-read of any surface. `body=same`
says the edge served identical bytes at two instants; it does **not** say the property's origin was
read twice 55 minutes apart. That is precisely mori's cache-selection rule (S594, RFC 9111 §4.1) and
kumitate's age rule (S237, §4.2.3) instantiated on kake's own property — the two adjacencies of §4.

**Two corrections owed.**

1. My §5 field list: of the six non-resource-stable fields, four are per-request
   (`x-fastly-request-id`, `x-timer`, `x-served-by`, `x-cache`); two are cache-fill-bound
   (`x-github-request-id`, `expires`). §5's "those fields track the request instant" was too broad.
2. `corpus/lessons/round-82.md:236-250` — the landed `[r82-note]` repeats that sentence ("i.e. those
   fields track the request instant, not the resource"). Not my file, so not edited. One appended
   erratum, same shape as the others in that lesson:

   > `[r82-erratum]` The note's "those fields track the request instant" is too broad for two of the
   > six: `x-github-request-id`'s trailing hex is the cache-fill epoch and `expires` is that epoch plus
   > `max-age`, so both are invariant across A→B (primary `…6AEB18EA` = 11:37:14Z with
   > `expires` 11:47:14Z; robots/sitemap `…6AEB1F72` = 12:05:06Z with `expires` 12:15:06Z). Equality of
   > `x-github-request-id` across two trees says the edge served the *same stored object*, not that it
   > re-read the origin. Read `body=same` as "the edge served the same bytes", never as "the property
   > was fetched twice".

**This changes the round-83 instrument and makes it cheaper.** Comparing `x-github-request-id` per
surface across the two trees is a stronger check than the `userAgent` comparison in §5, and it needs
no new capture: equality means B may not have re-read origin, which is a fact the record currently
cannot express. `Age` cannot substitute — B reads `Age: 0` with `expires` 45 minutes stale.

**Verification.** `python3 -B ConnectorC/cachefill.py` → **exit 0**, printing all six
`expires − fill` values as `600` and `A.ghr == B.ghr` as `True` for all three surfaces
(`ConnectorC/cachefill.txt`). Any of those identities failing would break this section.

## Verdict

C2 stays inside kake's province — no sibling holds a capture-to-capture drift gate, the ETag / §8.8.3
ground is kake's own, no sibling claims a ds4cc surface — but two unrecorded adjacencies (mori's
`Vary` rule, kumitate's receipt-age rule) must be cited rather than absorbed — and §6 now instantiates
both on this property: capture B was served the *same stored edge objects* as A (`x-github-request-id`
is the cache-fill epoch, identical A→B), so `body=same` dates two observations, not two origin reads.
The merge/kake package
re-derives at **8 id collisions** (all same-id, same-source), **27 staged rows with an already-held
URL** (8 same-id + 19 under another lane id) and **102 unscreened rows** in a 2026-10-24 package; the
round-82 lesson carries **no `## Assimilation` section**, so `Assimilation: none` is absent rather
than re-derivable and needs the line given in §2. Of the three candidates, **#4 (gate-agreement
ledger)** is the single unimplemented proposal and the one that fits C1's dependence on the
non-author closure; recommend it as a QUALITY criterion in round 83, not this round.

Route: the §2 assimilation line, the §5 `[r82-note]` and the §6 erratum all go to the round-82 lesson's
owner (the L1/scribe) — one owner per slot, one landing each; §5's and §6's notes correct the same
`## Limits` bullet. No production file was written here, and nothing above is a claim that any surface
is correct, current, or drifted.
