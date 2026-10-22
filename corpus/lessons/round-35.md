# Round 35 — sealed targets: link-preview audit repair and a security.txt publishing entry

## Claims

Declared before any build in `SCORECARD.md` section "Round 35 — declared claims" (commit
`81d9fd74f1460ba8cff007fc42f8fb8265aa2d4d`). Base `16a6b8b8144f4d6e6187e9ecbb4fb5f4528b911a`.
Round 34 was rejected because a do-nothing control met each declared counter (closure routed
defect 1). This round seals its test inputs instead. The L1 wrote the C1 cases and the C2 probes
before the declaration, kept them outside the lane until the reveal commit `4c6be2bd`, and
pinned them by sha256 in `.ufo/waves/round-35/sealed_count.py`. The counter refuses any revision
that already holds a key. Every control was scored and committed before the build (`318561ef`).
The C2 conditions were then revised once (version 2, `bd14096a`), still before any build was
measured.

- C1 (operability, capability repair): `scripts/link_preview_audit.py` meets the public
  round-35 contract (a) `og_url_multiple`, (b) metadata inside template/svg/math ignored and
  (c) an unreadable page no longer stops the other pages. Counter: 24 sealed cases. Before: 14
  of 24 at `16a6b8b8` and `bd14096a`. After: 24 of 24 at `b1cbbc39` (target ≥ 22).
- C2 (freshness, sourced learning claim on new ground): `corpus/knowledge/security-txt-publishing.md`,
  how a publisher serves a valid security.txt from GitHub Pages. The entry was drafted by wave-1
  `ScribeEntryDraft` and landed unedited. Counter version 2: met false at base, met true at
  `95abec21`, with 12 of 12 probes, 1388 words, copiedShare 0.0 and 8 good cites (S078–S080,
  S082–S086).

Disclosed: the probe topics (not the probe text) were public in the declaration, and the L1 also
named them in the drafter's item. The drafter never saw the regexes. Its report discloses one
`test -e` on a path under the sealed directory (existence only, exit 1); nothing under it was
read.

## Gate

### Source openings

Opened with `.ufo/waves/round-35/fetch_sources.py` (one public GET each; receipts and retained
text in `.ufo/waves/round-35/sources/`). S078–S085 and the S006 re-open were opened at
22:00:48Z–22:02:20Z, before the declaration. S086–S087 were opened at 22:27:54Z–22:27:55Z, after
wave-1 `ScoutPagesDotfilesSource` named them. A first screen of
`https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages` (it
redirects to what-is-github-pages, a page whose URL another row already covers, with no
`.nojekyll` text) was discarded before any row was written. Quotes are verified as exact
substrings by wave-1 `ScribeGateLines` (`w1/ScribeGateLines.md`; the S086 and S087 quotes by
the L1).

- S078 — https://www.rfc-editor.org/rfc/rfc9116.txt — accessed 2026-10-22T22:00:48Z, HTTP 200 — admit, tier A, kind spec, status mined: the RFC fixes the file's mandatory location and its field rules, so a publisher can conform rather than guess; quote “For web-based services, organizations MUST place the "security.txt" file under the "/.well-known/" path” (Section 3, Location of the security.txt File, first paragraph; 13 words).
- S079 — https://securitytxt.org/ — accessed 2026-10-22T22:00:48Z, HTTP 200 — admit, tier A (the RFC authors' own project site; the Gate draft said B, and the row draft's A is kept because the page is primary for its own guidance, as with S077 in round 34), kind docs, status mined: the project's landing page gives the one-step publishing instruction and names real adopters; quote “Create a text file called security.txt under the .well-known directory of your project.” (Step 1 block under the adopter list; 13 words).
- S080 — https://jekyllrb.com/docs/configuration/options/ — accessed 2026-10-22T22:00:49Z, HTTP 200 — admit, tier A, kind docs, status mined: Jekyll's options page documents the include setting that overrides the default dotfile exclusion, the mechanism a Pages publisher needs; quote “.htaccess is a good example since dotfiles are excluded by default.” (Global Configuration table, Include row; 11 words).
- S081 — https://en.wikipedia.org/wiki/Security.txt — accessed 2026-10-22T22:02:20Z, HTTP 200 — reject, tier C, kind community, status rejected: a tertiary encyclopedia summary whose whole File format section is two sentences and omits the Expires rule, the field grammar and any Jekyll or Pages publishing step, so it grounds no publisher procedure; quote “security.txt files can be served under the /.well-known/ directory (i.e. /.well-known/security.txt ) or the top-level directory (i.e. /security.txt ) of a website.” (File format section, first sentence; 22 words).
- S082 — https://www.rfc-editor.org/rfc/rfc8615.txt — accessed 2026-10-22T22:00:49Z, HTTP 200 — admit, tier A, kind spec, status mined: the RFC reserves the /.well-known/ path prefix and requires registering a suffix there, which is why the location is fixed and not chosen; quote “A well-known URI is a URI [RFC3986] whose path component begins with the characters "/.well-known/"” (Section 3, Well-Known URIs, first paragraph; 15 words).
- S083 — https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml — accessed 2026-10-22T22:00:50Z, HTTP 200 — admit, tier A, kind dataset, status mined: the IANA registry lists security.txt as a permanent IETF registration under RFC 9116, confirming the suffix is assigned and not local custom; quote “security.txt RFC 9116 permanent IETF 2021-07-13” (Well-Known URIs table, security.txt row; 6 words).
- S084 — https://github.com/.well-known/security.txt — accessed 2026-10-22T22:02:20Z, HTTP 200 — admit, tier A, kind dataset, status mined: GitHub's served file carries Canonical and a near-future Expires, one working example of the field layout; quote “Acknowledgments: https://hackerone.com/github/hacktivity Preferred-Languages: en Canonical: https://github.com/.well-known/security.txt Policy: https://bounty.github.com” (whole served body, field lines; 8 words).
- S085 — https://www.google.com/.well-known/security.txt — accessed 2026-10-22T22:02:20Z, HTTP 200 — admit, tier A, kind dataset, status mined: Google's served file shows two Contact lines, an Encryption URI and a long Expires, a second working example of the same layout; quote “Contact: https://g.co/vulnz Contact: mailto:security@google.com Encryption: https://services.google.com/corporate/publickey.txt” (whole served body, first three field lines; 6 words).
- S086 — https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site — accessed 2026-10-22T22:27:54Z, HTTP 200 — admit, tier A, kind docs, status mined: GitHub's current page for the branch-publishing switch that turns the Jekyll build off; quote “disable the Jekyll build process by creating an empty file called .nojekyll in the root of your publishing source” (Creating your site, static-site-generator note; 19 words).
- S087 — https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/bypassing-jekyll-with-nojekyll — accessed 2026-10-22T22:27:55Z, HTTP 404 — reject, tier C, kind docs, status rejected: the former dedicated .nojekyll page is gone with no redirect, so it teaches nothing and S086 carries the rule; quote “404 - GitHub Docs GitHub Docs Page not found. Return to home.” (whole served body; 11 words).
- S006 — https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll — accessed 2026-10-22T22:02:19Z, HTTP 200 — re-open of the existing row (status unchanged), tier A, kind docs, status mined: the re-opened page still states Jekyll's default exclusion of dot paths and the include override on a Pages site; quote “If you want Jekyll to process any of these files, you can use the include setting in your configuration file.” (Configuring Jekyll in your GitHub Pages site, sentence after the exclusion list; 20 words).

Real rejects with reasons: S081 (a secondary restatement that grounds no publisher step) and
S087 (a 404 page). Wave-1 `ScoutSecurityTxtCandidates` screened six more candidates and gave
none a row. It proposed rejecting the CISA BOD 20-01 template: “Your policy must be published as
a public web page in plain text or HTML at the “/vulnerability-disclosure-policy” path”. That
template names neither security.txt nor `.well-known` (`w1/ScoutSecurityTxtCandidates.md`).

Row changes logged old→new:
- S078, S079, S080, S082, S083, S084, S085, S086: `—` → `mined`, opened `2026-10-22`, recheck
  `90d`, used-by `corpus/knowledge/security-txt-publishing.md`.
- S081, S087: `—` → `rejected`, opened `2026-10-22`, recheck `90d`, used-by `—`.
- S006 used-by: `corpus/knowledge/ghp-served-set.md, corpus/knowledge/publish-channels.md,
  corpus/knowledge/sitemap-orphan-audit.md, corpus/knowledge/static-canonical-preflight.md,
  corpus/lessons/round-27.md` → the same plus `corpus/knowledge/security-txt-publishing.md`.
  Status and recheck are unchanged. The page was re-opened and its taught fact still holds.
- S074: no cell changed. A "Round-35 correction note for S074" is appended to `SOURCES.md`
  (routed defect 5): “no og: occurrence” is true of the extracted text only, because the page
  head carries 3 `og:` metas about the page itself. The reject stands.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| a declared counting target was published by the round's own pre-build receipt, so a copy of that receipt met the target | `.ufo/waves/round-34/verification/c2-at-d08d8de.json` (added at `a2fe31b`, before the entry at `9ef758c`) carries `census.derived` with all seven census values; the retained hollow control copied them (`corpus/lessons/round-34.md:68`) | routed defect 4 of `corpus/lessons/round-34-verifier-spotcheck.md`; no round-34 criterion | `.ufo/waves/round-35/criteria/prebuild_leak_check.py`: exit 1 on that receipt against the landed census line (`verification/criterion-prebuild-leak-r34-c2-at-a2fe31b.txt`), exit 0 on the C1 receipt (`criterion-prebuild-leak-r34-c1-at-a2fe31b.txt`). This round's design publishes no target value: the keys stayed sealed until `4c6be2bd`. QUALITY round-35 (b). |
| a retained control was explained by the counter's scratch layout instead of by its own bytes | `corpus/lessons/round-34.md:68` and `SCORECARD.md` "Limits found by wave 1" say `dcef39b5` "keys on the case directory name"; its bytes hash argv plus every relative path and file content under the cwd (correction below) | routed defect 2; no round-34 check re-read the retained bundle | `.ufo/waves/round-35/criteria/control_description_check.py`: exit 1 on round-34 mistake row 4 (`verification/criterion-control-description-r34-row4.txt`); the correction paragraph below is the passing case (`criterion-control-description-r35-correction.txt`). QUALITY round-35 (c). |
| a lane tool with a four-code exit contract and a selftest shipped with no `SKILL.md` gate registry row | `git grep -n 'link-preview-audit' 318561ef -- SKILL.md` finds nothing; `scripts/link_preview_audit.py` defines exits 0/1/2/64 | routed defect 3; PROTOCOL §Gate standard (Registry) | `.ufo/waves/round-35/criteria/registry_row_check.py`: exit 1 at `318561ef` naming `scripts/link_preview_audit.py` (`verification/criterion-registry-row-at-318561ef.txt`), exit 0 at `fd0d53b2` after the row landed (`criterion-registry-row-at-fd0d53b2.txt`). QUALITY round-35 (d). |
| the frozen C2 counter read raw bytes, not what a reader sees, so hidden bytes could carry a do-nothing control to one probe short of the target | Wave-1 `CriticC2Conditions`: a verbatim RFC transcription padded inside an HTML comment scored copiedShare 0.0376, and a zero-width-split copy with hidden rows scored 0.0043, each passing size, copied and cites under version 1 (`verification/control-c2-critic-dilute-comment.json`: 8 probes, `control-c2-critic-zwsp-hiddenrows.json`: 6) | prompt §6.9, which asks for the cheapest control that skips the work: the L1's four C2 controls did not include hidden-byte shapes | Counter version 2 (`bd14096a`) cleans comments and format characters, counts size in the overlap words, and reads only the first Registry section. The same two bundles now fail `copied` and `cites` (`verification/control-v2-c2-critic-*.json`: copiedShare 0.9781, cites 0). Committed before any build was measured. |

Sweep for other mistakes: wave-1 `ScribeMistakeMine` (`w1/ScribeMistakeMine.md`, commands and
output there) also found two round-34 rows. The carried-open ledger miscounted its regressions;
round 34 already corrected that by append, at `corpus/lessons/round-34.md:168-175`. The round-34
Mistakes table mined one of the five defects the closure later routed. Both are recorded there,
not promoted here.

## Round-34 routed defects — disposition

| # | Item | Disposition |
|---|---|---|
| 1 | Declare a target a do-nothing control cannot reach; score retained controls before the build | Sealed keys (`81d9fd74`) and control receipts committed before the build (`318561ef`; version 2 rescore `bd14096a`). On the new counter, `dcef39b5` scores 7 of 24 and `0cce15f0` met false. `criteria/lookup_control_check.py` reads the round-34 counter's `total` field, which the round-35 counter does not emit (wave-1 `ReviewSpotcheckRouting`), so the same check is done by direct receipt: `verification/control-v2-c1-lookup-dcef39b5.json` (exit 1, 7 of 24). |
| 2 | Lookup control misdescribed | Correction appended below and in SCORECARD round 35, with `control_description_check.py` shown able to fail. |
| 3 | No registry row | `SKILL.md` "Link-preview audit gate registry — round 35" (`fd0d53b2`) plus `registry_row_check.py`. |
| 4 | Census target published pre-build | Sealed design, and `prebuild_leak_check.py` shown able to fail. QUALITY round-35 (b). |
| 5 | S074 reason overclaims | Correction note appended to `SOURCES.md`; reject kept. |
| 6 | Carried items | Two are closed by C1: the tool compared only the first og:url (now `og_url_multiple`), and it accepted a canonical link inside `<template>`/`<svg>`. The third tool item is now (c): a non-UTF-8 page no longer stops the manifest. Still carried: C2 counter D1–D4 (that counter is retired, not reused); Git-pin mutants; option tables; NUL-byte runner crash; freshness-pins re-pin; round-31 F1–F3. |

## Correction of round-34 mistake row 4 and its two repeats (appended)

Correction of `dcef39b5` (round-34 mistake row 4, `corpus/lessons/round-34.md:68`, carried-open
`:130`; `.ufo/waves/round-34/criteria/lookup_control_check.py` line 6; SCORECARD round 34
"Limits found by wave 1"): the control reads no case directory name. Read with `git show
dcef39b5:scripts/link_preview_audit.py` from the retained bundle
`.ufo/waves/round-34/retained/r34-c1-lookup-dcef39b5.bundle`. Lines 5–8 walk the current
directory and keep every relative path and file content. Line 10,
`h = hashlib.sha256(json.dumps(argv).encode())`, starts the key from the arguments. Line 12,
`h.update(rel.encode() + b"\0" + files[rel].encode("utf-8", "surrogateescape") + b"\0")`, adds
each path and its content. Line 15, `r = r or T.get(key(argv)) or [0, "clean", []]`, prints the
stored row or a clean default. Renaming the case directories leaves it at 28 of 28. A one-comment
HTML change drops it to 7 of 28 (wave-1 `ScribeControlCorrection`, `w1/ScribeControlCorrection.md`;
the round-34 closure measured the same 7 of 28). The round-35 sealed counter scores it 7 of 24.
So the carried item "the C1 counter leaks the case id through the case directory name" names
the wrong mechanism. A content-keyed table is what passes, and only inputs the control has never
seen defeat it.

## Carried open

- C2 limits (version 2): a mechanical rewording of a source passes `copied`
  (`verification/control-v2-c2-reworded.json`: copiedShare 0.0733, 6 of 12 probes). Junk rows
  that copy a retained URL pass `cites`. The probes test that facts are present, not that every
  sentence is true. The non-author read of entry truth and row truth stays owed.
- C1 contract ambiguity (wave-1 `CriticC1ContractAmbiguity`, 19 inputs, 7 undecided by the
  text). One example: whether `</template>` also closes an svg opened inside it. The landed tool
  closes the matching element and every element nested in it. No sealed case depends on an
  undecided point (see the wave-2 review).
- Rule (b) follows the contract's literal reading, not the HTML parsing algorithm. A `<meta>`
  inside `<svg>` in the head is ignored by the tool, while an HTML5 tree builder would break out
  of the svg and count it (`CriticC1ContractAmbiguity`).
- Hold: wave-1 `CriticSealedDesign` ended in an automatic model switch after a safety filter.
  Its findings are not evidence, its two bundles were not scored, and the item is not retried.
