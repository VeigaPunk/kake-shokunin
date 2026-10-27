# RevengerC62Defect — c62 defect class vs the c63 counter

Seat: leaf, round 63 kake, claim C1. Read-only against the fleet root,
`kake-shokunin` and sibling repos; the only file written is this report.
No tool installs (python3 + git only). No pacman, no git/jj mutation outside
the throwaway fixture repos under `/fast/scratch/hyaku/kake-r63/RevengerC62Defect/`
(each verified with `git -C "$D" rev-parse --show-toplevel` == `$D` before its
first commit, each created with `git -C "$D" init -q`, all deleted after the
runs; see §9).

## 0. Frozen artifacts re-verified before the attack

```
$ sha256sum .ufo/waves/round-63/c63_calibration.py scripts/quote_class.py \
    .ufo/waves/round-63/c63_quote_tool.py .ufo/waves/round-62/c62_calibration.py
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  .ufo/waves/round-62/c62_calibration.py
```

Frozen ledger and its two blobs (`sha256sum`, at the measured revision — the
committed tree is identical):

```
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .ufo/waves/round-63/quote-class/S432.txt
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html
```

Frozen span, check (inline, same expression as the counter):
`in_raw False in_text True text_count 1` for
``The `X-Content-Type-Options` response header … destination of a request.``

Measured and base receipts reproduced from the committed tree (read-only):

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0

$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

Both match `controls/after-c1.txt` and `controls/base-c1.txt` byte-for-byte on
the result line.

## 1. Reconstructed c62 contract (what the old counter actually tested)

`kake-shokunin/.ufo/waves/round-62/c62_calibration.py:33-41`:

| line | test | kind |
|---|---|---|
| 33-34 | `QUOTE in knowledge and "S432 §3.6" in knowledge and "Round-62 correction" in knowledge` | three literal substrings |
| 35 | `"substantive located quote" in quality and "round-61-verifier-spotcheck.md" in quality` | two literal substrings |
| 36-37 | `"## Gate"`, `"S432"`, `"Agree"`, `"Reject"` in `lessons/round-62.md` | four literal substrings |
| 38 | `"\| S432 \|" in sources` | one literal substring |
| 40 | `unresolved = disagreements if not resolved else 0` | metric voided whenever `resolved` |
| 41 | `met = unresolved == 0 and resolved` ≡ `met = resolved` | — |

So c62's `resolved` is a pure conjunction of 10 literal substrings over 5
blobs; the only blob-content check is non-emptiness of the spot-check
(line 28: `if not data["spot"] … return 2`), and the `disagreements` count is
computable but structurally unable to make the counter red.

## 2. Reconstructed c63 contract

`kake-shokunin/.ufo/waves/round-63/c63_calibration.py`:

| lines | component | binding |
|---|---|---|
| 121-125 | `correction` | `"[r63-correction"`, `FROZEN_QUOTE`, `LEDGER_REL` in the knowledge blob — literal substrings |
| 133-140 | `blobs_match` | ledger row's `rawSha256`/`textSha256` equal the digests of **whatever blobs sit at the two fixed paths**, and row `quote == FROZEN_QUOTE` — self-referential, no frozen digest of the blobs or the ledger |
| 141-143 | `class_match` | inline `classify(FROZEN_QUOTE, raw, text) == "collapsed-only" == row["matchClass"]` — genuine derivation, real check |
| 145 | `quote_correction` | `correction and blobs_match and class_match` |
| 148-150 | `criterion` | `"substantive"` + `"round-61-verifier-spotcheck"` + the three `PURPOSE_TERMS` anywhere in `QUALITY.md` — **literal substrings** |
| 153-160 | `lesson_gate` | `"## Gate"`, `"round-61-verifier-spotcheck"`, `"Disagree"`, `"collapsed-only"`, `"author-side"\|"self-assessment"` anywhere in `lessons/round-63.md` — **literal substrings** |
| 162 | `source_row` | `^\|\s*S432\s*\|` regex — **literal**, cells unread |
| 164-166 | `resolved`, `unresolved`, `met` | `met = bool(resolved)`; `unresolved = disagreements if not resolved else 0` — *the c62 line 40/41 structure is preserved verbatim* |
| 94-96 | spot guard | only `blobs["spot"] is None` (unreadable blob) is fatal; an **empty** blob passes |

Three of the four components (`criterion`, `lesson_gate`, `source_row`) are
literal-substring tests — the exact c62 defect, carried forward unchanged. The
fourth (`quote_correction`) is class-derived but provenance-blind: it asks only
that *some* bytes at two paths agree with *some* JSON at a third path that the
same author also writes.

## 3. Every way c62's `resolved` could be 1 without semantic evidence

Enumerated from c62 lines 33-41, then each instantiated:

- **V1 planted markers in all five files** (no source body, disagreement live) — the committed round-62 fixture path.
- **V2 disagreement erased / replaced, markers intact** — delete the `Disagree` row; `disagreements=0`; every component still literal.
- **V3 fabricated evidence triple** — author two blobs at the fixed paths and a ledger whose digests hash them; no historical blob consulted.
- **V4 real blobs, swapped class label** — evidence real, the recorded class lies.
- **V5 real blobs, swapped digest fields** — ledger hashes misassigned.
- **V6 real blobs, wrong quote recorded** — a different (real) span carried in the ledger.
- **V7 empty/erased spot blob** — the outside verdict deleted; c62's non-empty guard is the only defence.
- **V8 lesson faking the outside verdict** — the gate's words present, the verdict absent.
- **V9 stubbed criterion / source row** — one junk line in `QUALITY.md`, one `| S432 |` row with empty cells.

## 4. Variant matrix

Fixtures: scratch git repos with a throwaway identity
(`git -C "$D" -c user.name=fixture -c user.email=fixture@example.invalid commit`);
counter invoked from the lane root as
`python3 -B .ufo/waves/round-63/c63_calibration.py --root "$D" --revision "$REV"`.
`c62` denotes `python3 -B .ufo/waves/round-62/c62_calibration.py` with the same
arguments.

| # | variant | fixture rev | c62 | c63 | c63 result line (abridged) |
|---|---|---|---|---|---|
| A | V1 marker-only (r62 fixture corpus copied byte-exact) | `756a92bf75b80d1d4c35a3a241233418f44a8b12` | **met=true** exit 0 | met=false exit 1 | `qc=0 blobs=0 derived=unevaluable class=0 crit=0 lesson=0 row=1 unresolved=1` |
| B | V2 markers + `Disagree` row deleted (r62 spot is one line → 0 bytes) | `1e67bdf160c405232e5df1ad1031bbcd7a4511f4` | **exit 2** `missing verifier spot-check` | met=false exit 1 | `disagreements=0 … unresolved=0 met=false` |
| B2 | V2 markers + `Disagree` row replaced by a fabricated `Agree` row (body kept) | `ca8bd365ce2cd085c6c3a0bf95bbc5b3b6c0bf46` | **met=true** exit 0 | met=false exit 1 | `disagreements=0 … unresolved=0 met=false` |
| C | V3 fabricated bundle: fake ledger + 3-line fake "raw" + 3-line fake "text" + junk markers + fabricated `Agree` verdict | `96a71a5bb79dee9bb541601a4aed83c12729b033` | met=false exit 1 | **met=true exit 0** | `disagreements=0 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true` |
| D | V4 real blobs + ledger `matchClass:"raw-substring"` | `98c53c3ab57a60ee1458fe6be54fd65a10c755db` | — | **killed** exit 1 | `blobs_match=1 derived=collapsed-only class_match=0 met=false` |
| E | V5 real blobs + `rawSha256`/`textSha256` swapped | `0cf3f968487df51db0e1f21653209236025973b5` | — | **killed** exit 1 | `blobs_match=0 … met=false` |
| F | V6 real blobs + ledger `quote` = the lead-in span | `c83f813bffb7669a80acd0be6de4e4b8326fd9eb` | — | **killed** exit 1 | `blobs_match=0 … met=false` |
| G | V7 real evidence, spot blob emptied (0 bytes) | `1b9668e858b357f8045af53e5a1d8a1b882ee05c` | **exit 2** (see G2) | **met=true exit 0** | `disagreements=0 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true` |
| G2 | same tree, c62 | `0d8b81d36e3753c6f71b5ac915ad228e4889d2d9` | **exit 2** `could-not-evaluate: missing verifier spot-check` | — | — |
| H | V8 real evidence, spot rewritten to `Agree`, lesson fabricated to claim an outside `Disagree` | `4c16161e50cb1500655b1f8c3746944657bb096b` | — | **met=true exit 0** | `quote_correction=1 … lesson_gate=1 … met=true` |
| I | real evidence, ledger `note` tampered (its own sha ≠ frozen `5f48e26…`) | `2f419e1f369a5fd8ee3632022192533ab89e9d83` | — | **met=true exit 0** | `quote_correction=1 … met=true`; fixture ledger sha `610608e9b80a5d8fd1f7b63cf83f88d399c3fd1cc929a859c2e9c5946000f1d4` |
| J | real evidence, ledger `locatedRawLines` forged `"1-1"` | `2358575b54aac056c24fca0d1e9b6ca0f31e198b` | — | **met=true exit 0** | `quote_correction=1 … met=true` |
| K | V3 bundle with the *real* corpus marker files (fake blobs + fake ledger only) | `633e68532051df85b89c04f1d6ec13082fd4f415` | — | **met=true exit 0** | `quote_correction=1 … met=true` |
| L | V3 bundle, ledger `classes: []` | `422cae8027b2457b2b511f760a42df24ce38ad9b` | — | **killed** exit 1 | `blobs_match=0 derived=unevaluable met=false` |
| M | V3 bundle, text blob lacks the span (ledger self-consistent) | `8b99ab7fe1b3f521939db2d56a9e26c025b9111a` | — | **killed** exit 1 | `blobs_match=1 derived=absent class_match=0 met=false` |
| N | V3 bundle, knowledge without the frozen span | `344ab22fb2c9e4d741c6d0d36af6bcd3512752e3` | — | **killed** exit 1 | `quote_correction=0 … class_match=1 met=false` |
| O | V3 bundle, ledger label swapped to `raw-substring` | `7fc0e8bef81cdb95cfd30a3ff55b1cbeb0e836fa` | — | **killed** exit 1 | `blobs_match=1 derived=collapsed-only class_match=0 met=false` |
| P | V2 real evidence + a **fresh, unresolved** `S432 … Disagree` line appended | `998d34a49dbd64afef9dec4542fe1bc9abcd3e25` | — | **met=true exit 0** | `disagreements=2 … unresolved=0 met=true` |
| Q | V3 bundle, ledger `textPath`/`rawPath`/`locatedRawLines` pointing nowhere | `1e7ea80e48c995402b8205210fa0d5e48c4a87a9` | — | **met=true exit 0** | `quote_correction=1 … met=true` |
| S | real blobs + ledger, but `QUALITY.md`/`SOURCES.md`/lesson/knowledge reduced to one marker line each | `2652ec7c71834d0fae5308e49907e852bf6394a5` | — | **met=true exit 0** | `quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true` |

## 5. The decisive miss: self-consistent fabrication (variant C)

Exact bundle, 8 files / 1379 bytes, zero historical bytes consulted:

```
353 corpus/knowledge/response-header-expectations.md   <- FROZEN_QUOTE + "[r63-correction" + ledger path
107 corpus/lessons/round-61-verifier-spotcheck.md      <- "| S432 / Fetch | … | Agree | fabricated agreement |"
 72 corpus/lessons/round-63.md                         <- "## Gate round-61-verifier-spotcheck Disagree collapsed-only author-side"
 88 corpus/QUALITY.md                                  <- "substantive round-61-verifier-spotcheck X-Content-Type-Options Content-Type destination"
 16 corpus/SOURCES.md                                  <- "| S432 | stub |"
 44 .ufo/waves/round-61/sources/S432.html              <- "<html><body><p>fabricated</p></body></html>"
544 .ufo/waves/round-63/quote-class/quote-classes.json <- hashes of the two files above, matchClass collapsed-only, locatedRawLines "1-1"
155 .ufo/waves/round-63/quote-class/S432.txt           <- the frozen span, one line
```

The fabricated ledger, verbatim:

```json
{"schema":"forged","classes":[{"id":"S432","quote":"The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.","matchClass":"collapsed-only","textPath":".ufo/waves/round-63/quote-class/S432.txt","rawPath":".ufo/waves/round-61/sources/S432.html","textSha256":"07a430b27e0c1a0ae0182b7a8bedee8634e40e9b3b22c74e85d48246118e9bf2","rawSha256":"63df0c7fad23721995560c2c57e4a6b7ab70e1e5ddd0deaa6386e8da27019deb","locatedRawLines":"1-1","note":"forged"}]}
```

Observed at `96a71a5bb79dee9bb541601a4aed83c12729b033`:

```
revision=96a71a5bb79dee9bb541601a4aed83c12729b033 disagreements=0 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

Nothing in this tree is the round-61 retained body (44-byte placeholder), the
round-61 non-author verdict (the spot file asserts agreement), or any real
correction. The counter is green. The single string that makes
`blobs_match=1` possible is a digest the fixture author computed over bytes the
fixture author wrote; `c63_calibration.py:133-140` never compares either blob —
or the ledger itself — against a constant, so provenance is not in the
predicate at all.

The same green is reached while keeping the *real* corpus marker files (K) and
while pointing the ledger's own path fields at nonexistent files (Q), which
shows the ledger's `textPath`/`rawPath`/`locatedRawLines` are decorative: the
counter hardcodes `QUOTE_REL`/`TEXT_REL` (`c63_calibration.py:41-43`) and never
reads a location.

Predicate-literal reading: the contract's sentence names one marker-only
fixture (the round-62 corpus), and c63 does print `met=false` on it (A) — that
control passes. Semantic reading: a tree containing no committed evidence is
still green. The repair moved the cost of the false green from "plant 5 marker
files" to "plant 5 marker files + 2 blobs + 1 JSON"; it did not remove the
class. Whether that trips the C1 kill rule ("any wave attack reproduces a
marker-only green") is the reviewer's ruling; the reproduction above is the
evidence for it.

## 6. Secondary misses

**V7 empty spot is accepted, and c63 is weaker than c62 here (G vs G2).**
c62 line 28 treated an empty spot blob as `could-not-evaluate` (exit 2). c63
line 94 only rejects an *unreadable* blob; `git show` returning 0 bytes passes.
Taxonomy: on an otherwise-real tree, deleting the outside verdict wholesale
prints `met=true`. The lesson still says the round-61 non-author `Disagree` is
recorded (`lesson_gate` is markers), so the counter certifies a verdict that
does not exist in the tree.

**V8 lesson faking the outside verdict (H).** `lesson_gate`
(`c63_calibration.py:153-160`) is five literal substrings. With the spot file
rewritten to `Agree`, a fabricated `round-63.md` containing
`## Gate … round-61-verifier-spotcheck … Disagree … collapsed-only … author-side`
prints `lesson_gate=1`. The counter never cross-reads the spot blob to see what
the outside verdict actually says, nor requires the verdict line to exist.

**V2 disagreement is never measured (B, B2, P).** `met = bool(resolved)`
(line 166) and `unresolved = disagreements if not resolved else 0` (line 165):
`disagreements` can only ever be reported as `unresolved=0` whenever the four
components are green. P appends a brand-new unresolved `S432 … Disagree` line
and gets `disagreements=2 … unresolved=0 met=true`. The printed `unresolved`
is structurally incapable of being non-zero in a green run — the c62 line 40/41
defect is inherited verbatim, so "the round-61 S432 disagreement is resolved"
is not a measured proposition in C1.

**Ledger self-digest not enforced (I).** The contract names the ledger as
`sha256 5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d`; the
counter never hashes the ledger. A tampered ledger (`610608e9…`) on the real
tree is green. (Reading: the contract ties `5f48e26…` to the blob digests being
"re-derived", so this is a degree-of-binding divergence rather than a breached
sentence; the counter nonetheless blesses a tree whose ledger is not the frozen
one.)

**Criterion and source row are c62 literals (C, K, S).** `QUALITY.md` of one
junk line `substantive round-61-verifier-spotcheck X-Content-Type-Options Content-Type destination`
yields `criterion=1`; `| S432 | stub |` yields `source_row=1`. Neither the
proposition sentence nor the row's `status`/`recheck`/`used-by` cells are read.
S goes further: the knowledge "block" is satisfied by the span on one line plus
`[r63-correction]` and the ledger path — there is no block, no `> ` quote, no
prose requirement.

## 7. What c63 does kill (credit where due)

- **A** marker-only, exactly the round-62 committed fixture: red. The routed
  defect's own reproduction no longer greens.
- **B2** markers with the disagreement replaced by a fabricated `Agree`: red.
- **D / O** real blobs with a swapped class label: red (`class_match=0`) — the
  inline derivation is genuinely load-bearing.
- **E** swapped digest fields: red (`blobs_match=0`).
- **F** a different (real) span substituted for the frozen one: red.
- **L** ledger without the `S432` row: red.
- **M** self-consistent ledger whose text blob lacks the span (`derived=absent`):
  red — the class is derived, not trusted.
- **N** knowledge without the frozen span: red.

The class-derivation core (`classify`, lines 46-58, and
`class_match`, lines 141-143) behaves as documented in every probe.

## 8. Divergences from the claim as written

1. Counter docstring lines 3-8 claim "every `resolved` component" is bound to
   semantic evidence; three of four (`criterion`, `lesson_gate`, `source_row`,
   lines 148-162) are literal-substring tests identical in kind to c62 lines
   33-38. Only `quote_correction` is class-derived, and its digest check is
   self-referential.
2. `met = bool(resolved)` (line 166) discards `disagreements`; the printed
   `unresolved` (line 165) is always 0 in a green run. The claim's phrase
   "the round-61 S432 disagreement is resolved" has no representation in the
   predicate — no post-resolution `Agree`, no cross-check of the spot verdict,
   no requirement that the disagreement line exist.
3. The spot guard regressed from c62's non-empty check (c62 line 28) to c63's
   readable-blob check (c63 line 94).
4. The contract's ledger digest (`5f48e26…`) is not enforced by the counter.
5. The ledger's own location fields (`locatedRawLines: "6150-6154"`) are never
   verified; J forges them to `1-1` and stays green, so the claim's "located
   proposition" is asserted by the ledger, not checked by the counter.

## 9. Method, limits, cleanup

- Every variant was built as its own scratch git repo under
  `/fast/scratch/hyaku/kake-r63/RevengerC62Defect/`, `git init -q`, toplevel
  asserted equal to the fixture path (`TOP_OK` logged for the last fixture; the
  same assertion ran for all and `mk()` aborts on mismatch), throwaway identity
  via `-c user.name=fixture -c user.email=fixture@example.invalid`, one commit
  per variant, counters invoked against the committed revision only.
- Real blobs copied for the "real evidence" variants were the committed files
  at the measured revision (`S432.html` 63b0a018…, `S432.txt` 8b90d096…,
  ledger 5f48e26…); the six real-corpus variants (G, G2, H, I, J, P) were
  therefore byte-identical to the measured tree apart from the named mutation.
- No fleet-root, `.ufo/state`, `scripts/`, `templates/`, sibling-repo,
  `corpus/SOURCES.md`, `considerthese/` or `MANIFEST.json` write occurred; the
  frozen claim, counter, ledger, blobs and receipts were not edited. Only
  read-only `python3 -B … --root` invocations touched the lane.
- Scratch cleanup: all fixture repos, the two drivers (`drive.sh`,
  `drive2.sh`) and their outputs were deleted after the runs;
  `scratch_cleanup=clean`. Fixture revs above are recorded for the record only
  and no longer resolve anywhere.
- Limits: fixture-level evidence only; I did not judge whether the measured
  tree's correction is substantively correct (C1's `met=true` at
  `05b0d7f4` reproduces, and the real ledger/blobs are internally consistent).
  The finding is about what the counter can and cannot distinguish, not about
  whether round 63's evidence is genuine.
- Untested by design: git-object attacks (replace refs, grafts, symlinked
  blobs); they are outside the "c62 defect class" the seat enumerated.

**Bottom line.** c63 kills the round-62 fixture and every variant that swaps,
deletes or mislabels real evidence (D, E, F, L, M, N, O). It does not kill
fabricated-but-self-consistent evidence (C, K, Q, S), an emptied outside
verdict (G — a regression against c62's exit 2), a lesson that manufactures the
verdict (H), a tampered ledger (I), a forged location (J), or a live unresolved
disagreement reported as `unresolved=0` (P). Four of the nine enumerated c62
green paths (V3 fabricated evidence, V7 empty verdict, V8 faked verdict, V9
stubbed criterion/row) still green the c63 family, and V2's disagreement
dimension is not measured at all.
