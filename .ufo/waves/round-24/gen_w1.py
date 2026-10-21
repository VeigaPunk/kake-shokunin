#!/usr/bin/env python3
"""Generate the round-24 wave-1 spec (w1-spec.json). Deterministic; run from anywhere."""
import json
import pathlib
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
R = f"{LANE}/.ufo/waves/round-24"
BASE = "f7de3ab4e9f030a15a857a5a08631bd8e690f436"
GS = "/skill:godspeed\n\n"  # the OMP task hook injects the godspeed directive bytes after this line

CONTEXT = f"""# Goal
Kake lane round 24 only (web properties and publishing; owned axes operability + freshness). Frozen claim contract {R}/contract.json (read it first). Base revision {BASE} (round 23, admitted).
- C1 freshness: reconcile all 19 paths-gate targets of `node {LANE}/scripts/freshness-sweep.mjs --section=paths` with the current filesystem (population {R}/c1-population.json; round-open JSON {R}/paths-before.json: 3 drift targets with 4 unannotated cites, 12 newMissing tokens not in pins.pathsMissSet, 4 recovered tokens because ~/Projects/ds4cc-marketplace reappeared on 2026-10-21 ~05:19 -03).
- C2 operability: the lane's receipt replay ({LANE}/.ufo/waves/round-23/measure_c1.py and measure_c2.py) must reject malformed receipts (exit 1 or 2, never a Python traceback) instead of accepting them; known gaps: lexical observedAt/fetchedAt prefix test (`x[:10] < "2026-10-21"`) accepts malformed or future strings; served() crashes on a non-string contentType. The fix lands as a maintained lane script {LANE}/scripts/receipt_replay.py (round-23 runners stay byte-intact as historical evidence).
The L1 (KakeR24) holds the planner seat and is the sole integration writer; you are author-side and never claim independent admission.
# Contract
- All paths absolute. Lane {LANE}. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Your tools start at the FLEET root /home/vgpnk/Projects/shokunin: NEVER write a relative path or redirect there; put every scratch file under a fresh `mktemp -d /tmp/kake-r24-<YourName>-XXXX`.
- Read-only on the lane: write ONLY your own report file. Never edit lane production files, never run git/jj mutations in the lane, never touch its index/jj state, the fleet repo, sibling lanes, ~/.omp config or .ufo/state. Anything that needs a git commit (sandboxes, mutation cases) runs in your own `git clone --no-hardlinks {LANE} /tmp/kake-r24-<YourName>-clone`; record the clone's observed HEAD. Writers (executors) work only in that clone and leave produced files there, listing absolute paths plus sha256 in the report; the L1 integrates.
- Domain source trees (~/Projects/ds4cc-marketplace, ~/Projects/ufo-fsd-alpha, ~/Projects/lucario, …) are read-only: stat/ls/git log/git show only, no fetch/pull/checkout. Web: read-only GET/HEAD of public documentation pages only.
- No builds/lint/formatters; targeted CLI probes, the named selftests and counters are allowed. Stay a leaf: spawn no subagents (executors may spawn one read-only labrat for one falsifiable hypothesis).
- Tooling: you and every seat may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard: ALL pacman transactions are PAUSED host-wide (no -S/-Sy/-Syu/-U/-R, no downgrade, no host service restart); use uv tool / npx / an official binary in ~/.local/bin, or skip. No live secrets.
- Report format: `## Verdict`, `## Findings` (severity P0–P3, exact command, exact observed output, impacted claim/axis, smallest fix), `## Checked and held`, `## Limits`. Quote exact outputs; an unrun check has not passed.
# C1 target receipt schema (C1 target items: include exactly one fenced ```json block with this object)
{{"id": "T##", "token": "<token from c1-population.json>", "class": "drift|newMissing|recovered", "observedAt": "<UTC RFC 3339 date-time of your observation, e.g. 2026-10-21T12:34:56Z>", "state": "absent|present", "observation": {{"commands": ["<exact read-only commands>"], "output": "<exact output, abbreviated faithfully>"}}, "event": "<dated event that explains the state, with its evidence, or 'unknown'>", "cites": [{{"cite": "<file:line from the population>", "lineText": "<exact current bytes of that line>", "authored": "lane|non-author", "status": "annotated-true|annotated-stale|unannotated|presence-claim-true|presence-claim-stale", "action": "none|append-inline|sidecar", "text": "<exact text to append at the END of that line, or the sidecar note>"}}]}}
Rules: non-author files are corpus/lessons/*aggregator*.md and *verifier-spotcheck*.md — never propose editing them; use action `sidecar`. Absence annotations follow the round-20 style and MUST contain an absence word matched by /absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing/i, the date 2026-10-21, the event, and the words "historical record, not an executable instruction". Restoration corrections (recovered targets) MUST contain NONE of those absence words (they sit within ±2 lines of other cites and would silently annotate them), must start with `*[r24 restoration 2026-10-21:` (or `<!-- r24 restoration 2026-10-21:` inside table rows / code), name what was observed present, and say which part of the earlier line stays historical/unverified. Never rewrite existing text; only append.
# C2 malformed-case schema (C2 gap items: include exactly one fenced ```json block: an array of case objects)
[{{"id": "<short-kebab-id>", "target": "c1|c2", "file": "<lane-relative path, e.g. .ufo/waves/round-23/receipts/drift-detection.json or .ufo/waves/round-23/live/ds4cc-primary/fetch.json>", "op": "set|delete", "jsonPath": ["observedAt"], "value": <JSON value for set>, "expect": "reject|accept", "why": "<one sentence; cite RFC section if it rests on one>", "r23Observed": {{"exit": <int>, "traceback": true|false, "stdoutTail": "<last line>"}}}}]
`r23Observed` is what the CURRENT round-23 runner actually did when you applied the case in your sandbox clone at {BASE}, committed it (fixed GIT_COMMITTER_DATE=2026-10-21T12:00:00Z), and ran `python3 {LANE}/.ufo/waves/round-23/measure_c1.py --root <clone> --revision <sandbox HEAD>` (or measure_c2.py). A case only counts when you actually ran it. `expect: accept` cases are controls that must stay accepted.
"""


def item(name, role, axes, prompt):
    assert len(name) <= 32, name
    return {"name": name, "role": role, "axes": axes, "prompt": GS + prompt}


def camel(s):
    return "".join(p[:1].upper() + p[1:] for p in s.replace("/", "-").replace(".", "-").replace("_", "-").split("-") if p)


items = []
pop = json.loads(pathlib.Path(R, "c1-population.json").read_text())["targets"]

# --- C1: one seat per target (recovered ds4cc-marketplace split in two by file family) ---
target_roles = {"drift": "scout", "newMissing": "reviewer", "recovered": "scout"}
for i, t in enumerate(pop):
    tok = t["token"]
    short = camel(tok.split("/")[-1] or tok)[:18]
    base = (f"C1 target {t['id']} `{tok}` (class {t['class']}). Observe its current state with read-only commands "
            f"(test -e, stat -c '%n %w %y', ls -la of the nearest existing ancestor; for a git repo `git -C <dir> log -3 --format='%H %cI %s'` and `git -C <dir> remote -v`). "
            f"Read every cite line in {LANE} (cites: {', '.join(t['cites'])}) with ±3 lines of context, classify each cite, and propose the exact append-only text. ")
    if t["class"] == "drift":
        base += (f"Unannotated cites to fix: {', '.join(t['unannotatedCites'])}. Explain why the existing r18/r20 annotations did not cover them "
                 f"(the gate reads the citing line ±2 after blanking citation text: {LANE}/scripts/freshness-sweep.mjs annotate()). Emit the C1 target receipt JSON.")
        role = "scout" if i % 2 == 0 else "revenger"
    elif t["class"] == "newMissing":
        base += ("This token is already annotated absent at its cite but was never pinned in pins.pathsMissSet. Establish whether it ever existed and when it vanished "
                 f"(lane history: `git -C {LANE} log -S'<token tail>' --format='%h %cI %s' -- <file>`; for kake-shokunin-local paths check `git -C {LANE} log --all --format=%h -- <relative path>`), "
                 "and whether the existing annotation text is truthful. Emit the C1 target receipt JSON (action none if the annotation is true).")
        role = "reviewer" if i % 2 == 0 else "revenger"
    else:
        base += ("This target exists again. For every cite decide whether the line (and its earlier r18/r20/r23 absence notes) now states something false about presence, "
                 "and draft the restoration correction (no absence words!). Also compare the restored tree with what the corpus cites (CNAME value, subdirs, HEAD) and say which presence-dependent claims stay unverified. Emit the C1 target receipt JSON.")
        role = "scout"
    if tok == "~/Projects/ds4cc-marketplace":
        skill = [c for c in t["cites"] if c.startswith("SKILL.md")]
        rest = [c for c in t["cites"] if not c.startswith("SKILL.md")]
        for part, cites in (("Skill", skill), ("Corpus", rest)):
            p = base.replace(", ".join(t["cites"]), ", ".join(cites))
            items.append(item(f"PathsRestoredDs4cc{part}", "scout", ["freshness"], p + f" Only these cites: {', '.join(cites)} (a sibling seat covers the others)."))
        continue
    prefix = {"drift": "PathsDrift", "newMissing": "PathsNew", "recovered": "PathsRestored"}[t["class"]]
    items.append(item(f"{prefix}{t['id']}{short}"[:32], role, ["freshness"], base))

items += [
    item("RevengeDs4ccRestoration", "revenger", ["freshness"],
         "Reconstruct the 2026-10-21 reappearance of ~/Projects/ds4cc-marketplace (read-only): stat birth/modify times of the dir, .git, CNAME, burnerchrome/, speedrun/; `git -C ~/Projects/ds4cc-marketplace log --format='%H %cI %an %s' -15`, `git -C ... reflog -10`, `remote -v`, branch tracking state. Is it the same repository the corpus cited before the 2026-10-12 prune (compare commit hashes or remotes cited in "
         f"{LANE}/SKILL.md, {LANE}/corpus/knowledge/fleet-registry.md, origin-repos.md, publish-channels.md)? Search /home/vgpnk/Projects/shokunin/.ufo/reports/round-2*/*.md and /home/vgpnk/Projects/shokunin/.ufo/watchdog.log read-only for any lane or operator note about the restoration. Give the most precise dated event sentence the evidence supports."),
    item("R23ReceiptsDs4ccStale", "reviewer", ["freshness"],
         f"Find every round-23 C1 claim and every '## Live re-verification — round 23' correction in {LANE}/corpus/knowledge/*.md and {LANE}/SKILL.md that asserts ~/Projects/ds4cc-marketplace (or CNAME/burnerchrome/speedrun under it) is absent (receipts under {LANE}/.ufo/waves/round-23/receipts/*.json; grep the unit files). For each, observe the current state and propose an appended round-24 correction (exact text; never rewrite the r23 observation). List file:line, the r23 claim id, and your observation."),
    item("GlobsWebzitesState", "scout", ["freshness"],
         "The paths gate cannot check glob tokens. Expand each now and report matches: ~/Projects/webzites/state/rebuild-*.json, ~/Projects/webzites/state/recreate-*.json, ~/Projects/webzites/state/recreate-plazir15-*.json, ~/Projects/webzites/state/update-*.json, ~/Projects/webzites/reports/keepers/grokbot-*.log.md (use `compgen -G` or python glob). "
         f"Find their cite lines in {LANE} (grep -n) and say whether each cite carries an absence annotation; propose an annotation for any that lacks one."),
    item("GlobsSystemdUfofsdbeta", "scout", ["freshness"],
         "Expand the two remaining glob tokens now: ~/.config/systemd/user/webzites-*.timer and ~/Projects/**/ufofsdbeta-kimi-review (python glob with recursive=True; bounded to ~/Projects depth 4). "
         f"Report matches, also `systemctl --user list-timers --all | grep -i webzites` (read-only), cite lines in {LANE}, annotation status, and any proposed annotation."),
    item("ProjectsChildrenDelta", "scout", ["freshness"],
         f"pins.projectsChildrenSet in {LANE}/corpus/knowledge/freshness-pins.json lists 14 ~/Projects children (informational). List ~/Projects now; for each added/removed child give birth time and whether any file in {LANE} cites it (grep -rn). Recommend whether the informational pin should be re-censused this round, with the exact new JSON array."),
    item("CritRepinGreenwash", "critic", ["freshness"],
         f"Attack C1 before it lands: is re-pinning 12 newMissing tokens into pins.pathsMissSet (and dropping 4 recovered ones) a reconciliation or greenwashing? Read {R}/contract.json, {LANE}/corpus/knowledge/freshness-sweep.md, the round-18 re-census precedent in {LANE}/SCORECARD.md move log and {LANE}/corpus/lessons/round-18.md, and the r23 closure note in /home/vgpnk/Projects/shokunin/MANIFEST.json rounds[394].verification and notes (read-only). Give the exact evidence conditions under which a re-pin is legitimate and the falsifier the counter must enforce."),
    item("ConnectDs4ccSiblingOverlap", "connector", ["freshness"],
         "Sibling-overlap scan (read-only): which other shokunin lanes under /home/vgpnk/Projects/shokunin/*-shokunin cite ~/Projects/ds4cc-marketplace or ds4cc.com, and do any of their current rounds record its 2026-10-21 restoration or depend on its absence? grep -rln, path:line evidence; say whether kake's reconciliation conflicts with any sibling claim."),
    item("ExecSweepSidecar", "executor", ["freshness"],
         f"In your clone of {LANE} at {BASE}: add a lane-authored sidecar to {LANE}/scripts/freshness-sweep.mjs so citations inside NON-author files (corpus/lessons/*aggregator*.md, *verifier-spotcheck*.md — reuse the predicate in {LANE}/scripts/corpus-contract.mjs if one exists) can be annotated without editing them. File corpus/knowledge/freshness-sidecar.json, schema `kake-paths-sidecar-v1`: entries {{file, line, token, lineSha256 (sha256 of the exact line text without newline), kind: absent|restored, date, note}}. An `absent` entry annotates (file:line, token) only if: file is non-author, the token occurs on that line, the line's sha256 still matches, and note matches the absence regex; a `restored` entry is informational. Malformed sidecar or an entry for a lane-authored file → exit 2 (fail closed). Keep the existing selftest green and add selftest cases proving each rule can fail (stale sha, lane-authored file, wrong token, missing absence word, malformed JSON). Report: unified diff, new sha256s, `node scripts/freshness-sweep.mjs --selftest` output in the clone, and a paths run in the clone with a sidecar entry for corpus/lessons/round-6-aggregator-audit.md:48 (`~/Projects/webzites/scripts/kimi-surface.mjs`)."),
    item("ExecPathsCounter", "executor", ["freshness"],
         f"In your clone of {LANE} at {BASE}: write .ufo/waves/round-24/measure_c1.py (stdlib only). Usage `python3 .ufo/waves/round-24/measure_c1.py --root LANE --revision REV [--json]`. Validate REV (no leading '-', `git rev-parse --verify --end-of-options REV^{{commit}}`). Read .ufo/waves/round-24/c1-population.json at REV and require its sha256 == the digest at {BASE}-era file {R}/c1-population.json (hardcode it). `git archive REV | tar -x` into a temp dir; run that tree's `node scripts/freshness-sweep.mjs --section=paths --json` with KAKE_REPO_ROOT=<tmp> and KAKE_FRESHNESS_PINS unset; record its exit. A target passes iff: (a) .ufo/waves/round-24/c1-receipts/<id>.json at REV is a JSON object whose id/token/class match the population, observedAt is a strict RFC 3339 date-time >= 2026-10-21T00:00:00Z and <= REV's committer time, state is absent for drift/newMissing and present for recovered, observation.commands and observation.output non-empty; (b) the live filesystem now agrees with state (os.path.exists(os.path.expanduser(token))); (c) the sweep JSON lists the token in none of drift, setDelta.newMissing, setDelta.recovered; (d) drift: every unannotatedCite is fixed either inline (in a lane-authored file a line exists at REV that starts with the base line text and contains '2026-10-21' and an absence word) or by a sidecar entry in corpus/knowledge/freshness-sidecar.json at REV for that file/line/token; (e) recovered: every lane-authored cite's base line text is followed (same line) by a '[r24 restoration 2026-10-21:' or '<!-- r24 restoration 2026-10-21:' marker at REV, and every non-author cite has a `restored` sidecar entry. Print per-target verdicts and `accepted N/19 · sweep exit E`; exit 0 iff 19/19 and sweep exit 0, 1 otherwise, 2 for unreadable inputs. Also write .ufo/waves/round-24/c1_selftest.py exercising pass and each failure clause on a throwaway git repo. Report file paths in the clone, sha256s, and a run at {BASE} (expected 0/19, exit 1)."),
]

# --- C2: tooling ---
items += [
    item("ExecReceiptReplay", "executor", ["operability"],
         f"In your clone of {LANE} at {BASE}: write scripts/receipt_replay.py (stdlib only) — the maintained replay of the round-23 receipt sets. `python3 scripts/receipt_replay.py c1|c2 --root LANE --revision REV [--json]` and `--selftest`. Port the exact acceptance semantics of {LANE}/.ufo/waves/round-23/measure_c1.py and measure_c2.py (same populations and digests, BASE, heading, ROUND paths, validator re-run) and harden: (1) revision must not start with '-' and must resolve via `git rev-parse --verify --end-of-options REV^{{commit}}` else exit 2; (2) observedAt/fetchedAt must be strings matching RFC 3339 §5.6 full-date or date-time (strict regex + real calendar/clock values via datetime; reject trailing garbage, missing offset on date-time, hour 24, month 13), on/after 2026-10-21 and not later than REV's committer timestamp; (3) contentType must be a string parsed as an RFC 9110 §8.3.1 media type (token '/' token, optional ';' parameters) — non-string or unparsable → not served, recorded as a problem, never a crash; (4) status must be an int but not bool; (5) every JSON field read is type-checked so any malformed receipt yields exit 1 with a named problem, unreadable revision/population exit 2, and no traceback for any JSON input; (6) --json output of per-unit problems and verdict tallies. At {BASE} it must print accepted 17/17 (c1, HOLD79/STALE55/UNVERIFIABLE42) and 12/12 (c2, clean3/failed-policy5/not-served4) — run both and paste outputs, plus --selftest. Report paths in the clone and sha256s."),
    item("ExecMalformedMatrix", "executor", ["operability"],
         f"In your clone of {LANE} at {BASE}: write .ufo/waves/round-24/measure_c2.py (stdlib only), the C2 counting command. Usage `python3 .ufo/waves/round-24/measure_c2.py --root LANE --revision REV [--json]`. It reads .ufo/waves/round-24/c2-population.json at REV ({{\"fixtureBase\": \"{BASE}\", \"cases\": [<C2 malformed-case schema objects>]}}; hardcode a POPULATION_SHA256 placeholder constant the L1 fills when freezing) and selects the runner under test from REV: if scripts/receipt_replay.py exists at REV run `python3 <tmp>/receipt_replay.py c1|c2 --root SANDBOX --revision H`; otherwise the round-23 runners `.ufo/waves/round-23/measure_c1.py|measure_c2.py` read at REV. Sandbox: `git clone --quiet --no-hardlinks LANE <tmp>/sb`, checkout fixtureBase detached; per case reset hard to fixtureBase, apply the JSON mutation (set/delete at jsonPath; for set write json.dumps with the same indent the file uses), commit with fixed GIT_AUTHOR/COMMITTER_DATE=2026-10-21T12:00:00Z and a fixed identity, run the runner with a timeout, classify: expect reject → correct iff exit in {{1,2}} and 'Traceback' not in stderr; expect accept → correct iff exit 0. Print one line per case and `correct N/M (reject R/Rt, accept A/At)`; exit 0 iff all correct, 1 otherwise, 2 for unreadable inputs. Never touch LANE except `git clone` reads. Build a provisional c2-population.json with at least 6 cases (observedAt '2026-10-21garbage', fetchedAt '2099-01-01T00:00:00Z', contentType 200 on ds4cc-primary, contentType ['text/html'], one unmodified c1 control, one unmodified c2 control) and paste the run against the round-23 runners at {BASE}. Report paths in the clone and sha256s."),
    item("SentinelRevisionInjection", "sentinel", ["operability"],
         f"Security review: {LANE}/.ufo/waves/round-23/measure_c1.py and measure_c2.py pass `f\"{{revision}}:{{path}}\"` to `git show`. In a sandbox clone (never the lane) test whether a revision such as `--output=/tmp/kake-r24-<you>-pwn` or other option-shaped strings make git write files or read outside the repo; also check subprocess/tempdir handling in measure_c2.py's validator re-run. Report exact commands/outputs and the minimal guard for scripts/receipt_replay.py."),
    item("SentinelMatrixSandbox", "sentinel", ["operability"],
         f"Security/safety review of the planned C2 matrix design (context above): cloning the lane into /tmp and committing mutated receipts there. Enumerate every way it could touch the real lane ({LANE}) — shared object dirs, hooks, git config inheritance (core.hooksPath, includeIf), jj colocated state, alternates, env vars (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE) — and verify the safest invocation empirically in a throwaway clone. Give the exact env/flags the matrix must use."),
]

gaps = [
    ("GapC1ObservedAt", "executor", "c1", "observedAt: malformed strings with a valid prefix ('2026-10-21garbage', '2026-10-21T25:00:00Z', '2026-10-21T12:00:00' without offset), impossible dates ('2026-02-30', '2026-13-01'), far-future ('2099-12-31'), near-future relative to the commit time ('2026-10-21T23:59:59Z' with committer date 12:00Z), non-ASCII digits, and the valid date-only control"),
    ("GapC1UnitPath", "reviewer", "c1", "unit/path identity: wrong unit, path with '../', path as list, unit missing, extra trailing whitespace"),
    ("GapC1ClaimsShape", "reviewer", "c1", "claims container: claims as dict, as string, empty list, list of non-objects (int, null, string), claims missing"),
    ("GapC1ClaimFieldTypes", "executor", "c1", "claim field types: id/anchor/claim/surface/method/observation as int, list, null, empty string, whitespace-only; does any type make the runner crash or accept"),
    ("GapC1VerdictSet", "mutation-tester", "c1", "verdict: lowercase 'hold', 'STALE ' with space, list ['HOLD'], STALE without correction, UNVERIFIABLE with empty reason, correction as int"),
    ("GapC1AnchorBase", "reviewer", "c1", "anchors: empty anchor '' (substring of everything), single-character anchor, anchor present only in the measured revision not the base, anchor as int"),
    ("GapC1HeadingIds", "mutation-tester", "c1", "the unit file heading/claim-id checks: duplicate claim ids, id containing ']' or newline, ids that collide as substrings ('c1' vs 'c11'), heading present but ids before it"),
    ("GapC1PopulationEdge", "mutation-tester", "c1", "the receipt file itself: invalid JSON, JSON array instead of object, UTF-8 BOM, NaN/Infinity tokens, duplicate keys (last-wins hiding a bad value), extremely large integers"),
    ("GapC2FetchedAt", "executor", "c2", "fetchedAt: same malformed/future/impossible/offset-less set as observedAt, plus non-string types, on a served and a not-served surface"),
    ("GapC2ContentType", "executor", "c2", "contentType: int 200, list, dict, true, false, null, '' , 'TEXT/HTML; charset=utf-8', 'text/html;', 'text/htmlx', ' text/html', 'text/html, text/plain' — RFC 9110 §8.3 media-type grammar decides each"),
    ("GapC2Status", "mutation-tester", "c2", "status: true (bool is an int in Python), 200.0, '200', 199/300 boundaries, 204 with a page, negative"),
    ("GapC2ErrorTruncated", "mutation-tester", "c2", "error/truncated flags: error '' vs null, error 0, truncated 'false' (string, truthy), truncated 0/1, missing keys"),
    ("GapC2UrlMethod", "reviewer", "c2", "url/method: method 'get', 'HEAD', url with trailing slash difference, url as list, finalUrl missing/int, redirects as dict"),
    ("GapC2ShaPage", "executor", "c2", "sha256/page binding: uppercase hex sha, sha of a different page, page.html present for a not-served surface, sha256 as int"),
    ("GapC2AuditReplay", "mutation-tester", "c2", "audit.json: verdict mismatch, exit field as string, extra keys, result missing, audit for not-served with wrong status"),
    ("GapC2NotServedShape", "reviewer", "c2", "not-served path: audit verdict 'not-served' on a served 200 text/html fetch, status 404 with contentType text/html, not-served with page.html stored"),
    ("GapC2FinalUrlManifest", "reviewer", "c2", "manifest re-run inputs: finalUrl with control characters, javascript: scheme, very long URL, non-ASCII host; does the validator re-run crash the counter"),
]
for name, role, tgt, focus in gaps:
    items.append(item(name, role, ["operability"],
        f"C2 gap audit, {tgt} side, focus: {focus}. For each case: apply it in your sandbox clone at {BASE} to a committed round-23 receipt ({'.ufo/waves/round-23/receipts/<unit>.json' if tgt == 'c1' else '.ufo/waves/round-23/live/<id>/fetch.json (and audit.json/page.html where relevant)'}), commit, run the round-23 runner, and record what it did. Decide expect reject/accept from the runner's documented contract and the RFCs (RFC 3339 §5.6, RFC 9110 §8.3.1, RFC 8259). Emit the C2 malformed-case JSON array (only cases you ran; 4-12 cases)."))

# --- C2 + frontier: sources ---
items += [
    item("SourceRFC3339", "scout", ["operability"],
         "Open RFC 3339 (https://www.rfc-editor.org/rfc/rfc3339.txt). Return URL, access date, sha256 of the plain-text bytes you fetched, and located ≤25-word quotes for: §5.6 full-date/full-time/date-time ABNF (time-offset required in date-time), §5.7 restrictions (date-mday by month/year; leap second), and whether a date-only string is an RFC 3339 'date-time'. Judge what a receipt validator must accept/reject."),
    item("SourceRFC9110MediaType", "scout", ["operability"],
         "Open RFC 9110 (https://www.rfc-editor.org/rfc/rfc9110.txt). Return URL, access date, sha256 of the bytes, and located ≤25-word quotes for §8.3 Content-Type, §8.3.1 media-type ABNF (type/subtype case-insensitive; parameters), and §5.6.2 token / §5.6.6 parameters (OWS around ';'). Judge how 'TEXT/HTML ; charset=utf-8', 'text/html;', ' text/html' and 'text/html, text/plain' parse."),
    item("SourcePythonDatetime", "scout", ["operability"],
         "Open https://docs.python.org/3/library/datetime.html (datetime.fromisoformat and date.fromisoformat). Return URL, access date, version shown, and located ≤25-word quotes on which ISO 8601 forms fromisoformat accepts in Python 3.11+ (e.g. basic format, week dates, 'T' optional?). Then run python3 -c checks on '20261021', '2026-W43-3', '2026-10-21T12:00', '2026-10-21 12:00:00+00:00' and state whether fromisoformat alone is a sufficient RFC 3339 validator (python3 --version)."),
    item("SourceRFC8259Json", "scout", ["operability"],
         "Open RFC 8259 (https://www.rfc-editor.org/rfc/rfc8259.txt). Return URL, access date, sha256, and located ≤25-word quotes on duplicate object names (§4 'SHOULD be unique', behaviour unpredictable), and numbers/literals (§3, §6: true/false are not numbers; NaN/Infinity not permitted). Then test python3 json.loads on duplicate keys, NaN and Infinity, and say what a receipt replay must do about them."),
]

# --- mutation, critics, simplifier, connectors ---
items += [
    item("MutateR23CounterSelftest", "mutation-tester", ["operability"],
         f"Mutation-test the timestamp and served() guards of {LANE}/.ufo/waves/round-23/measure_c1.py / measure_c2.py against {LANE}/.ufo/waves/round-23/counter_selftest.py in a sandbox copy: e.g. drop the `[:10]` slice, flip `<` to `<=`, remove the isinstance checks, remove the text/html compare. Which mutants survive? These survivors define what the new receipt_replay.py selftest must kill. Exact commands/outputs."),
    item("MutateSweepAnnotate", "mutation-tester", ["freshness"],
         f"Mutation-test {LANE}/scripts/freshness-sweep.mjs annotate()/set-delta logic (lines ~300-490) against its --selftest in a sandbox copy: window ±2 → ±1/±3, ABSENT_RE word removal, newMissing filter inversion, recovered list ignored. Which mutants survive the selftest? Report survivors the round-24 sidecar/selftest work should kill."),
    item("CritC2Separability", "critic", ["operability", "freshness"],
         f"Attack the round's claim structure ({R}/contract.json): are C1 (paths reconciliation) and C2 (receipt replay hardening) causally separable and on distinct axes; could either counter pass because of the other's landing; does C2's 'before' (round-23 runners as the lane's replay instrument) make a fair baseline, or is it a strawman? Propose falsifiers."),
    item("CritAxisHarm", "critic", ["operability", "freshness"],
         f"Pre-mortem for axis harm: list every existing lane gate the round-24 changes could break (scripts/corpus-contract.mjs --json, scripts/freshness-sweep.mjs --selftest and sections paths/history/armed, scripts/canonical_audit.py --selftest, .ufo/waves/round-23/measure_c1.py/measure_c2.py at the base, .ufo/waves/round-22/matrix.py) and run each NOW at {BASE} in a sandbox clone to record the baseline exits/counts the L1 must compare after landing. Paste exact commands and outputs."),
    item("CritLowestAxisRule", "critic", ["operability", "freshness"],
         f"Check the round against /home/vgpnk/Projects/shokunin/AXES.md and the lane's {LANE}/SCORECARD.md (saturation, stagnation window, capabilities table): does the lowest-axis duty apply, are both claims on the tied-lowest axes, does a capability row need updating for scripts/receipt_replay.py, and is any claim secretly exploratory? Cite lines."),
    item("SimplifyReplayPort", "simplifier", ["operability"],
         f"Read {LANE}/.ufo/waves/round-23/measure_c1.py, measure_c2.py and counter_selftest.py. Propose the smallest faithful port into one maintained scripts/receipt_replay.py: which helpers merge, what must stay byte-for-byte semantic, what is dead weight. Output a concrete outline (functions, signatures) the L1 can compare with the executor's draft; no files written."),
    item("ConnectSiblingTimestampGuards", "scout", ["operability"],
         "Read-only scan of sibling lanes /home/vgpnk/Projects/shokunin/*-shokunin/scripts and their .ufo/waves/round-2*/ counters for timestamp parsing (fromisoformat, strptime, [:10] comparisons) and Content-Type handling. Is the lexical-prefix pattern shared elsewhere (fleet-wide mistake class) or kake-only? path:line evidence; do not edit."),
    item("ConnectProvinceBoundary", "scout", ["operability", "freshness"],
         f"Read {LANE}/PROVINCE.md and the PROVINCE.md of tabi-shokunin, kagi-shokunin and chousa-shokunin (read-only, under /home/vgpnk/Projects/shokunin). Does reconciling ds4cc-marketplace presence or hardening receipt parsing bleed into a sibling province (rendering, credentials, research method)? path:line evidence."),
    item("ConnectFrontierRows", "scout", ["operability", "freshness"],
         f"Read {LANE}/corpus/README.md (## Frontier), {LANE}/PROVINCE.md frontier and {LANE}/SCORECARD.md planned rows. Which frontier row does each round-24 claim advance, and what new frontier ground does the ds4cc restoration open (e.g. re-verifying ds4cc presence-dependent claims, CNAME vs served ds4cc.com)? Propose exact appended rows."),
]

# --- scribes, frontier mining, quality ---
items += [
    item("ScribeSourcesRows", "scribe", ["operability"],
         f"Draft (in your report only) SOURCES.md rows S032+ for RFC 3339 (date-time), RFC 9110 media type (scope distinct from S010/S028) and RFC 8259 (JSON) in the exact column order of {LANE}/corpus/SOURCES.md, tier A spec, status mined, opened 2026-10-21, recheck 365d, used-by `scripts/receipt_replay.py` / `corpus/knowledge/static-canonical-preflight.md`; leave quote/locator cells as <FROM-SOURCE-SEAT>. Read /home/vgpnk/Projects/shokunin/CORPUS.md section 'SOURCES.md — where a shokunin learns' first and follow it."),
    item("ScribeLessonDraft", "scribe", ["operability", "freshness"],
         f"Draft (in your report only) {LANE}/corpus/lessons/round-24.md sections '## Claims', '## Gate' (sources opened this round with <URL/date/quote> placeholders), '## Mistakes' (class · evidence pointer · captured-by · fix), '## Measurement' from {R}/contract.json, following the structure of {LANE}/corpus/lessons/round-23.md; numbers as <TBD>."),
    item("ScribeKnowledgeReplay", "scribe", ["operability"],
         f"Draft (in your report only) an appended section '## Receipt replay hardening — round 24' for {LANE}/corpus/knowledge/static-canonical-preflight.md: why lexical timestamp prefixes and untyped contentType are unsafe, the RFC 3339/RFC 9110 rules applied (S### placeholders), the CLI `python3 scripts/receipt_replay.py c1|c2 --root . --revision <commit>` and its exit contract, and its limits (structure is not authentication of the network event)."),
    item("ScribeFreshnessKnowledge", "scribe", ["freshness"],
         f"Draft (in your report only) an appended section '## Round-24 reconciliation and sidecar' for {LANE}/corpus/knowledge/freshness-sweep.md: the 2026-10-21 ds4cc-marketplace reappearance (stale pinned misses), the re-pin rule (only targets observed this round with a receipt), restoration corrections without absence words (±2 window side effect), and the non-author sidecar (schema kake-paths-sidecar-v1, line sha256 binding)."),
    item("ScribeQualityCriterion", "scribe", ["operability", "freshness"],
         f"Draft (in your report only) two appended QUALITY criteria for {LANE}/corpus/QUALITY.md following its existing criterion shape: (1) receipt timestamps are parsed against a named grammar and bounded by the commit time, never prefix-compared; (2) an absence pin is re-armed when its target reappears (recovered tokens leave pathsMissSet) and restoration notes carry no absence vocabulary. Each needs a 'Fails if' predicate that a named probe can make fail."),
    item("ScribeLogScorecard", "scribe", ["operability", "freshness"],
         f"Draft (in your report only) the round-24 LOG.md entry (style of the last entries in {LANE}/LOG.md) and the SCORECARD.md '## Round 24' section with a claims table (axis/score delta, before→after, counting command, verdict/evidence) plus a '### Planned — supersedes round-23 plan' paragraph; numbers <TBD>."),
    item("ScoutMistakeSweep", "scout", ["operability", "freshness"],
         f"Mistake mining: read the kake closure entries for rounds 20-23 in /home/vgpnk/Projects/shokunin/MANIFEST.json (read-only; python json filter type=='closure' and lane=='kake'), {LANE}/corpus/lessons/round-2*-verifier-spotcheck.md and {LANE}/corpus/lessons/round-23.md '## Mistakes'. List every routed defect or disagreement, whether a later lesson/QUALITY criterion addressed it (file:line), and which remain open. Pick the single best unmined mistake for round 24 with class · evidence · captured-by · fix."),
    item("ReviewQualityCriteria", "reviewer", ["operability", "freshness"],
         f"Read {LANE}/corpus/QUALITY.md in full. Which criterion should have caught the round-23 lexical observedAt test and the non-string contentType crash before admission? If none, say so (captured-by: none). Check every 'Fails if' predicate for an inverted or unfalsifiable condition (the round-22 verifier found one). Cite lines."),
    item("ReviewSkillPathsRecipes", "reviewer", ["freshness"],
         f"Read {LANE}/SKILL.md sections that tell an agent to run the paths gate or re-pin (grep -n 'pathsMissSet\\|re-census\\|--section=paths'). Are the instructions executable today and do they say how to treat a recovered (reappeared) target? Propose exact append-only SKILL.md text (≤12 lines) for the recovered-target workflow."),
]

spec = {"wave": "kake-r24-w1", "context": CONTEXT, "reportDir": ".ufo/waves/round-24/w1", "maxLanes": 100,
        "axes": ["operability", "freshness"], "milestone": "r24-build", "items": items}
pathlib.Path(R, "w1-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
names = [i["name"] for i in items]
assert len(names) == len(set(names)), [n for n, c in Counter(names).items() if c > 1]
print(len(items), Counter(i["role"] for i in items))
