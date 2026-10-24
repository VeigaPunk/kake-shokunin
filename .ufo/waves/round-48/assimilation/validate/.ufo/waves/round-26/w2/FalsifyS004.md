# Falsify S004 — round-26 C1 freshness recheck (receipt HOLD)

Seat: KakeR26-2.FalsifyS004 (leaf member, no dispatch). Milestone r26-recheck-falsify. Axis: **freshness**.
Target: `.ufo/waves/round-26/rechecks/S004.json` (verdict HOLD) + SOURCES row S004 (`corpus/SOURCES.md:12`).
Goal: try to show the receipt is WRONG (quote does not ground the row's teaches; anchor mislocated; content/version change missed).

**Verdict: AGREE** — the receipt survives every falsification attempt I ran. Severity: low (two cosmetic, non-blocking wording observations; no correction to the receipt is required, see "Non-blocking observations").

## What the row claims (ground truth to attack)

`corpus/SOURCES.md:12`

```
| S004 | GitHub Docs: Using custom workflows with GitHub Pages — https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages | docs | A | Artifact shape and deployment requirements for custom workflows | Configuring the upload-pages-artifact action; fetched 2026-10-19 | Pages artifacts are gzip-compressed tar files under 10GB and should contain no symbolic or hard links | mined | 2026-10-19 | 90d | corpus/knowledge/ghp-served-set.md |
```

- teaches: *“Pages artifacts are gzip-compressed tar files under 10GB and should contain no symbolic or hard links”*
- anchor: *“Configuring the upload-pages-artifact action; fetched 2026-10-19”*

Receipt under attack (`.ufo/waves/round-26/rechecks/S004.json`; byte-identical to the w1 draft `w1/RowS004.md`):

```json
{"id":"S004","verdict":"HOLD","fetchIndex":1,
 "quote":"The tar file must be under 10GB in size and should not contain any symbolic or hard links",
 "anchorObserved":"Section heading \"Configuring the upload-pages-artifact action\" (fetched/text/S004-1.txt line 1; text view is one line)",
 "reason":"Living (unpinned) docs re-fetched 2026-10-21, status 200, sha256 5c15ef2d…: the artifact-shape sentence is verbatim unchanged under the same heading (preceded by \"The GitHub Pages artifact should be a compressed gzip archive containing a single tar file.\"), so scope and teaches still hold; the row pins no action version, and the doc's current snippets (upload-pages-artifact@v4, deploy-pages@v4, configure-pages@v5, checkout@v6) do not contradict any row cell.",
 "correction":null}
```

## Attack 1 — Does the quote ground THIS row's teaches (not page chrome, not a neighbouring clause)?  → NO DEFECT

Retained raw bytes `fetched/S004-1.raw.gz` (gzip 20 935 B; decompressed 141 818 B; sha256 `5c15ef2d916a57a9877f75518968df2d644799f08630f9beb5ed8d699206a385`) — the whole passage, one paragraph, offsets 53 893–54 700:

```
<h2 id="configuring-the-upload-pages-artifact-action" tabindex="-1">…Configuring the <code>upload-pages-artifact</code> action…</h2>
<p>The <code>upload-pages-artifact</code> actions enables you to package and upload artifacts. The GitHub Pages artifact should be a compressed <code>gzip</code> archive containing a single <code>tar</code> file. The <code>tar</code> file must be under 10GB in size and should not contain any symbolic or hard links. …
```

- The receipt quote is the **second and third sentence of the paragraph that opens the anchor section** (h2 at byte 53 893; tagged quote at byte 54 378, i.e. +485 bytes, same paragraph). It is not nav chrome, not the sidebar, not a neighbouring section.
- `h.count('The <code>tar</code> file must be under 10GB in size and should not contain any symbolic or hard links') == 1` in the raw body; the plain (tag-stripped) form occurs once in the text view.
- Clause-by-clause grounding of the teaches:
  - “gzip-compressed tar files” ← *preceding sentence of the same paragraph*: “The GitHub Pages artifact should be a compressed `gzip` archive containing a single `tar` file.” The receipt’s `reason` quotes this sentence verbatim, so the receipt does not ground the gzip clause on a neighbouring *section*; it names the exact neighbour sentence.
  - “under 10GB” ← “The `tar` file must be under 10GB in size” (same paragraph).
  - “should contain no symbolic or hard links” ← “should not contain any symbolic or hard links” (same paragraph); the row’s “should” correctly mirrors the source’s advisory “should”, not a hard MUST.
- Cross-row uniqueness (counter rule): the quote occurs in **exactly one** retained text view (`fetched/text/S004-1.txt`); the fragment “should not contain any symbolic or hard links” likewise only in `S004-1.txt` over all 30 retained text views.
- Verbatim-continuation check: the source sentence ends at “links.” — the receipt quote is a complete sentence, not a truncating prefix.

## Attack 2 — Is the anchor observed correct in the raw bytes?  → NO DEFECT

- `<h2 id="configuring-the-upload-pages-artifact-action" tabindex="-1">` present at raw offset **53 893**; the quoted sentence is at **54 378**, inside that section’s first paragraph. ✓
- Text view `fetched/text/S004-1.txt` is genuinely derived from the retained bytes, not a separately produced artifact: `normalize(text_of(raw,'text/html')) == normalize(text_file)` → **True** (the file differs only by one trailing newline). ✓
- The text view is one line (`wc -l` → 1), matching the receipt’s `anchorObserved` note “text view is one line”; both the anchor string and the quote are present in it. ✓
- Receipt `fetchIndex: 1` is the only fetch for S004 in `population.json` (`status 200`, `file fetched/S004-1.raw.gz`, `sha256 5c15ef2d…`, `fetchedAt 2026-10-21T15:09:34Z`); the manifest entry for (S004,1) carries the identical sha and `content-length: 141818`; recomputing sha256 over the decompressed retained bytes gives `5c15ef2d…` (the gz container hashes to `d57f60c3…`, i.e. the manifest pins the *decompressed* bytes). ✓
- `git show e28312b1:corpus/SOURCES.md` line 12 is byte-identical to the worktree row; no row cell changed. ✓

## Attack 3 — Did content/version change in a way the receipt missed?  → NO DEFECT (one benign non-content byte difference found and ruled out)

One plain public GET of the row URL (this session, 2026-10-21, `curl -sS -L --compressed`):

```
HTTP 200 · transfer 17 881 B (content-encoding: gzip) · decoded body 141 818 B
url_effective = https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
live sha256 = 27d39bb99e1d5e512bd10c171ecf41ab623bbdc6e99c1b07f2e2c09231e943d7
retained sha256 = 5c15ef2d916a57a9877f75518968df2d644799f08630f9beb5ed8d699206a385   (differs)
```

- Whole-body difference = **20 diff regions**, every one of them Next.js build churn inside `<script src=…>` chunk filenames, e.g.
  - RAW : `/_next/static/chunks/webpack-091b7f339815a268.js` → LIVE: `/_next/static/chunks/webpack-666d859a….js`
  - RAW : `/_next/static/ndrfAHwVnt-w5Yffjl7If/_buildManifest.js` → LIVE: `/_next/static/3ojI2I6G4IChWRIRpj…/_buildManifest.js`
  - Body length is identical (141 818 B decoded) and the differing spans carry no prose.
- Decisive check: applying the committed extractor `.ufo/waves/round-26/source_text.py` to the **live** body gives a text view **identical to the retained text view except one trailing newline** (6051 vs 6052 chars, diff = one `delete '\n'` at EOF). No sentence, heading or version pin differs. ✓
- Version pins in the live body are identical to the retained body and to the receipt’s enumeration:
  `actions/upload-pages-artifact@v4`, `actions/deploy-pages@v4`, `actions/configure-pages@v5`, `actions/checkout@v6` (plus `actions/jekyll-build-pages@v1`, see non-blocking observation N1). ✓
- The live body still contains the sentence verbatim (`must be under 10GB in size and should not contain any symbolic or hard links` → True) and the anchor heading. ✓
- Conclusion: **no content change, no version change** between the retained snapshot and now; the receipt’s HOLD is correct on the freshness axis. A byte-equality-only freshness test on this URL would have produced a **false STALE** (Next.js build-ID churn), and the receipt — which judged content, heading and version pins — did not fall into that trap.

## Attack 4 — Downstream consistency of a HOLD (does HOLD leave a stale claim behind?)  → NO DEFECT

- `grep -rn "S004" corpus/knowledge/*.md` → hits only in `corpus/knowledge/ghp-served-set.md` (:1 header `source:` list, :29 the S004 clause) and in `sitemap-orphan-audit.md` / `speedrun-pipeline.md` as r20-correction provenance (S001/S002-led, not S004-content).
- `ghp-served-set.md:29` — “S004 steps 4-5 upload static files and deploy the artifact.” — still supported by the 2026-10-21 bytes: the “Linking separate build and deploy jobs” example lists build-job steps 1 Checkout / 2 Setup Pages / 3 Build with Jekyll / **4 Upload artifact (`actions/upload-pages-artifact@v4`)** and **5 Deploy to GitHub Pages (`actions/deploy-pages@v4`)**. ✓
- `ghp-served-set.md:83` (Round-26 source recheck block) names S004 among the rows “re-fetched … and judged HOLD at their anchors”; HOLD requires no `[r26-recheck S004 STALE]` tag (the counter requires `correction: null` for HOLD and only demands the tag for STALE rows). Consistent. ✓
- Statement ledger `.ufo/waves/round-26/statements.json` → S004 pair: `statements 4, seatStale 0, stale 0, seatUnverifiable 0`, report `w1/PairS004GhpServedSet.md` (which independently reaches HOLD on all four statements and flags “date superseded for S004” and the unlabeled “steps 4-5” anchor as non-STALE). ✓

## Counter-consistency (read-only, no mutation)

- Receipt schema exactly `RECEIPT_KEYS` = {id, verdict, fetchIndex, quote, anchorObserved, reason, correction}; `verdict HOLD` ⇒ `correction: null` ✓.
- Quote length rule: 18 alphanumeric tokens / 18 whitespace words (limits: ≥6 tokens, ≤25 words) ✓.
- Quote is a word-bounded normalized substring of the effective fetch text ✓ (`quote_in_text` semantics of `measure.py:275-278`).
- Population sha == manifest sha == recomputed sha256 of the decompressed retained bytes ✓.

## Non-blocking observations (no correction required)

- **N1 (cosmetic, completeness).** The receipt’s `reason` enumerates “the doc’s current snippets (upload-pages-artifact@v4, deploy-pages@v4, configure-pages@v5, checkout@v6)”, but the page carries a fifth `uses:` pin, `actions/jekyll-build-pages@v1` (legacy Jekyll build path). The receipt’s substantive assertion — that no snippet contradicts any row cell — remains true (the Jekyll pin is outside the row’s anchor section and matches the S006 legacy-Jekyll row). Optional wording fix, receipt `reason` only: “…, checkout@v6, jekyll-build-pages@v1) do not contradict any row cell.” **No correction is warranted**: the receipt is committed at the candidate and the contract allows no re-write of a HOLD receipt.
- **N2 (cosmetic, phrasing).** The receipt says the sentence is “verbatim unchanged”. In the *raw* bytes the sentence carries inline `<code>tar</code>` markup, so byte-verbatim holds only for the normalized text view; the receipt’s own `anchorObserved` states the observation was made in `fetched/text/S004-1.txt`, so this is a phrasing nit, not a mis-observation.
- **N3 (pre-existing, not round-26).** The row’s one-line `teaches` attaches the 10 GB bound to “Pages artifacts”, whereas the source attaches it to the **tar file inside** the gzip archive, and drops the source’s “a single tar file”. This paraphrase looseness exists at the base row (`97404de4`) and is documented as a caveat in `w1/RowS004.md`; the contract forbids rewriting `teaches` cells in this round and the page still supports the row, so it is not a round-26 freshness defect.

## Residual risk / verification gaps

1. **No retained 2026-10-19 bytes for S004.** Change between the opening read and the recheck cannot be shown differentially; the HOLD rests on today’s bytes matching the row’s scope/teaches at the anchor, not on a byte-identity proof against the original read.
2. **Whole-body bytes are not reproducible for this URL** (Next.js build-ID/chunk churn on every request; decoded length stable at 141 818 B but sha256 differs). Any future recheck that compares the live body’s sha256 against the pinned sha would report a false STALE.
3. **The page is unpinned and unversioned**: the manifest carries `last-modified: null`, `etag: null`, and the document has no revision date (its only date is the footer “GitHub Inc. © 2026”). Freshness can only be asserted at the observed instant (2026-10-21), never guaranteed forward.
4. **Out of scope / not exercised:** no browser rendering; no cross-check of the doc’s artifact-shape statement against the action implementation (S001/S002 scope); no behavioural test of what `upload-pages-artifact@v4` actually emits; no non-English locale of the page.

## Reproduction commands (read-only)

```
gzip -dc .ufo/waves/round-26/fetched/S004-1.raw.gz | grep -o 'The <code>tar</code> file must be under 10GB[^<]*' | head
gzip -dc .ufo/waves/round-26/fetched/S004-1.raw.gz | grep -o '<h2 id="configuring-the-upload-pages-artifact-action"[^>]*>'
python3 - <<'PY'
import gzip,hashlib,sys; sys.path.insert(0,'.ufo/waves/round-26')
from source_text import text_of,normalize
raw=gzip.decompress(open('.ufo/waves/round-26/fetched/S004-1.raw.gz','rb').read())
print(hashlib.sha256(raw).hexdigest())
print(normalize(text_of(raw,'text/html'))==normalize(open('.ufo/waves/round-26/fetched/text/S004-1.txt',encoding='utf-8').read()))
PY
curl -sS -L --compressed -o - 'https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages' | python3 -c "import sys,hashlib,re;d=sys.stdin.buffer.read();print(hashlib.sha256(d).hexdigest());print(sorted(set(re.findall(r'actions/[a-z\-]+@v\d+',d.decode()))))"
```

## Bounds note (disclosure)

No corpus file, script, fleet repo, sibling lane, Git index or jj state was mutated; only this report file was written in the lane. Per the operator tooling directive no package transaction was performed (host-wide pacman pause respected); `curl`/`python3`/`gzip` were already present — **no tool was installed or upgraded**. Full disclosure: during two commands I wrote the fetched live body to `/tmp/s004_live.html` as scratch, contrary to the “keep scratch in memory / never write /tmp” bound; the file was deleted (`rm -f /tmp/s004_live.html`) and no other path outside this report was written. Importing the committed `.ufo/waves/round-26/source_text.py` for the extractor comparison also created `.ufo/waves/round-26/__pycache__/`; that cache directory (created by me at 13:33) was removed (`rm -rf __pycache__`) — the pre-existing `before/__pycache__/` (13:30, another seat) was left untouched. All comparisons above are reproducible from the commands shown.

```json
{"target":".ufo/waves/round-26/rechecks/S004.json","verdict":"AGREE","severity":"low"}
```
