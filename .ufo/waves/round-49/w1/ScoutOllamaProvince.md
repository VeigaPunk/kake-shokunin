# ScoutOllamaProvince — staged S321 is not in province

Seat: ScoutOllamaProvince (scout). Axes: operability, freshness. Read-only except this report. The staged entry was not copied in.

## Verdict

**Not in province.** Do not copy `corpus/knowledge/ollama-openapi-contract.md` in.

**Flip:** admit only if the operator amends kake `PROVINCE.md` so kake owns the Ollama API surface, or if `kama` releases that surface. Neither holds on the files read this turn.

## Binding lines

Staged source line, `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/ollama-openapi-contract.md:2`:

`source: S321 — https://raw.githubusercontent.com/ollama/ollama/efe43c5561047d8baf8c862730b2151249d51fd5/docs/openapi.yaml — § paths → /api/chat (repository state at commit efe43c55, 2026-10-06) — fetched 2026-10-24`

Staged row S321 in `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md:78`. used-by cell: `corpus/knowledge/ollama-openapi-contract.md`. Subject: the machine-readable HTTP contract for the endpoints a fleet agent calls. URL is the same raw `docs/openapi.yaml` pin.

Adjacent, `PROVINCE.md:41`:

`- `kama` owns local model-serving endpoints; kake owns remote web properties.`

Domain line (`PROVINCE.md:3`) scopes those properties to ds4cc.com, kimi.page/pro mirrors, and Pages deploys. Refuses line (`PROVINCE.md:6`): anything outside this domain is reported, not absorbed.

## Why the adjacency split fails

The staged file's ground line (`ollama-openapi-contract.md:5`) tries to park the entry beside the endpoint: kama owns the endpoints; this entry holds the vendor contract the runtime calls, not the endpoint.

Adjacent does not grant that third thing. Kake's half of the sentence is remote web properties, not vendor contracts of a sibling's endpoints. A commit-pinned `docs/openapi.yaml` whose located section is `paths → /api/chat` is the field contract of the local model-serving endpoints. The host being `raw.githubusercontent.com` does not make the subject a property kake serves.

## Flip, still closed

Same flip as round 48 (`corpus/lessons/round-48.md:81-85`): admit if the operator amends kake's `PROVINCE.md` to own the Ollama API surface, or if `kama` releases it. Round-49 Gate restates it (`corpus/lessons/round-49.md:17`). The round-49 province step records the refuse (`PROVINCE.md:349-350`).

Corroboration, not the test: kama already mines the rendered pages this spec drives (`kama-shokunin/corpus/SOURCES.md` S009–S012; S011 and S012 cite OpenAPI 3.1.0 for `/api/tags` and `/api/ps`). Releasing the surface is kama's, and province contraction there is an L0 decision. This seat did not edit kama and did not amend kake province.

Lane corpus has no `ollama-openapi-contract.md`. No row was appended.

## Axis read

- **Operability:** a later seat can refuse the copy from the two quoted lines. Copying the staged bytes would not clear the reason.
- **Freshness:** Adjacent and the staged source line were read this turn from the live paths above, not from the lesson paraphrase. The OpenAPI URL was not re-fetched; freshness here is the province test, not the vendor document.

No production edit. No `jj`. No fleet write. No commit. Staged package not written.

Report: .ufo/waves/round-49/w1/ScoutOllamaProvince.md
