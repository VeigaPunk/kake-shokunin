# ScribeScreenBlueprintCandidate — routed item 7 (screen one non-primary Render Blueprint page)

Wave 1, Kake round 32. Leaf seat, freshness axis. Decision: **REJECT** the screened candidate at tier C. Nothing written to `corpus/SOURCES.md`.

## Candidate opened

- URL: https://flueframework.com/docs/ecosystem/deploy/render/ (title: "Deploy Agents on Render — Flue")
- Non-primary: it is a third-party framework's deploy guide, not Render's own docs; Render's vendor page for the same topic is S057 (`https://render.com/docs/blueprint-spec`, `corpus/SOURCES.md:65`).
- Access time UTC: **2026-10-22T18:59:36Z** (server `date:` header identical). Plain `curl` GET, follow redirects, no browser, no challenge. HTTP/2 **200**, 76768 bytes, `content-type: text/html`.
- Retained bytes: `/fast/scratch/hyaku/kake-r32/w1/ScribeScreenBlueprintCandidate/flue.html`, sha256 `fd5b92b2d64db8c0f710ade876f3921801e6f1b2468d46e93598f99c8ad343e8`; headers at `headers_flue.txt`; tag-stripped text at `flue.txt`.
- Page's own date line: "Last updated Jul 21, 2026" (text offset 1215 in `flue.txt`) — fresh, so age is not the reason for rejection.

## Located quote (verbatim rendered text, 17 words, ≤25)

> "To auto-deploy on every push, set autoDeployTrigger: commit on the service (this replaces the deprecated autoDeploy field)."

Location: section **Deploy**, paragraph immediately after the `render.yaml` code block; `flue.txt` offset 3178. In the source HTML the two field names are wrapped in `<code>` elements, so the sentence is not a single contiguous byte run (`flue.html`, context around "this replaces the deprecated"); it is contiguous in the page's rendered text, which is what the quote reproduces.

## Drafted row (11 cells, not written to the registry)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S063 | Flue docs: Deploy Agents on Render — https://flueframework.com/docs/ecosystem/deploy/render/ | docs | C | A third-party framework's restatement of Render Blueprint fields for its own template, read once; not Render's own specification, not a statement about any hosted service or plan, and not a source for any field S057 does not also state | Deploy section render.yaml block (type web, runtime node, plan free, healthCheckPath /health, envVars sync false) and the paragraph after it, rendered text: "To auto-deploy on every push, set autoDeployTrigger: commit on the service (this replaces the deprecated autoDeploy field)."; page states Last updated Jul 21, 2026; fetched 2026-10-22T18:59:36Z, sha256 fd5b92b2d64db8c0f710ade876f3921801e6f1b2468d46e93598f99c8ad343e8 | REJECTED: every field it states inside S057's scope (root render.yaml, type and runtime, healthCheckPath with leading /, sync: false prompted at creation and ignored on updates) is already carried by S057, and its one additive claim, that autoDeployTrigger: commit replaces the deprecated autoDeploy field, is in no tier-A row; flip: S057 or another tier-A Render vendor page documents autoDeployTrigger and the autoDeploy deprecation | rejected | 2026-10-22 | 90d | — |

Row file: `/fast/scratch/hyaku/kake-r32/w1/ScribeScreenBlueprintCandidate/s063_row.md` (sha256 `4a3a69efcc85d5d52baf1bab97ce399938487d32a07e333e79fca1242e71802f`), validated to split into 11 cells under the same `' | '` parse as all 62 existing S rows.

## Why rejected, checked cell by cell against S057

- Agreement (all four corroborate S057, none new): Blueprint is `render.yaml` at the repo root; `type: web` plus `runtime: node`; `healthCheckPath: /health` with a leading slash; `envVars` entry with `sync: false` that Render prompts for at creation and ignores when updating an existing Blueprint ("Render ignores sync: false variables when updating an existing Blueprint", `flue.txt` offset ~4400).
- The only additive claim — `autoDeployTrigger: commit` and the deprecation of `autoDeploy` — is not in S057's anchor or teaches cells, and `grep -c autoDeploy corpus/SOURCES.md` returns 0 (exit 1), so **no tier-A row in this registry states it**. Admitting it as tier C would put a field name and a deprecation status into the corpus on a single third-party page.
- The page also carries free-plan behaviour (15-minute spin-down, ~1 minute cold start, in-memory state loss) that lies outside S057's declared scope; it would need its own vendor row, not this one.
- Freshness judgment: recent and not contradicted, so the reject is on **redundancy plus an uncorroborated additive claim**, not on staleness.

## Commands run (all in the sandbox; no lane writes except this report)

1. `curl -sS -L --max-time 40 … 'https://dev.to/ayushn21/deploy-rails-and-sidekiq-to-rendercom-using-yaml-346'` → exit 0, `http=404`, 5077 bytes. First candidate was dead; recorded as unopened, not used as evidence (`devto.html`, headers `headers.txt`).
2. `curl -sS -L --max-time 40 … 'https://flueframework.com/docs/ecosystem/deploy/render/'` → exit 0, `http=200`, 76768 bytes; sha256 as above.
3. `python3` tag-strip of `flue.html` → `flue.txt` (9914 chars), counted `autoDeploy`=3, `Last updated`=1; extracted quote context (exit 0).
4. `python3` assertion that the quote is ≤25 words and pipe-free, built the row and compared cell counts against the registry → exit 0, existing counts `{11}` over 62 rows, draft 11.
5. `grep -c 'autoDeploy' corpus/SOURCES.md` → **exit 1, count 0** (no tier-A coverage).
6. `grep -rl "SOURCES.md" --include=*.mjs --include=*.py .` → no output (exit 1): the lane has no script that parses registry rows, so cell shape was the only mechanical check available.

## Not verified

- I did not open `render.com/docs/blueprint-spec`; S057's cells are taken as recorded by the L1. So "S057 does not mention autoDeployTrigger" is verified against the row text only, not against the live vendor page.
- The page's "Last updated Jul 21, 2026" is a self-declared string; no HTTP `Last-Modified` header was returned.
- I did not check whether any knowledge file already needs the free-plan spin-down claim, so that half of the flip condition is untested.
- No tools installed or updated; no pacman touched.

## Concurrent-lane observation (not mine)

At 2026-10-22T19:0xZ `git status --porcelain corpus/SOURCES.md` briefly reported ` M` with a one-line change on the S062 row; a recheck seconds later showed the file byte-identical to `HEAD` (sha256 `57b36ecbb4492ba6711d8147e88683ae32204ba9656fa73f5c17db59e8ea111c` on both working tree and `git show HEAD:`). Another live seat wrote and reverted that row; I made no edit to `corpus/SOURCES.md` at any point (all my reads used `grep`/`awk`/`python3` only).
