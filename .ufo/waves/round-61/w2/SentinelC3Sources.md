# SentinelC3Sources

Scope: the two source-fetch receipt sets (`.ufo/waves/round-61/sources/receipts.json` S430–S433 and
`.ufo/waves/round-61/recheck/receipts.json` S001–S010), the fetcher that produced the recheck set
(`w1/ExecC3Fetch.files/fetch_recheck.py`), the retained bodies, and the C3 counter's path/evidence confinement
(`c61_recheck_pins.py`). Read-only on the lane; every counter run used scratch clones under
`/fast/scratch/hyaku/kake-r61/SentinelC3Sources` (`git clone --shared`, toplevel asserted), and the only
mutations were inside those clones. No tools installed.

Axes: evidence integrity (hash/URL/userAgent/cap/no-secret), evidence-state completeness at the measured
revision, and counter path confinement.

## S1 HIGH — redirect destination is never recorded, and the ≤5-hop cap is not enforced

Fetcher: `fetch_recheck.py:59-63` builds `urllib.request.build_opener()` with no custom redirect handler, so the
default `HTTPRedirectHandler` follows 301/302/303/307/308 automatically (its own `max_redirections = 10`) and
returns the final 200 to `opener.open`. The manual branch (`except HTTPError` on 3xx, lines 100-112) is therefore
unreachable for ordinary redirects; it only runs once the default handler has exhausted itself. Consequences,
all in the record the receipts are taken from:
- `effectiveUrl` is `current`, the URL **before** any redirect, so it can only ever equal the requested URL.
- `hops` stays 0 for every redirect the default handler swallowed.

Local probe against the unmodified function (scratch server, no network):

| probe | result |
|---|---|
| `/start` → 302 → `/final` | `status=200`, `effectiveUrl=/start`, `hops=0`, 2 requests on the wire |
| `/chain/3` | `effectiveUrl=/chain/3`, `hops=0`, 4 requests |
| `/chain/20` | `effectiveUrl=/chain/9`, `hops=1`, **21 requests (20 redirects)** |
| `/loop` | `RuntimeError: redirect limit 5 exceeded` after **30 requests** |
| `/big` (3 MiB) | 2097152 bytes returned, `truncated=True` |

So the "at most 5 redirects" fetch-ethics constraint is violated by construction (up to ~10 per manual hop;
30 requests observed on a loop), and the receipts cannot distinguish "served 200 at this URL" from "301'd to
another host, which served 200". `w1/ExecC3Fetch.md` assertions "redirects followed by hand and capped at 5
(zero occurred)" and "No redirect was followed (`hops=0` everywhere)" rest on fields that are structurally always
the request URL / 0; they are not evidence of anything.

Exploit path: a row URL that now 301s to an unrelated host (expired domain, parked page, CDN takeover) yields a
receipt with `effectiveUrl` = the registry URL and `hops` = 0 while the retained body is the redirect target. The
Gate quote is then "re-located" in the wrong document and the freshness claim is attached to a URL that no longer
serves the claimed page; nothing in the receipt set exposes the substitution.

Impact: the freshness claim's URL-identity anchor is unverifiable from the receipts; the hop cap is a false
statement about fetch conduct. This round no redirect is *proven* to have occurred — it is simply unobservable.

Smallest remediation: install a handler whose `redirect_request` returns `None` (or raises) so 3xx reaches the
manual loop, count hops in one place, and record the final URL plus each `Location`; persist `hops` and
`truncated` in each receipt, or fail the fetch when the final URL differs from the requested URL.

## S2 HIGH — the C3 after-state is not met at any committed revision, and not met in the worktree either

`c61_recheck_pins.py` reads committed bytes only (`git show`/`git ls-tree`), which is correct. The evidence,
however, is not committed:

- lane HEAD `f5a9b8a`: `.ufo/waves/round-61/recheck/S010.html`, `sources/S432.html`, `sources/S433.html` and
  `corpus/lessons/round-61.md` are **untracked** (`jj status`); `corpus/SOURCES.md` at HEAD is unedited (0 pins).
- Counter at HEAD: `conditions_passed=4` — C1, C3 (**vacuous**), C4, C6 pass; C2 fails
  (`no due row carries a concrete ISO recheck date (0 pins)`), C5 fails (`S001: unpinned due row carries no Gate
  note`).
- Counter on a scratch commit that overlays the current worktree (`SOURCES.md`, `lessons/round-61.md`, all ten
  recheck bodies + receipts): **4/6**. C3_gate_quotes fails for all 9 pinned rows because the lesson § Gate is
  still the skeleton with `<URL fetched>` placeholders — no URL, no access date, no quoted span. C5 fails because
  S001 was left at `on-release`.
- S001 is a direct contract deviation, not merely a missing note: the frozen pin rule says non-`Nd` cadences
  (S001, S002) pin to `opened + 90d` = 2027-01-17, and S001's fetch was HTTP 200. It is unfetched-looking
  (`on-release`) with no observed-state Gate note either.

What is sound inside that run: C4 passes 10/10 — every receipt `sha256` equals the committed body's sha256, every
`bytes` equals the blob length, all `status=200`, all `fetchedAt` on 2026-10-27 UTC, all `userAgent` `round61`,
every receipt `url` is one of the row's URLs (S010 keeps its `#section-8.8` fragment in `url`, `effectiveUrl`
strips it, which matches the row), and C6 sees `base_rows=167 rows=171 appended=[S430..S433]`.

Impact: claim C3's predicate (`conditions_passed == 6 of 6`) is false at every currently committed revision and
false for the present worktree state; a scored after-state would be 4/6. The receipt set itself pins correctly —
the after-state does not exist yet.

Smallest remediation: the L1 integration must (a) write the ten Gate lines with URL + 2026-10-27 + located quote,
(b) pin S001 to 2027-01-17 or write its observed-state note, (c) commit `recheck/S010.html` (and, for C2,
`sources/S432.html`, `sources/S433.html`, the lesson and the entry) before any after-state is measured.

## S3 MEDIUM — C3 body-to-row binding is by basename at any depth, so a nested committed file shadows the real body

`c61_recheck_pins.py:443-452` walks `ls_tree(RECHECK_DIR)` (recursive) and keys bodies by
`stem = os.path.splitext(os.path.basename(rel))[0]`. A committed file at any depth whose basename is
`S<id>.<ext>` becomes that row's retained body; git tree order is sorted, so a nested path sorts after the
top-level one and overwrites it.

Probe in the scratch clone (toplevel asserted), starting from the 10-body after-state:
1. commit `.ufo/waves/round-61/recheck/sub/S010.html` = `DECOY-BODY` (10 bytes) and rewrite only the S010 receipt
   to the decoy's sha256/size → counter C4 **passes** (`conditions_passed=4`, C4 True), i.e. the decoy was taken
   as S010's evidence.
2. keep the decoy, restore the true S010 receipt (`d4317606…`, 1187554) → counter C4 fails with
   `S010: receipt sha256 d431760660ea != committed blob sha256 178c1d3eab63` and
   `receipt bytes 1187554 != committed blob length 10`: the blob under test was the 10-byte decoy, while the
   canonical `recheck/S010.html` (1187554, `d4317606…`) was untouched.

Exploit path: a committer adds `recheck/<anything>/S010.html` with text of their choosing and a matching receipt
entry; the canonical fresh body stays in place, so the receipt set looks honest, while C3's quote-location check
runs against the shadow body. Any quote can be made to "occur" in the shadow. The same mechanism can also kill a
valid claim (shadow with a mismatching receipt → red) and is the kind of mutation a fix must be able to refuse.

Impact: the quote-truth half of C3 (condition C3) binds to an attacker-chosen blob rather than the retained
fresh body named by the contract (`recheck/<id>.<ext>`). Receipts and bodies are both committed by the same
actor, so hash agreement alone does not restore binding.

Smallest remediation: accept exactly `RECHECK_DIR/<sid>.<ext>` at depth 1, one file per id (reject a second
candidate with a `body_ambiguous`/`body_nested` finding instead of last-wins), and never derive a row id from a
basename outside that directory.

## S4 LOW–MEDIUM — receipts do not persist truncation/hops, and the S430–S433 fetch has no retained fetcher

- `truncated` is computed (`fetch_recheck.py:95`) and printed, but never written into the receipt; a body cut at
  the 2 MiB cap would be receipt-identical to a complete one. Not exercised this round (largest retained body
  1187554; S002 at 199999 bytes ends `</html>`, so it is not a cap artefact — verified).
- The S430–S433 receipts have no retained producer. `w1/ScribeC2Rows.md` records "tools used were `curl`"; no
  script in `w1/` fetches those URLs (`grep` over `*.py`/`*.sh` finds only `fetch_recheck.py`). `userAgent:
  round61`, GET-only, the 2 MiB cap and "no redirect" are therefore self-reported for the C2 sources, and no
  response headers were retained. S432/S433 bodies are additionally untracked at HEAD, as is the entry.
- `NoCookies` (`fetch_recheck.py:53`) is dead code (never instantiated); the opener is safe only because
  `build_opener()` adds no cookie processor by default. The comment "no proxy juggling" is wrong: the default
  `ProxyHandler` honours `http_proxy`/`https_proxy` (unset on this host — `env | grep -i proxy` empty — so no
  effect this run, but provenance is environment-dependent).

No secret material in either receipt file or the fetcher: no cookie, `Authorization`, bearer/token/`ghp_`/`sk-`
field; the retained bodies are public pages. All 14 receipt sha256 values match the on-disk bodies, and the
tracked blobs match at HEAD (9 recheck bodies + S430/S431 committed; the three untracked ones listed above are
the gap).

Smallest remediation: persist `hops`/`truncated` (and, ideally, the final URL as verified) in each receipt;
retain the source fetcher for S430–S433 or re-fetch them with the retained one; delete `NoCookies`; either clear
proxy env explicitly or state that the host has none.

## S5 LOW — counter knobs and one vacuous pass

- Contract CLI for C3 is `--root <lane> --revision <rev> [--json]`; the counter adds `--base` (default
  `BASE_REV`). A caller-chosen base re-defines C1's due-set derivation and C6's byte-identity baseline, so the
  measured "after" can be compared against a friendlier "before" (e.g. a base whose registry already carries
  pinned cells). The predicate sentence stays fixed, but the evidence under it moves.
- `C3_gate_quotes` loops over `pinned` rows only, so with 0 pins it passes vacuously (observed at HEAD: C3 True
  while the sweep had not run). C2's 0-pin failure is currently the only thing keeping that from being a clean
  partial score.

Smallest remediation: remove `--base` or require it to resolve to `BASE_REV`; make C3 fail when `pinned` is
empty.

## Confirmed-sound surface (for the record)

- Hash consistency: 14/14 receipt `sha256` == body sha256; `bytes` == file length; S430–S433 and S001–S010
  `fetchedAt` all on 2026-10-27 UTC; UA tag `round61` in every entry; receipt URLs equal row URLs (S010 fragment
  retained in `url`, dropped from the wire).
- Bodies are the pages the URLs name: S001 `action.yml` for upload-pages-artifact v4.0.0; S002 title
  `Release v4.0.0 · actions/upload-pages-artifact`; S008 GNU tar `tar.texi`; S430 RFC 6797 (`Strict-Transport-Security`
  ×30, `RFC 6797` ×45); S431 declares `WD-CSP3-20261027`, `27 October 2026` (a Working Draft, as A4 records);
  S432 `Fetch Standard`; S433/S010 `RFC 9110` with `section-8.8`/`8.8.3` present.
- Counter is committed-bytes-only in fact: a worktree-only edit of `recheck/S010.html` left the result unchanged
  (C4 True, 4/6). `--root` must be the repository toplevel (realpath compare), else exit 2. `--selftest` is
  green: `56/56 (… 30 fixture cases …)`.
- Cap behaviour itself is correct in code and probe: 3 MiB input → 2097152 bytes retained, `truncated=True`.

VERDICT: receipts are hash-consistent and secret-free, but the fetch record cannot evidence redirects (effectiveUrl/hops are structurally always the request URL and 0; the ≤5-hop cap is exceeded — 20 redirects observed), the C3 after-state is 4/6 today (Gate skeleton, S001 unpinned, S010 body uncommitted), and the C3 counter binds bodies by basename so a nested committed `S010.html` demonstrably shadows the real evidence.
