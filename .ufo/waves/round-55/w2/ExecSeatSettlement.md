# ExecSeatSettlement

ATTACKS: the round-55 W1 settlement — `.ufo/waves/round-55/w1-dispatch.json` (40 seats) and
`.ufo/waves/round-55/w1-results.json` measured against committed bytes at
`a7a548e102b71bd16b0a6ddafa469393a2c98b69`, plus the fleet-root and lane untracked sweeps.

## METHOD (commands and observed output)

- `git -C <lane> cat-file -t a7a548e1…` → `commit`; `git log -1 --format='%H%n%s%n%ci'` →
  `round-55: QUALITY criteria, gate registry rows, PROVINCE step, counter selftests`, `2026-10-25 18:06:01 -0300`.
- `git ls-tree -r --long a7a548e1… -- .ufo/waves/round-55/w1/` → **39 entries: 38 seat `.md` +
  `swarm-registry.json`**. Dispatch declares **40** seats.
- Per seat: `git show a7a548e1…:.ufo/waves/round-55/w1/<Name>.md` → 38 present, first line
  `# <Name>` 38/38, terminal single-line `VERDICT:` 36/38; `ConnectorSiblings` and
  `CriticC2Contract` end with a 4-line VERDICT paragraph (3 continuation lines after the
  `VERDICT:` line) — verdict present, terminal-line form absent.
- `git ls-tree a7a548e1… -- .ufo/waves/round-55/w1-results.json` → **empty** (record not in the
  measured revision). `git diff --name-status a7a548e1…..HEAD` → `A w1-results.json`,
  `A w1/ScoutScopeOverlap.md`, `A make_spec_w2.py`, `A w2-dispatch.json`, `A w2-spec.json`,
  `A w2-validator.err`, `A w2.ready`, `A w2/swarm-registry.json`. HEAD = `78963ae` (18:11:32),
  **5 m 31 s after** the measured revision.
- `git ls-tree -r HEAD -- .ufo/waves/round-55/w1/` → 39 `.md` + registry; every `.md` maps to a
  dispatched seat (no report without a seat). `ScoutScopeOverlap.md` at HEAD: 160 lines, first line
  `# ScoutScopeOverlap`, `VERDICT:` at line 155 with 5 continuation lines.
- Results record shape (`json.load`): 40 entries, keys exactly `agent,name,note,output`; `note` is
  `null` for **all 40**; `"status"` JSON-key occurrences = **0**; strings `settled`/`settlement` =
  **0**. Roster equals dispatch (40/40, no missing/extra); `agent` equals registry role for all 40.
  A `verdict` key inside `output` exists for 28/40; absent for 12: `RowSecurityTxt`,
  `EntryRefusalRules`, `EntryPatternSyntax`, `ScribeGroundMap`, `ScribeQuality`,
  `ScribeSkillRegistry`, `ScoutFreshS372`, `ScoutFreshS373`, `ScoutFreshS418`, `ConnectorSiblings`,
  `ExecIdGuard`, `MutC1Counter`.
- Claimed-vs-committed reconciliation of each `report`/`report_path`: 36 canonical;
  `EntryPatternSyntax` carries the string `.ufo/waves/round-55/w1/EntryPatternSyntax.md (145 lines)`
  (committed 145 lines — matches); `ConnectorSiblings` claims `lines: 104`, committed **103**;
  `ExecIdGuard` records no report path at all (keys `files_changed, behavior, commands, evidence,
  risks, unrun, tooling`); `ScribeQuality` names a path that does not exist (below).
- Empty reports: **none**. Smallest by bytes 4307 / 72 lines (`RowJsRenderQueue`); fewest lines 28
  (`RowPagesBasePath`, 5333 bytes).
- No tool installed; no pacman run; no git/jj mutation (read-only `show/ls-tree/diff/log/status/grep`).

SEAT TABLE: (report @a7a548e = committed at the measured revision; first line / VERDICT graded on
the committed blob; "recorded" = an entry exists in `w1-results.json`, which carries no status field)

| seat | role | report @a7a548e | report @HEAD | first line | VERDICT | results entry |
|---|---|---|---|---|---|---|
| RowAccessCards | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowAccessPacket | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowBaiduFriendly | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowBaiduMobile | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowCanonicalSel | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowCrawlBudget | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowCrawlErrors | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowCrawlerIdent | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowDynamicRender | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowFreshSidecar | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowJsRenderQueue | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowLinkPreview | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowPagesBasePath | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowReceiptIntegrity | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowRedirectRules | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowRenderStatic | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowRenderServices | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowRobotsRules | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowSecurityTxt | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded-no-verdict |
| RowVaultProps | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| RowYahooNofollow | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| EntryRefusalRules | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded-no-verdict |
| EntryPatternSyntax | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded-no-verdict |
| EntryRobotsBasics | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded |
| ScribeGroundMap | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded-no-verdict |
| ScribeQuality | scribe | **NO** | **NO** | — | — | recorded-no-verdict (phantom path) |
| ScribeSkillRegistry | scribe | yes ok/ok | yes ok/ok | ok | ok | recorded-no-verdict |
| ScoutFreshS372 | scout | yes ok/ok | yes ok/ok | ok | ok | recorded-no-verdict |
| ScoutFreshS373 | scout | yes ok/ok | yes ok/ok | ok | ok | recorded-no-verdict |
| ScoutFreshS418 | scout | yes ok/ok | yes ok/ok | ok | ok | recorded-no-verdict |
| ScoutScopeOverlap | scout | **NO** | yes ok/wrapped(+5) | — | — | recorded |
| ConnectorSiblings | connector | yes ok/wrapped(+3) | yes ok/wrapped(+3) | ok | wrapped(+3) | recorded-no-verdict |
| ConnectorCrossClaim | connector | yes ok/ok | yes ok/ok | ok | ok | recorded |
| ExecBaseControls | executor | yes ok/ok | yes ok/ok | ok | ok | recorded |
| ExecStagedQuoteAudit | executor | yes ok/ok | yes ok/ok | ok | ok | recorded |
| ExecIdGuard | executor | yes ok/ok | yes ok/ok | ok | ok | recorded-no-verdict (no report path in record) |
| CriticC1Contract | critic | yes ok/ok | yes ok/ok | ok | ok | recorded |
| CriticC2Contract | critic | yes ok/wrapped(+3) | yes ok/wrapped(+3) | ok | wrapped(+3) | recorded |
| MutC1Counter | mutation-tester | yes ok/ok | yes ok/ok | ok | ok | recorded-no-verdict |
| ReviewerC2CounterCode | reviewer | yes ok/ok | yes ok/ok | ok | ok | recorded |

MISSING:
- `ScribeQuality` — **no committed report at the measured revision and none at HEAD**:
  `git cat-file -e a7a548e1…:.ufo/waves/round-55/w1/ScribeQuality.md` and the same at `HEAD:` both
  fail; `git ls-files | grep -i scribequal` lists only round-23/24/34–39/42 files. Its results entry
  names `.ufo/waves/round-45/w2/ScribeQuality.md`, which is also absent at rev and HEAD. Its dispatch
  prompt (`w1-dispatch.json` tasks[25]) is correct round-55 text ("Draft a `## Round-55 criteria`
  block …"), and `w1-spec.json` items carry only `name,prompt,role` (no report path), yet the output
  body is round-45-shaped: `insertion_point` = append under `## Criteria appended — round 45
  (2026-10-25)`, criterion 85 titled "a deciding receipt binds the revision it measured".
  `git grep -c -F "Criterion 85" a7a548e1… -- .` → **0**; `git grep -l -F "binds the revision it
  measured" a7a548e1… -- .` → absent; the committed `corpus/QUALITY.md` at rev holds `## Round-55
  criteria` at line 1146 as five bullets. The seat is recorded as settled with no artifact and no
  verifiable deliverable in committed bytes.
- `ScoutScopeOverlap` — not committed at `a7a548e1…`; landed in the settlement commit `78963ae`.
  At the attacked revision the settlement therefore stood at **38 of 40** reports.
- `w1-results.json` — the settlement record itself is **not in the measured revision**; it is one of
  the eight additions in `78963ae`.
- A per-seat **settled status is unrecorded for all 40 seats**: entry keys are
  `agent,name,note,output`, `note` is `null` ×40, and no `status`/`settled` field or string exists in
  the file. "Settled" is only inferable from entry presence, and for `ScribeQuality` that inference
  is false.
- 12 of 40 results entries carry no `verdict` key (list in METHOD), so even the loose in-output
  verdict signal is absent for them.
- Reports without a seat: **none** (39 HEAD `.md` ↔ 39 dispatched names).
- Empty reports: **none**.
- Terminal `VERDICT:` line missing as a single final line: `ConnectorSiblings`,
  `CriticC2Contract` (both +3 continuation lines); `ScoutScopeOverlap` (+5). The keyword and verdict
  text are present in all three.

MISROOT:
- Fleet repo `git -C /home/vgpnk/Projects/shokunin status --porcelain` → 17 lines: 16 ` M`
  (15 × `.ufo/state/*.report-baseline` + `.ufo/watchdog.log`) and one `??`:
  `.ufo/waves/round-30/wave1/ScribeLesson.md`. `git status --porcelain -uall` confirms it is the only
  untracked path; `grep -niE 'kake|round.?55|r55'` on it → **no match** (it is a round-30 lesson
  assembly report). **No untracked fleet path names kake round 55.**
- Fleet root holds no `.ufo/waves/round-55` (`ls -d` → "No such file or directory"). The residual
  evidence of a misroot lives inside the settlement text: `RowBaiduMobile`'s `untouched` list states
  "a first write resolved to the workspace root and was copied to the lane path, then removed;
  /home/vgpnk/Projects/shokunin/.ufo/waves/round-55 no longer exists". Cleaned, not re-checkable.
- The results file cites `/home/vgpnk/Projects/shokunin/tameshi-shokunin` once, inside a falsifier
  command (read-only sibling reference), not as a write target.
- Lane `git -C <lane> status --porcelain` at the start of this seat → **empty output**; the same
  command later in the run → **15 `??`** paths, all `.ufo/waves/round-55/w2.ready.dispatched` or
  `.ufo/waves/round-55/w2/<Seat>.md` (concurrent W2 seats), with **0** tracked modifications. Ignored
  lane entries: `.jj/.gitignore`, `.jj/repo/`, `.jj/working_copy/`, `.ufo/waves/round-52/__pycache__/`,
  `.ufo/waves/round-52/selftest/`, `.ufo/waves/round-54/__pycache__/` — none written this round.
  No W1 path is untracked and no untracked lane file sits outside `.ufo/waves/round-55/w2/`.
- The only round-misrooted path inside the lane record is `ScribeQuality`'s
  `.ufo/waves/round-45/w2/ScribeQuality.md`.

VERDICT: Settlement is not committed at the measured revision (38/40 reports; record and
ScoutScopeOverlap land 5 m 31 s later in 78963ae) and stays defective at HEAD — ScribeQuality has no
report at any revision, its record points at a nonexistent round-45 path describing an absent
deliverable, no per-seat settled status exists for any of the 40 seats, and three reports lack a
single terminal `VERDICT:` line; fleet and lane misroot sweeps are clean of kake round-55 residue.
