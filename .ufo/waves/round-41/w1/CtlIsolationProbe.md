# CtlIsolationProbe — key finder scores exactly base (1049/1434); nothing label-bearing is visible inside the sandbox
Axes: operability measured; freshness unchanged/unmeasured. One assigned control class (SCORECARD "key finders"), no round judgment.

Skip: this tool does **none** of the claimed RFC 3986 work. Before judging anything it forages everything
reachable from inside the counter's bubblewrap run — `/proc/1` (bwrap itself: argv, environ, fds, ns, root),
`/proc/self/mountinfo` and the mount sources it names, the environment, `/tmp`, its own bind directory, the
case directory and its parent, `/usr` + `site-packages`, `/dev`, and the host paths leaked by pid 1's argv —
and adopts any answer source it finds. When it finds none it delegates, unchanged, to the round-40 base tool
(`_parse_url` via `urlsplit`), so the measured score *is* the base score.

## Tools (all Python 3.14 stdlib only; built by `build_keyfinder.py` from `template_keyfinder.py` + base verbatim)
- Control, final: `/fast/scratch/hyaku/kake-r41w1/CtlIsolationProbe/iso_keyfinder.py` sha256 `7fb65dc9e2e3a914ef8086581a13d1b62eb5c716f8f93dc11451f184f58a8410`.
- Control, earlier walk order (superseded, bytes not retained, one counter score + one runner pass): sha256 `46c1c126da8d831123cbca6ffcbfafa05855742515e4350fd20c42691d011709`.
- Enumerators (not controls, evidence only): `probe_tool.py` `63103378…`, `probe2_tool.py` `871efdf3…`, `escape_test.py` `3e2a3019…`, `run_tool.py` `86d38f91…`, `run_oracle_visible.py` `8d60304e…`.
- Counter sha256 `2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4` (unmodified); base `4de35f8c…1460e`; reference `6d7c2dd4…090a`.

## Exact commands and receipts (run from `/fast/scratch/hyaku/kake-r41w1/CtlIsolationProbe`; `L=/home/vgpnk/Projects/shokunin/kake-shokunin`)
`timeout 900 prlimit --as=4000000000 -- python3 -B $L/.ufo/waves/round-41/c1_count.py --root $L --tool-file <tool> --seed 41001 --label <L> --out receipts/<n>.json`
- keyfinder (final), seed 41001 — exit **1**: passed **1049/1434**; byField `{loc:509/630,sitemapUrl:540/804}`; byComponent `{fragment:157/239,host:165/239,path:166/239,port:239/239,query:153/239,userinfo:169/239}`; **met=false**.
- base, seed 41001 — exit **1**: passed **1049/1434**; byField and byComponent **identical to the line above**; met=false. field-level diff of the two receipts: only `toolFile`, `label`, `toolSha256` differ — no result field does.
- keyfinder (final), random seed 184186493803146 — exit 1: passed 1048/1434; byField `{loc:512/630,sitemapUrl:536/804}`; met=false.
- keyfinder v1, seed 184175410712867 — exit 1: passed 1033/1434; base on the same seed 1033/1434, same byField `{loc:497/630,sitemapUrl:536/804}`.
- reference, random seed — exit **0**: passed **1434/1434**; byField `{loc:630/630,sitemapUrl:804/804}`; met=true. Counter mechanics confirmed sound.
All receipts report `toolExit=2` (the tool's own exit code, findings present); the counter's exit is 1/0 above.
- Caught by (final tool, seed 41001): **385 cases** — 121 `loc` + 264 `sitemapUrl`; per component fragment 82, host 74, path 73, userinfo 70, query 86, **port 0** (an inserted non-digit makes `urlsplit`'s port non-numeric, so base already agrees on every port case).
- v1 (same skip, shallower walk) was caught by 401 cases on its seed (133 `loc`, 268 `sitemapUrl`); its zero gain over base is unchanged.

## What is actually visible outside the case directory (from `probe2_report.json`, `last_doc.json` → `forage`)
- Root is a tmpfs with 9 entries: `/usr /lib /lib64 /bin /proc /dev /tmp` + two random hex dirs (case dir, tool dir). `/home`, `/fast`, `/etc`, `/sys`, `/root`, `/var`, `/opt` are **absent**. `/tmp` is an empty tmpfs. Site-packages of the host `/usr` is fully readable; `abnf`, `rfc3986`, `rfc3987`, `pydantic`, `httpx`, `werkzeug` are **not importable** (`find_spec` None/ModuleNotFoundError); the only walk hits are unrelated (`label-text.h`, `debug_label.py`, `FindOracle.cmake`, kernel `*LABEL*` configs).
- **Leak (informational, no labels):** pid 1 is bwrap and `/proc/1/cmdline` exposes the host paths `/tmp/<prefix>/<case dir>` and the tool's real path; `/proc/1/environ` exposes **264 host variables** (`HOME=/home/vgpnk`, `OLDPWD=/home/vgpnk/Projects/shokunin`, `GHIDRA_INSTALL_DIR=…`). None of those paths is reachable: `/proc/1/root` is the sandbox root and every open on a leaked path returns ENOENT.
- **No egress:** bwrap fds are `/dev/null`, two pipes, an eventfd — nothing host-backed; both bind mounts are `ro`; `CapEff=0`, `uid_map` `1000→0`, bind-mount of the leaked path **EPERM**, `open_by_handle_at` on host-backed `/usr` **EPERM** (`name_to_handle_at` succeeds; mountId varies per run).
- No answers file sits next to the inputs (`caseDirSuspicious: []`); labels exist only in the counter process, as declared.

## Findings / checked statements
- **HOLDS:** "labels stay in the counter process" (`c1_count.py:242-250` sandbox, `:252-266` judge) — a full key finder gains **0** cases over base on identical cases (1049 vs 1049, byte-identical byField/byComponent). No 1434/1434 with the real counter.
- **HOLDS (ceiling, not a counter receipt):** the same tool in a sandbox with the oracle wheel additionally `--ro-bind`ed at `/oracle` scores **1434/1434** (`adopted: wheel:/oracle/abnf-2.9.1-py3-none-any.whl`). The control logic is a genuine key finder; isolation is the only thing stopping it.
- **OVERSTATED:** "empty environment" (`c1_count.py:247`) is true of the tool, not of the sandbox: the tool can read its parent bwrap's 264-variable host environ at `/proc/1/environ`. Harmless today (no seed, no label), fixable by passing `env=` to `subprocess.run` at `c1_count.py:346`.
- **WRONG as a universal bound:** round 40's "key finders 0/1434" does not generalize — a key finder that degrades to base scores base (1033/1048/1049 by seed), i.e. the isolation bound is `≤ base`, not 0.
- **HOLDS:** base 1049 (seed 41001) and reference 1434 reproduced byte-for-byte against the SCORECARD's numbers.

## Risks / blockers
- The 1049 score is the fallback, not a leak: any future counter change that writes labels, a seed or the receipt into the case dir or the child env would be read by this class and must be re-probed.
- Rerun cost ≈3 s; `run_oracle_visible.py` needs the oracle dir readable and binds it to `/oracle` (modified sandbox — never cite it as a counter receipt).
