# ReviewControlReceipts — control receipts and bundles vs SCORECARD (round 35)

Scope: committed receipts `.ufo/waves/round-35/verification/control-*.json(+.exit)`, bundles
`.ufo/waves/round-35/retained/r35-control-*.bundle`, round-34 bundles resolving `dcef39b5`/`0cce15f0`,
counter hash at `81d9fd74` and `318561ef`, and commit content vs the SCORECARD control table
(SCORECARD.md:1430-1455). Sandbox clone at `318561ef`; no lane state touched.

## Result table (all ten controls)

| Control | Receipt names | Bundle ok | Content matches description | Receipt fields consistent |
|---|---|---|---|---|
| C1 base (do nothing) | `16a6b8b8` = table | n/a (lane history) | yes: tool sha `cccc3a17` identical at base and declaration — genuinely unchanged | yes: passed 14/24, met false, perCase 14 true, target 22, exit 1 |
| C1 at declaration | `81d9fd74` = table | n/a (lane history) | yes (same tool bytes) | yes: 14/24, exit 1 |
| C1 round-34 lookup | `dcef39b5` = table | yes: r34-c1-lookup-dcef39b5.bundle verify OK, contains `refs/heads/lookup-c1` = dcef39b5 | yes: "sandbox: lookup C1", different tool bytes (`a2e274c0`) | yes: passed 7/24, exit 1 |
| C1 constant clean | `5f767534` = table | yes: r35-control-c1-constant.bundle verify OK, ref = 5f767534, prereq 81d9fd74 | yes: whole tool is `print({"findings":[],"pagesChecked":1,"verdict":"clean"}); sys.exit(0)`; only that file changed (2+/301-) | yes: passed 7/24, exit 1, toolSha `d0f1a53e` matches commit |
| C2 base, no entry | `16a6b8b8` = table | n/a | yes: `corpus/knowledge/security-txt-publishing.md` absent at 16a6b8b8 | yes: entrySha null, all conditions false, 0/12 |
| C2 at declaration | `81d9fd74` = table | n/a | yes: entry absent; pinnedTextsIntact true (texts landed with declaration) | yes: 0/12 |
| C2 hollow round-34 | `0cce15f0` = table | yes: r34-c2-hollow-0cce15f0.bundle verify OK, ref = 0cce15f0 | yes: entry absent at 0cce15f0 ("no entry at the round-35 path") | yes: 0/12, copiedShare 1.0 |
| C2 junk | `04848219` = table | yes: r35-control-c2-junk.bundle verify OK, ref = 04848219, prereq 81d9fd74 | yes: entry = `# junk` + 7×`filler` + `S078 S079 S080 S081` (13 words); SOURCES adds S078-S081 rows all marked `mined`, path = entry — "junk rows S078–S081 marked mined, filler, ids" | yes: entry/size/copied/cites true, probes false 0/12, entrySha `7491387a` matches |
| C2 keyword | `e5263d41` = table | yes: r35-control-c2-keyword.bundle verify OK, ref = e5263d41, prereq 81d9fd74 | yes: RFC 9116 TOC headings + field names (Contact, Encryption, Expires, Canonical, Preferred-Languages, …) + format tokens; same 4 junk rows (SOURCES.md diff vs junk = empty) | yes: 3/12 (P01,P03,P07), words 78, entrySha `c388667a` matches |
| C2 transcript | `ae9fb361` = table | yes: r35-control-c2-transcript.bundle verify OK, ref = ae9fb361, prereq 81d9fd74 | yes: body is one line that is a byte-exact contiguous substring of retained `.ufo/waves/round-35/sources/S078.txt` (offsets 9022–18300), starts "2.5. Field Definitions", contains "3.1." and not "3.2." — verbatim RFC 9116 §2.5–3.1; same 4 junk rows | yes: 8/12, copiedShare 0.9951 (copied false), words 1303, entrySha `750c8e6e` matches |

## Cross-checks

- Counter: `git show <rev>:.ufo/waves/round-35/sealed_count.py | sha256sum` = `c4d58dae…49ef` at BOTH
  `81d9fd74` and `318561ef`; `git diff --stat 81d9fd74 318561ef` shows the counter unchanged (only
  receipts, bundles, SCORECARD added, 25 files, 955 insertions). All ten receipts name that same hash.
- Chain: `318561e(parent=81d9fd7) <- 81d9fd7(parent=16a6b8b)`; all four r35 control commits have parent
  `81d9fd74` = the declared bundle prerequisite.
- Receipt identity: all 20 receipt/exit files and 4 bundles in the lane working tree are byte-identical
  (sha256) to the copies committed at `318561ef`.
- Exit files: all ten committed `.exit` = `exit=1` (fails, matching `met:false`).
- Tool hashes: base/declaration `cccc3a17`, lookup `a2e274c0`, constant `d0f1a53e` — each equals the
  receipt `toolSha256` and the sha256 of `scripts/link_preview_audit.py` at the named revision.
- C1 perCase: committed receipts contain exactly 14/14/7/7 `"passed": true`, equal to `passed`.
- C2 probes: keyword P01,P03,P07 true (=3); transcript P01,P02,P03,P06,P07,P08,P09,P11 true (=8); junk
  and no-entry controls 0. `goodCites` for the three entry controls = S078-S081, matching the counter's
  rule (counter lines 244-249: exactly-once row, `mined`, `2026-10-22`, entry path in cell 11) and the
  SCORECARD note "Junk rows do satisfy the `cites` condition" (SCORECARD.md:1453).
- copiedShare semantics (counter lines 218-223): shingle overlap of entry words vs retained `.txt`
  texts; a 1303-word entry that is ~99.5% verbatim RFC is consistent with 0.9951.

## Advisory notes (non-blocking)

1. SCORECARD.md:1451 says the transcript is "(1296 words)"; the receipt `words` is 1303. Arithmetic
   reconciles: body 1296 + 7-word title/sources header = 1303 (`python` split). Descriptor only.
2. `pinnedTextsIntact` is false in the two pre-declaration receipts (base, hollow) and true from
   `81d9fd74` on — pinned texts land with the declaration commit; the base `copied` condition therefore
   fails on pinning, not copying. Internally consistent, worth knowing when reading the receipts.

## Commands run (all exit 0 unless noted)

- `git clone -q <lane> <sandbox>/clone && git checkout -q 318561ef` — CLONE_OK.
- `git bundle verify <bundle>` ×6 — "is okay" with contained/required refs as tabled.
- `git fetch <bundle> 'refs/*:refs/bndl/<name>/*'` ×6 — fetchExit=0.
- `git cat-file -e <sha>^{commit}` ×8 — all OK (incl. dcef39b5, 0cce15f0 from r34 bundles).
- sha256 via `git show <rev>:<path> | sha256sum` for counter ×2, tool ×4, entry ×3.
- Content reads: constant tool, three entries, SOURCES.md diffs, transcript-vs-S078 substring check,
  perCase/probe true-counts, exit files, committed-vs-tree identity (24/24 SAME).

## Not verified

- The sealed counter was not re-executed (sealed keys are unreadable to this seat by rule); receipt
  numbers are verified for internal consistency and cross-hashes, not re-measured.
- copiedShare 0.9951 not recomputed shingle-by-shingle; only plausibility-checked against the counter
  definition and entry composition.

No tool installs (none needed). Findings are advisory input for the L1 and the non-author closure.
