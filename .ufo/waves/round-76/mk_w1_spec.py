#!/usr/bin/env python3
"""Build .ufo/waves/round-76/w1-spec.json (14 seats, one v1 wave)."""
import json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
ROUND = f"{LANE}/.ufo/waves/round-76"
W = f"{ROUND}/w1"
BASE = "a0491fcd041cbc3fff2c964ecf6268557e45a5c1"
SCRATCH = "/fast/scratch/hyaku/kake-r76"

DIRECTIVE = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = f"""{DIRECTIVE}

kake lane, round 76, attempt 1, wave w1. Lane checkout: {LANE}. Base revision `{BASE}` (lane master at
round open). Frozen contract: `{ROUND}/contract.md` — read it first; every item below is scoped by it.

## Hard rules (violating one voids the seat)

- **Report trailer paths are relative to {LANE}** — write every `Report:` path at {LANE}/<that path>.
  Nothing you write may land in the fleet root or a sibling repo.
- **You are a leaf.** Never dispatch subagents, never call `task`/`agent`, never message `agent://all`.
  Only an executor seat may spawn one read-only `labrat` probe for a single falsifiable hypothesis.
- **Never commit, push, or run a mutating git/jj command anywhere.** Read-only git (`log`, `show`, `diff`,
  `status`, `rev-parse`, `ls-files`, `cat-file`) is fine. All tree-level work happens in a
  `git clone --shared` under your own scratch dir; the lane checkout is read-only for you. You may write
  only your own files under `{ROUND}/w1/`.
- **Scratch**: `S={SCRATCH}/<YourSeatName>`; `mkdir -p "$S"`, pass `TMPDIR=$S/tmp` and every `--work`
  explicitly, and `rm -rf -- "$S"` before you finish (copy receipts into your wave-dir report first).
  `/tmp` is for files under 50 MB only and is never citable.
- **Never edit**: `{LANE}/scripts/`, `corpus/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md`, the
  fleet repo, `.ufo/state/`, `.ufo/watchdog.log`, any sibling lane. Deliver text/diffs into your wave-dir
  report; the L1 applies them.
- **No network** except where an item says so, and never against an operator-owned property (no writes, no
  authenticated calls, no form posts; public `curl -sSL` GET of a public documentation URL is allowed).
- **Never name a model** in your output and never pass one to a tool.
- **Tooling authorization (operator 2026-10-19)**: you may install or upgrade tools that help the task —
  read `/home/vgpnk/.omp/agent/RULES.md` first (official channels, update-safety gate; record
  tool/version/channel/reason in your report). **Pacman is PAUSED host-wide** (orchestrator ruling): no
  `pacman -S/-Sy/-Syu/-U/-R`, no downgrades, no host-service restarts. Use `uv tool` / `npx` / an official
  binary in `~/.local/bin`, or file an L0 question instead.
- **Honesty**: an unrun check has not passed. Every number you report carries the exact command that
  produced it and the observed output; a quote names its file and line range. If a premise of your item is
  wrong, say so with the bytes that show it — never invent a pass.

## Round claims (frozen; you are attacking or building against them, never redefining them)

{Path(ROUND, 'contract.md').read_text().split('## Frontier step')[0]}
"""


def item(name: str, role: str, body: str) -> dict:
    return {"name": name, "role": role, "item": body.strip()}


ITEMS = [
    item("ScoutHreflangSources", "scout", f"""
Open the three sources C2 rests on and produce the registry rows for them.
Write `{W}/ScoutHreflangSources.md`; retain fetched bytes under `{W}/ScoutHreflangSources/`.

(1) GET each of these with `curl -sSL --max-time 30`, recording HTTP status, final URL, byte size and
sha256, and saving the raw bytes:
  - https://developers.google.com/search/docs/specialty/international/localized-versions (Google
    localized versions / hreflang)
  - https://html.spec.whatwg.org/multipage/links.html (the `hreflang` attribute of `link`)
  - https://www.rfc-editor.org/rfc/rfc5646.txt (Tags for Identifying Languages, BCP 47)
(2) For each, locate the exact sentence(s) that ground these four rules of contract C2 and quote each at
<=25 words WITH its location (section heading + line number in the retained file, or HTML element anchor):
  a) every hreflang version must list itself, and the x-default value, if used, covers unmatched languages;
  b) hreflang values are language tags, `x-default` is the only non-tag value;
  c) alternate hrefs must be fully qualified URLs;
  d) the canonical of the page a hreflang points at must be itself (not another page).
  If a rule is NOT grounded in a fetched source, say so plainly — do not stretch a quote.
(3) Propose one contract-v1 SOURCES row per source in the exact 11-column shape
(`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`), ids
starting at the first unused above the lane's tip (read `{LANE}/corpus/SOURCES.md` for the tip; do not
guess). `kind` is one of spec/docs/paper/code/tool/dataset/talk/book/community/own-work; `tier` scoped to
the rule it grounds; `anchor` names the section + revision/date; `teaches` is one grounded learner benefit;
`status` `mined` only for the row C2's entry will cite; no `|` inside a cell.
(4) Record for each row: URL, access date (today, 2026-11-03), and the <=25-word quote with location —
this is the `## Gate` evidence the round lesson needs.
"""),

    item("ScoutHreflangEdge", "scout", f"""
Per-surface reconnaissance for C2's case matrix: enumerate the edge classes a correct offline hreflang
audit must decide, grounded in the fetched sources from `{W}/ScoutHreflangSources/` (read them when they
exist; otherwise fetch the same three URLs yourself into your own scratch — never assume another seat's
files exist).
Write `{W}/ScoutHreflangEdge.md`.

For each class give: the HTML snippet shape, the expected verdict under contract C2 (clean / which finding
id / input fault), and the sentence or spec rule that decides it. Cover at least:
  1. valid tags: `en`, `en-GB`, `zh-Hant`, `zh-Hant-TW`, `es-419`, `de-CH-1901`, `x-default`;
  2. invalid tags: `en_US`, `EN-gb` (case), `english`, `en-`, `x-defaults`, `i-klingon`, `en GB`;
  3. href forms: relative, protocol-relative (`//host/x`), fragment-only, absolute https, absolute http;
  4. duplicate (tag, href) pairs and the same tag pointing at two different hrefs (legal);
  5. more than one x-default;
  6. self-reference missing vs present;
  7. reciprocity: A→B with tag T and B→A with tag U (U≠T), B→A with T (ok), B has no alternates;
  8. canonical on a hreflang page pointing at itself vs at another page;
  9. HTML edges: `<link>` inside `<template>`/`<svg>`/`<math>` (ignored, per the lane's r35 og precedent),
     `rel="ALTERNATE"` uppercase, `rel="alternate stylesheet"` token list, self-closing tags, attribute
     order, single vs double quotes, HTML entities in href, comments and `<script>` content;
  10. manifest faults: missing file, undecodable bytes, duplicate page url, non-absolute page url.
For each class name which of the four degenerate constants (no-op reader, always-clean, report-all,
empty-list stub) would be caught by it, and flag any class the contract cannot decide (that is a contract
defect, not a tool defect — contract C2 kill rule 1).
"""),

    item("ExecAuditTool", "executor", f"""
Build the C2 tool at `{W}/ExecAuditTool/hreflang_audit.py` (the L1 copies it to `scripts/hreflang_audit.py`
after review; do not write into `{LANE}/scripts/`).
Contract: `{ROUND}/contract.md` §C2 — implement its findings, manifest, exit codes and limits EXACTLY.
Requirements:
- args `--manifest <path>` (required unless `--selftest`), `--root <dir>` (default cwd), `--json`,
  `--selftest`, `--work <dir>` (required with `--selftest`).
- read-only, network-free, stdlib only; no `/tmp` literal anywhere (scratch from `--work` or `TMPDIR`);
  never write outside `--work`.
- parser: a small tolerant HTML tag scanner sufficient for `<link>` elements (attributes in any order, both
  quote styles, self-closing, comments and `<script>`/`<style>`/`<template>` bodies skipped, entities
  decoded for href/tag values); document what it does not do.
- stable finding ids and a deterministic order; `--json` prints `{{version, pages, findings, counts, exit}}`.
- `--selftest` builds >=20 isolated cases under `--work` (one red and one green per finding id, plus the
  input faults and the tag-grammar corners), asserts exit code and finding ids, prints `selftest N/M passed`.
  It must exit 0 only when every case passes.
Deliver also `{W}/ExecAuditTool.md`: the argv, the selftest tally, the observed output of a run against a
3-page fixture you build, and every place where you had to interpret the contract (the L1 turns those into
contract amendments or tool fixes).
"""),

    item("ExecAuditMatrix", "executor", f"""
Build C2's frozen case matrix and its counter, and prove the constants fail.
Deliver `{W}/ExecAuditMatrix/c76_hreflang_matrix.py`, the case set `{W}/ExecAuditMatrix/cases/`, four
constant implementations under `{W}/ExecAuditMatrix/consts/`, and `{W}/ExecAuditMatrix.md`; receipts under
`{W}/ExecAuditMatrix/receipts/`.

(1) Freeze >=24 cases from contract §C2 (one JSON per case: name, manifest, page files, expected
`{{exit, ids}}`). Every expected verdict must be derivable from a contract sentence; a case you cannot
derive is marked `undecided` and excluded from the score (never a pass).
(2) `c76_hreflang_matrix.py --root . --tool <path> --revision <rev> --work <dir>` runs the tool over every
case in an isolated fixture tree and prints
`cases=N decided=M correct=C wrong=W undecided=U constants_failed=K/4 met=<bool>`, exit 0 met / 1 not.
(3) Four constants, each a drop-in replacement tool: `noop` (reads nothing, prints nothing, exit 0),
`always_clean` (parses, never reports), `report_all` (reports every page), `empty_list` (reader returns
no links). Run the matrix against each; every constant MUST fail >=1 case. A constant that passes the whole
matrix means the matrix is broken — say so and fix the matrix, never the constant.
(4) Run the matrix against `{W}/ExecAuditTool/hreflang_audit.py` when it exists (otherwise against your own
scratch copy of the contract implementation) and record the receipt.
(5) `--selftest` for the matrix counter: >=8 cases including a deliberately wrong expected verdict (must
produce `wrong>=1 met=false`) and a constant that passes everything (must be reported as a matrix defect).
"""),

    item("ExecAuditRealRun", "executor", f"""
Run C2 end-to-end on the real retained surfaces and produce the real-input receipt.
Deliver `{W}/ExecAuditRealRun.md`, the manifest `{W}/ExecAuditRealRun/real-manifest.json`, and receipts
under `{W}/ExecAuditRealRun/receipts/`.

(1) Enumerate `{LANE}/.ufo/waves/round-23/live/*/` — each directory holds `page.html`, `manifest.json`
(`pages[0].url`, `expectedCanonical`) and `fetch.json` (status, sha256, finalUrl). Build a version-1
hreflang manifest over all 12 surfaces (one page per directory; `file` relative to `{LANE}`, `url` from the
retained manifest). Verify each `page.html` sha256 equals the retained `fetch.json` sha256 before using it;
report any mismatch instead of using that page.
(2) Census the declarations: per page, every `<link rel="alternate" hreflang=...>` (tag + href) and the
`rel=canonical` href. Report the totals.
(3) Run `{W}/ExecAuditTool/hreflang_audit.py --manifest <your manifest> --root {LANE} --json` (against your
own scratch copy if the wave file does not exist yet) and record the exact output, exit code and every
finding with its page id.
(4) Cross-check with the lane's canonical audit: `python3 -B {LANE}/scripts/canonical_audit.py --manifest
<the same pages reshaped to its v1 manifest> --json` and report whether the two agree on which pages
declare canonicals.
(5) State the honest limit: this measures retained 2026-10-21 bytes, not live serving.
"""),

    item("ExecQuoteCounter", "executor", f"""
Harden C1's counter into the delivered instrument. Deliver `{W}/ExecQuoteCounter/doc_quote_truth.py` and
`{W}/ExecQuoteCounter.md`; receipts under `{W}/ExecQuoteCounter/receipts/`.

Start from `{ROUND}/c76_quote_truth.py` (the L1's v1, selftest 13/13). Keep contract §C1's predicate
EXACTLY — population, claim-bearing span test, receipt universe, T1/T2/T4/A1, `met = (findings == 0) and
append_only`, exit contract 0/1/2/64, `--base` required. Do not add, drop or reword a conjunct.
Requirements:
- `--selftest` over >=20 isolated fixtures under `--work` (superset of the v1's 13): every finding id red
  and green, the elision rules, a seat-prose file that must NOT act as a receipt
  (`*-results.json` excluded), an indented markdown table row, a row whose span is a plain commit hash,
  the append-only conjunct, and a correction row that quotes a validated line and names the span (green).
- performance: the receipt universe is ~10,000 committed files; batch reads (`git cat-file --batch`) or a
  single `git grep -F` per span so a full run stays under ~20 s on this host. Record the measured wall time.
- `--json` output keeps the contract's field names (`rows, receipt_files, spans_checked, spans_exempted,
  corrections, append_only, findings, met`).
Verify at base: `python3 -B {W}/ExecQuoteCounter/doc_quote_truth.py --root {LANE} --revision {BASE}
--base {BASE} --rounds 75,76` must reproduce `findings=8 met=false`, exit 1
(`{ROUND}/controls/base-c1-quote-truth.txt`). Report any divergence with the bytes.
"""),

    item("ExecQuoteRepair", "executor", f"""
Construct C1's after-state in a scratch clone and measure it. Deliver `{W}/ExecQuoteRepair.md` and the
exact text blocks to apply (`{W}/ExecQuoteRepair/blocks/`); receipts under `{W}/ExecQuoteRepair/receipts/`.

(1) Clone: `git clone --shared {LANE} $S/repo` in your scratch, check out the base commit
`{BASE}`, and confirm `git -C $S/repo rev-parse HEAD` is that commit before you write anything.
(2) Run the current counter (use `{W}/ExecQuoteCounter/doc_quote_truth.py` when it exists, else
`{ROUND}/c76_quote_truth.py`) at base and reproduce `findings=8`. For EACH of the eight findings, read the
receipt line it was trying to quote (the finding text plus the round-75 control receipts under
`{LANE}/.ufo/waves/round-75/controls/`) and write a correction row that:
  - names the defective span verbatim;
  - quotes the WHOLE receipt line it should have quoted, contiguously, inside backticks;
  - carries the marker `[r76-correction 2026-11-03]`;
  - names the receipt file it quotes.
(3) Append the correction rows in a NEW `## Round 75 — quote corrections (appended round 76)` section at the
end of `SCORECARD.md`; for the two `corpus/QUALITY.md` / `corpus/lessons/round-75.md` findings, append one
`## Round-76 criterion — quoted receipts are whole` bullet in QUALITY.md and one `## Corrections` bullet in
the round-75 lesson carrying the same marker. Do not modify any existing line (append-only; the standing
`c73_wave_pointers.py` gate will red a rewrite).
(4) Re-run the counter at your clone tip with `--base {BASE}`; the target is `findings=0 append_only=true
met=true`, exit 0. Iterate on the correction wording (not on the counter) until it is.
(5) Copy the final diff (`git -C $S/repo diff {BASE}..HEAD -- SCORECARD.md corpus/QUALITY.md
corpus/lessons/round-75.md`) and each applied block into your wave dir. The L1 applies them to the lane
verbatim; do not edit the lane.
"""),

    item("ScribeKnowledge", "scribe", f"""
Draft this round's prose. Write `{W}/ScribeKnowledge.md` with fenced blocks only.

(a) `corpus/knowledge/hreflang-declaration.md` — provenance trio in the first 8 lines (`source:` the S-id
rows the scout opened THIS round, `verified-at: 2026-11-03`, `recheck: 90d`); body: what a hreflang
declaration is; the self-reference rule; `x-default`; absolute hrefs; the canonical interaction; the
reciprocity requirement; the frozen contract's finding table; and a **Limits** section repeating contract
C2's stated limits verbatim in spirit (no fetch, no headers, no rendering, no language detection, no
ranking). Every quoted source sentence <=25 words WITH its line/section location. If a needed S-row is not
in `{LANE}/corpus/SOURCES.md` when you draft, use the id the scout proposed and say so in a `TODO(L1)` line
inside the fenced block — never invent a quote.
(b) A `corpus/QUALITY.md` round-76 addendum criterion for the class the round-75 closure routed: **a
claim-bearing quote is either the whole receipt line or an explicit elision whose fragments each occur in
the same receipt, and a correction closes a defective quote only by quoting the whole line and naming the
defective span**. Cite the round-76 lesson and the counter; include an able-to-fail line quoting
`{ROUND}/controls/base-c1-quote-truth.txt` output contiguously.
(c) The round-76 lesson skeleton `corpus/lessons/round-76.md`: front matter (base, contract freeze,
measured revision placeholder), `## Claims` (C1/C2 sentences verbatim from the contract), `## Gate`
(placeholders the L1 fills with the scout's rows), `## Mistakes` (you mine one: the round-75 elided-quote
class — class, evidence pointer, captured-by, fix), `## Routed dispositions` with one row per routed item
from `corpus/lessons/round-75-verifier-spotcheck.md` §6 (8 items) and `corpus/lessons/round-75.md`
§Routed (5 items), each `fixed`/`open` + pointer + flip condition, and `## Sources`.
Never write into `{LANE}/corpus/`; the L1 applies your blocks.
"""),

    item("ScribeRegistry", "scribe", f"""
Draft the registry, capability and log text. Write `{W}/ScribeRegistry.md` with fenced blocks only.

Read `{LANE}/SKILL.md` sections `### Round 74 gate registry additions` and `### Round 75 gate registry
additions` for the exact 8-column shape (Name | Kind | Entry command | Verdict map | Self-test | Pinned
values / frozen proof | Write scope | Owner).

(a) `### Round 76 gate registry additions` with one row for `scripts/doc_quote_truth.py` (gate: selftest
mode, verdict map 0 clean / 1 findings / 2 input fault / 64 usage, frozen proof = the base receipt path and
its `findings=8` line, write scope = read-only) and one row for `scripts/hreflang_audit.py` (gate: selftest,
verdict map 0/1/2/64, frozen proof = the matrix receipt and its case count). Every claim in a row must be
true of the delivered tool — read the wave files first; if a number is missing, write `pending(L1)` rather
than guessing.
(b) One `SCORECARD.md` capabilities-table row for the hreflang audit: name, one line of what it can now do,
evidence pointer (tool path + matrix receipt + real-input receipt), first-working round 76.
(c) The `LOG.md` round-76 entry: what was claimed, what landed, the counting commands and their observed
values, plus three correction bullets closing the round-75 closure's R1/R2/R3 (the two stale digests in the
round-75 LOG entry and the disagreeing revision labels), each naming the superseded text verbatim and the
current value with its receipt.
(d) The `SCORECARD.md` round-76 claim table in the same shape as rounds 74/75 (Claim | Axis | Before →
after | Counting command | Verdict), using only values that exist in the wave receipts.
Do not write into the lane's root files; the L1 applies your blocks.
"""),

    item("ReviewerC1", "reviewer", f"""
Attack C1 before its after-state exists. Write `{W}/ReviewerC1.md`; land held-out fixtures under
`{W}/ReviewerC1/`.

(1) Reproduce the base independently: read contract §C1 and `{ROUND}/c76_quote_truth.py`, derive the
population yourself from `git -C {LANE} show {BASE}:SCORECARD.md` and the two corpus files, and check
whether `findings=8` is exactly right — name any finding that is a harness artifact and any real defect the
counter misses.
(2) Build >=10 held-out fixtures (each a tiny repo you `git init` in your scratch, with a `controls/`
receipt) and record the counter's verdict for each:
  - a quote that IS contiguous but in an unrelated round's receipt (should pass — state whether you think
    it should);
  - a quote made contiguous only by a seat report (`w1/Seat.md`) or by `w1-results.json` (must fail);
  - an elision whose fragments sit in two different receipts (must fail, T2);
  - a correction row whose quote is contiguous but which names a DIFFERENT span (must not exempt);
  - a correction row naming the span but quoting a non-receipt line (must not exempt);
  - a row with a 64-hex digest that is fabricated (must fail);
  - a row whose span contains a `|` or a newline escape;
  - an indented table row (1-3 spaces) — decide whether the contract's population includes it and say
    which behaviour the contract sentence implies;
  - a `## Round 76` row in a section whose heading is `## Round 7` (prefix collision);
  - a duplicate correction pair for the same span.
(3) Divergence report: quote the contract sentence and the code line word-for-word wherever they differ.
"""),

    item("ReviewerC2", "reviewer", f"""
Attack C2's tool and case set before the after-state is claimed. Write `{W}/ReviewerC2.md`; land fixtures
under `{W}/ReviewerC2/`.

(1) Read contract §C2 and the delivered `{W}/ExecAuditTool/hreflang_audit.py` (if absent when you start,
implement the contract in your own scratch and attack that, saying so).
(2) Build >=12 adversarial fixtures and record the tool's verdict against the contract sentence for each:
  - tag grammar: `en-GB-oed`, `zh-yue-HK`, `sgn-BE-FR`, `en-u-ca-gregory` (extension — the contract grammar
    rejects it; is that the honest verdict, or a contract defect?), `x-default` uppercase, `X-DEFAULT`,
    `en--GB`, trailing dash, leading/trailing space in the attribute value;
  - href: HTML-entity `&amp;` in the query, uppercase scheme `HTTPS://`, `mailto:`/`tel:` targets,
    `#fragment` self-reference, whitespace-padded href;
  - structure: two alternates on one line, `<link>` split across lines, attribute without quotes, `<template>`
    wrapping, `<svg>` with xlink, a `<link rel=alternate>` with hreflang inside `<noscript>`;
  - reciprocity: a three-page cycle, a page whose partner is not in the manifest, a duplicate manifest url;
  - canonical: relative canonical resolving to the page, absolute canonical with trailing slash difference,
    two canonical links on one page.
(3) Matrix check: read `{W}/ExecAuditMatrix/c76_hreflang_matrix.py` when it exists and try to make a
constant pass the whole matrix (that would be a matrix defect) or a correct tool fail a case (that would be
a contract/tool defect). Report which.
(4) Report every case where the contract is silent, ambiguous, or contradicts a fetched source.
"""),

    item("CriticClaims", "critic", f"""
Falsify the two claims themselves. Write `{W}/CriticClaims.md`.

(1) **Do-nothing control.** A tree at `{BASE}` with nothing added must not reach either target. Measure
both: the C1 counter (`findings=8 met=false`) and the C2 matrix (no tool → no cases correct). Commit the
receipts in your report.
(2) **Predicate fidelity.** Check word-for-word that the contract's claim sentence, the counter's condition
and the receipt's label are the same predicate: for C1 `met = (findings == 0) and append_only`; for C2
`all decided cases correct AND every constant fails >=1 case AND selftest green`. Name any divergence
between the contract, `{ROUND}/c76_quote_truth.py`, and the wave's delivered tools.
(3) **Axis honesty.** C1 is claimed on calibration (score 2, the lane's lowest non-retired axis) and C2 on
operability. Argue whether each claim's after-state actually moves the named axis, or whether one is
bookkeeping with a counter wrapped around it; a claim that a do-nothing control can reach must be named.
(4) **Junk-row check.** Construct the cheapest junk state that a lazy author might commit (a correction
section with plausible-sounding rows, no real quotes; a matrix whose expected verdicts were copied from
the tool's own output). Show the counter/matrix verdict for each.
(5) Name the single strongest reason each claim could still be wrong after landing.
"""),

    item("MutationTesterGates", "mutation-tester", f"""
Mutation-test both new gates. Write `{W}/MutationTesterGates.md`; land mutants under
`{W}/MutationTesterGates/`.

(1) C1 counter (`{ROUND}/c76_quote_truth.py` or the hardened `{W}/ExecQuoteCounter/doc_quote_truth.py`):
apply at least eight mutations one at a time in your own scratch copy and record the selftest and base-run
verdict for each — drop the append-only conjunct; make `met` ignore findings; treat every span as
contiguous; match spans case-insensitively; accept `w1-results.json` as a receipt; make the elision rule
require only ONE fragment; skip the T4 correction check; treat a correction row's mere presence as
exemption; exit 0 unconditionally. Every mutant must be caught (selftest red or base green) — a surviving
mutant is a finding.
(2) C2 matrix/tool: mutate the tool (skip the self-reference rule, accept relative hrefs, ignore
`x-default` multiplicity, treat every external target as reciprocal, skip the canonical rule, accept `_` in
tags, return no findings, exit 0 always) and record which matrix case or constant fails it. Every mutant
must fail >=1 case.
(3) For each mutant record: file, exact one-line change, observed verdict, and whether it survived. Append
the tally `mutants=N killed=K survived=S` and name each survivor as a defect with the case that should have
killed it.
"""),

    item("ConnectorOverlap", "connector", f"""
Sibling-overlap and assimilation scan. Write `{W}/ConnectorOverlap.md`.

(1) **Sibling overlap.** Read every sibling lane's `SKILL.md` capability/registry sections and
`corpus/SOURCES.md` (read-only, `/home/vgpnk/Projects/shokunin/<lane>-shokunin/`) and answer: does any
sibling already hold (a) an offline hreflang audit, (b) a documentation-quote-truth counter, (c) a
BCP-47/language-tag validator? Name the lane, file and line for each hit, and whether kake's version is
duplicate, complementary, or contested scope (report it, never absorb it).
(2) **Assimilation (§10), read-only.** Re-check `/home/vgpnk/Projects/shokuknow/merge/kake/`:
`MERGE-REPORT.md`, `knowledge/corpus/knowledge/*`, `SOURCES.append.md`, `amendments/`. For three
representative staged entries, open the locators they cite and report whether each resolves in this lane
today (round 75 found `.ufo/waves/round-1[456]/` and `.ufo/waves/corpus-expansion-1/audit-wave.py`
absent). Also derive the staged id range and the lane registry tip, and say whether adopting any row would
insert ids below the tip (the append-only blocker). Verdict: `Assimilation: none` with the blocker named,
or name one entry that re-grounds cleanly from sources you can open this round. Never write in that repo.
(3) **considerthese.** Read `{LANE}/considerthese/2026-10-26.md` Part 2 (5 proposals). For each, state
whether it is implemented in the lane today with the file:line that shows it; name any still-unimplemented
proposal that is grounded enough to mine next round (do not implement it here).
(4) **Sources cross-check.** For the S-ids the scout proposes this round, check none duplicates an existing
row's URL inside its scope and that each id is above the lane tip.
"""),

    item("SentinelScope", "sentinel", f"""
Scope, secret and reproducibility audit of this round's artifacts. Write `{W}/SentinelScope.md`.

(1) **Write scope.** List every file any wave-76 seat wrote (the wave dir plus anything that leaked), and
confirm: nothing under `{LANE}/scripts|corpus/`, no lane root files modified, nothing in the fleet repo or
a sibling lane, no writes under `.ufo/state/`. `git -C {LANE} status --porcelain` and
`git -C /home/vgpnk/Projects/shokunin status --porcelain` are your evidence; report every untracked file
outside `{ROUND}/` with its owner guess.
(2) **Secrets.** Scan every wave-76 file for credential material: `op://`, `ghp_`, `github_pat_`,
`AKIA`, `-----BEGIN`, `Bearer `, cookies, session tokens, private URLs with query tokens. Report file:line
and class only — never copy a secret value into your report.
(3) **Host-absolute paths.** Count `/fast/scratch`, `/tmp`, `/home/<user>` occurrences in new round-76
files and in the new `scripts/` tools; the scratch discipline says a committed tool must not hardcode
`/tmp`, and a citied evidence path must resolve at closure. Report each class with its count and a
one-line risk note.
(4) **No operator-owned surface touched.** Confirm from the wave artifacts that no seat fetched, wrote or
authenticated against an operator-owned property; list every network endpoint any receipt shows was
contacted, and classify it public-docs vs property.
(5) **Reproducibility.** For each new counter/tool: does it honour `--work`/`TMPDIR`, exit 0 only on met,
and print the revision it measured? Verify by re-running one selftest with `TMPDIR` unset and once set, and
report both.
"""),
]

SPEC = {
    "wave": "kake-r76-w1",
    "reportDir": ".ufo/waves/round-76/w1",
    "maxLanes": len(ITEMS),
    "context": CONTEXT,
    "items": ITEMS,
}

out = Path(ROUND) / "w1-spec.json"
out.write_text(json.dumps(SPEC, indent=1) + "\n")
print(f"wrote {out} items={len(ITEMS)} bytes={out.stat().st_size}")
print("context bytes", len(CONTEXT.encode()))
for i in ITEMS:
    print(" ", i["name"], i["role"], len(i["item"].encode()))
