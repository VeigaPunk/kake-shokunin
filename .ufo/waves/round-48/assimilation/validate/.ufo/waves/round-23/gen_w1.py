#!/usr/bin/env python3
"""Generate the round-23 wave-1 spec (w1-spec.json). Deterministic; run from anywhere."""
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
R = f"{LANE}/.ufo/waves/round-23"
CAND = "4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc"
BASE = "b5d599e19bead54b96f589444e9ec64cdf67c28a"
GS = "/skill:godspeed\n\n"  # OMP task hook injects the directive bytes (shokunin host mapping)

CONTEXT = f"""# Goal
Kake lane round 23 only (web properties and publishing; axes operability + freshness). Frozen contract {R}/contract.json: C1 freshness = live re-verification of 16 historical knowledge entries + the SKILL.md property map ({R}/c1-population.json); C2 operability = first end-to-end canonical preflight over 12 live owned surfaces ({R}/c2-population.json). Candidate code commit {CAND} (base {BASE}): scripts/canonical_audit.py (now evaluates SVG/MathML and self-closed HTML void tags after a closed head) and scripts/live_snapshot.py. The L1 (KakeR22Recovery) holds the planner seat and is the sole integration writer. You are author-side; never claim independent admission.
# Contract
- All paths absolute. Lane {LANE}. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Your tools start at the FLEET root /home/vgpnk/Projects/shokunin: NEVER write a relative path or redirect (`> out.txt`) there; put every scratch file under a fresh `mktemp -d /tmp/kake-r23-<YourName>-XXXX`.
- Read-only on the lane: write ONLY your own report file. Never edit production files, never run git/jj mutations in the lane, never touch its index/jj state, the fleet repo, sibling lanes, ~/.omp config, .ufo/state. Writers (executors) work only in `git clone --no-hardlinks {LANE} /tmp/kake-r23-<YourName>-clone`, record the clone's observed HEAD, and put the produced files/diff inline in their report; the L1 integrates.
- Web properties: read-only HTTP GET/HEAD of public URLs only (no auth, cookies, forms, POST, publishing, deploys, account or DNS actions). Never send anything into a Kimi chat. Public documentation sites may be fetched. Domain source trees (e.g. ~/Projects/ufo-fsd-alpha, ~/Projects/lucario) are read-only.
- No builds/lint/formatters; targeted CLI probes and the named selftests/matrices/counters are allowed. Stay a leaf: spawn no subagents (executors may spawn one read-only labrat for one falsifiable hypothesis).
- Tooling: you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard: ALL pacman transactions are PAUSED host-wide (no -S/-Sy/-Syu/-U/-R, no host service restarts); use uv tool / npx / an official binary in ~/.local/bin, or skip. No live secrets.
- Report format: `## Verdict`, `## Findings` (severity P0–P3, exact command, exact observed output, impacted claim/axis, smallest fix), `## Checked and held`, `## Limits`. Quote exact outputs; an unrun check has not passed.
# C1 receipt schema (C1 items must include exactly one fenced ```json block with this object)
{{"unit": "<unit name from c1-population.json>", "path": "<unit path>", "observedAt": "2026-10-21", "claims": [{{"id": "c1", "anchor": "<exact substring of the unit file as it is at {BASE} (copy bytes, 20-160 chars, unique if possible)>", "claim": "<the load-bearing claim in your words>", "surface": "<URL / absolute path / exact command checked>", "method": "GET|HEAD|test -e|git|read|run", "observation": "<exact observed output, abbreviated faithfully>", "verdict": "HOLD|STALE|UNVERIFIABLE", "correction": "<STALE only: one self-contained sentence stating what is true now, dated 2026-10-21>", "reason": "<UNVERIFIABLE only: why no live surface can decide it now>"}}]}}
Choose 3-8 claims that carry the unit's operational weight (live URLs, statuses, paths, counts, commands, behaviours). A surface that no longer exists makes its claim UNVERIFIABLE (with reason) unless the claim asserts presence (then STALE). Never run a write/publish verb of any tool; read-only commands only.
"""


def item(name, role, axes, prompt):
    return {"name": name, "role": role, "axes": axes, "prompt": GS + prompt}


items = []
pop1 = json.loads(pathlib.Path(R, "c1-population.json").read_text())["units"]
for u in pop1:
    if u["unit"] == "property-map":
        items.append(item("ReverifyPropertyMapRegistry", "reviewer", ["freshness"],
            f"C1 unit `property-map` ({LANE}/SKILL.md section '## Property map' and the 'Registry of record' paragraph after it). "
            "Re-verify the NON-page claims only: each row's source dir (test -e), publish path statements checkable read-only (e.g. a repo's .github/workflows presence, CNAME file), app.ds4cc.com/mcp reachability by a single GET/HEAD status (no MCP calls), the registry-of-record paths. Page-serving status of the 12 surfaces is covered by sibling items; do not duplicate it. Emit the C1 receipt JSON (unit property-map, path SKILL.md)."))
    else:
        title = "".join(part.capitalize() for part in u["unit"].split("-"))
        items.append(item(f"Reverify{title}"[:32], "reviewer", ["freshness"],
            f"C1 unit `{u['unit']}`: read {LANE}/{u['path']} in full. Pick its 3-8 load-bearing live claims and re-verify each NOW against its live surface (local paths/repos/timers via read-only commands; public URLs via GET/HEAD). Emit the C1 receipt JSON for unit `{u['unit']}`. For each STALE claim give the correction sentence; for UNVERIFIABLE the reason. Also list any claim you skipped and why."))

pop2 = json.loads(pathlib.Path(R, "c2-population.json").read_text())["surfaces"]
for s in pop2:
    title = "".join(part.capitalize() for part in s["id"].split("-"))
    items.append(item(f"Surface{title}"[:32], "scout", ["operability", "freshness"],
        f"C2 surface `{s['id']}` url {s['url']} expectedCanonical {s['expectedCanonical']} (policy basis: {s['policyBasis']}). Independently of the L1: (1) one read-only GET (curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D <tmp>/h -o <tmp>/b) and record status, final URL, content-type, sha256 of the body; (2) read the head by eye and derive, BEFORE running any tool, which canonical_audit verdict/finding id the frozen policy implies ({LANE}/.ufo/waves/round-22/contract.json policy; head-only, one canonical equal to expectedCanonical); (3) run python3 {LANE}/scripts/canonical_audit.py --manifest <tmp>/manifest.json --json on your snapshot and compare; (4) judge whether expectedCanonical is the right local policy for this surface given {LANE}/SKILL.md property map and what the page itself declares; (5) emit C1 property-map claim rows for this surface (unit property-map, anchors from the SKILL.md property-map row text) in a fenced json block shaped like the C1 receipt; (6) name the upstream fix (documented only, never applied)."))

for name, focus in [("FalsifyForeignContent", "SVG/MathML after a closed head: nested svg/math, mismatched end tags, </svg> missing, <foreignObject> containing HTML, svg <title>/<style>/<script>, a canonical link inside foreignObject, CDATA, a second <head> or <base> inside svg"),
                    ("FalsifyVoidSelfClose", "self-closed HTML void tags after the head (<input/>, <img/>, <br/>, <hr/>, <source/>, <wbr/>), non-void self-closing (<div/>, <span/>, <p/>), self-closed tags before </head>, uppercase tag names, attributes with '/>' in values"),
                    ("FalsifyRefinementRegression", f"regression: run python3 {LANE}/.ufo/waves/round-22/matrix.py --root {LANE} --json (must be 32/32), python3 {LANE}/scripts/canonical_audit.py --selftest, and diff `git -C {LANE} show b539cc1:scripts/canonical_audit.py` against {CAND}; argue whether any previously unsupported input now becomes a false clean")]:
    items.append(item(name, "reviewer", ["operability"],
        f"Attack the validator refinement in {CAND} (scripts/canonical_audit.py, CanonicalHTMLParser foreign_depth / HTML_VOID_ELEMENTS / handle_startendtag): {focus}. Build fixtures in your /tmp dir, invoke the public CLI, derive expected verdicts before running. A false clean (canonical signal could differ in a browser but tool says clean) is P1."))

reopen = [("ReopenGoogleCanonical", "S021", "https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls"),
          ("ReopenHTMLLink", "S023", "https://html.spec.whatwg.org/multipage/links.html#link-type-canonical"),
          ("ReopenHTMLBase", "S024", "https://html.spec.whatwg.org/multipage/semantics.html#the-base-element"),
          ("ReopenHTMLTemplate", "S025", "https://html.spec.whatwg.org/multipage/scripting.html#the-template-element"),
          ("ReopenPythonParser", "S026", "https://docs.python.org/3/library/html.parser.html")]
for name, row, url in reopen:
    items.append(item(name, "scout", ["freshness"],
        f"Carried from round-22 dead wave-2 seat (never ran). Re-open {url} and attack row {row} in {LANE}/corpus/SOURCES.md plus its round-22 Gate quote in {LANE}/corpus/lessons/round-22.md: exact quote location (≤25 words), access date/version, tier scope, used-by paths exist and actually cite {row}; check {LANE}/corpus/knowledge/static-canonical-preflight.md for overclaim from this source. Report agree/disagree per field."))

items.append(item("Attack23WrongHost", "reviewer", ["operability"],
    f"Carried from round-22 dead wave-2 seat Attack23. Attack frozen case 'wrong_host' at {CAND}: read {LANE}/.ufo/waves/round-22/cases.json and its fixture, derive expected exit/id before running, run python3 {LANE}/.ufo/waves/round-22/matrix.py --root {LANE} --case wrong_host, then build one nearest-neighbour host fixture (IDN/punycode, trailing dot, port, uppercase) in /tmp and run the public CLI."))

boundary = {
    "BoundaryManifestKeys": "unknown keys, version true vs 1, empty pages, duplicate page entries, page url not absolute",
    "BoundaryTraversal": "absolute/parent/dot/backslash/NUL page paths and manifest-relative confinement",
    "BoundaryURLAuthority": "credential URLs, empty host, invalid/huge ports, IPv6 zones, whitespace and control characters",
    "BoundaryHeadRecovery": "invalid head children, second head, omitted </head>, body transitions, text in head",
    "BoundaryInertContexts": "title/style/noscript/template/script/textarea/iframe false canonical tokens",
    "BoundaryAttributes": "duplicate attributes, ASCII vs Unicode whitespace in rel, hreflang/media/type on canonical links",
    "BoundaryReadOnly": "normal clean and red invocations leave fixture byte/mode inventory unchanged (sha256 + stat before/after); no network-capable imports in scripts/canonical_audit.py",
    "BoundaryReplayIntegrity": f"round-22 replay ({LANE}/.ufo/waves/round-22/replay.py) is pinned to the b539cc1 validator: in a /tmp copy of the b539cc1 tree show tamper → snapshot_tampered exit 2 and untampered → frozen_replay_match; state what replay proves at the current tip {CAND}",
}
for name, focus in boundary.items():
    items.append(item(name, "reviewer", ["operability"],
        f"Carried from round-22 dead wave-2 seat {name}. Attack scripts/canonical_audit.py at {CAND} on: {focus}. Own /tmp fixtures, public CLI, exact outputs; one positive and one negative control; do not conflate unsupported with clean."))

connect = {
    "ConnectBrowser": "publisher static HTML preflight vs tabi browser/JS frontier and the new live-snapshot step (who owns rendered-DOM canonicals?)",
    "ConnectSource": "source hierarchy: explicit local policy vs RFC 6596/WHATWG/Google semantics, incl. the new foreign-content rule",
    "ConnectCapability": "canonical capability (r22) vs this round's end-to-end use on live owned surfaces: does C2 add operability or only re-run r22?",
    "ConnectProof": "selftest vs frozen matrix vs live snapshots vs archived domain snapshot: which proves what, no substitutes",
}
for name, focus in connect.items():
    items.append(item(name, "connector", ["operability", "freshness"],
        f"Carried from round-22 dead wave-2 seat {name}. Cross-axis attack: {focus}. Read {LANE}/PROVINCE.md, {LANE}/corpus/README.md, {LANE}/corpus/knowledge/static-canonical-preflight.md, {LANE}/SKILL.md gate registry and {R}/contract.json. Concrete path:line evidence and one counterexample to any broad assertion."))

for name, fix in [("ReviewDotdotSplit", "manifest path split without abspath (kernel resolves `..` once) in read_manifest_bytes"),
                  ("ReviewHelpSynopsis", "explicit argparse usage string vs actual accepted argument combinations and --help output"),
                  ("ReviewFdOwnership", "fd ownership transfer in read_page_bytes intermediate-directory loop; fd balance on every exception path"),
                  ("ReviewCounterPins", f"round-22 counter {LANE}/.ufo/waves/round-22/measure.py PINNED_INSTRUMENT_SHA256 and executed>=derived floor: hostile matrices in a /tmp clone")]:
    items.append(item(name, "reviewer", ["operability"],
        f"Round-22 fix verified only by probes (routed by the round-22 verifier, {LANE}/corpus/lessons/round-22-verifier-spotcheck.md note 4): {fix}. Seat-review it at {CAND}: read the code, build adversarial probes in /tmp, report exact results."))

items += [
    item("CritCounterC1", "critic", ["freshness"],
         f"Attack {R}/measure_c1.py and the C1 framing in {R}/contract.json: can a receipt pass without real live re-verification (e.g. trivial anchors, HOLD with no observation, UNVERIFIABLE as escape hatch)? Is 0/17 at the freeze commit 6847479 a failure-capable before? Is the population (historical-not-live-reverified entries + property map) honestly frozen? Propose tightening that keeps the frozen population."),
    item("CritCounterC2", "critic", ["operability"],
         f"Attack {R}/measure_c2.py and C2 in {R}/contract.json: does a reproducible receipt prove an end-to-end preflight or only that a file round-trips? Are expectedCanonical choices in {R}/c2-population.json defensible policy? Is counting not-served surfaces as passing honest? Propose the strongest admissible reading."),
    item("MutateCounterC1", "mutation-tester", ["freshness"],
         f"Mutation-test {R}/measure_c1.py in a /tmp clone of {LANE}: create a probe commit with deliberately bad receipts (missing heading, anchor absent at base, STALE without correction in section, wrong unit, duplicate ids, observedAt 2026-10-20) under .ufo/waves/round-23/receipts/ and confirm each is rejected; mutate the counter (drop each check) and report which mutants survive the bad-receipt set."),
    item("MutateCounterC2", "mutation-tester", ["operability"],
         f"Mutation-test {R}/measure_c2.py in a /tmp clone: run python3 {LANE}/scripts/live_snapshot.py --population {R}/c2-population.json --out <clone>/.ufo/waves/round-23/live in the clone (read-only GETs), commit there, confirm the counter passes; then commit tampered variants (edited page.html, edited audit.json, served page relabelled not-served, wrong url, stale fetchedAt) and confirm each fails; mutate counter checks and report survivors."),
    item("SentinelLiveSnapshot", "sentinel", ["operability"],
         f"Security/safety review of {LANE}/scripts/live_snapshot.py at {CAND}: confirm GET-only including redirects (method preservation, 307/308), no credentials/cookies, body cap, timeout, output confinement to --out (surface ids with ../ or /), content-type handling, behaviour on TLS errors; no write outside out dir. Use local probes (python -m http.server on 127.0.0.1) only."),
    item("SimplifyR23Tools", "simplifier", ["operability"],
         f"YAGNI review of {LANE}/scripts/live_snapshot.py, {R}/measure_c1.py, {R}/measure_c2.py: list deletions/simplifications that preserve verified behaviour, as a diff in your report (no lane edits)."),
    item("ScribeLessonDraft", "scribe", ["freshness", "operability"],
         f"Draft prose (in your report only) for {LANE}/corpus/lessons/round-23.md sections '## Claims' and '## Gate' from {R}/contract.json and the round-22 verifier notes in {LANE}/corpus/lessons/round-22-verifier-spotcheck.md; leave measured numbers as <TBD>. Follow the round-22 lesson's structure."),
    item("ScribeKnowledgeDelta", "scribe", ["operability"],
         f"Draft an appended section (in your report only) for {LANE}/corpus/knowledge/static-canonical-preflight.md explaining the round-23 parser boundary change (SVG/MathML and void self-closing after a closed head are evaluated; foreign content before head and canonical links inside foreign content stay unsupported) and the live-snapshot handoff, with S### placeholders for HTML-spec sources."),
    item("ScribeQualityCorrections", "scribe", ["freshness"],
         f"Draft append-only correction text (in your report only) for routed round-22 defects in {LANE}/corpus/lessons/round-22-verifier-spotcheck.md notes 1-3: the inverted 'Fails if counter-probe.py exits 0' predicate in {LANE}/corpus/QUALITY.md, lane-root err.txt/out.txt placement, and /tmp runner paths in postfix receipts (with the `git -C {LANE} show c0fd6d5:<path>` reproduction commands)."),
    item("ExecRealPageFixtures", "executor", ["operability"],
         f"In a /tmp clone of {LANE} at {CAND}: build 12+ realistic static-site fixtures (Hugo, Jekyll, Astro, Eleventy, Next static export, plain hand-written) each as page.html + manifest.json, including inline SVG icons, <input />, <img />, preload links and JSON-LD; derive the expected canonical_audit verdict for each before running; run the public CLI; report a table and the fixture files (inline or as a tarball base64 if small)."),
    item("ExecCounterSelftest", "executor", ["freshness"],
         f"In a /tmp clone of {LANE} at {CAND}: write {R.replace(LANE, '.')}/counter_selftest.py that builds a throwaway git repo in a temp dir with good and bad C1 receipts and C2 live receipts, runs measure_c1.py/measure_c2.py against it and asserts pass/fail per case (exit 0 iff all expectations met). Report the file content inline and its run output."),
    item("ExecReproduceBefore", "executor", ["operability"],
         f"In a /tmp clone of {LANE}: write .ufo/waves/round-23/routed/reproduce-r22-before.sh that recreates the round-22 before-fix runners via `git show c0fd6d5:scripts/canonical_audit.py` and `git show c0fd6d5:.ufo/waves/round-22/measure.py` into a mktemp dir and re-runs {LANE}/.ufo/waves/round-22/postfix/defect-probe.py and counter-probe.py against them, comparing with the committed -before.json verdicts (met counts / rejected flags). Report the script inline and its output."),
    item("ConnectSiblingOverlap", "connector", ["operability", "freshness"],
         "Sibling-overlap scan: read /home/vgpnk/Projects/shokunin/MISSION.md lane table and the SKILL.md/PROVINCE.md of tabi-shokunin and chousa-shokunin (read-only) and say where round-23's live snapshots, property-map re-verification and canonical policy overlap or conflict with sibling provinces; path:line evidence."),
    item("SourceHTMLVoidSyntax", "scout", ["operability"],
         "Open the WHATWG HTML Living Standard section on void elements and the self-closing start-tag syntax (https://html.spec.whatwg.org/multipage/syntax.html#void-elements and #start-tags). Return the URL, access date, a located ≤25-word quote showing the slash on void elements is allowed/ignored and that it is not allowed on non-void HTML elements, and the exact list of void elements; compare with HTML_VOID_ELEMENTS in /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py."),
    item("SourceHTMLForeignContent", "scout", ["operability"],
         "Open the WHATWG HTML parsing rules for foreign content (https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inforeign and the in-body svg/math start-tag rule) plus the 'in head' insertion mode. Return URL, access date, located ≤25-word quotes establishing (a) svg/math start tags in body insert foreign elements, (b) a <link> inside svg is an SVG-namespace element, not an HTML link, (c) whether any foreign-content path can move elements into head. Judge the validator rule at /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py against it."),
]

spec = {"wave": "kake-r23-w1", "context": CONTEXT, "reportDir": ".ufo/waves/round-23/w1", "maxLanes": 100,
        "axes": ["operability", "freshness"], "milestone": "r23-build", "items": items}
pathlib.Path(R, "w1-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
from collections import Counter
print(len(items), Counter(i["role"] for i in items))
