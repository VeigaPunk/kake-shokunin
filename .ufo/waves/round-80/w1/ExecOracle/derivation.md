# ExecOracle — independent re-derivation of the round-80 a2 oracle

Method: hand derivation from (i) the frozen round-79 grammar
(`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-79/contract.md`, §"C2 tool interface",
grammar items 1–9) and (ii) amendment 1
(`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-80/amendments/amendment-1.md`, A1–A3).
`scripts/x_robots_tag_audit.py` was never executed; `expect/expect.json` was not consulted until the
table below was fixed. Case field values were read from the frozen manifests
(`.ufo/waves/round-80/cases/cNN/manifest.json`); all 12 match the contract's case table verbatim.

## Shared clauses (cited by id below)

- **G1** (r79 item 1): split field value on ASCII `,`; trim each segment of ASCII ws; empty segment → `xrt_empty_rule`.
- **G2** (r79 item 2): first-`:` prefix matching `^[A-Za-z0-9_-]+$` and not a known directive name → bot scope; remainder (trimmed; pinned by r79 c05: `googlebot: noindex` → `bots.googlebot=["noindex"]`, `cases/c05/manifest.json:10`, `expect/expect.json:63-68`) parsed as one rule under the scope; scope persists to end of field value.
- **G3** (r79 item 3): otherwise directive: split at first `:`; name lowercased; unknown name → `xrt_unknown_directive`, contributes nothing.
- **G4** (r79 item 4): value validation per name; failing value → `xrt_invalid_value`, dropped.
- **G5** (r79 item 5): round-79 shapes — ISO 8601 `^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?(Z|[+-]\d{2}:\d{2})?)?$`; RFC 822 `^(Mon|…|Sun), \d{2} (Jan|…) \d{4} \d{2}:\d{2}(:\d{2})? GMT$`; RFC 850 `^(Monday|…|Sunday), \d{2}-(Jan|…)-\d{2} \d{2}:\d{2}:\d{2} GMT$`; ISO date-only accepted.
- **A1** (amdt §A1): a comma immediately following the leading weekday token of an `unavailable_after` value belongs to the value. Weekday tokens: `Mon`…`Sun` (IMF), `Monday`…`Sunday` (RFC 850). Only those commas; every other comma keeps G1.
- **A2** (amdt §A2): asctime joins: `(Mon|…|Sun) (Jan|…)` + day space-padded to width two (single space accepted, i.e. 1–2 spaces then 1–2 digits) + `hh:mm:ss YYYY`.
- **A3** (amdt §A3): a comma-bearing value that fails its shape yields `xrt_invalid_value` **only**, never `xrt_unknown_directive`.
- **VT** (value trim, implicit convention): the value after the directive colon is trimmed of surrounding ASCII ws before validation/rendering. Entailed by A1's own wording — for `Wed` to be "the leading weekday token of an `unavailable_after` value" in `unavailable_after: Wed, …`, the post-colon space cannot be part of the value — plus G1's segment-trim precedent and the c05 bot-remainder pin. No r79 case exercises it directly for directives (all r79 values are written without a space after the colon).
- **REN** (rendering, r79 item 7): token = lowercased name + `:` + value as declared (post-VT, internal ws preserved); normalization (r79 item 6) touches only `none`/`all`/`index`/`follow` and max caps, never date values.
- **DUP** (r79 item 6): duplicate = same value-bearing directive **name** twice in one scope, values irrelevant — pinned by r79 c21 (`max-snippet:50, max-snippet:100` → `xrt_duplicate_directive`, `cases/c21/manifest.json:10`, `expect/expect.json:327`).
- **G7** (r79 item 7): `directives` = declared normalized global tokens, duplicates kept, sorted; `effective` removes positives (`all`/`index`/`follow`), drops caps under `nosnippet`, collapses duplicate caps to min; per-bot effective out of scope.
- **G9** (r79 item 9): exit 0 no findings, 1 findings, 2 input fault. Sorting is codepoint sort.

## Per-case derivation

| id | field value | segmentation (clause) | derivation | directives | effective | bots | findings | exit |
|---|---|---|---|---|---|---|---|---|
| c32 | `unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` | 1 seg (A1 protects comma after `Wed`) | G3/G4 + G5 RFC 822: `Wed, 03 Dec 2025 13:09:53 GMT` matches `Day, \d{2} Mon \d{4} \d{2}:\d{2}(:\d{2})? GMT` ✓ | `unavailable_after:Wed, 03 Dec 2025 13:09:53 GMT` | same (G7: not a positive; no `nosnippet`) | {} | [] | 0 |
| c33 | `unavailable_after: Sunday, 06-Nov-94 08:49:37 GMT` | 1 seg (A1; `Sunday` ∈ RFC 850 weekday list) | G5 RFC 850 ✓ (`06-Nov-94`, `08:49:37`, `GMT`) | `unavailable_after:Sunday, 06-Nov-94 08:49:37 GMT` | same | {} | [] | 0 |
| c34 | `unavailable_after: Sun Nov  6 08:49:37 1994` | 1 seg (no comma) | A2 asctime: `Sun` `Nov` day = 2 spaces + `6` (padded width two) `08:49:37` `1994` ✓; REN keeps declared double space | `unavailable_after:Sun Nov  6 08:49:37 1994` | same | {} | [] | 0 |
| c35 | `unavailable_after:2025-12-31` | 1 seg | G5 ISO, date-only explicitly accepted ✓ | `unavailable_after:2025-12-31` | same | {} | [] | 0 |
| c36 | `unavailable_after:2025-12-31T23:59:59-03:00` | 1 seg | G5 ISO with `T`-time, seconds, `-03:00` offset ✓ | `unavailable_after:2025-12-31T23:59:59-03:00` | same | {} | [] | 0 |
| c37 | `unavailable_after: Wed, 03 Dec 2025 13:09:53 PST` | 1 seg (A1 protects comma after `Wed` — protection is unconditional on eventual shape match) | G4: `…PST` fails RFC 822 (` GMT$` required), fails asctime (`YYYY` required; form has no comma) → `xrt_invalid_value`, dropped; A3: invalid **only** (segment's name is known) | [] | [] | {} | `xrt_invalid_value` | 1 |
| c38 | `noindex, unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT, noarchive` | 3 segs: `noindex` / `unavailable_after: Wed, …GMT` (A1 inner comma protected; comma after `GMT` terminates) / `noarchive` | all known and valid (G3/G4/G5) | `noarchive`, `noindex`, `unavailable_after:Wed, 03 Dec 2025 13:09:53 GMT` (codepoint sort: `noarchive`<`noindex`<`unavailable_after:…`) | same | {} | [] | 0 |
| c39 | `unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT, unavailable_after: Sunday, 06-Nov-94 08:49:37 GMT` | 2 segs (comma after `GMT` terminates; A1 protects `Sunday,`) | both valid (RFC 822 / RFC 850); same value-bearing name twice in global scope → DUP | `unavailable_after:Sunday, 06-Nov-94 08:49:37 GMT`, `unavailable_after:Wed, 03 Dec 2025 13:09:53 GMT` (dups kept, `S`<`W`) | same | {} | `xrt_duplicate_directive` | 1 |
| c40 | `googlebot: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` | 1 seg (A1 reaches bot-scoped rules: its scope clause constrains the value's shape, not the scope) | G2: prefix `googlebot` matches, not a known directive → bot scope; remainder (VT, c05 pin) = valid RFC 822 under scope; G7: no global tokens, per-bot effective out of scope | [] | [] | `googlebot` → `unavailable_after:Wed, 03 Dec 2025 13:09:53 GMT` | [] | 0 |
| c41 | `unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT, frobnicate` | 2 segs (comma after `GMT` terminates) | seg1 valid RFC 822; seg2 `frobnicate`: no `:` → not a bot scope (G2), G3 unknown → `xrt_unknown_directive`, contributes nothing | `unavailable_after:Wed, 03 Dec 2025 13:09:53 GMT` | same | {} | `xrt_unknown_directive` | 1 |
| c42 | `max-snippet: 20, unavailable_after: Sunday, 06-Nov-94 08:49:37 GMT` | 2 segs (comma after `20` terminates — A1 protects only weekday-following commas; A1 protects the `Sunday,` comma in seg2) | seg1: prefix `max-snippet` IS a known directive → not a bot scope (G2 exclusion); G4 `^-?\d+$` on value `20` (VT) ✓; seg2 RFC 850 ✓. G7: `nosnippet` absent → cap kept | `max-snippet:20`, `unavailable_after:Sunday, 06-Nov-94 08:49:37 GMT` | same | {} | [] | 0 |
| c43 | `unavailable_after: Sun Nov 16 08:49:37 1994, noindex` | 2 segs (comma after `1994` is not weekday-following → terminates per A1's "only" clause) | seg1 A2 asctime: `Sun` `Nov` day = 1 space + `16`, `08:49:37`, `1994` ✓; seg2 `noindex` ✓ | `noindex`, `unavailable_after:Sun Nov 16 08:49:37 1994` | same | {} | [] | 0 |

## Diff vs frozen oracle (`expect/expect.json`, sha256 `8f24c0aaede6a9c893a4f6bd079667b8047ffe570557e44862501b00c0568e9a`)

Compared on exit, finding-id list, and each check's `directives`/`effective`/`bots`:

| id | verdict |
|---|---|
| c32 | agree |
| c33 | agree |
| c34 | agree |
| c35 | agree |
| c36 | agree |
| c37 | agree |
| c38 | agree |
| c39 | agree |
| c40 | agree |
| c41 | agree |
| c42 | agree |
| c43 | agree |

**Disagreements: none.** 12/12 agree on all compared fields.

## Is any expectation fitted to the round-79 tool's behaviour?

No. The set is structurally unfitted: 10 of 12 cases (c32–c34, c37–c43) expect outcomes the
untouched round-79 tool gets *wrong* — it splits on every comma and produces `xrt_invalid_value`
+ `xrt_unknown_directive` on c32/c33/c37/c38/c39/c40/c41 and `xrt_invalid_value` on c34/c43
(round-79 §Limits; `controls/base-c80-a2.txt`: `a2 wrong=10`). An oracle fitted to that tool would
have to expect findings where the grammar says clean, and A3 (§A3) pins the opposite. The only two
cases where the old tool and the oracle agree — c35, c36 — are pinned by round-79 grammar item 5
itself (ISO shapes, date-only accepted), so agreement there is grammar-entailed, not tool-derived.

Two latent conventions worth naming (not disagreements; both favour the frozen oracle):

1. **VT (value ws-trim)** — relied on by every comma-bearing case (c32's own token rendering) and
   standing *alone* on it in c42 (`max-snippet: 20` → `max-snippet:20`): no round-79 case exercises
   a space after a *directive* colon, so VT is supported textually (A1's "leading weekday token of a
   value" phrasing + G1 trim precedent) and by the c05 bot-remainder pin, but by no frozen case.
   ExecGrammar implementing VT (required for c32–c41) gets c42 for free; a no-VT implementation
   fails 10 cases, so the set pins the convention de facto.
2. **A2 regex notation** — the amendment's literal `{1,2}[0-9]{1,2}` is loose; the prose
   ("space-padded to width two, a single space also accepted") and RFC 9110 pin `[ ]{1,2}[0-9]{1,2}`.
   Read strictly, an unpadded single-space one-digit day (`Nov 6`) matches the loose regex but not
   strict RFC 9110; no case exercises it, so either implementation agrees with all 12 expectations.
   c34 (2 spaces + 1 digit) and c43 (1 space + 2 digits) are the pinned forms.

Also verified (frozen-oracle integrity, not authority): re-running the authoring record
`make_cases.py` from a scratch copy reproduces `cases/` and `expect/expect.json` byte-for-byte
(`cases=12`, rc=0; `diff -r` rc=0; `diff` rc=0; receipts
`.ufo/waves/round-80/w1/ExecOracle/receipts/repro-diff.txt` sha256
`8d8217208cfc32bdd524209095710770212fb2b7d057092a522cb1ecc5d541ec`, `regenerated-expect.json`
sha256 `8f24c0aaede6a9c893a4f6bd079667b8047ffe570557e44862501b00c0568e9a` = frozen oracle sha).
Scratch tree `/fast/scratch/hyaku/kake-r80/ExecOracle` deleted (verified absent).
