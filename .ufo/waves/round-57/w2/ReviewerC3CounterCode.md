# ReviewerC3CounterCode

Scope: the version-2 block of `.ufo/waves/round-57/c57_quote_truth.py` (from `BODY_SHA256`, line 94) and its generators
`derive_c57_quote_truth.py` + `derive_c57_selftest.py`. Revision read: **4b8c73050470ada9e6583f3b12d659d1bed6a17f**
(its counter, bodies and receipts are byte-identical to the working tree — sha256 compared; working tree HEAD 51921b9).
Method: no LSP server/tool is mounted in this seat's toolset, so no `references`/`definition`/`diagnostics` call was
possible; every claim below is from reading the committed source and from executing it (counter at the build revision,
its own selftest, the two derive scripts, and counter runs over scratch clones of the landed evidence). No tool installs;
pacman untouched. All inputs below are in a `mktemp` repo; lane, fleet and jj untouched.

Baseline measured first (so that every mutant is compared to a passing state):
`python3 -B .ufo/waves/round-57/c57_quote_truth.py --root . --revision 4b8c730…` → `8/8 met=True EXIT=0`; and a scratch
clone of the landed evidence (base commit = `28fa0b2:corpus/SOURCES.md`, mirror/pin/receipts/sources/validate at 4b8c730,
then the append) → `8/8` (`run_checks` given the clone's own base sha).

FINDINGS:

**F1 — [medium] declared anchor heading is truncated at the first ` (` and only its prefix is checked.**
`c57_quote_truth.py:363` `row[5].split("§", 1)[1].split(" (")[0]`.
Input (scratch clone, landed + validated registry copies): S421 anchor cell
`§ 一、了解死链 (附注：页面并未印出) (发布日期 2022-09-09)` → `8/8 met=True EXIT=0`; S422 `§ 死链处理更及时 (虚构副标题) (发布日期 2016-06-30)` → same.
The declared heading `一、了解死链 (附注：页面并未印出)` occurs nowhere in S421 (`text.count == 0`) yet the check passes on
the 4-unit prefix `一、了解死链` (page-unique, in a text node). *confirmed by running* (fixtures `/tmp/c3rev-w2d5esg4`, `/tmp/c3rev-lhethwlp`).
Fix: parse the cell structurally, not by prefix —
`m = re.match(r"^§\s*(.*?)\s*\(发布日期[：: ]\s*\d{4}-\d{2}-\d{2}\)\s*$", row[5])`, use `m.group(1)` whole, and fail when the
cell does not match that shape. Port a fixture whose heading contains " (" and is absent from the page.

**F2 — [medium] C8 reads an unreadable base revision as "mirror differs", i.e. not-met instead of unevaluable.**
`c57_quote_truth.py:527-528` `if base_registry is None or base_registry != mirror_text:` → note `"mirror bytes differ from the base-revision registry"`.
Input: `--root /tmp/tmp.44zia6rfBl --revision <that clone's tip>` — a clone built from the real blobs but whose history does
not contain `28fa0b2` (any shallow clone, fixture, or exported mirror) → `C8 FAIL`, `EXIT=1`. *confirmed by running* (RC=1).
The contract's kill rule reserves exit 2 for unevaluable evidence; "the base revision is not in this repo" is exactly that.
Contributing: line 1347 calls `run_checks(args.root, args.revision)` and drops the function's `base_rev` parameter, so the CLI
cannot name a base at all — only the selftest (line 1300) reaches it.
Fix: `if base_registry is None: return unevaluable("C8_mirror_bytes", f"base revision {base_rev} is not readable in {root}")`
and add `--base` (default `BASE_REV`) passed through at line 1347.

**F3 — [medium-low] argparse usage errors exit 2, not 64.**
`c57_quote_truth.py:1337` `args = ap.parse_args()`. Input: `--revisionn x` → stderr usage, **RC=2**, indistinguishable from
the unevaluable code. *confirmed by running*. (The hand-written usage path at 1341-1342 does return 64.)
Fix: `class _P(argparse.ArgumentParser): def error(self, msg): print(..., file=sys.stderr); raise SystemExit(64)`.

**F4 — [low] the Gate-line loop does not check every span, contrary to the version-2 declaration.**
`c57_quote_truth.py:395` `allq = [q for q in re.findall(...) if not (units(q) < 2 and len(q) < 12)]`; contract § Counter
versions (C3 v2): "every Gate-line span (not only 6+ units) is checked against both ceilings".
Input: append ` "QQQ" "ZZZ"` to the S421 Gate line (two spans that are not substrings of S421) → `8/8 met=True`. *confirmed by running*
(`/tmp/c3rev-so49yycg`). A 1-unit span of ≥12 chars is checked, so the hole is narrow, but the declared rule is "every".
Fix: for Gate lines use `allq = re.findall(r'"([^"]+)"', line)` (no unit filter) and keep the declared 2+-unit rule for entries only.

**F5 — [low] `--json` labels the run as claim C2, version 1.**
`c57_quote_truth.py:1351` `"schema": "kake-r57-c2-quote-truth-v1"`; intended `kake-r57-c3-quote-truth-v2`.
Provenance in the generator: `derive_c57_quote_truth.py:131` looks for `"schema": "kake-r56-c2-quote-truth-v2"` while the
round-56 source carries `…-v1`, so the guarded `sub(...) if … in body else None` silently no-ops; and line 213 replaces
`kake-r57-c2-quote-truth-v1` **before** the `kake-r56-` → `kake-r57-` rewrite (line 222), so it can never match.
*confirmed by running* the full two-script chain in a scratch dir: output is byte-identical to the committed counter
(sha256 `7aa66297…`), i.e. the pipeline really emits the mislabel; `--json` at 4b8c730 prints that string.
Fix: move the schema replacement after line 222 (`body.replace('"schema": "kake-r57-c2-quote-truth-v1"', '"schema": "kake-r57-c3-quote-truth-v2"')` at the end of derive), drop the dead line-131 edit, regenerate, re-run the selftest.

**F6 — [low] `--json` emits no `EXIT=` line, so a `--json` capture cannot serve as the C3 receipt.**
`c57_quote_truth.py:1349-1356` returns straight after `json.dumps`; the text form prints `EXIT={code}` (line 1362).
Round C1 version 2 requires the `after-c3` receipt body to carry `EXIT=0`. *confirmed by running*: `--json` at 4b8c730 → RC 0,
zero occurrences of `EXIT=`.
Fix: print `EXIT={code}` on stdout after the JSON object, or state in the docstring that receipts must use the text form and have the C1 body check accept the JSON shape.

**F7 — [low] the S421 block still holds the promo explainer, which the docstring and the contract say it excludes.**
`c57_quote_truth.py:96` `ARTICLE_END = {"S421": "往期回顾", …}` ends the window after `<hr><h3>——什么是【搜索问答剧场】？</h3>` and
its body paragraph. *confirmed by running*: `in_content(t421, '【搜索问答剧场】是资源平台基于资源平台工具相关', 'S421')` → True, and the
heading `——什么是【搜索问答剧场】？` → True; the module docstring (lines 5-6) claims "no sidebar, no promo" and the contract says "S421's
block ending at the promo block". A quote of the column's self-description therefore counts as article text.
Fix: `ARTICLE_END["S421"] = "——什么是【搜索问答剧场】"` (the promo heading) or strike "no promo" from the docstring; if the end marker changes, re-check the `.files` fixture set.

**F8 — [low] the "Article block" docstring describes v1 locators, not the code's.**
`c57_quote_truth.py:39-41`: "from the page's `class="article-info"` (S421) or `class="zz_dldes_content` (S422) container to the
page footer (`class="footer"`)". Code (95-96) uses `info-item-time` → `wiki-foot-right` for S422. The same stale sentence is in
the generator output, so the v2 locator edit never reached the prose a reviewer models the block from.
Fix: rebuild that paragraph from `ARTICLE_START`/`ARTICLE_END` and regenerate.

**F9 — [low] the row's date form and the page's date form are checked by different rules.**
`c57_quote_truth.py:353` accepts `发布日期[：: ]\s*(\d{4}-\d{2}-\d{2})`; line 356 then demands the page print `发布日期：{date}`.
Runs: `发布日期: 2022-09-09`, `发布日期  2022-09-09`, `发布日期 2022-09-091` (→ `2022-09-09`, no right boundary) all match the row
regex; `发布日期2022-09-09` does not. Unit probes of the page side: `in_content('<p class="article-info">发布日期: 2022-09-09</p>x往期回顾', '发布日期：2022-09-09', 'S421')` → False; the same date split by an inline `<span>` → False; the fullwidth form → True.
On the two retained bodies the fullwidth form holds (both pages print `发布日期：`), so today's claim is unaffected; a page
printing another form yields a false failure and a row may declare a form the page never prints. *confirmed by running* (unit probes).
Fix: build the page-side needle from the matched separator (`f"发布日期{sep}{date}"`), accept a text node split by inline tags,
and add `(?!\d)` after the day group.

**F10 — [low] an unevaluable run prints `met=False`.**
`c57_quote_truth.py:1358` `print(f"C3 quote-truth {passed}/8 met={code == 0} …")`. Input: the receipts-JSON-corrupt fixture
(`bad_receipts`) → `C3 quote-truth 5/8 met=False`, `EXIT=2`. *confirmed by running*. A reader (or a report line copied from it)
then reads "not met" for evidence that was never evaluated.
Fix: print `met=unevaluable` (or omit `met=`) when `code == 2`.

**F11 — [low] undecodable evidence is reported as absent (exit 1), not unevaluable (exit 2).**
`c57_quote_truth.py:109-117` `show()` returns `None` on `UnicodeDecodeError`, and the callers phrase `None` as absence.
Input: entry bytes `b'\xff\xfe not utf8 \x80'` at the measured revision → `C1 … absent at the measured revision`, RC=1. *confirmed by running*
(`/tmp/c3rev-jfg4b842`). Fix: distinguish a missing blob (`git show` rc≠0) from an undecodable blob and return `unevaluable` for the latter.

**F12 — [low] `content_window` reads an end marker inside the start tag as the block end.**
`c57_quote_truth.py:172-173` `hi = text.find(ARTICLE_END[sid], lo + 1)`; `return (lo, hi) if hi > lo else None` (the `hi > lo`
test is dead: `find(…, lo+1)` yields −1 or ≥ lo+1). Input: `'<div class="article-info" data-nav="往期回顾">正文</div> 往期回顾'`
→ window `(5, 36)` = `class="article-info" data-nav="`; every quote is then rejected with "sits outside the page's content block"
instead of a structural diagnosis. *confirmed by running*. (For the two real bodies the first `wiki-foot-right` sits before the
start and the intended one is chosen — checked by position dump.) Fix: `hi = text.find(ARTICLE_END[sid], text.find(">", lo) + 1)`;
if the window yields no text node, emit a structural note (unevaluable where the body is pinned).

**F13 — [nit] dead/redundant checks.** `c57_quote_truth.py:400-401` (`for q in spans: if not 6 <= units(q) <= UNIT_CEILING`) can
never fire, `spans` is already ≥ 6 (395-396); and the entry filter at 418 (`units < 2 and len < 12`) is narrower than the module
docstring's "every double-quoted span of 2+ units". Fix: delete the loop; reword the docstring to "2+ units or 12+ characters".

NO-DEFECT CHECKS:

- Generated-vs-intended regex (the assignment's escaping question): `derive_c57_quote_truth.py:157` writes
  `re.sub(r"(?is)<(style|script)\b.*?</\1>", "<>", …)` and the generated line 182 compiles to exactly
  `'(?is)<(style|script)\\b.*?</\\1>'`; the doubled backslashes in the generator's non-raw `'''…'''` are correct. Behaviour probed:
  `<script>var s="<p>假</p>";</script>` body is not text; `<scriptx>脚本外</scriptx>` is left as text (correct `\b`); the real
  S422 window's `<style>@font-face…</style>` produces no `@font-face` / `宋体` / `font-family` text node. *ran.*
- Bodies are not fixture-only: the article-block code passes on the landed pages — S421 window `(9346, 20418)` with 150 text
  nodes, S422 `(9199, 12939)` with 64; `<script` count in both windows is 0; the single `<style>` (S422) closes inside the window;
  S422's header `wiki-foot-right` at 9102 is correctly skipped in favour of 12939. *ran.*
- sha256 pin (bytes vs decoded text): C5 (347) and C6 (460) both hash the raw `git show` bytes; the digests equal
  `sources/receipts.json` and the blobs at the contract commit `b9a5d012` (`32eaf8b7…`, `7cf2e27d…`) — verified with
  `git show b9a5d012:.ufo/waves/round-57/sources/{S421,S422}.html | sha256sum`. A byte-level re-encode would fail closed. C8
  hashes the decoded mirror re-encoded (548); for strict-UTF-8 input the round-trip is byte-identical, so no behavioural
  difference, only a style inconsistency. *ran.*
- Entities: raw `&nbsp;` is text and accepted (`in_content(S421, '为什么要及时处理死链&nbsp;？')` → True); the decoded NBSP form is
  rejected → False. Matches the contract's "entities stay as written". *ran.*
- Exit codes exercised: no `--revision` → 64; unresolvable revision → 2 with `EXIT=2` on stdout; met → 0; not-met → 1;
  corrupt receipts JSON → 2 (C6 unevaluable). *ran.*
- Fault containment: `except Exception` at 576-579 turns any in-check exception into exit 2; malformed receipts JSON and
  malformed `mirror-pin.json` both route to `unevaluable` rather than a traceback. *ran.*
- Selftest: `KAKE_R57_SELFTEST_REV=4b8c730… c57_quote_truth.py --selftest` → `101/101 … baseline conditions 8/8, 89 fixtures in
  the kill matrix` (4.93 s). *ran.* Its fixture quotes are faithful: every quoted span in `_FX_ENTRY` is a raw substring of its
  own retained body, and the two Gate quotes are 9 and 12 units. *ran.*
- Reproducibility: running `derive_c57_quote_truth.py` then `derive_c57_selftest.py` in a scratch copy (with
  `w1/ExecC3Selftest.files/c57_quote_truth_selftest.py`) reproduces the committed counter byte for byte (sha256 `7aa66297…`).
  The one-script-alone run differs only by the selftest block (by design: version 1 ships a stub) — so the "generated" claim holds,
  and F5 is a generator bug, not a hand edit.
- C7 receipt parsing: `--file` present, `--root` absent, `sources-census.sh` named, `exit=0`, last line `file\tok\t<registry>`,
  scratch registry and entries byte-equal to the landed ones — all pass on the scratch clone of 4b8c730. *ran.*
- No credential material, session token, `op://` reference or private URL appears in the counter, the retained bodies or
  `receipts.json`; the two URLs are the public `ziyuan.baidu.com` pages the contract names.

Residual risk / gaps: F1, F4-F12 are latent (no current landed quote or row triggers them); F2 and F3 mis-price the exit code a
caller reads, F5/F6 mislabel and truncate the machine-readable form a receipt could be built from. I did not run the C1 or C2
counters, did not run the census/validate tool, and did not measure any quote's *support* for its sentence (out of scope).

VERDICT: version 2's core is sound — the generated regex, the byte-pinned bodies, the text-node doctrine and all 101 selftest
fixtures reproduce and hold — but the anchor check verifies only a truncated prefix (F1) and three interface paths misreport
(base-revision unevaluable as mismatch F2; argparse usage as 2 F3; `--json` as C2/v1 without `EXIT=` F5/F6), so C5's anchor
condition and the counter's exit-code contract are not yet trustworthy as written.
