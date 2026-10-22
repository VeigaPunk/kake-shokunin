# Round 35 C1 repair — ExecToolRepair

Built in the sandbox clone at base `318561efa67206699fdaf259ffb86e39f2d916a8`; commit `9386bb806d3f01b10e355f3c703ece3abcc50f6c`.
Axes: operability addressed; freshness untouched.

## Behavior and files
- `scripts/link_preview_audit.py`: reports one `og_url_multiple` (`<page>:og_url_multiple:og:url`, property `og:url`) for >1 non-empty `og:url`, while retaining first-value URL checks. Ignores metadata/canonical links inside open template/svg/math contexts; matching closes and nesting are tracked; self-closed svg opens nothing. An unreadable page yields `page_unreadable`; other readable pages are audited, findings are combined, verdict/exit remain could-not-evaluate/2, and `pagesChecked` is readable count. `input_invalid` still short-circuits as before.
- Docstring cites the R35 C1 lane policy where opened sources do not specify it and updates the formerly false `does NOT check` and unreadable-result statements.
- `scripts/link_preview_selftest.py` optionally verifies fixture `pagesChecked` and exact `findingIds`, so the mixed unreadable/readable case checks page attribution as well as reason/property.
- Updated `input_policy_suppressed_on_input` expected result: `page_unreadable` plus readable page's missing type/image/url findings; `pagesChecked: 1` and IDs assert the page.

New fixtures (all under `scripts/fixtures/link-preview/`):
- `og_url_multiple_distinct` — distinct non-empty URLs produce exactly the multiple finding.
- `og_url_multiple_same_value` — repeated identical non-empty URL still produces it.
- `og_url_empty_duplicate_guard` — one non-empty plus whitespace-only duplicate stays clean.
- `template_suppressed_metadata` — nested template stays suppressed after inner close; wrong hidden canonical/title do not count.
- `svg_nested_suppression` — nested SVG contents stay ignored; valid metadata after outer close counts and stays clean.
- `math_suppressed_metadata` — hidden title/canonical do not count.
- `svg_self_closing_guard` — metadata after `<svg/>` counts and stays clean.
- `input_unreadable_with_clean_page` — unreadable plus clean readable page; pagesChecked is 1.
- `input_multiple_unreadable_with_policy` — two unreadable pages plus a readable og:type defect; all findings returned, pagesChecked is 1.
- `input_non_regular_with_policy` — directory page is unreadable while readable-page policy findings are returned.

## Commands and observed evidence
- Setup, exit 0: `mkdir -p /fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/tmp && unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/clone && git -C /fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/clone checkout -q 318561efa67206699fdaf259ffb86e39f2d916a8`.
- Selftest, exit 0: `export TMPDIR=/fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/tmp; timeout 300s python3 -B scripts/link_preview_selftest.py; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"`; observed 45 cases, 45 passed, 0 failed, `passedOverTotal: 45/45`, clean. Full output: `artifact://37822`.
- Matrix, exit 0: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && export TMPDIR=/fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/tmp && timeout 300s python3 -B .ufo/waves/round-34/c1_matrix_count.py --root /fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/clone --revision 9386bb806d3f01b10e355f3c703ece3abcc50f6c; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"`; observed 28/28, `constantGatesAllRejected: true` (clean 6/28, failed-empty 0/28, refuse 6/28, all-missing 1/28); tool SHA-256 `1a8b27243a00cede1b93f8d3e95201476c75b70a3bcaa59a7e51f2220e5f5ef4`.
- Real input, runner exit 0: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && export TMPDIR=/fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/tmp && timeout 300s python3 -B .ufo/waves/round-34/real_input_run.py --root /fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/clone --revision 9386bb806d3f01b10e355f3c703ece3abcc50f6c --census /fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/clone/.ufo/waves/round-34/verification/c2-at-d08d8de.json; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"`; observed `agrees: true`, pagesChecked 102, toolExit 1, missing counts equal census (image 101; title/type/url 15 each).
- Commit, exit 0: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && export TMPDIR=/fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/tmp && git -C /fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/clone add scripts/link_preview_audit.py scripts/link_preview_selftest.py scripts/fixtures/link-preview/ && git -C /fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/clone commit -m "Repair round-35 link preview audit"`; commit `9386bb806d3f01b10e355f3c703ece3abcc50f6c`.
- Patch, exit 0: `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && git -C /fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/clone diff 318561efa67206699fdaf259ffb86e39f2d916a8 > /fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/patch.diff && sha256sum /fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/patch.diff && wc -l /fast/scratch/hyaku/kake-r35/w1/ExecToolRepair/patch.diff`; observed 420 lines, SHA-256 `7e463fa7788e70cc24581e4535e8069ccd1f6c8393c18c2bf1feeb514e793a13`.

Evidence pointers: sandbox `scripts/link_preview_audit.py:8-15,20-27,29-52,89-138,244-305`; `scripts/link_preview_selftest.py:99-132` (SHA-256 `699734bc2f20c05e4aa92e07cb58cf7700aff17203834a911780945a5493b3b2`); the listed fixture expectations are each at `<fixture>/expected.json:1`. Coverage HTML: `template_suppressed_metadata/index.html:1`, `svg_nested_suppression/index.html:1`, `svg_self_closing_guard/index.html:1`; directory unreadable case: `input_non_regular_with_policy/manifest.json:1`. No tools installed. No sealed files were accessed.
## Risks / not verified
- Did not run the R35 sealed counter; sealed keys remain untouched and L1 owns scoring. L1 must run it after reveal/integration.
- Per L1's CriticHarmPlan, `SKILL.md:1010` still says “Exit 2 reports input findings only,” which conflicts with this contract; L1 will append the Skill correction.
