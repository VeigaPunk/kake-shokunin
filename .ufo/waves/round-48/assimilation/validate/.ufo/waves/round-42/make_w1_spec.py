#!/usr/bin/env python3
"""Round-42 wave 1: the pre-freeze control wave for C1 (non-author controls scored with the candidate
counter before the declaration), the build (not scored by its seats), source opening, repairs routed by
the round-41 closure, and reviews of the counter. Usage: make_w1_spec.py REV"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
SB = "/fast/scratch/hyaku/kake-r42w1"
SH = "/fast/scratch/hyaku/kake-r42/shared"
W = f"{L}/.ufo/waves/round-42"
COUNTER = f"{W}/c42_count.py"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"
TOOLING = ("Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — "
           "read /home/vgpnk/.omp/agent/RULES.md first (official channels; record tool, version, channel and reason in your report). "
           "All pacman transactions are PAUSED host-wide (orchestrator ruling 2026-10-20): install via uv tool, npx or an official "
           "binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart.")

CONTEXT = f"""# Goal
Kake round 42, wave 1: test whether a counter separates a real speed-up of a URL check from cheaper tools, before the round's claim is frozen; plus the build (unscored), source opening, record repairs and reviews. The L1 (agent id KakeR42) is the only integrator and scorer; you are one leaf seat. Lane repo: {L} (tip {REV}). Lane axes: operability and freshness. This is ordinary software testing of a local, offline, network-free command-line tool that audits sitemap XML files.

# The planned claim (read {L}/SCORECARD.md section "Round 42 — C1 counter candidate")
`{L}/scripts/sitemap_audit.py` (the round-41 tool, sha256 50287ac6…, copy {SH}/tip41.py) judges URLs with a regular expression `_URI_RE` (lines 67-86) before `urlsplit`. That check is slow on long adversarial values (backtracking). C1: a rewritten check keeps EVERY judgment of the round-41 tool and costs at most 2.0 times the round-40 tool's CPU time (copy {SH}/base40.py, sha256 4de35f8c…) on five input shapes. Candidate counter: {COUNTER} (sha256 7bfc32c5…). Predicate: `met: the tool's exit code and output equal the round-41 tool's on every generated run, and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's`. Equality runs A/B/C and timing shapes T1–T5 are generated per run from a seed; read the counter's docstring. The round-41 tool itself scores T1 ≈5.4, T5 ≈9 (not met); the round-40 tool fails equality (3/8).

A "control" is a tool built to SKIP part of the claimed work: it judges some value differently from the round-41 tool, or it lowers the measured CPU without doing the work (hiding CPU, caching, keying on ids/shapes/labels, reading outside its case directory). If any control meets the predicate, the counter is too weak and the claim is redesigned or declared exploratory — so a control that meets is a valuable finding, not a failure. A tool whose judgments equal the round-41 tool's on every value, however written, is NOT a control. If your tool meets, also give a witness value on which it differs from tip41 (that is what makes it a control).

# Scoring a tool (control and mutant seats)
`timeout 900 prlimit --as=8000000000 -- python3 -B {COUNTER} --root {L} --tool-file <your tool> --label <YourName>-<suffix> --seed <N> --out {SB}/<YourName>/<suffix>.json` — exit 0 met, 1 not met, 2 cannot evaluate; about 50-90 s per run, single core. Run at most 3 counter processes at once. The receipt lists `equalRuns`, per-run `equal`/`candRepsEqual`, `ratios` and CPU samples. The L1 re-scores every tool that meets. Build seats (ExecBuild*) never run the counter.

# Bounds
- You are a leaf: no subagents, no swarm, no verdict on the round.
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report. Never edit files under {SH} or {W} (except your report).
- Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git is fine. Never run jj at /home/vgpnk/Projects/shokunin. If you need a clone: `git clone -q {L} {SB}/<YourName>/clone` after unsetting GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE.
- Cap every run with `timeout` (≤900 s), ≤8 parallel processes, `prlimit --as=8000000000`; bound every file you write (≤300 MB per seat; never append in a loop to a file Python imports; never point a log at sitecustomize.py or a .pth); kill every process tree you start before returning. Never run `du` or `find` over /fast/scratch as a whole.
- Network: only URLs your item names, GET only. Never request the operator's properties (ds4cc.com, app.ds4cc.com, operator *.onrender.com hosts, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json).
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- {TOOLING}
- A provider safety or policy refusal or an automatic model switch ends your item: a one-line report saying so; do not rephrase. Message only agent://KakeR42 for blockers; never agent://all. Plain English.

# Result
Report under 60 lines: what you built or checked, exact commands with exit codes, tool paths with sha256, counter results (equalRuns, ratios, met) for every tool you scored, findings with path:line, and per checked statement: holds / overstated / wrong. An unrun check has not passed. Time box: 30 minutes; a partial report (first line `PARTIAL:`) beats none.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, SH=SH, W=W, COUNTER=COUNTER)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR = ["operability"], ["freshness"]
CTL_ACC = ("First line: MET or NOT MET (did any of your tools meet the predicate). Tool path(s) and sha256, one receipt per tool "
           "(equalRuns, ratios, met), one line per tool naming the work it skips and which run caught it; for a meeting tool, a "
           "witness value where it differs from tip41, or a statement that none was found.")


def ctl(name, role, what, how):
    return item(name, role, OP,
                "Control class: " + what + " Measures: whether the counter scores a tool that skips this work as not met.",
                "- Build the tool(s) in {sb}/ (start from {SH}/tip41.py and/or {SH}/base40.py, Python 3 standard library only). " + how +
                "\n- Keep the skip. Within that constraint, try hard to meet the predicate (read {COUNTER} to see how runs and shapes are built).\n- Score every variant with the counter (seeds of your choice; record them).",
                CTL_ACC)


def mut(name, what):
    return item(name, "mutation-tester", OP,
                "Mutants of a fast rewrite of `_URI_RE`: " + what + " Measures: whether the counter's equality runs catch a one-member change of a rewritten regular expression.",
                "- In {sb}/, first write your own fast, behaviour-equal rewrite of `_URI_RE` in a copy of {SH}/tip41.py (possessive quantifiers `*+`/`++`/`?+` or atomic groups, Python ≥3.11; no backtracking blow-up); check it against tip41's `_parse_url` on your own generated values.\n- Then make ≥6 single-member mutants of YOUR rewrite in the named area (each changes one character class member, one quantifier or one alternative). Score the rewrite and every mutant with the counter.",
                "First line: MET or NOT MET for any mutant. Rewrite and mutant sha256s; per mutant the one-line change, receipt (equalRuns, ratios, met) and which run caught it; any mutant that meets with a witness value (or none found).")


ITEMS = [
    ctl("CtlTrivial", "executor", "trivial outputs.",
        "Variants: every check clean (exit 0); every check `check_invalid`; every entry `loc_not_absolute`; empty stdout with exit 0; junk bytes; a tool that reads the manifest only (no-reader) and copies tip41's verdict shape without parsing sitemap files."),
    ctl("CtlLengthGate", "mutation-tester", "skips or abbreviates the URL check above a length.",
        "Variants: tip41 that skips `_URI_RE` (urlsplit only, as base40) for values longer than 256, 1024, 2048, 10000 and 100000 code points; tip41 that runs `_URI_RE` on the first 1024 code points only."),
    ctl("CtlHeadTail", "mutation-tester", "judges only part of a long value.",
        "Variants: judge only the last N code points (N = 64, 128, 512) with a per-character table, only the first N, and head+tail combined; full judgment for values under 2,000."),
    ctl("CtlShapeKeyed", "executor", "fast paths keyed on the counter's timing shapes instead of a faster check.",
        "Variants keyed on: file size, number of `<url>` entries (20,000 / 50,000), a single long path segment, a defect within the last 64 code points, manifests with 48 checks or values of 200,000 code points; outside the keyed case run tip41 unchanged."),
    ctl("CtlCpuHide", "executor", "lowers the measured CPU without doing less work.",
        "Variants: do the work in a forked child the tool does not wait for (orphan, double fork, setsid); kill the parent process (the counter's runner) and exit; open /proc/<ppid>/fd/<n> to write a fake timing line; threads; multiprocessing; posix_spawn of a helper. Read the counter's RUNNER first."),
    ctl("CtlCache", "executor", "caches instead of judging.",
        "Variants: memoize `_parse_url` per value; memoize per value prefix/suffix; a cache file under /tmp (tmpfs per run) carried across runs if it survives; precomputed tables keyed on value hashes."),
    ctl("CtlKeyFinder", "executor", "looks outside its case directory for the expected outputs, the seed or the round-41 tool.",
        "Probe what the sandbox exposes: /proc (mountinfo, 1/environ, ppid cmdline, fds), /usr, /tmp, argv, timing; build a tool that uses anything label-bearing you find; report exactly what is visible."),
    ctl("CtlIdKeyed", "mutation-tester", "answers keyed on ids, file names, manifest names or check order.",
        "Base40 or tip41 plus rules that decide validity or take a fast path from properties of check ids, file names, manifest name or order; no character-level URL judgment beyond the tool you start from."),
    mut("MutRegexIP", "the IP-literal branch (drop `%`, add `|`, allow non-ASCII, restore round-40 parity with a broad branch plus a global TAB/CR/LF guard, drop `v` forms)."),
    mut("MutRegexPct", "percent triplets (one hex digit, lowercase-only hex, terminal `%`, `%` inside the host, `%` inside the port)."),
    mut("MutRegexRepertoire", "one-member drops or additions of the userinfo, host, path, query and fragment repertoires (`:`, `@`, `/`, `?`, sub-delims, `~`)."),
    mut("MutRegexNonAscii", "the non-ASCII range (start at U+00A0, exclude surrogates, exclude U+FFFE/U+FFFF, exclude astral planes, include U+007F)."),
    mut("MutRegexStructure", "structure (empty host, port letters or empty port, userinfo without `@`, second `#`, `?` inside the fragment, scheme characters)."),
    item("ReviewCounterCode", "reviewer", OP,
         "The candidate counter {COUNTER} (equality runs, timing loop, runner, ratio, receipt, exit codes). Read-only review; you may run it on {SH}/tip41.py and {SH}/base40.py.",
         "- Decide whether each docstring and SCORECARD statement about the counter holds in the code; look for paths where a failure becomes `met`, where a receipt is not written, where equality is not compared, or where a ratio is computed from missing samples.",
         "Findings with path:line and severity; per statement holds / overstated / wrong."),
    item("ReviewCounterGenerators", "reviewer", OP,
         "Do the counter's generated runs match their description (counts 1434/1200/656, T1 single-run values with one defect in the last 64 positions, lengths, distinct values, XML legality, the T4 SHA256SUMS check)?",
         "- Import {COUNTER} as a module in {sb}/ and call its generator functions with a few seeds; measure counts, lengths, defect positions, distinctness and segment structure; write nothing in the lane.",
         "Measured table per run/shape; per description sentence holds / overstated / wrong."),
    item("SentinelCounterSandbox", "sentinel", OP,
         "The isolation and timing integrity of {COUNTER} (`Sandbox.run`, `RUNNER`). Read-only review; you may run harmless probe tools you write in {sb}/ through the counter.",
         "- Decide what a tool under test can observe and write (paths, mounts, /proc, fds, the timing file, other processes, environment) and whether it can change the CPU time the counter records for itself or for the round-40 tool.",
         "Findings with path:line and severity; per SCORECARD sandbox statement holds / overstated / wrong."),
    item("CriticPredicate", "critic", OP,
         "C1's predicate, target and axis naming in {L}/SCORECARD.md section \"Round 42 — C1 counter candidate\", against the round prompt rules (/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-42.md §6 item 9) and {L}/corpus/QUALITY.md (n), (o), (r), (u).",
         "- Read only; no code runs. Is the predicate the same sentence in plan, code and receipt? Can a do-nothing or shortcut tool meet it? Is the 2.0 budget a target a cheap tool already meets? Is the axis named by the surface it changes? Any universal clause the counter does not enumerate?",
         "Per statement holds / overstated / wrong with reasons; the strongest attack a closure would make."),
    item("CriticHarmRule", "critic", OP,
         "The corrected harm rule (H1–H4) in the same SCORECARD section, against routed defect 1 of {L}/corpus/lessons/round-41-verifier-spotcheck.md.",
         "- Read only; no code runs. Does it name before data which new fixtures are change fixtures and which are guards, and price cost? Is any clause unmeetable by construction or met by doing nothing? Is the round-41 fixture classification a rule fitted after data, and does the closure note allow it?",
         "Per clause holds / overstated / wrong with reasons."),
    item("CriticZoneId", "critic", OP,
         "The declared zone-id behaviour (bracket contents limited to `[A-Za-z0-9._~:!$&'()*+,;=%-]` before urlsplit) in the same SCORECARD section and {L}/scripts/sitemap_audit.py:67-86.",
         "- Read only; no code runs. Does the declaration match the regex? Is any RFC 3986 IP-literal or RFC 6874 zone-id form outside that set? Is declaring it now (rather than restoring round-40 parity) a disposition the closure allowed?",
         "Per statement holds / overstated / wrong."),
    item("ProbeNoise", "executor", OP,
         "Hypothesis: a tool byte-identical to the round-40 tool scores every ratio within [0.8, 1.25] on five seeds under the current host load (so the 2.0 budget is outside noise).",
         "- Run the counter with `--tool-file {SH}/base40.py` on five seeds and with `--tool-file {SH}/tip41.py` on two seeds; at most 3 runs at once; record `uptime` before each.",
         "Hypothesis held / falsified, with every ratio and the load averages."),
    item("ProbeRunnerCalib", "mutation-tester", OP,
         "Hypothesis: the counter's RUNNER reports at least 90% of the CPU a probe tool burns in its own process, in threads, in waited children and in orphaned children.",
         "- In {sb}/ write probe tools that burn about 1 s of CPU in each mode and then print tip41's output for the case (copy tip41 and add the burn); import {COUNTER} and call `Sandbox(rng, td).run(...)` directly on a small case directory; compare reported CPU with the burn.",
         "Hypothesis held / falsified per mode with numbers."),
    item("ExecBuildRegex", "executor", OP,
         "The build: a fast, behaviour-equal `_URI_RE` in a copy of {L}/scripts/sitemap_audit.py, plus guard fixtures and the comment fix routed by the round-41 closure.",
         "- Work in a clone ({sb}/clone). Rewrite `_URI_RE` (lines 73-86) so matching never backtracks heavily: e.g. possessive quantifiers `*+`, `++`, `?+` or atomic groups (Python ≥3.11), runs `[set]*+(?:%XX[set]*+)*+`; keep every judgment of the round-41 tool. Change nothing else in the tool's behaviour.\n- Rewrite the comment at lines 67-72 and the regex comment at line 80 so they state the round-41 behaviour exactly: bracket contents limited to `[A-Za-z0-9._~:!$&'()*+,;=%-]`, then urlsplit; a zone id with a non-ASCII character or `|` is rejected; the port range is judged by urlsplit.\n- Add guard fixtures in the style of the `r41_*` fixtures of scripts/sitemap_audit_selftest.py, named `r42_*`: `loc` and `sitemapUrl` with zone ids `%eth0` and `%25eth0` (accepted), `%é` and `%en|0` (rejected); a 2,047-code-point single-segment `loc` ending in `%` (rejected) and a valid one (accepted). Every new fixture must pass on BOTH {SH}/tip41.py and your build.\n- Check: your `_parse_url` equals tip41's on ≥200,000 generated values of your own (long, short, IP literals, non-ASCII, defects anywhere); time both on long adversarial values. NEVER run {COUNTER}.",
         "Paths and sha256 of {sb}/sitemap_audit.py, {sb}/sitemap_audit_selftest.py and a unified diff {sb}/build.diff against the lane tip; selftest results on tip41 and build (counts, exit codes); differential count; timing table."),
    item("ExecBuildIndependent", "executor", OP,
         "An independent fast rewrite of the URL check, built without reading any other seat's work, to serve as an equivalence witness source.",
         "- In {sb}/, copy {SH}/tip41.py and replace `_URI_RE` matching with a different technique (e.g. a hand-written single-pass component scanner, or `str.translate`-based character tests plus a percent check), keeping every judgment of tip41.\n- Differential against tip41's `_parse_url` on ≥200,000 generated values of your own; list every disagreement you find (a disagreement in your tool is a bug to fix; a disagreement revealing odd tip41 behaviour is a finding). NEVER run {COUNTER}.",
         "Tool path and sha256; differential counts; any tip41 behaviour you found surprising, with values."),
    item("ExecH4Probe", "executor", OP,
         "The harm probe H4: the round-41 closure's probe method made reusable. Its script is {SH}/closure-probe/probe.py (oracle wheel beside it, sha256 cdcac127…).",
         "- In {sb}/ write `h4_probe.py --tool-file <cand> --base-file <base40> --seed N --out <json>`: seeded mutations (0-3 random insertions, deletions or duplications; ASCII 0x00-0x7F, broken percent units, delimiters, `[`, `]`, `é`, `:99999`) of the real `loc` values in {L}/.ufo/waves/round-41/realrun/sitemaps/; import each tool's `_parse_url` from its file; oracle = vendored abnf `rfc3986.Rule(\"URI\").parse_all` plus http(s) and a non-empty host. Report `validReject` (base accepts, oracle accepts, candidate rejects), `newAccept` (base rejects, candidate accepts), `oracleDisagree` (in-class only, as the closure defined it) and counts.\n- Run it on {SH}/tip41.py (seeds 924141 and 42001) and on {SH}/base40.py against itself.",
         "Script path and sha256; receipts with the counts; whether tip41 reproduces the closure's 0/0 and 0 in-class disagreements."),
    item("ExecHarmCriterionCheck", "executor", OP,
         "A check for a new QUALITY criterion: a frozen harm rule names, before data, each new fixture's class (change fixture: red on the base; guard: green on the base) and a numeric cost bound.",
         "- In {sb}/ write `harm_rule_check.py SCORECARD.md <round>`: find the round's pre-freeze / declared section in the given SCORECARD bytes, find its harm-rule bullet, and pass only when it names fixture classes (both the words for change fixtures and guards, or 'guards only'/'no change fixture') and a numeric cost bound (a ratio such as `2.0 times` / `≤ 2.0` or a time). Exit 0 pass, 1 fail, 2 cannot evaluate.\n- Show it able to fail: run it on `git -C {L} show 8eb121c8:SCORECARD.md` style bytes for round 41 (`git show 1ef7a0e9:SCORECARD.md`, round 41: expected FAIL) and on the lane tip's SCORECARD for round 42 (expected PASS); also on rounds 39 and 40.",
         "Script path and sha256; the four runs with exit codes and the lines they matched."),
    item("ScoutRFC6874", "scout", FR,
         "Sources for zone-id syntax in URIs: RFC 6874 and any RFC that updates or obsoletes it.",
         "- GET https://www.rfc-editor.org/rfc/rfc6874.txt and https://www.rfc-editor.org/info/rfc6874 ; follow any `Obsoleted by`/`Updated by` to that RFC's .txt. Locate the ZoneID ABNF and IPv6addrz (or their replacement); record sha256 of each body and HTTP status.\n- Run tip41's `_parse_url` (import {SH}/tip41.py) on `http://[fe80::1%25eth0]/`, `http://[fe80::1%25en1]/`, `http://[fe80::1%25%41]/`, `http://[fe80::1%eth0]/`, `http://[fe80::1%é]/`, `http://[fe80::1%en|0]/` and say which are RFC-valid under which RFC.",
         "Located quotes (≤25 words, with line numbers), sha256s, status lines, the table of six values, and a draft SOURCES row per source (columns as {L}/corpus/SOURCES.md)."),
    item("ScoutPythonRe", "scout", FR,
         "Source for possessive quantifiers and atomic groups in Python's `re`.",
         "- GET https://docs.python.org/3/library/re.html ; locate the possessive quantifiers `*+`, `++`, `?+` and the atomic group `(?>...)` paragraphs and their 'Added in version 3.11' notes; record sha256 and HTTP status; run `python3 --version` and a one-line check that `re.compile('a*+')` works on the host.",
         "Located quotes (≤25 words), sha256, and a draft SOURCES row in the {L}/corpus/SOURCES.md columns."),
    item("ScribeSupersedingRows", "scribe", FR,
         "Routed defect 4 of {L}/corpus/lessons/round-41-verifier-spotcheck.md: S117–S119 had `anchor`/`teaches` edited in place at 2653b629 and 0c5ad2f6 after they were committed at 9e3c31d2.",
         "- Read /home/vgpnk/Projects/shokunin/CORPUS.md section on SOURCES.md (rule 2 and how a correction is expressed) and `git -C {L} show 9e3c31d2:corpus/SOURCES.md`, `git -C {L} diff 9e3c31d2 2653b629 -- corpus/SOURCES.md`, `git -C {L} diff 2653b629 0c5ad2f6 -- corpus/SOURCES.md`.\n- Draft (in your report only) the exact row text that restores each original row's committed `anchor`/`teaches` if CORPUS.md requires that, the superseding rows S12x carrying the corrected text with a pointer to the row they supersede, and the old→new log lines for the lesson. Check the census rules in /home/vgpnk/Projects/shokunin/scripts/sources-census.sh for allowed `status` values.",
         "The draft rows and log lines, each tied to the CORPUS.md sentence it follows."),
    item("ScribeQualityCriterion", "scribe", OP,
         "Draft QUALITY criterion (v) for {L}/corpus/QUALITY.md: a frozen harm rule names before data each new fixture's class (change: red on the base; guard: green on the base) and a numeric cost bound, grounded in round-41 routed defect 1.",
         "- Read {L}/corpus/QUALITY.md criteria (n)–(u) for style and {L}/corpus/lessons/round-41-verifier-spotcheck.md. Draft ≤8 lines in that style naming the grounding lesson and the check script path {W}/criteria/harm_rule_check.py (being written by another seat), with red-on-round-41 / green-on-round-42 as the able-to-fail evidence.",
         "The draft text only."),
    item("ScribeMistakes", "scribe", OP,
         "Draft `## Mistakes` entries for {L}/corpus/lessons/round-42.md.",
         "- Entries: (1) round 41's frozen harm rule required every new fixture red on the base, unmeetable for guards by construction ({L}/corpus/lessons/round-41-verifier-spotcheck.md); (2) this round's counter draft 1 was met by the do-nothing tool (CPU read from bwrap's RUSAGE_CHILDREN, every sample 1–2 ms; `/` every ~80 characters bounded backtracking) — evidence {W}/draft1/ and SCORECARD \"Round 42 — C1 counter candidate\"; (3) S117–S119 edited in place. Shape: class · evidence pointer · captured-by · fix, as in {L}/corpus/lessons/round-41.md; for each fix, how it is shown able to fail.",
         "The draft entries with resolvable pointers."),
    item("ConnectorSiblingOverlap", "connector", OP,
         "Sibling-lane overlap: read-only scan of /home/vgpnk/Projects/shokunin/*-shokunin/ (SCORECARD.md, corpus/QUALITY.md, scripts/) for (a) harm rules that price runtime cost or classify fixtures as change vs guard, (b) regular-expression backtracking or URL-validation cost defects, (c) superseding-row practice in SOURCES.md.",
         "- Report pointers (file:line) and one line per pattern on what kake can reuse or must not duplicate; no edits.",
         "Table of pointers with one-line relevance."),
    item("ScoutSymlinkManifest", "scout", OP,
         "Routed defect 6 recon (planning only, not this round's claim): manifest `file` values that are symlinks to paths outside the manifest directory are read by {L}/scripts/sitemap_audit.py (`_file_value_invalid`, `_evaluate_check`).",
         "- In {sb}/ reproduce with tip41 (a manifest directory holding a symlink to a file outside it); read the contract {L}/.ufo/waves/round-39/c1-contract.md sentences on `file`; list what a fix would change and which existing fixtures it would touch. No lane edits.",
         "Reproduction commands and output; contract sentences quoted; a fix outline."),
    item("ReviewR41FixtureClasses", "reviewer", OP,
         "H1's classification of the 42 `r41_*` fixtures (29 change fixtures red on 8eb121c8, 13 guards green on both).",
         "- In a clone ({sb}/clone), run scripts/sitemap_audit_selftest.py against the base40 tool and the tip41 tool (read the selftest's usage to point it at a tool), and list every `r41_*` fixture with its result on each.",
         "The per-fixture table, the two counts, and whether H1's sentence holds."),
]

spec = {
    "wave": "kake-r42-w1",
    "milestone": "r42-controls",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-42/w1",
    "context": CONTEXT,
    "items": ITEMS,
}
(HERE / "w1-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS), "items")
