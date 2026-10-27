#!/usr/bin/env python3
"""Generate the round-61 wave w1 (v1 policy, build + recon + first falsifiers). Output: w1-spec.json beside this file."""
import json
import os
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W = f"{LANE}/.ufo/waves/round-61"
R = f"{W}/w1"
SRC = f"{W}/sources"
CAP = f"{W}/capture"
REC = f"{W}/recheck"
KNOW = f"{LANE}/corpus/knowledge"
STAGED = "/home/vgpnk/Projects/shokuknow/merge/kake"
FLEET = "/home/vgpnk/Projects/shokunin"
BASE = "9f07731a873585e655a6518233ea39f5d9fb8204"
SCR = "/fast/scratch/hyaku/kake-r61"
W60 = f"{LANE}/.ufo/waves/round-60"
W23 = f"{LANE}/.ufo/waves/round-23"

GODSPEED = "/skill:godspeed\n" + open("/home/vgpnk/.agents/skills/godspeed/directive.md", encoding="utf-8").read() + "\n"

CONTEXT = (
    "/skill:godspeed\n"
    "Round-61 kake wave w1 (BUILD wave of two v1 waves; wave w2 will attack what you produce). Lane repo: " + LANE + ". Your tools start at "
    "the FLEET root (" + FLEET + "), not the lane: FIRST `mkdir -p " + SCR + "/<your seat name> && cd` there; use absolute paths for every "
    "read and write; never use a relative redirect outside your scratch dir. Every `Report:` trailer path is relative to " + LANE + " — "
    "write it at " + LANE + "/<that path> (i.e. " + R + "/<Seat>.md), never under the fleet root. Seats never mutate the fleet repo, "
    "sibling lanes, lane jj state or the lane Git index: write ONLY your own report file and, when your item says so, files inside "
    + R + "/<Seat>.files/ — no other path; no `git add/commit/stash/checkout/reset/pull/push` and no jj mutation in the lane (read-only "
    "git show/log/ls-tree/rev-parse/diff/cat-file is fine). Scratch: every clone, fixture and work dir lives under " + SCR +
    "/<your seat name>/ (pass it as TMPDIR / --work; `/tmp` only for files under 50 MB, never cited); use `git clone -q --shared` "
    "rather than full clones; delete your scratch dir before you finish (copy what you cite into your .files/ first; "
    "`trap 'rm -rf -- \"$S\"' EXIT`). Fixture repos: `D=$(mktemp -d -p " + SCR + "/<seat>) && git -C \"$D\" init -q`, every later git "
    "call names `-C \"$D\"`, verify `git -C \"$D\" rev-parse --show-toplevel` equals `$D` before the first commit, commit only with "
    "`-c user.name=selftest -c user.email=selftest@local`; never commit anywhere else. /home/vgpnk/Projects/shokuknow is read-only; "
    "sibling lane repos are read-only. Round facts: contract " + W + "/contract.md (+ contract.json) — READ IT FIRST; base revision "
    + BASE + " (lane master at round open); access date 2026-10-27 (UTC). Claims: C1 calibration — scripts/receipt_lineage.py + "
    ".ufo/receipt-disclosures.json make undisclosed receipt rewrites detectable in-lane (counter c61_lineage_cases.py, 18 cases, "
    "population of 144 frozen control files, to be built this wave); C2 operability — GET-only scripts/response_snapshot.py captures "
    "the 12 public surfaces' response headers and offline scripts/header_audit.py audits them against declared expectations "
    "(counter c61_header_cases.py, 18 cases; new rows S430-S433 opened this round); C3 freshness — the ten oldest registry rows "
    "S001-S010 re-verified live and their recheck cadences pinned to concrete dates (counter c61_recheck_pins.py, 6 conditions). "
    "Receipt population list: " + W + "/controls/population-144.txt. Quote rule (rows/entries): every quote 6..25 whitespace tokens "
    "and <= 160 characters, a substring of one whitespace-collapsed text node of the retained body, page-unique; ASCII double quotes. "
    "NO seat scores an after-state: the counters are frozen by the L1 after this wave, before any measurement. Never fabricate: an "
    "unrun check is reported as unrun; mark unverified statements [INFERENCE]. No credentials, tokens, op:// refs or private URLs in "
    "any report. Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read "
    "/home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason). Pacman guard: all "
    "pacman transactions are PAUSED host-wide — never run pacman; install via `uv tool`/`npx`/an official binary in ~/.local/bin or "
    "report the need; never restart a host service. The host is loaded: generous timeouts, no retry loops. Report format: first line "
    "`# <your seat name>`, then the sections your item names, factual, under ~150 lines (code goes in .files/, not inline); last "
    "line `VERDICT: <one line>`. The L1 (KakeR61) holds the planner seat and integrates; you are a leaf: no subagent dispatch except "
    "an executor's single read-only labrat probe."
)

items = []


def add(name, role, text):
    for k, v in (("{W}", W), ("{R}", R), ("{LANE}", LANE), ("{SRC}", SRC), ("{CAP}", CAP), ("{REC}", REC),
                 ("{KNOW}", KNOW), ("{STAGED}", STAGED), ("{FLEET}", FLEET), ("{BASE}", BASE), ("{SCR}", SCR),
                 ("{W60}", W60), ("{W23}", W23)):
        text = text.replace(k, v)
    items.append({"name": name, "role": role, "prompt": GODSPEED + text})


TOOL1 = ("Implement {LANE}/scripts/receipt_lineage.py EXACTLY to contract § Claim C1 (CLI `--root --revision [--disclosures] [--json] "
         "plus --selftest`; read-only; stdlib Python; committed bytes only via git plumbing — `git rev-list --first-parent`, "
         "`git cat-file`, `git ls-tree` — never the worktree; inherited GIT_* env scrubbed; --root must be a repository toplevel; "
         "receipt grammar `# receipt:` / EXIT= / `^VERDICT:`; result-span regex and rewrite/pending_filled/phantom_disclosure rules "
         "exactly as frozen; summary line `receipts=<n> events=<k> undisclosed=<m> met=<bool>`; exits 0/1/2/64). Include a --selftest "
         "that builds its own fixture repos under TMPDIR and prints a `PASS/FAIL` tally. Scratch and fixtures only under {SCR}/<seat>.")

# ---- C1 calibration: receipt lineage ------------------------------------------------------------------
add("ExecC1Tool", "executor", "Claim C1, primary implementation. " + TOOL1 +
    " Report sections: `DESIGN:` (rule-to-code map, line refs), `SELFTEST:` (tally), `LIMITS:`.")
add("ExecC1Tool2", "executor", "Claim C1, second INDEPENDENT implementation for later differential comparison (do not coordinate). " + TOOL1 +
    " Report sections: `DESIGN:`, `SELFTEST:`, `LIMITS:`.")
add("ExecC1Counter", "executor",
    "Claim C1 counter. Write {W}/c61_lineage_cases.py EXACTLY to contract § Claim C1 (18 cases L1-L16 + R1/R2; the tool extracted "
    "with `git show <rev>:scripts/receipt_lineage.py`, absent tool fails every case; fixture repos `git init`ed per case under "
    "--work with --seed-drawn ids; frozen population list read from {W}/controls/population-144.txt, pinned in the counter; "
    "member_changed/extra_member at the measured revision; scores_held term reading SCORECARD.md axis table 10/10/2; PREDICATE "
    "constant; exits 0/1/2/64; --selftest with no-tool/always-clean/always-exit-1/sniffing controls). Do NOT run it against the lane "
    "after-state; you may run the fixture cases against your own scratch builds. Report sections: `DESIGN:`, `SELFTEST:` (tally), "
    "`CONTRACT AMBIGUITIES:`.")
add("ExecC1History", "executor",
    "Claim C1 data. Walk the REAL first-parent history of every path in {W}/controls/population-144.txt from its first commit "
    "through the base revision {BASE} and extract every event the contract's rules would flag: for each receipt file, each commit "
    "changing its blob, the result-span diff (from -> to lines), kind (rewrite / pending_filled). Use scratch clones under "
    "{SCR}/ExecC1History. Output the raw events table to {R}/ExecC1History.files/events.tsv (columns: path, commit, kind, "
    "parent_commit, changed_result_lines). Report sections: `EVENTS:` (count + the 10 most recent verbatim), `NON-RECEIPTS:` (how "
    "many population files never match the grammar), `RENAMES:` (paths whose history ends in a rename), `NOTES:`.")
add("ExecC1Disclose", "executor",
    "Claim C1 disclosures. From {W60}-era record: read {LANE}/.ufo/waves/round-57/receipt-errata.json (six historical relabels, "
    "rounds 52/55/56) and merge it with a fresh extraction of the same six events (verify each named path+commit still resolves in "
    "git history at {BASE}). Write the disclosures registry {LANE}/.ufo/receipt-disclosures.json with schema "
    "`kake-receipt-disclosures-v1` (`{note, entries:[{path, commit, kind, note, disclosed-by}]}`), one entry per historical event, "
    "kind `rewrite`, notes derived from the errata's own notes. This file is lane-authored round-61 work product (allowed path). "
    "Also enumerate any OTHER historical rewrite/pending events you find in rounds 57-60 control files and add entries for them. "
    "Report sections: `ENTRIES:` (count, per-entry one-line), `EXTRA EVENTS:` (beyond the errata six), `VERIFICATION:` (each "
    "path+commit resolves at {BASE}).")
add("ExecC1DiscloseCheck", "reviewer",
    "Claim C1 cross-check. Independently walk the first-parent history of the 144 population paths (scratch clone under "
    "{SCR}/ExecC1DiscloseCheck) and verify: (a) every rewrite/pending_filled event you find is covered by an entry in "
    "{LANE}/.ufo/receipt-disclosures.json (path+commit equal), (b) no entry is a phantom (its commit touches its path and the "
    "result span changes), (c) the JSON parses against the schema note. Report sections: `EVENTS FOUND:` (count), `COVERED:` "
    "(count), `UNCOVERED:` (each, verbatim), `PHANTOMS:` (each), `VERDICT:`.")
add("ScoutC1Shapes", "scout",
    "Claim C1 recon. Classify every path in {W}/controls/population-144.txt at {BASE}: receipt (matches the grammar) vs "
    "non-receipt; list the distinct result-tail shapes receipts actually carry (EXIT= lines, met=, VERDICT:, members=, "
    "revision: lines, `# receipt:` headers — which rounds use which); flag edge shapes the contract rules might misclassify: "
    ".json receipts, multi-line result spans, UTF-8 paths, files under nested subdirs, empty files, files whose first version "
    "predates round 40. Report sections: `CLASSES:` (counts), `SHAPES:` (round -> tail shape), `EDGE CASES:` (each with path), "
    "`CONTRACT FIT:`.")
add("CriticC1Semantics", "critic",
    "Attack claim C1's rule family BEFORE it is frozen. For each rule (grammar detection, result span, rewrite event, "
    "pending_filled, disclosure cover, phantom, range bound, member/extra_member): construct the cheapest false green (an "
    "undisclosed rewrite the tool/counter would miss) and false red (a benign history it would flag). Work in scratch fixtures "
    "under {SCR}/CriticC1Semantics; do not edit the lane. Report sections: `FALSE GREENS:` (each: construction, missed rule), "
    "`FALSE REDS:` (each), `TIGHTENINGS:` (minimal contract edits that close each), `VERDICT:`.")
add("CriticC1Cheat", "critic",
    "Attack the c61 counter design. Cheats to try in scratch: a tool that detects fixture repos (single-path history, seeded "
    "ids) and goes honest only on the real lane; a counter that reads the worktree instead of committed bytes; a counter whose "
    "frozen population list is the measured revision's list rather than the base list; a tool that hard-codes the 16 expected "
    "fixture shapes; a tool that treats disclosure entries with wrong case as covering. For each: caught by which frozen rule, "
    "or name the tightening. Report sections: `CHEATS:` (cheat, caught?, rule), `TIGHTENINGS:`, `VERDICT:`.")
add("ReviewerC1Contract", "reviewer",
    "Review contract § Claim C1 ({W}/contract.md) line by line against kake's QUALITY.md bar and CORPUS.md rules: predicate "
    "single-sentence check, kill-rule completeness, do-nothing reachability (can a do-nothing control score the target?), "
    "population-rule precision, receipt-grammar precision (would `# receipt:` as ONE of three grammar forms catch the r56/r57 "
    "defect receipts — check what those files' first versions actually looked like via git history), amendment surface. "
    "Report sections: `FINDINGS:` (severity, issue, fix), `VERDICT:`.")
add("ScribeC1Rows", "scribe",
    "Draft the SKILL.md gate-registry rows for the two new C1 instruments, in the lane's exact 8-cell table format (`| Name | "
    "Kind | Entry command | Verdict map | Pinned values / frozen proof | Write scope | Owner |` — mirror the round-60 rows at "
    "{LANE}/SKILL.md lines 1355-1358): one row for `receipt-lineage-tool` (scripts/receipt_lineage.py; kind `tool`, read-only "
    "description, entry command `python3 -B scripts/receipt_lineage.py --root . --revision <rev> [--disclosures <path>] [--json]`, "
    "verdict map 0=undisclosed=0 / 1=findings / 2=unevaluable / 64=usage, selftest named) and one for `lineage-cases-counter` "
    "(.ufo/waves/round-61/c61_lineage_cases.py; kind `gate`, verdict map 0=18/18 + scores_held / 1=not met / 2 / 64). No `|` "
    "inside cells. Write to {R}/ScribeC1Rows.files/rows.md. Report sections: `ROWS:`, `NOTES:`.")
add("SentinelC1Bounds", "sentinel",
    "Review the receipt_lineage.py design surface for execution safety BEFORE freeze (read the two implementations under "
    "{SCR} if present, else reason from the contract): no shell invocation, no network, no writes outside stdout, git plumbing "
    "only, env scrub, path traversal via population paths (a path like `../../x` — can it escape the repo?), symlinked control "
    "files, giant blobs (caps), `GIT_DIR`/`GIT_WORK_TREE` injection. Report sections: `FINDINGS:` (severity, line/rule, fix), "
    "`VERDICT:`.")

# ---- C2 operability: header audit ---------------------------------------------------------------------
AUDIT = ("Implement {LANE}/scripts/header_audit.py EXACTLY to contract § Claim C2 (offline, network-free; manifest v1 with "
         "checks[{id,source,url,https,expect{content_type_present,hsts_present,xcto_nosniff_value,csp_present,singleton_fields[]}}]; "
         "expectation classes exactly as frozen; per-check could_not_evaluate vs exit 2 semantics; findings `<check-id> <class> "
         "<detail>` + summary `checks=<n> findings=<k>`; exits 0/1/2/64; --selftest). ")
add("ExecC2Capture", "executor",
    "Claim C2 capture tool. Write {LANE}/scripts/response_snapshot.py: GET-only capture of the 12 surfaces listed in "
    "{W23}/live/ (each subdir's fetch.json names id + url) writing {CAP}/<id>/response.json (final status, finalUrl, ordered "
    "header name/value pairs with duplicates preserved, body sha256, bytes, fetchedAt, userAgent `round61`); no cookies, "
    "credentials or request body; at most 5 redirects, 20 s, 2 MiB; one GET per surface; honour TMPDIR for temp files. RUN it "
    "(network GETs of public surfaces only) and keep the receipts. Report sections: `TOOL:` (path), `CAPTURE:` (12 rows: id, "
    "status, finalUrl, header count, bytes, sha256 head), `FAILURES:` (any surface unreachable — name it, no retry storm), `LIMITS:`.")
add("ExecC2Audit", "executor", "Claim C2, primary implementation. " + AUDIT +
    "Report sections: `DESIGN:`, `SELFTEST:` (tally), `LIMITS:`.")
add("ExecC2Audit2", "executor", "Claim C2, second INDEPENDENT implementation for differential comparison (do not coordinate). " + AUDIT +
    "Report sections: `DESIGN:`, `SELFTEST:`, `LIMITS:`.")
add("ExecC2Counter", "executor",
    "Claim C2 counter. Write {W}/c61_header_cases.py EXACTLY to contract § Claim C2 (18 cases H1-H18 + R3/R4; fixture manifests "
    "with --seed-drawn ids under --work; the audit tool extracted with `git show <rev>:scripts/header_audit.py`; R3 binds the "
    "real manifest to the 12 capture receipts; PREDICATE constant; exits 0/1/2/64; --selftest with no-tool/always-clean/"
    "always-exit-1/sniffing controls). Do NOT run it against the lane after-state. Report sections: `DESIGN:`, `SELFTEST:` "
    "(tally), `CONTRACT AMBIGUITIES:`.")
add("ExecC2Manifest", "executor",
    "Claim C2 manifest. From the capture receipts in {CAP}/ (produced by ExecC2Capture; if absent, build from your own run of "
    "the capture tool), write the manifest {W}/capture/manifest.json (version 1, 12 checks, ids matching the surface ids, "
    "source pointing at each response.json, expect: content_type_present=true for all; hsts_present=true iff url scheme is "
    "https; xcto_nosniff_value=true; csp_present=true; singleton_fields=[content-type, content-security-policy, "
    "strict-transport-security] per check). Declare expectations from POLICY (uniform rules), never tuned per outcome. Report "
    "sections: `MANIFEST:` (path + 12-row table of declared expects), `POLICY NOTE:`, `RECEIPTS:` (sha256 of each response.json).")
add("ScoutC2Sources", "scout",
    "Open the four C2 sources and retain them. One GET each (public docs; userAgent `round61`): S430 https://www.rfc-editor.org/"
    "rfc/rfc6797.html (HSTS), S431 https://www.w3.org/TR/CSP3/ (CSP), S432 https://fetch.spec.whatwg.org/ (nosniff), S433 "
    "https://www.rfc-editor.org/rfc/rfc9110.html (Content-Type + field lines). For each: write the body to {SRC}/S430.html etc., "
    "and a receipt entry (url, effectiveUrl, status, sha256, bytes, fetchedAt, userAgent) appended to {SRC}/receipts.json "
    "(create as `{\"receipts\":[]}` if absent). Then locate, per source, the exact spans the entry will quote (6..25 whitespace "
    "units, <=160 chars, one whitespace-collapsed text node, page-unique, ASCII): S430 — the sentence conveying that the HSTS "
    "policy is signalled by the Strict-Transport-Security field; S431 — the sentence stating the Content-Security-Policy header "
    "field conveys the policy (per Section 3.1 / security policy delivery); S432 — the nosniff definition of "
    "X-Content-Type-Options; S433 — the Content-Type field definition (§8.3) and the field-line/singleton semantics you rely on "
    "(§5.2/5.3). Write spans to {R}/ScoutC2Sources.files/spans.md. Report sections: `FETCHES:` (4 rows), `SPANS:` (per id: "
    "span, unit count, location), `MISSES:` (any span not found — say so), `VERDICT:`.")
add("ScoutC2Population", "scout",
    "Recon the capture population. Read every {W23}/live/<id>/fetch.json and manifest.json: list the 12 ids + urls + expected "
    "canonical, and check each url's scheme/host today with ONE GET each (status + finalUrl only, no body retention beyond "
    "headers you already need) to catch dead or moved surfaces before the capture run. Report sections: `POPULATION:` (12 rows), "
    "`CHANGES:` (vs the round-23 record), `VERDICT:`.")
add("ScribeC2Entry", "scribe",
    "Draft {KNOW}/response-header-expectations.md (do NOT write the lane file; write the draft to {R}/ScribeC2Entry.files/entry.md). "
    "Structure per CORPUS.md: opens with `source: S430, S431, S432, S433`, `verified-at: 2026-10-27`, `recheck: 180d`; then sections "
    "per expectation class (content_type_present, hsts_present, xcto_nosniff_value, csp_present, singleton_fields, field_name_syntax) "
    "each with its located quote(s) from the retained bodies ({SRC}/S43x.html; spans from ScoutC2Sources if present, else derive "
    "your own and verify), a plain-language publisher reading, and the class's audit semantics; then `## Lane use` — the capture + "
    "audit flow, what is NOT claimed (no live serving claim, no policy endorsement, no renderer/MIME-sniffing judgment beyond the "
    "recorded headers), and `## Limits`. Mark any sentence that is the lane's reading. Report sections: `ENTRY:` (pointer), "
    "`SPAN CHECK:` (each quote: units, chars, page-unique?), `READINGS:` (which sentences are lane readings).")
add("ScribeC2Rows", "scribe",
    "Draft the four registry rows + Gate lines. Write {R}/ScribeC2Rows.files/rows.md: rows S430-S433 in the exact 11-cell "
    "registry schema (id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by — mirror "
    "existing rows in {LANE}/corpus/SOURCES.md): kind `spec`, tier A, status `mined`, opened `2026-10-27`, recheck `180d`, "
    "used-by `corpus/knowledge/response-header-expectations.md`; scopes: S430 `HSTS policy signalling (STS response header)`; "
    "S431 `Content-Security-Policy header as policy conveyance`; S432 `X-Content-Type-Options nosniff value rule`; S433 "
    "`Content-Type field semantics and HTTP field-line rules`; anchors name the located section per ScoutC2Sources; teaches "
    "one grounded benefit each. Then the lesson Gate lines (per CORPUS.md rule 1: `S43N — <url> — opened 2026-10-27 — "
    "\"<span>\"`). Also build the append block and run the mirror-census validation exactly like round 60 did "
    "({W60}/validate_append.sh is copied at {W}/validate_append.sh — read it, replicate its mirror under "
    "{SCR}/ScribeC2Rows/validate, paste your four rows in, run /home/vgpnk/Projects/shokunin/scripts/sources-census.sh "
    "validate --file <mirror>/corpus/SOURCES.md and record the exit). Report sections: `ROWS:`, `GATE:`, `CENSUS:` (exit + "
    "warnings).")
add("CriticC2Semantics", "critic",
    "Attack claim C2's expectation classes: for each of the six classes, is the expectation actually what the cited source "
    "says (open the retained bodies in {SRC}/ and quote-check), and is the class decidable from recorded headers alone? "
    "Find the cheapest false green (e.g. hsts_present satisfied by a syntactically present but empty header — does the class "
    "rule catch empty values? should it?) and false red. Work read-only; propose minimal contract tightenings. Report "
    "sections: `CLASS CHECKS:` (per class: source-faithful?, decidable?, issues), `FALSE GREENS:`, `FALSE REDS:`, "
    "`TIGHTENINGS:`, `VERDICT:`.")
add("CriticC2Cheat", "critic",
    "Attack the c61_header_cases counter design. Cheats: audit tool that pattern-matches the 18 fixture manifests; counter "
    "that reads the worktree; manifest tuned per-outcome (declaring all expects false to force clean); capture receipts "
    "fabricated after the audit (receipt sha order); a tool treating `Set-Cookie` duplicates as singleton findings. For "
    "each: caught by which frozen rule, or name the tightening. Report sections: `CHEATS:`, `TIGHTENINGS:`, `VERDICT:`.")
add("ReviewerC2Contract", "reviewer",
    "Review contract § Claim C2 against QUALITY.md + CORPUS.md: predicate single-sentence, R3's not-asserted-clean wording, "
    "manifest shape freeze, capture constraints (GET-only caps), the S433 W04 duplicate-URL-across-scopes disclosure, "
    "tier assignments, quote-rule fit, capability-row pre-claiming risk. Report sections: `FINDINGS:` (severity, issue, "
    "fix), `VERDICT:`.")
add("MutationC2Probe", "mutation-tester",
    "Mutation-test the header_audit design BEFORE freeze: take the contract's 18-case table, implement the cheapest 12 "
    "mutants of the expected semantics in scratch (off-by-one on singleton counting, case-sensitive header names, OWS not "
    "trimmed, 2xx boundary at 200-only, content-type matched on value instead of name, nosniff compared lowercase, exit "
    "2 on first manifest fault instead of per-check, etc.). Run each mutant against the H-fixture shapes you build under "
    "{SCR}/MutationC2Probe and report which cases kill which mutants; list surviving mutants and the fixture additions "
    "that would kill them. Report sections: `MUTANTS:` (12 rows: mutant, killed by case), `SURVIVORS:`, `ADDITIONS:`, `VERDICT:`.")
add("SentinelC2Net", "sentinel",
    "Review the capture tool's network surface AFTER ExecC2Capture lands (read {LANE}/scripts/response_snapshot.py): GET-only "
    "proof (no POST body, no cookies), redirect cap and off-switch, size/time caps, no file writes outside {CAP}, no secrets "
    "in receipts, userAgent tag, and the receipts' sha integrity. Also verify the 12 response.json files parse and each "
    "carries the claimed keys. Report sections: `FINDINGS:` (severity, issue, fix), `RECEIPTS:` (12-row parse table), `VERDICT:`.")
add("ExecC2HeaderRecon", "executor",
    "Read the 12 capture receipts ({CAP}/<id>/response.json) and produce the header census the report will cite: per surface, "
    "presence of content-type / strict-transport-security / x-content-type-options / content-security-policy, singleton "
    "duplicates among the three singleton names, and any field-name syntax fault. Cross-check with the audit tool's own "
    "output once ExecC2Audit lands (run it on the manifest if present; else note the dependency as unrun). Report sections: "
    "`CENSUS:` (12-row table), `FINDINGS:` (what the audit will flag), `CROSS-CHECK:` (audit output or UNRUN).")
add("ReviewerC2EntryQuotes", "reviewer",
    "After ScribeC2Entry lands, verify the drafted entry's quotes: every double-quoted span is a substring of the retained "
    "body named for its row, 6..25 whitespace units, <=160 chars, page-unique, and the sentence's meaning supports the "
    "expectation class the entry attaches it to (quote truth is not semantic support — name any sentence where the entry "
    "overreaches the quote). Report sections: `SPANS:` (per quote: found?, units, support OK?), `OVERREACH:` (each), `VERDICT:`.")

# ---- C3 freshness: recheck pins -----------------------------------------------------------------------
add("ExecC3Fetch", "executor",
    "Claim C3 fetches. One GET each (userAgent `round61`) for the ten due rows S001-S010 (URLs from {LANE}/corpus/SOURCES.md): "
    "write each body to {REC}/Sxxx.html and append a receipt per row to {REC}/receipts.json (url, effectiveUrl, status, sha256, "
    "bytes, fetchedAt, userAgent) — create the file as `{\"receipts\":[]}` if absent. Follow the contract's fetch ethics: no "
    "cookies, no POST, <=5 redirects, 20 s, 2 MiB. Report sections: `FETCHES:` (10 rows: id, status, bytes, sha256 head), "
    "`FAILURES:` (each with the exact error), `VERDICT:`.")
add("ExecC3Quote", "executor",
    "Claim C3 quote re-location. For each of S001-S010, extract the row's anchor description from {LANE}/corpus/SOURCES.md "
    "and re-locate the anchor material in the fresh body {REC}/Sxxx.html (the quoted spans / section names the row's anchor "
    "and teaches cells rely on; use {W60}/span_tools.py-style whitespace-collapsed text-node matching where helpful). "
    "Verdict per row: `anchor_found` (with the located span + unit count), `anchor_moved` (page OK, material relocated — "
    "new location), `page_changed` (material absent), `fetch_failed`. Write the verdict table to {R}/ExecC3Quote.files/"
    "verdicts.tsv. Report sections: `VERDICTS:` (10 rows), `NOTES:`.")
add("ExecC3Pins", "executor",
    "Claim C3 pin table. Compute the exact registry cell edits for the ten rows per the contract pin rule: for rows with "
    "anchor_found, the new recheck cell = opened + cadence (Nd) or opened + 90d (on-release/on-use); produce a table "
    "row-id | old cell | new cell | bound check (opened < new <= opened+cadence for Nd). For non-anchor_found rows: no pin, "
    "Gate note text naming the observed state. Do NOT edit the registry — output to {R}/ExecC3Pins.files/pins.tsv plus the "
    "proposed new cell strings. Report sections: `PINS:` (table), `BOUND CHECKS:`, `SKIPS:` (rows not pinned + reason).")
add("ExecC3Counter", "executor",
    "Claim C3 counter. Write {W}/c61_recheck_pins.py EXACTLY to contract § Claim C3 (offline; committed bytes only via git "
    "plumbing; conditions C1-C6; frozen due-set rule re-derived at the measured revision; pinned-date bounds vs base "
    "cadences; Gate-line checks against {LANE}/corpus/lessons/round-61.md at the revision; receipt checks against {REC}/; "
    "append-only registry check vs base for non-due rows; PREDICATE constant `met: conditions_passed == 6 of 6`; exits "
    "0/1/2/64; --selftest with constant-control and base-tree controls). Do NOT run it against the lane after-state. Report "
    "sections: `DESIGN:`, `SELFTEST:` (tally), `CONTRACT AMBIGUITIES:`.")
add("ScoutC3Rows", "scout",
    "Independently re-derive the due set at {BASE} from {LANE}/corpus/SOURCES.md (non-rejected rows, oldest opened, ties by "
    "lowest id) and verify it equals the contract's frozen ten; then check each of the ten rows' cells are well formed (11 "
    "cells, no pipe inside a cell, opened 2026-10-19) and report their current recheck cells verbatim. Report sections: "
    "`DUE SET:` (re-derived, 10 ids), `MATCH:` (equals frozen?), `CELLS:` (10 rows verbatim), `VERDICT:`.")
add("CriticC3Rule", "critic",
    "Attack claim C3's pin rule: the opened+90d default for on-release/on-use rows (is it honest or arbitrary?), the bound "
    "`opened < pinned <= opened+cadence` (edge: pinned == opened+cadence exactly — allowed by the contract's <=; should "
    "it be?), tie-breaking by lowest id (any stake?), the ten-row width, and the no-pin-on-quote-missing carry (could a "
    "lane leave rows stale forever by claiming quote-missing? what disclosure does the Gate note require?). Report "
    "sections: `ATTACKS:` (each + consequence), `TIGHTENINGS:`, `VERDICT:`.")
add("ReviewerC3Contract", "reviewer",
    "Review contract § Claim C3 against QUALITY.md + CORPUS.md: predicate single-sentence, condition C6's byte-identity "
    "check feasibility (how expensive is base-vs-revision diff of the whole registry?), the due-set freeze wording, the "
    "do-nothing reachability of C2's failure at base, amendment surface. Report sections: `FINDINGS:` (severity, issue, "
    "fix), `VERDICT:`.")

# ---- frontier, cross-claim, contract ------------------------------------------------------------------
add("ScribeLessonMistakes", "scribe",
    "Draft corpus/lessons/round-61.md (write the draft to {R}/ScribeLessonMistakes.files/lesson.md; the L1 lands it). "
    "Sections: `# Round 61` (date, base, claims one line each); `## Mistakes` — at minimum the mined mistake row: class "
    "`process/undisclosed-receipt-rewrite` · evidence `corpus/lessons/round-56.md`-verifier + `round-57`-verifier findings "
    "and considerthese/2026-10-26.md proposal 2 · captured-by `none` (only the external verifier caught the class) · fix "
    "`scripts/receipt_lineage.py` + `.ufo/receipt-disclosures.json` + counter c61_lineage_cases.py cases L2/L6/L7 "
    "(shown able to fail); plus rows for R60-D2 (EN-unit erratum: the round-60 scout printed 19 units where the lane's "
    "units() measures 22 — correction note, no claim) and R60-D3 (# receipt header convention, now in the contract receipt "
    "rule); `## Gate` skeleton with placeholders for the C2 rows (S430-S433), the C3 ten rows, the assimilation "
    "admit/reject record; `## Carried` (R60-D4 coupling routing, R60-D5 quarantine hold, R60-D6 SHONEN). Report sections: "
    "`LESSON:`, `MISTAKE ROWS:` (count), `GATE SKELETON:`.")
add("ScribeSearchLog", "scribe",
    "Write the round-61 search log draft to {R}/ScribeSearchLog.files/searchlog.md per CORPUS.md rule 5 (one prose note per "
    "bounded search: what was looked for, where, what was found/not found, commands): cover (a) whether any existing lane "
    "tool already detects receipt rewrites (grep scripts/ + corpus/knowledge/ for lineage/rewrite/receipt-history), (b) "
    "whether any lane gate already audits response headers (grep scripts/), (c) the considerthese proposals not taken this "
    "round (1, 3, 4, 5) with one-line reasons. Report sections: `SEARCH LOG:`, `COMMANDS:` (verbatim).")
add("ConnSiblingOverlap", "connector",
    "Sibling-overlap scan: which fleet lanes own adjacent ground to this round's three claims (receipt/measurement "
    "integrity, HTTP response-header semantics, registry recheck)? Read the sibling SKILL.md/PROVINCE.md headers only "
    "(fleet root children: /home/vgpnk/Projects/shokunin/*-shokunin/SKILL.md + PROVINCE.md — read-only). Report sections: "
    "`OVERLAPS:` (lane, file:line, what), `CONTESTED:`, `VERDICT:`.")
add("ConnCrossClaim", "connector",
    "Cross-claim coupling scan: read {W}/contract.md and list every way C1/C2/C3 could interact (shared files, shared "
    "commits, counter populations, registry appends vs cell edits, the capture receipts feeding both C2's counter and the "
    "report) and whether the contract's separability paragraph covers each; name any missed interaction as a contract "
    "amendment candidate. Report sections: `SEPARABILITY:`, `SHARED WEAKNESSES:`, `INTERACTIONS:`, `AMENDMENTS:`, `VERDICT:`.")
add("CriticAxisLabels", "critic",
    "Check the axis story: C1 calibration / C2 operability / C3 freshness — does each claim actually move its named axis "
    "per AXES.md's definitions, is the lowest-axis obligation met (calibration 2 < 10/10), are the claims causally "
    "separable as declared, and would a do-nothing control reach any target (read the contract's do-nothing rows and "
    "verify each target fails at base)? Report sections: `C1:`, `C2:`, `C3:`, `DO-NOTHING CHECKS:`, `VERDICT:`.")
add("ExecQuarantine", "executor",
    "Re-derive the kake quarantine slice exactly per the §10 contract (register read-only; data rows: lane, round, S-id): "
    "S=/home/vgpnk/Projects/shokuknow; R=$S/.ufo/waves/corpus-expansion-1/absent-defect-register.md; awk -F'|' -v l='kake' "
    "'$2 ~ (\"`\" l \"`\") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \"$R\". Compare the slice byte-for-byte "
    "against the round-60 record {W60}/assimilation/quarantine-slice (or the round-60 report's naming of it) and against "
    "the round-58 derivation; every line must carry an S-id. Verdict per row stays as previously recorded (held) — do NOT "
    "re-open the URLs this round. Output the slice to {W}/assimilation/quarantine-slice with the comparison notes. Report "
    "sections: `SLICE:` (row count + head), `BYTE-COMPARE:`, `VERDICT:`.")
add("ScoutOperatorLessons", "scout",
    "Read {LANE}/corpus/lessons/operator-*.md (newest three) and /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md (read-"
    "only): list the operator teachings not yet reflected in the round-61 contract and the L0 rows that remain open "
    "(quarantine hold; calibration-ownership ruling; S367 CJK unit rule). Map each to where the round routes around it. "
    "Report sections: `OPERATOR LESSONS:`, `L0 ROWS:` (each + routing), `INHERITED:`.")
add("ReviewerContract", "reviewer",
    "Whole-contract review LAST: read {W}/contract.md + contract.json end to end after every other w1 report exists "
    "({R}/). Check: the three predicates are each one sentence and identical between the prose, contract.json and the "
    "counter tasks; the frozen tables (L1-L16+R1/R2, H1-H18+R3/R4, C1-C6) are internally consistent; amendment surface is "
    "named; the report-contract sections (claims, measurements, sources, trends, SHONEN) can be filled from what w1 "
    "produces. List every inconsistency with severity. Report sections: `FINDINGS:` (severity, issue, fix), `VERDICT:`.")

SPEC = {"reportDir": ".ufo/waves/round-61/w1", "maxLanes": 64, "context": CONTEXT, "items": items}
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
    json.dump(SPEC, open(out, "w"), indent=1)
    c = Counter(i["role"] for i in items)
    attack = sum(v for k, v in c.items() if k in ("reviewer", "critic", "mutation-tester", "sentinel"))
    print(len(items), dict(c), f"attack={attack} ({attack/len(items):.0%})")
