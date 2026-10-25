# ReviewerEntryRefusal
ATTACKS: corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md @ a7a548e102b71bd16b0a6ddafa469393a2c98b69 (row S372, claim C2) — quote truth, rendering fidelity, contrasts, recheck, unit ceiling.

Method: entry + three contrast entries read as pinned bytes (`git -C <lane> show a7a548e1…:<path>`); retained body `.ufo/waves/round-55/sources/S372.html` read and sha-pinned. No lsp device exists in this seat's tool inventory and every target is pinned-revision content, so all evidence is byte-level (git show / grep / python); no semantic-index proof claimed. Line numbers below are the entry's at that revision (`git show … | cat -n`).

QUOTES: (20 double-quoted spans, entry lines 14–102; units = frozen counter segmentation, `units()` in `.ufo/waves/round-55/c55_quote_truth.py:167-169` with its CJK_RE at :104; "strict" adds ideographic/fullwidth punctuation U+3000–303F, FF01–FF64)

| LN | span (head) | units/strict | substring | rendering faithful |
| 14 | 「robots.txt」という名前でテキストファイルを… | 18/20 | yes | yes — 用意=prepare, named file |
| 15 | サイトのルートディレクトリに設置してください | 22/22 | yes | yes — root placement kept |
| 19 | サイトの一番上の階層を指します | 15/15 | yes | yes — topmost level kept |
| 23 | 特定のディレクトリ内のみの巡回を拒否したい… | 24/24 | yes | yes — のみ=only, 内=inside kept |
| 24 | 「Disallow: /」に続いてそのディレクトリ名を… | 20/21 | yes | yes — 続いて=following kept; gloss "refusal value `/`" compresses 「Disallow: /」 (nit, cleared below) |
| 34 | サイトに対する巡回の制限はないものとみなされ… | 24/24 | yes | yes — negation+みなされます kept; condition taken from page preamble |
| 38 | クローラーは巡回のたびにrobots.txtの有無を… | 22/22 | yes | yes — every crawl, presence-or-absence kept |
| 42 | 新たにrobots.txtが設置されていた場合には | 15/15 | yes | yes — 新たに=newly kept |
| 43 | ファイルに記載された内容に従って巡回します | 21/21 | yes | yes — 従って=according to kept |
| 47 | すぐに設定の内容が反映されるわけではありません | 23/23 | yes | yes — すぐに=immediately kept; causal clause matches page |
| 57 | 巡回の拒否（Disallow:）、クローラーの受け入れ… | 22/27 | yes | text faithful; 27 strict = ceiling boundary → D1 |
| 61 | この記述がないときはすべてのクローラーに対する指示 | 25/25 | yes | in-span faithful; modal とみなされます + （「*」と同様） outside span → D3 |
| 71 | 大文字と小文字の違いがあった場合 | 16/16 | yes | yes |
| 72 | 別のものとして扱います | 11/11 | yes | yes — treated-as-different kept |
| 82 | 「Allow:」は通常「Disallow:」と組み合わせて… | 15/19 | yes | yes — 通常=normally kept; "not never-used-alone" gloss correct |
| 86 | 「foo」ディレクトリ以下は巡回を拒否するが | 17/19 | yes | yes — 以下 rendered "under" (inclusive reading; prefix case carried by the example pair) |
| 87 | /foo/bar.htmlは巡回を許可する | 8/8 | yes | yes |
| 97 | 「robots.txt」による巡回拒否はできません | 13/15 | yes | yes — できません=cannot; "not merely ineffective" is a fair gloss |
| 101 | メタタグで、 | 5/6 | yes | yes |
| 102 | インデックスへの登録拒否を設定してください | 21/21 | yes | yes — registration-refusal kept |

All 20 spans: raw substring of the retained HTML bytes AND of tags-stripped visible text (no hidden markup), each page-unique (`raw.count(span)` = 1), each first occurring at/after the first `<h2` (byte 2534). No curly quotes in the entry (regex `[\u201c\u201d]` → 0). The recheck-line grep span is 24 units ≤ 25.

UNTAGGED BEYOND-PAGE:
- Line 21: "Directory scope is a property of the refusal value, not of the file" — the page states only the procedure (add the directory name after 「Disallow: /」); the explicit "not of the file" contrast is drawn nowhere → D2.
- Line 63 rendering states as fact ("the rule is an instruction…") what the page frames as とみなされます ("is regarded as") and drops the page's annotation （「*」と同様）; both lie outside the quoted span, so the rendering could carry them → D3.
- All other non-quoted statements are page-stated (verified against extracted visible text) or tagged: [INFERENCE] at lines 28 (silence = absence, not disagreement), 51 (2010 page not expected to carry a status table), 112 (meta-tag effect unestablished).

CONTRAST CHECKS: (contrast text vs pinned bytes of the named entry)
- L28 → robots-txt-rules.md: "A service publishes its rules at the lowercase `/robots.txt` path in the service's top-level path, with the protocol, authority and port determining the scope (S011 §2.3; S095 …)" — SUPPORTED verbatim.
- L51 → robots-txt-rules.md: "an HTTP 4xx "unavailable" response means crawlers MAY access server resources, while an unreachable file … assume complete disallow (S011 §§2.3.1.1, 2.3.1.3–2.3.1.4)" — SUPPORTED; S372's citation of §§2.3.1.3–2.3.1.4 is the same pair.
- L65 → robots-txt-rules.md: "RFC 9309 matches a crawler's product token case-insensitively, combines the rules of every group … `*` group only when no group matches the token (S011 §2.2.1)" — SUPPORTED; S372's "neither group combination nor the fallback condition" is accurate: the page's （「*」と同様） equates an absent UA record with `*`, it does not state when `*` governs, and no combination rule appears.
- L76 → robots-txt-rules.md: "**Lane reading:** … path patterns are case-sensitive (S011 §§2.2.2–2.2.3…)" — SUPPORTED, and correctly characterized as lane reading, not RFC text.
- L91 → robots-txt-rules.md: "the most specific match (the one with the most octets) is used, … `allow` SHOULD be used, and no matching rule means allowed (S011 §2.2.2)" + lane tie rule — SUPPORTED; the Yahoo page indeed states no precedence rule.
- L109 → S373 cross-link: `git ls-tree` at the revision shows `corpus/knowledge/yahoo-japan-robots-pattern-syntax.md`; its header names § サイト単位…設定 2 → 「*」記号 / 「$」記号 and its body covers the wildcard and the `$` end marker — "this operator's pattern-syntax page, carries that ground" SUPPORTED.
- L8 intro descriptors match the three entries' H1s ("Offline robots.txt rules", "Crawl scope follows host and path", "A link attribute is a statement about endorsement, not a crawl refusal") — SUPPORTED.

RECHECK:
- `grep -F -c 'サイトに対する巡回の制限はないものとみなされます' .ufo/waves/round-55/sources/S372.html` → `1` (claimed 1: exact). `grep -oF … | wc -l` → 1 (also occurrence-unique).
- Live curl arm, run 2026-10-25: `curl -fsSL 'https://info-search.yahoo.co.jp/archives/002849.php' | grep -F -c '…'` → `1` (matches "curl arm 1").
- `sha256sum` retained body → `ee8c9defeeee7abf3f2f6bd4bfb8dbb86c69cf9a272551264aa3f99f76200111` = receipts.json S372.sha256; `wc -c` → 10168 = receipt bytes; receipt httpStatus 200, fetchedAt 2026-10-25T20:40:13+00:00, URL equals the header URL.
- Header trio present in lines 1–3; header § title matches page title "サイト単位、ディレクトリ単位での巡回の拒否設定 1"; 更新日 2010年11月24日 present in page. Runnable and prints what it says: verified both arms.

DEFECTS:
- D1 (low, line 57): span units 22 under the frozen counter CJK_RE but 27 when ideographic/fullwidth punctuation (、（）) counts as CJK characters; the contract C2 ceiling sentence promises ≤25 "under any segmentation". Minimal fix: split the span at 、 — "巡回の拒否（Disallow:）、" (6/7) + "クローラーの受け入れ（Allow:）の記述の前には" (17/22) — making it segmentation-proof; or record the frozen segmentation as canonical in the report/lesson.
- D2 (low, line 21): ", not of the file" is an untagged contrast the page never draws. Minimal fix: delete the phrase (the following rendered gloss "the value is extended by the directory name" already carries the page's content), or append "[INFERENCE]".
- D3 (low, line 63): rendering drops the page's modal とみなされます and its annotation （「*」と同様）, both outside the span. Minimal fix: "(rendered: when this record is absent, the rule is taken to be an instruction addressed to all crawlers — the page adds: the same as 「*」.)" (Extending the quote is not an option: the full sentence is ~34 units, over the ceiling.)

NO-DEFECT CHECKS:
- No fabricated or truncated-mid-morpheme quotes; every span ends at a natural clause boundary.
- L34 rendering's condition "where a robots.txt is not placed" is the page's own preamble (また、robots.txtが設置されていない場合) — accurate, and negation/scope preserved.
- L36 "the page attaches no status code to it": raw page contains no ステータス, 404, 4xx, 5xx (each grep → no match).
- L26 "refuses `/cgi-bin/` only": page has のみ + example `Disallow: /cgi-bin/`.
- L21 examples: `http://example.com/`, `http://example.com/foo/` (one below root), save so the file sits at `http://example.com/robots.txt` — all present verbatim.
- L74 case triple and L89 allow/disallow pair present verbatim in page.
- L104 "names no tag value and no scope": substitute sentence names no meta tag.
- L109 sitemap disclaimer holds: page's サイトマップ/sitemap hits are footer-nav/category links only, no discovery content.
- L82 "normally is the page's own qualifier": 通常 present; page does not say the Allow record is never used alone.
- L97 "unavailable, not merely ineffective": fair reading of できません under the can't-place-files condition.
- L8 lane-history claim ("It did not hold the operator's own rules…") matches contract C2 before-state (0 of the 3 entries at base fcaf4b8).
- No unit counts are stated in the entry; the only count-bearing claim (quote ceiling) was recounted per-span above (canonical max 25, at ceiling on line 61).

VERDICT: S372 entry survives falsification — all 20 quotes raw, page-unique, ≤25 canonical units with faithful renderings, all 7 contrast/cross-link checks supported, recheck verified on both arms and sha-pinned; 3 low-severity defects only (L57 punctuation-inclusive 27-unit boundary, L21 untagged "not of the file", L63 dropped とみなされます modal).
