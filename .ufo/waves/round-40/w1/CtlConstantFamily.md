# CtlConstantFamily — constant/junk control family (round 40, wave 1)

No control met the predicate. Best is `manifest_only` at 17/30. All tools keep the skip (none performs the three declared repairs).

Baseline for scale: unmodified base tool `f043c721:scripts/sitemap_audit.py` scores **10/30** (E 4/9, R 3/8, U 3/13) with **selftest PASS 150/150**. The selftest therefore does not encode the C1 defects.

Command (identical for every row; exit 0 met / 1 not met / 2 cannot evaluate):
`timeout 1200 python3 -B .ufo/waves/round-40/c1_count.py --root <lane> --tool-file <tool> --label CtlConstantFamily-<name> --out receipt-<name>.json` → every run **exit 1**.

| tool (sandbox `/fast/scratch/hyaku/kake-r40w1/CtlConstantFamily/`) | sha256 | passed | byClass | selftest | met |
|---|---|---|---|---|---|
| base.py (control of control) | 6d86c8cef78e36d372f7277096ec163cc8f1e919fa66702ad24e5e32f9a240ec | 10/30 | E 4/9 R 3/8 U 3/13 | PASS 150/150 | no |
| const_findings.py | 79c9b7bb144e5cbcad58a4fa72428a9472e531bafcbbadad84bee83e575c423b | 5/30 | E 5/9 R 0/8 U 0/13 | PASS 17/150 | no |
| const_error.py | ada33d87b398b0836bf98914bd33ed374643addf6bd6086976f8b7a59f62d0c4 | 8/30 | E 0/9 R 4/8 U 4/13 | PASS 25/150 | no |
| exit_only_0.py | 3dee1cb019d7feea6ef797cdd9148d189f3f2e0fa44317c342e1d1c6a1794c31 | 0/30 | E 0/9 R 0/8 U 0/13 | PASS 6/150 | no |
| exit_only_base.py | ed79d959edfd354a99f8ceb2ba2401cec966b1b49828fd15b0d69d0534db70ff | 0/30 | E 0/9 R 0/8 U 0/13 | PASS 6/150 | no |
| flip.py | fc50c7e0fa56c4f3d4e19a67719a4d8f6ce26319431bf34bf3010b9e82cdf470 | 5/30 | E 5/9 R 0/8 U 0/13 | PASS 0/150 | no |
| manifest_only.py | 6fdf31889747f1ca1c9168802af35f947b99f3f85c74c54aeb69901dde5bc982 | 17/30 | E 2/9 R 8/8 U 7/13 | PASS 68/150 | no |
| memo_selftest.py | d4bbdb83ec2fb2d6d0c4b7b564c2511cf64b6ad8692b60f9890b18fe2b637b7f | 10/30 | E 4/9 R 3/8 U 3/13 | PASS 150/150 | no |
| verdict_only.py | e763bee87d3cc57760b19de9920b814d71eeb989aec2e53a28cf141debe423e6 | 0/30 | E 0/9 R 0/8 U 0/13 | PASS 6/150 | no |

Skipped work and the witness that caught each:
- const_findings — skips all three classes; emits `xml_malformed` on every check. Caught by E6 (`exit 1 != 0`, clean expected) and U1 (`got findings/[xml_malformed] want findings/[loc_not_absolute,1]`). Free credit: E1–E5 are themselves constant.
- const_error — skips all three; every check `check_invalid`, exit 2. Caught by R5 (`check 0: got error/check_invalid want clean/None`) and E1 (`exit 2 != 1`). Free credit: R1–R4 and U7–U10 expect uniform error output.
- exit_only_0 / exit_only_base / verdict_only — skip the entire report shape (empty or `checks: []`). Caught by R1 (`stdout not JSON` for exit_only_base; `exit 0 != 2` for the others) and every E/U witness.
- flip — base output with every status inverted. Caught by E6 and U1 (same as const_findings), selftest 0/150.
- manifest_only — never opens a referenced sitemap file; derives everything from manifest fields. Caught by E1 (`exit 0 != 1`) and U1 (`exit 0 != 1`): loc/encoding defects live only in file bytes. It does reproduce R 8/8 by manifest bookkeeping alone.
- memo_selftest — zero audit logic; 135-key table of (manifest sha256 + referenced-file sha256) → base stdout/exit. Passes the selftest 150/150, then falls back to base for anything unseen, so witnesses land on 10/30.

Findings:
- `.ufo/waves/round-40/c1_count.py:270-282` — the selftest half of the predicate is content-memorizable: 150 fixed cases collapse to 135 content keys (~33 KB). A tool that never reads a sitemap passes 150/150 (memo_selftest).
- `scripts/sitemap_audit_selftest.py:204-208` (`chk_duplicate_id`) expects `[clean, error]`, which is base's order-dependent behaviour; no selftest case distinguishes the R1 shape (`[bad, bad]`). Combined with base scoring 150/150, the selftest cannot gate C1.
- `c1_count.py:63-96` — 8 of 30 witnesses (R1–R4, U7–U10) expect a uniform constant per check, so a zero-work tool collects 8/30 (const_error). Floor, not a breach.
- `c1_count.py:99-113` — R is fully manifest-derivable: manifest_only passes R 8/8 without opening a file.

Attacked statements:
- "The counter rejects a tool that skips the declared work" — **holds** for every constant/junk variant (max 17/30, none met), but only by correctness margin: no structural rejection, and a zero-work constant already banks 8/30.
- "The round-39 selftest (150/150) evidences C1 correctness" — **overstated**: base, which fails 20/30 witnesses, passes 150/150, and a lookup table passes it with no audit logic.
- "The witness set cannot be memorized" — **holds** for the 30 witnesses (hosts/ids/files random per seed); the selftest, being fixed content, can be.

No tooling installed. No lane files touched; all writes confined to the sandbox and this report.
