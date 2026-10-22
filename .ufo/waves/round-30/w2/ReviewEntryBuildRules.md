# W2 ReviewEntryBuildRules — render-static-sites.md, "Publish directory and build" + "Redirect and rewrite rule order"

Axes: freshness (quote-truth of the two attacked sections against retained S049/S050) and operability (reproducible checks). Godspeed framing; leaf seat; no subagents, no live requests, no lane mutation.

## Method and commands (all exit 0)

All checks are read-only python3 against the lane at the working copy (451e98f is HEAD content of the two files; no git/jj commands run).

1. `python3` (eval device): split the two sections into sentences, extract every curly-quoted span, test exact substring against `.ufo/waves/round-30/sources/S049.txt` / `S050.txt`, recompute sha256 prefixes.
   Result: 16/16 quotes are byte-exact substrings; sha256 prefixes `3604f8f55e5ef2a9` (S049) and `1c41364393defcba` (S050) match the entry header at `corpus/knowledge/render-static-sites.md:2`.
2. `python3`: context windows (±260–300 chars) around every quote occurrence in the retained blobs.
3. `python3`: token scan of both blobs for `publish directory`, `root directory`, `output directory`, `Build Command`, `build command`, `render.yaml`, `Blueprint`, `301`, `302`, `Moved Permanently`, `Found`.

## Verdict table — sentence (entry line) -> quote found -> judgment

Quote-found means: exact substring of the named retained blob (byte-exact, unique occurrence).

### Publish directory and build

| Sentence (line) | Quote found | Judgment |
|---|---|---|
| Dashboard asks build details, branch included (:23-24) | "specify your build details (including which Git branch to deploy)" S049 | supported — S049: "In the Render Dashboard, click New > Static Site: Connect your repo, specify … and click Create Static Site." |
| Names no publish/root/output-directory field; only other build-time setting is dependency installation (:25-27) | "By default, Render automatically attempts to detect and install your static site's dependencies." S049 | supported — token scan: the three directory tokens 0 occurrences in S049 and S050; `Build Command` 0; the single `build command` hit is inside the SKIP_INSTALL_DEPS sentence itself, consistent with the claim |
| [INFERENCE] publish directory configured on an unretained page (:27) | none | correctly labelled [INFERENCE]; safe wording ("cannot state how it is chosen") |
| Manual install via env var, own command takes over (:28) | "If you prefer to install dependencies manually, add a SKIP_INSTALL_DEPS …", "You can then include your own dependency installation as part of your site's build command." S049 | supported — context confirms the opt-out structure ("By default … If you prefer …") |
| Builds per-push and atomic; success deploys + invalidates CDN (:29) | "We build your site with every push to your deployed branch, and each build is fully atomic." + "As soon as a build succeeds …" S049 | supported |
| Served from global CDN, edge caching (:30) | "Render serves your site over a blazing-fast, reliable, and secure global CDN." + "We cache your content on network edges …" S049 | supported |
| Server-rendered app belongs to another service kind (:31-32) | "Deploying a dynamic site, such as a Rails app? Create a web service instead of a static site." S049 | minor overreach (unlabeled gloss) — doc says "dynamic site"; equating that with "server-rendered application" is an inference from one example, unlabelled |

### Redirect and rewrite rule order

| Sentence (line) | Quote found | Judgment |
|---|---|---|
| Rules live in the dashboard, **not in the site** (:36) | "Define redirect and rewrite rules for your site's paths directly from the Render Dashboard—no code required." S049; "When the path of an incoming request matches a rule's Source …" S050 | **overreach** — see F1 |
| Redirect is client-visible 301; rewrite is not; browser can't detect (:37) | "Instructs the browser … via a 301 Moved Permanently response code.", "Does not redirect the browser. Instead …", "The browser can't detect …" S050 | supported — `302` occurs 0 times in S050; 301 is the only code the retained text names |
| Existing resource outranks any rule, first branch (:38-39) | "Render does not apply redirect or rewrite rules to a path if a resource exists at that path." + "Render simply serves the resource at that path." S050 | supported — S050 flowchart order confirmed: resource? -> serve : rule? -> first match : 404 |
| Only then rules apply, first match wins, else 404 (:40) | "Apply the first matching rule (starting from the top of the list)" + "Return 404 Not Found" S050 | supported |
| Redirect to another path re-enters process (:41) | "If this process results in a redirect to another site path, the process repeats with the new path." S050 | minor dropped qualifier — see F2 |
| Domain root can't carry a rule; source needs >=1 component (:42) | "You can't apply redirect/rewrite rules to your domain root." + "Each Source requires at least one URL path component (such as /blog , or even / )." S050 | supported — the root-vs-`/` tension is the doc's own and is faithfully juxtaposed |
| Source is a path; destination path or absolute URL (:43) | "Source must be a path (not a full URL)." + "Destination can be either a path or a full, publicly accessible URL." S050 | supported with minor gloss loss — see F3 |
| Wildcards capture in source, reappear in destination (:44) | "In Source , * matches any string that appears starting at that position in the path." + "In Destination , * applies the entire string captured by the wildcard in Source ." S050 | supported — entry omits doc's "Specify /* to match all paths" and the Placeholders section; omission, not contradiction |

## Findings by severity

**F1 (medium, overreach — entry:36).** "Rules live in the dashboard, **not in the site**" states exclusivity. The quoted span supports only "defined in the dashboard" and "no code required"; neither S049 nor S050 says rules cannot be declared in the repository (S050's only `render.yaml` occurrence is nav). The entry's own retained evidence cuts the other way: S052 body text says "Configure this in any of the following ways: Render Dashboard … Blueprint (render.yaml) … Render API" (S052@~6447, quoted at entry:105-106), and entry:106-108 concludes "a repository file can carry at least some domain settings". A repo-file config surface for at least some service settings is held by this very entry, so the flat "not in the site" needs an [INFERENCE] label or a hedge ("declared in the dashboard, without code" — or "the retained pages name only the dashboard").

**F2 (low, dropped qualifier — entry:41).** "lands on another path" drops "site" from "another **site** path". Material within this same section: entry:43 (and S050) allow a Destination that is a full URL on another host; the doc scopes repetition to site paths only. As written, the sentence can be read to include off-site redirects.

**F3 (low, gloss loss — entry:43).** "absolute URL" replaces "full, **publicly accessible** URL". The accessibility qualifier is the doc's own and is dropped.

**F4 (low, unlabeled inference — entry:31-32).** "a server-rendered application belongs to another" — the doc's category is "dynamic site, such as a Rails app"; the equivalence is a gloss, not labelled [INFERENCE] like neighboring inferences in this entry are.

## What I did not verify

- No live fetch of S049–S052 (this seat may not GET); freshness rests on the round's receipts at 2026-10-22T11:49Z and the sha256 match noted above.
- I judged only the two assigned sections; the GitHub-Pages contrast section and other sections are other seats' scope. (Adjacent spot-check: entry:105 "Blueprint (render.yaml)" is a true S052 substring, body occurrence confirmed.)

Residual risk: low. One medium overreach (F1) plus three wording-level findings; no unsupported quote and no false quote-span anywhere in the two sections.
