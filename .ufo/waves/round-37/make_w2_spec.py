#!/usr/bin/env python3
"""Write the round-37 wave-2 spec (w2-spec.json) next to this file. Usage: make_w2_spec.py REV"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = sys.argv[1]
SB = "/fast/scratch/hyaku/kake-r37w2"
W = f"{L}/.ufo/waves/round-37"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"

CONTEXT = f"""# Goal
Kake round 37, wave 2 (falsify). The L1 (KakeR37) holds the planner and integration seat; you are one leaf seat. Lane repo: {L}, measured tip {REV}. Lane axes: operability and freshness. Every item attacks one thing wave 1 or the L1 produced: re-run a counting command, re-open a source, review a tool, entry or gate, mutation-test a gate. Your job is to show it is wrong, overstated, irreproducible or harmful, with reproducible evidence; a confirmed result is also a result. Time box: finish within 30 minutes; a partial report beats none.

# What landed (read with git show {REV}:<path>)
- SCORECARD.md sections "Round 37 — declared claims" (202d625a), "control call" (4b089da6), "shortcut control follow-up" (ccc3b2b9), "measured results" ({REV}). Lesson corpus/lessons/round-37.md. LOG.md round 37.
- C1 (the only claim, operability capability): scripts/robots_audit.py (build 9dbc88bb, wave-1 ExecRobotsTool's file unedited). Frozen predicate `met: passed >= 25 of 28 sealed cases`; counter {W}/sealed_count.py; key revealed at 424aa2480bcbac1832b2aa9da49c51b78ec5092f ({W}/sealed/cases.json); L1 reference and ablation tools in {W}/sealed/reference/ and {W}/sealed/ablation-tools/; receipts {W}/verification/. Counting command: `python3 -B .ufo/waves/round-37/sealed_count.py --root <clone> --revision <rev> --key-revision 424aa248`.
- C2 withdrawn before data (snapshot control met its counter {W}/c2_mutkill.py). Non-claim repairs at 528a6d02: 5 fixtures in scripts/source_recheck_selftest.py; scripts/source_recheck.py hardening plus scripts/source_recheck_hardening_selftest.py; criteria v2 in {W}/criteria/.
- New selftest scripts/robots_audit_selftest.py (131 fixtures) and an independent implementation {W}/retained/independent/independent_robots_audit.py.
- Knowledge entry corpus/knowledge/robots-txt-rules.md; SOURCES rows S095-S097 and S011 used-by change; QUALITY round-37 criteria (a)-(i); PROVINCE and corpus/README round-37 sections.
- Controls {W}/retained/controls/ and {W}/ctl/; wave-1 reports {W}/w1/; live robots files and manifest {W}/realrun/.
- Routed defects being answered: {L}/corpus/lessons/round-36-verifier-spotcheck.md "Routed defects".

# Bounds
- The key is revealed: any seat may run the C1 counter, but only in its own sandbox clone.
- You are a leaf: no subagents, no swarm, no second judge, no admission verdict on the round.
- Your ONLY write paths are your sandbox {SB}/<YourName>/ and your report file. Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any lane file other than your report. Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git is fine. Never run any jj command at /home/vgpnk/Projects/shokunin.
- Code that writes files or Git state runs only in your sandbox: `git clone -q {L} {SB}/<YourName>/clone && git -C {SB}/<YourName>/clone checkout -q {REV}`; export TMPDIR={SB}/<YourName>/tmp. Unset GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE first. Cap every run with `timeout` (at most 900 s), at most 8 parallel processes; kill any process tree you started before returning. Do not read /fast/scratch/hyaku/kake-r37/ (the L1's private directory; everything needed is committed).
- Owned sites: no requests to the operator's web properties (ds4cc.com, app.ds4cc.com, operator *.onrender.com hosts, *.kimi.page, *.kimi.pro, veigapunk.github.io) unless your item names them. Network only when your item names a public URL; GET only; never pass a bot challenge.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>.
- Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels; record tool, version, channel, reason). pacman guard: all pacman transactions are PAUSED host-wide — use uv tool, npx or an official binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U, -R; no downgrade, no service restart.
- A provider safety or policy refusal or automatic model switch: stop and write a one-line report saying so; do not rephrase. Message only agent://KakeR37 and only for blockers; never agent://all. Plain English.

# Result
Report under 80 lines: what you attacked, exact commands with exit codes, observed outputs, evidence pointers (path:line, hash), verdict per attacked statement (holds / wrong / overstated / unverifiable). An unrun check has not passed. A partial report starts with `PARTIAL:`.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, W=W)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR = ["operability"], ["freshness"]
ITEMS = [
    item("RerunC1Sealed", "reviewer", OP,
         "Re-derive C1's measured result from committed bytes.",
         "- In a sandbox clone at {REV}, run the counting command at 9dbc88bb, 621fb528, 202d625a, 4b089da6, ccc3b2b9, 528a6d02 and 424aa248 (expect exit 2: key visible). Compare each stdout with {W}/verification/c1-keyrev-at-*.json (byte compare). Check the key's sha256 against KEY_SHA256 in the counter and against the declaration text, and that the tool at 9dbc88bb has sha256 5eb767ec…cabae and equals {L}/.ufo/waves/round-37/w1/ExecRobotsTool.md's stated hash.",
         "Per revision: passed, met, exit, byte-identical yes/no."),
    item("RerunControls", "reviewer", OP,
         "Re-score every retained C1 control and the independent implementation under the revealed key.",
         "- For each file in {W}/retained/controls/*-robots_audit.py and {W}/retained/independent/independent_robots_audit.py run `python3 -B .ufo/waves/round-37/sealed_count.py --root <clone> --tool-file <file> --key-revision 424aa248` and compare with {W}/verification/control-*.json and independent-selftest-reference.json (passed, perCase). Also check each control's sha256 matches its seat report in {W}/ctl/.",
         "Table control · committed passed · re-run passed · match."),
    item("RerunAblations", "reviewer", OP,
         "Re-score the 34 listed reference ablations and the reference itself under the revealed key; check the declaration's coverage sentence ('each of the 34 listed ablations scores at most 24 of 28 (16 to 24)').",
         "- Tools are in {W}/sealed/ablation-tools/ and {W}/sealed/reference/ref.py; receipts in {W}/verification/ablations/. Re-run each with --tool-file and the revealed key; compare passed. Check that each ablation's own bullet's four cases all fail (ablation-pre.json in {W}/sealed/reference/).",
         "Per ablation committed vs re-run; coverage sentence holds or not."),
    item("ReviewRobotsTool", "reviewer", OP,
         "Code review of scripts/robots_audit.py at 9dbc88bb against the round-37 C1 contract, sentence by sentence.",
         "- For every contract sentence ((a)-(g), usage, manifest, findings, verdict) name the implementing lines or the missing behavior. Look for any case-specific code, network, writes, subprocess or environment reads. Build at least 10 manifests in your sandbox for points where you doubt the tool and run it.",
         "Sentence → lines table; each doubt with a reproducer and verdict."),
    item("SentinelRobotsInputs", "sentinel", OP,
         "Hostile inputs against scripts/robots_audit.py at 9dbc88bb.",
         "- Try: FIFO and /dev/zero manifests and robots paths, a 64 MiB+1 manifest, a 1 GiB robots file (only 512000 bytes may be read), symlink loops and symlinks escaping the manifest dir, deep JSON nesting, 100 000 checks, pathological wildcard rules (`/*a*a*a*…` against long paths: catastrophic regex?), NUL bytes, invalid UTF-8 in robots and URLs, very long lines. Record wall time and memory (`/usr/bin/time -v`) and whether output stays one JSON report with the right exit.",
         "Each input with time, memory, exit and verdict; any hang, crash or wrong exit with reproducer."),
    item("MutRobotsTool", "mutation-tester", OP,
         "Mutation-test the landed tool against the sealed counter and the new selftest.",
         "- Make at least 30 single-point mutants of scripts/robots_audit.py at 9dbc88bb (one contract sentence each). Score each with the sealed counter (revealed key) and with `python3 -B scripts/robots_audit_selftest.py --tool <mutant>`. Report survivors of each and of both.",
         "Mutant table: change · sealed passed · selftest passed · survived which."),
    item("MutRefPassVsSelftest", "mutation-tester", OP,
         "Do the 42 MutRefPass mutants of the L1 reference (retained in {W}/retained/MutRefPass/mutants/) survive the new robots selftest?",
         "- Run `python3 -B scripts/robots_audit_selftest.py --tool <mutant>` for each (also run it on {W}/sealed/reference/ref.py itself: the L1 reports 130/131, failing c10). For each mutant: killed by the selftest or not; for the 28 that met the sealed target, how many the selftest kills. Mind that the reference's own c10 failure is shared by all mutants.",
         "Per mutant: sealed passed (from {W}/ctl/MutRefPass.md) · selftest result · killed."),
    item("DiffToolVsIndependent", "mutation-tester", OP,
         "Differential test: landed tool vs the independent implementation vs the L1 reference on generated inputs.",
         "- Write a generator of random robots files (groups, comments, BOM, CR/LF mixes, wildcards, `$`, percent escapes, non-ASCII, empty rules, other keys) and manifests (statuses incl. 4xx/5xx edges, user agents, URLs with queries/fragments/empty paths). Run all three on at least 2000 checks; report every disagreement with a minimal reproducer and which contract sentence decides it.",
         "Disagreement list with reproducers and the contract-correct answer argued from the text."),
    item("ReviewRobotsSelftest", "reviewer", OP,
         "Review scripts/robots_audit_selftest.py: does each fixture's expectation follow the contract sentence it quotes?",
         "- Sample at least 40 of the 131 fixtures across all bullets; for each, derive the expected result from the contract text yourself and compare. Check the judge (exit, version, verdict, findings projection, checksEvaluated, write detection), the FIFO fixtures' timing, and the ≥6-per-bullet gate. Run it on the landed tool and on {W}/retained/independent/toy_robotparser.py.",
         "Per sampled fixture agree/disagree with reasoning; judge review; run results."),
    item("ReviewHardening", "reviewer", ["operability", "freshness"],
         "Review the source_recheck hardening (528a6d02 vs 79d3c780's parent: `git diff 621fb528 528a6d02 -- scripts/source_recheck.py scripts/source_recheck_hardening_selftest.py`) and its contract amendment sentence (lesson round-37 'Non-claim routed repairs').",
         "- Does the tag-aware raw-element scan change any behavior the round-36 contract fixes, outside the attribute case? Run the round-36 sealed counter (`python3 -B .ufo/waves/round-36/sealed_count.py --root <clone> --revision 528a6d02 --key-revision fd1fb723`), the round-36 selftest and the hardening selftest at 528a6d02. Is the g32 strace fixture robust without strace?",
         "Behavior-change list with reproducers; run results; amendment wording verdict."),
    item("SentinelHardening", "sentinel", ["operability", "freshness"],
         "Hostile inputs against scripts/source_recheck.py at 528a6d02 (after hardening).",
         "- FIFO/device/1 GiB/`/dev/zero` manifests and body files, body symlink races, quadratic HTML (many unclosed `<script`, attributes with quotes and `>`), deep nesting. Record time, memory, exit, JSON shape.",
         "Each input with time/memory/exit; any hang or crash with reproducer; body-size cap status."),
    item("RerunC2Evidence", "reviewer", OP,
         "Re-derive the non-claim C2 evidence and the C2 control receipts.",
         "- Run `python3 -B .ufo/waves/round-37/c2_mutkill.py --root <clone> --revision 528a6d02 --jobs 8` and at 621fb528; compare with {W}/verification/c2-evidence-at-528a6d02.json and c2-at-621fb528.json. Rebuild the snapshot control from {W}/retained/controls/c2/selftest-snapshot.py (commit it as scripts/source_recheck_selftest.py in your clone) and re-score; compare with c2-snapshot.json.",
         "Per run: killed, valid fixtures, match yes/no."),
    item("ReviewC2RepairFixtures", "reviewer", OP,
         "Are the five fixtures added to scripts/source_recheck_selftest.py at 528a6d02 grounded in the round-36 contract text (not in E1's behavior)?",
         "- `git diff 621fb528 528a6d02 -- scripts/source_recheck_selftest.py`. For each fixture derive the expectation from the round-36 contract text (SCORECARD 'Round 36 — declared claims') and compare; compare with {W}/w1/RevengerSurvivors.md's independent distinguishing inputs.",
         "Per fixture: contract sentence, derived expectation, agree/disagree."),
    item("ReviewCriteriaV2", "reviewer", OP,
         "Attack the three criterion checks in {W}/criteria/ (control_tree_check.py v2, polarity_check.py, bare_id_check.py) and junk_control_receipt_check.py.",
         "- For each, construct a false pass (bad input it accepts) and a false fail (good input it rejects); re-run its receipts in {W}/criteria/receipts/.",
         "Per check: receipts reproduced, false pass/fail found with input."),
    item("ReviewKnowledgeEntry", "reviewer", OP,
         "Every sentence of corpus/knowledge/robots-txt-rules.md against its cited source.",
         "- For each cited sentence, locate the passage in {W}/sources/S011.txt, S095.txt or S096.txt (or S096 robots.cc at github if the sentence cites code) and judge supported / overstated / unsupported. Check each 'Lane reading' marker matches the contract. Check the metadata header.",
         "Sentence table with locations and verdicts."),
    item("ReopenGateS011", "scout", FR,
         "Re-open the S011 Gate line in corpus/lessons/round-37.md live: https://www.rfc-editor.org/rfc/rfc9309.html",
         "- Verify the quote, section, access claims and the S011 row's used-by change; note any drift since 02:50Z.",
         "Quote found yes/no with section; row change verified."),
    item("ReopenGateS095", "scout", FR,
         "Re-open the S095 Gate line live: https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt (and its redirect target).",
         "- Verify quote, section, redirect, tier/kind and the row cells in corpus/SOURCES.md.",
         "Quote, redirect and row verdicts."),
    item("ReopenGateS096", "scout", FR,
         "Re-open the S096 Gate line live: https://github.com/google/robotstxt",
         "- Verify quote, section and row; check that the knowledge entry's S096 statements (normalization left to the caller, no unreserved decoding) hold in README and robots.cc at the current master commit.",
         "Quote and claims verdicts with file:line."),
    item("ReopenGateS097", "scout", FR,
         "Re-open the S097 reject live: https://www.robotstxt.org/orig.html",
         "- Is the reject reason (superseded; no Allow; substring user-agent; one `*` record) supported by located text? Is the flip well-formed per /home/vgpnk/Projects/shokunin/CORPUS.md SOURCES rules?",
         "Reject verdict with located quotes; flip verdict."),
    item("ReviewSourcesRows", "reviewer", FR,
         "Registry conformance of the round-37 SOURCES changes.",
         "- `git diff 621fb528 {REV} -- corpus/SOURCES.md`: column shape, tiers, scope wording, used-by paths are knowledge entries or lessons (CORPUS.md contract v1), every change logged old→new in the lesson Gate. Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` (read-only) and compare with {W}/census-before.txt.",
         "Per row conformance; census output and exit."),
    item("ReviewLessonNumbers", "reviewer", OP,
         "Every number and hash in corpus/lessons/round-37.md and SCORECARD 'Round 37 — measured results' against the committed receipts.",
         "- For each figure, find the receipt (path) and check it; every cited hash resolves with `git cat-file -e <h>^{{commit}}` or names a bundle.",
         "Figure table: claim, receipt, holds/wrong."),
    item("ReviewMistakesTable", "reviewer", OP,
         "The round-37 lesson `## Mistakes` rows: is each fix shown able to fail?",
         "- Re-run `{W}/criteria/junk_control_receipt_check.py` at 1a16b8e3 and at 4b089da6 (commands in {W}/w1/ScribeMistakeMine.md). Judge rows 2 and 3 (captured-by, fix, 'no check yet').",
         "Per row: reproducible red/green or not; verdict."),
    item("ReviewTimeline", "reviewer", OP,
         "Freeze order: was every C1 rule (predicate, counter, key, target) fixed before any build seat existed and before any build was measured?",
         "- From `git log --format='%H %cI %s' 621fb528..{REV}`, {W}/ctl-dispatched-at.txt, {W}/w1-dispatched-at.txt, and the receipts' contents, build the timeline: declaration, control receipts, C2 withdrawal, shortcut follow-up receipt, wave-1 dispatch, build landing, first C1 measurement, reveal. `git diff 202d625a {REV} -- .ufo/waves/round-37/sealed_count.py` must be empty. Note the shortcut follow-up receipt landed after wave-1 dispatch: does that matter?",
         "Timeline table with hashes and times; any ordering defect."),
    item("ReviewShortcutDisposition", "reviewer", OP,
         "Attack the L1's disposition that the shortcut follow-up (stdlib parser + six patches, 28 of 28) does not skip the claimed work (SCORECARD ccc3b2b9 section).",
         "- Read {W}/ctl/CtlC1NoReader-shortcut.md and the tool {W}/retained/controls/CtlC1Shortcut-followup-robots_audit.py. Argue both sides: is it a do-nothing or shortcut in the round rule's sense (\"a control that skips the claimed work\"), or an implementation? Does the claim's capability wording overstate given it? Measure: the new selftest on it (the L1 reports 126/131).",
         "Verdict with reasons and the selftest run."),
    item("ReviewWithdrawalAndWording", "reviewer", OP,
         "Claim-sizing and withdrawal review: is C2's withdrawal before data honest and complete in SCORECARD, lesson and LOG? Does the C1 declaration and capability row use any universal clause the counter does not enumerate?",
         "- Quote each sentence you judge; check the predicate string is identical in SCORECARD, sealed_count.py PREDICATE and every receipt's predicate field.",
         "Per sentence verdict; predicate-identity check."),
    item("ReviewHarm", "reviewer", ["operability", "freshness"],
         "No axis harmed: `git diff --numstat 621fb528 {REV}` (deletions?), SCORECARD axis rows unchanged, and every lane selftest still passes at {REV}.",
         "- In a sandbox clone at {REV} run every scripts/*selftest*.py (and canonical_audit.py --selftest if present) with timeouts; compare with their round-36 results. List any file with deletions and why.",
         "Selftest table with exits; deletion list; harm verdict."),
    item("ReviewContainment", "reviewer", OP,
         "Containment: did any round-37 seat write outside its sandbox and report? Fleet-root misroots?",
         "- `git -C /home/vgpnk/Projects/shokunin status --porcelain` (read-only) and look for files naming kake round 37; in the lane, compare `git ls-tree -r --name-only {REV} -- .ufo/waves/round-37/` with what the L1 says it copied; read each wave-1 report's own disclosure of out-of-bounds actions (e.g. /tmp writes, a stat of the private directory).",
         "List of every out-of-bounds action found with pointer; misroot list."),
    item("ReviewRealRun", "reviewer", ["operability", "freshness"],
         "The live robots run: are the 55 expectations in {W}/realrun/robots/manifest.json justified by the quoted lines, and does the tool's clean result mean what the lesson says?",
         "- Check 20 checks by hand against the recorded robots files; re-run `python3 -B scripts/robots_audit.py --manifest .ufo/waves/round-37/realrun/robots/manifest.json` in your clone; construct 5 extra checks on the same live files where the contract and urllib.robotparser differ and run both tools.",
         "Per check verdict; extra-check results."),
    item("ScoutRobotsRefetch", "scout", FR,
         "Freshness of the live robots set: re-fetch the 10 non-owned hosts' /robots.txt (www.rfc-editor.org, developers.google.com, github.com, docs.github.com, www.sitemaps.org, developer.mozilla.org, en.wikipedia.org, www.robotstxt.org, html.spec.whatwg.org, pages.github.com).",
         "- One GET each, 1 s apart; compare sha256 with {W}/realrun/robots/receipts.json; for any change, diff and say whether any manifest check's answer changes.",
         "Per host: same/changed, diff summary."),
    item("MutSealedCounter", "mutation-tester", OP,
         "Mutation-test the C1 counter's guards with the revealed key.",
         "- At least 10 single-point mutants of {W}/sealed_count.py (drop the runs loop's all-must-pass, compare findings by reason only, drop id randomization, drop the key-visible refusal, accept any exit, etc.). For each, find a tool (a control in {W}/retained/controls/ or a constructed one) whose score differs between the real and mutant counter, or argue equivalence.",
         "Guard table with proving inputs."),
    item("RevengerToolReadings", "revenger", OP,
         "The landed tool's 12 open-point readings (listed in {W}/w1/ExecRobotsTool.md) vs the L1 reference and the independent implementation.",
         "- For each reading, construct the distinguishing input, run all three tools ({L}/scripts/robots_audit.py at 9dbc88bb, {W}/sealed/reference/ref.py, {W}/retained/independent/independent_robots_audit.py) and say which reading the contract text supports.",
         "Per reading: three outputs and the text-supported answer."),
    item("ReviewQualityProvince", "reviewer", OP,
         "QUALITY round-37 criteria (a)-(i), PROVINCE 'Round-37 robots.txt frontier step' and corpus/README 'Coverage — round 37' against the evidence.",
         "- Each criterion: grounding path exists and says what is cited; receipts exist and reproduce (run the three criteria receipts scripts in {W}/criteria/receipts/ in a clone). PROVINCE/README sentences: any claim beyond the contract or evidence?",
         "Per criterion and sentence verdict."),
    item("ReviewRoutedClosure", "reviewer", OP,
         "Disposition of every round-36 routed defect (1-8) and the session-note routes in the round-37 lesson.",
         "- Map each to the lesson text and evidence at {REV}; mark addressed / partly / not, with the gap. Include the 18 undecided round-36 contract points and the round-36 capability-row wording limit line (routed defect 3).",
         "Table per routed item with pointer and gap."),
    item("ScoutContractAmbiguityR37", "scout", OP,
         "Undecided or doubly decided points in the round-37 C1 contract text, now that a tool, a reference and an independent implementation exist.",
         "- Read the contract; list each point with a concrete input; run the three implementations on it ({L}/scripts/robots_audit.py, {W}/sealed/reference/ref.py, {W}/retained/independent/independent_robots_audit.py) and note whether they split.",
         "Numbered list with inputs and outputs."),
]

spec = {
    "wave": "kake-r37-w2",
    "milestone": "r37-falsify",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": ".ufo/waves/round-37/w2",
    "context": CONTEXT,
    "items": ITEMS,
}
(HERE / "w2-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS), "items")
