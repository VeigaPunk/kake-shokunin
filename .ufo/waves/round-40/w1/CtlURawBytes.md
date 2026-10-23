# CtlURawBytes — U proxy control (raw-bytes regex) scores 30/30

**CONTROL MET THE PREDICATE.** `passed 30/30`, `selftest PASS 150/150`, `met: true`, repeated on 5 independent draws. It does not do the declared U repair (it never judges the parsed `loc` value and never inspects `sitemapUrl` beyond a regex over the raw bytes/string). Under the frozen kill rule, C1 is exploratory.

## Built
- `ctl.py` sha256 `8dcc2f718d9ea7b1a6d529da5cc0f61fab29e2892a626f4ef094000733852946`
  - start from `/fast/scratch/hyaku/kake-r40/shared/ref_fix.py`; **delete** the `_parse_url` control guard (`ref_fix.diff` hunk 1, `if value[:1] <= " " or "\t" in value ...`) so no parsed value is ever scanned for TAB/CR/LF;
  - U detection is only `_RAW_LOC_TEXT_RE` over the file bytes (`ctl.py:176-206`) plus `_RAW_URL_CTRL_RE` over the raw `sitemapUrl` string (`ctl.py:204-206`, applied `ctl.py:397`);
  - E and R paths byte-identical to the reference (NUL→`xml_malformed`, duplicate-id ordering).
- `ctl_noraw.py` sha256 `ed579d17015c74237ab6dfe34f4b599fe8f78eddacb659bf3bc5fd902d146caa` = reference minus only those 2 guard lines (ablation, no prefilter).
- `base.py` sha256 `6d86c8cef78e36d372f7277096ec163cc8f1e919fa66702ad24e5e32f9a240ec` = `git show f043c72146ddb7e3bb1c64d26fd5ae2b01b508f8:scripts/sitemap_audit.py`.
- All under `/fast/scratch/hyaku/kake-r40w1/CtlURawBytes/`. No installs; no lane writes except this report.

## Commands (all exit codes shown)
`timeout 1200 prlimit --as=4000000000 python3 -B kake-shokunin/.ufo/waves/round-40/c1_count.py --root kake-shokunin --tool-file <t> --label <l> [--seed N] --out receipt*.json`
- `ctl.py --seed 4001` → exit 0
- `ctl.py --seed 98765` → exit 0
- `ctl.py` unseeded ×3 (labels `-rand1..3`) → exit 0, exit 0, exit 0
- `ctl_noraw.py --seed 4001` → exit 1
- `base.py --seed 4001` → exit 1

## Counter results (passed / byClass / selftest / met)
| tool | passed | E | R | U | selftest | met |
|---|---|---|---|---|---|---|
| ctl.py (seed 4001) | 30/30 | 9/9 | 8/8 | 13/13 | PASS 150/150 | **true** |
| ctl.py (seed 98765) | 30/30 | 9/9 | 8/8 | 13/13 | PASS 150/150 | **true** |
| ctl.py (rand1-3) | 30/30 ×3 | 9/9 | 8/8 | 13/13 | PASS 150/150 | **true** |
| ctl_noraw.py (seed 4001) | 20/30 | 9/9 | 8/8 | **3/13** | PASS 150/150 | false |
| base.py (seed 4001) | 10/30 | 4/9 | 3/8 | 3/13 | PASS 150/150 | false |

Receipts: `receipt.json`, `receipt-s2.json`, `receipt-rand{1,2,3}.json`, `receipt-noraw.json`, `receipt-base.json` (counter sha256 `6d73b8f4…bee8d8`).

## Declared work skipped, and the witnesses that would have to catch it
- `ctl.py` skips "judge the parsed `loc` value and reject TAB/CR/LF there" and "check `sitemapUrl` as a parsed value": it only regexes raw bytes. **No witness caught it** — U1-U13 all pass because the raw `<loc>` body still contains the byte (or `&#13;`), and the manifest string still contains the raw character. Selftest case only pins `loc_xml_whitespace_stripped` (edge whitespace), which the prefilter emulates.
- Ablation proves the U work really is the prefilter's: remove the guard from the reference and U collapses 13/13 → 3/13; the control's prefilter restores 13/13. So the counter measures *observable class-U output*, not the declared repair.
- E and R witnesses do have power: base scores E 4/9, R 3/8; the control carries the reference's NUL check and duplicate-id ordering and scores 9/9, 8/8.

## The control is semantically wrong in both directions (counter blind to both)
Fixtures in `fx1/`, `fx2/`, `python3 -B <tool> --manifest manifest.json`:
- `fx1`: comment decoy puts a second raw `<loc>` in the file, so `_raw_loc_map` sees a count mismatch and disables detection (`ctl.py:271-272`) → **under-detects**: control says `clean`/exit 0, reference says `loc_not_absolute` entry 1/exit 1.
- `fx2`: TAB inside an XML comment inside the `<loc>` body → **over-detects** (`ctl.py:197-200`): control says `loc_not_absolute`/exit 1, reference says `clean`/exit 0.

## Judgements on the round's declaration
- "C1 repairs … U … by judging the parsed value" — **overstated by the frozen counter**: it never distinguishes parsed-value judgement from a raw-bytes proxy; a proxy that is provably wrong on both fx1 and fx2 still scores 30/30.
- "Predicate met ⇒ C1's declared repair landed" — **wrong**: a tool with the repair deleted meets it.
- The kill-rule premise "a CONTROL meeting the predicate makes C1 exploratory" — **fires**: control meets on every draw, before any build lands.
- E (`xml_malformed` on UTF-16 without BOM) and R (repeat of an earlier invalid check's id) claims: **hold** as observable-class statements; both witnesses discriminate against `base.py`.
- Counter integrity: selftest pin `99ee9bbf…51db` matched, `--seed` honoured, receipts written. No counter defect found.

## Risks / blockers
- None for this seat. Scope held to the raw-bytes hypothesis; other U-skipping variants (`CtlSkipU.md`, `CtlELittleEndianOnly.md` in this directory) are other seats' evidence, not mine.
