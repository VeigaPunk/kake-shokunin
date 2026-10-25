#!/usr/bin/env python3
"""Generate the round-55 wave-1 (build) spec. Output: w1-spec.json beside this file."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W = f"{LANE}/.ufo/waves/round-55"
SRC = f"{W}/sources"
KNOW = f"{LANE}/corpus/knowledge"
STAGED = "/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge"
GODSPEED = "/skill:godspeed\n"

CONTEXT = (
    "/skill:godspeed\n"
    "Round-55 kake build wave (W1). Lane repo: /home/vgpnk/Projects/shokunin/kake-shokunin. Every path in your "
    "assignment is absolute under that repo. Every `Report:` trailer path is relative to "
    "/home/vgpnk/Projects/shokunin/kake-shokunin — write it at /home/vgpnk/Projects/shokunin/kake-shokunin/<that path>. "
    "Seats never mutate the fleet repo, sibling lanes, lane jj state or the lane Git index: write ONLY your own report file, "
    "no other path, no `git add/commit/stash/checkout/reset/pull/push`, no jj mutation. Read-only git (show, log, ls-tree) is fine. "
    "Any scratch fixture: `D=$(mktemp -d) && git -C \"$D\" init -q`, every later git call names `-C \"$D\"`, verify "
    "`git -C \"$D\" rev-parse --show-toplevel` equals `$D`; never commit with a throwaway identity anywhere else. "
    "Domain source trees and /home/vgpnk/Projects/shokuknow are read-only (read files; never run campaign tools there). "
    "Round facts: frozen contract `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-55/contract.md`; base revision "
    "fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d; round date 2026-10-25. Retained source bodies (Yahoo! JAPAN info-search pages, "
    "fetched 2026-10-25, HTTP 200) are `.ufo/waves/round-55/sources/S372.html` (archives/002849.php), `S373.html` (002850.php), "
    "`S418.html` (002885.php) with `receipts.json`. Unit rule: one unit per CJK character, one per non-CJK whitespace token; every quote "
    "you propose MUST be <= 25 units and a raw substring of the retained body (verify with `grep -F` / python `in`), written with ASCII "
    "double quotes, never paraphrased inside the quotes. Never fabricate: an unrun check is reported as unrun; a located quote names its "
    "heading/section. No credential material, session tokens, `op://` refs or private URLs in any report. "
    "Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read "
    "/home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason). Pacman guard: all "
    "pacman transactions are PAUSED host-wide — never run pacman; install via `uv tool`/`npx`/an official binary in `~/.local/bin` "
    "or report the need. Report format: first line `# <your seat name>`, then the sections your assignment names; end with a line "
    "`VERDICT: <one-line result>`. Keep reports factual and under ~150 lines. L1 holds the planner seat; you are a leaf: no subagent "
    "dispatch except an executor's single read-only labrat probe."
)

items = []


def add(name, role, text):
    items.append({"name": name, "role": role, "prompt": GODSPEED + text})


# ---- A. coverage-row scribes (C1) ------------------------------------------------------------------
ROWS = [
    ("RowAccessCards", "accessibility-review-cards.json"),
    ("RowAccessPacket", "accessibility-review-packet.md"),
    ("RowBaiduFriendly", "baidu-friendly-crawl-guidance.md"),
    ("RowBaiduMobile", "baidu-mobile-matching-error-causes.md"),
    ("RowCanonicalSel", "canonical-selection.md"),
    ("RowCrawlBudget", "crawl-budget-consequences.md"),
    ("RowCrawlErrors", "crawl-error-status-table.md"),
    ("RowCrawlerIdent", "crawler-identity.md"),
    ("RowDynamicRender", "dynamic-rendering-workaround-limits.md"),
    ("RowFreshSidecar", "freshness-sidecar.json"),
    ("RowJsRenderQueue", "js-rendering-queue.md"),
    ("RowLinkPreview", "link-preview-metadata.md"),
    ("RowPagesBasePath", "pages-base-path.md"),
    ("RowReceiptIntegrity", "receipt-integrity.md"),
    ("RowRedirectRules", "redirect-rewrite-rules.md"),
    ("RowRenderStatic", "render-static-sites.md"),
    ("RowRenderServices", "render-web-services.md"),
    ("RowRobotsRules", "robots-txt-rules.md"),
    ("RowSecurityTxt", "security-txt-publishing.md"),
    ("RowVaultProps", "vault-properties.md"),
    ("RowYahooNofollow", "yahoo-japan-rel-nofollow-semantics.md"),
]
for name, f in ROWS:
    add(name, "scribe",
        f"Claim C1 (coverage-map calibration). Read the whole knowledge file `{KNOW}/{f}` and the README section "
        f"`## Coverage map` of `{LANE}/corpus/README.md` (read its header and 3 existing rows for the exact 3-cell format "
        f"`| Area | Entry | Coverage |`, where the Entry cell names the file as `knowledge/{f}` in backticks). Draft exactly ONE new "
        "coverage-map row for this file: Area = a short noun phrase (<= 8 words, may carry the round tag found in the file's own "
        "header); Entry cell = the backticked `knowledge/<file>` path (optionally followed by ` (S###)` ids copied from the file's own "
        "`source:` line); Coverage = 10-45 words stating what the file actually holds, every statement traceable to the file's own text "
        "(copy counts only if the file states them; no `all`/`every`/`complete` unless the file does). The Coverage cell MUST share at "
        "least one 5+-letter word with the file's H1 or first 1500 characters, contain no `|` character, and not start with `TBD`. "
        "Report sections: `ROW:` (one fenced code block holding the single table line), `EVIDENCE:` (2-4 file-line references with the "
        "<=25-word passage each statement rests on), `RISKS:` (anything in the file that the row cannot say without overreach, or any "
        "inaccuracy/staleness you noticed in the file itself). Do not edit the file.")

# ---- B. entry scribes (C2) -------------------------------------------------------------------------
ENTRIES = [
    ("EntryRefusalRules", "S372", "yahoo-japan-robots-txt-refusal-rules.md", "S372.html",
     "https://info-search.yahoo.co.jp/archives/002849.php"),
    ("EntryPatternSyntax", "S373", "yahoo-japan-robots-pattern-syntax.md", "S373.html",
     "https://info-search.yahoo.co.jp/archives/002850.php"),
    ("EntryRobotsBasics", "S418", "yahoo-japan-robots-txt-basics.md", "S418.html",
     "https://info-search.yahoo.co.jp/archives/002885.php"),
]
for name, sid, fname, body, url in ENTRIES:
    add(name, "scribe",
        f"Claim C2 (Yahoo! JAPAN robots.txt assimilation). Draft the knowledge entry `corpus/knowledge/{fname}` for row {sid} "
        f"({url}). Read the retained body `{SRC}/{body}` fully (extract text, do not rely on memory). The shokuknow staging package "
        f"holds a candidate for reference ONLY: `{STAGED}/{fname}` — its `opened`, quotes and recheck prove nothing for this lane; "
        "re-ground every statement in the retained body. Required shape (see `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` "
        "for the lane's house style): lines 1-4 = `source: " + sid + " — <url> — § <section> (更新日 <date printed on the page>) — fetched 2026-10-25`, "
        "`verified-at: 2026-10-25`, `recheck: 180d — <runnable command printing a count>` (the command must be a `curl -fsSL '<url>' | "
        "grep -F -c '<quote>'` form; run the grep form against the RETAINED body and report its count), `ground: <one line>`; then a blank line; "
        "then an H1 and prose that cites `[" + sid + "]` below the 8-line header. Verbatim passages go in `> \"...\"` blockquote lines with ASCII "
        "double quotes; every verbatim span <= 25 units and a raw substring of the retained body; render each quote in English right after it "
        "(the rendering must preserve every qualifier the Japanese states — directive names, scope, negation, `case-sensitive`, `prefix`, "
        "`root`, `every crawl` …; round-54 mined exactly this error class). Prose beyond quotes is the lane's own reading: mark anything the "
        "page does not state as `[INFERENCE]`. End with a `Scope note:` line (a claim about what the operator's documentation states; no "
        "robots.txt was served, no crawl observed). Cross-link by plain path (no new S-ids beyond " + sid + " and ids already in "
        "`corpus/SOURCES.md`) to existing lane entries that really exist: `robots-txt-rules.md`, `crawl-scope-per-host.md`, "
        "`yahoo-japan-rel-nofollow-semantics.md` — state the Yahoo!-vs-RFC-9309 contrast only where `robots-txt-rules.md` itself states the "
        "RFC side. Also produce: (1) `GATE LINE:` the lesson `## Gate` line in exactly this shape: `- " + sid + " — " + url + " — accessed "
        "2026-10-25 — § <heading> (更新日 <date>) — quote: \"<located quote, 6-25 units>\" (<n> units; raw substring of the retained body, "
        "sha256 <from receipts.json>, <bytes> bytes, HTTP 200)`; (2) `ROW:` one coverage-map row `| Area | `knowledge/" + fname + "` (" + sid + ") | Coverage |` "
        "(Coverage >= 5 tokens, shares a 5+-letter word with the H1). Report sections: `ENTRY:` (the complete file in ONE fenced markdown block, "
        "verbatim as it should be committed), `GATE LINE:`, `ROW:`, `UNIT COUNTS:` (units per quote, computed with the unit rule), `RECHECK RUN:` "
        "(command and printed count), `OMITTED:` (page content you chose not to carry, with reason).")

# ---- C. frontier ground map (considerthese proposal 4) ---------------------------------------------
add("ScribeGroundMap", "scribe",
    f"Implements proposal 4 of `{LANE}/considerthese/2026-10-25.md` (read it): a running table of `PROVINCE.md` Frontier items against the rounds "
    f"and knowledge entries that entered them. Read `{LANE}/PROVINCE.md` (§Frontier lines 20-31 and the `## Round-NN ... frontier step` "
    f"sections), `{LANE}/corpus/README.md`, the knowledge file list `ls {KNOW}`, and `{LANE}/corpus/lessons/round-4[8-9].md round-5*.md`. Draft the "
    "body of a new README section `### Frontier ground map (round 55)`: a markdown table `| Frontier ground | Entered in round | Entries | Rows |` with one row per "
    "frontier ground you can evidence (rendering, crawl budget, canonical selection, crawler identity, per-engine hygiene Yahoo!/Baidu, base-path/Render/"
    "link-preview/security.txt/robots/sitemap steps, field performance, accessibility, etc.), the Entries cell using backticked `knowledge/<file>` paths that "
    "exist at the base revision (check each with `test -e`), the Rows cell using S### ids that exist in `corpus/SOURCES.md` (check each), and a final "
    "`Untouched ground` bullet list naming each PROVINCE frontier item no entry yet holds, with the PROVINCE line it came from. Also add a row for the round-55 "
    "Yahoo! JAPAN robots ground naming the three future paths `knowledge/yahoo-japan-robots-txt-refusal-rules.md`, `knowledge/yahoo-japan-robots-pattern-syntax.md`, "
    "`knowledge/yahoo-japan-robots-txt-basics.md` (S372 S373 S418) — mark that row `(lands this round)`. Report sections: `SECTION:` (one fenced markdown block), "
    "`PATH CHECK:` (each backticked path and S-id checked, with the command output), `UNEVIDENCED:` (grounds you could not date to a round).")

# ---- D. QUALITY / SKILL drafts ---------------------------------------------------------------------
add("ScribeQuality", "scribe",
    f"Draft a `## Round-55 criteria` block for `{LANE}/corpus/QUALITY.md` (read its last section `## Round-54 criteria` and the table style of earlier "
    f"sections, and `{LANE}/corpus/lessons/round-54-verifier-spotcheck.md`). Required rows, each `| Criterion | Admit | Reject | Grounding |` with a "
    "grounding that names a real file/lesson/commit: (1) coverage-map row at entry landing — an entry that lands without a README coverage-map row is an "
    "index claim left unwritten (grounding: base-revision counter `.ufo/waves/round-55/controls/base-c1-readme-index.txt`, 21 unindexed of 46); "
    "(2) a Gate quote and every quoted entry span is <= 25 units under the unit rule so no CJK word-segmentation ambiguity can arise (grounding: "
    "round-54 verifier-spotcheck routed defect 3, S367/S372/S373 at 31/27/27 units); (3) a held registry row reused by a new entry changes `used-by` only, "
    "logged old->new (grounding: CORPUS.md SOURCES rule 2); (4) a validated append block must be byte-identical to the appended one (grounding: counter "
    "condition C7 in `.ufo/waves/round-55/c55_quote_truth.py`). Also draft the `## Mistakes` rows for `corpus/lessons/round-55.md` (columns: class · evidence "
    "pointer · captured-by · fix) for: (a) index drift — 21 of 46 knowledge entries absent from the coverage map across rounds 21-54 (class `reference-drift`, captured-by `none`, fix = the C1 counter and criterion 1, shown able to fail by the base control exit 1) and (b) the round-54 single-wave shape "
    "(class `landing`; evidence `corpus/lessons/round-54-verifier-spotcheck.md` routed defect 1). Report sections: `CRITERIA:` (one fenced markdown block), "
    "`MISTAKES:` (one fenced markdown table), `GROUNDING CHECK:` (each cited path/commit verified to exist, with the command).")
add("ScribeSkillRegistry", "scribe",
    f"Draft a `### Round 55 gate registry additions` section for `{LANE}/SKILL.md`, copying the exact table schema and cell style of the section "
    f"`### Round 52 gate registry additions (r51 closure routed defect 1)` (find it with grep; read the two rows and the paragraph after them). Two rows: "
    "`readme-index-counter` (entry `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision <commit>`; verdict map 0 met / 1 not met / 2 could-not-evaluate / "
    "64 usage; self-test `--selftest` 10 fixtures; pinned: `contract.json`, base control receipt `.ufo/waves/round-55/controls/base-c1-readme-index.txt`; write scope none; owner kake) and "
    "`yahoo-robots-quote-truth-counter` (entry `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root . --revision <commit>`; `0=met` (`conditions_passed == 8 of 8`); self-test "
    "`--selftest` 30 fixtures; pinned: contract, retained-body receipts `.ufo/waves/round-55/sources/receipts.json`, mirror pin; write scope none; owner kake). Read both counters' docstrings and "
    "`--help` output first so the rows say what the code does. Report sections: `SECTION:` (one fenced markdown block), `CODE CHECK:` (each claim in the rows matched to a line of the counters).")

# ---- E. scouts -------------------------------------------------------------------------------------
for sid, body, url, name in (("S372", "S372.html", "https://info-search.yahoo.co.jp/archives/002849.php", "ScoutFreshS372"),
                             ("S373", "S373.html", "https://info-search.yahoo.co.jp/archives/002850.php", "ScoutFreshS373"),
                             ("S418", "S418.html", "https://info-search.yahoo.co.jp/archives/002885.php", "ScoutFreshS418")):
    add(name, "scout",
        f"Independent re-open of {sid}. Fetch `{url}` yourself now (plain GET, read-only, `curl -sSL`), compare its sha256 and byte length with the retained body "
        f"`{SRC}/{body}` and `{SRC}/receipts.json`, and report the match or the drift. Then, from your OWN fetch (not the retained file), locate the passages that "
        "carry the page's operative rules and report for each: the heading/section it sits under, the exact located quote (ASCII double quotes, <= 25 units, raw substring), "
        "its unit count, and a literal English reading that keeps every qualifier. Also list (a) the page's printed revision date (`更新日`), (b) every rule the page "
        "states that a publisher could get wrong, (c) any statement a plausible but careless gloss would add that the page does NOT make. Report sections: `FETCH:` "
        "(status, bytes, sha256, equality with retained), `LOCATED QUOTES:` (table), `RULES:`, `OVERREADS:`.")
add("ScoutScopeOverlap", "scout",
    f"PROVINCE.md scope check and overlap scan for three candidate entries (Yahoo! JAPAN robots.txt rules: refusal file placement/case-sensitivity/Allow; `*` and `$` "
    f"pattern syntax and prefix matching; what robots.txt is and when the crawler reads it). Read `{LANE}/PROVINCE.md` (§Core, §Frontier, §Adjacent, round-52 section), "
    f"`{LANE}/corpus/QUALITY.md` (round-50 and round-54 criteria, the `Replayable claim` / `Platform mechanism` rows), and the existing entries "
    f"`{KNOW}/robots-txt-rules.md`, `{KNOW}/crawl-scope-per-host.md`, `{KNOW}/yahoo-japan-rel-nofollow-semantics.md`, `{KNOW}/baidu-friendly-crawl-guidance.md`. "
    f"Also read the staged package notes `/home/vgpnk/Projects/shokuknow/merge/kake/MERGE-REPORT.md` (rows `yahoo-japan-robots-*`). For each candidate: in-scope or "
    "refuse (reason, flip condition), what the lane already holds that overlaps (file + line), what is new ground per the coverage map, and which existing entry must be "
    "cross-linked. Report sections: `SCOPE:` (per candidate), `OVERLAP:` (file:line pairs), `CROSS-LINKS:`, `RISKS:`. Evidence by file path and line; no web requests.")

# ---- F. connectors ---------------------------------------------------------------------------------
add("ConnectorSiblings", "connector",
    "Sibling-overlap scan (read-only). Siblings live at /home/vgpnk/Projects/shokunin/<id>-shokunin. Search for sibling-held ground that touches this round's "
    "topics: Yahoo! JAPAN info-search crawler pages (`info-search.yahoo.co.jp`), robots.txt Allow/Disallow semantics, `*`/`$` wildcard matching, robots.txt placement "
    "and consult order. Use `grep -rln` over each sibling's `corpus/knowledge`, `corpus/SOURCES.md`, `PROVINCE.md`. For each hit report sibling, file, whether it holds the "
    "same document (same URL) or only adjacent ground, and whether kake should cross-reference or leave it as the sibling's (adjacency rule: report, do not absorb). Also state "
    "whether kake's three candidate entries would duplicate any sibling entry. Report sections: `COMMAND LOG:` (each grep and its hit count), `HITS:` (table), "
    "`ADJACENCY CALLS:`. A negative claim carries its sweep command.")
add("ConnectorCrossClaim", "connector",
    f"Cross-claim pattern finder. Claims: C1 adds coverage-map rows to `{LANE}/corpus/README.md` for 21 existing knowledge files plus the three new Yahoo! robots entries; C2 "
    f"adds those three entries. Read `{W}/contract.md`, `{W}/c55_readme_index.py`, `{W}/c55_quote_truth.py` (docstrings and the condition code), and "
    f"`{LANE}/corpus/README.md` §Coverage map. Find: (1) interactions where one claim can break the other (e.g. new entries need rows or C1's counter fails; a README row quoting an "
    "entry text that C2's quote rule then constrains; anything that would make one claim unverifiable without the other landed); (2) repeated failure patterns across earlier rounds "
    f"(`{LANE}/corpus/lessons/round-5[0-4]-verifier-spotcheck.md`) that this round's design repeats or avoids, each with a file:line pointer; (3) README rows or existing entries that "
    "already cite S372/S373 or the Yahoo! pages and would need a pointer update. Report sections: `INTERACTIONS:`, `REPEATED PATTERNS:`, `POINTERS TO UPDATE:`.")

# ---- G. executors ----------------------------------------------------------------------------------
add("ExecBaseControls", "executor",
    f"Replicate the frozen base controls. Run, in `{LANE}` (read-only; the counters read committed bytes via git): "
    f"`python3 -B .ufo/waves/round-55/c55_readme_index.py --root {LANE} --revision fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`, "
    f"`python3 -B .ufo/waves/round-55/c55_quote_truth.py --root {LANE} --revision fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`, and "
    f"`python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest` (note `-B`; delete nothing, create no __pycache__). Diff each output against "
    f"`.ufo/waves/round-55/controls/base-c1-readme-index.txt`, `base-c2-quote-truth.txt`, `c1-selftest.txt`. Also run each counter once with `--json` and report whether the JSON "
    "parses and carries the frozen predicate string. Report sections: `COMMANDS:` (argv, exit, first and last 3 output lines each), `DIFFS:`, `JSON CHECK:`.")
add("ExecStagedQuoteAudit", "executor",
    f"Audit the staged package candidates against the retained bodies. For each of `{STAGED}/yahoo-japan-robots-txt-refusal-rules.md`, "
    f"`{STAGED}/yahoo-japan-robots-pattern-syntax.md`, `{STAGED}/yahoo-japan-robots-txt-basics.md` extract every double-quoted span >= 6 units and every `grep -F` string in "
    f"its `recheck:` line, and test each against the matching retained body (`{SRC}/S372.html`, `S373.html`, `S418.html`) with a python script (unit rule: one per CJK character, one per "
    "non-CJK whitespace token). Report per span: units, raw-substring yes/no, and whether it exceeds 25 units; also run each staged `recheck` grep against the retained body and "
    "print the count. Do not modify any file in shokuknow. Report sections: `SCRIPT:` (the python you ran, inline), `RESULTS:` (table), `SUMMARY:` (spans, over-ceiling count, non-substring count).")
add("ExecIdGuard", "executor",
    f"Replicate the assimilation id-collision guard and the quarantine slice from scratch. In your own `mktemp -d` scratch: build registry ids from `{LANE}/corpus/SOURCES.md` and staged ids from "
    "`/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` with `grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]+' | sort`, compute the intersection with `comm -12`, "
    f"and compare with `{W}/assimilation/{{reg-ids,staged-ids,collisions}}` (counts and bytes). Prove the guard on a scratch registry containing the indented row `  | S287 | x |` "
    f"(0-3 leading spaces): the 0-3-space pattern must report S287 and a column-zero-only pattern must report nothing; compare with `{W}/assimilation/guard-proof/`. Derive the "
    "kake quarantine slice from `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` with the awk in this round's prompt "
    "(`awk -F'|' -v l='kake' '$2 ~ (\"`\" l \"`\") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'`) and compare with `quarantine-slice`. Finally state which collision ids are the "
    "SAME document in both registries (compare the URL cell of each colliding row in the lane registry vs the staged row) and which are different documents — the renumber map is "
    "only legitimate for different documents. Report sections: `COMMANDS:`, `COMPARISON:`, `GUARD PROOF:`, `SAME-DOCUMENT TABLE:`.")

# ---- H. pre-data attacks ---------------------------------------------------------------------------
add("CriticC1Contract", "critic",
    f"Attack claim C1 BEFORE any build. Read `{W}/contract.md` and `{W}/c55_readme_index.py`. Find a do-nothing or junk change that meets `met: index_mismatches == 0 AND "
    "knowledge_files >= 46` without a real calibration improvement (e.g. rows that name a file but say nothing true; a README section that is not the coverage map; renaming/moving "
    "entries; a coverage map that is correct only because the population shrank or grew; token-overlap gaming), and a real improvement the predicate would wrongly reject. For each "
    "attack give the minimal fixture (file contents) and whether the committed selftest already kills it. Also assess whether the universal/negative clauses in the contract are backed by a "
    "counting command. Report sections: `ATTACKS:` (each: input, predicted exit, covered by selftest yes/no), `WRONG-REJECT:`, `RECOMMENDED CONTRACT/COUNTER CHANGES:` (before data).")
add("CriticC2Contract", "critic",
    f"Attack claim C2 BEFORE any build. Read `{W}/contract.md` and `{W}/c55_quote_truth.py` (all eight conditions). Find a do-nothing or junk change that reaches "
    "`conditions_passed == 8 of 8` without three truthful, re-grounded entries (e.g. an entry whose every quote is a trivial 6-unit span; quotes that are substrings but "
    "mis-glossed; a receipt for a body that is not the page; a validated mirror that is not the appended block; a mirror that equals base but registry edits outside the adopted rows; "
    "S418 pointing at a different document) and a truthful improvement the counter would wrongly reject (e.g. the held rows S372/S373 `used-by` ordering, the entry quoting with curly "
    "quotes, `[INFERENCE]` lines). Give the minimal fixture per attack and whether the selftest list (see `cases` in `selftest()`) already covers it. Report sections: `ATTACKS:`, "
    "`WRONG-REJECT:`, `RECOMMENDED COUNTER CHANGES:` (each with the exact condition and line).")
add("MutC1Counter", "mutation-tester",
    f"Mutation-test the C1 counter and its selftest. Copy `{W}/c55_readme_index.py` to a scratch dir (`mktemp -d`), then apply >= 12 single-point mutants (e.g. flip `>= FLOOR`, drop the "
    "`(?![A-Za-z0-9_.-])` boundary, remove the thin word-overlap clause, remove brace expansion, change `< 5` token threshold, make dangling always empty, make `unindexed` skip .json, "
    "read the working tree instead of `git show`, section regex matching any `## ` heading, etc.) and run the scratch copy's `--selftest` for each. Report which mutants the selftest "
    "KILLS (selftest exit != 0) and which SURVIVE; for each survivor give a fixture that would kill it. Do not edit the original. Report sections: `MUTANTS:` (table: id, change, selftest "
    "result), `SURVIVORS:`, `PROPOSED FIXTURES:`.")
add("ReviewerC2CounterCode", "reviewer",
    f"Code-review `{W}/c55_quote_truth.py` for logic defects before the claim is measured: especially C3 (cell comparison `row[:10] != base[:10]`), C4 ordering, C5 quote extraction "
    "(regex over ASCII double quotes; multi-quote lines; `[INFERENCE]` skip), C6 (UTC date vs round date), C7 (comparing scratch rows with landed rows; `row_lines` regex), C8 "
    "(`set_used_by` and the restoration loop; trailing-newline handling; a registry whose last line has no newline), and the selftest builder `_build` (global BASE_REV mutation, "
    "fixture commit ordering). For each defect give the line, a failing input, and the fix. Mark each finding `confirmed by running` only if you ran an input; otherwise "
    "`[INFERENCE]`. Report sections: `FINDINGS:` (severity, line, input, fix), `NO-DEFECT CHECKS:`.")

SPEC = {"reportDir": ".ufo/waves/round-55/w1", "maxLanes": 64, "context": CONTEXT, "items": items}
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
    json.dump(SPEC, open(out, "w"), indent=1, ensure_ascii=False)
    from collections import Counter
    print(len(items), dict(Counter(i["role"] for i in items)))
