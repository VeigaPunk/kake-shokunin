# SourceRulesConnect — round-26 recheck integration rules (L1 checklist)

Scope: read-only mapping of the SOURCES/knowledge mutation rules for the round-26 C1
freshness recheck. No corpus, SOURCES, knowledge, lesson, script or Git state was edited.
No tool was installed or upgraded. No network access was made by this seat; all evidence is
in the round-26 cache and the lane/fleet files named below.

Evidence base:

- `../CORPUS.md:89-110` — SOURCES cell definitions (id, tier, scope, anchor, teaches,
  status, opened/recheck, used-by).
- `../CORPUS.md:112-118` — SOURCES contract v1 rules 1-2: a row is a claim; append-only;
  **only `status`, `recheck`, `used-by` change in place**, each logged old→new in the round
  lesson; **a correction is a new row whose `teaches` opens `supersedes S0NN —`**.
- `../CORPUS.md:53-60` — corrections are new entries, never rewrites.
- `corpus/QUALITY.md:20` and `:31-40` — append-only tails; the round-20 ruling requires every
  prior lesson/knowledge line to survive byte-identically; use pure new-line additions or
  end-of-file correction blocks citing the old line; never split a table to satisfy a gate.
- `corpus/QUALITY.md:162` — round-24: original corpus lines remain byte-identical; separate
  correction blocks replace suffix edits; restoration notes carry no absence vocabulary.
- `corpus/SOURCES.md:9-43` — 35-row Registry (S001-S035), 11 cells per row (NF=13).
- `corpus/SOURCES.md:45-55,57-77,79-100,102` — Paths, Search log, Leads, and the existing
  EOF precision-note precedent.
- `.ufo/waves/round-26/contract.json` — C1, population, fetch method, `appendOnly`.
- `.ufo/waves/round-26/population.json` — 32 in-scope rows with current cells and fetches.
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` — E04 at `:646-649`, E08 at
  `:661-662`, E09 at `:663-666`, E11 at `:557-569`, W01 at `:670`, W03 at `:674`, overdue
  at `:675-685`; its own selftest names `cadence-due-on-opened-plus-N` at `:147`.

Snapshot at 2026-10-21T15:33Z (not a verdict for pending rows): 30 of 32 row reports had
landed, all `HOLD`; `RowS012.md` and `RowS030.md` were absent. `.ufo/waves/round-26/measure.py`
is absent although `contract.json.claim.count` names it. Both facts are integration
prerequisites, not results.

---

## 1. The mutation law

### 1.1 Frozen cells — never edit in place, under any verdict

`id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened`.

This is not a style preference. `teaches` is the registry's claim; `anchor` is its locator;
`opened` is the historical open date. Contract v1 rule 2 (`../CORPUS.md:116-118`) permits
only three cells to change. A changed teaching, anchor or version is carried by a **new row**,
not by editing the old one. The round-26 contract repeats this as `appendOnly`.

Consequences L1 must enforce:

- A `HOLD` whose only difference is a moved section/line does **not** get an `anchor` edit.
  The receipt's `anchorObserved` records the move; the row remains `HOLD` (round-26 receipt
  contract). If the literal locator can no longer be followed, add a prose EOF precision
  note (precedent: `corpus/SOURCES.md:102`), never an edit to the `anchor` cell.
- A `STALE` whose version/date/quote changed does **not** get an `anchor` or `teaches` edit.
  Add a superseding row (§3).
- Do not "fix" a table row's spacing, wording, cell order or trailing pipe while editing a
  permitted cell. The row must stay 11 cells / NF=13.

### 1.2 Mutable cells — only these three, only with a logged old→new value

| cell | legal reason to change | required evidence |
|---|---|---|
| `status` | a citation was added to `used-by` and the row becomes `mined`; or all citations were removed as erroneous and it returns to `queued`. A rejection is carried by a **new** row; the old row's status does not flip | Gate log row with exact old and new enum; E07/E11/W03 clean |
| `recheck` | the future recheck date/cadence changed (see §5); or the source's update model changed | Gate log row with exact old and new value; E09 clean; reason names the receipt date |
| `used-by` | a knowledge entry or lesson substantively cites the row and the path is missing from the cell; or a cited path moved/was corrected | Gate log row with exact old and new comma-separated value; each path exists (E11) |

No other cell is mutable. In particular, do not use `status=rejected` as a "retired" flag:
`rejected` means "kept — a rejection is evidence of taste" (`../CORPUS.md:105-107`). A
superseded row is not a rejected lead. Its immutable `teaches` still states what it taught;
the new row's `supersedes S0NN —` prefix is the retirement relation.

### 1.3 Row integrity and append position

- New rows are appended **after the last registry row** (currently S035), not inserted beside
  the old row. The census checks duplicate URL+scope in file order and exempts only the later
  row when its `teaches` contains `supersedes S[0-9]{3}` (`scripts/sources-census.sh:646-649`).
  Appending keeps the old row first and the superseding row later; inserting can trigger E04.
- New ids are `S036`, `S037`, … in ascending order of the old row id. ids are never reused.
- No `|` inside any cell. No row-shaped line outside `## Registry` (E12).
- The row must be a single physical line; 11 cells; NF=13.

---

## 2. Verdict → integration matrix

The receipt contract has exactly three verdicts. The row's current status changes the meaning
of `HOLD`; L1 must not flatten that.

### 2.1 `HOLD`

Meaning: the row's `teaches` and `scope` are still supported at its anchor now. For a
`rejected` row, `HOLD` means the rejection still holds and the flip condition is still unmet.

Integration:

1. No new row. No `teaches`/`anchor`/`source`/`tier`/`scope`/`opened` edit.
2. Record the receipt in `corpus/lessons/round-26.md` (§8).
3. Leave `status` and `used-by` unchanged. Do **not** add
   `corpus/lessons/round-26.md` to `used-by` merely because the Gate rechecks the row; that
   would turn every queued/rejected row into `mined` and contaminate the taste record.
4. Change `recheck` only per §5 (numeric cadence whose opened-anchored due date no longer
   equals the receipt-anchored due date). Log old→new.
5. If `anchorObserved` records a move, copy it into the Gate's `anchorObserved` column. Add an
   EOF precision paragraph only if the literal locator is now unfollowable; that paragraph
   must say the content is unchanged and must not say `STALE`.

### 2.2 `STALE`

Meaning: the re-fetched content changed so that `teaches`, `anchor` or the named
version/date is now wrong or incomplete. A pure move with identical content is `HOLD`, not
`STALE`.

Integration:

1. Append exactly one superseding row per stale row (§3), at the end of the Registry.
2. Leave the old row's cells unchanged by default: `status` stays `mined`/`queued`/`rejected`;
   `used-by` keeps its historical citations (supersession is not citation erasure); `recheck`
   is not advanced on a row being retired.
3. Append the correction block to the citing corpus file (§7). If the row is uncited
   (`used-by` is `—`), the new row in `corpus/SOURCES.md` is itself the appended correction
   and the Gate records the recheck; if a current lesson cites it, append to `round-26.md`,
   not to the historical lesson.
4. Log the old→new mapping in the Gate: `S0NN STALE → S0MM`; quote, fetchIndex and
   `anchorObserved`; correction-block path and line.
5. If the row is `rejected` and the flip condition is now met, the new row carries the
   positive claim with the authority that met the flip (tier rules, §3.3). The old row stays
   `rejected` as history. If the rejected claim was withdrawn/moot but the flip is not met,
   the new row is still `rejected`, with `teaches` = `supersedes S017 — REJECTED: …; flip: …`.

### 2.3 `UNVERIFIABLE`

Meaning: retained bytes cannot decide the row (failed fetch with no body, dynamic shell with
no normative text, ambiguous rendered state).

Integration:

1. No new row. No cell change other than the Gate record. Do not relabel it `HOLD`
   (round-23 QUALITY rule at `corpus/QUALITY.md:145-147`).
2. Do not advance `recheck`. The row remains due/overdue, so the debt stays visible.
3. Record the exact failure, the fetchIndex/status, the retained bytes (if any), the named
   owner, and the restore-or-retire action in the Gate (QUALITY "Missing substrate stays
   visible").
4. `UNVERIFIABLE` is reported separately and never counted in the C1 numerator.
5. Decision tree: 404/410 where the row claims the source currently documents X → `STALE`
   (the surface is gone; a presence claim cannot survive); timeout/5xx/network with no bytes →
   `UNVERIFIABLE`; 200 but only a JS shell/no normative text → `UNVERIFIABLE`; 200 with
   changed normative text → `STALE`; 200 with unchanged text → `HOLD`.

### 2.4 Rejected rows (S017, S018)

- `HOLD` = rejection still holds; flip condition still unmet. No row change. Keep `rejected`.
- `STALE` = the page changed such that the stated rejection reason is now wrong or
  incomplete. Add a new row (S036+). Two cases:
  - flip met: new row is positive, tier determined by the **new** authority (a community
    source can never be tier A; a tier-C row cannot be sole support for an admitted entry);
  - flip not met but the old rejection text is obsolete: new row is `rejected`, `teaches`
    opens `supersedes S0NN — REJECTED: <current state>; flip: <updated condition>`.
- Never flip the old row's `status` to `mined`/`queued`; its immutable `teaches` still reads
  `REJECTED: …`.

---

## 3. The superseding-row recipe

### 3.1 Answer to the direct question

**Yes — a `STALE` row needs a superseding new row.** Contract v1 rule 2
(`../CORPUS.md:116-118`): "A correction is a new row whose `teaches` opens
`supersedes S0NN —`." Because `teaches` and `anchor` are frozen, the new row is the only legal
correction vehicle. The old row remains byte-identical except for any independently justified
`status`/`recheck`/`used-by` change.

### 3.2 Exact template

```text
| S0MM | <title — canonical URL actually fetched> | <kind> | <A|B|C> | <scoped topic of the corrected claim> | <exact section/heading/line + revision/date now> | supersedes S0NN — <one grounded learner benefit, corrected> | <queued|mined|rejected> | 2026-10-21 | <cadence or next-due date> | <repo-relative paths or —> |
```

Field rules:

- `teaches` **opens with the exact string** `supersedes S0NN — ` — `supersedes`, one space,
  the old id, one space, em dash U+2014, one space, then the corrected benefit. Do not use a
  hyphen, `--`, or a colon. The contract's prefix is the machine-readable relation.
- The prefix is followed by **one** grounded learner benefit. Do not paste a paragraph or a
  full receipt reason. Compress the row seat's `correction` text; do not truncate a claim.
- No `|` anywhere in the cell. Rewrite prose rather than using a lookalike character.
- If the new row is a rejection, the form is
  `supersedes S0NN — REJECTED: <reason>; flip: <condition>`. This satisfies both the
  supersedes-prefix rule and the rejected-row `teaches` rule.
- `source` is the URL actually fetched for the corrected claim (use `finalUrl` if the fetch
  redirected); `anchor` is the current location/revision, not the old row's stale locator.
  For a multi-URL row (S001, S002), keep both URLs only if both still ground the corrected
  composite claim; otherwise narrow the row to the authoritative one.
- `kind` and `tier` describe the new authority, not a copy of the old row's tier. A flip that
  requires a tier-A source gets a tier-A row citing that source; a community row stays
  tier C and cannot be sole support for an admitted entry (`../CORPUS.md:95-101`).
- `scope` is the exact topic the tier applies to. If the correction narrows the claim, narrow
  the scope; do not reuse a scope the new row no longer covers.
- `status`:
  - `mined` only if `used-by` names ≥1 existing path that substantively cites the new row
    (typically the corrected knowledge entry's EOF block);
  - `queued` if no knowledge entry/lesson adopts it (used-by `—`);
  - `rejected` only for a superseding rejection. Never `mined` with `used-by: —` (W03).
- `opened` = `2026-10-21` (the date the source was opened/re-fetched this round).
- `recheck` = the old row's cadence (90d/180d/365d/on-release) unless the source's update
  model changed. Because `opened` is today, a cadence already yields the correct next-due
  date; no ISO conversion is needed on a new row.
- `used-by` = exact repo-relative paths, comma-separated, or `—`. Each path must exist at the
  measured commit (E11).

### 3.3 One-to-one and ordering

- Exactly one new row per stale old row. If two old rows share a source, still create one new
  row per old row (the old rows may have different scopes/tiers); do not collapse them into
  one row that supersedes two ids, because the contract's prefix names one id.
- Append new rows in ascending old-id order. Do not insert beside the old row (§1.3).
- If a row is already superseded and this round finds the terminal row stale, supersede the
  terminal row; do not create a second row superseding the same id. (No `supersedes` rows
  exist in the registry at this baseline, so this is forward guidance.)

---

## 4. `status` truth table — the surprising part

Because `teaches` is frozen, most status flips are illegal even though `status` is a mutable
cell. A status change must remain consistent with the immutable teaching text.

| current | proposed | legal? | condition |
|---|---|---|---|
| `queued` | `mined` | yes | `used-by` gains an existing path that substantively cites the row; log old→new |
| `mined` | `queued` | yes, rare | every `used-by` citation is removed because it was erroneous; log; re-run E11/W03 |
| `queued`/`mined` | `rejected` | **no** | the immutable `teaches` does not read `REJECTED: …`; a status flip would contradict it. Add a superseding rejected row instead |
| `rejected` | `queued`/`mined` | **no** | the immutable `teaches` still reads `REJECTED: …`; add a superseding positive row instead |
| any | same | yes | default for every HOLD row; no log row needed |

Expected delta for the 32 rows this round: **zero status changes**, unless L1 admits a new
knowledge claim that cites S015/S016 (queued → mined). A recheck receipt alone is not a
citation. Do not use status to signal "rechecked", "retired" or "superseded".

---

## 5. `recheck` scheduling — the one non-obvious move

### 5.1 The gap

The fleet census's `overdue` mode computes a numeric cadence's due date from the **immutable
`opened`** cell: `due = opened + N days` (`scripts/sources-census.sh:35,675-685`; its selftest
is literally named `cadence-due-on-opened-plus-N`, `:147`). It does not know the round-26
receipt date. Therefore, if L1 rechecks S003 today and leaves `recheck: 90d`, the tool will
still report S003 due on 2027-01-17 (`2026-10-19 + 90d`), as if the 2026-10-21 recheck never
happened. The recheck is invisible to the schedule.

Proven read-only on the current registry:

```text
$ scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin kake --today 2027-01-17
kake  cadence  S003 recheck=90d opened=2026-10-19
kake  overdue  S017 0d recheck=90d opened=2026-10-19
kake  overdue  S016 0d recheck=90d opened=2026-10-19
kake  overdue  S015 0d recheck=90d opened=2026-10-19
kake  overdue  S014 0d recheck=90d opened=2026-10-19
kake  overdue  S013 0d recheck=90d opened=2026-10-19
```

(Output excerpt; S003-S007 also report `overdue 0d` in the same run. S008-S012 are 365d and
are not overdue on 2027-01-17.)

### 5.2 The move (one bounded proposal)

On a **decided HOLD**, advance `recheck` from a numeric cadence to the explicit next-due ISO
date **only when the opened-anchored due date differs from the receipt-anchored due date**:

```text
due_old = opened + N days
due_new = receipt_date (2026-10-21) + N days
if due_old != due_new: recheck = due_new (ISO), logged old→new
else: leave the cadence unchanged
```

For the observed all-HOLD set (30 landed rows HOLD; S012 and S030 pending at the snapshot)
this is exactly 21 rows. Recompute after the two pending verdicts: a `STALE` old row is
excluded from the advance and handled per §2.2 (the new row gets the old cadence); an
`UNVERIFIABLE` row is excluded per §2.3. The date arithmetic for the remaining rows does not
change.

| rows | old value | new value | reason |
|---|---|---|---|
| S003-S007, S013, S015, S016, S017 | `90d` (opened 2026-10-19) | `2027-01-19` | old due 2027-01-17 |
| S018 | `180d` (opened 2026-10-19) | `2027-04-19` | old due 2027-04-17 |
| S008-S012 | `365d` (opened 2026-10-19) | `2027-10-21` | old due 2027-10-19 |
| S020 | `365d` (opened 2026-10-20) | `2027-10-21` | old due 2027-10-20 |
| S021-S025 | `90d` (opened 2026-10-20) | `2027-01-19` | old due 2027-01-18 |

Leave unchanged:

- S028-S034 (opened 2026-10-21): `opened + N` already equals `2026-10-21 + N`; no churn.
- S001, S002, S026, S027: `on-release` is symbolic and event-driven; the tool reports it as a
  cadence and never judges it overdue.
- S014, S019, S035: not in the round-26 population; do not advance their clocks.
- Any `STALE` old row: it is being retired; do not schedule its next check. Give the new row
  the old cadence (opened 2026-10-21 makes it correct).
- Any `UNVERIFIABLE` row: do not advance; the debt must remain visible/due.

The Gate log row must state the next-due semantics, e.g.:

```text
| S003 | recheck | 90d | 2027-01-19 | 90d cadence, receipt 2026-10-21; opened 2026-10-19 would make the tool due 2027-01-17 |
```

This is a permitted `recheck` change under contract v1, not a contract amendment. It makes the
completed recheck visible to the fleet scheduler and anchors the next check to the actual
observation date. It is the one proposal in this report.

---

## 6. `used-by` rules

- A path is listed only if that file **cites** the row (a claim, a correction block, or a
  substantive lesson statement), not merely because the Gate rechecked it.
- Do **not** add `corpus/lessons/round-26.md` to a HOLD row's `used-by`. The Gate is an audit
  record; treating it as a citation would make every queued/rejected row `mined` and would
  inflate the "mined" population.
- On a STALE row, keep the old row's historical `used-by` unchanged. Add the same path to the
  new row's `used-by` only if the knowledge entry's appended block cites the new row. Both
  statements are true: the entry historically cited S0NN and now also cites S0MM.
- Remove a path only if the citation itself was erroneous; log the exact old and new values.
- Every path must be repo-relative and exist at the measured commit (E11). This is the reason
  the row/block/lesson writing order matters (§7.4).

---

## 7. How knowledge corrections must be appended

### 7.1 Target-file precedence

1. **A current `corpus/knowledge/` entry that states the now-wrong claim** → append the block
   to that entry. This is the "citing corpus file" in the contract's `after`.
2. **Only historical lessons cite the row** (e.g., S022-S025's `used-by` is
   `corpus/lessons/round-22.md`) → do **not** edit the historical lesson. Append the block to
   `corpus/lessons/round-26.md`, citing `round-22.md:LL`. Historical lessons are evidence of
   their round; they are not rewritten.
3. **No citing file (`used-by: —`)** → the new row in `corpus/SOURCES.md` is itself the
   appended correction (the registry is the corpus file that carries the row), and the Gate
   records the recheck. Optionally append a block to `round-26.md`; do not invent a knowledge
   entry just to satisfy the phrase "citing corpus file".

If multiple files state the wrong claim, append one block per file. The row has one
superseding new row; the blocks are per citing file.

### 7.2 Exact block shape

Append at end of file, after one blank line, as pure new lines. Never insert above existing
content; never split a table; never edit knowledge-entry frontmatter (`source:`,
`verified-at:`, `recheck:`).

```text
## [r26-recheck S0NN STALE] <short claim title> (2026-10-21)

- Old statement: `corpus/knowledge/<file>.md:LL` — "<neutral paraphrase; do not copy absence vocabulary>".
- Re-fetched: <URL> at <fetchedAt UTC>; receipt `S0NN-N`; text `fetched/text/S0NN-N.txt`; sha256 `<64 hex>`.
- Anchor now: <heading/line from the receipt's anchorObserved>.
- Quote now: "<6–25 words copied verbatim from the text file>".
- Superseded by: `S0MM` — `teaches` opens `supersedes S0NN — <corrected benefit>`.
- Corrected statement: <what the entry now relies on>.
- Prior text above remains historical and is not rewritten; this block is the current correction.
```

The tag must be exactly `[r26-recheck S0NN STALE]`, on the block's first heading line, so a
single `grep -n '\[r26-recheck S0NN STALE\]'` finds it. One block per (row, file). If the same
file has two wrong statements from the same row, list both line refs in one block. If two
different rows are stale in the same file, use two blocks with their own tags.

### 7.3 Content rules

- Quote must be from the **normalized text view**, not the raw HTML. `source_text.py` collapses
  whitespace, strips spaces before punctuation, unescapes entities, and skips
  script/style/noscript/template content. A seat quote that only exists in raw HTML is not a
  valid grounding quote.
- 6–25 whitespace-delimited words, contiguous, word-bounded. Do not add an ellipsis unless the
  source contains it. Do not stitch two passages.
- Avoid the freshness-sweep absence vocabulary in the block: `absent`, `gone`, `vanished`,
  `emptied`, `no longer`, `dangling`, `no such file`, `never published`, `missing`
  (`scripts/freshness-sweep.mjs:122`). A correction is not a citation-local absence
  annotation; those words within ±2 lines of a live citation can silently clear a dead-path
  finding. Say "is superseded", "is withdrawn", "now reads …", not "no longer says".
- Do not state a new current fact beyond what the quoted bytes support. The block is a
  correction of a source claim, not a new platform observation.
- Keep the original lines byte-identical. EOF-only appends do not move existing line
  coordinates, so no round-21 line register is needed. If L1 ever inserts lines above
  existing content, stop and ship the round-21 inbound-pointer census; this checklist forbids
  that insertion.

### 7.4 Ordering (avoids E11 and dangling citations)

1. Freeze receipts/verdicts; validate quotes against the retained text (§8).
2. Append the new rows S036+ to `corpus/SOURCES.md` (Registry end).
3. Append the EOF correction blocks to the knowledge entries / `round-26.md`, citing the new
   ids.
4. Apply the permitted `status`/`recheck`/`used-by` cell edits, and write the exact old→new
   log in `round-26.md`.
5. Write the Gate receipt table and the STALE→superseding map in `round-26.md`.
6. Run the census; E11 requires every `mined` used-by path to exist, so steps 2-5 must precede
   the census.

Do not claim C1 until step 6 and the measure command pass.

---

## 8. Gate (`corpus/lessons/round-26.md`) — what L1 must record

### 8.1 Receipt table (32 rows, one row per population id)

Columns: `id | status class | verdict | fetchIndex | quote | anchorObserved | reason |
superseding row | correction block`.

Validation rules:

- Exactly the 32 population ids: S001-S013, S015-S018, S020-S034. No S014/S019/S035.
- Verdict ∈ HOLD/STALE/UNVERIFIABLE. Counts sum to 32; decided = HOLD+STALE; UNVERIFIABLE
  listed separately and never in the numerator.
- `fetchIndex` must be valid for that row's `population.json.fetches`:
  - S001, S002: 1 or 2; a single receipt quote may ground only one of the two URLs. Record
    the other fetch's comparison separately so the composite teaching is not implied
    unexamined;
  - S008: index 1, but the successful evidence is `S008-1-retry.raw.gz`
    (sha256 `93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084`, 512,359
    bytes). The failed first attempt `S008-1.raw.gz` is an empty-body timeout artifact
    (sha256 `e3b0c442…b855`); it is not evidence and must not be quoted;
  - all others: 1.
- Quote: 6-25 whitespace words, normalized to single spaces, exact substring of
  `fetched/text/S0NN-N.txt`, word-bounded. Mechanical check:

```python
q = ' '.join(quote.split())
t = open(f'.ufo/waves/round-26/fetched/text/{rid}-{idx}.txt', encoding='utf-8').read()
i = t.find(q)
assert 6 <= len(q.split()) <= 25 and i >= 0
assert i == 0 or not (t[i-1].isalnum() or t[i-1] == '_')
j = i + len(q)
assert j == len(t) or not (t[j].isalnum() or t[j] == '_')
```

- `anchorObserved` must name a heading/section or a line that resolves in the text file. A
  bare "page" or "fetched 200" is not an anchor.
- `reason` must name the row's own scope/teaches and say what the re-fetched bytes show. HTTP
  200/sha256 alone is not a verdict. A `HOLD` reason says why the teaching still holds; a
  `STALE` reason says exactly what changed; an `UNVERIFIABLE` reason says why the bytes cannot
  decide.
- `correction` is `null` for HOLD/UNVERIFIABLE; nonempty for STALE.

### 8.2 New-row grounding (contract rule 1)

For every new row, the Gate records the URL, access date, and a ≤25-word quote with its
location grounding the corrected `teaches` (`../CORPUS.md:112-115`). The quote must be from
the same retained text file as the receipt. A heading or doclink is not a grounding quote.
The Gate must also list the old→new id pair and the correction-block path.

### 8.3 Cell-change log

One row per changed cell, exact values:

```text
| id | cell | old | new | reason | evidence |
| S003 | recheck | 90d | 2027-01-19 | 90d from 2026-10-21 receipt; opened 2026-10-19 gave 2027-01-17 | RowS003.md HOLD |
```

No log row is needed for unchanged cells. The log is the contract's "logged old→new in the
round lesson" (`../CORPUS.md:116-118`). The SOURCES EOF note, if any, does not replace it.

### 8.4 Search log

A recheck is not a new bounded search. Do not add the 32 rows to the Search log's
"included" count; "included" means retained as a registry row, not re-opened. If L1 adds a
note, use a plain EOF paragraph after the existing S030 note (`corpus/SOURCES.md:102`), never
a row-shaped line (E12), and state "rechecked 32; new rows N; no new search population".

---

## 9. Pre-commit verification for L1

Run only after all edits, from the lane root. These are read-only checks; they are listed for
L1, not executed by this seat.

### 9.1 Only the three cells changed

```python
import re, subprocess
base = '97404de4ff73d6c8a4f87385cf5fdf36dca7f006'  # contract baseline
b = subprocess.check_output(['git', 'show', f'{base}:corpus/SOURCES.md'], text=True)
h = open('corpus/SOURCES.md', encoding='utf-8').read()
def rows(t):
    d = {}
    for line in t.splitlines():
        if re.match(r'^\|\s*S\d{3,}\s*\|', line):
            c = [x.strip() for x in line.split('|')[1:-1]]
            d[c[0]] = c
    return d
B, H = rows(b), rows(h)
ALLOWED = {7, 9, 10}  # status, recheck, used-by (0-based)
bad = 0
for i in sorted(set(B) & set(H)):
    for j, (x, y) in enumerate(zip(B[i], H[i])):
        if x != y and j not in ALLOWED:
            print('ILLEGAL', i, j, repr(x), '->', repr(y)); bad += 1
for i in sorted(set(H) - set(B)): print('NEW', i)
for i in sorted(set(B) - set(H)): print('REMOVED', i); bad += 1
print('illegal', bad)
```

Expected: `NEW S036…` only; `REMOVED` none; `illegal 0`. `NEW` rows are permitted because the
contract's correction vehicle is a new row; the script separates them from cell edits.

### 9.2 Prior bytes preserved in knowledge/lessons

```sh
git diff --numstat 97404de4ff73d6c8a4f87385cf5fdf36dca7f006 -- corpus/knowledge corpus/lessons \
  | awk '$2 != 0 {print "DELETIONS", $0}'
```

Expected: no `DELETIONS` lines. New `round-26.md` has `N 0`; existing entries with EOF blocks
have `N 0`. If a table or frontmatter line shows deletions, the append-only ruling is broken.

### 9.3 SOURCES shape and enums

```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
```

Expected: row count = 35 + number of new rows; malformed `0`; duplicate ids empty. The frozen
census examples are at `../CORPUS.md:135-147`.

### 9.4 Fleet census

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin kake
```

Baseline (before edits) is only the inherited warning:

```text
kake  W04  S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake  ok   /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
exit=0
```

Expected after edits: no E01-E12; the same W04 is acceptable as inherited; if a new row
duplicates a URL+scope, its `teaches` must contain `supersedes S…` (E04 exemption at
`scripts/sources-census.sh:646-649`). W01 (tier-C mined with used-by) and W03 (mined with
`used-by: —`) are warnings but should be designed out: a tier-C correction stays `queued`
with `—`, and a new row with no citation stays `queued`.

### 9.5 Recheck schedule (the proposal's witness)

Red-before / green-after with a future `--today`:

```sh
scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin kake --today 2027-01-17
```

Before: S003-S007/S013/S015-S017 report `overdue` at 0d from `opened=2026-10-19`, even though
they were rechecked on 2026-10-21. After setting the 21 ISO dates: those rows do not appear
overdue on 2027-01-17; they first become due on 2027-01-19. S014 (excluded from this round)
still appears, because its own recheck was not performed; that is correct, not a regression.
Also run plain `overdue` (today) to confirm no unintended overdue line appears and the
`cadence` lines for `on-release` remain.

### 9.6 Measure command

```sh
python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>
```

`measure.py` is absent at the time of this report. Do not report C1 as measured until it
exists and its output derives the decided count from the 32 receipts, not from a declared
total. The numerator must be HOLD+STALE over 32; UNVERIFIABLE separately; every STALE must
resolve to a new row and a tagged block.

---

## 10. One non-obvious proposal (bounded)

**Proposal: make the completed recheck visible to the fleet scheduler by advancing the
`recheck` cell to an explicit next-due ISO date for the rows in §5.2 (21 on the observed
all-HOLD set; recompute for the pending S012/S030 verdicts); leave every other in-population
row (11 on the observed set), all STALE old rows, all UNVERIFIABLE rows, and all excluded rows
unchanged.**

Affected axes: **operability** (the overdue queue currently ignores the recheck and keeps
due-dating from `opened`) and **freshness** (the next check is scheduled from the actual
observation, not the original open date). The contract selects freshness because operability
was not worked in round 25; this move advances the selected axis while also moving the tied
operability axis, without a contract amendment. Contract/substrate/verification are unharmed:
the change uses a cell contract v1 explicitly permits, is logged old→new, preserves every
frozen cell and every prior byte, and is exercised by the existing census tool.

Why it is non-obvious: the intuitive integration is "no cell changes on HOLD" or "change
`status` to show rechecked". The first leaves the fleet scheduler permanently anchored to
`opened`; the second is illegal because `status` has no "rechecked"/"retired" value and would
contradict the frozen `teaches`. The `recheck` ISO-date branch is the only legal, observable
clock, and its necessity is visible only by reading the census's overdue implementation and
running it with a future `--today`.

Risks:

- Mass-editing all 35 rows, including excluded S014/S019/S035: do not; scope is the 32
  in-population rows and only decided HOLD rows.
- Advancing an UNVERIFIABLE or STALE old row: do not; that would hide debt or schedule a
  retired source.
- Off-by-one date arithmetic: use UTC receipt date 2026-10-21 and the exact table in §5.2;
  the log states the cadence so the interval is auditable.
- A future tool expecting only cadences: E09 accepts ISO dates; `overdue` treats an ISO date
  as the due date. Document the semantics in the Gate.
- Confusing `recheck` (next due) with `opened` (historical open): never edit `opened`.

Verification: §9.5 red-before/green-after with `--today 2027-01-17`; §9.4 validate clean;
§9.1 illegal=0; §9.2 no deletions; the Gate has 21 exact log rows.

---

## 11. Explicit contradictions and edge cases L1 must not smooth

1. **A moved anchor with the same content is HOLD, but `anchor` is frozen.** The receipt
   contract says HOLD with `anchorObserved` noting the move; contract v1 says `anchor` cannot
   change in place. Resolution: record the move in the Gate and, only if the literal locator
   is now unfollowable, append a plain precision paragraph (precedent S030 note). Do not
   create a superseding row for a pure move; that would misclassify HOLD as STALE.
2. **No `retired`/`superseded` status exists.** Do not invent one and do not use `rejected`.
   The new row's `supersedes S0NN —` prefix is the relation. The old row keeps its historical
   status and `used-by`. The census's `overdue` mode does not read the prefix, so a retired
   row can still appear in the overdue queue; do not mask it with a fake date. A future
   population/queue builder should exclude ids named by a later row's supersedes prefix.
3. **`recheck` cadence vs. `opened` clock.** Contract v1 calls `recheck` "ISO date or cadence";
   the census anchors `NNd` to `opened`. The proposal uses the ISO branch to resolve this
   without touching `opened` or amending the contract.
4. **S001/S002 have two fetches.** A single `fetchIndex` quote grounds one URL, not the
   composite teaching. The Gate must record both halves; do not infer the unquoted half from
   the quoted half.
5. **S008 has a failed first attempt.** The retry blob is the evidence; the empty first blob
   is not. The population entry already points to the retry file; use population, not a naive
   "first manifest entry with index 1".
6. **`measure.py` is absent.** The contract's count command cannot run yet. Do not substitute
   a hand count or a row-seat tally for the measured count.
7. **The census E04 exemption is looser than the contract.** It only requires `supersedes
   S\d{3}` anywhere in `teaches`; the contract requires the exact opening prefix. Follow the
   contract, not the parser's looser check.
8. **A tier-C flip is not an admission.** If S017's flip is met by Astro's own changed text,
   the new row is still tier C and cannot be sole support for an admitted knowledge claim; a
   tier-A source must be opened for that. If only DebugBear changes its Firefox number (S018),
   the flip condition ("a tier-A source confirms its number") is still unmet; the new row
   remains rejected.

---

## 12. Do-not list (quick)

- Do not edit any frozen cell: `id source kind tier scope anchor teaches opened`.
- Do not insert new rows beside old rows; append after S035.
- Do not create a row for HOLD.
- Do not flip a stale row's status or clear its `used-by`.
- Do not add `round-26.md` to a HOLD row's `used-by`.
- Do not rewrite `verified-at:` or any frontmatter line.
- Do not edit a historical lesson; append to `round-26.md`.
- Do not split a table or insert lines above existing content.
- Do not use absence vocabulary in a correction block.
- Do not put `|` in a cell or a row-shaped line outside the Registry.
- Do not relabel UNVERIFIABLE as HOLD; do not advance its recheck.
- Do not touch S014/S019/S035 recheck cells.
- Do not claim C1 measured while `measure.py` is absent.

---

## Appendix A — current mutable cells for the 32 in-population rows

Shorthand: K-served = `corpus/knowledge/ghp-served-set.md`; K-domain =
`corpus/knowledge/ghp-custom-domain.md`; K-etag = `corpus/knowledge/ghp-etag-anatomy.md`;
K-crawl = `corpus/knowledge/crawl-scope-per-host.md`; K-canon =
`corpus/knowledge/static-canonical-preflight.md`; L22/L23/L24 = `corpus/lessons/round-22.md`,
`round-23.md`, `round-24.md`.

| id(s) | status | recheck | used-by | due old → new (HOLD case) |
|---|---|---|---|---|
| S001, S002 | mined | on-release | K-served | no change |
| S003 | mined | 90d | K-domain, K-served | 2027-01-17 → 2027-01-19 |
| S004, S006 | mined | 90d | K-served | 2027-01-17 → 2027-01-19 |
| S005, S007 | mined | 90d | K-domain | 2027-01-17 → 2027-01-19 |
| S008 | mined | 365d | K-served | 2027-10-19 → 2027-10-21 |
| S009, S010 | mined | 365d | K-etag | 2027-10-19 → 2027-10-21 |
| S011, S012 | mined | 365d | K-crawl | 2027-10-19 → 2027-10-21 |
| S013 | mined | 90d | K-crawl | 2027-01-17 → 2027-01-19 |
| S015, S016 | queued | 90d | — | 2027-01-17 → 2027-01-19 |
| S017 | rejected | 90d | — | 2027-01-17 → 2027-01-19 |
| S018 | rejected | 180d | — | 2027-04-17 → 2027-04-19 |
| S020 | mined | 365d | K-canon, L22 | 2027-10-20 → 2027-10-21 |
| S021 | mined | 90d | K-canon, L22 | 2027-01-18 → 2027-01-19 |
| S022-S025 | mined | 90d | L22 | 2027-01-18 → 2027-01-19 |
| S026, S027 | mined | on-release | K-canon, L22 | no change |
| S028, S029 | mined | 365d | K-canon, L22 | no change (opened 2026-10-21) |
| S030, S031 | mined | 90d | K-canon, L23 | no change (opened 2026-10-21) |
| S032-S034 | mined | 365d | K-canon, L24 | no change (opened 2026-10-21) |

Count check on the observed all-HOLD case (S012/S030 pending): 21 rows in the "due old → new"
change set; 7 rows opened 2026-10-21 with numeric cadences already correct; 4 rows
on-release; total 32. A pending row that lands STALE/UNVERIFIABLE leaves the change set and
is handled per §2.2/§2.3.

## Appendix B — receipt-path quirks

- 34 population fetch entries for 32 rows: S001 and S002 have indices 1 and 2; all others
  index 1. All 34 population entries are status 200.
- `fetched/manifest.json` has 34 entries: 33 status-200 entries plus S008's failed first
  attempt (status null, empty body). `fetched/manifest-retry.json` records the successful
  S008 retry (512,359 bytes, sha256 `93281a63…6084`). Total attempts: 35 (34 successful, 1
  timeout).
- Text views are one normalized line for HTML and RFC pages in most cases; anchor line numbers
  from the raw bytes are not line numbers in the text view. Quote binding uses the text view;
  anchor movement may be described by heading/character offset.
- `fetched/manifest.json` includes the failed S008 entry with `status: null` and the empty-body
  sha; `population.json` correctly points S008 to `S008-1-retry.raw.gz`. Prefer population.
