DEFECT: registry census numbers hold at both round-43 revisions, but round-43 freeze bookkeeping has four conformance defects (unreceipted 128→130 count, no exit code in census receipts, S129/S130 quote locators wrong, corpus index omits the round-43 knowledge entry).

Scope: kake round 43 wave 1, ExecCensus seat (freshness axis); freeze tip b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee; lane /home/vgpnk/Projects/shokunin/kake-shokunin.
Revisions censused: base 61046fcffa23898cd93b7a5a0af4906dac9926c9; freeze b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee; wave-1 tip 7c070797eb5b6661983995705b546a0b07a9ea41 (SOURCES.md byte-identical at freeze and tip, sha256 9ec92ad6ff29ae4890f7a40955ccf78b31f9724b6c41af0eeefe56693cc7cf2f).

## Census results (exit codes + histograms)

- Maintained script: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` -> exit 0; stdout = 12 W04 duplicate-url warnings + `kake\tok\t<path>`. Identical to committed receipt `.ufo/waves/round-43/verification/freeze/census-after-r43.txt` (diff: no changes).
- Same script, census mode, kake lane -> exit 0: rows 130; tier.A 108, tier.B 6, tier.C 16; status.mined 101, status.queued 8, status.rejected 21; FLEET invalid/missing 0.
- Manual CORPUS.md census over `git show b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee:corpus/SOURCES.md`: rows 130; malformed (NF!=13) 0; tier A=108 B=6 C=16; status mined=101 queued=8 rejected=21; duplicate ids none; enum violations none; mined used-by paths all exist. Same numbers over `git show 7c070797eb5b6661983995705b546a0b07a9ea41:corpus/SOURCES.md`.
- Checker `registry_count_check.py --claims verification/freeze/registry-count-r42-claims.json` -> exit 1 (7 mismatches); with `--claims ...r43-claims.json` -> exit 0; outputs byte-identical to committed `registry-count-r4{2,3}-check.txt` (re-run today).

## Checked statements

1. "Registry rows 128 → 130 at the freeze commit" (SCORECARD.md:3275) and "registry 128 → 130 rows at this lesson's commit" (corpus/lessons/round-43.md:20): HOLDS numerically (61046fc=128 rows, b49cba9=130 rows; mined 99→101, queued 8, rejected 21). OVERSTATED as evidence: no committed claims file/receipt covers that pair — `registry-count-r43-claims.json` measures 1ef7a0e9→5949e66ffe (119→128). I verified the 128→130 pair with the checker + a claims file I built (exit 0) and a wrong value 131 (exit 1). Under the lane's own rule 1 (corpus/knowledge/claim-count-derivation.md:22-24), this filed count lacks its counting command and measured-revision receipt.
2. "Census exit 0 before (`../round-42/census-after.txt`, carried) and after (`verification/freeze/census-after-r43.txt`)" (SCORECARD.md:3273-3274): HOLDS on re-run (validate and census exit 0 today), but the receipts contain stdout only — no exit-code line — and both files are byte-identical to each other (diff: IDENTICAL) and carry no row counts. The "exit 0" claim is not evidenced by the committed receipts.
3. "Census exit 0 before (`census-before.txt`) and after (`census-after.txt`)" (round-42 section, SCORECARD.md:3171-3172): r42 `census-before.txt` ends with an `exit=0` line; r42/r43 `census-after*.txt` do not. Same caveat.
4. Registry-arithmetic correction (SCORECARD.md:3264-3270): HOLDS — 119→128 rows, mined +7, queued +0, rejected +2 re-derive from committed bytes; checker red/green behavior reproduced.

## Defects found

- D1 (unreceipted count): the round-43 "128 → 130" count (SCORECARD.md:3275; corpus/lessons/round-43.md:20) has no committed claims file/receipt for the 61046fc→b49cba9 pair; the committed r43 receipt covers only 119→128. Number is true; evidence missing under the lane's own rule 1.
- D2 (exit code not recorded): the freeze census receipts do not contain an exit field; "census exit 0 before/after" is asserted in SCORECARD.md:3274 but not evidenced by the cited files.
- D3 (S129/S130 quote locators): corpus/lessons/round-43.md:16-17 and corpus/SOURCES.md:137-138 anchor the quotes to paragraph 2 ("## Verdict" paragraphs two to four); the quoted sentences are in paragraph 1 of the cited sources: tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md:9-11 ("The do-nothing shortcut never reaches `predicate_pass=true`.") and kama-shokunin/corpus/knowledge/self-assessment-at-writing.md:7 ("A mismatch therefore records a calibration error present when the statement was written."). Also the S129 quote is not a contiguous exact substring (line break + backticks in source), requiring whitespace normalization with no erratum note. (Sibling seat CriticFrontier reported the same; independently confirmed here with line numbers.)
- D4 (corpus index gap): corpus/README.md has no round-40..43 section and does not mention the round-43 knowledge entry `corpus/knowledge/claim-count-derivation.md` (0 occurrences; all other 33 knowledge files are named) nor S120–S130. README last updated at round-39 (commit b56433b). The registry rows S129/S130 used-by targets (corpus/lessons/round-43.md, corpus/knowledge/claim-count-derivation.md, SCORECARD.md) all exist.

## Risks / non-defects

- The checker's row predicate (len(cells)==13 AND S+digits) is not equivalent to the CORPUS.md manual rows command (regex S[0-9]{3,}; counts malformed rows too). Demonstrated divergence on a synthetic S12 row: manual rows 130 vs maintained census rows 131. No divergence at the censused revisions (all ids 3-digit, 0 malformed); latent risk only.
- S129/S130 `recheck=on-use` is a symbolic cadence accepted by the maintained parser; never overdue (overdue mode exit 0).
- SOURCES.md search log's last "bounded question" entry is Round 35; rounds 36-43 keep Gate records in lessons rather than SOURCES search-log prose (carried pattern, not new in round 43).

Sandbox outputs: /fast/scratch/hyaku/kake-r43/ExecCensus/ (validate/census/overdue/shared receipts, per-revision SOURCES.md snapshots, manual-census outputs, checker re-runs, mutant probes).
Tools: none installed (host python3 3.14.8, git, node used).
