# Scout — further link-preview source leads (Kake R34, wave 1)

Seat: KakeR34.ScoutMoreSourceLeads. Question: screen further link-preview sources for the Gate.
All opens were plain GET via `curl -sS -L` with a stock desktop UA (ordinary means only); no
headless browser, no login, no challenge was passed. Sandbox:
`/fast/scratch/hyaku/kake-r34/w1/ScoutMoreSourceLeads/` (bodies in `raw/`, visible text in `text/`,
extraction rule identical to the lane fetcher: script/style, comments and tags stripped,
entities decoded, whitespace collapsed). Fetched 2026-10-22 ~18:05–18:08Z.

## Candidate table

| # | URL | HTTP | Final URL | Ordinary? | Tier | 6–25-word quote | Decision + reason |
|---|-----|------|-----------|-----------|------|-----------------|-------------------|
| L1 | https://docs.discord.com/developers/link-previews/overview (entered via discord.com/developers/docs/resources/message → "Link Previews Overview" nav) | 200 | same | yes | **A** (primary vendor spec) | "The tags must be in the HTML your server sends. No code is executed, so tags added by a client-side script after load are never seen." | **ADMIT.** Consumer-side table maps og:title/description/image/site_name/image:* /video/type onto embed fields, and states hard fetch requirements (2xx, text/html, ≤5 redirects). Directly supports the audit premise that a static-HTML manifest is the right unit. Note: page never mentions og:url or canonical (gap, not a contradiction). Body sha256 11b73956247ef3163f985cd2bbf932732eb51554e92056f0ec58f68c8a032494 (1747 words). |
| L2 | https://oembed.com/ | 200 | https://oembed.com/ | yes | **C** (background) | "oEmbed is a format for allowing an embedded representation of a URL on third party sites." | **QUEUE (C), not admit as required-property evidence.** Different discovery mechanism (`<link type="application/json+oembed">`), zero occurrences of "og:" in 2030 words. Only useful if the doc needs the "preview mechanisms besides Open Graph" paragraph; L1 shows consumers also read oEmbed responses ("oEmbed is the only way to put an author on a preview"), so oEmbed is adjacent, not substitutable. Body sha256 a30e0890c1e48c6e7ff18ed585c1fd0d3583158c62b0567414fe1cefc389e33d. |
| L3 | https://core.telegram.org/bots/api#linkpreviewoptions | 200 | https://core.telegram.org/bots/api | yes | **C** (API surface only) | "Options used for link preview generation for the message, if it is a text message and link preview options were changed." | **REJECT as tag evidence.** LinkPreviewOptions documents only `is_disabled`/`url`/`prefer_*`; the page has **zero** "og:" occurrences in 73,876 words and never states which tags Telegram reads. Adds nothing to the S067–S070 tag contract. Body sha256 d70a187f82feaa1acfad9eda179feb163716b7ce42a0667f4886ab3b6695de00. |
| L4 | https://github.com/jekyll/jekyll-seo-tag (README/docs) | 200 | same | yes | **B** (generator docs) | "Open Graph title, description, site title, and URL (for Facebook, LinkedIn, etc.)" (repo README, "What it does" list) | **QUEUE (B), admit only if the doc discusses tag emitters.** Answers the asked question narrowly: the plugin emits og: tags, but `docs/installation.md` requires explicit Gemfile + `_config.yml` `plugins:` + `{% seo %}` — I observed **no** statement that GitHub Pages enables it automatically. `https://pages.github.com/versions/` (200) lists `jekyll-seo-tag` in the Pages dependency set, which shows availability, not opt-in. Retained ds4cc tree (`tree.txt`) has no `_config.yml`/Jekyll files among 102 .html paths, so this lead does not explain the audited corpus. install.md sha256 30bce08e44847f808c4cf2f533c1c3f7ab0fd314561dba662291453b93e73615; pages-versions sha256 daacecc6297ca3f837d547b17a00e28f6b196e312608214dcca7e02b3e53cfd1. |
| L5 | https://www.linkedin.com/post-inspector/ | 200 | https://www.linkedin.com/post-inspector/ | page returns, content does not | **— (rejected)** | "Post Inspector" (entire visible text, 2 words) | **REJECT.** JavaScript-only shell (3,577-byte body); the share-preview contract is not obtainable by ordinary means. Not opened further; no browser used. Body sha256 2426c99b010014c540771157261837bb38cd3d2189f19b4f021b22bc53e4f790. |
| L6 | https://www.linkedin.com/help/linkedin/answer/a528619/sharing-links-in-posts-on-linkedin (and bare a528619) | 404 / 404 | same | yes | **— (rejected)** | "404: Page Not Found \| LinkedIn Help Attention screen reader users, you are in a mobile optimized view…" | **REJECT.** Both variants 404 (19,824 / 19,680-byte error pages). No LinkedIn help article on shared-link previews was located within the time box; the help site's search is JS-driven, so it was not pursued. Body sha256 4a6f26786137127de2506edde343eebe2bf24643f292d93a7536146e148c17f7. |
| L7 | https://discord.com/developers/docs/resources/message and …/resources/channel | 200 | https://docs.discord.com/developers/resources/{message,channel} | yes | **— (folded into L1)** | "Link Previews Overview Component Embeds … link preview built from Discord components" | **REJECT as standalone.** These resource pages only cross-link the L1 overview; sha256 0fd5983e6d0e3959304597cf6936282bbce8b44249eba96c7074cb269a4043e8 / bd66e64bbb78dd3dd2bc5866d173b4aeb6eac8840570dc24db381983f1d559b2. |
| L8 | https://developer.x.com/…/cards/overview/markup, https://docs.github.com/…/social-media-preview | 200 | x.com → docs.x.com/overview ; github docs page | yes | **— (already rejected, confirmed)** | (retained S071/S072) | **REJECT, consistent with the declared S071/S072 rejection candidates.** S071's final URL is a generic docs.x.com overview (396 words, no cards markup); S072 is a repository-settings page, not a consumer tag spec. No new IDs proposed for them. |
| L9 | https://raw.githubusercontent.com/jekyll/jekyll-seo-tag/{master,main}/README.md | 404 / 404 | same | yes | **— (fetch path failed)** | "404: Not Found" (14 bytes, sha256 d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed) | **Recorded as unopened by that path.** Default branch is `master` (repo blob links); `docs/installation.md` raw on `master` is 200, so the README filename/raw path is what failed, not the branch. README text was read from the rendered repo page instead (L4). |

Related check: `https://api.github.com/repos/jekyll/jekyll-seo-tag` returned **403** (unauthenticated
rate limit, 280-byte body) — recorded, not retried.

## Recommendation to the Gate (advisory)

- Admit **L1 (Discord link-previews overview)** as a new source ID: it is the only candidate here
  with a tag→field contract and an explicit server-sent-HTML rule. It complements S067–S070 (OG
  vocabulary, Facebook sharing, Slack robot policy, Mastodon entity) without duplicating them.
- Queue **L4** as B supporting material for an "emitters" sentence, and **L2** as C for the
  non-OG mechanism sentence; neither should be cited for required properties.
- Reject L3, L5, L6, L7, L8, L9 with the reasons above.

## Coverage and unverified

- Verified: HTTP status + final URL + body hash for every row above (commands below).
- Not verified: no LinkedIn help article on previews was read (404 on the two URLs tried; site
  search not pursued); no claim is made about what tags LinkedIn reads. Discord's page was not
  checked for update date/version. No check made of whether S067/S068 say og:url must equal
  `<link rel="canonical">` (out of scope for this ticket).
- Tools installed/updated: none. Used only `curl` (system) and `python3 -B` (system 3.14).

## Commands run (all exit 0 unless noted)

```
mkdir -p /fast/scratch/hyaku/kake-r34/w1/ScoutMoreSourceLeads/{tmp,raw,text}
curl -sS -L -o /dev/null -w 'status=%{http_code} final=%{url_effective} bytes=%{size_download}\n' \
  https://oembed.com/ https://core.telegram.org/bots/api https://github.com/jekyll/jekyll-seo-tag \
  https://www.linkedin.com/post-inspector/ https://www.linkedin.com/help/linkedin/answer/a528619/sharing-links-in-posts-on-linkedin
curl -sS -L -A '<stock Chrome UA>' -o raw/<name>.html <each URL>          # bodies retained
python3 -B extract.py                                                    # visible text, lane rule
grep -o -i -E '.{0,120}(open graph|og:|link preview|canonical).{0,180}' text/<name>.txt
sha256sum raw/*.html raw/*.md                                            # hashes in table
curl -sS -L -o raw/pages-versions.html https://pages.github.com/versions/ # 200, 11,821 bytes
```
Exit codes: `python3 -B raw/…json | python3 -c json.load` failed once (GitHub API 403 body, not
JSON) — that is the API rate-limit row above, no other non-zero exit.
