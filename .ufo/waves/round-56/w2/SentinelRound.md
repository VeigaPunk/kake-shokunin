# SentinelRound

Adversarial security/safety review of round 56 (`e48354b7c26b` → `a450e43e696d`, 262 files, +42551/−15).
All execution was in my own `mktemp -d` clone / `git init` fixtures with `-c user.name=selftest`; the lane was
read-only. Nothing installed or upgraded (pacman paused; no tool needed).

## EXECUTION SURFACE:

**Target claim:** `SKILL.md` §Round 56 gate registry — "The C1 counter runs each row's documented self-test
command from the row's `Self-test` cell … in a `git clone` of the measured revision"; the counter docstring
(`.ufo/waves/round-56/c56_selftally.py:1-42`) claims `command_invalid` unless the command is exactly
`[pin ...] python3 -B <script> <pinned args>` and "no write to the lane, no network".

### S1 (verified, no defect): the cell whitelist holds against crafted cells
27 crafted `Self-test` cells through the shipped `documented_command` (:147) and `command_problem` (:164) in
`/tmp/sent-r56/harness.py`; 6 selected, 14 `command_invalid`, 7 `command_missing`.

| vector (cell text) | outcome |
|---|---|
| `python3 -B scripts/base_path_selftest.py` (canonical) | accepted → argv exactly canonical |
| `… ; touch PWNED`, `… \| tee x`, `… & touch PWNED`, `… $(touch PWNED)`, `… {a,b}` | `command_missing` / `command_invalid`, **never run** |
| `KAKE_R56_SELFTEST_REV=$(touch PWNED) …`, `=3691e968;touch …`, `=../../etc …` | `command_invalid` |
| `PATH=/tmp/evil python3 …` (env-key override attempt) | `command_invalid` |
| `python3 -B ../evil.py --selftest`, `scripts/../../evil/base_path_selftest.py`, `~/x/…`, `/tmp/evil/…` | `command_missing` (script name comes from `POP`, not the cell; membership is exact) |
| `… --selftest` (extra arg), `… #--selftest`, `-B -- script`, backslash-space | `command_invalid` / `command_missing` |
| `… [; touch PWNED]`, `… [--tool X --evil]` | accepted, but bracket content is **discarded** by `_strip_brackets` (:128) before `shlex.split`; argv = canonical only |
| `"scripts/base_path_selftest.py"` (quoted), `KAKE…=aaaaaaa KAKE…=bbbbbbb python3 …` | accepted; argv = canonical, pins stripped |

Recorded `run_command` argv (instrumented `measure()` over 5 hostile sandbox cells): **empty for every rejected
cell**; for the bracket-smuggled cell exactly `['python3','-B','t/alpha_selftest.py']` and the `touch` target never
appeared. `subprocess.run(argv)` (:211) has no `shell=`; `shlex.split` is used only to *compare* against a fixed
list, and `_strip_brackets` removes bracket text before splitting — so `shlex` quoting can only normalise a cell
onto the canonical command, never past it. Double pin: last value wins in `env` (`bbbbbbb`), both stripped from
argv; a pin after `python3` is rejected. No cell-controlled path reaches `env`, `argv[0]` or the script path.
*Note (fail-closed, not a hole):* because brackets are stripped, a **bracketed** required arg (e.g. sitemap's
`--tool`) yields `command_invalid` and the row is left unchecked rather than run.

### S2 (MEDIUM) `tool_changed` is recorded but does not stop execution — `c56_selftally.py:265-272`
`changed = helpers_changed(...)` appends the problem, then `code, out = run_command(...)` runs anyway. Demonstrated
in a sandbox: base `t/a_selftest.py` prints `1/1`, tip rewrites it to print `2/2` and write
`$HOME/.sent-r56-home-write`; result `problems=['tool_changed']`, `observed='2/2'`, and the file **was created in
the real `/home/vgpnk`** (removed by me afterwards). `env` (:202) inherits the caller's `HOME` and `PATH`; no
network namespace, no filesystem confinement beyond `cwd=clone`.
Impact: running this gate against any revision outside the trust domain (a PR branch, a staged mirror) executes
that revision's Python with the caller's home directory and network. "No write to the lane" holds; "no network"
and "$HOME isolated" do not.
Smallest remediation: point `HOME` at the clone (or a fresh `mkdtemp`) and wrap the run in `bwrap --unshare-net
--ro-bind / / --tmpfs /home` (or `unshare -n`); skip `run_command` when `changed` is non-empty — the tally is
meaningless once the tool bytes moved.

### S3 (MEDIUM) the byte-identity guard cannot see added code or non-`.py` data beside the pinned script — `c56_selftally.py:216-224`
`ls-tree --name-only <base> <dir>/` is non-recursive and `names` keeps only `*.py` **that exist at base**; the guard
therefore cannot flag a file that the measured revision *adds*. Two demonstrations (`/tmp/sent-r56/harness2.py`,
`harness3.py`, `git init` fixtures):
- **shadow module:** base `t/alpha_selftest.py` = `import tally; tally.report()`; tip adds `t/tally.py` (prints
  `9/9`). `helpers_changed(...) == []`, `measure()` exit 0, `observed='9/9'`, no problem — the counter reports the
  tally of code the revision supplied while calling it the pinned script's.
- **fixture data:** deleting one committed case file (`t/fixtures/b.txt`, not `.py`) → `helpers_changed == []`,
  `observed='1/1'` vs claim 2. Real instance: `scripts/base_path_selftest.py:51` defaults to the committed
  `scripts/fixtures/base-path/` (463 files at the measured rev); `MIN_DEFAULT_CASES` (:269) bounds **deletion**
  only, so a revision can add trivially passing cases and set the `Self-test` claim to the new total →
  `tally_mismatches == 0`, `rows_checked == 10`, predicate met without the tool changing.
  Related: `run_tool` (`scripts/base_path_selftest.py:163-171`) builds argv from the case's committed
  `expected.json`; the executable stays `python3 -B <pinned tool>`, so fixture data can choose the *arguments*
  but cannot become interpreter flags or a different binary.
Smallest remediation: compare the pinned script's whole directory subtree (recursive, every file type) against
base, and treat any added path beside the script as `tool_changed`; or pin an explicit blob allowlist for
`scripts/fixtures/**` used by a pinned selftest.

### S4 (LOW) `span_tools.py:51-52` — `main()` indexes `sys.argv[1]`/`[2]` with no length guard: a missing argument
raises `IndexError` (traceback, exit 1) instead of the tool's documented exit 64. Read-only otherwise (no `open(...,'w')`,
no subprocess).

## SECRET SWEEP:

```
git -C <lane> diff e48354b7c26b a450e43e696d | grep -n -i -E 'op://|token|secret|password|api[_-]?key|BEGIN [A-Z ]*PRIVATE'
→ 395 matching lines (prose: "product token", "secret files", "password" in WCAG/HTML knowledge text)
git … | grep -c -F 'op://'                    → 7
git … | grep -o -E 'op://[^ `)|]{0,40}'       → 5×`op://`, 1×`op://'`, 1×`op://\`  (bare pattern text, no Vault/Item/field)
git … | grep -E '^\+' | grep -i -E 'BEGIN [A-Z ]*PRIVATE|ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|Bearer [A-Za-z0-9._-]{10,}|api[_-]?key\s*[:=]\s*.{8,}' → 0
```
All 7 `op://` hits are credential-sweep pattern prose (`corpus/lessons/round-5/6-aggregator-audit.md` texts and the
embedded seat prompt in `make_spec_w1.py`), none resolvable. No key, token, password or `Bearer` value added.
`shell=True|os.system(|os.popen(|eval(|exec(` over added lines: 1 hit — a pre-existing documented procedure
(see O3), no shell in any script.

Retained bodies: `grep -i -E 'cookie|authorization|user:pass|://[^/ ]+:[^/ ]+@|csrf'` over
`.ufo/waves/round-56/sources/*.html` + `receipts.json` → S367/S419/S420 (the three adopted bodies) **0 hits**;
S388.html:111 has `http://www.example.com/products?sessionid=hgjkeor2`, an example URL printed by the page itself,
not a session value. `receipts.json` carries only `url`, `httpStatus`, `bytes`, `sha256`, `fetchedAt`,
`userAgent` (`kake-shokunin-round56`) — no headers, cookies or credentials.

## OTHER FINDINGS:

- **O1 `scripts/landed_check.py` — no shell, no report-derived argv.** `grep -c 'shell=True'` → 0; the only
  `subprocess.run` sites are list-argv `git` calls (`:63-71`, `:266`) and the selftest's own re-invocation
  (`:411`). Report text reaches git only through `HEX_RUN` (`:55`: 7–40 hex chars, 64-hex digests excluded), so a
  token can be neither an option nor a shell metacharacter, and `check_report` (`:214`) opens the report read-only
  (`:217`). Writes exist only in selftest fixtures under `mkdtemp` (`:238-266`); the measurement path writes
  nothing. Report-derived input is used as `git rev-parse --verify --quiet <token>^{commit}` and `cat-file -t`.
- **O2 files written outside the lane by committed scripts.** Gates: none — `c56_selftally.py` (`clone_at`/`rmtree`),
  `c56_quote_truth.py:587`, `landed_check.py` write only in `mkdtemp` trees. Authoring scripts (not gates):
  `derive_c56_selftest.py:58` and `derive_c56_quote_truth.py:97` write `c56_quote_truth.py` **in the caller's CWD**
  (would land outside the lane if run elsewhere); `make_spec_w1.py:293` writes `w1-spec.json` beside itself (inside
  the lane); `.ufo/waves/round-56/validate_append.sh` does `rm -rf "$V"` + `cp -r` only under the hardcoded
  `$LANE/.ufo/waves/round-56/assimilation/validate` after `cd "$LANE" || exit 64` (destructive to its own committed
  mirror by design) and executes `$ARGV` unquoted — a constant string, so no injection source, but latent if the lane
  path ever gains a space or glob character.
- **O3 (pre-existing, unchanged) remote-text `eval` in documentation.** The added line
  `const d=eval(s.match(/const PROPERTIES = (\[[\s\S]*?\]);/)[1])` appears only in the round-56 assimilation mirror
  `.ufo/waves/round-56/assimilation/validate/corpus/knowledge/vault-properties.md`; the same procedure is at base
  (`corpus/knowledge/vault-properties.md`). It instructs evaluating a fetched third-party body's JavaScript in
  `node -e` — an execution surface on remote text, not introduced or changed this round.
- **O4 verified run:** `python3 -B .ufo/waves/round-56/c56_selftally.py --selftest` at `a450e43e696d` in my own
  clone → `c56 selftally selftest: 47/47`, exit 0 (matches the SKILL.md claim "47 checks"). This exercises
  `documented_command`/`command_problem`/bracket-stripping unit checks, so S1's acceptance behaviour is the
  shipped one, not my harness copy's.
- **O5 not run:** the C1/C2 counters themselves (`--root … --revision …`) were not executed by this seat; only the
  C1 `--selftest`. `landed_check.py --selftest` was not run here (another seat covers its behaviour); my review of
  it is by reading, stated as such.

VERDICT: no cell-driven shell escape — every crafted `Self-test` cell either fails to select or runs exactly `python3 -B <pinned script>` — but the counter executes revision-controlled code with the caller's `$HOME` and network (S2) and its `tool_changed` guard is blind to added modules and to the committed `scripts/fixtures/**` data the base-path selftest reads (S3), so a self-serving revision can reach a passing tally without touching the pinned bytes; no credential, session or vault material in the diff or the retained bodies.
