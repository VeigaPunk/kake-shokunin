VERDICT: the sources hold. All 3 RFC bodies are byte-identical to L1/src and to the SOURCES digests, and every quote is verbatim and ≤25 words. S466 and S468 admit. S467 admits with one defect: its used-by names `corpus/knowledge/cache-key-construction.md`, which does not cite S467. So the use side of D89-3 (construction entry grounded on S463) is still open, and the C1 D3 predicate cannot see it. There are three cosmetic line/count errors. All three rejects are upheld.

Seat: ScoutSources (kake round 90, w1). Leaf seat, read-only on LANE. Writes only here and in `w1/ScoutSources/`.

## 1. Re-fetch (network: 3 GETs, only the URLs named in the item)

Command: `curl -sS -o $u.txt -w '%{http_code}' https://www.rfc-editor.org/rfc/$u.txt`, then `sha256sum` and `cmp` against `.ufo/waves/round-90/L1/src/$u.txt`. Receipt: `.ufo/waves/round-90/w1/ScoutSources/fetch-receipt.txt`

| URL | accessed (UTC) | HTTP | bytes | sha256 | = L1/src | = SOURCES row |
|---|---|---|---|---|---|---|
| rfc9110.txt | 2026-11-04T22:14:24Z | 200 | 502941 | 21c1cdce…f47232a | `cmp` identical | S466 (and S465) yes |
| rfc9111.txt | 2026-11-04T22:14:25Z | 200 | 84477 | aeb52adb…5302cf3e | `cmp` identical | S467 yes |
| rfc8259.txt | 2026-11-04T22:14:27Z | 200 | 28360 | 61a5378f…b4cd2d7 | `cmp` identical | S468 yes |

The knowledge entry claims "the two RFC 9110/9111 digests equal the round-89 retained copies". This is confirmed: `find .ufo/waves/round-89 -name 'rfc91*' -exec sha256sum` shows `round-89/L1/src/rfc9110.txt` = 21c1cdce… and `rfc9111.txt` = aeb52adb…. The lesson's Gate table (status, bytes and sha for all three) matches my fetch. I did not keep my fetched bodies because they are byte-identical to the committed `L1/src` copies. The fetch receipt holds the digests.

## 2. Quote location

The checker is `.ufo/waves/round-90/w1/ScoutSources/qcheck.py` and its output is `.ufo/waves/round-90/w1/ScoutSources/quote-check.txt` (exit 0). For each quote it checks whitespace-normalised containment in the stated line range, finds the minimal physical line span, and counts words by whitespace split. I also read each range by eye with `awk 'NR>=a&&NR<=b'`.

| Where | Quote (abridged) | Stated | Actual span | Words | Verdict |
|---|---|---|---|---|---|
| lesson Gate S466 | "Field values containing CR, LF, or NUL …dangerous" | 9110 1606–1607 | 1606–1607 | 12 (claimed 12) | OK |
| lesson Gate S467 | "and is composed from, at a minimum, the request method and target URI" | 9111 252 | 252 | 13 (claimed 13) | OK |
| lesson Gate S467 | "Caches differentiate these responses … the cache key as well" | 9111 258–261 | **259–261** | **19 (claimed 20)** | verbatim; start line off by one; word count wrong |
| lesson Gate S468 | "JSON text exchanged … using UTF-8" | 8259 485–486 | 485–486 | 18 (claimed 18) | OK |
| lesson Gate S468 | "the characters that MUST be escaped: … (U+0000 through U+001F)" | 8259 429–431 | 429–431 | 17 (claimed 17) | OK |
| lesson reject 2 | tchar includes "%" | 9110 1735–1737 | `"%"` on 1735; 1735–1737 is the tchar production | — | OK (the range cites the production) |
| knowledge S466 | "Field values containing CR, LF, or NUL characters are invalid and dangerous" | 9110 **1606–1609** | **1606–1607** | 12 | verbatim; range over-states the end and disagrees with the lesson (1606–1607) |
| knowledge S467 | "The "cache key" is the information a cache uses to choose a response" | 9111 251 | 251 | 13 | OK |
| knowledge S468 | "JSON text exchanged … using UTF-8" | 8259 485–486 | 485–486 | 18 | OK |

- Non-verbatim quotes: none.
- Quotes over 25 words: none.
- SOURCES anchors are correct:
  - S466: 1579 is the `5.5.  Field Values` heading; 1606–1612 covers the CR/LF/NUL sentence through "also invalid; however".
  - S467: §2 heading at 9111:236; 251–262 is the key paragraph pair; 526 is the `4.1.` heading.
  - S468: 424 is the `7.  Strings` heading through 431; 483 is the `8.1.` heading through 486.

## 3. Row judgment against CORPUS.md "SOURCES.md — where a shokunin learns" (contract v1)

Structural checks, all passing:

- **Columns:** S463, S465, S466, S467 and S468 each have exactly 11 cells (awk split, NCOLS=11). No `|` inside any cell.
- **kind and tier:** `spec`, tier A. This fits an IETF RFC for the stated scope.
- **S463 immutability:** `git diff 209027f4 e50c9566 -- corpus/SOURCES.md` contains only three `+` lines (S466–S468). S463 is byte-identical. The rule-2 supersede form is met: S467's `teaches` opens `supersedes S463 —`, with the em-dash bytes confirmed as `342 200 224` by `od -c`.
- **Rule 1:** the lesson `## Gate` gives the URL, access date and a ≤25-word located quote for every new row.

Per row:

- **S466: ADMIT.** It is correctly scoped (field-value validity, distinct from S465 tokens), the anchor is exact, and it is genuinely cited by `cache-key-conformance-gate.md` (its `source:` line), so `mined` is true.
  - Minor `teaches` overreach: "other control characters are also invalid but may be retained". The source restricts retention to "for the sake of robustness when they appear within a safe context" (lines 1612–1614), and the row drops that condition.
  - The Gate quote grounds only "invalid and dangerous". The reject-or-replace MUST (1608–1610) is cited by anchor but not quoted.
- **S467: ADMIT WITH DEFECT.** The scope, anchor, supersede form and §2 content are correct. 252 does say method plus target URI at minimum, and 259–262 does add Vary fields per §4.1. The defect is in the `used-by` cell, which lists `corpus/knowledge/cache-key-construction.md, corpus/knowledge/cache-key-conformance-gate.md`. The first path is false:
  - `grep -n 'S46[3-8]' corpus/knowledge/cache-key-construction.md` finds only S463 (lines 1 and 18) and S465 (line 32).
  - `git diff 209027f4 e50c9566 --stat` shows that the carrier did not touch `cache-key-construction.md`.
  - `corpus/README.md:133` still maps cache-key construction to "S463 S465".
  - CORPUS.md defines `used-by` as "paths of the knowledge entries or lessons citing the row". The construction entry does not cite S467, so the cell asserts a citation that does not exist. The construction entry still grounds itself on S463, whose scope says "not cache-key construction", and that is the substance of D89-3.
  - Fix options, for L1 to choose: either add S467 to `cache-key-construction.md`'s `source:` and to the README:133 map (logging the old→new change), or drop the construction path from S467's used-by and say plainly that D89-3's use side stays open.
  - Also minor: the knowledge entry's only S467 quote is the definition sentence (line 251). The construction-ingredient sentence (line 252) is quoted only in the lesson.
- **S468: ADMIT.** RFC 8259 (STD 90) is primary for JSON text. The scope correctly limits the row to two advisory cases.
  - Minor `teaches` overreach: "JSON text exchanged between systems must be UTF-8" drops "that are not part of a closed ecosystem" (line 485–486). A stdin/stdout gate harness is arguably a closed ecosystem, which is a further reason the case stays advisory.
  - The inference "a raw control character makes the input not JSON" is sound from the §7 MUST-escape list.

### Counter weakness this exposes (C1, D3 predicate)

`.ufo/waves/round-90/c90_defects.py` `item_d3` (lines 199–244) closes D3 when all of the following hold:

- S463 is byte-identical;
- some new row's `teaches` starts with `supersedes S463 —`, its source contains `rfc9111`, its status is `mined`, and its scope lacks "not cache-key construction";
- some Gate line naming that id contains any 3–25-word quote found anywhere in the retained rfc9111 body.

It never checks:

- that `cache-key-construction.md` (the "use" half of D89-3) cites the superseding row;
- that the new row's `used-by` is truthful;
- that the quote sits at its stated line or grounds `teaches`.

So `met=true` for D3 is satisfiable, and is in fact satisfied, while the construction entry still cites only S463. This is an inference from reading the code. I did not build a forgery fixture.

## 4. Re-judging the lesson's three rejects

- **Reject 1 (the round-89 byte layout "is what RFC 9111 specifies"): UPHELD.** 9111 §2 (251–256) composes the key from at least method and URI. Line 264 says "Caches might incorporate additional material into the cache key". There is no byte layout anywhere. The contract omits the method, and 255–256 notes that GET-only caches use only the URI, which R90-4 could cite.
- **Reject 2 (M37 "equivalent because names cannot contain `%`"): UPHELD.**
  - The source claim is at `.ufo/waves/round-89/w1/MutKey.md:109`, under `### 5.2 Equivalent mutants` (line 103).
  - `%` is a tchar at 9110:1735.
  - The contract (`round-89/c2-contract.md:38`) escapes `%`→`%25` in each name.
  - The carrier receipt `.ufo/waves/round-90/controls/after-c2-carrier.txt` reads `M37-absent-name-not-escaped.py => … clauses=5/6 hand=69/70 generated=105/120 … met=false`, while the shipped `scripts/cache_key.py` reads `met=true`.
  - The gate cases `name-percent-present` and `name-percent-absent` exist at `scripts/cache_key_conformance.py:189,191`.
- **Reject 3 (adding NUL to the refusal list this round): UPHELD.** 9110:1608–1610 allows either reject or replace-with-SP, so the RFC does not force refusal. Choosing one changes the contract, and routing it as R90-2 is right. It is labelled "row candidate", but it is a contract proposition rather than a source row. The label is cosmetic.

## 5. Defects found (all lane-internal)

1. **S467 `used-by`** lists `cache-key-construction.md`, which does not cite S467. The construction entry and README:133 still ground construction on S463 alone, so D89-3's use side is open. (Substantive.)
2. **C1 D3 predicate** does not check the use side, `used-by` truth, or quote position, so it is weaker than the defect it scores. (Substantive, counter design.)
3. **Lesson Gate, S467 second quote:** it is 19 words, not 20, and it starts at line 259, not 258. (Cosmetic.)
4. **Knowledge `## Located quotes`, S466:** the range 1606–1609 should be 1606–1607, and it disagrees with the lesson. (Cosmetic.)
5. **`teaches` overreach:** S466 drops "safe context" and S468 drops "closed ecosystem". (Minor.)

## Limits

- I did not run c90_defects.py or c90_gate.py and built no fixture; other seats own those.
- Word counts use whitespace splitting.
- I did not check the "202 → 205 rows" count.
- Tools installed or updated: none.
- Scratch `/fast/scratch/hyaku/kake-r90/ScoutSources/` was deleted after the receipts were copied.
