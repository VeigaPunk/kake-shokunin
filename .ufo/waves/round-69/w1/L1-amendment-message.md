Amendment 1 is in .ufo/waves/round-69/contract.md (section "Amendment 1"). Counter owners: apply the terms there.

ExecC1Counter: relabel only on the exact row regex with the observed integer; keep selftest and add cases (e) wrong integer and (f) id substring; the frozen pairs file is .ufo/waves/round-69/c1/pairs.json (sha256 4e787bcb...). Re-run base; deliver patch.diff, selftest.txt, base-run.txt.

ExecC2Fix: tmp_literals regex is quote-adjacent; replace offline_exit=0 with offline_unchanged (same exit and VERDICT as base on the same host); use distinct fresh dirs for TMPDIR and HOME; lstat for symlinks; output line "tmp_literals=N selftest_under_tmpdir=true|false offline_unchanged=true|false". Reword help text line ~182 and skipped message ~899 so they do not carry a /tmp literal. Default selftest dir from os.tmpdir().
