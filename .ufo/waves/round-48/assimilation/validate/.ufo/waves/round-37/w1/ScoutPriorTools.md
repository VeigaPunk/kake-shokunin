# ScoutPriorTools — conventions of the lane's offline audit tools (round 37, wave 1)

Question: what do `scripts/canonical_audit.py`, `base_path_audit.py`, `link_preview_audit.py`, `source_recheck.py` and their selftests hold in common, and which of those conventions does the C1 robots contract break?

Method: lane read at `4b089da699cfaaf5ebeb6a0746b7e4238602e20a`; tools and selftests executed in a sandbox clone (`/fast/scratch/hyaku/kake-r37w1/ScoutPriorTools/clone`). The sealed key tree was not touched and the C1 counter was not run (no key). No `lsp` device is mounted in this session (`read xd://lsp` → "No such tool: xd://lsp. Mounted devices: ast_edit, debug"), so every code claim below is literal `file:line` plus observed process behaviour, not semantic resolution.

## Conventions (file:line)

| # | Convention | Precedent |
|---|---|---|
| 1 | One stdlib-only file in `scripts/`; `python3 -B scripts/<tool>.py --manifest PATH`; no network, no writes | canonical_audit.py:1-7, base_path_audit.py:1-6, link_preview_audit.py:1-14, source_recheck.py:1-20 |
| 2 | One JSON object on stdout; exit 0 clean, 1 failed-policy, 2 could-not-evaluate | canonical_audit.py:113-115, base_path_audit.py:162-166, source_recheck.py:13-21 |
| 3 | `EXIT_CLEAN=0 EXIT_POLICY=1 EXIT_INPUT=2 EXIT_USAGE=64` constants at module top | canonical_audit.py:28-31, base_path_audit.py:76-79, link_preview_audit.py:65-68, source_recheck.py:42-45 |
| 4 | Report shape `version`,`verdict`,`checksEvaluated`,`findings` | only source_recheck.py:34,576-583; older tools use `pagesChecked` (+`referencesChecked`): canonical_audit.py:767-773, base_path_audit.py:759-766, link_preview_audit.py:166-167 |
| 5 | Finding identity `{"check": id-or-null, "reason": R}` | source_recheck.py:374-375, projected on (check, reason) at source_recheck_selftest.py:703-719; older tools use `id`: canonical_audit.py:767, base_path_audit.py:110-116, link_preview_audit.py:160-166 |
| 6 | Blocking reason names `input_invalid`/`check_invalid` force could-not-evaluate | source_recheck.py:52,566-573; `input_invalid` also canonical_audit.py:34, base_path_audit.py:84 |
| 7 | Invalid check → `check_invalid` with its id when a non-empty string else null; `checksEvaluated` counts only valid checks; other checks still evaluated | source_recheck.py:416-422,624-630 (observed) |
| 8 | JSON integer check rejects booleans and floats (`isinstance(v, bool) or not isinstance(v, int)`) | source_recheck.py:450 (observed: status 200.0 and `true` both `check_invalid`) |
| 9 | Bounded streaming read, 64 KiB chunks; manifest/HTML caps 1 MiB/2 MiB (older) or 4 MiB/16 MiB | canonical_audit.py:523-534,24-25; base_path_audit.py:247-258,71-72; link_preview_audit.py:73-74 |
| 10 | Non-regular/symlink handling: manifest no-follow open + S_ISREG, pages walked by dirfd with O_NOFOLLOW | canonical_audit.py:543-628, base_path_audit.py:260-336; newer pattern is `resolve()` + `relative_to()` containment: link_preview_audit.py:183,212-213,232-239 |
| 11 | Repeated `--manifest` is a usage error | canonical_audit.py:69-76,131-134, base_path_audit.py:131-139, link_preview_audit.py:330-333; source_recheck.py:591-611 rejects repeats but accepts `--manifest=PATH` |
| 12 | Usage-error output: two tools print the could-not-evaluate report on stdout at exit 64, two print stderr only | prints: canonical_audit.py:1028-1031, base_path_audit.py:772-779; silent: link_preview_audit.py:336-341, source_recheck.py:614-618 (observed) |
| 13 | `--help` exits 0 and emits no verdict | canonical_audit.py:81, base_path_audit.py:143, argparse default in link_preview; source_recheck instead exits 64 (observed, no stdout) |
| 14 | Selftest is a separate `scripts/<stem>_selftest.py` | base_path_selftest.py:1-9, link_preview_selftest.py:1, source_recheck_selftest.py:1-20; canonical_audit.py:129,941 embeds `--selftest` instead |
| 15 | Fixtures either on-disk case dirs (`manifest.json`+`expected.json`) or an in-code `FIXTURES` list built by `add(name, contract, …)` and materialised into one mkdtemp | base_path_selftest.py:51,163-179; link_preview_selftest.py:14,46-56; source_recheck_selftest.py:176-205,735-749 |
| 16 | Fixture floor below which the harness says could-not-evaluate and exits 2 (drift guard) | base_path_selftest.py:55 (45), link_preview_selftest.py:14 (20), source_recheck_selftest.py:91 (40) |
| 17 | Selftest stdout one JSON summary (`selftest`,`tool`,`cases`,`passed`,`failed`,`passedOverTotal`,`verdict`,`failures`), human lines on stderr, exit 0/1/2 | base_path_selftest.py:238-251,296-310; link_preview_selftest.py:144-156; source_recheck_selftest.py:863-875 |
| 18 | Case env `-B`, `PYTHONDONTWRITEBYTECODE=1`, `LC_ALL=C.UTF-8`, per-case timeout | base_path_selftest.py:54,156-179; link_preview_selftest.py:15,19-24; source_recheck_selftest.py:92,696-700 (60 s; others 120 s) |
| 19 | Compare exit, verdict, projected findings, plus counters only when pinned; usage cases skip JSON shape | base_path_selftest.py:181-225; source_recheck_selftest.py:654-661,792,810-845 |
| 20 | No-write assertion by snapshotting the work tree before/after → "tool wrote files" | source_recheck_selftest.py:731-733,759-775 |
| 21 | One manifest per fixture run; `accept` lists alternative outcomes, never several manifests in one case | source_recheck_selftest.py:179-197,810-845 |

## Contract departures (C1 vs the tools above)

- D1 `--help`. C1: "any argument list other than exactly `--manifest PATH`" is a usage error, so `--help` → 64. Three older tools exit 0 with help. Matters: use `add_help=False`; round-36 is the matching precedent. The contract describes no help text, so help output gains nothing, while a case written literally from the contract text could expect 64 for `-h` [INFERENCE on what the sealed cases test].
- D2 `--manifest=PATH`. C1's literal reading rejects the `=` form; source_recheck accepts it (source_recheck.py:599-602). Matters: a case written literally from the contract text could expect 64 for the `=` form [INFERENCE]; strict literal is the safe reading.
- D3 Cap. C1 fixes 64 MiB for the manifest, 16-64× the 1/2/4 MiB precedents. Matters: must stream with a bound (row 9) and detect a >64 MiB file without slurping it; the sealed (g) case supplies one.
- D4 Symlinks. C1 (f) resolves symlinks and `..` for the robots path and requires a regular file after resolution; the newest strict tools reject every symlink with O_NOFOLLOW. Observed: base_path_audit.py exits 2 `input_invalid` on an in-directory symlink, link_preview_audit.py evaluates it. Matters: reuse link_preview's resolve+containment shape, not `read_page_bytes`; an in-directory symlink must be accepted, an escaping one `check_invalid`.
- D5 Continuation. C1 (f): other checks still evaluated. source_recheck does this (observed: `checksEvaluated` 1, `check_invalid` + a policy finding from the valid check, exit 2); base_path aborts the whole run on the first page fault (base_path_audit.py:717-724; observed `pagesChecked` 0 with a clean page present). Matters: copy source_recheck.
- D6 JSON strictness. base_path (`strict_json`, 206-238) and link_preview (172-181) reject duplicate keys, non-finite numbers and deep nesting as `input_invalid`; canonical and source_recheck use plain `json.loads`. C1 (g)'s fault list is closed and omits these. Matters: plain `json.loads` stays inside the contract; extra strictness adds unlisted rejections.
- D7 Field names. C1 uses `check` and a report `version`, i.e. it continues round 36 and breaks the `id`/`pagesChecked` habit of the three older tools. This is not a defect, but a builder copying base_path emits findings without `check` and the sealed projection reads null. The `version` field is checked by no counter (round-36 lesson line 116), so only the selftest can catch it.
- D8 `checksEvaluated` is compared by no counter either (same lesson line). The C1 selftest must pin it (valid-only counting) or a wrong count ships unnoticed.
- D9 No `--selftest` mode is admissible under C1's usage rule, so the embedded-selftest pattern (canonical) is excluded; the selftest must be `scripts/robots_selftest.py`.
- D10 C1's (g) cases are five runs each; no harness today runs several manifests in one case. A `runs` list is needed (or five fixture entries).
- D11 Usage stdout. Printing the could-not-evaluate report at exit 64 (canonical/base_path habit) is harmless under C1's stated comparison and covers a sealed case that parses it; printing nothing also passes today. Print.

## Observed runs (sandbox clone at 4b089da; TMPDIR under the sandbox, `timeout 300`)

- `python3 -B scripts/base_path_selftest.py` → exit 0, `cases 45 passed 45`, `45/45 clean`
- `python3 -B scripts/link_preview_selftest.py` → exit 0, `cases 46 passed 46`, `46/46 clean`
- `python3 -B scripts/source_recheck_selftest.py` → exit 0, `cases 101 passed 101`, `101/101 clean` (all three in 6.9 s)
- Usage probes (`--help`; no args; `--manifest /nonexistent.json extra`): canonical 0/64/64 (stdout JSON on the 64s); base_path 0/64/64 (JSON on the 64s); link_preview 0/64/64 (empty stdout); source_recheck 64/64/64 (empty stdout, stderr `usage: …`).
- Symlink probe (`exp/bp`, `exp/lp`, real.html + link.html symlink): base_path `input_invalid` exit 2; link_preview `clean` exit 0, `pagesChecked` 1; symlinked manifest → base_path exit 2.
- Mixed manifest probe (`exp/sr/manifest.json`, one bad body + one good check): source_recheck `{"version":1,"verdict":"could-not-evaluate","checksEvaluated":1,"findings":[{"check":"bad","reason":"check_invalid",…}]}` exit 2; with the good check failing its quote, its `quote_missing` finding is kept alongside `check_invalid`, exit 2.
- base_path with one clean page plus one missing page: only `input_invalid`, `pagesChecked` 0, exit 2 — no continuation.
- Float/boolean status probe: both `check_invalid`, `checksEvaluated` 0, exit 2.

## Not verified / limits

- No sealed case, key or counter was read or run; nothing here predicts C1's score.
- No LSP server exists in this session (see Method), so call-graph claims are text-derived; the executed probes above are the only behavioural proof.
- I did not inspect `citing_set.py` or the `.mjs` tools; they are outside the offline-audit family named in the assignment. No tools were installed or upgraded.
