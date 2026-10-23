KILLED: counter v4 kills 5 of 6 single-member port-parsing mutants; SURVIVED: m6_default (default-port branch), witness below, ref41-verified.

# MutBuildPort — round 43 wave 1, build port parsing (r42 build 020bc45)

Base: `git -C kake-shokunin show 020bc4574729ed674299f6cab02faac1582d9464:scripts/sitemap_audit.py`
-> `/fast/scratch/hyaku/kake-r43/MutBuildPort/build.py`, sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` (matches dispatch), 657 lines.
Ref41 extracted read-only for the survivor witness: `ref41.py` sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` (counter's REF41_SHA).
Counter v4 sha256 verified `1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab`.

Command (one per mutant, no --seed, receipts in /fast/scratch/hyaku/kake-r43/MutBuildPort/<id>.json):
`timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-43/c43_count_v4.py --root <lane> --tool-file <mutant> --label MutBuildPort-<id> --out <id>.json`, exit 0 met / 1 not met. Wall 21–39 s.

| mutant | file / sha256 | one-member change (build.py:line) | equalRuns | met | seed | runs differing | verdict |
|---|---|---|---|---|---|---|---|
| m1_digit9 | m1_digit9.py `591820e5…485b` | port digit class upper `0x39`->`0x38` (:198) | 5/11 | false | 162030007837488 | A,B,D,E,F,T3 | KILLED |
| m2_digit0 | m2_digit0.py `083428d4…4f39` | port digit class lower `0x30`->`0x31` (:198) | 5/11 | false | 164457956355773 | A,B,D,E,F,T3 | KILLED |
| m3_colon | m3_colon.py `97bb6313…c73f` | branch `raw[at] == 0x3A` -> `!=` (:196) | 5/11 | false | 69141144905091 | A,B,D,E,F,T3 | KILLED |
| m4_boundary | m4_boundary.py `51399983…985f` | loop bound `at < size` -> `at < size - 1` (:198) | 8/11 | false | 10528708900732 | A,B,D | KILLED |
| m5_range | m5_range.py `16e700d4…2581` | `except ValueError: return None` -> `port = 0` (:301-302) | 3/11 | false | 146840433112812 | B,D,E,F,T1,T2,T3,T5 | KILLED |
| m6_default | m6_default.py `68f37500…87e` | branch `if port is None:` -> `if port is not None:` (:303) | 11/11 | true | 102451791411530 | none | SURVIVED |

Each diff is exactly one hunk (`diff -u build.py m*.py`). m6 passed the whole predicate, ratios T1 1.062 T2 1.166 T3 1.330 T4 1.216 T5 1.055.

## Survivor witness (m6_default), against the round-41 tool
Fixture `/fast/scratch/hyaku/kake-r43/MutBuildPort/fix/` (8 one-entry urlset files + one manifest; sitemapUrl `http://example.com/sitemap.xml`):
- loc `http://example.com:80/a`: ref41 check status `clean`, findings `[]`; m6 `findings: loc_out_of_scope entry 1`.
- loc `http://example.com:00080/a` (leading-zero form, same port value): ref41 `clean`; m6 `loc_out_of_scope`.
build.py == ref41 on this fixture (whole document equal, exit 1 both); m6 != ref41 on exactly c2 and c6.
Cause: the mutation overwrites explicit ports with 80/443 and leaves implicit ports as `None`; `parsed[:3]` then compares `(http, host, 80)` vs `(http, host, None)`. No counter run pairs an explicit default-port loc with an implicit-port sitemapUrl (derived sitemapUrls copy the authority string, random ones use another host), so 11/11 equality cannot see it. Coverage finding, not a claim that the r42 build differs from ref41.

## Findings per checked statement
- Dispatch "build sha 914ebdee…" — holds (re-checked after all scoring: `914ebdee…cd021`).
- "counter v4 sha 1c3b9661…" — holds.
- "6+-digit port class kills a 5-digit reader": freeze receipt `verification/freeze/r42ctl-M8-port-five-digits.json` 9/11 not met — holds (freeze evidence; I did not rerun that control).
- "port parsing incl. 5-digit boundary and 65535/65536/100000 edges is handled in the tool" — overstated as a code region: the tool has no digit-count bound and no range check; both live in `urlsplit` (`parts.port`, build.py:300). The only tool-side range lever is the `except ValueError` body, probed by m5 (killed 8/11). A "reads at most five digits" defect is not expressible as a single-member change here without bypassing `parts.port`.
- "F exercises the port loop" — holds for accept/reject flips (m1/m2/m3/m4/m5 all die partly or wholly on F/T3), not for default-port explicitness (m6).
- m4 is killed only by A,B,D; its defect (port at the very end of a value) is not produced by the F/T shapes (those always follow a port with `/`).

## Bounds / restoration
Only writes: /fast/scratch/hyaku/kake-r43/MutBuildPort/ (304 KB) and this file. build.py never edited (mutants are copies; pristine hash above both before and after). No lane mutation, no jj, no git writes; `git show` reads only. No processes left running; no tool installs.
