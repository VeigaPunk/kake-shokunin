# Round 34 receipt-presence probe

Axes: operability and freshness. I tested the checker at pinned commit `24a16474ee73e20453f3e1be9d2f33573c5196d9`; checker SHA-256 `172b08eb5400787c36facf76a75a373c7f2d3983a50c8baf8a0e8804f46e1bff`. All report fixtures are under `/fast/scratch/hyaku/kake-r34/w2/MutReceiptPresenceCheck/reports/`.

Commands used `python3 -B /fast/scratch/hyaku/kake-r34/w2/MutReceiptPresenceCheck/clone/.ufo/waves/round-34/criteria/receipt_presence_check.py --report <fixture> --repo /home/vgpnk/Projects/shokunin/kake-shokunin --rev <revision> --round <n>`; `TMPDIR=/fast/scratch/hyaku/kake-r34/w2/MutReceiptPresenceCheck/tmp`, GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset. Each shell wrapper printed the checker exit code.

| Variant / fixture | Revision / round | Expected | Observed |
|---|---|---:|---|
| Full hash, table (`reports/full-hash.md:3-6`, 40-char `9ef758c…`) | `24a16474…` / 34 | 0 | 0, `all measured hashes have committed receipts` |
| 7-char (`reports/hash-7.md:3-6`, `9ef758c`) | `24a16474…` / 34 | 0 | 0, same success output |
| 8-char (`reports/hash-8.md:3-6`, `9ef758c9`) | `24a16474…` / 34 | 0 | 0, same success output |
| Hash/value in prose, table has value only (`reports/prose-hash.md`) | `24a16474…` / 34 | 2 under table-only format | 2, `error: measurement table contains no hash paired with a measured value` |
| Equivalent renamed heading (`reports/renamed-section.md`) | `24a16474…` / 34 | 2 under exact-heading format | 2, `error: report has no 'Before → after measurements' section` |
| Mismatched receipt revision (`reports/wrong-revision.md`, `93359ff…`) | `93359ff0924bf622acc51eb15c2afa3cd2743022` / 33 | 1 | 1, `unreceipted hashes: 93359ff0924bf622acc51eb15c2afa3cd2743022` |
| Same hash at current r34, where only an unrelated text diagnostic mentions it | `24a16474…` / 34 | 1 | **0**, `all measured hashes have committed receipts` — false pass |
| Plain-text-only name (`reports/txt-only.md`, `a0b0dff`) | `24a16474…` / 33 | 0 for text-receipt rule | 0, same success output |

A preliminary full/7/8-char probe used `24a16474ee73e20453f3e1be9d2f33573c5196d9` as the measured hash at `--rev 24a16474ee73e20453f3e1be9d2f33573c5196d9 --round 34`; each correctly exited 1 with its own hash in `unreceipted hashes`. The pinned tree has no `c1-at-24a1647` receipt, so I then used the receipted `9ef758c95d5e2e4d983df53ad00a084e2c5fb36f` to isolate hash-length behavior.

Mutation probe (report input only; checker bytes unchanged): pristine `reports/probe.md` was SHA-256 `4dfb71f35530c456fd22fdbe0e8e789defbcbfd4b92a4fba09ab9930f37e6d53`, measured `9ef758c…`; command at `--rev 24a16474ee73e20453f3e1be9d2f33573c5196d9 --round 34` exited 0. I changed that report to the full `93359ff…` hash (mutant SHA-256 `bd915de27728d4937b674455b6b9c7b9bf198413e0a38035d520f3ada6c8424c`); expected exit 1, observed exit 0 / `all measured hashes have committed receipts`. Verdict: survived; false pass. Restored the original bytes; SHA-256 returned to `4dfb71f35530c456fd22fdbe0e8e789defbcbfd4b92a4fba09ab9930f37e6d53` and restored rerun exited 0 with the success output. All three probe runs used `--report /fast/scratch/hyaku/kake-r34/w2/MutReceiptPresenceCheck/reports/probe.md` with the common command above.

Why the false pass: `round-34/verification/criterion-receipt-presence-r33-report.txt:1` says `unreceipted hashes: 93359ff`; the checker treats any hash token in any non-JSON text file as a receipt (`receipt_presence_check.py:150-161`), and accepts a short token matching a prefix of the full measured hash. In contrast, at the historical round-33 revision, `c1-after-b1752a2.json` has `rev: b1752a2480aa86fc27536dd6e7d27a91b52bed12`; the `93359ff…` measurement correctly fails there (`--rev` 93359ff, round 33). The TXT-only probe is found in `round-33/verification/criterion-counter-control-r32-c2.txt:1`; the sole `a0b0dff` hit in the verification tree was that plain-text file, not a JSON `revision`.

Blind spots: exact heading/table parsing rejects prose and renamed headings (intentional under the strict format, false failures only if equivalent prose/headings are intended inputs). More serious, text matching does not establish that a text artifact is a receipt for the measurement; even a diagnostic explicitly reporting a missing receipt satisfies the check. JSON receipts do require a matching root `revision`/`rev` prefix (`:164-179`). No tools installed; no checker source or lane Git state changed.