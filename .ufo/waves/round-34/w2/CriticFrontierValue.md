# CriticFrontierValue — did round 34 advance the web-properties frontier in a way an operator can use? (advisory)

Read at lane 24a16474 (sandbox clone): `corpus/knowledge/link-preview-metadata.md` (entry), `scripts/link_preview_audit.py`, `SKILL.md:993-1024`, and the wave-1 reports ScoutDs4ccTemplateSource, ScoutOgUrlCanonicalSitemap and ScoutOwnedPropertiesOG. Sandbox: `/fast/scratch/hyaku/kake-r34/w2/CriticFrontierValue/`. Axes: freshness (judged), operability.

Short answer: partly. The census is fresh and correctly scoped, and the tool is usable offline. But the fix guidance is not safe to follow as written for two of the 15 pages. It also never sends the operator to the publish paths that actually emit two of the defects, and nothing tells anyone when the census goes stale.

## Findings

1. **Freshness of the census holds today (no defect).** `git ls-remote https://github.com/VeigaPunk/ds4cc-marketplace.git` (exit 0) still shows `refs/heads/main` = `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`, the commit the census line pins. The workflow in the upstream read-only clone (`git show 7fc6aa2f:.github/workflows/pages.yml`) checks the repo out into `ds4cc-marketplace/` and uploads `./ds4cc-marketplace`. So the deployed tree is the repository root, and there is no step that writes HTML. Counting the 102 source pages is the right population for "what we publish". Scoping holds: entry lines 4, 125-126 and 142-145 confine claims to source markup.

2. **Counterexample: the fix guidance, followed literally, certifies the bloat/exa defect into `og:url`.** Entry lines 149-152 say to add all four properties to the 15 unmarked pages and to "Keep `og:url` equal to the canonical link". On `bloat.html` the canonical is `https://ds4cc.com/bloat` (`bloat.html:384`), while the sitemap advertises `…/bloat.html`. I added exactly that block in the sandbox (`followguide/bloat.html`, sha256 b5f3cf4d…; original 57d05e9d…).
   - `link_preview_audit.py --manifest followguide/lp.json` exits 0, verdict `clean`.
   - `canonical_audit.py --manifest followguide/ca.json` (expectedCanonical = sitemap loc) exits 1 with `canonical_mismatch`.
   - S068 says "Likes and Shares for this URL will aggregate at this URL", so shares would collect at an extensionless URL that nobody has confirmed resolves (entry lines 209-210).
   - The wave-1 addition at lines 203-208 routes this to the canonical preflight, but the fix section never orders it first.
   - Smallest correction: one bullet in "Fixing the source" saying to resolve canonical versus sitemap for `bloat.html` and `exa.html` (run `scripts/canonical_audit.py`) before adding `og:url`. Axes: operability, correctness of guidance.

3. **The canonical preflight already catches bloat/exa, but no round-34 artifact runs it.** In the sandbox, `canonical_audit.py --manifest html/manifest-canon.json` exits 1 with `canonical_mismatch` on both pages. `grep canonical_audit` over `.ufo/waves/round-34`, the entry and `corpus/lessons/round-34.md` matches only `w1/CriticFrontierNovelty.md`. So "belongs to the canonical preflight" is correct, but the operator gets no command or receipt for it.

4. **Two "manifest version 1" formats reject each other.** The link-preview manifest is `{file,url}` and the canonical manifest is `{url,file,expectedCanonical}`. Feeding either one to the other tool gives `input_invalid`, exit 2 (both directions run). An operator who wants both checks on the same pages has to write two manifests, and nothing builds either one from `sitemap.xml`. The only builder is `.ufo/waves/round-34/real_input_run.py`, which is wave scaffolding hard-wired to the retained archive. Operability gap; it does not break the round's claims.

5. **The fix section is source-only, but two reported defects come from other publish paths.**
   - (a) The `ds4cc.kimi.page` relative `og:url="./"` (served capture `.ufo/waves/round-23/live/ds4cc-kimi/page.html:8`, sha256 108f5aca…) is not in the source. Source `index.html:10` has `https://ds4cc.com/`, and `git log --all -S'content="./"'` in upstream returns nothing. `SKILL.md:19` says the mirror is published from a Kimi chat surface and is stale (about Aug-29). Its fix is a re-publish there, not a source edit.
   - (b) `burnerchrome/README.md:19` at 7fc6aa2f names a Vercel mirror (`burnerchrome.vercel.app`), and commit 3586cf7 calls the vendored copy the canonical. ScoutDs4ccTemplateSource flagged this. Neither the entry nor `SKILL.md` mentions the mirror, so editing the 11 burnerchrome heads in ds4cc lets the two copies diverge.
   - Correction: one sentence per path in "Fixing the source", marked as operator-gated.

6. **The tool does find a real `og_url_not_absolute` case.** I ran the landed tool on five retained round-23 served roots (`served/manifest.json`; exit 1). Findings: `og:image` missing on ds4cc.com and ds4cc.kimi.page; `og_url_not_absolute` on ds4cc.kimi.page; all four properties missing on burnerchrome.kimi.page; plazir15 and charter Pages clean. This matches ScoutOwnedPropertiesOG. So the absolute-URL rule has a real-world case, which the source-only real-input run (`real-input-at-5613071.json`) could not show. The `og_url_not_canonical` and `og_type_multiple` rules still have no real-input case.

7. **`og:image` guidance is too vague to act on for the defect that dominates (101/102).**
   - Line 153 says to add a new image URL "where an image is wanted". The tree has no social image (ScoutDs4ccTemplateSource lines 64-69). The page cache advice at lines 152-154 is about replacing an image, not adding the first one.
   - The audit stays clean on an `og:image` that points to an asset not in the tree. My sandbox page uses the made-up `/assets/social-card-v1.png` and still passes. This is documented as unchecked, yet it could be checked offline against the source tree without any network.
   - S068's "Basic Tags … you should use for all content types" include `og:description`, which appears 0 times in the entry.
   - Correction: name the asset and decision as an operator step, and say that the offline audit does not check that the image exists.

8. **Operator gating is correctly stated.** Lines 157-159 keep push, deploy and the Sharing Debugger re-scrape with the operator. No seat touched an owned host (I made no live request either). Provenance is honest: the wave-1 additions are marked as not counted toward C2 (line 181).

9. **There is no drift alarm on freshness.** `grep -c` for `7fc6aa2f`, `link.preview` or `ogCensus` is 0 in both `corpus/knowledge/freshness-pins.json` and `scripts/freshness-sweep.mjs`. A new upstream commit that changes Open Graph tags would not trip anything until the 90-day manual recheck (line 3). Smallest correction: a pin on the ds4cc `main` SHA and the census line, in the sweep's existing equality-predicate style. Axis: freshness.

## What would falsify this round's frontier value
- Upstream `main` moving past 7fc6aa2f with head changes. Not true at the time of my `ls-remote`.
- Served ds4cc.com bytes whose Open Graph block differs from the source. The round-23 root (sha256 ccb3f46e…, 76159 B) differs from source `index.html` (d0a2f357…, 77625 B) only from line 525 on, so the Open Graph block is the same. That capture predates 7fc6aa2f, and checking it again needs an operator-gated fresh capture.
- A deploy step or edge layer that injects tags. The workflow has none; edge injection was not modelled.

## Next frontier step (advisory)
- Prepare an operator handoff patch in a sandbox:
  - canonical/sitemap fix for bloat and exa;
  - Open Graph block for the 11 burnerchrome pages and `exa`/`bloat` (skip the `burnerchrome.html` refresh shim);
  - one raster social image and an `og:image` line for the 86 other pages.
- Add a sitemap-driven manifest builder that feeds both audits.
- Add the freshness pin from finding 9.
- Route the kimi re-publish (finding 5a) to the operator.

## Commands (all in sandbox unless noted; exit codes observed)
- `git clone -q <lane> clone && git checkout -q 24a1647…` → 0; `tar -xJf …/html.tar.xz -C html` → 0
- `git ls-remote https://github.com/VeigaPunk/ds4cc-marketplace.git HEAD refs/heads/*` → 0 (main = 7fc6aa2f)
- `git -C /fast/scratch/hyaku/kake-r33/ds4cc-upstream show 7fc6aa2f:.github/workflows/pages.yml` → 0; `log --all -S'content="./"'` → 0, empty; `show -s 3586cf7` → 0
- `canonical_audit.py --manifest html/manifest-canon.json` → 1; `link_preview_audit.py --manifest html/manifest-lp.json` → 1 (Open Graph missing only)
- Each tool fed the other's manifest → 2 (both); `followguide/lp.json` → 0 clean; `followguide/ca.json` → 1
- `link_preview_audit.py --manifest served/manifest.json` → 1 (findings in item 6)

Not verified: whether `https://ds4cc.com/bloat` and `/exa` resolve (owned host); live served state today; whether the Vercel mirror shares bytes; any platform rendering. No tools installed or updated. Lane writes: this report only.
