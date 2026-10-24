# Attack — round-45 lesson Gate table (quotes, locations, labels, retained bytes)

Seat: `kake-r45.AttackGateQuotes` (wave 2, reviewer; axes: freshness, operability).
Target: `corpus/lessons/round-45.md` §Gate (lines 3-14 at HEAD `e545525`), rows
S133 (line 12), S134 (line 13), and the unlabeled candidate row (line 14).
Lane tree read-only; the only lane file written is this report. All scratch
writes are under `/fast/scratch/hyaku/kake-r45/AttackGateQuotes/`.

Attack questions, as assigned: (1) each S133/S134 row carries a <=25-word quote,
(2) the quote is located by section/paragraph, (3) each row is labeled, (4) the
access date is 2026-10-24, (5) the quote occurs in the retained bytes, and
(6) the round-34 `gate_reject_check.py` run **unmodified** over a scratch copy
holding the table still finds the reject.

## Decisive results

| Attack | S133 | S134 |
|---|---|---|
| quote <=25 words | **PASS** — 15 words, row says "15 words" | **PASS** — 14 words, row says "14 words" |
| located section/paragraph | **PASS** — `§Popen Objects` → `subprocess.Popen.returncode`, direct `<p>` 3 of 4 in the entry's `<dd>` | **PASS** — accepted answer id 24139472 (`question_id` 24139389, owner `sth`, `is_accepted` true), first `<p>` |
| per-row label | **PASS** — ID cell `S133` | **PASS** — ID cell `S134` |
| access date 2026-10-24 | **PASS** — present in the Accessed cell; retained mtime `2026-10-24 00:42:33` | **PASS** — present; retained mtime `2026-10-24 00:42:33` |
| quote in retained bytes | **PASS** — exact substring of visible text, whitespace collapsed | **PASS** — exact substring of the retained answer JSON's visible body |

The named attack **does not falsify the S133 or S134 rows**. The exact
`returncode` sentence survives a content re-open today (live page identical in
the quote region; see F2 for the footer-digest caveat). The residual defects I
did find are on the unlabeled candidate row and in the shape/reproducibility
layer (F1-F3); the round-34 check passes with a caveat about what it can prove
(F4).

## Evidence

### 1. Retained bytes and digests (lane, read-only)

```console
$ sha256sum .ufo/waves/round-45/sources/subprocess.html \
            .ufo/waves/round-45/sources/so-answer.json \
            .ufo/waves/round-45/sources/so-question.json
eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd  .ufo/waves/round-45/sources/subprocess.html
702954fd1946cfa2e3895804f48c850acd25a47523a780e1599e7851716ffcd1  .ufo/waves/round-45/sources/so-answer.json
b3fa82dbdb49e626204b635e5c7ca1399dc4603ff07f6e65276de52f49afaae0  .ufo/waves/round-45/sources/so-question.json
```

All three files are `git ls-files`-tracked at HEAD (verified with
`git ls-files .ufo/waves/round-45/sources/`), so quote truth is reproducible
from the commit, not from a dirty working tree.

### 2. S133 quote truth and location (HTML visible text + `<dd>` paragraph index)

Visible text was built with `HTMLParser(convert_charrefs=True)`, tags stripped,
`&nbsp;` mapped to space, whitespace collapsed — the QUALITY.md definition of
"exact after whitespace collapse".

```text
S133 exact-substring-in-normalized-text: True
S133 with U+2212: False
S133 with en-dash: False
wordcount S133 quote: 15
```

Location check with an HTML tree (`bs4`, `lxml`), direct `<p>` children of the
`<dd>` that follows `<dt id="subprocess.Popen.returncode">`:

```text
=== anchor subprocess.Popen.returncode tag dt
direct p count: 4
  p1: 'The child return code. Initially None , returncode is set by a call to the poll() , wait() , or communicate() methods if' ... q_in=False
  p2: 'A None value indicates that the process hadn’t yet terminated at the time of the last method call.' ... q_in=False
  p3: 'A negative value -N indicates that the child was terminated by signal N (POSIX only).' ... q_in=True
  p4: 'When shell=True , the return code reflects the exit status of the shell itself (e.g. /bin/sh ), which may map signals to' ... q_in=False
 nearest section: section popen-objects
 section ancestry: ['popen-objects', 'module-subprocess']
total occurrences of quote in page text: 2
```

The row's "paragraph 3" is the true index (p1 = child return code, p2 = None
half, p3 = the quoted negative-`-N` half, p4 = `shell=True`). The same sentence
also occurs once more under `§Using the subprocess Module` →
`CompletedProcess.returncode` p2 (2 occurrences page-wide); the row names the
`Popen.returncode` occurrence, which exists, so the attribution is valid but not
unique.

### 3. S134 quote truth, location, and reject-reason grounding

```text
answer question_id: 24139389 | question_id: 24139389 | title: Unable to find out what return code of -11 means
answer_id 24139472 accepted True score 27 owner sth
PARA1: 'Return code -11 means "segmentation fault". A negative return code usually means that the process was terminated by a signal. Return code -11 means it was signal 11, which is SIGSEGV.'
quote in para1: True | in body: True
SIGSEGV present: True | -11 present: True
```

The retained answer body is
`<p>Return code -11 means "segmentation fault". A negative return code usually means that the process was terminated by a signal. Return code -11 means it was signal 11, which is SIGSEGV.</p>`
— one paragraph, so "first paragraph" is exact; the quote is a sentence inside
it, not a paraphrase. The reject reason's claim that the answer makes a
`-11 is SIGSEGV` mapping is literally present. The reason's negative half ("the
opened primary does not make") was checked against the retained S133 page:

```console
$ grep -o "SIGSEGV\|signal 11\|segmentation fault" .ufo/waves/round-45/sources/subprocess.html | sort | uniq -c
(no output: zero matches)
```

### 4. Round-34 `gate_reject_check.py`, unmodified, on a scratch copy

Scratch repo built from the committed lesson at HEAD, whole file byte-for-byte
(`git show HEAD:corpus/lessons/round-45.md`), committed in a throwaway repo
(`ed299b9`, 7,269 bytes). The checker was executed from its frozen path with no
edits:

```console
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/criteria/gate_reject_check.py \
    --repo /fast/scratch/hyaku/kake-r45/AttackGateQuotes/repo --rev HEAD \
    --lesson corpus/lessons/round-45.md
MATCH: corpus/lessons/round-45.md:13: | S134 | https://stackoverflow.com/questions/24139389/unable-to-find-out-what-return-code-of-11-means (read via the Stack Exchange API) | accessed 2026-10-24, API read HTTP 200, 723-byte JSON, sha256 `702954fd…716ffcd1` (a plain HTML GET of the same URL answers HTTP 403) | "A negative return code usually means that the process was terminated by a signal." (accepted answer by `sth`, first paragraph; 14 words) | **reject** — the answer's durable point is already carried by the tier-A primary S133, and its `-11 is SIGSEGV` claim is a signal-number mapping the opened primary does not make; flip: a tier-A POSIX or Python `signal` source naming signal 11 as SIGSEGV is opened, and the answer becomes an illustrative examp…
exit=0
```

The match is on line 13 = the S134 row (line map measured from the same file:
`{12: '| S133 |', 13: '| S134 |', 14: '| — (candidate'}`).

Mutation controls on scratch copies only, same unmodified checker:

| Mutant | exit | first line |
|---|---|---|
| unmodified control | **0** | `MATCH: ...round-45.md:13: | S134 | ...` |
| M1: S134 decision replaced by `reject — tier C, kind community, status rejected` | **1** | `NO MATCH: ## Gate has no source decision beginning with reject and a non-empty reason` |
| M2: S134 `**reject**` → `admit` (reason text untouched) | **1** | `NO MATCH: ...` |
| M3: S134 row deleted, S133 + candidate kept | **1** | `NO MATCH: ...` |
| M4: S134 deleted; candidate row relabeled `S999` with a reject + substantive reason | **0** | `MATCH: ...round-45.md:13: | S999 | ...` |

M1-M3 show the pass is attributable to the S134 row's reject decision and a
reason that survives the "status words only" filter (M1). M4 shows the checker's
limit, recorded as F4.

### 5. Word counts and quote delimiters, row by row

```text
12  | S133 |  ascii_spans= 2 ['A negative value -N indicates that the child ', 'exit']  curly= 0
13  | S134 |  ascii_spans= 1 ['A negative return code usually means that the']           curly= 0
14  | — (candid  ascii_spans= 2 ['A negative value -N indicates that the child ', 'Unix only']  curly= 0
```

Per-row count check (`len(quote.split())` against the row's own claim):

```text
S133  actual_words 15  row says "15 words"   PASS
S134  actual_words 14  row says "14 words"   PASS
cand  actual_words 15  row says "(13 words)" FAIL — see F1
```

### 6. Freshness re-open of both sources (live, today)

S133, live `https://docs.python.org/3/library/subprocess.html`:

```text
LIVE subprocess.html HTTP=200 bytes=208624
b4c58392796b5dedeae51c96f051a6f265f196f55041e56072c2c80f43d19355  live-subprocess.html
eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd  .ufo/waves/round-45/sources/subprocess.html
quote in retained visible: True
quote in live visible: True
live version banner: Python 3.15.1 documentation
live last-updated: Last updated on Oct 24, 2026
differing byte count: 3 first 10 offsets: [208371, 208373, 208374]
 retained: '... Last updated on Oct 24, 2026 (00:13 UTC).'
 live    : '... Last updated on Oct 24, 2026 (03:37 UTC).'
quote context equal: True
```

S134, live `https://api.stackexchange.com/2.3/answers/24139472?site=stackoverflow&filter=withbody`:

```text
LIVE answers/24139472 HTTP=200 bytes=723
answer_id retained==live: True
score retained==live: True
is_accepted retained==live: True
body retained==live: True
live owner: sth quote in live visible: True
```

Content is fresh; only the docs footer build time moved (F2).

### 7. The S133 decision cell's factual justification holds

The row justifies the admit with "the v1 driver read `p.returncode` and never
gated on it (`c44_audit.py:54-61`)" and "the round-44 review recorded
`"exit": -9` rows certifying `ok=true`". Both halves check out on committed
bytes:

```text
.ufo/waves/round-44/c44_audit.py:61:    return p.returncode, rec, p.stdout..., p.stderr...
.ufo/waves/round-44/c44_audit.py:155:  code, rec, so, se = run_counter(...)
                                       ... met=(rec or {}).get("met"), exit=code, ...
semantic_witness (63-65): uses row["met"] and row["caughtBy"] only
expectation_ok  (69-83): uses met / error / witnessed only — never "exit"
.ufo/waves/round-44/w2/ReviewCounterContract.md:90-91: "The summary *records*
  `\"exit\": -9` on the control row and all three build rows and still reports
  `\"ok\": true`."
```

The exit code is recorded as `exit` and never consulted by the witness or
expectation predicates, so "read it and never gated on it" is literally true,
and the review sentence the row paraphrases exists at the cited lines.

## Findings, by severity

### F1 — Medium: the unlabeled candidate row fails the Gate table's own shape contract (and its word count is wrong)

`corpus/lessons/round-45.md:14` is a Gate table row that is not a registry row,
has no section/paragraph location, cites no retained bytes, and misstates its
excerpt length.

- Column 4 is `"A negative value -N indicates that the child was terminated by signal N (Unix only)." (13 words)`.
  Actual: **15 words** (identical structure to the S133 quote, which the same
  table counts as 15). The "(13 words)" claim is false by two words.
- The row's only location text is the word count; the header promises
  "Located quote (≤25 words)". No section, paragraph, or even "first paragraph"
  is named (contrast S133/S134).
- The quoted sentence is retained nowhere under `.ufo/waves/round-45/sources/`:
  `git grep -l 5631819 HEAD -- .ufo/waves/round-45/sources/` returns nothing.
  Its only committed support is a transcription in
  `.ufo/waves/round-45/w1/ScribeLessonMistakes.md:275-280` (a report body), which
  is not retained source text under QUALITY.md's Gate-quote bar (exact substring
  of retained visible source whose digest the counter verifies).
- Live re-open shows the text is **not fabricated**: answer 5631819 is score 363,
  `is_accepted` true, owner Eli Bendersky, body contains the passage (HTTP 200,
  1,445-byte JSON, quota_remaining 283). The defect is evidence shape, not
  content.

Severity is Medium rather than High because the row carries no decision and the
round's Gate credit (`reject` for S134) does not depend on it. It is still a
committed quote that no retained byte backs, and a wrong count in the same cell.

### F2 — Low: the S133 retained digest is a footer-timestamp snapshot, not a stable identity for the URL

Live re-fetch is the same size (208,624 bytes) and differs in exactly 3 bytes:
the docs footer build time (`00:13 UTC` retained vs `03:37 UTC` live). The quote
region is byte-identical and the page still reads "Python 3.15.1 documentation".
Consequence: any future re-check that fetches the URL and compares the registry
digest `eceda6f6…e5bdf0dd` will report drift although the quoted passage never
changed. The row is internally correct (it cites the retained path and that
file's digest), but "sha256 next to a URL" invites a live-digest comparison that
cannot pass. S134 is immune: the live answer body/score/accepted are
byte-identical to the retained JSON.

### F3 — Low: excerpts are ASCII-quoted, so the lane's existing quote-shape counters see zero quotes; the S133 line also carries a second quoted span

The landed rows use `"…"` (U+0022). Both existing Gate counters key on curly
quotes: `.ufo/waves/round-28/c2_source_count.py:41`
(`QUOTE_RE = "\u201c([^\u201d]+)\u201d"`) and
`.ufo/waves/round-29/c1_quote_truth.py`
(`QUOTE = re.compile(r"\u201c([^\u201c\u201d]+)\u201d")`). Applied to these rows
the span count is **0**, so a re-used shape check would report "no Gate line with
id, URL, access date and one 1-25 word quote" without ever reading the text.
The scribe's own draft (`.ufo/waves/round-45/drafts/sources-gate.md`) promised
curly quotes for exactly this reason; the landed table lost them. In addition,
under an ASCII-keyed "one quote per Gate line" rule the S133 line has **2** spans
(the excerpt plus `"exit"` from the cited `"exit": -9` review evidence), and the
candidate line has **2** (excerpt plus `"Unix only"`).

Mitigating facts, checked, not assumed: no standing counter consumes this shape
today — `scripts/corpus-contract.mjs` only requires a non-empty level-2 `## Gate`
section (lines 141-175), and the round-28/round-29 counters are hardcoded to
S036-S039 / S040-S043. Round-43's lesson also uses ASCII quotes, so this is a
lane-wide style tolerance, not a round-45-only break. Recorded as latent
fragility: the first ASCII-keyed shape gate would fail S133 on span count.

### F4 — Low (tool limit, not a round-45 defect): the round-34 check proves decision shape, not registry membership or truth

Mutant M4 (unregistered `S999` row with `reject — the candidate answer's durable
point is already carried by the tier-A primary source`) exits **0**. The checker
requires only `S[0-9]{3,}` in a row, a header with `id`+`decision`, a decision
starting with `reject`, and >=4 words left after status tokens. It never opens
`corpus/SOURCES.md` and never reads the retained source. Therefore:

- PASS is valid for the landed S134 row (S134 *is* registry row 142, status
  `rejected`), and M1-M3 show the pass is not incidental.
- PASS must not be read as "the reject reason is true". I checked the reason
  separately (§3): the `-11 is SIGSEGV` claim is in the retained answer, and the
  S133 page contains no SIGSEGV/signal-11 text, so the reason's factual halves
  hold on retained bytes.

## Verdict on the named attack

**S133 and S134 PASS** every assigned check (quote <=25 words, located by
section/paragraph, per-row label, access date 2026-10-24, quote present in the
retained bytes). **The round-34 checker, unmodified, exits 0 with
`MATCH: …:13: | S134 |` on a scratch copy of the committed table**, and its
negative controls (status-words-only reason, `admit`, row removed) all exit 1.

The Gate table is **not fully clean**: the third, unlabeled candidate row has a
false word count (13 vs 15), no location, and no retained bytes (F1), and the
S133 digest is a build-timestamp snapshot (F2). Neither changes the S133/S134
verdicts or the round's reject credit.

## Residual risk and unrun checks

- **Unrun:** `.ufo/waves/round-29/c1_quote_truth.py` and
  `.ufo/waves/round-28/c2_source_count.py` — both hardcode S040-S043 / S036-S039
  and a different row shape (bullet lines with curly quotes); running them would
  test their own constants, not this table. Their logic was reproduced by hand
  (regex span count, 1-25 word count, whitespace-collapsed substring).
- **Unrun:** `scripts/corpus-contract.mjs` over the whole corpus. Its Gate logic
  was read instead (it checks section presence, not quotes), so a full run adds
  no quote evidence. Not exercised.
- **Access-time provenance:** "accessed 2026-10-24" in both rows is self-reported;
  the only independent support is the retained files' mtime
  `2026-10-24 00:42:33`. No server timestamp is retained (the SO JSON carries
  `creation_date`, not the fetch time).
- **Live checks used one vantage** (this host's network, same day). The observed
  footer drift is build-time variance; a different CDN edge could serve a
  different build, so F2's 3-byte diff should be read as "footer time is not
  content".
- **Non-unique location:** the S133 sentence occurs twice on the page (Popen and
  CompletedProcess entries). The named occurrence exists, so this is a
  reproducibility nicety, not an error.
- **No tool installs or updates were made** (nothing was needed; pacman untouched).

## Files written

Lane (only file):

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w2/AttackGateQuotes.md` (this report)

Scratch (no lane state):

- `/fast/scratch/hyaku/kake-r45/AttackGateQuotes/repo/` — throwaway git repo holding `corpus/lessons/round-45.md` copied from HEAD, commit `ed299b9`
- `/fast/scratch/hyaku/kake-r45/AttackGateQuotes/mut_control/`, `mut_m1_statuswords/`, `mut_m2_admit/`, `mut_m3_noS134/`, `mut_m4_unregistered/` — mutation-control repos (unmodified checker only)
- `/fast/scratch/hyaku/kake-r45/AttackGateQuotes/live-subprocess.html`, `live-answer.json`, `so-a5631819.json` — live re-open bytes
