
## Round 37 — declared claims (before implementation lands)

Base `621fb528ba9116b9f440b8332be6dfc0cad4e972` (pushed lane tip at round start; round 36
admitted). Two claims on two different surfaces. Round 36 worked freshness on
`scripts/source_recheck.py`; the anti-loop rule moves C1 to a new frontier surface (publisher-side
crawl rules, PROVINCE "Crawl hygiene per host"). C2 only repairs a routed round-36 defect (closure
routed defect 3: the one-change tool mutants that still pass need fixture classes that kill them).

**C1 — operability (capability): offline robots.txt expectation audit `scripts/robots_audit.py`.**
Axis by the surface it changes: a new tool (operation) that tells a publisher, offline, whether
the robots.txt they will serve allows or disallows the URLs they say it should, under RFC 9309
(S011, re-opened this round) and the lane readings below. The command that would show the surface
unmoved: `git ls-tree <rev> -- scripts/robots_audit.py` prints nothing and the counter below scores
0 of 28. Frozen predicate, the same sentence here, in `.ufo/waves/round-37/sealed_count.py`
(`PREDICATE`, `met = cases == 28 and passed >= 25`) and in every receipt's `predicate` field:

    met: passed >= 25 of 28 sealed cases

- Before: 0 of 28 at the base `621fb528` (the tool is absent; `verification/c1-at-621fb528.json`,
  exit 1). After: `met` true at the build commit.
- Counting command (exit 0 met, 1 not met, 2 cannot evaluate):
  `python3 -B .ufo/waves/round-37/sealed_count.py --root . --revision <rev> --key-revision <reveal>`
- The 28 cases (7 bullets (a)–(g), 4 cases each) were written by the L1 before this declaration
  and stay outside the lane until a reveal commit; the counter pins their sha256 (`93ad9ee6…0a90`)
  and refuses a revision that holds them. Every case of a bullet carries one check per listed
  rule of that bullet, and every case has at least one check that holds and one that does not.
  Coverage statement, measured and nothing more: each of the 34 listed ablations of the L1's
  private reference scores at most 24 of 28 (16 to 24; receipts
  `.ufo/waves/round-37/verification/ablations/`), and the reference scores 28 of 28. This does not
  say that every way of skipping a rule fails; a mutation pass on the reference runs before any
  build (control wave) and its result is appended before any build.
- On every run the counter replaces every check id and robots file name with fresh random ones, so
  no tool can key on ids, file names or labels; the tool runs in a bubblewrap jail that sees only
  /usr and the scratch directory.
- Sourced: S011 (RFC 9309, re-opened this round, retained `.ufo/waves/round-37/sources/S011.txt`)
  and S095 (Google's robots.txt specification, opened this round); S096 and S097 are opened this
  round as well (row decisions in the lesson Gate).
- Limits: the cases are synthetic robots files and URLs, not live fetches. The tool reads a
  local file; it does not fetch, follow redirects, cache, or claim what any crawler does. Where
  RFC 9309 says SHOULD or MAY, the contract fixes one reading (marked "lane reading").

C1 contract (public; the sealed cases test exactly this):

- Usage: `python3 scripts/robots_audit.py --manifest PATH` prints one JSON report on stdout:
  `{"version": 1, "verdict": V, "checksEvaluated": N, "findings": [F, ...]}`, where each finding is
  `{"check": <check id or null>, "reason": R}` (extra fields allowed). Exit 0 when V is `clean`, 1
  when `failed-policy`, 2 when `could-not-evaluate`, 64 on a usage error (any argument list other
  than exactly `--manifest PATH`). It reads only the manifest and the robots files it names; no
  network, no writes.
- Manifest (UTF-8 JSON): `{"version": 1, "checks": [check, ...]}`. A check is an object with `id`
  (non-empty string, not equal to the id of an earlier check in the list), `robotsStatus` (a JSON
  integer 200–299, 400–499 or 500–599; booleans and floats are not integers), `userAgent` (a
  product token: one or more ASCII letters, `_` or `-`; RFC 9309 section 2.2.1), `url` (absolute
  URL, scheme `http` or `https`, non-empty host) and `expect` (`"allow"` or `"disallow"`). When
  `robotsStatus` is 200–299 the check also has `robots`: a relative path to a regular file inside
  the manifest's directory (after resolving symlinks and `..`). Otherwise `robots` is ignored.
- Findings per evaluated check: the tool decides whether the robots rules allow the URL for the
  user agent. `expect` `allow` and the decision is disallow: one `blocked` finding. `expect`
  `disallow` and the decision is allow: one `exposed` finding. Otherwise none.
- (a) Access result (RFC 9309 section 2.3.1). `robotsStatus` 200–299: the robots file is parsed
  and decides (rules (b)–(e)). 400–499 ("unavailable"): allowed, whatever any file says. 500–599
  ("unreachable"): disallowed, whatever any file says, including `/robots.txt`.
- (b) Lines. Only the first 512000 bytes (500 KiB, section 2.5; lane reading: exactly this
  limit) of the file are read; a leading UTF-8 byte order mark (EF BB BF) is dropped; the rest is
  decoded as UTF-8 with invalid bytes becoming U+FFFD. Lines end at CR, LF or CRLF. On each line
  everything from the first `#` is a comment and removed. A line without `:` is ignored. The key
  is the text before the first `:` with spaces and tabs trimmed, compared ASCII
  case-insensitively; the value is the text after it with spaces and tabs trimmed. Keys
  `user-agent`, `allow` and `disallow` are records; every other key (for example `sitemap`,
  `crawl-delay`) is ignored and does not end a group (section 2.2.4). An `allow` or `disallow`
  line before the first `user-agent` line is ignored (section 2.2.2).
- (c) Groups (section 2.2.1). A `user-agent` line starts a new group unless the previous record
  was also a `user-agent` line (blank, comment and ignored lines between them do not count), in
  which case it adds a name to the current group. The check's `userAgent` matches a group when it
  equals one of the group's names compared ASCII case-insensitively. The rules of every matching
  group are combined. If no group matches, the rules of every group named `*` are combined. If
  there is none, no rules apply and every URL is allowed.
- (d) Rules (sections 2.2.2, 2.2.3). A rule with an empty value never matches. `*` in a rule
  matches any sequence of characters (also none); a `$` that is the last character of the rule
  anchors the match at the end of the path (any other `$` is literal). A rule matches when it
  matches a prefix of the path starting at its first character (or the whole path when anchored).
  Of the matching rules the one with the longest normalized value (rule (e), counted in octets,
  `*` and `$` included) decides; when an `allow` and a `disallow` of that length both match,
  `allow` decides. No matching rule: allowed.
- (e) Path to match and normalization (section 2.2.2). The path to match is the URL's path (`/`
  when empty) followed by `?` and the query when the query is non-empty; the fragment is never
  part of it. The path `/robots.txt` is always allowed when (a) says the file decides. Before
  comparison both the rule value and the path are normalized: every non-ASCII character becomes
  its UTF-8 octets percent-encoded with uppercase hex; every `%XX` escape (two hex digits) of an
  unreserved character (ASCII letters, digits, `-`, `.`, `_`, `~`; RFC 3986) is decoded; every
  other `%XX` escape is kept with its hex digits uppercased. Lane reading of the section 2.2.2
  examples: reserved characters are never decoded or encoded, so `%2F` and `/` differ.
- (f) Check faults. A check that breaks any manifest rule above (not an object, id missing,
  empty or repeated, status outside the three ranges, a user agent that is not a product token,
  `expect` other than the two strings, a URL that is not absolute http(s) with a host, or for
  200–299 a robots path that is missing, absolute, escapes the manifest directory or is not a
  regular file): one `check_invalid` finding for it (check = its id when it is an object with a
  non-empty string id, else null) and no other finding for it; the other checks are still
  evaluated. `checksEvaluated` counts the checks that are not `check_invalid`.
- (g) Manifest faults. A manifest path that is not a regular file, larger than 64 MiB,
  unreadable, not UTF-8 or not JSON, a non-object, `version` other than the integer 1, or `checks`
  not a list: one `input_invalid` finding with check null, nothing evaluated.
- Verdict: any `input_invalid` or `check_invalid` finding gives `could-not-evaluate`; otherwise any
  finding gives `failed-policy`; otherwise `clean`.
- A case passes when, for each of its runs (one manifest each; most cases have one, the (g) cases
  five), the exit code, `verdict` and the multiset of findings projected on (check, reason) equal
  the sealed expectation. Field order, `checksEvaluated` and extra fields are not compared.

**C2 — operability: the fixture set of `scripts/source_recheck_selftest.py` kills the 32
round-36 one-change tool mutants.** Axis by the surface it changes: the lane's selftest gate for
its landed tool (its fixture data); not coverage of a new rule, not a new tool. Round-36 wave 2
`MutTool` found 5 of its 32 mutants pass the selftest (M07, M08, M09, M11, M24) and 9 meet the
sealed target. The command that would show the surface unmoved: the counter below at a revision
whose selftest is the base selftest gives the base count. Frozen predicate, the same sentence
here, in `.ufo/waves/round-37/c2_mutkill.py` (`PREDICATE`) and in every receipt:

    met: killed >= 32 of 32 round-36 tool mutants

- Counting command: `python3 -B .ufo/waves/round-37/c2_mutkill.py --root . --revision <rev>`
  (exit 0 met, 1 not met, 2 cannot evaluate). Before: killed 27 of 32 at the base `621fb528`
  (101 fixtures, all valid on E1 and E2; survivors M07, M08, M09, M11, M24; receipt
  `.ufo/waves/round-37/verification/c2-at-621fb528.json`, exit 1). After: `met` true at the build
  commit.
- The counter reads only the selftest's fixture data (dumped inside a jail) and runs every
  fixture itself; the selftest's own runner never runs, so a selftest cannot recognize a mutant by
  hash, name or text. A fixture counts only when it passes on both the measured round-36 tool
  (`4d5b3d55`, E1) and the round-36 independent blind implementation (E2), so a junk, all-false or
  one-reading fixture counts for nothing. A mutant is killed when a counted fixture fails on it.
- Limits: 32 known mutants, not every defect. The tool itself is not changed by C2.

Controls for both claims (receipts under `.ufo/waves/round-37/verification/control-*.json`,
committed before any build): the base (do nothing); for C1 a constant clean tool, an all-false
tool (every check reported against its expectation), a no-reader tool (status rule only, never
opens a robots file), a junk tool (non-JSON output), a shortcut tool keyed on ids, URL words,
user-agent names and file names, and a naive reader (a `disallow` value that is a raw prefix of
the URL path decides, no groups, no allow, no normalization); for C2 the base selftest, an
all-failing fixture set, a junk fixture set, a fixture set that keys on mutant ids, names or
hashes, and a snapshot fixture set (expectations recorded from E1 on random inputs). Built by a
pre-freeze control wave of fresh critic and mutation-tester seats from this public text only. A
control that meets a predicate means that counter or target is wrong; it is fixed before any
build, with the original rule kept as the rule of record (round-36 routed defect 4).

Counter digests at this declaration: `sealed_count.py` sha256 `2ebb39b5…f0e3`, `c2_mutkill.py`
sha256 `d72e232e…cf0e3`. Mutant manifest pin `9300ad38…dbd4` (MutTool's `manifest.json`; its
`summary.json` sha256 `1cfa9ce1…0af9` equals the one cited in `round-36/w2/MutTool.md`).
