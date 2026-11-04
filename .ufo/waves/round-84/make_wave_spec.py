#!/usr/bin/env python3
"""Emit the round-84 w1 wave spec (13 seats) as JSON."""
import json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W = f"{LANE}/.ufo/waves/round-84"
FREEZE = "f358022f7e1b2f3846be8ceacbe3a7ef22edf4be"
BASE = "fe42ad11eb1084ad2ea68d12c5bbb2922a089868"

CONTEXT = f"""/skill:godspeed

You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

kake lane, round 84, attempt 1, wave w1. Lane checkout: {LANE}. Base revision `{BASE}` (lane `master` tip at round open, 2026-11-04); round freeze `{FREEZE}`. The freeze carries the contract (`{W}/contract.md`), both counters, the frozen control pairs, the expectations file and the base receipts — read the contract first.

YOU ARE ONE SEAT OF ONE WAVE. Two claims are frozen. **C1** (calibration, the lowest non-retired axis) closes the four routed defects D1..D4 filed by `{LANE}/corpus/lessons/round-83-verifier-spotcheck.md` §6, decided by `python3 -B {W}/c84_defect_queue.py --root <tree> [--revision <rev>]`. **C2** (freshness, capability acquisition) classifies a changed `policy`-class response header's VALUE, decided by `python3 -B {W}/c84_policy_values.py --root <tree>`, whose instrument is `{LANE}/scripts/policy_value_class.py` specified in the contract §C2.

## Hard rules for every seat
1. **Absolute paths only.** Your tools start at the fleet root, not the lane. Every read, edit, write and command names absolute paths under {LANE}. The validator trailer prints `Report: .ufo/waves/round-84/w1/<Name>.md` — every `Report:` trailer path is relative to {LANE}, so write it at {LANE}/<that path>.
2. **Write scope.** You may write only inside {LANE} (the production files named in your item plus your own report and receipts under `{W}/w1/`). Never write or mutate the fleet repo `/home/vgpnk/Projects/shokunin` (no `.ufo/state/`, no `.ufo/watchdog.log`, no `.scratch/`, no `MANIFEST.json`), never write a sibling repo `/home/vgpnk/Projects/shokunin/*-shokunin/`, never edit `considerthese/` and never edit `corpus/SOURCES.md` unless your item names it.
3. **No VCS mutation.** Never run `git commit`, `git add`, `git stash`, `git checkout`, `git switch`, `git reset`, `git pull`, `git push`, or any mutating `jj` command. Read-only git (`log`, `show`, `diff`, `status`, `ls-tree`, `cat-file`, `rev-parse`) is fine; jj only with `--ignore-working-copy`. The L1 is the only committer.
4. **Never rewrite the frozen files.** `{W}/contract.md`, `{W}/c84_defect_queue.py`, `{W}/c84_policy_values.py`, `{W}/build_control_pairs.py`, `{W}/policy-expectations.json` and `{W}/controls/*` are frozen at the freeze commit: read them, never edit them. A defect you find is reported, not patched.
5. **Fixture git (run-6 fleet incident).** Any fixture repo is created as `D=$(mktemp -d) && git -C "$D" init -q`; every later git call names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit. Never commit with a throwaway identity anywhere else.
6. **Scratch.** All clones, mirrors, fixtures and counter work dirs live under `/fast/scratch/hyaku/kake-r84/<your-seat-name>/`, created with `mkdir -p` and passed explicitly (`TMPDIR=...`, `--work ...`, `mkdtemp(dir=...)`). Never rely on an inherited TMPDIR and never root scratch in `/tmp` (files under 50 MB excepted). Delete your scratch dir before you yield (`trap 'rm -rf -- "$S"' EXIT` or `finally: shutil.rmtree`); copy receipts into `{W}/w1/<Seat>/` first. A seat that leaves its tree behind reports that as its own defect.
7. **No network beyond your item.** Only a seat whose item names a URL may open a socket; GET-only, no credentials, no cookies, no POST. No publish, deploy, DNS, account or browser action anywhere.
8. **Depth.** An executor seat may spawn at most one read-only `labrat` probe for one falsifiable hypothesis. Every other role is a leaf. No seat runs its own swarm.
9. **Tooling authorization (operator, 2026-10-19).** You may install or upgrade tools that help the task: read `/home/vgpnk/.omp/agent/RULES.md` first (official channels, update-safety gate); record tool, version, channel and reason in your report. **pacman is PAUSED host-wide** (orchestrator ruling 2026-10-20): install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or file an L0 question — never `pacman -S`/`-Sy`/`-Syu`/`-U`/`-R`.
10. **Honesty.** An unrun check has not passed. Report dead ends, partial reads and surprise findings; never fabricate output or a verdict. Do not edit a file another item owns; report the conflict instead.
11. **Your report is the deliverable.** Write `{W}/w1/<Seat>.md` BEFORE you yield, at least ~20 substantive lines, with the commands you ran and their exit codes plus a `## Verdict` line. An empty output row is a dead seat and a defect of this round: if you cannot finish, write what you have and name the blocker.
12. **Report format.** Your report starts with `# <Seat> — round 84 wave w1` and must not restate this context. Receipts go under `{W}/w1/<Seat>/`.

Scratch for this seat: `/fast/scratch/hyaku/kake-r84/<your-seat-name>/`.
"""

TOOL_SPEC = """Write the production tool {lane}/scripts/policy_value_class.py exactly to the frozen CLI contract in {w}/contract.md §C2 ("The tool's frozen CLI"):

- imports the class table from the sibling module (`from header_change_class import POLICY, header_class, canonical, load_surface, declared_surfaces` via `sys.path.insert(0, str(Path(__file__).resolve().parent))`), never copies it;
- CLI: `policy_value_class.py --a <capture-dir> --b <capture-dir> --declared <json>` and `--selftest [--work <dir>]`; exit 0 printed, 1 unevaluable input, 64 usage;
- for every declared surface, every response header whose class is `policy` and whose canonical value differs between the two sides is a changed policy header; print one `change surface=<id> header=<lowercased name> class=<value-level class>` line per changed header, sorted by (surface, header), then one `surface=<id> changed=<k> reordered=<a> numeric_parameter=<b> directive_added=<c> directive_removed=<d> directive_changed=<e> header_added=<f> header_removed=<g> unclassified=<h> verdict=<v>` line per declared surface in declaration order, then one `summary surfaces=<n> <same keys> verdict=<v>` line;
- value grammar: comma-separated `name[=parameter]`, name lowercased, parameter trimmed and lowercased; class table and verdict rule exactly as the contract freezes them (`reordered`, `numeric_parameter`, `directive_added`, `directive_removed`, `directive_changed`, `header_added`, `header_removed`, `unclassified`; verdict order `policy-unchanged < policy-rewritten-equivalent < policy-changed < policy-unclassified`);
- offline by construction: no `socket`, `urllib`, `requests` or `http.client` import anywhere outside the module docstring;
- `--selftest` builds fixtures in `--work` (or a temp dir) and covers every class, the reordered-only pair, and one receipt fault; prints `selftest: <n>/<n> passed`, exit 0 iff all pass.

Then run it and write these receipts (byte-exact stdout plus the exit code):
- `{w}/controls/tool-real-pair.txt` — `--a {lane}/.ufo/waves/round-81/capture --b {lane}/.ufo/waves/round-82/capture --declared {lane}/.ufo/waves/round-81/capture-expectations.json` (the committed record the counter compares byte-for-byte);
- `{w}/controls/tool-ctl-control.txt` — the `control` pair under `{w}/capture-control/control/{{a,b}}`;
- `{w}/controls/tool-ctl-equivalent.txt` — the `equivalent` pair;
- `{w}/controls/tool-selftest.txt` — the `--selftest` run.
Report every line the tool prints for the three data runs and state which expected class each changed header landed in versus `{w}/policy-expectations.json`."""

ITEMS = [
    {
        "name": "ScoutRecon",
        "role": "scout",
        "item": f"""Read-only recon of the round-84 C1 queue at the freeze revision, plus the bounded planning data-walk the round's L1 planner seat maps onto a scout. Report `{W}/w1/ScoutRecon.md`, notes under `{W}/w1/ScoutRecon/`. Write no production file.
1. Read `{LANE}/corpus/lessons/round-83-verifier-spotcheck.md` §6 and restate D1..D4 in one line each: what the outside verifier measured and what it asked for.
2. Read the frozen contract `{W}/contract.md` §C1 and the counter `{W}/c84_defect_queue.py`; for each item name the file a seat must produce and the exact string shape the counter greps for. Check the counter's own selftest by running `python3 -B {W}/c84_defect_queue.py --selftest` and report the tally.
3. Data-walk: list, at the freeze revision `{FREEZE}`, every existing `corpus/knowledge/*.md` entry that covers HTTP response-header policy, caching or freshness, and say which of them a new `policy-value-classes.md` entry would duplicate versus extend. Give the `git ls-tree -r --name-only {FREEZE} -- corpus/knowledge | wc -l` count.
4. Order the round's work items: which production file must exist before which receipt, and which receipt only the L1 can take after WAVE-DONE (name them).""",
    },
    {
        "name": "ScoutSources",
        "role": "scout",
        "item": f"""Open the source that grounds C2, GET-only, and retain its bytes. Report `{W}/w1/ScoutSources.md`, receipts under `{W}/w1/ScoutSources/`. Write no production corpus file (the row text you deliver is appended by ScribeRegistry).
1. GET `https://www.rfc-editor.org/rfc/rfc9111.txt` (HTTP only, no credentials) and retain the body at `{W}/w1/ScoutSources/rfc9111.txt` plus a receipt (final URL, status, byte count, sha256, RFC 3339 fetch time).
2. Locate, with 1-based line numbers and raw numeric evidence, the spans that define the value semantics C2 classifies: §4.2 *Freshness* (freshness lifetime), §5.2 *Cache-Control*, §5.2.2 *Response Directives* and §5.2.2.2 `max-age`. For each chosen quote give ≤25 words, the line span, and prove it is a raw substring of the retained bytes (`grep -F` receipt in `{W}/w1/ScoutSources/raw-checks.txt`).
3. State why `max-age` is a numeric parameter whose value change alters freshness while a directive reorder does not, quoting only what the retained bytes say; name anything you could NOT ground.
4. Deliver the proposed `corpus/SOURCES.md` row for **S457** in contract-v1 shape (11 cells, no `|` inside a cell, ISO `opened` date 2026-11-04, `recheck` cadence, `status` `queued` or `mined`, `used-by` `corpus/knowledge/policy-value-classes.md`), plus the ≥1 admit / ≥1 reject pair the Gate needs (a rejected anchor with its reason and flip condition).""",
    },
    {
        "name": "ExecPolicyTool",
        "role": "executor",
        "item": TOOL_SPEC.format(lane=LANE, w=W),
    },
    {
        "name": "ExecC1Derive",
        "role": "executor",
        "item": f"""Independently re-derive the four C1 items from committed bytes and attack the C1 counter's do-nothing reachability. Report `{W}/w1/ExecC1Derive.md`, receipts under `{W}/w1/ExecC1Derive/`. Write no production file.
1. At the freeze revision `{FREEZE}`, verify each item's state conjunct yourself (do not run the counter for this step): for D1 and D2 read `{LANE}/.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt` and count the `:838-844` span's words with your own command, printing the boundary you used; for D3 read the wave spec/result files that exist and say what is still missing; for D4 re-derive the census `W04` set from `{LANE}/corpus/SOURCES.md` with your own parser and compare it to `{W}/controls/census-before.txt`.
2. Build a records-only control tree under `/fast/scratch/hyaku/kake-r84/ExecC1Derive/junk/` whose `corpus/lessons/round-84.md` asserts, in prose, that all four items are closed, with no other files, and run the counter over it. Report the verdict and say whether any item can be closed by prose alone.
3. Run `python3 -B {W}/c84_defect_queue.py --root {LANE}` and paste the exact output; mark which items are open now and why.
4. Name one way the counter could read `met=true` without the claimed work having been done, and whether the frozen control catches it.""",
    },
    {
        "name": "ExecControlAudit",
        "role": "executor",
        "item": f"""Audit the frozen control pairs and the control-pair builder. Report `{W}/w1/ExecControlAudit.md`, receipts under `{W}/w1/ExecControlAudit/`. Write no production file and never edit the frozen pair.
1. Verify every receipt under `{W}/capture-control/{{control,equivalent}}/{{a,b}}/`: GET, integer status, bytes == body length, sha256 == body digest, truncated false. Print a per-receipt table.
2. Diff each pair's `a` against its `b` header-by-header and list every changed header with old→new value; confirm the changed set equals the table frozen in `{W}/contract.md` §"Frozen control expectations" and `{W}/policy-expectations.json`, and that no body, status or digest moved.
3. Re-run `python3 -B {W}/build_control_pairs.py --root /fast/scratch/hyaku/kake-r84/ExecControlAudit/rebuild-copy` in a scratch copy of the needed inputs and `cmp` the rebuilt pairs against the committed ones byte-for-byte; report the command and the result. (Copy `{LANE}/.ufo/waves/round-81/capture` into the scratch root first and run the builder with `--root` pointing at that scratch root.)
4. State whether the `equivalent` pair can be distinguished from the `control` pair by the value-level class table alone, and what a counter that only summed `changed` would miss.""",
    },
    {
        "name": "ScribeLesson",
        "role": "scribe",
        "item": f"""Write `{LANE}/corpus/lessons/round-84.md`. Report `{W}/w1/ScribeLesson.md`, receipts under `{W}/w1/ScribeLesson/`. Do not edit any other lane file.
The lesson must carry, in this order:
1. A header naming lane, round 84, attempt 1, base `{BASE}`, freeze `{FREEZE}`, the two claims and their axes.
2. `## Corrections` — one row per routed defect D1..D4 from `{LANE}/corpus/lessons/round-83-verifier-spotcheck.md` §6, each naming the file that re-derives it.
3. A line opening exactly `[r84-correction 2026-11-04]` that names `round-83.md` and its §`Gate`, and cites the four real RFC 9111 headings verbatim: `5.2.  Cache-Control`, `5.2.1.  Request Directives`, `5.2.2.  Response Directives`, `5.2.3.  Extension Directives` (this is D1).
4. Exactly one line `D2 count=66 span=838-844 measure=words-full-span` (this is D2; 66 is the whole-span count of lines 838–844 inclusive of the retained RFC 9111 bytes — verify it yourself before writing, with `python3 -c` over `{LANE}/.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt` and print the command in your report).
5. A line naming `{W}/controls/census-before.txt` and its `W04` count (this is D4's row conjunct).
6. `## Gate` — the round's candidates (S457), at least one admit and at least one reject with reason and flip condition, the URLs, the 2026-11-04 access date, and ≤25-word located quotes for every new row. Do not name a source heading the retained bytes do not contain.
7. `## Mistakes` — one row per mined mistake: class · evidence pointer · captured-by · fix.
Do not claim an after-state the counter has not measured: C1's after receipt is taken by the L1 after WAVE-DONE, and the lesson says so.""",
    },
    {
        "name": "ScribeKnowledge",
        "role": "scribe",
        "item": f"""Write `{LANE}/corpus/knowledge/policy-value-classes.md`, the C2 knowledge entry. Report `{W}/w1/ScribeKnowledge.md`, receipts under `{W}/w1/ScribeKnowledge/`. Do not edit `corpus/SOURCES.md` (ScribeRegistry owns it).
1. Open with the provenance trio: `source:`, `verified-at:`, `recheck:` — `source:` cites the `S457` row, the retained URL and the line anchors ScoutSources located.
2. Body: the value-level class table the tool implements (each class, its definition, one concrete example), the verdict order, and the two limits — it decides whether a policy statement's text moved, not whether the new policy is good, and it reads two captures, not a history.
3. Quote only spans you can locate in the retained bytes `{LANE}/.ufo/waves/round-83/w1/ScoutSources/rfc9111.txt`; give line numbers and ≤25 words per quote, and run the substring check yourself.
4. Mark the entry `opinion` where it is not source-backed (e.g. the mapping from class to a publisher's intent).
5. Re-open the sources you cite in this entry this round (CORPUS.md rule 1).""",
    },
    {
        "name": "ScribeRegistry",
        "role": "scribe",
        "item": f"""Append the S457 row to `{LANE}/corpus/SOURCES.md` and update the coverage index. Report `{W}/w1/ScribeRegistry.md`, receipts under `{W}/w1/ScribeRegistry/`. You are the only writer of `corpus/SOURCES.md` this round.
1. Append **S457** after the highest existing id (the registry had 194 rows at round 83; re-derive the count and the next free id yourself with the census commands). Contract-v1 shape: 11 cells, no `|` inside a cell, `kind=spec`, `tier=A`, `scope` naming policy-header value semantics, `anchor` naming §4.2/§5.2/§5.2.2 with the RFC revision, `status=mined`, `opened=2026-11-04`, `recheck=180d`, `used-by=corpus/knowledge/policy-value-classes.md`.
2. Append-only: never edit an existing cell except the three mutable ones, and record every `status`/`recheck`/`used-by` change old→new in the round lesson (do not edit the lesson; deliver the lines in your report for ScribeLesson/the L1).
3. Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` before and after and commit both outputs as `{W}/controls/census-after.txt` (full stdout plus `census_exit=`); the row count and `W04` count must be stated.
4. Add the new entry's row to `{LANE}/corpus/README.md` coverage map (one row, `policy-value-classes.md` / S457 / one-line coverage), and nothing else in that file.""",
    },
    {
        "name": "ReviewC1",
        "role": "reviewer",
        "item": f"""Attack C1. Report `{W}/w1/ReviewC1.md`, receipts under `{W}/w1/ReviewC1/`. Read-only over the lane; write only your report and receipts.
1. Re-derive each of D1..D4 from the worktree yourself; do not trust the counter's own output. Report per item: closed/open, the exact bytes you read, and the command.
2. Try to close an item with words alone: build a scratch tree (under `/fast/scratch/hyaku/kake-r84/ReviewC1/`) whose lesson asserts closure without the required files, and one where a heading string appears in the lesson but not in the retained bytes; run the counter on both and report the verdicts.
3. Check D2 as arithmetic: the claimed count must equal the whole-span word count of lines 838–844. Print your own count and the boundary definition you used.
4. Check D4's census re-derivation against the real registry: does the counter's `W04` set equal the census's? Name any divergence.
5. List every way the frozen predicate could read `met=true` while a row conjunct is false.""",
    },
    {
        "name": "ReviewC2",
        "role": "reviewer",
        "item": f"""Attack C2 and its tool. Report `{W}/w1/ReviewC2.md`, receipts under `{W}/w1/ReviewC2/`. Read-only over the lane; write only your report and receipts.
1. Read `{W}/contract.md` §C2 and `{LANE}/scripts/policy_value_class.py` when it exists (the tool is produced in this same wave; if it is absent at your start, wait by re-reading a few times at most and then report it absent — never fabricate its output).
2. Verify every receipt of the real pair and of both control pairs independently, and re-derive each changed policy header's class from the two `response.json` header lists by hand.
3. Check the frozen table's boundaries: a directive reorder must be `reordered`; a `max-age` numeric change must be `numeric_parameter`; a presence change must be `header_added`/`header_removed`; an unparsable value must be `unclassified` and decisive. Name a value that the grammar would misclassify.
4. Attack the predicate: can `met=true` hold with a tool whose control run is right but whose real-pair run is a canned string? What does `record_equal` add over `determinism`, and what does neither catch? Give the exact checks that would close the gap.
5. Report whether the real pair's `policy-unchanged` verdict is arithmetically right: 14 header diffs, all per-request, zero policy changes — verify or refute.""",
    },
    {
        "name": "CriticClaims",
        "role": "critic",
        "item": f"""Falsify both claims. Report `{W}/w1/CriticClaims.md`, receipts under `{W}/w1/CriticClaims/`. Read-only over the lane; write only your report and receipts.
1. For each claim, build the cheapest do-nothing control: what is the least work that makes the frozen counter read `met`? For C1 name the exact files and their contents; for C2 name the exact receipts. Score the control with the frozen counter (in a scratch tree) and report whether it reaches the target.
2. Name the axis each claim moves and whether an axis is harmed by the round's changes (state the diff you inspected).
3. Say whether C2 is a capability acquisition under AXES.md §Capabilities: what can the lane now do that it could not, and is the demonstration the round's own, not borrowed?
4. Name the strongest single reason a non-author closure should reject this round as currently framed, and the smallest change that would remove it.""",
    },
    {
        "name": "MutC",
        "role": "mutation-tester",
        "item": f"""Mutation-test both counters. Report `{W}/w1/MutC.md`, receipts under `{W}/w1/MutC/`. Write no production file.
1. Read `{W}/c84_defect_queue.py` and `{W}/c84_policy_values.py`. Propose at least six mutants (three per counter) that each remove one guard without changing the claimed sentence — e.g. drop a conjunct, accept a substring instead of the heading, accept `truncated != false`, skip the control expectation comparison.
2. Score each mutant against the fixtures/receipts it should fail on, in copies under `/fast/scratch/hyaku/kake-r84/MutC/`, and report killed/survived with the pristine and mutant readings side by side.
3. For every survivor, state the guarding conjunct that makes it equivalent (not a survivor) or name it a real gap.
4. Re-run both counters' `--selftest` and report the tallies.""",
    },
    {
        "name": "ConnectorSibling",
        "role": "connector",
        "item": f"""Sibling-overlap scan and cross-claim pattern finding (this seat also carries the round's connector duty). Report `{W}/w1/ConnectorSibling.md`, receipts under `{W}/w1/ConnectorSibling/`. Read-only over every repo; write only your report and receipts.
1. Search `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge/` and `corpus/SOURCES.md` (read-only) for ground this round would duplicate: header-change classification, HTTP caching policy values, drift gates over captured headers. Name each sibling file that overlaps and the exact overlap.
2. Check whether the round's new row S457 collides with an existing id or URL in the kake registry and in the shokuknow staged package (`/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md`), with the 0–3-space-tolerant id extractor; paste the id lists and the collision count.
3. Cross-claim pattern: is the C1 repair pattern (a routed-defect queue closed by conjuncts over bytes) the same pattern other lanes use? Name one sibling lane's file that implements it and one that does not, with line pointers.
4. State what the lane should learn from the pattern across lanes that it cannot learn from its own repo.""",
    },
]


def main() -> None:
    spec = {
        "wave": "kake-r84-w1",
        "reportDir": ".ufo/waves/round-84/w1",
        "maxLanes": len(ITEMS),
        "context": CONTEXT,
        "items": ITEMS,
    }
    out = Path(W) / "w1-spec.json"
    out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out} items={len(ITEMS)}")
    from collections import Counter
    print(Counter(item["role"] for item in ITEMS))


if __name__ == "__main__":
    main()
