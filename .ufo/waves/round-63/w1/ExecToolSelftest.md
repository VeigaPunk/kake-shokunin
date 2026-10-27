# ExecToolSelftest — round-63 w1 report

**Seat:** ExecToolSelftest (leaf executor; single labrat, no subagent dispatch)
**Item:** Run `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py --selftest` and `--selftest --json` from the lane root; then exercise `classify` on the three fixture pairs under `scripts/fixtures/quote-class/` plus a missing-file case (expect exit 2) and an empty-quote case. Paste all outputs.

**Lane root (cwd for every command below):** `/home/vgpnk/Projects/shokunin/kake-shokunin`
**Measured commit:** `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` — base (round-62 tip) `13d4519818db28cd0aa912e49020659140d7b9fa`
**Scratch:** `/fast/scratch/hyaku/kake-r63/ExecToolSelftest/` (deleted on completion; `scratch_cleanup=clean`)

**Scope note:** the item says "three fixture pairs under `scripts/fixtures/quote-class/`". That directory holds **two** pairs of files (`inline.raw.html`/`inline.txt`, `markup.raw.html`/`markup.txt`), and the frozen tool's case set has **four** cases. The third pair used by the tool is the S432 pair, whose two blobs live *outside* that directory (`.ufo/waves/round-61/sources/S432.html` + `.ufo/waves/round-63/quote-class/S432.txt`); the fourth case (`absent_everywhere`) re-uses the inline pair with a different quote. I exercised **all four** frozen cases plus the two non-fixture cases, so both readings of "three fixture pairs" are covered. Verified at `scripts/quote_class.py:42-79` (case set) and `scripts/fixtures/quote-class/` (2 pairs, 4 files).

**Verdict:** the item's literal request is **fully satisfied** — `--selftest` prints `selftest 4/4` exit 0, `--selftest --json` prints `{"ok": true, "passed": 4, "total": 4}` exit 0, all three fixture pairs classify correctly, the missing-file case exits 2 as specified, and the empty-quote case runs and exits 0. **However, three defects in the frozen tool/counter surface are material and are reported below**: (1) the C2 counter is not revision-pinned — it reads the tool's *inputs* from the **worktree**, not from the committed bytes at `--revision`, so a green can be produced against a revision whose committed tree is red; (2) the C2 counter accepts a **stub tool** that hardcodes the four frozen case ids and derives nothing (the contract's kill rule names "a stub tool passes" as unprovable); (3) the round-63 class semantics **diverge from round-50** for spans present in raw-but-not-text.

---

## 1. Environment and provenance

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && git rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/kake-shokunin
$ git rev-parse HEAD
15eb965c1d0f23ce2a522c651e9306a0952da7d3
$ git log --oneline 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f..HEAD
15eb965c round-63: w1 wave spec + validated dispatch (64 seats, v2 policy)
7f77d12b round-63: green-after receipts at measured commit 05b0d7f4
$ git diff --stat 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f..HEAD -- scripts/quote_class.py scripts/fixtures/quote-class/ .ufo/waves/round-61/sources/S432.html .ufo/waves/round-63/quote-class/
(empty — none of the tool's six input paths changed after the measured revision)
```

Frozen shas, re-derived from the **committed blobs at the measured revision** (not the worktree):

```
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:scripts/quote_class.py | sha256sum
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  -
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:.ufo/waves/round-63/c63_quote_tool.py | sha256sum
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  -
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:.ufo/waves/round-63/c63_calibration.py | sha256sum
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  -
$ git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:.ufo/waves/round-63/quote-class/quote-classes.json | sha256sum
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  -
```

All four match the contract's frozen values **exactly**. The tool under test is the frozen one.

Worktree-vs-revision equality for every path the tool's selftest reads (all six `SAME`, so the after-state is not a worktree artifact):

```
$ for p in scripts/fixtures/quote-class/inline.raw.html scripts/fixtures/quote-class/inline.txt \
           scripts/fixtures/quote-class/markup.raw.html scripts/fixtures/quote-class/markup.txt \
           .ufo/waves/round-61/sources/S432.html .ufo/waves/round-63/quote-class/S432.txt; do
    A=$(git show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:$p | sha256sum | cut -d' ' -f1)
    B=$(sha256sum "$p" | cut -d' ' -f1)
    [ "$A" = "$B" ] && echo "SAME  $p" || echo "DIFF  $p rev=$A wt=$B"
  done
SAME  scripts/fixtures/quote-class/inline.raw.html
SAME  scripts/fixtures/quote-class/inline.txt
SAME  scripts/fixtures/quote-class/markup.raw.html
SAME  scripts/fixtures/quote-class/markup.txt
SAME  .ufo/waves/round-61/sources/S432.html
SAME  .ufo/waves/round-63/quote-class/S432.txt
```

---

## 2. The item's commands, verbatim output

### 2.1 `--selftest`

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B scripts/quote_class.py --selftest
case inline_raw_substring: derived=raw-substring expected=raw-substring pass
case markup_collapsed_only: derived=collapsed-only expected=collapsed-only pass
case absent_everywhere: derived=absent expected=absent pass
case s432_real: derived=collapsed-only expected=collapsed-only pass
selftest 4/4
exit=0
```

### 2.2 `--selftest --json`

```
$ python3 -B scripts/quote_class.py --selftest --json
{"cases": [{"derived": "raw-substring", "expected": "raw-substring", "id": "inline_raw_substring", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "markup_collapsed_only", "passed": true}, {"derived": "absent", "expected": "absent", "id": "absent_everywhere", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "s432_real", "passed": true}], "ok": true, "passed": 4, "total": 4}
exit=0
```

Both match the committed after-receipt `.ufo/waves/round-63/controls/after-c2.txt` (which records `present=1 selftest=4/4 frozen_cases=ok met=true`, exit 0). The four frozen case ids are exactly the contract's `inline_raw_substring`, `markup_collapsed_only`, `absent_everywhere`, `s432_real`.

### 2.3 `classify` on the fixture pairs

Fixture file contents (for the reader's reference):

```
$ cat scripts/fixtures/quote-class/inline.raw.html
<p>The quick brown fox jumps over the lazy dog.</p>
$ cat scripts/fixtures/quote-class/inline.txt
The quick brown fox jumps over the lazy dog.
$ cat scripts/fixtures/quote-class/markup.raw.html
<p>The `<dfn data-dfn-type="http-header"><code>X-Content-Type-Options</code></dfn>` header marks the response.</p>
$ cat scripts/fixtures/quote-class/markup.txt
The `X-Content-Type-Options` header marks the response.
```

```
$ python3 -B scripts/quote_class.py classify --quote "quick brown fox" \
      --raw scripts/fixtures/quote-class/inline.raw.html --text scripts/fixtures/quote-class/inline.txt
derived=raw-substring
exit=0

$ python3 -B scripts/quote_class.py classify --quote 'The `X-Content-Type-Options` header marks the response' \
      --raw scripts/fixtures/quote-class/markup.raw.html --text scripts/fixtures/quote-class/markup.txt
derived=collapsed-only
exit=0

$ python3 -B scripts/quote_class.py classify --quote 'The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.' \
      --raw .ufo/waves/round-61/sources/S432.html --text .ufo/waves/round-63/quote-class/S432.txt
derived=collapsed-only
exit=0

$ python3 -B scripts/quote_class.py classify --quote "this span occurs in no retained blob at all" \
      --raw scripts/fixtures/quote-class/inline.raw.html --text scripts/fixtures/quote-class/inline.txt
derived=absent
exit=0
```

All four agree with the frozen expectations. The S432 case derives `collapsed-only` for a real reason — the frozen span is *not* a substring of the retained HTML, and only becomes one after markup removal and whitespace collapse:

```
$ python3 - <<'PY'
raw  = Path(".ufo/waves/round-61/sources/S432.html").read_bytes().decode("utf-8","replace")
text = Path(".ufo/waves/round-63/quote-class/S432.txt").read_bytes().decode("utf-8","replace")
q = ("The `X-Content-Type-Options` response header can be used to require "
     "checking of a response\u2019s `Content-Type` header against the "
     "destination of a request.")
print("quote in RAW :", q in raw)
print("quote in TEXT:", q in text)
PY
quote in RAW : False
quote in TEXT: True
```

And the committed flat-text blob is reproducible byte-for-byte from the committed raw blob by the committed recipe (independent re-derivation, not asserted):

```
$ python3 -B .ufo/waves/round-63/quote-class/extract_text.py --raw ./S432.html --out ./S432.repro.txt
extracted 1854393 bytes -> 286933 chars
$ sha256sum ./S432.repro.txt .ufo/waves/round-63/quote-class/S432.txt
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  ./S432.repro.txt
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .../S432.txt
```

That reproduction sha equals the ledger's `textSha256` (`8b90d096…`), and the raw blob's sha equals the ledger's `rawSha256` (`63b0a018…`) — both re-derived from the committed blobs at the measured revision. The ledger is internally truthful.

### 2.4 Missing-file case (expect exit 2) — **passes**

```
$ python3 -B scripts/quote_class.py classify --quote "quick brown fox" \
      --raw scripts/fixtures/quote-class/NOPE.raw.html --text scripts/fixtures/quote-class/inline.txt
could-not-evaluate: FileNotFoundError: [Errno 2] No such file or directory: 'scripts/fixtures/quote-class/NOPE.raw.html'
exit=2

$ python3 -B scripts/quote_class.py classify --quote "quick brown fox" \
      --raw scripts/fixtures/quote-class/inline.raw.html --text scripts/fixtures/quote-class/NOPE.txt
could-not-evaluate: FileNotFoundError: [Errno 2] No such file or directory: 'scripts/fixtures/quote-class/NOPE.txt'
exit=2
```

Also, a directory where a blob is expected:

```
$ python3 -B scripts/quote_class.py classify --quote "quick brown fox" \
      --raw scripts/fixtures/quote-class --text scripts/fixtures/quote-class/inline.txt
could-not-evaluate: IsADirectoryError: [Errno 21] Is a directory: 'scripts/fixtures/quote-class'
exit=2
```

The tool's docstring (`scripts/quote_class.py:14`) promises "Exits: 0 determination printed; 2 unreadable input or usage fault." — met for the missing-file case.

### 2.5 Empty-quote case — runs, exits 0, **but reports `raw-substring`**

```
$ python3 -B scripts/quote_class.py classify --quote "" \
      --raw scripts/fixtures/quote-class/inline.raw.html --text scripts/fixtures/quote-class/inline.txt
derived=raw-substring
exit=0
```

This is not a crash, but it is a **silent wrong answer**: `""` is a substring of every string, so `classify` short-circuits at `scripts/quote_class.py:35` (`if quote in raw: return "raw-substring"`) and reports the most specific class for a quote that names no span at all. An empty quote is an **absent** span, not a raw substring; the tool has no guard for it and no distinct exit code. A caller that passes an unset shell variable (`--quote "$VAR"` with `VAR` empty) gets a confident `raw-substring` rather than an error. The frozen case set has no empty-quote case, so the selftest cannot catch it. See Finding F.

### 2.6 Exit-code matrix (all measured, no inference)

| invocation | exit |
|---|---|
| `--selftest` | 0 |
| `--selftest --json` | 0 |
| `classify … ` (all three pairs, plus absent) | 0 |
| `classify` with missing raw blob | 2 |
| `classify` with missing text blob | 2 |
| `classify` with raw = a directory | 2 |
| `classify --quote ""` | 0 |
| no arguments at all | 2 |
| `classify` missing `--text` | 2 |
| `bogus-subcommand` | 2 |

Note the last three: the module's own code says `ap.error(...); return 64` (`scripts/quote_class.py:145-147`), but `argparse.error()` raises `SystemExit(2)` before the `return 64` is reachable, so **every** usage fault exits 2, never 64. The docstring advertises exit 2 for usage faults, so the observable behavior matches the docstring — but the `return 64` line is dead code, and 64 is indistinguishable from a missing-file exit if it ever became reachable. Cosmetic; recorded, not material.

---

## 3. Finding A — the C2 counter is **not revision-pinned**: it reads the tool's inputs from the worktree

`c63_quote_tool.py` extracts the *tool* from the revision correctly (`git show <rev>:scripts/quote_class.py`, `c63_quote_tool.py:66-74`) and then runs it **with `cwd=root`** (`c63_quote_tool.py:80-83`). The tool resolves its fixtures relative to `Path.cwd()` (`scripts/quote_class.py:24-25`: `LANE_ROOT = Path.cwd()`, `FIXTURES = Path("scripts/fixtures/quote-class")`) — so the **fixture blobs and the S432 blobs are read from the worktree of `--root`, not from the committed bytes at `--revision`**. Only the tool's *code* is revision-pinned; its *inputs* are not.

This is the exact round-50 discipline that the round-50 counter declares and that the round-63 C1 counter preserves, and the round-63 C2 counter drops. Compare `.ufo/waves/round-50/c50_quote_class.py:29` (`COMMITTED_BYTES_ONLY: no worktree open of lane artifacts.`) and `c50_quote_class.py:148-176` (every artifact via `git_show`). The round-63 **C1** counter does the same (`c63_calibration.py:70-76`, `git_show` for all five corpus files plus the two blobs plus the ledger) — I confirmed it stays green when the worktree copy of `S432.html` is deleted, i.e. C1 is genuinely committed-bytes-only:

```
$ rm -f "$D/.ufo/waves/round-61/sources/S432.html"   # clone worktree, uncommitted
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root "$D" --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

The C2 counter, on the same clone with the same deletion, goes **red** — proving it is reading the worktree:

```
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D" --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=failed met=false
exit=1
```

**Attack A1 — a green at a revision whose committed tree cannot run the tool at all.** Scratch repo `D=/fast/scratch/hyaku/kake-r63/ExecToolSelftest/nonself`, `git -C "$D" init -q`, top-level asserted to equal `$D` before the first commit. The commit contains **only** `scripts/quote_class.py`; the six tool-input paths exist **only as untracked worktree files**:

```
$ git -C "$D" ls-tree -r --name-only 2bedcc3477c84e508cbca5cb40add6ebd47cf77b
scripts/quote_class.py
$ git -C "$D" status --porcelain
?? .ufo/
?? scripts/fixtures/
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D" --revision 2bedcc3477c84e508cbca5cb40add6ebd47cf77b
revision=2bedcc3477c84e508cbca5cb40add6ebd47cf77b present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

The revision's tree has no fixtures and no blobs — the tool at that revision could never pass its own selftest from committed bytes — yet the counter prints `met=true`. Delete the untracked worktree files and the same revision goes red (`present=1 selftest=failed met=false`), confirming the green came from the worktree, not the revision.

**Attack A2 — green at a revision whose *committed* fixture bytes are red.** Scratch repo `revpinned`, commit `f88523978eb986d908371be6e51494b6d06d55d9`, whose committed `scripts/fixtures/quote-class/markup.txt` is **empty** (tampered). From the committed bytes alone the tool is red:

```
$ git -C "$D" archive "$REV" | tar -x -C "$CLEAN"
$ cd "$CLEAN" && python3 -B scripts/quote_class.py --selftest
case inline_raw_substring: derived=raw-substring expected=raw-substring pass
case markup_collapsed_only: derived=absent expected=collapsed-only FAIL
case absent_everywhere: derived=absent expected=absent pass
case s432_real: derived=collapsed-only expected=collapsed-only pass
selftest 3/4
exit=1
```

But the counter, run against that same revision with the *worktree* holding a good `markup.txt` (an uncommitted modification), prints green:

```
$ git -C "$D" status --porcelain
 M scripts/fixtures/quote-class/markup.txt
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D" --revision f88523978eb986d908371be6e51494b6d06d55d9
revision=f88523978eb986d908371be6e51494b6d06d55d9 present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

**Attack A3 — the measured revision itself is not self-certifying.** Same revision `05b0d7f4…`, clean clone; an **uncommitted** truncation of the worktree `markup.txt` flips the verdict with the committed bytes untouched:

```
$ : > "$D/scripts/fixtures/quote-class/markup.txt"
$ git -C "$D" status --porcelain
 M scripts/fixtures/quote-class/markup.txt
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D" --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=failed met=false
exit=1
$ git -C "$D" show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:scripts/fixtures/quote-class/markup.txt | head -c 90
The `X-Content-Type-Options` header marks the response.
```

**Impact.** The after-receipt `after-c2.txt` is *currently* truthful — I re-ran it and it reproduces exactly, and the six input paths are byte-identical between the measured revision and the worktree (§1). But the counter as written cannot distinguish "the tool runs at the measured revision" from "the tool runs against whatever bytes happen to sit in the worktree". The contract's own C2 predicate is about the tool **at the measured revision**; the counter does not measure that. This is the same *shape* of defect as the round-62 routed defect (a counter whose green depends on ambient bytes rather than committed bytes), one level up: round-62's `c62_calibration.py` trusted literal marker strings; round-63's `c63_quote_tool.py` trusts the worktree's copy of the fixture blobs. A cleaner counter would resolve the six input paths through `git show <rev>:<path>` (as C1 does) and run the tool with `cwd` pointed at a materialized tree, or would pass the blobs to the tool explicitly.

**Scope of the finding.** This is a *fidelity* defect in the C2 counter, not evidence that the current after-receipt is false. Nothing here makes `after-c2.txt` wrong today.

---

## 4. Finding B — a stub tool passes the C2 counter (the contract's stated kill rule)

The contract's kill rule: *"if the after receipt does not print `met=true`, or **a stub tool passes**, C2 is `unprovable`."* The contract further claims the counter's *"frozen-case-set check rejects a stub selftest missing the four frozen case ids."* That weaker claim is true — I confirmed a stub **missing** `s432_real` is rejected:

```
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D" --revision 850debd80ecf3f20d6a6944d1916b59eaeb84d5a
revision=850debd80ecf3f20d6a6944d1916b59eaeb84d5a present=1 selftest=3/3 frozen_cases=missing met=false
exit=1
```

But a stub that **includes all four frozen ids** and **hardcodes their expected values** — reading no blob, deriving nothing, containing no `classify` logic at all — passes:

```
$ cat stubfixture/scripts/quote_class.py
#!/usr/bin/env python3
"""STUB: no derivation whatsoever; prints the four frozen ids with expected values."""
import json, sys
CASES = [("inline_raw_substring","raw-substring"),("markup_collapsed_only","collapsed-only"),
         ("absent_everywhere","absent"),("s432_real","collapsed-only")]
if "--selftest" in sys.argv:
    print(json.dumps({"cases":[{"id":i,"derived":d,"expected":d,"passed":True} for i,d in CASES],
                      "total":4,"passed":4,"ok":True}, sort_keys=True))
    sys.exit(0)
sys.exit(64)

$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D" --revision e6a5896db1a6afe6ad3ff2053de12a607eaa0df8
revision=e6a5896db1a6afe6ad3ff2053de12a607eaa0df8 present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

I then built the stub at the **exact shape of the measured revision's relevant tree** — same six input paths, same frozen case ids — and it still passes:

```
$ git -C "$D" ls-tree -r --name-only f4d44798de9ce4c3e5a2451257d838e32e125151
.ufo/waves/round-61/sources/S432.html
.ufo/waves/round-63/quote-class/S432.txt
scripts/fixtures/quote-class/inline.raw.html
scripts/fixtures/quote-class/inline.txt
scripts/fixtures/quote-class/markup.raw.html
scripts/fixtures/quote-class/markup.txt
scripts/quote_class.py
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D" --revision f4d44798de9ce4c3e5a2451257d838e32e125151
revision=f4d44798de9ce4c3e5a2451257d838e32e125151 present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

**Why this happens.** The counter's frozen-case-set check (`c63_quote_tool.py:88-95`) requires only that each of the four ids appear with `passed is True` and `derived == expected`. Both `derived` and `expected` come from the *tool's own output*, so a tool that prints them equal is trivially self-certifying. The counter never verifies the tool's frozen sha256 — `grep -c sha256 .ufo/waves/round-63/c63_quote_tool.py` returns **0** — even though the contract freezes it (`431e75e8…`) and the file's own frozen sha is checked nowhere in the counter. It also never re-derives the class itself; C1 does that inline, but C2's contract is deliberately a *thin* "does the tool run" check, and thin is exactly where the stub lands.

**Consequence for the kill rule.** The kill rule is written in terms of *a stub tool passing*. A stub tool does pass the counter. On the contract's own terms that is a C2 `unprovable` trigger. The counter's defense as described in the contract (the frozen case-id set) only rejects stubs that *omit* an id — it does not reject a stub that *asserts* the ids with the right values, which is the stronger and more natural way to write a stub. Note the counter's own docstring is candid about the narrowness ("a stub tool that skips the frozen case ids is rejected by the case-set check") — the gap is that "skips" ≠ "fabricates".

**Scope of the finding.** The tool actually present at the measured revision is the frozen, real one (sha `431e75e8…`, verified in §1) and it genuinely derives its classes. So `after-c2.txt` is not false. The finding is that the counter does not *enforce* what the contract's kill rule takes it to enforce, so the counter as written cannot certify the tool's authenticity — a substituted tool at the measured revision would go green. Whether that lands C2 `unprovable` is the L1's call; I report the evidence and the exact reproduction, not the verdict.

---

## 5. Finding C — round-63 class semantics diverge from round-50 for raw-but-not-text spans

Round-50's class rule (`c50_quote_class.py:101-106`, and `corpus/QUALITY.md:1101-1106`) is:

```python
def classify(quote, raw, text):
    if quote not in text:  return "absent"
    if quote in raw:       return "raw-substring"
    return "collapsed-only"
```

Round-63's tool (`scripts/quote_class.py:34-39`) and the C1 counter's inlined copy (`c63_calibration.py:59-66`) are:

```python
def classify(quote, raw, text):
    if quote in raw:  return "raw-substring"
    if quote in text: return "collapsed-only"
    return "absent"
```

The two orders disagree on exactly one input class — a span present in the raw HTML but **not** in the flat text (e.g. an HTML attribute value or a tag name, which the extractor drops):

| span | round-50 `c50` | round-63 tool / C1 |
|---|---|---|
| in raw only (html attribute) | `absent` | **`raw-substring`** |
| in text only | `collapsed-only` | `collapsed-only` |
| in both | `raw-substring` | `raw-substring` |
| in neither | `absent` | `absent` |

Demonstrated on the real fixture (`markup.raw.html` contains `data-dfn-type="http-header"`; `markup.txt` does not):

```
$ python3 -B scripts/quote_class.py classify --quote 'data-dfn-type="http-header"' \
      --raw scripts/fixtures/quote-class/markup.raw.html --text scripts/fixtures/quote-class/markup.txt
derived=raw-substring
exit=0
```

Round-50's rule would call that span `absent`. The contract explicitly says the C1 class must be re-derived **"inline from those blobs as `collapsed-only` (never gating on `scripts/quote_class.py`)"** and that C1 re-derives "the round-50 semantics" — but the inlined `classify` in `c63_calibration.py` is the round-63 order, not round-50's. For the S432 span specifically the two agree (it is in text, not in raw → `collapsed-only`), so **the S432 verdict is unaffected** and `after-c1.txt` stands. The divergence is latent: it would bite any future span that occurs in raw but not in the flat rendering. The round-63 order is also the one `corpus/QUALITY.md:1102-1103` describes in prose ("a span that is a substring of the retained HTML is `raw-substring`"), so the round-63 tool arguably matches the *stated* rule better than round-50's implementation does — but the *implementation* named in the contract is round-50's, and the two now disagree. Worth an explicit ruling rather than a silent divergence.

---

## 6. Finding D — the tool's `--json` flag is documented on the wrong side of the subcommand

The module docstring (`scripts/quote_class.py:9`) advertises:

```
quote_class.py classify --quote "..." --raw <file> --text <file> [--json]
```

That form does **not** work — `--json` is registered on the top-level parser, not on the `classify` subparser (`scripts/quote_class.py:114`, `ap.add_argument("--json", …)` sits on `ap`, while `cl` gets only `--quote/--raw/--text`):

```
$ python3 -B scripts/quote_class.py classify --quote "quick brown fox" \
      --raw scripts/fixtures/quote-class/inline.raw.html --text scripts/fixtures/quote-class/inline.txt --json
usage: quote_class.py [-h] [--selftest] [--json] {classify} ...
quote_class.py: error: unrecognized arguments: --json
exit=2
```

The working spelling puts `--json` **before** the subcommand:

```
$ python3 -B scripts/quote_class.py --json classify --quote "quick brown fox" \
      --raw scripts/fixtures/quote-class/inline.raw.html --text scripts/fixtures/quote-class/inline.txt
{"derived": "raw-substring"}
exit=0
```

Cosmetic-to-operability: a caller following the docstring gets exit 2 and a usage error. No receipt depends on this, and the C2 counter invokes `--selftest --json` (top-level, correct), so no claim is affected.

---

## 7. Finding E — `--selftest` is cwd-bound by design; the freeze note documents it, the counter depends on it

Running the tool from any directory other than the lane root makes every case `unevaluable`:

```
$ cd /tmp && python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py --selftest
case inline_raw_substring: derived=unevaluable expected=raw-substring FAIL
case markup_collapsed_only: derived=unevaluable expected=collapsed-only FAIL
case absent_everywhere: derived=unevaluable expected=absent FAIL
case s432_real: derived=unevaluable expected=collapsed-only FAIL
selftest 0/4
exit=1
```

This is the round-63 freeze-note's stated change (`LANE_ROOT = Path.cwd()` at `scripts/quote_class.py:24`, replacing the round-50-era `Path(__file__).resolve().parent.parent` — I confirmed the pre-freeze blob `6d8c52a6:scripts/quote_class.py` carries the `__file__`-relative form and sha `40655dd8…`, matching the contract's freeze note exactly). It is documented and deliberate, and the C2 counter compensates by running the extracted tool with `cwd=root` (`c63_quote_tool.py:80-83`). **But that compensation is precisely what produces Finding A**: the counter made the tool cwd-sensitive in order to make it *see* the fixtures, and the fixtures it then sees are the worktree's, not the revision's. The two changes are causally linked. The fix for A is not to re-bind the tool to `__file__` (that was frozen deliberately) but to have the counter materialize the revision's tree and point `cwd` at it.

---

## 8. Finding F — the empty-quote case is a silent wrong answer

Restated from §2.5 with the mechanism: `classify("", raw, text)` returns `raw-substring` because `"" in raw` is always true (`scripts/quote_class.py:35`). Exit 0, no diagnostic. The class vocabulary has exactly three values (`raw-substring` / `collapsed-only` / `absent`) and an empty span is genuinely `absent` — it names nothing. No frozen case covers it, so the selftest cannot catch it. Not contract-affecting today (the four frozen quotes are all non-empty), but it is a real input the tool accepts and misclassifies, and it is the kind of input that appears when a shell variable is unset.

---

## 9. What I did **not** do

- No commits, no push, no `git`/`jj` mutation in the fleet repo or any sibling repo. The fleet repo's `git status --porcelain` is unchanged apart from untracked wave files that existed before I started (`.ufo/waves/round-63/w1.ready`, `.ufo/waves/round-63/w1.ready.dispatched`, `.ufo/waves/round-63/w1/`).
- No edits to `scripts/`, `templates/`, `.ufo/state`, the lane corpus, `SOURCES.md`, `MANIFEST.json`, `considerthese/`, the frozen counters, the frozen tool, the contract, or any receipt. The only file I wrote is this report.
- No subagent dispatch. No pacman, no package installs (nothing needed installing; `python3` and `git` were already present).
- All fixture repos were created under `/fast/scratch/hyaku/kake-r63/ExecToolSelftest/`, each with `git -C "$D" init -q` and an asserted `git -C "$D" rev-parse --show-toplevel` equal to `$D` before its first commit, each with a throwaway identity set **inside the fixture repo only** (`user.email p@l`, `user.name p`).
- Scratch deleted on completion: `rm -rf /fast/scratch/hyaku/kake-r63/ExecToolSelftest` — `scratch_cleanup=clean`.

---

## 10. Summary table

| # | Finding | Severity for the claims | Evidence |
|---|---|---|---|
| A | C2 counter is not revision-pinned: tool **inputs** come from the worktree, so a green does not certify the revision's committed bytes | **Material** to C2's counter fidelity; after-receipt is truthful today (all six input paths byte-identical) | §3, attacks A1/A2/A3 |
| B | A stub tool that hardcodes the four frozen ids **passes** the C2 counter; the counter checks no frozen sha256 (`grep -c sha256` → 0) | **Material** — touches the contract's stated kill rule ("a stub tool passes") | §4 |
| C | Round-63 class order diverges from round-50 for raw-but-not-text spans (`raw-substring` vs `absent`); C1's inlined copy follows round-63, not round-50 | **Latent** — S432 verdict unaffected (`collapsed-only` under both) | §5 |
| D | `--json` documented after the subcommand but only accepted before it | Cosmetic / operability; no claim affected | §6 |
| E | cwd-bound selftest (deliberate, documented) is the mechanism behind A | Context for A | §7 |
| F | Empty quote classifies as `raw-substring` instead of `absent`, exit 0 | Minor; no frozen case affected | §2.5, §8 |

**Claims status after this seat's work (my measurement only; the L1 adjudicates):**
- **C2** — the item's commands all reproduce exactly; `after-c2.txt` is truthful as measured. But the counter has two open fidelity gaps (A, B), and B touches the contract's kill rule by its own wording.
- **C1** — untouched by this seat's findings except for the latent class-order divergence (C), which does not change the S432 verdict or `after-c1.txt`.

**Recommended checks for the main agent (I did not run them):** re-run `python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` against a `git archive`-materialized copy of the measured revision with `cwd` inside it, to confirm the C2 green is revision-pinned rather than worktree-pinned; and decide whether Finding B trips the C2 kill rule as written.

---

### Files changed

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/ExecToolSelftest.md` (this report — the only file written)

### Commands run (for replay)

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 -B scripts/quote_class.py --selftest
python3 -B scripts/quote_class.py --selftest --json
python3 -B scripts/quote_class.py classify --quote "quick brown fox" --raw scripts/fixtures/quote-class/inline.raw.html --text scripts/fixtures/quote-class/inline.txt
python3 -B scripts/quote_class.py classify --quote 'The `X-Content-Type-Options` header marks the response' --raw scripts/fixtures/quote-class/markup.raw.html --text scripts/fixtures/quote-class/markup.txt
python3 -B scripts/quote_class.py classify --quote 'The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.' --raw .ufo/waves/round-61/sources/S432.html --text .ufo/waves/round-63/quote-class/S432.txt
python3 -B scripts/quote_class.py classify --quote "this span occurs in no retained blob at all" --raw scripts/fixtures/quote-class/inline.raw.html --text scripts/fixtures/quote-class/inline.txt
python3 -B scripts/quote_class.py classify --quote "quick brown fox" --raw scripts/fixtures/quote-class/NOPE.raw.html --text scripts/fixtures/quote-class/inline.txt
python3 -B scripts/quote_class.py classify --quote "quick brown fox" --raw scripts/fixtures/quote-class/inline.raw.html --text scripts/fixtures/quote-class/NOPE.txt
python3 -B scripts/quote_class.py classify --quote "" --raw scripts/fixtures/quote-class/inline.raw.html --text scripts/fixtures/quote-class/inline.txt
python3 -B .ufo/waves/round-63/quote-class/extract_text.py --raw ./S432.html --out ./S432.repro.txt
python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
```

Scratch (deleted): `/fast/scratch/hyaku/kake-r63/ExecToolSelftest/{clone,nonself,revpinned,revpinned_clean,revpinned_measured,stubfixture,stubfixture2,stub_at_measured}`.
