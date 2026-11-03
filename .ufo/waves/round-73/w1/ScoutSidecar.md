# ScoutSidecar Seat Report (Round 73, Wave w1)

## Executive Summary
- **Seat**: `ScoutSidecar` (leaf member, godspeed posture, read-only lane checkout, scratch-only work)
- **Base Revision**: `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`
- **Tool Installs**: None (Node.js v24.21.0, Python 3.14.3, and Git already available on host; no pacman transactions executed)
- **Scratch Path**: `/fast/scratch/hyaku/kake-r73/ScoutSidecar/`

---

## 1. Baseline Freshness Sweep at Base Revision

Cloned the lane at base revision `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc` into scratch tree:
```bash
git clone --shared -q /home/vgpnk/Projects/shokunin/kake-shokunin "$S/clone" && git -C "$S/clone" checkout -q c1f3d8d4ed9470ecbaaf3353952a374b079e68cc
```

Ran offline freshness sweep:
```bash
node scripts/freshness-sweep.mjs --offline
```
- **Exit code**: `2`
- **Stderr first line**:
  ```
  freshness-sweep: Error: paths sidecar binding invalid: corpus/SOURCES.md:140
  ```
- **Stdout**: (empty)

---

## 2. Sidecar Entry Enumeration at Base

Enumerated all 174 entries of `corpus/knowledge/freshness-sidecar.json` (`data.entries[]`) against the base files by splitting target file on `\n`, taking `line = lines[entry.line - 1]`, and computing SHA-256 over its UTF-8 bytes.

- **Total entries evaluated**: 174
- **Entries where `lineSha256 !== sha256(line)`**: exactly 1 entry (at array index 142)

### Mismatching Entry Details
- **file**: `corpus/SOURCES.md`
- **line**: `140`
- **token**: `~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md`
- **kind**: `absent`
- **date**: `2026-10-31`
- **lineSha256 (full in base sidecar)**: `b3315f41997ae6881726be2a5258f3dc2ae815cde7e3a166617322caed4a8a47`
- **note**: `2026-10-31: ~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md absent on this host — an old-host home path; the Windows host migration removed every former home tree, so this target does not exist on the current machine. Citation corpus/SOURCES.md:140 is a historical record, not an executable instruction.`

---

## 3. Computed SHA-256 of Base Line 140

Base line 140 of `corpus/SOURCES.md` (782 UTF-8 bytes):
```markdown
| S132 | Checking self-assessment statements at writing (kama round 29, adjacency import) — /home/vgpnk/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md | own-work | A | Fleet-internal calibration method: self-assessment statements (SCORECARD and SHONEN lines) checked against the committed tree at their writing revision, not only at tip | §"Checking self-assessment statements at writing", first paragraph; opened 2026-10-23 | supersedes S130 — a self-assessment is checked against the committed tree/history at its writing revision, not only at the current tip; the quoted calibration-error statement is in the first section-prose paragraph. | mined | 2026-10-23 | on-use | corpus/lessons/round-44.md, SCORECARD.md, corpus/lessons/round-64.md |
```

- **Computed SHA-256**: `4e4081310d6ad17268d8120a29b0400c0edbe6fcee0c035af7c9341acc732e15`
- (This is the value the entry should carry).

---

## 4. Freshness Sweep Run with Re-Pinned Entry (Scratch Clone Only)

In the scratch clone only, updated `lineSha256` of that single entry to `4e4081310d6ad17268d8120a29b0400c0edbe6fcee0c035af7c9341acc732e15`, with no other changes to the sidecar.

Ran offline sweep:
```bash
node scripts/freshness-sweep.mjs --offline
```
- **Exit code**: `1`
- **Section status lines**:
  - `§paths  191 files · 708 occurrences · 107 unique tokens`
  - `§history  SUSPENDED — probe-history source absent by declaration (pins.probeHistoryAbsent): /home/vgpnk/Projects/webzites/state/probe-history.jsonl — section suspended until a history source is re-anchored`
  - `§armed`
    `  all remote checks skipped(offline) — NOT counted as pass (complete=false)`
  - Summary: `skipped(offline): §armed (all remote checks) · §history (probe-history source absent — pin-declared) — complete=false, never counted as pass`
  - Verdict: `VERDICT: DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet (exit 1, partial: offline)`
- **Error: lines**: None (0 `Error:` lines on stdout or stderr; stderr was empty).
- **SUSPENDED lines**:
  ```
  §history  SUSPENDED — probe-history source absent by declaration (pins.probeHistoryAbsent): /home/vgpnk/Projects/webzites/state/probe-history.jsonl — section suspended until a history source is re-anchored
  ```
- **could-not lines**: None.

---

## 5. Hermetic Selftest

Ran selftest with isolated directories under scratch tree:
```bash
env HOME="$S/home" KAKE_SELFTEST_DIR="$S/selftest" node "$S/clone/scripts/freshness-sweep.mjs" --selftest
```
- **Environment variable names and shapes**:
  - `HOME`: directory path string (`/fast/scratch/hyaku/kake-r73/ScoutSidecar/home`)
  - `KAKE_SELFTEST_DIR`: directory path string (`/fast/scratch/hyaku/kake-r73/ScoutSidecar/selftest`)
- **Exit code**: `0`
- **Pass count**: `36/36 passed` (0 failed)
- **Key output line**: `selftest: 36/36 passed`

---

## 6. Verdict and Sidecar Validation Analysis

### Verdict
- **Verdict**: `exit 1` (evaluable with named drift, clean of `Error:`)
- **Named Finding(s)**:
  - `DRIFT 1 cited path(s) missing with unannotated citation(s):`
    `~/projects (5 of 24 cites unannotated: corpus/lessons/round-66-verifier-spotcheck.md:101, corpus/lessons/round-66-verifier-spotcheck.md:102, corpus/lessons/round-66.md:69, …)`
  - `set-delta miss: !! NEW MISS ~/projects`

### Sweep Source Conditions (`scripts/freshness-sweep.mjs` lines 360–394)
In `loadPathSidecar(repoRoot)`:
1. **Container Schema Checks** (lines 363–364):
   - File `corpus/knowledge/freshness-sidecar.json` exists, JSON-parses, `data.schema === 'kake-paths-sidecar-v1'`, and `Array.isArray(data.entries)`.
2. **Entry Field / Structural Checks** (lines 367–377, throws `paths sidecar invalid entry`):
   - `e` is an object (line 367).
   - `typeof e.file === 'string'` and `(e.file === 'SKILL.md' || /^corpus\/.+\.md$/.test(e.file))` (lines 367–368).
   - `!e.file.split('/').some(part => part === '.' || part === '..' || !part)` (line 369).
   - `Number.isSafeInteger(e.line) && e.line >= 1` (line 370).
   - `typeof e.token === 'string' && canonHome(e.token) === e.token` (canonical home starts with `~`, not `/home/vgpnk/`) (line 371).
   - `typeof e.lineSha256 === 'string' && /^[0-9a-f]{64}$/.test(e.lineSha256)` (line 372).
   - `['absent', 'restored'].includes(e.kind)` (line 373).
   - `typeof e.date === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(e.date)` (line 374).
   - `!Number.isNaN(Date.parse(e.date)) && new Date(e.date).toISOString().slice(0, 10) === e.date` (valid calendar date) (line 375).
   - `typeof e.note === 'string' && e.note.includes(e.date)` (line 376).
3. **Content and Line-Binding Checks** (lines 378–388, throws `paths sidecar binding invalid: ${e.file}:${e.line}`):
   - `line = lines[e.line - 1]` exists (`line !== undefined`) (lines 379, 384).
   - `sha256(line) === e.lineSha256` (line 384).
   - `tokens = [...line.matchAll(PATH_RE)].flatMap(...)` contains `e.token` (`tokens.includes(e.token)`) (lines 380–382, 384).
   - If `e.kind === 'absent'`:
     - `prose = e.note.replace(PATH_RE, '\u00abcite\u00bb')` matches `ABSENT_RE` (lines 383, 385).
     - `e.note.includes('historical record, not an executable instruction')` (line 386).
   - If `e.kind === 'restored'`:
     - `!ABSENT_RE.test(prose)` (line 387).
4. **Duplicate Prevention** (lines 389–391, throws `paths sidecar duplicate: ${key}`):
   - Key `${e.file}:${e.line}:${e.token}` must be unique.

### Re-pinned Entry Compliance Status
The entry `corpus/SOURCES.md:140` meets **every single one** of these conditions:
- `file`: `"corpus/SOURCES.md"` matches `/^corpus\/.+\.md$/` with no relative path escapes (lines 368–369).
- `line`: `140` is a safe integer >= 1 (line 370).
- `token`: `"~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md"` is a canonical home path (line 371).
- `lineSha256`: `"4e4081310d6ad17268d8120a29b0400c0edbe6fcee0c035af7c9341acc732e15"` is a valid 64-char hex string (line 372).
- `kind`: `"absent"` is an allowed kind (line 373).
- `date`: `"2026-10-31"` is a valid calendar date matching its ISO representation (lines 374–375).
- `note`: string containing `"2026-10-31"` (line 376).
- Line existence: line 140 exists in `corpus/SOURCES.md` (lines 378–379, 384).
- SHA-256 binding: `sha256(line)` equals `4e4081310d6ad17268d8120a29b0400c0edbe6fcee0c035af7c9341acc732e15` (line 384).
- Token binding: `tokens` extracted from line 140 contains `~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md` (extracted from `/home/vgpnk/Projects/...` via `canonHome`) (lines 381, 384).
- Absence prose & formula: `ABSENT_RE.test(prose)` is true (contains "absent on this host") and `e.note` contains `"historical record, not an executable instruction"` (lines 385–386).
- Uniqueness: key `corpus/SOURCES.md:140:~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md` is unique across the sidecar (lines 389–391).

Thus, prior to re-pinning, the entry violated **only** the `sha256(line) !== e.lineSha256` binding check on line 384 (due to the `used-by` cell appended in commit `84dcc841`). With the updated SHA-256, it satisfies every condition of the contract.
