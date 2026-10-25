# CriticProvince — staged `ollama-openapi-contract.md` refusal stands

Seat: CriticProvince (critic, adjacency). Read-only except this report. No staged bytes copied; no production file, fleet repo, or sibling lane touched.

## Question

Is the staged entry `ollama-openapi-contract.md` (S321) in kake's province, what is the flip condition, and is the round's refusal of it correct?

## Verdict

**Not in kake's province. The refusal is correct and is repeated for round 50.**

**Flip condition (unchanged):** admit only if the operator amends kake's `PROVINCE.md` so kake owns the Ollama API surface, or if `kama` releases that surface. Neither holds on the files read this turn.

## Path note

The item prompt named the staged entry at `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/ollama-openapi-contract.md`; that path does not exist. The file actually sits one level deeper at `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/ollama-openapi-contract.md`, and that is the file read. Same name, same S321 source line, same content the round-49 scout verdict quoted — the verdict binds to the content, not the path.

## Binding lines

Staged source line, `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/ollama-openapi-contract.md:2`:

`source: S321 — https://raw.githubusercontent.com/ollama/ollama/efe43c5561047d8baf8c862730b2151249d51fd5/docs/openapi.yaml — § paths → /api/chat (repository state at commit efe43c55, 2026-10-06) — fetched 2026-10-24`

Staged `ground:` line, same file `:5`:

`ground: adjacency — `kama` owns local model-serving endpoints; this entry holds the vendor contract that lane's runtime calls, not the endpoint`

Kake Adjacent, `PROVINCE.md:41`:

`- `kama` owns local model-serving endpoints; kake owns remote web properties.`

Kake domain line, `PROVINCE.md:3`: `web properties & publishing — scopes ds4cc.com, kimi.page/pro mirrors, Pages deploys`. Refuses line, `PROVINCE.md:6`: `anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it.`

Round-49 province record, `PROVINCE.md:349-350`: `The Ollama OpenAPI staged row was refused as kama's province.`

## Why the adjacency argument still fails

The staged entry's `ground:` line argues a third category: kama owns the *endpoints*, this entry holds the *vendor contract* those endpoints implement, so it can sit beside kama inside kake. That split does not survive kake's own province text.

- Kake's half of the Adjacent sentence is **remote web properties** — the hosts kake serves or mirrors. A commit-pinned `docs/openapi.yaml` in the Ollama repository is not a remote web property of kake's; the host being `raw.githubusercontent.com` does not make the *subject* a kake property.
- The entry's own scope is `§ paths → /api/chat` — the field-level request/response contract of the local model-serving endpoints. "The contract of the endpoint" is not separable from "the endpoint" for province purposes here: kama's province is defined by exactly that surface (`kama-shokunin/PROVINCE.md:3-4` — local model serving, served-model reconciliation, probe conventions), and kama's boundary question (`kama-shokunin/PROVINCE.md:42-43`, *"is the thing at this baseURL the model this config believes it is, right now"*) presumes authority over what the endpoint's documented fields mean.
- Kama already mines this surface: `kama-shokunin/corpus/SOURCES.md` S009–S013, S025, S031 cite `docs.ollama.com/api/*` pages — and S011/S012 name the OpenAPI 3.1.0 spec behind `/api/tags` and `/api/ps` explicitly. The staged S321 is the upstream repo file those rendered pages are generated from. Kama holds the same spec already; the staged row is a duplicate authority inside a sibling's ground, not a gap kake fills.
- The staged package's own SOURCES row (`/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md:78`) calls it "a dependency reference for the fleet's shared model server, not owned ground" — the author concedes it is not owned ground; the refusal is the registry acting on that concession.

## Prior rounds agree

- Round 48 refused it; flip recorded at `corpus/lessons/round-48.md:81-85` (per `.ufo/waves/round-49/w1/ScoutOllamaProvince.md:33`).
- Round 49 refused it again: `corpus/lessons/round-49.md:14-17` restated reason and flip (`.ufo/waves/round-49/w1/ScribeRejects.md:9-10`), the round-49 scout verdict re-derived it from the live files (`ScoutOllamaProvince.md`), and `PROVINCE.md:350` now records the refusal.
- Nothing changed on the files since: `PROVINCE.md:41` still reads the same this turn; the staged bytes still carry the same S321 source line.

## Corroboration, not the test

Kama's corpus also covers the adjacent Ollama surfaces this same staged package offers (S320 legacy `docs/api.md`, S322 `docs/development.md` — `SOURCES.append.md:77,79`): kama already reasons about the runtime/build of the server it probes (`kama-shokunin/PROVINCE.md` round-16 through round-28 notes on the lane-owned llama.cpp fixture and request-field schema). A kake copy would put the vendor contract for a sibling's serving surface into the wrong lane and create two owners for the same spec.

## Instrument context (reported, not judged)

The three counting commands were run verbatim:

- `c50_quote_class.py` @ base `9619af67` → `classed 0/3 met=False` (S273, S274, S286 all fail; class ledger absent).
- `c50_quote_class.py` @ pre-append `33eec7f2` → `classed 0/3 met=False` (S273/S274 lesson absent; S286 lesson absent, no live registry row, entry absent).
- `c50_durable.py` @ base `9619af67` → `durable 0/1 met=False` (order proof, wave-cite proof, LOG citation, settlement all absent).

These are do-nothing/pre-append baselines as the contract expects; they are cited here only to show the instruments ran.

## Axis read (adjacency)

The staged entry asks kake to absorb a sibling's endpoint contract on the strength of a `ground:` line its own text contradicts. Adjacency discipline says the refusal is the correct move and the flip — operator amendment or kama release — is the only route in. No new evidence this turn opens it.

No production edit. No `jj`. No fleet write. No commit.

Report: .ufo/waves/round-50/w1/CriticProvince.md
