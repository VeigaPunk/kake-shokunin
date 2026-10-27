# ExecResolverTests

Seat: w1 C2 attack seat, independent of the fix author. Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`,
contract base `044048597d62f3199494b63b36e90dd57825e350`, lane HEAD during measurement
`cc8da1674d6e590ae2d05e1f48944ac7939e9ecd`, round date 2026-10-26.
Battery artifact: `.ufo/waves/round-58/w1/ExecResolverTests.files/battery.py` (stdlib only, builds its own
fixture lanes under `/fast/scratch/hyaku/kake-r58/ExecResolverTests`, prints PASS/FAIL per case + a tally).
Measured tool: `scripts/id_resolver.py` as committed at HEAD, blob sha256
`25982446d2e647830269cfff0b4bebf7bf263dde57c4321d87eeb42f06461bee` (file clean vs HEAD; identical bytes
to the base revision — `git diff 0440485..HEAD -- scripts/id_resolver.py` is empty).
No tools were installed or upgraded for this seat.

## BATTERY:

13 cases. Each builds one fixture lane `demo-shokunin` (a `corpus/SOURCES.md` registry + `corpus/knowledge/*.md`
that cite known ids) and asserts **(a)** the exact set of `DANGLING <id>` ids on stdout and **(b)** the exit code.
Fence semantics are CommonMark 4.5/4.6, and each fence fixture's expected code/heading classification was
independently confirmed against the reference parser `cmark 0.31.2` (`cmark-oracle.txt`: 8/8 fixtures match).

| # | case | expectation | why any correct fix must show it |
|---|---|---|---|
| 00 | `control-plain-registry` | dangling `{}`, exit 0 | control: a fence-free registry resolves S001; catches a battery whose invocation itself is broken |
| 01 | `four-backtick-not-closed-by-three` | dangling `{S901,S902}`, exit 1 | a closing fence needs the same character and **at least as many** of it; real section holds only S101, so both decoy rows (before and after the bare ``` line) stay code — and the ``` line does not end the fence |
| 02 | `tilde-fence-not-closed-by-backticks` | dangling `{S903,S904}`, exit 1 | a `~~~` fence is closed only by `~~~`; the ``` inside and the second fenced `## Registry` stay code; the trailing `~~~` closes |
| 03 | `four-space-fence-line-is-code` | dangling `{}`, exit 0 | a 4-space line is an indented code block, never a fence, and does not open or end a section: the `## Registry` after it is real and S905 resolves. **Anti-over-correction control** |
| 04 | `fence-with-info-string` | dangling `{S906}`, exit 1 | an info-string opener (```` ```markdown ````) still opens; only S906 is inside; S907 after the bare closing fence resolves |
| 05 | `unclosed-fence-to-eof` | dangling `{S908,S909}`, exit 1 | an unclosed fence runs to EOF; a second `## Registry` and its rows after it must not count, while S105 in the real section still resolves |
| 06 | `heading-after-fenced-heading` | dangling `{S910}`, exit 1 | a **fenced** `## Registry` is code and neither opens nor ends the section; the later real `## Registry` does open it (S911 resolves) |
| 07 | `three-space-row-after-fence` | dangling `{S912}`, exit 1 | both rows are inside the real Registry section: the 3-space row inside the fence is code, the 3-space row after the closed fence is a valid row (0–3 spaces) and resolves |
| 08 | `crlf-around-fence` | dangling `{S914}`, exit 1 | same structure with CRLF endings: fence open/close, heading and rows must survive `\r` on every line |
| 09 | `revision-tab-in-name` | dangling `{S917}`, exit 1 | `--revision`: `corpus/knowledge/has<TAB>tab.md` cites S917; git C-quotes that name, so the cited id must still be read. Registered S020 in `ok.md` must resolve |
| 10 | `revision-newline-in-name` | dangling `{S918}`, exit 1 | same at `--revision` for a name containing a newline (`new\nline.md`) |
| 11 | `revision-backslash-in-name` | dangling `{S919}`, exit 1 | same at `--revision` for a name containing a literal backslash (`back\slash.md`) |
| 12 | `revision-non-ascii-subdir` | dangling `{S920}`, exit 1 | same at `--revision` for a knowledge file in a non-ASCII subdirectory (`日本語/notes.md`) |

Notes. `--fleet` is always the case dir (no siblings), so `owners=-`; the battery deliberately does not re-test
sibling ownership, absent `--fleet`, or the tool's own selftest — `c58_resolver_cases.py` P4/P5/P6 own those.
An early layout of case 07 placed the fenced row outside any Registry section, so a fence-blind tool passed it by
accident; the fixture was re-shaped so the in-fence row lies inside the real section, and the current tool now fails it.

## CURRENT TOOL:

`python3 -B battery.py <lane>/scripts/id_resolver.py` → **2/13 cases passed**, exit 1
(`run-current.txt`; an immediate second run with default fixture cleanup reproduced 2/13, `run-current-clean.txt`).

Passing today: `00-control-plain-registry`, `03-four-space-fence-line-is-code`.

Failing today (11), with observed output:

| case | observed | reading |
|---|---|---|
| 01 | exit 0, `dangling=0`, `ids_cited=3` | fence-blind: both decoy rows parsed as registry rows → **false green** |
| 02 | exit 0, `dangling=0`, `ids_cited=3` | fence-blind (`~~~` and ``` both ignored as markup) → false green |
| 04 | exit 0, `dangling=0`, `ids_cited=3` | fence-blind; info-string opener not recognised → false green |
| 05 | exit 0, `dangling=0`, `ids_cited=3` | no unclosed-fence state; decoy registry after the opener is parsed → false green |
| 06 | exit 0, `dangling=0`, `ids_cited=3` | a fenced `## Registry` opens the section (defect D1) → false green |
| 07 | exit 0, `dangling=0`, `ids_cited=3` | the 3-space row inside the fence is parsed as a row → false green |
| 08 | exit 0, `dangling=0`, `ids_cited=3` | CRLF rows around a fence all parsed → false green |
| 09 | exit 0, `dangling=0`, `ids_cited=1` | tab-named file dropped entirely (`ls-tree --name-only` C-quotes it, so `endswith(".md")` is false); only `ok.md` counted → **false green** |
| 10 | exit 0, `dangling=0`, `ids_cited=1` | newline-named file dropped the same way → false green |
| 11 | exit 0, `dangling=0`, `ids_cited=1` | backslash-named file dropped the same way → false green |
| 12 | exit 0, `dangling=0`, `ids_cited=1` | non-ASCII path quoted with octal escapes by git, dropped the same way → false green |

The raw quoting that causes 09–12 is recorded in `git-quoting.txt`, e.g.
`'"corpus/knowledge/has\\ttab.md"'`, `'"corpus/knowledge/\\346\\227\\245\\346\\234\\254\\350\\252\\236/notes.md"'`.
Both disclosed defect classes (D1 fence-blind registry, F1 git-quoted knowledge paths) reproduce on the committed tool;
every failure is a silent exit-0 `dangling=0`, never an unevaluable exit 2.

## RUN COMMAND:

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/w1/ExecResolverTests.files/battery.py \
        /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py        # 2/13, exit 1
# add --keep to leave fixtures; default removes <scratch>/cases. Missing tool path → exit 2. All-pass → exit 0.
```

## SATISFIABILITY PROBE (not the lane fix):

To prove the battery is not over-constrained, a scratch copy of the committed tool with exactly two hunks
(fence-aware `parse_registry`; `git ls-tree -r -z --name-only` + NUL split in `knowledge_bodies`) was run:
**13/13**, exit 0 (`run-reference.txt`), and that probe's own `--selftest` still prints `selftest: 49/49`.
Hunks: `reference-probe.diff`. This is evidence that a correct fix can clear every case, not a proposal for the lane.

## JUNK CONTROLS (the battery discriminates plausible cheats):

| mutant | tally | caught by |
|---|---|---|
| M1 fence-blind + `-c core.quotePath=false` tweak on `ls-tree` | 3/13 | 09/10/11 (quotePath=false leaves tab/newline/backslash quoted → `-z` is required) + all fence cases |
| M3 correct `-z` paths, registry still fence-blind | 6/13 | 01,02,04,05,06,07,08 (fence cases are load-bearing independently of the path fix) |
| M2 correct `-z` paths + over-eager fence toggle (`^\s*` on either char, any length) | 10/13 | 01,02 (length + character), 03 (4-space indent must not open) |

`junk-controls.txt` holds the full output; `mutant_m1_quotepath.py`, `mutant_m2_overeager.py`,
`mutant_m3_paths_only.py` are the wrappers.

## LIMITS:

- Cases 09–12 require git's C-quoting to be bypassed at the byte level (`-z`, or an unquoting parser that also
  survives newlines); a `core.quotePath=false` shortcut is intentionally insufficient, shown by M1.
- The battery asserts an exact dangling set and exit code; a fix that reports the id but exits 0/2 fails (contract
  kill rules allow 1 only).
- Fixtures use git defaults (`core.quotePath=true`) and local-only repos; no network, no sibling lanes, no lane state touched.
- Not tested here (by design): sibling ownership reality, absent `--fleet`, tool selftest size, the real lane run
  (`c58_resolver_cases.py` P4–P7), and whether the census should become fence-aware (contract keeps it fence-blind).
- Read-only use of the lane: only `scripts/id_resolver.py` was read (copied into scratch to run), `git show/log/diff/
  rev-parse` were used; the lane Git index, jj state and all other paths are untouched.

Evidence in `.ufo/waves/round-58/w1/ExecResolverTests.files/`: `battery.py`, `run-current.txt`,
`run-current-clean.txt`, `run-reference.txt`, `junk-controls.txt`, `cmark-oracle.txt`, `verify_cmark.py`,
`git-quoting.txt`, `reference-probe.diff`, `mutant_m1_quotepath.py`, `mutant_m2_overeager.py`,
`mutant_m3_paths_only.py`. Scratch dir removed after the receipts were copied.

VERDICT: battery of 13 cases is satisfiable (correct 2-hunk reference 13/13, selftest 49/49) and discriminating (junk mutants 3/13, 6/13, 10/13); committed tool passes 2/13 — 11 failures are silent exit-0 false greens covering both disclosed defects (fence-blind registry D1 and git-quoted knowledge paths F1).
