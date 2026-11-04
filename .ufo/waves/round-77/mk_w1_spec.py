#!/usr/bin/env python3
"""Build .ufo/waves/round-77/w1-spec.json (14 seats, one v1 wave, round 77)."""
import json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
ROUND = f"{LANE}/.ufo/waves/round-77"
W1 = f"{ROUND}/w1"
BASE = "a2cc5f51002433e11cc3d2f70e650a6c60ad5e68"
SCRATCH = "/fast/scratch/hyaku/kake-r77"

DIRECTIVE = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = f"""{DIRECTIVE}

kake lane, round 77, attempt 1, wave w1. Lane checkout: {LANE}. Base revision `{BASE}` (lane master tip at
round open, 2026-11-03). Frozen contract: `{ROUND}/contract.md` — read it first; every item below is scoped
by it and no item redefines a claim.

## Hard rules (violating one voids the seat)

- **Every `Report:` trailer path the validator rendered is relative to {LANE}** — write it at
  {LANE}/<that path>. Nothing you write may land in the fleet root, another wave dir, or a sibling repo.
- **You are a leaf.** Never dispatch subagents, never call `task`/`agent`, never message `agent://all`.
  Only an executor seat may spawn one read-only `labrat` probe for a single falsifiable hypothesis.
- **Never commit, push, or run a mutating git/jj command anywhere** (`commit`, `add`, `stash`, `checkout`,
  `switch`, `reset`, `pull`, `push`, and any `jj` verb other than read-only `--ignore-working-copy`).
  Read-only git (`log`, `show`, `diff`, `status`, `rev-parse`, `ls-files`, `cat-file`, `merge-base`) is
  fine. The L1 is the only writer of lane history.
- **Write only the files your item names as yours.** The rest of the checkout is read-only for you: no
  edits to another seat's files, `MANIFEST.json`, `.ufo/state/`, `.ufo/watchdog.log`, the fleet repo, or any
  sibling lane. Two executors editing the same file is the one failure mode that voids the wave.
- **Scratch**: `S={SCRATCH}/<YourSeatName>`; `mkdir -p "$S"`, pass `TMPDIR=$S/tmp` and every `--work`
  explicitly, and `rm -rf -- "$S"` before you finish — copy receipts into your wave-dir report first.
  `/tmp` is for files under 50 MB only and is never citable evidence. A 52 MB fixture belongs under `$S`.
- **No network** except where your item says so, and never against an operator-owned property (public
  `curl -sSL --max-time 30` GET of a public documentation URL is allowed; no authenticated calls, no posts).
- **Never name a model** in your output and never pass one to a tool.
- **Tooling authorization (operator 2026-10-19)**: you may install or upgrade tools that help the task —
  read `/home/vgpnk/.omp/agent/RULES.md` first (official channels, update-safety gate; record
  tool/version/channel/reason in your report). **Pacman is PAUSED host-wide** (orchestrator ruling): no
  `pacman -S/-Sy/-Syu/-U/-R`, no downgrades, no host-service restarts. Use `uv tool` / `npx` / an official
  binary in `~/.local/bin`, or file an L0 question instead.
- **Honesty**: an unrun check has not passed. Every number you report carries the exact command that
  produced it and the observed output; every quote names its file and line range. If a premise of your item
  is wrong, say so with the bytes that show it — never invent a pass.

## Round claims (frozen; you build or attack them, never redefine them)

C1 (calibration, score 2 HOLD) — every `SHONEN.md` box is classified from committed bytes by
`.ufo/waves/round-77/c77_shonen_ledger.py` over `corpus/knowledge/shonen-ledger.json`; frozen predicate
`met <=> boxes == 4 and unexamined == 0 and mismatches == 0`; base prints `unexamined=4 mismatches=4
met=false`, exit 1.

C2 (operability, score 10 HOLD; capability) — `scripts/sitemap_audit.py` decides the 20-case frozen
container/format matrix (gzip G1/G2, plain text T1, syndication F1/F2, index F3, unsupported X1) with
`met <=> cases == decided and wrong == 0 and constants_failed == 4`; base fails the gzip/text/feed cases.

Scores stay HOLD. No publish, no deploy, no operator-owned property is touched.
"""


def item(name, role, body):
    return {"name": name, "role": role, "item": body.strip() + f"\n\nReport: .ufo/waves/round-77/w1/{name}.md\n"}


ITEMS = [
    item("ScoutSources", "scout", f"""
Open the three sources C2's frozen contract sentences rest on, from scratch, and produce the registry rows
for them. Write `{W1}/ScoutSources.md`; retain raw bytes under `{W1}/ScoutSources/`.

(1) GET each of these with `curl -sSL --max-time 30`, recording HTTP status, final URL, byte size and
sha256, and save the raw body:
  - https://www.sitemaps.org/protocol.html      (S012 re-open: formats, gzip, text, limits)
  - https://www.rfc-editor.org/rfc/rfc1952.txt  (RFC 1952, GZIP file format — S447 candidate)
  - https://www.rfc-editor.org/rfc/rfc4287.txt  (RFC 4287, Atom 1.0 — S448 candidate)

(2) Strip tags to a stable text rendering (record the stripping recipe and the text sha256), then for each
row produce: the anchor (section name + tag-stripped line range), a **≤25-word** located quote, and the
one-sentence `teaches` cell. Required coverage: gzip compression and the decompressed-size limit; the
one-URL-per-line text file with its UTF-8, 50,000-entry and 50MB limits and its "no other information"
rule; RSS 2.0 `<link>`/`<pubDate>` and Atom 1.0 `<link href>`/`<updated>` as sitemaps.org states them; the
sitemap-index `<loc>` container freedom; RFC 1952's magic number/CRC framing; RFC 4287's `atom:link`
`href` attribute and `atom:updated` element.

(3) Draft the three 11-column registry rows exactly as `corpus/SOURCES.md` writes them (id, source, kind,
tier, scope, anchor, teaches, status, opened, recheck, used-by) for S012 (an update line: old→new for
`used-by`) and for S447/S448 as new rows. Keep every cell free of a literal or escaped `|`.

(4) Verify every quote mechanically: a script that re-finds each quote in the retained text and prints
`quotes=<n> failures=0` (write it to `{W1}/ScoutSources/verify_quotes.py`; receipt
`{W1}/ScoutSources/verify-output.txt`).

Do not write into `corpus/` — the L1 applies the rows.
"""),

    item("ScoutSurface", "scout", f"""
Read-only data walk for both claims. Write `{W1}/ScoutSurface.md` (no production edits, no network).

(A) `scripts/sitemap_audit.py` (657 lines at base): map the structure a format extension must respect —
the manifest loader, where the document root is decided, the XML parse path (expat vs ElementTree), where
the 52,428,800-byte and 50,000-entry limits are enforced, the finding-id vocabulary and its emitters, the
exit-code mapping, and the `--selftest` entry point. Name function names and line numbers. Then read
`scripts/sitemap_audit_selftest.py`: how cases are declared, the exact tally line it prints, and whether it
writes inside the repo or only to temp dirs.

(B) The C2 matrix: for each of the 20 frozen case ids in the contract, state the smallest file bytes that
decide it and the exact expected exit + finding ids. Flag any case where the contract's expected value is
ambiguous against S012's text, with the sentence that makes it ambiguous.

(C) The C1 surface: enumerate the 4 `SHONEN.md` boxes verbatim; for each, propose 2–3 checks derivable from
committed bytes **at a named revision** with a one-line command (e.g. table/registry/checklist counts in
`SKILL.md`, LOG round entries that name a committed receipt path, registry rows whose command path exists,
absence of sibling-lane paths in `corpus/knowledge/`). Say which of the four the current tree would pass
and which it would not, with the count you measured.

(D) The round-76 non-author closure's six routed defects (`corpus/lessons/round-76-verifier-spotcheck.md`
§6): for each, give file:line pointers into the lane tree and the cheapest concrete repair inside this
round's write scope, or say why it is operator-owned.
"""),

    item("ExecSitemapFormats", "executor", f"""
Implement the C2 contract in `scripts/sitemap_audit.py`. You own exactly two files:
`{LANE}/scripts/sitemap_audit.py` and `{LANE}/scripts/sitemap_audit_selftest.py`. Touch nothing else.

Required behaviour (contract G1, G2, T1, F1, F2, F3, X1):
  - gzip container: detect by the `1f 8b` magic regardless of file name (G2); decompress with `gzip`;
    enforce the 52,428,800-byte limit on the **decompressed** bytes (G1) and a bounded read (never buffer
    an unbounded stream — read at most limit+1 bytes, then decide); a corrupt/truncated gzip stream is an
    input fault (exit 2), not a policy finding.
  - plain text sitemap: one absolute http(s) URL per line, UTF-8, ≤50,000 lines, ≤52,428,800 bytes, no
    header/footer/comment line; blank lines are ignored; a leading UTF-8 BOM is stripped from the first
    URL; findings `text_line_not_url`, `text_url_not_absolute`, `text_empty`, `text_too_many_entries`,
    `sitemap_too_large`.
  - syndication: RSS 2.0 (`<item><link>` text, optional `<pubDate>`) and Atom 1.0 (`<entry><link href>`,
    optional `<updated>`); missing link → `feed_item_missing_link`; relative link →
    `loc_not_absolute`; malformed date → `lastmod_invalid` (reuse the existing date validation).
  - sitemap index `<loc>`s are container-agnostic (F3); no format inference from the `.gz/.txt/.rss/.atom`
    suffix.
  - any other root element → `format_unsupported`, exit 2.
Keep every round-39 behaviour and finding id unchanged; extend `scripts/sitemap_audit_selftest.py` with a
case per new rule (at least one per finding id above) and keep the whole selftest green.

Deliver in your report: the new selftest tally receipt (exact command + `selftest <n>/<n> passed` line),
the sha256 of each of your two files, and a table mapping each new rule to the case that would fail if the
rule were removed. Run the selftest from the lane root with `TMPDIR` under your scratch.

Mutation-tester `MutC` and reviewers run concurrently: never rewrite the tool after your final receipt —
if you must, re-run the selftest and say which blob the receipt covers.
"""),

    item("ExecMatrix", "executor", f"""
Build the C2 measurement instrument. You own `{ROUND}/c77_sitemap_matrix.py`, `{ROUND}/cases/**`,
`{ROUND}/consts/**` and `{ROUND}/controls/**` — no production file.

1. `cases/<id>/` for each of the 20 frozen case ids (contract table): `manifest.json` (version-1 shaped like
   the round-39 manifests — read `.ufo/waves/round-39/` and the tool's own docs for the exact shape), the
   local sitemap file, and `expect.json` with `{{"exit": <int>, "findings": [<ids>]}}`. Build g02 as a real gzip whose
   decompressed body is 52,428,801 bytes (write the bytes under your scratch, gzip them, keep the `.gz` only
   if it is small; otherwise record how to regenerate it deterministically in the case README and make the
   counter build it in its work dir). t05 is 50,001 URL lines.
2. `consts/` — four constant tools, each a standalone `.py` with the same CLI as `scripts/sitemap_audit.py`:
   always-clean, report-every-id, empty-findings-with-real-exits, and the round-39 XML-only tool extracted
   from `git show {BASE}:scripts/sitemap_audit.py`.
3. `c77_sitemap_matrix.py` — runs one tool (path or `--tool-revision <hash>` to extract from committed
   bytes into `--work`) over all 20 cases and the 4 constants, and prints exactly:
   `C2 revision=<rev> cases=<n> decided=<n> correct=<n> wrong=<n> constants_failed=<k>/4 met=<true|false>`
   with `met <=> cases == decided and wrong == 0 and constants_failed == 4`, exit 0/1, `--selftest` for the
   counter itself (≥8 cases, including a wrong-expected fixture that must be reported wrong and a constant
   that must be reported failed).
4. Run the **before** state now: the matrix against the base tool bytes
   (`--tool-revision {BASE}`), receipt `{ROUND}/controls/base-c2-matrix.txt`. Expected: the gzip/text/feed
   cases are decided wrong. State the observed line verbatim. Also run each of the four constants against
   the base tool and record which cases they fail (the XML-only constant should match the base tool
   exactly — say whether it does).
5. Do **not** run the after-state against a half-built tool: `ExecSitemapFormats` is writing it
   concurrently. The L1 runs the after-state over the landed bytes.

Report: case inventory with expected exits, the counter's selftest tally, the base receipt line, and the
deterministic regeneration recipe for g02.
"""),

    item("ExecShonenLedger", "executor", f"""
Build C1. You own `{ROUND}/c77_shonen_ledger.py`, `{LANE}/corpus/knowledge/shonen-ledger.json` and
`{LANE}/SHONEN.md`. Nothing else.

1. `c77_shonen_ledger.py --root . --revision <hash> [--work <dir>]` reads committed bytes through
   `git show <rev>:<path>` (never the worktree), parses `SHONEN.md` boxes and
   `corpus/knowledge/shonen-ledger.json`, **re-derives every `checks[].observed` from the committed bytes**
   (path existence at the revision; counts parsed from the named file; for a `command` check, run it or
   re-read the committed receipt it names) and prints exactly one line:
   `C1 revision=<rev> boxes=<n> evidenced=<n> gap=<n> unexamined=<n> mismatches=<n> met=<true|false>`
   with the contract's predicate, exit 0/1, plus `--selftest` (≥10 cases: missing ledger, empty checks,
   fake path, `[x]` without verifier, `[~]` with no row, duplicate row, holds=true over a contradicting
   observation, and a clean 4-box fixture).
2. `corpus/knowledge/shonen-ledger.json` (schema `shonen-ledger/v1`): one row per box, each with the checks
   you actually ran, the observed values and the status. Be honest: a box whose evidence is partial is
   `gap` with a `reason` and a `flip` — a `gap` row is a legitimate outcome and the claim does not require
   four green boxes.
3. `SHONEN.md`: set each box's marker to what the ledger supports (`[~]` for an evidenced row, `[ ]` for a
   gap) and add one pointer line under each box naming the ledger row and its primary evidence path. Never
   write `[x]`: no named non-author verifier has signed a box this round.
4. Run the base state (`--revision {BASE}`) and record the red line; then run against your working tree's
   files at a scratch `git` snapshot only if you can do it without a commit — otherwise report the
   working-tree run separately and say which bytes it read.

Report: both observed lines, the selftest tally, the per-box derivation table (box → check → observed →
status), and what a non-author must do to promote a `[~]` to `[x]`.
"""),

    item("ExecRevisionReceipts", "executor", f"""
Repair round-76 routed defect D1 and leave a receipt class the lane can re-cite. Read-only elsewhere; you
own `{W1}/ExecRevisionReceipts.md` and `{ROUND}/controls/*revision*`.

1. Extract `.ufo/waves/round-76/w1/ExecAuditMatrix/c76_hreflang_matrix.py` and the round-76 cases/consts;
   run the matrix with an **explicit full hash** and the landed tool:
   `python3 -B .ufo/waves/round-76/w1/ExecAuditMatrix/c76_hreflang_matrix.py --root . --tool
   scripts/hreflang_audit.py --revision {BASE} --cases ... --consts ... --work <scratch>`.
   Record whether the receipt prints a concrete revision, whether `git cat-file -e <rev>:scripts/hreflang_audit.py`
   succeeds at that revision, and the tool sha256 the receipt names versus `git show <rev>:scripts/hreflang_audit.py | sha256sum`.
   This is the exact defect: the round-76 receipt says `revision=master … head=d00ea7fb` where the tool
   does not exist.
2. Do the same for the 8-page real-input manifest with the **landed** tool digest (the round-76 run used a
   pinned predecessor build `58a2cdce…`): rerun it on `scripts/hreflang_audit.py` at the same full hash and
   record `pages=<n>` and the finding count. Retained pages live under `.ufo/waves/round-76/w1/` (find the
   manifest and the 8 `page.html` files; verify each against its `fetch.json` sha256 as the round-76 seat
   did).
3. Write a short reusable recipe in your report: the three checks that make a receipt revision-bound
   (concrete full hash, artifact exists at that hash, named tool digest equals the blob at that hash) and a
   one-command form the lane can paste next round.
4. Receipts: `{ROUND}/controls/r77-hreflang-matrix.txt`, `{ROUND}/controls/r77-hreflang-realrun.txt`.

Do not edit round-76 files, `scripts/hreflang_audit.py`, or the counters.
"""),

    item("ScribeSources", "scribe", f"""
Write the C2 knowledge entry. You own exactly `{LANE}/corpus/knowledge/sitemap-formats.md`.

Open https://www.sitemaps.org/protocol.html yourself (one public GET, HTTP status recorded) and use
`{W1}/ScoutSources.md` and `{W1}/ScoutSources/verify-output.txt` if they exist when you write; if they are
not there yet, derive your own quotes from your own fetch and say so in the entry's provenance line.

The entry must carry the corpus header fields (`source:`, `verified-at:`, `recheck:`) and sections:
  - what a sitemap file is in this lane's reading, with the three formats S012 names;
  - the gzip container: magic, and the limit applied to decompressed bytes;
  - the plain-text format: one absolute URL per line, UTF-8, 50,000/52,428,800 limits, no other content;
  - syndication: RSS 2.0 `<link>`/`<pubDate>`, Atom 1.0 `<link href>`/`<updated>`;
  - the sitemap-index `<loc>` container freedom;
  - **Limits**: it states no fetch, no engine acceptance, no robots `Sitemap:` cross-submission, no
    compression-ratio or server behaviour, and no claim about any owned property; every rule is attributed
    to the row that states it (S012, S447, S448 — use those ids; the L1 assigns the final registry ids and
    will correct the citations if they move).
Every factual sentence carries its `S###`. Quotes are ≤25 words and locate exactly (section + line range).
Do not write outside your one file.
"""),

    item("ScribeRecord", "scribe", f"""
Two prose deliverables. You own `{LANE}/corpus/QUALITY.md` (append-only) and deliver the rest as text.

1. Append two criteria to `corpus/QUALITY.md` under a new heading `## Round-77 criteria — the report's own
   evidence`, each with a name, the rule, and an able-to-fail form:
   - **Census-warning counts are quoted whole.** A round that states a `sources-census.sh` warning count
     names the round-end census line it came from and accounts for warnings the round itself added
     (round-76 D2: report said 16, tip census printed 17).
   - **A report's evidence quotes obey the same whole-line rule as the ledger's.** Any backticked command
     output in a round report is a contiguous substring of a committed receipt line (or is marked as a
     rendering, naming the transformation) — the rule `scripts/doc_quote_truth.py` enforces on
     `SCORECARD.md` applies to the report (round-76 D3).
   Also add one line stating that a receipt names one revision per artifact and that revision must contain
   the artifact's bytes (round-76 D1 class).

2. Deliver, in your report file `{W1}/ScribeRecord.md`, ready-to-apply text (no placeholders) for:
   - `SCORECARD.md` §"Round 77 — declared and measured claims": the two claim rows with the frozen
     before→after shapes (leave the measured numbers as the contract's field names to be filled by the L1,
     formatted exactly like the round-76 table) plus the two capability-table rows the round would enter if
     C2 lands;
   - `LOG.md` §"Round 77 — 2026-11-03 (hyaku run 15; attempt 1; Linux host; claims frozen before any seat
     ran)" following the round-76 entry's shape;
   - three append-only correction lines closing round-76 routed defects D4 (five SCORECARD rows + one
     QUALITY criterion + one lesson bullet, not seven in SCORECARD), D5 ("entered from unlisted ground",
     not "frontier to core") and D6 (the deletion control prints `A1` only).
3. Write no file under `corpus/` except `QUALITY.md`.
"""),

    item("ReviewC1", "reviewer", f"""
Adversarially attack C1. Write `{W1}/ReviewC1.md`; numbered findings `F1…`, each with severity
(`blocker`/`major`/`minor`), the exact command you ran, and its observed output.

Attack surface:
  1. Can the counter be greened without evidence? Build the cheapest fake in your own scratch: a ledger
     whose four rows carry `status=evidenced`, `checks` with `holds=true` and observations you did not
     measure. The counter must report a mismatch (or `unexamined`) — show it does, or show the hole.
  2. Does `met` really require `unexamined == 0`? Try 3 rows, 5 rows, duplicate rows, a `[x]` with no
     `verifier`, and a `[~]` whose check path does not exist at the revision.
  3. Are the four box predicates honest, or tautologies that any repo passes? For each, name what a wrong
     repo would have to do to pass it.
  4. Is the base red for the right reason (`{BASE}` → `unexamined=4`), and does the counter read committed
     bytes only (no worktree reads, no `--revision` default silently equal to HEAD)?
  5. Does the SHONEN.md marker vocabulary (`[ ]`, `[~]`, `[x]`) agree with what the ledger can support?
Run every command against a scratch copy; never modify the lane's files.
"""),

    item("ReviewC2", "reviewer", f"""
Adversarially attack C2. Write `{W1}/ReviewC2.md`; numbered findings `F1…`, each with severity, command and
observed output.

Attack surface:
  1. Does each of the 20 frozen cases actually decide the rule it names? Name any case that passes for the
     wrong reason (e.g. a gzip case that would also pass if gzip were treated as opaque bytes).
  2. Are the expected values grounded in S012's own sentences? Re-open https://www.sitemaps.org/protocol.html
     with one public GET and quote the sentence behind each disputed expectation.
  3. Does the base tool really fail the new cases (run the matrix at `{BASE}` yourself with the counter if
     `ExecMatrix` has landed it, or reproduce three cases by hand)? A before-state that is red only because
     the case files are malformed is not a before-state.
  4. Can a shape-only stub pass — e.g. a tool that prints the expected ids by parsing the case directory?
     Say what the counter does to detect that.
  5. Is the decompressed-size rule actually enforced on decompressed bytes (build a small gzip whose body
     exceeds a lowered limit is not allowed — instead show the code path and one real >50MB receipt if the
     matrix produced it)?
Run against scratch copies; never modify the lane.
"""),

    item("CriticC", "critic", f"""
Falsify both claims' premises — the sizing, not the implementation. Write `{W1}/CriticC.md`.

  1. C1: is "classify each promotion box from committed bytes" a calibration move or a documentation
     reorganisation? Name the strongest case that the lane learns nothing it did not know, and the strongest
     case that it does. Check the contract's own words for an unfalsifiable step (`evidenced` may be 0 and
     the counter still greens if all four are `gap`) — is `met` then a shape? Say what would make it bite.
  2. C2: is the after-state reachable in one round by the seats the contract names, and is the matrix's
     20-case population enough to separate the three families from the round-39 tool? Name the two cases you
     think are most likely to be mis-specified and say what the contract should have said.
  3. Axis naming: C2 claims operability with a coverage side-effect; C1 claims calibration. Say whether
     either claim is actually on a different axis, with the AXES.md sentence.
  4. Do-nothing control: for each claim, state the cheapest thing a do-nothing round could do that still
     meets the frozen target, and whether the contract's kill rule excludes it.
You may run read-only commands and scratch experiments; never modify lane files.
"""),

    item("MutC", "mutation-tester", f"""
Mutation-test both instruments. Write `{W1}/MutC.md`; one table row per mutant: id, instrument, mutation,
killed-by (the case/control/receipt that went red), or `survived` + why it is unreachable/equivalent.

Targets and a minimum of 12 mutants:
  - `scripts/sitemap_audit.py` (if `ExecSitemapFormats` has landed it): remove the gzip magic check; apply
    the size limit to compressed bytes; accept a relative text URL; drop the 50,000-entry check; drop the
    feed missing-link check; treat a malformed date as clean; return clean for an unsupported root; catch
    every exception and return exit 0.
  - `{ROUND}/c77_sitemap_matrix.py`: count a `decided` case with mismatched findings as correct; stop
    requiring all four constants to fail; compare exit codes only.
  - `{ROUND}/c77_shonen_ledger.py`: accept `holds=true` without re-deriving; count a `checks`-empty row as
    examined; drop the `[x]`-needs-verifier rule; treat duplicate rows as one.
For each mutant, run the counter and record the observed line. A mutant that the counter does not kill is a
finding against the instrument, not a pass: name the case the instrument should have had.
Run everything on scratch copies; delete your scratch before finishing.
"""),

    item("ConnectorC", "connector", f"""
Cross-lane overlap and assimilation scan. Read-only; write `{W1}/ConnectorC.md`.

  1. **Sibling overlap.** For each sibling lane under `/home/vgpnk/Projects/shokunin/*-shokunin/`, search
     for an existing sitemap-format audit (gzip/plain-text/RSS/Atom) and for a SHONEN/promotion-box
     ledger. Report: lane, path, what it holds, and whether kake's round-77 claims would duplicate it. Do not
     absorb or copy sibling bytes into kake; overlap is reported, never imported.
  2. **Assimilation id-collision check** (contract §Frontier): run exactly this, under
     `{ROUND}/assimilation/`, and paste all three id lists, the collision count and any renumber map:
     ```
     S=/home/vgpnk/Projects/shokuknow
     A={ROUND}/assimilation; mkdir -p "$A"
     grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}' {LANE}/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
     grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}' "$S/merge/kake/SOURCES.append.md" | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
     comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
     ```
     Then prove the guard bites once: build a scratch registry with an **indented** (`  | Sxxx |`) row that
     collides with a staged id and show the 0–3-space parser catches it while a column-zero-only parser
     does not.
  3. **`considerthese`** — read `{LANE}/considerthese/2026-10-26.md` §Part 2 and, for each of its five
     proposals, name the lane round/artifact that implemented it, or `unimplemented`. Never edit that file.
  4. **`merge/kake` MERGE-REPORT** — state whether any staged entry cites a row whose id is now occupied by
     different content, with one concrete example pair (staged id, lane row at that id, first 80 chars of
     each).
"""),

    item("SentinelC", "sentinel", f"""
Security review of the new code paths. Write `{W1}/SentinelC.md`; findings `F1…` with severity and a
reproduction that does not harm the host.

Review (read the bytes as they are when you review; record the sha256 you reviewed):
  - `scripts/sitemap_audit.py` after `ExecSitemapFormats` lands: gzip decompression bounds (a 50 KB gzip
     must not be able to force unbounded memory; the limit must be applied while reading, not after),
    XML entity/DOCTYPE handling (billion laughs, external entities), manifest path traversal (`../`,
    absolute paths, symlinks), UTF-8 decode errors, extremely long lines, and the exit-code contract
    (an internal exception must never read as `clean`).
  - `{ROUND}/c77_sitemap_matrix.py` and `c77_shonen_ledger.py`: subprocess argument injection, reading
    untrusted case files, writing outside `--work`, and any `shell=True`.
  - The matrix's 52 MB fixture: confirm it lives under scratch and is removed.
Reproduce at most in scratch; never crash the host, never exceed 1 GB of memory, never write outside your
scratch dir.
"""),
]


def main():
    spec = {
        "wave": "kake-r77-w1",
        "reportDir": ".ufo/waves/round-77/w1",
        "maxLanes": len(ITEMS),
        "context": CONTEXT,
        "items": ITEMS,
    }
    out = Path(ROUND, "w1-spec.json")
    out.write_text(json.dumps(spec, indent=1) + "\n")
    print(f"wrote {out} items={len(ITEMS)}")


if __name__ == "__main__":
    main()
