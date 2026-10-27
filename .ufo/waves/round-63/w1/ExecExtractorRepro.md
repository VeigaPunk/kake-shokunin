# Seat ExecExtractorRepro — round-63 w1

**Item:** re-run `.ufo/waves/round-63/quote-class/extract_text.py --raw
.ufo/waves/round-61/sources/S432.html --out <scratch>/S432.txt` from the lane root,
byte-compare the output against the committed
`.ufo/waves/round-63/quote-class/S432.txt` with `cmp`, and run `--selftest`.

**Scope:** C1 (calibration) reproduction of the retained-HTML → flat-text step
that the round-63 class ledger
(`.ufo/waves/round-63/quote-class/quote-classes.json`) names as its `recipe`.
Read-only against the fleet repo; nothing outside my scratch and this report
was written.

**Verdict: REPRODUCED — byte-identical.** The committed flat-text blob is
exactly the deterministic output of the frozen extractor over the retained raw
blob, on every interpreter available on this host.

---

## 1. Environment and inputs (absolute paths)

Lane root (cwd for all commands below):
`/home/vgpnk/Projects/shokunin/kake-shokunin`
Scratch: `/fast/scratch/hyaku/kake-r63/ExecExtractorRepro/`
(only created with `mkdir -p`; no fixture git repo was needed — this seat
performs no mutation, so no `git init`/`rev-parse` assertion applies).

```
$ mkdir -p /fast/scratch/hyaku/kake-r63/ExecExtractorRepro
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -V
Python 3.14.8
```

Interpreter set present on this host (used for the stability sweep in §5):
`python3`→3.14.8, `python3.13`→3.13.16, `python3.12`→3.12.15, `python3.11`→3.11.17.

Input digests (worktree):

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && sha256sum \
    .ufo/waves/round-63/quote-class/extract_text.py \
    .ufo/waves/round-63/quote-class/S432.txt \
    .ufo/waves/round-61/sources/S432.html
6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405  .ufo/waves/round-63/quote-class/extract_text.py
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .ufo/waves/round-63/quote-class/S432.txt
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html
```

These three match the ledger's `rawSha256` / `textSha256` fields
(`quote-classes.json:12-13`) exactly, and the extractor sha256
`6b0a88cd…f362405` is the blob committed at the measured revision
(§4).

---

## 2. The three requested commands, verbatim output

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-63/quote-class/extract_text.py \
    --raw .ufo/waves/round-61/sources/S432.html \
    --out /fast/scratch/hyaku/kake-r63/ExecExtractorRepro/S432.txt
extracted 1854393 bytes -> 286933 chars
exit=0

$ cmp .ufo/waves/round-63/quote-class/S432.txt \
      /fast/scratch/hyaku/kake-r63/ExecExtractorRepro/S432.txt
exit=0            # cmp is silent on equality; exit status 0 == identical

$ python3 -B .ufo/waves/round-63/quote-class/extract_text.py --selftest
selftest 1/1
exit=0
```

Corroborating digests and sizes of the two compared files:

```
$ sha256sum /fast/scratch/hyaku/kake-r63/ExecExtractorRepro/S432.txt \
             .ufo/waves/round-63/quote-class/S432.txt
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  /fast/scratch/hyaku/kake-r63/ExecExtractorRepro/S432.txt
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .ufo/waves/round-63/quote-class/S432.txt

$ wc -c /fast/scratch/hyaku/kake-r63/ExecExtractorRepro/S432.txt \
         .ufo/waves/round-63/quote-class/S432.txt
290480 /fast/scratch/hyaku/kake-r63/ExecExtractorRepro/S432.txt
290480 .ufo/waves/round-63/quote-class/S432.txt
```

`cmp -l` between the two files emits no differing byte positions (empty
output), so the match is byte-for-byte, not merely same-length or
same-hash.

---

## 3. C1 linkage: the reproduced blob re-derives `collapsed-only`

The committed ledger row (`quote-classes.json:5-21`) records
`matchClass: "collapsed-only"` for the S432 purpose span. Using the counter's
own inlined round-50 classifier (`c63_calibration.py:60-71`, `classify()`),
loaded as a module and fed the **freshly reproduced** text (not the committed
file), plus the retained raw blob:

```
$ python3 - <<'EOF'   # in lane root
import importlib.util
spec=importlib.util.spec_from_file_location("c63",".ufo/waves/round-63/c63_calibration.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw=open('.ufo/waves/round-61/sources/S432.html',encoding='utf-8',errors='replace').read()
fresh=open('/fast/scratch/hyaku/kake-r63/ExecExtractorRepro/S432.txt',encoding='utf-8').read()
committed=open('.ufo/waves/round-63/quote-class/S432.txt',encoding='utf-8').read()
print("class(fresh output) =",m.classify(m.FROZEN_QUOTE,raw,fresh))
print("class(committed txt)=",m.classify(m.FROZEN_QUOTE,raw,committed))
print("fresh == committed bytes:",fresh==committed)
EOF
class(fresh output) = collapsed-only
class(committed txt)= collapsed-only
fresh == committed bytes: True
```

The `collapsed-only` classification is therefore **reproducible from the
retained bytes by an independent reader**, exactly the property C1 claims
(round-50 semantics). The class is a property of the pair (raw, flat-text),
not an assertion in the ledger.

Direct evidence that the span is genuinely *not* a raw substring — i.e. that
`collapsed-only` is the honest class and not a mislabel:

```
quote in FLAT TEXT: True
quote in RAW bytes: False
quote(no backticks) in RAW bytes: False
```

The raw blob carries the sentence split across inline markup; the flat-text
rendering carries it contiguous. Raw lines 6150-6154 (the ledger's
`locatedRawLines`) of
`.ufo/waves/round-61/sources/S432.html`:

```
raw line 6150:    <p>The
raw line 6151: `<dfn class="dfn-paneled" data-dfn-type="http-header" data-export id="http-x-content-type-options"><code>X-Content-Type-Options</code></dfn>`
raw line 6152: response <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑤">header</a> can be used to require checking of a <a data-link-type="dfn" href="#concept-response" id="ref-for-concept-response④①">response</a>’s
raw line 6153: `<code>Content-Type</code>` <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑥">header</a> against the <a data-link-type="dfn" href="#concept-request-destination" id="ref-for-concept-request-destination①⓪">destination</a> of a
raw line 6154: <a data-link-type="dfn" href="#concept-request" id="ref-for-concept-request①⓪⑦">request</a>.
```

The C1 counter, run read-only at the measured revision, is consistent with
this reproduction:

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . \
    --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
c1_exit=0
```

---

## 4. Reproduction from the measured commit's blobs alone (worktree-independent)

To rule out any dependence on the live working tree, the three blobs were
extracted from the measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`
with `git show` and the extractor was run against those blobs alone:

```
$ git show 05b0d7f4…c06f:.ufo/waves/round-63/quote-class/extract_text.py  > $S/blob-extract_text.py
$ git show 05b0d7f4…c06f:.ufo/waves/round-61/sources/S432.html            > $S/blob-S432.html
$ git show 05b0d7f4…c06f:.ufo/waves/round-63/quote-class/S432.txt         > $S/blob-S432.txt
$ python3 -B $S/blob-extract_text.py --raw $S/blob-S432.html --out $S/blob-out.txt
extracted 1854393 bytes -> 286933 chars
exit=0
$ cmp $S/blob-S432.txt $S/blob-out.txt
cmp_blob_exit=0
$ python3 -B $S/blob-extract_text.py --selftest
selftest 1/1
selftest_blob_exit=0
```

Blob digests at the measured commit vs. worktree (all identical, i.e. the
worktree carries no post-measurement drift in these paths):

```
6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405  blob:.ufo/waves/round-63/quote-class/extract_text.py
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  blob:.ufo/waves/round-63/quote-class/S432.txt
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  blob:.ufo/waves/round-63/quote-class/quote-classes.json
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  blob:.ufo/waves/round-61/sources/S432.html
```
(identical to the worktree sha256s listed in §1)

The ledger's `quote-classes.json` sha256 is
`5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d`, matching
the contract's frozen C1 ledger digest.

---

## 5. Determinism / robustness sweep (extra, within item scope)

**Same cwd, three runs** — identical output each time:

```
$ cd $S && python3 -B <abs>/extract_text.py --raw <abs>/S432.html --out $S/S432-run2.txt
extracted 1854393 bytes -> 286933 chars ; cmp_run2_exit=0
$ cd /tmp && python3 -B <abs>/extract_text.py --raw <abs>/S432.html --out $S/S432-run3.txt
extracted 1854393 bytes -> 286933 chars ; cmp_run3_exit=0
```

**Cwd-independence**: the extractor resolves nothing relative to cwd (it takes
`--raw`/`--out` as explicit paths and reads only those), and the outputs match
the committed blob byte-for-byte when run from the lane root, from the scratch
dir, and from `/tmp`.

**Interpreter-independence** (the only real risk for a "byte-stable"
rendering claim, since `html.parser` is stdlib):

```
py3.11: byte-identical to committed S432.txt
py3.12: byte-identical to committed S432.txt
py3.13: byte-identical to committed S432.txt
py3.14: byte-identical
```

Selftest on each: `selftest 1/1` for 3.11, 3.12, 3.13, 3.14.

So the committed flat-text blob is stable across the interpreter versions
available here, not just under the one `python3` that happened to be first on
PATH.

---

## 6. Findings, risks, blockers

**Findings (all positive, no defect found in this seat's scope):**

1. `extract_text.py` reproduces the committed `S432.txt` **byte-for-byte**
   (`cmp` exit 0, sha256 `8b90d096…2a69`, 290480 bytes) — the ledger's
   `textSha256` is not an unverifiable assertion.
2. `--selftest` prints `selftest 1/1` (exit 0) on 3.11/3.12/3.13/3.14.
3. The reproduced text re-derives `collapsed-only` via the C1 counter's
   inlined round-50 classifier; the quote is genuinely absent from the raw
   bytes and present in the flat text, so the class label is honest.
4. The same result is obtained from the measured commit's git blobs alone, so
   the reproduction is not an artifact of the current working tree.
5. The ledger's `rawSha256`/`textSha256` and the C1 counter's `blobs_match=1`
   agree with independently recomputed digests of the retained blobs.

**Risks / notes for the orchestrator (advisory only — no file was edited):**

- The extractor is *not* pinned by sha256 anywhere in the round-63 contract
  (the contract freezes `c63_calibration.py` and `scripts/quote_class.py`;
  the ledger names the extractor only by path in its `recipe` field, and no
  sha256 of `extract_text.py` — `6b0a88cd…f362405` — is recorded in
  `quote-classes.json` or in `contract.md`). The recipe is therefore
  reproducible today but not tamper-evident the way the frozen tool is: a
  future edit to `extract_text.py` that preserved the output bytes would go
  unnoticed, and one that changed them would invalidate the ledger's
  `textSha256` without any receipt pointing at the extractor. This is a
  contract-completeness observation for the next round, not a round-63 defect:
  the frozen claim as written is satisfied.
- `extract_text.py`'s `--selftest` covers only 1 synthetic case
  (`selftest 1/1`), while the sibling lane tool `scripts/quote_class.py`
  carries 4 frozen cases (`selftest 4/4` per the C2 predicate). The
  extractor's selftest asserts entity-decoded-once / inline-concat /
  block-boundary / script-omission semantics on a 4-element sample but does
  not exercise the retained-blob path. Not a blocker for C1/C2 as frozen —
  C1 re-derives the class inline and never gates on the tool — but it means
  the extractor itself is not independently pinned by its own selftest.
- `locateRawLines` in the ledger is `6150-6154`; the raw file's line 6150 is
  the bare `<p>The` and the sentence's inline-markup continuation runs
  6151-6154. The range is correct but includes the `<p>` opener; no
  ambiguity that affects the claim.
- No credentials, network calls, or external state are touched by this seat's
  commands; `git` was used read-only (`show`, `ls-tree`, `rev-parse`,
  `status`). No pacman/uv/npx install was performed, so there is nothing to
  record under the operator tooling authorization.

**Blockers:** none.

---

## 7. Files written by this seat

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ExecExtractorRepro.md`
  (this report) — the only file written outside scratch.

Scratch (transient evidence, under the seat's assigned scratch root):
`/fast/scratch/hyaku/kake-r63/ExecExtractorRepro/` — contained `S432.txt`,
`S432-run2.txt`, `S432-run3.txt`, `S432-py3.11.txt`, `S432-py3.12.txt`,
`S432-py3.13.txt`, `blob-extract_text.py`, `blob-S432.html`, `blob-S432.txt`,
`blob-out.txt`. The scratch dir was **removed after the measurements**
(`rm -rf /fast/scratch/hyaku/kake-r63/ExecExtractorRepro`; the tree contained
no git fixture — `git rev-parse --show-toplevel` there reported "not a git
repository"), so the commands in §7 recreate it from scratch if re-run.

No fixture git repository was created (this seat mutates nothing), so no
`git init`/`rev-parse --show-toplevel` assertion and no scratch-repo teardown
were required.

**Commands run, for exact replay** (lane root = `/home/vgpnk/Projects/shokunin/kake-shokunin`):

```bash
mkdir -p /fast/scratch/hyaku/kake-r63/ExecExtractorRepro
cd /home/vgpnk/Projects/shokunin/kake-shokunin
sha256sum .ufo/waves/round-63/quote-class/extract_text.py \
          .ufo/waves/round-63/quote-class/S432.txt \
          .ufo/waves/round-61/sources/S432.html
python3 -B .ufo/waves/round-63/quote-class/extract_text.py \
  --raw .ufo/waves/round-61/sources/S432.html \
  --out /fast/scratch/hyaku/kake-r63/ExecExtractorRepro/S432.txt
cmp .ufo/waves/round-63/quote-class/S432.txt \
    /fast/scratch/hyaku/kake-r63/ExecExtractorRepro/S432.txt
python3 -B .ufo/waves/round-63/quote-class/extract_text.py --selftest
```
