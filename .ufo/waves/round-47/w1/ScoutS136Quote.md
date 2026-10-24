# ScoutS136Quote — S136 gitrevisions quote / receipt verification

Seat: ScoutS136Quote (scout, axis: freshness). Read-only checks; scratch fetch at
`/fast/scratch/hyaku/kake-r47/ScoutS136Quote/gitrevisions-live.html`. No lane files modified.

## Verdict

**VERIFIED with one minor imprecision flagged.** The Gate's located quote is verbatim in
the retained text at the claimed span (≤25-word rule satisfied), the HTTP receipt is
real and the committed bytes hash-match the recorded sha256, a live re-fetch today is
byte-identical, and the knowledge entry's teaching stays inside Git's repo-local
abbreviation semantics. One imprecision found in the *closure spot-check's* restatement
(not the Gate itself), detailed below.

## 1. Quote location and word count — PASS

Gate text: `corpus/lessons/round-47.md:67-69` locates the quote (labeled "18 words") as:

> "The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that
> is unique within the repository."

Retained text `.ufo/waves/round-47/sources/S136.txt:2179-2180` is the source, wrapped
mid-sentence inside `<p>` under the `<sha1>` `<dt>` (line 2177):

```
2179  <p>The full SHA-1 object name (40-byte hexadecimal string), or\n
2180  a leading substring that is unique within the repository.\n
```

Byte dump (`sed -n '2179p' | od -c`, same for 2180) shows line 2179 ends `o r \n` (no
trailing space) and 2180 ends `. \n`; joining the wrapped lines with one space and
stripping `<p>` yields the Gate quote **verbatim**. Word count re-derived:

```
echo 'The full SHA-1 object name (40-byte hexadecimal string), or a leading substring
that is unique within the repository.' | wc -w  →  18
```

18 words, ≤25 — the Gate's count and the spec's bound are both correct.

The second quote claimed "verified present" at Gate lines 72-75 ("E.g.
dae86e1950b1277e545cee180551750029cfe735 and dae86e both name the same commit object if
there is no other object in your repository whose object name starts with dae86e.")
matches S136.txt:2181-2183 verbatim modulo line-wrap, including the plain-text `dae86e`
(the HTML keeps the source's `&lt;em&gt;` typography, not `*dae86e*` asterisks).

### Flag (minor imprecision, not a Gate error)

`corpus/lessons/round-47-verifier-spotcheck.md:60` restates the quote as the fragment
`"…or a leading substring that is unique within the repository."` and labels it
"(18 words, ≤25) present verbatim at retained-text line 2180". Observed: that displayed
fragment is **10 words** (`wc -w` = 10); 18 is the count of the full Gate quote. The
claimed line number and ≤25 verdict still hold, so the spot-check's *conclusion* is
sound, but its word count does not describe the fragment it prints. Cosmetic; the
admissibility rule is still satisfied either way (10 or 18, both ≤25).

## 2. HTTP / byte / hash receipt — PASS, with a structural note

- Receipt file: `.ufo/waves/round-47/sources/receipts.log`:
  ```
  GET https://git-scm.com/docs/gitrevisions  2026-10-24T06:31:20Z
  HTTP_STATUS=200 BYTES=74526
  exit=0
  ```
- Committed file measured: `wc -c` → **74526 bytes**, `sha256sum` →
  `33a99ba212228d6968e7721a87197558b0e88a450ecfc303eaa34d8321d2da8c` — matches the
  `33a99ba2…2d2da8c` recorded in `corpus/SOURCES.md:144` (S136 row), `round-47.md:65`,
  and the spot-check. BYTES=74526 matches receipts.log and the row's "74,526 bytes".
- **Live re-fetch run** (read-only, into scratch):
  `curl -sS -o …/gitrevisions-live.html https://git-scm.com/docs/gitrevisions` →
  `HTTP_CODE=200 BYTES=74526`; `sha256sum` → `33a99ba2…2d2da8c` — **byte-identical to
  the committed retained text today**. Freshness confirmed as of this check, not just
  at fetch time.
- Structural note (observed, not a defect per the row's own claim): `receipts.log`
  itself carries only URL/status/bytes/exit — **no content hash in the receipt file**.
  The hash binding lives in the SOURCES row and Gate prose. Since the row records the
  full path and the truncated sha, verification still closes (I did exactly that), but
  the receipt log alone does not prove content identity.

## 3. Repo-local abbreviation semantics — within scope

Git's documented rule (S136.txt:2179-2183): an abbreviated object name resolves iff it
is a leading substring **unique within the repository**; the example is
prefix-collision against objects in "your repository". That is the only abbreviation
statement in the page — grepping the retained file for `unique|ambiguous|abbreviat|
minimum` finds no other sha1-abbreviation qualifier (the only "ambiguous" hits concern
*refname* disambiguation, lines 2197+). Notably the page states **no minimum length**.

Checked claims in `corpus/knowledge/commit-citation-hygiene.md` against that rule:

- Lines 17-19: "Git accepts an abbreviated object name only while it is a leading
  substring unique within the repository — uniqueness, not length, is the
  resolvability test" — faithful paraphrase, quotes the doc verbatim.
- Lines 22-24: a once-resolving token "can go dead later if the prefix becomes
  ambiguous" — a direct consequence of uniqueness being evaluated against the live
  object store; supported by the doc's collision example, though the "later" temporal
  aspect is [INFERENCE] from the semantics, not a literal doc sentence.
- Lines 22-27: dead here / may resolve elsewhere; `e5455253` example — grounded
  exactly in the doc's "within the repository" / "your repository" scoping. Correctly
  repo-local, no universal nonexistence claim (the entry explicitly says
  "repository-scoped, never universal", line 24).
- Lines 28-34: external-repo tokens "can never resolve here" — strictly, resolution
  succeeds for any object present in this object store regardless of provenance; the
  claim holds for objects absent from the lane repo and is a lane exclusion policy,
  consistent with repo-local scope rather than a misreading of Git.
- SOURCES.md row claim (line 144) and study path (line 152) scope S136 to "revision-
  token abbreviation and resolution semantics only; not a claim about any hosting
  platform" — accurate; the page is exactly that and the study path's instruction
  ("do not infer whether an external repository contains that object") mirrors the
  repo-local boundary.
- Boundary caveat worth recording: "uniqueness, not length" is the *doc's* framing,
  but Git also enforces a minimum abbreviation length (~4 hex via `core.abbrev`/
  disambiguation rules) that this page never mentions. For the entry's actual scope —
  7-8+ char tokens — the caveat is immaterial; the teaching does not overclaim about
  sub-4-char tokens.

## 4. Cross-claims verified

- `corpus/README.md:38`: "S136 grounds Git revision semantics only" — consistent.
- `round-47.md:84`: "rows 135 → 136 (S136 added, mined, tier A)" — row exists at
  SOURCES.md:144 with `mined | 2026-10-24 | 365d` and used-by
  `corpus/knowledge/commit-citation-hygiene.md, corpus/lessons/round-47.md`; both
  files exist and cite S136 (checked above).
- `LOG.md:1843` ("opened … S136 (tier A, 2026-10-24T06:31:20Z, HTTP 200)") matches
  receipts.log exactly.

## Tooling

No installs needed; used only repo files, `wc`, `sha256sum`, `curl`, `od`, `sed`.

## Remaining unknowns / not checked

- Whether `git rev-parse -q --verify` resolves abbreviated names identically to the
  doc's `<sha1>` rule in every Git version (the page does not discuss rev-parse's
  flags); not needed to close this item.
- The 40-hex `dae86e1950b1277e545cee180551750029cfe735` in the doc is illustrative,
  not a real object — no claim made about it by the lane.
