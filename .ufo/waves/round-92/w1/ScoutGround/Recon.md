# ScoutGround — round-92 planning data-walk (freshness / heuristic ground)

Scope: read-only walk of LANE working-tree bytes (`/home/vgpnk/Projects/shokunin/kake-shokunin`).
No file outside `.ufo/waves/round-92/w1/ScoutGround/` and `.ufo/waves/round-92/w1/ScoutGround.md`
was written. No git mutation, no network, no scratch clone. Reads are of the **working tree**,
not of committed bytes: the carrier-revision check is routed to the L1 (see Limits).

Hits file: `hits.txt` in this directory (grep output, 253 lines; regenerate with the two
commands in §Reproduce).

---

## 1. Existing freshness / staleness / Cache-Control material

### 1a. Named instruments (`scripts/`, `corpus/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`)

| Instrument | Hit (file:line) | What it decides | Relation to round-92 C2 |
|---|---|---|---|
| `scripts/stored_reuse.py` | `:17`, `:30-31`, `:224`, `:306`, `:312` | Reuse vs revalidate vs serve-stale, with `freshness_lifetime` and `current_age` from `s-maxage`/`max-age`/`Expires−Date` | **The composition partner.** Its "no heuristic" answer is the decision C2 refines. See §2. |
| `scripts/cache_current_age.py` | `:6` ("not a Date parser, clock, network client, freshness") | RFC 9111 §4.2.3 age arithmetic only | Upstream of any lifetime comparison; C2 does not compute age. Not duplicated. |
| `scripts/cache_control_effective.py` | `:141`, `:183-206` (`freshness_lifetime_seconds` field and selftest) | Field-specific Cache-Control lifetime (r86) | Already decides explicit lifetime from directives; its `freshness_lifetime_seconds` is `null` when no explicit lifetime exists. It has **no** Last-Modified input. C2 must not re-implement this grammar (see K91-9 / R91-4). |
| `scripts/vary_match.py` | `:33` ("freshness or serving behaviour: … not") | RFC 9111 §4.1 match only | None. Scope disclaimer only. |
| `scripts/cache_key.py` | — (no freshness hit) | Key construction | None. |
| `scripts/cache_key_conformance.py` | — (no freshness hit) | Key conformance gate | None. |
| `SKILL.md` registry | `:1568` cache_control_effective; `:1587` cache_current_age; `:1607` vary_match; `:1610` cache_key; `:1613` cache_key_conformance; `:1634` stored_reuse; `:1635` c91 reuse | Verdict maps; each says "not a … freshness decision" | Each row disclaims freshness; no row decides heuristic lifetime. |
| `PROVINCE.md` | `:724-747` (Round 91 section) | Round-91 scope excludes "heuristic freshness (§4.2.2 — with no explicit lifetime the answer is `heuristic-undecided`, never a guessed number)" | Explicit deferral. C2 is the first owner of §4.2.2. |
| `SCORECARD.md` | `:5609`, `:5611`, `:5618-5622` (repertoire row), `:5631-5640` (Planned after round 91) | Lists "heuristic freshness (§4.2.2)" as **open** | C2 retires this item; the round-92 SCORECARD section must say so. |
| `corpus/README.md` | `:731-733` (Round-91 frontier, "Still open on this axis … heuristic freshness (§4.2.2)") | Open-list | C2 supersedes this sentence in an appended round-92 paragraph (precedent: `## Round-88 frontier step`, which says "This supersedes only …"). |

### 1b. Knowledge entries (`corpus/knowledge/`) — every hit on freshness/staleness/Last-Modified/heuristic/Expires

Pattern: `[Hh]euristic|[Ss]tales?|[Ll]ast-[Mm]odified|[Ee]xpires|heuristic freshness|freshness lifetime`.
Full list in `hits.txt` §B. HTTP-relevant entries only:

| Entry:line | Text (abridged) | Duplicates / extends / contradicts C2 contract |
|---|---|---|
| `cache-control-effective.md:4-5` | `ground: freshness — round-86 C2 … scope: … explicit freshness lifetime inputs … not general HTTP cache conformance.` | Extends nothing; scope is explicit lifetime only. Consistent. |
| `cache-control-effective.md:16` | "4. Otherwise there is no explicit freshness lifetime; heuristic freshness is a separate question." | **Consistent with and is the precondition for C2.** C2 answers "separate question". Do not edit this line; append only. |
| `cache-control-effective.md:20` | "Freshness lifetime is not remaining freshness … This instrument does not calculate current age …" | Consistent. |
| `cache-control-effective.md:70` | "No browser cache model; no Vary, Age calculation, Pragma, **heuristic freshness**, …" | Declares heuristic freshness out of scope **for that entry**. C2 is the separate entry that takes it. |
| `cache-current-age.md:52-54` | "A computed age … does not prove freshness or reuse permission. RFC §4.2 also requires `freshness_lifetime > current_age`" | Consistent. C2 reports a lifetime, not a reuse permission. |
| `cache-key-construction.md:129, 175-178` | "section 4.2's freshness are separate questions"; "does not decide … freshness or age (§4.2; S462 holds the age arithmetic)" | Consistent. Names §4.2 as separate; C2 is §4.2.2. |
| `capture-drift-validators.md:154-155` | "not a freshness guarantee for any later instant" | Homonym-adjacent (capture drift, not HTTP freshness). No conflict. |
| `stored-response-reuse.md:5` | "scope: … not a Date parser, clock, network client, revalidation exchange, cache store, **heuristic freshness**, …" | Declares heuristic freshness out of scope for that entry. Consistent with C2 being separate. |
| `stored-response-reuse.md:37-38` | "`Expires − Date`, else `null`. The order is first-match … `Expires` may precede `Date`" | **Explicit-lifetime rules that C2 must not re-decide** (C2 clause 10 is the same order; identical by construction). |
| `stored-response-reuse.md:55-57` | "**No heuristic freshness.** §4.2.2 lets a cache assign a heuristic expiration; this contract answers `heuristic-undecided` instead and never invents a number. That is a chosen narrower profile" | **The one place C2 extends this entry.** C2 is the chosen-profile successor: it gives the number only when Last-Modified ≤ Date and an explicit lifetime is absent. Quote this as the reason the r91 narrowing is now superseded *in a new entry*, not by editing this one. |
| `stored-response-reuse.md:183, 198-208, 231-236, 263-265, 276-290` | Quote table (line 236 names "clause 11 turns into `heuristic-undecided`", line 264-267 adapter conventions incl. "§4.2.1 line 664–667 falls back to receipt time") | Adapter conventions for Date/Expires already in place; C2 inherits the same integer convention (contract clause 5). Consistent. |
| `stored-response-reuse.md:286-290` | "A passing candidate can still be wrong about any RFC behaviour … heuristic freshness" | Limit statement; C2 retires that limit for §4.2.2 only. |
| `vary-matching.md`, `cache-key-conformance-gate.md`, `policy-value-classes.md` | no freshness-decision content (`policy-value-classes.md` S457 row mentions "freshness as age against a freshness lifetime") | No conflict. |

Non-HTTP "freshness" (lane drift sense: `freshness-sweep`, `freshness-sidecar`, `drift-detection.md:23-114`,
`crawl-scope-per-host.md:21-22`): homonym. **Excluded** from C2 composition. Noted so a seat does not
mistake them for HTTP freshness.

### 1c. Retained RFC 9111 §4.2.2 (verified this walk, read-only)

- `.ufo/waves/round-92/L1/src/rfc9111.txt` sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` (matches `freeze.md` pin).
- §4.2.2 heading at plain-text line **686**; body lines 689–708 ("a cache MAY assign a heuristic expiration time …"; "MUST NOT use heuristics … when an explicit expiration time is present"; "… `public` response directive"; "… 10%"). Read directly at lines 686–720.
- §15.1 "heuristically cacheable" set is cited by the RFC (line 699) but **not** retained in `rfc9111.txt`; the 12-code set in the contract is taken from RFC 9110 §15.1 (`.ufo/waves/round-90/L1/src/rfc9110.txt`, retained). Not re-verified here.

### 1d. Registry rows touching §4.2 / §4.2.2

- `corpus/SOURCES.md:204` S457 — §4.2 freshness, §5.2, §5.2.2 (scope excludes "any server's freshness policy"). Covers §4.2 definitions, **not** §4.2.2.
- `corpus/SOURCES.md:208` S461 — §4.2.1 paragraphs 1 and 4. Not §4.2.2.
- `corpus/SOURCES.md:209` S462 — §4.2.3 age arithmetic. Not §4.2.2.
- `corpus/SOURCES.md:215` S469 — §5.2.1, §4.2.1, §4.2.4, §1.2.2. Not §4.2.2.
- `corpus/SOURCES.md:22`/`:18` S028, S454 mention "4.2.2" only as RFC 9110 / cacheability pointers. **No registry row cites RFC 9111 §4.2.2.** A new row is required before C2's knowledge entry cites §4.2.2 (CORPUS rule 1, QUALITY `:1115`).

---

## 2. Composition with `scripts/stored_reuse.py` — the heuristic-undecided decision

The one place the tool returns `heuristic-undecided` (decide(), `scripts/stored_reuse.py`):

```
   222	    # Clauses 11-19: first match wins.
   223	    if lifetime is None:
   224	        decision = "heuristic-undecided"                          # clause 11
```

and its declared contract in the module docstring:

```
    heuristic-undecided    no explicit freshness lifetime; this contract guesses nothing      (:17)
  * no heuristic freshness (RFC 9111 4.2.2) -- with no max-age/s-maxage and no
    Expires the answer is ``heuristic-undecided``, never a guessed lifetime;                 (:30-31)
```

`lifetime is None` (line 223) arises exactly when no shared `s-maxage`, no `max-age`, and no `Expires` is present (lines 196–204). Storability is decided **before** this (lines 211–220), so `heuristic-undecided` is only ever reached for a storable response.

**Composition rules (for the L1 integration, not for a seat to edit):**

1. `stored_reuse.py` must **not** be changed to return a heuristic lifetime. Its `c91_reuse.py` counter scores the frozen 45 hand cases (including `heuristic-undecided` at `stored_reuse.py:306-312`) against contract v1; a changed decision would make the frozen round-91 counter red, and it is not repaired after scoring.
2. The new instrument is a **caller-side second step**: called only when `stored_reuse` returns `heuristic-undecided`. Its `heuristic` / `lifetime` output then feeds nothing that re-decides reuse. The reuse answer stays `heuristic-undecided` in the stored_reuse output; the heuristic lifetime is reported beside it, not as a reuse permission. (C2 contract §Scope already says this.)
3. Clause order divergence to record, not fix:
   - `stored_reuse.py:211-216` storability requires `status in CACHEABLE_STATUS` (the same 12 codes as the counter's `HEURISTICALLY_CACHEABLE`, `c92_heuristic.py:55`) and **does not read `public`**. So for `status=500` + `Cache-Control: public` + `Last-Modified`, `stored_reuse` answers `not-storable`, while C2 clause 11 says `heuristic`. A composed caller would never reach the heuristic step for that response. The contract is correct per RFC 9111 §4.2.2; the gap is in `stored_reuse`'s storability, and it is out of C2's scope. **Route as a composition defect**, not an r92 edit.
   - `stored_reuse.py:213` also treats request `no-store` as not-storable; C2 clause 9 does not. Only stricter; harmless when composed (stored_reuse runs first).
4. Date convention is shared: `stored_reuse.py` `delta(...)` integer-only (lines 1–50 of helpers, `c92_heuristic.py:110-111`), same as contract clause 5. Consistent.
5. Explicit precedence is shared: `stored_reuse.py:196-204` (s-maxage shared → max-age → Expires−Date) equals C2 clause 10 and the counter's reference (`c92_heuristic.py` lines 186–204). Duplicated by design; C2 must **not** re-implement the explicit branch as a second grammar. It should call `scripts/cache_control_effective.py` or accept the explicit lifetime as input — but C2's input is fixed by contract (`stored` + `now` + `shared`), so the explicit branch is necessarily re-derived in C2's own code. Record that as the K91-9 duplication, unchanged this round.

---

## 3. Insertion points for round-92 corpus work

### 3a. `corpus/README.md`

- **Frontier paragraph** (new `## Round-92 frontier step — …` section): append at EOF after the last section.
  - Last section heading: `## Round-91 frontier step — the reuse decision` at **line 718**; file is **734 lines**; the section runs to EOF.
  - Its final sentence (line 733): "…field-specific header normalisation, and every live-cache or browser observation." — the round-92 paragraph should say it supersedes that open-list item for §4.2.2 only (precedent: line 709-711 `## Round-88 frontier step` "The remaining frontier here is …").
- **Coverage-map row** (index row for a new knowledge file): **the first table only** — `## Coverage map` at line 15, the first contiguous table is rows **17–86**; the last row of that table is line **86** (`| Policy-header value classes (r84) | …`). Insert after line 86, before the blank line 87 and `### Frontier ground map (round 55; round-60 update)` at line 88.
  - Why this placement matters: `scripts/c55`-class readme-index counter reads only that first table (`c55_readme_index.py:139-145`). The r91 row sits at **line 135** inside the *frontier* table (lines 102–135), which that counter does not read. Result, measured at HEAD: `C1 readme-index index_mismatches=22 knowledge_files=85 met=False`, `unindexed=19 … coverage_rows=68`, including `stored-response-reuse.md` and `cache-control-effective.md` (`python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision HEAD`, exit 0 printed by the shell wrapper, counter exit not captured by me; the printed `met=False` is the counter's own line). Historical per SKILL row `:1233`, but it shows the placement rule.
- Frontier-ground-map row (optional, `:102-135` table): round-92 row could go after line 135 (`| Stored-response reuse decision … | r91 | … | S469 |`), following the cache-key rows pattern.

### 3b. `SKILL.md` registry table

- Round section heading `## Round 91 — stored-response reuse decision` at **line 1623**; table header **line 1633**; separator line 1633+1 (= 1633 is the header row, 1634 `| stored_reuse | probe | …`, 1635 `| c91 reuse capability | gate | …`).
- Format (8 columns, pipe-delimited, no trailing spaces): two quoted rows:
  - `| stored_reuse | probe | \`printf '%s' '<payload>' \| python3 -B scripts/stored_reuse.py\` with stdin JSON … | 0 clean/decided … | \`TMPDIR=$(mktemp -d) python3 -B scripts/stored_reuse.py --selftest\` → \`selftest 45/45\` | … | stdin/stdout/stderr only … | kake |`
  - `| c91 reuse capability | gate | \`python3 -B .ufo/waves/round-91/c91_reuse.py --root . --revision <rev> --work <explicit-scratch> …\` | 0 clean/met; 1 failed/not-met … | … | … | \`--work\` scratch only … | kake |`
- SKILL.md is pinned in `corpus/knowledge/freshness-sidecar.json`: the largest pinned `SKILL.md` line is **935** (`{'file': 'SKILL.md', 'line': 935, …}`). Append at EOF (below 935) so no pinned line moves. Any SKILL.md edit requires the §paths sweep (QUALITY `:1426`, round-64).
- **Working-tree state observed**: `SKILL.md:1663` `c92_defects.py` and `:1664` `c92_heuristic.py` rows already exist in the working tree (round-92 section heading near line 1650-1660). Whether they are committed at `HEAD` was **not verified** (no git run). Routed K91-2 item B is closed at the revision the rows land in; the L1 must confirm from committed bytes.

### 3c. `SCORECARD.md`

- Round-91 section heading: `## Round 91 — the round-90 instrument defects and a stored-response reuse decision` at **line 5602**.
- `### Planned — after round 91` heading at **line 5631**; section body lines 5633–5640; file ends at **line 5640** (EOF).
- Insertion: append the round-92 section after line 5640 (EOF). The L1 appends after the Planned block; do not edit lines 5602–5640.
- Also: the round-91 Planned text at `:5638-5640` lists "heuristic freshness (§4.2.2) … stay open" — the round-92 section supersedes that item by appended correction, not by edit (append-only; QUALITY `:1524` whole-line quote rule applies to any receipt quoted there).

### 3d. (Also) `PROVINCE.md` — not asked, noted

- `## Round 91 — stored-response reuse decision only` at **line 724**; file ends **line 747**. A round-92 ground section appends at EOF.

---

## 4. Quality criteria a new instrument and a new knowledge entry must satisfy (`corpus/QUALITY.md`)

Line numbers are the bold criterion line in `corpus/QUALITY.md` (verified by grep this walk).

### 4a. New instrument (`scripts/heuristic_freshness.py`) and its counter

| Criterion id (short) | Line | Requirement for C2 |
|---|---|---|
| Counter attacked before it scores — "A counter that gates a claim is run against do-nothing and junk changes …" | 1181 | Counter `c92_heuristic.py` must have been attacked pre-freeze (controls/base-c2.txt, ctl-c2-positive.txt in freeze.md). |
| Selftest tally is the tally its command prints — "A stated selftest tally …" | 1190 | Any registry row stating a count (e.g. `selftest N/N`) must match the printed line. |
| Selftest rebuilt from HEAD names fixture revision — "A selftest that rebuilds from `HEAD` …" | 1199 | Only if the instrument's selftest is `git show`-based; C2 reads a file, so no. |
| Registry Kind cell re-derived at measured revision — "A gate's status label …" | 1362 | `c92_heuristic.py` row Kind = "gate" must be re-run at the carrier. |
| Verdict-map claims only exits it can print — "A registry row's verdict map …" | 1393 | `heuristic_freshness.py` exits: 0 decision printed, 1 invalid_input, 64 usage (per contract). Row must not claim others. |
| Do-nothing control dies — "A frozen counter's claim dies when any do-nothing control …" | 1420 | `controls/base-c2.txt` (candidate=absent) present. ✔ per freeze.md. |
| Round-90 "met only after shown able to say no" — (1) do-nothing `met=false`, (2) a forgery per conjunct, (3) positive `met=true`; capability claim: (3) replaced by a blanket-refuse control and the report states reachability rests on carrier alone | 1761-1775 (block) | C2 is a capability claim: the **blanket-refuse** control must be in the record (freeze.md lists `controls/ctl-c2-positive.txt` only as positive + sandbox differential). The report must state that reachability rests on the carrier. |
| Round-86 measurement downstream of predicate — counter must not require its own future green receipt | 1724 | `c92_heuristic.py` reads committed candidate; it does not require its own receipt. ✔ by inspection (no receipt read; `show` of candidate only). |
| Round-87 source-pinned agreement is metadata — expected decisions must independently match pinned source tables | 1742 | C2 expected decisions come from the contract/RFC §4.2.2 text, not from the candidate. The contract §Grounding quotes must match `L1/src/rfc9111.txt` at lines 689–708. |
| Round-85 field-specific interpretation — "Admit a field-specific parser with its own source algorithm and ordered counterexample; reject blanket semantic equivalence from multiset equality." | 1712-1722 | Cache-Control parsing in C2 is field-specific (directive names lowercased, duplicates refused). Do not compare Cache-Control as a comma multiset. |
| Round-84 field-specific equivalence — reject equivalence from comma-separated multiset | 1703-1709 | Same as above. |
| Whole-line receipt quotes — "A quote of observed output is one whole receipt line …" | 1524 | Any counter output quoted in SCORECARD/report must be a whole line of the receipt. |
| Receipt written after the run — "A receipt is written after the run it records; a placeholder is not a receipt." | 1262 | Receipts under `w1/` must be byte-copies of real runs. |
| Receipt rewrite disclosure — "A measurement receipt rewritten after its first commit is disclosed …" | 1614 (round-79) | Any later edit to a receipt disclosed with blob ids. |
| SKILL.md edits re-run §paths sweep — "A round that edits a sidecar-pinned file re-runs the standing §paths sweep …" | 1426 | Any SKILL.md row edit: run `node scripts/freshness-sweep.mjs --offline` (per QUALITY 1426) before landing. |

### 4b. New knowledge entry (`corpus/knowledge/<heuristic-freshness>.md`)

| Criterion | Line | Requirement |
|---|---|---|
| Entry lands with its index row — 5+ tokens sharing a non-common word, in the **first** coverage table | 1148 (+ c55 `c55_readme_index.py:139-145`) | Row after `corpus/README.md:86` (§3a). |
| New quotes ≤25 units, raw substrings, ≥3 page-unique spans | 1160 | Every quote of RFC 9111 §4.2.2 ≤25 words, raw substring of `L1/src/rfc9111.txt`. |
| Quote substantively supports the proposition | 1412 | e.g. "MAY assign a heuristic expiration time" must state the cache *may*; the 10 % sentence must be attributed as the RFC's "typical setting", not as a rule. The contract already does this (§Grounding). |
| Source locator names the section containing the quote | 1116 | Cite §4.2.2 with heading text "Calculating Heuristic Freshness" at line 686. |
| Source id resolves in this lane's own registry | 1115 | **No registry row cites RFC 9111 §4.2.2** (§1d). A new row (next S-id) must be opened (CORPUS rule 1) and added; S457/S461/S462/S469 may not be widened (QUALITY `:1170` held-row rule: used-by only). |
| Held row reused changes `used-by` only | 1170 | Reusing S469 or S457 for §4.2 context: only the `used-by` cell may change. |
| Validated append block is the appended block | 1174 | Registry append must be byte-equal to the validated scratch. |
| Quote receipts whole | 1524 | Any receipt-quote in the entry must be a whole line of a committed receipt. |
| Measurement receipt not a placeholder | 1262 | n/a unless the entry cites a live receipt (it must not; no live GET is in scope). |
| Scope declaration: no live property, no RFC conformance claim | (QUALITY `:1191`-style; `stored-response-reuse.md:5, 183, 286-290` is the lane precedent) | Entry must say "a decision over supplied integers; not a claim about any deployed cache" (precedent `stored-response-reuse.md:183`). |

---

## 5. Defects and routed findings (from this walk; not repaired)

- **W-1 (index placement).** The round-91 coverage row for `stored-response-reuse.md` sits in the frontier table (`corpus/README.md:135`), outside the first coverage table the readme-index counter reads (17–86). Counter red at HEAD (`index_mismatches=22`, `unindexed=19`). Historical per SKILL `:1233`; the placement defect is not routed in `lessons/round-91.md`. Route: round-92 index row goes in the first table.
- **W-2 (no §4.2.2 registry row).** No `SOURCES.md` row cites RFC 9111 §4.2.2 (§1d). Route: round-92 registers it before citing it.
- **W-3 (composition gap, `public`).** `scripts/stored_reuse.py:211-216` storability omits the `public` storability route the RFC gives (§4.2.2 ¶3 "marked as explicitly cacheable (e.g., with a public response directive)"); a 500+public+Last-Modified response is `not-storable` there and `heuristic` in C2 clause 11. Route to the L1: not repaired this round (the round-91 counter pins that decision). Recommend the L1 record it as a known composition limit.
- **W-4 (SKILL.md working-tree rows).** `SKILL.md:1663-1664` c92 rows exist in the working tree; committed status unverified here. Route: L1 confirms from `git show <carrier>:SKILL.md`.
- **W-5 (duplication, carried).** Explicit lifetime precedence (`stored_reuse.py:196-204`, `cache_control_effective.py:141`, `c92_heuristic.py:186-204`) is implemented three times. Already K91-9 / R91-4 (`corpus/lessons/round-91-verifier-spotcheck.md`, routed). Not repaired here; C2 must not add a fourth without the routed fix.
- **W-6 (open frontier carried).** README `:731-733`, PROVINCE `:724-747`, SCORECARD `:5631-5640` each list §4.2.2 as open. The round-92 section must supersede these by appended text (QUALITY `:1426`, append-only rule).

---

## 6. Limits

- Read the **working tree**, not committed bytes. No `git` run (no mutating command; no read-only `git show` was executed). Committed-revision claims in §3b/§5 W-4 are unverified.
- The `c55` readme-index run printed `met=False` on the counter's own line; the shell wrapper exit code was not captured separately. The counter's `met` line is the claim cited.
- QUALITY lines `1219-1259`, `1262-1290` and `1303-1345` were not re-read in full in this walk (a provider stream stalled mid-read; the criterion ids in §4 are taken from the grep heading list and the bold lines read). The criterion line numbers in §4 are grep-verified; the requirement text for `:1199`, `:1275`, `:1289`, `:1303` is a paraphrase from the bold-line grep, not a full read.
- `scripts/sources-census.sh` is not present in the working tree (`find` returned nothing); the census gate cannot be run from this walk. The round-91 lesson refers to it; flagged as an absent tool, not as a finding against C2.
- No candidate `scripts/heuristic_freshness.py` exists yet (`ls` not run; grep for it not included); C2 candidate status is out of this walk's scope.
- Non-HTTP "freshness" (lane drift instrument) excluded by design (§1b homonym).

## Reproduce

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin
grep -rn -E "stored_reuse\.py|cache_current_age\.py|cache_key\.py|vary_match\.py|cache_control_effective\.py|cache_key_conformance\.py" scripts/ corpus/ SKILL.md PROVINCE.md SCORECARD.md
grep -rn -E "[Hh]uristic|[Ss]tales?|[Ll]ast-[Mm]odified|[Ee]xpires|heuristic freshness|freshness lifetime" corpus/knowledge/
sed -n '222,224p' scripts/stored_reuse.py
sed -n '686,708p' .ufo/waves/round-92/L1/src/rfc9111.txt
sha256sum .ufo/waves/round-92/L1/src/rfc9111.txt
```
