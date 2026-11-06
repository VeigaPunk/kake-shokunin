# ScribeEntry — round-99 C2 knowledge entry and coverage-map row

Scope: draft the C2 knowledge entry for the 304-freshening decision and the
`corpus/README.md` coverage-map row for it. Nothing outside
`.ufo/waves/round-99/w1/ScribeEntry/` was written except this report file and
its seat-local copy. No product code, contract, counter or instrument was
edited.

## Behavior delivered

1. **The C2 knowledge entry**, drafted at
   `.ufo/waves/round-99/w1/ScribeEntry/freshening-304.md`, in the shape of
   `corpus/knowledge/stale-extensions.md`: four front-matter lines (`source:`
   naming S484 and S485, `verified-at: 2026-11-05`, `recheck:`, `ground:`,
   `scope:`), a title, then the RFC text by section, the lane conventions, the
   decision table, the contract/counter pointer, the quote table, the source
   rows, the erratum, and a closing "what this entry does not decide" list.

   Content, section by section:
   - **§4.3.4 and the initial set** — the initial set is defined by exclusion
     from §4's reuse conditions; the section then filters it by a first match.
   - **The three first-match rules** — strong validators (all initial-set
     responses carrying the same strong validator are identified; none matched
     forbids any update), weak validators (the most recent matching stored
     response), no validator (the single stored response, only when it is the
     only one and itself lacks a validator).
   - **§3.2** — the update is "add each header field in the provided response
     to the stored response, replacing field values that are already present",
     with its four exceptions named in the section's order: the §3.1-excepted
     fields, the fields the stored response depends upon, the fields the
     recipient processes and removes, and the Content-Length field. The
     MAY-omit allowance and the "Content-* prefix is not a signal" note are
     recorded too.
   - **The §3.1 exceptions §3.2 points at** — all four, each with its own
     quote: the Connection field and the fields it names; fields whose
     semantics require removal before forwarding; the qualified no-cache and
     private directives; and the proxy-specific fields, bounded by the
     section to Proxy-Authenticate, Proxy-Authentication-Info and
     Proxy-Authorization.
   - **LC1-LC6**, each explicitly named a lane convention and not an RFC
     requirement: Last-Modified always weak; the meaning of "corresponds" in
     the weak rule; a tie on the largest `received` is a refusal; the fixed
     list of fields never copied; §3.2's other exceptions not modelled;
     qualified `no-cache="`/`private="` refused rather than excluded.
   - **Erratum EID 9185** — status **Reported** (not Verified), type
     Technical, reported 2026-09-24 against the §4.3.4 initial-set paragraph.
     What it would change (a criteria list instead of the exception list, and
     an appended association rule for a strong-ETag match despite a
     selecting-header mismatch) and why the contract does not depend on it: the
     contract takes the initial set as supplied by the caller and never
     computes it, so the clause the erratum touches is not one the contract
     implements; the three first-match rules, the §3.2 update rule and its
     four exceptions are untouched by it.
   - **A decision table** — 304 validators → rule → identified set →
     decision, one row per first-match rule, plus the paragraph fixing which
     fields the updated map never receives.

2. **Quote verification**, `quotes-check.txt`: one row per quotation that
   appears in the entry — 30 in all (26 from the retained RFC 9111 body, each
   with its plain-text line, and 4 from the retained errata page, each with
   its HTML line). Every one is a whitespace-collapsed substring of the body
   named in its row and at most 25 whitespace-separated words. Row shape:
   `body`, `id`, `line`, `found` (yes/no), `words`, `quote`. The wider errata
   wording check (nine strings, with a `used_in_entry` column) is
   `erratum-wording-check.txt`.

3. **The coverage-map row**, drafted at
   `.ufo/waves/round-99/w1/ScribeEntry/readme-row.md` in the shape of the
   existing `corpus/README.md` coverage-map table (area label with the round,
   backticked `knowledge/` path plus source rows, one-sentence coverage cell
   naming the decision and its exclusions), together with the round-99
   frontier-step section it would be appended under, in the shape round 98
   used.

4. **The meta-text gate**, run and its output saved:
   `python3 -B scripts/knowledge_metatext_lint.py --dir
   /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-99/w1/ScribeEntry`
   → `gate_findings=0 review_hits=0`, exit 0. No seat name and no handoff
   wording appears in either drafted `.md` file.

5. **A consistency cross-check** of the entry against itself, run and its
   result recorded: the entry's quote table, `quotes-check.txt` and the
   entry's own blockquote lines were compared row by row — 26 table rows, 30
   ledger rows, 30 blockquotes — with 0 mismatches in body, line, word count
   or quote text, and 0 quotations over 25 words.

## Gates run and observed results

| Check | Command | Observed |
|---|---|---|
| Frozen instrument digests | `sha256sum -c .ufo/waves/round-99/controls/instrument-sha256.txt` | 11 files `OK`, rc=0 |
| RFC body digest | `sha256sum .ufo/waves/round-99/sources/rfc9111.txt` | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` (matches the contract and the freeze) |
| Errata body digest | `sha256sum .ufo/waves/round-99/sources/eid9185.html` | `83c3b795290e09842d1af973f73b52c98fd661bf77cafc17658eb5ac4df63dd3` |
| Quote substring check | `python3 quotecheck.py` (in the seat dir) | `rfc=26 err=9 notfound=0 linemismatch=0 over25=0`, rc=0 |
| Entry/ledger/blockquote cross-check | inline script over `freshening-304.md` and `quotes-check.txt` | 26 table rows, 30 ledger rows, 30 blockquotes, `mismatches: 0` |
| Meta-text gate | `python3 -B scripts/knowledge_metatext_lint.py --dir <seat dir>` | `files=2 gate_findings=0 review_hits=0`, rc=0 |

The quote checker collapses all whitespace in the retained body, maps every
collapsed character back to its plain-text line, then locates each quote as a
collapsed substring and compares the located start line with the line stated
in the entry. A quote that is present but sits at a different line is reported
as `linemismatch`, and any quote over 25 whitespace-separated words is
reported as `over25`; both counters are 0.

## Touched surfaces

Written, all inside `.ufo/waves/round-99/w1/ScribeEntry/`:

- `freshening-304.md` — the drafted C2 knowledge entry
- `quotes-check.txt` — the 26-row RFC quote check
- `erratum-wording-check.txt` — a 9-row substring check for the erratum
  wording the entry quotes (the errata page is HTML, so it has no plain-text
  line numbering of the RFC kind; the check records the same found/words
  columns and is kept beside `quotes-check.txt` rather than mixed into it)
- `readme-row.md` — the drafted coverage-map row and its placement
- `metatext-lint.txt` — the saved gate output
- `receipts.txt` — the digest, body and gate receipts
- `quotecheck.py`, `emit_quotes_check.py` — the checker and its emitter
- `quotecheck-output.txt`, `quotecheck-summary.txt` — their output

Also written: `.ufo/waves/round-99/w1/ScribeEntry.md` (this report) and a
copy of it at `.ufo/waves/round-99/w1/ScribeEntry/report.txt`.

Nothing else in the lane tree was touched. No git or jj mutation was run in
the lane or the fleet repo; the only git commands used were read-only
(`rev-parse`, `ls-tree`, `show`, `status`, `log`).

## Findings

**F1 — the S484 and S485 registry rows are not in `corpus/SOURCES.md` at the
tip read.** `grep -n "^| S484\|^| S485" corpus/SOURCES.md` returns nothing;
the last rows present are S482 and S483. The freeze (`freeze.md`, "C2 —
freshness") and the contract both name S484 and S485 as this round's source
rows, and the contract cites the retained bodies by digest. The entry is
therefore drafted with `source:` naming S484, S485 as the freeze specifies.
Routing: the rows themselves are the scout seat's to write, and the entry
cannot be admitted until they exist. Not repaired here.

**F2 — `scripts/freshen_304.py` does not exist in the lane.** The contract
names it as the candidate path; the counter's base receipt
(`controls/base-c2.txt`) records `candidate=absent met=false`. The entry's
"contract and the counter" section therefore names the path the contract fixes
and its interface, and states explicitly that the entry reports no measurement
of any candidate and claims no conformance. It makes no claim that the file
exists or that it conforms.

**F3 — the counter's own reference list must agree with the contract before
any candidate is scored.** Not exercised by this seat; recorded because the
entry's decision table was written against the contract text, and the
contract is the scored instrument. No disagreement was found between the
contract text and RFC 9111 §4.3.4/§3.2/§3.1 as read here; the two places
where the contract is deliberately stricter than the RFC text — LC3 (a tie on
the largest `received` is a refusal, where the RFC says only "the most
recent") and LC5 (the "depends upon" and "automatically processed and
removed" exceptions are not modelled) — are named as lane conventions in the
entry, which is the treatment the freeze requires.

## Out of scope, not done

- The entry was not integrated into `corpus/knowledge/` and the row was not
  appended to `corpus/README.md`. Both are the L1's to write; this seat
  delivers drafts only.
- The S484/S485 rows in `corpus/SOURCES.md` were not written (see F1).
- `scripts/freshen_304.py` was not built, not scored, and the C2 predicate
  was not evaluated (see F2). No counter was run against a candidate.
- No claim was made about any live cache, CDN, proxy or browser.
- The §3.2 "depends upon", "automatically processed and removed" and MAY-omit
  allowances are described, not exercised; the contract does not model them.
- The initial-set computation (§4 reuse conditions, cache keys, Vary) is
  described as out of scope, not implemented.

## Limits of this seat's evidence

- The quote check establishes that each quoted string is a substring of the
  retained body at the stated line. It does not establish that the quoted
  passage is the whole of the section, nor that the section is the RFC's
  current text; the RFC body was read as retained and not re-fetched.
- The errata page was read as retained HTML. Its wording check is a substring
  check on the rendered text, and the entry does not restate the erratum's
  proposed replacement list in full — it names the three conditions and quotes
  the record's own summary of the technical change.
- The lane tip moved during this seat's work (82ce1b62 at the first read,
  7f5b1b7b at the last). All digests were verified against the working tree
  as it stood at each check, and `controls/instrument-sha256.txt` verified
  clean at the last run.
- No measurement of the C2 instrument was made, so nothing here bears on the
  frozen C2 predicate.

## Artifacts

- `.ufo/waves/round-99/w1/ScribeEntry/freshening-304.md` — the drafted entry
- `.ufo/waves/round-99/w1/ScribeEntry/quotes-check.txt` — 26-row quote check
- `.ufo/waves/round-99/w1/ScribeEntry/erratum-wording-check.txt` — 9-row erratum wording check
- `.ufo/waves/round-99/w1/ScribeEntry/readme-row.md` — the drafted coverage-map row
- `.ufo/waves/round-99/w1/ScribeEntry/metatext-lint.txt` — saved gate output
- `.ufo/waves/round-99/w1/ScribeEntry/receipts.txt` — digest and gate receipts
- `.ufo/waves/round-99/w1/ScribeEntry/quotecheck.py`, `emit_quotes_check.py` — the checker and emitter
- `.ufo/waves/round-99/w1/ScribeEntry/entry_selfcheck.py` — the entry/ledger/blockquote cross-check
- `.ufo/waves/round-99/w1/ScribeEntry/quotecheck-output.txt`, `quotecheck-summary.txt` — their output
- `.ufo/waves/round-99/w1/ScribeEntry/report.txt` — a copy of this report
- `.ufo/waves/round-99/w1/ScribeEntry.md` — this report

No tool was installed or upgraded in this seat; no tooling change was needed,
and pacman was not invoked.
