# SkillTableCheck — round 29 wave 2 (falsify)

Item attacked: SKILL.md section "Project-site base-path triage — round 29" (SKILL.md:699-718) at lane
commit 7697990cbca20291f3b0367b8ff4220e93b38b03. Sandbox clone: /fast/scratch/hyaku/kake-r29/w2/SkillTableCheck/clone
(TMPDIR inside the sandbox). No installs. No network. No lane mutation besides this report.

## Byte prefix (base fe1805cf → 7697990)
- `git show fe1805cf:SKILL.md` = 78147 bytes, ends in `\n`; `git show 7697990:SKILL.md` = 82289 bytes.
- `head -c 78147 new.md | cmp - base.md` → exit 0. sha256 of both = 04995d900bb14719…d6f2a.
- `git diff fe1805cf 7697990 -- SKILL.md` is one hunk `@@ -695,3 +695,24 @@`, additions only.
- Verdict: holds.

## Tool CLI and exit codes (scripts/base_path_audit.py at 7697990)
Contract: exits 0/1/2/64 (lines 60-63), reasons `outside_base_path`/`input_invalid`/`page_outside_base_path`
(65-67), usage path prints JSON to stdout and returns 64 (745-749), reference set includes `a[href]` (76-89).
Probes in sandbox `probes/`, manifest `{version:1, basePath:"/repo/", pages:[{file:"index.html", url}]}`:
- r1 `<link href="/style.css"><img src="/img/a.png">` → exit 1, two `outside_base_path` findings, each with element, attribute, value, resolved.
- r2 `<a href="/about/">` → exit 1, resolved `https://owner.github.io/about/`.
- r4 `<base href="/"><link href="style.css">` → exit 1, resolved `https://owner.github.io/style.css`.
- r6a page url `/other/` → exit 2 `page_outside_base_path`; r6b manifest not JSON → exit 2 `input_invalid`; r6c `ftp:` page url → exit 2 `input_invalid`.
- no `--manifest` → exit 64; duplicate `--manifest` → exit 64; both print JSON `verdict:could-not-evaluate` to stdout. `--help` → exit 0.
- Real input: re-ran the tool directly on `.ufo/waves/round-29/real-input/sites/{charter,lucario,plazir15}-ghp/manifest.json`
  → exits 1/0/1, findings 3/0/1, all `('a','href')`; matches out/summary.json (totals findings 4). Page sha256
  7c243a1d…aba / bee2d9f5…cff / d82af77a…18e equal `.ufo/waves/round-23/live/*-ghp/page.html` (round-23 snapshots).

## Source support (retained texts)
S040-S043: `.ufo/waves/round-29/sources/S04{0..3}.txt`. S024: `.ufo/waves/round-26/fetched/S024-1.raw.gz`
(sha256 fd9ae4b6…b959, equals round-26 manifest) contains "If there are multiple base elements with href
attributes, all but the first are ignored." Intro quotes of S040 (default site location row, both site kinds) are present.

## Per-row verdicts (SKILL.md line)
| Line | Symptom | Check vs tool | Citations | Verdict |
|---|---|---|---|---|
| 712 | Asset 404s on project site | matches (r1) | S040 location; S041 relative_url filters; S042 "Prepend baseurl config value"; S043 `base` to `'/<REPO>/'` in vite.config.js | holds |
| 713 | Links jump to owner root | matches (r2) | S042 relative_url, S043 base, S040 location; S041 cited but not used in the row text (it still supports filters) | holds |
| 714 | Custom domain vs github.io | no tool claim | S043 `'/'` for user site or custom domain and `'/<REPO>/'` quoted correctly; S041 "unless a custom domain is specified" verbatim | holds, with limits stated below |
| 715 | `base` element rewrites refs | matches (r4) | S024 supports "first base href sets the base"; S040 premise ok; **S043 has no base-element text** (grep for `<base`/"base element" in S043.txt: 0 hits) | limit: S043 does not support this row |
| 716 | Local preview green | no tool claim | S041 `bundle exec jekyll serve --baseurl = ""` on localhost:4000 verbatim; S043 `npm run preview` serves `dist` at localhost:4173 verbatim | limit: see below |
| 717 | Exit 2 or 64 | matches (r6a-c, usage probes; JSON on stdout for both) | S040/S043 only back the basePath shape; exit codes are tool facts, no source needed | holds |
| 718 | Sibling-project `a href` | matches (real-input rerun: 4 findings, all `a href` to other veigapunk.github.io projects) | S040 owner-host location | holds |

## Limits and smallest corrections
1. Line 715 cites S043, which says nothing about the HTML `base` element (Vite `base` is a build option, a name
   collision). Correction: drop S043 from that row's Cited ids (S040, S024 remain sufficient).
2. Line 716 calls Vite `npm run preview` a "local root preview". The retained S043 text says only that it
   "serves the files from dist at http://localhost:4173" and calls it "an easy way to check if the production
   build looks OK"; it does not say the preview ignores `base`. [INFERENCE] Vite's preview server normally
   serves under the configured `base`, so with `base: '/<REPO>/'` a stray root-relative reference could fail
   locally too. Not verified (no network, no Vite run). Correction: limit the "root preview" claim to the
   Jekyll `--baseurl ""` case, or say "a preview served from the root" without naming Vite.
3. Line 714 cites S042, which the row text never uses; and "A custom domain does not change the repository
   name (S041)" paraphrases a heading in S041's User and Organization Pages section, not the Project Pages
   section. Tradeoff, not a factual error; optional correction: drop S042 from the row.
4. Line 718 lists subresources as `link, script, img, source, iframe`; the tool also checks audio, video, track,
   embed and video[poster]. Incomplete list, not wrong.

## Not verified
- Did not run `scripts/base_path_selftest.py`, the C1/C2 counters, or `real_input_run.py` (it writes into the lane path).
- Did not reopen any public URL; source support judged only against retained texts at 7697990.
- Did not check that the S040-S043 `.txt` files are faithful extractions of their `.html.gz` bytes.

Overall: byte prefix holds; every Check column matches the landed CLI and exit codes; two rows (715, 716) carry
citation or wording overreach that the smallest edits above would fix.
