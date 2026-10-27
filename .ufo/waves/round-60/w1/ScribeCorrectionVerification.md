# ScribeCorrectionVerification

Assignment: draft the C3 append-only correction for `corpus/knowledge/googlebot-verification.md` (S426 entry), first line
`  **[r60-correction 2026-10-27]**`, citing S428, quoting the S428 sentence, stating the dated divergence and its
publisher-side consequence. Base revision `97cdc122379711c2b02a8970752c8782da3ac81d`; access date 2026-10-27 (UTC).
No lane file was modified: the patched whole file and the insertion live in `.files/` for the L1 to integrate.

## INSERT:

Anchor: base line 38
`  > "acts on the request of a user. Because the fetch was requested by a user, these fetchers ignore robots.txt rules."`.
The run is written into the paragraph gap that base line 39 (the base's own blank line) opens, i.e. patched lines 40..49:
nine prose lines plus the run's closing blank line. The base prefix `[:39]` is byte-identical to the base blob.

```text
  **[r60-correction 2026-10-27]** S428, printed revision `Last updated 2026-08-19 UTC`, states: "Because the fetch was requested by a user, these fetchers generally ignore robots.txt rules."
  S428 is the user-triggered fetchers page the S426 category table links to; the page quoted above (S426, printed revision
  `Last updated 2026-03-20 UTC`) prints the same sentence without the qualifier, reading these fetchers ignore robots.txt
  rules [S426]. The divergence is dated, not editorial: S426 carries the unqualified verb at its 2026-03-20 revision and
  S428 carries generally ignore at its 2026-08-19 revision [S428]. For a publisher deciding whether robots.txt alone holds a
  user-triggered fetcher back, the later, category-specific page is the stronger source and says something weaker than the
  line it supersedes: the category generally does not consult robots.txt, and the page stops short of promising that every
  request in it does not [INFERENCE]. No fetch was observed and no Google behaviour was measured here; both statements are
  what the two printed revisions say.
```

Placement rationale (two rejected shapes):
- Between base 38 and base 39 with no blank: a non-blank line directly after a blockquote paragraph is a CommonMark lazy
  continuation, so the correction would render *inside* the S426 quote — a misattribution of the newer page's wording to the
  older page. [INFERENCE: read from the CommonMark lazy-continuation rule; no renderer was run]
- A leading blank line in the run: the run's first line would be blank, not the tag, and the correction would not begin with
  `  **[r60-correction 2026-10-27]**`.
- Chosen shape: the base's own blank line closes the quote, the run starts with the tag, and the run ends with one blank line
  so the following base paragraph (line 40) stays a separate paragraph. Only inserted lines; no base line moved.

Line layout: tag line carries tag + `S428` + the 14-unit quote (so a check that wants tag, citation and span on one line is
satisfied); lines 2-9 hard-wrapped, no internal blank line.

## DIFF:

Command (base read with read-only git, no worktree touch):

```bash
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 97cdc122379711c2b02a8970752c8782da3ac81d:corpus/knowledge/googlebot-verification.md > base.md
diff -u base.md .ufo/waves/round-60/w1/ScribeCorrectionVerification.files/googlebot-verification.md
```

Result: one hunk `@@ -36,6 +36,15 @@`; plain `diff` reports `39a40,49` — 10 added lines (9 prose + 1 blank), zero
deletions, zero changed lines. Independent checks:

- `difflib.SequenceMatcher(base, patched)` opcodes: `[('equal',0,38,0,38), ('insert',38,38,38,48), ('equal',38,143,48,153)]` — no `replace`, no `delete`.
- `patched[:39] + patched[49:] == base` (byte-for-byte, after decoding with `split('\n')`).
- base line 38 occurs exactly once and is byte-identical; base file also keeps its trailing newline.
- sha256: base `25e3ac82a9402a40a1755a1f572837c2b41dbbd1914507aabd67db2b10a4ba39` (10 433 B) →
  patched `7ab4451206e27667fa2346ded3dcd46fa82cfb539bc6eb5fa4dfc31fd53cd628` (11 523 B).
- Insertion sha256 (10 lines, last blank): `0cbac24603d098ade2e04b54ff639f848a18607d3c2d63bf28f5679a513ec24a`.

Alignment caveat for the C2 guard (`scripts/append_guard.py`): the run ends with a blank line that duplicates the base blank
line at position 39, so a single difflib alignment classifies patched 39..48 as the inserted run — starting with a *base*
blank — and would print `untagged_insertion`. The contract's existential rule ("iff **no** alignment ... exists") makes the
file clean; the alignment that matches base blank 39 to the run's closing blank yields one run beginning with the tag. This
is exactly the C2 `K15` shape (`a,"",b` → `a,TAG,"","",b`, expected 0), so a guard that passes K15 must pass this file; a
difflib-only implementation fails both. Flagging it here because the real-lane case `R1` covers this file once integrated.

## SPAN CHECK:

Quote: `Because the fetch was requested by a user, these fetchers generally ignore robots.txt rules.`
14 whitespace units, 92 characters, ASCII quotes only (`"`), no curly quotes anywhere in the run.

Checks run against the retained bodies (whitespace-collapsed, article block `class="devsite-article-body` ..
`<devsite-content-footer`, text nodes only, `<style>/<script>/<aside>/<nav>/devsite-feedback/devsite-thumb-rating` blanked —
the round-59 helper's `text_segments`, imported directly from `.ufo/waves/round-59/c59_quote_truth.py`):

- S428 body (`S428.html`, 76 197 B, sha256 `0f296b8636d5fb9d44c66fc1453a5610fdf738c80c9baef44c233e0a1872d3b2`): the quote is a
  substring of exactly **one** text node of the article block; occurrences in the whole collapsed body: **1**.
- Page-uniqueness: occurrences in S426 body **0**, S427 **0**, S429 **0**.
- Printed revisions: S428 body carries `Last updated 2026-08-19 UTC`; S426 body carries `Last updated 2026-03-20 UTC`.
- Divergence is real in the retained bytes: S426 carries the unqualified sentence `these fetchers ignore robots.txt rules`
  exactly once; S428 carries it **0** times and carries the `generally ignore` sentence once.
- Link claim: S426's article-block category table, user-triggered row, has
  `<a href="/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers">User-triggered fetchers</a>` — the S428 URL.
- The run carries exactly one double-quoted span (the 92-character quote); nothing else in it is quoted, so no span of the
  inserted text can fail the C5 rules.
- Tag line: tag matches `\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]`, sits outside an HTML comment and outside a
  backtick span (4 backticks on the line, all after the tag; whole-file backtick prefix before the tag is even).

## Artifacts

- `.ufo/waves/round-60/w1/ScribeCorrectionVerification.files/insert.md` — the exact 10 inserted lines (last line blank).
- `.ufo/waves/round-60/w1/ScribeCorrectionVerification.files/googlebot-verification.md` — full patched file.
- `.ufo/waves/round-60/w1/ScribeCorrectionVerification.files/verify.py` — read-only re-run of every check above; last run
  exit 0, 16/16 PASS, printing the sha256s and byte counts quoted here.

## Out of scope / unrun

- No counter was run or written: C3's `c60_quote_truth.py` does not exist yet in this wave; nothing is scored here.
- No markdown renderer was available/run; the blockquote/paragraph rendering statements are [INFERENCE] from CommonMark.
- The S428 entry (`google-user-triggered-fetchers.md`) and the S429 entry are other seats' items; untouched.
- No git/jj mutation, no installs, no pacman; scratch `/fast/scratch/hyaku/kake-r60/ScribeCorrectionVerification/` was used
  only for the base snapshot and the patched build, and every cited byte was copied into `.files/` before removal.

VERDICT: Insertion drafted and self-verified — tag-first single run, S428 quote 14 units/92 chars in one page-unique text node, base bytes unchanged; sole integration caveat is the blank-line alignment the C2 guard's existential rule (K15) already requires.
