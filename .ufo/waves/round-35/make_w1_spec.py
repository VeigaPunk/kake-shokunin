#!/usr/bin/env python3
"""Write the round-35 wave-1 spec (w1-spec.json) next to this file."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV = "318561efa67206699fdaf259ffb86e39f2d916a8"
SB = "/fast/scratch/hyaku/kake-r35/w1"
DIRECTIVE = Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + DIRECTIVE.rstrip("\n") + "\n\n"

CONTEXT = f"""# Goal
Kake round 35, wave 1 (build + first falsifiers). The L1 (KakeR35) holds the planner and integration seat; you are one leaf seat. Lane repo: {L}. Lane axes: operability and freshness (web properties and publishing). Round 34 was rejected because a do-nothing control met each declared counter; this round seals its test inputs so no control can reach the targets. Each item names what it builds or attacks; attacks try to show work is wrong, overstated or harmful, with reproducible evidence. Time box: finish and write your report within 25 minutes; a partial report beats none.

# Declared claims (SCORECARD.md section "Round 35 — declared claims", landed at 81d9fd74f1460ba8cff007fc42f8fb8265aa2d4d; controls landed at {REV}; base 16a6b8b8144f4d6e6187e9ecbb4fb5f4528b911a)
- C1 (operability, capability repair): `scripts/link_preview_audit.py` meets the public round-35 contract (SCORECARD "C1 contract" bullets a, b, c: `og_url_multiple`; metadata inside template/svg/math does not count; an unreadable page no longer stops the other pages) on 24 sealed cases. Counter `python3 -B {L}/.ufo/waves/round-35/sealed_count.py c1 --root <repo> --revision <commit> --key-revision <reveal commit>`. Before 14/24 at base; target passed >= 22 of 24.
- C2 (freshness, sourced learning claim on new ground): `corpus/knowledge/security-txt-publishing.md` (not yet written), how a publisher serves a valid security.txt (RFC 9116) from a GitHub Pages site, grounded in rows opened this round (S078-S085). Counter `... sealed_count.py c2 ...`: entry present, <= 1500 words, copiedShare <= 0.25 against the retained texts, >= 3 good cites of S078-S099, >= 9 of 12 sealed probes. Before met false.
- Controls already scored with the frozen counter (SCORECARD "Round 35 — controls scored before any build"; receipts {L}/.ufo/waves/round-35/verification/control-*.json; bundles {L}/.ufo/waves/round-35/retained/r35-control-*.bundle, prerequisite 81d9fd74): C1 base 14, lookup dcef39b5 7, constant clean 7; C2 junk 0 probes, keyword 3, RFC transcription 8 probes with copiedShare 0.9951. None meets its target.

# Sealed keys — binding
The C1 cases and C2 probes are sealed under /fast/scratch/hyaku/kake-r35/sealed/. Never read, list, stat, copy, grep or open anything under that directory, and never ask for its content. A seat that touches it by mistake says so in the first line of its report. Attack the design from the public counter code and contract only. If you build a control commit you want scored, bundle it (prerequisite {REV}) in your sandbox and name the bundle path; the L1 scores it.

# Landed state and inputs
- Lane branch master: {REV}. Work from your own clone at that revision unless your item names another; never read the lane working tree as evidence of landed state (the L1 integrates while this wave runs).
- Retained round-35 sources (opened 2026-10-22T22:00-22:02Z by {L}/.ufo/waves/round-35/fetch_sources.py): {L}/.ufo/waves/round-35/sources/ S078.txt (RFC 9116 security.txt), S079.txt (securitytxt.org), S080.txt (Jekyll configuration options), S081.txt (Wikipedia security.txt, a rejection candidate: secondary), S082.txt (RFC 8615 well-known URIs), S083.txt (IANA well-known URIs registry), S084.txt (https://github.com/.well-known/security.txt), S085.txt (https://www.google.com/.well-known/security.txt), S006.txt (re-open of existing row S006, GitHub Docs About GitHub Pages and Jekyll), with SXXX.html.gz bodies and receipts.json.
- Registry {L}/corpus/SOURCES.md (rows S001-S077; contract in /home/vgpnk/Projects/shokunin/CORPUS.md section "SOURCES.md — where a shokunin learns"). Existing rows S001/S002 cover actions/upload-pages-artifact hidden-file handling; S006 covers Jekyll's default exclusion of paths starting with `_`, `.` or `#`.
- Round-34 closure with routed defects: {L}/corpus/lessons/round-34-verifier-spotcheck.md; round-34 lesson {L}/corpus/lessons/round-34.md; round-34 retained controls {L}/.ufo/waves/round-34/retained/r34-c1-lookup-dcef39b5.bundle and r34-c2-hollow-0cce15f0.bundle (fetch with `git fetch <bundle> 'refs/heads/*:refs/heads/r34/*'` in your clone).
- Holds (ended items; never retry, reroute or rephrase): KakeR31.CriticC1Counter and KakeR31.CriticSandboxThreatModel. No item here asks whether a counter or selftest may trust runner-reported failure names, reason text or codes, and none models sandbox threats; if your item drifts there, stop that line and say so. If your own seat hits a provider safety or policy refusal or an automatic model switch, stop and write a one-line report saying so; do not rephrase.

# Bounds
- You are a leaf: no subagents, no swarm, no second judge, no admission or verdict on the round. Executors may spawn at most one read-only labrat probe.
- Never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, the lane jj state, the lane Git index or any tracked lane file. Never run git add/commit/stash/checkout/reset/pull/push or any mutating jj command in {L}; seats never push, commit or update refs in the lane. Never run any jj command at /home/vgpnk/Projects/shokunin; in the lane, read-only jj only with --ignore-working-copy.
- Code that writes files or Git state runs only in your own sandbox: {SB}/<YourName>/ (clone with `git clone -q {L} {SB}/<YourName>/clone` when you need one, then `git -C <clone> checkout -q <rev>`; export TMPDIR={SB}/<YourName>/tmp after creating it; never /tmp or /dev/shm). Unset GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE before any git command in a sandbox. Cap test runs: no unbounded recursive test runs; use `timeout` and at most 4 parallel processes. Deliverable files (code, patches, drafts, receipts) stay in your sandbox; name their absolute paths in your report.
- Owned sites: no live requests of any kind to the operator's owned web properties (ds4cc.com, app.ds4cc.com, *.onrender.com hosts of the operator, *.kimi.page, *.kimi.pro, veigapunk.github.io and any host pinned in {L}/corpus/knowledge/freshness-pins.json). ~/Projects/ds4cc-marketplace is a read-only local checkout: read it with git show/cat-file only; never fetch into it.
- Network: only seats told to open a named public URL may fetch, GET only (github.com reads of the public ds4cc-marketplace repository are allowed for every seat). Open sources by ordinary means only; never use a headless browser or any tool to pass a bot challenge, captcha or access control; a page you cannot open that way is recorded as unopened.
- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Your report is the only file you write in the lane.
- Tooling (operator, 2026-10-19): you and every seat may install or update tools that help the task without asking; read /home/vgpnk/.omp/agent/RULES.md first, use official channels, and record tool, version, channel and reason in your report. All pacman transactions are PAUSED host-wide: no pacman, no -Sy/-Syu/-U/-R, no downgrade, no service restart; use uv tool, npx or an official binary in ~/.local/bin.
- The only message target is agent://KakeR35 (the L1), for blockers only. Never message agent://all. Write plain English with no run-together words or private jargon.

# Result
Report under 80 lines: what you attacked or built, the exact commands you ran with exit codes, observed outputs, and evidence pointers (path:line, hash). An unrun check has not passed; say what you did not verify. If you stop before finishing, the first line of your report must be `PARTIAL:` with what is missing. Your findings are advisory input for the L1 and the non-author closure.
"""


def item(name, role, axes, target, change, acceptance):
    sb = f"{SB}/{name}"
    body = (f"# Target\n{target.format(sb=sb, L=L, REV=REV)}\n# Change\n{change.format(sb=sb, L=L, REV=REV)}\n"
            f"# Acceptance\n{acceptance.format(sb=sb, L=L, REV=REV)}\n")
    return {"name": name, "role": role, "axes": axes, "prompt": LEAD + body}


OP, FR = ["operability"], ["freshness"]
BOTH = ["operability", "freshness"]
ITEMS = [
    # ---- C1 build
    item("ExecToolRepair", "executor", OP,
         "Repair C1's tool `scripts/link_preview_audit.py` to the round-35 contract in your clone {sb}/clone at {REV}. You are the only seat writing the landed tool.",
         "- Read SCORECARD.md section \"Round 35 — declared claims\", bullets (a), (b), (c) of \"C1 contract\", and implement exactly those. Keep every other round-34 rule, reason name, verdict and exit code.\n- (a) `og_url_multiple` finding (property og:url, id `<page>:og_url_multiple:og:url`) when a page has more than one non-empty og:url element. (b) meta/link start tags inside an open template, svg or math element do not count; matching end tags close; nesting counted; a self-closed svg opens nothing. (c) unreadable pages give `page_unreadable` and the readable pages are still audited; their policy findings are listed beside the input findings; verdict could-not-evaluate, exit 2, pagesChecked = readable pages. Manifest-level faults unchanged.\n- Update the docstring (the 'does NOT check' bullets that the repair makes false) and cite the contract as lane policy where no source states it.\n- Update `scripts/link_preview_selftest.py` fixtures under `scripts/fixtures/link-preview/`: the fixture `input_policy_suppressed_on_input` encodes the old rule (c) replaces; change its expectation and name the change in your report. Add at least 9 new fixtures (3 per repair, including guard cases that must stay clean).\n- Run the selftest, the round-34 counter `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root {sb}/clone --revision <your sandbox commit>` and the round-34 real-input run if cheap. Commit in your sandbox clone and write `git diff {REV} > {sb}/patch.diff`.",
         "patch.diff applies to {REV}; selftest all pass; round-34 counter 28/28 with constants rejected; report lists each fixture added and each behaviour change.")
    ,
    item("ExecIndependentOracle", "executor", OP,
         "An independent implementation of the round-35 link-preview contract, as a differential oracle, in {sb}. Do not read `scripts/link_preview_audit.py` beyond its CLI and JSON output shape.",
         "- From SCORECARD.md \"Round 35 — declared claims\" (C1 contract a-c) and the round-34 interface in {L}/.ufo/waves/round-34/c1-matrix.json (key \"interface\"), write `{sb}/oracle.py` using a tree builder (html5lib or lxml via `uv run --with`), same CLI (`--manifest PATH`), same JSON output and exit codes.\n- Run it on the round-34 matrix (the round-34 counter takes `--revision`; put the oracle at scripts/link_preview_audit.py in a sandbox commit) and on every fixture in scripts/fixtures/link-preview/ at {REV}; list each disagreement and which side the contract supports.",
         "oracle.py runs; matrix result and fixture disagreements listed with the contract text that decides each.")
    ,
    item("ExecDifferentialGenerator", "executor", OP,
         "A seeded generator of random manifests and pages that exercises the round-35 contract and diffs two tool implementations, in {sb}.",
         "- Write `{sb}/difftest.py --tool-a PATH --tool-b PATH --seed N --count K`: generate pages mixing the four required properties, duplicate og:type and og:url, relative/absolute og:url, canonical links in head, template, svg and math (nested and self-closed), non-UTF-8 and directory pages beside readable ones; run both tools; print a JSON summary of disagreements with minimal reproducers.\n- Run it with tool A = the base tool at {REV} and tool B = itself (sanity: 0 disagreements), then with A = base and B = a deliberately repaired toy you write for rule (a) only, to show it finds differences.",
         "difftest.py runs; sanity run 0 disagreements; toy run shows rule-(a) disagreements only; wave 2 can point it at the landed tool and the oracle.")
    ,
    # ---- C2 build
    item("ScribeEntryDraft", "scribe", FR,
         "Draft C2's knowledge entry `corpus/knowledge/security-txt-publishing.md` in {sb}/security-txt-publishing.md. You are the only seat drafting it.",
         "- Bounded question: how does a publisher serve a valid security.txt (RFC 9116) from a GitHub Pages site, for a Jekyll branch build and for an Actions artifact build? Read the retained texts S078, S079, S080, S082, S083, S084, S085 and S006 under {L}/.ufo/waves/round-35/sources/ and existing rows S001, S002, S006 in corpus/SOURCES.md.\n- Cover what a publisher must know and decide: where the file lives and what happens with a second copy, how it is served (scheme, media type, encoding), each field and which are required or single-use, date format and how far ahead Expires should be, contact ordering, encryption and signing, what the file covers (scope), what the two live example files (S084, S085) show against the RFC, and how GitHub Pages builds treat a dot-directory (Jekyll exclusion and `include`, `.nojekyll`, the upload-pages-artifact hidden-file option).\n- Follow the lane's entry header convention (see the first 10 lines of corpus/knowledge/link-preview-metadata.md: source, verified-at, recheck, scope, ground, coverage, falsifier, counter lines). Cite source ids (S078 etc.) beside each fact. Write in your own words: quotes at most 25 words each and few of them; never paste source passages. Stay between 700 and 1300 words in total. Mark lane inferences as inferences.",
         "Draft file exists, 700-1300 words (`wc -w`), every factual sentence carries an id, no quote over 25 words; report lists the facts covered and any source gap.")
    ,
    item("ScoutDs4ccWellKnown", "scout", FR,
         "Offline facts about the operator's ds4cc-marketplace publishing tree that a security.txt on that site would depend on.",
         "- In a sandbox clone of https://github.com/VeigaPunk/ds4cc-marketplace.git (public) at its current head (record the hash), find: whether a `.well-known/` directory, `security.txt`, `_config.yml` (and any `include:` key), `.nojekyll` or `CNAME` exist; which GitHub Pages workflow and `actions/upload-pages-artifact` version publish it and whether `include-hidden-files` is set. Use git ls-tree / git show only. No request to ds4cc.com.",
         "Report lists each fact with `git show <hash>:<path>` evidence and the head hash; says what this implies for serving /.well-known/security.txt, marking inference.")
    ,
    item("ScoutPagesDotfilesSource", "scout", FR,
         "Find the current primary source for how GitHub Pages treats dotfiles and `.nojekyll`, and the current upload-pages-artifact hidden-file default.",
         "- Open by ordinary GET: GitHub Docs pages on publishing sources and static site generators (search docs.github.com for `.nojekyll`), and the current actions/upload-pages-artifact README/action.yml at its latest release tag. Save bodies in {sb}/. For each, give URL, access time (UTC), HTTP status, and a located quote of at most 25 words.\n- Compare against existing rows S001, S002 and S006 in {L}/corpus/SOURCES.md: still current or changed?",
         "Each candidate has URL, time, status, quote and a proposed admit/reject with reason; S001/S002/S006 currency stated with evidence.")
    ,
    item("ScoutSecurityTxtCandidates", "scout", FR,
         "Screen more candidate sources for security.txt publishing beyond the retained S078-S085.",
         "- Open by ordinary GET at most six candidates, for example: the securitytxt.org project repository on GitHub, CISA guidance on security.txt, a security.txt validator's documentation, Google or Cloudflare documentation about serving security.txt. Save bodies in {sb}/.\n- For each: URL, UTC access time, status, tier (A primary / B maintained secondary / C weak) and kind, a located quote of at most 25 words, and a proposed admit, queue or reject with a reason that names what the page does or lacks.",
         "At least four candidates screened with evidence; at least one proposed reject with a located reason.")
    ,
    item("ScoutRfc9116Errata", "scout", FR,
         "Freshness of S078: errata and status of RFC 9116.",
         "- Open https://www.rfc-editor.org/errata/rfc9116 and https://datatracker.ietf.org/doc/rfc9116/ by GET; save bodies in {sb}/. Report each verified or reported erratum (id, section, status, one-line summary) and whether any changes a rule a publisher follows (field names, Expires, location, media type). Also note whether RFC 9116 is updated or obsoleted.",
         "Errata list with ids and statuses, a located quote per page, and a yes/no on publisher-facing changes with evidence.")
    ,
    item("ScoutGithubExpiresDynamic", "scout", FR,
         "Hypothesis: https://github.com/.well-known/security.txt sets Expires a fixed interval after each request (S084 showed Expires 2026-11-21T22:02:20z for a fetch at 2026-10-22T22:02:20Z).",
         "- Fetch the file three times by GET, at least 60 seconds apart, recording the UTC request time, the Date response header and the Expires field each time; save bodies and headers in {sb}/. Also fetch https://www.google.com/.well-known/security.txt once and record its Expires.\n- State whether the hypothesis holds (same offset each time) or is refuted.",
         "Three timed observations with headers and bodies saved; verdict holds/refuted with the measured offsets.")
    ,
    item("ScoutSecurityTxtCensus", "scout", FR,
         "A small public census of security.txt files on ten large public hosts.",
         "- GET https://<host>/.well-known/security.txt for: github.com, www.google.com, www.cloudflare.com, www.mozilla.org, gitlab.com, www.python.org, www.wikipedia.org, www.apple.com, www.microsoft.com, www.facebook.com. Save each body and status in {sb}/census/. For each host: HTTP status, final URL, Content-Type, fields present, Expires value and its distance from the request time in days, Canonical present, signed (BEGIN PGP SIGNED MESSAGE) or not.\n- Write {sb}/census.json and a one-table summary: how many serve it, how many set Expires more than 365 days ahead, how many sign.",
         "census.json with ten rows and the saved bodies; summary counts reproduce from the saved bodies with one command you paste.")
    ,
    item("RevengerJekyllInclude", "revenger", FR,
         "How a GitHub Pages Jekyll branch build treats `.well-known/` and the `include` setting, from the code GitHub Pages runs.",
         "- In a sandbox, read (git clone or GitHub raw by GET) the github/pages-gem repository's configuration defaults (lib/github-pages/configuration.rb) and Jekyll's EntryFilter (lib/jekyll/entry_filter.rb) at the Jekyll version pages-gem pins. Answer: does a `.well-known/` directory get published by default; does GitHub Pages add any default `include` entries; does a user `include: [\".well-known\"]` override the dot exclusion; what does `.nojekyll` do.\n- Quote the code lines with path:line at named commits.",
         "Each answer backed by a quoted code line at a commit hash; mark anything inferred.")
    ,
    item("ScribeSourcesRows", "scribe", FR,
         "Draft `corpus/SOURCES.md` rows S078-S085 and the S006 re-open change, in {sb}/rows.md.",
         "- Use the row shape of rows S067-S077 in {L}/corpus/SOURCES.md (11 cells: id | source with URL | kind | tier | scope | anchor with fetch time, status and retained text sha256 prefix from {L}/.ufo/waves/round-35/sources/receipts.json | teaches | status | opened | recheck | used-by). Proposed statuses: S078, S079, S080, S082, S083, S084, S085 mined, used-by `corpus/knowledge/security-txt-publishing.md`; S081 (Wikipedia) rejected as a secondary restatement with a flip condition. Tier: say why for each (S079 is the RFC authors' project site; S084/S085 are live operator-published files, kind dataset).\n- For S006 (re-opened, same URL): draft the old->new used-by change only; confirm from S006.txt that its taught fact still holds, quoting it.",
         "rows.md has 8 rows with 11 cells each and no unescaped pipe inside a cell; each anchor names a section and the retained text sha256 prefix.")
    ,
    item("ScribeGateLines", "scribe", FR,
         "Draft the round-35 lesson `## Gate` source-opening lines in {sb}/gate.md.",
         "- One line per source S078-S085 plus the S006 re-open, in the shape of {L}/corpus/lessons/round-34.md lines 34-44: URL, accessed UTC time and HTTP status from receipts.json, decision (admit/reject/queue), tier, kind, status, a reason of at least four words naming what the page does or lacks, and a quote of 6-25 words that is an exact substring of the retained text, with its location and word count.\n- Verify each quote with a command (for example python3 checking `quote in text`) and paste the command and output.",
         "gate.md with 9 lines; every quote verified as an exact substring by a pasted command; S081 carries a located reject reason.")
    ,
    # ---- round-34 routed defects
    item("ScribeSkillRegistryRow", "scribe", OP,
         "Routed defect 3 of the round-34 closure: draft the SKILL.md gate registry row for the link-preview audit, in {sb}/registry.md.",
         "- Read the precedent registry tables in {L}/SKILL.md (canonical-audit near line 411, base-path-audit near line 725: columns Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner) and PROTOCOL.md section \"Gate standard\" (in /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md: Registry and Delivery).\n- Draft a `### Link-preview audit gate registry — round 35` heading, the table header and one `link-preview-audit` row: exits 0/1/2/64 with reason names (include the round-35 `og_url_multiple` and the page_unreadable change, marked as round-35 contract), selftest command, pinned proof (round-34 counter receipt, round-35 sealed counter), write scope (none; read-only), owner kake.",
         "registry.md row matches the precedent column set; every command in it exists at {REV} or is named as round-35 pending.")
    ,
    item("ScribeControlCorrection", "scribe", OP,
         "Routed defect 2 of the round-34 closure: draft the appended correction of how the round-34 lookup control dcef39b5 works.",
         "- Fetch {L}/.ufo/waves/round-34/retained/r34-c1-lookup-dcef39b5.bundle into a sandbox clone and read `git show dcef39b5:scripts/link_preview_audit.py`. Read the misdescriptions: {L}/corpus/lessons/round-34.md mistake row 4 (line 68), {L}/.ufo/waves/round-34/criteria/lookup_control_check.py line 6, and SCORECARD.md \"Limits found by wave 1\" (round 34).\n- Draft, in {sb}/correction.md, one correction paragraph per site that quotes the control's own lines with line numbers (what it hashes: argv plus every relative path and file content under the cwd) and states what defeats it (a one-comment HTML change; the round-34 closure measured 7/28 on perturbed cases). Append-only wording: never rewrite the old text.",
         "correction.md with three site paragraphs, each quoting control lines verified by a pasted `git show ... | sed -n` command.")
    ,
    item("ReviewS074Head", "reviewer", FR,
         "Routed defect 5 of the round-34 closure: the S074 reject reason says the page has no og: occurrence.",
         "- Count og: meta tags in the retained body {L}/.ufo/waves/round-34/sources/S074.html.gz (zcat; inside <head> and anywhere) and in S074.txt. Paste commands and counts. Draft, in {sb}/s074-note.md, a one-paragraph correction note for the SOURCES.md notes area in the shape of the \"Round-31 resolution note for S053 and S054\" line, keeping the reject and its reason that the page grounds no publisher-side tag rule.",
         "Counts reproduced by pasted commands; note text drafted; it changes no status, recheck or used-by cell.")
    ,
    item("ExecPrebuildLeakCheck", "executor", BOTH,
         "Routed defect 4 of the round-34 closure: a criterion check that fails when a pre-build receipt publishes a target value, in {sb}/prebuild_leak_check.py.",
         "- CLI: `prebuild_leak_check.py --repo R --receipt-rev REV --receipt PATH --entry-rev EREV --entry PATH --line-regex RE`: read the receipt at REV and the entry at EREV; take the entry line matching RE, extract its key=value pairs (numbers and tokens); exit 1 when every value also appears as a value in the receipt JSON (the target was published before the build), exit 0 otherwise, exit 2 on unreadable inputs. Print the matched values.\n- Show it able to fail: round 34, receipt `.ufo/waves/round-34/verification/c2-at-d08d8de.json` at d08d8de26c9a4290c44282b0eee2b860e8ea4ecc against entry `corpus/knowledge/link-preview-metadata.md` at ce72dd1b31673f62c54e4663ffa9723a53caf79d with RE `^ds4cc-7fc6aa2f-og-census:` must give exit 1. Show a pass: the same entry against `.ufo/waves/round-34/verification/c1-at-d08d8de.json` must give exit 0. Save both outputs with exit codes as text receipts in {sb}/.",
         "Script plus two receipts showing exit 1 and exit 0 on the named inputs.")
    ,
    item("ExecControlDescriptionCheck", "executor", OP,
         "Routed defect 2 as a check: a description of a retained control must quote the control's own bytes, in {sb}/control_description_check.py.",
         "- CLI: `control_description_check.py --repo R --bundle B --revision H --path P --doc D --doc-rev DREV --anchor TEXT`: fetch the bundle into a temporary clone in your sandbox, read P at H; in document D at DREV take the paragraph or table row containing TEXT; exit 0 when that paragraph quotes at least one whole non-blank line of P (backticked, at least 20 characters) and names the line number; exit 1 otherwise; exit 2 on unreadable inputs.\n- Show it able to fail on {L}/corpus/lessons/round-34.md at {REV} (anchor `dcef39b5`, mistake row 4) and show a pass on a sample corrected paragraph you write in {sb}/sample.md quoting real lines. Save both outputs with exit codes in {sb}/.",
         "Script plus a failing receipt on round-34 row 4 and a passing receipt on the sample.")
    ,
    item("ExecRegistryRowCheck", "executor", OP,
         "Routed defect 3 as a check: every lane tool with an exit contract has a SKILL.md gate registry row, in {sb}/registry_row_check.py.",
         "- CLI: `registry_row_check.py --repo R --rev REV`: list `scripts/*.py` at REV that define `EXIT_` constants or document exit codes 0/1/2/64 in their docstring; for each, look in SKILL.md at REV for a markdown table row whose Name cell is the tool's kebab name or whose Entry command cell names the script path; print missing tools; exit 1 when any is missing, 0 when none, 2 on unreadable input. Ignore selftests.\n- Show it at {REV}: it must report `scripts/link_preview_audit.py` missing (exit 1). Then add a sample row in a sandbox commit and show exit 0 for that tool. Report every other tool it flags at {REV} (a real gap is a finding).",
         "Script plus receipts at {REV} (exit 1, link_preview_audit listed) and on the sandbox commit.")
    ,
    item("ScribeQualityCriteria", "scribe", BOTH,
         "Draft QUALITY.md \"Round-35 criteria\" in {sb}/quality.md.",
         "- Read {L}/corpus/QUALITY.md sections \"Round-34 criteria\" and its wave-2 corrections, and the round-34 closure's routed defects 1-5. Draft criteria (a) a declared target must be out of reach of the cheapest do-nothing controls, scored with the frozen counter and committed before the build (name this round's sealed-input design and receipts as the example); (b) no pre-build receipt publishes a target value (check `prebuild_leak_check.py`); (c) a retained control is described by quoting its own bytes (check `control_description_check.py`); (d) every lane tool with an exit contract has a SKILL registry row (check `registry_row_check.py`). Each criterion names its check command (the scripts are being written by other seats; use the CLI shapes in this wave's items) and says what it cannot catch.",
         "quality.md with four criteria, each with a command and a limit.")
    ,
    item("ScribeMistakeMine", "scribe", BOTH,
         "Draft the round-35 lesson `## Mistakes` rows in {sb}/mistakes.md.",
         "- Sweep the round-34 closure {L}/corpus/lessons/round-34-verifier-spotcheck.md, the round-34 lesson and report (/home/vgpnk/Projects/shokunin/.ufo/reports/round-34/kake.md) for author mistakes not yet mined. Expected candidates: the C2 census target published in the declaration receipt; the misdescribed lookup control; the missing registry row; the S074 overclaim. For each: class, evidence pointer (path:line or hash), captured-by (the criterion or rule that should have caught it, or none), fix (the round-35 check that is shown able to fail, named by path).\n- Paste the sweep commands and outputs.",
         "mistakes.md with at least three rows in the table shape of {L}/corpus/lessons/round-34.md line 63, plus the pasted sweep.")
    ,
    item("ScribeProvinceReadme", "scribe", FR,
         "Draft the PROVINCE.md round-35 frontier step and the corpus/README.md coverage row for security.txt publishing, in {sb}/province.md and {sb}/readme.md.",
         "- Read {L}/PROVINCE.md (round-34 link-preview frontier step section) and {L}/corpus/README.md (coverage rows and round-34 section). Draft the matching round-35 sections: security.txt publishing on GitHub Pages enters held ground; what stays out of province (vulnerability handling itself, any live publishing action on operator sites, which is operator-owned).",
         "Two drafts in the shape of the round-34 sections, no cross-domain bleed, operator-owned actions named as such.")
    ,
    # ---- attacks on declaration, counter, controls
    item("CriticSealedDesign", "critic", BOTH,
         "Attack: can any control that skips the claimed work reach C1 >= 22/24 or C2 met without the sealed keys?",
         "- Read {L}/.ufo/waves/round-35/sealed_count.py at {REV} and the declaration. Look for routes around the seal: a revision that holds the key under another path, a key fetched from a ref the counter resolves, counter code paths that pass without running the tool, the cheapest tool that could plausibly pass 22 of 24 from the public contract alone without parsing HTML, an entry that passes probes without studying sources.\n- Build at most two candidate controls as sandbox commits on {REV}, bundle them, and name the bundle paths for the L1 to score.",
         "Each route stated with code line evidence and a verdict (open / closed); bundles named for scoring.")
    ,
    item("CriticC2Conditions", "critic", FR,
         "Attack the C2 conditions other than the probes: size, copied, cites.",
         "- From sealed_count.py at {REV}: can a lightly reworded transcription (word substitution, reordering) pass copiedShare <= 0.25 while carrying the RFC's sentences? Can junk rows pass `cites` (they do: the declaration says so) and what would stop them? Can fenced blocks, escaped pipes or duplicate ids fool registry_rows? Test each on sandbox commits with the public conditions; for probes, say only what the public description allows.\n- Bundle at most two candidate controls (prerequisite {REV}) for the L1 to score.",
         "Each condition attacked with a reproducible sandbox command and result; bundles named.")
    ,
    item("CriticC1ContractAmbiguity", "critic", OP,
         "Attack the C1 public contract (SCORECARD round 35, bullets a-c) for ambiguity that would let two honest implementations differ.",
         "- List concrete inputs where the contract text admits two readings (for example identical duplicate og:url values, an unclosed template, svg inside template, a FIFO page beside readable pages, a manifest whose only page is unreadable). For each, say which reading the text favours and quote it.",
         "A list of at least six inputs with the competing readings and the quoted text deciding each (or `undecided`).")
    ,
    item("MutSealedCounter", "mutation-tester", BOTH,
         "Mutation-test {L}/.ufo/waves/round-35/sealed_count.py with fake keys.",
         "- In a sandbox copy, make your own fake C1 case file and C2 probe file in the same JSON shapes the counter reads, and patch the pinned sha256 constants in your copy only. Build mutants: drop the key-visible refusal, drop the pinned-text check, compare findings as a set not a multiset, skip the verdict compare, accept any exit, count cites without the used-by check, count fenced registry rows, invert a threshold. For each mutant, show whether a fixture run detects it; report survivors.",
         "Mutant table (mutant, detected yes/no, command); survivors listed with a fixture that would kill each.")
    ,
    item("ReviewCounterCode", "reviewer", BOTH,
         "Code review of {L}/.ufo/waves/round-35/sealed_count.py at {REV}.",
         "- Check: exit-code contract (0/1/2) on every path, crash paths (bad JSON key, non-UTF-8 entry, missing git), GIT_ environment stripping, timeout handling, temp-directory cleanup, the registry parser against fenced blocks and escaped pipes, the shingle computation, the word count, the key-visible refusal and the pinned-text check. Use fake keys in a sandbox copy with patched pins to exercise paths.",
         "Findings with line numbers, severity and a reproducing command each; say which findings could change a claim's result.")
    ,
    item("ReviewControlReceipts", "reviewer", BOTH,
         "Verify the committed control receipts and bundles against the SCORECARD control table.",
         "- For each receipt in {L}/.ufo/waves/round-35/verification/control-*.json: the revision it names, the counterSha256 against sha256 of sealed_count.py at 81d9fd74 and at {REV}, the exit file. For each bundle in {L}/.ufo/waves/round-35/retained/r35-control-*.bundle: verify it, fetch it, and check the commit content matches the SCORECARD description (junk rows, keyword list, transcription span, constant tool). Check the round-34 bundles resolve dcef39b5 and 0cce15f0.",
         "Table per control: revision, bundle ok, content matches description yes/no, receipt fields consistent.")
    ,
    item("ReviewDeclarationSizing", "reviewer", BOTH,
         "Review the round-35 declaration against the round prompt's claim-sizing rules.",
         "- Read /home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-35.md section 6 item 9 and SCORECARD \"Round 35 — declared claims\". Check: one concrete after-state per claim re-derivable by one command over committed bytes; no universal clause the counter does not enumerate; controls scored and committed before any build (commit order 81d9fd74 then {REV}); no target value published before the build; claims causally separable; the sourced claim rests on rows opened this round.",
         "A pass/fail line per rule with evidence.")
    ,
    item("SentinelKeyExposure", "sentinel", BOTH,
         "Check that no committed or shared byte reveals the sealed keys before the reveal, without reading the keys.",
         "- Search the lane at {REV} (git grep, git log -p), the fleet repo working tree and /fast/scratch/hyaku/kake-r35/ outside sealed/ for case or probe content: per-case expectations, regex text, the words of probe labels. The receipts list opaque case ids and probe ids with pass flags; say whether those flags let anyone reconstruct a case or probe. You may run `stat -c '%a %U' /fast/scratch/hyaku/kake-r35/sealed` only; never list or read inside it.",
         "Verdict leak/no-leak with the commands run; any exposure path named with evidence.")
    ,
    item("ConnectorSiblingOverlap", "connector", BOTH,
         "Sibling-overlap scan and planning data walk for round 35.",
         "- Scan sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin (read-only) for security.txt, well-known URI or sealed/held-out counter work (git grep at each lane's branch tip). Report overlaps with path:line and whether kake's entry would duplicate or should cite them.\n- Planning data walk: map every item of this wave to C1, C2, the frontier step or a routed defect, and name any round-34 routed defect with no item.",
         "Overlap list (or none, with the commands) and the item map with gaps named.")
    ,
    item("ReviewSpotcheckRouting", "reviewer", BOTH,
         "Review how round 35 routes each round-34 closure defect.",
         "- Read {L}/corpus/lessons/round-34-verifier-spotcheck.md \"Routed defects\" 1-6. For each, name the round-35 artifact that addresses it (declaration, controls, a check, a correction note) at {REV} or as a wave item in this wave context, and say whether the disposition is a fix shown able to fail, a correction by append, or carried. Flag any defect left without a disposition.",
         "Six rows with disposition and evidence pointer; gaps flagged.")
    ,
    item("ReopenSourcesSpecs", "reviewer", FR,
         "Re-open S078, S082 and S083 live and check the retained copies.",
         "- GET https://www.rfc-editor.org/rfc/rfc9116.txt, https://www.rfc-editor.org/rfc/rfc8615.txt and https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml; save in your sandbox; compare body sha256 with {L}/.ufo/waves/round-35/sources/receipts.json and state whether the retained text still matches. Name the sections a publisher needs (RFC 9116 sections 2.5, 3, 4; RFC 8615 section 3; the registry's security.txt row) and quote one located line of at most 25 words from each.",
         "Three rows: status, sha match yes/no, located quote, tier/kind check.")
    ,
    item("ReopenSourcesOthers", "reviewer", FR,
         "Re-open S079, S080, S081, S084, S085 and the S006 page live and check the retained copies.",
         "- GET https://securitytxt.org/, https://jekyllrb.com/docs/configuration/options/, https://en.wikipedia.org/wiki/Security.txt, https://github.com/.well-known/security.txt, https://www.google.com/.well-known/security.txt and https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll; save in your sandbox; compare with receipts.json (S084 is expected to differ in Expires: say by how much). Quote one located line of at most 25 words per page, and judge whether S081 should be rejected as a secondary restatement.",
         "Six rows: status, match or the exact difference, quote, tier/kind check, S081 verdict with reason.")
    ,
    item("ReviewSelftestContractChange", "reviewer", OP,
         "Harm check for C1 contract (c): it changes round-34 behaviour (policy findings were suppressed on any input fault).",
         "- Find every lane text and check that relies on the old behaviour: git grep at {REV} for `policy_suppressed`, `could-not-evaluate`, `page_unreadable` and `link_preview` in SKILL.md, corpus/, scripts/ and .ufo/waves/round-34/. For each, say whether contract (c) makes it false and what must be appended. Also check the round-34 matrix cases with input faults keep their expected outputs under (c).",
         "List of dependent texts and checks with path:line and the needed append; matrix check result.")
    ,
    item("CriticHarmPlan", "critic", OP,
         "Attack: which existing measures could the C1 repair harm, and how to show it did not.",
         "- From the lane at {REV}: list every counter, selftest and receipt that runs `scripts/link_preview_audit.py` (round-34 C1 counter, selftest, real-input run). Write the exact before/after commands wave 2 should run at the landed repair commit, and predict any expected change in each (for example the selftest fixture whose rule (c) replaces). Run the before side at {REV} now and save outputs in your sandbox.",
         "Command list with before outputs captured at {REV} and predicted after values.")
    ,
]

spec = {"wave": "kake-r35-w1", "milestone": "r35-build", "maxLanes": 64, "axes": BOTH,
        "reportDir": ".ufo/waves/round-35/w1", "context": CONTEXT, "items": ITEMS}
(HERE / "w1-spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
print(len(ITEMS), sorted({i["role"] for i in ITEMS}))
