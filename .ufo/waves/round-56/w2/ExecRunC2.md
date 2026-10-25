# ExecRunC2

Seat ExecRunC2, round-56 W2 falsify, lane kake-shokunin. Attacks C2 as measured. All runs in my own clone
`D=$(mktemp -d)` → `/tmp/tmp.DNBDbgDZO8`, `git clone -q --no-checkout <lane> $D && git -C $D checkout -q a450e43e696d032e3ac308383f6b3394e0c92860`;
`git -C $D rev-parse HEAD` = `a450e43e696d032e3ac308383f6b3394e0c92860`, `rev-parse --show-toplevel` = `/tmp/tmp.DNBDbgDZO8`.
`git merge-base --is-ancestor e48354b… a450e43…` → true. Lane tip at run time was `7ad7db51…` (not mutated by me).

## COUNTER RUNS:

Command (all three runs, from `$D`):
`python3 -B .ufo/waves/round-56/c56_quote_truth.py --root $D --revision a450e43e696d032e3ac308383f6b3394e0c92860 [--json]`

- RUN1: exit **0**. `C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)`; C1_entries_exist, C2_entry_provenance,
  C3_row_shape, C4_used_by, C5_quote_truth, C6_receipt_pins, C7_validate_before_append, C8_mirror_bytes all `PASS`;
  `revision: a450e43…`, trailing `EXIT=0` line.
- RUN2: exit **0**, byte-identical to RUN1 (`diff` empty → `IDENTICAL`).
- RUN3 `--json`: exit **0**; `conditions_passed: 8`, `exit: 0`, `met: true`, `schema kake-r56-c2-quote-truth-v1`; facts
  `C1 entries:3`, `C3 rows:158 base_rows:156`, `C6 receipts:6`, `C8 registry_rows:158`; no `notes` entries anywhere.
- Determinism: two plain runs byte-equal; the JSON run agrees on all eight `passed:true` states. Wall time 1.8 s for all three
  (no 40–130 s cost on this claim; that cost is C1).
- No tree pollution: `git -C $D status --porcelain` empty after six counter runs (the counter works from temp dirs).
- Do-nothing control, re-run by me: same command with `--revision e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6` → exit **1**,
  `0/8 met=False`, all eight conditions FAIL, output **byte-identical** to the committed `controls/base-c2-quote-truth.txt`
  (`diff` empty). The counter therefore discriminates base from tip on the measured revision, not by reading the working tree.

## RECOUNT:

Counter-free; my own python (`/tmp/c2recount.py`, does not import `c56_quote_truth`), plus shell.

(a) three entries exist — all present at the measured revision:
`corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md` 7835 B; `yahoo-japan-deleted-url-recrawl.md` 7346 B;
`yahoo-japan-nonexistent-url-recrawl.md` 7037 B. Result `exists=True` for each.

(b) registry rows, exactly the assigned pipeline:
`git show a450e43…:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → **158**
`git show e48354b…:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → **156**
(independent row parser over the same blobs: base 156, tip 158).

(c) base→tip registry diff is exactly S367 changed (used-by only) + S419/S420 added:
`git diff --stat e48354b… a450e43… -- corpus/SOURCES.md` → `1 file changed, 3 insertions(+), 1 deletion(-)`;
`git diff -U0` line classes: 1 removed line = the `S367` row, 3 added lines = `S367`, `S419`, `S420`. No other registry line
touched. Cell-level compare of the parsed rows: `added=['S419','S420'] removed=[] changed=['S367']`; S367 differing cells =
`['used-by']`; base `used-by` = `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`, tip = same **plus**
`, corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md` (base value is a prefix; added suffix is exactly the new
entry). S419/S420 absent from the base registry, 11 cells each at tip.

(d) retained bodies match `receipts.json` (sha256 and bytes):
S367 8051 B / `0188de9dae01e9088231098a9c6af3c8f5dc62a5982419a5f82fd98e86772a19`; S419 7428 B / `6172d5d108d0c31d25244659516fc7fc81472c924ef35a51afc964cdd3a4a5c8`;
S420 7332 B / `a860d4f33181302d7ab467f5a0b21f2008916bb6dc6def69e69df5b54c630209` — `match=True` for all three.
Extra, outside the assigned list: I re-fetched all three live URLs myself today (`curl -fsSL --compressed -A
kake-shokunin-round56`, HTTP 200 each) and got **byte-identical sha256/byte counts** to the receipts, so C6 is no longer only
receipt-shaped at this measurement moment. Mirror/validate receipts also hold: pre-append mirror `cc402e4b…` = `mirror-pin.json`
= `git show base:corpus/SOURCES.md`; `validate/corpus/SOURCES.md` = landed `corpus/SOURCES.md` (`483b5d13…`); census argv
`--file …/validate/corpus/SOURCES.md`, exit 0, stderr empty, 0 `E03`/`E04`, last stdout line `file\tok\t…/validate/corpus/SOURCES.md`.

(e) every double-quoted span of 2+ units is a raw substring of its row's body: S367 17 spans, S419 14, S420 12; **0 non-substring**
(`substr=True` on every one). All spans occur exactly once in their own body except S420 `を行ってください` (2). Under the
counter's `CJK_RE` the maxima are 24/23/24 units and 34/37/26 characters — inside both ceilings (25 units, 40 chars). Result
`OK a=True c=True d=True e=True`, exit 0.

## DISAGREEMENTS:

1. **S419 entry prose undercounts its own cross-body overlap** — `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md`, section
   `## Quote classes` ("Four spans also occur on the sibling S420 body — …"). Measured against `sources/S420.html`: **six** of
   S419's 14 spans of 2+ units occur there — the four named plus `HTTP 200 OK` (3 units) and `HTTP 404 Not Found` (4 units).
   The count should read six. Not a predicate break: C5 needs ≥3 distinct page-unique spans and S419 has 8, and the four it
   names are indeed non-unique across the three adopted bodies. S420's symmetric sentence ("Four spans … the other eight are
   page-unique") is exact — confirmed independently here and by `w2/ExecQuoteRecountS420.md:75-78`.
2. **Unit-rule reading differs between my strict count and the counter's regex** (ceiling not breached either way). The frozen
   rule is "one unit per CJK character"; `CJK_RE` in `c56_quote_truth.py:97` and `span_tools.py:18` is
   `[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]`, so CJK punctuation U+3000–U+303F
   (`「」、。`) costs 0. Counting those as CJK characters, S367's `ウェブページ自身のインデックスへの登録も拒否する」` is **25**
   units and S420's `存在しないウェブページを表示しようとしたときには、` is **25**, versus 24 under the counter. Both are ≤25, so
   the predicate and the Gate ceiling stand; the lesson's "re-cut … pieces of at most 24 units" (`corpus/lessons/round-56.md`,
   `## Gate`) holds only under the counter's regex.
3. **Control shape, recorded so the base receipt is not misread** — `c56_quote_truth.py` does not exist at the base revision
   (added in `2d308e8`); a clone checked out at `e48354b…` cannot run it (my attempt exited 2, `can't open file`). The
   committed base control is `--revision e48354b…` from a later root, which I reproduced byte-identically. The control proves
   condition discrimination, not that a base checkout ships the counter.
4. Nothing else diverged: all eight conditions reproduce from my own recount, and the entry-level factual assertions I sampled
   hold against the bodies — S367 `個別リンクURL` count 1 and outside the article block (`offset 3348 > <h2 2499`), `002851.php`
   link present, `X-Robots-Tag: NOFOLLOW` and both meta examples printed as the entry shows, head description naming the HTTP
   header; S420 `ユーザーエージェント` count 1 in a sidebar link to `002855.php`.

VERDICT: C2 reproduces at `a450e43e696d032e3ac308383f6b3394e0c92860` — 8/8 met=True exit 0 twice (byte-identical) and once under `--json`, base control 0/8 exit 1 byte-identical to the committed receipt, recount (a)–(e) all true; one non-predicate prose defect (S419 says four shared spans where six occur).
