#!/usr/bin/env python3
"""Round-40 wave 1: the adversarial control wave for C1 (before the build lands) plus source re-opens,
declaration attacks and the routed-defect items. Usage: make_w1_spec.py REV"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
SB = "/fast/scratch/hyaku/kake-r40w1"
SH = "/fast/scratch/hyaku/kake-r40/shared"
COUNTER = f"{L}/.ufo/waves/round-40/c1_count.py"
CONTRACT = f"{L}/.ufo/waves/round-39/c1-contract.md"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"
TOOLING = ("Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — "
           "read /home/vgpnk/.omp/agent/RULES.md first (official channels; record tool, version, channel and reason in your report). "
           "All pacman transactions are PAUSED host-wide (orchestrator ruling 2026-10-20): install via uv tool, npx or an official "
           "binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart.")

CONTEXT = f"""# Goal
Kake round 40, wave 1 (the adversarial control wave, run before the claimed build lands), plus source re-opens and attacks on the round's declaration. The L1 (agent id KakeR40) is the only integrator and scorer; you are one leaf seat. Lane repo: {L} (tip {REV}). Lane axes: operability and freshness.

# The claim (frozen at {REV}; read {L}/SCORECARD.md section "Round 40 — C1 declared")
C1 repairs `{L}/scripts/sitemap_audit.py` (contract {CONTRACT}) on three input classes: E (UTF-16 without a BOM → `xml_malformed`), U (a `loc` or `sitemapUrl` carrying TAB/CR/LF, or a `sitemapUrl` with a leading C0 control or space → `loc_not_absolute` / `check_invalid`), R (a check repeating the string id of an earlier invalid check → `check_invalid`). Frozen counter: {COUNTER} (30 public witnesses with random hosts/ids per run, plus the round-39 selftest 150/150). Predicate: `met: passed >= 30 of 30 witnesses and the round-39 selftest passes 150 of 150`. The L1's reference repair (the build candidate, not yet in the lane) is at {SH}/ref_fix.py, its diff against the base tool at {SH}/ref_fix.diff (read-only). Kill rule: any CONTROL that meets the predicate before the build lands makes C1 exploratory. A control is a tool built to skip declared work (classes in the SCORECARD section). Finding a control that meets the predicate is a success for you, not a failure: report it plainly.

# Scoring a tool (control seats)
`timeout 1200 python3 -B {COUNTER} --root {L} --tool-file <your tool> --label <YourName>[-suffix] --out <your sandbox>/receipt[-suffix].json` — exit 0 met, 1 not met, 2 cannot evaluate. The counter only reads the lane via read-only `git show`. Run it as often as you like; the L1 re-scores every tool you return.

# Bounds
- You are a leaf: no subagents, no swarm, no verdict on the round.
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report. Never edit files under {SH}.
- Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git is fine. Never run jj at /home/vgpnk/Projects/shokunin. If you need a clone: `git clone -q {L} {SB}/<YourName>/clone` after unsetting GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE.
- Cap every run with `timeout` (≤1200 s), ≤8 parallel processes, `prlimit --as=4000000000`; bound every file you write (≤200 MB per seat; never append in a loop to a file Python imports; never point a log at sitecustomize.py or a .pth); `df -h /fast` before writing >1 GB; kill every process tree you start before returning. Never run `du` or `find` over /fast/scratch as a whole.
- Network: only URLs your item names, GET only. Never request the operator's properties (ds4cc.com, app.ds4cc.com, operator *.onrender.com hosts, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json).
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- {TOOLING}
- A provider safety or policy refusal or an automatic model switch ends your item: a one-line report saying so; do not rephrase. Message only agent://KakeR40 for blockers; never agent://all. Plain English.

# Result
Report under 60 lines: what you built or checked, exact commands with exit codes, tool paths with sha256, counter results (passed, byClass, selftest, met) for every tool you scored, findings with path:line, and per attacked statement: holds / overstated / wrong. An unrun check has not passed. Time box: 30 minutes; a partial report (first line `PARTIAL:`) beats none.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, SH=SH, COUNTER=COUNTER, CONTRACT=CONTRACT)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR = ["operability"], ["freshness"]
CTL_ACC = "Tool path(s) and sha256, one counter receipt per tool (passed, byClass, selftest, met), and one line per tool naming the declared work it skips and the witness(es) that caught it — or, if it meets, say so in the first line."


def ctl(name, role, what, how):
    return item(name, role, OP,
                "Control class: " + what + " Attacks: the C1 counter's power to reject a tool that skips this work.",
                "- Build the control in {sb}/ (start from the base tool `git -C {L} show {REV}:scripts/sitemap_audit.py` and/or the reference {SH}/ref_fix.py, or from scratch). " + how +
                "\n- Keep the skip: the control must still NOT do the named work. Within that constraint, try hard to make it meet the predicate (study the witnesses in {COUNTER}).\n- Score every variant with the counter.",
                CTL_ACC)


ITEMS = [
    ctl("CtlSkipE", "executor", "partial repair that skips class E.", "Implement U and R exactly as the reference does; leave the E path as in the base tool."),
    ctl("CtlSkipU", "executor", "partial repair that skips class U.", "Implement E and R exactly as the reference does; leave URL judgment as in the base tool."),
    ctl("CtlSkipR", "executor", "partial repair that skips class R.", "Implement E and U exactly as the reference does; leave the repeated-id rule as in the base tool."),
    ctl("CtlUTabOnly", "mutation-tester", "U sub-shape: rejects TAB but not CR or LF.", "Reference with the U guard narrowed to TAB only; also variants rejecting TAB+LF but not CR, and CR+LF but not TAB."),
    ctl("CtlURawBytes", "executor", "U proxy: detects TAB/CR/LF by a regex over the raw file bytes between `<loc>` tags instead of judging the parsed value.", "E and R as the reference; U only through the raw-bytes regex (no check of the parsed `loc` value or of `sitemapUrl` beyond what the regex sees)."),
    ctl("CtlULocOnly", "mutation-tester", "U sub-shape: repairs `loc` only, not `sitemapUrl`.", "Reference with the U guard applied only where `loc` values are judged."),
    ctl("CtlUSitemapUrlOnly", "mutation-tester", "U sub-shape: repairs `sitemapUrl` only, not `loc`.", "Reference with the U guard applied only to manifest `sitemapUrl`."),
    ctl("CtlUAnyWhitespace", "mutation-tester", "U proxy: rejects any URL value containing any whitespace (before or instead of the sentence-21 strip).", "Variants: guard on the unstripped `loc` text; guard on any Unicode whitespace; guard on `str.isspace` anywhere."),
    ctl("CtlELittleEndianOnly", "mutation-tester", "E sub-shape: detects BOM-less UTF-16LE only.", "Reference with the E repair replaced by a little-endian-only test (e.g. a NUL at every odd offset); also a big-endian-only variant."),
    ctl("CtlEDeclOnly", "mutation-tester", "E sub-shape: repairs only files that carry an XML declaration.", "Detect BOM-less UTF-16 only by a `<\\0?\\0x\\0m\\0l` / `\\0<\\0?\\0x` declaration sniff."),
    ctl("CtlENulSniff", "mutation-tester", "E proxy: any NUL byte in the raw bytes gives `xml_malformed` before UTF-8 decoding.", "Variants: NUL test before decode; `<\\0` prefix sniff before decode; NUL test before the BOM strip."),
    ctl("CtlEWrongCode", "mutation-tester", "E with a code other than the contract's: BOM-less UTF-16 gives `encoding_invalid`.", "Reference with the E repair returning `encoding_invalid`; also a variant that returns an error check (`file_unreadable`)."),
    ctl("CtlRAnyRepeat", "mutation-tester", "R proxy: any repeated id regardless of type (`str(id)` or `repr` comparison).", "Reference with the R repair comparing `str(raw.get('id'))` for every check, including non-string ids and non-object checks."),
    ctl("CtlRCaseFold", "mutation-tester", "R proxy: ids compared case-insensitively.", "Reference with the R repair comparing `id.casefold()`; also `.lower()` and NFKC variants."),
    ctl("CtlROneKind", "mutation-tester", "R sub-shape: registers the id of an earlier invalid check for one invalid kind only.", "Variants: only earlier checks missing `file`; only missing `sitemapUrl`; only non-string `file`."),
    ctl("CtlPositionKeyed", "executor", "shortcut keyed on check positions or counts.", "Base tool plus rules keyed on manifest shape (e.g. 'in a 2-check manifest whose first check is invalid, mark the second invalid'; 'third check of three'); no id comparison."),
    ctl("CtlLabelKeyed", "executor", "shortcut keyed on ids, file names, hosts or labels.", "Base tool plus rules keyed on the counter's random name shapes (ids `c…`/`r…`, hosts `w…​.example`, dirs `d…`, files `f….xml`) or on witness labels; no behaviour-level repair."),
    ctl("CtlKeyFinder", "executor", "key-finder: reads outside the case directory (the counter source, the lane, /proc of the parent, environment) to find expectations.", "Write a tool that tries every path it can to read expectations at run time inside the counter's bubblewrap sandbox; report what was visible."),
    ctl("CtlConstantFamily", "executor", "constant and junk outputs not yet scored by the L1.", "Constant all-findings (`xml_malformed` on every check), constant all-error (`check_invalid`), exit-code-only tools (correct exit, empty stdout), and a tool that echoes the base tool's output but flips every verdict; score each."),
    item("MutFamilyE", "mutation-tester", OP,
         "The E repair line in {SH}/ref_fix.py (`if \"\\x00\" in text`). Attacks: whether the 9 E witnesses kill every weakening of that repair.",
         "- Write ≥8 single-change mutants of the reference that weaken or misplace the E repair only (wrong position, wrong character, wrong code, BOM-order swap, partial condition), in {sb}/mutants/.\n- Score each with the counter.",
         "Per mutant: the one-line change, sha256, counter result; list every survivor (a mutant that meets) first."),
    item("MutFamilyU", "mutation-tester", OP,
         "The U repair line in `_parse_url` of {SH}/ref_fix.py. Attacks: whether the 13 U witnesses kill every weakening of that repair.",
         "- Write ≥8 single-change mutants that weaken the U repair only (drop one character, `lstrip` vs leading test, `<` vs `<=`, apply after `urlsplit`, apply to the stripped value only, etc.), in {sb}/mutants/.\n- Score each with the counter.",
         "Per mutant: the one-line change, sha256, counter result; list every survivor first."),
    item("MutFamilyR", "mutation-tester", OP,
         "The R repair lines in `_evaluate_check` of {SH}/ref_fix.py. Attacks: whether the 8 R witnesses kill every weakening of that repair.",
         "- Write ≥8 single-change mutants that weaken the R repair only (register after the type check, register non-string ids, compare `ident_out`, skip registration on invalid file values, etc.), in {sb}/mutants/.\n- Score each with the counter.",
         "Per mutant: the one-line change, sha256, counter result; list every survivor first."),
]

ITEMS += [
    item("ReopenS110", "scout", FR, "Row S110 in {L}/corpus/SOURCES.md and its Gate line in {L}/corpus/lessons/round-40.md. Attacks: the row's quote, anchor and `teaches`.",
         "- GET https://www.w3.org/TR/xml/ ; compare sha256 with {L}/.ufo/waves/round-40/sources/SHA256SUMS.\n- Find the Gate quote (§2.8 Note) and production [2] Char in the stripped text; check each clause of `teaches` (U+0000 not a Char; UTF-16 MUST begin with the BOM; 1.x processed as 1.0) against the text.",
         "Per clause: holds / overstated / wrong with the located text."),
    item("ReopenS111", "scout", FR, "Row S111 (Python urllib.parse). Attacks: quote, anchor, `teaches`.",
         "- GET https://docs.python.org/3/library/urllib.parse.html ; compare sha256 with the retained copy.\n- Locate the quote and the 3.10 / 3.12 change notes; check on the installed Python (`python3 -c` with urlsplit) that the described stripping happens.",
         "Per clause: holds / overstated / wrong with the located text and the python output."),
    item("ReopenS112", "scout", FR, "Row S112 (supersedes S106). Attacks: whether the correction is right and complete.",
         "- GET https://www.w3.org/TR/xml-names/ and https://www.sitemaps.org/protocol.html ; search both for `ignor`; locate the §2.3 quote; read S106's row and the round-39 spot-check (\"S106 clause\") and say whether S112 now states only what the sources say.",
         "Per clause of S112's `teaches`: holds / overstated / wrong."),
    item("ReopenS113", "scout", FR, "Row S113 (supersedes S107). Attacks: the xsd:date / xsd:dateTime statements.",
         "- GET https://www.w3.org/TR/xmlschema11-2/ ; locate productions [16] dateTimeLexicalRep and [18] dateLexicalRep, their regular expressions and the timezone range; check every clause of S113's `teaches`.",
         "Per clause: holds / overstated / wrong with located text."),
    item("ReopenS114", "scout", FR, "Row S114 (supersedes S109). Attacks: the apostrophe correction and the rest of `teaches`.",
         "- GET https://yandex.com/support/webmaster/en/controlling-robot/sitemap ; locate the quote and print the code point of the apostrophe; check 'same-domain URLs only' against the page text.",
         "Per clause: holds / overstated / wrong with located text and code points."),
    item("CriticDeclaration", "critic", OP,
         "The C1 declaration in {L}/SCORECARD.md (\"Round 40 — C1 declared\") and the counter {COUNTER}. Attacks: the declaration against the prompt's claim-sizing rules (/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-40.md §6 item 9).",
         "- Read only; do not run code. Check: one predicate that is the same sentence in plan, code and receipts; a do-nothing control or shortcut that could meet the target; axis named by surface; universal clauses; whether the control classes name only tools that skip declared work (QUALITY (n)); whether the pre-declaration tools are all named by sha256 (QUALITY (o)); whether the claim is coverage dressed as quality or the reverse.",
         "Per rule: holds / overstated / wrong with SCORECARD line numbers."),
    item("CriticD1Reject", "critic", OP,
         "The rejection of routed defect 2's D1 fix in {L}/corpus/lessons/round-40.md (Gate, rejects) and the SCORECARD declaration. Attacks: the reading that `version=\"1.1\"` is well-formed XML 1.0 under contract sentence 8.",
         "- Read only. Read {CONTRACT} sentence 8, the retained XML 1.0 text {L}/.ufo/waves/round-40/sources/xml-1.0.html (§2.8 productions [24]–[26] and the Note, §1 on versions), and {L}/.ufo/waves/round-39/resid/ReviewBuildContract.md D1. Argue the strongest case that D1 is a real deviation, then judge.",
         "Verdict: rejection holds / overstated / wrong, with quoted text."),
    item("ReviewD3Reading", "reviewer", OP,
         "D3 (doctype plus malformed gives `doctype_present`) in {L}/.ufo/waves/round-39/resid/ReviewBuildContract.md and the round-40 lesson's 'Not changed: D3'. Attacks: whether leaving D3 unchanged is a contract reading or a dodged repair.",
         "- Read sentences 8–9 of {CONTRACT}, `scripts/sitemap_audit.py:155-196` at {REV}, and the build seat's declared reading ({L}/.ufo/waves/round-39/w2a3/BuildSitemapAudit.md). You may run the base tool on small fixtures in {sb}/.",
         "Holds / overstated / wrong with commands and path:line."),
    item("ReviewCounterCode", "reviewer", OP,
         "The frozen counter {COUNTER}. Attacks: bugs that would make it pass a wrong tool or fail a right one (judge, normalisation, sandbox argv, selftest summary parsing, seed handling, exit mapping).",
         "- Read the code; run it on the base tool (`--revision {REV}`) and on {SH}/ref_fix.py with two seeds each; try malformed stdout shapes against `judge` in a copy under {sb}/.",
         "Per finding: severity, path:line, a reproducing command."),
    item("ReviewWitnessContract", "reviewer", OP,
         "The 30 witnesses in `witnesses()` of {COUNTER}. Attacks: whether each expected outcome is what contract {CONTRACT} decides (sentence by sentence), and whether any witness depends on a reading the declaration does not state.",
         "- For each witness E1–E9, U1–U13, R1–R8: name the deciding sentence(s) and say agree / disagree. You may materialise witnesses in {sb}/ with a fixed seed.",
         "A 30-row table: witness, sentence(s), agree/disagree, reason."),
    item("ScribeR39ReportCorrections", "scribe", OP,
         "Three miscounts in the round-39 report (/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/kake.md) named by {L}/corpus/lessons/round-39-verifier-spotcheck.md 'Report defects'. Attacks: whether each correction is right on committed bytes.",
         "- Re-derive each from committed bytes: (1) `git -C {L} ls-tree -r --name-only 565ef4c9 scripts/ | grep -c sitemap_audit` vs `grep -cx scripts/sitemap_audit.py`; (2) how many critic seats returned source or diffs (round-39 `w1a3/` reports and `a3-controls/w1a3-materialized/`); (3) the denominator of the criterion-(o) false accepts (`w2a3/MutCriterionO.md`).\n- Draft the appended correction text (one sentence each, with the command).",
         "Three corrected sentences with commands and outputs; flag any where the spot-check itself is wrong."),
    item("ConnectorSiblingOverlap", "connector", ["operability", "freshness"],
         "Sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin (read-only). Attacks: overlap or conflict between kake's C1 (sitemap audit repairs; urlsplit stripping; XML encoding) and any sibling's corpus, tools or sources.",
         "- Search sibling corpora and scripts for sitemap, urlsplit, UTF-16/BOM, XML version handling and RFC 3986 rows; name any sibling row or entry that agrees, conflicts or duplicates S110/S111.",
         "List of overlaps with path:line and the relation (agrees / conflicts / duplicates / none)."),
    item("ScoutCarriedItems", "scout", OP,
         "Open items carried into round 40: round-38 routed defect 6 items 2–10 ({L}/corpus/lessons/round-38-verifier-spotcheck.md), (j) survivor M06 and `MutRecheckOversize` survivors (round-39 SCORECARD corrections). Attacks: the claim that they are still open.",
         "- For each item, check its status at {REV} from committed bytes (read-only).",
         "One line per item: open / closed, with path:line evidence."),
    item("ExecD1Check", "executor", OP,
         "A check for the round's mined mistake (a routed defect accepted without re-deriving it from its source would have broken the tool on D1). Attacks: whether the D1 rejection can be enforced and shown able to fail.",
         "- Write {sb}/d1_check.py: given `--tool <path>`, it materialises a urlset in UTF-8 with `<?xml version=\"1.1\" encoding=\"UTF-8\"?>` and 1.0-only content plus a `version=\"2.0\"` twin, runs the tool, and exits 0 only if the 1.1 file is `clean` and the 2.0 file is `xml_malformed`.\n- Show it green on the base tool and on {SH}/ref_fix.py, and red on a 'D1-fixed' mutant you write (any version other than `1.0` → `xml_malformed`).",
         "Paths with sha256, three runs with exits."),
    item("ScribeMistake", "scribe", OP,
         "The `## Mistakes` entry for {L}/corpus/lessons/round-40.md. Attacks: nothing; drafts text the L1 integrates.",
         "- Draft one entry (class · evidence pointer · captured-by · fix) for: the round-39 closure routed 'fix D1' and the lane would have applied it, though S110 §2.8 makes `version=\"1.1\"` well-formed XML 1.0. Evidence: spot-check routed defect 2, {L}/.ufo/waves/round-40/l1-probe.py rows v11/v20, S110. Captured-by: say which existing QUALITY criterion (read {L}/corpus/QUALITY.md) should have caught it, or `none`. Fix: a criterion text '(q) a routed defect is re-derived from its source before a fix is built' whose check is the D1 check another seat writes.\n- Also sweep rounds 38–39 lessons and spot-checks for any other unmined mistake and list it.",
         "Draft text ≤25 lines plus the sweep commands and output."),
    item("ExecIndependentOracle", "executor", ["operability", "freshness"],
         "The next frontier step named by the orchestrator: an independent oracle for the sitemap audit. Attacks: whether libxml2 (`xmllint`, installed at /usr/bin/xmllint) agrees with the contract on the E and U witnesses and on the real-run inputs.",
         "- Materialise the counter's witnesses with a fixed seed in {sb}/ (import `witnesses` from {COUNTER} with `random.Random(40001)`); run `xmllint --noout` and `xmllint --noout --schema` with the sitemaps.org XSDs ({L}/.ufo/waves/round-39/sources/ if retained, else GET https://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd) on each witness file; tabulate agreement with the contract outcome per witness; say which disagreements are contract readings (UTF-8-only rule, lane readings) and which would be oracle-checkable claims next round.",
         "A per-witness table (witness, contract outcome, xmllint well-formed, xmllint schema-valid, agree?) and a 5-line summary of what an oracle-backed measured claim could count."),
    item("ReviewScorecardCorrection", "reviewer", OP,
         "The 'Round 39 — closure correction (appended in round 40)' paragraph in {L}/SCORECARD.md and the capability row 'Offline sitemap file audit (round 39, exploratory)'. Attacks: whether the correction states the closure's verdict exactly and leaves no row reading 'pending closure' unexplained.",
         "- Compare with {L}/corpus/lessons/round-39-verifier-spotcheck.md and MANIFEST (/home/vgpnk/Projects/shokunin/MANIFEST.json, read-only, `rounds[523]`).",
         "Holds / overstated / wrong with line numbers."),
]

spec = {
    "wave": "kake-r40-w1",
    "milestone": "r40-controls",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-40/w1",
    "context": CONTEXT,
    "items": ITEMS,
}
(HERE / "w1-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS), "items")
