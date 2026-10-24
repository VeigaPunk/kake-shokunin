# C2 conventions — what `scripts/base_path_audit.py` must mirror

Read-only scout. Lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`; all paths below are relative to it.
Sources read: `scripts/canonical_audit.py`, `scripts/accessibility_packet.py`, `scripts/citing_set.py` (comparison only),
`corpus/lessons/round-28.md`, `.ufo/waves/round-29/c2-matrix.json` and `c2_matrix_count.py` (contract consumers).
Confidence: high — every claim is a direct source read; nothing was executed.

## 1. Exit-code contract
- `0` clean, `1` policy failure, `2` could-not-evaluate/input, `64` usage: `canonical_audit.py:28-31`.
  Same four values in `accessibility_packet.py:133` (0/1), `:142,:146` (2), `:214` (64) and `citing_set.py:105-108`.
- Matrix interface (`c2-matrix.json` field `interface`) narrows these: 0 = `clean`; 1 = `failed-policy` with only
  `outside_base_path`; 2 = `could-not-evaluate` with only `input_invalid` or `page_outside_base_path`; 64 needs no JSON.
- Precedence to copy: any input-class finding forces `could-not-evaluate`/exit 2 even when policy findings also exist —
  `canonical_audit.py:746-755` (`INPUT_FINDINGS` at `:33`). Do not emit `html_unsupported`: the matrix allows only the two
  exit-2 reasons above, so oversize, non-regular, missing, non-UTF-8 page files must all map to `input_invalid`.
- `--selftest` uses 0 pass / 1 fail / 2 setup error only: `canonical_audit.py:1016-1021`.

## 2. Report JSON shapes
- Audit stdout is exactly one JSON object: `{verdict, pagesChecked, findings}` via `public_result`
  (`canonical_audit.py:766-771`, printed at `:1035`), `sort_keys`, compact separators.
- Usage (64) writes message plus usage to stderr and a `{verdict:"could-not-evaluate",pagesChecked:0,findings:[]}` object to
  stdout (`canonical_audit.py:34,1029-1031`); matrix skips stdout at 64 (`c2_matrix_count.py:81-82`), so either passes.
- New tool's object must add `referencesChecked` and object findings
  `{id,reason,page,element,attribute,value,resolved}` (matrix `interface`). Field-name trap: canonical uses `id`
  (`:732,753,759`), matrix selects on `reason`. Counter projects only the keys present in an expected row and stringifies via
  `str(f.get(k))` (`c2_matrix_count.py:62-72`), so a missing key becomes `"None"` and fails, while extra keys are ignored.
  Emit `reason,element,attribute,value` on every violation; D1-D14 expected rows use exactly those four.
- Finding order is free: counter sorts both sides (`c2_matrix_count.py:62-72`); still emit manifest/page order for humans.
- Selftest JSON: `{tool, selftest:{passed, cases:[{name, expected, actual, ok}]}}` (`canonical_audit.py:946-955,1020`), setup
  failure adds `error` (`:1016`). Accessibility's `result()` findings are bare strings (`accessibility_packet.py:68-72`); do not copy.
- Do not invent keys for a `usage` verdict that the counter does not read; matrix U1 compares exit only.

## 3. Input-safety checklist
- Manifest file: open relative to a directory fd with `O_NOFOLLOW | O_NONBLOCK | O_CLOEXEC` (`canonical_audit.py:561`), then
  `fstat` + `S_ISREG` (`:567`); if `O_NOFOLLOW`/`O_DIRECTORY` are unavailable, return input-invalid, not a traceback (`:545-546`).
- Manifest directory is opened as given, once, and reused for pages (`:542-545,559`). A symlinked prefix in the caller's path is
  accepted by design: fixture `manifest_dir_caller_prefix` expects `clean` (`:868`). Round-28's repair-over-refusal family
  (`corpus/lessons/round-28.md:66-73`) says do not realpath-compare the caller's path.
- Page path confinement (`canonical_audit.py:583-595`): reject absolute, `ntpath.isabs`, drive prefix, backslash, and any
  `""`, `"."`, `".."` component. Then walk directories with `O_NOFOLLOW|O_DIRECTORY` and open the leaf with `O_NOFOLLOW`
  (`:597-613`, flags `:597-598`), `fstat` regular-file check (`:617`). Symlinked leaf and symlinked parent are both input errors
  (fixtures `:864-865`); traversal fixture `:863`.
- FIFO/device: `O_NONBLOCK` prevents a blocking open and `S_ISREG` rejects the opened object (`:561,567,617`; fixture `:866`).
  Add `getattr(os,"O_NOCTTY",0)` — no script in `scripts/` sets it (grep over `scripts/*.py`), and `round-28.md:112-114` records it.
- Size caps: manifest 1 MiB, page 2 MiB, 64 KiB chunks; oversize detected by reading `limit+1` bytes (`canonical_audit.py:24-26,523-535`).
  Trade-off: canonical maps page oversize to `html_unsupported` (`:619-621`), which the matrix forbids; use `input_invalid`.
  Note its selftest has no oversize fixture (grep: caps only at constants and reads) — add one in the new selftest.
- Decoding: manifest `utf-8-sig` strict (`:710`); page decode failure is input-class (`:634-637`). Never use `errors="replace"`.
- Audit mode performs no writes and no network (`:80-90`); every fd is closed on success and failure (`:572-575,625-627`).
- Accessibility contrast (a weakness, not a model): `load()` uses `Path.read_bytes/read_text` (`accessibility_packet.py:138-144`) —
  symlinks followed, no size cap, no `O_NONBLOCK` (a FIFO blocks); SHA-256 pins (`:140-142`) cover only POPULATION and SOURCE.

## 4. Manifest structural checks worth copying
- Exact key set `{version,pages}`; version must be `int` equal to 1 (a bool fails the `type` check); pages non-empty; duplicate
  `url` or `file` rejected (`canonical_audit.py:684-703`). Extend the key set to `{version,basePath,pages}` and validate
  `basePath` starts and ends with `/` per the matrix interface.

## 5. CLI/usage conventions
- `argparse` with `allow_abbrev=False` and a required mutually exclusive group (`canonical_audit.py:119-134`); repeated
  `--manifest` rejected by a custom Action (`:69-76`); `--selftest --json` is a usage error (`:132-134`).
- `accessibility_packet.py:208-214` counts duplicate occurrences of every option, including booleans, and emits the usage JSON
  with 64. `round-28.md:98-100` lists repeated `--population`, `--ledger`, `--revision`, `--root` as an open failure family in
  `citing_set.py` (`:639-647` has no duplicate guard). New tool: reject any repeated option; at minimum `--manifest`.
- Help: canonical keeps `add_help=True` and documents `--help` as exit 0 with no verdict, checked in its selftest
  (`canonical_audit.py:80-84,1007-1013`); accessibility sets `add_help=False` (`:203`), so `--help` is usage-64. Matrix does not
  test help; canonical's behaviour is the documented lane precedent.

## 6. Selftest conventions
- Preferred pattern (`canonical_audit.py:872-883`): drive the real CLI as a subprocess with `sys.executable -B`,
  `capture_output`, `text`, UTF-8 with `errors="replace"`, `timeout=10`, `check=False`; run inside `tempfile.TemporaryDirectory`
  (`:944`); one record per case with expected/actual/ok (`:946-955`); a single JSON summary and 0/1/2 exit (`:1016-1021`).
- Fixture construction covers regular, symlinked leaf, symlinked parent, FIFO, traversal, manifest symlink, caller-prefix symlink,
  empty manifest, duplicate pages (`canonical_audit.py:899-939,957-981`); usage rows cover missing/unknown/abbreviated/repeated
  options and conflicting modes (`:985-1006`).
- Accessibility's in-process table (`accessibility_packet.py:150-190`) is cheaper but cannot observe exit codes or stdout;
  with a contract made of exit plus JSON, use canonical's subprocess harness.
- Compare `(exit, sorted reason/element/attribute/value tuples)` like `c2_matrix_count.py:62-72`, not just finding ids
  (`round-28.md:101-106` shows id-only checks can pass for the wrong reason). Cover D1-D14, I1-I8, U1 families plus clean controls.

## 7. Round-28 open failure families to avoid from day one (`corpus/lessons/round-28.md:95-116`)
- Duplicate-key JSON accepted (`:98-100`): reject with `object_pairs_hook` (`accessibility_packet.py:50-55`).
- Nonfinite JSON accepted (`:99-100`): `parse_constant` raises (`accessibility_packet.py:58-63`).
- Deep nesting with stack-dependent limits under CPython 3.14 (`:113-114`): pre-scan depth cap 64 (`accessibility_packet.py:33-47`)
  and convert `RecursionError` to `ValueError` (`:63-65`). Plain `json.loads` (`canonical_audit.py:710`) accepts all three families.
- Repeated options last-wins (`round-28.md:98-100`): see section 5.
- Missing `O_NOCTTY` on device opens, and socket opens mislabelled unreadable (`:112-114`): see section 3; matrix compares reason
  only, so failure detail must stay outside the compared keys.
- A ~990-level directory crashes a recursive walk (`:112-113`): avoid directory recursion entirely; pages are explicit paths.

## Commands run (all read-only)
- `grep -n … scripts/canonical_audit.py`, `scripts/accessibility_packet.py`, `scripts/citing_set.py` — exit 0.
- `read` over `canonical_audit.py:1-140,523-640,684-780,872-940,941-1040`, `accessibility_packet.py:1-222`,
  `corpus/lessons/round-28.md`, `c2_matrix_count.py:55-100` — exit 0.
- `python3 -c` inspection of `c2-matrix.json` — first variant exit 1 (U1 has `findings:null`), corrected variant exit 0.
- `mkdir -p /fast/scratch/hyaku/kake-r29/w1/ScoutGateConventions` — exit 0. No installs, no network, no Git/jj mutation.

## Not verified
- Neither gate was executed; no claim here is a runtime observation. `c2_matrix_count.py` was not run (tool absent at this
  revision; executor scope), and no check was made of whether the eventual tool satisfies the matrix. Advisory input only.
