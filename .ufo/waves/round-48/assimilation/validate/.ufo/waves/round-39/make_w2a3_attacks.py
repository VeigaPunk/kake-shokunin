#!/usr/bin/env python3
"""Writes w2a3-attacks.json: one attack item per wave-1 output that a claim, a record or a non-claim patch rests on."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W1 = "/fast/scratch/hyaku/kake-r39a3w1"
R1 = f"{L}/.ufo/waves/round-39/w1a3"
V = f"{L}/.ufo/waves/round-39/verification/a3"
OP, FR, BOTH = ["operability"], ["freshness"], ["operability", "freshness"]
items = []


def add(name, role, axes, target, change, acceptance=None):
    d = {"name": name, "role": role, "axes": axes, "target": target, "change": change}
    if acceptance:
        d["acceptance"] = acceptance
    items.append(d)


MET = [("MutUrlAuthority", "M03", 4), ("MutUrlAuthority", "M04", 22), ("MutUrlAuthority", "M05", 22),
       ("MutUrlAuthority", "M09", 4), ("MutUrlAuthority", "M10", 25), ("MutEntryNumbering", "M02", "11, 33"),
       ("MutNamespaceBinding", "M02_root_trailing_slash", 10), ("MutNamespaceBinding", "M03_root_uri_casefold", 10),
       ("MutNamespaceBinding", "M04_entry_local_default_binding", 11), ("MutNamespaceBinding", "M07_foreign_root_url", "10/14"),
       ("MutNamespaceBinding", "M08_foreign_entry_url", "11/14"), ("MutNamespaceBinding", "M09_field_default_reset", "15/17"),
       ("MutNamespaceBinding", "M10_foreign_priority", "14/17"), ("MutNamespaceBinding", "M11_entry_nested_url", "11/14"),
       ("MutStdlibSubstitution", "M09", "see mutants.json")]
for fam, m, s in MET:
    short = m.split("_")[0]
    add(f"Verify{fam[3:]}{short}", "reviewer", OP,
        f"Met control `{V}/w1a3-{fam}__{m}.json` (passed 24 of 24): mutant `{W1}/{fam}/mutants/{m}.py`, its entry in `{W1}/{fam}/mutants.json`, said to break contract sentence(s) {s}.",
        f"- Diff the mutant against `{W1}/shared/reference.py`; confirm exactly one change. Run both on the seat's witness (paths in mutants.json) with `timeout 60 python3 -B <tool> --manifest <manifest>` and quote both outputs.\n"
        "- Decide from {CONTRACT} alone: does the contract determine the expected output on that witness, and which tool matches it? Verdict: `valid control` (mutant breaks a contract sentence the reference obeys), `equivalent` (same outputs on all inputs you can construct), or `contract-silent` (the contract does not decide the witness). A valid control here is evidence that kill rule (1) fired correctly.",
        "One-line verdict first, then the two outputs, the sentence text and your reasoning (≤25 lines).")

for sid, url, f in [("S105", "https://www.w3.org/TR/xml/", "xml-1.0.html"), ("S106", "https://www.w3.org/TR/xml-names/", "xml-names.html"),
                    ("S107", "https://www.w3.org/TR/xmlschema11-2/", "xmlschema11-2.html"), ("S108", "https://www.sitemaps.org/faq.html", "faq.html"),
                    ("S109", "https://yandex.com/support/webmaster/en/controlling-robot/sitemap", "yandex-sitemap.html")]:
    add(f"Reopen{sid}", "scout", OP,
        f"SOURCES row {sid} (`{L}/corpus/SOURCES.md`, added in this round) and its retained bytes `{L}/.ufo/waves/round-39/sources/{f}`.",
        f"- Fetch {url} (GET once), sha256 it and compare with the row and the retained file (a dynamic page may differ: then diff the visible text). Check that every claim in the row's `scope`, `anchor` and `teaches` cells is located in the page text (quote the line), that each quoted phrase is verbatim, and that the contract sentence numbers the row names say what the row says they say.",
        "Per cell: holds / overstated / wrong, with the located line.")

for c, shape in [("CtlRegexTweak", "regex reader, no XML parser (24 of 24)"), ("CtlGuessTweak", "keyword guesser, no parse tree (23)"),
                 ("CtlHandTokenizer", "str-split tokenizer, no re/xml/html (23)"), ("CtlStdlibConvenience", "stdlib conveniences only (21)"),
                 ("CtlXsdTweak", "XSD-expressible rules only (20)"), ("CtlHtmlParserReader", "html.parser reader (20)"),
                 ("CtlValuesOnly", "value rules 21–32 only (14)"), ("CtlEngineLenient", "lenient crawler reading (14)")]:
    add(f"Fidelity{c[3:]}", "reviewer", OP,
        f"Control `{L}/.ufo/waves/round-39/a3-controls/w1a3/{c}.py`, shape: {shape}; seat report `{R1}/{c}.md` (for tweaks: base file in `{L}/.ufo/waves/round-39/a3-controls/dead-w1/` and the L1-materialized diff `{W1}/{c}/l1-materialized.diff`).",
        "- Does the file keep its named shape (grep for forbidden imports or techniques; for tweaks count changed lines against the base)? Does it skip the work its shape says it skips? Did the L1 materialize the seat's text byte-for-byte (compare with the fenced block in the report)? Construct 3 inputs from the contract on which this control must disagree with a correct tool and run it on them.",
        "Verdict: faithful shortcut / not a shortcut (implements the skipped work) / mis-materialized, with commands and outputs.")

add("CriticKeyStrength", "critic", OP,
    f"The sealed 24-case key's discriminating power, from receipt totals only (`{V}/*.json`: read label, passed, met, toolSha256; never rows or why) and the mutant descriptions in `{W1}/Mut*/mutants.json`.",
    "- Tabulate, per contract sentence 1–34, how many scored single-sentence mutants break it and how many of those reach 24. Name the sentences the key evidently never tests, and the smallest set of added cases (described from the contract, not from the key) that would kill every 24-scoring mutant and the regex shortcut. This feeds the lesson; no claim is re-scored.",
    "Per-sentence table plus the proposed case list (≤40 lines).")
add("ReviewKillRuleRecord", "reviewer", OP,
    f"The SCORECARD records 'Round 39 — kill rule (1) fired' and 'Wave-1 additions' at lane tip (`git -C {L} show HEAD:SCORECARD.md | sed -n '/kill rule (1) fired/,$p'` — use the branch tip from `git -C {L} rev-parse master`).",
    f"- Check each statement against the frozen declaration `git -C {L} show ceecb1b1:SCORECARD.md` (control classes, kill rule, order) and the receipts in `{V}/`: every receipt cited exists, says met true, has the frozen counterSha256 f3a0cd60… and keySha256 16440f62…; the counts (15 of 54 mutants; controls' totals) are right (`jq` over the receipts); no key, counter, predicate or target text changed between ceecb1b1 and the tip (`git diff ceecb1b1 master -- .ufo/waves/round-39/sealed_count.py .ufo/waves/round-39/c1-contract.md`).")
add("RerunCcCheckFinal", "mutation-tester", OP,
    f"QUALITY (j) check v2 `{L}/.ufo/waves/round-39/criteria/control_consequence_check.py` on the final wave-1 receipts `{V}/`, and the survivors reported in `{R1}/MutCcCheckV2.md`.",
    f"- Run it (v2.1 at the lane tip; readings A and B: without and with `--oracle-sha 663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8`) on a copy of `{V}/` and quote both; the L1 recorded A = 17 controls meeting (the reference, 15 mutants, CtlRegexTweak) and B = 16 (`{L}/.ufo/waves/round-39/verification/a3-jcheck/v21-*.txt`). Re-apply each MutCcCheckV2 survivor (`{W1}/MutCcCheckV2/mutants/`, same single-point change) to v2.1 and report which v2.1's 20-case selftest now kills; M06 (build identity by revision text) is expected to survive the selftest — write a fixture that kills it.",
    "Outputs, exits, and a patch adding the killing fixtures (in your sandbox).")
add("ReviewRobotsFixtures", "reviewer", OP,
    f"ExecRobotsDeclaredFixtures' selftest patch (`{R1}/ExecRobotsDeclaredFixtures.md`, patch under `{W1}/ExecRobotsDeclaredFixtures/`).",
    "- For each new fixture, check its expected value against the round-38 contract text it cites (`git -C {L} show 2909f1dc:.ufo/waves/round-38/` contract files and `corpus/knowledge/robots-txt-rules.md`); apply the patch in a sandbox clone and run the selftest against the unchanged tool; confirm the claimed mutant kills.")
add("ReviewRecheckOversize", "reviewer", FR,
    f"ExecRecheckOversize's fix for `scripts/source_recheck.py` (`{R1}/ExecRecheckOversize.md`, patch under `{W1}/ExecRecheckOversize/`).",
    "- Apply in a sandbox clone; run `source_recheck_selftest.py` and `source_recheck_hardening_selftest.py` before and after; check the fix changes only the oversized-body path (diff review) and that no other status changes on the existing fixtures.")
add("MutRecheckOversize", "mutation-tester", FR,
    f"The new oversized-body fixture added by ExecRecheckOversize (`{W1}/ExecRecheckOversize/`).",
    "- In a sandbox clone with the patch applied, write ≥6 single-point mutants of the fixed code path (drop the guard, emit both statuses, count it in checksEvaluated, off-by-one on the cap) and show which the new fixture kills.")
add("MutCopyGuard", "mutation-tester", OP,
    f"ExecCopyGuard's `copy_guard.py` (`{W1}/ExecCopyGuard/`).",
    "- Try to evade it with copies it should flag (identifier renames, statement reordering, dead-code insertion, function splitting) and to trip it with independent code; ≥8 attempts; report which pass and the thresholds' effect.")
add("VerifyCarriedDefects", "reviewer", BOTH,
    f"ScribeCarriedDefects' ten 'still open' statements (`{R1}/ScribeCarriedDefects.md`, `{W1}/ScribeCarriedDefects/carried.md`).",
    "- Re-check each pointer at the lane tip (path:line or command); verdict per item.")
add("MutCriterionO", "mutation-tester", OP,
    f"ScribeQualityCriterion's checker `{W1}/ScribeQualityCriterion/check_control_inventory.py` and draft criterion (o).",
    "- Write ≥8 mutants of the checker and ≥4 adversarial SCORECARD samples (an inventory listing hashes in a code block only, a hash with a typo, a tool scored after the declaration, an empty inventory) and report what it accepts that it should not.")
add("ReviewPublicSitemaps", "reviewer", OP,
    f"Real-run inputs `{W1}/ScoutPublicSitemaps/realrun/` (manifest and six files) from `{R1}/ScoutPublicSitemaps.md`.",
    "- Check provenance: sha256 of each file against the report; each robots.txt line cited allows the fetch; the manifest is version 1 with `sitemapUrl` equal to the fetched URL. Hand-derive, from the contract alone, the expected verdict for the two smallest files (rfc-editor, mdn) and record your reasoning; do not run any sitemap tool.")

(HERE / "w2a3-attacks.json").write_text(json.dumps(items, indent=1, ensure_ascii=False) + "\n")
print(len(items), "attack items")
