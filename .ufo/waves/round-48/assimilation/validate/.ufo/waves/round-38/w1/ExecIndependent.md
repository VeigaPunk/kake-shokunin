# Kake R38 W1 — ExecIndependent (blind independent implementation, C2 contract)

Built the round-38 contract from the public text only (round-37 contract + amendments (h), (i),
(k)), starting from the round-37 independent file, without reading the builder's tool, the L1
reference, or anything sealed. No access to `/fast/scratch/hyaku/kake-r38*`.

## Deliverable

- `/fast/scratch/hyaku/kake-r38w1/ExecIndependent/independent_robots_audit.py`
  sha256 `ee78ba4656bed0638d1c7df06f267bad6d1f1b6711a4cef2b32e039bb30495b1` (14 262 bytes,
  `bash: sha256sum` exit 0). Written from `git show 2dab7f31:.ufo/waves/round-37/retained/
  independent/independent_robots_audit.py` (sha256 `3400abd5…bdb8`), modified for (h), (i), (k)
  and the NUL-path crash. L1 copies it into the lane; nothing in the lane was written.

## Harm instruments (declared gates), exit codes measured

1. `python3 -B <lane>/.ufo/waves/round-37/sealed_count.py --root /fast/scratch/hyaku/kake-r38w1/ExecIndependent/clone --tool-file .../independent_robots_audit.py --key-revision 424aa248`
   → exit **0**, `passed 28 of 28`, `met true`, receipt `r37_counter.json`
   (sha256 `f418f343…`, counterSha256 `2ebb39b585e2…`, toolSha256 `ee78ba46…`). Clone HEAD `2dab7f3114f3e9dcf072b524c88816ab05fdfcf1`.
2. `python3 -B clone/scripts/robots_audit_selftest.py --tool .../independent_robots_audit.py`
   → exit **0**, `137/137`, `failed 0`, stderr 0 bytes, receipt `selftest.json` (sha256 `155f64fa…`).

## What changed (all in the sandbox file)

- (h) `json.loads(..., parse_int=parse_json_int, parse_constant=reject_json_constant)`:
  `NaN`/`Infinity`/`-Infinity` raise → one `input_invalid`, exit 2. Integer literals carry a
  route to a non-int `LongInteger` sentinel: > 4000 digits, or `int()` refused by a lowered
  `sys.set_int_max_str_digits` limit. Out-of-range status of any length → `check_invalid` (other
  checks still evaluated); long numbers in unread fields are inert.
- (i) `url_characters_ok()` on the raw string before parsing: ASCII outside letters, digits,
  `-._~`, `:/?#[]@!$&'()*+,;=%` → `check_invalid`; non-ASCII kept; `%` allowed anywhere.
- (k) `path_to_match()` → `normalize()` once, compare with `/robots.txt` before opening the file.
  `/robots%2Etxt`, `/%72obots.txt`, `/robots.txt?` (empty query) allowed; `/ROBOTS.TXT`,
  `/robots.txt?x=1`, `/robots%2Ftxt` decided by rules; fragment never part of the path.
- NUL crash: `"\x00" in robots` → `check_invalid` before any `os.path` call; `os.stat`/`open`
  now catch `ValueError` as well as `OSError`.
- Wildcard matcher replaced the backtracking regex with an exact windowed segment scan (the
  round-37 regex could backtrack; the round-37 tool hung on this). Falsifier:
  `python3 -B fuzz_matcher.py <tool>` → exit 0, `checked=200000 mismatches=0` against the
  round-37 regex formulation over random rules (mid-rule `$`, `*`, `/`, `%`).

## Targeted falsifiers (my own, in the sandbox)

Harness hashes: `fuzz_matcher.py` `63822571…`, `feature_tests.py` `4fef541c…`.

`python3 -B feature_tests.py <tool>` → exit **0**, 28/28 PASS: h1–h11 (NaN/±Infinity, 1e400,
4000- and 5000-digit statuses, 5000-digit unread field, huge `version`, 64 MiB literal as unread
field and as status, each ≤ 0.08 s), i1–i8 (space, `{`, leading/trailing space, `\`, U+0007,
DEL, non-ASCII kept, `%zz` kept), k1–k8, n1 (`r\u0000.txt` → `check_invalid`, exit 2, valid JSON,
stderr 0 bytes). Extra probe: `q0` `?`-only query, `q1` doubly encoded path, `q2` query+fragment,
`q3` control — only `q3` blocked, exit 1.

## Independent readings where the text left room

From the file docstring (1–14): (k) compares the *normalized* path-to-match, and the implicit
allow is returned before opening the robots file (as round 37); 512000 bytes applied to raw bytes
before BOM drop; robots path relative iff not `/`-rooted, realpath must start with real manifest
dir + separator; duplicate ids include earlier invalid checks; missing manifest = not a regular
file (input_invalid, not usage); unreadable-but-validated robots file → `check_invalid`;
A–Z-only folding; URL valid iff scheme http/https (case-insensitive) and non-empty host;
normalization covers query too; 4000-digit conversion threshold; `RecursionError` on the manifest
→ `input_invalid` (cannot be read); (i) judged before parsing with `%` unconditioned; NUL in a
robots path is `check_invalid`; group/rule parsing and all other round-37 readings unchanged.

## Not verified / risks

- The round-38 v3 counter was **not run**: no key, and the sealed trees were not touched. My
  `checksEvaluated` and (h)/(i)/(k) behaviour are checked only by my harness and the two gates
  above; 20/20 against the sealed cases is unmeasured by me.
- Exactness against the L1 reference on the 20 sealed cases is unknown by design (blind).
- Duplicate JSON member names left undecided (per the declaration).
- No tools installed or upgraded; no lane file, Git or jj state touched. Lane untouched: all
  commands ran in `/fast/scratch/hyaku/kake-r38w1/ExecIndependent/` (clone + `tmp/`).
