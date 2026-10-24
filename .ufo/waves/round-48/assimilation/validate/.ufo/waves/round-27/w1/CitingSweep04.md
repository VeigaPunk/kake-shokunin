# CitingSweep04 — blind citing-set data-walk: `free-read-verbs.md`, `freshness-pins.json`

Seat: read-only leaf, r27 full-citing-set milestone. No source/public-site evaluation performed.
Observed revision: worktree `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (HEAD), measured base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`. `git status --porcelain` for both paths: clean; `git diff --stat <base>` for both paths: empty; base blobs byte-equal working files.
Tooling: python3 stdlib + git reads only. No installs, no pacman, no writes outside this report and `/fast/scratch/hyaku/kake-r27/CitingSweep04/`.

## 0. Identity hashes (both match `frozen/expected.json` exactly)

| file | bytes | lines | sha256 |
|---|---|---|---|
| `corpus/knowledge/free-read-verbs.md` | 38347 | 503 content (split len 504, trailing empty) | `5464ae6dee18b14785a8faf957e8eb80ec7baa78eb0b264965b08b618c5180ee` |
| `corpus/knowledge/freshness-pins.json` | 8109 | 200 | `2db3d777a86b5fa585eda3ada8629e0889351659bcec232b2c3678475814035a` |

## 1. Manual census — every S-token in both files (exhaustive, exact-parser independent)

Scan basis: whole-file byte read; exact frozen regexes `\bS(\d{3,})\b` and `\bS(\d{3,})\s*(?:[-–—]|\.\.|to|through)\s*S(\d{3,})\b`; plus alternate scan `(?<![A-Za-z0-9])S-?\s?\d{2,5}` and any `S\d{2,5}`.

| # | location | token | form | scope as written (support ≤25 words) | r26 population? | in frozen57? | in missing16? |
|---|---|---|---|---|---|---|---|
| 1 | `free-read-verbs.md:1:266` | `S019` | literal, provenance header | "metadata contract S019 (corpus/SOURCES.md, metadata authority only, not platform authority)" | **NO** — S019 excluded by contract (`round-26/contract.json:14`: "S001..S034 minus own-work S014/S019; S035 … excluded") | no | no |
| 2 | `free-read-verbs.md:195:31` | `S404` | pseudo-token inside `S404_SHA256` | sync-check card: "13 409-byte Kimi 404 sentinel (`S404_SHA256`, `scripts/kimi-surface.mjs:180`)" | n/a — not a registry id | no | no |
| 3 | `freshness-pins.json` | — | **none** | whole file 200 lines, 0 literal, 0 range, 0 near-form | — | no | no |

- Token 2 is not a source-id reference: `_` is a word character, so `\b` fails between `S404` and `_`; the frozen counter does not match it (confirmed by run, §4). Semantically it names a SHA-256 sentinel constant, not a `SOURCES.md` row; a naive `S\d+` read yields S404, which is unregistered (registry ends S035) and outside population. **Zero obligation either way.**
- No ranges, grouped lists, brace-lists, en/em-dash forms, `..`, `to`, `through`, or lowercase/space-separated variants exist in either file. Only capital-S digit forms are `S019` (line 1) and `S404` (line 195) in `free-read-verbs.md`; `freshness-pins.json` has none.
- Other `S`-adjacent hits are unrelated (`SKILL.md`, `S404`, dates like `2026-09-28`, counts like "18 sites"): no id semantics.
- **Citing pairs contributed by this seat's two files: 0 populated pairs; 1 outside-population pair `(S019, corpus/knowledge/free-read-verbs.md)`.**

## 2. Provenance headers and EOF notes inventory (line + scope + S-status)

| lines | block | S-id content |
|---|---|---|
| 1 | `source:` header; webzites tree list + "metadata contract S019" | **S019** (only S-token) |
| 2 | `verified-at:` 2026-09-28 / r16 2026-09-29 / absence notes r18, r20 | none; see §6 staleness note |
| 3 | `recheck:` webzites source restore-or-retire | none |
| 9 | inline `<!-- r18 re-census 2026-10-14 … -->` inside `Sources:` sentence | none |
| 37 | inline `<!-- r18 re-census 2026-10-14 … -->` **inside** ```` ```bash ```` `/ node -e '…'` block | none; see §3 defect |
| 195 | `S404_SHA256` sentinel constant | pseudo-token (§1 #2) |
| 325 | `[r20 citation-local 2026-10-19]` kimi-surface.mjs absence | none |
| 481–483 | `## Round-20 citation-local note (base cb807bc …)` + blockquote | none |
| 485–498 | `## Live re-verification — round 23 (2026-10-21)`, claims c1–c8 | none |
| 499–503 | `## Round-24 path reconciliation` + EOF absent note citing `free-read-verbs.md:321` | none |

`freshness-pins.json` provenance surface: `_comment` line 2, `schema` 3, `updated` 4 (`2026-10-21`), `round` 5 (`24`), `pins` 6–198. Contains 43 pin keys; `pathsMissSet` 63 path literals (57–121), `projectsChildrenSet` 14 (122–137), `pathsFiles` 56 repo-relative file literals (138–198). These are path/file literals, **not** source-id references; none matches `S\d{3,}`. So `freshness-pins.json` adds zero citing pairs and cannot hide an inherited pair behind path syntax.

## 3. Self-citation and sidecar binding for the EOF note (verified, plus one adjacent defect)

- `free-read-verbs.md:321` is the `probe` row of the Round-11 provenance table and does contain `node ~/Projects/webzites/bin/webzites.mjs probe ds4cc-com --json`; the EOF pointer is accurate.
- `sha256(line321) = 7d7703875301a6e04c2377d903709599507357da1da2dadcec7144945ac6b244`; `freshness-sidecar.json` entry (`file` at line 23, `line` 24, `token` 25, `lineSha256` 26, `note` 29) pins the same digest and token. Note text is byte-contained in EOF line 503 after the `- ` list prefix. Binding valid at this revision.
- **Adjacent defect (not a citing pair, flagged for L1):** the r18 `<!-- … -->` annotation at line 37 was inserted into the single-quoted argument of `node -e '…'` (line 37: `cd ~/Projects/webzites && node -e 'const s=…sites; <!-- … -->`). Copying the "Reproduce" block yields a JS syntax error, not the recorded `{rows:21,…}` output, so the entry's own reproduction recipe is broken at HEAD. The line-9 annotation is outside code and harmless.

## 4. `count_c1.py` parser vs manual census (comparison performed only after §1)

Parser (frozen file): `LITERAL = \bS(\d{3,})\b`; `RANGE = \bS(\d{3,})\s*(?:[-–—]|\.\.|to|through)\s*S(\d{3,})\b`; scans git blobs of every file under `corpus/knowledge` at `--revision`; pairs = (ids ∩ r26 population) ∪ `discovered-pairs.json`.

Run at base: `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision 83528f7c…` → exit 1, `citingPairs=57`, `decided=41`, `r26CarriedPairs=41`, `newDecided=0`, `missing=16`, `findings=[]`, `outcomes=[]`; no entry with either target file in `missing` (saved: `/fast/scratch/hyaku/kake-r27/CitingSweep04/c1-base.json`).
Byte provenance of the counter (observed, not authored by this seat): HEAD `be375d9` blob sha256 `a1e46d19…44a14c`; worktree file sha256 `7ebb3f36…6af76e2d` (uncommitted +9 lines: baseline-missing monotonicity union plus `--selftest` dispatch; `c2_count.py` likewise +2 lines). Both byte variants were run at base and return identical 57/41/16 with `findings=[]` and no target-file pair, so this report's parser comparison does not depend on which variant is current. No writes to either script by this seat.

Agreement on this slice: **exact** — S019 matched once and dropped by the population intersection; `S404` not matched; `freshness-pins.json` zero matches. Parser properties relevant to denominator integrity:
1. `RANGE` endpoints are already matched by `LITERAL`, so `RANGE` contributes only interior ids (no interior-only pair exists in these files).
2. Word-boundary behavior correctly excludes `S404_SHA256`; no false positive.
3. `to`/`through` are lowercase-only and `S` is uppercase-only; zero impact here, untested elsewhere.
4. `discovered` pairs are added **without** the population filter — an S019 discovered row would grow the denominator to 58. `.ufo/waves/round-27/discovered-pairs.json` does not exist at this revision (`glob round-27/**/discovered*` → none), so no discovered pair currently enters; monotonicity is unexercised, not violated.
5. Corpus-wide cross-check (outside this seat's files): 5 valid ranges — `publish-channels.md:2 S001-S007`, `sitemap-orphan-audit.md:2 S001-S006`, `static-canonical-preflight.md:2 S020-S027`, `:2 S028-S029`, `:54 S001–S006`. **None in the two targets and none spans S014/S019/S035**, so no range expansion creates an outside-population pair.

## 5. `c1-before.json` / 16-missing comparison

- `c1-before.json` (revision base) = 32 population, 57 citing pairs, 41 decided, 16 missing. The 16 rows live in `static-canonical-preflight.md` (9), `publish-channels.md` (2), `sitemap-orphan-audit.md` (2), and one each in `crawl-scope-per-host.md`, `ghp-custom-domain.md`, `ghp-etag-anatomy.md` — **neither target file appears**.
- Frozen57 membership from these files: **zero** (counter `missing`/`pairs` slice confirms; r26 `statements.json` has no row for either file).
- Therefore: **no inherited32-row pair in these two files is missing from frozen57; this seat names no additional frozen-denominator obligation.** Verdict does not rest on file shape — it rests on whole-file exact scans plus the frozen counter agreeing.
- Named separately per ticket: `(S019, corpus/knowledge/free-read-verbs.md)` at `1:266`, literal, scope metadata-authority-only. It is **outside** the frozen population (`round-26/contract.json:14`), so it is not counted in 57 and cannot be "missing". If L1 admits it via `discovered-pairs.json` or widens population, it becomes obligation #58; on the text it is scope-consistent with S019's own row ("Local provenance-field and lesson-heading census only; no verification of historical platform claims"), i.e. a HOLD-at-own-scope candidate — **not decided here**.
- S014 and S035 are **absent from both targets** (0 tokens). Corpus-wide, S014 appears only in `freshness-sweep.md` (lines 1, 182) and S035 only in `accessibility-review-packet.md` (lines 1, 88, 155). Registry asymmetry worth L1's attention: SOURCES S019 `used-by` lists only `corpus/lessons/round-21.md`, yet 16 knowledge files cite S019; no frozen-denominator effect today, but any population widening inherits an incomplete used-by index.

## 6. Freshness observations on the two targets (metadata-level only; no source evaluation)

- `free-read-verbs.md` provenance chain: original 2026-09-28 (r11) → r16 2026-09-29 → r18 absence 2026-10-14 → r20 2026-10-19 → r23 live re-verification 2026-10-21 (8 claims: 3 HOLD, 2 STALE, 3 UNVERIFIABLE) → r24 path reconciliation 2026-10-21. Header line 2 still says "absence notes 2026-10-14 (r18) and 2026-10-19 (r20) are citation-local" and names neither r23 nor r24; the EOF sections are newer than the header's own enumeration. Word-level staleness only; no source claim re-evaluated.
- r23 `c2` is self-contradictory as worded: claim text says the documented node invocation "is currently runnable … because its script is present", verdict STALE, correction says the script is absent. Read the correction as the observation; the claim sentence asserts presence and should be re-worded (freshness wording defect, not a citing-pair issue).
- `freshness-pins.json` pins `round: 24`, `updated: 2026-10-21`, 43 keys. The paths sidecar schema admits only `corpus/**/*.md` entries (`scripts/freshness-sweep.mjs:356`), so this `.json` cannot carry a sidecar binding; its only re-pin contract is the `_comment` rule. No S-id or source-claim surface exists in it.
- Both files are byte-identical to base and to checked-out HEAD (no r27 writer touched them), so base-revision citing-set results apply unchanged to the current worktree.

## 7. Verdict summary and remaining unknowns

- Factual: targets contribute **0** frozen-population citing pairs, **0** of the 16 missing pairs, **1** outside-population pair (`S019` × `free-read-verbs.md:1`), **0** ranges/groups/alternates with id semantics, and **1** non-id pseudo-token (`S404_SHA256`).
- Confidence: **high** for the census (whole-file exact-regex scans, alternate-form scans, frozen-counter agreement, byte-identical base/HEAD); **medium-high** for the S019 read-as-metadata interpretation (row scope text matches the citing parenthetical, but adjudication belongs to L1).
- Unknowns: (a) whether L1 admits `(S019, free-read-verbs.md)` as discovered pair #58 or keeps it outside the frozen denominator; (b) whether the header's r18/r20-only enumeration and the line-37 broken reproduce block are corrected in r27 or deferred; (c) S014/S035 citing scope outside these files (out of this seat's slice).

## Evidence

- `git show 83528f7…:corpus/knowledge/{free-read-verbs.md,freshness-pins.json} | sha256sum` → hashes in §0, equal to `frozen/expected.json`.
- Exact-regex census + alternate scans: reproduced in §1 (python3, stdlib `re`).
- Frozen counter run output: `/fast/scratch/hyaku/kake-r27/CitingSweep04/c1-base.json`.
- Sidecar entry: `corpus/knowledge/freshness-sidecar.json:22-30`; line-321 digest recomputed and matched.
- Population authority: `.ufo/waves/round-26/contract.json:14`; population ids `.ufo/waves/round-26/population.json`.
