# ReviewerEntryPattern

ATTACKS: corpus/knowledge/yahoo-japan-robots-pattern-syntax.md (row S373) at a7a548e102b71bd16b0a6ddafa469393a2c98b69, claim C2 (freshness, quote-true Yahoo! JAPAN robots.txt assimilation).

Method note: entry read via `git show a7a548e…:corpus/knowledge/yahoo-japan-robots-pattern-syntax.md | cat -n` (90 lines). Retained body `.ufo/waves/round-55/sources/S373.html` read as raw bytes and as visible text (Python html.parser, scripts/styles dropped; extraction printed the page title サイト単位、ディレクトリ単位での巡回の拒否設定 2, the 記号/マッチ table, the Allow/Disallow examples and both 注意 notes). Units recounted with the canonical counter definition `units()` and `CJK_RE` from `git show a7a548e…:.ufo/waves/round-55/c55_quote_truth.py` lines 104/167-169.

## QUOTES:

19 quoted spans. Substring/units from one script run: extract `> "…"` spans from the entry text, test `span in body`, count units with canonical `CJK_RE`. All 19 are raw substrings, all sit at/after the body's first `<h2` (byte 2516), all ≤ 25 units.

| line | span | units | substring | rendering faithful |
|---|---|---|---|---|
| 10 | robots.txtでは、以下のパターン記号が使用できます。 | 18 | yes | yes — では以下の/使用できます → "in robots.txt the following … can be used"; no qualifier dropped |
| 14 | ワイルドカードのパターンマッチ | 15 | yes | yes — table cell; "`*` is a" added from table context the page states |
| 15 | URLの末尾文字のパターンマッチ | 13 | yes | yes — 末尾文字 → "ending characters" kept |
| 21 | 任意の長さの、任意のURL文字列にマッチ | 16 | yes | yes — both 任意の kept ("of any length, an arbitrary URL string"); see note N1 |
| 22 | URL文字列のいずれの部分にも使えます。 | 16 | yes | yes — いずれの部分にも → "in any part"; 使えます → "can be used" |
| 26 | 「public」で始まるすべてのディレクトリへの巡回を許可 | 21 | yes | yes — で始まる/すべて/許可 all kept |
| 32 | Disallow: /*.gif$ | 2 | yes | yes — directive name and value literal (example block) |
| 33 | robots.txtが設置されたサイト以下で | 12 | yes | yes — 設置された → "is placed"; サイト以下 → "and below it" |
| 34 | 「.gif」で終わるすべてのファイルへの巡回を拒否 | 19 | yes | yes — negation 拒否 → "refuses"; で終わる/すべて kept |
| 38 | ファイルパスに「.gif」を含む | 10 | yes | yes — ファイルパスに/含む kept |
| 42 | 「$」記号は、文字列の末尾でのみ意味をなします。 | 19 | yes | yes — でのみ → "only at the end of the string" |
| 43 | 末尾であると判断し、以降の文字列を無視します。 | 21 | yes | yes — subject クローラー is in the source sentence and labelled as such |
| 51 | 「$」記号がない場合、 | 7 | yes | yes — ない場合 → "when … absent" |
| 52 | クローラーはプリフィクス（接頭辞）として扱い | 20 | yes | yes — prefix gloss kept verbatim |
| 53 | 記述された文字列を含むURLがすべてマッチします。 | 21 | yes | yes — 記述された/含む/すべて kept ("every URL containing that string matches") |
| 59 | 以下のように書かれていた場合、 | 14 | yes | yes |
| 60 | 2つの「Disallow」の指示は、同等とみなされます。 | 15 | yes | yes — 同等とみなされます → "regarded as equivalent"; the two lines are shown by the page |
| 61 | Disallow: /private* | 2 | yes | yes |
| 62 | Disallow: /private | 2 | yes | yes |

N1 (nit, not a defect): line 24 renders span 21 as "it matches …", while the page's full sentence is 「*」記号は、…マッチ**させるときに使います** ("is used when matching"); the usage qualifier sits outside the quoted span, and flat match behaviour is page-stated in the 注意 notes, so nothing is asserted beyond the page.

## UNTAGGED BEYOND-PAGE:

None found. Sweep of every non-quoted assertion against the extracted visible text: "second refusal page" (page nav + SOURCES row S372 = 設定 1), "the page's table lists `*` and `$`" (table in body), "worked example puts it at the end of a path under the allow directive" (`Allow: /public*/` in body), "treats any `$` it finds as the end" (クローラーが「$」記号を見つけると… in body), "not confined to a path that begins with the string" (page's own .gif parenthetical: ファイルパスに「.gif」を含む…), "no case section" (`grep -c '大文字' S373.html` → 0), "page does not define サイト" — tagged `[INFERENCE]` at line 77 anyway. Process claims at lines 85/88/90 (no robots.txt served, sha/bytes/HTTP 200) are receipts-backed (below), not page claims.

## CONTRAST CHECKS:

All supported, quoted from `git show a7a548e…:<file>`:
- L68 "`*` matches zero or more characters and `$` marks the end of a match" — robots-txt-rules.md:51: "The special character `*` matches zero or more characters, `$` marks the end of a match, and `#` begins a comment (S011 §2.2.3)." Supported.
- L70 "only a final `$` anchors at the end and a non-final `$` is literal" — robots-txt-rules.md:53: "…only a final `$` anchors at the end (a non-final `$` is literal), and path patterns are case-sensitive…". Supported.
- L71 "longest normalized rule value measured in octets, counting `*` and a terminal `$`" — robots-txt-rules.md:55: "choose the longest matching normalized rule value measured in octets, counting `*` and a terminal `$`…". Supported.
- L72 "path patterns are case-sensitive" — robots-txt-rules.md:53 (same line). "sibling page is registry-recorded with § 大文字と小文字の区別" — corpus/SOURCES.md:158, row S372 §-cell: "page body from 更新日 to § 大文字と小文字の区別 (更新日 2010年11月24日)". Supported.
- L73 "matches an allow or disallow path from the first octet of the path" — robots-txt-rules.md:49: "An `allow` or `disallow` path is matched from the first octet of the path…". Supported.
- L77 "file is discovered at the service's top-level path and … project subpaths share the host-root policy" — crawl-scope-per-host.md:7-8: "Robots rules are discovered at the service's root `/robots.txt`, not separately at each project-page subpath."; :10 "host-root robots policy". Supported.
- L79 "`yahoo-japan-rel-nofollow-semantics.md` holds the same operator's other crawl-control page, on the link attribute" — that entry's header line 1 (source S374, § rel属性の利用, info-search.yahoo.co.jp) and H1 line 6 "A link attribute is a statement about endorsement, not a crawl refusal". "neither page states the other's mechanism" — `grep -c 'nofollow' sources/S373.html` → 0; `grep -c` robots.txt/Disallow/パターン on `.ufo/waves/round-52/sources/S374.html` (sha256 3ad358bd…, matching the sha that entry itself cites) → 0, 0, 0. Supported both directions.
- L84 "where robots.txt is fetched from or what its absence means … sibling page (S372)" — SOURCES.md:158 S372 lede: "where it goes, what its absence means…". Supported.

## RECHECK:

- Header trio: lines 1-3 carry `source:`/`verified-at:`/`recheck:` (within first 8 lines); source line names S373 and re-cites it at line 8; URL https://info-search.yahoo.co.jp/archives/002850.php equals receipts.json S373.url; `grep -o 'info-search[^"<]*' S373.html` shows the body carries `archives\/002850.php`; § title and 更新日 2010年11月24日 match the extracted page title and date; fetched/verified-at 2026-10-25 match receipts fetchedAt 2026-10-25T20:40:14+00:00. Verified.
- `grep -F -c '記述された文字列を含むURLがすべてマッチします。' .ufo/waves/round-55/sources/S373.html` → `1`. Prints exactly the `-> 1` the header claims. Verified.
- Body pin: `sha256sum S373.html` → 3173d9613128e1aaa7cb55919fa52438602095bd7bc54d4437760ee8b1c03885; `wc -c` → 9402; receipts.json S373: httpStatus 200, bytes 9402, same sha256, fetchedAt on the round date. Verified (line 88 claims all three).
- The live `curl` half of the recheck command: unrun (assignment scopes recheck verification to the grep half against the retained body; no live fetch performed this seat).

## DEFECTS:

None. No span fails substring or ceiling; no rendering drops a source qualifier; no cross-link statement is unsupported; no beyond-page statement goes untagged.

## NO-DEFECT CHECKS:

- Unit recount (canonical `CJK_RE`): longest spans are lines 26, 43, 53 at exactly 21 units — line 88's "The longest span is 21 units" is true. All 19 spans ≤ 25 (ceiling headroom ≥ 4).
- Under a punctuation-inclusive reading (counting 、。「」（）) three spans would read 22-23 units; the canonical counter regex excludes U+3000-303F and fullwidth ASCII, so the claim stands as written, and ≤ 25 holds under either segmentation (contract's "under any segmentation" intent).
- Negation/scope/only/every/containing/prefix/directive names each appear in the renderings exactly where the Japanese states them (table above): 拒否→refuses (L36), サイト以下→site and below (L36), でのみ→only (L45), すべて/含む→every/containing (L55), プリフィクス kept (L55), `Disallow` names kept (L32/36/64).
- Entry's own meta-claim "nothing was paraphrased inside a quotation" (line 88): confirmed — every span is byte-exact in the body.
- All spans lie inside the page's content block (first `<h2` at byte 2516; every occurrence found at/after it) — the counter's C5 in-content condition is satisfiable for this entry, not just claimed.
- SOURCES row S373 (corpus/SOURCES.md:159) describes this page's content consistently with the entry ("prefix … every URL containing it matches … two refusal lines" paraphrase row); no registry/entry mismatch found.

VERDICT: no defect — all 19 spans are exact raw substrings ≤ 25 units (longest 21, canonical counter), renderings preserve every source qualifier, all cross-links and the recheck/header trio verify; entry S373 survives claim-C2 falsification.
