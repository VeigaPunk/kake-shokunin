# ScoutRound50Precedent — S273 collapsed-only precedent vs round-63 S432 admission

Seat verdict: the round-63 S432 admission uses the same three-class semantics as the
round-50 S273 precedent, mechanically re-derived from committed bytes. No semantic
drift in the class decision procedure; the differences between the two rounds are
provenance tightening and adjudication posture, both named below.

## Evidence (absolute paths, exact commands)

### 1. Round-50 criterion (the precedent)

- `corpus/QUALITY.md:1100-1108` (criterion header at 1100):
  "A quote's match class is derived from its own two blobs, never asserted (round 50).
  A quoted span's class is derived by comparing the span against both retained blobs
  of that id: a span that is a substring of the retained HTML is `raw-substring`, a
  span that survives only whitespace collapse is `collapsed-only`. The class is
  recorded together with the sha256 of both blobs, and a collapsed-only span is never
  described as a raw substring nor the reverse — the two classes are different facts
  and a swapped label fails the check."
- `kake-shokunin/.ufo/waves/round-50/c50_quote_class.py` R2 docstring (lines 33-35):
  "Derived class is raw-substring when the quote is a substring of both blobs, and
  collapsed-only when it is a substring of the text blob only." (`BLOBS` map at lines
  44-48: S273/S274 blobs under `.ufo/waves/round-49/sources/`, S286 under round-50.)
- `kake-shokunin/.ufo/waves/round-50/quote-classes.json`: S273 `matchClass`
  `collapsed-only`; S274, S286 `raw-substring`; per-id `textSha256`/`rawSha256` pins.
- `kake-shokunin/corpus/knowledge/crawl-budget-consequences.md` quotes the S273 span
  verbatim: "Google won't shift this newly available crawl budget to other pages
  unless Google is already hitting your site's crawl capacity limit. (S273)".

### 2. S273 precedent re-derived end-to-end (this seat, 2026-10-27)

Command (run from `/home/vgpnk/Projects/shokunin/kake-shokunin`):

```
python3 -B - <<'EOF'   # re-derives all three round-50 ids from their retained blobs
import json, pathlib, hashlib
q50 = json.loads(pathlib.Path(".ufo/waves/round-50/quote-classes.json").read_text())
BLOBS = {
 "S273": (".ufo/waves/round-49/sources/S273.txt", ".ufo/waves/round-49/sources/S273.raw.html"),
 "S274": (".ufo/waves/round-49/sources/S274.txt", ".ufo/waves/round-49/sources/S274.raw.html"),
 "S286": (".ufo/waves/round-50/sources/S286.txt", ".ufo/waves/round-50/sources/S286.raw.html"),
}
for c in q50["classes"]:
    tp, rp = BLOBS[c["id"]]
    text = pathlib.Path(tp).read_text(); raw = pathlib.Path(rp).read_bytes()
    q = c["quote"]
    derived = "raw-substring" if q in raw.decode("utf-8","replace") else ("collapsed-only" if q in text else "absent")
    th = hashlib.sha256(text.encode()).hexdigest(); rh = hashlib.sha256(raw).hexdigest()
    print(c["id"], "recorded:", c["matchClass"], "derived:", derived, "AGREE/DRIFT",
          "| textSha ok:", th==c["textSha256"], "rawSha ok:", rh==c["rawSha256"])
EOF
```

Output:

```
S273 recorded: collapsed-only derived: collapsed-only AGREE | textSha ok: True rawSha ok: True
S274 recorded: raw-substring derived: raw-substring AGREE | textSha ok: True rawSha ok: True
S286 recorded: raw-substring derived: raw-substring AGREE | textSha ok: True rawSha ok: True
```

So the S273 collapsed-only label is itself a derived fact under the same recipe the
round-63 seat applies to S432: the S273 quote is a substring of the flat-text blob
`.ufo/waves/round-49/sources/S273.txt` and not of the raw HTML blob
`.ufo/waves/round-49/sources/S273.raw.html` (same membership test as below).

### 3. Round-63 S432 admission — same semantics, same derivation

- `kake-shokunin/.ufo/waves/round-63/quote-class/quote-classes.json`
  (sha256 `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d`,
  confirmed identical to the contract's pinned value by
  `sha256sum .ufo/waves/round-63/quote-class/quote-classes.json`):
  S432 `matchClass` `collapsed-only`, `textPath` `.ufo/waves/round-63/quote-class/S432.txt`,
  `rawPath` `.ufo/waves/round-61/sources/S432.html`, pins
  `textSha256 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69`,
  `rawSha256 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`,
  `locatedRawLines 6150-6154`, note "the span is a substring of the committed
  flat-text rendering only, which is the collapsed-only class of corpus/QUALITY.md
  round 50."
- Pin re-derivation (`sha256sum` from repo root):

  ```
  8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .ufo/waves/round-63/quote-class/S432.txt
  63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html
  ```

  Both equal the ledger pins. The same raw sha `63b0a018…911b` is the S432 receipt
  digest recorded in `corpus/knowledge/response-header-expectations.md:4`.
- Class membership (mechanical, from repo root):

  ```
  quote in raw-substring form: False
  quote in flat text        : True
  quote in raw bytes        : False
  ```

  Raw HTML context (raw bytes around the purpose sentence, line 6150-6154 region):
  `The\n`<dfn class="dfn-paneled" data-dfn-type="http-header" ...><code>X-Content-Type-Options</code></dfn>`\nresponse <a ...>header</a> can be used to require checking of a <a ...>response</a>’s\n`<code>Content-Type</code>` ...` — inline element boundaries and newlines sit inside
  the sentence, so the verbatim span cannot be a raw substring; it survives only in
  the flat-text rendering. This is byte-for-byte the same situation as S273.
- Independent tool derivation (`scripts/quote_class.py`, frozen sha256
  `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14`, confirmed):

  ```
  $ python3 -B scripts/quote_class.py classify --quote 'The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.' --raw .ufo/waves/round-61/sources/S432.html --text .ufo/waves/round-63/quote-class/S432.txt
  derived=collapsed-only
  $ python3 -B scripts/quote_class.py --selftest
  case inline_raw_substring: derived=raw-substring expected=raw-substring pass
  case markup_collapsed_only: derived=collapsed-only expected=collapsed-only pass
  case absent_everywhere: derived=absent expected=absent pass
  case s432_real: derived=collapsed-only expected=collapsed-only pass
  selftest 4/4
  ```

  `classify()` at `scripts/quote_class.py:34-38` is the identical predicate to
  round-50 R2: raw-substring iff quote ∈ raw HTML; else collapsed-only iff quote ∈
  flat text; else `absent`. Raw is checked first, so the two positive classes are
  mutually exclusive; a swapped label fails (round-50 blur control,
  `.ufo/waves/round-50/verification/blur-control.txt`, cited at QUALITY.md:1108).
- Rendering recipe fidelity: `.ufo/waves/round-63/quote-class/extract_text.py`
  (`--selftest` → `selftest 1/1`); re-running
  `python3 -B .ufo/waves/round-63/quote-class/extract_text.py --raw .ufo/waves/round-61/sources/S432.html --out <tmp>/S432.txt`
  and `cmp` against the committed `.ufo/waves/round-63/quote-class/S432.txt` printed
  `REPRODUCES-BYTE-IDENTICAL` with sha `8b90d096…2a69`. Any reader can re-derive the
  exact text blob from the retained HTML.
- Counter-side derivation: `.ufo/waves/round-63/c63_calibration.py:60-67` inlines the
  same `classify` ("Round-50 class semantics, inlined so C1 is verifiable without the
  scripts/quote_class.py tool"), and lines 117-151 re-derive the ledger pins and the
  class from `git show` bytes at the measured revision, never gating on the lane tool
  (contract Separability). Its after receipt
  `.ufo/waves/round-63/controls/after-c1.txt` prints
  `quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 … met=true`,
  exit 0, at commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`.
- Knowledge entry `corpus/knowledge/response-header-expectations.md`: the held
  `[r62-correction 2026-10-27]` block (lines 218-220) records the disagreement —
  the §3.6 purpose sentence "contains the field-purpose proposition across inline
  markup, but that rendered sentence is not a raw substring of the retained HTML" and
  held the quote unresolved under an over-strict raw-substring reading. The
  `[r63-correction 2026-10-27]` block (lines 222-250) quotes the frozen span in its
  located rendering, states it "is a substring of the committed flat-text rendering
  … and not of the retained HTML, so its derived class is `collapsed-only` — never
  described as a raw substring", cites both blob sha256s and the recipe, and grounds
  the admission explicitly "under the round-50 quote-class rule (`corpus/QUALITY.md`)".
  It also keeps the purpose span separate from the `nosniff` value rule per the
  round-62 substantive-support criterion, and notes the live 2026-10-27 re-GET of
  fetch.spec.whatwg.org returned a body byte-identical to the round-61 retention.
- Disagreement lineage: `corpus/lessons/round-61-verifier-spotcheck.md:33` records the
  non-author `Disagree` on S432 ("generic lead-in, not substantive evidence");
  `corpus/QUALITY.md:1412` carries the resulting round-62 criterion (quoted span must
  substantively support the proposition attributed to its source); the round-63
  lesson gate records the outside verdict and its own author-side assessment
  (`corpus/lessons/round-63.md:61-65`).

## Same class semantics — confirmed

The round-63 admission uses the identical three-class decision procedure as round 50:

- `raw-substring` ⇔ span ∈ retained HTML (raw checked first);
- `collapsed-only` ⇔ span ∉ retained HTML and span ∈ flat-text rendering;
- `absent` ⇔ span ∈ neither;
- classes are mutually exclusive facts about the same two blobs; a swapped label
  fails the check; the class is always derived, never asserted.

Both rounds record the class together with sha256 pins of both blobs, and both
counter families re-derive the class from the pinned blobs rather than trusting the
ledger (round-50 R2 in `c50_quote_class.py`; round-63 `quote_correction` component in
`c63_calibration.py:117-151`).

## Named differences (provenance/posture, not class-semantics drift)

1. Recipe pinning. Round 50's criterion says "survives only whitespace collapse"
   while its text blobs (`.ufo/waves/round-49/sources/S27x.txt`) were retained
   artifacts whose extraction recipe was not itself committed. Round 63 pins the
   rendering recipe (`extract_text.py`, textContent semantics: charrefs decoded once,
   script/style/noscript skipped, block elements → newline, whitespace runs collapsed
   to one ASCII space) and commits the derived `S432.txt`, verified byte-reproducible
   from the retained HTML. This tightens provenance of the "flat text" side of the
   test; the membership predicate and its outcomes are unchanged (S273 re-derives
   under the same recipe family; S432 is collapsed-only under both phrasings).
2. Ledger schema cosmetics. `kake-r50-quote-classes-v1` used bare `textPath`/
   `rawPath` filenames and no recipe field; `kake-r63-quote-classes-v1` uses
   repo-relative paths and adds `recipe`, `locatedRawLines`, and `note`. No class
   meaning changed.
3. Adjudication posture. S273's collapsed-only label at round 50 was a fresh
   derivation inside a 3-id count with a swapped-label blur control. S432's
   collapsed-only label at round 63 is the resolution of a held round-61/62
   disagreement: the round-62 held block read QUALITY as requiring raw-substring
   evidence, and round 63 corrects that reading by applying the round-50 rule that
   collapsed-only is an admitted, derived class — grounded explicitly at
   `corpus/QUALITY.md:1100-1108` — while satisfying the round-62
   substantive-support criterion (purpose statement, kept separate from the
   `nosniff` value grammar).
4. Separability. The round-63 counter inlines the round-50 semantics and never gates
   on `scripts/quote_class.py`; the tool is C2 evidence only. Round 50 had no such
   separation requirement. This does not change the class semantics either seat
   applies.

## Confidence and remaining unknowns

- Confidence: high. Every class label and sha pin cited above was re-derived
  mechanically from committed bytes in this seat; the tool and the frozen counter
  independently produce `collapsed-only` for the S432 span; the round-50 S273/S274/
  S286 labels all re-derive and agree with the round-50 ledger.
- Remaining unknown: none blocking for this seat's question. (Noted, not a defect:
  the round-50 `.txt` blobs' own extraction history predates the pinned-recipe
  practice; nothing in round 63 depends on re-deriving round-50 text blobs.)

No installs this seat. No writes outside this Report.
