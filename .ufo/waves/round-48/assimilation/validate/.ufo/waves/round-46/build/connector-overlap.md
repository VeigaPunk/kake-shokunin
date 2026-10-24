# Round 46 — sibling overlap (redirect/rewrite audit, citation-resolution lint)

Scan: headers only (first 80 lines) of `SKILL.md` and `PROVINCE.md` for kasegi, kengaku, kumitate, kotoba, kagi, kama, tabi, chousa, mori, tameshi under `/home/vgpnk/Projects/shokunin/<lane>-shokunin/`. Bodies below line 80 were not read.

Question: does the header claim ownership of (C1) static-host redirect/rewrite-rule auditing, or (C2) resolving lane commit citations in a committed ledger (`SCORECARD.md` / `LOG.md` class)?

Rule: **contested** only if a header claims one of those two surfaces. A shared verb on a different surface is **clean**, with the nearest miss named. Kake's own split (not a sibling claim): `kake-shokunin/PROVINCE.md:34-41` routes research method to chousa, browser driving to tabi, endpoints to kama, secrets to kagi; `PROVINCE.md:29` leaves Render deploy semantics on kake's frontier.

Verdict: **10 clean, 0 contested.**

| lane | verdict | one-line evidence |
|---|---|---|
| kasegi | clean | Header domain is bounty/security research (`PROVINCE.md:3`); adjacent line names kake as web properties (`PROVINCE.md:46`). "citation" in `SKILL.md:17,29` is lost-tree file bases, not a commit-lint or rewrite audit. |
| kengaku | clean | Header domain is LLM eval (`PROVINCE.md:3`); refusal names kake web properties and says the shared word "probe" carries no scope (`PROVINCE.md:33`). No redirect/rewrite or commit-lint claim in the header. |
| kumitate | clean | Header domain is OMP/ufo-fsd orchestration (`PROVINCE.md:3`); core instruments are claims-check, proxy-check, kimi-census, sources-check (`PROVINCE.md:12-15`). Zero header hits for redirect/rewrite/citation/lint. |
| kotoba | clean | Header domain is prompt/skill craft (`PROVINCE.md:3`). `SKILL.md:4` "rewrites" means rewriting SKILL.md text; `PROVINCE.md:21` "redirect" means client always-on file redirects (AGENTS.md/CLAUDE.md), not HTTP host rules. `PROVINCE.md:27` compound-clause citation grades this lane's Action cells, not kake commit tokens. Census row sends web publishing to kake (`PROVINCE.md:54`). |
| kagi | clean | Header domain is secrets/vault (`PROVINCE.md:3`). `claim-ledger.sh citations` and `sources-census.sh` (`SKILL.md:46,49`, `PROVINCE.md:52,55`) audit kagi's own stamps, not kake SCORECARD commit objects. Header contest with kake is the musketeer CDP profile lease (`PROVINCE.md:43`), a different surface. |
| kama | clean | Header domain is local model endpoints (`PROVINCE.md:3-4`); explicit refusal of remote web surfaces to kake (`PROVINCE.md:40-43`, `SKILL.md:29`). Zero header hits for redirect/rewrite/citation/lint. |
| tabi | clean | Header domain is browser/CDP craft (`PROVINCE.md:3-4`); refusal sends web publishing to kake (`PROVINCE.md:15-16`). Header "citation" hits are pin-staleness of tabi notes (`SKILL.md:18,68`), not commit-lint. |
| chousa | clean | Nearest verb-family miss, not a surface contest. Header owns research-record citation chaining and hop resolution (`SKILL.md:3,9,19`, `PROVINCE.md:5-8`) and disclaims fleet citation mechanics (`SKILL.md:34-35`: fleet gates state resolvable/pinned/labelled mechanics; chousa owns the ranking). Kake already keeps only its own findings and `corpus/SOURCES.md` rows (`kake-shokunin/PROVINCE.md:36-37`). |
| mori | clean | Header domain is fleet/host liveness (`PROVINCE.md:3-4`); refuses orchestration, OS state, endpoint health, credentials. The only header "citation" hit is a souji path pin (`PROVINCE.md:69`). |
| tameshi | clean | Header domain is hermetic/mutation fixture method (`PROVINCE.md:3-5`); "every lane's gate remains its own" (`PROVINCE.md:14-16`). Zero header hits. A kake-local commit lint or redirect manifest audit does not become tameshi's gate. |

## False friends (do not smooth)

- kotoba `rewrite` / `redirect` tokens are instruction-file craft, not Render redirect/rewrite rules.
- chousa, kagi, and kotoba all "resolve citations," on research hops, vault claim stamps, and skill Action cells respectively. None names git commit-object resolution over `{SCORECARD.md, LOG.md}`.
- kagi×kake musketeer profile lease stays contested elsewhere; it is not C1 or C2.

## Proposed move (one)

Scope fence for the two new tools, not a province edit (committed province files stay frozen):

- `scripts/citation_lint.py` stays a commit-object resolver over the frozen population `{SCORECARD.md, LOG.md}`: hex tokens that are lane commit citations, with sha256-digest prefixes and line-adjudicated foreign pins classified, not fetched. It does not call chousa hop resolution, kagi `claim-ledger.sh citations`, or kotoba Action-cell support.
- `scripts/redirect_audit.py` stays a read-only, network-free reader of a version-1 static-host redirect/rewrite manifest. It does not open a browser (tabi), probe a model port (kama), or treat always-on file redirects (kotoba) as checks.

Axes: adjacency improves (verb collision cannot be read as ownership). Operability and freshness are unchanged: both tools stay offline, local, and inside the frozen sentences.

Risk: an implementer who "resolves" every path:line or URL in those two files, or who shells out to `research-gate` / `claim-ledger`, crosses the split and harms adjacency without helping either frozen counter. Foreign-repo pins in C2 are ledger adjudication or object resolution, not a research hop.

Verification already run: header keyword extract over the ten lanes, first 80 lines (see seat report). Unrun: no tool execution of `citation_lint.py` or `redirect_audit.py` (neither is this seat's file).
