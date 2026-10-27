# ExecJunkControl — round-63 w1 seat report

**Item.** Build three adversarial junk fixtures (round-63 quote planted without
blobs; ledger JSON with fabricated shas; lesson+knowledge markers with a
wrong-quote variant) as scratch git repos under
`/fast/scratch/hyaku/kake-r63/ExecJunkControl/`, run `c63_calibration.py` on
each, and confirm every one prints `met=false`. Paste outputs; delete scratch
when done.

**Verdict.** All three junk fixtures print `met=false` with exit 1 against the
frozen round-63 counter. **C1's counter is not defeatable by any of the three
planted-junk families.** A supplementary fourth fixture (the committed
round-62 marker-only corpus) reproduces the historical false-green under the
old c62 counter (`met=true`) and is red under c63 (`met=false`), confirming
the defect family is closed rather than relabelled. No frozen claim, counter,
receipt, registry row or corpus file was edited; scratch deleted at end of
wave.

**Tooling.** None installed. No pacman transaction, no `uv`/`npx`/binary
install. Everything below uses pre-existing `git` and `python3`.

---

## 1. Counter under test (unmodified, frozen)

```
$ sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_calibration.py
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_calibration.py
```

Matches the contract's frozen sha256
(`bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91`) — the
counter was run **as committed**, not edited.

Positive control (the real measured commit, unmodified tree) still greens, so
the three reds below are attributable to the fixtures and not to a
counter that is simply always-red:

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

---

## 2. Fixture construction

Source of truth for every corpus byte copied into a fixture: the fleet repo at
the measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`, extracted with
`git archive` (read-only). Each fixture is an independent git repo with a
throwaway identity set **inside that repo only**.

```
$ D=/fast/scratch/hyaku/kake-r63/ExecJunkControl
$ for FX in fxA fxB fxC; do
    mkdir -p "$D/$FX"
    git -C "$D/$FX" init -q
    T=$(git -C "$D/$FX" rev-parse --show-toplevel)
    [ "$T" = "$D/$FX" ] || exit 9          # top-level asserted == fixture dir
    git -C "$D/$FX" config user.email "junk-control@scratch.invalid"
    git -C "$D/$FX" config user.name "Junk Control Fixture"
  done
fxA toplevel=/fast/scratch/hyaku/kake-r63/ExecJunkControl/fxA ok
fxB toplevel=/fast/scratch/hyaku/kake-r63/ExecJunkControl/fxB ok
fxC toplevel=/fast/scratch/hyaku/kake-r63/ExecJunkControl/fxC ok
```

Top-level assertion re-verified immediately before each fixture's first
commit; every `rev-parse --show-toplevel` printed exactly the fixture dir.

### Fixture inventory

| Fixture | Adversarial family | Planted junk | Retained blobs | Ledger |
|---|---|---|---|---|
| `fxA` | round-63 quote planted, no blobs | `[r63-correction …]` block with the exact frozen quote + ledger path in `corpus/knowledge/response-header-expectations.md`; full marker corpus (`criterion`, `lesson_gate`, `source_row` all satisfiable) | **absent** (no `.ufo/` tree at all) | **absent** |
| `fxB` | ledger JSON with fabricated shas | complete real corpus + **real** retained blobs; ledger's `textSha256`/`rawSha256` overwritten with fabricated digests | present, byte-exact real | present but **lying** |
| `fxC` | lesson+knowledge markers with a wrong-quote variant | markers planted (`[r63-correction`, ledger path, `## Gate`, `Disagree`, `collapsed-only`, `author-side`, criterion terms, S432 registry row) but the quoted span uses the **straight apostrophe** variant (`response's`) instead of the frozen typographic apostrophe (`response’s`) | present, byte-exact real | present, byte-exact real |
| `fxD` (supplementary) | the committed round-62 **marker-only** corpus, byte-exact | the historical marker-only tree that made the old c62 counter print `met=true` | **absent** | **absent** |

### Fixture digests (proving which bytes are real)

```
$ sha256sum "$D/fxC/.ufo/waves/round-61/sources/S432.html" "$D/fxC/.ufo/waves/round-63/quote-class/S432.txt"
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .../fxC/.ufo/waves/round-61/sources/S432.html
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .../fxC/.ufo/waves/round-63/quote-class/S432.txt

$ sha256sum "$D/fxB/.ufo/waves/round-61/sources/S432.html" "$D/fxB/.ufo/waves/round-63/quote-class/S432.txt"
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .../fxB/.ufo/waves/round-61/sources/S432.html
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .../fxB/.ufo/waves/round-63/quote-class/S432.txt

$ git -C "$D/fxA" ls-tree -r --name-only HEAD
corpus/QUALITY.md
corpus/SOURCES.md
corpus/knowledge/response-header-expectations.md
corpus/lessons/round-61-verifier-spotcheck.md
corpus/lessons/round-63.md
```

`fxA`'s tracked tree contains **no `.ufo/` path at all** — the retained raw
body, the flat-text rendering and the class ledger are genuinely absent, not
empty or placeholder.

`fxB`'s ledger after fabrication (line 12–13 of
`.ufo/waves/round-63/quote-class/quote-classes.json`):

```
   "textSha256": "0000000000000000000000000000000000000000000000000000000000000000",
   "rawSha256": "1111111111111111111111111111111111111111111111111111111111111111",
```

while the blobs it claims to describe are the real ones (digests above). This
is the strongest form of the attack: the ledger is present, well-formed JSON,
schema-conformant, and points at real paths — only its digests are false.

`fxC`'s planted knowledge block, verified by direct byte test:

```
$ python3 - <<'PY'   # in $D/fxC
k=open('corpus/knowledge/response-header-expectations.md',encoding='utf-8').read()
FROZEN=("The `X-Content-Type-Options` response header can be used to require "
        "checking of a response\u2019s `Content-Type` header against the "
        "destination of a request.")
print("has '[r63-correction':", "[r63-correction" in k)
print("has ledger path:", ".ufo/waves/round-63/quote-class/quote-classes.json" in k)
print("has FROZEN_QUOTE:", FROZEN in k)
print("has straight-apostrophe variant:", FROZEN.replace("\u2019","'") in k)
PY
has '[r63-correction': True
has ledger path: True
has FROZEN_QUOTE: False
has straight-apostrophe variant: True
```

So `fxC` is a fully-marker-complete, fully-blob-backed tree whose only defect
is a one-byte apostrophe substitution in the quote — precisely the class of
near-miss a marker-only predicate would wave through.

---

## 3. Results — every fixture prints `met=false`, exit 1

Single command, exact output, from the fleet repo (counter path relative to
fleet root, `--root` pointing at each scratch fixture):

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ D=/fast/scratch/hyaku/kake-r63/ExecJunkControl
$ for FX in fxA fxB fxC; do
    R=$(git -C "$D/$FX" rev-parse HEAD)
    echo "=== $FX rev=$R toplevel=$(git -C "$D/$FX" rev-parse --show-toplevel) ==="
    python3 -B .ufo/waves/round-63/c63_calibration.py --root "$D/$FX" --revision "$R" || echo "exit=$?"
    echo
  done

=== fxA rev=54256061b1289ceb3eb1b3178b8f04116c936757 toplevel=/fast/scratch/hyaku/kake-r63/ExecJunkControl/fxA ===
revision=54256061b1289ceb3eb1b3178b8f04116c936757 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1

=== fxB rev=1ae842b1e9d19702bc134e4dedb5dd1843ac2349 toplevel=/fast/scratch/hyaku/kake-r63/ExecJunkControl/fxB ===
revision=1ae842b1e9d19702bc134e4dedb5dd1843ac2349 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1

=== fxC rev=bf0d7c20f2d4f3f947e574b9de288dc57f3f5aee toplevel=/fast/scratch/hyaku/kake-r63/ExecJunkControl/fxC ===
revision=bf0d7c20f2d4f3f947e574b9de288dc57f3f5aee disagreements=1 quote_correction=0 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

**All three: `met=false`, exit 1.** No fixture greens.

### Why each goes red (component-level read of the printed fields)

- **fxA — quote planted, blobs absent.** `quote_correction=0`,
  `blobs_match=0`, `derived=unevaluable`, `class_match=0`. The correction
  block carries the frozen quote and names the ledger, and every *other*
  component is satisfiable from markers (`criterion=1 lesson_gate=1
  source_row=1`), yet `quote_correction` is 0 because there are no committed
  bytes to re-derive the digests and the match class from. The round-62
  defect family (marker strings ⇒ `resolved`) is dead: `derived=unevaluable`
  is printed explicitly, so the class is *not* assumed from the ledger or the
  knowledge prose.
- **fxB — ledger with fabricated shas.** `quote_correction=0`,
  `blobs_match=0`, `derived=unevaluable`, `class_match=0`. The ledger is
  present and well-formed, and the blobs it names are the *real* ones, but
  the counter re-derives `sha256(raw_blob)` / `sha256(text_blob)` itself and
  compares them against the ledger rows. Fabricated digests therefore fail
  `blobs_match`, and the class is never derived from the ledger's asserted
  `matchClass`. A lying ledger cannot manufacture a green.
- **fxC — markers complete, quote wrong.** This is the near-miss case and the
  most informative: `blobs_match=1`, `derived=collapsed-only`, `class_match=1`
  — the retained blobs are real, the digests re-derive, and the class is
  re-derived inline to exactly `collapsed-only`. `criterion=1`,
  `lesson_gate=1`, `source_row=1`. The **only** failing component is
  `quote_correction=0`, because the knowledge entry's quoted span is the
  straight-apostrophe variant and not the frozen typographic-apostrophe
  string. A counter that gated on "some quote about `X-Content-Type-Options`
  is present" would have greened this; the byte-exact comparison does not.
  `unresolved=1` because the round-61 S432 disagreement is still standing in
  the spot-check.
- **fxD — marker-only (supplementary).** `quote_correction=0`,
  `blobs_match=0`, `derived=unevaluable`, `class_match=0`, `criterion=0`,
  `lesson_gate=0`, `source_row=1`. This is the historical round-62 tree:
  it carries markers only, with no retained body, and it is the tree the old
  counter greened. c63 refuses it (see §4.1 for the two-counter contrast).

Note the counter's own guard structure visible in the output: `unresolved` is
the *round-61 disagreement count* and stays `1` whenever `resolved` is 0, so
each fixture reports an unresolved disagreement rather than a silently
satisfied one.

---

### 3.1 Consolidated final run (all four fixtures, one command)

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ for FX in fxA fxB fxC fxD; do
    R=$(git -C "$D/$FX" rev-parse HEAD)
    echo "=== $FX rev=$R toplevel=$(git -C "$D/$FX" rev-parse --show-toplevel) ==="
    python3 -B .ufo/waves/round-63/c63_calibration.py --root "$D/$FX" --revision "$R" || echo "exit=$?"
    echo
  done

=== fxA rev=54256061b1289ceb3eb1b3178b8f04116c936757 toplevel=/fast/scratch/hyaku/kake-r63/ExecJunkControl/fxA ===
revision=54256061b1289ceb3eb1b3178b8f04116c936757 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1

=== fxB rev=1ae842b1e9d19702bc134e4dedb5dd1843ac2349 toplevel=/fast/scratch/hyaku/kake-r63/ExecJunkControl/fxB ===
revision=1ae842b1e9d19702bc134e4dedb5dd1843ac2349 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1

=== fxC rev=bf0d7c20f2d4f3f947e574b9de288dc57f3f5aee toplevel=/fast/scratch/hyaku/kake-r63/ExecJunkControl/fxC ===
revision=bf0d7c20f2d4f3f947e574b9de288dc57f3f5aee disagreements=1 quote_correction=0 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1

=== fxD rev=47449b0eb31f1e735634f3e17baced9fa7902ab1 toplevel=/fast/scratch/hyaku/kake-r63/ExecJunkControl/fxD ===
revision=47449b0eb31f1e735634f3e17baced9fa7902ab1 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

**Four fixtures, four `met=false`, four exit 1.**

---

## 4. Contrast — the same fixtures against the round-62 (defective) counter

To confirm the fixtures are genuinely adversarial and not merely malformed
trees, each was also run against the old, marker-only round-62 counter
(`.ufo/waves/round-62/c62_calibration.py`, unmodified, still committed as
defect history per the contract's No-harm clause):

```
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root "$D/fxA" --revision <fxA rev>
revision=54256061b1289ceb3eb1b3178b8f04116c936757 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1

$ python3 -B .ufo/waves/round-62/c62_calibration.py --root "$D/fxB" --revision <fxB rev>
revision=1ae842b1e9d19702bc134e4dedb5dd1843ac2349 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1

$ python3 -B .ufo/waves/round-62/c62_calibration.py --root "$D/fxC" --revision <fxC rev>
revision=bf0d7c20f2d4f3f947e574b9de288dc57f3f5aee disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

The old counter also refuses these three, because none of them carries c62's
specific literal marker set. Per-gate reason, measured directly against each
fixture's committed blobs:

```
$ python3 - <<'PY'   # in $D/<fx>
q=("response header can be used to require checking of a response’s Content-Type "
   "header against the destination of a request")
for fx in ("fxA","fxB","fxC"):
    def blob(p):
        r=subprocess.run(["git","-C",root,"show",f"HEAD:{p}"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return "" if r.returncode else r.stdout.decode("utf-8","replace")
    k=blob("corpus/knowledge/response-header-expectations.md")
    ql=blob("corpus/QUALITY.md")
    print(fx,
          "| c62 QUOTE in knowledge:", q in k,
          "| 'S432 §3.6' in knowledge:", "S432 §3.6" in k,
          "| 'Round-62 correction' in knowledge:", "Round-62 correction" in k,
          "| 'substantive located quote' in QUALITY:", "substantive located quote" in ql,
          "| round-62.md lesson exists:", bool(blob("corpus/lessons/round-62.md")))
PY
fxA | c62 QUOTE in knowledge: False | 'S432 §3.6' in knowledge: True | 'Round-62 correction' in knowledge: True | 'substantive located quote' in QUALITY: False | round-62.md lesson exists: False
fxB | c62 QUOTE in knowledge: False | 'S432 §3.6' in knowledge: True | 'Round-62 correction' in knowledge: True | 'substantive located quote' in QUALITY: False | round-62.md lesson exists: False
fxC | c62 QUOTE in knowledge: False | 'S432 §3.6' in knowledge: False | 'Round-62 correction' in knowledge: False | 'substantive located quote' in QUALITY: False | round-62.md lesson exists: False
```

c62's `correction` gate is
`QUOTE in knowledge and "S432 §3.6" in knowledge and "Round-62 correction" in knowledge`
(`.ufo/waves/round-62/c62_calibration.py:33-34`) and its `criterion` gate
requires the literal phrase `substantive located quote`
(`.ufo/waves/round-62/c62_calibration.py:14,35`) — none of which the round-63
trees satisfy. So the three junk fixtures do not themselves reproduce the
round-62 false-green.

### 4.1 Supplementary: the committed round-62 marker-only fixture (fxD)

Because the contract's kill rule fires if "any wave attack reproduces a
marker-only green", the committed round-62 marker-only corpus was
re-committed byte-exact into a fourth scratch fixture and run through **both**
counters. This is the decisive contrast — it is the same tree the old counter
greened:

```
$ git -C "$SRC" archive --format=tar "$REV" .ufo/waves/round-62/controls/false-green-fixture/corpus | tar -x -C "$D/fxD"
$ mv "$D/fxD/.ufo/waves/round-62/controls/false-green-fixture/corpus" "$D/fxD/corpus"
$ rm -rf "$D/fxD/.ufo"
$ git -C "$D/fxD" add -A && git -C "$D/fxD" commit -q -m "marker-only fixture (round-62 committed corpus)"
fxD rev=47449b0eb31f1e735634f3e17baced9fa7902ab1 toplevel=/fast/scratch/hyaku/kake-r63/ExecJunkControl/fxD

$ git -C "$D/fxD" ls-tree -r --name-only HEAD
corpus/QUALITY.md
corpus/SOURCES.md
corpus/knowledge/response-header-expectations.md
corpus/lessons/round-61-verifier-spotcheck.md
corpus/lessons/round-62.md
```

```
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root "$D/fxD" --revision 47449b0eb31f1e735634f3e17baced9fa7902ab1
revision=47449b0eb31f1e735634f3e17baced9fa7902ab1 disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
exit=0

$ python3 -B .ufo/waves/round-63/c63_calibration.py --root "$D/fxD" --revision 47449b0eb31f1e735634f3e17baced9fa7902ab1
revision=47449b0eb31f1e735634f3e17baced9fa7902ab1 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

**The round-62 false-green reproduces exactly on the tree that produced it
(`c62 → met=true`, exit 0) and is dead on the repaired counter
(`c63 → met=false`, exit 1).** This independently confirms the committed
receipt
`.ufo/waves/round-63/controls/control-marker-fixture.txt` from a freshly
built scratch repo, and it shows the defect family is genuinely closed
rather than merely re-labelled. The marker-only tree has no retained blobs
and no ledger, so c63 prints `derived=unevaluable` / `blobs_match=0` /
`class_match=0` — the class is never asserted from prose.

### 4.2 Mechanism, as printed

- c62 gates `quote_correction` on **literal marker strings** in the knowledge
  file — no digest, no class, no retained body
  (`.ufo/waves/round-62/c62_calibration.py:33-34`).
- c63 replaces that with **digest re-derivation from committed bytes plus
  inline class re-derivation** (`.ufo/waves/round-63/c63_calibration.py:106-145`):
  `sha256(raw_blob)` / `sha256(text_blob)` are compared against the ledger
  rows, and the class is recomputed from the blobs by the inlined
  `classify()` (`.ufo/waves/round-63/c63_calibration.py:59-68`) rather than
  read from the ledger's asserted `matchClass`.

That difference is exactly what the four fixtures exercise: `fxA` removes the
bytes, `fxB` lies about the digests, `fxC` misquotes the span, `fxD` is the
historical marker-only green. All four are red under c63.

---

## 5. Constraint compliance

- **No fleet-repo mutation.** The only file written under the fleet root is
  this report,
  `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ExecJunkControl.md`.
  The frozen counter, its receipts (`after-c1.txt`, `after-c2.txt`,
  `base-c1.txt`, `base-c2.txt`, `control-marker-fixture.txt`,
  `control-junk-fixture.txt`), the contract, `MANIFEST.json`, `considerthese/`,
  `.ufo/state`, `scripts/`, `templates/` and this lane's `corpus/SOURCES.md`
  were read only. The S432 registry row is untouched.
- **No git/jj mutation outside scratch.** All `git init`, `git add`,
  `git commit` and `git archive` calls targeted
  `/fast/scratch/hyaku/kake-r63/ExecJunkControl/<fx>` only; `git archive` on
  the fleet repo is read-only. No commit, push, branch or tag was created in
  the fleet repo. No `jj` invocation.
- **Fixture identity.** Throwaway identity (`junk-control@scratch.invalid` /
  `Junk Control Fixture`) configured with `git -C <fixture> config`, i.e.
  local to each scratch repo only; no global git config touched.
- **No pacman.** No pacman transaction of any kind.
- **No installs.** No `uv tool install`, no `npx`, no binary written to
  `~/.local/bin` or any PATH directory.
- **Scratch cleanup.** The whole `/fast/scratch/hyaku/kake-r63/ExecJunkControl/`
  tree was deleted after the runs (evidence below).

## 6. Cleanup

```
$ rm -rf /fast/scratch/hyaku/kake-r63/ExecJunkControl
$ ls -la /fast/scratch/hyaku/kake-r63/
total 20
drwxr-xr-x 23 vgpnk vgpnk   4096 Oct 27 10:34 .
drwxr-xr-x 18 vgpnk vgpnk   4096 Oct 27 10:30 ..
drwxr-xr-x  2 vgpnk vgpnk      6 Oct 27 10:31 CriticToolValue
drwxr-xr-x 29 vgpnk vgpnk    4096 Oct 27 10:34 ExecCounterControls
drwxr-xr-x  9 vgpnk vgpnk    187 Oct 27 10:33 ExecDoNothingControl
drwxr-xr-x  5 vgpnk vgpnk    106 Oct 27 10:33 ExecExitCodes
drwxr-xr-x  3 vgpnk vgpnk     83 Oct 27 10:29 ExecLedgerMutation
drwxr-xr-x  6 vgpnk vgpnk     62 Oct 27 10:28 ExecMarkerControl
drwxr-xr-x  8 vgpnk vgpnk    144 Oct 27 10:33 ExecReceiptReproduce
drwxr-xr-x  6 vgpnk vgpnk     82 Oct 27 10:32 ExecStubControl
drwxr-xr-x  6 vgpnk vgpnk     58 Oct 27 10:34 ExecSwappedLabel
drwxr-xr-x  4 vgpnk vgpnk    163 Oct 27 10:28 L1
drwxr-xr-x  4 vgpnk vgpnk     67 Oct 27 10:34 MutC1Counter
drwxr-xr-x  2 vgpnk vgpnk   4096 Oct 27 10:34 MutExtractor
drwxr-xr-x  3 vgpnk vgpnk     20 Oct 27 10:32 MutLedger
drwxr-xr-x  2 vgpnk vgpnk   4096 Oct 27 10:34 MutTool
drwxr-xr-x  3 vgpnk vgpnk     17 Oct 27 10:32 ReviewerC1Semantics
drwxr-xr-x  3 vgpnk vgpnk     17 Oct 27 10:33 ReviewerC1Separability
drwxr-xr-x  2 vgpnk vgpnk     30 Oct 27 10:34 ReviewerFalseGreenDead
drwxr-xr-x  3 vgpnk vgpnk     21 Oct 27 10:34 ReviewerQualityCriteria
drwxr-xr-x  4 vgpnk vgpnk     32 Oct 27 10:34 ReviewerReceiptIntegrity
drwxr-xr-x  2 vgpnk vgpnk     29 Oct 27 10:25 ScoutS432Reopen
drwxr-xr-x  4 vgpnk vgpnk     27 Oct 27 10:31 ScribeQualityCriterion

$ test -e /fast/scratch/hyaku/kake-r63/ExecJunkControl && echo "STILL EXISTS" || echo "ExecJunkControl scratch removed"
ExecJunkControl scratch removed
```

All four fixture repos (`fxA`–`fxD`), their `.git` dirs and their throwaway
identities are gone with the tree.

## 6.1 Post-run verification that the fleet repo was not mutated

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && git status --porcelain
?? .ufo/waves/round-63/w1.ready
?? .ufo/waves/round-63/w1.ready.dispatched
?? .ufo/waves/round-63/w1/
```

The only untracked path is this wave's report directory (this report and the
sibling seats' reports) plus the orchestrator's `w1.ready*` markers — none
written by this seat. No tracked file is modified, no staged change, no commit
was made by this seat.

The three frozen artifacts this seat attacked remain byte-identical to their
contract shas after the run:

```
$ sha256sum .ufo/waves/round-63/c63_calibration.py scripts/quote_class.py .ufo/waves/round-63/quote-class/quote-classes.json
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  .ufo/waves/round-63/c63_calibration.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  .ufo/waves/round-63/quote-class/quote-classes.json
```

All three match the contract's frozen digests exactly.

## 7. Risk / blocker statement

- **Risks.** None outstanding for C1's counter from these three families. The
  residual exposure is bounded by what the counter does *not* bind: it does
  not check that `corpus/QUALITY.md`'s criterion text is itself substantively
  correct, only that the named proposition terms appear — so a future tree
  could satisfy `criterion=1` with a hollow criterion. That is outside this
  seat's three named junk families and outside the frozen counter's sha
  (which this seat may not edit), so it is recorded as an observation only.
- **Blockers.** None.
