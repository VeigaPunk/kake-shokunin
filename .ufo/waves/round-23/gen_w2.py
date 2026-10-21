#!/usr/bin/env python3
"""Generate the round-23 wave-2 (falsify) spec w2-spec.json from the integrated receipts."""
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
R = f"{LANE}/.ufo/waves/round-23"
CAND = "5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd"  # = 83098b5 integration + counter-selftest fix only
BASE = "b5d599e19bead54b96f589444e9ec64cdf67c28a"
GS = "/skill:godspeed\n\n"  # OMP task hook injects the directive bytes (shokunin host mapping)

CONTEXT = f"""# Goal
Kake lane round 23, wave 2 = FALSIFY. Integrated candidate {CAND} (base {BASE}) is frozen for this wave. Claims (contract {R}/contract.json): C1 freshness — 17 units carry round-23 live re-verification receipts ({R}/receipts/<unit>.json; appended "## Live re-verification — round 23" sections in {LANE}/corpus/knowledge/<unit>.md and {LANE}/SKILL.md); counter python3 {R}/measure_c1.py --root {LANE} --revision {CAND} reports 17/17 (168 claims: 79 HOLD, 49 STALE, 40 UNVERIFIABLE). C2 operability — 12 owned surfaces have committed GET snapshots in {R}/live/<id>/ whose audits python3 {R}/measure_c2.py --root {LANE} --revision {CAND} reproduces 12/12; the validator {LANE}/scripts/canonical_audit.py now evaluates body SVG/MathML and void self-closing tags but rejects any base after the head. You are a fresh author-side falsifier: attack what wave 1 produced; you are not the admission authority.
# Contract
- All paths absolute. Lane {LANE}. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Your tools start at the FLEET root /home/vgpnk/Projects/shokunin: NEVER write a relative path or redirect there; scratch only under a fresh `mktemp -d /tmp/kake-r23w2-<YourName>-XXXX`.
- Read-only on the lane: write ONLY your own report. No production edits, no git/jj mutations in the lane, no index/jj state, fleet repo, sibling lanes, ~/.omp config, .ufo/state. Git writes only inside `git clone --no-hardlinks {LANE} /tmp/...` clones.
- Web properties: read-only HTTP GET/HEAD of public URLs only (no auth, cookies, forms, POST, publishing, deploys, account/DNS actions, nothing sent into a Kimi chat). Domain source trees read-only. Read-only local commands only (no systemctl start/stop/enable, no service restarts).
- No builds/lint/formatters; targeted probes and the named counters/selftests are fine. Stay a leaf (executors may spawn one read-only labrat).
- Tooling: you may install or upgrade useful tools — read /home/vgpnk/.omp/agent/RULES.md first (official channels; record tool/version/channel/reason). pacman guard: ALL pacman transactions are PAUSED host-wide (no -S/-Sy/-Syu/-U/-R, no host service restarts); use uv tool / npx / an official binary in ~/.local/bin, or skip. No live secrets.
- Report: `## Verdict` (counterexample found / none), `## Findings` (severity P0–P3, exact command, exact output, impacted claim/axis, smallest fix), `## Checked and held`, `## Limits`. Derive expectations before running; an unrun check has not passed.
"""


def item(name, role, axes, prompt):
    return {"name": name, "role": role, "axes": axes, "prompt": GS + prompt}


items = []
units = json.loads(pathlib.Path(R, "c1-population.json").read_text())["units"]
for u in units:
    receipt = json.loads(pathlib.Path(R, "receipts", f"{u['unit']}.json").read_text())
    title = "".join(p.capitalize() for p in u["unit"].split("-"))[:22]
    stale = [c["id"] for c in receipt["claims"] if c["verdict"] == "STALE"]
    rest = [c["id"] for c in receipt["claims"] if c["verdict"] != "STALE"]
    if stale:
        items.append(item(f"Stale{title}", "reviewer", ["freshness"],
            f"C1 unit `{u['unit']}`: attack the STALE claims {', '.join(stale)} in {R}/receipts/{u['unit']}.json and their corrections in the round-23 section of {LANE}/{u['path']}. For each: re-run the live check yourself (read-only), decide whether the claim is really stale and whether the correction sentence is true, complete and not overclaiming. A wrong correction is P1."))
    items.append(item(f"Hold{title}", "reviewer", ["freshness"],
        f"C1 unit `{u['unit']}`: attack the HOLD/UNVERIFIABLE claims {', '.join(rest)} in {R}/receipts/{u['unit']}.json. Re-run each HOLD check yourself (read-only); for each UNVERIFIABLE decide whether a live surface could in fact decide it now (then it should be HOLD/STALE). Also judge whether the claim selection skips a more load-bearing claim of {LANE}/{u['path']}. A HOLD that does not hold is P1."))

for s in json.loads(pathlib.Path(R, "c2-population.json").read_text())["surfaces"]:
    title = "".join(p.capitalize() for p in s["id"].split("-"))[:24]
    items.append(item(f"Recheck{title}", "scout", ["operability"],
        f"C2 surface `{s['id']}` ({s['url']}): read {R}/live/{s['id']}/fetch.json and audit.json, do one fresh read-only GET, and compare status/finalUrl/content-type/sha256 (a changed body is drift, not a defect, but say so). Derive by eye from the committed page.html head which verdict the policy implies, then confirm `python3 {R}/measure_c2.py --root {LANE} --revision {CAND}` reproduces this surface. Attack the expectedCanonical choice and the receipt's not-served/served classification."))

guards = {
    "AttackBaseGuard": "the rule 'any <base> after the closed head is unsupported': bypasses via uppercase/whitespace tag names, <base> inside template/noscript/table/select contexts, xmp/iframe raw text, comments that HTMLParser misreads (`<!--->`, `--!>`), CDATA sections",
    "AttackForeignStack": "the SVG/MathML element stack and the set_cdata_mode override: deep nesting, `</svg >` with spaces, self-closing vs open forms of the same element, text/cdata hiding inside svg <style>/<script>, a `<head>`/`<link rel=canonical>` reached after an exactly balanced stack",
    "AttackControlChars": "C0/C1/DEL rejection in normalize_http_url: base href, expectedCanonical in the manifest, document url, percent-encoded %C2%85 (must stay accepted), U+00A0 and U+2028",
    "AttackDuplicatePages": "duplicate page url/file rejection: same file under different spellings (a/../a.html is already rejected? ./a.html?), same URL differing only by normalization (default port, case), large manifests",
}
for name, focus in guards.items():
    items.append(item(name, "reviewer", ["operability"],
        f"Attack {LANE}/scripts/canonical_audit.py at {CAND}: {focus}. Build fixtures under /tmp, derive expected verdicts first, run the public CLI. A false clean is P1. Also confirm `python3 {LANE}/.ufo/waves/round-22/matrix.py --root {LANE} --json` stays 32/32 and `--selftest` passes."))

items += [
    item("MutateGuards", "mutation-tester", ["operability"],
         f"In a /tmp clone at {CAND}: mutate each new guard in scripts/canonical_audit.py (base-after-head check, foreign base/head/link token check, foreign end-tag mismatch, set_cdata_mode override, C1-control range, duplicate-page check, HTML_VOID_ELEMENTS allowance) one at a time; run `python3 scripts/canonical_audit.py --selftest` and `python3 .ufo/waves/round-23/relaxation_probe.py --validator scripts/canonical_audit.py` per mutant; report killed/survived with exact outputs; restore bytes after each."),
    item("MutateCounterSelftest", "mutation-tester", ["freshness", "operability"],
         f"In a /tmp clone at {CAND}: mutate each check in .ufo/waves/round-23/measure_c1.py and measure_c2.py (one at a time) and run `python3 .ufo/waves/round-23/counter_selftest.py` from the clone (it clones its own root); report which counter checks the selftest kills and which survive."),
    item("SentinelSnapshotV2", "sentinel", ["operability"],
         f"Re-attack {LANE}/scripts/live_snapshot.py at {CAND} after hardening: id confinement (unicode, uppercase, 64+ chars, symlinked out dir), userinfo/non-http redirects (local 127.0.0.1 server only), --reaudit with a tampered or missing fetch.json/page.html, audit-error path, writes outside --out. Local probes only."),
    item("CritCounterTightening", "critic", ["freshness"],
         f"Attack the post-wave-1 tightening of {R}/measure_c1.py (one HOLD/STALE claim per unit) and the anchor-rewrap acceptance in {R}/integrate_c1.py: was tightening the counter after seeing receipts honest given the frozen population; does whitespace-only anchor matching admit anything a strict match would wrongly reject or accept; are the 3 rejected claims in {R}/receipts/rejected.json correctly rejected?"),
    item("CritEvaluability", "critic", ["operability"],
         f"Attack the evaluability evidence: `python3 {R}/evaluability.py --root {LANE} --before b539cc1 --after {CAND}` claims served surfaces evaluated 4/8 → 8/8. Is that a fair before/after (same bytes, same expectations)? Does any newly evaluated verdict depend on behaviour a browser would not share? Is it correctly reported as part of C2, not a third claim on operability?"),
    item("CritRelaxationProbe", "critic", ["operability"],
         f"Attack completeness of {R}/relaxation_probe.py and the QUALITY criterion 'Parser relaxations' in {LANE}/corpus/QUALITY.md: list head-affecting paths from body markup the probe omits (e.g. a second canonical link reached through breakout, <meta http-equiv>, <link rel=canonical> in body after foreign content), run them against the current validator, report any clean."),
    item("ReopenS030", "scout", ["operability"],
         f"Re-open https://html.spec.whatwg.org/multipage/syntax.html#start-tags and #void-elements; attack row S030 in {LANE}/corpus/SOURCES.md and its quote in {LANE}/corpus/lessons/round-23.md (≤25 words, located, access date, tier scope, used-by paths exist and cite S030); check {LANE}/corpus/knowledge/static-canonical-preflight.md §Round 23 for overclaim."),
    item("ReopenS031", "scout", ["operability"],
         f"Re-open https://html.spec.whatwg.org/multipage/parsing.html (in body svg/math, foreign content, breakout list, HTML integration points); attack row S031 in {LANE}/corpus/SOURCES.md and its quote in {LANE}/corpus/lessons/round-23.md; check whether the knowledge entry's claim 'SVG title is an HTML integration point' and the base-anywhere rule are supported."),
    item("ReviewKnowledgeDelta", "reviewer", ["operability"],
         f"Review the appended §Round 23 of {LANE}/corpus/knowledge/static-canonical-preflight.md and the round-23 additions at the end of {LANE}/SKILL.md (gate row, replay correction) against the code at {CAND}: every statement true, no overclaim, commands runnable as written (run them)."),
    item("ReviewQualityCriteria", "reviewer", ["freshness", "operability"],
         f"Review the round-23 additions at the end of {LANE}/corpus/QUALITY.md (correction register, parser relaxations, live receipts): each criterion's fail condition must be stated correctly and be able to fail — run each named command against a revision where it should fail (git show b539cc1 / 4d95d2e for the validator) and the current one."),
    item("ReviewLessonGate", "reviewer", ["freshness", "operability"],
         f"Review {LANE}/corpus/lessons/round-23.md: claims, Gate admits/rejects, routed-defect table and Mistakes. Check every evidence pointer resolves (files, commits {CAND}, 4e7dd1d, 4d95d2e, 6847479), every number matches the receipts/counters, and that no dead or unrun check is credited."),
    item("ReviewRoutedR22", "reviewer", ["freshness"],
         f"Verify the round-22 routed dispositions: {LANE}/corpus/QUALITY.md §Correction register — round 23, {LANE}/.ufo/waves/round-22/postfix/REPRODUCE.md (run it), the misroot move to {LANE}/.ufo/waves/round-22/residual/misroot/ (byte-identity with `git show d5a0369:err.txt` / out.txt), and the w1 seat reviews of the four probe-only fixes. Report any disposition that is wrong or unproven."),
    item("ConnectR23Axes", "connector", ["freshness", "operability"],
         f"Cross-axis attack: C1 freshness corrections vs C2 live verdicts vs the property map — do any C1 corrections in {LANE}/SKILL.md's round-23 section contradict the C2 receipts in {R}/live/ (status, canonical, served/not-served), or each other across units? Are C1 and C2 causally separable as {LANE}/corpus/lessons/round-23.md claims? path:line evidence."),
    item("ReviewUpstreamFixes", "reviewer", ["operability"],
         f"From {R}/live/*/audit.json and the w1 Surface* reports in {R}/w1/, compile the domain findings (surfaces with canonical_missing, not-served mirrors, stale property-map rows) and attack each proposed upstream fix: is it correct for that host (GitHub Pages branch vs Actions, Kimi slot), is the expectedCanonical policy right, and which need an operator decision (L0)? Documented only; never apply."),
    item("ExecRealGeneratorPages", "executor", ["operability"],
         f"In /tmp only: generate real static pages with an actual site generator installable without pacman (e.g. `npx @11ty/eleventy` or `uvx` mkdocs build) using a minimal project that sets a canonical link, inline SVG icons and form inputs; run {LANE}/scripts/canonical_audit.py on the built HTML via a manifest; report generator name/version, exact output, and whether the result matches your pre-run expectation. Record any tool install (tool/version/channel/reason)."),
]

spec = {"wave": "kake-r23-w2", "context": CONTEXT, "reportDir": ".ufo/waves/round-23/w2", "maxLanes": 100,
        "axes": ["operability", "freshness"], "milestone": "r23-falsify", "items": items}
pathlib.Path(R, "w2-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
from collections import Counter
print(len(items), Counter(i["role"] for i in items))
