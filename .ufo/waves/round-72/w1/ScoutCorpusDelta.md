census_exit=0 rows=176 S439_base=0 q1=1 q2=1 q3=1 max_words=11

# ScoutCorpusDelta — Round-72 Census and Source Check

- Seat: `ScoutCorpusDelta` (role: scout, leaf member, read-only on lane)
- Lane: `kake` (`/home/vgpnk/Projects/shokunin/kake-shokunin`)
- Base revision: `3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1`
- Retained fetch artifact: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-72/sources/gitcli.html`

## Summary Verdict

All five census and source checks pass cleanly:
1. `census_exit=0`: `sources-census.sh validate` succeeds with 0 errors.
2. `rows=176`: base `corpus/SOURCES.md` contains 176 registry rows.
3. `S439_base=0`: S439 is completely absent from the base registry and all `corpus/` files.
4. `q1=1`, `q2=1`, `q3=1`: all three raw quote substrings occur exactly once in `gitcli.html`.
5. `max_words=11`: quotes have 11, 7, and 7 words; all are <= 25 words.
`end-of-options` count in `gitcli.html`: 1.

## Evidence Commands and Exit Codes

### (1) Sources Census Validation and Registry Row Count

- Validate command:
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
  - Exit code: 0
  - Output summary: 16 cross-scope duplicate URL warnings (`W04`), 0 error codes (`E*`), final line `kake ok /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`.
- Registry row count command:
  `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3,}'`
  - Exit code: 0
  - Output: `176`
- Cross-check census command:
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake`
  - Exit code: 0
  - Output: `kake rows 176` (tier.A 153, tier.B 6, tier.C 17; mined 146, queued 8, rejected 22).

### (2) Absence of S439 at Base Revision

- Base corpus grep command:
  `git -C /home/vgpnk/Projects/shokunin/kake-shokunin grep -c S439 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1 -- corpus`
  - Exit code: 1 (no matches)
  - Matches: 0 (`S439_base=0`)
- Registry check:
  `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1:corpus/SOURCES.md | grep S439`
  - Exit code: 1 (absent from base registry)

### (3) Retained Fetch SHA-256 Digest Verification

- Target file: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-72/sources/gitcli.html`
- Checksum command:
  `sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-72/sources/gitcli.html`
  - Exit code: 0
  - Computed SHA-256: `4e1ea3a5951e10f5c31157d1b03e0938d9b09130c5db099aa5baec6a02714a1e`
  - Expected SHA-256: `4e1ea3a5951e10f5c31157d1b03e0938d9b09130c5db099aa5baec6a02714a1e`
  - Result: Match confirmed.

### (4) Raw Substring Quote Checks and end-of-options Count

- File: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-72/sources/gitcli.html`

- Q1 = `'cannot be used for those commands to separate options and revisions'`
  - Command: `grep -F -c 'cannot be used for those commands to separate options and revisions' /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-72/sources/gitcli.html`
  - Exit code: 0
  - Count: `1` (`q1=1`)
  - Line 1895: `cannot be used for those commands to separate options and revisions.`

- Q2 = `'disambiguates revisions and paths in some commands'`
  - Command: `grep -F -c 'disambiguates revisions and paths in some commands' /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-72/sources/gitcli.html`
  - Exit code: 0
  - Count: `1` (`q2=1`)
  - Line 1894: `<p>Because <span class='synopsis'><code>--</code></span> disambiguates revisions and paths in some commands, it`

- Q3 = `'for this (it also works for commands'`
  - Command: `grep -F -c 'for this (it also works for commands' /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-72/sources/gitcli.html`
  - Exit code: 0
  - Count: `1` (`q3=1`)
  - Line 1896: `You can use <span class='synopsis'><code>--end-of-options</code></span> for this (it also works for commands`

- `end-of-options` count:
  - Command: `grep -c 'end-of-options' /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-72/sources/gitcli.html`
  - Exit code: 0
  - Count: `1`
  - Line 1896: `You can use <span class='synopsis'><code>--end-of-options</code></span> for this (it also works for commands`

### (5) Quote Word Count Audit (<= 25 words)

- Q1 word count:
  - Command: `printf '%s' 'cannot be used for those commands to separate options and revisions' | wc -w`
  - Result: 11 words (<= 25 words)
- Q2 word count:
  - Command: `printf '%s' 'disambiguates revisions and paths in some commands' | wc -w`
  - Result: 7 words (<= 25 words)
- Q3 word count:
  - Command: `printf '%s' 'for this (it also works for commands' | wc -w`
  - Result: 7 words (<= 25 words)
- Maximum word count among quotes: `max(11, 7, 7) = 11` (`max_words=11`).
All quotes satisfy the 25-word limit.

## Counterexamples and Defects

None observed. The base tree and retained fetch meet all criteria without deviations:
- S439 is not present in base `corpus/`.
- `gitcli.html` retains exact content matching SHA-256 `4e1ea3a5...`.
- All three quotes exist as verbatim single-line substrings.
- Each quote is concise (<= 11 words, well within the 25-word ceiling).

## Tooling Authorization & Scratch Cleanup

- Tooling: No tools installed or upgraded.
- Scratch: `/fast/scratch/hyaku/kake-r72/ScoutCorpusDelta` directory removed prior to yield.
