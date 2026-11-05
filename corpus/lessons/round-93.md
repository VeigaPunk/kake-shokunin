# Round 93 — kake: self-assessment conformance, and a conditional request evaluation instrument

Author: kake L1 (`KakeR93`). Base `10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5`; freeze
`bb8012fee38c0e497cdaf36337072737bca0b3cd`. Outside closure owns admission and the non-author
spot-check of this Gate.

## Gate

Sources opened this round (CORPUS.md rule 1), by the L1 with one public GET each and retained under
`.ufo/waves/round-93/L1/src/`:

| URL | HTTP | bytes | sha256 | opened |
|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9110.txt` | 200 | 502 941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 2026-11-04T22:20Z |
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 200 | 84 477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 2026-11-04T22:20Z |

`rfc9111.txt` is byte-identical to the round-92 retained body, so the round-92 §4.2.2 ground is
unchanged at this fetch. Line numbers below are plain-text lines of these bodies.

Admits:

- **§13.2.2 lines 6229–6231** — "A recipient cache or origin server MUST evaluate the request
  preconditions defined by this specification in the following order" (20 words). Grounds the
  decision order of contract clauses 7–12.
- **§13.1.1 lines 5794–5795** — "An origin server MUST use the strong comparison function when
  comparing entity tags for If-Match" (15 words). Grounds If-Match using strong comparison only.
- **§13.1.2 lines 5880–5881** — "A recipient MUST use the weak comparison function when comparing
  entity tags for If-None-Match" (15 words). Grounds If-None-Match using weak comparison only.
- **§8.8.3.2 lines 3648–3653** — the two definitions, "two entity tags are equivalent if both are
  not weak and their opaque-tags match character-by-character" (15 words) and the weak counterpart
  "… if their opaque-tags match character-by-character, regardless of either or both being tagged
  as 'weak'" (19 words). Grounds both comparison functions and the Table 3 hand cases.
- **§13.1.2 lines 5930–5933** — "the origin server MUST respond with either a) the 304 (Not
  Modified) status code if the request method is GET or HEAD or b) the 412" (23 words). Grounds
  clause 10's 304-versus-412 split by method.
- **§13.1.3 lines 5956–5958** — "A recipient MUST ignore If-Modified-Since if the request contains
  an If-None-Match header field" (16 words). Grounds If-None-Match precedence over
  If-Modified-Since.
- **§13.1.3 lines 5963–5965** — ignore when "the request method is neither GET nor HEAD" (9 words).
  Grounds clause 11's method gate.
- **§13.1.4 lines 6037–6039** — "A recipient MUST ignore If-Unmodified-Since if the request contains
  an If-Match header field" (14 words). Grounds clause 9's suppression rule.
- **§13.1.4 lines 6072–6073** — "earlier than or equal to the date provided in the field value, the
  condition is true" (16 words). Grounds the `<=` boundary and the equality case.
- **RFC 9111 §4.3.2 lines 889–891** — "the If-Match and If-Unmodified-Since conditional header
  fields are not applicable to a cache" (14 words). Grounds the contract's `role: "cache"` skip.

Rejects:

- **Reject (row candidate): the RFC-Editor errata pages as a grounding row for this contract.** The
  RFC 9110 errata listing carries 14 records and none names a section in 13.x or 8.8.3.x; the RFC
  9111 listing carries two *Reported* (not Verified) records and they touch §3.5 and §4.3.4, not
  §4.3.2 or §13.2.2. So the pages ground nothing about this round's clauses. Flip: an erratum that
  touches §4.3.2, §13.1.x, §13.2.2 or §8.8.3.2.
- **Reject (row candidate): a secondary explainer for the precedence order.** The specification text
  is available and grounds the order directly; a secondary row would be tier inflation and would
  cite ground the lane already holds at tier A. Flip: a precedence point the RFC leaves unstated
  that the secondary source documents with a locator.

### Source-seat re-verification (w1/ScribeSources)

The Gate section above was written by the L1 from the L1's own retained bodies. This block is the
source seat's independent re-verification, done from bodies this seat fetched itself this round
with one public GET each and retained under `.ufo/waves/round-93/w1/ScribeSources/src/`:

| URL | HTTP | bytes | sha256 | opened (UTC) | `cmp` vs `.ufo/waves/round-93/L1/src/` |
|---|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9110.txt` | 200 | 502 941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 2026-11-05T01:26:51Z | identical, exit 0 |
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 200 | 84 477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 2026-11-05T01:26:51Z | identical, exit 0 |

`rfc9111.txt` is also byte-identical to the round-92 retained body
(`.ufo/waves/round-92/L1/src/rfc9111.txt`, `cmp` exit 0), so the round-92 §4.2.2 ground is
unchanged at this fetch. Every quote below was checked mechanically to be an exact substring of its
cited plain-text line span, and to be within the ≤25-word rule, by
`.ufo/waves/round-93/w1/ScribeSources/verify_quotes.py` (receipt
`.ufo/waves/round-93/w1/ScribeSources/quotes.json`, `all_ok=true`, exit 0).

Admits (source-seat, each re-located in the same bodies; line spans are corrected where the
Gate above cites a span that does not contain its quote):

- **§13.2.2 lines 6233–6234** — "A recipient cache or origin server MUST evaluate the request
  preconditions defined by this specification in the following order" (19 words). Grounds the
  decision order of contract clauses 7–12.
- **§13.1.1 lines 5794–5795** — "An origin server MUST use the strong comparison function when
  comparing entity tags for If-Match" (15 words). Grounds If-Match using strong comparison only.
- **§13.1.2 lines 5880–5881** — "A recipient MUST use the weak comparison function when comparing
  entity tags for If-None-Match" (14 words). Grounds If-None-Match using weak comparison only.
- **§8.8.3.2 lines 3648–3649** — "two entity tags are equivalent if both are not weak and their
  opaque-tags match character-by-character" (15 words). Grounds the strong comparison function; the
  worked pairs at lines 3658–3668 give its table cases.
- **§13.1.2 lines 5930–5931** — "the origin server MUST respond with either a) the 304 (Not
  Modified) status code if the request method is GET or HEAD" (22 words). Grounds clause 10's
  304-versus-412 split by method.
- **§13.1.3 lines 5956–5957** — "A recipient MUST ignore If-Modified-Since if the request contains
  an If-None-Match header field" (13 words). Grounds If-None-Match precedence over
  If-Modified-Since.
- **§13.1.3 lines 5963–5966** — "the request method is neither GET nor HEAD" (8 words). Grounds
  clause 11's method gate.
- **§13.1.4 lines 6037–6038** — "A recipient MUST ignore If-Unmodified-Since if the request contains
  an If-Match header field" (13 words). Grounds clause 9's suppression rule.
- **§13.1.4 lines 6072–6073** — "earlier than or equal to the date provided in the field value, the
  condition is true" (16 words). Grounds the `<=` boundary and the equality case.
- **RFC 9111 §4.3.2 lines 889–890** — "the If-Match and If-Unmodified-Since conditional header
  fields are not applicable to a cache" (13 words). Grounds the contract's `role: "cache"` skip.

Three spans in the Gate above do not contain the quote they are attached to, and one quote exceeds
the ≤25-word rule; the corrected spans and quote lengths are in the list above. The spans at issue:
the §13.2.2 evaluation-order sentence is at lines 6233–6234, not 6229–6231 (lines 6229–6231 carry
the "lost update preconditions" rationale); the §13.1.3 method gate spans lines 5963–5966, not
5963–5965 (the phrase "neither GET nor HEAD" crosses into line 5966); and the weak-comparison
definition at lines 3651–3653 is broken across lines by the hyphenation of "opaque-tags", so the
quote as printed in the Gate above is not a literal substring of its span. The §13.1.2 304-versus-412
quote at 23 words is over the ≤25-word rule at 26 words and is shortened above to 22 words. These
are recorded as findings for the round's routed list, not repaired in the Gate above.

Rejects (source-seat):

- **Reject (row candidate): a row for the RFC-Editor errata pages as a grounding row for this
  contract.** The RFC 9110 errata listing (`https://www.rfc-editor.org/errata/rfc9110`, HTTP 200,
  97 750 B, sha256 `cec32fd170146656d933f627b512f2e027ae5c3592f5ec7760c3627493b30505`, fetched
  2026-11-05T01:30:04Z, byte-identical to the L1's retained
  `.ufo/waves/round-93/L1/src/errata-9110.html`) carries 14 records and none targets a section in
  13.x or 8.8.3.x; the RFC 9111 listing (`https://www.rfc-editor.org/errata/rfc9111`, HTTP 200,
  40 383 B, sha256 `1df394f9c04e33e74bf69360e3b7d3bbdeccbe80e27caaa18fdace216ccb54a4`, byte-identical
  to the L1's retained `errata-9111.html`) carries 4 records, of which the two *Reported* ones
  (eid 9004, 9185) touch §3.5 and §4.3.4, one is *Held for Document Update* (eid 9166, §5.2.3) and
  one is *Rejected* (eid 7695, §4.3.2). So the pages carry no accepted change to §13.1.x, §13.2.2,
  §8.8.3.2 or §4.3.2, and they ground nothing about this round's clauses. Flip: an erratum in
  *Verified* or *Held for Document Update* status that touches §13.1.x, §13.2.2, §8.8.3.2 or §4.3.2.
- **Reject (row candidate): a row for a secondary explainer of the precedence order.** The
  specification text is available and grounds the order directly at tier A; a secondary row would
  be tier inflation and would cite ground the lane already holds. Flip: a precedence point the RFC
  leaves unstated that the secondary source documents with a locator.
- **Reject (proposition): "the RFC fixes the 304 body content".** RFC 9110 §15.4.5 lines 7477–7478
  says a 304 response "is terminated by the end of the header section; it cannot contain content or
  trailers", and §15.4.5 lines 7456–7462 lists the header fields the sender must or should
  regenerate; the RFC fixes which *metadata* a 304 carries, not the body of the stored
  representation, whose bytes the client already holds. Flip: a section that states the 304's body
  content.

## Registry

- Rows added: S471–S476 (six rows; see the report's Sources & frontier section for the id list).
- Rows touched: none.
- Census `validate --root … kake`: exit 0 before (`.ufo/waves/round-93/assimilation/census-before.txt`)
  and exit 0 after; W04 advisories 31 → 37 (the new rows re-scope `rfc9110.txt`, already held at
  S033/S453/S454/S455/S465/S466).
- Sidecar (`corpus/knowledge/freshness-sidecar.json`, old→new line, each re-derived by `lineSha256` match, commit `4f5846fe`): `corpus/lessons/round-29.md` 200→203 (`~/.local/bin/time`), `corpus/lessons/round-29.md` 128→131 (`~/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md`), `corpus/QUALITY.md` 649→651 (`~/Projects/shokunin/.ufo/reports/round-33/kake.md`). `freshness-sweep.mjs --offline --section=paths`: exit 2 at `d838e744` → exit 1 with the one pre-existing unannotated miss at `4f5846fe`. Note texts still cite the old line numbers (not validated by the sweep; routed).

## Mistakes

| # | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| 1 | A frozen contract and its own reference disagreed on a field's type | the reference refused `if_unmodified_since: 600` as "date field must be a raw field value string" while the contract's input block declares `if_modified_since`/`if_unmodified_since` as ints; the first `--selftest` run read `reference drift on ius/older-modification-passes` | the counter's pre-freeze reference self-check (`controls/ctl-c2-fixtures.txt` was produced only after the fix) | clause 1 of the contract and the reference both now read the two date fields as `null` or a non-negative int; the refusal cases were re-keyed to a string date and a bool date, and the generator emits ints |
| 2 | A sandbox denied a module the runner itself needs | the positive control failed with `ModuleNotFoundError: No module named 'pkgutil'` inside `runpy.run_path` because `sys.path[:] = [root]` ran without preloading the stdlib modules the sandbox itself uses | the pre-freeze fixture battery (`selftest FAIL: … pos-good.py admitted=False hand=14/44`) | the sandbox now preloads `importlib.machinery, importlib.util, json, os, pkgutil, runpy, sys` before the path reset, exactly as the round-92 sandbox does; the same control then reads `7/7 fixtures scored as declared` |
| 3 | A self-test asserted through the production entry point, so its own fixture could never pass | `report()` applies the real `BASE_PINS`, so the synthetic lane read `pins=short` even with zero mismatches and the "repaired" revision could not exit 0 | the C1 selftest's own exit-code assertion | the selftest now asserts on `audit(..., base_pins=synth)` and checks `mismatches`/`short` directly; `controls/ctl-c1-selftest.txt` prints `5/5 planted findings, exit 1 on planted, exit 0 on repaired` |
| 4 | A control never wrote its own fixture | the "planted" commit was empty (`git commit` exit 1, "nothing to commit") and the battery reported `planted findings []` — the planted defect set was built but `write_all(planted)` was never called | the selftest's expected-findings assertion (an empty finding list where five were declared) | the write call was added; the same battery then reports exactly the five planted `(class, path)` pairs |
| 5 | A scratch mirror was built from a file that did not hold the whole registry, so the census gate read six rows and failed E12 | the first append attempts printed `E12 row outside Registry section` ×6, then after a whole-corpus copy `E11 missing used-by` ×18, before a validated mirror (`mirror rc: 0 E-errors: 0 W04 advisories: 37`) | `sources-census.sh validate --file <mirror>` exit 1 on the failed mirrors; the real registry was written only after a mirror exited 0 | the mirror is a full-length copy of `corpus/` with a line-count assertion (`len(mirror)==len(registry)`) before insertion; the registry write happens only after that mirror passes |
| 6 | Held rows' non-`corpus/` used-by targets were absent from the mirror, so E11 failed rows that were correct | `S088 missing used-by scripts/source_recheck.py`, `S117 missing used-by SCORECARD.md`, `.ufo/waves/round-41/…`, `.ufo/waves/round-73/contract.md` on the mirror | `sources-census.sh validate --file` E11 (exit 1 before the copy step) | the mirror copies every `mined` row's non-`corpus/` used-by target from the lane tree before validation; `copied 6` targets, then exit 0 |
| 7 | A fix committed without its consequence: `d838e744` landed ScribeC1Prose's E1/E2/E4 repairs without re-pinning the three line-bound freshness-sidecar entries, so `freshness-sweep --section=paths` exited 2 at that commit | `.ufo/waves/round-93/w1/ScribeC1Prose/sweep-sidecar-before-after.txt` (`BEFORE_pipe_exit=2`: `paths sidecar binding invalid: corpus/lessons/round-29.md:200`) | none — the C1 counter does not run the sweep, so its met=true at `d838e744` did not see the crash | the sidecar re-pin by digest match at `4f5846fe`; the sweep then exits 1 with the baseline miss (`sweep-sidecar-before-after.txt`, `AFTER` line). A repair's downstream gates are run before the commit, not after it |

Disclosure: mistakes 1–4 were found and fixed before the freeze commit; no counter, case, predicate,
label or target was changed after it. Every instrument defect the wave found is routed in the
round's report, not patched.

## Wave review and Routed

Wave `w1` (v1, 13 seats dispatched at 2026-11-04T22:26:45 per `.ufo/waves/round-93/w1.ready.dispatched`; the freeze text says 12, the dispatch file says 13 — a count drift, no predicate changed). Seats and what each filed:

- Filed a report in the wave dir (9): ScoutContract (`w1/ScoutContract.md`), ExecC2Tool (`w1/ExecC2Tool.md`), ExecC1Fixes (`w1/ExecC1Fixes.md`), ScribeC1Prose (`w1/ScribeC1Prose.md`), ScribeEntry (`w1/ScribeEntry/ScribeEntry.md`), ScribeSources (`w1/ScribeSources.md`), ReviewC2 (`w1/ReviewC2.md`), ReviewC1 (`w1/ReviewC1.md`), ConnectorScope (`w1/ConnectorScope.md`).
- No filed report (4): ScoutGround (empty directory `w1/ScoutGround/`), CriticClaims (partial receipts only, `w1/CriticClaims/` holds two scripts), MutConditional (mutation receipts, 40 mutants, copied to `w1/recovered-partial/MutConditional/`), SentinelScope (partial escape receipts, copied to `w1/recovered-partial/SentinelScope/`). No `results.json` for `w1` existed when the L1 resumed; their final-output pointers (`agent://<id>`) returned blank, a preamble, or another round's output (`agent://SentinelScope` shows round 75). These four are recorded as unsettled, not as passes.

Attack items that landed: ReviewC1 (C1 instrument falsified; six fixture routes, two live-capable), ReviewC2 (C2 candidate 162/162 on a contract-only battery; frozen positive control 160/162), MutConditional (9 of 40 reference mutants survive the frozen C2 counter), SentinelScope (partial: sandbox denies HOME, /proc and oracle reads; two escape probes returned information). Non-author spot-check of this round's gate decisions: none yet — owed to closure (LEARNING.md).

Routed (each names the defect, its evidence and the successor it binds to; none patched after scoring):

- **R93-1 (ReviewC1 F1, high, live-capable).** The documented command puts the counter's directory first on `sys.path`; a shadow `subprocess.py` there forges `ls-tree`/`show` and the frozen bytes read `met=true` at a defective revision. Successor: run from a digest-verified blob or add `-P`/`-I`; print the counter sha256 on line 1.
- **R93-2 (ReviewC1 F2, high).** A canned wrapper at the counter's path prints a frozen-format `met=true` line. No self-digest pins the counter bytes in its output; defence is procedural only.
- **R93-3 (ReviewC1 F3, high, live: 9 uncounted `Round` sections at base).** Pins are cardinality-only: a defective counted QUALITY section escapes while a junk conformant section refills `criteria=39`. Successor: pin surfaces by identity (digests or a section census).
- **R93-4 (ReviewC1 F4, high, live: 4 E4 defects at base).** Deleting a defective `## Mistakes` section clears E4 with no pin change. E4 checks only the first Mistakes table and one gap per lesson (F7). Successor: check every Mistakes section and every gap.
- **R93-5 (ReviewC1 F5/F6, medium, live: 12 SKILL rows name trees).** E3 resolves an id against any token in SOURCES.md; E5 accepts directories and empty blobs. Successor: row-level id resolution; reject trees and empty blobs.
- **R93-6 (ReviewC1 predicate-level).** A bare `## Gate`, a pointer to an empty lesson and an id-free `source:` line all satisfy the frozen C1 sentence. Successor: decide whether vacuity is in the predicate before the next wave is scored.
- **R93-7 (MutConditional, 9/40 surviving mutants of the reference).** M11 (If-Unmodified-Since with absent last_modified), M18 (lowercase `w/` accepted), M19 (empty opaque-tag refused), M24 (negative integer date accepted), M28 (last_modified with exists=false), M29 (If-Unmodified-Since malformed under If-Match), M32 (extra key in `current`), M37 (method compared case-insensitively), M40 (HTAB around list members). The frozen population has no case for these classes, so the frozen counter cannot falsify a candidate that has them. The candidate's own behaviour on these classes is not measured by the frozen counter; it is the successor's to pin. Successor: one case per class (R92-4 class).
- **R93-8 (ReviewC2 F3).** The frozen positive control `frozen/pos-good.py` refuses a legal quoted-comma opaque-tag and crashes on non-UTF-8 stdin (160/162 on ReviewC2's battery), though the freeze declared it contract-faithful. The frozen population has neither case class. Not patched after scoring; successor adds both.
- **R93-9 (ScoutContract, 18 ambiguities; 2 material refusal divergences from normative RFC text).** RFC 9110 §5.6.1.2 requires accepting empty list elements (clause 4 refuses them); RFC 9110 §8.8.3 etagc admits obs-text (clause 3 refuses). The §13.2 CONNECT/OPTIONS/TRACE method filter is absent from the contract. The candidate conforms to contract v1, not to these RFC points; the knowledge entry says so. Successor: contract v2 decides each point.
- **R93-10 (ReviewC2 C-OBS-1..3).** Contract v1 is silent on `role: null`, on duplicate JSON keys and on the scope of clause 3 for `current.etag`. Successor: a clause for each.
- **R93-11 (ScribeEntry F93-1 / ExecC2Tool RC2-1).** The counter's sandbox import allowlist omits `__future__`: a conforming candidate with `from __future__ import annotations` reads `hand=14/44` and every case is reported as a contract disagreement, not as a sandbox refusal. Successor: allow `__future__` or give sandbox refusals their own finding id.
- **R93-12 (ExecC1Fixes F1/F2).** The frozen E5 has no annotation-skip: a bare backticked path beside an absence annotation still fails. The absent paths were moved inside `[r93-absence …]` spans, which PATH_RE cannot match. The E3 prefix lines are untagged inserts that `append_guard.py` would flag against a pre-r93 base; registered here as a known exception.
- **R93-13 (ConnectorScope).** No sibling-lane overlap for the seven C2 terms across 20 lanes (19 non-HTTP false positives, 1 lane with related ground, named in `w1/ConnectorScope.md`); 0 within-scope duplicate URLs; census W04 advisories 31 → 37 (the six new rows re-scope `rfc9110.txt`, already held at S033/S453/S454/S455/S465/S466).
- **R93-14 (SentinelScope, partial).** Probes returned `HOME-READ DENIED`, `PROC-READ DENIED`, `import denied: c93_conditional` and `open outside the subject tree` (denials), but `sub-execv.py` returned a live pid (`EXECV-READ 27753`) and `sub-fork-exec.py` listed the counter's own path through a child process. The harness sandbox is not a security boundary. Successor: state that in the counter's contract, or close the two paths.
- **R93-15 (CriticClaims, partial).** `attack-c1-minimalrepair` reads `met=true, mismatches=0` at `6fcb5d7` (the predicate is satisfiable by repair alone, as designed); `attack-c2-candoverride` and `attack-c2-gen0` read `met=true` on frozen bytes with `generated=0/0`. Receipts copied to `w1/recovered-partial/CriticClaims/`; the 0/0 generated population is recorded as a successor check, not as a C2 defect.

Discernment (for the closure's spot-check): the round's C1 admit rests on a predicate ReviewC1 falsified as a counter; the C2 admit rests on a counter whose population misses nine reference mutants. Both admits are recorded with those limits, not as clean passes.

Assimilation: none. `merge/kake/SOURCES.append.md` still collides with the registry on eight ids (`.ufo/waves/round-93/assimilation/collisions`; 129 staged ids from S287, registry 207 → 213 rows). No package row was appended; S471–S476 are fresh primary-source rows opened this round, not staged rows.
considerthese: `considerthese/2026-11-05.md` is operator-authored and mined read-only; no proposal was implemented this round (at most one is allowed; none was taken). The file's Part 2 proposal 3 (a held-out vs frozen divergence column) is the successor to R93-7/R93-8 and is named here rather than implemented.
