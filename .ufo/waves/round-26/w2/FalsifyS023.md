# FalsifyS023 — attack receipt `rechecks/S023.json` (verdict HOLD)

- Seat: `KakeR26-2.FalsifyS023` (reviewer, leaf — no dispatch). Axis: **freshness**. Milestone: `r26-recheck-falsify`. Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Checked 2026-10-21.
- Target: receipt `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/rechecks/S023.json` (HOLD, fetchIndex 1) and row line `corpus/SOURCES.md:31` (S023 — WHATWG HTML: Link type canonical; teaches «Canonical indicates the preferred URL; link-type keywords compare ASCII case-insensitively»; anchor «Section 4.6.8 Link types and 4.6.8.4 canonical; Living Standard accessed 2026-10-20»).
- Retained bytes: `.ufo/waves/round-26/fetched/S023-1.raw.gz` (gunzip → 381,019 B, sha256 `82a81f233583716daf76ce20938a399016dfd877a9368ea2cdb1a60bcd3df6b7`); retained view `.ufo/waves/round-26/fetched/text/S023-1.txt` (108,074 chars, 1 newline → all content on line 1); provenance `.ufo/waves/round-26/fetched/manifest.json`.
- Tooling: **no tool installed or upgraded this run** (no `pacman`, no `uv`, no `cargo`/`npm`); only `python3` stdlib, `curl`, `grep`, `read`, and the repo's own `measure.py`. All checks read-only; no corpus, script, lane-state or Git mutation by this seat.

## Verdict: AGREE (low) — the HOLD stands on freshness; one metadata locator defect in the receipt

The substantive attack failed. The document has not drifted by one byte since the row was opened on 2026-10-20, the quote is verbatim and uniquely located inside §4.6.8, it grounds this row's `teaches` clause, and both cited section numbers (§4.6.8, §4.6.8.4) still carry the same text. The **HOLD** verdict is correct. One **low-severity** defect survives: `anchorObserved` describes the §4.6.8.4 body as following "at the same heading level" as §4.6.8, and in the retained raw bytes §4.6.8 is an `<h4>` while §4.6.8.4 is an `<h5>` — one level deeper, not the same. (A second, adjacent nit in the seat report is recorded in §5; it does not touch the receipt.)

---

## 1. Did content/version change in a way the receipt missed? — No. Zero drift, provable three ways.

**(a) Live GET today is byte-identical to the retained fetch.** One plain public GET of the row URL (body hashed in memory, not saved):

```
$ curl -sS -D - -o /dev/null --max-time 60 "https://html.spec.whatwg.org/multipage/links.html#link-type-canonical"
HTTP/2 200
date: Wed, 21 Oct 2026 16:31:02 GMT
content-type: text/html; charset=utf-8
content-length: 381019
last-modified: Tue, 20 Oct 2026 12:58:32 GMT
etag: "6ad76578-5d05b"

$ curl -sS --max-time 60 "https://html.spec.whatwg.org/multipage/links.html#link-type-canonical" | sha256sum
82a81f233583716daf76ce20938a399016dfd877a9368ea2cdb1a60bcd3df6b7  -
```

That digest equals the retained raw (`zcat S023-1.raw.gz | sha256sum` → same) and the manifest entry for S023 (`fetched/manifest.json`: `row: S023`, `index: 1`, `status: 200`, `bytes: 381019`, `sha256: 82a81f23…f6b7`, `last-modified: Tue, 20 Oct 2026 12:58:32 GMT`, `etag: "6ad76578-5d05b"`). `Last-Modified` is unchanged, and the retained raw's own masthead still reads `Last Updated 20 October 2026`.

**(b) The document is byte-identical to the original 2026-10-20 read — the receipt's argument is weaker than the available proof.** The receipt argues freshness from date equality ("the row's access date (2026-10-20) equals the page's current Last-Modified date"). Date equality is not sufficient in general (a same-day publish after the read would be invisible). The round-22 record pins the read by digest, and that digest is the one served today — `.ufo/waves/round-22/w1/Case06.md:387`:

> `| S023 | WHATWG HTML §4.6.8.4, https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." | 82a81f233583716daf76ce20938a399016dfd877a9368ea2cdb1a60bcd3df6b7 (html-links.html) |`

under `Case06.md:380-382` — "Primary, opened this session, access date 2026-10-20; living standards, so anchors + fetch digest pin the read". Same sha256 as today ⇒ the row's `accessed 2026-10-20` pins the live bytes exactly, not merely the date. (The receipt's conclusion is right; this is the stronger form of the same conclusion.)

**(c) Section numbering and headings are unchanged in the live bytes.** Raw heading scan of the retained (byte-identical) document:

```
<h3 id=links>            secno 4.6      <h4 id=linkTypes>             secno 4.6.8
<h4 id=introduction-2>   secno 4.6.1    <h5 id=rel-alternate>         secno 4.6.8.1
<h4 id=api-for-hyperlink-elements> 4.6.3 <h5 id=link-type-author>    secno 4.6.8.2
<h4 id=following-hyperlinks> 4.6.5    <h5 id=link-type-bookmark>    secno 4.6.8.3
<h4 id=hyperlink-auditing> 4.6.7      <h5 id=link-type-canonical>   secno 4.6.8.4
<h5 id=the-ping-headers> 4.6.7.1      <h5 id=link-type-dns-prefetch> secno 4.6.8.5
```

so `…/links.html#link-type-canonical` still lands on §4.6.8.4, and the row's anchor labels «Section 4.6.8 Link types and 4.6.8.4 canonical» remain accurate — no renumbering, no heading churn.

## 2. Does the quote ground THIS row's `teaches`, or is it page chrome / a neighbouring clause?

It grounds it, and it is uniquely located inside the cited section.

- **Not chrome, not a neighbour.** In the retained raw the sentence sits at byte **163461**, strictly between the §4.6.8 heading (`<h4 id=linkTypes>` at **159717**) and the first §4.6.8.x subsection (`<h5 id=rel-alternate>` at **177428**), and before the link-type table (`<table` at **165015**). `h.count('Keywords are always')` → **1**. It is a normative paragraph of §4.6.8, not navigation or boilerplate.
- **Verbatim in the effective text.** The receipt's quote is byte-for-byte present and word-bounded in the retained view (`fetched/text/S023-1.txt`, span **41679–41752**, 73 chars), and it is the *only* occurrence in that view. In the raw HTML the phrase is split by an inline link and a newline — `Keywords are always <a id=linkTypes:ascii-case-insensitive href=https://infra.spec.whatwg.org/#ascii-case-insensitive …>ASCII case-insensitive</a>, and must be\n  compared as such.` — i.e. the spec's "ASCII case-insensitive" is a hyperlink to the Infra standard's definition. The receipt locates the quote in the *text view* ("text view line 1"), which is exactly where it is contiguous; the counter's own check (`measure.py` `quote_in_text` over `source_text.text_of(raw, …)`) resolves it there too.
- **Row-specific.** Across all 32 population rows' effective texts, the normalized quote occurs in exactly one: `('S023', 1, 'S023-1.raw.gz')`. It cannot be boilerplate from another row's document (verified by re-running the counter's own `text_of`/`normalize` path over every manifest entry).
- **It grounds the second `teaches` clause; the first is grounded by §4.6.8.4, whose text is also unchanged.** The row teaches «Canonical indicates the preferred URL; link-type keywords compare ASCII case-insensitively». The receipt's quote is the ASCII-case-insensitivity half; the preferred-URL half is §4.6.8.4's own body, still reading verbatim (text-view offset **53082**):

  > `The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document.`

  and the §4.6.8 link-type table still carries the canonical row («Gives the preferred URL for the current document.», text-view offset **42350**). The receipt's `reason` states both halves, and the receipt is not obliged to quote both — the counter requires one verbatim, row-specific quote, which it has (12 alphanumeric tokens / 11 whitespace words; 6+ tokens and ≤25 words required).

- **The citing corpus statement is still true.** S023's only citing file is the lesson `corpus/lessons/round-22.md:46` — "Section 4.6.8.4: “The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document.”" — which I re-found verbatim in the fresh text at offset 53082. Nothing in `corpus/lessons/round-22-verifier-spotcheck.md` or `corpus/lessons/round-23.md` asserts anything about S023 that the fresh bytes contradict (`round-23.md:37` re-opens S023 "without change"). **No STALE correction is owed for S023**, and none is present in `corpus/knowledge/*` (which contains zero S023 mentions — the ledger's `pairs` correctly has no S023 entry, because S023 has no knowledge-entry claim).

## 3. Falsify the anchor as recorded — LOW-severity defect found

`rechecks/S023.json` `anchorObserved` says:

> "§4.6.8 Link types preamble (just before the link-type table), text view line 1; **§4.6.8.4 "Link type canonical" body follows at the same heading level**"

The **first** clause is correct in the raw bytes (§4.6.8 body, before the table, text view line 1). The **second** clause is not: §4.6.8 and §4.6.8.4 are at *different* heading levels.

```
$ python3 -c "import gzip,re; h=gzip.open('fetched/S023-1.raw.gz','rt',encoding='utf-8',errors='replace').read(); …"
<h4 id=linkTypes>            at 159717   secno 4.6.8
<h5 id=link-type-canonical>  at 197163   secno 4.6.8.4
```

§4.6.8 is an `<h4>`; §4.6.8.4 is an `<h5>` — a subsection one level deeper (as are all of 4.6.8.1–4.6.8.13). So "follows at the same heading level" is false under the only antecedent the sentence supplies (the §4.6.8 anchor named in the same sentence); it is at best ambiguous, since §4.6.8.4 *is* level-5 like its sibling subsections. Metadata only: the section numbers, the quotes, the `HOLD` verdict and `correction: null` are unaffected, and no corpus text, ledger statement or counter result depends on it.

**Minimal correction** (metadata only — no corpus text, no verdict change, no `correction` field needed):

> `anchorObserved`: "§4.6.8 Link types preamble (before the link-type table; text view line 1, quote at 41679–41752); §4.6.8.4 "Link type canonical" body — raw `<h5 id=link-type-canonical><span class=secno>4.6.8.4</span>`, one heading level below §4.6.8's `<h4 id=linkTypes>`"

(Optionally drop "just before": three paragraphs separate the quote from the table — 375 text-view chars between the quote's end at 41752 and the table header at 42127: `Thus, rel="next" is the same as rel="NEXT". Keywords that are body-ok affect whether link elements are allowed in the body. … The remainder can be registered as extensions.`)

## 4. Counter cross-check — the receipt is accepted by the committed counter

The committed counter at the pushed candidate accepts this receipt and the whole population, and rejects the base:

```
$ python3 -B .ufo/waves/round-26/measure.py --root . --revision e28312b14b076584fedd696fae2a684e460bd11e
{"decided": 32, "expected": 32, "findings": [], "hold": 32, "stale": 0, "unverifiable": 0,
 "statements": 276, "statementsStale": 8, "statementCorrections": 8, "populationSha256": "16330e1e…", …}
EXIT=0

$ python3 -B .ufo/waves/round-26/measure.py --root . --revision 97404de4ff73d6c8a4f87385cf5fdf36dca7f006
{"decided": 0, "expected": 32, "findings": [{"id": "receipts_absent", …}], …}
EXIT=1
```

S023-specific counter predicates all pass on the receipt as committed: `RECEIPT_KEYS` exact match; `id` matches the row; `verdict` ∈ {HOLD, STALE, UNVERIFIABLE}; `fetchIndex` 1 is a population fetch of S023; `quote` is a string with 12 tokens / 11 words; the quote is word-bounded in the effective fetch text; `correction` is `null` for a HOLD; `anchorObserved` is a nonempty string.

## 5. Adjacent finding (not in the receipt): stale text-view offsets in the seat report

`w1/RowS023.md` caveat 5 records:

> "Text view is a single-line extraction, so anchorObserved cites heading/section rather than line numbers; **body heading offsets 40385 (§4.6.8) and 52950 (§4.6.8.4)**."

Against the committed view `fetched/text/S023-1.txt` those offsets are **40398** and **52963** — stale by 13 characters. Root cause, evidenced not guessed: the shared extractor was edited and every view re-extracted between the seat's measurement and now.

```
$ stat -c '%y %n' fetched/text/S023-1.txt source_text.py w1/RowS023.md rechecks/S023.json before/source_text.py
2026-10-21 13:02:14 fetched/text/S023-1.txt
2026-10-21 13:02:13 source_text.py
2026-10-21 12:28:43 w1/RowS023.md
2026-10-21 13:04:31 rechecks/S023.json
```

Re-running both extractors over the same raw bytes reproduces exactly the two offset sets:

```
before/source_text.py : len 108057, 4.6.8 at 40385, 4.6.8.4 at 52950   <- seat report's numbers
source_text.py (now)  : len 108073, 4.6.8 at 40398, 4.6.8.4 at 52963   <- committed view
```

The committed view is self-consistent with the committed extractor (`text_of(load_gz('fetched/S023-1.raw.gz'))` → 108,073 chars = file minus its trailing newline). This is the same locator-staleness class the S024 seat recorded for that row; it affects **only** the seat report, because the receipt itself cites no offsets ("text view line 1" remains true). Minimal fix for the owning seat: caveat 5's "40385 … 52950" → "40398 … 52963". I do not own that file and did not edit it.

## 6. Residual risk / verification gaps

- **Residual risk (low, lane-wide, not row-specific):** because `source_text.py` was changed mid-wave and all 32 text views were re-extracted at 13:02:14, any seat report or receipt whose `anchorObserved` cites *character offsets* measured before 13:02 may be stale in the same way. S023's receipt cites none, so it is unaffected; whether other rows' receipts cite stale offsets is outside this leaf's scope.
- **Verification gaps:** (i) the §4.6.8.4 preferred-URL sentence is confirmed by *reading* the retained (byte-identical-to-live) document, not by re-fetching that fragment URL — the fragment is client-side only, and the section id `link-type-canonical` was confirmed present in the byte-identical document; (ii) I did not fetch `https://infra.spec.whatwg.org/#ascii-case-insensitive` (not a `corpus/SOURCES.md` row URL) — the raw shows the spec links that term to the Infra definition, and the receipt's quote does not depend on its content; (iii) the round-22 digest cited in §1(b) is taken from the committed round-22 record, which I did not re-derive by re-fetching on 2026-10-20 (impossible); the live GET today is independently byte-identical to the retained bytes, which is the strongest available drift test.
- **Coverage note (not a defect of this receipt):** S023 has no entry in `.ufo/waves/round-26/statements.json` `pairs`. That is consistent with the contract — the ledger enumerates *knowledge-entry* claims, `corpus/knowledge/*` contains no S023 mention, and S023's sole citing file (`corpus/lessons/round-22.md`) is a lesson, whose one S023 line is still verbatim-true against the fresh bytes (§2). The separate question of S022–S025 statement coverage is owned by `w2/LessonAudit.md` (D2) and `w2/UncoveredS024S025.md`; I neither contest nor extend it here.

## 7. Bottom line

The freshness attack fails: the document served today is byte-for-byte the document read on 2026-10-20 (sha256 `82a81f23…f6b7`, `Last-Modified: Tue, 20 Oct 2026 12:58:32 GMT`), §4.6.8 and §4.6.8.4 are unchanged and still carry the quoted text, the quote is verbatim, word-bounded and unique to this row, and it grounds the row's ASCII-case-insensitivity clause while §4.6.8.4 grounds the preferred-URL clause. The receipt's `HOLD` is correct and the counter accepts it (32/32 decided, exit 0). The only actionable item is the receipt's `anchorObserved` heading-level wording ("at the same heading level" — §4.6.8 is `<h4>`, §4.6.8.4 is `<h5>`), correctable by restating the two raw heading tags; a second, non-receipt nit (stale offsets 40385/52950 → 40398/52963) belongs to `w1/RowS023.md` caveat 5.

```json
{"target":".ufo/waves/round-26/rechecks/S023.json","verdict":"AGREE","severity":"low"}
```
