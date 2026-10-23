HOLDS — routed defect 3: the comment at `scripts/sitemap_audit.py:67-104` matches SKILL.md and observed `_parse_url` behaviour. No defect found.

## Attacked
Comment block `scripts/sitemap_audit.py:67-104` (assignment's ":67-82" is the round-41 paragraph; the block runs to line 104) vs SKILL.md ("sitemap_audit" rows: round-41 URL rule + round-42 scanner sections) vs actual behaviour.

## Identity
- Tool probed: `scripts/sitemap_audit.py` sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` (= frozen build identity).
- `tip41.py` (round 41) `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`; `base40.py` (round 40) `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e` — both match the SCORECARD/context identities.
- Probe: `/fast/scratch/hyaku/kake-r42w2/ReviewCommentFix/probe.py` sha256 `f59010fa9caa2275a01a598ac0cb38b305ccafffde1eb7306aa4645763b4b97b`.

## Commands (exit codes)
- `python3 -B probe.py` (loads all three tools, calls `_parse_url` on 15 values, asserts round42==round41) → EXIT=0.
- `timeout 300 ~/.local/share/uv/python/cpython-3.10.22-linux-x86_64-gnu/bin/python3.10 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` → EXIT=0, "PASS 235/235" (17.8 s wall).
- No tools installed; pacman untouched.

## Per-sentence result (comment line: claim → verdict)
- 67-68 first judged as written vs RFC 3986 URI-with-authority, every ASCII char (sent 22/S117) → **holds**: `_parse_url` calls `_uri_ok` before urlsplit (`sitemap_audit.py:291`); `http://ex<mple.com/x`, `http://example.com/a[b`, `http://u@x@ample.com/x`, `http://example.com/x%zz`, `http://example.com/x#f#2` → None (round 40 accepted all five; 41/42 reject). Header "sentences 22, 24-27" verified against `.ufo/waves/round-39/c1-contract.md:61-73` (22=absolute URL, 24-27=scope).
- 69-71 "Not changed from round 40... U+0080+ accepted wherever RFC 3986 allows `unreserved`" → **holds** (colon-scoped reading, same as tip41's own comment at tip41.py:69-70): `http://exämple.com/päth?q=é#fö` accepted by all three tools, identical tuples. Matches SKILL round-41 "Unchanged on purpose... broader than RFC 3987 ucschar".
- 71-74 bracket charset `[A-Za-z0-9._~:!$&'()*+,;=%-]`, zone id with non-ASCII or `|` rejected, urlsplit judges literal address + port range → **holds**: `_IP_LITERAL_ASCII = _USERINFO_ASCII` (`:124`) = that set; `_TABLE_IP_LITERAL = _class_table(..., non_ascii=False)` (`:130`) rejected at `:189-190`. Probes: `[fe80::1%é]` → None, `[fe80::1%en|0]` → None (round 40 accepted both — exactly SKILL's "where the round-40 tool accepted some of them"); `[zz::1]` → None (urlsplit address), `:65536` → None (urlsplit port range, RFC 3986 does not forbid — matches SKILL).
- 76-78 same grammar, byte-table scanner vs one regex with `\u0080-\U0010ffff` class → **holds**: scanner is `translate`-table based (`:105-130, :189`); the slow class exists in tip41.py:73.
- 78-79 keeps round-41 judgments (claim C1) → **holds on evidence available**: 15/15 probe values round42 ≡ round41 (exact tuple equality, including accepted-zone-id and rejection cases); the "every value the counter generated" quantifier is the scored C1 predicate (SCORECARD round 42, met), not re-derived here.
- 80-81 no possessive quantifiers; selftest passes under Python 3.10 → **holds**: grep `[*+?]\+` over the file → no hits; 3.10 selftest PASS 235/235.
- 83-98 grammar table → **holds**: every production matches the byte tables (`_SCHEME_ASCII:132`, `_USERINFO_ASCII:120`, `_REGNAME_ASCII:121`, `_PCHAR_ASCII:122`, `_QUERY_ASCII:123`, port `*DIGIT`, reg-name `1*` = non-empty host) and probes (second `@`, `%zz`, `#f#2`, `[` in path all rejected).
- 100-103 non-ASCII = one UTF-8 run ≥0x80, accepted as unreserved, rejected inside IP-literal, exactly as round-41 class → **holds**: `exämple.com` accepted identically; `%é` in brackets rejected identically (tip41's `_UNRESERVED` includes `\u0080-\U0010ffff`, its bracket class excludes it).
- 103-104 `%` is a literal character inside an IP-literal (no percent-triplet requirement) → **holds**: `http://[fe80::1%eth0]/x` → `('http','fe80::1%eth0',80,'/x')` in all three tools (SKILL: "`%25eth0` and `%eth0` stay accepted (legacy laxity)"; `%25eth0` probe likewise equal).

## Adjacent observation (out of scope, no action taken)
`/fast/scratch/hyaku/kake-r42/shared/tip41.py:71-72` still says an IP literal's contents are "judged only by urlsplit below" while its regex at `:80` pre-filters the charset — stale comment in the round-41 copy; the round-42 comment under review states the behaviour correctly.

## Residual risk / gaps
- "Every value the counter generated" (line 78-79) and "×4-10 slow" (line 78) rest on the scored C1 counter and SCORECARD timing rows, not a fresh run by this seat (counter runs are the L1/executor seats' lane; my probes cover judgment equality only).
- "One UTF-8 sequence whose bytes are all >= 0x80" is true for the decoded `str` inputs the tool sees; no lone-surrogate path was probed (XML parser output domain, cannot occur from file bytes).
