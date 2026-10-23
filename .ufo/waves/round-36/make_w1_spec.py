#!/usr/bin/env python3
"""Write the round-36 wave-1 spec (w1-spec.json) next to this file."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = "cd3212796cab7a2afa03b638dbfafe7194df9629"
SB = "/fast/scratch/hyaku/kake-r36w1"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"

CONTEXT = f"""# Goal
Kake round 36, wave 1 (build + first falsifiers). The L1 (KakeR36) holds the planner and integration seat; you are one leaf seat. Lane repo: {L}. Lane axes: operability and freshness (web properties and publishing). Rounds 34 and 35 were rejected because a cheap control met a knowledge-entry counter. This round makes no knowledge-entry claim: it builds a new tool that re-checks a source registry row's quote against a recorded fetch of its source, measured on sealed cases no control can reach. Each item names what it builds or attacks; attacks try to show work is wrong, overstated or harmful, with reproducible evidence. Time box: finish and write your report within 25 minutes; a partial report beats none.

# Declared claim (SCORECARD.md section "Round 36 — declared claims", declared at 3555f63fbf58f19445823eb88bc3161b7b1faad4; counter version 3 (key version 2) and pre-build receipts at {REV}; base b720d799ae99c19a7c97f2b1391d4fe928be0e11)
- C1 (freshness, capability): offline source re-check audit `scripts/source_recheck.py` (not yet written). Public contract: SCORECARD "C1 contract" bullets (a) final status, (b) redirects, (c) HTML text, (d) quote match, (e) media types, (f) decoding, (g) input faults, plus the verdict rule. Read it with `git -C {L} show {REV}:SCORECARD.md | tail -130`.
- Frozen predicate: `met: passed >= 25 of 28 sealed cases`. Counter `{L}/.ufo/waves/round-36/sealed_count.py` (version 3; v1 and v2 kept beside it): runs the tool in a bubblewrap jail once per case, fresh random check ids and body file names per run, judges exit code, verdict and the findings multiset projected on (check, reason, target). Before: 0 of 28 at base.
- Pre-build receipts at {REV}: `{L}/.ufo/waves/round-36/verification/control-base.json`, `control-declaration.json` (0 of 28), `verification/ablations/*.json` (the L1's private reference 28 of 28; 36 ablations 13 to 24 of 28, none met; control seats: constant clean 0, all-false 0, no-reader 8, naive reader 12, shortcut 9).
- Sources opened 2026-10-23T01:08:56Z-01:09:01Z by `{L}/.ufo/waves/round-36/fetch_sources.py`, retained in `{L}/.ufo/waves/round-36/sources/` (SXXX.txt visible text, SXXX.html.gz body, receipts.json): S088 RFC 9110 (status codes, redirects, Location), S089 RFC 3986 (reference resolution), S090 WHATWG Encoding, S091 UAX #15 Unicode normalization, S092 WHATWG HTML syntax (element kinds), S093 Wikipedia "HTTP 301" (reject candidate: tertiary), S094 MDN "Redirections in HTTP". No row is written yet; the registry is `{L}/corpus/SOURCES.md` (rows S001-S087; contract in /home/vgpnk/Projects/shokunin/CORPUS.md section "SOURCES.md — where a shokunin learns"). Existing rows the contract also cites: S025 (template contents), S033 (media types).
- Previous closures with routed defects: `{L}/corpus/lessons/round-35-verifier-spotcheck.md` (section "Routed defects", 5 items) and `{L}/corpus/lessons/round-34-verifier-spotcheck.md`. Round-35 lesson: `{L}/corpus/lessons/round-35.md`.

# Sealed key — binding
The 28 cases are sealed outside the lane. Never list, read, stat, search or open anything under /fast/scratch/hyaku/kake-r36/ (any path), never look for the cases anywhere, and never run the counter (you have no key). A seat that touches that tree by mistake says so in the first line of its report. Work from the public contract, the public counter code and the pass counts in the receipts.

# Bounds
- You are a leaf: no subagents, no swarm, no second judge, no admission or verdict on the round.
- Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any tracked lane file. Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git (show, log, ls-tree) is fine. Never run any jj command at /home/vgpnk/Projects/shokunin.
- Code that writes files or Git state runs only in your own sandbox {SB}/<YourName>/ (clone with `git clone -q {L} {SB}/<YourName>/clone && git -C {SB}/<YourName>/clone checkout -q {REV}` when you need one; export TMPDIR={SB}/<YourName>/tmp after creating it). Unset GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE before any git command. Cap every run with `timeout` (at most 300 s) and at most 4 parallel processes; kill any process tree you started before returning. Deliverable files stay in your sandbox; name their absolute paths in your report.
- Owned sites: no requests to the operator's web properties (ds4cc.com, app.ds4cc.com, *.onrender.com hosts of the operator, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json).
- Network: only seats whose item names a public URL to open may fetch, GET only, ordinary means; never pass a bot challenge or access control; a page you cannot open is recorded as unopened.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Your report is the only file you write in the lane.
- Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, record tool, version, channel and reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via uv tool, npx or an official binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart.
- If your seat hits a provider safety or policy refusal or an automatic model switch, stop and write a one-line report saying so; do not rephrase. The only message target is agent://KakeR36 (the L1), for blockers only; never agent://all. Write plain English.

# Result
Report under 80 lines: what you built or attacked, exact commands with exit codes, observed outputs, evidence pointers (path:line, hash). An unrun check has not passed; say what you did not verify. A partial report starts with `PARTIAL:`. Your findings are advisory input for the L1 and the non-author closure.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


FR, OP = ["freshness"], ["operability"]
BOTH = ["freshness", "operability"]
SRC = {"S088": "https://www.rfc-editor.org/rfc/rfc9110.html (sections 15.4, 15.4.2, 15.4.3, 15.4.4, 15.4.8, 15.4.9, 15.5.5, 15.5.11, 10.2.2)",
       "S089": "https://www.rfc-editor.org/rfc/rfc3986.html (sections 5.2, 5.2.2, 5.2.4, 5.4.1, 5.4.2)",
       "S090": "https://encoding.spec.whatwg.org/ (sections 4.2 names and labels, 6 decode / BOM sniff, windows-1252 labels)",
       "S091": "https://www.unicode.org/reports/tr15/ (section 1.1 canonical and compatibility equivalence, NFKC)",
       "S092": "https://html.spec.whatwg.org/multipage/syntax.html (13.1.2 elements: raw text elements; 13.1.4 character references; 13.1.6 comments)",
       "S093": "https://en.wikipedia.org/wiki/HTTP_301",
       "S094": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Redirections"}

ITEMS = [
    # ---- C1 build
    item("ExecToolBuild", "executor", BOTH,
         "Build C1's tool `scripts/source_recheck.py` to the round-36 public contract in your clone {sb}/clone at {REV}. You are the only seat writing the landed tool.",
         "- Read SCORECARD.md section \"Round 36 — declared claims\" (C1 contract: usage, manifest, bullets a-g, verdict, pass rule) and implement exactly that, python3 stdlib only, one file. Read-only: it reads the manifest and the body files it names, nothing else; no network, no writes, no subprocess, no environment reads.\n- Where the contract text leaves a point open, choose the reading closest to the cited source (S088-S092, S025, S033; retained texts under {L}/.ufo/waves/round-36/sources/) and list each such choice in your report.\n- Keep inputs bounded (no quadratic scans on hostile bodies; a 5 MB body must finish in seconds).\n- Self-check by hand on at least 10 manifests you write in {sb}/cases/ covering every bullet; paste each command and output.\n- Deliver {sb}/source_recheck.py and {sb}/patch.diff (git diff against {REV} adding only scripts/source_recheck.py).",
         "Tool runs on your manifests with the exits and findings the contract gives; each open-point choice listed with its source; patch applies to {REV}."),
    item("ExecSelftest", "executor", BOTH,
         "An independent selftest for C1's tool, written from the public contract only, in {sb}/source_recheck_selftest.py (to land as scripts/source_recheck_selftest.py). Do not read or wait for the builder's tool.",
         "- Shape: like {L}/scripts/link_preview_selftest.py (read it): `python3 scripts/source_recheck_selftest.py [--tool PATH]` runs the tool on fixtures written to a temp dir, prints passedOverTotal and a verdict, exit 0 only when all pass.\n- At least 40 fixtures, at least 4 per contract bullet (a)-(g) plus verdict, exit-64 usage and output-shape fixtures; each fixture names the contract sentence it tests.\n- To show the selftest can fail, write a deliberately wrong toy tool {sb}/toy_wrong.py (for example raw substring, no redirect rules) and run the selftest on it; paste the result.",
         "Selftest file exists with >=40 fixtures mapped to contract sentences; on the toy it exits non-zero with named failures."),
    item("ExecSnapshotFetcher", "executor", ["freshness"],
         "A recorder that turns a list of (id, url, quote) into a C1 manifest from live fetches, in {sb}/source_snapshot.py (to land as scripts/source_snapshot.py).",
         "- Input JSON list of {{id, url, quote}}; for each: GET without following redirects (urllib with a no-redirect handler), record each hop's status and Location, follow at most 8 hops by resolving Location against the hop URL, stop at the first non-redirect; save the final body (cap 8 MiB) under an output dir; write a version-1 manifest exactly as the contract describes (hops, contentType from the final response, body path). One User-Agent naming kake-shokunin round 36; 1 request per second; timeouts 30 s.\n- Test offline with a local `python3 -m http.server`-style server you write in {sb}/ that serves a 301, a 302 chain, a 404 and a 200 page on 127.0.0.1; paste the manifest it writes. Never fetch a real host in this item.",
         "Recorder writes a contract-shaped manifest from the local server; hop recording and Location resolution shown on the 301 and the 302 chain."),
    item("ExecGateQuoteExtractor", "executor", ["freshness"],
         "An extractor of (id, url, quote) triples from the lane's lesson Gate lines, the real-input set for C1, in {sb}/gate_quotes.py.",
         "- Parse every `{L}/corpus/lessons/round-*.md` line shaped like `- S0NN — <url> — accessed <time>, HTTP <code> — ... quote “...” (...)` (see round-34.md and round-35.md Gate sections; also older shapes you find). Emit JSON list of {{id, url, quote, lesson, line}}. Report counts: lines matched, distinct ids, SOURCES.md rows (`{L}/corpus/SOURCES.md`) with no extracted quote, and ids whose URL in the Gate line differs from the URL in the SOURCES row.\n- Paste the command and counts; save the JSON at {sb}/gate_quotes.json.",
         "gate_quotes.json exists; counts and mismatches reproduce with one pasted command."),
    # ---- routed-defect criteria (round-35 closure)
    item("ExecCriterionAblation", "executor", OP,
         "Round-35 closure routed defect 3 (target slack: a bullet could be skipped and the target still met). A criterion check `{sb}/ablation_floor_check.py` to land under .ufo/waves/round-36/criteria/.",
         "- Input: a predicate target T and a list of ablation receipts (JSON with `passed`, `met`, and a name like `ablation-<bullet>_<rule>.json`). Exit 1 if any ablation has met true or passed >= T, or if any bullet letter has no ablation receipt; exit 0 otherwise; print one line per failure.\n- Show it able to fail: build round-35 style receipts from {L}/.ufo/waves/round-35/w2/ExecPartialRepairs.md (isolated repairs moved (a) +3, (b) +5, (c) +2 from base 14; target 22), for example the receipt `skip (c)` = 22 of 24, and run the check (exit 1). Then run it on {L}/.ufo/waves/round-36/verification/ablations/ with T=25 (expected exit 0). Paste both.",
         "Check written; exit 1 on the round-35 shape, exit 0 on the round-36 receipts, both pasted."),
    item("ExecCriterionControlTree", "executor", OP,
         "Round-35 closure routed defect 4 (control key-blindness: a post-reveal control clone held the key). A criterion check `{sb}/control_tree_check.py` to land under .ufo/waves/round-36/criteria/.",
         "- Input: a control report (markdown) that must contain a tree listing (`ls -la` or `git ls-tree` output) of the tree the control was built from, and a list of key path patterns. Exit 1 if the report has no listing, or the listing shows a key path; exit 0 otherwise.\n- Show it able to fail on the round-35 case: the control commit 0b7779dc's clone held `.ufo/waves/round-35/sealed/c2-probes.json` (see {L}/corpus/lessons/round-35-verifier-spotcheck.md defect iii and {L}/.ufo/waves/round-35/w2/CriticC2Sufficiency.md; the bundle {L}/.ufo/waves/round-35/retained/r35-w2-c2-sufficiency.bundle can be fetched into a sandbox clone and `git ls-tree -r` run on its parent tree). Then run it on the round-36 control reports at {L}/.ufo/waves/round-36/ctl/*.md with pattern `/fast/scratch/hyaku/kake-r36/.k` and `.ufo/waves/round-36/sealed/` (do not open anything under /fast/scratch/hyaku/kake-r36/). Paste both.",
         "Check written; exit 1 on the round-35 case, results on the round-36 control reports pasted."),
    item("ExecCriterionVersionBump", "executor", OP,
         "Round-35 closure routed defect 2 (a counter version bump loosened a condition no control forced). A criterion check `{sb}/version_bump_check.py` to land under .ufo/waves/round-36/criteria/.",
         "- Input: two counter files (old, new). Compare every module-level UPPER_CASE constant and every string constant naming a predicate; exit 1 when any target, threshold, cap, pin or predicate differs, printing each difference; exit 0 when only code outside those constants changed.\n- Show it able to fail on round 35: {L}/.ufo/waves/round-35/sealed_count_v1.py vs {L}/.ufo/waves/round-35/sealed_count.py (the size cap moved). Then run it on {L}/.ufo/waves/round-36/sealed_count_v1.py vs {L}/.ufo/waves/round-36/sealed_count.py. Paste both.",
         "Check written; exit 1 on round 35 naming the cap, round-36 result pasted."),
    # ---- probes on the contract's sources (falsifiable hypotheses)
    item("ExecProbeCp1252", "executor", FR,
         "Hypothesis to test: the contract's (f) sentence \"bytes invalid in the chosen encoding decode to U+FFFD\" agrees with the WHATWG windows-1252 index for every byte 0x00-0xFF.",
         "- Read S090 (retained {L}/.ufo/waves/round-36/sources/S090.txt; the index file https://encoding.spec.whatwg.org/index-windows-1252.txt may be fetched by GET). Compare with Python `bytes([b]).decode('cp1252', 'replace')` for all 256 bytes. List each byte where they differ and what each gives.\n- State whether a tool built on Python cp1252 diverges from WHATWG, and which sentence of the contract (f) a closure should read as decisive.",
         "Table of differing bytes with both decodings; verdict holds or refuted with the byte list."),
    item("ExecProbeUrljoin", "executor", FR,
         "Hypothesis to test: Python `urllib.parse.urljoin` gives the RFC 3986 section 5.4 results for every normal and abnormal example.",
         "- Take the examples from S089 (retained {L}/.ufo/waves/round-36/sources/S089.txt, sections 5.4.1 and 5.4.2, base http://a/b/c/d;p?q). Run urljoin on each; list each mismatch. Also test resolution from an https base with `//host/path`, `?q` only, `../` beyond the root, and an empty reference.\n- Write a 30-line stdlib RFC 3986 section 5.2.2 resolver in {sb}/rfc3986_resolve.py and show it passes all examples.",
         "Mismatch list for urljoin (or none) with pasted output; the resolver passes every example."),
    item("ExecProbeUnescape", "executor", FR,
         "Hypothesis to test: Python `html.unescape` decodes character references as the HTML parser does (contract bullet (c) says it conforms).",
         "- Using S092 (retained {L}/.ufo/waves/round-36/sources/S092.txt, 13.1.4) and the WHATWG named character reference rules (https://html.spec.whatwg.org/multipage/named-characters.html may be fetched by GET), test: named references with and without semicolon (`&amp`, `&notit;`, `&copy`), numeric references to 0x80-0x9F (`&#150;`), to surrogates, to 0 and beyond 0x10FFFF, and hex case (`&#X41;`). Compare html.unescape with what the HTML tokenizer specifies, and with `html.parser.HTMLParser(convert_charrefs=True)` text.\n- Record where they differ and whether any difference matters in text content (outside attributes).",
         "Table of test inputs with unescape vs specified result; verdict on the contract's 'conforms' sentence."),
    item("ExecProbeQuoteMatch", "executor", FR,
         "Hypothesis to test: on real retained sources, the contract's quote rule (c)+(d) finds each Gate quote in its own source and gives no hold for a quote in an unrelated source (false holds).",
         "- Take Gate quotes from {L}/corpus/lessons/round-34.md and round-35.md (`quote “...”` in the Gate lines) and the retained bodies {L}/.ufo/waves/round-34/sources/*.html.gz and {L}/.ufo/waves/round-35/sources/*.html.gz (bodies, gunzip in your sandbox). Implement only rules (c) and (d) in {sb}/match.py (stdlib). For each quote: does it hold in its own body? For each pair (quote, other body): does it hold? Report the own-source hold rate, every own-source miss with the reason (typography, truncation, extraction rule), and every cross-source false hold.\n- Compare with the older Gate check rule in {L}/.ufo/waves/round-35/fetch_sources.py visible_text (whitespace collapsed, not deleted).",
         "Own-source holds and misses listed with reasons; cross-source false holds counted; commands pasted."),
    # ---- scribes
    item("ScribeSourcesRows", "scribe", FR,
         "Draft `corpus/SOURCES.md` rows S088-S094 in {sb}/rows.md.",
         "- Row shape: the 11 cells of rows S078-S087 in {L}/corpus/SOURCES.md (id | source with URL | kind | tier | scope | anchor with fetch time, HTTP status and retained text sha256 prefix from {L}/.ufo/waves/round-36/sources/receipts.json | teaches | status | opened | recheck | used-by). Admits: status mined, opened 2026-10-23, recheck 90d, used-by `scripts/source_recheck.py`. S093 (Wikipedia HTTP 301) is a reject candidate (tertiary restatement); S094 (MDN) may be admitted as tier B or rejected — decide from its text and say why. Scopes must be distinct from existing rows with the same URL (S010, S028, S033 for RFC 9110; S029 for RFC 3986; S030, S031 for syntax.html).\n- Read each retained text; every teaches cell states only what the text says.",
         "rows.md has 7 rows of 11 cells, no unescaped pipe in a cell; each anchor names a section and the sha256 prefix; each reject has a located reason."),
    item("ScribeGateLines", "scribe", FR,
         "Draft the round-36 lesson `## Gate` source-opening lines in {sb}/gate.md.",
         "- One line per source S088-S094 in the shape of {L}/corpus/lessons/round-35.md lines 44-53: URL, accessed UTC time and HTTP status from receipts.json, decision, tier, kind, status, a reason of at least four words, and a quote of at most 25 words with its location.\n- Every quote must be an exact substring of the retained text {L}/.ufo/waves/round-36/sources/SXXX.txt (whitespace-normalised); paste the verifying command per quote. Choose quotes that carry the rule the contract cites (for example S088: the 301 and 308 'new permanent URI' sentences, the 302 'resides temporarily' sentence, 404, 410, Location relative reference; S090: BOM sniff and the windows-1252 labels; S091: compatibility equivalence; S092: raw text elements).",
         "gate.md with 7 lines; each quote verified by a pasted command; at least one located reject."),
    item("ScribeMistakeMine", "scribe", ["freshness", "operability"],
         "Mine mistakes for `corpus/lessons/round-36.md` `## Mistakes`, in {sb}/mistakes.md.",
         "- Sweep {L}/corpus/lessons/round-35-verifier-spotcheck.md, round-35.md, round-34-verifier-spotcheck.md and round-34.md for mistakes not yet mined (compare with the Mistakes tables in round-34.md and round-35.md). Candidates: the all-false entry meeting C2 (already row 5 of round 35?), the v2 size-cap loosening (routed defect 2), the S084 'whole served body' wording (defect 5), the 'absent → English' cite (defect 5), the C1 target slack (defect 3), control key-blindness (defect 4).\n- Each row: class · evidence pointer (path:line or hash) · captured-by (criterion or rule that should have caught it, or none) · fix (and how the fix is shown able to fail). Paste the sweep commands.",
         "mistakes.md with rows not already in earlier Mistakes tables, each with a resolvable pointer; sweep commands pasted."),
    item("ScribeCorrectionsR35", "scribe", FR,
         "Round-35 closure routed defect 5: draft two appended corrections in {sb}/corrections.md.",
         "- (1) The round-35 Gate line for S084 says 'whole served body' but the quote is 4 of 7 lines ({L}/corpus/lessons/round-35.md:50; retained {L}/.ufo/waves/round-35/sources/S084.txt). (2) The entry {L}/corpus/knowledge/security-txt-publishing.md cites S079 for the 'absent → English' (Preferred-Languages absent) clause, but S078 RFC 9116 section 2.5.8 carries it; find the exact sentence (grep the entry) and the RFC sentence in {L}/.ufo/waves/round-35/sources/S078.txt.\n- Draft each as an append-only note in the style of the round-35 'Correction of round-34 mistake row 4' section, quoting the exact lines with pasted grep commands. Never rewrite the original lines.",
         "corrections.md with two notes, each quoting the original and the source with pasted commands."),
    item("ScribeQualityCriteria", "scribe", OP,
         "Draft `corpus/QUALITY.md` section `## Round-36 criteria` in {sb}/quality.md.",
         "- Read {L}/corpus/QUALITY.md sections Round-34 and Round-35 criteria for shape. Draft criteria (a)-(d), one per round-35 routed defect 1-4 ({L}/corpus/lessons/round-35-verifier-spotcheck.md 'Routed defects'): (1) a sourced-learning counter must fail an inverted-facts control and an unsourced control, and a bare id line must not satisfy a cites condition; (2) a counter version bump changes no target, threshold, cap, pin or predicate unless a scored control forced it, named in the note; (3) every contract bullet's ablation scores below target; (4) every control is built from a tree whose listing shows no key path. Each names its check script path under .ufo/waves/round-36/criteria/ (ablation_floor_check.py, version_bump_check.py, control_tree_check.py; for (1) the existing .ufo/waves/round-35/criteria/knowledge_control_check.py) and how it is shown able to fail.",
         "quality.md with four criteria in the existing shape, each naming its check and failing case."),
    item("ScribeSkillRegistry", "scribe", OP,
         "Draft the SKILL.md gate registry row and a short procedure for the source re-check audit, in {sb}/registry.md.",
         "- Read the precedent tables in {L}/SKILL.md (\"Link-preview audit gate registry — round 35\" near line 1035, \"Base-path audit gate registry — round 29\" near line 721) and PROTOCOL.md section \"Gate standard\" (/home/vgpnk/Projects/shokunin/PROTOCOL.md). Draft `### Source re-check audit gate registry — round 36` with the same columns: name source-recheck-audit, kind gate|probe, entry command `python3 scripts/source_recheck.py --manifest PATH`, verdict map 0=clean 1=failed-policy 2=could-not-evaluate 64=usage, self-test `python3 scripts/source_recheck_selftest.py`, frozen proof (the round-36 counter and its predicate), write scope none, owner kake. Add a 6-line procedure: build a manifest with scripts/source_snapshot.py from Gate quotes, run the audit, what each reason means for a SOURCES row (moved → update URL, gone → status flip, quote_missing → re-open and re-quote).",
         "registry.md with one row in the precedent column set and the procedure; every command named exists or is marked round-36 pending."),
    # ---- scouts / connector
    item("ScoutRecheckDue", "scout", FR,
         "Which `corpus/SOURCES.md` rows are due for recheck on 2026-10-23, the target set for C1's first real run.",
         "- Parse the Registry table of {L}/corpus/SOURCES.md at {REV} (git show): for each row id, status, opened, recheck (for example 90d, 30d, 7d, a date), first URL. Compute due = opened + recheck <= 2026-10-23. Report counts by status and the due list with URLs. Flag rows whose recheck cell is unparseable.\n- Paste the one command that reproduces the counts.",
         "Due list and counts reproduce from one pasted command."),
    item("ScoutPriorArt", "scout", FR,
         "Prior art in the lane and the fleet for re-checking sources, so C1 reuses rather than duplicates.",
         "- Read {L}/scripts/freshness-sweep.mjs (head and section list), {L}/scripts/receipt_replay.py, {L}/scripts/live_snapshot.py, {L}/.ufo/waves/round-35/fetch_sources.py and /home/vgpnk/Projects/shokunin/scripts/sources-census.sh (read-only). For each: does it fetch, does it check quotes, what it records. Name any overlap with C1's contract and any convention C1 should follow (JSON shape, exit codes, finding ids).",
         "Table of five tools with fetch/quote/record columns and named overlaps, each with a path:line."),
    item("ConnectorSiblingOverlap", "connector", FR,
         "Sibling-lane overlap scan: other shokunin lanes that re-check sources or quotes.",
         "- Under /home/vgpnk/Projects/shokunin/*-shokunin/ (read-only; skip kake-shokunin), grep scripts/ and corpus/ for source re-check tooling: words like recheck, re-open, quote, stale, link rot, 301, 410. List lanes with such tools or lessons (path:line), and whether C1's contract conflicts with or could serve them. Also read /home/vgpnk/Projects/shokunin/CORPUS.md section on SOURCES.md for what 'recheck' means fleet-wide.",
         "List of sibling hits with path:line and a one-line overlap judgement each; CORPUS recheck wording quoted."),
    item("ScoutReopenS088", "scout", FR,
         "Re-open source S088 live, independently of the L1's fetch.",
         "- GET " + SRC["S088"] + "; save the body in {sb}/. Locate verbatim the sentences the contract cites (301 and 308 'assigned a new permanent URI', 302/303/307 temporary, 404, 410 'likely to be permanent', Location relative reference resolved against the target URI). Compare with the retained {L}/.ufo/waves/round-36/sources/S088.txt (sha256 in receipts.json) and say if anything changed.",
         "Each cited sentence quoted with its section number from your own fetch; retained-vs-live comparison pasted."),
    item("ScoutReopenS089", "scout", FR,
         "Re-open source S089 live, independently of the L1's fetch.",
         "- GET " + SRC["S089"] + "; save the body in {sb}/. Locate verbatim section 5.2.2 (Transform References) and the 5.4.1 examples, and the remove_dot_segments description (5.2.4). Compare with the retained {L}/.ufo/waves/round-36/sources/S089.txt and say if anything changed.",
         "Sentences quoted with section numbers from your own fetch; comparison pasted."),
    item("ScoutReopenS090", "scout", FR,
         "Re-open source S090 live, independently of the L1's fetch.",
         "- GET " + SRC["S090"] + "; save the body in {sb}/. Locate verbatim: the BOM sniff table (EF BB BF, FE FF, FF FE), the decode algorithm's BOM handling, 'get an encoding' label matching (trim ASCII whitespace, ASCII case-insensitive), and the windows-1252 label list (does it include iso-8859-1, latin1, ascii, us-ascii?). Compare with the retained {L}/.ufo/waves/round-36/sources/S090.txt.",
         "Each item quoted from your own fetch; label list pasted; comparison pasted."),
    item("ScoutReopenS091", "scout", FR,
         "Re-open source S091 live, independently of the L1's fetch.",
         "- GET " + SRC["S091"] + "; save the body in {sb}/. Locate verbatim the definition of NFKC and of compatibility equivalence, with examples (ligatures, fullwidth forms, circled digits, Roman numerals if present). Note the UAX #15 revision and Unicode version. Compare with the retained {L}/.ufo/waves/round-36/sources/S091.txt.",
         "Definitions quoted with section numbers; revision named; comparison pasted."),
    item("ScoutReopenS092", "scout", FR,
         "Re-open source S092 live, independently of the L1's fetch.",
         "- GET " + SRC["S092"] + "; save the body in {sb}/. Locate verbatim: the kinds of elements (raw text elements script, style; escapable raw text title, textarea), the comment syntax, and character references (13.1.4). Also open https://html.spec.whatwg.org/multipage/scripting.html#the-template-element (existing row S025) and quote the template-contents sentence. Compare with the retained {L}/.ufo/waves/round-36/sources/S092.txt.",
         "Sentences quoted with section numbers; S025 sentence quoted; comparison pasted."),
    item("ScoutReopenS093", "scout", FR,
         "Re-open reject candidate S093 live and judge it.",
         "- GET " + SRC["S093"] + " (and `?action=raw`); save in {sb}/. What does it say about 301 that RFC 9110 does not, and is any of it wrong or SEO lore without a primary source? Quote the lines. Recommend reject or admit with a located reason.",
         "Recommendation with located quotes from your own fetch."),
    item("ScoutReopenS094", "scout", FR,
         "Re-open candidate S094 live and judge it.",
         "- GET " + SRC["S094"] + "; save in {sb}/. Quote what it says about permanent vs temporary redirects and what crawlers and feed readers do with each. Does it add anything to RFC 9110 (S088) that a registry re-check needs, or restate it? Any statement that conflicts with RFC 9110? Recommend admit (tier B) or reject with a located reason.",
         "Recommendation with located quotes; any conflict with RFC 9110 named with both quotes."),
    # ---- first falsifiers
    item("CriticContractAmbiguity", "critic", BOTH,
         "Attack the C1 public contract (SCORECARD \"Round 36 — declared claims\" at {REV}) for points it leaves undecided.",
         "- Write at least 20 concrete inputs (manifest plus body bytes) where two careful readers of the contract could give different findings, exits or targets; for each, the two readings and which sentence (or source) decides, or 'undecided'. Cover every bullet. Examples to consider: `<script>` inside a comment, `</script >` spacing, unclosed template, a BOM plus invalid bytes, charset with spaces or single quotes, a redirect whose Location is empty, duplicate check ids, a 200 hop with body but redirect before it to another host, uppercase `<SCRIPT>`, `<!---->`.\n- Save as {sb}/ambiguity.json (list of objects) and summarise.",
         "ambiguity.json with >=20 inputs, each with readings and a decider or 'undecided'; counts per bullet."),
    item("CriticPredicateIdentity", "critic", FR,
         "Attack §9 conformance of the declaration: is the predicate one sentence, identical in plan, code and receipts; was anything changed after data?",
         "- Compare the predicate sentence in SCORECARD at 3555f63f and {REV}, the `PREDICATE`/`TARGET`/`CASES` constants and the `met` expression in {L}/.ufo/waves/round-36/sealed_count.py and sealed_count_v1.py, and the `predicate` field in every receipt under {L}/.ufo/waves/round-36/verification/. Read the v2 note in SCORECARD and the git log of those files (`git -C {L} log --format='%H %cI %s' -- .ufo/waves/round-36/`). Was any receipt scored with v1 kept as if v2? Did v2 change anything beyond the jail? Diff v1 and v2.\n- Read the prompt rules at /home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-36.md section 6 item 9 and judge each bullet.",
         "Per §9 bullet: conforms or not, with a pasted diff or grep."),
    item("CriticAxisFit", "critic", FR,
         "Attack the claim's framing: axis by surface, capability status, and whether any cheap control could still meet the predicate.",
         "- Read the declaration and MISSION/AXES (/home/vgpnk/Projects/shokunin/MISSION.md, AXES.md). Is 'freshness' the right axis for a new re-check tool, or is it operability? Is it a capability per AXES §Capabilities (what must run in the round report)? Does the claim name the surface it moves and the command that shows it unmoved?\n- From the public counter and contract, design (do not build) the three cheapest controls you think score highest and estimate their score bound from the declared case structure (4 cases per bullet, one check per rule). Compare with the ablation receipts' pass counts.",
         "Verdict per question with quoted rule text; three control designs with bounded score estimates."),
    item("ReviewCounterV2", "reviewer", OP,
         "Review the counter `{L}/.ufo/waves/round-36/sealed_count.py` (version 3) for correctness.",
         "- Read every line. Check: project() maps observed ids back and compares (check, reason, target) as declared, with target only for moved; judge() exit/verdict/findings; materialize() id and body renaming (including '../' bodies), what happens with duplicate ids, non-string ids, a body path shared by two checks; the key-visible refusal; --tool-file path; error exits. Write synthetic cases in your sandbox and unit-test project/judge/materialize by importing the module (do not run main without a key; you have none).\n- List each defect with line number and a reproducer, and say whether it could change a pass count.",
         "Defect list with line numbers and reproducers, or 'none found' with the tests run."),
    item("ReviewJailIsolation", "reviewer", OP,
         "Review what the counter's jail (`jail()` in {L}/.ufo/waves/round-36/sealed_count.py) lets a jailed tool see, as a defensive check of the measurement.",
         "- In your sandbox, call jail() with a temp scratch dir and run a small harmless probe script inside it that lists which of these exist or are readable: /home, /fast, /etc, /usr, /tmp, the scratch dir's siblings, /proc/self, the parent process cmdline, network (try connecting to 127.0.0.1:9 with a 1 s timeout). Report each with yes or no.\n- Say whether the jail hides the key path, the lane repository and the counter's command line, and whether a case directory can see earlier case directories (same scratch dir).",
         "Visibility table from a pasted run; verdict on each of the three hidden items."),
    item("ReviewAblationDesign", "reviewer", FR,
         "Review whether the 34 ablation receipts support the declaration's claim that every contract bullet moves the target.",
         "- Read {L}/.ufo/waves/round-36/verification/ablations/*.json (names and pass counts, per-case pass flags) and the contract. Map each ablation name to the contract sentence it skips. List contract rules with no ablation (for example manifest-level input_invalid, fragment out of scope, 'no other finding for a check_invalid check', checksEvaluated). For each uncovered rule, say whether a tool that skips it could still meet the predicate, given 4 cases per bullet and target 25.",
         "Mapping table of ablations to sentences; uncovered rules listed with a bounded risk each."),
    item("ReviewSpotcheckDisposition", "reviewer", OP,
         "Check that every round-35 closure routed defect and every round-34 carried item has a round-36 disposition in progress.",
         "- Read {L}/corpus/lessons/round-35-verifier-spotcheck.md 'Routed defects' 1-5 and 'Defects' i-iii, {L}/corpus/lessons/round-35.md 'Carried open', and the wave items listed in {L}/.ufo/waves/round-36/w1-spec.json (names and targets only). For each defect: which item addresses it, or none. Flag defects nobody addresses.",
         "Table defect → item or 'none', with pointers."),
    item("MutCounterJudge", "mutation-tester", OP,
         "Mutation-test the counter's judge, projection and materialization on synthetic cases.",
         "- Copy {L}/.ufo/waves/round-36/sealed_count.py into your sandbox. Write 12 synthetic cases in the key's apparent shape (read materialize/judge for the fields: id, files {{name: {{b64}}}}, manifest, expect {{exit, verdict, findings}}), and a correct toy tool for them. Apply at least 12 single mutations to judge/project/materialize (drop the target comparison, compare target for all reasons, skip id mapping, sort vs multiset, ignore verdict, ignore exit, accept non-list findings, etc.) and show which mutations change the pass count of a correct tool and of three wrong tools you write. Survivors = judge parts no case would detect.\n- Do not change the key pin to read any real key; use your own synthetic key by calling the functions directly.",
         "Mutation table with killed/survived and the wrong tools used."),
    item("RevengerGateRule", "revenger", FR,
         "Reverse-engineer how round 34 and 35 verified Gate quotes, and whether the C1 contract's quote rule (c)+(d) agrees with that rule.",
         "- Read {L}/.ufo/waves/round-34/fetch_sources.py and {L}/.ufo/waves/round-35/fetch_sources.py (visible_text) and the Gate verification notes in {L}/corpus/lessons/round-34.md and round-35.md (ScribeGateLines reports under {L}/.ufo/waves/round-35/w1/). State the rule they used (tags, script/style, comments, entities, whitespace collapsed vs deleted, NFKC or not, template kept or removed) and list each difference from the C1 contract with a concrete input where the two disagree. Say which Gate quotes would change verdict.",
         "Rule statement with line pointers; difference list with inputs."),
]


def main():
    spec = {"wave": "kake-r36-w1", "milestone": "r36-build", "maxLanes": 64, "axes": ["operability", "freshness"],
            "reportDir": ".ufo/waves/round-36/w1", "context": CONTEXT, "items": ITEMS}
    (HERE / "w1-spec.json").write_text(json.dumps(spec, indent=1) + "\n")
    print(len(ITEMS), "items")


if __name__ == "__main__":
    main()
