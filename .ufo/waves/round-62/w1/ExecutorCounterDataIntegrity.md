# ExecutorCounterDataIntegrity — round 62

Scope: verify that the base revision and the source/spot-check blobs used by the frozen
counter are read from Git **objects**, not from a changed worktree. No claim, counter,
criterion, score, or lane corpus file was modified. This seat wrote only this report.
No pacman transaction, no install, no `PATH` write, no lane Git/jj/index mutation.

## 1. Verdict

**PASS.** The frozen counter resolves every measured input through
`git -C <root> show <rev>:<path>` — a pure object-database read. Worktree state is
provably irrelevant: a fixture with every one of the five measured paths overwritten by
junk still produced the byte-identical base measurement, and a repo containing the file
only as an untracked worktree file was refused (`exit 2`) rather than measured.

## 2. Base revision identity

```
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13^{commit}
c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
$ git -C … rev-parse master origin/master
c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
$ git -C … ls-remote origin refs/heads/master
c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13	refs/heads/master
$ git -C … branch -a --contains c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
* (no branch)
  master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
$ git -C … log -1 --format='%H %ci %s' c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 2026-10-27 08:50:17 -0300 round-61 verifier spot-check (integrator, hyaku): non-author admit/reject
```

Base is a well-formed `commit` object, is the current `HEAD`, `master`, `origin/master`,
and equals the live remote ref `refs/heads/master` (remote verified, not merely the
local tracking ref). `git fsck --no-progress --no-dangling` → exit 0, no output.
`git replace -l` → empty; `.git/info/grafts` absent; `.git/info/attributes` absent.
Commit is unsigned (`%G?` = `N`) — no signature to verify, so object-id + remote-ref
equality is the binding evidence.

## 3. Frozen counter identity

```
$ sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/c62_calibration.py
ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  .ufo/waves/round-62/c62_calibration.py
```

Matches the mission's frozen hash exactly (re-checked at the end of the seat's work;
unchanged). Note: `.ufo/waves/round-62/` is **untracked** in the lane
(`git status --porcelain` → `?? .ufo/waves/round-62/`), so the SHA-256 above is the only
pin on the counter — nothing in the base commit attests it.

Counter dataflow (`.ufo/waves/round-62/c62_calibration.py:23-28`):

```python
def blob(root: str, rev: str, path: str) -> str:
    p = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], …)
```

`git show <rev>:<path>` reads the object DB and the tree at `<rev>`; it never consults
the index or the worktree. There is no `open()`/`Path.read_text()` anywhere in the
counter.

## 4. Blob vs worktree hashes (base revision)

```
$ for p in corpus/lessons/round-61-verifier-spotcheck.md \
           corpus/knowledge/response-header-expectations.md corpus/QUALITY.md \
           corpus/SOURCES.md .ufo/waves/round-61/sources/S432.html; do
    printf '%s %s %s\n' "$(git rev-parse c341a7a…:$p)" "$(git hash-object -- $p)" "$p"; done
0c6370550b66e1067a96e6e8a2517d60985597ee 0c6370550b66e1067a96e6e8a2517d60985597ee corpus/lessons/round-61-verifier-spotcheck.md
4ff91e4ae3409cc56ea7e808475211d86735845d 4ff91e4ae3409cc56ea7e808475211d86735845d corpus/knowledge/response-header-expectations.md
3e269cf2f3ff2aa98016dd05428c538c1f48135c 3e269cf2f3ff2aa98016dd05428c538c1f48135c corpus/QUALITY.md
3993185e5eb13ed51cd32ffd21b20c3a2815a261 3993185e5eb13ed51cd32ffd21b20c3a2815a261 corpus/SOURCES.md
51b848dafc418e7e3f4bd9371ae2e3b7ea64beb3 51b848dafc418e7e3f4bd9371ae2e3b7ea64beb3 .ufo/waves/round-61/sources/S432.html
```

Base blob OID == worktree blob OID for all five measured paths and for the retained
source body: the worktree is currently identical to the base commit for these files.
`git status --porcelain --untracked-files=no` → empty (no tracked-file drift at
measurement time). `git diff --stat c341a7a… -- corpus/` → empty.

`corpus/lessons/round-62.md` is **absent at base** in both the tree and the worktree:

```
$ git -C … cat-file -e c341a7a…:corpus/lessons/round-62.md
fatal: path 'corpus/lessons/round-62.md' does not exist in 'c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13'
```

The counter's `blob()` therefore returns `""` for that path and `lesson_gate` evaluates
to 0 — the expected base-control value, not a measurement defect.

## 5. Worktree-independence experiments

All fixtures were private clones under `/fast/scratch/hyaku/kake-r62/ExecutorCounterDataIntegrity/`,
each verified with `git rev-parse --show-toplevel` before any commit. Identity was passed
per-command (`git -c user.name=fixture -c user.email=fixture@local …`); the fixture
`.git/config` contains no `user.*` entry and no global identity was written.

### 5a. Junk worktree, base revision → unchanged measurement

Fixture clone checked out at base, then **all five measured worktree files overwritten
with `JUNK`** (worktree now `MM`/`M` against the index):

```
$ python3 -B fixture/c62_calibration.py --root <fixture> --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

Identical to the lane's own base-control output. The counter cannot see the junk.

### 5b. Worktree file with no committed object → refused, not measured

A second, empty repo whose worktree contained `corpus/lessons/round-61-verifier-spotcheck.md`
containing a `| S432 | … | Disagree |` row, but with nothing committed:

```
$ python3 -B …/c62_calibration.py --root <empty-repo> --revision c341a7a…
could-not-evaluate: missing verifier spot-check
exit=2
```

Fail-closed. A worktree file can never satisfy a measurement; the counter reads only
objects.

### 5c. Bogus revision → fail-closed

```
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision 0000000000000000000000000000000000000000
could-not-evaluate: missing verifier spot-check
exit=2
```

### 5d. A committed change is picked up only at its own revision

In the fixture, a candidate "fix" commit was created (knowledge file gains a
`Round-62 correction` block with the frozen quote and `S432 §3.6`; `corpus/QUALITY.md`
gains `substantive located quote` + the spot-check filename; new `corpus/lessons/round-62.md`
with a `## Gate` section) → fix commit `a533803a546651d693616230254da2f5ceebb58e`:

```
$ python3 -B … --root <fixture> --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13   # base, worktree still at fix
revision=c341a7a… disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false   exit=1
$ python3 -B … --root <fixture> --revision a533803a546651d693616230254da2f5ceebb58e   # the fix commit
revision=a533803a… disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true   exit=0
```

Two integrity properties confirmed at once:
* the measurement follows the **revision**, not the checkout (base still fails while the
  worktree holds the fix);
* `disagreements` stays `1` — the S432 `Disagree` row was left in place, exactly as the
  mission requires — while `unresolved` drops to `0` because the counter derives
  `unresolved` from `resolved` (all four artifacts landed), not from the row count. The
  row may therefore be kept, not rejected.

## 6. Retained source body — blob ↔ worktree ↔ fetch receipt

```
$ git -C … ls-tree --name-only c341a7a…:.ufo/waves/round-61/sources
S430.html
S431.html
S432.html
S433.html
receipts.json
$ git -C … cat-file --batch-check='%(objectname) %(objecttype) %(objectsize) %(objectsize:disk)' <<EOF
c341a7a…:.ufo/waves/round-61/sources/S432.html
51b848dafc418e7e3f4bd9371ae2e3b7ea64beb3 blob 1854393 244922
EOF
$ sha256sum .ufo/waves/round-61/sources/S432.html
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b
$ git -C … show c341a7a…:.ufo/waves/round-61/sources/receipts.json   # S432 entry
{"id": "S432", "url": "https://fetch.spec.whatwg.org/", "effectiveUrl": "https://fetch.spec.whatwg.org/",
 "status": 200, "sha256": "63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b",
 "bytes": 1854393, "fetchedAt": "2026-10-27T09:14:55Z", "userAgent": "round61"}
```

The retained body at base is byte-identical to the worktree copy
(`git show c341a7a…:S432.html | diff - .ufo/waves/round-61/sources/S432.html` → no
output), its SHA-256 equals the round-61 fetch receipt's SHA-256, and its byte length
(1 854 393) equals the receipt's `bytes`. The source the correction will quote is the
same artifact that was fetched with HTTP 200 on 2026-10-27.

### §3.6 body, exact raw lines (base blob)

```
$ git -C … show c341a7a…:.ufo/waves/round-61/sources/S432.html | awk 'NR>=6146 && NR<=6157 {printf "%d: %.100s\n", NR, $0}'
6146: </p>
6147:     </div>
6148:    </div>
6149:    <h3 class="heading settled" data-level="3.6" id="x-content-type-options-header">…
6150:    <p>The
6151: `<dfn class="dfn-paneled" data-dfn-type="http-header" …><code>X-Content-Type-Options</code></dfn>`
6152: response <a …>header</a> can be used to require checking of a <a …>response</a>’s
6153: `<code>Content-Type</code>` <a …>header</a> against the <a …>destination</a> of a
6154: <a …>request</a>.
6155:
6156: </p>
6157:    <div class="algorithm" data-algorithm="determine nosniff">
```

The substantive sentence occupies lines **6151–6154** under the `data-level="3.6"`
heading at 6149 — matching the contract's cited range. The generic lead-in the
round-61 verifier rejected is in the same §3.6 section at line 6183
(`"Web developers and conformance checkers must use the following"`), confirming the two
strings are distinct and the correction targets a different sentence than the rejected
one.

### Quote normalization (integrity of the frozen `QUOTE` constant)

The counter's `QUOTE` is the *de-markup* rendering of the §3.6 sentence. It is **not** a
literal substring of the raw HTML (inline `<a>`/`<code>` elements and backticks
intervene). After stripping tags, unescaping entities, collapsing whitespace and
removing the code backticks:

```
de-tagged, backtick-stripped §3.6 text:
"The X-Content-Type-Options response header can be used to require checking of a response’s Content-Type header against the destination of a request."
QUOTE in that text: True      (exact substring)
occurrences of QUOTE in the whole de-markuped body: 1   (offset 109070)
```

The counter's quote is therefore faithful to the source text and **unique** to §3.6: the
only other "response header can be used to require checking …" sentence in the body is at
line 6232 and belongs to §3.7 (`Cross-Origin-Resource-Policy`, "checking a request's
current URL's origin"), a different sentence. The counter's quote uses U+2019 (`’`),
matching the source's apostrophe exactly; no ASCII-`'` variant occurs in the body.

### Base-state gate inputs (all read from base blobs)

```
disagreements = 1   (exactly one line in the base spot-check blob carries both "S432" and "Disagree":
                     line 33 — "| S432 / Fetch | Admit | https://fetch.spec.whatwg.org/, §3.6; … | Disagree | …")
quote_correction = 0 (knowledge blob: QUOTE absent; "S432 §3.6" present; "Round-62 correction" absent)
criterion        = 0 (QUALITY blob: "substantive located quote" absent; "round-61-verifier-spotcheck.md" absent)
lesson_gate      = 0 (corpus/lessons/round-62.md absent at base → blob "" )
source_row       = 1 (corpus/SOURCES.md line 178: "| S432 | WHATWG Fetch — https://fetch.spec.whatwg.org/ | spec | A | …")
```

Base control, run from the lane root with the frozen counter:

```
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit=1
```

Byte-identical to the mission's recorded base-control. No filter interference is
possible: the base tree has no `.gitattributes` and `git check-attr -a` returns nothing
for any measured path, so `git show` returns raw blob bytes (the global `filter.lfs.*`
config is inert here — no LFS attributes bind these paths).

## 7. Advisory notes (no action taken — claim/counter untouched)

1. **Counter lives outside Git.** `.ufo/waves/round-62/c62_calibration.py` is untracked;
   its SHA-256 is the sole integrity pin. It matched `ba7b7737…548d` at the start and at
   the end of this seat's work.
2. **Silent-degradation path in `blob()`.** A missing/unreadable path returns `""`.
   Only the spot-check path is guarded (exit 2, `could-not-evaluate`); a failed read of
   `corpus/knowledge/…`, `corpus/QUALITY.md`, `corpus/lessons/round-62.md` or
   `corpus/SOURCES.md` silently contributes 0 to its flag. Fail-closed with respect to
   `met` (a 0 can never satisfy the composite predicate), but the failure is invisible in
   the output. Post-integration re-verification should therefore confirm the individual
   flags, not only `met=true`.
3. **Keep the S432 row.** `disagreements` is expected to remain `1` after the fix
   (§5d); `unresolved` reaches 0 through the four landed artifacts, not by editing the
   row. Editing the row's verdict is unnecessary and would misrepresent the round-61
   record.
4. **`lesson_gate` is all-or-nothing on `corpus/lessons/round-62.md`**, which does not
   exist at base — it must be created and committed, containing `## Gate`, `S432`,
   `Agree` and `Reject`.

## 8. Commands run (read-only against the lane)

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse --show-toplevel
git -C … rev-parse c341a7a…^{commit} / master / origin/master / HEAD
git -C … ls-remote origin refs/heads/master
git -C … branch -a --contains c341a7a…
git -C … log -1 --format=… c341a7a…
git -C … fsck --no-progress --no-dangling
git -C … replace -l ; ls .git/info/grafts ; ls .git/info/attributes
git -C … status --porcelain [--ignored] [--untracked-files=no]
git -C … diff --stat c341a7a… -- corpus/
git -C … ls-tree -r --name-only c341a7a… -- <measured paths>
git -C … ls-tree --name-only c341a7a…:.ufo/waves/round-61/sources
git -C … rev-parse c341a7a…:<path>       (blob OIDs)
git -C … hash-object -- <path>           (worktree blob OIDs)
git -C … cat-file --batch-check='…'      (object type/size, packed)
git -C … cat-file -e c341a7a…:corpus/lessons/round-62.md
git -C … show c341a7a…:<path>            (blob contents for line-exact quoting)
git -C … check-attr -a -- <measured paths>
sha256sum .ufo/waves/round-62/c62_calibration.py
sha256sum .ufo/waves/round-61/sources/S432.html
python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision <base|0…0>
```

Fixture-side (private clone, explicit `git -C`, no lane mutation):
`git clone --no-hardlinks <lane> fixture` → `git -C fixture checkout <base>` →
junk-file overwrite → measure → candidate-fix commit (`-c user.name=fixture -c user.email=fixture@local`) →
measure base and fix revisions → second empty repo with worktree-only file → measure.

Scratch: `/fast/scratch/hyaku/kake-r62/ExecutorCounterDataIntegrity/` (fixture clone,
second empty repo, backup copy) — **deleted before yield**.

## 9. Blockers

None.
