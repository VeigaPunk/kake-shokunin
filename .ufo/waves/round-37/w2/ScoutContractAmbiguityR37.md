# Scout: C1 contract ambiguity — KakeR37 wave 2 (falsify)

Seat: ScoutContractAmbiguityR37. Probed undecided/doubly decided points of the round-37 C1
contract by running the three implementations side by side: `scripts/robots_audit.py`
(tool, `9dbc88bb`), `sealed/reference/ref.py` (ref), `retained/independent/independent_robots_audit.py`
(independent). All runs: `python3 -B <impl> --manifest <path>`. Harness:
`/fast/scratch/hyaku/kake-r37w2/ScoutContractAmbiguityR37/tmp/driver.py` (+ `extras/`); inputs in
`tmp/cases/T*`, `tmp/extras/e*`. No tools installed (none needed).

## Splits found (implementations disagree on contract text)

1. **(f)/(g) symlinked manifest path: which directory is "the manifest's directory"?**
   Input (`tmp/cases/t1`): `link/manifest.json` is a symlink to `target/manifest.json`;
   `link/robots.txt` = `user-agent: *\nallow: /\n`; `target/robots.txt` =
   `user-agent: *\ndisallow: /x\n`; check: status 200, robots `robots.txt`, URL
   `http://example.com/x`, expect `disallow`.
   - tool: exit 0 `clean` (resolved target dir → disallow → pass)
   - independent: exit 0 `clean` (same)
   - ref: exit 1 `failed-policy` [`exposed`] (link dir → allow → exposed)
   Contract (f): robots path must be "inside the manifest's directory (after resolving symlinks
   and `..`)" — the parenthetical reads as governing the robots path, but "the manifest's
   directory" itself is undecided when the manifest path is a symlink. Tool+independent resolve
   the manifest first (`realpath` then dirname); ref does not (`dirname` then realpath).
   **Undecided; split 2:1.** Sealed cases exercise no symlinked manifest (scan of `cases.json`).

2. **(e) implicit `/robots.txt` allowance: before or after normalization?**
   Input (`tmp/cases/t2`): robots = `user-agent: *\ndisallow: /robots.txt\n`; URL
   `http://example.com/robots%2Etxt` (normalizes to `/robots.txt`); expect `disallow`.
   - tool: exit 0 `clean` (exemption on raw path-to-match → not exempt → disallow → pass)
   - independent: exit 0 `clean` (same)
   - ref: exit 1 `failed-policy` [`exposed`] (exemption post-normalization → exempt → exposed)
   Contract (e): "The path `/robots.txt` is always allowed" — does not state whether
   normalization precedes that comparison. **Undecided; split 2:1.** Selftest fixture
   `e11-robots-txt-exemption-is-exact` pins the tool's pre-normalization reading; ref disagrees.
   Sealed cases contain no `%2E`/`/robots.txt` interaction.

3. **(c) group-name folding ASCII-only? (reference defect, not a text gap)**
   Input (`tmp/cases/t7`): robots = `user-agent: \u212A\ndisallow: /x\n` (KELVIN SIGN, U+212A,
   Unicode-fold-equivalent to `k`); userAgent `k`, expect `disallow`.
   - tool: exit 1 `failed-policy` [`exposed`] (ASCII-only fold → no match → allowed)
   - independent: exit 1 `failed-policy` [`exposed`] (same)
   - ref: exit 0 `clean` (Unicode `lower()` folds U+212A → `k` → matches → disallowed)
   Contract says "ASCII case-insensitively" — decided; ref's Unicode folding is the known defect
   already recorded in SCORECARD measured results ("reference folds group names with Unicode
   `lower()`, a reference defect the sealed cases do not reach"). Still a live split: both
   independently-written implementations agree with the contract; ref does not.

## Probed, no split (all three agree)

4. **(e)** URL `/robots.txt?q=1` vs rule `disallow: /robots.txt`, expect `disallow`: all three
   exit 0 `clean` — exemption by strict equality to the whole path-to-match (path+query); none
   exempts on the path component alone (`extras/e1`). Text underdetermined; all three chose the
   same reading.
5. **(c)** matching group with empty rules suppresses the `*` fallback (group `g` empty, group `*`
   disallow /x, UA `g`): all three `clean` (`extras/e2`).
6. **(b)** line `user-agent#x: y` (comment strips before colon check): ignored; all three `clean`
   (`extras/e7`).
7. **(a)/(f)** 4xx ignores `robots` (T59); 5xx disallows incl. `/robots.txt` (T61); status
   300/399/600 and 200.0 invalid (T10/T11); duplicate `id` invalid even when both otherwise valid
   (E4); `robots` pointing to a directory invalid (E5); uppercase scheme + port URL valid (E6);
   comment-only robots → all allowed (E3); usage error (extra arg) exit 64 on all three (E8).
8. **(b)/(d)/(e)** CRLF (T31), BOM dropped (T79), reserved `%2F` distinct from `/` (T41),
   non-ASCII rule equals percent-encoded path (T75), `%7E` decoded (T77), empty rule never matches
   (T47), rule before first user-agent ignored (T49), non-record key does not end a group (T51),
   `$` alone never matches (T43), non-final `$` literal (T45), `*` matches any run (T22), longest
   rule wins (T27), equal-length tie allow wins (T28), fragment excluded (T67), query included
   (T69), empty path → `/` (T71), symlink robots inside base OK (T53), symlink robots escaping →
   check_invalid (T55), `sub/../robots.txt` inside OK (T57), manifest BOM/`version: true`/
   `checks` non-list → input_invalid (T35/T15/T14), missing `expect` → check_invalid (T16).

## Verdicts
- The implementations split on 2 genuinely undecided contract sentences (manifest-directory
  resolution for a symlinked manifest; pre- vs post-normalization `/robots.txt` exemption) plus
  the known reference defect in group-name folding; tool and independent agree on every probed input, ref differs on those 3.
- C1's sealed 28 cases reach none of the split points (no symlink manifest, no `%2E`, no
  fold-equivalent non-ASCII group name), so "passed >= 25 of 28" is silent on them — consistent
  with the declared limit "the sealed cases certify the tested rules of (a)–(g), not every
  contract sentence". Confidence: high (direct differential execution). Remaining unknown:
  whether the lane's canonical reading for the two undecided sentences is the tool's (selftest-pinned) or the reference's; no admission verdict offered here (leaf seat).
