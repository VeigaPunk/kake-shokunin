#!/usr/bin/env python3
"""Write the round-38 wave-1 spec (w1-spec.json) next to this file. Usage: make_w1_spec.py REV"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
DECL = "b0ab7f606d1f61fb6b850785866ba71583f629cc"
BASE = "af43a50fa399881eead9381d835b78a015e277a6"
SB = "/fast/scratch/hyaku/kake-r38w1"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"
TOOLING = """Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, record tool, version, channel and reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via uv tool, npx or an official binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart."""

CONTEXT = f"""# Goal
Kake round 38, wave 1 (build + first falsifiers). The L1 (KakeR38) holds the planner and integration seat; you are one leaf seat. Lane repo: {L}. Lane axes: operability and freshness (web properties and publishing). Each item names what it builds or attacks; attacks try to show work is wrong, overstated or harmful, with reproducible evidence. Time box: finish and write your report within 30 minutes; a partial report (first line `PARTIAL:`) beats none.

# Declared claim (SCORECARD.md "Round 38 — C2 declared", at {REV}; C1 was declared at {DECL} and WITHDRAWN before any build at {REV} because controls of its declared kinds met its predicate; base {BASE}). Read: `git -C {L} show {REV}:SCORECARD.md | sed -n '/^## Round 37 — closure correction/,$p'`.
- C2 (operability, tool repair; the redesign of C1): `scripts/robots_audit.py` gains three contract rules — (h) non-JSON number literals (NaN, Infinity, -Infinity → input_invalid) and integers of any length (out-of-range status → check_invalid; unused long numbers change nothing), (i) URL characters (ASCII outside the RFC 3986 character set anywhere in `url` → check_invalid; non-ASCII kept), (k) the implicit /robots.txt allow compared on the normalized path to match. The round-37 contract ("Round 37 — declared claims") holds except where (h), (i), (k) change it. Frozen predicate `met: passed >= 20 of 20 sealed cases`; counter {L}/.ufo/waves/round-38/sealed_count_v3.py (C1's withdrawn counter sealed_count.py stays its rule of record). Before: 8 of 20 at base. Harm instruments: round-37 counter 28/28 (key 424aa248) and `scripts/robots_audit_selftest.py` 137/137 must hold at the build.
- Round-37 closure (non-author): {L}/corpus/lessons/round-37-verifier-spotcheck.md — round-37 C1 NOT admitted (a stdlib-plus-patches control met its predicate before the build and the lane kept the claim). Routed defects 1–6 there are this round's repairs.
- Control receipts (committed before this wave): {L}/.ufo/waves/round-38/verification/ (control-*.json and mutref/ under C1's v2 counter; v3/*.json and c2-at-af43a50f.json under C2's v3 counter) and control seat reports {L}/.ufo/waves/round-38/ctl/. Control tool files: {L}/.ufo/waves/round-38/retained/controls/.
- Sources registry {L}/corpus/SOURCES.md (rows S001–S097; contract in /home/vgpnk/Projects/shokunin/CORPUS.md section "SOURCES.md — where a shokunin learns"). Rows this round bears on: S034 (RFC 8259), S029 and S089 (RFC 3986), S011 (RFC 9309), S095 (Google robots spec), S096 (google/robotstxt).

# Sealed key — binding
The 20 C1 and C2 cases are sealed outside the lane. Never list, read, stat, search or open anything under /fast/scratch/hyaku/kake-r38/ or /fast/scratch/hyaku/kake-r38ctl/ (those exact directories and below; your sandbox is the different directory {SB}/<YourName>/), never look for the cases anywhere, and never run the round-38 counters (you have no key). A seat that touches those trees by mistake says so in its report's first line. The round-37 counter and key (revealed at 424aa248) are public: any seat may run them in its own sandbox clone.

# Bounds
- You are a leaf: no subagents, no swarm, no admission or verdict on the round. (An executor may spawn one read-only labrat probe for a falsifiable hypothesis; nothing else.)
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report — deliverables (code, fixtures, prose drafts, patches) stay in your sandbox; name their absolute paths and sha256 in the report; the L1 copies after review.
- Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git (show, log, ls-tree, diff) is fine. Never run any jj command at /home/vgpnk/Projects/shokunin.
- Code that writes files or Git state runs only in your sandbox (clone with `git clone -q {L} {SB}/<YourName>/clone && git -C {SB}/<YourName>/clone checkout -q {REV}`; export TMPDIR={SB}/<YourName>/tmp after creating it). Unset GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE before any git command. Cap every run with `timeout` (≤900 s), ≤8 parallel processes, and memory (e.g. `prlimit --as=4000000000`) for inputs that may blow up; kill any process tree you started before returning.
- Owned sites: no requests to the operator's web properties (ds4cc.com, app.ds4cc.com, operator *.onrender.com hosts, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json) unless your item names it.
- Network: only seats whose item names a public URL to open may fetch, GET only, ordinary means; never pass a bot challenge or access control; a page you cannot open is recorded as unopened.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- {TOOLING}
- A provider safety or policy refusal or an automatic model switch ends your item: write a one-line report saying so; do not rephrase. The only message target is agent://KakeR38 (the L1), for blockers only; never agent://all. Write plain English.

# Result
Report under 80 lines: what you built or attacked, exact commands with exit codes, observed outputs, evidence pointers (path:line, hash). An unrun check has not passed; say what you did not verify. Your findings are advisory input for the L1 and the non-author closure.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, BASE=BASE)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR = ["operability"], ["freshness"]
BOTH = ["operability", "freshness"]
CON = "the round-38 contract (round-37 contract plus amendments (h), (i), (k))"

ITEMS = [
    # ---- C1 build and its instruments
    item("ExecRobotsTool", "executor", OP,
         "Build C2: amend `scripts/robots_audit.py` to " + CON + " (with the C2 clarifications in SCORECARD 'Round 38 — C2 declared') in your clone {sb}/clone at {REV}. You are the only seat writing the landed tool. Write it yourself from the contract: do not open {L}/.ufo/waves/round-38/retained/controls/ (control tools, some of which implement the rules) or the ctl/ reports' code.",
         "- Change only what (h), (i), (k) require; keep every round-37 behaviour (the round-37 counter with key 424aa248 must still read 28 of 28 and `scripts/robots_audit_selftest.py` 137/137 on your file: run both in your clone: `python3 -B .ufo/waves/round-37/sealed_count.py --root {sb}/clone --tool-file <file> --key-revision 424aa248` and `python3 -B scripts/robots_audit_selftest.py --tool <file>`).\n- (h): reject NaN/Infinity/-Infinity outside strings (json `parse_constant`); integers of any length parse without Python's 4300-digit ValueError and without quadratic int conversion (a manifest within the 64 MiB cap made mostly of digits must finish in a few seconds; measure it); an out-of-range long `robotsStatus` is `check_invalid`; `checksEvaluated` must stay exact (the v3 counter compares it).\n- (i): judge `url` characters as written, before urlsplit.\n- (k): compare the normalized path to match with `/robots.txt`.\n- Update the module docstring's readings (it states the old raw-path reading). Python3 stdlib only; no network, writes or subprocess.\n- Self-check on at least 15 manifests you write from the amendment text (include `NaN` inside a string, `1e400`, `-0`, `%2e`, `/robots.txt?x`, a trailing space, a non-ASCII URL).",
         "Patch (diff vs {BASE}) and final file with sha256; round-37 counter 28/28 and selftest 137/137 on it (commands, exits); your 15+ manifests with outputs; timing of the 64 MiB digits manifest."),
    item("ExecRobotsSelftest", "executor", OP,
         "Extend `scripts/robots_audit_selftest.py` (copy from {REV} into {sb}/) with fixtures for " + CON + " AND for the urllib.robotparser departures in (c)/(d), written blind from the contract text. Do not read or wait for the builder's tool.",
         "- New fixtures (keep all 137 existing ones unchanged): (h) NaN/Infinity/-Infinity at top level, in a check field, inside a string (valid), a 5000-digit status, a 6000-digit unused number, `1e400` status; (i) each excluded ASCII class (space, controls, DEL, `\"<>\\\\^`{{|}}`), leading/trailing, non-ASCII kept, `%7C` valid; (k) `/robots%2Etxt`, `/%72obots.txt`, `/robots%2etxt`, `/robots%2Ftxt`, `/robots.txt?x`, `/ROBOTS.TXT`, fragment, 5xx; (c)/(d) stdlib departures: substring UA (googlebot vs googlebot-news both ways), crawl-delay between user-agent lines, same-name groups combined, Kelvin-sign name, `*` rule length vs matched length (Allow /abc + Disallow /*), Disallow /private/ + Allow /*.html, ties allow, non-final `$`. Map each to its sentence.\n- Show the new selftest passes on the base-tool-plus-amendments as YOU implement it minimally in {sb}/mini.py (blind, from the contract) and that the base tool ({BASE}) fails exactly the (h)/(i)/(k) fixtures; run it on {L}/.ufo/waves/round-37/retained/controls/CtlC1Shortcut-followup-robots_audit.py and list what it fails.",
         "New selftest file + sha256, fixture count, results on mini.py, base tool and the r37 shortcut (commands, exits)."),
    item("ExecIndependent", "executor", OP,
         "Independent blind implementation of " + CON + " at {sb}/independent_robots_audit.py, starting from the round-37 independent implementation `git -C {L} show {REV}:.ufo/waves/round-37/retained/independent/independent_robots_audit.py` (find its exact path with `git ls-tree -r --name-only {REV} .ufo/waves/round-37/retained/independent`).",
         "- Apply (h), (i), (k) yourself from the amendment text; do not read the builder's work. Also fix its round-37 NUL-path crash (`r\\u0000.txt` must give check_invalid; w2/ReviewRobotsTool.md side finding).\n- Run the round-37 counter on it (`python3 -B .ufo/waves/round-37/sealed_count.py --root <clone> --tool-file <file> --key-revision 424aa248`, must stay 28/28) and the 137 selftest.",
         "File + sha256; r37 counter and selftest results with exits; list of readings you chose where the text left room."),
    item("ExecQualityJCheck", "executor", OP,
         "QUALITY (j) has no executable check (round-37 closure routed defect 3). Write `{sb}/control_consequence_check.py` (to land as .ufo/waves/round-38/criteria/control_consequence_check.py).",
         "- Input: a round's verification directory (`--verification DIR`, plus `--root` and `--revision` to read it from git). Rule: group every JSON receipt by `counterSha256`; a receipt whose file name starts with `control-` (or which sits under a `controls/` or `pre/` path and is named as a control) and has `met: true` makes that counter tainted; any non-control receipt (a claim measurement such as c1-*.json) with `met: true` under a tainted counter is a violation → exit 1 with the list; else exit 0; unreadable input exit 2. Document the receipt-naming convention it relies on.\n- Show it able to fail: exit 1 on round 37 (`.ufo/waves/round-37/verification` at {REV}: control-CtlC1Shortcut-followup met true and c1-keyrev-at-9dbc88bb met true share a counter); exit 0 on round 36 and on a constructed compliant directory; exit 0 or 1 on round 38's current receipts as they are (report which).",
         "Script + sha256; red run on round 37, green runs, commands and exits."),
    item("ExecReceiptPin", "executor", OP,
         "Round-37 closure routed defect 5: post-measurement selftest receipts named the tool by path only. Write `{sb}/pinned_selftest.py` (to land as .ufo/waves/round-38/pinned_selftest.py) and a pinned re-run receipt for round 37's postfix tool.",
         "- pinned_selftest.py: `--root R --revision REV --tool PATH --selftest PATH --out FILE` runs the selftest on the tool read from git at REV (written to a temp file), and writes a receipt with the selftest's JSON summary plus `toolPath`, `toolRevision`, `toolSha256`, `selftestRevision`, `selftestSha256`, UTC time; exit = selftest exit.\n- Produce `{sb}/r37-postfix-selftest-pinned.json`: the 137 selftest at {BASE} on `scripts/robots_audit.py` at {BASE} (expect sha256 944d2f51…d3e5, 137/137) and show the sha256 equals the round-37 tip tool named in the closure.",
         "Script + sha256; pinned receipt with sha256 fields; command and exit."),
    item("ExecRecheckCaps", "executor", BOTH,
         "Carried round-37 defects in `scripts/source_recheck.py`: body reads are uncapped (a 1 GiB body → MemoryError, w2/SentinelHardening.md) and a ~60 MiB manifest can raise MemoryError inside json.loads. Work in your clone {sb}/clone at {REV}.",
         "- Read {L}/.ufo/waves/round-37/w2/SentinelHardening.md and ReviewRoutedClosure.md. Smallest fix inside the round-36 contract (a body larger than a stated cap is an input fault for that check, not a crash; the manifest cap is the existing 64 MiB). Fixtures in scripts/source_recheck_hardening_selftest.py (existing file) red on {REV}, green on the fix; `scripts/source_recheck_selftest.py` must stay all-pass and the round-36 sealed counter (`.ufo/waves/round-36/sealed_count.py --key-revision fd1fb723`) must stay 28/28 on the fixed tool. Run blow-up inputs under `prlimit --as=2000000000` and `timeout`.",
         "Patch + sha256; red/green fixtures; selftest and r36 counter on the fix; commands and exits."),
    item("ExecRealRunPrep", "executor", BOTH,
         "Real input for C2 after the build: extend the round-37 real-run manifest ({L}/.ufo/waves/round-37/realrun/) with checks that exercise (h), (i), (k) on the same 12 retained live robots.txt files, at {sb}/realrun/.",
         "- Reuse the retained robots files (no new fetch). Add 2–3 checks per host whose URLs use `%2E`/`%72` escapes of /robots.txt, a URL with an excluded character (expect check_invalid), and an ordinary percent-encoded path; set `expect` from the rules of that host's file, quoting the deciding line.\n- Run the base tool ({BASE}) on it and record exit/report; the L1 runs the built tool later.",
         "manifest.json + receipts; base-tool run output; per-check justification lines."),
    # ---- sources (scouts reopen; scribes draft)
    item("ScoutReopenS034", "scout", FR,
         "Live re-open of S034 RFC 8259 https://www.rfc-editor.org/rfc/rfc8259.txt (sections 6 Numbers and 9 Parsers).",
         "- GET it (ordinary means); quote exactly (≤25 words, with section) the sentence excluding Infinity and NaN, and the sentence on implementation limits for numbers (range and precision). Record UTC access time, status, final URL, sha256 of the body. Say whether the round-38 (h) amendment reads it correctly, including the 'number of any length is JSON' reading.",
         "Located quotes with section, access time, status, sha256; verdict on (h)."),
    item("ScoutReopenRFC3986s2", "scout", FR,
         "Live open of RFC 3986 sections 2, 2.1, 2.2, 2.3 and 2.4 and Appendix A/C https://www.rfc-editor.org/rfc/rfc3986.txt (registry rows S029 and S089 hold other sections of this RFC).",
         "- Quote (≤25 words each, with section) the character-set sentence, the reserved and unreserved sets, and anything on whitespace or delimiting (Appendix C). Check the round-38 (i) allowed set character by character against sections 2.2/2.3 plus `%`; name any character the amendment wrongly allows or excludes. Record access time, status, sha256.",
         "Quotes with sections; per-character check of (i); access receipt."),
    item("ScoutReopenS011", "scout", FR,
         "Live re-open of S011 RFC 9309 https://www.rfc-editor.org/rfc/rfc9309.html section 2.2.2 (percent-encoding before comparison, implicit /robots.txt allow) and 2.2.3.",
         "- Quote the sentences (≤25 words each) on '/robots.txt URI is implicitly allowed' and on unencoding percent-encoded octets before comparison. Argue whether the round-38 (k) reading (normalize, then compare with /robots.txt; query and case break it) follows; compare with the retained text {L}/.ufo/waves/round-37/sources/S011.txt (same bytes?). Record access time, status, sha256.",
         "Quotes with sections; (k) verdict; diff against retained text."),
    item("ScoutPythonJson", "scout", FR,
         "Open the Python documentation for json (https://docs.python.org/3/library/json.html) and for the integer string conversion length limit (https://docs.python.org/3/library/stdtypes.html#int-max-str-digits).",
         "- Quote (≤25 words) where the docs say json accepts NaN/Infinity outside the spec and how `parse_constant`/`parse_int` work; quote the 4300-digit limit and its ValueError. These explain the round-37 tool defects D2/D3 ({L}/.ufo/waves/round-37/w2/ReviewRobotsTool.md). Record access time, status, sha256; verify each claim with a one-line python3 run on this host (version).",
         "Quotes, access receipt, python version and one-line confirmations."),
    item("ScoutWhatwgUrl", "scout", FR,
         "Open the WHATWG URL Standard https://url.spec.whatwg.org/ (basic URL parser: leading/trailing C0 control or space, ASCII tab or newline removal) and Python's urllib.parse docs (https://docs.python.org/3/library/urllib.parse.html, urlsplit and its WHATWG-like stripping).",
         "- Quote (≤25 words each) the parser steps that strip or remove these characters and the validation-error notes. Contrast with the round-38 (i) amendment (which rejects them as written): is rejecting them a defensible publisher-side lane reading? Candidate registry decision for each page (admit as contrast/counterexample or reject with reason). Record access time, status, sha256.",
         "Quotes with step names; contrast verdict; candidate row decisions."),
    item("ScoutGoogleImplicit", "scout", OP,
         "Does Google's parser (S096 github.com/google/robotstxt robots.cc) or Google's spec (S095) normalize the path before the implicit /robots.txt allow, and how does it treat `%2E`, query and case there?",
         "- Read robots.cc on GitHub (cite file:line at the commit you read) and the S095 page section on URL matching. Report agree/differ/silent with the round-38 (k) amendment, with quotes.",
         "Findings with file:line or quotes; agree/differ/silent per (k) sentence."),
    item("ScribeSourcesRows", "scribe", FR,
         "Draft corpus/SOURCES.md row changes and Gate lines for this round at {sb}/sources-rows.md: S034 re-open (recheck note), a new RFC 3986 section-2 row (scope distinct from S029 section 3 and S089 section 5.2), S011 re-open note, candidate rows for Python json docs and WHATWG URL (admit or reject with reason and flip).",
         "- Read {L}/corpus/SOURCES.md (header, rows S088–S097 for shape, the notes block at the end) and /home/vgpnk/Projects/shokunin/CORPUS.md 'SOURCES.md — where a shokunin learns'. Open each URL yourself (GET) so every quote is located by you: rfc8259.txt section 6, rfc3986.txt section 2.2/2.3, rfc9309.html 2.2.2, docs.python.org json, url.spec.whatwg.org. Each Gate line: URL — accessed UTC, HTTP status — decision, tier, kind, status: reason; quote “…” (section) ≤25 words; prove each quote with a pasted grep over your saved copy.",
         "Rows in column shape; Gate lines with grep proofs; status/recheck/used-by changes listed old→new."),
    item("ScribeKnowledgeEntry", "scribe", OP,
         "Draft an appended section for corpus/knowledge/robots-txt-rules.md at {sb}/robots-entry-r38.md: the round-38 readings (h), (i), (k) as publisher knowledge, each sentence citing a row and section (S034 RFC 8259 §6, RFC 3986 §2, S011 RFC 9309 §2.2.2).",
         "- Read {L}/corpus/knowledge/robots-txt-rules.md at {REV}. Find every sentence there that the (k) amendment makes stale (the raw-path reading of the implicit allow) and draft an append-only correction, never a rewrite. Mark lane readings as such. Under 40 lines.",
         "Draft with per-sentence cites; stale sentences listed with path:line and the correction text."),
    item("ScribeMistakeMine", "scribe", OP,
         "Draft `## Mistakes` rows for corpus/lessons/round-38.md at {sb}/mistakes.md: class · evidence pointer · captured-by · fix, from the round-37 closure disagreements.",
         "- Candidates: (1) a control met the frozen predicate and the lane kept the claim by reclassifying the control (spot-check C1 ruling; captured-by QUALITY (j), which had no check); (2) a dead seat's item was built by a living seat (prompt §6 'Never replace a dead seat'); (3) a declared order ('control receipts before any build') broken by 7 min 15 s; (4) a post-measurement receipt named the tool by path only. For each fix name a check that can be shown to fail on the old state (e.g. the control-consequence check this wave builds; a timeline check comparing control-receipt commit time with the build dispatch time in w1-dispatched-at.txt). Write the timeline check as a small script in {sb}/ and run it red on round 37 ({L}/.ufo/waves/round-37) and green on a fixed layout.",
         "Mistake rows; timeline-check script + sha256 with red and green runs pasted."),
    item("ScribeQualityCriteria", "scribe", OP,
         "Draft QUALITY.md 'Round-38 criteria' at {sb}/quality-r38.md from the round-37 closure routed defects 2–5 and this round's design.",
         "- Read {L}/corpus/QUALITY.md tail (round-36 and round-37 criteria (a)–(j)) for shape. Each criterion: rule · motivating lesson path · enforcing check and red-before receipt (or 'no check yet'). Include: (k) dead seats are reported unbuilt, never handed to a living seat; (l) post-measurement receipts carry tool sha256; (m) control receipts commit before the build wave's dispatch time; plus the (j) check this wave builds (ExecQualityJCheck) as (j)'s check.",
         "Criteria with grounding paths and check status per criterion."),
    item("ScribeProvinceStep", "scribe", OP,
         "Draft the PROVINCE.md 'Round-38 robots audit repair step' and a corpus/README.md coverage line at {sb}/province-r38.md.",
         "- Read {L}/PROVINCE.md round-37 step and {L}/corpus/README.md coverage rows for round 37. State: round-37 capability not admitted; round 38 re-claims the tool's (h)/(i)/(k) rules under a counter that separates it from a stdlib-delegating reader; what stays open (live fetch, redirects, caching, crawler extensions, the two round-37 undecided points: symlinked manifest directory and U+FFFD per byte). Under 20 lines each.",
         "Two drafts, each sentence traceable to the declaration or a source row."),
    item("ConnectorSiblings", "connector", OP,
         "Sibling-overlap scan for round 38: which other lanes under /home/vgpnk/Projects/shokunin/*-shokunin hold rules or tools for strict JSON parsing (NaN/Infinity, long integers), URL character validation, or robots.txt.",
         "- Read-only grep of sibling PROVINCE.md, SKILL.md, corpus/knowledge and scripts; name overlaps, reusable patterns, conflicting readings (e.g. a sibling that accepts NaN or strips whitespace from URLs), and province boundaries (tabi: client-side crawler discipline; kake: publisher-side).",
         "Overlap table with paths; boundary statement."),
    item("ScoutPlanWalk", "scout", OP,
         "Planning data-walk (the L1 holds the planner seat; this item is its bounded data-walk): map every routed defect (1–6) of {L}/corpus/lessons/round-37-verifier-spotcheck.md and every 'Carried open' item of {L}/corpus/lessons/round-37.md to this round's work at {REV}.",
         "- For each item: addressed now (by which file at {REV} or which named wave-1 item from the declaration's plan), carried (why acceptable), or missing. Also check the SCORECARD correction at {REV} against routed defect 1 word by word.",
         "Table per item with disposition and evidence pointer."),
    item("ScoutCorpusStale", "scout", FR,
         "Freshness of the lane's own robots statements: which sentences in {L}/corpus/knowledge, {L}/SKILL.md, {L}/PROVINCE.md, {L}/corpus/README.md and the round-37 lesson state readings that (h), (i), (k) change (raw-path implicit allow, NaN accepted, urlsplit stripping) or claim round-37 admission.",
         "- grep and read; list each sentence with path:line, what changes, and whether an append-only correction is needed.",
         "List with path:line and needed correction."),
    # ---- first falsifiers
    item("CriticControlReceipts", "critic", OP,
         "Attack the round-38 control receipts and the C1 withdrawal at {REV} ({L}/.ufo/waves/round-38/verification/ and ctl/ reports): were the controls strong enough, scored with the frozen counter, committed before this wave, and honestly reported in SCORECARD?",
         "- Check every control seat report against its receipt (sha256 of the tool named in the report = `toolSha256` in the receipt; counterSha256 = v2 52daff55…6e7b for control-*.json and mutref/, v3 for v3/*.json). Was withdrawing C1 (rather than keeping it) what its declaration required, and does the C2 declaration's control-class list (named before v3 scores) amount to reclassifying a control after it scored? Argue both sides with quotes.. Design one more control you think the call missed (describe it concretely; build it in {sb}/ if cheap and give sha256 for the L1 to score).",
         "Per-receipt check table; missed-control design with sha256 if built."),
    item("CriticContractAmbiguity", "critic", OP,
         "List every point the (h), (i), (k) amendments leave undecided or decide two ways.",
         "- For each, a concrete manifest + robots file where two careful readers give different reports (e.g. `-Infinity` vs `-1e400`, a NaN inside a nested object, `%` not followed by two hex digits, IPv6 brackets, `/robots.txt;x`, `/./robots.txt`, a trailing `?`, `%2E` in the host). Classify each: changes a sealed-style check / edge only.",
         "Numbered list with inputs and the two readings."),
    item("CriticClaimSizing", "critic", OP,
         "Claim-sizing attack on the round-38 C2 declaration and the C1 withdrawal (prompt /home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-38.md §6 item 9; the closure rulings in {L}/corpus/lessons/round-37-verifier-spotcheck.md).",
         "- One concrete after-value re-derivable by one command? Universal clauses? Axis named by surface? Do (g)/(d) count rows a rule the lane already holds (and is that disclosed as separation, not the move)? Predicate same sentence in plan, `sealed_count.py` and receipts? Does the closure correction append rather than rewrite? Quote each sentence you attack.",
         "Per rule: holds / breaks with quoted sentence and fix."),
    item("ReviewCounterV2", "reviewer", OP,
         "Review {L}/.ufo/waves/round-38/sealed_count.py against the round-37 counter (diff them) for correctness and leaks, without the key.",
         "- Check the rawTemplate path: token regexes, fresh ids per token, @FILE substitution for names that do not exist (KeyError?), ids appearing inside strings, expected-findings mapping, a token that appears in a robots file. Exercise with a dummy key of your own in a sandbox copy (change KEY_SHA256 in the copy).",
         "Findings with line numbers, reproducer commands and severity."),
    item("SentinelManifestDoS", "sentinel", OP,
         "Adversarial inputs for the (h)/(i) parse paths: deep nesting, 64 MiB of digits, many long numbers, huge exponents, many checks with long URLs; measure the BASE tool ({BASE}) now and write the inputs so the L1 can re-run them on the build.",
         "- Under `timeout 60` and `prlimit --as=4000000000`, time each input on the base tool; report crashes, tracebacks, timeouts, memory errors. Save inputs as files in {sb}/inputs/ with a runner script {sb}/run.sh TOOL that prints exit/time per input.",
         "Input set + runner + sha256; base-tool timing table."),
    item("ProbeDigits", "executor", OP,
         "Hypothesis: Python's json with a custom parse_int that never calls int() on strings longer than N digits parses a 64 MiB manifest of digits in under 5 s, while default json.loads raises ValueError above 4300 digits and `sys.set_int_max_str_digits(0)` makes it quadratic.",
         "- Measure on this host (python3 version), each run under `timeout 120` and `prlimit --as=4000000000`, in {sb}/. Report times for 10^3..10^7 digits for each variant.",
         "Timing table; hypothesis confirmed or refuted."),
    item("ProbeUrlsplit", "executor", OP,
         "Hypothesis: Python's urllib.parse.urlsplit silently removes tab, CR and LF anywhere and strips leading C0 controls and spaces, so the base tool accepts URLs holding them; every other ASCII character outside RFC 3986 passes through unchanged.",
         "- For each of the 128 ASCII characters, at start, middle of path and end of a URL, record urlsplit's result and the BASE tool's ({BASE}) decision on a one-check manifest (expect allow, robots `Disallow: /a`, URL `http://h.example/a<ch>`). Table in {sb}/table.json.",
         "Table summary: which characters are dropped, stripped, kept, or raise; base-tool verdict per class."),
    item("ReviewCorrection", "reviewer", OP,
         "Review the round-38 SCORECARD 'Round 37 — closure correction' and the declaration's handling of routed defects 1, 2, 5 at {REV} against {L}/corpus/lessons/round-37-verifier-spotcheck.md.",
         "- Is the correction appended (not rewriting earlier lines: `git diff {BASE} {REV} -- SCORECARD.md` shows only additions)? Does it state non-admission and the Capabilities rows' status exactly? Is the round-37 counter kept as rule of record? Is anything overstated?",
         "Findings with quoted lines and fixes."),
    item("RevengerExemption", "revenger", OP,
         "Reverse-engineer the round-37 choice of the raw-path implicit /robots.txt allow (tool docstring at {BASE} lines 40–60) and the NaN/urlsplit behaviour: who chose it, what evidence the round-37 seats had (w1/ExecRobotsTool.md, w2/ScoutContractAmbiguityR37.md, w2/ReviewRobotsTool.md D2–D5), and whether the round-38 amendments contradict any round-37 sealed case or selftest fixture.",
         "- Run the 137 selftest and the round-37 counter (key 424aa248) in a sandbox clone against a quick local patch of the base tool implementing only (k), only (i), only (h); report any fixture or sealed case that flips.",
         "Origin narrative with pointers; flip table per amendment."),
    item("MutBaseSelftest", "mutation-tester", OP,
         "Which single-point mutants of the base tool ({BASE}) in the (c)/(d) code (user-agent matching, folding, group combining, group continuation, rule length, ties, `$`, `*`) survive the current 137-fixture selftest?",
         "- Write 15–25 mutants in {sb}/mutants/ (one change each) and run `python3 -B scripts/robots_audit_selftest.py --tool <mutant>` from a sandbox clone at {REV}; table of survivors with the sentence broken. These inform fixture additions; do not edit the selftest.",
         "Mutant table with selftest result per mutant and survivors named."),
    item("ReviewHarmBaseline", "reviewer", BOTH,
         "Harm baseline at the base {BASE}: every lane selftest and replayable counter, so the L1 can compare the build against it.",
         "- In a sandbox clone at {REV}, run with `timeout 900` each lane selftest (find exact names with `ls scripts/*selftest*`; read each file's usage line), plus the round-37 counter on scripts/robots_audit.py at {BASE} (key 424aa248) and the round-36 counter (`.ufo/waves/round-36/sealed_count.py --revision {BASE} --key-revision fd1fb723`). Record command, exit, pass counts and the tool sha256 each ran on, in {sb}/baseline.json.",
         "baseline.json with every command, exit, count and sha256; anything that does not run named with its error."),
]

spec = {
    "wave": "kake-r38-w1",
    "milestone": "r38-build",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-38/w1",
    "context": CONTEXT,
    "items": ITEMS,
}
(HERE / "w1-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS), "items")
