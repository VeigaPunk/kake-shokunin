# ExecFresh — C2 candidate v2 (round 100, kake-r100)

## Candidate
`.ufo/waves/round-100/w1/ExecFresh/freshen_304.py` — stdlib-only Python 3.
Docstring names contract v2, RFC 9111 §4.3.4/§3.2/§3.1/§5.2/§5.2.3,
RFC 9110 §5.5/§5.6.1.2/§5.6.4, lane conventions LC1–LC6 + LC8, and every
V2 clause; stdin read as BYTES via `sys.stdin.buffer` (non-UTF-8 → refusal);
every argv word other than `--selftest` ignored; no file/socket/subprocess
in the decision path. V1 candidate was read and adapted; the counter code
below its docstring (lines 1–33 only), build_frozen.py and frozen/*.py were
not read.

## Changes vs v1 (from contract text alone)
- V2-1: hand-rolled RFC 9111 §5.2 Cache-Control parser (`#cache-directive`,
  recipient list syntax, quoted-string with qdtext/quoted-pair, comma inside
  quotes does not split, whitespace only as OWS around commas and at ends,
  empty elements accepted). Qualified `no-cache`/`private` in either
  argument form, any case → `invalid_input: qualified cache-control outside
  contract`; malformed → `invalid_input: malformed cache-control` (LC8).
  Extension names merely containing/ending in those tokens ignored. Only
  the 304's Cache-Control examined.
- V2-2: every output header value trimmed of leading/trailing SP/HTAB.
- V2-3: `proxy-authenticate`, `proxy-authentication-info`,
  `proxy-authorization` dropped from the stored base map as well as from the
  304 copy (e1: stored `connection`, hop-by-hop, `content-length` etc. stay).
- e2: malformed ETag in any stored response refused (validated up front,
  as in v1). e3: Last-Modified trims SP+HTAB (already the v1 behaviour).
  e5: non-UTF-8/invalid JSON refused, never a traceback. e7: LC3 tie
  applies under weak ETag and/or Last-Modified (unchanged code path).

## Receipts (`scores.txt` in the seat dir)
- `sha256sum -c controls/instrument-sha256.txt` from the round-100 dir:
  all 21 entries OK (rc=0) — frozen instruments verified before attacking.
- Counter `c100_fresh304.py --candidate-file .../ExecFresh/freshen_304.py
  --work /fast/scratch/hyaku/kake-r100/ExecFresh/w` (bwrap sandbox):
  - attempt 1, default seed 100100: `hand=91/91 generated=300/300
    refusals=119/119 met=true` (rc=0)
  - seed 1: `hand=91/91 generated=300/300 refusals=132/132 met=true` (rc=0)
  - seed 2: `hand=91/91 generated=300/300 refusals=122/122 met=true` (rc=0)
  - seed 3: `hand=91/91 generated=300/300 refusals=131/131 met=true` (rc=0)
  sha256 `00edf6c4f5daad497042e997ed54ef9da022acfb7da3a6a35f6922b263672c04`
  in all four. One attempt; no fix needed.
- Selftest: `python3 -B freshen_304.py --selftest` → `selftest 97/97` (rc=0);
  covers every V2 clause (V2-1 token form, empty quoted form, extension
  names, comma-in-quoted, empty elements, malformed variants, OWS,
  caps-variants; V2-2 trimming; V2-3 stored proxy drop, e1 kept fields)
  and e1–e7 (e2 unselected malformed ETag, e3 tab trim, e5 non-UTF-8
  bytes case, e6 `age` copied, e7 tie under LM and ETag+LM), plus LC1–LC5
  selection/update cases.
- Step 4: `python3 -B .../freshen_304.py --zz-bogus-r100 </dev/null` →
  `invalid_input: input is not valid JSON` on stderr, rc=1 (empty-stdin
  refusal path; with non-empty invalid input also rc=1). Unknown flag
  behaves like no flag.

## Bounds observed
All writes inside `.ufo/waves/round-100/w1/ExecFresh/` (candidate +
scores.txt) and this report; scratch `/fast/scratch/hyaku/kake-r100/
ExecFresh/w` used as `--work` and removed after scoring. No git writes,
no tool installs, no host changes. Lane tip `e84a18714b6be7fd2456a2dcc5f28c0cb0ab981f`
matches the C1 repair commit.

## Findings / risks
None blocking. Paper risk only: the quote/qdtext acceptance matches the
contract ranges as written (`!`–`[`, `]`–`~`, obs-text; quoted-pair
`!`–`~`/obs-text), which excludes DEL/controls — consistent with the
counter's 91 hand + 1200 generated cases all passing.

EXECFRESH sha256=00edf6c4f5daad497042e997ed54ef9da022acfb7da3a6a35f6922b263672c04 hand=91/91 generated=300/300 met=true selftest=97/97 attempts=1
