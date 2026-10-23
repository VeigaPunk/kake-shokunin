#!/usr/bin/env python3
"""Write the round-39 wave-1 spec (control wave + independent non-data work). Usage: make_w1_spec.py DECL_REV"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
BASE = "2909f1dcf2a4e411394a5093c4ed811a81809895"
SB = "/fast/scratch/hyaku/kake-r39w1"
REF = f"{SB}/shared/reference.py"
CONTRACT = f"{L}/.ufo/waves/round-39/c1-contract.md"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"
TOOLING = """Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, record tool, version, channel and reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via uv tool, npx or an official binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart."""

CONTEXT = f"""# Goal
Kake round 39, wave 1: the adversarial CONTROL wave plus independent non-data work, run BEFORE any build of the claimed tool exists. The L1 (KakeR39A2) holds integration and is the only scorer; you are one leaf seat. Lane repo: {L}. Lane axes: operability and freshness (web properties and publishing).

# The claim under attack (declared at {REV}; base {BASE})
C1 (capability): a new tool `scripts/sitemap_audit.py` (does NOT exist yet) audits local sitemap and sitemap-index files against the contract {CONTRACT} (sentences 1–34, rules (a)–(k)). Declaration: `git -C {L} show {REV}:SCORECARD.md | sed -n '/^## Round 39 — C1 declared/,$p'`. Frozen counter `{L}/.ufo/waves/round-39/sealed_count.py` scores a tool against a SEALED key of 24 cases (predicate `met: passed >= 24 of 24 sealed cases`); each case runs the tool inside bubblewrap with only /usr, the case files (a manifest plus sitemap files at /work) and the tool visible. A case passes only if exit code, verdict, error and every check's status, error and finding set match the contract exactly.

# Key-blindness (binding)
The key is sealed and you must not look for it: never read, list or search /fast/scratch/kake-r39-sealed/, /fast/scratch/hyaku/kake-r39a2/, or any file named cases.json or build_key.py outside your sandbox. Do not try to run the counter (it needs the key). The L1 scores every tool you return. A control is judged by how it scores, so build exactly the shape your item names, as well as you can.

# Bounds
- You are a leaf: no subagents, no swarm, no verdict on the round.
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report. Deliverables stay in your sandbox; give absolute paths and sha256 in the report.
- Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git (show, log, ls-tree, diff) is fine. Never run jj at /home/vgpnk/Projects/shokunin. If you need a lane checkout, clone it into your sandbox (`git clone -q {L} {SB}/<YourName>/clone`) after unsetting GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE.
- Cap every run with `timeout` (≤600 s), ≤8 parallel processes, `prlimit --as=4000000000` for blow-up inputs; kill any process tree you started before returning.
- Network: only the public URL your item names, GET only. Never request the operator's properties (ds4cc.com, app.ds4cc.com, operator *.onrender.com hosts, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json).
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- {TOOLING}
- A provider safety or policy refusal or an automatic model switch ends your item: a one-line report saying so; do not rephrase. Message only agent://KakeR39A2 for blockers; never agent://all. Plain English.

# Result
Report under 60 lines: what you built or checked, exact commands with exit codes, deliverable paths with sha256, and findings (path:line). An unrun check has not passed. Time box: 30 minutes; a partial report (first line `PARTIAL:`) beats none.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, BASE=BASE, REF=REF, CONTRACT=CONTRACT)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR = ["operability"], ["freshness"]
BOTH = ["operability", "freshness"]

CTL_ACC = ("A single Python 3 file `{sb}/control.py` runnable as `python3 control.py --manifest <path>` with only the standard library and /usr, "
           "plus `{sb}/NOTE.md` (≤15 lines: the shape, what it deliberately skips). Report its sha256. Do not read the reference implementation.")


def ctl(name, shape):
    return item(name, "critic", OP,
                "The C1 counter and key, attacked with one cheap control that skips the claimed work. Shape: " + shape,
                "- Read the contract {CONTRACT} (output format, sentences 33–34) so your control's output is well-formed where the shape allows.\n"
                "- Build the control; make it as strong as its shape permits (the aim is to reach the target while skipping the work, so a control that meets shows the counter is wrong).\n"
                "- Self-test it on 3–5 small manifests you write in {sb}/t/ to show it runs.", CTL_ACC)


MUT_ACC = ("`{sb}/mutants/M*.py` (each a full copy of the reference with ONE change) and `{sb}/mutants.json` "
           "listing per mutant: file, sha256, contract sentence number(s) it breaks, and a minimal input (manifest + sitemap) on which the contract and the mutant disagree. "
           "Aim for 6–12 mutants; prefer mutants you think a 24-case key could miss (boundaries, polarity, interactions between rules). Equivalent mutants are noted, not shipped.")


def mut(name, family):
    return item(name, "mutation-tester", OP,
                "The sealed key's power to kill tools that break one declared contract sentence, for the family: " + family,
                "- Copy the private reference {REF} (sha256 663e051e…2d69f8) into {sb}/; it implements the contract and scores 24 of 24.\n"
                "- Write single-point mutants that break exactly one sentence of the family's rules in {CONTRACT}; for each, build a minimal witness input and run both reference and mutant on it to show they differ.\n"
                "- Do not try to score them against the key; the L1 scores every mutant.", MUT_ACC)


def rv(name, role, axes, target, change, acc="Verdict per attacked statement (holds / overstated / wrong) with commands, exits and pointers."):
    return item(name, role, axes, target, change, acc)


ITEMS = [
    ctl("CtlConstClean", "constant output — every check `clean`, verdict `clean`, exit 0, ids echoed from the manifest; may emit `input_invalid` when the manifest is not a version-1 object."),
    ctl("CtlConstFindings", "constant findings — every check `findings` with the single most likely finding code/entry you can guess from the contract, verdict `failed-policy`, exit 1; nothing read but the manifest."),
    ctl("CtlConstError", "constant errors — every check `error` with `check_invalid` or `file_unreadable` chosen from manifest fields only, exit 2."),
    ctl("CtlJunk", "junk output — prints plausible-looking but wrong JSON (wrong key names, findings as strings) with the contract's exit codes chosen at random per run."),
    ctl("CtlNoReader", "manifest-only reader — reads the manifest (ids, file names, sitemapUrl) but never opens a sitemap file; decides each check's result from manifest strings alone (e.g. relative sitemapUrl → check_invalid, '..' → check_invalid, everything else clean)."),
    ctl("CtlLabelIds", "label shortcut — keys on check ids, file names, file sizes, positions and sitemapUrl strings (e.g. guesses findings from file names like 'bad', 'big', size > 50 MB → too_large) without parsing XML."),
    ctl("CtlShallowStdlib", "shallow stdlib reader — xml.etree.ElementTree parse + root name/namespace check + entry count only; no loc, scope, lastmod, changefreq or priority rules; correct manifest handling and verdicts."),
    ctl("CtlRegexOnly", "regex reader — no XML parser at all; finds <loc>, <lastmod>, <changefreq>, <priority> with regular expressions and implements as many value rules as regexes can, ignoring namespaces, prefixes, comments and entity escaping."),
    ctl("CtlFirstFinding", "first-finding-only — a reasonable implementation of the rules that stops at the FIRST finding per file (reports one finding per check)."),
    ctl("CtlXsdDelegate", "schema delegation — validate each file against the sitemaps.org XSDs (fetch https://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd and siteindex.xsd once into your sandbox and EMBED them; use whatever validator exists under /usr, e.g. `xmllint --schema` or python lxml if importable from /usr) and map schema errors to the contract's codes; no scope rule, no W3C-profile lastmod check beyond the schema."),
    ctl("CtlCodeGuess", "statistical guesser — reads each file as text and emits finding codes by keyword/heuristic scoring (e.g. 'changefreq' present → changefreq_invalid on entry 1 when value not lowercase), never building a parse tree."),
    ctl("CtlSandboxProbe", "key finder / sandbox escape — a tool that tries to obtain expected answers from anywhere other than the case files (environment, /proc, parent directories, /usr, timing, network). The counter runs it under `bwrap --ro-bind /usr /usr ... --ro-bind <case> /work --unshare-all --clearenv`; reproduce that sandbox from `{L}/.ufo/waves/round-39/sealed_count.py` and report every path or channel visible from inside it. Never read the sealed key yourself."),
    mut("MutEncodingXml", "(a) encoding and (b) well-formedness/DOCTYPE (sentences 6–9)."),
    mut("MutRootEntries", "(c) root and (d) entries, including namespace prefixes and foreign-namespace elements (sentences 10–14)."),
    mut("MutEntryChildren", "(e) loc_missing / loc_repeated / field_repeated / element_unexpected and the skip rules (sentences 15–18)."),
    mut("MutLimits", "(f) size and entry-count limits and their 'no other finding'/'in addition' clauses (sentences 19–20)."),
    mut("MutLocForm", "(g) whitespace stripping, absolute-URL test and loc length (sentences 21–23)."),
    mut("MutScope", "(h) scope: case-insensitive scheme/host, default ports, directory prefix, as-written comparison, index host-only (sentences 24–27)."),
    mut("MutLastmod", "(i) lastmod forms, calendar validity, TZD (sentences 28–30)."),
    mut("MutFreqPriority", "(j) changefreq and (k) priority (sentences 31–32)."),
    mut("MutManifestVerdict", "usage, manifest, check errors and the verdict/exit mapping (sentences 1–5, 33–34)."),
    mut("MutCrossRule", "interactions between rules: which findings suppress which (e.g. too_large vs others, loc_repeated skipping (g)/(h), field_repeated skipping value checks, loc_not_absolute skipping scope), entry numbering when non-entries are interleaved."),
    rv("CriticContractSentences", "critic", OP, "Contract {CONTRACT} as a rule of record.",
       "- For each sentence 1–34, say whether a 24-case key could plausibly test it and give a witness input that distinguishes a tool obeying it from one breaking it. List ambiguous sentences (two readings, both plausible) with both readings and an input where they differ. Do not read the reference or the key."),
    rv("CriticAxisFit", "critic", OP, "C1's axis and claim shape (declaration at {REV}).",
       "- Attack under the lane's sizing rules (prompt `/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-39.md` §6 item 9; `corpus/lessons/round-38-verifier-spotcheck.md`): is this a capability move or re-scoring? Can a do-nothing or shortcut control meet `24 of 24`? Is anything in the declaration a rule that could change after data? Is 'every tool other than the build bytes is a control' enforceable? Name the strongest objection a closure would raise."),
    rv("ReviewCounter", "reviewer", OP, "The frozen counter `{L}/.ufo/waves/round-39/sealed_count.py` (sha256 f3a0cd60…084593).",
       "- Read it line by line: can a tool pass a case without matching the contract (JSON tricks, duplicate keys, findings as dict vs list, None vs missing, extra checks, entry types like 1.0 vs 1 or true vs 1, NaN, huge output)? Does `met` equal the predicate sentence? Does revision mode refuse a revision holding the key? Write small fake tools in {sb}/ that probe each loophole against a FAKE key you write yourself (copy the counter, change KEY_SHA256/CASES to your fake key's values, never the real one)."),
    rv("SentinelCounterSandbox", "sentinel", OP, "The counter's bubblewrap sandbox and process handling.",
       "- In a copy of the counter with a fake key you write, try: fork bombs, 10 GB stdout, sleeping past the timeout, writing outside /work, reading /proc/1/environ, /proc/self/mountinfo, network sockets, leftover child processes after timeout. Report what the sandbox allows and any case where the counter hangs, crashes or mis-scores. Cap memory with prlimit and kill every process you start."),
    item("ReopenS102", "scout", OP, "SOURCES row S102 (`{L}/corpus/SOURCES.md`, sitemaps.org protocol) and its Gate quote in `{L}/corpus/lessons/round-39.md`.",
         "- Fetch https://www.sitemaps.org/protocol.html (GET), sha256 it against the row, locate the quote verbatim and count its words; check every contract sentence that cites S102 against the page text.", "Per check: holds / wrong, with the fetched line."),
    item("ReopenS103", "scout", OP, "SOURCES row S103 (sitemap.xsd, siteindex.xsd) and its Gate quote.",
         "- Fetch both XSDs, sha256 against the row, locate the quote; check the contract's readings of tLoc (minLength 12!), tLastmod, tChangeFreq, tPriority and the ##other wildcards against the schema text; flag any contract sentence that silently departs from S103 without a 'lane reading' label.", "Per check: holds / wrong, with the fetched line."),
    item("ReopenS104", "scout", OP, "SOURCES row S104 (W3C NOTE-datetime) and its Gate quote.",
         "- Fetch https://www.w3.org/TR/NOTE-datetime, sha256, locate the quote; check contract sentences 28–30 against the note (levels, TZD, field ranges, fraction digits).", "Per check: holds / wrong, with the fetched line."),
    item("ScoutGoogleSitemaps", "scout", OP, "How Google reads sitemaps compared with contract (a)–(k) — candidate SOURCES row.",
         "- Open https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap (S013) and https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps; record: priority/changefreq ignored?, lastmod use, size/count limits, index limits, cross-host rules. Give a draft SOURCES row (contract v1 columns) with URL, access time, sha256, and a ≤25-word located quote; mark where Google differs from the contract.", "Draft row plus a difference table, each line with its located quote."),
    item("ScoutBingSitemaps", "scout", OP, "A second engine's sitemap reading — candidate SOURCES row.",
         "- Find and open Bing Webmaster Guidelines or Bing's sitemap help page (official Microsoft/Bing domain only); record size/count limits, lastmod use and anything contradicting the contract. Draft a SOURCES row (or a rejected row with reason and flip) with URL, access time, sha256, ≤25-word located quote.", "Draft row with located quote."),
    item("ScribeKnowledgeEntry", "scribe", OP, "New knowledge entry `corpus/knowledge/sitemap-file-audit.md` (draft only).",
         "- Draft it in {sb}/sitemap-file-audit.md from the contract and the retained sources `{L}/.ufo/waves/round-39/sources/` (S102–S104): header lines `source:`, `verified-at:`, `recheck:` like `{L}/corpus/knowledge/robots-txt-rules.md`; sections: what a sitemap file must satisfy (with S-ids per claim), the two source conflicts and the lane readings, what the audit does not check, and how it differs from `sitemap-orphan-audit.md` and `crawl-scope-per-host.md`. Every factual sentence cites an S-id whose retained text you re-read; no claim about any tool's results.", "The draft path and sha256; a list of each sentence's S-id and the source line it rests on."),
    item("ScribeProvinceSkill", "scribe", OP, "Lane docs for the new capability (drafts only).",
         "- Draft, in {sb}/: (1) a `## Round-39 sitemap file audit step` for PROVINCE.md (≤12 lines, what moves Frontier→Core and what stays open), (2) a SKILL.md registry/usage entry for `scripts/sitemap_audit.py` in the style of the robots_audit entry (`grep -n robots_audit {L}/SKILL.md`), (3) a corpus/README.md frontier row. Write them conditionally: 'if the build meets the predicate'; no measured number.", "Three draft files with sha256."),
    item("ScribeLessonMistake", "scribe", ["operability", "freshness"], "Round-39 lesson `## Mistakes` entry (draft).",
         "- From `{L}/corpus/lessons/round-38-verifier-spotcheck.md` (C2 ruling) and `{L}/corpus/lessons/round-37-verifier-spotcheck.md`, draft one mistake: class · evidence pointer (path:line) · captured-by (the QUALITY criterion that should have caught it, or none) · fix, where the fix names a check shown able to fail. Also list which round-38 routed defects (1–6) round 39 addresses and which stay open, with pointers.", "Draft in {sb}/mistakes.md with sha256."),
    item("ExecCcCheck", "executor", OP, "QUALITY (j) check v2 (routed defect 4): `.ufo/waves/round-39/criteria/control_consequence_check.py` (write it in {sb}/ only).",
         "- Implement: `control_consequence_check.py --root <lane> --verification-dir <dir> [--build-revision <rev>]`. It reads every `*.json` receipt in the dir (recursively) that has a `predicate` field, and decides by CONTENT, never by file name, label or class text: a receipt with `met` true whose `toolSha256` is not the sha256 of `git show <build-revision>:scripts/sitemap_audit.py` is a control meeting the predicate → exit 1 listing it; without --build-revision every met receipt fails. Exit 0 otherwise; 2 on unreadable input.\n"
         "- Negative fixtures in {sb}/fixtures/: a met control receipt named `build-…json`; a met receipt with label 'build'; a met receipt whose toolSha256 differs from the build by one hex digit; a receipt dir where the build receipt is met and one control at 23. Show exit codes for each; mutate your own check (≥8 mutants) and show each mutant fails at least one fixture.", "Paths, sha256 and an exit-code table for fixtures and mutants."),
    item("ExecPublicSelftest", "executor", OP, "A public selftest for the future tool: `scripts/sitemap_audit_selftest.py` (write it in {sb}/ only).",
         "- From the contract alone (never the key or the reference), write `sitemap_audit_selftest.py --tool <path>` that materializes ≥40 small fixtures (manifest + files) in a temp dir, runs the tool, and checks exit, verdict and finding sets, printing `PASS n/N`. Cover every rule (a)–(k) with both polarities. Prove it can fail: run it against `{sb}/null.py` (prints nothing) and a constant-clean tool. Do not run it against the reference (you must not read it).", "Paths, sha256, the fixture count per rule, and the two failing runs' output."),
    item("ExecRealRunPrep", "executor", BOTH, "Real inputs for the future tool: owned sitemaps available offline.",
         "- Find sitemap files of the operator's properties on disk without network: `{L}/.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/` (S065), and read-only searches of ~/Projects/*/ for sitemap*.xml (do not modify any repo). Build {sb}/realrun/manifest.json (version 1, checks with id, file copied into {sb}/realrun/, sitemapUrl = the URL each file is served at, with the evidence for that URL). For each file, hand-derive the findings the contract expects (record your reasoning).", "Manifest path, files with sha256 and provenance, hand-derived expectations."),
    item("ConnectSiblings", "connector", BOTH, "Sibling-lane overlap for sitemap validation.",
         "- Search /home/vgpnk/Projects/shokunin/*-shokunin (read-only) for sitemap tools, knowledge or SOURCES rows (grep -ril sitemap). Report any sibling owning sitemap validation (tabi: client-side crawling; chousa: method) and whether C1 crosses kake's PROVINCE boundary (`{L}/PROVINCE.md` Adjacent).", "Overlap table with paths."),
    rv("ReviewDeclaration", "reviewer", OP, "The declaration commit {REV} versus its own rule.",
       "- Check: the predicate sentence is byte-identical in SCORECARD, the counter's PREDICATE and receipt `predicate` fields; CASES/TARGET; KEY_SHA256 pin; the before receipt `.ufo/waves/round-39/verification/base-2909f1dc.json`; that pre-summary.jsonl has no row at 24 except the reference; that no key path is in {REV}'s tree (`git ls-tree -r {REV} | grep -c sealed/`); every hash the declaration writes resolves. Re-run the counter at {REV} in a sandbox clone with `--revision {REV}` and any `--key-file` path (it must refuse or report tool absent; quote the output)."),
    rv("ReviewR38Evidence", "reviewer", OP, "Routed-defect-5 evidence `{L}/.ufo/waves/round-39/r38w2-evidence/` and the SCORECARD 'Round 38 — closure correction'.",
       "- Verify the SHA256SUMS against the files, compare a sample against /fast/scratch/hyaku/kake-r38w2/, check the four mutant hashes quoted in the closure (ed00b962, f20d1bf8, e11073ae, e7907567), and check the correction appends only (`git diff {BASE} {REV} -- SCORECARD.md | grep -c '^-[^-]'`)."),
]

spec = {
    "wave": "kake-r39-w1",
    "milestone": "r39-controls",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-39/w1",
    "context": CONTEXT,
    "items": ITEMS,
}
(HERE / "w1-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS), "items")
