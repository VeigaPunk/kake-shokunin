#!/usr/bin/env python3
"""Write the round-35 wave-2 (falsify) spec (w2-spec.json) next to this file."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = "7deacc4629c1d05a34fb919d8095e99efc7b712f"
SB = "/fast/scratch/hyaku/kake-r35/w2"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"
CNT = ".ufo/waves/round-35/sealed_count.py"
KREV = "4c6be2bdec5630166c4013e53c226b1119ec63cc"

CONTEXT = f"""# Goal
Kake round 35, wave 2 (falsify). The L1 (KakeR35) holds the planner and integration seat; you are one leaf seat. Lane repo: {L}. Lane axes: operability and freshness (web properties and publishing). Wave 1 built and landed the round's work; your item attacks one named piece of it. Try to show it is wrong, overstated or harmful, with reproducible evidence; a confirmed result is also a finding. Time box: finish and write your report within 25 minutes; a partial report beats none.

# Claims and landed state (lane branch master at {REV}; read SCORECARD.md sections "Round 35 — ...")
- Declaration 81d9fd74 (base 16a6b8b8). Sealed keys written by the L1 before the declaration, pinned by sha256 in {CNT}, revealed at {KREV} as {L}/.ufo/waves/round-35/sealed/c1-cases.json and c2-probes.json (now readable by you). Controls scored before any build at 318561ef; C2 counter version 2 landed at bd14096a before any build was measured (version 1 kept as sealed_count_v1.py); every control rescored (verification/control-v2-*.json).
- C1 (operability, capability repair): scripts/link_preview_audit.py repaired at b1cbbc39 (wave-1 ExecToolRepair) to contract bullets a-c in SCORECARD "Round 35 — declared claims". Counter `python3 -B {CNT} c1 --root <repo> --revision <rev> --key-revision {KREV}`: 14/24 at 16a6b8b8 and bd14096a, 24/24 at b1cbbc39 and 95abec21; target >= 22. Selftest 45/45 and round-34 matrix 28/28 at b1cbbc39.
- C2 (freshness, sourced): corpus/knowledge/security-txt-publishing.md landed unedited from wave-1 ScribeEntryDraft at 95abec21, with SOURCES rows S078-S087 and the S006 used-by change. Counter `python3 -B {CNT} c2 ...`: met false before, met true at 95abec21 (12/12 probes, 1388 words, copiedShare 0.0, 8 good cites).
- Routed round-34 defects: SKILL.md "Link-preview audit gate registry — round 35" (fd0d53b2); criteria checks {L}/.ufo/waves/round-35/criteria/*.py with receipts verification/criterion-*.txt; S074 correction note at the end of corpus/SOURCES.md; dcef39b5 correction in corpus/lessons/round-35.md. Lesson corpus/lessons/round-35.md, QUALITY.md "Round-35 criteria", PROVINCE.md and corpus/README.md round-35 sections, LOG.md round 35.
- Wave-1 reports: {L}/.ufo/waves/round-35/w1/*.md. Retained controls: {L}/.ufo/waves/round-35/retained/*.bundle (prerequisite 81d9fd74 or 318561ef) and round-34 bundles in {L}/.ufo/waves/round-34/retained/. Wave-1 tools: {L}/.ufo/waves/round-35/evidence/w1-tools/ (oracle.py, difftest.py, patch.diff).
- Holds (ended items; never retry, reroute or rephrase): KakeR31.CriticC1Counter, KakeR31.CriticSandboxThreatModel and KakeR35.CriticSealedDesign (its findings are not evidence; do not use or score its bundles). No item here asks whether a counter or selftest may trust runner-reported failure names, reason text or codes, and none models sandbox threats; if your item drifts there, stop that line and say so. If your own seat hits a provider safety or policy refusal or an automatic model switch, stop and write a one-line report saying so; do not rephrase.

# Bounds
- You are a leaf: no subagents, no swarm, no second judge, no admission or verdict on the round. Executors may spawn at most one read-only labrat probe.
- Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any tracked lane file. Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; seats never push, commit or update refs in the lane. Never run any jj command at /home/vgpnk/Projects/shokunin; in the lane, read-only jj only with --ignore-working-copy.
- Code that writes files or Git state runs only in your own sandbox: {SB}/<YourName>/ (clone with `git clone -q {L} {SB}/<YourName>/clone` when you need one, then `git -C <clone> checkout -q <rev>`; export TMPDIR={SB}/<YourName>/tmp after creating it; never /tmp or /dev/shm). Unset GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE before any git command in a sandbox. Sandbox commits in your own clone are allowed. Cap test runs: no unbounded recursive test runs; use `timeout` and at most 4 parallel processes. Deliverable files stay in your sandbox; name their absolute paths in your report.
- Owned sites: no live requests of any kind to the operator's owned web properties (ds4cc.com, app.ds4cc.com, *.onrender.com hosts of the operator, *.kimi.page, *.kimi.pro, veigapunk.github.io and any host pinned in {L}/corpus/knowledge/freshness-pins.json). ~/Projects/ds4cc-marketplace is a read-only local checkout: git show/cat-file only; never fetch into it.
- Network: only seats told to open a named public URL may fetch, GET only. Open sources by ordinary means only; never use a headless browser or any tool to pass a bot challenge, captcha or access control; a page you cannot open that way is recorded as unopened.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Your report is the only file you write in the lane.
- Tooling (operator, 2026-10-19): you and every seat may install or update tools that help the task without asking; read /home/vgpnk/.omp/agent/RULES.md first, use official channels, and record tool, version, channel and reason in your report. All pacman transactions are PAUSED host-wide: no pacman, no -Sy/-Syu/-U/-R, no downgrade, no service restart; use uv tool, npx or an official binary in ~/.local/bin.
- The only message target is agent://KakeR35 (the L1), for blockers only. Never message agent://all. Write plain English with no run-together words or private jargon.

# Result
Report under 80 lines: what you attacked, the exact commands you ran with exit codes, observed outputs, and evidence pointers (path:line, hash). Name what your item attacks in the first line. An unrun check has not passed; say what you did not verify. If you stop before finishing, the first line of your report must be `PARTIAL:` with what is missing. Your findings are advisory input for the L1 and the non-author closure.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    f = dict(sb=sb, L=L, REV=REV, CNT=CNT, KREV=KREV)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR, BOTH = ["operability"], ["freshness"], ["operability", "freshness"]
ITEMS = [
    # ---- C1
    item("RerunC1Sealed", "reviewer", OP, "Attacks C1's measured values: re-run the sealed C1 counter.",
         "- In a fresh clone at {REV}, run `python3 -B {CNT} c1 --root . --revision <rev> --key-revision {KREV}` for 16a6b8b8, bd14096a, b1cbbc39, 95abec21 and {KREV} (the last must exit 2). Compare each output field by field with {L}/.ufo/waves/round-35/verification/c1-at-<rev>.json (ignore nothing but ordering). Check the key sha256 against the pin in the counter.",
         "Table rev / exit / passed / matches receipt yes-no; any mismatch shown with both values.")
    ,
    item("ReviewSealedCasesVsContract", "reviewer", OP, "Attacks the C1 key: does every sealed case's expectation follow from the public contract and the round-34 rules?",
         "- Read {L}/.ufo/waves/round-35/sealed/c1-cases.json and the contract (SCORECARD round 35, C1 contract a-c; round-34 interface in .ufo/waves/round-34/c1-matrix.json). For each of the 24 cases: what it tests, whether its expected exit, verdict and findings follow from the public text alone, and whether it depends on any point {L}/.ufo/waves/round-35/w1/CriticC1ContractAmbiguity.md lists as undecided or as an HTML-standard mismatch.",
         "24-row table; every case that depends on an undecided point named with the quoted text.")
    ,
    item("ReviewToolRepairCode", "reviewer", OP, "Attacks the C1 repair code: `git diff 318561ef b1cbbc39 -- scripts/link_preview_audit.py`.",
         "- Review the end-tag stack logic (closing a matching element and its nested ones; a stray end tag; `</template>` with an open svg inside), `handle_startendtag`, the input_invalid vs page_unreadable split, pagesChecked, finding order and ids, and the docstring against behaviour. Write probe pages in your sandbox and run the tool on them.",
         "Findings with line numbers, a reproducing manifest for each, and severity.")
    ,
    item("MutToolRepair", "mutation-tester", OP, "Attacks the C1 test strength: mutation-test the repaired rules.",
         "- In a sandbox clone at {REV}, build at least 10 single-rule mutants of scripts/link_preview_audit.py: suppression never closes; only svg suppressed; self-closed svg opens suppression; og_url_multiple only for distinct values; og_url_multiple counts empty values; policy findings suppressed on any input fault (old rule); pagesChecked 0 on input faults; page_unreadable for a path escape; first og:url not compared when multiple; findings for unreadable pages duplicated. Score each with the selftest, the round-34 matrix counter and the sealed C1 counter (`--key-revision {KREV}`; put the mutant at scripts/link_preview_audit.py in a sandbox commit).",
         "Mutant table: selftest, matrix, sealed score; survivors of all three named with a fixture that would kill each.")
    ,
    item("ExecDifferentialRun", "executor", OP, "Attacks C1 behaviour on generated inputs: differential run of the landed tool against the wave-1 oracle.",
         "- Use {L}/.ufo/waves/round-35/evidence/w1-tools/difftest.py and oracle.py (lxml via `uv run --with lxml`). Run tool A = `git show b1cbbc39:scripts/link_preview_audit.py` against tool B = oracle.py for at least 20 seeds. Classify every disagreement: tool wrong per contract, oracle wrong (the oracle drops the round-34 og:image:url alias, which the contract keeps), or contract undecided.",
         "Disagreement classes with counts and one minimal reproducer each; any tool-wrong case flagged.")
    ,
    item("ReviewSelftestFixtures", "reviewer", OP, "Attacks the 10 new selftest fixtures and the changed `input_policy_suppressed_on_input` expectation.",
         "- For each fixture under scripts/fixtures/link-preview/ added or changed between 318561ef and b1cbbc39: does the expected.json follow from the contract; does the fixture test what its name says; is any fixture a copy of a sealed case (compare with sealed/c1-cases.json). Run the selftest at b1cbbc39 in a clean clone and paste its result.",
         "Per-fixture verdict; selftest output pasted; copies of sealed cases named or none.")
    ,
    item("CriticC1Sufficiency", "critic", OP, "Attacks what C1's 24/24 proves: could a tool that skips real parsing reach 22 of 24?",
         "- Build at most three cheap tools as sandbox commits on {REV}: a regex-only tool (no HTML parser) written from the public contract; the base tool plus only repair (c); the base tool plus a naive (a) that counts the substring `og:url`. Score each with the sealed C1 counter (`--key-revision {KREV}`) and the selftest. Say what the scores imply about the strength of the sealed cases.",
         "Scores per tool with commands; a verdict on whether 22 of 24 requires the claimed work.")
    ,
    item("ExecPartialRepairs", "executor", OP, "Attacks C1 separability inside the repair: score tools with only one repair each.",
         "- From patch {L}/.ufo/waves/round-35/evidence/w1-tools/patch.diff, make three sandbox tools: base plus only (a), only (b), only (c). Score each with the sealed C1 counter and report which sealed cases each repair group moves.",
         "Three scores with per-case pass lists; the sum of the moves explains 14 -> 24.")
    ,
    item("ExecRealInputRegression", "executor", OP, "Attacks C1 harm on real pages: the round-34 real-input run on the 102 retained ds4cc pages.",
         "- Run {L}/.ufo/waves/round-34/real_input_run.py (read its usage) with the tool at b1cbbc39 and at 318561ef in a clean clone; diff the outputs (findings per page). Explain every difference by contract rule.",
         "Both outputs saved, a diff summary, and a yes/no on unexplained changes.")
    ,
    item("SentinelToolInputs", "sentinel", OP, "Attacks the new code paths with hostile inputs.",
         "- On the tool at b1cbbc39: 100000 nested template tags, 50000 unclosed svg tags, a page of only end tags, mixed-case tag names (SVG, Template), a page listed twice, a symlinked page, a 16 MiB page with an unclosed svg at the start. Measure time and peak memory (`/usr/bin/time -v` with `timeout 60`), exit code and JSON validity; confirm no network and no writes (strace if available).",
         "Table per input: exit, valid JSON, seconds, max RSS; any crash, hang or wrong verdict flagged.")
    ,
    item("ReviewToolDocsConsistency", "reviewer", OP, "Attacks the C1 documentation: tool docstring, SKILL.md registry row and exit-2 correction, SCORECARD capability row.",
         "- Compare each statement about behaviour in those four places at {REV} with the tool at b1cbbc39 (run probes where cheap). Flag anything false or missing (for example a reason name absent from the verdict map, a fixture count, an old sentence the correction does not cover).",
         "List of statements with true/false and evidence.")
    ,
    # ---- C2
    item("RerunC2Sealed", "reviewer", FR, "Attacks C2's measured values: re-run the sealed C2 counter, both versions.",
         "- In a fresh clone at {REV}, run `python3 -B {CNT} c2 --root . --revision <rev> --key-revision {KREV}` for 16a6b8b8, bd14096a, b1cbbc39 and 95abec21, and sealed_count_v1.py at 95abec21. Compare field by field with verification/c2-at-<rev>.json and c2-v1-at-95abec21.json. Check which entry lines satisfy each probe (print the match span).",
         "Table rev / exit / met / probes / matches receipt; per-probe matching span quoted.")
    ,
    item("ReviewProbeMatchesTruth", "reviewer", FR, "Attacks C2's probe passes: is each matching entry sentence true per its cited source?",
         "- For each of the 12 probes in sealed/c2-probes.json, find the sentence(s) of corpus/knowledge/security-txt-publishing.md at 95abec21 that match, and check them against the retained source text cited (.ufo/waves/round-35/sources/*.txt), quoting both. Mark each true, partly true or false.",
         "12 rows with entry quote, source quote and verdict.")
    ,
    item("CriticProbeLeniency", "critic", FR, "Attacks the probe regexes: would false statements pass?",
         "- For each probe regex in sealed/c2-probes.json, write one false or misleading sentence that still matches (for example `Contact is not required`), and one true paraphrase that fails. Run them through the counter's normalization (lowercase, whitespace collapsed) and `re.search`. Estimate how many probes a confidently wrong entry could pass.",
         "Per-probe false-pass and true-fail examples with the command output; a count.")
    ,
    item("CriticC2Sufficiency", "critic", FR, "Attacks what C2's met proves: what would a cheaper entry score, now that the probes are known?",
         "- Without using the probe text to write them, build at most three entries as sandbox commits on {REV} (with the landed rows): an entry written only from S081 (the rejected Wikipedia text); an entry written only from the public topic list in the SCORECARD declaration with no source read; an entry from S079 alone. Score each with the sealed C2 counter. Say whether met requires this round's primary sources.",
         "Scores with commands; a verdict with reasons.")
    ,
    item("ReviewEntryRfcFacts", "reviewer", FR, "Attacks the C2 entry's RFC 9116 and RFC 8615 statements.",
         "- Check every sentence of corpus/knowledge/security-txt-publishing.md at 95abec21 that cites S078, S079, S082 or S083 against the retained texts; flag false, overstated or unsupported sentences and wrong ids. Note where the entry relies on a Reported (not Verified) erratum.",
         "Sentence list with verdicts and source quotes; count of false or unsupported.")
    ,
    item("ReviewEntryPagesFacts", "reviewer", FR, "Attacks the C2 entry's GitHub Pages build statements.",
         "- Check every sentence citing S006, S080, S086, S001 or S002 against the retained texts (round-35 sources and the S001/S002 rows and corpus/knowledge/ghp-served-set.md). Check each [INFERENCE] label is used where no source states the fact, and that no sentence presents an inference as sourced. Compare with {L}/.ufo/waves/round-35/w1/RevengerJekyllInclude.md and ScoutPagesDotfilesSource.md.",
         "Sentence list with verdicts; mislabelled inferences named.")
    ,
    item("ReviewEntryExamples", "reviewer", FR, "Attacks the C2 entry's statements about the live example files S084 and S085.",
         "- Check each sentence about github.com's and google.com's security.txt against the retained bodies (sources/S084.txt, S085.txt, html.gz) and the wave-1 observations (w1/ScoutGithubExpiresDynamic.md, w1/ScoutSecurityTxtCensus.md, evidence/). Fetch both files once now by GET and say whether the entry still holds.",
         "Sentence verdicts plus today's two bodies saved with times.")
    ,
    item("ReviewEntryHeader", "reviewer", FR, "Attacks the C2 entry's header lines (source, verified-at, recheck, scope, ground, coverage, falsifier, counter).",
         "- Check each header line against the receipts, the rows and the counter (version 2 caps size at 2200 [a-z0-9]+ words, not 1500 words). Run the recheck instruction as written in a sandbox if it is runnable. Compare with the header convention of corpus/knowledge/link-preview-metadata.md.",
         "Per-line verdict; any stale or unrunnable instruction named with the fix wording.")
    ,
    item("ReviewSourcesRows35", "reviewer", FR, "Attacks the SOURCES.md rows S078-S087 and the S006 change.",
         "- At {REV}: 11 cells per row, no unescaped pipe, tier and kind against CORPUS.md tier rules, anchors against receipts.json (time, status, text sha256 prefix), status and used-by against the entry's cites, S006's used-by change logged in the lesson, census `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exit code. Note the S079 tier (row A, the Gate draft said B) and judge it.",
         "Per-row verdict and the census output pasted.")
    ,
    item("ReopenGateQuotes", "reviewer", FR, "Attacks the round-35 Gate: re-verify every quote and re-open S086 and S087.",
         "- For each Gate line in corpus/lessons/round-35.md: the quote is an exact substring of the retained text and its word count is right. GET S086 and S087 live now; report status and whether the quote still holds.",
         "11-row table with exact yes/no and word counts; two live results.")
    ,
    item("ReviewS074Note", "reviewer", FR, "Attacks the appended S074 correction note at the end of corpus/SOURCES.md.",
         "- Check its counts against .ufo/waves/round-34/sources/S074.html.gz and S074.txt, that no S074 cell changed between 16a6b8b8 and {REV} (`git diff`), and that the note's shape matches the earlier notes in that area.",
         "Counts reproduced, diff result, verdict.")
    ,
    item("MutCounterV2", "mutation-tester", FR, "Attacks the C2 counter version 2 checks.",
         "- In a sandbox copy of {CNT} at {REV}, build mutants: no comment stripping; no Cf stripping; size by whitespace words; second Registry section allowed; tilde fences ignored; receipt URL check removed; used-by check removed; copied threshold 0.5. For each, rescore the retained C2 controls (verification/control-v2-c2-*.json revisions; bundles in .ufo/waves/round-35/retained/) with the revealed key and report which mutants no control kills.",
         "Mutant table with the controls that kill each; survivors named.")
    ,
    item("CriticCounterV2", "critic", FR, "Attacks counter version 2 for new evasions.",
         "- Look for routes version 2 opens or leaves: an unterminated `<!--` hiding honest text; NFKC folding; a URL substring that matches a longer junk URL; a Registry heading inside an HTML comment; an entry with honest text inside a fence (still counted). Build at most two sandbox commits on {REV} and score them with the revealed key.",
         "Each route with code line evidence, a scored commit where built, verdict open or closed.")
    ,
    item("ReviewV2Timing", "reviewer", FR, "Attacks the counter revision's timing and effect: was version 2 landed before any build was measured, and did it narrow anything?",
         "- From git history: order of 318561ef, bd14096a, b1cbbc39, 95abec21, {KREV}; list every receipt committed before bd14096a and whether any measures a build. Diff sealed_count_v1.py and sealed_count.py: list every behaviour change and whether it can only make met harder, or can also make it easier (for example the 1500-word versus 2200-word cap). Check the honest entry meets under both versions.",
         "Order table; change list with harder/easier; verdict on narrowing.")
    ,
    item("ReviewSealDiscipline", "reviewer", BOTH, "Attacks the seal: were the keys outside the lane until the reveal, and did the builders see them?",
         "- Check `git log --all -- .ufo/waves/round-35/sealed/` and `git log -p` for any key content before {KREV}; key file sha256 against the pins; wave-1 seat prompts in .ufo/waves/round-35/w1-spec.json and the L1's messages to ScribeEntryDraft and ExecToolRepair recorded in their reports, for any probe text or case expectation. Quantify how much of the probe topic list the drafter's item named.",
         "Leak/no-leak verdict with commands; topic-overlap list.")
    ,
    # ---- routed defects, frontier, harm
    item("ReviewCriteriaChecks", "reviewer", BOTH, "Attacks the three criteria checks and their receipts.",
         "- Re-run each command recorded in .ufo/waves/round-35/verification/criterion-*.txt in a clean clone at {REV} and compare. Then try to make each check pass on a bad input it should fail (an irrelevant 20-character quoted line; a row only in a task table; a receipt holding values in an array).",
         "Reproduction table and each false-pass found with its input.")
    ,
    item("MutCriteriaChecks", "mutation-tester", BOTH, "Attacks the strength of the three criteria checks.",
         "- Build at least three mutants per check (.ufo/waves/round-35/criteria/*.py) and show which the recorded receipts kill; propose fixtures for survivors.",
         "Mutant table per check with killed yes/no.")
    ,
    item("ReviewLessonMistakes", "reviewer", BOTH, "Attacks corpus/lessons/round-35.md: Mistakes rows, routed dispositions, correction and carried open.",
         "- Check every pointer (path:line, hash, receipt) resolves at {REV}; each `shown able to fail` claim has a receipt with exit 1; the correction's quoted lines match `git show dcef39b5:scripts/link_preview_audit.py` line numbers; no routed defect is mis-stated.",
         "Per-row verdict; every broken pointer listed.")
    ,
    item("ReviewQualityProvinceReadme", "reviewer", BOTH, "Attacks QUALITY.md \"Round-35 criteria\", PROVINCE.md and corpus/README.md round-35 sections.",
         "- Check every command they name runs as written at {REV}; every statement about the entry matches the landed entry; no cross-domain bleed (vulnerability handling, owned-site actions stay out). Check the QUALITY (a) numbers against the receipts.",
         "Per-section findings with evidence.")
    ,
    item("ReviewSkillRegistryRow35", "reviewer", OP, "Attacks the SKILL.md link-preview-audit gate registry row against PROTOCOL's Gate standard.",
         "- Read PROTOCOL.md section \"Gate standard\" (/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md) and the row at {REV}: every required field present, the verdict map equals the code's exits and reasons, the self-test command runs, the pinned proof files exist.",
         "Field-by-field verdict.")
    ,
    item("CriticHarmCheck", "critic", BOTH, "Attacks the no-harm claim across both axes.",
         "- `git diff --stat 16a6b8b8 {REV}` and `--numstat`: any deleted text line outside the repaired tool and the one changed fixture? Run the other lane gates' selftests (scripts/canonical_audit.py --selftest, scripts/base_path_selftest.py, scripts/citing_set_selftest.py if cheap) at 16a6b8b8 and {REV}; compare. Check that no earlier SOURCES row other than S006's used-by changed.",
         "Harm table; any deletion or changed result explained or flagged.")
    ,
    item("ReviewScorecardLog35", "reviewer", BOTH, "Attacks SCORECARD.md round-35 sections and LOG.md round 35 against the receipts.",
         "- Every number, hash and revision in those sections at {REV} against the receipt files; the capability row's evidence; the version-2 section's claims about controls. Flag any statement that a receipt does not support.",
         "Statement list with supported yes/no.")
    ,
    item("ExecSeparabilityAtTip", "executor", BOTH, "Attacks C1/C2 separability at the tip.",
         "- In a sandbox clone at {REV}: commit A = tip with scripts/link_preview_audit.py restored from 318561ef; commit B = tip with the entry and rows S078-S087 removed. Score both with both sealed counters (`--key-revision {KREV}`; the key path is present at the tip, so build A and B on 95abec21 instead, which predates the reveal, and say so).",
         "Four scores: A-C1, A-C2, B-C1, B-C2, with commands.")
    ,
    item("ReviewControlCorrection", "reviewer", OP, "Attacks the appended dcef39b5 correction in corpus/lessons/round-35.md and SCORECARD round 35.",
         "- Fetch the round-34 bundle in a sandbox clone; check every line number and quoted line; re-run the frozen round-34 counter on the control with renamed case directories and with one HTML comment appended (wave-1 ScribeControlCorrection probe: .ufo/waves/round-35/w1/ScribeControlCorrection.md) and confirm 28/28 and 7/28.",
         "Line-number table and the two scores reproduced or not.")
    ,
]

spec = {"wave": "kake-r35-w2", "milestone": "r35-falsify", "maxLanes": 64, "axes": BOTH,
        "reportDir": ".ufo/waves/round-35/w2", "context": CONTEXT, "items": ITEMS}
(HERE / "w2-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS))
