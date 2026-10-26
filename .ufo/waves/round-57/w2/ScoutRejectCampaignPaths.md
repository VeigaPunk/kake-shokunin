# ScoutRejectCampaignPaths

Read: lane tree as it stands 2026-10-25 (`PROVINCE.md`, `corpus/SOURCES.md`), staged files under `/home/vgpnk/Projects/shokuknow/merge/kake/` (read-only), campaign evidence under `/home/vgpnk/Projects/shokuknow/lanes/kake/round15|16/.evidence/` (read-only). No live Baidu/Ollama fetch was run (unrun). No tool installed.

## S404/S414:

**Staged lines** (confirmed by running `cat -n`):
- `baidu-series-has-no-rendering-section.md` (S404) line 2: `source: S404 — lanes/kake/round15/.evidence/baidu_series_sweep_r15.txt — § the per-article table — own measurement, 2026-10-24`; line 4 `recheck: 180d — bash lanes/kake/round15/.evidence/lane_sweeps_r15.sh && grep -F -c 'no article body mentions rendering' …baidu_series_sweep_r15.txt -> 1`.
- `baidu-wiki-publication-map.md` (S414) line 2: `source: S414 — lanes/kake/round16/.evidence/wiki_map_r16.txt — § the index census and the per-announcement vocabulary table`; line 4 `recheck: … bash lanes/kake/round16/.evidence/lane_sweeps16.sh && grep -F -c 'never an execution of a script' …wiki_map_r16.txt -> 1`.
- Staged registry rows `merge/kake/SOURCES.append.md` lines 124, 134: kind `own-work`, tier B, relative paths as above. Neither id is in the lane registry (`grep -c '^| S404 ' corpus/SOURCES.md` = 0, same S414, S358).

**`test -e` results** (confirmed by running):

| path (relative to a root) | under `kake-shokunin` | under `/home/vgpnk/Projects/shokuknow` |
|---|---|---|
| `lanes/kake/round15/.evidence/baidu_series_sweep_r15.txt` | absent (`kake-shokunin/lanes` does not exist) | EXISTS (1748 B, 18 lines) |
| `lanes/kake/round16/.evidence/wiki_map_r16.txt` | absent | EXISTS (1756 B) |
| `…/round15/.evidence/lane_sweeps_r15.sh` (recheck script) | absent | EXISTS |
| `…/round16/.evidence/lane_sweeps16.sh` (recheck script) | absent | EXISTS |

`find /home/vgpnk/Projects -name <the four names>` returns only those four shokuknow paths. So the evidence **does exist and is readable**, but only in the shokuknow repo (the relative `lanes/kake/…` path resolves against the shokuknow root, never against the lane). The raw fetched bodies it counts also exist there (`round15/.evidence/baidu_3453…3462_r15.txt`, `round16/.evidence/baidu_wiki{963,990,1021,867}_r16.txt`, `baidu_wiki_index_r16.txt`, `fetch_manifest_r15.txt`).

**Claims (both are NEGATIVE claims, "no page says X"):**
- S404: nine Q&A-series articles (ids 3453,3454,3456–3462; 3455 is "Page Not Found", not in manifest) contain 渲染 zero and JavaScript zero times in the body, so no Baidu-authored sentence on whether its spider executes a script is in the series.
- S414: the `/wiki/` index lists 300 entries, 9 with crawl/agent titles, 4 fetched; 执行 appears in none; title says "Three hundred announcements, and not one says the spider executes a script".

**Could the sweeps be re-run?** Yes, in two modes.
- Offline re-count (confirmed by running, stdout only, nothing written): I ran the entry's own `body()` sed pipeline on the nine r15 files: 渲染=0 and JavaScript=0 in all nine (3457 has one 执行, in a curl instruction, not about rendering). r16: 渲染/执行 = 963: 0/0, 990: 2/0, 1021: 6/0, 867: 0/0, matching `wiki_map_r16.txt`. Index re-parse (the script's own regex) gives 300 unique `/wiki/` links, ids 519–3566.
- Caveat: both shell scripts hard-code `EV=/home/vgpnk/Projects/shokuknow/...` and "Reads only files already fetched" (header comments). Re-running them re-counts stored bytes; it does not re-fetch. They cannot run from the lane (`bash lanes/kake/round15/…` path does not exist there).
- Live re-run (unrun by me): `curl -sS -L -m 60 'https://ziyuan.baidu.com/college/articleinfo?id=N'` for N in 3453 3454 3456 3457 3458 3459 3460 3461 3462, then strip as the script does and count 渲染/JavaScript; for S414 `curl 'https://ziyuan.baidu.com/wiki/'` and `/wiki/{963,990,1021,867}`.
- Fact: this round's retained `S421.html` equals `baidu_3458_r15.txt` in size (34750 B) but is not byte-identical (`cmp` differs at line 346; `diff` is 10 lines, the passport `cdnversion` query only). S422.html is 27327 B, same size as `baidu_wiki867_r16.txt`, also not byte-identical (cmp at line 318). Both retained bodies have 渲染=0, 执行=0 (`grep -o`, confirmed by running).

**Weaknesses of the entries themselves (confirmed by running unless marked):**
1. Method text: the sweep's `body()` replaces only the opening `<script…>`/`<style…>` tag with a newline; it does not delete the block's content. The entry says "script and style blocks stripped". Inline script text stays in the count, so a zero is still a zero, but the stated method is not what ran.
2. S414 line 7 title/line 17-28 overclaim: only 4 of 300 announcements were fetched and counted; "not one says" is a four-page measurement. Also "the one announcement that mentions JavaScript does so to say the crawler fetches it" — my text pass on 990 finds "访问网站的CSS、Javascript和图片信息" (fetches), but 1021 (06-07) says "尽量不要使用 JS 加载的方式，以免造成不能索引" (avoid JS-loaded content, risk of non-indexing); the sweep vocabulary (`JavaScript|Javascript|javascript`) misses "JS". The entry's practical conclusion agrees with 1021, but its "mentions JavaScript" tally is incomplete.
3. The 300 figure: single index page, `/wiki/` 59540 B, 300 unique links, sparse ids 519–3566. Whether this is the whole publication record or a first page capped at 300 is not checked [INFERENCE: a round number suggests a page cap]. "The whole record" is unproven.
4. S404 says "nine entries around the spider entry" — two (3453, 3454) share one title; the set includes non-crawl notices; not a defect, just the measured scope.

**Is "evidence path missing from the lane" a valid reject reason?** As a literal fact yes (`test -e` absent). As a policy it is weak: the lane registry already carries own-work rows citing paths outside the lane (e.g. `corpus/SOURCES.md` S129/S130 cite `/home/vgpnk/Projects/shokunin/tameshi-shokunin/…` and `…/kama-shokunin/…`; 6 own-work rows exist). The difference is that S129/S130 cite absolute readable paths; S404/S414 cite relative campaign paths that resolve only under another repo, and their recheck commands cannot execute in the lane. State the reason that way.

## S358:

**Staged file** `ollama-openapi-contract.md` line 5: `ground: adjacency — kama owns local model-serving endpoints; this entry holds the vendor contract that lane's runtime calls, not the endpoint`. Source (line 2): `raw.githubusercontent.com/ollama/ollama/efe43c55…/docs/openapi.yaml` § paths → /api/chat. Claim: the OpenAPI spec is the field-level source of record and ahead of the legacy reference (term counts: logprobs 11/0/33, top_logprobs 3/0/11, think 25/11/30). It is a comparison of two documents in a GitHub repo; "No endpoint was contacted" (line 38).

**PROVINCE lines** (confirmed by reading):
- `kake-shokunin/PROVINCE.md` line 3: `Domain: web properties & publishing — scopes ds4cc.com, kimi.page/pro mirrors, Pages deploys`; line 6: `Refuses: anything outside this domain; report cross-domain evidence back to the orchestrator`; line 41 (Adjacent): `kama owns local model-serving endpoints; kake owns remote web properties.`
- `kake-shokunin/PROVINCE.md` lines 347-349 (Round-49 section): "The Ollama OpenAPI staged row was refused as kama's province." — a prior refusal of the same staged row, so a precedent exists.
- `kama-shokunin/PROVINCE.md` lines 3-4: `Domain: local model serving & endpoint health — local LLM endpoints, baseURL drift, served-model reconciliation, probe conventions`; line 40 `Refuses: model quality/eval (kengaku), credential material & auth flows (kagi) …`.
- kama's PROVINCE names no vendor-spec surface and no "Ollama" (grep of `ollama|openapi|vendor|upstream` there: empty). But kama's own registry already holds the same vendor docs at the same commit: `kama-shokunin/corpus/SOURCES.md` S009–S013, S025, S031 (S025 cites "Ollama API docs source commit efe43c5561047d8baf8c862730b2151249d…"). Kake's registry has zero Ollama rows (`grep -c -i ollama` = 0).

**Verdict on "PROVINCE reject":** yes, supportable, but the precise basis is kake's own domain/Refuses lines (3, 6) with line 41 as the adjacency pointer — the entry is about a model-server vendor's API spec, not a web property or publishing surface. Line 41 alone assigns *endpoints* to kama, not vendor documentation; kama's PROVINCE does not literally claim the vendor spec, so do not write "kama's PROVINCE lists this" — write what kake's lines say. [INFERENCE for the kama-lane-holds-it point beyond S009–S031.]

## DECISIONS:

Reject reason texts (each tied to the sentence/file read against it):

1. **S404 (`baidu-series-has-no-rendering-section.md`)** — "Rejected: its `source:` line (line 2) and `recheck:` (line 4) cite `lanes/kake/round15/.evidence/baidu_series_sweep_r15.txt` and `lane_sweeps_r15.sh`, which are not paths in this lane (`test -e` absent under kake-shokunin; they exist only under /home/vgpnk/Projects/shokuknow/lanes/kake/round15/.evidence/, where I re-counted the nine bodies and got 渲染=0, JavaScript=0). The lane cannot re-run the recheck command, and the claim is a negative one ('no article body mentions rendering') over nine fetched pages; the method text says script/style blocks were stripped but the sweep only deletes the opening tags." Supporting side fact: "the nine counts reproduce offline; no objection to the measurement."
   **Flip:** the evidence file, the nine raw bodies and a lane-resident recheck script are committed inside kake-shokunin (or cited by absolute readable path with a rechecker that runs from the lane), or the lane re-fetches the nine ids and re-counts into a lane path; and the stripping sentence is corrected to what the sed does.

2. **S414 (`baidu-wiki-publication-map.md`)** — "Rejected: `source:` line 2 and `recheck:` line 4 cite `lanes/kake/round16/.evidence/wiki_map_r16.txt` and `lane_sweeps16.sh`, absent in this lane (exist only under shokuknow; offline re-count there reproduces 300 index entries and 渲染/执行 = 0/0, 2/0, 6/0, 0/0 for wiki 963/990/1021/867). The title and body claim 'three hundred announcements, not one says' but four announcements were read; the 300 count comes from one index page and is not shown to be the whole record; announcement 1021 says 'avoid JS loading' (JS), which the 'mentions JavaScript' tally does not count."
   **Flip:** same as S404, plus either (a) retitle/scope the claim to the four announcements read, or (b) read all 9 crawl/agent-titled entries and show the index is complete (no pager/next page), and count 'JS'.

3. **S358 (`ollama-openapi-contract.md`)** — "Rejected as outside this lane's domain: PROVINCE.md line 3 (`web properties & publishing`) and line 6 (`Refuses: anything outside this domain`), with line 41 (`kama owns local model-serving endpoints; kake owns remote web properties`) naming the adjacent owner. The page read (`ollama-openapi-contract.md` lines 2, 5, 37-38) is a vendor API spec comparison for a local-model runtime, 'No endpoint was contacted'; kama's registry already carries the same Ollama docs at commit efe43c55 (kama `corpus/SOURCES.md` S009–S013, S025, S031). Same disposition as the round-49 refusal recorded at PROVINCE.md lines 347-349."
   **Flip:** kake gains a web-publishing consumer that must cite the Ollama spec (e.g. a kake-owned Pages deploy that documents or proxies the Ollama API), or the operator widens kake's domain line 3, or kama declines the row and the orchestrator reassigns it. Absent those, forward the staged file to kama rather than re-staging it in kake.

VERDICT: S404/S414 evidence exists only under shokuknow (absent in lane, offline re-count reproduces) so reject as "not lane-resident/recheck cannot run in lane" plus S414 overclaim; S358 is a defensible domain/PROVINCE reject via kake PROVINCE lines 3, 6, 41 (not via kama PROVINCE text), with the round-49 precedent at lines 347-349.
