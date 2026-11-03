# ReviewerC2 — attack seat for C2 (round 73, wave w1)

Scope: contract `.ufo/waves/round-73/contract.md` §C2 (read, not restated), frozen corpus `attack-corpus.txt` (read only),
frozen counter `.ufo/waves/round-72/c72_tmp_v2.py` (read only, sha256 `af2f0c9c…6e6ca`, identical at base c1f3d8d4 and on disk).

## Headline

- c72 `line_findings` accepts **9 of 11** frozen attack lines (k ≥ 1 holds; the do-nothing control is not void) and **16 of 19** held-out attack lines.
- c72 rejects **0 of 4** frozen legit lines and **0 of 6** held-out legit lines.
- The C2 predicate does **not** close H3 (symlink) or H4 (PHRASE pin), and the corpus cannot express H3 at all. The title "closes the four routed c72 holes" is not supported by the predicate (F1).
- Verdict-changing findings: F1, F2, F3, F8, F9. Untestable-as-written: F4, F5, F6, F12.

## Commands run (cwd noted; all exit codes observed)

1. `git -C <lane> show c1f3d8d4…:.ufo/waves/round-72/c72_tmp_v2.py | sha256sum` → `af2f0c9c6b7ba04f…6e6ca`, rc 0; `sha256sum <lane>/.ufo/waves/round-72/c72_tmp_v2.py` → same hash.
2. `(cd <lane> && python3 -B .ufo/waves/round-72/c72_tmp_v2.py --lane . --revision c1f3d8d4…)` → `C2v2 revision=c1f3d8d4… brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=8 added=8 guard=ok met=True`, exit 0 (matches `controls/c2-c72-base.txt`).
3. `python3 -B c72_tmp_v2.py --selftest` → `C2v2 selftest 11/11`, exit 0.
4. `drive.py` (importlib of c72 from the round-72 path, `-B`; calls `line_findings` per line):
   - frozen corpus: `SUMMARY frozen: c72_accepts_attack=9 of 11; c72_rejects_legit=0 of 4`, exit 0. The two rejected attack lines are frozen file lines 13 (`` `cp …` `` span) and 14 (bare `cp` imperative).
   - held-out (before the last addition): `c72_accepts_attack=16 of 18; c72_rejects_legit=0 of 6`, exit 0.
5. Held-out line 23 added (`rm -rf /tmp/kake-r13/ (historical record)`), then `drive2.py` re-run over the 29-line file: attack lines 19, c72 accepts 16 (lines 05–08, 10–21), rejects 09, 22, 23; legit lines 24–29 all accepted. Exit 0. (The summary's legit field in that script was a printing error; the per-line rows are the evidence for `c72_rejects_legit=0`.)
6. H3 fixture (`mktemp -d -p /fast/scratch/hyaku/kake-r73/ReviewerC2`, `git init`, toplevel asserted equal to the fixture dir; `SKILL.md` committed as mode 120000 → `notes/extra.md`; commit with `-c user.name=kake-scratch -c user.email=kake@scratch.local.`): `git ls-tree HEAD SKILL.md` → `120000 blob … SKILL.md`; c72 `show(D,"HEAD")` → `['notes/extra.md']`; `line_findings` on it → `(0, 0, 0)`; the target bytes `cp state/x /tmp/kake-r13/live/x.json (historical record, not an executable instruction)` → `(0, 1, 0)`. Exit 0.
7. H4 (in-memory constant only; frozen file not edited): line `rm -rf /tmp/kake-r13/ (historical record)`; real `PHRASE='not an executable instruction'` → `line_findings (0, 0, 1)`; with `PHRASE='historical record'` → `(0, 0, 0)`. Exit 0.
8. `git -C <lane> cat-file -e HEAD:.ufo/waves/round-73/attack-corpus.txt` → rc 0; same at `c1f3d8d4…` → rc 128 (`exists on disk, but not in c1f3d8d4`). Disk sha256 `9da8778285b3e8c0…9ed44b` = `git show HEAD:…| sha256sum` (identical).
9. `sources/bash-param.html` sha256 → `6b0800fd35c7f9fa…a13c8e3` (matches the contract prefix/suffix). `sources/bash-param.txt` contains "Bash tests for a parameter that is unset or null" (8 hits), rc 0. `sources/receipts.txt` holds a timestamp, URL, `http=200 bytes=30764`; `grep -c S440` → 0, rc 1.
10. Base SKILL.md (`git show c1f3d8d4…:SKILL.md`, 1397 lines): python scan for `c72`/`c71`/`tmp_v`/`round-72` → no line names `c72_tmp_v2.py` or `c71_tmp`; the only round-72 hit is row 1253 (`selftest-tally-counter`). Its 4 `/tmp/` lines (27, 227, 356, 359) are all annotated and clean under c72.
11. `git cat-file -t cc6b4e0b…` → `commit`, rc 0; `git merge-base --is-ancestor cc6b4e0b… c1f3d8d4…` → rc 0.

Installed tools: none (no tool install was needed). Artifact observed, not created by this seat: `.ufo/waves/round-72/__pycache__/c72_tmp_v2.cpython-314.pyc`, mtime 2026-11-03 19:40:15 -0300. Every import I ran used `python3 -B`, which suppresses bytecode writes; I did not touch the directory. Origin unverified.

## Held-out corpus (file line numbers; c72 `line_findings` result)

| file line | class / expected | shape | c72 |
|---|---|---|---|
| 05 | attack | A01 heredoc body after `payload step: cat <<'EOF' > /tmp/…` | accepts |
| 06 | attack | A02 `restore: [cp state/x](/tmp/…)` markdown link | accepts |
| 07 | attack | A03 `snapshot ok; cp … /tmp/…` second segment after `;` | accepts |
| 08 | attack | A04 `workdir: BK=$(mktemp -p /tmp/) && cp …` | accepts |
| 09 | attack | A05 raw TAB before `cp` | **rejects** (command=1; c72 strips whitespace) |
| 10 | attack | A06 U+200B zero-width space before `cp` | accepts |
| 11 | attack | A07 `env KAKE=1 TMPDIR=/tmp/… node run.mjs` | accepts |
| 12 | attack | A08 `doas cp …` | accepts |
| 13 | attack | A09 `unlink /tmp/…` | accepts |
| 14 | attack | A10 `note: ``cp … /tmp/…`` ` double-backtick span | accepts |
| 15 | attack | A11 `scp state/x host:/tmp/…` | accepts |
| 16 | attack | A12 `then cd /tmp/… && cp …` | accepts |
| 17 | attack | A13 `find … -exec cp {} /tmp/… \;` | accepts |
| 18 | attack | A14 `${TMPDIR-/tmp/…}` (no colon) | accepts |
| 19 | attack | A15 `${XDG_RUNTIME_DIR:-/tmp/…}` | accepts |
| 20 | attack | A16 `result: $(cp … /tmp/…)` | accepts |
| 21 | attack | A17 `eval "cp … /tmp/…"` | accepts |
| 22 | attack | A18 truncated annotation `not an executable)` | **rejects** (prose=1) |
| 23 | attack | A19 `rm -rf /tmp/… (historical record)` | **rejects** (prose=1); accepted if PHRASE is truncated (H4 repro, item 7) |
| 24–29 | legit | prose / dated absence / `grep`-span / "used cp" prose / TMPDIR-unset history | all accept (clean) |

Frozen corpus under the same function: attack lines 04–12 accept (includes H1 `${TMPDIR:-/tmp}` at 04–05, H2 rsync/rm/env/cd/sudo at 06–12); 13–14 reject.

Control reading of H2 as stated in C2: all six named H2 shapes (`rsync`, `rm`, `cd … &&`, env prefix, `sudo` prefix, double-backtick) are confirmed accepted by c72 (frozen 06, 07, 10, 08, 12; held-out 14). H1 confirmed (frozen 04, 05).

## Findings on the contract text (§C2 and its counter bullet)

Each finding names the sentence, the reproduction (item numbers above), and whether it changes the verdict.

**F1 — scope of "closes the four routed c72 holes" and "Attack lines carry H1–H4 shapes". Verdict-changing.**
- The predicate and the corpus cover H1 and H2 only. H3 (symlink) has no corpus line (a line cannot express a symlink) and no predicate clause. Item 6 reproduces it: c72 reads the 14-byte link text and returns `(0,0,0)` while the target carries a command-bearing `/tmp` line scoring `command=1`. A c73 that still reads symlinks as link text would meet C2.
- H4 (PHRASE not pinned) has no predicate clause and no corpus line that exercises it. At line level c72 already rejects a truncated annotation (held-out 22, 23), so the hole exists only in the PHRASE constant (item 7: real `(0,0,1)`, truncated constant `(0,0,0)`).
- The counter bullet's "Attack lines carry H1–H4 shapes" is false: none of the 11 frozen attack lines is a symlink or a PHRASE-truncation shape (checked by reading all 11).
- The sentence "(H4) the PHRASE constant is not pinned: a truncated phrase (`not an executable instruction`, `historical record`) passes" is not testable as written: its first example is the full phrase, not a truncation, and it does not say which constant to pin.

**F2 — "every `attack` line in the corpus is a finding" with `--corpus`, versus the `--revision` gate. Verdict-changing (not reproduced: no c73 counter yet).**
The predicate never requires the corpus run and the `--revision` scan to share one line function. A counter that routes the corpus through a separate function, while SKILL.md is checked by the old logic, meets C2 with "c73 accepts 0 of A" measured on code the gate never runs. "Before → after" is measured on the function, not on the file.

**F3 — corpus-only pass; no held-out or perturbation clause. Verdict-changing (not reproduced).**
A counter that allowlists the exact 11 frozen attack strings (and 4 legit strings) satisfies every clause of C2. Items 4–5 show the held-out lines separate a c72-style rule set (accepts 16 of 19) from a correct one, so the closure should run the held-out file as a routed check (c73 must accept 0 of 19 and reject 0 of 6). This is a routed check only; it is not a new predicate.

**F4 — "every `attack` line … is a finding" and "every `legit` line is clean": not testable as written.**
No per-line output format is specified for `--corpus`. "Finding" granularity (per line or per token occurrence) is not defined. "Clean" is defined only at revision level (`findings=[]`). The closure cannot read per-line verdicts from the stated command.

**F5 — "`--selftest` exits 0 with the full case count passing": not testable as written.**
No case count is pinned. c72 reports its own denominator (`C2v2 selftest 11/11`, item 3); a counter that deletes cases still prints N/N. "Full" needs a pinned number or a pinned case-name list.

**F6 — "the SKILL.md gate registry gains exactly one row naming `c73_tmp_v3.py`" (and "beyond line 935"): not testable as written; no precedent.**
Item 10: base SKILL.md has no line naming `c72_tmp_v2.py` or `c71_tmp`, so round-72's counter was never registered there, and no convention exists to follow. The "gate registry" is a set of per-round tables spanning lines 208–1356; "row" and the placement rule are not defined; "beyond line 935" appears only in the Scope paragraph, not the predicate. Low severity; the closure must choose the target before it can check the clause.

**F7 — "legit lines are the lane's own dated-absence annotations": description mismatch. Low.**
Frozen legit line 17 (`cp state/probe-latest.json "$BK/probe-latest.backup.json" (repaired recipe; …)`) is a repaired recipe with no `/tmp` token. It can only catch command-verb overreach, not `/tmp` overreach. Only 3 frozen legit lines carry a token, all annotated, so the legit side is thin.

**F8 — corpus provenance is contradictory; the freeze identity is not named. Verdict-changing for the independence claim.**
The contract says the corpus is "Frozen before any seat of wave `w1` ran" and, in the counter bullet, "written by the executor seat `ExecC2Counter` into `w1/` and promoted by the integrator". The file is not under `w1/`; it sits at the round root (item 8). It is absent at base (rc 128) and present at HEAD. The contract never names the freeze commit it calls "this commit". If the counter's author wrote the test set, the "frozen before counters" claim does not hold.

**F9 — corpus bytes are not pinned. Verdict-changing if the file is edited after freeze.**
The predicate runs `--corpus .ufo/waves/round-73/attack-corpus.txt` (a working-tree path). No sha256 is pinned and no kill rule covers a changed corpus. Current disk and HEAD both hash to `9da8778285b3e8c0…9ed44b` (item 8), but nothing in C2 prevents a later edit.

**F10 — the c72 guard base differs from the contract base; not disclosed. Low.**
The c72 counter's `BASE` constant is `cc6b4e0b…`, an ancestor of `c1f3d8d4…` (item 11), while the contract cites base `c1f3d8d4…` for "c72 exits 0 met=True". The `met=True` result therefore compares additions and removals against `cc6b4e0b`, not against the stated base. The contract does not say which base c73's guard uses.

**F11 — "the claim requires k ≥ 1" is not in the kill-rule list; "the claim is void" is not a defined outcome. Low.**
Current k is 9 of 11 (item 4), so the outcome is unaffected now. The control paragraph and the kill rule should name the same outcome.

**F12 — sourced claim S440: identity not closed in receipts. Low.**
The contract's sha prefix/suffix for `bash-param.html` matches (item 9), and the page text supports `${parameter:-word}` semantics. But `sources/receipts.txt` does not contain the string `S440` (item 9), so the S-id to file binding is not in the receipts file the contract cites.

Confirmed (no finding): the H1 and H2 descriptions in the C2 "Before" paragraph reproduce exactly (items 2, 4).

## Residual risk and verification gaps

- No c73 counter exists in this seat's view; F2, F3 and F9 are routed as reasoning, not as executed reproductions.
- The held-out corpus is a routed check. It does not establish that the executor's counter is wrong or right.
- Base SKILL.md has only 4 `/tmp/` lines (item 10), all annotated and clean under c72. The c73 base-clean requirement in C2 is therefore low-exposure, but it has not been run against a c73 counter.
- Symlink reproduction (item 6) used a single fixture shape (`SKILL.md` → relative file). Other link targets were not tested.
- Scratch tree: `/fast/scratch/hyaku/kake-r73/ReviewerC2/` created for the drivers and the fixture; removed at the end of the seat (see the final cleanup step).
