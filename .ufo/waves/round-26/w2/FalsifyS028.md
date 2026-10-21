# FalsifyS028 — author-side falsification of receipt S028 (verdict HOLD)

Seat: KakeR26-2.FalsifyS028 (leaf member — no dispatch). Milestone r26-recheck-falsify. Axis: **freshness**.
Target receipt: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-26/rechecks/S028.json` (verdict HOLD).
Candidate `e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.
Row: `corpus/SOURCES.md:36`.

**Verdict: AGREE (severity: low).** The HOLD survives every falsification attack I ran and must **not** be
flipped: the quoted sentence is verbatim in the retained bytes at the exact raw lines the receipt names, it
grounds *this* row's `teaches` (both the http and the https half), the live source today is byte-identical to
the retained bytes and to the digest pinned at row open, and no erratum touches the cited sections. The one
actionable defect is **not in the receipt** — it is a stale text-view digest, size, and set of character
offsets published by the row's own statement-level seat, `.ufo/waves/round-26/w1/PairS028StaticCanonicalPrefl.md`,
which describes a view that the same candidate commit superseded. Same defect class as sibling
`w2/FalsifyS010.md` (stale digest in `w1/RowS010.md` → AGREE/low) and `w2/FalsifyS034.md` (same class in
`w1/PairS034StaticCanonicalPrefl.md` → DISAGREE/low). For S028 the stale numbers never entered the receipt,
so AGREE/low is the consistent label.

---

## Axes named

1. **Grounding** — does the receipt's quote ground *this* row's `teaches` ("A recipient must reject an http or
   https URI reference with an empty host identifier as invalid"), or only page chrome / a neighbouring clause?
2. **Anchor correctness in raw bytes** — is the quoted sentence really at raw lines 1106-1108 and 1135-1137 of
   `fetched/S028-1.raw.gz`, inside §§4.2.1/4.2.2, and does the receipt's `anchorObserved` resolve against the
   artifact it names?
3. **Content/version drift** — did the source change since the row was opened, in a way the receipt missed?
4. **Evidence-pointer integrity** — do the numbers the receipt's own seat published (digest, size, offsets)
   describe the committed artifacts?
5. **Counter / schema compliance** — does the receipt satisfy the amendment's quote rules and `measure.py`'s
   checks (token/word counts, word-bounded match, row specificity)?

## Evidence

### 1. Digest, live content, and version freshness — CONFIRMED

Retained bytes:

```
$ gunzip -c .ufo/waves/round-26/fetched/S028-1.raw.gz | sha256sum
21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a  -
$ gunzip -c .ufo/waves/round-26/fetched/S028-1.raw.gz | wc -c
502941
```

Matches `fetched/manifest.json` (S028/index 1: `status 200`, `bytes 502941`, same sha256,
`fetchedAt 2026-10-21T15:10:49.556871+00:00`, `finalUrl` == the row URL, no redirect, no error) and
`population.json` (S028 `fetches[0].sha256` = the same digest, `fetches[0].index` = 1, matching the
receipt's `fetchIndex: 1`). Matches the row's own pin in `corpus/SOURCES.md:36` ("plain text sha256
21c1cdce…7232a"). The `SOURCES.md` row line is byte-identical at base and candidate:

```
$ git show 97404de…:corpus/SOURCES.md | grep "^| S028 |" | sha256sum
0c6bf14506fd5949a09d0cd54d18694eddb7b99f5313b50ca50edcb5f49e754c  -
$ git show e28312b…:corpus/SOURCES.md | grep "^| S028 |" | sha256sum
0c6bf14506fd5949a09d0cd54d18694eddb7b99f5313b50ca50edcb5f49e754c  -
```

Plain public GET of the row URL (the one allowance; not saved, nothing else contacted):

```
$ curl -sS --max-time 60 -o /dev/stdout https://www.rfc-editor.org/rfc/rfc9110.txt | sha256sum
21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a  -
```

Live bytes are **byte-identical** to the retained bytes and to the pin. The document header is unchanged
(`STD: 97`, `Obsoletes: 2818, 7230, 7231, 7232, 7233, 7235, 7538, 7615, 7694`, `Updates: 3864`, `June 2022`),
so the receipt's "immutable June 2022 STD 97 text" is right. No `Obsoleted by` / `Updated by` marker appears in
the retained raw text, and the round's own errata sweep (`w1/PairS028StaticCanonicalPrefl.md`, "Superseded-anchor
check") records no erratum against §§4.1-4.3; the only §4.2.1/§4.2.2 mention is reported (unverified, editorial)
erratum 9164, which concerns the Appendix A collected-ABNF notation for `http-URI`/`https-URI` — confirmed
here to be a notation difference between body (raw line 1096: `http-URI = "http" "://" authority path-abempty
[ "?" query ]`) and Appendix A (raw line 9885: `http-URI = "http://" authority path-abempty [ "?" query ]`),
not a change to the prose requirement the row teaches. **No content or version drift.** STALE is not
supportable for this row.

### 2. Anchor observed is correct in the raw bytes — CONFIRMED

The receipt's `anchorObserved` names raw-text lines 1106-1108 (§4.2.1) and 1135-1137 (§4.2.2). Verified in the
retained raw bytes:

```
$ gunzip -c .ufo/waves/round-26/fetched/S028-1.raw.gz | sed -n '1106,1108p'
   A sender MUST NOT generate an "http" URI with an empty host
   identifier.  A recipient that processes such a URI reference MUST
   reject it as invalid.
$ gunzip -c .ufo/waves/round-26/fetched/S028-1.raw.gz | sed -n '1135,1137p'
   A sender MUST NOT generate an "https" URI with an empty host
   identifier.  A recipient that processes such a URI reference MUST
   reject it as invalid.
$ gunzip -c .ufo/waves/round-26/fetched/S028-1.raw.gz | sed -n '1090p;1113p'
4.2.1.  http URI Scheme
4.2.2.  https URI Scheme
```

The receipt's quote is the normalized form of exactly those paragraphs, and both headings sit immediately above
their respective paragraphs. The receipt's "text view line 1" is also right: the committed view is one line
(`wc -c` 457,411; a single trailing LF).

### 3. Quote grounds this row's teaches, not a neighbouring clause — CONFIRMED

- The quote is **not** chrome and **not** a neighbouring clause: it is the operative recipient requirement of
  the empty-host paragraph, and `grep -c "empty host"` in the raw text returns **2** — one in §4.2.1, one in
  §4.2.2, no other occurrence anywhere in RFC 9110.
- The row's `teaches` is *"A recipient must reject an http **or https** URI reference with an empty host
  identifier as invalid"*, i.e. it asserts the rule for **both** schemes. The quoted sentence is scheme-neutral
  and occurs **twice**, once under each scheme heading, so the same quote legitimately grounds both halves.
  Occurrences in the committed view: offsets 44947 and 46307.
- No contamination from another row: the quote occurs in exactly three retained raws — `S010-1.raw.gz` (2),
  `S028-1.raw.gz` (2), `S033-1.raw.gz` (2) — all three being the same RFC 9110, i.e. the declared document
  group `{S010, S028, S033}` in `measure.py` (`DOCUMENT_GROUPS`). No other population row's bytes contain it.
- Within the group the three quotes are distinct: S010 "A strong validator might change for reasons other than
  a change to the representation data", S028 (this quote), S033 "media-type = type \"/\" subtype parameters
  type = token subtype = token". `measure.py`'s `quote_not_row_specific` check therefore passes.
- Amendment quote rules: 18 whitespace words, 18 alphanumeric tokens — within ">=6 tokens and <=25 words".
  Word-bounded match in the effective fetch text holds.
- The only "sensitivity" the receipt's own seat flagged is a precision note, not a defect: the paraphrase
  drops the RFC condition "that processes such a URI reference" (`w1/PairS028StaticCanonicalPrefl.md:36`).
  The corpus statement at `corpus/knowledge/static-canonical-preflight.md:83-85` ("RFC 9110 sections 4.2.1-4.2.2
  require a recipient to reject an http(s) URI with an empty host as invalid (S028)") is a faithful rendering of
  the MUST, and the dropped condition does not bite because the validator processes every reference it rejects.

### 4. Consumer drift — none found

`corpus/knowledge/static-canonical-preflight.md:83-85` still renders the requirement exactly (verified at the
candidate: lines 83-85 read "so the reference carries an empty authority, and RFC 9110 sections 4.2.1-4.2.2 /
require a recipient to reject an http(s) URI with an empty host as invalid / (S028)"). `corpus/lessons/round-22.md:183`
still quotes the identical sentence — "Section 4.2.1 (same in 4.2.2): 'A recipient that processes such a URI
reference MUST reject it as invalid.'" — which is verbatim present at both anchors; and
`corpus/lessons/round-22-verifier-spotcheck.md:123` records the same digest `21c1cdce…7232a`, which equals the
bytes re-fetched today. No statement attributed to S028 is stale; the ledger's S028 pair
(`statements.json`: `{"row":"S028","file":"corpus/knowledge/static-canonical-preflight.md","statements":6,
"seatStale":0,"stale":0,"seatUnverifiable":0}`) is consistent with the six HOLD verdicts tabulated at
`w1/PairS028StaticCanonicalPrefl.md:19-24`.

### 5. Receipt schema and counter — CONFIRMED

Receipt keys are exactly the seven `RECEIPT_KEYS` (`measure.py:41`); `id` matches the file name; `verdict` is a
member of `VERDICTS`; `correction` is `null` on a HOLD; `reason` and `anchorObserved` are non-empty strings;
`fetchIndex` 1 is a population fetch of S028; the quote is a word-bounded normalized substring of the effective
fetch text. Counter at the candidate:

```
$ python3 -B .ufo/waves/round-26/measure.py --root . --revision e28312b14b076584fedd696fae2a684e460bd11e
{"decided": 32, "expected": 32, "findings": [], "hold": 32, "populationSha256": "16330e1e…", "populationSource":
"revision", "revision": "e28312b…", "rows": [], "schema": "kake-source-recheck-v1", "stale": 0,
"statementCorrections": 8, "statements": 276, "statementsStale": 8, "unverifiable": 0}
exit=0
```

Base for contrast: `decided 0`, finding `receipts_absent`. `S028` carries no `[r26-recheck S028 STALE]` tag in
`corpus/**` (correct: the row is HOLD, and no S028 statement was adjudicated stale).

---

## Finding (actionable, not in the receipt): stale text-view digest, size and offsets in the S028 seat report

`w1/PairS028StaticCanonicalPrefl.md` publishes numbers for `fetched/text/S028-1.txt` that do not describe the
committed blob at the candidate:

| Claim in `w1/PairS028StaticCanonicalPrefl.md` | Committed artifact at candidate `e28312b…` |
|---|---|
| `:13` "457,337 bytes, sha256 `93a20ab9e35d1a59d3d370ed9fc89d2b4a62c45a4a7d5560218bc532c2757853`" | 457,411 bytes, sha256 `0dd1b33b4d2bb7bc585f662bf593576bb005fb6bd348dc6aee9a4bbeda661d2b` |
| `:30` "§4.2.1 at col 44184" | the heading is at col **44185**; col 44184 lands on the preceding space |
| `:34` "§4.2.1 requirement at col 44913; same sentence in §4.2.2 at col 46271" | the requirement starts at **44915** and **46274**; the claimed cols land 2 and 3 characters early, mid-token |
| `:36` "(col 44913)" / "(col 46271)" | same as above |
| `:34` recipient sentence "col 44976" | starts at **44978** |

Reproduction (the claimed values are the *pre-amendment* view; the committed view is the post-amendment one):

```
$ python3 - <<'PY'
import gzip, importlib.util, hashlib
def load(p,n):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
old=load('.ufo/waves/round-26/before/source_text.py','old')
raw=gzip.decompress(open('.ufo/waves/round-26/fetched/S028-1.raw.gz','rb').read())
t=old.normalize(old.text_of(raw,'text/plain;charset=utf-8'))
print(len((t+'\n').encode()), hashlib.sha256((t+'\n').encode()).hexdigest())
PY
457337 93a20ab9e35d1a59d3d370ed9fc89d2b4a62c45a4a7d5560218bc532c2757853
```

i.e. the seat report's digest is exactly the output of the **retired** extractor `before/source_text.py`. The
cause is the amendment `.ufo/waves/round-26/contract-amendment.json:15` — "source_text.py: single entity decode
… and no `]` spacing rule; before copy retained at before/source_text.py; 18 text views regenerated and all 32
receipt quotes re-found". RFC 9110's plain text contains 74 `]` tokens, so dropping `]` from the whitespace-before-
punctuation class lengthened this view by exactly 74 characters:

```
old view: 457,302 chars / 457,337 B (sha 93a20ab9…)
new view: 457,376 chars / 457,411 B (sha 0dd1b33b…)   <- committed
```

The offsets diverge accordingly: `44913→44915`, `44976→44978`, `46271→46274`, `44184→44185` (the first `]`
occurs after col 3319 and after col 230, which is why the TOC offset 3319 and the RFC-header offset 230 still
resolve unchanged in the committed view — they are the only two that do).

**Scope.** This is wave-wide, not S028-specific. Auditing every full 64-hex text-view digest published by the
`w1/Pair*.md` seats against the committed blobs, **eight** pair reports publish a digest that reproduces the
pre-amendment view rather than the committed one: `PairS006`, `PairS011`, `PairS012`, `PairS020`, `PairS028`,
`PairS030`, `PairS031`, `PairS034`. (`w1/RowS033.md:4` carries the same stale `93a20ab9…` for the identical
RFC 9110 view.) `w2/FalsifyS034.md:87` asserts that S034 is "the only pair report that states a digest for the
committed text view that contradicts the committed blob" — that is **wrong**; there are eight, and S028 is one
of them. `w2/FalsifyS010.md:185` already flagged the `RowS033.md` instance as a wave-level note; it did not
cover `PairS028StaticCanonicalPrefl.md`.

**Why the counter cannot see it.** `measure.py` recomputes each fetch's text view from the *raw* bytes through
the revision's `source_text.py` (`measure.py:300-330`, `:262-266`) and validates the quote as a word-bounded
normalized substring (`measure.py:273-276`, used at `:391-392`); it never reads `fetched/text/*.txt` and never
checks `anchorObserved` for numeric accuracy beyond being a non-empty string (`measure.py:365-370`). So the
committed views' correctness is enforced elsewhere — `text_selftest.py:135-150` asserts each committed view
equals `text_of(raw)+LF` under the current extractor, which is why the committed views are right and the
*reports* about them are stale. The counter's exit 0 certifies quote presence, not the seat reports' published
coordinates.

**Minimal correction (one w1 artifact; no receipt, corpus, SOURCES, script or manifest change).** In
`w1/PairS028StaticCanonicalPrefl.md`:

- `:13` — replace "457,337 bytes, sha256 `93a20ab9e35d1a59d3d370ed9fc89d2b4a62c45a4a7d5560218bc532c2757853`"
  with "457,411 bytes, sha256 `0dd1b33b4d2bb7bc585f662bf593576bb005fb6bd348dc6aee9a4bbeda661d2b`".
- `:30` — "col 44184" → "col 44185".
- `:34` — "col 44913" → "col 44915"; "col 46271" → "col 46274".
- `:36` — "(col 44913)" → "(col 44915)"; "(col 46271)" → "(col 46274)"; "col 44976" → "col 44978".

No change to `rechecks/S028.json`: its `anchorObserved` cites **raw-text line numbers** (1106-1108, 1135-1137),
which are correct against `fetched/S028-1.raw.gz`, and it carries no digest, size or character offset. If L1
wants offsets to be trustworthy evidence in future rounds, they need either re-derivation after every text-view
regeneration or an explicit view digest inside each `anchorObserved` — today the field is prose the counter
never verifies.

---

## Residual risk and verification gaps (not actionable by this seat)

1. **Errata coverage of the S028 sections is second-hand here.** I confirmed errata *impact* by reading the
   retained raw bytes against the taught sentences and by checking the body's `http-URI`/`https-URI` ABNF against
   Appendix A's, but the erratum list and its statuses come from `w1/PairS028StaticCanonicalPrefl.md`'s
   "Superseded-anchor check". My own network use was one plain GET of the row URL already in `corpus/SOURCES.md`
   (rfc9110.txt); a documentation search that surfaced the RFC Editor errata index was used only as a
   cross-check and was not saved. If the integrator wants the receipt itself to carry errata state, re-verify the
   list at the source before writing it in.
2. **Statement-seat coverage gap for `corpus/lessons/round-22.md`.** S028's `usedBy` lists
   `corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-22.md`, and the seat report itself notes
   at `w1/PairS028StaticCanonicalPrefl.md:60` that the lessons file "is outside this pair and needs its own
   seat". No `statements.json` pair covers any `corpus/lessons/**` file for any row in this wave. The S028
   lessons claim is nonetheless accurate against today's bytes (verified above), so this is a coverage
   observation, not a stale statement — but the wave's `claim.after` ("knowledge-entry claims citing the rows
   rechecked") reads as covering knowledge entries only, and the lessons-file half of `usedBy` is unadjudicated.
3. **Single-snapshot limit.** Byte identity of a live GET proves the document did not change between the
   fetch (2026-10-21T15:10:49Z) and my GET today; it cannot rule out a change made after my GET, nor any
   erratum filed later.
4. **Bound interpretation disclosed.** I did not open, run, retry, rephrase or reroute any round-24 assignment,
   probe, counter or `.ufo/waves/round-24/` material, and no round-24 content was used as evidence. I read
   `corpus/lessons/round-22.md`, `corpus/lessons/round-22-verifier-spotcheck.md` and
   `corpus/lessons/round-26.md` because they are S028's own `usedBy` consumers; the S033 receipt quotes a
   round-24 path, but that receipt is a wave artifact I read as a sibling, not round-24 material.

## Tooling

No tool was installed, updated or removed; no pacman transaction was attempted (all pacman transactions are
paused host-wide). Everything used was already present: `python3` 3.14.8 (stdlib only: `gzip`, `hashlib`, `re`,
`types`, `importlib`, `json`, `glob`, `os`), `git` 2.56.0, `curl` 8.23.0, `gzip` 1.15, `sha256sum` 0.8.0,
`grep`/`sed`. The counter `measure.py` was executed read-only at both revisions (base and candidate) — it reads
committed blobs and writes nothing. No file was written except this report; no corpus file, script, fleet repo,
sibling lane, lane Git index or jj state was mutated; no `/tmp` or out-of-lane write occurred.

```json
{"target":".ufo/waves/round-26/rechecks/S028.json","verdict":"AGREE","severity":"low"}
```
