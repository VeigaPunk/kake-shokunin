# Round 21 · w1 · GateContract — corpus-contract gate audit

Lane: `kake-shokunin` · Seat: `GateContract` (reviewer, leaf) · Baseline revision: `5009ecaa1cce10b895617a585ddd3f7c7c923a84` (= current HEAD)

## Scope and method

Read-only audit of the proposed corpus-contract gate requirements against the canonical Gate standard. No code, no tests, no edits outside this report. Gate execution was not run (assignment: main agent verifies once after integration).

Canonical sources (read in full or by section):
- `~/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md` (blob header `#3BE2`): §Round-robin step 4 history pin (L335–338), §Evidence standard (L356–386), **§Gate standard (L388–437)**: Verdict L393–397, Self-test L398–402, Two evidences L403–410, Registry L411–419, Scope L420–424, Closure consequence L425–430, Delivery L431–437; §File contract (L439–451); §Invariants pathspec and waves rules (L485–486, L500–502).
- `~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` (header `#2838`): provenance trio L18–20 and L162–165; `## Mistakes` L166–168.
- `~/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL-APPENDIX.md` rows *Gate standard* (10, 12), *Frozen inputs* (12, 13), *Registry home* (14).
- Proposal under audit: `.ufo/waves/round-21/wave1-spec.json` entry `MetadataCheck` (line 189, raw), plus `measure.mjs` (`FrozenMeasurement`) and `anchor-census.mjs` (`AnchorCensus`) prompts, which are also in scope as second implementations.
- Lane artifacts: `SKILL.md` (registry section L208–212), `scripts/`, `.ufo/waves/round-21/frozen/before/expected.json`, `.ufo/round-20/replay-proof.mjs`, `.ufo/reports/round-20/kake.md` L162–164.

## Verified facts (observed, with command)

| # | Fact | Evidence |
|---|---|---|
| V1 | `scripts/corpus-contract.mjs` does **not** exist. `scripts/` holds `freshness-sweep.mjs` and `probe-delta.mjs` only. | `ls scripts` |
| V2 | Frozen baseline `expected.json` pins **36** input digests (21 knowledge + 15 lessons). All 36 match both the frozen copies and `git show 5009eca:<path>`. Zero exceptions. | node sha256 check over `expected.json.inputs` |
| V3 | Baseline counts are true at `5009eca`: knowledge md 21; provenance trio nonempty in first 8 lines 4; lane-author lessons (`^round-\d+(-recensus)?\.md$`) 15; `^## Gate$` heading present in 1 (`round-20.md`). `expected.json` states `21 / 4 / 15 / 1`, `expected_exit: 1`. | `git ls-tree` + `git show` parse |
| V4 | `.ufo/waves/` is **untracked** (`?? .ufo/waves/`) and not gitignored (`git check-ignore` rc=1). The frozen baseline is therefore not yet durable evidence. | `git status --short`, `git check-ignore -v` |
| V5 | The round-20 precedent (`.ufo/round-20/frozen/citation-locality/`) **is** tracked. That path lies outside the `.ufo/waves/*/frozen` root the Registry names. | `git ls-files .ufo/round-20/frozen`; PROTOCOL L418 |
| V6 | Live worktree is **dirty** relative to the baseline: 32 status entries (17 `corpus/knowledge`, 12 `corpus/lessons`, 2 `corpus/` top-level, 1 `.ufo/waves`). Sibling scribes are writing now. A live-tree run today does not measure `5009eca`. | `git status --short`, `git diff --quiet 5009eca -- corpus/...` (both nonzero) |
| V7 | Lane `SKILL.md` already carries the owned registry: header `### Owned freshness gate registry` (L208) with the 8-column schema and a `freshness-sweep` row (L212). It is the precedent for the child-lane registry home. | `grep -n` on `SKILL.md` |
| V8 | Round-20 replay precedent: `replay-proof.mjs` checks every `expected.inputs` digest first, emits `snapshot_tampered` on mismatch (L19), and pins the baseline script digest (L25–26). | `read` `.ufo/round-20/replay-proof.mjs` L13–26 |
| V9 | Round-20 report already records that a green selftest is not a complete write-free proof, and that the prior confinement check was a static self-source scan. | `.ufo/reports/round-20/kake.md` L162–164 |
| V10 | The `expected.json` has no finding IDs, no gate argv, no gate script digest, and no `name`. | `read` `expected.json` L1–46 |
| V11 | The `wave1-spec.json` proposal says "exit0 clean/1 failed/2 could-not-evaluate/64 usage" and "stable missing_metadata and missing_gate IDs". It says nothing about `revision`, `snapshot_tampered`, `unpinned (legacy)`, the registry row, or the frozen replay. | `wave1-spec.json` L189 raw |

Noted hazard (not used as evidence): unscoped grep under `.ufo/` returned fragments of `.ufo/interactive-sessions/` transcripts. Those files were not opened, cited, or committed, and nothing from them is relied on here.

## Findings, severity-ordered

### F1 — HIGH — Registry home is `SKILL.md`, not `SCORECARD.md`, and no row exists
- Standard: a child lane's registry home is its own `SKILL.md`. The `SCORECARD.md` split at `## Aggregator lane` applies only to main-repo lanes (PROTOCOL L411–416; appendix row *Registry home*, round 14).
- Closure: a gate is not conformant until its registry row exists at that home (L431–435).
- Fact V7: the row must go under `SKILL.md` L208 next to `freshness-sweep`.
- Constraint: `SKILL.md` is L1-owned in this round. The row is a required L1 landing; this seat does not edit it.
- Required row fields (PROTOCOL L414–416): name · `gate|probe` · entry command · verdict map · self-test command and spelling · pinned-value path · write scope · owner.

### F2 — HIGH — Proposal omits revision binding
- Standard: "A verdict names the revision it was measured against … a run over a moving worktree is not comparable to one over the cited commit" (L403–407).
- Proposal: no `revision` field, no tree-state field, no `--revision` mode. `measure.mjs` has `--revision` through `git ls-tree`/`git show`, but it is a second, unregistered counter (see F5).
- Given V6, any live verdict taken now is not comparable to `5009eca`.

### F3 — HIGH — Frozen baseline is untracked, so it is not evidence yet
- Standard: drift pins count only when persisted inside the repo (L383–386). A gate that depends on a mutable artifact ships a committed input snapshot with a committed expected verdict (L403–405).
- Fact V4: `.ufo/waves/round-21/frozen/before/**` and `expected.json` are untracked.
- Protocol: `.ufo/reports/`, `.ufo/waves/`, and prompts are committed with the round's integration commit (L485–486). Commit must be pathspec-limited (L500–502), never `add -A`.

### F4 — HIGH — Baseline does not pin what the gate must emit
- Standard: the frozen run asserts exit code and stable finding IDs (L398–402), and `expected.json` pins digests of every input before comparison (L408–410).
- Fact V10: `expected.json` pins counts only. A gate could emit the wrong IDs and still match.
- Missing from the baseline: `findings` (sorted IDs), gate argv, gate script SHA-256 (precedent V8, `baselineScriptSha256`), and `name`.
- Hazard: editing `expected.json` after first measurement is a hand edit of a baseline. Add the new keys in the same integration commit, before any compare is recorded, and state in the report that the pre-commit state was never measured against.

### F5 — HIGH — Replay mechanism is undefined; `snapshot_tampered` and `unpinned (legacy)` are not handled
- Standard: the gate verifies snapshot digests before comparing verdicts. An edited snapshot is `snapshot_tampered` (could-not-evaluate). A baseline without digests is `unpinned (legacy)` (L408–410).
- Proposal: no compare mode, no digest verification, no mapping of these two states.
- Precedent: `replay-proof.mjs` (V8) does digest-first, then compare. Copy the order, not the file.
- Two implementations exist in the spec: `corpus-contract.mjs` (MetadataCheck) and `measure.mjs` (FrozenMeasurement). Standard: "a tool that cannot fail is a probe, and is registered as one" (L391–392). Pick one: either fold `measure.mjs` into the gate or register it as a probe. Do not ship both unregistered.

### F6 — MEDIUM — Verdict map and self-test are under-specified
- Verdict: `0` clean, `1` failed, others declared and mapped to `clean | failed | could-not-evaluate`; undeclared codes read as could-not-evaluate (L393–397). Proposed: `2` and `64`. Must also map `snapshot_tampered`, read errors, and `unpinned (legacy)` into the declared set. Use `2` for those; declare each in the row.
- Self-test: must invoke the CLI as a subprocess over isolated temp fixtures (no network, no live-tree write). Expected exit and expected finding-ID set are literal, committed, and independent of the recomputation. "Helper-only" self-check does not satisfy (L398–402).
- The proposal says "Persist expected fixture outputs in script" — acceptable only if the literals are not generated by the function under test.
- Required cases (both polarities): exclusion of verifier/aggregator names; trio present but empty value; trio on line 9 (outside first 8); missing `recheck:`; `## Gate` with and without the exact heading; unanchored name rejected; `snapshot_tampered` fixture; `unpinned (legacy)` fixture; usage error → 64.
- Isolation: set `HOME` and temp dir to fresh temp paths; record variable names only, never values (freshness precedent, SKILL.md L212).

### F7 — MEDIUM — Write confinement must be runtime, not static
- V9: the round-20 static self-source scan was judged insufficient. Confinement proof = digest the lane tree before and after the normal run and the selftest, and assert no change outside the temp root. Do not rely on scanning the script's own source for write-API names.

### F8 — MEDIUM — Gate naming and scope overstate what is checked
- The trio check verifies presence and non-empty values in the first 8 lines. It does not verify source truth or the `verified-at` date (HistoricalDate and GateTruth concerns). Output and registry text must say "structure/presence", not "verified".
- `## Gate` heading presence does not show admits or rejects. Rename `gates_complete` (in `expected.json` and output) to `gate_section_present` so the number is not read as quality.
- Scope: read only `corpus/knowledge/*.md` and `corpus/lessons/round-N(-recensus)?.md` (basename-anchored). Never traverse `.ufo/interactive-sessions/`, `*.jsonl`, or any credential/auth path. Never touch publishing surfaces (PROTOCOL L420–424).

### F9 — LOW — Round-20 frozen path is outside the Registry name root
- V5: `.ufo/round-20/frozen/…` is not under `.ufo/waves/*/frozen`. Do not reuse that location for the round-21 pattern; keep `.ufo/waves/round-21/frozen/before`.
- A bare name `before` currently resolves uniquely under `.ufo/waves/*/frozen` (checked), but use an explicit name (for example `round-21/before`) to stay fail-closed if another wave adds a `before`.

## Integration checklist (ordered)

1. **Single gate.** Create `scripts/corpus-contract.mjs` (zero deps, read-only normal path). Flags: `--json`, `--selftest`, `--root DIR` (default lane), `--revision SHA` (git object read, no working tree). Usage header in code.
2. **Population.** `corpus/knowledge/*.md` (21 at baseline). `corpus/lessons/` matched by `^round-\d+(?:-recensus)?\.md$` on basename (15 at baseline). Excluded: `round-20-verifier-spotcheck.md`, every `round-*-aggregator-*`.
3. **Finding IDs.** `missing_metadata:<relpath>:<field>` and `missing_gate:<relpath>`. Sort by ID. Stable across runs.
4. **Verdict map** (declare in registry row): `0=clean`; `1=failed` (any finding); `2=could-not-evaluate` (unreadable root, `snapshot_tampered`, `unpinned (legacy)`, revision not found); `64=could-not-evaluate` (usage).
5. **JSON output.** Include `revision` (HEAD or `--revision` SHA), `tree` (`clean` | `dirty` from `git status --porcelain` on the scanned root), `gateSha256`, `root`, `findings` (sorted), `counts` (`knowledge`, `metadata_complete`, `lessons`, `gate_section_present`), `exit`. A dirty tree is labelled, never silently compared.
6. **Selftest.** `--selftest` only: `mkdtemp` fixtures, subprocess invocation, literal expected exit and finding-ID set, cases per F6. Confinement by before/after digest of the lane tree (F7). Record `HOME`/`TMPDIR` names only.
7. **Replay.** Digest-first: verify all `expected.inputs` digests under the frozen root; any mismatch → `snapshot_tampered`, exit 2, no comparison. Then run the gate with `--root` on the frozen root and compare exit and `findings` to `expected.json`. Missing `inputs` → `unpinned (legacy)`, exit 2.
8. **Baseline update (before first commit).** Extend `.ufo/waves/round-21/frozen/before/expected.json` with `name`, `command` argv, `gateSha256`, `findings` (ID list from the replay run). Keep the existing 36 `inputs` and count keys byte-identical. Do this in the integration pass, before the first recorded compare.
9. **Commit the baseline.** `git add` pathspec-limited to `.ufo/waves/round-21/frozen/before/` and `.ufo/waves/round-21/w1/`, in the round commit. Never `add -A`. Pre-commit state is not evidence until committed.
10. **Registry row (L1 lands, `SKILL.md` L212 neighbour):**
    `| corpus-contract | gate | \`node scripts/corpus-contract.mjs --json\` (lane root); frozen replay \`node scripts/corpus-contract.mjs --root .ufo/waves/round-21/frozen/before --json\` | \`0=clean\`; \`1=failed\`; \`2=could-not-evaluate\` (unreadable root, snapshot_tampered, unpinned legacy, revision missing); \`64=could-not-evaluate\` (usage) | \`node scripts/corpus-contract.mjs --selftest\`; caller isolates HOME and TMPDIR; variable names only | \`.ufo/waves/round-21/frozen/before/expected.json\` (36 input digests; revision 5009ecaa1cce10b895617a585ddd3f7c7c923a84) | read: \`corpus/knowledge\`, \`corpus/lessons\`; write: temp dirs in selftest only | kake-shokunin |`
11. **Resolve `measure.mjs` / `anchor-census.mjs`.** Either fold into the gate or register as probes. Do not leave unregistered counters in `.ufo/waves/`.
12. **Live run gate (after the tree settles).** Current tree has 32 dirty paths (V6). Run `--json` only when `tree=clean` and `revision` equals HEAD. Until then record the live run as not comparable.
13. **Closure consequence.** Red result (baseline expects 1) is a conformance defect, routed to the owner, status-neutral unless the round already prescribes `failed` (L425–430). It must not mark a lane `failed`.
14. **Delivery.** The corpus-contract rule reaches lanes through the re-read duty (L431–434). The integrator names the exact `lane_prompt()` addition in its round report.
15. **Verification by main agent (once, after integration).** Run `--selftest`, the frozen replay, and one `--json` live run with `tree` recorded. Compare the replay against `expected.json`. Do not run per-seat.

## Residual risk and gaps

- Gate script and expected finding IDs do not exist yet. Every statement about the gate's behaviour above is a requirement, not an observation.
- `measure.mjs` and `anchor-census.mjs` are described in the spec only; they are not in the tree.
- The 36-input digest check covered snapshot inputs, not the 17 knowledge files and 12 lessons modified in the live tree (V6); those edits do not affect the frozen baseline.
- Unpinned-legacy mapping to `could-not-evaluate` is my recommendation for the verdict map. It is a lane decision (L1) and should be stated in the registry row.
- Trio truth, `verified-at` date truth, and gate-section quality are out of this gate's reach and must be labelled as such.
- I did not inspect any credential or auth file, did not open `.ufo/interactive-sessions/` bodies, and did not run the gate or selftest.

## Tool log

- No installs or upgrades in this seat. Existing tools used: `node`, `git`, `jq` (`~/.local/bin/jq`, pre-existing), `sha256sum`.

## File changes

- Created: `.ufo/waves/round-21/w1/GateContract.md` (this report) under `/home/vgpnk/Projects/shokunin/kake-shokunin`.
- No other files written. No commits. No changes to `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `README.md`, or `SKILL.md`.
