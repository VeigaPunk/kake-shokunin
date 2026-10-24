# RowS003 — GitHub Docs: Configuring a publishing source (freshness re-check, round 26)

```json
{"id":"S003","verdict":"HOLD","fetchIndex":1,"quote":"You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.","anchorObserved":"'About publishing sources' section, first paragraph (directly after the 'In this article' nav); matching CNAME note retained at the end of 'Creating a custom GitHub Actions workflow to publish your site'","reason":"The living page (no commit/tag pin) returned 200 today with both row anchors intact: the 'About publishing sources' paragraph still names branch publishing and GitHub Actions workflow publishing, the branch/folder source-selection steps remain, and the custom-workflow note still reads 'A CNAME file in your repository file does not automatically add or remove a custom domain.' Scope and teaches hold; both citing claims (ghp-custom-domain.md:22 CNAME note, ghp-served-set.md:28 source folder) are still supported.","correction":null}
```

Caveats (≤10 lines):
1. Living docs URL, no version/date pin: freshness is judged on content/anchor presence; no prior S003 byte copy exists under `.ufo/waves/round-25` or `round-26`, so a byte-level drift comparison against the 2026-10-19 fetch was not possible.
2. Fetch #1: status 200, 154,136 HTML bytes, sha256 `aa758b4a543f792f3afa1ea37edf4042581719510a479a3f45ce3ace58fdf1ac`, fetchedAt `2026-10-21T15:09:34Z`.
3. The note's section position matches the row wording: it sits at the end of the "Creating a custom GitHub Actions workflow to publish your site" section, followed by "Troubleshooting publishing with a custom GitHub Actions workflow".
4. Incidental quote-fidelity note for knowledge seats (no row action): `ghp-served-set.md:28` quotes "the source folder can either be the root of the repository (`/`) or a `/docs` folder", while today's page interpolates "on the source branch" before both alternatives; semantics are identical.
5. Tooling: none installed or upgraded.
