VERDICT: planning data-walk complete; no claim scored (C1 and C2 untouched by this seat).

# ScoutGround — round-92 data-walk report

Seat: ScoutGround (scout, leaf). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Freeze pin read: `a5640ca02c20f94a0fa03af41b977b46ae99808e` (from `freeze.md`). Working-tree reads only.

Full recon: `.ufo/waves/round-92/w1/ScoutGround/Recon.md`. Grep output: `.ufo/waves/round-92/w1/ScoutGround/hits.txt` (253 lines).

## 1. Existing freshness material — what C2 duplicates, extends, contradicts

- **Duplicates** (consistent, nothing to fix): explicit lifetime precedence `s-maxage` (shared) → `max-age` → `Expires−Date` is implemented in `scripts/stored_reuse.py:196-204` and mirrored by C2 clause 10 and the counter reference (`c92_heuristic.py` ~186-204). Date/Expires integer-epoch convention: `stored-response-reuse.md:263-265`, `stored_reuse.py` `delta()`, C2 clause 5. `cache-control-effective.md:16` already says "heuristic freshness is a separate question".
- **Extends**: `corpus/knowledge/stored-response-reuse.md:55-57` ("No heuristic freshness … never invents a number. That is a chosen narrower profile") is the exact r91 narrowing C2 takes up. Supersede by a new entry, not an edit.
- **Contradicts**: nothing in C2's contract contradicts the lane. One **composition gap**: `scripts/stored_reuse.py:211-216` storability requires a status in the 12-code set and never reads `public`; RFC 9111 §4.2.2 (retained `L1/src/rfc9111.txt:695-699`) lets `public` make a non-heuristically-cacheable status heuristic. So `status=500 + public + Last-Modified` is `not-storable` in stored_reuse and `heuristic` in C2. Recorded as W-3, not repaired.
- Homonym excluded: lane drift "freshness" (`freshness-sweep`, `freshness-sidecar`, `drift-detection.md`) is not HTTP freshness.

## 2. The `heuristic-undecided` decision C2 must compose with

`scripts/stored_reuse.py:222-224`:

```
   222	    # Clauses 11-19: first match wins.
   223	    if lifetime is None:
   224	        decision = "heuristic-undecided"                          # clause 11
```

Docstring `:17` "heuristic-undecided    no explicit freshness lifetime; this contract guesses nothing" and `:30-31` "no heuristic freshness (RFC 9111 4.2.2) -- … the answer is ``heuristic-undecided``, never a guessed lifetime".

Rule: C2 is a caller-side second step invoked only on `heuristic-undecided`. It must not change `stored_reuse.py` (the frozen round-91 counter `c91_reuse.py` pins that decision via `stored_reuse.py:306-312`) and must not re-decide reuse. Its `heuristic`/`lifetime` output sits beside the undecided reuse answer.

## 3. Insertion points

- **`corpus/README.md`**: new frontier section `## Round-92 frontier step …` appended after the last heading `## Round-91 frontier step — the reuse decision` at **line 718** (file 734 lines, EOF). Supersedes the open-list at `:731-733` for §4.2.2 only.
- **`corpus/README.md` index row**: first coverage table only, rows **17–86**; insert after **line 86** (`| Policy-header value classes (r84) | …`). The r91 row at `:135` sits in the frontier table, which the readme-index counter does not read; measured at HEAD `index_mismatches=22 unindexed=19 met=False` (`c55_readme_index.py`).
- **`SKILL.md` registry**: round section heading `## Round 91 — stored-response reuse decision` at **line 1623**; table header **line 1633**; example rows **1634** (`| stored_reuse | probe | \`printf '%s' '<payload>' \| python3 -B scripts/stored_reuse.py\` … | …`) and **1635** (`| c91 reuse capability | gate | \`python3 -B .ufo/waves/round-91/c91_reuse.py --root . --revision <rev> …\` | …`). Eight columns. Append at EOF; the largest `SKILL.md` line pinned in `freshness-sidecar.json` is **935**, so no pinned line moves. Working-tree rows `c92_defects.py` (`:1663`) and `c92_heuristic.py` (`:1664`) exist; committed status **not verified**.
- **`SCORECARD.md`**: `## Round 91 …` at **line 5602**; `### Planned — after round 91` at **line 5631**; EOF **line 5640**. Append the round-92 section after 5640; do not edit 5602–5640.

## 4. QUALITY criteria a new instrument and entry must satisfy (`corpus/QUALITY.md`)

Instrument / counter: attacked before scoring **1181**; selftest tally = printed tally **1190**; registry Kind re-derived at measured revision **1362**; verdict map claims only printable exits **1393**; do-nothing control **1420**; round-90 "able to say no" (do-nothing `met=false`, forgery per conjunct, positive `met=true`; capability claim: blanket-refuse control replaces the positive and the report states carrier-only reachability) **1761**; measurement downstream of predicate **1724**; source-pinned agreement is metadata **1742**; field-specific parse, no multiset equivalence **1703-1722**; whole-line receipt quotes **1524**; receipt after run **1262**; SKILL edit re-runs §paths sweep **1426**.

Knowledge entry: index row lands with entry **1148**; quotes ≤25 units, raw substring, ≥3 page-unique **1160**; quote supports proposition **1412**; source locator names section **1116**; source id resolves in lane registry **1115** (no RFC 9111 §4.2.2 row exists, see W-2); held row changes `used-by` only **1170**; append block byte-equal **1174**.

## 5. Defects found (routed, not repaired)

- **W-1** r91 index row in the frontier table, outside the first coverage table the counter reads (`corpus/README.md:135`; readme-index counter red at HEAD, `index_mismatches=22`). Round-92 index row goes after `:86`.
- **W-2** No `corpus/SOURCES.md` row cites RFC 9111 §4.2.2 (S457/S461/S462/S469 cover §4.2, §4.2.1, §4.2.3, §4.2.4 only). A row is needed before the entry cites §4.2.2.
- **W-3** `stored_reuse.py:211-216` storability omits the `public` route (composition gap above).
- **W-4** `SKILL.md:1663-1664` c92 rows: committed status unverified (working-tree read only). L1 confirms from committed bytes.
- **W-5** explicit-lifetime precedence implemented three times (`stored_reuse.py:196-204`, `cache_control_effective.py:141`, `c92_heuristic.py`); already routed as K91-9 / R91-4.
- **W-6** README `:731-733`, PROVINCE `:724-747`, SCORECARD `:5631-5640` list §4.2.2 as open; the round-92 text must supersede by appended text.

## 6. Honest limits

- Working-tree reads only; no `git` run of any kind. Committed-revision facts are unverified where stated.
- A provider stream stalled mid-walk. QUALITY `:1219-1259`, `:1262-1290`, `:1303-1345` were not re-read in full; the criteria in §4 are grep-verified by line and bold text, with paraphrase for `:1199`, `:1275`, `:1289`, `:1303`.
- `scripts/sources-census.sh` is absent from the working tree (`find` empty); the census gate cannot be run from this seat.
- The `c55` counter's shell wrapper exit was not captured separately; its own `met=False` line is cited.
- No `scripts/heuristic_freshness.py` candidate was checked for existence (out of scope for a planning walk).

## 7. Tools, installs, writes

- Installs: none. Network: none. Git mutations: none. Fixtures/scratch: none created (no `/fast/scratch` tree, nothing to delete).
- Writes: `.ufo/waves/round-92/w1/ScoutGround/Recon.md`, `.ufo/waves/round-92/w1/ScoutGround/hits.txt`, `.ufo/waves/round-92/w1/ScoutGround.md`.
- Read-only runs: `grep`, `sed`, `python3` one-liner over `corpus/knowledge/freshness-sidecar.json` (max SKILL.md line 935), and `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision HEAD` (read-only; output as above).
