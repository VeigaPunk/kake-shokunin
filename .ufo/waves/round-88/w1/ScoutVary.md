# ScoutVary — round 88 C1/C2 recon, data-walk and bounded planning

Seat: `ScoutVary` (scout, leaf, no dispatch). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Base `f4479c14813037ad993a49a3dee4028763470f7a`. Freeze named in the brief: v2 `8063739791e21a8d7966fd968913e552e1433881`;
the lane has since moved to **v3 `52e41d2d0ea6f5a7eaf8b5ac09ab0d78c538d644`** ("freeze amendment v3 — validation precedes the
wildcard rule", 2026-11-04 15:58:05). Everything below states which revision it was measured against. All probe scripts and
their raw output are copied to `.ufo/waves/round-88/w1/ScoutVary/` (receipts, not findings).

**Axes.** The two claims under audit are `calibration` (lowest owned axis, 2 HOLD) and `freshness` (10 HOLD). Neither the
C1 counter nor the C2 counter is itself a claim; both are the *measuring instruments* for a claim, so the axis this seat
protects is **calibration of the round's own instruments** (does the counter measure the stated thing, and does the stated
thing match the RFC it cites?). Findings below are grouped as: (A) ground inventory and duplication, (B) base data-walk
proofs, (C) case-set audit against RFC 9111 §4.1, (D) defects in the round's own counters and case set, (E) planning data
for the carrier. Every command is reproduced in the receipts.

---

## A. Ground inventory: what Vary / cache-key / request-header-matching / conditional-request material the lane already holds

Greps run over `LANE/corpus`, `LANE/scripts`, `LANE/SKILL.md`, `LANE/PROVINCE.md` (case-insensitive
`\bvary\b`, `cache[- ]key`, `request[- ]header`, `conditional`, `revalidat`, `if-none-match|if-modified-since|if-match|precondition`).

### A.1 In-lane corpus hits (file:line)

| hit | content | relation to round-88 C2 |
|---|---|---|
| `corpus/knowledge/header-change-classes.md:93-96` | `vary` is a *representation* class field; "`vary` … §4.1 makes it the field that selects a stored response for a request, so a moved `vary` changes the object-to-request mapping" | holds the **selection role** of §4.1, not the matching algorithm |
| `corpus/knowledge/capture-drift-validators.md:222-226` | cites **mori S594** §4.1 `Vary` as *adjacency, not re-taught* | the lane's own pointer that §4.1 lives in another lane's registry row |
| `corpus/lessons/round-84.md:87-94` | rejects §4.1's normalisation sentence as ground for the `reordered` **response** class, and records the flip: "if the lane ever compares request-header values across captures — a `Vary`-key drift check — this sentence becomes the correct anchor for that new row, and the tool would then need a **request-side grammar**" | **direct pre-authorisation of round-88 C2's ground**; also the origin of the `, `-combination rule used by the reader |
| `corpus/lessons/round-84-verifier-spotcheck.md:74` | the reject row itself; exact quote "reordering field values when order is not significant" with the scope note that it is about **two request** header sets | the sentence C2's profile reasons about |
| `corpus/lessons/round-82.md:246-249` | mori's Vary rule (S594) applied to a capture-to-capture `user-agent` difference | adjacency, applied not derived |
| `corpus/lessons/round-82-verifier-spotcheck.md:103` | adjacency table: mori `Vary`/cache-selection + kumitate receipt-age | adjacency ledger |
| `corpus/lessons/round-87.md:38,44` | §4 "separately requires matching URI/method/**Vary** and directive/validation conditions"; frontier keeps "Date/Age extraction, **Vary**/Pragma … remain open" | names Vary as the lane's own open frontier → C2 closes part of it |
| `corpus/lessons/round-87-verifier-spotcheck.md:169-181` | routed defects **R1** (ledger JSON in `knowledge/` cannot open with the trio), **R2** (non-integer reported as "not boolean"), **R3** (ephemeral `TMPDIR=/fast/scratch/...` in the recheck line) | the three defects C1 re-routes as D1/D2/D3 |
| `corpus/knowledge/cache-current-age.md:54` | "§4 adds URI/method, Vary, directives, validation and other applicable reuse conditions" | the entry whose `recheck:` line D3 rewrites |
| `corpus/knowledge/cache-control-effective.md:70` | "no Vary, Age calculation, Pragma …" (scope exclusion) | neighbouring reader, Vary deliberately out of scope |
| `corpus/knowledge/hreflang-declaration.md:159` | "No HTTP headers, no `Vary`." | scope exclusion |
| `corpus/README.md:667`, `:694-697` | round-83/87 coverage tables: "Age/Vary/Pragma … remain frontier" | the frontier sentence C2 partially advances |
| `corpus/SOURCES.md:203` (S456), `:204` (S457), `:207` (S461), `:209` (S462) | the four RFC-9111 rows the lane holds (`.txt` §3.1/§3.2/§4/§4.2/§4.2.3/§4.3.1/§4.3.4; §4.2/§5.2; §4.2.3 age; RFC 7234) | **no §4.1 row exists in the lane's registry today** — C2 adds one (see A.3) |

### A.2 Scripts (`LANE/scripts`)

- `scripts/header_change_class.py:16` and `:52` — `vary` appears only as a *response* header name in the
  representation/policy/unknown class table. No matching logic.
- `scripts/hreflang_audit.py:54` — "no `Vary`" scope exclusion.
- **No script in the lane performs request-header matching, cache-key construction, conditional-request selection or
  revalidation.** `grep -rn -i -E 'if-none-match|if-modified-since|if-match|precondition' scripts/` → 0 hits;
  `grep -rn -i 'revalidat' scripts/` → 3 hits, all the literal `must-revalidate` token inside
  `scripts/cache_control_effective.py:145,182,185`. `grep -rn -w -i 'vary' scripts/*.py scripts/*.mjs` → only the two files above.
  **C2's reader is therefore the first lane artefact that implements any part of §4.1; nothing in `scripts/` duplicates it.**

### A.3 `LANE/SKILL.md` and `LANE/PROVINCE.md`

- `SKILL.md`: **zero** `vary` hits (`grep -n -i 'vary' SKILL.md` → nothing). The cache neighbourhood is
  `SKILL.md:1568` (`cache_control_effective.py`), `:1587` (`cache_current_age`), `:1588` (`c87 finite claims`). A new
  registry row for `vary_match.py` / the round-88 counters belongs in this block.
- `PROVINCE.md:668-669` — `vary` sits in the `representation` class of the drift taxonomy; `PROVINCE.md:697` — "missing-Date
  handling, cache storage/reuse permission, **Vary**/Pragma … remain outside this capability". C2 changes the *scope
  sentence* at 697 (Vary matching moves inside) but not the class table at 668-669 (`vary` is still a response-header class
  there — a different axis).

### A.4 Fleet-side duplication (read-only; nothing written)

`mori-shokunin/corpus/SOURCES.md:375` = **S594**, tier A, `https://www.rfc-editor.org/rfc/rfc9111.txt`, anchored §4.1 with
the quotes `:528-534`, `:552-554`, `:556-557`, `:559`, `:576` and its own sha256 `aeb52adb…`. `round-84/w1/ConnectorSibling.md:30`
records the ruling: "the `Vary`/cache-key half of §4.1 is **`S594`'s and must not be restated**".

So the ground C2 rests on is **already held by a sibling lane at tier A**; the round-88 contract's "one SOURCES row for RFC
9111 section 4.1" would create a *second* tier-A registry row for the same document and section across the fleet. Measured
consequence in the fleet census (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate`):

- new kake row, URL `www.rfc-editor.org/rfc/rfc9111.txt`, **scope cell identical to S456's** → `E04 duplicate url … within scope`,
  **validate exits 1** (fatal);
- new kake row, same URL, **different scope cell** → `W04 duplicate url … across scopes` (warning, exit 0);
- new kake row, URL `httpwg.org/specs/rfc9111.html` → `W04` again (S461/S462 already share that URL; the committed
  pre-round census `controls/census-before.txt` already lists both W04s).

Receipt: `receipts/census-scope-probe.txt`. **Planning consequence:** the new SOURCES row must carry a scope cell distinct
from S456's (else the fleet census goes red), and the knowledge entry should cite mori S594 as the tier-A §4.1 row rather
than re-anchoring §4.1 as if kake were first to retain it.

### A.5 What C2 covers vs duplicates — the sharp statement

- **C2 covers (new in-lane capability):** the *matching* half of RFC 9111 §4.1 — an offline, conservative decision
  procedure over (Vary value, original request's header fields, presented request's header fields) producing
  match/mismatch/refused. Nothing in the lane or fleet implements this; round-84's flip note explicitly anticipated that a
  `Vary`-key drift check "would then need a request-side grammar".
- **C2 duplicates (at registry level):** mori's S594 (same document, same section, tier A) — the r84 connector ruled the
  §4.1 half "must not be restated". The *knowledge entry* is new (an executable reader); the *source row* is a restatement.
  The round's own contract already concedes the pattern by reporting `Assimilation: none` for the merge/kake package
  (eight colliding registry ids).
- **C2 does not duplicate and must not claim:** cache-key construction, storage, revalidation, freshness, serving,
  browser behaviour (the contract's "Not claimed" list). Confirmed empirically: no lane script touches those.

---

## B. Base data-walk proofs at `f4479c14`

| claim | command | result |
|---|---|---|
| `scripts/vary_match.py` absent at base | `git -C LANE show f4479c14:scripts/vary_match.py` | `fatal: path 'scripts/vary_match.py' does not exist in 'f4479c14'`, exit 128 |
| `corpus/knowledge/gate-agreement-metadata.md` absent at base | `git -C LANE show f4479c14:corpus/knowledge/gate-agreement-metadata.md` | `fatal: path … does not exist in 'f4479c14'`, exit 128 |
| base `recheck:` line (D3) | `git -C LANE show f4479c14:corpus/knowledge/cache-current-age.md \| sed -n 3p` | `recheck: 180d or source/adapter change; GET https://httpwg.org/specs/rfc9111.html#age.calculations and compare §4.2.3 equations; offline command TMPDIR=/fast/scratch/hyaku/kake-r87/L1 python3 -B scripts/cache_current_age.py --selftest (create the explicit scratch directory first).` — names `/fast/scratch/hyaku/kake-r87/L1` and `TMPDIR=`, and contains no `mktemp -d` |
| base diagnostic line (D2) | `git -C LANE show f4479c14:scripts/cache_current_age.py \| sed -n 34p` | `            raise ValueError(f"{key} must be an integer, not boolean")` — the word `boolean` is emitted for a **float** input; the float and bool paths share one message |
| D1 evidence | `git -C LANE show f4479c14:corpus/knowledge/gate-agreement-ledger.json \| python3 -c '…'` | 8 rows of admit/reject metadata, a `.json` file sitting in `knowledge/` with no `source:`/`verified-at:`/`recheck:`; the base counter reports `companion entry missing` |

Base counter receipts reproduced byte-for-byte:
- C1: `python3 -B .ufo/waves/round-88/c88_defect_queue.py --root LANE --revision f4479c14 --work <scratch>` →
  `C1v1 revision=f4479c14 items=3 open=3 closed=0 met=false`, exit 1 — identical to committed `controls/base-c1.txt`.
- C2: `python3 -B .ufo/waves/round-88/c88_vary.py --root LANE --revision f4479c14 --work <scratch>` →
  `frozen=0/20 random=0/200 met=false`, exit 1 — identical to committed `controls/base-c2.txt` **at v3** (sha
  `52714a5f…`); the v2-committed copy of that receipt carries the superseded `004a8eb…` sha (see D.4).

Also confirmed: the three frozen blobs in `frozen/` are byte-identical to base (`base-cache-current-age.md`
`8bbbeb9e…`, `base-cache_current_age.py` `d1b09ae1…`, `base-gate-agreement-ledger.json` `ef58f909…`).

---

## C. Case-set audit: all 20 frozen cases against RFC 9111 §4.1

Reference bytes: `.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt`, sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`
(identical to mori's retained copy) — §4.1 at lines 526-557. RFC 9110 bytes: `.ufo/waves/round-80/sources/rfc9110.txt`
(sha `21c1cdce…`), §5.1 field names at 1468, §5.2 combined field value at 1492, §5.3 field order at 1515, §5.6.1.2 recipient
requirements at 1690ff, §5.6.2 tokens at 1728, §8.4.1 content codings at 3105, §12.4.2 weight at 5362, §12.5.3
Accept-Encoding at 5525, §12.5.5 Vary at 5668.

**Constant-`match` tool: 7 of 20 frozen cases pass** (the seven labelled `match`: ids 1, 2, 4, 9, 11, 13, 16) — the
committed control `controls/ctl-c2-constant-match.txt` says `7/20 + 67/200` and my independent count of the v3 seeded
population gives match=67, mismatch=109, invalid=24 (v2: match=67, mismatch=112, invalid=21) → constant-`match` also
passes 67/200. The stub tallies therefore reproduce.

### C.1 Verdicts

| id | expected | my verdict | deciding text |
|---|---|---|---|
| 1 | match | **correct** | §4.1 528-534; identical values need no transformation |
| 2 | match | **correct** | §4.1 528-534 + RFC 9110 §5.1 (1468) field names case-insensitive |
| 3 | mismatch | **label contradicts §4.1's match definition** (see C.2) | §4.1 536-538 ("if and only if … by applying any of the following") + 546-550 (case-normalization "where values are defined to be case-insensitive") + RFC 9110 §8.4.1 (3105) content codings case-insensitive + §12.5.3 (5540) accept-encoding codings are content-codings |
| 4 | match | **correct** | §4.1 552-554: absent from a request ⇒ may only match another request if also absent there |
| 5 | mismatch | **correct** | same sentence (absent on one side only) |
| 6 | mismatch | **correct** | same sentence |
| 7 | mismatch | **correct** | §4.1 556-557: a Vary value containing `*` always fails to match |
| 8 | mismatch | **correct** | same sentence ("containing a member `*`") — `*` dominates the list |
| 9 | match | **correct** | §4.1 540-541 (whitespace) + RFC 9110 §5.5 (field value excludes leading/trailing whitespace; parsers MUST exclude it) |
| 10 | mismatch | **defensible but on the same tension as id 3** | §4.1 546-550 gives "reordering field values when order is not significant" as an example; the basis text itself concedes "even though the field spec may allow it" |
| 11 | match | **correct** | §4.1 528-534 (all nominated fields match) |
| 12 | mismatch | **correct** | §4.1 528-534 (one nominated field differs) |
| 13 | match | **correct** | §4.1 528-534 over the *set* of nominated fields; RFC 9110 §5.1 makes the two members the same field, so the duplicate is redundant |
| 14 | exit 1 (refused) | **label is an adapter policy that contradicts RFC 9110 §5.6.1.2** (see C.3) | §4.1 536-538 gives no "invalid" outcome; RFC 9110 §5.6.1.2 recipient rules (1690ff) require a recipient to parse and ignore empty list elements |
| 15 | exit 1 (refused) | **correct** | RFC 9110 §5.6.2 (1728) `token = 1*tchar` (no SP) + §5.1 + §12.5.5 (5668) `field-name` |
| 16 | match | **correct label, citation slightly off** | RFC 9110 §5.2 (1492-1512) gives the combined field value; the *`, `-combination convention* is §5.3 (1515ff, "For consistency, use comma SP"). The case cites only §5.2 |
| 17 | mismatch | **correct** | combined presented value `gzip, br` ≠ stored `br, gzip`, order preserved |
| 18 | mismatch | **label contradicts §4.1's match definition for accept-encoding** (see C.2) | §4.1 540-541 (whitespace "where allowed in the header field's syntax") + RFC 9110 §12.4.2 (5362) `weight = OWS ";" OWS "q=" qvalue` — the internal OWS is legal syntax, so the two values match |
| 19 | exit 1 (refused) | **correct** (adapter input typing) | no §4.1 bearing; basis says "local adapter" |
| 20 | exit 1 (refused) | **correct** (adapter input typing) | same |

### C.2 The systematic issue: `mismatch` is not §4.1's `match`, and three frozen cases encode that

RFC 9111 §4.1 defines the relation in the **biconditional** direction (line 536-538): "The header fields from two requests
are defined to match **if and only if** those in the first request can be transformed to those in the second request by
applying any of the following: adding or removing whitespace, where allowed in the header field's syntax; combining
multiple header field lines with the same field name; **normalizing both header field values in a way that is known to have
identical semantics, according to the header field's specification (e.g., reordering field values when order is not
significant; case-normalization, where values are defined to be case-insensitive)**".

Three frozen cases sit on the *permissive* side of that biconditional and therefore return `mismatch` where §4.1 says the
fields **match**:

- **id 3** (`gzip` vs `GZip`): RFC 9110 §8.4.1 (3105) "All content codings are case-insensitive"; §12.5.3 (5540) makes
  accept-encoding's `codings` content-codings. ⇒ §4.1's third bullet applies ⇒ §4.1 verdict = **match**.
- **id 10** (`gzip, br` vs `br, gzip`): §4.1's own example "reordering field values when order is not significant";
  accept-encoding preference is carried by q-values (§12.4.2), not by list position. ⇒ arguably **match**; the case basis
  already concedes the field spec "may allow it".
- **id 18** (`gzip;q=1` vs `gzip; q=1`): RFC 9110 §12.4.2 (5362) `weight = OWS ";" OWS "q=" qvalue` — the internal OWS is
  *legal syntax* for the field, so §4.1's first bullet ("adding or removing whitespace, **where allowed in the header
  field's syntax**") applies ⇒ §4.1 verdict = **match**.

The contract acknowledges the direction of travel: "a `match` verdict is always produced by transformations §4.1 permits
while a `mismatch` may be more conservative than a field-specific rule" — safe for reuse (a stricter `mismatch` never
authorises reuse), and the L1 candidate's own docstring says the same. **But the case `basis` strings are the problem:** id 3's
basis says "although a field-specific rule **might** permit it" and id 18's says "conservative profile: no internal
whitespace normalisation" — they present a *local adapter rule* as if it were the RFC's answer. The round-84 verifier already
ruled that §4.1's normalisation sentence "becomes the correct anchor" for a request-side grammar, so the round cannot
present these three as RFC verdicts.

**Action for the carrier (not a counter change):** the knowledge entry and the SOURCES row must say *"a conservative subset
of §4.1's permitted transformations; `mismatch` may be stricter than §4.1 for a field whose syntax admits the
normalisation we decline (case-insensitive codings, list order, internal OWS)"* — and the three case `basis` strings should
not be quoted as §4.1's verdicts. If the L1 instead wants §4.1-literal verdicts, ids 3/10/18 must flip — that is a
case-set edit, which the contract forbids after scoring, so the profile route is the only legal one.

### C.3 Empty list elements: the case set pins a *stricter-than-RFC* recipient rule

RFC 9110 §5.6.1.2 (recipient requirements): "A recipient MUST parse and ignore a reasonable number of empty list elements …
In other words, a recipient MUST accept lists that satisfy the following syntax: `#element => [ element ] *( OWS "," OWS
[ element ] )`". The round's reader is a *recipient* of a Vary field value. The frozen reference nonetheless refuses:
- frozen id 14 (`vary: ""`) → `invalid`;
- 11 of the 200 seeded cases carry an empty Vary member (4 × `vary: ""`, 7 × trailing comma) and are all labelled `invalid`;
- the reference's `reference()` returns `invalid` for any Vary with an empty member, i.e. `accept-encoding,` is refused where
  §5.6.1.2 says it must be *accepted and the empty element ignored*.

Measured: a reader that follows §5.6.1.2 (ignore empty list elements; empty Vary ⇒ no nominated field) scores
**19/20 frozen and 189/200 seeded — it fails the round's own counter** (receipt `receipts/probe_readers.txt`). The refusal is
safe in the reuse direction, but it is an **undeclared** narrowing: the contract's Profile paragraph does not mention it,
and the r87 routing (R1) never asked for it.

### C.4 Branches the frozen set and the seeded population do *not* pin (measured by mutating the counter's own reference)

`probe_mutations.py` / `probe_mutations2.py` (receipt `receipts/probe_mutations*.txt`) — one branch mutated at a time,
counting how many frozen/seeded verdicts move:

| mutated branch | frozen moved | seeded moved |
|---|---|---|
| value case-folding | 1 | 27 |
| value OWS trimming (`strip(' \t')` → no trim) | 1 | 4 |
| value trimming (`strip()` instead of `strip(' \t')`) | 0 | **0** |
| `*` rule ignored | 2 | 11 |
| one-sided absence → match | 2 | 14 |
| non-token member allowed | 1 | 2 |
| non-string field value allowed | 0 | 2 |
| empty-member / empty-Vary accepted | 0 | 0 (already refused by the token check) |
| case-variant duplicate key in one request allowed | 0 | **0** |
| `, `-combination replaced by `,` | 1 | 1 |
| `, `-combination replaced by `; ` | 1 | 1 |
| token regex admitting LF | 0 | **0** |

Three consequences:

1. **The seeded population is self-referential.** Its expected verdicts are produced by the very `reference()` the candidate
   is scored against, so an error in `reference()` cannot show up as a seeded failure; only the 20 hand labels can catch it.
   This is exactly why C.2/C.3 matter: the seeds cannot be the oracle of the oracle.
2. **Unpinned branch (a): a field name may carry a trailing LF.** `TOKEN = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")`
   used with `re.match` — Python's `$` matches before a final newline, so `'gzip\n'` passes as a token. Measured:
   `reference('gzip\n', …) == 'match'`; the **L1 candidate at `.ufo/waves/round-88/w1/L1/vary_match.py` returns
   `match`, exit 0** for `{"vary": "accept-encoding\n", …}`. RFC 9110 §5.5: "Field values containing CR, LF, or NUL
   characters are invalid and dangerous … a recipient of CR, LF, or NUL within a field value MUST either reject the message
   or replace each of those characters with SP"; §5.6.2 `token = 1*tchar` excludes LF. **This is a live defect in the
   candidate that will ship as `scripts/vary_match.py`, and the counter cannot see it (0 frozen, 0 seeded coverage).**
3. **Unpinned branch (b): a request map with two case-variant spellings of one field name is refused.** Both the
   reference and the L1 candidate refuse `{accept-encoding: …, Accept-Encoding: …}` as "ambiguous duplicate name". RFC 9110
   §5.1 makes the two names *the same* field, and §5.2/§5.3 say the combined field value is the ordered concatenation of
   the field-line values — so the contract's own Profile sentence ("multiple field lines combine in order with `, `")
   describes combining, not refusing. The JSON list form is the adapter's way of expressing multiple field lines; the
   case-variant-key form is refused instead. 0 frozen, 0 seeded coverage ⇒ the counter cannot distinguish the two readings.

---

## D. Defects in the round's own counters and case set

D.1 (C2 counter) **The v3 amendment moved the oracle onto the already-authored candidate.** v3 changed one thing in
`reference()`: the `*` rule now runs *after* input validation, so a malformed request map with `*` in the Vary value yields
`invalid` instead of `mismatch`. That flips **exactly three** seeded verdicts — `r53`, `r150`, `r193` — and those three are
**exactly** the cases where the L1 candidate disagreed with the v2 oracle (probe `probe_l1_vs_v2.py`: candidate-vs-v2 = 3
disagreements, candidate-vs-v3 = 0). Timeline: wave dispatched `w1.ready.dispatched` 15:52:15 → candidate file
`w1/L1/vary_match.py` mtime **15:56:39** → v3 commit **15:58:05**, which contains *both* the counter change and
`w1/L1/vary_match.py` (170 lines added). The contract's kill rule says "the case set, the seed, the generator and the
reference are not edited after scoring"; the reference was edited after dispatch and after the candidate existed, and the
edit's effect set equals the candidate's disagreement set. *The v3 precedence is defensible on the merits* (a malformed
header map is not a request, so refusing beats reporting a mismatch), but the *coupling* is a calibration exposure the L1
should record explicitly rather than leave implicit. Note also the v3 control restatement is correct and complete for the
counter (`109/200`, `24/200`).

D.2 (C2 counter) **The seeded population cannot detect an oracle error** (see C.4 item 1). Mitigation available at no
target-narrowing cost: cross-check the reference against the 20 hand labels *and* against an independent RFC-derived
reading for the empty-element branch (C.3) — e.g. score the §5.6.1.2-conformant reader and require it to be within the
declared profile, or state the refusal in the Profile paragraph.

D.3 (C1 counter, item D3) **Three false-failure defects in the D3 conjunct**, all reproduced against the committed
counter (receipts `probe_d3*.txt`):
- *Cadence grammar is arbitrary.* The test is `rest[:1].isdigit() and ('d' in rest.split()[0].lower() or rest[:4].isdigit())`.
  Measured: `180d` **accepted**, `180-day` **accepted**, ISO date **accepted**, but `180 days`, `90 days` and `6 months`
  are **rejected** with "recheck line does not open with a cadence or ISO date". The contract only requires "a cadence in
  its single `recheck:` line" and prescribes no format ⇒ a carrier edit that writes "180 days" is falsely failed.
- *Diff-based history check is alignment-sensitive.* The check walks `difflib.SequenceMatcher` opcodes and allows an
  `insert` or a 1-line→1-line `replace` of a `recheck:` line. Inserting the required mktemp command **immediately after**
  the recheck line yields the opcode `('replace', 2, 3, 2, 4)` — a 2-line replacement region — and the item then reports
  "history-preservation violation at base line 3 (replace)" even though the only base line that changed *is* the recheck
  line and everything else is a pure insertion. Measured: insert-after-recheck **rejected**, insert-before-recheck
  **rejected**, insert-mid-body **accepted**, append-at-EOF **accepted**. The counter's own green fixture appends at EOF,
  so its selftest never exercises the natural placement.
- *mktemp command must be on one line.* The predicate is `'mktemp -d' in l and TOOL in l and '--selftest' in l` for a single
  line `l`. A carrier edit that puts the command on one line and `TMPDIR=$(mktemp -d)` on the next is rejected even though
  the contract only asks the body to "carry the offline selftest command in a `mktemp -d` form".

D.4 (C1 counter, item D1) **The ledger path is frozen, which forecloses the other routed R1 option.** R1 offered "relocate
it to a metadata path **or** add a sourced companion entry"; the contract picked the companion, and D1 additionally
requires the ledger bytes to equal the frozen base copy, so relocation would fail D1. That is consistent with the contract,
but it should be stated as a *scope narrowing of the routed defect*, not silently inherited.

D.5 (C1 counter) **No defect found** in D2: the float/bool split is genuinely checkable (base message contains `boolean`
for a float input; `scripts/cache_current_age.py` `--selftest` is green at base: "selftest: 61 isolated CLI fixtures passed",
exit 0). D1's sha256 binding to the ledger bytes is sound (the digest is only derivable from the bytes).

D.6 (round hygiene) **Stale v2 receipts under `w1/`.** The committed pre-round census `controls/census-before.txt` and the
committed control receipts were regenerated at v3 (`base-c2.txt` now carries `52714a5f…`), but **42** occurrences of the
superseded v2 sha `004a8eb7…` remain in `w1/MutReader/receipts/c2_sweep.json` (mtime 16:05:45, i.e. *after* v3), plus
`w1/ExecReader/c2-score.json`, `w1/ExecReader/alt-validity-first.json`, `w1/ReviewReader/receipts/c88-score-L1-candidate-v2.json`,
`w1/ScribeLesson/receipts/scribe-probes.json`, and the `v2_*` receipts under `w1/CriticClaims/`. `w1/ExecReader/c2-score.json`
also reports `tool_sha256 51f5d778…` for `.../w1/ExecReader/vary_match.py`, whose current bytes hash to `fdceef47…` — that
receipt describes a candidate revision that no longer exists at that path. A reader comparing receipt ↔ file will find a
mismatch. (Sibling seats' business, but it is the round's calibration record.)

D.7 (round hygiene) **`.ufo/waves/round-88/w1/` tracks only two files** (`git ls-files .ufo/waves/round-88/w1/` →
`w1/L1/vary_match.py`, `w1/swarm-registry.json`); every other seat receipt is untracked, so the round's evidence is not yet
committed. Also `validator.err` is a 0-byte tracked file and `w1.ready`/`w1.ready.dispatched` are untracked.

D.8 (round hygiene) **The `SOURCES.md` E11 warnings are pre-existing and not this round's** — a fresh `validate` on the
committed `corpus/SOURCES.md` emits ~250 `E11 missing used-by …` lines because the census resolves `used-by` paths against
the *fleet root*, and my scratch validation had no sibling lanes present. Not a round-88 defect; noted so the L1 does not
chase it.

---

## E. Planning data for the carrier (bounded; finders only, no production edits)

1. **Shipped-candidate defect to fix before integration:** the trailing-LF token hole in
   `.ufo/waves/round-88/w1/L1/vary_match.py` (C.4 item 2). One-character-class fix: use `re.fullmatch` (or add `\Z`), or
   reject any member containing CR/LF/NUL per RFC 9110 §5.5. Verified consequence today: the candidate answers `match`
   for `{"vary": "accept-encoding\n", …}`. Nothing in the frozen set or the seeded 200 will catch it.
2. **Case-variant duplicate field names** (C.4 item 3): decide and *declare* one reading (combine in order, per §5.2/§5.3 and
   the contract's own Profile sentence) rather than refusing silently; either way it is unpinned by the populations.
3. **Empty list elements** (C.3): either state the refusal in the Profile paragraph as a local adapter boundary, or accept
   the §5.6.1.2 reading — the latter changes 12 population labels (1 frozen + 11 seeded) and therefore cannot be done
   after scoring. Recommend *stating* it, not changing it.
4. **Knowledge-entry wording** (C.2): say "conservative subset of §4.1's permitted transformations; `mismatch` may be
   stricter than §4.1 where the field's syntax admits a normalisation we decline (case-insensitive codings, list order,
   internal OWS)". Do not quote frozen ids 3/10/18 as §4.1 verdicts.
5. **SOURCES row** (A.4): a §4.1 row for kake needs a scope cell **different** from S456's (else `E04`, census exit 1); cite
   mori **S594** as the tier-A §4.1 registry row rather than re-anchoring it; and the row's `used-by` must list
   `corpus/knowledge/vary-matching.md` once that file exists. Also note the fleet merge/kake package already reports eight
   colliding registry ids and the round reports `Assimilation: none`.
6. **Registry/PROVINCE/SKILL bookkeeping**: `SKILL.md` has no `vary` row — add the reader row next to `:1568`/`:1587`;
   `PROVINCE.md:697` is the scope sentence that changes (`:668-669` does not).
7. **Frozen-blob hygiene**: if the carrier re-runs the counters, quote the **v3** shas (`cases c461cbd8…`,
   `random 52714a5f…`) and note that v2's `004a8eb7…` is superseded; regenerate or annotate the 42 stale occurrences listed
   in D.6.

---

## F. Honest limits

- The retained RFC bytes I read are the lane's copies (`.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt`,
  `.ufo/waves/round-80/sources/rfc9110.txt`); I did **not** re-fetch either document, so the §4.1 / §5.6.1.2 / §12.4.2
  quotations are byte-local to the lane's retained copies (their sha256s are recorded above and match the values the lane
  and mori already cite). No network access was used in this seat.
- `git show` of the two absent base paths, the counter reproductions, the mutation sweeps, the D3 probes, the reader
  comparisons and the census scope probes all ran against the live lane read-only; the only writes in this seat were the
  scratch tree and this report plus its receipts.
- The **v3 amendment landed mid-seat** (15:58:05). Everything labelled "v3" above is measured against
  `52e41d2d0ea6f5a7eaf8b5ac09ab0d78c538d644`; everything labelled "v2" against
  `8063739791e21a8d7966fd968913e552e1433881`. Where the two differ I say so. The brief named v2 as the freeze; the
  operative freeze is v3 and the contract's own Freeze-history paragraph was updated accordingly.
- Cross-interpreter reproducibility of the seeded population **verified**: identical `random_sha256 52714a5f…` and identical
  counts under CPython 3.11.17, 3.12.15, 3.13.16 and 3.14.8 (host default 3.14.8). No tool was installed or upgraded in
  this seat (`uv 0.13.0` was already present and unused for installation).

## G. Tooling

No installs, no upgrades, no `pacman` invocation. Tools used: `git`, `python3` (3.11-3.14, pre-installed), `grep`,
`difflib`, `re`, `json`, `hashlib`, `diff`, `awk`/`sed` only for reading. No credential, cookie or account state was used;
no URL was fetched.

---

Report: .ufo/waves/round-88/w1/ScoutVary.md
