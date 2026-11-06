# ExecFresh — round 99 C2 candidate (scripts/freshen_304.py)

Seat: ExecFresh (leaf; no subagent dispatched). Lane tip read-only: `git rev-parse master`
= 7f5b1b7b8dbfdae74dfe6d487bbf5406c478b916. Round base cde408e5817bf1376c701d8decc5469fa82b2985.

## Path deviation (flagged)

The spec's `Report:` line names `.ufo/waves/round-99/w1/ExecFresh.md`. That path is outside this
seat's own directory, which the hard bounds reserve as the only writable location. This report
is therefore written to `.ufo/waves/round-99/w1/ExecFresh/ExecFresh.md`. The L1 may move it.

## Inputs read

- `skill://godspeed` (posture only).
- `freeze.md`, `fresh304-contract.md`, `controls/instrument-sha256.txt`, `controls/base-c2.txt`
  (`candidate=absent met=false`, rc 1), `controls/ctl-c2-pos-oracle.txt`
  (`hand=50/50 generated=240/240 refusals=42/42 met=true`, rc 0), `controls/ctl-c2-selftest.txt`.
- RFC 9111 retained body, §3.1 (lines 338-368), §3.2 (369-), §4.3.4 (951-1012); EID 9185 page
  (only its boilerplate shell is readable in the retained copy; the erratum body is elided there,
  and the contract does not compute the initial set, so it does not bear on this candidate).
- `c99_fresh304.py` lines 1-30 (docstring) only. Code of `c99_fresh304.py`, `build_frozen.py` and
  `frozen/*.py` was NOT read; their sha256 was checked only through the digest file.

## Verification of the frozen instruments

`sha256sum -c .ufo/waves/round-99/controls/instrument-sha256.txt` → all 11 entries `OK`, rc 0.

## Candidate

- Path: `.ufo/waves/round-99/w1/ExecFresh/freshen_304.py`
- sha256 (final scored bytes): `db3a0f12b91a5a54409ebafcf800204011385a523ff4da9b897b71dd7c0c1d4f`
- Stdlib only (`json`, `re`, `sys`). Decision path opens no file, socket or process.
- stdin JSON → stdout JSON, exit 0; refusals → `invalid_input: <reason>` on stderr, empty stdout,
  exit 1. `--selftest` prints `selftest N/N`.
- Module docstring names the contract, RFC 9111 §4.3.4 / §3.2 / §3.1 and LC1-LC6.

## Scores (frozen counter, `--candidate-file` only, `--revision master`, rc recorded)

| run | seed | candidate sha256 (prefix) | hand | generated | refusals | met | rc |
|---|---|---|---|---|---|---|---|
| iter 1 default | 2136677243 | 60543423… | 49/50 | 240/240 | 50/51 | false | 1 |
| iter 1 seed 1 | 1 | 60543423… | 49/50 | 240/240 | 45/46 | false | 1 |
| iter 1 seed 2 | 2 | 60543423… | 49/50 | 240/240 | 53/54 | false | 1 |
| iter 1 seed 3 | 3 | 60543423… | 49/50 | 240/240 | 40/41 | false | 1 |
| **final default** | 2136677243 | db3a0f12… | 50/50 | 240/240 | 51/51 | **true** | 0 |
| **final seed 1** | 1 | db3a0f12… | 50/50 | 240/240 | 46/46 | **true** | 0 |
| **final seed 2** | 2 | db3a0f12… | 50/50 | 240/240 | 54/54 | **true** | 0 |
| **final seed 3** | 3 | db3a0f12… | 50/50 | 240/240 | 41/41 | **true** | 0 |

Receipts: `score-default.txt`, `score-1.txt`, `score-2.txt`, `score-3.txt` (each the counter's
output line plus `rc=` trailer), `selftest.txt` (`selftest 76/76`, rc 0), `selftest.stderr.txt` (empty).

Iteration 1 outputs are recorded in `log.md` (not as separate receipt files).

## Iteration summary

- One fix, in the candidate only: LC6 check made case-insensitive on Cache-Control directive
  names (RFC 9111 §5.2), with four added selftest cases. Found by the single failing hand case
  `ref-qualified-private` on all four seeds.
- No contract edit, no counter edit, no seed change. The scored revision (`master`) was
  unchanged across all runs.

## Contract ambiguities (detail in log.md)

1. LC6 says "contains `no-cache="` or `private="`" without saying whether directive names are
   case-sensitive. The candidate reads them case-insensitively per RFC 9111 §5.2. This is the one
   reading that changed after a score, so the L1 should weigh it on that basis.
2. Weak-rule conjunction over every validator the 304 carries (read as: a stored response must
   match all of them).
3. Stored-response ETag validity is checked for every stored element before selection.
4. `rule` is the 304's own classification (weak when the 304 carries a weak validator and nothing
   matches), per "rule is decided by the 304 alone".

## Predicate note (for the L1, not a judgement of C2)

The frozen predicate reads: "at the C2 content commit, `candidate=present hand=50/50
generated=240/240 met=true`, exit 0, and the scored sha256 equals `git show <REV>:scripts/freshen_304.py`."
This seat has produced the scoring line at the lane tip (`7f5b1b7b`) against the candidate file, not
a committed content commit. The sha256 equality clause therefore cannot be met until the candidate
is committed; this seat did not commit (no mutating git in the lane). The L1 must commit the file
and re-score with `--revision <C2 commit>` (without `--candidate-file`) to satisfy the frozen
predicate. This seat is not making that claim.

## Verdict (command and rc observed)

`python3 -B c99_fresh304.py --root <LANE> --revision master --candidate-file freshen_304.py --work <scratch>` → rc 0, met=true on default, seed 1, seed 2, seed 3.

EXEC freshen_304 selftest=76/76 default=met seeds=3/3 sha256=db3a0f12b91a5a54409ebafcf800204011385a523ff4da9b897b71dd7c0c1d4f
