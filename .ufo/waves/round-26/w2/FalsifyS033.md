# FalsifyS033 — round 26 C1 FRESHNESS, author-side falsification of row S033

Target: receipt `.ufo/waves/round-26/rechecks/S033.json` (verdict HOLD) and the SOURCES.md row
`corpus/SOURCES.md:41` — `| S033 | RFC 9110: HTTP Semantics, media types — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | Content-Type media-type grammar, distinct from S010 validator and S028 URI scopes | Sections 8.3, 8.3.1, 5.6.2 and 5.6.6, June 2022; opened 2026-10-21 | Media types have token type/subtype and optional parameters; nullable omitted headers are distinguished from malformed values by the receipt schema | mined | 2026-10-21 | 365d | corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-24.md |`

Candidate `e28312b14b076584fedd696fae2a684e460bd11e` (base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`).
Milestone: r26-recheck-falsify. Judged on: freshness. Date: 2026-10-21.

**Verdict: AGREE** (HOLD is correct; no correction to the receipt or the row). Severity: **none**.
One **low**-severity precision note on the receipt's `reason` (a mis-described source for a claim it
makes), and one **low**-severity record-keeping note about the statement ledger. Neither changes the
verdict.

## Axes attacked

1. **Digest / live-content freshness** — do the retained bytes still match the row's pin, and does the
   live source still serve them?
2. **Anchor observed in raw bytes** — is the quoted ABNF really at §8.3.1, and are §8.3, §5.6.2, §5.6.6
   present at their cited numbers in the raw file (not just in a normalized view)?
3. **Quote → teaches grounding** — does the quote carry *this* row's teaches, or only page chrome, an
   Appendix A restatement, or a neighbouring clause?
4. **Receipt schema and counter rules** — token/word counts, word-bounded match, row specificity
   (the amendment's `{S010,S028,S033}` document-group rule), and the counter's own per-row verdict.
5. **Consumer drift** — do the citing corpus files still say what the row teaches, and is the append-only
   discipline preserved?

## Evidence

### 1. Digest and live content (freshness) — unchanged, byte-for-byte

Retained bytes decompress to the manifest and population digest:

```
$ zcat .ufo/waves/round-26/fetched/S033-1.raw.gz | sha256sum
21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a  -
$ zcat .ufo/waves/round-26/fetched/S033-1.raw.gz | wc -c
502941
```

This equals the row's own pin (`fetched/manifest.json` row S033 index 1: `status 200`, `error null`,
`bytes 502941`, `sha256 21c1cdce…7232a`, `fetchedAt 2026-10-21T15:10:52.138664+00:00`), the
population entry (`.ufo/waves/round-26/population.json` → S033 → `fetches[0].sha256`), and the digest
recorded for this row at base (`git show 97404de4:corpus/lessons/round-24.md | sed -n '32p'` →
`…source bytes SHA256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a…`).
The receipt's citation of that base line is accurate.

One plain public GET of the row URL (the one allowance in my item; bytes not saved) compared against the
retained copy:

```
$ curl -sS -o /tmp/s033_live.txt -w '__HTTP__ %{http_code} %{content_type} %{size_download}\n' --max-time 60 https://www.rfc-editor.org/rfc/rfc9110.txt
__HTTP__ 200 text/plain;charset=utf-8 502941
$ sha256sum /tmp/s033_live.txt
21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a  /tmp/s033_live.txt
$ cmp /tmp/s033_live.txt /tmp/s033_retained.txt && echo IDENTICAL
IDENTICAL
```

Live bytes are **byte-identical** to the retained bytes and to the row's pin. No content change, and no
version drift visible in the document header itself: raw lines 7 and 11 read `STD: 97` and
`Category: Standards Track … June 2022`, and the header shows no `Updated by` / `Obsoleted by` entry for
this document (the only `Obsoleted by` hits are raw lines 77 and 484 — §1.4 "Specifications Obsoleted by
This Document", the RFC's own table heading). The receipt's "immutable … June 2022" framing holds.

### 2. Anchor observed is correct in the raw bytes

The receipt's `anchorObserved` claims *"§8.3.1 'Media Type', first ABNF block (single-line text view);
§8.3, §5.6.2 'Tokens' and §5.6.6 'Parameters' all present at their cited numbers"*. Verified against
the decompressed raw text, not the normalized view:

```
$ zcat .../S033-1.raw.gz | sed -n '2972,2986p'
2972  8.3.1.  Media Type
...
2980       media-type = type "/" subtype parameters
2981       type       = token
2982       subtype    = token
2984     The type and subtype tokens are case-insensitive.
2986     The type/subtype MAY be followed by semicolon-delimited parameters
```

* §8.3.1 "Media Type" heading at raw 2972, immediately followed by the ABNF block at 2980–2982 — the
  receipt's "first ABNF block" is exactly right.
* §8.3 "Content-Type" heading at raw 2928; §5.6.2 "Tokens" at raw 1728 (`token = 1*tchar` at 1733);
  §5.6.6 "Parameters" at raw 1811 ("Parameters are instances of name/value pairs" at 1813). All four
  cited numbers are present in the raw file, at the cited section numbers.
* The quoted text is **not** page chrome: the RFC text has no per-page furniture, and the quote sits
  inside a numbered section body between two prose paragraphs.

### 3. The quote really grounds THIS row's teaches

Row teaches: *"Media types have token type/subtype and optional parameters; nullable omitted headers are
distinguished from malformed values by the receipt schema."*

**Clause 1 — "token type/subtype and optional parameters" — is grounded by the quote itself.** The quote
is exactly the normalized form of the §8.3.1 ABNF block; I re-derived it from the raw file:

```
$ python3 - <<'EOF'
raw lines 2980-2982 -> "     media-type = type \"/\" subtype parameters\n     type       = token\n     subtype    = token\n"
normalize(...) -> 'media-type = type "/" subtype parameters type = token subtype = token'
EOF
quote == normalized raw block: True
```

So `type = token` and `subtype = token` are literally in the quote, and the "optional parameters" half is
carried by the same §8.3.1 block plus its own follow-on sentence ("The type/subtype **MAY** be followed
by semicolon-delimited parameters (Section 5.6.6) in the form of name/value pairs", raw 2986–2987) and
by §5.6.6's `parameters = *( OWS ";" OWS [ parameter ] )` (raw 1817), whose `*`/optional element is what
makes parameters optional. The receipt's `reason` names exactly this ("§8.3.1 still defines media-type as
token type/subtype plus optional parameters, §5.6.6 still defines name/value parameters") and it is true.

**Clause 2 — "nullable omitted headers are distinguished from malformed values by the receipt schema" — is
a local-policy clause, and the receipt says so rather than pretending the RFC grounds it.** The receipt's
`reason` states: *"§8.3 still says an absent Content-Type lets the recipient assume application/octet-stream"*
(raw 2946–2949, verified: *"If a Content-Type header field is not present, the recipient MAY either assume
a media type of \"application/octet-stream\""*), and then attributes the omitted-vs-malformed distinction
to the receipt schema, not to RFC 9110. That attribution is accurate. The reader does implement it, and
the receipt's line citations are exact at the candidate revision:

* `scripts/receipt_replay.py:210-227` — the `parse_media_type` function and its regex
  (`def parse_media_type` at 218, `_MEDIA_TYPE` at 215), raising `Malformed` for a non-string or a
  grammar violation (224).
* `scripts/receipt_replay.py:395-415` — the validation branch: `absent` is computed at 395, and
  `if "contentType" not in absent and fetch["contentType"] is not None:` at 410 means an **absent** key
  and a **present-but-null** value are both skipped, while a **malformed** value takes the `except
  Malformed` path and appends `fetch.contentType …` (414). That is precisely the three-way distinction
  the row teaches.
* `scripts/` is byte-identical between base and candidate (`git diff --stat <base> <cand> -- scripts/` is
  empty), so the cited line numbers are the same at both revisions.

**The quote is not borrowed boilerplate and not a neighbouring clause.** The 12-word quote occurs exactly
**once** in the committed text view and in the live bytes, and it is not the Appendix A restatement: the
Appendix A collected-ABNF copy of `media-type = type "/" subtype parameters` (raw 9898) is followed there
by `method = token`, not by `type = token` / `subtype = token`, so the 12-word sequence does not form
there (verified: the committed view contains the full 12-word quote exactly once, and the Appendix A
context reads `… media-type = type "/" subtype parameters method = token minute = 2DIGIT …`).

### 4. Receipt schema, quote rules and the counter's own per-row verdict

* Receipt keys are exactly `{id, verdict, fetchIndex, quote, anchorObserved, reason, correction}` —
  `measure.py:52 RECEIPT_KEYS`; `correction: null` is required for HOLD (`measure.py:398-401`).
* `fetchIndex: 1` is a real population fetch of S033 (`population.json` → S033 → `fetches[0].index 1`,
  file `fetched/S033-1.raw.gz`).
* Amendment quote rules: the quote has **12 whitespace words** (≤25) and **9 alphanumeric tokens** (≥6).
* Word-bounded match in the effective fetch text: `quote_in_text` (`measure.py:273-276`) → **True**.
* Row specificity: the quote occurs only in `fetched/text/S033-1.txt` and `fetched/text/S028-1.txt` — both
  members of the declared document group `{S010,S028,S033}` (`measure.py:47 DOCUMENT_GROUPS`; S010 is the
  HTML rendering of the same RFC, S028 the same `.txt` body). It occurs in **no** other population row
  text, so it is not boilerplate; and it differs from S010's quote (*"A strong validator might change for
  reasons other than a change to the representation data"*) and S028's quote (*"with an empty host
  identifier. A recipient that processes such a URI reference MUST reject it as invalid"*), satisfying the
  amendment's "group needs distinct quotes" clause.
* **The lane's own counter, run read-only by me at the candidate revision** (`python3 -B
  .ufo/waves/round-26/measure.py --root . --revision e28312b14b076584fedd696fae2a684e460bd11e`):
  exit **0**, `{"decided": 32, "expected": 32, "hold": 32, "stale": 0, "unverifiable": 0, "statements":
  276, "statementsStale": 8, "statementCorrections": 8, "findings": []}`. At base
  `97404de4ff73d6c8a4f87385cf5fdf36dca7f006` the same command exits **1** with the single finding
  `receipts_absent` and `decided: 0` — the before/after the claim rests on is real.
* I also re-ran the counter's per-row check for S033 alone through the module API
  (`Checker.check("S033", …)` at revision e28312b1): **verdict HOLD, findings `[]`**, quote registered as
  `media-type = type "/" subtype parameters type = token subtype = token`.

### 5. Consumers still say what the row teaches (no missed staleness)

* `corpus/knowledge/static-canonical-preflight.md:159` — *"S033 (RFC9110 §8.3.1 and §5.6.6)"* — the two
  sections it names exist at those numbers in the raw bytes and carry the content the entry uses
  ("The type/subtype MAY be followed by semicolon-delimited parameters (Section 5.6.6) in the form of
  name/value pairs." is verbatim in the committed view, 1 occurrence).
* `corpus/knowledge/static-canonical-preflight.md:174` — the `contentType` bullet the row's clause 2
  underwrites — reads *"contentType permits null for an omitted header (not-served) or an HTTP media-type
  string. Type/subtype comparison is case-insensitive; semicolon parameters may be empty under
  RFC9110…"*. Each RFC-anchored half is supported by the retained bytes: "Type/subtype comparison is
  case-insensitive" ← §8.3.1 raw 2984; "semicolon parameters may be empty" ← §5.6.6's
  `parameters = *( OWS ";" OWS [ parameter ] )`; the null-vs-malformed distinction is the local schema
  policy of `receipt_replay.py` described above.
* `corpus/lessons/round-24.md:17` and `:32` still record S033 as the media-type-grammar source with the
  same digest.
* Append-only discipline holds: `git diff <base> <cand> -- corpus/knowledge/static-canonical-preflight.md`
  contains **no `-` lines** (pure EOF append), and `corpus/SOURCES.md` was changed only by an appended
  round-26 narrative paragraph — the S033 row line itself is byte-identical between base and candidate.
* No S033 correction tag is required: `grep -c "r26-recheck S033" corpus/knowledge/static-canonical-preflight.md`
  → 0, correctly, because the row is HOLD (the counter requires a tag only for STALE,
  `measure.py:393-396`).

## Findings

* **No falsifying finding against the receipt or the row.** The HOLD is grounded in bytes that are
  identical in the retained copy *and* identical on the live source, at the exact cited raw lines, with
  the quote carrying the row's teaches rather than page chrome, an Appendix A restatement, or a
  neighbouring clause.
* **Precision note (low, no verdict effect, no correction):** the receipt's `reason` opens *"Published
  RFC 9110 (STD 97, June 2022) is immutable; today's 200 body sha256 … is identical to the digest
  recorded for this row in corpus/lessons/round-24.md:32"*. The digest comparison and the file/line
  citation are both correct (verified above), but the *reason* for the equality is stated as immutability
  of the published RFC, whereas the operative cause is that the corpus pins the document **by digest**:
  the row is re-checked against a pinned byte hash, and the live endpoint re-serving the same bytes is
  what makes the pin hold. A living document with the same pin would fail this receipt on digest
  mismatch, and the lane's own `corpus/lessons/round-26.md:42` records exactly that distinction for
  another family ("Living documents were judged by quote at anchor, never by sha equality"). The wording
  is a rationale imprecision inside the receipt's free-text `reason`, which the counter does not judge;
  the verdict and every cited fact are right.
* **Record-keeping note (low, no verdict effect, no correction):** the S033 pair seat
  (`w1/PairS033StaticCanonicalPrefl.md:39`) reports *"S033-attributed units: 9. Decided: 6 (HOLD 6,
  STALE 0). UNVERIFIABLE: 3 (rows 2, 4, 9)"*, but `.ufo/waves/round-26/statements.json` records the S033
  entry as `{"statements": 6, "seatStale": 0, "stale": 0, "seatUnverifiable": 0}` — the 3 UNVERIFIABLE
  units are not carried into the ledger, and the ledger's `statements: 6` is the *decided* count, not the
  9 units the seat enumerated. The same pattern holds for S007 (seat report: *"1 statement UNVERIFIABLE
  and not counted"*; ledger `seatUnverifiable: 0`) while S001's 4 UNVERIFIABLE units are carried
  (`seatUnverifiable: 4`). The contract requires only that UNVERIFIABLE be *"reported separately, never
  counted decided"* — which the corpus does for S001 — and S033's three UNVERIFIABLE units are recorded
  in the seat report but nowhere in the corpus or the lesson, and the lesson's UNVERIFIABLE line
  (`corpus/lessons/round-26.md:61`) names only the four v3.0.1 statements. This does not touch the
  receipt's verdict or the row; it is a gap in the round's own statement accounting, and it is the kind of
  gap a ledger field (`seatUnverifiable: 3` for S033) would close. No corpus edit is warranted from this
  seat, which must not write corpus files.

## Residual risk / verification gaps

* The live GET proves the bytes are identical **now**; it cannot by itself prove that no *future* erratum
  will touch §8.3/§8.3.1/§5.6.2/§5.6.6. The lane's own errata scan
  (`w1/PairS033StaticCanonicalPrefl.md`, "Superseded check", same date) records six verified errata
  (7138 §12.5.1, 7306 §14.1.1, 7419 §8.3.2, 7105 App. B.1, 7109 §15.4.9, 8268 App. B.2) plus two
  reported-but-unverified (9162 §5.2, 9164 App. A), none of which touches the four cited sections. I did
  not re-open the RFC Editor errata/info pages: my item's network allowance is one plain GET of the row
  URL, and the row URL's own bytes carry no "Updated by"/"Obsoleted by" line for this document.
* The reverse relation "which RFC updates RFC 9110" is not observable from the retained bytes; the lane
  recorded RFC 9557 → RFC 3339 for a sibling row (S032), and no analogous update is recorded for
  RFC 9110.
* The `w1/PairS033StaticCanonicalPrefl.md` report's character offsets (e.g. §8.3.1 @126997, grammar
  @127331) were computed against the *pre-fix* extractor view (`.ufo/waves/round-26/before/source_text.py`);
  the committed view, regenerated with the fixed extractor, shifts them by +3 to +12 characters (§8.3.1
  @127009, grammar @127343, §8.3 @124873, §5.6.6 @75778, §5.5 @66848). Every cited offset still resolves
  in the *before* view and every quoted sentence still occurs exactly once in the *committed* view, so no
  statement in that report is falsified — but the offsets are stale as pointers into the committed
  `fetched/text/S033-1.txt`. Same for the pair's row-7 quote, whose ABNF spacing (`[ parameter]`) matches
  the before-view form and no longer the committed form. Not a receipt defect: the receipt itself carries
  **no** character offsets, only section-level anchors, and its quote is byte-identical under both
  extractors (1 occurrence each). I did not re-verify the pair report's other rows' quotes beyond
  S033's six (all except row 7 occur exactly once in the committed view).
* I did not run builds, tests or linters; `scripts/receipt_replay.py` was read, not executed, and the
  reader-behaviour claims above are from its source and its own selftest expectations
  (`scripts/receipt_replay.py:768-771, 837-845`), not from a run.
* `measure.py` was run by me read-only (`-B`, no bytecode written) and its own committed verification
  artifacts (`verification/measure-candidate.json`, `verification/measure-candidate-reverify.json`) agree
  with my run: exit 0, 32/32 decided, 0 findings, 276 statements, 8 statement corrections.

## Tooling

No tool was installed or updated (no pacman/uv/pip/cargo action; all pacman transactions are paused
host-wide). Read-only checks used `sha256sum`, `gunzip`/`zcat`, `wc`, `sed -n`, `grep`, `cmp`, one `curl`
plain GET of the row URL (bytes written to a scratch path, then deleted), and one-line `python3 -B`
stdlib calls. The only file I created is this report; I removed the single `__pycache__/*.pyc` byproduct
an in-memory import produced under `.ufo/waves/round-26/before/__pycache__/`. No corpus, script, fleet
repo, sibling lane, lane Git index or jj state was touched; no round-24 wave material was read, run,
retried, rephrased or rerouted.

```json
{"target":".ufo/waves/round-26/rechecks/S033.json + SOURCES.md row S033 (RFC 9110 §8.3/§8.3.1/§5.6.2/§5.6.6)","verdict":"AGREE","severity":"none"}
```
