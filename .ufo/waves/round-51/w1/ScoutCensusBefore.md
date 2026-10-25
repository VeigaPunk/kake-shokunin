# ScoutCensusBefore — round 51 wave 1

**Seat:** `L1Kake51.ScoutCensusBefore-2` (scout, leaf — no subagent dispatch)
**Question:** does the frozen census command reproduce read-only at the lane tip, what exactly
does it print, and what registry row count does it report?
**Lane:** `/home/vgpnk/Projects/shokunin/kake-shokunin`
**HEAD throughout:** `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (verified at the end of the run; unchanged)
**Run date:** 2026-10-25 (container UTC; `date -u +%F` → `2026-10-25`)

## Verdict

At the committed tip the frozen command **reproduces deterministically and read-only: exit 0,
empty stderr, 13 stdout lines**. It **reports no registry row count** — `validate` has no `rows`
metric; the count exists only in `census` mode, a different argv. Measured separately:
**registry row count = 145**, corroborated three ways.

Two qualifications, both observed:

1. The exit-0 verdict is a **worktree-state** assertion, not a committed-bytes one. During this
   run another writer staged two rows in `corpus/SOURCES.md`; while that was live the same command
   returned **exit 1** with four E-codes (§6). The writer's edits were gone by 03:37:08 and the
   command returned to the T1 bytes.
2. The C2 condition that consumes this command (C7) validates a file whose bytes are
   **post-append**, not pre-append, under a directory named `pre-append` (§7).

---

## 1. Exact invocation

```
argv:  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
cwd:   /home/vgpnk/Projects/shokunin
env:   no overrides (TZ, TODAY, SHOKUNIN_ROOT all inherited unset)
```

Byte-identical to the assigned string. `kake` binds through `shokunin.conf:48`
(`kake|kake-shokunin|operability + freshness …`) via `build_roster`; it is a declared conf lane,
not a root-directory fallback (`resolve_targets`, `scripts/sources-census.sh`).

## 2. Observed result (T1 = 03:33:42, registry blob `9e2a221`)

**exit code: `0`**
**stderr: 0 bytes** (`od -An -tx1` shows no bytes)
**stdout: 1010 bytes, 13 lines, trailing LF, sha256 `2d3ed752fe26ec6ddeac06eff6bd31c437a4b9cc7ccc1784cb1239714e48352e`**

Verbatim (real tabs):

```
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```

Reading it correctly:

- **0 E-codes, 12 W04, 1 `ok`.**
- `ok` is emitted when the lane has no `E[0-9]` finding (`sources-census.sh:745`). It does **not**
  mean "no findings": twelve W04 lines are printed above it.
- Per the script's own contract (`sources-census.sh:18`), **exit `0` means "clean or warnings"**,
  so `0` is not evidence of a clean registry. W04 (scope-sensitive duplicate URLs) is non-fatal by
  design (selftest `W04-does-not-fail-validation`).
- The `ok` line embeds the **absolute** registry path, so stdout is bound to the `--root` spelling.

## 3. Registry row count — the frozen argv does not report one

Code fact (read, not inferred):

- The `rows` counter is printed only in `END { if (mode=="census") { … } }` at **line 690**
  (`rows`, `tier.*`, `status.*`).
- The `validate` branch (**725–747**) emits only `[EW][0-9]+` lines plus `ok`. There is no row
  count, and `--verbose` does not add one — its only use is line 714 ("has no corpus/SOURCES.md",
  stderr, missing-registry case).

So the frozen argv **cannot** supply "the registry row count it reports": it reports none. The
number requires `census` mode, i.e. a **different** argv:

```
supplementary (NOT the frozen argv):
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake
→ exit 0, stderr empty, and:
kake	rows	145
kake	tier.A	122
kake	tier.B	6
kake	tier.C	17
kake	status.mined	115
kake	status.queued	8
kake	status.rejected	22
FLEET	rows	145
FLEET	tier.A	122 | tier.B 6 | tier.C 17 | tier.invalid 0
FLEET	status.queued 8 | mined 115 | rejected 22 | invalid 0
FLEET	missing	0
```

**Row count = 145**, corroborated independently:

| method | result |
|---|---|
| `census` mode `rows` metric | 145 |
| awk over `## Registry` rows matching `^ {0,3}\| *S[0-9]{3}` (worktree) | 145 |
| same awk over `git show 9d13768:corpus/SOURCES.md` | 145 |

Provenance spread (same awk, `## Registry` only):

| revision | S-rows | S262 | S263 |
|---|---|---|---|
| base `007d66e` | 143 | absent | absent |
| tip `9d13768` | 145 | present, line 152 | present, line 153 |

The tip delta is **exactly +2 rows** and they are the C2 adopted entries. Both rows are
well-formed: 11 cells, `tier=A`, `status=mined`, `opened=2026-10-24`, `recheck=180d`,
`used-by` naming `corpus/knowledge/canonical-selection.md` / `crawler-identity.md`, no inner pipe.
That is C2's *structural* grounding; it does not validate C2's other conditions (C2-tip/base seats).

## 4. Determinism, and where it is not deterministic

| probe | result |
|---|---|
| rerun of frozen argv | byte-identical (`cmp` clean) |
| frozen argv + explicit `--today 2026-10-25` | byte-identical |
| `TZ=Pacific/Kiritimati` | byte-identical (TODAY from `date -u +%F`) |
| `TZ=UTC` | byte-identical |
| frozen argv + `--today 2026-01-01` | **exit 1, 145 × E08** ("opened is a future date") |

Stable for a fixed day and timezone-independent, **but the verdict is clock-relative**: the argv
fixes no `--today`, so it inherits the wall clock. Correct for a "today" validator; a
reproducibility caveat for any ledger that cites the exit code as a time-invariant fact.

## 5. Read-only proof, time-scoped

I never wrote to the registry. Every measurement below is a read; the only file this seat wrote is
this report.

| time (local) | registry blob (`git hash-object`) | in-`Registry` rows | frozen argv |
|---|---|---|---|
| 03:33:42 | `9e2a22175ef95a23252b349d8743cf0e5b5480fc` (**== HEAD**) | 145 | exit 0, 13 lines |
| 03:36:21 | `ae7e6229b791e6834c647c171c8f88dc07b8899e` (dirty) | 145 (+1 outside) | **exit 1, 4 E-codes** |
| 03:36:47 | `e165948289cb29565391cbfa131dda02f6835a50` (dirty) | 146 (+1 outside) | not run |
| 03:37:08 | `9e2a22175ef95a23252b349d8743cf0e5b5480fc` (**== HEAD**, restored) | 145 | exit 0, byte-identical to T1 |

- At T1 `git hash-object corpus/SOURCES.md` == `git rev-parse HEAD:corpus/SOURCES.md` ==
  `9e2a221…`; sha256 `4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3`;
  `git status --porcelain -- corpus/` empty.
- At T1 no `--out` was passed and nothing was written under the lane.
- The T2/T3 dirty states were **not mine** — see §6. §5 is scoped to T1/T4, where the claim holds.

## 6. Observed: a concurrent writer briefly broke the census

Between T1 and T2 an external writer staged two lines in `corpus/SOURCES.md`
(`git diff --stat` → `1 file changed, 2 insertions(+)`, no deletions). While live, the **same
frozen argv** returned **exit 1** with:

```
kake	E01	S149 fields=12
kake	E12	S160 row outside Registry section
kake	E11	S149 missing used-by grep -c 'a hint
kake	E11	S149 missing used-by not a rule'` -> 1 (ran 2026-10-23)
```

Mechanisms (read from the staged bytes):

- **S149** was inserted inside `## Registry` (line 154) with a literal `|` in the *recheck* cell,
  inside a backtick shell snippet: `180d — `curl -fsSL '…' \ | grep -c 'a hint, not a rule'` -> 1
  (ran 2026-10-23)`. The unescaped pipe splits the row into 12 fields → **E01**, and the two
  fragments are then read as `used-by` paths → **two E11**.
- **S160** was appended under `## Leads (unopened)` (line 261), i.e. outside `## Registry` → **E12**.
- At T2 the staged S149 carried the **same URL** as committed S262
  (`developers.google.com/search/docs/crawling-indexing/canonicalization`). **[INFERENCE]** if that
  row is later repaired to 11 cells and appended as-is, `E04` (duplicate URL+scope) is the expected
  finding unless it supersedes S262.

By T4 both lines were gone, the blob returned to `9e2a221`, and the frozen argv returned to the
exact T1 bytes. HEAD never moved.

**Consequence for the round's claims:** "the census exits 0" is true of the *committed tip* and
false of the *worktree* whenever a sibling is mid-append. Any wave instrument that pins this exit
code must pin the registry blob alongside it (`9e2a221…` here), otherwise the receipt is not
re-derivable from bytes.

## 7. Attack: the C2 condition that consumes this command (C7) is labelled wrongly

Observed bytes:

- C7 (`c51_quote_truth.py:246-262`) reads three receipts under
  `.ufo/waves/round-51/assimilation/pre-append/`: `census-argv.txt`, `census-stdout.txt`,
  `census-exit.txt`.
- `census-argv.txt` (verbatim):
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md`
- `census-exit.txt` = `0`; `census-stdout.txt` = 13 lines, 1054 bytes; `census-stderr.txt` = 0 bytes.
- Replaying that argv against the committed mirror: **rc 0, stdout byte-identical to the receipt**,
  stderr empty; also identical with `--today 2026-10-24`. The receipt is honestly reproducible.

The problem is what the receipt is about:

| object | blob | in-`Registry` rows | S262/S263 |
|---|---|---|---|
| mirror file `assimilation/pre-append/corpus/SOURCES.md` | `9e2a221` | 145 | **both present** |
| registry at the mirror's add-commit `19a99bd8` (23:20:47) | `cd448ea` | 143 | absent |
| registry at tip (append commit `5591557`, 23:20:56) | `9e2a221` | 145 | present |

- The mirror file's committed bytes **are the post-append registry** (same blob as the final
  `corpus/SOURCES.md`), despite living under `pre-append`.
- Therefore C7's "validate **before** append" runs the census over the **already-appended**
  registry. It cannot distinguish pre-append from post-append, so its evidential value under that
  label is tautological.
- C8 escapes this: it compares against `show(mirror_commit, REGISTRY)` — the registry *at the
  commit*, 143 rows, no S262/S263 (`c51_quote_truth.py:281-289`) — not the mirror file. C7 and C8
  disagree about which bytes "the mirror" means.
- C2 still prints `C2 quote-truth 8/8 met=True`, rc 0, when I run it at the tip myself. The counter
  is internally consistent; the finding is about C7's evidence meaning, not a failed condition.
- `--file` mode also resolves `used-by` relative to `dirname(file)/..`, so a `--file` census is
  only faithful when the file sits at `<some-dir>/corpus/SOURCES.md` (observed: extracting the
  committed registry to `/tmp` and validating it produced two spurious `E11` for S262/S263, because
  `/tmp/corpus/knowledge/` does not exist). C7's mirror path satisfies this by accident of layout.

Confidence: **observed** for every blob, row count and byte above. **[INFERENCE]** that the mirror
copy was written after the append had landed — I see commit timestamps (23:20:47 vs 23:20:56) and
identical blobs, not the authoring order itself.

## 8. Not checked (out of this seat)

- Wire reachability/content of the S262 and S263 URLs (freshness at source) — C2 tip/base seats.
- C1's L1/L2/L3 (ledger was 0/3 at dispatch; the L1 authors that evidence; `c51_wave_ledger.py`
  contains no census/registry reference, verified by grep).
- Whether `--file` mode's lane label `file` is an intended consumer contract or a `resolve_targets`
  shortcut.

## Tooling

No installs or upgrades. Commands: `bash`, `git` (read-only: `show`, `rev-parse`, `hash-object`,
`log`, `diff`, `status`, `merge-base --is-ancestor`), `python3 -B`, `awk`, `cmp`, `sha256sum`,
`wc`, `od`, `stat`, `diff`.
