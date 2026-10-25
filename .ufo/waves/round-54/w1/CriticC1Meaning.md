# CriticC1Meaning — r54 C1 revised-wording attack

Seat: `L1Kake54.CriticC1Meaning` (critic, leaf, read-only).
Scope: attack whether the revised English wording captures the Japanese
crawl qualifier without implying a crawl refusal — distinguishing
"does not recommend crawling" from "will not fetch".
Verdict: **the committed wording largely survives the attack; the
instrument that "verifies" it does not.** One demonstrated gate
counterexample, one framing residue, three minor distortions.

## Evidence base

- Source (retained body, sha256 `3ad358bd…`, confirmed):
  `.ufo/waves/round-52/sources/S374.html` line 104 — single occurrence
  (byte offset 2727):
  `&lt;a&gt;タグに属性rel=&quot;nofollow&quot;が指定された場合、このリンク先のウェブページの巡回を推奨していない、あるいは信頼できるリンクではないとサイト管理者（ウェブマスターやブログのオーナー）が考えているとみなします。rel=&quot;nofollow&quot;の指定されたリンクのURLは、新しいウェブページを見つけるために利用されますが、…`
  Title/subject line 100 (also 33, 242): `リンク先のウェブページの巡回制限　― rel属性の利用`.
- Repair commit `8e408e00fbe1c5908df62ba79e78c944bda479e2`
  ("round-54: repair S374 calibration…"); worktree entry bytes ==
  HEAD bytes (`59d600c2…`).
- Entry: `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`
  lines 11–21 (quote + old gloss), 52–62 (r54 correction block).
- Counter: `.ufo/waves/round-54/c54_s374_calib.py` (committed bytes
  `32b96727…` = HEAD), lines 43–48, 60–73, 107.

## What the revised wording gets right (attack resisted)

1. **Modality preserved — recommendation withheld, not action refused.**
   推奨していない is "does not recommend"; the correction (entry 56–58)
   renders "the site owner is taken to **not recommend the crawling of
   the link target's web page**" — negated recommendation of *the crawl
   itself*, which is the qualifier the base gloss (entry 13–14) dropped.
   Crucially the source lexicon separates the two modalities: this page
   uses 推奨 (recommend) for `nofollow`; sibling nav anchors at lines
   222 and 232 use 拒否 (refusal) for robots-level settings
   (`サイト単位、ディレクトリ単位での巡回の拒否設定`). "Does not
   recommend crawling" ≠ "will not fetch" is a distinction the source
   itself draws — the wording honors it.
2. **Inference framing preserved.** みなします ("we deem/regard") is an
   engine-side inference about the *site administrator's* stance
   (サイト管理者考えている). The correction keeps "is taken to" +
   "the site owner" — no subject inversion to the crawler. The disjunct
   structure survives: "or to consider the link untrustworthy" mirrors
   あるいは信頼できるリンクではない.
3. **Explicit anti-refusal disclaimer.** Entry 60–61: "this does **not**
   assert that the crawler refuses to fetch the URL, and the source
   continues that the URL may be used to discover new pages" — grounded
   in line 104's 利用されます. A reader cannot walk away with "will
   not fetch" from this block.
4. **No new refusal implication introduced.** The old gloss survives
   verbatim above as "historical text" (62); the block names its own
   scope ("supersedes its gloss"). The phrase 「…巡回を推奨していない」
   is quoted byte-exact (11, 55).

## Counterexample — refusal-implying correction passes the gate (demonstrated)

The instrument checks *presence* of the polarity phrase, never
*absence* of a co-asserted refusal. `qualifier_findings`
(`c54_s374_calib.py:68–72`) requires only `QUOTE in window` +
`NEGATIVE_CRAWL_RE.search(window)` in a 1200-byte window; line 46's
`SEMANTIC_RE` (which contains `refus`) is applied to rendered cells,
never to the correction window.

Constructed entry: real repair entry with the honest block replaced by

```
**[r54-correction 2026-10-25]** The phrase 「このリンク先のウェブページの巡回を推奨していない」:
the site owner is taken to not recommend the crawling of the link
target's page, and the engine will not fetch that URL because of the
attribute.
```

This asserts exactly the refused-fetch misreading the entry exists to
stop (entry 25–28: "Reading `nofollow` as 'do not fetch this URL' is
the over-read this row exists to stop"). Result, committed counter
bytes (`/tmp/c54_committed.py` = `git show HEAD:…`), scratch repo
`/tmp/c1mean` rev `e93a9267e2c8a183791e23bfc9b867970008406b`:

```
PASS C1.1_body / C1.2_cells(suspect_cells=1) / C1.3_correction(block_offset 2876)
PASS C1.4_mismatch {'mismatches': 0}
mismatches=0 met=True   EXIT=0
```

Impact: the frozen predicate measures "qualifier stated and upstream
suspect suppressed" — it cannot detect "qualifier stated *while
implying refusal*". On the meaning axis the claim over-proves: the
wording is honest but nothing in the gate would catch the same repair
done dishonestly. Fixable defect, not just tradeoff (sibling
CriticC1CorrectionBinding reaches a parallel conclusion on supersession
binding; this is the refusal-polarity flank of the same 1200-byte
window).

## Framing residue (fixable, low-moderate)

Entry 55–56: "glosses the source phrase … as only an endorsement
statement. The phrase includes a crawl qualifier". Calling the crawl
recommendation a "qualifier" under-centers it: the source clause is a
two-disjunct predicate — 巡回を推奨していない ∨ 信頼できるリンクではない —
with **no endorsement vocabulary at all** (no 支持/推薦/endorse term;
the nearest second disjunct is link *trust*, which the old gloss's
"cannot vouch for" already approximates). The phrase does not "include"
the crawl reading; the crawl reading *is* its first disjunct. Same
residue in the retained headline (line 6: "a statement about
endorsement, not a crawl refusal") — now protected historical text,
but the block's own phrasing half-perpetuates the endorsement-first
reading it corrects.

## Minor distortions (logged, none blocking)

- Entry 61: "the URL **may be** used to discover new pages" hedges
  利用されます (assertive "is used"); entry 29 itself says "is used".
  Understates the strongest in-source evidence against refusal.
- "untrustworthy" (57) for 信頼できるリンクではない ("not a trustworthy
  link") — slightly stronger predicate; acceptable gloss.
- "site owner" for サイト管理者（ウェブマスターやブログのオーナー)
  (administrator/webmaster-or-blog-owner) — flattens the gloss;
  consistent with base gloss (13), so not a regression introduced here.
- Dropped demonstrative この ("*this* link target's page") — negligible;
  referent is clear.
- `NEGATIVE_CRAWL_RE` (line 46–47) accepts only the literal surface
  `not recommend (the) crawl(ing)`: semantically equivalent correct
  wordings — "recommends against crawling", "does not endorse the
  crawl", "discourages crawling" — all fail the gate (false negatives).
  Precision-by-form, not meaning: a canonical-judge tradeoff worth
  recording.
- "The subject is crawl restriction of linked pages" (58–59) is true
  of the *page's topic* (title line 100); a hostile reader could bind
  "crawl restriction" to the attribute's *effect* — mitigated by the
  same sentence citing the title and by 60–61's disclaimer.

## Mid-wave counter churn (provenance note)

The counter file mutated under this review: md5 `32b96727` (HEAD) →
`330bb254` (10:51, `qualifier_findings` returning 3-tuple while
`run_checks:108` unpacked 2 — crashes) → `153eddbdb` (later). The wave
is nominally read-only; the lane counter is being rewritten in place.
Committed `8e408e0` bytes were used for all receipts above. Sibling
CriticC1CorrectionBinding documents the earlier churn epoch; this is a
continuing provenance item for the closure, not a meaning defect.

## Smallest safe correction

1. Add a refusal-polarity clause to the correction acceptance in
   `qualifier_findings`: within the same window, reject on un-negated
   refusal assertions — e.g. fail if
   `(?:will not (?:fetch|crawl)|refus(?:e|es|al)|do(?:es)? not fetch)`
   appears *unless* it occurs inside an explicit disclaimer span
   (`does not assert …`/`not (?:a|any) refus`). Admittedly brittle —
   which is itself the finding: "does not imply refusal" is a semantic
   property a token gate can only approximate; the predicate should
   either say so or stay silent on the axis.
2. One-line wording tighten in the appended block (append-only,
   so a further `[r54-correction]` addendum if the judge agrees):
   "the phrase's first disjunct is the withheld crawl recommendation;
   'endorsement' appears nowhere in the source clause."
3. Un-hedge 61 to "the URL **is** used to discover new pages" (or cite
   利用されます) — restores source strength, harmless to the predicate.

## Axes impacted

- **Calibration (C1)**: revised wording = faithful to 巡回を推奨していない
  with refusal explicitly disclaimed — supports `met=True` at `8e408e0`.
- **Gate coverage**: refusal-implying correction passes `met=True`
  (demonstrated, exit 0) — unearned-green reachable on the meaning axis.
- **Integrity/provenance**: live mid-wave counter rewrites; receipts
  anchored to committed bytes `32b96727…` only.

No installs performed (pacman paused host-wide; none needed). Lane tree
untouched; counterexample receipts from `/tmp/c1mean` scratch repo
exercising the committed counter code path.
