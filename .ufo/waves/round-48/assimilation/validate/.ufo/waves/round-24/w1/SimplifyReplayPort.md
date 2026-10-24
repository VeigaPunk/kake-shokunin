## Verdict

**One maintained module** `scripts/receipt_replay.py` should subsume the validation cores of `measure_c1.py` and `measure_c2.py` behind `c1` / `c2` subcommands, sharing git I/O and revision bootstrap only. Round-23 runners stay byte-frozen; the port is **semantically identical on all committed round-23 receipts at base `f7de3ab4e9f030a15a857a5a08631bd8e690f436`** (17/17 C1, 12/12 C2 per `gen_w1.py` ExecReceiptReplay) while **deliberately diverging** on malformed timestamps, non-string `contentType`, bool `status`, and unsafe revision strings. **`counter_selftest.py` fixture machinery is dead weight inside the replay module** — re-home as `receipt_replay.py --selftest` (invoke self via subprocess like today’s selftest does for the two measure scripts). Do not extract a shared Python package imported elsewhere; stdlib-only single file matches lane convention.

## Findings

### P0 — `served()` crashes on non-string `contentType` (operability / C2 contract)

**Command:** (static) `measure_c2.py` line 37–38: `ctype = fetch.get("contentType") or ""` then `ctype.split(";")` with no `isinstance(ctype, str)`.

**Observed:** JSON `contentType: 200` → `AttributeError` on `.split`, stderr traceback; exit not in `{1,2}` with a named problem.

**Impacted:** C2 operability — malformed-receipt matrix requires reject-without-traceback.

**Smallest fix in port:** `parse_media_type(value: Any) -> tuple[str, str] | None`; `fetch_is_served` returns false when unparsable; append a **named problem** on the surface row (e.g. `contentType not a valid media type`) so exit is 1, never crash.

### P0 — Lexical `observedAt` / `fetchedAt` accepts garbage and far-future strings (operability / C1+C2)

**Command:** (static) `measure_c1.py` line 55–56; `measure_c2.py` line 56–57: `isinstance(..., str) and field[:10] < "2026-10-21"`.

**Observed:** Prefix `"2026-10-21garbage"`, `"2099-01-01T00:00:00Z"`, `"2026-10-21T25:00:00Z"`, date-time without offset pass the gate if the first ten characters sort ≥ `"2026-10-21"`.

**Impacted:** C2 claim in `contract.json` — receipt replay must reject malformed timestamps.

**Smallest fix in port:** Replace with `validate_timestamp_field(name, value, *, floor_date, ceiling_dt) -> list[str]` (strict RFC 3339 §5.6 full-date or date-time, calendar/clock sanity, no trailing garbage; date-time requires offset; on/after 2026-10-21; not after revision committer time). Map failures to existing problem strings where possible (`observedAt missing or before 2026-10-21` → split into more precise messages or keep one bucket — **executor should pick stable problem substrings the matrix expects**).

### P1 — Revision passed to `git show` without `--end-of-options` (operability / security)

**Command:** (static) both measure scripts: `git -C root show f"{revision}:{path}"`.

**Impacted:** Sentinel seats — option-shaped `revision` could confuse git; port must use `git rev-parse --verify --end-of-options REV^{commit}` and reject `revision.startswith("-")`.

**Smallest fix:** Shared `resolve_revision(root, revision) -> tuple[str | None, int]` returning exit 2 on failure.

### P2 — Duplicate bootstrap in two `main()` functions (maintainability, not user-visible)

**Observed:** Identical `rev-parse`, frozen population SHA-256 gate, JSON load pattern in `measure_c1.py` and `measure_c2.py`.

**Smallest fix:** `load_frozen_population(root, revision, relpath, digest) -> tuple[dict | None, int]`; C1-only `BASE` and heading constants stay beside `check_c1_unit`.

### P3 — Optional stdout trims from round-23 YAGNI (do not block r24)

Per `round-23/w1/SimplifyR23Tools.md`: `claimVerdicts` / per-unit `claims` tallies and `validatorSha256` are not part of exit semantics. **Receipt replay may omit them** unless L1 wants matrix compatibility with selftest parsers; `counter_selftest.run_case` does not assert on those fields.

## Port outline (for L1 vs executor draft)

Module docstring: CLI usage, exit contract (`0` all pass, `1` validation failure, `2` unreadable revision/population/validator), note that round-23 paths/digests are frozen.

### Frozen constants (byte-for-byte with round-23 measure scripts)

| Symbol | Source | Value / role |
|--------|--------|----------------|
| `ROUND23` | both | `".ufo/waves/round-23"` |
| `C1_BASE` | measure_c1 | `"b5d599e19bead54b96f589444e9ec64cdf67c28a"` |
| `C1_HEADING` | measure_c1 | `"## Live re-verification — round 23"` |
| `C1_POPULATION_SHA256` | measure_c1 | `ffc9b3a4…7697daf` |
| `C2_POPULATION_SHA256` | measure_c2 | `ac58c80f…7c75d98` |
| `C1_VERDICTS` | measure_c1 | `{"HOLD","STALE","UNVERIFIABLE"}` |
| `C1_CLAIM_FIELDS` | measure_c1 | 7-tuple `id`…`verdict` |

### Helpers to merge (single implementation each)

```python
def git_show_bytes(root: str, revision: str, path: str) -> bytes | None:
    """git show revision:path; None if missing. Use --end-of-options on revision in rev-parse only; path is separate arg (no injection via revision)."""

def git_show_text(root: str, revision: str, path: str) -> str | None:
    """UTF-8 decode of git_show_bytes; used for JSON receipts and unit markdown."""

def resolve_revision(root: str, revision: str) -> tuple[str | None, int]:
    """Reject revision.startswith('-'). git rev-parse --verify --end-of-options REV^{commit}. (sha, 0) or (None, 2)."""

def load_frozen_json(root: str, revision: str, relpath: str, expected_sha256: str) -> tuple[Any | None, int]:
    """git_show_text + sha256 gate + json.loads; (None, 2) on missing/bad digest/invalid JSON."""

def validate_timestamp_field(
    field_name: str,
    value: Any,
    *,
    floor_utc: datetime,
    ceiling_utc: datetime,
) -> list[str]:
    """RFC 3339 §5.6; return problem strings (empty if ok). Used for observedAt and fetchedAt."""

def is_status_int(value: Any) -> bool:
    """type(value) is int — excludes bool."""

def parse_media_type(value: Any) -> tuple[str, str] | None:
    """RFC 9110 §8.3.1 token/token + params; lowercased type/subtype or None."""

def fetch_is_served(fetch: dict[str, Any]) -> bool:
    """Semantic port of measure_c2.served() with parse_media_type + is_status_int guards."""

def validate_fetch_redirect_chain(fetch: dict[str, Any]) -> list[str]:
    """Extract measure_c2 check() lines 60–70 unchanged logic."""

def rerun_canonical_audit(
    validator: bytes,
    page: bytes,
    final_url: str,
    expected_canonical: str,
    *,
    timeout: int = 60,
) -> tuple[dict[str, Any] | None, list[str]]:
    """Tempdir layout + subprocess from measure_c2 check() lines 83–102; returns (actual, problems)."""

def check_c1_unit(root: str, revision: str, unit: dict[str, str]) -> list[str]:
    """Port measure_c1.check_unit problems list only (drop verdict tally if YAGNI). Body unchanged except observedAt uses validate_timestamp_field."""

def check_c2_surface(
    root: str,
    revision: str,
    validator: bytes,
    surface: dict[str, str],
) -> tuple[list[str], str | None]:
    """Port measure_c2.check verbatim structure; fetchedAt hardened; fetch_is_served; not-served expected receipt equality unchanged."""

def run_c1(root: str, revision: str) -> tuple[dict[str, Any], int]:
    """Population load, loop units, build JSON {revision, accepted, total, units:[{unit, pass, problems}]}; optional claimVerdicts if L1 wants."""

def run_c2(root: str, revision: str) -> tuple[dict[str, Any], int]:
    """Load validator bytes at revision; surfaces loop; JSON {revision, accepted, total, surfaces:[{id, pass, verdict, problems}]}."""

def run_selftest() -> int:
    """Port counter_selftest.py cases: disposable clone, seed fixtures, mutate cases; subprocess targets receipt_replay.py c1|c2 instead of measure_*.py; print {"selftest":"passed","cases":[...]}."""

def main(argv: list[str] | None = None) -> int:
    """argparse: subparsers c1|c2 (--root, --revision, [--json]); global --selftest. main(argv=) preserved for tests."""
```

### Must stay byte-for-byte semantic (valid round-23 receipts)

- C1: receipt path `{ROUND23}/receipts/{unit}.json`; population digest gate; `unit`/`path` equality; claims list non-empty; anchor substring of **base** text at `C1_BASE`; heading `C1_HEADING` and section checks for STALE corrections and `[unit:id]` citations; duplicate-id and verdict/correction/reason rules; **at least one HOLD or STALE** rule.
- C2: paths under `{ROUND23}/live/{id}/`; fetch url/method GET; redirect chain rules (max 5 hops, status set, `finalUrl` tail); served path: page digest/bytes vs fetch, validator re-run manifest `{version:1, pages:[{url: finalUrl, file: page.html, expectedCanonical}]}`; **strict equality** `audit.json == {"exit", "result"}` from rerun; not-served path: **no page.html**; audit exactly `{"verdict":"not-served","status":<fetch.status>,"exit":None,"error":None}`.
- Exit codes and JSON `sort_keys=True`, `indent=1` on success/failure summaries (match measure scripts for diff-friendly replay at base).
- Validator invocation: `[sys.executable, "-B", canonical_audit.py, "--manifest", ..., "--json"]`, 60s timeout, same temp prefix pattern acceptable (`kake-r24-c2-` ok if behavior identical).

### Intentional semantic changes (hardening only)

- Timestamps: strict validation + ceiling at committer time (requires `git log -1 --format=%cI` or `%ct` on resolved revision).
- `contentType` / `status` / JSON shapes: type-check before use; never raise on malformed receipt.
- Revision resolution: `--end-of-options`, leading `-` rejected.

### Dead weight — do not port into `receipt_replay.py`

| Artifact | Reason |
|----------|--------|
| Second copies of `measure_c1.py` / `measure_c2.py` | Frozen under `.ufo/waves/round-23/` as historical evidence |
| `counter_selftest.py` as a separate entrypoint | Fold into `--selftest` only; keep file at r23 path untouched |
| `git_show` text vs bytes duplication | One bytes primitive + thin decode |
| Verdict histogram aggregation in C1 | Optional stdout; not required for C2 operability claim |
| `validatorSha256` in C2 stdout | YAGNI per r23 simplify |
| Shared importable `kake_receipt` package | Violates stdlib-only single-script lane pattern |
| Network, freshness sweep, round-24 C1 paths | Different counters (`measure_c1.py` r24, `measure_c2.py` r24 matrix) |

### `--selftest` scope

Minimum: port the **seven primary cases** from `counter_selftest.py` (valid C1/C2, bad anchor, missing heading, bad audit, all-UNVERIFIABLE, non-GET) plus **regression loops** (lines 393–440) so mutant coverage is not lost. Selftest continues to clone lane at `Path(__file__).resolve().parents[1]` (lane root = parent of `scripts/`), not `parents[3]` (which was wrong for a `scripts/` placement — executor should use **lane root = two parents up from `scripts/receipt_replay.py`**).

## Checked and held

**Read-only review** of:

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py` (127 lines)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py` (134 lines)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/counter_selftest.py` (452 lines)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/contract.json` (C2 claim)
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/gen_w1.py` ExecReceiptReplay / ExecMalformedMatrix text

**Held:** Round-23 measure scripts must not be edited. No sandbox runs in this seat (outline-only assignment). No `scripts/receipt_replay.py` exists at lane HEAD yet.

## Limits

- Outline only; no executor diff or sha256.
- Malformed-case `expect` labels and exact problem substring matrix come from gap-audit seats and frozen `c2-population.json` (not yet in lane at read time).
- LSP reference proof not attempted (script not on disk); caller/import absence inferred from assignment scope.
- **Tool installs:** none this session.

Report: `.ufo/waves/round-24/w1/SimplifyReplayPort.md`
