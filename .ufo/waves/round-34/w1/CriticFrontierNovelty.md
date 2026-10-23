# CriticFrontierNovelty — round 34, wave 1 (critic, freshness)

Target: is link-preview metadata a genuinely new frontier area for kake, and is C2 a learning and
freshness move rather than citing-set work or a supplement written after a finding?
All reads are `git show`/`git grep` at landed `a2fe31b2` (base `1e54c895`), with read-only git only.
Verdict in brief: the area is new as *held* knowledge, and C2 is neither citing-set work nor a
post-finding supplement. There are two fixable gaps (findings 2 and 6) and two tradeoffs the
closure should weigh (findings 7 and 8).

## Findings

1. **New as held knowledge, though not untouched.** `git grep -i` for Open Graph, `og:`,
   link preview, preview card, `twitter:card`, oEmbed and unfurl over `corpus PROVINCE.md SKILL.md`
   at `a2fe31b2` finds no knowledge entry, no SOURCES row (no ogp.me, Facebook, Slack or Mastodon
   URL anywhere in `corpus/`) and no SKILL.md or PROVINCE.md hit. The only corpus hits are
   incidental drift and publish facts about Plazir pages: `corpus/knowledge/drift-detection.md:80,109`,
   `publish-queue.md:38,181,270` and `lessons/round-16.md:58`.
   Strongest counterexample: a round-33 seat already checked canonical == `og:url` on the three
   frostbite pages (`.ufo/waves/round-33/w1/ScoutUpstreamCommitAnatomy.md:25,65`). That check stayed
   in wave evidence and was never admitted (`sitemap-orphan-audit.md` has no `og:` hit). Live
   snapshots in rounds 22, 23 and 29 also hold `og:` and `twitter:card` tags, but only as data.
   So SCORECARD.md "Round 34 — declared claims" ("a frontier area the lane has never held") holds
   for "held". It would be false if it were reworded as "never touched", and the 102-page
   `og-url-equals-canonical` count partly re-measures a round-33 observation.
2. **Not on either frontier list.** PROVINCE.md:20-30 `## Frontier` (crawl hygiene, CWV,
   base path, WCAG, Render) and corpus/README.md:90-108 `## Frontier` do not name link previews.
   The area does fit the domain (PROVINCE.md:3) and Core (PROVINCE.md:12-13, source-grounded audits
   of the lane's web properties) as publisher-side head metadata. But nothing in the round forces a
   PROVINCE record: C2 counter conditions a–e (`c2_source_census.py` docstring) never read PROVINCE.
   Smallest correction: append `## Round-34 frontier step` to PROVINCE.md naming link-preview
   metadata, its entry and its gate. Rounds 29, 30, 31 and 33 did this (PROVINCE.md:84, 94, 111, 133).
   Without it, the goal-file learning-claim test ("changes what the lane knows … in its PROVINCE core
   or frontier", goal file :145-148) has to be inferred.
3. **Adjacency edge.** S069 (the Slackbot robots page) and S070 (the Mastodon PreviewCard entity)
   describe consumer and crawler behaviour. PROVINCE.md:34-35 gives tabi "client-side crawler
   discipline" and gives kake "publisher-side placement". The entry should frame S069 and S070 facts
   as what a publisher must place (which tags, and where in the document). Restating crawler
   internals would absorb tabi's ground (adjacency axis).
4. **Not citing-set work.** SCORECARD round-34 declaration: "Neither claim touches the citing-set
   gate". `git diff-tree` of `d08d8de` and `a2fe31b` lists no `scripts/citing_set*` path. The
   only `scripts/` path the round names is the new `scripts/link_preview_audit.py`.
5. **Not a supplement written after a finding.** The C2 counter landed in the declaring commit
   `d08d8de` (2026-10-22T18:00:16-03:00), together with the SCORECARD declaration. Before-receipts
   followed in `a2fe31b` (18:01:53-03:00). The counter hard-codes no census number: grepping it for
   `87` or `102` exits 1. Pre-declaration screening (`git grep` opening counts) is disclosed in the
   declaration. This is the same shape the round-33 closure accepted, where the counter hard-coded
   no count (`corpus/lessons/round-33-verifier-spotcheck.md:111-116`). That closure's ruling frame
   for supplements (:36-42) does not apply here. C2 is also not a routed repair: the round-33
   routed-defects list (:185-205) has no Open Graph item.
6. **The drift sentinel tripped, but the round does not say so.** Goal file :173 reads: "Same
   axis+surface claim … 3 rounds running → next round must work a different frontier area". The
   operability claim worked the citing-set gate in round 31 (SCORECARD.md:819-830), round 32
   (:1009-1020) and round 33 (:1091-1100), so the sentinel binds round 34. Round 34 complies.
   Round 29 named the sentinel as its reason (`corpus/lessons/round-29.md:124-132`,
   `LOG.md:1246`); round 34's declaration does not. Smallest correction: one sentence in
   `corpus/lessons/round-34.md` and the LOG entry citing goal file :173. The round prompt
   `.ufo/prompts/kake-round-34.md` has no operator drift note: `grep -n -i drift` printed nothing.
7. **Tradeoff: the freshness surface repeats into round 35.** Every freshness claim from round 31
   to round 34 reads ds4cc-marketplace source bytes:
   - round 31: `render.yaml` at `1fbdb8ed` (`render-web-services.md:4-5,50`)
   - round 32: the retained `1fbdb8ed` blobs
   - round 33: the `7fc6aa2f` pin
   - round 34: the `7fc6aa2f` HTML census

   The topics differ, but if the closure reads "surface" as the repository, the sentinel trips at
   the round-34 closure and round 35 must take a different area. This is not a round-34 defect;
   the L1 should know it for round-35 planning.
8. **Tradeoff: the fit of a learning claim to the freshness axis.** AXES.md:14 defines freshness as
   "skill claims re-verified against live surfaces". C2 is offline new knowledge, which reads closer
   to expansion and coverage, and SCORECARD.md:3-4 assigns coverage to other lanes. Precedent
   admitted the same shape as freshness:
   - `round-29-verifier-spotcheck.md:69`
   - `round-30-verifier-spotcheck.md:93`
   - `round-31-verifier-spotcheck.md:76`

   C2 also has a real freshness element. The sources were opened at 20:57Z this round, and upstream
   is still at the census commit: `git ls-remote https://github.com/VeigaPunk/ds4cc-marketplace.git`
   at 2026-10-22T21:07:47Z returned `7fc6aa2f…` for both HEAD and `refs/heads/main`. This is
   consistent with precedent and is no reason to reject.
9. **Two canonical rules in the lane (latent).** The tools disagree on how to resolve a relative
   canonical:
   - `scripts/canonical_audit.py:98-99` resolves it through "The first head base[href]".
   - The C1 matrix `og_url_not_canonical` resolves it "against the page URL".
   - The C2 counter resolves it against `https://ds4cc.com/<path>`.

   Strongest local counterexample: `omegag/index.html:4` `<base href="/omegag/">`. Its canonical
   (:19) is absolute, so the current census is unaffected; it is the only `<base` in the 102 pages.
   A relative canonical under a `<base>` would give the two lane tools different canonicals.
   Smallest correction: state in the tool and entry that `<base>` is ignored and that this differs
   from `canonical_audit.py`, or adopt its rule.

## Commands (cwd: the lane, read-only; every exit 0 unless stated)

- `git grep -n -i -E 'open graph|opengraph|og:|link[- ]preview|preview card|previewcard|twitter:card|oembed|unfurl' a2fe31b2 -- corpus PROVINCE.md SKILL.md SOURCES.md`; the same over base `1e54c895`, all paths except `.ufo/waves/round-34`
- `git show a2fe31b2:PROVINCE.md` and `:corpus/README.md` (Frontier sections); `git show a2fe31b2:SCORECARD.md` (rounds 31–34)
- `git log`/`git diff-tree` over `1e54c895..a2fe31b2`; `git show d08d8de:.ufo/waves/round-34/c2_source_census.py | grep -n -E '\b(87|102)\b'` → exit 1 (no match)
- `git grep` for the sentinel wording; `git show` of the round-29 lesson, the round-33 spot-check and LOG.md
- `grep -n -i drift .ufo/prompts/kake-round-34.md` printed nothing; read goal file :95-247
- `git ls-remote https://github.com/VeigaPunk/ds4cc-marketplace.git HEAD refs/heads/main` (public GitHub, GET)
- `git show a2fe31b2:.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz | xz -dc | tar -xOf - | grep -c -i '<base[ >]'` → 1 (archive sha256 `818f0644…d2fe7a3`); per-file `tar --to-command` grep, which wrote nothing to disk

## Not verified

I did not read S067–S070 retained text or check any quote, and I did not run either counter. I
did not read `link-preview-metadata.md` or `link_preview_audit.py`, which have not landed. I read
goal file lines 1-94 only through grep. No sandbox was needed and no tools were installed. No
operator-owned property was contacted.

<!-- 2026-10-23 round-43 movement census: corpus/lessons/round-29.md gained one annotation row (line 104) after its round-29 FieldsAndCounts row; this file's pointer "corpus/lessons/round-29.md:124-132" now reads "125-133". Cited content unchanged; the new row itself carries absence wording. -->
