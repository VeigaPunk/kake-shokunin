# Round 45 — source gate draft (S133 admit, one reject)

Seat: `kake-r45.ScribeSourcesGate` (wave 1, scribe). Draft only: the L1 lands
`corpus/SOURCES.md` and `corpus/lessons/round-45.md`. This seat edited no
corpus file; the only lane files written are this draft and
`.ufo/waves/round-45/w1/ScribeSourcesGate.md`.

## What was opened (read-only fetches)

| Source | URL | Accessed | Result | Retained bytes |
|---|---|---|---|---|
| S133 candidate — Python docs: `subprocess` | https://docs.python.org/3/library/subprocess.html | 2026-10-24 | HTTP 200, 208,624 bytes | sha256 `eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd` |
| S134 candidate — Stack Overflow answer (via Stack Exchange API `questions/24139389/answers?site=stackoverflow&filter=withbody`) | https://stackoverflow.com/questions/24139389/unable-to-find-out-what-return-code-of-11-means | 2026-10-24 | HTTP 200, 723 bytes JSON; the plain HTML GET of the same question returned **HTTP 403** (bot filter), so the quoted text is the API body | sha256 `702954fd1946cfa2e3895804f48c850acd25a47523a780e1599e7851716ffcd1` |
| S134 candidate — same question's metadata and title (via Stack Exchange API `questions/24139389?site=stackoverflow&filter=withbody`) | https://stackoverflow.com/questions/24139389/unable-to-find-out-what-return-code-of-11-means | 2026-10-24 | HTTP 200, 2,857 bytes JSON | sha256 `b3fa82dbdb49e626204b635e5c7ca1399dc4603ff07f6e65276de52f49afaae0` |

Both fetches are live HTTP reads made on 2026-10-24. No local
`python3 -c 'import subprocess, inspect'` output was used as a quote source.

## The located `returncode` passages (S133 candidate)

The page carries three relevant `returncode` entries. Verbatim, markup
stripped, code spans rendered without markdown backticks (round-36 closure
correction: a Gate quote must not carry backticks the page text does not):

1. §Using the `subprocess` Module → `CompletedProcess.returncode`, **paragraph
   1** — "Exit status of the child process. Typically, an exit status of 0
   indicates that it ran successfully." (17 words)
2. §Popen Objects → `Popen.returncode`, **paragraph 2** — "A None value indicates
   that the process hadn’t yet terminated at the time of the last method call."
   (18 words; the apostrophe is U+2019)
3. §Popen Objects → `Popen.returncode`, **paragraph 3** — "A negative value -N
   indicates that the child was terminated by signal N (POSIX only)." (15 words)

Paragraph 3 is the anchor the item names (the negative `-N` signal paragraph);
paragraph 2 is the `None`-while-running half of the same semantics, in the same
attribute entry, so the anchor cell names both. The Gate row carries only
paragraph 3 in curly quotes, so the line holds exactly one 1–25-word excerpt
(the round-28 quote-shape check counts curly-quoted spans per line).

Grounded benefit for the receipt gates (one, per contract rule 1): the driver
that certifies a witness reads the counter child's exit status
(`.ufo/waves/round-44/c44_audit.py:54-61`, `p = subprocess.run(...)` →
`p.returncode`). By the documented semantics a negative value is a signal
termination and `None` is "not yet terminated", so a receipt gate that accepts
only 0/1 is reading the one set of values that means "the counter ran and
reported", and a killed (`-9`), signalled or still-running counter can never be
credited as a witness. The round-44 review showed the un-gated driver recording
`"exit": -9` on every row while still reporting `"ok": true`
(`.ufo/waves/round-44/w2/ReviewCounterContract.md` defect 1c) and crediting
exit-2 counter-error receipts and `note: "tool absent"` receipts as witnesses
(defects 1a, 1b).

Scope limit (opinion, marked as such): the same page warns that with
`shell=True` the return code reflects the shell's own status and may map
signals to `128+N`. The lane's counters are invoked without `shell=True`
(`c44_audit.py:54`), so the POSIX `-N` reading is the one that applies; a
future driver that switches to a shell must not reuse this row's reasoning
unchanged.

## Draft `corpus/SOURCES.md` rows (L1 to land)

| S133 | Python: subprocess — https://docs.python.org/3/library/subprocess.html | docs | A | child-process exit-status semantics used by receipt gates | §Popen Objects → `Popen.returncode`, paragraphs 2-3 (paragraph 2 = None-while-running, paragraph 3 = negative -N signal), and §Using the `subprocess` Module → `CompletedProcess.returncode`, paragraph 1; Python 3.15.1 documentation accessed 2026-10-24, HTTP 200, 208,624 bytes, sha256 `eceda6f6…e5bdf0dd` | A receipt gate that reads a counter's exit status must read it as the docs define it — 0 success, a negative value a signal termination, None not-yet-terminated — so only an explicit 0 or 1 can carry witness credit and a killed, signalled or still-running counter can never pass as one | queued | 2026-10-24 | on-release | corpus/knowledge/receipt-integrity.md, corpus/lessons/round-45.md |

| S134 | Stack Overflow question 24139389 “Unable to find out what return code of -11 means”, accepted answer by sth — https://stackoverflow.com/questions/24139389/unable-to-find-out-what-return-code-of-11-means (read through the Stack Exchange API on 2026-10-24: question HTTP 200, 2,857 bytes JSON, sha256 `b3fa82db…49afaae0`; answers HTTP 200, 723 bytes JSON, sha256 `702954fd…716ffcd1`; a direct HTML GET of the question returned HTTP 403) | community | C | signal-number meaning of a negative child exit status (illustrative only; not the receipt-gate scope) | Accepted answer, first paragraph; accessed 2026-10-24 | REJECTED: the answer's durable point (a negative return code means termination by a signal) is already carried by the tier-A primary S133, and its one specific claim, that -11 is SIGSEGV, is a signal-number mapping the opened primary does not make; flip: a tier-A POSIX or Python `signal` source naming signal 11 as SIGSEGV is opened, and this answer is then cited as an illustrative example rather than as the support | rejected | 2026-10-24 | 180d | corpus/lessons/round-45.md |

Contract notes for the L1: row shape is 11 cells (markdown `NF=13`); `kind`
values `docs` / `community` are in the contract enum; `tier` ∈ A/B/C; `status`
∈ queued/mined/rejected; `opened` is the ISO date the author opened the source
(2026-10-24); `recheck` for the living Python doc page is `on-release` (the page
itself states "Last updated on Oct 24, 2026"), the community answer gets `180d`;
`used-by` lists only repo-relative paths that will exist once the L1 lands
`corpus/knowledge/receipt-integrity.md` and `corpus/lessons/round-45.md`. The
rejected row follows the contract's `REJECTED: <reason>; flip: <what would
change the verdict>` shape. If the L1 prefers not to give the rejected
candidate a registry id, drop the S134 registry row and keep only its Gate row
— the decision text is what the Gate must carry.

## Draft Gate rows for `corpus/lessons/round-45.md` §Gate

One row per new row, labeled per new row (round-44 closure observation: at
least one screened reject with its reason is required this round). The table
header uses `ID` and `Decision` so the round-34 `gate_reject_check.py` finds
the decision column, and each line names the id, the URL, `accessed
2026-10-24` and exactly one curly-quoted excerpt of ≤25 words (round-28
quote-shape check).

| ID | URL | Accessed | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S133 | https://docs.python.org/3/library/subprocess.html | accessed 2026-10-24, HTTP 200, 208,624 bytes, sha256 `eceda6f6…e5bdf0dd` | “A negative value -N indicates that the child was terminated by signal N (POSIX only).” (§Popen Objects → `Popen.returncode`, paragraph 3; the same entry’s paragraph 2 gives the None-while-running half) | admit — grounds the receipt-gate exit-status reading (A, docs, queued) |
| S134 | https://stackoverflow.com/questions/24139389/unable-to-find-out-what-return-code-of-11-means | accessed 2026-10-24, Stack Exchange API read, HTTP 200, 723 bytes JSON, sha256 `702954fd…716ffcd1` | “A negative return code usually means that the process was terminated by a signal.” (accepted answer by sth, first paragraph) | **reject** — the answer's durable point is already carried by the tier-A primary S133, and its `-11 is SIGSEGV` claim is a signal-number mapping the opened primary does not make; flip: a tier-A POSIX or Python `signal` source naming signal 11 as SIGSEGV is opened, and this answer is then cited as an illustrative example rather than as the support |

## Findings for the L1

1. **S133's `used-by` depends on a sibling seat's draft.**
   `corpus/knowledge/receipt-integrity.md` is drafted by
   `kake-r45.ScribeSourcesGate`'s sibling `kake-r45.ScribeKnowledge` (its spec
   names S133 as the source); this seat did not create it. If that draft does
   not land, S133's `used-by` must name only `corpus/lessons/round-45.md`, and
   its status stays `queued` until a knowledge entry cites it (contract:
   `mined` = cited by ≥1 path in `used-by`).
2. **The rejected candidate is reachable only through the Stack Exchange API.**
   A plain `curl` GET of the question returned HTTP 403; the API read returned
   HTTP 200. The quoted sentence is therefore sourced from the API body, and the
   Gate row says so; a reviewer re-opening the HTML URL directly will hit the
   bot filter.
3. **Quote truth is reproducible.** Every quote above is asserted to be a
   substring of the retained bytes' markup-stripped visible text by
   `/fast/scratch/hyaku/kake-r45/ScribeSourcesGate/make_draft.py` (scratch
   only, not a lane file). The retained `subprocess.html` sha256 is recorded
   above so the L1 can retain the same bytes under
   `.ufo/waves/round-45/sources/` and satisfy the "Gate quote is found in
   retained source text" criterion (`corpus/QUALITY.md`).
4. **No local-docs fallback was needed and none was used.** The network served
   both fetches on 2026-10-24; `python3 -c 'import subprocess, inspect'` output
   was deliberately not used as a quote source, per the item.
5. **Registry ids.** S133 is the next unused id in `corpus/SOURCES.md` (last row
   is S132). The rejected candidate takes S134 in this draft; the L1 may
   renumber or drop it (finding above) without changing the Gate decision text.

## Commands run

```sh
curl -sS -L -o subprocess.html -w "subprocess.html HTTP=%{http_code} bytes=%{size_download} url=%{url_effective}\n" https://docs.python.org/3/library/subprocess.html
curl -sS -L -o so-24139389.html -w "so-24139389.html HTTP=%{http_code} bytes=%{size_download} url=%{url_effective}\n" "https://stackoverflow.com/questions/24139389/unable-to-find-out-what-return-code-of-11-means"
curl -sS -o so-answer.json -w "so-answer.json HTTP=%{http_code} bytes=%{size_download}\n" "https://api.stackexchange.com/2.3/questions/24139389/answers?site=stackoverflow&filter=withbody&order=desc&sort=votes"
curl -sS -o so-question.json -w "so-question.json HTTP=%{http_code} bytes=%{size_download}\n" "https://api.stackexchange.com/2.3/questions/24139389?site=stackoverflow&filter=withbody"
sha256sum subprocess.html so-answer.json so-question.json
python3 make_draft.py    # asserts each quote is a substring of the retained visible text
python3 check_gate.py    # round-34 gate_reject_check.py + the round-28 quote-shape rule
python3 check_rows.py    # CORPUS.md census over the drafted rows + quote truth
```
