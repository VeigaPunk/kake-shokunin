#!/usr/bin/env python3
"""Build .ufo/waves/round-100/w1-spec.json (kake round 100, ONE v1 wave).
Usage: make_spec_w1.py <freeze-commit> <c1-repair-commit>"""
import json
import os
import sys

L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W = L + "/.ufo/waves/round-100"
O = W + "/w1"
BASE = "3989618d9f8310b2eb5fb456aa7c4e58fb0b5ff5"
INSTR = "d7b73d161173710d04efc5f66784779bce5746ff"
FREEZE, REPAIR = sys.argv[1], sys.argv[2]
GOD = open(os.path.expanduser("~/.agents/skills/godspeed/directive.md")).read().strip()
SCR = "/fast/scratch/hyaku/kake-r100/<YourSeatName>/"

context = f"""/skill:godspeed
{GOD}

kake round 100 (hyaku run 15, attempt 1), ONE v1 wave, 14 seats. Lane root
{L} (call it LANE). Round base {BASE}; instruments commit {INSTR}; freeze commit
{FREEZE}; C1 repair commit {REPAIR}. Read the lane tip with `git -C LANE rev-parse master`.
Claims, predicates, counters, kill rules and targets are FROZEN at the freeze commit
(LANE/.ufo/waves/round-100/freeze.md): attack the instruments and the work, never patch them; a
suspected defect is a finding you route, never a repair you make. Read first:
LANE/.ufo/waves/round-100/freeze.md and LANE/.ufo/waves/round-100/controls/ (committed pre-freeze
receipts — reproduce, never re-stamp).
Claims: C1 calibration — SKILL.md tool registry v2: one current registry row per committed
scripts/ tool and every row's verdict map naming the exit code the tool returns for an unknown flag;
counter LANE/.ufo/waves/round-100/c100_registry.py (base: duplicated=7 probe_mismatch=2 mismatches=9;
the repair at {REPAIR} removes the seven older duplicate rows and keeps them verbatim in the fenced
`## Round 100 — superseded registry rows` block at the end of SKILL.md), plus a two-reviewer review
conjunct. C2 freshness capability — 304 freshening contract v2
(LANE/.ufo/waves/round-100/fresh304-contract-v2.md, on top of the v1 contract
LANE/.ufo/waves/round-99/fresh304-contract.md): qualified Cache-Control in either argument form and any
case, unrecognised directives ignored, output values trimmed, stored proxy fields dropped, the seven
round-99 escape classes; counter LANE/.ufo/waves/round-100/c100_fresh304.py (bwrap-sandboxed
candidate runner); candidate scripts/freshen_304.py v2 built in this wave by ExecFresh. Sources:
RFC 9111 retained at LANE/.ufo/waves/round-99/sources/rfc9111.txt (sha256 aeb52adb…), RFC 9110 at
LANE/.ufo/waves/round-100/sources/rfc9110.txt (sha256 21c1cdce…).

Hard bounds (every seat, no exceptions):
- Write ONLY inside {O}/<YourSeatName>/ (create it; flat filenames). NOTHING else in the lane tree,
  no other round dir, no sibling lane, no fleet repo (/home/vgpnk/Projects/shokunin itself), no
  .ufo/state, never MANIFEST.json. You are a reporter: deliver tables, receipts, drafts and
  verdicts; the L1 integrates.
- Never run a mutating git or jj command in LANE or the fleet repo (no add/commit/push/checkout/
  reset/stash; no jj commit/new/describe/rebase/bookmark/undo). Read-only git is fine. Fixture
  repos or clones live in your scratch root: D=<scratch>/fx && git -C "$D" init -q (or
  `git clone --shared LANE "$D"`); verify `git -C "$D" rev-parse --show-toplevel` equals "$D"
  before the first commit; identity <yourseat>@example.invalid via -c flags only.
- Scratch root: {SCR} (create it; pass it explicitly as --work / TMPDIR; never rely on inherited
  TMPDIR; /tmp only for files under 50 MB). Delete ONLY your own seat directory before you yield
  (receipts first copied into your w1 subdir). NEVER remove /fast/scratch/hyaku/kake-r100 or any
  other ancestor or sibling of your own seat directory. One live clone per seat.
- Never mutate host sysctls (user.max_user_namespaces included) or any host config; if bwrap fails,
  name the need in your report instead.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task;
  first read /home/vgpnk/.omp/agent/RULES.md; pacman is PAUSED host-wide (never pacman
  -S/-Sy/-Syu/-U/-R, never a partial upgrade; use `uv tool install`, `npx`, or an official binary in
  ~/.local/bin); record any tool/version/channel/reason in your report.
- Honesty: an unrun check has not passed. Every verdict line names its command and observed rc.
  Never fabricate output. End your final answer with your seat's verdict line exactly as the item
  spells it (plain text, not inside JSON).
- Every `Report:` trailer path in the validator output is relative to {L}: write it at
  {L}/<that path>.
- Frozen digests: LANE/.ufo/waves/round-100/controls/instrument-sha256.txt. Verify before attacking;
  a mismatch is a finding, not a repair license."""

items = []


def add(name, role, text):
    items.append({"name": name, "role": role, "item": text.replace("<YourSeatName>", name)})


D = O + "/<YourSeatName>"
R100 = "LANE/.ufo/waves/round-100"

add("ScoutSources", "scout", f"""Target: re-open, this round, the two sources C2 rests on (evidence for new SOURCES rows S486 and S487).
Change: (1) GET https://www.rfc-editor.org/rfc/rfc9111.txt and https://www.rfc-editor.org/rfc/rfc9110.txt once each (record status, final URL, bytes, sha256, UTC time); copy bodies into your scratch only, and state whether each sha256 equals the retained {R100}/../round-99/sources/rfc9111.txt (aeb52adb…) and {R100}/sources/rfc9110.txt (21c1cdce…). (2) From the bodies give, with plain-text line numbers, one ≤25-word verbatim located quote each for: RFC 9111 §5.2 "identified by a token, to be compared case-insensitively" sentence; §5.2 "recipients ought to accept both forms"; the `cache-directive = token [ "=" ( token / quoted-string ) ]` rule; §5.2.2.4 qualified no-cache (the field-name argument sentence); §5.2.2.7 qualified private; §5.2.3 "MUST ignore unrecognized cache directives"; §3.1 proxy-specific fields MUST NOT be stored; RFC 9110 §5.5 "A field value does not include leading or trailing whitespace"; §5.6.1.2 the `#element => [ element ] *( OWS "," OWS [ element ] )` recipient rule; §5.6.4 quoted-string/qdtext/quoted-pair rules. (3) Draft two registry rows in the 11-column shape of LANE/corpus/SOURCES.md (`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`; no literal `|` inside a cell): S486 = RFC 9111 §5.2/§5.2.2.4/§5.2.2.7/§5.2.3 (Cache-Control grammar and extension handling; scope distinct from S484's §3.1/§3.2/§4.3.4 and S456), S487 = RFC 9110 §5.5/§5.6.1.2/§5.6.2/§5.6.4 (field-value whitespace, list and quoted-string syntax; scope distinct from S433/S453/S465), status `mined`, opened 2026-11-06, recheck 365d, used-by `corpus/knowledge/freshening-304.md`. Write {D}/report.md and {D}/rows.md.
Acceptance: final line `SCOUT rfc9111-sha=<match|differs> rfc9110-sha=<match|differs> quotes=<n>/10 rows=2`.""")

add("ExecFresh", "executor", f"""Target: the C2 candidate — scripts/freshen_304.py v2, built from the contracts ALONE.
Change: (1) Read {R100}/fresh304-contract-v2.md, the v1 contract LANE/.ufo/waves/round-99/fresh304-contract.md it amends, and the RFC text; you MAY read the current v1 candidate LANE/scripts/freshen_304.py and adapt it. Do NOT read the code of {R100}/c100_fresh304.py below its docstring (lines 1-33 allowed), {R100}/build_frozen.py or {R100}/frozen/*.py — the candidate must be an independent implementation of the v2 text. (2) Write {D}/freshen_304.py: stdlib-only Python 3; module docstring naming contract v2, RFC 9111 §4.3.4/§3.2/§3.1/§5.2/§5.2.3, RFC 9110 §5.5/§5.6.1.2/§5.6.4, each lane convention LC1-LC6 and LC8 and each V2 clause; reads stdin BYTES (non-UTF-8 or invalid JSON → refusal); stdout one JSON object + one `\\n`, exit 0; refusal `invalid_input: <reason>` on stderr, ZERO bytes on stdout, exit 1; every argv word other than `--selftest` is ignored (an unknown flag behaves like no flag); `--selftest` runs ≥40 in-memory cases of your own (cover every V2 clause and e1-e7), prints `selftest N/N`, exit 0 only when all pass; no file, socket or subprocess in the decision path. (3) Score it: `python3 -B LANE/.ufo/waves/round-100/c100_fresh304.py --candidate-file {D}/freshen_304.py --work {SCR}w` and with three extra `--seed` values; record each output line in {D}/scores.txt. If any case fails, fix your candidate from the CONTRACT text (never from the counter's code) and re-score; record every attempt. (4) `python3 -B {D}/freshen_304.py --zz-bogus-r100 </dev/null; echo $?` must print exit 1 — record it.
Acceptance: final line `EXECFRESH sha256=<hex> hand=<a>/<b> generated=<c>/<d> met=<bool> selftest=<n>/<n> attempts=<k>`.""")

add("ExecTwinFresh", "executor", f"""Target: an independent held-out differential for C2 (considerthese 2026-11-05 proposal 3: held-out vs frozen divergence).
Change: (1) Read ONLY {R100}/fresh304-contract-v2.md, LANE/.ufo/waves/round-99/fresh304-contract.md and the RFC text — not c100_fresh304.py's code, not frozen/*.py. Write {D}/twin.py implementing contract v2. (2) Write your OWN input generator (different from the counter's): qualified Cache-Control in token/quoted/empty-quoted forms and mixed case, extension directives whose names contain no-cache/private, quoted strings with commas and escapes, empty list elements, malformed lists (unterminated quote, space around `=`, `;`, control chars, non-ASCII token), OWS-bearing values on both sides, stored proxy/hop/connection fields, Age, LM ties with and without ETag, malformed stored ETags, raw non-JSON / non-UTF-8 stdin. Run ≥3000 inputs through your twin and through LANE/.ufo/waves/round-100/frozen/pos-oracle.py (`python3 -I -B`, stdin bytes). (3) For every disagreement decide from the contract text who is right and quote the deciding sentence; classify oracle defect / twin defect / contract ambiguity. Write {D}/disagreements.md and {D}/run.txt (counts per class).
Acceptance: final line `TWIN inputs=<n> disagreements=<n> oracle_defects=<n> twin_defects=<n> ambiguities=<n>`.""")

add("ExecRegProbe", "executor", f"""Target: independent re-measurement of C1 at the repair commit {REPAIR} (no use of c100_registry.py's code paths; your own commands).
Change: (1) `git -C LANE archive {REPAIR} | tar -x -C <scratch>/tree`. (2) For each committed tool directly under scripts/ (*.py, *.mjs), count the SKILL.md registry-table rows (outside fences) whose Entry-command cell INVOKES it (first word, or after python3/node and flags) — report any tool with ≠1. (3) For the seven tools the repair touched (cache_key.py, cache_key_conformance.py, live_snapshot.py, response_snapshot.py, robots_audit.py, source_snapshot.py, x_robots_tag_audit.py): under `bwrap --unshare-net` (or `unshare -rn`), run with no arguments, with `--zz-bogus-r100`, and (stdin tools) with `{{}}` and with `not json` on stdin; NEVER run a network fetch mode; record each rc and compare with the kept row's verdict map. Run each kept row's Self-test cell command and record rc + last line. (4) Verify the fenced history block: each of the 7 removed rows (lines 494, 1079, 1104, 1370, 1505, 1621, 1624 of SKILL.md at {BASE}) appears byte-identical inside the fence (`git show {BASE}:SKILL.md | sed -n '<n>p'` vs the block line). (5) `git diff {BASE} {REPAIR} --stat` — confirm only SKILL.md changed and only those 7 lines were removed. Write {D}/probe.tsv and {D}/report.md.
Acceptance: final line `REGPROBE tools=<n> not_one_row=<n> probe_contradictions=<n> selftest_fail=<n> history_verbatim=<n>/7 other_changes=<n>`.""")

add("ReviewRegA", "reviewer", f"""Target: the C1 review conjunct, seat A (frozen; read freeze.md §C1).
Change: At the repair commit {REPAIR}, judge each of the 8 units: the seven KEPT registry rows (Name cells `cache_key.py`, `cache_key_conformance.py`, `live_snapshot.py`, `response_snapshot.py`, `robots_audit.py`, `source_snapshot.py`, `scripts/x_robots_tag_audit.py (round-80 grammar)`) and the fenced history block. For each kept row read the tool's CODE (every return / sys.exit / parser error path, argparse behaviour; never the docstring alone) and decide whether the row's verdict map, entry command, self-test cell and write scope are true; for the history block decide whether it keeps the 7 removed rows verbatim and labels each with the right tool and current row. Run what you need in scratch (no network). Write {D}/verdicts.tsv: exactly 8 lines `<unit>\\t<agree|disagree>\\t<reason with path:line>` (unit = the row's Name cell, or `history-block`).
Acceptance: final line `REVIEWREG-A agree=<n> disagree=<n> of 8`.""")

add("ReviewRegB", "reviewer", f"""Target: the C1 review conjunct, seat B — independent of seat A (do not read w1/ReviewRegA).
Change: Same task as seat A: at {REPAIR}, judge the seven KEPT registry rows (Name cells `cache_key.py`, `cache_key_conformance.py`, `live_snapshot.py`, `response_snapshot.py`, `robots_audit.py`, `source_snapshot.py`, `scripts/x_robots_tag_audit.py (round-80 grammar)`) against the tools' CODE (return / sys.exit / parser-error paths), and the fenced `## Round 100 — superseded registry rows` block (7 removed rows verbatim, correct labels). Also check that no OTHER registry row in SKILL.md still invokes one of these seven tools. Write {D}/verdicts.tsv: exactly 8 lines `<unit>\\t<agree|disagree>\\t<reason with path:line>`.
Acceptance: final line `REVIEWREG-B agree=<n> disagree=<n> of 8`.""")

add("ReviewFresh", "reviewer", f"""Target: contract v2 and its hand expectations against the RFC text (findings are routed; they do not change the frozen C2 predicate).
Change: (1) For each HAND case tagged `v2-*` or `e1`-`e7` in {R100}/c100_fresh304.py (reading this file is allowed for you), judge whether its expectation follows from RFC 9111 §5.2/§5.2.2.4/§5.2.2.7/§5.2.3/§3.1 (retained LANE/.ufo/waves/round-99/sources/rfc9111.txt), RFC 9110 §5.5/§5.6.1.2/§5.6.4 ({R100}/sources/rfc9110.txt) or a contract sentence marked as a lane convention; write {D}/hand-review.tsv (`tag\\tagree|disagree\\tbasis line`). (2) Judge each V2 clause and LC8: does the RFC contradict it, leave it open, or require it; does v2 newly contradict any RFC MUST. (3) Say which round-99 findings F1-F12 (LANE/.ufo/waves/round-99/w1/ReviewFresh/contract-findings.md) v2 closes and which stay open. Write {D}/contract-findings.md.
Acceptance: final line `REVIEWFRESH hand=<agree>/<total> v2_findings=<n> rfc_contradictions=<n> closed=<list>`.""")

add("CriticClaims", "critic", f"""Target: falsify both claims as frozen.
Change: (1) C1: in a scratch clone of LANE at {REPAIR}, construct SKILL.md edits that make c100_registry.py print met=true while the registry is wrong in a way the freeze's DECLARED limits (extra codes named in a map; false-but-well-formed prose) do NOT cover — e.g. a second row for a tool hidden from the invocation parser (`python3 -X dev scripts/x.py`, `env python3 scripts/x.py`, `bash -c`, a `cd scripts &&` prefix, `uv run`), a tool invoked via a relative path, a duplicate in a table whose header misses one required column, a probe that a tool can detect and special-case. Run the counter on each fixture commit; record outputs in {D}/c1-attacks.md. (2) C2: write candidates in scratch that score met=true under c100_fresh304.py (`--candidate-file`) while violating contract v2 (name the clause), and try ones that detect the sandbox. Record each candidate file and its counter line in {D}/candidates/ and {D}/c2-attacks.md. (3) Attack the claim framing: can a do-nothing or cheaper control reach either target? Is C1 really calibration (self-assessment vs observed state)?
Acceptance: final line `CRITIC c1_escapes=<n> c2_escapes=<n> framing_defects=<n>`.""")

add("MutCounters", "mutation-tester", f"""Target: mutation-test both frozen counters.
Change: (1) Copy {R100}/c100_registry.py and {R100}/c100_fresh304.py into your scratch; make ≥12 single-point mutants of predicate-bearing lines in each (c100_registry: invoked() interpreter/flag/assignment/pipe handling, duplicate threshold, CODE regex lookbehind/lookahead, probe argument, sandbox flags, met sum; c100_fresh304: _cc_directives token/quoted/escape/OWS/empty-element paths, qualified-name test, case folding, output trim, PROXY drop, decide_bytes error set, judge() stdout strictness, sandbox_ok). (2) Run each mutant on its own --selftest and on the committed controls (re-run the matching commands of {R100}/controls.sh against the mutant: for c100_registry the base revision {BASE} and the pos/keepold/deleteall fixtures; for c100_fresh304 the frozen/*.py candidates and base). A mutant is killed when any outcome changes. (3) For each survivor say whether it is equivalent and give a separating input. Write {D}/mutants.tsv and {D}/survivors.md. Watch disk: run `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` first.
Acceptance: final line `MUT registry=<killed>/<n> fresh304=<killed>/<n> survivors=<n> equivalent=<n>`.""")

add("SentinelScope", "sentinel", f"""Target: the sandboxes both counters added this round (R99-9 W1-W4 successor).
Change: As a candidate (c100_fresh304 `--candidate-file`) and as a scripts/ tool in a scratch fixture repo scored by c100_registry, try to: read the counter's source or its oracle (/proc, inherited fds, environment, cwd, bind mounts), write outside the sandbox or into the scored tree in a way a later case or row sees, reach the network, outlive the case (background process, --die-with-parent), exhaust time/disk, or detect the sandbox to change behaviour. Record each attempt, the command, observed result and whether it succeeded in {D}/vectors.md and {D}/poc-*.py. Never touch the host outside your scratch; never change sysctls.
Acceptance: final line `SENTINEL vectors=<n> escapes=<n> cross_case_leaks=<n>`.""")

add("LabratDeterminism", "labrat", f"""Target: one falsifiable hypothesis — "both frozen counters are deterministic on committed bytes: re-running them at the same revision gives byte-identical receipts".
Change: Run `python3 -B {R100}/c100_registry.py --root LANE --revision {BASE} --work {SCR}a` three times and diff the outputs against {R100}/controls/base-c1.txt (minus its `$`/exit lines); run `python3 -B {R100}/c100_fresh304.py --root LANE --revision {BASE} --work {SCR}b` three times and diff against controls/base-c2.txt; also run c100_fresh304 at {BASE} with `--seed 1` twice. Record outputs and diffs in {D}/runs.txt.
Acceptance: final line `LABRAT registry_identical=<n>/3 fresh304_identical=<n>/3 seeded_identical=<bool> hypothesis=<held|falsified>`.""")

add("ScribeEntry", "scribe", f"""Target: the knowledge entry C2 lands with (sourced on S486/S487).
Change: Draft {D}/freshening-304.md: the full replacement of LANE/corpus/knowledge/freshening-304.md (read it first; keep every still-true v1 statement and its citations, the provenance trio first lines `source:` now `S484, S485, S486, S487`, `verified-at: 2026-11-06`, `recheck:` ISO date or NNd). Add a `## Contract v2 (round 100)` section: the Cache-Control qualified-form decision (both argument forms, case-insensitive names, §5.2.3 extension handling, LC8 malformed-list refusal as a lane convention), field-value trimming (RFC 9110 §5.5), proxy-field drop (§3.1 bullet 4), the seven escape classes as a decision table, and known limits (F4-F9, F11 still open). Every quote ≤25 words with its plain-text line number from the retained bodies ({R100}/sources/rfc9110.txt, LANE/.ufo/waves/round-99/sources/rfc9111.txt); cite S486/S487 for the new statements. No meta-text about seats, waves or drafting. Run `python3 -B LANE/scripts/knowledge_metatext_lint.py` on your draft if it accepts a path (else note it) and record the result.
Acceptance: final line `SCRIBE entry=freshening-304.md quotes=<n> citations=S486:<n>,S487:<n> lint=<rc>`.""")

add("ScribeLesson", "scribe", f"""Target: the round-100 lesson draft (gate, mistakes, criterion).
Change: (1) Sweep LANE/corpus/lessons/round-99-verifier-spotcheck.md, round-99.md, round-98-verifier-spotcheck.md for a mistake NOT yet mined in round-97/98/99 `## Mistakes` tables (read them); draft ≥1 `## Mistakes` row in the round-99 table shape (`# | Class | Evidence (path:line) | Captured-by | Fix (shown able to fail)`); if you find none, paste the sweep commands and their output. (2) Read LANE/considerthese/2026-11-05.md Part 2 proposal 3 ("held-out vs frozen divergence column"); draft it as QUALITY criterion R100-A with a check command and say how it can be shown red (proposal 2 was taken in r98, proposal 4 in r99). (3) Draft the `## Gate` skeleton for rows S486/S487 (admit, with URL, access date 2026-11-06, ≤25-word located quote and line) and the reject of merge/kake package adoption (read LANE/.ufo/waves/round-99/assimilation/collisions and /home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md read-only; re-derive the collision list for the current registry with the 0-3-space pattern; never write into shokuknow). Write {D}/lesson-draft.md.
Acceptance: final line `SCRIBELESSON mistakes=<n> criterion=R100-A collisions=<n>`.""")

add("ConnectorScope", "connector", f"""Target: read-only sibling-overlap scan for this round's two surfaces.
Change: (1) In sibling lane repos /home/vgpnk/Projects/shokunin/*-shokunin (read-only; skip kake), find (a) instruments that detect duplicate or shadowed registry/table rows, or probe a tool's real exit codes against a documented map, and (b) any lane holding RFC 9111 §5.2 Cache-Control parsing / qualified no-cache or private / RFC 9110 §5.5 whitespace ground. (2) For each hit: lane, path, `git -C <repo> rev-parse HEAD`, one-line gist, whether it overlaps, contradicts or could be cited. (3) Name one technique from a sibling that would harden c100_registry.py or c100_fresh304.py, with its path. Write {D}/overlap.md.
Acceptance: final line `CONNECTOR hits=<n> overlaps=<n> contradictions=<n> techniques=<n>`.""")

spec = {"wave": "kake-r100-w1", "reportDir": ".ufo/waves/round-100/w1", "maxLanes": len(items),
        "context": context, "items": items}
json.dump(spec, open(W + "/w1-spec.json", "w"), indent=1, ensure_ascii=False)
print(len(items), "items")
