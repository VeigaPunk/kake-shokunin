# MetadataCheck — corpus-contract.mjs gate implementation

Seat: KakeR21.MetadataCheck · wave r21/w1 · scope: `scripts/corpus-contract.mjs` (new file, only target)

## Files changed

- `scripts/corpus-contract.mjs` (new, 610 lines) — zero-dependency, read-only Node ≥18 CLI gate.

## Behavior contract implemented

- Checks `corpus/knowledge/*.md` under `--root` (default = script's parent dir, the lane checkout; `--root .ufo/waves/round-21/frozen/before` style frozen roots work unchanged — only `corpus/knowledge` + `corpus/lessons` are consulted).
- Provenance trio `source:` / `verified-at:` / `recheck:` required non-empty within the FIRST 8 lines of each knowledge `.md`. Matching is strictly per-line (`[ \t]` whitespace never crosses a line break; bare `source:` followed by a `verified-at:` line does NOT satisfy `source` — reviewer-driven regression pinned by fixture `bare-then-key.md`). ≤3 leading spaces and any case tolerated; `.json` and non-`.md` files never enumerated.
- Lane-author lessons = exact basename `/^round-\d+(?:-recensus)?\.md$/`. Gate = a non-empty level-2 `## Gate` ATX section; `## Gate — …` suffix subtitles accepted (all 15 scribe outputs observed, e.g. `## Gate — round-21 retrospective reconstruction`); `### Gate`, `##Gate`, `## Gatekeeping`, and `## Gate` inside fenced code rejected. A second `## Gate` heading restarts the section so existence of ONE non-empty section is the verdict.
- Exclusions: knowledge basenames containing `verifier`/`aggregator`/`operator` (case-insensitive) → `excluded-name`; lessons basenames failing the lane-author regex → `not-lane-author` (this already excludes every `-aggregator-*`/`-verifier-*` lesson; the basename test is applied to lessons too, as belt-and-suspenders). Skipped files are reported under `skipped`, never as findings.
- Finding IDs embed paths for replay grep-ability, per L1 relay: `missing_metadata:<file>:<field>` (one finding per missing field, ordered source → verified-at → recheck per file) and `missing_gate:<file>` (exactly one per offending lesson; `detail` = `no-gate-section` | `empty-gate-section`).
- Exit contract: `0` clean · `1` findings · `2` could-not-evaluate (unreadable/missing corpus dirs or files; outranks findings) · `64` usage (unknown flag, bare/empty `--root`).
- `--json` emits `{tool,contract,root,ok,code,counts,findings,skipped,errors}` — fully deterministic: sorted findings/skips/errors, fixed key order, no timestamps, replay-stable.
- Human mode prints `FAIL <id>` / `SKIP <reason> <file>` / `ERROR <file>` lines plus a `result:` summary.

## --selftest

Hermetic `fs.mkdtempSync` fixture roots under `os.tmpdir()`; every fs write call in the file sits inside `SELFTEST-WRITES-BEGIN/END` marker pairs in `selftest()` only. Eight cases, expected outputs persisted as `EXPECTED_CLEAN` / `EXPECTED_FAIL` / `EXPECTED_BARE` literals compared byte-for-byte via `JSON.stringify`:

- c1 clean root: exit 0, zero findings, 5 excluded basenames pinned — covers positive trio variants (case, spaced colon, indented labels, line-8 boundary) and positive gate variants (suffix subtitle, `###`-only content).
- c2 failing root: exit 1, all 18 pinned composite-id findings — covers malformed/empty metadata, bare-label-then-next-key regression, trio past the 8-line window, empty/fenced/wrong-level gate sections, exclusion negatives.
- c3 human mode same exit contract (1).
- c4 bare corpus dirs: vacuous exit 0.
- c5 absent root: exit 2, exactly errors `[corpus/knowledge, corpus/lessons]`, no findings.
- c6 usage: `--bogus`, bare `--root`, `--root=` all exit 64.
- e1 write-confinement: own-source scan proves zero fs-write calls outside markers, markers provably inside `selftest()`, synthetic positive/negative scanner controls pass. Control probe strings are built by concatenation so they stay invisible to the scanner itself.

## Baseline measured (not exercised, static counts at authoring time)

`corpus/knowledge` = 21 `.md` files (+`freshness-pins.json` skipped by extension) — at authoring time all sampled entries carried the trio; `corpus/lessons` = 15 lane-author files (`round-{1,3,4,5,6,7,8,9,10,12,16,17,18,19-recensus,20}.md` plus `round-21.md` appearing during the wave) + 9 excluded audit/verifier files. `round-18.md` was the last lesson pending a Gate append.

## Limitations / risks

- Per assignment: not executed — no `--selftest` run, no `node --check`. L1 exercises once after landing. Logic was reviewed statically; residual risk is concentrated in `gateStatus` fence tracking (`~~~` vs ```` ``` ```` toggle) and `split(/\r?\n/, 8)` truncation semantics (verified correct for LF/CRLF).
- Gate check is shape-only per the C2 contract (heading + any content line); fabricated-admission review belongs to other seats.
- Basename `verifier|aggregator|operator` exclusion is substring-based; a future lane-authored name containing those substrings would be silently skipped (reported under `skipped`, so visible).
- Confinement scanner residuals (documented in-file): aliases, bracket access, split calls, fd-level writes, `execFileSync` side effects.
- Header cites "S019" as the contract name used across scribe prompts; L1 owns canonical registration in CORPUS.md.
