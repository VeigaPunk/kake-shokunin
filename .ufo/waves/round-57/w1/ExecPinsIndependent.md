# ExecPinsIndependent

Claim C1 (calibration), independent re-derivation of the committed revision-pin relabel set.
Lane `kake-shokunin`; base `28fa0b23e699303725aba2727094531f5e44494d`; tip read
`f7c98ff269286723077848f3caf1422c4004f46d`; round date 2026-10-25.
`.ufo/waves/round-57/c57_receipt_pins.py` was **not** used to derive anything below — no import, no
subprocess call, no copy of its output. It was read afterwards only to characterise its `POP_RE` /
`REV_RE` for the "would the counter see it" columns, and executed exactly once, as `--selftest`.

SCRIPT:

`python3 -B .ufo/waves/round-57/w1/ExecPinsIndependent.files/relabels.py [--json <file>]`
(stdlib only; read-only `git log` / `git show` / `git ls-tree` / `git grep` / `git rev-parse`).

- Phase 1 — streams `git log --first-parent -p --unified=0` over 18 explicit pathspecs
  `.ufo/waves/round-40 … round-57` (wider than the counter's round-52..57 `control(s)/`), pairs every
  removed/added pin line landing in the same (commit, path, key-name), and classifies the file as
  receipt-like (.txt/.json/.jsonl/.log/.tsv/.yaml/.md/…) or code (.py/.sh/.mjs/…). Key set is wider
  than the counter's: `revision|rev|sourceRevision|source_revision|measuredRevision|measured|pinned_revision`,
  optional JSON quotes, `:` or `=`, tab or space indent.
- Phase 2 — blob level: for the 87 paths with >= 2 first-parent commits, compares the set of
  (key, 40-hex) tokens of consecutive committed versions using both a line-anchored regex and a
  mid-line JSON regex, so a compact single-line JSON receipt (`{"…","revision":"<40hex>",…}`) is not
  a blind spot.
- Phase 3 — `git grep -E` over the same population at HEAD for revision-ish keys, marking each line the
  counter's `^[ ]*revision[:=]` would not match.
- Phase 4 — reads the six `UNDISCLOSED` lines of `.ufo/waves/round-57/controls/base-c1-receipt-pins.txt`
  and confirms/denies each against the derived set.

Run at tip: `commits_scanned=86` (first-parent commits touching the population), `diff_blocks=11845`,
`commit_path_buckets=2945`, `relabels_total=8` (6 receipt-like + 2 code), `pin_strips=0`,
`same_value_reformats=0`, `pin_introductions=3075` (first pin in a file — dominated by newly added
receipts and by the vendored `*/assimilation/{validate,pre-append}/` mirrors; not relabels).
Blob phase: 87 multi-commit paths, `blob_relabels=6`, `not_seen_by_line_pairing=0`.
First-parent gap closed: the 3 non-first-parent commits (`0bc04e4`, `58f9f04`, `7c9f28f`) touch no
pin line under the population (checked with `git show -m`).
Artifacts: `ExecPinsIndependent.files/relabels.py`, `relabels.out.txt` (full run), `relabels.json`.
Nothing in this seat was left unrun.

CONFIRMED: 6 of 6 — the counter's six are exactly the receipt-like relabels my independent scan
finds, on the same from/to/commit. Spot-checked against `git show <commit> -- <path>` for rows 1, 3, 5
(full 40-hex lines printed by git, not by my script).

| # | path | from | to | commit |
|---|------|------|----|--------|
| 1 | `.ufo/waves/round-52/control/c1-ledger-real.txt` | `3a50ae4321e6` | `1ae8de5d4dee` | `a4a890cf1381` |
| 2 | `.ufo/waves/round-52/control/c2-quote-real.txt` | `3a50ae4321e6` | `1ae8de5d4dee` | `a4a890cf1381` |
| 3 | `.ufo/waves/round-55/controls/after-c1-readme-index.txt` | `faf9abe81d1e` | `64c0ce12ffe3` | `955e3d7bd6d1` |
| 4 | `.ufo/waves/round-55/controls/after-c2-quote-truth.txt` | `faf9abe81d1e` | `64c0ce12ffe3` | `955e3d7bd6d1` |
| 5 | `.ufo/waves/round-56/controls/after-c1-selftally.txt` | `f8438a282d59` | `4cb225fb032b` | `ad06cb8a17bd` |
| 6 | `.ufo/waves/round-56/controls/after-c2-quote-truth.txt` | `f8438a282d59` | `4cb225fb032b` | `ad06cb8a17bd` |

Base-control cross-check: `6 UNDISCLOSED` lines read, `6 CONFIRMED`, `0 DENIED`; derived-but-not-in-control
= the two code rows in WIDER POPULATION (no receipt-like extra). The counter's `population=45` also reproduces
independently: 45 files match `round-5[2-7]/(control|controls)/*.{txt,json}` at `28fa0b23e699`
(51 at the tip, after round-57 added its receipts).
`c57_receipt_pins.py --selftest` → `19/19` PASS, exit 0 (one run).

WIDER POPULATION: zero additional receipt-like relabels. Scanning rounds 40–57, every subdirectory,
`.json` receipts and `receipt.json` finds no seventh receipt relabel:

- Rounds 40–49/51 JSON measurement receipts (`c1-at-*.json`, `c1-before/after-*.json`, round-46
  matrix receipts, round-45 build receipts, `receipt.json` under round-45 fixtures and the round-30
  mirror) were each written once and never had a revision value rewritten. The blob phase (which sees
  mid-line tokens) confirms this for all 87 multi-commit paths.
- `receipt.json` / `*-receipt.json`: 3 non-mirror lane copies under `.ufo/waves/round-45/fixtures/`
  (two `counter-error`, one `tool-absent`) plus 2 in the round-48 mirror. Two carry
  `"revision": "<40hex>"`, one `null`, one has no pin; none was relabelled.
- `pin_strips=0` and `same_value_reformats=0` over the whole wider population — no pin line was ever
  deleted without a replacement, and no relabel-shaped pair has equal values.
- Two relabel-shaped pairs in **code**, both at `2bda8e4227a7`, correctly excluded as non-receipts:
  `.ufo/waves/round-55/c55_quote_truth.py` (`rev = os.environ.get(...) or git(...)` →
  `... or head.strip()`) and `.ufo/waves/round-55/c55_readme_index.py` (`revision=args.revision`
  call-site text). A naive `^[ ]*rev[:=]` counter would report these as relabels — a false-positive
  trap, not a miss.

MISSED KEY FORMS: the counter's `REV_RE = (?m)^\s*revision\s*[:=]\s*([0-9a-f]{40})\b` plus
`POP_RE = ^\.ufo/waves/round-5[2-7]/(control|controls)/[^/]+\.(txt|json)$`. Inside that population at
HEAD there are 28 line-start rev-ish lines and all 28 are seen by the counter — the key-form exposure
is outside it, plus one embedded-pin case inside it.

- **Inside the declared population, real:** `.ufo/waves/round-52/control/c1-mutation-ladder.json`
  carries 18 `revision: <40hex>` values per version, embedded in JSON string values
  (`"old_tail": "  revision: 6b8627be…"`), so no line-anchored regex sees them; the counter reports 0
  pins and 0 relabels for the file. Their value set changes in 3 of its 4 committed versions
  (`73c22a3 → 1ae8de5 → a4a890c → fd91527`, 18 values rewritten each time). They are the old counter's
  printed tails for mutated fixtures, not the receipt's own measurement pin — but the file is inside
  `POP_RE` and its pins are demonstrably rewritten with no errata entry.
- **Rounds 52–57, outside `POP_RE`:** `assimilation/mirror-pin.json` uses `"sourceRevision"` (rounds
  52, 55, 56, 57; 4 files) — the pre-append mirror pin; `contract.json` uses `baseRevision` (55, 56, 57)
  and `redRevision` (57); `round-53/exec-quality-gate/real-round52-tip.txt` uses `revision=` with the key
  matched but the path outside `POP_RE` (round-53 has no `control(s)/`), and its sibling
  `real-round52-tip.json` uses the quoted form (next bullet).
- **Rounds 40–51, plus round-53's `exec-quality-gate` JSON:** quoted JSON key `"revision":` at line
  start in 1198 lines / 1198 non-mirror files
  (40: 86 files, 41: 332, 42: 142, 43: 23, 44: 295, 45: 307, 47: 6, 48: 2, 49: 4, 53: 1) — the leading
  quote defeats `REV_RE`; also 4 compact single-line JSON receipts (`round-46/verification/c1-*.json`,
  `c2-*.json`) whose pin is mid-line and invisible to any line-anchored regex.
- **False-positive trap:** `round-51/sources/receipts.json` has `"docRevision": "Last updated
  2026-08-20 UTC"` (2 lines) — a page date, not a commit pin. Key-name matching alone would misread it.
- `rev=`: 106 `rev =` / `rev:` lines exist in the wider surface, all in `.py`/`.md` code and prose; no
  receipt-like file carries a `rev=` pin. Quoted `"rev": "<40hex>"` appears only in vendored mirrors
  (8 round-32 mirror JSONs; 446 mirror JSONs in total carry a quoted pin) — not lane receipts.
- No abbreviated (< 40 hex) pin exists in any receipt-like file, so `REV_RE`'s 40-hex requirement is a
  latent, not a live, miss.

RECOMMENDED COUNTER CHANGES (before data): to land before round-57 measurement is scored. Each item is
marked `[structural]` (rests only on the counter's declared `POP_RE`/`REV_RE`/docstring) or `[from
scan]` (rests on the counts above).

- R1 `[structural]` Accept the quoted JSON key: `REV_RE = (?m)^\s*"?revision"?\s*[:=]\s*([0-9a-f]{40})\b`.
  Zero cost today inside `POP_RE` (all 28 lines match already), closes the whole `"revision":` class
  for any future `.json` receipt — `POP_RE` already admits `.json`.
- R2 `[structural]` Do **not** widen to every key that contains "revision". If sibling keys are added,
  add only commit-pin keys (`sourceRevision`, `baseRevision`, `redRevision`, `measuredRevision`) and
  explicitly exclude `docRevision` (a page date); a blanket `[A-Za-z_]*evision` pattern false-positives
  on round-51 `sources/receipts.json`.
- R3 `[structural]` Pin the population boundary with a selftest. The docstring declares `control(s)/`
  only, but no selftest exercises a pin under `round-55/assimilation/mirror-pin.json`
  (`sourceRevision`) or `round-53/exec-quality-gate/` (`revision=`) — add one so the boundary is tested,
  not just described.
- R4 `[from scan]` Stop silently reporting 0 pins for a file that has them embedded:
  `round-52/control/c1-mutation-ladder.json` is inside `POP_RE`, carries 18 pins per version, has
  rewritten them in 3 commits, and the counter reports 0. Either narrow `POP_RE` (exclude
  `*-mutation-ladder.json`, or require the receipt's own line-anchored pin) or add a check that a
  population file whose text contains `revision:` but yields 0 `REV_RE` matches is reported as
  "pins not line-anchored" instead of counting as pin-free. Add the matching selftest.
- R5 `[structural]` Keep the 40-hex requirement but warn on 7–39-hex pin values inside `POP_RE`; today
  there are none, so this is prevention only.
- R6 `[from scan]` `round-52/control/final-verify.txt` holds 3 pins and the counter compares **sets** of
  revisions per version, so a permutation inside one file is invisible. No permutation exists in
  history; compare ordered lists (or multisets) if multi-pin receipts are to stay in scope.
- R7 `[structural]` No change to relabel semantics: the counter's per-version set difference and my
  independent line-pairing derivation agree on exactly the same six rows, and the blob-level pass adds
  none.

VERDICT: Six of six counter relabels independently confirmed on path/from/to/commit; zero additional
receipt-like relabels in rounds 40–57 (only 2 code-text false positives); the one in-population blind
spot is `round-52/control/c1-mutation-ladder.json`, whose 18 embedded pins were rewritten 3 times
unseen — counter selftest 19/19, exit 0.
