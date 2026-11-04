# Round 76 — lessons (kake, attempt 1)

Base `a0491fcd041cbc3fff2c964ecf6268557e45a5c1` (lane master at round open). Frozen contract
`.ufo/waves/round-76/contract.md` at `b758cb04`; Amendment 1 at `783c7c13` (terms-only: the C2 real-input
population is the **8** retained served pages, not the 12 the frozen sentence names — the other four retain
`audit.json` + `fetch.json` only); Amendment 2 at `e674bc60` (decides the 16 classes the frozen terms left
undecidable, A1–A17); Amendment 3 at `6b52407b` (B1 revision-versus-digest, B2 section identity and row
dedupe, B3/B3-bis whole-line correction closure, B4 exact append-only, B5 ready artifacts, B6 the
re-measured before-state); Amendment 4 at `f4f076ba` (the counter's own diagnostics are never receipts);
Amendment 5 at `152bffd5` (receipt directories only, diagnostic-line stripping, the selftest must run); Amendment 6
at `d2555766` (canonical/x-default granularity); Amendment 7 at `d2555766` (the seat-tree exclusion applies only to the
newest measured round); Amendment 8 at `d00ea7fb` (same-tag reciprocity is a stricter lane policy; the
grammar is a frozen ASCII validator, not a BCP-47 validator). Each amendment is terms-only and recorded
before any after-state.

Wave `w1`: one v1 wave, **15 seats** — scout 2, executor 5, scribe 2, reviewer 2, critic 1,
mutation-tester 1, connector 1, sentinel 1; attack share 4/15 = 26.7 %; the L1 held the planner seat (the
validator rejects a `planner` role).

## Claims

**C1 — calibration (owned score 2, the lane's lowest non-retired axis).** A round's claim rows stop
quoting command output that no committed receipt contains: every claim-bearing backticked span in the
effective claim rows of rounds 75–76 is a contiguous substring of a committed receipt, or carries an
explicit elision whose fragments are contiguous, or is closed by a correction line that itself quotes a
validated receipt line and names the defective span. Counter `.ufo/waves/round-76/c76_quote_truth.py`
(v0) hardened into `scripts/doc_quote_truth.py`; `met = (findings == 0) and append_only`.

```sh
python3 -B scripts/doc_quote_truth.py --root . --revision <rev> --base a0491fcd041cbc3fff2c964ecf6268557e45a5c1 --rounds 75,76
```

**C2 — operability (capability acquisition: offline hreflang declaration audit).** The lane can audit
hreflang declarations offline on a versioned manifest: the new tool decides every decided contract case
correctly, every degenerate constant control fails at least one case, its own selftest passes, and it runs
end-to-end on the 8 retained served surfaces. Tool `scripts/hreflang_audit.py`; findings
`hreflang_missing_value`, `hreflang_invalid_tag`, `hreflang_relative_href`, `hreflang_duplicate_pair`,
`hreflang_multiple_xdefault`, `hreflang_self_missing`, `hreflang_nonreciprocal` /
`hreflang_external_target` (informational), `hreflang_canonical_not_self`; exit 0 clean, 1 policy, 2 input
fault, 64 usage.

```sh
python3 -B .ufo/waves/round-76/w1/ExecAuditMatrix/c76_hreflang_matrix.py \
  --root . --tool scripts/hreflang_audit.py --revision <rev> \
  --cases .ufo/waves/round-76/w1/ExecAuditMatrix/cases \
  --consts .ufo/waves/round-76/w1/ExecAuditMatrix/consts --work <scratch>
```

## Gate

- **Admit — S444, Google Search Central, Localized versions of your pages.**
  <https://developers.google.com/search/docs/specialty/international/localized-versions>, opened
  2026-11-03, HTTP 200, 199,246 B retained (sha256 `12fbe281…dc8d7b`; tag-stripped text 25,035 B, sha256
  `96175da8…a8788`), retained at `.ufo/waves/round-76/w1/ScoutHreflangSources/`. Located quote (13 words,
  §"Guidelines for all methods", `google-localized-versions.txt` lines 362–364): "Each language version
  must list itself as well as all other language versions." Teaches the self-reference rule the entry's
  `hreflang_self_missing` rests on. Status `mined` (the C2 entry cites it). **Flip condition:** a re-fetch
  whose tag-stripped text no longer carries the sentence at those lines → reject the row and retitle the
  entry as a lane-internal note.
- **Admit — S445, WHATWG HTML, the `hreflang` attribute and link type "alternate".**
  <https://html.spec.whatwg.org/multipage/links.html>, opened 2026-11-03, HTTP 200, 381,019 B (sha256
  `2f21e82b…eec3`; tag-stripped 111,855 B), retained at the same directory. Located quote (10 words, §4.6.3
  `attr-hyperlink-hreflang`, `whatwg-links.txt` line 1356): "The value must be a valid BCP 47 language
  tag." Teaches the tag requirement plus the advisory/non-authoritative clauses the entry's language limit
  quotes. Status `mined`. **Flip:** the sentence leaves line 1356 or the advisory clauses change →
  re-ground before the next round cites it.
- **Admit — S446, RFC 5646 (BCP 47), §2.1 Syntax and §2.2.9 Classes of Conformance.**
  <https://www.rfc-editor.org/rfc/rfc5646.txt>, opened 2026-11-03, HTTP 200, 208,592 B (sha256
  `5d9515f0…8228`). Located quote (13 words, lines 1053–1054): "A tag is considered "well-formed" if it
  conforms to the ABNF (Section 2.1)." Teaches the well-formed/valid split that scopes `hreflang_invalid_tag`
  to syntax. A second quote the entry uses (20 words, §2.1.1, lines 327–328): "At all times, language tags
  and their subtags, including private use and extensions, are to be treated as case insensitive". Status
  `mined`. **Flip:** a later RFC replaces 5646 at this URL and the sentences move → re-open before citing.
- **Reject — "Google requires a hreflang target's canonical to be itself" as a sourced fact.** No opened
  source states it: `grep -n 'canonical' google-localized-versions.txt` returns navigation links only, and
  RFC 5646 does not discuss canonical. The contract's `hreflang_canonical_not_self` therefore stands as a
  **lane policy** and the entry says so in those words (`corpus/knowledge/hreflang-declaration.md`
  §"The canonical interaction"). **Flip condition:** an opened source (an engine's own documentation)
  states the rule with a locatable sentence → the id becomes sourced and the entry is corrected append-only.
- **Reject — the scout's claim that `x-default` is "the only non-tag value" is only Google-grounded.**
  `x-default` occurs 0 times in the WHATWG page and 0 times in RFC 5646 (the scout's own grep); the reserved
  status rests on S444 alone. The entry attributes it to S444 and does not generalise it.
- **Row cells:** the three rows' full 11-column text is in `corpus/SOURCES.md` (S444–S446, appended this
  round, census 181 → 184, exit 0) and the scout's `ScoutHreflangSources.md` §4 carries the derivation.
- **Quote verification:** `ScoutHreflangSources/verify_quotes.py` → `verify-output.txt`: `quotes=17`,
  `failures=0`, every line `exact=true`.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| **A diagnostic receipt laundered the defects it reported.** The C1 counter's own output prints each absent span verbatim, and so do seats' receipts; once that file was committed the counter found its own findings "contiguous" and printed `findings=0` with no repair, so the round's do-nothing control silently met the target | `w1/MutationTesterGates.md` and `w1/ExecQuoteRepair.md`; measured: `python3 -B .ufo/waves/round-76/c76_quote_truth.py --root . --revision 6b52407b --base a0491fcd --rounds 75,76` → `findings=0 met=true`, while the same command at `a0491fcd` prints `findings=8 met=false`; the launder files are `controls/base-c1-quote-truth.txt` and the five `controls/ctl-*.txt` | none at freeze — the frozen C1 sentence said "a committed receipt" without a universe rule; Amendment 4 (name exclusion) and Amendment 5 (receipt directories only, diagnostic lines stripped, seat tree of the newest round excluded) are the criterion that should have caught it | the delivered counter excludes its own diagnostics by name, strips `T1/T2/T4/A1` lines from every receipt, and refuses the newest round's `w1/` tree; the red no-repair control is committed (`w1/ExecQuoteRepair/receipts/13-…`: base + the round's controls → `findings=7 met=false`) |
| **A frozen counter's selftest could not run, and four mutants survived behind it.** The hardened build's fixture helper was invoked twice with a byte-identical payload, so the second `git commit` exited 1 and the harness raised before any case; the build still looked green in its own report | `w1/MutationTesterGates.md` (the intermediate build reported as tool blob 63af0ede: `--selftest` aborts in fixture setup; mutants M3/M6/M7 and the presence-exempts mutant survive); final build `scripts/doc_quote_truth.py` runs `selftest: 63/63 passed` | none — the round-75 QUALITY criterion requires "a `--selftest` that exits 0", but nothing executed it before the build was reported | Amendment 5 §D5; the delivered build's tally is a committed receipt and the mutation seat re-ran against the final sha |
| **A claim row quoted an interior slice of a receipt line** (unmarked elision) — the round-75 closure's R6 class, found eight times in this lane's own ledger | the seven base findings at `a0491fcd` (`controls/base-c1-quote-truth-v2.txt`): `SCORECARD.md:4892` ×2, `4893` ×2, `4904`, `corpus/QUALITY.md:1499`, `corpus/lessons/round-75.md:82`; each splices across an observed field (`classes=-`, `met=false`, `worktree=identical … declared_match=false`) or stitches two lines | the round-75 QUALITY criterion stated the rule but no instrument ran it over the ledger; the round-76 C1 counter is that instrument (base red before any repair) | whole-line correction rows in `SCORECARD.md` `## Round 75 — quote corrections (appended round 76)`, one QUALITY criterion, one lesson `## Corrections

- **Round-75 closure R1/R2 (stale digests).** The round-75 LOG entry named the hardened counter as
  `0699a672…` and the receipt as `f3128628…` (both the blobs at `4e3fc159`). Re-derived at `a0491fcd`
  (`controls/r1-r2-digests-v2.txt`), whole lines:
  `counter_sha256=63e321b28e509781405f1b4209a66b99460bc2512c92a8615fec06f2423e944b`
  `receipt_sha256=15768f81460bcbf991bacf9ffdf6a2145d32f4de7d952f52526589d8013e6613`
  `tool_sha256=162dd6852cd5f6adbf278405365464f0b2f5c5d66100883a0974c32b0e6a68e7`
  `[r76-correction 2026-11-03]`
- **Round-75 closure R3 (revision labels).** The round-75 before→after table was headed "After (tip
  `6c10b433`)" while every after cell named `f87d14a9`, the tip paragraph called `3ae076ab` the measured
  revision, and `controls/after-harm-battery.txt` measured the tree at `306fff49`. This round's report and
  SCORECARD row state one measured revision per artifact; the three labels above are superseded.
- **Round-75 closure R7 (C2 quotation scope).** The round-75 after-quote omitted
  `declared_match=false` (the receipt's subject is `abfbfaac…`, not its carrier `f87d14a9`), and the
  16-forgery matrix in `W1/ReviewerC2.md` ran on the predecessor tool blob, not on the landed tool. Both
  are disclosed here; the matrix is not re-cited as evidence for the landed blob.
- **Round-75 closure R8 / lesson §Routed 4 (superseded docstring).**
  `.ufo/waves/round-74/c74_registry_gap.py:25` still says "the five contract fixtures f1-f5"; the file
  defines `fx_f1`–`fx_f8` and its own selftest runs all eight. The frozen wave file is not rewritten; this
  correction is its erratum.

## Routed dispositions

`fixed` / `open` below are read from committed bytes; nothing claims a check that was not run. Rows 1–8 are
`corpus/lessons/round-75-verifier-spotcheck.md` §6; rows 9–13 are `corpus/lessons/round-75.md` §Routed.

| # | Routed item | Status | Pointer | Flip condition |
|---|---|---|---|---|
| 1 | Stale counter digest in `LOG.md:2534` | fixed | round-76 LOG correction bullet; `controls/r1-r2-digests.txt` → `63e321b2…` | a later counter edit leaves the bullet naming a non-tip digest |
| 2 | Stale receipt digest in `LOG.md:2535` | fixed | same bullet; receipt `15768f81…`, 3,793 B | receipt regeneration without a new correction |
| 3 | Revision labels disagree with their own evidence | fixed | this lesson §Corrections; the report states one measured revision per artifact | a round-76 row naming two revisions for one artifact |
| 4 | R5 partly closed: the two sidecar tools have no receipt/registry row | open | `corpus/knowledge/instrument-receipts.json` → 18 paths, neither sidecar present; binding them moves the population 18 → 20 and reddens `--check` at the tip until a new receipt is written | a round that adds both registry rows and regenerates the receipt to `population=20 bound=20` with `--check` green |
| 5 | Round-74 R3 undispositioned: sweep delta unrecorded | fixed | `controls/sweep-r76.txt`: `citation base: 107 targets · missSet 65 · files 199`, `VERDICT: DRIFT — §paths: 1 unannotated miss`, `observed-exit=1`; the 193/195-file figures in the r74 closure are not reproducible here because the corpus grew — the delta is recorded, not re-pinned (open L0 `kake \| round-69` forbids pinning `~/projects` unilaterally) | the operator rules the r69 L0 question |
| 6 | `QUALITY.md` able-to-fail quote not contiguous | fixed | base finding `T1 corpus/QUALITY.md:1499` (`controls/base-c1-quote-truth-v2.txt`); the r76 criterion quotes the landed deletion-control line whole; `findings=0` at the carrier proves contiguity | a QUALITY row that again elides middle tokens |
| 7 | C2 quotation scope (`declared_match=false`; matrix snapshot blob) | fixed | this lesson §Corrections | a later claim reusing that matrix as evidence for the landed blob |
| 8 | Superseded docstring `c74_registry_gap.py:25` | fixed | this lesson §Corrections (erratum) | a rewrite of the frozen file |
| 9 | E2 multi-pair ambiguity in `c75_row_truth.py` | open | the frozen r75 counter is unchanged; the r76 instrument does not inherit E2 (its predicate is span contiguity) | a round that freezes the multi-pair interpretation and lands a superseding row |
| 10 | `--base` optional in the r75 counter | fixed in the successor | `scripts/doc_quote_truth.py` exits 64 without `--base`; the r75 file stays frozen | the operator re-scopes the frozen counter |
| 11 | Carrier receipt outside `c58_receipt_rewrites.py`'s watch | open (operator) | `corpus/lessons/round-75.md` §Routed 3 | the checker's watched population includes the carrier path, or `tool_sha256` enters the receipt schema |
| 12 | Superseded docstring (same as row 8) | fixed | this lesson §Corrections | as row 8 |
| 13 | Host-absolute paths in committed evidence | open (operator) | the class is repo-wide; this round's new receipts name scratch only where a tool's argv must | the operator rules on public-facing path policy |

## Sources

- **S444 — Google Search Central, Localized versions of your pages** (opened 2026-11-03, HTTP 200,
  199,246 B retained, sha256 `12fbe281…dc8d7b`): located quote, 13 words, §"Guidelines for all methods"
  `google-localized-versions.txt` lines 362–364: "Each language version must list itself as well as all
  other language versions." Row status `mined`; the C2 entry cites it for self-reference, `x-default`,
  absolute hrefs and the limits. The body changed between two fetches the same day (199,246 vs 199,242 B);
  the tag-stripped article text was byte-identical, so quotes are anchored to the retained text and lines.
- **S445 — WHATWG HTML, §4.6.3 `attr-hyperlink-hreflang` and §4.6.8.1 Link type "alternate"** (opened
  2026-11-03, HTTP 200, 381,019 B, sha256 `2f21e82b…eec3`): located quote, 10 words, `whatwg-links.txt`
  line 1356: "The value must be a valid BCP 47 language tag." Row status `mined`. Re-fetch byte-identical.
- **S446 — RFC 5646 (BCP 47), §2.1 Syntax, §2.1.1 Formatting and §2.2.9 Classes of Conformance** (opened
  2026-11-03, HTTP 200, 208,592 B, sha256 `5d9515f0…8228`): located quote, 13 words, lines 1053–1054:
  "A tag is considered "well-formed" if it conforms to the ABNF (Section 2.1)." Row status `mined`. Re-fetch
  byte-identical.
- The scout's quote receipt is `.ufo/waves/round-76/w1/ScoutHreflangSources/verify-output.txt`
  (`quotes=17`, `failures=0`).
- C1 rests on lane instruments and committed receipts, not on a web source: the predicate is contract §C1
  as amended, the counter `scripts/doc_quote_truth.py`, and the controls under
  `.ufo/waves/round-76/controls/`.
- The canonical-interaction rule has **no opened source** (see §Gate, reject): it is recorded in the entry
  as the contract's policy; registry rows S020/S021 were not re-opened this round and are not quoted.
