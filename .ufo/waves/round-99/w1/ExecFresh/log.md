# ExecFresh — iteration log (C2 candidate scripts/freshen_304.py)

Built from `fresh304-contract.md` + RFC 9111 §3.1, §3.2, §4.3.4 (retained body) only. The
counter's code (`c99_fresh304.py`, `build_frozen.py`, `frozen/*.py`) was NOT read; only the
docstring (lines 1-30) of `c99_fresh304.py`. Instruments digest-verified before use
(`sha256sum -c controls/instrument-sha256.txt` rc=0). Lane tip read-only:
`git rev-parse master` = 7f5b1b7b8dbfdae74dfe6d487bbf5406c478b916.

## Iteration 1 — first candidate (sha256 60543423efbc2b2451e3179c7d9f3f0cf91f2d0f12fffe588295fd9a439c2e75)

- Own selftest: 72/72, rc 0.
- Score, `--candidate-file`, `--revision master`:
  - default seed 2136677243: `hand=49/50 generated=240/240 refusals=50/51 met=false`, rc 1;
    `fail hand:ref-qualified-private`
  - seed 1: `hand=49/50 generated=240/240 refusals=45/46 met=false`, rc 1; same failing case
  - seed 2: `hand=49/50 generated=240/240 refusals=53/54 met=false`, rc 1; same failing case
  - seed 3: `hand=49/50 generated=240/240 refusals=40/41 met=false`, rc 1; same failing case
- Diagnosis: the only failing expectation is the LC6 hand case `ref-qualified-private`
  (a qualified `private="` in the 304 Cache-Control must be refused). My check used a
  case-sensitive literal substring; the counter's reference treats the same directive in a
  different letter case as qualified too. The failing case's exact input was not read from the
  counter (the counter's code is off-limits); the diagnosis rests on the output line plus the
  contract text below.

## Iteration 2 — fix in candidate only (sha256 db3a0f12b91a5a54409ebafcf800204011385a523ff4da9b897b71dd7c0c1d4f)

- Change: the LC6 check lowercases the Cache-Control value before matching `no-cache="` and
  `private="`. Added 4 selftest cases (uppercase/mixed-case qualified forms refused; uppercase
  unqualified forms accepted; other qualified directive e.g. `max-age="60"` not refused).
- Own selftest: 76/76, rc 0.
- Score:
  - default seed 2136677243: `hand=50/50 generated=240/240 refusals=51/51 seed=2136677243 met=true`, rc 0
  - seed 1: `hand=50/50 generated=240/240 refusals=46/46 seed=1 met=true`, rc 0
  - seed 2: `hand=50/50 generated=240/240 refusals=54/54 seed=2 met=true`, rc 0
  - seed 3: `hand=50/50 generated=240/240 refusals=41/41 seed=3 met=true`, rc 0
- No counter or contract edit was made between or after scorings.

## Contract sentences found ambiguous (recorded, not resolved by counter reading)

1. **LC6 directive case.** "a 304 whose Cache-Control value contains `no-cache="` or `private="`"
   does not say whether the directive names are case-sensitive. RFC 9111 §5.2 makes directive
   names case-insensitive, so the candidate reads them case-insensitively. This was the one
   change made after a failing score. It is a reading of the RFC, applied to the lane's own
   candidate, not a counter edit; the contract text itself was not changed.
2. **Strong-rule comparison.** "equal character-for-character" was implemented as opaque-tag
   equality with both tags strong (the `W/` prefix is the only other part of a strong tag, and
   strong tags have none). Equivalent to a literal string comparison for valid strong tags.
3. **Weak rule with both validators.** "for every validator the 304 carries" was read as a
   conjunction: a stored response with the ETag but without the Last-Modified does not
   correspond when the 304 carries both (implemented; a selftest case covers it).
4. **Stored-response ETag validity.** "malformed ETag ... in any stored response is refused" was
   read as checked for every stored element, not only candidates (implemented in validation,
   before selection).
5. **Last-Modified value comparison.** "compared after trimming spaces/tabs, exact octet
   equality" was read literally: case-sensitive, no date parsing (implemented).
6. **`rule` when the 304 has an ETag but it is weak and nothing matches.** `rule` = "weak"
   (decided by the 304 alone), decision "no-update" — follows the contract's "rule is decided by
   the 304 alone" sentence.

## Tooling

No tool was installed or upgraded. The candidate uses only the Python 3.14.8 standard library
(`json`, `re`, `sys`). No pacman, no sudo.
