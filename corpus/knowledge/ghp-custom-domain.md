source: S003, S005, S007 (corpus/SOURCES.md) — https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site §Configuring an apex domain
verified-at: 2026-10-19 (GitHub Docs and REST API opened 2026-10-19)
recheck: on Pages behavior or docs change — curl -fsSL 'https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site.md' | grep -cF 'any existing `CNAME` file is ignored'

# Custom-domain authority by publishing mode

**Claim (falsifiable).** When a Pages site uses workflow publishing,
GitHub documents the custom domain as Pages configuration: an existing
repository `CNAME` file is ignored. The Pages API exposes `cname` separately
from `build_type`, which distinguishes `workflow` from `legacy`. This does
not establish the current mode or configured domain of any lane property.

**r20-correction at base `cb807bc`.** Refines `corpus/knowledge/publish-channels.md:9`
and `SKILL.md:16`: those lines attribute the domain to a repository file,
whereas the documented mechanism depends on Pages publishing mode.

**Source checks (quotes reopened 2026-10-19).**
- S005, Configuring an apex domain, step 4: “no `CNAME` file is created, and
  any existing `CNAME` file is ignored”; branch publishing instead creates
  a root file when the domain is saved. S005 recommends domain verification
  and warns against wildcard DNS records.
- S003, custom-workflow NOTE: “A CNAME file in your repository file does not
  automatically add or remove a custom domain.” It directs configuration to
  repository settings or the API.
- S007, Get a Pages site response schema: `cname` is string-or-null and
  `build_type` is `legacy`, `workflow`, or null; the update endpoint accepts
  both fields. No API call was made.

**Falsifier.** For the lane's ds4cc property, an operator-authorized read of
`GET /repos/{owner}/{repo}/pages` returning `build_type: legacy` would refute
applying the workflow-specific conclusion to its current setup. In that
branch mode, S005 says saving the custom domain writes a root `CNAME` file.

**Named debt.** The historical lane map labels ds4cc as Actions publishing
(`SKILL.md:16`; `corpus/knowledge/publish-channels.md:5-9`), but workflow pin
and current API `build_type` are unavailable after the 2026-10-12 checkout
prune. Owner: operator/webzites. Obtain an authorized free read and retain
only the relevant response fields; credentials and session material are
outside this evidence. Current `build_type` remains unknown.

**Recheck (2026-10-19).** The header argv returned `2` matches.

## How it clears corpus/QUALITY.md
- **Replayable claim:** gives the authoritative docs, exact recheck argv, and count.
- **Missing substrate stays visible:** current build mode remains debt with an owner.
- **Admission authority:** official Pages docs and API schema support the distinction.
- **Citation-local absence:** cites surviving lane lines, not the pruned workflow checkout.
- **Shape-only probe environment:** no API request or credential material is retained.

## Post-review correction — round 20 (2026-10-19)

S007 quote-format erratum: the earlier gate's “`cname`: required, string or
null” is a schema transcription, not a verbatim quotation of the rendered
GitHub Docs page (which reads “cname string or null”). The Markdown
representation fetched by the L1 exposes `cname`: required, string or null;
those representations must not be presented as an identical quote. The
field claim remains supported by S007 §Get a GitHub Pages site, response
schema; no API request was made.
