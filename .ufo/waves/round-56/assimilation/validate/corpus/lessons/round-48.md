# Round 48 — lesson

## Mistakes

1. **class:** landing — inherited round work left uncommitted in the lane
   working tree, including a mode-only drift on eight tracked files ·
   **evidence:** at the round start the lane working tree carried 9
   tracked-modified and 31 untracked paths; `git diff --stat` showed 8 files
   with a 0-line diff (mode 100644 → 100755: `.gitignore`, `AGENTS.md`,
   `LOG.md`, `PROVINCE.md`, `README.md`, `SCORECARD.md`, `SHONEN.md`,
   `SKILL.md`) and the ninth, `.ufo/waves/round-47/w1/swarm-registry.json`,
   with a real content change (33 insertions / 33 deletions: every member's
   `agentId` filled from `null` by the round-47 wave's own dispatch, whose 30
   seat reports are the untracked files under `.ufo/waves/round-47/w1/`) ·
   **captured-by:** none — no criterion required a respawn to disposition
   inherited lane work before its next commit · **fix:** the mode drift was
   reverted with `chmod 644` (no byte changed) and the round-47 wave evidence
   is committed under this round's entry; the eight reports under
   `.ufo/waves/round-46/residual/` are orchestrator-owned (they were
   dispatched by the orchestrator, not by this lane) and stay uncommitted and
   untouched, named in the round report as the closure's durable queue.
2. **class:** vacuous — the citation lint's resolver asked git the wrong
   question, so a dead full-40-hex citation passed the gate ·
   **evidence:** `.ufo/waves/round-46/residual/CriticCitationOverreach.md`
   Finding 1 records that `git rev-parse -q --verify
   deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` exits 0 on git 2.56.0, so
   `scripts/citation_lint.py`'s `resolves()` (line 126) treated "no such
   object" as "resolves"; the live population carries one such dead token
   (`7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` at `SCORECARD.md`, the
   ds4cc-marketplace upstream commit) that the gate accepted ·
   **captured-by:** none — the shipped selftest planted only an 8-hex dead
   token, which `rev-parse` does reject · **fix:** the resolver now asks
   whether the object exists (`git cat-file -e`), the dead full-40 token is a
   committed selftest fixture, and the C2 counter's case set carries it (the
   before measurement is 1 of 2 dead cases detected, the after measurement 2
   of 2).
3. **class:** number-drift — a staged row cannot be appended as staged ·
   **evidence:** the campaign's staged rows for this theme carry prose
   `recheck` cells (`180d — `curl …` -> 1 (ran 2026-10-23)`) and escaped
   pipes, and the lane's census parser accepts rows with 0–3 leading spaces,
   so a column-zero-only id scan misses an indented collision ·
   **captured-by:** CORPUS.md's census clause (the maintained parser's
   0–3-space tolerance) and the item-10 transformation rule ·
   **fix:** the append block was built in scratch (`.ufo/waves/round-48/
   assimilation/append-block.md`), normalized to the bare cadence `180d`, with
   the stripped re-verify conditions recorded in this lesson's Gate block;
   the id-collision check used the 0–3-space pattern and its guard was proven
   able to fail on an indented colliding row (`.ufo/waves/round-48/
   assimilation/guard-collisions`); the append was gated on a full-repo
   mirror whose census exits 0 with only the twelve pre-existing W04
   warnings.

## Gate

Theme (one): the client-rendering crawl contract — the crawl/render/index
phase boundary a publisher can act on.

**Admitted (2 entries, 4 rows).** Every row below was re-opened by the L1 in
this round; the quotes are the L1's own located quotes, not the campaign's.

- **S137** — URL: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics ; opened: 2026-10-24T20:40:31Z ; HTTP 200, 221711 raw bytes, visible-text sha256 `7f12d2f257b02fb498277925c0cc150bee6ff7ff076e1e8cccb3469b75a5cfdb` ; retained: `.ufo/waves/round-48/sources/S137.txt` ; quote: "All pages with a 200 HTTP status code are sent to the rendering queue, no matter whether JavaScript is present on the page." ; located at `S137.txt` line 216, § "Rendering".
- **S137** — second quote, same source and access: quote: "When Googlebot fetches a URL from the crawling queue by making an HTTP request, it first checks if you allow crawling." ; located at `S137.txt` line 207, § "Crawling".
- **S138** — URL: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=zh-cn ; opened: 2026-10-24T20:40:34Z ; HTTP 200, 224104 raw bytes, visible-text sha256 `e15db715242b22ec5e1ccd5cb14f0cb8d9e94bfc4d3961dfc5186eadcecbfce3` ; retained: `.ufo/waves/round-48/sources/S138.txt` ; quote: "所有具有 200 HTTP 状态代码的网页都会发送到渲染队列，无论网页上是否存在 JavaScript。" ; located at `S138.txt` line 211, §「渲染」.
- **S139** — URL: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=ja ; opened: 2026-10-24T20:40:37Z ; HTTP 200, 233866 raw bytes, visible-text sha256 `9290f969eafc865db2607d1198d813c274c9a8a6bcb670bc2ae1a4778cb87745` ; retained: `.ufo/waves/round-48/sources/S139.txt` ; quote: "200 HTTP ステータス コードのすべてのページは、ページに JavaScript が存在するかどうかに関係なく、レンダリング キューに送信されます。" ; located at `S139.txt` line 208, §「レンダリング」.
- **S249** — URL: https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering ; opened: 2026-10-24T20:40:40Z ; HTTP 200, 175284 raw bytes, visible-text sha256 `f5a9fd1f8f1d3c291f3ad45d9aeb243eb38c7fe94adaaca6babdd8d09f87c09f` ; retained: `.ufo/waves/round-48/sources/S249.txt` ; quote: "Dynamic rendering is a workaround and not a recommended solution, because it creates additional complexities and resource requirements." ; located at `S249.txt` line 205, § "Dynamic rendering as a workaround".

Stripped re-verify conditions (the staged rows' prose `recheck` cells, recorded
here because the fleet schema's `recheck` cell carries the cadence only):
S137 `curl -fsSL --compressed '…/javascript-seo-basics' | grep -F -c 'sent to the rendering queue'` -> 1 ; S138 the same page with `?hl=zh-cn` and `grep -c '渲染队列'` -> 3 ; S139 the same page with `?hl=ja` and `grep -c 'レンダリング キュー'` -> 2 ; S249 `curl -fsSL --compressed '…/dynamic-rendering' | grep -F -c 'Dynamic rendering is a workaround and not a recommended solution, because it creates additional complexities and resource requirements.'` -> 1. All four were re-run on 2026-10-24 with the fetcher at `.ufo/waves/round-48/sources/fetch_sources.py` (receipts in `.ufo/waves/round-48/sources/receipts.json`, each receipt naming the fetcher's sha256).

**Rejected (2 candidates from the assimilation set, with reasons and flips).**

- `corpus/knowledge/client-rendered-source-citation-rule.md` (staged, round 9)
  — **reason:** it states the campaign's own archive rule ("a withdrawn source
  is re-pointed at an archive that carries the content") and its cited source
  is a campaign-internal path (`lanes/kake/round9/.evidence/archive_route_r9.txt`),
  not a re-openable public source, so contract v1 rule 1 cannot be satisfied
  for it; the teaching belongs to the corpus contract, not to the lane's
  domain. **flip:** admit it if it is restated against a re-openable public
  source and scoped as publisher-side handling of a withdrawn page.
- `corpus/knowledge/ollama-openapi-contract.md` (staged, round 8) — **reason:**
  out of province. Ollama's API surface is local model serving, which belongs
  to the `kama` lane (PROVINCE.md, Adjacent); a lane may not absorb a
  sibling's domain. **flip:** admit it if the operator amends kake's
  PROVINCE.md to own the Ollama API surface, or if `kama` releases it.

**Quarantine hand-check (the kake slice of the campaign's absent-defect
register).** All 12 rows were fetched and their quotes located by the L1
(`.ufo/waves/round-48/assimilation/quarantine-handcheck.py`, receipt
`.ufo/waves/round-48/assimilation/quarantine-handcheck.json`): nine rows
(S142, S143, S148, S156, S161, S193, S194, S195, S206) came back `absent` —
the body was fetched cleanly and the registered quote is in none of the four
folds — so they are refused (fabrication class; four of them cite the lane's
own GitHub repository while quoting the lane's own prose, which is not a
source quote); three rows (S154, S178, S184) came back `unreachable`
(HTTP 404, 429 and 404), so they are unverifiable, never fabrication. None of
the twelve is a row this round appends.

**Non-author spot-check:** not run in this seat — every seat this round was
dispatched by this lane, and a seat the lane dispatched is still the lane
(LEARNING.md). The admit/reject leg above is therefore author-side only; the
outside spot-check remains owed to the closure.

**Registry changes:** rows 136 → 140 (S137, S138, S139, S249 added, mined, tier
A, opened 2026-10-24, recheck 180d). No status / recheck / used-by cell of an
existing row changed. Census exit 0 before and after the append (the twelve
W04 duplicate-url warnings are pre-existing and unchanged).

**Sourced claim:** C1 rests on S137, S138, S139 and S249 — the four rows opened
this round, cited by the two entries the claim lands.

## Wave note

Round shape: one v2 wave of 64 seats under `scripts/hyaku/ufo-wave-policy-v2.json`
(band 64–128), validated by `ufo-swarm-wave.mjs plan|run`; the L1 holds the
canonical planner seat (planner is frozen topology and is not a swarm role);
27 of the 64 seats carry an attack role (reviewer, critic, mutation-tester,
sentinel, revenger), 42 percent. Spec, registry and dispatch payload are under
`.ufo/waves/round-48/`.
