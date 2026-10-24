# w1a3 / ReviewJsonDepth — C1 hunk review: load_json_document RecursionError catch

Seat: KakeR28a3.ReviewJsonDepth. Scope: one hunk of
`git diff 22c1669c1fec83d1a0769de6b9ce686c75657e66 b5d423fc02057f67a6f3a255808313ce40d29069 -- scripts/citing_set.py`
(`except ValueError` -> `except (ValueError, RecursionError)`, detail `(str(exc) or type(exc).__name__)[:120]`),
repaired file lines 399-402, callers at 458-461 (evaluate), contract main() 701-715,
`InputInvalid.as_finding` 142-152, `EXIT_CANNOT_EVALUATE = 2` at line 102.
All findings below are advisory input to the L1; no lane file other than this report was touched.

Environment: host python3 3.14.8, `sys.getrecursionlimit()` 1000, `ulimit -s` 8192 (exit 0).
Sandbox: /fast/scratch/hyaku/kake-r28a3/w1/ReviewJsonDepth (TMPDIR set there); gate extracted with
`git -C /home/vgpnk/Projects/shokunin/kake-shokunin show b5d423f...:scripts/citing_set.py`
(exit 0, 27458 bytes, sha256 28ba996524b444b2...). Lane working copy verified at b5d423f
(`git rev-parse HEAD`, exit 0). No installs were needed; none performed. No `lsp` device exists
in this seat, so caller/definition checks used read/grep, not an LSP server.

## Findings

### F1 — MEDIUM — MemoryError still escapes load_json_document as a traceback (exit 1, no JSON report)
- Case: `cases/mem/population.json` = 300 MB flat JSON array (`[1,1,...]`), otherwise valid tree;
  run under `resource.setrlimit(RLIMIT_AS, 512 MiB)`.
- Observed: rc=1, stdout empty (no report), stderr traceback tail `MemoryError`. The exception is
  raised inside `json.loads`/decode inside the try at 399-402, which catches only
  `(ValueError, RecursionError)`; main() catches only `InputInvalid` (line 702), so it escapes.
- Contract impact: C1 says an unusable input document must yield the contracted JSON report and
  exit 2. An oversized-but-real document reaches the same escape the hunk fixes for depth, one
  exception class away. Adversarially triggerable by committing a multi-GB JSON document; needs
  resource-exhaustion conditions, hence MEDIUM not HIGH.
- Suggested fix (advisory): add `MemoryError` to the caught tuple with
  `detail=type(exc).__name__` (str(MemoryError) is often empty, which the new `or` fallback
  already handles).

### F2 — LOW — on CPython 3.14 the depth boundary is stack-dependent and the finding detail is not byte-stable
- Python 3.14 bounds C recursion by a stack watermark, not by `sys.setrecursionlimit`:
  - depth 2000/5000/10000/20000/50000 population: parse succeeds -> `document_shape_invalid`,
    rc=2 (rejection reason differs, exit code still contracted).
  - depth 200000 @ 8 MB stack: caught -> rc=2, `document_not_json`, detail
    `Stack overflow (used 8152 kB) while decoding a JSON array from a unicode string`.
  - same input @ 1 MB stack: `... (used 984 kB) ...`; @ 1 GB stack: parse succeeds ->
    `document_shape_invalid`, rc=2.
  - legal-shape doc (valid rows + 200k-deep junk key) **flips verdicts with stack size**:
    `could-not-evaluate` exit 2 @ 8 MB stack vs `clean` exit 0 @ 1 GB stack. Same input,
    opposite observable verdicts across environments; no segfault ever observed (min rc seen 0,
    even @ 1 MB stack) because 3.14 converts the overflow to RecursionError.
- Detail instability: three runs of the identical depth-200000 case produced byte-different
  stdout (`identical: False`, len 337): the detail embeds measured stack kB (8152 vs 8156).
  Mitigations already true: `judge()` in .ufo/waves/round-28/c1_interface_count.py checks only
  the finding `reason` id (not detail), and counter cases U3/U4 use `deep_json(200000)` whose
  post-parse shape is invalid too, so they pass under any stack size. Malformed-JSON detail is
  byte-identical base vs repair (see F3). Severity LOW: informational instability, contract
  (report + exit 2) still met at every tested stack size.

### F3 — no defect found — no over-rejection, parity kept, raised recursion limit still safe
- Control: depth-500 legal document (`rows` valid + deep `meta`) -> verdict `clean`, rc=0:
  legitimate input is not rejected at sane depths (rejection starts between 50000 and 200000
  on this host's 8 MB stack).
- Detail parity: `{"rows": {"id": "S001"},,,}` gives byte-identical findings detail at base and
  repair: `"Expecting property name enclosed in double quotes: line 1 column 25 (char 24)"`,
  both rc=2 — the hunk widens the catch without changing existing details.
- Embedded use with `sys.setrecursionlimit(150000)` (driver running gate.main in-process):
  depth 200000 still caught -> rc=2, JSON report `could-not-evaluate` with `document_not_json`.
  On 3.14 raising the Python limit does not remove the C-stack guard, so the catch holds even
  in a raised-limit host process.

## Commands and exit codes (representative)
- `git -C <lane> rev-parse HEAD` -> 0, `b5d423fc02057f67a6f3a255808313ce40d29069`.
- `git -C <lane> diff 22c1669... b5d423f... -- scripts/citing_set.py` -> 0 (73 changed lines).
- `python3 -B <sandbox>/citing_set.py --root cases/<t> --population population.json --ledger ledger.json --json`
  -> 0 for `d500legit`; -> 2 with contracted report for d200000, d1000000, d200000@1MB,
  d200000 (limit raised), malformed, thr980-thr1010 (reason `document_shape_invalid`);
  -> 1 with traceback for mem under RLIMIT_AS 512 MiB (F1).
- Per-run subprocess timeout 40-60 s; no timeout fired; all rc observed first-hand.

## Residual risk / not verified
- Other CPython versions: on <=3.12 the trigger is `sys.setrecursionlimit` (1000), so the
  boundary sits near depth ~990 and F2's watermark behavior does not apply; not run here
  (single host interpreter 3.14.8).
- Full `c1_interface_count.py` not rerun (L1 evidence at 15/15 stands; this seat ran targeted
  falsifiers only). No CrUX/API/network probes (out of seat scope).
- Other exception classes from `json.loads`: none observed beyond ValueError/RecursionError/
  MemoryError across malformed, deep, and oversize probes; not exhaustive.
- F1's escape also covers `raw.decode("utf-8")` (line 396) for huge inputs; same remedy.
