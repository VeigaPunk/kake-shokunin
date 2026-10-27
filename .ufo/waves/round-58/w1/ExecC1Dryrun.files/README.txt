ExecC1Dryrun dry-run receipts (round-58 w1). Each file is the verbatim stdout of
  python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root <clone> --revision <rev> --list
run in a throwaway shared clone (/fast/scratch/.../clone, deleted after this seat) whose ancestry is the lane's.
Commit map in the clone: cc8da16 = lane tip the clone started from (base 0440485 + contract fff3eea + spec),
T0=7336f7c ledger+after-c2/after-c3 receipts, T1=26b1d2c C1 receipt committed, T1b=0a7d7a8 SCORECARD/LOG/report
edits, T2=b06e874 C1-receipt rewrite, T3=474af1b census-before.txt rewrite, T4=0222160 census rewrite disclosed.
Extra probes p2..p8 are named in the seat report. p1-stale-ledger-at-411db8d.txt is the round-57 rewrite with the
ledger still at 19 entries (the earlier `git revert` of the disclosure commit did not apply and produced a noop
commit, so that stale-ledger probe was re-run at the proper revision).
