# Round 23 sibling-overlap scan

## Verdict

The intended ownership split is sound: Kake checks publisher-side static HTML and its declared canonical policy; Tabi owns browser/CDP and client-side crawler evidence; Chousa owns research method and source hierarchy. The two meanings of “C2” are unrelated: Kake C2 is this round’s canonical-preflight claim, while Tabi C2 is its operator-owned-site interaction class.

There is one concrete avoidable overlap: C1 knowledge-unit rechecks can ask for GETs of the same root URLs already snapshotted for C2. The property-map C1 task explicitly excludes that overlap, but the generic C1 task does not. Recommend reusing an exact, same-day C2 fetch receipt/body as the C1 observation for the identical URL, while retaining separate claim-level verdicts. Do not transfer Kake’s GET authority to Tabi browser work or Chousa research, and do not present static canonical-policy results as rendered-DOM or search-engine selection evidence.

## Findings

### P2 — C1/C2 share root-page observations, but only the property-map task is explicitly deduplicated

**Exact inspected calls:** `functions.read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/gen_w1.py:35-47")`; `functions.read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/vault-properties.md:1-20")`; `functions.read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/live/vault-index-kimi/fetch.json")`.

**Observed output:** the generated property-map assignment says “Re-verify the NON-page claims only” and “Page-serving status of the 12 surfaces is covered by sibling items; do not duplicate it” (gen_w1.py:35-37). The generic assignment for the other C1 units says to re-verify live claims, with public URLs via GET/HEAD (gen_w1.py:39-41). `vault-properties.md:7-19` names `veigapunk.kimi.page` and prescribes GETting it; C2 includes that same page as `vault-index-kimi` (`c2-population.json:38-41`). The committed C2 fetch receipt records `"fetchedAt": "2026-10-21T06:33:08Z"`, `"method": "GET"`, `"status": 200`, `"bytes": 10059`, and `"sha256": "a0a7f33aba443a85a4952a0bf57aa52947fdf95638b5ac7aba1c7d92b87a92fb"` (`live/vault-index-kimi/fetch.json:2-12`). Another exact overlap is `publish-queue.md:111-116`’s `charter-ufo-fsd.kimi.page` and C2’s `charter-kimi` surface (`c2-population.json:74-77`); its stored C2 receipt says `"fetchedAt": "2026-10-21T06:33:20Z"`, `"method": "GET"`, `"status": 404` (`live/charter-kimi/fetch.json:5-12`).

**Impacted claims/axes:** C1 freshness and C2 operability. These are related observations, not interchangeable verdicts: C1 checks whether a historical knowledge claim remains true; C2 applies the local canonical policy to the served page. The saved fetch can support both only when the C1 claim concerns that exact URL and the snapshot contains the needed evidence.

**Smallest fix / proposed move:** for an exact C1/C2 root-URL match, cite the C2 `fetch.json` and, when present, `page.html` as the single dated live observation in the C1 receipt instead of issuing a second GET. Keep the C1 `HOLD`/`STALE`/`UNVERIFIABLE` decision separate from the C2 canonical audit verdict. Do not reuse a root snapshot for a subpath, a different URL, a claim requiring a later observation, or a claim whose evidence is absent from the saved response. This is a receipt/evidence-routing change only; no production or sibling files need modification.

### P2 — Static canonical policy is not Tabi’s rendered-browser surface

**Exact inspected calls:** `functions.read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/PROVINCE.md:20-58")`; `functions.read(path="/home/vgpnk/Projects/shokunin/tabi-shokunin/PROVINCE.md:1-21")`; `functions.read(path="/home/vgpnk/Projects/shokunin/tabi-shokunin/SKILL.md:720-729")`; `functions.read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/static-canonical-preflight.md:7-30,58-94")`; `functions.read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py:6-15,50-81")`.

**Observed output:** Kake’s province assigns browser/client-side crawler discipline to Tabi and publisher-side placement to Kake (Kake `PROVINCE.md:30-31`); Kake’s frontier says canonical/JS rendering remains open and browser execution is Tabi-adjacent (`:22-23,52-58`). Tabi owns CDP endpoints/targets and screenshot/DOM evidence and refuses web publishing (`tabi/PROVINCE.md:6-19`). Its approval taxonomy makes operator-owned sites C2 “operator-asleep-blocked” pending an operator go-ahead naming site and scope, and third-party read-only C3 default-deny (`tabi/SKILL.md:724-726`). Kake C2 instead explicitly permits GET-only public-page snapshots and says the policy comparison is “never search-engine selection” (`contract.json:26`). The snapshot implementation issues HTTP GET and saves served response bytes; it does not launch a browser or render JavaScript (`live_snapshot.py:6-15,50-81`). Kake’s canonical note likewise limits the tool to publisher-side static-file validation and disclaims browser crawling/search selection (`static-canonical-preflight.md:7-9,27-30,90-94`).

**Impacted claims/axes:** C2 operability and C1 freshness, at the boundary between a served-byte observation and a rendered-page claim. There is no conflict for the actual Kake GET-only workflow. A conflict would arise only if Kake’s round authorization were treated as permission for Tabi to navigate/inspect an operator-owned site in a browser without Tabi’s site-and-scope approval, or if a static audit were described as proving the rendered canonical.

**Smallest fix:** keep the evidence label explicit (`publisher-static-html` versus `rendered-DOM/CDP`). Any rendered-DOM follow-up must be a separately scoped Tabi task and satisfy Tabi’s approval table; absent that, record rendered canonical behavior as untested/open.

### P2 — Chousa’s research approval and support standard are not supplied by a Kake live receipt

**Exact inspected calls:** `functions.read(path="/home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md:1-17")`; `functions.read(path="/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md:17-23,47-64")`; `functions.read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/contract.json:7-26")`.

**Observed output:** Chousa owns source hierarchy, citation chains, claim-vs-source verification and the external-target approval table (`chousa/PROVINCE.md:5-15`). Its skill refuses external live-target research without operator approval and says a window without its approval table is loopback-only (`chousa/SKILL.md:49-51`). It also separates “opens,” “on-topic,” “states the claim at a named anchor,” and “true”; access alone is not verification (`:22-23`). Kake C1 instead authorizes read-only GET/HEAD of public pages and calls `HOLD` an observation at `observedAt`, not a guarantee (`contract.json:12,15`); Kake C2’s permitted GET is limited to its owned surfaces and explicitly disclaims search-engine selection (`:21-26`).

**Impacted claims/axes:** C1 freshness and C2 operability. Kake’s own property recheck is within Kake’s declared domain; it does not authorize Chousa to perform external live research. Likewise, a Kake receipt can establish what its URL served at a time, but cannot by itself establish a factual claim’s truth or a source’s authority.

**Smallest fix:** retain Kake’s dated observation/verdict vocabulary for its own claims; do not relabel a C1 `HOLD` as Chousa-style `verified`, and route any independent external-source research through Chousa’s own approval and evidence procedure.

## Affected axes and proposed move

**Move (one bounded evidence-routing change):** allow exact-URL reuse of the current C2 snapshot as the live observation for any matching C1 knowledge claim, while recording the C1 and C2 conclusions independently. Keep static publisher policy, browser-rendered state, and source-truth validation as explicitly separate evidence classes. This improves operability by avoiding duplicate GETs and improves freshness by pointing both receipts to the same dated bytes; it does not change the frozen claims, source tree, or any sibling’s authority.

## Risks

- Same URL is not enough when a C1 claim concerns a subpath, links inside a page, deployment vintage, or a different property; those require their own observation.
- C2’s non-served outcome establishes status, not response-body facts; unsupported/truncated snapshots must not be rounded up to clean.
- Kake’s local expected-canonical policy is not universal SEO truth. A clean result means only that the supported static HTML matches the locally declared policy; it does not establish rendered DOM, Google-selected canonical, or factual source support.
- Approval does not transfer across provinces: a Kake GET-only authorization is not a Tabi browser approval or a Chousa external-research approval.

## Verification

**Read-only verification performed:** inspected the frozen round-23 contract/populations, generated seat instructions, Kake/TAbi/Chousa policy files, and existing local round-23 snapshot receipts. Example exact local evidence: `live/vault-index-kimi/fetch.json` records a 2026-10-21 GET/200/10,059-byte snapshot; `live/charter-kimi/fetch.json` records a 2026-10-21 GET/404/13,409-byte response. These are cached observations, not new requests by this scan.

**Not run:** no HTTP request, browser/CDP session, selftest, matrix, or counter. To verify the proposed move in the round output, compare C1 receipt surfaces against the 12 frozen C2 URLs: for exact root matches, confirm the C1 observation points to the dated C2 receipt/body while preserving its own claim verdict; confirm subpaths and missing/unsupported bodies are not treated as covered. Separately keep the C2 counter/audit as the authority for the 12 static canonical-policy results. No admission or integration is claimed.

## Checked and held

- `/home/vgpnk/Projects/shokunin/MISSION.md:16-29` labels the displayed lane table a historical example; it lists Kake as “operability + freshness (web properties),” but is not evidence of the current roster. The frozen round-23 contract supplies the operative C1/C2 claims and axes.
- Read-only sibling policies: `/home/vgpnk/Projects/shokunin/tabi-shokunin/SKILL.md` and `PROVINCE.md`; `/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md` and `PROVINCE.md`.
- Read-only Kake evidence used: frozen contract and populations, `gen_w1.py`, `PROVINCE.md`, `SKILL.md` property map, `static-canonical-preflight.md`, `live_snapshot.py`, `canonical_audit.py` declarations, and cached snapshot/summary files.
- No sibling, production, cache, or domain source files were changed. The only write is this scoped report.

## Limits

This scan assesses jurisdiction and evidence overlap from local repository/cache text only. It did not contact the public sites or test the browser/parser behavior. Tabi’s approval table and Chousa’s external-target rule were read as written; this report does not grant either lane approval. The cached C2 snapshots remain point-in-time observations.