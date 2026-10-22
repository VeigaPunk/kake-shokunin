# AttackEntryBreaks — round 29, wave 2 (falsify)

Item attacked: the section "Which references break" in `corpus/knowledge/pages-base-path.md`
at lane commit 7697990cbca20291f3b0367b8ff4220e93b38b03 (lines 23-27). Axis: freshness (source provenance).
Sandbox: /fast/scratch/hyaku/kake-r29/w2/AttackEntryBreaks/ (clone checked out at 7697990, TMPDIR inside the sandbox).
No installs. No network. No lane mutation apart from this report.

## Commands (all run, exit codes observed)
1. `git show 7697990:corpus/knowledge/pages-base-path.md`: exit 0
2. `git show 7697990:.ufo/waves/round-29/sources/S04{0,1,2,3}.txt | grep -o -i -P '.{0,160}(relative|resolv|\.\./|site root|origin|subdirectory|hard-?cod|url filter|base element|<base|base href|outside|break|broken).{0,200}'`: exit 0.
   S040: no match. S042: only the relative_url row. S043: only the "Breaking Changes" navigation label.
   S041: only "The subdirectory-like URL structure GitHub uses for Project Pages complicates the proper resolution of URLs. In order to assure your site builds properly, use the handy URL filters :", followed by the example `{{ 'assets/css/style.css' | relative_url }}` (no leading slash).
   None of the four texts contains `../`, "root-relative", "origin", or any base element.
3. Matrix cases D1, D4, D7, D11 and K6 read from `git show 7697990:.ufo/waves/round-29/c2-matrix.json`: exit 0
4. `git show 7697990:.ufo/waves/round-29/c1_quote_truth.py`: exit 0. Check b only requires each id to appear somewhere in the entry body. The quotes it checks come from `corpus/lessons/round-29.md ## Gate`. So C1 measures nothing about whether the bullets in this section are sourced.
5. Nested-page probe in the sandbox (`probe/`, basePath `/repo/`). Both pages contain `<a href="../other/">`; one page is `index.html` at `https://o.github.io/repo/`, the other is `sub/page.html` at `https://o.github.io/repo/sub/page.html`.
   Command: `python3 -B clone/scripts/base_path_audit.py --manifest manifest.json`, exit 1.
   Output: one finding only, for `index.html` (`resolved: https://o.github.io/other/`). `pagesChecked: 2`, `referencesChecked: 3`. The same `../other/` on the nested page resolves inside `/repo/` and is not flagged.

## Per-bullet verdicts

### Bullet 1, root-relative references (line 25): BROKEN on provenance; the behaviour itself is not disputed
- The claim that "under ordinary URL resolution `/style.css` resolves against the origin, not the base path, so on a project site it points outside the site" is inferred from URL resolution. No source supports it: S040–S043 never discuss root-relative references (command 2), and the entry cites no URL standard.
- The phrase "the condition the Jekyll remedy exists for" assigns a purpose to S041. S041 only says that the subdirectory-like structure "complicates the proper resolution of URLs", and its example input has no leading slash. The quote is real, but it does not state the root-relative condition.
- S042's worked example (`"/assets/style.css" | relative_url` gives `/my-baseurl/assets/style.css`) is indirect support at best.
- What `/style.css` actually returns on a project site (a 404, or the owner's user site) is unsourced. Wave 1 `w1/CriticEntryScope.md` item 8 reached the same conclusion, and the entry did not adopt it.
- D1 only pins the lane policy. It is not evidence about how GitHub Pages behaves.
- Needs [INFERENCE] on: "under ordinary URL resolution `/style.css` resolves against the origin, not the base path, so on a project site it points outside the site — the condition the Jekyll remedy exists for".
  The S041 quote can stay as the remedy citation. The D1 sentence is fine as written.

### Bullet 2, escapes above the base path (line 26): BROKEN on provenance and on scope
- False provenance: "(S041, on resolution under a subdirectory-like URL structure)" cites S041 for the `../` claim, but S041 never mentions upward or `../` references (command 2). The parenthetical admits this is paraphrase and still presents it as sourced.
- Overgeneral: "resolves outside the base path on a page served under it" is false for nested pages. The lane's own matrix case D11 expects `../a.css` from `sub/page.html` to stay inside the base, with only `../../x` flagged. The probe in command 5 shows `../other/` is flagged on the base-root page and not on `/repo/sub/page.html`.
- Correct: the policy name `outside_base_path` matches matrix case D4 and the audit output.
- Smallest safe correction: drop the S041 attribution, mark the sentence [INFERENCE], and scope it. For example: "[INFERENCE] a relative reference with more `../` segments than the page's depth below the base path resolves outside it (`../other/` on the base-root page; matrix D4, D11)."

### Bullet 3, the base element (line 27): HOLDS on scope; one sentence lacks a source id
- Correctly scoped: "Only the first base element with an `href` applies" keeps S024's attribute scope ("If there are multiple base elements with href attributes, all but the first are ignored", quoted in `static-canonical-preflight.md:198`).
  It avoids the wording that round 26 marked STALE in that entry (line 101, "first base in tree order"). It points at the lane rule, not at a new source.
  "None of S040–S043 discusses the base element" is true (command 2). The note on K6 cites S024 (c2-matrix.json, case `K6-first-base-element-wins`).
- Gap: the first sentence, "a `<base href>` changes what every relative reference resolves against, so `<base href="/">` sends relative references to the origin root, out of a project site", has no source id in this entry. The entry's `source:` header lists only S040–S043.
  S024 (SOURCES.md:32) is the lane source for the document base URL. Either cite S024 inline or mark the sentence [INFERENCE].
  The audit honouring the rule (D7, K6) is policy, not provenance.

## Sentences that need [INFERENCE] markers (or a real source)
1. Line 25: "under ordinary URL resolution `/style.css` resolves against the origin … the condition the Jekyll remedy exists for".
2. Line 26: the entire `../` sentence. Remove "(S041, …)" and add depth scoping.
3. Line 27: "a `<base href>` changes what every relative reference resolves against … out of a project site". This one can cite S024 instead of being marked.

## Outside the target, observed once
Line 32 says "`absolute_url` for page URLs that can change (S041)". In the S041 retained text, the comment "For documents/pages whose URLs can change..." sits above `{{ page . url | relative_url }}`, not `absolute_url`. SOURCES.md:49 also states that S041 "says nothing about absolute_url". This looks like the same kind of false provenance; I did not investigate it further.

## Not verified
- No live source was reopened. I relied on the committed retained texts; I did not recheck their sha256 against receipts.json, and I did not run the C1 counter.
- I did not run the C2 counter or the selftest. Only the single probe in command 5 was run against the audit.
- I did not check WHATWG URL or RFC 3986 text for root-relative resolution; no such row is cited by this entry.
