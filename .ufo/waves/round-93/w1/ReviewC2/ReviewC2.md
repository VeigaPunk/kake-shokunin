# ReviewC2 — independent contract-only review of the round-93 C2 candidate

VERDICT: C2 clean on the author-declared final bytes — 162/162 cases agree
(sha256 `d3bac7de…`, deterministic across two runs). The review found 2 real
tool defects in earlier builds (one reproduced live on a mid-state digest);
both are fixed in the final bytes. The frozen positive control still shares
both defect behaviours, which is the round's load-bearing instrument finding.

## Scored surface (final)

- Target: `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/conditional_eval.py`
- **Scored digest: sha256 `d3bac7de1c2d04fc355db795aebdf6012030ea5c5793d9362bc9cd8e0b8cac5e`**,
  24 854 B, mtime 2026-11-04T22:44:13-03:00 — the author seat's declared final
  (their scratch clone commit `e26ef3ae`), verified byte-identical in the lane
  tree at scoring time; still untracked at lane HEAD `191ef8dd`
  (`master` = `191ef8dd`; freeze `bb8012fe`; base `10ecbd1a`; the file does not
  exist at the freeze revision — expected, delivered mid-wave).
- Battery executed twice against this digest: identical results (deterministic).
- Reference surface (secondary): `.ufo/waves/round-93/frozen/pos-good.py`,
  sha256 `0fe018a8e33ca82928a876f2b0d2e5b3f33befa00260f2fdf995418822a868e4`,
  run black-box only. `c93_conditional.py` (hand cases + reference), `neg-*.py`
  and `build-fixtures.py` were **never read**.

## Method

1. I read `.ufo/waves/round-93/freeze.md` and `.ufo/waves/round-93/c2-contract.md`
   and computed the entire case set from the **contract text alone** — before
   the candidate existed, before its source was read, and without reading any
   frozen counter content.
2. Double entry: every case carries a hand-derived pin; an oracle written
   directly from the contract re-derives every pin.
   `python3 -B battery.py --selfcheck` → `SELFOK oracle reproduces all 162 pins`.
3. Grading on the contract's observable contract: refusal ⇔ exit 1, empty
   stdout, stderr starting `invalid_input:`; success ⇔ exit 0 and stdout
   parsing to exactly `{"decision","precondition"}`. One subprocess per case,
   stdin JSON, cwd = scratch.
4. Harness disclosure (honesty): my first comparison had a bug — a tool refusal
   was auto-scored as agreement regardless of the pin, masking exactly the
   "false refusal of a legal input" class. Found while reconciling a source
   read against a direct probe; fixed; everything below is from the corrected
   harness (`battery.py` beside this report). The first 160/160 reading was an
   artifact of that bug and is superseded.

## Case taxonomy (162 cases; ids in `cases.json`, harness in `battery.py`)

- **71 refusals (R01–R70, E01)** — schema shape; clause 1 types (method token
  syntax incl. `"GE T"`, `"GET,"`, `"GÉT"`, `"GET\t"`, empty, non-string,
  non-ASCII; bool-vs-int, negative, float for the date fields; `etag` type);
  clause 2 (absent representation with non-null `etag`/`last_modified`);
  clause 3 (unterminated tags, lowercase `w/`, `W/ ` space, trailing junk,
  space/DEL/control/non-ASCII inside the opaque-tag); clause 4 (empty/blank
  value, empty members `,,`/trailing/leading, `*` mixed, non-OWS separators,
  `"a" "b"` without comma); clause 6 (malformed field that would never be
  evaluated, incl. under `role:"cache"`); stdin shape (array, invalid JSON,
  empty stdin, JSON null, **non-UTF-8 bytes** E01); `role` enum (`"proxy"`,
  `123`, `"Origin"`).
- **87 decisions (D01–D86, E02)** — step 8: `*` with/without representation,
  list hit/miss, **all four rows of RFC 9110 §8.8.3.2 Table 3 through
  If-Match** (strong/strong same D06; strong/strong different D07+D16; weak
  involved same opaque D10/D11/D12; weak involved different opaque E02), null
  etag, OWS/HTAB, **quoted comma D21**, case-sensitivity, empty opaque tag,
  prefix non-equality. Step 9: suppressed when `if_match` present (D22),
  equal/older/newer, null `last_modified`, boundary 0. Step 10: **all four
  Table-3 rows through If-None-Match** (D32; D36/D37/D79; D33/D34/D35/D74/D85;
  D78), `*` × GET/HEAD/POST/DELETE/PATCH/OPTIONS, lowercase `get`/`head`, `*`
  as method token, list members, case-sensitive opaque compare. Step 11:
  suppressed by `if_none_match` presence regardless of outcome (D47–D49, D66,
  D73), suppressed by non-GET/HEAD incl. lowercase (D52, D54), decided only
  when `if_none_match` absent (D50, D53, D67–D69), boundary 0, 2^62. Step 7
  cache role: `if_match`/`if_unmodified_since` skipped even when they would
  412 (D60, D62, D86), INM/IMS still decide (D61, D63, D64), malformed skipped
  field still refused (R62). Step 12: `200`/null (origin, cache, POST).
  Cross-step precedence: IM before INM (D55), IUS before INM both outcomes
  (D58, D59), IM-present suppressing IUS (D22, D57), INM-present suppressing
  IMS (D47–D49 vs D50).
- **4 exploratory (X01–X04)** — contract under-decides: clause-3 scope over
  `current.etag` (unquoted `abc` X01; obs-text `café` X02), `role: null`
  (X03), duplicate stdin keys (X04).

## Result on the final bytes (`d3bac7de…`)

**162 cases, 162 agree, 0 disagreements** (71/71 refusals, 87/87 decisions,
4/4 exploratory), identical across two runs. Spot re-pros on the same bytes:

```
printf '\xff\xfe{"method":"GET"}' | python3 -B scripts/conditional_eval.py
# → invalid_input: input is not valid JSON          (exit 1, stdout empty)
printf '%s' '{"method":"GET","current":{"exists":true,"etag":"\"a,b\"", …,"if_match":"\"a,b\"",…}}' \
  | python3 -B scripts/conditional_eval.py
# → {"decision": "200", "precondition": null}       (exit 0)
python3 -B scripts/conditional_eval.py --selftest   # → selftest 90/90, exit 0
```

No illegal input accepted; no legal input falsely refused; refusal and success
shapes match the contract exactly.

### Digest history observed during this review (all in the lane tree)

| digest (prefix) | time (mtime/probe) | my corrected battery | notes |
|---|---|---|---|
| `55e94971…` | 22:35 | (first run used the buggy harness — superseded) | initial state seen |
| `e38f8720…` | 22:37:05 | direct probe: D21 input **refused** (`invalid_input: malformed entity-tag in if_match`) | mid-state regression, never battery-scored |
| `5a3bd465…` | 22:37:10 | **160/162** — D21 false refusal + E01 crash | first stable state I scored |
| `b659029e…` | 22:43:09 | **161/162** — D21 fixed, E01 remained | author's first "final" |
| `10bf2b1e…` | (observed 22:45 probe) | E01 direct probe now refusing; not battery-scored | intermediate |
| **`d3bac7de…`** | 22:44:13→ | **162/162** | **author-declared final; scored** |

## Findings

**F1 — TOOL DEFECT in `5a3bd465…`, FIXED in `d3bac7de…` (clauses 3+4): quoted
commas inside an entity-tag were falsely refused.** Clause 3's etagc set is
"`!`" or 0x23–0x7E; comma is 0x2C, so `"a,b"` is a well-formed single
entity-tag with opaque `a,b`, and clause 4's list must separate members at
commas *between* entity-tags (the only reading consistent with clause 3). The
`5a3bd465…` bytes split members with a quote-blind `value.split(",")` (line 95
of those bytes), refusing legal `ETag: "abc,123"`-style tags in both `If-Match`
and `If-None-Match`; the `e38f8720…` mid-state had the same behaviour (live
probe transcript in the digest history). The author's fix (sequential,
quote-aware member parser) resolves it: D21 and the whole clause-4 refusal set
pass on the final bytes. Anchors: contract text; RFC 9110 §8.8.3
(`L1/src/rfc9110.txt:9871-9874`: `etagc = %x21 / %x23-7E / obs-text`).

**F2 — TOOL DEFECT in `5a3bd465…`/`b659029e…`, FIXED in `d3bac7de…`
(Input/Output): non-UTF-8 stdin crashed instead of refusing.** Input that is
not one JSON object must produce `invalid_input: <reason>` on stderr, exit 1,
nothing on stdout. Undecodable bytes died in `sys.stdin.read()` with a raw
`UnicodeDecodeError` traceback — per the lane's own QUALITY.md round-24 bar, "a
nonzero process exit accompanied by a Python traceback is a crash, not a
successful rejection." The author's fix (stdin read as bytes, undecodable
input refused) resolves it: E01 refuses cleanly on the final bytes.

**F3 — INSTRUMENT FINDING, STILL OPEN (frozen fixture): `pos-good.py` shares
both defect behaviours and therefore diverges from the contract the candidate
now implements.** The freeze declares `frozen/pos-good.py` "an independent
contract-faithful implementation". My identical battery scores it **160/162**:
it refuses the legal quoted-comma entity-tag (`invalid_input: tag`, exit 1)
and crashes on non-UTF-8 stdin — i.e. on exactly the two points where the
delivered candidate was wrong and is now right, the frozen "contract-faithful"
reference is still wrong. Consequences, for the round's routed list — not for
my scoring:
- The reference is not contract-faithful on quoted commas and stdin encoding;
  this is the R92-5 class one level up (the reference needed a contract-only
  reader before the freeze).
- The counter checks its reference against every worked hand case; since the
  reference refuses quoted-comma tags, any hand case containing one would have
  failed the reference pre-freeze — so [INFERENCE] the 44 hand cases and the
  120-case generated population almost certainly do not exercise quoted-comma
  members or non-UTF-8 stdin (I never read them). The counter can read
  `met=true` on the final candidate, but its population would also have read
  `met=true` on the defective `5a3bd465…` bytes: **the counter does not
  discriminate the defect class this round just lived through.** A successor
  population needs at least one quoted-comma member case and one non-UTF-8
  stdin case (R92-4/R92-5, one contract generation later).
- Neither defect, on the bytes where they existed, tripped any frozen kill
  rule (no admitted forgery, no hand/generated disagreement, positive control
  admitted).

**F4 — PROCESS FINDING (churn): the candidate changed five times during this
review; one mid-state regressed.** Full timeline above. Two consequences: (a)
any measurement must pin a digest — mine does, and the counter's receipt-level
`candidate_sha256` pinning (r92 pattern) is the right defence; (b) an author
seat declaring "final" twice within two minutes (`b659029e…` then
`d3bac7de…`) shows the final-digest handshake needs the reviewer's
re-confirmation round, which this addendum is. My scored-bytes copies of
intermediate states were discarded; the probe transcripts above are the
evidence.

**C-OBS-1 (contract, clause 3 scope).** Clause 3 never states whether
"A malformed entity-tag is a refusal" governs only precondition members or
also `current.etag`. Candidate (final) and reference both validate
`current.etag`; my pins agree. Pin the scope in the contract's next revision.
**C-OBS-2 (contract, `role: null`).** Optional key with default `origin` — an
explicit `null` is refused by both implementations; contract should say so.
**C-OBS-3 (contract, duplicate stdin keys).** Both implementations take
last-value-wins (X04); the contract is silent, and the lane's round-25 quality
bar prefers "could-not-evaluate" over last-value-wins for duplicate members.
Successor-contract material, not scored here.
**C-OBS-4 (contract vs RFC, verified faithful).** Checked against the round's
retained sources: `rfc9110.txt` §13.2.2 precedence steps (lines 6222–6280),
strong/weak MUSTs (5794, 5880), If-Modified-Since suppression (5956–5965),
If-Unmodified-Since suppression (6037–6041), etagc ABNF (9871–9874);
`rfc9111.txt` §4.3.2 ("the If-Match and If-Unmodified-Since conditional header
fields are not applicable to a cache", ~line 889). The contract's steps 8–12
are a faithful subset of RFC 13.2.2 (If-Range excluded by declared scope) and
step 7 matches RFC 9111 4.3.2. One deliberate narrowing: RFC 9111 4.3.2's
"cache SHOULD use the stored response's Date field" when `Last-Modified` is
absent is not modelled (`last_modified: null` ⇒ `If-Modified-Since` ignored);
the Date field is outside the supplied input — declared scope limit, not a
defect. No contract-vs-RFC drift found.

## Claim relevance (recommendation only — the kill rules belong to the counter)

On the final bytes (`d3bac7de…`) the candidate passes my full independent
battery with zero disagreements; I have no finding that contradicts the C2
after-state the counter is expected to read (`hand=44/44 generated=120/120
forgeries_refused=6/6 positive=admitted … met=true`). The routed debt is F3:
the frozen reference and population cannot see the quoted-comma or
stdin-encoding defect classes, so this round's `met=true` would have been
equally true on bytes that had both defects. Route F3 (reference re-check
against the contract; population additions) exactly as R92-4/R92-5 were
routed; do not patch the frozen reference post-scoring.

## Receipts (this directory)

- `cases.json` — all 162 cases against the final bytes: input, pin, raw
  exit/stdout/stderr, verdict, agreement (target sha256 `d3bac7de…`).
- `agreement.txt` — summary (162/162, no DISAGREE lines).
- `posgood_cases.json`, `posgood_agreement.txt` — same battery against the
  frozen positive control (sha256 `0fe018a8…`): 160/162, D21+E01 disagree.
- `battery.py` — the exact corrected harness: oracle, pins, selfcheck, runner.

## Honest limits

- I never read `c93_conditional.py`, its hand cases or its reference, any
  `neg-*.py`, or `build-fixtures.py`; the quoted-comma blind-spot claim about
  the counter's population is an inference from the reference's behaviour
  (marked [INFERENCE] above), not a reading of its cases.
- The oracle and pins share an author (me). The pre-frozen `pos-good.py` run
  is the author-independent anchor — and on the two defect points it anchors
  the *defective* behaviour, which is why the contract text and the RFC ABNF
  are the deciding evidence in F1/F2.
- Intermediate-digest readings in the digest-history table that were not
  battery-scored rest on direct single-case probes (transcripts above).
- Non-goals I did not probe: performance, concurrency, argv behaviour beyond
  `--selftest`'s existence, audit-hook sandbox interaction (the counter's
  concern), and any live-network or cache-store semantics (outside the
  contract's declared scope).
