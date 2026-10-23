#!/usr/bin/env python3
"""Round-41 wave 1: the pre-freeze control wave for C1 (non-author controls scored with the candidate
counter before the declaration), plus source re-opens, reviews of the counter, oracle and reference,
and drafting items. Usage: make_w1_spec.py REV"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
SB = "/fast/scratch/hyaku/kake-r41w1"
SH = "/fast/scratch/hyaku/kake-r41/shared"
W = f"{L}/.ufo/waves/round-41"
COUNTER = f"{W}/c1_count.py"
CONTRACT = f"{L}/.ufo/waves/round-39/c1-contract.md"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"
TOOLING = ("Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — "
           "read /home/vgpnk/.omp/agent/RULES.md first (official channels; record tool, version, channel and reason in your report). "
           "All pacman transactions are PAUSED host-wide (orchestrator ruling 2026-10-20): install via uv tool, npx or an official "
           "binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart.")

CONTEXT = f"""# Goal
Kake round 41, wave 1: measure how well a test counter separates a correct URL-validation repair from cheaper tools, before the round's claim is frozen; plus source re-opens and reviews. The L1 (agent id KakeR41) is the only integrator and scorer; you are one leaf seat. Lane repo: {L} (tip {REV}). Lane axes: operability and freshness. This is ordinary software testing of a local, offline, network-free command-line tool that audits sitemap XML files.

# The planned claim (read {L}/SCORECARD.md section "Round 41 — C1 counter candidate")
C1 repairs the URL judgment of `{L}/scripts/sitemap_audit.py` (contract {CONTRACT}, sentences 4 and 22): a `loc` value or a manifest `sitemapUrl` is valid only when it parses as the RFC 3986 `URI` grammar (Appendix A) with scheme http/https and a non-empty host. Today the tool accepts whatever `urllib.parse.urlsplit` accepts. Candidate counter: {COUNTER} (sha256 2acc443a…). It generates 1434 cases per run from a random seed (one inserted ASCII character or percent sequence in one of six URL components, 630 `loc` + 804 `sitemapUrl`) and labels each with a published RFC 3986 parser (abnf 2.9.1, vendored wheel in {W}/oracle/). Predicate: `met: the tool's judgment of loc and sitemapUrl agrees with the RFC 3986 URI oracle on 1434 of 1434 generated cases`. The base tool scores 1049. The L1's reference repair (read-only) is {SH}/ref_fix.py, its diff {SH}/ref_fix.diff, the base tool {SH}/base.py. It scores 1434.

A "control" is a tool built to SKIP part of the claimed work (see the SCORECARD control classes). If any control reaches 1434/1434, the counter is too weak and the claim is redesigned or declared exploratory — so a control that reaches the target is a valuable finding, not a failure. A tool that fully judges every component against RFC 3986 (however written) is not a control.

# Scoring a tool (control and mutant seats)
`timeout 900 python3 -B {COUNTER} --root {L} --tool-file <your tool> --label <YourName>-<suffix> --out {SB}/<YourName>/<suffix>.json` — exit 0 met, 1 not met, 2 cannot evaluate; about 3 s per run. The receipt lists `passed`, `byField`, `byComponent` and up to 200 `misses`. The counter reads the lane only through read-only `git show`. Run it as often as you like; the L1 re-scores every tool you return.

# Bounds
- You are a leaf: no subagents, no swarm, no verdict on the round.
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report. Never edit files under {SH} or {W}.
- Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git is fine. Never run jj at /home/vgpnk/Projects/shokunin. If you need a clone: `git clone -q {L} {SB}/<YourName>/clone` after unsetting GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE.
- Cap every run with `timeout` (≤900 s), ≤8 parallel processes, `prlimit --as=4000000000`; bound every file you write (≤200 MB per seat; never append in a loop to a file Python imports; never point a log at sitecustomize.py or a .pth); kill every process tree you start before returning. Never run `du` or `find` over /fast/scratch as a whole.
- Network: only URLs your item names, GET only. Never request the operator's properties (ds4cc.com, app.ds4cc.com, operator *.onrender.com hosts, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json).
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- {TOOLING}
- A provider safety or policy refusal or an automatic model switch ends your item: a one-line report saying so; do not rephrase. Message only agent://KakeR41 for blockers; never agent://all. Plain English.

# Result
Report under 60 lines: what you built or checked, exact commands with exit codes, tool paths with sha256, counter results (passed, byField, byComponent, met) for every tool you scored, findings with path:line, and per checked statement: holds / overstated / wrong. An unrun check has not passed. Time box: 30 minutes; a partial report (first line `PARTIAL:`) beats none.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, SH=SH, W=W, COUNTER=COUNTER, CONTRACT=CONTRACT)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR = ["operability"], ["freshness"]
CTL_ACC = ("Tool path(s) and sha256, one counter receipt per tool (passed, byField, byComponent, met), and one line per tool "
           "naming the work it skips and which cases caught it — or, if one reaches 1434/1434, say so in the first line.")


def ctl(name, role, what, how):
    return item(name, role, OP,
                "Baseline tool class: " + what + " Measures: whether the counter scores a tool that skips this work below 1434.",
                "- Build the tool(s) in {sb}/ (start from {SH}/base.py and/or {SH}/ref_fix.py, or from scratch; Python 3 standard library only, as the contract requires). " + how +
                "\n- Keep the skip: the tool must still NOT do the named work. Within that constraint, try hard to reach 1434 (read {COUNTER} to see how cases are built).\n- Score every variant with the counter.",
                CTL_ACC)


ITEMS = [
    ctl("CtlConstantFamily", "executor", "constant and trivial outputs.",
        "Variants: every check clean; every check `check_invalid`; every entry `loc_not_absolute`; both at once; correct exit code with empty stdout; the base tool's output with every URL judgment flipped."),
    ctl("CtlNoReader", "executor", "reads the manifest only and never parses the sitemap files.",
        "Judge `sitemapUrl` as well as you can from the manifest; guess `loc` judgments without parsing XML (e.g. from file sizes or counts)."),
    ctl("CtlIdKeyed", "executor", "answers keyed on check ids or file names.",
        "Base tool plus rules that decide validity from properties of the check `id`, the file name or the manifest name (hash parity, length, characters); no character-level URL judgment beyond the base tool."),
    ctl("CtlPositionKeyed", "executor", "answers keyed on positions or counts.",
        "Base tool plus rules keyed on check order, entry index, number of entries per file or file order; no character-level URL judgment beyond the base tool."),
    ctl("CtlGeneratorShape", "executor", "recognizes the counter's URL templates instead of judging RFC 3986.",
        "Read the case generator in the counter (`make_url`, `fill`, `insert`) and build a tool that exploits its template shapes (e.g. finds the inserted unit by its position or by what the filler can never contain) and decides with a small table, without a per-component RFC 3986 check."),
    ctl("CtlIsolationProbe", "executor", "looks for expected answers outside its case directory.",
        "Write a tool that, inside the counter's bubblewrap run, lists and reads what it can see outside the case directory (/proc entries, mount info, environment, /tmp, parent paths, the counter or lane files if visible) and uses anything label-bearing to answer; otherwise falls back to the base tool. Report exactly what was visible."),
    ctl("CtlCharsetProxy", "executor", "a repertoire test without position.",
        "Base tool plus: reject a value when any character is outside the RFC 3986 character repertoire (unreserved, reserved, `%`), wherever it stands; variants with and without a `%XX` triplet test."),
    ctl("CtlCharTable", "executor", "a per-character validity table that ignores the component.",
        "Base tool plus a 128-entry table (one validity bit per ASCII character, the best single table you can find) applied to every character of the value; tune the table to the counter."),
    ctl("CtlRawBytes", "executor", "judges `loc` by regular expressions over the raw file bytes instead of the parsed XML value.",
        "Base tool for `sitemapUrl` plus a full RFC 3986 check; `loc` only through a regex over the bytes between `<loc>` tags (no XML parsing, no entity decoding)."),
    ctl("CtlAllowList", "executor", "a common-character allow-list.",
        "Base tool plus: accept a value only when every character is a letter, digit or one of `-._~:/?#=&%@+`; variants with a slightly wider or narrower list tuned to the counter."),
    ctl("CtlLocOnly", "mutation-tester", "repairs `loc` only, not `sitemapUrl`.",
        "The reference repair applied only where `loc` values are judged; `sitemapUrl` judged as in the base tool."),
    ctl("CtlSitemapUrlOnly", "mutation-tester", "repairs `sitemapUrl` only, not `loc`.",
        "The reference repair applied only to the manifest `sitemapUrl`; `loc` judged as in the base tool."),
    ctl("CtlNoPct", "mutation-tester", "skips the percent-triplet rule.",
        "The reference repair with `%` accepted as an ordinary character wherever it stands; also a variant that requires only one hex digit after `%`."),
    ctl("CtlNoQueryFragment", "mutation-tester", "skips the query and fragment components.",
        "The reference repair checking scheme, authority and path only; query and fragment accepted as in the base tool. Also a fragment-only skip."),
    ctl("CtlNoUserinfoPort", "mutation-tester", "skips the userinfo and port components.",
        "The reference repair with userinfo and port accepted as in the base tool. Also a userinfo-only and a port-only skip."),
    ctl("CtlNoHost", "mutation-tester", "skips the host component.",
        "The reference repair with any host accepted as in the base tool."),
    ctl("CtlPrintableOnly", "mutation-tester", "rejects printable characters RFC 3986 never allows but not C0 controls or DEL.",
        "Reference repair variant that rejects space and `\"<>\\\\^`{{|}}` and misplaced delimiters, but lets every C0 control and DEL pass."),
    ctl("CtlGenDelimsOnly", "mutation-tester", "checks delimiter structure only.",
        "A tool that checks only the placement of `: / ? # [ ] @` (e.g. no second `#`, no `[` outside an IP literal, no `@` after the host) and nothing else beyond the base tool."),
    item("MutRepertoireDrop", "mutation-tester", OP,
         "The character classes in {SH}/ref_fix.py (`_UNRESERVED`, `_SUB_DELIMS`, `_PCHAR`, the userinfo, reg-name, query and fragment classes). Measures: whether the counter kills every mutant that drops one allowed character from one component.",
         "- Write ≥12 single-change mutants in {sb}/mutants/, each removing one allowed character from one component's class (e.g. `~` from unreserved, `;` from sub-delims, `@` from pchar, `?` from the query class, `:` from userinfo).\n- Score each with the counter.",
         "Per mutant: the one-line change, sha256, counter result; list every survivor (a mutant that reaches 1434) first."),
    item("MutRepertoireAdd", "mutation-tester", OP,
         "The same classes in {SH}/ref_fix.py. Measures: whether the counter kills every mutant that admits one character RFC 3986 does not allow in one component.",
         "- Write ≥12 single-change mutants in {sb}/mutants/, each adding one disallowed character to one component's class (e.g. space, `|`, `^`, `[` in a path, `#` in a fragment, `@` in userinfo, a letter in the port, U+007F).\n- Score each with the counter.",
         "Per mutant: the one-line change, sha256, counter result; list every survivor first."),
    item("MutStructure", "mutation-tester", OP,
         "The structure of `_URI_RE` and `_rfc3986_uri` in {SH}/ref_fix.py. Measures: whether the counter kills every structural mutant.",
         "- Write ≥10 single-change mutants in {sb}/mutants/: percent triplet with one hex digit; hex letters upper-case only; empty host accepted; port optional digits removed; second `@` allowed; path segments allowing `?`; query allowing `#`; scheme allowing a leading digit; anchoring dropped at the end; check applied only when the value contains `%`.\n- Score each with the counter.",
         "Per mutant: the change, sha256, counter result; list every survivor first, and say for each survivor whether it is inside the class the SCORECARD section declares."),
    item("MutPlacement", "mutation-tester", OP,
         "Where `_parse_url` in {SH}/ref_fix.py applies the RFC 3986 check. Measures: whether the counter kills mutants that apply the check to a different string.",
         "- Write ≥8 single-change mutants in {sb}/mutants/: check the `urlsplit(...).geturl()` result instead of the value; check after `.strip()`; check only the first 20 characters; check `value.lower()` with an upper-case-only hex rule; check only `loc` values longer than N; skip the check when the value has a query; etc.\n- Score each with the counter.",
         "Per mutant: the change, sha256, counter result; list every survivor first."),
    item("ExecIndependentBuild", "executor", OP,
         "An independent repair of `_parse_url` written from RFC 3986 Appendix A (https://www.rfc-editor.org/rfc/rfc3986.txt) and the contract {CONTRACT} only — do NOT read {SH}/ref_fix.py or ref_fix.diff.",
         "- Copy {SH}/base.py to {sb}/indep.py and repair the URL judgment yourself (Python 3 standard library only), keeping every other rule as is; non-ASCII code points stay accepted where `unreserved` stands (RFC 3987 IRI characters).\n- Score it with the counter on three seeds; run `python3 -B {L}/scripts/sitemap_audit_selftest.py --tool {sb}/indep.py` and report the PASS line.",
         "Tool path and sha256, three counter receipts, selftest summary, and any case where your reading of RFC 3986 differs from the oracle's label (with the value)."),
    item("ExecSelftestFixtures", "executor", OP,
         "New fixtures for `{L}/scripts/sitemap_audit_selftest.py` covering the RFC 3986 URL rule.",
         "- Read the selftest's fixture format; in a copy at {sb}/selftest.py add ≥12 fixtures with ids `r41_*` (interior C0 control in `sitemapUrl`; space, `|`, `^`, `{{`, DEL in `loc` path; second `#` in fragment; `[` in a path; bad percent triplet; `@` in userinfo; letter in port; plus ≥3 valid controls: sub-delims in path, `%7e`, IPv6 literal host, userinfo with `:`).\n- Show each new fixture red on {SH}/base.py and green on {SH}/ref_fix.py; the 183 old fixtures stay green on both.\n- Keep the selftest's existing style; do not change old fixtures.",
         "Path and sha256 of the selftest copy, a unified diff against the lane selftest, the PASS/FAIL lines on base and reference."),
    item("ReviewCounterCode", "reviewer", OP,
         "The candidate counter {COUNTER} (read-only code review; you may run it).",
         "- Look for judging errors (a case scored as agreeing when it should not, or the reverse), case-plan bugs (entry index, check index, shuffling), generator bugs (a case whose inserted unit lands outside its component), any way the tool can see a label or case identity, exit-code and receipt gaps, and anything that would make the 1434 total or the predicate differ from the SCORECARD text.",
         "Findings with path:line and severity; per SCORECARD statement about the counter: holds / overstated / wrong."),
    item("ReviewOracleFidelity", "reviewer", OP,
         "The oracles: {W}/oracle/abnf-2.9.1-py3-none-any.whl (module `abnf/grammars/rfc3986.py`) and rfc3987-1.3.8 (`rfc3987.py`), against RFC 3986 Appendix A.",
         "- Unzip copies into {sb}/; compare the abnf grammar module's rule text with Appendix A of https://www.rfc-editor.org/rfc/rfc3986.txt rule by rule (URI, hier-part, authority, userinfo, host, IP-literal, IPvFuture, IPv6address, IPv4address, reg-name, port, path-abempty, segment, pchar, query, fragment, pct-encoded, unreserved, sub-delims).\n- Check how `load_oracle` in {COUNTER} decides host and scheme from the parse tree; try ≥10 tricky values of your own on both oracles.",
         "Per rule: equal / differs (quote both); per tricky value: both oracles' answers; findings with path:line."),
    item("ReviewReferenceDiff", "reviewer", OP,
         "The L1 reference repair {SH}/ref_fix.diff against RFC 3986 Appendix A and the contract {CONTRACT}.",
         "- Check every character class and the regex structure against the ABNF; the IP-literal handling; what changes for non-ASCII values, ports above 65535, IPv4 hosts and empty ports compared with the base; whether any other contract sentence changes behaviour; whether the code keys on anything the counter generates.",
         "Findings with path:line and severity; per out-of-class choice in the SCORECARD section: holds / overstated / wrong."),
    item("CriticPredicate", "critic", OP,
         "The SCORECARD section \"Round 41 — C1 counter candidate\" against the claim-sizing rules in /home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-41.md §6 item 9 and QUALITY (n), (o), (r) in {L}/corpus/QUALITY.md.",
         "- Read only; do not run code. Check: one predicate that is the same sentence in plan, code and receipts; whether a do-nothing control or a shortcut could reach the target; axis named by surface; universal clauses; whether the control classes name only tools that skip declared work; whether every pre-section tool is named by sha256; whether the harm rule is decidable.",
         "Per rule: holds / overstated / wrong with SCORECARD line numbers."),
    item("CriticClassScope", "critic", OP,
         "The class C1 claims (six components, ASCII units, the percent sequences) and its stated exclusions (non-ASCII, IP-literal contents, ports above 65535) in the SCORECARD section.",
         "- Read only. Is the class what routed defect 4 of {L}/corpus/lessons/round-40-verifier-spotcheck.md asked for? Is the 'not a control' sentence sound under QUALITY (n)? Are the exclusions decided by source (S102 names RFC 3987) or by convenience? What would a closure seat say the claim does not show?",
         "Per statement: holds / overstated / wrong with reasons."),
    item("ScoutReopenS117", "scout", FR,
         "RFC 3986 as a source for the claim (planned row S117; existing row S098 in {L}/corpus/SOURCES.md covers §2 only).",
         "- GET https://www.rfc-editor.org/rfc/rfc3986.txt ; compare sha256 with {W}/sources/SHA256SUMS and S098's retained sha256.\n- Locate `URI = scheme \":\" hier-part [ \"?\" query ] [ \"#\" fragment ]` (§3 and Appendix A), `port = *DIGIT`, `reg-name`, `pchar`, `query`, `fragment`, and §4.3 absolute-URI; give line numbers.",
         "Located lines with numbers; sha256 comparison; whether S098's `teaches` overlaps the planned row."),
    item("ScoutReopenOracles", "scout", FR,
         "The two oracle packages as sources (planned rows S118 abnf 2.9.1, S119 rfc3987 1.3.8).",
         "- GET https://pypi.org/pypi/abnf/2.9.1/json and https://pypi.org/pypi/rfc3987/1.3.8/json ; compare the wheel sha256 digests with `sha256sum {W}/oracle/*.whl`; record summary, author, license, upload time and project URLs.\n- GET https://github.com/declaresub/abnf (HTTP status only plus the README line naming bundled grammars, if any).",
         "Per package: digest equal / differs, metadata lines, located quotes (≤25 words)."),
    item("ScoutIRIRule", "scout", FR,
         "The non-ASCII exclusion: S102's RFC 3987 sentence and RFC 3987 itself.",
         "- GET https://www.sitemaps.org/protocol.html and locate \"Please check to make sure that your URLs follow the RFC-3986 standard for URIs, the RFC-3987 standard for IRIs\"; and the escaping example that follows it.\n- GET https://www.rfc-editor.org/rfc/rfc3987.txt and locate `iunreserved`, `ucschar` and `iprivate`.",
         "Located quotes with line numbers; whether 'non-ASCII stays accepted where unreserved stands' is supported, overstated or wrong."),
    item("SentinelSandbox", "sentinel", OP,
         "The isolation of the tool run in {COUNTER} (`sandbox_argv`, `layout`, `main`). Read-only review; you may run the counter on harmless tools you write in {sb}/.",
         "- Decide what a tool under test can observe (paths, mounts, /proc, environment, timing, other processes), whether anything observable correlates with a case label, and whether a tool can write anything the counter later reads.",
         "Findings with path:line and severity; per SCORECARD sandbox statement: holds / overstated / wrong."),
    item("ConnectorSiblingOverlap", "connector", OP,
         "Other tools that judge URLs with `urlsplit`: {L}/scripts/ (robots_audit.py, link_preview_audit.py, source_recheck.py, others) and, read-only, sibling lane repos under /home/vgpnk/Projects/shokunin/*-shokunin/scripts/.",
         "- Find every place a URL's validity is decided by `urlsplit`/`urlparse` acceptance; say which would share the defect C1 repairs and which belong to another lane (report only; no edits).",
         "Table: file:line, what is judged, shares the defect yes/no, owning lane."),
    item("ReviewR40Restatement", "reviewer", OP,
         "Round-40 spot-check routed defect 1 ({L}/corpus/lessons/round-40-verifier-spotcheck.md): restate the round-40 control tally over live seats only.",
         "- From committed bytes (`git -C {L} show 8eb121c8:<path>` or `git archive 8eb121c8 .ufo/waves/round-40/verification/w1 | tar -x -C {sb}`), recount `jq -s 'map(select(.met))|length'` over all receipts and over the receipts not from the dead seat `CtlUTabOnly`; list the dead seat's receipts apart.",
         "The two counts with commands and exit codes; the exact sentence the round-41 correction should carry."),
    item("ScribeLessonDraft", "scribe", OP,
         "Draft text for `## Mistakes` of {L}/corpus/lessons/round-41.md from {L}/corpus/lessons/round-40-verifier-spotcheck.md routed defects 1–3 (dead-seat leftovers counted; revised build checked only by the L1; counter exposing witness ids).",
         "- For each: class · evidence pointer · captured-by · fix, in the shape of {L}/corpus/lessons/round-40.md Mistakes. Name for each fix how it can be shown able to fail (a check that is red on round 40's bytes).\n- Write the draft into your report only.",
         "The draft entries, each with resolvable evidence pointers."),
    item("ScribeSkillAmendment", "scribe", OP,
         "Draft the SKILL.md amendment for the sitemap audit's URL rule: read {L}/SKILL.md (grep `sitemap_audit`) and the SCORECARD section.",
         "- Draft ≤12 lines in the existing style stating the RFC 3986 rule, its source rows (S102, planned S117), the out-of-class choices and the counting command; no claim of admission.\n- Write the draft into your report only.",
         "The draft text and the SKILL.md line numbers where it would go."),
]

spec = {
    "wave": "kake-r41-w1",
    "milestone": "r41-controls",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-41/w1",
    "context": CONTEXT,
    "items": ITEMS,
}
(HERE / "w1-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS), "items")
