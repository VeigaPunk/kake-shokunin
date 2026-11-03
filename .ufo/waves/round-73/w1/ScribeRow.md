# ScribeRow — round 73, wave w1 (kake, attempt 1)

Status: **draft only, read-only**. This seat produced text, not a lane change. Nothing below was written
into `corpus/SOURCES.md`, `LOG.md` or `SCORECARD.md`; the integrator owns those writes. No lane git/jj
mutation, no fixture repo, no subagent, no counter run, no tool install (pacman untouched; no `uv`, `npx`
or binary download used). Scratch: no clone or work tree was created; the one temp file
(`/tmp/s440_sources.txt`, the 162841-byte base `corpus/SOURCES.md` blob per `git cat-file -s`, exit 0) was
deleted in the same command that created it.

Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`
Base revision (all base reads): `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`
Freeze commit (round-73 contract, sources, controls, attack corpus): `4c7c53bc563a66ae0676b468966781f023ae0110`
(`git -C $L merge-base --is-ancestor c1f3d8d4… HEAD` → exit 0; `git diff --name-status c1f3d8d4… HEAD` lists the
eleven round-73 files as `A`).

## Evidence (command, exit code, key output line)

`$L` = `/home/vgpnk/Projects/shokunin/kake-shokunin`, `$B` = `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`.

| # | Command | Exit | Key output |
|---|---|---|---|
| E1 | `git -C "$L" show "$B:corpus/SOURCES.md" \| grep -cE '^\| *S440 *\|'` (also split: `show > /tmp/s440_sources.txt`; `grep -cE … /tmp/s440_sources.txt`) | show 0; grep 1 (grep `-c` exits 1 on a zero count) | `0` — S440 absent at base |
| E2 | `grep -o '<title>[^<]*' "$L/.ufo/waves/round-73/sources/bash-param.html"` | 0 | `<title>Shell Parameter Expansion (Bash Reference Manual)` (title tag on html line 21) |
| E3 | `sha256sum "$L/.ufo/waves/round-73/sources/bash-param.html"` | 0 | `6b0800fd35c7f9fa8bb66d0eae1cd2e8bae7ded09ad6e89460dda2775a13c8e3` |
| E4 | `cat "$L/.ufo/waves/round-73/sources/receipts.txt"` | 0 | sha256 line (same as E3); `2026-11-03T22:33:40Z`; `url=https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html http=200 bytes=30764` |
| E5 | `grep -c -F 'If parameter is unset or null, the expansion of' "$L/.ufo/waves/round-73/sources/bash-param.txt"` | 0 | `2` |
| E6 | `grep -n -F 'If parameter is unset or null, the expansion of' "$L/.ufo/waves/round-73/sources/bash-param.txt"` | 0 | `117:If parameter is unset or null, the expansion of` and `139:If parameter is unset or null, the expansion of word` |
| E7 | `awk 'NR>=114 && NR<=120 {printf "%d:[%s]\n", NR, $0}' "$L/.ufo/waves/round-73/sources/bash-param.txt"` | 0 | `116:[${parameter:&minus;word}]`, `117:[If parameter is unset or null, the expansion of]`, `118:[word is substituted.]`, `119:[Otherwise, the value of parameter is substituted.]` — the located occurrence is the `${parameter:-word}` entry |
| E8 | `sed -n '117p' …/bash-param.txt \| wc -c`; `awk 'NR==117{print length($0)}'`; string-equality test of that line against the quote | 0 | `48` bytes (47 chars + LF); `47`; `IDENTICAL` — the quote is one whole raw line |
| E9 | `printf '%s' 'If parameter is unset or null, the expansion of' \| wc -w` | 0 | `9` |
| E10 | `grep -n -F 'unset or null' …/bash-param.html`; `wc -l` on both files | 0 | html line 117 `109:…tests for a parameter that is unset or null.`, `117:<dd><p>If <var class="var">parameter</var> is unset or null, the expansion of`; html 661 lines, txt 661 lines |
| E11 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-72/controls/{c1-tip-final.txt,c2-tip-final.txt,c1-tip.txt,c2-tip.txt}"` (one call per path) | 0, 0, 128, 128 | `c1-tip-final.txt` EXISTS; `c2-tip-final.txt` EXISTS; `c1-tip.txt` `fatal: path … does not exist in 'c1f3d8d4…'`; `c2-tip.txt` same fatal |
| E12 | `git -C "$L" ls-tree -r --name-only "$B" -- .ufo/waves/round-72/controls/` | 0 | 13 files, including `c1-tip-final.txt` and `c2-tip-final.txt`, none named `c1-tip.txt`/`c2-tip.txt` |
| E13 | `git -C "$L" show "$B:LOG.md" \| grep -n 'controls/c1-tip\.txt\|controls/c2-tip\.txt'` | 0 | `2466:` (round-70 section) and `2505:` (round-72 `§ Measured`, one bullet carrying both tokens); `## Round 72` heading at line 2498; `grep -n 'tip-final'` on base `LOG.md` → no match, exit 1 |
| E14 | `git -C "$L" show "$B:SCORECARD.md" \| grep -n 'c1-tip\|c2-tip'` | 0 | `4775:` (`\| 70 \|` calibration row), `4818:` (`\| 72 \|` calibration row → `controls/c1-tip.txt`), `4819:` (`\| 72 \|` operability row → `controls/c2-tip.txt`) |
| E15 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-70/controls/c1-tip.txt"` | 0 | EXISTS — the round-70 row's identically named pointer resolves under `.ufo/waves/round-70/`, outside C1's scope |
| E16 | `git -C "$L" show "$B:.ufo/waves/round-72/controls/c1-tip-final.txt" \| wc -l` and `… \| grep -n agreement` | 0 | 71 lines; line 70 `C1 gate-status members=28 evaluated=28 mismatches=3 structural=0 agreement=25 scores_held=3/3 met=True`; exactly 1 `agreement` line |
| E17 | `git -C "$L" show "$B:.ufo/waves/round-72/controls/c2-tip-final.txt"` | 0 | 2 lines; line 1 `C2v2 revision=5013c0ee87bda5fee03024488b4e293c4ca7ff16 brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=8 added=8 guard=ok met=True`; line 2 `exit=0` |
| E18 | `git -C "$L" grep -n 'c2-tip-final' "$B" -- .` and `git -C "$L" grep -n 'c1-tip-final' "$B" -- .` (two calls) | 0, 0 | `corpus/lessons/round-72-verifier-spotcheck.md:35` (C1 receipt, `mismatches=3 agreement=25 … met=True`, `exit=0`), `:46` (C2 receipt, `revision=5013c0ee… met=True`), `:59`, `:63`, `:76` (routed defect: the two dead pointers and the real receipts); `corpus/lessons/round-72.md:15-16`; `.ufo/waves/round-72/w1-results.json:46` |
| E19 | `grep -cE '^\| *S440 *\|' "$L/corpus/SOURCES.md"` (working tree) | 1 | `0` — no sibling has inserted S440 yet; `ls -la "$L/.ufo/waves/round-73/w1/"` at probe time lists only `swarm-registry.json` (a sibling later added `ReviewerC2-heldout.txt` to the same untracked dir; not this seat's file) |

## ROW

```ROW
| S440 | Shell Parameter Expansion (Bash Reference Manual) — https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html | docs | A | Bash's `${parameter:-word}` default-value expansion for the lane's shell recipes only, not a claim about other shells | the `${parameter:-word}` entry of the Shell Parameter Expansion section, revision fetched 2026-11-03, retained at `.ufo/waves/round-73/sources/bash-param.html` (sha256 6b0800fd35c7f9fa8bb66d0eae1cd2e8bae7ded09ad6e89460dda2775a13c8e3) with tag-stripped text `.ufo/waves/round-73/sources/bash-param.txt` (quote at line 117) | A default such as `${TMPDIR:-/tmp}` substitutes its word when the parameter is unset or null, so a repoint that keeps the `/tmp` word still falls back to `/tmp` | mined | 2026-11-03 | on-release | `.ufo/waves/round-73/contract.md` |
```

Cell check (E1/E2/E3): 11 cells, no cell contains a pipe (the row splits on `|` into exactly 11 fields);
`id=S440` is absent at base (`0`), so the row is not a duplicate. Column order matches the `## Registry`
header at base `corpus/SOURCES.md:9`.

## GATE

```GATE
url: https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
accessed: 2026-11-03 (receipts.txt: 2026-11-03T22:33:40Z; http=200; bytes=30764; sha256 6b0800fd35c7f9fa8bb66d0eae1cd2e8bae7ded09ad6e89460dda2775a13c8e3)
quote: If parameter is unset or null, the expansion of
line: 117 of .ufo/waves/round-73/sources/bash-param.txt (whole raw line, 47 characters; grep -c -F on that file prints 2, the second occurrence at line 139 belonging to the ${parameter:=word} entry, so the ${parameter:-word} occurrence is 117)
words: 9 (printf '%s' 'If parameter is unset or null, the expansion of' | wc -w -> 9)
```

Provenance cross-check: the retained html is line-aligned with the stripped text (both 661 lines), and html
line 117 is `<dd><p>If <var class="var">parameter</var> is unset or null, the expansion of`; the plain quote
therefore does **not** occur as a contiguous substring of the html (`grep -c -F` → 0, exit 1) — the quote is
grounded in the tag-stripped `.txt`, which is the retained derivative named in the anchor cell.

## LOG_TAIL

```LOG_TAIL
[r73-correction 2026-11-03] Round 72 § Measured (appended; the bullet is kept unedited): the two wave-relative receipt pointers `controls/c1-tip.txt` and `controls/c2-tip.txt` are superseded and name no committed file. The corrected committed receipts are `.ufo/waves/round-72/controls/c1-tip-final.txt` (C1 landed-tip) and `.ufo/waves/round-72/controls/c2-tip-final.txt` (C2 tip).
```

Preconditions for that text, all measured at base: both superseded names are absent
(`git cat-file -e` exits 128 each, E11); both corrected names exist (`cat-file -e` exits 0, E11/E12); the
round-72 entry is the one place in `LOG.md` where the two tokens co-occur (`LOG.md:2505`, E13); the
correction names each superseded token exactly once, as superseded, and points only at resolving paths.

## SCORECARD_TAIL

```SCORECARD_TAIL
[r73-correction 2026-11-03] Round 72 rows (appended; the two rows above are kept unedited): their receipt pointers `controls/c1-tip.txt` (calibration row) and `controls/c2-tip.txt` (operability row) are superseded and name no committed file. The corrected committed receipts are `.ufo/waves/round-72/controls/c1-tip-final.txt` and `.ufo/waves/round-72/controls/c2-tip-final.txt`.
```

Preconditions: the rows whose first cell is `72` and cite the tokens are exactly `SCORECARD.md:4818`
(calibration → `controls/c1-tip.txt`) and `SCORECARD.md:4819` (operability → `controls/c2-tip.txt`) at base
(E14). `SCORECARD.md:4775` also carries `controls/c1-tip.txt`, but its first cell is `70` and that pointer
resolves under `.ufo/waves/round-70/` (E15) — it is deliberately outside the correction and the appended
line is scoped to the round-72 rows so no reader infers that round-70 pointer is dead.

## Findings

1. **Both deliverable texts are drafts; none is applied.** Any claim that `LOG.md`, `SCORECARD.md` or
   `corpus/SOURCES.md` already carry the correction or the S440 row is false at this revision: base
   `LOG.md` has no `tip-final` match (E13), base `SOURCES.md` has no S440 row (E1), and the only round-73
   file in `w1/` is `swarm-registry.json` (E19).
2. **The quote has two occurrences in the stripped text, not one.** `grep -c -F` prints `2` (lines 117 and
   139); line 139 belongs to the `${parameter:=word}` entry. The GATE block pins the `${parameter:-word}`
   occurrence at 117 with that reason stated, so the count is not reported as `1`.
3. **The quote is not a contiguous substring of the retained html** (`grep -c -F` → 0, exit 1) because the
   html wraps `parameter` in `<var class="var">`. The html and txt are line-aligned (661 lines each, E10),
   so line 117 of the derived text is the anchor for html line 117. No sha256 or fetch defect: the retained
   html hash equals the `receipts.txt` hash (E3/E4).
4. **The stripped text retains HTML comments and entities.** `bash-param.txt` still carries the leading
   Texinfo comment and renders the entry heading as `${parameter:&minus;word}` (E7), because the stripping
   removes tags but not comments/entities. This is why the anchor cell names the entry in shell form rather
   than quoting the literal `.txt` heading.
5. **`controls/c1-tip-final.txt` is a 71-line multi-counter dump, not a single C1 receipt.** Its last line
   (70) is the C1 gate-status line with `agreement=25 … met=True`; lines 1-69 are round-48/49 counter runs
   at revision `5013c0ee…` (E16). The corrected pointer resolves and the C1 value the round-72 rows claim
   (`agreement 25`) is present, but anyone citing the file should cite line 70.
6. **`controls/c2-tip-final.txt` records `revision=5013c0ee…`, not the round-72 base or landed revision**
   (E17). The round-72 non-author spot-check already documents that exact string for this receipt
   (`corpus/lessons/round-72-verifier-spotcheck.md:46`), so the file matches its documented content; the
   mismatch between the receipt's revision field and the round-72 revisions is pre-existing bookkeeping,
   outside this seat's write scope, and is not introduced by the correction text (which makes no revision
   or magnitude claim).
7. **A same-named pointer exists under round 70 and is live.** `LOG.md:2466` and `SCORECARD.md:4775` cite
   `controls/c1-tip.txt`, which exists at `.ufo/waves/round-70/controls/c1-tip.txt` (E15). The two
   correction tails name the token only as superseded *in round 72*, so they cannot be read as killing the
   round-70 pointer.

## Out of scope / not done

- No edit to `corpus/SOURCES.md`, `LOG.md`, `SCORECARD.md`, `SKILL.md`, the contract, the attack corpus, the
  frozen counters, or any file under `.ufo/waves/round-72/`; no git/jj mutation anywhere (the lane's `git
  status --porcelain` was read, not changed: the pre-existing untracked `w1/`, `w1.ready{,.dispatched}` and
  `w1-dispatch.json` markers were left as found).
- No frozen counter was run (`c66_gate_status_hostportable.py`, `c70_pointer_audit.py`, `c72_tmp_v2.py`,
  `c73_wave_pointers.py`, `c73_tmp_v3.py`, `scripts/freshness-sweep.mjs`); no C1/C2/C3 predicate is claimed.
  This seat's ROW/GATE/tails are text; whether an appended correction satisfies C1 is for
  `c73_wave_pointers.py` and the closure to measure, not for this report to assert.
- No build, lint, test or freshness sweep was run; none is in this seat's acceptance.
- No tool install or upgrade (pacman untouched per the host-wide pause; no `uv`/`npx`/binary channel used).
- No scratch tree was created, so none remains; the single temp file was removed (see header).

## Artifact paths

- Report: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-73/w1/ScribeRow.md`
- Read (base, committed bytes): `corpus/SOURCES.md`, `LOG.md`, `SCORECARD.md`,
  `corpus/lessons/round-72-verifier-spotcheck.md`, `corpus/lessons/round-72.md`,
  `.ufo/waves/round-72/controls/c1-tip-final.txt`, `.ufo/waves/round-72/controls/c2-tip-final.txt`,
  `.ufo/waves/round-72/w1-results.json` (path listing only)
- Read (working tree, freeze commit `4c7c53bc` content): `.ufo/waves/round-73/contract.md`,
  `.ufo/waves/round-73/sources/bash-param.html`, `.ufo/waves/round-73/sources/bash-param.txt`,
  `.ufo/waves/round-73/sources/receipts.txt`
