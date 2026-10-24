# SourceCensus — round 27 W1 scoped findings (read-only seat)

Seat: `KakeR27.SourceCensus`. Lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Axes: **freshness** (source openness, anchor survival, used-by routing), **operability** (maintained census command behaviour/exit).
No registry, corpus, sibling, index or git mutation was made. All scratch under `/fast/scratch/hyaku/kake-r27/SourceCensus/`.

## 1. Maintained source census — exact command, output, exit

Command (maintained, `scripts/sources-census.sh`, sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
exit=0        stderr: (empty)
```

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake
kake	rows	35
kake	tier.A	33
kake	tier.C	2
kake	status.mined	31
kake	status.queued	2
kake	status.rejected	2
FLEET	rows	35 | FLEET.tier.A	33 | FLEET.tier.B	0 | FLEET.tier.C	2 | FLEET.tier.invalid	0
FLEET	status.queued	2 | FLEET.status.mined	31 | FLEET.status.rejected	2 | FLEET.status.invalid	0 | FLEET	missing	0
exit=0
```

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin kake
35 lines, all "kake cadence S0NN recheck=<x> opened=<date>" (S001/S002 on-release; S003–S007/S013–S017/S021/S023–S027/S030 90d;
S008–S012/S018/S019/S020/S022/S028/S029/S032–S034 365d/180d/on-release) — zero "overdue" lines
exit=0
```

- `--today` default = `date -u +%F` = **2026-10-21** (UTC); the run is dated today.
- Reproduces `.ufo/waves/round-27/census-before.txt` (recorded 2026-10-21 16:58) byte-for-byte: `W04 S033` + `ok`, `exit=0`.
- Only finding is the **inherited** W04 (S033 shares `rfc9110.txt` with S010/S028 — different scopes, warning only, exit unaffected).
- `overdue` exit 0 ⇒ **no row is due**: earliest numeric due date is S003 (opened 2026-10-19 + 90d = 2027-01-17). Numeric `Nd` cadences are computed (`scripts/sources-census.sh:679-685`) and only surface when due; the informational `cadence` line is also printed for `Nd` (`:677`), so the `cadence` label does not imply "symbolic only".

## 2. Independent re-count (hand-run SOURCES-CONTRACT-v1 census commands)

Ran the contract's own awk/grep block (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` §Census) against `corpus/SOURCES.md`:

| metric | contract command | maintained script | r26 lesson claim (`corpus/lessons/round-26.md:150`) | agreement |
|---|---|---|---|---|
| rows | 35 | 35 | 35→35 | ✔ |
| tiers | A=33 C=2 | A=33 C=2 | A33/C2 | ✔ |
| status | mined=31 queued=2 rejected=2 | same | mined31/queued2/rejected2 | ✔ |
| malformed (NF≠13) | 0 | 0 (no E01) | — | ✔ |
| duplicate ids | none | 0 (no E03) | — | ✔ |
| enum violations (kind/tier/status) | none | 0 (no E05/E06/E07) | — | ✔ |
| community-at-A | none | 0 (no E10) | — | ✔ |
| mined used-by paths missing on disk | none | 0 (no E11) | — | ✔ |

Verdict: the maintained census and a hand re-count agree exactly; the frozen r26 baseline numbers still hold at the current tree.

## 3. The grouped S001–S006 preflight pairs are exactly six, and they are the six grouped ones

Independent enumeration of the C1 population (32 rows from `.ufo/waves/round-26/population.json`) over `corpus/knowledge/**` at base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`, replicating `count_c1.py` grammar (literal `\bS\d{3,}\b` + range `\bS\d{3,}\s*([-–—]|\.\.|to|through)\s*S\d{3,}\b`):

- **total pairs = 57** — equals `c1-before.json` `citingPairs: 57`, and equals the count at HEAD `be375d9…` (unchanged; `git diff 83528f7..be375d9 -- corpus/` is empty).
- The **six grouped preflight pairs** are all in one file and come from **one grouped range citation**: `corpus/knowledge/static-canonical-preflight.md:54` — "…not over an assumed checkout served set (**S001–S006**, `ghp-served-set.md`)". It expands to the six pairs `(S001…S006, corpus/knowledge/static-canonical-preflight.md)`; all six are in the frozen 16-missing list of `c1-before.json`.
- The other four S001–S006 pairs among the 16 are **literal**, not grouped: `(S003, sitemap-orphan-audit.md)`, `(S004, publish-channels.md)`, `(S005, sitemap-orphan-audit.md)`, `(S006, publish-channels.md)`.
- Remaining six of the 16: `(S008, crawl-scope-per-host.md | ghp-custom-domain.md | ghp-etag-anatomy.md | static-canonical-preflight.md)`, `(S022, static-canonical-preflight.md)`, `(S023, static-canonical-preflight.md)`.
- No uncaptured citation form was found: no `S0NN-0NN` / `S0NN..0NN` shorthand, no `S0NNff` suffix forms in `corpus/knowledge/**` or `corpus/lessons/**`. **No pair beyond the frozen 57 is added by this seat** (denominator unchanged at 57; nothing silently dropped).
- **Discovered 58th pair (monotone, named as required)**: `.ufo/waves/round-27/discovered-pairs.json` (sibling seat) adds `(S013, corpus/knowledge/ghp-served-set.md)`. My independent census confirms the mechanical count is **57** and that S013 is a literal pair only in `crawl-scope-per-host.md`; the 58th comes from an **embedded-only** reference at `corpus/knowledge/ghp-served-set.md:95` ("…(w2/Rejection01S001.md, w2/Rejection07S013.md)") which the frozen literal regex cannot see (`\bS013\b` has no leading word boundary inside "Rejection07S013.md"). Denominator therefore grows 57→58, obligations grow by one, and the pair is an artifact-reference rather than a source citation.

## 4. Allowed used-by changes for the grouped preflight claim (SOURCES v1 rule 2)

Contract v1 rule 2 (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`): *"Append-only. Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson."* Rule 1/2 also make `teaches`/`anchor`/`source`/`opened` immutable in place; a correction is a **new** row opening `supersedes S0NN —`.

**Minimum allowed change for the six grouped pairs** (append the grouped citing file to each row's `used-by`; no other cell moves):

| row | old used-by | new used-by | status | recheck | opened |
|---|---|---|---|---|---|
| S001 | corpus/knowledge/ghp-served-set.md | + corpus/knowledge/static-canonical-preflight.md | mined (no change) | on-release (no change) | 2026-10-19 (no change) |
| S002 | corpus/knowledge/ghp-served-set.md | + corpus/knowledge/static-canonical-preflight.md | mined | on-release | 2026-10-19 |
| S003 | corpus/knowledge/ghp-custom-domain.md, corpus/knowledge/ghp-served-set.md | + corpus/knowledge/static-canonical-preflight.md | mined | 90d | 2026-10-19 |
| S004 | corpus/knowledge/ghp-served-set.md | + corpus/knowledge/static-canonical-preflight.md | mined | 90d | 2026-10-19 |
| S005 | corpus/knowledge/ghp-custom-domain.md | + corpus/knowledge/static-canonical-preflight.md | mined | 90d | 2026-10-19 |
| S006 | corpus/knowledge/ghp-served-set.md | + corpus/knowledge/static-canonical-preflight.md | mined | 90d | 2026-10-19 |

(S003 opened cell reads `2026-10-19`; the `90d` cadence is unchanged.)

- **No status change is owed**: all six are already `mined` (≥1 used-by path), so W03 cannot fire.
- **No recheck change is owed**: re-open is not a cadence change; `on-release`/`90d` stay.
- **No `opened` change is owed or allowed** (rule 2 does not list `opened`).
- **Logging requirement**: each of the six old→new strings must appear in the r27 round lesson; r26 precedent = `corpus/lessons/round-26.md:130` ("S024 and S025 `used-by`, each: `corpus/lessons/round-22.md` → `corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-22.md`. Status and recheck unchanged; no new rows."), which is exactly the same shape of change.
- **Simulation (scratch only, repo untouched)**: a copy of `corpus/` at `/fast/scratch/hyaku/kake-r27/SourceCensus/simlane` with the six `used-by` cells amended →
  `validate` → `simlane W04 S033 …` + `simlane ok …`, **exit=0**; `census` → rows 35, A33/C2, mined31/queued2/rejected2, **exit=0**.
  Negative control: adding a non-existent path (`corpus/knowledge/does-not-exist.md`) to S001's used-by → `simlane E11 S001 missing used-by corpus/knowledge/does-not-exist.md`, **exit=1** — so the E11 check is live on the amended cell and the clean result is not vacuous.

**Pre-existing used-by completeness gap (not created by r27, census does not enforce it)**: the six rows are cited by more knowledge files than the registry lists — S001 also by `ghp-subpath-spotcheck.md`, `publish-channels.md`, `sitemap-orphan-audit.md`, `speedrun-pipeline.md`; S002 by `publish-channels.md`, `sitemap-orphan-audit.md`, `speedrun-pipeline.md`; S003 by `publish-channels.md`, `sitemap-orphan-audit.md`; S004 by `publish-channels.md`, `sitemap-orphan-audit.md`, `speedrun-pipeline.md`; S005 by `ghp-subpath-spotcheck.md`, `publish-channels.md`, `sitemap-orphan-audit.md`; S006 by `publish-channels.md`, `sitemap-orphan-audit.md`. The census has no exhaustiveness rule (only E11 existence, W03 mined-with-`—`), so adding them is *permitted* under rule 2 but is a separate completeness decision for the L1 — and, if done, must also be logged old→new. Lesson files (`corpus/lessons/round-20.md`, `round-21.md`, `round-26.md`, `round-26-verifier-spotcheck.md`, `round-7.md`) cite S001–S006 too but are outside the C1 pair scope (C1 scans `corpus/knowledge` only).

## 5. First-open dates vs re-open dates, and v1 immutability

- `opened` for S001–S006 = **2026-10-19** (first open, r20 authoring round). It must stay that value: rule 2 permits in-place change only to `status`/`recheck`/`used-by`.
- Re-opens this round: `.ufo/waves/round-27/fetched/manifest.json` (sha256 `d3b0b1ca215bfa6d89edf639b2b87475d668fdf73cbf0ddf089c87e11d043781`), 8 GETs, all HTTP 200, `fetchedAt` 2026-10-21T19:59:53.61Z → 19:59:56.11Z, rows S001×2, S002×2, S003, S004, S005, S006. Prior re-open: r26 recheck (2026-10-21, 32 rows, HOLD 32, `corpus/SOURCES.md` §Search log "Round 26 bounded recheck").
- **Every re-fetched URL is byte-identical to the URL recorded in the registry** for that row (registry URL set == manifest URL set for all six rows) ⇒ no URL drift between first open and re-open.
- Registry immutability evidence: `corpus/SOURCES.md` sha256 = `5001eadee20c65c5df364a88430b6b0e76a99940afc282d72fecdd6d7c6be62d` **identical** at base `83528f7…`, at HEAD `be375d9…`, and in the working tree; `git status --porcelain -- corpus/` is empty. Last cell change was r26 (`a2be0dc`: S024/S025 `used-by` only, logged in the r26 lesson).
- Precedent for keeping re-open dates out of the cells: r26 kept re-open evidence in append-only prose ("Older verified-at/reopened dates … remain the historical record of the earlier reading; they are not rewritten", `corpus/knowledge/static-canonical-preflight.md:184`) and in the SOURCES prose note for S030 (round-23 precision note) — not in `opened`.

## 6. Anchor survival against the r27 retained bytes (freshness spot-check, own re-read)

Retained raw bytes (`fetched/*.raw.gz`, sha256 in manifest) and extracted text (`fetched/text/*.txt`):

- S001 main `5f327015…`: raw lines **17–20** = `include-hidden-files:` input block, **37–39** = `--exclude=.git`, `--exclude=.github`, `--exclude=.[^/]*` conditional → the anchor's stated line ranges hold **exactly** for the main commit. Caveat: the same line numbers in the v4.0.0 tag file (`7b1f4a7…`, 85 lines) point to unrelated lines (`outputs: artifact_id:` at 17–20) — the anchor cell names only the main commit, so it is correct as written and must not be restated as covering the tag file.
- S002 v5.0.0 changelog: "feat: add include-hidden-files input" present; v4.0.0: "hidden files (specifically dotfiles) will not be included in the artifact" present → `teaches` still supported.
- S003: "publishing source … publish when changes are pushed to a specific branch, or … a GitHub Actions workflow" present → supports `teaches`.
- S004: "upload-pages-artifact", "tar", "symbolic", "10GB", "gzip" all present → supports `teaches`.
- S005: "no CNAME file is created, and any existing CNAME file is ignored and is not required" present → supports `teaches` (and the ART:333 CNAME conflict note resolves against S017).
- S006: "By default, Jekyll doesn't build files or folders that: … /node_modules or /vendor, Start with _,., or #, End with ~" present → supports `teaches` (the underscore path is phrased "Start with _", not the word "underscore").

(Each of the six rows' full re-opening with quote/anchor adjudication is the `KakeR27.SourceOpenS00x` seats' scope; the above is my own bounded re-read for census/anchor freshness only.)

## 7. Findings by severity

1. **MEDIUM — `opened` immutability is not machine-enforced.** The validator's only date rule is E08 (`opened` must be a non-future ISO date, `scripts/sources-census.sh:660-662`); rewriting `opened` from 2026-10-19 to 2026-10-21 passes `validate` (exit 0) silently. Detecting such a rewrite depends on the round-lesson old→new log and git history. *Consequence for r27*: the grouped re-open must be recorded in the lesson/ledger, not by touching `opened`.
2. **MEDIUM — the "frozen" oracle scripts are modified in the working tree (observed, not judged).** `git status` shows `M .ufo/waves/round-27/count_c1.py` and `M .ufo/waves/round-27/c2_count.py` (uncommitted, sibling seats). The `count_c1.py` diff adds (a) a floor that unions `c1-before.json` `missing` and the r26 decided pairs into the pair set, (b) `decided.discard(key)` so a fresh row cannot inherit old credit, (c) a new error code `group_source_required` for the six grouped preflight pairs when `kind != "source"`, and (d) `--selftest` dispatch to `oracle_selftest.py`. Both scripts also gain a `--selftest` dispatch. These are measurement-semantics edits to the artifacts the r27 context declares frozen; whether they count as a harness extension or as oracle drift is an L1/critic call, but the change is present and uncommitted at the time of this census. `c2-oracle.json` itself is unmodified (sha256 `1d038205473180c7cb57895c2d480a8b52debe3bf08ab0a2f58ca7b1f67bc7dd`, matching the frozen blob). **This seat neither edits nor evaluates that decision.**
3. **LOW — used-by cells are not exhaustive** (§4 list). Not a census violation, but a routing hazard of the same kind r26 already fixed for S024/S025: a correction aimed at the grouped preflight claim would be routed to `ghp-served-set.md` only. Since the r27 grouped adjudication lands in `static-canonical-preflight.md`, the append is required for correct routing; extending to the other citing files is a separate, permitted completeness step.
4. **LOW — `cadence` label overload in `overdue` mode**: numeric `Nd` rows are printed with the `cadence` prefix as well as being evaluated for due-ness (`:677` vs `:679-685`). No row is currently overdue, so exit 0 is correct; the label alone must not be read as "never judged".
5. **INFO — inherited W04 (S033 duplicate URL across scopes)** persists unchanged; it is a warning by contract and does not affect lane status (exit 0).
6. **INFO — anchor precision**: S001's line ranges are valid for the main commit only (see §6). No change is owed (anchor is immutable in place); if the anchor must name the tag variant, that is a **new** superseding row per rule 2, not an edit.

## 8. Residual risk and verification gaps

- The census measures the **registry**, not the truth of the 57 pairs; C1 adjudication of the six grouped pairs (HOLD/STALE/UNVERIFIABLE) is not decided by this seat and must not be inferred from "sources still open".
- My pair census replicates `count_c1.py` grammar; it does not cover `corpus/lessons/**` (C1's declared scope) nor any citation form outside the two regexes — none found by the shorthand sweep in §3.
- `overdue` was evaluated at `--today` 2026-10-21 (UTC). A later date changes due-ness, not the registry.
- I did not execute the gate/selftest/fixture writers (`scripts/citing_set.py` does not yet exist at this revision — `c2_count.py` reports `gate_absent`); C2 remains unmeasured by me.
- No HTTP request was issued by this seat (all reads local); the r27 fetches were performed by the wave's own `fetch_group.py` before this seat ran.

## 9. Tooling record

No installs, upgrades, pacman/uv/cargo/npm actions were needed or performed. Commands used: `bash` (read-only), `read`, `grep`, plus two scratch Python scripts written under `/fast/scratch/hyaku/kake-r27/SourceCensus/` (`pairs.py`, and an inline copy/apply/validate simulation). Nothing was written into the repository except this report.

**Report:** `.ufo/waves/round-27/w1/SourceCensus.md`
