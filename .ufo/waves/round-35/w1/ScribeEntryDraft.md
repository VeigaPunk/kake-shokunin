Disclosure: one `test -e /fast/scratch/hyaku/kake-r35/sealed` (existence check on the directory path, exit 1 meaning it exists) ran in a verification command. No file under it was read, listed, copied, hashed, grepped or opened, and no key material was accessed; this seat did not use its contents.
Sealed keys: no read, list, copy or grep of anything under `/fast/scratch/hyaku/kake-r35/sealed/`.

# ScribeEntryDraft — C2 entry draft (round 35, wave 1)

Draft: `/fast/scratch/hyaku/kake-r35/w1/ScribeEntryDraft/security-txt-publishing.md`, 8849 bytes, sha256 `0b5ac7e83a622045a3c1a528e25c042ecb400b46309a09660ac0b500e6c0c397`.
Receipt: `/fast/scratch/hyaku/kake-r35/w1/ScribeEntryDraft/security-txt-publishing.receipt.json`. Folded source copies for reading sit beside them.
Sealed keys: nothing under `/fast/scratch/hyaku/kake-r35/sealed/` was read, listed, stat'ed or grepped.

## What I built

One entry, 1298 words, sections: where the file lives, how it is served, the fields, what the file covers, GitHub Pages branch build versus artifact build, the two live files, decisions before publishing.
Header follows the `link-preview-metadata.md` convention (source, verified-at, recheck, scope, ground, coverage, falsifier, counter) plus a coverage-map paragraph naming `ghp-served-set.md` and `publish-channels.md`.
Every factual sentence carries a source id; lane reasoning is marked `[INFERENCE]`; longest quoted span is 5 words.

Facts covered (source ids as carried in the draft):

- Well-known location and the top-of-path rule (S078, S082); IANA lists `security.txt` permanent, IETF, RFC 9116, registered 2021-07-13 (S083).
- Root copy as legacy fallback, both copies allowed, well-known copy must win (S078, S079); namespace reservation and write access (S078, S082).
- HTTPS, HTTP/1.0+, `text/plain`, default charset utf-8, UTF-8 Net-Unicode, ABNF, CRLF or LF, `#` comments, case-insensitive names, redirects (S078, S079).
- `Contact` mandatory, URI schemes, preference order; `Expires` mandatory and single, RFC 3339, under one year; `Preferred-Languages` single, comma list, equal weight, English default; `Canonical` trust rule; `Encryption` as a URI not a key (S078, S079).
- `Policy`, `Hiring`, `Acknowledgments`; OpenPGP cleartext signing with Canonical; IANA field registry, unknown fields ignored, `CSAF` extension (S078, S079).
- Scope limited to the fetching host, products, policy states scope, no implied testing permission, stale worse than absent (S078, S082).
- Branch build: `_`, `.`, `#` skipped by default, `include` overrides, Jekyll 4 include beats exclude (S006, S080); empty `.nojekyll` at the publishing source root disables the Jekyll build (S086).
- Artifact build: v4.0.0 drops hidden paths, v5.0.0 adds `include-hidden-files`, `.git`/`.github` excluded regardless, unset input ships no `/.well-known/`, entry file at artifact top level (S001, S002, S086).
- Live files: GitHub field set and `Expires: 2026-11-21T22:02:20z` (about a month out, inside the year); Google's two `Contact` lines (`https` first), `Encryption`, `Expires: 2030-04-01T00:00:00z` (about 3.5 years, past the recommendation), no `Canonical`/`Preferred-Languages`; GitHub has no `Encryption`; neither retained body opens with PGP armor (S084, S085, S078).

## Commands and observed results

- `fold -s -w 110 <source>.txt > <sandbox>/<id>.fold.txt` for S006, S078–S087 — exit 0; reading aid only.
- `wc -w security-txt-publishing.md` → `1298` (task bound 700–1300; counter bound 1500).
- Python replication of the counter's own `words`/`shingles` functions imported from `.ufo/waves/round-35/sealed_count.py`, draft against every retained `.txt` → `counterWords 1298, shingles 1381, sharedShingles 0, copiedShare 0.0, longestQuoteWords 5` — exit 0.
- `grep -c` for rows S078–S087 in `corpus/SOURCES.md` → exit 1, count `0`.
- Sealed counter not run: its key and probes are sealed and were not read.

## Gates

- Word bound: met (1298, under 1300 and under 1500).
- Copied share: met with margin (0.0 against all retained source text).
- Quote length: met (longest 5 words; no pasted passages).
- Cites: the draft cites S078–S086 plus S001/S002/S006, but the counter's `goodCites` condition is 0 of 3 because `corpus/SOURCES.md` at lane state `318561e` has no S078–S087 rows. The row seat must land them with status `mined`, opened `2026-10-22`, and `corpus/knowledge/security-txt-publishing.md` in the used-by cell, or C2 cannot pass whatever the draft says.
- Probes: not evaluated (12 sealed probes unread), so `probesPassed` is unknown.

## Gaps and limits

- No retained source states that GitHub Pages actually serves a dot-directory once Jekyll is bypassed or `include` runs; S086 gives the `.nojekyll` mechanism, S006/S080 give `include`, S001/S002 give packaging, and the served-path step stays `[INFERENCE]`, as does the exact `include: [".well-known"]` value.
- Pages' served `Content-Type` was not observed; the `text/plain` requirement is S078's rule, not a measurement.
- S081 (Wikipedia, secondary) and S087 (404) were opened and rejected; S087 is mentioned only as a reject and carries no fact.
- The L1's ds4cc tree observation was not added: the draft had 3 words of headroom under 1300 and the scope line excludes operator-property facts; `ScoutDs4ccWellKnown.md` stays the pointer if the L1 integrates it.
- No live request made by this seat; no tool installed or updated.

## Touched surfaces and out of scope

Lane: only this report, `.ufo/waves/round-35/w1/ScribeEntryDraft.md`. Sandbox: the draft, its receipt, folded source copies.
Not touched: product code, judge, counters, commits, pushes, jj, registry rows, sibling lanes, subagents. No verdict on the round.
