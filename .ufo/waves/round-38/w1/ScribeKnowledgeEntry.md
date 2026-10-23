# ScribeKnowledgeEntry — round 38

- Axes: operability (primary: actionable publisher knowledge) and freshness (traceable, section-specific sourcing).
- Scope: drafted an append-only lane-reading section for (h), (i), and (k). The draft is not a product edit and makes no implementation-pass claim.
- Artifact: `/fast/scratch/hyaku/kake-r38w1/ScribeKnowledgeEntry/robots-entry-r38.md`, 23 lines; SHA-256 `4fa315b57d42bfc8eebfe25d8a17cc38cd2e51136cce8e8d43c66d255ed63d1a`.

## Stale text and correction
- Only affected/incomplete sentence found: `corpus/knowledge/robots-txt-rules.md:57`, the lane-reading sentence that limits implicit allow to when the file decides (2xx), then says every 5xx URL, including `/robots.txt`, is disallowed.
- The existing status split remains accurate; the sentence does not state normalized matching. Append the draft's clarification (`robots-entry-r38.md:17-23`): during file-deciding status, allow iff the normalized comparison target is exactly `/robots.txt`; this includes `/robots%2Etxt` and `/%72obots.txt`, excludes a non-empty query, case change, or kept reserved escape, treats `/robots.txt?` as a match, and is not overridden by explicit `Disallow: /robots.txt` (S011 RFC 9309 §2.2.2; SCORECARD C2 (k)). No other sentence in the entry explicitly says the implicit match is raw-path-only.

## Evidence and commands
- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 2dab7f3114f3e9dcf072b524c88816ab05fdfcf1:corpus/knowledge/robots-txt-rules.md` — exit 0; emitted the source entry. The located passage is line 57; path construction and normalization are lines 59-63.
- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --no-ext-diff -- corpus/knowledge/robots-txt-rules.md; git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse 2dab7f3114f3e9dcf072b524c88816ab05fdfcf1:corpus/knowledge/robots-txt-rules.md` — exit 0; diff emitted no text; pinned blob `543d03279d28be18c577668f8bfc87a4ac04714c`.
- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; timeout 30 git -C /home/vgpnk/Projects/shokunin/kake-shokunin hash-object corpus/knowledge/robots-txt-rules.md` — exit 0; output `543d03279d28be18c577668f8bfc87a4ac04714c`, confirming the read copy matches the pinned blob.
- `timeout 30 sha256sum /fast/scratch/hyaku/kake-r38w1/ScribeKnowledgeEntry/robots-entry-r38.md` — exit 0; output `4fa315b57d42bfc8eebfe25d8a17cc38cd2e51136cce8e8d43c66d255ed63d1a`.
- `timeout 30 sha256sum /fast/scratch/hyaku/kake-r38w1/ScribeKnowledgeEntry/robots-entry-r38.md && timeout 30 wc -l /fast/scratch/hyaku/kake-r38w1/ScribeKnowledgeEntry/robots-entry-r38.md` — exit 0; same digest; `wc -l` output `22` (22 newline terminators; 23 logical lines).
- `timeout 30 sha256sum /fast/scratch/hyaku/kake-r38w1/ScribeKnowledgeEntry/robots-entry-r38.md && timeout 30 b2sum /fast/scratch/hyaku/kake-r38w1/ScribeKnowledgeEntry/robots-entry-r38.md && timeout 30 wc -c /fast/scratch/hyaku/kake-r38w1/ScribeKnowledgeEntry/robots-entry-r38.md` — exit 0; SHA-256 as above, BLAKE2b `fdcd476f97b0566648d1535565f719d2ec6a88bd90ad58f709e3507bae9de85810f81f09af9ae1fc8f42bf1f4035f24287ee0f36135f8c7bc4a1722edd236902`, size `3463`.
- `timeout 30 openssl dgst -sha256 /fast/scratch/hyaku/kake-r38w1/ScribeKnowledgeEntry/robots-entry-r38.md` — exit 0; same SHA-256 as `sha256sum`.
- Contract evidence read: `SCORECARD.md:2145-2162` defines (h), (i), (k); `SCORECARD.md:2252-2257` clarifies 64 MiB/20 s, malformed `%`, empty query, and explicit Disallow. Existing source entry: `robots-txt-rules.md:57,59-63`. Registry: `corpus/SOURCES.md:19` (S011), `:42` (S034), `:37` (S029), `:97` (S089).

## Findings, gates, and limits
- Provenance caveat: draft cites the requested RFC 3986 §2 for (i), but registry row S029 anchors §3 and S089 anchors §§5.2-5.3, not §2. Flagged for L1 review; registry was not changed.
- No tests, selftests, counters, builds, or implementation commands were run; no network fetch or tool installation. No sealed material was accessed.
- Touched surfaces: this report and the sandbox draft only. No product/source entry, scorecard, source registry, or lane Git state was modified. Out of scope: implementation, gate passage, and round admission/verdict.
