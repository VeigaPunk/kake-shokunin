# ExecIndependentBuild — independent `_parse_url` repair (r41 wave 1, operability)

Tool: `/fast/scratch/hyaku/kake-r41w1/ExecIndependentBuild/indep.py`
sha256 `a5b5c93ed6f19402fb6d966917532b74f844b3661eeab152acacf357934ea890`
Built from `/fast/scratch/hyaku/kake-r41/shared/base.py` (sha256 `4de35f8c…55a1460e`); `ref_fix.py` and `ref_fix.diff` were never opened.
Grammar source: `https://www.rfc-editor.org/rfc/rfc3986.txt` (sha256 `3102dae4…02b2d683`), Appendix A (lines 2695-2800), plus contract `.ufo/waves/round-39/c1-contract.md` sentences 4, 22 and 24-26.

## Change — 2 import lines and one function (`indep.diff`: 3 hunks, 163 lines)
- `indep.py:15` adds `import ipaddress`; the `from urllib.parse import urlsplit` line is removed.
- `indep.py:123-183` `_parse_url` decides the Appendix A `URI` instead of trusting a splitter: first `#` ends the fragment, first `?` in what remains ends the query, `scheme ":"` must match `ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )`, the hier-part must be `"//" authority path-abempty`, and the authority is `[ userinfo "@" ] host [ ":" port ]` (split at the first `@` and first `:`; a second `@`, or a non-digit port, rejects).
- `indep.py:80-104` character classes: userinfo `unreserved/sub-delims/":"`, reg-name `unreserved/sub-delims`, path `pchar + "/"`, query and fragment `pchar + "/" + "?"`, each position a member character or a `%HH` triplet — a `%` not followed by two hex digits rejects. `port = *DIGIT`: empty port is legal and takes the sentence-24 default (80/443), and there is no 65535 cap.
- `indep.py:108-120` `host = IP-literal / reg-name`: `[...]` must be IPvFuture (`v`/`V` — ABNF string literals are case-insensitive) or a real IPv6 (`ipaddress.IPv6Address`; `%` rejected because zone ids are RFC 6874). IPv4address is a subset of reg-name, so a separate branch would add nothing.
- `indep.py:83-91`: where `unreserved` stands, non-ASCII is accepted exactly as RFC 3987 `ucschar` (the task's IRI instruction), so C1 controls, surrogates and private-use code points are rejected rather than waved through.
- Callers unchanged: `indep.py:380-393` `_audit_loc` and `indep.py:458` consume the same `(scheme, host, port, path)` tuple, so sentences 21 and 23-27 (`loc_too_long`, scheme/host/port scope, literal path prefix) behave as before.

## Counter receipts (counter `.ufo/waves/round-41/c1_count.py`, sha256 `2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4`)
Command: `timeout 900 python3 -B …/c1_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file <tool> --label <label> --seed <seed> --out <file>.json`

| seed | tool | passed | byField loc / sitemapUrl | met | exit |
|---|---|---|---|---|---|
| 41 | indep.py | 1434/1434 | 630/630 · 804/804 | true | 0 |
| 42 | indep.py | 1434/1434 | 630/630 · 804/804 | true | 0 |
| 43 | indep.py | 1434/1434 | 630/630 · 804/804 | true | 0 |
| 41001 | indep.py | 1434/1434 | 630/630 · 804/804 | true | 0 |
| 41001 | base.py | 1049/1434 | 509/630 · 540/804 | false | 1 |
| 41 | base.py | 1045/1434 | 508/630 · 537/804 | false | 1 |

byComponent is 239/239 on every component (fragment, host, path, port, query, userinfo) for all four indep.py runs; for base.py at seed 41001: fragment 157/239, host 165/239, path 166/239, port 239/239, query 153/239, userinfo 169/239. `toolExit` 2 in every met receipt is the tool's verdict for the error checks the counter plants; the judge reads the JSON (`c1_count.py:252-267`), so exit 2 is expected, not a signal.

Selftest: `cd /home/vgpnk/Projects/shokunin/kake-shokunin && timeout 900 python3 -B scripts/sitemap_audit_selftest.py --tool /fast/scratch/hyaku/kake-r41w1/ExecIndependentBuild/indep.py` → exit 0, `PASS 183/183`.

## Oracle differential (`diff_oracle.py`, exit 0) — 31,528 values, 2 mismatches
56 hand-built RFC edges + the counter's own generator over seeds 1-8 (11,472 values) + 20,000 random fuzz strings. Both mismatches are the instructed IRI reading, i.e. ours accepts and the RFC 3986 oracle rejects:
- `http://h/é?é#é` (non-ASCII in path/query/fragment)
- `http://é.com/x` (non-ASCII in host)
Everything else agrees, including: empty port `http://example.com:/x` and `http://h:80`, ports above 65535, `%00`/`%4a`/`%4A`, `?` inside a query and inside a fragment, IPvFuture `[V1.ab]`, IPv4-mapped IPv6, `[fe80::1%25eth0]` (rejected), `999.0.2.1` (valid reg-name, not IPv4), empty/lone `%`, `[`/`]`/`\`/`^`/`` ` ``/`{}`/`|`, space, tabs, controls, and `#`/`?` as authority and port terminators.

## Findings — statements checked
- Sentence 22/4 as an implementable target: **holds**. Written from the RFC and the contract alone, the repair reaches 1434/1434 on 4 seeds, so the predicate is reachable without the L1's reference.
- "The base tool scores 1049": **holds at its stated seed 41001** (reproduced exactly: 1049, loc 509/630, sitemapUrl 540/804) but is **seed-dependent** — 1045 at seed 41 — so any reading of 1049 as a property of the base rather than of the seed is overstated.
- "A correct repair scores 1434": **holds** (four seeds, plus selftest 183/183).
- Counter discriminates the claimed work rather than one trick: base loses 385-389 cases spread over 5 of 6 components (port only 0-1), so a repair that handles only ports, only `%`, or only brackets cannot pass; `holds`.
- Case split 630 `loc` / 804 `sitemapUrl` per run: `holds` (receipts).
- New behaviour worth naming: `urlsplit` used to reject `http://h:99999/x` (`Port out of range`) and accept `http://h/x^y`; the repair inverts both, which is what Appendix A requires (`port = *DIGIT`, `^` in no class). `indep.py:167-183`.
- Deviation from the oracle's label: exactly the two non-ASCII values above; no ASCII value in 31,528 differed. If the round wants a byte-identical RFC 3986 reading instead of an IRI one, `_IRI` (`indep.py:83-91`) is the only line to change and the counter score is unaffected (it generates ASCII only).

## Risks
- Non-ASCII host/reg-name acceptance (IRI) contradicts the oracle's RFC 3986 label; unguarded by the counter, so the claim's wording should say "IRI-permissive in `unreserved` positions".
- `int(port_text)` on an arbitrarily long digit run is bounded by input length; no cap means a `sitemapUrl` port such as `999999999999` compares unequal to any default port — grammar-correct, but a real-world loc will then be `loc_out_of_scope` rather than `check_invalid`.
- Percent-decoding and dot-segments stay untouched (sentence 26); the repair changes judgment only, not scope semantics.
- Freshness axis: nothing in this item touches corpus dates; no network read except `rfc-editor.org` for the RFC text.
- No tool installs or upgrades were needed (python3 3.14 host stdlib only), so no install record.

Sandbox artifacts: `indep.py`, `indep.diff`, `diff_oracle.py`, `extra_probe.py`, `rfc3986.txt`, `s41.json`, `s42.json`, `s43.json`, `s41001.json`, `base41.json`, `base41001.json`, `selftest2.out`, `diff2.out`, `extra2.out` under `/fast/scratch/hyaku/kake-r41w1/ExecIndependentBuild/`.
