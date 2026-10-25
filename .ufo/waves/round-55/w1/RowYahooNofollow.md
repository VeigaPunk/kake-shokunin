# RowYahooNofollow

Claim C1 (coverage-map calibration) for `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`.
Read: the whole knowledge file (68 lines), `corpus/README.md:1-63` header + 3 existing map rows,
and read-only `round-52/sources/receipts.json`. No file edited; no git/jj mutation; no pacman;
no tool install needed.

## ROW:

```markdown
| Yahoo! JAPAN rel=nofollow semantics | `knowledge/yahoo-japan-rel-nofollow-semantics.md` (S374) | One operator's rel=nofollow reading: the phrase is a crawl qualifier on the link target's page, the URL may still be used to discover new pages, and the attribute is not weighed in result ordering; other operators and attribute values out of scope. |
```

Constraint check (all run, all pass):
- 3 cells, `| Area | Entry | Coverage |` shape; matches the 47 existing 3-cell rows in README.
- Area 4 words (<= 8). Entry is the backticked `knowledge/<file>` path + `(S374)` copied from the
  file's own `source:` line (`:1`), same `(S###)` convention as `knowledge/field-performance-cwv.md` (S036–S039).
- Coverage 42 words (10-45); no `|`; does not start with `TBD`.
- Shared 5+-letter words with H1/first 1500 chars: `attribute`, `crawl`, `nofollow`, `pages`,
  `reading`, `result`, `still`, `target`, `weighed` (H1 supplies `attribute`, `crawl`).
- No duplicate row exists: the string `yahoo-japan-rel-nofollow-semantics` does not occur in README.

## EVIDENCE:

Every passage below was verified as an exact raw substring (python `in`, count 1) of the file it is
attributed to. Quote lengths: 24 CJK units for the Japanese passage (one unit per CJK character,
no whitespace tokens), word counts for English passages.

1. `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md:56-58` — grounds "crawl qualifier on the
   link target's page": "statement. The phrase includes a crawl qualifier: the site owner is taken to"
   (13 words); `:57` continues "**not recommend the crawling of the link target's web page**".
2. `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md:11` — the file's raw source quotation:
   "このリンク先のウェブページの巡回を推奨していない" (24 units). Verified raw in the retained body
   `.ufo/waves/round-52/sources/S374.html` (count 1), inside `<h2>リンク先のウェブページの巡回制限　― rel属性の利用</h2>`
   — the section the file names on `:1` and `:20`.
3. `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md:29` — grounds "URL may still be used to
   discover new pages": "The page says the tagged URL is used to discover" (10 words).
4. `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md:19` — grounds "not weighed in result
   ordering": "the attribute is not weighed when the result order is decided" (11 words).
5. `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md:38` and `:40` — grounds "one operator's" /
   "other operators and attribute values out of scope": "it is one operator's page, and the lane has no"
   (10 words) and "It does not establish how other link-attribute values (`sponsored`, `ugc`) are read by this"
   (14 words).

Provenance of the `(S374)` id: `round-52/sources/receipts.json` records S374 =
archives/002851.php, HTTP 200, 8153 bytes, sha256
`3ad358bdbe7a74798df151c282e4b57af7475686dc405b3f8bad08f68881aecb`, fetchedAt 2026-10-25T10:19:41+00:00.
That digest equals the digest the knowledge file states on `:66`, and equals the digest I recomputed
from the retained body (`hashlib.sha256`). The file's `:1` date `fetched 2026-10-25` is therefore
accurate for S374 but denotes a round-52 fetch, not a round-55 one.

## RISKS:

- **No round tag in the header.** `:1-4` carry `source:`, `verified-at:`, `recheck:`, `ground:` and
  no round tag, so the Area cell carries none. The only round string in the file is `Round-54 correction`
  (`:52`), which labels a correction, not the file's provenance; borrowing it as an Area tag would
  misstate when the body was captured.
- **Provenance is round-52, not this round.** The row's source S374 is not among round-55's retained
  bodies (S372/S373/S418), and `:68` states the evidence was "a local re-open of the retained round-52
  HTTP-200 body, not a fresh network fetch". The row must not be read as a round-55 fetch.
- **Second quotation exceeds the 25-unit cap.** The file's quotation on `:17`
  (検索結果の表示順序を決める要素としては考慮されません) is 26 CJK units, so it cannot be reproduced
  under the unit rule; the row does not quote it. The ordering clause rests on the file's own gloss at
  `:19`, which is itself a rendering of that quotation.
- **Superseded gloss inside the file.** H1 (`:6`) says "not a crawl refusal", while the body gloss at
  `:13-14` renders the phrase as endorsement only; `:54-62` supersedes that gloss and restores the crawl
  qualifier. The row says "crawl qualifier" and deliberately does not say the target is fetched or not
  fetched — the file asserts neither.
- **Unsupported detail left out.** `:21` says the attribute is "one of its three routes"; the file never
  enumerates the three, so the row omits the count. `:51` says "The lesson Gate pins the first of the
  two" but names no gate path or command, so the row claims no gate.
- **Cross-reference not verified here.** `:27` cites S367 (meta/header link-target restriction), which
  is not in this round's retained set; nothing in the row rests on it.
- **Scope of the source.** One operator's page, updated 2010-11-24 per `:1`; `:43-44` states no
  operator-owned surface was fetched this round. The row therefore says "One operator's ... reading"
  and does not generalize to other engines or to live crawl behaviour.
- **Freshness.** `recheck: 180d` (`:3`) with `verified-at: 2026-10-25` implies a recheck around
  2027-04-23; the row states no freshness claim.

VERDICT: One coverage-map row drafted and constraint-checked (42-word Coverage, 4-word Area, S374 Entry); all five evidence passages verified as raw substrings, quote-unit and digest checks pass, no files edited beyond this report.
