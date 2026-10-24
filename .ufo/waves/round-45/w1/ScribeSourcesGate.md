# ScribeSourcesGate — round-45 wave 1

Seat: `kake-r45.ScribeSourcesGate` (scribe, axes: freshness). Lane
`kake-shokunin`. Milestone: round-45 wave 1 (build: fixtures, driver v2,
counter v6, matrices, drafts).

## Result

**PASS** against the item's named attack. The S133 source was opened over the
live network (HTTP 200, bytes retained, sha256 recorded), the `returncode`
semantics passage was located with its exact section and paragraph, the ≤25-word
quote is a byte-exact substring of the retained bytes' visible text, the S133
SOURCES.md row is drafted, ONE REJECT decision is drafted with a located fact
and a flip, and the Gate rows are drafted labeled per new row.

Files written (lane):

- `.ufo/waves/round-45/drafts/sources-gate.md` — the draft (S133 row, S134
  reject row, Gate rows, findings, commands).
- `.ufo/waves/round-45/w1/ScribeSourcesGate.md` — this report.

Scratch only (not lane files), under
`/fast/scratch/hyaku/kake-r45/ScribeSourcesGate/`: `subprocess.html`,
`so-answer.json`, `so-question.json`, `so-24139389.html` (the HTTP 403 body),
`make_draft.py`, `check_gate.py`, `check_rows.py`, `census/SOURCES.md`,
`gaterepo/` (a scratch git repo used to run the unmodified round-34 checker).

No corpus file was edited. No commit, push, or publish. No tool was installed
(python3, curl and git were already present; pacman is paused host-wide and
nothing was needed).

## What was opened (live, read-only)

| Source | URL | Accessed | Result |
|---|---|---|---|
| Python docs: `subprocess` | https://docs.python.org/3/library/subprocess.html | 2026-10-24 | HTTP 200, 208,624 bytes, sha256 `eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd` |
| Stack Overflow answer (Stack Exchange API `questions/24139389/answers?site=stackoverflow&filter=withbody`) | https://stackoverflow.com/questions/24139389/unable-to-find-out-what-return-code-of-11-means | 2026-10-24 | HTTP 200, 723 bytes JSON, sha256 `702954fd1946cfa2e3895804f48c850acd25a47523a780e1599e7851716ffcd1` |
| Same question's metadata/title (API `questions/24139389?site=stackoverflow&filter=withbody`) | same URL | 2026-10-24 | HTTP 200, 2,857 bytes JSON, sha256 `b3fa82dbdb49e626204b635e5c7ca1399dc4603ff07f6e65276de52f49afaae0` |

The network served every fetch, so **no local-docs fallback was needed and
none was used**: `python3 -c 'import subprocess, inspect'` output was
deliberately not used as a quote source, per the item. A plain HTML `curl` of
the Stack Overflow question returned **HTTP 403** (bot filter); the API reads
returned HTTP 200, so the quoted sentence is sourced from the API body and the
Gate row says so.

## The located `returncode` passages

Page: *subprocess — Subprocess management — Python 3.15.1 documentation*,
"Last updated on Oct 24, 2026 (00:13 UTC)".

1. §Using the `subprocess` Module → `CompletedProcess.returncode`, **paragraph
   1** — "Exit status of the child process. Typically, an exit status of 0
   indicates that it ran successfully." (17 words)
2. §Popen Objects → `Popen.returncode`, **paragraph 2** — "A None value indicates
   that the process hadn’t yet terminated at the time of the last method call."
   (18 words; apostrophe is U+2019)
3. §Popen Objects → `Popen.returncode`, **paragraph 3** — "A negative value -N
   indicates that the child was terminated by signal N (POSIX only)." (15 words)

Paragraph 3 is the anchor the item names (negative `-N` = signal N);
paragraph 2 is the `None`-while-running half in the same attribute entry, so
the S133 anchor cell names both. Quotes are rendered without markdown
backticks (round-36 closure correction: a Gate quote must not carry backticks
the page text does not).

**Grounded benefit (one, per SOURCES contract rule 1):** the driver that
certifies a witness reads the counter child's exit status
(`.ufo/waves/round-44/c44_audit.py:54-61`, `p = subprocess.run(...)` →
`p.returncode`). By the documented semantics a negative value is a signal
termination and `None` is "not yet terminated", so a receipt gate that accepts
only 0/1 is reading the one set of values meaning "the counter ran and
reported" — a killed (`-9`), signalled or still-running counter can never be
credited as a witness. The round-44 review recorded `"exit": -9` on every row
while still reporting `"ok": true`
(`.ufo/waves/round-44/w2/ReviewCounterContract.md` defect 1c) and credited
exit-2 counter-error and `note: "tool absent"` receipts as witnesses (defects
1a, 1b). Scope limit, marked as opinion: with `shell=True` the same page says
the code reflects the shell's status and may map signals to `128+N`; the lane's
counters run without `shell=True` (`c44_audit.py:54`).

## Decisive command output

```
$ curl -sS -L -o subprocess.html -w "subprocess.html HTTP=%{http_code} bytes=%{size_download} url=%{url_effective}\n" https://docs.python.org/3/library/subprocess.html
subprocess.html HTTP=200 bytes=208624 url=https://docs.python.org/3/library/subprocess.html
$ curl -sS -L -o so-24139389.html -w "so-24139389.html HTTP=%{http_code} bytes=%{size_download} url=%{url_effective}\n" "https://stackoverflow.com/questions/24139389/unable-to-find-out-what-return-code-of-11-means"
so-24139389.html HTTP=403 bytes=5659 url=https://stackoverflow.com/questions/24139389/unable-to-find-out-what-return-code-of-11-means
$ curl -sS -o so-answer.json -w "so-answer.json HTTP=%{http_code} bytes=%{size_download}\n" "https://api.stackexchange.com/2.3/questions/24139389/answers?site=stackoverflow&filter=withbody&order=desc&sort=votes"
so-answer.json HTTP=200 bytes=723
$ curl -sS -o so-question.json -w "so-question.json HTTP=%{http_code} bytes=%{size_download}\n" "https://api.stackexchange.com/2.3/questions/24139389?site=stackoverflow&filter=withbody"
so-question.json HTTP=200 bytes=2857
$ sha256sum subprocess.html so-answer.json so-question.json
5d68416f383f6f3f01fca08a280a9d481e660e7ea274d7d78afb24c0391ba74d  so-24139389.html
702954fd1946cfa2e3895804f48c850acd25a47523a780e1599e7851716ffcd1  so-answer.json
b3fa82dbdb49e626204b635e5c7ca1399dc4603ff07f6e65276de52f49afaae0  so-question.json
eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd  subprocess.html
```

Quote truth — every quote asserted to be a substring of the retained bytes'
markup-stripped visible text (paragraph soft wraps collapsed to spaces, code
spans rendered without backticks):

```
$ python3 make_draft.py
QUOTE OK (18 words): Popen.returncode paragraph 2 (None)
QUOTE OK (15 words): Popen.returncode paragraph 3 (signal -N)
QUOTE OK (17 words): CompletedProcess.returncode paragraph 1
SO QUOTE OK (14 words) score=27 accepted=True
SO TITLE OK: 'Unable to find out what return code of -11 means'
WROTE /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/drafts/sources-gate.md (11451 bytes)

$ python3 check_rows.py
malformed rows (must print 0): '0'
duplicate ids (must print nothing): ''
enum violations (must print nothing): ''
row count: '134'
S133: 11 cells (want 11)
S134: 11 cells (want 11)
quote 14w FOUND in so-answer.json: A negative return code usually means that the process was terminated b
quote 15w FOUND in subprocess.html: A negative value -N indicates that the child was terminated by signal
quote 10w FOUND in so-question.json: Unable to find out what return code of -11 means
retained subprocess.html sha256: eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd
retained so-answer.json sha256: 702954fd1946cfa2e3895804f48c850acd25a47523a780e1599e7851716ffcd1
```

(The census lines are CORPUS.md §Census run over a copy of the real
`corpus/SOURCES.md` plus the two drafted rows: 0 malformed rows, no duplicate
ids, no enum violations, no tier inflation. Both drafted rows have 11 cells,
i.e. markdown `NF=13`.)

Gate rows against the two standing checks — the round-34
`gate_reject_check.py` **unmodified**, run against a scratch git repo holding
the draft's Gate table as a lesson file, plus the round-28 quote-shape rule
(id + URL + literal `accessed <date>` + exactly one 1–25-word curly-quoted
excerpt per line):

```
$ python3 check_gate.py
Gate rows found: 2
  S133: quote 15 words — A negative value -N indicates that the child was terminated ...
  S133: shape OK
  S134: quote 14 words — A negative return code usually means that the process was te...
  S134: shape OK
QUOTE-SHAPE CHECK: PASS
gate_reject_check.py exit: 0
MATCH: corpus/lessons/round-45.md:7: | S134 | https://stackoverflow.com/questions/24139389/unable-to-find-out-what-return-code-of-11-means | accessed 2026-10-24, Stack Exchange API read, HTTP 200, 723 bytes JSON, sha256 `702954fd…716ffcd1` | “A negative return code usually means that the process was terminated by a signal.” (accepted answer by sth, first paragraph) | **reject** — the answer's durable point is already carried by the tier-A primary S133, and its `-11 is SIGSEGV` claim is a signal-number mapping the opened primary does not make; flip: a tier-A POSIX or Python `signal` source naming signal 11 as SIGSEGV is opened, and this answer is then cited as an illustrative example rather than as the support |
```

## Drafted decisions (in the draft file, L1 lands them)

- **S133 row** — `Python: subprocess — https://docs.python.org/3/library/subprocess.html`
  | kind `docs` | tier `A` | scope "child-process exit-status semantics used
  by receipt gates" | anchor §Popen Objects → `Popen.returncode`, paragraphs 2-3
  (+ §Using the `subprocess` Module → `CompletedProcess.returncode`, paragraph
  1) | one grounded benefit | status `queued` | opened `2026-10-24` | recheck
  `on-release` | used-by `corpus/knowledge/receipt-integrity.md,
  corpus/lessons/round-45.md`.
- **S134 row** — Stack Overflow question 24139389, accepted answer by sth |
  kind `community` | tier `C` | status `rejected` | `REJECTED: <located fact
  that failed it>; flip: <what would change the verdict>`. Reason: the
  answer's durable point (a negative return code means termination by a signal)
  is already carried by the tier-A primary S133, and its one specific claim —
  that `-11` is SIGSEGV — is a signal-number mapping the opened primary does
  not make. Flip: a tier-A POSIX or Python `signal` source naming signal 11 as
  SIGSEGV is opened, and the answer is then cited as an illustrative example
  rather than as the support.
- **Gate rows** — two rows in the round-45 lesson's `## Gate`, labeled per new
  row (S133 admit, S134 reject), each with URL, access date, one ≤25-word
  located quote with its section/paragraph, and a decision cell.

## Coordination

`kake-r45.ScribeLessonMistakes` had independently opened the same Python docs
page (same sha256 `eceda6f6…e5bdf0dd`) and had chosen a *different* reject
candidate (SO 5631819, a restatement of the same doc passage). I messaged that
seat: my candidate (24139389) is kept because its reject reason rests on a
located fact the docs do **not** contain (the `-11` → SIGSEGV signal-number
mapping) and carries a real flip condition, whereas a restatement of the same
passage only says "adds no authority". That seat was asked to label its row
"candidate only, no decision — decision carried by the S133/S134 rows in
`.ufo/waves/round-45/drafts/sources-gate.md`", so the round carries **one**
reject decision, as the item requires. I did not edit any sibling's file.

## Findings for the L1 (also in the draft)

1. **S133's `used-by` depends on a sibling seat's draft.**
   `corpus/knowledge/receipt-integrity.md` is drafted by `kake-r45.ScribeKnowledge`
   (its spec names S133 as the source); this seat did not create it. If that
   draft does not land, S133's `used-by` must name only
   `corpus/lessons/round-45.md`, and its status stays `queued` (contract:
   `mined` = cited by ≥1 path in `used-by`).
2. **The rejected candidate is reachable only through the Stack Exchange API.**
   A plain HTML GET returned HTTP 403; the API read returned HTTP 200. A
   reviewer re-opening the HTML URL directly will hit the bot filter — the
   Gate row names the API read and its sha256.
3. **Retention is the L1's step.** The retained `subprocess.html` sha256 is
   recorded so the L1 can retain the same bytes under
   `.ufo/waves/round-45/sources/` and satisfy the standing "Gate quote is
   found in retained source text" criterion (`corpus/QUALITY.md`). This seat's
   retained bytes live in scratch only and are not lane files.
4. **Registry ids.** S133 is the next unused id (last row is S132). The
   rejected candidate takes S134 in this draft; the L1 may renumber or drop
   that registry row (keeping its Gate decision) without changing the decision
   text.

## Out of scope / not done

- No corpus file (`corpus/SOURCES.md`, `corpus/lessons/round-45.md`,
  `corpus/knowledge/receipt-integrity.md`) was edited — the corpus is
  L1-write-only this wave.
- No git commit, push, or publish of any kind; the scratch `gaterepo/` commits
  live only under scratch.
- No tool install was needed or performed (python3, curl, git already present;
  pacman paused host-wide).
- No counter, driver, matrix or fixture was executed or modified — those are
  other seats' files.
