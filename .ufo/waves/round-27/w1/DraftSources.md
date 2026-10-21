# DraftSources — SOURCES search log + allowed used-by changes for grouped S001–S006

Seat `KakeR27.DraftSources` (scribe, axis freshness). Report-only; this seat edited no production file. Lane
base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`, declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`,
implementation `08014ce6186b16574fdf458ad4a9fd6b95a49366`.

## 1. Independent re-count of the required exact figures

Three mutually independent methods, all from `corpus/SOURCES.md`; all agree.

| Figure | Required | A: contract awk/grep | B: python table parse | C: maintained census |
|---|---|---|---|---|
| source rows | 35 | 35 | 35 | 35 |
| tier A | 33 | `A=33` | `A:33` | `tier.A 33` |
| tier C | 2 | `C=2` | `C:2` | `tier.C 2` |
| mined | 31 | `mined=31` | `mined:31` | `status.mined 31` |
| queued | 2 | `queued=2` | `queued:2` | `status.queued 2` |
| rejected | 2 | `rejected=2` | `rejected:2` | `status.rejected 2` |

A = SOURCES-CONTRACT-v1 §Census awk/grep block: rows=35, malformed=0, `A=33 C=2`, `mined=31 queued=2
rejected=2`, duplicate ids empty, enum/tier-inflation violations empty, mined used-by paths all present. B =
independent python parse of `^| S\d{3} |` rows: 35 rows, ids contiguous S001–S035, `Counter({'A':33,'C':2})`,
`Counter({'mined':31,'queued':2,'rejected':2})`. C = `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
--root /home/vgpnk/Projects/shokunin kake` → `kake W04 S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across
scopes` + `kake ok .../corpus/SOURCES.md`, exit=0; `census` mode → rows 35, tier.A 33, tier.B 0, tier.C 2,
status.mined 31 / queued 2 / rejected 2, FLEET.missing 0, exit=0 — reproducing `.ufo/waves/round-27/census-before.txt`
byte-for-byte. **No row added, rejected or re-tiered**: ids stay contiguous S001–S035, S015/S016 stay `queued` with
`used-by = —`, S017/S018 stay `rejected` (tier C) with `used-by = —`; rejections are retained, not deleted.

**Cell-level diff, HEAD vs worktree (`corpus/SOURCES.md`):** exactly six rows changed and, in each, only cell
index 10 (`used-by`). `status`, `opened`, `recheck`, `tier`, `anchor`, `teaches`, `source`, `kind` are byte-identical
for S001–S006 and all other rows — contract v1 rule 2 (append-only; only `status`/`recheck`/`used-by` change in place,
logged old→new in the round lesson) and "do not rewrite immutable row teachings" both hold. HEAD sha256
`5001eadee20c65c5df364a88430b6b0e76a99940afc282d72fecdd6d7c6be62d`; worktree sha256
`c92807d7558b53d5c54197749d926a3706a215a56ca57d1bd7441b45e9fb8dd2`.

## 2. Where the grouped S001–S006 preflight claim lives
`corpus/knowledge/static-canonical-preflight.md` holds exactly **one** occurrence of any S001–S006 literal or
range, at line 54: "an assumed checkout served set (S001–S006, `ghp-served-set.md`). No production". Full sentence
(lines 52–54): "Prepare the manifest over actual built/deployable HTML when that artifact exists, not over an assumed
checkout served set (S001–S006, `ghp-served-set.md`)." The en-dash range expands (count_c1 RANGE regex) to S001…S006,
so the grouped claim is one sentence behind one citation group: a *recommendation* to build the manifest from real
deployed HTML, not from an assumed checkout listing — not a platform assertion.

The other four S001–S006 pairs among the frozen 16 omissions are **not** part of the grouped preflight claim;
they are metadata/provenance bands in other entries (`sitemap-orphan-audit.md:2` "r20 S001-S006 quote corrections";
`publish-channels.md:2` "round-20 corrections 2026-10-19 (S001-S007 opened that day)"), disposed in
`corpus/knowledge/sitemap-orphan-audit.md` §Round-27 provenance-range clarification and in
`.ufo/waves/round-27/pairs.json` (S003 HOLD at contextual batch scope, S005 STALE partial attribution, S004/S006 HOLD
on historical opened-date metadata). The preflight range expansion is thus six pairs from one sentence; nothing else
in that file cites S001–S006.

## 3. Old → new `used-by`, and whether source-specific support permits each

Only `used-by` moves. Beyond the preflight file, each new cell names the enumerated knowledge citers the r26
ledger already adjudicated but the registry cell never named, plus this round's lesson.

| Row | Old used-by | New used-by | Source-specific support permits the preflight addition? |
|---|---|---|---|
| S001 | `corpus/knowledge/ghp-served-set.md` | `corpus/knowledge/ghp-served-set.md, corpus/knowledge/ghp-subpath-spotcheck.md, corpus/knowledge/publish-channels.md, corpus/knowledge/sitemap-orphan-audit.md, corpus/knowledge/speedrun-pipeline.md, corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-27.md` | **Yes, limited premise.** v4.0.0 `action.yml` archive command, 16 words, anchor "v4.0.0 action.yml Archive artifact, Linux tar command lines29–36": `tar \ --dereference --hard-dereference \ --directory "$INPUT_PATH" \ -cvf "$RUNNER_TEMP/artifact.tar" \ --exclude=.git \ --exclude=.github \ --exclude=".[^/]*"`. Unconditional `.git`/`.github`/dot-path exclusion means artifact membership can differ from a checkout listing. HOLD as a *premise*, not as entailment of the recommendation. |
| S002 | `corpus/knowledge/ghp-served-set.md` | `corpus/knowledge/ghp-served-set.md, corpus/knowledge/publish-channels.md, corpus/knowledge/sitemap-orphan-audit.md, corpus/knowledge/speedrun-pipeline.md, corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-27.md` | **Yes, limited premise.** v4.0.0 release, What's Changed, 14 words: "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact"; v5.0.0 Changelog adds `feat: add include-hidden-files input` (4 words). Version-specific membership change ⇒ a checkout listing is not the artifact set. HOLD as premise. |
| S003 | `corpus/knowledge/ghp-custom-domain.md, corpus/knowledge/ghp-served-set.md` | `corpus/knowledge/ghp-custom-domain.md, corpus/knowledge/ghp-served-set.md, corpus/knowledge/publish-channels.md, corpus/knowledge/sitemap-orphan-audit.md, corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-27.md` | **Yes, limited premise.** 22 words, anchor "Creating a custom GitHub Actions workflow to publish your site, general workflow flow steps3–4": "If required by your site, build any static site files. Use the actions/upload-pages-artifact action to upload the static files as an artifact." Publishing mode / source selection and the optional build step define the deployment inputs. HOLD as premise. |
| S004 | `corpus/knowledge/ghp-served-set.md` | `corpus/knowledge/ghp-served-set.md, corpus/knowledge/publish-channels.md, corpus/knowledge/sitemap-orphan-audit.md, corpus/knowledge/speedrun-pipeline.md, corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-27.md` | **Yes, limited premise.** 15 words, anchor "Configuring the upload-pages-artifact action": "The GitHub Pages artifact should be a compressed gzip archive containing a single tar file." Defines the packaged deployment unit; does **not** by itself prove checkout divergence. HOLD as premise. Separately, the *numbered locator* attribution at `ghp-served-set.md` lines 29–30 is STALE, corrected append-only to S003 (`[r27-recheck S004 STALE]` present there). |
| S005 | `corpus/knowledge/ghp-custom-domain.md` | `corpus/knowledge/ghp-custom-domain.md, corpus/knowledge/ghp-subpath-spotcheck.md, corpus/knowledge/publish-channels.md, corpus/knowledge/sitemap-orphan-audit.md, corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-27.md` | **No — the citation is over-inclusive.** 15 words, anchor "Configuring an apex domain step4; repeated under Configuring a subdomain step4": "If you are publishing from a custom GitHub Actions workflow, no CNAME file is created". That is domain configuration, not which built/deployable HTML files populate a manifest. STALE for the preflight attribution (`[r27-recheck S005 STALE]` appended to the preflight file); the row's own domain teaching remains HOLD at its own scope and its row cells are untouched. The cell still names the preflight file because that file does cite S005 — a routing premise, not an assertion of support. |
| S006 | `corpus/knowledge/ghp-served-set.md` | `corpus/knowledge/ghp-served-set.md, corpus/knowledge/publish-channels.md, corpus/knowledge/sitemap-orphan-audit.md, corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-27.md` | **Yes, limited premise.** 18 words, anchor "Configuring Jekyll in your GitHub Pages site, default exclusions paragraph": "By default, Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor". Supports only the Jekyll branch-build leg; not every Actions workflow uses that build path. HOLD as premise. |

Five rows (S001, S002, S003, S004, S006) supply limited premises for **local synthesis**; none individually
entails the manifest recommendation. S005 is the one row whose citation at the grouped sentence is rejected as
support. This matches the paired judgments in `.ufo/waves/round-27/pairs.json` (S001 HOLD, S002 HOLD, S003 HOLD, S004
HOLD, S005 STALE, S006 HOLD; each with `reason`, `anchor`, `fetchIndex`, `quote`, `reviewA`/`reviewB`).

**Anchor re-read on the r27 retained bytes (independent, normalized view offsets).** S001
`include-hidden-files:` input description (452) and main-pin exclude block (1006); S002 v4 "What's Changed" (2613) /
"Potentially breaking change…" (2628), v5 "Changelog" (661) / "feat: add include-hidden-files input" (2703); S003
"About publishing sources" (1560) / "Creating a custom GitHub Actions workflow" (6026) / "You can publish your site…"
(1684); S004 "Configuring the upload-pages-artifact action" (1431) / "…compressed gzip archive containing a single tar
file." (2741) / "…under 10GB…" (2833); S005 "Configuring an apex domain" (1493) / "Configuring a subdomain" (1520) /
"no CNAME file is created…" (3319); S006 "Configuring Jekyll in your GitHub Pages site" (1312) / "By default, Jekyll
doesn't build files or folders that:" (2782) / "Start with _,., or #" (2894) / "End with ~" (2915). All eight fetches
HTTP 200 (`fetchedAt` 2026-10-21T19:59:53.61Z–19:59:56.11Z); `gzip.decompress(raw)` sha256 equals the manifest sha256
for 8/8 (no `source_hash` finding). Raw-byte line check for S001: the **main** pin (`5f327015…`) has
`include-hidden-files:` at lines 17–20 and the exclude block at 37–39; the **v4.0.0 tag** (`7b1f4a7…`) has *no*
`include-hidden-files` input at all and its Linux tar command at 29–36. The registry anchor cell therefore describes
main-pin coordinates — hence a separate anchor-clarification search-log note instead of a rewritten anchor cell.

## 4. Draft SOURCES.md search-log entry (report-only draft; not applied by this seat)

Contract v1 rule 5 requires question/query, where searched, date, identified/screened/ included/excluded counts,
exclusion reasons and stop rationale. Two paragraphs already exist in the worktree `corpus/SOURCES.md` §Search log
(lines 81, 83) and satisfy that shape. Clause-by-clause independent check (✔ = verified against the bytes/registry):

- "Round27 repair-first question (2026-10-21): does each member of the omitted S001–S006
group support the actual built-HTML manifest recommendation at its stated scope?" → question ✔. "Opened the fixed six
existing rows' eight public URLs; identified6, screened6, re-opened6, new rows0, excluded registry candidates0" →
counts ✔ (6 rows / 8 URLs; all 8 manifest URLs are these six rows' registry URLs — no URL drift). "Five rows supply
limited premises for local synthesis; S005 retains its domain teaching but is rejected as support for the
HTML-membership sentence" → per-row exclusion rationale ✔. "57 frozen pairs plus one conservatively included embedded
report-reference pair" → denominator ✔ (57 + 1 = 58). "R26 remains rejected-honest-stop; its 32 receipts and 313 units
are not retroactively changed" → ✔ (32 files under `.ufo/waves/round-26/rechecks/`; `sum(statements)=313` over the 41
r26 pairs, `sum(stale)=7`). "No status/recheck/opened/teaching cell changes; only used-by routing is expanded" → ✔
(cell-level diff). Stop rationale present ✔.
- "Round27 anchor clarification for S001: input lines17–20 and archive lines37–39 are
main-pin coordinates; the v4.0.0 archive command is at lines29–36." → ✔ verified byte-exactly against `S001-2.raw.gz`
(89 lines) and `S001-1.raw.gz` (85 lines). "No claim of an inclusion input in v4 is made" → ✔ (no
`include-hidden-files` token in the v4.0.0 file). "original row cells are not rewritten" → ✔.

No third paragraph is required: this round opened no new registry candidate, so there is no additional
identified/screened population to log, and no new row quota is claimed.

## 5. Denominator growth (monotone) — one newly discovered citing pair
`discovered-pairs.json` adds exactly one obligation beyond the frozen 57: `S013 /
corpus/knowledge/ghp-served-set.md` (an embedded evidence-report filename, not a new teaching). The denominator grows
**57 → 58**; nothing is silently excluded. Re-derivation: frozen base pairs 57; +1 discovered = 58; r26-decided 41;
undecided obligations 17 (the 16 frozen omissions + the S013 discovery). All 18 `pairs.json` additions (17 obligations
+ 1 carried-pair override, S004 × ghp-served-set) validate clean against the frozen count_c1 rules: no duplicate, no
`not_cited`, all verdicts in {HOLD, STALE, UNVERIFIABLE}, all reasons present, `group_source_required` satisfied for
the six grouped preflight rows, every source quote present in its own row's view and absent from every other row's
view, word counts ≤25 and ≥6 non-underscore tokens, every artifact `contains` string present in its named evidence
blob at revision 08014ce, no self-supporting artifact evidence, and both `[r27-recheck S0NN STALE]` markers present in
their citing files. Worktree-state simulation of the frozen C1 logic: **citingPairs 58, decided 58, missing 0,
findings 0**.

## 6. Uncertainties and limits (explicit, not decided)

- **`used-by` cell semantics.** The cell is a routing premise, not a support claim. It now
names files that cite the row — including the preflight file for S005, whose citation was adjudicated STALE and
corrected append-only. If the lane instead reads `used-by` as "files whose claims are supported by this row", the S005
cell would need S005 removed. The per-row support test is answered above; the reading is the L1's to pick. Flagged,
not resolved here.
- **Lesson-file routing.** The r27 cells add `corpus/lessons/round-27.md` but not the older
lessons that also cite these rows (`corpus/lessons/round-7.md`, `round-20.md`, `round-21.md`, `round-26.md`,
`round-26-verifier-spotcheck.md`). The r26 precedent (S024/S025, `corpus/lessons/round-26.md:130`) added only the
newly-citing knowledge entry and stated that other rows' pre-existing routing exhaustiveness is not claimed repaired;
the r27 lesson repeats that scope limit. The omission is therefore consistent with the stated precedent rather than a
silent gap — but the cells are **not** exhaustive over lesson citers, and this seat does not claim otherwise.
- **The frozen 16 are a base-time obligation set.** `count_c1.py` at 08014ce still reports
`citingPairs 57 / decided 41 / missing 16`, because it reads files at a *committed* revision and the r27 corpus/ledger
edits are uncommitted in the worktree. The 0-missing result above is a worktree-state simulation of the same frozen
rules, not a committed-revision run; only L1, after committing, can produce the authoritative revision-pinned number.
- **Extractor normalization.** `round-26/source_text.py` (sha256
`55ae7abc52a5acfd95a86d96c27f12898c30e33ab63cfa7f383640120f57b7d6`, unchanged) merges punctuation-adjacent spaces, so
the S001 main-pin text reads "Excludes.git and.github regardless." — a quote written "Excludes .git and .github
regardless" fails a whitespace-normalized substring check against the *text view* while passing against the *raw
bytes*. The r27 S001 quote avoids the affected region. No extractor repair claimed.
- **No new-source freshness claim.** Re-opening 8 URLs on 2026-10-21 does not establish
perpetual source freshness, live-site conformance, or that any built artifact was inspected. No production artifact or
website was evaluated.
- **r26 remains rejected-honest-stop.** Its 32 receipts, 41 pairs and 313 statement units
are carried explicitly, not retroactively relabelled as r27 observations; the six prior UNVERIFIABLE units stay
disclosed.

## 7. Tools, versions, channels

No tool was installed or updated by this seat — no pacman transaction, no `uv tool install`, no release binary,
no `cargo install`, no `npm -g`; the task needed none and all pacman transactions are host-wide PAUSED. All scratch
written by this seat is under `/fast/scratch/hyaku/kake-r27/DraftSources/` (a census candidate simulation); `/tmp` and
`/dev/shm` were not used. Everything else was read-only inspection plus the Python/`git`/`awk`/`bash` already on the
host.

## 8. Verdict summary

| Check | Result |
|---|---|
| Source rows / tier A / tier C / mined / queued / rejected | 35 / 33 / 2 / 31 / 2 / 2 — reproduced three ways, matches census-before.txt |
| New rows minted | 0 (ids contiguous S001–S035; S017/S018 rejections retained) |
| Immutable cells rewritten | 0 (only cell 10 `used-by` on S001–S006 differs) |
| Grouped S001–S006 preflight claim | one grouped range citation at `static-canonical-preflight.md:54`; S001/S002/S003/S004/S006 HOLD as limited premises, S005 STALE as support |
| used-by old→new | 6 rows, tabulated in §3, all inside the contract-allowed cell |
| Citing-set denominator | 57 frozen + 1 discovered = 58, monotone growth only |
| Worktree-state frozen-logic simulation | citingPairs 58, decided 58, missing 0, findings 0 (not a committed-revision run) |
| Tool installs | none |

Artifact paths: `.ufo/waves/round-27/w1/DraftSources.md` (this report); `.ufo/waves/round-27/pairs.json` (18
adjudications); `.ufo/waves/round-27/discovered-pairs.json` (1 discovery); `.ufo/waves/round-27/fetched/manifest.json`
+ `fetched/text/*.txt` (8 retained opens); `corpus/lessons/round-27.md` §Source routing changes (old→new table);
`corpus/knowledge/static-canonical-preflight.md` §Round-27 grouped-citation adjudication;
`corpus/knowledge/sitemap-orphan-audit.md` §Round-27 provenance-range clarification;
`corpus/knowledge/ghp-served-set.md` §Round-27 attribution and evidence-pointer recheck.

Report: .ufo/waves/round-27/w1/DraftSources.md
