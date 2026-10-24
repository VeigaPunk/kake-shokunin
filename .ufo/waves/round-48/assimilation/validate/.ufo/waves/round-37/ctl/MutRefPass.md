# MutRefPass — single-point reference controls
Axes: contract deviation / counter sensitivity / exact restoration. Each control skips one C1 rule; no ABL flags; no installs, key copied/read by this probe: no (counter alone reads it).
Expected detector: frozen `passed >= 25 of 28`; met **28/42**; killed 14, survived 28, inconclusive 0. Pristine scores [28]/28; restored [28]/28; exact exits in evidence.
Before = restored = private source after: sha256 `2c294e495ef9a36c6d74472e4128f432a7bf81cbccc7998136866a877988c05d` (all 42 trials restored exactly; delivered mutants intentionally retained).
Every deliverable absolute path + sha256: `/fast/scratch/hyaku/kake-r37/ctl/MutRefPass/evidence/SHA256SUMS`; manifest sha256 `22ec8bebaba52ea383e31ff3df6172f54265c77e6c2fa3f1e575adab0f9494f1`. Summary, 126 raw stdouts, stderr, exact argv/exit codes and listing are included; report hash is in the handoff.
Exact commands/exits: `/fast/scratch/hyaku/kake-r37/ctl/MutRefPass/evidence/commands.jsonl`; runner `timeout --kill-after=5s 850s python3 -B /fast/scratch/hyaku/kake-r37/ctl/MutRefPass/evidence/run_probe.py` exit 0 after one locator-count failure (exit 1, retained); completed trials were not rerun. Root listing below; no sealed key copied here; temporary fixtures removed.
Mutation scores use `timeout 300 python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-37/sealed_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file <mutants/Mxx.py> --key-file /fast/scratch/hyaku/kake-r37/private/cases.json` with TMPDIR=/fast/scratch/hyaku/kake-r37/ctl/MutRefPass/evidence/tmp; pristine/restored use the same detector on trials/Mxx.py.
Equivalence column: N = [INFERENCE] non-equivalent under the public contract, with reason; not a claim about an undisclosed case. Killed means predicate false, not merely fewer than 28.
| id | contract sentence broken | one-line diff | passed/28 | met | equivalent if met / why |
|---|---|---|---:|:---:|---|
| M01 | b: exactly 512000 bytes | `LIMIT: 512000 -> 511999` | 28/28 | yes | N: the last permitted byte is dropped |
| M02 | b: exactly 512000 bytes | `LIMIT: 512000 -> 512001` | 28/28 | yes | N: a forbidden extra byte can change a rule |
| M03 | b: key trims only SP/TAB | `key.strip(SP/TAB) -> key.strip()` | 28/28 | yes | N: Unicode whitespace can turn an ignored key into a record |
| M04 | b: value trims only SP/TAB | `value.strip(SP/TAB) -> value.strip()` | 28/28 | yes | N: Unicode whitespace in a literal rule or agent is lost |
| M05 | b: first # starts comment | `find(#) -> rfind(#)` | 28/28 | yes | N: text between comment markers is wrongly retained |
| M06 | b: only CR/LF/CRLF split lines | `CR/LF regex -> splitlines()` | 28/28 | yes | N: Unicode separators wrongly start new records |
| M07 | b: split at first colon | `split(:,1) -> rsplit(:,1)` | 28/28 | yes | N: a colon inside a value changes the parsed key |
| M08 | b: ASCII key case comparison | `key.lower() -> key.casefold()` | 28/28 | yes | N: Unicode folding can convert a non-ASCII key to a record |
| M09 | c: ASCII agent comparison | `group-name lower() -> casefold()` | 28/28 | yes | N: Unicode group names can spuriously equal an ASCII product |
| M10 | c: exact group-name equality | `agent equality -> substring` | 28/28 | yes | N: a longer different group name can match |
| M11 | c: wildcard only without exact match | `if not matched -> if matched` | 0/28 | no | — |
| M12 | c: combine every matching group | `rules.extend(group) -> rules = group` | 24/28 | no | — |
| M13 | c: agent after rule starts group | `after rule: last_ua False -> True` | 24/28 | no | — |
| M14 | c: consecutive agents share group | `after agent: last_ua True -> False` | 24/28 | no | — |
| M15 | d: star also matches empty | `wildcard .* -> .+` | 28/28 | yes | N: a zero-length wildcard expansion no longer matches |
| M16 | d: only terminal $ anchors | `endswith($) -> startswith($)` | 20/28 | no | — |
| M17 | d: unanchored match is prefix | `re.match -> re.fullmatch` | 2/28 | no | — |
| M18 | d: prefix begins at first character | `re.match -> re.search` | 28/28 | yes | N: a rule can wrongly match in the middle of a path |
| M19 | d: normalized octet length wins | `len(normalized) -> len(raw)` | 28/28 | yes | N: raw Unicode or escaped lengths can select another rule |
| M20 | d: allow wins equal-length ties | `longest comparison > -> >=` | 26/28 | yes | N: a later equal-length disallow overrides allow |
| M21 | d: allow wins equal-length ties | `tie kind allow -> disallow` | 24/28 | no | — |
| M22 | e: reserved escapes stay encoded | `decode unreserved -> also decode %2F` | 24/28 | no | — |
| M23 | e: kept escapes use uppercase hex | `escape hex upper() -> lower()` | 24/28 | no | — |
| M24 | e: UTF-8 escapes use uppercase hex | `UTF-8 octet format %02X -> %02x` | 24/28 | no | — |
| M25 | e: empty URL path becomes / | `empty-path default / -> empty` | 24/28 | no | — |
| M26 | e: non-empty query is included | `append ?query -> append empty` | 20/28 | no | — |
| M27 | e: fragment is never included | `path -> path plus fragment` | 24/28 | no | — |
| M28 | e: /robots.txt exemption is exact | `robots path comparison -> case-insensitive` | 28/28 | yes | N: differently cased paths wrongly bypass their rules |
| M29 | g: version is integer 1, not True | `exact int type -> isinstance(int)` | 27/28 | yes | N: JSON true is wrongly accepted as manifest version |
| M30 | manifest: entire agent is product token | `UA fullmatch -> match` | 25/28 | yes | N: a valid prefix hides an invalid trailing character |
| M31 | manifest: agent alphabet excludes digits | `UA alphabet -> add 0-9` | 28/28 | yes | N: digit-containing agents are wrongly accepted |
| M32 | manifest: reject status 300 | `3xx lower bound 300 -> 301` | 28/28 | yes | N: status 300 becomes valid and evaluated |
| M33 | manifest: reject status 399 | `3xx upper bound 399 -> 398` | 27/28 | yes | N: status 399 becomes valid and evaluated |
| M34 | manifest: floats are not status integers | `status int-only -> int or float` | 28/28 | yes | N: in-range floating statuses are wrongly accepted |
| M35 | manifest: status 200 is valid | `status lower bound 200 -> 201` | 0/28 | no | — |
| M36 | manifest: status 599 is valid | `status upper bound 599 -> 598` | 27/28 | yes | N: an allowed 599 status becomes check_invalid |
| M37 | manifest: resolve symlinks for containment | `realpath(file) -> abspath(file)` | 28/28 | yes | N: a symlink can refer outside the manifest directory |
| M38 | manifest: file stays inside directory | `containment prefix drops separator` | 28/28 | yes | N: a sibling directory sharing the base prefix passes |
| M39 | g: only sizes greater than 64 MiB fail | `manifest max 64 MiB -> 64 MiB minus 1` | 28/28 | yes | N: an otherwise valid exactly-64-MiB manifest is rejected |
| M40 | g: non-UTF-8 manifest is invalid | `manifest UTF-8 strict -> replacement` | 28/28 | yes | N: invalid UTF-8 inside a JSON string can be accepted |
| M41 | f: checksEvaluated counts valid checks | `evaluated increment 1 -> 2` | 28/28 | yes | N: every nonempty valid set has a doubled count; counter explicitly ignores it |
| M42 | usage: stdout report version is 1 | `output report version 1 -> 2` | 28/28 | yes | N: the required output version is wrong; counter does not compare it |
```text
total 4
drwxr-xr-x  4 vgpnk vgpnk   37 Oct 23 00:06 .
drwxr-xr-x 10 vgpnk vgpnk  178 Oct 23 00:10 ..
drwxr-xr-x  5 vgpnk vgpnk  146 Oct 23 00:12 evidence
drwxr-xr-x  2 vgpnk vgpnk 4096 Oct 23 00:12 mutants
```
