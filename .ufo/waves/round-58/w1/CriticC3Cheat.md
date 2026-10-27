# CriticC3Cheat

Attack on C3 (freshness, sourced) counter `c58_quote_truth.py` v1 at the frozen contract commit
`fff3eea6aa349c8635fd84a791cc32de350ee1c2`. Method: shared clone (`git clone --shared` of the lane)
of the freeze, junk build on a new branch, commit with `selftest` identity, run the counter against the
junk tip. Result: **8/8, met=true, EXIT=0** at tip `41ab1f315db25d26ce4f7452201b2f522c0c028f`
(base control: 0/8, EXIT=1). No tools installed (raw `python3 -B` + `git` only); no credentials/private URLs.

## CHEATS:

**C1. Question-header-only entries — zero claims pass all quote conditions.**
Entries quote FAQ question headers verbatim from the retained article block, with prose stating no claim
is made (e.g. `"2、Q：如何才能识别当前抓取是正确的百度蜘蛛？"`). Counter passes because C5 checks
provenance only: raw substring of one text node of the article block, 6–25 units, ≤40 chars (ASCII
quotes), page-unique, ≥3 distinct, one containing the literal `百度蜘蛛`. Nothing verifies any quoted span
carries or supports a claim. Entry built from 4 question headers (S423) and 3 question/suggestion
fragments (S424) passes C1–C8.

**C2. Cross-entry span reuse is tolerated.**
`"封禁百度蜘蛛"` (6 units / 6 chars; occurs 4× in S423, 5× in S424) is quoted in both entries. C5
passes: `verify()` is per-body (substring + ceilings + in-content, no cross-body duplicate check), and
the uniqueness accumulator only *excludes* non-unique spans instead of failing them. Only Gate quotes are
strictly uniqueness-gated; reusing a span across the two Gates would fail C5.

**C3. Rendering/claim contradiction is untestable.**
Entry S424's prose asserts the quoted fragments are questions/suggestions carrying no procedure fact —
directly contradicting the claim the entry nominally makes (the unblocking procedure) — while quoting the
real fragments. The counter never connects prose to quotes, so it passes 8/8. The contract's own stated
limit ("quote truth, not support" / "does not test whether the English rendering is faithful") is the hole.

**C4. UA strings as quotes: mostly blocked, fragment-filler only.**
Full UA strings fail: PC UA `Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)`
= 4 units / 83 chars → FAILS the 40-char ceiling; mobile UA ≈ 18 units / 219 chars → FAILS. A fragment
`Baiduspider/2.0` (1 unit / 15 chars) passes `verify()` but sits under the 6-unit floor, so it never
contributes to the required unique/topic spans — usable only as inert filler. Net: the 25-unit vs 40-char
interplay blocks whole-UA-string quotes; a whitespace-free Latin token scores 1 unit, so the unit rule is
effectively inert for Latin-only filler (40-char ceiling is the real bound).

Tally: junk fixture 8/8 met=true (exit 0); base do-nothing control 0/8 met=false (exit 1).

Fixture committed on top of the freeze (branch `junk`, tip `41ab1f3`; first tip `9d23b3b` was 7/8 only
because my own census stdout text contained the substrings "E03"/"E04" — removed in the second commit):
- `corpus/knowledge/baidu-spider-identification.md`, `corpus/knowledge/baidu-spider-unblocking.md` —
  question-header-only junk entries (headers `source:`/`verified-at:`/`recheck:` filled; id cited below header).
- `corpus/SOURCES.md` — base mirror + exactly two new rows S423/S424
  (`docs`/`A`/`mined`/`opened 2026-10-26`/`recheck 90d`; anchor `§<Q-header> (发布日期 YYYY-MM-DD)`;
  used-by exactly the entry path; title = page `<title>` before suffix; scope/teaches ≥ 20 chars).
- `corpus/lessons/round-58.md` — `## Gate` lines per id carrying URL, access date 2026-10-26, body
  sha256 + byte count, the anchor cell, and one topic-carrying unique quote with stated unit count.
- `.ufo/waves/round-58/assimilation/validate/{census-argv.txt,census-stdout.txt,census-exit.txt,
  corpus/SOURCES.md,corpus/knowledge/*.md}` — hand-written validate receipt.
- Frozen bodies (`sources/S423.html`, `sources/S424.html`), `sources/receipts.json`, mirror, pin untouched.

## HOLES:

- C5 validates quote provenance, never claim support: real, sourced, sized, unique, in-block — but no
  condition checks that the entry's assertions follow from the quotes.
- Topic test is lexical: substring `百度蜘蛛` anywhere in one unique span satisfies the subject
  requirement; a bare question header suffices.
- Uniqueness counts only toward the min-3 accumulator; duplicates are silent and tolerated.
- C7 is a self-describing text receipt: argv/stdout/exit files are committed text; any plausible text
  passes, including the `file\tok\t…` tail. No link to a real census run exists (contract says the same).
- Counter v1 selftest is a stub (exit 2): none of the round-57 v2.1 junk classes (off-topic spans, curly
  quotes, wrong digest, mirror divergence, etc.) are exercised by a wave-1 run; nothing in v1 stops these
  four cheats.
- Curly quotes are banned in every entry/Gate line, even though the source pages legitimately contain “”;
  quoting genuine curly-quote passages is impossible — a stricter-than-necessary restriction.

## LIMITS TO DISCLOSE:

- The counter does not test rendering faithfulness (contract: "quote truth, not support"); cherry-picking
  true-but-inert spans is the residual attack surface — human/critic review is the only defense.
- Receipts are checked as committed artifacts, not proofs of fetch/validation (C6/C7 as designed).
- All results above are against counter v1 at the frozen commit (contract sha256
  `0dde4d649d9b455025badd3f2c5260a4026e53cde24a53d61c7a8b01d3abbeed`); a ported selftest or reviewer
  judgment remains the defense.
- Fixture scratch under `/fast/scratch/hyaku/kake-r58/CriticC3Cheat` was deleted after this report; the
  evidence above is the full run record (per-check states all pass at the junk tip).

VERDICT: C3's counter is junk-passable at 8/8 with zero-claim question-header entries, cross-entry span
reuse, prose that contradicts the quoted material, and a hand-written validate receipt; the claim's truth
rests entirely on human review of rendering and claims, which the counter explicitly disclaims.
