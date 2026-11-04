# ScribeKnowledge — kake round 80, wave w1

**Verdict:** all three corpus drafts delivered and quote-verified; both sources opened by this seat (HTTP 200, byte-identical to the pair `ScoutSources` landed one minute later); the C1 `R79-1` conjunct that was unsatisfiable at the freeze bytes now closes against the corrected counter at HEAD `de65ec21` — my row, draft entry and a lesson stub give `(True, 'S453 = RFC 9110 row present, used-by resolves …')`, and the counter's own `--selftest` prints `selftest: 3/3 passed`, exit 0.

## Delivered (under `.ufo/waves/round-80/w1/ScribeKnowledge/`)

| file | sha256 | notes |
|---|---|---|
| `row-S453.md` | `4ad25c6d7d35b67d10a4b0f434840dc87fa6d75bb16de88f835bbf682dd04f7a` | one 11-cell registry row, no `|` inside any cell, `row_shape` returns `''` |
| `knowledge-http-date-grammar.md` | `423d691a0781055bf52110295accfcb9bcd7fb12584a09c286f57f0da0cd0106` | provenance trio first, three ABNF shapes, comma placement, amendment-1 terms, five `[INFERENCE]` marks, limits |
| `gate-quote.md` | `e50c558e6a8883486ec5f84a619bafdbd0595663255d12ae7807325853a01567` | URL + access date + `file:line` + ≤25-word quote per row (S453 row and S452 re-open) |
| `verify_quotes.py`, `quote-receipts.json` | script `fce23784…`, receipt `658c8551…` | 19/19 quotes located; row check |
| `sources-receipts.json` | `b1fb172b…` | both GETs: status, bytes, sha256, fetched-at, cross-check |
| `r79-1-counter-probe.txt` | `6d593d1f…` | freeze-vs-HEAD counter probe and selftest output |
| `rfc9110.txt`, `mdn-x-robots-tag.raw`, `mdn-x-robots-tag.txt` | `21c1cdce…47232a`, `c4216ffb…7aaf38`, `8be2a406…82556e` | retained bytes the quotes were checked against |
| `rfc-sweep.txt`, `scout-status.txt` | `70ab1dd0…`, `daca87d3…` | negative sweeps; scout-availability timeline |

## Sources opened (one GET each, this seat)

| source | status | bytes | sha256 | fetched (UTC) |
|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9110.txt` (final URL identical) | 200 | 502,941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 2026-11-04T10:45:05Z |
| `https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Robots-Tag` (final URL identical) | 200 | 218,816 | `c4216ffb7aa934e309329d3b5adf1e62557464eebcbaab0bb33b60a72b7aaf38` | 2026-11-04T10:45:12Z |

`ScoutSources` was empty when I started (`ScoutSources.md` not found; `ScoutSources/` empty at 10:44Z) and landed at 10:46-10:47Z, mid-run. Cross-check after the fact: both raw bodies are byte-identical to the scout's (`sources-receipts.json`), and the RFC bytes match the document the lane already registers as S028 (`corpus/SOURCES.md:36`). The MDN tag-strip differs by pipeline only: my 302-line strip is byte-identical to `.ufo/waves/round-79/sources/S452-mdn-x-robots-tag.txt`, so `S452:209/:212/:239` keep the round-79 numbering; the scout's 677-line strip numbers them `:211/:214/:243`. The entry cites the round-79 numbering and names the scout numbering for the clean-punctuation sentence.

## Findings

1. **R79-1 was unsatisfiable at the freeze, and that is now fixed.** At `f20163c1` (`c80_defect_queue.py:124`, sha256 `90649c08…b26538`) the counter read `used = row[11]` on an 11-cell row, so `used-by` was always empty; a 12-cell row that populates index 11 is rejected by `row_shape`. Probe: freeze bytes return `(False, 'S453 used-by resolves to no file that cites S453')`; HEAD `de65ec21` (`used = row[10]`, sha256 `ccb05318…522a32`) returns `(True, 'S453 = RFC 9110 row present, used-by resolves (corpus/knowledge/http-date-grammar.md), row shape ok, erratum recorded')`; a 12-cell row still returns the shape failure (`r79-1-counter-probe.txt`). The fix is the L1's `amendments/amendment-2.md` (10:47Z) + commit `de65ec21` (10:48:18Z); `--selftest` prints `selftest: 3/3 passed`, exit 0. My probe at 10:46:54Z and `ScoutSources.md` §7 are two independent sightings of the same freeze defect; amendment 2 credits the scout and does not mention this seat.
2. **The base control survives the fix.** At the base revision R79-1 returns at the earlier `no S453 row` branch, before the `used-by` line (amendment 2 says this; the base receipt line `R79-1 open no S453 row` is unchanged) — so `open=6 met=false` is not an artefact of the buggy index.
3. **The carrier moved while this seat ran.** `corpus/SOURCES.md:200` now carries an integrated S453 row and `corpus/knowledge/http-date-grammar.md` exists (7,890 B, sha256 `4b819585…42f7f`, mtime 07:49 −0300) — neither written by me. Checked against the counter: landed row is 11 cells, `shape=''`, `used-by` resolves to the landed entry and it cites `S453`. `corpus/lessons/round-80.md` is still absent, so R79-1 remains open until the lesson conjunct lands. My draft differs from the landed pair in the section range (mine `1836-1937`, landed `1836-1925`; `5.6.7` ends at line 1937, next header `6.  Message Abstraction` at 1939) and in quoting MDN's clean-punctuation sentence from the scout strip; the L1 should keep one.
4. **S452's vocabulary is narrower than the case set's.** The page names "RFC 822, RFC 850, or ISO 8601" (`ScoutSources/S452-mdn-x-robots-tag.txt:214`) and never names `asctime` or IMF-fixdate; A2's asctime shape therefore rests on S453 alone. The page also never states that the comma belongs to the date value — it only demonstrates the value (`mdn-x-robots-tag.txt:239`) and defines `,` as the rule separator — so A1 is a lane segmentation rule, not a source statement. RFC 9110 §5.5 says a field definer "ought to" delimit a member that may contain a comma (`rfc9110.txt:1629-1631`), and the RFC never mentions `x-robots-tag` (`grep -ci` → 0, exit 1; control `robots` → 2, exit 0).
5. **A2 widens RFC 9110 by one branch.** The RFC's `date3 = month SP ( 2DIGIT / ( SP 1DIGIT ))` (`rfc9110.txt:1911`) admits `Nov 16` and `Nov  6`; A2's prose also admits `Nov 6`. No frozen round-80 case uses that branch (c34 is `Nov  6`, c43 is `Nov 16`), so no oracle byte depends on it. Recorded in the entry's Limits as `[INFERENCE]`.

## Checks run (verbatim outcomes)

- Two `curl -sSL --max-time 45` GETs: `http_code=200`, sizes/hashes as tabled, exit 0 each.
- `python3 -B verify_quotes.py` → `quotes=19 found=19 missing=0`; `row cells=11 shape='' used_by=corpus/knowledge/http-date-grammar.md exists_at_carrier=True draft_cites_S453=True`; exit 0.
- Freeze/HEAD probe → the three predicate lines quoted in finding 1; `python3 -B .ufo/waves/round-80/c80_defect_queue.py --selftest` → `selftest: 3/3 passed`, exit 0.
- RFC sweep → `x-robots-tag` 0 (exit 1), `robots` 2 (exit 0), `unavailable_after` 0 (exit 1) (`rfc-sweep.txt`).
- Withdrawn R79-5 sentence sweep over `SCORECARD.md`, `SKILL.md`, `LOG.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/knowledge/**`: no matching line (the phrase was not repeated by anything I wrote).

## Not done (scope)

No `corpus/` edit, no lesson text, no run of `scripts/x_robots_tag_audit.py`, no counter edit, no commit, no fetch beyond the two source openings. The entry describes amendment terms, not observed tool behaviour; C2 at the carrier is ExecGrammar's and the L1's to measure.

## Housekeeping

No tooling installed or upgraded (host `curl`/`python3`/coreutils only). Scratch lived at `/fast/scratch/hyaku/kake-r80/ScribeKnowledge/` and was removed with `rm -rf` (rc 0, `test -e` → absent) after the retained copies were made; a second one-shot probe tree under the same path was removed the same way. Files written: `.ufo/waves/round-80/w1/ScribeKnowledge/**` and this report only.
