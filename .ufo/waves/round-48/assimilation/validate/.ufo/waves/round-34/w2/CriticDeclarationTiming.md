# KakeR34.CriticDeclarationTiming — declared-before-data and post-finding discipline, round 34

Axes: operability, freshness. Read landed state with `git show` only; all writes in sandbox
`/fast/scratch/hyaku/kake-r34/w2/CriticDeclarationTiming/`. No network. No tools installed.
Times are UTC (lane commits are -03:00; file times are mtimes, and mtimes can be changed, so a time taken from an mtime is marked [INFERENCE]).

## Timeline
- 20:52:08Z d08d8de authored → 20:57:39–42Z S067–S072 opened (receipts.json accessedUtc) → 21:00:16Z d08d8de committed (declaration, matrix, counters).
- 21:00:35–37Z before receipts written (mtime) → 21:01:53Z a2fe31b → 21:05:22Z wave 1 dispatched (`w1-dispatched-at.txt`).
- 21:07:10Z first tool to score 28/28, sandbox efacac6 (`ExecLinkPreviewGate`) → 21:07:36Z hollow C2 0cce15f0 → 21:07:54Z lookup C1 dcef39b5 → 21:09:03Z `CriticDeclarationFit.md` written (mtime).
- 21:08:44–21:09:47Z S073–S077 opened → 21:09:09Z final tool 7cc3587 → 21:10:28Z 5613071 (tool) → 21:10:36Z c1-at-5613071 → 21:10:52Z ExecHollowControlC2.md → 21:10:59Z real-input receipt.
- 21:12:52Z lookup-control and hollow receipts → 21:12:59Z selftest receipt → 21:13:49Z 9ef758c (C2 entry, rows, lesson) → 21:18:49Z 24a1647.

## Findings
1. PASS — the declaration and both counters were frozen before any wave-1 data or finding. `git diff d08d8de 24a1647 -- c1-matrix.json c1_matrix_count.py c2_source_census.py` is empty (exit 0). Every receipt carries counterSha256 fc72d855… (C1) or ee7461b9… (C2). The SCORECARD diff from d08d8de to 24a1647 only appends text and adds the capability row, so the declaration section is unchanged.
2. NOTE (freshness, not a defect) — S067–S072 were opened at 20:57Z, five minutes after d08d8de was authored (20:52Z) and three minutes before it was committed (21:00Z). `census-before.txt` is in that same commit. So the declarer had the source text and the census numbers before freezing. `lessons/round-34.md:31` says the sources were "opened at 20:57Z before the declaration"; that is true against the commit time only. The fact that condition (e) is already satisfied by the published before-receipt is already disclosed (`CriticSeparability` 4).
3. PASS — the behaviour that counts for C1 was fixed before the lookup finding existed. efacac6 scored 28/28 at 21:07:10Z, 44 s before lookup commit dcef39b5. The only behaviour change after that, 7cc3587 at 21:09:09Z, removes a try/except. The landed 5613071 differs from 7cc3587 only in the module docstring: the two syntax trees are equal once the docstring is removed (sandbox `tool-w1-vs-landed.diff`; sha256 56ec5b30… vs 8dd00182…). The L1's docstring edit is labelled in the 5613071 commit message and in the LOG round-34 entry.
4. DEFECT (low, false provenance) — the docstring the L1 edited after the findings cites S073, quoting "The key comes from name if present, otherwise from property". S073 was opened at 21:08:44Z, after dispatch, and is not in `corpus/SOURCES.md` at 5613071; its row first appears at 9ef758c (checked with `git show`). The same edit also adds non-checks taken from wave-1 findings: `name=`, `<base>`, and the URL the host actually serves. SCORECARD:1270-1271 says only "The tool docstring says so at `5613071`", which refers to the lane-policy rules. Nothing is counted because of it (finding 3). Smallest correction: one limits line saying the 5613071 docstring cites S073 (registered at 9ef758c) and lists non-checks added after the findings.
5. DEFECT (low, a label overstated in the safe direction) — SCORECARD:1265-1266 says the selftest, the real-input run and the lookup check "were written after the finding". The selftest was assigned in `w1-spec.json` before the finding (dispatch 21:05:22Z). Its runner mtime is 21:06:22Z, and 80 of its 85 fixture files predate 21:09:03Z ([INFERENCE], mtime). The builder's own real-input run also predates the finding: manifest 21:06:57Z, result 21:09:12Z (sandbox `ExecLinkPreviewGate/`). Only the lane receipts (real-input 21:10:59Z, selftest run 21:12:59Z, lookup check 21:12:52Z) come after it. "Does not count toward C1" is correct for all three. Smallest correction: say that the three receipts were made after the finding, not the checks themselves.
6. GAP (low, labelling) — three places cite the post-finding selftest or real-input receipts as evidence without the "not counted" label: the capability row (SCORECARD:195), the C1 bullet of the LOG round-34 entry ("Committed selftest … 29 of 29") and PROVINCE:181-182, which uses the selftest to justify held Frontier ground. The label exists only at SCORECARD:1266. SKILL:1024 is labelled ("Round-34 additions after wave 1").
7. PASS with a note — the C2 artifacts that count were written after the hollow finding. These are the S067–S070 rows, the entry body and the lesson Gate, all in 9ef758c (21:13:49Z); the hollow findings are from 21:07:36Z and 21:10:52Z. That is inherent, because the claim's artifacts are the wave's output, and the frozen counter scores them. The S067–S072 receipts are byte-identical from d08d8de to 24a1647. The note: 9ef758c changed `fetch_sources.py` (sha256 eaf37076… → a36758b5…). The S067–S072 receipts keep fetcherSha256 eaf37076…, which matches the d08d8de fetcher, not the fetcher at the tip. The C2 counter does not check this; the fetcher's added comment labels the change.
8. PASS — S073–S077 (opened 21:08:44–21:09:47Z, after `ScoutMoreSourceLeads.md` at 21:08:13Z) cannot count, because the counter's `IDS` is fixed to S067–S070. The lesson labels them (`lessons/round-34.md:40`: "counts toward no claim"), and so does the fetcher comment. README:320-324 lists S073 as mined without that label (minor).
9. DEFECT (medium, false provenance) — the entry heading at 24a1647, `link-preview-metadata.md:181`, says "not counted toward C2", and line 184 says "The C2 counter does not read them". The second statement is false. Condition (b) accepts a cite on any unfenced line after line 8, and condition (e)'s "exactly one census line" covers the whole file. Sandbox test with the frozen lane counter (sha256 ee7461b9…):
   - X1 `4f736a94`: S067 removed from body lines 9–180 and kept only in the wave-1 additions (line 192). Result: exit 0, C2 5/5, S067 b_entry_body_cites true.
   - X2 `b986183e`: also removed from line 192. Result: exit 1, C2 4/5, S067 b false.
   So the post-finding section can satisfy a counted condition. The measured after-value is safe only because SCORECARD measures C2 at 9ef758c, which predates the section. Smallest correction: reword line 184 to "measured at 9ef758c, before this section; the counter reads the whole file and these lines change no condition (c2-at-24a1647 = c2-at-9ef758c, 5/5)".

## Commands (exit codes)
- `git log --format='%H %aI %cI %s' 1e54c895..24a1647` → 0; `git diff-tree -r --stat` for each of the five commits → 0; `git diff --stat d08d8de 24a1647 -- <matrix, counters>` → 0, empty.
- `git show <rev>:.ufo/waves/round-34/sources/receipts.json` | python (accessedUtc, fetcherSha256) → 0; `ls --time-style=full-iso` on the w1, verification and retained directories and the w1 sandboxes → 0.
- `git -C <w1 ExecLinkPreviewGate clone> log`/`diff efacac6 7cc3587` → 0; `diff -u tool-w1.py tool-landed.py` → 1 (docstring hunks only); python AST compare → True.
- python check: S073–S077 cites in the entry and the S073 row in SOURCES at 5613071, 9ef758c and 24a1647 → 0 (shown in findings 4 and 8).
- `python3 -B <lane>/.ufo/waves/round-34/c2_source_census.py --root <sandbox clone> --revision <rev>`: 24a1647 → 0 (5/5); X1 → 0 (5/5); X2 → 1 (4/5).
- A first X2 attempt blanked the entry by mistake (0/5). It was discarded with a hard reset inside my sandbox only, and its output was deleted.

## Evidence (sandbox)
- `tool-w1.py`, `tool-landed.py`, `tool-w1-vs-landed.diff`
- `c2-24a16474.json` 7b737bf4…, `c2-X1.json` 13cabd53…, `c2-X2.json` f0cdbbcd…
- `cite-mutants.bundle` ac1537bc… (24a1647..b986183e)

## Not verified
- When the L1 first learned of the findings by message: I did not read transcripts, and report mtimes are only an upper bound.
- That jj's author time marks when a change was started ([INFERENCE]).
- Whether the five selftest fixtures written after 21:09:03Z were shaped by the finding.
- Whether the lesson's 24a1647 addition sits outside `## Gate`. The whole-file run at 24a1647 is 5/5 either way.
