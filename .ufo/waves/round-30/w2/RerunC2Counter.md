# Wave 2 — RerunC2Counter — attack C2's measured value at 451e98f

Seat: KakeR30.RerunC2Counter (leaf, falsify). Axes: freshness (judged), operability.
Sandbox: /fast/scratch/hyaku/kake-r30/w2/RerunC2Counter/ (clone + tmp TMPDIR).
No installs (none needed). No network was used; all work is on committed bytes.
No writes inside the lane except this file.

## What I attacked

C2 4/4 at 451e98fc8415edf10f41b2aad656318e7edc84ca (counter .ufo/waves/round-30/
c2_quote_truth.py, receipt verification/c2-after-451e98f.json), plus the four
declared closure checks in SCORECARD.md "Round 30 — declared claims" /
"C2 closure checks" (SCORECARD.md:752-757).

## Commands run and observed outputs (all in sandbox/clone, cwd=clone)

1. git clone -q <lane> clone; git rev-parse HEAD
   -> 451e98fc8415edf10f41b2aad656318e7edc84ca (lane master HEAD == measured rev). exit 0.
2. TMPDIR=<sandbox>/tmp python3 -B .ufo/waves/round-30/c2_quote_truth.py \
   --root . --revision 451e98fc8415edf10f41b2aad656318e7edc84ca
   -> stderr "C2 4/4 at 451e98fc…", exit 0; all ids pass a_row, b_entry_body_cites,
   c_gate_quote, d_quote_in_retained_text; controlBroken false.
   stdout saved: <sandbox>/c2_rerun_stdout.json.
3. diff <sandbox>/c2_rerun_stdout.json <lane>/.ufo/waves/round-30/verification/c2-after-451e98f.json
   -> exit 0 (byte-identical to the landed receipt).
4. python3 -B … c2_quote_truth.py --root . --revision 035668132250b75b38d399e86e540b0a0371efbc
   -> stderr "C2 0/4 at 0356681…", exit 1; stdout byte-identical (diff exit 0) to the
   TRACKED .ufo/waves/round-30/verification/c2-before-0356681.json. Before-claim holds.
5. git show 451e98f:.ufo/waves/round-30/c2_quote_truth.py | sha256sum
   -> a2cd3164f67e221f0d38609afd50be61260902f963f05f96bd1b223451975e7a (matches
   SCORECARD a2cd3164…5e7a and receipt counterSha256; working-tree file same hash).
6. git diff --quiet 4580c78 451e98f -- .ufo/waves/round-30/sources/S049.txt
   …S052.txt receipts.json .ufo/waves/round-30/fetch_sources.py -> exit 0.
7. git diff --quiet 4580c78 451e98f -- .ufo/waves/round-30/sources/ .ufo/waves/round-30/fetch_sources.py
   -> exit 1. diff --stat: only ADDITIONS under sources/screened/
   (C1.html.gz/.txt, C2…, C3…, screened/receipts.json; 7 files). All six C2 files
   already existed at 4580c78 (git ls-tree 4580c78 confirms).
8. git show 451e98f:.ufo/waves/round-30/fetch_sources.py | sha256sum
   -> b9431a5f349c7b857e2139fd148b8f75a2ddb8a4d94a3ea7013709a28a9190b4
   == fetcherSha256 in all four receipts (fetcher identity ties out).
9. Registry vs receipt URLs (python over git-show bytes at 451e98f):
   S049-S052: URL token inside each SOURCES.md source cell equals the receipt url
   exactly; finalUrl == url; status 200; one GET each at 11:49:44Z (S049,S050) and
   11:49:45Z (S051,S052). Cells are "Render Docs: <title> — <URL>", so the counter's
   own test is substring-only; exact URL-token equality verified by me.
10. Entry citations: first body citation of S049/S050/S051/S052 at entry lines
   19/36/49/19 (entry has 113 lines), i.e. all below the counter's 8-line skip.
    Quote contexts in retained text are on-topic body sentences, not navigation.

## Findings

F1 (medium, closure check as written fails): SCORECARD.md:755-757 declares
`git diff --quiet 4580c78 <commit> -- .ufo/waves/round-30/sources/ .ufo/waves/round-30/fetch_sources.py`
exits 0. At the measured revision it exits 1, because 451e98f adds
sources/screened/* inside the same directory. The six C2 files are unchanged
(check 6, exit 0), so the substantive intent holds; the declared command is
unsatisfiable at the landed state and should be scoped to the six files.

F2 (medium-high, provenance): verification/c2-after-451e98f.json is not committed
anywhere. Absent from `git ls-files` in the clone; `git log --oneline --all -- <path>`
empty in clone AND lane; `git check-ignore -v` exit 1 (not ignored); lane
`git ls-files --others` lists it as untracked. The round context lists it under
"Landed this round"; every C1 receipt IS tracked, this one is not. My rerun
reproduces it byte-for-byte (check 3), so the measurement is sound, but the
receipt's "landed" status is false — commit it or amend the claim.

F3 (minor, closure sentence overbroad): "Each registry row's URL must equal its
receipt URL exactly" holds only for S049-S052. sources/receipts.json has exactly
keys S049-S052; S053-S055 receipts live under sources/screened/receipts.json with
ids C1-C3 (URLs match the S053-S055 rows exactly); S056's source cell is a sibling
-lane file pointer, not a fetched URL. If "each registry row" means all six new
rows S049-S056, four rows have no receipt in sources/receipts.json.

## Verdict

C2 measured value: HOLDS. 4/4 at 451e98f reproduces byte-identically in a fresh
clone; 0/4 at base reproduces; counter hash ties; retained sources unchanged
since declaration; receipts self-consistent (one GET each, finalUrl == url,
fetcher hash ties); quotes are real body text below the metadata skip.
Declared closure checks as written: PARTIAL FAIL — F1 (declared diff command
exits 1), F2 (after-receipt untracked while claimed landed), F3 (sentence
unsatisfiable for S053-S056 as worded).

Residual risk / not verified: no live re-fetch (bound: non-reopen seat, no
network), so the receipts' claimed 2026-10-22T11:49Z GETs are trusted from
committed bytes; html.gz bodies were not decompressed/rehashed against bodySha256
(out of counter scope, cheap for a reopener to add); I did not judge the entry's
prose quality, only quote truth and citation placement.

Sandbox artifacts: /fast/scratch/hyaku/kake-r30/w2/RerunC2Counter/
{c2_rerun_stdout.json, c2_base_stdout.json, c2_rerun_stderr.txt, c2_base_stderr.txt, clone/}.
