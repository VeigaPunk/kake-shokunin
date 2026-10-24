# ScoutWhatwgUrl — R38 w1: WHATWG URL preprocessing vs `urlsplit` vs rule (i)

Item: open `https://url.spec.whatwg.org/` and Python 3.15.1 `urllib.parse`; quote the strip/remove steps; contrast with amendment (i); registry decision per page. Fetched 2026-10-23 04:30:17Z–04:31:49Z. No install or upgrade; sealed trees untouched; no round-38 counter or key touched.

**Freshness.** WHATWG `https://url.spec.whatwg.org/`: HTTP 200 (curl exit 0), 703601 bytes, sha256 `08cb42a9a8575dab006676378c846fdd8a72d06897c27929aa51eaf099656be4`, `Last-Modified Mon, 19 Oct 2026 11:58:10 GMT`, etag `6ad605d2-abc71`; Living Standard, no build date in text. Python `https://docs.python.org/3/library/urllib.parse.html`: HTTP 200, 119730 bytes, sha256 `10fe85136e5ad7bdc5be46ed3ff0f286e4a61e73e41910ac47d951b6a42d6349`, `Last-Modified Fri, 23 Oct 2026 01:40:01 GMT`, title "Python 3.15.1 documentation" (unversioned `/3/` page). Header re-check 04:31:49Z: same etag and length.

## Quotes (step names as numbered)
Basic URL parser §4.4, ordered steps 2–5 (ordinals counted as `<li>` from `id="url-parsing"`; the six-step window reads *"If url is not given…"*, error, remove, error, remove, *"Let state be…"*):
- step 2 "If input contains any leading or trailing C0 control or space, invalid-URL-unit validation error." (16 w)
- step 3 "Remove any leading and trailing C0 control or space from input." (11 w)
- step 4 "If input contains any ASCII tab or newline, invalid-URL-unit validation error." (13 w)
- step 5 "Remove all ASCII tab or newline from input." (8 w)
- §1.1 "A validation error does not mean that the parser terminates." (10 w)
- §4.4 path state "If c is not a URL code point and not U+0025 (%), invalid-URL-unit validation error." (17 w) then "UTF-8 percent-encode c using the path percent-encode set and append the result to buffer." (15 w)
- §1.3 path set = query set + `? ^ ` ` { }`; query set = C0 set + space `"` `#` `<` `>`. `C0 control or space` and `ASCII tab or newline` are **not defined here** — the index lists both under `[INFRA] defines the following terms`; U+0000–U+001F / U+0020 is the Infra reading, by reference.
Python 3.15.1 `urlsplit` ("Following some of the WHATWG spec that updates RFC 3986…"):
- "leading C0 control and space characters are stripped from the URL" (11 w)
- "\n, \r and tab \t characters are removed from the URL at any position" (14 w)
- Warning "urlsplit() does not perform validation." (5 w); changelog 3.10 (newline/tab stripped), 3.12 (leading WHATWG C0/space stripped).
RFC 9309 (S011 retained text, not re-fetched): "The /robots.txt URI is implicitly allowed."; `path-pattern = "/" *UTF8-char-noctl`; "Octets … outside the range of the ASCII coded character set … MUST be percent-encoded … prior to comparison" (elisions marked, ≈20 w).

## Measured (sandbox only)
- Node v24.21.0 `new URL`, 14 inputs, exit 0: leading/trailing space and trailing NUL stripped; `\t`, `\n`, `\r\n` removed (`x\ty` → `/xy`); `"`→`%22`, `<`→`%3C`, `>`→`%3E`, `^`→`%5E`, `` ` ``→`%60`, `{`→`%7B`, `}`→`%7D`, space→`%20`; `\`→`/`; `|` kept. Nothing rejected.
- Python 3.14.8 `urlsplit`, same 14, exit 0: strips leading C0/space only, removes `\t\n\r`, keeps trailing space/NUL and keeps `" < > \ ^ ` { } |` raw in `path` (sibling `ProbeUrlsplit.md`, 640 rows, agrees).
- Base tool `scripts/robots_audit.py` sha256 `944d2f51…d3e5` at `2dab7f31`, five manifests (trailing space, tab-mid, leading space, mid space, backslash): every one **`clean`, `checksEvaluated 1`, exit 0** — evaluated and allowed. Under (i) all five are `check_invalid` → `could-not-evaluate`, exit 2.

## Contrast verdict
Neither source rejects: both normalize first. WHATWG strips/removes at steps 3 and 5 and only emits a non-fatal validation error (§1.1); `urllib.parse` ≥3.12 copies those steps inside `urlsplit`; RFC 9309 mandates percent-encoding "prior to comparison", not refusal (only its *rule* grammar excludes controls).
(i) is therefore **stricter than all three sources and derived from none of them**. It remains a **defensible publisher-side lane reading** when stated as one: RFC 3986 §2 admits only (i)'s character set, so the tool cannot honestly predict which octets a crawler compares; the answer is fail-closed ("cannot say", never a wrong allow/disallow); the contract already fixes it ("judged as written, before any parsing").
Its measured cost is the class where the two implementations **agree**: for `http://a.example/rob\bots.txt` and ` http://a.example/robots.txt` both WHATWG and `urlsplit` yield `/robots.txt` (allow), while (i) answers `could-not-evaluate`. It is **not** defensible as "what browsers/crawlers do" nor as "RFC 3986 requires rejection" (it requires percent-encoding). Trailing space/NUL is the one class where the sources disagree with each other (WHATWG strips, `urlsplit` keeps), so (i) is most defensible there. **Hold (i) as declared** — key v3 is frozen; record in the lesson that (i) strictly supersedes WHATWG §4.4 steps 3/5 and `urlsplit` preprocessing, with the five-case delta as its cost.

## Registry decisions (candidate; L1 decides)
**`url.spec.whatwg.org` → ADMIT (contrast/counterexample) as S098.** `source` URL Standard — https://url.spec.whatwg.org/ · `kind` spec · `tier` A · `scope` "Basic URL parser input preprocessing and non-fatal validation errors, as contrast to strict input rejection" · `anchor` "§4.4 basic URL parser steps 2–5 and §1.1 Writing; Living Standard, HTTP 200 fetched 2026-10-23T04:30:17Z, sha256 08cb42a9…, Last-Modified 2026-10-19T11:58:10Z" · `teaches` "The parser strips leading/trailing C0 control or space, removes ASCII tab/newline anywhere, and reports non-fatal validation errors instead of failing" (20 w) · `status` `queued` · `opened` 2026-10-23 · `recheck` 90d · `used-by` — (flip to `mined` once the round-38 lesson or a knowledge entry cites it). No existing row covers this page (S023–S025, S030, S031, S090, S092 are HTML/Encoding).
**`docs.python.org/3/library/urllib.parse.html` → ADMIT (counterexample) as S099, overlap recorded.** Same URL as S027 ("URL splitting and resolution are not validation", on-release) but a disjoint claim (preprocessing), so S027 is neither superseded nor edited. `kind` docs · `tier` A · `scope` "urlsplit's WHATWG-derived preprocessing: leading C0 control and space stripped, tab/CR/LF removed anywhere" · `anchor` "urlsplit paragraph 'Following some of the WHATWG spec…' and Changed in version 3.10/3.12; Python 3.15.1 docs, HTTP 200 fetched 2026-10-23T04:30:18Z, sha256 10fe8513…" · `teaches` "urlsplit strips leading C0 controls and space and removes tab, CR and LF anywhere, and performs no other validation" (19 w) · `status` `queued` · `opened` 2026-10-23 · `recheck` on-release · `used-by` —. **Flip to REJECT** (duplicate page; cite S027) if the round-38 Gate does not itself cite this row.

## Not verified / limits
- Infra Standard not opened (`C0 control`, `space`, `ASCII tab or newline` by reference; exact Infra text is `[INFERENCE]`, its scope from the URL spec's index). Node `URL` treated as WHATWG-conformant from its documented API (`[INFERENCE]`); its 14 results match steps 2–5 and §1.3 sets — corroboration, not proof. No browser, crawler, or owned host contacted. (h) and (k) not assessed beyond the RFC 9309 sentence quoted.

## Evidence (sandbox paths + sha256)
- `…/kake-r38w1/ScoutWhatwgUrl/src/05997133.html` = WHATWG page `08cb42a9…656be4`; `…/src/7d6b3297.html` = Python docs `10fe8513…2d6349`; `…/src/t.js` (14-case node matrix) `85294a6f…5c91`.
- `…/ScoutWhatwgUrl/evidence.txt` — hashes, node + urlsplit matrices, base-tool verdicts, `6ec4897e8fb3c3cf252eb9dc8d100d325cb64684aedef610fb346fc15c34d8af` (40 lines).
- `…/ScoutWhatwgUrl/m/{trail-space,tab-mid,lead-space,mid-space,backslash}.json` + `robots.txt`; clone `…/ScoutWhatwgUrl/c2` at `2dab7f31`, tool sha256 `944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`.
