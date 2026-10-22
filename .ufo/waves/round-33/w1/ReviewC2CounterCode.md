# ReviewC2CounterCode — attack on .ufo/waves/round-33/c2_pin_count.py

Sandbox: /fast/scratch/hyaku/kake-r33/w1/ReviewC2CounterCode/ (clone at HEAD=bc6c4a8d435473f3c30903210be30d9d6e3ef750, the frozen declaration rev). Upstream blob ids in `PINNED` (lines 44-49) verified equal to `git ls-tree -r 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` of /fast/scratch/hyaku/kake-r33/ds4cc-upstream; sitemap uses the standard 0.9 namespace (100 locs); all three frostbite pages carry matching self-canonicals.

Baseline: at bc6c4a8 the counter reports met=0 (pre-implementation). To exercise each check I built a compliant rev G1=539c991291548d40b56414254ce9eeecc620380b (retained bytes by `git show` from upstream read-only clone, S065 row, "## Round-33 ds4cc source pin 7fc6aa2f" section, sitemap-locs: 100, three `canonical <url>: clean` lines) → met=4, exit 0. All mutants below are commits on G1; every run exited 0 unless marked CRASH.

## Round-32 defects: status

- **F1 row-id pin — FIXED.** c2 requires exactly one Registry row whose first cell equals `S065` (lines 120-128). m-fake-row-preamble: a compliant-looking `S900` row planted in preamble prose before `## Registry` → rowsFound=1, met=4 (decoy ignored). m-dup-s065-row: a second `S065` row → rowsFound=2, met=3 (ambiguous registry fails, not silently accepted).
- **F2 substring "## Registry" window — FIXED for text, still present via fences.** `section()` now requires an exact line `## Registry` (line 73), so prose "see ## Registry" no longer opens the window (same m-fake-row-preamble rev). But equality is not fence-aware: m-fence-registry (a fenced block containing a literal `## Registry` line above the real heading) → headings=2, window=None, c2=false, met=3 — a false negative on otherwise-compliant content.
- **F3 naive `split("|")` — FIXED for `\|`, new edge defects remain.** `(?<!\\)\|` (line 119) keeps an escaped pipe inside a cell: m-escpipe met=4. Two residual parse divergences, both demonstrated: (a) `cells[1:-1]` assumes a trailing pipe — m-no-trail-pipe (S065 row rendered `... | corpus/knowledge/sitemap-orphan-audit.md` with no closing `|`, legal GFM) → last cell eaten, rowCells=10... counter reports rowsFound=1 but c2 false, met=3; (b) `\\|` (literal backslash then cell break, renders as 12 cells) is merged by the counter into 11 — m-backslash-pipe met=4 while the rendered table's cell contents differ from what was checked (parser/renderer disagreement, exploitable in the false-positive direction).
- **F4 `## ` inside a fence truncates the window — STILL PRESENT, unchanged.** Line 78 `line.startswith("## ")` is not fence-aware. m-fence-trunc-registry (fenced `## fenced` inside Registry before the S065 row) → rowsFound=0, met=3. m-fence-trunc-entry (same inside the audit section before the `canonical` lines) → c4 false, met=3. False-negative direction in both files.
- **F5 path-blind c1 — FIXED.** Per-path `git ls-tree -z rev -- RETAIN_DIR/<path>` plus `name ==` equality (lines 101-107). m-mv-retain (`git mv` of the retained dir to `attic/`) → c1 false, met=2. m-lookalike-dir (extra copies under `ds4cc-7fc6aa2fX/`) → met=4, extras correctly ignored.
- **F6 mode-blind c1 — FIXED.** `mode == "100644"` required (line 107). m-exec-mode (chmod +x sitemap.xml → 100755, same blob id) → c1 false, met=2; symlink class covered by the same check.
- **F7 anywhere-cite — FIXED.** c3 requires both `S065` and the hash inside the single `HEADING` section only (lines 132-135). m-intro-cite (S065 + hash in the intro, section absent) → headings=0, met=2. m-dup-heading (second exact heading) → headings=2, met=2.

## New defects

- **N1 crash on non-UTF8 SOURCES.md (MEDIUM).** `show()` line 68 decodes strict UTF-8; m-nonutf8-sources → UnicodeDecodeError traceback, exit 1, no JSON — violates the "exit 0 when the count ran" contract. Same path for ENTRY.
- **N2 crash on large `sitemap-locs` integer (LOW).** `int(stated[0])` line 154: m-bigint (`sitemap-locs: ` + 5000 nines) → ValueError (int-str limit), exit 1, no JSON.
- **N3 substring cite weakness (LOW).** `ROW_ID in body` (line 135) is substring, not word-boundary: m-s0650 (section cites only "S0650") → met=4 with no actual S065 mention. Literally satisfies the declared spec text "contains S065", so a spec weakness as much as a counter one. Same shape for `ENTRY in cells[10]` (line 126): `.../sitemap-orphan-audit.md.bak` would pass.
- **N4 strict-equality heading fragility (LOW).** m-heading-trail-sp (`## …7fc6aa2f ` trailing space, still an ATX heading per GFM) → headings=0, met=2.
- **N5 unreachable-but-unhandled ET.ParseError.** Line 150 has no try: a malformed retained sitemap would crash like N1. Currently unreachable — c1 pins the blob id to a file that parses — so noted, not demonstrated.

## Checks with no defect

Manifest path resolution is correct: `manifest-N.json` is written inside the extracted retained dir (line 158) and canonical_audit resolves `file` relative to the manifest dir (canonical_audit.py:581-615, no-follow/descend-by-fd); `rel` paths like `magga/frostbite/index.html` resolve there. c4 uses the revision's own scripts/canonical_audit.py via `git archive` (lines 144-148), has a 120 s timeout, and rejects lies: m-lie-verdict (stated `failed-policy` vs observed `clean`) → c4 false. Stated-verdict regex `^canonical <url>: (\S+)$` requires exactly one matching line; fenced duplicates count, so a fenced wrong verdict fails c4 — safe direction.

## Commands and revs (all under the sandbox clone, exit 0 unless CRASH noted)

`python3 -B .ufo/waves/round-33/c2_pin_count.py --rev HEAD --repo .` per mutant commit; G1=539c991, mutant revs recorded by `git commit` in sandbox only (m-fake-row-preamble, m-fence-registry, m-escpipe, m-no-trail-pipe, m-backslash-pipe, m-mv-retain, m-exec-mode, m-s0650, m-dup-head, m-intro-cite, m-nonutf8, m-bigint, m-fence-trunc-reg, m-fence-trunc-entry, m-dup-row, m-lie-verdict, m-head-trail-sp, m-lookalike-dir).

## Not verified

`--rev` resolution edge cases; non-default `--repo`; behavior when `git archive` partially fails; performance on adversarial SOURCES.md size. No lane files mutated; this report is the only lane write.

Tooling: none installed (pacman paused; host python3 is 3.14.8 — `tarfile.extractall(filter="data")` at line 148 requires ≥3.11.4/3.12, satisfied here but a hard floor on older hosts).
