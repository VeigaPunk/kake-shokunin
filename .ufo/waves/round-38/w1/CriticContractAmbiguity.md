# CriticContractAmbiguity — r38 w1: what (h)/(i)/(k) leave undecided

Advisory for the L1 and the non-author closure; no verdict on the round. Sealed trees untouched (no
`/fast/scratch/hyaku/kake-r38*/` path opened, no case search, no round-38 counter run), no network, no installs.

## Evidence base
- Sandbox clone at `2dab7f31`; `sha256sum clone/scripts/robots_audit.py` → `944d2f51…d3e5` (the claimed base bytes).
- Fixtures `/fast/scratch/hyaku/kake-r38w1/CriticContractAmbiguity/fx/<id>/`; builder `mkfx.py` sha256 `a91b601f7caed2e85d84c5589c30e6e95347b596b5a05b6faba0aa90fa3dbf6b`; fixture tree (sorted `sha256sum` of every file, 78 files) `b4fe0cb9140e472414cb149703b4edeccd2a5448baeda22b3fdd283fb3f10ae8`.
- Every `rc=` is `python3 -B clone/scripts/robots_audit.py --manifest fx/<id>/m.json` (base tool), default
  robots file `User-agent: *\nDisallow: /`; only the base column is observed, each "B" is a reading of the
  cited sentences. SCORECARD line numbers are at `2dab7f31`.

## Points
1. `checksEvaluated` under an input fault — undecided *and* counter vs contract. h07 (5000-digit status plus
   one valid check): A ("nothing is evaluated", 2146-2147/1856) emits 0 (base emits 0); B reads (f) "counts
   the checks that are not `check_invalid`" (1852-1853) literally — no check *is* check_invalid when an input
   fault preempts — and emits 2. The contract says "`checksEvaluated` … not compared" (1861) while counter v3
   compares it whenever a run states it (`sealed_count_v3.py:178-180`) and 2233-2234 says every run states it.
   **Changes a sealed-style check**: a build reading only the contract cannot know which value to emit.
2. Literal in an ignored field or nested object. h01 (`"note":NaN`), h03 (`check.extra={"z":NaN}`), h04
   (`"NaN":1` key): A (base) ignores → `rc=1` blocked, evaluated 1; B ("a manifest holding any of them", 2146)
   → `rc=2`, `[null input_invalid]`, 0. h02 (`"note":"NaN"`) and h12 (`id:"-Infinity"`): evaluated identically both ways.
   **Changes a sealed-style check** (`A1-no-constant-reject` fails j1,j2).
3. Literal inside a read field — (h) vs (f). h08 (`robotsStatus:-Infinity`): A ((h)) `[null input_invalid]`,
   0, rc2; B ((f) 1847-1853: one `check_invalid` for that check) `[a1 check_invalid]`, rc2 — base = B.
   **Changes a sealed-style check** (j1/j2).
4. `-Infinity` vs `-1e400` (h08 vs h09). Decided by 2253-2254 (input_invalid vs check_invalid) and base splits
   them so, but after parsing both are `-inf` and compare equal (measured): the split exists only at parse
   time (`json.loads(parse_constant=…)` fires for the three literals, never for `-1e400`; measured). A
   value-level validator collapses the pair. **Changes a sealed-style check.**
5. Long integers. h05 (`"pad":` 5000 digits, unread field): A ("a number of any length in a field the contract
   does not read changes nothing", 2149-2150) → `rc=1` blocked; B (CPython 3.14 `json`, 4300-digit int limit)
   `ValueError` → `rc=2` `[null input_invalid]`, 0 — base = B. h06/h07 (5000-digit status; h07 plus one valid
   check): A `[a1 check_invalid]` (+ a2 evaluated, count 1 for h07); B `[null input_invalid]`, 0 (base).
   **Changes a sealed-style check** (`A2-no-long-int` fails j3,j4).
6. Integral numerals in float syntax. h10 (`robotsStatus:2e2`), h11 (`200.0`), `version:1.0`: A (float syntax;
   "floats are not integers", 1848+2253) → `[a1 check_invalid]` (base agrees), `version:1.0` input_invalid;
   B (RFC 8259 has one number type; `2e2` *is* 200) → status 200, evaluated → `rc=1` blocked.
   **Edge only** for the sealed set, but it flips (a) and the verdict class.
7. The 64 MiB digit bound is unreachable by converting. Measured `int()`: 8 M digits 2.71 s, 16 M 6.22 s, 32 M
   13.86 s → 64 M ≈ 30 s > the 20 s budget; and a ≤64 MiB manifest cannot hold 64 MiB of digits plus
   `{"version":1,"checks":…}`. Only deciding long integers by digit count meets 2150-2151; 2253 changes
   nothing arithmetic. **Operability, not a check.**
8. "(i) … judged as written, before any parsing" (2157): decoded value or manifest bytes? i13
   (`"url":"https://h/\u0041"`): A (decoded `A`) → evaluated, `rc=1` blocked (base); B (bytes hold `\`, which
   (i) excludes, 2155-2156) → `[a1 check_invalid]`, rc2. **Changes a sealed-style check** (u1–u4).
9. (i) against a parser that deletes characters. i01 (TAB in the path): A ((i)) check_invalid; B (validate the
   parsed URL) — `urlsplit` deletes `\t`, so the path becomes `/ab` (measured) → evaluated, `rc=1` blocked
   (base). Same for CR/LF; i02 (trailing space) survives parsing and (i) decides it. **Changes a sealed-style check.**
10. Scope of (i): `url` only or every check string. i12 (`robots":"r .txt"`, a real file): A ("A check's
    `url`", 2152) → valid, `rc=1` blocked (base); B (extend to `robots`) → `[a1 check_invalid]`, rc2.
    **Edge only** (no sealed class names `robots`) but it voids a check.
11. Host geometry — (i) is "not a full RFC 3986 grammar check" (2139-2140) and (f) only says "with a host"
    (1849). i03 `https://[::1/x`, i05 `https://h:abc/x`, i06 `https://exämple.com/x`, i07 `https://ex%2Eample.com/x`,
    k13 `https://ex%2Eample.com/robots.txt`: A (`urlsplit` host non-empty) → i03 check_invalid, rest evaluated
    (base); B (RFC 3986 host) → all check_invalid; C (raw netloc non-empty, no bracket logic) → i03 evaluated too.
    **Edge only** unless a u case carries one.
12. `%` not followed by two hex digits. i08 (`/x%zz`, rule `Disallow:/x%zz`), i09 (`/x%`): decided by 2254-2255
    ("allowed by (i) and kept by (e)"); base agrees (`rc=1` both); no divergence for `%`+one hex, `%FF`, rule values. **Edge only.**
13. Lone surrogate. k14 (`"url":"https://h/\ud800"`): A (base `surrogatepass` — a docstring lane reading, not
    the contract) `%ED%A0%80` → `rc=1`; B ((b)'s U+FFFD analogy) `%EF%BF%BD`; C (no UTF-8 octets →
    check_invalid). Observable only against a rule naming the octets. **Edge only.**
14. (k) dot segments. k01 `/./robots.txt`, k02 `/a/../robots.txt`: A ("normalized by rule (e)", 2159; (e) has
    no dot-segment step) → rules → `rc=1` blocked (base); B (RFC 3986 §5.2.4, or a URL library applying it) →
    allowed, `rc=0` clean. **Changes a sealed-style check** (r1–r4).
15. (k) matrix parameters. k03 `/robots.txt;x`: A ((e) "the URL's path") → rules → `rc=1` (base); B (a URL
    library strips `;params`) → clean. **Edge only**, but silent in a rebuild.
16. (k) implicit allow vs an explicit longer disallow. k08 (`Disallow: /robots.txt$`): A (2256-2257: implicit
    allow wins) → `rc=0` (base agrees); B (implicit allow as a length-11 allow rule under (d)) → the length-12
    rule wins → blocked. k09 (`Disallow: /robots.txt`, a tie) is clean under both. Declared decided, but S011
    puts "The /robots.txt URI is implicitly allowed" right after the no-match sentence (reads as a default).
17. (k) trailing `?` and query. k04 (`/robots.txt?`) → allowed, `rc=0` (base agrees); k05 (`/robots.txt?x=1`)
    → rules, `rc=1`. Decided by 2255-2256; no divergence found. **Edge only.**

## Not verified
- No round-38 counter run (no key) and no second reader built: every "B" report is a reading, not observed.
- Whether points 2, 3, 8, 9, 14 land in a sealed run is inference from the public ablations (`A1` fails j1,j2;
  `A2` j3,j4; `A3`–`A5` u1–u4; `A6`–`A8` r*), not from the case contents.
- Points 7, 12, 17 are negative results (no divergence found), not defects.
