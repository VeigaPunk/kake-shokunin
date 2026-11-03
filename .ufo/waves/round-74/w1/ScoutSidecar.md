# ScoutSidecar — round 74, wave w1: `corpus/knowledge/freshness-sidecar.json` at base

Measured revision `ced2878a1e77f57afb4ee3baebf1021e5130399b` (lane `kake-shokunin`, `git show <rev>:<path>` for every byte). Sidecar blob `0e7b11094e8a77bff16f5b2a02c0360145d94322`, 103243 bytes, sha256 `9ecfdf2b3a1772198ebdf47f521ad28c4f7176c30469a17063da95a035dfba9f`. Lane worktree is identical to base for the target (`git diff base -- corpus/knowledge/freshness-sidecar.json` empty; `git hash-object` == blob id).

Probe: `os.stat(HOME + token[1:])` with `HOME=/home/vgpnk`; `FileNotFoundError`/`NotADirectoryError` → absent, any other `OSError` → unevaluable. Enumeration receipt: `w1/ScoutSidecar/enumeration.txt` (174 rows, one per entry); probe source `w1/ScoutSidecar/scout_sidecar_enum.py`.

## (1) Enumeration and base-number reproduction

- total entries: **174**; kinds: **absent=148**, **restored=26**.
- host state matrix: absent→present **144**, absent→absent **4**, absent→unevaluable **0**; restored→present **26**, restored→absent **0**, restored→unevaluable **0**.
- contradictions (kind=absent, host=present): **144**.

Control `controls/base-c2-sidecar.txt` states `entries=174 absent=148 restored=26 absent_present=144 absent_absent=4 absent_unevaluable=0 restored_present=26 restored_absent=0 restored_unevaluable=0 contradictions=144 met=false`, `genuinely_absent_tokens=3` (2/1/1). **Every one of those numbers reproduces exactly; delta = 0.** No counter exists at base (`c74_sidecar_reobserve.py` and `scripts/sidecar_reobserve.py` are both absent), so this is an independent re-derivation, not a replay.

### Entries whose kind and host state disagree (144)

All 144 disagreements are `kind=absent` over a token that `stat`s fine on this host. There is no `kind=restored` over an absent token.

```
corpus/lessons/round-29-verifier-spotcheck.md:190	~/.local/bin/time
corpus/lessons/round-29-verifier-spotcheck.md:191	~/.local/bin/time
corpus/lessons/round-29.md:200	~/.local/bin/time
corpus/lessons/round-29-verifier-spotcheck.md:194	~/.omp/agent/RULES.md
corpus/lessons/round-50-verifier-spotcheck.md:55	~/.omp/agent/RULES.md
SKILL.md:512	~/Projects/ds4cc-marketplace
SKILL.md:513	~/Projects/ds4cc-marketplace
SKILL.md:514	~/Projects/ds4cc-marketplace
SKILL.md:515	~/Projects/ds4cc-marketplace
SKILL.md:516	~/Projects/ds4cc-marketplace
SKILL.md:517	~/Projects/ds4cc-marketplace
SKILL.md:518	~/Projects/ds4cc-marketplace
SKILL.md:815	~/Projects/ds4cc-marketplace
SKILL.md:935	~/Projects/ds4cc-marketplace
corpus/SOURCES.md:70	~/Projects/ds4cc-marketplace
corpus/SOURCES.md:73	~/Projects/ds4cc-marketplace
corpus/knowledge/fleet-registry.md:110	~/Projects/ds4cc-marketplace
corpus/knowledge/origin-repos.md:93	~/Projects/ds4cc-marketplace
corpus/knowledge/origin-repos.md:94	~/Projects/ds4cc-marketplace
corpus/knowledge/origin-repos.md:95	~/Projects/ds4cc-marketplace
corpus/knowledge/publish-channels.md:80	~/Projects/ds4cc-marketplace
corpus/knowledge/publish-channels.md:90	~/Projects/ds4cc-marketplace
corpus/knowledge/render-web-services.md:108	~/Projects/ds4cc-marketplace
corpus/knowledge/render-web-services.md:5	~/Projects/ds4cc-marketplace
corpus/knowledge/render-web-services.md:52	~/Projects/ds4cc-marketplace
corpus/knowledge/render-web-services.md:73	~/Projects/ds4cc-marketplace
corpus/knowledge/sitemap-orphan-audit.md:187	~/Projects/ds4cc-marketplace
corpus/lessons/round-18.md:107	~/Projects/ds4cc-marketplace
corpus/lessons/round-30-verifier-spotcheck.md:222	~/Projects/ds4cc-marketplace
corpus/lessons/round-32-verifier-spotcheck.md:106	~/Projects/ds4cc-marketplace
corpus/lessons/round-32-verifier-spotcheck.md:68	~/Projects/ds4cc-marketplace
corpus/lessons/round-32.md:31	~/Projects/ds4cc-marketplace
SKILL.md:519	~/Projects/ds4cc-marketplace/burnerchrome
SKILL.md:520	~/Projects/ds4cc-marketplace/burnerchrome
SKILL.md:521	~/Projects/ds4cc-marketplace/burnerchrome
corpus/knowledge/fleet-registry.md:111	~/Projects/ds4cc-marketplace/burnerchrome
corpus/knowledge/fleet-registry.md:112	~/Projects/ds4cc-marketplace/burnerchrome
corpus/knowledge/mirror-pitfalls.md:72	~/Projects/ds4cc-marketplace/speedrun
corpus/knowledge/speedrun-pipeline.md:90	~/Projects/ds4cc-marketplace/speedrun
corpus/knowledge/speedrun-pipeline.md:91	~/Projects/ds4cc-marketplace/speedrun
corpus/knowledge/speedrun-pipeline.md:92	~/Projects/ds4cc-marketplace/speedrun
corpus/knowledge/speedrun-pipeline.md:93	~/Projects/ds4cc-marketplace/speedrun
corpus/SOURCES.md:27	~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md
corpus/lessons/round-18.md:74	~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md
corpus/lessons/round-21.md:39	~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md
corpus/lessons/round-55-verifier-spotcheck.md:61	~/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge
corpus/lessons/round-21-verifier-spotcheck.md:95	~/Projects/shokunin
corpus/lessons/round-21.md:177	~/Projects/shokunin
corpus/lessons/round-22-verifier-spotcheck.md:134	~/Projects/shokunin
corpus/lessons/round-22.md:200	~/Projects/shokunin
corpus/lessons/round-24.md:113	~/Projects/shokunin
corpus/lessons/round-25.md:240	~/Projects/shokunin
corpus/lessons/round-26-verifier-spotcheck.md:97	~/Projects/shokunin
corpus/lessons/round-28-verifier-spotcheck.md:172	~/Projects/shokunin
corpus/lessons/round-28.md:75	~/Projects/shokunin
corpus/lessons/round-29-verifier-spotcheck.md:125	~/Projects/shokunin
corpus/lessons/round-30-verifier-spotcheck.md:141	~/Projects/shokunin
corpus/lessons/round-31-verifier-spotcheck.md:136	~/Projects/shokunin
corpus/lessons/round-32-verifier-spotcheck.md:100	~/Projects/shokunin
corpus/lessons/round-33-verifier-spotcheck.md:148	~/Projects/shokunin
corpus/lessons/round-34-verifier-spotcheck.md:189	~/Projects/shokunin
corpus/lessons/round-35-verifier-spotcheck.md:38	~/Projects/shokunin
corpus/lessons/round-36-verifier-spotcheck.md:133	~/Projects/shokunin
corpus/lessons/round-37-verifier-spotcheck.md:117	~/Projects/shokunin
corpus/lessons/round-37-verifier-spotcheck.md:25	~/Projects/shokunin
corpus/lessons/round-38-verifier-spotcheck.md:148	~/Projects/shokunin
corpus/lessons/round-38-verifier-spotcheck.md:24	~/Projects/shokunin
corpus/lessons/round-39-verifier-spotcheck.md:135	~/Projects/shokunin
corpus/lessons/round-40-verifier-spotcheck.md:138	~/Projects/shokunin
corpus/lessons/round-41-verifier-spotcheck.md:128	~/Projects/shokunin
corpus/lessons/round-45-verifier-spotcheck.md:55	~/Projects/shokunin
corpus/lessons/round-47-verifier-spotcheck.md:66	~/Projects/shokunin
corpus/lessons/round-49-verifier-spotcheck.md:72	~/Projects/shokunin
corpus/lessons/round-50-verifier-spotcheck.md:198	~/Projects/shokunin
corpus/lessons/round-51-verifier-spotcheck.md:121	~/Projects/shokunin
corpus/lessons/round-51-verifier-spotcheck.md:15	~/Projects/shokunin
corpus/lessons/round-52-verifier-spotcheck.md:20	~/Projects/shokunin
corpus/lessons/round-54-verifier-spotcheck.md:48	~/Projects/shokunin
corpus/lessons/round-55-verifier-spotcheck.md:68	~/Projects/shokunin
corpus/lessons/round-56-verifier-spotcheck.md:52	~/Projects/shokunin
corpus/lessons/round-57-verifier-spotcheck.md:92	~/Projects/shokunin
corpus/lessons/round-57.md:79	~/Projects/shokunin
corpus/lessons/round-58-verifier-spotcheck.md:60	~/Projects/shokunin
corpus/lessons/round-59-verifier-spotcheck.md:107	~/Projects/shokunin
corpus/lessons/round-60-verifier-spotcheck.md:87	~/Projects/shokunin
corpus/lessons/round-62-verifier-spotcheck.md:44	~/Projects/shokunin
corpus/lessons/round-62.md:23	~/Projects/shokunin
corpus/lessons/round-63-verifier-spotcheck.md:107	~/Projects/shokunin
corpus/lessons/round-63.md:69	~/Projects/shokunin
corpus/lessons/round-64-verifier-spotcheck.md:43	~/Projects/shokunin
corpus/lessons/round-64.md:106	~/Projects/shokunin
corpus/lessons/round-29.md:128	~/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md
corpus/QUALITY.md:649	~/Projects/shokunin/.ufo/reports/round-33/kake.md
corpus/lessons/round-34.md:67	~/Projects/shokunin/.ufo/reports/round-33/kake.md
corpus/lessons/round-54-verifier-spotcheck.md:6	~/Projects/shokunin/.ufo/reports/round-54/kake.md
corpus/lessons/round-55-verifier-spotcheck.md:6	~/Projects/shokunin/.ufo/reports/round-55/kake.md
corpus/lessons/round-44-verifier-spotcheck.md:5	~/Projects/shokunin/kake-shokunin
corpus/lessons/round-45-verifier-spotcheck.md:5	~/Projects/shokunin/kake-shokunin
corpus/lessons/round-60-verifier-spotcheck.md:5	~/Projects/shokunin/kake-shokunin
corpus/lessons/round-64-verifier-spotcheck.md:10	~/Projects/shokunin/kake-shokunin
corpus/lessons/round-64-verifier-spotcheck.md:27	~/Projects/shokunin/kake-shokunin
SKILL.md:442	~/Projects/shokunin/kake-shokunin/SKILL.md
SKILL.md:476	~/Projects/shokunin/kake-shokunin/SKILL.md
SKILL.md:477	~/Projects/shokunin/kake-shokunin/SKILL.md
corpus/lessons/round-21-verifier-spotcheck.md:96	~/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
corpus/lessons/round-21.md:178	~/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
corpus/lessons/round-22-verifier-spotcheck.md:135	~/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
corpus/lessons/round-24.md:114	~/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
corpus/lessons/round-24.md:117	~/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
corpus/lessons/round-25.md:245	~/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
corpus/lessons/round-26-verifier-spotcheck.md:99	~/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
corpus/SOURCES.md:138	~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md
corpus/SOURCES.md:140	~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md
corpus/lessons/round-44.md:10	~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md
corpus/lessons/round-21-verifier-spotcheck.md:95	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-21.md:177	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-22-verifier-spotcheck.md:134	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-24.md:113	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-25.md:240	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-26-verifier-spotcheck.md:97	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-28-verifier-spotcheck.md:172	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-31-verifier-spotcheck.md:136	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-35-verifier-spotcheck.md:38	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-37-verifier-spotcheck.md:116	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-38-verifier-spotcheck.md:147	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-45-verifier-spotcheck.md:55	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-47-verifier-spotcheck.md:66	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-49-verifier-spotcheck.md:72	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-50-verifier-spotcheck.md:198	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-55-verifier-spotcheck.md:68	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-57-verifier-spotcheck.md:92	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-57.md:79	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-62.md:23	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-63-verifier-spotcheck.md:107	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-63.md:69	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-64-verifier-spotcheck.md:43	~/Projects/shokunin/scripts/sources-census.sh
corpus/lessons/round-64.md:106	~/Projects/shokunin/scripts/sources-census.sh
corpus/SOURCES.md:137	~/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md
corpus/SOURCES.md:139	~/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md
corpus/lessons/round-44.md:9	~/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md
corpus/SOURCES.md:137	~/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/ReviewFreeze.md
corpus/SOURCES.md:139	~/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/ReviewFreeze.md
corpus/lessons/round-44.md:9	~/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/ReviewFreeze.md
corpus/lessons/round-22-verifier-spotcheck.md:94	~/Projects/ufo-fsd-alpha
```

Contradicted entries per token (20 distinct tokens):

| n | token |
|---|---|
| 45 | `~/Projects/shokunin` |
| 27 | `~/Projects/ds4cc-marketplace` |
| 23 | `~/Projects/shokunin/scripts/sources-census.sh` |
| 7 | `~/Projects/shokunin/kake-shokunin/corpus/SOURCES.md` |
| 5 | `~/Projects/ds4cc-marketplace/burnerchrome` |
| 5 | `~/Projects/ds4cc-marketplace/speedrun` |
| 5 | `~/Projects/shokunin/kake-shokunin` |
| 3 | `~/.local/bin/time` |
| 3 | `~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` |
| 3 | `~/Projects/shokunin/kake-shokunin/SKILL.md` |
| 3 | `~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md` |
| 3 | `~/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md` |
| 3 | `~/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/ReviewFreeze.md` |
| 2 | `~/.omp/agent/RULES.md` |
| 2 | `~/Projects/shokunin/.ufo/reports/round-33/kake.md` |
| 1 | `~/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge` |
| 1 | `~/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md` |
| 1 | `~/Projects/shokunin/.ufo/reports/round-54/kake.md` |
| 1 | `~/Projects/shokunin/.ufo/reports/round-55/kake.md` |
| 1 | `~/Projects/ufo-fsd-alpha` |

## (2) The genuinely absent entries and a contradicted sample

### 4 genuinely absent entries, 3 distinct tokens (4)

- `corpus/knowledge/drift-detection.md:77` token `~/Projects/plazir-15-site` — stat `absent` (FileNotFoundError)
  - note: 2026-10-21: ~/Projects/plazir-15-site absent (test -e exit 1); exact removal time and cause unknown, earlier W7 attribution historical. Citation corpus/knowledge/drift-detection.md:77 is a historical record, not an executable instruction.
- `corpus/knowledge/fleet-registry.md:57` token `~/Projects/plazir-15-site` — stat `absent` (FileNotFoundError)
  - note: 2026-10-21: ~/Projects/plazir-15-site absent (test -e exit 1); exact removal time and cause unknown, earlier W7 attribution historical. Citation corpus/knowledge/fleet-registry.md:57 is a historical record, not an executable instruction.
- `corpus/knowledge/free-read-verbs.md:321` token `~/Projects/webzites/bin/webzites.mjs` — stat `absent` (FileNotFoundError)
  - note: 2026-10-21: ~/Projects/webzites/bin/webzites.mjs absent (test -e exit 1); exact removal time and cause unknown, earlier W7 attribution historical. Citation corpus/knowledge/free-read-verbs.md:321 is a historical record, not an executable instruction.
- `corpus/lessons/round-6-aggregator-audit.md:48` token `~/Projects/webzites/scripts/kimi-surface.mjs` — stat `absent` (FileNotFoundError)
  - note: 2026-10-21: ~/Projects/webzites/scripts/kimi-surface.mjs absent (test -e exit 1); exact removal time and cause unknown, earlier W7 attribution historical. Citation corpus/lessons/round-6-aggregator-audit.md:48 is a historical record, not an executable instruction.

Distinct absent tokens (contract's 3, counts 2/1/1 confirmed): `~/Projects/plazir-15-site` ×2, `~/Projects/webzites/bin/webzites.mjs` ×1, `~/Projects/webzites/scripts/kimi-surface.mjs` ×1. `~/Projects/webzites` does not exist at all on this host (`ls` exit 2), so both `webzites` tokens are absent by parent-directory absence.

### Sample of 10 contradicted entries (note + stat)

- `corpus/lessons/round-29-verifier-spotcheck.md:190` token `~/.local/bin/time` kind=`absent` date=`2026-10-31` → **stat present**
  - note: 2026-10-31: ~/.local/bin/time absent on this host — an old-host home path; the Windows host migration removed every former home tree, so this target does not exist on the current machine. Citation corpus/lessons/round-29-verifier-spotcheck.md:190 is a historical record, not an executable instruction.
- `corpus/lessons/round-29-verifier-spotcheck.md:191` token `~/.local/bin/time` kind=`absent` date=`2026-10-31` → **stat present**
  - note: 2026-10-31: ~/.local/bin/time absent on this host — an old-host home path; the Windows host migration removed every former home tree, so this target does not exist on the current machine. Citation corpus/lessons/round-29-verifier-spotcheck.md:191 is a historical record, not an executable instruction.
- `corpus/lessons/round-29.md:200` token `~/.local/bin/time` kind=`absent` date=`2026-10-31` → **stat present**
  - note: 2026-10-31: ~/.local/bin/time absent on this host — an old-host home path; the Windows host migration removed every former home tree, so this target does not exist on the current machine. Citation corpus/lessons/round-29.md:200 is a historical record, not an executable instruction.
- `corpus/lessons/round-29-verifier-spotcheck.md:194` token `~/.omp/agent/RULES.md` kind=`absent` date=`2026-10-31` → **stat present**
  - note: 2026-10-31: ~/.omp/agent/RULES.md absent on this host — an old-host home path; the Windows host migration removed every former home tree, so this target does not exist on the current machine. Citation corpus/lessons/round-29-verifier-spotcheck.md:194 is a historical record, not an executable instruction.
- `corpus/lessons/round-50-verifier-spotcheck.md:55` token `~/.omp/agent/RULES.md` kind=`absent` date=`2026-10-31` → **stat present**
  - note: 2026-10-31: ~/.omp/agent/RULES.md absent on this host — an old-host home path; the Windows host migration removed every former home tree, so this target does not exist on the current machine. Citation corpus/lessons/round-50-verifier-spotcheck.md:55 is a historical record, not an executable instruction.
- `SKILL.md:512` token `~/Projects/ds4cc-marketplace` kind=`absent` date=`2026-10-31` → **stat present**
  - note: 2026-10-31: ~/Projects/ds4cc-marketplace absent on this host — an old-host home path; the Windows host migration removed every former home tree, so this target does not exist on the current machine. Citation SKILL.md:512 is a historical record, not an executable instruction.
- `SKILL.md:513` token `~/Projects/ds4cc-marketplace` kind=`absent` date=`2026-10-31` → **stat present**
  - note: 2026-10-31: ~/Projects/ds4cc-marketplace absent on this host — an old-host home path; the Windows host migration removed every former home tree, so this target does not exist on the current machine. Citation SKILL.md:513 is a historical record, not an executable instruction.
- `SKILL.md:514` token `~/Projects/ds4cc-marketplace` kind=`absent` date=`2026-10-31` → **stat present**
  - note: 2026-10-31: ~/Projects/ds4cc-marketplace absent on this host — an old-host home path; the Windows host migration removed every former home tree, so this target does not exist on the current machine. Citation SKILL.md:514 is a historical record, not an executable instruction.
- `SKILL.md:515` token `~/Projects/ds4cc-marketplace` kind=`absent` date=`2026-10-31` → **stat present**
  - note: 2026-10-31: ~/Projects/ds4cc-marketplace absent on this host — an old-host home path; the Windows host migration removed every former home tree, so this target does not exist on the current machine. Citation SKILL.md:515 is a historical record, not an executable instruction.
- `SKILL.md:516` token `~/Projects/ds4cc-marketplace` kind=`absent` date=`2026-10-31` → **stat present**
  - note: 2026-10-31: ~/Projects/ds4cc-marketplace absent on this host — an old-host home path; the Windows host migration removed every former home tree, so this target does not exist on the current machine. Citation SKILL.md:516 is a historical record, not an executable instruction.

Note the uniform 2026-10-31 template across all 144: *“absent on this host — an old-host home path; the Windows host migration removed every former home tree”*. It is false for `~/Projects/shokunin` (the live fleet root), for `~/.local/bin/time` and `~/.omp/agent/RULES.md` (both present, both used by this very round), and for the lane's own `corpus/SOURCES.md`.

## (3) What a flipped entry must satisfy — `scripts/freshness-sweep.mjs` `loadPathSidecar` (base lines 359–394)

Relevant constants: `ABSENT_RE` line 133, `PATH_RE` line 136, `sha256` line 142, `normalize` line 292, `canonHome` line 356. The validator throws in three places: `paths sidecar invalid schema` (line 364), `paths sidecar invalid entry` (line 377), `paths sidecar binding invalid: <file>:<line>` (line 388), `paths sidecar duplicate: <key>` (line 390).

| # | Rule | Exact condition |
|---|---|---|
| 1 | schema | `data.schema === 'kake-paths-sidecar-v1'` and `Array.isArray(data.entries)` |
| 2 | file pattern | `e.file === 'SKILL.md'` **or** `/^corpus\/.+\.md$/`; additionally no path segment may be `''`, `'.'`, `'..'` |
| 3 | line | `Number.isSafeInteger(e.line) && e.line >= 1` |
| 4 | token spelling | `typeof e.token === 'string'` and `canonHome(e.token) === e.token`, i.e. the `~` spelling — `/home/vgpnk/...` is rejected |
| 5 | lineSha256 | 64 lowercase hex (`/^[0-9a-f]{64}$/`) **and** `sha256(line)` of the cited line (file read as utf8, `split('\n')`, 1-based) |
| 6 | token on line | the line's `PATH_RE` hits, each run through `normalize` (strip trailing `.` `,` `;` `)` `*` and trailing `/`; expand `{a,b}`/`{n..m}`) then `canonHome`, must **include** `e.token` |
| 7 | kind vocabulary | `absent` → `ABSENT_RE.test(note.replace(PATH_RE,'«cite»'))` **true** AND note contains the literal `historical record, not an executable instruction`; `restored` → the same regex must be **false** |
| 8 | date | `typeof e.date === 'string'`, `/^\d{4}-\d{2}-\d{2}$/`, `Date.parse` not NaN, and `new Date(date).toISOString().slice(0,10) === date` (rejects impossible/rolling dates) |
| 9 | note-includes-date | `e.note.includes(e.date)` — the note must contain the **entry's own** `date` string verbatim |
| 10 | uniqueness | `file:line:token` must be unique across the array |

Absence vocabulary regex (line 133, applied to the note **after** `~/`-prefixed paths are blanked to `«cite»`):

```
/absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing/i
```

Proposed new-note words, tested against that regex (Python `re.I`, same alternatives):

| word | matches? |
|---|---|
| `re-observed` | **no** |
| `resolves` | **no** |
| `history` | **no** |
| `historical record` | **no** |
| `stat ok` | **no** |

All five pass. Two cautions that the words alone do not cover, both observed rather than inferred:

- The regex is **unanchored and substring-matching**. `no longer` fails — my first simulated note (“so the earlier absence annotation **no longer** describes this host”) made the sweep exit 2 with `paths sidecar binding invalid: corpus/lessons/round-29-verifier-spotcheck.md:190`. `gone` also fires inside *undergone/begone*, `missing` inside *dismissing*, `absent` inside *absentee*.
- The blanking is `PATH_RE` only, i.e. only `~/…` and `/home/vgpnk/…` spellings. A relative path or a bare word in the note is **not** blanked.

Consequences for the flip, in order:

- A `restored` note may **not** reuse the prior note text (it says “absent”); the prior bytes must move to `history`, which the sweep never reads.
- If `date` becomes `2026-11-03`, the note must contain `2026-11-03`; a note dated 2026-11-03 with `date` left at 2026-10-31 fails rule 9 unless the note also carries the old date.
- `lineSha256` must **not** change: flipping a `kind`/`note` does not touch the cited corpus line.
- The 4 entries that stay `kind=absent` must keep both an absence word and the literal `historical record, not an executable instruction` — all 4 do today (148/148 absent notes match `ABSENT_RE` and carry the phrase).

## (4) Binding integrity at base

- `lineSha256` mismatches over all 174 entries: **0**. No cited line has changed since the entry was written.
- Entries whose token is not on the cited line after `normalize`+`canonHome`: **0**. One entry (`corpus/lessons/round-55-verifier-spotcheck.md:61`) binds only because the line spells the path as `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/` with a trailing slash: `normalize` strips the slash and `canonHome` rewrites the prefix. A rewrite that re-derives tokens without that pair would break it.
- Cited lines carrying the entry's token **more than once** (ambiguous binding): **13** — all `kind=restored`, all in the `ds4cc-marketplace` family (`SKILL.md` 16/19/365/424, `corpus/knowledge/fleet-registry.md` 49/50/64, `corpus/knowledge/origin-repos.md` 11/19/70, `corpus/lessons/round-1-aggregator-audit.md` 30, `corpus/knowledge/mirror-pitfalls.md` 63, `corpus/knowledge/speedrun-pipeline.md` 13). **Zero of the 144 flips has a duplicated token** — the flip introduces no new ambiguity. `lineSha256` pins the whole line, so both occurrences are frozen; only the intent is ambiguous, and the sweep accepts it (`tokens.includes`, not a count).
- Files: 62 distinct, all present at base; no entry cites a file that is missing.
- Duplicate `file:line:token` keys: 0.

## (5) The 26 `restored` entries

- Tokens: 4 distinct, all under `~/Projects/ds4cc-marketplace` (`…`, `/CNAME`, `/burnerchrome`, `/speedrun`). **Every one is present on this host** (`restored_absent=0` confirmed); none needs a second flip.
- Every one already carries a dated observation: `date=2026-10-21` and a note opening `2026-10-21: … present (test -e exit 0; checkout 1fbdb8ed)`. So rule 9 is already satisfied and these entries need **no edit at all**.
- They do **not** carry `historical record, not an executable instruction` (0/26) — correctly, since that phrase is required only for `kind=absent`.
- Pre-existing defect, not binding-validated: **7** of the 26 notes self-cite a line one lower than the entry's own `line` — `SKILL.md:365→364`, `446→445`, `449→448`, `450→449`, `451→450`, `424→423`, `432→431`. A rewrite that regenerates restored notes would silently “fix” these; a rewrite that leaves them alone preserves the defect. Neither is required by the contract — but touching them is churn, so leave them.
- The sidecar is internally contradictory for three tokens today: `~/Projects/ds4cc-marketplace` is `absent` in 27 entries and `restored` in 15; `/burnerchrome` 5/5; `/speedrun` 5/5. The flip collapses each family to a single `restored` state (42 / 10 / 10), which is a real consistency gain.

## (6) Byte-level constraints for a deterministic rewrite

The base file is exactly reproduced by `json.dumps(data, indent=2, ensure_ascii=False) + "\n"` — **byte-identical, 103243 bytes** (verified). The current writer of record, `.ufo/waves/round-66/sidecar_from_drift.mjs:96`, is `JSON.stringify(sidecar, null, 2) + '\n'`, the same convention. Constraints:

1. **Indent 2 spaces**, `"key": value` separators, one entry per object, array items at 4 spaces.
2. **`ensure_ascii=False`** — the base file carries 144 raw U+2014 em dashes (432 non-ASCII bytes, 0 `\u` escapes). Python's `json.dump` defaults to `ensure_ascii=True`; that default rewrites every em dash as `\u2014`.
3. **Trailing newline** — the file ends `}\n`; no CRLF anywhere.
4. **Field order per entry**: `file, line, token, lineSha256, kind, date, note` — uniform across all 174. A new `history` key must be appended in one fixed position (after `note`), or the diff becomes positional noise.
5. **Array order is historical, not sorted** — 125 file-runs in append order (e.g. the first four entries are four different files, then `SKILL.md:16…`). A rewrite must **mutate in place** and must not sort; a re-sort would rewrite every entry.
6. **Field presence**: all 7 fields on every entry; `history` added only to flipped entries, as a list of `{date, kind, note}` objects preserving the prior values verbatim. Extra keys are ignored by the sweep (observed: adding `history` to a `kind=absent` entry still exits 1), so the sweep cannot enforce the history rule — only the counter can.
7. **No re-pinning**: `lineSha256` stays as-is; a rewrite must not recompute it from a re-read line (that would mask a genuine drift).

## Observed cross-checks (scratch probe, not inference)

I rebuilt a 4.1 MB probe tree from committed bytes (`git archive <rev> SKILL.md corpus scripts`) and ran the sweep there; the base run reproduces `controls/base-c2-sweep.txt` line-for-line except that the control appends its own `SWEEP_EXIT=1` trailer (`resolve 32 · declaredAbsent 64 · drift 1 · unresolved 10`, exit 1). Receipts: `w1/ScoutSidecar/sweep-base.out`, body `w1/ScoutSidecar/sweep-base.body`.

1. **The flip is invisible to `§paths` by construction.** A token that exists is classified `resolve` before any annotation is consulted, so the 144 flips change no counter: the sweep output after a valid flip is **byte-identical** to the base output (verified by `cmp` on the body). This is exactly the blindness the contract names — and it means the flip cannot be validated by the sweep's counts, only by the counter.
2. **Negative controls all fire** (scratch, exit codes observed): note containing `no longer` → exit 2 `paths sidecar binding invalid`; note missing the entry date → exit 2 `paths sidecar invalid entry`; tampered `lineSha256` → exit 2 binding invalid; `kind=restored` keeping the prior absent note → exit 2 invalid entry; `kind=absent` without the historical-record phrase → exit 2 binding invalid. **Missing `history` array → exit 1, accepted**: the sweep does not enforce contract clause 2.
3. **The in-flight repair tool already lands a valid flip.** `w1/ExecC2Tool/sidecar_reobserve.py` (sha256 `1284bd17…`) on the probe: `--check` reports `entries=174 absent=148 restored=26 absent_present=144 absent_absent=4 restored_absent=0 unevaluable=0` exit 0; `--write --date 2026-11-03 --host linux-x86_64` reports `flipped=144 wrote=true` exit 0; the result is 170 restored / 4 absent / 144 with `history`, the sweep accepts it (no stderr, exit 1, same single drift), and the `§paths` body is byte-identical to base. Receipts: `w1/ScoutSidecar/sweep-tool.out`.

   One deviation from the byte convention above: the tool writes with `json.dump(data, target, indent=2)` and no `ensure_ascii=False`, so the 144 em dashes become `\u2014` escapes (file 103,243 → 149,983 bytes, 0 non-ASCII bytes, 144 `\u` escapes). Functionally accepted everywhere (JSON string values are identical after parse, so the history rule holds); it is a reviewability/diff-noise regression against the round-66 writer, not a predicate failure. Adding `ensure_ascii=False` restores byte parity for every untouched entry.

## Hazards for the landing (recorded, not acted on)

- **`SKILL.md` pins are line-bound.** 25 sidecar entries cite `SKILL.md` with `lineSha256`, largest `line=935`. C1 must add a round-74 gate-registry section naming `c74_registry_gap.py`. `SKILL.md` itself already states the rule at line 1400: the section “is appended after line 935 … a future row keeps this append-at-EOF discipline or re-pins the sidecar in the same commit.” Appending at EOF (file is 1404 lines at base) keeps all 25 pins valid; inserting a row anywhere above 935 breaks all of them and fails C2.
- **`corpus/SOURCES.md` pins are line-bound.** 7 entries cite it, largest `line=140` (file is 294 lines). The round's `S441`/`S442` rows must be appended at EOF, not inserted, for the same reason.
- The 4 surviving `kind=absent` entries are the contract's fixed population: they are the only `absent_absent` rows, and flipping any of them would produce `restored_notes_absent > 0` and exit 1. The flipper must key on the observed state (`present`), not on "was absent in the note".

## Remaining unknowns

- Whether the L1 will adopt `ensure_ascii=False` in the tool before landing — a one-token change I did not make (read-only seat).
- The counter's own semantics are out of this seat's scope; I verified only what the sweep accepts.

## Scratch

`/fast/scratch/hyaku/kake-r74/ScoutSidecar/` (probe tree, receipts, probe scripts) is deleted before this seat yields; the receipts copied to `w1/ScoutSidecar/` are listed above.
