# ReviewSourcesRows — SOURCES.md rows S067–S077 at 24a1647 (Kake r34, wave 2)

Method: all cell checks ran against my pinned clone
`/fast/scratch/hyaku/kake-r34/w2/ReviewSourcesRows/clone` at 24a16474ee73e20453f3e1be9d2f33573c5196d9,
never the lane tree. Contract = CORPUS.md:64-141 ("SOURCES.md — where a shokunin learns", contract v1).

## Commands and exits (all read-only)
- `git clone -q <lane> … && git checkout -q 24a1647` → exit 0, HEAD `24a16474ee73e20453f3e1be9d2f33573c5196d9`.
- `git -C <lane> rev-parse HEAD` → 24a1647; `status --porcelain` → 7 entries, all untracked
  `.ufo/waves/round-34/{verification,w2*}` wave-2 artifacts; corpus/ clean, so the census below sees landed state.
- `sha256sum clone/.ufo/waves/round-34/sources/S0{67..77}.txt` → exit 0: all 11 text hashes equal
  `receipts.json` `textSha256` byte-for-byte.
- `gunzip -c S0{67..77}.html.gz | sha256sum` → all 11 body hashes equal `receipts.json` `bodySha256`.
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0, `kake ok`;
  one `W04 S033 duplicate url …rfc9110.txt across scopes` — pre-existing row outside S067–S077; warnings never fail.
- `… census …` → exit 0: 77 rows, tier A63/B2/C12, mined56/queued8/rejected13, `FLEET missing 0`.
- `… overdue …` → exit 0: nothing overdue; S067–S077 all `recheck=90d opened=2026-10-22`.

## Per-row checks (11/11 rows, cell by cell)
Verified per row: source URL and stated final URL vs receipts `url`/`finalUrl`; fetch timestamp and
HTTP 200 vs `accessedUtc`/`status`; sha256 prefix+suffix vs `textSha256`; anchor phrases and teaches
claims grepped in retained `S0xx.txt`; lesson Gate row (corpus/lessons/round-34.md:34-44) quote located;
kind/tier enums; rejected-row `REJECTED: …; flip: …` format; used-by existence; NF=13; duplicate ids (0).

| row | url/final | ts | sha | anchor | teaches | status/flip | used-by |
|---|---|---|---|---|---|---|---|
| S067 | ✓ | 20:57:39Z ✓ | ✓ 0174794e…675581 | ✓ four-props sentence=1, canonical URL=1, permanent ID=1 | ✓ | mined | ✓ exists |
| S068 | ✓ redirect disclosed, matches finalUrl | (see O2) | ✓ 2c9a5d3c…5baa72 | ✓ Jun 30 2026=1; og:title/description/image/type present; internal heuristics=1 | ✓ | mined | ✓ |
| S069 | ✓ | 20:57:41Z ✓ | ✓ e39bdc3d…b2c722 | ✓ Slackbot-LinkExpanding=1, "we are looking for oEmbed"=1, as little=1, cache=2 | ✓ | mined | ✓ |
| S070 | ✓ | 20:57:41Z ✓ | ✓ 81f99a9d…1df9539 | ✓ PreviewCard=6, OpenGraph=1, Attributes=4; url/title/description/type/image/provider_name all present | ✓ | mined | ✓ |
| S071 | ✓ final docs.x.com/overview matches | 20:57:41Z ✓ | ✓ 05206565…b2cd31b | ✓ og:=0, meta=0, exactly one `card` — in "$20 for saving a first payment card…" | ✓ REJECTED+flip | rejected | — ✓ |
| S072 | ✓ | 20:57:42Z ✓ | ✓ c248a847…7bd289b | ✓ Adding an image=3, Social preview=2, meta=0, og:=0 | ✓ REJECTED+flip | rejected | — ✓ |
| S073 | ✓ | 21:08:44Z ✓ | ✓ f60ef122…ea5433 | ✓ 5 redirects=1, 10 seconds=1, text/html=1, Tag Reference=2, "No code is executed"=1 | ✓ | mined | ✓ |
| S074 | ✓ | 21:08:44Z ✓ | ✓ 9be76fda…9554 | ✓ 73,876 words=receipts; og:=0; LinkPreviewOptions=7, is_disabled=1, prefer_large_media=1, show_above_text=1 | ✓ REJECTED+flip | rejected | — ✓ |
| S075 | ✓ | 21:09:47Z ✓ | ✓ c50d0369…199e | ✓ retained text is exactly `Post Inspector` (2 words, 15 B); bodyBytes 3577=row's 3,577 | ✓ REJECTED+flip | rejected | — ✓ |
| S076 | ✓ | 21:09:47Z ✓ | ✓ 2b8b1410…85af2 | ✓ "format for allowing an embedded representation"=1, Discovery=3 | ✓ queued (O1) | queued | — ✓ |
| S077 | ✓ | 21:09:47Z ✓ | ✓ d4d2626b…8afe5 | ✓ "Open Graph title, description, site title, and URL"=1, "What it does"=2, og:image=0 (supports the row's negative parenthetical) | ✓ queued (L1,O1) | queued | — ✓ |

Cross-checks that closed specific claims:
- S075's "two LinkedIn help URLs tried by wave-1 ScoutMoreSourceLeads returned 404" traces to
  `.ufo/waves/round-34/w1/ScoutMoreSourceLeads.md` L6 (both 404, body hashes recorded); screen-out logged at
  round-34.md:54-57. Attribution in the cell is accurate.
- used-by `corpus/knowledge/link-preview-metadata.md` exists at 24a1647 (15,933 B); census E11 clean on disk.
- Gate quotes ≤25 words each (rule 1); row changes logged old→new at round-34.md:46-52; id sequence
  S067–S077 contiguous after S066; no `|` in cells (NF=13 for all 11).

## Findings by severity
- L1 (low, S077, tier-vs-contract): scope is "A Jekyll plugin's own README listing the metadata it emits" —
  the project's own statement, i.e. primary for that scope; CORPUS.md:76-78 reserves A for
  "primary or authoritative for that scope (… source code … maintainer statement …)" and B for "strong
  secondary (expert write-up …, survey, textbook)" (CORPUS.md:79-80), which a README is not. Advisory:
  re-tier A or narrow the scope wording. No claim rides on it (queued, not sole support; census W-free).
- O1 (observation, S076/S077): queued rows' teaches end "flip to mined: …". Contract specifies flip wording
  only for rejected rows (CORPUS.md:81-82) and does not forbid it on queued rows; consistent extension, noted only.
- O2 (observation, S068): the only row in range whose anchor omits a fetched-UTC stamp (has page-stated
  "Updated : Jun 30, 2026" + text sha). Receipts `20:57:39Z` and round-34.md:35 carry the time; cosmetic.
- O3 (observation, receipts.json): `fetcherSha256` changes mid-batch — `eaf37076…` for S067–S072 vs
  `a36758b5…` for S073–S077 — consistent with round-34.md:30-31 (second batch opened after wave-1
  screening); receipts pin the per-batch fetcher bytes, and no contract clause names the fetcher.

## Residual risk
No live re-fetch: third-party pages can have changed since 2026-10-22; a web row's "revision" is the
retained-text sha + fetch stamp, so upstream edits after that are invisible by design. S070 attribute
presence was checked as words in whitespace-collapsed text, not as the rendered Attributes layout.
Pre-existing W04 (S033) and the S061–S066 rows were out of scope and not audited here.

## Verification gaps
- Did not re-open any URL (bounds: no live requests from this seat); freshness of the 11 pages rests on wave-1 receipts.
- receipts `textRule` ("HTML minus script/style …") was not independently reimplemented; text hashes are
  verified retained-artifact ↔ receipts ↔ row, not extractor correctness.
- No installs/updates performed (system curl/grep/sha256sum/gawk only).

Report: .ufo/waves/round-34/w2/ReviewSourcesRows.md
