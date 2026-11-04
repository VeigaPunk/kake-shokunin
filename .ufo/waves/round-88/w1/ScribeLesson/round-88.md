# Round 88 — three routed r87 defects and a conservative Vary-match reader

Seat: `ScribeLesson` (scribe, leaf member — no subagent dispatch). Lane root
`/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE). Draft candidate for the lane's
round lesson; L1 integrates. Nothing in this file is an outside admission.

Base commit `f4479c14813037ad993a49a3dee4028763470f7a`. Freeze named in the seat
brief: **v2** `8063739791e21a8d7966fd968913e552e1433881`. LANE HEAD when this seat
finished: **v3** `52e41d2d0ea6f5a7eaf8b5ac09ab0d78c538d644` ("freeze amendment v3 —
validation precedes the wildcard rule", committed 2026-11-04 15:58:05 -0300, six
minutes after the wave was dispatched at 15:52:15). Every C2 number below is pinned
to a counter sha256; the v2/v3 delta is measured in §Limits.

## Gate

Sources personally opened this round (single unauthenticated GET each, no cookies,
no credentials, no session values sent, nothing published):

| URL | HTTP | bytes | sha256 | accessed (UTC) |
|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 200 | 84 477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 2026-11-04T18:56:05Z |
| `https://www.rfc-editor.org/rfc/rfc9110.txt` | 200 | 502 941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 2026-11-04T19:01:34Z |

Both retained under `w1/ScribeLesson/receipts/` with their response headers. The
RFC 9111 body is byte-identical to the lane's round-87 retained copy
(`.ufo/waves/round-87/w1/ScribeLesson/receipts/rfc9111.txt`, same sha256); the
RFC 9110 body is byte-identical to the lane's round-81/82 retained copies. A
`set-cookie` header came back from the CDN and was **not** resent; no request in
this seat carried a cookie, an Authorization header or a query token.

| Candidate | Decision | URL, access date, exact located quote (≤25 words) | Reason and flip |
|---|---|---|---|
| RFC 9111 §4.1 match rule as the ground of the new Vary-match knowledge row | **admit**, tier A, scope-limited | `https://www.rfc-editor.org/rfc/rfc9111.txt`, 2026-11-04, §4.1 ¶1, txt lines 528–534: “the cache MUST NOT use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match” (24 words) | This is the sentence the reader implements, and it is the only place the *match* half is written down. It supports the field-match scope alone: cache-key construction, storage, revalidation, freshness and serving stay out. Flip: a §4.1 rewrite, or a reader that starts deciding reuse, storage or freshness — then the scope must be re-derived, not widened. |
| RFC 9110 §12.5.5 `Vary` grammar as the member-shape ground | **admit**, tier A | `https://www.rfc-editor.org/rfc/rfc9110.txt`, 2026-11-04, §12.5.5, txt line 5675: “Vary = #( "*" / field-name )” (7 words) | Gives the member alphabet the parser implements (`field-name`, or the wildcard `*`) and the list syntax that makes `*` a *member* rather than a value. Supports the member-shape claim only; the reader's field-name token set is the RFC 9110 `token` production, not this line. Flip: if a later RFC changes the `Vary` ABNF, or if the reader starts accepting members outside `field-name`. |
| “the C2 counter's 220-case pass shows the reader implements RFC 9111 §4.1” | **reject** (proposition) | same RFC 9111 §4.1, txt lines 528–534, the quote above, read as the *precondition* sentence: it makes matching a **condition** on reuse, not a rule about what the reader is | The sentence is a permission-shaped precondition; it does not decide case-normalisation, ordering or OWS handling, and the contract's conservative profile deliberately declines the third permitted transformation, so a `mismatch` may be stricter than the RFC allows. Flip: a *separately bounded* procedure that applies the field-specific normalisation for the fields it names, with its own cases — then the claim can be restated against that narrower target. |
| “an empty `Vary` value must be refused” as an RFC requirement | **reject** (proposition) | `https://www.rfc-editor.org/rfc/rfc9110.txt`, 2026-11-04, §5.6.1.2, txt lines 1695–1697: “A recipient MUST parse and ignore a reasonable number of empty list elements” (13 words) | The RFC tells a recipient to *parse and ignore* empty list elements; a zero-member list is not a field-name member, so nothing is nominated and nothing can mismatch. The frozen case 14 therefore rests on a **local adapter** convention, not on RFC 9111 §4.1 — the case's own `basis` says so. Flip: an explicit RFC sentence requiring refusal of an empty list, or a reader that adopts and *declares* the adapter convention in `contract.md` rather than leaving it in the case file. |

Registry delta: the round's RFC 9111 §4.1 row is **not yet integrated** — the lane
registry still ends at **S462** (`grep -c 'S463' corpus/SOURCES.md` → 0), and the
row candidate `S463` lives in a peer seat's wave file, not in `corpus/SOURCES.md`.
Existing rows' status/recheck/used-by are unchanged; this seat changed no registry
row. `merge/kake` still collides on eight ids (S312, S329, S367, S372, S373, S374,
S390, S409 — re-derived by a peer seat and consistent with the contract's
`Assimilation: none`); S463 is not among them. Frontier advances only the
supplied-header-map field-match half of §4.1; cache-key construction, storage,
revalidation, freshness, serving and browser behaviour remain open.

## Mistakes

One mistake, mined from an earlier round, with the fix and the witness that
reddens it.

| Class | Evidence pointer | Captured-by criterion | Fix | Fix can fail — the witness that reddens it |
|---|---|---|---|---|
| Weak exact-type / equality-only predicate: a counter that compares a candidate's output with `==` accepts a value of the wrong type, because `20.0 == 20` in Python, and a counter that trusts the *candidate's own* green banner certifies nothing | `corpus/lessons/round-87.md` §Mistakes row “Weak exact-type predicate”, evidence `round87 w1/ReviewAge/predicate-results.json` and `CriticClaims/probe.json`; the same defect class reappears in the **round-88** C1 counter at `.ufo/waves/round-88/c88_defect_queue.py:111` (`if obj != VALID_OUT:` — equality, no `type(...) is int`) and `:124` (`'selftest' not in p.stdout.lower()` — a printed string, self-attested) | r86 QUALITY measurement-downstream criterion + outside closure; r87 ReviewAge + CriticClaims, before production integration; r87 disclosed it as “counter defect remains disclosed” | The r88 C1 counter was supposed to close the r87 defect and instead re-instantiates it: `item_d2` compares the six terms with `!=` against a dict of ints, so a tool that emits `20.0` passes, and its “the tool's own `--selftest` stays green” conjunct is satisfied by a tool that prints `selftest: 61 isolated CLI fixtures passed` and runs nothing | **Reddens today, measured by this seat.** Three mirror trees built from the counter's own `mirror_tree()` green fixture, scored with `python3 -B LANE/.ufo/waves/round-88/c88_defect_queue.py --mirror <tree> --work <scratch>` — all three score `open=0 closed=3 met=true`, exit 0: (a) the six terms emitted as **floats** `20.0 …`, with the tool's own type assertion relaxed to accept them → the tool's own `--selftest` still prints `selftest: 61 isolated CLI fixtures passed`, exit 0; (b) the tool's arithmetic replaced by a **hardcoded table** for the one probed payload, and its `--selftest` replaced by a single printed banner with **no fixture run** → the counter's selftest conjunct is satisfied by that banner, and a second valid payload (`age_value` omitted) returns `invalid_input: unsupported input`; (c) the arithmetic left intact and only the `--selftest` replaced by the printed banner → `open=0 closed=3 met=true`. A type-strict comparison alone kills (a) and (b) but not (c): the selftest conjunct must be replaced by evidence the counter computes itself (its own expected values for ≥2 payloads), not by a banner the candidate prints. Receipts: `w1/ScribeLesson/receipts/scribe-probes.json` (P3, P4, P5), `w1/ScribeLesson/receipts/p3-p5-tool-detail.txt`; probe source `w1/ScribeLesson/probes/round88-scribe-probes.py`. |

## Claims and what this seat measured

The two round claims, as frozen, with this seat's own readings.

**C1 — calibration (lowest owned axis, 2 HOLD): three routed r87 defects, decided
over committed bytes.** Items D1 ledger-companion, D2 diagnostic-type, D3
recheck-path; predicate `open=0 closed=3 met=true`, exit 0 at the carrier.

- Base `f4479c14`, re-run by this seat: `open=3 closed=0 met=false`, exit 1, and the
  three detail strings are byte-identical to the committed `controls/base-c1.txt`
  (receipt `base-c1-rerun.txt`). Base tool: float input
  `{"date_value":7.0,…}` → `invalid_input: date_value must be an integer, not
  boolean`, exit 1 — the r87 routed R2 defect reproduced from the frozen copy.
- Counter selftest re-run: **11/11**, exit 0 (`c1-selftest.txt`).
- The counter reads only lane bytes: a copy of the wave directory with
  `vary-cases.json` deleted still passes the C1 selftest 11/11 exit 0
  (`c1-selftest-without-c2-fixture.txt`) — the r87 “eager unrelated fixture load”
  defect does **not** recur in the r88 C1 counter.
- D2 and D3 are textual apart from the D2 diagnostic check and the sha256 binding;
  the non-author closure remains the catch for D1/D3. This seat's own probes show
  the D2/D3 predicates are weaker than their wording (see below).

**C2 — freshness (10 HOLD): a conservative Vary-match reader over 20 frozen + 200
seeded cases.** Predicate `frozen=20/20 random=200/200 met=true`, exit 0, with
`frozen cases_sha256` and `random_sha256` printed in every receipt.

- Base `f4479c14`: tool absent, `frozen=0/20 random=0/200 met=false`, exit 1
  (receipt `base-c2-rerun.txt`).
- Counter selftest re-run: **17/17**, exit 0 (`c2-selftest.txt`); the v3 numbers
  are `match=67 mismatch=109 invalid=24`.
- L1's committed candidate `w1/L1/vary_match.py` (sha256 `2da573d3…`) scored by
  this seat against the v3 counter: `frozen=20/20 random=200/200 met=true`, exit 0
  (`l1-candidate-c2-score.txt`). **Pending receipt:** the candidate lives in the
  wave directory, not at `scripts/vary_match.py`; the carrier measurement at the
  integrated revision is L1's to take, and no such receipt exists yet.
- The C2 reference's branch coverage over the 220-case population, measured by
  this seat: 0 disagreements with the reference, but **three branches are never
  exercised** — a non-token header-map key (`nontoken_key`), an ambiguous
  case-variant duplicate name (`dup_key_in_side`) and a non-dict request map
  (`side_not_dict`). Two mutants that change declared behaviour therefore still
  score `20/20 + 200/200 met=true`: merging duplicate names instead of refusing
  them, and accepting non-token header-map keys instead of refusing them
  (`P11_c2_mutants`). A third mutant — refusing to trim OWS around `Vary` members —
  is killed (`16/20 + 110/200`), so that clause is pinned.

## Limits

- **The freeze moved under this wave.** The seat brief names freeze v2
  `80637397`; HEAD is v3 `52e41d2d`. Measured by this seat (`P1_v2_v3`): the 200
  generated inputs are identical between the two revisions and the frozen 20 are
  byte-identical, but **three seeded labels flip** — `r53`, `r150`, `r193`, all
  `mismatch` → `invalid` — and the population digest moves
  `004a8eb75b95…` → `52714a5f4ae9…`. The C2 counter's own docstring says the
  generated batch “cannot drift from the hand-labelled one”, and this seat's
  measurement is that the *labels* moved while the *inputs* did not. The v3
  commit's sentence “No item, case, threshold, control or target moved” is
  accurate about the 20-case set and the C1 items and inaccurate about the
  200-case labels and the constant-stub control scores. Any C2 receipt must be
  pinned by counter sha256.
- **The C2 counter is satisfiable without the capability.** Two false greens
  measured by this seat: a stub that imports the committed counter's own
  `reference()` and prints its verdict scores `20/20 + 200/200 met=true`, exit 0
  (`P10`); and the contract's sentence “a lookup table keyed on known inputs
  cannot pass it” is defeated by a table over the *committed* seed, because the
  generator and the seed are committed bytes. The v3 counter therefore measures
  agreement with a published oracle, not implementation of the profile. This is
  a defect in the round's own counter, not in any candidate.
- **The C1 counter's D2/D3 predicates are weaker than their wording**, measured by
  this seat: D2 accepts float-valued terms and a candidate-printed selftest banner
  and a hardcoded lookup table (`P3`, `P4`, `P5`); D3 accepts a CRLF rewrite of
  every base line (the history check compares `splitlines()`, which drops `\r`) and
  accepts `recheck: 5` as a cadence (`P6`, `P8`); D1 accepts a `source:` line
  naming a non-existent look-alike path because the ledger path is matched as a
  substring (`P7`). D3 is also **over-strict** in one direction: a pure insertion
  immediately after the `recheck:` line — which the contract permits — is reported
  as `history-preservation violation at base line 3 (replace)`, exit 1 (`P9`).
- The C2 reference's `is_token` accepts a **trailing LF** (`TOKEN` ends in `$`,
  which matches before a final newline): `is_token('accept-encoding\n')` is
  `True`, so `Vary: "*\n"` is read as the wildcard member and the reference
  answers `match` for `{"vary":"*\n", …}` where the wildcard rule requires
  `mismatch`. No frozen or random case contains an LF (0 of 220), so this cannot
  move a score today; it is a live soundness hole in the frozen oracle and in the
  committed candidate that copies the same regex. Measured by this seat; a peer
  seat reports the same defect independently.
- This seat changed **no production byte**: no `scripts/`, `corpus/`, `SKILL.md`,
  `LOG.md` or `SCORECARD.md` edit, no commit, no push, no mutating git/jj command,
  no write outside `w1/ScribeLesson/` and this seat's own scratch. No tool was
  installed or upgraded (Python 3.14.8 already present; PACMAN untouched).
- This seat scored no carrier revision: the production files
  `scripts/vary_match.py`, `corpus/knowledge/vary-matching.md` and
  `corpus/knowledge/gate-agreement-metadata.md` are **absent at HEAD**; the
  candidates live in peer wave directories. Carrier measurement, the S463 registry
  row and the integrated lesson are L1's, and no receipt for them exists yet.
- Nothing here asserts cache-key construction, storage, revalidation, freshness,
  serving or browser behaviour; no live surface was contacted by this seat beyond
  the two RFC documents named above.

## Reviews

Peers' wave reports read by this seat, with what was corroborated independently
and what was not:

| Peer report | Its headline | This seat's independent measurement |
|---|---|---|
| `ExecReader.md` | The v3 amendment landed after a seat had scored; the v2 receipt is no longer re-derivable | **Corroborated and extended.** `P1_v2_v3` re-derives the same three label flips (`r53`, `r150`, `r193`) from the two committed counter versions, and this seat adds that the **L1 candidate scores 197/200 under the v2 oracle and 200/200 under v3** — the amendment is load-bearing for the candidate shipped in the same commit. |
| `ReviewCounter.md` | C1 counter false greens: hardcoded output table, float terms + stub selftest, `.bak` look-alike path, CRLF rewrite, `0d`/ISO cadence, plus a D3 false red on a permitted insertion | **Corroborated.** `P3`–`P9` reproduce the float-terms, stub-selftest, hardcoded-table, `.bak`, CRLF, `recheck: 5` and insertion-adjacent-to-recheck shapes with the same outcomes (`met=true` for the false greens, exit 1 for the false red). This seat's `recheck: 5` case is the bare-number form of the peer's `0d`/ISO variants. |
| `CriticClaims.md` | A lookup table over the committed seed passes 220/200; an oracle-import stub passes 220/200; empty-list reading drifts 2/200; the C1 junk control cannot distinguish correct from false prose | **Corroborated in part.** `P10` reproduces the oracle-import false green (met=true, exit 0). This seat did **not** rebuild the 216-entry table, and does not restate the peer's number; the independent claim here is narrower: the contract's anti-lookup sentence is defeated by the committed seed, and the *oracle* is importable at scoring time. |
| `MutReader.md` | 15/21 C2 mutants killed, 6 survived; the survivors are exactly the zero-coverage classes (internal whitespace run, duplicate key, empty-as-absent, list element type, non-ASCII token) | **Corroborated in part.** This seat did not run that sweep. Its own two C2 mutants that change declared behaviour — merging duplicate names and accepting non-token keys — both score `20/20 + 200/200 met=true`, which is the same zero-coverage class the peer reports as `dup_case_key` and `nonascii`. |
| `ReviewReader.md` | The trailing-LF token is accepted, so `Vary: "*\n"` returns `match`; a spec-faithful reader that follows RFC 9110 §5.6.1.2 scores 19/20 + 187/200 | **Corroborated.** This seat measured `is_token('accept-encoding\n') == True` and `reference('*\n', …) == 'match'` directly against the committed counter, and confirmed 0 of 220 cases contain an LF or CR. This seat's Gate reject row on empty `Vary` quotes the same §5.6.1.2 sentence. |
| `ExecCases.md` | The contract never enumerates the refusal rules; 24/200 random labels and 4/20 frozen labels are refusals; a strictly spec-conformant reader is unreachable by the frozen metric | **Corroborated in part.** This seat's Gate reject row rests on the same §5.6.1.2 sentence; this seat did not rebuild the trigger census. |
| `ScribeLedger.md`, `ScribeVary.md`, `ConnectorScope.md`, `ExecDefects.md`, `ExecTrial.md`, `ScoutSpec.md` | D1 digest placement, D3 ISO-date cadence, the eight-id `merge/kake` collision, the one-line D2 repair, one live GET to ds4cc.com, the primary-source quote set | **Not re-run by this seat.** Their drafts are the candidates L1 integrates; this seat read the reports and used the RFC 9111 §4.1 / RFC 9110 §5.2 / §5.3 / §5.6.1.2 / §12.5.5 texts it fetched itself. |

No WAVE-DONE claim is made here, no peer report was edited, and no peer artefact
was copied into this seat's directory.

## Census before and after

Command (run from the fleet root, read-only; writes only stdout):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
```

**Before** (2026-11-04, first run of this seat; full output in
`w1/ScribeLesson/receipts/census-before.txt`): 24 `W04` lines (S033, S088, S092,
S098, S099, S102, S110, S111, S115, S116, S117, S127, S416, S417, S427, S433, S445,
S450, S451, S453, S454, S455, S461, S462 — the same-URL-across-scopes warning class),
then `kake ok /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`;
**exit 0**.

**After** (re-run at the end of this seat; full output in
`w1/ScribeLesson/receipts/census-after.txt`): byte-identical to the before output
apart from the trailer line; **exit 0**. Same 24 `W04` lines, same `ok` line.

Expected and not yet observed: when L1 lands the `S463` row and the two knowledge
entries, the `W04` count should rise by one (the row's URL
`httpwg.org/specs/rfc9111.html` is already used by S461 and S462, and the census
normaliser strips the `#…` anchor, so it is the same URL key in a third scope) and
the row's `used-by` path `corpus/knowledge/vary-matching.md` must exist on disk or
`E11` fires. Neither is observed yet: the registry still ends at S462 and
`corpus/knowledge/vary-matching.md` is absent at HEAD. This seat's after-run is
therefore the *pre-integration* census; the post-integration census is L1's to
take and no receipt for it exists yet.

## Artefacts

All inside `w1/ScribeLesson/`:

| path | contents |
|---|---|
| `round-88.md` | this lesson draft |
| `receipts/census-before.txt`, `receipts/census-after.txt` | the two census runs, full stdout + exit |
| `receipts/rfc9111.txt`, `receipts/rfc9111.headers` | RFC 9111 body + response headers (200, 84 477 B, sha256 `aeb52adb…`) |
| `receipts/rfc9110.txt`, `receipts/rfc9110.headers` | RFC 9110 body + response headers (200, 502 941 B, sha256 `21c1cdce…`) |
| `receipts/c1-selftest.txt`, `receipts/c2-selftest.txt` | counter selftests re-run (11/11, 17/17) |
| `receipts/c1-selftest-without-c2-fixture.txt` | C1 selftest with the C2 case file deleted — 11/11, exit 0 |
| `receipts/base-c1-rerun.txt`, `receipts/base-c2-rerun.txt` | both counters at base `f4479c14` (exit 1 each) |
| `receipts/l1-candidate-c2-score.txt` | L1's committed candidate scored 20/20 + 200/200 by the v3 counter, exit 0 |
| `receipts/scribe-probes.json` | P1–P11 probe output (JSON, deterministic) |
| `receipts/p3-p5-tool-detail.txt` | what the P3/P4/P5 candidates' own `--selftest` actually did, and their second-payload behaviour |
| `receipts/commands.txt` | every command with its exit code |
| `probes/round88-scribe-probes.py` | the single reproducible probe script (P1–P11) |
| `probes/branch-coverage.py`, `probes/v2-v3-label-diff.py`, `probes/mutant-*.py`, `probes/stub-delegate-to-committed-oracle.py` | the individual probe sources |
