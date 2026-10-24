# ConnectorSiblingOverlap — round 46 w1

Axes named: adjacency (judged), operability, freshness.

Attack: does any other lane own redirect/rewrite-rule auditing or citation-resolution linting?

Result: **pass — clean.** 10/10 sibling headers are clean on both surfaces. 0 contested. No sibling header claims static-host redirect/rewrite-rule auditing or commit-citation lint over a SCORECARD/LOG population.

## What I did

Read first 80 lines only of `SKILL.md` and `PROVINCE.md` for kasegi, kengaku, kumitate, kotoba, kagi, kama, tabi, chousa, mori, tameshi. Also read kake's own province header (`PROVINCE.md:1-63`) and skill description (`SKILL.md:1-4`) as the local split, not as a sibling. Did not read file bodies past the header, did not edit committed files, did not commit.

No tools installed. PACMAN not touched.

## Decisive command

```text
python3 - << 'PY'
import pathlib
root = pathlib.Path("/home/vgpnk/Projects/shokunin")
lanes = ["kasegi","kengaku","kumitate","kotoba","kagi","kama","tabi","chousa","mori","tameshi"]
keys = ("redirect", "rewrite", "citation", "lint")
for lane in lanes:
    base = root / f"{lane}-shokunin"
    print(f"===== {lane} =====")
    for name in ("SKILL.md", "PROVINCE.md"):
        p = base / name
        lines = p.read_text(errors="replace").splitlines()
        head = lines[:80]
        dom = next((ln.strip() for ln in head if ln.startswith("**Domain:**") or ln.startswith("description:")), "")
        owns = next((ln.strip() for ln in head if ln.startswith("**Owns:**") or ln.startswith("**Owns ")), "")
        hits = []
        for i, ln in enumerate(head, 1):
            low = ln.lower()
            found = [k for k in keys if k in low]
            if found:
                hits.append(f"    L{i} [{','.join(found)}] {ln.strip()[:180]}")
        print(f"-- {name} lines={len(lines)} head=80")
        print(f"  domain: {dom[:220]}")
        if owns:
            print(f"  owns: {owns[:220]}")
        print(f"  header-hits: {len(hits)}")
        for h in hits[:8]:
            print(h)
PY
```

Verbatim stdout (prints are sliced at 220/180 by the script; nothing below was retyped):

```text
===== kasegi =====
-- SKILL.md lines=1023 head=80
  domain: description: Domain specialist — bounty & security research — scopes ~/Projects/bounties, program rules, claim packages. Rank: shonen.
  header-hits: 2
    L17 [citation] cites a file — but as of round 15 each citation resolves against one of three
    L29 [citation] `964f443e`). Citations that resolved against them are now marked
-- PROVINCE.md lines=49 head=80
  domain: **Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages
  owns: **Owns:** the domain knowledge, playbooks, error patterns, and checklists above.
  header-hits: 0
===== kengaku =====
-- SKILL.md lines=703 head=80
  domain: description: "Domain specialist — LLM/model research & evaluation — eval design, benchmark selection, offline replay grading, blind shim-cascade leg attribution and interval-calibrated verdicts; llm-wiki (~/Projects/webz
  header-hits: 1
    L14 [citation] wiki citation below is a dated historical observation; what this lane retains
-- PROVINCE.md lines=211 head=80
  domain: **Domain:** LLM/model research & evaluation — scopes ~/Projects/webzites/repos/llm-wiki, route telemetry
  owns: **Owns:** the domain knowledge, playbooks, error patterns, and checklists above.
  header-hits: 0
===== kumitate =====
-- SKILL.md lines=904 head=80
  domain: description: Domain specialist — orchestration & tooling — scopes OMP task/hub dispatch, ufo-fsd scripts, crates/ufo-core-runtime. Rank: shonen.
  header-hits: 0
-- PROVINCE.md lines=28 head=80
  domain: **Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime
  owns: **Owns:** the domain knowledge, playbooks, error patterns, and checklists above.
  header-hits: 0
===== kotoba =====
-- SKILL.md lines=599 head=80
  domain: description: >
  header-hits: 2
    L4 [rewrite] Prompt & skill craft — audits, writes, and rewrites SKILL.md / AGENTS.md /
    L55 [citation] line has drifted, re-read the file and update the citation — do not
-- PROVINCE.md lines=67 head=80
  domain: **Domain:** prompt & skill craft — scopes SKILL.md/AGENTS.md quality, trigger fidelity
  owns: **Owns:** the domain knowledge, playbooks, error patterns, and checklists above.
  header-hits: 3
    L21 [redirect] - Always-on rule files (round 53, moved from Frontier "Executed checklist coverage", its always-on half): which always-on file names nine clients read, what each does when `AGENTS.
    L27 [citation] - Compound-clause citation on this lane's scoped-rule Action cells, and appended correction of this lane's own committed record (round 63): an Action cell must clear A2's forward-s
    L56 [citation] | kasegi | adjacent | 1fafde8f11454f3b0b98ab7f2b2e640aaf7f399a | bounty and security research; kotoba's description names kasegi among the lanes that own their own SKILL.md content
===== kagi =====
-- SKILL.md lines=813 head=80
  domain: description: Domain specialist — secrets & vault ops — the-janitor flows, credential hygiene evidence, vault lifecycle. Rank: shonen.
  header-hits: 2
    L46 [citation] | Re-run a claim this corpus makes / name the revision you read / cite an artifact / audit a score | `bash corpus/claim-ledger.sh verify` (91 stamps + 65 claims + claim ids; both c
    L49 [citation] | Learn from, cite or curate an external source | a row in `corpus/SOURCES.md` (opened this round, tier scoped to its claim, anchor + revision) then `bash corpus/sources-census.sh`
-- PROVINCE.md lines=84 head=80
  domain: **Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence
  owns: **Owns:** the domain knowledge, playbooks, error patterns, and checklists above.
  header-hits: 3
    L51 [citation] - `corpus/scope-gate.sh` — ownership partition + shared-directory breadth. `corpus/adjacency.tsv` declares 5 owned prefixes (27 census rows), 4 shared groups (8 rows), 8 no-enumera
    L52 [citation] - `corpus/claim-ledger.sh` — calibration gate: `verify` (91 revision stamps + 65 claim rows; since round 24 host/substrate rows are HOST-SKIPped by default and run only with `--all
    L55 [citation] - `corpus/sources-census.sh` — source-registry gate (round 21): the SOURCES-CONTRACT-v1 census over `corpus/SOURCES.md` plus the citation handshake with `corpus/knowledge/` entries
===== kama =====
-- SKILL.md lines=1313 head=80
  domain: description: Domain specialist — local model serving & endpoint health — scopes local LLM endpoints, baseURL drift, model-id reconciliation. Rank: shonen.
  header-hits: 0
-- PROVINCE.md lines=148 head=80
  domain: **Domain:** local model serving & endpoint health — local LLM endpoints, baseURL
  owns: **Owns (surfaces):**
  header-hits: 0
===== tabi =====
-- SKILL.md lines=2441 head=80
  domain: description: Domain specialist — browser & web-interaction craft. Rank: shonen (probation).
  header-hits: 2
    L18 [citation] (§Approval table). If a hash in §Pins has moved, every citation is stale — re-verify the
    L68 [citation] A hash change means the citations below are stale — re-verify against the note before
-- PROVINCE.md lines=21 head=80
  domain: **Domain:** browser & web-interaction craft (旅, journey) — driving real
  owns: **Owns (surfaces):** the kimi-webbridge plugin
  header-hits: 0
===== chousa =====
-- SKILL.md lines=699 head=80
  domain: description: "Deep-research method (調査) — question framing, source hierarchy, citation chaining, claim-vs-source verification. Triggers: 'research this', 'deep research', 'verify this claim', 'primary source', 'citation 
  header-hits: 5
    L3 [citation] description: "Deep-research method (調査) — question framing, source hierarchy, citation chaining, claim-vs-source verification. Triggers: 'research this', 'deep research', 'verify t
    L9 [citation] sources outrank which, how a citation chain is followed, and how a claim is
    L19 [citation] | Follow a citation chain | follow each hop to the cited artifact and resolve its anchor there | stopping at a summary of the citation | chain with each hop's anchor verified or ma
    L34 [citation] fleet gates state citation *mechanics* (resolvable, pinned, labelled), not this
    L47 [citation] | hop anchor resolves but the relay drops a qualifier | altered hop — `resolved` is not faithful; compare proposition, scope, quantity, hedge, date at that hop (`corpus/knowledge/c
-- PROVINCE.md lines=17 head=80
  domain: **Domain:** deep-research method (調査) — the reusable craft of source research.
  owns: **Owns:** question framing; source hierarchy (primary / secondary / aggregator /
  header-hits: 1
    L6 [citation] unsourced); citation chaining and hop resolution; claim-vs-source verification;
===== mori =====
-- SKILL.md lines=888 head=80
  domain: description: "Fleet & host observability (森) — detect and report fleet liveness, wave settlement, kill/OOM events and resource runway. Triggers: 'fleet health', 'did a wave die', 'why did the daemon vanish', 'watchdog li
  header-hits: 0
-- PROVINCE.md lines=400 head=80
  domain: **Domain:** fleet & host observability (森) — whether the fleet, its waves and
  owns: **Owns (read-only probes):** shokunin watchdog liveness (pid, start time, log
  header-hits: 1
    L69 [citation] | souji | Lists own-uid scratch residue and proposes removal for operator approval; routes liveness/resource findings to mori. Mori reports, never performs reclamation. | `souji-sh
===== tameshi =====
-- SKILL.md lines=2136 head=80
  domain: description: "Verification-fixture craft for 'hermetic suites', 'mutation testing', and 'gate fixtures'. Anti-trigger: product behavior or endpoint health; route those to the product lane or kama. Rank: shonen."
  header-hits: 0
-- PROVINCE.md lines=118 head=80
  domain: **Domain:** verification-fixture craft — the reusable method of honest
  owns: **Owns:** the method, documented from the fleet's existing gates as primary
  header-hits: 0
```

Header lines behind the two false-friend tokens (read, not inferred): kotoba `SKILL.md:4` is "rewrites SKILL.md / AGENTS.md"; kotoba `PROVINCE.md:21` is always-on rule-file redirects (`AGENTS.md` / `CLAUDE.md`), not HTTP host rules. chousa `SKILL.md:34-35` says fleet gates own citation mechanics (resolvable, pinned, labelled) and chousa owns the ranking. kake `PROVINCE.md:29` still lists Render deploy semantics as frontier; `PROVINCE.md:36-37` already gives research method to chousa.

## Proposed move

Scope fence, recorded in `build/connector-overlap.md`, for the seats that create the two new scripts:

- `citation_lint.py`: commit-object resolution over `{SCORECARD.md, LOG.md}` only. Do not absorb chousa hop resolution, kagi `claim-ledger.sh citations`, or kotoba Action-cell citation.
- `redirect_audit.py`: read-only network-free version-1 static-host redirect/rewrite manifest. Do not absorb tabi CDP, kama endpoint probes, or kotoba always-on file redirects.

Adjacency improves (shared verbs stay on their own surfaces). Operability and freshness stay inside the frozen sentences: offline, local, no sibling-tool dependency.

Risk: generalizing "resolve" to every path:line or URL, or shelling out to a sibling gate, crosses the split. Foreign-repo pins stay object-resolve or ledger-adjudicate.

## Files written

- `.ufo/waves/round-46/build/connector-overlap.md`
- `.ufo/waves/round-46/w1/ConnectorSiblingOverlap.md` (this report)
- scratch dir created: `/fast/scratch/hyaku/kake-r46/ConnectorSiblingOverlap/` (empty; no temp file retained)

## Unrun

`scripts/redirect_audit.py` and `scripts/citation_lint.py` were not executed (not this seat's files). No install.
