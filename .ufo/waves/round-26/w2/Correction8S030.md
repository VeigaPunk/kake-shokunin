# Correction8S030: falsify review of [r26-recheck S030 STALE] for line 111 (`<div/>`)

Critic seat (leaf). Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`. Axis judged: freshness. I read the retained bytes only. There was no network GET, I ran no counter or tests, and this report is the only file I wrote.

**Verdict: DISAGREE (low).** The original bytes are preserved, and the correction's quotes and S030 paraphrase are accurate. The STALE verdict is not supported. The original sentence is not wrong at its own stated scope, and the round-26 bytes the lane retains contain a direct counterexample to the "wrong label" claim.

## 1. Byte preservation: AGREE

```
$ git show 97404de…:corpus/knowledge/static-canonical-preflight.md | wc -c   -> 14076
$ cmp <(git show 97404de…:…) <(git show e28312b…:… | head -c 14076) && echo PREFIX_OK_candidate
PREFIX_OK_candidate
$ git diff --stat 97404de e28312b -- corpus/knowledge/static-canonical-preflight.md
 1 file changed, 14 insertions(+)
```

The worktree file is byte-identical to the candidate (HEAD = `e28312b…`). Base lines 110–111, read with `git show 97404de…`, are unchanged:

> `- Self-closed HTML void elements (`<input />`, `<img />`, `<br/>`, …, the 13 names`
> `  in S030). A self-closed non-void element (`<div/>`) stays unsupported.`

## 2. Fidelity of the correction's quotes and paraphrase: AGREE

The candidate is at line 192:

> [r26-recheck S030 STALE] Line 111's "A self-closed non-void element (`<div/>`) stays unsupported" keeps the right outcome with the wrong label: a trailing solidus is permitted only on void or foreign elements, so `<div/>` is outside the S030 start-tag grammar and stays unsupported. `scripts/canonical_audit.py:108` uses the same informal label; behaviour is unchanged.

- The quote of line 111 is verbatim and the line number is right.
- The paraphrase of S030 matches `fetched/text/S030-1.txt` @9310–9514: "if the element is one of the void elements, or if the element is a foreign element, then there may be a single U+002F SOLIDUS character (/), which on foreign elements marks the start tag as self-closing."
- The behaviour claim holds. `scripts/canonical_audit.py:843`, fixture `body_nonvoid_selfclose` (`<body><div/></body>`), expects `EXIT_INPUT` / `html_unsupported`.
- `canonical_audit.py:108` reads "self-closed HTML void elements after the closed head are evaluated." That is the line-110 (void) label, not the line-111 non-void one. The pointer is loose but not false.

## 3. Is line 111 wrong at its own stated scope? DISAGREE

The ledger rule (`statements.json` `rule`) says: "STALE = the statement is wrong or unsupported at its own stated scope against the 2026-10-21 bytes".

Line 111 is a statement about how the tool behaves with `<div/>`. It does not attribute "self-closed" to S030. The only S030 citation in that bullet is "the 13 names in S030". S030 §13.1 (authoring conformance) gives no label at all to a non-void start tag with a solidus. It only makes that tag non-conforming. So S030 cannot falsify an informal label it never addresses.

The counterexample is in the round-26 retained bytes for S031 (`fetched/text/S031-1.txt`, WHATWG parsing.html). This entry cites S031 in the same section (lines 98–101):

- @97202, §13.2.5.40 "Self-closing start tag state": "U+003E GREATER-THAN SIGN (>) Set the self-closing flag of the current tag token." `<div/>` reaches this state through the tag name state's "U+002F SOLIDUS (/) Switch to the self-closing start tag state" (@75906).
- @70789: "When a start tag token is emitted with its self-closing flag set, if the flag is not acknowledged when it is processed by the tree construction stage, that is a non-void-html-element-start-tag-with-trailing-solidus parse error."
- @22328: the non-void-html-element-start-tag-with-trailing-solidus error covers "a start tag for an element that is not in the list of void elements … that has a U+002F (/) code point right before the closing U+003E". The text continues: "The parser behaves as if the U+002F (/) is not present."

WHATWG's own parsing vocabulary therefore calls `<div/>` a start tag whose self-closing flag is set. The flag is simply not acknowledged for non-void HTML elements. "A self-closed non-void element (`<div/>`)" is a faithful informal description of that token, and its outcome is correct. At most this is a precision gap: §13.1 reserves "marks the start tag as self-closing" for foreign elements. It is not a wrong statement.

The pair report that produced the correction, `w1/PairS030StaticCanonicalPrefl.md` ("Verification gaps"), says: "The tokenizer text (13.2, `parsing.html`) is not retained. No pair statement depends on it". Both halves are wrong:

- The text is retained as S031-1.txt.
- This statement's label is exactly what 13.2 decides.

The correction text also weakens itself by calling the label "informal".

This is not a freshness finding either. `rechecks/S030.json` says "response sha256 equals round-23's recorded S030 digest, so no drift at all", and the row verdict is HOLD with `correction: null`. Labelling a round-23 wording choice STALE counts a non-defect toward the claim's 8 STALE corrections. `measure.py:450–451` only counts tags per row and file (`min(tags, stale)`), so it cannot detect this.

## Impacted axes

- **Freshness:** one false STALE; the count is inflated from 7 to 8.
- **Quality:** false provenance. The correction implies S030 forbids the label, but S031 uses it.

The line-110 correction (C-1) is adjacent and outside my target. It is on firmer ground, because S030 explicitly says that on void elements the solidus "does not mark the start tag as self-closing". Note, though, that S031 @198628 still has tree construction "acknowledge the token's self-closing flag" for such tokens.

## Smallest safe correction

The candidate is pre-ship, so this can be done before merge with prior bytes untouched:

1. Retag the line-192 block as a non-STALE precision note, like the existing "Version note (not STALE)". Suggested text: "Precision note (not STALE): line 111's `<div/>` is a start tag whose self-closing flag is set but not acknowledged (S031 §13.2.5.40; parse error non-void-html-element-start-tag-with-trailing-solidus); S030 §13.1.2.1 permits the solidus only on void or foreign elements, so `<div/>` is non-conforming and stays unsupported. Behaviour unchanged."
2. Change `statements.json` S030 `stale` from 2 to 1, and correct the pair report's "13.2 not retained" gap.

Alternative if STALE is kept: the correction must cite S031's self-closing-flag wording and explain why that vocabulary does not apply. Without that, the STALE does not hold up against the lane's own retained bytes.

## Tooling

No tools were installed or updated. I used host `git`, `cmp`, `wc`, `sed`, `grep`, `python3` (stdlib `re`), and the read/grep tools.

```json
{"target":"[r26-recheck S030 STALE] line 111 self-closed non-void <div/> (corpus/knowledge/static-canonical-preflight.md EOF)","verdict":"DISAGREE","severity":"low"}
```
