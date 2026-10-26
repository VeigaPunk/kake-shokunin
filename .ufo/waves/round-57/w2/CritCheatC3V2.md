# CritCheatC3V2

C3 version 2, attacked by experiment. Counter read: `.ufo/waves/round-57/c57_quote_truth.py` at lane revision
`4b8c73050470ada9e6583f3b12d659d1bed6a17f` (blob `a51e5b6e7e7ecddc60da42b097130f28130b7742`); the lane HEAD is
`51921b97` (W2 working-tree files), so every result below names the scratch tip it was measured at.
Scratch clone `/tmp/critc3v2.rxokq3` (own toplevel; commits with `-c user.name=selftest -c user.email=selftest@local`).
Command for every row: `python3 -B .ufo/waves/round-57/c57_quote_truth.py --root $D --revision <tip>`.
Lane paths touched: this report only. Tool installs: none.

## EXPERIMENTS:

Every row is **confirmed by running** at the named tip unless marked `[INFERENCE]`. `$D` = the scratch clone.

| Exp | Condition attacked | Change in `$D` (files) | Tip | Result |
| --- | --- | --- | --- | --- |
| E0 | control | none | `4b8c730` | `8/8 met=True`, exit 0 |
| E1 | (1) off-topic text-node spans, entries only | 2 entries + 2 `validate/` copies (4) | `7a37a5d` | `8/8`, exit 0; entries 286 B + 255 B (real: 7314 B + 8933 B) |
| E2 | (1) same + both lesson `## Gate` quotes replaced | 5 | `3c04599` | `8/8`, exit 0; Gate quotes are intro fluff and a speed label |
| E3 | (2) three page-unique spans = headings/label lines | 4 | `dd685f2` | `8/8`, exit 0; S421 spans are `<h3>` text, S422 spans are `<p><span>` label lines (not `<hN>`) |
| E4 | (3) real entries, every rendering replaced | 4 | `71865a7` | `8/8`, exit 0; 21/21 `(rendered: …)` replaced with `NONSENSE — the page says the exact opposite…` |
| E5 | (4a) body byte edit, receipt untouched | `S421.html` + `\n` (1) | `edf2788` | `6/8` exit 1; C5 digest + C6 sha256/bytes fail; sha256 `32eaf8b7…`→`966f08b2…` |
| E6 | (4a) body + `sources/receipts.json` made self-consistent | 2 | `ca9c9a1` | `7/8` exit 1; C5 still fails on the frozen constant (`c57_quote_truth.py:94,347-348`), C6 passes |
| E7 | (4b) amended constant in a counter **copy** (uncommitted) | 1 copy | `ca9c9a1` | copy `8/8`, frozen counter on the same tree `7/8` |
| E8 | (4b) amended constant committed at the canonical path | 1 (counter) | `8c354cb` | canonical counter `8/8`, exit 0; diff vs `4b8c730` is one line (`BODY_SHA256`) |
| E9 | entry `source:` URL and Gate `§` label unverified | 5 | `5241704` | `8/8`, exit 0; `source:` = `https://example.invalid/…`, S421 Gate `§ 完全无关的小节`, stale `(9 units; … sha256 32eaf8…; 34750 bytes)` for a 12-unit quote |
| E10 | selftest vs amended constant | copy | `4b8c730` / `ca9c9a1` | frozen: `101/101`, exit 0. Amended copy: `101/101`, exit 0 at `ca9c9a1`; 12 FAIL, exit 1 at `4b8c730` |

Boundary probes (**confirmed by running**): `往期回顾` is S421's `ARTICLE_END`, so `in_content(…) == False` — the end marker's own
text cannot be quoted. The byline node `发布日期：2022-09-09` is 4 units, below the 6-unit floor for a counted span (it is only
required as the row anchor's printed date). `发布日期`-bearing spans are otherwise usable.

## MINIMAL JUNK:

- **Minimal tree** (E1): 4 files, 32 insertions / 360 deletions, **541 bytes** of entry content, tip `7a37a5d` → `8/8`.
  It keeps the real registry rows, receipts, mirror and Gate lines; it only replaces the two entries and their `validate/`
  copies. No registry cell can be junked (title = page `<title>`, anchor 4+ units and page-unique in a text node, URL and
  used-by pinned), so the entries are the whole attack surface.
- Structural minimum per entry: 9 lines — `source:`/`verified-at:`/`recheck:` (3), three distinct 6+-unit text-node spans,
  fillers, and the id cited on line 9+ (`lines[8:]` is the citation window). No H1, no blockquote, no dead-link term.
- With **every quoted surface** junked (entries **and** both Gate quotes): 5 files, 520 bytes, tip `3c04599` → `8/8`.
- C7/C8 stayed green in every entry attack by copying the junk text into
  `.ufo/waves/round-57/assimilation/validate/corpus/knowledge/…`; the census argv/stdout is the real build's. C7 is byte
  equality, not a record that the census saw this content.

## WHAT THE COUNTER CANNOT SEE:

1. **Relevance/support.** `in_content` + `units` + `count==1` are the only content tests (`c57_quote_truth.py:162-190`). Off-topic
   intro/promo/UI-step text ("最近平小雕在观察和学习时，", "——什么是【搜索问答剧场】？", "登录百度搜索资源平台",
   "近期百度搜索最大的动作应该就是百度", "天左右，现在提升") passes (E1), and so do bare list-item fragments from the page's
   causes list ("服务器不稳定", "网站短暂无法访问，") when used in the entries and the Gate lines (E2). Confirmed by running.
2. **Renderings.** The counter reads only double-quoted spans; the 21 `(rendered: …)` glosses were replaced with a flat contradiction
   and the score did not move (E4). Confirmed by running.
3. **Entry `source:` URL.** C2 (`c57_quote_truth.py:259-280`) requires only that the line names the id; `https://example.invalid/…`
   passes (E9). Confirmed by running.
4. **Gate `§` anchor.** The Gate line's section label is never compared to `row[5]` or the body; `§ 完全无关的小节` passes (E9).
   Confirmed by running.
5. **Gate annotations.** `(N units; … sha256 …; N bytes)` is free text; a 12-unit quote annotated `9 units` with the old digest
   passes (E9). Confirmed by running.
6. **Entry shape.** The title/page-title equality is a **registry-row** check (`c57_quote_truth.py:346-351`), not an entry H1 check;
   neither entry has a title, and bare quoted lines (no blockquotes) count. Confirmed by running (E1).
7. **Boundary text.** `往期回顾` is excluded by `ARTICLE_END`; the byline is 4 units, under the 6-unit floor. Confirmed by running.
8. **C7 census receipt.** Content-blind, as above. Confirmed by running (E1/E2).
9. **`sources/receipts.json`.** C6 compares it to the body, so editing both is self-consistent (E6, `7/8`): the only catch is the
   in-code constant. C1's population regex (`c57_receipt_pins.py:73`) covers only `.ufo/waves/round-5[2-7]/control(s)/**`, so this
   file is outside its history walk. E6 run; C1 exclusion is `[INFERENCE]` from the regex (grep run).
10. **The counter itself.** `grep -c c57_quote_truth .ufo/waves/round-57/c57_receipt_pins.py` → `0`; `COUNTER` is
    `c57_receipt_pins.py:69`, and `first_add` only requires the measured revision to descend from the commit that added *C1's*
    counter (`c57_receipt_pins.py:234-237`). `after-c3` is accepted on a first-line regex plus `EXIT=0`
    (`BODY_FIRST["3"]`, `c57_receipt_pins.py:77-80`), not a re-run — only `after-c1` is re-derived. `contract.json` carries no
    counter digest (grep `sha256` → none) and `measured.json` does not exist at `4b8c730`. When the amended counter is committed
    at the canonical path the canonical command prints `8/8` (E8). **So the answer to the assignment's question is: no, C1's pin
    does not count this.** Confirmed by running E8 and the greps; the "C1 would accept the matching receipt" step is `[INFERENCE]`
    (not run: C1 needs the full W2 evidence set).
11. **Counter v1 provenance (secondary).** `git show b9a5d01:.ufo/waves/round-57/c57_quote_truth.py` has
    `HELD_BODY_SHA256: dict = {}`; the S421/S422 pin **values** are in `sources/receipts.json` at `b9a5d01`, but the pin
    `BODY_SHA256` was written at `cddef5b` (wave 1). The line comment "frozen at the contract commit" describes the values'
    provenance, not an enforcement that existed at that commit. Confirmed by running `git show` / `git log -S`.
12. **Body sha256.** Keeping the digest across an edit is impossible in practice: one appended byte changed `32eaf8b7…` to
    `966f08b2…` (E5), a preimage is infeasible, and C6 also compares `bytes`, so a same-length collision would be needed; even then
    both `receipts.json` and `BODY_SHA256` must be rewritten (E6 shows the receipt alone fails). E5/E6 confirmed by running;
    preimage claim is `[INFERENCE]` (standard assumption).

Impacted axes: **freshness (C3)** — the predicate certifies located substrings, not that the entry states a page fact; **calibration
(C1)** — the counter bytes and `sources/receipts.json` are outside the pin walk; operability is untouched (C2).

## RECOMMENDED CHANGES:

1. **Pin the counter bytes (smallest safe fix for E8).** Record the sha256 of all three counters at `b9a5d01` (or `4b8c730`) in
   `contract.json` and have C1 compare `git show <measured>:<counter>` against it before crediting `after-c3`; alternatively require
   the `after-c3` receipt to carry that digest. Without this the instrument is editable by the revision it measures.
2. **Make the Gate line's typed fields real.** Recompute `units`/`sha256`/`bytes` from the span instead of trusting the text, compare
   the Gate `§` with `row[5]`'s anchor, and compare the entry `source:` URL with `ROW_URL` (E9). These are three cheap checks in C5/C2.
3. **Bind C7 to content.** Put the sha256 of the two admitted entries into `census-stdout.txt` (or a census receipt) so a reused
   census cannot validate new entry bytes.
4. **Do not fake a topic test in the counter.** A keyword filter invites keyword-heavy junk; support is a reviewer judgement. The
   smallest honest counter-side rule is one span per entry drawn from a text node that also contains a page-named dead-link kind
   (e.g. 死链 / 404 / 状态码), with the reviewer still reading the surrounding sentence.
5. **Extend C1's population** to `sources/receipts.json` (or state in the contract that source receipts are outside the relabel walk),
   since E6 shows it is the first file a self-serving revision rewrites.

VERDICT: C3 v2 is met 8/8 by 541 bytes of off-topic article text (no dead-link statement, no rendering, no title) and by a one-line amendment to the counter itself; C1 does not pin the counter, so both holes are invisible.
