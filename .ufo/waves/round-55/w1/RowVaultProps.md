# RowVaultProps

Seat: C1 (coverage-map calibration), leaf, read-only. Read in full: `corpus/knowledge/vault-properties.md`
(103 lines, sha256 `f26b2d10…ff51`, byte-identical to `HEAD:corpus/knowledge/vault-properties.md`) and
`corpus/README.md` §`## Coverage map` (line 15; 27 existing data rows, 3-cell `| Area | Entry | Coverage |`).
No file edited; the knowledge file is unchanged.

## ROW:

```markdown
| Vault PROPERTIES[] surface audit (r23) | `knowledge/vault-properties.md` (S019) | Static GET exposes the client-rendered PROPERTIES literal, so rot-checking needs no rendered DOM: 13 entries, 3 null URLs, seed-tag byte normalization, and round-23 HOLD/STALE corrections where URLs marked live are not 200. |
```

Cell checks: Area = 5 words (round tag `round 23` from the file's own section header, line 89);
Entry = backticked path + `S019` copied from the file's own `source:` line (line 1); Coverage = 32
whitespace tokens (limit 10–45), no `|`, does not start with `TBD`, shares `static`, `rendered`,
`literal`, `entries`, `properties` with the H1/first 1500 chars. Replicated the C1 counter's own
per-file helpers (`c55_readme_index.py`: `coverage_section`, `words`, `TOKEN_RE`, `resolves`) against
`HEAD` bytes plus this row in memory: indexed = yes, thin = no, new dangling tokens = none. The counter
itself was not run.

## EVIDENCE:

- `corpus/knowledge/vault-properties.md:9` — "`const PROPERTIES = [...]` source, so **rot-checking
  needs NO rendered DOM**" (11 tokens; raw substring of line 9, context "a static GET sees the full" on
  line 8) → Coverage clause "Static GET exposes the client-rendered
  PROPERTIES literal, so rot-checking needs no rendered DOM".
- `corpus/knowledge/vault-properties.md:29` — "13 entries, 3 `url:null` (ds4cc-mirror,
  snapshot.kimi.pro, burnerchrome .com)" (8 tokens) → Coverage clause "13 entries, 3 null URLs" (the
  file's own count; not re-derived locally — see RISKS).
- `corpus/knowledge/vault-properties.md:75-76` — "normalize the seed tag; byte deltas alone cannot carry
  freshness evidence" (11 tokens; raw substring of line 76, context "post-publish byte-digest checks
  MUST" on line 75) → Coverage clause "seed-tag byte normalization".
- `corpus/knowledge/vault-properties.md:95` — "four of the nine URLs marked live (among ten non-null
  property URLs) are non-200" (14 tokens) → Coverage clause "round-23 HOLD/STALE corrections where URLs
  marked live are not 200"; the round tag itself is line 89, "## Live re-verification — round 23
  (2026-10-21)" (7 tokens).

All four passages were checked as raw substrings of the committed body (`in` over `git show
HEAD:corpus/knowledge/vault-properties.md`), and each is ≤ 25 units.

## RISKS:

- **Front matter is stale relative to the file's own newest section.** Line 3 still reads
  "Historical-not-live-reverified; no round-21 domain recheck", while line 89 adds a live round-23
  re-verification dated 2026-10-21. The row therefore takes its round tag from the section header, not
  the front matter; a reader who dates the file from lines 1–3 would call it r21-era and
  non-live-reverified.
- **The file contradicts itself on the twins.** Line 7 calls the scope "(byte-twin vaults)", but line 94
  (c2, STALE) records that the GET bodies are not byte-identical (10,059 B vs 9,966 B, distinct
  SHA-256s). The row deliberately says nothing about byte-twins.
- **Baseline dead-URL count is superseded.** Line 30 says "**3 of the 10 are dead while marked
  `"live"`**", and the table under it lists five entries; line 95 corrects this to four of nine
  live-marked URLs non-200. The row states no dead-URL count, only that the round-23 corrections exist.
- **`S019` is metadata authority only, not evidence for the property observations.** The file's own
  source line says "Metadata authority only: S019 in corpus/SOURCES.md"; `corpus/SOURCES.md:27` describes
  S019 as an "own-work" local provenance-field census with "no verification of historical platform
  claims". The Entry-cell id must not be read as grounding the counts or the URL statuses.
- **Nothing in the row was re-derived here.** Line 3 states no local copy of `fleet/vault-properties.json`
  or `kimi-surface.mjs` exists in the lane, and c8 (line 100) confirms both absent; I confirmed absence
  and made no network call. The row's counts are the file's statements, not this seat's measurement.
- **Unverifiable content the row cannot carry.** c10 (line 103) is UNVERIFIABLE on `sourceDir`/`cmdUpdate`
  enforcement, and the round-23 receipt `.ufo/waves/round-23/receipts/vault-properties.json` exists
  (10,001 B, mtime 2026-10-21 04:58) but its contents were not re-read, so no receipt-level claim is made.
- **Format constraint for the landing seat.** The coverage map's `dangling` term scans every backticked
  `*.md|py|mjs|json|sh|txt` token in the whole section; this row adds exactly one
  (`knowledge/vault-properties.md`, resolving under `corpus/`). Any future edit to this row must not add
  a backticked path that resolves nowhere, and the row must stay the first row naming the file (the
  `thin` check reads only the first naming row).

VERDICT: one coverage-map row drafted and counter-helper-validated for `knowledge/vault-properties.md` (32-token Coverage, shared H1 words, no dangling pointer); file left unedited, with its stale front matter and byte-twin/dead-count contradictions recorded as risks.
