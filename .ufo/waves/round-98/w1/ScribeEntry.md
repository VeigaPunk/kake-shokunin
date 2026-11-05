# ScribeEntry — round-98 C2 knowledge entry and coverage-map row

Seat ScribeEntry, kake round 98 (hyaku run 15, attempt 1), wave 1. Leaf member:
no subagent dispatch. Every command below was run by this seat; each verdict
line names its command and its observed rc.

## Behavior

Three deliverables, all under
`LANE/.ufo/waves/round-98/w1/ScribeEntry/`, plus one report at
`LANE/.ufo/waves/round-98/w1/ScribeEntry.md`.

1. **`stale-extensions.md`** — the draft C2 knowledge entry, in the shape of
   `LANE/corpus/knowledge/revalidation-exchange.md`. First lines are
   `source:` (S482, S483, S480, S478), `verified-at: 2026-11-05`,
   `recheck: 180d`, `ground:`, `scope:`. The body carries: what RFC 5861 §3/§4
   say (31 quotes total, each ≤25 words, each with its plain-text line span in
   the retained body it comes from); how RFC 9111 §4.2.4 and §5.2.2.2 /
   §5.2.2.8 / §5.2.2.10 prohibit serving stale and how RFC 9111 §4.2.4 names
   RFC 5861 as the permission; the RFC 9110 §5.6.2/§5.6.4 field grammar the
   Cache-Control parse rests on; a 15-row clause table that labels each clause
   either RFC-exact or a lane convention; the tool `scripts/stale_extensions.py`
   and the counter `.ufo/waves/round-98/c98_stale.py` with their digests, the
   counter's output line and the round's frozen predicate; an explicit
   "What this entry does not decide" list; and an errata section for RFC 5861.
   No seat meta-text: the draft contains no "Drafted by", no "this seat", no
   "the L1 integrates", no "word-count receipt", no "quotes-verified.txt", no
   `body is N words`, no seat-id and no `.ufo/waves/round-N/w1/` path.
2. **`readme-row.md`** — one `corpus/README.md` Entry-table row in the
   round-97 columns (Area | Entry | Coverage), carrying
   `knowledge/stale-extensions.md`, all four source ids and 38 other-cell
   words, with the placement note and the column-by-column check.
3. **`quote-check.txt`** — every quote `grep -n`'d in its retained body, with
   the body digests, the located line number and the observed rc.

## Gates

| Gate | Command | Observed |
|---|---|---|
| Quote truth (31 quotes) | `python3 -B verify-quotes.py` (scratch) | `violations=0 quotes=31 located=31`, rc 0 |
| Draft↔table agreement | same run, `table_rows=31 row_mismatches=none` | rc 0 |
| README row vs the index counter's own rules | `python3 -B check-row.py` (scratch) | rules (a)(b)(c) all True, `violations=0`, rc 0 |
| The counter's public CLI over the fixture | `python3 -B .ufo/waves/round-97/c97_index.py --root <fixture> --revision HEAD --work <scratch>` | `entries=85 indexed=85 unindexed=0 dangling=0 mismatches=0 met=true`, rc 0 |
| Index counter at master (pre-change baseline) | `python3 -B .ufo/waves/round-97/c97_index.py --root . --revision master --work <scratch>` | `entries=84 indexed=84 unindexed=0 dangling=0 mismatches=0 met=true`, rc 0 |
| Meta-text patterns in the draft | `grep -n -i 'Drafted by\|this seat\|word-count receipt\|quotes-verified.txt\|the L1 integrates\|body is [0-9]* words'` over the draft | rc 1 (no match) |
| Seat-id / seat-scratch-path patterns in the draft | `grep -n -o 'Scout[A-Z][A-Za-z0-9]*\|Exec[A-Z][A-Za-z0-9]*\|Scribe[A-Z][A-Za-z0-9]*\|\.ufo/waves/round-[0-9]*/w1/\|this seat\|L1 integrates'` | rc 1 (no match) |
| Corpus shape gate with the entry in place | `node scripts/corpus-contract.mjs --root <fixture>` (fixture = the lane clone plus the entry) | `result: 0 findings · 85 knowledge entries · 92 lane lessons · 82 skipped · 0 errors — exit 0`, rc 0 |
| Corpus meta-text gate over the seat directory | `python3 -B scripts/knowledge_metatext_lint.py --dir .ufo/waves/round-98/w1/ScribeEntry` | `files=2 gate_findings=0 review_hits=0`, rc 0 |

`verify-quotes.py` and `check-row.py` live in this seat's scratch directory
`/fast/scratch/hyaku/kake-r98/ScribeEntry/`; their output receipts
(`quote-check.txt`, `readme-row-check.txt`) are copied into the seat
directory. The scripts were deleted with the scratch tree at yield, so the
receipts are the durable record.

Frozen digests verified before any work, all matching
`LANE/.ufo/waves/round-98/controls/instrument-sha256.txt`:

- `c98_captable.py` → `efd598575c6e377ac76c68c876c96449bf80dc0e4b2fbf8c0436205167ac7cf3`
- `c98_stale.py` → `e0331e56378fb5acabe4447a37590cbf3273537aabd8c8d88f842e0a434a9f3f`
- `stale-contract.md` → `ec077b4f30ad786316df86e784290267b12df1cb11519623d9519b88fd971075`

Bodies quoted, re-hashed at draft time:

- RFC 5861 `LANE/.ufo/waves/round-98/sources/rfc5861.txt` →
  `1193f1c8710af162e1b9fb4250d79bc6dd26497df4caeeaaa8bcb2fefdd2529e`, 10 359
  bytes, 339 lines — the digest the freeze names.
- RFC 9111 `LANE/.ufo/waves/round-93/L1/src/rfc9111.txt` →
  `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, 84 477
  bytes, 1 956 lines; `cmp` against the round-96 fetch exit 0.
- RFC 9110 `LANE/corpus/lessons/round-81-gate/rfc9110.txt` →
  `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`, 10 785
  lines.

## Touched surfaces

Written, all inside the seat directory:

- `.ufo/waves/round-98/w1/ScribeEntry/stale-extensions.md`
- `.ufo/waves/round-98/w1/ScribeEntry/readme-row.md`
- `.ufo/waves/round-98/w1/ScribeEntry/quote-check.txt`
- `.ufo/waves/round-98/w1/ScribeEntry/readme-row-check.txt`
- `.ufo/waves/round-98/w1/ScribeEntry.md` (this report)

Nothing else in the lane tree was created, modified or deleted; the lane's
`git status --porcelain` shows only the pre-existing untracked round-98 wave
paths, none of them this seat's. No file was written to `corpus/`, to
`corpus/knowledge/`, to `corpus/README.md`, to `SCORECARD.md`, to `LOG.md`, to
`MANIFEST.json`, to `.ufo/state`, or to the fleet repo. The L1 integrates.

Scratch: `/fast/scratch/hyaku/kake-r98/ScribeEntry/` — created by this seat,
used for the two check scripts and one fixture clone
(`git clone --shared` of the lane, toplevel verified equal to the fixture dir
before its single fixture commit, identity `scribeentry@example.invalid` via
`-c` flags only). The seat's own scratch directory was removed at yield; no
ancestor or sibling of it was touched.

## Out of scope, not attempted

- No edit to `corpus/README.md`, `corpus/knowledge/stale-extensions.md`,
  `corpus/SOURCES.md`, `SCORECARD.md` or any other lane file: the seat is a
  reporter and the L1 integrates.
- No SOURCES row for RFC 5861 or its errata record (S482/S483). The seat
  cites them, as the spec's `source:` line requires; the registry row is
  another seat's and the L1's to land.
- No verdict on the C2 claim itself, on the candidate's sha256, or on the
  counter's score. The entry describes the tool and the counter; it reports no
  score. The frozen predicate's identity conjunct (scored sha256 equals the
  landed `scripts/stale_extensions.py`) was not evaluated by this seat.
- No repair of any instrument, contract or counter. The two interpretation
  points ExecStale flagged (`[INFERENCE]` on first-occurrence-for-values and
  on request-directive refusal scope) are recorded here as observations, not
  as changes.

## Findings

1. **The `source:` id set is wider than the quoted sections.** The spec
   fixes the entry's `source:` line to S482, S483, S480, S478. S480's
   registry scope is RFC 9111 §4.3.1/§4.3.3 (validation request and
   response), while the RFC 9111 clauses this entry actually quotes are §4.2.4
   and §5.2.2.2/§5.2.2.8/§5.2.2.10/§5.2.2.4/§5.2.1.4/§1.2.2/§4.2.1; S478's
   registry scope is RFC 9110 §5.6.1.2 and §5.6.3, while the entry quotes
   §5.6.2 and §5.6.4. The entry says so explicitly in its "What this entry
   cites" section rather than implying the rows cover the quoted sections.
   Routed to the L1 as a registry-scope observation, not a defect of the
   entry; the ids are the frozen instruction.
2. **Two RFC 9110 sections are quoted without a registry row naming them.**
   RFC 9110 §5.6.2 (Tokens) is covered by S465, not S478, and §5.6.4 (Quoted
   Strings) has no row at all in `corpus/SOURCES.md` as far as
   `grep -n -E '^\| S[0-9]+ .*5\.6'` shows (S453 covers §5.6.7 only). The
   entry quotes both and cites the S478 body, which is where the retained
   RFC 9110 text lives. A §5.6.4 row would close the gap. This is the
   L1's to open.
3. **The lane's own corpus convention is to cite the canonical retained body
   path, not a wave seat's copy.** `corpus/knowledge/revalidation-exchange.md`
   cites `.ufo/waves/round-93/L1/src/rfc9111.txt` and mentions the round-96
   fetch only as a byte-identity note. The draft follows that: it cites the
   round-93 path and says the body is byte-identical to this round's fetch
   (`cmp` exit 0). This also keeps the draft free of the `.ufo/waves/round-N/w1/`
   path that the R98-D1 meta-text gate flags for review.
4. **RFC 5861 has two Verified editorial errata, and neither reaches a quoted
   clause.** Read from the round-98 retained errata body: EID 2255 (§3) and
   EID 2256 (§4), both Editorial, both proposing "Age header" → "Age header
   field" and "warning header" → "Warning header field" in the note after the
   stale-if-error paragraph. The card census is one category card, "Verified
   (2)" — there is no Reported, Held or Rejected erratum for RFC 5861. The
   entry's errata section says this and names the four clauses that carry no
   erratum.
5. **Two observations carried, not acted on.** ExecStale flagged two
   `[INFERENCE]` interpretation points: that "the FIRST occurrence of a name is
   used" is read as applying to directive *values* while prohibition checks are
   *presence* checks over the whole field, and that the request-directive
   refusal is enforced in the request field only (a response carrying
   `max-age=600` is not refused). Both passed every counter case. The entry
   records the corresponding readings as lane conventions (C13, C14, C15) and
   does not adjudicate them.
6. **The entry's `staleness` figure is a lane computation, not an RFC one.**
   RFC 5861 bounds staleness by "more stale than the indicated amount" without
   defining it numerically; the contract's `max(0, A − L)` over a supplied
   lifetime and age is the lane's arithmetic. The entry marks it as such in
   C1 and C7 rather than implying the RFC fixes it.

## Artifacts

- `LANE/.ufo/waves/round-98/w1/ScribeEntry/stale-extensions.md` — the entry draft
- `LANE/.ufo/waves/round-98/w1/ScribeEntry/readme-row.md` — the README row draft
- `LANE/.ufo/waves/round-98/w1/ScribeEntry/quote-check.txt` — per-quote `grep -n` receipts
- `LANE/.ufo/waves/round-98/w1/ScribeEntry/readme-row-check.txt` — the row's counter-rule check
- `LANE/.ufo/waves/round-98/w1/ScribeEntry.md` — this report

## Tooling

No tool was installed or upgraded. Only `python3` (3.14.8, already present)
and `grep`/`sha256sum`/`cmp`/`git` (already present) were used. No pacman
command was run; no PATH directory was touched.

SCRIBE-ENTRY quotes=31 located=31
