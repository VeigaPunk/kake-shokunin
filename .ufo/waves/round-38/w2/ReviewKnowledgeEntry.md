# Kake R38 w2 — ReviewKnowledgeEntry (falsify): `corpus/knowledge/robots-txt-rules.md` Round 38 amendments

Scope: every sentence of "## Round 38 amendments — lane readings (appended)" (lines 84–123 at `adab4c7e`) plus the amended source line (line 1), each vs its cited SOURCES row/section/quote and vs the built tool's observed behavior. No installs this run (curl/git/python3 preexisting; pacman untouched per 2026-10-20 pause). Sandbox clone at tip: `/fast/scratch/hyaku/kake-r38w2/ReviewKnowledgeEntry/clone` (HEAD `adab4c7e…`, verified). Host Python 3.14.8.

Commands (all exit 0 unless noted): `git clone -q … && git checkout -q adab4c7e…`; `git show adab4c7e:corpus/SOURCES.md | grep -n 'S0(34|98|99|100|101)'`; `curl -sS -o <f> <url>` for rfc8259.txt, rfc9309.html, robots.cc@22b355ff, docs.python.org json.html; `TMPDIR=<sb>/tmp timeout 300 python3 -B run_tests.py` → **exit 0, 17/17 PASS** (harness `/fast/scratch/hyaku/kake-r38w2/ReviewKnowledgeEntry/run_tests.py`, sha256 `0ff62b23219822fd8a533519f3f861900ea55fe5fd6f510fd5164675921c7d0f`; tip tool sha `f4d057c4…baace` = declared; base tool `944d2f51f396…d3e5` extracted via `git show af43a50:scripts/robots_audit.py`).

## Verdicts (holds unless marked)

- L1 source line rows exist: S034 (:42), S098 (:106), S099 (:107), S100 (:108), S101 rejected (:109). Holds.
- L88 "Sources opened 2026-10-23: S034, S098, S099, S100": lesson `corpus/lessons/round-38.md:25-53` Gate lines show all four accessed 2026-10-23T04:30:xxZ; S034 is a re-open, "identical to the 2026-10-21 opening" — I reproduced the byte-identical copy (my fetch sha `61a5378f4255…b4cd2d7` = lesson receipt; rfc9309 fetch `bbaa2806…dc1a87` = S099 row pin; json docs fetch `234b80bf…f792e` = S100 row pin). Holds.
- L91-92 (h) RFC 8259 §6 quote "are not permitted": `rfc8259.txt:377-378` verbatim. Holds.
- L92-94 NaN/Infinity/-Infinity → "one input_invalid finding with nothing evaluated": tool exits 2, verdict could-not-evaluate, checksEvaluated 0, findings `[{"check":null,"reason":"input_invalid"}]` (harness h2 ×3). Holds.
- L94-96 "Python's json module accepts all three by default… (S100…); the round-37 tool used the default and let them through": `json.loads` → nan/inf/-inf; S100 row anchors match the page; base tool on NaN manifest → exit 0 clean, no findings (harness h3). Holds.
- L96-99 "…limit range and precision (S034 §§6, 9)… any-length integer parses; out-of-range robotsStatus of any length is check_invalid for that check; long number in an unread field changes nothing": RFC 8259 §9 at `rfc8259.txt:549-550`; 5000-digit robotsStatus → exactly one `check_invalid` for id `long`, other check evaluated (evaluated=1); 5000-digit unread field → clean, evaluated=1 (harness h4). Holds.
- L99-100 "Python's default 4300-digit conversion limit would make a 5000-digit integer an input_invalid manifest instead": default `json.loads` raises ValueError; base tool → input_invalid (harness h5); `w1/ProbeDigits.md:3,19` confirms from 4301 digits. Behavior holds — but see F2 on "(S100 points to that limit)".
- L101-103 (i) S098 §§2.1–2.3 classes; rejects (check_invalid) the named ASCII set wherever it sits; judged as written before parsing; non-ASCII kept; bare `%` passes; charset-only, no grammar check: harness i2 = 12 classes (space, `\x01`, `\x7f`, `"`, `<`, `>`, `\`, `^`, `` ` ``, `{`, `|`, `}`) × 6 positions → 72/72 `check_invalid`, evaluated 0; controls `http://h/caf%C3%A9`, `%2zb`, `%2`, `http://h/[a]`, `http://h/::::` → no fault, decided by rules (evaluated 5, clean). Tool: `scripts/robots_audit.py:149` (`_URL_FORBIDDEN_RE` = exactly the other 43 ASCII), `:508` checked before urlsplit in `:513-523`, normalize `:174`; lesson `round-38.md:36-37` 85 allowed / 43 excluded / 0 mismatches. Holds.
- L108-109 "WHATWG URL parser and Python's urlsplit strip or drop some of these characters instead of rejecting them": urlsplit drops `\t\n` (path `/px`), keeps space as written (`/p `), rejects neither (harness i6); WHATWG half per retained S101 quote (lesson `:47-51`); S101 correctly cited as rejected, not a source (row :109). Holds.
- L114-115 (k) S099 §2.2.2 "The /robots.txt URI is implicitly allowed." + same-section unencoding of percent-encoded unreserved octets: `rfc9309.html:1635` (`#section-2.2.2-2`) and `#section-2.2.2-4` "…MUST be unencoded prior to comparison, unless it is a reserved character… or outside the unreserved character range." Holds.
- L115-118 2xx implicit allow on normalized path: `/robots%2Etxt`, `/%72obots.txt`, `/robots.txt?` allowed; `/robots.txt?x=1`, `/ROBOTS.TXT`, `/robots%2Ftxt`, `/a/../robots.txt` decided by the rules (all 8 checks clean with `Disallow: /` file, expect split allow/disallow). Holds. Tool `:605-606` `normalize(path_to_match(parts)) == IMPLICIT_ALLOWED_PATH`; `path_to_match` `:534-539` (empty query dropped, non-empty appended).
- L119-120 "replaces the round-37 tool's raw-path comparison": base tool on `/robots%2Etxt` expect allow → exit 1, finding `blocked` (raw comparison confirmed; base docstring said so, diff af43a50..adab4c7e). Holds.
- L120 "under 5xx every URL is disallowed": robotsStatus 503 + `/robots.txt` expect disallow → clean; expect allow → exit 1 `blocked`. Holds.
- L121-123 "Google differs: no implicit allow, does not decode the path, blocks `/robots%2Etxt` under `Disallow: /` (S096 robots.cc @22b355ff, lines 537–546)": fetched robots.cc — `AllowedByRobots` at `:537-546`, comment ":540-541 The url is not normalized (escaped, percent encoded) here", `return !disallow();` with no /robots.txt special case; `grep -i implicit` finds none. "Blocks" follows by prefix match of `/` on the un-decoded path [INFERENCE, not executed C++]. Holds.

## Findings (by severity)

- F1 — overstated (minor), L1: "S034, S098–S100 added round 38" is wrong for S034. The S034 row was added in round 24 (`git log -S'| S034 |' -- corpus/SOURCES.md` → `3d07733`; present at base af43a50, `grep -c '| S034 |'` → 1). Round 38 re-opened it and widened `used-by` only (lesson `round-38.md:55-58`: "S034 used-by … → …; S098, S099, S100 `—` → mined"). Suggested fix: "S034 re-opened, S098–S100 added round 38".
- F2 — unsourced parenthetical (minor), L99-100: "(S100 points to that limit)". The cited S100 page (byte-identical to the row's retained pin `234b80bf…`) contains no `4300`, no `int_max_str_digits`, no "maximum digits" (grep empty). The limit's lane evidence is empirical (`w1/ProbeDigits.md`) and its documentation lives in CPython's int/sys docs, not the json page. Behavior itself verified; attribution wrong.

## Residual risk / verification gaps

- Tool behavior tested on Python 3.14.8; S100 row pins 3.15.1 docs (row disclaims all-version claims; parse_constant/constant behavior unchanged 3.11+).
- Google "blocks" conclusion is reasoned from robots.cc source, not an executed binary; `w1/ScoutGoogleImplicit.md` not re-derived line-by-line.
- WHATWG strip/drop half accepted from retained S101 quote + lesson, WHATWG spec not re-fetched (S101 is a rejected row; entry makes no further claim on it).
- Duplicate JSON members, `1e400`, `version` handling: unclaimed by the amendments (SCORECARD marks undecided/untested); not attacked.
- No lane mutation: reads + git read-only in the fleet repo; writes only to my sandbox and this report. No processes left running.

Report: .ufo/waves/round-38/w2/ReviewKnowledgeEntry.md
