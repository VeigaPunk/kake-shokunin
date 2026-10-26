# ReviewerQualitySkill

Reviewed text: `corpus/QUALITY.md` § Round-57 criteria (5 criteria, lines 1219–1256), `SKILL.md` § Round 57 gate registry
additions (lines 1263–1280; 3 gate rows + 1 tool row, 8 cells each, verified `pipes=9` on every row), `PROVINCE.md` § Round-57
(lines 429–447), `corpus/README.md` coverage rows (lines 73–74) and ground-map row (line 104, preamble 77–86, absence note
119–121). Read at `4b8c73050470ada9e6583f3b12d659d1bed6a17f`. Lane HEAD is `51921b97124616d8526160231aec5c5708c74f3d`
(W2 spec/dispatch); `git diff --stat 4b8c730 -- corpus/QUALITY.md SKILL.md PROVINCE.md corpus/README.md` is **empty**, i.e. the
working tree is identical to the named revision for all four files (only untracked W2 reports differ).

## DEFECTS

**1. `SKILL.md:1274` (id-resolver-gate, Self-test cell) — the "wave-1 and wave-2 seats scored the gate against a constant
printer (3/5) and the genuine tool (5/5)" clause is unsupported by any committed seat report.** At `4b8c730`
`git ls-tree -r 4b8c730 .ufo/waves/round-57/w2` lists no files (the W2 directory is untracked at HEAD), so no wave-2 seat had
scored anything when the row was committed. The only committed 3/5 measurement, `w1/CritCheatC2.md:89`, is labelled
"patched gate" and the report itself says the patch was "not applied to the lane" (`w1/CritCheatC2.md`, PROPOSED GATE PATCH);
it is that seat's prototype, not the shipped gate. The committed genuine-tool 5/5 (`w1/ExecResolverBuild.md:31`, `:86`) reports
green `104/104/0`, the version-1 G5 shape (the shipped gate's reference prints `106/106/0`), so it is a version-1 figure too.
Exact fix — replace the cell with: "the gate has no selftest of its own; the tool it gates has
`python3 -B scripts/id_resolver.py --selftest` (33 checks, generated sandbox lanes and siblings); measured on the shipped gate:
the genuine tool 5/5 exit 0 and a constant printer 3/5 with G3 and G5 failing (`.ufo/waves/round-57/w2/ReviewerQualitySkill.md`;
the wave-1 3/5 in `w1/CritCheatC2.md` was against that seat's patch, not this file)". (confirmed by running the tree listing,
the two w1 reports and the gate.)

**2. `corpus/QUALITY.md:1245` (criterion 3, Falsifier) — the named failing conditions are wrong.** Measured against the shipped
gate, three shapes separate cleanly: a **green-only constant printer** (no red branch) scores **2/5**, G3, G4 and G5 FAIL; a
**constant printer with the five red-revision lines hardcoded** — the wave-1 cheat's mechanism — scores **3/5** with **G3 and
G5 FAIL and G4 PASS**. No printer I built fails exactly "G3 and G4"; the 3/5 shape the criterion and the row care about fails
**G3 and G5**. Exact fix: "… must print `5/5` for the genuine tool and fails a constant printer at `G3` and `G5`
(`G3_fixture`, `G5_green`; a printer that also drops the hardcoded red-block lines drops to 2/5, `G4_red_before` failing as
well)." The same wrong parenthetical is in `contract.md:144` ("against a constant printer: 3/5 (G3, G4 fail)") — outside my
file set but it is the origin of the sentence; flagged for the L1. (confirmed by running, both printers, see COMMANDS RUN 7–8.)

**3. `corpus/QUALITY.md:1228, :1237, :1244, :1250, :1256` — every lesson Grounding dangles.** All five criteria cite
`corpus/lessons/round-57.md` §Mistakes (`landing`, `attribution`, `vacuous`, `vacuous`, `reference-drift`) and criterion 2 also
cites `§Rejects`; at `4b8c730` and at HEAD that file is 84 lines and both sections are unfilled placeholders —
`## Rejects` = "(filled after wave 2 re-reads each reason against the page)", `## Mistakes` = "(filled below)"
(`git show 4b8c730:corpus/lessons/round-57.md`). `PROVINCE.md:443` has the same dangling `§ Rejects` pointer. Exact fix: land
the four drafted mistake rows (labels `landing`, `attribution` and the two others already drafted in
`w1/ScribeLessonMistakes.md:12-15`) and fill `§ Rejects` before the criteria are published, or repoint the citations to the
seat reports that hold the text. (confirmed by reading the file at both revisions.)

**4. `corpus/QUALITY.md:1228` and `:1238` — subsection numbers that do not exist.** `corpus/lessons/round-56-verifier-spotcheck.md`
has `## 6. Defects routed to the lane` as a numbered list of items 1–4 and no `### 6.1`/`§6.2` headings; §6 item 1 is the r56
receipt relabel and item 2 is the S388 reject reason — exactly the two facts cited. `§4` resolves (line 71). Exact fix:
"§6 item 1" and "§6 item 2". (confirmed by running the heading list.)

**5. `SKILL.md:1275` (quote-truth counter, Verdict map) — exit 64 is missing and the usage claim is half-true.** The cell says
"`2=could-not-evaluate` (…); usage errors also exit 2 (`ap.error`)" with no 64 row, but the counter's own usage path returns
64: `python3 -B .ufo/waves/round-57/c57_quote_truth.py` (no args) prints `usage: --revision is required unless --selftest is
used` and exits **64** (code `.ufo/waves/round-57/c57_quote_truth.py:1339-1342`; its docstring line 46 says "64 usage").
Argparse-level errors do exit 2 (`--bogus-flag` → 2). Exact fix: "…; usage errors exit 2 via `ap.error` (an unrecognised
option) and 64 when `--revision` is missing without `--selftest`". (confirmed by running.)

**6. `SKILL.md:1273` (receipt-pin-counter, Pinned values cell) — names `measured.json` as frozen proof; no such file exists.**
`git ls-tree -r 4b8c730 | grep measured` returns only round-20 files; `find . -name 'measured.json'` is empty in the working
tree too. The counter requires it (`c57_receipt_pins.py:71, :225`), so it will be produced at measurement. Exact fix: append
"(landed with the C1 receipt)" after `measured.json`, or drop the name until it exists. Minor. (confirmed by running.)

Non-defect worth recording: `corpus/README.md:83` ("160 rows") carries no in-line command, but neither do the r55/r56 counts
in the same preamble; the number is true (§ACCURATE) and the omission is the existing convention, not a round-57 introduction.

## COMMANDS RUN

1. `git cat-file -t 4b8c730…` → commit; `git diff --stat 4b8c730 -- <4 files>` → empty (working tree matches).
2. `python3 -B .ufo/waves/round-57/c57_receipt_pins.py --selftest` → **48/48**, exit 0, 3.5 s; the output contains
   `relabel on a merged side branch`, `rename plus relabel in one commit`, `measured revision is not an ancestor`,
   `receipt deleted`, `a receipt moved out of the population counts as vanished`, `claim 3 body is a bare pin`,
   `claim 2 body records a failed run`, `stripped then re-pinned yields two relabels`, `errata names nothing git shows`,
   `errata wrong 'to'`, `errata wrong commit`, `CLI usage error exits 64`.
3. `python3 -B scripts/id_resolver.py --selftest` → **33/33**, exit 0.
4. `KAKE_R57_SELFTEST_REV=b9a5d012f7fd python3 -B .ufo/waves/round-57/c57_quote_truth.py --selftest` → **101/101**
   (baseline 8/8, 89 fixtures), exit 0. The five case identifiers named in criterion 4 exist as `@case(...)` in
   `c57_quote_truth.py:1154-1172` (they are identifiers, not printed lines).
5. Entry commands, verbatim: C1 `--root . --revision 51921b9…` → exit 1,
   `new_receipts=0 scorecard_pin=0 met=False` (unmeasured round, as expected); C2 `--root . --revision 4b8c730…` (default
   fleet) → **5/5 met=True exit 0**, G4 `summary=(99,94,5,5,0)`, G5 `(106,106,0,0,0)`; C3 `--root . --revision 51921b9…` →
   **8/8 met=True exit 0** (C1–C8 PASS).
6. Exit-code probes: C1 no-args 64, `--revision deadbeef` 2; C2 no-args 64, bad rev 2; C3 no-args 64, `--bogus-flag` 2,
   bad rev 2; tool no-args 64, bad rev 2. `c57_idresolver_gate.py --selftest` → 64 (case 1274's "no selftest of its own" holds).
7. Green-only constant printer, committed in a `git clone` of the lane at `4b8c730` (`$D`, `rev-parse --show-toplevel` = `$D`,
   `-c user.name=selftest -c user.email=selftest@local`), fleet = temp dir of symlinks to every `*-shokunin` except the lane:
   **2/5**, G3, G4, G5 FAIL, exit 1.
8. Same clone, printer with the five `3994101` DANGLING lines hardcoded (copied from a real tool run): **3/5**, G3 FAIL,
   **G4 PASS**, **G5 FAIL**, exit 1.
9. Criterion 2 grep pair: `grep -c '共通の規格' corpus/lessons/round-56.md` → **0**; `… .ufo/waves/round-56/sources/S388.html` → **1**.
10. Criterion 5 pair: `id_resolver.py --root . --fleet /home/vgpnk/Projects/shokunin` → `ids_cited=106 … dangling=0`, exit 0;
    `--revision 3994101dba2…` → exit 1, exactly S367 S372 S373 S390 S409, all `owners=kotodama-shokunin`.
11. Row counts: `awk` over `## Registry` — `4b8c730` **160**, base `28fa0b23` **158**, `fcaf4b85` **155**, `e48354b7` **156**
    (README preamble consistent). `grep -nE '^\| S42[12]' corpus/SOURCES.md` → lines **167 (S421)** and **168 (S422)**; base
    registry has 0 such rows; both entry paths absent at `28fa0b23`.
12. Ground-map ref: `awk '/^## Round-57/{f=1} f&&/Frontier knowledge/{print NR; exit}' PROVINCE.md` → **441**; `PROVINCE.md:22-30`
    is the `## Frontier` list as the preamble says.
13. Content spot-checks: S422 body prints 发布日期：2016-06-30, "能识别协议死链，以及大多数内容死链、跳转死链等低质网页", "大约几天内就可以处理掉",
    and "索引展现时效性提升，原来是 10 天左右，现在提升 40%~80%" (index display); S421 prints 发布日期：2022-09-09.
    `sha256sum sources/S42{1,2}.html` equals `BODY_SHA256` in the counter and the same digests are in
    `sources/receipts.json` at the contract commit `b9a5d012` (counter at that commit had `HELD_BODY_SHA256 = {}` but the
    receipts — the provenance the criterion names — already carried both digests). Entries cite no S408; kotodama holds S408
    as a British Museum record (another document), as criterion 5 states.
14. Tool installs: none.

## ACCURATE

- Tallies all reproduce: 48 (C1 selftest), 33 (tool selftest), 101/101 with 89 fixtures (C3 selftest), matching
  `SKILL.md:1273-1276` and `QUALITY.md:1230, :1245, :1251`.
- `SKILL.md:1273` base control `undisclosed_relabels=6`, exit 1; `:1274` base `0/5` exit 1; `:1275` base `0/8` exit 1 — all
  three v2 control files exist with exactly those values.
- Verdict maps for C1 (0/1/2/64), C2 (0/1/2/64) and the tool (0/1/2/64) match observed exits; C3's 0/1/2 match (see defect 5
  for 64).
- `SKILL.md:1274` kinds/flags: `--fleet` present; snapshot check is real (`c57_idresolver_gate.py:325` raises unevaluable on a
  live/snapshot mismatch); "no selftest of its own" true.
- `SKILL.md:1275` digest pinning and `:1276` red-before claim are exact (five ids, kotodama owner, exit 1) — reproduced directly.
- Criteria 1–5 each have a Grounding *path* that exists (`controls/base-c1-receipt-pins-v2.txt`, spotcheck §4,
  `w1/CritCheatC2.md`, `w1/CriticControlsSizing.md` (21-line stub 5/5, `:70/:159`), `w1/CritCheatC3.md` (13 junk files, `:133`),
  `w1/CriticC3Counter.md` A1/A2 (`:20/:32`), `scripts/id_resolver.py`, `considerthese/2026-10-25.md` proposal 2 (`:27`),
  `w1/ExecRelabelDiffs.md` (12 re-runs, bodies identical)); only the lesson pointers dangle (defects 3–4).
- Falsifiers 1, 2, 4 and 5 execute and can fail: C1's prints `met=False` today (no receipts yet) and the selftest carries the
  pin-blind cases it names; the grep pair prints 0/1; the C3 selftest names the five hostile cases; the resolver exits 0 in
  green and 1 on the five ids in red.
- `PROVINCE.md:429-447` content matches the retained bodies (two kinds, HTTP 200 content kind, 404-only submission tool,
  Spider 3.0 scope, few-days handling, protocol dead link preferred, 10-day/40–80% in index display, dates 2022-09-09 /
  2016-06-30, "no URL was served under test and no crawl was observed").
- `corpus/README.md` rows 73, 74, 104 and the absence note (119–121) are true; "160 rows" and "158 at base" verified; the
  ground-map line reference `PROVINCE.md:441` is correct.
- No credential material, tokens or private URLs appear in the reviewed text.

Residual risk: the constant-printer probe ran on a `git clone` with a symlink fleet rather than in-place; the sibling set equals
the lane's real one (all `*-shokunin` except the lane), and G5's reference (`106/106/0`) matches the in-place run, so the 3/5 and
2/5 scores are representative. I did not test the C3 counter's exit-2 paths for malformed `mirror-pin.json` (only the revision
path), nor the gate's snapshot-mismatch exit 2.

VERDICT: registry rows and criteria are numerically sound and their falsifiers execute, but six text defects stand — an unsupported "wave-1 and wave-2 seats … 3/5 and 5/5" attribution (SKILL.md:1274), a wrong failing-condition pair "G3 and G4" that is measured as G3 and G5 (QUALITY.md:1245), five dangling lesson/report section citations (QUALITY.md:1228,1237,1244,1250,1256; PROVINCE.md:443), a missing exit-64 in the C3 verdict map (SKILL.md:1275), and `measured.json` named before it exists (SKILL.md:1273).
