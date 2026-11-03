# ExecRegistryRow — round 73, wave 1 (kake, attempt 1)

Base revision `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`. Every reading below is over committed bytes
(`git show`, `git cat-file blob`) or over the scratch clone built from that revision. Host tools:
`python3 -V` → Python 3.14.8 (exit 0), `node -v` → v24.21.0 (exit 0), `git --version` → git version 2.56.0
(exit 0). **No tool was installed or upgraded** (none was needed; no pacman transaction was run).

Write scope honoured: the only file written inside the lane checkout is this report. No lane git/jj
command was run (`git -C /home/vgpnk/Projects/shokunin/kake-shokunin` was used for read-only `show`,
`cat-file`, `log` only). All fixtures lived under `/fast/scratch/hyaku/kake-r73/ExecRegistryRow/`
(307 MB) and were deleted before yield (§7).

## 1. Registry geometry at base

Commands (cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`, all exit 0):

```
git show c1f3d8d4ed9470ecbaaf3353952a374b079e68cc:SKILL.md | grep -n "Owned freshness gate registry"
  208:### Owned freshness gate registry

git show c1f3d8d4ed9470ecbaaf3353952a374b079e68cc:SKILL.md | sed -n '210,214p'
  210  | Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
  211  |---|---|---|---|---|---|---|---|
  212  | freshness-sweep | gate | ...
  213  | c53_gate_truth.py | gate (never met: ...
  214  (blank)

git show c1f3d8d4ed9470ecbaaf3353952a374b079e68cc:SKILL.md | wc -l
  1396
```

- **Column count: 8**, read from the header row at line 210 (`Name`, `Kind`, `Entry command`,
  `Verdict map`, `Self-test`, `Pinned values / frozen proof`, `Write scope`, `Owner`).
- **Last data row of the `Owned freshness gate registry` table: line 213** (`c53_gate_truth.py`;
  separator is 211, first data row is 212, line 214 is blank).
- **Last registry row anywhere in SKILL.md: line 1396** (`gate-status-counter-v2-hostportable`, in the
  "Round 67 gate registry additions" table — header 1394, separator 1395, row 1396).

Sidecar census (`python3` over `git show c1f3d8d4…:corpus/knowledge/freshness-sidecar.json`, exit 0):

```
entries 174 ; entries with file == "SKILL.md" 25
lines [16,19,20,365,424,432,442,446,449,450,451,476,477,512,513,514,515,516,517,518,519,520,521,815,935]
largest .line for SKILL.md = 935
```

**Insertion point and the 935 test.** "After the last registry row" is taken at line 1396 — the last
registry row in the file — so the appended row lands at **line 1404** (blank separator 1397, heading
1398, prose 1400, header 1402, separator 1403, row 1404). The insertion point is therefore **after
935**, the largest pinned `SKILL.md` line.

The alternative insertion — a data row in the 208 table, i.e. new line 214 — is demonstrably
disruptive: 22 of the 25 `SKILL.md` pins are at line ≥ 214 (only 16, 19, 20 are below it), so all 22
would shift by one and `loadPathSidecar` would throw `paths sidecar binding invalid: SKILL.md:<line>`
(the sweep's own error shape, `scripts/freshness-sweep.mjs:388`). With the append, 0 pins move (§3.2)
and the sweep loads the sidecar without error (§4b).

## 2. The row (deliverable)

Exact committed line at scratch state B (`git show 75e1dc1244f83ce2c6fc2a64ab353ae3c7cf2d62:SKILL.md`,
line 1404, 1549 bytes incl. newline):

```
| c73_tmp_v3.py | gate (live; operability: the round-73 C2 counter closing the four round-72 holes H1-H4; counting command below; selftest command below) | `python3 -B .ufo/waves/round-73/c73_tmp_v3.py --revision <commit>` | `0=met` (`--selftest` exits 0 with the full case count, and the counting run `python3 -B .ufo/waves/round-73/c73_tmp_v3.py --lane <clone> --revision <rev> --corpus .ufo/waves/round-73/attack-corpus.txt` reports every `attack` line a finding and every `legit` line clean, and `--revision c1f3d8d4ed9470ecbaaf3353952a374b079e68cc` plus the measured tip both exit 0 with `findings=[]`); `1=not met` (any attack line accepted, any legit line rejected, a short selftest, or a non-zero base/tip run); `2=unevaluable` (git show or corpus read failure); `64=usage` | `python3 -B .ufo/waves/round-73/c73_tmp_v3.py --selftest` | `.ufo/waves/round-73/contract.md` § C2 (the predicate sentence) and `.ufo/waves/round-73/attack-corpus.txt` (frozen at the round-73 freeze, pipe-delimited rows of `<class>`, `<expected>`, `<line>` with class in {attack, legit}); base pin `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`; do-nothing control is `c72_tmp_v2.py` over the same corpus, reported as `c72_accepts=<k> of <A> attack lines` (the claim requires k >= 1) | read-only over committed bytes and the frozen corpus; `--lane` names the clone, `--work` or an exported TMPDIR names only a scratch dir; `--selftest` is function-level and writes nothing | round-73 wave-1 seat ExecC2Counter (counter); this registry row drafted by ExecRegistryRow |
```

Cells (8 of 8, in the registry's cell order):

| # | Column | Content |
|---|---|---|
| 1 | Name | `c73_tmp_v3.py` |
| 2 | Kind | `gate (live; operability: the round-73 C2 counter closing the four round-72 holes H1-H4; counting command below; selftest command below)` |
| 3 | Entry command | `` `python3 -B .ufo/waves/round-73/c73_tmp_v3.py --revision <commit>` `` |
| 4 | Verdict map | `0=met` (selftest full + every attack line a finding + every legit line clean + base and tip runs exit 0 with `findings=[]`); `1=not met`; `2=unevaluable`; `64=usage` |
| 5 | Self-test | `` `python3 -B .ufo/waves/round-73/c73_tmp_v3.py --selftest` `` |
| 6 | Pinned values / frozen proof | `contract.md` § C2 predicate, `attack-corpus.txt` (frozen at the round-73 freeze), base pin `c1f3d8d4…`, do-nothing control `c72_accepts=<k> of <A> attack lines` (k ≥ 1) |
| 7 | Write scope | read-only over committed bytes + frozen corpus; `--lane` = clone, `--work`/TMPDIR = scratch only; `--selftest` writes nothing |
| 8 | Owner | round-73 wave-1 seat ExecC2Counter (counter); row drafted by ExecRegistryRow |

Row-byte checks (each run against the committed row line):

- No `/tmp` token: `python3` scan of the appended block for the literal → `literal slash-tmp in added block: False`
  (so the phrase `not an executable instruction` is not needed and is not used).
- c72's own `line_findings` (frozen `c72_tmp_v2.py`, imported read-only) over every added line →
  `added-line findings brace/command/prose: [0, 0, 0]`; `any added line with the token root: False`.
- c66's own `md_tables` (frozen `c66_gate_status_hostportable.py`, imported read-only) →
  `tables parsed: 35`, `registry tables containing my row: 1`, `lineno 1404 cells 8 nonempty 8`,
  header `['Name','Kind','Entry command','Verdict map','Self-test','Pinned values / frozen proof','Write scope','Owner']`.
- c66 population: `population_candidates({".ufo/waves/round-73/c73_tmp_v3.py": ("100755", "0"*40)})` → `[]`
  (the regex matches, but the population filter is rounds 48–59), so the row cannot produce
  `extra_member`/`structural`.

Section prose that carries the row (needed because a bare data row after line 1396 is not in a table;
wrapped here for display — the committed file holds it as one paragraph line between the heading and
the table header):

```
### Round 73 gate registry additions

Round 73 ships one counter, `c73_tmp_v3.py`, whose predicate is frozen in `.ufo/waves/round-73/contract.md`
§ C2 before any data; it is offline and reads committed bytes (`git show --end-of-options <rev>:SKILL.md`)
plus the frozen attack corpus `.ufo/waves/round-73/attack-corpus.txt`. No earlier row is superseded:
`c72_tmp_v2.py` has no registry row anywhere in this file (the round-72 closure routed that absence as
defect 2), and this section registers the round-73 counter only. The section is appended after line 935,
the largest `.line` pinned for `SKILL.md` in `corpus/knowledge/freshness-sidecar.json`, so no pinned line
moves. Withdrawal rule: a row goes when its counter leaves the tree.
```

(`git show c1f3d8d4…:SKILL.md | grep -c "c72_tmp"` → `0`, so the non-supersession sentence is measured,
not assumed.)

## 3. Scratch clone, re-pin, and the two commits

```
S=/fast/scratch/hyaku/kake-r73/ExecRegistryRow
mkdir -p "$S"                                                                       exit 0
git clone --shared -q /home/vgpnk/Projects/shokunin/kake-shokunin "$S/clone"        exit 0
git -C "$S/clone" checkout -q c1f3d8d4ed9470ecbaaf3353952a374b079e68cc              exit 0
git -C "$S/clone" rev-parse --show-toplevel
  /fast/scratch/hyaku/kake-r73/ExecRegistryRow/clone
git -C "$S/clone" rev-parse HEAD → c1f3d8d4ed9470ecbaaf3353952a374b079e68cc
git -C "$S/clone" status --porcelain → 0 entries
```

### 3.1 State A — the single sidecar re-pin (one field)

- `corpus/SOURCES.md` line 140 at base is 782 bytes; sha256 of the line's UTF-8 bytes, computed over
  `git cat-file blob c1f3d8d4…:corpus/SOURCES.md` split on `\n` (the sweep's own method):
  `4e4081310d6ad17268d8120a29b0400c0edbe6fcee0c035af7c9341acc732e15`
  (recomputed value printed as `matches new pin: True`).
- Old pin `b3315f41997ae6881726be2a5258f3dc2ae815cde7e3a166617322caed4a8a47` occurs exactly once in the
  sidecar (`grep -c` → `1`), so the edit is a single-string replacement; the entry's file/line/token/
  kind/date/note are untouched.
- Commit A `aa528b2dfbd05385de694e7465be63fd3a04b172`, identity `kake-scratch <kake@scratch.local>`.
  `git -C "$S/clone" diff HEAD~1 HEAD --numstat` → `1	1	corpus/knowledge/freshness-sidecar.json`.

The base→A sidecar diff is one hunk with exactly one changed line:

```
-      "lineSha256": "b3315f41997ae6881726be2a5258f3dc2ae815cde7e3a166617322caed4a8a47",
+      "lineSha256": "4e4081310d6ad17268d8120a29b0400c0edbe6fcee0c035af7c9341acc732e15",
```

### 3.2 State B — the appended registry row

- 8 lines appended to `SKILL.md` after line 1396 (blank separator, heading, blank, prose, blank,
  header, separator, row); commit B `75e1dc1244f83ce2c6fc2a64ab353ae3c7cf2d62`, same scratch identity.
- `git -C "$S/clone" diff c1f3d8d4… HEAD --numstat` → `8	0	SKILL.md` and
  `1	1	corpus/knowledge/freshness-sidecar.json`; nothing else in the tree changed.
- Pin verification at B (python; sha256 of `lines[e.line-1]` vs each entry's `lineSha256`):
  `SKILL.md pinned entries checked: 25`, `pins broken: 0`, `max pinned line: 935`, `new row line: [1404]`.
- `git -C "$S/clone" ls-tree -r --name-only HEAD | grep -c "^.ufo/waves/round-73/"` → `0` (base has no
  round-73 tree; the counters see only base + the two commits above).

## 4. Required measurements at state B (exact argv, exit, summary)

### (a) c66 gate status

```
+++ python3 -B .ufo/waves/round-66/c66_gate_status_hostportable.py \
      --root /fast/scratch/hyaku/kake-r73/ExecRegistryRow/clone \
      --revision 75e1dc1244f83ce2c6fc2a64ab353ae3c7cf2d62 --jobs 6 \
      --work /fast/scratch/hyaku/kake-r73/ExecRegistryRow/c66work
exit 0   (stderr empty; 28 member lines; Wall time: 85.35 seconds)
C1 gate-status members=28 evaluated=28 mismatches=3 structural=0 agreement=25 scores_held=3/3 met=True
```

Mismatch lines at B — the same three as the base control, all `live_not_green`:

```
.ufo/waves/round-57/c57_idresolver_gate.py   label=live e_T=2 eval=ok MISMATCH live_not_green
.ufo/waves/round-58/c58_resolver_cases.py    label=live e_T=1 eval=ok MISMATCH live_not_green
.ufo/waves/round-59/c59_resolver_cases.py    label=live e_T=1 eval=ok MISMATCH live_not_green
```

Diff against `controls/c0-gate-status-base-c66.txt` after normalizing the harness `+++` header and the
control's own trailing `c66_exit=0` footer: **no other line differs** — all 28 member lines (label,
exit, eval, argv, argv@pin) and the summary line are byte-identical to base
(`diff c66-base.norm c66-B.norm` → only `1d0 < +++ normalized` and `72d70 < c66_exit=0`).

### (b) Offline freshness sweep

```
cwd /fast/scratch/hyaku/kake-r73/ExecRegistryRow/clone
node scripts/freshness-sweep.mjs --offline
exit 1
stderr: empty — `grep -c "Error" sweep-B.err` → 0 (no `Error:` line)
§paths  191 files · 708 occurrences · 107 unique tokens
  citation base: 107 targets · missSet 65 · files 191
  relative-form cites (outside PATH_RE, not resolve-checked): 3036 — e.g. SKILL.md:27 fleet/grokbots.json …
VERDICT: DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet (exit 1, partial: offline)
```

The named drift is the pre-existing `~/projects` NEW MISS, present identically at state A (no row), so
it is not attributable to this seat. Exit 2 is gone: the sidecar binding for `corpus/SOURCES.md:140`
now loads.

### (c) c72 /tmp-citation counter

```
cwd /fast/scratch/hyaku/kake-r73/ExecRegistryRow/clone
python3 -B .ufo/waves/round-72/c72_tmp_v2.py \
    --lane /fast/scratch/hyaku/kake-r73/ExecRegistryRow/clone \
    --revision 75e1dc1244f83ce2c6fc2a64ab353ae3c7cf2d62
exit 0
C2v2 revision=75e1dc1244f83ce2c6fc2a64ab353ae3c7cf2d62 brace_findings=0 command_findings=0
     prose_findings=0 findings=[] removed=8 added=16 guard=ok met=True
```

(At state A: `revision=aa528b2dfbd05385de694e7465be63fd3a04b172 … removed=8 added=8 guard=ok met=True`,
exit 0 — same as the base control `controls/c2-c72-base.txt`.)

### (d) c70 pointer counter (contract harm check, measured)

```
python3 -B .ufo/waves/round-70/c70_pointer_audit.py \
    --root /fast/scratch/hyaku/kake-r73/ExecRegistryRow/clone \
    --revision 75e1dc1244f83ce2c6fc2a64ab353ae3c7cf2d62 \
    --work /fast/scratch/hyaku/kake-r73/ExecRegistryRow/c70work
exit 0
pointers=359 dangling=17 annotated=17 unannotated=0 met=true
```

Byte-identical to `controls/c1-pointer-base-c70.txt` apart from the harness `+++` header. The counter
reads `SCORECARD.md` only (`show = git(root, ['show', revision + ':SCORECARD.md'])`, line 80), and
SCORECARD.md is untouched by this seat.

## 5. Non-disruption, isolated: state A (re-pin only) vs state B (re-pin + row)

| Measurement | State A `aa528b2d` | State B `75e1dc12` | Delta caused by the row |
|---|---|---|---|
| c66 summary | not run at A (see below) | `members=28 evaluated=28 mismatches=3 structural=0 agreement=25 scores_held=3/3 met=True`, exit 0 | none vs base control (measured at B) |
| sweep exit / verdict | 1 / `DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet` | 1 / same sentence | `diff sweep-A.out sweep-B.out` → one line: relative-form cites `3034` → `3036` |
| sweep stderr `Error` count | 0 | 0 | none |
| c72 summary | `brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=8 added=8 guard=ok met=True`, exit 0 | same, `added=16`, exit 0 | only the added-line count (8 → 16; 8 are round-72's own vs c72's BASE `cc6b4e0b`) |
| SKILL.md sidecar pins | 25/25 valid (implied by the sweep loading the sidecar) | 25/25 valid | none |
| sidecar entry count / pins | 174 entries; `corpus/SOURCES.md:140` → `4e408131…` | identical | none |

The two extra relative-form cites are the block's two newly cited relative paths,
`.ufo/waves/round-73/contract.md` and `.ufo/waves/round-73/attack-corpus.txt` (the counter path is `.py`,
outside the cite extension list; `corpus/knowledge/freshness-sidecar.json`, also named in the prose, was
already cited at base — `git show c1f3d8d4…:SKILL.md | grep -c freshness-sidecar.json` → `2`, lines 510
and 528). That class is explicitly informational (`outside PATH_RE, not resolve-checked`) and changes
no verdict.

## 6. Findings caused by the row

- **None with a line number of its own.** The row (line 1404) and its section prose (line 1400) add
  0 c72 findings, 0 sweep resolve-checked citations, 0 sidecar bindings, 0 c66 population members,
  and no SCORECARD/LOG bytes. The only measured delta anywhere is the informational relative-cite
  count (`3034 → 3036`), which is the sweep's declared not-resolve-checked class.
- The base `paths sidecar binding invalid: corpus/SOURCES.md:140` (exit 2) is removed by the re-pin
  (state A), not by the row; the row is not needed for that and does not change it.

## 7. Cleanup and write scope

- Scratch tree `/fast/scratch/hyaku/kake-r73/ExecRegistryRow` (307 MB: clone + c66/c70 work dirs +
  captured stdout/stderr) removed with `rm -rf --`; `test -e <scratch>` → exit 1 afterwards (absent).
- Lane checkout: only `.ufo/waves/round-73/w1/ExecRegistryRow.md` written. No `git add/commit/checkout/
  reset/stash/pull/push`, no jj command, no lane file other than this report.
- No file under `~/.local/bin` or any other PATH directory was created or modified; no pacman
  transaction was run.

## 8. Risks and blockers (for the integrator)

1. **Sequencing / dependency (not a blocker for the row text).** The row's command,
   `--lane`/`--corpus`/`--selftest` flags and 0/1/2/64 exits are the contract's documented interface;
   the counter file itself is delivered by seat `ExecC2Counter` and does not exist at base
   (`ls-tree` round-73 count `0`). The row must be committed **with or after** the counter; landing it
   alone registers a gate whose command cannot run.
2. **Re-read the row against the delivered counter before landing.** If the delivered `c73_tmp_v3.py`
   names its flags differently (e.g. a `--root`/`--base` form), cell 3/5 and the `0=met` sentence in
   cell 4 must be re-drafted to the delivered bytes — the frozen part is the predicate (contract § C2),
   not my quoting of the CLI.
3. **Label risk.** Cell 2 says `gate (live; …)`. Under a future c66-style label check a `live` row needs
   a green run at the measured revision; if the counter lands red, the label must become
   `historical`/`never met` **with a 40-hex ancestor pin** (the round-72 `c56_selftally` relabel is the
   precedent). This row must not be relabelled without a pin.
4. **Placement dependence.** The section is non-disruptive *because* it is appended after line 935. If a
   later edit moves the section above any `SKILL.md` sidecar pin line, the 25 pins break and the sweep
   returns exit 2 at `loadPathSidecar`. Any future row must keep the same append-at-EOF discipline or
   re-pin the sidecar in the same commit.
5. **c66 population boundary.** The row's path matches `POP_RX` and is excluded only by the counter's
   rounds 48–59 filter (`population_candidates(...) → []`, measured). Extending that filter to round 73
   would make this row a population member and require it to satisfy the full member grammar
   (8 non-empty cells, a `Verdict map` with `0=`/`1=`, a runnable argv) — which it already does, but the
   green/red outcome would then gate `members`/`evaluated` counts.
