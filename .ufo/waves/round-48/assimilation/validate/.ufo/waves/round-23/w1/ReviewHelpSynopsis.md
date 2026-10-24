## Verdict

Recommendation: **P3 operability wording correction**. The target tree's canonical-audit parser accepts both help aliases, but its explicit help synopsis advertises only `-h`, while the options list advertises both; the usage text printed on errors is a third presentation. Other probed mode/flag combinations matched the documented constraints. This is a review recommendation, not independent admission.

Reviewed commit `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc` from an archive extracted under `/tmp/kake-r23-ReviewHelpSynopsis-83LO` (the lane's observed HEAD was `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`). No lane production files were changed.

## Findings

### P3 — custom synopsis omits the accepted `--help` alias and differs on usage errors

- **Path/evidence:** `scripts/canonical_audit.py:78-81,119-133` in the reviewed tree. `parse_cli()` uses `add_help=True` and the explicit usage string `canonical_audit.py --manifest PATH [--json] | --selftest | -h`; `usage()` prints `usage: canonical_audit.py --manifest PATH [--json] | --selftest` followed by a separate `--help prints standard CLI help...` sentence.
- **Command:** `python3 -B /tmp/kake-r23-ReviewHelpSynopsis-83LO/scripts/canonical_audit.py --help --not-a-flag && printf 'PROBE_RC=0\n'`
- **Exact observed output (exit 0):**

  ```text
  usage: canonical_audit.py --manifest PATH [--json] | --selftest | -h

  Offline static canonical preflight; --help is documentation only.

  options:
    -h, --help       show this help message and exit
    --manifest PATH
    --selftest
    --json           emit JSON (the default)
  PROBE_RC=0
  ```

  `--help` is accepted although the explicit synopsis shows only `-h`. The same help output and `PROBE_RC=0` resulted from `--manifest /tmp/kake-r23-ReviewHelpSynopsis-83LO/probe-manifest.json --help`: argparse exits for help instead of auditing the manifest. Thus the synopsis is not an exact representation of supported help spellings/precedence, and the error-path synopsis also differs from the help-path synopsis.
- **Impacted claim/axis:** operability; CLI documentation is internally inconsistent, though both help aliases work and this does not block a valid audit.
- **Smallest fix:** use one synopsis for `ArgumentParser(usage=...)` and `usage()` that names both `-h` and `--help` (or remove the manually inserted help branch and make the options list the canonical disclosure). Keep normal argparse help precedence unchanged.

## Checked and held

- `python3 -B /tmp/kake-r23-ReviewHelpSynopsis-83LO/scripts/canonical_audit.py --manifest /tmp/kake-r23-ReviewHelpSynopsis-83LO/probe-manifest.json` and the same command with `--json` before `--manifest`: exit 0; exact stdout `{"findings":[],"pagesChecked":1,"verdict":"clean"}`.
- `python3 -B /tmp/kake-r23-ReviewHelpSynopsis-83LO/scripts/canonical_audit.py --selftest`: exit 0; JSON reported `"passed": true` and all case records `"ok": true`.
- `--selftest --json` and `--selftest --manifest /tmp/kake-r23-ReviewHelpSynopsis-83LO/probe-manifest.json`: exit 64; respective stderr starts `canonical_audit.py: --json is only valid with --manifest` and `canonical_audit.py: argument --manifest: not allowed with argument --selftest`; stdout in each case was `{"findings":[],"pagesChecked":0,"verdict":"could-not-evaluate"}`.
- No arguments: exit 64; stderr starts `canonical_audit.py: one of the arguments --manifest --selftest is required`; the error synopsis is `usage: canonical_audit.py --manifest PATH [--json] | --selftest`.
- Repeated `--manifest` was rejected with exit 64 and `canonical_audit.py: --manifest may be given only once`. The minimal manifest and HTML fixture were created only inside the `/tmp` probe directory.

## Limits

- LSP status/references/definition/diagnostics could not be used: both `read xd://lsp` and an `xd://lsp` status attempt returned `No such tool: xd://lsp` (no LSP device was mounted). Source was read from the target commit; a literal search only located argparse declarations, and is not semantic evidence.
- No public web surfaces, publishing actions, or live freshness checks were involved. Round-23 freshness, runtime routing/saturation, and resume-continuity checks are outside this CLI synopsis assignment. No tools were installed or updated.
