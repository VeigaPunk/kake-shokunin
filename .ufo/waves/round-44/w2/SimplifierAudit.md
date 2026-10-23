# SimplifierAudit — YAGNI review of c44_audit.py + ledger_latest_check.py

Axes: **operability** (one counting command, no duplicate authorities) and **freshness**
(receipt fields traceable to consumers). Frontier walked: full source read of both files
(reviewed bytes: `c44_audit.py` sha256 `8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75`
— the pinned frozen bytes; `ledger_latest_check.py` sha256
`50384505b981352b691f24fbdd66c521c18b80408aeed4bbb54c70f8903f63dd`), consumer grep across the
whole lane (spec generators, dispatch JSON, SCORECARD/LOG, w1/w2 reports, all code), receipt
inspection of `verification/claim/*.json`, truth-table evaluation of `expectation_ok`, and two
real 1-row audit runs. No lane file was edited; all scratch lives under
`/fast/scratch/hyaku/kake-r44/SimplifierAudit/`.

## Headline answers

1. **`--expect blind` vs `--expect not-met` differ observably — proven, not just statically.**
   On the same scored input (1-row TSV, `portlen-v1`, `--classes v4`, met=True):
   blind → `ok=True`, exit 0; not-met → `ok=False`, exit 1. The modes partition the `met`
   polarity: blind requires every row `met is True` (plus zero class-witnesses); not-met
   requires every row `met is False`. `expectation_ok` truth table:

   ```
   met=True clean         blind=True  witnessed=False not-met=False
   met=False no catch     blind=False witnessed=False not-met=True
   met=False legacy key   blind=False witnessed=False not-met=True
   met=False class key    blind=False witnessed=True  not-met=True
   met=None error         blind=False witnessed=False not-met=False
   ```

   Real-receipt corroboration: `verification/claim/canary.json` passed under `not-met`
   (`ok:true`, witnessed 3/5 — the three r42 canaries carry G-class catches); the identical
   rows under `blind` would be `ok:false` on two independent conjuncts (met≠True AND
   witnessed≠0). Keep all three modes; each has a dispatched consumer in `make_w2_spec.py`
   (blind→ExecV4Support+ExecBuildMeet, witnessed→ExecG6FoldFix+ExecBeforePlacebo,
   not-met→ExecCanary).

2. **Every `--selftest` fixture is referenced by a discriminating assert** — none is dead:

   | c44_audit.py fixture (L85-89) | Kill rule it anchors |
   |---|---|
   | `passing` (met=True) | L92 kills "any row counts as witness"; L98 pins blind's met=True requirement |
   | `class_divergence` `["G2"]` | L93 kills "no key counts"; L97 (with `set()`) kills "class_keys ignored"; L100 kills "witnessed doesn't require a witness" |
   | `v4_divergence` `["D"]` | L95 kills "any met-false = witness" (m3 of MutClassGate); L99 kills "blind accepts not-met"; L103 pins not-met |
   | `mixed_divergence` `["D","G3"]` | L94 kills the historical "every caughtBy key must be a class key" bug (m1 of MutClassGate) |
   | `legacy_divergence` `["C","D"]` | L96 kills "legacy keys count" and m2 (any-divergence witness) |
   | ledger check `matching`/`mismatching` (L251-260) | `should_match` pair kills "always-MATCH"/"always-MISMATCH" and m1 (containment); `latest_match` on 2-line fixtures kills m2 (first-match) |

   No unreferenced fixture found in either file.

## Deletion proposals — `c44_audit.py` (two dead writes; no observable change)

Both are **fields written to memory that no reader ever sees**: the summary-row projection
at L197-201 enumerates its keys explicitly and drops anything else, and nothing prints them.

- **D1 — `toolSha256=got` at L150 and L157-160** (both `dict(row, …)` constructions in
  `score()`). The variable `got` stays (it drives the `got != row["sha256"]` check at L149);
  only the two kwargs are dead. The field never reaches the receipt (`sha256` from the TSV is
  what rows carry), and the file is already frozen — a mismatching tool errors at L150 before
  `toolSha256` could matter. Receipt bytes unchanged: `toolSha256` does not appear in any
  committed receipt under `verification/` (verified by inspecting row keys of
  `after-v5-wave2-baseline.json`, `canary.json`, `v4-support.json`, `placebo-before.json`).
- **D2 — `"seat": seat` in the row dict at L143**. Column 6 of the TSV is parsed (the tuple
  unpack at L141 must still consume it) and then never read: not in `score()`, not in the
  summary projection, never printed. Keep the `seat` *variable* in the L141 unpack (it pins
  the TSV's 6-column schema); drop only the dict member. Receipt bytes unchanged — `seat` is
  absent from every committed receipt row.

Neither file may be edited this wave (frozen); these are recorded for the L1's pre-freeze
trim or the next round.

## Considered, recommend KEEPING (dead-looking, but legibility/defense is the point)

- **`expectation_ok` implied conjuncts.** In blind (L75), `not witnessed` is logically implied
  by `all(met is True)` since `semantic_witness` requires `met is False` — it can never be the
  sole failing clause. Similarly `not errors` (L75,78,81) is implied by
  `total == expected_rows` when an error row always shrinks `total`. They mirror the docstring
  clauses verbatim; deleting saves nothing measurable and costs contract legibility.
- **`isinstance(key, str)` at L66**: unreachable in practice (`rec["runs"]` keys come from
  `json.load`, always `str`), but it is a 4-token guard against a counter that emits a
  non-dict `runs`. Keep.
- **`--label` (L119, 187, 211-212)**: *functional* but **no dispatched command passes it** —
  every committed receipt has `"label": ""`. Deleting it (hardcode `"kake-r44"`) is a
  legitimate third micro-trim; I list it as *optional* rather than a proposal because it is a
  working feature, not dead code, and receipt tagging is a plausible operator want.
- **Summary fields `label`, `verdict`, `metNames`, `witnessedNames`, `notMetNames`,
  `witnessedByClass`, `classCaught`/`legacyCaught`, row `exit`/`equalRuns`/`seed`, build
  `ratios`**: no *programmatic* consumer exists — the claim is read from `ok`, `witnessed`,
  `notMet`, `build[*].met`, and report prose. They are the receipt's evidentiary surface
  (LOG.md:3547 explicitly names `classCaught`/`legacyCaught` as the mixed-key visibility fix;
  ExecBuildMeet's item instructs quoting build `ratios` against the 2.0 bound). Deleting
  evidence surface to save JSON bytes would harm freshness, not operability. Keep all.
- **`run_counter` stdout tail `so` (L61)**: consumed only when the counter writes no JSON
  (error fallback at L160/180). Live for the error path. Keep.

## `ledger_latest_check.py` — no deletions; trace that justifies each kept branch

Mechanical scan: `uvx ruff check --select F401,F841,F811,F601` → `All checks passed!` (both
files). Branch-level trace:

| Branch | Why it stays |
|---|---|
| `load_spec` full-document equality vs `contract_spec()` (L110-111) | The declared C2 attack-resistance: `ledger-quotes.json` is a *pin*, not config — a spec edit that narrows scope is rejected verbatim. Confirmed: on-disk spec equals the embedded contract byte-for-byte in structure. |
| `parse_constant` throw lambda (L63-65) | Fails closed on `NaN`/`Infinity` in a *receipt* (stdlib `json` accepts them by default). Uneditable receipts at master make this a guard, not a feature. |
| `rescore_receipts` pattern != literal check (L123-124) | Same fail-closed pin — contract fixes the glob; any spec divergence is an `InputError`. |
| `derive_values` `raise InputError(unsupported kind)` (L184) | Contract-pinned unreachable, but it is the exhaustiveness guard that makes the equality pin load-bearing. |
| `run_selftest` `name == "mismatching" and not actual` (L269-273) | Live reachable branch (fires on the second fixture); produces the "shown red" evidence ExecLedgerCheck's acceptance requires. |
| `main(argv=None)` (L278) | Standard injection hook for a mutation/copy seat to drive `main([...])` without subprocess; pattern kept by prior round YAGNI reviews. |
| `latest_match` returns `(match, line)`; `_line` unused in selftest (L265) | The tuple keeps `run_check`'s `file:line` provenance print; intentional discard. |
| `NUMBER_RE` / `ROUND_HALF_UP` / `isinstance(raw,bool)` guards | Reject non-decimal quotes and bool-typed receipt ratios — the receipt-vs-quote comparison's type safety. |
| `--root` default `parents[1]` (L289) | Exercised by the C2 counting command `python3 -B scripts/ledger_latest_check.py` (no args) in the wave-1 before run. |

## Verification transcript (verbatim, decisive commands)

```text
$ python3 -B .ufo/waves/round-44/c44_audit.py --selftest
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
$ echo $?
0

$ python3 -B scripts/ledger_latest_check.py --selftest
ledger_latest_check --selftest
  PASS matching fixture MATCH quoted=14 derived=14
  RED MISMATCH mismatching fixture quoted=18 derived=14
selftest: 2/2 passed
$ echo $?
0

# same 1-row controls file (portlen-v1), --classes v4, frozen counter:
$ python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .../one-row.tsv \
    --counter .ufo/waves/round-44/c44_count_v5.py --classes v4 --expect blind \
    --workers 1 --out .../blind/out.json
AUDIT kake-r44 classes=v4 classKeys=- witnessed=0/1 (no class runs; witnessed=0 by construction) notMet=0 build_met=0/0 ok=True counter=5cedaa3b9f91
  portlen-v1           G1         met=True  caught=-
$ echo exit code → 0

$ python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .../one-row.tsv \
    --counter .ufo/waves/round-44/c44_count_v5.py --classes v4 --expect not-met \
    --workers 1 --out .../notmet/out.json
AUDIT kake-r44 classes=v4 classKeys=- witnessed=0/1 (no class runs; witnessed=0 by construction) notMet=0 build_met=0/0 ok=False counter=5cedaa3b9f91
  portlen-v1           G1         met=True  caught=-
$ echo exit code → 1

$ uvx ruff check --select F401,F841,F811,F601 c44_audit.py ledger_latest_check.py
All checks passed!
```

## Pass/fail against the item's named attack

Item's attack: *find dead code, unused flags, or unconsumed receipt fields; check blind vs
not-met equivalence and selftest-fixture kill coverage.* **PASS (review completed with two
proposals):** the claimed equivalence between `--expect blind` and `--expect not-met` is
*refuted* — opposite exit codes observed on identical scored input; all selftest fixtures are
kill-referenced; exactly two dead writes found (`toolSha256=got` ×2, `"seat": seat`) plus one
optional unused-flag trim (`--label`). `ledger_latest_check.py`: zero deletions — every
branch traced above.

## Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w2/SimplifierAudit.md` (this report)
- `/fast/scratch/hyaku/kake-r44/SimplifierAudit/one-row.tsv` (1-row controls fixture)
- `/fast/scratch/hyaku/kake-r44/SimplifierAudit/{blind,notmet}/out.json`, `out.txt` (+ earlier `blind.json`, `notmet.json` at scratch root)

## Tool installs

- `ruff 0.17.1` via `uvx ruff@latest` (uv tool channel; pacman paused) — mechanical
  unused-name/import scan (F401/F841/F811/F601), clean on both files.

## Blockers / notes

- None. Both target files are frozen (proposals only, as the item requires — "propose
  deletions with line numbers").
- Observed adjacent dead weight (outside this item's two files, for the L1's awareness):
  `verification/{after-v5,canary,v4-support,placebo}/` are empty dirs, and the top-level
  `verification/tools/` dir is empty — stray dirs from `--out <dir>` runs, not consumed by
  any command.
- `v4-support.json` (wave-2 repro) currently shows `ok:false, notMet=1` — one control scored
  met=False under `--classes v4` this wave. Not this item's scope; flagged for the L1.
