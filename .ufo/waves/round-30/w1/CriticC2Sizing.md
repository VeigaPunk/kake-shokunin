# Round 30 wave 1 — CriticC2Sizing: C2 claim sizing and quote-truth counter limits

Seat: KakeR30.CriticC2Sizing (leaf critic, advisory). Axis judged: freshness. No network, no installs, no lane mutation beyond this file.
Read: `.ufo/waves/round-30/c2_quote_truth.py` (sha256 a2cd3164…5e7a, blob bae263ac), `fetch_sources.py`, `sources/receipts.json`,
`verification/c2-before-0356681.json`, SCORECARD.md:676-727, round-29 counter diff, `corpus/lessons/round-29.md:24-39`, all 25 `corpus/knowledge/*.md` headers.
Sandbox: `/fast/scratch/hyaku/kake-r30/w1/CriticC2Sizing/` (clone at 4580c78; `attack.py` builds detached adversarial commits there; `relaxed_counter.py`).

## Commands run (cwd sandbox or its clone, TMPDIR inside the sandbox)
- Re-derive the retained text from each `<id>.html.gz` with the fetcher's rule, compare to body/text sha256 in receipts: all four True (exit 0). The retained evidence at 4580c78 is internally honest.
- `python3 -B attack.py` (exit 0) runs the unmodified counter on six commits on top of 4580c78:

| Case | What the commit contains | Counter result |
|---|---|---|
| A1 | entry asserts false things ("publish only on a full moon", "ignores every redirect rule"); ids only on a trailing `Sources: S049 S050 S051 S052.` line; every Gate quote is “Render” | exit 0, 4/4, control holds |
| A2 | Gate quote is the sub-word fragment “ender”; ids only inside `<!-- S049 S050 S051 S052 -->` | exit 0, 4/4 |
| A3 | registry cell `https://attacker.example/?next=https://render.com/docs/static-sites-v2`; Gate lines name `https://wrong.example/<id>` | exit 0, 4/4 |
| A4 | `<id>.txt` replaced by one fabricated sentence, `textSha256` in receipts.json updated to match | exit 0, 4/4 on a fabricated quote |
| A5 | sensible entry citing all ids only on line 7 (a real body line) | exit 1, 0/4 |
| A6 | Gate quote “Static   Sites” (three spaces) | exit 1, 2/4 (S049, S051 pass: collapse applied; S050, S052 lack the phrase) |

- `python3 -B relaxed_counter.py --root . --revision 99c5ff76` (copy with check d forced true): exit 0, 4/4, same `revision`, counterSha256 748a3fd5….
- `git show 4580c78:.ufo/waves/round-30/c2_quote_truth.py | python3 -B - …`: exit 1, `FileNotFoundError: '<stdin>'` (the self-hash opens `__file__`).

## Findings

1. **4/4 does not show any entry sentence rests on a quote, and the declaration understates how little 4/4 shows.** The gap itself is disclosed (SCORECARD.md:725-726). Not disclosed: a one-word or sub-word quote passes (counter lines 107-109: 1-25 words; line 114: plain substring, no word boundary), the quote need not appear in or near any entry sentence, and check b (line 105) accepts any body mention, including a sources list or an HTML comment (A1, A2). The control (line 116) flips only the first letter, so with “Render” it checks that "qender" is absent. That guards against a vacuous substring test. It says nothing about how strong the quote is.
   Fix (disclosure, value unchanged): add to SCORECARD C2 "4/4 is reachable with one-word quotes and a single sources line; the counter does not tie a quote to any entry sentence". Closure step: for each id, name the entry line that relies on its Gate quote and check it by hand.

2. **A row passes with a wrong URL.** Check a (lines 103-104) tests `url in cells[1]` as a substring, so any cell that contains the receipt URL passes (A3). The Gate-line URL and the entry header URL are never checked.
   Fix (closure check, counter untouched): require the source cell's URL token to equal `receipts.json[id].url` exactly, e.g. `python3 -c 'import re,json,sys;r=json.load(open(".ufo/waves/round-30/sources/receipts.json"));t=open("corpus/SOURCES.md").read();sys.exit(any(r[s]["url"] not in re.findall(r"https?://[^\s|;]+",next(l for l in t.splitlines() if l.startswith(f"| {s} |")).split("|")[2]) for s in r))'` (exit 0 means every id's URL is exact). I ran it in the sandbox: exit 0 on A1, which has the exact URLs, and exit 1 on A3. Disclose that the counter's URL test is a containment test.

3. **The counter trusts retained text and receipts at the measured revision (strongest counterexample, A4).** Lines 89-93 and 110-114 read `receipts.json` and `<id>.txt` from `<commit>`, and nothing pins them to the declared opening at 4580c78. A landed commit that rewrites both reports 4/4 on fabricated text.
   Fix (non-narrowing, no counter edit): the closure runs `git diff --quiet 4580c78 <commit> -- .ufo/waves/round-30/sources/ .ufo/waves/round-30/fetch_sources.py .ufo/waves/round-30/c2_quote_truth.py` and requires exit 0. SCORECARD C2 should say so. Optional: re-derive `<id>.txt` from `<id>.html.gz` as I did above.

4. **The "8-line metadata header" does not match the entry shape.** All 25 knowledge entries have a 3-line header (`source:`, `verified-at:`, `recheck:`); lines 4-8 are blank, title, blank and the first body lines. The counter (line 94) skips 8 lines. That is stricter than described, not inflating. A real body citation on line 7 (field-performance-cwv.md:7 cites S036 this way) would be ignored, and A5 shows an honest entry shaped like that scores 0/4: an avoidable honest stop.
   Fix: correct SCORECARD.md:719 to "after its first 8 lines (the 3-line metadata header, the title and the opening lines)", and tell the entry writer to keep the first citation of each id below line 8. Do not change the counter, because that would change its sha256.

5. **The whitespace-collapse rule is disclosed in the counter docstring (lines 17-18) and in each receipt's `textRule`, but not in the declaration (SCORECARD.md:719-721).** It is wider than spaces: the fetcher puts a space at every tag boundary and decodes entities, so a "true quote" matches the extracted text, not the rendered page (round-29.md:36 shows `http(s):/ / <owner>.github.io`). The quote pattern (line 41) also cannot hold curly quotes; the four texts contain none, so this round is unaffected. Matching is case-sensitive, so case is not part of the leniency.
   Fix: one SCORECARD sentence: "the quote and text are compared after collapsing all whitespace runs to one space; the text is the fetcher's tag-stripped extraction, so a quote may span tag boundaries; matching is plain substring".

6. **counterSha256 makes the receipt name the code that ran, but not tie it to the declared or committed counter.** Line 121 hashes the running file (`open(__file__)`), not the blob at `--revision`. A modified copy reports 4/4 with an unchanged `revision` field, and only the hash differs (748a3fd5… against a2cd3164…). The hash is sha256 of the bytes, not git's blob id (bae263ac), while the docstring cites the round-29 counter by blob id (139ede1e), so the two are easy to confuse. SCORECARD's C2 paragraph does not pin the counter hash; the C1 paragraph does (SCORECARD.md:714). Running the committed blob from stdin crashes with exit 1, which is the same code as an honest fail.
   Fix: add "counter sha256 `a2cd3164…5e7a`" to the C2 base evidence. The closure requires that the after-receipt's counterSha256 equals both that value and `git show <commit>:.ufo/waves/round-30/c2_quote_truth.py | sha256sum`.

## Impacted axes
freshness (sizing and provenance of the C2 value). Operability is not affected. None of the findings needs the declared value narrowed. Findings 2, 3 and 6 are fixable defects that need closure checks. Findings 1, 4 and 5 are disclosure wording.

## Not verified
I did not see the landed C2 entry, lesson or registry rows, because they do not exist at 4580c78. I did not check whether any real entry sentence follows from its quote, or whether the Render pages say what the entry will claim. No sources were fetched. There were no installs or updates.
