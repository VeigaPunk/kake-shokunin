# ExecHarm — harm battery at base + EOF-append harm map (round 75, wave w1)

Measured 2026-11-03 on linux-x86_64: node v24.21.0, Python 3.14.8, git at the lane checkout.
Base revision under measurement: `c9c5e484c533aa65f4374b841a3edcf572ed19a9`. Lane HEAD when the
scan closed: `d599c8be` (round-75 amendment 2); freeze `88f2e05f`.

Method: `git clone --shared` of the lane checked out at base in
`/fast/scratch/hyaku/kake-r75/ExecHarm/lane`; every scratch artifact (fixture repos, `HOME`,
`TMPDIR`, `--work`) lives outside that clone. Exact commands and exits: `ExecHarm/commands.txt`.
No lane file was created, edited or deleted; no git mutation was run in the lane.

**Answer in one line:** none of the eight gates is harmed by a `SKILL.md` append *at EOF* that stays
below the largest sidecar pin (line 935) and contains no `/tmp` literal and no non-resolving `~/`
token; inserting text *above* line 935 breaks freshness-sweep with `exit 2` (sidecar binding
invalid), and a `/tmp` literal in appended prose breaks `c72_tmp_v2` and `c73_tmp_v3` with `exit 1`.
The round's two new instruments are scratch-honest; the C2 receipt does not exist yet.

## 1. Base battery (eight gates, `c9c5e484`)

| # | Gate | Exit | Verdict line | Receipt |
|---|---|---|---|---|
| 1 | `freshness-sweep --selftest` | 0 | `selftest: 36/36 passed` | `base-fs-selftest.txt` |
| 2 | `freshness-sweep --offline` | 1 | `VERDICT: DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet (exit 1, partial: offline)` | `base-fs-offline-realhome.txt`, `base-fs-offline-freshhome.txt` |
| 3 | `c66_gate_status_hostportable.py` | 0 | `C1 gate-status members=28 evaluated=28 mismatches=3 structural=0 agreement=25 scores_held=3/3 met=True` | `base-c66.txt` |
| 4 | `c70_pointer_audit.py` | 0 | `pointers=373 dangling=17 annotated=17 unannotated=0 met=true` | `base-c70-realhome.txt`, `base-c70-freshhome.txt` |
| 5 | `c72_tmp_v2.py` | 0 | `C2v2 … brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=8 added=48 guard=ok met=True` | `base-c72.txt` |
| 6 | `c73_tmp_v3.py` | 0 | `C2v3 … attack_accepted=0/0 legit_rejected=0/0 selftest=41/41 findings=[] met=True` | `base-c73-tmp-v3.txt` |
| 7 | `c73_wave_pointers.py` | 0 | `C1v1 … pointers=9 dead=2 annotated=2 unannotated=0 append_only=true met=true` | `base-c73-wave-pointers.txt` |
| 8 | `c74_registry_gap.py` | 0 | `population=8 … unregistered=0 own_row=true met=true`; `--selftest` → `selftest 8/8` | `base-c74-registry-gap.txt`, `base-c74-registry-gap-selftest.txt` |
| 9 | `c74_sidecar_reobserve.py` | 0 | `C2v1 … entries=174 absent=4 restored=170 contradictions=0 annotation_findings=0 met=true` | `base-c74-sidecar-realhome.txt`, `base-c74-sidecar-freshhome.txt` |

(C1's contract calls the set "eight gates"; the sidecar re-observe is the eighth instrument and the
freshness sweep counts once.)

Details that matter:

- **freshness-sweep counts** (`§paths`): `196 files · 722 occurrences · 107 unique tokens`;
  `resolve 32 · declaredAbsent 64 · drift 1 · unresolved 10` on the real host `HOME`, and
  `resolve 1 · declaredAbsent 73 · drift 23 · unresolved 10` on a fresh scratch `HOME`.
  The selftest is hermetic (`36/36`) in both.
- **c66** reports three `live_not_green` members, all reported and not gated: `c57_idresolver_gate`
  `e_T=2` (`base-c66.txt:48`; its registry argv embeds the old host's
  `C:/Users/jpvei/...` fleet path, line 49), `c58_resolver_cases` `e_T=1` (line 61),
  `c59_resolver_cases` `e_T=1` (line 68). The gate-status ledger's Windows-era "this-host observed"
  cells are therefore stale on this host by their own recheck rule; `met=True` is unchanged because
  c66 gates evaluability, not agreement.
- **c74_registry_gap**'s own row claims five fixtures `f1`–`f5` while the counter prints
  `selftest 8/8`; the E3 finding is real and reproduces the contract's base control.
- **HOME sensitivity** (see §6 D1): c70 flips `0 → 1` and c74_sidecar flips `0 → 1` when run with a
  fresh scratch `HOME`.

### Unannotated drift tokens (freshness-sweep `--offline`)

Real host `HOME` — 1 token: `~/projects` (11 of 32 cites). `1 NOT in pins.pathsMissSet`.
Fresh scratch `HOME` — 23 tokens: `~/.local/bin/time` (3/3), `~/.omp/agent/RULES.md` (2/2),
`~/.omp/agent/config.yml` (1/1), `~/Projects` (8/119), `~/Projects/ds4cc-marketplace` (27/45),
`~/Projects/ds4cc-marketplace/burnerchrome` (5/10), `~/Projects/ds4cc-marketplace/speedrun` (5/10),
`~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` (3/3),
`~/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge` (1/1), `~/Projects/shokunin` (53/60),
`~/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md` (1/1),
`~/Projects/shokunin/.ufo/reports/round-33/kake.md` (2/2),
`~/Projects/shokunin/.ufo/reports/round-54/kake.md` (1/1),
`~/Projects/shokunin/.ufo/reports/round-55/kake.md` (1/1), `~/Projects/shokunin/kake-shokunin` (5/10),
`~/Projects/shokunin/kake-shokunin/SKILL.md` (3/8),
`~/Projects/shokunin/kake-shokunin/corpus/SOURCES.md` (7/7),
`~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md` (3/3),
`~/Projects/shokunin/scripts/sources-census.sh` (23/24),
`~/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md` (3/3),
`~/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/ReviewFreeze.md` (3/3),
`~/Projects/ufo-fsd-alpha` (1/4), `~/projects` (11/32).
`4 NOT in pins.pathsMissSet` = `~/.local/bin` (set-delta only), `~/.omp/agent/config.yml`,
`~/Projects`, `~/projects`. The 23-token picture is the fresh-`HOME` artefact; only `~/projects`
is a real host miss.

## 2. Scratch literals in the round's instrument bytes

Full transcript: `ExecHarm/scratch-literal-scan.txt`.

- `.ufo/waves/round-75/c75_row_truth.py` (freeze bytes, sha256 `43538343…a596ce`): `git grep -n /tmp`
  → **no hit** (exit 1). `-E '/tmp|tempfile'` → one hit, `c75_row_truth.py:37:import tempfile`; the
  import is never used (`grep -n 'tempfile\.'` → no hit). Scratch gates: `--work` is mandatory
  (without it: exit 64, `64 usage: --work <dir> is required`), the clone lands in `<work>/tree` and
  `HOME`/`TMPDIR` are set to `<work>/scratch/{home,tmp}` — scratch is a sibling of the clone.
- `scripts/instrument_receipts.py` (C2 tool): **not committed** at scan; the wave's in-progress copy
  `.ufo/waves/round-75/w1/ExecC2Tool/instrument_receipts.py` was pinned by copy
  (sha256 `60312744…725f1c7`, 1081 lines). `grep -n /tmp` → no hit; `:94 import tempfile`;
  `:754 tempfile.mkdtemp(prefix="fx-", dir=work)`; `--selftest` without `--work` → exit 64;
  `--selftest --work <scratch>` → exit 0, `selftest: 14/14`.
- `corpus/knowledge/instrument-receipts.json`: **absent** at scan — no C2 receipt exists yet.
- Zero `/tmp` hits in the freeze tree (`88f2e05f`). At HEAD the only hits are prose, not code:
  `w1-dispatch.json:60,108,121,151,191`, `w1-spec.json:5,35,75`, `w1/swarm-registry.json:42,90`
  (the dispatch's own scratch rule); plus seat reports `w1/ScoutRegistry.md:142,143,145`
  (`TMPDIR=<scratch>/tmp` inside quoted registry cells) and `w1/ScoutRegistry.receipts.txt:2,17,20,26`
  (the expanded `TMPDIR=/fast/scratch/…/tmp`). No `/tmp` hit in any `.py`/`.mjs`/control receipt.

## 3. Which of the eight gates an EOF append harms

Five probe clones at base, one local commit each; full receipts under `ExecHarm/append-*.txt` and
`ExecHarm/insert-*.txt`. The `/tmp`-literal probe was run against all eight gates; the other shapes
against the gates they could plausibly touch (a dash = not run for that shape).

| Append shape | freshness-sweep | c66 | c70 | c72 | c73_tmp_v3 | c73_wave_ptr | c74_gap | c74_sidecar |
|---|---|---|---|---|---|---|---|---|
| clean 10-line section, first new line 1437 | 1 (same drift as base) | 0 | 0 | 0 (`added` 48→58) | 0 | 0 | 0 | 0 |
| row names an uncommitted `.py` | — | — | 0 | 0 (`added` 56) | — | — | 0 | 0 |
| `/tmp` literal in prose (`SKILL.md:1442`) | 1 (same verdict as base) | 0 | 0 | **1** `prose_findings=1 findings=[(1442,0,0,1)] guard=fail met=False` | **1** `findings=[('skill',1442,0,0,1)] met=False` | 0 | 0 | 0 |
| absent `~/` token in prose (`SKILL.md:1442`) | 1, drift 1→2 (adds `~/Projects/execharm-probe-absent`) | — | 0 | 0 | 0 | — | — | 0 |
| one-line insertion above line 935 | **2** `paths sidecar binding invalid: SKILL.md:935` | — | — | — | — | — | — | 0 |

Reading of the map:

- **Append at EOF is safe for all eight** when (a) the first appended line is ≥ 1437, i.e. below the
  largest sidecar pin (935), (b) the text carries no `/tmp` literal, (c) it cites no `~/` path that
  does not resolve on this host. Under those conditions every gate returns its base verdict; the
  only movement is `c72_tmp_v2`'s informational `added` count, which is a line diff against its
  pinned baseline (+1 per appended line: 48 → 58 / 56 / 54).
- **Harmed shapes**: a `/tmp` literal reds `c72_tmp_v2` and `c73_tmp_v3` (proven); an insertion above
  line 935 reds freshness-sweep with exit 2 (proven); an absent `~/` token adds a freshness drift
  target (proven, exit was already 1 at base).
- **Not harmed in any tested shape**: `c66`, `c70`, `c73_wave_pointers`, `c74_registry_gap`,
  `c74_sidecar`. `c74_sidecar` even survives a mid-file insertion because it checks token
  `os.stat`, not line digests; the digest binding is enforced by freshness-sweep.
- A table row naming a not-yet-committed instrument path is invisible to both `c70` and
  `c74_registry_gap` (pointer count stayed 373; `unregistered=0 met=true`), so the landing order
  (row before file) is not itself a harm — but the C1 counter's E4 would still flag it.

## 4. Sidecar pin state (line 935)

`corpus/knowledge/freshness-sidecar.json` carries 174 entries, 25 for `SKILL.md`, largest pinned
line 935; `SKILL.md` is 1436 lines at base and at HEAD `d599c8be` (sha256 at base
`2843f395…5949dde9`, 209,459 B). At base with the real `HOME`,
`c74_sidecar_reobserve` → `entries=174 … contradictions=0 annotation_findings=0 met=true`, exit 0
(`base-c74-sidecar-realhome.txt`): the pin state is green.

After the clean EOF append (probe `a906ce2d`, SKILL.md 210,481 B, sha256 `d8305385…e8d7bf74`):
`c74_sidecar` stays `met=true` exit 0 and freshness-sweep's sidecar binding stays valid (offline run
exits 1 on drift, not 2 on a binding error). After a one-line insertion above 935
(probe `1e732388`): freshness-sweep exits 2 with `paths sidecar binding invalid: SKILL.md:935`
(`insert-above-pin-fs-offline.txt`), while `c74_sidecar` still reports `met=true` exit 0 — the pin is
enforced by freshness-sweep only.

## 5. Instrument scratch honesty (round's new tools)

- `c75_row_truth.py`: no code-level `/tmp`; `--work` mandatory (exit 64 without); the clone lands in
  `<work>/tree` and every recorded self-test command runs with `HOME`/`TMPDIR` pinned to
  `<work>/scratch/{home,tmp}` (lines 111-112) — scratch is a sibling of the clone, never inherited.
  One dead weight: unused `import tempfile` (line 37).
- `instrument_receipts.py` (pinned copy): no code-level `/tmp`; `--work` mandatory (exit 64);
  `--check`/`--write` read committed blobs via `git show` and parse them statically (no recorded
  command is spawned); the selftest builds its fixture repos with
  `tempfile.mkdtemp(prefix="fx-", dir=work)` (line 754) and reaches `selftest: 14/14` exit 0 — the
  fixture tree observed is `<work>/fx-…`, i.e. inside the named `--work`. It inherits the caller's
  `HOME`/`TMPDIR` for its child processes (no override); measured with an explicit scratch `TMPDIR`,
  nothing appeared outside the `--work` tree.

## 6. Defects and risks for the L1

- **D1 (harness, high).** `c70_pointer_audit` and `c74_sidecar_reobserve` are `HOME`-sensitive:
  fresh scratch `HOME` turns both red with no lane defect (c70: 3 unannotated at `SKILL.md:60,66,67`;
  sidecar: 170 `restored_absent` contradictions). Run these two with the real host `HOME` and record
  the fresh-`HOME` figure separately, or the after-state will read false failures.
- **D2 (landing, high).** Any `/tmp` literal in the appended `### Round 75 gate registry additions`
  section reds `c72_tmp_v2` and `c73_tmp_v3` at the appended line (proven at `SKILL.md:1442`).
- **D3 (landing, medium).** An appended `~/` token that does not exist on this host adds an
  unannotated freshness drift target (`~/Projects/execharm-probe-absent` in the probe). Cite only
  repo-relative paths in the new section.
- **D4 (self-application, medium).** `c75_row_truth.py` has no `--selftest` mode. Under Amendment 2
  A3 the Self-test command must name the row's own instrument; the round's own row must therefore be
  Kind `instrument` (or declare a differential), never `gate` with a borrowed command, or C1 E1
  fires on the round's own instrument.
- **D5 (dead weight, low).** Unused `import tempfile` at `.ufo/waves/round-75/c75_row_truth.py:37`.
- **D6 (measured, informational).** `c74_registry_gap`'s row claims `f1`–`f5` while the counter runs
  `selftest 8/8`; `c66` reports `agreement=25` with three `live_not_green` members
  (`c57_idresolver_gate` 2, `c58_resolver_cases` 1, `c59_resolver_cases` 1). Both are reported, not
  gated; the ledger's Windows-era cells are stale on this host by their own recheck rule.
- **D7 (scope note).** No committed instrument contains `/tmp`; the hits named in §2 are dispatch
  prose and seat reports. `ScoutRegistry.receipts.txt` serialises `/fast/scratch/...` seat paths as
  evidence — sentinel remit, named here only because it matched the scan.

## 7. Scope and retained evidence

Files written by this seat: this report plus `ExecHarm/` receipts (46 files) — nothing else in the
lane; no production file, no git mutation, no sibling lane. Scratch tree
`/fast/scratch/hyaku/kake-r75/ExecHarm` (base clone + five fixture clones + out receipts) is deleted
after the receipts were copied; if it is still present at read time that is this seat's defect.

Receipts: `base-*.txt` (base battery, both `HOME` modes), `append-*.txt` (four probe shapes incl.
the `/tmp`-literal probe's full eight-gate run), `insert-above-pin-*.txt`,
`scratch-literal-scan.txt`, `instrument-*.txt`, `commands.txt`.
