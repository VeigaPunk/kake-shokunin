# kake round 76 — frozen claim contract (attempt 1)

Frozen at lane tip `a0491fcd041cbc3fff2c964ecf6268557e45a5c1` (base for every before-state) before any
seat ran. Amendments are separate files, terms-only, and recorded before any after-state.

Round shape: ONE v1 wave (`w1`), 14 seats, ≥25 % attack share. The L1 holds the planner seat; a bounded
planning data-walk rides scout/connector items (validator refuses `planner`).

## C1 — calibration (owned score 2, the lane's lowest non-retired axis)

**Claim sentence (one).** A round's claim rows stop quoting command output that no committed receipt
contains: every claim-bearing backticked span in the effective claim rows of rounds 75–76 is a contiguous
substring of a committed receipt, or carries an explicit elision whose fragments are contiguous, or is
closed by a correction line that itself quotes a validated receipt line and names the defective span.

**Counter** `.ufo/waves/round-76/c76_quote_truth.py` (v0, the L1's; the wave hardens it into
`scripts/doc_quote_truth.py` with the same predicate and a superset selftest).

```sh
python3 -B scripts/doc_quote_truth.py --root . --revision <rev> --base a0491fcd --rounds 75,76
```

**Population.** Claim rows: markdown table data rows inside a `## Round <N>` section of `SCORECARD.md`
(headers and separator rows excluded); bullets inside `## Round-<N> criterion` sections of
`corpus/QUALITY.md`; table data rows and bullets inside `## Mistakes` / `## Gate` / `## Claims` /
`## Corrections` of `corpus/lessons/round-<N>.md`. N ∈ {75, 76}.

**Claim-bearing span.** A backticked span of a claim row carrying an observed-value shape: `token=value`,
`exit <n>`, an `a/b` tally, or a 7–64 char lowercase hex token. Command lines, CLI flags and path tokens
are never claim-bearing.

**Receipt universe.** Committed files at the measured revision under `.ufo/waves/**` that are observed data:
any file inside a `controls/`, `verification/`, `resid/`, `receipts/`, `frozen/`, `fixtures/` or `cases/`
directory, plus `.txt/.json/.csv/.tsv/.log/.out/.ndjson` files outside them. Dispatcher artifacts
(`*-results.json`, `*-dispatch.json`, `*-spec.json`, `swarm-registry.json`, `*.ready*`) are never receipts,
so a seat's own prose can never make a bad quote contiguous.

**Findings (stable ids).**
- `T1` span absent from every receipt.
- `T2` elided span whose non-empty fragments are not all contiguous inside one receipt file.
- `T4` correction line (`[rNN-correction` or `supersedes`) that carries no validated receipt quote.
- `A1` claim row present at `--base` and gone at the measured revision (append-only conjunct).

`met = (findings == 0) and append_only`. Exit 0 met, 1 findings, 2 input fault, 64 usage (`--base`
required).

**Before (measured at base, committed).** `rows=19 receipt_files=10452 spans=30 exempted=0 corrections=0
append_only=true findings=8 met=false`, exit 1 — `controls/base-c1-quote-truth.txt`. The eight findings are
the round-75 ledger's elided quotes (the closure's R6 twice, plus six SCORECARD spans).

**Target after.** `findings=0 append_only=true met=true`, exit 0, over the same population, closed by
appended correction rows that quote whole receipt lines. A deletion or a rewrite is never the repair.

**Controls (committed before freezing, all red).**
| Control | Receipt | Observed |
|---|---|---|
| do-nothing (base tree, nothing added) | `controls/ctl-do-nothing.txt` | `findings=8 met=false`, exit 1 |
| junk correction (supersedes with no quote) | `controls/ctl-junk-correction.txt` | `findings=9` incl. `T4`, exit 1 |
| laundering (validated quote that names no defective span) | `controls/ctl-launder.txt` | `corrections=1 exempted=0 findings=8`, exit 1 |
| deletion (defective row removed) | `controls/ctl-deletion.txt` | `A1`, `append_only=false`, `met=false`, exit 1 |
| cheap content (fabricated values in the same rows) | `controls/ctl-cheap-content.txt` | `findings=9`, exit 1 |

**Kill rules.** (1) If any control above reaches `met=true`, C1 is withdrawn before landing. (2) If the
predicate sentence above and the counter's condition diverge, the contract sentence wins and the divergence
is a defect of the build. (3) The repair may not rewrite a historical line; a rewrite withdraws C1.

## C2 — operability (capability acquisition: offline hreflang declaration audit)

**Claim sentence (one).** The lane can audit hreflang declarations offline on a versioned manifest: the new
tool decides every frozen contract case correctly, every degenerate constant control fails at least one
case, its own selftest passes, and it runs end-to-end on the 12 retained real surfaces.

**Tool** `scripts/hreflang_audit.py`: `--manifest <path>`, `--root <dir>`, `--json`, `--selftest`,
`--work <dir>`; scratch honours `TMPDIR`/`--work`, no `/tmp` literal, no network.

**Manifest v1.** `{"version":1,"pages":[{"id","file","url"}]}`; `url` absolute; `file` a local HTML path
relative to `--root`.

**Findings (stable ids; policy class exits 1).**
- `hreflang_missing_value` — `<link rel="alternate">` with no hreflang value.
- `hreflang_invalid_tag` — value neither `x-default` nor a well-formed BCP-47 tag under the frozen ASCII
  grammar `^[A-Za-z]{2,3}(-[A-Za-z]{4})?(-([A-Za-z]{2}|[0-9]{3}))?(-([A-Za-z0-9]{5,8}|[0-9][A-Za-z0-9]{3}))*$`
  (case-insensitive; `_` never accepted).
- `hreflang_relative_href` — alternate `href` without scheme and host.
- `hreflang_duplicate_pair` — same (lowercased tag, exact href) twice on one page.
- `hreflang_multiple_xdefault` — more than one x-default on one page.
- `hreflang_self_missing` — a page with ≥1 hreflang alternate does not list its own `url` among them.
- `hreflang_nonreciprocal` — manifest-internal target B does not declare a return alternate with A's url
  and the same tag; a target outside the manifest is `hreflang_external_target` (informational).
- `hreflang_canonical_not_self` — a page with ≥1 hreflang alternate whose resolved canonical is not its own
  `url`.
- Input faults (exit 2): `input_unreadable`, `input_duplicate_url`, `input_url_not_absolute`.

**Exit.** 0 clean, 1 policy findings, 2 input faults (also when both), 64 usage.

**Limits (stated, never claimed closed).** No live fetch, no HTTP headers/`Vary`, no rendering or JS, no
`hreflang` value outside `x-default`/BCP-47 syntax, no claim about the actual language of any page, no
search-engine selection or ranking claim.

**Target after.** Every frozen contract case decided correctly over a matrix of ≥24 cases; the four
constants (no-op reader, always-clean, report-all, empty-list stub) each fail ≥1 case; tool selftest ≥20
cases green; real-input run over the 12 retained surfaces recorded with its observed state.

**Controls.** The matrix's four constant implementations are the cheap controls and are committed with the
matrix receipt before the after-state is claimed. A constant that passes every case withdraws C2.

**Kill rules.** (1) A matrix case whose expected verdict is not derivable from this contract is a contract
defect, not a tool defect: the case is marked `undecided` and excluded, never counted as a pass. (2) Any
network access during a run withdraws C2. (3) If the real-input run cannot be produced, C2 lands with the
matrix only and the report says so — the capability row does not enter the table.

## Frontier step (inside the claim cap, not a claim)

- `corpus/SOURCES.md`: every new row is opened this round, with URL, access date and a ≤25-word located
  quote in `corpus/lessons/round-76.md` `## Gate`.
- Census before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exit 0,
  181 rows (recorded in the round lesson).
- At least one claim is sourced: C2 cites an `S###` row opened this round.
- One mistake is mined into `## Mistakes` (class · evidence · captured-by · fix), from the round-75
  closure's routed defects or this round's own.
- Assimilation: `merge/kake/` is re-checked read-only; `Assimilation: none` with the blocker named if the
  staged entries' locators still do not re-ground (round-75 precedent).
- `considerthese/2026-10-26.md` Part 2 proposal 5 is already adopted (r66 ledger + r75 criterion); no new
  proposal is mined this round unless a seat finds one unimplemented and grounded.

## Report and landing

Report `.ufo/reports/round-76/kake.md` after WAVE-DONE, citing the pushed lane hash; lane commit and push
through `scripts/hyaku/jj-lane.sh --as kake`, report through `scripts/hyaku/fleet-commit.sh --as kake`.
