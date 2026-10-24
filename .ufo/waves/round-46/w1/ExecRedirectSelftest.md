# ExecRedirectSelftest

Axis: operability.

## Outcome

**FAIL / blocked against the named attack:** `scripts/redirect_audit.py --selftest` could not run because the assigned tool file was absent. The six requested mutation probes are unrun, not survivors. I did not edit the tool or any peer-owned implementation path.

## Decisive command evidence

From `/home/vgpnk/Projects/shokunin/kake-shokunin`:

```text
python3 -B scripts/redirect_audit.py --selftest
```

Verbatim stderr (stdout empty):

```text
python3: can't open file '/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/redirect_audit.py': [Errno 2] No such file or directory
```

Exit code: `2` (`Command exited with code 2`). A direct read of `scripts/redirect_audit.py` also returned not found. Therefore there was no source to copy under scratch or test against the mutations: drop status check; drop first-match order; drop existing-resource precedence; accept malformed rules; always-clean return; skip URL-decoding. All six are **BLOCKED — not run**; none is scored killed/survived.

## Commands run

```text
mkdir -p /fast/scratch/hyaku/kake-r46/ExecRedirectSelftest
python3 -B scripts/redirect_audit.py --selftest
mkdir -p .ufo/waves/round-46/build
```

The scratch directory was empty after setup. No tools were installed.

## Files written

- `.ufo/waves/round-46/build/redirect-selftest.md` — evidence and mutant-kill table.
- `.ufo/waves/round-46/w1/ExecRedirectSelftest.md` — this scoped report.

Detailed evidence: `.ufo/waves/round-46/build/redirect-selftest.md`.
