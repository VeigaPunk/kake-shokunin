# ConnectorScope — evidence receipts (round-87 w1, read-only seat)

All commands run 2026-11-04, cwd `/home/vgpnk/Projects/shokunin/kake-shokunin` (reads only; no writes outside this wave dir; scratch `/fast/scratch/hyaku/kake-r87/ConnectorScope/` created then deleted, receipts retained here first).

## 1. Snapshot digests vs expected-ledger.json bindings

`sha256sum .ufo/waves/round-87/snapshots/round-{84,85,86}-verifier-spotcheck.md`

```
80f48887b1e5f2e9d7d54adcce19d8b935f77fc0b236620abac3335b730dfda9  round-84-verifier-spotcheck.md
948c316831d0c71927e6a29501f05037b3faa940a251984ed28ca8f0eee2ce71  round-85-verifier-spotcheck.md
47499686bc976564c43174fdeeae2219e0db2351c571678ba35caff0a34de42b  round-86-verifier-spotcheck.md
```

All three equal the `sha256` fields in `.ufo/waves/round-87/expected-ledger.json` (3 rows each bind r84; 2 rows bind r85; 3 rows bind r86).

## 2. Base/freeze objects and do-nothing red

```
git cat-file -t 86ca7803fd964db7ae2a628c7e9048741c78a45f -> commit
git cat-file -t 58fee726102aa89ad2c1fa9f697869de3a212510 -> commit
git merge-base --is-ancestor 58fee726… HEAD -> ANCESTOR_YES (HEAD 0f5739f9)
git cat-file -e <base>:scripts/cache_current_age.py           -> fatal: path does not exist (BASE_NO_TOOL)
git cat-file -e <base>:corpus/knowledge/gate-agreement-ledger.json -> fatal (BASE_NO_LEDGER)
git cat-file -e <freeze>:scripts/cache_current_age.py          -> fatal (FREEZE_NO_TOOL)
git cat-file -e <freeze>:corpus/knowledge/gate-agreement-ledger.json -> fatal (FREEZE_NO_LEDGER)
```

## 3. Spotcheck gate tables == frozen rows (independent read)

- r84 snapshot lines 73–75: `S457 response max-age semantics | admit/mined | … | agree`; `§4.1 normalization… | reject | … | agree`; `§5.2.2.2 as max-age anchor | reject | … | agree` → 3 rows, matches expected rows 1–3.
- r85 snapshot lines 71–72: `S458 field-specific algorithm | admit | … | agree`; `Blanket response-policy reorder equivalence | reject | … | agree` → 2 rows, matches expected rows 4–5.
- r86 snapshot spot-check table: `S459 CrUX Vis docs | admit | agree`; `S461 RFC 9111 slice | admit | agree`; `RFC 7234 minimum-duplicate attribution | reject | agree` → 3 rows, matches expected rows 6–8.
- Totals: 8 decisions, 8 `outside=agree`, 0 mismatches — the population C1 freezes.

## 4. D84-4 routing still open (fleet L0, not lane)

`grep -n "kake | round-8" /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` → line 294 only:
`kake | round-86 | Routed defect D84-4: … Round 86 proceeds with the mitigation and this routing; no answer blocks it.`
Line 295 (kotodama round-86) names the same unresolved planner conflict. No answer line exists. The lane has no `.ufo/l0-questions.md` (checked: absent).

## 5. README debt block (D84-2/D84-3 retained-open) present at HEAD

`corpus/README.md` lines 671–683: `## Open instrument debt (round 86)` — "Retained-open per the round-85 non-author routing; disposition, not repair"; D84-2 and D84-3 rows each carry `flip:` conditions; D84-3 row ends "this field reader alone does not close it." Lines 665–668: "General policy equivalence, the independent changed-row oracle, full HTTP extraction, **Age/Vary/Pragma**, browser/runtime cache behavior and live property repair remain frontier."

## 6. Duplicate-capability scan (bounded grep)

`grep -ri "current_age|apparent_age|corrected_age|age_value|resident_time|response_delay" scripts/` → **No matches found** (45 existing scripts). `glob **/cache_current_age*.py` → **No files found**. Nearest neighbor: `scripts/cache_control_effective.py` (r86 row: "First-occurrence local profile, shared/private precedence, explicit Expires+Date, directive flags; not cache storage/reuse authorization"). `grep -c "S462" corpus/SOURCES.md` → **0** (id unused).

## 7. Inherited r86 mirror disposal state

`ls .ufo/waves/round-86/w1/ExecAssim/mirror/corpus/lessons/round-81-gate/` → only `rfc9110.txt` (502,941 B). `git cat-file -e HEAD:…rfc9110.html` → fatal (HTML_NOT_AT_HEAD); `git log --all -- …rfc9110.html` → empty (never committed). `git log --follow -- …rfc9110.txt` → `3f2de0fd round-86: land bounded cache reader…` (tracked since the r86 carrier, before the spotcheck that named only the untracked 1.2 M html as the defect).

## 8. Frozen age-cases shape (read)

`.ufo/waves/round-87/age-cases.json` — 17 case objects; visible tail shows 5 exit-1 invalids: inverted local time (`now < response_time`), negative `age_value`, boolean `date_value` (integer-not-bool rule), missing required key.

## 9. Sibling scope check (w1-spec.json, read-only)

ScoutAge: data-walk explicitly excludes "cache storage/reuse, browser, publishing and missing Date"; proposes S462 only. ExecAge: candidate only under own dir. ExecTrial: ONE GET to owned public https://ds4cc.com/, sanitized record, no cookies/auth retained, missing/invalid Date → could-not-evaluate. ScribeRegistry: "PROVINCE scoped frontier update **(Age arithmetic only)**". ScribeLesson: "Explain Gate agreement ledger is calibration metadata not domain knowledge". No sibling item touches browser execution (tabi), research method (chousa), secrets (kagi), or model serving (kama): no province absorption.
