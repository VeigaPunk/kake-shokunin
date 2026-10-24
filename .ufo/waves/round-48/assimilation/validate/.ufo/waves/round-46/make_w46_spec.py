#!/usr/bin/env python3
"""Build the round-46 wave spec (ONE v2 wave, exactly 64 seats, policy v2 band 64-128).

Round 46 claims (frozen at bd86ee80ab62fdc507775b93ab1cd4e7306544b8, before any claim
receipt): C1 = offline static-host redirect/rewrite expectation audit capability
(operability; scripts/redirect_audit.py + sealed matrix .ufo/waves/round-46/c46_matrix.py);
C2 = standing-records citation-hygiene gate (freshness; scripts/citation_lint.py + QUALITY.md
receipt-identity criterion). Attack share: 32/64 reviewer+critic+mutation-tester (labrat is
a frozen-topology probe the swarm validator rejects as a lane; it may ride as an
executor-spawned depth-2 probe only).
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
WAVE = ".ufo/waves/round-46/w1"
SCRATCH = "/fast/scratch/hyaku/kake-r46"

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
Kake round 46, ONE v2 wave of 64 seats (build + attack together). Lane: kake-shokunin (axes:
operability, freshness; offline audit instruments over committed bytes, local CLI tools only).
You are one independent leaf seat with one item; the L1 (kake-r46) is sole writer of lane
history and the only integrator — you do NOT commit, push, or edit files outside your named
write paths. Never call ask; never `agent://all` (message your seat id only if ever needed).

Lane repo: LANE_PH. Scratch: SCRATCH_PH/<YourSeatName>/ (create it; temp files there only).
Every `Report:` trailer path is relative to LANE_PH — write your report at LANE_PH/WAVE_PH/<YourSeatName>.md.

# Round claims (frozen at bd86ee80; the frozen sentences below are quoted from SCORECARD.md — do not re-declare, attack them)
- C1 (operability, capability acquisition): "The committed tool scripts/redirect_audit.py
  reads a version-1 manifest of static-host redirect/rewrite checks and reports, read-only
  and network-free, every check whose decided outcome differs from its expectation; the
  frozen counting command python3 -B .ufo/waves/round-46/c46_matrix.py --root . --revision
  <commit> --stage before|after decides before = at least one planted witness uncaught or
  one do-nothing/constant/junk control accepted, after = sealed matrix with every planted
  witness caught and every do-nothing, constant and junk control rejected."
  Ground: PROVINCE frontier — Render redirect/rewrite semantics are knowledge-only since
  round 30 (corpus/knowledge/render-static-sites.md, S050/S088); no gate exists. Matrix must
  stay under 120 s wall (routed defect 4).
- C2 (freshness): "The committed gate scripts/citation_lint.py resolves every lane commit
  citation over the frozen population {SCORECARD.md, LOG.md} and reports each violation with
  file, line and token; python3 -B scripts/citation_lint.py --root . --revision <commit>
  exits 1 with at least one named violation at base 7cdbaefd… and exits 0 at the round-46
  tip with every base violation repaired append-only or adjudicated in the committed ledger;
  and corpus/QUALITY.md carries the receipt-identity criterion, counting grep -c '^- .*
  receipt.*\\(path\\|sha256\\)' corpus/QUALITY.md 0 → 1."
  Routed from r45 closure defects: dead short-hash e5455253 (the commit is
  e54552553eaff4d7033dc2df299300fc056f4a0d; note e545525 x7 resolves, e5455253 x8 does not)
  and receipt-identity binding (any filed count against a receipt cites path + sha256).
  Known hard case the rule must classify correctly: sha256-digest prefixes like
  d7e79ba1…9d48 are NOT commit citations; foreign-repo commits (ufo-fsd-alpha HEAD 964f443e,
  Pages repo pins like 7c243a1d, deploy pins like a8f1e2b) must resolve OR be line-adjudicated
  in the ledger. Protected non-author files (corpus/lessons/round-*-verifier-spotcheck.md)
  are OUTSIDE the frozen population.

# Frozen — never edit (any pre-existing committed file; sha-guarded by SentinelWriteBounds)
Especially: .ufo/waves/round-4{3,4,5}/ everything, scripts/* (existing tools), corpus/**
(corpus is L1-write-only this wave — scribes deliver drafts under LANE_PH/.ufo/waves/round-46/drafts/).
New tool files scripts/redirect_audit.py and scripts/citation_lint.py are created ONLY by the
seats whose items name them (new files, disjoint paths).

# Report
Write LANE_PH/WAVE_PH/<YourSeatName>.md: what you did, exact commands, verbatim decisive
output, files written, blockers. Unrun check = reported unrun; never fabricate.

# Bounds
You may write only: the lane paths your item names, your scratch dir, your report.
Read-only: fleet repo /home/vgpnk/Projects/shokunin (you may read sibling lanes' cited files),
sibling lane repos, .ufo/state/, watchdog logs. Never git commit/jj/push; never edit
MANIFEST.json, templates/, fleet scripts/, route tables, mcp.json.
Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade
tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels,
update-safety gate, record tool/version/channel/reason in your report).
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
W = ".ufo/waves/round-46"

items = [
    # ================= BUILD 32 =================
    # ---- scouts (recon) ----
    item("ScoutRoutedLedger", "scout", ["operability", "freshness"],
         "Build the canonical routed-defect ledger for round 46. Read: corpus/lessons/"
         "round-45-verifier-spotcheck.md (routed defects 1-4 with line cites), corpus/lessons/"
         "round-45.md Mistakes 14-15, SCORECARD.md round-46 declarations, LOG.md round-46 entry. "
         "Deliver " + L + "/" + W + "/build/routed-ledger.md: each defect with its source line cite, "
         "the r46 item(s) that answer it, and the frozen claim sentence each answers."),
    item("ScoutRedirectSemantics", "scout", ["operability"],
         "Map the redirect/rewrite semantics ground for C1. Read corpus/knowledge/"
         "render-static-sites.md, corpus/SOURCES.md rows S050 and S088 (their located quotes), "
         "and scripts/robots_audit.py + scripts/sitemap_audit.py for the established v1-manifest "
         "tool shape. Deliver " + L + "/" + W + "/build/redirect-semantics-map.md: the expectation "
         "types a v1 redirect/rewrite manifest must express (status, target resolution, rewrite "
         "pass-through, existing-resource precedence, rule order, malformed rules), each with its "
         "S-row grounding, and the rule-syntax classes S050's retained text does NOT cover (these "
         "become the new-source candidates)."),
    item("ScoutSourceCandidates", "scout", ["freshness"],
         "Screen candidate NEW sources for C1's opened-this-round rows. Requirements: primary/"
         "docs tier A/B; must cover Render static-site _redirects rule SYNTAX (splats, placeholders, "
         "forced rules, rewrite/proxy flag) and/or HTML meta-refresh publisher-side redirects; "
         "must not duplicate existing row URLs in corpus/SOURCES.md (check W04 duplicate-url "
         "warnings: rfc9110.txt/html, whatwg syntax, rfc3986, rfc9309, sitemaps protocol, w3.org/TR/xml, "
         "urllib.parse docs, rfc9844). Fetch each candidate read-only (GET only, no credentials) and "
         "retain raw text under " + L + "/" + W + "/sources/ with sha256. Deliver " + L + "/" + W +
         "/build/source-candidates.md: per candidate — URL, final URL, HTTP status, byte count, "
         "sha256, tier, the ≤25-word located quote, and admit/screen-out with reason."),
    item("ScoutBasePopulation", "scout", ["freshness"],
         "Measure the C2 frozen population at base. Population = SCORECARD.md and LOG.md at "
         "revision 7cdbaefd3ecbbc8814eca1f013fcee101a6157b0 (git show <rev>:<path> to read base "
         "bytes; do not trust the working tree). Inventory every hex token 7-40 chars that is a "
         "commit citation (citation context: commit/landed/HEAD/tip/pin/beat/base/revision/deploy/"
         "sha words on the same line), classify each: resolves-as-lane-commit (git rev-parse "
         "--verify <tok>^{commit}), foreign-repo commit (name the repo on the line), sha256-digest "
         "prefix (the … ellipsis form or a sha256 label — NOT a commit citation), or unresolved. "
         "Deliver " + L + "/" + W + "/build/base-population.json: per-file, per-token records "
         "{file, line, token, class, evidence-line} plus summary counts. This is the before-state "
         "for C2; be exact, the ledger must reconcile."),
    item("ScoutFixtureDesign", "scout", ["operability"],
         "Design the C1 witness matrix. 14-18 planted witness classes over a v1 manifest family, "
         "each class a distinct rule-evaluation behavior, e.g.: exact match redirect; wildcard "
         "splat capture; placeholder forwarding :splat/:path segments; forced rule (existing "
         "resource overridden); rewrite/proxy pass-through flag; rule order (first match wins); "
         "existing-resource precedence (no rule applied where resource exists); 301 vs 302 vs 307 "
         "vs 308 status expectation; relative target resolution; malformed rules file (bad status, "
         "missing target, 4-segment splat); URL-encoded path match; circular redirect chain; "
         "trailing-slash handling. For each class: 2-3 manifest rows, the expected outcome, and "
         "which semantic source grounds it (S050/S088/new rows). Keep total matrix runs < 120 s. "
         "Deliver " + L + "/" + W + "/build/fixture-design.md + fixture-design.json (machine form)."),
    item("ConnectorSiblingOverlap", "connector", ["adjacency"],
         "Sibling-overlap scan: does any other lane own redirect/rewrite-rule auditing or "
         "citation-resolution linting? Read sibling SKILL.md/PROVINCE.md headers only (kasegi, "
         "kengaku, kumitate, kotoba, kagi, kama, tabi, chousa, mori, tameshi under "
         "/home/vgpnk/Projects/shokunin/). Deliver " + L + "/" + W + "/build/connector-overlap.md: "
         "per sibling, contested or clean with one-line evidence."),
    item("RevengerRound45Leftovers", "revenger", ["operability"],
         "Sweep for round-45 leftovers: untracked or uncommitted files in the lane working tree "
         "(git status --porcelain), stray __pycache__ under .ufo/waves/round-45/, files newer "
         "than the r45 tip outside .ufo/waves/round-46/, and seat reports missing from "
         ".ufo/waves/round-45/w1|w2 against their registries. Deliver " + L + "/" + W +
         "/build/r45-leftovers.md with findings; delete nothing."),
    item("SentinelWriteBounds", "sentinel", ["operability"],
         "Define the r46 write-bounds guard. Emit " + L + "/" + W + "/build/frozen-manifest.json: "
         "sha256 of every pre-existing committed file under .ufo/waves/round-43/, round-44/, "
         "round-45/ and every existing scripts/ and corpus/ file (find + sha256sum), plus the "
         "population freeze for C2 ({SCORECARD.md, LOG.md} at bd86ee80). Include a check script "
         ".ufo/waves/round-46/build/frozen-check.sh that re-hashes and reports any drift (read-only, "
         "exit 0/1). Verify it runs clean now; later seats re-run it as no-harm evidence."),
    item("SimplifierContractShape", "simplifier", ["operability"],
         "Propose the minimal v1 manifest + CLI contract for scripts/redirect_audit.py, shaped "
         "exactly like the prior tools (read scripts/robots_audit.py header + SCHEMA + argparse "
         "block; scripts/sitemap_audit.py for the exits 0/1/2/64 contract). Decisions to make and "
         "justify in " + L + "/" + W + "/build/contract-minimal.md: manifest JSON schema name and "
         "fields, how a check row expresses expectation, what 'decided outcome' means per check "
         "type, output finding shape, exit codes, --selftest hook. Keep it minimal — no live fetch, "
         "no rendering, no DNS."),
    # ---- executors (build) ----
    item("ExecRedirectTool", "executor", ["operability"],
         "Write the C1 tool: NEW FILE " + L + "/scripts/redirect_audit.py only. Implement the "
         "contract from SimplifierContractShape's artifact if present (else scripts/robots_audit.py "
         "shape): strict JSON manifest read, version-1 schema, per-check decided outcome vs "
         "expectation, findings with stable ids, exits 0/1/2/64, --selftest with planted able-to-fail "
         "fixtures, --root/--revision/--json/--manifest flags. Semantics per corpus/knowledge/"
         "render-static-sites.md + S050/S088: rule parsing (splats, placeholders, force flag, "
         "rewrite flag), first-match order, existing-resource precedence, status/target checks, "
         "relative-target resolution, malformed-rules faults. NO network, NO file writes outside "
         "the audit's own output flag. Selftest must FAIL if any planted witness is uncaught "
         "(prove by temporarily breaking one assertion and showing exit change, then restore). "
         "Report exact commands + outputs."),
    item("ExecCitationLint", "executor", ["freshness"],
         "Write the C2 gate: NEW FILE " + L + "/scripts/citation_lint.py only. Frozen population "
         "{SCORECARD.md, LOG.md}; --root/--revision flags read base bytes via git show <rev>:<path>. "
         "Rule (commit citation = hex token 7-40 chars with a citation-context word on the same "
         "line: commit|landed|HEAD|tip|pin|beat|base|revision|deploy; exclude sha256-digest forms: "
         "token followed/preceded by … OR line carries a 'sha256' label; exclude protected "
         "round-*-verifier-spotcheck.md files — they are outside the population anyway). For each "
         "citation: resolves-as-lane-commit (git rev-parse --verify) OR line-adjudicated (the line "
         "names a foreign repo) — else violation {file, line, token, line-text}. Output JSON ledger "
         "+ human summary; exits 0 (no violations) / 1 (violations) / 2 (input fault) / 64 (usage). "
         "--selftest with planted fixtures: a dead short hash (e5455253-class), a resolving hash, "
         "a sha256 prefix that must NOT flag, a foreign-repo commit that must NOT flag — each "
         "proven able-to-fail. Report exact commands + outputs."),
    item("ExecRedirectSelftest", "executor", ["operability"],
         "Write " + L + "/" + W + "/build/redirect-selftest.md AND extend-prove ExecRedirectTool's "
         "selftest: run scripts/redirect_audit.py --selftest, capture verbatim output + exit; then "
         "apply each of 6 mutants to a COPY under your scratch (drop status check; drop first-match "
         "order; drop existing-resource precedence; accept malformed rules; always-clean return; "
         "skip URL-decoding) and show the selftest kills each (exit/stdout change). Deliver the "
         "mutant-kill table; if a mutant survives, report it as a finding with the surviving "
         "behavior — do not patch the tool yourself."),
    item("ExecCitationSelftest", "executor", ["freshness"],
         "Mutation-test the C2 gate: run scripts/citation_lint.py --selftest (built by "
         "ExecCitationLint) against 5 mutants on a scratch copy (drop git-resolution check; drop "
         "citation-context filter; drop sha256 exclusion; always exit 0; flag every token). Show "
         "killed/survived per mutant with verbatim output. Deliver " + L + "/" + W +
         "/build/citation-mutants.md; survivors are findings, do not patch."),
    item("ExecMatrixCounter", "executor", ["operability"],
         "Write the C1 frozen counter: " + L + "/" + W + "/c46_matrix.py. It runs "
         "scripts/redirect_audit.py over the committed fixture manifests (population from "
         "ExecFixtureFiles; design from ScoutFixtureDesign) at --stage before (tool = a baseline "
         "copy with one witness class deliberately uncaught, kept under " + L + "/" + W +
         "/controls/before-tool.py) and --stage after (tool = scripts/redirect_audit.py), plus "
         "three controls scored per stage: do-nothing (always-clean counter), constant (reports "
         "every row violated), junk (reports a fixed nonsense finding). Receipt: {stage, "
         "witnesses_caught, witnesses_total, controls: {name: accepted|rejected}, wall_s, "
         "tool_sha256, matrix_sha256, revision, claim: '<the frozen C1 sentence>'}. Before receipt "
         "MUST show >=1 uncaught witness OR >=1 accepted control; after MUST show all witnesses "
         "caught and all controls rejected, wall_s < 120. Report both receipts verbatim."),
    item("ExecFixtureFiles", "executor", ["operability"],
         "Write the committed C1 fixtures: " + L + "/" + W + "/fixtures/ — rules files "
         "(_redirects-form for the Render static-site profile), existing-resource path lists, and "
         "manifest-v1 JSON implementing ScoutFixtureDesign's matrix (or your own 14-18 classes if "
         "that artifact is absent, naming your source ground per class). Include a fixtures README. "
         "Every planted witness must be decidable from the files alone (no network). Report the "
         "class inventory + the manifest sha256."),
    item("ExecMatrixPlacebo", "executor", ["operability"],
         "Build and score the C1 do-nothing control BEFORE data: write " + L + "/" + W +
         "/controls/placebo.py — a counter that reads the manifest and reports clean for every row "
         "without evaluating rules. Run ExecMatrixCounter's scoring shape against it manually (or "
         "write " + L + "/" + W + "/controls/score-placebo.py doing the same receipt shape): the "
         "placebo MUST be rejected (it reports clean while planted witnesses exist — show the "
         "receipt proving rejection). Deliver the placebo receipt; this is the claim-sizing "
         "control receipt committed before data."),
    item("ExecCitationDoNothing", "executor", ["freshness"],
         "Build and score the C2 do-nothing control: write " + L + "/" + W + "/controls/always0.py "
         "— a lint stub that exits 0 with an empty ledger regardless of input — and score it "
         "against the frozen C2 sentence at base: show it would certify the base population that "
         "contains unresolved citations, i.e. the do-nothing control cannot reach the after-state. "
         "Deliver " + L + "/" + W + "/controls/always0-receipt.json + a written verdict. This is "
         "the C2 claim-sizing control receipt before data."),
    item("ExecRunReceipts", "executor", ["operability"],
         "Write the r46 run-receipt stamper: " + L + "/" + W + "/build/stamp_receipt.py — wraps any "
         "counting command, captures {argv, exit, stdout_tail, started_at, wall_s} and writes a "
         "receipt naming the measured revision, the tool path and the tool sha256 (path + sha256 "
         "per the receipt-identity rule). Use it to produce " + L + "/" + W + "/verification/"
         "census-before.json receipt and the freshness-sweep baseline receipt "
         "(node scripts/freshness-sweep.mjs --section=paths) at base — paste both verbatim; honest "
         "red drift state is expected and must be recorded, not 'fixed'."),
    item("ExecLedgerBaseline", "executor", ["operability"],
         "Produce the no-harm baselines: run scripts/ledger_latest_check.py and "
         "node scripts/freshness-sweep.mjs --selftest at the current tip; capture verbatim exits "
         "and outputs into " + L + "/" + W + "/verification/no-harm-baseline.md. Also re-run "
         "SentinelWriteBounds' frozen-check.sh and append the result. Any failure is a finding."),
    item("ExecBudgetSizing", "executor", ["operability"],
         "Size the C1 matrix wall clock (routed defect 4: r45 honest-cohort re-cert exceeded 4 "
         "min). Run ExecMatrixCounter's after-stage shape once with timing; if wall_s >= 120, "
         "deliver a shrink plan (fixture count, parallel rows) that keeps every witness class "
         "represented and re-measure. Deliver " + L + "/" + W + "/build/budget-sizing.md with the "
         "measured wall and the final recipe."),
    item("ExecContractDoc", "executor", ["operability"],
         "Write " + L + "/" + W + "/c1-contract.md: the C1 audit contract v1 — manifest schema, "
         "check/expectation semantics per class, decided-outcome definitions, finding shape, exit "
         "codes, explicit non-claims (no live fetch, no DNS, no rendered-DOM, no publication "
         "approval; Render static-site _redirects profile only), and the frozen C1 sentence as "
         "the contract's claim label."),
    item("ExecQualityCriterion", "executor", ["freshness"],
         "Draft the QUALITY.md receipt-identity criterion (routed defect 3) as " + L + "/" + W +
         "/drafts/quality-criterion.md — a single bullet in the established QUALITY.md voice: "
         "any filed count/verdict against a receipt cites the receipt path + sha256; a receipt "
         "citation without sha256 is a violation of this criterion; the r45 closure language "
         "(per Mistake 15's fix) is the anchor. Also draft the application check: a grep/shape "
         "command counting criterion occurrences (before 0 → after 1) with its frozen output "
         "shape."),
    item("ExecReproReadme", "executor", ["operability"],
         "Write " + L + "/" + W + "/README.md: how to re-run every r46 counting command from a "
         "clean clone at the tip (exact commands, expected exits, expected receipt paths, wall "
         "budgets). Include the frozen C1/C2 sentences verbatim and the claim-sizing control "
         "receipts' locations."),
    item("ExecSanityReplay", "executor", ["operability"],
         "Replay-proof the C1 after-state: run the after-stage matrix twice (fresh temp outputs) "
         "and diff the receipts modulo {started_at, wall_s}; they must agree on every counted "
         "field. Deliver " + L + "/" + W + "/build/replay-proof.md with both receipts and the "
         "normalized diff. If they disagree, that is a finding."),
    item("ExecRepairPlanner", "executor", ["freshness"],
         "Build the C2 repair plan: run scripts/citation_lint.py --root . --revision "
         "7cdbaefd3ecbbc8814eca1f013fcee101a6157b0 over the frozen population and, for each "
         "violation, produce the append-only repair or adjudication the L1 must land (exact "
         "new line text per file, quoting the existing line; adjudications carry the "
         "foreign-repo/digest evidence). Write the plan as " + L + "/" + W + "/build/repair-plan.md "
         "plus repair-plan.json (machine form: file, line, token, action, replacement-text). "
         "Every proposed edit must be append-only or errata-style; flag any violation that "
         "cannot be repaired without rewriting history as routed."),
    item("ExecLedgerReconcile", "executor", ["freshness"],
         "Reconcile the C2 ledger with ScoutBasePopulation's inventory: every inventory token "
         "the lint did not classify as a violation must have a stated reason in the lint's "
         "output or your reconciliation notes (foreign-repo, sha256-digest, resolves). Deliver "
         + L + "/" + W + "/build/ledger-reconcile.md with the full reconciliation table and any "
         "inventory/lint disagreement called out as a finding."),
    # ---- scribes (drafts only; corpus is L1-write-only) ----
    item("ScribeKnowledgeDraft", "scribe", ["depth"],
         "Draft the C1 knowledge entry: " + L + "/" + W + "/drafts/redirect-rules-audit.md — "
         "shaped like corpus/knowledge/robots-txt-rules.md: what the audit decides, the v1 "
         "manifest shape, the expectation classes with their S-grounding (S050/S088 + the new "
         "rows ScoutSourceCandidates admits), limits (Render static-site profile only, offline), "
         "and source:/verified-at:/recheck: metadata front-matter in the exact lowercase trio "
         "form used by corpus/knowledge/receipt-integrity.md."),
    item("ScribeSourcesRows", "scribe", ["freshness"],
         "Draft the new SOURCES.md rows for the sources ScoutSourceCandidates admitted: " + L +
         "/" + W + "/drafts/sources-rows.md — one row per source in the exact table shape of "
         "corpus/SOURCES.md (id S135…, name, URL, kind, tier, scope, sections-opened, opened "
         "evidence line with fetch date/HTTP/sha256, teaches, status, recheck, used-by). "
         "Include any rejection rows with reason + flip, in the established rejection wording."),
    item("ScribeLessonMistakes", "scribe", ["calibration"],
         "Mine the round-46 lesson mistakes from wave evidence as it exists so far: " + L + "/" +
         W + "/drafts/lesson-mistakes.md — candidates (class, evidence pointer, captured-by, fix) "
         "drawn from the honest-stop re-declaration discipline (r45 closure), the citation-hygiene "
         "rule design, and any wave findings; each fix must be shown able to fail by a named "
         "check. If a candidate lacks evidence, mark it candidate-only."),
    item("ScribeCapabilityRow", "scribe", ["operability"],
         "Draft the SCORECARD capabilities-table row for C1: " + L + "/" + W + "/drafts/"
         "capability-row.md — name, one-line what-it-can-do, evidence pointer (tool + matrix "
         "receipt + selftest), first-working round 46, in the exact voice of the existing rows."),
    item("ScribeReportEvidence", "scribe", ["operability"],
         "Assemble the before-measurement evidence pack for the L1 report: " + L + "/" + W +
         "/drafts/report-evidence.md — census before output (from ExecRunReceipts' receipt or "
         "run it yourself: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate "
         "--root /home/vgpnk/Projects/shokunin kake), SOURCES row count before (grep -c '^| S' "
         "corpus/SOURCES.md), base-population summary from ScoutBasePopulation, and the frozen "
         "claim sentences. Everything verbatim; no invented numbers."),
    item("ScribeGateDraft", "scribe", ["freshness"],
         "Draft the round-46 lesson Gate: " + L + "/" + W + "/drafts/lesson-gate.md — per "
         "CORPUS.md SOURCES contract v1: for every new row, URL + access date + ≤25-word located "
         "quote; admits/rejects with reasons; spot-check status placeholders for the L1 to fill."),
    # ================= ATTACK 32 =================
    item("ReviewFrozenSentences", "reviewer", ["calibration"],
         "Attack the frozen claim sentences themselves (C1 and C2, quoted in the context above). "
         "For each: find any clause a do-nothing control could reach, any universal without an "
         "enumerated set, any term that is not decidable over committed bytes (the r45 C1 'over "
         "the invoked counter bytes' failure mode). Verdict per sentence: sound / overreach with "
         "the exact clause. Deliver " + L + "/" + W + "/attack/ReviewFrozenSentences.md."),
    item("ReviewCounterSeparation", "reviewer", ["calibration"],
         "Prove or refute causal separability: run the C1 matrix receipt check without the "
         "citation lint existing, and the C2 lint without the redirect tool existing; each must "
         "be independently decidable. Report exact commands. " + L + "/" + W +
         "/attack/ReviewCounterSeparation.md."),
    item("ReviewToolSemantics", "reviewer", ["operability"],
         "Fidelity-attack ExecRedirectTool: read scripts/redirect_audit.py and compare every "
         "decided outcome against corpus/knowledge/render-static-sites.md + S050/S088 located "
         "quotes (retained text under .ufo/waves/round-30/sources/ if present, else the row "
         "quotes). Any behavior not grounded in a cited row is a finding. " + L + "/" + W +
         "/attack/ReviewToolSemantics.md."),
    item("ReviewSelftestCoverage", "reviewer", ["operability"],
         "Attack both selftests' able-to-fail claim: for each planted fixture in "
         "redirect_audit.py --selftest and citation_lint.py --selftest, demonstrate (on a "
         "scratch copy) that breaking the corresponding assertion flips the exit; list any "
         "fixture that cannot fail (decorative assertion). " + L + "/" + W +
         "/attack/ReviewSelftestCoverage.md."),
    item("ReviewReceiptIdentity", "reviewer", ["freshness"],
         "Attack the ExecQualityCriterion draft: does the criterion sentence unambiguously "
         "require path + sha256 for ANY filed count against a receipt (including matrix "
         "receipts, census receipts, report figures)? Check every receipt produced so far in "
         ".ufo/waves/round-46/ for compliance; list violators with paths. " + L + "/" + W +
         "/attack/ReviewReceiptIdentity.md."),
    item("ReviewPopulationFreeze", "reviewer", ["freshness"],
         "Attack the C2 population: is {SCORECARD.md, LOG.md} complete for 'standing records' "
         "as the sentence claims, or does the sentence overreach/underreach? Independently "
         "re-derive ScoutBasePopulation's inventory (your own scan script, scratch only); any "
         "token disagreement is a finding. " + L + "/" + W + "/attack/ReviewPopulationFreeze.md."),
    item("ReviewClaimLabels", "reviewer", ["calibration"],
         "Verify the frozen-sentence discipline: the C1 receipt's claim field and the C2 "
         "ledger/README must carry the SAME sentence as SCORECARD round-46 (diff them). Any "
         "paraphrase is a finding. " + L + "/" + W + "/attack/ReviewClaimLabels.md."),
    item("ReviewPlacebo", "reviewer", ["operability"],
         "Independently re-score the C1 do-nothing placebo and constant/junk controls from "
         "committed bytes; verify the after-receipt truly rejects each (a rejected control "
         "that the receipt accidentally accepts = the r44 defect class). " + L + "/" + W +
         "/attack/ReviewPlacebo.md."),
    item("ReviewAlways0Control", "reviewer", ["freshness"],
         "Independently re-score the C2 always-0 control: at base bytes it must be shown unable "
         "to reach the after-state (it certifies violations away). Also attack the lint for "
         "false negatives: plant 3 NEW dead-cite shapes it might miss (e.g. uppercase hex, 40-char "
         "dead full hash, citation split across a line break) and report which the rule catches. "
         + L + "/" + W + "/attack/ReviewAlways0Control.md."),
    item("ReviewBudget", "reviewer", ["operability"],
         "Re-run the C1 after-stage matrix yourself with timing; verify wall_s < 120 and that "
         "the receipt's counts match ExecMatrixCounter's receipt. Report divergence. " + L + "/" +
         W + "/attack/ReviewBudget.md."),
    item("ReviewNoHarm", "reviewer", ["operability"],
         "No-harm sweep: re-run frozen-check.sh, scripts/ledger_latest_check.py, node "
         "scripts/freshness-sweep.mjs --selftest, and git status --porcelain in the lane; every "
         "pre-existing byte must be untouched (module gitignored __pycache__ drift, report it). "
         + L + "/" + W + "/attack/ReviewNoHarm.md."),
    item("ReviewSourcesRows", "reviewer", ["freshness"],
         "Attack the new SOURCES row drafts: each located quote ≤25 words and verbatim in the "
         "retained text (sha256-check); tier and scope honest; no duplicate URL against "
         "corpus/SOURCES.md; rejection rows carry reason + flip. " + L + "/" + W +
         "/attack/ReviewSourcesRows.md."),
    item("ReviewSourcedClaim", "reviewer", ["freshness"],
         "Verify the sourced-claim requirement: C1's knowledge entry draft must cite at least "
         "one row OPENED THIS ROUND (new S-id), and the audit semantics it teaches must rest on "
         "that row (not only on S050/S088). If the draft only re-uses old rows, that is a "
         "finding. " + L + "/" + W + "/attack/ReviewSourcedClaim.md."),
    item("ReviewLessonQuality", "reviewer", ["calibration"],
         "Attack the lesson drafts: each mined mistake needs class, evidence pointer, "
         "captured-by (the criterion/rule that should have caught it), and a fix shown able to "
         "fail. Candidate-only rows are acceptable only with that label. " + L + "/" + W +
         "/attack/ReviewLessonQuality.md."),
    item("CriticC1Predicate", "critic", ["calibration"],
         "Adversarially falsify the C1 after-state: find any way the after-receipt's "
         "'witnesses caught / controls rejected' can hold while the tool is wrong (e.g. "
         "witnesses decidable by construction, controls mis-scored, receipt fields unverifiable "
         "from committed bytes). Model-demonstrate the strongest shortcut you find. " + L + "/" +
         W + "/attack/CriticC1Predicate.md."),
    item("CriticC2Predicate", "critic", ["calibration"],
         "Adversarially falsify the C2 after-state: can the lint exit 0 at the tip while a "
         "dead citation remains (rule gap), or a live citation is flagged (rule overreach that "
         "would make exit 0 unreachable without history rewriting)? Demonstrate the strongest "
         "case. " + L + "/" + W + "/attack/CriticC2Predicate.md."),
    item("CriticHarmGuard", "critic", ["operability"],
         "Hunt for harmed axes: any r46 artifact that weakens an existing gate, loosens a "
         "frozen receipt, rewrites history, or pushes unscoped bytes into scripts/ or corpus/. "
         "Deliver the harm list (empty = say so with the sweep commands). " + L + "/" + W +
         "/attack/CriticHarmGuard.md."),
    item("CriticGateDesign", "critic", ["operability"],
         "Attack the redirect audit's usefulness: is a manifest-driven expectation audit on a "
         "publisher-side rules file a real capability, or does it reduce to 'JSON says what "
         "JSON says'? Name what observable publishing failure class it catches that the "
         "existing tools (base_path, canonical, link-preview) do not. " + L + "/" + W +
         "/attack/CriticGateDesign.md."),
    item("CriticCitationRule", "critic", ["freshness"],
         "Adversarially classify the citation rule's error modes: enumerate 10 citation shapes "
         "in SCORECARD/LOG-style lines and decide each by the rule (in your head + test where "
         "cheap); count false-positive and false-negative classes; any class that flips the "
         "exit code outcome is a finding. " + L + "/" + W + "/attack/CriticCitationRule.md."),
    item("CriticCoverage", "critic", ["calibration"],
         "Coverage attack: name any genuine round-46 obligation (routed defects 1-4, frontier "
         "step §2b: census, mistake mining, sourced claim, trend verdicts, SHONEN, report "
         "sections) that NO seat item covers. Deliver the gap list. " + L + "/" + W +
         "/attack/CriticCoverage.md."),
    item("MutRedirectStatus", "mutation-tester", ["operability"],
         "Mutation-test scripts/redirect_audit.py: mutant A drops the 301/302/307/308 status "
         "comparison (always pass status). Build a manifest row where status differs; the "
         "matrix/selftest must reject the mutant. Score killed/survived with verbatim output. "
         + L + "/" + W + "/attack/MutRedirectStatus.md."),
    item("MutRedirectOrder", "mutation-tester", ["operability"],
         "Mutant B reverses rule-match order (last match wins). Plant two overlapping rules "
         "with different targets; show the mutant's decided outcome differs and the selftest or "
         "matrix kills it. Score + evidence. " + L + "/" + W + "/attack/MutRedirectOrder.md."),
    item("MutRedirectPrecedence", "mutation-tester", ["operability"],
         "Mutant C removes existing-resource precedence (rules apply even where a resource "
         "exists). Plant a resource + a rule at the same path; kill evidence required. " + L +
         "/" + W + "/attack/MutRedirectPrecedence.md."),
    item("MutRedirectMalformed", "mutation-tester", ["operability"],
         "Mutant D accepts malformed rules (bad status line kept instead of faulted). Plant a "
         "malformed rules file; kill evidence required. " + L + "/" + W +
         "/attack/MutRedirectMalformed.md."),
    item("MutRedirectClean", "mutation-tester", ["operability"],
         "Mutant E returns always-clean (zero findings regardless of manifest). Score against "
         "the matrix after-stage: must be rejected. " + L + "/" + W + "/attack/MutRedirectClean.md."),
    item("MutCitationResolution", "mutation-tester", ["freshness"],
         "Mutant F: scripts/citation_lint.py variant that skips git resolution (treats every "
         "token as resolving). At base bytes it must exit 0 — show the do-nothing-style "
         "false-green, then show the committed selftest kills it. " + L + "/" + W +
         "/attack/MutCitationResolution.md."),
    item("MutCitationContext", "mutation-tester", ["freshness"],
         "Mutant G drops the citation-context filter (every 7-40 hex token is a citation). "
         "Show it explodes the violation count on real population bytes (overreach) and that "
         "the selftest kills it. " + L + "/" + W + "/attack/MutCitationContext.md."),
    item("MutCitationShaExclusion", "mutation-tester", ["freshness"],
         "Mutant H removes the sha256-digest exclusion: sha256 prefixes in SCORECARD must "
         "start flagging (overreach proof) and the selftest must kill it. " + L + "/" + W +
         "/attack/MutCitationShaExclusion.md."),
    item("ScoutReopenNewRows", "scout", ["freshness"],
         "Independently re-open each NEW source row (live GET, read-only) retained under "
         ".ufo/waves/round-46/sources/: verify the draft row's quote occurs verbatim (≤25 "
         "words) in the CURRENT page, record HTTP status + fetch time; if the page changed, "
         "report the drift (do not silently re-pin). " + L + "/" + W + "/attack/ScoutReopenNewRows.md."),
    item("ScoutMisrootPattern", "scout", ["operability"],
         "Misroot sweep: check the FLEET repo working tree (/home/vgpnk/Projects/shokunin) for "
         "any kake-r46-authored files at the fleet root (git status --porcelain there, look for "
         "seat-note style files naming kake/r46). Report findings; move nothing yourself. " + L +
         "/" + W + "/attack/ScoutMisrootPattern.md."),
    item("SentinelFinalAudit", "sentinel", ["operability"],
         "Final bounds audit: re-run frozen-check.sh over all guarded paths, verify every seat "
         "report exists against the wave's 64 seats, verify every receipt names path + sha256, "
         "and confirm the only new lane files are the ones items name (git status --porcelain). "
         + L + "/" + W + "/attack/SentinelFinalAudit.md."),
    item("RevengerDeadWeight", "revenger", ["operability"],
         "Dead-weight scan over the new .ufo/waves/round-46 artifacts: scratch copies that "
         "escaped scratch, duplicate fixtures, unused drafts, oversized retained sources (>2 MB "
         "without justification). List candidates for deletion (L1 decides; delete nothing). "
         + L + "/" + W + "/attack/RevengerDeadWeight.md."),
]

spec = {
    "wave": "kake-r46-w1",
    "milestone": "round-46 single v2 wave (build+attack, 64 seats): C1 redirect/rewrite audit capability, C2 citation-hygiene gate",
    "maxLanes": 64,
    "axes": ["operability", "freshness"],
    "reportDir": WAVE,
    "context": CTX,
    "items": items,
}

out = L + "/" + W + "/w46-spec.json"
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1)
roles = {}
for it in items:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print("seats:", len(items), "roles:", roles)
