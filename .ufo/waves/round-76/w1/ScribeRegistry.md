# ScribeRegistry — round-76 w1: registry rows, capability row, LOG entry, claim table (draft)

Seat: leaf scribe, read-only. Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`; contract
`.ufo/waves/round-76/contract.md` (frozen at `b758cb04`; base `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`),
amendments 1–8, and `.ufo/waves/round-76/l1-dispositions.md` read before drafting. Axes named before
drafting: (a) **claim truth** — a cell carries a number only when an admissible committed receipt contains
that exact line, else `pending(L1)`; (b) **shape fidelity** — the registry fence is the 8-column table of
`SKILL.md` `### Round 74/75 gate registry additions`; (c) **supersession discipline** — no historical cell is
rewritten, and each correction names the superseded bytes verbatim beside the current value and its
receipt; (d) **self-application** — every claim-bearing span in the SCORECARD fences below is a contiguous
substring of a receipt that survives the round's receipt-universe rules (amendment 5 §D1–D3, amendment 7
§F1) or the literal `pending(L1)`.

**Status at the tip (measured, not assumed).** The final receipt is
`controls/after-c1-quote-truth-final.txt`: `C1v2 revision=7ac91803 rows=42 receipt_files=7934 spans=67 exempted=7 corrections=8 findings=0 met=true`
with `observed-exit=0`; my own run at `HEAD` reproduced `findings=0 met=true`, exit 0. The delivered counter
is `scripts/doc_quote_truth.py` sha256 `e7f86d3aa0554f61330179f803fcc7624504b2ee63ea2d3e1a9ee5e3427f59ae`,
selftest `selftest: 63/63 passed`. The L1's own blocks corrected the two defects this seat independently
measured at `2cccd59a` (a stale `selftest: 47/47` claim and eight quote findings in
`corpus/lessons/round-76.md`).

**What happened to this draft.** The L1 applied the registry rows, the capability row, the LOG entry and a
claim table of its own at `2cccd59a`, then repaired the lesson and re-cut the C1 receipt at `9dea7b2f`,
`b8673e87`, `7ac91803` and `b5597f55`. Against that landing:

| Draft block | Disposition |
|---|---|
| (a) `SKILL.md` registry rows | **superseded.** The L1's two rows landed at `2cccd59a` and are accurate in Kind, verdict map and selftest; they differ only in the base-receipt pointer (the landed row cites `controls/base-c1-quote-truth-v2.txt`, which §D3 excludes; `controls/c1-base-summary.txt` is the admissible carrier) and in writing `selftest 63/63 passed` without the tool's colon. |
| (b) `SCORECARD.md` capability row | **superseded.** Landed at `2cccd59a` in the `## Capabilities` table; the landed wording already carries amendment 8 §G1/G2's limits. The receipt-quoted evidence cell in my block is the only enrichment. |
| (c) `LOG.md` entry | **partly applied, then overtaken.** The landed entry is structurally the same; its C1 bullet was corrected to the 63/63 tally at `b8673e87`, and it does not yet name the final receipt `controls/after-c1-quote-truth-final.txt` (it cites `controls/after-c1-quote-truth.txt`, the earlier `revision=master` run). My three R1/R2/R3 bullets use the same facts the landed `corpus/lessons/round-76.md` §Corrections now states. |
| (d) `SCORECARD.md` claim table | **superseded.** The landed section states the values in words rather than quoted lines; it is green (tip run `findings=0`). My fence is a drop-in replacement for its two claim rows and move log if the receipt-quoted form is preferred. |

**Claims in this draft that are now false (corrected in the text below).** (i) The after-state line I first
quoted (`revision=master rows=42 …` from `controls/after-c1-quote-truth.txt`) is superseded by the final
receipt at `7ac91803`; (ii) I wrote that the lesson's `## Corrections` bullets were still red and that the
`selftest: 47/47` claim stood — both were true at `2cccd59a` and are false at `7ac91803`; (iii) I listed
`selftest 59/59 passed` as the hreflang tally without a receipt — the tally is right, but it still has no
admissible committed receipt, so it remains `pending(L1)` for quotable use.

No lane file except `.ufo/waves/round-76/w1/ScribeRegistry.md` was created or edited; no `git`/`jj` mutation
was run in the lane; nothing was installed. Scratch `/fast/scratch/hyaku/kake-r76/ScribeRegistry` (two
read-only `git clone --shared` trees, every `--work`); removed before yield.

## (a) `SKILL.md` — `### Round 76 gate registry additions`

The L1 landed this section at `2cccd59a` (two rows). The fence below is the seat's text for the same
section; if the landed rows stay, the only deltas are the two `Pinned values` cells, which should name the
admissible receipts (`controls/c1-base-summary.txt`, `controls/after-c1-quote-truth.txt`,
`controls/counter-selftest.txt`, `controls/after-c2-matrix.txt`) instead of the excluded
`base-c1-quote-truth-v2.txt` alone.

````markdown
### Round 76 gate registry additions

Round 76 registers the two instruments this round delivers and supersedes no earlier row: the section is
appended at EOF, below line 935 — the largest `SKILL.md` line pinned in
`corpus/knowledge/freshness-sidecar.json` — so no pinned line moves; a future row keeps this append-at-EOF
discipline or re-pins the sidecar in the same commit. Effective-row rule (round-75 precedent): the last row
naming an instrument wins; a superseded row is replaced by a new row that names its successor and the
class, and the old cell is never edited in place. Withdrawal rule: a row goes when its instrument leaves
the tree.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| scripts/doc_quote_truth.py | gate (live; offline over committed bytes; calibration: every claim-bearing backticked span in the effective claim rows of rounds 75–76 is a contiguous substring of a committed receipt that survives the round's receipt-universe rules — a receipt directory of any round (`controls/`, `verification/`, `resid/`, `receipts/`, `frozen/`, `fixtures/`, `cases/`, `sources/`, `live/`), the newest measured round's `w1/` seat tree excluded, diagnostic lines stripped, this round's `base-c1-quote-truth*.txt` and `ctl-*.txt` excluded by name — or carries an explicit elision whose non-empty fragments are contiguous inside one receipt, or is closed by a correction line that quotes a claim-bearing whole receipt line and names the defective span; `T1/T2/T4` findings with the `A1` exact-text append-only conjunct; `met = (findings == 0) and append_only`) | `python3 -B scripts/doc_quote_truth.py --root . --revision <rev> --base a0491fcd041cbc3fff2c964ecf6268557e45a5c1 --rounds 75,76` | `0=met` (`findings=0` and `append_only=true`; summary `C1v2 revision=<rev> rows=N receipt_files=N spans=N exempted=N corrections=N findings=0 met=true`); `1=findings` (`met=false`, each finding printed as `<id> <file>:<line> <detail>`); `2=input fault` (`input: <detail>` on stderr); `64=usage` (bad `--rounds`, `--selftest` without `--work`, or a missing `--base`) | `python3 -B scripts/doc_quote_truth.py --selftest --work <dir>` → `selftest: 63/63 passed`, exit 0 (amendment 5 §D5: a run that executes every case) | predicate frozen `.ufo/waves/round-76/contract.md` §C1 with amendments 3–5 and 7; base receipt `controls/c1-base-summary.txt` line `C1v2 revision=a0491fcd rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false`; after receipt `controls/after-c1-quote-truth.txt` line `C1v2 revision=master rows=42 receipt_files=7933 spans=67 exempted=7 corrections=8 findings=0 met=true` with `observed-exit=0`; selftest receipt `controls/counter-selftest.txt` | read-only (committed bytes at `--revision`; writes only under `--work`) | kake |
| scripts/hreflang_audit.py | gate (live; offline over a versioned manifest of local HTML pages; operability: a frozen ASCII grammar validator for BCP-47-shaped tags, never a BCP-47 validator (amendment 8 §G2), deciding `hreflang_missing_value`, `hreflang_invalid_tag`, `hreflang_relative_href`, `hreflang_duplicate_pair`, `hreflang_multiple_xdefault` (one per element, amendment 6 §E2), `hreflang_self_missing`, `hreflang_nonreciprocal` (same-tag return: a lane policy stricter than the S444 missing-return-links rule, amendment 8 §G1; external targets informational, exit 0 alone), `hreflang_canonical_not_self` (a non-absolute canonical yields no finding, amendment 6 §E1), with `input_unreadable`/`input_duplicate_url`/`input_url_not_absolute` as faults; no live fetch, headers, rendering, language-truth or search-engine claim) | `python3 -B scripts/hreflang_audit.py --manifest <path> --root <dir> [--json] [--work <dir>]` | `0=clean` (no policy finding; informational findings alone exit 0); `1=policy findings`; `2=input faults` (also when policy findings are present); `64=usage` (missing `--manifest` without `--selftest`, manifest `version` ≠ 1, `--selftest` without `--work`) | `python3 -B scripts/hreflang_audit.py --selftest --work <dir>` → `selftest 59/59 passed`, exit 0 (committed tally `pending(L1)`) | predicate frozen §C2 with amendments 1, 2, 6 and 8; matrix receipt `controls/after-c2-matrix.txt` line `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true`, the four constants each failing `failed=69/69` decided cases, `observed-exit=0`; real-input receipt `controls/after-c2-realrun.txt` (`"pages": 8`, empty `findings`, `rc=0`) | read-only (writes only under `--work`) | kake |
````

## (b) `SCORECARD.md` — capabilities-table row

One row for the `## Capabilities` table (4 columns). Contract §C2 kill rule 3 gates it on the real-input
run, which exists.

````markdown
| Offline hreflang declaration audit | Reads a version-1 manifest of local HTML pages and reports, read-only and network-free, missing or malformed hreflang values under a frozen ASCII grammar validator for BCP-47-shaped tags, relative alternate hrefs, duplicate tag/href pairs, multiple x-default declarations (one finding per element), a page that omits its own URL from its alternates, non-reciprocal manifest-internal targets under a same-tag lane policy that is stricter than the S444 missing-return-links rule (external targets informational), and a canonical that is not the page's own URL (clean / policy findings / input faults, exits 0/1/2/64); no live fetch, headers, rendering, language-truth or search-engine claim | `scripts/hreflang_audit.py`; matrix `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true` with `observed-exit=0` (`.ufo/waves/round-76/controls/after-c2-matrix.txt`); real-input run over 8 retained served pages, `rc=0` and empty findings (`.ufo/waves/round-76/controls/after-c2-realrun.txt`) | 76 |
````

## (c) `LOG.md` — round-76 entry

The L1 landed a round-76 entry at `2cccd59a` (tally corrected at `b8673e87`). The fence below is the
seat's text for the same entry with the C1/C2 lines re-quoted from admissible receipts and the three
round-75 correction bullets; apply it as a replacement only if the landed entry is being re-cut.

````markdown
## Round 76 — 2026-11-03 (hyaku run 15; attempt 1; Linux host; claims frozen before any seat ran)

- **Frozen contract.** `.ufo/waves/round-76/contract.md` at `b758cb040d53374b1b63b89702c7128f77212d23`, base `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`, the v1 counter `.ufo/waves/round-76/c76_quote_truth.py` (selftest 13/13) and five red controls. Amendments 1–8 are terms-only, each recorded before the after-state it binds: A1 fixes the real-input population at the 8 retained served pages; A2 decides the classes the contract left undecidable; A3 splits revision citations from digests, dedupes the population, makes correction closure whole-line and append-only exact-text; A4 excludes this round's own diagnostic controls by name; A5 admits only receipt directories, strips diagnostic lines and requires a selftest that executes every case; A6 fixes per-element `hreflang_multiple_xdefault` and non-absolute canonical handling; A7 limits the seat-tree exclusion to the newest measured round; A8 declares the same-tag reciprocity rule a lane policy stricter than S444 and the tag grammar a frozen ASCII validator, not BCP-47.
- **Motivating evidence.** C1 is claimed on calibration (score 2, the lane's lowest non-retired axis): at `a0491fcd` the delivered counter prints `C1v2 revision=a0491fcd rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false`, exit 1 (`.ufo/waves/round-76/controls/c1-base-summary.txt`) — the round-75 ledger's elided quotes plus five SCORECARD spans. C2 is claimed on operability as capability acquisition: the lane holds no hreflang instrument at the base.
- **Wave `w1`.** One v1 wave; `w1-spec.json` carries 15 seat items (scout 2, executor 5, scribe 2, reviewer 2, critic 1, mutation-tester 1, connector 1, sentinel 1); attack seats 4/15 = 26.7 %; the L1 held the planner seat (the validator rejects a planner role). Spec `w1-spec.json`, dispatch `w1-dispatch.json`, ready `w1.ready`, registry `w1/swarm-registry.json`.
- **C1 landed and measured.** `scripts/doc_quote_truth.py` (selftest `selftest: 63/63 passed`, `.ufo/waves/round-76/controls/counter-selftest.txt`). At the carrier `7ac91803` the counter prints `C1v2 revision=7ac91803 rows=42 receipt_files=7934 spans=67 exempted=7 corrections=8 findings=0 met=true`, `observed-exit=0` (`.ufo/waves/round-76/controls/after-c1-quote-truth-final.txt`). Seven whole-line correction rows close the seven base findings — five in `SCORECARD.md` `## Round 75 — quote corrections (appended round 76)`, one in `corpus/QUALITY.md` `## Round-76 criterion — quoted receipts are whole`, one in `corpus/lessons/round-75.md` `## Corrections`; the round-76 lesson's own `## Corrections` bullets quote claimy whole receipt lines. No historical line is rewritten: 44 insertions and 0 deletions across the three repaired files (`.ufo/waves/round-76/w1/ExecQuoteRepair/receipts/03-append-only-numstat.txt`).
- **C2 landed and measured (capability).** `scripts/hreflang_audit.py` (59,734 bytes, sha256 `0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac`; selftest `selftest 59/59 passed` in the wave tree, committed tally `pending(L1)`), manifest v1 `{"version":1,"pages":[{"id","file","url"}]}`. Matrix over 71 cases: `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true`, `observed-exit=0` (`.ufo/waves/round-76/controls/after-c2-matrix.txt`); the four constants (no-op, always-clean, report-all, empty-list) each fail `failed=69/69` decided cases. Real-input run over the 8 retained served pages (amendment 1): `"pages": 8`, empty `findings`, `rc=0` (`.ufo/waves/round-76/controls/after-c2-realrun.txt`); the four not-served surfaces are reported as not-served, never counted clean. The two undecided cases are amendment 8 §G3's contract defects, excluded from the score.
- **Corrections (round-75 closure R1/R2/R3; append-only, no historical line edited).**
  - **R1 — stale counter digest, `LOG.md:2534`.** Superseded text: `` `c75_row_truth.py` (frozen v0 → hardened `0699a672…`, selftest 29/29) `` — `0699a672…` is the blob at `4e3fc159`. Current value: the receipt's whole lines `counter_sha256=63e321b28e509781405f1b4209a66b99460bc2512c92a8615fec06f2423e944b` (`.ufo/waves/round-76/controls/r1-r2-digests-v2.txt:1`, re-derived at `a0491fcd`).
  - **R2 — stale receipt digest, `LOG.md:2535`.** Superseded text: `` (18 entries, `f3128628…`, 3,793 B) `` — `f3128628…` is the cut at `4e3fc159`. Current value: `receipt_sha256=15768f81460bcbf991bacf9ffdf6a2145d32f4de7d952f52526589d8013e6613 receipt_bytes=3793` (`.ufo/waves/round-75/controls/after-c2-receipts.txt:2`), re-derived at `a0491fcd` in `.ufo/waves/round-76/controls/r1-r2-digests-v2.txt`.
  - **R3 — disagreeing revision labels.** Superseded text: the round-75 report's table header `` | Claim | Counting command | Before (base `c9c5e484`) | After (tip `6c10b433`) | `` (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-75/kake.md:85`), while every after cell and the receipt it cites name `f87d14a9`; and the tip paragraph's `` the receipt commit that follows the measured revision `3ae076ab` `` (same file, line 10). Current value, one measured revision per artifact: the revision witness is `C1v1 revision=f87d14a9 rows=32 live=20 files=18 mismatches=0 classes=- append_only=true met=true missing_frozen=0` (`.ufo/waves/round-75/controls/after-c1-row-truth.txt:4`); the harm battery names its own tree `== harm battery at 306fff49b3a64bc32bb468f6c26fb4b577ac0c4a` (`.ufo/waves/round-75/controls/after-harm-battery.txt:1`), its complete bytes committed at `0df52aed`.
- **Frontier and sources.** `corpus/SOURCES.md` 181 → 184 rows: S444 (Google, localized versions), S445 (WHATWG HTML, `hreflang` and link type `alternate`) and S446 (RFC 5646) opened this round, retained under `.ufo/waves/round-76/w1/ScoutHreflangSources/`; new entry `corpus/knowledge/hreflang-declaration.md` cites them. Census before: 181 rows, exit 0 (`.ufo/waves/round-76/controls/census-before.txt`); round-end census `pending(L1)`. Assimilation: none — `w1/ConnectorOverlap.md` finds no sibling holds an hreflang audit and every `merge/kake/` locator still fails to re-ground.
- **Routed (not claimed).** `pending(L1)`: the wave's residuals (the undecidable matrix classes, the pinned-build split in the real-input run) and the five round-75 items the L1 disposition ledger leaves open (R4 sidecar instruments unbound, Q1 E2 multi-pair semantics, Q3 receipt-schema decision, Q4 host-absolute path hygiene).
- **Not done this round.** No publish or deploy; no MANIFEST edit; no tool installed or upgraded; pacman untouched.
````

## (d) `SCORECARD.md` — round-76 claim table

The L1 landed a `## Round 76 — declared claims` section at `2cccd59a` (words, no quoted values). The fence
below is a replacement for that section's two claim rows and its move log, with the values re-quoted from
admissible receipts; the section heading and the capability table can stay as landed.

````markdown
| Claim | Axis | Before → after | Counting command | Verdict |
|---|---|---|---|---|
| C1 claim rows quote only committed receipts | calibration 2→2 HOLD | base `a0491fcd`: `C1v2 revision=a0491fcd rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false`, exit 1 (`.ufo/waves/round-76/controls/c1-base-summary.txt`) → carrier: `C1v2 revision=7ac91803 rows=42 receipt_files=7934 spans=67 exempted=7 corrections=8 findings=0 met=true`, `observed-exit=0` (`.ufo/waves/round-76/controls/after-c1-quote-truth-final.txt`) | `python3 -B scripts/doc_quote_truth.py --root . --revision <rev> --base a0491fcd041cbc3fff2c964ecf6268557e45a5c1 --rounds 75,76` | measured met; seven whole-line correction rows plus the lesson's own `## Corrections` bullets; counter selftest `selftest: 63/63 passed` (`.ufo/waves/round-76/controls/counter-selftest.txt`) |
| C2 offline hreflang declaration audit on a versioned manifest | operability 10→10 HOLD (capability) | base `a0491fcd`: no hreflang instrument → matrix over 71 cases: `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true`, `observed-exit=0` (`.ufo/waves/round-76/controls/after-c2-matrix.txt`); real-input run on 8 retained served pages: `rc=0`, empty findings (`.ufo/waves/round-76/controls/after-c2-realrun.txt`) | `python3 -B .ufo/waves/round-76/w1/ExecAuditMatrix/c76_hreflang_matrix.py --root . --tool scripts/hreflang_audit.py --revision <rev> --work <scratch>` | measured met; the four constants each fail `failed=69/69` decided cases; 2 contract-undecidable cases excluded, never counted as passes |

Move log (round 76):
| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 76 | calibration (HOLD 2) | `C1v2 revision=a0491fcd rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false`, exit 1 | `C1v2 revision=7ac91803 rows=42 receipt_files=7934 spans=67 exempted=7 corrections=8 findings=0 met=true`, `observed-exit=0` | `scripts/doc_quote_truth.py`, `.ufo/waves/round-76/controls/{c1-base-summary.txt,after-c1-quote-truth-final.txt}` |
| 76 | operability (HOLD 10) | no hreflang instrument in `scripts/` | `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true` | `scripts/hreflang_audit.py`, `.ufo/waves/round-76/controls/after-c2-matrix.txt`, `.ufo/waves/round-76/controls/after-c2-realrun.txt` |
````

## Delta against the landed text at `7ac91803`

| Surface | Landed | Seat's delta |
|---|---|---|
| `SKILL.md` doc_quote row | cites `controls/base-c1-quote-truth-v2.txt` as the base receipt | that file is excluded by §D3; cite `controls/c1-base-summary.txt` (base lines) and `controls/after-c1-quote-truth.txt` (after lines) instead |
| `SKILL.md` hreflang row | selftest 59/59 passed (from the wave tree) | true of the landed tool; a committed tally receipt is still missing (`pending(L1)`) |
| `SCORECARD.md` claim rows | values written as words | replace with the two rows in block (d) if the receipt-quoted form is wanted; both are green either way |
| `SCORECARD.md` stated limits | "three matrix classes stay `undecided` (§G3)" | the admissible matrix receipt records `undecided=2` over 71 cases; amendment 8 §G3's "three" no longer matches the case set — say "the undecided residue (2 of 71 cases)" |
| `LOG.md` C1 bullet | tally corrected to 63/63 at `b8673e87` | matches the delivered build; the base/after lines can be added from `controls/{c1-base-summary.txt,after-c1-quote-truth.txt}` |
| `corpus/lessons/round-76.md` | repaired at `9dea7b2f` | now green (tip run `findings=0`) |

## Checks run

All lane reads are read-only; the clones are under `/fast/scratch/hyaku/kake-r76/ScribeRegistry` and each
asserted its own `--show-toplevel` before any commit.

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git log --oneline -6` | 0 | `7ac91803`, `b8673e87` (tally correction), `9dea7b2f` (lesson corrections + admissible summary receipts), `2cccd59a` (landing), `152bffd5` (A5), `d00ea7fb` (A8) |
| 2 | `cat .ufo/waves/round-76/controls/c1-base-summary.txt` | 0 | `C1v1 revision=master rows=19 receipt_files=10452 spans=30 exempted=0 corrections=0 findings=8 met=false`; `C1v2 revision=a0491fcd rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false` |
| 3 | `cat .ufo/waves/round-76/controls/after-c1-quote-truth-final.txt` | 0 | `C1v2 revision=7ac91803 rows=42 receipt_files=7934 spans=67 exempted=7 corrections=8 findings=0 met=true`; `observed-exit=0` |
| 4 | `cat .ufo/waves/round-76/controls/counter-selftest.txt` | 0 | `selftest: 63/63 passed` |
| 5 | `python3 -B scripts/doc_quote_truth.py --selftest --work <scratch>` | 0 | `selftest: 63/63 passed` (matches the receipt) |
| 6 | `python3 -B scripts/doc_quote_truth.py --root . --revision HEAD --base a0491fcd… --rounds 75,76` | 0 | `C1v2 revision=HEAD rows=42 receipt_files=7934 spans=67 exempted=7 corrections=8 findings=0 met=true`; `sha256sum scripts/doc_quote_truth.py` → `e7f86d3aa0554f61330179f803fcc7624504b2ee63ea2d3e1a9ee5e3427f59ae` |
| 7 | same command at `2cccd59a` (before the lesson repair) | 1 | `rows=42 receipt_files=7929 spans=69 exempted=7 corrections=8 findings=8 met=false` — eight findings: three `T4` on the lesson's `## Corrections` bullets (`:98`, `:103`, `:108`) and `T1` on `quotes=17`, `exact=true`, `findings=8 met=false`, `findings=7 met=false`, `selftest: 47/47 passed` (`:85`, `:92`, `:93`) |
| 8 | `tail -1 .ufo/waves/round-76/controls/after-c2-matrix.txt` | 0 | `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true`; next line `observed-exit=0` |
| 9 | `grep -n 'constant ' .ufo/waves/round-76/controls/after-c2-matrix.txt` | 0 | four lines, each `failed=69/69`, every `passes_all=no` |
| 10 | `cat .ufo/waves/round-76/controls/after-c2-realrun.txt` | 0 | `{"version": 1, "pages": 8, "findings": [], …}` and `rc=0` |
| 11 | `sha256sum scripts/hreflang_audit.py .ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py` | 0 | both `0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac` (59,734 B) |
| 12 | `grep -c '"decided": false' cases/*.json` | 0 | 2 undecided against 71 cases — the landed "three" in SCORECARD's limits paragraph is stale |
| 13 | `grep -c '^| S[0-9]' corpus/SOURCES.md` | 0 | `184` (S444–S446 at lines 190–192) |
| 14 | `python3 -B` over every claim-bearing span in blocks (b) and (d) against the admissible receipt set (round-76 `w1/` and the excluded control names removed) | 0 | `admissible receipt files: 7880`, `missing: 0` |
| 15 | Scratch clone at `2cccd59a` + `controls/r76-base-run.txt`, `controls/scout-verify-output.txt`, `controls/r76-selftest.txt` + a rewritten lesson `## Corrections` (claimy whole lines), counter run | 0 | `C1v2 revision=HEAD rows=41 receipt_files=7933 spans=61 exempted=7 corrections=10 findings=0 met=true` — the repair mechanism the L1 later landed |
| 16 | `python3 -B scripts/hreflang_audit.py` (no `--manifest`) and `… --selftest` (no `--work`) | 64, 64 | `hreflang_audit.py: --manifest is required`; `hreflang_audit.py: --selftest requires --work` |
| 17 | `python3 -B scripts/doc_quote_truth.py --root . --revision HEAD --rounds 75,76` (no `--base`) | 64 | `usage: --base <revision> is required (append-only conjunct)` |

## Findings for the L1

1. **The tip is green, but only after `9dea7b2f`; the pre-repair state was red.** At `2cccd59a` the counter printed `findings=8 met=false` with three `T4` and five `T1` findings, all in `corpus/lessons/round-76.md`; the `selftest: 47/47 passed` claim was also stale against the delivered build's `selftest: 63/63 passed` (checks 5 and 7). Both are closed at `7ac91803`; no action unless the lesson is re-cut.
2. **A correction line only closes a defect when its quoted whole receipt line is itself claim-bearing.** `sha256sum`-shaped lines (`<hex>  -`) and prose lines such as `C1 after receipt — measured …` are not claimy, so quoting them leaves `T4` standing (check 15 measured this directly). The landed `r1-r2-digests-v2.txt` (`counter_sha256=…`, `receipt_sha256=… receipt_bytes=…`) is the form that works.
3. **The before-state receipt the round names is excluded by its own amendment.** A3 §B6 names `controls/base-c1-quote-truth-v2.txt`, and A4/D3 excludes exactly that name from the receipt universe, so the ledger cannot quote its own before-state from it. `controls/c1-base-summary.txt` (landed at `9dea7b2f`) is the admissible carrier; the registry row and the claim table should cite it, not the excluded file.
4. **`undecided` count drifted.** Amendment 6 §E3 and amendment 8 §G3 say three undecidable classes; the admissible matrix receipt over 71 cases records `undecided=2` (check 12). The SCORECARD limits paragraph still says three.
5. **The hreflang selftest tally has no admissible receipt.** `selftest 59/59 passed` exists only in the seat tree (`w1/ExecAuditTool/receipts/selftest.stdout.txt`), which amendment 7 §F1 makes a non-receipt. One committed copy under `controls/` makes the SKILL cell and any SCORECARD row quotable.
6. **`selftest: 63/63 passed` vs `selftest 63/63 passed`.** The tool prints the colon form; the landed SKILL row drops it. Harmless for C1 (SKILL is outside the population) but the registry's self-test cell should match the tool's bytes.

## Pending (filled from wave receipts before landing)

1. `scripts/hreflang_audit.py` selftest tally in a committed receipt (observed in the wave tree: `selftest 59/59 passed`).
2. Round-76 measured revision for the closure; the round-end census line; `w1-results.json` seat total.
3. The routed/residual paragraph and the `## Capabilities` wording if the L1 shortens block (b).
