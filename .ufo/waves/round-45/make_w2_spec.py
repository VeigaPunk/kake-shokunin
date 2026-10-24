#!/usr/bin/env python3
"""Build the round-45 wave-2 spec (falsify wave, 32 seats, policy v1 band 32-64).

Wave 1 built and measured; wave 2 attacks what landed: it re-runs every counting
command, re-derives every receipt-backed figure, re-attacks both claim predicates and
their NOT-MET-as-declared dispositions, mutation-tests the new gates (driver v2, matrix
runner, freshness runner, counter v6) and re-opens the two new source rows. Every item
names what it attacks. Seats are read-only over corpus/SCORECARD except their own report.
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
WAVE = ".ufo/waves/round-45/w2"
SCRATCH = "/fast/scratch/hyaku/kake-r45"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim \u2014 let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can be parallelized. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

TIMEBOX = """Time-box: return within 15 minutes with your best findings+evidence; partial results are acceptable.
You are an independent leaf: never block on or wait for another seat; if a needed artifact is absent, record the dependency as a finding and return."""

CTX = """# Goal
Kake round 45 wave 2 (falsify wave, 32 seats). Lane: kake-shokunin (axes: operability,
freshness). Wave 1 built and measured; your job is to ATTACK what landed, not to extend
it. The L1 (kake-r45) is sole writer of lane history; you do NOT commit, push, or edit
files outside your named write paths. This wave you write ONLY your report at
LANE_PH/WAVE_PH/<YourSeatName>.md — every seat here is read-only over the lane except
that file (mutation tests run on scratch copies, never in the tree).

Lane repo: LANE_PH. Scratch: SCRATCH_PH/<YourSeatName>/ (create it; temp files there only).

# Round state (measured at tip; do not re-declare)
- C1 (operability): frozen v1 accepts 3/3 invalid receipt classes; driver v2
  (c45_audit.py sha256 f3c3171b...) refuses all three (named counter_error /
  tool_absent / stale_receipt) and re-certifies the honest cohort 27/27 + build 3/3;
  counting command python3 -B .ufo/waves/round-45/c45_matrix.py --stage before|after.
  VERDICT recorded: NOT MET as declared -- the frozen sentence's causal clause ("over the
  invoked counter bytes") is unfalsifiable by mtime+self-reported sha
  (w1/CriticC1Predicate.md); bounded repair verified; routed to the operator.
- C2 (freshness): legs (a) selftest kills 2/4 -> 4/4 and (b) v4 receipt predicate
  names class runs true -> false verify; leg (c) FALSIFIED as declared -- the named
  claim receipt re-derives 26 class-only + 1 mixed + 0 met, not the frozen 22/1/4
  (that tuple is the earlier 23-witness receipt's). Counting: c45_freshness.py.
- Corpus: S133 admitted (Python subprocess docs), S134 rejected (SO answer); lesson
  round-45 Mistakes 14-15; knowledge receipt-integrity.md; registry 134 rows.

# Frozen — never edit
.ufo/waves/round-44/**, .ufo/waves/round-43/verification/**, controls-27.tsv,
controls-r43/, classes/, and every round-43/44 receipt. Do not edit ANY committed file;
mutants are scratch copies.

# Report
Write LANE_PH/WAVE_PH/<YourSeatName>.md: what you attacked, exact commands, verbatim
decisive output, verdict on the named attack. Unrun check = reported unrun; never
fabricate. Every `Report:` trailer path is relative to LANE_PH — write it at
LANE_PH/<that path>.

# Bounds
Read-only over the lane except your report; scratch writes under your dir only. Never
git commit/jj/push; never edit MANIFEST.json, fleet scripts/, templates/, route tables,
mcp.json, .ufo/state/. Never `agent://all`. Tool installs authorized (read
/home/vgpnk/.omp/agent/RULES.md first; record tool/version/channel/reason). PACMAN IS
PAUSED host-wide: no pacman transactions; use uv tool/npx/~/.local/bin; never
-Sy/-Syu/-U/-R.
""".replace("LANE_PH", LANE).replace("SCRATCH_PH", SCRATCH).replace("WAVE_PH", WAVE)


def item(name, role, axes, body):
    return {"name": name, "role": role, "axes": axes,
            "prompt": GODSPEED + "\n# Target\n" + body +
            "\n" + TIMEBOX +
            "\n# Acceptance\nPaste the decisive command output into your report; state pass/fail "
            "against the item's named attack; name every file you wrote.\n"}


L = LANE
S = SCRATCH

items = [
    # ---- executor re-runs (the counting commands, fresh) ----
    item("ReRunMatrixBefore", "executor", ["operability"],
         "Attack target: the C1 before receipt. Re-run `python3 -B .ufo/waves/round-45/c45_matrix.py "
         "--stage before` from " + L + " (expect several minutes: it runs the honest 27-control "
         "cohort under v1). Verify the fresh verification/matrix/before.json records invalid_accepted=3 "
         "and honest 27/3 valid; compare its fixture cohort paths and driver sha against the committed "
         "receipt; exit code must be 0. Report any drift between the fresh receipt and the committed one."),
    item("ReRunMatrixAfter", "executor", ["operability"],
         "Attack target: the C1 after receipt. Re-run `python3 -B .ufo/waves/round-45/c45_matrix.py "
         "--stage after` (the heavy honest v2 cohort). Verify the fresh after.json records "
         "invalid_accepted=0, rejections_named=3 with classes [counter_error, stale_receipt, "
         "tool_absent], honest_witnessed=27, honest_build_met=3, and exit 0. Note: the honest leg "
         "re-runs the full 27-control counter audit -- budget your time; if it cannot finish inside "
         "your box, run the three fixture legs only by invoking the driver directly over each fixture "
         "and record the honest leg as unrun."),
    item("ReRunFreshness", "executor", ["freshness"],
         "Attack target: the C2 receipt. Re-run `python3 -B .ufo/waves/round-45/c45_freshness.py`; "
         "verify it prints selftest_kills before=2/4 after=4/4, "
         "v4_predicate_names_class_runs before=true after=false, and witness_split "
         "class_only=26 mixed=1 met=0; exit 0; verification/freshness/freshness.json refreshed."),
    item("ReRunLedgerGate", "executor", ["operability", "freshness"],
         "Attack target: round-44 C2 no-harm. Run `python3 -B scripts/ledger_latest_check.py --root .` "
         "and `--selftest` at the current tip (after all round-45 SCORECARD/LOG edits). Must print "
         "'3 figures, 0 mismatches' exit 0 and selftest 2/2. Any mismatch = the round-45 edits harmed "
         "the r44 gate: report as the top finding."),
    item("ReRunCensusSelftest", "executor", ["freshness", "operability"],
         "Attack target: registry conformance + gate selftests. Run "
         "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root "
         "/home/vgpnk/Projects/shokunin kake (must exit 0, no E-class rows) and "
         "`python3 -B .ufo/waves/round-45/c45_audit.py --selftest` (exit 0). Record the row count."),

    # ---- reviewer re-derivations ----
    item("RederiveSplit", "reviewer", ["freshness"],
         "Attack target: the C2(c) correction. Independently re-derive the witness split from the "
         "named claim receipt .ufo/waves/round-44/verification/claim/after-final/after-v5.json "
         "(sha256 9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1): confirm 26 "
         "class-only + 1 mixed + 0 met, and confirm 22/1/4 comes ONLY from the earlier receipt "
         "verification/claim/after-v5.json (sha256 2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902). "
         "Verify the SCORECARD append names both sha256s correctly."),
    item("RederiveV4Receipt", "reviewer", ["freshness"],
         "Attack target: the C2(b) after receipt. jq verification/v6v4/counter-v4.json: predicate "
         "names only the eleven v4 runs (no 'class runs' phrase), classesMode v4, classRuns [], "
         "runs keys exactly A-F + T1-T5, exit code 0 recorded in counter-v4.txt, counterSha256 equals "
         "sha256(c45_count.py). Also jq the committed before receipt verification/claim/v4-final/v4.json "
         "and confirm its predicate DOES name the ten class runs (before=true)."),
    item("RederiveMutantsV1", "reviewer", ["operability"],
         "Attack target: the C2(a) before-state. Run python3 -B .ufo/waves/round-45/mutants/mN.py "
         "--selftest for N=1..4; confirm exactly m1/m3 exit 1 and m2/m4 exit 0 (2/4 killed). Quote "
         "the exits. Also confirm the four v1 mutants differ from the frozen v1 driver by exactly the "
         "one-line mutation each (diff and verify the mutation matches the MutClassGate definitions)."),
    item("RederiveMutantsV2", "reviewer", ["operability"],
         "Attack target: the C2(a) after-state. Run python3 -B .ufo/waves/round-45/mutants/mN_v2.py "
         "--selftest for N=1..4; confirm 4/4 exit 1. Verify each mN_v2.py equals the committed "
         "c45_audit.py except the one documented mutation line (diff)."),
    item("AttackMeasurementAppend", "reviewer", ["calibration"],
         "Attack target: SCORECARD.md round-45 measurement append (the section after 'Round 45 — C1 "
         "and C2 measured'). EVERY number in it must re-derive from the receipt it names: check "
         "invalid_accepted 3/0, rejections_named 3, honest 27/3, kills 2/4 and 4/4, the v4 flags, "
         "both receipt sha256s, and both instrument sha256s. Any number without a receipt or any "
         "receipt that does not contain the number = defect."),
    item("AttackHonestIdentity", "reviewer", ["operability"],
         "Attack target: the matrix's honest-leg identity validation. Read c45_matrix.py "
         "run_honest_leg: list every identity check (counter sha, controls==27, ok, witnessed==27, "
         "build 3/3, errors empty). For each, name the cheapest forged receipt that would pass it "
         "while being dishonest, or state why none exists. Is the validation complete relative to "
         "the C1 claim's honest clause?"),
    item("AttackV2Scope", "reviewer", ["operability"],
         "Attack target: C1 kill rule 3 (no reads beyond v1's). Compare the file reads of "
         "c44_audit.py and c45_audit.py (grep open(/read_json/etc). v2 must read no control file "
         "beyond what v1 read, and no network. Report the read set of each and any v2-only read."),
    item("AttackSourcesRows", "reviewer", ["freshness"],
         "Attack target: the S133/S134 registry rows. Run the CORPUS.md manual census commands over "
         "corpus/SOURCES.md (row count 134, malformed 0, tier histogram, status histogram, duplicate "
         "ids empty, enum violations empty); verify S133/S134 have 11 cells each, tier A/C matches "
         "the scope cell, S134's teaches opens 'REJECTED:' with a flip, and every used-by path "
         "exists. Report any defect."),
    item("AttackGateQuotes", "reviewer", ["freshness"],
         "Attack target: the lesson Gate table. Each of the S133/S134 rows: quote <=25 words, "
         "located (section/paragraph), per-row label, access date 2026-10-24, and the quote occurs "
         "in the retained bytes (.ufo/waves/round-45/sources/subprocess.html for S133; the SO API "
         "JSON for S134). Run the round-34 gate_reject_check.py unmodified against a scratch copy "
         "holding the table if feasible, else verify the reject row shape by hand."),
    item("AttackMatrixReceipt", "reviewer", ["operability"],
         "Attack target: the matrix's printed line vs its JSON receipt. verification/matrix/"
         "before.json and after.json must contain exactly the fields the SCORECARD append cites: "
         "invalid_accepted, rejections_named, named_classes (3 distinct for after), "
         "honest_witnessed, honest_build_met, per-fixture cohort paths and driver_sha256 matching "
         "the committed driver bytes. Also check the append's arithmetic honesty: the frozen text "
         "once said '9 rejected rows' where 3 classes x (control + 3 builds) = 12 -- the correction "
         "must be recorded, not silently fixed."),
    item("AttackLessonMistakes", "reviewer", ["calibration"],
         "Attack target: corpus/lessons/round-45.md ## Mistakes entries 14-15. Each must carry "
         "class, evidence pointer, captured-by, fix, and an able-to-fail demonstration that now "
         "exists (matrix receipts). Verify entry 14's fix description matches the landed v2 bytes "
         "(line refs may drift; function names must match) and entry 15's red state (the two "
         "receipts) is real."),
    item("AttackKnowledgeEntry", "reviewer", ["freshness"],
         "Attack target: corpus/knowledge/receipt-integrity.md. Provenance trio present "
         "(source/verified-at/recheck first)? Every count carries its command? Opinion marked as "
         "opinion? The named residual limit (CriticC1Predicate) faithfully represented? The v2 "
         "sha256 quoted matches the committed bytes?"),

    # ---- critics ----
    item("AttackC1Sentence", "critic", ["operability"],
         "Attack target: the C1 NOT-MET-as-declared disposition. Re-read w1/CriticC1Predicate.md "
         "and the frozen sentence (SCORECARD 'Round 45 — C1 and C2 declared'). Is the L1's "
         "disposition honest? Specifically: (1) could the sentence have been read as the bounded "
         "three-fixture claim all along (in which case declaring NOT-MET over-reaches)? (2) is "
         "routing to the operator a punt or genuinely operator-owned (trust boundary)? (3) does the "
         "bounded verification actually prove the three routed defects closed? Verdict: disposition "
         "sound / unsound, with the exact sentence at issue."),
    item("AttackC2Composition", "critic", ["freshness"],
         "Attack target: the C2 NOT-MET-as-declared disposition. The conjunctive MET failed on leg "
         "(c) alone while (a)/(b) verify. Is reporting the whole claim NOT-MET honest, or should "
         "(a)/(b) be reported as verified sub-moves (the SCORECARD append does report them)? Check "
         "the append for any place where the failure of (c) silently drags down (a)/(b) or where "
         "(a)/(b) are inflated into more than they are."),
    item("AttackFixtureShapes", "critic", ["operability"],
         "Attack target: fixture fidelity of the four invalid/stale fixtures (kill rule 5). Using "
         "w1/ScoutReceiptShape.md's schema, verify each fixture receipt matches a real "
         "counter-observable shape field-by-field (seed/met/runs/caughtBy/counterSha256/note/exit), "
         "and that fixtures/stale-backdate/fake_counter.py's receipt is reachable from real counter "
         "code paths (only mtime is synthetic). A shape real bytes cannot produce = strawman."),
    item("AttackV6Diff", "critic", ["freshness"],
         "Attack target: counter v6 minimality (C2 kill rule 1). Re-hunk-classify EVERY hunk of "
         "v6diff/v5-v6.diff: allowed classes = docstring-header, predicate-text (+ the one-line "
         "module-level PREDICATE alias). ANY other hunk = FAIL. Then check the smuggle vectors "
         "w1/ReviewKillRules.md raised: does the receipt-construction line carry ratioLimit/reps "
         "changes? Is RATIO_LIMIT or REPS or the run list touched anywhere? Is PREDICATE_V5 "
         "byte-identical to the frozen PREDICATE string (python compare)?"),
    item("AttackV2Regression", "critic", ["operability"],
         "Attack target: driver v2 interface compatibility with v1 (kill rule 4's surface). "
         "Enumerate v1's observable interface (CLI flags/defaults, summary fields, row fields, "
         "witnessedByClass txt format, exit codes, tools/ layout, build-N naming) from "
         "c44_audit.py and verify c45_audit.py preserves each, using the in-memory selftest rows "
         "and one fixture run for evidence. Any silent interface change = defect; check especially "
         "that rows now carry error/_valid fields ADDITIVELY (old fields unchanged) and the summary "
         "keeps every v1 field."),
    item("AttackScorecardHonesty", "critic", ["calibration"],
         "Attack target: the whole round-45 SCORECARD/LOG surface for overstatement. Grep the "
         "round-45 sections for any wording that claims a claim PASSED/MET/admitted, prettifies the "
         "two falsifications, or omits the named residual hole. Also check LOG.md's round-45 entries "
         "and the lesson for the same. Honest-stop compliance is the attack: report any inflation."),

    # ---- mutation-testers ----
    item("MutMatrixRunner", "mutation-tester", ["operability"],
         "Attack target: c45_matrix.py able-to-fail. In scratch, build >=3 mutants of c45_matrix.py: "
         "(1) honest identity validation removed; (2) after-stage expectation loosened "
         "(invalid_accepted==0 changed to <=1); (3) the stale fixture swapped for the SIGKILL one "
         "without adjusting expectations. Run each mutant --stage after (fixture legs only if time "
         "is short; record the honest leg as unrun) and show each mutant CERTIFIES (prints PASS / "
         "exit 0) where the honest runner fails it -- or that it dies, reporting which. A mutant "
         "that passes = the matrix cannot fail = C1's counter is decorative."),
    item("MutFreshnessRunner", "mutation-tester", ["freshness"],
         "Attack target: c45_freshness.py able-to-fail. In scratch, build >=3 mutants: (1) split "
         "read from the WRONG receipt (verification/claim/after-v5.json) -- must print 22/1/4; "
         "(2) v4_after read from the committed r44 v4.json -- must print true; (3) after-kills read "
         "from the v1 mutant set -- must print 2/4. Show each mutant prints its wrong values while "
         "the honest runner prints the measured truth."),
    item("MutV2GateFinal", "mutation-tester", ["operability"],
         "Attack target: driver v2's shipped selftest against the FINAL bytes (w1/MutDriverV2Spec "
         "ran against an earlier snapshot). Rebuild its six spec mutants (exit gate removed; note "
         "gate removed; freshness window removed; counter-sha binding removed; invalid rows counted "
         "as not-met; build-count pin removed) as scratch copies of the committed c45_audit.py and "
         "run --selftest against each: all six must exit 1, the honest bytes exit 0. Also rerun "
         "their m8/m10 unwired-gate class (control/build row builders ignore the gate): the "
         "end-to-end cohort must kill them -- verify, since the selftest was extended for exactly "
         "this."),
    item("MutCounterV6Final", "mutation-tester", ["freshness"],
         "Attack target: counter v6 detectors against the final bytes (w1/MutCounterV6Spec ran "
         "against an earlier banner). Rebuild its four mutants (PREDICATE_V5 changed; classRuns "
         "populated in v4; a G-run inserted into the v4 runs; provenance header wrong) as scratch "
         "copies of the committed c45_count.py and show each is killed by its detector (byte-compare, "
         "receipt-fields from a fresh --classes v4 run, diff-audit, docstring check). The "
         "module-level PREDICATE alias must NOT mask a PREDICATE_V5 change -- check the detector "
         "compares PREDICATE_V5, not the alias."),
    item("AttackStaleBackdate", "mutation-tester", ["operability"],
         "Attack target: the stale-backdate fixture's ability to fail the after stage. Build two "
         "scratch variants of fixtures/stale-backdate/fake_counter.py: (1) WITHOUT the os.utime "
         "backdate (fresh mtime) -- run it under the real v2 driver --expect witnessed: v2 must "
         "ACCEPT it as a witness (exit 0 ok=True), proving the fixture carries the refusal; (2) with "
         "a self sha of zeroes -- v2 must name stale_receipt via the sha branch. Show both runs."),
    item("AttackNotMetGate", "mutation-tester", ["operability"],
         "Attack target: the not-met half of C1. Build a scratch mutant of c45_audit.py that lets "
         "an invalid receipt count as not-met (weaken not_met_rows to skip validity) and a fixture "
         "with --expect not-met where the only row is invalid: the mutant must certify not-met while "
         "the honest driver refuses. Demonstrate both, then confirm the shipped --selftest kills "
         "the mutant (it should: the cohort's honest not-met leg and the error-row asserts)."),

    # ---- scouts ----
    item("ReopenS133", "scout", ["freshness"],
         "Attack target: S133's continued truth. Re-fetch "
         "https://docs.python.org/3/library/subprocess.html and compare against the retained bytes "
         ".ufo/waves/round-45/sources/subprocess.html: does the quoted sentence 'A negative value -N "
         "indicates that the child was terminated by signal N (POSIX only).' still occur verbatim at "
         "Popen.returncode? Record HTTP status, byte size, sha256, and whether the page changed "
         "(recheck=on-release row: is a re-open due?)."),
    item("ReopenS134", "scout", ["freshness"],
         "Attack target: S134's reject reason. Re-fetch the SO answer via the Stack Exchange API "
         "(questions/24139389/answers?site=stackoverflow&filter=withbody). Does the answer still "
         "carry only the point S133 covers? Is the '-11 is SIGSEGV' mapping still absent from the "
         "Python docs page (supporting the tier-C scope limit)? Record HTTP status and sha256; "
         "verdict: reject reason still holds / stale."),

    # ---- sentinel ----
    item("SentinelFinal", "sentinel", ["operability"],
         "Attack target: frozen-set integrity at round end. Rebuild the sha256 guard over "
         ".ufo/waves/round-44/{c44_audit.py,c44_count_v5.py,c44_placebo.py,controls-27.tsv,"
         "controls-canary.tsv}, every file under classes/, classes-placebo/, controls-r43/, and "
         "every file under round-43/verification/ and round-44/verification/ EXCLUDING __pycache__ "
         "entries (generated caches, remediated this round -- name the exclusion and why), and "
         "compare against .ufo/waves/round-45/verification/sha-guard/before.sha256 modulo that "
         "exclusion: every committed byte must match. Also guard scripts/sitemap_audit.py and "
         "scripts/ledger_latest_check.py. Any committed-byte drift = top finding."),
]

spec = {"wave": "kake-r45-w2",
        "milestone": "round-45 wave 2 (falsify: re-runs, re-derivations, claim attacks, gate mutations, source re-opens)",
        "maxLanes": 64,
        "axes": ["operability", "freshness"],
        "reportDir": ".ufo/waves/round-45/w2",
        "context": CTX,
        "items": items}

out = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w2-spec.json"
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1)
from collections import Counter
print(out, len(items), Counter(i["role"] for i in items))
