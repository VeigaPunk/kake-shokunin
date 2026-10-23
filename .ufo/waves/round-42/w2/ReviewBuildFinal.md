# ReviewBuildFinal — wave 2 seat: final build bytes URL-section review (falsify C1)

Verdict: NO divergence found. The final scanner `_parse_url` equals the round-41 regex `_parse_url` on every value probed (~5.8M differential checks, all equal). No witness value; no finding with a confirmed disagreement.

## What was checked
- Target bytes: `scripts/sitemap_audit.py` at 721310b (sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`), identical to the scored build 020bc457 (`git diff 020bc457 721310b -- scripts/sitemap_audit.py` empty, exit 0).
- Round-41 reference: `git show 1ef7a0e9:scripts/sitemap_audit.py` (sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`).
- Whole-tool diff (`diff <(git show 1ef7a0e9:scripts/sitemap_audit.py) scripts/sitemap_audit.py`): every change confined to the URL gate (regex `_URI_RE` at tip41 lines 73-87 replaced by the byte-table scanner `_uri_ok` at lines 105-284; gate call at 290). All other code byte-identical. Callers unchanged: `_parse_url` at 506, 580.
- Grammar classes compared by reading: scheme, userinfo, reg-name, IP-literal (ASCII-only both, `%` literal inside brackets), port digits, path, query/fragment classes are the same sets; the only grammatical backtracking point (userinfo `@` split) is mirrored by the `starts` loop (lines 275-283); the port/host split is deterministic in both because `:` is in neither host class.

## Differential evidence (all `python3 -B`; scripts in seat sandbox, sha256 below)
- `diff_fuzz.py` (445c8d26): exhaustive length 0-4 over a 34-char alphabet (letters/digits, `:/?#@%[].-_~!$&'()*+,;=`, space/tab/newline, é/€/中) = 1,376,831 values; random lengths 5-8 = 1,770,000. Mismatches: 0.
- `diff_targeted.py` (761b2b98): sampled structured cross-product (14 schemes x 11 userinfos x 24 hosts x 12 ports x 13 paths x 12 queries x 9 frags, 2M samples + prefixed variants) = 2,666,667; ~150 targeted singletons (surrogates, non-ASCII, IP-literals incl. zone-id forms, ports 65535/65536/empty, malformed/missing percent triplets, empty authority, double `@`, `#`/`?`/`/` orderings); long values (100k-char host, 20k non-ASCII, 90k percent-triplet path, 50k-digit port). Mismatches: 0.
- Byte sweep: every byte 0x00-0x7F inserted into each of 9 slots (scheme/userinfo/host-end/host-start/port/path/query/frag), exotic code points (emoji surrogate pair, U+F8FF, U+FFFF, U+10FFFF), `%`+byte pairs, and structural extras (e.g. `a://h://x`, `http://h#f#g`, `http://h:?x`) = 1,636. Mismatches: 0.
- Total probes ≈ 5.82M; verdict equality on both None and tuple outcomes. Grammar-level gate differences found by reading (e.g. `http://u@?x` is regex-accepted, scanner-rejected; `http://[a-b]/` grammar-passing both) all collapse at the shared `urlsplit` stage — observable `_parse_url` equal.
- Python 3.10.22 (`~/.local/share/uv/python/cpython-3.10.22-linux-x86_64-gnu/bin/python3.10`) `-m py_compile`: OK (exit 0).

## Per checked statement
- "the same grammar, matched by a byte-oriented scanner" (lines 76-82): holds — judgment-equivalent on every probed value.
- Comment claims (lines 67-74, 100-104): accurate as far as probed (zone-id non-ASCII/`|` rejected; `%` literal inside brackets; U+0080-U+10FFFF accepted in unreserved slots).
- C1 equality claim on counter-generated runs: not independently re-scored (L1 receipts 10/10 x3 exist); the far broader differential above supports equality beyond the counter corpus.

## Residual risk / verification gaps
- Differential is empirical, not a proof; pathological classes with no short witness (e.g. adversarial multi-megabyte values with complex `%`/non-ASCII interleavings) were sampled, not exhausted.
- The 2.0x CPU ratio (T1-T5) was not re-measured (L1 receipts exist).
- H1/H2/H4/H5 receipts accepted from L1; only 3.10 compile re-checked here.
