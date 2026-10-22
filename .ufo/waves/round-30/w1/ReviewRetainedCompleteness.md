# ReviewRetainedCompleteness — round-30 fetch receipts and retention vs round-29 conventions

Axes: freshness (receipt integrity, determinism, host discipline). No installs performed; no live requests made; read-only in the lane.

## What I attacked

Compared the two fetchers, then byte-verified the round-30 retained artifacts
(`.ufo/waves/round-30/sources/`: S049–S052 .html.gz, .txt, receipts.json) against their own
receipts and against round-29 conventions.

## Commands and exit codes

1. `diff -u .ufo/waves/round-29/fetch_sources.py .ufo/waves/round-30/fetch_sources.py` → exit 1
   (differs, as expected). Four hunks, nothing elided after artifact review:
   - Docstring: round refs and paths `.ufo/waves/round-29/` → `.ufo/waves/round-30/`;
     added sentence "Each receipt also names the sha256 of this fetcher file (fetcherSha256)."
   - `SOURCES`: S040–S043 (docs.github.com, jekyllrb.com ×2, vite.dev) → S049–S052 (render.com
     docs ×4). Source ids continue the round-29 numbering without gaps.
   - `UA`: `kake-shokunin-round-29-source-opening (one GET per page)` → round-30 equivalent.
   - Receipt dict gains one line: `"fetcherSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()`.
   Everything else is byte-identical: `visible_text`, fetch loop, `gzip.compress(body, mtime=0)`
   (r30 line 60 / r29 line 59), receipt schema, `json.dumps(..., indent=1, sort_keys=True)+"\n"`,
   `timeout=60`, `--only` filter.
2. Read-only Python verification over the sources dir → exit 0. For each of S049–S052:
   - gzip header: MTIME field = 0, FLG = 0, OS = 255.
   - `gzip.decompress` → recomputed sha256 equals receipt `bodySha256`; `len(body)` equals
     `bodyBytes` (320167 / 348130 / 280291 / 371923).
   - `.txt` sha256 equals receipt `textSha256`; word count equals `textWords`
     (983 / 854 / 539 / 1488).
   - `gzip.compress(body, mtime=0)` reproduces the stored .gz byte-for-byte (all four True).
   - Receipt `fetcherSha256` equals sha256 of the on-disk fetcher:
     `b9431a5f349c7b857e2139fd148b8f75a2ddb8a4d94a3ea7013709a28a9190b4` (all four match — the
     receipts were produced by the file as it exists now, no post-run drift).
   - Receipts contain exactly S049, S050, S051, S052 — no stale ids; statuses all 200.
3. Same header check over round-29 S040–S043 .gz → exit 0: MTIME 0, FLG 0, OS 255 on all four
   (convention continuity).
4. Grep pinning: r30 `SOURCES` lines 26–29 (only URLs in the file), UA line 31, `Request(...,
   headers={"User-Agent": UA})` line 54, single `urlopen` line 55, `mtime=0` line 60,
   `fetcherSha256` line 63.

## Findings

- No convention break. The round-30 fetcher is a faithful re-instantiation of the round-29 one
  with the four expected edits (round refs, source list, UA round number, plus one additive
  receipt field).
- `fetcherSha256` is an additive schema extension vs round-29 (r29 receipts have 9 fields,
  r30 have 10). It is documented in the fetcher docstring (line 9) and verified to match the
  on-disk fetcher hash. Advisory only: any tooling that diffs receipt fieldsets across rounds
  will see the new key.
- gzip determinism holds: MTIME=0 in every retained .gz (both rounds), no filename flag,
  OS=255; byte-identical recompression on this host for all four round-30 bodies.
- Host discipline holds: the script's only URLs are the four render.com docs pages
  (r30 lines 26–29); `urlopen` is called once per SOURCES entry; `finalUrl == url` in all four
  receipts (no redirect to another host was followed). `--only` can only filter, never add URLs.
- UA string is exactly `kake-shokunin-round-30-source-opening (one GET per page)` (line 31),
  same pattern as round-29 with the round bumped.
- Timestamps: accessedUtc 2026-10-22T11:49:44Z (S049, S050) and 2026-10-22T11:49:45Z
  (S051, S052) — matches the declared "one GET each at 2026-10-22T11:49Z"; one timestamp per
  source, sequential, consistent with a single pass.

## Residual risk and verification gaps

- I did not re-run the fetcher (would re-GET render.com; unnecessary). Receipt authenticity
  rests on internal consistency (hashes, byte counts, fetcher hash, 200 statuses) plus file
  mtimes ~13 min before my check, consistent with the 11:49Z receipts.
- Byte-identical recompression was verified with this host's Python/zlib only; the portable
  guarantee is the MTIME=0 header field itself, which is present.
- "No other host contacted" is a source-plus-receipt conclusion (fixed SOURCES dict, single
  urlopen, no cross-host finalUrl); I cannot observe the network after the fact.
