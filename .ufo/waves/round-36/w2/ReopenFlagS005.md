# ReopenFlagS005 — S005 `quote_missing` re-opened by hand

Item: real-input re-check (`.ufo/waves/round-36/realrun/`) reported S005 `quote_missing`.
Verdict: **real as a quote-fidelity defect; NOT a freshness / page-change / extraction defect.**
The live page is byte-identical to the recorded fetch and contains the sentence verbatim. The
recorded quote carries two markdown backticks (`` `CNAME` ``) that do not exist in the page text;
the frozen literal-match rule rejects them.

## What the row / Gate input says
- `corpus/SOURCES.md:13` S005 → GitHub Docs "Managing a custom domain…", anchor "Configuring an
  apex domain step 4 and Configuring a subdomain step 4; fetched 2026-10-19", teaching "An
  Actions-published site ignores a repository CNAME file…".
- `.ufo/waves/round-36/realrun/input.json` (entry id `S005`, from `round-20.md`):
  quote = ``any existing `CNAME` file is ignored and is not required.`` (backticks literal).
  Origin `corpus/lessons/round-20.md:207` — same backticked text; S017 line 219 repeats it.
- `realrun/manifest.json` S005: hops `[{status 200, location ""}]`, contentType `text/html;
  charset=utf-8`, body `S005.body`.

## Commands run (sandbox /fast/scratch/hyaku/kake-r36w2/ReopenFlagS005)
- `git clone lane` + checkout `f3a38bf8e68f6cee386125d34b5e95ac9b2df66e` → exit 0, HEAD as stated.
- Live GET, no redirect following, no `-L`:
  `curl -sS -D headers-noredir.txt -o body-noredir.html <row URL>` → exit 0;
  `HTTP/2 200`, `content-type: text/html; charset=utf-8`, 240439 bytes (no redirect hop).
- Recorded body extracted from `realrun/snap-bodies.tar.xz` (`./S005.body`) →
  sha256 `fec9d318c60045b51761692f84e3b3fa00bf32b22989d6265b019e412a15711b`
  == my live `body-noredir.html` sha256 (same hash). Page unchanged since capture.
- Tool reproduction (cloned tool, unedited, offline, manifests in sandbox `m/`):
  - recorded quote verbatim: `python3 -B clone/scripts/source_recheck.py --manifest m/asis.json`
    → exit 1, `{"verdict":"failed-policy","findings":[{"check":"S005","reason":"quote_missing"}]}`
    (matches `realrun/audit.json` finding `{"check":"S005","reason":"quote_missing"}`).
  - same quote with the two backticks removed: `--manifest m/plain.json` → exit 0,
    `{"verdict":"clean","checksEvaluated":1,"findings":[]}`.
- Tool internals on the body (import of `clone/scripts/source_recheck.py`):
  `normalize(q_backticked) in normalize(html_text(body))` = False (len 48);
  `normalize(q_plain) in …` = True (len 46); difference set = `['`','`']`.
  Normalized context: `…anyexistingCNAMEfileisignoredandisnotrequired.Formoreinformation
  aboutyourpublishingsource,…`
- Extraction is not at fault: `<code>CNAME</code>` is tag-stripped and its text kept per contract
  bullet (c). Raw extracted text window:
  `'If you are publishing from a custom GitHub Actions workflow, no CNAME file is created, and
  any existing CNAME file is ignored and is not required. For more information about your
  publishing source, see Configuri…'`
  Nearest preceding heading: `'Configuring an apex domain\nTo set up an apex domain, such as'` —
  the row's anchor (step 4) is accurate.
- Raw HTML occurrence (3× incl. JSON payload): `…no <code>CNAME</code> file is created, and any
  existing <code>CNAME</code> file is ignored and is not required.…`

## Why the finding fires (root cause)
SCORECARD.md:1630-1633 bullet (d) — NFKC, delete only `str.isspace()` characters, case-sensitive
substring. Backticks are punctuation, kept, so the markdown-formatted quote can never match plain
page text; `scripts/source_recheck.py:525` implements exactly that. The defect is in the stored
quote (markdown inline-code ticks transcribed from `round-20.md`), not in the page and not in the
tool's handling of HTML text.

## Scope check (same artifact elsewhere in the real-input run)
All 7 checks whose quote contains a backtick produced `quote_missing` (S004, S005, S006, S007,
S008, S017, S065); 14 findings total on 90 checks. Offline test on the recorded bodies: with
backticks removed, S004, S005, S006, S008, S017 become verbatim matches (`deticked_in_text=True`);
S007 stays False (its recorded body extracts to a JSON schema dump, quote is a table line) and
S065 stays False (quote is a raw `<link …>` tag, i.e. quote-as-markup). So at least 5 of the 14
findings are pure quote-formatting artifacts, S005 among them; the audit headline "14 findings on
13 rows" overstates freshness damage by those.

## Recommendation (for the L1 / non-author closure)
Re-quote S005 (and the other backticked Gate quotes) from page text without markdown ticks and
record the corrected quote; do not relax bullet (d) — widening the match rule would change the
frozen predicate and weaken the audit. The capture step should strip inline-code ticks when it
transcribes quotes into manifests/lessons.

## Not verified here
Only S005 was re-fetched live; S004/S006/S007/S008/S017/S065 were judged offline against their
recorded bodies (no live refetch). S007/S065 root causes are characterized, not fully diagnosed.
I did not run the sealed counter, criteria checks, or any ablation — those are other seats.

Deliverables (sandbox, absolute): `/fast/scratch/hyaku/kake-r36w2/ReopenFlagS005/body-noredir.html`
(live body), `headers-noredir.txt`, `bodies/S005.body` (recorded body, identical hash),
`m/asis.json`, `m/plain.json`, `clone/` (lane at f3a38bf8). No tool installs or upgrades.
