
## Round 87 — offline current-age probe registry

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| cache_current_age | probe | `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_current_age.py` (one JSON object on stdin) | `0=clean/calculated`: stdout contains the six calculated integer age terms only; `1=failed/invalid_input`: diagnostic identifier `invalid_input` on stderr. Calculated does not mean fresh, storable or reusable. | `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_current_age.py --selftest` (`--selftest`, not `--self-test`); CLI subprocess checks are separate from the frozen oracle. | `.ufo/waves/round-87/age-cases.json`: fixed seventeen-case oracle; twelve valid cases require complete six-key outputs, five invalid cases require exit 1. Registry text is not a successful execution receipt. | Normal invocation uses stdin/stdout only, with invalid-input diagnostics on stderr; no filesystem, clock or network reads, no persistent writes. Selftest fixture isolation is separate from normal operation. | kake |

Source and bounds: `corpus/knowledge/cache-current-age.md` (S462, RFC 9111
§4.2.3). The probe chooses the conservative corrected-initial-age maximum;
integer epoch seconds and arbitrary-precision Python arithmetic are local
adapter conventions. Missing Date is unsupported. Cache-Control interpretation,
storage/reuse approval, browser behavior and publishing remain outside this probe.
