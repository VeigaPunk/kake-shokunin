# ExecRecheckHardening — round-37 wave 1, carried round-36 tool defects (routed defect 8)

Status: complete; sandbox only (`/fast/scratch/hyaku/kake-r37w1/ExecRecheckHardening/`); lane repo,
jj state and Git index untouched; no tools installed; `/fast/scratch/hyaku/kake-r37/` never touched.

## Contract (c) amendment — proposed sentence, verbatim

> A raw-element start tag counts only where a tag can start, not inside another tag's attribute value.

## Deliverables (sandbox; L1 copies)

- `clone/scripts/source_recheck.py` — sha256 `37a8a8ef491db584b9d53b50020a8dacf824d2588b3f7ba2e5125c6d1c820e95`
  - contract (g) "unreadable": `load_manifest` stats before open, refuses a non-regular file
    (`stat.S_ISREG`) or `st_size > MAX_MANIFEST_BYTES` (64 MiB, `:40`), opens `O_RDONLY|O_NONBLOCK`,
    re-checks `fstat`, reads at most `MAX_MANIFEST_BYTES + 1`, catches `MemoryError` (`:607-643`);
    FIFO, device and oversized manifests give one `input_invalid` (check null), exit 2.
  - contract (c) amendment: tag-aware scan — `tag_end` (`:288`, `>` inside a quoted `"`/`'` value does
    not end the tag), `raw_tag_name` (`:306`), rewritten `remove_raw_elements` (`:337`); dead
    `_RAW_START_RE` deleted. No `<` inside another tag's span (quoted or unquoted) opens a raw element.
  - `body_path` returns the path it validated, the realpath (`:457-479`), so `evaluate_check` opens
    the resolved body file instead of re-resolving the body symlink.
- `clone/scripts/source_recheck_hardening_selftest.py` — sha256
  `6e922c73e68427e2bb8e07f24397b96c56447ea7b3aa60d985c2f2b6591486e5`, 6 fixtures in the
  `source_recheck_selftest.py` fixture shape, `--tool PATH`. `scripts/source_recheck_selftest.py`
  was not edited.
- `hardening.patch` — sha256 `50af0bc6b4676d203739f35ad6706e2fa066d8c579d420824893fd15c7303125`,
  diff against `4b089da699cfaaf5ebeb6a0746b7e4238602e20a`; `git apply --check` on a pristine clone
  at that revision: exit 0.

## Fixtures: red on the `4d5b3d55` tool, green on the fix

| fixture | defect | base (`577b2d7d…`) | fix (`37a8a8ef…`) |
|---|---|---|---|
| g29-fifo-manifest | FIFO manifest blocks | killed at the 10 s cap, exit 124, no output | exit 2, `{"verdict":"could-not-evaluate","checksEvaluated":0,"findings":[{"check":null,"reason":"input_invalid","target":null}]}` |
| g30-huge-manifest | 1 GiB manifest, RLIMIT_AS 512 MiB | exit 1, `MemoryError` traceback, no JSON | exit 2, same `input_invalid` JSON |
| g31-device-manifest | `/dev/zero`, RLIMIT_AS 512 MiB | exit 1, `MemoryError` traceback, no JSON | exit 2, same `input_invalid` JSON |
| c-attributed-script | `<script` inside an attribute value | exit 1, `quote_missing` (page truncated) | exit 0, `clean` |
| c-attributed-script-real | genuine `<script>` still removed | exit 1, `k1` and `k2` quote_missing | exit 1, only `k2` (`bad()`) quote_missing; `LINK-TEXT` found |
| g32-body-open-resolved | check-then-open | opened `body.html` (the unresolved symlink) | opened `real-body.html`, never `body.html` (strace `openat`) |

## Commands and observed results (transcript `evidence/transcript.txt`, sha256 `ddc50c6c…`)

- `timeout 300 python3 -B scripts/source_recheck_hardening_selftest.py --tool <fix>` → `cases 6,
  failed 0, 6/6`, exit 0; with `--tool <base>` → `cases 6, failed 6`, exit 1 (failure lines in the
  transcript name each defect, e.g. g32: "tool opened the unresolved path 'body.html'").
- `timeout 600 python3 -B scripts/source_recheck_selftest.py --tool <fix>` → `101/101`, exit 0.
- `timeout 600 python3 -B .ufo/waves/round-36/sealed_count.py --root <clone> --tool-file <fix>
  --key-revision fd1fb7…` → `cases 28, passed 28, target 25, met true`, `toolSha256 37a8a8ef…`, exit 0.
- FIFO: `timeout 10 python3 -B <base> --manifest <fifo>` → exit 124 (still blocked); fix → exit 2.
- 1 GiB: `truncate -s 1G huge.json`; `( ulimit -v 524288; timeout 30 python3 -B <base> … )` → exit 1
  `MemoryError` at `load_manifest`; fix → exit 2 with the JSON report.
- `/dev/zero`: same caps, base exit 1 `MemoryError`; fix exit 2 with the JSON report.
- attribute body `<p title="see <script> note">VISIBLE-TEXT</p><script>hidden();</script><p>TAIL</p>`,
  quote `VISIBLE-TEXT`: base `{"verdict":"failed-policy", … "reason":"quote_missing"}`, exit 1;
  fix `{"verdict":"clean", … "findings":[]}`, exit 0.
- body symlink `body.html -> real-body.html`: `strace -f -q -e trace=openat` shows base opens
  `…/link/body.html`, fix opens `…/link/real-body.html`. Symlinked manifest still `clean`; a
  directory as `--manifest` gives `input_invalid`, exit 2.
- Applied-tree re-run (`evidence/applycheck.txt`, sha256 `f1aaeb05…`): pristine clone at `4b089da` +
  `git apply hardening.patch` → selftest `101/101` exit 0, hardening selftest `6/6` exit 0, sealed
  `28/28 met` exit 0, `toolSha256 37a8a8ef…`.

## Limits and carried risks

- The 64 MiB cap is a new deliberate refusal (contract (g) "unreadable"); exactly 64 MiB is still
  read and a manifest path that is a symlink to a regular file stays readable.
- `strip_tags` is untouched: contract (c) still strips "up to the next `>`", so a `>` inside a quoted
  attribute value still truncates tag stripping. Pre-existing wording; the 28 sealed cases and the
  round-36 selftest are unaffected (28/28, 101/101).
- The amendment lets quoted attribute values decide where a tag ends; a `<` in an unquoted value is
  inside the tag span already, so it also opens nothing.
- Body reads remain unbounded: a multi-gigabyte *regular* body still raises `MemoryError` with no
  report (manifests only were assigned); a sibling risk for a later round, not fixed here.
- Fixture g32 needs `/usr/bin/strace` (present); without it the fixture reports a failure, not a skip.

## Not verified

- The round-37 C1 counter (no key; never run, never looked for); `source_recheck_selftest.py` left
  byte-identical (another seat owns it); round-36 counter against the base tool (not needed).
