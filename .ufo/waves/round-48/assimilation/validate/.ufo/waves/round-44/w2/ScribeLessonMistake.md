# ScribeLessonMistake — round-44 wave-2 lesson mining (one mistake)

Axes: **operability** (evidence identity, causal attribution of a scored control) and
**freshness** (provenance of the cited artifacts). No round judgment, admission, or score is made
here; the canonical judge owns that.

## What was mined

One mistake, written as entry **12** under `## Mistakes` in `corpus/lessons/round-44.md`, in the
`corpus/lessons/round-43.md` entry format (`N. class - evidence pointer - captured-by - fix`,
plus the round-43 `Able to fail` clause):

> **Class: a manifest class label treated as causal proof — one control attributed to a mechanism
> its source does not contain (round 44, found by the wave-1 critics).**

The inherited round-44 evidence carries the manifest row `buildport-m6` labelled
`portdigit / G9` in every inherited receipt, while the control's own source flips the
**default-port branch** and holds no memo or cache construct at all. The wave-1 critics caught it
before any claim receipt existed (`CriticClaimC1` attack (a3); `CriticMathDenominator` finding 2
and table row 25); the L1 recorded the correction at `SCORECARD.md:3551` ("Round 44 — pre-freeze
correction 2", item 2) and the manifest row now reads `default_port / G2`.

The mined entry names the artifacts that now prevent recurrence: the frozen manifest
`.ufo/waves/round-44/controls-27.tsv` (row 26 = `default_port / G2`, sha256 `a1f0e364…`, changed
from the `233afa37…` the wave-1 critics pinned) and the frozen audit driver
`.ufo/waves/round-44/c44_audit.py` (sha256 `8ee2c8bf…`), which writes the label **and** the caught
keys into every receipt (`class` / `classCaught` / `legacyCaught`, `c44_audit.py:199-200`), so a
label that does not match the mechanism stays visible per row. The entry also states plainly that
the label is **not** a witness gate (`semantic_witness` accepts any class key,
`c44_audit.py:63-66`) — the guard is the manifest row plus the receipt-level label-vs-caught
exposure, not the predicate.

Numbering: round-43's `## Mistakes` ends at 11 (`corpus/lessons/round-43.md:37,77,86,94`), so the
new entry continues the lane's counter at 12.

## Named attack — pass/fail

The item names two candidate attacks; this seat mined the second one and answers against it
explicitly.

| Named attack | Verdict | Decisive fact |
|---|---|---|
| buildport-m6 manifest misattribution (control labelled `portdigit / G9`, mechanism is a default-port branch) | **FAIL — the defect is present in the inherited evidence** | inherited receipts `verification/freeze/control-v4blind.json`, `verification/placebo/before.json`, `verification/smoke-v4.json` all record `family=portdigit class=G9` for `buildport-m6`; the control source flips the default-port branch and has 0 `memo`/`cache` hits |
| — is it fixed in the current lane state? | **PASS (fixed before scoring, evidence preserved)** | manifest row 26 now reads `default_port / G2`; manifest sha256 changed `233afa37…` → `a1f0e364…`; the claim receipt records `buildport-m6` as `default_port / G2` with `classCaught ["G2","G4","G9"]` |
| (not mined) original v4 counter blind to the 27 live-seat controls scored as a class instrument | **not mined by this seat** — reported as out of scope for this entry, not as a finding | the v4 blindness is recorded by the L1 at `SCORECARD.md:3508-3520`; this seat mined one mistake only, as the item requires |

## Exact commands and verbatim decisive output

All commands were run from the lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`. No counter
run, no audit scoring run, no build, no test, no formatter, no git/jj write, no commit, no push,
no install.

### 1. Scratch directory

```sh
mkdir -p /fast/scratch/hyaku/kake-r44/ScribeLessonMistake
```

Exit 0; no output.

### 2. Hashes of the artifacts the lesson cites

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && sha256sum .ufo/waves/round-44/controls-27.tsv .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-44/c44_audit.py && ls .ufo/waves/round-44/classes/
```

```text
a1f0e364dad5ff937666966a16622e6895591a2eb3db714d6ecf3f3948c31bf8  .ufo/waves/round-44/controls-27.tsv
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
__pycache__
g10_headtail_windows.py
g1_longport_grammar.py
g2_default_port.py
g3_empty_path.py
g4_port_scope.py
g5_prefix_cut_45plus.py
g6_fold_pairs.py
g7_band_memos.py
g8_host_tables.py
g9_port_digits.py
```

### 3. Decisive evidence script (read-only)

```sh
python3 -B /fast/scratch/hyaku/kake-r44/ScribeLessonMistake/evidence.py
```

Exit 0. Verbatim output:

```text
MANIFEST_SHA now=a1f0e364dad5ff937666966a16622e6895591a2eb3db714d6ecf3f3948c31bf8 pinned_by_w1_critics=233afa37d6ce85b0cbbedba8fe941de25f96d13773d3d388d68cbd9ab182eb57 changed=True
MANIFEST_ROWS 27 unique_names=27
MANIFEST_ROW buildport-m6 line=26 family=default_port class=G2 path=.ufo/waves/round-44/controls-r43/buildport-m6-default-branch.py
MANIFEST_ROW_CONTROL_SHA declared=68f3750025531d7815d6ec665432536abc3b0c78a036fdb49339e1f73bcbe87e on_disk=68f3750025531d7815d6ec665432536abc3b0c78a036fdb49339e1f73bcbe87e match=True
PORTDIGIT_ROWS [["portvalue-digits", "G9"], ["portvalue-digits-67", "G9"], ["portlen-v4", "G9"]]
G2_ROWS [["buildscheme-M5", "G2"], ["buildport-m6", "G2"]]
RECEIPT freeze-v4blind sha=4957875178e5 buildport-m6 family=portdigit class=G9 met=True caughtBy=[] classCaught=None
RECEIPT placebo-before sha=3490d46dc8f1 buildport-m6 family=portdigit class=G9 met=True caughtBy=[] classCaught=None
RECEIPT smoke-v4 sha=5638b6a75b58 buildport-m6 family=portdigit class=G9 met=True caughtBy=[] classCaught=None
RECEIPT claim-after-v5 sha=2383efaee0fe buildport-m6 family=default_port class=G2 met=False caughtBy=['G2', 'G4', 'G9'] classCaught=['G2', 'G4', 'G9']
CONTROL_SRC 299:             return None
CONTROL_SRC 300:         port = parts.port
CONTROL_SRC 301:     except ValueError:
CONTROL_SRC 302:         return None
CONTROL_SRC 303:     if port is not None:
CONTROL_SRC 304:         port = 80 if scheme == "http" else 443
CONTROL_SRC 305:     path = parts.path or "/"
CONTROL_SRC 306:     return (scheme, host.lower(), port, path)
CONTROL_SRC_PATTERN \bmemo\b hits=0 lines=[]
CONTROL_SRC_PATTERN \bcache\b hits=0 lines=[]
CONTROL_SRC_PATTERN _parse_url.*memo hits=0 lines=[]
CONTROL_SRC_PATTERN port_digits hits=0 lines=[]
G9_MODULE 1: """G9 port-digit caches and default-port scope comparisons for round 44.
G9_MODULE 10: The default-port control maps explicit ports to the scheme default but leaves an absent
G9_MODULE 50: # The branch maps an explicit non-default port to the scheme default. Pairfile's
G2_MODULE 1: """G2 (round-44 class run): explicit default-port authority comparisons.
G2_MODULE 4: five clean locations under that sitemap directory. HTTPS locations omit :443,
G2_MODULE 6: mistakenly treats as 80. HTTP mirrors use explicit :80 on the sitemap URL.
AUDIT 6: run divergence (A-F, T1-T5 keys) is reported as legacyCaught and never witnesses a class.
AUDIT 63: def semantic_witness(row, class_keys):
AUDIT 199: "classCaught": [k for k in (r.get("caughtBy") or []) if k in class_key_set],
AUDIT 200: "legacyCaught": [k for k in (r.get("caughtBy") or []) if k not in class_key_set]}
AUDIT_SHA 8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75
SCORECARD 3551: 2. **One manifest row misattributed (CriticClaimC1 a3, CriticMathDenominator finding 2).**
```

Reading of the decisive lines: the manifest has been edited since the wave-1 critics pinned it
(`changed=True`), the row is now `default_port / G2`, the three inherited receipts still carry the
old `portdigit / G9` label, and the control source contains the default-port branch and **no**
memo/cache construct — so the label was metadata, never the mechanism.

### 4. Audit driver selftest (witness classifier; no counter execution)

```sh
python3 -B .ufo/waves/round-44/c44_audit.py --selftest
```

```text
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
EXIT=0
```

### 5. Lane freshness gate re-run after the lesson edit (read-only, `--offline`)

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && timeout 300 node scripts/freshness-sweep.mjs --section=paths --offline
```

Decisive lines:

```text
§paths  104 files · 627 occurrences · 101 unique tokens
  resolve 26 · declaredAbsent 65 · drift 0 · unresolved 10
  set-delta miss: no new miss
VERDICT: OK (exit 0, partial: offline)
EXIT=0
```

The mined entry cites lane-relative paths only; it adds no new drift and no new miss.

## Files written by this seat

1. `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-44.md` — appended entry **12**
   under `## Mistakes` (the only lane-content write of this seat).
2. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w2/ScribeLessonMistake.md` —
   this report.
3. `/fast/scratch/hyaku/kake-r44/ScribeLessonMistake/evidence.py` — the read-only decisive script
   (scratch only).

No frozen artifact, counter, class module, receipt, manifest, SCORECARD entry, state file, fleet
file, or sibling-lane file was edited. No `git`/`jj` write, no commit, no push, no install or
update of any tool (none was needed; `python3` and `node v24.21.0` were already present). No
subagent dispatched.

## Bounds, coordination, blockers

- The mined entry names only artifacts this seat read directly: the manifest, the four receipts,
  the control source, the two class generators, the audit driver, the wave-1 critic reports, the
  r43 originating report, and the SCORECARD correction line.
- Peer `kake-r44.ScribeC2Repairs` was notified before the append (same `## Mistakes` section of the
  same lesson file) to avoid a numbering/anchor collision; the file was re-read immediately before
  the edit and the anchor `## Mistakes` was unique at that moment (no other entry existed).
- Unrun by this seat, and therefore **not** claimed: any counter, probe, audit scoring run, build
  scoring, canary run, placebo run, or ledger check; the G6 casememo build item; the `k/27`
  placebo figure; the 23/27 vs 27/27 witnessing state. The lesson entry asserts nothing about them.
- No blocker. The evidence needed for the mined mistake was all present in the lane tree.

Report: `.ufo/waves/round-44/w2/ScribeLessonMistake.md`
