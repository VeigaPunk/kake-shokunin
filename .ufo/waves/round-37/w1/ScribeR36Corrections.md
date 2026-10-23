# Round 36 corrections — scribe report

- Axis: freshness; auditability/provenance is the supporting surface. Operability unchanged.
- Behavior: drafted append-only correction text for routed defects 1, 5, 6; no product files or source rows changed. Sealed tree/cases and C1 counter untouched. No tests or counters run.
- Touched surfaces: sandbox draft below; this report only in the lane. No tools installed.

## Findings

1. `bf9b2089` is not a lane object. `git cat-file` fails; the retained bundle names full object `bf9b20892d241a73648d04a37feea145a03efe77` at `refs/heads/postfix`. Proposed citation preserves post-measurement / no-claim status. Existing references: `SCORECARD.md:1748`; `corpus/lessons/round-36.md:153-155`; the closure records the orphan at `corpus/lessons/round-36-verifier-spotcheck.md:23,153-154`.
2. Junk control: the Round-36 hold/no-receipt disclosure is `corpus/lessons/round-36.md:107-109` and `SCORECARD.md:1686-1688`; a junk result is nevertheless implied by `SCORECARD.md:1659-1665,1746` and `corpus/lessons/round-36.md:143`. The expected Round-36 receipt path tested absent. The current Round-37 scorecard already says untested in Round 36 and now run at `SCORECARD.md:1933-1935`; the draft points to `.ufo/waves/round-37/ctl/CtlC1Junk.md`.
3. SOURCES corrections: current cells are `corpus/SOURCES.md:96-102`. S091 anchor is §1.2/1.3, while the closure identifies the quote at §7 Design Goals item 2 (`round-36-verifier-spotcheck.md:126`); S093 rejected `teaches` lacks `flip:`; S094 says “contradicts” where “overbroad” is warranted; S088-S092 `used-by` names `scripts/source_recheck.py`. Contract: `CORPUS.md:107-108,116-118` requires lesson/knowledge-entry used-by paths and superseding rows for anchor/teaches corrections.

## Commands and observed outputs

- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin bundle list-heads .ufo/waves/round-36/retained/r36-l1-postfix-remeasure.bundle` — exit 0; `bf9b20892d241a73648d04a37feea145a03efe77 refs/heads/postfix`.
- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin cat-file -t bf9b2089` — exit 128; `fatal: Not a valid object name bf9b2089`.
- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; timeout 30s sh -c 'p=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-36/verification/control-r36-junk.json; if test -e "$p"; then printf "present: %s\n" "$p"; else printf "absent: %s\n" "$p"; fi'` — exit 0; `absent: /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-36/verification/control-r36-junk.json`.
- Search output: `S091.txt` matches `7 Design Goals` at line 1, column 2380 and the quoted compatibility-equivalence sentence at line 1, column 39004; the retained text is one 82.7KB line, so search excerpts were clipped. Closure line 126 gives the exact section.
- Initial malformed bundle invocation used `git -C <bundle-file> bundle list-heads`; exit 128, `fatal: cannot change to '.../r36-l1-postfix-remeasure.bundle': Not a directory`. Corrected with `git -C <lane> bundle list-heads <bundle>` above.
- Draft preparation: `timeout 30s mkdir -p /fast/scratch/hyaku/kake-r37w1/ScribeR36Corrections` — exit 0. Hash: `timeout 30s sha256sum /fast/scratch/hyaku/kake-r37w1/ScribeR36Corrections/r36-corrections.md` — `1a73377ec89cbf6cac48532f7218298b73864ce24a0560db9a57cb440e0a7ffe`.

## Artifacts and limits

- Draft: `/fast/scratch/hyaku/kake-r37w1/ScribeR36Corrections/r36-corrections.md` — SHA-256 `1a73377ec89cbf6cac48532f7218298b73864ce24a0560db9a57cb440e0a7ffe`.
- Scope limit: source cell proposals are advisory notes; `SOURCES.md` was not edited. No C1 case, key, or counter was accessed or executed. No behavioral test was run.
