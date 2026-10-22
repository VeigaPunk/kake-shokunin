# AttackEntrySiteKinds — round 29, wave 2 (falsify)

Item attacked: the section "What a project-site base path is" in `corpus/knowledge/pages-base-path.md` at lane commit 7697990cbca20291f3b0367b8ff4220e93b38b03 (lines 17–21, three bullet sentences). I checked each sentence against the retained texts `.ufo/waves/round-29/sources/S040.txt` and `S041.txt` at that commit. Axis: freshness.

Overall verdict: **holds, with one fixable defect and two limits to state.** Every quoted span appears exactly once in its retained text. The section makes no claim about redirects, letter case or trailing slashes. The defect is the parenthetical note on line 20, which describes the spacing artifact backwards.

## Commands (all read-only in the lane; writes only in the sandbox /fast/scratch/hyaku/kake-r29/w2/AttackEntrySiteKinds/, with TMPDIR set inside it)
- `git show 7697990:corpus/knowledge/pages-base-path.md`: exit 0.
- `git show 7697990:.ufo/waves/round-29/sources/S04{0,1}.txt | sha256sum`: exit 0. S040 625f2b07…, S041 86a77ee2…; both match the entry header (line 2) and `sources/receipts.json` `textSha256`.
- Sandbox clone checked out at 7697990, then `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision 7697990cbca20291f3b0367b8ff4220e93b38b03`: exit 0, output `C1 4/4`, controlBroken false.
- Regenerated the text from `S040.html.gz` and `S041.html.gz` using `fetch_sources.py`'s own `visible_text`: body sha fac40d86 and 1e3149a8 match the receipts, and the regenerated text equals the retained text for both. My first attempt used my own reimplementation, which left out the trailing newline, and gave different hashes; I discarded it.
- Fixed-string count of each quote in the retained text, using `grep -oF | wc -l`: exit 0. Every quote listed below had a count of 1.
- Case-insensitive keyword scan of S040 and S041:
  - "redirect", "trailing", "slash", "base path" and "lowercase": 0 hits in both.
  - "case": one hit in S041, inside "Showcase", the site navigation.
  - "default": one hit in S040, the table row.
  - "subpath", "subdirectory" and "baseurl": one hit each, all in S041.
- Inspected the "Default site location" cell in the raw S040 HTML (python slice of `S040.html.gz`).

## Per-sentence verdicts
1. Line 19, "GitHub Pages is “a static site hosting service … repository on GitHub” (S040), and “There are two types … for a specific project.” (S040)": **holds.** Both quotes are verbatim, count 1 each. The first quote cuts the source sentence before ", optionally runs the files through a build process, and publishes a website"; the cut does not change the meaning, and line 31 quotes that clause.
2. Line 20, "The two types differ in published location, not only in repository layout: a project site's default site location is “http(s):/ / <owner>.github.io/ <repositoryname>” … while a user or organization site is the host alone": **holds on substance.** The quote is verbatim (count 1). The table's "Source files" and "Default site location" rows support "location, not only repository layout". "Host alone" matches the cell `http(s):/ / <owner>.github.io` (scheme plus host, no path).
   - **Defect (fixable, false provenance wording):** "the retained text collapses that cell's spacing" is backwards. The published HTML is `<code>http(s):/<wbr/>/<wbr/>&lt;owner&gt;.github.io/<wbr/>&lt;repositoryname&gt;</code>`. The text rule (`fetch_sources.py:36`) replaces each `<wbr/>` tag with a space, so the retained text *inserts* spaces, and GitHub's page shows no spaces. The wave-1 seat said it correctly (`w1/SrcS040AboutPages.md:85`: "tag stripping left a space"). The smallest fix is to say the retained text "inserts a space at each `<wbr>` break; the published cell reads http(s)://<owner>.github.io/<repositoryname>". The quoted bytes can stay as they are, because the counter needs the exact retained spacing.
   - **Limit (mild overstatement):** the opening clause "differ in published location" drops S040's qualifier "Default". S040 also says a site can use a custom domain, and S041's "(unless a custom domain is specified)" moves a project site off the subpath. The same sentence says "default site location" a few words later, so the overstatement stays local. A tighter wording is "differ in default published location".
3. Line 21, S041 "will become available under a subpath … (unless a custom domain is specified)" and "The subdirectory-like URL structure … complicates the proper resolution of URLs.": **holds.** Both quotes are verbatim, count 1 each.
   - **Limit (scope):** in S041 the first quote describes branch publishing: content "stored in a specially named gh-pages branch or in a docs folder on the master branch … rendered using Jekyll". The entry's "project page output" generalizes that without the branch-publishing scope. `corpus/SOURCES.md:49` records that S041 "says nothing about … Actions publishing", but the entry does not carry that scope. The second quote sits under S041's local-preview paragraph; quoting it alone does not distort its meaning.

Heading: neither S040 nor S041 uses the term "base path" (0 hits). S041 says "subpath", "subdirectory-like URL structure" and `--baseurl`. The heading term is the lane's own label and is not attributed to a source, so this is not an overstatement. The section has no explicit sentence defining the term.

## Redirect, case and trailing slash (the named overstatement examples)
- None of the section's three sentences makes a redirect, case or trailing-slash claim, and S040 and S041 contain none to support one. No overstatement was found on these points.
- S040's requested URL redirects to `what-is-github-pages` (receipt `finalUrl`; page title "What is GitHub Pages?"). The entry's source line 1 gives only the requested URL, but `corpus/SOURCES.md:48` records the redirect, so the provenance is complete in the registry.
- Outside the section: line 49's "needs a rebuild, not a redirect" is already marked `[INFERENCE]`.

## Impacted axes
- Freshness: provenance accuracy of the line-20 parenthetical (fixable). Quote truth is not affected: C1 is 4/4 and the bytes are verified.
- Operability: none.

## Not verified
- I did not open any live URL (no network). Whether the retained text still matches the live pages today is unchecked.
- I did not check S042, S043, or sections other than the target, apart from the line-49 note above.
- I did not run the C1 counter at other revisions or test its gates.

## Tooling
- No installs or updates.
