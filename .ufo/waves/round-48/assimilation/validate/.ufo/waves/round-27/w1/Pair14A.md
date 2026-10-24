# Pair14A — (S008, corpus/knowledge/static-canonical-preflight.md) — axis: freshness

Seat: KakeR27.Pair14A (read-only reviewer, leaf). Base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`;
declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`. No network GET, no installs, no repo edits
outside this report.

## Verdict

**HOLD** — the single S008 occurrence in this entry is round-26 fetch-provenance boilerplate
("S008 via `manifest-retry.json`"), true of the round, not an attribution of any statement of this
entry, and not stale at its own stated scope. No `[r27-recheck S008 STALE]` marker is warranted.

## 1. Exact citing location

`corpus/knowledge/static-canonical-preflight.md:184` — the **only** S008 occurrence in the file
(verified: `grep -on "S0[0-9][0-9]"` over the file yields one `S008`, at line 184; the only other
range-form is `S001–S006` at line 54, which expands to S001…S006 and cannot reach S008).

Full cited line (verbatim, one physical line, line 184):

> `- Round-26 source recheck (2026-10-21, append-only; original lines unchanged). Rows S020, S021, S026, S027, S028, S029, S030, S031, S032, S033 and S034 were re-fetched by one public GET each (`.ufo/waves/round-26/fetched/manifest.json`, S008 via `manifest-retry.json`) and judged HOLD at their anchors against the retained bytes; receipts `.ufo/waves/round-26/rechecks/S0NN.json`, statement-level reviews `.ufo/waves/round-26/w1/Pair*.md`. Older verified-at/reopened dates in this entry remain the historical record of the earlier reading; they are not rewritten. Pointers labelled `at base cb807bc` stay base-scoped (QUALITY.md round-21 coordinate rule), so current-tree line movement is not a stale claim. Counting command: `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`.`

Surrounding structure: line 182 `## Round-26 source recheck`; 184 the recheck bullet; 186–194 the
appended `[r26-recheck …]` STALE/precision blocks (S021, S026, S030 ×2, S032 note); 196
`### Round-26 falsify-wave adjudication`; 198–203 the falsify-wave corrections and reclassifications.
Line 184 is the round's EOF-provenance preamble, not a body claim.

## 2. What the words actually assert (scope test)

Split the parenthetical: the sentence's asserted subject is the row list
**S020, S021, S026, S027, S028, S029, S030, S031, S032, S033, S034** — S008 is **not** in it. The
parenthetical routes fetch records to manifests: `manifest.json`, and, for S008, `manifest-retry.json`.
So the pair's claim is exactly one manifest-routing fact:

> "the round-26 fetch record for S008 is in `.ufo/waves/round-26/fetched/manifest-retry.json`"

It asserts **no** content from the GNU tar manual, and it attributes **no** statement of this entry to
S008. Corroborating scoping facts:

- `corpus/knowledge/static-canonical-preflight.md:1` (the entry's `source:` header) lists
  `S020, S021, S026, S027, S028, S029` — S008 absent; the body adds S022–S025, S030–S034, never S008.
- `corpus/SOURCES.md:16` — S008 `used-by` = `corpus/knowledge/ghp-served-set.md` only.
- `.ufo/waves/round-26/statements.json` — the r26 ledger has 41 pairs; S008 appears only as
  `{row: S008, file: corpus/knowledge/ghp-served-set.md}`; the pair
  (S008, static-canonical-preflight.md) was **never** adjudicated (it is in the 16 missing).

## 3. Evidence for the manifest-routing fact (all committed, hash-matched)

Repo path: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

| Artifact | sha256 (worktree == base == be375d9) | Relevant content |
|---|---|---|
| `.ufo/waves/round-26/fetched/manifest-retry.json` | `84e83fb0cf5bf431eb029a9ab8cab69b661054e6e992b862e87b514786a65d1b` | the **only** row is S008, `"attempt": 2`, `"status": 200`, `"bytes": 512359`, `"sha256": "93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084"`, `"file": "S008-1-retry.raw.gz"`, `"fetchedAt": "2026-10-21T15:11:01.972009+00:00"` |
| `.ufo/waves/round-26/fetched/manifest.json` | `28f9944d36db40b56362903d6ba1245ae54d26a0e612615b3174f45ea3c7cba8` | S008 index 1 = the **failed** attempt: `"status": null`, `"error": "TimeoutError: The read operation timed out"`, `"bytes": 0`, `"sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"` (empty-body digest) |
| `.ufo/waves/round-26/rechecks/S008.json` | `9e39e7da3099c442b4789919b1690339d74d776050ab5bd4536b242c22efe6ab` | `"verdict": "HOLD"`, `"fetchIndex": 1` |
| `corpus/knowledge/static-canonical-preflight.md` | `833b28f26fa7309f7e31398275bae2f704969d8e6f095bc5bb96250da5c531bc` | identical at base `83528f7` and at `be375d9` (matches `frozen/expected.json`) — no drift |

Located support (≤25 words, verbatim from `manifest-retry.json`):

> `"row": "S008", "index": 1, "attempt": 2, … "status": 200`

and from `manifest.json` (S008 entry):

> `"error": "TimeoutError: The read operation timed out"`

So the parenthetical is **true**: S008's successful round-26 bytes live in the retry manifest, while
`manifest.json` holds only the timed-out first attempt (0 bytes). `corpus/lessons/round-26.md:22-25`
says the same: "S008 first timed out at 60 s and was retried once … Bytes are retained gzip-compressed
with sha256 in `fetched/manifest.json` and `manifest-retry.json`."

## 4. Stale premise vs source-date vs irrelevant retry boilerplate

- **Stale premise — none.** The premise (S008's fetch record is in `manifest-retry.json`; manifest.json
  holds a failed attempt) is still exactly true at `be375d9`; the artifact is byte-identical at base and
  at the declared revision, and the citing file is byte-identical too. Nothing in the claim moved.
- **Source-date / historical-date noise — not the driver.** `corpus/SOURCES.md:16` gives S008
  `opened 2026-10-19`, `recheck 365d`; the r26 re-fetch is 2026-10-21 (two days later). The r26 rule
  (`.ufo/waves/round-26/statements.json:4`) states: "Historical dates and base-scoped pointers are not
  stale." Line 184 itself says older verified-at/reopened dates "remain the historical record … they
  are not rewritten". The r20 tail (`corpus/lessons/round-20.md:310`, "S008's '1.35' label is
  withdrawn") is about `ghp-served-set.md`, not this entry, and is preserved by an appended erratum —
  it is not a premise this entry leans on.
- **Irrelevant retry boilerplate — this is the classification.** Round-wide manifest routing is stated
  in an entry that does not use S008. Precedent, decided in r26 by the falsify wave's own L1:
  `.ufo/waves/round-26/w2/Rejection07S013.md:70` — "**Copied boilerplate provenance.** That same
  appended bullet includes "(S008 via `manifest-retry.json`)", but this entry cites only S011, S012 and
  S013. The same wording appears in 5 knowledge files (`git grep -c` at e28312b: crawl-scope-per-host,
  ghp-custom-domain, ghp-etag-anatomy, ghp-served-set, static-canonical-preflight). **It is true of the
  round but irrelevant to this entry. This is a provenance-precision nit, not staleness.**" — and the
  corpus already records the same reading at `corpus/knowledge/ghp-served-set.md:95`: "The words 'S008
  via `manifest-retry.json`' in the recheck paragraph name the round's retry, not a source of this entry."
  `.ufo/waves/round-26/w2/Correction3S010.md:47` rates the identical wording in the sibling file "low",
  with the optional fix "drop 'S008 via manifest-retry.json' from the line-60 preamble" — an optional
  polish, not a defect.
- **Not UNVERIFIABLE.** Every fact above is checkable offline from committed blobs with matching
  digests; nothing depends on the network.

## 5. Suggested C1 ledger record (`.ufo/waves/round-27/pairs.json`, `pairs[]`)

```json
{"row":"S008","file":"corpus/knowledge/static-canonical-preflight.md","kind":"artifact","verdict":"HOLD","reason":"Only S008 occurrence in the entry is line-184 r26 EOF provenance boilerplate '(manifest.json, S008 via manifest-retry.json)': it asserts only that the round-26 fetch record for S008 sits in the retry manifest, and attributes no statement of this entry to S008 (row list is S020,S021,S026-S034; entry source header line 1 lists S020,S021,S026-S029; SOURCES.md:16 used-by = ghp-served-set.md only). Verified at be375d9: manifest.json S008 entry is the failed attempt (status null, TimeoutError, 0 bytes, sha256 e3b0c442...b855), manifest-retry.json holds the single S008 row (attempt 2, status 200, 512359 bytes, sha256 93281a63...6084, fetchedAt 2026-10-21T15:11:01Z); recheck receipt rechecks/S008.json verdict HOLD. True of the round, irrelevant to this entry's scope: provenance-precision nit, not staleness (r26 w2/Rejection07S013.md:70; corpus/knowledge/ghp-served-set.md:95). Historical dates are not stale per r26 statements.json rule.","evidence":".ufo/waves/round-26/fetched/manifest-retry.json","contains":"\"row\": \"S008\""}
```

`contains` alternatives (each verbatim in that blob, single-line, unique): `"file": "S008-1-retry.raw.gz"`,
`"attempt": 2`, `"reason": "first attempt TimeoutError at 60s; single retry with 240s timeout"`.

`kind` note for L1: `artifact` is the faithful kind here — the adjudicated claim is a pointer to a repo
artifact, not content quoted from the GNU tar manual. A `kind:"source"` record would require an r27
fetch of S008 in `.ufo/waves/round-27/fetched/manifest.json` (currently S001–S006 only,
`fetch_group.py` filters `range(1,7)`); S008's URL timed out at 60 s in r26 and needed a 240 s retry,
and that fetch would add a new runtime rather than adjudicate an existing pointer. Not required by
contract C1 ("each of the six grouped pairs grounded against sources opened this round" applies to
S001–S006).

## 6. Correction wording

- **Required: none.** HOLD ⇒ no `[r27-recheck S008 STALE]` marker (adding one would mislabel the pair).
- **Optional precision note (non-STALE, append-only, parity with `ghp-served-set.md:95`)** — if L1 wants
  the ambiguity closed. Suggested wording, appended at EOF, leaving line 184's bytes and the
  2026-10-21 / 2026-10-19 dates untouched:
  `- Round-27 precision note (append-only, not STALE): the words "S008 via `manifest-retry.json`" in the round-26 recheck bullet name that round's single retried fetch (S008 attempt 2; manifest.json holds the timed-out first attempt) and are not a source of this entry, which cites S020-S034 only. HOLD (w1/Pair14A.md).`
  This is a precision note, so it must not be tagged with a STALE marker and must not alter the
  r26-ledger counts.

## 7. Uncertainties, gaps, denominator

- Residual interpretive risk (only): a reader could mis-parse the parenthetical as "…and S008 (via
  manifest-retry.json) was also re-fetched for this entry". That reading is unsupported (S008 is not
  in the entry's row list, not in its `source:` header, and SOURCES.md assigns S008's used-by to
  `ghp-served-set.md`), so it does not make the sentence false at its stated scope; the r26 L1 ruling
  above already fixed this reading. §6's optional note removes the residual ambiguity.
- Known r26 debt, not a defect of this citation and out of scope for this pair: the retry manifest was
  produced by an inline command and `fetch_retry.py` was committed post hoc
  (`.ufo/waves/round-26/w2/FetchCritic.md:61`, `corpus/lessons/round-26.md:76`). The manifest remains
  the evidence; the citation's own scope does not depend on the generator.
- Denominator: **no new citing pair discovered** by this seat. The pair
  (S008, corpus/knowledge/static-canonical-preflight.md) is already enumerated by the frozen C1
  counter; my pair count is unchanged at 57 citing pairs / 16 missing
  (`python3 -B .ufo/waves/round-27/count_c1.py --root . --revision be375d90afc6fc7aca369ab3cf5247bf460aeed2`
  → population 32, citingPairs 57, decided 41, r26Carried 41, missing 16, and this pair is listed
  among the 16). Adjudicating it reduces the missing set by one (16 → 15) and grows the decided set
  by one (41 → 42); the denominator never shrinks.
- Verification gaps: none for this pair — all support is offline, committed, and hash-checked at the
  declared revision. No r24 stopped work was read, retried, rephrased, or rerouted.

## 8. Tooling

No tool installed or upgraded; no pacman transaction; no service mutation. Read-only git
(`show`, `ls-tree`, `status`), `grep`, `sha256sum`, `python3 -B` (frozen `count_c1.py`, stdlib only).
Only this report written, under `.ufo/waves/round-27/w1/`. No scratch directory was needed.

Report: .ufo/waves/round-27/w1/Pair14A.md
