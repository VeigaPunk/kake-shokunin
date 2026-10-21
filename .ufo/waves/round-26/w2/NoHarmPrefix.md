# W2 — Append-only / no-harm prefix check (round-26 C1)

**Verdict: AGREE (severity: low)** — with one documented criterion deviation on
`corpus/SOURCES.md` (see §4). No prior byte was altered or dropped anywhere in the
diff; no file was deleted or renamed; the S001–S035 registry rows are byte-identical.

- Base: `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`
- Candidate: `e28312b14b076584fedd696fae2a684e460bd11e` (== `HEAD` of
  `/home/vgpnk/Projects/shokunin/kake-shokunin`)
- Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`
- Tooling: no package installed or upgraded by this seat (no `pacman` / `uv` / `cargo`
  / `npm` transaction; all checks used the already-present `git`, `python3` (stdlib),
  `node`). Nothing outside this report file was written.

---

## 1. Change inventory — no deletions, no renames

```
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --name-status \
    97404de4ff73d6c8a4f87385cf5fdf36dca7f006 e28312b14b076584fedd696fae2a684e460bd11e \
  | cut -f1 | sort | uniq -c
    187 A
     11 M
```

```
$ git diff --diff-filter=D --name-only 97404de… e28312b… | wc -l
0
$ git diff --diff-filter=R --name-status 97404de… e28312b… | wc -l
0
$ git diff --summary 97404de… e28312b… | grep -v 'create mode'   # mode/type changes
(no output)
```

The 11 modified paths (`git diff --name-status … | grep -v '^A'`):

```
M LOG.md
M SCORECARD.md
M SKILL.md
M corpus/QUALITY.md
M corpus/README.md
M corpus/SOURCES.md
M corpus/knowledge/crawl-scope-per-host.md
M corpus/knowledge/ghp-custom-domain.md
M corpus/knowledge/ghp-etag-anatomy.md
M corpus/knowledge/ghp-served-set.md
M corpus/knowledge/static-canonical-preflight.md
```

All 187 added paths are new: 186 under `.ufo/waves/round-26/**` (fetch scripts, 35
retained `*.raw.gz`, `manifest.json`, `manifest-retry.json`, 34 `text/*.txt` views, 32
`rechecks/S0NN.json`, `statements.json`, `population.json`, `measure.py`, `w1/**`
reports) plus one new corpus lesson `corpus/lessons/round-26.md`. No added path
collides with a base path (all statuses are `A`).

## 2. Byte-prefix property, per modified file

Procedure (in-memory, no scratch files): for each `M` path, read the old blob with
`git show <base>:<path>` and the new blob with `git show <cand>:<path>` and test
`new.startswith(old)` byte-wise.

```
LOG.md: oldlen=86831 newlen=88285 prefix=True  delta=1454
SCORECARD.md: oldlen=47529 newlen=48278 prefix=True  delta=749
SKILL.md: oldlen=68847 newlen=70117 prefix=True  delta=1270
corpus/QUALITY.md: oldlen=18162 newlen=19210 prefix=True  delta=1048
corpus/README.md: oldlen=14567 newlen=14968 prefix=True  delta=401
corpus/SOURCES.md: oldlen=28637 newlen=29404 prefix=False delta=767   <-- see §4
corpus/knowledge/crawl-scope-per-host.md: oldlen=3160 newlen=3942 prefix=True delta=782
corpus/knowledge/ghp-custom-domain.md: oldlen=3694 newlen=4475 prefix=True delta=781
corpus/knowledge/ghp-etag-anatomy.md: oldlen=3304 newlen=4905 prefix=True delta=1601
corpus/knowledge/ghp-served-set.md: oldlen=4843 newlen=6865 prefix=True delta=2022
corpus/knowledge/static-canonical-preflight.md: oldlen=14076 newlen=16987 prefix=True delta=2911
```

**10 of 11 modified files are strict byte-prefix extensions.** The single exception is
`corpus/SOURCES.md` (§4).

### 2a. The two `-1` numstat rows are not deletions

`git diff --numstat` reports `5 1` for `crawl-scope-per-host.md` and `9 1` for
`ghp-etag-anatomy.md`, i.e. one removed line each. This is the missing final newline
on the base blob, not a lost line:

```
crawl-scope-per-host.md  old_endswith_nl=False new_endswith_nl=True prefix=True
  old tail: b'... - **Shape-only probe environment:** no live response, credential, or session data was collected.'
ghp-etag-anatomy.md       old_endswith_nl=False new_endswith_nl=True prefix=True
  old tail: b'... - **Validator is not identity:** the opaque marker is not treated as a content digest.'
```

The diff renders the last base line as removed and re-added only because the base
blob lacked a trailing `\n`:

```
@@ -50,4 +50,8 @@ An operator-authorized free read can settle this; no lane property was probed.
- **Shape-only probe environment:** no live response, credential, or session data was collected.
+ **Shape-only probe environment:** no live response, credential, or session data was collected.
+
+## Round-26 source recheck
```

No base line content was dropped; the appended EOF block follows it.

## 3. Lane-canonical append-only criterion (stripped diff) — PASS on all 11 files

`corpus/QUALITY.md:19` ("Append-only tails") requires: *“every base line survives
byte-for-byte once the tails are stripped (checked by a stripped-diff over `git show
<base>:<file>`)”*, superseded by `corpus/QUALITY.md:33-39` (round-20 ruling):
*“preserve every prior lesson/knowledge line byte-identically; use pure new-line
additions or end-of-file correction blocks citing the old line.”*

Stripped-diff reconstruction (remove exactly the `+` lines of the unified diff from
the candidate blob, compare with the base blob, line by line):

```
LOG.md: stripped==base_lines True  (base 987 lines, cand 1010 lines, added 23)
SCORECARD.md: stripped==base_lines True  (base 501, cand 513, added 12)
SKILL.md: stripped==base_lines True  (base 575, cand 588, added 13)
corpus/QUALITY.md: stripped==base_lines True  (base 206, cand 225, added 19)
corpus/README.md: stripped==base_lines True  (base 166, cand 174, added 8)
corpus/SOURCES.md: stripped==base_lines True  (base 103, cand 105, added 2)
corpus/knowledge/crawl-scope-per-host.md: stripped==base_lines True  (base 53, cand 58, added 5)
corpus/knowledge/ghp-custom-domain.md: stripped==base_lines True  (base 59, cand 63, added 4)
corpus/knowledge/ghp-etag-anatomy.md: stripped==base_lines True  (base 56, cand 65, added 9)
corpus/knowledge/ghp-served-set.md: stripped==base_lines True  (base 80, cand 90, added 10)
corpus/knowledge/static-canonical-preflight.md: stripped==base_lines True  (base 181, cand 195, added 14)
```

So under the lane's own canonical definition the change set is append-only: every base
line survives byte-for-byte, and every modification is a pure new-line addition.

## 4. Deviation (low) — `corpus/SOURCES.md` is not a byte-prefix extension

`corpus/SOURCES.md` fails the strict byte-prefix check: the Round-26 log paragraph and
one blank line are **inserted at line 79**, between the Round-25 paragraph and the
`## Leads (unopened)` heading, not appended at EOF.

```
$ git diff -U0 97404de… e28312b… -- corpus/SOURCES.md
@@ -78,0 +79,2 @@ Round 25 bounded question (2026-10-21): what publisher-side evidence must be
+Round 26 bounded recheck (2026-10-21): do the 32 previously opened external rows (S001–S034 minus own-work S014/S019) still support their teaches at their anchors? … [603 chars]
+
```

Byte-level divergence point:

```
diverge at 26150
 old: b'… is inferred.\n\n## Leads (unopened)\n\n- GitHub Docs: Verifying your custom do'
 new: b'… is inferred.\n\nRound 26 bounded recheck (2026-10-21): do the 32 previously …'
```

Why this is *not* content harm (all evidence, no inference):

- The insertion is a **pure new-line addition**: no base line is modified, split, or
  removed; §3 shows the stripped candidate equals the base exactly.
- Placement is chronologically correct inside the `## Search log` section: base file
  order is `## Search log` → Round 21 → 22 → 23 → 24 → 25 paragraphs → `## Leads
  (unopened)`. The new Round-26 paragraph sits after Round 25 and before the next
  heading, so it stays inside the search-log section and preserves round ordering.
  Appending at EOF instead would place it after the trailing `## Leads` block and the
  `Round-23 precision note for S030` paragraph — semantically misplaced and outside
  the search-log section.
- The lane's canonical rule explicitly permits “pure new-line additions”
  (`corpus/QUALITY.md:35-37`), so the placement complies with the corpus contract
  even though it is not a strict prefix.

**Minimal correction (only if a literal byte-prefix reading is demanded):** move the two
inserted lines to EOF of `corpus/SOURCES.md` (i.e. append the Round-26 paragraph after
the current last line), leaving every base byte in place. That yields
`new.startswith(old) == True` for all 11 modified files without touching any other
file. Trade-off: the search-log paragraph then sits outside the `## Search log`
section, which is why this is filed as a deviation, not as a defect.

## 5. `corpus/SOURCES.md` registry rows S001–S035 — byte-identical

Rows extracted with `^\|\s*(S0\d\d)\s*\|` from both blobs; every row compared as a full
line, with line numbers and a sha256 over the concatenated row set:

```
rows in base: 35   rows in cand: 35   all rows byte-identical: True
ids: S001,S002,S003,S004,S005,S006,S007,S008,S009,S010,S011,S012,S013,S014,S015,S016,S017,S018,S019,S020,S021,S022,S023,S024,S025,S026,S027,S028,S029,S030,S031,S032,S033,S034,S035
sha256(base rows)= 672172e691639e00fea4491aec246438bf00e3703992282288724c9f68f6ddb1
sha256(cand rows)= 672172e691639e00fea4491aec246438bf00e3703992282288724c9f68f6ddb1
base row line numbers identical: True
table-line sets equal: True  only_old: 0  only_new: 0
```

No row was added, removed, or edited; no status/recheck/used-by cell changed — which is
exactly what the appended Round-26 paragraph in the same file asserts (“No row added,
rejected or changed; no status/recheck/used-by cell changed”). The assertion and the
bytes agree.

## 6. Cross-check: the 8 STALE corrections sit in appended tails only

Contract: `appendOnly: "… prior corpus bytes preserved; corrections as EOF blocks tagged
[r26-recheck S0NN STALE]"` (`.ufo/waves/round-26/contract.json`).

```
$ grep -rno '\[r26-recheck S0[0-9][0-9] STALE\]' corpus/ | sort
corpus/knowledge/ghp-etag-anatomy.md:62:[r26-recheck S010 STALE]
corpus/knowledge/ghp-etag-anatomy.md:64:[r26-recheck S010 STALE]
corpus/knowledge/ghp-served-set.md:85:[r26-recheck S003 STALE]
corpus/knowledge/ghp-served-set.md:87:[r26-recheck S003 STALE]
corpus/knowledge/static-canonical-preflight.md:186:[r26-recheck S021 STALE]
corpus/knowledge/static-canonical-preflight.md:188:[r26-recheck S026 STALE]
corpus/knowledge/static-canonical-preflight.md:190:[r26-recheck S030 STALE]
corpus/knowledge/static-canonical-preflight.md:192:[r26-recheck S030 STALE]
--- count ---
8
```

All 8 tags are inside the appended tails of the five modified knowledge files; every
one of those files is a strict byte-prefix extension (§2), so no tagged correction sits
on or beside an altered original line. Tags occur only in files the candidate actually
modified — the 20 untouched `corpus/knowledge/*.md` and `corpus/lessons/*.md` files
remain byte-identical to base.

## 7. Operability / no-harm gates re-run on the candidate tree

```
$ node scripts/corpus-contract.mjs --root .
result: 0 findings · 23 knowledge entries · 21 lane lessons · 10 skipped · 0 errors — exit 0

$ node scripts/freshness-sweep.mjs --offline --json   # read-only path; writes only in --selftest fixtures
exit=0
```

The candidate's new `corpus/lessons/round-26.md` satisfies the lane-author `## Gate`
requirement, and the freshness sweep is clean with the candidate corpus in place.

Retained-byte inventory consistent with the appended SOURCES.md paragraph (“34 fetches;
S008 one retry after a 60 s timeout”):

```
$ ls .ufo/waves/round-26/fetched/*.raw.gz | wc -l   → 35   (34 manifest attempts + 1 retry artifact)
$ ls .ufo/waves/round-26/fetched/text/ | wc -l       → 34
manifest.json entries: 34   distinct rows: 32
rows: S001..S013,S015,S018,S020..S034 (32)  == population S001..S034 minus S014/S019 → True
non-200 entries: [('S008', 'TimeoutError: The read operation timed out', None)]
manifest-retry.json: row S008, attempt 2, status 200
```

35 raw artifacts = 34 recorded attempts (one of which is the timed-out S008 attempt,
retained as the 20-byte `S008-1.raw.gz`) + the successful retry artifact. The count
claimed in the appended paragraph is accurate.

## 8. Findings by severity

- **low — `corpus/SOURCES.md` byte-prefix deviation (§4).** Two pure new lines inserted
  at line 79 instead of at EOF. No base byte lost or altered; registry rows untouched;
  lane-canonical append-only criterion still satisfied. Minimal fix if strict prefix is
  required: relocate the two lines to EOF of `corpus/SOURCES.md`.
- **none — everything else.** 0 deletions, 0 renames, 0 mode/type changes; 10/11
  modified files are strict byte-prefix extensions; the 11th is a pure new-line
  addition; S001–S035 rows byte-identical (sha256 match); all 8 `[r26-recheck S0NN
  STALE]` corrections confined to appended tails; corpus-contract and freshness-sweep
  gates exit 0.

## 9. Residual risk and verification gaps

- The literal byte-prefix reading of my assignment is violated by one file; a reviewer
  who treats that as a hard gate would require the §4 relocation. I judge it a
  placement choice, not a no-harm breach, because the lane's canonical rule
  (`corpus/QUALITY.md:33-39`) authorises pure new-line additions and the placement
  preserves the search-log ordering.
- Two base blobs (`crawl-scope-per-host.md`, `ghp-etag-anatomy.md`) gained a trailing
  newline. Byte-level append-only still holds; if a downstream hash over the exact
  final byte mattered, that is the only byte-level change outside new content.
- Untracked working-tree artifacts exist under `.ufo/waves/round-26/` (`__pycache__/`,
  `verification/`, `w2*/` wave files). They are not part of the candidate commit, so
  they are outside the diff verdict, but `__pycache__/` is unignored scratch that
  should not be committed later.
- Not adjudicated here (other seats own them): whether the 32 HOLD/0 STALE row verdicts
  and the 8 statement-level corrections are *correct*; I verified only that they were
  appended without touching prior bytes.
- No round-24 material was read, run, retried or rerouted.

```json
{"target":"round-26 C1 append-only/no-harm prefix check (97404de -> e28312b), corpus/SOURCES.md S001-S035 rows","verdict":"AGREE","severity":"low"}
```
