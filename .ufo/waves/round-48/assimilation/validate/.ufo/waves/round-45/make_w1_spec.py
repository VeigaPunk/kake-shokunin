#!/usr/bin/env python3
"""Build the round-45 wave-1 spec (build wave, 32 seats, policy v1 band 32-64).

Round 45 claims (frozen at 3b4c430ae9fa2cf505a7b20f70a34fadf35a065c, before any claim
receipt): C1 = audit driver v2 receipt-integrity hardening (operability; routed from
round-44 w2 ReviewCounterContract defects 1a/1b/1c); C2 = gate standing-claim
re-verification and repair (freshness; MutClassGate coverage caveat, CriticHarmGuard
receipt-text finding, CriticC1Predicate mixed-witness caveat). Seats write only their
named disjoint lane paths; reports at .ufo/waves/round-45/w1/<Seat>.md.
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
WAVE = ".ufo/waves/round-45/w1"
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
Kake round 45 wave 1 (build wave, 32 seats). Lane: kake-shokunin (axes: operability,
freshness; offline audit instruments over committed bytes, local CLI tools only). You are
one leaf seat with one item; the L1 (kake-r45) is sole writer of lane history and the
only integrator — you do NOT commit, push, or edit files outside your named write paths.

Lane repo: LANE_PH. Scratch: SCRATCH_PH/<YourSeatName>/ (create it; temp files there only).

# Round claims (frozen at 3b4c430a; quoted from SCORECARD.md — do not re-declare)
- C1 (operability): driver v2 .ufo/waves/round-45/c45_audit.py refuses witness/not-met
  credit for receipts with (i) counter exit other than 0/1, (ii) note "tool absent",
  (iii) written outside the driver's run window over the invoked counter bytes; honest
  cohort certification unchanged (27/27 witnessed, build 3/3 at 020bc457).
  Before: frozen v1 .ufo/waves/round-44/c44_audit.py (sha256 8ee2c8bf...) accepts 3/3
  invalid fixture classes. Counting: python3 -B .ufo/waves/round-45/c45_matrix.py
  --stage before|after.
- C2 (freshness): (a) shipped v1 --selftest kills 2/4 witness-class mutants (timing-only
  m2, error m4 survive), v2 selftest kills 4/4; (b) v4-mode receipt predicate names ten
  class runs v4 never executes — counter v6 .ufo/waves/round-45/c45_count.py v4 receipt
  names only the eleven v4 runs; (c) the round-44 claim receipt's 27 witnessed controls
  re-derive as 22 class-only + 1 mixed + 4 met. Counting: python3 -B
  .ufo/waves/round-45/c45_freshness.py.

# Frozen — never edit (sha256-guarded)
.ufo/waves/round-44/c44_audit.py, c44_count_v5.py, c44_placebo.py, controls-27.tsv,
controls-canary.tsv, controls-r43/, classes/, classes-placebo/, build_v5.py, and every
round-43/round-44 receipt under .ufo/waves/round-4{3,4}/verification/. The corpus
(knowledge/, SOURCES.md, lessons/) is L1-write-only this wave — scribes deliver drafts
under .ufo/waves/round-45/drafts/ instead.

# Report
Write LANE_PH/WAVE_PH/<YourSeatName>.md: what you did, exact commands, verbatim decisive
output, files written, blockers. Unrun check = reported unrun; never fabricate. Every
`Report:` trailer path is relative to LANE_PH — write it at LANE_PH/<that path>.

# Bounds
You may write only: the lane paths your item names, your scratch dir, your report.
Read-only: fleet repo /home/vgpnk/Projects/shokunin (except reading sibling lanes'
cited files), sibling lane repos except paths your item names, .ufo/state/, watchdog
logs. Never git commit/jj/push; never edit MANIFEST.json, templates/, fleet scripts/,
route tables, mcp.json. Never `agent://all`. Tool installs authorized: you and every
seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md
first (official channels, update-safety gate, record tool/version/channel/reason).
PACMAN IS PAUSED host-wide: all pacman transactions are paused; install via
uv tool / npx / an official binary in ~/.local/bin, or file an L0 question; never
-Sy/-Syu/-U/-R. Report dead ends as dead ends.
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
    # ---- scouts / connector / revenger (recon) ----
    item("ScoutRoutedLedger", "scout", ["operability", "freshness"],
         "Build the canonical routed-defect ledger for round 45. Read: "
         + L + "/.ufo/waves/round-44/w2/ReviewCounterContract.md (defects 1a/1b/1c with line cites), "
         "CriticHarmGuard.md (v4 receipt predicate finding), MutClassGate.md (selftest coverage caveat "
         "and the m1-m4 mutant definitions), CriticC1Predicate.md (mixed-witness caveat), "
         "ScoutSourcesVerify.md (S131 'and §1' leftover), corpus/knowledge/claim-count-derivation.md "
         "(source: S130), and the round-44 verifier spotcheck "
         "(.ufo/reports/round-44/kake.md is fleet-side; use the lane copy "
         "corpus/lessons/round-44-verifier-spotcheck.md). For each defect verify the cited file:line "
         "against current bytes and record exact current line numbers. Output: one table — defect, "
         "severity, evidence pointer (verified line), minimal fix shape, which round-45 claim (C1/C2/"
         "neither) absorbs it."),
    item("ScoutCounterV4Map", "scout", ["freshness"],
         "Map the v4-mode execution path of the frozen counter " + L + "/.ufo/waves/round-44/c44_count_v5.py: "
         "the run-list construction (A-F, T1-T5 under --classes v4), the receipt construction "
         "(predicate/classesMode/classRuns fields), and the PREDICATE string. Record exact line numbers. "
         "Then specify the minimal mode-conditional change for counter v6 (.ufo/waves/round-45/c45_count.py): "
         "PREDICATE_V5 byte-identical to the current PREDICATE string; PREDICATE_V4 = 'met: the tool's exit "
         "code and output equal the round-41 tool's on every generated run (the eleven v4 runs), and its "
         "median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's'. "
         "Also check the docstring provenance-label nit CriticHarmGuard raised (the 'Round-43 version 4 "
         "header follows' line shows the v3 header — record the accurate description of what follows)."),
    item("ConnectorSiblingOverlap", "connector", ["adjacency"],
         "Sibling-overlap scan. The round-45 surfaces are: hardening a Python audit driver that scores "
         "controls against a frozen differential counter (kake/.ufo/waves/round-44/c44_audit.py family), "
         "a sitemap-audit counter family (kake scripts/sitemap_audit.py lineage), and kake corpus SOURCES "
         "repairs. Scan the other lane repos under /home/vgpnk/Projects/shokunin/*/ for current-round work "
         "touching the same surfaces (grep their newest .ufo/waves/ and recent commits for c44_audit, "
         "sitemap_audit, receipt, witness, ledger_latest_check). Report any contested scope with evidence "
         "pointers; report 'no overlap found' with the sweep command if none."),
    item("ScoutDoNothingControls", "scout", ["calibration"],
         "Phase-4 claim-sizing check (do-nothing controls). For each declared claim, define the cheapest "
         "control that skips the claimed work and verify it CANNOT reach the declared after-state: "
         "C1 — the frozen v1 driver (accepts 3/3 invalid classes) and a v2 with the hardening removed; "
         "both must fail the after predicate (they will accept >=1 invalid class). C2 — the frozen v1 "
         "selftest (kills only m1/m3) and the frozen v5 counter in v4 mode (receipt names class runs); "
         "both must fail the after predicate. Junk controls: an honest fixture cohort must stay green "
         "under v1 and v2; mutants m1/m3 must be killed by BOTH shipped selftests. Report the control "
         "table with expected before/after outcomes and how each is scored."),
    item("ScoutReceiptShape", "scout", ["operability"],
         "Extract the exact JSON shape of a real counter receipt and a real audit row from committed "
         "bytes in " + L + ": read .ufo/waves/round-44/verification/claim/after-final/tools/repeat-len-band.json "
         "(a real per-control receipt), build-1.json (a real build receipt), and after-v5.json (the audit "
         "summary rows). List every field with type and example value (seed, met, runs, caughtBy derivation "
         "in the summary, counterSha256, toolSha256, note, classesMode, classRuns, equalRuns). This is the "
         "fidelity contract the C1 invalid fixtures must match — CriticFixtures audits against your "
         "schema; be exhaustive about which fields the v1 audit actually reads vs ignores."),
    item("RevengerReceiptFlow", "revenger", ["operability"],
         "Reverse-engineer the receipt-trust dataflow of " + L + "/.ufo/waves/round-44/c44_audit.py "
         "end-to-end: run_counter (:49-53) -> score() row construction (:151-160) -> semantic_witness "
         "(:63-66) -> expectation_ok (:69-84). Produce the fix-point map for driver v2: for each defect "
         "1a (exit-2 receipt after class divergence), 1b (tool-absent note), 1c (stale planted receipts), "
         "plus the medium defects (not-met counts cannot-evaluate; build count unpinned), name the exact "
         "function and the insertion point where v2's gate must live so that ALL defects close with ONE "
         "receipt-validity mechanism. Verify ReviewCounterContract's line cites against current bytes and "
         "record any drift."),

    # ---- executors (build; disjoint lane write paths) ----
    item("ExecInvalidFixtures", "executor", ["operability"],
         "Build the three invalid-receipt fixture classes and capture the C1 BEFORE receipts.\n"
         "# Write\n"
         + L + "/.ufo/waves/round-45/fixtures/{counter-error,tool-absent,stale-planted}/ each holding: "
         "controls.tsv (one control row; use a copy of an existing control source, e.g. "
         "controls-r43/headtail-v1.py, named ctl1), the fake counter or planted receipts per class, and "
         "a README stating the real-counter provenance of every receipt field (match committed receipts "
         "under .ufo/waves/round-44/verification/claim/after-final/tools/ — see ScoutReceiptShape's schema "
         "if its report exists by the time you finish; fidelity is kill rule 5).\n"
         "Classes: (1) counter-error — a fake counter that writes a receipt copied from a REAL committed "
         "receipt (seed/met/runs/caughtBy included) but exits 2 (simulating CannotEvaluate after a class "
         "divergence); (2) tool-absent — a fake counter that writes a receipt with every run equal=False, "
         "candExit='tool absent', note='tool absent', met=False, exit 1; (3) stale-planted — a fake "
         "counter that writes NOTHING and kills itself (SIGKILL via os.kill(os.getpid(), signal.SIGKILL)), "
         "with tools/ctl1.json and build-{1,2,3}.json planted BEFORE the run, copied byte-exact from real "
         "committed receipts (after-final/tools/buildport-m6.json and build-1.json).\n"
         "# Run\n"
         "Run the FROZEN v1 driver over each class: python3 -B .ufo/waves/round-44/c44_audit.py --root . "
         "--controls <class>/controls.tsv --counter <class>/fake_counter.py --classes v5 --expect witnessed "
         "--build-rev 020bc457 --build-runs 3 --workers 1 --out <class>/out-v1/summary.json (capture txt too). "
         "Expected per the round-44 review: all three certify ok=True (invalid accepted). Save under "
         ".ufo/waves/round-45/verification/hardening/before/<class>/{summary.json,summary.txt,stdout}.\n"
         "# Also\n"
         "Run the junk control: the same v1 driver over ONE honest control (a real control source copied "
         "into fixtures/honest/) with the REAL frozen counter v5 --classes v5 --expect not-met; the receipt "
         "must be written during the run (it will be) — save under verification/hardening/before/honest/."),
    item("ExecDriverV2", "executor", ["operability"],
         "Implement the C1 instrument: " + L + "/.ufo/waves/round-45/c45_audit.py — driver v2.\n"
         "# Contract (from the frozen SCORECARD declaration)\n"
         "Refuse witness AND not-met credit for any control whose receipt (i) records a counter exit "
         "other than 0 or 1, (ii) records note 'tool absent', or (iii) was not written inside the "
         "driver's own run window over the invoked counter bytes; honest-cohort certification unchanged.\n"
         "# Mechanism (one receipt-validity gate)\n"
         "Keep v1's CLI, summary fields, row fields and exit codes byte-shape-compatible. New behavior: "
         "v2 creates the outdir cohort itself and refuses a non-empty one; writes run-manifest.json "
         "{started_ns, counter_sha256, nonce} BEFORE spawning any counter; after each control run, the "
         "row is VALID iff receipt parses AND receipt['counterSha256'] == invoked counter sha AND receipt "
         "mtime in [started_ns-eps, finish_ns+eps] AND receipt exit recorded in {0,1} AND "
         "receipt.get('note') != 'tool absent' AND receipt has a recorded seed. Invalid rows join "
         "errors[] with a named class: counter_error / tool_absent / stale_receipt; expectation_ok fails "
         "if any row is invalid (a measurement failure is never a witness and never a not-met); "
         "--expect not-met counts only valid met==False rows; build rows get the same validity gate and "
         "build_met additionally requires len(build) == --build-runs when --build-runs > 0. Structure the "
         "gate as a pure function receipt_validity(receipt, exit_code, mtime_bounds, counter_sha) so the "
         "selftest exercises it in memory.\n"
         "# Selftest (must kill the witness-class mutants)\n"
         "Keep every v1 assertion; add: timing-only caughtBy=['T1'] row is not a witness; an invalid "
         "receipt fixture per named class (counter_error, tool_absent, stale_receipt via sha mismatch and "
         "via mtime-outside-window) is rejected by receipt_validity; an error row is excluded from "
         "not-met counting; build count pin enforced (1 receipt fails --build-runs 3). Ship "
         "--selftest exit 0.\n"
         "# Run\n"
         "python3 -B .ufo/waves/round-45/c45_audit.py --selftest (capture output). Do NOT run the full "
         "audit (ExecRegressionHonest owns that)."),
    item("ExecCounterV6", "executor", ["freshness"],
         "Implement the C2(b) instrument: " + L + "/.ufo/waves/round-45/c45_count.py — counter v6.\n"
         "# Change (only)\n"
         "Byte-copy .ufo/waves/round-44/c44_count_v5.py, then change EXACTLY: (1) PREDICATE becomes "
         "mode-conditional — PREDICATE_V5 must be the byte-identical current PREDICATE string; "
         "PREDICATE_V4 = 'met: the tool\\'s exit code and output equal the round-41 tool\\'s on every "
         "generated run (the eleven v4 runs), and its median CPU time on each of the five timing shapes "
         "is at most 2.0 times the round-40 tool\\'s'; the receipt records the mode's predicate. "
         "(2) The docstring header: correct the provenance-label nit (the line claiming a 'Round-43 "
         "version 4 header follows' must accurately describe the v3 header that actually follows, per "
         "CriticHarmGuard). Nothing else changes — not the run lists, not the class loader, not the "
         "scoring.\n"
         "# Proof\n"
         "diff -u .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-45/c45_count.py > "
         ".ufo/waves/round-45/v6diff/v5-v6.diff (hunks classified: predicate-text, docstring, or OTHER — "
         "any OTHER hunk is a FAIL you must fix before reporting); plus a grep proof that PREDICATE_V5 "
         "is byte-identical (python3 -c comparing the exact strings). Do NOT run the counter."),
    item("ExecV4ReceiptV6", "executor", ["freshness"],
         "Produce the C2(b) AFTER receipt: run counter v6 in v4 mode over the real tool file and commit "
         "the receipt bytes.\n"
         "# Run (from " + L + ")\n"
         "python3 -B .ufo/waves/round-45/c45_count.py --root . --classes v4 --tool-file scripts/sitemap_audit.py "
         "--out .ufo/waves/round-45/verification/v6v4/counter-v4.json (capture stdout/stderr/exit to "
         "counter-v4.txt). If c45_count.py does not exist yet when you start, poll is forbidden — record "
         "the dependency in your report and return; the L1 will re-run.\n"
         "# Verify (decisive output for your report)\n"
         "jq '{predicate, classesMode, classRuns, runs_keys:(.runs|keys)}' counter-v4.json — predicate "
         "must name ONLY the eleven v4 runs (no 'class runs' phrase), classesMode 'v4', classRuns [], "
         "and runs must contain no G-keys. Any G-key or class-runs phrase = FAIL. Also record the "
         "counter sha256 and seed."),
    item("ExecMutantMatrix", "executor", ["operability", "freshness"],
         "Reconstruct the four witness-class mutants m1-m4 of semantic_witness/expectation_ok from "
         + L + "/.ufo/waves/round-44/w2/MutClassGate.md (the 'four mutants' section) and build the C2(a) "
         "before/after matrix.\n"
         "# Write\n"
         "mutant copies (never edit frozen files): .ufo/waves/round-45/mutants/m{1..4}.py = byte-copy of "
         ".ufo/waves/round-44/c44_audit.py with exactly one mutation each, documented with its target "
         "line. If the report's mutant bodies are not fully specified, derive minimal mutants by class: "
         "m1 = classifier weakened so a no-class/legacy divergence witnesses; m2 = timing-only caughtBy "
         "counts as a witness; m3 = met==True counted as witness; m4 = an error/cannot-evaluate row "
         "counts as not-met (or as witness). State precisely which you implemented and quote the MutClassGate "
         "text you followed.\n"
         "# Run BEFORE\n"
         "python3 -B .ufo/waves/round-45/mutants/mN.py --selftest for each; expect (per the report) m1/m3 "
         "KILLED (exit 1) and m2/m4 SURVIVING (exit 0) under the shipped v1 selftest body. Capture to "
         ".ufo/waves/round-45/verification/selftest-coverage/before/mN.txt. This is the C2(a) before-state: "
         "2/4 killed.\n"
         "# Run AFTER (if v2 exists — else record dependency)\n"
         "Same four mutants applied to .ufo/waves/round-45/c45_audit.py (mutants/m{1..4}_v2.py), run "
         "under the v2 shipped --selftest; expect 4/4 killed. Capture to "
         "verification/selftest-coverage/after/mN.txt. Report the kill table both states."),
    item("ExecWitnessSplit", "executor", ["freshness"],
         "Re-derive the C2(c) witness split from the committed round-44 claim receipt.\n"
         "# Run (from " + L + ")\n"
         "jq -r '.rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and "
         "(.legacyCaught|length)==0))|length, mixed: map(select(.met==false and (.classCaught|length)>0 "
         "and (.legacyCaught|length)>0))|length, met: map(select(.met==true))|length, other: map(select("
         ".met==false and (.classCaught|length)==0))|length}' .ufo/waves/round-44/verification/claim/after-final/after-v5.json\n"
         "Expected per CriticC1Predicate: class_only=22, mixed=1, met=4, other=0 (27 total).\n"
         "# Write\n"
         ".ufo/waves/round-45/verification/witness-split/split.json (the jq output verbatim plus the jq "
         "command and the receipt sha256) and split.txt (human-readable). Also draft the exact SCORECARD "
         "sentence filing the split (one sentence, naming this re-derivation command) into "
         ".ufo/waves/round-45/drafts/witness-split-sentence.md."),
    item("ExecMatrixRunner", "executor", ["operability"],
         "Implement the C1 counting command: " + L + "/.ufo/waves/round-45/c45_matrix.py.\n"
         "# Contract\n"
         "--stage before: run the FROZEN v1 driver .ufo/waves/round-44/c44_audit.py over the three "
         "committed fixture classes (fixtures/{counter-error,tool-absent,stale-planted}) plus the honest "
         "control, and count invalid_accepted = how many of the three invalid classes certify ok=True. "
         "--stage after: run v2 .ufo/waves/round-45/c45_audit.py over the same fixtures (each into its own "
         "fresh cohort dir created by v2) and count invalid_accepted, rejections_named (distinct named "
         "error classes among the 9 rejected rows: 3 fixture classes x control+3 builds), then run the "
         "honest regression ONLY if invoked with --with-honest (ExecRegressionHonest owns the heavy run; "
         "the matrix reads its committed receipt for honest_witnessed/honest_build_met instead).\n"
         "# Output\n"
         "Print one line: stage=<stage> invalid_accepted=<n> rejections_named=<n> honest_witnessed=<n> "
         "honest_build_met=<n>; write the JSON receipt under "
         ".ufo/waves/round-45/verification/matrix/<stage>.json; exit 0 iff the stage's expectations hold "
         "(before: invalid_accepted=3; after: invalid_accepted=0 and rejections_named=3). If fixtures or "
         "v2 are absent, run what exists and record dependencies as JSON fields — never fabricate."),
    item("ExecRegressionHonest", "executor", ["operability"],
         "Run the C1 honest-cohort regression under driver v2 (the heavy run).\n"
         "# Run (from " + L + ", after ExecDriverV2's c45_audit.py exists — else record dependency and return)\n"
         "python3 -B .ufo/waves/round-45/c45_audit.py --root . --controls .ufo/waves/round-44/controls-27.tsv "
         "--counter .ufo/waves/round-44/c44_count_v5.py --classes v5 --expect witnessed --build-rev 020bc457 "
         "--build-runs 3 --workers 4 --out .ufo/waves/round-45/verification/honest-regression/after-v5-v2.json "
         "(capture the txt table too). Expected: witnessed 27/27, build_met 3/3, ok=True, exit 0 — matching "
         "the frozen v1 receipt .ufo/waves/round-44/verification/claim/after-final/after-v5.json (kill rule 4).\n"
         "# Report\n"
         "Paste the AUDIT line and exit code; diff the summary fields (witnessed/build_met/counter sha) "
         "against the v1 receipt; name any divergence — divergence = C1 kill rule 4 failure."),
    item("ExecLedgerGate", "executor", ["operability", "freshness"],
         "No-harm evidence for the round-44 C2 gate: run " + L + "/scripts/ledger_latest_check.py --root . "
         "and --selftest BEFORE any round-45 instrument is integrated (captures to "
         ".ufo/waves/round-45/verification/ledger-gate/before.txt) and re-state in your report what the "
         "checker's three figures are (read the code — do not just run it). Then state exactly which "
         "round-45 writes could harm it (SCORECARD/LOG edits touching the three quoted figures) so the "
         "L1 can re-run after integration (after-run is the L1's or a wave-2 seat's job)."),

    # ---- scribes (drafts only; L1 lands corpus/SCORECARD bytes) ----
    item("ScribeDeclarations", "scribe", ["operability", "freshness"],
         "Draft the SCORECARD measurement-append text for round 45. Read the frozen declarations at "
         + L + "/SCORECARD.md (section 'Round 45 — C1 and C2 declared'). Draft, with placeholders where a "
         "receipt value is not yet known: (1) the C1 measurement paragraph (before/after receipts named, "
         "invalid_accepted 3 -> 0, kill-rule evidence pointers), (2) the C2 measurement paragraph "
         "(selftest kills 2/4 -> 4/4, v4 predicate true -> false, the witness-split sentence), (3) the "
         "move-log row. Rules: every count names its counting command and measured commit; no number "
         "without its receipt; append-only framing. Write the draft to "
         + L + "/.ufo/waves/round-45/drafts/scorecard-measurement.md."),
    item("ScribeSourcesGate", "scribe", ["freshness"],
         "Open the source for the C1 knowledge entry and draft the Gate rows. Open "
         "https://docs.python.org/3/library/subprocess.html (read-only fetch; if the network refuses, "
         "use the local python3 docs: python3 -c 'import subprocess,inspect; ...' is NOT a quote source — "
         "find the installed docs or record the dependency). Locate the 'returncode' semantics passage "
         "(a negative value -N indicates the child was terminated by signal N; None while running). "
         "Record: URL, access date 2026-10-24, and a <=25-word verbatim quote WITH its location "
         "(section/paragraph). Draft: (1) the S133 SOURCES.md row (kind docs, tier A for the scope "
         "'child-process exit-status semantics used by receipt gates', scope cell naming that, anchor = "
         "the returncode paragraph, teaches one grounded benefit, status queued, opened 2026-10-24); "
         "(2) ONE REJECT decision — a candidate non-primary source on the same topic you actually "
         "opened (e.g. a Stack Overflow answer or blog on subprocess exit codes) with reason and flip; "
         "(3) Gate rows labeled per new row (round-44 closure observation). Write the draft to "
         + L + "/.ufo/waves/round-45/drafts/sources-gate.md."),
    item("ScribeKnowledge", "scribe", ["operability"],
         "Draft the C1 knowledge entry: corpus/knowledge/receipt-integrity.md content (the L1 lands it; "
         "you write the draft). Content: the three defect classes (counter-error receipts, tool-absent "
         "receipts, stale planted receipts) each with its round-44 evidence pointer; the v2 binding rule "
         "(run-window + counter-sha + exit + note validity gate); the do-nothing reachability note. "
         "Provenance trio per CORPUS.md: source: S133 (Python subprocess docs) + .ufo/waves/round-44/"
         "w2/ReviewCounterContract.md; verified-at: 2026-10-24 (round 45); recheck: the c45_matrix.py "
         "command over future receipts. Mark any opinion as opinion; every count carries its command. "
         "Write to " + L + "/.ufo/waves/round-45/drafts/receipt-integrity.md."),
    item("ScribeLessonMistakes", "scribe", ["operability", "freshness"],
         "Draft the round-45 lesson content (L1 lands corpus/lessons/round-45.md). Draft: (1) the ## "
         "Mistakes row for the receipt-trust mistake class — class 'instrument trusted receipts without "
         "binding them to the run' · evidence .ufo/waves/round-44/w2/ReviewCounterContract.md defects "
         "1a/1b/1c (three HIGH) · captured-by 'kill rule 2 (receipts must re-derive at recorded seeds) "
         "should have required run-binding, not just seed-binding' · fix 'driver v2 run-window + counter-"
         "sha validity gate (c45_audit.py), able-to-fail via c45_matrix.py' · able-to-fail evidence "
         "placeholder; (2) a Gate table skeleton with one labeled row per expected decision (S133 admit, "
         "the rejected non-primary source, and any wave-1 rejections seats report). Write to "
         + L + "/.ufo/waves/round-45/drafts/mistakes.md."),

    # ---- critics (first falsifiers) ----
    item("CriticC1Predicate", "critic", ["operability"],
         "Freeze-attack the C1 declaration sentence (quoted in your context). Try to break it: is "
         "'written inside the driver's own run window over the invoked counter bytes' precisely "
         "checkable (what clock, what tolerance, what proves 'over the invoked counter bytes')? Does "
         "the sentence smuggle universals ('any control whose receipt...') the counting command does not "
         "enumerate? Is the honest-cohort clause measurable against committed bytes? Produce the "
         "strongest counterexample you can (e.g. a receipt written during the window by DIFFERENT bytes "
         "with the invoked sha — can the gate still be fooled? name the residual hole honestly) and "
         "state whether the residual hole is claim-breaking or reportable-risk. Do not propose new "
         "claim text the L1 must adopt; classify: claim-breaking vs reportable."),
    item("CriticC2Scope", "critic", ["freshness"],
         "Attack C2's composition: three legs (selftest coverage, v4 receipt text, witness split) under "
         "one freshness claim. Is that ONE axis-move or three smuggled claims? Check the frozen counting "
         "command: does one command measure all three legs, and does the MET condition require all three "
         "simultaneously? Try to construct a state where the claim reads MET but a leg is false (e.g. "
         "split re-derived from the WRONG receipt). Verdict: composition sound / unsound, with the exact "
         "sentence boundary that would make it sound if unsound."),
    item("CriticFixtures", "critic", ["operability"],
         "Fixture-fidelity attack (kill rule 5). Compare the three invalid fixture classes' receipt "
         "shapes against REAL committed receipts: .ufo/waves/round-44/verification/claim/after-final/"
         "tools/*.json and build-1.json. For each class state: which real counter code path produces "
         "this shape (cite c44_count_v5.py line), and does the fixture deviate in any field the v1 audit "
         "reads (seed/met/runs/caughtBy/counterSha256/toolSha256/note/exit)? A fixture shape real bytes "
         "cannot produce is a strawman — name any. Also verify the stale-planted class copies its "
         "planted receipts BYTE-EXACT from the committed sources (sha256 compare)."),
    item("CriticV6Minimal", "critic", ["freshness"],
         "Harm-guard the v6 counter change (CriticHarmGuard style). If .ufo/waves/round-45/v6diff/"
         "v5-v6.diff exists: hunk-classify EVERY hunk — allowed classes: predicate-text (mode-conditional "
         "PREDICATE), docstring-header; ANY other hunk (run lists, loader, scoring, CLI, receipt fields) "
         "= FAIL. Verify PREDICATE_V5 is byte-identical to the frozen PREDICATE (python string compare "
         "against c44_count_v5.py's exact string). If the diff does not exist yet, produce the "
         "classification against the SPEC and record the dependency. Also verify the v3-header "
         "provenance description, once present, is accurate."),
    item("CriticV2Regression", "critic", ["operability"],
         "Regression surface of driver v2. Enumerate every v1 behavior a user could observe: CLI flags "
         "and defaults, summary JSON fields, row fields (name/exit/met/caughtBy/classCaught/legacyCaught/"
         "receipt/seed/error), witnessedByClass txt format, exit codes, tools/ receipt layout, build-N "
         "naming. If c45_audit.py exists, diff behaviors by reading both files and by running --selftest "
         "on both; any silent interface change = defect (name it). If absent, deliver the enumeration "
         "table with the check each behavior needs. Kill rule 4 (honest verdict equality) depends on "
         "your list being complete — try to find a field v2 drops that a receipt re-derivation needs."),

    # ---- reviewers ----
    item("ReviewV1Defects", "reviewer", ["operability"],
         "Re-derive the three HIGH defects on the frozen v1 driver TODAY (independence from the "
         "round-44 reviewer's claims). Rebuild probes A (exit-2 receipt with class caughtBy -> "
         "semantic_witness True), B (tool-absent note receipt -> witness True), C (--expect not-met with "
         "an exit-2 cannot-evaluate row -> expectation True) against .ufo/waves/round-44/c44_audit.py at "
         "the current commit, plus the end-to-end stale-plant run (fake counter SIGKILLs with receipts "
         "planted beforehand -> ok=True exit 0). Scratch copies only — never edit the frozen file. "
         "Each probe must print its decisive output. Any defect that does NOT fire today = report "
         "immediately as a claim-breaking finding."),
    item("ReviewKillRules", "reviewer", ["operability"],
         "Review the C1/C2 kill rules (quoted in your context) for gaps a shortcut could sail through. "
         "For each kill rule: name the cheapest control that violates it while the claim still reads "
         "MET, or state why none exists. Pay special attention to: kill rule 5 enforceability (who "
         "proves fixtures non-strawman, and when), the regression equality scope (same INPUTS — are the "
         "inputs pinned?), and the v6 diff-audit kill rule (can a semantic change hide in a "
         '"predicate-text" hunk? e.g. the ratio limit or run order smuggled into the string is impossible '
         "— but check the receipt-construction hunk)."),
    item("ReviewWave1Plan", "reviewer", ["calibration"],
         "Padding/duplication audit of this wave's 32 items: list any two items whose deliverables "
         "substantially overlap (name both), any item that cannot produce evidence relevant to C1/C2 or "
         "the frontier step, and any claim-sizing violation (universal clause, unmeasurable after-state, "
         "do-nothing-reachable target). Read the frozen declarations in " + L + "/SCORECARD.md. Verdict: "
         "wave sound / item X unsound, with reasons."),
    item("ReviewScopeBound", "reviewer", ["adjacency"],
         "Write-scope audit. Enumerate every lane write path this wave's items name (fixtures/, "
         "c45_audit.py, c45_count.py, v6diff/, verification/*, mutants/, drafts/, w1/ reports) and check "
         "each against: (a) inside the lane repo, (b) not a frozen path, (c) not MANIFEST.json / fleet "
         "scripts/ / templates/ / .ufo/state/ / sibling repos. Also verify the corpus is L1-write-only "
         "this wave (scribe drafts under drafts/ only). Report any out-of-scope write path with the "
         "item name."),

    # ---- mutation-testers ----
    item("MutDriverV2Spec", "mutation-tester", ["operability"],
         "Mutation-attack the v2 hardening spec (the C1 mechanism in your context). Derive >=6 mutants "
         "of c45_audit.py: (1) exit gate removed; (2) note gate removed; (3) freshness window removed; "
         "(4) counter-sha binding removed; (5) invalid rows counted as not-met under --expect not-met; "
         "(6) build-count pin removed. If c45_audit.py exists, build each mutant copy under "
         ".ufo/waves/round-45/mutants/v2/m{1..6}.py and test: the v2 --selftest must kill each (exit 1) "
         "and the honest --selftest must stay green (exit 0) — run and capture. If v2 does not exist, "
         "write the mutant PATCHES as diff text plus the kill method each, and record the dependency. "
         "Any mutant you predict the selftest CANNOT kill = a coverage finding to report loudly."),
    item("MutCounterV6Spec", "mutation-tester", ["freshness"],
         "Mutation-attack the v6 spec: (1) PREDICATE_V5 string changed (v5 receipts no longer "
         "comparable); (2) classRuns populated in v4 mode; (3) runs list mutated in v4 (a G-run "
         "inserted); (4) docstring header left claiming the wrong provenance. For each, name the "
         "detector that must kill it (grep/diff-audit/receipt-fields) and, where possible, run the "
         "detector against the real files. If v6 does not exist yet, deliver the four mutant specs + "
         "kill methods and record the dependency."),

    # ---- sentinel / simplifier ----
    item("SentinelFrozen", "sentinel", ["operability"],
         "Sha-guard the frozen set at " + L + ": sha256sum of .ufo/waves/round-44/{c44_audit.py,"
         "c44_count_v5.py,c44_placebo.py,controls-27.tsv,controls-canary.tsv}, every file under "
         ".ufo/waves/round-44/{classes,classes-placebo,controls-r43}/, and every file under "
         ".ufo/waves/round-4{3,4}/verification/ — write the manifest to "
         ".ufo/waves/round-45/verification/sha-guard/before.sha256 (count the files guarded; expect "
         "hundreds). At the END of your seat re-run the guard and diff — any drift in a frozen path is "
         "a kill-rule-1 failure: report it as the seat's top finding. Also guard scripts/ledger_latest_check.py "
         "and scripts/sitemap_audit.py."),
    item("SimplifierV2", "simplifier", ["operability"],
         "YAGNI review of the v2 mechanism spec: can the three defect classes close with FEWER checks "
         "than the spec's five-part validity gate (sha binding, mtime window, exit set, note, seed "
         "presence)? For each spec check, answer: which defect class regresses if it is deleted? Checks "
         "with no regressing class = deletion candidates (name them); classes closing with one combined "
         "check = simplification (show it). Read the v1 driver and the C1 declaration. Report only — "
         "the L1 owns the instrument bytes."),
]

spec = {"wave": "kake-r45-w1",
        "milestone": "round-45 wave 1 (build: fixtures, driver v2, counter v6, matrices, drafts)",
        "maxLanes": 64,
        "axes": ["operability", "freshness"],
        "reportDir": ".ufo/waves/round-45/w1",
        "context": CTX,
        "items": items}

out = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w1-spec.json"
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1)
from collections import Counter
print(out, len(items), Counter(i["role"] for i in items))
