# Falsify S018 — round-26 C1 (freshness), author-side FALSIFY wave

**Target:** receipt `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/rechecks/S018.json` (verdict `HOLD`)
**Row:** `corpus/SOURCES.md:26` — S018, DebugBear "Firefox And Safari Now Support Two Core Web Vitals Metrics", tier C, scope "Firefox version and date for interactionId and INP support", anchor "INP support in Firefox 114; updated 2026-03-19", teaches "REJECTED: DebugBear says Firefox 114, while Firefox 144.0 release notes carry interactionId; flip: a tier-A source confirms its number", status `rejected`, recheck `180d`, used-by `—`
**Bytes:** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/fetched/S018-1.raw.gz`, text view `.../fetched/text/S018-1.txt`
**Candidate:** `e28312b14b076584fedd696fae2a684e460bd11e` (base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`)

**Verdict: AGREE** (severity `none`). I could not falsify the HOLD on any of the three attack axes. Two non-blocking observations are recorded as residual risk, not as findings.

---

## Attack 1 — Does the quote really ground THIS row's teaches (not page chrome, not a neighbouring clause)?

**Result: grounded, and row-specific.**

Receipt quote (`.ufo/waves/round-26/rechecks/S018.json:5`):

> "Mozilla released version 114 of Firefox on the 14th of October 2025. It added support for the interactionId property that's needed to measure INP"

Both sentences live in the same `<p>` element immediately under the row's anchor heading, in the retained raw bytes:

```
$ python3 - <<'EOF'   # gzip -dc S018-1.raw.gz, region 22080..22560
<h2 class="anchor anchorWithStickyNavbar_FNw8" id="inp-support-in-firefox-114">INP support in Firefox 114<a href="#inp-support-in-firefox-114" …></a></h2>
<p>Mozilla released version 114 of Firefox on the 14th of October 2025. It added support for the <code>interactionId</code> property that&#x27;s needed to measure INP.</p>
```

- It is the Firefox paragraph, not the neighbouring clause. The adjacent `h2` is `id="lcp-and-inp-support-in-safari-262"` ("LCP and INP support in Safari 26.2", whose body reads "Apple released Safari 26.2 on the 12th of December 2025"); the following element is the `info` admonition "Firefox has already supported LCP since January 2024". The quote is neither.
- It is not page chrome: it is body prose carrying version + date + `interactionId`/INP, i.e. exactly the row's declared scope "Firefox version and date for interactionId and INP support".
- Row-specificity holds against every other row in the wave (the counter's own `quote_not_row_specific` rule). Independent re-run over all 32 population rows' text views:

```
rows whose text contains S018 quote: [('S018', 1)]
```

- Counter admissibility holds: 25 alphanumeric tokens ≥ 6, 24 whitespace words ≤ 25, and word-bounded match in the effective fetch text:

```
quote_in_text: True
quote tokens/words: 25 24
```

## Attack 2 — Is the anchor observed correct in raw bytes?

**Result: correct on every component.**

| Receipt claim (`rechecks/S018.json:6`) | Raw-byte evidence in `S018-1.raw.gz` |
|---|---|
| h2 "INP support in Firefox 114" with anchor `#inp-support-in-firefox-114` | `id="inp-support-in-firefox-114"` at raw offset 22100; heading text at 22132/22241/22291 |
| body "immediately after the heading" | `</h2>\n<p>Mozilla released version 114 …` — the `<p>` is the very next element after the `</h2>` (raw 22333) |
| byline "December 15, 2025 · Updated on March 19, 2026" | `<span>December 15, 2025</span> · <!-- -->Updated on<!-- --> <time datetime="2026-03-19T10:53:34.000Z" itemprop="dateModified">March 19, 2026</time> · <!-- -->4 min read` (raw 19269–19421); the literal string is contiguous in the canonical text view at offset 757, and `dateModified`/`article:modified_time` both carry `2026-03-19T10:53:34.000Z` — this is what grounds the row's anchor cell "updated 2026-03-19" |
| "text view is one extracted line, quote at char offset 1545" | text view is a single content line (`newlines 1`, 6200 chars incl. trailing `\n`); `text.find(quote) == 1545` |

The quote is not verbatim in the *raw* HTML (the `<code>` boundary and `&#x27;` intervene), but the receipt explicitly scopes its quote and offsets to the text view, which is the canonical extraction (`source_text.py`, single decode — `HTMLParser(convert_charrefs=True)`). Re-deriving the view from the retained gzip reproduces the committed text file byte-for-byte modulo the trailing newline:

```
textview == recomputed: True 6199 6200
```

## Attack 3 — Did content/version change in a way the receipt missed?

**Result: no change; live bytes are identical to the retained bytes.**

One plain GET of the row URL (the only URL the receipt names, already in `corpus/SOURCES.md:26`), compared against the retained gzip:

```
$ curl -sS -A "Mozilla/5.0 (X11; Linux x86_64) kake-recheck" https://www.debugbear.com/blog/firefox-safari-web-vitals | python3 -c "…"
live bytes 55919 retained bytes 55919
sha256 live     21a3e87351b4a621bafeb7a0caeabb5845dc9bbb89613156383798d7bf2a9045
sha256 retained 21a3e87351b4a621bafeb7a0caeabb5845dc9bbb89613156383798d7bf2a9045
BYTE IDENTICAL: True
live sha == manifest sha: True
```

A `difflib.SequenceMatcher` over the two documents reports **zero** differing opcodes. The retained gzip also matches its own manifest entry exactly (`sha256(decompressed) == manifest.sha256 == 21a3e873…`, `bytes 55919 == decompressed len 55919`), and `population.json`'s pinned sha for S018 index 1 equals the manifest sha.

Nothing in the page has been corrected or re-versioned:

```
'Firefox 114'  22147 / 22256 / 22306 / 51865     (heading, body, ToC)
'version 114'  22350
'144.0' []   'firefox.com' []   'releases.mozilla.org' []   'Firefox release' []
```

So the tier-C number is still `114`, the update stamp is still `2026-03-19`, and no `144`/`correction`/`erratum` text has appeared. The receipt's factual claims all survive.

## Identity, routing and counter checks (no rerouting, no double runtime)

- Receipt JSON is byte-identical between the working tree and the candidate commit: `d4d35d425755e116a40795e943405dc7b558812ea01e0eb01a3ca0228128b8ae` from both `git show e28312b1:…/rechecks/S018.json` and the file on disk. No working-tree drift.
- Receipt JSON is identical to the JSON block in the seat report `.ufo/waves/round-26/w1/RowS018.md` (`identical to receipt: True`), i.e. the "copied unchanged from the row seat reports" claim in `corpus/lessons/round-26.md` holds for this row — same-identity, no rerouting.
- One fetch only for S018 in `fetched/manifest.json`; `manifest-retry.json` contains only the S008 retry, so there is no second runtime for this row.
- Counter at the candidate revision: `{"decided": 32, "expected": 32, "findings": [], "hold": 32, "stale": 0, "unverifiable": 0, "statements": 276, "statementsStale": 8, "statementCorrections": 8}` → exit 0. At the base revision: exit 1, `decided 0`, finding `receipts_absent` — the "before 0/32" claim in the task context reproduces. All 32 receipts in `rechecks/` are `HOLD` (no row was silently STALE).
- `corpus/SOURCES.md` diff base→candidate adds only the Round-26 note paragraph; **no SOURCES cell changed** (S018 row 26 is byte-identical), consistent with the contract's appendOnly rule.
- No knowledge file depends on S018: `grep -rln "S018" corpus/knowledge/` → empty, and the row's used-by cell is `—`. `statements.json` pairs contain no S018 entry (25 pairs, rows S001–S013 + S020–S034). So there is no laundering path by which a stale knowledge statement could ride on a row-level HOLD: nothing in the corpus states the Firefox 114 number.
- The receipt's flip-condition reasoning matches the row cell and the page: no `releases.mozilla.org` / `firefox.com` link appears in the page's external links (only Apple Safari 26.2 release notes, MDN Navigation API, the web-platform-tests interop issue, statcounter, rumarchive, web.dev/baseline, debugbear.com, LinkedIn, YouTube), and the page remains tier C/community — the flip condition is still unmet, exactly as recorded.

---

## Findings by severity

**Blocking findings: none.** No falsifiable defect in the receipt on the freshness axis.

**Low (non-blocking, recorded as residual risk only):**

1. *Tier-A comparator was outside this wave's fetch population.* The receipt's reason asserts the tier-C number "still conflicts with Firefox 144.0 release notes carrying interactionId", but `fetched/manifest.json` contains **no** `firefox.com`/`mozilla` URL (S018's population entry pins only the DebugBear URL), so the tier-A half of the conflict was not re-verified in round 26. It is nonetheless durable and unmodified: `corpus/lessons/round-20.md:220` (untouched by this wave's diff) records the tier-A quote "Firefox now supports the PerformanceEventTiming.interactionId API, allowing developers to group related input events." from Firefox "144.0 Firefox Release", "Web Platform", released 2025-10-14 — and the DebugBear date "14th of October 2025" matches 144.0's release date, so the page's version/date pair is internally inconsistent (a digit transposition), which is the substance of the rejection. The receipt's own parenthetical evidence ("no link to Firefox release notes in the page") is honestly scoped to the page it read; it simply does not cite the corpus location of the tier-A fact, which the seat report does (`w1/RowS018.md` caveat 4). No verdict impact; a citation improvement only.
2. *Byline string form.* The receipt's `anchorObserved` quotes the byline as one contiguous string; in raw HTML it is split by `<!-- -->` comment markers and a `<time>` element, and it is contiguous only in the canonical text view. The receipt names the text view as its artifact, so this is not a misquote — but a reviewer checking raw bytes for that literal will not find it. The `dateModified`/`article:modified_time` attributes (`2026-03-19T10:53:34.000Z`) are the raw-byte proof of the row's "updated 2026-03-19" anchor cell.

## Residual risk

- Single-fetch drift blindness: one fetch cannot exclude a server-side edit that leaves the `2026-03-19` stamp (noted in the seat report's caveat 2). Mitigated here but not eliminated by today's byte-identical live GET.
- The tier-A side of the rejection (Firefox 144.0 release notes) remains outside the recheck population; if that page were ever revised, the conflict and the flip condition would need re-adjudication outside this wave's URL set.

## Verification gaps (what I could not settle here, by lane bound)

- The Firefox 144.0 release-notes page was not fetched in this wave and is not a recorded URL in `population.json`; per the lane bound ("Run only commands your item names", one plain GET of the row URL only) I did not GET it. I relied on the corpus's unmodified round-20 record for the tier-A fact.
- Whether DebugBear will ever correct 114 → 144 is not decidable from retained bytes and does not affect this verdict.

## Tooling

No tool was installed or updated: this falsification needed only the preinstalled `python3` (stdlib `gzip`/`difflib`/`re`/`hashlib`), `curl`, and `git`. No pacman/uv/npm/cargo transaction was performed, so no version/channel/reason record is owed.

## Lane hygiene

Read-only against the lane: no corpus, script, fleet-repo, sibling-lane, or Git-index/jj mutation. Scratch was kept in memory; two transient `/tmp` files used for byte comparison were deleted (`/tmp/s018_live.html`, `/tmp/base_measure.txt` — both confirmed absent). `corpus/`, `.ufo/waves/round-26/rechecks/`, and `.ufo/waves/round-26/fetched/` are clean per `git status --porcelain`. The only untracked residue under `.ufo/waves/round-26/` is regenerable `__pycache__/` bytecode produced by importing the committed `source_text.py` for the text-view recomputation (it was already present before this seat and is not tracked content); I left it rather than risk a sibling's running import. This report is the only file I wrote.

```json
{"target":".ufo/waves/round-26/rechecks/S018.json","verdict":"AGREE","severity":"none"}
```
