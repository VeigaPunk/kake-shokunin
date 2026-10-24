#!/usr/bin/env python3
"""Round-39 attempt-3 wave-1 spec: adversarial control wave plus independent non-claim work.
Usage: make_w1a3_spec.py REV   (REV = lane commit holding the attempt-3 control receipts and the (j) check)
No item repeats a task of attempt 2's dead wave 1 (w1-spec.json); dead-seat tools were scored by the L1."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
DECL = "ceecb1b1f9093471eb0b17d2c9190e78bceb0b78"
BASE = "2909f1dcf2a4e411394a5093c4ed811a81809895"
SB = "/fast/scratch/hyaku/kake-r39a3w1"
REF = f"{SB}/shared/reference.py"
CONTRACT = f"{L}/.ufo/waves/round-39/c1-contract.md"
DEAD = f"{L}/.ufo/waves/round-39/a3-controls/dead-w1"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"
TOOLING = ("Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — "
           "read /home/vgpnk/.omp/agent/RULES.md first (official channels; record tool, version, channel and reason in your report). "
           "All pacman transactions are PAUSED host-wide (orchestrator ruling 2026-10-20): install via uv tool, npx or an official "
           "binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart.")

CONTEXT = f"""# Goal
Kake round 39 (attempt 3), wave 1: the adversarial CONTROL wave plus independent non-claim work, run BEFORE any build of the claimed tool exists. The L1 (agent id KakeR39A3) holds integration and is the only scorer; you are one leaf seat. Lane repo: {L}. Lane axes: operability and freshness (web properties and publishing).

# The claim under attack (declared at {DECL}; base {BASE}; current lane tip {REV})
C1 (capability): a new tool `scripts/sitemap_audit.py` (does NOT exist yet) audits local sitemap and sitemap-index files against the contract {CONTRACT} (sentences 1–34, rules (a)–(k)). Declaration: `git -C {L} show {REV}:SCORECARD.md | sed -n '/^## Round 39 — C1 declared/,$p'`. The frozen counter `{L}/.ufo/waves/round-39/sealed_count.py` scores a tool against a SEALED key of 24 cases (predicate `met: passed >= 24 of 24 sealed cases`). Each case runs the tool inside bubblewrap with only /usr, the case files (a manifest plus sitemap files at /work, read-only), the tool at /tool/tool.py and a private /tmp: no network, no environment, no lane, no key. A case passes only if exit code, verdict, error and every check's status, error and finding set match the contract exactly. Every tool scored with this counter other than the build bytes is a control; a control that reaches 24 changes C1's verdict, so controls are built as strong as their shape allows.

# Key-blindness (binding)
The key is sealed; never look for it: never read, list or search any path under /fast/scratch whose name contains `l1priv` or `sealed`, /fast/scratch/hyaku/kake-r39a2/, /fast/scratch/hyaku/kake-r39a3/, or any file named cases.json, build_key.py or make_key.py outside your own sandbox. Do not run the counter (it needs the key). Control and critic seats also never read any sitemap reference implementation (files named reference.py, sitemap_ref.py, sitemap_audit_ref.py) unless the item hands you one.

# Bounds
- You are a leaf: no subagents, no swarm, no verdict on the round.
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report. Deliverables stay in your sandbox; give absolute paths and sha256 in the report.
- Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git (show, log, ls-tree, diff) is fine. Never run jj at /home/vgpnk/Projects/shokunin. If you need a lane checkout, `git clone -q {L} {SB}/<YourName>/clone` after unsetting GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE.
- Cap every run with `timeout` (≤600 s), ≤8 parallel processes, `prlimit --as=4000000000` for blow-up inputs; bound every file you write (≤200 MB total per seat; never append in a loop to a file Python imports, never point a log at sitecustomize.py or any .pth); check `df -h /fast` before writing more than 1 GB; kill any process tree you started before returning. Never run `du` or `find` over /fast/scratch as a whole.
- Network: only the public URLs your item names, GET only. Never request the operator's properties (ds4cc.com, app.ds4cc.com, operator *.onrender.com hosts, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json).
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- {TOOLING}
- A provider safety or policy refusal or an automatic model switch ends your item: a one-line report saying so; do not rephrase. Message only agent://KakeR39A3 for blockers; never agent://all. Plain English.

# Result
Report under 60 lines: what you built or checked, exact commands with exit codes, deliverable paths with sha256, and findings (path:line). An unrun check has not passed. Time box: 30 minutes; a partial report (first line `PARTIAL:`) beats none.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, DECL=DECL, BASE=BASE, REF=REF, CONTRACT=CONTRACT, DEAD=DEAD)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR, BOTH = ["operability"], ["freshness"], ["operability", "freshness"]

CTL_ACC = ("A single Python 3 file `{sb}/control.py` runnable as `/usr/bin/python3 -B control.py --manifest <path>` inside the sandbox "
           "described in the context (standard library under /usr only; no third-party imports, no network, no files outside /work and /tmp), "
           "plus `{sb}/NOTE.md` (≤15 lines: the shape, what it deliberately skips). Report its sha256. Self-test it on 3–5 small manifests you write in {sb}/t/.")


def ctl(name, shape, extra=""):
    return item(name, "critic", OP,
                "The C1 counter and key, attacked with one control that skips claimed work. Shape: " + shape,
                "- Read the contract {CONTRACT} (output format, sentences 33–34) so the output is well-formed where the shape allows.\n"
                "- Build the control as strong as its shape permits: the aim is to reach 24 of 24 while skipping the named work; a control that reaches it shows the counter is wrong, which is a finding the round needs.\n"
                + extra, CTL_ACC)


def tweak(name, base, score, rule):
    return item(name, "critic", OP,
                f"The near-miss shortcut control `{{DEAD}}/{base}` (scored {score} of 24 by the L1 under the frozen counter; receipt `{{L}}/.ufo/waves/round-39/verification/a3/dead-{base[:-3]}.json` shows only the total you may use: do not read its `rows`).",
                f"- Copy it to {{sb}}/control.py and improve it by at most 60 changed lines (count with `diff -u | grep -c '^[+-][^+-]'`) {rule}, guided only by the contract {{CONTRACT}}, to raise its score toward 24.\n"
                "- You get no per-case feedback; reason from the contract sentences the shape likely misses.", CTL_ACC)


MUT_ACC = ("`{sb}/mutants/M*.py` (each a full copy of the reference with ONE change) and `{sb}/mutants.json` listing per mutant: file, sha256, "
           "the contract sentence number(s) it breaks, and a minimal witness input (manifest + sitemap) on which reference and mutant outputs differ "
           "(show both outputs). 6–12 mutants; prefer ones a 24-case key could miss. Equivalent mutants are noted, not shipped. "
           "Delete your copy of the reference itself from {sb}/ before returning (keep mutants).")


def mut(name, family):
    return item(name, "mutation-tester", OP,
                "The sealed key's power to kill tools that break one declared contract sentence; family: " + family,
                "- Copy the reference {REF} (sha256 663e051e…2d69f8; it scores 24 of 24) into {sb}/; read the contract {CONTRACT}.\n"
                "- Write single-point mutants, each breaking exactly one contract sentence of the family; build a witness input for each and run reference and mutant on it.\n"
                "- Do not score them against the key; the L1 scores every mutant.", MUT_ACC)


def scout(name, target, change, acc="A draft SOURCES row in the contract-v1 shape of {L}/corpus/SOURCES.md (see `/home/vgpnk/Projects/shokunin/CORPUS.md` section 'SOURCES.md — where a shokunin learns'): URL, access time (UTC), HTTP status, sha256 of the fetched bytes (file kept in {sb}/), a ≤25-word quote located by line in the fetched text, and the contract sentence numbers it grounds or contradicts. Or a reject with reason."):
    return item(name, "scout", OP, target, change, acc)


ITEMS = [
    # Controls: new shapes (attempt 2's twelve dead control seats are scored, not resent)
    ctl("CtlLaneToolWrapper", "cheapest wrapper around code the lane already has — port the sitemap handling in {L}/scripts/freshness-sweep.mjs (PQ-14 live/source sitemap parity, `<loc>` extraction) and any sitemap-entry logic in {L}/scripts/link_preview_audit.py into Python, wrap it in the contract's manifest and output format, and add nothing the existing code does not already decide."),
    ctl("CtlStdlibConvenience", "lazy implementer — attempts every rule (a)–(k) but only through standard-library conveniences, never a hand-written lexical rule: xml.etree for structure, str.strip() for whitespace, urllib.parse (urlsplit, .port, .hostname) for loc and scope, datetime.fromisoformat for lastmod, float() for priority, `in` on a set for changefreq."),
    ctl("CtlEngineLenient", "lenient search-engine reader — reads sitemaps the way a forgiving crawler does: parse, collect `loc`s, drop what it cannot use; ignores priority and changefreq values, accepts any ISO-8601-looking lastmod, accepts any loc urlsplit can parse, never rejects for size or count; manifest handling and verdict mapping per contract."),
    ctl("CtlStructureOnly", "structure-only — implements sentences 1–20 (manifest, encoding, well-formedness, DOCTYPE, root, entries, entry children, limits) exactly, and none of the value rules 21–32 (no loc form, scope, lastmod, changefreq or priority findings)."),
    ctl("CtlValuesOnly", "values-only — implements the value rules 21–32 exactly on every `loc`/`lastmod`/`changefreq`/`priority` element found anywhere (local-name match), with manifest handling and verdicts per contract; any parse exception gives `xml_malformed`; no encoding, DOCTYPE, root, entry-structure, repeat or limit rule."),
    ctl("CtlHandTokenizer", "parser-free tokenizer — splits the file on `<` and `>` with str methods (no re, no xml.*, no html.*), tracks a tag stack by hand, and implements as many rules as that allows; ignores namespaces beyond the literal prefix text."),
    ctl("CtlHtmlParserReader", "wrong-parser reader — reads each sitemap with html.parser.HTMLParser (lower-cases names, no namespaces, tolerant of malformed input) and implements the rules on what it sees; no xml.* module."),
    ctl("CtlNamespaceBlind", "namespace-blind reader — a careful implementation of the rules that matches element LOCAL names only (xml.dom.minidom or ElementTree with namespaces stripped), never checks the sitemap namespace URI (sentences 10, 11, 14 skipped)."),
    tweak("CtlGuessTweak", "CtlCodeGuess.py", 23, "without adding any XML or HTML parser (no xml.*, html.*, no hand-built tag tree)"),
    tweak("CtlRegexTweak", "CtlRegexOnly.py", 19, "without adding any XML or HTML parser (regular expressions only)"),
    tweak("CtlXsdTweak", "CtlXsdDelegate.py", 19, "without adding any rule the schemas do not express (no scope rule, no W3C-profile lastmod check beyond the schema types)"),
    # Mutants of the reference: cross-cutting families
    mut("MutNumericBoundaries", "every numeric boundary — 52,428,800 bytes, 50,000 entries, 2,048 code points, priority 0.0/1.0 inclusive and exact-decimal compare, hh 23, mm 59, ss 59, leap years (1900, 2000, 2024), month lengths."),
    mut("MutStdlibSubstitution", "replacing one hand-written lexical rule by a standard-library convenience (str.strip for sentence 21, urlsplit().port for 24, fromisoformat for 28–29, float() for 32, str.lower for 31, os.path.normpath for 26)."),
    mut("MutNamespaceBinding", "namespace handling — prefixed sitemap namespace, default namespace redeclared on a child, entry or field in a foreign namespace, a foreign element named `url`, the 0.9 URI with a trailing slash or different case (sentences 10, 11, 13, 14, 17)."),
    mut("MutEntryNumbering", "finding identity — entry positions counted 0-based, counting foreign-namespace or unexpected elements as entries, `null` versus a number for file-level findings, duplicate findings collapsed or kept (sentences 11, 33 and the findings-as-set rule)."),
    mut("MutUrlAuthority", "URL authority and form — explicit default port (`:80`, `:443`), empty port (`host:`), userinfo, IPv6 literal, upper-case scheme, empty path read as `/`, query or fragment in sitemapUrl, the directory of a sitemapUrl ending in `/` (sentences 4, 22, 24–27)."),
    # (j) check v2 (landed at REV)
    item("MutCcCheckV2", "mutation-tester", OP, "QUALITY (j) check v2 `{L}/.ufo/waves/round-39/criteria/control_consequence_check.py` at {REV} (routed defect 4 of `{L}/corpus/lessons/round-38-verifier-spotcheck.md`).",
         "- Copy it into {sb}/; write ≥12 single-point mutants (decision by name or label, trusting `met`, ignoring counterSha256 or keySha256, build by revision instead of bytes, exemption without --oracle-sha, missing recursion, exit-code swaps, rows-count off by one).\n"
         "- Run `python3 -B <mutant> --selftest` for each and also run each against a receipt directory you build in {sb}/rx/ from copies of `{L}/.ufo/waves/round-39/verification/a3/*.json`; report survivors (mutants whose selftest still prints PASS 14/14) and a fixture that would kill each.",
         "Table: mutant, sha256, change, selftest result, killing fixture for survivors."),
    item("ReviewCcCheckV2", "reviewer", OP, "QUALITY (j) check v2 `{L}/.ufo/waves/round-39/criteria/control_consequence_check.py` at {REV}.",
         "- Check it against routed defect 4 (classify by declaration content, not by file name or by the class text under test) and the frozen class sentence in `git -C {L} show {DECL}:SCORECARD.md` ('Control classes, frozen now'). Can any receipt meet the predicate yet pass as non-control? Does reading B (`--oracle-sha`) widen anything beyond the one named tool? Run its selftest and both invocations on `{L}/.ufo/waves/round-39/verification/a3/` and quote outputs.",
         "Verdict per question (holds / wrong) with commands, exits, path:line."),
    # Sources (frontier)
    scout("ScoutXmlSpec", "XML 1.0 Fifth Edition (https://www.w3.org/TR/xml/) as the source for contract sentences 7–9 and 21.",
          "- Open it (GET); locate production [3] S (white space), the document type declaration §2.8 and the encoding declaration §4.3.3; say whether sentence 21's whitespace set equals S and whether sentence 7's case-insensitive `UTF-8` compare matches §4.3.3."),
    scout("ScoutXmlNamespaces", "Namespaces in XML 1.0 Third Edition (https://www.w3.org/TR/xml-names/) as the source for contract sentences 10, 11 and 14.",
          "- Open it (GET); locate the rules for default namespace scope, prefix binding and namespace-name comparison (§2.3: compared as strings, case-sensitive); say whether the contract's 'whatever prefix binds it' and 'any other namespace … ignored' follow from it."),
    scout("ScoutXsdDatatypes", "W3C XML Schema 1.1 Part 2 Datatypes (https://www.w3.org/TR/xmlschema11-2/) for `decimal`, `date` and `dateTime` lexical spaces (contract sentences 28–32).",
          "- Open it (GET); locate the decimal lexical mapping and the date/dateTime lexical rules (timezone optional, year range, 24:00:00); quote where they differ from the contract's lane readings in sentences 28–30."),
    scout("ScoutSitemapsFaq", "sitemaps.org FAQ (https://www.sitemaps.org/faq.html) as a second page from the protocol's own site.",
          "- Open it (GET); record what it says about entity escaping, URL encoding of loc, file location/scope, gzip and the 50,000/50 MB limits; flag any contradiction with contract sentences 19–27."),
    scout("ScoutYandexSitemaps", "Yandex Webmaster sitemap help (official yandex.com / yandex.ru help domain only) as a second engine's reading.",
          "- Find and open the official page; record its size/count limits, lastmod use, encoding rules and cross-host rules, quoting where it differs from contract (a)–(k)."),
    item("ScoutPublicSitemaps", "scout", OP, "Real-world sitemap files for a post-build real run (inputs only).",
         "- From six well-known public non-operator sites whose robots.txt allows fetching /sitemap.xml (e.g. www.python.org, www.kernel.org, www.debian.org, www.gnu.org, www.w3.org, docs.github.com — pick others if absent), fetch each robots.txt and one sitemap or sitemap index (≤5 MB each, GET, one request per URL), keep bytes in {sb}/realrun/, and write {sb}/realrun/manifest.json (version 1: id, file, sitemapUrl = the URL fetched).",
         "Manifest path; per file: URL, HTTP status, bytes, sha256, the robots.txt line allowing it. No expectations, no tool runs."),
    # Executors: non-claim repairs and a guard
    item("ExecRobotsDeclaredFixtures", "executor", OP, "Routed defect 3 of `{L}/corpus/lessons/round-38-verifier-spotcheck.md` (lines 174–176): the robots selftest `{L}/scripts/robots_audit_selftest.py` lacks fixtures for sentences declared in round 38.",
         "- In a sandbox clone at {sb}/clone, add fixtures for: `/robots.txt?` (empty query), bare `%`, explicit `Disallow: /robots.txt`, the 20 s bound on a 64 MiB integer literal, and the six MutBuildTool survivors (H03 sign of short integers, H04 truncation of short integers, `_` rejected, U+00A0 rejected, implicit allow https-only, implicit allow below a directory; see `{L}/.ufo/waves/round-39/r38w2-evidence/MutBuildTool/`). Derive each expected value from the round-38 contract text and cite it. Do NOT change scripts/robots_audit.py.\n"
         "- Run the extended selftest against the unchanged tool and against the four reference mutants in `{L}/.ufo/waves/round-39/r38w2-evidence/CriticKeyExpectations/mutants/`; each mutant must fail ≥1 new fixture.",
         "Patch file {sb}/robots-selftest.patch with sha256; fixture count before→after; pass/fail of the unchanged tool per new fixture; which mutant each fixture kills."),
    item("ExecRecheckOversize", "executor", FR, "Carried defect: `{L}/scripts/source_recheck.py` can emit `moved` alongside `check_invalid` on an oversized body and count it in `checksEvaluated` (`{L}/SCORECARD.md` 'Defects carried to round 39'; ReviewRecheckCaps P2).",
         "- In a sandbox clone at {sb}/clone, write a failing fixture in the existing selftest style, then the minimal fix. Run `source_recheck_selftest.py` and `source_recheck_hardening_selftest.py` before and after (commands from their headers).",
         "Patch {sb}/recheck-oversize.patch with sha256; the new fixture failing before and passing after; both selftests' totals before and after."),
    item("ExecCopyGuard", "executor", OP, "A copy guard for the future build: `{sb}/copy_guard.py` (stdlib only).",
         "- Implement `copy_guard.py --candidate <py> --against <py>...`: normalise each file (strip comments and docstrings, rename identifiers in order of first use via the ast module) and print, per pair, the longest common normalised token run and difflib ratio; exit 1 if any ratio ≥ 0.6 or a common run ≥ 200 tokens.\n"
         "- Show it can fail: fixtures in {sb}/fx/ — a file vs itself with identifiers renamed and comments changed (must exit 1), two independent implementations of a small function (must exit 0). Use the committed controls in {DEAD}/ as the 'against' corpus in one demo run.",
         "Path, sha256, fixture exit codes, demo output."),
    # Critic, connector, scribes, reviewer
    item("CriticReadingAB", "critic", OP, "The drafting defect recorded at {REV}~1 (`git -C {L} show 915e9e87:SCORECARD.md | sed -n '/Drafting defect/,$p'`): is the private reference (sha256 663e051e…, scored 24 before the declaration and re-scored 24 by the L1 at {REV}, receipt `{L}/.ufo/waves/round-39/verification/a3/ref.json`) a control under the frozen class sentence?",
         "- Argue reading A (literal: it is a control; kill rule (1) makes C1 exploratory) and reading B (it is the key's oracle named in the declaration, not a control) against the frozen text at {DECL}, the prompt's §6 item 9 (`/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-39.md` lines 343–365), and the closures `{L}/corpus/lessons/round-37-verifier-spotcheck.md`, `{L}/corpus/lessons/round-38-verifier-spotcheck.md`. Which reading would a strict closure adopt and why? Does the L1's re-score at {REV} change anything? What must the report say under each?",
         "Ruling-ready analysis, ≤40 lines, every claim with path:line."),
    item("ConnectClosurePrecedent", "connector", BOTH, "Fleet precedent on (1) oracle/reference implementations that score a sealed key before the declaration, (2) exploratory claims admitted with a named non-author reviewer.",
         "- Read-only: search /home/vgpnk/Projects/shokunin/*-shokunin/corpus/lessons/round-*-verifier-spotcheck.md and /home/vgpnk/Projects/shokunin/.ufo/reports/round-*/ for 'oracle', 'reference', 'exploratory', 'unprovable-but-better'; list each ruling with lane, round, path:line and its outcome.",
         "Precedent table (lane, round, pointer, ruling, how it applies to kake C1)."),
    item("ScribeCarriedDefects", "scribe", BOTH, "Routed defect 6 of `{L}/corpus/lessons/round-38-verifier-spotcheck.md` (lines 181–185): ten carried items.",
         "- For each of the ten items, state at lane revision {REV} whether it is still open, with a pointer (path:line or a command and its output) and the smallest fix; never edit the lane.",
         "Draft table in {sb}/carried.md with sha256."),
    item("ScribeQualityCriterion", "scribe", OP, "A QUALITY.md criterion from round 39's drafting defect (`git -C {L} show 915e9e87:SCORECARD.md | sed -n '/Drafting defect/,$p'`) and the existing (j)–(n) in `{L}/corpus/QUALITY.md`.",
         "- Draft one criterion (o): a control-class sentence must name, by sha256, every tool already scored with the counter before the declaration (oracle, reference, ablations), saying which class each belongs to; give a mechanical check (command over committed bytes) that fails on round 39's declaration text and passes on a corrected one. Show both runs.",
         "Draft in {sb}/criterion-o.md with sha256, the check command and both outputs."),
    item("ReviewA3Receipts", "reviewer", OP, "The L1's attempt-3 control receipts `{L}/.ufo/waves/round-39/verification/a3/*.json` at {REV} and the copied dead-seat tools `{DEAD}/`.",
         "- For each receipt check by content: `toolSha256` equals `sha256sum` of the committed tool copy it names (or the reference sha 663e051e… for ref.json), `counterSha256` = sha256 of `{L}/.ufo/waves/round-39/sealed_count.py` at {DECL}, `keySha256` = the pin in that counter, 24 rows, `passed` = count of passing rows, `met` consistent; compare each copied tool with its original under /fast/scratch/hyaku/kake-r39w1/<Name>/control.py by sha256. Never open the key.",
         "Per-receipt table (holds / wrong) with commands and outputs."),
]

spec = {
    "wave": "kake-r39a3-w1",
    "milestone": "r39-controls-a3",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-39/w1a3",
    "context": CONTEXT,
    "items": ITEMS,
}
(HERE / "w1a3-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS), "items")
