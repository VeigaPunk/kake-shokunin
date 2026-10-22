# ReviewEntrySectionTruth — sentence-by-sentence truth check of the two round-33 sections

Scope: `corpus/knowledge/sitemap-orphan-audit.md` lines 184–215 ("Round-33 ds4cc source pin 7fc6aa2f") and 217–253 ("Round-33 wave-1 additions") at `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`, read in my sandbox clone `/fast/scratch/hyaku/kake-r33/w2/ReviewEntrySectionTruth/clone`. Upstream read via my own clone `/fast/scratch/hyaku/kake-r33/w2/ReviewEntrySectionTruth/upstream` (HEAD `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`). Caveat: `.ufo/waves/round-33/w1/*.md` are untracked working-tree files (absent from the tree at tip); I read them read-only at the lane path as the named evidence.

## Sentence table

| # | Claim (audit.md line) | Verdict | Evidence |
|---|---|---|---|
| 1 | Reads pinned at `1fbdb8ed`; local clone `~/Projects/ds4cc-marketplace` still at that commit (:186-187) | supported | `git -C ~/Projects/ds4cc-marketplace rev-parse HEAD` → `1fbdb8ed…`, exit 0; S062 row SOURCES.md:70 |
| 2 | Upstream moved one commit to `7fc6aa2f…e884`, 2026-10-21T17:32:55Z, subject "magga: Frostbite — Classic & Remastered at /magga/frostbite/" (:188-190) | supported | upstream `git log`: `7fc6aa2f 2026-10-21T17:32:55Z`, parent `1fbdb8ed` (exactly one commit ahead) |
| 3 | Read 2026-10-22 through a sandbox clone (S065) (:190-191) | supported | S065 row SOURCES.md:73 names sandbox clone + full hash; blob ids listed there all match |
| 4 | Adds three pages under `/magga/frostbite/` (hub, classic/, remastered/) with scripts and covers (:191-193) | supported | `git diff --name-status`: 9 adds under `magga/frostbite/` (3 index.html, 4 .js, 2 covers) |
| 5 | Links them from `magga/index.html` (:193) | supported | `magga/index.html:365-371` at 7fc6aa2f carries the frostbite card + 3 hrefs (`./frostbite/classic/`, `./remastered/`, `./frostbite/`) |
| 6 | Adds three locs to `sitemap.xml` (lines 15–17) (:193-194) | supported | lines 15-17 = `/magga/frostbite/`, `/classic/`, `/remastered/`; 97→100 |
| 7 | Changes none of the four files S062 retains (:194-196) | supported | diff is 12 files, all `magga/**` + `sitemap.xml`; `render.yaml`, `apps-sdk/Dockerfile`, `apps-sdk/src/server.ts`, `.dockerignore` untouched; ScoutUpstreamCommitAnatomy.md:18-19 confirms blob-identical |
| 8 | `sitemap-locs: 100`, each canonical verdict = canonical_audit.py with expectedCanonical = loc (:199-206) | supported | I re-derived: XML parse of retained sitemap.xml → 100 locs; canonical_audit.py v1 manifests (counter's own format) on each retained page → `clean`, exit 0, ×3 |
| 9 | At `1fbdb8ed` the same file had 97 locs (:208) | supported | `grep -c '<loc>'` on 1fbdb8ed sitemap → 97; 7,614 B; sha256 `18c51c45…` matches :242 |
| 10 | Earlier counts historical (93 locs at `f3d2ecd`, 103 across three GHP rows 2026-09-28); section does not re-measure them (:209-211) | supported | kimi-subpath-audit.md:24 "(93 locs)"; audit.md:78-79 "93 + 8 + 2 = 103" dated r16 2026-09-29; `f3d2ecd` is not an object upstream anymore (annotated "at f3d2ecd" correctly) |
| 11 | Limits: source-side only; nothing fetched from ds4cc.com; deploy/live-sitemap unknown; `clean` is lane offline policy, not search-engine selection (:211-215) | supported | honest and precise; matches S066's own scope note (SOURCES.md:74 "not a statement about what ds4cc.com serves") |
| 12 | Checked against `7fc6aa2f` and lane `bc6c4a8`; reports under w1/ (:219-220) | supported | w1/ dir holds all named reports; ExecNewPagesRefIntegrity.md:34 recorded clone at `bc6c4a8` |
| 13 | Parity: 100 locs → tracked file (86 dir locs to index.html, 14 explicit file locs), 0 unmapped (:222-224) | supported | ExecSitemapTreeParity.md:5; my recount: 100 locs, 14 contain `.html`, 102 tracked `.html` files |
| 14 | `benchmarks/benxshitter-frontier.html` in no loc, also at `1fbdb8ed` (97/97 mapped) (:224-226) | supported | benxshitter absent from my locs.txt, present in html.txt at 7fc6aa2f; parity report:6 same at 1fbdb8ed |
| 15 | Three new pages' 21 relative/same-host refs all resolve; base_path_audit base `/` clean (:226-229) | supported | ExecNewPagesRefIntegrity.md:29 table = 21 rows all "yes"; base_path_audit exit 0 `{"referencesChecked":24,"verdict":"clean"}` (:31, :70); "Static source parity only" correctly scoped |
| 16 | Pages deploy run 39644779773 for 7fc6aa2f concluded success, started 17:32:59Z, updated 17:33:42Z; GitHub's record, not live observation (:230-233) | supported | gh-actions-runs-7fc6aa2f.json: `id 39644779773`, "Deploy marketplace to GitHub Pages", success, `created_at 17:32:59Z`, `updated_at 17:33:42Z`; wording honestly bounded |
| 17 | "Test Apps SDK wrapper" run 39644779805 concluded failure (:233-234) | supported | same JSON: id 39644779805, failure, apps-sdk.yml |
| 18 | Six most recent main-branch runs of that workflow (7fc6aa2f back to 480dd05f, 2026-10-14) all concluded failure (:234-238) | supported | gh-actions-apps-sdk-runs-main.json: exactly 6 runs, all `head_branch=main`, all failure, shas 7fc6aa2f→480dd05f (created 2026-10-14T21:32:49Z); retained path + read-time 20:06:32Z match S066 |
| 19 | The cause was not examined (:238) | supported | no counter-evidence in w1 reports |
| 20 | "93 locs" should-serve set stale: kimi-subpath-audit.md:24, this entry's lines 48–49 (:239-241) | supported | kimi-subpath-audit.md:24 has the literal; audit.md:48-49 has "93 locs, unpushed" |
| 21 | Round-24 "97 parsed loc elements" stays exact for `1fbdb8ed` (7,614 bytes, sha256 `18c51c45…`) (:241-242) | supported | audit.md:145 wording; my re-measure: 7,614 B, sha256 `18c51c45d62d…`, 97 locs |
| 22 | Round-23 "96 locs" readings are a live vintage, not a source state (:243-244) | supported | audit.md:135 (c3) is an HTTP 200 live observation of 96 locs on 2026-10-21 |
| 23 | `freshness-pins.json` still pins `pq2Remote` `e6bd0718` (29 behind `7fc6aa2f`) and `sitemapStatus` 404, contradicted by r23 live obs (:245-247) | supported | pins file carries both literals; `git rev-list --count e6bd0718..7fc6aa2f` = 29 exactly; r23 c3 records live 200 |
| 24 | Re-pinning needs the sweep's armed section, which fetches owned sites; not run this round (:247-249) | supported | freshness-sweep.md:21-22 armed skipped `--offline`; w1 ScribeSkillPinAdvanceTable.md:15 confirms only `--offline` ran (`§armed/§history skipped offline`); no w1/w2 artifact shows an armed run |
| 25 | `magga/frostbite/index.html:208` declares `width="1280" height="960"` for `covers/classic.png`, bytes 960×768 (:250-252) | supported | line 208 has those exact attrs; PNG IHDR parse → 960×768, 5,336 B (ScoutUpstreamCommitAnatomy F1:45-46) |
| 26 | Rendering governed by CSS `aspect-ratio` per that report; not verified in a browser (:252-253) | supported | `.preview img{…aspect-ratio:16 / 10;object-fit:cover}` at :116-119 applies to `img.pixel` inside `a.preview`; honest unverified-browser qualifier |

## Verdict

Zero unsupported or overstated sentences. The two sections are unusually disciplined: every number I could re-derive (100 locs XML-parsed, 97 at parent, 7,614 B / `18c51c45…`, blob ids `67d8c7a5`/`e0d9ee29`/`12c58e2d`/`4e6d70ae`, 29-commit distance, run ids/timestamps, 86/14 parity, 21 refs) matched to the byte. Deploy-run wording correctly limits itself to GitHub's record; the limits paragraph correctly disclaims live knowledge.

## Commands run (all exit 0 unless noted)

- `git clone -q <lane> …/clone && git checkout -q 0a0acfb…` → HEAD `0a0acfb…`
- `git clone -q https://github.com/VeigaPunk/ds4cc-marketplace.git …/upstream` → HEAD `7fc6aa2f…e884`
- `git diff --name-status 1fbdb8ed 7fc6aa2f` → 12 files (9 adds `magga/frostbite/**`, M `magga/index.html`, M `magga/README.md`, M `sitemap.xml`)
- `grep -c '<loc>'` on 7fc6aa2f / 1fbdb8ed sitemap → 100 / 97; retained sitemap sha matches; 1fbdb8ed sitemap 7,614 B sha256 `18c51c45d62d…`
- `git rev-parse 7fc6aa2f:<f>` vs `git hash-object` retained bytes → identical for all 4 retained files
- `git rev-list --count e6bd0718..7fc6aa2f` → 29
- ElementTree parse of retained sitemap → 100 `<loc>`; `scripts/canonical_audit.py --manifest` on each retained page → `{"verdict":"clean"}` exit 0 ×3
- PNG IHDR parse of `covers/classic.png` → 960×768; `git show` line 208 attrs `width="1280" height="960"`
- `git -C ~/Projects/ds4cc-marketplace rev-parse HEAD` → `1fbdb8ed…`; `cat-file -t 7fc6aa2f` → not present (exit 128, expected)
- JSON parses of both retained gh-actions files → all ids/conclusions/timestamps quoted above

## Residual risk / not verified

- w1 reports are untracked working-tree files; another seat could have edited them post-hoc. Content was internally consistent with my independent recomputation, so reliance risk is low.
- I did not re-run the seats' own analysis scripts (sitemap_tree_parity.py, analyze_refs.py); I recomputed the same quantities independently instead — results agreed.
- L1's named upstream clone `/fast/scratch/hyaku/kake-r33/ds4cc-upstream` currently reads as "not a git repository" via `git -C` (bare-layout quirk); I used my own clone, same HEAD.
- No live requests to owned hosts (bounded); "deployed to ds4cc.com" remains unknown by design.

Tooling: none installed; git 2.x, python3 stdlib only. No mutations anywhere in the lane besides this report file.
