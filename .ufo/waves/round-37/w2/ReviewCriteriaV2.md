# ReviewCriteriaV2 — round 37 wave 2 (falsify), criteria checks

Attacked, at 79d3c780: `.ufo/waves/round-37/criteria/{control_tree_check,polarity_check,bare_id_check,junk_control_receipt_check}.py`,
the receipts in `criteria/receipts/`, and the statements in QUALITY.md:900-914 and lessons/round-37.md:128,156.
Sandbox: /fast/scratch/hyaku/kake-r37w2/ReviewCriteriaV2 (clone at 79d3c780). Attack harness: `atk.py`
(sha256 d188345d943bd98d…), with output in `atk.out` (05259bb5cad17926…). Every input named below is under `atk/`. No tools were installed.

## Receipts reproduced
- Committed scripts match the hashes in the receipts: bare 8b8fe47d…, control-tree b592270e…, polarity 7ebc5d67…. The wave-1 scratch copies are identical.
- I ran `run_{bare_id,control_tree,polarity}.sh` with only `L` pointed at my clone, reading the wave-1 fixtures in `/fast/scratch/hyaku/kake-r37w1/ExecCriteriaRepairs/fixtures`. All three scripts exit 0, and each output matches its committed receipt byte for byte apart from the lane path. Control-tree exits: 0 1 1 1 1 1 1 0 0 0 0. Polarity: v1 gives exit 1 (bullets e and f fail), v2 gives 0. Bare id: red 1, green 0, sweep 0 (31 PASS lines).
- **Overstated (reproducibility):** none of the fixtures is committed (`git ls-files` returns nothing for them). When I copied the fixtures to my sandbox and reran, two control-tree steps changed: the "RED tree walk" fails for a different reason, and the "GREEN key-free tree + disk walk" turns into a FAIL with exit 1 ("records no listing of the control tree"). The reports hard-code absolute w1 paths. So the `--tree` receipts only hold while that scratch directory survives.
- junk check: exit 1 at 1a16b8e3, exit 0 at 4b089da6, 528a6d02 and 79d3c780, and exit 1 at 202d625a. This matches lessons/round-37.md:156. `criteria/receipts/` holds no receipt file for this check.
- I re-ran the r36 junk receipt as `.ufo/waves/round-36/sealed_count.py --tool-file <retained CtlC1Junk-source_recheck_junk.py> --key-revision fd1fb723`. It exits 1 with passed 0/28, counterSha 88ec5914…, toolSha 4c23062f…. The only difference from `verification/control-r36-junk.json` is `toolFile`. **Holds.**

## control_tree_check.py v2 — QUALITY (f) "reject any key/sealed-case path anywhere in the tree": **overstated**
False passes (each exits 0, pattern `.ufo/waves/round-37/sealed/`):
- FP1, symlink: `atk/ct/symtree/k` points to the clone's `.ufo/waves/round-37/sealed`. It passes even with `--tree`. `_ls_name` drops the `-> target` part (:150-151), and `os.walk` does not follow the link (:227).
- FP2, nested clone: the root listing shows `lane/`, and `lane/.ufo/waves/round-37/sealed/cases.json` exists. `_above_key` only matches a listed directory that lies on the pattern path itself (:111-127), so the same miss happens one level down. A real instance has the same shape: `ctl/CtlC1Junk.md` passes the receipt, and its listing shows `lane`, a clone at 202d625a holding 8 `round-36/sealed/` files. That was an authorized, already-revealed key, so it is not a leak.
- FP3, renamed key: the key copied as `c1-cases.json` (the real round-35 key name) and `key.json`. Passes even with `--tree`, because `KEY_NAME_RE` is `^cases.*\.json$` (:51).
- FP4, unparsed listing formats: a clean `ls -la` plus the key dir shown by `ls -lai` (an inode number leads, so `LS_ENTRY_RE` at :39 fails to match), `ls -lo` (fewer than 9 fields, dropped at :147), and `find` output. All four pass.

False fails (each exits 1):
- FF1: a complete `ls -laR` of a key-free tree containing `.ufo/waves/round-37/w1/`, run with `--tree`. Its `.ufo`, `waves` and `round-37` directories are each flagged "cannot certify the subtree", although the recursive listing does certify it (`_above_key` never checks whether the subtree was listed).
- FF2: a public fixture table `fixtures/cases.json` is flagged as key-named. A real instance: the RED receipt's first FAIL line flags `.ufo/waves/round-22/cases.json`, which is round-22's public fixture table (c0fd6d5), not a key.
- FF3: a key-free tree listed with plain `ls -la` from inside it (no path argument), run with `--tree`. Result: "records no listing of the control tree" (:241-256 requires an absolute root).

Verdict: v2 does catch the round-36 false pass, as the RED receipts show. But "no key anywhere in the tree" is not established: links, nesting, renames and other listing formats all get past it.

## polarity_check.py — QUALITY (e): per-case polarity **holds** on the r36 keys; "label independence" and the docstring's "kills every shortcut" claim are **wrong**
- FP1: the receipt's own GREEN fixture `key-both-polarities.json` is self-inconsistent. Run on its manifest, `scripts/source_recheck.py` emits `quote_missing` on q1, a check the key expects to hold (q1's body is "x" and its quote is "present quote"). Exit 1, 3 findings. The polarity check passes it because it never decodes a body (:84-98).
- FP2 (`atk/pol/fp-filename.json`): the hold uses body `present.html` and the finding uses body `missing.html`. A tool that emits `quote_missing` whenever the body file name contains "missing" gets every check right, and the check reports PASS with exit 0. QUALITY (e) explicitly requires rejecting keys where a file-name label can substitute for reading the body.
- FP3 (`fp-absent-body.json`): the only hold names a body file that is not in `files`. The contract would give `check_invalid` there, yet the check reports PASS with exit 0.
- FF1 (`ff-utf16.json`): a body-decided `quote_missing` under `charset=utf-16`, which the contract maps to utf-16-le (`scripts/source_recheck.py:225`). The check errors out with exit 2. Seven contract labels are missing from `SUPPORTED_CHARSETS` (:48-54): csunicode, iso-10646-ucs-2, ucs-2, unicode, unicodefeff, unicodefffe, utf-16.
- FF2 and FF3: in the contract a byte order mark overrides the label (`source_recheck.py:257-261`), so `charset_unsupported`, and the holds under an unsupported label, are decided by the body. I checked this by running the contract tool on `ff-bom`: q1 holds, q2 gets `quote_missing`, q3 gets `charset_unsupported`. On the same key the polarity check exits 2, and on `ff-bom-charset` it exits 1 with "0 holds". Listing `charset_unsupported` in `METADATA_REASONS` (:37-45) is therefore wrong in general.
- Scope check: neither r36 key has an unsupported-label check whose body starts with a byte order mark (v1: 93 checks with a charset, v2: 90; 0 such cases in each). So the v1 RED and v2 GREEN results are unaffected. **Holds** for those receipts.

## bare_id_check.py — QUALITY (g): **holds** for the receipt's red/green; the check is a word-count heuristic, so the rule is overstated
- FP1: `- S098 lorem ipsum dolor` and `- S099 and the of` both pass with exit 0, since 3 tokens of 2+ letters count as claim text (:41, :48-60).
- FP2: a table row `| S098 | |` is credited by a sibling row's claim, because the whole table is one block. Exit 0.
- FF1: `- S011` with the claim in a nested sub-bullet fails with exit 1, because the sub-bullet starts a new block (:36).
- FF2: `- S011 §2.2.2: \`Allow: /a\` > \`Disallow: /\`` fails with exit 1, because inline code and section references are stripped before words are counted.
- The new entry `robots-txt-rules.md` passes with exit 0 (3 S-ids).

## junk_control_receipt_check.py — lessons:156 receipts **hold**; as a gate it is **overstated**
Each test is a throwaway commit in a sandbox-only clone, built on 79d3c780 and checked with `--revision HEAD`:
- FP, j1 (d95030f): replaced the receipt with a fabricated 5-key JSON (`toolFile` "made-up/source_recheck_junk.py", no counterSha, no perCase, no tool). PASS, exit 0. The check never ties the receipt to the round-36 counter hash, the retained tool hash or a per-case list (:61-70).
- FF, j2 (071fc5b): an honest-shaped receipt reporting 1/28 with met=false. That still supports "no control reached 25", yet the check fails ("does not show 0/28"), exit 1.
- FF, j3 (81658be): the correction sentence reflowed across a line break, which renders identically. FAIL "no later correction", exit 1, because the check is an exact byte match (:44).

## Residual risk / gaps
- I did not run the `--tree` mode against real control sandboxes, which live in the L1-private `/fast/scratch/hyaku/kake-r37/`, out of bounds for me. `toolFile` in control-r36-junk.json also points there, so I checked it by hash against the retained copy only.
- No lsp server was used. These are standalone scripts, and every finding comes from executed runs.
- Processes: none are left running. My clones j1, j2 and j3 stay in the sandbox only.
