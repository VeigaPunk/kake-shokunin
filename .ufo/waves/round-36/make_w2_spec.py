#!/usr/bin/env python3
"""Write the round-36 wave-2 spec (w2-spec.json) next to this file."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = "f3a38bf8e68f6cee386125d34b5e95ac9b2df66e"
BUILD = "4d5b3d550748e5b52af31646b74c1aa435942bde"
KREV = "fd1fb723624b742a00a6e8e908f3b42901d627f8"
SB = "/fast/scratch/hyaku/kake-r36w2"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"

CONTEXT = f"""# Goal
Kake round 36, wave 2 (falsify). The L1 (KakeR36) holds the planner and integration seat; you are one leaf seat. Lane repo: {L}. Lane axes: operability and freshness (web properties and publishing). Wave 1 built and landed the work below; your item attacks one named piece of it. An attack tries to show the work is wrong, overstated, unsupported or harmful, with reproducible evidence; a clean result is reported as clean with what you ran. Time box: finish and write your report within 25 minutes; a partial report beats none.

# What landed (lane branch master at {REV}; base b720d799ae99c19a7c97f2b1391d4fe928be0e11)
- Claim C1 (freshness, capability): `scripts/source_recheck.py`, an offline re-check of a registry row's quote against a recorded fetch. Public contract: SCORECARD.md section "Round 36 — declared claims" (declared at 3555f63f), bullets (a)-(g). Frozen predicate `met: passed >= 25 of 28 sealed cases`. Counter `{L}/.ufo/waves/round-36/sealed_count.py` (version 3; v1 and v2 beside it; appended notes in SCORECARD explain each version). Build commit {BUILD} (tool from wave-1 ExecToolBuild, unedited). The sealed key is now public: reveal commit {KREV} holds `.ufo/waves/round-36/sealed/` (cases.json = key v2, cases-v1.json, make_cases.py, the L1's private reference ref.py, ablate.sh).
- Counting command: `python3 -B {L}/.ufo/waves/round-36/sealed_count.py --root <clone> --revision <rev> --key-revision {KREV}` (needs bwrap; refuses a revision holding the key).
- Receipts: `{L}/.ufo/waves/round-36/verification/` (c1-*.json, control-*.json, ablations/, v2/, criterion-*.txt, independent-selftest-reference.json). Control bundles: `{L}/.ufo/waves/round-36/retained/r36-control-*.bundle` (prerequisite 9d81c75c963cd9399c788e51bbd7f376fbe42cec).
- Also landed: `scripts/source_recheck_selftest.py` (101 fixtures, wave-1 ExecSelftest, fixture f08 changed by the L1), `scripts/source_snapshot.py` (live recorder, wave-1 ExecSnapshotFetcher), rows S088-S094 in `corpus/SOURCES.md`, lesson `corpus/lessons/round-36.md`, QUALITY `## Round-36 criteria` (a)-(f) in `corpus/QUALITY.md`, criteria checks `.ufo/waves/round-36/criteria/*.py`, SKILL.md section "Source re-check audit gate registry — round 36", appended corrections in `corpus/lessons/round-35.md` and `corpus/knowledge/security-txt-publishing.md`, SCORECARD "Round 36 — measured results" and a capabilities row, LOG.md round 36.
- Real-input run: `{L}/.ufo/waves/round-36/realrun/` (input.json 90 Gate quotes, manifest.json, snap-bodies.tar.xz, audit.json: 14 findings on 13 rows).
- Wave-1 reports: `{L}/.ufo/waves/round-36/w1/*.md`; control-wave reports `{L}/.ufo/waves/round-36/ctl/*.md`.

# Bounds
- You are a leaf: no subagents, no swarm, no second judge, no admission or verdict on the round.
- Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any tracked or untracked lane file other than your report. Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; read-only git is fine. Never run any jj command at /home/vgpnk/Projects/shokunin.
- Code that writes files or Git state runs only in your own sandbox {SB}/<YourName>/ (clone with `git clone -q {L} {SB}/<YourName>/clone && git -C {SB}/<YourName>/clone checkout -q {REV}`; export TMPDIR={SB}/<YourName>/tmp after creating it). Unset GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE before any git command. Cap every run with `timeout` (at most 300 s) and at most 4 parallel processes; kill any process tree you started before returning. Deliverables stay in your sandbox; name their absolute paths in your report. Never write deliverables into the lane.
- Never list or read /fast/scratch/hyaku/kake-r36/ (the L1's private tree); the key is public in the lane now, use that.
- Owned sites: no requests to the operator's web properties (ds4cc.com, app.ds4cc.com, *.onrender.com hosts of the operator, *.kimi.page, *.kimi.pro, veigapunk.github.io, any host in {L}/corpus/knowledge/freshness-pins.json). github.com and api.github.com reads of the public VeigaPunk/ds4cc-marketplace repository are allowed.
- Network: only seats whose item names a URL to open may fetch, GET only, ordinary means; never pass a bot challenge or access control; a page you cannot open is recorded as unopened.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Your report is the only file you write in the lane.
- Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, record tool, version, channel and reason in your report). pacman guard (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via uv tool, npx or an official binary in ~/.local/bin; never pacman -S, -Sy, -Syu, -U or -R, no downgrade, no service restart.
- If your seat hits a provider safety or policy refusal or an automatic model switch, stop and write a one-line report saying so; do not rephrase. The only message target is agent://KakeR36 (the L1), for blockers only; never agent://all. Write plain English.

# Result
Report under 80 lines: what you attacked, exact commands with exit codes, observed outputs, evidence pointers (path:line, hash). An unrun check has not passed; say what you did not verify. A partial report starts with `PARTIAL:`. Findings are advisory input for the L1 and the non-author closure.
"""


def item(name, role, axes, target, change, acceptance):
    f = dict(sb=f"{SB}/{name}", L=L, REV=REV, BUILD=BUILD, KREV=KREV)
    body = (f"# Target\n{target.format(**f)}\n# Change\n{change.format(**f)}\n"
            f"# Acceptance\n{acceptance.format(**f)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


FR, OP, BOTH = ["freshness"], ["operability"], ["freshness", "operability"]
FLAGS = {
    "S004": "quote_missing", "S005": "quote_missing", "S006": "quote_missing", "S007": "quote_missing",
    "S008": "quote_missing", "S016": "unsupported_type", "S017": "quote_missing", "S025": "quote_missing",
    "S040": "moved", "S065": "quote_missing", "S066": "unsupported_type", "S068": "moved and quote_missing",
    "S087": "gone",
}

ITEMS = [
    item("RerunC1Sealed", "reviewer", BOTH,
         "Re-run C1's counting command and compare with the committed receipts.",
         "- In a sandbox clone at {REV}, run the counter for --revision {BUILD}, b720d799ae99c19a7c97f2b1391d4fe928be0e11, cd3212796cab7a2afa03b638dbfafe7194df9629 and {KREV} with --key-revision {KREV}. Compare passed, met, toolSha256, counterSha256 and perCase with `{L}/.ufo/waves/round-36/verification/c1-keyrev-at-*.json` field by field. Confirm the tool at {BUILD} equals the wave-1 deliverable sha256 577b2d7d028964e06152f5a7b792141e586045eaa8ec9262ee7f416ba5510d48 and the tool at {REV}.",
         "Four runs pasted with exit codes; every field compared; any difference named."),
    item("RerunControls", "reviewer", OP,
         "Re-score every control with the frozen counter and compare with the committed receipts.",
         "- Fetch each `{L}/.ufo/waves/round-36/retained/r36-control-*.bundle` into your sandbox clone (`git fetch <bundle> 'refs/heads/*:refs/heads/ctl/*'`), score each head with --key-revision {KREV}, and compare with `{L}/.ufo/waves/round-36/verification/control-*.json`. Also score the independent implementation `{L}/.ufo/waves/round-36/retained/independent/selftest-seat-reference.py` with --tool-file. Confirm each control's tool bytes equal `{L}/.ufo/waves/round-36/ctl/<Name>.md`'s described control.",
         "Table control → committed vs re-run score; any difference named."),
    item("RerunAblations", "mutation-tester", OP,
         "Regenerate the 36 ablation receipts from the revealed reference and compare.",
         "- In your sandbox, copy `{L}/.ufo/waves/round-36/sealed/ref.py` and reproduce `ablate.sh`'s ablation files (each prefixes `import os; os.environ['KAKE_ABLATE']='<name>'`), score each with the counter (--tool-file, --key-file pointing at the revealed `sealed/cases.json` in your clone), and compare passed/perCase with `{L}/.ufo/waves/round-36/verification/ablations/`. Then add 6 ablations of your own that skip a rule the 36 do not (for example manifest-level input_invalid, version check, check_invalid on a missing body file, the 'no other finding for a check_invalid check' rule, uppercase `<SCRIPT>`, character references without semicolon) and report each score.",
         "Committed vs regenerated table; six new ablations with scores and whether any meets 25."),
    item("ReviewToolCode", "reviewer", BOTH,
         "Review the landed tool `scripts/source_recheck.py` at {BUILD} line by line against the C1 contract.",
         "- For each contract sentence (usage, manifest rules, a-g, verdict), cite the implementing lines or name the gap. Look for case-specific code (literals, hashes or strings that only make sense for the revealed cases in `sealed/cases.json`), any file read beyond the manifest and its bodies, network, environment or subprocess use. List the builder's open-point choices from `{L}/.ufo/waves/round-36/w1/ExecToolBuild.md` and judge each against the cited source.",
         "Sentence → lines table; gaps and any case-specific code named with line numbers."),
    item("MutTool", "mutation-tester", OP,
         "Mutation-test the landed tool against the sealed counter and the selftest.",
         "- Copy `scripts/source_recheck.py` from {BUILD} into your sandbox. Make at least 20 single-point mutants spread over bullets a-g (drop a removal step, flip case sensitivity, swap 301/302, skip BOM, compare media type case-sensitively, stop evaluating after a check_invalid, etc.). Score each with the sealed counter (--tool-file, --key-file = revealed cases.json) and with `scripts/source_recheck_selftest.py --tool`. Survivors = mutants that still meet 25 or still pass 101/101.",
         "Mutant table with sealed score and selftest result; survivors named with the rule they skip."),
    item("SentinelToolInputs", "sentinel", OP,
         "Check the landed tool's robustness on large and malformed inputs (defensive review of a read-only audit tool).",
         "- In your sandbox, run `scripts/source_recheck.py` (from {BUILD}) with timeout 60 on: a 20 MB HTML body, 1 million unmatched `<script>` start tags, 1 million `<!--` without close, a 50000-hop redirect chain in the manifest, a body path that is a symlink pointing outside the manifest directory, a body path that is a directory, a FIFO, deeply nested JSON (depth 100000), a manifest of 100000 checks. Record wall time, exit code and whether output is valid JSON for each.",
         "Table input → time, exit, valid JSON; any hang, crash or out-of-directory read named."),
    item("CriticSealedCasesFairness", "critic", BOTH,
         "Attack the fairness of the revealed sealed cases (`sealed/cases.json` at {KREV}) against the public contract.",
         "- For each of the 28 cases, check that every expected finding follows from the contract text (not only from the L1's reference). Map the 18 undecided points listed in `{L}/.ufo/waves/round-36/w1/CriticContractAmbiguity.md` to any case whose expectation depends on one. Note the ScoutReopenS088 finding that RFC 9110 never calls 303 temporary, and the ExecProbeCp1252 bytes: does any case depend on them?",
         "Per-case verdict fair / depends-on-undecided-point, with the deciding sentence."),
    item("CriticKeyV2Change", "critic", BOTH,
         "Attack the key v1 → v2 and counter v2 → v3 change as possibly a rule changed after data.",
         "- Diff `sealed/cases-v1.json` and `sealed/cases.json` (case by case: checks added, contentTypes changed). Did any case become easier for some tool? Read the appended SCORECARD notes and git timestamps (`git log --format='%H %cI %s' -- .ufo/waves/round-36/ scripts/source_recheck.py`). Was anything measured on a build before v3? Judge against prompt section 6 item 9 (`/home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-36.md`) and the round-35 closure's ruling on its v1 → v2 change (`{L}/corpus/lessons/round-35-verifier-spotcheck.md` 'Ruling on the counter change').",
         "Ruling-style argument both ways with timestamps; any case made easier named."),
    item("CriticClaimSufficiency", "critic", BOTH,
         "Attack whether 28 of 28 shows the capability the claim names, now that the key is public.",
         "- With the revealed cases, build the cheapest tool you can that skips one whole contract bullet's work yet scores >= 25 (for example by exploiting check patterns the cases share). If you succeed, it shows a slack the pre-reveal ablations missed. Build in your sandbox and score with --tool-file. Also judge whether 'freshness' is the right axis given the real-input run in `realrun/`.",
         "Best skipping tool's score and what it skips, or the bound you reached; axis judgement with quotes."),
    item("ExecDifferential", "executor", OP,
         "Differential test between the landed tool and the independent implementation `retained/independent/selftest-seat-reference.py`.",
         "- Write a seeded generator in your sandbox producing random manifests and bodies across bullets a-g (status mixes, redirect chains with relative locations, HTML with comments/script/style/template/entities, whitespace and NFKC variants, media types, BOMs and charset labels, malformed checks). Run 2000 manifests through both tools; list every disagreement with a minimal reproducer and the contract sentence that decides it.",
         "Disagreement list with reproducers and deciders, or zero disagreements with the generator seed."),
    item("ReviewSelftest", "reviewer", OP,
         "Review `scripts/source_recheck_selftest.py` against the contract, including the L1's f08 change.",
         "- Sample at least 30 fixtures across bullets: does each expectation follow from the contract sentence it quotes? Is the f08 change (charset utf-16 → shift_jis) right per S090 (WHATWG labels)? Which fixtures accept two readings, and is that justified? Run it against the landed tool and against the toy tools the seat described (`w1/ExecSelftest.md`).",
         "Fixture verdicts with line numbers; run outputs pasted."),
    item("ReviewSnapshotTool", "reviewer", FR,
         "Review `scripts/source_snapshot.py` (recorder) for correctness and safe fetching.",
         "- Read it fully. Check: no redirect following by urllib, hop recording, Location resolution, 8-hop cap, 1 request per second, timeouts, body cap, contentType recording, manifest shape vs the contract, what it does with a non-http(s) Location, and that it has no owned-host guard (the procedure in SKILL.md relies on the input list). Run it offline against a local server you write (127.0.0.1 only).",
         "Findings with line numbers and a pasted offline run."),
    item("ReviewRealRunInput", "reviewer", FR,
         "Review the real-input run's input selection and manifest.",
         "- Read `{L}/.ufo/waves/round-36/realrun/input.json` and `manifest.json` and the extractor report `w1/ExecGateQuoteExtractor.md`. For 15 sampled ids, check the chosen quote and URL against the lesson Gate line it came from and the SOURCES row. Were any owned hosts included? Were rows without quotes silently dropped (which)? Re-run the audit from `snap-bodies.tar.xz` (extract in your sandbox next to manifest.json) and compare with `audit.json`.",
         "Sample table; owned-host check; re-run identical or differences named."),
    item("ReviewSourcesRows", "reviewer", FR,
         "Review rows S088-S094 in `corpus/SOURCES.md` at {REV} against the retained texts.",
         "- For each row: does the teaches cell state only what the retained text `{L}/.ufo/waves/round-36/sources/SXXX.txt` says (quote the supporting span)? Scope distinct from existing same-URL rows (S010, S028, S033, S029, S030, S031)? Anchor sha256 prefix equals receipts.json? S094's reject reason located? Run the census `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` (read-only) and paste it.",
         "Per-row verdict with quoted spans; census output pasted."),
    item("ReviewGateLines", "reviewer", FR,
         "Review the round-36 lesson Gate lines (`corpus/lessons/round-36.md` section Gate).",
         "- Each quote an exact substring of the retained text (whitespace-normalised)? <= 25 words? Location named? Decision matches the SOURCES row? The S094 decision differs from the scribe's draft (`w1/ScribeSourcesRows.md`): is the L1's reject supported by `w1/ScoutReopenS094.md`? Paste each verifying command.",
         "Seven lines verified with pasted commands; mismatches named."),
    item("ReviewCriteriaChecks", "reviewer", OP,
         "Review the four round-36 criteria checks and their receipts.",
         "- `.ufo/waves/round-36/criteria/{{ablation_floor_check,control_tree_check,version_bump_check,hash_resolve_check}}.py` and `verification/criterion-*.txt`. For each: does the failing receipt fail for the stated reason, does the passing receipt pass for the right reason, and name one false pass you can construct (as round 35's ReviewCriteriaChecks did).",
         "Per check: receipt verdicts confirmed and one constructed false pass."),
    item("ReviewQualityAndSkill", "reviewer", OP,
         "Review QUALITY `## Round-36 criteria` (a)-(f) and the SKILL.md round-36 registry section.",
         "- Each criterion's grounding pointer resolves and says what is claimed; each named check exists and its 'shown able to fail' receipt exists. SKILL rows: every command runs as written (run the selftest; run source_recheck.py with no arguments for exit 64); verdict map matches the tool's code.",
         "Per criterion and per row: resolves / runs, or the defect."),
    item("ReviewCorrections", "reviewer", FR,
         "Review the two appended round-35 corrections (end of `corpus/lessons/round-35.md`, end of `corpus/knowledge/security-txt-publishing.md`).",
         "- Check each against the retained texts (`.ufo/waves/round-35/sources/S084.txt`, `S078.txt`) and the round-35 closure routed defect 5. Was any original line rewritten (`git diff b720d799ae99c19a7c97f2b1391d4fe928be0e11 {REV} -- <file>` must show additions only)?",
         "Both corrections verified with pasted commands; additions-only confirmed."),
    item("ReviewLessonAndScorecard", "reviewer", BOTH,
         "Review the round-36 lesson, SCORECARD round-36 sections and LOG round 36 for numbers that do not reproduce.",
         "- Re-derive every count and hash in `corpus/lessons/round-36.md`, SCORECARD sections headed 'Round 36' and the LOG round-36 entry from the committed receipts. Check the capability row's pointers. Check the SCORECARD diff from base is additions only plus the one inserted capability row (`git diff --numstat`).",
         "List of numbers checked with source; each mismatch named."),
    item("CriticHarmCheck", "critic", BOTH,
         "Attack the no-harm statement: did the round break or weaken anything that held before?",
         "- In a sandbox clone at {REV}, run the earlier lane selftests with timeouts: `scripts/link_preview_selftest.py`, `scripts/base_path_selftest.py`, `scripts/citing_set_selftest.py`, `scripts/citing_set_hostile_selftest.py`, and `node scripts/freshness-sweep.mjs --selftest` (HOME and KAKE_SELFTEST_DIR set to sandbox temp dirs), and compare with their base results at b720d799ae99c19a7c97f2b1391d4fe928be0e11. Check `git diff --numstat b720d799ae99c19a7c97f2b1391d4fe928be0e11 {REV}` for deletions in tracked files.",
         "Before/after selftest table; deletions listed (or none)."),
    item("ReviewMistakesTable", "reviewer", FR,
         "Review the round-36 lesson `## Mistakes` rows and the routed-defect disposition table.",
         "- Each row's evidence pointer resolves; each fix is shown able to fail by a committed receipt; the captured-by column is honest. Are there round-36 mistakes the table misses (for example in the wave-1 reports: seats writing into the lane, the predicate label 'met:' missing from receipts noted in `w1/CriticPredicateIdentity.md`)?",
         "Per row verdict; missing mistakes listed with pointers."),
]

for sid, reason in FLAGS.items():
    ITEMS.append(item(f"ReopenFlag{sid}", "scout", FR,
                      f"Re-open {sid} by hand: the real-input re-check reported `{reason}`.",
                      f"- Find {sid}'s input in `{{L}}/.ufo/waves/round-36/realrun/input.json` (url, quote, lesson) and its row in `{{L}}/corpus/SOURCES.md`. GET the URL yourself (no redirect following first, then follow), save the body in {{sb}}/. Decide whether the finding is real: for quote_missing, search the live page text for the quote and for its key words (did the page change, does the quote sit in JavaScript-rendered content, is the Gate quote a paraphrase, or is it a tool or extraction rule miss?); for moved, record each hop and whether the row URL should change; for gone, record status; for unsupported_type, record the media type and whether the row needs a different check. Quote the live text you found.",
                      "Verdict real / tool miss / extraction miss / paraphrase, with the live evidence quoted and the saved body path."))


def main():
    spec = {"wave": "kake-r36-w2", "milestone": "r36-falsify", "maxLanes": 64, "axes": ["operability", "freshness"],
            "reportDir": ".ufo/waves/round-36/w2", "context": CONTEXT, "items": ITEMS}
    (HERE / "w2-spec.json").write_text(json.dumps(spec, indent=1) + "\n")
    print(len(ITEMS), "items")


if __name__ == "__main__":
    main()
