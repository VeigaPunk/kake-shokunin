# ScribeRegistry — round-76 w1: registry rows, capability row, LOG entry, claim table (draft)

Seat: leaf scribe, read-only. Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`; contract
`.ufo/waves/round-76/contract.md` (frozen at `b758cb04`; base `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`),
amendments 1–8 (`783c7c13`, `e674bc60`, `6b52407b`, `f4f076ba`, `8427d36a`, `d2555766`, `d2555766`,
`d00ea7fb`) and `.ufo/waves/round-76/l1-dispositions.md` read before drafting. Axes named before drafting:
(a) **claim truth** — a cell carries a number only when an admissible committed receipt contains that exact
line, else `pending(L1)`; (b) **shape fidelity** — the registry fence is the 8-column table of `SKILL.md`
`### Round 74/75 gate registry additions`, appended at EOF below the sidecar pin; (c) **supersession
discipline** — no historical cell is rewritten, and each correction names the superseded bytes verbatim
beside the current value and its receipt; (d) **self-application** — every claim-bearing span in the
SCORECARD fences below is either a contiguous substring of a receipt that survives the round's own
receipt-universe rules (amendment 5 §D1–D3, amendment 7 §F1) or the literal `pending(L1)`.

**Admissibility note for the L1 (blocking).** Under amendment 5 §D1 and amendment 7 §F1 the seat tree
`.ufo/waves/round-76/w1/**` is **never** a receipt at this round's measured revision. A receipt that can
carry a round-76 claim-row span must therefore sit in `.ufo/waves/round-76/controls/` (a name that matches
neither `base-c1-quote-truth*` nor `ctl-*`, per §D3), `.ufo/waves/round-76/verification/`, `resid/`,
`frozen/`, `fixtures/` or `cases/`, or in an earlier round's receipt tree. The C2 values below are already
in `controls/after-c2-matrix.txt` and `controls/after-c2-realrun.txt`; the C1 after-state and both selftest
tallies are not yet in an admissible receipt and are marked `pending(L1)`.

No lane file except `.ufo/waves/round-76/w1/ScribeRegistry.md` was created or edited; no `git`/`jj`
mutation was run in the lane; nothing was installed. Scratch `/fast/scratch/hyaku/kake-r76/ScribeRegistry`
(created; used for read-only clone checks and every `--work`; removed before yield).

## (a) `SKILL.md` — `### Round 76 gate registry additions`

Land the bytes inside the fence, unfenced in `SKILL.md`, appended at EOF with one blank line before the
heading (below line 935, the largest `SKILL.md` line pinned in
`corpus/knowledge/freshness-sidecar.json`). Two rows, one per delivered instrument.

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
| scripts/doc_quote_truth.py | gate (live; offline over committed bytes; calibration: every claim-bearing backticked span in the effective claim rows of rounds 75–76 is a contiguous substring of a committed receipt that survives the round's receipt-universe rules — a receipt directory of any round (`controls/`, `verification/`, `resid/`, `receipts/`, `frozen/`, `fixtures/`, `cases/`, `sources/`, `live/`), with the newest measured round's `w1/` seat tree excluded, diagnostic lines stripped and this round's `base-c1-quote-truth*.txt` / `ctl-*.txt` excluded by name — or carries an explicit elision whose non-empty fragments are contiguous inside one receipt, or is closed by a correction line that quotes a whole receipt line and names the defective span; `T1/T2/T4` findings with the `A1` exact-text append-only conjunct; `met = (findings == 0) and append_only`) | `python3 -B scripts/doc_quote_truth.py --root . --revision <rev> --base a0491fcd041cbc3fff2c964ecf6268557e45a5c1 --rounds 75,76` | `0=met` (`findings=0` and `append_only=true`; summary `C1v2 revision=<rev> rows=N receipt_files=N spans=N exempted=N corrections=N findings=0 met=true`); `1=findings` (`met=false`, each finding printed as `<id> <file>:<line> <detail>`); `2=input fault` (`input: <detail>` on stderr — unresolvable revision/base, unreadable claim file); `64=usage` (bad `--rounds`, `--selftest` without `--work`, or a missing `--base`, which the append-only conjunct requires) | `python3 -B scripts/doc_quote_truth.py --selftest --work <dir>` → `selftest: N/N passed`, exit 0 (superset of the v1 counter's 13 fixtures: every finding id red and green, the elision rules, a dispatcher-prose file that must not act as a receipt, an indented table row, a commit-hash span, the append-only conjunct, a valid whole-line correction row; amendment 5 §D5 requires the tally to be produced by a run that executes every case) | predicate frozen in `.ufo/waves/round-76/contract.md` §C1 with amendments 3–5 and 7; base receipt `.ufo/waves/round-76/controls/base-c1-quote-truth-v2.txt` line `C1v2 revision=a0491fcd rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false` (seven `T1` findings); the no-repair control at `f4f076ba` stays red at the same seven findings (`w1/ExecQuoteCounter/receipts/no-repair-controls.txt`); selftest tally `pending(L1)` | read-only (committed bytes at `--revision`; writes only under `--work`) | kake |
| scripts/hreflang_audit.py | gate (live; offline over a versioned manifest of local HTML pages; operability: a frozen ASCII grammar validator for BCP-47-shaped tags — never a BCP-47 validator (amendment 8 §G2) — deciding `hreflang_missing_value`, `hreflang_invalid_tag`, `hreflang_relative_href`, `hreflang_duplicate_pair`, `hreflang_multiple_xdefault` (one per element, amendment 6 §E2), `hreflang_self_missing`, `hreflang_nonreciprocal` (same-tag return required: a lane policy stricter than the S444 missing-return-links rule, amendment 8 §G1; targets outside the manifest are `hreflang_external_target`, severity `info`, exit 0 alone), `hreflang_canonical_not_self` (a non-absolute canonical yields no finding, amendment 6 §E1), with `input_unreadable`/`input_duplicate_url`/`input_url_not_absolute` as faults; no live fetch, headers, rendering, language-truth or search-engine claim) | `python3 -B scripts/hreflang_audit.py --manifest <path> --root <dir> [--json] [--work <dir>]` | `0=clean` (no policy finding; informational findings alone exit 0); `1=policy findings` (any `hreflang_*` policy id); `2=input faults` (`input_*` ids, also when policy findings are present); `64=usage` (missing `--manifest` without `--selftest`, manifest `version` ≠ 1, `--selftest` without `--work`) | `python3 -B scripts/hreflang_audit.py --selftest --work <dir>` → `selftest 59/59 passed`, exit 0 (amendment 2's decided classes plus the amendment 6 rules; tally `pending(L1)` as a committed receipt) | predicate frozen in `.ufo/waves/round-76/contract.md` §C2 with amendments 1, 2, 6 and 8; matrix receipt `.ufo/waves/round-76/controls/after-c2-matrix.txt` line `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true`, the four constants each failing `failed=69/69` decided cases, `observed-exit=0`; real-input receipt `.ufo/waves/round-76/controls/after-c2-realrun.txt` (`"pages": 8`, empty `findings`, `rc=0`) | read-only (writes only under `--work`) | kake |
````

**How to verify.** `python3 -B scripts/doc_quote_truth.py --root . --revision <rev> --base a0491fcd041cbc3fff2c964ecf6268557e45a5c1 --rounds 75,76` must exit 0 with `findings=0`, `append_only=true`, `met=true`; at `a0491fcd` it reproduces the seven findings of `controls/base-c1-quote-truth-v2.txt`. `python3 -B scripts/hreflang_audit.py --manifest <manifest> --root . --json` must decide the matrix's 69 decided cases as `controls/after-c2-matrix.txt` records; `--selftest --work <dir>` must exit 0.

## (b) `SCORECARD.md` — capabilities-table row

One row for the `## Capabilities` table (4 columns, same shape as the round-61/64 rows). Contract §C2 kill
rule 3 gates it on the real-input run, which exists (`controls/after-c2-realrun.txt`).

````markdown
| Offline hreflang declaration audit | Reads a version-1 manifest of local HTML pages and reports, read-only and network-free, missing or malformed hreflang values under a frozen ASCII grammar validator for BCP-47-shaped tags, relative alternate hrefs, duplicate tag/href pairs, multiple x-default declarations (one finding per element), a page that omits its own URL from its alternates, non-reciprocal manifest-internal targets under a same-tag lane policy that is stricter than the S444 missing-return-links rule (external targets informational), and a canonical that is not the page's own URL (clean / policy findings / input faults, exits 0/1/2/64); no live fetch, headers, rendering, language-truth or search-engine claim | `scripts/hreflang_audit.py`; matrix `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true` with `observed-exit=0` (`.ufo/waves/round-76/controls/after-c2-matrix.txt`); real-input run over 8 retained served pages, `rc=0` and empty findings (`.ufo/waves/round-76/controls/after-c2-realrun.txt`) | 76 |
````

## (c) `LOG.md` — round-76 entry

Append at EOF. `pending(L1)` marks a cell whose receipt does not exist yet; a number not present in a
receipt is never written.

````markdown
## Round 76 — 2026-11-03 (hyaku run 15; attempt 1; Linux host; claims frozen before any seat ran)

- **Frozen contract.** `.ufo/waves/round-76/contract.md` at `b758cb040d53374b1b63b89702c7128f77212d23`, base `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`, the v1 counter `.ufo/waves/round-76/c76_quote_truth.py` (selftest 13/13) and five red controls. Amendments 1–8 are terms-only, each recorded before the after-state it binds: A1 fixes the real-input population at the 8 retained served pages; A2 decides the classes the contract left undecidable; A3 splits revision citations from digests, dedupes the population, makes correction closure whole-line and append-only exact-text; A4 excludes this round's own diagnostic controls by name; A5 excludes the newest measured round's seat tree and strips diagnostic lines, and requires a selftest that executes every case; A6 fixes per-element `hreflang_multiple_xdefault` and non-absolute canonical handling; A7 limits the seat-tree exclusion to the newest measured round; A8 declares the same-tag reciprocity rule a lane policy stricter than S444 and the tag grammar a frozen ASCII validator, not BCP-47.
- **Motivating evidence.** C1 is claimed on calibration (score 2, the lane's lowest non-retired axis): at `a0491fcd` the delivered counter prints `C1v2 revision=a0491fcd rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false`, exit 1 (`.ufo/waves/round-76/controls/base-c1-quote-truth-v2.txt`) — the round-75 ledger's elided quotes plus five SCORECARD spans. C2 is claimed on operability as capability acquisition: the lane holds no hreflang instrument at the base.
- **Wave `w1`.** One v1 wave; `w1-spec.json` carries 15 seat items (scout 2, executor 5, scribe 2, reviewer 2, critic 1, mutation-tester 1, connector 1, sentinel 1); attack seats 4/15 = 26.7 %; the L1 held the planner seat (the validator rejects a planner role). Spec `w1-spec.json`, dispatch `w1-dispatch.json`, ready `w1.ready`, registry `w1/swarm-registry.json`.
- **C1 landed and measured.** The delivered counter is `scripts/doc_quote_truth.py`; the wave's build `302bcb9b…` prints `findings=0 met=true` at the tip, while the build first copied into `scripts/` (`eae3ce48…`) is the one amendment 7 names as red, so the L1 ships the wave build and records its selftest. Seven whole-line correction rows close the seven base findings — five in `SCORECARD.md` `## Round 75 — quote corrections (appended round 76)`, one in `corpus/QUALITY.md` `## Round-76 criterion — quoted receipts are whole`, one in `corpus/lessons/round-75.md` `## Corrections`; no historical line is rewritten (44 insertions, 0 deletions across the three files, `w1/ExecQuoteRepair/receipts/03-append-only-numstat.txt`). After-state at the measured revision and the counter selftest tally: `pending(L1)`.
- **C2 landed and measured (capability).** `scripts/hreflang_audit.py` (59,734 bytes, sha256 `0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac`; selftest `selftest 59/59 passed` in the wave tree, committed tally `pending(L1)`), manifest v1 `{"version":1,"pages":[{"id","file","url"}]}`. Matrix over 71 cases: `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true`, `observed-exit=0` (`.ufo/waves/round-76/controls/after-c2-matrix.txt`); the four constants (no-op, always-clean, report-all, empty-list) each fail `failed=69/69` decided cases. Real-input run over the 8 retained served pages (amendment 1): `"pages": 8`, empty `findings`, `rc=0` (`.ufo/waves/round-76/controls/after-c2-realrun.txt`); the four not-served surfaces are reported as not-served, never counted clean. The two undecided cases are amendment 8 §G3's contract defects, excluded from the score.
- **Corrections (round-75 closure R1/R2/R3; append-only, no historical line edited).**
  - **R1 — stale counter digest, `LOG.md:2534`.** Superseded text: `` `c75_row_truth.py` (frozen v0 → hardened `0699a672…`, selftest 29/29) `` — `0699a672…` is the blob at `4e3fc159`. Current value: `63e321b28e509781405f1b4209a66b99460bc2512c92a8615fec06f2423e944b` for `.ufo/waves/round-75/c75_row_truth.py`, re-derived at `a0491fcd` by `git show a0491fcd:.ufo/waves/round-75/c75_row_truth.py | sha256sum` (`.ufo/waves/round-76/controls/r1-r2-digests.txt`), and identical to the `counter_sha256=` line of `.ufo/waves/round-75/controls/after-c1-row-truth.txt:2`.
  - **R2 — stale receipt digest, `LOG.md:2535`.** Superseded text: `` (18 entries, `f3128628…`, 3,793 B) `` — `f3128628…` is the cut at `4e3fc159`. Current value: `15768f81460bcbf991bacf9ffdf6a2145d32f4de7d952f52526589d8013e6613`, 3,793 bytes for `corpus/knowledge/instrument-receipts.json`, re-derived at `a0491fcd` by `git show a0491fcd:corpus/knowledge/instrument-receipts.json | sha256sum` and `| wc -c` (`.ufo/waves/round-76/controls/r1-r2-digests.txt`), and identical to the `receipt_sha256=… receipt_bytes=` line of `.ufo/waves/round-75/controls/after-c2-receipts.txt:2`.
  - **R3 — disagreeing revision labels.** Superseded text: the round-75 report's table header `` | Claim | Counting command | Before (base `c9c5e484`) | After (tip `6c10b433`) | `` (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-75/kake.md:85`), while every after cell and the receipt it cites name `f87d14a9`; and the tip paragraph's `` the receipt commit that follows the measured revision `3ae076ab` `` (same file, line 10). Current value, one measured revision per artifact: C1 `C1 after receipt — measured 2026-11-04T00:22:37Z at f87d14a949e1b5f8b4ec5807b75f22aa3e337353` (`.ufo/waves/round-75/controls/after-c1-row-truth.txt:1`); C2 `C2 after receipt — carrier f87d14a949e1b5f8b4ec5807b75f22aa3e337353 (2026-11-04T00:22:30Z)` (`.ufo/waves/round-75/controls/after-c2-receipts.txt:1`); the harm battery names its own tree `== harm battery at 306fff49b3a64bc32bb468f6c26fb4b577ac0c4a` (`.ufo/waves/round-75/controls/after-harm-battery.txt:1`) and its complete bytes are committed at `0df52aed` (`git log --oneline -- .ufo/waves/round-75/controls/after-harm-battery.txt` → `0df52aed round-75: final harm-battery receipt bytes`).
- **Frontier and sources.** `corpus/SOURCES.md` 181 → 184 rows: S444 (Google, localized versions), S445 (WHATWG HTML, `hreflang` and link type `alternate`) and S446 (RFC 5646) opened this round, retained under `.ufo/waves/round-76/w1/ScoutHreflangSources/`; new entry `corpus/knowledge/hreflang-declaration.md` cites them. Census before: 181 rows, exit 0 (`.ufo/waves/round-76/controls/census-before.txt`); round-end census `pending(L1)`. Assimilation: none — `w1/ConnectorOverlap.md` finds no sibling holds an hreflang audit and every `merge/kake/` locator still fails to re-ground. `considerthese/2026-10-26.md` proposal 5 stays as its round-66 adoption, not re-mined.
- **Routed (not claimed).** `pending(L1)`: the wave's residuals (the two undecidable matrix classes, the pinned-build split in the real-input run) and the five round-75 items the L1 disposition ledger leaves open (R4 sidecar instruments unbound, Q1 E2 multi-pair semantics, Q3 receipt-schema decision, Q4 host-absolute path hygiene).
- **Not done this round.** No publish or deploy; no MANIFEST edit; no tool installed or upgraded; pacman untouched.
````

## (d) `SCORECARD.md` — round-76 claim table

Same shape as the round-74/75 sections. Every claim-bearing span below is a contiguous substring of a
receipt that survives the round's receipt-universe rules, or the literal `pending(L1)`.

````markdown
## Round 76 — declared and measured claims (attempt 1; author-side, admission belongs to the closure)

Frozen contract `.ufo/waves/round-76/contract.md` (`b758cb04`), amendments 1 (`783c7c13`), 2 (`e674bc60`),
3 (`6b52407b`), 4 (`f4f076ba`) and 5–8, each terms-only and recorded before the after-state it binds. Base
`a0491fcd041cbc3fff2c964ecf6268557e45a5c1`; measured at `pending(L1)`. Wave `w1`: one v1 wave, 15 seat
items (scout 2, executor 5, scribe 2, reviewer 2, critic 1, mutation-tester 1, connector 1, sentinel 1;
attack share 4/15 = 26.7 %). Scores unchanged: operability 10, freshness 10, calibration 2 (all HOLD; no
scalar move).

| Claim | Axis | Before → after | Counting command | Verdict |
|---|---|---|---|---|
| C1 claim rows quote only committed receipts | calibration 2→2 HOLD | base `a0491fcd` → after: `pending(L1)` (both run lines; see Pending 1) | `python3 -B scripts/doc_quote_truth.py --root . --revision <rev> --base a0491fcd041cbc3fff2c964ecf6268557e45a5c1 --rounds 75,76` | `pending(L1)` |
| C2 offline hreflang declaration audit on a versioned manifest | operability 10→10 HOLD (capability) | base `a0491fcd`: no hreflang instrument → matrix over 71 cases: `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true`, `observed-exit=0` (`.ufo/waves/round-76/controls/after-c2-matrix.txt`); real-input run on 8 retained served pages: `rc=0`, empty findings (`.ufo/waves/round-76/controls/after-c2-realrun.txt`) | `python3 -B .ufo/waves/round-76/w1/ExecAuditMatrix/c76_hreflang_matrix.py --root . --tool scripts/hreflang_audit.py --revision <rev> --work <scratch>` | measured met; the four constants each fail `failed=69/69` decided cases; 2 contract-undecidable cases excluded, never counted as passes |

### Capabilities acquired in round 76

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Offline hreflang declaration audit | `pending(L1)` (the same row as `SCORECARD.md` `## Capabilities`; see block (b)) | `scripts/hreflang_audit.py`; matrix `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true` with `observed-exit=0` (`.ufo/waves/round-76/controls/after-c2-matrix.txt`); real-input `rc=0` on 8 retained served pages (`.ufo/waves/round-76/controls/after-c2-realrun.txt`) | 76 |

Move log (round 76):
| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 76 | calibration (HOLD 2) | `pending(L1)` (the base run line; see block (d)) | `pending(L1)` | `scripts/doc_quote_truth.py`, `pending(L1)` |
| 76 | operability (HOLD 10) | no hreflang instrument in `scripts/` | `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true` | `scripts/hreflang_audit.py`, `.ufo/waves/round-76/controls/after-c2-matrix.txt`, `.ufo/waves/round-76/controls/after-c2-realrun.txt` |

Stated limits, not claimed closed: the audit is offline and declaration-only (no live fetch, no HTTP
headers/`Vary`, no rendering or JavaScript, no claim about the actual language of any page, no search-engine
selection or ranking claim); the tag grammar is a frozen ASCII validator for BCP-47-shaped tags and rejects
grandfathered, extlang and extension-singleton forms, so it is not a BCP-47 validator; the same-tag
reciprocity rule is a lane policy that flags strictly more than the S444 missing-return-links rule, and no
finding is a claim that Google would flag the page; two matrix cases remain contract-undecidable and are
excluded rather than scored; the retained real-input corpus declares hreflang on one page only, so the run
exercises the parser and the self/duplicate/canonical conditions but cannot discriminate
`hreflang_nonreciprocal` or `hreflang_external_target` on real bytes; the four not-served surfaces are
reported, not audited.
````

## Checks run

All lane reads are read-only; the one clone (check 20) is under `/fast/scratch/hyaku/kake-r76/ScribeRegistry`
and asserts its own `--show-toplevel` before any commit.

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git log --oneline -8` | 0 | freeze `b758cb04`; amendments `783c7c13`, `e674bc60`, `6b52407b`, `f4f076ba`, `d2555766` (A6/A7), `d00ea7fb` (A8); repair `442d36c6` |
| 2 | `sed -n '1,2p' .ufo/waves/round-75/controls/after-c1-row-truth.txt` | 0 | `C1 after receipt — measured 2026-11-04T00:22:37Z at f87d14a949e1b5f8b4ec5807b75f22aa3e337353`; `counter_sha256=63e321b28e509781405f1b4209a66b99460bc2512c92a8615fec06f2423e944b` |
| 3 | `sed -n '1,2p' .ufo/waves/round-75/controls/after-c2-receipts.txt` | 0 | `C2 after receipt — carrier f87d14a949e1b5f8b4ec5807b75f22aa3e337353 (2026-11-04T00:22:30Z)`; `receipt_sha256=15768f81460bcbf991bacf9ffdf6a2145d32f4de7d952f52526589d8013e6613 receipt_bytes=3793` |
| 4 | `grep -n '0699a672\|f3128628' LOG.md` | 0 | lines 2534 and 2535 carry the superseded digests quoted in (c) |
| 5 | `grep -n 'After (tip\|3ae076ab' /home/vgpnk/Projects/shokunin/.ufo/reports/round-75/kake.md` | 0 | table header at line 85; tip paragraph at line 10 |
| 6 | `git log --oneline -- .ufo/waves/round-75/controls/after-harm-battery.txt` | 0 | `0df52aed round-75: final harm-battery receipt bytes` |
| 7 | `cat .ufo/waves/round-76/controls/r1-r2-digests.txt` | 0 | `63e321b2…` for `c75_row_truth.py`; `15768f81…` and `3793` for `instrument-receipts.json`, both re-derived at `a0491fcd` |
| 8 | `python3 -c` over `w1-spec.json` (`role` counts) and `w1-dispatch.json` `counts` | 0 | 15 items (scout 2, executor 5, scribe 2, reviewer 2, critic 1, mutation-tester 1, connector 1, sentinel 1); `spawn=15 resume=0 total=15` |
| 9 | `tail -1 .ufo/waves/round-76/controls/after-c2-matrix.txt` | 0 | `cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true`; next line `observed-exit=0` |
| 10 | `grep -n 'constant ' .ufo/waves/round-76/controls/after-c2-matrix.txt` | 0 | four lines, each `failed=69/69`, every `passes_all=no` |
| 11 | `cat .ufo/waves/round-76/controls/after-c2-realrun.txt` | 0 | `{"version": 1, "pages": 8, "findings": [], …}` and `rc=0` |
| 12 | `sha256sum scripts/hreflang_audit.py .ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py` | 0 | both `0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac` (59,734 B) |
| 13 | `sha256sum scripts/doc_quote_truth.py .ufo/waves/round-76/w1/ExecQuoteCounter/doc_quote_truth.py` | 0 | `eae3ce48a78a328e89389fb690b64965a01945e5510d3a2084625721de793b54` (44,101 B) vs `302bcb9bc8faa4dace522602416e0ca9c5e42fdbc6bcc40d4f4db94b6468ebf7` (47,511 B) — the landed copy is the older build |
| 14 | `python3 -B scripts/doc_quote_truth.py --root . --revision d00ea7fb --base a0491fcd… --rounds 75,76` | 1 | `C1v2 revision=HEAD rows=23 receipt_files=7726 spans=41 exempted=7 corrections=7 findings=2 met=false` (the older build reds the two round-75 lesson rows amendment 7 names) |
| 15 | `python3 -B .ufo/waves/round-76/w1/ExecQuoteCounter/doc_quote_truth.py --root . --revision d00ea7fb --base a0491fcd… --rounds 75,76` | 0 | `C1v2 revision=HEAD rows=23 receipt_files=7925 spans=41 exempted=7 corrections=7 findings=0 met=true` |
| 16 | `python3 -B .ufo/waves/round-76/w1/ExecQuoteCounter/doc_quote_truth.py --selftest --work <scratch>` | 0 | `selftest: 57/57 passed` (scribe check on the wave build; the committed tally is `pending(L1)`) |
| 17 | `grep -c '^| S[0-9]' corpus/SOURCES.md` | 0 | `184` (S444–S446 present at lines 190–192) |
| 18 | `python3 -B` over every claim-bearing span in blocks (b) and (d) against the admissible receipt set (round-76 `w1/` and the excluded control names removed) | 0 | `admissible receipt files: 7880`, `missing: 0` |
| 19 | `python3 -B scripts/doc_quote_truth.py --root . --revision HEAD --rounds 75,76` (no `--base`) and `… --selftest` (no `--work`) | 64, 64 | `usage: --base <revision> is required (append-only conjunct)`; `usage: --selftest requires --work <dir>` |
| 20 | `python3 -B scripts/hreflang_audit.py` (no `--manifest`) and `… --selftest` (no `--work`) | 64, 64 | `hreflang_audit.py: --manifest is required`; `hreflang_audit.py: --selftest requires --work` |
| 21 | Scratch clone at `d00ea7fb` + the five new `controls/` files committed + block (d) appended to `SCORECARD.md`, then the wave-build counter at that commit | 0 | `C1v2 revision=HEAD rows=28 receipt_files=7929 spans=51 exempted=7 corrections=7 findings=0 met=true` — the draft's own rows stay green under the delivered predicate |

## Findings for the L1 (blocking or near-blocking)

1. **Ship the wave build of the counter.** `scripts/doc_quote_truth.py` is build `eae3ce48…` (44,101 B), the build amendment 7 names as printing a wrong base count; at `d00ea7fb` it prints `findings=2 met=false` (check 14), while the wave file `302bcb9b…` (47,511 B) prints `findings=0 met=true` (check 15). Nothing else in this draft depends on which build ships, but the C1 after-state does.
2. **Admissible receipts for the C1 run lines.** Under amendment 5 §D1 and amendment 7 §F1 the round-76 `w1/` tree is never a receipt, and §D3 excludes `base-c1-quote-truth*.txt` and `ctl-*.txt` in this round's `controls/`. The base line (`C1v2 revision=a0491fcd rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false`) and the after line (`… exempted=7 corrections=7 findings=0 met=true`) therefore need one committed copy under `.ufo/waves/round-76/controls/` whose name matches neither pattern — `after-c1-quote-truth.txt` carrying both runs is the smallest form; the row's two `pending(L1)` cells then quote those two lines.
3. **Matrix numbers moved between receipts.** `w1/ExecAuditMatrix/receipts/matrix-run-execaudittool.txt` records 69 cases / 66 decided / 3 undecided; the admissible `controls/after-c2-matrix.txt` records 71 / 69 / 2 with all four constants at `failed=69/69`. This draft uses the admissible one; do not mix the two in one row.
4. **Selftest tallies need committed receipts.** `selftest: 57/57 passed` (counter, wave build) and `selftest 59/59 passed` (hreflang, same sha as the landed copy) exist only in the seat tree today; a committed copy under `controls/` (e.g. `selftest-both.txt`) makes them quotable in the SCORECARD rows and in the SKILL rows' proof cells.
5. **The capability table's placement.** `### Capabilities acquired in round 76` sits inside the `## Round 76` section, so its rows are in the C1 population; its evidence cell therefore quotes only `controls/` values. The `## Capabilities` row (block b) is outside every `## Round <N>` section and is not scanned.
6. **One QUALITY risk outside this seat.** The unlanded `blocks-quality.md` bullet carries the reject example `files=18 mismatches=0 append_only=true met=true missing_frozen=0`, a base `T1` finding. It passes only because the literal word `supersedes` inside a code span makes the counter classify that bullet as a correction line (B3-bis then exempts the base finding). If that word is edited out when the block lands, C1 reds on that bullet; a whole-line quote or an explicit `[r76-correction …]` marker removes the accident.

## Pending (filled from wave receipts before landing)

1. C1 base and after run lines in an admissible receipt (`controls/after-c1-quote-truth.txt`), then paste both into block (d)'s C1 row and the calibration move-log row.
2. `scripts/doc_quote_truth.py` selftest tally in a committed receipt (observed on the wave build: `selftest: 57/57 passed`, check 16).
3. `scripts/hreflang_audit.py` selftest tally in a committed receipt (observed in the wave tree: `selftest 59/59 passed`).
4. Round-76 measured revision; the `## Capabilities` row's wording if the L1 shortens block (b).
5. `w1-results.json` seat total, the round-end census line, and the routed/residual paragraph.
