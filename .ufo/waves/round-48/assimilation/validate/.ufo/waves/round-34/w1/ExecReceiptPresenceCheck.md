# Round 34 W1 — receipt presence check

Axes: **operability** (a missing-receipt claim fails) and **freshness** (receipts are read from the requested committed revision).

Built `receipt_presence_check.py` at `/fast/scratch/hyaku/kake-r34/w1/ExecReceiptPresenceCheck/clone/.ufo/waves/round-34/criteria/receipt_presence_check.py` (SHA-256 `172b08eb5400787c36facf76a75a373c7f2d3983a50c8baf8a0e8804f46e1bff`). It parses hashes in measured values of the report's `Before → after measurements` table, then reads only committed files under `.ufo/waves/round-N/verification/` at `--rev`. It accepts JSON root `revision` or legacy `rev` fields starting with a measured hash, or a UTF-8 text receipt naming it. Exit 1 lists missing hashes; exit 0 reports all found; malformed/unreadable inputs exit 2.

Evidence: source report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kake.md:58-66`; the table claims `93359ff: 4/4 (run, not committed)` at line 62. The committed `c1-after-b1752a2.json` at `93359ff0924bf622acc51eb15c2afa3cd2743022` uses the `rev` key (`b1752a2480aa86fc27536dd6e7d27a91b52bed12`), motivating legacy-key support. The modified test copy is `/fast/scratch/hyaku/kake-r34/w1/ExecReceiptPresenceCheck/inputs/kake-round-33.md`; its line 62 removes only the `93359ff` run from the measurement cell.

Commands and results (Python runs used `python3 -B`; no test/build/lint/formatter beyond the requested runs):

1. Initial diagnostic, before supporting the existing `rev` receipt key; exit **1**, output `unreceipted hashes: 93359ff, b1752a2`:
   `python3 -B /fast/scratch/hyaku/kake-r34/w1/ExecReceiptPresenceCheck/clone/.ufo/waves/round-34/criteria/receipt_presence_check.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kake.md --repo /home/vgpnk/Projects/shokunin/kake-shokunin --rev 93359ff0924bf622acc51eb15c2afa3cd2743022 --round 33`
2. Final required report run; exit **1**, output `unreceipted hashes: 93359ff` (same command as item 1 after the key fix).
3. Final run on the copy with the measured run removed; exit **0**, output `all measured hashes have committed receipts`:
   `python3 -B /fast/scratch/hyaku/kake-r34/w1/ExecReceiptPresenceCheck/clone/.ufo/waves/round-34/criteria/receipt_presence_check.py --report /fast/scratch/hyaku/kake-r34/w1/ExecReceiptPresenceCheck/inputs/kake-round-33.md --repo /home/vgpnk/Projects/shokunin/kake-shokunin --rev 93359ff0924bf622acc51eb15c2afa3cd2743022 --round 33`

Known blind spots: recognizes the exact section heading and before/after table, and measured fractions or numeric arrows; it does not resolve prose such as “same revisions” to hashes elsewhere. Text receipt matching accepts hash prefixes in any UTF-8 non-JSON file under the verification directory, so a coincidental prefix can satisfy it. JSON matching is limited to root `revision`/`rev`. It intentionally cannot see uncommitted receipts.

Blockers: none. LSP tooling was not available in this seat's tool inventory. No tools installed. The only lane write was this report; the checker and modified test copy remain in the assigned sandbox.
