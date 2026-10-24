# GateQuotesTruth — round 29, wave 2 (falsify)

Item: the nine Gate quotes in corpus/lessons/round-29.md lines 36–39 and 51–55, at commit 7697990cbca20291f3b0367b8ff4220e93b38b03. Tests: exact substring of the retained text; at most 25 words; starts and ends on whole words. Committed bytes only, in sandbox clone /fast/scratch/hyaku/kake-r29/w2/GateQuotesTruth/clone. No network, no lane state changed, no installs (git 2.56.0, Python 3.14.8 standard library).

## Commands and exit codes
- git clone, then checkout 7697990…: exit 0. HEAD matches; status empty.
- git ls-files .ufo/waves/round-29: exit 0 (sources S040–S043 .txt, screened C1–C6 .txt, two receipts.json).
- sha256sum of retained .txt files: exit 0.
- python3 -B check_gate_quotes.py <clone> (sandbox script, reads only): exit 0. Output "quotes 9; failing 0". Negative controls on S042, all FAIL as expected: one letter changed; end cut "…into a rel"; start cut "end baseurl…".
- python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision 7697990… (in clone): exit 0. Output "C1 4/4 at 7697990…", controlBroken false.
- Search for the opening curly quote in the lesson file: lines 36–39 and 51–55 only.
- Read-only python re-derivation (no script run): all 10 retained bodies match receipts bodySha256. The visible-text rule copied from fetch_sources.py:33–38 (not imported) reproduces every .txt byte for byte and its textSha256.
- Locators checked against decompressed raw HTML and the .txt files.

## Verdicts per quote (one exact occurrence each; boundaries clean)
| Line | ID | Retained file (sha256 prefix) | Words ws / \w+ | Before / after | Verdict |
|---|---|---|---|---|---|
| 36 | S040 | sources/S040.txt (625f2b0783a1) | 10 / 14 | space / space | holds; limit F3 |
| 37 | S041 | sources/S041.txt (86a77ee24f7e) | 20 / 23 | space / . | holds |
| 38 | S042 | sources/S042.txt (b66fefc15f2b) | 16 / 16 | space / space | quote holds; locator broken F1 |
| 39 | S043 | sources/S043.txt (d665dd23b193) | 19 / 25 | space / space | holds; limit F2 |
| 51 | S044 | screened/C1.txt (9e49199dfbd8) | 19 / 21 | space / , | holds |
| 52 | S045 | screened/C3.txt (040620b6a2cc) | 21 / 24 | space / space | holds |
| 53 | S046 | screened/C5.txt (dd0cd1f18890) | 15 / 15 | space / space | holds |
| 54 | S047 | screened/C4.txt (38c2af9096c9) | 14 / 14 | space / space | holds |
| 55 | S048 | screened/C6.txt (dc221f2ef67c) | 11 / 11 | space / space | holds |

Receipt URLs match each Gate row. Access times: 2026-10-22T10:29:37Z (S040–S043) and 10:34:12Z–10:35:40Z (C1–C6).

## Findings
F1, broken, minor (locator). Line 38 names a "Standard filters table". The quote occurs once, in the table under the h1 "Liquid Filters" (decompressed sources/S042.html.gz: h1 at offset 6950, quote at 7627). The "Standard Liquid Filters" h3 sits at 29803 (S042.txt char 8141), after the quote (char 786). Quote holds; table name does not.
F2, limit, undisclosed. Line 39 quote has two spaces the rendered page lacks: "<REPO> )," and "'/<REPO>/' .". The page HTML has "</code>)," and "&#39;</code>.". Cause: fetch_sources.py:36 replaces each removed tag with a space. Lines 41–42 disclose this for S040 only.
F3, limit, disclosed. Line 36 "http(s):/ /" comes from `<wbr/>` replaced by a space (lines 41–42).
F4, limit, documentation. textRule in sources/receipts.json:8 and sources/screened/receipts.json:9 says "tags removed". Code at fetch_sources.py:36 writes a space. Texts reproduce exactly, so the artifacts are deterministic, but the rule is misdescribed.
F5, limit, counter scope. c1_quote_truth.py covers S040–S043 only. Word check is whitespace tokens (line 106). No boundary test. Quote and text are both whitespace-collapsed (lines 105, 108). Its 4/4 reproduces. S044–S048 have no committed counter.
F6, limit, margin. S043 is 25 words by the \w+ count and 19 by whitespace. It passes "at most 25" under both.
F7, out of scope. Line 56 says C2 "Not opened". screened/receipts.json:19 records "opened": true with status 403 and a 9-word retained text. I did not open that text. No quote is involved.

## Residual risk and gaps
- No live fetch (bounds). I did not confirm the live pages still carry these quotes; the evidence is the 2026-10-22 receipts.
- Lane working tree not examined; committed bytes only.
- Whole-word rule used: neighbouring characters are not letters, digits or underscores. Another reading could change S043, which ends in " .".
- Registry claims beyond URL, access date and quote text not checked. No other seat's reports read.

## Verdict
All nine quotes hold on exact substring, the 25-word limit and whole-word boundaries. Broken: F1 (S042 table name). Limits to state: F2 (S043 spacing, undisclosed) and F5 (counter covers four quotes and tests no boundaries). Freshness: retained bodies and texts match their receipts byte for byte.

Checker (sandbox only): /fast/scratch/hyaku/kake-r29/w2/GateQuotesTruth/check_gate_quotes.py
