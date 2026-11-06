# ReviewRegA — scoped findings (round 99, C1 row-review conjunct)

Verdict line: REVIEW rows=26 agree=24 disagree=2

Disagree (live, judged at repair commit 9d341d1b46f16dbfbb41af75dd6d4966808dfa5d):
- quote_class.py — Entry command `classify ... [--json]` does not run: `--json` is accepted only before the subcommand (scripts/quote_class.py:112); observed `quote_class.py classify --quote x --raw R --text T --json` rc=2 'unrecognized arguments: --json'. Verdict map `64 usage` is false: no-subcommand path is ap.error (:142), which exits 2 (observed rc=2); `return 64` at :143 is unreachable.
- wave_seat_record.py — Verdict map `64 usage` is false: no 64 return in the code; `ap.parse_args()` at :45 is uncaught, so usage errors exit 2 (observed rc=2 with no args).

Effect under the frozen C1 kill rule: a live `disagree` on two repair rows means C1 is unmet, recorded unmet by L1 (the verdict does not flip on later correction). Counter at 9d341d1b reports met=true (counter does not read Entry flags or verdict codes; declared limit).

Agree with notes (no false cell; wording only): live_snapshot.py ('receipts only' is loose: manifest.json and page.html also land in --out/<id>/); source_snapshot.py (receipts.json at :297 not named in Write scope, location covered); robots_audit_selftest.py (coverage shortfall reports as 2, 'setup fault' wording loose); cache_key_conformance.py (--work omitted falls back to TMPDIR); cache_key.py (vary must be a JSON string; cell silent).

Routed for L1 (not repaired, not in my 26):
- SKILL.md:1104 robots-expectation-audit self-test cell carries literal `[--tool PATH]`; counter exec_fail rc=2 for it; met stays true because the repair row for robots_audit.py passes.
- Counter does not validate Entry flags (declared limit; the review conjunct is the only check on that).

Method, commands and rc: review.md. Per-row verdict reasons: verdicts.tsv. Probes and self-test rc: probes.json, selftest-rc.tsv.

Deviation: the spec's Report path (.ufo/waves/round-99/w1/ReviewRegA.md) lies outside the seat directory; per the bounds it is written here as w1/ReviewRegA/ReviewRegA.md.

Tooling: no tools installed or upgraded by this seat.
