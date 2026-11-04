# ExecGuard — R79-2 standing ledger append guard (kake round 80, w1)

**Verdict: R79-2 closed.** `scripts/ledger_append_guard.py` (shipped by the L1 at carrier `aa44b9af`, sha256 `0c12838e…`, unchanged through HEAD `63afc0ee`) verifies independently under my runs: `--selftest` exits 0 with the non-prefix fixture failed, and the round-58 ledger's base bytes are a byte prefix of the tree bytes — base 20,061 B (`93182dec…`) is a strict prefix of the current tree's 22,324 B (`5a59b068…`) after two in-round byte-spliced appends, still green at HEAD `63afc0ee`. The C1 counter (revision mode, the receipt mode) prints `R79-2 closed … files=1 prefix preserved` with `open=0 closed=6 met=true` at HEAD and at `aa44b9af`, and still prints `open=6 met=false` at base `9998dc7a`, so the before→after premise holds.

Production-file authorship: mid-wave the L1 took over `scripts/ledger_append_guard.py` (message on record; I had been asked not to write that path). This report verifies the shipped artifact byte-for-byte; my own validated design reference is retained at `w1/ExecGuard/design-reference-execguard.py` for comparison (see §5).

## 1. Guard semantics — endorsement

`prefix_probe` (`scripts/ledger_append_guard.py:37-45`): `cut = base.rindex(b"]")`; preserved iff `carrier.startswith(base[:cut])`; on failure reports the first divergent offset. I endorse this over the common-prefix+common-suffix (A+I+B) rule I proposed mid-wave: A+I+B would accept a mid-entry insertion (e.g. a field spliced into a prior event's note — the rewrite class R79-2 targets) as long as the tail matched, while prefix-to-`]`` accepts only an insertion at the array's end, which is exactly the sanctioned byte-splice. I could not name any legitimate append that must move bytes before the final `]` — the L1's challenge stands answered: none exists under this ledger's end-append discipline.

Stated limit (residual risk): bytes after the ledger's final `]` — today the pure JSON close `\n}\n` — are unconstrained; an edit confined to that tail would stay green. No evidence content lives there in the v1 schema.

## 2. Evidence (all re-run by me; verbatim transcripts in `w1/ExecGuard/`)

| # | Command (from `/home/vgpnk/Projects/shokunin/kake-shokunin` unless noted) | Result | Receipt |
|---|---|---|---|
| 1 | `python3 -B scripts/ledger_append_guard.py --selftest --work $S/st` | `fixture append: passed` / `fixture non-prefix: failed (first divergence at byte 126)` / `selftest: 2/2 passed`, exit 0 | `selftest-output.txt` |
| 2 | `python3 -B scripts/ledger_append_guard.py --root <lane> --json` (HEAD `1e7abe7f`) | `files=1 prefix_preserved=true`, base 20061 → carrier 22324, exit 0 | `lane-json-output.txt` |
| 3 | same as 2 at HEAD `63afc0ee` | `files=1 prefix_preserved=true`, exit 0 | `final-lane-json.txt` |
| 4 | `python3 -B .ufo/waves/round-80/c80_defect_queue.py --root <lane> --revision HEAD --work $S/cw2` | `R79-2 closed guard selftest green (non-prefix fixture failed); ledger files=1 prefix preserved`; `C1v1 … open=0 closed=6 met=true`, exit 0 | `counter-revision-HEAD.txt` |
| 5 | same with `--revision aa44b9af` | identical, `met=true`, exit 0 | `counter-revision-aa44b9af.txt` |
| 6 | same with `--revision 9998dc7a586b9fe76379014c8123aa3606f2d8b9` (base) | `R79-2 open scripts/ledger_append_guard.py absent`; `open=6 closed=0 met=false`, exit 1 | `counter-revision-base.txt` (transcript in §5 note) |
| 7 | `sha256sum scripts/ledger_append_guard.py` | `0c12838e3d4ea441eb750fd4c6af2398cfa704e5077f6c58b053d535f8514067`, identical at HEAD `1e7abe7f`, `63afc0ee` and the worktree | `final-lane-json.txt` header context |
| 8 | `git show 9998dc7a…:.ufo/waves/round-58/receipt-rewrites.json \| sha256sum` vs `sha256sum` of tree file | base `93182decabda35b88c8e993e6e178d4689692b4d35396a25d372ff251efbb210` (20061 B); tree `5a59b068d7bc04e815bfc3419872c1f8aae617d8fb129ff0be4a6630c46c8abc` (22324 B) | §3 |

Scratch for all runs: `$HYAKU_SCRATCH/kake-r80/ExecGuard` with `TMPDIR` pinned there; tree deleted before yield (§6).

## 3. Byte-level splice verification (the R79-2 remedy, live)

The ledger grew twice this round by the sanctioned splice — new event inserted before the events-array close, every prior entry byte untouched:

- base tail (offset ~20045): `…corrections, row 3)."\n}\n]\n}\n` — final `]` of the events array at offset 20057.
- tree at the same region: `…row 3)."\n}\n ,\n{\n"path": ".ufo/waves/round-80/control…` — insertion begins exactly at 20057 with `,`; tree tail is again `…"\n}\n]\n}\n`.
- so `base[:20057]` (all base bytes up to the final `]`) is a byte prefix of the tree; the structural tail shifted right. `carrier_bytes` grew 20061 → 21148 (carrier receipt `controls/after-c1-ledger-guard.txt`) → 22324 (settlement appends) with the guard green at every step.

## 4. Findings routed

1. **C1 counter worktree mode is broken (operability, round-81 fix).** `c80_defect_queue.py:306-311`: the worktree branch never binds `errors`, so line 308 `if errors:` raises `UnboundLocalError` — receipt `counter-worktree-crash.txt`. Introduced by amendment 2 (`de65ec21`); the frozen junk control (`ctl-c80-junk-queue.txt`) predates it and ran worktree mode fine, so a reviewer re-running that control verbatim now gets a traceback instead of `open=6`. Revision mode — the mode both committed controls use at/after base — is unaffected. One-line fix: `errors: list[str] = []` in the worktree branch.
2. **Interim export-mode flag — withdrawn.** I flagged mid-wave that `p_r79_2`'s `--json` conjunct looked unevaluable in revision-export mode (no `.git`, ledger absent from `EXPORT_PATHS`). Amendment 3 (`e8d3a924`) resolved it before my runs: the ledger is now exported (`c80_defect_queue.py:39`), main writes a `base-ledger.json` snapshot from `git show <base>:…` and passes `--base-file` to the guard (`:145-147, 296-303`), and the base receipt was re-run. Verified by runs 4–6.
3. **Counter amended post-freeze — premise re-verified.** Counter history: `f20163c1` freeze → `de65ec21` amendment 2 → `e8d3a924` amendment 3 (base receipt re-run) → `1e7abe7f` code-2 paths → `2950aa18`/`63afc0ee` settlements. Run 6 confirms the amended counter still reports `open=6 met=false` at base, so C1's kill-rule premise (a counter that meets at base fails its own premise) holds.
4. **Guard glob governs exactly one ledger.** `.ufo/waves/*/receipt-rewrites*.json` matches only `.ufo/waves/round-58/receipt-rewrites.json` today (glob-verified); `files=1` in all runs. If a future round adds another `receipt-rewrites*.json`, the guard begins governing it automatically against the same base — intended, but worth knowing if a future base re-pin is ever needed.

## 5. Design reference (superseded, retained)

`w1/ExecGuard/design-reference-execguard.py` is my independently validated implementation (strict whole-file prefix + divergence reporting + git fixture battery). My own selftest proved strict whole-file prefix unsatisfiable: the splice fixture came out red because any array append shifts the structural tail — the strict-prefix lane run showing `first_divergence offset 20057 (base 0x5d, tree 0x2c)` is retained at `w1/ExecGuard/design-reference-strict-prefix-run.txt`. The shipped prefix-to-`]` rule is the right cut. Transcript of run 6 (base premise) was captured at scratch before teardown: `R79-2 open scripts/ledger_append_guard.py absent` … `C1v1 revision=9998dc7a… items=6 open=6 closed=0 exported=77 met=false`, exit 1.

## 6. SKILL.md registry row for the L1

Per the round-79 convention (append at EOF; supersede by successor name, never edit a cell):

| Name | Kind | Entry command | Verdict map | Self-test | Pinned proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| scripts/ledger_append_guard.py | gate, standing receipt-ledger append discipline (calibration) | `python3 -B scripts/ledger_append_guard.py --root . --json` (`--base <rev>` overrides the default base `9998dc7a586b9fe76379014c8123aa3606f2d8b9`) | 0 prefix preserved for every governed ledger; 1 prior bytes lost or truncated; 2 unevaluable; 64 usage | `python3 -B scripts/ledger_append_guard.py --selftest` → `fixture append: passed`, `fixture non-prefix: failed (first divergence at byte 126)`, `selftest: 2/2 passed` | round-80 contract C1 row R79-2; receipt `.ufo/waves/round-80/controls/after-c1-ledger-guard.txt`; rule = base bytes up to the ledger's final `]` must be a byte prefix of the tree bytes; governs `.ufo/waves/*/receipt-rewrites*.json` | reads only | kake |

## 7. Risks and blockers

- R79-2 itself: none. The item closes at the carrier in the only working counter mode; the guard is able to fail (selftest fixture + the strict-prefix evidence in §5).
- Round-81 candidates: the worktree-mode `UnboundLocalError` (finding 1); the tail-after-final-`]` coverage limit (§1).
- HEAD moved twice during verification (`1e7abe7f` → `63afc0ee`, both settling other seats' reports only); guard and ledger bytes were identical across the moves and the guard re-ran green at the final HEAD.
