# CtlC1NoReader-shortcut — C1 shortcut control (disclosed follow-up for dead CtlC1Shortcut)

- Tool: `/fast/scratch/hyaku/kake-r37/ctl/CtlC1NoReader/shortcut/robots_audit.py`, sha256
  `61724ead9831776ea70c72cdf6ae25221535b1b74e070665536a249bfebe6f7d` (10147 bytes, stdlib only).
- Usage, (a), (f), (g) and the verdict: the no-reader's faithful code (`4a4dfc5d…`), unchanged.
- Skipped for 2xx: all (b)–(e) matching. No group, precedence, wildcard, `$` or length code of mine.
  Lines go to `urllib.robotparser.RobotFileParser` (Python 3.14), decided by `can_fetch`.
- Guess from public receipts: `control-CtlC1NaiveReader.json` (same stdlib parser) passes a, c, d, f, g
  and fails only b and e; the ablation names say what b and e test. So I keep the stdlib and patch it:
  S1 only the first 512000 bytes [(b) limit]; S2 drop a leading BOM, stdlib keeps it in the key [(b) BOM];
  S3 split at CR, LF, CRLF only [(b) line ends]; S4 drop lines whose key is not user-agent, allow or
  disallow, since stdlib's `crawl-delay` ends a group [(b) other keys];
  S5 pass `path[?query]`, no fragment, `?` only for a non-empty query [(e) path];
  S6 rewrite `%XX` of a reserved ASCII character as `%25XX` in URL and rules, so stdlib's unquote/quote
  keeps `%2F` apart from `/` [(e) reserved escapes, by a hack].
- Not used: URL words, user-agent names, ids, file names, order, `expect` (their bullets pass already).
- Honest class: "stdlib + 6 one-line patches"; S1–S6 copy contract rules where the stdlib differs. Not
  covered: substring user-agent match, mid-rule `$`, wildcard/`$` length counting.

## Commands (exit codes)
1. Per-case summary of `verification/control-*.json` and `ablations/*.json` → 0. Read-only `git log`
   and `git ls-tree HEAD` (4b089da: reports and receipts committed) → 0.
2. `cat .ufo/waves/round-37/ctl/CtlC1NaiveReader.md` → 0 (committed report; retained tools and
   sandboxes not opened). `grep` of `/usr/lib/python3.14/urllib/robotparser.py` → 0. `mkdir`/`cp` seed → 0.
3. 18 contract-derived 2xx checks (BOM, CR, crawl-delay, orphan, limit, key case and comment, `%2F`, hex
   case, `?` + `$`, fragment + `$`, empty path, `%7e`, non-ASCII, `/robots.txt`, groups) → harness 0, tool 0
   `clean`, all as the contract says. Under the counter's bwrap argv, 5 checks → harness 0, tool 2 with the
   expected `exposed`/`blocked`/`check_invalid`. Temp dirs inside `shortcut/` were removed.

## Score
Not measured; the key was not granted. [INFERENCE] 25–28 if b and e fail the stdlib only through these
quirks. That means stdlib plus patches does the claim: cheap, but not a counter defect in itself. Whether
delegating to the stdlib counts as the claimed work is the L1's call. Installs: none.
`timeout 10s ls -la /fast/scratch/hyaku/kake-r37/ctl/CtlC1NoReader/shortcut/` (exit 0):
```text
drwxr-xr-x 2 vgpnk vgpnk    29 Oct 23 00:27 .
drwxr-xr-x 3 vgpnk vgpnk    45 Oct 23 00:26 ..
-rwxr-xr-x 1 vgpnk vgpnk 10147 Oct 23 00:27 robots_audit.py
```
Report: .ufo/waves/round-37/ctl/CtlC1NoReader-shortcut.md
