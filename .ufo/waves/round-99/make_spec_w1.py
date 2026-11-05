#!/usr/bin/env python3
"""Build .ufo/waves/round-99/w1-spec.json (kake round 99, ONE v1 wave)."""
import json
import os
import sys

L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W = L + "/.ufo/waves/round-99"
O = W + "/w1"
BASE = "cde408e5817bf1376c701d8decc5469fa82b2985"
INSTR = "2345e309640adac6c36e41eca87409085ba3a276"
FREEZE, REPAIR = sys.argv[1], sys.argv[2]
GOD = open(os.path.expanduser("~/.agents/skills/godspeed/directive.md")).read().strip()
SCR = "/fast/scratch/hyaku/kake-r99/<YourSeatName>/"

context = f"""/skill:godspeed
{GOD}

kake round 99 (hyaku run 15, attempt 1), ONE v1 wave, 13 seats. Lane root
{L} (call it LANE). Round base {BASE}; instruments commit {INSTR}; freeze commit
{FREEZE}; C1 repair commit {REPAIR}. Read the lane tip with `git -C LANE rev-parse master`.
The round's claims, predicates, counters, kill rules and targets are FROZEN at the freeze commit
(LANE/.ufo/waves/round-99/freeze.md): attack the instruments and the work, never patch them; a
suspected defect is a finding you route, never a repair you make. Read first:
LANE/.ufo/waves/round-99/freeze.md, LANE/.ufo/waves/round-99/fresh304-contract.md,
LANE/.ufo/waves/round-99/controls/ (committed pre-freeze receipts — reproduce, never re-stamp).
Claims: C1 calibration — SKILL.md registry tables vs committed tools directly under scripts/,
counter LANE/.ufo/waves/round-99/c99_registry.py (26 unlisted at base -> 0 at {REPAIR}; the repair
is the `## Round 99 — tool registry completion` section at the end of SKILL.md, 26 rows), plus a
two-reviewer row-review conjunct. C2 freshness capability — which stored responses a 304 freshens
and their updated header fields (RFC 9111 §4.3.4 + §3.2), contract
LANE/.ufo/waves/round-99/fresh304-contract.md, candidate scripts/freshen_304.py (built in this
wave by ExecFresh), counter LANE/.ufo/waves/round-99/c99_fresh304.py. RFC 9111 body retained at
LANE/.ufo/waves/round-99/sources/rfc9111.txt (sha256 aeb52adb…); erratum EID 9185 page at
LANE/.ufo/waves/round-99/sources/eid9185.html.

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
  (receipts first copied into your w1 subdir). NEVER remove /fast/scratch/hyaku/kake-r99 or any
  other ancestor or sibling of your own seat directory. A seat that ends with its tree on disk
  reports that as its own defect. One live clone per seat.
- Never mutate host sysctls; name the need instead.
- Tooling authorization (operator, 2026-10-19): you may install/upgrade tools that help the task;
  first read /home/vgpnk/.omp/agent/RULES.md; pacman is PAUSED host-wide (never pacman
  -S/-Sy/-Syu/-U/-R, never a partial upgrade; use `uv tool install`, `npx`, or an official binary in
  ~/.local/bin); record any tool/version/channel/reason in your report.
- Honesty: an unrun check has not passed. Every verdict line names its command and observed rc.
  Never fabricate output. End your final answer with your seat's verdict line exactly as the item
  spells it (plain text, not inside JSON).
- Every `Report:` trailer path in the validator output is relative to {L}: write it at
  {L}/<that path>, i.e. inside your own w1/<YourSeatName>/ directory.
- Frozen digests: LANE/.ufo/waves/round-99/controls/instrument-sha256.txt. Verify before attacking;
  a mismatch is a finding, not a repair license."""

items = []


def add(name, role, text):
    items.append({"name": name, "role": role, "item": text.replace("<YourSeatName>", name)})


D = O + "/<YourSeatName>"
add("ScoutRfc9111", "scout", f"""Target: re-open, this round, the two sources C2 rests on: RFC 9111 (§3.1, §3.2, §4.3.4) and erratum EID 9185; evidence for SOURCES rows S484 and S485.
Change: (1) GET https://www.rfc-editor.org/rfc/rfc9111.txt, https://www.rfc-editor.org/errata/eid9185 and https://www.rfc-editor.org/errata_search.php?rfc=9111 once each (follow redirects; record every hop status, final URL, byte count, sha256, UTC time) into your scratch; copy bodies to {D}/. State whether the RFC body sha256 equals the retained LANE/.ufo/waves/round-99/sources/rfc9111.txt (aeb52adb…). (2) From the RFC body give, with plain-text line numbers, a ≤25-word located quote each for §3.2's add/replace sentence, §3.2's Content-Length exception, §4.3.4's strong-validator MUST NOT, §4.3.4's weak "most recent" sentence, §4.3.4's no-validator sentence, and §3.1's Proxy-Authenticate sentence. (3) From the errata pages list every erratum touching §3.1, §3.2 or §4.3.4 (id, status, type, date, one-line gist) and quote EID 9185's status line. (4) Draft two registry rows in LANE/corpus/SOURCES.md's 11-column shape (`| S484 | … | spec | A | … |` and `| S485 | … | dataset | A | … |`, status `mined`, opened 2026-11-05, recheck an ISO date or NNd, used-by `corpus/knowledge/freshening-304.md`), no literal `|` inside any cell. Write {D}/report.md + {D}/rows.md.
Acceptance: final line `SCOUT rfc9111-sha=<match|differs> eid9185=<status> errata-touching=<n> quotes=<n>/6`.""")
add("ConnectorScope", "connector", f"""Target: read-only sibling-overlap scan for this round's two surfaces.
Change: (1) In sibling lane repos /home/vgpnk/Projects/shokunin/*-shokunin (read-only; skip kake), find (a) instruments that check a SKILL.md gate/tool registry against committed scripts (grep -ril for `registry` together with `scripts/` in .ufo/waves counters, `gate registry`, `unlisted`), and (b) any lane holding RFC 9111 §4.3.4 / §3.2 ground (grep -ril `4.3.4`, `Freshening Stored`, `Updating Stored Header`). (2) For each hit: lane, path, `git -C <repo> rev-parse HEAD`, one-line gist, and whether it overlaps, contradicts or could be cited by this round's work (prior art to learn from, never to copy). (3) Name one technique from a sibling that would harden c99_registry.py or c99_fresh304.py, with its path. Write {D}/overlap.md.
Acceptance: final line `CONNECTOR hits=<n> overlaps=<n> contradictions=<n> techniques=<n>`.""")
add("ExecFresh", "executor", f"""Target: the C2 candidate — build scripts/freshen_304.py from the contract ALONE.
Change: (1) Read LANE/.ufo/waves/round-99/fresh304-contract.md and the retained RFC 9111 §3.1/§3.2/§4.3.4 text; do NOT read the code of LANE/.ufo/waves/round-99/c99_fresh304.py, build_frozen.py or frozen/*.py (c99_fresh304.py's docstring, lines 1-30, is allowed) — the candidate must be an independent implementation. (2) Write {D}/freshen_304.py: stdlib-only Python 3, module docstring naming the contract, RFC 9111 §4.3.4/§3.2/§3.1 and each lane convention LC1-LC6; stdin JSON → stdout JSON exit 0, refusals `invalid_input: <reason>` on stderr, empty stdout, exit 1; a `--selftest` mode over ≥30 in-memory cases of your own that prints `selftest N/N` and exits 0 only when all pass; no file, socket or subprocess use in the decision path. (3) Score it with the frozen counter via `--candidate-file` only: `python3 -B LANE/.ufo/waves/round-99/c99_fresh304.py --root LANE --revision master --candidate-file {D}/freshen_304.py --work <scratch>` on the default seed and seeds 1, 2, 3; save each output to {D}/score-<seed>.txt. If a case fails, fix YOUR candidate from the contract (never the counter) and re-score; record each iteration in {D}/log.md, including any contract sentence you found ambiguous.
Acceptance: final line `EXEC freshen_304 selftest=<n>/<n> default=<met|unmet> seeds=<k>/3 sha256=<hex>`.""")
add("ExecTwinFresh", "executor", f"""Target: differential falsifier of the C2 oracle — an independent twin written from the contract only.
Change: (1) Read ONLY LANE/.ufo/waves/round-99/fresh304-contract.md (and RFC 9111) — not c99_fresh304.py's code, not frozen/*.py. Write {D}/twin.py implementing the contract. (2) Write your own random input generator (different from the counter's; include multiple matching strong ETags, weak/strong mixes, Last-Modified whitespace, ties on `received`, Connection lists naming excluded and non-excluded fields, mixed-case names, obs-text ETags, bools/floats/huge ints for received, every refusal kind) and run ≥2000 inputs through your twin and through LANE/.ufo/waves/round-99/frozen/pos-oracle.py (the counter's reference as a tool). (3) For every disagreement, decide from the contract text who is right and quote the deciding sentence; classify as oracle defect, twin defect or contract ambiguity. Write {D}/disagreements.md and {D}/run.txt (command, n, disagreements count).
Acceptance: final line `TWIN inputs=<n> disagreements=<n> oracle-defects=<n> ambiguities=<n>`.""")
add("ExecRegProbe", "executor", f"""Target: empirical falsifier of the C1 repair rows — run what each row claims.
Change: (1) Extract the lane at {REPAIR} into your scratch (`git -C LANE archive {REPAIR} | tar -x -C <scratch>/tree`). (2) For each of the 26 rows in SKILL.md's `## Round 99 — tool registry completion` section: run its Self-test cell command (if any) and record rc + last line; then, without network, probe its Verdict map: run the tool with no arguments, with an unknown flag `--zz-bogus`, and (stdin tools) with `{{}}` and with `not json` on stdin; record each rc. A row's exit-code claim is contradicted when an observed rc is neither in its map nor explained by argparse's usage exit 2 (note it). Do NOT run network tools' fetch modes (live_snapshot, response_snapshot, source_snapshot): probe only usage/bad-input paths for them. (3) Also check the Write scope cell for any tool you ran: list files created outside your scratch, if any (`find LANE -newer <stamp>` read-only). Write {D}/probe.tsv (`row\\tprobe\\trc\\tconsistent?`) and {D}/findings.md.
Acceptance: final line `REGPROBE rows=26 selftests_ok=<n> contradictions=<n> scope_escapes=<n>`.""")
add("ScribeEntry", "scribe", f"""Target: draft the C2 knowledge entry and its coverage-map row.
Change: (1) Draft {D}/freshening-304.md in the shape of LANE/corpus/knowledge/stale-extensions.md: first lines `source:` (S484, S485), `verified-at: 2026-11-05`, `recheck:` (ISO date or NNd), `scope:`; then what RFC 9111 §4.3.4 says about the initial set and its three first-match rules, what §3.2 says about updating stored header fields and its four exceptions, the §3.1 exceptions §3.2 points at, the lane conventions LC1-LC6 of LANE/.ufo/waves/round-99/fresh304-contract.md (each named a lane convention, not an RFC requirement), erratum EID 9185 (Reported, not Verified; what it would change and why the contract does not depend on it), and a decision table (304 validators → rule → identified set). Every quote ≤25 words with its plain-text line number in LANE/.ufo/waves/round-99/sources/rfc9111.txt; verify each quote is a substring (after whitespace collapse) and write {D}/quotes-check.txt (quote, line, found yes/no). (2) Draft the corpus/README.md entry-table row for it in the existing row shape. No seat names, no handoff wording inside the entry (R98-D1: `scripts/knowledge_metatext_lint.py --dir {D}` must exit 0 — run it and save the output).
Acceptance: final line `SCRIBE entry quotes=<found>/<total> metatext_lint_rc=<rc>`.""")
add("ScribeLesson", "scribe", f"""Target: mistake mining and the considerthese proposal for corpus/lessons/round-99.md.
Change: (1) Sweep LANE/corpus/lessons/round-9{{6,7,8}}-verifier-spotcheck.md and LANE/corpus/lessons/round-98.md for mistakes not yet mined; draft ≥2 `## Mistakes` entries (class · evidence pointer path:line · captured-by (criterion or rule, or `none`) · fix), one of them the registry drift this round's C1 measures (tools landed r89-r98 with no conformant SKILL.md row: cite the r98 closure R98-C1 line and `controls/base-c1.txt`). For each fix say how it was shown able to fail (a red control) or say it was not. (2) Read LANE/considerthese/2026-11-05.md; pick ONE proposal not yet implemented (check LANE/corpus/lessons/round-98.md for proposal 2 already taken) and draft it as a QUALITY criterion with an id R99-A and a check command. (3) Draft the lesson's `## Gate` skeleton for rows S484/S485 (admit, URL, access date, ≤25-word quote placeholders the scout fills) and one reject (the merge/kake package: 8 id collisions, LANE/.ufo/waves/round-99/assimilation/collisions). Write {D}/lesson-draft.md.
Acceptance: final line `LESSON mistakes=<n> proposal=<id> gate_rows=<n>`.""")
for nm in ("ReviewRegA", "ReviewRegB"):
    add(nm, "reviewer", f"""Target: the C1 row-review conjunct — judge EVERY one of the 26 rows the round-99 repair added, independently.
Change: (1) `git -C LANE diff {FREEZE} {REPAIR} -- SKILL.md` shows the repair: the `## Round 99 — tool registry completion` section, 26 table rows. (2) For each row, open the tool at {REPAIR} (`git -C LANE show {REPAIR}:scripts/<tool>`) and judge each cell against the code: Kind (what the tool is), Entry command (flags exist and the form runs), Verdict map (each exit code the code can return is mapped truthfully; `not used` is true), Self-test (the command exists and is the tool's self-test; run it in a scratch extraction of {REPAIR} and record rc), Write scope (what the code writes), Owner. A row is `agree` only if no cell is false; minor wording you would improve is still `agree` with a note; a false cell is `disagree` with the cell, the code line (path:line) and the observed rc. (3) Write {D}/verdicts.tsv with exactly 26 lines `<row name>\\t<agree|disagree>\\t<reason>` (row name = first cell, e.g. `cache_key.py`) and {D}/review.md (method, commands, rc).
Acceptance: final line `REVIEW rows=26 agree=<n> disagree=<n>`.""")
add("ReviewFresh", "reviewer", f"""Target: the semantic ground of C2 — the contract and the 50 hand expectations against the RFC text.
Change: (1) For each hand case in the HAND list of LANE/.ufo/waves/round-99/c99_fresh304.py (reading this file is allowed for you), judge whether its expectation follows from RFC 9111 §3.1/§3.2/§4.3.4 (retained LANE/.ufo/waves/round-99/sources/rfc9111.txt) or from a contract sentence explicitly marked as a lane convention (LC1-LC6); write {D}/hand-review.tsv (`tag\\tagree|disagree\\tbasis`). (2) Judge each lane convention: does the RFC contradict it, leave it open, or require it; is any RFC requirement in §3.2/§4.3.4 silently dropped by the contract (name the sentence). (3) Read the erratum page LANE/.ufo/waves/round-99/sources/eid9185.html and say whether it changes any hand expectation. Write {D}/contract-findings.md.
Acceptance: final line `REVIEWFRESH hand=<agree>/50 contract_findings=<n> rfc_contradictions=<n>`.""")
add("CriticClaims", "critic", f"""Target: falsify both claims as frozen.
Change: (1) C1: construct, in a scratch fixture clone of LANE at {REPAIR}, SKILL.md edits that make c99_registry.py print met=true while the registry is wrong in a way the declared junk-prose limit does NOT cover (ideas: a row whose self-test span runs a different, always-passing command such as `python3 -B scripts/x.py --selftest` on a tool whose `--selftest` silently ignores failure; a table split by a blank line; a header with a duplicate `Owner` column; a row naming a tool only inside a later column; an unterminated fence before the section; a tool under scripts/ with a non-.py/.mjs extension the population ignores; `git ls-tree` quoting of odd names); run the counter on each fixture commit and record output. (2) C2: write candidates (in scratch, scored only with `--candidate-file`) that pass the frozen counter while violating the contract, or fail while honouring it; seed-grinding is out of scope unless you show the default seed can be steered by the candidate. (3) Predicate holes: anything in freeze.md that a do-nothing or junk landing could satisfy. Write {D}/attacks.md (each attack: fixture/candidate path, command, observed line, rc, escape yes/no).
Acceptance: final line `CRITIC c1_escapes=<n> c2_escapes=<n> predicate_holes=<n>`.""")
add("MutCounters", "mutation-tester", f"""Target: mutation-test both frozen counters' own batteries.
Change: (1) Copy LANE/.ufo/waves/round-99/c99_registry.py and c99_fresh304.py into your scratch; make ≥12 single-point mutants of each predicate-bearing line (c99_registry: REQUIRED header set, cell-count check, names_path boundary, verdict_ok regexes, owner check, FORBIDDEN/ASSIGN/PLACEHOLDER handling, fence/comment stripping, population filter, dangling token regex, met condition; c99_fresh304: _etag grammar, strong/weak comparison, LC2 correspondence, LC3 tie, no-validator single rule, exclusion set, Connection parsing, judge(), met condition, seed derivation). (2) Run each mutant against (a) its own --selftest and (b) the committed controls (re-run controls.sh's commands for that counter against the mutant in your scratch; for c99_registry use a scratch clone with fixture commits; never commit in LANE). A mutant is killed when any of those changes verdict. Write {D}/mutants.tsv (`counter\\tmutant\\tline\\tkilled_by|SURVIVED`) and {D}/survivors.md (each survivor: a concrete input that would separate it, as a recipe for the next round).
Acceptance: final line `MUT registry=<killed>/<n> fresh304=<killed>/<n>`.""")
add("SentinelScope", "sentinel", f"""Target: execution-boundary review of c99_registry.py (it EXECUTES commands taken from SKILL.md cells) and of c99_fresh304.py's candidate runner.
Change: (1) c99_registry.py run_span(): enumerate what a SKILL.md row can make the counter execute (any binary on PATH? relative paths escaping the extracted tree? env leakage? writes outside --work? network?) and whether the FORBIDDEN/ASSIGN filters can be bypassed (e.g. quoting, backslashes, `$VAR` expansion — note shlex does not expand); prove each with a harmless PoC in a scratch fixture clone only. (2) c99_fresh304.py run_candidate(): what a candidate can do during scoring (read the counter source or frozen oracle to compute answers, write outside its case dir, persist state between cases, network); PoCs only via `--candidate-file`, confined to your scratch. (3) For each vector: severity for THIS round's verdicts (could it falsify met=true?) and a fix recipe. Write {D}/vectors.md.
Acceptance: final line `SENTINEL vectors=<n> verdict_affecting=<n> blocking=<n>`.""")

spec = {"wave": "kake-r99-w1", "reportDir": ".ufo/waves/round-99/w1", "maxLanes": len(items),
        "context": context, "items": items}
json.dump(spec, open(W + "/w1-spec.json", "w"), indent=1, ensure_ascii=False)
print(len(items), "items")
