# PeripheralScope — scout, axis freshness (Kake r27 w1)

Read-only seat. No corpus/SKILL/Git edits, no gates, no network, no tool installs.
Frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`; declarations
`be375d90afc6fc7aca369ab3cf5247bf460aeed2`; worktree = declarations + untracked r27 artifacts.
## 0. Verdict
1. **Literal r26 clause does not require citations outside `corpus/knowledge/`.** The frozen
   after-clause is `knowledge-entry claims citing the rows rechecked`
   (`.ufo/waves/round-26/contract.json:9`); the shipped ledger has 41 pairs, all nine files
   under `corpus/knowledge/`.
2. **The broader r26 adjudication sentence covers corpus lessons/README/QUALITY textually.**
   `corpus/QUALITY.md:231-233`: "A recheck covers every corpus statement that cites a
   rechecked row, not only files listed in `usedBy`." That reaches 135 expanded
   corpus-statement pairs (122 lessons + 10 README + 3 QUALITY); it does not reach root
   `SKILL/LOG/SCORECARD` or `considerthese/`/`scripts/`.
3. **No gate or ledger was built for either outside scope.** `measure.py` checks only ledger
   pairs and tags; `corpus/lessons/round-26.md:118` records `completeness of the citing set is
   still not machine-checked (open)`. r27 C1 explicitly narrows to `All corpus/knowledge files
   at measured revision` (`.ufo/waves/round-27/contract.json:12`).
4. **Outside census:** 219 expanded `(row,file)` pairs across 22 files at declarations
   (186 literal; 213/184 at frozen base). None are in the r26 ledger or r27's 57-pair C1
   denominator. They are named excluded debt, not silently covered.
5. **The 16 missing knowledge pairs are 12 substantive citations + 4 procedural S008 retry
   mentions.** The frozen C2 oracle counts all 16; the pair count is not 16 new source claims.
6. **Uncorrected r26 success framing survives in `corpus/README.md:167-180`.** `SCORECARD.md`
   and `LOG.md` carry r27 appends naming the non-author rejection; `SKILL.md`/`PROVINCE.md`
   carry no rejection/status note but also make no admission claim.
## 1. Target tails read (bounded)

**SKILL.md 576-592** (sha256 `63fc812d…`): procedure 578-583, registry row 587, falsify update
589-592. Row verdict: `0 all 32 rows decided and every adjudicated STALE statement corrected`;
capability: `the counter also verifies every population fetch of a row`. No admission claim,
no rejection note; exit-0 wording can be read as closure, and the grouped S001–S006 gap is not
named.

**corpus/README.md 167-180** (sha256 `a4ac3009…`): `All 32 prior external SOURCES rows were
re-fetched 2026-10-21 and hold at their anchors` (169-170), then `Falsify-wave final` and
`Final ledger: 313 row-statement units` (175-178). Row-level HOLD is genuine per the verifier;
the text omits `admitted false; rejected-honest-stop` and the grouped missing pairs, and ends
the file with no r27 append. **This is the one current uncorrected author-side success framing.**

**corpus/QUALITY.md 207-233** (sha256 `fd5065a1…`): adjudication rules (row-specific quote,
STALE-at-own-scope, single entity decode, falsify addendum). Line 231 is the widest scope
sentence: `A recheck covers every corpus statement that cites a rechecked row, not only files
listed in usedBy`. No admission claim; this is the only r26 text that can be read as requiring
lesson/README citations, and it was not implemented by the 41-pair ledger or `measure.py`.

**PROVINCE.md** (78 lines, sha256 `f71df98e…`): ends at `## Round-25 accessibility preparation
boundary` (70-78), last sentence `Round24's policy-stop disposition remains separate open
debt.` No r26/r27 section: omission, not a false claim. Its only S0NN is out-of-population
S035 at line 74.
## 2. Citations outside the knowledge-file denominator

Method: same token/range regex as `count_c1.py` (`\bS\d{3,}\b`; hyphen/en/em dash, `..`, `to`,
`through`; descending or >200 spans rejected), over every `git ls-tree -r <rev>` path except
`corpus/knowledge/`, `.ufo/`, `.git/`; rows intersected with the frozen 32-row population;
ranges expanded, matching C1.

| Surface | Files | be375d9 | base 83528f7 |
|---|---:|---:|---:|
| `corpus/lessons/*.md` | 13 | 122 | 122 |
| `corpus/SOURCES.md` (row ids/cells) | 1 | 32 | 32 |
| `corpus/README.md` | 1 | 10 | 10 |
| `corpus/QUALITY.md` | 1 | 3 | 3 |
| `SKILL.md` | 1 | 14 | 14 |
| `SCORECARD.md` | 1 | 11 | 5 |
| `LOG.md` | 1 | 19 | 19 |
| `considerthese/*.md` | 2 | 7 | 7 |
| `scripts/corpus-contract.mjs` | 1 | 1 | 1 |
| **Total** | **22** | **219** | **213** |

Literal totals: 186 at declarations, 184 at base. The declaration delta is the r27
`SCORECARD.md:533` range `S001–S006` (6 expanded, 2 literal endpoints). Largest lesson
contributors: round-26 32, round-20 17, round-21 17, verifier-spotcheck 14, round-22 10,
round-22-verifier 10; the verifier's own correction document is itself outside the denominator
(14 pairs).

Knowledge denominator for contrast: **9 files, 57 expanded pairs** (47 literal); r26 ledger 41;
16 missing = S001, S002, S003×2, S004×2, S005×2, S006×2, S008×4, S022, S023 — exactly
`c2-oracle.json` `expectedPairs`.
## 3. Does the full r26 "knowledge-entry" clause require the outside citations?

- **Literal frozen clause: no.** It names knowledge-entry claims only. The r26 ledger
  (`statements.json`) is 41 pairs over nine `corpus/knowledge/` files. The canonical `used-by`
  wording quoted in `w2/UncoveredLessonCites.md` distinguishes "knowledge entries or lessons",
  so lessons are a different class. The non-author verifier read it the same way: it faulted
  only the grouped S001–S006 knowledge pair and stated `The frozen C1 is not merely the receipt
  count.` followed by the clause quote.
- **QUALITY.md:231 broader sentence: yes for corpus statements.** If operative, 135 expanded
  pairs in `corpus/lessons/`, `corpus/README.md`, `corpus/QUALITY.md` cite rechecked rows and
  are in textual scope. r26 did not adjudicate them as pairs:
  `UncoveredLessonCites.md` re-verified the four S022–S025 lesson quotes and concluded
  `no lesson statement is false and no lesson may be edited`; no lesson pair entered
  `statements.json`.
- **Root/narrative files: no under either text.** `SKILL.md`, `LOG.md`, `SCORECARD.md`,
  `considerthese/`, `scripts/` are neither knowledge entries nor `corpus/` statements.
- **r27 resolves the ambiguity toward knowledge-only.** C1's denominator is `All corpus/knowledge
  files at measured revision`; `discovered-pairs.json` can add forms, not the 219 existing
  outside pairs. r27's "all frozen/discovered pairs" is therefore a knowledge-file claim;
  calling it the corpus-wide full citing set without naming the 219 would be silent rounding.

Both r26 critics already located the ledger's narrowness inside knowledge:
`w2/CounterCritic.md` — `The citing set is wider than the ledger.`; `w1/ClaimCritic.md` —
`The knowledge clause is unmeasured, and pair coverage is narrower than the citing set.`
## 4. Excluded surfaces named (not invisibly dropped)

- **File-scope exclusions from C1:** the 22 files / 219 pairs in §2.
- **Population exclusions, outside knowledge:** S014 (5 pairs: SOURCES, round-20, round-21,
  round-26, verifier), S019 (27 pairs across 27 files incl. LOG/SKILL/SCORECARD/README/QUALITY),
  S035 (11 pairs incl. PROVINCE, handoff, r25/r26 lessons), S036 (1, hypothetical superseding
  row in round-26.md), S999 (1, fixture token in `scripts/corpus-contract.mjs`).
- **Population exclusions, inside knowledge:** S014 in `freshness-sweep.md`; S019 in 16
  knowledge files; S035 in `accessibility-review-packet.md`. Excluded because the population is
  S001–S034 minus own-work S014/S019, with S035 opened r25 — a population rule, not file scope.
- **Evidence machinery:** `.ufo/waves/round-26/**` receipts/ledgers and r27 artifacts contain
  S0NN ids universally; they are evidence records, not corpus citing claims, and are not counted.
- **4 of the 16 C1 missing pairs are procedural S008 mentions.** In `crawl-scope-per-host.md`,
  `ghp-custom-domain.md`, `ghp-etag-anatomy.md`, `static-canonical-preflight.md`, the only S008
  literal is the appended r26 paragraph's `S008 via manifest-retry.json`; the substantive S008
  citation is in `ghp-served-set.md` and is already ledgered. The frozen contract deliberately
  includes "historical metadata/r26 EOF prose", so these are valid obligations, not substantive
  S008 claims. [INFERENCE: the r26 verifier's 43-literal/41-ledger count excluded exactly these
  four, leaving S001/S006 as its only unlisted literal endpoints.]
## 5. Current r26 status claims and correction state

Authoritative record: `corpus/lessons/round-26-verifier-spotcheck.md:9` — `Status ok (real
report); admitted false; rejected-honest-stop.` Same file records the grouped S001–S006 gap and
accepts the receipt result `0/32 → 32/32 HOLD`.

| File:line | Current text | State |
|---|---|---|
| `SCORECARD.md:516` | `C1 freshness verified author-side` | **Corrected by r27 append** `:533`: `r26 author-side verify claim above is superseded by non-author rejected-honest-stop` … `313 units are not retroactively completed.` |
| `LOG.md:1040-1066` | `32/32 HOLD exit 0`, ledger 313/7/4 | **Corrected by r27 append** `:1068`: `r26 C1 was rejected, not completed by the green32 counter.` |
| `corpus/README.md:169` | `All 32 prior external SOURCES rows were re-fetched 2026-10-21 and hold at their anchors` | **Uncorrected in this file.** Ends at 180 with no rejection note and no r27 append. Row HOLD is true; the omission is the rejection and grouped gap. |
| `SKILL.md:576-592` | Counter procedure/registry/falsify update | No admission claim; no rejection note. Exit-0 wording can be read as closure. |
| `PROVINCE.md:70-78` | Last section Round-25 | No r26/r27 status. Omission, not false claim. |
| `corpus/QUALITY.md:207-233` | Adjudication rules | No admission claim. |
| `corpus/lessons/round-26.md` | `discernment unchanged pending the outside spot-check (all wave seats are author-side)` | Honest pending; no admission claim; later append does not claim admission. |

No current file literally claims r26 was *admitted*. The only "verified author-side" string is
`SCORECARD.md:516`, and it has an r27 append. The uncorrected freshness defect is the
`corpus/README.md` r26 section. Correcting it must be an **r27 append**, not an edit to the r26
block: r27's record says r26 report/contract/ledger/receipts/waves remain unchanged and
`Correction belongs to r27`.
## 6. Uncertainties / not done

- `QUALITY.md:231`'s "corpus statement" is not formally defined. I read it as `corpus/**`
  statements (lessons/README/QUALITY in; registry cells out as row identity/metadata). A
  knowledge-only reading collapses the 135 in-principle pairs to the 57 already counted.
- No counter was re-run; no outside line was semantically judged HOLD/STALE. The census proves
  scope, not truth. No source fetches, browser/property operations or installs. The 43-vs-47
  literal reconciliation is arithmetic plus phrase inspection, marked INFERENCE.
- `.ufo/waves/round-27/pairs.json` and `discovered-pairs.json` were absent when read, so the
  denominator may grow monotonically; 57 is the frozen minimum, never a ceiling.
## 7. Reproducibility
```bash
python3 - <<'PY'
import re,json,subprocess
R=re.compile(r'\bS(\d{3,})\s*(?:[-–—]|\.\.|to|through)\s*S(\d{3,})\b'); L=re.compile(r'\bS(\d{3,})\b')
pop={r['id'] for r in json.loads(subprocess.check_output(['git','show','83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba:.ufo/waves/round-26/population.json']))['rows']}
rev='be375d90afc6fc7aca369ab3cf5247bf460aeed2'; paths=subprocess.check_output(['git','ls-tree','-r','--name-only',rev],text=True).splitlines()
for scope in ('corpus/knowledge/','outside'):
    pairs=set()
    for p in paths:
        if p.startswith(('.ufo/','.git/')): continue
        if (scope=='outside') == p.startswith('corpus/knowledge/'): continue
        t=subprocess.check_output(['git','show',rev+':'+p],text=True)
        ids={f'S{int(m.group(1)):03d}' for m in L.finditer(t)}
        for m in R.finditer(t):
            a,b=int(m.group(1)),int(m.group(2)); ids.update(f'S{i:03d}' for i in range(a,b+1))
        pairs.update((r,p) for r in ids if r in pop)
    print(scope,len(pairs))
PY
```
Hashes: SKILL.md `63fc812d…`, PROVINCE.md `f71df98e…`, corpus/README.md `a4ac3009…`,
corpus/QUALITY.md `fd5065a1…`, r26 contract `4179bde7…`, r26 statements `c2026376…`, r27
contract `6d2d7f51…`, count_c1.py `a1e46d19…`, c2-oracle.json `1d038205…`, verifier lesson
`94c43088…`, round-26 lesson `095335fd…`.

Report: .ufo/waves/round-27/w1/PeripheralScope.md
