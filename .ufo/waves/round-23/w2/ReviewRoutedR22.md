## Verdict

Counterexample found. The round-23 lesson says the `ReviewHelpSynopsis` P3 was fixed by putting `--help` in the synopsis, but the separately printed usage-error synopsis still differs and omits the `-h` alias. This is a residual P3 documentation inconsistency, not a broken help invocation. The other requested routed dispositions checked out or remain explicitly recorded as open.

## Findings

### P3 — Help-synopsis disposition is only partially closed

**Path/evidence:** `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-23.md:74` records `ReviewHelpSynopsis (P3 fixed: --help in synopsis)`. In the current `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py`, `parse_cli()` sets argparse's help synopsis at line 122 to include `-h | --help`; however, `usage()` at lines 78–81 supplies a separate error-path synopsis that ends at `--selftest`, followed by a sentence mentioning `--help` but not `-h`. `main()` prints that separate helper for usage errors (lines 1027–1029).

**Exact commands and observed output:**

```text
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B scripts/canonical_audit.py --help
exit=0
usage: canonical_audit.py --manifest PATH [--json] | --selftest | -h | --help

Offline static canonical preflight; --help is documentation only.

options:
  -h, --help       show this help message and exit
  --manifest PATH
  --selftest
  --json           emit JSON (the default)
```

```text
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B scripts/canonical_audit.py --not-a-flag
exit=64
stdout: {"findings":[],"pagesChecked":0,"verdict":"could-not-evaluate"}
stderr prefix:
canonical_audit.py: unrecognized arguments: --not-a-flag
usage: canonical_audit.py --manifest PATH [--json] | --selftest
--help prints standard CLI help, exits 0, and emits no publishing verdict.
```

The P3's accepted-`--help` omission in argparse help output is fixed, but its reported error-path synopsis discrepancy remains; the error synopsis also does not list the accepted `-h` spelling. **Impacted claim/axis:** round-23 routed disposition 4 / `ReviewHelpSynopsis`, operability. **Smallest fix:** use the same synopsis for `ArgumentParser(usage=...)` and `usage()`, listing both help spellings, or revise the lesson's disposition to say the fix was limited to argparse help output and retain the error-path difference as a residual.

## Checked and held

- **Correction register:** `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md:106` retains the historical inverted predicate; lines 121–127 explicitly correct its interpretation. The before-fix reproduction below shows the c0fd6d5 counter returning exit 1 with all three counter-examples `rejected:false`. Against the current measure, `counter-probe.py --lane . --measure .ufo/waves/round-22/measure.py` emitted `passed:true`, with CE1–CE3 all `rejected:true`; `counter-probe.py` returns 0 when `passed` is true (source line 78). The current defect probe emitted `met:8`, `total:8`, `passed:true`; its source returns 0 when passed (line 114). The correction's counter predicate and its statement that the defect-probe failure predicate remains correct are consistent with these results.
- **REPRODUCE.md:** Ran the documented `git show c0fd6d5:...` materialization and both probe commands, using scratch directory `/tmp/kake-r23w2-ReviewRoutedR22-VAUr`. Observed defect probe exit 1, `met=2/8`, `passed=false`; counter probe exit 1, `passed=false`, and CE1–CE3 each `rejected:false`. Recreated runner SHA-256 values were `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7` (validator) and `329f45b67b3610c5ac132ef53f3428ad8dc9c2dd065ec0a96834a08b71ab9c49` (measure), matching the documented prefixes and committed before receipts. This agrees with `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/w1/ExecReproduceBefore.md` (`all_matched:true`).
- **Misroot move:** Compared each destination file byte-for-byte against `git show d5a0369:<name>` using `cmp`; both returned 0. SHA-256 pairs matched exactly: `err.txt` `e19fd26e3fc308498b111052cc1b858807976805e4e1354334e45bd686916bd1`; `out.txt` `1a3935f52600fec84ccd5f8212cffbf4544ec05b646d1e7c1f28cbf25ba52493`. Both lane-root paths are absent. Commit `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b` records adds under `.ufo/waves/round-22/residual/misroot/` and deletes at root. The move preserved bytes.
- **Four w1 seat reviews:** All four named reports exist. `ReviewDotdotSplit.md` records its scoped no-finding result with adversarial `..`/symlink probes. `ReviewHelpSynopsis.md` records the P3; the closure is only partial as detailed above. `ReviewFdOwnership.md` reports a descriptor leak only under a Python-injected exception before the `close()` syscall, and expressly says it did not reproduce a kernel close error; the round-23 lesson preserves that qualification, so this is not demonstrated as a production failure. `ReviewCounterPins.md` demonstrates an unpinned fixture-change P2; it remains an acknowledged gap, not a claimed fix. The committed replay inventory includes 64 fixture paths, and `replay-after.json` reports `inputsVerified:69`, `casesCompared:32`, and no per-case mismatches. That replay protects the frozen evidence bytes; it does not remove the measure counter's fixture-pin gap. The lesson records the P2 and the decision not to alter the frozen round-22 runner.

## Limits

No production file was changed; this report is the only lane write. No tools were installed. I ran only the requested before-fix reproduction and targeted read-only CLI/probe checks; no build, lint, formatter, or broad suite was run. The help finding concerns output consistency only; `--help` itself exited 0 and exposed both accepted spellings.