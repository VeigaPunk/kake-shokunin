#!/usr/bin/env python3
"""Generate the round-55 wave-2 (falsify) spec. Output: w2-spec.json beside this file."""
import json
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W = f"{LANE}/.ufo/waves/round-55"
REV = sys.argv[1] if len(sys.argv) > 1 else "a7a548e102b71bd16b0a6ddafa469393a2c98b69"
GODSPEED = "/skill:godspeed\n"
STAGED = "/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge"
ENT = {
    "S372": "corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md",
    "S373": "corpus/knowledge/yahoo-japan-robots-pattern-syntax.md",
    "S418": "corpus/knowledge/yahoo-japan-robots-txt-basics.md",
}

CONTEXT = (
    "/skill:godspeed\n"
    f"Round-55 kake falsify wave (W2). Lane repo: {LANE}. The build under attack is committed at revision {REV} (measured by both counters "
    f"at that revision; read committed bytes with `git -C {LANE} show {REV}:<path>`; the worktree may move after you start). Every path in your assignment is absolute under "
    f"{LANE}. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. "
    "Seats never mutate the fleet repo, sibling lanes, lane jj state or the lane Git index: write ONLY your own report file, no other path "
    "inside the lane, no `git add/commit/stash/checkout/reset/pull/push`, no jj mutation. Read-only git (show, log, ls-tree, diff) is fine. Any scratch fixture: "
    "`D=$(mktemp -d) && git -C \"$D\" init -q`, every later git call names `-C \"$D\"`, verify `git -C \"$D\" rev-parse --show-toplevel` equals `$D`; never commit with a "
    "throwaway identity anywhere else; to test a mutated copy, `git clone -q --no-hardlinks " + LANE + " \"$D\"` or `git -C " + LANE + " archive <rev> | tar -x -C \"$D\"` and mutate only `$D`. "
    "Domain source trees and /home/vgpnk/Projects/shokuknow are read-only (never run campaign tools there). Frozen contract: "
    f"`{W}/contract.md` (with its counter-version-2 section) and `{W}/contract.json`; retained source bodies `{W}/sources/S372.html S373.html S418.html` + `receipts.json`. "
    "Unit rule: one unit per CJK character, one per non-CJK whitespace token; quotes are <= 25 units. Every claim of yours names the command you ran and its observed output; an unrun "
    "check is `unrun`, an inference is `[INFERENCE]`; never fabricate. No credential material, session tokens, `op://` refs or private URLs in any report. "
    "Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety "
    "gate; record tool/version/channel/reason). Pacman guard: all pacman transactions are PAUSED host-wide — never run pacman; use `uv tool`/`npx`/an official binary in `~/.local/bin` "
    "or report the need. Report format: first line `# <your seat name>`, a line `ATTACKS: <what you attack, by path or id>`, then the sections your assignment names; end with a line "
    "`VERDICT: <one-line result>`. Keep reports factual and under ~150 lines. L1 holds the planner seat; you are a leaf: no subagent dispatch except an executor's single read-only labrat probe."
)

items = []


def add(name, role, text):
    items.append({"name": name, "role": role, "prompt": GODSPEED + text})


# ---- row verification executors (C1 rows) ---------------------------------------------------------
GROUPS = [
    ("ExecRowsAccess", ["accessibility-review-cards.json", "accessibility-review-packet.md", "freshness-sidecar.json"]),
    ("ExecRowsBaiduYahoo", ["baidu-friendly-crawl-guidance.md", "baidu-mobile-matching-error-causes.md", "yahoo-japan-rel-nofollow-semantics.md"]),
    ("ExecRowsGoogleA", ["canonical-selection.md", "crawler-identity.md", "crawl-budget-consequences.md"]),
    ("ExecRowsGoogleB", ["crawl-error-status-table.md", "dynamic-rendering-workaround-limits.md", "js-rendering-queue.md"]),
    ("ExecRowsPublish", ["link-preview-metadata.md", "pages-base-path.md", "security-txt-publishing.md"]),
    ("ExecRowsOps", ["receipt-integrity.md", "redirect-rewrite-rules.md", "vault-properties.md"]),
    ("ExecRowsRender", ["render-static-sites.md", "render-web-services.md", "robots-txt-rules.md"]),
]
for name, files in GROUPS:
    lst = ", ".join(f"`corpus/knowledge/{f}`" for f in files)
    add(name, "executor",
        f"ATTACK target: the three coverage-map rows added to `corpus/README.md` §Coverage map at {REV} for {lst} (claim C1). For each file: extract the row with "
        f"`git -C {LANE} show {REV}:corpus/README.md` (the row whose Entry cell names `knowledge/<file>`); split its Coverage cell into atomic factual statements; for each, find "
        f"the supporting passage in `git -C {LANE} show {REV}:corpus/knowledge/<file>` (quote <= 25 words with line number) and classify SUPPORTED / OVERREACH (row says more than the file) / "
        "UNSUPPORTED / STALE (true once, no longer). Re-derive every number or count in the row with a command you run (e.g. `python3 -c` over the JSON, `grep -c`) and print the observed value. "
        "Check the row's `(S###)` ids equal ids named in the file's own `source:` header and that each id exists as a row in `corpus/SOURCES.md` at that revision. If a row has any "
        "OVERREACH/UNSUPPORTED/STALE statement, propose a minimal replacement Coverage cell (keep >= 5 tokens, no `|`, share a word with the file's H1 or first 1500 characters, still true). "
        "Report sections: `PER-ROW:` (table: file, statement, class, evidence line, command output), `COUNTS RE-DERIVED:`, `PROPOSED REPLACEMENTS:` (or `none needed`), `UNRUN:`.")

# ---- entry reviewers ------------------------------------------------------------------------------
for sid, path in ENT.items():
    name = {"S372": "ReviewerEntryRefusal", "S373": "ReviewerEntryPattern", "S418": "ReviewerEntryBasics"}[sid]
    add(name, "reviewer",
        f"ATTACK target: knowledge entry `{path}` (row {sid}) at {REV}, claim C2. Read the entry (`git -C {LANE} show {REV}:{path}`) and the retained body `{W}/sources/{sid}.html` "
        "(extract visible text). Falsify, in order: (1) every quoted span is a raw substring AND its English rendering preserves every qualifier the Japanese states (negation, scope, "
        "`every crawl`, `normally`, `only`, `first`, `root`, directive names, `prefix`/`end`); list each rendering you judge lossy or inflated with the exact words; (2) every non-quoted "
        "statement is either stated by the page or tagged `[INFERENCE]` — list statements that go beyond the page untagged; (3) every `Contrast with the RFC side` or cross-link statement "
        f"about the lane's other entries is actually what that entry says (`{LANE}/corpus/knowledge/robots-txt-rules.md`, `crawl-scope-per-host.md`, `yahoo-japan-rel-nofollow-semantics.md` at "
        "that revision): quote the supporting line, or mark the contrast unsupported; (4) the header trio and the `recheck:` command is runnable and prints what it says (run its `grep -F -c` "
        "half against the retained body); (5) the scope note and `What this entry does not establish` claims no more than the page; (6) counts of units stated anywhere match a recount. "
        "Report sections: `QUOTES:` (table: span, units, substring yes/no, rendering faithful yes/no + reason), `UNTAGGED BEYOND-PAGE:`, `CONTRAST CHECKS:`, `RECHECK:`, `DEFECTS:` "
        "(each with the line number and a minimal fix), `NO-DEFECT CHECKS:`.")

# ---- source re-open executors ---------------------------------------------------------------------
for sid, path in ENT.items():
    url = {"S372": "https://info-search.yahoo.co.jp/archives/002849.php",
           "S373": "https://info-search.yahoo.co.jp/archives/002850.php",
           "S418": "https://info-search.yahoo.co.jp/archives/002885.php"}[sid]
    add({"S372": "ExecReopenS372", "S373": "ExecReopenS373", "S418": "ExecReopenS418"}[sid], "executor",
        f"ATTACK target: freshness of {sid} and the entry `{path}` at {REV}. Perform a fresh plain GET of `{url}` now (`curl -sSL`, read-only; one request). Compare byte length and "
        f"sha256 with `{W}/sources/receipts.json` and `{W}/sources/{sid}.html`. Run the entry's own `recheck:` command exactly as written (the curl half) and the same grep against the retained "
        "body; print both counts. Then, for EVERY double-quoted span of 6+ units anywhere in the entry and in the lesson Gate line "
        f"(`git -C {LANE} show {REV}:corpus/lessons/round-55.md`, the `- {sid} ` line), test `span in fresh_text` with python and report units + result. Report drift (any byte change) with a "
        "`diff` summary. Also record the HTTP status, final URL, and `Last-Modified`/`ETag` response headers if present. Report sections: `FETCH:`, `RECHECK COMMAND:`, `SPAN TABLE:`, `DRIFT:`.")

# ---- counter run executors ------------------------------------------------------------------------
add("ExecRunC1", "executor",
    f"ATTACK target: the C1 measurement. In `{LANE}` run (python3 -B; no writes): `python3 -B .ufo/waves/round-55/c55_readme_index.py --root {LANE} --revision {REV}` (twice; outputs must be "
    f"byte-identical), the same with `--json` (parse it with python; check `met`, `exit`, `index_mismatches`), and `--selftest`. Run the counter at the BASE revision "
    "fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d and diff against `.ufo/waves/round-55/controls/base-c1-readme-index-v2.txt`. Then independently recount the claim WITHOUT the counter: with your own "
    "python (not importing c55_readme_index), list `git ls-tree -r --name-only` under `corpus/knowledge/` at the base and at the build revision and, for each file, whether the first table of "
    "`## Coverage map` in `corpus/README.md` names `knowledge/<file>` in its second column; print unindexed at base (expect 21 by the counter) and at the build revision. Report any disagreement "
    "between your count and the counter's. Report sections: `COMMANDS:`, `DETERMINISM:`, `INDEPENDENT RECOUNT:`, `DISAGREEMENTS:`.")
add("ExecRunC2", "executor",
    f"ATTACK target: the C2 measurement. In `{LANE}` run (python3 -B; no writes): `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root {LANE} --revision {REV}` (twice; byte-identical), the "
    f"same with `--json` (parse; `conditions_passed`, `met`, per-check state), and `KAKE_R55_SELFTEST_REV={REV} python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` (run it from "
    f"`{LANE}`; it builds fixtures only under `mktemp -d`). Run the counter at base fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d and diff against `controls/base-c2-quote-truth-v2.txt`. Then recount "
    "the claim WITHOUT the counter: rows at base vs build revision (`grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|'` over `git show <rev>:corpus/SOURCES.md`), the S372/S373 rows "
    "diffed cell by cell against base (only used-by may differ), S418 present once with 11 cells and no pipe inside a cell, the three entries present with the header trio. Report any "
    "disagreement between your recount and the counter. Report sections: `COMMANDS:`, `DETERMINISM:`, `INDEPENDENT RECOUNT:`, `DISAGREEMENTS:`.")
add("ExecCensusReplay", "executor",
    f"ATTACK target: condition C7 (validate-before-append) and the census exit. In a `mktemp -d` scratch, extract the build revision ({REV}) with "
    f"`git -C {LANE} archive {REV} | tar -x -C \"$D\"`, then replay `{W}/validate_append.sh`'s steps against the scratch (copy the scratch `corpus/` plus the five non-corpus used-by targets into a "
    "`validate` dir and run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <that dir>/corpus/SOURCES.md`; do NOT run the script itself in the lane — it writes there). "
    f"Compare your stdout/exit byte-for-byte (modulo the absolute path) with the committed receipts `{W}/assimilation/validate/census-stdout.txt` and `census-exit.txt`. Also run "
    f"`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` (lane-level census; read-only) and report exit + counts of warnings by code, and "
    "run the census on a scratch registry with S418 duplicated (E03 expected) and with a pipe inside a cell to confirm the census catches what C3 relies on. Report sections: `REPLAY:`, `DIFF:`, `LANE CENSUS:`, `NEGATIVE CONTROLS:`.")
add("ExecSeatSettlement", "executor",
    f"ATTACK target: the wave-1 settlement (round-54 routed defect 4: reports must be committed at settlement). Read `{W}/w1-dispatch.json` (seat names, roles) and `{W}/w1-results.json` if it exists. "
    f"For every W1 seat: does `{W}/w1/<Name>.md` exist in git at {REV} (`git -C {LANE} ls-tree`), is its first line `# <Name>`, does it end with a `VERDICT:` line, did the results file report "
    f"a settled status. List seats without a committed report, reports without a seat, seats whose report is empty. Misroot sweep: `git -C /home/vgpnk/Projects/shokunin status --porcelain` — list every "
    "untracked path whose content names `kake` round 55 (check with grep) and any file under the lane that is not git-tracked or ignored and was written this round (`git -C <lane> status --porcelain`; "
    "read-only). Report sections: `SEAT TABLE:` (name, role, report committed, status), `MISSING:`, `MISROOT:`.")

# ---- mutation testers -----------------------------------------------------------------------------
add("MutC2Counter", "mutation-tester",
    f"ATTACK target: `{W}/c55_quote_truth.py` and its `--selftest` (47 fixtures + 3 unit checks). In a scratch (`git clone -q --no-hardlinks {LANE} \"$D\"`, mutate only `$D`), apply >= 18 single-point "
    f"mutants to the counter (examples: drop each of the 8 conditions; `<= UNIT_CEILING` to `<= 40`; remove the page-unique rule; remove `in_content`; flip `!=` in C3's held-row cell test; "
    "drop the strict-ancestor check; accept any `used_by` order; compare registries only on adopted rows; read the worktree not `git show`; skip the title/URL-field body identity check; "
    "`MIN_UNIQUE_SPANS` 3→0), and for each run `KAKE_R55_SELFTEST_REV=" + REV + " python3 -B <scratch>/.ufo/waves/round-55/c55_quote_truth.py --selftest` from inside `$D`. Report KILLED/SURVIVED per mutant. "
    "For each survivor, write a fixture (python dict edit in the same style as the selftest `@case`) that kills it and run it to prove it. Report sections: `MUTANTS:` (table), `SURVIVORS:`, `KILL FIXTURES:`.")
add("MutC1V2Counter", "mutation-tester",
    f"ATTACK target: `{W}/c55_readme_index.py` (version 2) and its `--selftest` (35 fixtures). In a scratch clone, apply >= 16 single-point mutants (examples: `FLOOR` 46→45; drop `common` words filter; "
    "`MAX_FILES_PER_ROW` 2→99; drop the first-table restriction; drop `deleted`; drop `head_changed`; drop duplicate detection; change the `< 5` token rule; read the worktree instead of `git show`; "
    "remove protocol-name exemption; drop nested-path population; header-name column lookup removed), run the scratch copy's `--selftest` for each, report KILLED/SURVIVED, and for each survivor write and "
    "run a killing fixture. Also report mutants that are exit-code-equivalent and say which facts a facts-asserting fixture would pin. Report sections: `MUTANTS:`, `SURVIVORS:`, `KILL FIXTURES:`.")
add("MutDataClaims", "mutation-tester",
    f"ATTACK target: whether the two counters notice damage to the DATA they judge, at the real tree. In scratch clones of {LANE} at {REV} (each mutant in its own clone commit with `git -C \"$D\" -c "
    "user.name=mut -c user.email=mut@local commit` — identity confined to `$D`), apply >= 14 data mutants — C1: edit one coverage cell to `TBD`; replace a row's Coverage with another row's text; delete a "
    "knowledge file; change a knowledge file H1; add an unindexed file; second `## Coverage map` heading; point a row at a nonexistent path; swap two Entry cells — C2: change one character inside a quoted "
    "span of each entry; lengthen a quote beyond 25 units; edit `corpus/lessons/round-55.md` Gate quote; remove S418's row; change S372 `teaches` cell; change a receipt sha; remove the validate receipt. "
    "Run BOTH counters (`--root $D --revision <that clone commit>`) for each and report the exit; a mutant that leaves a counter at exit 0 is a SURVIVOR. Report sections: `MUTANTS:` (table: id, edit, "
    "counter, exit), `SURVIVORS:`, `WHAT EACH SURVIVOR MEANS FOR THE CLAIM:`.")

# ---- critics --------------------------------------------------------------------------------------
add("CriticJunkC1", "critic",
    f"ATTACK target: claim C1 at {REV} — can a change that improves nothing meet `met: index_mismatches == 0 AND knowledge_files >= 46` under counter version 2? Build (in a scratch clone at {REV}) "
    "at least 5 junk variants that would pass without an honest index (rows copying each file's H1 verbatim; rows listing another file's paragraph; a coverage cell that is true of every file; "
    "an unrelated 5-token cell sharing one rare H1 word; moving coverage-map rows into a second table; header renaming to shift column roles) and run the counter on each commit. For each pass, say "
    "whether a human reviewer would also pass it (is it a real description?). Also attack the claim wording in `contract.md` for universal/negative clauses that the counter does not enumerate, and the "
    "`calibration` axis declaration (is `calibration` honestly the lowest non-retired axis per SCORECARD.md; is there any harm to operability/freshness from the README edits — diff the existing rows "
    "`git diff fcaf4b85 " + REV + " -- corpus/README.md` and confirm no pre-existing row changed). Report sections: `JUNK VARIANTS:` (edit, exit, human-would-pass), `WORDING:`, `AXIS/HARM:`.")
add("CriticJunkC2", "critic",
    f"ATTACK target: claim C2 at {REV} — can a junk or mis-glossed set of entries meet `met: conditions_passed == 8 of 8` under counter version 2? In scratch clones construct >= 5 variants (e.g. "
    "true-but-trivial quotes that are page-unique; entry prose that inverts the page's meaning around truthful quotes; a lossy rendering that drops `normally`/`first`/`every crawl`; an entry that "
    "quotes only S372's text under S373; a receipt for the right body with a stale `fetchedAt` in a different offset) and run the counter. For each pass explain what the counter cannot see, and "
    "whether the entry text you wrote would also fool the two reviewers' checks. Also attack the frozen wording: `contract.md` §C2 'Before/After' for universal clauses; the do-nothing control; "
    "the sourced-claim requirement (does a claim rest on a row opened this round: S372/S373 were opened in round 53 and re-opened now; S418 is new) — is that honest, or should the report say the sourced "
    "claim rests on S418 plus re-opened rows? Report sections: `VARIANTS:`, `WHAT THE COUNTER CANNOT SEE:`, `WORDING:`, `SOURCED-CLAIM HONESTY:`.")
add("CriticClaimsAdmission", "critic",
    f"ATTACK target: the round's admission posture at {REV}. Read `{W}/contract.md`, `{LANE}/corpus/lessons/round-55.md`, `{LANE}/corpus/README.md` (diff vs base fcaf4b85), `{LANE}/SCORECARD.md` calibration row "
    "and Round-54 block, `corpus/lessons/round-54-verifier-spotcheck.md` (routed defects 1–4). For each routed defect: addressed in the round's bytes? (cite path:line or say no). Check that "
    "the lesson's statements of fact (row counts, collision list, quarantine ids, 'none renumbered', '49 of 49') re-derive from committed bytes — run each command. List every sentence in the lesson or "
    "contract that is not yet true at that revision (the lesson was written before the final measurement) and every assertion with no counting command. Also check trend-verdict inputs honestly: "
    "expansion/quality/discernment — what would each verdict be today and what evidence is missing. Report sections: `ROUTED DEFECTS:`, `RE-DERIVED FACTS:`, `NOT YET TRUE / UNCOUNTED:`, `TREND INPUTS:`.")

# ---- reviewers (docs) -----------------------------------------------------------------------------
add("ReviewerQualityRegistry", "reviewer",
    f"ATTACK target: `corpus/QUALITY.md` §Round-55 criteria and `SKILL.md` §Round 55 gate registry additions at {REV}. For each criterion: does its grounding path/lesson/counter exist and say what it is cited for "
    "(open each); is the falsifier command real and does it fail on the stated base (run the base control command at fcaf4b85 where the criterion names one); is the criterion new relative to earlier "
    "rows (`grep` prior QUALITY sections) or a duplicate; does it cite a lesson that exists (a criterion with no lesson behind it is `harmed` per LEARNING.md). For the two gate-registry rows: check "
    "all eight cells, that every number (35 fixtures, 47 + 3, exit-code map) matches the counters at that revision (run `--selftest`), and that the entry commands run. Report sections: "
    "`CRITERIA:` (each: grounded yes/no, falsifier real yes/no, new yes/no), `REGISTRY ROWS:`, `DEFECTS:`.")
add("ReviewerLessonGate", "reviewer",
    f"ATTACK target: `corpus/lessons/round-55.md` at {REV} against `/home/vgpnk/Projects/shokunin/CORPUS.md` (SOURCES rule 1: every new row's Gate has URL, access date, <= 25-word located quote; "
    "`## Mistakes` shape; counts carry commands; corrections append-only) and `/home/vgpnk/Projects/shokunin/LEARNING.md` (a Gate with candidates, admitted, rejected with reasons, spot-check). "
    "Report every missing element (e.g. no rejected candidate with reason and flip condition yet; no spot-check result yet; Gate lines for held rows S372/S373 vs 'new row' wording), every sentence stating a "
    "number without a command, and every claim contradicted by committed bytes (run the commands). Do not edit. Report sections: `CONFORMANCE TABLE:`, `UNCOUNTED NUMBERS:`, `CONTRADICTIONS:`, `MISSING:`.")

# ---- scouts ---------------------------------------------------------------------------------------
for name, cand in (("ScoutRejectUaList", "yahoo-japan-user-agent-list-unreadable.md"),
                   ("ScoutRejectSitemap", "yahoo-japan-sitemap-constraints.md"),
                   ("ScoutRejectDnsId", "yahoo-japan-crawler-identification-by-dns.md")):
    add(name, "scout",
        f"ATTACK target: an UNADOPTED staged candidate, to give the lesson Gate a reasoned admit/reject from the same theme. Read `{STAGED}/{cand}` (reference only; its quotes and dates prove nothing), find "
        f"the source page it cites (URL in its `source:` line), fetch it yourself once (plain GET), and judge it against the lane's bar (`{LANE}/corpus/QUALITY.md` criteria on qualifier-preserving glosses, "
        f"Platform mechanism, quote ceiling 25 units) and scope (`{LANE}/PROVINCE.md` §Core/§Frontier/§Adjacent: sitemap and crawl-hygiene ground is kake's; browser/DOM is tabi's). Give: verdict "
        "ADMIT-LATER / REJECT, the reason (concrete: unreadable body, duplicate of a held row by URL, out-of-scope, claim not on the page, over-ceiling quote), the flip condition, up to 3 located quotes "
        "(<= 25 units, raw substrings of YOUR fetch, with heading), whether the URL already appears in `corpus/SOURCES.md` at the build revision (`grep -c`), and the sha256/bytes/status of your fetch. "
        "Report sections: `CANDIDATE:`, `FETCH:`, `VERDICT TABLE:`, `QUOTES:`, `REGISTRY COLLISION CHECK:`.")
add("ScoutStaleClaims", "scout",
    f"ATTACK target: statements in lane documents that the round's build made stale or false. At {REV} (and the worktree for comparison) scan `{LANE}/corpus/README.md`, `{LANE}/PROVINCE.md`, `{LANE}/SKILL.md`, "
    f"`{LANE}/corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`, `{LANE}/corpus/knowledge/robots-txt-rules.md` and `{LANE}/corpus/knowledge/crawl-scope-per-host.md` for: counts of knowledge entries/rows that no "
    "longer hold (e.g. `46`, `155`, `27 rows`), the phrase 'lane holds' / 'did not hold' about Yahoo! robots ground, pointers that say the lane has no entry for the refusal-file rules, and anything that "
    "should now cross-reference the three new entries. Give file:line, the stale text, and a one-line correction proposal. Corrections to existing entries must be APPENDED (corrections-are-new-entries), so "
    "say which lines would need an appended note vs which are historical round-dated prose. Report sections: `STALE:` (table), `CROSS-REFERENCES DUE:`, `HISTORICAL-OK:`.")

# ---- sentinel / connector / simplifier / revenger -------------------------------------------------
add("SentinelHygiene", "sentinel",
    f"ATTACK target: credential and path hygiene in everything this round adds. For the diff `git -C {LANE} diff fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d {REV} --name-only` (and its content), search for: secrets "
    "patterns (keys, tokens, `Authorization`, cookies), `op://` refs, session or private URLs, home-directory paths that name private material, accidental binary files, files over 1 MiB, nested `.git` dirs, "
    "`__pycache__`, and any file written outside the lane's declared scope (`.ufo/waves/round-55`, `corpus/`, `SKILL.md`, `PROVINCE.md`). Also check that no seat wrote to the fleet root "
    "(`git -C /home/vgpnk/Projects/shokunin status --porcelain | grep -i 'round-55\\|kake'`). Give each search command and hit count. Report sections: `SEARCHES:`, `HITS:`, `SCOPE:`.")
add("ConnectorW2", "connector",
    f"ATTACK target: cross-claim and cross-source interactions after the build at {REV}. Look for: (1) C1's coverage rows for the three new entries and C2's entries disagreeing on titles/ids/areas; (2) the frontier "
    "ground map's `Rows`/`Entries` cells disagreeing with the registry's `used-by` cells (build a python check over `corpus/SOURCES.md` used-by vs the map); (3) README rows or the ground map that cite "
    "ids that no longer match (S372/S373 now also used-by the new entries); (4) other sibling lanes that now hold a conflicting statement about Yahoo! robots rules or about prefix matching "
    "(grep sibling `corpus/knowledge` read-only); (5) patterns repeated from earlier rounds' verifier spot-checks that this build repeats. Report sections: `INTERACTIONS:`, `MAP-VS-REGISTRY CHECK:` (script and output), "
    "`SIBLING CONFLICTS:`, `REPEATS:`.")
add("SimplifierBuild", "simplifier",
    f"ATTACK target: surplus in what this round adds (YAGNI deletion, evidence-preserving). At {REV} measure and propose deletions or merges for: README rows that restate their entry's H1; ground-map rows that no "
    f"counter or reader needs; duplicated scratch (`{W}/assimilation/validate/` is a ~2.8 MB mirror — what is the minimum the census and C7 need, per the counter and `sources-census.sh`); redundant "
    "paragraphs inside the three new entries (list sentence pairs that say the same thing); leftover scaffolding (`make_spec_w1.py` outputs, `__pycache__`). For each: size, who reads it (a counter, a reader, "
    "nobody), the deletion and what verification would stay green. Do not edit. Report sections: `CANDIDATES:` (path, bytes, consumer, proposal), `KEEP:` (and why), `RISK:`.")
add("RevengerStaged", "revenger",
    f"ATTACK target: what the landing dropped from the staged package. Compare `{STAGED}/yahoo-japan-robots-txt-refusal-rules.md`, `yahoo-japan-robots-pattern-syntax.md`, `yahoo-japan-robots-txt-basics.md` with the "
    f"landed entries at {REV} (`git show`). List every claim/observation in a staged entry that the landed entry omits, and judge each: dropped on purpose (unsupported, over-ceiling quote, pre-renumber id, "
    "dated 2026-10-24) or lost (a true, page-stated point the lane should still hold). Reconstruct the staged author's intent from `MERGE-REPORT.md` and the staged `ground:` lines; say whether the landed "
    "entries serve that intent. Report sections: `DROPPED:` (table: staged claim, why, on purpose/lost), `LOST CLAIMS TO RESTORE:` (with a located <= 25-unit quote from the retained body), `INTENT:`.")

# ---- scribes (drafts for L1 integration) ----------------------------------------------------------
add("ScribeScorecard", "scribe",
    f"Draft the `## Round 55 — declared and measured claims` block for `{LANE}/SCORECARD.md` in the style of the `## Round 54 — declared and measured claims` block (read it, and Round 52). Facts: frozen "
    f"contract `{W}/contract.md`; base fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d; measured revision {REV} (final revision will be recorded by L1: write the placeholder `<FINAL>` exactly where the measured "
    f"commit goes); run both counters yourself (`python3 -B .ufo/waves/round-55/c55_readme_index.py --root {LANE} --revision {REV}` and the quote-truth one) and copy the observed outputs. Columns "
    "`Claim | Axis | Before → after | Counting command | Verdict`. Axis wording: C1 is declared on `calibration` (round-54 sub-axis, score 1) and the block must say that is outside the prompt-declared "
    "operability+freshness axes and the operator may rule; C2 on freshness. State the verdict words as `improved` only where the counters at the measured revision and independent recounts agree; leave "
    "admission to the non-author closure. Include one capabilities-table row candidate (the quote-truth + readme-index gates: what they can now do, evidence pointer, first-working round 55) only if "
    "you judge it a real capability. Report sections: `BLOCK:` (one fenced markdown block), `NUMBERS RE-DERIVED:` (command, output), `OPEN:`.")
add("ScribeLog", "scribe",
    f"Draft the `LOG.md` entry for round 55. Read the last two round entries in `{LANE}/LOG.md` for the exact heading/field style (it is append-only; the entry goes at the end). Content: the motivating "
    "evidence (README coverage map 21 of 46 unindexed at base; the version-1 counters passing junk per W1 critic/mutation reports; the staged package's 6 of 6 over-ceiling quotes), the claims, the "
    "re-verification result (freshness: the three recheck commands re-run; S372/S373 fresh GET sha equal to retained, no drift per `w1/ScoutFreshS372.md` / `ScoutFreshS373.md`), landed changes with file paths, "
    f"and the placeholder `<FINAL>` for the measured commit. Every number carries its command (re-run them at {REV}). Report sections: `ENTRY:` (one fenced markdown block), `COMMANDS RUN:`, `OPEN:`.")
add("ScribeReportFacts", "scribe",
    f"Assemble the fact sheet L1 will paste into the round report's `Sources & frontier` and `Before → after measurements` sections. Run and paste the outputs (python3 -B, read-only): both counters at base "
    f"fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d and at {REV}; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` with its exit code; registry census commands "
    f"from `/home/vgpnk/Projects/shokunin/CORPUS.md` §Census (rows, malformed, tier histogram, status histogram, duplicate ids, enum violations, missing used-by paths) at base and at {REV} via "
    "`git show <rev>:corpus/SOURCES.md` in a scratch dir (the commands assume the lane root: extract the revision to `mktemp -d` and run them there); knowledge-file count and entries-by-ground "
    "table before/after; the used-by changes old→new for S372 and S373 (cell diff vs base). Report sections: `COMMANDS AND OUTPUTS:` (verbatim), `SOURCES TABLE:` (rows before→after, added by tier, "
    "touched old→new), `FRONTIER:` (rows advanced, per PROVINCE).")

SPEC = {"reportDir": ".ufo/waves/round-55/w2", "maxLanes": 64, "context": CONTEXT, "items": items}
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w2-spec.json")
    json.dump(SPEC, open(out, "w"), indent=1, ensure_ascii=False)
    from collections import Counter
    print(len(items), dict(Counter(i["role"] for i in items)))
