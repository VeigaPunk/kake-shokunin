#!/usr/bin/env python3
"""Generate the round-60 wave w1 (v1 policy, build + recon + first falsifiers). Output: w1-spec.json beside this file."""
import json
import os
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W = f"{LANE}/.ufo/waves/round-60"
R = f"{W}/w1"
SRC = f"{W}/sources"
KNOW = f"{LANE}/corpus/knowledge"
STAGED = "/home/vgpnk/Projects/shokuknow/merge/kake"
FLEET = "/home/vgpnk/Projects/shokunin"
BASE = "97cdc122379711c2b02a8970752c8782da3ac81d"
SCR = "/fast/scratch/hyaku/kake-r60"
W59 = f"{LANE}/.ufo/waves/round-59"

# Godspeed lead (prompt §3): `/skill:godspeed` followed by the verbatim bytes of the host binding's directive file.
GODSPEED = "/skill:godspeed\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md", encoding="utf-8").read() + "\n"

CONTEXT = (
    "/skill:godspeed\n"
    "Round-60 kake wave w1 (BUILD wave of two v1 waves; wave w2 will attack what you produce). Lane repo: " + LANE + ". Your tools start at "
    "the FLEET root (" + FLEET + "), not the lane: FIRST `mkdir -p " + SCR + "/<your seat name> && cd` there; use absolute paths for every "
    "read and write; never use a relative redirect outside your scratch dir. Every `Report:` trailer path is relative to " + LANE + " — "
    "write it at " + LANE + "/<that path> (i.e. " + R + "/<Seat>.md), never under the fleet root. Seats never mutate the fleet repo, "
    "sibling lanes, lane jj state or the lane Git index: write ONLY your own report file and, when your item says so, files inside "
    + R + "/<Seat>.files/ — no other path; no `git add/commit/stash/checkout/reset/pull/push` and no jj mutation in the lane. Read-only "
    "git (show, log, ls-tree, rev-parse, diff, cat-file) is fine. Scratch: every clone, fixture and work dir lives under " + SCR +
    "/<your seat name>/ (pass it as TMPDIR / --work; `/tmp` only for files under 50 MB, never cited); use `git clone -q --shared` rather "
    "than full clones; delete your scratch dir before you finish (copy what you cite into your .files/ first; `trap 'rm -rf -- \"$S\"' "
    "EXIT`). Fixture repos: `D=$(mktemp -d -p " + SCR + "/<seat>) && git -C \"$D\" init -q`, every later git call names `-C \"$D\"`, "
    "verify `git -C \"$D\" rev-parse --show-toplevel` equals `$D` before the first commit, commit only with `-c user.name=selftest -c "
    "user.email=selftest@local`; never commit anywhere else. /home/vgpnk/Projects/shokuknow is read-only (read files; never run its "
    "campaign tools); sibling lane repos are read-only. Round facts: contract " + W + "/contract.md (+ contract.json) — READ IT FIRST; "
    "base revision " + BASE + " (lane master at round open); access date 2026-10-27 (UTC). Claims: C1 calibration — the SKILL.md gate "
    "registry's status labels (live / historical / never-met) of the 28 round 48-59 counters match their observed exits (counter "
    "c60_gate_status.py, to be built this wave); C2 operability — a new tool scripts/append_guard.py whose append-only rule accepts a "
    "tagged in-file correction ([rNN-correction YYYY-MM-DD]) and catches rewrites/deletions (counter c60_guard_cases.py, 24 cases, to be "
    "built this wave); C3 freshness (sourced) — row S425's scope overstatement superseded by S427, user-triggered fetchers' robots.txt "
    "posture re-verified on S428, the assimilated robots.txt limits entry on S429 (counter c60_quote_truth.py derived from the round-59 "
    "counter, to be built this wave). Retained bodies: " + SRC + "/S427.html, S428.html, S429.html (+ receipts.json; fetched "
    "2026-10-27T04:03Z). Quote rule: every quote 6..25 whitespace tokens and <= 160 characters, a substring of ONE whitespace-collapsed "
    "text node of the retained body's article block (`class=\"devsite-article-body` .. `<devsite-content-footer`), page-unique; ASCII "
    "double quotes only (round-59 helper for the S425/S426 bodies: " + W59 + "/span_tools.py). NO seat scores an after-state: the "
    "counters are frozen by the L1 after this wave, before any measurement. Never fabricate: an unrun check is reported as unrun; mark "
    "unverified statements [INFERENCE]. No credentials, tokens, op:// refs or private URLs in any report. Tooling authorization "
    "(operator, 2026-10-19): you may install or upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official "
    "channels, update-safety gate; record tool/version/channel/reason). Pacman guard: all pacman transactions are PAUSED host-wide — never "
    "run pacman (no -S, -Sy, -Syu, -U, -R); install via `uv tool`/`npx`/an official binary in ~/.local/bin or report the need; never "
    "restart a host service. The host is loaded: generous timeouts, no retry loops. Report format: first line `# <your seat name>`, then "
    "the sections your item names, factual, under ~150 lines (code goes in .files/, not inline); last line `VERDICT: <one line>`. The L1 "
    "(KakeR60) holds the planner seat and integrates; you are a leaf: no subagent dispatch except an executor's single read-only labrat probe."
)

items = []


def add(name, role, text):
    for k, v in (("{W}", W), ("{R}", R), ("{LANE}", LANE), ("{SRC}", SRC), ("{KNOW}", KNOW), ("{STAGED}", STAGED), ("{FLEET}", FLEET),
                 ("{BASE}", BASE), ("{SCR}", SCR), ("{W59}", W59)):
        text = text.replace(k, v)
    items.append({"name": name, "role": role, "prompt": GODSPEED + text})


POP = ("the 28 population counters (contract § Claim C1: `.ufo/waves/round-N/[subdir/]cN_*.py`, 48 <= N <= 59)")
ROWRULE = ("Draft for each counter a COMPLETE 8-cell SKILL.md registry row in the lane's format (`| Name | Kind | Entry command | Verdict map | "
           "Self-test | Pinned values / frozen proof | Write scope | Owner |`; copy the style of {LANE}/SKILL.md lines 1283-1310): Kind = `gate (live; "
           "...)` or `gate (historical: green at its round-N measured revision <40-hex> ...; red on later trees by design — <why>)` or `gate (never "
           "met: red at its round-N measured revision <40-hex> ...)`; the entry command must be the counter's real CLI (`python3 -B <path> --root . "
           "--revision <commit>`); the verdict map must state `0=`, `1=` and the other exit codes the code really uses (read the code); self-test cell "
           "names the real selftest flag or says `none (no selftest mode)`. No `|` inside a cell. Write the rows to {R}/<Seat>.files/rows.md.")

# ---- C1 calibration: gate-status ledger ------------------------------------------------------------
add("ExecC1Counter", "executor",
    "Claim C1. Write the counter {W}/c60_gate_status.py EXACTLY to contract § Claim C1 (population regex, row/label/command/observation/mismatch "
    "rules, scores_held, predicate sentence as the constant `PREDICATE`, exit 0/1/2/64, `--json`, `--work`, `--jobs N` parallel runs, scrub inherited "
    "GIT_*, resolve --revision once to a commit id, --root must be a repository toplevel, every clone under --work or TMPDIR, never /tmp hardcoded, "
    "remove its clones on exit). Output: one line per member `<path> label=<l> e_T=<n> [e_P=<n>] <ok|MISMATCH class>` then the summary line "
    "`C1 gate-status members=<n> mismatches=<k> scores_held=<s>/3 met=<True|False>`. Add `--selftest`: fixture lanes built in scratch "
    "(`git init`, selftest identity) with toy counters that exit 0/1 depending on the revision, covering every mismatch class, every label, "
    "placeholder substitution (incl. `[--fleet <fleet root>]` kept, `[--seed N]` dropped, `TMPDIR=<scratch>` env word), a row inside a fenced block "
    "or HTML comment (does not count), duplicate row, junk row (row_incomplete), a calibration-score-only mutant 2 -> 10 (scores_held fails), and "
    "members != 28. Write the counter to {R}/ExecC1Counter.files/c60_gate_status.py (the L1 copies it into place). Then run it read-only at the "
    "base: `python3 -B <your copy> --root {LANE} --revision {BASE} --work {SCR}/ExecC1Counter/w --jobs 6` and paste the full output. Report "
    "sections: `DESIGN:` (how each contract rule maps to code, line refs), `SELFTEST:` (tally), `BASE RUN:` (verbatim), `CONTRACT AMBIGUITIES:`.")
add("ExecC1Fixtures", "executor",
    "Claim C1, independent test author (do NOT read another seat's counter; work only from contract § Claim C1). Write a standalone harness "
    "{R}/ExecC1Fixtures.files/c60_gate_status_fixtures.py that builds fixture lanes in scratch (git init, selftest identity; a SKILL.md registry, "
    "a SCORECARD.md axis table, toy `.ufo/waves/round-N/cN_x.py` counters whose exit depends on the revision) and runs ANY candidate counter path "
    "given by `--counter <path>` against each fixture, comparing exit code and the mismatch class it prints, one case per contract clause (>= 30 "
    "cases: each structural class, each label/observation combination, placeholder substitution, bracket keep/drop rules, env words, fenced/"
    "commented rows, pin not an ancestor, score mutant, population boundary — e.g. c47_x.py and c60_x.py are not members, `round-53/sub/c53_x.py` "
    "is, `round-53/a/b/c53_x.py` is not). Prove the harness itself discriminates by running it against two trivial counters you write (always "
    "exit 0; always exit 1) and paste both tallies. Report sections: `CASES:` (id, fixture, expected exit, expected class), `HARNESS SELF-CHECK:`, "
    "`CONTRACT AMBIGUITIES:`.")
for nm, members in (("ExecC1Data48", "c48_lint_count.py, c48_quote_truth.py (round 48), c49_order.py, c49_quote_truth.py (round 49)"),
                    ("ExecC1Data50", "c50_durable.py, c50_quote_class.py (round 50), c51_quote_truth.py, c51_wave_ledger.py (round 51)"),
                    ("ExecC1Data52", "c52_gate_registry.py, c52_mutation_ladder.py (round 52; both mentioned in SKILL.md prose but in no table row), and "
                                     "the two registered round-52 rows (c52_quote_truth.py, c52_wave_ledger.py): check their labels"),
                    ("ExecC1Data53", "exec-quality-gate/c53_gate_truth.py (round 53; registered live at SKILL.md line 213, exits 1 at base) and "
                                     "c54_ops_debt.py, c54_s374_calib.py (round 54)")):
    add(nm, "executor",
        f"Claim C1 data, members: {members}. For each: (1) find the round's MEASURED revision(s) — the commit its claim was measured at, from "
        "`{LANE}/SCORECARD.md` `## Round N` sections, `{FLEET}/.ufo/reports/round-N/kake.md`, the round's `corpus/lessons/round-N-verifier-spotcheck.md` "
        "and receipts under `.ufo/waves/round-N/` (quote the line that names it); (2) in a `git clone -q --shared {LANE} {SCR}/<seat>/c` detached at "
        "{BASE}, run the counter `python3 -B <path> --root . --revision <rev>` (TMPDIR=scratch, timeout 1800) at {BASE} and at each measured revision, "
        "record exit and last summary line; (3) say whether it was EVER green (try the measured revision, its parent and the round's final tip) and "
        "the honest label (live if green at {BASE}; historical with the green pin; never-met with the red measured revision). " + ROWRULE +
        " Report sections: `MEMBERS:` (path, measured rev + source line, exit@base, exit@measured, label), `ROWS:` (pointer to rows.md), `NOTES:`.")
add("ExecC1Registered", "executor",
    "Claim C1 data for the 12 REGISTERED members of rounds 55-59 (c55 x2, c56 x2, c57 x3, c58 x3, c59 x3 — SKILL.md lines 1233-1309). For each "
    "row: parse the Kind cell's label and pin per contract § Claim C1; run the Entry command (contract placeholder rules: `<commit>/<rev>/<tip>` -> "
    "revision, `<scratch>` -> scratch dir, `[--fleet <fleet root>]` kept as `--fleet {FLEET}`, `[--seed N]` dropped, `TMPDIR=<scratch>` env) in a "
    "`git clone -q --shared` of the lane detached at {BASE}, at {BASE} and (historical rows) at the pin; also run c57_idresolver_gate.py WITHOUT "
    "--fleet. Report exit, wall time and summary line for every run and every label-vs-observation mismatch AT BASE. Report sections: `RUNS:` "
    "(member, label, pin, e_T, e_P, seconds), `MISMATCHES AT BASE:`, `ENV NOTES:` (anything that depends on the clone location, network or sibling "
    "lanes).")
add("ExecC1Predict", "executor",
    "Claim C1 collision forecast (routed defect R59-D1: a round's own change turned a live gate red unnoticed). In a scratch clone of {BASE}, make a "
    "MOCK commit (selftest identity, scratch only) of round-60's planned changes: append three well-formed 11-cell rows S427/S428/S429 to the "
    "`## Registry` table of corpus/SOURCES.md (copy the URLs from the contract; any plausible cells), add corpus/knowledge/google-user-triggered-fetchers.md "
    "and corpus/knowledge/robots-txt-limits.md (provenance trio + a paragraph), insert a 3-line run starting `  **[r60-correction 2026-10-27]**` into "
    "corpus/knowledge/googlebot-verification.md right after line 38, append a `## Round 60` section to SCORECARD.md and LOG.md, add a "
    "`### Round 60 gate registry additions` table to SKILL.md with one complete row, add scripts/append_guard.py (any stub). Then run all " + POP +
    " (`python3 -B <path> --root . --revision HEAD`, registered entry commands where they exist) on the mock and on {BASE}. Report sections: `RUNS:` "
    "(member, exit@base, exit@mock), `PREDICTED RED:` (each member the round's changes turn red, with the condition that fails and why), "
    "`RELABEL NEEDED:` (which rows must be relabelled historical, with which pin).")
add("CriticC1Cheat", "critic",
    "Claim C1 — attack the PREDICATE and RULES of contract § Claim C1 before any code exists. Find the cheapest ways to reach `members == 28 AND "
    "mismatches == 0 AND scores_held == 3` without honest labels: rows that name the path in a different command (e.g. `--selftest`, or a wrapper "
    "that always exits 0), a pin that is green for the wrong reason, `never-met` abuse, a duplicate path inside a fenced block, labels in a Kind cell "
    "of a different table, running the counter at a different --root, a member made green by editing its frozen expected values, deleting and "
    "re-adding a counter under a new name, Unicode lookalikes in `historical`. For each: does the contract's rule catch it? propose the exact "
    "tightening. Report sections: `CHEATS:` (cheat, caught?, rule), `TIGHTENINGS:`, `VERDICT:`.")
add("CriticC1Population", "critic",
    "Claim C1 — attack the population boundary and the axis label. Is `48 <= N <= 59` honest or cherry-picked? List every `.ufo/waves/round-4[0-7]/` "
    "counter at {BASE} (`git -C {LANE} ls-tree -r --name-only {BASE} -- .ufo/waves`), whether each is registered in SKILL.md, and how its absence "
    "should be disclosed; is a SKILL.md gate registry a 'self-assessment' under {FLEET}/AXES.md calibration (compare round 56's admitted C1 in "
    "{LANE}/corpus/lessons/round-56-verifier-spotcheck.md)? Is `scores_held == 3` a real fix of R59-D2 or a vacuous guard? Report sections: "
    "`POPULATION:`, `AXIS:`, `R59-D2:`, `VERDICT:`.")
add("ScribeC1Section", "scribe",
    "Claim C1 prose. Draft (a) a SKILL.md section `### Round 60 gate-status ledger` that explains the three labels (live / historical / never-met), "
    "the pin rule and the relabel duty (a live gate a round turns red is relabelled with its pin BEFORE measurement, or the round says why — routed "
    "defect R59-D1 {LANE}/corpus/lessons/round-59-verifier-spotcheck.md §6) and that implements considerthese proposal 5 (historical-gate list, "
    "{LANE}/considerthese/2026-10-26.md lines 33) — a table header only, rows to be filled by the L1 from data; (b) a corpus/QUALITY.md criterion "
    "appended in the lane's style (read {LANE}/corpus/QUALITY.md tail, §Round-59 criteria) citing corpus/lessons/round-60.md and the round-59 "
    "gate-collision mistake row. Write both to {R}/ScribeC1Section.files/{skill.md,quality.md}. Report sections: `SKILL SECTION:`, `QUALITY:`, "
    "`GROUNDING:` (file:line for every cited fact).")

# ---- C2 operability: append_guard ----------------------------------------------------------------
GUARD = ("Implement scripts/append_guard.py EXACTLY to contract § Claim C2 (CLI, default scope `corpus/knowledge/**/*.md`, exits 0/1/2/64, finding "
         "lines `<kind> <path>[:<line>]` + summary `files=<n> findings=<k>`, `--json`, committed bytes only via git, GIT_* scrubbed, --root must be "
         "a toplevel, base must be an ancestor). The untagged_insertion rule is EXISTENTIAL: report it iff no alignment of the base lines into the "
         "revision lines makes every non-EOF inserted run start with a visible tag — implement it exactly (e.g. DP over (base index, revision "
         "index, run state)); the tag must be outside `<!-- -->` and outside backtick code spans. Add `--selftest` (fixture repos in scratch, git "
         "init, selftest identity) asserting exit code AND finding kind/path for >= 24 cases including all contract K-cases. stdlib only, "
         "python3 >= 3.10. Write it to {R}/<Seat>.files/append_guard.py. Run its selftest and run it on the real lane: `--root {LANE} --base "
         "fd6303ce5c14b3f892dec586297a942ab6e4193b --revision {BASE}` and `--base 64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 --revision {BASE}` "
         "(paste both outputs). Report sections: `DESIGN:` (alignment algorithm, complexity, tag visibility rules), `SELFTEST:`, `REAL LANE:`, "
         "`LIMITS:`.")
add("ExecGuardTool", "executor", "Claim C2, primary implementation. " + GUARD)
add("ExecGuardTool2", "executor", "Claim C2, second independent implementation for differential comparison (do not coordinate with another seat). " + GUARD)
add("ExecC2Counter", "executor",
    "Claim C2. Write the counter {W}/c60_guard_cases.py EXACTLY to contract § Claim C2: the 24 cases K1..K22, R1, R2 in the contract table (each "
    "a fixture repo `git init` in its own scratch dir under --work, file names/ids/line contents drawn from --seed so a fixture-keyed tool cannot "
    "recognise them), running the tool AS COMMITTED AT --revision (extract `scripts/append_guard.py` with `git show <rev>:scripts/append_guard.py` "
    "into the work dir; a missing tool fails every case), a per-case timeout (hang = fail), pass only on expected exit AND expected finding "
    "kind+path in stdout; `PREDICATE = \"met: cases_passed == 24 of 24\"`; summary `C2 guard-cases <p>/24 met=<bool>`; exits 0/1/2/64; GIT_* "
    "scrubbed; --root toplevel; no /tmp hardcoding; work dir removed on exit. Add `--selftest` running the 24 cases against controls via a hidden "
    "`--tool <path>` override: no tool (0/24), always-exit-0, always-exit-1 (no output), a port of c55_readme_index's byte-prefix `head_changed` "
    "rule (read {LANE}/.ufo/waves/round-55/c55_readme_index.py; must fail K2, K15, R1), and a small reference implementation you write inside the "
    "selftest (24/24). Write to {R}/ExecC2Counter.files/c60_guard_cases.py. Report sections: `CASES:` (id, fixture, expected), `SELFTEST:` (control, "
    "tally), `BASE RUN:` (`--revision {BASE}` output: expected 0/24), `CONTRACT AMBIGUITIES:`.")
add("ExecGuardRealLane", "executor",
    "Claim C2 grounding on the real lane. For every commit range that touched corpus/knowledge/**/*.md since round 50 (`git -C {LANE} log --format=%H "
    "--first-parent -- corpus/knowledge`), classify each per-file change as: pure EOF append, tagged mid-file insertion (which tag spelling), untagged "
    "mid-file insertion, rewrite/deletion, new file, rename. Write a short stdlib script for it in {R}/ExecGuardRealLane.files/. State what the "
    "contract's rule would report for `fd6303ce..{BASE}`, `64c0ce12..{BASE}` and the last 10 rounds, and which historical edits it would flag "
    "(these are facts, not failures). Report sections: `CHANGES:` (table), `TAG SPELLINGS:` (each spelling with count and one file:line), "
    "`EXPECTED R1:`, `FLAGGED HISTORY:`.")
add("ScoutTagForms", "scout",
    "Claim C2 tag grounding. Enumerate every correction-marker spelling in {LANE}/corpus/knowledge, SKILL.md and corpus/lessons at {BASE} "
    "(`git -C {LANE} grep -n -E '\\[r[0-9]+[- ]' {BASE} -- corpus SKILL.md`; also `r18 re-census`, `citation-local`, `erratum`) and the rules that "
    "govern corrections ({FLEET}/CORPUS.md 'Corrections are new entries, never rewrites', {FLEET}/PROTOCOL.md, {LANE}/corpus/QUALITY.md, "
    "{LANE}/AGENTS.md). Is the contract's tag regex `\\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\\]` the lane's convention for in-file "
    "corrections? Which other spellings exist and are they in-file insertions? Report sections: `SPELLINGS:` (spelling, count, file:line), `RULES:` "
    "(file:line quotes), `REGEX FIT:`.")
add("CriticC2Semantics", "critic",
    "Claim C2 — attack the append-only SEMANTICS in contract § Claim C2 before code exists: existential alignment vs greedy, EOF-append definition "
    "when the base lacks a final newline, a run inserted before the first base line, a run that starts with a tag but also rewrites meaning, "
    "multiple tags, tag regex too loose (any `[r9-correction 0000-00-00]`) or too strict, a correction appended at EOF without a tag, tags inside "
    "link text or headings, whole-file prepend of a provenance trio (round-21 practice), binary files, very large files (DP cost), symlinked "
    "corpus/knowledge dir, scope globbing (`**` vs nested), renames detected by content. For each: what the rule says, whether the 24 cases test it, "
    "the case to add. Report sections: `CASES:`, `CONTRACT RISKS:`, `VERDICT:`.")
add("RevengerC55Intent", "revenger",
    "Claim C2 / R59-D1 intent. Reverse-engineer {LANE}/.ufo/waves/round-55/c55_readme_index.py (`head_changed` term and the six others), its "
    "round-55 contract ({LANE}/.ufo/waves/round-55/contract.*) and the round-59 collision ({LANE}/.ufo/waves/round-59/a2r1/ReviewerNoHarm.md, "
    "{LANE}/corpus/lessons/round-59.md §Mistakes row gate-collision). What was head_changed protecting against? Does a tagged in-file correction "
    "violate that intent? Can the new guard supersede head_changed without losing a protection (list each)? Report sections: `INTENT:` (with "
    "file:line), `PROTECTIONS:` (each, kept by the guard?), `VERDICT:`.")
add("ProbeAlignment", "executor",
    "Claim C2 algorithm probe. Prototype, in {R}/ProbeAlignment.files/align.py, the existential alignment check of contract § Claim C2 (minimum "
    "number of untagged non-EOF runs over all subsequence alignments; report 0 iff some alignment is clean), measure its time and memory on the "
    "largest file under {KNOW} against a revision with 50 inserted lines, and on a synthetic 5,000-line file; compare with greedy-leftmost and "
    "greedy-rightmost on 200 random fixtures (seeded) and report disagreements. Report sections: `ALGORITHM:`, `COST:`, `GREEDY DISAGREEMENTS:` "
    "(counts + one minimal example each), `VERDICT:`.")
add("ScribeC2Rows", "scribe",
    "Claims C1-C3 registry prose. Draft, in the lane's exact row format ({LANE}/SKILL.md lines 1297-1310), complete 8-cell SKILL.md registry rows "
    "for: `append-guard` (tool, scripts/append_guard.py, contract § Claim C2), `gate-status-counter` (c60_gate_status.py), `guard-cases-counter` "
    "(c60_guard_cases.py), `user-triggered-quote-truth-counter` (c60_quote_truth.py) — exit maps and commands from the contract; selftest tallies "
    "as `<N>` (the L1 fills real numbers; never invent one); and a SCORECARD.md capabilities row for the append guard in the style of "
    "{LANE}/SCORECARD.md lines 191-204. Write to {R}/ScribeC2Rows.files/rows.md. Report sections: `ROWS:`, `CAPABILITY ROW:`, `OPEN NUMBERS:`.")
add("ReviewerGuardSpec", "reviewer",
    "Claim C2 — review contract § Claim C2 against the lane's and fleet's append-only rules ({FLEET}/CORPUS.md 'Corrections are new entries, never "
    "rewrites' and SOURCES rule 2, {FLEET}/PROTOCOL.md §Gate standard, {LANE}/corpus/QUALITY.md §Round-59 gate-collision criterion). Is the "
    "tool a gate (can it fail? self-test over isolated fixtures? exit map?) Does K/R coverage match the rule clause by clause? Is R1 a fair "
    "real-lane case (does fd6303ce..rev contain any non-append change the rule would flag)? Report sections: `FINDINGS:` (severity, issue, fix), "
    "`VERDICT:`.")

# ---- C3 freshness (sourced) --------------------------------------------------------------------------
add("ExecC3Derive", "executor",
    "Claim C3. Write {R}/ExecC3Derive.files/derive_c60_quote_truth.py that generates c60_quote_truth.py from the committed round-59 counter "
    "{W59}/c59_quote_truth.py (version 2; read {W59}/derive_c59_quote_truth.py for the method: `sub()` asserts each replaced snippet occurs exactly "
    "once) implementing contract § Claim C3 conditions C1..C9 exactly: rows S427 (supersedes S425; scope rule), S428, S429; entries "
    "corpus/knowledge/google-user-triggered-fetchers.md (S428) and corpus/knowledge/robots-txt-limits.md (S429); staged name google-robots-txt-limits.md "
    "absent; used-by sets; subjects (`generally ignore`, `cannot enforce`, S427 Gate quote `automatic crawls`); bodies pinned to the sha256 in "
    "{SRC}/receipts.json; S429 is a Search Central page — check its article-block markers and `<title>` form in {SRC}/S429.html and adapt; "
    "`Last updated <date> UTC` must be read inside `<devsite-content-footer` (routed R59-D3); C7 validate receipt path "
    "`.ufo/waves/round-60/controls/validate-append.txt`; C8 mirror pin `.ufo/waves/round-60/assimilation/mirror-pin.json` (164 rows at {BASE}); C9 "
    "on corpus/knowledge/googlebot-verification.md after the base line holding `these fetchers ignore robots.txt rules.` (line 38 at base). Keep "
    "`PREDICATE = \"met: conditions_passed == 9 of 9\"`, GIT_* scrub, revision resolved once. Port the round-59 selftest to the new rows (fixtures "
    "per condition, red and green). Generate the counter into your .files/, run its selftest and run it at {BASE} (expected 0/9, exit 1). Report "
    "sections: `CHANGES:` (each substitution and why), `SELFTEST:` (tally), `BASE RUN:`, `CONTRACT AMBIGUITIES:`.")
add("EntryUserTriggered", "scribe",
    "Claim C3 entry. Draft corpus/knowledge/google-user-triggered-fetchers.md from the retained body {SRC}/S428.html (read the article block only). "
    "Open with the provenance trio: `source: S428 — Google Crawling Infrastructure — Google User-Triggered Fetchers — "
    "https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers — § <h2 that holds the robots sentence> (Last "
    "updated 2026-08-19 UTC)`, `verified-at: 2026-10-27 (retained body sha256 <from receipts.json>)`, `recheck: 180d — <a grep span inside one "
    "text node>`. Body: what a user-triggered fetcher is per the page, its robots.txt posture in the page's words (\"generally ignore\"), how a "
    "publisher can still identify these fetchers (the page's own hostname / IP-range statements if present), the wording difference from S426 "
    "(googlebot-verification.md line 38: \"these fetchers ignore robots.txt rules\" on a page last updated 2026-03-20) stated as a dated "
    "divergence, not a judgement; a `## What this entry does not establish` section. >= 3 page-unique double-quoted spans (rules in context), one "
    "carrying `generally ignore`; each statement traceable to a span or marked as the lane's reading. Check every span with a short script against "
    "the collapsed text nodes and paste the check. Write the entry to {R}/EntryUserTriggered.files/google-user-triggered-fetchers.md. Report "
    "sections: `ENTRY:` (pointer), `SPAN CHECK:`, `READINGS:` (sentences that are the lane's reading).")
add("EntryRobotsLimits", "scribe",
    "Claim C3 assimilated entry. The staged package entry {STAGED}/knowledge/corpus/knowledge/google-robots-txt-limits.md (staged row S415 in "
    "{STAGED}/SOURCES.append.md) is re-grounded as corpus/knowledge/robots-txt-limits.md on row S429 (renumbered by document), from the retained "
    "body {SRC}/S429.html (`Last updated 2025-12-10 UTC`). Refuse every staged sentence the page does not hold (Baidu/Yahoo cross-document "
    "attributions, lane meta-prose, 'only one operator has promised' style glosses) and list each refusal with the reason. Do not duplicate what "
    "{KNOW}/robots-txt-rules.md already holds (RFC 9309 'not authorization'); state what this page adds (cannot enforce; crawlers interpret "
    "syntax differently; a disallowed URL can still be indexed if linked; the 'don't use robots.txt to hide pages' warning) and say what the lane "
    "already held. Provenance trio first (`source: S429 — ... — § <h2> (Last updated 2025-12-10 UTC)`); >= 3 page-unique double-quoted spans, one "
    "carrying `cannot enforce`; check every span against collapsed text nodes and paste the check. Write to "
    "{R}/EntryRobotsLimits.files/robots-txt-limits.md. Report sections: `ENTRY:`, `REFUSED STAGED SENTENCES:` (sentence, reason), `SPAN CHECK:`, "
    "`HELD BEFORE:`.")
add("ScribeCorrectionVerification", "scribe",
    "Claim C3 correction. Draft the append-only insertion for {KNOW}/googlebot-verification.md placed right after base line 38 (`  > \"acts on the "
    "request of a user. Because the fetch was requested by a user, these fetchers ignore robots.txt rules.\"`): a run whose FIRST line starts "
    "`  **[r60-correction 2026-10-27]**`, that cites S428, quotes \"Because the fetch was requested by a user, these fetchers generally ignore "
    "robots.txt rules.\" (check it is one text node of {SRC}/S428.html's article block, page-unique), and states the dated divergence (S426 "
    "`Last updated 2026-03-20 UTC` says ignore; the category page `Last updated 2026-08-19 UTC` says generally ignore) and its publisher-side "
    "consequence without overreach; no base line changed. Write the exact lines to {R}/ScribeCorrectionVerification.files/insert.md and the full "
    "patched file to .files/googlebot-verification.md; prove append-only with `diff` against `git show {BASE}:corpus/knowledge/googlebot-verification.md`. "
    "Report sections: `INSERT:`, `DIFF:`, `SPAN CHECK:`.")
add("ScribeRowsGate", "scribe",
    "Claim C3 registry rows + Gate. Draft three 11-cell rows for {LANE}/corpus/SOURCES.md `## Registry` (copy the cell style of S425/S426 rows): "
    "S427 (URL of S425; `teaches` opens `supersedes S425 —`; corrected `scope`: robots.txt posture is stated for common crawlers and "
    "special-case crawlers only — it must contain `common crawlers` and `special-case crawlers` and must NOT contain `their robots.txt posture`; "
    "used-by `corpus/lessons/round-60.md`), S428 (used-by `corpus/knowledge/google-user-triggered-fetchers.md, corpus/knowledge/googlebot-verification.md`), "
    "S429 (used-by `corpus/knowledge/robots-txt-limits.md`); status `mined`, opened `2026-10-27`, recheck `180d`, anchor `§ <h2> (Last updated "
    "<date> UTC)`; no `|` or `\\|` in any cell. Then the lesson `## Gate` lines (one per id: URL, access date 2026-10-27, anchor, >= 1 quote of "
    "6..25 units with unit count, body sha256 + bytes + HTTP 200 from {SRC}/receipts.json), the R59-D4 erratum paragraph for S425 (what its scope "
    "cell overstated, the page evidence, superseded by S427), and the `## Registry changes (old -> new)` block (164 -> 167). Validate the three "
    "rows with the frozen CORPUS.md census awk (NF==13) on a scratch copy. Write to {R}/ScribeRowsGate.files/{rows.md,gate.md}. Report sections: "
    "`ROWS:`, `GATE:`, `ERRATUM:`, `CENSUS:`.")
add("ScoutStagedS415", "scout",
    "Claim C3 assimilation screen. Read the staged entry {STAGED}/knowledge/corpus/knowledge/google-robots-txt-limits.md and staged row S415 in "
    "{STAGED}/SOURCES.append.md sentence by sentence against the retained body {SRC}/S429.html (collapsed article text). For each staged sentence: "
    "supported (page span), unsupported (count 0), cross-document attribution, or lane meta-prose. Check the staged row's cells for census "
    "defects (escaped pipes, prose recheck, wrong title/anchor/date). Report sections: `SENTENCES:` (staged sentence, verdict, page span or "
    "absence count), `ROW DEFECTS:`, `KEPT:`.")
add("ScoutRejectCommonJa", "scout",
    "Assimilation reject screen. The staged entry {STAGED}/knowledge/corpus/knowledge/common-crawlers-japanese.md cites staged S337 "
    "(`google-common-crawlers?hl=ja`) and the lane registry already holds an S337 row (`grep -n 'S337' {LANE}/corpus/SOURCES.md`). Re-open the "
    "live page (curl -sL --compressed) and the English edition; check the staged quote, its unit count under the round-59 rule, whether the lane "
    "already holds the entry's content (grep {KNOW}), and the id collision. Decide admit/reject with a flip condition. Report sections: "
    "`SOURCE CHECK:` (url, http, quote found?), `HELD ALREADY:`, `DECISION LINE:`.")
add("ExecSpans", "executor",
    "Claim C3 span inventory. Write {R}/ExecSpans.files/spans.py (stdlib; adapt {W59}/span_tools.py to the three round-60 bodies {SRC}/S427.html, "
    "S428.html, S429.html — note S429 is a Search Central page: verify its article block markers) with verbs `nodes <id>` (collapsed text nodes of "
    "the article block), `check <id> <span>` (units, chars, node-substring, page-unique count) and `window <id> <word>`. Then list, per body, every "
    "sentence that states a robots.txt posture or limit and every candidate quote 6..25 units around: S427 `automatic crawls`, `AdsBot`; S428 "
    "`generally ignore`, user-triggered definition, hostnames/IP ranges; S429 `cannot enforce`, `interpret`, `indexed`. Report sections: `TOOL:`, "
    "`SPANS:` (id, span, units, chars, unique?), `MULTI-NODE TRAPS:` (sentences split across nodes).")
add("ExecSourceLive", "executor",
    "Claim C3 live re-open. Independently re-fetch the three round-60 URLs and the S426 URL (curl -sL --compressed, your own UA), compare the "
    "collapsed article text nodes with the retained {SRC}/S427.html, S428.html, S429.html and {W59}/sources/S426.html; report byte and text-node "
    "differences, the printed `Last updated` of each, and confirm the S426 page links the user-triggered category page (href count and the "
    "anchor text). Also confirm S427's article block states robots posture for exactly which categories. Save hashes (not bodies) to "
    "{R}/ExecSourceLive.files/. Report sections: `FETCHES:`, `TEXT-NODE DIFF:`, `S426->S428 LINK:`, `POSTURE BY CATEGORY:`, `VERDICT:`.")
add("CriticEntryOverreach", "critic",
    "Claim C3 — before the entries are written, list for each of the three bodies {SRC}/S427.html, S428.html, S429.html the statements an entry "
    "must NOT make (e.g. 'user-triggered fetchers never obey robots.txt', 'robots.txt hides a page from Google', 'special-case crawlers ignore "
    "robots.txt', 'Google says other crawlers ignore robots.txt'), each with the exact page wording that bounds it, and the qualifiers that must "
    "survive (`generally`, `may`, `with the ad publisher's permission`, `automatic crawls`). Report sections: `MUST-NOT:` (statement, page "
    "evidence), `QUALIFIERS TO KEEP:` (exact words), `VERDICT:`.")
add("CriticC3Conditions", "critic",
    "Claim C3 — attack conditions C1..C9 of contract § Claim C3 before the counter exists: cheapest after-states that meet 9/9 without the claimed "
    "work (an S427 row that copies S425 with only the phrase removed; an entry of three quotes and no reading; a correction run that restates the "
    "stale wording; spans inside page chrome; `generally ignore` quoted from a different page), whether C3's scope-cell rule catches R59-D4's "
    "real defect, whether C9's 6-line window is right. Propose tightenings. Report sections: `CHEATS:` (cheat, met?, why), `TIGHTENINGS:`, "
    "`VERDICT:`.")
add("ReviewerS425Erratum", "reviewer",
    "Routed defect R59-D4. Re-open the S425 row ({LANE}/corpus/SOURCES.md, `grep -n '^| S425'`) and the retained bodies {W59}/sources/S425.html and "
    "{SRC}/S427.html: which categories does the overview page give a robots.txt posture for (quote each sentence), and does any other S425-citing "
    "file ({KNOW}/crawler-identity-signals.md, {KNOW}/crawler-identity.md) repeat the overstatement? Is a superseding row (CORPUS.md SOURCES rule 2) "
    "the right fix versus a lesson-only erratum, and does the census (`{FLEET}/scripts/sources-census.sh`, E04 exemption for `supersedes S`) accept "
    "a same-URL row? Report sections: `POSTURE SENTENCES:`, `OTHER OCCURRENCES:`, `FIX FORM:`, `VERDICT:`.")
add("ExecValidateAppend", "executor",
    "Claim C3 C7 tooling. Write {R}/ExecValidateAppend.files/validate_append.sh (adapt {W59}/validate_append.sh to round 60: a scratch mirror of "
    "the lane's corpus/ at {BASE} plus a 3-row append block in the `## Registry` table plus the admitted knowledge files at their repo-relative "
    "paths, then `{FLEET}/scripts/sources-census.sh validate --file <scratch>/corpus/SOURCES.md`, receipt to "
    "`.ufo/waves/round-60/controls/validate-append.txt` when run by the L1) and the mirror-pin JSON generator (rows, bytes, sha256 of the base "
    "registry at {BASE}). Dry-run it with three dummy well-formed rows (S427..S429) and dummy entries in scratch only; paste output and exit. "
    "Report sections: `SCRIPT:` (pointer), `DRY RUN:`, `MIRROR PIN:` (rows, bytes, sha256 at {BASE}).")
add("ReviewerQuarantineHold", "reviewer",
    "Assimilation quarantine. Re-derive the kake slice of /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md "
    "with the awk in the round prompt ({FLEET}/.ufo/prompts/kake-round-60.md §6 item 10) into scratch, compare with {W}/assimilation/quarantine-slice "
    "and {W59}/assimilation/quarantine-slice; check the round-58 L0 question in {FLEET}/.ufo/l0-questions.md still has no answer; re-open three slice "
    "rows (S142, S161, S206) live and confirm the round-59 verdicts in {LANE}/corpus/lessons/round-59.md §Assimilation still hold. Report "
    "sections: `SLICE:`, `L0 STATUS:`, `RE-OPENED:` (row, url, finding), `VERDICT:`.")

# ---- frontier, mistakes, cross-claim -------------------------------------------------------------------
add("ScribeLessonMistakes", "scribe",
    "Frontier step 3. Draft corpus/lessons/round-60.md `## Mistakes` rows (class · evidence pointer · captured-by · fix; classes from CORPUS.md "
    "vocabulary) for: R59-D1 gate collision (c55 head_changed red on an append-only tagged correction; fix = C2 guard, shown able to fail by the c55 "
    "port control failing K2/K15/R1 and by R2), R59-D2 counter-scope gap (fix = C1 `scores_held == 3`, shown able to fail by the score-only mutant), "
    "R59-D4 row precision (S425 scope cell; fix = S427 + C3 condition C3), and the class behind them (a gate's status label not re-derived after a "
    "round's own change). Each row's evidence pointer must resolve at {BASE} (paths, lines, commits); give the red-before command for each fix as "
    "it WILL be run (the L1 runs it). Read {LANE}/corpus/lessons/round-59.md §Mistakes and round-59-verifier-spotcheck.md §6 first. Report sections: "
    "`MISTAKES:` (markdown rows), `RED-BEFORE:` (command + expected failing text), `CARRIED:` (R59-D3 P6/fixture-sniff/Q1-Q8 with reason).")
add("ScribeConsiderthese", "scribe",
    "Considerthese. Read {LANE}/considerthese/2026-10-26.md (latest) and {LANE}/corpus/lessons/round-59.md §Considerthese. Ground proposal 5 "
    "(historical-gate list) through the lane's own bar: open what it points at (SKILL.md registry rows labelled historical; c56_quote_truth 6/8), "
    "list every SKILL.md row labelled historical at {BASE} with its pin, and draft the lesson §Considerthese paragraph saying how C1 implements it "
    "and what stays open (proposals 1, 2, 4 not taken; why). Report sections: `PROPOSAL 5 GROUNDING:` (file:line), `HISTORICAL ROWS AT BASE:`, "
    "`LESSON TEXT:`, `NOT TAKEN:`.")
add("ScribeSearchLog", "scribe",
    "Frontier step, search log (CORPUS.md SOURCES rule 5). Draft the lesson `## Search log` paragraph for the C3 theme 'robots.txt posture and "
    "limits per Google crawler category': question, where searched (staged package {STAGED}: MERGE-REPORT.md lines mentioning google/robots, "
    "staged rows S415, S337; the lane's held ground: grep {KNOW} for robots/user-triggered/special-case; the pages S427/S428/S429 and the S426 "
    "category table), identified/screened/included/excluded counts with reasons, stop rationale. Every count carries its command. Report sections: "
    "`SEARCH LOG:`, `COMMANDS:`.")
add("ConnSiblingOverlap", "connector",
    "Adjacency. Scan sibling lane repos under {FLEET}/*-shokunin (read-only) for overlap with this round's ground: Google user-triggered fetchers, "
    "robots.txt posture/limits (tabi owns client-side crawler discipline; kake owns publisher-side placement — {LANE}/PROVINCE.md §Adjacent), "
    "append-only/correction guards and gate-status ledgers (kumitate, kotoba, kaidoku?). `grep -rl -i -E 'user-triggered|generally ignore|cannot "
    "enforce|append.only|historical gate' {FLEET}/*-shokunin/{SKILL.md,corpus,scripts} 2>/dev/null`. Report contested scope; absorb nothing. Report "
    "sections: `OVERLAPS:` (lane, file:line, what), `CONTESTED:`, `VERDICT:`.")
add("ConnCrossClaim", "connector",
    "Cross-claim pattern scan. From contract.md: are C1, C2, C3 causally separable as declared (could one land and verify while another fails)? "
    "Shared weaknesses (all three read SKILL.md/SOURCES.md? all rely on git clones under scratch?), interactions (C3's appended rows turn "
    "c59_quote_truth red -> C1 relabel; C2's guard on C3's correction), and one pattern across rounds 55-59 lessons that this round should not "
    "repeat (read {LANE}/corpus/lessons/round-5[5-9]*.md). Report sections: `SEPARABILITY:`, `SHARED WEAKNESSES:`, `INTERACTIONS:`, `PATTERN:`, `VERDICT:`.")
add("CriticAxisLabels", "critic",
    "Attack the axis labels and target sizing of contract.md against the round prompt §9 ({FLEET}/.ufo/prompts/kake-round-60.md: 'Name the axis by "
    "the surface the round changes'; 'A target must be one a do-nothing control cannot reach'; 'Re-scoring a rule the lane already holds on new "
    "inputs ... is quality work'). Is C1 calibration or operability bookkeeping? Is C2 operability (new tool) or a fix of the lane's own gate? Is "
    "C3 freshness or coverage/expansion? For each, the cheapest control that skips the claimed work and whether it meets the target. Report "
    "sections: `C1:`, `C2:`, `C3:`, `VERDICT:`.")
add("CriticD1Collision", "critic",
    "Routed defect R59-D1 forward check. Will any round-60 change break a gate labelled live at {BASE} (SKILL.md rows, including non-population "
    "tools: scripts/id_resolver.py selftest, scripts/corpus-contract.mjs, freshness-sweep, canonical/robots/sitemap/link-preview audits, "
    "c52_gate_registry completeness over the new rows)? Read the contract and the SKILL.md registry; where cheap, run the gate at {BASE} in a "
    "scratch clone. List each predicted collision and the pre-data note the contract must carry. Report sections: `GATES:` (gate, live?, "
    "predicted effect), `NOTES REQUIRED:`, `VERDICT:`.")
add("ReviewerContract", "reviewer",
    "Review {W}/contract.md and contract.json for conformance with the round prompt {FLEET}/.ufo/prompts/kake-round-60.md §2, §2b, §6 items 2, 9, "
    "10: claims 1-3 on distinct axes, lowest axis worked, sourced claim, frozen predicate sentence identical in contract.md and contract.json, "
    "kill rules, do-nothing controls named, routed defects R59-D1..D5 each mapped, assimilation (collision check, renumber by document, quarantine "
    "held), access date. Report sections: `FINDINGS:` (severity, issue, fix), `VERDICT:`.")
add("ScoutOperatorLessons", "scout",
    "Inherited state and operator teaching. List {LANE}/corpus/lessons/operator-*.md (if any) and whether each is reflected in QUALITY.md/SKILL.md; "
    "map every item of {LANE}/corpus/lessons/round-59-verifier-spotcheck.md §6 (R59-D1..D5) and §7 to a round-60 action in contract.md or "
    "'carried'; list kake rows of {FLEET}/.ufo/l0-questions.md and whether any has an operator answer; check `git -C {LANE} status --porcelain` "
    "is empty apart from .ufo/waves/round-60/. Report sections: `OPERATOR LESSONS:`, `SPOT-CHECK MAP:`, `L0 ROWS:`, `INHERITED:`.")

SPEC = {"reportDir": ".ufo/waves/round-60/w1", "maxLanes": 64, "context": CONTEXT, "items": items}
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
    json.dump(SPEC, open(out, "w"), indent=1, ensure_ascii=False)
    c = Counter(i["role"] for i in items)
    attack = sum(c[r] for r in ("reviewer", "critic", "mutation-tester"))
    print(len(items), dict(c), f"attack={attack} ({attack/len(items):.0%})")
