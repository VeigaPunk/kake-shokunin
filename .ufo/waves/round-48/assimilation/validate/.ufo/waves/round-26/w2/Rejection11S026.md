# Rejection11S026: falsify the L1 rejection of seat C1 for S026 (Python 3.15.0 → 3.15.1 label)

Candidate e28312b14b076584fedd696fae2a684e460bd11e; base 97404de4ff73d6c8a4f87385cf5fdf36dca7f006.
Axis: freshness. Leaf member; no delegation; only this file written.

## Verdict: AGREE

I tried to show that rejecting seat C1 hides staleness. It does not. The statement C1 targeted makes no version claim. Every taught sentence relied on from the 3.15.0-era readings is still verbatim in the 3.15.1 bytes. The changelog markers were the same at the 3.15.0 reading. The live page is byte-identical to the retained fetch. No corpus statement asserts "3.15.0" as a documentation version.

## What was rejected

- Seat C1 (`w1/PairS026StaticCanonicalPrefl.md`, row #2) marked L2 STALE. L2 is the S026 component of `verified-at: 2026-10-20 (S020-S027) ... documentation opened this round`. The seat's reason was that the 2026-10-20 reading was Python 3.15.0 and the current bytes carry 3.15.1.
- Ledger `statements.json`, S026 pair: `"seatStale": 2, "stale": 1`, l1Disposition `"C1 version label 3.15.0→3.15.1 within the pinned 3.15 family with relied-on sentences unchanged (recorded as a note); C2 accepted."`
- The rule applied is `corpus/QUALITY.md:217-221` (new in the candidate): "a patch-version label in the same documented family is not a stale claim; record it as a note."

## Counterexamples attempted, with evidence

1. **Is L2 wrong at its stated scope?** No. At base, line 2 reads (`git show 97404de:corpus/knowledge/static-canonical-preflight.md`, NR==2): `verified-at: 2026-10-20 (S020-S027) ... documentation opened this round`. It states only the date the documentation was opened, with no version, and that date is true. The row anchor (`SOURCES.md:34`, `population.json`) says "Python 3.15 documentation accessed 2026-10-20", which is family-scoped and still true. The rejection does not even need the new round-26 rule. The base round-21 rule (`97404de:corpus/QUALITY.md:43-49`) already says: "A provenance header records the original evidence date/revision and names whether that evidence is historical; installing a header is never live re-verification."

2. **Did taught content change between 3.15.0 and 3.15.1?** No evidence of any change. I extracted every quoted string from the 3.15.0-era reports (`round-22/w1/PythonParser.md`, `round-23/w1/ReopenPythonParser.md`, `round-22/w1/ParserScope.md`) and matched them after whitespace normalisation against `round-26/fetched/text/S026-1.txt`. All doc-content quotes were found, for example:
   - "This parser does not check that end tags match start tags or call the end-tag handler for elements which are closed implicitly by closing an outer element."
   - "The name will be translated to lower case, and quotes in the value have been removed"
   - "all character references (except the ones in elements like script and style) are automatically converted to the corresponding Unicode characters"
   - "This method is only called if convert_charrefs is false."
   - "incomplete data is buffered until more data is fed or close() is called"
   - "The content of elements like script and style is returned as is, without further parsing"

   The only misses were the 3.15.0 title and footer (the label itself), trailing-comma variants of found quotes ("parse invalid markup,"), and strings that are not from S026 (knowledge-entry text, row text, test inputs).

3. **Did the changelog or API move?** No. The retained 3.15.1 page has "Changed in version 3.4: convert_charrefs keyword argument added", "Changed in version 3.5: The default value for argument convert_charrefs is now True", and "Changed in version 3.14.1: Added the scripting parameter". Round 22 read the 3.15.0 page and already recorded the same facts (`round-22/w1/PythonParser.md:51`): "`convert_charrefs` default changed to `True` in 3.5 and `scripting` was added in 3.14.1." So the `scripting`/noscript wording was not introduced by 3.15.1.

4. **Has the page drifted since the retained fetch?** No. I made a plain public GET of the URL in `SOURCES.md:34` without saving it:
   - Headers: `HTTP/2 200`, `last-modified: Wed, 21 Oct 2026 13:04:30 GMT`, `etag: "6ad8b85e-d7dc"`, `content-length: 55260`, at `date: Wed, 21 Oct 2026 16:29:15 GMT`.
   - `curl -sS https://docs.python.org/3/library/html.parser.html | sha256sum` returned `d92217e08486dc9bfedf255f071fdad1ea1a506a1e8a8570c4711a47aad5faa3`.
   - `zcat fetched/S026-1.raw.gz | sha256sum` returned the same value. This is also the manifest/population digest.

5. **Does any statement pin 3.15.0 as a documentation version?** No. Running `git grep -E "3\.15(\.0)?|3\.14\.1|scripting"` at base over corpus, SKILL.md, LOG.md and SCORECARD.md finds:
   - `SOURCES.md:34-35` and `lessons/round-22.md:52`, which say "Python 3.15 documentation" (family scope).
   - `LOG.md:887` and `lessons/round-24.md:172`, which refer to an installed CPython 3.15.0 *interpreter*. These are historical install records, not S026 claims.

   Nothing becomes false because of the 3.15.1 label.

6. **Was the change recorded, not hidden?** Yes. The candidate's appended S026 block in `corpus/knowledge/static-canonical-preflight.md` (under "## Round-26 source recheck") says: "The page now labels itself Python 3.15.1 documentation (S026 and S027 alike); the 3.15 family and the relied-on sentences are unchanged." The row's `recheck: on-release` trigger was satisfied by this re-fetch (`RowS026.md` caveat 2). Seat C2 (L69's "all implicit closures") was accepted, so the real S026 overreach is corrected.

7. **Coordinates.** L2 and L69 are current coordinates, and they equal the base coordinates: the candidate only appended to this file, and at base NR==69 is "matching start/end tags or report all implicit closures (S026)". The round-21 +4 rule (`QUALITY.md:69-72` at base) covers only pre-round-21 pointers, so it does not apply to these round-26 pointers.

## Residual notes (none changes the verdict)

- **Low precision issue in the receipt.** `rechecks/S026.json` says "no taught content changed". The seat itself records that the 3.15.0 whole-page bytes were not retained, so a whole-page diff is UNVERIFIABLE. Quote-level evidence (items 2 and 3) supports the claim for every relied-on sentence, but strictly the receipt should say "no relied-on sentence changed".
- **Rule provenance.** The patch-label clause at `QUALITY.md:217-221` was written in the same candidate as the adjudication that cites it. The outcome stands without it, because of the base round-21 historical-header rule (item 1).
- **Out of target, routing only.** The row's teaches clause "HTML5 tree construction are not validated" has no verbatim support on the page: zero hits for "HTML5" or "tree construction" (`RowS026.md` caveat 1; seat R1). Under `QUALITY.md:220-221` ("attribution was false even at its base revision is STALE"), whoever owns row S026 should decide whether this is inference or misattribution. It is unrelated to the 3.15.1 label.

## Tooling

No installs or updates. Used `git`, `python3` (read-only, in memory), `sha256sum`, `zcat`, `curl` (one GET plus one header/body GET of the same SOURCES.md URL, nothing saved). Not run: `measure.py`, builds, tests, linters.

```json
{"target":"S026 L1 rejection of seat C1 (Python 3.15.0→3.15.1 label, same family)","verdict":"AGREE","severity":"none"}
```

Report: .ufo/waves/round-26/w2/Rejection11S026.md
