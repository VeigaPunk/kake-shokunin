#!/usr/bin/env python3
"""Round-43 wave 1 (single v2 wave: build + attack, policy v2 band 64-96). Usage: make_w1_spec.py REV"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
SB = "/fast/scratch/hyaku/kake-r43"
W = f"{L}/.ufo/waves/round-43"
COUNTER = f"{W}/c43_count_v4.py"
COUNTER_SHA = "1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab"
BUILD = "020bc4574729ed674299f6cab02faac1582d9464"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"
TOOLING = ("Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — "
           "read /home/vgpnk/.omp/agent/RULES.md first (official channels; record tool, version, channel and reason in your report). "
           "All pacman transactions are PAUSED host-wide (orchestrator ruling 2026-10-20): install via uv tool, npx or an official "
           "binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart.")

CONTEXT = f"""# Goal
Kake round 43, wave 1 (single v2 wave, build + attack together): falsify what the L1 froze at {REV}. The L1 (agent id KakeR43) is the only integrator; you are one leaf seat with one item. Lane repo: {L} (freeze tip {REV}). Lane axes: operability and freshness. Ordinary software testing of a local, offline command-line tool that audits sitemap XML files.

# What landed at {REV} (read {L}/SCORECARD.md "Round 43 — C1 and C2 declared (frozen before any seat scores)")
- C1 (operability): counter v4 `{COUNTER}` (sha256 {COUNTER_SHA}) = round-42 counter v3 + run F and timing-shape classes (6+-digit ports, mostly out-of-range and otherwise clean; case-fold pairs under segment-cased sitemapUrls; tail-defective shared-prefix pairs in both orders; repeated-host blocks; common-host values on localhost/example.invalid/sitemaps.invalid/test.invalid plus a basket). Predicate (frozen sentence): `met: the tool's exit code and output equal the round-41 tool's on every generated run, and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's`. Target: the round-42 build `{BUILD}` (tool sha256 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021) met on three independent os.urandom seeds. Kill rules: any live-seat control meeting v4 -> C1 NOT MET; a below-predicate build -> honest-stop miss; a seat-demonstrated counter unsoundness (do-nothing/junk/constant meeting v4, or frozen references disagreeing) -> C1 NOT MET. L1 freeze receipts: `{W}/verification/freeze/` (build-1..3 met 11/11; ref41-base not met T1 4.27 T5 8.68; r42ctl-M8/v1/v2/v4 not met; junk 0/11).
- C2 (freshness): the round-29/33 misroot fleet paths declared absent (annotation rows corpus/lessons/round-29.md:104 and round-33.md:45; pins pathsMissSet 63->65; movement census with EOF corrections in .ufo/waves/round-30/w2/CriticC1Scope.md and .ufo/waves/round-34/w1/CriticFrontierNovelty.md). `node scripts/freshness-sweep.mjs --section=paths` exit 1 -> 0.
- Routed repair 1: registry arithmetic corrected (119 -> 128 rows, mined +7, rejected +2) with able-to-fail checker `{W}/registry_count_check.py` (red on r42 claims, green on r43).
- Frontier: SOURCES S129 (tameshi r33 verification fixtures) and S130 (kama r29 self-assessment-at-writing), sibling adjacency imports; lesson {L}/corpus/lessons/round-43.md.
- Dispatch protocol: the L1 froze everything above BEFORE this wave was dispatched; any evidence you find of a seat score predating {REV} is a conformance defect to report.

# Scoring a tool with the frozen counter
`timeout 900 prlimit --as=8000000000 -- python3 -B {COUNTER} --root {L} --tool-file <tool> --label <YourName>-<suffix> --out {SB}/<YourName>/<suffix>.json` (exit 0 met, 1 not met, 2 cannot evaluate; ~30-240 s; at most 3 at once per seat). Score WITHOUT --seed (seed drawn from os.urandom, recorded in the receipt).

# Bounds
- You are a leaf: no subagents, no swarm, no verdict on the round.
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report.
- Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git is fine. Never run jj at /home/vgpnk/Projects/shokunin. Clone only into {SB}/<YourName>/ with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE unset.
- Cap every run with `timeout` (<=900 s), <=8 parallel processes, `prlimit --as=8000000000`; bound every file you write (<=300 MB per seat; never append in a loop to a file Python imports; never point a log at sitecustomize.py or a .pth); kill every process tree you start before returning. Never run `du` or `find` over /fast/scratch as a whole.
- Network: only URLs your item names, GET only. Never request the operator's properties (ds4cc.com, app.ds4cc.com, operator *.onrender.com hosts, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json).
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- {TOOLING}
- A provider safety or policy refusal or an automatic model switch ends your item: a one-line report saying so; do not rephrase. Message only agent://KakeR43 for blockers; never agent://all. Plain English.

# Result
Report under 60 lines: first line your verdict on what you attacked (MET / NOT MET / CONFORMANT / DEFECT: <what>); exact commands with exit codes; tool paths with sha256; findings with path:line; per checked statement holds / overstated / wrong. An unrun check has not passed. Time box: 25 minutes; a partial report (first line `PARTIAL:`) beats none.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, W=W, COUNTER=COUNTER, BUILD=BUILD, COUNTER_SHA=COUNTER_SHA)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR = ["operability"], ["freshness"]
BOTH = ["operability", "freshness"]
CTL_ACC = ("First line MET or NOT MET. Per tool: path, sha256, one-line skip, receipt (seed, equalRuns, ratios, met), which run caught it, "
           "and for a meeting tool a witness value where its `_parse_url` or CLI output differs from the round-41 tool "
           "(copy {W}/controls-r42 is not needed — the references are pinned in the counter).")
MUT_ACC = ("First line KILLED or SURVIVED. Per mutant: path, sha256, the one-member change, receipt (equalRuns, met), and for a survivor a witness value "
           "where it differs from the round-41 tool. Every scored mutant gets its own receipt file.")


def mut_counter(name, what, show):
    return item(name, "mutation-tester", OP,
                "Attacks: counter v4's power to catch one-member weakenings of the round-43 classes: " + what,
                "- Copy {COUNTER} into {sb}/ (keep the PREDICATE sentence byte-identical; weaken only the named class). Make >=4 one-member variants: " + what +
                "\n- Build the matching control from {L}/scripts/sitemap_audit.py (the build) or write a small fresh tool embodying the named skip; score every weakened counter against it (no --seed). " + show,
                MUT_ACC)


def ctl(name, what, how):
    return item(name, "executor", OP,
                "Attacks: counter v4 against a fresh control class: " + what,
                "- Build >=3 variants in {sb}/ from {L}/scripts/sitemap_audit.py (the fast build, revision {BUILD}) by adding the named skip. Keep the skip; try hard to meet the predicate. Score each with the counter (no --seed).",
                CTL_ACC)


def mut_build(name, area):
    return item(name, "mutation-tester", OP,
                "Attacks: the build's " + area + " area with one-member mutants, scored by counter v4 (the r42 pattern at v4 strength).",
                "- Copy the build tool out of the lane with read-only git (`git -C {L} show {BUILD}:scripts/sitemap_audit.py > {sb}/build.py`; sha256 must be 914ebdee...cd021). Make >=5 single-member mutants in the " + area + " area (one class member, one boundary, one branch condition). Keep each mutant fast. Score every mutant with the counter (no --seed).",
                MUT_ACC)


items = [
    # --- counter mutation coverage (each class must be load-bearing) ---
    mut_counter("MutCounterPort", "6+-digit ports (remove F port values; shorten ports to 5 digits; remove T1/T3/T5 port variants; padded-in-range ports only)",
                "The M8-style control (port loop capped at 5 digits) must MEET every weakening that removes the discriminating values and FAIL the unweakened v4 — run it on v4 too as the baseline."),
    mut_counter("MutCounterFold", "case-fold pairs (remove F foldpairs; make the T2 second member an independent value, not the exact fold partner; segment_smu replaced by the root-dir derived smu)",
                "The case-fold memo control (cache keyed on upper-to-lower folded value) must MEET every weakening and FAIL unweakened v4."),
    mut_counter("MutCounterPrefix", "shared-prefix pairs (prefix cut to 16 and 24 code points; remove F prefixpairs; remove the T3 prefix-pair branch)",
                "The 32-prefix table control must MEET every weakening and FAIL unweakened v4."),
    mut_counter("MutCounterHost", "common-host and repeated-host classes (remove F common-host values; remove only the four tabled hosts; remove F/T3 repeated-host blocks)",
                "The static-host-table control (table on localhost/example.invalid/sitemaps.invalid/test.invalid) must MEET the removals that take its hosts out of the generated population and FAIL unweakened v4."),
    mut_counter("MutCounterT2", "the T2 scoped restructure (revert T2 to one write_single file of 20,000 values with no fold pair; keep the rest of v4)",
                "The case-fold memo and 32-prefix controls must MEET the reverted counter and FAIL unweakened v4, proving the T2 restructure is load-bearing."),
    # --- build mutants ---
    mut_build("MutBuildPort", "port parsing (the digit loop, the 5-digit boundary, the 65535/65536/100000 range edges, leading-zero handling)"),
    mut_build("MutBuildScope", "scope/directory comparison (first-segment vs first-slash dir, case-sensitivity of the dir compare, trailing-slash forms)"),
    mut_build("MutBuildPct", "percent-triplet validation (hex case, short/long percent forms, triplet at value end)"),
    mut_build("MutBuildScheme", "scheme handling (odd case, odd schemes, schemeless values)"),
    mut_build("MutBuildHost", "host handling (reg-name case, userinfo, empty host, host with trailing dot)"),
    mut_build("MutBuildQF", "query/fragment validation (defects after ?, after #, delimiters in path)"),
    mut_build("MutBuildIP", "IP-literal handling (zone ids, IPvFuture, bracket defects, port after bracket)"),
    mut_build("MutBuildMisc", "entry/exit handling (manifest faults, missing files, output formatting lines)"),
    # --- fresh controls of the frozen classes ---
    ctl("CtlPortLen", "port-length gates — skip or abbreviate the URL check when the authority carries a port of >=6 digits, or key a cache on the port length",
        "Variants: (1) skip `_parse_url` entirely when `value.count(':')` after the scheme is followed by >=6 digits; (2) answer any >=6-digit port value from a static 'clean' table; (3) truncate the port read to 5 digits like the round-42 M8 control but keep everything else."),
    ctl("CtlPortValue", "port-value caches — memoize on the port digits only, or skip the port range check",
        "Variants: (1) dict keyed on the exact port substring; (2) port range check removed (any digits accepted); (3) port check only when the port is exactly 5 digits."),
    ctl("CtlCaseMemo", "case-fold memo variants — cache keyed on a folded form of the value or a component",
        "Variants: (1) fold lower-to-upper instead of upper-to-lower; (2) fold only the path before caching; (3) memoize on the lowercased HOST while parsing the path fresh."),
    ctl("CtlPrefixCache", "shared-prefix caches at 16, 24 and 48 code points, with and without tail revalidation",
        "Variants: (1) cache keyed on value[:16] without tail check; (2) value[:24]; (3) value[:48] with a tail check that only re-scans the last 8 characters."),
    ctl("CtlHostTable", "expanded static host tables — answer without the URI check for a table of common hosts",
        "Variants: (1) the four round-42 tabled hosts plus the whole COMMON_HOSTS basket from the counter; (2) wildcard *.invalid and *.example; (3) table hit answers 'clean' only when the path has no percent sign."),
    ctl("CtlHeadTail", "head/tail judging — judge only a window of values with long ports or long shared prefixes",
        "Variants: (1) judge only the first 64 and last 256 code points of any value whose authority has a >=6-digit port; (2) judge only the first 32 code points of any value sharing its first 24 with a previous value; (3) skip the URI check for values longer than 100,000 code points."),
    ctl("CtlRepeat", "repetition classes outside the frozen list — value-length memo, dir-depth cache, defect-position cache",
        "Variants: (1) memo keyed on exact value length; (2) cache keyed on the depth of the loc's directory; (3) cache keyed on the byte offset of the first '%' — answer values whose first-% offset repeats from the cache."),
    item("CtlTiming", "executor", OP,
         "Attacks: counter v4's measurement channel (the v3 runner carried into v4).",
         "- Build >=2 tools that try to lower measured CPU without doing the work: (1) write a forged line to the timing file through a /proc/<runner>/fd route or an inherited descriptor; (2) fork a helper that does the parsing while the main process sleeps in an unwaited child; (3) cache timing-shape outputs across reps keyed on the file size. Score each with the counter (no --seed).",
         CTL_ACC),
    # --- reviewers ---
    item("ReviewCounterDiff", "reviewer", OP,
         "The v4 transform: {W}/build_v4.py applied to the round-42 v3 counter.",
         "- Read build_v4.py and diff its output against the round-42 counter ({L}/.ufo/waves/round-42/c42_count_v3.py) mentally per replacement anchor: does every claimed change appear exactly once? Are runs A-E and the sandbox byte-behaviour unchanged? Is run F's value population XML-legal for the `loc` field (xml_text applied) and well-formed for the round-41 parser? List any generator bug that could make a correct tool fail or a wrong tool pass.",
         "First line CONFORMANT or DEFECT: <what>. Findings with path:line; each checked invariant holds/overstated/wrong."),
    item("ReviewCounterDet", "reviewer", OP,
         "Counter v4 determinism and receipt soundness.",
         "- Re-run `python3 -B {COUNTER} --root {L} --revision {BUILD} --seed 151761938919664 --out {sb}/rerun.json` and diff against {W}/verification/freeze/build-1.json (seed is recorded there): the receipts must be byte-identical. Re-run the ref41-base seed 43001 receipt the same way. Report any nondeterminism with the differing keys.",
         "First line CONFORMANT or DEFECT: <what>. Exact commands, exits, diff summary."),
    item("ReviewLayoutF", "reviewer", OP,
         "layout_f scope semantics vs the round-41 tool's actual scope rule.",
         "- Read the round-41 tool's scope/dir comparison in the URL-check code (`git -C {L} show 1ef7a0e9:scripts/sitemap_audit.py`, the _directory_of / out_of_scope logic) and {COUNTER}'s layout_f/segment_smu: for a fold pair (a with upper-cased first-segment letter, b all-lower), does the round-41 tool really flag b out_of_scope under a's segment-cased sitemapUrl? Run a two-value witness through both the round-41 tool and the v1_casefold control ({W}/controls-r42/v1_casefold.py) in {sb}/ to demonstrate the flip empirically.",
         "First line CONFORMANT or DEFECT: <what>. The witness run outputs (exit + stdout) for both tools."),
    item("ReviewFreezeReceipts", "reviewer", OP,
         "The nine freeze receipts under {W}/verification/freeze/.",
         "- Re-derive each receipt's headline (met, equalRuns, ratios, seed recorded, tool sha256, counter sha256 = {COUNTER_SHA}, predicate byte-equal to the PREDICATE in {COUNTER} and to the SCORECARD sentence) from the committed JSON; run one fresh build scoring yourself and compare shapes. Confirm exits.txt matches the receipt mets.",
         "First line CONFORMANT or DEFECT: <what>. Per-receipt table row: file, met, your re-derivation, match."),
    item("ReviewKillRule", "reviewer", OP,
         "The frozen kill rules and control-class list in the SCORECARD round-43 section.",
         "- Attack the wording: construct (on paper or as small tools) edge cases — a tool equal to the round-41 tool on every GENERATED value but different elsewhere; a tool that meets v4 only at seeds below 2^40; a cache keyed on the check id. For each, state which kill rule answers it and whether the rule's text covers it without the L1's judgment.",
         "First line CONFORMANT or DEFECT: <what>. Per edge case: which rule, covered/not covered, quote."),
    item("ReviewC2A", "reviewer", FR,
         "C2's annotation repair: the two annotation rows and the pins entries.",
         "- Re-run `node {L}/scripts/freshness-sweep.mjs --section=paths` and confirm exit 0. Verify each annotation row sits within +/-2 lines of the citation it annotates (corpus/lessons/round-29.md:104 vs :102, corpus/lessons/round-33.md:45 vs :43), names the exact missing target, the dated event and the surviving lane copy, and says the citation is a historical record, not executable. Verify both tokens are in corpus/knowledge/freshness-pins.json pathsMissSet (65 entries) and the pins JSON parses.",
         "First line CONFORMANT or DEFECT: <what>. Per check: command, exit, holds/overstated/wrong."),
    item("ReviewC2B", "reviewer", FR,
         "C2's movement census completeness.",
         "- Sweep the whole lane and the fleet root for line pointers into corpus/lessons/round-29.md and round-33.md (`grep -rEn 'round-(29|33)\\.md:[0-9]+' {L} /home/vgpnk/Projects/shokunin --include='*.md' --include='*.txt'` style, excluding .git): for every pointer, check whether the insertion (one row after line 102 / after line 43) shifted its target and whether a correction exists (the two dated EOF notes). Any missed pointer is a defect.",
         "First line CONFORMANT or DEFECT: <what>. Full pointer census table: pointer, target, shifted, correction present."),
    item("ReviewSourcesRows", "reviewer", FR,
         "SOURCES rows S129 and S130 ({L}/corpus/SOURCES.md) and their Gate rows.",
         "- Verify: 11 cells each, no in-cell pipe, kind own-work, tier A with a scoped (not global) scope cell, status mined with existing used-by paths, opened 2026-10-23, and the located quotes verbatim in the sibling files (/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md and /home/vgpnk/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md) at the named anchors. Run the census malformed-row and enum checks on the committed file.",
         "First line CONFORMANT or DEFECT: <what>. Per check: command, exit, holds/overstated/wrong."),
    item("ReviewHarmUnchanged", "reviewer", OP,
         "The claim 'v4 changes only generated inputs, not the tool' and H4's qualification.",
         "- Verify by read-only git diff that scripts/sitemap_audit.py at {BUILD} is byte-unchanged since the round-42 build commit (git log/diff over the tool path), that the round-42 harm receipts (selftest 235, real run fd985a41, H4 in-class zeros, Python 3.10 selftest) still describe the same tool bytes, and that the SCORECARD round-43 section carries the H4 in-class-only qualification text.",
         "First line CONFORMANT or DEFECT: <what>. Commands, exits, digests."),
    item("ReviewQualityV", "reviewer", FR,
         "registry_count_check.py: is the able-to-fail checker itself sound?",
         "- Probe it as the round-42 QUALITY (v) reviewer probed harm_rule_check.py: (1) a claims file whose counts match at the wrong revisions; (2) rows with stray leading spaces or an extra trailing empty cell; (3) a registry row with a status typo. Each probe must be caught (exit 1 with the right mismatch) or reported as a bypass. Also verify the red/green receipts (exit 1 on r42 claims, exit 0 on r43) reproduce.",
         "First line CONFORMANT or DEFECT: <what>. Per probe: command, exit, caught/bypassed."),
    item("ReviewLesson43", "reviewer", FR,
         "corpus/lessons/round-43.md against the CORPUS.md contract.",
         "- Check: ## Gate with per-row URL/access date/<=25-word located quotes for S129/S130; ## Mistakes rows 7-8 each with class/evidence/captured-by/fix; every evidence pointer resolves; the fix claims ('able to fail') are backed by committed receipts with exits; the round-42 closure disposition table matches the closure file's seven items (1-6 worked here, 5 is operator-owned).",
         "First line CONFORMANT or DEFECT: <what>. Per item: holds/overstated/wrong with pointer."),
    # --- critics ---
    item("CriticFreezeOrder", "critic", BOTH,
         "The freeze-order claim: everything scored before any seat scores, per routed repair 2.",
         "- Establish the chronology from committed data only: the freeze commit {REV}'s committer time; the mtime and content of every file under {W}/verification/ (do any receipts or logs predate the freeze?); the absence of any round-43 seat artifact before the dispatch log line. Any counterexample (a seat receipt, wave file or score predating {REV}) is DEFECT with the exact artifact.",
         "First line CONFORMANT or DEFECT: <what>. Chronology table: artifact, mtime, before/after {REV}."),
    item("CriticC1Sizing", "critic", OP,
         "C1's claim sizing per the fleet rules (do-nothing control, kill rule frozen, no post-data rule change).",
         "- Verify: the do-nothing control (round-41 tool at base) was scored with the frozen counter BEFORE the build's receipts and both are committed (receipts ref41-base and build-1..3 with recorded seeds); the predicate sentence is byte-identical in the SCORECARD section, the counter and every receipt; the kill rule and control classes are the same text before and after any seat could score; the target (met x3) is one a do-nothing cannot reach (show the do-nothing receipt fails).",
         "First line CONFORMANT or DEFECT: <what>. Per sizing rule: holds/overstated/wrong with the receipt digests."),
    item("CriticC2Sizing", "critic", FR,
         "C2's claim sizing and honesty.",
         "- Verify: the before state is a committed receipt (sweep-before.txt, exit 1, the exact verdict line), the after state is committed (sweep-after.txt, exit 0), the claim's counting command is one command, and a do-nothing round (no annotations, no pins entries) could not reach the after state — name the exact gate line that would stay red. Check the claim does not assert more than the gate shows (e.g. it must not claim the whole sweep is green — only --section=paths).",
         "First line CONFORMANT or DEFECT: <what>. Per check: holds/overstated/wrong."),
    item("CriticFrontier", "critic", FR,
         "The frontier step's conformance: census, sourced claim, mined mistake.",
         "- Verify: census exit 0 committed (verification/freeze/census-after-r43.txt) and registry row counts as stated (128 -> 130 at {REV}); at least one round claim cites a row opened this round (C1 cites S129 — check the SCORECARD text); the mined mistake (lesson Mistake 7) has a fix shown able to fail with committed receipts; S129/S130 are genuinely 'opened this round' (no prior round cites them).",
         "First line CONFORMANT or DEFECT: <what>. Per item: holds/overstated/wrong."),
    # --- sentinel / revengers / labrats ---
    item("SentinelSandbox", "sentinel", OP,
         "Counter v4's sandbox and timing channel (carried from v3: non-dumpable runner, append timing file, PATH-only env).",
         "- Attempt: (1) reopen the runner's timing descriptor via /proc/<pid>/fd from a tool under the counter's own sandbox; (2) forge a timing line by writing to the timing file path guessed from /proc; (3) leak the case directory path via error messages or fd inheritance. Each attempt is a small tool you score with the counter (no --seed); a forged CPU must either fail equality or record honest CPU.",
         "First line SECURE or DEFECT: <what>. Per attempt: tool sha256, receipt outcome, what the timing line recorded."),
    item("RevengerMath", "revenger", FR,
         "The registry-arithmetic correction, re-derived independently.",
         "- Without reading the L1's checker output, re-derive rows/mined/queued/rejected at 1ef7a0e9 and 5949e66ffe from committed bytes with the CORPUS.md census commands; compare to the r43 correction entry (119/128/+7/+2/0) and to the r42 report's claim (128/131/+1). Also re-run the census validator and record its exit.",
         "First line CONFIRMED or DEFECT: <what>. Your derived table, both derivations side by side."),
    item("RevengerV3Receipts", "revenger", OP,
         "The round-42 kill-rule evidence: counter v3 receipts on the four controls.",
         "- Re-run the committed round-42 counter v3 ({L}/.ufo/waves/round-42/c42_count_v3.py, sha256 ce2d5a0c...) against each tool in {W}/controls-r42/ (no --seed): all four must be met (10/10 or 9/10 equal, ratios <= 2.0) — reproducing the round-42 wave-2 L1 receipts (L1-*.json). Confirm the four committed tool sha256s equal the round-42 w2 report values (MutBuildAuthority.md / CtlFreshCache.md).",
         "First line CONFIRMED or DEFECT: <what>. Per tool: sha256, v3 receipt met/equalRuns/ratios, the r42 L1 receipt's values."),
    item("RevengerFreeze", "revenger", OP,
         "Freeze byte-completeness at {REV}.",
         "- Verify: {COUNTER} sha256 equals {COUNTER_SHA}; build/receipt digests (tool 914ebdee at {BUILD}, ref41 50287ac6, base40 4de35f8c pins in the counter); the SCORECARD round-43 section's PREDICATE sentence equals the counter's PREDICATE (python string ==); the controls-r42 SHA256SUMS verify; the freeze commit touches only the paths its message names (git show --name-status).",
         "First line CONFIRMED or DEFECT: <what>. Per digest: expected, observed, match."),
    item("ScoutCacheScope", "scout", OP,
         "Hypothesis: the fold pair defeats v1_casefold only because both members share one manifest file.",
         "- Test: build a v4 variant in {sb}/ whose layout_f writes each fold-pair member to a SEPARATE file (two checks, two segment-cased sitemapUrls) and score v1_casefold against it. If v1_casefold meets the split variant, the single-file layout is load-bearing — report which run (F or T2) carried the kill in the unweakened receipts (receipt runs.unequal lists them).",
         "First line SUPPORTED or REFUTED: <which>. Both receipts' unequal-run lists."),
    item("ScoutPortMath", "scout", OP,
         "Hypothesis: out-of-range ports are the only M8-discriminating values in F.",
         "- Build a v4 variant in {sb}/ with padded in-range ports only (long_port out_of_range forced False) and score M8-port-five-digits against it. Then revert just the F port values to out-of-range (T1/T3/T5 ports padded only) and score again. Report which population carries the kill.",
         "First line SUPPORTED or REFUTED: <which>. Both receipts' unequal-run lists."),
    # --- scribes / connector / simplifier / distiller ---
    item("ScribeReportInputs", "scribe", BOTH,
         "Draft inputs for the round-43 report (the L1 writes the report itself).",
         "- From committed bytes only, produce under {sb}/: (1) sources-frontier.txt — registry rows at 61046fc vs {REV} (count commands + outputs), rows added by tier, touched old->new (none expected), census exits; (2) measurements.txt — the C1/C2 before/after blocks with counting commands and receipt paths exactly as committed; (3) waves.txt — this wave's seat list with roles from {W}/w1-spec.json. Do not invent numbers: every count carries its command output.",
         "First line DRAFTED. The three files' paths; any number you could not re-derive is named, not filled."),
    item("ScribeLessonSupplement", "scribe", FR,
         "Draft the lesson supplement for the wave's gate/attack findings.",
         "- Under {sb}/lesson-supplement.md: a ## Gate supplement listing any source this wave's seats opened (row, access date, <=25-word quote, decision — none expected beyond S126/S127 reopens), and a ## Mistakes digest of every mistake-class the wave found (or 'none found' with the sweep command). The L1 will adapt; your draft must cite evidence paths only.",
         "First line DRAFTED. The supplement path; candidates admitted/rejected with reasons."),
    item("ConnectorOverlap", "connector", BOTH,
         "Sibling-overlap census for the round-43 instruments and rows.",
         "- Scan sibling lanes (/home/vgpnk/Projects/shokunin/*-shokunin) for: (1) counters or verification fixtures with the same claim shape as {COUNTER} (grep for c4*_count*, count-c1.py, registry_count_check); (2) registry rows quoting the same source URLs as S129/S130; (3) any lane already holding Mistake-5-style classes (long-port / repetition-class generators). Report overlap with paths; novel ground is as valuable as overlap.",
         "First line CONFORMANT or DEFECT: <what>. Overlap table: lane, artifact, relation to kake r43."),
    item("SimplifierCounter", "simplifier", OP,
         "Is every v4 block load-bearing? Cross-check with the MutCounter* coverage proofs.",
         "- Read the five MutCounter* reports (wait — run after them: their reports land as {L}/.ufo/waves/round-43/w1/MutCounter*.md; if absent when you run, fall back to running the named weakenings yourself, <=2). Flag any v4 generator block that no weakening experiment covers, or any weakening that kills discrimination without a corresponding block (dead code or missing class).",
         "First line LEAN or DEFECT: <what>. Per v4 block: covering experiment, load-bearing yes/no."),
    item("ScribeFindings", "scribe", BOTH,
         "Dedupe the wave's findings into the C1/C2 verdict input.",
         "- Read every seat report in {L}/.ufo/waves/round-43/w1/*.md that exists when you run (skip your own): group findings by the claim they attack (C1 counter, C1 build, C2, freeze, frontier), drop duplicates, and emit {sb}/verdict-input.md — one table per claim: finding, seat, severity (kills claim / bounds it / cosmetic), evidence pointer. Seats that found nothing still get a row ('no defect found').",
         "First line DONE. The verdict-input path; seats covered vs total."),
    # --- executors: reproductions and gates ---
    item("ExecRerunBuild", "executor", OP,
         "Reproduce the C1 build scoring with fresh seeds.",
         "- Run `python3 -B {COUNTER} --root {L} --revision {BUILD} --out {sb}/build-rerun-<n>.json` three times (no --seed). All three must be met 11/11 with ratios <= 2.0. Record seeds and compare toolSha256/counterSha256 to {W}/verification/freeze/build-1.json.",
         "First line REPRODUCED or DEFECT: <what>. Three receipts' seeds, met, ratios."),
    item("ExecRerunControls", "executor", OP,
         "Reproduce the four r42-control red receipts under v4.",
         "- Score each tool in {W}/controls-r42/ (the four r42 controls; skip junk_constant) with the counter (no --seed), twice each: all eight receipts must be not met. Record equalRuns and the unequal runs per receipt; compare to the freeze receipts' unequal-run lists.",
         "First line REPRODUCED or DEFECT: <what>. Eight receipts' met/equalRuns/unequal."),
    item("ExecCensus", "executor", FR,
         "The registry census at both round-43 revisions.",
         "- Run /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake (record exit) and the CORPUS.md manual census commands over `git show {REV}:corpus/SOURCES.md` (rows, malformed, tier histogram, status histogram, duplicate ids, enum violations, mined used-by existence). Save outputs under {sb}/.",
         "First line CONFORMANT or DEFECT: <what>. Exit codes and histograms."),
    item("ExecSweepFull", "executor", FR,
         "The FULL freshness sweep (all sections), not just paths.",
         "- Run `node {L}/scripts/freshness-sweep.mjs` (no --section) and record exit + verdict; report any section other than paths that is red, and compare the paths verdict to {W}/verification/freeze/sweep-after.txt. C2 claims only --section=paths — anything else red bounds the round's freshness claim and must be reported, not fixed.",
         "First line CONFORMANT or DEFECT: <what>. Per-section exits and verdicts."),
    item("ScoutReopen", "scout", FR,
         "Freshness re-open of the newest external source rows S126/S127.",
         "- GET https://docs.python.org/3/library/re.html and https://www.rfc-editor.org/rfc/rfc9844.txt (GET only): record HTTP status, byte count, sha256; locate each row's quoted sentence in the fetched bytes; compare to the round-42 retentions ({L}/.ufo/waves/round-42/sources/, SHA256SUMS). churn-only differences are named as such.",
         "First line FRESH or CHURN or DEFECT: <what>. Per source: status, sha256, quote located yes/no, retention relation."),
    item("ScoutMissingFiles", "scout", FR,
         "The two C2 tokens: absence and byte-exact lane copies.",
         "- `test -e` both fleet paths (must be absent); `cmp` the lane copies (.ufo/waves/round-29/w2/FieldsAndCounts.md, .ufo/waves/round-33/w2/ScoutPinsFlagAccuracy.md) against nothing — instead record their sha256 and byte sizes, and grep the fleet root for any other kake-round-N wave file present at /home/vgpnk/Projects/shokunin/.ufo/waves/ (misroot census for the report).",
         "First line CONFIRMED or DEFECT: <what>. Per path: absent/present, lane-copy sha256; misroot census result."),
    item("ScoutChronology", "scout", OP,
         "The round-43 dispatch log shape (routed repair 4: settle line required).",
         "- Read {W}/w1-dispatch-log.txt: confirm it carries the dispatch line with the wave-slot grant (lane, wave, seats, live, cap) AND a settle line (settled, dead, refused counts) — if the settle line is absent (the log is written before dispatch settles), report that the L1 must append it at settle time, quoting the w1 log format requirement from the round-42 closure routed repair 4.",
         "First line CONFORMANT or PENDING-SETTLE. The log's lines verbatim."),
    # --- added seats (band fill, all load-bearing) ---
    mut_build("MutBuildZone", "IP-literal and zone handling (zone ids after %25 and bare %, IPvFuture bodies, bracketed port, ::/::1 forms)"),
    mut_build("MutBuildLong", "long-value edges (the 2,047/2,048 boundary, the last-64 defect window, percent at the value end, non-ASCII in long bodies)"),
    mut_build("MutBuildManifest", "manifest and file faults (missing file, malformed JSON, duplicate check ids, file outside the manifest)"),
    mut_build("MutBuildOutput", "output and exit formatting (finding line order, duplicate findings, exit code on mixed clean/failed checks)"),
    ctl("CtlShapeKeyed", "shape-keyed fast paths (v3's caught class, revived against v4)",
        "Variants: (1) judge only the first 64 and last 256 code points of any value in a file with >= 20,000 entries; (2) skip the URI check when the manifest has exactly 48 checks; (3) answer any value in a file whose total bytes exceed 1 MB from a head/tail scan."),
    ctl("CtlSeedKeyed", "seed-, id- and name-keyed tools",
        "Variants: (1) a tool that special-cases check ids of the exact token shape the counter generates (tok lengths 6-12 alnum); (2) a tool keyed on the manifest file name pattern (%x.json); (3) a tool that reads the case directory listing and short-circuits when it sees the round-41 reference files absent."),
    item("ReviewSpecFidelity", "reviewer", BOTH,
         "This wave's own spec against the committed bytes it cites.",
         "- Check {W}/w1-spec.json item by item: every path it names exists at {REV} (counter, receipts, controls, pins, lessons); every digest it states matches the committed bytes; every role is in the taxonomy; no item asks a seat to write outside its sandbox. A spec that misdescribes the committed state is a DEFECT (the wave would attack a fiction).",
         "First line CONFORMANT or DEFECT: <what>. Per item sample (>=10): path/digest exists, match."),
    item("ReviewReceiptSchema", "reviewer", OP,
         "Receipt schema soundness across the committed freeze receipts.",
         "- Every {W}/verification/freeze/*.json must carry: predicate (byte-equal to the counter's), counterSha256 ({COUNTER_SHA}), ref41/base40 pin digests, toolSha256, seed, runs A-F + T1-T5 each with equal and (for T) ratiosExact, equalRuns '11/11' style. Write a small reader in {sb}/ and check all nine; a malformed receipt is a DEFECT.",
         "First line CONFORMANT or DEFECT: <what>. Per-receipt: missing keys, mismatched digests."),
    item("ScoutRegistryUsedBy", "scout", FR,
         "Every mined row's used-by paths exist at {REV}.",
         "- Extract all mined rows' used-by cells from {L}/corpus/SOURCES.md at {REV} (git show {REV}:corpus/SOURCES.md) and test each path's existence in the {REV} tree (git cat-file -e <rev>:<path>). List any missing path (a census W-level finding is acceptable; a missing one is not).",
         "First line CONFORMANT or DEFECT: <what>. Rows checked, missing list."),
    item("ScoutFleetRootWide", "scout", FR,
         "Fleet-root misroot census beyond the two C2 tokens.",
         "- `git -C /home/vgpnk/Projects/shokunin status --porcelain` plus a listing of /home/vgpnk/Projects/shokunin/.ufo/waves/: name every fleet-root path matching kake round citations that does NOT exist in the lane (cross-check against {L}/.ufo/waves/). Any kake-cited fleet-root file absent from the lane is a misroot debt for the report.",
         "First line CONFORMANT or DEFECT: <what>. Census table: path, lane-copy exists, cited where."),
    item("CriticReportContract", "critic", BOTH,
         "The round-43 report contract, made checkable before the L1 writes the report.",
         "- From the committed round prompt (/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-43.md) and PROTOCOL.md, derive the exact checklist the L1's report at /home/vgpnk/Projects/shokunin/.ufo/reports/round-43/kake.md must satisfy (sections in order, evidence pointers, SHONEN lines, sources & frontier, trend verdicts, per-source T2 numbers, settle line, Stale-lane, tool installs). Emit it under {sb}/report-checklist.md so the L1 and the closure can grade the filed report against it.",
         "First line CONFORMANT or DEFECT: <what>. The checklist path; any contract item you could not derive is named."),
    item("RevengerCounterLineage", "revenger", OP,
         "Counter lineage and freeze-provenance re-check (the round-42 defect class).",
         "- Verify the round-43 freeze does not repeat the round-42 provenance defect: {COUNTER} has exactly one committed version, first committed AT {REV} (git log --follow --format on the counter path); no receipt under {W}/verification/ references a counter sha other than {COUNTER_SHA}; the freeze receipts' mtime order matches counter-then-receipts; the wave spec (which arrived after) names only {COUNTER_SHA}.",
         "First line CONFIRMED or DEFECT: <what>. The counter path's commit history and sha audit."),
]

spec = {
    "wave": "kake-r43-w1",
    "milestone": "r43-verify",
    "maxLanes": 96,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-43/w1",
    "context": CONTEXT,
    "items": items,
}
out = HERE / "w1-spec.json"
out.write_text(json.dumps(spec, indent=1))
print("wrote", out, "seats:", len(items))
from collections import Counter
print(Counter(i["role"] for i in items))
