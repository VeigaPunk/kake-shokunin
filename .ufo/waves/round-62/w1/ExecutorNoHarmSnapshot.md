# ExecutorNoHarmSnapshot — round-62 C1 no-harm snapshot

**Seat:** `ExecutorNoHarmSnapshot` (advisory, leaf)
**Wave:** round-62, w1 · **Claim:** C1 calibration (score 2)
**Base:** `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13` (lane `HEAD` = base)
**Frozen counter:** `.ufo/waves/round-62/c62_calibration.py`
**Item:** *Create a read-only checksum inventory of the claimed files at base and explain a safe post-run comparison; no lane changes.*

**Status: no lane changes.** The claim, the counter, the criteria and the score
were not touched. This seat wrote exactly one file: this report. Every command
below was a read against committed blobs; the only writes were inside the seat's
own scratch tree, which is deleted before yield.

---

## 1. What the frozen counter actually reads

`c62_calibration.py` resolves every state from **committed Git blobs only**
(`git show <rev>:<path>`), never the worktree. Its `PATHS` map names five
files; the counter reads all five and nothing else.

| key | path |
|---|---|
| `spot` | `corpus/lessons/round-61-verifier-spotcheck.md` |
| `knowledge` | `corpus/knowledge/response-header-expectations.md` |
| `quality` | `corpus/QUALITY.md` |
| `lesson` | `corpus/lessons/round-62.md` |
| `sources` | `corpus/SOURCES.md` |

Frozen constants (read out of the file, not paraphrased):

- `QUOTE` (120 chars) = `response header can be used to require checking of a response’s Content-Type header against the destination of a request`
  — contains exactly one non-ASCII codepoint, `’` U+2019.
- `CRITERION` (25 chars) = `substantive located quote` (pure ASCII).
- `correction` = `QUOTE in knowledge AND "S432 §3.6" in knowledge AND "Round-62 correction" in knowledge`
  — `§` is U+00A7.
- `criterion` = `"substantive located quote" in quality AND "round-61-verifier-spotcheck.md" in quality`
- `lesson_gate` = `"## Gate" in lesson AND "S432" in lesson AND "Agree" in lesson AND "Reject" in lesson`
- `source_row` = `"| S432 |" in sources`
- `disagreements` = count of lines in `spot` containing **both** `S432` and `Disagree`
- `resolved` = `correction==1 AND criterion==1 AND lesson_gate==1 AND source_row==1`
- `unresolved` = `disagreements if not resolved else 0`
- `met` = `unresolved == 0 AND resolved`; exit `0` if `met` else `1`.

**Base control reproduced exactly as the wave prompt records it.**

```
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

Matches the recorded base-control (`unresolved=1 quote_correction=0 criterion=0
lesson_gate=0 source_row=1 met=false exit 1`) field for field. The frozen
counter's bytes also match the frozen digest:

```
$ sha256sum .ufo/waves/round-62/c62_calibration.py
ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  .ufo/waves/round-62/c62_calibration.py
```

The counter runs identically at the lane's jj working-copy commit
`1108744228b567ee1f91841d92a0e0b2f564727e` (an empty descendant of the base;
its tree diff against the base is empty), printing the same `met=false` line.

---

## 2. Checksum inventory at base

All digests are `sha256` over the **committed blob bytes** at
`c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`, obtained with
`git -C <lane> show <base>:<path> | sha256sum`. The blob OID is git's own
`sha1` object id.

| path | blob OID | sha256 of blob bytes |
|---|---|---|
| `corpus/lessons/round-61-verifier-spotcheck.md` | `0c6370550b66e1067a96e6e8a2517d60985597ee` | `b4faa46bb618399b02d8dc52e14a7f785bb87c17697737f5a92c92621203d013` |
| `corpus/knowledge/response-header-expectations.md` | `4ff91e4ae3409cc56ea7e808475211d86735845d` | `3f469deef0b14f596683c2d9fdd753687cb3c5c4a7c59b04cf5ba7dbbea7e1dd` |
| `corpus/QUALITY.md` | `3e269cf2f3ff2aa98016dd05428c538c1f48135c` | `c37bad48518210951771760924e5af6c5b0ea8fd06c19a3d2398d03757a78820` |
| `corpus/SOURCES.md` | `3993185e5eb13ed51cd32ffd21b20c3a2815a261` | `63af1594e2f8d0b499fbf2673424bf818cf93dd380232a8c8d546eef00f75ae2` |
| `corpus/lessons/round-62.md` | **absent at base** | **absent at base** |
| `.ufo/waves/round-61/sources/S432.html` | `51b848dafc418e7e3f4bd9371ae2e3b7ea64beb3` | `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b` |
| `.ufo/waves/round-62/c62_calibration.py` | untracked at base (wave dir is `??`) | `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d` (worktree bytes) |
| `.ufo/waves/round-62/contract.md` | untracked at base | `0922ceff49442b0b4ca1b75d98f5c9c7632b987be4f07b0a765a8a1a0c4b6e18` (worktree bytes) |

### Two inventory facts the implementer needs

**(a) `corpus/lessons/round-62.md` does not exist at base.** It must be
**created** (not appended to). The base blob is absent; the counter's
`blob()` returns `""` for it, so `lesson_gate` is `0` until the file exists
with a `## Gate` section naming `S432`, `Agree` and `Reject`.

**(b) The worktree copies of the five claimed files are byte-identical to
their base blobs.** `git status --porcelain` in the lane shows only the
pre-existing untracked wave directory:

```
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain
?? .ufo/waves/round-62/
```

so the worktree sha256 of each claimed file equals its base blob sha256 in
the table above. A post-run comparison may therefore read either the worktree
or the committed blob for the *current* state and get the same bytes — but the
**base** side must come from `git show <base>:<path>`, never from the
worktree, because the worktree will have moved by then.

### Grounding of the frozen `QUOTE` in the retained body

The `QUOTE` string is **not** a literal substring of the raw retained HTML —
inline `<a>`/`<code>` markup splits it. It becomes literal once the markup is
stripped from the retained body's §3.6 body lines 6151–6154:

```
$ git -C <lane> show <base>:.ufo/waves/round-61/sources/S432.html | sed -n '6151,6154p'
`<dfn class="dfn-paneled" data-dfn-type="http-header" data-export id="http-x-content-type-options"><code>X-Content-Type-Options</code></dfn>`
response <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑤">header</a> can be used to require checking of a <a data-link-type="dfn" href="#concept-response" id="ref-for-concept-response④①">response</a>’s
`<code>Content-Type</code>` <a data-link-type="dfn" href="#concept-header" id="ref-for-concept-header④⑥">header</a> against the <a data-link-type="dfn" href="#concept-request-destination" id="ref-for-concept-request-destination①⓪">destination</a> of a
<a data-link-type="dfn" href="#concept-request" id="ref-for-concept-request①⓪⑦">request</a>.
```

De-marked (tags removed, backticks removed, whitespace collapsed):

> `X-Content-Type-Options response header can be used to require checking of a response’s Content-Type header against the destination of a request.`

which **contains** the frozen `QUOTE` verbatim (programmatically checked:
`QUOTE in demarked == True`; `QUOTE in raw_html == False`). The retained body's
digest reconciles with its own round-61 receipt:

```
receipt S432 sha256 : 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  (status 200, bytes 1854393, fetchedAt 2026-10-27T09:14:55Z)
committed S432.html   : 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b
```

and the same digest is the one the knowledge entry already cites at its
`fetches:` line (`S432 63b0a018…bad911b`).

**Implementation note for whoever lands the correction.** Because `QUOTE` is
de-marked rather than raw, the correction must reproduce the de-marked
sentence — including the U+2019 `’` in `response’s` — and must contain the
literal strings `S432 §3.6` and `Round-62 correction` (note: `§` is U+00A7 and
the phrase is hyphenated `Round-62`, not `Round 62`). A copy of the raw HTML
markup, or a typographic straight quote, will not satisfy the frozen
predicate. The existing generic lead-in that the correction must supersede is
at `corpus/knowledge/response-header-expectations.md:79`:
`> "Web developers and conformance checkers must use the following"`.

---

## 3. The safe post-run comparison

### 3.1 Why a checksum inventory alone is not enough

The counter's `unresolved` term is `disagreements if not resolved else 0`.
Once `resolved` is true, the `Disagree` row's presence stops mattering to the
verdict — and if the row is **deleted or edited**, `disagreements` falls to
`0` while `resolved` still becomes true. So a counter-only check can be
satisfied by *removing* the very record the contract says to keep. Measured in
the scratch fixture (§4, cases S3/S4): the counter prints `met=true` and
exits `0` with the S432 verifier row **deleted** or with its `Disagree`
verdict **rewritten to `Agree`**.

The contract requires the opposite: *"The existing S432 row is kept; do not
mark it rejected."* That requirement is not expressible in the frozen
counter, so it needs a separate check. That is what this seat's comparison
adds.

### 3.2 The comparison procedure

**Principles.** (i) Every read is `git show <rev>:<path>` — committed bytes
only, worktree never used for state. (ii) The base side is always pinned to
the base revision; the after side is the *measured committed revision* the
L1 declares. (iii) The append-only judgement is delegated to the lane's own
committed tool `scripts/append_guard.py` — this seat does **not** define a
second append rule. (iv) The lane's Git/jj state is never mutated: no
checkout, reset, clean, stash, add, commit, or jj write.

**The four checks.**

- **N1 — base lines preserved.** Every base line of every claimed file must
  still occur, byte-for-byte and **in order**, in the after-state. This is the
  round-20 ruling (`corpus/QUALITY.md` §"Post-review append-only ruling —
  round 20"): preserve every prior line byte-identically; use pure new-line
  additions or end-of-file correction blocks citing the old line. A file
  absent at base (here `corpus/lessons/round-62.md`) is a new file and is not
  subject to N1.
- **N2 — the S432 verifier row survives.** The base `| S432 / Fetch |` line
  (carrying its `Disagree` verdict) must be byte-identical at the measured
  revision. This is the contract's "the existing S432 row is kept" clause,
  which the frozen counter does not test.
- **N3 — the S432 registry row survives.** The base `| S432 |` line in
  `corpus/SOURCES.md` must be byte-identical.
- **N4/N5 — the frozen counter is unchanged.** The counter bytes at the
  measured revision must hash to
  `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`, and its
  `QUOTE` / `CRITERION` / `PATHS` constants must still be present verbatim
  (defence in depth against an edit-then-re-pin).

**The commands.** The comparator is a read-only script; the L1 (or the
post-integration reviewer) runs it against the lane and the measured revision:

```bash
LANE=/home/vgpnk/Projects/shokunin/kake-shokunin
BASE=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
REV=<the measured committed revision declared by the L1>

# 1. the frozen counter, at the measured revision (the only C1 score)
python3 -B "$LANE/.ufo/waves/round-62/c62_calibration.py" --root "$LANE" --revision "$REV"
echo "counter exit=$?"

# 2. the no-harm comparison (read-only; writes nothing)
python3 -B compare_claimed.py --root "$LANE" --base "$BASE" --revision "$REV"
echo "comparator exit=$?"
```

Exit `0` = every no-harm check passed; `1` = a check failed; `2` =
could-not-evaluate (root not a repo, revision unreadable).

The comparator internally calls the lane's own append-only guard with the
claimed files in scope:

```
python3 -B $LANE/scripts/append_guard.py --root $LANE --base $BASE --revision $REV \
  --scope corpus/lessons/round-61-verifier-spotcheck.md \
  --scope corpus/knowledge/response-header-expectations.md \
  --scope corpus/QUALITY.md \
  --scope corpus/lessons/round-62.md \
  --scope corpus/SOURCES.md
```

**Why `append_guard.py` and not a private rule.** Its rule is already the
lane's: base lines must be an **ordered subsequence** of revision lines, and
any non-EOF insertion must open with a visible `[rNN-correction YYYY-MM-DD]`
tag that is not inside an HTML comment or a backtick code span. A mid-file
correction that carries the tag is therefore **allowed** by the lane's own
rule — this seat's N1 likewise accepts an in-order insertion, and does not
impose a stricter "append at EOF only" rule of its own. What N1 adds beyond
`append_guard` is the *claim-specific* N2/N3 row checks.

**One safe, cheap alternative** if the L1 prefers not to carry a second
script: the same N1/N2/N3 checks are expressible directly from the lane's
own plumbing, e.g.

```bash
git -C "$LANE" diff --unified=0 "$BASE" "$REV" -- corpus/lessons/round-61-verifier-spotcheck.md
git -C "$LANE" diff --unified=0 "$BASE" "$REV" -- corpus/SOURCES.md
```

A diff on those two files must be **empty** (no line added, removed or
changed) — that alone enforces N2 and N3. The knowledge, QUALITY and lesson
files must show additions only.

### 3.3 What "safe" means concretely

- **No lane mutation.** The comparator runs `git show` / `git rev-parse` /
  `git ls-tree` reads and nothing else; it never runs `checkout`, `reset`,
  `clean`, `stash`, `add`, `commit`, `merge`, or any `jj` write. It was run
  against the live lane and the lane was re-inspected afterwards: `git status`
  still shows only `?? .ufo/waves/round-62/`, `HEAD` is still the base, and
  the jj working-copy commit is still an empty descendant of the base.
- **No frozen-predicate change.** The counter's bytes are verified, not
  edited. The claim text, the criteria and the score are untouched.
- **No write on lane files.** The only lane write by this seat is this report.
  The comparator, the scenario harness and the fixture clone lived entirely
  under `/fast/scratch/hyaku/kake-r62/ExecutorNoHarmSnapshot/` and that
  directory was deleted before yield.
- **Fixture identity stayed inside the fixture.** The scratch clone commits
  with `-c user.name=round62-no-harm-fixture -c user.email=fixture@example.invalid`
  passed per-command, so no global git config was written and no identity
  leaked outside the fixture. Every fixture git operation used an explicit
  `git -C <fixture-dir>`.
- **No pacman transaction.** No package was installed; the toolchain used was
  the host's existing `git`, `python3` (stdlib only) and `jj`. Nothing was
  installed, so no install/version/channel/reason record is owed.

---

## 4. Evidence: the comparison was exercised, not just designed

Seven after-states were built in an isolated scratch clone of the lane
(`git clone --no-hardlinks` of the lane into the seat scratch; each case
reset to a committed base+wave state; each case committed its own revision).
The harness is `scenarios.sh`; the comparator is `compare_claimed.py`.

| case | after-state | frozen counter | comparator | expected |
|---|---|---|---|---|
| **S0** | do-nothing (base control) | `met=false`, exit **1** | PASS, exit 0 | ✔ |
| **S1** | valid append-only after (knowledge correction + QUALITY criterion + new `round-62.md`) | `met=true`, exit **0** | PASS, exit 0 | ✔ |
| **S2** | knowledge base byte rewritten in place (`one response` → `ONE response`) | `met=true`, exit **0** | **FAIL**, exit 1 | ✔ |
| **S3** | S432 verifier row **deleted** from the spot-check | `met=true`, exit **0** | **FAIL**, exit 1 | ✔ |
| **S4** | S432 verifier row edited `Disagree` → `Agree` | `met=true`, exit **0** | **FAIL**, exit 1 | ✔ |
| **S5** | `\| S432 \|` registry row deleted from `SOURCES.md` | `met=false`, exit **1** | **FAIL**, exit 1 | ✔ |
| **S6** | frozen counter bytes changed | `met=true`, exit **0** | **FAIL**, exit 1 | ✔ |

All seven behaved exactly as expected (`CASE S0 … AS EXPECTED` … `CASE S6 … AS EXPECTED`).

**The load-bearing result is S3/S4.** The frozen counter prints
`disagreements=0 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1
source_row=1 met=true` and exits `0` in both cases — i.e. the counter is
**satisfied by deleting or flipping the S432 `Disagree` row**, which the
contract forbids ("The existing S432 row is kept; do not mark it rejected").
The comparator catches both:

```
FAIL: N1 corpus/lessons/round-61-verifier-spotcheck.md: base line not preserved: b'| S432 / Fetch | Admit | https://fetch.spec.whatwg.org/, \xc2\xa73.6; retained body `.ufo/waves/round-61/sources/S432.html` | Disagree | \xe2\x80\x9cWeb developers and conformance checkers must use the following\xe2\x80\x9d is only a generic lead-in, not substantive evidence for a response-header expectation. Lesson itself identifies it as a generic lead-in. |'
FAIL: N2 spot: base S432 verifier row was changed or removed
FAIL: append_guard: findings (exit 1)
```

S6 shows the counter's own bytes are a required part of the comparison:
`FAIL: N4 .ufo/waves/round-62/c62_calibration.py: frozen bytes changed
(sha256=5afc407f…, committed@…)`. Note that in S6 the counter still printed
`met=true` — a drifted counter can still produce a green verdict.

### Comparison run against the live lane (base vs base)

```
$ python3 -B compare_claimed.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --base c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
…
corpus/lessons/round-61-verifier-spotcheck.md: PASS
corpus/knowledge/response-header-expectations.md: PASS
corpus/QUALITY.md: PASS
corpus/lessons/round-62.md: absent at base (new file) -> not applicable
corpus/SOURCES.md: PASS
spot S432 verifier row: PASS (byte-identical)
sources | S432 | row: PASS (byte-identical)
.ufo/waves/round-62/c62_calibration.py: PASS sha256=ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d (worktree)
frozen counter constants: PASS (QUOTE, CRITERION, PATHS)
files=4 findings=0
append_guard: PASS (no findings)
no-harm checks: PASSED
exit=0
```

`files=4` because `corpus/lessons/round-62.md` is absent at the base revision
and `append_guard` only scopes regular blobs that exist at base — consistent
with inventory fact (a) above.

---

## 5. Findings and recommendations for the L1

1. **The frozen counter does not enforce "the existing S432 row is kept".**
   Cases S3 and S4 show a green verdict with the row deleted or its verdict
   flipped to `Agree`. The post-run comparison must therefore include N2 (and
   N3 for the `SOURCES.md` row) — a counter-only verification is not
   sufficient evidence of no harm. **No change to the frozen counter is
   proposed or made**; the predicate is frozen and this seat does not touch it.
2. **`corpus/lessons/round-62.md` must be created, not appended.** It is
   absent at base; the counter requires a `## Gate` section naming `S432`,
   `Agree` and `Reject`.
3. **The correction's quote must be the de-marked sentence** with U+2019
   `’` in `response’s`, plus the literal `S432 §3.6` and `Round-62
   correction`. The raw retained HTML does **not** contain the frozen `QUOTE`
   as a literal substring (§2), so a verbatim HTML copy would fail the
   predicate.
4. **A mid-file correction in the knowledge entry must carry the lane's
   visible tag** `[r62-correction 2026-10-27]` — the lane's
   `append_guard.py` accepts an in-order insertion only when the run opens
   with that tag (visible: not inside an HTML comment or a backtick code
   span). An end-of-file append needs no tag.
5. **The `Disagree` row's own prose is the evidence the correction answers.**
   `corpus/lessons/round-61-verifier-spotcheck.md:33` is the row; the generic
   lead-in it names is quoted in the knowledge entry at line 79. The
   correction should point at the §3.6 sentence and state why it grounds the
   entry where the lead-in did not.

---

## 6. Scope, state and honesty record

**Files changed by this seat:** exactly one —
`.ufo/waves/round-62/w1/ExecutorNoHarmSnapshot.md` (this report).

**Not touched:** the claim text, `.ufo/waves/round-62/c62_calibration.py`,
`.ufo/waves/round-62/contract.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`,
`corpus/knowledge/response-header-expectations.md`,
`corpus/lessons/round-61-verifier-spotcheck.md`, the lane's Git index and
`HEAD`, the lane's jj working copy, the fleet repo, sibling repos, source
trees and operator config.

**Verification actually performed (all read-only or scratch-local):**
the base control was re-run and matches the recorded one field for field;
the frozen counter's sha256 was confirmed; the base blob digests of all five
claimed files plus the retained S432 body and the wave-local files were
computed; the `QUOTE`'s presence in the de-marked retained body was checked
programmatically; the retained body's digest was reconciled against its own
round-61 receipt; seven after-states were built and measured in a scratch
clone; the comparator was run against the live lane; and the lane's Git and jj
state were re-inspected afterwards and found unchanged.

**Scratch:** `/fast/scratch/hyaku/kake-r62/ExecutorNoHarmSnapshot/` — created
for this seat, used only for the clone, the comparator, the harness and the
captured outputs, and **deleted before yield**. Nothing was written under
`/tmp`.

**No installs, no pacman transaction, no network fetch.** The round's source
opening (https://fetch.spec.whatwg.org/, HTTP 200, 2026-10-27) was performed
by the lane before this wave; this seat verified the **retained** committed
body against its receipt and did not re-fetch. Re-fetching would have produced
a body whose digest could not be reconciled with the committed receipt, which
is exactly the re-pinning failure the lane's own criteria warn against.

**Tools used:** `git` (host version, read-only plumbing), `python3` (host
version, stdlib only — no third-party packages), `jj` (host version, read-only
`log`/`op log`). No package was installed, so there is no
tool/version/channel/reason entry to record.
