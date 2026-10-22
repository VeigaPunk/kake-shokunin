# Round 29 wave 2 — AttackEntryCustomDomain

Item attacked: `corpus/knowledge/pages-base-path.md` at lane commit 7697990cbca20291f3b0367b8ff4220e93b38b03, sections "What changes under a custom domain" (lines 44–49) and "Reading a finding" (lines 58–60). Axis: freshness (with operability read-through).
Sandbox: /fast/scratch/hyaku/kake-r29/w2/AttackEntryCustomDomain/clone (checked out at 7697990, HEAD verified); TMPDIR inside the sandbox. No network, no installs.

## Commands (all run in the sandbox clone)
- `git clone -q <lane> clone && git -C clone checkout -q 7697990…` → exit 0; `rev-parse HEAD` = 7697990cbca2…
- `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision 7697990…` → exit 0, `C1 4/4`.
- `sha256sum .ufo/waves/round-29/sources/S04{0,1,3}.txt` → 625f2b07…, 86a77ee2…, d665dd23… (match entry line 2).
- `grep -o` on the retained source text (S040/S041/S043.txt) for each quoted custom-domain phrase → every quote found verbatim (single-line files, line 1).
- `python3 -B .ufo/waves/round-29/real-input/real_input_run.py --tool scripts/base_path_audit.py --sites .ufo/waves/round-29/real-input/sites --out $TMPDIR/rerun` → exit 0; totals sites=3 refs=114 findings=4 failedSites=2 contractProblems=0. The per-site `result` objects equal the committed `out/*.json` (all three True).
- `sha256sum` of real-input/sites/*/page.html against .ufo/waves/round-23/live/*/page.html → identical (7c243a1d…, bee2d9f5…, d82af77a…); round-23 fetch.json `fetchedAt` values are 2026-10-21T06:33:03Z, 06:33:04Z and 06:33:17Z.
- Python HTMLParser pass over the three snapshots that classifies every href/src/srcset/poster/action value by shape (absolute, root-relative, document-relative, fragment).

## Per-bullet verdicts — "What changes under a custom domain"
1. Line 46, S040 “You can host your site on GitHub's github.io domain or your own custom domain.” — **holds.** The quote is verbatim in S040.txt, in the *Hosting on your own custom domain* row.
2. Line 47, S041 “Custom domains do not affect repository names” plus “initially configured to live under the username.github.io subdomain” — **holds.** Both are verbatim. In S041 the first is a callout title in the User and Organization Pages section, followed by "…which is why repositories must be named this way even if a custom domain is being used". The entry attributes the second quote to a user or organization site, which matches that section.
3. Line 48, "A project site under a custom domain is published at the domain root" — **limit to state (wording is too broad).** The quotes are verbatim: S041 says “(unless a custom domain is specified)” after “username.github.io/project”, and S043 says to “set base to '/'” for a custom domain. Together they support the case where a project site has its own custom domain. The bullet's wording also covers a second case: a project site whose owner's user site has a custom domain. GitHub documents that case on its "About custom domains" page, which is not in S040–S043 and which I did not open (no network authorization). [INFERENCE] In that case the project site is served at `<custom-domain>/<repo>/`, so a base path still applies. Wave-1 seat CriticEntryScope.md:33 already marks that rule U (unsourced). The entry's own caveat "S040 itself states only that a custom domain is possible" is accurate: the retained S040 text has no project-site/custom-domain mapping.
   Smallest correction: write "A project site with its own custom domain configured…", and add "Whether project sites under an owner's custom domain keep `/<repo>/` is not established by S040–S043."
4. Line 49, the [INFERENCE] "One artifact serves one shape … Moving between the two shapes needs a rebuild, not a redirect" — **broken as a general statement; holds only for builds that bake the base.** The counterexample comes from the lane's own owned bytes:
   - charter-ghp: same-site references are 8 document-relative values (`style.css`, `vessel.webp`, `i18n.js?v=…`, `main.js?v=…` and `papers/….pdf`), with 0 root-relative and 0 prefixed with `/charter-ufo-fsd/`.
   - plazir15-ghp: 17 document-relative values (`styles.css`, `assets/fonts/*.woff2`, `images/*.jpg`, `main.js`, `snake/` and others), with 0 root-relative.
   - An index page with only document-relative references resolves inside the site whether it is served at `/<repo>/` or at a domain root. Only the absolute canonical/alternate `<link>` values (charter lines 8–10, plazir15 line 10) and the og meta tags are tied to the github.io address.
   - The premise "a build for the domain root carries root-relative URLs" holds only for the documented remedies: Jekyll `relative_url` with `baseurl` empty, and Vite `base: '/'`.
   - Not checked: CSS `url()`, JavaScript-built URLs and deeper pages, which the audit and this check do not read.
   Smallest correction: "A build whose URLs carry the base (`baseurl`/`base` of `/<REPO>/`, or root-relative output for `/`) serves one shape; a build with only document-relative references that never climb above the site root can serve both."

## "Reading a finding" (line 60)
- "4 such findings" — **holds.** Sum of committed out/*.json is 3 (charter) + 0 (lucario) + 1 (plazir15) = 4, and the sandbox rerun reproduces it.
- "all navigation links … no subresource" — **holds.** All 4 findings are `element: "a"`, `attribute: "href"`:
  - charter page.html#21 and #27 point to veigapunk.github.io/horizon-halo-comma-design/;
  - charter page.html#54 points to veigapunk.github.io/plazir-15-site/;
  - plazir15 page.html#38 points to veigapunk.github.io/xbrd-spark/highlights.html.
  All four are on the shared owner host and none is a subresource.
- "to sibling projects" — **limit to state.** The `/<name>/` first segment on the owner host is consistent with project sites, and plazir-15-site is one of the three audited properties. Whether horizon-halo-comma-design and xbrd-spark are published repositories is not shown by the bytes. The charter page has no github.com link for horizon-halo-comma-design. The entry itself says (line 55) the audit "cannot … identify which repository publishes a site". Suggested wording: "links to other paths on the owner host".
- "the round-23 GET snapshots … saved bytes from 2026-10-21" — **holds.** Hashes match round-23/live, and fetchedAt is 2026-10-21.
- Reader-trap (not a false statement): "no subresource finding" does not mean no subresource leaves the site. The audit ignores references to other sites (base_path_audit.py:37, :581). For example, lucario-ghp's only reference is `<script src="https://cdn.jsdelivr.net/pyodide/v0.28.2/full/pyodide.js">`. Lucario's "clean" verdict therefore covers 0 same-site references, which makes it vacuous.
  Optional correction: append "references to other hosts are outside the audit's scope".
- Minor: the bullet's subresource list (`link, script, img, source, iframe, track`) omits `audio`, `video`, `embed`, `srcset` and `poster`, which line 53 says the audit reads.

## Not verified
- I did not open GitHub's "About custom domains" page, so the owner-custom-domain case is unopened and [INFERENCE].
- I made no live probe of any owned property.
- I did not check whether the three linked targets exist.
- I did not read CSS or JavaScript reference shapes.

## Impacted axes
Freshness: bullets 3 and 4 carry an unsourced generalization. Operability: the "Reading a finding" guidance is accurate but has a scope gap for references to other hosts. Nothing here breaks the C1 4/4 or C2 counters.
