# ReopenS043 — wave-2 falsify report (Kake round 29)

Seat: KakeR29.ReopenS043. Axes: freshness (live web vs retained bytes), operability
(row cells, entry lines). Target: row S043 and every entry line citing S043, at lane
commit 7697990cbca20291f3b0367b8ff4220e93b38b03. All lane reads below are committed
bytes at that revision; every write happened in my sandbox
/fast/scratch/hyaku/kake-r29/w2/ReopenS043/ (clone at 7697990, TMPDIR inside sandbox).
No installs were needed; nothing was installed or upgraded.

## Item attacked

C1 freshness at S043: the claim that corpus/knowledge/pages-base-path.md and row S043
in corpus/SOURCES.md are grounded in the live page https://vite.dev/guide/static-deploy.html
(retained text sha256 d665dd23…, receipt in .ufo/waves/round-29/sources/receipts.json).

## Commands and observed output

1. Clone at pinned revision — exit 0.
   `git clone -q <lane> <sandbox>/clone && git -C <sandbox>/clone checkout -q 7697990…`
   → HEAD = 7697990cbca20291f3b0367b8ff4220e93b38b03.
2. Single live GET — exit 0.
   `curl -sSL -o vite-static-deploy.html -w "…"` → HTTP 200, final url
   https://vite.dev/guide/static-deploy.html (no redirect), 93983 bytes, one GET total.
3. Body identity — live sha256(vite-static-deploy.html) = be274bde3c2b6b09…302b4b80
   = receipts.json S043 bodySha256; 93983 bytes = receipt bodyBytes. Today's page is
   byte-identical to the L1's 2026-10-22T10:29:37Z fetch.
4. Retained text equality — reproduced the documented rule ("HTML minus script/style,
   comments and tags removed, entities decoded, whitespace collapsed"; implemented as:
   script/style skipped, comments skipped, every tag replaced by one space, character
   references decoded, whitespace runs collapsed, stripped, plus one trailing newline)
   over the live body: sha256(derived) = d665dd23b193b0a4…535b52dcba
   = receipt textSha256 = sha256(.ufo/waves/round-29/sources/S043.txt), and derived
   bytes == retained bytes exactly. Word count 2164 = receipt textWords 2164.
   The odd spacing inside corpus quotes ("vite.config.js .", "workflow ,") is a real
   artifact of tag→space removal, and the live page reproduces it verbatim.
5. Official counter — exit 0.
   `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision 7697990…`
   → "C1 4/4 at 7697990cbca20291f3b0367b8ff4220e93b38b03", controlBroken: false
   (flipped-letter control not found in retained text).
6. Internal consistency — sha256 of S040.txt/S041.txt/S042.txt/S043.txt each equal
   their receipt textSha256 (S040 625f2b07…, S041 86a77ee2…, S042 b66fefc1…,
   S043 d665dd23…).

## Row S043 cells (corpus/SOURCES.md:51), cell by cell

- cell[0] `S043` — id. OK.
- cell[1] URL https://vite.dev/guide/static-deploy.html — equals receipt url and
  finalUrl, and my live final url. OK.
- cell[2] `docs` — kind classification, not live-falsifiable. Noted, not checked.
- cell[3] `A` — tier classification. Noted, not checked.
- cell[4] summary ("build-time base value… bundler configuration rule") — consistent
  with the page. OK.
- cell[5] "GitHub Pages section, the Update Vite Config step; Vite v8.3.4 docs,
  fetched 2026-10-22" — heading "GitHub Pages" and step "Update Vite Config" both in
  live text; "v8.3.4" present (navbar version span, survives tag removal, in retained
  text); fetched date = receipt accessedUtc 2026-10-22T10:29:37Z, status 200. OK.
- cell[6] "project site needs base /<REPO>/, user site or custom domain base /, also
  the default when base is omitted" — all three statements verbatim in live text
  (quotes below). OK.
- cell[7] `mined`, cell[8] `2026-10-22` — match receipts. OK.
- cell[9] `90d` — refresh policy, not live-falsifiable. Noted, not checked.
- cell[10] pointers corpus/knowledge/pages-base-path.md, corpus/lessons/round-29.md —
  both exist at 7697990. OK.

## Every entry line citing S043 — per-line verdicts

corpus/knowledge/pages-base-path.md (all at 7697990):

- L1 (source list) — S043 URL listed matches receipt/live. HOLDS.
- L2 (verified-at, "text sha256 … S043 d665dd23…") — matches S043.txt sha and receipt;
  "one public GET each, HTTP 200" matches receipts (all four accessedUtc
  2026-10-22T10:29:37Z, status 200). HOLDS.
- L15 (section header "Vite (S043)") — label only. HOLDS.
- L27 (negative claim "None of S040–S043 discusses the base element") — "base element"
  and "<base" absent from all four retained texts; S041's only " href=" hit is the
  Jekyll Liquid example `<link href="…relative_url…">`, not a base-element discussion.
  HOLDS.
- L39 — quote "Set the correct base in vite.config.js ." in retained AND live. HOLDS.
- L40 — quote "If you are deploying to https://<USERNAME>.github.io/<REPO>/ (eg. your
  repository is at https://github.com/<USERNAME>/<REPO> ), then set base to
  '/<REPO>/' ." in retained AND live. HOLDS.
- L41 — two quotes: "If you are deploying to https://<USERNAME>.github.io/ , or to a
  custom domain through GitHub Pages (eg. www.example.com ), set base to '/' ." and
  "Alternatively, you can remove base from the configuration, as it defaults to '/' ."
  — both in retained AND live. HOLDS.
- L42 — quote "GitHub will now deploy your site using a GitHub Actions workflow ,
  which is necessary since Vite requires a build step for deployment." in retained AND
  live. HOLDS.
- L48 — S043 part (`base` of `'/'` for a custom domain) supported by L41 quote in live
  text; its S041 quote "(unless a custom domain is specified)" is in S041.txt; its S040
  characterization holds: S040's body says only "You can host your site on GitHub's
  github.io domain or your own custom domain. See Configuring a custom domain…", with
  no statement of where a custom-domain project site is served. HOLDS.

corpus/lessons/round-29.md:

- L39 (Gate row) — quote "If you are deploying to … then set base to '/<REPO>/' ." in
  retained AND live; section labels "GitHub Pages", "Update Vite Config" present. HOLDS.
- L10, L60, L122 — group mentions; L60's "tier A, status mined, opened 2026-10-22"
  matches row cells[3]/[7]/[8]. HOLDS.

Semantic checks against live text (all PASS): project-site base '/<REPO>/'; user-site
base '/'; default '/' when base is removed; Actions-workflow deploy sentence; "Set the
correct base in vite.config.js"; nav version v8.3.4.

## Verdict

HOLDS. The falsification attempt found no freshness or operability defect in the S043
chain: live body byte-identical to the retained receipt body, retained text reproduced
byte-exactly from today's live page by the documented rule, every quoted S043 line
verbatim in both retained and live text, row cells accurate, counter 4/4 with control
intact. C1 as declared at S043 survives reattack with one fresh GET.

## Residual risk and what I did not verify

- Freshness is proven for today (2026-10-22, hours after the L1's 10:29:37Z GET);
  content could have differed between the two GETs.
- S040–S042 retained texts verified against receipts only (hash equality), not
  re-fetched live — those URLs were not in my grant.
- Row cells "docs" (kind), "A" (tier), "90d" (TTL) are classification/policy and were
  not checked against anything external.
- The original extractor implementation was not read; I pinned the rule by output
  equivalence (byte-exact reproduction from the same body), not by source identity.
- The C1 counter's checks run against retained text only; my live-text checks above
  close that gap for S043.
