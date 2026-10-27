# ReviewerQualityHarm — round 63 quality-trend harm review

Seat item: per `/home/vgpnk/Projects/shokunin/LEARNING.md`, an admitted entry failing its bar is harm
(expansion table: "an admitted entry fails the bar it was admitted under"; quality table: "an entry
is found false or stale and left unmarked"). Scoped checks: (a) diff every corpus file
`base..measured` and judge each hunk for silent weakening of an existing entry, criterion or lesson;
(b) confirm the old c62 counter and its receipts remain committed as defect history.

Revisions: base `13d4519818db28cd0aa912e49020659140d7b9fa` → measured
`05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`; `git merge-base --is-ancestor` confirms base is a strict
ancestor. Repo root `/home/vgpnk/Projects/shokunin/kake-shokunin` (the diff below covers the whole tree).

## Verdict: NO quality-trend harm confirmed

## Evidence

### 1. The corpus diff is pure append — zero deleted lines

`git diff 13d4519 05b0d7f -- corpus/` yields **0** `-` lines (verified by counting `^-[^-]`); name-status
shows only `M`/`A`, no `D`/`R`. Three corpus files touched:

| File | Change | Judgment |
|---|---|---|
| `corpus/QUALITY.md` | +4 (new `## Round-63 criteria` section, one criterion) | Append-only; the round-62 criterion above is byte-identical (pure context in the hunk). The new criterion — a frozen counter's `resolved` predicate binds semantic evidence, not marker strings — is orthogonal to all quote/citation criteria; it rewrites or softens none. It cites its grounding per LEARNING.md (round-62 routed defect receipt `.ufo/waves/round-62/controls/counter-false-green-l1.txt`; `corpus/lessons/round-63.md` §Mistakes). It declares no supersession and needs none — nothing it overlaps was replaced. |
| `corpus/knowledge/response-header-expectations.md` | +29 (new `## Round-63 correction` section) | Pure append after line 219. The round-62 `[r62-correction]` held block is preserved **verbatim** above the r63 block (the whole file differs only by the tail append). Entry header (`source:`/`verified-at:`/`recheck:`) unchanged — `verified-at: 2026-10-27` predates this round and is backed by the lesson's recorded live GET. |
| `corpus/lessons/round-63.md` | new (+69) | Contains `## Mistakes` (the c62 marker-only false-green honestly recorded with receipt evidence), `## Gate` (1 admit, 2 rejects with reasons, assimilation none), and the required outside-verdict record: the round-61 non-author `Disagree` (`corpus/lessons/round-61-verifier-spotcheck.md:33`) quoted, plus the explicit author-side label: "This round's own gate decisions … are lane self-assessment, author-side". No prior lesson is retracted or softened; the round-62 rejects are "kept rejected". |

### 2. The admitted entry clears the bar it was admitted under

The r63 correction admits the S432 field-purpose span classed `collapsed-only` "under the round-50
quote-class rule (`corpus/QUALITY.md`)". Verified against that bar:

- `corpus/QUALITY.md` round-50 criterion (unchanged at measured, lines ~1099–1108) defines the class by
  derivation: "a span that is a substring of the retained HTML is `raw-substring`, a span that survives
  only whitespace collapse is `collapsed-only`". Its committed operationalization —
  `.ufo/waves/round-50/c50_quote_class.py` R2 — is binding: "collapsed-only when it is a substring of the
  text blob only." The r63 class, the ledger, and `scripts/quote_class.py` (selftest case
  `markup_collapsed_only` → `collapsed-only`) all use this same derivation. Consistent vocabulary, no
  reinterpretation.
- Digests re-derived from committed bytes at measured and match the ledger and the r63 correction:
  raw `.ufo/waves/round-61/sources/S432.html` sha256 `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`;
  flat text `.ufo/waves/round-63/quote-class/S432.txt` sha256 `8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69`;
  ledger `.ufo/waves/round-63/quote-class/quote-classes.json` sha256
  `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d` (contract-frozen).
- Span presence: `git show 05b0d7f:.ufo/waves/round-63/quote-class/S432.txt | grep -c 'response’s
  `Content-Type` header against the destination'` → 1; the ledger and entry both record it is *not* a
  raw substring — the honest-label falsifier holds.
- The round-62 criterion (substantive support, field-purpose kept separate from value rule) is
  satisfied, not weakened: the quoted sentence *is* the field-purpose proposition, and the r63 text
  explicitly keeps it "separate from the `nosniff`-only value rule per the round-62 criterion".

### 3. Nothing false or stale left unmarked

The only spans ever found non-evidencing (the fragment ending before its object; the generic lead-in)
are marked inside the same entry by both the verbatim r62 block and the r63 block ("remain historical
text and ground nothing"; the lesson's Gate rejects them again). The entry is therefore marked at file
level — the harmed-trigger does not fire.

### 4. Defect history preserved — old c62 counter and receipts committed, untouched

`git diff 13d4519 05b0d7f -- .ufo/waves/round-62/` produces **0 lines of diff** — the entire round-62
subtree is byte-identical at measured. `git ls-tree -r 05b0d7f -- .ufo/waves/round-62/` lists
`c62_calibration.py`, `contract.md`, all controls including `controls/counter-false-green-l1.txt`, the
`controls/false-green-fixture/corpus/` marker-only fixture, and all 65 w1 seat reports. Documented, not
repaired in place and not deleted — exactly as the QUALITY.md falsifier states.

### 5. Registry untouched

`corpus/SOURCES.md` does not appear anywhere in the `base..measured` name-status. The S432 row verified
at measured (line 178): `| S432 | WHATWG Fetch … | mined | 2026-10-27 | 180d |
corpus/knowledge/response-header-expectations.md |` — `status`/`recheck`/`used-by` cells as required,
matching the lesson's "No registry row added or changed".

## Residual observations (not harm)

1. **Prose looser than operationalization (pre-existing).** The round-50 criterion's words say
   "survives only *whitespace* collapse"; the admitted span survives *markup* collapse (inline
   `<code>`/element boundaries; the text blob is a textContent-semantics flat rendering). The binding
   derivation in the committed c50 counter ("substring of the text blob only") has always covered this
   case, so the round-50 bar is unchanged — but if the lane wants the prose to match its
   operationalization, a future criterion row naming the round-50 row would close the gap. Not a
   round-63 weakening: the rule text is byte-identical and the operational class is the one applied.
2. **Section-local readability.** The `xcto_nosniff_value` section body still renders the two rejected
   spans as bare blockquotes (identical to base); a reader of that section alone, without the appended
   correction blocks, could misread them as grounding. The entry-level marking exists, so LEARNING.md's
   "left unmarked" harm does not apply; an inline strikethrough or `[rejected]` annotation would be the
   conservative upgrade. Unchanged from base; flag only.

## Commands used (all read-only)

```
git diff --stat / --name-status 13d4519 05b0d7f   # corpus + whole tree
git diff 13d4519 05b0d7f -- corpus/QUALITY.md corpus/knowledge/response-header-expectations.md
git diff 13d4519 05b0d7f -- .ufo/waves/round-62/ | wc -l        # → 0
git ls-tree -r --name-only 05b0d7f -- .ufo/waves/round-62/
git show 05b0d7f:<blob> | sha256sum                            # four blobs, all match
grep -n 'collapsed-only' corpus/QUALITY.md; sed -n '1088,1108p'
git merge-base --is-ancestor 13d4519 05b0d7f                   # → true
```

No installs; no writes outside this report; no fixture repos created.
