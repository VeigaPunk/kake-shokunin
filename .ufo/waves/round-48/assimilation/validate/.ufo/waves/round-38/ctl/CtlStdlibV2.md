# CtlStdlibV2 — round-38 control (stdlib-delegating reader, patched for (h), (i), (k))

DISCLOSURE (binding, first line): I ran `test ! -e /fast/scratch/hyaku/kake-r38` — one existence *stat of that directory's inode*; nothing inside it was listed, read, searched, opened or observed, and the round-38 counter was not run.

## Built

- `/fast/scratch/hyaku/kake-r38ctl/CtlStdlibV2/robots_audit.py` (442 lines), sha256 `15b3f643671ad250400e214c411ccc9683ac4144770a2760ddcfa2d671230a04`
- harness (mine, unscored) `/fast/scratch/hyaku/kake-r38ctl/CtlStdlibV2/harness.py`, sha256 `dd690f549bfa3db911e1dbd06514bfd2b89dfaa6b043289b659a4a3a9104ae51`; no installs, no git/jj, nothing written outside my sandbox and this report.

## Patches (each with the contract sentence it copies)

Carried from round-37 `CtlC1Shortcut-followup` (`61724ead…`; 7/20 here: g3, j3, j4, r1–r4):
- S1 (b) "Only the first 512000 bytes … of the file are read"; S2 (b) "a leading UTF-8 byte order mark (EF BB BF) is dropped"; S3 (b) "Lines end at CR, LF or CRLF".
- S4 (b) "Keys `user-agent`, `allow` and `disallow` are records; every other key … is ignored and does not end a group" + "the text before the first `:` with spaces and tabs trimmed" — text filter only, no group or rule chosen; changed from 37 to `.strip(" \t")` (a key padded with U+000B is not a record under (b)).
- S5 (e) "path (`/` when empty) followed by `?` and the query when the query is non-empty; the fragment is never part of it".
- S6 (e) "every `%XX` escape of an unreserved character is decoded; every other `%XX` escape is kept with its hex digits uppercased" — text transform against the stdlib's unquote/quote round trip.
New:
- P-h1 (h) "`NaN`, `Infinity` and `-Infinity` outside a string are not JSON, so a manifest holding any of them gives one `input_invalid` finding and nothing is evaluated".
- P-h2 (h) "A JSON number of any length is JSON: an integer `robotsStatus` outside the three ranges, however many digits it has, is a check fault … and a number of any length in a field the contract does not read changes nothing" — conversion capped at 4000 digits (longer ⇒ out of range ⇒ check fault, unconverted; unread fields carried unconverted), keeping the 64 MiB bound linear.
- P-i (i) "A check's `url` holds, besides non-ASCII characters, only ASCII letters, digits, `-` `.` `_` `~`, the reserved characters and `%`. A `url` holding any other ASCII character anywhere … is a check fault … judged as written, before any parsing".
- P-k (k) "a URL whose path to match, normalized by rule (e), is exactly `/robots.txt` is allowed (so `/robots%2Etxt` and `/%72obots.txt` are allowed). A path to match with a query, another case or a kept reserved escape is decided by the rules".

(c) groups, user-agent matching, rule ranking and `*`/`$` matching stay inside `urllib.robotparser` (host 3.14.8, the RFC 9309 rewrite): no matcher, merger or precedence rule is written here.
Deliberately not done: delimiter-wrapping UA names and the token so the stdlib's substring test degenerates to equality — that is user-agent matching by another name.

## Expected score: 13 of 20 (`met` false); plausible 12–14

- g1, g2, g4, d1–d4 lost (7) by construction. Measured on 3.14.8: substring UA (`mybot` vs group `bot`), Unicode folding (`K` U+212A vs token `k`), non-final `$` (rule silently dropped), rank-by-matched-length vs rank-by-rule-length (`Disallow: /a**z` vs `Allow: /az`, path `/az`).
- "Groups ended by non-record lines" is neutralized by S4 and the empty-value rule is a no-op on 3.14, so a case whose only deviation is one of those could pass → 14; g3 passed the six-patch reader, so only P-k or the S4 trim could flip it → 12.
- j1–j4, u1–u4, r1–r4 expected (12). The six-patch reader passed j3, j4, r1–r4; j1/j2 failed it for a reason the constant rule cannot explain (it rejects constants), so they most likely mix a constant run with a (i) check, which P-i covers.
- 64 MiB-of-digits status → `check_invalid` in 0.09 s; 64 MiB number in an unread field → 0.06 s, no finding. 13 < 19: without writing (c)/(d) this control cannot meet the predicate — the separation the declaration claims; the counter measures it, I do not judge it.

## Evidence

- `python3 -B harness.py` → `41 ok, 0 failing`, exit 0: (h) constants / huge status / 64 MiB bound / float status; (i) 14 rejected + 4 accepted URL shapes; (k) 8 path shapes + 5xx; four (g)/(d) probes where the base agrees with the contract and the control does not (printed `dev`).
- Counter-shaped bwrap jail (`--ro-bind /usr /usr … --unshare-all --clearenv`, tool in scratch) → `could-not-evaluate` + `check_invalid` for the bad check, exit 2, contract shape, stdlib only.
- Differential fuzz, 240 random checks (6 robots files × 40, safe geometry): 0 differences against the base at `af43a50f` — the patches do not disturb (b)/(e)/(f).

## Attack notes for the L1

1. Counter, latent: `materialize()` writes case files flat (`work/fresh`) but rewrites `sub/x.robots` to `sub/<fresh>` — a case naming a robots file in a subdirectory becomes `check_invalid` for every tool; harmless today (reference 20/20), but the geometry is silently forbidden, and `files` keys differing only by directory collide.
2. Scratch dir and `HOME` are shared across cases and runs, so a tool can persist state between cases; no key is reachable, so it buys nothing now, but a stateful tool is not excluded.
3. Separation is measured on tools, not intent: delimiter-wrapping UA names and the token (`<name>`/`<token>`) turns 3.14's `agent in useragent` into equality — a transform that repairs the substring class; unicode folding, rank-by-length and non-final `$` are not repairable that way, so 19 still needs real (c)/(d). To make the sentence measured, pair a substring-UA check with a unicode-fold or non-final-`$` check in one case.
4. My tool: P-k short-circuits before the file is opened, so a file that validates but cannot be read would report allow, not `check_invalid` (the base's reading); unreachable without a race.
