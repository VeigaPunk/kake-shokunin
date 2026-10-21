# UncoveredS024S025 — S024/S025 statement freshness in `corpus/knowledge/static-canonical-preflight.md`

- Seat: `KakeR26-2.UncoveredS024S025` (reviewer, leaf — no dispatch). Axis: **freshness**. Milestone: `r26-recheck-falsify`. Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Checked 2026-10-21.
- Target: the S024/S025-attributable statements of `corpus/knowledge/static-canonical-preflight.md` (no W1 pair seat covered these rows for this file: `statements.json` pairs exist only for rows `S001–S013, S020–S034` minus `S024, S025`; `rows` list confirmed by `python3 -c "…"` over `.ufo/waves/round-26/statements.json` → `['S001',…,'S034']`, `'S024' in rows → False`).
- Retained bytes: `.ufo/waves/round-26/fetched/text/S024-1.txt` (96,513 chars; raw `fetched/S024-1.raw.gz`, sha256 `fd9ae4b6a2e12472ae6f61c52b4ef32751e63f8262cea997d8c6056eba2db959`) and `.ufo/waves/round-26/fetched/text/S025-1.txt` (78,976 chars; raw `fetched/S025-1.raw.gz`, sha256 `5854951bbabbdca6b5ea365edd1e2f14e342bc51e77353469d21e46f859abe43`); provenance `.ufo/waves/round-26/fetched/manifest.json`; row receipts `.ufo/waves/round-26/rechecks/S024.json` (HOLD), `rechecks/S025.json` (HOLD).
- Tooling: **no tool installed or upgraded this run** (no `pacman`, no `uv`, no `cargo`/`npm`; `python3` stdlib and `curl`/`grep`/`read` already present). All checks read-only; no corpus, script, lane-state or Git mutation by this seat.

## Verdict: DISAGREE (low) — the S025 statements hold; the S024 attributions need one appended correction

The row receipts for S024/S025 are correct (HOLD) and the S025-derived statements in this entry are faithful. But the two S024-sourced statements in this entry drop S024's attribute scope, and one of them applies the S024 tree-order rule to a case where S024 cannot apply at all (a `<base>` inside foreign content). That is exactly the defect class the lane already accepted twice for S030 in this same file ("misuses S030's term", "keeps the right outcome with the wrong label"), so it is a STALE-attribution finding, not nitpicking. Outcome/behaviour of `scripts/canonical_audit.py` is unaffected.

---

## 1. Statement inventory and verdicts

| # | Corpus statement (file:line) | Row | Verdict | Reason |
|---|---|---|---|---|
| S-1 | `corpus/knowledge/static-canonical-preflight.md:101` — “S024 (the first base in tree order wins)” | S024 | **STALE** | Drops S024's attribute scope (href vs target). Evidence §2.1. |
| S-2 | `corpus/knowledge/static-canonical-preflight.md:115-117` — “**any `<base>` after the head**, in or out of foreign content, because a body base is still the document's first base in tree order (S024) and would change a relative canonical.” | S024 | **STALE** | Two defects: attribute scope (S-1) and the “in … foreign content” half, which S024 does not govern (§2.2). |
| S-3 | `corpus/knowledge/static-canonical-preflight.md:72` — “Comments, raw script text and template descendants cannot supply a document-head canonical.” (template clause) | S025 | **HOLD** | Verbatim §4.12.3 support, §3.1. |
| S-4 | `corpus/knowledge/static-canonical-preflight.md:143-146` — “[r23-correction] ‘template descendants cannot supply a document-head canonical’ rests on S025 (template contents are not children of the template) … it holds for the static input bytes only, not for script-cloned template content” | S025 | **HOLD** | Quote-faithful paraphrase plus a correct scope limit, §3.2. |

Not in scope / not S024-S025-attributable (recorded so the coverage claim is explicit): lines 80-81’s `///project/a.html` discussion is attributed to S029/S028 (not S024); line 72’s “Comments, raw script text” clauses rest on the tool/HTMLParser scope (`scripts/canonical_audit.py:104-105`, S026), not on S025.

---

## 2. Findings

### 2.1 S-1 (line 101) — “the first base in tree order wins” drops S024's attribute scope — STALE (low)

S024 §4.2.3 (retained view `fetched/text/S024-1.txt`) says, verbatim:

> offset 9795: “There must be no more than one base element per document.”
> offset 10172: “If there are multiple base elements with href attributes, all but the first are ignored.”
> offset 10588: “If there are multiple base elements with target attributes, all but the first are ignored.”
> offset 10957: “…contains a base element with a target attribute, set target to the value of the target attribute of the first such base element.”
> offset 11210: “A base element that is the first base element with an href content attribute in a document tree has a frozen base URL.”

So S024 has **two independent first-wins rules, each scoped to one attribute**: the first base **with href** in tree order owns the frozen base URL, and the first base **with target** owns the default navigable. The corpus's “the first base in tree order wins” collapses them and loses the scoping. The corpus's own source row already states the precise form — `corpus/SOURCES.md:32` (S024) teaches: “Only the first base element with href supplies the base; later base href values are ignored”. A base with only `target` does not affect URL resolution at all, so a later base **with href** still sets the base URL; under the corpus's shorthand, such a document would be read the other way round.

Command and output (quote offsets measured in the retained view, not in any other row's text):

```
$ python3 -c "t=open('fetched/text/S024-1.txt',encoding='utf-8').read(); …"
== S024-1.txt len 96513
   10172 FOUND If there are multiple base elements with href attributes, all but the first are ignored.
   11210 FOUND A base element that is the first base element with an href content attribute in a document tree has a frozen base URL.
    9795 FOUND There must be no more than one base element per document.
   10588 FOUND If there are multiple base elements with target attributes, all but the first are ignored.
   10957 FOUND contains a base element with a target attribute, set target to the value of the target attribute of the first such base element
```

Material consequence for this entry's own reasoning (line 116-117): a body base changes a relative canonical **only** when it is the first base *with href* in tree order. If the head already carries a `base[href]`, S024 ignores the later one (“all but the first are ignored”), so the body base would **not** change the canonical — yet the tool still rejects it. The corpus presents the tree-order rule as the reason for that blanket rejection; the rule is not the reason in that subcase. The tool's blanket rejection is still justified — it is conservative local policy and it matches the conformance sentence “There must be no more than one base element per document” (also S024, offset 9795) — but the entry's stated ground is wrong for that subcase, so the attribution is stale even though the behaviour is right.

### 2.2 S-2 (lines 115-117) — the “in … foreign content” half has no S024 support — STALE (low)

The sentence attaches the S024 reason to a `<base>` “in or out of foreign content”. Per WHATWG parsing (S031 §13.2.6.5, retained view `fetched/text/S031-1.txt`, offset 235576), the foreign-content breakout list is:

> “A start tag whose tag name is one of: "b", "big", "blockquote", "body", "br", "center", "code", "dd", "div", "dl", "dt", "em", "embed", "h1", "h2", "h3", "h4", "h5", "h6", "head", "hr", "i", "img", "li", "listing", "menu", "meta", "nobr", "ol", "p", "pre", "ruby", "s", "small", "span", "strong", "strike", "sub", "sup", "table", "tt", "u", "ul", "var"”

**“base” is not in that list** (neither is “link”). The same section's fallback is “Insert a foreign element for the token, with the adjusted current node's namespace”, and the HTML integration points are (S031, offset ~130371) “An SVG foreignObject element / An SVG desc element / An SVG title element”. Therefore:

- `<svg><base href="…">` (no integration point, no preceding `head` breakout) becomes an **SVG-namespace** element, not the HTML `base` element of S024 §4.2.3 (whose DOM interface is `HTMLBaseElement`, whose context is “In a head element containing no other base elements”). S024's “first base element with an href content attribute in a document tree” rule therefore does not apply to it, and it **cannot** change a relative canonical. The corpus's stated reason is unsupported for this case.
- Bases that *do* end up as HTML base elements keep the S024 reason: a base directly in the body; a base inside an HTML integration point (`foreignObject`, `desc`, `title` — the entry itself already notes “SVG `title` is an HTML integration point” at line 109); or a base after a `head` breakout (the `head` token *is* a breakout tag), which is the corpus's `svg_head_breakout_base` case.

The tool's behaviour is unchanged and still conservative: `scripts/canonical_audit.py:207-210` rejects `base`/`head`/canonical-looking `link` tokens inside SVG/MathML as unsupported, and the corpus already states that as its own rule at lines 113-114 (“any `base`, `head` or canonical-looking `link` token inside SVG/MathML”; the SVG/MathML subtree rule itself is at lines 106-107). Only the *reason* attached to the foreign case is wrong. The script even carries the same over-broad wording in a comment:

```
$ sed -n '206,210p' scripts/canonical_audit.py
        # Inside SVG/MathML after the explicit head, only tokens that a browser
        # could turn into an effective HTML base/head/canonical are ambiguous.
        if tag in {"base", "head"} or (tag == "link" and is_canonical_relation(attrs_first_wins(attrs))):
            self.unsupported = True
```
```
$ sed -n '289,291p' scripts/canonical_audit.py
        if tag in {"head", "base"}:
            # A body base is still the document's first base in tree order.
            self.unsupported = True
```

(“a browser could turn into an effective HTML base” is true for integration-point children and after a `head` breakout, not for a plain `<base>` in SVG.) This is the same pattern the lane already recorded for S030, where the correction named the script's mirror text: “`scripts/canonical_audit.py:108` uses the same informal label” (`corpus/knowledge/static-canonical-preflight.md:192`). This seat does not mutate the script; the wording mirror is reported only.

### 2.3 The entry's own Round-26 narrative omits S024/S025 (completeness, low)

`corpus/knowledge/static-canonical-preflight.md:184` enumerates the rows covered this round: “Rows S020, S021, S026, S027, S028, S029, S030, S031, S032, S033 and S034 were re-fetched by one public GET each … and judged HOLD at their anchors against the retained bytes”. S024 and S025 **were** re-fetched this round (retained views `fetched/text/S024-1.txt`, `S025-1.txt`; receipts `rechecks/S024.json`, `rechecks/S025.json`, both HOLD) and S024/S025 statements live in this file — the sentence lists only the rows that had W1 pair seats, which is not stated. Because that sentence sits inside an already-appended block, it cannot be edited append-only; the appended bullets in §4 below close the gap for these two rows instead.

### 2.4 Cross-lane note (not my adjudication): `rechecks/S025.json` `anchorObserved` offset is not word-bounded at its quote

The receipt records “text view S025-1.txt line 1 at offset 62596”. The quoted sentence actually begins at **62638** (span 62638–62721, 83 chars); 62596 lands inside the preceding sentence (“…is a boolean attribute.”), and the paragraph proper starts at 62560. Metadata-only nit for the S025 row seat; the quote string, section label, HOLD verdict and `correction: null` are unaffected (same class of locator staleness the S024 seat recorded for `rechecks/S024.json`).

---

## 3. What holds

### 3.1 S-3 (line 72, template clause) — HOLD

S025 §4.12.3, verbatim from `fetched/text/S025-1.txt`:

> offset 62638: “The template contents of a template element are not children of the element itself.”
> offset 63489: “The p element in the template is not a child of the template in the DOM; it is a child of the DocumentFragment returned by the template element's content IDL attribute.”

So a `<link rel=canonical>` written inside template contents is not in the document tree at all and cannot supply a document-head canonical in the static bytes — the corpus's sentence is supported, and the row's own `teaches` (`corpus/SOURCES.md:33`, S025: “Template contents are not children of the template element itself and do not supply document-head canonical links”) matches it. The tool implements it (`scripts/canonical_audit.py:218-221, 320-323`, selftest case `template_decoy` → `canonical_missing`; `scripts/canonical_audit.py:104-105`: “Comments, raw-text elements, and template descendants do not contribute links.”). No stale wording.

### 3.2 S-4 (lines 143-146, the `[r23-correction]`) — HOLD

The correction's parenthetical “template contents are not children of the template” is a faithful paraphrase of the offset-62638 sentence, its attribution to S025 is exact, and its scope limit is correct in the retained bytes: §4.12.3 keeps the template content model “Nothing”, keeps the contents in a `DocumentFragment` owned by an inert template-contents owner document, and describes the template element as “used to declare fragments of HTML that can be cloned and inserted in the document by script” (retained view, immediately before offset 62638) — which is exactly why the claim is bounded to the static input bytes and does not cover script-cloned content. Nothing to correct.

---

## 4. Exact append-only text proposed for `corpus/knowledge/static-canonical-preflight.md`

Append at EOF, inside the existing `## Round-26 source recheck` bullet list (the file's last bullet is the S032 “Version note (not STALE)”). No earlier line is touched.

```markdown
- [r26-recheck S024 STALE] Line 101's "S024 (the first base in tree order wins)" and lines 115-117's "a body base is still the document's first base in tree order (S024) and would change a relative canonical" drop S024's attribute scope. Section 4.2.3 says "If there are multiple base elements with href attributes, all but the first are ignored" and "A base element that is the first base element with an href content attribute in a document tree has a frozen base URL"; the target attribute has its own separate first-with-target rule. Read: the first base with href in tree order sets the document base URL, and the first base with target sets the default navigable; a base carrying only target does not affect URL resolution, so a later base with href still sets the base URL. A body base therefore changes a relative canonical only when no earlier base[href] exists; a body base that follows a head base[href] is ignored by S024 ("all but the first are ignored"), so the tool's blanket html_unsupported for any base after the head is a conservative local policy (and matches "There must be no more than one base element per document"), not a requirement of the tree-order rule. The "in ... foreign content" half of line 115-117 has no S024 support: WHATWG parsing (S031 section 13.2.6.5) does not list "base" among the foreign-content breakout tags, so a base inside SVG/MathML outside an HTML integration point (SVG foreignObject, desc, title) is inserted as a foreign element, not an HTML base element, and cannot change a relative canonical; the rejection of base/head/canonical-link tokens inside foreign content (lines 113-114) stays the tool's own conservative unsupported-shape rule. scripts/canonical_audit.py:207-209 and :290 carry the same informal wording; behaviour is unchanged. Evidence: w2/UncoveredS024S025.md.

- [r26-recheck S025 HOLD — not STALE] The S025 statements in this entry hold against the 2026-10-21 bytes: line 72's "template descendants cannot supply a document-head canonical" and the [r23-correction] at lines 143-146 rest on section 4.12.3's "The template contents of a template element are not children of the element itself" and on "The p element in the template is not a child of the template in the DOM; it is a child of the DocumentFragment returned by the template element's content IDL attribute". The static-bytes-only limit and the script-cloned caveat still stand, and S024/S025 — re-fetched this round (rechecks/S024.json, rechecks/S025.json, both HOLD) — are the two rows of this entry's statement set that had no W1 pair seat. Evidence: w2/UncoveredS024S025.md.
```

Ledger consequence for the round-26 statement ledger (`statements.json` has no S024/S025 entry for this file): the S024 STALE bullet above satisfies the contract-amendment rule “each adjudicated STALE knowledge statement needs its `[r26-recheck S0NN STALE]` tag in the named corpus file”; the S025 bullet is a coverage note, not a STALE.

---

## 5. Residual risk and verification gaps

- **Residual risk (low).** The only behaviour-relevant statement in scope is the base-after-head rule; the tool's outcomes (reject any base after the head; ignore later base hrefs inside the head) are unchanged by the correction, so no receipt, counter result or published artifact changes. The risk that remains is *documentary*: a reader of line 116-117 may believe a `<base>` inside plain SVG changes the document base URL, which is false, and may believe that a body base always wins, which is false when a head `base[href]` precedes it.
- **Residual risk (low, lane-wide).** The same attribute-scope slip exists in the script comment `scripts/canonical_audit.py:290` and in the tool docstring's foreign-content wording (`scripts/canonical_audit.py:207-208`); if the entry's text is corrected but the comments are not, the informal wording survives in code. Not mutated by this seat (out of lane bounds); flagged for the owning lane.
- **Verification gaps.** (i) I did not GET `https://html.spec.whatwg.org/multipage/semantics.html` or `…/scripting.html` today; all S024/S025 quotes are read from the retained round-26 bytes, which the S024 seat showed to be byte-identical to the live document (sha256 `fd9ae4b6…2db959`, `Last-Modified: Tue, 20 Oct 2026 12:58:32 GMT`). (ii) The S031 parsing quotes come from the retained `fetched/text/S031-1.txt` view of `https://html.spec.whatwg.org/multipage/parsing.html` (row S031), not from a fresh GET. (iii) I did not fetch the SVG specification to confirm that no SVG element named `base` carries URL semantics; the argument does not depend on it, because the HTML base element of S024 §4.2.3 is an HTML-namespace element and the parsing rules insert a foreign element for `<base>` outside an HTML integration point. (iv) No tool was executed against fixtures (lane bound: only the commands this item names), so the tool's rejection of a body base and of base tokens inside foreign content is evidenced from source (`scripts/canonical_audit.py:207-210, 289-291`) and from the entry's own selftest list, not from a fresh run.

## 6. Bottom line

S025 (both statements) holds against the retained 2026-10-21 bytes; the S025 row receipt's HOLD is right. The two S024-sourced statements in this entry are stale in attribution and scope: “the first base in tree order wins” drops S024's href/target attribute scoping, and the “in … foreign content” half applies S024's tree-order rule to a `<base>` that is a foreign element and therefore cannot affect the document base URL. One appended `[r26-recheck S024 STALE]` bullet (text in §4) plus one appended coverage note for S025 fixes it; no behaviour, receipt, or counter result changes.

```json
{"target":"corpus/knowledge/static-canonical-preflight.md (S024/S025 statements, round-26 C1 freshness)","verdict":"DISAGREE","severity":"low"}
```
