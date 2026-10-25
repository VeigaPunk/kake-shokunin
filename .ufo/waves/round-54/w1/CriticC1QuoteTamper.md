# CriticC1QuoteTamper — C1 (S374 crawl-qualifier) quote/date/body tamper review

Seat: L1Kake54.CriticC1QuoteTamper · Round 54, wave w1 · 2026-10-25
Scope: try to make C1 accept (a) a paraphrase that no longer quotes S374, (b) a
malformed marker date, (c) a source body with missing quote. Findings only.

## Method

Real gate = `.ufo/waves/round-54/c54_s374_calib.py` run with
`--root <fixture repo> --revision <committed rev>` — the same committed-bytes
path the wave uses (`git show <rev>:<path>`). Fixture rig: a scratch git repo in
/tmp holding only `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` +
`.ufo/waves/round-52/sources/S374.html`; each variant committed as its own
revision; ~25 variants run. No lane bytes modified; lane tree only read.

## Counter instability note (material to all findings)

The gate was rewritten while this review ran — three distinct worktree versions
observed in one session despite the wave's "no concurrent writers" note:

- v_old (committed @8e408e0): unanchored literal-marker finditer, 1200-char
  forward window, `pos < corr_at` mismatch direction.
- v_mid (md5 abcc8639): `qualifier_findings` + `BASE_RENDER` count added, but
  `run_checks` lost its `mismatch =` line → `UnboundLocalError` on EVERY path
  (rc=1 traceback, indistinguishable from met=False); selftest also red on its
  own `corrected` fixture (fixture lacked the quote the new code requires).
- v_now (md5 6e214fc5, tested head): crash fixed, selftest fixture updated.

All acceptance results below were reproduced on the final version; the gate
evaluated is therefore the current worktree file, not any committed revision.
A canonical judge should pin counter+selftest bytes before trusting receipts.

## Result matrix (final gate version, md5 6e214fc5)

| variant | verdict | why |
|---|---|---|
| P0 honest corrected entry | met=True exit 0 | expected pass; also passes at real tip `8e408e0` |
| N0 base @68228b2 | exit 1 | do-nothing control holds: `mismatches=1 met=False` |
| A1 correction paraphrased, quote removed from claim text | exit 1 | rejected |
| A4 pure paraphrase, quote nowhere in correction section | exit 1 | rejected |
| A2 unbolded marker `​[r54-correction …]` at file top | exit 1 | rejected (marker regex requires `^**…**`) |
| **D2 paraphrased claim + exact quote in a trailing "reference" line, same section** | **met=True exit 0** | ACCEPTED |
| **D1 marker + word-soup section (no S374 repair asserted at all)** | **met=True exit 0** | ACCEPTED |
| **D3 entire correction inside an HTML comment (renders as nothing)** | **met=True exit 0** | ACCEPTED |
| **D4 correction inside a fenced code block under "## Scratch notes"** | **met=True exit 0** | ACCEPTED |
| B1 `2026/10/25`, B2 `2026-10-26`, B5 `2026-10-25T00:00`, B6 `25-10-2026` (alone) | exit 1 | rejected |
| **D5b visible `2026/10/25` correction + valid bold marker hidden in `<!-- -->` in same section** | **met=True exit 0** | ACCEPTED |
| B7 marker + quote + crawl claim but no "earlier rendering/endorsement/supersedes/gloss" | exit 1 | rejected |
| A5 fresh `(rendered: …vouch…)` suspect appended after the correction | exit 1 | rejected (`corr_at <= end` now catches post-correction suspects) |
| **F1 fresh false gloss appended, vocabulary escaping `SEMANTIC_RE`** | **met=True exit 0** | ACCEPTED |
| **F2 "not recommend the crawl" inside a sentence that DENIES that reading** | **met=True exit 0** | ACCEPTED |
| E1 honest correction that quotes the old gloss verbatim | exit 1 | over-strict reject (`base_render_count=2`) |
| E2 old gloss duplicated verbatim in a "## Changelog" tail | exit 1 | over-strict reject (`suspect_cells=2`) |
| C1 body with quote absent | exit 2 | rejected (unevaluable) |
| C4 body with zero-width space injected inside quote | exit 2 | rejected (raw substring holds; no normalization bypass) |
| **C2 quote relocated from its paragraph into `<!-- … -->` at EOF** | **met=True exit 0** | ACCEPTED |
| **C3 body replaced by the bare 28-char quote alone** | **met=True exit 0** | ACCEPTED |
| **C5 rel=nofollow paragraph reworded, quote stashed in a `<script>` JSON blob** | **met=True exit 0** | ACCEPTED |

## Findings

### F-A1 — Paraphrase acceptance via section-scope quote borrowing (contract breach, ACCEPTED)

`qualifier_findings` defines a correction "block" as marker → next `^## ` or
EOF, then checks `QUOTE in block`. The quote does not have to occur in the
correction claim — anywhere in the section satisfies it. D2's claim text is a
pure paraphrase ("the site owner does not recommend the crawl…"); the literal
quote survives only in an appendix/reference line. Verdict: `met=True`.

The frozen contract (contract.md:22-25) requires the correction block to quote
the exact source substring and state the crawl qualifier. Section-scope is not
block-scope: the gate cannot distinguish "the correction quotes S374" from "a
quote happens to live later in the same section." The same looseness admits D1
(word-soup section that asserts no repair at all — `earlier rendering …
endorsement … supersedes … gloss` is satisfied by three unrelated sentences) and
F2 (the required phrase `not recommend the crawl` is matched inside a sentence
that explicitly denies that reading — `NEGATIVE_CRAWL_RE` has no polarity).

Impacted axes: verdict truth (met=True on a file that never makes the pinned
claim), quote binding.

Smallest safe correction: require `QUOTE` between the marker and the end of the
*claim paragraph* (or within N chars before `NEGATIVE_CRAWL_RE`'s match), not
merely in the section; add a selftest case for the appendix-quote shape.

### F-A2 — Correction markers honored inside HTML comments and code fences (ACCEPTED)

`CORRECTION_MARK_RE` is `(?m)^\*\*\[r54-correction 2026-10-25\]\*\*` — a line
anchor only. A fully valid correction inside `<!-- … -->` (D3: no visible
repair exists, met=True) or inside a fenced block under a "Scratch notes"
heading (D4) satisfies the gate. Rendered-document semantics and gate semantics
diverge: the entry can visibly contain zero correction while the gate reports
one.

Impacted axes: verdict truth, false provenance (gate attests a repair the
rendered entry does not show).

Smallest safe correction: strip fenced code blocks and HTML comments before
scanning, or require the marker line to be outside them (cheap: skip lines
inside ``` fences / between `<!--` and `-->`).

### F-B1 — Malformed visible marker date accepted when an inert valid marker coexists (ACCEPTED)

Date rejection only works when the malformed marker is the *only* marker. With
a valid `**[r54-correction 2026-10-25]**` hidden in an HTML comment inside the
correction section, a visible correction headed `**[r54-correction
2026/10/25]**` passes (`corr_at` = the hidden marker; the malformed one is never
inspected — `finditer` stops at the first *pattern-valid* hit). The date is
enforced on the first matching line, not on every line claiming the role.

Impacted axes: verdict truth, duplicate authority (two lines claim correction
status; only the invisible one is validated).

Smallest safe correction: after finding the satisfying marker, scan the file
for *any* `[r54-correction` literal whose date ≠ `2026-10-25` (or whose marker
line isn't the accepted one) and report it as a finding — presence of a
malformed sibling marker should poison the verdict.

### F-B2 — Correct date rejections: B1/B2/B5/B6/B7 all exit 1. Bare/unbolded marker (A2) also rejected. No acceptance found for a malformed date standing alone.

### F-C1 — Body quote check is presence-only; pinned provenance is unverified (ACCEPTED)

C1.1 is `QUOTE in body` — no position, no context, and **the contract-pinned
sha256 `3ad358bdbe7a74798df151c282e4b57af7475686dc405b3f8bad08f68881aecb`
(contract.md:74-76, echoed in the entry itself) is never checked**. Consequences,
all `met=True`:
- quote moved out of the `rel=nofollow` paragraph into an EOF HTML comment (C2);
- body gutted to the bare quote (C3) — the "source" is 29 bytes and still pins;
- paragraph reworded with the quote stashed in a `<script>` blob (C5) — a body
  that would not support the claim at all still anchors it.

The counter can therefore be satisfied by a source body that does not contain
the quote *as evidence* — only as a string.

Impacted axes: quote binding, false provenance (the strongest finding in this
family — the pinned hash exists precisely to prevent it and is unused).

Smallest safe correction: `hashlib.sha256(body_raw).hexdigest() == PINNED` in
C1.1 (one line; the hash is already in the contract and the entry); treat any
other body as exit 2 with an explicit "body digest mismatch" note.

### F-C2 — Missing quote exits 2 (unevaluable), not a failure — downgrade ambiguity

A body lacking the quote yields `EXIT=2`. Per the kill rule that is
"unevaluable", which is correct for a *missing file* but wrong for *present
bytes that don't contain the pinned evidence*: a swapped/forged source that
simply drops the phrase reports identically to an unreadable one. An admission
pipeline that treats only `exit==0` as pass is safe here, but any lane that
treats `!=1` as "needs recheck" launders a tampered body into a retry.

Smallest safe correction: distinct exit for "body present, quote absent"
(e.g. keep exit 2 for unreadable/missing; make present-but-quoteless a hard
exit 1 with `occurrences=0`), or record `body_sha256` in the C1.1 facts so a
judge can distinguish.

### F-D — Supplementary accepts/rejects outside the three assigned families

- **F1 accepted**: a fresh false gloss appended after the correction using
  vocabulary outside `SEMANTIC_RE` ("declines to stand behind or put forward")
  is invisible — `met=True` coexists with a live, un-superseded misrendering.
  The suspect vocabulary is a fixed wordlist; paraphrased misrenderings escape.
- **E1/E2 rejected (over-strict)**: `entry.count(BASE_RENDER) != 1` adds a
  mismatch whenever the old gloss text is quoted verbatim anywhere — including
  inside the correction itself as an explicit quote of what is being corrected
  (a natural way to write the repair). Also, the duplicate literal re-matches
  `RENDER_RE`, doubling `suspect_cells`. Preservation check conflates
  "unchanged" with "appears once as a suspect cell".
- **A5 rejected**: re-asserting a suspect cell after the correction is now
  caught (`corr_at <= end`) — direction flip from v_old, good.
- **C1.2_cells double-duty**: `add("C1.2_cells", base_copy_count == 1, …)`
  reports a preservation violation as a cells-check failure; minor receipt
  wart.

### F-E — Gate/selftest divergence and receipt drift

- v_mid crashed on every path (`UnboundLocalError: mismatch`) while its own
  selftest could still print `ok` for cases run through `run_checks_fix` — the
  selftest exercises a parallel path, not the gate's; a crash in `run_checks`
  is invisible to `--selftest` and exits 1 like a normal not-met.
- `controls/c1-selftest.txt` was committed with 5 cases, then 8; the live
  selftest currently emits 9 (`correction_removed_render` added last). The
  committed receipt is stale against the current script — run receipts against
  the same bytes they describe.

## Verdict

C1 **can be made to accept** all three tamper classes, under the current gate:

- paraphrase-without-quote: accepted via section-scope quote borrowing (D2, D1, F2);
- malformed marker date: accepted when a valid marker is parked inertly (D5b);
- body "missing" the quote: accepted when the quote is present but
  non-evidentiary (C2, C3, C5); the pinned sha256 is never verified.

The honest positive (tip `8e408e0`) and base do-nothing control both hold, and
the plain-shape tampers (paraphrased claim alone, malformed date alone,
missing quote, ZWSS in quote, post-correction suspect re-assertion) are all
correctly rejected — the holes are structural-scope holes, not regex gaps.

Tool installs: none. Scratch rig under /tmp/c1tamp only; no lane bytes written.
