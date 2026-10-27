# ScribeC1Section

Claim C1 prose. Two drafts and one prose-grounding receipt, written under
`.ufo/waves/round-60/w1/ScribeC1Section.files/`. Nothing else in the lane touched: no lane file, no
jj/git mutation, no fleet-root write, no pacman, no tool install. No after-state scored and no counter
run — `c60_gate_status.py` does not exist at this revision, so every verdict in the drafts is stated as
the frozen predicate + a command, not as a measured result.

## SKILL SECTION:

`.ufo/waves/round-60/w1/ScribeC1Section.files/skill.md` (85 lines) — `### Round 60 gate-status ledger`,
written to be appended to `SKILL.md` after `### Round 59 gate registry additions` (the current tail,
`SKILL.md:1297-1309`); the heading text is exactly the seat spec's, and `grep -n 'Round 60\|Round-60'
SKILL.md` returns nothing, so it collides with no existing section.

Content, in the lane's registry-prose voice:

1. **Framing.** A view over the registry rows, not a second registry: the label the counter reads lives
   in the row's `Kind` cell (`contract.md:59-61`), so a ledger row that disagrees with its `Kind` cell is
   a finding. Receipt discipline named: `--json` report committed once under
   `.ufo/waves/round-60/controls/`, never rewritten, no placeholder.
2. **The three labels.** `live` = neither marker, must exit 0 at the measured revision
   (`live_not_green`); `historical` = the word `historical` in the `Kind` cell, green at its pin and red
   later by design, with this lane's actual freeze kinds named (mirror row counts 148/156/158/158+2/160,
   the round-55 byte-prefix rule, the round-57 frozen file set with `new_receipts == 3`); `never met` =
   the words `never met`, spelled **with a space** because the parse is a substring — `never-met` parses
   as `live`, the class the base shows twice (`c53_gate_truth.py` live/exit 1, `c57_idresolver_gate.py`
   live/exit 2 without `--fleet`, per the L1 base probe) and the registry had no word for. Whether either
   row is relabelled is left to the measured run, not to the prose.
3. **The pin rule.** Pin = first 40-hex revision in the `Kind` cell; = the last revision the command was
   observed to exit 0 at (for a gate this round reddens, the last revision before the change); must be an
   ancestor of the measured revision (`pin_not_ancestor`), absent → `unpinned`; a `never met` pin is the
   revision the red was measured at; pin says *when*, `Pinned values / frozen proof` still says *what*; a
   pin is not evidence of green until run.
4. **Relabel duty (R59-D1).** Prospective: before the contract freezes, every non-`historical` row runs
   on a scratch draft of the after-state; a gate the claim must redden is named in the contract with its
   disposition (historical + pin, or claim reshaped), else the contract says why and the red stands as a
   counted mismatch. Round 59 as the counterexample (`c55_readme_index` `head_changed=1`, H1 prediction,
   marking after the fact, `ReviewerNoHarm.md`), with the explicit rule that a relabel landing after the
   counter scored is a second defect and a relabel used to launder a red is worse. Round 60's own
   instance is spelled out with arithmetic: S427–S429 make 167 registry rows where the live
   `crawler-identity-quote-truth-counter` requires `registry rows == mirror rows + 2` (162 + 2 = 164), so
   it goes `historical` at its measured revision before the after-state is measured.
5. **What the labels do not claim.** Not verdict-map truth beyond `0=`/`1=`, not the pin's provenance
   (`contract.md:84-85`); `unrun` is a state, never a cell filled from memory.
6. **The table — header only, as instructed**, 7 columns: `Gate (registry row name) | Label | Pin —
   first 40-hex in the Kind cell | Exit at pin | Exit at the measured tree | Why red by design (or why
   live) | Re-labelled`. No body rows; the paragraph under it tells the L1 to add one row per population
   member (28 at base) and per non-population gate that can go red on growth, from the counter's report
   and `SCORECARD.md`, never from the prose.

**C1-safety decision worth the L1's attention.** The ledger's first three header cells are deliberately
**not** `Name` / `Kind` / `Entry command`, and the prose says so. `c60_gate_status.py`'s row rule keys on
exactly those three header cells (`contract.md:55-58`), so a ledger row can never be read as a registry
row — otherwise the ledger would duplicate all 28 members and every one would score `duplicate_row`.
For the same reason the ledger names gates by registry row name, never by counter path.

## QUALITY:

`.ufo/waves/round-60/w1/ScribeC1Section.files/quality.md` (34 lines) — one criterion under a new
`## Round-60 criteria` heading, to be appended at the `QUALITY.md` tail after the round-59 section
(`corpus/QUALITY.md:1317-1358`; file is 1358 lines at the base). Lane style kept: bold lead sentence,
evidence prose, `Grounding:` with resolving pointers, `Falsifier:` command, `Example that fails it:`.

Criterion: **a gate's status label is re-derived from a run at the revision being measured, and a round
that reddens a live gate relabels it with its pin before the counter scores.** Evidence used: 12 of 28
population members unregistered at base; the two live reds; the `never met` spelling trap; round 59's
`readme-index-counter` relabel as the trade's only record; round 60's S427–S429 arithmetic. Falsifier:
`c60_gate_status.py --root . --revision <rev>` must print `members=28 mismatches=0 scores_held=3
met=True`, base exits 1, and the score-only mutant (calibration 2 → 10) must fail `scores_held`.
Examples that fail it: a `Kind` cell reading `never-met`; a `historical` row whose pin is a later commit.

Grounding requested by the seat spec is carried in the criterion: `corpus/lessons/round-60.md` §Mistakes
(gate-collision; status label) plus the round-59 gate-collision row.

## GROUNDING:

Every cited fact, with the pointer I checked it at (base revision `97cdc122379711c2b02a8970752c8782da3ac81d`):

| Fact as written | Pointer | How checked |
|---|---|---|
| population = 28 paths, `48 <= N <= 59` | `.ufo/waves/round-60/contract.md:49-53` | read; re-derived 28 files by `git ls-tree -r 97cdc122` + the contract regex |
| earliest three labels / `Kind`-cell parse | `contract.md:59-61` | read |
| pin = first 40-hex in `Kind`, must be ancestor | `contract.md:60-61` | read; 7/7 historical pins return `merge-base --is-ancestor` = 0 at base |
| mismatch classes named | `contract.md:64-71` | read |
| `scores_held == 3` (10, 10, 2) | `contract.md:72-73` | read |
| frozen predicate, kill rule, counter CLI | `contract.md:75-77` | read |
| 12 unregistered members; `c53_gate_truth` live exit 1; `c57_idresolver_gate` live exit 2 without `--fleet` | `contract.md:78-81` (L1 base probe) | unregistered list **re-derived by me** (12, same list); the two exit values are **cited, not run** |
| do-nothing control ≥ 13 mismatches; `historical_but_green`, `pin_not_ancestor`, `scores_held` mutants | `contract.md:82-83` | read |
| counter does not test verdict-map truth or pin provenance | `contract.md:84-85` | read |
| C3's appended rows may redden a population counter; honest relabel required | `contract.md:44-45` | read |
| R59-D1 routing (C2 + C1) | `contract.md:22-24` | read |
| 28 base members, 16 registered, 7 historical, 9 live, 12 unregistered | `.ufo/waves/round-60/w1/ScribeC1Section.files/base-label-evidence.txt` | my own read-only derivation from `git show 97cdc122:SKILL.md`, row rule per `contract.md:55-58` |
| `c53_gate_truth.py` row is `live` | `SKILL.md:213` | read at base blob |
| c52 quote-truth historical, 148-row mirror | `SKILL.md:1216` | read at base blob |
| `readme-index-counter` historical from r59, byte-prefix `head_changed`, cites `ReviewerNoHarm.md` | `SKILL.md:1233` | read at base blob |
| c55 quote-truth historical, 156 rows | `SKILL.md:1234` | read |
| c56 quote-truth historical, 158 rows | `SKILL.md:1254` | read |
| `receipt-pin-counter` historical, frozen file set, `new_receipts == 3` | `SKILL.md:1273` | read |
| `id-resolver-gate` row is `live` | `SKILL.md:1274` | read |
| c57 quote-truth historical, 158 + 2 | `SKILL.md:1275` | read |
| c58 quote-truth historical, 160-row mirror, r59 grows registry to 164 | `SKILL.md:1295` | read |
| round-59 rows 1307–1309; `crawler-identity-quote-truth-counter` is `live` | `SKILL.md:1307-1309` | read (1309 Kind cell has neither marker) |
| registry = 164 rows at base | `corpus/SOURCES.md` at `97cdc122` | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 164 |
| c59 C8 arithmetic `registry rows == mirror rows + 2` | `.ufo/waves/round-59/c59_quote_truth.py:595-598`, `:93` (`NEW_ROWS = ("S425", "S426")`) | read |
| c59 mirror = 162 rows, 150968 bytes | `.ufo/waves/round-59/assimilation/mirror-pin.json` at `97cdc122` | read; 162 rows counted in the mirror blob |
| round-59 gate-collision mistake row | `corpus/lessons/round-59.md:175` | read (class `gate-collision`, H1 `ExecHistoricalGates.md`, build `ab6e100e`, `a2r1/ReviewerNoHarm.files/out-c55.txt`) |
| R59-D1 as routed | `corpus/lessons/round-59-verifier-spotcheck.md:135-137` | read |
| round-59 criterion "A frozen claim never silently turns a standing gate red" | `corpus/QUALITY.md:1350-1358` | read |
| round-58 criterion "A gate that cannot be green on any later tree is registered as historical at its measured revision" | `corpus/QUALITY.md:1289-1300` | read |
| proposal 5, historical-gate list | `considerthese/2026-10-26.md:33` | read (quoted verbatim in the section) |
| QUALITY.md tail ends at the round-59 section | `corpus/QUALITY.md:1317-1358` | `wc -l` = 1358 |
| no `Round 60` heading exists yet in SKILL.md | `SKILL.md` (whole file) | `grep -n 'Round 60\|Round-60'` → no match |

## Findings / dependencies for the L1

- **Lesson pointer is forward.** `corpus/lessons/round-60.md` does **not** exist at base (`ls
  corpus/lessons/` has no round-60 file; checked twice during this seat). The criterion's primary pointer
  is therefore valid only once the lesson seat's `## Mistakes` draft lands. Two already-committed anchors
  sit beside it in the same `Grounding:` run (`corpus/lessons/round-59.md:175`, `corpus/QUALITY.md`
  round 59), so the criterion keeps a resolving path either way — but if the lesson lands without a
  gate-collision / status-label row, the first pointer dangles and the criterion should be re-pointed.
- **Ledger fill order.** `Label`, `Pin`, `Exit at pin` can only be filled from the version-1 counter's
  `--json` report; `Exit at the measured tree` needs the measured revision fixed first. `base-label-evidence.txt`
  is a starting point, not the fill: it parses one line per row and does not apply the contract's
  fenced-block/HTML-comment exclusions or the command-placeholder rules.
- **Relabel is a registry edit, not a ledger edit.** S427–S429 force the round-59 quote-truth row to
  `historical`; if the L1 instead keeps it `live`, C1 scores `live_not_green` on the measured tree, which
  is the honest outcome the contract allows (`contract.md:44-45`) as long as the contract says why.
- **Not mine to decide, flagged:** whether `c53_gate_truth.py` / `c57_idresolver_gate.py` become
  `never met` — the label needs a pin where the command is red, so it follows the measured run; the
  section states the label's meaning and leaves the call to the run.
- Unrun by me, on purpose: `c60_gate_status.py` (absent), any population counter, any selftest. Both
  drafts are prose; their falsifiers are stated as commands, not as results.

## Artifacts

- `.ufo/waves/round-60/w1/ScribeC1Section.files/skill.md` (85 lines)
- `.ufo/waves/round-60/w1/ScribeC1Section.files/quality.md` (34 lines)
- `.ufo/waves/round-60/w1/ScribeC1Section.files/base-label-evidence.txt` (35 lines: 5 header lines, a
  summary line, 28 member rows)
- scratch `/fast/scratch/hyaku/kake-r60/ScribeC1Section/` created and removed; nothing cited from it

VERDICT: Both prose drafts are in the lane's own register and grounded line-by-line; the ledger is a header-only 7-cell table shaped so it cannot register as a duplicate row, and the relabel duty is stated prospectively with round 60's S427–S429 case spelled out arithmetically.
