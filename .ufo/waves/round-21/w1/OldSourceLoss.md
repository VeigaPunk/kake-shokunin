# OldSourceLoss — historical verified-at/recheck patterns from source-absence annotations

Seat: scout (leaf). Scope: `corpus/knowledge/origin-repos.md` and
`corpus/knowledge/fleet-registry.md` only. Read-only: no target edits, no domain
tree reads (presence checks via `test`/`find` only), no network, no credential
or auth files, no installs. The only repository artifact written is this report;
local measurements used transient files under `/tmp` only.

Base: `5009ecaa1cce10b895617a585ddd3f7c7c923a84`. Working-tree measurements
are a mid-flight snapshot (2026-10-20, files last touched 05:55–05:58 local);
sibling seats may change files after this snapshot.

## 1. Observed state (high confidence, measured)

Both entries now open with a 3-field prefix plus blank line; old bytes are
byte-identical. Both were in the 17-entry non-trio population at base.

| entry | base lines | now lines | prefix | suffix check | first-8 layout |
|---|---|---|---|---|---|
| `corpus/knowledge/origin-repos.md` | 69 | 73 | 4 lines, **745 bytes** | `tail -n +5` sha256 `039967ad3131…d1062` = base sha256 | fields 1–3, blank 4, H1 5, blank 6, prose `Source:` 7 |
| `corpus/knowledge/fleet-registry.md` | 81 | 85 | 4 lines, **882 bytes** | `tail -n +5` sha256 `5b79d39d8ac4…2775e` = base sha256 | fields 1–3, blank 4, H1 5, body `Source:` 7, plazir15 row 57, r20 note 85 |

Commands: `git show <base>:<path> | sha256sum`, `tail -n +5 <path> | sha256sum`,
`git diff --numstat` (each: 4 insertions, 0 deletions), `head -n 4 | wc -c`.

Discrepancy: `Knowledge04.md` (fleet seat report) states the prefix is **1002
bytes** and asks Main to check that value. Measured now: **882 bytes**
(4 lines: 246 + 245 + 383 + 0 chars plus newlines; 882 bytes with UTF-8 em
dashes). Cause unknown — likely a stale draft measurement. Main's stated check
will fail as written; use 882 or, more robustly, verify the suffix hash.

Snapshot of the round-21 C1 count (`SCORECARD.md:25` command): source 21/21,
verified-at 21/21, recheck 21/21. This is field presence only; it does not
measure field truth.

S019: now registered at `corpus/SOURCES.md:27` (status `mined`, opened
2026-10-20, used-by `corpus/lessons/round-21.md`). The sibling reports'
"`S019` is not registered" limitation is stale. The canonical input
`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md:18,162-165`
does require the trio first and says freshness reads fields, not provenance
buried in prose or HTML comments.

## 2. Evidence-date ledger (the dates each field must obey)

| evidence | date | location |
|---|---|---|
| wz-repos terminal round r8, run `gqab44994c06d7e7a4` | 2026-09-21 | origin-repos body line 8 |
| 50/50 clones re-fetched `HEAD == @{u}` at r8 | r8, 2026-09-21 | origin-repos body line 13 |
| byte-verified writer receipts | r5–r8 | origin-repos table |
| fleet config `updatedAt` | 2026-09-26 | fleet body lines 7–8 |
| `len(sites)` = 21 + live probe + lucario/charter-ghp observations | 2026-09-28 | fleet body lines 9–20 |
| r18 absence re-census (webzites tree, ds4cc checkout, origin-work) | 2026-10-14 | inline `<!-- r18 re-census … -->` comments |
| r20 citation-local absence (`~/Projects/plazir-15-site`) | 2026-10-19 | fleet line 85 (standalone blockquote) |
| S019 metadata contract opened | 2026-10-20 | `corpus/SOURCES.md:27` |

Current fields use 2026-09-21 (origin) and 2026-09-28 (fleet) — the last dates
of evidence that actually supports the claims. Neither advances to an
annotation date and neither uses 2026-10-19/20 as a domain recheck. That is
the correct precedence.

[INFERENCE] The 2026-09-26 `updatedAt` is config provenance, not verification
of the registry contents; using 2026-09-28 (the lane's verification/probe) is
therefore right.

## 3. Absence annotations present in the two entries

- origin-repos: five inline r18 HTML comments (current lines 7, 9, 11, 19, 70)
  naming `~/Projects/webzites/reports/keepers/repos-r1.md`,
  `~/Projects/webzites/repos/<name>`, `~/Projects/ds4cc-marketplace`; event
  "gone in the 2026-10-12 ~/Projects prune/migration"; wording "cite retained
  as historical record".
- fleet-registry: four inline r18 comments (lines 49, 50, 60, 64) naming
  `~/Projects/ds4cc-marketplace` and `~/Projects/origin-work/charter-ufo-fsd`;
  one standalone r20 blockquote (line 85) naming `~/Projects/plazir-15-site`,
  event W7 2026-10-12 prune, annotation date 2026-10-19.

The table also cites absent paths without inline comments: line 51
(`…/ds4cc-marketplace/burnerchrome`) and line 58 (`…/plazir-15-site`) are only
covered indirectly by a neighbouring ±2 annotation; line 67 (`…/lucario`) is
self-annotated by "never published"; **line 57's `~/Projects/plazir-15-site`
is not annotated at all** (see §4).

## 4. Recheck commands: validated behavior and gate coupling

Exact commands as currently written were executed once (read-only, local):

- origin: `test -e ~/Projects/webzites/reports/keepers/repos-r1.md && test -d ~/Projects/webzites/repos && echo present || echo absent` → `absent`.
- fleet: `test -f "$HOME/Projects/webzites/fleet/fleet.config.json" && node -p '…' || echo "absent: operator must restore the fleet source or retire this entry"` → `absent: operator must restore the fleet source or retire this entry`.
  The `node -p` idiom (`const c=require(<json>); [c.schema,c.updatedAt,c.sites.length].join(" ")`) was separately validated against a fixture: prints `webzites-fleet-v1 2026-09-26 3` and exits 0 on Node v24.21.0.

Gate coupling, measured with `scripts/freshness-sweep.mjs --section=paths
--offline --json` on (a) an archived copy of base `5009ecaa` and (b) the
current tree:

| surface | base `5009ecaa` | current working tree |
|---|---|---|
| exit | 1 | 1 |
| drift targets | 3 | 6 |
| unannotated cites | 4 | 8 |
| newMissing | 0 | 5 |
| declaredAbsent | 52 | 54 |

- The two assigned trios are gate-neutral: origin-repos' `~/Projects/webzites`
  cite at line 3 is annotated and pinned; fleet's `fleet.config.json` cite is
  pinned and annotated via line 2; relative paths and `$HOME` are not scanned.
  Neither adds a newMissing token or a drift cite.
- fleet-registry's only drift cite, line 57, is **preexisting**: base line 53
  was already unannotated. History: at `02b6dd0` the r20 note sat inline on the
  plazir15 row; `9639ec7` ("round-20: post-review fixes") moved it to a
  standalone EOF block, which is outside the scanner's per-citation ±2 window.
  Round-20's own post-review note admits "4 unannotated locations / 3 drift
  targets remain"; the base measurement matches exactly. It is not a round-21
  regression and cannot be repaired this round without a non-prefix/EOF edit
  (contract prohibits altering old lines or inserting mid-file).
- New round-21 drift targets (adjacent, measured): `~/Projects/webzites` from
  `round-4.md:46` Gate prose, `~/Projects/webzites/reports/r9-publish-queue.md`
  from `round-9.md:179` Gate recheck, `~/projects` from `round-17.md:64-65`
  Gate recheck. All three are appended-Gate lines with no absence word in the
  ±2 window.
- New round-21 `newMissing` tokens and their introducing lines:
  `~/Projects/webzites/state/probe-latest.json` (`drift-detection.md:3`);
  `~/Projects/ds4cc-marketplace/render.yaml` and
  `~/Projects/plazir-15-site/.github/workflows/pages.yml`
  (`publish-channels.md:3`); `~/Projects/webzites/fleet` (`mirror-pitfalls.md:3`);
  `~/Projects/webzites/reports/sentinel-sourceless-extract-r9.md`
  (`round-9.md:182`). The publish-channels line even contains the word
  "absent", proving **annotation does not exempt a new miss from newMissing**:
  `missSet` includes every absent cite, and `newMissing = missSet −
  pins.pathsMissSet` (`freshness-sweep.mjs:463-478`).

## 5. Derived pattern — safe historical `verified-at` / `recheck`

### 5.1 Field grammar (4 lines, first 8)

```
source: <entry-specific evidence: paths/instrument + revision/run id + what it established>; <absence state: target(s) absent since <event> <date>, per <annotation/date>, retained as historical record> — metadata contract S019 (format authority only; not platform evidence)
verified-at: <latest original evidence date> (<what was observed then; rN/run id>) — historical-not-live-reverified; no domain or source-tree recheck performed in round 21
recheck: on restore of <tree/artifact> or change to <artifact> — <read-only local command producing present/absent and, when present, the expected schema/count>; <operator restore-or-retire requirement>
<blank>
```

Both assigned entries match this shape. Keep the three fields on lines 1–3 so
the round-21 count regex (`^field:\s*\S` in first 8) and the corpus contract's
"trio comes first" both hold.

### 5.2 `verified-at` decision rule

1. Take the **latest date at which the entry's claims were actually
   observed** (origin 2026-09-21; fleet 2026-09-28).
2. A later absence annotation (r18 2026-10-14, r20 2026-10-19) proves the
   source is gone; it does **not** refresh the claims. Never use it as
   verified-at.
3. Never use today/round date for a historical entry. Today is legitimate only
   for a source genuinely opened this round (the r20 `S001–S014` style entries
   use 2026-10-19 for that reason).
4. Name the revision/run (`gqab44994c06d7e7a4`, terminal r8; schema
   `webzites-fleet-v1`) so the date is checkable.
5. State the negative plainly: `historical-not-live-reverified`. Do not write
   "re-verified", "confirmed current", or a live-probe claim.

### 5.3 `recheck` design rules

1. **Read-only and local**: `test`, `ls`, `find`, `node -p`/`require` only.
   No curl/wget, no git fetch, no kimi-surface verbs, no publish/deploy, no
   service or system-state changes, no credential paths.
2. **Both outcomes defined**: today the command must print absent and say what
   the operator must do; when restored it must print a checkable value.
3. **Carry the count** (CORPUS: "a count carries its command"). fleet already
   returns `webzites-fleet-v1 2026-09-26 21`. origin should also verify the
   terminal report and the 50-clone claim when restored.
4. **Pin-set discipline**: any literal `~/` or `/home/vgpnk` cite of an absent
   path that is not already in `pins.pathsMissSet` becomes `newMissing` and
   fails §paths even when annotated. For executable commands use `$HOME/...`
   (invisible to `PATH_RE`) or only already-pinned `~/` tokens. Do not add a
   new absent `~/` cite without an authorized re-pin; the round-20 C1
   disposition kept `pins.pathsMissSet` untouched at 55.
5. **Restore-or-retire** is explicit and operator-owned; the lane never
   restores, probes, or publishes.
6. A trio is **not** an absence annotation for body citations. It annotates
   only cites on/near its own lines (±2). It must never be described as
   clearing §paths.

### 5.4 Placement rule for absence vocabulary

The scanner accepts `absent|gone|vanished|emptied|no longer|dangling|no such
file|never published|missing` within the citing line ±2, with citation text
blanked (`freshness-sweep.mjs:122,314-346`). Standalone EOF notes do not
cover remote body cites. Therefore:

- If a new sentence cites a vanished `~/` path, put an absence word on the
  same line and name the target/event.
- Prefer `$HOME` in commands and plain descriptions for paths that should not
  enter the gate.
- Treat "historical record" / "see annotations above" as **insufficient** —
  they are not absence vocabulary (evidence: `round-4.md:46` drift).

## 6. Field audit of the two assigned entries

Both prefixes are honest on the central question: original evidence dates,
explicit "historical-not-live-reverified", vanished-source statement, safe
local recheck, restore-or-retire, S019 as format authority only. No invented
live verification and no today-dated domain claim.

Recommended refinements (owning seats decide; none required for the C1 count):

1. origin-repos `source`: add the absence-evidence date for self-containment
   (`per r18 re-census 2026-10-14`), matching fleet's wording. Current "absent
   since the 2026-10-12 prune" is true but does not say when absence was
   established.
2. origin-repos `recheck`: test the terminal report and the count, not only
   `repos-r1.md` + dir presence. Safe form (all tokens already pinned):
   `test -e ~/Projects/webzites/reports/keepers/repos-r1.md && test -e ~/Projects/webzites/reports/keepers/repos-r8.md && [ "$(find ~/Projects/webzites/repos -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)" -eq 50 ] && echo present || echo absent`.
   This matters after a partial restore; the current command can print
   `present` with the terminal report missing or the clone set incomplete.
   (Validated now: the refined command prints `absent`.)
3. fleet-registry `source`/`recheck`: the fields cover the r18 fleet-config
   absence but not the r20 `~/Projects/plazir-15-site` absence carried only in
   the line-85 blockquote. Since the contract says readers use fields, not
   buried prose, add a clause such as "`~/Projects/plazir-15-site` also absent
   per the r20 citation-local note (2026-10-19); operator restore-or-retire"
   to `recheck` (path is already pinned; include the word "absent").
4. fleet-registry `source`: "the live probe of 2026-09-28" could read as
   present tense; "the recorded live probe of 2026-09-28" matches `verified-at`.
   Optional.
5. Do **not** touch fleet-registry line 57 this round: repairing it requires a
   mid-file insertion or altering an old line, both prohibited. Record it as
   bounded C1 debt instead.

## 7. Falsifiers — conditions that would make the metadata dishonest

| condition | why it fails |
|---|---|
| `verified-at` is 2026-10-19/20 while the source is absent and no read occurred | stamps a live recheck that never happened |
| wording "re-verified", "confirmed current", or a live-probe claim for a vanished tree | contradicts the r18/r20 annotations |
| `source` cites S019 (or any S-id) as the platform source of a domain claim | S019 is metadata-format authority only |
| `recheck` uses curl/wget against a live property, `kimi-surface`, or a publish verb | crosses the operator publishing boundary and implies live verification |
| `recheck` references credential/auth paths or `~/.omp` | forbidden surface |
| trio described as making §paths green / clearing citation debt | measured false: per-citation window is independent of the prefix; fleet line 57 stays red |
| adding new `~/` absent cites without a re-pin | creates `newMissing` and fails the gate even when annotated (measured 5 cases) |
| prefix changes any old byte or is not exactly 3 fields + blank | violates the round contract and first-8 count |
| origin recheck prints `present` on a partial restore | command under-covers the terminal artifact and count |

## 8. Remaining unknowns

- Dates of the individual `repos-r1…r7` reports and whether `repos-r8.md` is
  the only terminal artifact; the entry pins only the terminal round date and
  run id.
- Date/revision of `fleet/fleet.dedupe-report.md`; `updatedAt 2026-09-26` is
  the config's field, not the report's date.
- Exact origin of the "live probe of 2026-09-28" values (the entry does not
  name `state/probe-latest.json` as its source; `drift-detection.md` does).
- Whether Main wants the two refinements applied before integration; the C1
  count passes without them.
- Final §paths verdict after all sibling edits land; my current-tree numbers
  are a mid-flight snapshot and include unrelated seats' additions.
- Cause of the 1002-vs-882 prefix mismatch in `Knowledge04.md` (stale draft
  measurement is the [INFERENCE]; the file itself is intact).

## 9. Handoff checks for Main

1. `tail -n +5 corpus/knowledge/origin-repos.md | sha256sum` →
   `039967ad31312709071b11e153cd51ca0944403f1386295b97ebd806781d1062`.
2. `tail -n +5 corpus/knowledge/fleet-registry.md | sha256sum` →
   `5b79d39d8ac43fa9100b77324615c8a217712f789184e929cafe50347402775e`.
3. `head -n 4 … | wc -c` → 745 (origin), 882 (fleet); correct
   `Knowledge04.md`'s 1002 expectation.
4. Re-run `node scripts/freshness-sweep.mjs --section=paths --offline` after
   integration. Expect the preexisting fleet-registry:57 (plazir) drift and
   the documented r20 bounded debt; expect no newMissing from these two trios.
   If gate green is required, do not fake it by re-pinning or by rewriting old
   lines — re-pinning needs explicit authorization and the preservation
   contract forbids mid-file repair this round.
5. If refinements 6.1–6.3 are applied, re-check that `verified-at` still names
   the evidence date (not 2026-10-20) and that the added clauses keep the
   absence word on the cited line.
