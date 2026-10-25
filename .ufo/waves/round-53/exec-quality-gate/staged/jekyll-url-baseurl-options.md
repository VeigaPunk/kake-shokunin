
source: S296 — https://jekyllrb.com/docs/configuration/options/ — § "Configuration Options" → option headings "Web Domain URL" (`url`) and "Base URL" (`baseurl`) (no publication date rendered — pinned by the option lines, fetched 2026-10-23) — fetched 2026-10-23
verified-at: 2026-10-23
recheck: 180d — `curl -fsSL 'https://jekyllrb.com/docs/configuration/options/' | grep -c 'baseurl: /PATH/TO/SITE'` -> 1 (ran 2026-10-23)
ground: static-site build and deploy toolchain — Jekyll/base-path tooling

# Jekyll composes the canonical site URL from two options, not one

The lane already holds the *filter* half of Jekyll's URL story (`relative_url` /
`absolute_url`, S042) and the *project-site path* half (S041). What was missing
is the **configuration** half: the two options that compose the canonical
production URL.

From S296, § "Configuration Options":

- **`url`** — option heading "Web Domain URL". Value form `url: SCHEME://HOST[:PORT]`.
  The doc describes it as the canonical URL of the root of the production deploy,
  composed of protocol scheme, hostname or IP, and optionally the port. It
  states the value "should NOT have a trailing slash", and that it "will be
  appended with the baseurl to form the full URL to your Jekyll site when using
  the Liquid filter `absolute_url`". It also notes this setting is automatically
  configured to the localhost URL when `jekyll serve` runs.
- **`baseurl`** — option heading "Base URL". Value form `baseurl: /PATH/TO/SITE`.
  "Serve the website from the given base URL (the path between web-server or
  domain root and your landing page)." The CLI form is `-b, --baseurl /PATH/TO/SITE`.

The composition rule that follows: **the site URL is `url` + `baseurl`**, and
`url` carries no trailing slash because `baseurl` supplies the separating one.
A site served from a subdirectory is therefore not a deployment fact — it is
`baseurl` in the site configuration, and every internal link must go through the
filter for it to come out right.

This is the gap the lane's `scripts/base_path_audit.py` (r29) works against: the
audit checks emitted links, while this row pins the option semantics those links
are supposed to follow.

## What this entry does not establish

- It does not establish the **`github-pages` gem's** version behaviour, the
  dependency set, or any GitHub Pages build detail — those are separate rows in
  the lane registry (S016 and the S040–S043 block) and were not reopened.
- It does not establish what `baseurl` a specific lane property uses. That is a
  per-property read of an owned site and is operator-gated.
- The options reference carries **no publication date**, so the recheck above is
  content-anchored (exact option line) rather than date-anchored.
