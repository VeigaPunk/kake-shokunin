#!/usr/bin/env python3
"""Round-50 wave-1 spec generator.

Emits `.ufo/waves/round-50/w50-spec.json` — one v1 wave of 36 seats under
`scripts/hyaku/ufo-wave-policy.json` (band 32-64). Strict attack roles are
reviewer + critic + mutation-tester; they must be >= 25 percent of the wave.
The planner seat is frozen topology and is held by the L1, not by a seat.

Usage: python3 -B make_spec_w1.py <pre_rev>
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"
BASE = "9619af67c52939daac502ca7a24c9d714f3f51db"

DIRECTIVE = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can be run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""


def context(pre_rev: str) -> str:
    return f"""# Goal
Kake round 50, wave 1. You are one leaf seat in a 36-seat batch. The L1 holds the planner seat.
The two claims were declared and frozen BEFORE any score, in `{LANE}/.ufo/waves/round-50/contract.json`:

  C1 (freshness, capability) — quote class, committed bytes only.
     Predicate: `met: classed == 3 of 3 declared ids` (S273, S274, S286).
     Counting command: `python3 -B {LANE}/.ufo/waves/round-50/c50_quote_class.py --root {LANE} --revision <commit>`
  C2 (operability) — pre-append order proof and wave-grant durability.
     Predicate: `met: durable == 1 of 1`.
     Counting command: `python3 -B {LANE}/.ufo/waves/round-50/c50_durable.py --root {LANE} --revision <commit>`

Base (do-nothing) revision: {BASE}
Pre-append revision (mirror committed, live registry still without S286): {pre_rev}
Lane root: {LANE}
Fleet root: {FLEET}

# Counting commands (run them; do not reason about them)
`python3 -B {LANE}/.ufo/waves/round-50/c50_quote_class.py --root {LANE} --revision {BASE}`
`python3 -B {LANE}/.ufo/waves/round-50/c50_quote_class.py --root {LANE} --revision {pre_rev}`
`python3 -B {LANE}/.ufo/waves/round-50/c50_durable.py --root {LANE} --revision {BASE}`

# Bounds
Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.
Never mutate the fleet repo, a sibling lane, the lane jj state, or the lane Git index. Do not run `git add`, `git commit`, `git stash`, `git checkout`, `git switch`, `git reset`, `git pull`, `git push`, or any mutating `jj` command. Read-only git (log, show, diff, status, ls-files, rev-parse, merge-base, cat-file) is fine.
Do not edit any production file in the lane: `corpus/SOURCES.md`, `corpus/lessons/round-50.md`, `corpus/knowledge/crawl-error-status-table.md`, `SCORECARD.md` and `LOG.md` are the L1's. Write scratch under `/tmp` only.
Do not edit `{LANE}/considerthese/` — it is operator-authored input.
Do not touch `{LANE}/.ufo/waves/round-46/residual/` (eight orchestrator-owned reports) or the nine `>1MiB` copies under `{LANE}/.ufo/waves/round-48/assimilation/validate/`. They stay uncommitted.
Read-only external: `{FLEET}/../shokuknow/merge/kake/` and `{FLEET}/../shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`. Never write there, never run a campaign tool there.
Publishing stays operator-owned. Do not publish, deploy, or touch an owned property.
Tool installs and updates need genuine need and require reading `/home/vgpnk/.omp/agent/RULES.md` first. ALL PACMAN TRANSACTIONS ARE PAUSED HOST-WIDE: never run `pacman -S`, `-Sy`, `-Syu`, `-U`, `-R`, never downgrade, never restart a host service. Use `uv tool`/`npx`/an official binary in `~/.local/bin` or file an L0 question. You should not need a new tool.
One public GET of a documentation URL is allowed; do not fetch an owned property.
Godspeed directive bytes follow the leading `/skill:godspeed` line in your item prompt; do not paraphrase them.
"""


def I(name, role, axes, item):
    return {"name": name, "role": role, "axes": axes, "item": item}


TEMPLATE = (
    "/skill:godspeed\n"
    + DIRECTIVE
    + "\n\n{{item}}\n\n"
    + "The item names the only file you may write. Report trailers are relative to "
    + LANE
    + ".\n"
)


def build_items(pre_rev: str) -> list:
    w1 = f"{LANE}/.ufo/waves/round-50/w1"
    return [
        # ---- scouts: reconnaissance and source re-opening ----
        I("ScoutReopenS286", "scout", ["freshness"],
          "Re-open https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors with one curl GET. Report the HTTP status, the byte size, whether the frozen quote \"Googlebot will scale back its crawling if it detects that your servers are having trouble\" is a RAW substring of the fetched body, and whether it survives whitespace collapse. State the class you derive. Do not write the body into the lane repo. Write ONLY " + w1 + "/ScoutReopenS286.md"),
        I("ScoutReopenS273", "scout", ["freshness"],
          "Re-open https://developers.google.com/crawling/docs/crawl-budget with one curl GET. Report the HTTP status, the byte size, whether the frozen S273 quote is a RAW substring of the fetched body (expected false) and whether it is a substring of the whitespace-collapsed body (expected true). State the class you derive. Do not write the body into the lane repo. Write ONLY " + w1 + "/ScoutReopenS273.md"),
        I("ScoutReopenS274", "scout", ["freshness"],
          "Re-open https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate with one curl GET. Report the HTTP status, the byte size, and whether the frozen S274 quote is a RAW substring of the fetched body. State the class you derive. Do not write the body into the lane repo. Write ONLY " + w1 + "/ScoutReopenS274.md"),
        I("ScoutQuarantineSlice", "scout", ["freshness"],
          "Re-derive the lane's quarantine slice read-only from /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md with this exact filter: awk -F'|' -v l='kake' '$2 ~ (\"`\" l \"`\") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'. Report the row count, every id and its class cell, and whether any of those ids is present in the lane's live registry " + LANE + "/corpus/SOURCES.md. Do NOT fetch any of the cited sources and do NOT append anything. Write ONLY " + w1 + "/ScoutQuarantineSlice.md"),
        I("ScoutUncommitted", "scout", ["calibration"],
          "Run `git -C " + LANE + " status --porcelain` and `git -C " + FLEET + " status --porcelain` (read-only, no pathspec). Report every path, classified as (a) round-50 lane-authored work, (b) inherited orchestrator-owned round-46 residual reports, (c) inherited >1MiB round-48 validate copies, (d) operator or driver runtime, (e) a possible misroot at the fleet root. Report the exact count in each class and name any file that a round-50 seat wrote into the fleet root. Write ONLY " + w1 + "/ScoutUncommitted.md"),
        # ---- executors: run the frozen counters and the census ----
        I("ExecCensusMirror", "executor", ["freshness"],
          "Re-run the pre-append census against the mirror: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file " + LANE + "/.ufo/waves/round-50/assimilation/pre-append/corpus/SOURCES.md`. Paste the FULL stdout and the exit code. Then run the same census with `--root " + FLEET + " kake` and paste the FULL stdout and the exit code. Report every finding the mirror introduces beyond the lane tip, and state explicitly whether any E03 or E04 appears. Do not modify anything. Write ONLY " + w1 + "/ExecCensusMirror.md"),
        I("ExecCensusLive", "executor", ["freshness"],
          "Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root " + FLEET + " kake` and paste the FULL stdout and the exit code. Count the registry rows in " + LANE + "/corpus/SOURCES.md with `grep -cE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}'` and report the number. Report whether S286 is in the live registry at this moment. Write ONLY " + w1 + "/ExecCensusLive.md"),
        I("ExecRerunC1Base", "executor", ["freshness"],
          "Run `python3 -B " + LANE + "/.ufo/waves/round-50/c50_quote_class.py --root " + LANE + " --revision " + BASE + "` and paste the EXACT stdout and the exit code. Report the classed count and, per id, the reason it fails. This is the do-nothing control; it must not be met. Write ONLY " + w1 + "/ExecRerunC1Base.md"),
        I("ExecRerunC1Pre", "executor", ["freshness"],
          "Run `python3 -B " + LANE + "/.ufo/waves/round-50/c50_quote_class.py --root " + LANE + " --revision " + pre_rev + "` and paste the EXACT stdout and the exit code. Report which ids are classed, which are not, and the exact reason for each unclassed id. Write ONLY " + w1 + "/ExecRerunC1Pre.md"),
        I("ExecRerunC2Base", "executor", ["operability"],
          "Run `python3 -B " + LANE + "/.ufo/waves/round-50/c50_durable.py --root " + LANE + " --revision " + BASE + "` and paste the EXACT stdout and the exit code. Report the durable count and every reason. This is the do-nothing control; it must not be met. Write ONLY " + w1 + "/ExecRerunC2Base.md"),
        I("ExecCensusParse", "executor", ["freshness"],
          "Re-derive the registry id list with the census parser's OWN pattern, which accepts 0 to 3 leading spaces: `grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' " + LANE + "/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort`. Report the id count, any duplicate ids (`sort | uniq -d`), and the intersection with the staged ids of /home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md computed the same way with `comm -12`. Then repeat the intersection with a column-zero-only pattern `^\\|` and report whether that pattern MISSES any collision. Write ONLY " + w1 + "/ExecCensusParse.md"),
        # ---- scribes: prose and row shape ----
        I("ScribeGateQuotes", "scribe", ["freshness"],
          "Read " + LANE + "/corpus/lessons/round-50.md and report: the exact quote string recorded for S286 in the ## Gate block, its word count, and the exact class sentences recorded for S273, S274 and S286. Compare each of the three quote strings byte for byte with the frozen quote in " + LANE + "/.ufo/waves/round-50/quote-classes.json and report any difference character by character. Write ONLY " + w1 + "/ScribeGateQuotes.md"),
        I("ScribeRowShape", "scribe", ["freshness"],
          "Read the S286 row in " + LANE + "/.ufo/waves/round-50/assimilation/pre-append/corpus/SOURCES.md and report: the number of pipe-separated cells, and the status, opened, recheck and used-by cells verbatim. State whether any cell contains a literal or escaped pipe. Then compare that row cell by cell with the staged S286 row in /home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md and list every cell that changed, old value to new value. Write ONLY " + w1 + "/ScribeRowShape.md"),
        I("ScribeLessonShape", "scribe", ["calibration"],
          "Read " + LANE + "/corpus/lessons/round-50.md and report whether it satisfies the round's frontier-step shape: a ## Gate block recording this round's access date and a located quote of at most 25 words for each admitted row, at least one REJECT with a reason and a flip condition, the stripped recheck prose, the used-by old-to-new change, and a ## Mistakes block whose rows each carry class, evidence pointer, captured-by and fix. Name the first missing or malformed element if any. Write ONLY " + w1 + "/ScribeLessonShape.md"),
        I("ScribeConsider", "scribe", ["calibration"],
          "Read " + LANE + "/considerthese/2026-10-24.md (READ ONLY — never edit it). Report the full list of proposals under 'Self-improvement proposals (not acted on)', which single proposal this round's lesson mined, and whether that proposal is implemented anywhere in the lane today (search the lane for it). Report the exact file and date you cite. Write ONLY " + w1 + "/ScribeConsider.md"),
        # ---- reviewers: independent checks of the claimed surfaces ----
        I("ReviewClassLedger", "reviewer", ["freshness"],
          "Review " + LANE + "/.ufo/waves/round-50/quote-classes.json against the committed blobs. For each of S273, S274 and S286 recompute sha256 of the text blob and the raw blob with `git -C " + LANE + " show <rev>:<path>` (S273 and S274 from .ufo/waves/round-49/sources/, S286 from .ufo/waves/round-50/sources/), recompute the derived class from the two blobs, and report whether each ledger row's pins and its recorded matchClass match your recomputation. Report every mismatch with the expected and the actual value. Write ONLY " + w1 + "/ReviewClassLedger.md"),
        I("ReviewOrderProof", "reviewer", ["operability"],
          "Read " + LANE + "/.ufo/waves/round-50/c50_durable.py and state, for each of its eleven numbered conditions, whether it can be satisfied by an artifact that does NOT carry the claimed evidence. Name the cheapest artifact that satisfies the whole predicate while skipping the claimed work (a do-nothing control), and say which single condition blocks it. Report per condition. Write ONLY " + w1 + "/ReviewOrderProof.md"),
        I("ReviewEntryCite", "reviewer", ["freshness"],
          "Read " + LANE + "/corpus/knowledge/crawl-error-status-table.md and the S286 row. Report whether the entry's source/verified-at/recheck header is lane-shaped, whether the entry cites S286 below its 8-line header (count the lines), whether any sentence in the entry asserts more than the located quote supports, and whether the entry crosses the lane's province. Quote the offending sentence if there is one. Write ONLY " + w1 + "/ReviewEntryCite.md"),
        I("ReviewReportContract", "reviewer", ["calibration"],
          "Read section 4 of " + FLEET + "/.ufo/prompts/kake-round-50.md and report every required report section in the required order, the marker rule's contentless conditions, and which sections are conformance-only rather than marker predicates. Then read " + LANE + "/SCORECARD.md's last two round sections and report the exact row shape the lane uses for a declared-claim table and a measured-results table, so the round-50 rows can match it. Write ONLY " + w1 + "/ReviewReportContract.md"),
        I("ReviewShonen", "reviewer", ["calibration"],
          "Read " + LANE + "/SHONEN.md and report, per box, the mark the author may honestly write this round given that no non-author verifier is bound to this round, and whether any [x] would be self-awarded. Report which boxes a non-author reviewer could check and what evidence each would need. Do not edit SHONEN.md. Write ONLY " + w1 + "/ReviewShonen.md"),
        # ---- critics: falsify the frozen claims ----
        I("CriticSwappedLabel", "critic", ["freshness"],
          "Attack C1's predicate by label. In /tmp build a copy of " + LANE + "/.ufo/waves/round-50/quote-classes.json with S286's matchClass changed from raw-substring to collapsed-only, and a copy of the lesson with the S286 class sentence changed to match. Score both with the frozen counter (`python3 -B " + LANE + "/.ufo/waves/round-50/c50_quote_class.py --root <your-tmp-repo> --revision <your-tmp-rev>` or by importing its run() with the lesson blob replaced). Paste the counter's stdout and exit codes. Report whether a WRONG class can be met. Write ONLY " + w1 + "/CriticSwappedLabel.md"),
        I("CriticCrossWire", "critic", ["freshness"],
          "Attack C1 by cross-wiring. In /tmp swap the S273 and S274 quotes, and their text and raw blob paths, between the two ledger rows, and score with the frozen counter. Paste the stdout and the exit code. Report whether the counter detects the swap; if it does not, name exactly which rule failed to fire and why. Write ONLY " + w1 + "/CriticCrossWire.md"),
        I("CriticPredicateSizing", "critic", ["calibration"],
          "Attack both frozen predicates against the claim-sizing rule in " + FLEET + "/.ufo/prompts/kake-round-50.md section 9: is each declared after-state ONE concrete value a closure can re-derive with one command over committed bytes, does each have a do-nothing control that cannot reach it, and does either use a universal clause its counting command does not enumerate? Read the contract at " + LANE + "/.ufo/waves/round-50/contract.json and both counters. Report a verdict per claim and the exact fix if either fails. Write ONLY " + w1 + "/CriticPredicateSizing.md"),
        I("CriticExpandCredit", "critic", ["calibration"],
          "Test the expansion-credit rule against this round's plan. Read the coverage map in " + LANE + "/corpus/README.md and the held entries it names, and decide whether the crawl-error-status ground (what an error status does to crawling) is ground the lane did NOT hold. Report the verdict with the entries you checked and the exact map rows you read. Write ONLY " + w1 + "/CriticExpandCredit.md"),
        I("CriticProvince", "critic", ["adjacency"],
          "Read the staged entry corpus/knowledge/ollama-openapi-contract.md under /home/vgpnk/Projects/shokuknow/merge/kake/knowledge/, kake's PROVINCE.md Adjacent section, and kama's PROVINCE.md at " + FLEET + "/kama-shokunin/PROVINCE.md. Report whether the staged entry is in kake's province, the flip condition, and whether the round's refusal of it is correct. Write ONLY " + w1 + "/CriticProvince.md"),
        # ---- mutation testers: kill the predicates with mutants ----
        I("MutationDropSha", "mutation-tester", ["freshness"],
          "Mutation-test C1. In /tmp remove the sha256 pins from a copy of the class ledger and score it with the frozen counter; paste the stdout and the exit code and name the rule that fired. Then remove the matchClass field instead and score again. Report whether each mutant is rejected and which rule rejects it. Write ONLY " + w1 + "/MutationDropSha.md"),
        I("MutationWrongPath", "mutation-tester", ["freshness"],
          "Mutation-test C1's per-id binding. In /tmp point S286's textPath and rawPath at S274's committed blobs, and separately point S273's textPath at S274's, and score each with the frozen counter. Paste the stdout and the exit code for each mutant and name the rule that fired. Report whether the counter can be met by an id that points at another id's bytes. Write ONLY " + w1 + "/MutationWrongPath.md"),
        I("MutationGrantDrop", "mutation-tester", ["operability"],
          "Mutation-test C2. In /tmp build three mutants of the lane's committed artifacts: (1) wave-grant.txt absent, (2) dispatch-command.txt containing the token --auto, (3) LOG.md citing the wave before the grant commit. Score each with the frozen counter `python3 -B " + LANE + "/.ufo/waves/round-50/c50_durable.py --root <your-tmp-repo> --revision <your-tmp-rev>`. Paste each stdout and exit code and name the condition that rejected the mutant. Report whether C2 rejects all three. Write ONLY " + w1 + "/MutationGrantDrop.md"),
        I("MutationOrderSwap", "mutation-tester", ["operability"],
          "Mutation-test C2's order rule. In /tmp swap the roles of the pre-append mirror and the live registry (a mirror WITHOUT S286, a live registry WITH S286) and score with the frozen counter. Paste the stdout and the exit code, name the condition that fired, and report whether the counter can be met by a registry that was appended before the mirror was committed. Write ONLY " + w1 + "/MutationOrderSwap.md"),
        # ---- sentinels: bounds and trust boundary ----
        I("SentinelBounds", "sentinel", ["operability"],
          "Audit the trust boundary of the two round-50 counters " + LANE + "/.ufo/waves/round-50/c50_quote_class.py and c50_durable.py: which files do they read, do they run git inside the lane checkout, do they write anything, could they read a secret or credential path, and what happens if the lane path is a different repository. Report the narrowest safe scope and every concrete failure scenario you find. Write ONLY " + w1 + "/SentinelBounds.md"),
        I("SentinelWriteScope", "sentinel", ["calibration"],
          "Audit write scope for this round. Run `git -C " + LANE + " status --porcelain` and `git -C " + FLEET + " status --porcelain` (read-only). Report every path, and name anything a round-50 seat wrote outside its own report file, especially anything at the fleet root. Do not delete or modify anything. Write ONLY " + w1 + "/SentinelWriteScope.md"),
        I("SentinelLargeFiles", "sentinel", ["calibration"],
          "Check the round's evidence sizes: report the byte size of every file under " + LANE + "/.ufo/waves/round-50/ and flag any file above 1 MiB. Confirm by listing the nine inherited >1MiB copies under " + LANE + "/.ufo/waves/round-48/assimilation/validate/ and the eight reports under " + LANE + "/.ufo/waves/round-46/residual/ that must stay uncommitted. Do not modify or delete any of them. Write ONLY " + w1 + "/SentinelLargeFiles.md"),
        # ---- revengers: reconstruct the routed defects ----
        I("RevengerR49", "revenger", ["calibration"],
          "Reconstruct what round 49 landed and what its verifier routed. Read " + LANE + "/corpus/lessons/round-49-verifier-spotcheck.md, list its three routed defects, then read this round's frozen contract " + LANE + "/.ufo/waves/round-50/contract.json and both counters. Report, per routed defect, whether this round's frozen instrument would ACTUALLY catch it, with the concrete condition or rule number that does the catching, or state plainly that it would not. Write ONLY " + w1 + "/RevengerR49.md"),
        I("RevengerR48", "revenger", ["calibration"],
          "Reconstruct the round-48 hand-check of the 12 quarantine ids. Read " + LANE + "/corpus/lessons/round-48.md and the round-48 wave reports under " + LANE + "/.ufo/waves/round-48/ and report which of the 12 ids were actually re-fetched with a located quote in round 48, with the file that proves it per id. Report whether this round's adoption of NONE of them is consistent with the round-49 verifier's routed defect 2. Write ONLY " + w1 + "/RevengerR48.md"),
        # ---- connector and simplifier ----
        I("ConnectorSiblingOverlap", "connector", ["adjacency"],
          "Sibling-overlap scan, read-only: check whether sibling lane repos under " + FLEET + "/ hold the crawl-error-status ground (error status codes, soft 404, 5xx and crawl rate). Look at their PROVINCE.md and their corpus/knowledge listings. Report which lane owns which surface, whether this round's theme is contested, and the exact paths you checked. Write ONLY " + w1 + "/ConnectorSiblingOverlap.md"),
        I("SimplifierCounters", "simplifier", ["calibration"],
          "Simplify-attack the two round-50 counters. Report the SHORTEST implementation that meets each frozen predicate without doing the claimed work — for example a counter that always returns met=True, or one that checks only the lesson sentence and never the blobs. Score each shortcut with the frozen counter and report whether the predicate is met by the shortcut. Then say which ONE added rule would kill both shortcuts without changing the predicate sentence. Write ONLY " + w1 + "/SimplifierCounters.md"),
    ]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: make_spec_w1.py <pre_rev>", file=sys.stderr)
        return 64
    pre_rev = sys.argv[1]
    items = build_items(pre_rev)
    if len(items) != 36:
        print(f"refusing: {len(items)} items, expected 36", file=sys.stderr)
        return 64
    names = [i["name"] for i in items]
    if len(set(names)) != len(names):
        print("refusing: duplicate seat name", file=sys.stderr)
        return 64
    texts = [i["item"] for i in items]
    if len(set(texts)) != len(texts):
        print("refusing: duplicate item text", file=sys.stderr)
        return 64
    roles = {}
    for i in items:
        roles[i["role"]] = roles.get(i["role"], 0) + 1
    strict = {"reviewer", "critic", "mutation-tester"}
    attack = sum(v for k, v in roles.items() if k in strict)
    print("roles:", roles, "strict-attack:", attack, f"({attack}/{len(items)})")
    if attack * 100 < 25 * len(items):
        print("refusing: attack share below 25 percent", file=sys.stderr)
        return 64
    for frozen in ("planner", "distiller", "labrat", "main"):
        if frozen in roles:
            print(f"refusing: frozen-topology role {frozen}", file=sys.stderr)
            return 64
    spec = {
        "wave": "kake-r50-w1",
        "milestone": "Round 50 wave 1: build and attack the frozen quote-class and order-durability instruments, plus the frontier step and the item-10 assimilation contract",
        "maxLanes": 36,
        "axes": ["freshness", "operability"],
        "reportDir": ".ufo/waves/round-50/w1",
        "context": context(pre_rev),
        "template": TEMPLATE,
        "items": items,
    }
    out = os.path.join(HERE, "w50-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("wrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
