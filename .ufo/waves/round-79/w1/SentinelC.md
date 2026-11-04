# SentinelC — round 79 w1 — security review of the C2 tool, both c79 counters, and the C1 fixture

**Verdict: no claim-breaking vulnerability.** The frozen matrix reproduces met=true from my seat (31/31, constants 4/4, selftest ok; tool sha256 `f06c47b5cdd38bccf3dd1c0f381fbd560f6622bdf9d25443a02a2e2c23a24de8`, 18053 bytes — matches the L1 receipt; cases_sha256 `fd0a3bccbe7c1b6d3522259ab5c57d4eb1f272abe6acaba44013aae3af7978af`), the C1 counter reproduces the base red (`events=32 undisclosed=5 met=false`, exit 1 at `0898085`) and selftest 15/15, and the fixture's five variants behave as documented. I found 2 crash defects (medium) in the tool, 1 resource defect (medium-low), 1 frozen-grammar deviation (medium-low), 1 output-injection defect (low-medium), 1 exit-code defect (low), and 1 counter `--json` purity defect (low-medium). Nothing writes outside its declared surface; no oracle leakage path exists. Tool and counters were not edited by me; the crash/id findings below are candidates for a future L1 amendment or a post-freeze fix round.

Review surface: `scripts/x_robots_tag_audit.py`, `.ufo/waves/round-79/c79_xrt_matrix.py`, `.ufo/waves/round-79/c79_receipt_ledger.py`, `.ufo/waves/round-79/ctl_receipt_fixture.py`. No tools were installed or upgraded for this seat (nothing to record under the 2026-10-19 authorization). All probes ran under `/fast/scratch/hyaku/kake-r79/SentinelC/` (deleted before this report was finalized).

## Tool — `scripts/x_robots_tag_audit.py`

### F1 (medium) — uncaught `ValueError` on huge integer directive values → traceback, exit 1, no report
- **Repro** (`$S` = scratch):
  `python3 -c "...'max-snippet:'+'1'*4301..." ; python3 -B scripts/x_robots_tag_audit.py --manifest $S/p6c.json --json`
- **Observed**: `rc=1`, stderr `ValueError: Exceeds the limit (4300 digits) for integer string conversion` at `x_robots_tag_audit.py:202` (`int(value)`); negative 5000-digit variant crashes identically (`p6b`). No JSON object emitted; exit 1 collides with "findings present".
- **Expected**: a decided case (grammar §4: `^-?\d+$` matches, token emitted) or a graceful `xrt_invalid_value` — never an unhandled crash. CPython's `int()` string-conversion limit (4300 digits) is invisible to `INT_RE`.
- **Impact**: any recorded/degenerate header carrying a pathologically long numeric cap kills the audit instead of deciding it. Not pinned by a frozen case (matrix unaffected); violates the tool's "decides every case, closed vocabulary" contract on unpinned input.
- **Smallest fix**: wrap `int(value)` in `try/except ValueError` → `findings.add("xrt_invalid_value"); return []` (or cap digits inside `INT_RE` — grammar change, needs L1).

### F2 (medium) — uncaught `RecursionError` on deeply nested manifest JSON
- **Repro**: manifest `{"schema":"x-robots-tag-manifest/v1","checks":[[[[…]]]]}` at 100 000 nesting depth → `python3 -B scripts/x_robots_tag_audit.py --manifest $S/p7d.json --json`.
- **Observed**: `rc=1`, traceback ending `RecursionError: Stack overflow (used 8140 kB) while decoding a JSON array from a unicode string` (`json/decoder.py raw_decode`, raised through `main:367 → load_manifest`). 20 000 depth parses fine (rc=2 `xrt_input_check_shape`), so the fault window is real but narrow.
- **Expected**: `xrt_input_bad_json`, exit 2.
- **Fix**: add `RecursionError` to the caught tuple at `load_manifest` (`except (UnicodeDecodeError, json.JSONDecodeError, RecursionError)`).

### F3 (medium-low) — unbounded read: `/dev/zero` hangs, FIFO blocks on open
- **Repro**: `timeout 5 python3 -B scripts/x_robots_tag_audit.py --manifest /dev/zero` → `rc=124` (killed mid-`read()`; unbounded memory growth without the timeout). `mkfifo p.fifo` → `--manifest p.fifo` → `rc=124` (blocks in `open()`).
- **Expected**: an input fault (`xrt_input_unreadable`, exit 2), not a hang/OOM on the analyst's machine.
- **Impact**: offline analyst tool, operator-run — aggravation/DoS only, no privilege path. The counter is not exposed (it copies plain case files to scratch first).
- **Fix**: `os.stat` before read; reject non-regular files and sizes above a cap (e.g. 16 MiB) as `xrt_input_unreadable`.

### F4 (medium-low) — frozen-grammar §6 deviation: duplicate `unavailable_after` / `max-image-preview` yield no `xrt_duplicate_directive`
- **Repro**: value `unavailable_after:2025-12-31, unavailable_after:2026-01-01` (and `max-image-preview:large, max-image-preview:standard`) → tool returns `findings=[]`, `exit=0` (probes f1/f2).
- **Expected** (contract §6): "The same value-bearing directive twice in one scope yields `xrt_duplicate_directive`". `scope_findings` (tool lines ~143-149) only counts `max-snippet:`/`max-video-preview:` prefixes.
- **Frozen-case coverage**: none — only c21 pins a duplicate (max-snippet). So the matrix stays green, but the tool under-reports on unpinned input; real publishers do emit repeated date caps.
- **Fix**: extend the duplicate scan to all four value-bearing names (or drop-in: count by token name before the `:` for every token carrying a value).

### F5 (low-medium) — text-mode output injection: forged `XRTv1` summary lines and ANSI via check id
- **Repro**: check id `"c01\nXRTv1 checks=999 findings=0 exit=0\n\x1b[32mFAKE-GREEN"` → `--manifest $S/p8.json` (text mode).
- **Observed**:
  ```
  check c01
  XRTv1 checks=999 findings=0 exit=0
  ^[[32mFAKE-GREEN directives=['noindex'] effective=['noindex'] bots={} findings=[]
  XRTv1 checks=1 findings=0 exit=0
  ```
  The contract fixes id as any non-empty string; `render_text` echoes it raw. The default text mode is the human/grep surface — a manifest can forge a clean-looking final summary line. `--json` escapes correctly (verified); bot names are regex-gated (`^[A-Za-z0-9_-]+$`) and cannot carry control chars.
- **Fix**: escape control characters (e.g. `id.encode('unicode_escape').decode()`) when rendering ids in text mode. Report-only until unfreeze.

### F6 (low) — argparse usage errors exit 2, not 64
- **Repro**: `--bogus` → `rc=2`; `--manifest` without value → `rc=2`. No args → `rc=64` ✓; input faults → `rc=2` with error object ✓; directory → `xrt_input_unreadable` ✓.
- **Expected**: contract §9 reserves 2 for input faults (report JSON) and 64 for usage; argparse's bare 2 (usage text on stderr, no error id) collides with the fault channel.
- **Fix**: `parser.exit(64, ...)` override or wrap `parse_args()` and remap `SystemExit(2)`.

### Tool — explicitly cleared (no-issue)
- **No write surface**: sole `open()` is `open(path, "rb")` (grep: line 156); imports are `argparse, json, re, sys` only — no os/shutil/subprocess/socket/urllib. No mode writes files.
- **No oracle leakage**: zero path composition — the tool opens only `--manifest`. Symlink to `expect/expect.json` → `xrt_input_schema` rc 2 with no oracle bytes in output; `xrt_input_unreadable`/`bad_json` details carry exception text + path only, never file content. `..\expect\expect.json` style traversal has nothing to traverse.
- **Scale**: 10 000 checks → 0.07 s / 35 MB RSS; 500 k-segment 4 MB header value → 0.20 s / 75 MB; 2 MB adversarial date-tail string → 0.02 s, correctly `xrt_invalid_value` exit 1. Date/bot/int regexes are anchored literal alternations — no catastrophic backtracking.
- **`noarchive` in KNOWN** matches `contract-amendment-1.md` (L1 terms-only amendment, 06:51, before the 07:04 tool and any scored case; frozen case set unchanged — c26 oracle expects `noarchive` as known). Not a defect; grounding recorded in the amendment.
- **Informational**: `--selftest --manifest X` silently ignores X (rc 0); `str.lower()` vs "ASCII case-insensitive" has no practical false match for `x-robots-tag`.

## Counter `c79_xrt_matrix.py` (frozen — reported, not fixed)

### F7 (low-medium) — `--json` stdout is not a single JSON document
- **Repro**: `c79_xrt_matrix.py … --json | python3 -c "import json,sys; json.load(sys.stdin)"` → `JSONDecodeError: Expecting value: line 1 column 3 (char 2)`.
- **Observed**: `selftest(work)` prints `  ok good-decided …` lines to stdout before the JSON object (raw head verified). Strict machine consumers of `--json` cannot parse the stream.
- **Fix (when unfrozen)**: send selftest lines to stderr or return them.

### Counter — explicitly cleared (no-issue)
- Subprocess handling: list-argv `["sys.executable","-B",tool,"--manifest",…]`, shell=False, timeout=120, capture_output — on every run path including the selftest's synthetic tools and the four constants.
- Work-dir hygiene: explicit `--work` is caller-owned (persists — correct); default `mkdtemp` is owned and removed in `finally`. Nothing is written outside `--work` (code-inspected: inputs/selftest/const-* only).
- Opaque input: each frozen manifest is `copyfile`d to `$work/inputs` before the tool sees it — the tool never receives case-dir paths.
- Symlinked `--tool`: `Path(a.tool).resolve()` → executed and receipt-hashed bytes are the same resolved file (verified via `tool-link.py`: identical sha256, met=true). Theoretical read-vs-exec TOCTOU is local-only (informational).
- Constants (`consts/const_{all,clean,echo,regex}.py`): pure offline JSON emitters; read only the manifest path; no writes, no network. `--consts-only` smoke: failures 31/29/19/23 → 4/4 red, exit 0 ✓.
- Informational (not reachable in the frozen run): a hostile "tool" emitting `bots` as a non-dict would raise `AttributeError` in `compare` (traceback, rc outside {0,1,2}) instead of counting the case wrong.

## Counter `c79_receipt_ledger.py` (frozen — reported, not fixed)
- **no-issue**: `--json` parses clean (strict `json.load` verified: `schema kake-r79-c1-receipt-ledger-v1 undisclosed 5`); git calls list-form `git -C root …`; `--selftest` 15/15; base at `0898085` reproduces the contract's frozen base exactly (`events=32 undisclosed=5 … round_rewritten=0 met=false`, exit 1).
- Informational: `load_c58()` executes whatever file sits at `.ufo/waves/round-58/c58_receipt_rewrites.py` via importlib — repo-trusted input by construction. c58's only write sites (`open(p,"wb"/"w")`, lines 269-273) are inside its selftest fixture helper `_commit`, not the `measure()`/`events()` path c79 uses; all c58 subprocesses are list-form with `-C` and `clean_env()`.

## Fixture `ctl_receipt_fixture.py`
- **no-issue — git discipline**: every git call goes through the single `git(d,*args)` helper prepending `-C d`; toplevel asserted (`rev-parse --show-toplevel == d`) before the first commit; throwaway identity set only inside the fixture repo.
- **no-issue — write confinement**: all writes under `HYAKU_SCRATCH/kake-r79/ctl-fixture/<mkdtemp>`; honors `TMPDIR`; counter is invoked with `--root <fixture>` (read-only against the lane).
- **Behavioral receipt** (run with `HYAKU_SCRATCH=$S`, rc=0): correct → `met=true` exit 0; fabricated → `phantom=1 undisclosed=1` red; drop-one → `undisclosed=1` red; cheap-note → `malformed=1` red; round-rewrite → `round_rewritten=1` red. Every able-to-fail variant failed; the able-to-pass variant passed.
- Low/informational: `finally` removes only the mkdtemp repo; the empty parent `kake-r79/ctl-fixture/` remains. The fallback base when `HYAKU_SCRATCH` is unset is `tempfile.gettempdir()` (TMPDIR-aware), not the round's declared `/fast/scratch/hyaku` default — tiny repo, within the /tmp <50 MB rule, but a caller without `HYAKU_SCRATCH` lands in /tmp.

## Commands run (verbatim, all rc reported inline above)
Probe families: directory/missing-file/symlink-FIFO-/dev/zero manifests; unknown-flag and missing-arg usage; 4301/5000-digit `max-snippet`; 20k/100k nested JSON; newline+ANSI id in text and `--json` mode; 10k checks and 4 MB value timing; 2 MB date-regex input; §6 duplicate repros (unavailable_after, max-image-preview); frozen matrix via worktree tool and via symlinked tool; matrix `--consts-only`; matrix `--json` strict parse; C1 selftest, C1 base at `0898085`, C1 `--json` strict parse; `ctl_receipt_fixture.py` with scratch cleanup check. Scratch tree `/fast/scratch/hyaku/kake-r79/SentinelC` removed before yield.

**Route**: F1/F2/F3/F4/F5/F6 need an L1 amendment or a post-freeze fix (they cannot flip the frozen verdict — no frozen case reaches them — but they are real defects against the frozen grammar and CLI contract). F7 is a counter defect to fix only when the round unfreezes the counter.
