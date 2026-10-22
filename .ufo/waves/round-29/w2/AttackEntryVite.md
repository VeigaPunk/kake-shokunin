# R29 w2 — AttackEntryVite

Item attacked: `corpus/knowledge/pages-base-path.md`, section "The Vite remedy" (lines 37–42), at lane commit
7697990cbca20291f3b0367b8ff4220e93b38b03. The source is S043, the retained text `.ufo/waves/round-29/sources/S043.txt`
at the same commit, with sha256 d665dd23b193b0a416e9d2e9b15e65e30b5644e5b513a9c834c0c2535b52dcba. That hash equals
`receipts.json` S043.textSha256. The S043 GitHub Pages section runs from character offset 3032 to 5489, where
"GitLab Pages and GitLab CI" begins. Axis: freshness, meaning grounding fidelity.

## Commands (sandbox /fast/scratch/hyaku/kake-r29/w2/AttackEntryVite, TMPDIR set there)
- `git -C <lane> show 7697990…:corpus/knowledge/pages-base-path.md` exited 0. `git -C <lane> show 7697990…:.ufo/waves/round-29/sources/S043.txt > S043.txt` exited 0, and `sha256sum` printed d665dd23…52dcba.
- `git clone -q <lane> clone && git -C clone checkout -q 7697990…` exited 0. `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision 7697990…` exited 0 and printed `C1 4/4`. The S043 check passed all four sub-checks, and its gate quote is the project-site `base` sentence.
- Python exact-substring and offset checks of every quoted span against S043.txt exited 0. The results are listed below.

## Per-bullet verdicts
1. Line 39: "Vite bakes the base into the build output, so set it before the build: “Set the correct base in vite.config.js .”"
   - The quote is verbatim at offset 3066. A second copy at 5518 sits in the GitLab section.
   - The lead clause is not supported by S043. The retained text contains no "bake", "build time" or "at build time". The only "build output" hits (offsets 1159 and 2346) are about the `dist` location, not `base`. S043 tells you where to set `base`. It never says the value is fixed into the emitted files.
   - The claim is very likely true from Vite's `base` config docs, but those docs are not a cited source. Line 49 of the entry depends on this claim through its "one artifact serves one shape" inference.
   - Verdict: **limit to state**. The quote holds, but the lead is an inference without the entry's own `[INFERENCE]` marker (that marker is used at line 49).
2. Line 40, "Project site …":
   - The quote is verbatim at offset 3331, with exactly 1 occurrence. The label "Project site" matches the S040 default-location row.
   - Verdict: **holds**.
3. Line 41, "User site or custom domain …":
   - Both quotes are verbatim, at offsets 3107 and 3248, with 1 occurrence each.
   - S043 says "to a custom domain through GitHub Pages" and does not separate user sites from project sites. The bullet's label stays within that wording.
   - Verdict: **holds**.
4. Line 42: "Pages does not run Vite: “GitHub will now deploy your site using a GitHub Actions workflow , which is necessary since Vite requires a build step for deployment.”"
   - The quote is verbatim at offset 3637, with 1 occurrence.
   - Verdict: **broken (overreach)**. The quote gives a reason why an Actions workflow is needed. It says nothing about what Pages does or does not run.
   - Strongest counterexample, from the same S043 section: the setup S043 recommends has GitHub run Vite as part of the Pages deployment.
     - "Under Build and deployment , open the Source dropdown, and select GitHub Actions ." (offset 3554)
     - "installs dependencies with npm, builds the site, and deploys it whenever you push changes to the main branch" (offset 4008)
     - "environment : name : github-pages" (offset 4703)
     - "name : Build run : npm run build" (offset 5084)
     - "name : Deploy to GitHub Pages id : deployment uses : actions/deploy-pages" (offset 5369)
   - Read plainly, "Pages does not run Vite" is false of the documented setup.
   - At most, the source implies that without the GitHub Actions source, Pages would not run the Vite build. Even that is an inference: S043 never mentions branch publishing or the Jekyll build.
   - The entry itself quotes S040 at line 31 saying Pages "optionally runs the files through a build process" (S040.txt offset 1591). S040's nav also lists "Use custom workflows". So the unqualified "does not run" also conflicts with the entry's own S040 grounding.
   - The phrase appears only at line 42 of the entry (git grep at 7697990 over `corpus`, `SCORECARD.md` and `README.md`), plus the frozen copies under `.ufo/waves/round-29/verification/reject-path/`.

## Why the counter does not catch it
`c1_quote_truth.py` checks four things: the registry row, that the entry body cites the source, the one gate quote in the lesson, and that this quote appears in the retained text. It never reads the lead text of a bullet. So C1 4/4 is unaffected by both defects: it is true but cannot tell whether a lead claim stays within its quote. Both defects are fixable wording problems, not tradeoffs.

## Smallest safe correction (for the L1; I made no edit)
- Line 42: replace the lead with wording S043 states, for example: "A Vite site needs GitHub Actions as the Pages publishing source, and the workflow runs the build: “Under Build and deployment , open the Source dropdown, and select GitHub Actions .” (S043); “GitHub will now deploy your site using a GitHub Actions workflow , which is necessary since Vite requires a build step for deployment.” (S043)." Both quotes are verified substrings.
- Line 39: either drop "Vite bakes the base into the build output, so" and keep "Set `base` before the build", or mark it `[INFERENCE]`, or cite the Vite `base` config page after opening it under the source gate.
- If line 39 changes, recheck the line 49 inference, which leans on it.

## Not verified
- No live GET of vite.dev. I had no network authorization, so freshness rests on the committed receipt from 2026-10-22T10:29:37Z and the wave-1 refetch reported in `w1/SrcS043ViteDeploy.md`. I did not repeat that refetch.
- I did not open the Vite `base` config docs, so the truth of line 39 beyond S043 is not established here.
- I did not run the C2 counter or the selftest, because they are out of scope.
- No tools were installed or updated.
