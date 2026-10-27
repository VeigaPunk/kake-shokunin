# Seat ExecMarkerControl — round-63 w1

**Item:** rebuild the marker-only false-green fixture in my own scratch, run
BOTH `.ufo/waves/round-62/c62_calibration.py` and
`.ufo/waves/round-63/c63_calibration.py` against it. Expected: c62
`met=true` (defect), c63 `met=false`.

**Verdict: the assigned reproduction lands exactly as expected.** The old
counter greens on the marker-only fixture (the round-62 routed defect is
real and still reproducible); the repaired counter is red on the same
fixture. No contradiction found with the committed receipts.

I additionally ran a bounded attack sweep (17 scratch fixtures) against
both counters. **The kill rule is not tripped** — no *marker-only* tree
(no retained bodies at all) greens under c63, and the committed
`control-marker-fixture.txt` behaviour reproduces byte-for-byte. But two
robustness gaps in the repaired counter are real and are reported below as
risk, not as a claim falsification:
(c63's semantic binding is only *self-consistent*, never *upstream-anchored*;
and two of its four `resolved` components are still token checks).

**Scope note.** Read-only against the fleet repo
`/home/vgpnk/Projects/shokunin/kake-shokunin`. Nothing in the fleet repo,
`.ufo/state`, `scripts/`, `templates/`, the corpus or `SOURCES.md` was
modified; no git/jj mutation was performed against the fleet repo or any
sibling repo; no `pacman` transaction was run. All fixtures were built under
`/fast/scratch/hyaku/kake-r63/ExecMarkerControl/` in throwaway repos with a
throwaway identity local to each fixture
(`ExecMarkerControl Fixture <exec-marker-control@example.invalid>`), and the
whole scratch tree was deleted at the end of the seat. This report file is
the only path written outside scratch.

**Tools installed:** none (nothing to record).

---

## 1. Frozen-artifact digests (verified before attacking)

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ sha256sum .ufo/waves/round-63/c63_calibration.py .ufo/waves/round-62/c62_calibration.py \
    .ufo/waves/round-63/quote-class/quote-classes.json scripts/quote_class.py .ufo/waves/round-63/c63_quote_tool.py
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  .ufo/waves/round-62/c62_calibration.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  .ufo/waves/round-63/c63_quote_tool.py
```

All four contract-pinned digests match exactly (c63 counter
`bcd16f68…`, ledger `5f48e26b…`, tool `431e75e8…`, C2 counter `9fcbfad0…`).
The same digests re-verify at the measured commit `05b0d7f4` (see §3), so
the artifacts I attacked are the artifacts the contract froze.

## 2. Assigned reproduction — the marker-only fixture

### 2.1 Fixture construction

```
$ D=/fast/scratch/hyaku/kake-r63/ExecMarkerControl
$ rm -rf "$D"; mkdir -p "$D"; git -C "$D" init -q
$ git -C "$D" rev-parse --show-toplevel
/fast/scratch/hyaku/kake-r63/ExecMarkerControl          # == $D (asserted before the first commit)
$ cp -a .../.ufo/waves/round-62/controls/false-green-fixture/corpus "$D/"
$ git -C "$D" add corpus
$ git -C "$D" -c user.name="ExecMarkerControl Fixture" \
      -c user.email="exec-marker-control@example.invalid" commit -q -m "marker-only false-green fixture ..."
$ git -C "$D" rev-parse HEAD
53745c524ec746c5475efef6eeff905c24abd862
```

The corpus copy is byte-exact — the five sha256s equal the ones recorded in
the round-62 defect receipt
`.ufo/waves/round-62/controls/counter-false-green-l1.txt` and equal the
blobs at the measured commit:

```
0a9a034861b19ba9f0c2b49adb9e9c394b406816a63dc458b1b8ee62668405c3  corpus/lessons/round-61-verifier-spotcheck.md
635089aadf398ea2b17799494c5a0e209af3f87a4459234e71892d29351ba6b6  corpus/knowledge/response-header-expectations.md
373b9d254dff8668f9ae273e3f24ec87ff9b52f2c862ebabd158d76ad64d0457  corpus/QUALITY.md
d7033c6dc40448844e9c652900fb54298de8af539c8e45819e29d377bb1a8923  corpus/lessons/round-62.md
a27f4338e565e5231b48adb49c24f759612f8827927cd80cf838462ff4dd8d2b  corpus/SOURCES.md
```

Fixture rev differs from the receipt's `7833be88…` only because the
re-commit used a different throwaway identity and timestamp; the tree
content is identical.

### 2.2 Old counter (round-62 family) — defect reproduced

```
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root "$D" --revision 53745c524ec746c5475efef6eeff905c24abd862
revision=53745c524ec746c5475efef6eeff905c24abd862 disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
exit=0
```

`met=true`, exit 0, while the S432 `Disagree` line still stands
(`disagreements=1`) and no retained source body exists in the fixture.
This is the round-62 routed defect, reproduced independently.

### 2.3 Repaired counter — red on the same fixture

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root "$D" --revision 53745c524ec746c5475efef6eeff905c24abd862
revision=53745c524ec746c5475efef6eeff905c24abd862 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

`met=false`, exit 1. This matches the committed receipt
`.ufo/waves/round-63/controls/control-marker-fixture.txt` field-for-field
(`quote_correction=0 blobs_match=0 derived=unevaluable class_match=0
criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false`); only the
fixture rev differs.

**Assigned expectation: CONFIRMED.** The marker-only false-green is dead
for the exact committed fixture.

Note *why* c63 is red here: it fails on **three** components, not only the
blob binding — `quote_correction=0` (no `[r63-correction]` block, no frozen
quote, no ledger path in the fixture's knowledge file), `criterion=0` (the
fixture's `QUALITY.md` is the single line `substantive located quote
round-61-verifier-spotcheck.md` and names none of
`X-Content-Type-Options` / `Content-Type` / `destination`), and
`lesson_gate=0` (there is no `corpus/lessons/round-63.md` in the fixture;
its `lessons/round-62.md` is the single line `## Gate S432 Agree Reject`).

## 3. Baseline re-measurement at the measured commit and at base

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0

$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1

$ python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=1 source_row=1 met=false
exit=1
```

Identical to `controls/after-c1.txt` and `controls/base-c1.txt`. The frozen
predicate in the contract ("`met=true` at the measured revision, `met=false`
on the marker-only fixture, `met=false` at base") holds on all three legs as
measured by me.

C2 side, same tree, same commands:

```
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
exit=1
```

Matches `controls/after-c2.txt` / `controls/base-c2.txt`.

Independent confirmation that the committed class evidence is *substantively*
right (not just self-consistent): the round-63 flat-text rendering is
byte-exactly re-derivable from the retained HTML by the committed recipe
tool, and the retained HTML's digest equals the round-61 fetch receipt's:

```
$ python3 -B .ufo/waves/round-63/quote-class/extract_text.py \
      --raw "$D/derive/S432.html" --out "$D/derive/S432.rederived.txt"
extracted 1854393 bytes -> 286933 chars
$ sha256sum "$D/derive/S432.rederived.txt"
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69   # == committed S432.txt digest
$ cmp S432.txt S432.rederived.txt   ->  byte-identical
$ receipts.json (measured) S432 sha256 = 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b
$ sha256sum .ufo/waves/round-61/sources/S432.html  ->  63b0a018…bad911b   # == receipt
```

And the quote is genuinely split by inline markup in the raw body — it is
*not* a raw substring (raw lines 6150–6154, `<code>X-Content-Type-Options
</code>` … `<a …>header</a> can be used to require checking of a …`), while
the collapsed rendering contains it — hence `collapsed-only` is the correct
class, and the counter's inline `classify()` reaches it independently.

## 4. Attack sweep (17 scratch fixtures)

Every fixture is a fresh throwaway repo under
`/fast/scratch/hyaku/kake-r63/ExecMarkerControl/` (top-level asserted before
its first commit). Base tree for the "measured-tree" variants is
`git archive 05b0d7f4` (the measured commit), mutated in one named way.

| # | variant | mutation | c63 | c2 |
|---|---------|----------|-----|-----|
| — | **marker-only fixture** (assigned) | round-62 corpus, no bodies | `met=false` (1) | `present=0 met=false` (1) |
| A | `A-fabricated-body` | marker corpus + fabricated raw/text, no ledger | `met=false` (1) | `met=false` (1) |
| B | `B-no-quote-text` | marker corpus + fabricated raw/text (quote absent), no ledger | `met=false` (1) | `met=false` (1) |
| C | `C-measured-tree-fabricated-body` | measured tree; **raw+text replaced by fabricated pair, ledger rewritten to match** | **`met=true` (0)** | `met=true` (0) |
| D | `D-measured-tree-bad-ledger-hash` | measured tree; ledger `textSha256` tampered | `met=false` (1) | `met=true` (0) |
| E | `E-measured-tree-no-blobs` | measured tree; both retained blobs deleted | `met=false` (1) | `selftest=failed met=false` (1) |
| F | `F-measured-tree-raw-substring` | quote made contiguous in raw | `derived=raw-substring` → `met=false` (1) | `selftest=failed met=false` (1) |
| G | `G-measured-tree-wrong-matchclass` | ledger `matchClass` flipped to `raw-substring` | `class_match=0 met=false` (1) | `met=true` (0) |
| H | `H-marker-plus-fabricated-ledger` | marker corpus + fabricated pair + fabricated ledger | `met=false` (1) | `met=false` (1) |
| I | `I-genuine-raw-fabricated-text` | **genuine raw kept; text blob replaced by a hand-written one-liner containing the quote; ledger `textSha256` updated** | **`met=true` (0)** | `met=true` (0) |
| J | `J-measured-tree-no-tool` | `scripts/quote_class.py` deleted | `met=true` (0) | `present=0 met=false` (1) |
| K | `K-measured-tree-stub-lesson` | `corpus/lessons/round-63.md` → 4-line token stub | **`met=true` (0)** | `met=true` (0) |
| L | `L-measured-tree-stub-quality` | `corpus/QUALITY.md` → 2-line token stub | **`met=true` (0)** | `met=true` (0) |
| M | `M-measured-tree-no-correction-block` | `[r63-correction]` section deleted from knowledge | `met=false` (1) | `met=true` (0) |
| N | `N-measured-tree-marker-knowledge` | knowledge replaced by one marker line (no frozen quote) | `met=false` (1) | `met=true` (0) |
| O | `O-rev-no-blobs-worktree-has-blobs` | revision lacks blobs; worktree has fabricated ones | `met=false` (1) | **`met=true` (0)** |
| P | `P-worktree-raw-substring` | revision genuine; worktree text edited | `met=true` (0) | `met=true` (0) |
| P2 | `P2-worktree-raw-has-quote` | revision genuine; worktree raw edited to contain the quote | `met=true` (0) | **`selftest=failed met=false` (1)** |
| Q | `Q-rev-no-tool-fixtures` | revision lacks `scripts/fixtures/quote-class/*` | `met=true` (0) | `selftest=failed met=false` (1) |
| R | `R-stub-tool` | `scripts/quote_class.py` → 10-line stub printing a hardcoded green selftest | `met=true` (0) | **`met=true` (0)** |
| S | `S-marker-degraded-corpus` | corpus reduced to token stubs + fabricated pair + matching ledger | **`met=true` (0)** | `met=true` (0) |
| T | `T-measured-tree-wrong-prose-digests` | knowledge prose digests replaced with `000…`/`111…` | **`met=true` (0)** | `met=true` (0) |
| U | `U-many-disagreements` | 4 `Disagree` lines in the spot-check | **`met=true` (0)** | `met=true` (0) |
| V | `V-junk-markers-no-blobs` | junk markers, no bodies (rebuild of the junk control) | `met=false` (1) | — |

Key lines (verbatim counter output, exit codes captured by the wrapper):

```
C-measured-tree-fabricated-body  rev=751aeb69ea04d86e80073f5ea39d307c8e298de3
  c63 exit=0  revision=751aeb6… disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
I-genuine-raw-fabricated-text    rev=be677395eb3e93573c1e779a3ce453be77cf98bd
  c63 exit=0  revision=be67739… disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
S-marker-degraded-corpus          rev=d47e462023177a324b4c7862c79207237caadd71
  c63 exit=0  revision=d47e462… disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
T-measured-tree-wrong-prose-digests rev=3eae8ae179dda75808f6b5d3b36722bd883b84f7
  c63 exit=0  revision=3eae8ae… quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 … met=true
U-many-disagreements              rev=f4379ef72e9d80cbd1082d0c57d46e54b277c3e8
  c63 exit=0  revision=f4379ef… disagreements=4 … unresolved=0 met=true
```

**What is red (good):** A, B, D, E, F, G, H, M, N, V — i.e. a marker-only
tree, a junk-marker tree, a tampered ledger digest, a missing blob, a
wrongly-classed span, a marker corpus even with a fabricated ledger, and a
missing `[r63-correction]` block are all rejected. This is the round-62
defect class genuinely dead.

**What is green (risk):** C, I, K, L, S, T, U, R. Detailed below.

---

## 5. Findings (reported, not adjudicated — the L1 owns the call)

### 5.1 c63's semantic binding is self-consistent, never upstream-anchored

`c63_calibration.py` checks the ledger against the blobs *in the same tree*
(`c63_calibration.py:133-137`): `row.rawSha256 == sha256(raw_blob)`,
`row.textSha256 == sha256(text_blob)`, `row.quote == FROZEN_QUOTE`. Nothing
ties either blob to an authority outside that tree. Concretely:

* **Variant C** — replace `.ufo/waves/round-61/sources/S432.html` with a
  72-byte unrelated marketing page, replace
  `.ufo/waves/round-63/quote-class/S432.txt` with a hand-written line
  containing the quote, rewrite the ledger's two digests to match → c63
  prints `derived=collapsed-only class_match=1 … met=true`, exit 0. The
  "retained WHATWG Fetch body" is now a page about widgets, and the counter
  cannot tell.
* **Variant I** — keep the *genuine* raw HTML (digest `63b0a018…`, byte-equal
  to the round-61 receipt) but replace the flat-text blob with a one-line
  hand-written string containing the quote and update the ledger's
  `textSha256` → c63 prints `met=true`, exit 0. The class "collapsed-only"
  is then derived from a rendering that the committed recipe
  (`extract_text.py`) would never produce from that raw body.
* **Variant T** — keep every blob and the ledger byte-exact but corrupt the
  sha256 strings *quoted in the corpus prose* (the knowledge file's
  `8b90d096…` / `63b0a018…` references) → c63 still prints `met=true`,
  exit 0.

The anchors that would close this are present in the tree and are never
consulted by the counter: `receipts.json` carries the upstream S432 fetch
digest `63b0a018…`; the ledger records `locatedRawLines: "6150-6154"`;
`extract_text.py` can re-derive the text blob deterministically from the raw
blob. `grep -n "receipts|extract_text|locatedRawLines|5f48e26b"
.ufo/waves/round-63/c63_calibration.py` → **no matches**. The counter also
never pins the ledger *file's own* digest against the contract-frozen
`5f48e26b…`, so a rewritten ledger is accepted (variant C/S).

This is **not** a marker-only green (the trees do carry bodies, and the
committed controls stay red), so the C1 kill rule is not tripped. It is a
one-line-away strengthening: `sha256(ledger_blob) == 5f48e26b…` and
`row.rawSha256 == receipts.json[S432].sha256` would make C/I/S/T red. Worth
noting for the next round, since the round-63 QUALITY criterion itself
claims the counter "re-derives from committed bytes … a match class
re-derived from those blobs" — true — but never says the bytes are the
upstream bytes.

### 5.2 Two of the four `resolved` components are still token checks

`criterion` (`c63_calibration.py:147-150`) requires the substrings
`substantive`, `round-61-verifier-spotcheck`, and the three purpose terms to
appear *somewhere* in `corpus/QUALITY.md`; `lesson_gate`
(`c63_calibration.py:153-159`) requires `## Gate`, `round-61-verifier-spotcheck`,
`Disagree`, `collapsed-only` and `author-side`|`self-assessment` to appear in
`corpus/lessons/round-63.md`. Neither is a semantic check.

* **Variant K** — replace `corpus/lessons/round-63.md` with four lines
  (`## Gate` / `round-61-verifier-spotcheck Disagree collapsed-only` /
  `author-side`) → `lesson_gate=1`, `met=true`, exit 0. The real lesson
  (the outside-verdict record, the admit/reject reasoning, the re-open
  receipt) is gone and the counter does not notice.
* **Variant L** — replace `corpus/QUALITY.md` with two lines
  (`substantive round-61-verifier-spotcheck` / `X-Content-Type-Options
  Content-Type destination`) → `criterion=1`, `met=true`, exit 0. The entire
  quality bar (40+ criteria rows) is replaced by a token line.

**Variant S** stacks these: the whole corpus reduced to token stubs (stub
`QUALITY.md`, stub `lessons/round-63.md`, one-line `SOURCES.md` row,
one-line knowledge file) plus the fabricated body pair from variant C →
`met=true` on both counters. That tree contains no WHATWG Fetch body, no
substantive criterion and no lesson record — yet both counters report green.
This is the round-62 defect *shape* (assertion without evidence) surviving
in a weaker form: not marker-only, but assertion-shaped.

### 5.3 `disagreements` is printed but never gates `met`

`c63_calibration.py:165-167`: `unresolved = disagreements if not resolved
else 0`, `met = bool(resolved)`. **Variant U** — four `Disagree` lines in
`corpus/lessons/round-61-verifier-spotcheck.md` → `disagreements=4 …
unresolved=0 met=true`. The count is decoration; only `resolved` decides.
At the measured commit `disagreements=1` (the round-61 `Disagree` line is
still on disk — append-only) and the counter still reports `met=true`,
which is consistent with the contract's design (the disagreement is
*resolved* by the round-63 correction, and `resolved` requires the lesson to
record the verdict), but a reader of the printed line
`disagreements=1 … met=true` should know the `Disagree` line is never
re-examined. The `resolved` side is token-gated (5.2), so the disagreement's
*resolution* rests on the lesson's token presence, not on the counter
re-deriving it.

### 5.4 C2's counter measures the working tree, not the revision

`c63_quote_tool.py:60-67` writes the tool blob **from the revision** into a
temp dir and runs it with `cwd=root`. The tool's `s432_real` case resolves
`.ufo/waves/round-61/sources/S432.html` and
`.ufo/waves/round-63/quote-class/S432.txt` relative to `Path.cwd()`
(`scripts/quote_class.py:24,64-65,79-80`) — i.e. against the **working
tree**, not the revision. Consequences:

* **Variant O** — the *revision* has no retained blobs at all; the working
  tree has fabricated ones → C2 prints `present=1 selftest=4/4
  frozen_cases=ok met=true`, exit 0, i.e. C2 green on a revision that does
  not contain the evidence its own real case claims to test.
* **Variant P2** — the revision is the genuine measured tree; the working
  tree's raw HTML was edited to contain the quote contiguously → C2 prints
  `present=1 selftest=failed met=false`, exit 1 — C2 red on a revision that
  is perfectly good.

By contrast **C1 is hermetic**: it reads every input via
`git show <rev>:<path>`, so variants O and P2 leave its verdict unchanged
(`met=false` and `met=true` respectively, matching the committed blobs).
The C2 result is only correct when the worktree equals the revision; the
contract's freeze note acknowledges the cwd binding for the *tool*, but the
consequence for the *counter* is that "at the measured revision" is only
true of the tool blob, not of the corpus it exercises. At the real lane root
the worktree was byte-identical to the measured commit for all four
tool-fixture files and both retained blobs (verified by sha256), so
`after-c2.txt` is correct as measured — this is a latent hermeticity defect,
not a wrong receipt.

### 5.5 A stub tool greens C2 (independent reproduction)

**Variant R** — `scripts/quote_class.py` replaced by a 10-line stub that
prints a hardcoded `{"cases": [ …four frozen ids, passed=true… ],
"ok": true, "passed": 4, "total": 4}` and never opens a corpus file → C2
prints `present=1 selftest=4/4 frozen_cases=ok met=true`, exit 0. The
counter's frozen-case-set check is an id-presence check, not a tool-identity
check; `grep -n "sha256\|hashlib" .ufo/waves/round-63/c63_quote_tool.py` →
no matches, so the tool blob is never compared against the contract-frozen
`431e75e8…`. Sibling seat `ExecC2CounterAttack.md` §8.1 reports the same
class independently; I record it as corroboration with my own fixture.
This is a design property of an *operability* counter (it certifies "the
tool runs and self-reports 4/4", not "the tool is the frozen tool"), and
the contract's C2 kill rule names "a stub tool passes" — but the contract
also names the frozen tool sha256 `431e75e8…` as the thing to be counted.
Not adjudicated here.

---

## 6. What I did **not** do

No file outside `/fast/scratch/hyaku/kake-r63/ExecMarkerControl/` and this
report was written. The frozen claim, counters, ledger, tool, receipts,
`corpus/`, `SOURCES.md`, `MANIFEST.json`, `considerthese/`, `.ufo/state`
and `scripts/` were read only. No commit, push, or any other mutation of
the fleet repo or a sibling repo; the only git mutations were inside my
throwaway scratch repos. No `pacman` (paused host-wide) and no package
installs.

## 7. Cleanup

```
$ rm -rf /fast/scratch/hyaku/kake-r63/ExecMarkerControl
$ ls /fast/scratch/hyaku/kake-r63/
ExecExtractorRepro  L1  ScoutS432Reopen      # (sibling seats' scratch; mine removed)
scratch_cleanup=clean
```

## 8. Summary for the L1

1. **Assigned item: PASS.** Marker-only fixture (byte-exact copy of the
   committed round-62 fixture, throwaway identity, top-level asserted) →
   `c62_calibration.py` prints `met=true` exit 0 (defect reproduced);
   `c63_calibration.py` prints `met=false` exit 1 on the same tree. Matches
   `controls/control-marker-fixture.txt` field-for-field.
2. **Frozen predicate: holds on all three legs** (measured commit green,
   marker fixture red, base red), for C1 and C2 alike, with the after/base
   receipts reproduced verbatim.
3. **Kill rule: not tripped.** No marker-only or junk-marker tree greens
   under c63 (A, B, H, V all red; the committed controls all red).
4. **Residual risk, in priority order:** (a) c63 binds the class to
   self-consistent committed bytes and never to an upstream anchor
   (`receipts.json` digest, ledger file digest, `extract_text.py`
   re-derivation) — variants C, I, T green (5.1); (b) `criterion` and
   `lesson_gate` remain token checks — variants K, L green, and stacked
   with fabricated bodies variant S greens on both counters (5.2); (c)
   `disagreements` is decorative — variant U green with four `Disagree`
   lines (5.3); (d) C2's counter exercises the *working tree* corpus, not
   the revision — variants O and P2 flip its verdict (5.4); (e) a stub tool
   greens C2 — variant R (5.5, corroborating `ExecC2CounterAttack.md`).
5. **Independent positive evidence:** the committed class is substantively
   correct — `extract_text.py` reproduces the committed `S432.txt`
   byte-exactly from the committed `S432.html`, the retained HTML's digest
   equals the round-61 fetch receipt's `63b0a018…`, and the quote is
   genuinely split by inline markup at raw lines 6150–6154, so
   `collapsed-only` is the right class, independently re-derived.
