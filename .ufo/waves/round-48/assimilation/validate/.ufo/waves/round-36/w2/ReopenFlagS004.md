# Re-open S004 — `quote_missing`

**Verdict: paraphrase (quote-form defect). Not page drift, not a tool miss, not an extraction miss.**
The page is byte-identical to the recorded fetch; the sentence is present in the server-rendered
HTML. The `quote_missing` finding is caused solely by literal backticks in the ledger quote, which
contract (d) does not delete.

## Inputs

- `realrun/input.json`: S004, url `https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages`,
  quote `compressed `gzip` archive containing a single `tar` file`, `from: round-20.md`.
- Origin: `corpus/lessons/round-20.md:206` (same backticked form, in curly quotes).
- Registry row: `corpus/SOURCES.md:12` — its quote field is itself a paraphrase:
  "Pages artifacts are gzip-compressed tar files under 10GB and should contain no symbolic or hard links".

## Live fetch (no redirect, then body check)

```
curl -sS -D headers-noredir.txt -o live-noredir.body --max-time 40 --max-redirs 0 \
  'https://docs.github.com/.../using-custom-workflows-with-github-pages'   # exit 0
```
- `HTTP/2 200`, no `location`, `content-type: text/html; charset=utf-8`,
  `content-length: 141818`, `date: Fri, 23 Oct 2026 02:03:36 GMT`. No hop, so no `moved` question.
- Saved: `/fast/scratch/hyaku/kake-r36w2/ReopenFlagS004/live-noredir.body`
  (141818 bytes, sha256 `0f0c5ce93c181ae94ff0ceefef88c55bcc37c6f52d4057867a32bdfc88d84c59`).
- Recorded body: same bytes. `cmp -s recorded/S004.body live-noredir.body` → **exit 0**, same sha256
  (recorded copy extracted from `realrun/snap-bodies.tar.xz`, `./S004.body`). The page has not
  changed since the snapshot or since the row's 2026-10-19 fetch.

## Live text found (quoted)

Raw HTML (index 54315, also duplicated in the Next.js JSON payload at 90157):

> The GitHub Pages artifact should be a compressed `<code>gzip</code>` archive containing a single `<code>tar</code>` file. The `<code>tar</code>` file must be under 10GB in size and should not contain any symbolic or hard links.

Tool-extracted text (contract bullet (c), `html_text`): "The GitHub Pages artifact should be a
compressed gzip archive containing a single tar file." — i.e. `<code>` tags removed, no backticks.

## Reproduction and cause isolation

Runner: `python3 -B scripts/source_recheck.py` (lane file at build commit, unedited), single-check
manifest rebuilt from `realrun/manifest.json`'s S004 entry, run in my sandbox.

```
timeout 60 python3 -B .../scripts/source_recheck.py --manifest repro/manifest.json   # exit 1
{"version":1,"verdict":"failed-policy","checksEvaluated":1,
 "findings":[{"check":"S004","reason":"quote_missing","target":null}]}
```
Importing the tool's own `html_text`/`normalize` on the live body:
- as-recorded quote (`compressed `gzip` archive containing a single `tar` file`): **False**
- same quote with backticks removed (`compressed gzip archive ... single tar file`): **True**, at
  normalized index 2349
- round-20.md's second S004 quote (`under 10GB in size and should not contain any symbolic or hard links`): **True**

So the only failing token is the two backticks. Bullet (d) is NFKC plus delete-whitespace;
backtick is neither whitespace nor changed by NFKC. Bullet (c) removes the `<code>` tags correctly,
so the extracted text does contain the sentence. The tool matches exactly its frozen contract;
the source text is present; the quote is the markdown-source form, not rendered text.

## Scope note (not adjudicated here)

7 of the 9 `quote_missing` inputs carry backticks and all six `round-20.md` ones do
(S004, S005, S006, S007, S008, S017); S065 too. The two plain quotes (S025, S068) are different
cases owned by other seats. This looks like a systematic ledger quote-form issue from round-20,
not nine independent page drifts.

## Recommendation (advisory)

Reword S004's ledger/audit quote to the rendered form ("compressed gzip archive containing a single
tar file") and, if the registry row is the audit target, replace the row's paraphrase with that
verbatim quote. Changing contract (d) to strip markdown delimiters would touch the frozen predicate;
do not do that — fix the quote. Until then the real-input finding for S004 must not be read as
freshness evidence.

## Not verified

- Origin of the ledger form as github/docs raw markdown notation is [INFERENCE]; I did not fetch it.
- Did not run the sealed counter or the realrun snapshot myself; used the recorded bundle.
- No tools installed or updated. No processes left running.
