# ExecQuoteRawScan — every entry quote classified against its retained body

Seat: `L1Kake51.ExecQuoteRawScan-2` · Round 51 wave 1 · read-only except this file.
Revision measured: lane tip `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (working tree clean for
the two entries; bodies are the wave's retained artifacts, hash-matched below).
Scope: `corpus/knowledge/canonical-selection.md` (S262), `corpus/knowledge/crawler-identity.md` (S263).

## Verdict

| question | result |
|---|---|
| Body quotations found (passages + one inline fragment) | **15** (S262 10, S263 5) |
| `raw` substring of the retained body | **3** |
| `collapsed` (whitespace-only difference) | **2** |
| **`absent` — a defect under the assigned test** | **10** |
| Quotes carrying an explicit source-relation label | 13 (S262 8, S263 5) |
| Of those, label **false** | **10** |
| Quotes fabricated (words not on the page) | **0** |
| Quotes outside the cited section | **0** |
| Retained-body sha256 + byte count vs `receipts.json` | S262, S263 both **match** |

The ten `absent` quotes are **not fabricated**: every one is recoverable word-for-word once
inline HTML elements are removed. What fails is the entries' *own provenance claim* — each is
annotated `collapsed-only` or `raw`, and neither holds. The defect is a provenance-label
defect, not a quotation-fabrication defect. Ten of them, named below.

## Axes measured

1. **Raw substring** — the quote's text (entry hard-wraps joined with one space) occurs
   byte-for-byte in the retained body.
2. **Whitespace-collapsed** — not raw, but occurs after collapsing every `\s+` run in the body
   to one space. Collapsing whitespace only: tags are not whitespace.
3. **Absent** — neither. The spec's defect class. I then bound each defect with three
   independent axes so the reader can tell *why* and *how bad*:
   - **tolerant** — the quote's word sequence occurs with only whitespace and inline elements
     between words (fabrication test);
   - **faithful render** — occurs after *deleting* tags (not substituting a space) and
     collapsing: i.e. in the page as a browser renders it;
   - **faithful + space-repair** — same, after removing a space the entry inserted before
     punctuation. This is the signature of a `tag → " "` normalisation pipeline.
4. **In cited section** — the tolerant match's nearest preceding heading on the page.

Interpretation note: the "retained body" is the committed artifact
`.ufo/waves/round-51/sources/S262.html` / `S263.html`, whose sha256 and byte count equal
`receipts.json`. Raw bytes are therefore the primary test. Because a fair reader might instead
mean *rendered* text, I also report the rendered test — the result is robust: **7 of the 10
remain `absent` even under the rendered reading**, and all 7 are exactly the ones carrying an
inserted space before punctuation.

## S262 — `corpus/knowledge/canonical-selection.md`

Body `174926` B, sha256 `792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b`
(= receipt).

| entry L | kind | quote head | class | entry's label | label holds | splitting element | faithful render | nearest heading |
|---|---|---|---|---|---|---|---|---|
| 15 | blockquote | `indicating a canonical preference is a hint, not a rule.` | **raw** | "quoted from the section" | yes | — | yes | h3 How Google indexes and chooses the canonical URL |
| 20 | blockquote | `There are a handful of factors that play a role in canonicalization: …` | **absent** | "(collapsed-only quote, the source breaks the sentence across lines)" | **no** | `<code>rel="canonical"</code> <code>link</code>` | yes | h3 …chooses the canonical URL |
| 26 | blockquote | `Google then chooses the page that, based on the factors (or signals ) …` | **absent** | "(collapsed-only quote)" | **no** | `<em>signals</em>` **+ inserted space before `)`** | **no** | h3 …chooses the canonical URL |
| 32 | blockquote | `You can indicate your preference to Google using these techniques, …` | **absent** | "(collapsed-only quote)" | **no** | `<a href="…/consolidate-duplicate-urls#define-canonical">indicate your preference to Google</a>` | yes | h3 …chooses the canonical URL |
| 39 | bullet | `Device variants : for example, a page with both a mobile and a desktop version` | **absent** | "each quoted **raw** from the page" | **no** | `<b>Device variants</b>` **+ colon artifact** | **no** | h1 What is canonicalization |
| 40 | bullet | `Protocol variants : for example, the HTTP and HTTPS versions of a site` | **absent** | "each quoted **raw** from the page" | **no** | `<b>Protocol variants</b>` **+ colon artifact** | **no** | h1 What is canonicalization |
| 41 | bullet | `Site functions : for example, the results of sorting and filtering …` | **absent** | "(collapsed-only quote)" | **no** | `<b>Site functions</b>` + line wrap **+ colon artifact** | **no** | h1 What is canonicalization |
| 43 | bullet | `Accidental variants : for example, the demo version of the site …` | **absent** | "(collapsed-only quote)" | **no** | `<b>Accidental variants</b>` + line wrap **+ colon artifact** | **no** | h1 What is canonicalization |
| 49 | blockquote | `the search result will probably point to the mobile page …` | **collapsed** | "(collapsed-only quote)" | **yes** | — | yes | h3 …chooses the canonical URL |
| 60 | inline | `objectively the most complete and useful for search users` | **raw** | (none; presented as page wording) | n/a | — | yes | h3 …chooses the canonical URL |

Revision line, quoted at L76 as `"Last updated 2026-08-20 UTC"`: **raw**, and equal to
`receipts.json` `sources.S262.docRevision`.

## S263 — `corpus/knowledge/crawler-identity.md`

Body `175561` B, sha256 `6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de`
(= receipt).

| entry L | kind | quote head | class | entry's label | label holds | splitting element | faithful render | nearest heading |
|---|---|---|---|---|---|---|---|---|
| 10 | blockquote | `Googlebot is the generic name for two types of` | **raw** | "quoted raw from the page" | **yes** | — | yes | h1 Googlebot |
| 15 | blockquote | `Googlebot Smartphone : a mobile crawler that simulates a user on a mobile device` | **absent** | "(collapsed-only quotes; the source puts a space before the colon and breaks the lines)" | **no** | `<a href="…#googlebot-smartphone"><b>Googlebot Smartphone</b></a>` **+ colon artifact** | **no** | h1 Googlebot |
| 17 | blockquote | `Googlebot Desktop : a desktop crawler that simulates a user on desktop` | **absent** | same label | **no** | `<a href="…#googlebot-desktop"><b>Googlebot Desktop</b></a>` **+ colon artifact** | **no** | h1 Googlebot |
| 21 | blockquote | `You can identify the subtype of Googlebot by looking at the HTTP user-agent request header in the request` | **absent** | "(collapsed-only quote)" | **no** | `<a …>HTTP <code>user-agent</code> request header</a>` | yes | h1 Googlebot |
| 26 | blockquote | `both crawler types obey the same product token (user agent token) in robots.txt` | **collapsed** | "(collapsed-only quote)" | **yes** | — | yes | h1 Googlebot |

Revision line, quoted at L53 as `"Last updated 2026-02-03 UTC"`: **raw**, and equal to
`receipts.json` `sources.S263.docRevision`.

## The ten defects, by name

Each is `absent` under the assigned test, and each carries a label the bytes contradict. Byte
evidence is the exact retained-body slice, quoted as a Python repr.

**D1 — S262 L20.** Label: *collapsed-only, the source breaks the sentence across lines.*
Collapsing whitespace is not sufficient; two `<code>` elements sit inside the sentence:
`…in a sitemap, and\n  <code translate="no" dir="ltr">rel="canonical"</code> <code translate="no" dir="ltr">link</code> annota…`
The "across lines" half of the claim is true; "collapsed-only" is false.

**D2 — S262 L26.** Label: *collapsed-only.*
`(or <em>signals</em>) the\n  indexing process` — and the entry prints `factors (or signals )`
with a space before `)`. The page has `signals)`. Two failures: tag split, and a surface form
that exists nowhere in the body (fails even the rendered test).

**D3 — S262 L32.** Label: *collapsed-only.*
`indicate your preference to Google</a>\n  using these techniques` — the anchor
`…/consolidate-duplicate-urls#define-canonical` opens inside the sentence. Under the rendered
test the entry's string is exact.

**D4 — S262 L39.** Label: *each quoted **raw** from the page.*
`<b>Device variants</b>: for example` — not raw by any reading, and the entry's `variants :`
inserts a space the page does not have.

**D5 — S262 L40.** Label: *each quoted **raw** from the page.*
`<b>Protocol variants</b>: for example` — same two failures.

**D6 — S262 L41.** Label: *collapsed-only.*
`<b>Site functions</b>: for example, … of a category\n     page` — tag split, line wrap, and
`functions :` artifact.

**D7 — S262 L43.** Label: *collapsed-only.*
`<b>Accidental variants</b>: for example, the demo version of the site is accidentally left\n    accessible`
— tag split, line wrap, and `variants :` artifact.

**D8 — S263 L15.** Label: *collapsed-only; **the source puts a space before the colon**.*
The retained bytes are
`…google-common-crawlers#googlebot-smartphone"><b>Googlebot Smartphone</b></a>:\n    a mobile crawler…`
— `</b></a>:` i.e. **no space before the colon**. The space is produced by the entry's own
`tag → " "` substitution, and the entry attributes it to the source. This is the sharpest of
the ten: a claim about the source that the source contradicts, not merely an over-narrow
normalisation label.

**D9 — S263 L17.** Same label, same contradiction, same artifact (`Googlebot Desktop :` vs
`<b>Googlebot Desktop</b></a>:`).

**D10 — S263 L21.** Label: *collapsed-only.*
`…by looking at the\n  <a href="…/overview-google-crawlers">HTTP <code translate="no" dir="ltr">user-agent</code> request header</a>\n  in the request.`
Nested anchor + code inside the sentence.

## What held (negatives, so the next seat need not re-measure)

- **No fabrication.** All 15 quotations match the page's word sequence with only inline
  elements interleaved. Nothing was invented, reordered, or paraphrased into a quotation.
- **No out-of-section quotation.** Every quotation resolves under a heading that precedes it on
  the page, inside the cited document (nearest-heading column above). None resolved into a
  support/resource block.
- **The two `collapsed` labels are correct**: S262 L49 and S263 L26 differ from the body by
  whitespace alone, exactly as annotated.
- **The two `raw` labels that are on the gate path are correct**: S262 L15 and S263 L10 are raw.
- **Revision lines certify themselves**: both `"Last updated …"` strings are raw and equal the
  receipts' `docRevision` field, so the "doc rev." in each row is readable from the retained
  body rather than remembered.
- **Bodies unchanged**: `sha256sum` and `stat -c %s` reproduce `receipts.json` exactly
  (`174926` / `175561` bytes).
- Two nuisances, not defects: the S262 row's § label `What is URL canonicalization` is the
  page `<title>` (offset 73197), while the on-page `h1` reads `What is canonicalization`; the
  S263 § label is the page's opening sentence rather than a heading (itself tag-split around
  `<a>web crawlers</a>`). Both are defensible as "the passage beginning …".

## Exposure: what the C2 predicate does and does not see

Read directly from `.ufo/waves/round-51/c51_quote_truth.py` (311 lines) and
`corpus/lessons/round-51.md`:

- The only condition that tests quotation truth is **C5**, and C5 tests *the lesson's Gate
  quote*, not the entries' quotations: `gate_quote(lesson, sid)` → 6–25 words → `quote in text`
  against the retained body.
- The two Gate quotes are `"indicating a canonical preference is a hint, not a rule"` (10
  words) and `"Googlebot is the generic name for two types of"` (9 words) — i.e. precisely the
  S262 L15 and S263 L10 strings, the two that *are* raw.
- Therefore `C2 quote-truth 8/8 met=True` is fully consistent with 10 of 15 body quotations
  failing the strict test and 10 of 13 provenance labels being false. Conditions C1–C4 and C6–C8
  check existence, id citation, row shape, `used-by`, hashes and mirror ancestry; none inspects
  entry quotations.
- This is a coverage gap, not a miscomputation: C5 is correct on what it measures. If the
  round wants entry-quote truth inside the predicate, a condition of the form "every quotation
  in an admitted entry is raw **or** tag-stripped-raw, and its annotation names which" would
  have to be added. I did not modify the counter — it is outside this seat.

## Reproduction

Scratch only, under `/tmp` (never in the lane). Two scripts, both stdlib, no network:

```
python3 -B /tmp/quote_raw_scan.py     # full scan: 15 body quotations + 2 revision lines,
                                      # 4 axes, section check, excluded-span ledger
python3 -B /tmp/qrs_condensed.py      # 14 passage quotations, prints classes + split tags
```

`quote_raw_scan.py` printed: `TOTAL raw=5 collapsed=2 absent=10 quotes=17` (the 17 = 14
passages + 1 inline fragment + 2 revision strings; the revision strings are raw and are reported
separately above). `qrs_condensed.py` printed `raw=2 collapsed=2 absent=10 n=14`, matching the
full run on the passage set. The condensed script is embedded so the table is re-derivable even
if `/tmp` is wiped:

```python
#!/usr/bin/env python3
import json, re
ROOT = "/home/vgpnk/Projects/shokunin/kake-shokunin"
SRC = ROOT + "/.ufo/waves/round-51/sources"
ENT = {"S262": ("corpus/knowledge/canonical-selection.md", SRC + "/S262.html"),
       "S263": ("corpus/knowledge/crawler-identity.md", SRC + "/S263.html")}
TAIL = re.compile(r'^\s*(\([^"<>]*\))?\s*\.?\s*$')
COLL = lambda s: re.sub(r"\s+", " ", s)
GAP = r"(?:\s*(?:<[^>]*>\s*)*)"


def closing(t):
    for p in reversed([i for i, c in enumerate(t) if c == '"']):
        if TAIL.match(t[p + 1:]) and t.find('"') < p:
            return p
    return None


def passages(path):
    L = open(path, encoding="utf-8").read().splitlines()
    out, i = [], 0
    while i < len(L):
        s = L[i].lstrip()
        bq = s.startswith(">") and '"' in s
        bl = s.startswith("- ") and s[2:].lstrip().startswith('"')
        if not (bq or bl):
            i += 1
            continue
        blk, j = [s[1:].lstrip() if bq else s[2:].lstrip()], i + 1
        while closing("\n".join(blk)) is None and j < len(L):
            if bq and not L[j].lstrip().startswith(">"):
                break
            if not bq and not L[j].strip():
                break
            blk.append(L[j].lstrip()[1:].lstrip() if bq else L[j].strip())
            j += 1
        t = "\n".join(blk)
        p = closing(t)
        if p is not None:
            out.append((i + 1, COLL(t[t.find('"') + 1:p]).strip()))
        i = j
    return out


rows = []
for sid, (entry, body_path) in ENT.items():
    body = open(body_path, encoding="utf-8", errors="replace").read()
    body_c = COLL(body)
    for ln, q in passages(ROOT + "/" + entry):
        cls = "raw" if q in body else ("collapsed" if q in body_c else "absent")
        m = re.search(GAP.join(re.escape(f) for f in q.split(" ")), body)
        tags = sorted(set(re.findall(r"<[^>]+>", m.group(0)))) if m else []
        rows.append({"row": sid, "line": ln, "class": cls,
                     "tolerant": bool(tags), "tags": tags, "quote": q})

print(json.dumps(rows, indent=1, ensure_ascii=False))
print("\n".join(f"{r['row']} L{r['line']:<3} {r['class']:<9} "
                f"tolerant={'y' if r['tolerant'] else 'N'} "
                f"{','.join(r['tags']) or '-'} | {r['quote'][:58]}"
                for r in rows))
c = {"raw": 0, "collapsed": 0, "absent": 0}
for r in rows:
    c[r["class"]] += 1
print(f"\nraw={c['raw']} collapsed={c['collapsed']} absent={c['absent']} n={len(rows)}")
```

Byte-evidence probes used, all read-only:

```
sha256sum S262.html S263.html ; stat -c '%n %s' S262.html S263.html
grep -o -m2 ".\{0,80\}handful of factors.\{0,120\}" S262.html
python3 -B -c 'b=open("S263.html").read(); i=b.find("Googlebot Smartphone"); print(repr(b[i-60:i+120]))'
```

## Risks and blockers

- **R1 — label defects propagate.** Any later round that reads `collapsed-only` as an
  instruction ("strip whitespace and you will find this") will fail to find 10 strings. The
  cheap repair is to rewrite the ten annotations as `tag-split quote` and to drop the inserted
  spaces before `:` and `)` (D2, D4–D9), which changes surface text but no claim.
- **R2 — the predicate blind spot is durable, not accidental.** Because C5's Gate quotes are
  the two raw strings, the 8/8 predicate will keep passing on entries whose quotations are
  annotated wrongly. This is a design choice visible in the frozen contract, so it is the L1's
  call, not this seat's; I am flagging it, not changing it.
- **R3 — my section test is heading-based, not DOM-based.** It reports the nearest preceding
  `<h1>…<h4>`; a quote hidden inside a `<devsite-…>` component between headings would still
  read as in-section. None did: all 15 matched ordinary prose under the headings listed.
- No blocker. Nothing outside this report was written; no tool was installed or upgraded (the
  scan needed only `python3` stdlib and coreutils already present). No `pacman`, `uv`, or
  network channel was used, so the host-wide pacman pause did not apply.

## Appendix — parser-free re-derivation and scratch durability

This lane's evidence does **not** rest on any sweepable scratch tree, and it cites no
`.ufo/waves/round-35/scratch*/` path at all.

Correcting an earlier version of this paragraph: the tree discussed by the sibling lanes
belongs to **`mado-shokunin`**, not to this one. `kake-shokunin`'s round-35 holds
`census-before.txt`, `census-after.txt`, `criteria/`, `evidence/`, `retained/`, `sealed/`,
`sources/`, `w1/`, `w2/` and has never carried a `scratch/` directory, so the `ls` this seat
first ran *here* could not have corroborated anything about it; that sentence was wrong and is
replaced by the measurement below, taken read-only in the repo the tree actually lives in:

- `mado-shokunin/.ufo/waves/round-35/scratch/` was **relocated**, not deleted, to
  `scratch-evidence/`: **59** seat directories, tree mtime `2026-10-25 03:45:56 -0300`,
  per-seat contents byte-intact.
- Spot-check of the peer files the relocation notice cites:
  `scratch-evidence/RevQuoteS210/rederive.sh` = 3727 B, sha256
  `468c54a6e2e2e2c79931ea416cadd4f027655199c4bcfb6e40174b90b6e675df`; `rederive.out` =
  2714 B, sha256 `4b7b77d6d3fd8bc661a61d5b02c53feebd4db68fbca3b8ad860649911c0a2026`. Both match
  the values that lane's report cites.
- A fresh `scratch/` also exists again at that path, mtime `2026-10-25 03:47:41 -0300`,
  currently holding **1** seat directory — i.e. the old path is in use again while the
  checkpoint lives beside it, which is why the report body, not scratch, has to be the durable
  locus.
- No `QuoteRawScan` and no `Kake` seat directory exists in that tree: this seat is
  `L1Kake51.ExecQuoteRawScan-2`, round **51**, lane **kake-shokunin**, so there is nothing of
  this seat's to recover from `mado-shokunin`'s round 35.

The only scratch this report ever used is `/tmp`, and both scripts are reproduced in this file:
the `## Reproduction` block re-derives the 14 passage quotations from the tree, and the block
below re-derives **all 15** from the verbatim strings alone — no parsing of the entries, no
scratch file needed. Better still, every column of both per-entry tables (class, faithful
render, nearest heading, splitting element) is stated per-quote above, so the tables themselves
are the evidence, and this report remains valid if `/tmp` and every scratch tree are swept.

Run as `python3 -B <this block>`; it prints
`raw=3 collapsed=2 absent=10 n=15`, and `faithful=no` for exactly the seven quotes listed in
the Verdict discussion (S262 L26, L39, L40, L41, L43; S263 L15, L17).

```python
#!/usr/bin/env python3
"""Parser-free re-derivation: the 15 quotations verbatim, classified from the bodies alone."""
import re

SRC = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/sources"
COLL = lambda s: re.sub(r"\s+", " ", s)
GAP = r"(?:\s*(?:<[^>]*>\s*)*)"
REPAIR = re.compile(r"\s+([,.;:)\]}])")

Q = {
 "S262": ("S262.html", [
  (15, "indicating a canonical preference is a hint, not a rule."),
  (20, 'There are a handful of factors that play a role in canonicalization: whether the page is '
       'served over HTTP or HTTPS, redirects, presence of the URL in a sitemap, and rel="canonical" '
       'link annotations.'),
  (26, "Google then chooses the page that, based on the factors (or signals ) the indexing process "
       "collected, is objectively the most complete and useful for search users, and marks it as the "
       "canonical."),
  (32, "You can indicate your preference to Google using these techniques, but Google may choose a "
       "different page as canonical than you do, for various reasons."),
  (39, "Device variants : for example, a page with both a mobile and a desktop version"),
  (40, "Protocol variants : for example, the HTTP and HTTPS versions of a site"),
  (41, "Site functions : for example, the results of sorting and filtering functions of a category page"),
  (43, "Accidental variants : for example, the demo version of the site is accidentally left accessible to crawlers"),
  (49, "the search result will probably point to the mobile page if the user is on a mobile device, "
       "even if the desktop page is the canonical"),
  (60, "objectively the most complete and useful for search users"),
 ]),
 "S263": ("S263.html", [
  (10, "Googlebot is the generic name for two types of"),
  (15, "Googlebot Smartphone : a mobile crawler that simulates a user on a mobile device"),
  (17, "Googlebot Desktop : a desktop crawler that simulates a user on desktop"),
  (21, "You can identify the subtype of Googlebot by looking at the HTTP user-agent request header "
       "in the request"),
  (26, "both crawler types obey the same product token (user agent token) in robots.txt"),
 ]),
}

tot = {"raw": 0, "collapsed": 0, "absent": 0}
for sid, (name, qs) in Q.items():
    body = open(f"{SRC}/{name}", encoding="utf-8", errors="replace").read()
    body_c, flat = COLL(body), COLL(re.sub(r"<[^>]+>", "", body))
    heads = [(m.start(), int(m.group(1)), COLL(re.sub(r"<[^>]+>", "", m.group(2))).strip())
             for m in re.finditer(r"<h([1-4])[^>]*>(.*?)</h\1>", body, re.S)]
    for ln, q in qs:
        cls = "raw" if q in body else ("collapsed" if q in body_c else "absent")
        tot[cls] += 1
        m = re.search(GAP.join(re.escape(f) for f in q.split(" ")), body)
        tags = sorted(set(re.findall(r"<[^>]+>", m.group(0)))) if m else []
        near = [h for h in heads if h[0] < m.start()][-1] if m else (0, 0, "<no match>")
        print(f"{sid} L{ln:<3} {cls:<9} faithful={'no ' if q not in flat else 'yes'} "
              f"repaired={'yes' if REPAIR.sub(r'\1', q) in flat else 'no '} "
              f"tolerant={'y' if m else 'N'} h{near[1]} {near[2][:44]!r} "
              f"tags={','.join(tags) or '-'}")
print(f"raw={tot['raw']} collapsed={tot['collapsed']} absent={tot['absent']} n={sum(tot.values())}")
```
