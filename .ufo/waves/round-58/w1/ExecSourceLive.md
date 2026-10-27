# ExecSourceLive

Claim C3 (freshness, sourced), round-58 w1, base 0440485. Live re-open of the two claim sources plus the linked
identification article, compared node-for-node with the retained bodies using the counter's own
`text_segments` (imported from `.ufo/waves/round-58/c58_quote_truth.py` via importlib). Scratch:
`/fast/scratch/hyaku/kake-r58/ExecSourceLive` (deleted after copying receipts to `w1/ExecSourceLive.files/`).

## FETCHES

`curl -sSL --compressed -A 'Mozilla/5.0' --max-time 60` on 2026-10-26 (curl `Date` header 23:55:17–23:55:21 GMT).

| id | url | HTTP | transfer (gzip) | decompressed | sha256 |
| --- | --- | --- | --- | --- | --- |
| S423 / 3457 | https://ziyuan.baidu.com/college/articleinfo?id=3457 | 200 | 10,438 B | 29,007 B | `52c203374eededc6d8c177ed394d87a53a8feca9875d78adc5fcd2a27f9b4829` |
| S424 / 3028 | https://ziyuan.baidu.com/college/articleinfo?id=3028 | 200 | 8,015 B | 22,476 B | `3e4bd06c617266eb3b3d2e5902a83f6a53269960c2752f0b786278623f4e261d` |
| 2855 (no row) | https://ziyuan.baidu.com/college/articleinfo?id=2855 | 200 | 9,125 B | 30,377 B | `5920cfe823da5e3518c085b9956bbb3087ea392df3e123bad3af746a41f160f2` |

Retained bodies (unchanged on disk): S423 `8b8aef60bd7e315799e9a97dadfd02a5982f8c7e17b9d4064a6fc3913a0736ec`, S424
`3ef1275b730230f2cb9c14b28b1c4bd08dc363dc7941b63d06c507fb2729cad1`. Decompressed lengths are identical to the
retained lengths (29,007 / 22,476); only the sha256 differ.
Response headers carry **no validators**: `Cache-Control: no-store, no-cache, must-revalidate`, no `ETag`, no
`Last-Modified` — so freshness can only be shown by content comparison, not by a 304.

## ARTICLE DIFF

`cmp -l` retained vs live: **+S423: 8 differing bytes; S424: 8 differing bytes**, in 4 two-byte sites each, and every
site is inside a `<script>` tag — none inside the article block:

| page | offset | retained | live | what it is |
| --- | --- | --- | --- | --- |
| S423 | 22469 | `cdnversion=202610270735` | `cdnversion=202610270753` | static-asset cache buster (timestamp) |
| S423 | 22562 | `wrapper.js?cdnversion=1793057745` | `…=1793058819` | cache buster (epoch) |
| S423 | 23063 | `ziyuan.baidu.com%3A8021` | `%3A8087` | port in an embedded config URL |
| S424 | 15938 | `cdnversion=202610270735` | `cdnversion=202610270753` | cache buster |
| S424 | 16031 | `wrapper.js?cdnversion=1793057746` | `…=1793058822` | cache buster |
| S424 | 16532 | `ziyuan.baidu.com%3A8054` | `%3A8010` | port in an embedded config URL |

Article-block comparison (counter's own bounds: start `class="article-info"`, end `往期回顾` for S423 / `推荐阅读` for S424):

- **Raw article-block bytes are identical** for both pages (`diff` of the block slices → no output).
- Text nodes via `qt.text_segments`: **S423 155/155 nodes identical, S424 30/30 identical, `diffs: []`**; joined-node
  sha256 prefixes `88c07fa98e07a1f0` (S423) and `9d9d01c1eef55c71` (S424) match retained and live.
- Therefore the byte deltas are cache-busting tokens and a per-request server port only — no article content changed
  between the retained fetch (20:35 local) and the live re-open. [INFERENCE] the port varies per request/edge node.

## RECHECKS

Staged recheck grep, run on both the retained body and the live body:

- `grep -F -c '非*.baidu.com或*.baidu.jp即为冒充。'` on 3457 → **1 retained, 1 live** (identical). It is a raw substring
  of one text node in both (raw context: `…Baiduspider的hostname以*.baidu.com或*.baidu.jp&nbsp;的格式命名，非*.baidu.com或*.baidu.jp即为冒充。</p>`).
- Same grep on 3028 → **0** (S424 carries no identification sentence; its article is the unblocking procedure).
- `span_tools.py check S423 '非*.baidu.com或*.baidu.jp即为冒充。'` → `6u 28c in_text_node=True count_in_body=1 unique=True within_ceilings=True`
  — quote-viable on S423 for the entry scribes. The whole enclosing node (30u/107c) is over both ceilings, so a quote
  must be this shorter span (or another sub-span); the same sentence in 2855 is split by `<span lang="EN-US">` tags and
  is **not** quote-viable there.
- The two other `grep -F -c '<quote>'` occurrences in `w1-spec.json` are unfilled placeholders owned by the entry seats;
  nothing concrete to run for this seat.

## 2855

`轻松两步，教你快速识别百度蜘蛛（User-Agent）`, printed 发布日期：2020-05-19. Both new pages link it inside their
article blocks: S423 `详情可参考文档：《<span>轻松两步，教你快速识别百度蜘蛛》`, S424 as a bare URL anchor
(offsets 11492 / 10456, both within the counter's block bounds).

Article block (same markers, `class="article-info"` → `推荐阅读`, offsets 9442–18758): 105 non-empty text nodes
(dump: `w1/ExecSourceLive.files/s2855_nodes.txt`). IP-range sentence and its sub-span:

- node: `还有很多站点想得到百度蜘蛛的IP段，想把IP加入白名单，但IP地址范围动态变化不固定，我们无法对外公布。` — 42u/52c, over both ceilings.
- sub-span `IP地址范围动态变化不固定，我们无法对外公布。` — **19u/23c**; `IP地址范围动态变化不固定` — 11u/13c.
- Both are absent from S423 and S424 (`IP地址范围` count 0 in both), i.e. this fact exists only on 2855, and 2855 has
  no row, so `span_tools.py` (ids fixed to S423/S424) cannot check any 2855 span and no 2855 quote path exists.

Does it add a fact the two entries should cross-reference? **Yes, one, for the S424 entry primarily:**

1. *Baidu does not publish Baiduspider IP ranges because they change dynamically.* This is the stated reason why
   identification has to be reverse/forward DNS (it explains S423's DNS method) and why the S424 IP-ban step cannot be
   closed with a fixed Baidu-IP allowlist. S424's only 白名单 mention is a UA-strategy allowlist
   (`针对百度UA添加策略白名单`), not an IP-range allowlist, so nothing conflicts — the entries just do not state the
   constraint. Suggested handling: one paraphrased cross-reference sentence in the S424 entry (and optionally S423),
   **not** a quote, unless the L1 decides to add a 2855 row.
2. A worked reverse-DNS example (2855 only): `host 111.206.198.69` → `69.198.206.111. in-addr.arpa domain name pointer
   baiduspider-111-206-198-69.crawl.baidu.com.` → `has address 111.206.198.69`. S423 has **0** occurrences of
   `crawl.baidu.com`, so it illustrates but does not supersede S423's rule. Its host string is 1u/42c — over the 40-char
   ceiling, so even with a row it could not be quoted whole.

Duplication check (2855 is the older, shorter ancestor of S423's methods section): 21 of 2855's 105 nodes appear verbatim
in S423 and 7 in S424; the UA lists (mobile, `Baiduspider-render`, PC, Smartapp) are byte-identical to S423's. 2855 is
dated 2020-05-19 vs S423 2022-08-19, so it contributes **no newer doctrine**, only the IP-range non-disclosure statement
and the example.

No tool installs were needed; no pacman transaction was run.

VERDICT: Both claim sources re-open byte-stable in content (article blocks raw-identical, all text nodes identical; only 8 bytes/page of cache-buster and port tokens differ) and the staged 3457 grep still returns 1; 2855 adds one non-quotable fact (Baidu publishes no Baiduspider IP ranges) worth a prose cross-reference, L1 to decide.
