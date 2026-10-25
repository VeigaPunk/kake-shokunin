# ExecSourceDigest — retained-body digest re-derivation (round 51, wave 1)

Seat: `L1Kake51.ExecSourceDigest-2` (executor, leaf). Scope: recompute sha256 over the two retained
bodies, compare with `sources/receipts.json`, report byte size, digest match and receipt URL, flag
mismatches. Read-only otherwise; this file is the only write.

## Axes (freshness)

1. **Digest integrity** — recomputed sha256 equals the receipt's `sha256`.
2. **Byte accounting** — filesystem size equals the receipt's `bytes` / `declaredBytes`.
3. **URL identity** — the receipt URL is the document the body actually is (canonical link, title,
   live status).
4. **Content identity** — the body is the page the entries claim (heading, gate quote present).
5. **Committed-bytes equivalence** — the bytes C2 reads via `git show <rev>:<path>` equal the bytes
   on disk (a working-tree-only edit would pass a disk digest while the counter reads the commit).
6. **Corroboration** — independent evidence that the recorded "doc rev" is not invented.

## Result — both bodies match, no defect

| id | body | bytes on disk | receipt `bytes` | receipt `declaredBytes` | recomputed sha256 | receipt sha256 | match | receipt URL |
|----|------|---------------|-----------------|--------------------------|-------------------|----------------|-------|-------------|
| S262 | `sources/S262.html` | 174926 | 174926 | 174926 | `792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b` | same | **yes** | `https://developers.google.com/search/docs/crawling-indexing/canonicalization` |
| S263 | `sources/S263.html` | 175561 | 175561 | 175561 | `6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de` | same | **yes** | `https://developers.google.com/search/docs/crawling-indexing/googlebot` |

Bodies are distinct (`b262 == b263` → False): the two receipts are not one body counted twice.
Receipt URLs are distinct and neither body is a copy of the other's document (titles differ:
"URL Canonicalization" vs "Googlebot").

## Evidence actually produced

Commands run (working tree at `/home/vgpnk/Projects/shokunin/kake-shokunin`, HEAD
`9d13768c4fdd0e9a2688d2ecf1616b539cf57658`):

- `sha256sum sources/S262.html sources/S263.html` →
  `792224…d23b  sources/S262.html` / `6afbdc…55de  sources/S263.html`;
  `stat -c '%n %s'` → 174926 / 175561.
- `git show 9d13768c4fdd:.ufo/waves/round-51/sources/S262.html | sha256sum` → `792224…d23b`;
  same for S263 → `6afbdc…55de`. **Committed bytes hash identically to disk bytes.**
- `git hash-object` on the three working files → `8669b013…`, `606eb71e…`, `63bd4ac5…`, equal to the
  blob ids at revisions `19a99bd8c30d`, `55915579563a`, `9d13768c4fdd` (receipt blob `63bd4ac5…`
  at all three). No drift in receipt or bodies across the round's three commits.
- Python check against `receipts.json`: `S262 disk_bytes 174926 receipt_bytes 174926 declared
  174926 bytes_eq_declared True digest_match True`; `S263 … 175561 … True … True`; receipt has
  exactly the keys `['S262','S263']`, URLs distinct.
- Content identity: `S262.html` `<link rel="canonical" href="…/canonicalization">`, title
  "What is URL Canonicalization", "Last updated 2026-08-20 UTC"; gate quote
  `indicating a canonical preference is a hint, not a rule` occurs once in the body.
  `S263.html` canonical `…/googlebot`, title "What Is Googlebot", "Last updated 2026-02-03 UTC";
  gate quote `Googlebot is the generic name for two types of` occurs once in the body.
- Both bodies end cleanly `…</body>\n</html>` with no trailing newline (curl-identity, not a
  re-serialized or truncated file). Both decode as UTF-8 (C2's C5 condition depends on this).
- Base revision `007d66e4e836` does **not** carry `sources/S262.html` (`git cat-file` → "exists on
  disk, but not in '007d66e4e836'"), so the retained bodies are new in round 51, as claimed.
- Live corroboration of `docRevision` (HEAD requests only, no body re-fetch):
  `canonicalization` → `http=200`, `last-modified: Thu, 20 Aug 2026 15:04:18 GMT`;
  `googlebot` → `http=200`, `last-modified: Tue, 03 Feb 2026 18:38:05 GMT`. These match the
  receipts' `docRevision` ("Last updated 2026-08-20 UTC" / "2026-02-03 UTC") and the in-body
  "Last updated" lines — the recorded revision is not invented.

## Defects

**None.** No digest mismatch, no byte mismatch, no URL/body mismatch, no commit-vs-disk divergence.

## Advisories (not defects against any frozen predicate)

1. **`bytes` and `declaredBytes` are the same number recorded twice** (174926/174926,
   175561/175561). The receipt's own fetcher line says the transfer size came from
   `%{size_download}`, and `bytes` presumably from `stat`; because the two fields are equal, the
   receipt cannot distinguish a transfer measurement from a filesystem measurement — the only
   independent byte witness is the on-disk length, which does agree. Harmless for C2 (which checks
   the digest, not the byte field), but the byte pair carries no extra information.
2. **S263's lesson section label is a de-tagged reflow, not a raw substring.** The lesson records
   § "Googlebot is the generic name for two types of web crawlers used by Google Search"; the body
   has an anchor between "of" and "web crawlers"
   (`…for two types of\n  <a href="/search/docs/fundamentals/how-search-works">web crawlers</a> used…`),
   so a literal `grep -F` for that § string in `S263.html` returns 0 hits. The Gate quote itself
   (`Googlebot is the generic name for two types of`) *is* a raw substring, and C5 only constrains
   the Gate quote, so C2 is unaffected. Readers grepping the § label verbatim will be misled.
3. Byte-count claims in `corpus/lessons/round-51.md` (174926 / 175561, HTTP 200, same sha256s) agree
   with the receipts and with the disk; no drift there either.

## Bounds / honesty

- No lane, fleet or jj/Git state mutated; no `git add/commit/stash/checkout/reset/pull/push`,
  no mutating `jj`. Only read-only `git log/show/rev-parse/hash-object/cat-file/merge-base` and the
  read-only `HEAD` requests above.
- Body bytes were **not** re-downloaded for comparison (HEAD only, `size_download=0`); the live
  claim is limited to status 200 plus `last-modified`, which is what I actually observed.
- No tools installed or upgraded in this seat, so there is nothing to record under the tooling
  directive.
