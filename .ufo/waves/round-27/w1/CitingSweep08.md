# CitingSweep08 — blind citing-set data-walk (2 files)

Seat: KakeR27.CitingSweep08 (leaf, read-only). Milestone r27-full-citing-set; axis freshness.
Targets: `corpus/knowledge/keeper-timer-inert.md`, `corpus/knowledge/kimi-subpath-audit.md`.
Measured revision `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations
`be375d90afc6fc7aca369ab3cf5247bf460aeed2` (HEAD at measurement).
`git diff --name-only base..HEAD -- corpus/knowledge` is empty and `git diff -- corpus/...` is
empty, so both files are byte-identical at frozen base, declarations commit, and working tree.

## Verdict (facts first)

- **Inherited-32 citing pairs contributed by this slice: 0.** Neither file contains any
  literal, grouped, range, or alternate reference to any of the 32 inherited rows
  (S001–S034 minus S014/S019); the only S-id present in either file is S019, outside that
  population.
- **Only S-id in either file: S019** (own-work row, excluded from the inherited population by
  construction). Two out-of-population references, recorded separately below.
- **No additional obligation to name.** No valid inherited32-row pair exists in these two files
  that could be missing from the frozen 57; the frozen parser and my manual census both return
  the empty set for these files.
- Parser reproduction matches `c1-before.json` exactly: population 32, citingPairs 57,
  decided 41, missing 16 (identical list), exit 1.

## Method (census before any parser/oracle comparison)

1. Read both files end-to-end (187 + 100 lines). Hand-enumerated every source-id form in every
   surface: `source:`/`verified-at:`/`recheck:` headers, body citations, fenced `text` blocks,
   inline HTML `<!-- r18 re-census -->` comments (keeper L15, L18, L25, L52, L97, L118, L163),
   and EOF notes.
2. Re-scanned with three independent patterns: frozen literal `\bS(\d{3,})\b`; frozen range
   `\bS(\d{3,})\s*(?:[-–—]|\.\.|to|through)\s*S(\d{3,})\b`; loose alternate
   `(?i)\bS[\s_-]?\d{2,}\b` (would catch `S-019`, `S 019`, `S_019`, 2-digit forms).
3. Only then replicated `count_c1.py`'s pair construction at base, listed all 26 knowledge files'
   pair sets, and diffed against my census, `c1-before.json`, and the 16 frozen missing pairs.
4. Cross-checked `c2-oracle.json` expectedPairs set-equality against the 16, and confirmed
   `scripts/citing_set.py` is absent at HEAD (C2 not yet integrated; no C2 verdict claimed here).
   No source/public-site evaluation was performed (out of scope by ticket).

No LSP server is meaningful for a Markdown source-id census; the regex/parser contract is the
frozen instrument, so grep results below are literal-census evidence, not semantic proof. No
tool installs or updates were made.

## Manual census — every reference occurrence

`corpus/knowledge/keeper-timer-inert.md` — 187 lines, 15,666 bytes,
sha256 `3863e4283dff1a7079c7525b8fa6e964f44e7092a745c15e087e5d0a2f18b916`.

| Line | Form | Ids | Scope |
|---|---|---|---|
| 1 | literal | **S019** | `source:` provenance header; “Metadata authority only: S019 in corpus/SOURCES.md, not current service-state verification.” (10-word quote) — metadata authority, explicitly *not* a live service-state claim |
| 2 | none | — | `verified-at:` header (2026-09-28T22:18Z capture, r13 re-read; historical-not-live-reverified) |
| 3 | none | — | `recheck:` header (unit files absent after 2026-10-12 prune; operator restore-or-retire) |
| 15,18,25,52,97,118,163 | none | — | inline HTML r18 re-census comments; merge-checked across multi-line comment spans, no S-token |
| 20–175 | none | — | body: Verbatim state (20), Consequence chain (61), What still works (108), r5 correction (124), operator decision (137), r13 addendum (157) — artifact paths only (`ops-automation.md:8-19`, `SKILL.md:58-61/68-75/159-172`, `fleet.config.json:256`, `src/cli.mjs:932`, `src/fleet.mjs:7-11`, `.ufo/l0-questions.md`), no S-id |
| 176–187 | none | — | EOF `## Live re-verification — round 23`; claims `keeper-timer-inert:c1`–`c8` carry surfaces and corrections but no source-id token |

`corpus/knowledge/kimi-subpath-audit.md` — 100 lines, 7,005 bytes,
sha256 `6fe588f8c35f15fa28085665be290a4ca3747abc882ff0e9d5d606b34c767fec`.

| Line | Form | Ids | Scope |
|---|---|---|---|
| 1 | placeholder only | — (`S###`) | `source:` header; “no SOURCES.md S### row” (4-word quote) — explicit negation of an S-row for this own-work baseline; `#` is not a digit and the frozen literal regex correctly does not enumerate it |
| 2 | none | — | `verified-at:` header (2026-09-28 ~21:15Z baseline, sitemap rev f3d2ecd) |
| 3 | literal | **S019** | `recheck:` header tail; “… or retire this recheck; metadata contract S019” (13-word quote) — metadata contract scope |
| 5–91 | none | — | body: link sweep, parity tables, `dir/` 404 finding, procedure recipe; artifact/file tokens only (`fleet.config.json`, `kimi_audit.py`, `/tmp/kimi-subpath-audit.json`), no S-id |
| 92–100 | none | — | EOF `## Live re-verification — round 23`; claims `kimi-subpath-audit:c1`–`c5` with surfaces/corrections, no source-id token |

Negative evidence, both files combined:

- Grouped lists (`S011, S012`-style): none.
- Ranges (`S001–S006`, `S001..S006`, `S001 to S006`, `through`): none; range-count 0 in both.
- Alternate forms (`S-019`, `S 019`, `S_019`, 2-digit ids, full-width digits): none; loose scan
  returns `['S019']` per file and nothing else.
- EOF notes: neither file has a `Round-26 source recheck` append note (0 matches for
  `round-26`/`round 26`); their EOF sections are round-23 re-verification blocks with no ids.
- Broad token scan `S[^A-Za-z0-9]{0,2}[0-9]{2,}` returns only `S019` per file.

## Parser comparison (performed after the census)

`python3 -B .ufo/waves/round-27/count_c1.py --root . --revision \
83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba` → exit 1;
`population 32, citingPairs 57, decided 41, r26CarriedPairs 41, newDecided 0, missing 16`.

- Reproduced missing list is **set-identical** to `c1-before.json` (`af55d0a4bb1aa9b21bc2ce02
  6035beaf21e523458661252f8a520008f2ec6e3c`): 16/16, no target rows, no extra/missing rows.
- Script identity (freshness): the frozen counter was observed in two byte states during this
  seat — HEAD blob `a1e46d19…` (the content first read here) and a later working-tree state
  `7ebb3f36…` that adds a `c1-before.json`-derived minimum-obligation guard plus a `--selftest`
  hook (alongside new untracked `oracle_selftest.py`; `c2_count.py` likewise gained a 2-line
  selftest hook, `93f39b0f…` → `e5b6fa7f…`). Both copies were executed at the frozen revision:
  outputs deep-equal (32/57/41/16, identical missing list, exit 1), so the conclusion does not
  depend on which copy ran.
- Independent recomputation of the pair set from all 26 knowledge files at base: 57 distinct
  pairs, sorted-set sha256 `8a66fa36aaee0298f1f279ff92df6e73ba71884db8dc5c620f68450c14932279`.
  Per-file pair sets for the targets are `[]` and `[]`; neither filename occurs in the 57.
- `c2-oracle.json` (`1d038205473180c7cb57895c2d480a8b52debe3bf08ab0a2f58ca7b1f67bc7dd`)
  expectedPairs is set-identical to the 16 missing pairs (16/16, no symmetric difference), and
  contains no target row. `scripts/citing_set.py` absent at HEAD — observed state only.
- So parser, manual census, `c1-before.json`, and the frozen C2 oracle agree on this slice:
  contribution 0, and no silent shrinkage is possible because the denominator here is empty.

## Pairs named for the record

In inherited-32 population: **none** (empty set, not an omission).

Outside the inherited population (recorded separately, NOT counted in 57/16):

1. `(S019, corpus/knowledge/keeper-timer-inert.md)` — L1, `source:` header, metadata-authority
   scope only.
2. `(S019, corpus/knowledge/kimi-subpath-audit.md)` — L3, `recheck:` header, metadata-contract
   scope.

If L1 ever widens the population to all SOURCES rows, these two pairs are the exact seeds from
this slice (57 → 59 citing pairs; both undecided unless adjudicated). A read-only repo-wide
scan (outside my two-file scope, supplied only as monotonicity context) finds **18** such
out-of-population pairs across knowledge files at base: S014 ×1 (`freshness-sweep.md`),
S019 ×16 (the two here plus `drift-detection`, `fire-journal-codes`, `fleet-registry`,
`free-read-verbs`, `freshness-sweep`, `ghp-subpath-spotcheck`, `mirror-pitfalls`,
`ops-automation`, `origin-repos`, `probe-delta-alerting`, `publish-channels`, `publish-queue`,
`speedrun-pipeline`, `vault-properties`), S035 ×1 (`accessibility-review-packet.md`).
That scan uses the same frozen regexes and is not a re-audit of those files.

Registry note (freshness, not a C1 pair): both files cite S019 as metadata authority, but the
S019 row's `usedBy` cell (`corpus/SOURCES.md:27`) lists only `corpus/lessons/round-21.md`;
`grep` of `corpus/SOURCES.md` for either target filename returns nothing. S019's stated scope
(“provenance-field and lesson-heading census only; no verification of historical platform
claims”) is consistent with both headers' “metadata authority only” wording, so the citation
semantics hold; only the registry's used-by bookkeeping is incomplete.

## Uncertainties / remaining gaps

- Scope is exactly these two files; other sweeps cover the remaining knowledge files.
- `count_c1.py`/`c2_count.py` were edited in the working tree by another seat while this seat
  measured (selftest hooks and a c1-before minimum-obligation guard; `oracle_selftest.py` is new
  and untracked). Numbers are pinned to the executed base revision and reproduce under both
  observed script copies; a single script hash is not a stable anchor.
- `S###` is a placeholder, not an id. A future gate that expands `#` as a wildcard would
  false-positive on `kimi-subpath-audit.md:1`; the frozen literal regex (digits required) does not.
- Population membership is frozen to r26's 32 rows (S001–S034 minus S014/S019, confirmed by
  `SOURCES.md:79` and by `frozen/population.json`, byte-identical to `round-26/population.json`,
  sha256 `16330e1effd5ee52665f8f31738e9423c6ec387e5d4a1404c5bcc35f69d01b03`). Any widening is an
  L1 decision; seeds are named above and are additive only.
- Both files' bodies are historical/host-state narratives whose citations are artifact paths,
  not SOURCES ids; nothing in them can expand the C1 denominator.
- No source/public-site evaluation was needed or performed; this report judges citation
  presence and parser agreement only, not the truth of the cited claims.

## Evidence appendix (paths relative to repo root)

- `corpus/knowledge/keeper-timer-inert.md` — sha256 `3863e4283dff1a7079c7525b8fa6e964f44e7092a745c15e087e5d0a2f18b916` (base = HEAD = tree).
- `corpus/knowledge/kimi-subpath-audit.md` — sha256 `6fe588f8c35f15fa28085665be290a4ca3747abc882ff0e9d5d606b34c767fec` (base = HEAD = tree).
- `.ufo/waves/round-27/count_c1.py` — HEAD blob `a1e46d19b438fc254689dc42f474664864b7fd7fecc6a992ad70f5d5da44a14c`;
  working tree at last check `7ebb3f366f72f53db2b1e26fc633d90de5aa6e4fa042a615ad80c70e6af76e2d`.
- `.ufo/waves/round-27/c1-before.json` — `af55d0a4bb1aa9b21bc2ce026035beaf21e523458661252f8a520008f2ec6e3c`.
- `.ufo/waves/round-27/c2-oracle.json` — `1d038205473180c7cb57895c2d480a8b52debe3bf08ab0a2f58ca7b1f67bc7dd`.
- `.ufo/waves/round-27/c2_count.py` — HEAD blob `93f39b0f7187fa084abd220d8c3734ce02b11b64cd940a1953347f37fa304686`;
  working tree at last check `e5b6fa7f2e850225ed79c45534ba1222832f7365003908aec054f756960af999`.
- `.ufo/waves/round-27/contract.json` — `6d2d7f51371650c2d7535c401ead613355135d18b44762c41f385d05ee7582da`.
- `.ufo/waves/round-27/frozen/expected.json` — `628b7a054b3eb95370cb6716bf5fe8e87a9c9ab7caaadafad9797b726ec170c2`.
- `.ufo/waves/round-26/statements.json` — `c2026376832ad4e4114d1bc19abeec4fcbdbd0fea3dbb102ab8a5c2eb18c95ce`.
- Scratch: `/fast/scratch/hyaku/kake-r27/CitingSweep08/count_c1_base.json` (parser stdout).
- No lane/file edits made; report is the only write.
