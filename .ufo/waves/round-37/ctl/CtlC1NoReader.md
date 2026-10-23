# CtlC1NoReader — round-37 C1 pre-freeze control (no-reader)

## Control and what it skips
- Tool: `/fast/scratch/hyaku/kake-r37/ctl/CtlC1NoReader/robots_audit.py`, sha256
  `4a4dfc5dbad775c74c322d40b94ae840a82dafb52e138e1601042bc9479773e3` (9589 bytes, stdlib only).
- Skips all robots-file work: never opens or reads a robots file; contract bullets (b) lines/limit/BOM/
  comments, (c) groups, (d) rule matching, (e) path normalization are absent.
- Implements exactly: usage (argv must be exactly `--manifest PATH`, else exit 64); (a) 400–499 allow,
  500–599 disallow (also `/robots.txt`); (f) every check fault: non-object, id missing/empty/non-string/
  repeated (an earlier invalid check's id still counts), `robotsStatus` not a JSON integer in the three
  ranges (bool/float rejected), `userAgent` not `[A-Za-z_-]+`, `expect` not `allow`/`disallow`, URL not
  http(s) with host (`urlsplit`, scheme lowercased, `hostname` non-empty), and for 2xx a robots path
  that is missing, non-string, absolute, escapes the manifest directory after `resolve()` or is not a
  regular file (`os.stat` metadata only); (g) manifest not a regular file, > 64 MiB, unreadable, not
  UTF-8, not JSON (`NaN`/`Infinity` and a BOM rejected), non-object, `version` not the integer 1,
  `checks` not a list; verdict/exit precedence `could-not-evaluate` 2 > `failed-policy` 1 > `clean` 0.
- 2xx heuristic (documented in the tool docstring): every 2xx file is treated as empty, so every URL
  is `allow` (the `/robots.txt` rule is then automatically met). No URL shape (depth, query, escapes,
  non-ASCII, trailing slash) predicts a decision without bytes, and a case passes only when every check
  is right. Rejected: URL-word keying (that is the separate shortcut control), reading `expect`
  (becomes a constant-clean/all-false hybrid), constant disallow (no contract basis).

## Commands run (exit codes)
1. `timeout 30s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -B -c '<harness 1>'` → 0,
   `SELFTEST_OK` on the first version (`e45b839b…636e`): 5 usage forms exit 64, 9 (g) shapes, 7 (a)
   checks, a 16-entry (f) manifest. Temp dir in `/tmp` (removed on exit), outside my write paths.
2. Edits: URL check aligned to `urlsplit`+`hostname` (no extra space/port rejection), `NaN` rejector.
3. `timeout 120s env -u GIT_DIR … python3 -B -c '<harness 2>'` → 0, `JAIL_SELFTEST 13/13 USAGE_OK`:
   final tool run under the counter's exact bwrap argv, fresh ids and fresh flat file names, judged on
   exit, verdict and (check, reason) multiset: access case, 19-entry fault case, 10 raw (g) manifests,
   empty clean manifest. Temp dir created inside my sandbox and removed.
4. `timeout 10s sha256sum …/robots_audit.py` → 0; `ls -la …/CtlC1NoReader/` → 0; `pgrep -fa` → 1 (none).
5. Read-only: per-case summary of public receipts `verification/ablations/*.json` (12 files) → 0;
   `git ls-tree --name-only 202d625a -- .ufo/waves/round-37/…` → 0 (81 tracked paths, receipts public).

## Score
Not measured: the key was not granted; the L1 scores via `sealed_count.py --tool-file`.
[INFERENCE] Ceiling well below 25: public receipt `ablation-c_star` fails c1–e4, so those 12 cases hold
a 2xx check that a `*` group decides, very likely `disallow`; constant-allow fails them, and b1–b4
(BOM/CR/key-case only show through an applied rule) likely too. Reachable at most a, f, g (12).

## Counterexample, axes, smallest correction
- Exercised (harness 1, `c_200_allow`): status 200, robots `User-agent: *` / `Disallow: /private`, URL
  `https://example.com/private/doc`, expect `allow`. Contract: `blocked`, exit 1. Control: no finding.
- Axis: operability (C1 capability); missing rule work, not a tradeoff. Installs: none (stdlib, bwrap).
- If this control meets 25, the counter is wrong: at least 4 cases need a file-decided `disallow`
  on a 2xx check not masked by a fault. No tool change is proposed (that would defeat the control).

## Sandbox listing (key never held)
`timeout 10s ls -la /fast/scratch/hyaku/kake-r37/ctl/CtlC1NoReader/` (exit 0):
```text
total 12
drwxr-xr-x  2 vgpnk vgpnk   29 Oct 23 00:19 .
drwxr-xr-x 10 vgpnk vgpnk  178 Oct 23 00:10 ..
-rwxr-xr-x  1 vgpnk vgpnk 9589 Oct 23 00:19 robots_audit.py
```
Never listed or read `/fast/scratch/hyaku/kake-r37/private/` or other seats' sandboxes; no git/jj writes.

Report: .ufo/waves/round-37/ctl/CtlC1NoReader.md
