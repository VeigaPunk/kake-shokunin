# ReopenGateS097 — live re-open of robotstxt.org/orig.html; reject reason and flip (freshness)
Seat KakeR37.ReopenGateS097, leaf. Lane read-only; only lane write is this file. Sandbox evidence
`/fast/scratch/hyaku/kake-r37w2/ReopenGateS097/{s097.html,s097.hdr,repro.py,SOURCES.at-tip.md}`.
Lane tip read `79d3c78` (row `corpus/SOURCES.md:105`; row in working tree identical).

## Commands, exit codes, observed output
- `curl -sS -D s097.hdr -o s097.html --max-time 60 https://www.robotstxt.org/orig.html` → **0**;
  `HTTP/1.1 200`, `Date: Fri, 23 Oct 2026 03:44:46 GMT`, `Apache/2.4.68 (Debian)`,
  `Last-Modified: Sun, 03 May 2020 13:24:25 GMT`, `ETag "2a1e-5a4be554a2ea6"`, length 10782. No redirect.
- `sha256sum s097.html` → **0** `446ea152…20c1b2` = receipt `S097.bodySha256` = `gzip -dc S097.html.gz | sha256sum`.
  Identical 54 min after the 02:50:51Z receipt.
- `timeout 120 python3 -B repro.py` → **0**: `live-visible sha a42aee4e…be3801 == retained True`, 6606 B /
  1072 words (receipt `textWords` 1072); `tag->empty sha e01f4076…da82`, 6573 B / 1039 words;
  `quotes NOT in retained: [1, 2, 6, 11]`, `quotes NOT in tag->empty: []`; `Allow:` 0.
- `awk -F'|'` on `git show 79d3c78:corpus/SOURCES.md` → **0**: `S097 NF=13`, `malformed=0`.
- `grep -rn "S097" corpus/knowledge/` → **1** (no hits): `used-by —` consistent.
- `grep -c -i obsoletes .ufo/waves/round-37/sources/S011.txt` → **1** (count 0).

## Reject reason (line = raw-HTML line of today's body)
1. **`superseded` — holds as scoped inference, not as S097 text.** The page says "This document
   represents a consensus on 30 June 1994" (l.132), "It is not an official standard backed by a
   standards body" (l.141), "It is not enforced by anybody" (l.144), and points to itself as the latest
   version (l.153). Supersession rests on S011: retained `S011.txt:1` has `Category: Standards Track`
   and "specifies and extends the 'Robots Exclusion Protocol' method originally defined by Martijn
   Koster in 1994"; no `Obsoletes` field. "For current behavior" keeps it honest. **Holds.**
2. **`no Allow` — holds.** Zero `Allow:` in body; located: "The record starts with one or more
   User-agent lines, followed by one or more Disallow lines" (l.258-259), "Unrecognised headers are
   ignored." (l.260), "At least one Disallow field needs to be present in a record." (l.304-305).
3. **`substring user-agent` — holds verbatim** (l.277): "A case insensitive substring match of the
   name without version information is recommended." It is advice; retained RFC 9309 instead requires
   "case-insensitive matching to find the group that matches the product token", so "historical" is fair.
4. **`one '*' record` — holds verbatim** (l.283-285): "It is not allowed to have multiple such records
   in the "/robots.txt" file." (raw HTML wraps `/robots.txt` in `<code>`; retained shows `" /robots.txt "`).
Reject verdict as a whole: **holds** — the document self-declares non-normative and differs from S011
on `Allow`, matching and the single-`*` restriction.

## Flip verdict
Row: "flip: RFC 9309 is withdrawn and this text becomes the operative primary REP specification".
- **Shape well-formed** per `CORPUS.md:102` (`REJECTED: <reason>; flip: <what would change the verdict>`).
- **Content not operational: overstated.** Conjunct 1 is observable (RFC status) and unmet (S011
  retained 2026-10-23T02:50:49Z, HTTP 200, Standards Track). Conjunct 2 has no observation path: no
  source publishes "this text becomes the operative primary REP specification", and the page itself
  disclaims official status and enforcement (l.141, l.144), so the 365d recheck can never see it.
- Precedent: 16 of the 17 other rejected rows carry a literal `flip:`, each one observable (e.g. GET:
  S053/S071/S087; named-page statement: S017/S018/S044-S046/S063/S074/S075/S081; checkable fact:
  S094); `corpus/lessons/round-29.md:75` credits "a checkable flip". S097 is the only literal flip with
  an unobservable second limb. The 17th, **S093** (rejected, opened 2026-10-23, `SOURCES.md:101`), has
  no `flip:` label at all — teaches ends "Reconsider only for unique evidence not available from a
  primary source" — a `CORPUS.md:102` shape breach in an integrated row; S097's defect is not unique,
  but S093 does not cure it.
- Wording drift: Gate (`79d3c78:corpus/lessons/round-37.md:54-58`) "operative specification" vs row "operative **primary REP** specification" — not a rule breach.

## Wave-1 freshness note: two reproducible defects
- "Quotes 2 and 11 are in browser-rendered form" — undercounts: **four** quotes (1, 2, 6, 11) are absent
  from the retained text because they wrap `<code>/robots.txt</code>` or `<code>*</code>` (l.189-190,
  l.283-285); retained has 6 spaced `" /robots.txt "` and 1 `' * '`, 0 tight forms. **Overstated.**
- "Naive tag deletion gives 1039 words and `" /robots.txt "`" — pairs numbers from two extractions:
  tags→empty = 1039 words with **tight** `"/robots.txt"` (0 spaced); tags→space = 1072 words with
  **spaced** `" /robots.txt "` (6). **Wrong pairing** (harmless to content).
- Consequence for `corpus/lessons/round-37.md:37` "every retained visible text is byte-identical to the
  scout's live extraction": true for the fetcher-rule extraction (`a42aee4e…`), false for the extraction
  in which all twelve wave-1 quotes are substrings (`e01f4076…`, 1039 words). **Unverifiable as written**;
  the scout's extraction file is not committed.
- Minor: lesson "contradicts the contract on seven points" (l.60) — two of wave-1's seven are conditional
  divergences (empty value; a validity rule the contract drops). "Diverges" is accurate. Also row scope
  calls the document a "proposal"; the page calls itself a consensus/standard (unofficial).

## Confirmed
- Gate quote "It is not an official standard backed by a standards body" is exact in retained (1 match),
  10 words, Status section l.141; reject evidence in the wave-1 report matches the S094 precedent.
  Body unchanged since 2020-05-03 (server header); identical across the 02:50:51Z receipt, wave-1's
  03:22:58Z fetch and mine at 03:44:46Z. Retained text reproduces byte-for-byte from today's body.
  No sealed key/case touched, no tool installs, no lane git/jj mutation.

## Unknowns
- Scout's rendering file uncommitted; its cites are raw-HTML lines and all sampled ones check (`#status`
  130, `#method` 183, `#format` 235, `#examples` 314; quotes 141/189/260/277/283-285/304). Plain-`http://`
  URL and archives untested (named https URL 200, byte-stable). Flip observability is a rule judgement:
  high confidence on facts, medium on the label.
