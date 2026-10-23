# Round 38 wave 2 — ReopenGateS099 (freshness / OPER)

Target: `corpus/lessons/round-38.md:39-42` (S099 Gate line) and `corpus/SOURCES.md:107` (S099 row) at
`adab4c7e9ec2178657395f49346f18800ff4796f`; row's `used-by` target `corpus/knowledge/robots-txt-rules.md`.
Sandbox: `/fast/scratch/hyaku/kake-r38w2/ReopenGateS099` (`TMPDIR` set there). No installs.

## Commands and observed output (exit code after `;`)

1. `curl -sS -o rfc9309.html -w 'http_code=%{http_code} size=%{size_download}\n' https://www.rfc-editor.org/rfc/rfc9309.html` → 0, `http_code=200 size=82367`.
2. `sha256sum rfc9309.html` → `bbaa280636d3e38f0a1a130a5ce40e9753db1ed18c860945b0bf795ff8dc1a87` — byte-equal to the row's sha and to `.ufo/waves/round-37/sources/receipts.json` S011 `bodySha256` (`bodyBytes` 82367).
3. `git -C … show adab4c7e:…/round-37/sources/S011.html.gz | gunzip | sha256sum` → same hash, 82,367 B; `cmp` live vs retained → 0.
4. Whitespace-normalized page text: exact quote count `use case-insensitive matching to find the group that matches the product token` = **1**; containing sentence = **“Crawlers MUST use case-insensitive matching to find the group that matches the product token and then obey the rules of the group.”**; paragraph id `section-2.2.1-4` at `rfc9309.html:1560-1561`.
5. Heading scan: 1, 1.1, 2, 2.1, 2.2, 2.2.1–2.2.4, 2.3, 2.3.1, 2.3.1.1–2.3.1.5, 2.4, **2.5 Limits** (`rfc9309.html:1865`), 3, 4, 5, 6 (References). Header text: “RFC 9309 Robots Exclusion Protocol (REP) September 2022 … Standards Track”; page carries `2022-09`.
6. `curl -sSL 'https://www.rfc-editor.org/errata_search.php?rfc=9309'` → 0, HTTP 200 (final `errata.rfc-editor.org/search/?rfc_number=9309`); 4 errata, **all `Status: Reported`**: 7124 §5.2 (2022-09-10), 7128 §2.2.2 (2022-09-13), 7995 §2.2 (2024-06-18), 8895 §2.3.1.5 (2026-04-28).
7. `git show adab4c7e:corpus/knowledge/robots-txt-rules.md` scans: **3** S099 tokens (lines 1, 89, 114); **26** `S011 §…` tokens (e.g. 29 §2.3.1.5/§2.5, 33 §§2.2.1–2.2.4, 39 §2.2.1, 49 §2.2.2, 51 §2.2.3, 55 §2.2.2, 61 §2.2.2, 77 §2.3.1.2/§2.4). S011's row scope is “Section 2.3 Access Method and 2.3.1.4 Unreachable Status” (`SOURCES.md:19`).
8. `git diff af43a50f adab4c7e -- corpus/SOURCES.md` → S011 line has no diff; S099 row is added at line 107. `corpus/knowledge/robots-txt-rules.md` diff is 41 insertions / 1 deletion (the `source:` header line plus appended amendment (k), which cites `S099 §2.2.2` at line 114); no existing body statement changed.

## Verdicts

- **Quote present verbatim — HOLDS** (confidence high). It is a contiguous verbatim substring after HTML whitespace normalization; section `§2.2.1` is correct (`section-2.2.1-4`).
  **Caveat (overstated as a sentence quote):** it is a mid-sentence fragment. The source sentence opens “Crawlers MUST” and closes “and then obey the rules of the group”; the Gate drops the normative subject. Per `CORPUS.md:112-114` the quote must ground `teaches`; it grounds only case-insensitive group matching, while the row's `teaches` claims group selection, path matching, retrieval and parsing — 1 of 4.
- **HTTP 200 / access 2026-10-23 — HOLDS** for status and body. **sha256 `bbaa2806…dc1a87` — HOLDS exactly**, against both a fresh GET and the retained round-37 HTML.
- **“published September 2022” — HOLDS** (page header, `2022-09`).
- **Scope “§§1–5 (groups, rule matching, retrieval, encoding and limits)” — HOLDS** on content: groups §2.2.1, matching §2.2.2–2.2.3, retrieval §2.3/§2.3.1.x, encoding §2.3 (“The file MUST be UTF-8 encoded”, `rfc9309.txt:1408`) and §2.2.3, limits §2.5. Minor overbreadth: §§3–4 are Security/IANA, not REP behavior.
- **Anchor “Sections 1–5, especially §§2.2.1–2.5” — HOLDS**; §2.5 exists and §6 References sits outside the range.
- **`teaches` “supersedes S011 — …” — HOLDS in form** (`CORPUS.md:116-118` mandates that opening for a correction row) and in scope (S099 is a superset of §2.3/§2.3.1.4). **OVERSTATED as the round-37 complaint's repair:** `SOURCES.md:207` said S011's scope is narrower than its *use*; the entry still credits S011 with 26 section citations, at least 20 naming sections outside S011's row scope, while S099 is cited 3 times. The wider row is filed but the corpus statements it was owed for still cite the narrow row. Confidence high.
- **`status: mined` — HOLDS**: the entry cites S099 §2.2.2 (line 114); the lesson cites it at line 39; both `used-by` paths exist.
- **Harm (curation, not a rule breach):** the same URL and identical bytes are now registered twice, both `mined`, both 365d recheck, opened 2026-10-19 vs 2026-10-23 → one document carries two recheck obligations four days apart (`CORPUS.md:123-125`: “a short registry … beats a long one”). No `CORPUS.md` rule forbids duplicate URLs; duplicate *ids* are the prohibited case.
- **Access-time fact 04:30:34Z — WEAK/unverified.** `.ufo/waves/round-38/w1/ScribeSourcesRows.md` prints `2026-10-23 04:30:34Z` as the `date -u` output for **all five** sequential GETs, while the lesson gives six timestamps across four distinct values (S098 04:30:17, S034 04:30:20, S011 04:30:20, S100 04:30:22, S101 04:30:17, S099 04:30:34). Both records cannot be right; S099's figure matches the report, but that report cannot timestamp five fetches at one second. The round-38 tree retains no source receipt (`git ls-tree .ufo/waves/round-38/` has no `sources/`); the only retained 9309 bytes are round-37's S011 artifact.
- **Currency — INCOMPLETE (not wrong):** neither the Gate line nor the row records the four open technical errata. 8895 (2026-04-28) disputes §2.3.1.5's “Crawlers MUST try to parse each line … MUST use the parseable rules”, which the entry states at line 29; 7995 (2024-06-18) disputes the §2.2 `path-pattern` ABNF. All are `Reported`, not `Verified`, so the published RFC remains normative; but the entry's `recheck:` already names “an RFC 9309 … erratum”, so the trigger fired and nothing was recorded.

## Remaining unknowns

- No round-38 shell transcript for the 04:30:34Z GET; the lesson's per-source times have no retained receipt to check against.
- Low-weight anomaly: `.ufo/waves/round-38/w1/ScoutWhatwgUrl.md:34` proposes `urllib.parse.html` “as S099”; landed S099 is RFC 9309. Wave-1 record misnumbers; no effect on the registry row.
