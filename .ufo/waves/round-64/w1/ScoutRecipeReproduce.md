# Seat ScoutRecipeReproduce — round-64 independent recipe reproduction & located-range derivation

**Verdict: C1's recipe + located-line derivation reproduces exactly. Output sha256 = `8b90d096…2a69`; byte-identical to the committed `S432.txt`; the minimal raw-line range is uniquely `6150-6154`.** No defect found in the C1 derivation chain. The round-63 routed defect (self-authored / circular flat text) is genuinely closed on this path: a flat text that is not the recipe's output over the retained raw blob cannot reproduce this sha.

Scope of attack: the C1 `recipe` and `located` components only (the `pins`/`prose`/`unresolved` components were read but are other seats' axes). Nothing in the lane repo was edited; all computation ran in scratch and was deleted.

- Lane repo (read-only): `/home/vgpnk/Projects/shokunin/kake-shokunin`
- Base revision (round-63 tip): `1a48131577ba82c967650561be34e8dba909432a`
- Measured T0: `4c8295fa5e3b628f1fdf3840299ae415c01849fb`
- Scratch tree (created, used, deleted): `/fast/scratch/hyaku/kake-r64/ScoutRecipeReproduce/`
- Report path: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/w1/ScoutRecipeReproduce.md`

---

## 1. What I attacked

The C1 counter's two re-derivation components, per its own docstring in
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py`
(sha256 `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf` — matches the contract's frozen pin):

- **`recipe`** — "re-executes the committed `extract_text.py` over the retained raw blob inside this counter … and requires its output to equal the pinned flat text sha and the committed `S432.txt` blob byte-for-byte. Kills the round-63 circular text blob."
- **`located`** — "re-derives the minimal raw-line range whose committed-recipe rendering contains the frozen span and requires it to equal the ledger's `locatedRawLines` and the pinned constant."

The round-63 routed defect this lane is meant to confirm closed: the round-63 counter could be greened by a **digest-self-consistent fabrication** (a circular text blob authored by the claimant rather than extracted from the raw source). If my reproduction of the flat text — done *outside* the counter, from the committed recipe and the committed raw blob only — yields exactly the pinned sha and the committed `S432.txt` bytes, then the committed flat text is provably the recipe's output over the retained raw, and no self-authored text can stand in for it.

---

## 2. Blobs materialized at T0 (independent `git show`, lane untouched)

```
$ cd /fast/scratch/hyaku/kake-r64/ScoutRecipeReproduce
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-63/quote-class/extract_text.py > extract_text.py
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-61/sources/S432.html  > S432.html
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-63/quote-class/S432.txt     > S432.txt
$ sha256sum extract_text.py S432.html S432.txt
6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405  extract_text.py
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  S432.html
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  S432.txt
```

All three shas equal the contract's frozen pins:

| Blob | Contract pin | Observed at T0 | Match |
|---|---|---|---|
| raw `S432.html` | `63b0a018…911b` | `63b0a018…911b` | yes |
| flat text `S432.txt` | `8b90d096…2a69` | `8b90d096…2a69` | yes |
| recipe `extract_text.py` | `6b0a88cd…2405` | `6b0a88cd…2405` | yes |
| ledger `quote-classes.json` | `5f48e26b…0c42d` | `5f48e26b…0c42d` | yes |

The four pinned blobs are **byte-identical at BASE `1a481315` and at T0 `4c8295fa`** (verified per-blob; see §7 output), so the derivation is not sensitive to the round-64 delta.

---

## 3. Task (a) — recipe output sha256 equals `8b90d096…2a69`

```
$ python3 --version
Python 3.14.8
$ python3 -B extract_text.py --selftest; echo "selftest_exit=$?"
selftest 1/1
selftest_exit=0
$ python3 -B extract_text.py --raw S432.html --out out.txt; echo "extract_exit=$?"
extracted 1854393 bytes -> 286933 chars
extract_exit=0
$ sha256sum out.txt
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  out.txt
```

**(a) CONFIRMED.** The recipe, run by me over the retained raw blob at T0, produces output whose sha256 is exactly the pinned `8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69`. The recipe's own `--selftest` passes 1/1.

Determinism re-check (same input, second independent run):

```
$ python3 -B extract_text.py --raw S432.html --out out2.txt >/dev/null && cmp out.txt out2.txt && echo "DETERMINISTIC=yes"
DETERMINISTIC=yes
```

---

## 4. Task (b) — output byte-identical to the committed `S432.txt` at T0

```
$ cmp out.txt S432.txt && echo "BYTE_IDENTICAL=yes" || echo "BYTE_IDENTICAL=NO"
BYTE_IDENTICAL=yes
$ wc -c out.txt S432.txt
  290480 out.txt
  290480 S432.txt
```

**(b) CONFIRMED.** `cmp` reports no difference; both are 290 480 bytes. The committed flat text is bit-for-bit the recipe's rendering of the retained raw blob — i.e. it is *not* a self-authored blob. This is the direct evidentiary answer to the round-63 routed defect: a digest-self-consistent fabrication (a text blob the claimant wrote and then committed alongside its own hash) cannot reproduce this sha from this raw, because the sha is now pinned to a *transformation of a different pinned blob*, re-executed inside the counter from the revision blob rather than from the worktree.

---

## 5. Task (c) — independent located-range derivation: is it `6150-6154`?

### 5.1 What "located" means, read from the source

`c64_calibration.py` defines the span it searches for and the search space (read from the file, not guessed):

```python
FROZEN_QUOTE = (
    "The `X-Content-Type-Options` response header can be used to require "
    "checking of a response\u2019s `Content-Type` header against the "
    "destination of a request."
)
EXPECTED_LOCATED = "6150-6154"
LOCATED_WINDOW = (6100, 6200)
LOCATED_SPAN_MAX = 15
```

`derive_located()` renders each candidate raw-line window with the committed recipe and returns the **minimal** `(b - a)` window whose rendering *contains* `FROZEN_QUOTE`; `raw_lines` is `raw.decode(...).split("\n")` (1-based line numbering, so window `a..b` is `raw_lines[a-1:b]`).

### 5.2 My independent implementation

I did **not** call the counter's `derive_located`. I wrote three independent scripts in scratch and cross-checked them, because a naive re-implementation can hide a shorter window:

- `derive_located2.py` — per-line renders used as a cheap *candidate detector*, then every candidate confirmed with the real joined-window render. Scans the **whole file** (not just 6100–6200) and reports the global minimum.
- `derive_located3.py` — **exhaustive authoritative** scan: for every start `a` in `1..18915` and every end `b` with `b-a ≤ 6`, render the joined window with the committed recipe and test the quote. No cheap pre-filter at all, so no heuristic can hide a window. (My first filter attempt, a whitespace-collapse substring test over raw source, was **wrong** — the quote is broken across HTML tags, so it never matched; the corrected scripts do the real render.)
- A final whole-file pass with `b-a ≤ 15` (the counter's own `LOCATED_SPAN_MAX`).

### 5.3 Results

```
$ python3 -B derive_located2.py
windows containing the frozen quote: 12
all (span,a,b): [(15, 6139, 6154), (14, 6140, 6154), (13, 6141, 6154), (12, 6142, 6154),
                  (11, 6143, 6154), (10, 6144, 6154), (9, 6145, 6154), (8, 6146, 6154),
                  (7, 6147, 6154), (6, 6148, 6154), (5, 6149, 6154), (4, 6150, 6154)]
minimal span (b-a) = 4 candidates: [(4, 6150, 6154)]
INDEPENDENT MINIMAL RANGE = 6150-6154
render: The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.
  drop-first(6151-6154): contains_quote=False
  drop-last(6150-6153): contains_quote=False
```

```
$ python3 -B derive_located3.py
raw lines (split on \n): 18915
span 4: 1 window(s) -> [(6150, 6154)]
span 5: 2 window(s) -> [(6149, 6154), (6150, 6155)]
span 6: 3 window(s) -> [(6148, 6154), (6149, 6155), (6150, 6156)]
EXHAUSTIVE MINIMAL SPAN = 4 windows: [(6150, 6154)]
EXHAUSTIVE MINIMAL RANGE = 6150-6154
counter's EXPECTED_LOCATED = 6150-6154 -> True
inside counter LOCATED_WINDOW (6100,6200): True
counter LOCATED_SPAN_MAX=15 covers span 4 : True
```

Whole-file pass at `b-a ≤ 15` (the counter's own cap):

```
spans 1..15 over WHOLE file: {4: (1, [(6150, 6154)]), 5: (1, [(6149, 6154)]), 6: (1, [(6148, 6154)]),
  7: (1, [(6147, 6154)]), 8: (1, [(6146, 6154)]), 9: (1, [(6145, 6154)]), 10: (1, [(6144, 6154)]),
  11: (1, [(6143, 6154)]), 12: (1, [(6142, 6154)]), 13: (1, [(6141, 6154)]), 14: (1, [(6140, 6154)]),
  15: (1, [(6139, 6154)])}
```

**No window of span 1, 2 or 3 anywhere in the 18 915-line file contains the frozen span.** The minimal range is **uniquely `6150-6154`** — not merely minimal within the counter's 6100–6200 window, but globally minimal over the entire file, and the counter's `LOCATED_SPAN_MAX=15` and `LOCATED_WINDOW=(6100,6200)` are not truncating anything.

### 5.4 Minimality witnesses (both endpoints are load-bearing)

```
drop-first(6151-6154): contains_quote=False
drop-last(6150-6153):  contains_quote=False
```

The five raw lines at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html` (T0), lines 6150–6154:

```
6150:    <p>The
6151: `<dfn class="dfn-paneled" data-dfn-type="http-header" data-export id="http-x-content-type-options"><code>X-Con…
6152: response <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑤">header</a> can be used t…
6153: `<code>Content-Type</code>` <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑥">heade…
6154: <a data-link-type="dfn" href="#concept-request" id="ref-for-concept-request①⓪⑦">request</a>.
```

The frozen span genuinely straddles inline markup across five physical lines, which is exactly why it is `collapsed-only` and not a raw substring (§6).

### 5.5 Ledger cross-check

```
ledger S432 row: {"id": "S432", "quote": "The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.", "matchClass": "collapsed-only", "textPath": ".ufo/waves/round-63/quote-class/S432.txt", "rawPath": ".ufo/waves/round-61/sources/S432.html", "textSha256": "8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69", "rawSha256": "63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b", "locatedRawLines": "6150-6154", "note": "Retained-HTML raw lines 6150-6154 carry the field-purpose sentence across inline markup; the span is a substring of the committed flat-text rendering only, which is the collapsed-only class of corpus/QUALITY.md round 50."}
ledger matchClass==collapsed-only: True
ledger locatedRawLines==6150-6154: True
```

The ledger's `locatedRawLines` is `6150-6154` — matching my independent derivation exactly, and matching the ledger's own `rawSha256`/`textSha256` (which are the two blobs I re-derived from).

---

## 6. Class re-derivation (round-50 semantics, re-derived inline)

The counter's `classify()` is `raw-substring` if the quote is in the raw, else `collapsed-only` if it is in the flat text, else `absent`. Re-derived independently:

```
quote in raw: False | quote in flat text: True | class: collapsed-only
recipe output == committed S432.txt: True | sha256 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
```

Matches the ledger's `matchClass: collapsed-only` and the counter's reported `derived=collapsed-only`.

---

## 7. Counter cross-read at both revisions (read-only invocation)

The counter is the frozen instrument; I ran it **read-only** against the lane repo to confirm its own `located` component agrees with my independent value (this run only reads via `git show`; the counter's own temp materialization goes to a scratch `TMPDIR` I set explicitly).

At T0:

```
$ TMPDIR=/fast/scratch/hyaku/kake-r64/ScoutRecipeReproduce/tmp python3 -B c64_calibration.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb
revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
counter_exit=0
```

At BASE:

```
$ python3 -B c64_calibration.py --root … --revision 1a48131577ba82c967650561be34e8dba909432a
revision=1a48131577ba82c967650561be34e8dba909432a disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
base_exit=1
```

Note: at BASE the `recipe` and `located` components **already** pass (`recipe_rederive=1`, `located=6150-6154`) — the base's `met=false` comes from the round-64 `lesson_gate` component (the round-64 lesson's Gate block does not exist at BASE) and `unresolved=1`. So the round-64 delta for C1 is the prose/gate binding, **not** the recipe or the located derivation. That is the correct shape for the contract's routing, and it confirms my independent derivation is measuring the same quantity the counter measures.

---

## 8. Round-64 live re-fetch corroboration (read-only)

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/sources/receipts.json` (untracked, orchestrator-produced) records a fresh public GET of `https://fetch.spec.whatwg.org/` with `sha256 63b0a018…911b`, `retainedRound61Sha256 63b0a018…911b`, `byteIdenticalToRetained: true`. I verified the on-disk blob independently:

```
$ sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/sources/S432.live.html
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  …
```

The live re-fetch is byte-identical to the retained round-61 raw blob I re-derived from, so the derivation is stable against upstream drift as of 2026-10-30.

---

## 9. Spot-check verdict-span binding (the C1 `prose` axis, cross-read)

The counter binds the round-61 spot-check's actual verdict span, block-level, into the round-64 lesson's Gate. Verified from the revision blobs:

- `corpus/lessons/round-61-verifier-spotcheck.md` (T0) line 33 — the S432 row's Reason cell contains the span verbatim:
  `| S432 / Fetch | Admit | https://fetch.spec.whatwg.org/, §3.6; retained body .ufo/waves/round-61/sources/S432.html | Disagree | "Web developers and conformance checkers must use the following" is only a generic lead-in, not substantive evidence for a response-header expectation. …`
- `corpus/lessons/round-64.md` (T0) line 95 — the Gate block binds it: `"S432 / Fetch" — its reason: "is only a generic lead-in, not substantive evidence for a response-header expectation")`.

The span is the *actual* verdict reason text, not a paraphrase — matching the counter's `SPOT_VERDICT_SPAN` constant exactly (I asserted `SPOT_VERDICT_SPAN in spot` → `True`). This is the round-63 "unquoted spot verdict" defect, closed.

---

## 10. Findings, and what remains open

**Findings (all negative — no defect):**

1. The committed flat text is provably the committed recipe's output over the committed raw blob, byte-for-byte. The round-63 circular-text / digest-self-consistent-fabrication hole is closed on this path.
2. The located range is **uniquely `6150-6154`**, globally minimal over the whole 18 915-line raw file, with both endpoints load-bearing and both drop-witnesses negative. The counter's window (`6100–6200`) and span cap (`15`) do not truncate the answer.
3. The ledger's `locatedRawLines`, `matchClass`, `rawSha256` and `textSha256` all agree with the independently re-derived values.
4. The four pinned blobs are identical at BASE and T0, so this derivation is not an artifact of the round-64 delta.
5. The round-61 spot-check verdict span is quoted verbatim in the round-64 lesson's Gate block.

**Explicitly out of my scope (other seats' axes), not verified here:** the `prose` component's other sub-conditions (`quote_correction`, `criterion`, `source_row`) beyond the verdict-span binding in §9; the C2 stub-proofing of `c64_quote_tool.py`; the C3 sidecar re-pin and `freshness-sweep.mjs` outcome; the committed control fixtures and their `met=false` receipts.

**Residual unknown (bounded, non-blocking):** my derivation validates the *derivation*, not the *claim* that `X-Content-Type-Options`'s "field purpose" is a response-header expectation. The frozen span's substance — that the Fetch Standard says the `X-Content-Type-Options` response header "can be used to require checking of a response's `Content-Type` header against the destination of a request" — is read here as a **generic lead-in**, exactly as the round-61 spot-check recorded; the round-64 lesson Gate must say so in its own words, and it does (line 95). If the Gate had instead asserted the span is substantive evidence of a response-header expectation, the located range would still be `6150-6154` and the recipe would still reproduce — the derivation cannot detect that prose failure. That is the boundary between this lane's axis and the `prose` axis, and it is why the counter binds the verdict span block-level rather than relying on the derivation.

---

## 11. Commands, files, and hygiene

**Absolute paths of the artifacts I read (lane repo, read-only):**

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py` (frozen sha256 `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf` — re-verified, matches contract)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/extract_text.py` (T0 sha256 `6b0a88cd…2405`)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html` (T0 sha256 `63b0a018…911b`)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/S432.txt` (T0 sha256 `8b90d096…2a69`)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/quote-classes.json` (T0 sha256 `5f48e26b…0c42d`)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-61-verifier-spotcheck.md` (line 33)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-64.md` (line 95)

**Scratch (created under the mandated path, deleted before yield):**

- `/fast/scratch/hyaku/kake-r64/ScoutRecipeReproduce/` — `extract_text.py`, `S432.html`, `S432.txt`, `out.txt`, `out2.txt`, `c64_calibration.py`, `derive_located.py`, `derive_located2.py`, `derive_located3.py`, `work/`, `tmp/`
- Deleted with `rm -rf` after all evidence above was captured into this report.

**Hygiene assertions:**

- No mutating `git`/`jj` command was run anywhere. Only `git show`, `git rev-parse`, `git status` (all read-only) against the lane repo; no fixture repo was created, so the `rev-parse --show-toplevel` precondition never arose.
- No fixture/clones/archives created; no `TMPDIR` reliance — the counter's temp materialization was pointed at my own scratch `TMPDIR` explicitly.
- The lane working tree was **not** modified by me. `git status --porcelain` in the lane shows only orchestrator-produced untracked paths (`.ufo/waves/round-64/sources/`, `.ufo/waves/round-64/w1*`), which pre-existed my seat; my only write inside the lane is this report file at the path the seat spec names.
- Nothing was written to `~/.local/bin` or any PATH directory; no fleet-root tracked file (`LOG.md`, `SCORECARD.md`, `MANIFEST.json`) was touched.
- Nothing was committed or pushed.

**Tools:** no installs. `python3` 3.14.8 (pre-existing system interpreter) and `git` (pre-existing) were sufficient; `pacman` was not invoked (host-wide pause respected).

---

## 12. One-line verdict

**C1's `recipe` and `located` components are independently reproducible and correct: the committed recipe over the committed raw blob at T0 yields sha256 `8b90d096…2a69` byte-identical to the committed `S432.txt`, and the minimal raw-line range whose rendering contains the frozen span is uniquely `6150-6154` (globally minimal over the whole file; both endpoint drop-witnesses negative) — the routed round-63 circular-fabrication defect is closed on this path; no C1 derivation defect found.**
