# Falsify S009 — round-26 C1 freshness recheck (receipt HOLD)

Seat: `KakeR26-2.FalsifyS009` (leaf member, no dispatch). Milestone `r26-recheck-falsify`. Axis: **freshness**.
Target: `.ufo/waves/round-26/rechecks/S009.json` (verdict HOLD) + SOURCES row S009 (`corpus/SOURCES.md:17`).
Goal: try to show the receipt is WRONG — quote not grounding the row's teaches, anchor mislocated, content/version change missed.

**Verdict: AGREE** — the receipt's HOLD survives every falsification I ran. Severity: **low** (three low defects attached; none changes a verdict or a count).

## 1. What is under attack

`corpus/SOURCES.md:17` (byte-identical base `97404de` → candidate `e28312b`):

```
| S009 | nginx source release-1.28.0, src/http/ngx_http_core_module.c — https://raw.githubusercontent.com/nginx/nginx/release-1.28.0/src/http/ngx_http_core_module.c | code | A | nginx's own ETag format only; not an assertion about the GitHub Pages backend | ngx_http_set_etag at line 1682, ETag sprintf lines 1708-1710; tag release-1.28.0, commit 481d28cb4e04c8096b9b6134856891dc52ecc68f | nginx formats its ETag from hexadecimal last-modified time and hexadecimal content length; this says nothing about which server GitHub Pages runs | mined | 2026-10-19 | 365d | corpus/knowledge/ghp-etag-anatomy.md |
```

Receipt (`.ufo/waves/round-26/rechecks/S009.json:1-9`, sha256 `ae59606056bd9ea696a6e45dbaf7b7b7aefcd6167e221389581d7e8bcb6bf854`, byte-identical in the worktree and at candidate `e28312b`):

```json
{"id":"S009","verdict":"HOLD","fetchIndex":1,
 "quote":"etag->value.len = ngx_sprintf(etag->value.data, \"\\\"%xT-%xO\\\"\", r->headers_out.last_modified_time, r->headers_out.content_length_n) - etag->value.data;",
 "anchorObserved":"src/http/ngx_http_core_module.c:1708-1710 inside ngx_http_set_etag (function definition at line 1682); line numbers derived from decompressed raw bytes because fetched/text/S009-1.txt is newline-flattened",
 "reason":"The tag-pinned URL still resolves (200) and the re-fetched bytes place ngx_http_set_etag at 1682 and the ETag sprintf with last_modified_time and content_length_n at 1708-1710; the hex-time/hex-length format and the nginx-only scope still hold.",
 "correction":null}
```

## 2. Attack 1 — Does the quote ground THIS row's teaches? → NO DEFECT

- The quote is the whitespace-joined form of the real source statement. Decompressed retained bytes `fetched/S009-1.raw.gz` (147,410 B, sha256 `c58ebede93aa6c790858ce7e14e01f80f3480466ceb9f7d784c1051321cec3fe`, equal to `fetched/manifest.json:202`):

```
1708  '    etag->value.len = ngx_sprintf(etag->value.data, "\\"%xT-%xO\\"",'
1709  '                                  r->headers_out.last_modified_time,'
1710  '                                  r->headers_out.content_length_n)'
1711  '                      - etag->value.data;'
```

- Membership checks (my own, in-memory): receipt quote is a word-bounded substring of the effective text view `fetched/text/S009-1.txt` (`count 1`); the same quote is **not** a literal substring of the raw bytes (it spans 4 source lines) but **is** exactly the whitespace-joined span of raw 1708–1711 (`joined(1708..1711) == quote` → True; `joined(1708..1710) == quote` → False). The receipt itself discloses this mechanism (`anchorObserved`: "line numbers derived from decompressed raw bytes because fetched/text/S009-1.txt is newline-flattened").
- **Row specificity** (the counter's `quote_not_row_specific` rule): I normalized the quote and scanned all 34 committed text views `fetched/text/*.txt`; the S009 quote occurs in **no other row's** text, and no other receipt duplicates it. No boilerplate.
- **Semantic grounding**: the quoted statement is precisely the row's teach — the ETag value is `ngx_sprintf` of `r->headers_out.last_modified_time` and `r->headers_out.content_length_n` with the format `"\"%xT-%xO\""`. The file contains exactly one `%xT-%xO` (`grep -cF '%xT-%xO'` → 1), so the quote is the file's only ETag-format site, not a neighbouring clause. `etag->key` is set to `"ETag"` at line 1700, and the buffer is sized `NGX_OFF_T_LEN + NGX_TIME_T_LEN + 3` at 1702 — consistent with a hex time + hex length.
- **Scope cell** ("not an assertion about the GitHub Pages backend"): the file contains no `GitHub`, `github`, `Jekyll`, `jekyll` tokens (0 occurrences each); the 16 `pages` hits are nginx-internal identifiers (`error_pages`, `recursive_error_pages`, `ngx_pagesize`). The scope disclaimer is honest.
- The "hexadecimal" wording is additionally corroborated outside this file by the lane's own arithmetic, which I re-verified: `0x6ab49127` = 1790218535 = `2026-09-24T02:55:35Z` (the recorded `Last-Modified` second) and `0x1365d` = 79453 (the recorded body size, `LOG.md:161-163`).

## 3. Attack 2 — Is the anchor observed correct in the raw bytes? → NO DEFECT (one low defect on the receipt's own range label)

- Raw line **1682** is exactly `ngx_http_set_etag(ngx_http_request_t *r)` (the function name line; `ngx_int_t` on 1681, `{` on 1683). The receipt's "function definition at line 1682" and the row's "ngx_http_set_etag at line 1682" both point at the right line.
- Raw **1708** is the `ngx_sprintf` with `"\"%xT-%xO\""`; `last_modified_time` on 1709, `content_length_n` on 1710. The receipt's "ETag sprintf … at 1708-1710" is exact for the call site.
- **Defect 1 (low) — the receipt's quote is one line wider than the range the receipt itself declares.** The quote's final fragment `- etag->value.data;` lives on raw line **1711**, outside the `1708-1710` range in both the receipt's `anchorObserved` and its `reason`. A reader who extracts raw 1708–1710 gets the `ngx_sprintf(...)` call *without* the trailing `- etag->value.data;` and cannot match the receipt's quote byte-for-byte. Compounding it, `w1/PairS009GhpEtagAnatomy.md:26` (R7) prints that same wider quote and asserts "release-1.28.0 raw 1708-1710, tail 1711. **Excerpt equals raw 1708-1710 with whitespace joined (checked)**" — that equality is false for the quote it displays (it equals 1708–1711 joined); only the corpus's own narrower excerpt (`corpus/knowledge/ghp-etag-anatomy.md:23`) is a true contiguous substring of joined 1708–1710. Minimal correction (append-only; receipts are committed evidence and are not to be rewritten): append one line to the S009 tail recording that the receipt quote spans raw 1708–1711 (sprintf call 1708–1710, assignment tail 1711), or narrow the receipt quote to the 1708–1710 call. Either way the teaches, the anchor symbol, and every count are unaffected.

## 4. Attack 3 — Did content/version change in a way the receipt missed? → NO DEFECT

- One plain public GET of the recorded row URL (in memory, nothing saved), 2026-10-21 16:56:38 GMT:

```
HTTP/2 200
etag: "d44bccb92e9b627564744648c542c7931a62ba340d900f3bd8b1f859c152adbc"
content-length: 147410
content-type: text/plain; charset=utf-8
bytes 147410  sha256 c58ebede93aa6c790858ce7e14e01f80f3480466ceb9f7d784c1051321cec3fe
```

  Byte-identical to the retained `fetched/S009-1.raw.gz` and to `fetched/manifest.json:187-204` (`bytes 147410`, same sha256, same `etag` header). The pinned tag's content has not changed; the receipt's "tag-pinned URL still resolves (200)" holds today, and the live body still places `ngx_http_set_etag` at 1682 and the only `%xT-%xO` at 1708.
- The URL is an immutable release tag, so a "version drift" for this row is not applicable; the row's own `recheck` cell (365d) and `status` (mined) are untouched by the candidate (row byte-identical base→candidate).
- **Defect 2 (low) — the row's commit pin is not attested by any retained artifact this round, and the two wave-1 reports disagree about whether it was re-queried.** The row's anchor cell asserts "tag release-1.28.0, commit 481d28cb4e04c8096b9b6134856891dc52ecc68f". `w1/RowS009.md:13` (caveat 3) states the opposite of `w1/PairS009GhpEtagAnatomy.md:58`, which asserts "Tag check: `release-1.28.0` (annotated tag object f6f8d515885fcda20f09b83583d576337fbabe0a) resolves to commit 481d28cb…, matching the pinned commit" (its §5 disclosure lists an `api.github.com` tag-ref GET). No such read is retained: `grep -c "api.github.com" fetched/manifest.json` → **0**, and the manifest holds exactly one nginx URL (release-1.28.0). The receipt S009 itself makes no commit claim, so HOLD is not falsified — but the anchor cell's commit half is unverifiable from the wave's retained evidence. Minimal correction: state in the S009 tail that the commit pin is carried from `corpus/lessons/round-20.md:211` and was not re-queried this round (or retain the tag-ref read). No count impact.
- **Defect 3 (low) — the committed counter at the candidate does not surface the per-row decision.** Running the committed `measure.py` at `e28312b` yields `exit 0, decided 32, hold 32, findings []` but prints `"rows": []` — the committed `score()` builds the per-row list and never assigns it to `output["rows"]` (candidate `measure.py:513-519`; the worktree copy at `:557` does assign it, and the candidate's own committed artifact `.ufo/waves/round-26/verification/measure-candidate.json` shows the same `"rows": []`). Consequence for S009 specifically: the committed counter output cannot show *S009's* row record, so "S009 decided HOLD" is visible only from the receipt file itself, not from the counter's published table. I re-ran the counter at `e28312b` and confirmed the S009 record in the worktree copy: `{'decided': True, 'findings': [], 'id': 'S009', 'verdict': 'HOLD'}`. This is the survivor already logged in the worktree lesson (`corpus/lessons/round-26.md` §Falsify wave and resume → Mistakes → "survivor | `rows` was never assigned in `score()`; the candidate printed `rows: []` with 32 decided (w2/FalsifyS015)"), so it is a known, already-handled defect — recorded here only because it is the audit path for this row's HOLD.

## 5. Counter / append-only consistency (read-only, no mutation)

- Committed counter, candidate `e28312b`: `exit 0`, `decided 32/32`, `hold 32`, `stale 0`, `unverifiable 0`, `findings []`, `statements 276`, `statementsStale 8`, `statementCorrections 8`. Committed counter, base `97404de`: `exit 1`, `decided 0`, finding `receipts_absent`. The round's before/after claim is reproduced.
- Receipt schema for S009 is exactly the seven required keys; `correction: null` is required for HOLD and present; quote is 25 tokens / 8 words (limits: ≥6 tokens, ≤25 words); `fetchIndex 1` matches `population.json`'s single S009 fetch; the quote is word-bounded in the effective text view.
- `corpus/SOURCES.md`: every base line survives byte-identically and in order in the candidate; the only insertion is the "Round 26 bounded recheck" paragraph, placed in the same log region as the Round 22–25 paragraphs, ahead of `## Leads (unopened)` — the file's established convention, and a pure new-line addition per the round-20 append-only ruling.
- `corpus/knowledge/ghp-etag-anatomy.md`: the base blob is an exact byte-prefix of the candidate blob (base lacked a final newline; the candidate adds one plus the appended round-26 block). The S009 row is byte-identical base→candidate; the S009 row's cells were not edited, and no `[r26-recheck S009 STALE]` tag exists or is required (S009 `stale: 0` in `statements.json`).

## 6. Residual risk / verification gaps

1. The receipt's own quote/anchor range mismatch (defect 1) is the only precision defect in the artifact under review; it is a labelling issue, not a factual error about the source.
2. The commit pin (defect 2) is the one assertion in the row's anchor cell that this round's retained bytes do not support; content stability of the tag is independently confirmed, so no statement in the corpus depends on it being re-proven.
3. The `hex` reading of `%xT`/`%xO` is nginx-printf semantics defined in `src/core/ngx_string.c`, not in the fetched file; `w1/RowS009.md:14` (caveat 4) discloses this, and the lane's own ETag arithmetic corroborates it. A future recheck that cites only this file for the word "hexadecimal" would be over-reaching.
4. The receipt cannot be re-verified without the retained gzip (the raw file has no trailing newline and the quote is multi-line); anyone re-deriving the anchor must re-decompress `fetched/S009-1.raw.gz` rather than grep the text view.
5. Out of scope for this seat (other lanes' territory, and main reports corpus ledger disagreements are already integrated): the counter's `rows` population at the candidate (defect 3) and the corpus-tail provenance of the 1.30/1.31 line observation, which rests on seat prose plus 8-hex digests rather than retained bytes (no `1.28.3`/`1.30.6`/`1.31.8` URL exists in `fetched/manifest.json`).

## 7. Reproduction (read-only; the live body was never written to disk)

```
gzip -dc .ufo/waves/round-26/fetched/S009-1.raw.gz | grep -n 'ngx_http_set_etag\|%xT-%xO'      # 1682, 1708
gzip -dc .ufo/waves/round-26/fetched/S009-1.raw.gz | sed -n '1708,1711p'                       # the quoted statement
gzip -dc .ufo/waves/round-26/fetched/S009-1.raw.gz | grep -cF '%xT-%xO'                          # 1
python3 -B .ufo/waves/round-26/measure.py --root . --revision e28312b14b076584fedd696fae2a684e460bd11e   # exit 0, 32 decided
python3 -B .ufo/waves/round-26/measure.py --root . --revision 97404de4ff73d6c8a4f87385cf5fdf36dca7f006   # exit 1, receipts_absent
curl -sS -D- https://raw.githubusercontent.com/nginx/nginx/release-1.28.0/src/http/ngx_http_core_module.c | sha256sum   # c58ebede…
```

## 8. Tooling / disclosures

- No installs or upgrades; no pacman transaction (host-wide pause respected). Python 3.14 stdlib only (`gzip`, `hashlib`, `json`, `urllib`, `re`, `difflib`); `git`, `sed`, `grep`, `sha256sum` were already present.
- Network: exactly one plain public GET of the recorded row URL (`raw.githubusercontent.com`), response kept in memory only, never written to disk. No other host was contacted; no website/property probing, browser, account, credential, publication or security testing; no round-24 material was read, retried, rephrased or rerouted.
- Files written: this report only. No corpus, script, fleet, sibling-lane, lane Git index or jj state was mutated. (The wave's own uncommitted worktree edits — `measure.py`, `statements.json`, corpus tails — were pre-existing and were left untouched; `git status` shows the same modified/untracked set before and after this seat.)
- Python bytecode caches were written by the interpreter under `.ufo/waves/round-26/__pycache__/` and `before/__pycache__/` (untracked, pre-existing directories; regenerated by `python3 -B` runs of the wave's own modules).

```json
{"target":".ufo/waves/round-26/rechecks/S009.json","verdict":"AGREE","severity":"low"}
```
