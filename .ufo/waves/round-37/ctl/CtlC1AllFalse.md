# C1 Control Receipt — `CtlC1AllFalse`

- **Control name:** `CtlC1AllFalse` (C1 all-false control)
- **What it skips:** Skips all `robotsStatus` policy evaluation (rule (a)) and all `robots.txt` reading, line parsing, group matching, rule precedence, and URL path normalization (rules (b)–(e)). Implements CLI usage (exit `64`), manifest-fault rule (g) (`input_invalid`), check-fault rule (f) (`check_invalid`, including `os.stat`/`realpath` confinement and regular-file validation without opening `robots` files), verdict aggregation, and exit codes (`0`/`1`/`2`/`64`), then emits the opposite finding for every valid check (`blocked` when `expect` is `"allow"`, `exposed` when `expect` is `"disallow"`).
- **Tooling installs / updates:** None.

## Deliverables

| File | Bytes | SHA-256 |
|---|---:|---|
| `/fast/scratch/hyaku/kake-r37/ctl/CtlC1AllFalse/robots_audit.py` | 7215 | `7bb59c7aeb988356de935f0837b05e0b72d27bf29c9e6a626987c56ca796825a` |
| `/fast/scratch/hyaku/kake-r37/ctl/CtlC1AllFalse/selftest.py` | 9705 | `c225462f8829f68bbf08c3b9147e6d55ac84874651c0b5ec0160c38b6e3d3ec4` |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-37/ctl/CtlC1AllFalse.md` | report | (this file) |

## Commands Run & Exit Codes

1. `timeout 60 python3 -B /fast/scratch/hyaku/kake-r37/ctl/CtlC1AllFalse/selftest.py` → `exit 0` (`selftest: all assertions passed`)
2. `sha256sum /fast/scratch/hyaku/kake-r37/ctl/CtlC1AllFalse/robots_audit.py /fast/scratch/hyaku/kake-r37/ctl/CtlC1AllFalse/selftest.py` → `exit 0`
3. `ls -la /fast/scratch/hyaku/kake-r37/ctl/CtlC1AllFalse` → `exit 0`
4. Bubblewrap (`bwrap`) jail smoke test invoking `/usr/bin/python3 -B <tool> --manifest <manifest>` with two valid checks (`expect: "allow"` and `expect: "disallow"`) → `exit 1` (`verdict: "failed-policy"`, `findings: [{"check": "c1", "reason": "blocked"}, {"check": "c2", "reason": "exposed"}]`)

## Score & Critic Assessment

- **Score:** Scored by L1 on the sealed key (this seat never read `/fast/scratch/hyaku/kake-r37/private/`). Expected score under the declared C1 structure ("every case has at least one check that holds and one that does not"): at most `4 / 28` (only `(g)` cases if their runs contain solely manifest-level `input_invalid` faults; `0 / 24` on `(a)`–`(f)` because every holding check gets a spurious `blocked`/`exposed` finding), well below `passed >= 25 of 28`.
- **Counterexample / Evidence:** Any valid check whose expectation holds in `robots_audit.py` is reported as `blocked` (`expect: "allow"`) or `exposed` (`expect: "disallow"`), even when `robots.txt` is `chmod 000` (unreadable) because the file is never opened (`selftest.py` case 4).
- **Impacted axes:** `operability` (C1 capability).
- **Smallest safe correction:** None required unless this control scores `>= 25 / 28` under `sealed_count.py`; if any `(g)` or `(f)` case passes without evaluating a holding check, ensure every case requires at least one valid holding check to produce zero policy findings.

## Sandbox Directory Listing (`ls -la /fast/scratch/hyaku/kake-r37/ctl/CtlC1AllFalse`)

```text
total 20
drwxr-xr-x 2 vgpnk vgpnk   48 Oct 23 00:08 .
drwxr-xr-x 9 vgpnk vgpnk  157 Oct 23 00:07 ..
-rwxr-xr-x 1 vgpnk vgpnk 7215 Oct 23 00:07 robots_audit.py
-rwxr-xr-x 1 vgpnk vgpnk 9705 Oct 23 00:08 selftest.py
```
