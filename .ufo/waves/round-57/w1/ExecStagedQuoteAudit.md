# ExecStagedQuoteAudit

W1 audit of the two staged package candidates (`merge/kake/`, shokuknow, read-only) against the retained round-57
bodies. Nothing in shokuknow, the fleet repo, lane jj state or the lane Git index was modified; no git/jj command ran.

SCRIPT:
- `.ufo/waves/round-57/w1/ExecStagedQuoteAudit.files/staged_quote_audit.py` (new, read-only; two modes)
  - `python3 -B …/staged_quote_audit.py` — quoted spans, recheck `grep -F` strings, `source:` labels.
  - `python3 -B …/staged_quote_audit.py --rows` — staged `SOURCES.append.md` rows + the maintained census parser.
  - Unit rule = the counters' `units()`; content block = `c57_quote_truth.py`'s `content_window()`
    (`class="article-info"`/`class="zz_dldes_content` → `class="footer"`); page-unique = 1 occurrence in its own body
    and 0 in the other adopted body.
- Transcripts (same dir): `quote-audit.txt` (25 lines, exit 0), `rows-audit.txt` (40 lines, exit 0).
- Grounding: `sha256sum`/`wc -c` on the retained bodies reproduce `sources/receipts.json` exactly
  (S421 `32eaf8b7…7182`, 34 750 B; S422 `7cf2e27d…71ff`, 27 327 B), so substring tests ran over the receipted bytes.
- Tooling: nothing installed or upgraded (no install needed).

RESULTS:

Entry 1 = staged S403 `baidu-dead-link-taxonomy.md` → body S421; entry 2 = staged S408
`baidu-spider3-dead-link-recognition.md` → body S422.

| item | page | units | chars | raw substr | in content | page-unique | >25u | >40ch | grep -F -c |
|---|---|---|---|---|---|---|---|---|---|
| entry 1: every ASCII double-quoted span ≥2u | S421 | — | — | — | — | — | 0 | 0 | — |
| entry 2: every ASCII double-quoted span ≥2u | S422 | — | — | — | — | — | 0 | 0 | — |
| entry 1 recheck `grep -F` string | S421 | 29 | 31 | yes | yes | yes | **YES** | no | **1** |
| entry 2 recheck `grep -F` string | S422 | 37 | 40 | yes | yes | yes | **YES** | no | **1** |
| entry 1 `source:` label (full, incl. `§ `) | S421 | 16 | 25 | **no** | no | no | no | no | — |
| entry 1 label piece `一、了解死链` | S421 | 5 | 6 | yes | yes | yes | no | no | — |
| entry 1 label piece `1、死链都有哪些类型？ A：` | S421 | 9 | 14 | **no** | no | no | no | no | — |
| entry 1 label piece `1、死链都有哪些类型？` | S421 | 8 | 11 | yes | yes | yes | no | no | — |
| entry 1 label piece `A：` | S421 | 1 | 2 | yes | yes | **no (10×)** | no | no | — |
| entry 2 `source:` label (full, incl. `§ `) | S422 | 6 | 38 | **no** | no | no | no | no | — |
| entry 2 row-anchor heading `死链处理更及时` | S422 | 7 | 7 | yes | yes | yes | no | no | — |

- **Zero double-quoted spans exist in either staged entry** (ASCII `"` count = 0, curly `“”` count = 0, 2 backticks each
  = the recheck command only). There is therefore nothing to test for the per-span rules, and the only verbatim page text
  the staged package carries is the two `recheck` patterns — both over the 25-unit quote ceiling (29u / 37u; 31 / 40 chars).
- Both recheck patterns are raw substrings, inside the article block and page-unique; the `grep -F -c` half of each staged
  command was **run** against the retained body and prints `1`, matching the staged claim. The `curl` half was **not run**
  (no network fetch; the retained body is the local stand-in).
- Label failures, exactly: the `→` in the S403 label is editorial (the page writes `<h2>一、了解死链</h2>` then
  `<h3>1、死链都有哪些类型？</h3>`; body contains `→` 0× and `§` 0×), and `？ A：` with a space is not a raw substring
  (`A：` starts the next paragraph, `</h3><p …>A：`). `A：` alone occurs 10× in S421, so it is not page-unique either.
  The S408 label is English prose describing the section ("the article body's dead-link section"), 0 hits; the page text
  it means, `死链处理更及时`, is unique and would pass.
- Date drift: both staged entries say `fetched 2026-10-24` / `verified-at: 2026-10-24` and the recheck says
  `(ran 2026-10-24)`, but the retained bodies are receipted `fetchedAt 2026-10-25T23:38Z`. A `ran 2026-10-24` recheck
  cannot be a run over these bodies.

STAGED ROWS:

`SOURCES.append.md` line 123 = S403, line 128 = S408. Both rows: 12 cells, not 11 — one escaped `\|` inside the recheck
cell (`curl … \| grep -F -c …`), and the maintained parser splits on every `|` with no unescaping
(`gawk -F'|'`, `sources-census.sh` `row_pass`), so `gawk NF = 14` where the contract wants 13.

| check | S403 | S408 |
|---|---|---|
| cells (`split('\|')`) | 12 (want 11) | 12 (want 11) |
| escaped pipes in row | 1 | 1 |
| recheck prose (not `NNd`) | yes (`180d — \`curl…\` -> 1 (ran …)`) | yes (same shape) |
| anchor cell | `§ 一、了解死链 → 1、死链都有哪些类型？ A： (发布日期 2022-09-09)` | `§ the article body's dead-link section (the passage headed 死链处理更及时) (发布日期 2016-06-30)` |
| opened | 2026-10-24 | 2026-10-24 |
| used-by | `corpus/knowledge/baidu-dead-link-taxonomy.md` | `corpus/knowledge/baidu-spider3-dead-link-recognition.md` |

Maintained census parser, `validate --today 2026-10-25 --file <scratch>/corpus/SOURCES.md` (scratch `mktemp -d`, both
rows as-is, used-by targets present): **exit 1** —
`file E01 S403 fields=12`, `file E01 S408 fields=12`, plus two spurious
`E11 … missing used-by grep -F -c '<pattern>'\` -> 1 (ran 2026-10-24)` — the escaped pipe shifts the columns, so the
parser reads the recheck tail as used-by and drops the real used-by cell.
Control (identical rows with `\|` → `/`, nothing else changed): **exit 1**, `E09 S403 recheck=180d — \`curl …`,
`E09 S408 recheck=180d — \`curl …` — i.e. the prose recheck fails E09 on its own; E01 merely masks it in the as-is run.

`c57_quote_truth.py` C5 clauses emulated on the staged rows (title / anchor heading / printed date):

| row → lane | title in body | anchor heading in body | `发布日期：<date>` in body | opened = 2026-10-25 |
|---|---|---|---|---|
| S403 → S421 | **FAIL** (`搜索问答剧场【六】“死链”常见问题解析` 0×; body has `搜索问答剧场 【六】…`, a space after 剧场) | **FAIL** (`一、了解死链 → 1、死链都有哪些类型？ A：` 0×) | PASS (1×) | **FAIL** |
| S408 → S422 | PASS (2×) | **FAIL** (`the article body's dead-link section` 0×) | PASS (1×) | **FAIL** |

Both rows also name the staged filenames in used-by; the lane refuses those names (contract C1 maps them to
`baidu-dead-link-types.md` / `baidu-spider3-dead-link-model.md`), so the used-by cell is wrong for a lane append even
after the pipe repair.

SUMMARY:

- Spans tested: **0** (neither staged entry contains a single ASCII double-quoted span; 0 curly quotes).
- Over-ceiling: **0 of 0 quoted spans**; the only verbatim page text in the package is the two recheck patterns, both
  over the 25-unit ceiling (29u, 37u) — 2 of 2 verbatim strings exceed it, 0 exceed 40 characters.
- Non-substring: **0 of 0 quoted spans**; non-substring among the label/recheck items tested: **2** (both full `source:`
  labels) plus 1 label piece (`1、死链都有哪些类型？ A：`).
- Labels with 0 hits: **2 of 2** (`S403` full label, `S408` full label); both rows' C5 anchor headings also 0 hits.
- Recheck greps: **2 run, both print 1** (S421, S422) — the staged counts are true.
- Staged rows fail the maintained census parser as-is on **both** rows (E01 fields=12, and a column-shifted E11), and
  fail E09 once the pipe is repaired; both also fail the round-57 `opened` date and the lane's filename mapping.

VERDICT: 0 quoted spans in either staged entry (nothing over ceiling, nothing non-substring); both full `source:` labels
have 0 hits (`→`/` A：` and English prose are not page text); both recheck greps truly print 1; both staged rows fail the
census parser as-is (12 cells, escaped pipe → E01 + shifted E11; E09 after repair).
