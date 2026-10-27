# ReviewerKnowledgeEntry — round-63 w1

Scope: internal consistency of `corpus/knowledge/response-header-expectations.md`
after the round-63 append, per seat item. Read-only review; no mutations
anywhere. Reviewed file state = working tree, verified byte-identical to
measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`
(`git diff 05b0d7f4 HEAD -- corpus/knowledge/response-header-expectations.md` →
empty; `git status --porcelain` on the file → empty). Repo HEAD is
`15eb965c1d0f23ce2a522c651e9306a0952da7d3` (w1 dispatch commit, after-state
receipts only).

The round-63 append is exactly the `## Round-63 correction` block
(entry lines 222–250), added by `git diff 13d45198…05b0d7f4` — nothing else in
the file changed.

## Verdict

CONFIRMED internally consistent. No contradiction between the
`xcto_nosniff_value` section's older text (lines 69–94) and the
`[r63-correction]` block; the two old spans are unambiguously demarked as
grounding nothing; the S432 citation for the value rule remains accurate.
Three cosmetic notes below — none reach finding severity.

## Q1 — older text vs correction block: no contradiction

The old section text (lines 71–87) asserts facts that remain true:

- Both old spans are raw substrings of the retained HTML — verified:
  `"can be used to require checking of a"` at `S432.html:6152`,
  `"Web developers and conformance checkers must use the following"` at
  `S432.html:6183` (grep). The `[S432 §3.6]` citations are correct.
- The r63 block demotes their *grounding status* ("remain historical text and
  ground nothing", line 245–246) — a supersession of evidentiary weight, not a
  factual dispute. It also names the same diagnosis the r62 block already gave
  (line 220: generic lead-in; fragment ends before its object), so the file's
  own narrative is continuous.
- The block's structural claims hold against ground truth: the "node after
  the second span introduces the ABNF value block" (old text, lines 81–84) —
  `S432.html:6184` literally reads `…value ABNF for X-Content-Type-Options:`,
  and the `<pre>` at `S432.html:6187–6188` is
  `X-Content-Type-Options = "nosniff" ; case-insensitive` — one production,
  only permitted value `nosniff`, exactly as the old text paraphrases; the
  ABNF does span `<c->` element boundaries inside `<pre><code>`, so the
  "not quoted because it spans element boundaries" rationale is accurate.
- The algorithm paraphrase (old text lines 85–87) matches
  `S432.html:6174–6175`: `values[0]` ASCII case-insensitive match for
  `"nosniff"`.

The new span's claim is verified independently:

```
$ python3 -B - <<'EOF'   # substring tests on the two blobs
span (154 B) in .ufo/waves/round-63/quote-class/S432.txt : True
span in .ufo/waves/round-61/sources/S432.html            : False
EOF
```

→ `collapsed-only` is the correct derived class under
`corpus/QUALITY.md:1100–1108` (round-50 rule: class derived from the span's
own two blobs; substring of retained HTML = `raw-substring`, surviving only
whitespace collapse = `collapsed-only`; never swapped-label). The block's
shas match the files: `sha256sum` gives S432.txt =
`8b90d096…f542a69`, S432.html = `63b0a018…bad911b`, quote-classes.json =
`5f48e26b…010c42d` — all equal to the contract-frozen values, and the ledger's
`matchClass`/`locatedRawLines` entries match the block.

## Q2 — old spans demarked: yes, unambiguous

Entry line 245–246: "The two earlier spans quoted in that section — the
fragment ending before its object and the generic lead-in — remain historical
text and ground nothing." Each referent is identified by the description the
r62 block (`corpus/knowledge/response-header-expectations.md:220`) and the
spotcheck (`corpus/lessons/round-61-verifier-spotcheck.md:33`, verified line
number) already assigned to it, so there is exactly one mapping onto the two
quoted spans at lines 77–79. Demarcation is clear.

Mechanical note (not a contradiction): the demarcation lives only in the
trailing correction block; the quotes at lines 77–79 carry no in-section
pointer. Under the lane's append-only convention (contract No-harm:
"the round-62 held correction preserved verbatim above the round-63 block";
`corpus/QUALITY.md` append-only corrections) this is the expected mechanism —
a reader must read the entry to its end to learn the spans are ungrounded.

## Q3 — S432 citation for the value rule: still accurate

The audit rule (`xcto_nosniff_value`, lines 89–94) rests on the
cited-by-location ABNF (`S432.html:6187`) and algorithm
(`S432.html:6174–6175`), neither of which is among the demoted spans; the r63
block explicitly keeps the new span "separate from the `nosniff`-only value
rule" (lines 243–244). `corpus/SOURCES.md:178` still scopes the row to
"X-Content-Type-Options nosniff value rule" with a summary matching the ABNF +
algorithm facts, status `mined` — entry and registry agree, and the block's
"no registry cell changed" claim is consistent with the row's content.

## Cosmetic notes (below finding severity)

1. Line ranges for the same sentence: r62 block says `S432.html:6150–6156`,
   r63 block and ledger say `6150–6154`. Checked raw lines: 6150–6154 carry
   the sentence text; 6155 is blank, 6156 is `</p>`. r62's wider range
   contains the sentence; r63's is exact. Compatible, not contradictory.
2. Old text line 71–72 says the purpose sentence sits "in the
   response-processing steps"; it is actually the §3.6 intro paragraph
   (`S432.html:6150–6154`), with the "determine nosniff" steps starting at
   6157. Loose wording that predates the append and does not conflict with it
   (the block calls it "the field-purpose sentence of §3.6", which is
   strictly more precise).
3. r62's stated rationale — "`corpus/QUALITY.md` quote rules require
   raw-substring evidence" (line 220) — overstates the rule: QUALITY.md has
   admitted a labeled `collapsed-only` class since round 50
   (`corpus/QUALITY.md:1102–1104`). Read sequentially the blocks stay coherent
   (r62 declined a *silent normalized* substitution; r63 admits a *labeled*
   collapsed quote), but the r62 sentence alone understates the rule.

## Evidence index

- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/response-header-expectations.md:69-94` (old section), `:218-220` (r62 block), `:222-250` (r63 block), `:8` (falsifier header)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html:6149-6189` (§3.6 layout), `:6183-6188` (lead-in + ABNF), `:6174-6175` (algorithm step)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/quote-classes.json` (schema `kake-r63-quote-classes-v1`, `matchClass: collapsed-only`, `locatedRawLines: 6150-6154`, both shas matching files)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md:1100-1108` (round-50 class rule)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md:178` (S432 row, `mined`, value-rule scope)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-61-verifier-spotcheck.md:33` (S432 Disagree row)
- Commands run (all read-only): `git rev-parse HEAD`, `git log --oneline -4`, `git status --porcelain`, `git diff 13d45198..05b0d7f4` / `05b0d7f4..HEAD` on the entry file, `sha256sum` on the five frozen paths, `grep -n`/`sed -n` on S432.html, the python3 substring test above. No installs.
