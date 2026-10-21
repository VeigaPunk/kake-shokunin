# Correction7S030 — falsify `[r26-recheck S030 STALE]` (line 110, "Self-closed HTML void elements")

Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.
Target: `corpus/knowledge/static-canonical-preflight.md:190` (candidate), the correction of base line 110.
Axis: freshness. Verdict: **DISAGREE (low)**. The bytes are preserved and the quote is verbatim. The STALE classification and the attribution "misuses S030's term" do not survive the retained bytes.

## 1. Original bytes preserved — HOLD

Command (in the lane, nothing written):

```
bl=$(git show $B:$F | wc -c)                 -> base=14076 cand=16987
git show $B:$F | sha256sum                   -> 192eac303fa3ba8a2aab9d545fe6b0627f3a174dff1b54472e1bab2f771fdaf7
git show $C:$F | head -c $bl | sha256sum     -> 192eac303fa3ba8a2aab9d545fe6b0627f3a174dff1b54472e1bab2f771fdaf7
git diff --stat $B $C -- $F                  -> 1 file changed, 14 insertions(+)
```

The worktree file sha256 (`aab1ddf5…`) equals the candidate blob. The appended tail starts `\n## Round-26 source recheck`. The base line 110 text is unchanged: "- Self-closed HTML void elements (`<input />`, `<img />`, `<br/>`, …, the 13 names / in S030)."

## 2. Verbatim quote and the 13-name claim — HOLD

- `fetched/text/S030-1.txt` (31,812 bytes) contains: "which on foreign elements marks the start tag as self-closing. On void elements, it does not mark the start tag as self-closing but instead is unnecessary and has no effect of any kind." The correction's quoted fragment "does not mark the start tag as self-closing" is verbatim. "It marks self-closing only on foreign elements" is an unquoted paraphrase, and it is accurate.
- The same text has "13.1.2 Elements … 13.1.2.1 Start tags", and the void list reads "Void elements area, base, br, col, embed, hr, img, input, link, meta, source, track, wbr". That is 13 names under §13.1.2, as the correction says.

## 3. Is the original wrong at its own stated scope? — counterexample: NO

**3a. Line 110 does not attribute the label to S030.** Its only S030 attribution is "the 13 names in S030". The word "self-closed" is the entry's own gloss for a tool behaviour (the tool evaluates these tags after the head closes), and S030 confirms that behaviour. `grep -c "self-closed" S030-1.txt` returns `0`, so S030 has no such term to "misuse". The correction's "misuses S030's term" is therefore a false attribution.

**3b. The retained bytes of the companion source make the gloss defensible.** The same Round-23 section (base lines 97–101) cites S031 (WHATWG parsing), and `fetched/text/S031-1.txt` contains this text:

- Tokenizer: "When a start tag token is emitted with its self-closing flag set, if the flag is not acknowledged when it is processed by the tree construction stage, that is a non-void-html-element-start-tag-with-trailing-solidus parse error."
- In body, for "area", "br", "embed", "img", "keygen", "wbr", and likewise for input, "param", "source", "track", base/link/meta and hr: "Insert an HTML element for the token. Immediately pop the current node off the stack of open elements. Acknowledge the token's self-closing flag, if it is set."

So in WHATWG's own parsing vocabulary, `<input />` is a start tag whose self-closing flag is set and acknowledged. `<div/>` is the case where the flag is set but not acknowledged, which is a parse error. "Self-closed void element" versus "self-closed non-void element" maps onto exactly that distinction. Only the syntax-section sense (§13.1.2.1, "does not mark the start tag as self-closing") conflicts with the label. The original is a terminology tension between two sections of one standard. It is not a claim that the bytes falsify. The w1 Pair report admitted that 13.2 "is not retained", but S031-1.txt is 13.2 and it is retained in this same round (`fetched/text/S031-1.txt`, 280,206 bytes). The w1 verdict skipped that evidence.

**3c. Nothing went stale.** The S030 row receipt (`rechecks/S030.json`) says `"verdict": "HOLD"` and `"correction": null`, with the reason "response sha256 equals round-23's recorded S030 digest, so no drift at all". The w1 Pair report agrees: "The two STALE items predate this recheck". Base line 151 already states the syntax-level reading: "This is not an XML-style self-closing element (w2/ReopenS030)". The w1 draft C-1 said "Line 151 gives the same reading", but the admitted text at line 190 drops that cross-reference. Under the freshness criterion, tagging a round-23 wording choice as `[r26-recheck S030 STALE]` asserts a staleness that the row's own receipt denies. The admitted correction also duplicates an existing in-entry caveat without pointing to it.

**3d. Duplicate-authority side effect.** The same label remains uncorrected in `corpus/SOURCES.md:38` ("Self-closing slash on void and foreign elements") and `:52` ("accept void self-closing"), and in `scripts/canonical_audit.py:108` ("self-closed HTML void elements"). Only the line-111 bullet mentions the script. If the STALE reading were right, the corpus would now hold two conflicting authorities for one term.

## Impacted axes

- Freshness: a STALE verdict without drift, issued against a row receipt that says HOLD.
- Provenance: "misuses S030's term" attributes to S030 a term it never uses.
- Duplicate authority: the correction overlaps the existing line-151 caveat without citing it.

Byte preservation and quote fidelity are unaffected.

## Smallest safe correction

Replace the line-190 text with a precision note that keeps the existing tag, so the counter's ledger stays satisfied, or have the judge reclassify the statement from stale to a note (`statements.json` S030 `stale` 2→1 for this item). Either way the wording should be:

> `[r26-recheck S030 STALE]` Line 110's "Self-closed" is the tokenizer gloss (S031: a trailing solidus sets the token's self-closing flag, which tree construction acknowledges for void elements). In S030 §13.1.2.1 syntax terms the solidus on a void element "does not mark the start tag as self-closing" and has no effect; line 151 already gives this reading. The 13 names (§13.1.2) and the tool behaviour are unchanged.

## Tooling

No tools were installed or updated. I used only `git show`, `wc`, `sha256sum`, `head`, `od`, `grep` and `sed` from the host, plus file reads. I made no network GET.

```json
{"target":"corpus/knowledge/static-canonical-preflight.md:190 [r26-recheck S030 STALE] (base line 110)","verdict":"DISAGREE","severity":"low"}
```
