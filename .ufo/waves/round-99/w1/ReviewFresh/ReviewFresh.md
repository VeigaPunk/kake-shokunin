# ReviewFresh — seat report (round 99, C2 semantic ground)

Path note: the seat spec named `.ufo/waves/round-99/w1/ReviewFresh.md`. That file sits outside the seat
directory, which the hard bounds forbid. The report is written here instead, inside
`w1/ReviewFresh/`.

Files (all in `w1/ReviewFresh/`):
- `hand-review.tsv`: 50 rows, `tag<TAB>agree|disagree<TAB>basis`. Checked: 50 rows, 3 fields each, 48 agree, 2 disagree.
- `contract-findings.md`: F1–F12 with RFC or LC grounding, erratum verdict, LC1–LC6 verdicts, counts.
- `receipts.txt`: digest check, git rev-parse, counter run, sha256 of fetched RFC 9110.

## Commands and observed rc

- `git -C LANE rev-parse master` -> `7f5b1b7b8dbfdae74dfe6d487bbf5406c478b916`, rc=0. The spec names freeze ab35eace and the lane tip is a different commit; I did not check ancestry. The counter was run at the tip only.
- `sha256sum -c .ufo/waves/round-99/controls/instrument-sha256.txt` (cwd LANE) -> all 11 OK, rc=0.
- `python3 -B .ufo/waves/round-99/c99_fresh304.py --root LANE --revision master --work <scratch>/c2run` ->
  `revision=7f5b1b7b… candidate=absent met=false`, rc=1. No drift exit (2): the reference agrees with all 50
  HAND expectations.
- `sha256sum .ufo/waves/round-99/sources/rfc9111.txt` -> aeb52adb… (matches the freeze).
- RFC 9110 fetched from rfc-editor.org into scratch: sha256 21c1cdce… (not lane-retained).

## Results

- Hand: 48/50 agree. Disagree: `strong-trim`, `upd-value-bytes-kept` (both F2: byte-for-byte copy of values
  with OWS; RFC 9110 5.5).
- Lane conventions: LC1, LC3, LC4, LC5 agree; LC2 agrees and is load-bearing (F7); LC6 partly disagrees (F1, F10).
- Erratum EID 9185 (Reported, not Verified): changes NO hand expectation. It changes the caller's `stored`
  set for Vary-mismatched strong matches and needs a named initial-set definition in the contract (F4).
- contract_findings = 12. rfc_contradictions = 3 (F1 token-form qualified no-cache/private vs §3.1 bullet 3 and
  §5.2; F2 OWS-bearing values vs RFC 9110 5.5; F10 literal no-cache=/private= match refuses unknown extension
  directives vs RFC 9111 5.2.3 MUST ignore).
- Instrument notes (not counted): the reference's LC6 substring check; no HAND or generated case covers the
  token form or extension directives. Routed; not repaired.

## Verdict

`REVIEWFRESH hand=48/50 contract_findings=12 rfc_contradictions=3`
