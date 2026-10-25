# ScoutCounterC2Tip — C2 counter at the lane tip, and one hand re-check

Seat: `L1Kake51.ScoutCounterC2Tip-2` (scout, read-only). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Measured revision: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (`git rev-parse HEAD` at run time).
Base: `007d66e4e8360a5f88d29a93eeedd8066dad4434`. Contract read: `.ufo/waves/round-51/contract.json`
(sha256 `1f158422622ce027a3938428953bef40b3189281625768befd351f396aa79d18`, identical to the blob at the measured revision).

---

## 1. Command and verbatim output

```
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/c51_quote_truth.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin \
    --revision 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)
  C1_entries_exist pass
  C2_entry_cites_id pass
  C3_row_shape pass
  C4_used_by pass
  C5_gate_quote_truth pass
  C6_receipt_pins pass
  C7_validate_before_append pass
  C8_append_after_mirror pass
  revision: 9d13768c4fdd0e9a2688d2ecf1616b539cf57658
EXIT=0
```

The executed counter is the committed artifact: `sha256(.ufo/waves/round-51/c51_quote_truth.py)` in the worktree
equals `sha256(git show 9d13768:.ufo/waves/round-51/c51_quote_truth.py)` = `29a899a0345d36b457e8381e0f611b00cda920f741d3e52cbf3ba88df156f99f`.

Do-nothing control re-run by me, not taken from `controls/c2-before-base.txt`:

```
$ python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 007d66e4e8360a5f88d29a93eeedd8066dad4434
C2 quote-truth 0/8 met=False  ... (all eight FAIL)
EXIT=1
```

So the 8/8-at-tip and 0/8-at-base figures reproduce. The claim's *predicate* (the counter's own arithmetic)
holds. Section 4 shows the predicate is earned partly by reading a different object than the frozen condition names.

---

## 2. Hand re-check of one condition: `C6_receipt_pins`

I did not take C6 on the counter's word. Re-derived from committed bytes with `git show` + `sha256sum`,
independent of `c51_quote_truth.py`:

| id | `git show <rev>:...sources/<id>.html \| wc -c` | `sha256sum` of those bytes | receipt `bytes` / `declaredBytes` | receipt `sha256` |
|---|---|---|---|---|
| S262 | 174926 | `792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b` | 174926 / 174926 | `792224334aea…d50d23b` ✔ |
| S263 | 175561 | `6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de` | 175561 / 175561 | `6afbdc826e55…a4e155de` ✔ |

URL clause, checked as exact token rather than the counter's substring test:
`S262` receipt `https://developers.google.com/search/docs/crawling-indexing/canonicalization` == the URL token in
`corpus/SOURCES.md` row S262 cell 2 (split on ` — `) — **exact match**; same for `S263` →
`…/crawling-indexing/googlebot`. `C6` is genuinely true for both ids.

Supporting hand checks (same method, cheaper):

- **C5** — `grep -F` of each lesson Gate quote against the retained body returns exactly 1 raw hit each:
  `"indicating a canonical preference is a hint, not a rule"` (10 words) in `S262.html`;
  `"Googlebot is the generic name for two types of"` (9 words) in `S263.html`. Both inside the frozen 6–25 window.
- **C3/C4** — both rows parse to 11 cells at the measured revision, `status=mined`, `opened=2026-10-24`,
  `recheck=180d`, `used-by` exactly one path (`corpus/knowledge/canonical-selection.md`, `…/crawler-identity.md`).
- **C1/C2 content** — `S262.html` title is "What is URL Canonicalization … Google Search Central"; `S263.html`
  title is "What Is Googlebot … Google Search Central"; each body carries its receipt's doc revision
  (`Last updated 2026-08-20 UTC`, `Last updated 2026-02-03 UTC`). Bodies are not interchangeable (distinct sizes,
  distinct hashes, distinct titles).

**Verdict for the hand-checked condition: C6 true** (high confidence, byte-level, tool-independent of the counter).

---

## 3. Independent provenance checks that agree with the counter

Row accounting at the root registry (`corpus/SOURCES.md`, parsed with the census parser's `^ {0,3}\|` rule):

| revision | registry rows | S262 | S263 |
|---|---|---|---|
| `007d66e` (base) | — (entries/rows absent) | no | no |
| `19a99bd` (mirror commit) | 143 | no | no |
| `5591557` (append commit) | 145 | yes (11 cells) | yes (11 cells) |
| `9d13768` (tip) | 145 | yes (11 cells) | yes (11 cells) |

`git diff --stat 19a99bd 5591557` touches only `LOG.md`, `corpus/SOURCES.md` (+2 lines), the two knowledge entries
and the lesson — no existing registry row was edited. The append is real and clean at the root.
`merge-base --is-ancestor 19a99bd 9d13768` exits 0, and `19a99bd != 9d13768`, so the mirror commit is a strict ancestor.

---

## 4. Finding: `C8` passes because the counter reads the root registry, not the mirror

`contract.json` C8 reads: *"… the **mirror's** registry carries none of the adopted ids and the measured
revision's registry carries all of them."* `c51_quote_truth.py:277` implements the middle clause as

```python
mirror_registry = show(root, mirror_commit, REGISTRY)   # REGISTRY = "corpus/SOURCES.md"
```

i.e. the **repository's own registry at the mirror commit** — not the `MIRROR` constant defined at line 51
(`.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md`). The mirror file itself is never opened by C8.
That substitution decides the verdict, because the two objects disagree:

| object | rows | has S262/S263 | sha256 |
|---|---|---|---|
| `corpus/SOURCES.md` @ `19a99bd` (what the counter reads) | 143 | **no** | `cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117` |
| `…/pre-append/corpus/SOURCES.md` @ `19a99bd` (the literal mirror) | 145 | **yes, both** | `4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3` |
| `corpus/SOURCES.md` @ `5591557` (post-append) | 145 | yes, both | `4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3` |

The mirror blob at the mirror commit is **byte-identical to the post-append registry**. This is not a
grep artefact: the mirror is a full-tree copy whose blobs equal the post-append root blobs —

- `pre-append/corpus/SOURCES.md` = `4ea81a5a…` = `corpus/SOURCES.md`@`5591557`
- `pre-append/corpus/knowledge/canonical-selection.md` = `6fee23e433ca` = `corpus/knowledge/canonical-selection.md`@`5591557`
- `pre-append/corpus/knowledge/crawler-identity.md` = `cac135880712` = `corpus/knowledge/crawler-identity.md`@`5591557`
- `pre-append/corpus/lessons/round-51.md` = `dc9ab00ab051` = `corpus/lessons/round-51.md`@`5591557`
- both trees hold the same 130 corpus files, set-identical (`comm` diff empty)
- `git diff --stat 19a99bd 5591557 -- .ufo/` is empty: the mirror was never touched by the append commit.

So "pre-append" names a tree that already *is* the post-append corpus, committed 9 s earlier
(`19a99bd` 23:20:47 −0300; `5591557` 23:20:56 −0300). Consequences on committed bytes:

1. **C8's frozen sentence is false under its plain reading.** The mirror's registry does carry S262 and S263 —
   2 rows, 145 total. `conditions_passed` is therefore **7 of 8**, and `met: conditions_passed == 8 of 8`
   is **False** for C2 as written. The counter's `8/8 met=True` is an artefact of reading `corpus/SOURCES.md`
   at `mirror_commit` instead of the mirror.
2. **C7 is literally satisfied but evidentially empty of "before".** The census argv names `--file` and the mirror
   path, not `--root`; exit is `0`; stdout carries only `W04` duplicate-URL lines and `file ok` — no `E03`/`E04`.
   But the file it validated already contained the adopted rows (section above), so this receipt certifies a
   *prospective post-append* file's format, not a clean pre-append registry. The lane's own `LOG.md` concedes it:
   *"The mirror is the lane's `corpus/` **plus the two new rows and the two admitted knowledge files** …"*
   (`LOG.md`, round-51 mirror bullet).
3. **The counter cannot see this by construction.** Only `C7` and `C8` reference the mirror; `C7` checks argv/exit
   text, `C8` checks the wrong file. A one-line change to read `MIRROR` at `mirror_commit` would flip C8 to FAIL
   on today's bytes — that is the cheapest falsification test for any reviewer.
4. **Inherited, not invented here.** Round 50's mirror commit `33eec7f` already carried its adopted row
   (`S286`: mirror `yes`, root `no`) and its mirror bytes (`cd9ee4cf…`) are exactly round 51's pre-append root.
   Round 50's counter (`c50_quote_class.py`) contains no mirror check at all. Round 51 added the mirror condition
   but bound it to the root object. The mislabel is systemic across the two rounds, so this report should be read
   as a recurring-evidence defect, not a one-off typo.

**Confidence: high** for every byte-level statement above (each is a direct `git show`/`sha256sum`/`ls-tree` result
quoted with its value). **Confidence: medium-high** for the adjudication that C8 fails — it depends on reading
"the mirror's registry" as the registry *inside the mirror*, which is how C7 uses "the mirror path" and how the
counter names its own `MIRROR` constant; the alternative reading ("the lane's registry at the mirror commit")
is what the code implements and would make C8 pass, but then the mirror file is never tested by any of C1–C8.

---

## 5. Freshness judgement for the C2 seat

- **Substance landed.** Two genuinely fresh, source-pinned entries: bodies fetched 2026-10-24T23:16:49−03:00
  (`receipts.json.fetchedAt`), 174 926 / 175 561 bytes, sha256 pinned and hand-reproduced, doc revisions
  2026-08-20 / 2026-02-03 present in the bytes, gate quotes raw substrings, rows `mined` / `opened 2026-10-24` /
  `recheck 180d`, `used-by` single-entry. The freshness move is real work, not a restatement.
- **Attestation does not hold as frozen.** Under the contract's own C8 sentence the predicate is 7/8, so
  `met=False`. The failure is narrow and mechanical (mirror object), not a fabricated source: the bytes of both
  Google pages are what the receipts say they are.
- **Do not read this as "the rows were already there".** Root `corpus/SOURCES.md` went 143 → 145 rows with
  `+2` insertions and no cell edits; both ids are absent at `19a99bd` and present at `5591557`. The append is real.
  What is missing is evidence that the pre-append *mirror* was a pre-append state.
- **Quality note (not a failure).** The S263 Gate quote, `"Googlebot is the generic name for two types of"`,
  is a sentence prefix ending on the preposition "of"; it satisfies the frozen 6–25-word rule and is raw, but it
  asserts less than the row's `teaches` cell (the smartphone/desktop split and the user-agent discriminator live in
  separate *collapsed-only* quotes inside the entry). A stricter quote rule would require a complete clause.

---

## 6. Unresolved / not verified here

- **Authoring order is unknowable from commits alone.** The observed state is consistent with "write prospective
  post-append registry → census it → commit it as the mirror → copy it over `corpus/SOURCES.md`". That workflow is
  defensible as a pre-write validation; it is still not a pre-append *snapshot*, and it is what the counter's C8
  substitutes away. Commit timestamps are author-controlled, so I do not treat them as independent proof.
- **Remote truth not re-fetched.** I verified the retained bodies against their receipts and confirmed the pages'
  identity/revision from the body itself. I did **not** issue a network GET to `developers.google.com`; nothing here
  certifies that today's live page still matches the retained 2026-10-24 body (that is `recheck: 180d`'s job).
- **C1 not assessed.** `c51_wave_ledger.py` was reported 0/3 at dispatch; it is another seat's object and I did not
  run or judge it. My 8/8 reproduction is independent of it.
- Files read but not written: contract, both counters' source, `corpus/SOURCES.md` at four revisions, both knowledge
  entries, `corpus/lessons/round-51.md`, `receipts.json`, `census-{argv,exit,stdout}.txt`, guard receipts,
  `LOG.md` tail, round-50 mirror blobs. No file was unreadable.
- **Tooling:** no install or upgrade was performed in this seat, so there is nothing to record under the
  2026-10-19 directive.
