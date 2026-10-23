#!/usr/bin/env python3
"""Write the round-37 wave-1 spec (w1-spec.json) next to this file. Usage: make_w1_spec.py REV"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
SB = "/fast/scratch/hyaku/kake-r37w1"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"

CONTEXT = f"""# Goal
Kake round 37, wave 1 (build + first falsifiers). The L1 (KakeR37) holds the planner and integration seat; you are one leaf seat. Lane repo: {L}. Lane axes: operability and freshness (web properties and publishing). Each item names what it builds or attacks; attacks try to show work is wrong, overstated or harmful, with reproducible evidence. Time box: finish and write your report within 30 minutes; a partial report beats none.

# Declared claims (SCORECARD.md section "Round 37 — declared claims", declared at 202d625a323a09d519aaeb9a1be150c228859e26; control receipts appended at {REV}; base 621fb528ba9116b9f440b8332be6dfc0cad4e972). Read them with `git -C {L} show {REV}:SCORECARD.md | sed -n '/^## Round 37 — declared claims/,$p'`.
- C1 (operability, capability): offline robots.txt expectation audit `scripts/robots_audit.py` (not yet written). Public contract: usage, manifest, findings, bullets (a) access result, (b) lines, (c) groups, (d) rules, (e) path and normalization, (f) check faults, (g) manifest faults, verdict. Frozen predicate `met: passed >= 25 of 28 sealed cases`; counter {L}/.ufo/waves/round-37/sealed_count.py (bubblewrap jail, fresh ids and file names per run). Before: 0 of 28.
- C2 (operability): the fixture data of `scripts/source_recheck_selftest.py` kills the 32 round-36 one-change tool mutants. Frozen predicate `met: killed >= 32 of 32 round-36 tool mutants`; public counter {L}/.ufo/waves/round-37/c2_mutkill.py (dumps the selftest's FIXTURES in a jail and runs them itself against E1 = 4d5b3d55:scripts/source_recheck.py, E2 = the round-36 independent implementation, and the mutants in {L}/.ufo/waves/round-37/c2/mutants/; a fixture counts only when E1 and E2 both pass it). Before: 27 of 32 (survivors M07, M08, M09, M11, M24).
- Control receipts (pre-build): {L}/.ufo/waves/round-37/verification/ and {L}/.ufo/waves/round-37/ctl/ (seat reports).
- Sources opened 2026-10-23T02:50:49Z-02:50:51Z by {L}/.ufo/waves/round-37/fetch_sources.py, retained in {L}/.ufo/waves/round-37/sources/ (SXXX.txt visible text, SXXX.html.gz body, receipts.json): S011 RFC 9309 (existing row, re-opened), S095 Google "robots.txt specification" (request URL https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt, final URL https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec), S096 github.com/google/robotstxt, S097 robotstxt.org "A Standard for Robot Exclusion" (1994). Registry {L}/corpus/SOURCES.md (rows S001-S094); contract in /home/vgpnk/Projects/shokunin/CORPUS.md section "SOURCES.md — where a shokunin learns".
- Routed defects this round must address: {L}/corpus/lessons/round-36-verifier-spotcheck.md section "Routed defects" (8 items). Round-36 lesson {L}/corpus/lessons/round-36.md.

# Sealed key — binding
The 28 C1 cases are sealed outside the lane. Never list, read, stat, search or open anything under /fast/scratch/hyaku/kake-r37/ (that exact directory and below; your sandbox is the different directory {SB}/), never look for the cases anywhere, and never run the C1 counter (you have no key). A seat that touches that tree by mistake says so in the first line of its report. The C2 counter is public: any seat may run it in its own sandbox clone.

# Bounds
- You are a leaf: no subagents, no swarm, no second judge, no admission or verdict on the round.
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report — deliverables (code, fixtures, prose drafts, patches) stay in your sandbox and you name their absolute paths and sha256 in the report; the L1 copies after review. Round 36 had two seats write into the lane outside their report; do not.
- Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git (show, log, ls-tree, diff) is fine. Never run any jj command at /home/vgpnk/Projects/shokunin.
- Code that writes files or Git state runs only in your sandbox (clone with `git clone -q {L} {SB}/<YourName>/clone && git -C {SB}/<YourName>/clone checkout -q {REV}` when you need one; export TMPDIR={SB}/<YourName>/tmp after creating it). Unset GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE before any git command. Cap every run with `timeout` (at most 900 s) and at most 8 parallel processes; kill any process tree you started before returning.
- Owned sites: no requests to the operator's web properties (ds4cc.com, app.ds4cc.com, *.onrender.com hosts of the operator, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json) unless your item names it.
- Network: only seats whose item names a public URL to open may fetch, GET only, ordinary means; never pass a bot challenge or access control; a page you cannot open is recorded as unopened.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, record tool, version, channel and reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via uv tool, npx or an official binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart.
- If your seat hits a provider safety or policy refusal or an automatic model switch, stop and write a one-line report saying so; do not rephrase. The only message target is agent://KakeR37 (the L1), for blockers only; never agent://all. Write plain English.

# Result
Report under 80 lines: what you built or attacked, exact commands with exit codes, observed outputs, evidence pointers (path:line, hash). An unrun check has not passed; say what you did not verify. A partial report starts with `PARTIAL:`. Your findings are advisory input for the L1 and the non-author closure.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR = ["operability"], ["freshness"]
BOTH = ["operability", "freshness"]
SRC = {
    "S011": "https://www.rfc-editor.org/rfc/rfc9309.html (sections 2.1, 2.2.1, 2.2.2, 2.2.3, 2.2.4, 2.3.1.3, 2.3.1.4, 2.5)",
    "S095": "https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt (follow its redirect; sections on file format, syntax, grouping, precedence for rules, URL matching, HTTP status codes, file size)",
    "S096": "https://github.com/google/robotstxt (README and robots.cc / robots.h matching code)",
    "S097": "https://www.robotstxt.org/orig.html (the 1994 document: record format, which record applies, Disallow semantics)",
}
CONTRACT = "the round-37 C1 contract (SCORECARD round-37 declaration)"

ITEMS = [
    # ---- C1 build
    item("ExecRobotsTool", "executor", OP,
         "Build C1's tool `scripts/robots_audit.py` to {CONTRACT_} in your clone {sb}/clone at {REV}. You are the only seat writing the landed tool.".replace("{CONTRACT_}", CONTRACT),
         "- Implement exactly the contract (usage, manifest, findings, (a)-(g), verdict), python3 stdlib only, one file. Read-only: it reads the manifest and the robots files it names, nothing else; no network, no writes, no subprocess, no environment reads. Do not use urllib.robotparser (its rules differ).\n- Where the text leaves a point open, choose the reading closest to S011 (retained {L}/.ufo/waves/round-37/sources/S011.txt) and list each choice in your report.\n- Bounded: a 64 MiB manifest or a 500 KiB robots file with 50 000 rules must finish in seconds; a FIFO or device path given as the manifest must not block (check it is a regular file before opening, open non-blocking or stat first).\n- Self-check by hand on at least 12 manifests you write in {sb}/cases/ covering every bullet; paste each command and output. Write the file at {sb}/robots_audit.py and a patch {sb}/robots_audit.patch against {REV}.",
         "Tool runs on your manifests with the exits and findings the contract gives; every open-point choice listed; patch applies to {REV}; sha256 of the file in the report."),
    item("ExecRobotsSelftest", "executor", OP,
         "An independent selftest for C1's tool, written from the public contract only, at {sb}/robots_audit_selftest.py (to land as scripts/robots_audit_selftest.py), plus your own blind implementation {sb}/independent_robots_audit.py. Do not read or wait for the builder's tool.",
         "- Shape like {L}/scripts/source_recheck_selftest.py (read it): `python3 scripts/robots_audit_selftest.py [--tool PATH]`; fixtures as data in a FIXTURES list built by build_fixtures(); judged on exit, verdict and findings projected on (check, reason); prints passedOverTotal; exit 0 only when all pass.\n- At least 60 fixtures, at least 6 per bullet (a)-(g) plus verdict, exit-64 usage, FIFO manifest and oversize manifest fixtures; each names the contract sentence it tests.\n- Implement independent_robots_audit.py from the contract yourself and run the selftest on it until both agree; list every point where you had to choose a reading.\n- Show the selftest can fail: a toy tool using urllib.robotparser ({sb}/toy_robotparser.py) and run the selftest on it; paste the result.",
         "Selftest with >=60 fixtures mapped to contract sentences passes on your independent implementation and fails on the toy with named failures."),
    # ---- C2 build
    item("ExecC2Fixtures", "executor", OP,
         "C2: extend the fixture data of `scripts/source_recheck_selftest.py` so the C2 counter kills all 32 round-36 mutants, in your clone {sb}/clone at {REV}. You are the only seat writing that file for C2.",
         "- Read {L}/.ufo/waves/round-37/c2_mutkill.py and {L}/.ufo/waves/round-36/w2/MutTool.md (mutant table) and diff each survivor (M07, M08, M09, M11, M24 in {L}/.ufo/waves/round-37/c2/mutants/) against `git show 4d5b3d55:scripts/source_recheck.py`.\n- Add fixtures through the existing `add(...)` helper inside build_fixtures(), each named for the contract sentence it tests (e.g. relative redirect chains resolved against the previous hop (b); dot segments in a relative Location (b); a comment containing `>` (c); ordinary tags splitting a quote (c); a UTF-8 BOM body with a quote that begins with U+FEFF (f)). Expectations come from the round-36 contract text, not from running a tool; then check that both E1 and E2 pass each new fixture (the counter reports failedOnE1/failedOnE2). Do not change or delete existing fixtures; do not change the tool.\n- Commit in your clone and run `timeout 900 python3 -B .ufo/waves/round-37/c2_mutkill.py --root {sb}/clone --revision <your commit> --jobs 8`; keep stdout at {sb}/c2-after.json. Also run the selftest itself on the 4d5b3d55 tool (expect all pass). Write a patch {sb}/c2-fixtures.patch against {REV}.",
         "c2-after.json shows killed and survivors; every new fixture valid on E1 and E2; patch touches only scripts/source_recheck_selftest.py."),
    item("ExecRecheckHardening", "executor", ["operability", "freshness"],
         "Carried round-36 tool defects in `scripts/source_recheck.py` (routed defect 8): a FIFO or device manifest blocks forever; a 1 GB or /dev/zero manifest raises MemoryError with no JSON; a `<script` string inside an attribute value opens a script element and truncates the page; `body_path` checks the resolved path then opens the unresolved one. Work in your clone {sb}/clone at {REV}.",
         "- Fix the first two inside the existing contract: a manifest that is not a regular file or is larger than 64 MiB gives `input_invalid` (contract (g) 'unreadable'); stat before open; open the resolved body path.\n- For the attribute case, the round-36 contract (c) literally says raw-element contents run from the start tag; propose the smallest amendment sentence (a raw-element start tag counts only where a tag can start, not inside another tag's attribute value) and implement it. Put the amendment sentence in your report verbatim.\n- Add fixtures for all four to a NEW file {sb}/clone/scripts/source_recheck_hardening_selftest.py (same fixture shape as source_recheck_selftest.py; do not edit source_recheck_selftest.py, another seat owns it). Show each fixture fails on the 4d5b3d55 tool and passes on yours.\n- Regression: run `scripts/source_recheck_selftest.py --tool <yours>` (expect all pass) and the round-36 sealed counter on your tool (`timeout 600 python3 -B .ufo/waves/round-36/sealed_count.py --root {sb}/clone --tool-file <yours> --key-revision fd1fb723624b742a00a6e8e908f3b42901d627f8`, expect 28 of 28). Write {sb}/hardening.patch against {REV}.",
         "Each defect has a fixture red on 4d5b3d55 and green on the fix; round-36 sealed 28/28 and selftest all-pass on the fixed tool; amendment sentence quoted."),
    item("ExecCriteriaRepairs", "executor", OP,
         "Routed defect 7 (round-36 closure): QUALITY round-36 (f) has no polarity red-before receipt; (d) `control_tree_check.py` passes a root listing over a tree holding a sealed key; (a) lacks a bare-id-only negative receipt. Fixed checks go in {sb}/criteria/ (to land under .ufo/waves/round-37/criteria/).",
         "- Read {L}/corpus/QUALITY.md section 'Round-36 criteria', {L}/.ufo/waves/round-36/criteria/*.py and {L}/.ufo/waves/round-36/w2/ReviewCriteriaChecks.md (four constructed false passes).\n- Write `control_tree_check.py` v2 that fails when any listing (root or recursive) shows a path named like a sealed key (`sealed/`, `cases*.json`, the key path in the counter's KEY_PATH) anywhere in the listed tree; show exit 1 on the round-35 key-path listing and on a constructed root listing over a tree holding a key, exit 0 on {L}/.ufo/waves/round-37/ctl/*.md once they exist (or on round-36 ctl reports).\n- Write `polarity_check.py`: given a sealed key JSON, exit 1 when any bullet's cases have no check whose correct outcome is a finding (or none whose correct outcome is a hold); show exit 1 on round-36 key v1 (`git show cd321279:.ufo/waves/round-36/sealed/cases-v1.json` or the path in round-36 verification) and exit 0 on key v2 ({L}/.ufo/waves/round-36/sealed/cases.json).\n- For (a), write `bare_id_check.py` that fails a knowledge entry whose cite of an S-id is a bare id line with no claim text; build the negative receipt on a constructed entry.\n- Paste every command and exit.",
         "Each check shown able to fail (exit 1) and to pass (exit 0) with pasted commands."),
    item("ExecLiveRobotsSnapshot", "executor", BOTH,
         "Real input for C1 after the build: record the served robots.txt of public hosts the lane's corpus names, at {sb}/robots/.",
         "- GET (one request each, User-Agent naming kake-shokunin round 37, 1 request per second, timeout 30 s, no redirects followed beyond 5) the /robots.txt of: www.rfc-editor.org, developers.google.com, github.com, docs.github.com, www.sitemaps.org, developer.mozilla.org, en.wikipedia.org, www.robotstxt.org, html.spec.whatwg.org, pages.github.com. Owned-site exception for this item only: also ds4cc.com and veigapunk.github.io (read-only GET of /robots.txt only).\n- Save each body with a receipts.json (url, final url, status, bytes, sha256, UTC time).\n- For each host write 4 to 8 checks of a C1 manifest at {sb}/robots/manifest.json: a Googlebot or `*` user agent, URLs on that host, and `expect` set to what a publisher would plausibly intend AND justified by a line you quote from that file (e.g. a Disallow line you expect to block). Include status from the receipt. Do not run any robots tool.",
         "manifest.json is contract-shaped (validate the shape by hand) and every expect has a quoted justifying line; receipts complete."),
    # ---- sources (scouts reopen; scribes draft)
] + [
    item(f"ScoutReopen{sid}", "scout", FR,
         f"Independent live re-open of {sid}: {url}.",
         "- GET it yourself (ordinary means) and compare with the retained text {L}/.ufo/waves/round-37/sources/" + sid + ".txt and receipts.json: same page? same final URL? Quote (exact, <=25 words, with section) the passage that grounds the round-37 C1 contract rule it bears on, and any passage that contradicts a contract sentence.\n- Record access time (UTC), status and final URL. Note if the page moved.",
         "Report gives the located quotes with section, access time, final URL, and every contradiction with the contract.")
    for sid, url in SRC.items()
] + [
    item("ScoutContractVsGoogle", "scout", OP,
         "Compare the round-37 C1 contract rules (b)-(e) with Google's robots.txt specification (S095) and Google's open-source parser (S096: github.com/google/robotstxt robots.cc).",
         "- For each contract sentence in (b)-(e), say whether S095 and robots.cc agree, differ or are silent, quoting the line (robots.cc with file:line at the commit you read). Pay attention to: user-agent value matching (prefix, version suffix), grouping across non-group records, 500 KiB limit, BOM, percent-encoding normalization, `$` and `*`, allow-wins ties, /robots.txt implicit allow, 4xx/5xx handling (S095 HTTP status section, 429).\n- Output a table: contract sentence · S011 · S095 · robots.cc · lane reading justified? (yes/no).",
         "Table covers every sentence of (b)-(e) and (a) with quotes and file:line."),
    item("ScoutPriorTools", "scout", OP,
         "Conventions of the lane's existing offline audit tools, for consistency of the new robots tool and its selftest.",
         "- Read {L}/scripts/canonical_audit.py, base_path_audit.py, link_preview_audit.py, source_recheck.py and their selftests: list usage lines, exit codes, report fields, input-fault handling (non-regular file, size caps, symlinks), and how each selftest structures FIXTURES.\n- Name any convention the round-37 C1 contract breaks (e.g. findings field names, `checksEvaluated` naming) and whether that matters.",
         "Table of conventions with file:line; list of contract departures."),
    item("ScoutCorpusRobots", "scout", OP,
         "What the lane already holds on robots.txt: {L}/corpus/knowledge/crawl-scope-per-host.md, SOURCES rows S011-S013, PROVINCE 'Crawl hygiene per host', and any lesson or LOG mention of robots.",
         "- List every robots claim the corpus makes, with path:line, and whether the round-37 contract agrees or contradicts it. Name the frontier gap the new tool fills and what stays open (live fetch, redirects, caching, crawler-specific extensions).",
         "List with path:line; agree/contradict per claim; gap statement."),
    item("ConnectorSiblings", "connector", OP,
         "Sibling-overlap scan for round 37: which other shokunin lanes under /home/vgpnk/Projects/shokunin/*-shokunin own or touch robots.txt, crawler rules, mutation testing of selftests, or sealed-counter tooling.",
         "- grep (read-only) sibling lanes' PROVINCE.md, SKILL.md, corpus/knowledge and scripts for robots/RFC 9309/crawler/mutation/sealed counter; name overlaps and province boundaries (tabi owns client-side crawler discipline; kake owns publisher-side placement), reusable patterns, and any conflict with the new tool.",
         "Overlap table with paths; boundary statement; reusable patterns named."),
    item("ScribeSourcesRows", "scribe", FR,
         "Draft the corpus/SOURCES.md rows for S095, S096, S097 and the S011 re-open note, in the registry's exact column shape, at {sb}/sources-rows.md.",
         "- Read {L}/corpus/SOURCES.md (header and rows S088-S094 for shape) and /home/vgpnk/Projects/shokunin/CORPUS.md section 'SOURCES.md — where a shokunin learns'. Use the retained texts in {L}/.ufo/waves/round-37/sources/.\n- Propose status per row with reason: admit (mined) or reject with reason and the `flip:` form the contract requires. Candidate judgments to test, not to copy: S095 admit (vendor spec, tier A docs), S096 admit (code, tier A), S097 reject (superseded 1994 text: no Allow, first-match semantics; flip: none / if RFC 9309 withdrawn). Note S095 now answers at a new URL (redirect).\n- Draft one Gate line per row in the round-36 lesson shape (URL — accessed time, HTTP status — decision, tier, kind, status: reason; quote “…” (location; N words)), each quote an exact substring of the retained text (paste the grep command that proves it).",
         "Rows in column shape; each quote proven by a pasted grep; decision with reason per row."),
    item("ScribeKnowledgeEntry", "scribe", OP,
         "Draft a knowledge entry `corpus/knowledge/robots-txt-rules.md` at {sb}/robots-txt-rules.md: how a publisher checks, offline, what its robots.txt allows (the round-37 C1 contract's rules as domain knowledge), citing S011 and S095 (and S096 where code settles a reading).",
         "- Read {L}/corpus/knowledge/crawl-scope-per-host.md and link-preview-metadata.md for the lane's entry shape (metadata header source:/verified-at:/recheck:). Every rule sentence cites a row and a section; every lane reading is marked as such; a 'Limits' section (no fetch, no redirects, no crawler-specific extensions, not a statement of what Google does beyond S095). Under 120 lines.",
         "Entry draft with per-sentence cites and limits; no claim without a cite."),
    item("ScribeR36Corrections", "scribe", FR,
         "Draft the round-36 corrections routed by the closure ({L}/corpus/lessons/round-36-verifier-spotcheck.md 'Routed defects' 1, 5, 6) as append-only text for corpus/lessons/round-37.md and SCORECARD, at {sb}/r36-corrections.md.",
         "- (1) `bf9b2089` is not an object in lane history; it exists only in {L}/.ufo/waves/round-36/retained/r36-l1-postfix-remeasure.bundle (verify with `git bundle list-heads`); write the corrected citation.\n- (5) the junk control has no receipt; find every place the lane text says or implies it ran ('No do-nothing, junk, ...'), with path:line, and draft the correction ('untested in round 36; run in round 37: see ctl/CtlC1Junk.md').\n- (6) S091 quote location is section 7 Design Goals not 1.2 (verify in {L}/.ufo/waves/round-36/sources/S091.txt); S093 teaches lacks `flip:`; S094 reason should say 'overbroad' not 'contradicts' for 304; used-by of S088-S092 names a script while contract v1 asks for knowledge-entry or lesson paths. Draft exact replacement cells for SOURCES rows as append-only notes.",
         "Each correction drafted with the verifying command output pasted."),
    item("ScribeMistakeMine", "scribe", OP,
         "Mine one mistake for corpus/lessons/round-37.md `## Mistakes` from round 36 or earlier (spot-check disagreements, wave-2 corrections, holds): class · evidence pointer · captured-by (criterion or rule that should have caught it, or none) · fix, at {sb}/mistakes.md.",
         "- Candidates: the junk control recorded as if it ran; a cited hash that lives only in a bundle; a declaration's coverage sentence measured only on the author's ablations; seats writing into the lane outside their report. Pick the ones without an existing fix, and for each fix name a check that can be shown to fail on the old state (write it as a small script in {sb}/ and run it red on the old state, green on a fixed state).",
         "At least one mistake row with a fix check shown red then green (commands pasted)."),
    item("ScribeQualityCriteria", "scribe", OP,
         "Draft QUALITY.md 'Round-37 criteria' at {sb}/quality-r37.md from the round-36 closure's routed defects 2, 3, 4, 7 and this round's design.",
         "- Read {L}/corpus/QUALITY.md tail (round-35 and round-36 criteria) for shape. Each criterion: rule · lesson that motivates it (path) · the check that enforces it and its red-before receipt (or 'no check yet'). Include: a seat's only deliverable path is its sandbox and the L1 checks `jj-lane.sh state` for stray paths after each wave; a key repair keeps the original-key measurement as the rule of record; a coverage sentence names its listed ablations and a mutation pass; a cited hash must resolve in lane history or name its bundle.",
         "Criteria drafted with motivating lesson paths and enforcement/receipt status per criterion."),
    item("ScribeProvinceStep", "scribe", OP,
         "Draft the PROVINCE.md 'Round-37 robots.txt frontier step' section and the corpus/README.md coverage paragraph, at {sb}/province-r37.md.",
         "- Read {L}/PROVINCE.md (Frontier and round-29..35 frontier steps) and {L}/corpus/README.md 'Coverage — round 35'. State what moves (offline robots expectation audit), what stays open (live fetch and redirects, caching, crawler extensions, sitemaps), province boundary with tabi. Under 25 lines each; no claim beyond the contract.",
         "Two short drafts, each sentence traceable to the contract or a source row."),
    # ---- first falsifiers
    item("CriticC1AxisFit", "critic", OP,
         "Attack C1's declaration: axis named by surface? Target reachable by a cheap control? Universal clauses? Coverage statement honest? Sourcing real?",
         "- Read the declaration and the control receipts at {REV}. Try to design a cheaper tool than the contract that would plausibly reach 25 of 28 given only the public text (you cannot run the counter); argue from the contract's '4 cases per bullet, one check per rule' design. Name any wording that overclaims.",
         "Each objection with the sentence it attacks and a concrete counter-design or fix."),
    item("CriticC2Design", "critic", OP,
         "Attack C2 and its counter {L}/.ufo/waves/round-37/c2_mutkill.py: can a fixture set meet 32 of 32 without being a contract-grounded test? Is 'valid on E1 and E2' a real guard? Is the axis name right ('quality work, never coverage')?",
         "- Run the counter in a sandbox clone at {REV} on a constructed selftest variant of your own if needed. Look for: fixtures that exploit E1/E2 shared defects; fixtures depending on the jail environment; dump-time code execution tricks; tolerant 'accept' alternatives that make a fixture pass E1/E2 but fail a mutant spuriously (e.g. timing, file writes).",
         "Each attack with a reproducer command and observed counter output, or a reasoned no-attack."),
    item("ReviewSealedCounter", "reviewer", OP,
         "Review {L}/.ufo/waves/round-37/sealed_count.py (adapted from round-36 counter v3) for correctness and leaks, without the key.",
         "- Diff it against {L}/.ufo/waves/round-36/sealed_count.py; check: materialize (fresh ids, setdefault for repeated ids, robots path rewrite keeps directories), runs-per-case loop (a case passes only if all runs pass; a missing tool scores 0), judge projection (check, reason), jail binds, per-run directory removal, crash paths (unhashable check, non-list findings, huge stdout). Build a dummy key of your own (change KEY_SHA256 in a sandbox copy) with 2-3 cases to exercise it.",
         "Findings with line numbers and reproducer commands; severity per finding."),
    item("ReviewC2Counter", "reviewer", OP,
         "Review {L}/.ufo/waves/round-37/c2_mutkill.py: does its judge equal the round-36 selftest's run_case (`git show 1a16b8e3:scripts/source_recheck_selftest.py`)? Are E1/E2 and mutants pinned? Is the base 27 of 32 reproducible?",
         "- Line-by-line comparison of judge vs run_case (accept alternatives, shape, exit 64, version, REASONS, checksEvaluated, write snapshot). Re-run the base in a sandbox clone at {REV}: `timeout 900 python3 -B .ufo/waves/round-37/c2_mutkill.py --root <clone> --revision 621fb528 --jobs 8` and compare with {L}/.ufo/waves/round-37/verification/c2-at-621fb528.json. Compare survivors with MutTool's selftest survivors.",
         "Equivalence verdict per judge clause; base re-run result and diff."),
    item("SentinelCounterJail", "sentinel", OP,
         "Adversarial review of the round-37 counters' jails: could a tool run by sealed_count.py, or selftest code imported by c2_mutkill.py, read the sealed key, the lane, other tools, or influence other runs' results?",
         "- Read both counters' jail() and materialize paths; in a sandbox, run a probe tool under a copy of the jail command (same bwrap argv) that lists what it can see (/, /proc, scratch siblings, earlier case directories, env). Report each exposure with the exact probe and output. No attack on the real key.",
         "Exposure list with probe commands and outputs."),
    item("CriticContractAmbiguity", "critic", OP,
         "List every point the round-37 C1 contract text leaves undecided or decides two ways (round 36 had 18).",
         "- Read the contract sentence by sentence. For each undecided point, give a concrete manifest + robots file where two careful readers would produce different reports. Classify: matters for a reasonable test / edge only.",
         "Numbered list with concrete inputs and the two readings."),
    item("CriticDeclarationWording", "critic", ["operability", "freshness"],
         "Claim-sizing attack on the round-37 declaration (prompt rules: one concrete after-value re-derivable by one command; no universal clauses unless the counter enumerates the set; a do-nothing control cannot reach the target; predicate same sentence in plan, code, receipt).",
         "- Check each rule against the declaration text, both counters' PREDICATE strings and the receipts at {REV} (predicate fields). Flag any sentence a closure would reject.",
         "Per rule: holds / breaks with quoted sentence."),
    item("MutC2Counter", "mutation-tester", OP,
         "Mutation-test the C2 counter {L}/.ufo/waves/round-37/c2_mutkill.py in a sandbox clone at {REV}: does each guard matter?",
         "- Make at least 10 single-point mutants of the counter (e.g. drop the E2 validity requirement, drop the write check, accept any exit, ignore checksEvaluated, skip mutant hash checks, count a fixture valid on E1 only). For each, show an input (a selftest variant committed in your clone, or the base) where the mutant counter gives a different count than the real one, or argue it is equivalent.",
         "Table: counter mutant · input · real vs mutant output · guard proven or equivalent."),
    item("MutSelftestTolerance", "mutation-tester", OP,
         "Which existing round-36 selftest fixtures are tolerant (accept alternatives) and could mask a mutant? Work in a sandbox clone at {REV}.",
         "- From `scripts/source_recheck_selftest.py`, list the fixtures with `accept` alternatives or shape=False. For each of the 32 mutants in {L}/.ufo/waves/round-37/c2/mutants/, run the C2 counter's per-mutant killers (counter output perMutant) at 621fb528 and say which killers are tolerant fixtures. Name any mutant killed only by a tolerant fixture.",
         "Per-mutant killer list with tolerant flags; any mutant killed only through tolerance named."),
    item("RevengerSurvivors", "revenger", OP,
         "Reverse-engineer why round-36 mutants M07, M08, M09, M11 and M24 survived the round-36 selftest and which contract sentence each one breaks.",
         "- Diff each mutant ({L}/.ufo/waves/round-37/c2/mutants/Mxx.py) against `git -C {L} show 4d5b3d55:scripts/source_recheck.py`; for each, state the smallest manifest + body on which E1 and the mutant differ, and check by running both (python3 -B <tool> --manifest ...) in your sandbox. Also run E2 (`git show 1a16b8e3:.ufo/waves/round-36/retained/independent/selftest-seat-reference.py`) on it: does E2 agree with E1? If not, that fixture cannot count for C2; say so.",
         "Per mutant: distinguishing input, E1/mutant/E2 outputs, contract sentence."),
    item("ReviewRoutedDisposition", "reviewer", OP,
         "Check the round's plan covers all 8 routed defects in {L}/corpus/lessons/round-36-verifier-spotcheck.md 'Routed defects' and the session note's routes (junk untested, bf9b2089 in bundle, 9 of 32 sealed survivors need fixture classes, gate-line fixes, criteria-check gaps, carried tool defects, containment).",
         "- For each routed item, map it to this wave's items (names in the context's spec are visible in your own prompt context only; use the declaration and the routed list) and state: addressed by a claim / by a non-claim repair / not addressed and why that is acceptable. Note: the 9 sealed survivors (M07, M08, M13, M20, M24, M26, M28, M31, M32) differ from the 5 selftest survivors; check whether C2 (counter over selftest fixtures) covers 'fixture classes that kill them' for all 9.",
         "Table per routed item with disposition and gaps."),
    item("SimplifierCounters", "simplifier", OP,
         "YAGNI review of the round-37 counters and spec tooling ({L}/.ufo/waves/round-37/sealed_count.py, c2_mutkill.py, make_w1_spec.py): what can be deleted without changing any measured value?",
         "- Propose deletions only where you can show (by reasoning over the code, or by running the C2 counter at 621fb528 in a sandbox clone before and after your deletion) that outputs are byte-identical. Do not propose changes to frozen predicates, pins or judges — those are frozen; list them as out of scope.",
         "Deletion proposals with identical-output evidence; frozen parts listed."),
]

spec = {
    "wave": "kake-r37-w1",
    "milestone": "r37-build",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-37/w1",
    "context": CONTEXT,
    "items": ITEMS,
}
(HERE / "w1-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS), "items")
