# Falsify S022 — round-26 C1 freshness recheck (receipt HOLD)

Seat: KakeR26-2.FalsifyS022 (leaf member, no dispatch). Milestone r26-recheck-falsify. Axis: **freshness**.
Target: `.ufo/waves/round-26/rechecks/S022.json` (verdict HOLD) + SOURCES row S022 (`corpus/SOURCES.md:30`).
Goal: try to show the receipt is WRONG (quote does not ground the row's teaches; anchor mislocated; content/version change missed).

**Verdict: AGREE** — the receipt survives every falsification attempt I ran. Severity: none.

## What the row claims (ground truth to attack)

`corpus/SOURCES.md:30`

```
| S022 | Google Search Central: Fix canonicalization issues — https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting | docs | A | Declared canonical versus Google-selected canonical | Opening paragraph, updated 2026-08-21; opened 2026-10-20 | Google may choose a different canonical even when the publisher explicitly designates one | mined | 2026-10-20 | 90d | corpus/lessons/round-22.md |
```

- teaches: *“Google may choose a different canonical even when the publisher explicitly designates one”*
- anchor: *“Opening paragraph, updated 2026-08-21; opened 2026-10-20”*

Receipt under attack (`.ufo/waves/round-26/rechecks/S022.json`, byte-identical in the worktree and at candidate `e28312b1`):

```json
{"id":"S022","verdict":"HOLD","fetchIndex":1,
 "quote":"Even if you explicitly designate a canonical page, Google might choose a different canonical for various reasons",
 "anchorObserved":"Main-content opening paragraph under H1 \"Fix canonicalization issues\" (id=fix-canonicalization-issues); footer \"Last updated 2026-08-21 UTC\"",
 "reason":"Opening paragraph still states Google may choose a different canonical despite an explicit designation; page footer date 2026-08-21 matches the row anchor and the live Last-Modified header (Fri, 21 Aug 2026 11:28:27 GMT), so scope and teaches are unchanged.",
 "correction":null}
```

## Attack 1 — Does the quote ground THIS row's teaches (not page chrome, not a neighbouring clause)?  → NO DEFECT

Raw retained bytes `fetched/S022-1.raw.gz` (decompressed, 178056 B), line 3873–3878:

```
  <h1 class="page-title" id="fix-canonicalization-issues" data-text="Fix canonicalization issues" tabindex="-1">Fix canonicalization issues</h1>

<p>
  Even if you explicitly designate a canonical page, Google might choose a different canonical
  for various reasons, such as the quality of the content or technical signals. To troubleshoot
  canonicalization issues, follow these steps:
</p>
```

- The quote is the **first `<p>` after the H1** of the main article body — i.e. literally the “Opening paragraph” the row's anchor names.
- Byte offsets in the raw body: `devsite-article-body` starts at 137595, `<devsite-footer>` starts at 149009; H1 at 137690, quote at 137819 → the quote is inside the article body, **not** nav chrome, **not** the sidebar, **not** a neighbouring clause.
- Occurrence counts: `raw.count(b'Even if you explicitly designate') == 1`; the quote occurs **exactly once** in the retained text view (`fetched/text/S022-1.txt`), word-bounded match `True`.
- Cross-row uniqueness (counter's `quote_not_row_specific` rule): `grep -l "explicitly designate a canonical page" .ufo/waves/round-26/fetched/text/*.txt` → **only `S022-1.txt`**.
- Semantic grounding: the sentence *is* the teaches. Publisher designates a canonical → “Google might choose a different canonical”. The row's paraphrase adds nothing the source does not say, and drops nothing the source asserts (the row does not claim Google *will* choose differently, nor that a designated canonical is invalid — the source says “might … for various reasons, such as the quality of the content or technical signals”, and the row’s scope column “Declared canonical versus Google-selected canonical” is the page’s own distinction: the page links `#google-selected-canonical` and “which page Google considers canonical”).

Verbatim-continuation check (the receipt truncates the sentence at “various reasons”): the raw continues “for various reasons, such as the quality of the content or technical signals.” The truncation is a clean prefix; it does not reverse or overstate the clause.

## Attack 2 — Is the anchor observed correct in the raw bytes?  → NO DEFECT

- `id="fix-canonicalization-issues"` — present (raw line 3873; byte 137690). ✓
- “Main-content opening paragraph” — the quote is the first `<p>` of `devsite-article-body`. ✓
- “footer ‘Last updated 2026-08-21 UTC’” — raw lines 4066–4069:

```
  <devsite-content-footer class="nocontent" data-nosnippet>
  <p>Except as otherwise noted, the content of this page is licensed under the …</p>
  <p>Last updated 2026-08-21 UTC.</p>
</devsite-content-footer>
```

  The string is literally in a `<devsite-content-footer>` element (offset 146903) — “footer” is the correct element name, not a loose description. ✓
- Version marker matches the row anchor “updated 2026-08-21” (footer date = 2026-08-21, `last-modified: Fri, 21 Aug 2026 11:28:27 GMT`). ✓
- Receipt `fetchIndex: 1` is the only fetch in `population.json` for S022, with `status 200`, `file fetched/S022-1.raw.gz`, `sha256 4d42dd82db74b81329deaa0e46fc4bfdf08548894d1e437a1a2634009b173e47`. The manifest entry for (`S022`,1) carries the same sha and `last-modified: Fri, 21 Aug 2026 11:28:27 GMT`. ✓
- Retained text view is genuinely derived from the retained bytes (not a separately produced artifact): `normalize(text_of(raw))` == `normalize(fetched/text/S022-1.txt)` → **EQUAL** (both 12125 normalized chars), and the text view contains “Last updated 2026-08-21 UTC.” ✓

## Attack 3 — Did content/version change in a way the receipt missed?  → NO DEFECT (one benign, non-content byte-level difference found and ruled out)

Plain public GET of the row URL (2026-10-21 16:28:17 GMT), body compared in memory only (never written to disk):

```
HTTP/2 200
last-modified: Fri, 21 Aug 2026 11:28:27 GMT
content-type: text/html; charset=utf-8
cache-control: no-cache, must-revalidate
content-length: 178060          (body actually received: 178056 B)
```

- **Content region byte-identical.** The `devsite-article-body → devsite-footer` region (live 137595–149009, 11414 B; raw 137595–149009, 11414 B) compares **EQUAL**. Zero differing bytes at any offset < 149473.
- **Version marker unchanged** in the live body: `b'Last updated 2026-08-21 UTC.' in live → True`; `b'id="fix-canonicalization-issues"' in live → True`.
- **Whole-body sha differs, but only in footer chrome.** live sha256 `ed47024e45e8e48ee655909d70c64f1664704fcdd53439fb7a085698c7730b41` vs retained `4d42dd82db74b81329deaa0e46fc4bfdf08548894d1e437a1a2634009b173e47`; 4189 differing bytes in 302 runs, **all at offsets ≥ 149473**, i.e. after the article body ends (149009). Sampled runs are server-side ordering shuffles of footer analytics attributes and of a permalink-ordering array in an inline script, e.g.

  RAW : `…data-category="Search docs"\n … aria-label="LinkedIn feed for Google Search Central"… data-label="linkedin footer promo"…`
  LIVE: `…data-label="linkedin footer promo"\n … aria-label="LinkedIn feed for Google Search Central"… data-category="Search docs"…`

  and the tail array `[[1,1],[6,5],[3,2],…]` vs `[[1,1],[2,2]]` / `[[6,5],[13,10],…]`. The response’s own `content-length` even varied between two requests (178060 vs 178056) on identical content — i.e. the byte length is not stable, while the article content is.
- Conclusion: **no content change, no version change.** The receipt’s HOLD is correct on the freshness axis; a byte-equality-only freshness test would here have produced a false STALE, and the receipt (which judged content + version marker) did not fall into that trap.

## Attack 4 — Downstream consistency of a HOLD (does HOLD leave any stale claim behind?)  → NO DEFECT

- `grep -rn "S022" corpus/knowledge/*.md` → **no hits**; no knowledge entry cites S022, so a HOLD needs no appended “Round-26 source recheck” block or `[r26-recheck S022 STALE]` correction (the contract requires those only for STALE). Consistent with `corpus/knowledge/static-canonical-preflight.md:184`, whose round-26 list covers S020, S021, S026–S034 and correctly omits S022.
- The one citing file, `corpus/lessons/round-22.md:45`, quotes S022 with the **identical** string:
  `| S022 | …/canonicalization-troubleshooting | Opening paragraph: “Even if you explicitly designate a canonical page, Google might choose a different canonical for various reasons” |`
  → still verbatim true against the 2026-10-21 re-fetch; no stale lesson claim.
- `corpus/knowledge/static-canonical-preflight.md:1` attributes Google’s canonical guidance to **S021** (`consolidate-duplicate-urls`), not S022 — no S022-derived statement is left uncorrected by this HOLD.

## Counter-consistency (read-only, no mutation)

- The committed receipt at the candidate is byte-identical to the worktree file (`git diff e28312b1 -- .ufo/waves/round-26/rechecks/S022.json` → empty).
- Counter constraints satisfied for this receipt: quote has 17 tokens / 17 words (limits: ≥6 tokens, ≤25 words); normalized quote is a word-bounded substring of the effective fetch text; `verdict HOLD` ⇒ `correction: null` (present). No finding attributable to S022.

## Residual risk / verification gaps

1. **Whole-body bytes are not reproducible for this URL.** Chrome ordering is nondeterministic (4189 B / 302 runs differ on every request, and `content-length` itself varies: 178060 vs 178056). Any future recheck that compares the live body’s sha256 against the pinned sha would report a false STALE. The current round avoids this (it pins and compares retained bytes; content/version are judged from the article body and the footer date). Flagged as a process risk, not a defect in this receipt.
2. **No retained copy of the 2026-10-20 opening read** exists for S022, so byte identity with the original opening read is unproven; [INFERENCE] the `last-modified` date 2026-08-21 predates both the 2026-10-20 opening and the 2026-10-21 re-fetch, so both reads saw the same published version (2026-08-21).
3. The live page serves `cache-control: no-cache, must-revalidate`; freshness can only ever be asserted at the observed instant (2026-10-21 16:28 GMT), not guaranteed forward.
4. Verification gaps that remain out of scope here and were not exercised: no browser rendering, no `rel=canonical` behavioural test, no non-English locale of the page.

## Reproduction commands (read-only; the live body was never saved)

```
gzip -dc .ufo/waves/round-26/fetched/S022-1.raw.gz | grep -n -A3 'Even if you explicitly designate'
gzip -dc .ufo/waves/round-26/fetched/S022-1.raw.gz | grep -n 'Last updated 2026-08-21'
gzip -dc .ufo/waves/round-26/fetched/S022-1.raw.gz | grep -c 'explicitly designate'        # 1
curl -sS -D- -A 'Mozilla/5.0 … Chrome/124' https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting
# article-body comparison (live body piped straight into python, kept in memory)
```

## Tooling

No installs or upgrades were required; `curl` and `python3` were already present. Per the operator directive, no package transaction was performed (pacman host-wide pause respected); nothing outside this report file was written, and no corpus/script/fleet/sibling-lane state was mutated.

```json
{"target":".ufo/waves/round-26/rechecks/S022.json","verdict":"AGREE","severity":"none"}
```
