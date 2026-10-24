# ReopenSourcesMined — live re-open of S067 S068 S069 S070 S073 vs the retained receipts

Seat KakeR34.ReopenSourcesMined (wave 2, freshness), fetched 2026-10-22T21:23:52Z.
Verdict: **all five mined sources survive a fresh GET.** Every visible-text sha256 equals its
receipt, every final URL is unchanged, every status is 200, and each Gate quote from
`corpus/lessons/round-34.md` is present exactly once in the new text. Three bodies changed bytes,
but every changed block lies in a region the fetcher's text rule strips (script/style/tag/
comment): 0 visible words moved (word counts 1884/1276/495/1273/1747 match the receipts exactly).
The C2 grounding is not stale.

| id | status | final URL (== receipt) | text sha equal | body sha equal | Gate quote present |
|---|---|---|---|---|---|
| S067 ogp.me | 200 | https://ogp.me/ | yes | yes | yes (1) |
| S068 Facebook sharing | 200 | https://developers.facebook.com/documentation/sharing/webmasters | yes | **no** | yes (1) |
| S069 Slack robots | 200 | https://api.slack.com/robots | yes | **no** | yes (1) |
| S070 Mastodon PreviewCard | 200 | https://docs.joinmastodon.org/entities/PreviewCard/ | yes | yes | yes (1) |
| S073 Discord link previews | 200 | https://docs.discord.com/developers/link-previews/overview | yes | **no** | yes (1) |

Quotes checked literally (whitespace-collapsed), retained text and fresh text each count 1: S067
"The four required properties for every page are"; S068 "Without these Open Graph tags, the
Facebook Crawler uses internal heuristics to make a best guess about the title, description, and
preview image"; S069 "Specifically, we are looking for oEmbed and Twitter Card / Open Graph tags.";
S070 "Represents a rich preview card that is generated using OpenGraph tags from a URL."; S073 "No
code is executed, so tags added by a client-side script after load are never seen."

Differing spans (body-sha mismatches, reproduced by decompressing the retained gzip):
- **S068** 726,758→726,620 B (net −138): 25 changed line blocks = 19 script + 5 tag + 1 style,
  0 visible. Spans: `nonce="x7wIeGdI"`→`nonce="cq6YKFQd"` on script/style tags; qpl ids
  `"7699599296655639822"`→`"7699605611655494806"`; one `<link rel="preload" …>` tag line dropped
  (the −138 B sits inside those tag/script blocks — no visible byte moved).
- **S069** 38,089→38,089 B: 3 script + 1 tag + 1 comment, 0 visible. `GA.boot_data.version_uid`
  `ff528438…`→`59c3ac3b…`; `visitor_uid` `972810e4…`→`0105d4c2…`; `version_ts` 1792695739→
  1792699608 (66 min newer, consistent with a live re-open); asset hashes `modern.vendor.
  c4408bfe…`→`modern.vendor.395323a5…`, `modern.vendor.95e7dea0…`→`modern.vendor.70d384a6…`;
  server comment `slack-www-hhvm-main-iad-aozl1e2mfi42/ 2026-10-22 13:57:41/` →
  `…-wy1du8i7cgei/ 2026-10-22 14:22:11/`.
- **S073** 536,702→536,702 B: 1 script block, 0 visible. Cloudflare challenge payload in
  `window.__CF$cv$params`: `r:'a4eb7aa35a280a7a'`→`r:'a4eb8e5c79b35cb6'`, `t:'MTc5MjcwMzMyNA=='`
  →`t:'MTc5MjcwNDEzMg=='` (base64 epoch 1792703332→1792704132).
So the only churn is per-request anti-bot boot data (S069, S073) and Facebook nonce/timing churn
(S068); a freshness failure would have to show as a text change, and none occurred.

Commands (sandbox `/fast/scratch/hyaku/kake-r34/w2/ReopenSourcesMined`, TMPDIR set there,
GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset, no lane mutation, no jj, no git write):
1. `python3 -B reopen_sources.py` — exit 0. One GET per source, UA
   `kake-shokunin-round-34-source-opening (one GET per page)`, `Accept-Language:
   en-US,en;q=0.9` (the fetcher's own header), `visible_text()` copied verbatim from
   `.ufo/waves/round-34/fetch_sources.py:38-43`; quotes parsed out of the lesson Gate bullets
   instead of retyped. Print: S067 `200 23130 bodySha=yes textSha=yes quote=yes` · S068
   `200 726620 bodySha=NO textSha=yes quote=yes` · S069 `200 38089 bodySha=NO textSha=yes
   quote=yes` · S070 `200 58446 bodySha=yes textSha=yes quote=yes` · S073 `200 536702
   bodySha=NO textSha=yes quote=yes`.
2. `python3 -B classify_delta.py` — exit 0; region classification above plus retained-vs-fresh
   quote counts `retained=1 fresh=1` for all five at the lesson's stated word counts (8, 23, 13,
   14, 16).
3. Inline python integrity probe — exit 0: each retained `S0NN.txt` hashes to its receipt
   `textSha256` (`retained.txt_sha_matches_receipt=True` ×5), so the baseline is the receipt,
   not a drifted working copy; each fresh `textWords` equals `receiptTextWords`.

Evidence pointers: receipts `kake-shokunin/.ufo/waves/round-34/sources/receipts.json` (S067 `:3`,
S068 `:12`, S069 `:21`, S070 `:30`, S073 `:57`); quotes and access times
`corpus/lessons/round-34.md:30-38` (S067 `:30`, S068 `:31`, S069 `:32`, S070 `:33`, S073 `:36`);
retained inputs `.ufo/waves/round-34/sources/{S067,S068,S069,S070,S073}.{html.gz,txt}`; fetcher
sha256 `a36758b506a4870798bcb29f7805b3f832be5021b10123793d9e2b74e1a20fb7` (= `fetcherSha256` for
S073–S077; S067–S070 carry `eaf37076…`, an earlier revision with an identical `textRule` whose
retained text still reproduces the receipts' `textSha256`, verified). Sandbox artefacts:
`reopen_sources.py`, `classify_delta.py`, `reopen.json`, `S067.now.*`…`S073.now.*`.

Not verified / limits: only the five assigned ids were re-opened (S071, S072, S074–S077 untouched;
the reject rows are another seat's `ReopenSourcesRejected.md`); quote checks are literal presence,
not semantic reading — the equal text hashes make surrounding-context drift impossible for the
three unchanged sources; one GET per URL as instructed, no retry or conditional request, so a
transient CDN variant cannot be formally excluded for the three body mismatches, though their text
equality and the identified per-request tokens make a content change implausible; no tool was
installed or updated.
