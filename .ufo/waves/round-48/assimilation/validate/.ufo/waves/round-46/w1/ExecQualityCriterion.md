# ExecQualityCriterion — round 46

Axis: freshness (lane axes: operability, freshness).

## Result

Drafted the single receipt-identity criterion bullet in the established QUALITY.md style. It requires every filed count/verdict against a receipt to cite that receipt's path + sha256 and explicitly treats a receipt citation without sha256 as a violation. Its grounding follows round-45 lesson Mistake 15's fix: bind the filed number to the named receipt's identity and re-derive from that receipt's committed bytes.

**Named attack — receipt identity / wrong or unnamed receipt:** PASS for criterion coverage in the draft; it explicitly disallows a count/verdict detached from the cited receipt identity and receipt citations lacking sha256. This is a documentation draft, not an executed gate or behavioral attack.

## Application check and decisive output

The draft proposes a unique-label `grep -c` check with a one-decimal-count stdout shape (`0` before addition, `1` after). The requested broad expression is not selective on current QUALITY.md bytes. Exact command and output:

```sh
printf 'corpus_marker='; grep -c '^- \*\*Receipt identity for filed counts' corpus/QUALITY.md; printf 'draft_marker='; grep -c '^- \*\*Receipt identity for filed counts' .ufo/waves/round-46/drafts/quality-criterion.md; printf 'broad_corpus='; grep -c '^- .*receipt.*\(path\|sha256\)' corpus/QUALITY.md
```

```text
corpus_marker=0
draft_marker=1
broad_corpus=2
```

**Check verdict:** targeted marker shape is 0 in current QUALITY.md and 1 in the draft (consistent with 0 → 1 on integration). **FAIL** for the broad expression's claimed current 0 → 1 shape: it already returns 2 before this criterion is integrated. The two existing matches are QUALITY.md:128 (a receipt naming a runner path) and :951 (a post-measurement receipt criterion mentioning sha256). No preexisting QUALITY.md content was changed.

## Files written

- `.ufo/waves/round-46/drafts/quality-criterion.md` — proposed criterion and application check.
- `.ufo/waves/round-46/w1/ExecQualityCriterion.md` — this report.

No tools were installed or updated. No tests/build/lint/format checks were run. No blockers; L1 should use the targeted marker check or revise the broad-count expectation before treating it as an application check.
