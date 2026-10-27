# ExecC2Counter

Counter built: `.ufo/waves/round-60/w1/ExecC2Counter.files/c60_guard_cases.py` (~770 lines,
stdlib-only, `PREDICATE = "met: cases_passed == 24 of 24"`). CLI per contract:
`--root <lane> --revision <rev> [--work <scratch>] [--seed N]` plus `--selftest` and the hidden
`--tool <path>` override. Exits 0/1/2/64 verified below. The tool under test is extracted with
`git show <rev>:scripts/append_guard.py` into the work dir (missing tool → every case fails →
exit 1, the do-nothing control). Every fixture is `git init` in its own seed-named dir under
`--work` (`mkrepo`/`init_repo` assert `rev-parse --show-toplevel` realpath-equals the dir before
the first commit; commits use `-c user.name=selftest -c user.email=selftest@local
-c commit.gpgsign=false`). Knowledge paths and all line bodies are drawn from `--seed`
(`corpus/knowledge/<slug>.md`, `sub/` for K22). Per-case timeout 300 s (`run()` returns
`"TIMEOUT"` → judge fails the case). `GIT_*` scrubbed in every subprocess env; R1/R2 run on
`git clone --shared` of `--root`; the `--work` mkdtemp dir is `shutil.rmtree`d in `finally`
(verified empty after the base run). Pass rule: expected exit AND expected finding kind+path on
stdout (`^(deleted|changed|untagged_insertion) <path>[:<line>]$`, optional `:line`); expected-clean
and K20/K21 exit-only cases also require zero finding lines (and `findings=0` if the
`files=<n> findings=<k>` summary is printed).

## CASES:
(id — fixture base→tip, expected)
- K1 — 3 seeded lines appended at EOF → 0
- K2 — 3-line run mid-file (after line 6), first line `**[r60-correction 2026-10-27]** …` → 0
- K3 — untagged 2-line run mid-file → 1 + `untagged_insertion <kf>`
- K4 — first byte of line 5 replaced `x→Z` → 1 + `changed <kf>`
- K5 — line 6 deleted → 1 + `changed <kf>`
- K6 — file deleted → 1 + `deleted <kf>`
- K7 — file renamed inside `corpus/knowledge/` (new name = new path, unchecked) → 1 + `deleted <kf>`
- K8 — 2-line run, tag on its second line → 1 + `untagged_insertion <kf>`
- K9 — run's first line `<!-- [r60-correction 2026-10-27] -->` → 1 + `untagged_insertion <kf>`
- K10 — run's first line carries the tag only inside `` `...` `` → 1 + `untagged_insertion <kf>`
- K11 — second knowledge file added, base file untouched → 0
- K12 — lines 5 and 8 swapped → 1 + `changed <kf>`
- K13 — trailing space on line 5 → 1 + `changed <kf>`
- K14 — whole file converted to CRLF → 1 + `changed <kf>`
- K15 — `a,"",b` → `a,TAG,"","",b` (tagged-run alignment exists only if base `""` may match
  the second `""`) → 0
- K16 — `a,b,c` → `a,b,b,c` (untagged duplicate under every alignment) → 1 + `untagged_insertion <kf>`
- K17 — `SKILL.md` rewritten at tip, knowledge file untouched → 0
- K18 — file replaced by symlink `../../peer.md` → 1 + `deleted <kf>`
- K19 — bytes `\n\xff\xfe` appended at EOF (the `\n` keeps base's newline-terminated tail a
  pure EOF-run append) → 0
- K20 — `--base` = tip commit, `--revision` = base commit (base is a descendant, not ancestor) → 2
- K21 — `--base` flag omitted → 64
- K22 — base file under `corpus/knowledge/sub/` rewritten one byte → 1 + `changed <kf>`
- R1 — lane clone `--shared`, `--base fd6303ce5c14b3f892dec586297a942ab6e4193b --revision <rev>`
  (real diff = `M crawler-identity.md` tagged `**[r59-correction 2026-10-27]**` mid-file +
  2 added files, verified 2026-10-27) → 0
- R2 — same clone checked out at `<rev>`, one byte `a→A` of a base line of
  `corpus/knowledge/crawler-identity.md` committed as `selftest`, `--base <rev>
  --revision <new-head>` → 1 + `changed corpus/knowledge/crawler-identity.md`

## SELFTEST:
`--selftest` scores five controls through the same `measure()` (seed fixed 60; expected scores
derived from the case table, never observed). Run at `--revision 97cdc12…` (controls still clone
the lane for R1/R2; `--revision` may be omitted in selftest, resolving `HEAD`):
- `missing_tool` (nonexistent path) → 0/24, exit 1 — ok
- `always_exit_0` (`sys.exit(0)`) → 7/24: K1,K2,K11,K15,K17,K19,R1 pass — ok
- `always_exit_1` (no output) → 0/24 — ok
- `c55_byte_prefix_port` — faithful port of `c55_readme_index.py`'s rule (`deleted` on ls-tree
  name absence; `head_changed` when revision bytes don't start with base bytes; real ancestor
  check, exits 2/64) → 8/24: K1,K6,K7,K11,K17,K19,K20,K21 pass; **fails K2, K15, R1 as required**
  (also K18 — the port reads the symlink's target bytes, faithful to c55's membership-only
  `deleted` test) — ok
- `reference_impl` — in-file reference per contract (existential alignment via 2-row DP over
  (position, in-run); HTML comments tracked across lines, inline backtick spans stripped;
  `**` glob matcher; committed bytes via `cat-file`/`ls-tree`; mode `120000`→`deleted`) → 24/24,
  exit 0 — ok
- Result: `selftest: ok (5 controls scored) exit 0`.

## BASE RUN:
`python3 -B c60_guard_cases.py --root /home/vgpnk/Projects/shokunin/kake-shokunin
--revision 97cdc122379711c2b02a8970752c8782da3ac81d --work <scratch> --seed 60` →
`C2 guard-cases 0/24 met=False`, all 24 cases `FAIL scripts/append_guard.py absent at
97cdc1223797`, `EXIT=1` (expected: tool does not exist at base — `git ls-tree 97cdc12 scripts/`
has no `append_guard.py`). Edge checks: no `--revision` → 64; non-toplevel `--root` → 2;
unresolvable `--revision` → 2. Direct `--tool` run of the selftest reference at base →
`24/24 met=True EXIT=0` (R1 `files=53 findings=0`, R2 `changed corpus/knowledge/crawler-identity.md`).
No tools installed (stdlib + git only; pacman paused per guard).

## CONTRACT AMBIGUITIES:
- **Trailing-newline phantom (load-bearing)**: `split(b"\n")` on `…\n`-terminated bytes yields a
  final `b""`. Read literally, that phantom is B's last line, must match in R, and any EOF append
  becomes an interior run needing a tag — contradicting K1/K19 expected `0`. The reference drops
  one trailing `b""` from each side before analysis; a literal-split tool would fail K1 and K19
  with `untagged_insertion`. The w1 tool seat should implement the drop (or treat `\n` as
  terminator); w2 may probe a base file not ending in `\n` (then the phantom is real content —
  a changed tail byte — and nothing is dropped).
- **Clean-case strictness**: the contract requires only the expected exit; the counter
  additionally rejects any finding-kind line on clean/K20/K21 cases and a printed `findings=>0`
  summary on clean cases. A contract-conformant tool (findings ⇔ exit 1) is unaffected.
- **`untagged_insertion` `:line`**: which line/run is unspecified; the counter accepts any `:N`.
  The reference reports the first bad run under the leftmost alignment; K15's existential
  reading means a leftmost-greedy-only tool emits the same finding the reference avoids.
- **"backtick code span"**: fenced code blocks are not addressed by the contract; reference
  strips inline spans only and tracks `<!-- -->` across lines.
- **Empty base file** (`""` at base, lines added): every revision run is post-last-match
  (there is no match) → clean append under the reference. [INFERENCE] — no case exercises it.
- **R2 `--revision`**: the fixture head is a scratch-clone commit (selftest identity) on top of
  `<rev>`; base `<rev>` is its parent, so ancestry holds.
- **Tool absent → exit 1** (not 2): the contract's do-nothing control states a missing tool
  fails every case; unevaluable-2 is reserved for unresolvable input.
VERDICT: c60_guard_cases.py delivered; selftest 5/5 controls exact (c55 port fails K2,K15,R1; reference 24/24), base run 0/24 exit 1 as required, all kill-rule exits verified.
