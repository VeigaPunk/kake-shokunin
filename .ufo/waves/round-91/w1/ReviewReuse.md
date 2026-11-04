# ReviewReuse — clause-by-clause review of the round-91 C2 contract, counter and tool

VERDICT: C2 instrument review clean — 0 disagreements in 53 independent hand-computed
cases against `scripts/stored_reuse.py` (protocol exact), 0 uncovered numbered clauses
except clause 3 (fully uncovered by the frozen battery; the tool nevertheless implements
it), 4 contract ambiguities documented; the candidate is conforming but **uncommitted**,
so the counter still reads `candidate=absent met=false` at HEAD.

Measured at HEAD `f4fff130a52ae6de49af5de7d568d2ee320ebfb0`, 2026-11-04. Frozen bytes
verified before any run: `c91_reuse.py` `0cd61042…1ab660`, `c2-contract.md`
`faa91e09…768fe4`, `frozen/c2-population.sha256` `033b6103…5084c8` — all three equal to
the digests named in `freeze.md`. Counter `--selftest` → `selftest 45/45 hand cases,
120 generated, 7 decisions`, exit 0 (reference matches every worked case; no
oracle/case drift).

Artifacts (this directory): `driver_rr.py` (my case driver), `subject-run.txt`
(candidate run), `reference-run.txt` (reference run), `counter-at-head.txt`,
`counter-candidate-fixture.txt`. Scratch deleted after copying; receipts below are the
copied files.

## 1. Clause 1–21 coverage in `c91_reuse.py`'s hand cases

All 45 hand cases named by their counter names. 36 decided + 9 refusals.

| Cl. | Deciding hand case(s) | Coverage |
|---|---|---|
| 1 names case-insensitive, case-variant dup refusal | `refuse-duplicate-header-name` | PARTIAL — refusal half only; no case reads a sole non-canonical-case header (e.g. `CACHE-CONTROL`) as the directive source |
| 2 value trim/byte-exact, CR/LF/NUL refusal | `refuse-cr-value` | PARTIAL — LF refusal, NUL refusal (R90-2's resolved point) and trimming (`" max-age=60 "`) have no case |
| 3 header name/value must be strings | — | **UNCOVERED — no case**. (In JSON the name half is grammar-vacuous; the value half, e.g. `"X-Note": 5`, is testable and absent) |
| 4 Cache-Control parse: quoted delta, dup diff args, unknown ignored | `refuse-quoted-delta`, `refuse-duplicate-directive`, `unknown-directive-ignored` | PARTIAL — empty directive (`` `max-age=60,` `` or empty value), empty name (`=60`), same-name-same-arg (must NOT refuse), lowercased-name positive (`MAX-AGE=60`), OWS around `=` all untested |
| 5 Date required integer | `refuse-missing-date` | PARTIAL — non-integer Date (`abc`) untested |
| 6 Age optional non-negative | `refuse-negative-age` | PARTIAL — non-integer Age untested |
| 7 Expires optional integer, may precede Date | `expires-negative` | PARTIAL — non-integer Expires untested |
| 8 current_age = max(0,Age)+max(0,now−Date) | `age-header`, `age-future-date` | covered |
| 9 lifetime order s-maxage/max-age/Expires/null | `s-maxage-shared`, `s-maxage-ignored-private`, `max-age-beats-expires`, `expires-lifetime`, `expires-negative`, `no-lifetime` | covered; gap: `s-maxage` alone, not shared → falls to null (untested) |
| 10 not-storable six disjuncts | `not-storable-method`, `not-storable-status`, `not-storable-no-store`, `not-storable-request-no-store`, `not-storable-private-shared`, `not-storable-vary-star`; negatives `private-private`, `vary-named`, `head-method`; ordering `only-if-cached-not-storable` | covered; gap: `*` as a list member (`Vary: Accept, *`) — only bare `*` tested |
| 11 lifetime null → heuristic-undecided | `no-lifetime` | PARTIAL — ordering vs clauses 12–15 (null lifetime + a directive present) untested |
| 12 request no-cache → revalidate | `request-no-cache` | covered |
| 13 stored no-cache → revalidate | `stored-no-cache` | covered |
| 14 request max-age, current_age > N | `request-max-age`, `request-max-age-equal` (== boundary) | covered |
| 15 min-fresh, lifetime − age < N | `min-fresh-short`, `min-fresh-exact` (== boundary) | covered |
| 16 fresh reuse | `fresh-max-age` (+ several negatives) | covered |
| 17 must-revalidate / proxy-revalidate while shared | `must-revalidate-stale`, `proxy-revalidate-shared`; negatives `proxy-revalidate-private`, `must-revalidate-fresh` | covered |
| 18 max-stale (no arg = any; ≤ N) | `stale-max-stale-ok`, `stale-max-stale-too-old`, `max-stale-unbounded` | covered; equality boundary (excess == N) untested (5≤10 and 11>10 only) |
| 19 revalidate otherwise | `stale-boundary` (age == lifetime) | covered |
| 20 only-if-cached conversion | `only-if-cached-stale`, negatives `only-if-cached-fresh`, `only-if-cached-not-storable` | PARTIAL — the middle conversions (`serve-stale`→miss, `heuristic-undecided`→miss) untested; a candidate converting only `revalidate` would pass the battery |
| 21 lifetime/age reported unless not-storable | implicit in every decided case's lifetime/ageout; nulls via `no-lifetime` | covered |

Uncovered list (clauses with no hand case at all): **clause 3 only.** Partially
covered halves listed above: 1, 2, 4, 5, 6, 7, 10, 11, 18, 20. Input-schema gaps
(Input section, not numbered): missing `stored`/`request`/`now`; `shared` non-bool;
`shared` absent (default false — never absent in hand or generated cases); status out
of 100..599 (99/600 → refusal, not not-storable); `request.headers` absent;
`stored.headers` absent.

## 2. My 53 inputs from contract text alone

Driver: `driver_rr.py` — expectations are literals hand-derived from the contract
before any run, never from the reference. Mode `--subject` runs the candidate as the
counter would (subprocess, fresh cwd, one JSON on stdin). Mode `--reference` runs the
counter's `reference()` in-process.

Commands and results (all under my scratch, receipts copied here):

- `python3 -B driver_rr.py --mode subject --subject LANE/scripts/stored_reuse.py --work <scratch>`
  → `SUMMARY subject agree=53 disagree=0 protocol_notes=0 of 53`, exit **0**
  (`subject-run.txt`).
- Same cases against the frozen counter's `reference()` →
  `SUMMARY reference agree=50 disagree=0 of 50`, exit 0 (`reference-run.txt`;
  run before the clause-3 cases were added).

Named cases from my item, candidate results (all as hand-computed):

| Input | Hand expectation | Candidate |
|---|---|---|
| OWS around `=`: `max-age = 60` | AMBIG — strict-token reading `heuristic-undecided` (untrimmed name `max-age ` is an unknown directive); lenient reading `reuse` | `reuse 60/30` — lenient, same as reference (see F8) |
| `no-cache="field"` (request) | revalidate 60/30 (clause 12 presence check) | agree |
| empty Cache-Control value `""` | AMBIG — split semantics make one empty directive → refusal | refusal `empty directive` (see F12) |
| `max-stale="10"` | refusal (quoted delta, clause 4) | refusal `quoted delta-seconds argument: max-stale` |
| `Age: 007` | reuse 60/17 | agree |
| `Date` far future (2000000, now 1000000) | reuse 60/0 | agree |
| `Expires` == `Date` | lifetime 0 → revalidate 0/0 | agree |
| `Vary: Accept,` (empty member) | reuse 60/30 (empty member is not `*`; not a refusal) | agree |
| HEAD with directive (`no-cache`; `no-store`) | revalidate 60/30; not-storable | agree both (see note on "body-only": no HTTP directive is body-only; I read the intent as "HEAD must not bypass directives") |
| `s-maxage` without `max-age`, not shared | heuristic-undecided null/50 | agree |
| `s-maxage` without `max-age`, shared | reuse 100/50 | agree |
| `private="field"` while shared | not-storable | agree |
| two directives, same name, same argument (`max-age=60, max-age=60`) | NOT a refusal → reuse 60/30 | agree |
| case-variant directive duplicate (`max-age=60, MAX-AGE=30`) | refusal | agree |
| signed delta (`max-age=+60`, `max-age=-0`) | refusal | agree both |
| uppercase directive (`MAX-AGE=60`) | reuse 60/30 | agree |
| tab-padded value | reuse 60/30 | agree |
| nameless directive (`=60`) | AMBIG → refusal | refusal `empty directive name` |
| quoted arg containing comma (`private="a, b"`, shared) | split-inside-quotes → private present → not-storable | agree |
| request `max-age=30`, age 31 / `max-age=0` boundary | revalidate 60/31; reuse 60/0 | agree both |
| clause order: `max-stale=100, min-fresh=10` stale | clause 15 before 18 → revalidate 60/65 | agree |
| `only-if-cached` + serve-stale | only-if-cached-miss 60/65 | agree |
| `only-if-cached` + heuristic-undecided | only-if-cached-miss null/10 | agree |
| `min-fresh` with null lifetime | clause 11 first → heuristic-undecided null/10 | agree |
| negative lifetime + bare `max-stale` | serve-stale −100/0 | agree |
| `head` lowercase / `GET ` with trailing space | not-storable | agree both |
| `now: 0`, `Date: 0` | reuse 60/0 | agree |
| `request.headers` absent | reuse 60/30 | agree |
| `shared` absent (default), with and without `s-maxage` | reuse 60/30; heuristic-undecided null/50 (default false actually taken, not just accepted) | agree both |
| LF / NUL in a value | refusal | agree both |
| status 99 / 600 | refusal (input spec 100..599), **not** not-storable | agree both |
| `shared: "true"` | refusal | agree |
| missing `stored` / `stored.headers` absent | refusal | agree both |
| extra key inside `stored` | AMBIG → refusal | refusal `unknown stored/request key` |
| `Date: abc` / `Date: " 1000000 "` | refusal; reuse 60/30 | agree both |
| `min-fresh="20"` / `s-maxage="100"` | refusal | agree both |
| unknown directive with quoted arg ignored | reuse 60/30 | agree |
| clause 3 value half: `"X-Note": 5 / true / null` | refusal | refusal `header names and values must be strings` — all three |

**Zero disagreements.** The four AMBIG inputs are the honest statement of what the
contract text leaves open; on all four the candidate takes the same posture as the
counter's reference, so the battery cannot distinguish the two readings (F8/F12).

## 3. Output protocol (exact)

My driver checks, per case, stricter than the counter: refusal → exit **exactly 1**,
stdout **raw-empty** (the counter accepts whitespace-only), stderr starts with
`invalid_input:` (plus a note when the reason is empty — never was); success → exit
exactly 0, stdout parses as one JSON object, key set **exactly**
`{decision, freshness_lifetime, current_age}` (an absent key fails the set check — null
must be literal `null`, and `smaxage-only-not-shared`/`only-if-cached-heuristic`
confirm it is), `freshness_lifetime`/`current_age` must be `int` or `None`, never
`bool` (type check on all 36 decided cases), decision ∈ vocabulary. The candidate
passed every case under these strict checks. Exit codes: my runs' `exit=0` receipts
above; refusal exits recorded per line in `subject-run.txt`.

Counter-side leniencies vs the contract (frozen bytes → findings, not edits):

- F-P1 `c91_reuse.py` `run_one`: `if out.strip(): return False, "refusal wrote stdout"`
  — a whitespace-only stdout passes, contract says "nothing on stdout".
- F-P2 the refusal check requires only the `invalid_input:` prefix; the contract's
  `invalid_input: <reason>` allows an empty reason. Minor.

Counter-side exactness that does match the contract: three-key set equality,
`type(got[k]) is not type(expected[k])` (bool≠int caught), refusal exit must be exactly
1, success exactly 0, `json.loads` rejects two concatenated objects.

## 4. Contract honesty

RFC-grounded (checked against `.ufo/waves/round-91/L1/src/rfc9111.txt`, the retained
84 477 B body): clause 9's first-match order (§4.2.1, verbatim bullet order); the
clause 10 disjuncts no-store/private-while-shared/Vary:\* (§3, §5.2.2.4/5/7);
clauses 12–15 (§5.2.1.1/3/4 request directives); 17 (§5.2.2.2/§5.2.2.8, with the
`must-revalidate-fail` vocabulary honestly mapping §5.2.2.2's 504 consequence);
18 (§5.2.1.2 both argument forms); 20 (§5.2.1.7's 504); unknown directives ignored
(§5.2.3 "A cache MUST ignore unrecognized…" — I verified the MUST at line 1411);
case-insensitive token comparison and token/quoted-string arguments (§5.2, line ~1084).

Declared adapter conventions (labelled in the contract, and honestly repeated in the
tool's docstring): clause 5 Date-as-integer (no HTTP-date parsing, shared with
`cache_current_age.py`); clause 8's two-term max equation — explicitly "adapter
convention, from S462's equation set", NOT §4.2.3's six-term equation (PROVINCE r87
records the conservative-max profile); clause 11 declining heuristic freshness (§4.2.2
named in Scope); serve-stale-without-directive and revalidation exchanges out of scope.

Undeclared choices a reader would take as RFC-normative:

- F6 Status whitelist: the 12 codes (incl. 308) are the RFC 7234 §3 / RFC 9110 §15.1
  heuristically-cacheable set. RFC 9111 (2022) §3 has **no fixed list** ("method
  understood + final status + explicit freshness info"). Conservative and defensible,
  but unlabelled, and the freeze's sourcing sentence (§5.2.1, §4.2.1, §4.2.4) does not
  cover it.
- F7 Stricter-than-RFC refusals: quoted delta-seconds refused (§5.2 intro: "recipients
  ought to accept both forms"; only the send side MUST NOT generate) and
  duplicate-directives-with-different-args refused (§4.2.1: "either the first
  occurrence should be used or the response should be considered stale" — refusal is a
  third behavior). Both fine as adapter policy, both unlabelled.
- F8 OWS around `=`: the contract never says the name/argument are trimmed; RFC 9111
  §5.2's ABNF has no BWS, so `max-age = 60` is an unrecognized directive → ignore.
  Reference and candidate take the lenient reading and accept it as `max-age`; no hand
  or generated case pins either reading. This is the one place my hand reading and the
  instruments genuinely diverge.
- F9 HEAD storable (worked case 32): permissible under §3 ("method understood") and §2
  (key includes method), but the lane's r89 key omits the method (R90-4) — pairing this
  instrument with that key conflates GET and HEAD entries. Worth a routed line; the
  contract doesn't flag it.
- F10 `no-cache="field"` and `private="field"` treated as the full directive
  (§5.2.2.4/§5.2.2.7 make them field-scoped; request no-cache defines no argument at
  all). Conservative simplification, undeclared.
- F12 Empty Cache-Control *value* is refused via "an empty directive is a refusal" +
  split semantics (zero-directives reading would decide); nameless directive `=60`
  refused though the contract has no nameless-directive clause. Both postures are the
  reference's; the battery never tests them.

Knowledge-entry overclaim check: **unanswerable at measurement time** — the freeze
names "the RFC 9111 §5.2.1 row opened this round (S469)", but `corpus/SOURCES.md` has
no S469 row and no round-91 knowledge entry exists yet. Until they land, the freeze's
sourcing claim is unbacked on committed bytes. As a substitute I read the shipped
tool's docstring: it claims nothing beyond the contract (mirrors the scope section,
labels the Date convention, disclaims network/clock/heuristics/key-identity). Honest.

## Findings by severity

- **F1 (round-state, closes only with the L1 commit).** `scripts/stored_reuse.py`
  exists only in the working tree (untracked at HEAD `f4fff130`); the counter reads
  committed bytes → `candidate=absent … met=false`, exit 1
  (`counter-at-head.txt`). The same bytes committed in a scratch fixture
  (clone at `f4fff130` + one commit `d94295a4968993f10425e3ec1e302f05ac2c43ec`,
  toplevel asserted, throwaway identity inside the fixture only) score
  `candidate=present hand=45/45 generated=120/120 forgeries_refused=5/5
  anti_table=ok population=ok met=true`, exit 0
  (`counter-candidate-fixture.txt`, candidate sha256
  `5004657dbf2ae43399631f79e5d5955a8aa698b53f6127e22e2cc654ba9ad299`).
  C2 lands or dies with the commit of these exact bytes.
- **F2 (frozen counter).** Clause 3 decided by no hand case; e.g. `"Date": 1000000`
  (JSON number) must be refused, and any behavior scores 45/45 today. The tool
  actually refuses (`header-value-*` cases) — gap closed on the tool, open on the
  battery.
- **F3 (frozen counter).** Clause 20's middle conversions untested; a
  convert-only-`revalidate` candidate passes the battery. Tool converts correctly.
- **F4 (frozen counter).** Protocol leniencies F-P1/F-P2 above.
- **F5 (frozen counter).** Battery-uncovered halves: 1, 2, 4, 5, 6, 7, 10 (star
  member), 11 (ordering), 18 (equality boundary), plus the input-schema gaps listed in
  §1. My 53 cases cover every one; the tool agreed on all.
- **F6–F10, F12 (contract honesty, routed):** undeclared grounding/strictness choices
  in §4 above.
- **F11 (round state).** S469 and the knowledge entry absent at measurement; re-run
  the §4 overclaim check when they land.

## Residual risk and verification gaps

- The 120 generated cases are decided by the counter's own reference (oracle =
  reference), so a shared misreading inside a clause passes both; my independent
  battery is the mitigation and surfaced exactly one (F8).
- My fixture receipt measures cloned bytes at a scratch revision; the canonical
  measurement is the L1's counter run at the real carrier commit.
- I did not fuzz beyond the 53 cases + the frozen battery; no timing or resource
  stress was applied.
- No frozen file was edited; no git/jj mutation touched LANE (fixture commit only,
  toplevel asserted `toplevel-ok`); scratch deleted after copying receipts.
